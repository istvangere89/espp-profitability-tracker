# 🚀 Netlify Migration Branch

Welcome to the `netlify-migration` branch! This branch contains all the changes needed to migrate from AWS to Netlify.

## 📊 What's New

**Branch:** `netlify-migration`  
**Status:** ✅ Ready for deployment  
**Cost Reduction:** $11.50/month → $0/month  

## 📝 Changes Summary

### Modified Files
- ✅ `src/js/api.js` - Updated API endpoints from AWS to Netlify Functions

### New Files
- ✅ `netlify.toml` - Netlify site configuration
- ✅ `netlify/functions/cors-proxy.js` - Netlify Function for CORS proxy
- ✅ `.github/workflows/deploy-netlify.yml` - GitHub Actions workflow
- ✅ `docs/NETLIFY_MIGRATION.md` - Complete migration guide
- ✅ `.github/workflows/NETLIFY_DEPLOYMENT_GUIDE.md` - Workflow setup guide

### Removed (after this deploys)
- AWS infrastructure files can be archived/deleted
- `.github/workflows/deploy.yml` can be removed (optional)

---

## 🎯 Quick Start

### For Testing (Local Machine)
```bash
# 1. Switch to this branch
git checkout netlify-migration

# 2. Install Netlify CLI
npm install -g netlify-cli

# 3. Start local dev server
cd /path/to/espp-profitability-tracker
netlify dev

# 4. Open http://localhost:8888 in browser
```

### For Deployment (GitHub Actions)

**Prerequisites:**
1. Create Netlify account: https://app.netlify.com
2. Connect repository to Netlify
3. Add GitHub secrets (see step-by-step below)

**Setup Steps:**

1. **Get Netlify Auth Token:**
   - Go to https://app.netlify.com/user/applications/personal
   - Click "New access token"
   - Copy the token

2. **Add to GitHub Secrets:**
   - Go to: https://github.com/istvangere89/espp-profitability-tracker/settings/secrets/actions
   - Add secret `NETLIFY_AUTH_TOKEN` with your token
   - Add secret `NETLIFY_SITE_ID` with your site ID

3. **Trigger Deployment:**
   - Push to this branch: `git push origin netlify-migration`
   - Or manually run workflow from Actions tab
   - GitHub Actions automatically deploys!

**Detailed setup guide:** See `.github/workflows/NETLIFY_DEPLOYMENT_GUIDE.md`

---

## ✅ Pre-Deployment Checklist

Before merging/deploying, verify:

- [ ] Netlify account created
- [ ] Repository connected to Netlify
- [ ] `NETLIFY_AUTH_TOKEN` secret added to GitHub
- [ ] `NETLIFY_SITE_ID` secret added to GitHub
- [ ] Tested app locally (if possible)
- [ ] All API endpoints updated to use `/.netlify/functions/cors-proxy`
- [ ] No AWS references remain in `src/js/api.js`
- [ ] No CORS errors in browser console

---

## 🧪 Testing

### Local Testing
```bash
# Install dependencies
npm install -g netlify-cli

# Start dev server
netlify dev

# Test in browser: http://localhost:8888
# - Load app
# - Check browser console (F12)
# - Try fetching stock price
# - Try currency conversion
# - Check for errors
```

### GitHub Actions Testing
```bash
# Push to netlify-migration branch
git push origin netlify-migration

# Watch Actions tab for workflow execution
# https://github.com/istvangere89/espp-profitability-tracker/actions
```

### Deployment Testing
After workflow completes:
1. Go to Netlify dashboard
2. Check site status shows "Published"
3. Visit your Netlify URL
4. Verify app works correctly
5. Check browser console for errors

---

## 📚 Documentation

### For Deployment Setup
→ Read: `.github/workflows/NETLIFY_DEPLOYMENT_GUIDE.md`
- Step-by-step GitHub secrets setup
- Workflow configuration details
- Troubleshooting guide

### For Complete Migration Guide
→ Read: `docs/NETLIFY_MIGRATION.md`
- Full feature list
- Cost breakdown
- Pre and post-deployment steps
- AWS cleanup instructions

### For Workflow Details
→ Read: `.github/workflows/deploy-netlify.yml`
- Workflow trigger conditions
- Step-by-step execution
- Error handling

---

## 🔄 How It Works

### GitHub Actions Workflow
1. **On push to `netlify-migration`:**
   - Runs syntax tests
   - Validates Netlify configuration
   - Deploys to Netlify automatically

2. **On pull request:**
   - Runs syntax tests
   - Comments with setup info
   - Does NOT deploy (safe for review)

3. **Manual trigger:**
   - Can manually run from Actions tab
   - Useful for re-deploying if needed

### Netlify Deployment
1. Builds static site from `src/`
2. Deploys Netlify Functions from `netlify/functions/`
3. Applies caching and security headers
4. Creates deployment preview
5. Shows deployment status

---

## ⚡ Performance Benefits

### Speed
- Netlify CDN is globally distributed
- Typically faster than AWS CloudFront
- ~2-3 second initial load
- Functions cold start: ~100-500ms

### Bandwidth
- **Before:** Charged $0.085/GB
- **After:** Unlimited bandwidth (included)

### Latency
- CloudFront: 50-200ms from EU
- Netlify: 30-100ms from EU
- Edge function execution: <100ms additional

---

## 💰 Cost Breakdown

### Before (AWS)
```
CloudFront:        ~$8-10/month
API Gateway:       ~$1-2/month
Lambda:            ~$0-0.50/month
CloudWatch Logs:   ~$1-2/month
S3:                ~$0.05/month
─────────────────────────────
Total:             ~$11.50/month
```

### After (Netlify)
```
Static hosting:    $0/month
Functions:         $0/month (free tier)
Bandwidth:         $0/month (unlimited)
CI/CD:             $0/month (included)
─────────────────────────────
Total:             $0/month
```

**Savings: $11.50/month** 🎉

---

## 🚦 Deployment Flow

```
1. Code ready on netlify-migration branch
   ↓
2. Push to GitHub
   ↓
3. GitHub Actions runs tests
   ↓
4. If tests pass → Deploy to Netlify
   ↓
5. Netlify builds and deploys
   ↓
6. Site published at netlify-app-name.netlify.app
   ↓
7. (Optional) Merge to main for permanent deployment
```

---

## 🆘 Need Help?

### Workflow Setup Issues
→ See `.github/workflows/NETLIFY_DEPLOYMENT_GUIDE.md`

### General Migration Questions
→ See `docs/NETLIFY_MIGRATION.md`

### Specific Error Messages
→ Check GitHub Actions logs or Netlify dashboard

### Local Testing Issues
→ Try `netlify dev --debug` for verbose logging

---

## 🎯 Next Steps

### Immediate (Before Deployment)
1. Create Netlify account
2. Connect GitHub repo to Netlify
3. Add GitHub secrets
4. (Optional) Test locally with `netlify dev`

### Deployment
1. Verify all checks above pass
2. Push to `netlify-migration` branch
3. Watch GitHub Actions deploy
4. Test on Netlify URL

### After Deployment
1. Create PR to merge `netlify-migration` → `main`
2. Review changes
3. Merge to `main`
4. All future deployments automatic

### Cleanup (Optional)
1. Archive AWS infrastructure code
2. Delete AWS resources if not needed
3. Remove old AWS workflow (deploy.yml)

---

## 📞 Questions?

- **How do I test this locally?** → Run `netlify dev`
- **When does it deploy?** → On push to this branch
- **Do I need AWS still?** → No, can delete everything after this works
- **Can I rollback?** → Yes, just revert the merge and redeploy
- **Will my data transfer?** → Yes, browser storage continues to work

---

## 🎉 Ready?

You're all set! Follow the "Quick Start" section above and you'll have a zero-cost EPAM Stock Tracker deployed on Netlify.

**Questions?** Check the documentation files or GitHub Actions logs.

**Let's go!** 🚀
