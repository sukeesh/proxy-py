import http.server
import socketserver
import urllib.request
from urllib.parse import urlparse

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the requested URL
        parsed_url = urlparse(self.path)

        # Construct the new URL to forward the request to port 8000
        target_url = f"http://localhost:8000{parsed_url.path}"
        if parsed_url.query:
            target_url += f"?{parsed_url.query}"

        try:
            # Forward the request to port 8000 and get the response
            with urllib.request.urlopen(target_url) as response:
                self.send_response(response.getcode())
                for header, value in response.getheaders():
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except Exception as e:
            self.send_error(500, f"Proxy error: {str(e)}")

    def do_POST(self):
        # Parse the requested URL
        parsed_url = urlparse(self.path)

        # Construct the new URL to forward the request to port 8000
        target_url = f"http://localhost:8000{parsed_url.path}"
        if parsed_url.query:
            target_url += f"?{parsed_url.query}"

        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Forward the POST request to port 8000
            req = urllib.request.Request(target_url, data=post_data, method='POST')
            for header, value in self.headers.items():
                req.add_header(header, value)

            with urllib.request.urlopen(req) as response:
                self.send_response(response.getcode())
                for header, value in response.getheaders():
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
        except Exception as e:
            self.send_error(500, f"Proxy error: {str(e)}")

if __name__ == "__main__":
    PORT = 8118
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        print(f"Proxy server running on port {PORT}, forwarding to localhost:8000")
        httpd.serve_forever()
