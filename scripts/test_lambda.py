"""
Local test script for Lambda CORS proxy function
Tests the Lambda handler without deploying to AWS
"""

import sys
import json

# Add the lambda function path to Python path
sys.path.insert(0, '../infrastructure/lambda/cors_proxy')

from index import handler


def test_valid_request():
    """Test with a valid URL"""
    print("\n=== Test 1: Valid Request (Exchange Rate) ===")
    event = {
        'queryStringParameters': {
            'url': 'https://api.exchangerate-api.com/v4/latest/USD'
        }
    }
    
    response = handler(event, None)
    print(f"Status Code: {response['statusCode']}")
    print(f"Headers: {json.dumps(response['headers'], indent=2)}")
    
    # Check for caching headers
    if 'Cache-Control' in response['headers']:
        print(f"✅ Cache-Control: {response['headers']['Cache-Control']}")
    else:
        print("⚠️  Warning: Cache-Control header not found")
    
    if response['statusCode'] == 200:
        body = json.loads(response['body'])
        if 'rates' in body and 'HUF' in body['rates']:
            print(f"✅ SUCCESS - HUF Rate: {body['rates']['HUF']}")
        else:
            print(f"❌ FAILED - Unexpected response: {body}")
    else:
        print(f"❌ FAILED - {response['body']}")


def test_stock_price():
    """Test with Yahoo Finance stock price"""
    print("\n=== Test 2: Stock Price Request ===")
    event = {
        'queryStringParameters': {
            'url': 'https://query1.finance.yahoo.com/v8/finance/chart/EPAM'
        }
    }
    
    response = handler(event, None)
    print(f"Status Code: {response['statusCode']}")
    
    if response['statusCode'] == 200:
        body = json.loads(response['body'])
        if 'chart' in body and 'result' in body['chart']:
            price = body['chart']['result'][0]['meta']['regularMarketPrice']
            print(f"✅ SUCCESS - EPAM Price: ${price}")
        else:
            print(f"❌ FAILED - Unexpected response structure")
    else:
        print(f"❌ FAILED - {response['body']}")


def test_missing_url():
    """Test with missing URL parameter"""
    print("\n=== Test 3: Missing URL Parameter ===")
    event = {
        'queryStringParameters': {}
    }
    
    response = handler(event, None)
    print(f"Status Code: {response['statusCode']}")
    
    if response['statusCode'] == 400:
        print("✅ SUCCESS - Correctly returns 400 for missing URL")
    else:
        print(f"❌ FAILED - Expected 400, got {response['statusCode']}")


def test_invalid_url():
    """Test with invalid URL"""
    print("\n=== Test 4: Invalid URL ===")
    event = {
        'queryStringParameters': {
            'url': 'https://invalid-domain-that-does-not-exist-12345.com/api'
        }
    }
    
    response = handler(event, None)
    print(f"Status Code: {response['statusCode']}")
    
    if response['statusCode'] >= 400:
        print("✅ SUCCESS - Correctly returns error for invalid URL")
    else:
        print(f"❌ FAILED - Expected error status, got {response['statusCode']}")


if __name__ == '__main__':
    print("🧪 Testing Lambda CORS Proxy Handler Locally")
    print("=" * 60)
    
    try:
        test_valid_request()
        test_stock_price()
        test_missing_url()
        test_invalid_url()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("\nTo deploy to AWS, run: python deploy.py")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
