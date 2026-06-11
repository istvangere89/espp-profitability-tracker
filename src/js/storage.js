/**
 * Storage Module - Handles all localStorage operations
 * Data structure: { purchases: [], settings: {} }
 */

const Storage = {
    STORAGE_KEY: 'epamStockTracker',

    /**
     * Initialize storage with default structure if empty
     */
    init() {
        if (!localStorage.getItem(this.STORAGE_KEY)) {
            const defaultData = {
                purchases: [],
                settings: {
                    stockTicker: 'EPAM',
                    currency: 'HUF',
                    lastRefresh: null
                }
            };
            this.saveData(defaultData);
        }
    },

    /**
     * Get all data from localStorage
     */
    getData() {
        try {
            const data = localStorage.getItem(this.STORAGE_KEY);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return null;
        }
    },

    /**
     * Save all data to localStorage
     */
    saveData(data) {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(data));
            return true;
        } catch (error) {
            console.error('Error saving to localStorage:', error);
            return false;
        }
    },

    /**
     * Get all purchases
     */
    getPurchases() {
        const data = this.getData();
        return data ? data.purchases : [];
    },

    /**
     * Add a new purchase
     */
    addPurchase(purchase) {
        const data = this.getData();
        if (!data) return false;

        // Generate unique ID
        purchase.id = this.generateId();
        
        // Add to purchases array
        data.purchases.push(purchase);
        
        // Sort by date (newest first)
        data.purchases.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        return this.saveData(data);
    },

    /**
     * Update an existing purchase
     */
    updatePurchase(id, updatedPurchase) {
        const data = this.getData();
        if (!data) return false;

        const index = data.purchases.findIndex(p => p.id === id);
        if (index === -1) return false;

        // Preserve the ID
        updatedPurchase.id = id;
        data.purchases[index] = updatedPurchase;

        // Sort by date (newest first)
        data.purchases.sort((a, b) => new Date(b.date) - new Date(a.date));

        return this.saveData(data);
    },

    /**
     * Delete a purchase
     */
    deletePurchase(id) {
        const data = this.getData();
        if (!data) return false;

        data.purchases = data.purchases.filter(p => p.id !== id);
        return this.saveData(data);
    },

    /**
     * Get a single purchase by ID
     */
    getPurchase(id) {
        const purchases = this.getPurchases();
        return purchases.find(p => p.id === id);
    },

    /**
     * Update settings
     */
    updateSettings(settings) {
        const data = this.getData();
        if (!data) return false;

        data.settings = { ...data.settings, ...settings };
        return this.saveData(data);
    },

    /**
     * Get settings
     */
    getSettings() {
        const data = this.getData();
        return data ? data.settings : null;
    },

    /**
     * Update last refresh timestamp
     */
    updateLastRefresh() {
        const data = this.getData();
        if (!data) return false;

        data.settings.lastRefresh = new Date().toISOString();
        return this.saveData(data);
    },

    /**
     * Generate a unique ID
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },

    /**
     * Export all data as JSON
     */
    exportData() {
        return this.getData();
    },

    /**
     * Import data from JSON (replaces existing data)
     */
    importData(data) {
        if (!data || !data.purchases || !data.settings) {
            console.error('Invalid import data structure');
            return false;
        }
        return this.saveData(data);
    },

    /**
     * Clear all data (with confirmation)
     */
    clearAll() {
        try {
            localStorage.removeItem(this.STORAGE_KEY);
            this.init();
            return true;
        } catch (error) {
            console.error('Error clearing localStorage:', error);
            return false;
        }
    },

    /**
     * Export purchases to CSV format
     */
    exportToCSV() {
        const purchases = this.getPurchases();
        if (purchases.length === 0) {
            return null;
        }

        // CSV headers
        const headers = ['Date', 'HUF Contributed', 'Shares Received', 'Purchase Price USD', 'Fair Price USD', 'Discount %'];
        
        // CSV rows
        const rows = purchases.map(p => {
            const fairPrice = p.purchasePriceUSD / 0.85; // Calculate fair price
            return [
                p.date,
                p.hufContributed,
                p.sharesReceived,
                p.purchasePriceUSD,
                fairPrice.toFixed(2),
                p.discountApplied || 15
            ];
        });

        // Combine headers and rows
        const csvContent = [
            headers.join(','),
            ...rows.map(row => row.join(','))
        ].join('\n');

        return csvContent;
    },

    /**
     * Import purchases from CSV format
     */
    importFromCSV(csvContent) {
        try {
            const lines = csvContent.trim().split('\n');
            if (lines.length < 2) {
                throw new Error('CSV file is empty or invalid');
            }

            // Skip header row
            const dataLines = lines.slice(1);
            const purchases = [];

            for (const line of dataLines) {
                const [date, hufContributed, sharesReceived, purchasePriceUSD, discountApplied] = line.split(',');
                
                purchases.push({
                    date: date.trim(),
                    hufContributed: parseFloat(hufContributed),
                    sharesReceived: parseFloat(sharesReceived),
                    purchasePriceUSD: parseFloat(purchasePriceUSD),
                    discountApplied: parseFloat(discountApplied) || 15
                });
            }

            // Add all purchases
            let successCount = 0;
            for (const purchase of purchases) {
                if (this.addPurchase(purchase)) {
                    successCount++;
                }
            }

            return { success: true, count: successCount };
        } catch (error) {
            console.error('Error importing CSV:', error);
            return { success: false, error: error.message };
        }
    }
};

// Initialize storage on load
Storage.init();
