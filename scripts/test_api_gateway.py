#!/usr/bin/env python3
"""
Test the deployed API Gateway endpoint
"""
import urllib.request
import urllib.parse
import json

# API Gateway URL
API_URL = "https://5m16c2qhoc.execute-api.eu-central-1.amazonaws.com/prod/"

def test_yahoo_finance():
    """Test Yahoo Finance API through Lambda proxy"""
    print("Testing Yahoo Finance API...")
    yahoo_url = "https://query1.finance.yahoo.com/v8/finance/chart/EPAM"
    proxy_url = f"{API_URL}?url={urllib.parse.quote(yahoo_url)}"
    
    print(f"Request URL: {proxy_url}")
    
    try:
        req = urllib.request.Request(proxy_url)
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            print(f"Status: {response.status}")
            print(f"Headers: {dict(response.headers)}")
            print(f"\nResponse (first 500 chars):")
            print(content[:500])
            
            # Try to parse as JSON
            try:
                data = json.loads(content)
                print(f"\n✅ Valid JSON response")
                print(f"Keys: {list(data.keys())}")
                if 'chart' in data:
                    print(f"Chart keys: {list(data['chart'].keys())}")
                    if 'result' in data['chart'] and data['chart']['result']:
                        print(f"Result keys: {list(data['chart']['result'][0].keys())}")
            except json.JSONDecodeError:
                print(f"\n❌ Response is not valid JSON")
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        error_body = e.read().decode('utf-8')
        print(f"Error body: {error_body}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_exchange_rate():
    """Test Exchange Rate API through Lambda proxy"""
    print("\n" + "="*60)
    print("Testing Exchange Rate API...")
    exchange_url = "https://api.exchangerate-api.com/v4/latest/USD"
    proxy_url = f"{API_URL}?url={urllib.parse.quote(exchange_url)}"
    
    print(f"Request URL: {proxy_url}")
    
    try:
        req = urllib.request.Request(proxy_url)
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            print(f"Status: {response.status}")
            print(f"Headers: {dict(response.headers)}")
            print(f"\nResponse (first 500 chars):")
            print(content[:500])
            
            # Try to parse as JSON
            try:
                data = json.loads(content)
                print(f"\n✅ Valid JSON response")
                print(f"Keys: {list(data.keys())}")
                if 'rates' in data:
                    print(f"Has 'rates' key")
                    if 'HUF' in data['rates']:
                        print(f"✅ HUF rate found: {data['rates']['HUF']}")
                    else:
                        print(f"❌ HUF not in rates. Available: {list(data['rates'].keys())[:10]}")
            except json.JSONDecodeError:
                print(f"\n❌ Response is not valid JSON")
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        error_body = e.read().decode('utf-8')
        print(f"Error body: {error_body}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("="*60)
    print("API Gateway Endpoint Test")
    print("="*60)
    test_yahoo_finance()
    test_exchange_rate()
    print("\n" + "="*60)
    print("Test complete!")
