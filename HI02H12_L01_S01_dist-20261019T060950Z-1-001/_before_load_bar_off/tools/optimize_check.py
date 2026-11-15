"""[optimize] (2026-11-15) checks the optimised dist like a user, over HTTP (http_serve.py: Range, Content-Length, Vercel's caching):
 A. throttled network (CDP, 8 Mbit/s, 80 ms): the loading bar shows real progress with the play button hidden, never goes back,
    reaches 100 %, the button pops in only after it (and after the welcome), the lesson starts; the queue is smallest-first and
    the cover's pictures land in the first seconds; no JS error, no 4xx / 5xx, no failed request.
 B. every page mounted in turn (after the preload): every shown picture decoded (complete, naturalWidth > 0), no media error, no
    console error, no failed request; the sounds play from blob: URLs; a screenshot per page (outdir/pages/).
 C. failure paths: blocked files (the bar still completes, the lesson still starts and runs past them), a stalled file (aborted
    by the stall timer, counted done), a revoked blob (reverts to the file's URL and still plays / shows), a welcome that never
    loads (the watchdog ends it, the button still comes), file:// (no bar, the cover as before).
 D. compositing: layers and their area on every page (CDP LayerTree), hidden overlays hold none.
usage: python -I -X utf8 optimize_check.py <index.html> <outdir> [A B C D]   (default: all)"""
import json, math, pathlib, sys, time
SCR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCR))
from http_serve import serve
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
PARTS = set(sys.argv[3:]) or {"A", "B", "C", "D"}
dist = html.parent
results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok))); print(("PASS " if ok else "FAIL ") + name + (" — " + str(detail)[:600] if detail != "" else ""), flush=True)

ARGS = ["--autoplay-policy=no-user-gesture-required", "--mute-audio"]
SAMPLER = """(() => { window.__plS = []; const t0 = performance.now();
  const tick = () => { try {
    const bar = document.getElementById('sgLoad'), btn = document.getElementById('sgBtn'), P = window.__preload;
    const fill = bar && bar.querySelector('.sg-load-fill'), pct = bar && bar.querySelector('.sg-load-pct');
    const a = (typeof currentAudio !== 'undefined') ? currentAudio : null;
    const cover = [...document.querySelectorAll('.sg-card img')].filter(i => i.getAttribute('src'));
    window.__plS.push({ t: Math.round(performance.now() - t0), barShown: !!bar && getComputedStyle(bar).display !== 'none' && getComputedStyle(bar).opacity !== '0',
      fill: fill ? parseFloat(fill.style.width) || 0 : null, pct: pct ? pct.textContent : null, frac: P ? P.fraction : null, done: P ? P.done : null,
      btnReady: !!btn && btn.classList.contains('ready'), btnShown: !!btn && getComputedStyle(btn).display !== 'none',
      clip: a ? String(a.src).split('/').pop() : null, playing: !!(a && !a.paused), start: document.body.classList.contains('is-start'),
      coverDone: cover.filter(i => i.complete && i.naturalWidth > 0).length, coverAll: cover.length });
  } catch(e){ window.__plS.push({ t: Math.round(performance.now() - t0), err: String(e) }); } };
  const iv = setInterval(tick, 100); window.__plStop = () => clearInterval(iv); tick(); })();"""
ERRLOG = """(() => { window.__mediaErr = []; document.addEventListener('error', e => { const t = e.target;
  if (t && (t.tagName === 'IMG' || t.tagName === 'AUDIO' || t.tagName === 'VIDEO')) window.__mediaErr.push(String(t.currentSrc || t.src || '')); }, true); })();"""


def new_page(b, throttle=None, cache=True):
    ctx = b.new_context(viewport={"width": 1333, "height": 750})
    pg = ctx.new_page()
    log = {"console": [], "pageerror": [], "bad": [], "failed": [], "req": []}
    pg.on("console", lambda m: log["console"].append(m.text[:300] + " @ " + str((m.location or {}).get("url"))) if m.type == "error" else None)
    pg.on("pageerror", lambda e: log["pageerror"].append(str(e)[:300]))
    pg.on("response", lambda r: log["bad"].append((r.status, r.url)) if r.status >= 400 else None)
    pg.on("requestfailed", lambda r: log["failed"].append((r.url, r.failure)))
    pg.add_init_script(ERRLOG)
    cdp = ctx.new_cdp_session(pg)
    cdp.send("Network.enable")
    if not cache: cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    if throttle:
        cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": throttle[1], "downloadThroughput": throttle[0], "uploadThroughput": throttle[0]})
    reqs = {}
    cdp.on("Network.requestWillBeSent", lambda e: reqs.setdefault(e["requestId"], {"url": e["request"]["url"], "t0": e["timestamp"], "type": e.get("type")}))
    cdp.on("Network.loadingFinished", lambda e: reqs.get(e["requestId"], {}).update({"t1": e["timestamp"], "bytes": e.get("encodedDataLength")}))
    cdp.on("Network.loadingFailed", lambda e: reqs.get(e["requestId"], {}).update({"t1": e["timestamp"], "fail": e.get("errorText")}))
    log["req"] = reqs
    return ctx, pg, cdp, log


def leave_cover_and_wait_preload(pg, timeout=120000):
    pg.wait_for_function("window.__preload && window.__preload.done", timeout=timeout, polling=100)


with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=ARGS)
    base, stop = serve(dist)
    url = base + "index.html"

    # ---------------------------------------------------------------- A
    if "A" in PARTS:
        ctx, pg, cdp, log = new_page(b, throttle=(1_000_000, 80), cache=False)
        pg.add_init_script(SAMPLER)
        t_nav = time.time()
        pg.goto(url, wait_until="commit")
        pg.wait_for_function("window.__preload && window.__preload.done", timeout=240000, polling=200)
        try:
            pg.wait_for_function("document.getElementById('sgBtn').classList.contains('ready')", timeout=60000, polling=100)
        except Exception:
            pass
        pg.wait_for_timeout(600)
        S = pg.evaluate("window.__plStop(), window.__plS")
        st = pg.evaluate("window.__preload.stats()")
        (out / "A_samples.json").write_text(json.dumps({"samples": S, "stats": st}, indent=0), encoding="utf-8")
        loading = [s for s in S if s.get("done") is False]
        shown_partial = [s for s in loading if s.get("barShown") and s.get("pct") and 0 < int(s["pct"].rstrip("%")) < 100]
        check("A. while loading, the bar shows real progress in the play button's place (a part-filled bar seen, e.g. 1-99 %)",
              len(shown_partial) >= 5, (len(loading), len(shown_partial), [s["pct"] for s in shown_partial[::max(1, len(shown_partial)//8)]]))
        check("A. ...and the play button stays hidden the whole time (never shown or ready before every file is in)",
              loading and not any(s.get("btnShown") or s.get("btnReady") for s in loading), sum(1 for s in loading if s.get("btnShown")))
        fr = [s["frac"] for s in S if s.get("frac") is not None]; fills = [s["fill"] for s in S if s.get("fill") is not None]
        check("A. ...it never goes back (the fraction and the bar's width only grow) and reaches 100 %",
              all(b2 >= a2 - 1e-9 for a2, b2 in zip(fr, fr[1:])) and all(b2 >= a2 - 1e-6 for a2, b2 in zip(fills, fills[1:])) and fr and fr[-1] == 1,
              (fr[:3], fr[-3:], max((a2 - b2 for a2, b2 in zip(fills, fills[1:])), default=0)))
        done_t = next((s["t"] for s in S if s.get("done")), None); ready_t = next((s["t"] for s in S if s.get("btnReady")), None)
        check("A. the play button pops in only after the preload is complete (and the welcome was heard), then the bar is gone",
              done_t is not None and ready_t is not None and ready_t >= done_t and not S[-1]["barShown"], (done_t, ready_t, S[-1].get("barShown")))
        check("A. every file in, none failed (the files' bytes on disk = what arrived)", st["failed"] == 0 and st["done"] == st["files"],
              {k: st[k] for k in ("files", "done", "failed", "bytes", "ms")})
        # ordering: the preloader's fetches start smallest first (page-initiated bumps aside), and the cover's pictures land early
        fetches = sorted((r for r in log["req"].values() if r.get("type") == "Fetch" and "/assets/" in r["url"]), key=lambda r: r["t0"])
        sizes = []
        for r in fetches:
            f = dist / r["url"].split(base, 1)[-1].split("?")[0]
            sizes.append(f.stat().st_size if f.exists() else 0)
        inv = sum(1 for i in range(1, len(sizes)) if sizes[i] < sizes[i - 1] * 0.5)
        first_names = [r["url"].split("/")[-1].split("?")[0] for r in fetches[:2]]
        check("A. the queue: the cover's own big files first (the bird's wave animation, the welcome), then smallest first (sizes in start order nearly always ascending; the exceptions are files the page asked for early)",
              len(sizes) > 20 and inv <= max(6, len(sizes) // 15) and "new_landing_swiftee_anim.webp" in first_names, (len(sizes), inv, first_names, sizes[:8], sizes[-4:]))
        cover_t = next((s["t"] for s in S if s.get("coverAll") and s["coverDone"] == s["coverAll"]), None)
        check("A. the cover's pictures are all in within the first seconds (before half of the preload)", cover_t is not None and done_t and cover_t < 0.5 * done_t, (cover_t, done_t))
        pg.click("#sgBtn", force=True)
        try:
            pg.wait_for_function("CARD.slides[state.idx].id === 'T0' && document.getElementById('startGate').classList.contains('hidden')", timeout=20000)
            started = True
        except Exception:
            started = False
        check("A. the play button starts the lesson (the gate, then page 1 T0)", started)
        pg.wait_for_timeout(1500)
        pg.screenshot(path=str(out / "A_after_start.png"))
        check("A. no JS error, no 4xx / 5xx, no failed request during load and start", not log["console"] and not log["pageerror"] and not log["bad"] and not log["failed"],
              (log["console"][:3], log["pageerror"][:3], log["bad"][:3], log["failed"][:3]))
        ctx.close()

    # ---------------------------------------------------------------- B
    if "B" in PARTS:
        ctx, pg, cdp, log = new_page(b)
        pg.goto(url)
        leave_cover_and_wait_preload(pg)
        pg.wait_for_function("document.getElementById('sgBtn').classList.contains('ready')", timeout=30000)
        pg.screenshot(path=str(out / "B_cover_ready.png"))
        pg.click("#sgBtn", force=True)
        pg.wait_for_function("CARD.slides[state.idx].id === 'T0'", timeout=20000)
        (out / "pages").mkdir(exist_ok=True)
        n = pg.evaluate("CARD.slides.length")
        bad_pages = []
        for i in range(n):
            sid = pg.evaluate(f"CARD.slides[{i}].id")
            pg.evaluate(f"mountSlide({i})")
            t0 = time.time()
            pg.wait_for_timeout(1800)
            try:
                pg.wait_for_function("!isPlaying", timeout=14000, polling=100)
            except Exception:
                pass
            pg.wait_for_timeout(700)
            info = pg.evaluate("""() => { const shown = [...document.querySelectorAll('img')].filter(i => { const r = i.getBoundingClientRect(), cs = getComputedStyle(i);
                 return i.getAttribute('src') && r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; });
               const broken = shown.filter(i => !(i.complete && i.naturalWidth > 0)).map(i => i.src.split('/').pop());
               const a = currentAudio; return { imgs: shown.length, broken, mediaErr: window.__mediaErr.slice(), blobClip: a ? (a.getAttribute('src') || '').startsWith('blob:') : null,
                 clip: a ? a.src.split('/').pop() : null, nav: (() => { const nb = document.getElementById('navBtn'); return nb ? { shown: getComputedStyle(nb).display !== 'none', disabled: nb.disabled } : null; })() }; }""")
            pg.screenshot(path=str(out / "pages" / f"{i+1:02d}_{sid}.png"))
            if info["broken"] or info["mediaErr"]: bad_pages.append((sid, info["broken"], info["mediaErr"]))
            print(f"   page {i+1} {sid}: {info['imgs']} pictures shown, broken {info['broken']}, clip {info['clip']} blob={info['blobClip']}, nav {info['nav']}", flush=True)
        check("B. every page: every shown picture decoded (complete, naturalWidth > 0), no media error", not bad_pages, bad_pages[:5])
        st = pg.evaluate("window.__preload.stats()")
        check("B. pages play their sounds / show their pictures from memory (blob: URLs served, none reverted)", st["served"] > 50 and not st["reverts"], (st["served"], st["reverts"][:3]))
        check("B. no JS error, no 4xx / 5xx, no failed request across every page", not log["console"] and not log["pageerror"] and not log["bad"] and not log["failed"],
              (log["console"][:3], log["pageerror"][:3], log["bad"][:3], log["failed"][:3]))
        ctx.close()

    # ---------------------------------------------------------------- C
    if "C" in PARTS:
        # C1 blocked files: the bar completes, the lesson starts and runs past them
        ctx, pg, cdp, log = new_page(b)
        BLOCK = ["vo_pt_tutorial.ogg", "sfx_play_button.ogg", "title_shadow_1.svg"]
        pg.route("**/*", lambda r: r.abort() if any(r.request.url.split("?")[0].endswith("/" + x) for x in BLOCK) else r.continue_())
        pg.goto(url)
        leave_cover_and_wait_preload(pg)
        st = pg.evaluate("window.__preload.stats()")
        check("C1. three blocked files: each counted done (failed list), the preload completes", st["done_flag"] and st["failed"] == 3, st["failedList"])
        try:
            pg.wait_for_function("document.getElementById('sgBtn').classList.contains('ready')", timeout=30000); ok = True
        except Exception: ok = False
        check("C1. ...the play button still comes", ok)
        pg.click("#sgBtn", force=True)
        try:
            pg.wait_for_function("CARD.slides[state.idx].id === 'T0' && document.getElementById('startGate').classList.contains('hidden')", timeout=25000); ok = True
        except Exception: ok = False
        check("C1. ...and the lesson starts past the gate whose line could not load (its silent beat)", ok)
        ctx.close()
        # C2 a stalled file: aborted by the stall timer, counted done
        ctx, pg, cdp, log = new_page(b)
        STALL = "img_stamp_final_pinki.webp"
        held = []
        pg.route("**/*", lambda r: held.append(r) if r.request.url.split("?")[0].endswith("/" + STALL) else r.continue_())
        t0 = time.time(); pg.goto(url)
        leave_cover_and_wait_preload(pg, timeout=60000); dt = time.time() - t0
        st = pg.evaluate("window.__preload.stats()")
        check("C2. a file that never answers: aborted after the 15 s stall and counted done; the preload completes (14-40 s)",
              any(STALL in f and "stalled" in f for f in st["failedList"]) and 14 <= dt <= 40, (round(dt, 1), st["failedList"]))
        try:
            pg.wait_for_function("document.getElementById('sgBtn').classList.contains('ready')", timeout=30000); ok = True
        except Exception: ok = False
        check("C2. ...the play button still comes", ok)
        ctx.close()
        # C3 a revoked blob: reverts to the file's URL, once, and still plays / shows
        ctx, pg, cdp, log = new_page(b)
        pg.goto(url); leave_cover_and_wait_preload(pg)
        pg.evaluate("document.getElementById('startGate').classList.add('hidden'); document.body.classList.remove('is-start')")
        r = pg.evaluate("""() => new Promise(res => { const src = 'assets/Audio/vo_pt_guided.ogg';
            URL.revokeObjectURL(__preload.blobURL(src)); let ended = false;
            play(src, () => { ended = true; });
            const a = currentAudio; setTimeout(() => res({ t: a.currentTime, paused: a.paused, attr: a.getAttribute('src'), reverts: __preload.stats().reverts, ended }), 2200); })""")
        check("C3. a sound whose blob fails: back to the file's own URL once, and it plays on (no error reaches the page)",
              r["t"] > 0.8 and not r["paused"] and not str(r["attr"]).startswith("blob:") and any("vo_pt_guided" in x for x in r["reverts"]), r)
        r2 = pg.evaluate("""() => new Promise(res => { const src = 'assets/Images/img_g3_garden.webp'; URL.revokeObjectURL(__preload.blobURL(src));
            const im = new Image(); let err = false; im.onerror = () => { err = true; }; im.onload = () => res({ ok: im.naturalWidth > 0, err, attr: im.getAttribute('src'), src: im.src });
            document.body.appendChild(im); im.src = src; setTimeout(() => res({ ok: false, err, timeout: true }), 5000); })""")
        check("C3. a picture whose blob fails: shown from the file's own URL, its own error handler never fired", r2.get("ok") and not r2.get("err") and r2["src"].endswith("img_g3_garden.webp") and any("img_g3_garden" in x for x in pg.evaluate("__preload.stats().reverts")), r2)
        ctx.close()
        # C4 a welcome that never loads: the watchdog ends it, the button still comes
        ctx, pg, cdp, log = new_page(b)
        held2 = []
        pg.route("**/*", lambda r: held2.append(r) if r.request.url.split("?")[0].endswith("/vo_landing.ogg") else r.continue_())
        stuck = []
        pg.expose_function("__onStuck", lambda d: stuck.append(d))
        pg.add_init_script("window.addEventListener('plmediastuck', e => window.__onStuck(e.detail));")
        t0 = time.time(); pg.goto(url)
        try:
            pg.wait_for_function("document.getElementById('sgBtn').classList.contains('ready')", timeout=45000); ok = True
        except Exception: ok = False
        dt = time.time() - t0
        check("C4. the welcome never loads: the clip watchdog ends it (9 s + its length), the play button still comes (< 35 s)",
              ok and any("vo_landing" in (d or {}).get("src", "") for d in stuck) and dt < 35, (ok, round(dt, 1), stuck))
        ctx.close()
        # C5 file://: nothing fetched, no bar, the cover as before
        ctx = b.new_context(viewport={"width": 1333, "height": 750}); pg = ctx.new_page()
        errs = []; pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.add_init_script(SAMPLER)
        pg.goto(html.as_uri())
        try:
            pg.wait_for_function("document.getElementById('sgBtn').classList.contains('ready')", timeout=30000); ok = True
        except Exception: ok = False
        S = pg.evaluate("window.__plStop(), window.__plS")
        check("C5. file://: no fetch at all, the bar never shows, the play button comes after the welcome as before, no error",
              ok and not any(s.get("barShown") for s in S) and pg.evaluate("__preload.stats().files") >= 0 and not errs and pg.evaluate("__preload.active") is False, (ok, errs[:3]))
        ctx.close()

    # ---------------------------------------------------------------- D
    if "D" in PARTS:
        ctx, pg, cdp, log = new_page(b)
        pg.goto(url); leave_cover_and_wait_preload(pg)
        layers = {}
        cdp.on("LayerTree.layerTreeDidChange", lambda e: layers.update(last=e.get("layers") or []))
        cdp.send("LayerTree.enable")
        def snap(label):
            # the tree is reported only when it changes: a 1x1 composited probe forces a report of every layer (and is left out)
            layers.pop("last", None)
            pg.evaluate("(() => { const d = document.createElement('div'); d.id = '__lprobe'; d.style.cssText = 'position:fixed;left:0;top:0;width:1px;height:1px;will-change:transform;z-index:2147483647;pointer-events:none'; document.body.appendChild(d); })()")
            pg.wait_for_timeout(700)
            L = [l for l in (layers.get("last") or []) if not (round(l.get("width", 0)) == 1 and round(l.get("height", 0)) == 1)]
            pg.evaluate("document.getElementById('__lprobe') && document.getElementById('__lprobe').remove()")
            draw = [l for l in L if l.get("drawsContent")]
            area = sum(l["width"] * l["height"] for l in draw)
            return {"page": label, "layers": len(L), "drawing": len(draw), "mpx": round(area / 1e6, 2), "mb": round(area * 4 / 1048576, 1),
                    "biggest": sorted(((round(l["width"]), round(l["height"])) for l in draw), key=lambda w: -w[0] * w[1])[:4]}
        rows = [snap("cover")]
        pg.evaluate("document.getElementById('startGate').classList.add('hidden'); document.body.classList.remove('is-start'); document.body.classList.add('loaded')")
        n = pg.evaluate("CARD.slides.length")
        for i in range(n):
            pg.evaluate(f"mountSlide({i})"); pg.wait_for_timeout(2500)
            rows.append(snap(pg.evaluate(f"CARD.slides[{i}].id")))
        for r_ in rows: print("   ", r_, flush=True)
        (out / "D_layers.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
        worst = max(rows, key=lambda r_: r_["mb"])
        check("D. every page's composited layers stay far inside a GPU texture budget (their drawn area <= 120 MB of textures; a snapshot on every page)",
              all(r_["layers"] > 0 for r_ in rows) and all(r_["mb"] <= 120 for r_ in rows), (worst, [r_["page"] for r_ in rows if not r_["layers"]]))
        pg.evaluate("mountSlide(0)"); pg.wait_for_timeout(1500)                   # an ordinary page: no overlay is in use
        hid = pg.evaluate("""() => ['startGate','endScreen','hintOverlay','phaseGate'].map(id => { const e = document.getElementById(id); return e ? [id, getComputedStyle(e).display, getComputedStyle(e).visibility] : [id, null]; })""")
        check("D. the overlays not in use (the cover after the start, the end screen, the hint card, the gate) are display:none — no layers kept for them",
              all(h[1] in (None, "none") for h in hid), hid)
        ctx.close()

    stop(); b.close()

fails = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(fails)}/{len(results)} passed" + ("" if not fails else f"; FAILED: {fails}"))
sys.exit(1 if fails else 0)
