# 🚀 AWS Deployment Guide

This guide explains how to deploy the EPAM Stock Tracker to AWS using CDK.

## 🎯 Deployment Options

### Option 1: Automated GitHub Actions (Recommended)

The easiest way to deploy is using GitHub Actions CI/CD:

**Benefits:**
- ✅ Fully automated on push to `main`
- ✅ Runs tests before deployment
- ✅ No local setup required
- ✅ Consistent deployments
- ✅ Deployment history tracked

**Setup Steps:**
1. Create OIDC role in AWS
2. Add `AWS_GITHUB_ROLE_ARN` secret to GitHub
3. Push to `main` branch

**See:** [.github/workflows/README.md](../.github/workflows/README.md) for complete setup instructions.

**Target Region:** eu-central-1 (Frankfurt)

### Option 2: Manual CLI Deployment

Deploy from your local machine using the deployment script.

## 📋 Prerequisites

1. **AWS Account** - You need an AWS account ([sign up here](https://aws.amazon.com/))

2. **AWS CLI** - Install and configure AWS CLI:
   ```bash
   # Install AWS CLI (Windows)
   msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
   
   # Configure with your credentials
   aws configure
   ```

3. **Node.js & npm** - Required for AWS CDK:
   - Download from [nodejs.org](https://nodejs.org/) (LTS version recommended)

4. **AWS CDK** - Install globally:
   ```bash
   npm install -g aws-cdk
   ```

5. **Python 3.x** - Already installed (you're using it for the local server)

## 🎯 Quick Deployment

Run the automated deployment script:

```bash
python scripts/deploy.py
```

This script will:
1. ✅ Check if CDK is installed
2. ✅ Install CDK dependencies
3. ✅ Bootstrap your AWS account (first time only)
4. ✅ Deploy the infrastructure
5. ✅ Update `src/js/api.js` with the API Gateway URL
6. ✅ Redeploy with the updated configuration
7. ✅ Show you the website URL

## 🏗️ What Gets Deployed

### Infrastructure Components:

1. **S3 Bucket**
   - Stores your static website files (HTML, CSS, JS)
   - Private bucket (not publicly accessible directly)

2. **CloudFront Distribution**
   - Global CDN for fast content delivery
   - HTTPS enabled by default
   - Caches your website globally
   - **WAF Protection**: Rate limiting + protection against common exploits

3. **Lambda Function**
   - Replaces the local Python proxy server
   - Handles CORS for API requests
   - Fetches stock prices and exchange rates
   - Returns Cache-Control headers (1-hour cache)

4. **API Gateway**
   - REST API endpoint for the Lambda function
   - CORS enabled for browser access
   - **Throttling**: 10 req/s rate limit, 50 burst (optimized for 10-25 users)
   - Pay-per-request pricing
   - Optional server-side caching (disabled by default to avoid costs)

5. **AWS WAF (Web Application Firewall)**
   - **Rate Limiting**: 100 requests per 5 minutes per IP address
   - **AWS Managed Rules**: Protection against common web exploits
   - **Known Bad Inputs**: Blocks malicious request patterns
   - Cost: ~$5-10/month + $0.60 per million requests

6. **CloudWatch Alarms**
   - Monitors API Gateway throttling
   - Alerts on 4XX/5XX errors
   - Tracks Lambda errors and duration
   - Free tier: 10 alarms free, then $0.10/alarm/month

### Caching Strategy:

**Browser Caching (Enabled)**:
- Lambda responses include `Cache-Control: public, max-age=3600`
- Browsers cache API responses for 1 hour
- Reduces Lambda invocations and external API calls
- No additional cost

**API Gateway Caching (Optional)**:
- Server-side caching at API Gateway level
- Costs ~$0.02/hour (~$15/month) for 0.5GB cache
- Enable by uncommenting in `cdk/stock_tracker_stack.py`
- Only recommended for high-traffic scenarios

**Recommendation**: Use browser caching (default) for personal use to stay in free tier.

### Cost Estimate:
- **CloudFront**: ~$0.10/GB + $0.01 per 10,000 requests
- **Lambda**: 1M requests free per month, then $0.20 per 1M
- **API Gateway**: 1M requests free for 12 months, then $3.50 per 1M
- **S3**: ~$0.023 per GB storage
- **WAF**: $5/month + $1 per rule + $0.60 per 1M requests
- **CloudWatch Alarms**: 10 free alarms, then $0.10/alarm/month

**Expected cost for 10-25 users:**
- **First year**: ~$5-8/month (free tier covers most costs, WAF is main cost)
- **After first year**: ~$8-12/month (includes all services)

**Without WAF**: ~$1-3/month (if you prefer minimal cost, comment out WAF in CDK)

## 📝 Manual Deployment Steps

If you prefer manual deployment:

### 1. Install CDK dependencies:
```bash
cd infrastructure/cdk
pip install -r requirements.txt
```

### 2. Bootstrap CDK (first time only):
```bash
cdk bootstrap
```

### 3. Preview the deployment:
```bash
cdk diff
```

### 4. Deploy:
```bash
cdk deploy
```

### 5. Get outputs:
```bash
cdk output
```

### 6. Update api.js:
Copy the `ApiUrlForConfig` output and replace `http://localhost:8080?url=` in `src/js/api.js` with that URL.

### 7. Redeploy to upload updated files:
```bash
cdk deploy
```

## 🔧 Stack Configuration

The CDK stack creates:

```
EpamStockTrackerStack
├── Lambda Function (Python 3.11)
│   ├── CORS proxy handler
│   └── 30-second timeout
├── API Gateway REST API
│   ├── GET / endpoint
│   └── CORS enabled
├── S3 Bucket
│   ├── Website files
│   └── Private (CloudFront access only)
└── CloudFront Distribution
    ├── HTTPS enabled
    ├── Global caching
    └── Error handling (404 → index.html)
```

## 🌐 Accessing Your App

After deployment, you'll get a CloudFront URL like:
```
https://d1234567890abc.cloudfront.net
```

Open this URL in your browser to use your app!

## 🔄 Updating the App

To deploy changes:

1. Make your changes to the code
2. Run: `python deploy.py` (or `cd cdk && cdk deploy`)
3. CloudFront cache will be invalidated automatically
4. Changes appear in ~1-2 minutes

## 🗑️ Cleanup / Destroy

To remove all AWS resources:

```bash
cd cdk
cdk destroy
```

Confirm with 'y' when prompted. This will:
- Delete the CloudFront distribution
- Empty and delete the S3 bucket
- Delete the Lambda function
- Delete the API Gateway
- Remove all associated resources

**Note**: This is permanent and cannot be undone!

## 🔐 Security Notes

- All API calls go through Lambda (no direct API keys in browser)
- S3 bucket is private (only CloudFront can access)
- HTTPS enforced on CloudFront
- No authentication required (personal use app)
- Data stored locally in browser (not on AWS)

## � Monitoring & Alarms

After deployment, CloudWatch alarms monitor your application:

### Alarms Created:

1. **API 4XX Errors Alarm**
   - Triggers if >50 client errors in 10 minutes
   - Usually means bad requests or throttling

2. **API Throttling Alarm**
   - Triggers if >10 throttle events in 5 minutes
   - Means rate limits are being hit frequently

3. **Lambda Errors Alarm**
   - Triggers if >5 Lambda errors in 5 minutes
   - Indicates external API issues or bugs

4. **Lambda Duration Alarm**
   - Triggers if average duration >25 seconds
   - Warning that Lambda is approaching 30s timeout

### View Alarms:

```bash
# AWS CLI
aws cloudwatch describe-alarms --alarm-name-prefix "StockTracker"

# Or open CloudWatch Console (URL in deployment outputs)
```

### Enable Email Notifications (Optional):

To receive email alerts, uncomment the SNS topic section in `cdk/stock_tracker_stack.py`:

```python
alarm_topic = sns.Topic(
    self, "AlarmTopic",
    display_name="Stock Tracker Alarms"
)
alarm_topic.add_subscription(
    sns.Subscription(self, "EmailSubscription",
        endpoint="your-email@example.com",
        protocol=sns.SubscriptionProtocol.EMAIL
    )
)
```

Then uncomment the alarm actions at the bottom:
```python
api_4xx_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))
# ... repeat for other alarms
```

Redeploy with `cdk deploy` and confirm email subscription.

## 🛡️ WAF Protection Details

### WAF Rules Enabled:

1. **Rate Limiting**
   - 100 requests per 5 minutes per IP address
   - Prevents DDoS and abuse
   - Cost-effective for 10-25 users

2. **AWS Managed Rules - Common Rule Set**
   - Protects against OWASP Top 10 vulnerabilities
   - SQL injection, XSS, etc.
   - Automatically updated by AWS

3. **AWS Managed Rules - Known Bad Inputs**
   - Blocks known malicious patterns
   - Invalid request formats
   - Reduces noise and spam

### View WAF Metrics:

```bash
# Check blocked requests
aws wafv2 get-sampled-requests \
  --web-acl-arn <WAF-ARN-from-outputs> \
  --rule-metric-name RateLimitRule \
  --scope CLOUDFRONT \
  --time-window StartTime=<timestamp>,EndTime=<timestamp> \
  --max-items 100
```

Or view in AWS Console: WAF & Shield → Web ACLs → StockTrackerWebACL

### Adjust WAF Rules:

To change rate limit (e.g., for more users), edit `cdk/stock_tracker_stack.py`:

```python
limit=200,  # Change from 100 to 200 requests per 5 min
```

### Disable WAF (To Save Costs):

If you want minimal cost, comment out the WAF section and remove from CloudFront:

```python
# distribution = cloudfront.Distribution(
#     ...
#     web_acl_id=waf_web_acl.attr_arn,  # Comment this line
# )
```

This saves ~$5/month but removes DDoS protection.

## 📊 Monitoring Dashboard

After deployment, view metrics at:
- CloudWatch URL in deployment outputs
- Metrics to monitor:
  - **API Gateway**: Count, 4XXError, Latency, CacheHitCount
  - **Lambda**: Invocations, Duration, Errors, Throttles
  - **WAF**: AllowedRequests, BlockedRequests
  - **CloudFront**: Requests, BytesDownloaded, 4xxErrorRate

## �🐛 Troubleshooting

### CDK not found
```bash
npm install -g aws-cdk
```

### AWS credentials not configured
```bash
aws configure
```

### Bootstrap failed
Make sure you have IAM permissions to create CloudFormation stacks.

### Deployment fails
- Check AWS CLI is configured: `aws sts get-caller-identity`
- Ensure you're using CDK v2: `cdk --version`
- Check CloudFormation console for detailed errors

### CloudFront URL shows error
- Wait 2-3 minutes for CloudFront distribution to fully deploy
- Check S3 bucket has files uploaded
- Check CloudFront origin configuration

### API calls failing
- Verify API Gateway endpoint in api.js matches the deployed URL
- Check Lambda function logs in CloudWatch
- Test API endpoint directly: `https://your-api.execute-api.region.amazonaws.com/prod/?url=https://api.exchangerate-api.com/v4/latest/USD`

## 💡 Tips

1. **Custom Domain**: Add Route53 and ACM certificate to use your own domain
2. **Monitoring**: Check CloudWatch for Lambda logs and API Gateway metrics
3. **Caching**: CloudFront caches for 24h by default, invalidate manually if needed
4. **Costs**: Monitor AWS Cost Explorer to track spending

## 📚 Learn More

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [CloudFront Pricing](https://aws.amazon.com/cloudfront/pricing/)
- [Lambda Pricing](https://aws.amazon.com/lambda/pricing/)
- [API Gateway Pricing](https://aws.amazon.com/api-gateway/pricing/)
