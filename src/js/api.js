/**
 * API Module - Handles stock price and currency conversion API calls
 * Uses caching to avoid rate limits
 */

const API = {
    // Cache duration in milliseconds (5 minutes)
    CACHE_DURATION: 5 * 60 * 1000,
    
    // Cache storage
    cache: {
        stockPrice: null,
        exchangeRate: null
    },

    /**
     * Fetch current EPAM stock price (in USD)
     * Uses Yahoo Finance API through financialmodelingprep or alternative
     */
    async getStockPrice() {
        // Check cache first
        if (this.cache.stockPrice && this.isCacheValid(this.cache.stockPrice.timestamp)) {
            return this.cache.stockPrice.data;
        }

        try {
            // Method 1: Try Yahoo Finance query via local proxy
            const symbol = 'EPAM';
            const yahooUrl = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}`;
            const proxyUrl = `http://localhost:8080?url=${encodeURIComponent(yahooUrl)}`;
            const response = await fetch(proxyUrl, {
                method: 'GET'
            });

            if (!response.ok) {
                throw new Error('Failed to fetch stock price from Yahoo Finance');
            }

            const data = await response.json();
            
            if (data.chart && data.chart.result && data.chart.result[0]) {
                const result = data.chart.result[0];
                const price = result.meta.regularMarketPrice;
                
                // Cache the result
                this.cache.stockPrice = {
                    data: {
                        price: price,
                        symbol: symbol,
                        currency: 'USD'
                    },
                    timestamp: Date.now()
                };

                return this.cache.stockPrice.data;
            }

            throw new Error('Invalid response format from Yahoo Finance');

        } catch (error) {
            console.error('Error fetching stock price:', error);
            
            // Try fallback method - Alpha Vantage (requires free API key)
            try {
                return await this.getStockPriceFallback();
            } catch (fallbackError) {
                console.error('Fallback also failed:', fallbackError);
                
                // Return cached data if available, even if expired
                if (this.cache.stockPrice) {
                    console.warn('Using expired cache data');
                    return this.cache.stockPrice.data;
                }
                
                throw new Error('Unable to fetch stock price. Please try again later.');
            }
        }
    },

    /**
     * Fallback method for stock price using Alpha Vantage
     * Note: Requires API key - users should get their own free key from alphavantage.co
     */
    async getStockPriceFallback() {
        // For demo purposes, using demo key (very limited)
        // Users should replace with their own key
        const apiKey = 'demo'; // Replace with actual key
        const symbol = 'EPAM';
        
        const avUrl = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${apiKey}`;
        const proxyUrl = `http://localhost:8080?url=${encodeURIComponent(avUrl)}`;
        const response = await fetch(proxyUrl);

        if (!response.ok) {
            throw new Error('Alpha Vantage API request failed');
        }

        const data = await response.json();
        
        if (data['Global Quote'] && data['Global Quote']['05. price']) {
            const price = parseFloat(data['Global Quote']['05. price']);
            
            // Cache the result
            this.cache.stockPrice = {
                data: {
                    price: price,
                    symbol: symbol,
                    currency: 'USD'
                },
                timestamp: Date.now()
            };

            return this.cache.stockPrice.data;
        }

        throw new Error('Invalid response from Alpha Vantage');
    },

    /**
     * Fetch USD to HUF exchange rate
     * Uses exchangerate-api.com (free, no API key needed)
     */
    async getExchangeRate() {
        // Check cache first
        if (this.cache.exchangeRate && this.isCacheValid(this.cache.exchangeRate.timestamp)) {
            return this.cache.exchangeRate.data;
        }

        try {
            // Using local proxy for reliability
            const exchangeUrl = 'https://api.exchangerate-api.com/v4/latest/USD';
            const proxyUrl = `http://localhost:8080?url=${encodeURIComponent(exchangeUrl)}`;
            const response = await fetch(proxyUrl);

            if (!response.ok) {
                throw new Error('Failed to fetch exchange rates');
            }

            const data = await response.json();
            
            if (data.rates && data.rates.HUF) {
                const rate = data.rates.HUF;
                
                // Cache the result
                this.cache.exchangeRate = {
                    data: {
                        rate: rate,
                        from: 'USD',
                        to: 'HUF',
                        date: data.date
                    },
                    timestamp: Date.now()
                };

                return this.cache.exchangeRate.data;
            }

            throw new Error('HUF rate not found in response');

        } catch (error) {
            console.error('Error fetching exchange rate:', error);
            
            // Try alternative API
            try {
                return await this.getExchangeRateFallback();
            } catch (fallbackError) {
                console.error('Exchange rate fallback also failed:', fallbackError);
                
                // Return cached data if available, even if expired
                if (this.cache.exchangeRate) {
                    console.warn('Using expired exchange rate cache data');
                    return this.cache.exchangeRate.data;
                }
                
                throw new Error('Unable to fetch exchange rate. Please try again later.');
            }
        }
    },

    /**
     * Fallback method for exchange rate using frankfurter.app
     */
    async getExchangeRateFallback() {
        const frankfurterUrl = 'https://api.frankfurter.app/latest?from=USD&to=HUF';
        const proxyUrl = `http://localhost:8080?url=${encodeURIComponent(frankfurterUrl)}`;
        const response = await fetch(proxyUrl);

        if (!response.ok) {
            throw new Error('Frankfurter API request failed');
        }

        const data = await response.json();
        
        if (data.rates && data.rates.HUF) {
            const rate = data.rates.HUF;
            
            // Cache the result
            this.cache.exchangeRate = {
                data: {
                    rate: rate,
                    from: 'USD',
                    to: 'HUF',
                    date: data.date
                },
                timestamp: Date.now()
            };

            return this.cache.exchangeRate.data;
        }

        throw new Error('HUF rate not found in fallback response');
    },

    /**
     * Fetch historical stock price for a specific date
     * @param {string} date - Date in YYYY-MM-DD format
     * @returns {Promise<number>} Stock price on that date
     */
    async getHistoricalStockPrice(date) {
        try {
            const symbol = 'EPAM';
            // Convert date to Unix timestamps for Yahoo Finance
            const dateObj = new Date(date);
            const period1 = Math.floor(dateObj.getTime() / 1000);
            const period2 = period1 + 86400; // Add one day
            
            const yahooUrl = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?period1=${period1}&period2=${period2}&interval=1d`;
            const proxyUrl = `http://localhost:8080?url=${encodeURIComponent(yahooUrl)}`;
            
            const response = await fetch(proxyUrl);
            
            if (!response.ok) {
                throw new Error('Failed to fetch historical stock price');
            }
            
            const data = await response.json();
            
            if (data.chart && data.chart.result && data.chart.result[0]) {
                const result = data.chart.result[0];
                const quotes = result.indicators.quote[0];
                
                // Try to get close price, fallback to open if close is not available
                const price = quotes.close[0] || quotes.open[0];
                
                if (price) {
                    return price;
                }
            }
            
            throw new Error('No historical price data available for this date');
            
        } catch (error) {
            console.error('Error fetching historical stock price:', error);
            throw new Error(`Unable to fetch stock price for ${date}. The market may have been closed on this date.`);
        }
    },

    /**
     * Fetch historical exchange rate for a specific date
     * @param {string} date - Date in YYYY-MM-DD format
     * @returns {Promise<number>} USD to HUF exchange rate on that date
     */
    async getHistoricalExchangeRate(date) {
        try {
            // Using frankfurter.app for historical rates (free and reliable)
            const frankfurterUrl = `https://api.frankfurter.app/${date}?from=USD&to=HUF`;
            const proxyUrl = `http://localhost:8080?url=${encodeURIComponent(frankfurterUrl)}`;
            
            const response = await fetch(proxyUrl);
            
            if (!response.ok) {
                throw new Error('Failed to fetch historical exchange rate');
            }
            
            const data = await response.json();
            
            if (data.rates && data.rates.HUF) {
                return data.rates.HUF;
            }
            
            throw new Error('HUF rate not found for this date');
            
        } catch (error) {
            console.error('Error fetching historical exchange rate:', error);
            
            // Fallback: try exchangerate-api (but it might not have historical data)
            try {
                // If historical data is not available, use current rate as fallback
                const currentRate = await this.getExchangeRate();
                console.warn(`Using current exchange rate as fallback for ${date}`);
                return currentRate.rate;
            } catch (fallbackError) {
                throw new Error(`Unable to fetch exchange rate for ${date}`);
            }
        }
    },

    /**
     * Fetch both stock price and exchange rate in parallel
     */
    async fetchAllData() {
        try {
            const [stockData, exchangeData] = await Promise.all([
                this.getStockPrice(),
                this.getExchangeRate()
            ]);

            return {
                success: true,
                stockPrice: stockData.price,
                exchangeRate: exchangeData.rate,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            console.error('Error fetching data:', error);
            return {
                success: false,
                error: error.message
            };
        }
    },

    /**
     * Check if cached data is still valid
     */
    isCacheValid(timestamp) {
        if (!timestamp) return false;
        return (Date.now() - timestamp) < this.CACHE_DURATION;
    },

    /**
     * Clear cache manually
     */
    clearCache() {
        this.cache = {
            stockPrice: null,
            exchangeRate: null
        };
    },

    /**
     * Get cache status
     */
    getCacheStatus() {
        return {
            stockPrice: {
                cached: !!this.cache.stockPrice,
                valid: this.cache.stockPrice ? this.isCacheValid(this.cache.stockPrice.timestamp) : false,
                age: this.cache.stockPrice ? Date.now() - this.cache.stockPrice.timestamp : null
            },
            exchangeRate: {
                cached: !!this.cache.exchangeRate,
                valid: this.cache.exchangeRate ? this.isCacheValid(this.cache.exchangeRate.timestamp) : false,
                age: this.cache.exchangeRate ? Date.now() - this.cache.exchangeRate.timestamp : null
            }
        };
    }
};
