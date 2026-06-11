# 🛡️ Security & Monitoring Implementation Summary

## ✅ What Was Implemented

### 1. API Gateway Throttling (10-25 Users)

**Configuration:**
- **Rate Limit**: 10 requests/second across all users
- **Burst Limit**: 50 requests (handles concurrent spikes)
- **Monitoring**: CloudWatch metrics enabled

**Why These Limits:**
```
25 users × 3 refreshes/day = 75 requests/day
÷ 24 hours = ~3 requests/hour average
10 req/s = 36,000 requests/hour = 20x headroom
```

**Location**: `cdk/stock_tracker_stack.py` - API Gateway deploy_options

### 2. AWS WAF on CloudFront

**Rules Enabled:**

1. **Rate Limiting Rule**
   - 100 requests per 5 minutes per IP
   - Blocks excessive requests from single source
   - Prevents DDoS attacks

2. **AWS Managed Rules - Common Rule Set**
   - OWASP Top 10 protection
   - SQL injection, XSS, etc.
   - Auto-updated by AWS

3. **AWS Managed Rules - Known Bad Inputs**
   - Blocks malicious patterns
   - Invalid request formats
   - Reduces spam

**Cost Impact**: ~$5-10/month

**Location**: `cdk/stock_tracker_stack.py` - WAF WebACL section

### 3. CloudWatch Alarms

**Four Alarms Created:**

1. **API 4XX Errors Alarm**
   - Threshold: >50 errors in 10 minutes
   - Detects: Bad requests, throttling, client issues

2. **API Throttling Alarm**
   - Threshold: >10 throttle events in 5 minutes
   - Detects: Rate limits being hit frequently

3. **Lambda Errors Alarm**
   - Threshold: >5 errors in 5 minutes
   - Detects: External API failures, code bugs

4. **Lambda Duration Alarm**
   - Threshold: Average >25 seconds (timeout is 30s)
   - Detects: Performance issues, external API slowness

**Optional**: Email notifications via SNS (commented out by default)

**Location**: `cdk/stock_tracker_stack.py` - CloudWatch Alarms section

## 📊 Complete Protection Stack

```
User Request
    ↓
CloudFront + WAF
    ├─ Rate Limiting (100 req/5min per IP)
    ├─ Common Exploits (OWASP Top 10)
    └─ Known Bad Inputs (Malicious patterns)
    ↓
[If allowed by WAF]
    ↓
API Gateway
    ├─ Throttling (10 req/s, 50 burst)
    ├─ CloudWatch Metrics
    └─ Logging (INFO level)
    ↓
[If within rate limit]
    ↓
Lambda Function
    ├─ 30-second timeout
    ├─ Error monitoring
    └─ Duration tracking
    ↓
External APIs
```

## 💰 Cost Breakdown

### Monthly Costs (10-25 Users)

| Service | Cost | Notes |
|---------|------|-------|
| **S3** | ~$0.10 | Storage (<1GB) |
| **CloudFront** | ~$0.50 | Data transfer |
| **Lambda** | FREE | Within 1M free tier |
| **API Gateway** | FREE | Free tier (first 12 months) |
| **WAF** | ~$5-10 | Base + rules + requests |
| **CloudWatch Alarms** | FREE | 10 free alarms |
| **CloudWatch Logs** | ~$0.50 | Lambda logs |
| **TOTAL** | **$6-11/month** | |

### Without WAF:
**$1-3/month** (if you comment out WAF to minimize costs)

## 🚀 Deployment

### Deploy All Features:

```bash
cd cdk
cdk diff      # Preview changes
cdk deploy    # Deploy everything
```

### What Gets Deployed:
- ✅ API Gateway with 10 req/s throttling
- ✅ WAF with 3 protection rules
- ✅ 4 CloudWatch alarms
- ✅ CloudWatch metrics and logging
- ✅ All existing infrastructure (S3, CloudFront, Lambda)

### Deploy Time:
~5-10 minutes (WAF and CloudFront take longest)

## 📧 Enable Email Notifications (Optional)

To receive emails when alarms trigger:

1. **Edit** `cdk/stock_tracker_stack.py`
2. **Uncomment** the SNS topic section:
   ```python
   alarm_topic = sns.Topic(...)
   alarm_topic.add_subscription(
       endpoint="your-email@example.com",  # <-- Add your email
       protocol=sns.SubscriptionProtocol.EMAIL
   )
   ```
3. **Uncomment** alarm actions:
   ```python
   api_4xx_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))
   # ... repeat for all 4 alarms
   ```
4. **Redeploy**: `cdk deploy`
5. **Confirm** subscription email from AWS

## 🔍 Monitoring After Deployment

### View in AWS Console:

**CloudWatch Alarms:**
```
https://console.aws.amazon.com/cloudwatch/home#alarmsV2:
```

**WAF Dashboard:**
```
https://console.aws.amazon.com/wafv2/homev2/web-acls
```

**API Gateway Metrics:**
```
https://console.aws.amazon.com/apigateway/home#/apis
```

### CLI Commands:

```bash
# Check alarms
aws cloudwatch describe-alarms --alarm-name-prefix "StockTracker"

# View WAF blocked requests
aws wafv2 get-sampled-requests --web-acl-arn <arn> --scope CLOUDFRONT

# View API metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiName,Value="Stock Tracker CORS Proxy" \
  --start-time $(date -u -d '1 hour ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 300 \
  --statistics Sum
```

## ⚙️ Configuration Options

### Adjust Rate Limits:

**For More Users (50-100):**
```python
# In stock_tracker_stack.py
throttling_rate_limit=25,      # Increase from 10 to 25
throttling_burst_limit=100,    # Increase from 50 to 100
```

**WAF Rate Limit:**
```python
limit=200,  # Increase from 100 to 200 requests per 5 min
```

### Disable WAF (Save $5-10/month):

Comment out in `stock_tracker_stack.py`:
```python
# waf_web_acl = wafv2.CfnWebACL(...)  # Comment out entire WAF section

distribution = cloudfront.Distribution(
    # web_acl_id=waf_web_acl.attr_arn,  # Comment this line
)
```

### Adjust Alarm Thresholds:

```python
# More sensitive (alert sooner):
threshold=25,  # From 50

# Less sensitive (fewer alerts):
threshold=100,  # From 50
```

## 🎯 What This Protects Against

✅ **DDoS Attacks**: WAF rate limiting blocks excessive requests  
✅ **SQL Injection**: AWS Managed Rules detect and block  
✅ **XSS Attacks**: Common Rule Set protection  
✅ **API Abuse**: API Gateway throttling prevents spam  
✅ **Cost Overruns**: Rate limits prevent unexpected bills  
✅ **Performance Issues**: Alarms alert before outages  
✅ **External API Failures**: Lambda error monitoring  

## 📈 Scaling Path

| Users | API Rate | WAF Rate | Monthly Cost |
|-------|----------|----------|--------------|
| 10-25 | 10 req/s | 100/5min | $6-11 |
| 25-50 | 15 req/s | 150/5min | $8-15 |
| 50-100 | 25 req/s | 200/5min | $12-20 |
| 100+ | 50 req/s | 300/5min | $20-30 |

*Note: After year 1, add ~$3/month for API Gateway after free tier expires*

## 🆘 Troubleshooting

### Alarms Firing Frequently?

**API Throttling Alarm:**
- Increase `throttling_rate_limit` in CDK
- Check if legitimate traffic spike
- Review CloudWatch metrics to see patterns

**WAF Blocking Legitimate Users:**
- Check WAF sampled requests in console
- Adjust rate limit if needed
- Consider IP whitelisting for known good IPs

**Lambda Errors:**
- Check Lambda logs in CloudWatch
- External API (Yahoo Finance) may be down
- Verify proxy configuration

### No Alarms After Deployment?

Alarms only trigger when thresholds are exceeded. To test:
1. Make multiple rapid requests
2. Check "Insufficient Data" vs "OK" state
3. Wait 5-10 minutes for metrics to appear

## 📚 Further Reading

- [API Gateway Throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)
- [AWS WAF Rules](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html)
- [CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
- [AWS Free Tier](https://aws.amazon.com/free/)

---

**Ready to deploy?** Run `python deploy.py` from the project root! 🚀
