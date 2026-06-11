"""
AWS Lambda CORS Proxy Handler
Fetches data from external APIs and adds CORS headers

Caching Strategy:
- Returns Cache-Control: public, max-age=3600 (1 hour)
- Browsers cache responses to reduce Lambda invocations
- Reduces load on external APIs (Yahoo Finance, Exchange Rate APIs)
- Keeps data reasonably fresh for stock tracking
"""

import json
import urllib.request
import urllib.parse


def handler(event, context):
    """
    Lambda handler for CORS proxy requests
    Expects: ?url=<encoded_url> as query parameter
    """
    
    print(f"Received event: {json.dumps(event)}")
    
    # Get the target URL from query parameters
    query_params = event.get('queryStringParameters', {})
    
    if not query_params or 'url' not in query_params:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps({
                'error': 'Missing url parameter',
                'usage': 'GET /?url=<encoded_url>'
            })
        }
    
    target_url = query_params['url']
    
    try:
        # Make request to target URL
        req = urllib.request.Request(
            target_url,
            headers={'User-Agent': 'Mozilla/5.0 (EPAM Stock Tracker Lambda Proxy)'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
            content_type = response.headers.get('Content-Type', 'application/json')
            
            # Return response with CORS headers and caching
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': content_type,
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, OPTIONS',
                    'Access-Control-Allow-Headers': '*',
                    'Cache-Control': 'public, max-age=3600',  # Cache for 1 hour
                    'X-Cache-Policy': 'Cached for 1 hour'
                },
                'body': content.decode('utf-8')
            }
            
    except urllib.error.HTTPError as e:
        print(f'HTTP Error: {e.code} - {e.reason}')
        return {
            'statusCode': e.code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'HTTP {e.code}: {e.reason}',
                'target_url': target_url
            })
        }
        
    except urllib.error.URLError as e:
        print(f'URL Error: {e.reason}')
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Failed to fetch: {str(e.reason)}',
                'target_url': target_url
            })
        }
        
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Internal error: {str(e)}',
                'target_url': target_url
            })
        }
