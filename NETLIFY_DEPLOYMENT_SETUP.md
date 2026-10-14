# 🚀 Netlify Deployment Setup - espp-profitability-tracker.netlify.app

**Your code is now on main and ready to deploy to Netlify with automatic builds & deploys!**

---

## ✅ Current Status

- ✅ `netlify-migration` merged into `main`
- ✅ All code on main branch ready for Netlify
- ✅ Site name: `espp-profitability-tracker.netlify.app`
- ⏳ Waiting for Netlify connection

---

## 🎯 Step-by-Step Netlify Setup

### Step 1: Create/Login to Netlify Account (5 min)

**If you don't have a Netlify account:**
```
1. Go to https://app.netlify.com
2. Click "Sign up"
3. Choose "GitHub"
4. Authorize GitHub access
5. Done!
```

**If you already have an account:**
```
1. Go to https://app.netlify.com
2. Log in with GitHub
3. Continue to Step 2
```

### Step 2: Create New Site & Connect Repository (5 min)

**In Netlify Dashboard:**
```
1. Click "Add new site" button (top left)
2. Choose "Import an existing project"
3. Select "GitHub"
4. Search for: istvangere89/espp-profitability-tracker
5. Click to select it
```

### Step 3: Configure Build Settings (5 min)

**Configure deployment:**
```
Branch to deploy:    main
Build command:       (leave empty)
Publish directory:   src
Functions directory: netlify/functions
```

**Click "Deploy site"**

Netlify will now:
- ✅ Clone your repository
- ✅ Copy static files from `src/`
- ✅ Deploy functions from `netlify/functions/`
- ✅ Apply configuration from `netlify.toml`
- ✅ Provide your site URL

### Step 4: Set Custom Site Name (2 min)

**After initial deployment:**
```
1. Go to Netlify dashboard
2. Click your site
3. Go to "Site settings" → "General"
4. Find "Site details" section
5. Click "Change site name"
6. Enter: espp-profitability-tracker
7. Click "Save"
```

**Your site will be available at:**
```
https://espp-profitability-tracker.netlify.app
```

---

## 🔄 How Automatic Deployment Works

Once connected:

```
You commit & push to main
        ↓
GitHub notifies Netlify
        ↓
Netlify automatically:
  1. Clones your repo
  2. Deploys src/ → website files
  3. Deploys netlify/functions/ → serverless functions
  4. Applies netlify.toml config
        ↓
App is live at espp-profitability-tracker.netlify.app ✅
```

**Every push to main = automatic deploy!**

---

## 📊 What Happens After Setup

### First Deployment
- Initial build takes ~1-2 minutes
- Netlify builds and deploys everything
- Site goes live automatically

### Future Deployments
- Every time you push to `main`
- Automatic build and deploy
- Usually done in ~1-2 minutes
- You can track in Netlify dashboard

### Monitoring Deployments
```
1. Go to app.netlify.com
2. Click your site
3. Click "Deploys" tab
4. See all deployments with:
   - Status (Published/Building/Failed)
   - Time
   - Git commit message
   - Deployment log link
```

---

## ✅ First Deployment Verification

After Netlify deploys:

- [ ] Go to https://espp-profitability-tracker.netlify.app
- [ ] Page loads without errors
- [ ] Open DevTools (F12)
- [ ] Go to Console tab
- [ ] No red error messages
- [ ] Try fetching stock price (should appear)
- [ ] Try currency conversion (should show HUF)
- [ ] Add a test purchase
- [ ] Verify calculations work
- [ ] Check no CORS errors

---

## 🛠️ Common Tasks

### View Deployment Logs
```
1. Go to app.netlify.com
2. Click your site
3. Click "Deploys" tab
4. Click on any deployment
5. Click "Deployment log"
6. See exactly what happened
```

### View Function Logs
```
1. Go to app.netlify.com
2. Click your site
3. Go to "Functions" tab
4. Click "cors-proxy"
5. See function execution logs
6. Check for errors
```

### Rollback to Previous Version
```
1. Go to "Deploys" tab
2. Find the working deployment
3. Click "..." menu
4. Click "Publish deploy"
5. Site instantly reverts!
```

### Check Build Settings
```
1. Click "Site settings" → "Build & deploy"
2. Verify:
   - Branch: main
   - Build command: (empty)
   - Publish directory: src
   - Functions: netlify/functions
3. Edit if needed and save
```

---

## 🚨 Troubleshooting

### Issue: Deployment Shows "Failed"
**Solution:**
1. Click the failed deployment
2. Click "Deployment log"
3. Look for red error messages
4. Fix the issue and push again
5. Netlify auto-redeploys

### Issue: Static Files Show 404
**Solution:**
1. Check netlify.toml
2. Verify `publish = "src"` is correct
3. Verify files exist in `src/`
4. Re-push to trigger build

### Issue: CORS Proxy Not Working
**Solution:**
1. Go to Functions tab
2. Click cors-proxy
3. Check logs for errors
4. Also check browser console (F12)

### Issue: Site Not Updating After Push
**Solution:**
1. Check Netlify "Deploys" tab
2. Is it still building?
3. Hard refresh browser (Ctrl+Shift+R)
4. Check build logs for errors

---

## 💡 Tips & Best Practices

### Tip 1: Deploy Previews
Netlify creates preview for every branch:
```
1. Create a new branch
2. Push changes
3. Netlify auto-creates preview URL
4. Test before merging
5. Merge when ready
```

### Tip 2: Environment Variables (If Needed Later)
```
1. Site settings → Build & deploy → Environment
2. Add environment variables
3. No secrets exposed
4. Available to functions
```

### Tip 3: Notifications
```
1. Site settings → Build & deploy → Deploy notifications
2. Get email when deploy completes
3. Get alerts on failures
```

### Tip 4: Custom Domain (Optional)
```
If you have your own domain:
1. Site settings → Domain management
2. Click "Add custom domain"
3. Follow DNS setup
4. Domain now points to Netlify
```

---

## 📈 Performance

Your app on Netlify:
- ✅ Global CDN distribution
- ✅ 30-100ms latency from EU
- ✅ Automatic caching
- ✅ Compression enabled
- ✅ Unlimited bandwidth
- ✅ No data transfer charges

---

## 🎯 Summary

**Setup Complete:**
- ✅ Code merged to main
- ✅ Ready for Netlify connection
- ✅ Documentation complete
- ✅ Automatic deployment configured

**Next Steps:**
1. Follow Steps 1-4 above in Netlify
2. Wait for first deployment
3. Test app at `espp-profitability-tracker.netlify.app`
4. Every push to main = automatic deploy!

**Cost Savings:**
- Before: $11.50/month (AWS)
- After: $0/month (Netlify)
- Savings: $138/year 🎉

---

## 🚀 You're Ready to Deploy!

**Everything is set up.** Just connect to Netlify following Steps 1-4 above, and your app will be live!

Questions? Check the documentation in the repo:
- `docs/NETLIFY_SIMPLE_DEPLOYMENT.md` - Detailed setup guide
- `docs/NETLIFY_MIGRATION.md` - Complete overview
- `NETLIFY_MIGRATION_BRANCH.md` - What changed

Good luck! 🎉
