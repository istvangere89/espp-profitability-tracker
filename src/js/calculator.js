/**
 * Calculator Module - Handles all profit/loss calculations
 */

const Calculator = {
    /**
     * Calculate current value of a purchase in HUF
     * @param {number} shares - Number of shares
     * @param {number} currentPriceUSD - Current stock price in USD
     * @param {number} exchangeRate - USD to HUF exchange rate
     * @returns {number} Current value in HUF
     */
    calculateCurrentValue(shares, currentPriceUSD, exchangeRate) {
        return shares * currentPriceUSD * exchangeRate;
    },

    /**
     * Calculate profit/loss for a purchase in HUF
     * @param {number} currentValue - Current value in HUF
     * @param {number} hufContributed - Amount contributed in HUF
     * @returns {number} Profit/loss in HUF
     */
    calculateProfitLoss(currentValue, hufContributed) {
        return currentValue - hufContributed;
    },

    /**
     * Calculate profit/loss percentage
     * @param {number} profitLoss - Profit/loss in HUF
     * @param {number} hufContributed - Amount contributed in HUF
     * @returns {number} Profit/loss percentage
     */
    calculateProfitLossPercentage(profitLoss, hufContributed) {
        if (hufContributed === 0) return 0;
        return (profitLoss / hufContributed) * 100;
    },

    /**
     * Calculate cost per share in HUF
     * @param {number} hufContributed - Amount contributed in HUF
     * @param {number} shares - Number of shares received
     * @returns {number} Cost per share in HUF
     */
    calculateCostPerShare(hufContributed, shares) {
        if (shares === 0) return 0;
        return hufContributed / shares;
    },

    /**
     * Calculate all metrics for a single purchase
     * @param {object} purchase - Purchase record
     * @param {number} currentPriceUSD - Current stock price in USD
     * @param {number} exchangeRate - USD to HUF exchange rate
     * @returns {object} All calculated metrics
     */
    calculatePurchaseMetrics(purchase, currentPriceUSD, exchangeRate) {
        const currentValue = this.calculateCurrentValue(
            purchase.sharesReceived,
            currentPriceUSD,
            exchangeRate
        );

        const profitLoss = this.calculateProfitLoss(
            currentValue,
            purchase.hufContributed
        );

        const profitLossPercentage = this.calculateProfitLossPercentage(
            profitLoss,
            purchase.hufContributed
        );

        const costPerShare = this.calculateCostPerShare(
            purchase.hufContributed,
            purchase.sharesReceived
        );

        return {
            id: purchase.id,
            date: purchase.date,
            hufContributed: purchase.hufContributed,
            sharesReceived: purchase.sharesReceived,
            purchasePriceUSD: purchase.purchasePriceUSD,
            costPerShare: costPerShare,
            currentValue: currentValue,
            profitLoss: profitLoss,
            profitLossPercentage: profitLossPercentage
        };
    },

    /**
     * Calculate portfolio totals
     * @param {array} purchases - Array of purchase records
     * @param {number} currentPriceUSD - Current stock price in USD
     * @param {number} exchangeRate - USD to HUF exchange rate
     * @returns {object} Portfolio totals
     */
    calculatePortfolioTotals(purchases, currentPriceUSD, exchangeRate) {
        if (!purchases || purchases.length === 0) {
            return {
                totalShares: 0,
                totalContributed: 0,
                currentValue: 0,
                totalProfitLoss: 0,
                totalProfitLossPercentage: 0
            };
        }

        let totalShares = 0;
        let totalContributed = 0;
        let currentValue = 0;

        purchases.forEach(purchase => {
            totalShares += purchase.sharesReceived;
            totalContributed += purchase.hufContributed;
            currentValue += this.calculateCurrentValue(
                purchase.sharesReceived,
                currentPriceUSD,
                exchangeRate
            );
        });

        const totalProfitLoss = this.calculateProfitLoss(currentValue, totalContributed);
        const totalProfitLossPercentage = this.calculateProfitLossPercentage(
            totalProfitLoss,
            totalContributed
        );

        return {
            totalShares: totalShares,
            totalContributed: totalContributed,
            currentValue: currentValue,
            totalProfitLoss: totalProfitLoss,
            totalProfitLossPercentage: totalProfitLossPercentage
        };
    },

    /**
     * Format number as currency (HUF)
     * @param {number} value - Number to format
     * @param {boolean} includeCurrency - Whether to include currency symbol
     * @returns {string} Formatted currency string
     */
    formatHUF(value, includeCurrency = true) {
        const formatted = new Intl.NumberFormat('hu-HU', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(Math.round(value));

        return includeCurrency ? `${formatted} HUF` : formatted;
    },

    /**
     * Format number as USD currency
     * @param {number} value - Number to format
     * @param {boolean} includeCurrency - Whether to include currency symbol
     * @returns {string} Formatted currency string
     */
    formatUSD(value, includeCurrency = true) {
        const formatted = new Intl.NumberFormat('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);

        return includeCurrency ? `$${formatted}` : formatted;
    },

    /**
     * Format number as shares (with 4 decimal places)
     * @param {number} value - Number to format
     * @returns {string} Formatted shares string
     */
    formatShares(value) {
        return new Intl.NumberFormat('en-US', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 4
        }).format(value);
    },

    /**
     * Format percentage
     * @param {number} value - Percentage value
     * @returns {string} Formatted percentage string
     */
    formatPercentage(value) {
        const sign = value >= 0 ? '+' : '';
        return `${sign}${value.toFixed(2)}%`;
    },

    /**
     * Format exchange rate
     * @param {number} rate - Exchange rate
     * @returns {string} Formatted rate string
     */
    formatExchangeRate(rate) {
        return new Intl.NumberFormat('hu-HU', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(rate);
    },

    /**
     * Get profit/loss class for styling (positive/negative)
     * @param {number} value - Profit/loss value
     * @returns {string} CSS class name
     */
    getProfitLossClass(value) {
        if (value > 0) return 'profit';
        if (value < 0) return 'loss';
        return 'neutral';
    },

    /**
     * Calculate average cost per share across all purchases
     * @param {array} purchases - Array of purchase records
     * @returns {number} Average cost per share in HUF
     */
    calculateAverageCostPerShare(purchases) {
        if (!purchases || purchases.length === 0) return 0;

        let totalHUF = 0;
        let totalShares = 0;

        purchases.forEach(purchase => {
            totalHUF += purchase.hufContributed;
            totalShares += purchase.sharesReceived;
        });

        return totalShares > 0 ? totalHUF / totalShares : 0;
    },

    /**
     * Calculate weighted average purchase price in USD
     * @param {array} purchases - Array of purchase records
     * @returns {number} Weighted average price in USD
     */
    calculateWeightedAveragePrice(purchases) {
        if (!purchases || purchases.length === 0) return 0;

        let totalValue = 0;
        let totalShares = 0;

        purchases.forEach(purchase => {
            totalValue += purchase.purchasePriceUSD * purchase.sharesReceived;
            totalShares += purchase.sharesReceived;
        });

        return totalShares > 0 ? totalValue / totalShares : 0;
    },

    /**
     * Calculate return on investment (ROI)
     * @param {number} currentValue - Current portfolio value
     * @param {number} totalInvested - Total amount invested
     * @returns {number} ROI as decimal (e.g., 0.25 for 25%)
     */
    calculateROI(currentValue, totalInvested) {
        if (totalInvested === 0) return 0;
        return (currentValue - totalInvested) / totalInvested;
    }
};
