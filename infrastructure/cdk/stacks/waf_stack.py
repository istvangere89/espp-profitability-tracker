"""
CDK Stack for CloudFront WAF WebACL
Must be deployed to us-east-1 for CloudFront compatibility
"""

from aws_cdk import (
    Stack,
    aws_wafv2 as wafv2,
    CfnOutput
)
from constructs import Construct


class WafStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ========================================
        # CloudFront WAF WebACL (us-east-1 only)
        # ========================================
        self.waf_web_acl = wafv2.CfnWebACL(
            self, "CloudFrontWebACL",
            scope="CLOUDFRONT",  # Must be CLOUDFRONT for CloudFront distributions
            default_action=wafv2.CfnWebACL.DefaultActionProperty(
                allow={}  # Allow by default
            ),
            rules=[
                # Rule 1: Rate limiting (100 requests per 5 minutes per IP)
                wafv2.CfnWebACL.RuleProperty(
                    name="RateLimitRule",
                    priority=1,
                    statement=wafv2.CfnWebACL.StatementProperty(
                        rate_based_statement=wafv2.CfnWebACL.RateBasedStatementProperty(
                            limit=100,  # 100 requests per 5 minutes
                            aggregate_key_type="IP"
                        )
                    ),
                    action=wafv2.CfnWebACL.RuleActionProperty(
                        block={}  # Block if rate limit exceeded
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        sampled_requests_enabled=True,
                        cloud_watch_metrics_enabled=True,
                        metric_name="RateLimitRule"
                    )
                ),
                # Rule 2: AWS Managed Rules - Core Rule Set (basic protection)
                wafv2.CfnWebACL.RuleProperty(
                    name="AWSManagedRulesCommonRuleSet",
                    priority=2,
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            vendor_name="AWS",
                            name="AWSManagedRulesCommonRuleSet"
                        )
                    ),
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(
                        none={}  # Use rule group's actions
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        sampled_requests_enabled=True,
                        cloud_watch_metrics_enabled=True,
                        metric_name="AWSManagedRulesCommonRuleSet"
                    )
                ),
                # Rule 3: AWS Managed Rules - Known Bad Inputs
                wafv2.CfnWebACL.RuleProperty(
                    name="AWSManagedRulesKnownBadInputsRuleSet",
                    priority=3,
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            vendor_name="AWS",
                            name="AWSManagedRulesKnownBadInputsRuleSet"
                        )
                    ),
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(
                        none={}
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        sampled_requests_enabled=True,
                        cloud_watch_metrics_enabled=True,
                        metric_name="AWSManagedRulesKnownBadInputsRuleSet"
                    )
                )
            ],
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                sampled_requests_enabled=True,
                cloud_watch_metrics_enabled=True,
                metric_name="StockTrackerWebACL"
            ),
            description="WAF protection for Stock Tracker CloudFront (rate limiting + common exploits)"
        )

        # ========================================
        # Outputs
        # ========================================
        CfnOutput(
            self, "WAFWebACLArn",
            value=self.waf_web_acl.attr_arn,
            description="WAF WebACL ARN for CloudFront (deployed in us-east-1)",
            export_name="StockTrackerWAFArn"
        )
