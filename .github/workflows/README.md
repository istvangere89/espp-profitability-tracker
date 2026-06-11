# GitHub Actions Workflows

This directory contains automated CI/CD workflows for the EPAM Stock Tracker.

## Workflows

### 1. 🚀 Deploy to AWS (`deploy.yml`)

**Triggers:**
- Push to `main` branch
- Manual trigger via `workflow_dispatch`

**What it does:**
1. **Test** - Runs all tests and validates code syntax
2. **Deploy** - Deploys infrastructure to AWS using CDK
3. **Update** - Updates frontend with API Gateway URL
4. **Redeploy** - Pushes updated frontend to S3/CloudFront
5. **Notify** - Reports deployment status

**Required Secrets:**
- `AWS_GITHUB_ROLE_ARN` - ARN of the OIDC role for AWS authentication

**Environment:**
- Region: `eu-central-1`
- Python: `3.11`
- Node.js: `18`

**Outputs:**
- Deployment outputs saved as artifacts
- Website URL and API Gateway URL printed

### 2. 🧪 Pull Request Tests (`pr-tests.yml`)

**Triggers:**
- Pull requests to `main` branch
- Only when changes affect code or workflows

**What it does:**
1. **Validate** - Checks Python syntax
2. **Test** - Runs Lambda handler tests
3. **Synth** - Validates CDK stack can synthesize
4. **Check JS** - Validates JavaScript syntax
5. **Security** - Scans for exposed secrets

**No AWS deployment** - Safe to run on external PRs

## Setup Instructions

### 1. Create OIDC Role in AWS

```bash
# This creates a trust relationship between GitHub and AWS
aws iam create-role \
  --role-name GitHubActionsDeployRole \
  --assume-role-policy-document file://trust-policy.json
```

**trust-policy.json:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:istvangere89/espp-profitability-tracker:*"
        }
      }
    }
  ]
}
```

### 2. Attach Policies to Role

```bash
# AdministratorAccess (for full CDK deployment)
aws iam attach-role-policy \
  --role-name GitHubActionsDeployRole \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Or create a more restrictive custom policy
```

### 3. Add Secret to GitHub

1. Go to: https://github.com/istvangere89/espp-profitability-tracker/settings/secrets/actions
2. Click "New repository secret"
3. Name: `AWS_GITHUB_ROLE_ARN`
4. Value: `arn:aws:iam::<ACCOUNT_ID>:role/GitHubActionsDeployRole`
5. Click "Add secret"

### 4. Enable GitHub Actions

1. Go to: https://github.com/istvangere89/espp-profitability-tracker/actions
2. Click "I understand my workflows, go ahead and enable them"

## Manual Deployment Trigger

To manually trigger a deployment:

1. Go to: https://github.com/istvangere89/espp-profitability-tracker/actions
2. Click "Deploy to AWS" workflow
3. Click "Run workflow"
4. Select branch (usually `main`)
5. Click "Run workflow"

## Monitoring Deployments

### View Workflow Runs
- https://github.com/istvangere89/espp-profitability-tracker/actions

### Check Deployment Logs
1. Click on a workflow run
2. Expand the job (Test/Deploy/Notify)
3. View step-by-step logs

### Download Outputs
- Deployment outputs are saved as artifacts
- Available for 30 days after deployment
- Contains CDK outputs with URLs

## Environment Variables

The workflows use these environment variables:

| Variable | Value | Purpose |
|----------|-------|---------|
| `AWS_REGION` | `eu-central-1` | AWS region for deployment |
| `PYTHON_VERSION` | `3.11` | Python version for builds |
| `NODE_VERSION` | `18` | Node.js version for CDK |

## Security

### OIDC Authentication
- **No static credentials** - Uses OIDC tokens
- **Short-lived tokens** - Expire after job completes
- **Scoped permissions** - Role limited to this repository

### Secrets Management
- `AWS_GITHUB_ROLE_ARN` stored encrypted in GitHub
- Never logged or exposed in workflow runs
- Only accessible to workflows in this repository

### Branch Protection
Consider enabling:
- Require PR reviews before merging
- Require status checks (tests must pass)
- Restrict who can push to `main`

## Troubleshooting

### Deployment Fails with "AccessDenied"
- Check OIDC role ARN is correct
- Verify role has necessary permissions
- Ensure trust policy matches repository

### "Role not found"
- Confirm secret `AWS_GITHUB_ROLE_ARN` is set
- Verify OIDC provider exists in AWS account
- Check role exists in correct AWS account

### CDK Bootstrap Error
- First deployment may need manual bootstrap:
  ```bash
  cdk bootstrap aws://<ACCOUNT_ID>/eu-central-1
  ```

### Tests Fail on PR
- Run tests locally first: `python scripts/test_lambda.py`
- Check for syntax errors: `python -m py_compile <file>`
- Ensure all dependencies are in `requirements.txt`

## Cost Considerations

GitHub Actions minutes:
- **Free tier**: 2,000 minutes/month for private repos
- **Public repos**: Unlimited free minutes
- Typical deployment: ~5-10 minutes

AWS costs remain the same (~$6-11/month as documented in [DEPLOYMENT.md](../../docs/DEPLOYMENT.md))

## Workflow Files

```
.github/
└── workflows/
    ├── deploy.yml       # Main deployment workflow
    └── pr-tests.yml     # Pull request testing workflow
```

## Next Steps

1. ✅ Set up OIDC role in AWS
2. ✅ Add `AWS_GITHUB_ROLE_ARN` secret
3. ✅ Push to `main` to trigger first deployment
4. ✅ Monitor workflow execution
5. ✅ Verify deployment in AWS Console

## Learn More

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OIDC with AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/latest/guide/home.html)
