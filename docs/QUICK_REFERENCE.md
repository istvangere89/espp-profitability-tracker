# 🎯 Quick Reference Card

## 🚀 Local Development

### Start Local Servers
```bash
# Terminal 1: Proxy server
python dev/proxy_server.py

# Terminal 2: Web server
python -m http.server 8000 --directory src
```

Then open: http://localhost:8000

### Stop Servers
Press `Ctrl+C` in each terminal

---

## ☁️ AWS Deployment

### Check Prerequisites
```bash
python scripts/check_aws_setup.py
```

### Test Lambda Locally
```bash
python scripts/test_lambda.py
```

### Deploy to AWS
```bash
python scripts/deploy.py
```

### View Stack Info
```bash
cd infrastructure/cdk
cdk diff     # Preview changes
cdk output   # Show outputs
```

### Destroy Stack
```bash
cd infrastructure/cdk
cdk destroy
```

---

## 📝 Project Commands

### File Structure
```bash
# View project structure
dir /b   # Windows
ls -la   # Mac/Linux
```

### Git Operations
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

---

## 🔍 Troubleshooting

### Local Development Issues

**Port already in use:**
```bash
# Windows - Find process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Mac/Linux - Find process
lsof -i :8000
kill -9 <process_id>
```

**CORS errors:**
- Make sure proxy_server.py is running on port 8080
- Check browser console for actual error
- Verify api.js uses http://localhost:8080

### AWS Deployment Issues

**CDK not found:**
```bash
npm install -g aws-cdk
```

**AWS credentials not configured:**
```bash
aws configure
# Enter: Access Key ID, Secret Access Key, Region
```

**Bootstrap required:**
```bash
cd cdk
cdk bootstrap
```

**Deployment failed:**
```bash
# Check CloudFormation console for details
# View logs:
aws cloudformation describe-stack-events --stack-name EpamStockTrackerStack
```

---

## 📊 Monitoring

### CloudWatch Alarms
```bash
# List all alarms
aws cloudwatch describe-alarms --alarm-name-prefix "StockTracker"

# Get alarm history
aws cloudwatch describe-alarm-history --alarm-name "StockTracker-API-Throttling"
```

### WAF Metrics
```bash
# View WAF blocked requests
aws wafv2 get-web-acl --scope CLOUDFRONT --id <web-acl-id> --name StockTrackerWebACL

# View WAF sampled requests (last 3 hours)
aws wafv2 get-sampled-requests \
  --web-acl-arn <arn-from-outputs> \
  --rule-metric-name RateLimitRule \
  --scope CLOUDFRONT \
  --time-window StartTime=$(date -u -d '3 hours ago' +%s),EndTime=$(date -u +%s) \
  --max-items 100
```

### API Gateway Metrics
```bash
# View API Gateway metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiName,Value="Stock Tracker CORS Proxy" \
  --start-time $(date -u -d '1 hour ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 300 \
  --statistics Sum

# Check throttling
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name 4XXError \
  --dimensions Name=ApiName,Value="Stock Tracker CORS Proxy" \
  --start-time $(date -u -d '1 hour ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 300 \
  --statistics Sum
```

### AWS CloudWatch Logs
```bash
# View Lambda logs
aws logs tail /aws/lambda/EpamStockTrackerStack-CorsProxyFunction --follow
```

### Check API Gateway
```bash
# Test endpoint directly
curl "https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/?url=https%3A%2F%2Fapi.exchangerate-api.com%2Fv4%2Flatest%2FUSD"
```

### CloudFront Cache
```bash
# Invalidate cache (forces refresh)
aws cloudfront create-invalidation --distribution-id <id> --paths "/*"
```

---

## 💾 Data Management

### Caching Behavior

**Browser Cache (Automatic)**:
- API responses cached for 1 hour
- Stock prices and exchange rates
- Reduces external API calls
- Clear cache: Hard refresh (`Ctrl+Shift+R` or `Cmd+Shift+R`)

**JavaScript Cache (api.js)**:
- Additional 5-minute in-memory cache
- For rapid successive calls
- Cleared on page refresh

**To Force Fresh Data**:
```javascript
// In browser console:
location.reload(true)  // Hard reload
// Or click the "🔄 Refresh Prices" button
```

### Export Data
Click "📥 Export CSV" button in the app

### Import Data
Click "📤 Import CSV" button and select your file

### Backup LocalStorage
```javascript
// In browser console:
JSON.stringify(localStorage)
```

### Clear All Data
```javascript
// In browser console (CAUTION: Deletes all data!)
localStorage.clear()
```

---

## 🔧 Configuration

### Update API Endpoint (api.js)
```javascript
// Change this line in api.js:
const proxyUrl = `http://localhost:8080?url=...`;

// To your AWS endpoint:
const proxyUrl = `https://xxx.execute-api.region.amazonaws.com/prod/?url=...`;
```

### Change AWS Region
```bash
# Edit cdk/app.py:
env=cdk.Environment(region="eu-central-1")  # Change region
```

### Change Stack Name
```bash
# Edit cdk/app.py:
StockTrackerStack(app, "MyCustomStackName", ...)
```

---

## 💰 Cost Monitoring

### View AWS Costs
```bash
# Open AWS Console → Billing → Cost Explorer
# Or use CLI:
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-01-31 --granularity MONTHLY --metrics BlendedCost
```

### Free Tier Dashboard
https://console.aws.amazon.com/billing/home#/freetier

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| **Local App** | http://localhost:8000 |
| **AWS Console** | https://console.aws.amazon.com |
| **CloudFormation** | https://console.aws.amazon.com/cloudformation |
| **Lambda Console** | https://console.aws.amazon.com/lambda |
| **CloudFront** | https://console.aws.amazon.com/cloudfront |
| **CloudWatch Logs** | https://console.aws.amazon.com/cloudwatch/home#logsV2:log-groups |
| **CDK Docs** | https://docs.aws.amazon.com/cdk/ |

---

## 📞 Support

- **CDK Issues**: https://github.com/aws/aws-cdk/issues
- **AWS Support**: https://console.aws.amazon.com/support
- **Python Help**: https://docs.python.org/3/

---

## 🎓 Learning Resources

- **AWS Free Tier**: https://aws.amazon.com/free/
- **CDK Workshop**: https://cdkworkshop.com/
- **Lambda Tutorial**: https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html
- **Python CDK**: https://docs.aws.amazon.com/cdk/api/v2/python/

---

*Keep this file bookmarked for quick reference!*
