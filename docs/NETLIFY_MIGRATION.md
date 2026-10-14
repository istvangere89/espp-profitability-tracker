# Netlify Migration Guide

This guide walks you through deploying the ESPP Profitability Tracker to Netlify, which will reduce your costs from **$11.50/month to $0/month**.

## 🎯 What's Changed

### Summary of Changes
- ✅ Removed dependency on AWS (no more CloudFront, API Gateway, Lambda)
- ✅ Migrated to Netlify for hosting and serverless functions
- ✅ Updated API endpoint from AWS Lambda to Netlify Function
- ✅ Created GitHub Actions workflow for automatic deployment
- ✅ Added security headers and caching policies

### Files Modified
- `src/js/api.js` - Updated all API endpoints to use `/.netlify/functions/cors-proxy`
- `.github/workflows/deploy-netlify.yml` - New GitHub Actions workflow
- `netlify.toml` - Netlify configuration
- `netlify/functions/cors-proxy.js` - CORS proxy replacement function

### Removed AWS Components
Once deployed to Netlify, you can delete:
- AWS CloudFront distribution
- AWS S3 bucket
- AWS Lambda function
- AWS API Gateway
- All AWS infrastructure code (infrastructure/ directory)

**Cost Savings: $11.50/month → $0/month** 🎉

---

## 📋 Prerequisites

1. **GitHub Account** - Already have this ✓
2. **Netlify Account** - Sign up at https://app.netlify.com (free)
3. **Node.js** (optional, for local testing)

---

## 🚀 Deployment Steps

### Step 1: Create Netlify Account (if you don't have one)

```
1. Go to https://app.netlify.com
2. Click "Sign up"
3. Choose "GitHub" as signup method (easiest)
4. Authorize GitHub access
```

### Step 2: Generate Netlify Personal Access Token

```
1. Go to https://app.netlify.com/user/applications/personal
2. Click "New access token"
3. Name it: "GitHub Actions Deploy"
4. Copy the token (you'll need this in Step 3)
```

### Step 3: Add GitHub Secrets

Add two secrets to your GitHub repository:

**For GitHub secrets setup:**
1. Go to: https://github.com/istvangere89/espp-profitability-tracker/settings/secrets/actions
2. Click "New repository secret"

**Secret 1: NETLIFY_AUTH_TOKEN**
- Name: `NETLIFY_AUTH_TOKEN`
- Value: Paste your token from Step 2

**Secret 2: NETLIFY_SITE_ID** (we'll get this after creating the site)
- Name: `NETLIFY_SITE_ID`
- Value: (leave blank for now, update after Step 4)

### Step 4: Link Repository to Netlify

**Option A: Via Netlify UI (Recommended)**
```
1. Go to https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Choose "GitHub"
4. Select "istvangere89/espp-profitability-tracker"
5. Choose branch: netlify-migration
6. Build settings:
   - Build command: (leave empty - static site)
   - Publish directory: src
   - Functions directory: netlify/functions
7. Click "Deploy site"
```

**Get your Site ID:**
1. After deployment, go to Site settings
2. Go to "Site details" or "General"
3. Copy "API ID" (this is your NETLIFY_SITE_ID)
4. Add it to GitHub secrets (Step 3, Secret 2)

**Option B: Via Netlify CLI**
```bash
npm install -g netlify-cli
cd /path/to/espp-profitability-tracker
netlify login
netlify init --git
```

### Step 5: Update GitHub Secrets

After getting your NETLIFY_SITE_ID from Step 4:
1. Go back to: https://github.com/istvangere89/espp-profitability-tracker/settings/secrets/actions
2. Edit `NETLIFY_SITE_ID` secret
3. Paste your site ID
4. Save

### Step 6: Trigger Deployment

**Option A: Push to netlify-migration branch**
```bash
cd /path/to/espp-profitability-tracker
git checkout netlify-migration
git push origin netlify-migration
```

GitHub Actions will automatically:
1. Run tests
2. Deploy to Netlify
3. Show deployment status

**Option B: Manual workflow trigger**
1. Go to: https://github.com/istvangere89/espp-profitability-tracker/actions
2. Select "Deploy to Netlify" workflow
3. Click "Run workflow"
4. Select branch: `netlify-migration`
5. Click "Run workflow"

### Step 7: Verify Deployment

After deployment completes:

1. **Check deployment status:**
   - Go to: https://app.netlify.com
   - Your site should show a "Published" badge
   - Your Netlify URL will be something like: `https://random-name-12345.netlify.app`

2. **Test the app:**
   - Visit your Netlify URL
   - Try fetching a stock price (should work)
   - Check browser console for any errors

3. **Check GitHub Actions:**
   - Go to: https://github.com/istvangere89/espp-profitability-tracker/actions
   - Select "Deploy to Netlify" workflow
   - View the latest run for deployment details

---

## 🔧 Configuration Details

### netlify.toml
- Build command: None (static site)
- Publish directory: `src/`
- Functions directory: `netlify/functions/`
- Caching: 1 year for CSS/JS, no-cache for HTML
- Security headers: Enabled
- Redirects: All routes → index.html for SPA routing

### CORS Proxy Function (netlify/functions/cors-proxy.js)
- **Purpose:** Replaces AWS Lambda CORS proxy
- **Endpoint:** `/.netlify/functions/cors-proxy`
- **Features:**
  - Handles Yahoo Finance API requests
  - Handles currency exchange API requests
  - 5-minute response caching
  - Domain whitelist (security)
  - Error handling

---

## ✅ Testing After Deployment

### Test 1: App Loads
```
1. Visit your Netlify URL
2. Page should load without errors
3. Should see the stock tracker interface
```

### Test 2: Fetch Stock Price
```
1. Open browser DevTools (F12)
2. Go to Console tab
3. The app should automatically fetch EPAM stock price
4. Should see price displayed
5. No CORS errors should appear
```

### Test 3: Currency Conversion
```
1. Enter a purchase amount in USD
2. Should see HUF conversion
3. Exchange rate should be fetched and displayed
4. No API errors in console
```

### Test 4: Full Workflow
```
1. Add a test purchase
2. Enter shares and amount
3. Auto-calculation should work
4. Profit/loss should calculate correctly
```

---

## 🎯 Next Steps After Successful Netlify Deployment

### 1. Test Thoroughly
- Test all features on Netlify deployment
- Verify stock prices update correctly
- Verify currency conversion works
- Test on mobile devices

### 2. Create Pull Request
```bash
# After testing:
git add .
git commit -m "feat: migrate to Netlify"
git push origin netlify-migration
```
Then create a PR on GitHub to merge into `main`

### 3. Review & Merge
1. Go to GitHub
2. Create Pull Request: `netlify-migration` → `main`
3. Review changes
4. Merge to main

### 4. Destroy AWS Resources
Once you're confident Netlify deployment is stable:

```bash
# Backup AWS config first
cd infrastructure/cdk
cdk destroy EpamStockTrackerStack

# Confirm destruction
```

This removes all AWS costs.

### 5. Clean Up AWS Account
```bash
# Optional: Remove deployment role if created for GitHub Actions
aws iam delete-role --role-name GitHubActionsDeployRole

# Remove old outputs file if exists
rm outputs.json
```

### 6. Update Main Workflow
After confirming Netlify is stable:
1. You can optionally remove `deploy.yml` (AWS workflow)
2. Keep `pr-tests.yml` if you want to run tests on PRs
3. Update main README.md to reference Netlify deployment

---

## 🆘 Troubleshooting

### Issue: "NETLIFY_AUTH_TOKEN not found"
**Solution:** Add the secret to GitHub
1. Go to Settings → Secrets
2. Add `NETLIFY_AUTH_TOKEN` secret

### Issue: "Function returns 500 error"
**Solution:** Check function logs
1. Go to Netlify site settings
2. Go to "Logs" → "Functions"
3. Check what error is shown

### Issue: "Stock prices not loading"
**Solution:** Check API endpoints
1. Open browser DevTools (F12)
2. Go to Network tab
3. Look for `cors-proxy` request
4. Check response status and body

### Issue: "Deployment fails in GitHub Actions"
**Solution:** Check workflow logs
1. Go to Actions tab
2. Click "Deploy to Netlify" workflow
3. Click the failed run
4. Expand "Deploy to Netlify" step
5. Check error message

### Issue: "Static files not loading (404 errors)"
**Solution:** Check netlify.toml
1. Verify `publish = "src"` is correct
2. Verify `src/index.html` exists
3. Check file permissions

---

## 💰 Cost Comparison

### Before (AWS)
```
CloudFront:        $8-10/month
API Gateway:       $1-2/month
Lambda:            $0-0.50/month
CloudWatch Logs:   $1-2/month
S3:                $0.05/month
─────────────────────────────
Total:             $11.50/month ❌
```

### After (Netlify)
```
Static hosting:    $0/month
Functions:         $0/month (free tier)
Bandwidth:         $0/month (unlimited)
CI/CD:             $0/month (free)
─────────────────────────────
Total:             $0/month ✅
```

**Monthly savings: $11.50** 🎉

---

## 📚 Additional Resources

- [Netlify Documentation](https://docs.netlify.com)
- [Netlify Functions Guide](https://docs.netlify.com/functions/overview/)
- [Netlify CLI Reference](https://cli.netlify.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## ✨ Summary

You've successfully migrated your ESPP Profitability Tracker to Netlify! 

**Key Benefits:**
- ✅ $0/month cost (down from $11.50/month)
- ✅ Simpler infrastructure (no AWS account needed)
- ✅ Automatic deployments via GitHub Actions
- ✅ Better performance with global CDN
- ✅ Built-in security and monitoring

**Next time you update the app:**
1. Edit code on any branch
2. Create PR to `main`
3. Merge to `main`
4. GitHub Actions automatically deploys to Netlify
5. App is live! 🚀

---

## 🤝 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Check Netlify deployment logs: https://app.netlify.com
3. Check GitHub Actions logs: https://github.com/istvangere89/espp-profitability-tracker/actions
4. Review error messages carefully (often indicate the solution)
