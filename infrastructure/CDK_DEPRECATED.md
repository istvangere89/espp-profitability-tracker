# ⚠️ AWS CDK Infrastructure - DEPRECATED

**Status:** This AWS infrastructure is no longer in use. The application has been migrated to Netlify.

## Historical Reference

This folder contains the AWS CDK infrastructure code that was previously used to deploy the ESPP Profitability Tracker to AWS.

### Previous Architecture

The AWS deployment consisted of:
- **S3 Bucket**: Static website hosting
- **CloudFront Distribution**: Global CDN with geo-restriction (Hungary)
- **Lambda Function**: CORS proxy for external API requests
- **API Gateway**: REST API for Lambda integration
- **CloudWatch**: Monitoring and alarms

### Cost

The AWS infrastructure cost approximately **$11.50/month**:
- CloudFront data transfer: $8-10/month
- API Gateway: $1-2/month
- CloudWatch logs: $1-2/month
- Lambda: $0-0.50/month
- S3: $0.05/month

## Current Architecture

The application is now deployed on **Netlify** at zero cost:

✅ **Netlify Static Hosting** (Free)
- Global edge network CDN
- Unlimited bandwidth
- Automatic deploys on every push to main
- One-click rollback

✅ **Netlify Functions** (Free)
- CORS proxy function replaces AWS Lambda
- 125k invocations/month free tier
- Auto-scaling, no maintenance

**New Monthly Cost: $0** 🎉
**Annual Savings: $138**

## Why This Code is Kept

This CDK code is retained for:
1. **Historical reference** - Understanding the previous architecture
2. **Knowledge preservation** - Learning how AWS CDK works
3. **Future reference** - If AWS deployment is needed again
4. **Documentation** - Understanding AWS best practices that were applied

## If You Need AWS Deployment Again

To redeploy this infrastructure:

```bash
cd infrastructure/cdk

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

# Deploy the stack
cdk deploy
```

## Important Notes

- The AWS stack has been **deleted** (as of Oct 14, 2026)
- The S3 bucket, CloudFront distribution, Lambda function, and API Gateway have been removed
- No AWS billing is occurring for this infrastructure

## Migration Details

See [docs/NETLIFY_MIGRATION.md](../../docs/NETLIFY_MIGRATION.md) for full migration details:
- What changed in the codebase
- How Netlify deployment works
- Performance and cost comparisons
- Setup instructions for Netlify

## Files in This Directory

- `app.py` - CDK App entry point
- `cdk.json` - CDK configuration
- `requirements.txt` - Python dependencies
- `stacks/stock_tracker_stack.py` - Main stack definition with all AWS resources

---

**Last Updated:** October 14, 2026  
**Status:** Infrastructure destroyed, application running on Netlify
