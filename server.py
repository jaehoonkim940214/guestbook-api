from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

PORT = 8000
DATA_FILE = "data.json"

# 데이터 파일이 없으면 빈 리스트로 생성
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False)

class GuestbookHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if self.path == "/messages":
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)
            self._set_headers()
            self.wfile.write(json.dumps(messages, ensure_ascii=False).encode('utf-8'))

    def do_POST(self):
        if self.path == "/messages":
            content_len = int(self.headers["Content-Length"])
            post_body = self.rfile.read(content_len)
            new_message = json.loads(post_body.decode())

            with open(DATA_FILE, "r", encoding="utf-8") as f:
                messages = json.load(f)

            messages.append(new_message)

            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False)

            self._set_headers(201)
            self.wfile.write(json.dumps({"message": "Saved"}, ensure_ascii=False).encode('utf-8'))

httpd = HTTPServer(("", PORT), GuestbookHandler)
print(f"🚀 서버 실행 중: http://localhost:{PORT}")
httpd.serve_forever()