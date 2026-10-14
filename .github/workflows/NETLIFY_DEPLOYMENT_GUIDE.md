# GitHub Actions Workflow Setup for Netlify Deployment

This guide explains how to set up the GitHub Actions workflow to automatically deploy to Netlify.

## 📋 Prerequisites

You need to have:
1. ✅ GitHub account (you have this)
2. ✅ Netlify account (create at https://app.netlify.com if you don't have one)
3. ✅ Repository connected to GitHub (istvangere89/espp-profitability-tracker)

## 🔑 Required Secrets

The `deploy-netlify.yml` workflow needs two secrets:

### 1. NETLIFY_AUTH_TOKEN
**What it is:** Personal access token from Netlify for authentication

**How to get it:**
1. Go to https://app.netlify.com/user/applications/personal
2. Click "New access token"
3. Name it: "GitHub Actions Deploy"
4. Copy the generated token

**How to add to GitHub:**
1. Go to: https://github.com/istvangere89/espp-profitability-tracker/settings/secrets/actions
2. Click "New repository secret"
3. Name: `NETLIFY_AUTH_TOKEN`
4. Value: Paste the token from above
5. Click "Add secret"

### 2. NETLIFY_SITE_ID
**What it is:** Unique ID for your Netlify site

**How to get it:**
1. Go to https://app.netlify.com
2. Click on your site
3. Go to "Site settings" → "General"
4. Find "Site details" section
5. Copy the "API ID" field

**How to add to GitHub:**
1. Go to: https://github.com/istvangere89/espp-profitability-tracker/settings/secrets/actions
2. Click "New repository secret"
3. Name: `NETLIFY_SITE_ID`
4. Value: Paste the API ID from above
5. Click "Add secret"

## ⚙️ Workflow Configuration

### File Location
- `.github/workflows/deploy-netlify.yml`

### What It Does

**On every push to `netlify-migration` branch:**
1. ✅ Runs tests (JavaScript syntax, function validation)
2. ✅ Deploys to Netlify
3. ✅ Tests the deployment

**On pull requests:**
1. ✅ Runs tests
2. ✅ Comments with setup instructions

**Manual trigger:**
1. You can manually run from GitHub Actions tab

### Workflow Stages

#### 1. Test Stage
```yaml
- Checks netlify.toml exists
- Validates JavaScript syntax
- Validates Netlify function syntax
- Checks no AWS references remain
```

#### 2. Deploy Stage (automatic on push)
```yaml
- Builds and deploys to Netlify
- Uses NETLIFY_AUTH_TOKEN and NETLIFY_SITE_ID
- Creates deployment preview
```

#### 3. Test Deployment Stage
```yaml
- Waits for deployment to complete
- Verifies function endpoint is accessible
```

## 🚀 Using the Workflow

### Automatic Deployment
Push to `netlify-migration` branch:
```bash
git push origin netlify-migration
```

Workflow automatically:
1. Runs tests
2. Deploys to Netlify
3. Reports status

### Manual Deployment
1. Go to: https://github.com/istvangere89/espp-profitability-tracker/actions
2. Click "Deploy to Netlify" workflow
3. Click "Run workflow"
4. Select branch: `netlify-migration`
5. Click "Run workflow"

### View Deployment Status
1. Go to: https://github.com/istvangere89/espp-profitability-tracker/actions
2. Click "Deploy to Netlify" workflow
3. Click the latest run
4. Expand each step to see details

## ✅ Verification Steps

After workflow completes:

### 1. Check GitHub Actions
```
✅ All steps should show green checkmarks
✅ Deployment stage should show "success"
```

### 2. Check Netlify
```
1. Go to https://app.netlify.com
2. Click on your site
3. Should show "Published" status
4. Deployment time should show recent timestamp
```

### 3. Test Your Site
```
1. Visit your Netlify URL (shown in Netlify dashboard)
2. App should load and work correctly
3. Stock prices should fetch
4. No console errors
```

## 🔄 Future Deployments

Once workflow is set up:

**To deploy new changes:**
```bash
# Make your changes
git add .
git commit -m "feat: description"

# Push to netlify-migration (or main if you merge the PR)
git push origin netlify-migration
```

Workflow runs automatically! ✨

**To merge to production:**
```bash
# Create PR on GitHub
# Review changes
# Merge to main
# Workflow runs on main branch too!
```

## 🆘 Troubleshooting

### "Deployment failed - secrets not found"
**Fix:** Check you added both secrets to GitHub
1. Go to Settings → Secrets
2. Verify both NETLIFY_AUTH_TOKEN and NETLIFY_SITE_ID exist
3. Re-run workflow after adding

### "Build failed - netlify.toml not found"
**Fix:** Ensure netlify.toml exists in repo root
```bash
ls -la netlify.toml
```

### "Tests failed - AWS references found"
**Fix:** All AWS API endpoint references must be updated
```bash
grep -r "execute-api" src/
# Should return nothing - if it does, update those files
```

### "Deployment succeeded but site shows errors"
**Fix:** Check Netlify function logs
1. Go to Netlify dashboard
2. Click site
3. Go to "Logs" → "Functions"
4. Check for error messages

### "Workflow doesn't run on push"
**Fix:** Check you pushed to correct branch
```bash
git push origin netlify-migration
# Not "origin main" until you merge PR
```

## 📊 Workflow File Details

### When It Runs
```yaml
on:
  push:
    branches: [netlify-migration]     # Push to this branch
  pull_request:
    branches: [main, netlify-migration]  # PR against these branches
  workflow_dispatch:                   # Manual trigger
```

### Environment
```yaml
- Node.js 24
- Runs on ubuntu-latest
- No Python needed (different from AWS deployment)
```

### Key Differences from AWS Workflow
```
AWS Workflow (deploy.yml):
- Uses Python CDK
- Deploys to AWS via OIDC role
- Creates CloudFront, Lambda, API Gateway
- Takes ~5-10 minutes

Netlify Workflow (deploy-netlify.yml):
- Uses Netlify CLI
- Deploys to Netlify via auth token
- Deploys static site + functions
- Takes ~2-3 minutes ⚡
```

## 🎯 Next Steps

1. ✅ Create Netlify account and site
2. ✅ Get NETLIFY_AUTH_TOKEN
3. ✅ Get NETLIFY_SITE_ID
4. ✅ Add both secrets to GitHub
5. ✅ Push to `netlify-migration` branch
6. ✅ Workflow runs and deploys!

## 📞 Need Help?

- **Workflow not running?** Check you're pushing to `netlify-migration` branch
- **Deployment failing?** Check secrets are added correctly
- **Site not working?** Check browser console for errors, check Netlify logs
- **Need AWS cleaned up?** See docs/NETLIFY_MIGRATION.md for cleanup steps

---

## 💡 Pro Tips

### Tip 1: Speed Up Testing
Comment out unused checks in workflow if they slow it down

### Tip 2: Monitor Deployments
Watch Netlify dashboard and GitHub Actions tab during first few deployments

### Tip 3: Keep Branches Clean
Once merged to main:
- Delete `netlify-migration` branch locally and remotely
- All future merges to main automatically deploy

### Tip 4: Rollback if Needed
```bash
# If deployment has issues, simply revert the merge
git revert <commit-hash>
git push origin main
# Workflow automatically deploys the reverted version
```

---

Happy deploying! 🚀
