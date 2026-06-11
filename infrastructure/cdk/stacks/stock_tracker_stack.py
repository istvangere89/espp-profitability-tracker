"""
CDK Stack for EPAM Stock Tracker
- S3 bucket for static website hosting
- CloudFront distribution
- Lambda function for CORS proxy
- API Gateway with throttling (10-25 users)
- CloudWatch alarms for monitoring
"""

from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
    CfnOutput,
    RemovalPolicy,
    Duration
)
from constructs import Construct


class StockTrackerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, waf_acl_arn: str = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ========================================
        # Lambda CORS Proxy Function
        # ========================================
        cors_proxy_lambda = lambda_.Function(
            self, "CorsProxyFunction",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="index.handler",
            code=lambda_.Code.from_asset("../lambda/cors_proxy"),
            timeout=Duration.seconds(30),
            memory_size=256,
            description="CORS proxy for stock and currency APIs"
        )

        # Grant Lambda permission to make HTTP requests
        cors_proxy_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                resources=["*"]
            )
        )

        # ========================================
        # API Gateway CloudWatch Role (Account-level)
        # ========================================
        # API Gateway needs a CloudWatch Logs role at the account level
        # This is a one-time setup, but we create it here for automation
        cloudwatch_role = iam.Role(
            self, "ApiGatewayCloudWatchRole",
            assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonAPIGatewayPushToCloudWatchLogs"
                )
            ]
        )

        # Set the CloudWatch Logs role for API Gateway account settings
        # This is idempotent and only needs to be done once per region
        apigateway.CfnAccount(
            self, "ApiGatewayAccount",
            cloud_watch_role_arn=cloudwatch_role.role_arn
        )

        # ========================================
        # API Gateway for Lambda with Throttling
        # ========================================
        api = apigateway.RestApi(
            self, "CorsProxyApi",
            rest_api_name="Stock Tracker CORS Proxy",
            description="CORS proxy with throttling for 10-25 users",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["*"]
            ),
            deploy_options=apigateway.StageOptions(
                stage_name="prod",
                # Throttling for 10-25 users
                throttling_rate_limit=10,        # 10 requests per second
                throttling_burst_limit=50,       # Handle concurrent spikes
                # Monitoring
                metrics_enabled=True,            # Track usage in CloudWatch
                logging_level=apigateway.MethodLoggingLevel.INFO,
                data_trace_enabled=False,        # Don't log bodies (privacy)
                # Optional: Server-side caching (costs ~$0.02/hour)
                # Uncomment to enable caching in addition to browser caching
                # caching_enabled=True,
                # cache_ttl=Duration.hours(1),
                # cache_data_encrypted=True
            )
        )

        # Add Lambda integration (proxy=True passes query params and full event)
        proxy_integration = apigateway.LambdaIntegration(
            cors_proxy_lambda,
            proxy=True  # Enable Lambda proxy integration to pass query parameters
        )

        # Add GET method
        api.root.add_method("GET", proxy_integration)

        # ========================================
        # S3 Bucket for Static Website
        # ========================================
        # Note: When using OAC, bucket should NOT be configured as a website
        # CloudFront serves files directly from S3 using OAC
        website_bucket = s3.Bucket(
            self, "WebsiteBucket",
            bucket_name=f"epam-stock-tracker-{self.account}",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # ========================================
        # CloudFront Distribution with OAC
        # ========================================
        # Create Origin Access Control (OAC) for secure S3 access
        oac = cloudfront.S3OriginAccessControl(
            self, "OAC",
            signing=cloudfront.Signing.SIGV4_NO_OVERRIDE
        )
        
        # Create S3 origin with OAC
        s3_origin = origins.S3BucketOrigin.with_origin_access_control(
            website_bucket,
            origin_access_control=oac
        )

        # Build CloudFront distribution configuration
        distribution_props = {
            "default_behavior": cloudfront.BehaviorOptions(
                origin=s3_origin,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD,
                compress=True
            ),
            "default_root_object": "index.html",
            "error_responses": [
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.minutes(5)
                )
            ],
            "price_class": cloudfront.PriceClass.PRICE_CLASS_100,
            "comment": "EPAM Stock Tracker Distribution"
        }
        
        # Add WAF if ARN is provided
        if waf_acl_arn:
            distribution_props["web_acl_id"] = waf_acl_arn

        distribution = cloudfront.Distribution(
            self, "WebsiteDistribution",
            **distribution_props
        )

        # ========================================
        # Deploy Website Files to S3
        # ========================================
        s3deploy.BucketDeployment(
            self, "DeployWebsite",
            sources=[s3deploy.Source.asset("../../src")],
            destination_bucket=website_bucket,
            distribution=distribution,
            distribution_paths=["/*"]
        )

        # ========================================
        # CloudWatch Alarms for API Gateway Throttling
        # ========================================
        
        # Optional: Create SNS topic for alarm notifications
        # Uncomment and add your email to receive alerts
        # alarm_topic = sns.Topic(
        #     self, "AlarmTopic",
        #     display_name="Stock Tracker Alarms",
        #     topic_name="stock-tracker-alarms"
        # )
        # alarm_topic.add_subscription(
        #     sns.Subscription(self, "EmailSubscription",
        #         endpoint="your-email@example.com",
        #         protocol=sns.SubscriptionProtocol.EMAIL
        #     )
        # )
        
        # Alarm: High number of 4XX errors (client errors)
        api_4xx_alarm = cloudwatch.Alarm(
            self, "Api4xxErrorAlarm",
            metric=cloudwatch.Metric(
                namespace="AWS/ApiGateway",
                metric_name="4XXError",
                dimensions_map={
                    "ApiName": api.rest_api_name
                },
                statistic="Sum",
                period=Duration.minutes(5)
            ),
            evaluation_periods=2,
            threshold=50,  # Alert if >50 4XX errors in 10 minutes
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description="High number of 4XX errors in API Gateway",
            alarm_name="StockTracker-API-4XX-Errors",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
        )
        
        # Alarm: API Gateway throttling (429 errors)
        api_throttle_alarm = cloudwatch.Alarm(
            self, "ApiThrottleAlarm",
            metric=api.metric_client_error(
                statistic="Sum",
                period=Duration.minutes(5)
            ),
            evaluation_periods=1,
            threshold=10,  # Alert if >10 throttle events in 5 minutes
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description="API Gateway throttling limit being hit frequently",
            alarm_name="StockTracker-API-Throttling",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
        )
        
        # Alarm: Lambda errors
        lambda_error_alarm = cloudwatch.Alarm(
            self, "LambdaErrorAlarm",
            metric=cors_proxy_lambda.metric_errors(
                statistic="Sum",
                period=Duration.minutes(5)
            ),
            evaluation_periods=1,
            threshold=5,  # Alert if >5 Lambda errors in 5 minutes
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description="Lambda function experiencing errors",
            alarm_name="StockTracker-Lambda-Errors",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
        )
        
        # Alarm: Lambda duration (timeout warning)
        lambda_duration_alarm = cloudwatch.Alarm(
            self, "LambdaDurationAlarm",
            metric=cors_proxy_lambda.metric_duration(
                statistic="Average",
                period=Duration.minutes(5)
            ),
            evaluation_periods=2,
            threshold=25000,  # Alert if average duration >25 seconds (timeout is 30s)
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description="Lambda function approaching timeout limit",
            alarm_name="StockTracker-Lambda-Duration",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
        )
        
        # If SNS topic is created, add actions to alarms:
        # api_4xx_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))
        # api_throttle_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))
        # lambda_error_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))
        # lambda_duration_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # ========================================
        # Outputs
        # ========================================
        CfnOutput(
            self, "WebsiteURL",
            value=f"https://{distribution.distribution_domain_name}",
            description="CloudFront URL for the Stock Tracker website"
        )

        CfnOutput(
            self, "ApiEndpoint",
            value=api.url,
            description="API Gateway endpoint for CORS proxy"
        )

        CfnOutput(
            self, "S3BucketName",
            value=website_bucket.bucket_name,
            description="S3 bucket name for website files"
        )

        CfnOutput(
            self, "ApiUrlForConfig",
            value=f"{api.url}?url=",
            description="Use this as the proxy URL in api.js (replace http://localhost:8080?url=)"
        )
        
        CfnOutput(
            self, "CloudWatchDashboard",
            value=f"https://console.aws.amazon.com/cloudwatch/home?region={self.region}#alarmsV2:",
            description="CloudWatch Console - View alarms and metrics"
        )
