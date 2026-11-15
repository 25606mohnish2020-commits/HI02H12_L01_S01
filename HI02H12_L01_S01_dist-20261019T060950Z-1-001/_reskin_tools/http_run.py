"""[optimize] (2026-11-15) run any of this folder's Playwright checks unchanged, but over HTTP: the dist is served by http_serve.py and
every file:// page load inside the dist is redirected to it, so the check exercises the online path (the preloader, the blob URLs,
the fetches). Optionally logs every request / failure / console error of every page to a JSON file.
    python -I -X utf8 http_run.py [--log <requests.json>] [--after-preload] [--settle <ms>] <check.py> <index.html> [check args...]
--after-preload: each page load waits until the preload is complete before the check goes on (as a child must: the play button
comes only then); leave it out for checks of the cover itself (title_check.py measures it from the first frame).
--settle <ms>: then waits that long too (the minutes a child spends before a later page, shortened).
Exit code = the check's own. Log format: [{"script": ..., "records": [{event, url, status|failed|text}, ...]}, ...] (appended)."""
import json, pathlib, runpy, sys, atexit

SCR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCR))
from http_serve import serve

args = sys.argv[1:]
log_path = None
after_preload = False
settle_ms = 0
while args and args[0] in ("--log", "--after-preload", "--settle"):
    if args[0] == "--log": log_path = pathlib.Path(args[1]); args = args[2:]
    elif args[0] == "--settle": settle_ms = int(args[1]); args = args[2:]
    else: after_preload = True; args = args[1:]
script, html = args[0], pathlib.Path(args[1]).resolve()
dist = html.parent
base_url, stop = serve(dist)
file_prefix = dist.as_uri().rstrip("/") + "/"
recs = []

from playwright.sync_api._generated import Browser, BrowserContext, Page

_goto = Page.goto
def goto(self, url, *a, **k):
    ours = isinstance(url, str) and url.startswith(file_prefix)
    if ours:
        url = base_url + url[len(file_prefix):]
    r = _goto(self, url, *a, **k)
    if ours and after_preload:   # a child reaches the pages only after the bar is full: so does the check (the cover's own checks don't wait)
        self.wait_for_function("!window.__preload || window.__preload.done", timeout=180000, polling=100)
        if settle_ms: self.wait_for_timeout(settle_ms)   # --settle: the minutes a child spends on the cover and the earlier pages, shortened
    return r
Page.goto = goto

def attach(page):
    if log_path is None: return page
    page.on("request", lambda r: recs.append({"event": "request", "url": r.url, "type": r.resource_type}))
    page.on("response", lambda r: recs.append({"event": "response", "url": r.url, "status": r.status}))
    page.on("requestfailed", lambda r: recs.append({"event": "failed", "url": r.url, "failed": r.failure}))
    page.on("console", lambda m: recs.append({"event": "console", "type": m.type, "text": m.text[:400]}) if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: recs.append({"event": "pageerror", "text": str(e)[:400]}))
    return page
_bnp = Browser.new_page
Browser.new_page = lambda self, *a, **k: attach(_bnp(self, *a, **k))
_cnp = BrowserContext.new_page
BrowserContext.new_page = lambda self, *a, **k: attach(_cnp(self, *a, **k))

def dump():
    if log_path is None: return
    old = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else []
    old.append({"script": " ".join([script] + args[1:]), "records": recs})
    log_path.write_text(json.dumps(old), encoding="utf-8")
atexit.register(dump)

sys.argv = [script] + [str(html)] + args[2:]
code = 0
try:
    runpy.run_path(str(SCR / script) if not pathlib.Path(script).is_absolute() else script, run_name="__main__")
except SystemExit as e:
    code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
stop()
sys.exit(code)
