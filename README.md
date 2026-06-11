# 📈 EPAM Stock Purchase Tracker

A web-based application to track EPAM stock purchases from your company's Employee Stock Purchase Program (ESPP), displaying real-time profit/loss calculations in Hungarian Forint (HUF).

## 🎯 Features

- **Real-time Stock Prices**: Fetches current EPAM stock prices from Yahoo Finance API
- **Historical Data**: Automatically fetches historical stock prices and exchange rates for past purchase dates
- **Auto-Calculation**: Smart form that auto-calculates shares and purchase price with 15% ESPP discount when left empty
- **Currency Conversion**: Automatically converts USD to HUF using live exchange rates
- **Profit/Loss Tracking**: Calculates profit/loss for each purchase and total portfolio
- **Purchase History**: View all your stock purchases with detailed metrics
- **Data Persistence**: All data stored locally in browser (no server required)
- **CSV Import/Export**: Backup and restore your purchase data
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Smart Caching**: 1-hour browser cache for API responses to reduce external API load

## 🚀 Getting Started

### Prerequisites

To use the auto-calculation feature and avoid CORS issues, you need to run two local servers:
1. A web server to serve the HTML/CSS/JS files (port 8000)
2. A proxy server to handle API requests (port 8080)

**Requirements:**
- Python 3.x (download from [python.org](https://python.org) if you don't have it)

### Setup Instructions

1. **Download/clone the project** to a folder on your computer

2. **Open two terminal/command prompt windows** in the project folder

3. **Start the proxy server** (in terminal 1):
   ```bash
   python dev/proxy_server.py
   ```
   You should see: `🚀 CORS Proxy Server running on http://localhost:8080`

4. **Start the web server** (in terminal 2):
   ```bash
   python -m http.server 8000 --directory src
   ```
   You should see: `Serving HTTP on :: port 8000`

5. **Open your browser** and go to: `http://localhost:8000`

6. **That's it!** The app is ready to use with full auto-calculation features.

**To stop the servers:** Press `Ctrl+C` in each terminal window.

**New Organized Structure**: The project is now organized into clear folders. See [docs/CODE_ORGANIZATION.md](docs/CODE_ORGANIZATION.md) for details.

### Alternative 1: Deploy to AWS (Production-Ready)

For a production deployment with global CDN and serverless backend:

**Check prerequisites first:**
```bash
python scripts/check_aws_setup.py
```

**Then deploy:**
```bash
python scripts/deploy.py
```

This deploys to AWS with:
- ☁️ CloudFront CDN for global access
- 🔒 HTTPS enabled automatically
- ⚡ Lambda-based CORS proxy (no local server needed)
- �️ WAF protection (rate limiting + DDoS prevention)
- 📊 CloudWatch monitoring and alarms
- 🚦 API throttling (optimized for 10-25 users)
- 💰 Free tier eligible (~$6-11/month with WAF, $1-3/month without)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Security & Monitoring**: See [SECURITY_MONITORING.md](SECURITY_MONITORING.md) for details on:
- API Gateway throttling (10 req/s)
- WAF protection rules
- CloudWatch alarms
- Cost optimization options

**Prerequisites**: AWS account, AWS CLI, Node.js, and CDK installed

### Alternative 2: Manual Entry Without Servers

If you don't want to run servers or deploy to AWS:
1. Open `index.html` directly in your browser
2. Manually enter all fields (shares and purchase price)
3. Auto-calculation features won't work, but manual tracking will

## 📊 How to Use

### Adding a Purchase Record

1. Click the "Add Purchase Record" section
2. Fill in the form:
   - **Purchase Date** (required): The date you received the shares
   - **HUF Contributed** (required): Total amount deducted from your payroll (in HUF)
   - **Shares Received** (optional): Number of shares you received - leave empty to auto-calculate
   - **Purchase Price (USD)** (optional): The stock price on purchase date - leave empty to auto-calculate with 15% ESPP discount
3. Click "Add Purchase"

**Auto-Calculation Feature:**
- If you leave **Shares Received** or **Purchase Price** empty, the app will:
  1. Fetch the historical stock price for the purchase date
  2. Apply the 15% ESPP discount automatically
  3. Fetch the USD/HUF exchange rate for that date
  4. Calculate the number of shares based on your HUF contribution

**Manual Entry Example:**
- You contributed 500,000 HUF over 6 months
- Purchase date: 2026-01-15
- Stock price on that date: $250 (before discount)
- Price after 15% discount: $212.50
- You received: 500,000 HUF ÷ (212.50 × exchange rate) = ~X shares

**Auto-Calculation Example:**
- Just enter: Purchase date (2026-01-15) and HUF Contributed (500,000)
- Leave Shares and Price empty
- Click "Add Purchase"
- The app fetches historical data and calculates everything for you! ✨

### Understanding the Dashboard

The dashboard shows:
- **Current Stock Price**: Real-time EPAM stock price in USD
- **USD/HUF Rate**: Current exchange rate
- **Total Shares**: Total number of shares you own
- **Total Contributed**: Total HUF you've invested
- **Current Value**: Current worth of all shares in HUF
- **Total Profit/Loss**: Your gain/loss in HUF and percentage

### Refreshing Prices

- Click the "🔄 Refresh Prices" button to update stock price and exchange rate
- The app caches data for 5 minutes to avoid API rate limits
- Last update timestamp is shown below the button

### Exporting Data

1. Click "📥 Export CSV" to download your purchase history
2. File is saved as `epam-purchases-YYYY-MM-DD.csv`
3. Use this to backup your data regularly

### Importing Data

1. Click "📤 Import CSV"
2. Select a previously exported CSV file
3. All purchases from the file will be added to your history

## 🔧 Technical Details

### Technology Stack

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Storage**: Browser localStorage (up to 10MB)
- **APIs**:
  - Yahoo Finance API for EPAM stock prices
  - exchangerate-api.com for USD/HUF conversion
- **Fallback APIs**:
  - Alpha Vantage for stock prices (if Yahoo fails)
  - frankfurter.app for currency rates (if primary fails)

### Data Structure

All data is stored in browser localStorage under the key `epamStockTracker`:

```json
{
  "purchases": [
    {
      "id": "unique-id",
      "date": "2026-01-15",
      "hufContributed": 500000,
      "sharesReceived": 25.5,
      "purchasePriceUSD": 212.50,
      "discountApplied": 15
    }
  ],
  "settings": {
    "stockTicker": "EPAM",
    "currency": "HUF",
    "lastRefresh": "2026-06-11T10:30:00Z"
  }
}
```

### Calculation Formulas

**Current Value (per purchase):**
```
Current Value = Shares × Current Price USD × Exchange Rate
```

**Profit/Loss:**
```
Profit/Loss = Current Value - HUF Contributed
```

**Profit/Loss Percentage:**
```
Profit/Loss % = (Profit/Loss ÷ HUF Contributed) × 100
```

**Cost per Share (in HUF):**
```
Cost per Share = HUF Contributed ÷ Shares Received
```

## 🔒 Privacy & Security

- **No server**: All data stays in your browser
- **No tracking**: No analytics or data collection
- **No login required**: No personal information needed
- **Local storage only**: Data never leaves your device (except API calls for prices)

**Important Notes:**
- Data is tied to your browser. If you clear browser data, your records will be lost.
- Export your data regularly as backup
- Use the same browser/device to access your data
- Incognito/Private browsing mode doesn't save data permanently

## 🐛 Troubleshooting

### Prices not loading?

**Issue**: "Failed to fetch stock price" error

**Solutions**:
1. Check your internet connection
2. Wait a few minutes and try again (API may be temporarily down)
3. Check browser console (F12) for specific error messages
4. Try using a different browser
5. Some corporate networks block external APIs - try from home

### Data disappeared?

**Issue**: All purchase records are gone

**Possible causes**:
1. Browser cache was cleared
2. Using different browser or incognito mode
3. Browser data was reset

**Prevention**:
- Export your data regularly (weekly/monthly)
- Keep CSV backups in a safe location
- Don't use incognito/private browsing mode

### Exchange rate seems wrong?

**Issue**: USD/HUF rate doesn't match your bank

**Explanation**:
- APIs provide mid-market rates (average of buy/sell)
- Banks add margins (1-3%) to exchange rates
- Rates update throughout the day
- The app shows real-time rates, not historical rates from your purchase date

### Import not working?

**Issue**: CSV import fails

**Solutions**:
1. Make sure the CSV file was exported from this app
2. Don't modify the CSV file structure (keep headers intact)
3. Check that all numeric values are valid (no letters in number fields)
4. Ensure date format is YYYY-MM-DD

## 🆘 API Rate Limits

### Yahoo Finance API
- **Limit**: ~2000 requests/hour
- **Caching**: 5 minutes (reduces requests to ~12 per hour)
- **If exceeded**: Fallback to Alpha Vantage or use cached data

### exchangerate-api.com
- **Limit**: 1500 requests/month (free tier)
- **Caching**: 5 minutes (reduces to ~300 requests/month)
- **If exceeded**: Fallback to frankfurter.app

### Alpha Vantage (Fallback)
- **Limit**: 5 requests/minute, 500 requests/day (free tier)
- **API Key**: Using demo key (very limited)
- **Improvement**: Get your own free key from alphavantage.co

**Recommendation**: Don't spam the refresh button. 5-minute caching is sufficient for tracking purposes.

## 📝 CSV File Format

When you export data, the CSV file has this format:

```csv
Date,HUF Contributed,Shares Received,Purchase Price USD,Discount %
2026-01-15,500000,25.5,212.50,15
2025-07-20,450000,22.3,203.40,15
```

You can edit this file in Excel/Google Sheets, but maintain the structure when importing back.

## 🎨 Customization

### Changing Colors

Edit `styles.css` at the top `:root` section:

```css
:root {
    --primary-color: #2563eb;  /* Main blue color */
    --profit-color: #22c55e;   /* Green for profits */
    --loss-color: #ef4444;     /* Red for losses */
    /* ... more colors ... */
}
```

### Adding New Features

The codebase is modular:
- `storage.js` - Data operations (add/edit/delete purchases)
- `api.js` - External API calls (stock price, currency)
- `calculator.js` - All calculations (profit/loss, totals)
- `app.js` - UI logic and event handlers
- `styles.css` - Visual styling

## 🤝 Contributing

This is a personal project, but improvements are welcome! Common enhancements:

- Historical price charts
- Multiple stock ticker support
- Tax calculation features
- Dividend tracking
- Email price alerts
- Mobile app version
- Multi-currency support

## 📜 License

This project is free to use, modify, and distribute. No warranty provided.

## ⚠️ Disclaimer

This tool is for personal tracking purposes only. It should not be used as the sole basis for financial decisions. Always verify calculations with official company documents and tax advisors.

- Stock prices may be delayed
- Exchange rates are approximate
- No guarantee of data accuracy
- Not financial advice

## 📞 Support

For issues or questions:

1. Check the Troubleshooting section above
2. Review browser console (F12) for error messages
3. Ensure all files are in the same folder
4. Try clearing browser cache and refreshing

## 🎉 Enjoy Tracking Your EPAM Stock!

Remember to:
- ✅ Export your data regularly
- ✅ Refresh prices weekly/monthly (not too frequently)
- ✅ Keep your purchase records accurate
- ✅ Backup CSV files in a safe location

**Happy investing! 📈**
