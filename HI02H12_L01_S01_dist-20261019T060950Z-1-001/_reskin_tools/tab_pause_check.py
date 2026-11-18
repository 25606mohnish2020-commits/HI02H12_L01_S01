"""[tab-pause] (2026-11-18) the lesson stands still while its tab is hidden and goes on from the same moment when it is seen again.
usage: python -I -X utf8 tab_pause_check.py <index.html> [--headed]
Chrome is driven over its own DevTools protocol (no Playwright: Playwright keeps every page "visible"), so opening a second tab
REALLY hides the lesson's tab (visibilityState "hidden", no frames, timers throttled) as a child's browser does.
A. the welcome: hidden 2 s into it for 6 s - its clock stands (within 0.05 s), the page's clock gains < 0.1 s, no timer fires (a probe
   interval), the CSS animations stand (their currentTime), nothing new starts (no flight, no button); seen again: the same clip plays on
   from where it stood (no new clip, the engine's isPlaying never dropped, no "ended", no stuck-clip report), the page's clock goes on.
B. the symbols' flight: hidden mid-flight for 5 s - the danda's flight animation and its glyph copy stand at the same progress, the
   landing does not happen; seen again: they go on from there; the । lands at the planned moment ON THE PAGE'S CLOCK (3.25 s after the
   flight's start, as in a run that is never hidden), the badge pops, the commas land, the button comes - the whole sequence on the
   page's clock within 0.3 s of a run never hidden (C).
C. the same run never hidden (the reference timings).
D. a lesson page with its voice and the music bed (T1): hidden for 5 s while the example line speaks - the line's clock, the music's
   clock and the lit word stand; the Web Audio context (if any) is suspended; seen again, all go on; the page completes as normal.
E. opened in a background tab (hidden from the start): nothing plays and no timer runs until it is seen; then the welcome starts.
F. no page errors anywhere."""
import sys, json, time, subprocess, tempfile, pathlib, itertools, urllib.request
import websocket

HTML = pathlib.Path(sys.argv[1]).resolve(); HEADED = "--headed" in sys.argv
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not pathlib.Path(CHROME).exists(): CHROME = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {str(detail)[:500]}" if detail != "" else ""), flush=True)
    if not ok: fails.append(name)

class Chrome:
    def __init__(self, port):
        self.port = port; self.ud = tempfile.mkdtemp(prefix="tabpause_")
        args = [CHROME, f"--remote-debugging-port={port}", f"--user-data-dir={self.ud}", "--no-first-run", "--no-default-browser-check",
                "--remote-allow-origins=*", "--autoplay-policy=no-user-gesture-required", "--mute-audio", "--window-size=1333,750", "about:blank"]
        if not HEADED: args.insert(1, "--headless=new")
        self.proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(150):
            try: urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1); break
            except Exception: time.sleep(0.2)
    def tabs(self): return [t for t in json.load(urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json/list")) if t["type"] == "page"]
    def new_tab(self, url="about:blank"):
        return json.load(urllib.request.urlopen(urllib.request.Request(f"http://127.0.0.1:{self.port}/json/new?{url}", method="PUT")))
    def activate(self, tid): urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json/activate/{tid}")
    def close_tab(self, tid): urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json/close/{tid}")
    def close(self):
        try: self.proc.terminate(); self.proc.wait(10)
        except Exception: pass

class Tab:
    def __init__(self, info):
        self.id = info["id"]; self.ws = websocket.create_connection(info["webSocketDebuggerUrl"], timeout=120); self.n = itertools.count(1); self.errors = []
    def send(self, method, params=None):
        i = next(self.n); self.ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("method") == "Runtime.exceptionThrown": self.errors.append(m["params"]["exceptionDetails"].get("exception", {}).get("description", "?")[:200])
            if m.get("id") == i:
                if "error" in m: raise RuntimeError(f"{method}: {m['error']}")
                return m.get("result", {})
    def ev(self, expr):
        r = self.send("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        if "exceptionDetails" in r: raise RuntimeError(json.dumps(r["exceptionDetails"])[:400])
        return r["result"].get("value")
    def wait(self, expr, timeout=60, step=0.05):
        t0 = time.time()
        while time.time() - t0 < timeout:
            try:
                if self.ev(expr): return True
            except Exception: pass
            time.sleep(step)
        return False
    def goto(self, url):
        self.send("Page.enable"); self.send("Runtime.enable"); self.send("Page.navigate", {"url": url})
        self.wait("document.readyState === 'complete'", 30)

LEAVE = """(() => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded'); const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); return 1; })()"""
# a probe: a 100 ms interval through the page's own timers, the media events the engine would see, the stuck-clip reports
PROBE = """(() => { window.__pt = { tick: 0, ended: 0, stuck: 0, plays: [] };
  setInterval(() => window.__pt.tick++, 100);
  window.addEventListener('plmediastuck', () => window.__pt.stuck++);
  const op = HTMLMediaElement.prototype.play; HTMLMediaElement.prototype.play = function(){ window.__pt.plays.push([(this.src || '').split('/').pop().split('?')[0], performance.now()]); return op.apply(this, arguments); };
  return 1; })()"""
CSSANIM = """(() => { const a = document.getAnimations().filter(x => typeof CSSAnimation !== 'undefined' && x instanceof CSSAnimation && x.playState === 'running').slice(0, 8);
  window.__pa = a; return a.map(x => x.currentTime); })()"""
CSSANIM_AGAIN = "(window.__pa || []).map(x => x.currentTime)"
VO = """(() => { const a = (typeof currentAudio !== 'undefined') ? currentAudio : null;
  return { src: a ? (a.src || '').split('/').pop().split('?')[0] : null, t: a ? a.currentTime : null, paused: a ? a.paused : null, playing: isPlaying,
           now: performance.now(), tick: window.__pt ? window.__pt.tick : null, vis: document.visibilityState, sp: window.__sgPause ? { h: __sgPause.hidden, total: __sgPause.total, n: __sgPause.count } : null,
           fly: window.__sgFly ? __sgFly.phase : null, ready: document.getElementById('sgBtn').classList.contains('ready') }; })()"""

def sequence_marks(tab):
    return tab.ev("""(() => { const f = window.__sgFly; if (!f) return null; return { t0: f.t0, fl: (f.flights || []).map(x => [x.name, x.start]), shown: (f.shown || []).map(x => [x.ch, x.at]),
      golds: (f.golds || []).map(g => [g.kind, g.at]), doneAt: f.doneAt || null }; })()""")

def run_cover(c, hide_at=None, hide_s=6.0):
    """the cover from load to the button; hide_at: 'welcome' (2 s into the line) or 'flight' (1.5 s into it) or None"""
    tab = Tab(c.tabs()[0]); tab.goto(HTML.as_uri()); tab.ev(PROBE)
    res = {}
    if hide_at == "welcome":
        tab.wait("(() => { const a = typeof currentAudio !== 'undefined' ? currentAudio : null; return !!(a && /vo_landing/.test(a.src) && !a.paused && a.currentTime > 2); })()", 40)
    elif hide_at == "flight":
        tab.wait("window.__sgFly && __sgFly.flights && __sgFly.flights.length > 0 && performance.now() > __sgFly.flights[0].start + 1500", 60)
    if hide_at:
        tab.ev(CSSANIM)
        res["before"] = tab.ev(VO); res["css0"] = tab.ev(CSSANIM_AGAIN)
        res["fa0"] = tab.ev("(() => { const e = document.querySelector('.sgf-purn'); const a = e && e.getAnimations()[0]; return a ? a.effect.getComputedTiming().progress : null; })()")
        other = c.new_tab("about:blank"); time.sleep(0.4)
        res["hidden"] = tab.ev(VO); res["cssh"] = tab.ev(CSSANIM_AGAIN)
        res["fah"] = tab.ev("(() => { const e = document.querySelector('.sgf-purn'); const a = e && e.getAnimations()[0]; return a ? a.effect.getComputedTiming().progress : null; })()")
        time.sleep(hide_s)
        res["late"] = tab.ev(VO); res["css1"] = tab.ev(CSSANIM_AGAIN)
        res["fa1"] = tab.ev("(() => { const e = document.querySelector('.sgf-purn'); const a = e && e.getAnimations()[0]; return a ? a.effect.getComputedTiming().progress : null; })()")
        res["marks_hidden"] = sequence_marks(tab)
        c.activate(tab.id); time.sleep(0.6)
        res["after"] = tab.ev(VO); res["css2"] = tab.ev(CSSANIM_AGAIN)
        try: c.close_tab(other["id"])
        except Exception: pass
    tab.wait("document.getElementById('sgBtn').classList.contains('ready')", 90)
    time.sleep(0.5)
    res["marks"] = sequence_marks(tab); res["pt"] = tab.ev("window.__pt"); res["end"] = tab.ev(VO); res["errors"] = tab.errors[:]
    tab.ws.close(); return res

def rel(m):   # the sequence on the page's clock, from the flight's start: । landing, comma landing, the two pops, done
    if not m or not m["fl"]: return None
    s0 = m["t0"]; sh = {}
    for ch, at in m["shown"]: sh.setdefault(ch, at)
    g = {k: at for k, at in m["golds"]}
    return {"danda": round(sh.get("।", 0) - s0), "comma": round(sh.get(",", 0) - s0), "pop_blue": round(g.get("blue", 0) - s0), "pop_green": round(g.get("green", 0) - s0),
            "done": round((m["doneAt"] or 0) - s0)}

port = itertools.count(9341)
# ---- C. never hidden (the reference) ----
c = Chrome(next(port))
try: C = run_cover(c, None)
finally: c.close()
refc = rel(C["marks"]); print("reference (never hidden):", refc)
# ---- A. hidden in the welcome ----
c = Chrome(next(port))
try: A = run_cover(c, "welcome", 6.0)
finally: c.close()
b, h, l, a = A["before"], A["hidden"], A["late"], A["after"]
check("A. another tab opened: the lesson's tab is hidden and the pause is on", h["vis"] == "hidden" and h["sp"]["h"] is True and h["sp"]["n"] == 1, (h["vis"], h["sp"]))
check("A. ...6 s hidden: the welcome stands where it was (its clock within 0.05 s), paused, still the engine's current clip, isPlaying kept",
      l["src"] == b["src"] == "vo_landing.ogg" and abs(l["t"] - h["t"]) < 0.05 and l["paused"] and l["playing"], (b["t"], h["t"], l["t"], l["paused"], l["playing"]))
check("A. ...the page's clock stood still (< 0.1 s gained in 6 s) and no timer fired (the probe interval did not tick)", l["now"] - h["now"] < 100 and l["tick"] == h["tick"], (round(l["now"] - h["now"]), h["tick"], l["tick"]))
check("A. ...the CSS animations stood (each one's currentTime unchanged), nothing new started (no flight, no button)",
      A["css1"] and A["css1"] == A["cssh"] and l["fly"] == "wait" and not l["ready"], (len(A["cssh"] or []), A["css1"] == A["cssh"], l["fly"], l["ready"]))
check("A. seen again: the pause is off, the same clip plays on from where it stood, the CSS animations and the timers go on",
      a["vis"] == "visible" and not a["sp"]["h"] and a["src"] == "vo_landing.ogg" and not a["paused"] and a["t"] > l["t"] and a["t"] - l["t"] < 0.9 and a["tick"] > l["tick"]
      and A["css2"] and all(x2 > x1 for x1, x2 in zip(A["css1"], A["css2"]) if x1 is not None and x2 is not None), (a["vis"], a["src"], a["paused"], round(a["t"] - l["t"], 3), a["tick"] - l["tick"]))
pa = A["pt"]
check("A. ...the engine saw nothing: one welcome play() in all, no stuck-clip report, the button came after the flight + sparkle as ever",
      [x[0] for x in pa["plays"]].count("vo_landing.ogg") == 1 and pa["stuck"] == 0 and A["end"]["ready"], ([x[0] for x in pa["plays"]], pa["stuck"]))
refa = rel(A["marks"])
check("A. ...the whole sequence after it is the never-hidden run's on the page's clock (each mark within 300 ms)",
      refa and refc and all(abs(refa[k] - refc[k]) <= 300 for k in refc), (refa, refc))
check("A. no page errors", not A["errors"], A["errors"][:3])
# ---- B. hidden mid-flight ----
c = Chrome(next(port))
try: B = run_cover(c, "flight", 5.0)
finally: c.close()
check("B. hidden 1.5 s into the flight for 5 s: the danda's flight stands at the same progress, nothing lands, no pop",
      B["fah"] is not None and B["fa1"] is not None and B["fa1"] == B["fah"] and B["late"]["fly"] in ("blue", "green")
      and not any(ch == "।" for ch, _ in (B["marks_hidden"]["shown"] or [])) and not (B["marks_hidden"]["golds"] or []), (B["fa0"], B["fah"], B["fa1"], B["late"]["fly"], B["marks_hidden"]["shown"]))
refb = rel(B["marks"])
check("B. seen again: the flight goes on from there - the । lands, its pop, the commas, their pop + shine, the button: all at the never-hidden run's moments on the page's clock (300 ms)",
      refb and refc and all(abs(refb[k] - refc[k]) <= 300 for k in refc) and B["end"]["ready"], (refb, refc))
check("B. ...one badge play per landing, no stuck-clip report; no page errors", [x[0] for x in B["pt"]["plays"]].count("sfx_title_badge.ogg") == 2 and B["pt"]["stuck"] == 0 and not B["errors"],
      ([x[0] for x in B["pt"]["plays"]], B["pt"]["stuck"], B["errors"][:2]))
# ---- D. a lesson page: T1, its example line and the music bed ----
c = Chrome(next(port))
try:
    tab = Tab(c.tabs()[0]); tab.goto(HTML.as_uri()); tab.ev(PROBE); time.sleep(1.5); tab.ev(LEAVE)
    tab.ev("mountSlide(CARD.slides.findIndex(s => s.id === 'T1'))")
    ok = tab.wait("(() => { const a = typeof currentAudio !== 'undefined' ? currentAudio : null; return !!(a && /vo_recap_purn_eg/.test(a.src) && !a.paused && a.currentTime > 1.0); })()", 60)
    LINE = """(() => { const a = currentAudio, m = window.__bgm && __bgm.el; return { src: (a.src || '').split('/').pop().split('?')[0], t: a.currentTime, paused: a.paused,
      bgm: m ? [m.currentTime, m.paused] : null, lit: [...document.querySelectorAll('#slideHost .on, #slideHost .hot')].map(e => e.textContent).join('|'),
      ac: (() => { try { return [...(window.__acs || [])].map(x => x.state); } catch(e){ return null; } })(), now: performance.now(), tick: __pt.tick }; })()"""
    d0 = tab.ev(LINE); other = c.new_tab("about:blank"); time.sleep(0.4); d1 = tab.ev(LINE); time.sleep(5); d2 = tab.ev(LINE)
    c.activate(tab.id); time.sleep(0.8); d3 = tab.ev(LINE)
    check("D. T1's example line speaking (the user's new take), the music bed on", ok and d0["src"] == "vo_recap_purn_eg.ogg" and d0["bgm"] and not d0["bgm"][1], (ok, d0))
    check("D. hidden 5 s: the line's clock and the music's clock stand, both paused, the lit word stays the same, no timer fires",
          abs(d2["t"] - d1["t"]) < 0.05 and d2["paused"] and abs(d2["bgm"][0] - d1["bgm"][0]) < 0.05 and d2["bgm"][1] and d2["lit"] == d1["lit"] and d2["tick"] == d1["tick"],
          (round(d2["t"] - d1["t"], 3), d2["paused"], d2["bgm"], d1["lit"], d2["lit"], d2["tick"] - d1["tick"]))
    check("D. seen again: the line and the music play on from where they stood, timers go on",
          not d3["paused"] and d3["t"] > d2["t"] and d3["t"] - d2["t"] < 1.2 and d3["bgm"] and not d3["bgm"][1] and d3["bgm"][0] > d2["bgm"][0] and d3["tick"] > d2["tick"],
          (round(d3["t"] - d2["t"], 3), d3["bgm"], d3["tick"] - d2["tick"]))
    done = tab.wait("state.idx !== CARD.slides.findIndex(s => s.id === 'T1') || !!document.querySelector('#navBtn.ready, #navBtn:not([disabled])')", 60)
    check("D. ...and the page goes on to its end as normal (आगे ready or the next page)", done)
    check("D. no page errors", not tab.errors, tab.errors[:3])
    tab.ws.close()
finally:
    c.close()
# ---- E. opened in a background tab ----
c = Chrome(next(port))
try:
    front = c.tabs()[0]; bg = c.new_tab("about:blank"); time.sleep(0.3)
    tab = Tab(bg); tab.send("Page.enable"); tab.send("Runtime.enable")
    c.activate(front["id"]); time.sleep(0.3)
    tab.send("Page.navigate", {"url": HTML.as_uri()}); tab.wait("document.readyState === 'complete'", 30); tab.ev(PROBE); time.sleep(6)
    e1 = tab.ev(VO)
    check("E. a lesson opened in a background tab stays still: hidden from the start, nothing plays (no welcome), no timer runs",
          e1["vis"] == "hidden" and e1["sp"]["h"] and (e1["src"] is None or e1["paused"] or e1["t"] in (0, None)) and e1["tick"] == 0 and e1["fly"] == "wait",
          e1)
    c.activate(tab.id); started = tab.wait("(() => { const a = typeof currentAudio !== 'undefined' ? currentAudio : null; return !!(a && /vo_landing/.test(a.src) && !a.paused && a.currentTime > 0.3); })()", 30)
    e2 = tab.ev(VO)
    check("E. ...seen: it starts (the welcome plays, timers run)", started and e2["tick"] > 0, e2)
    check("E. no page errors", not tab.errors, tab.errors[:3])
    tab.ws.close()
finally:
    c.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
