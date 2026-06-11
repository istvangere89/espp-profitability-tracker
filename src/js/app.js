/**
 * Main Application Module
 * Coordinates UI interactions, data flow, and updates
 */

const App = {
    // Current market data
    currentStockPrice: null,
    currentExchangeRate: null,

    /**
     * Initialize the application
     */
    async init() {
        console.log('Initializing EPAM Stock Tracker...');
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Load and display data
        await this.refreshData();
        
        // Display purchase history
        this.renderPurchaseTable();
        
        console.log('Application initialized successfully');
    },

    /**
     * Set up all event listeners
     */
    setupEventListeners() {
        // Purchase form submission
        const purchaseForm = document.getElementById('purchaseForm');
        purchaseForm.addEventListener('submit', (e) => this.handlePurchaseSubmit(e));

        // Refresh button
        const refreshBtn = document.getElementById('refreshBtn');
        refreshBtn.addEventListener('click', () => this.handleRefresh());

        // Export button
        const exportBtn = document.getElementById('exportBtn');
        exportBtn.addEventListener('click', () => this.handleExport());

        // Import file input
        const importFile = document.getElementById('importFile');
        importFile.addEventListener('change', (e) => this.handleImport(e));
    },

    /**
     * Refresh market data and update display
     */
    async refreshData() {
        const refreshBtn = document.getElementById('refreshBtn');
        const originalText = refreshBtn.textContent;
        
        try {
            // Show loading state
            refreshBtn.textContent = '⏳ Loading...';
            refreshBtn.disabled = true;

            // Fetch data from APIs
            const result = await API.fetchAllData();

            if (result.success) {
                this.currentStockPrice = result.stockPrice;
                this.currentExchangeRate = result.exchangeRate;

                // Update display
                this.updateDashboard();
                this.renderPurchaseTable();

                // Update last refresh timestamp
                Storage.updateLastRefresh();
                this.updateLastRefreshDisplay();

                // Show success message briefly
                this.showNotification('✅ Data refreshed successfully', 'success');
            } else {
                throw new Error(result.error || 'Failed to fetch data');
            }
        } catch (error) {
            console.error('Error refreshing data:', error);
            this.showNotification(`❌ Error: ${error.message}`, 'error');
            
            // Try to use cached data
            if (API.cache.stockPrice && API.cache.exchangeRate) {
                this.currentStockPrice = API.cache.stockPrice.data.price;
                this.currentExchangeRate = API.cache.exchangeRate.data.rate;
                this.updateDashboard();
                this.showNotification('⚠️ Using cached data (may be outdated)', 'warning');
            }
        } finally {
            // Reset button state
            refreshBtn.textContent = originalText;
            refreshBtn.disabled = false;
        }
    },

    /**
     * Update dashboard with current market data and portfolio summary
     */
    updateDashboard() {
        // Update current price and exchange rate
        document.getElementById('currentPrice').textContent = 
            this.currentStockPrice ? Calculator.formatUSD(this.currentStockPrice) : 'N/A';
        
        document.getElementById('exchangeRate').textContent = 
            this.currentExchangeRate ? Calculator.formatExchangeRate(this.currentExchangeRate) : 'N/A';

        // Calculate and display portfolio totals
        if (this.currentStockPrice && this.currentExchangeRate) {
            const purchases = Storage.getPurchases();
            const totals = Calculator.calculatePortfolioTotals(
                purchases,
                this.currentStockPrice,
                this.currentExchangeRate
            );

            document.getElementById('totalShares').textContent = 
                Calculator.formatShares(totals.totalShares);
            
            document.getElementById('totalContributed').textContent = 
                Calculator.formatHUF(totals.totalContributed);
            
            document.getElementById('currentValue').textContent = 
                Calculator.formatHUF(totals.currentValue);

            const profitLossElement = document.getElementById('totalProfitLoss');
            const profitLossText = `${Calculator.formatHUF(totals.totalProfitLoss)} (${Calculator.formatPercentage(totals.totalProfitLossPercentage)})`;
            profitLossElement.textContent = profitLossText;
            
            // Apply styling based on profit/loss
            profitLossElement.className = 'value ' + Calculator.getProfitLossClass(totals.totalProfitLoss);
        }
    },

    /**
     * Update last refresh timestamp display
     */
    updateLastRefreshDisplay() {
        const settings = Storage.getSettings();
        const lastUpdateElement = document.getElementById('lastUpdate');
        
        if (settings && settings.lastRefresh) {
            const date = new Date(settings.lastRefresh);
            lastUpdateElement.textContent = date.toLocaleString('hu-HU');
        } else {
            lastUpdateElement.textContent = 'Never';
        }
    },

    /**
     * Render purchase history table
     */
    renderPurchaseTable() {
        const tbody = document.getElementById('purchaseTableBody');
        const purchases = Storage.getPurchases();

        // Clear existing rows
        tbody.innerHTML = '';

        if (purchases.length === 0) {
            tbody.innerHTML = '<tr class="empty-state"><td colspan="10">No purchase records yet. Add your first purchase above!</td></tr>';
            return;
        }

        // Render each purchase
        purchases.forEach(purchase => {
            const row = this.createPurchaseRow(purchase);
            tbody.appendChild(row);
        });
    },

    /**
     * Create a table row for a purchase
     */
    createPurchaseRow(purchase) {
        const tr = document.createElement('tr');

        // Calculate metrics if market data is available
        let metrics = null;
        if (this.currentStockPrice && this.currentExchangeRate) {
            metrics = Calculator.calculatePurchaseMetrics(
                purchase,
                this.currentStockPrice,
                this.currentExchangeRate
            );
        }

        // Date
        const tdDate = document.createElement('td');
        tdDate.textContent = new Date(purchase.date).toLocaleDateString('hu-HU');
        tr.appendChild(tdDate);

        // HUF Contributed
        const tdHUF = document.createElement('td');
        tdHUF.textContent = Calculator.formatHUF(purchase.hufContributed);
        tr.appendChild(tdHUF);

        // Shares
        const tdShares = document.createElement('td');
        tdShares.textContent = Calculator.formatShares(purchase.sharesReceived);
        tr.appendChild(tdShares);

        // Purchase Price USD (after discount)
        const tdPurchasePrice = document.createElement('td');
        tdPurchasePrice.textContent = Calculator.formatUSD(purchase.purchasePriceUSD);
        tr.appendChild(tdPurchasePrice);

        // Fair Price USD (before discount)
        const tdFairPrice = document.createElement('td');
        const fairPrice = purchase.purchasePriceUSD / 0.85; // Reverse the 15% discount
        tdFairPrice.textContent = Calculator.formatUSD(fairPrice);
        tdFairPrice.style.color = 'var(--text-secondary)';
        tdFairPrice.title = 'Market price before 15% ESPP discount';
        tr.appendChild(tdFairPrice);

        // Cost per Share (HUF)
        const tdCostPerShare = document.createElement('td');
        if (metrics) {
            tdCostPerShare.textContent = Calculator.formatHUF(metrics.costPerShare);
        } else {
            tdCostPerShare.textContent = 'N/A';
        }
        tr.appendChild(tdCostPerShare);

        // Current Value (HUF)
        const tdCurrentValue = document.createElement('td');
        if (metrics) {
            tdCurrentValue.textContent = Calculator.formatHUF(metrics.currentValue);
        } else {
            tdCurrentValue.textContent = 'N/A';
        }
        tr.appendChild(tdCurrentValue);

        // Profit/Loss (HUF)
        const tdProfitLoss = document.createElement('td');
        if (metrics) {
            tdProfitLoss.textContent = Calculator.formatHUF(metrics.profitLoss);
            tdProfitLoss.className = Calculator.getProfitLossClass(metrics.profitLoss);
        } else {
            tdProfitLoss.textContent = 'N/A';
        }
        tr.appendChild(tdProfitLoss);

        // Profit/Loss %
        const tdProfitLossPercent = document.createElement('td');
        if (metrics) {
            tdProfitLossPercent.textContent = Calculator.formatPercentage(metrics.profitLossPercentage);
            tdProfitLossPercent.className = Calculator.getProfitLossClass(metrics.profitLoss);
        } else {
            tdProfitLossPercent.textContent = 'N/A';
        }
        tr.appendChild(tdProfitLossPercent);

        // Actions
        const tdActions = document.createElement('td');
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '🗑️';
        deleteBtn.className = 'btn-delete';
        deleteBtn.title = 'Delete purchase';
        deleteBtn.onclick = () => this.handleDelete(purchase.id);
        tdActions.appendChild(deleteBtn);
        tr.appendChild(tdActions);

        return tr;
    },

    /**
     * Handle purchase form submission
     */
    async handlePurchaseSubmit(e) {
        e.preventDefault();

        // Get form values
        const date = document.getElementById('purchaseDate').value;
        const hufContributed = parseFloat(document.getElementById('hufContributed').value);
        let sharesReceived = parseFloat(document.getElementById('sharesReceived').value);
        let purchasePriceUSD = parseFloat(document.getElementById('purchasePriceUSD').value);

        // Validate required fields
        if (!date || !hufContributed) {
            this.showNotification('❌ Please enter purchase date and HUF contributed', 'error');
            return;
        }

        if (hufContributed <= 0) {
            this.showNotification('❌ HUF contributed must be greater than zero', 'error');
            return;
        }

        // Check if we need to auto-calculate
        const needsAutoCalculation = !sharesReceived || !purchasePriceUSD;

        if (needsAutoCalculation) {
            try {
                this.showNotification('⏳ Fetching historical data...', 'info');
                
                // Fetch historical data for the purchase date
                const [historicalPrice, historicalRate] = await Promise.all([
                    API.getHistoricalStockPrice(date),
                    API.getHistoricalExchangeRate(date)
                ]);

                // Apply 15% ESPP discount to market price
                const discountedPrice = historicalPrice * 0.85;
                purchasePriceUSD = purchasePriceUSD || discountedPrice;

                // Calculate shares: HUF contributed / (purchase price in HUF)
                const purchasePriceHUF = purchasePriceUSD * historicalRate;
                sharesReceived = sharesReceived || (hufContributed / purchasePriceHUF);

                this.showNotification(`✅ Auto-calculated: ${sharesReceived.toFixed(4)} shares at $${purchasePriceUSD.toFixed(2)} (15% discount applied)`, 'success');
                
            } catch (error) {
                console.error('Auto-calculation error:', error);
                this.showNotification(`❌ ${error.message}`, 'error');
                return;
            }
        }

        // Validate calculated/entered values
        if (sharesReceived <= 0 || purchasePriceUSD <= 0) {
            this.showNotification('❌ Shares and purchase price must be greater than zero', 'error');
            return;
        }

        // Create purchase object
        const purchase = {
            date: date,
            hufContributed: hufContributed,
            sharesReceived: sharesReceived,
            purchasePriceUSD: purchasePriceUSD,
            discountApplied: 15
        };

        // Add to storage
        if (Storage.addPurchase(purchase)) {
            this.showNotification('✅ Purchase added successfully', 'success');
            
            // Reset form
            e.target.reset();
            
            // Update displays
            this.updateDashboard();
            this.renderPurchaseTable();
        } else {
            this.showNotification('❌ Failed to add purchase', 'error');
        }
    },

    /**
     * Handle delete purchase
     */
    handleDelete(id) {
        if (confirm('Are you sure you want to delete this purchase record?')) {
            if (Storage.deletePurchase(id)) {
                this.showNotification('✅ Purchase deleted', 'success');
                this.updateDashboard();
                this.renderPurchaseTable();
            } else {
                this.showNotification('❌ Failed to delete purchase', 'error');
            }
        }
    },

    /**
     * Handle refresh button click
     */
    async handleRefresh() {
        await this.refreshData();
    },

    /**
     * Handle export to CSV
     */
    handleExport() {
        const csvContent = Storage.exportToCSV();
        
        if (!csvContent) {
            this.showNotification('❌ No data to export', 'error');
            return;
        }

        // Create download link
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        
        link.setAttribute('href', url);
        link.setAttribute('download', `epam-purchases-${new Date().toISOString().split('T')[0]}.csv`);
        link.style.visibility = 'hidden';
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        this.showNotification('✅ Data exported successfully', 'success');
    },

    /**
     * Handle import from CSV
     */
    handleImport(e) {
        const file = e.target.files[0];
        
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            const csvContent = event.target.result;
            const result = Storage.importFromCSV(csvContent);

            if (result.success) {
                this.showNotification(`✅ Imported ${result.count} purchases`, 'success');
                this.updateDashboard();
                this.renderPurchaseTable();
            } else {
                this.showNotification(`❌ Import failed: ${result.error}`, 'error');
            }

            // Reset file input
            e.target.value = '';
        };

        reader.readAsText(file);
    },

    /**
     * Show notification message
     */
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;

        // Add to page
        document.body.appendChild(notification);

        // Trigger animation
        setTimeout(() => notification.classList.add('show'), 10);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
};

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
} else {
    App.init();
}
