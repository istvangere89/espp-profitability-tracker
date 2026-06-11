# 📁 Project Structure

```
epam-stock-tracker/
│
├── 🌐 Frontend (Static Website)
│   ├── index.html              # Main HTML page
│   ├── styles.css              # Styling and responsive design
│   ├── app.js                  # Main application logic
│   ├── api.js                  # API calls (stock prices, exchange rates)
│   ├── calculator.js           # Portfolio calculations and formatting
│   └── storage.js              # LocalStorage management (data persistence)
│
├── 🐍 Local Development
│   ├── proxy_server.py         # Local CORS proxy for development
│   └── test_lambda.py          # Test Lambda function locally
│
├── ☁️ AWS Infrastructure (CDK)
│   ├── cdk/
│   │   ├── app.py              # CDK app entry point
│   │   ├── stock_tracker_stack.py  # Infrastructure definition
│   │   ├── cdk.json            # CDK configuration
│   │   ├── requirements.txt    # CDK Python dependencies
│   │   └── .gitignore          # CDK-specific ignores
│   │
│   └── lambda/
│       └── index.py            # Lambda CORS proxy handler
│
├── 📄 Documentation
│   ├── README.md               # Main documentation
│   ├── DEPLOYMENT.md           # AWS deployment guide
│   ├── SECURITY_MONITORING.md  # Security & monitoring details
│   ├── PROJECT_STRUCTURE.md    # This file
│   └── QUICK_REFERENCE.md      # Command cheat sheet
│
├── 🚀 Deployment
│   └── deploy.py               # Automated deployment script
│
└── ⚙️ Configuration
    └── .gitignore              # Git ignore patterns
```

## 🔍 File Descriptions

### Frontend Files

- **index.html**: Main page with dashboard, form, and purchase history table
- **styles.css**: Modern, responsive CSS with dark mode support for profit/loss
- **app.js**: Handles UI interactions, form submission, and data rendering
- **api.js**: Fetches stock prices and exchange rates from external APIs
- **calculator.js**: Calculates portfolio metrics, profit/loss, and formatting
- **storage.js**: Manages localStorage for data persistence and CSV import/export

### Backend/Proxy

- **proxy_server.py**: Simple HTTP server for local development (port 8080)
  - Adds CORS headers to API responses
  - Allows testing without deploying to AWS
  
- **lambda/index.py**: AWS Lambda function (serverless replacement for proxy_server.py)
  - Same functionality as local proxy
  - Runs on AWS Lambda (pay-per-request)
  - Invoked via API Gateway

### Infrastructure (CDK)

- **cdk/app.py**: Defines the CDK application and stack
- **cdk/stock_tracker_stack.py**: Infrastructure as Code
  - S3 bucket for static hosting
  - CloudFront for global CDN
  - Lambda function for CORS proxy
  - API Gateway for Lambda endpoint
  - Automated deployment configuration

### Scripts

- **deploy.py**: Automated deployment workflow
  1. Installs dependencies
  2. Deploys CDK stack
  3. Updates api.js with API Gateway URL
  4. Redeploys with updated config
  
- **test_lambda.py**: Local testing for Lambda function
  - Tests valid requests
  - Tests error handling
  - Validates CORS headers

## 🔄 Data Flow

### Local Development:
```
Browser (localhost:8000)
    ↓
JavaScript (api.js)
    ↓ [5-min in-memory cache]
    ↓
Local Proxy (localhost:8080)
    ↓ [1-hour browser cache via Cache-Control header]
    ↓
External APIs (Yahoo Finance, Exchange Rate)
```

### AWS Production:
```
Browser (CloudFront URL)
    ↓
CloudFront CDN [Static files cached 24h]
    ↓
S3 Bucket (Static Files)
    ↓
JavaScript (api.js)
    ↓ [5-min in-memory cache]
    ↓
API Gateway
    ↓ [Optional: Server-side cache 1h - costs extra]
    ↓
Lambda Function
    ↓ [1-hour browser cache via Cache-Control header]
    ↓
External APIs (Yahoo Finance, Exchange Rate)
```

### Caching Layers:

1. **JavaScript In-Memory Cache (5 minutes)**
   - Defined in api.js
   - Prevents duplicate calls within same page session
   - Cleared on page refresh

2. **Browser HTTP Cache (1 hour)**
   - Cache-Control: public, max-age=3600
   - Set by proxy server / Lambda function
   - Reduces server load and API calls
   - Clear with hard refresh (Ctrl+Shift+R)

3. **API Gateway Cache (Optional, disabled by default)**
   - Server-side caching at AWS level
   - Costs ~$15/month for 0.5GB cache
   - Only needed for high-traffic scenarios

4. **CloudFront Edge Cache (Static files only)**
   - Caches HTML/CSS/JS files
   - Does not cache API proxy responses
   - 24-hour default TTL

## 💾 Data Storage

- **Browser LocalStorage**: All user data (purchases, settings)
- **AWS**: No user data stored (stateless serverless architecture)
- **Export**: CSV files for backup/portability

## 🛠️ Development Workflow

1. **Local Testing**:
   ```bash
   python proxy_server.py    # Terminal 1
   python -m http.server 8000  # Terminal 2
   ```

2. **Lambda Testing**:
   ```bash
   python test_lambda.py
   ```

3. **Deploy to AWS**:
   ```bash
   python deploy.py
   ```

4. **Update & Redeploy**:
   - Make changes to files
   - Run `python deploy.py` again
   - CloudFront cache invalidates automatically

## 📦 Dependencies

### Frontend (No npm packages - Pure vanilla JS!)
- No dependencies
- Works in any modern browser

### Backend
- **Local**: Python 3.x (standard library only)
- **AWS**: Python 3.11 runtime (Lambda)

### Infrastructure
- **CDK**: aws-cdk-lib, constructs
- **AWS CLI**: For credentials and deployment
- **Node.js**: For CDK CLI

## 🔐 Security

- **No API Keys**: No authentication needed (free public APIs)
- **No Backend Database**: All data in browser localStorage
- **HTTPS**: Enforced by CloudFront
- **Private S3**: Bucket not publicly accessible
- **CORS**: Properly configured for browser security

## 💰 Cost Structure

### Local Development: **FREE**
- Uses your computer
- No cloud costs

### AWS Deployment: **~$0-1/month**
- CloudFront: Free tier 1TB data, 10M requests/month
- Lambda: Free tier 1M requests/month
- API Gateway: Free tier 1M requests/12 months
- S3: ~$0.023/GB (website is <1MB)

Personal use typically stays in free tier!

## 🎯 Key Features by File

| Feature | Primary File | Supporting Files |
|---------|-------------|------------------|
| Real-time Prices | api.js | proxy_server.py / lambda/index.py |
| Historical Data | api.js | - |
| Auto-calculation | app.js | api.js, calculator.js |
| Portfolio Tracking | calculator.js | storage.js |
| Data Persistence | storage.js | - |
| CSV Import/Export | storage.js | app.js |
| Responsive UI | styles.css | index.html |
| AWS Deployment | cdk/stock_tracker_stack.py | deploy.py |
| API Caching (1h) | lambda/index.py | proxy_server.py |
| In-Memory Cache (5m) | api.js | - |
