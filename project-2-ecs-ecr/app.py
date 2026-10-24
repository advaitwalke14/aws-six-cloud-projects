from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os, socket

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        payload = {
            "status": "ok",
            "service": "ecs-ecr-demo",
            "hostname": socket.gethostname(),
            "path": self.path
        }
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

HTTPServer(("0.0.0.0", int(os.getenv("PORT", "8080"))), Handler).serve_forever()
