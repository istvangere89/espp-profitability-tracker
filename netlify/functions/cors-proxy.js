/**
 * CORS Proxy for Stock & Currency APIs
 * 
 * This Netlify Function replaces the AWS Lambda CORS proxy
 * It handles requests for:
 * - Yahoo Finance stock prices
 * - Currency exchange rates
 * 
 * Caches responses for 5 minutes to avoid rate limits
 */

export default async (req, context) => {
  // Only allow GET requests
  if (req.method !== 'GET') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  const url = new URL(req.url);
  const targetUrl = url.searchParams.get('url');

  // Validate URL parameter
  if (!targetUrl) {
    return new Response(
      JSON.stringify({ error: 'URL parameter required' }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }

  // Security: Only allow specific domains
  const allowedDomains = [
    'query1.finance.yahoo.com',
    'query2.finance.yahoo.com',
    'api.exchangerate-api.com',
    'api.exchangerate.host',
    'open.er-api.com'
  ];

  try {
    const urlObj = new URL(targetUrl);
    if (!allowedDomains.some(domain => urlObj.hostname.includes(domain))) {
      return new Response(
        JSON.stringify({ error: 'Domain not allowed' }),
        {
          status: 403,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
  } catch (e) {
    return new Response(
      JSON.stringify({ error: 'Invalid URL' }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }

  try {
    const response = await fetch(targetUrl, {
      method: 'GET',
      headers: {
        'User-Agent': 'ESPP-Profitability-Tracker/1.0',
        'Accept': 'application/json'
      },
      timeout: 10000
    });

    // Handle non-OK responses
    if (!response.ok) {
      return new Response(
        JSON.stringify({ 
          error: `API Error: ${response.status} ${response.statusText}`,
          status: response.status
        }),
        {
          status: response.status,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }

    const data = await response.json();

    // Return with caching headers (5 minute cache)
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=300',  // 5 minute cache
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
      }
    });
  } catch (error) {
    console.error('CORS Proxy Error:', error);
    
    return new Response(
      JSON.stringify({ 
        error: error.message || 'Internal server error',
        details: process.env.CONTEXT === 'dev' ? error.stack : undefined
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
};
