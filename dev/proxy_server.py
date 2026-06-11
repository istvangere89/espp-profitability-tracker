"""
Simple CORS proxy server for stock tracker app
Runs on port 8080 and proxies API requests

Caching Strategy:
- Returns Cache-Control: public, max-age=3600 (1 hour)
- Browsers cache responses to reduce proxy requests
- Reduces load on external APIs during development
- Mirrors production Lambda caching behavior
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.parse
import json

class CORSProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameter
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        if 'url' not in query_params:
            self.send_error(400, 'Missing url parameter')
            return
        
        target_url = query_params['url'][0]
        
        try:
            # Make request to target URL
            req = urllib.request.Request(
                target_url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                
                # Send response with CORS headers
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', '*')
                self.send_header('Cache-Control', 'public, max-age=3600')  # Cache for 1 hour
                self.end_headers()
                
                self.wfile.write(content)
                
        except Exception as e:
            print(f'Error proxying request: {e}')
            self.send_error(500, f'Error: {str(e)}')
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Custom logging
        print(f'[Proxy] {args[0]}')

if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, CORSProxyHandler)
    print('🚀 CORS Proxy Server running on http://localhost:8080')
    print('Usage: http://localhost:8080?url=<encoded_url>')
    print('Press Ctrl+C to stop')
    httpd.serve_forever()
