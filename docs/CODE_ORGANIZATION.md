# 📁 Code Organization Guide

## New Project Structure

The project has been reorganized for better navigation and maintainability:

```
epam-stock-tracker/
├── src/                          # Frontend Application
│   ├── index.html                # Main HTML page
│   ├── css/                      # Stylesheets
│   │   └── styles.css            # Main stylesheet
│   └── js/                       # JavaScript modules
│       ├── app.js                # Main application logic
│       ├── api.js                # API calls (stock prices, exchange rates)
│       ├── calculator.js         # Portfolio calculations
│       └── storage.js            # LocalStorage management
│
├── infrastructure/               # AWS Infrastructure (CDK)
│   ├── cdk/                      # CDK application
│   │   ├── app.py                # CDK app entry point
│   │   ├── cdk.json              # CDK configuration
│   │   ├── requirements.txt      # Python dependencies
│   │   ├── .gitignore            # CDK-specific ignores
│   │   └── stacks/               # CDK stack definitions
│   │       ├── __init__.py       # Python package init
│   │       └── stock_tracker_stack.py  # Main infrastructure stack
│   └── lambda/                   # Lambda functions
│       └── cors_proxy/           # CORS proxy Lambda
│           └── index.py          # Lambda handler
│
├── scripts/                      # Deployment & Utility Scripts
│   ├── deploy.py                 # Automated AWS deployment
│   ├── check_aws_setup.py        # Prerequisites checker
│   └── test_lambda.py            # Local Lambda testing
│
├── dev/                          # Local Development Tools
│   └── proxy_server.py           # Local CORS proxy for development
│
├── docs/                         # Documentation
│   ├── DEPLOYMENT.md             # AWS deployment guide
│   ├── SECURITY_MONITORING.md    # Security & monitoring details
│   ├── PROJECT_STRUCTURE.md      # This file
│   └── QUICK_REFERENCE.md        # Command cheat sheet
│
├── README.md                     # Main documentation
└── .gitignore                    # Git ignore patterns
```

## What Changed?

### Before (Flat Structure)
- All files in root directory
- Hard to find specific files
- Mixed concerns (frontend, infrastructure, docs)
- CDK stack in root of cdk/ folder

### After (Organized Structure)
- Clear separation of concerns
- Easy to navigate
- Professional folder hierarchy
- Better for team collaboration

## File Locations Quick Reference

| What You Need | Where To Find It |
|---------------|------------------|
| **Frontend HTML** | `src/index.html` |
| **JavaScript** | `src/js/*.js` |
| **Stylesheets** | `src/css/styles.css` |
| **CDK Stack** | `infrastructure/cdk/stacks/stock_tracker_stack.py` |
| **CDK App** | `infrastructure/cdk/app.py` |
| **Lambda Function** | `infrastructure/lambda/cors_proxy/index.py` |
| **Deployment Script** | `scripts/deploy.py` |
| **Local Proxy** | `dev/proxy_server.py` |
| **Documentation** | `docs/*.md` |

## Running The App

### Local Development

```bash
# Terminal 1: Start local proxy
python dev/proxy_server.py

# Terminal 2: Start web server  
python -m http.server 8000 --directory src

# Open browser
http://localhost:8000
```

### AWS Deployment

```bash
# From project root
python scripts/deploy.py
```

### Testing Lambda Locally

```bash
# From project root
python scripts/test_lambda.py
```

### Check AWS Prerequisites

```bash
# From project root
python scripts/check_aws_setup.py
```

## Path Updates Made

### CDK Stack (`infrastructure/cdk/stacks/stock_tracker_stack.py`)
- Lambda code path: `../../lambda/cors_proxy`
- S3 deployment source: `../../../src`

### CDK App (`infrastructure/cdk/app.py`)
- Import: `from stacks.stock_tracker_stack import StockTrackerStack`

### Deployment Script (`scripts/deploy.py`)
- CDK commands run from: `infrastructure/cdk`
- Updates: `src/js/api.js`

### Test Script (`scripts/test_lambda.py`)
- Lambda import from: `../infrastructure/lambda/cors_proxy`

### HTML (`src/index.html`)
- CSS: `css/styles.css`
- JavaScript: `js/app.js`, `js/api.js`, etc.

## Benefits of New Structure

✅ **Easier Navigation**: Find files by category  
✅ **Professional**: Industry-standard layout  
✅ **Scalable**: Easy to add new features  
✅ **Team-Ready**: Clear separation for collaboration  
✅ **Maintainable**: Related files grouped together  
✅ **Clean Root**: Only essential files at top level  

## Development Workflow

1. **Edit Frontend**: Work in `src/` folder
   - HTML changes: `src/index.html`
   - Styling: `src/css/styles.css`
   - Logic: `src/js/*.js`

2. **Edit Infrastructure**: Work in `infrastructure/` folder
   - CDK stack: `infrastructure/cdk/stacks/stock_tracker_stack.py`
   - Lambda: `infrastructure/lambda/cors_proxy/index.py`

3. **Run Scripts**: Use from project root
   - Deploy: `python scripts/deploy.py`
   - Test: `python scripts/test_lambda.py`

4. **Update Docs**: Edit in `docs/` folder

## Migration Notes

All file paths have been updated to work with the new structure. No manual path updates needed when running:
- `python scripts/deploy.py` - Automatically uses correct paths
- `python dev/proxy_server.py` - Works from dev folder
- Local server: `python -m http.server 8000 --directory src`

## For Contributors

When adding new files:
- **Frontend code**: Add to `src/js/` or `src/css/`
- **New Lambda**: Add to `infrastructure/lambda/`
- **New CDK stack**: Add to `infrastructure/cdk/stacks/`
- **Utility script**: Add to `scripts/`
- **Documentation**: Add to `docs/`

## Need Help?

- See [README.md](../README.md) for overview
- See [docs/DEPLOYMENT.md](DEPLOYMENT.md) for AWS deployment
- See [docs/QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commands
