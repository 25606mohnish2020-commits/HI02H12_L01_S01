"""[optimize] (2026-11-15) a local static server for the checks: serves a folder over HTTP with Content-Length, Range (206) and the
types a browser needs (Vercel serves all of these), on a free port, in a background thread.
    from http_serve import serve;  url, stop = serve(folder)      # url = "http://127.0.0.1:<port>/"
or alone:  python -I http_serve.py <folder> [port]"""
import http.server, os, pathlib, re, socketserver, threading, sys, urllib.parse

TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".json": "application/json", ".svg": "image/svg+xml", ".webp": "image/webp", ".png": "image/png", ".gif": "image/gif",
         ".jpg": "image/jpeg", ".ogg": "audio/ogg", ".mp3": "audio/mpeg", ".woff2": "font/woff2", ".webm": "video/webm"}


def make_handler(root):
    root = pathlib.Path(root).resolve()

    class H(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):
            pass

        def _file(self):
            path = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path).lstrip("/")
            p = (root / path).resolve()
            if root not in p.parents and p != root:
                return None
            if p.is_dir():
                p = p / "index.html"
            return p if p.is_file() else None

        def do_HEAD(self):
            self.do_GET(head=True)

        def do_GET(self, head=False):
            p = self._file()
            if p is None:
                body = b"not found"
                self.send_response(404); self.send_header("Content-Type", "text/plain"); self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if not head: self.wfile.write(body)
                return
            size = p.stat().st_size
            ctype = TYPES.get(p.suffix.lower(), "application/octet-stream")
            etag = '"%x-%x"' % (int(p.stat().st_mtime), size)
            inm = self.headers.get("If-None-Match")
            if inm and etag in [t.strip() for t in inm.split(",")]:   # a revalidation of an unchanged file: 304, as Vercel answers
                self.send_response(304); self.send_header("ETag", etag); self.send_header("Cache-Control", "public, max-age=0, must-revalidate"); self.end_headers(); return
            ims = self.headers.get("If-Modified-Since")
            if ims and not self.headers.get("Range"):
                try:
                    import email.utils
                    if int(p.stat().st_mtime) <= email.utils.parsedate_to_datetime(ims).timestamp():
                        self.send_response(304); self.send_header("Cache-Control", "public, max-age=0, must-revalidate"); self.end_headers(); return
                except Exception:
                    pass
            rng = self.headers.get("Range")
            start, end, status = 0, size - 1, 200
            m = re.match(r"bytes=(\d*)-(\d*)$", rng or "")
            if m and size:
                a, b = m.group(1), m.group(2)
                if a == "": start, end = max(0, size - int(b)), size - 1
                else: start, end = int(a), (int(b) if b else size - 1)
                end = min(end, size - 1)
                if start > end:
                    self.send_response(416); self.send_header("Content-Range", f"bytes */{size}"); self.send_header("Content-Length", "0"); self.end_headers(); return
                status = 206
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Cache-Control", "public, max-age=0, must-revalidate")   # what Vercel sends for static files
            self.send_header("Last-Modified", self.date_time_string(int(p.stat().st_mtime)))
            self.send_header("ETag", etag)
            if status == 206: self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(end - start + 1))
            self.end_headers()
            if head: return
            try:
                with open(p, "rb") as f:
                    f.seek(start); left = end - start + 1
                    while left > 0:
                        chunk = f.read(min(65536, left))
                        if not chunk: break
                        self.wfile.write(chunk); left -= len(chunk)
            except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
                pass
    return H


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        if isinstance(sys.exc_info()[1], (ConnectionAbortedError, ConnectionResetError, BrokenPipeError)):
            return                                   # the browser dropped a connection (an aborted media read): not an error
        super().handle_error(request, client_address)


def serve(folder, port=0):
    srv = Server(("127.0.0.1", port), make_handler(folder))
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return f"http://127.0.0.1:{srv.server_address[1]}/", srv.shutdown


if __name__ == "__main__":
    url, stop = serve(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8765)
    print("serving", sys.argv[1], "at", url, flush=True)
    threading.Event().wait()
