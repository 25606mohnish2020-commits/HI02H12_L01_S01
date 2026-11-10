"""[stamp-close] L2's finale beat by beat (2026-11-04): after the last round's confetti the letter page's envelope transition runs
BACKWARDS — the veil falls over the table and lifts off the sheet filling the screen, the view pulls back out of the envelope, the
sheet sinks, the flap comes down on L1's paper crackle, the seal comes back, the closed envelope shrinks into Pinki's raised hand as
the room of Figma 792:1253 comes into focus — then the gold glitter on her envelope ([stamp-final]'s), and the end screen.

The letter page's own opening is traced first (its tap -> its page change, and the stamp page's veil lifting) and the finale is judged
AGAINST IT: every property of the envelope (the box's scale, the flap's angle, the seal, the sheet's rise, its ruled lines, the
backdrop, both veils) must follow the forward curve read backwards, frame by frame, on the page's own clock (an rAF trace and a class
observer in the page; Playwright's lag never enters). Then the schedule, the landing in her hand (1x1 markers in the box), the sounds,
the pictures (the closed envelope as drawn, the last frame against Figma's render — each shot with the page's animations paused through
DevTools, in a run of its own), leaving mid-way, and the frames' smoothness (bare rAF times in fresh browsers, L1's opening alongside).

usage: python -I -X utf8 stamp_close_check.py <index.html> <outdir> [--quick]
  --quick: the traced run plays L2 with its last round only (868:74) — the finale is the same; by default it plays all five rounds,
  the stamps dropped as smoke.py drops them. The other runs always use the last round only. Exits 1 on any FAIL."""
import sys, re, math, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageFilter
import numpy as np

html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
QUICK = "--quick" in sys.argv[3:]
here = pathlib.Path(__file__).resolve().parent
RENDER = here / "stamp_assets" / "fig_792-1253_render.png"
IM = html.parent / "assets" / "Images"
fails = []
def check(name, ok, detail=""):
    ok = bool(ok); print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else "")); sys.stdout.flush()
    if not ok: fails.append(name)

LEAVE = """() => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); }"""
HOOK = """(() => { try{ performance.setResourceTimingBufferSize(5000); }catch(e){} window._plays = []; const P = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function(){ try{ window._plays.push({ src: String(this.src || '').split('/').pop().split('?')[0], t: performance.now(), el: this, vol: this.volume }); }catch(e){} return P.apply(this, arguments); }; })()"""
PLAYS = "() => window._plays.map(p => ({ src: p.src, t: p.t, vol: +(+p.vol).toFixed(3), paused: p.el.paused }))"
# every class change of the letter page's root, the stamp page's root and the finale's layer, with its moment (the observer runs in the
# task that made the change); completeSlide's moment too
OBS = """() => { window.__cls = []; const keep = (e) => e.classList && (e.classList.contains('ltr') || e.classList.contains('stp') || e.classList.contains('stp-close') || e.classList.contains('stp-veil'));
  new MutationObserver((ms) => { const t = performance.now(); for (const m of ms) { const e = m.target;
      if (m.type === 'childList') { m.addedNodes.forEach(n => { if (n.classList && n.classList.contains('stp-close')) window.__cls.push({ t, el: 'close', add: '(inserted)' }); }); continue; }
      if (!keep(e)) continue;
      const a = (m.oldValue || '').split(/\\s+/).filter(Boolean), b = e.className.split(/\\s+/).filter(Boolean),
            who = e.classList.contains('stp-close') ? 'close' : (e.classList.contains('stp-veil') ? 'veil' : (e.classList.contains('stp') ? 'stp' : 'ltr'));
      b.filter(x => !a.includes(x)).forEach(x => window.__cls.push({ t, el: who, add: x })); a.filter(x => !b.includes(x)).forEach(x => window.__cls.push({ t, el: who, rm: x })); } })
    .observe(document.body, { subtree: true, childList: true, attributes: true, attributeFilter: ['class'], attributeOldValue: true });
  const cs = completeSlide; completeSlide = function(){ window.__csT = (window.__csT || []).concat([performance.now()]); return cs.apply(this, arguments); }; }"""
# 1x1 markers at known box px (centred on the point): in the envelope's box (the drawing's envelope's centre, its heart, two corners,
# the mouth) and on the flap (its tip, its hinge) — they read the box's PROJECTED place (a rect of the box itself is its whole bounds)
MARK = """([sel, pts]) => { const r = document.querySelector(sel); if (!r) return false; const ep = r.querySelector('.ltr-env-pos'), fl = r.querySelector('.ltr-flap');
  for (const [host, c, x, y] of [[ep, 'mk-c', pts.c[0], pts.c[1]], [ep, 'mk-h', 602.36, 396.81], [ep, 'mk-tl', 127.44, 246.12], [ep, 'mk-tr', 938.45, 52.92], [ep, 'mk-mo', pts.mo[0], pts.mo[1]],
                                 [fl, 'mk-apex', 608.3, 468.3], [fl, 'mk-hinge', 538.6, 154.1]]) {
    if (host.querySelector('.' + c)) continue; const m = document.createElement('i'); m.className = c;
    m.style.cssText = 'position:absolute;left:' + (x - 0.5) + 'px;top:' + (y - 0.5) + 'px;width:1px;height:1px;pointer-events:none'; host.appendChild(m); }
  return true; }"""
# the page's own frames: the layer's classes and every moving property of the envelope, the veils, the markers, the glitter; each frame
# also stamps the document timeline's time (the time its animations were sampled at) and collects every new animation of the layers
# (CSS transitions and keyframe animations): their startTime is when each really began — the frame the style change was resolved in,
# which on a busy frame comes after the class change
TRACE = """(sel) => { window.__tr = []; window.__stop = false; const st = document.getElementById('stage');
  window.__aSeen = window.__aSeen || new WeakSet(); window.__aList = window.__aList || [];
  const q = (e) => { if (!e) return null; const b = st.getBoundingClientRect(), k = b.width / 1280, r = e.getBoundingClientRect(); return [(r.left - b.left) / k, (r.top - b.top) / k, r.width / k, r.height / k]; };
  const mc = (e) => { const r = q(e); return r ? [r[0] + r[2] / 2, r[1] + r[3] / 2] : null; };
  const M = (e) => e ? getComputedStyle(e).transform : null, O = (e) => e ? +getComputedStyle(e).opacity : null;
  (function loop(){ if (window.__stop) return; const r = document.querySelector(sel), s = document.querySelector('.stp');
    for (const a of document.getAnimations()) { if (window.__aSeen.has(a)) continue; const tg = a.effect && a.effect.target; if (!tg || !tg.closest) continue;
      if (!(tg.closest('.ltr') || tg.closest('.stp-close') || tg.classList.contains('stp-veil'))) continue; window.__aSeen.add(a); window.__aList.push({ a, start: null }); }
    for (const R of window.__aList) if (R.a.startTime != null) R.start = R.a.startTime;   /* kept while it lives: a filled animation is cancelled with its page */
    const f = { t: performance.now(), tt: document.timeline.currentTime, slide: CARD.slides[state.idx].id, end: document.body.classList.contains('is-end'), stpVeil: s ? O(s.querySelector('.stp-veil')) : null, stp: s ? s.className : '' };
    if (r) { const g = (x) => r.querySelector(x), pa = g('.ltr-paper'), gl = g('.stp-glit.on .stp-glow');
      Object.assign(f, { cls: r.className, layer: O(r), env: M(g('.ltr-env-pos')), flap: M(g('.ltr-flap')), heartO: O(g('.ltr-heart')), heart: M(g('.ltr-heart')),
        paper: M(pa), lines: pa ? +getComputedStyle(pa, '::after').opacity : null, blur: O(g('.ltr-blur')), pulse: O(g('.ltr-env-pos')), veil: O(g('.ltr-veil')),
        c: mc(g('.mk-c')), h: mc(g('.mk-h')), tl: mc(g('.mk-tl')), tr: mc(g('.mk-tr')), mo: mc(g('.mk-mo')), apex: mc(g('.mk-apex')), hinge: mc(g('.mk-hinge')),
        sparks: r.querySelectorAll('.stp-glit.on .stp-spark').length, glow: gl ? getComputedStyle(gl).animationName : '', gbox: q(g('.stp-glit')), pic: g('.stp-fin-pic') ? q(g('.stp-fin-pic')) : null }); }
    window.__tr.push(f); requestAnimationFrame(loop); })(); }"""
ANIMS = """() => (window.__aList || []).map(R => { const a = R.a, tg = a.effect.target, tm = a.effect.getTiming();
  return { start: R.start != null ? R.start : a.startTime, name: a.transitionProperty || a.animationName || '', cls: tg.getAttribute('class') || '', pe: a.effect.pseudoElement || '', delay: tm.delay, dur: tm.duration, dir: tm.direction }; })"""
BARE = """() => { window.__ft = []; (function f(n){ window.__ft.push(n); if (!window.__stopBare) requestAnimationFrame(f); })(performance.now()); }"""
ONE_ROUND = "(() => { const s = CARD.slides.find(s => s.id === 'L2'); s.data = Object.assign({}, s.data, { rounds: [s.data.rounds[s.data.rounds.length - 1]] }); })()"

def nums(s): return [float(x) for x in re.findall(r"-?[\d.]+(?:e-?\d+)?", s[s.index("(") + 1:])] if s and s != "none" else None
def scale_of(s):   # a 2-D (or planar 3-D) matrix's uniform scale
    v = nums(s)
    if v is None: return 1.0
    return math.hypot(v[0], v[1])
def rot_of(s):
    v = nums(s)
    return 0.0 if v is None else math.degrees(math.atan2(v[1], v[0]))
def flap_deg(s):   # rotate(t) rotateX(a) rotate(-t): its z-z entry is cos a
    v = nums(s)
    if v is None or len(v) < 16: return 0.0
    return math.degrees(math.acos(max(-1.0, min(1.0, v[10]))))
def rise_of(s):    # the sheet's rotate(-12.72deg) translateY(-d): |its translation| = d
    v = nums(s)
    if v is None: return 0.0
    return math.hypot(v[4], v[5]) if len(v) == 6 else math.hypot(v[12], v[13])
def interp(ser, t):
    for (t0, v0), (t1, v1) in zip(ser, ser[1:]):
        if t0 <= t <= t1: return v0 + (v1 - v0) * ((t - t0) / (t1 - t0) if t1 > t0 else 0)
    return None
def band(rev, fwd, E_r, E_f, D, off_r=0, off_f=0, slack=6):
    """rev(E_r + off_r + x) against fwd(E_f + off_f + D - x) for x in [0, D], both on the document timeline from their animations' own
    starts: the reverse value must lie within the forward curve's values over +-slack ms around the mirrored moment (the timeline is
    quantised to frames); returns (samples, worst excess, where)"""
    n, worst, at = 0, 0.0, None
    for (t, v) in rev:
        x = t - E_r - off_r
        if x < 0 or x > D: continue
        tm = E_f + off_f + D - x
        before = max((tt for (tt, _) in fwd if tt <= tm), default=None); after = min((tt for (tt, _) in fwd if tt >= tm), default=None)
        if before is None or after is None or after - before > 34: continue   # the reference skipped frames there (a busy frame): no reliable value to judge against
        vals = [vv for (tt, vv) in fwd if tm - slack <= tt <= tm + slack]
        for edge in (tm - slack, tm + slack):
            iv = interp(fwd, edge)
            if iv is not None: vals.append(iv)
        if not vals: continue
        ex = max(0.0, min(vals) - v, v - max(vals)); n += 1
        if ex > worst: worst, at = ex, round(x)
    return n, round(worst, 4), at

def ev(cls, who, what, kind="add", after=0):
    for c in cls:
        if c["el"] == who and c.get(kind) == what and c["t"] >= after: return c["t"]
    return None
def anim(al, cls_name, name, after, pe=""):   # the first animation of that element and property / keyframes begun after a moment
    c = [a for a in al if cls_name in a["cls"].split() and a["name"] == name and a["pe"] == pe and a["start"] is not None and after is not None and a["start"] >= after - 5]
    return min(c, key=lambda a: a["start"]) if c else None

with sync_playwright() as p:
    ARGS = ["--autoplay-policy=no-user-gesture-required", "--mute-audio", "--allow-file-access-from-files"]
    reqs = []   # every file the page fetches (file:// pages keep no resource timing; Playwright sees the requests)
    def page(b):
        pg = b.new_page(viewport={"width": 1280, "height": 720}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("request", lambda r_: reqs.append(r_.url.split("/")[-1].split("?")[0]))
        pg.add_init_script(HOOK); pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE); pg.evaluate("_ac()")   # the AudioContext made now, not on a beat
        return pg, errs
    def until(pg, base, ms): pg.wait_for_function(f"performance.now() - {base} >= {ms}", timeout=ms + 15000, polling=10)
    def drops(pg, RS):   # each round's slots in turn get their right stamp (the slot's own pick, or the round's), as smoke.py drops them
        fpx = lambda x, y: pg.evaluate("([x, y]) => { const b = document.getElementById('stage').getBoundingClientRect(), k = b.width / 1280; return [b.left + x * k, b.top + y * k]; }", [x, y])
        for ri, R in enumerate(RS):
            pg.wait_for_function(f"document.querySelector('.stp').dataset.round === '{ri}' && !!document.querySelector('.stp.live')", timeout=60000, polling=50)
            for j, sl in enumerate(R.get("slots") or [R["slot"]]):
                k = sl.get("pick", R["pick"]); bx = R["boxes"][k]; tp = R["tips"][k]
                if j: pg.wait_for_function(f"document.querySelectorAll('.stp-slot.gone').length >= {j} && !!document.querySelector('.stp.live')", timeout=10000); pg.wait_for_timeout(300)
                g = fpx(bx[0] + bx[2] / 2, bx[1] + 40); d = fpx(bx[0] + bx[2] / 2 + sl["x"] + sl["w"] / 2 - (bx[0] + tp[0]), bx[1] + 40 + sl["y"] + sl["h"] / 2 - (bx[1] + tp[1]))
                pg.mouse.move(g[0], g[1]); pg.mouse.down(); pg.wait_for_timeout(80)
                for i in range(1, 13): pg.mouse.move(g[0] + (d[0] - g[0]) * i / 12, g[1] + (d[1] - g[1]) * i / 12); pg.wait_for_timeout(16)
                pg.wait_for_timeout(60); pg.mouse.up()
            nsl = len(R.get("slots") or [R["slot"]])
            pg.wait_for_function(f"document.querySelectorAll('.stp-mark.in').length === {nsl}", timeout=8000)
    def mount_l2(pg, one_round=True):
        if one_round: pg.evaluate(ONE_ROUND)
        pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'L2'))")
        return pg.evaluate("CARD.slides.find(s => s.id === 'L2').data")

    # ================= run 1 (traced): L1's opening, then L2 to its finale and the end screen =================
    b = p.chromium.launch(channel="chrome", args=ARGS); pg, errs = page(b)
    D0 = pg.evaluate("CARD.slides.find(s => s.id === 'L2').data"); P = D0["pace"]; LY = D0["layout"]; C = P["close"]; HD = LY["hand"]
    L1 = pg.evaluate("CARD.slides.find(s => s.id === 'L1').data"); P1 = L1["pace"]; LY1 = L1["layout"]
    check("the finale's data: L1's pace copied as the transition to reverse (zoom, paper_at, dive_at, dive, dive_scale, veil_at, done_at), L1's envelope (its four layers, 610:6's box, the mouth), L1's paper crackle; 792:1253's picture and its blurred room; no dissolve and no dissolve chime",
          all(C[k] == P1[k] for k in ("zoom", "paper_at", "dive_at", "dive", "dive_scale", "veil_at", "done_at")) and D0["images"]["env"] == L1["env"] and LY["env_full"] == LY1["full"] and LY["env_mouth"] == LY1["mouth"]
          and D0["sfx"]["paper"] == L1["sfx"]["paper"] == "sfx_letter_paper" and D0["images"]["final"] == "img_stamp_final_pinki" and D0["images"]["fin_blur"] == "img_stamp_final_blur"
          and "final" not in D0["sfx"] and "fin_fade" not in P and LY["final"] == [0, -1, 1280, 721],
          {k: C[k] for k in ("zoom", "dive", "veil_at", "done_at")})
    # the beats' clock starts when the veil's fall has ended (the layer goes in then): V
    T = C["zoom"] + C["done_at"]; R0 = P["close_hold"] - (T - (C["zoom"] + C["veil_at"] + C["veil_ms"])); m = lambda t: R0 + T - t
    PLAN = {"on": 0, "unveil": m(C["zoom"] + C["veil_at"] + C["veil_ms"]), "undive": m(C["zoom"] + C["dive_at"] + C["dive"]), "sink": m(C["zoom"] + C["paper_at"] + C["sheet_ms"]),
            "shut": m(C["zoom"] + C["flap_ms"]), "seal": m(C["zoom"] + C["seal_ms"]), "away": m(C["zoom"]), "land": m(0) - P["land_lead"], "glitter": m(0) + P["fin_glitter_at"],
            "done": m(0) + P["fin_glitter_at"] + P["fin_glitter_ms"] + P["fin_done"]}
    PLAN["paper"] = PLAN["shut"] + P["close_paper_at"]
    print("INFO the plan (ms after the veil is full):", PLAN)
    # --- L1's opening, forward
    pg.evaluate(OBS); pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'L1'))")
    pg.wait_for_function("!!document.querySelector('.ltr.ready')", timeout=40000, polling=50)
    pg.evaluate(MARK, [".ltr", {"c": HD["c"], "mo": LY1["mouth"]}]); pg.evaluate(TRACE, ".ltr")
    bb = pg.locator(".ltr-env-pos").bounding_box(); pg.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
    pg.wait_for_function("CARD.slides[state.idx].id === 'L2' && !!document.querySelector('.stp.lit')", timeout=15000)
    pg.wait_for_timeout(900); trF = pg.evaluate("window.__stop = true, window.__tr"); clsF = pg.evaluate("window.__cls")
    tap = ev(clsF, "ltr", "zoom"); f_open = ev(clsF, "ltr", "open"); f_paper = ev(clsF, "ltr", "paper"); f_dive = ev(clsF, "ltr", "dive"); f_veil = ev(clsF, "ltr", "veil"); f_lit = ev(clsF, "stp", "lit")
    delta = (f_open - tap - C["zoom"]) if (f_open and tap) else 0
    check("L1's opening traced (the reference): zoom at the tap, the flap on the crackle's start, the sheet, the dive, the veil, then L2 with its veil lifting",
          tap and f_open and f_paper and f_dive and f_veil and f_lit, {"open": round(f_open - tap) if f_open and tap else None, "paper": round(f_paper - tap) if f_paper and tap else None,
                                                                       "dive": round(f_dive - tap) if f_dive and tap else None, "veil": round(f_veil - tap) if f_veil and tap else None, "L2 lit": round(f_lit - tap) if f_lit and tap else None})
    fl = [f for f in trF if f.get("cls") is not None]; fs = [f for f in trF if f.get("stpVeil") is not None]
    FWD = {"scale": [(f["tt"], scale_of(f["env"])) for f in fl], "flap": [(f["tt"], flap_deg(f["flap"])) for f in fl], "heartO": [(f["tt"], f["heartO"]) for f in fl],
           "heartS": [(f["tt"], scale_of(f["heart"])) for f in fl], "rise": [(f["tt"], rise_of(f["paper"])) for f in fl], "lines": [(f["tt"], f["lines"]) for f in fl],
           "blur": [(f["tt"], f["blur"]) for f in fl], "veil": [(f["tt"], f["veil"]) for f in fl], "stpVeil": [(f["tt"], f["stpVeil"]) for f in fs]}
    s_icon = LY1["letter"][2] / LY1["full"][2]
    FWD["zoomq"] = [(t, 1 - (v - s_icon) / (1 - s_icon)) for (t, v) in FWD["scale"] if tap and t <= tap + C["zoom"] + 300]
    # --- L2 to its finale
    if QUICK: pg.evaluate(ONE_ROUND); pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'L2'))")
    RS = pg.evaluate("CARD.slides.find(s => s.id === 'L2').data.rounds")
    pg.evaluate("window.__cls = []")
    drops(pg, RS)
    pg.wait_for_function("!!document.querySelector('.stp-veil.fall')", timeout=15000, polling=10); pg.evaluate(TRACE, ".stp-close")   # the veil's fall too
    pg.wait_for_function("!!document.querySelector('.stp-close')", timeout=3000, polling=5); pg.evaluate(MARK, [".stp-close", {"c": HD["c"], "mo": LY["env_mouth"]}])
    F = ev(pg.evaluate("window.__cls"), "veil", "fall")   # (no screenshots in this run: a shot can hold the page's timers)
    pg.wait_for_function("CARD.slides[state.idx].id === 'CEL' && document.body.classList.contains('is-end')", timeout=20000); pg.wait_for_timeout(600)
    tr = pg.evaluate("window.__stop = true, window.__tr"); cls = pg.evaluate("window.__cls"); pl = pg.evaluate(PLAYS); csT = pg.evaluate("window.__csT || []")
    pg.screenshot(path=str(out / "c7_end.png"))
    fr = [f for f in tr if f.get("cls") is not None and f["t"] >= F]
    E = {k: ev(cls, *a) for k, a in {"on": ("close", "(inserted)"), "unveil": ("veil", "lift"), "undive": ("close", "dive", "rm"), "sink": ("close", "paper", "rm"), "shut": ("close", "shut"),
                                      "seal": ("close", "seal"), "away": ("close", "zoom", "rm"), "land": ("close", "land")}.items()}
    last_drop = max((x["t"] for x in pl if x["src"] == "sfx_stamp_press.ogg"), default=None)
    check("the finale begins done_at after the last stamp is pressed (its thud thud_at after the drop), as the old one did: the veil starts falling over the table; the layer comes only under the full veil",
          last_drop and F and abs((F - last_drop) - (P["done_at"] - P["thud_at"])) < 60 and fr and fr[0]["stpVeil"] > 0.999 and fr[0]["layer"] == 1, (round(F - last_drop) if last_drop and F else None, fr[0]["stpVeil"] if fr else None))
    AL = pg.evaluate(ANIMS); V = E["on"]; A_fall = anim(AL, "stp-veil", "opacity", F)
    sched = {k: (round(E[k] - V) if E[k] and V else None, PLAN[k]) for k in E}
    check("the layer goes in the moment the veil's fall has really ended (its transitionend: within 25 ms of the fall's own end), and every later beat at its mirrored moment from there (within 30: setTimeout's jitter) — L1's moment t after its tap comes at R0 + T - t",
          V and A_fall and abs(V - (A_fall["start"] + P["close_veil"])) < 25 and all(v[0] is not None and abs(v[0] - v[1]) <= 30 for v in sched.values()),
          (round(V - F) if V else None, round(A_fall["start"] + P["close_veil"] - F) if A_fall else None, sched))
    # --- the mirror: each property against L1's, read backwards, both timed on the document timeline from their animations' own starts
    #     (a transition begins in the frame that resolves its class change: on a busy frame later than the change — L2's mount, the crackle's start)
    REV = {"scale": [(f["tt"], scale_of(f["env"])) for f in fr], "flap": [(f["tt"], flap_deg(f["flap"])) for f in fr], "heartO": [(f["tt"], f["heartO"]) for f in fr],
           "heartS": [(f["tt"], scale_of(f["heart"])) for f in fr], "rise": [(f["tt"], rise_of(f["paper"])) for f in fr], "lines": [(f["tt"], f["lines"]) for f in fr],
           "blur": [(f["tt"], f["blur"]) for f in fr], "stpVeil": [(f["tt"], f["stpVeil"]) for f in tr if f.get("stpVeil") is not None and f["t"] >= F]}
    s_hand = HD["scale"]
    REV["zoomq"] = [(t, (1 - v) / (1 - s_hand)) for (t, v) in REV["scale"] if E["away"] and t >= E["away"] - 300]
    pairs = [  # name, rev key, fwd key, (element, property, after, pseudo) reverse, the same forward, length, tolerance
        ("the veil lifting off the sheet = L1's veil coming down, backwards (.5 s)", "stpVeil", "veil", ("stp-veil", "opacity", E["unveil"], ""), ("ltr-veil", "opacity", f_veil, ""), C["veil_ms"], 0.03),
        ("the view pulling back out of the envelope = L1's dive backwards (the box's scale 5.2 -> 1 over 1.7 s)", "scale", "scale", ("ltr-env-pos", "transform", E["undive"], ""), ("ltr-env-pos", "transform", f_dive, ""), C["dive"], 0.03),
        ("the ruled lines coming back = L1's fading, backwards (1.2 s, ending with the pull-back)", "lines", "lines", ("ltr-paper", "opacity", E["undive"], "::after"), ("ltr-paper", "opacity", f_dive, "::after"), C["lines_ms"], 0.03),
        ("the sheet sinking into the pocket = L1's rise backwards (35 px over .9 s)", "rise", "rise", ("ltr-paper", "transform", E["sink"], ""), ("ltr-paper", "transform", f_paper, ""), C["sheet_ms"], 0.6),
        ("the flap coming down = L1's lift backwards (80 deg -> 0 over 1 s)", "flap", "flap", ("ltr-flap", "ltrFlap", E["shut"], ""), ("ltr-flap", "ltrFlap", f_open, ""), C["flap_ms"], 1.5),
        ("the seal coming back = L1's pop backwards (opacity, .35 s)", "heartO", "heartO", ("ltr-heart", "ltrSeal", E["seal"], ""), ("ltr-heart", "ltrSeal", f_open, ""), C["seal_ms"], 0.04),
        ("the seal coming back = L1's pop backwards (its scale .55 -> 1.18 -> 1)", "heartS", "heartS", ("ltr-heart", "ltrSeal", E["seal"], ""), ("ltr-heart", "ltrSeal", f_open, ""), C["seal_ms"], 0.03),
        ("the shrink into her hand = L1's zoom out of the cloud, backwards (the box's way, normalised, over 1.2 s)", "zoomq", "zoomq", ("ltr-env-pos", "transform", E["away"], ""), ("ltr-env-pos", "transform", tap, ""), C["zoom"], 0.02),
        ("the room coming into focus = L1's blur coming in, backwards (.9 s, ending with the landing)", "blur", "blur", ("ltr-blur", "opacity", E["away"], ""), ("ltr-blur", "opacity", tap, ""), C["blur_ms"], 0.03),
        ("the veil falling over the table = this page's veil lifting at its start, backwards (.6 s)", "stpVeil", "stpVeil", ("stp-veil", "opacity", F, ""), ("stp-veil", "opacity", f_lit, ""), P["close_veil"], 0.03)]
    lat = {}
    for name, rk, fk, ra, fa_, Dd, tol in pairs:
        A_r, A_f = anim(AL, *ra), anim(AL, *fa_)
        if not A_r or not A_f: check(name, False, ("no animation", bool(A_r), bool(A_f))); continue
        lat[rk + ("" if rk == fk else "/" + fk)] = (round(A_r["start"] - ra[2]), round(A_f["start"] - fa_[2]))
        n, worst, at_ = band(REV[rk], FWD[fk], A_r["start"] + A_r["delay"], A_f["start"] + A_f["delay"], Dd)
        check(name + f": every frame on L1's curve read backwards (within {tol}), {A_r['dur']:.0f} ms, {A_r['dir']}" + (f", {A_r['delay']:.0f} ms in" if A_r["delay"] else ""),
              n >= Dd / 40 and worst <= tol and abs(A_r["dur"] - Dd) < 1 and abs(A_f["dur"] - Dd) < 1, (n, worst, at_))
    print("INFO from each class change to its animation's start (ms: the finale's, L1's):", lat)
    # --- the states between the beats
    def frame_at(ms): return min(fr, key=lambda f: abs(f["t"] - F - ms))
    f0 = next((f for f in fr if E["unveil"] and f["t"] >= E["unveil"]), None)
    check("as the veil starts lifting: L1's dive's end state — the box at 5.2x with the mouth's centre on the frame's centre, the flap standing (80 deg), the seal gone, the sheet risen, its lines gone, the room blurred",
          f0 and abs(scale_of(f0["env"]) - C["dive_scale"]) < 0.02 and f0["mo"] and abs(f0["mo"][0] - 640) < 1.5 and abs(f0["mo"][1] - 360) < 1.5 and abs(flap_deg(f0["flap"]) - 80) < 0.5
          and f0["heartO"] == 0 and abs(rise_of(f0["paper"]) - 35) < 0.3 and f0["lines"] < 0.01 and f0["blur"] > 0.99,
          (round(scale_of(f0["env"]), 3), [round(v, 1) for v in f0["mo"]], round(flap_deg(f0["flap"]), 1), f0["heartO"], round(rise_of(f0["paper"]), 1), f0["lines"]) if f0 else None)
    fx = LY["env_full"]; A_seal = anim(AL, "ltr-heart", "ltrSeal", E["seal"]); A_away = anim(AL, "ltr-env-pos", "transform", E["away"])
    f_pre = max((f for f in fr if A_away and f["tt"] <= A_away["start"]), key=lambda f: f["tt"], default=None)            # the last frame before the shrink moves
    f_sl = next((f for f in fr if A_seal and f["tt"] >= A_seal["start"] + C["seal_ms"]), None)                          # the first with the seal's pop over
    ok_c = (f_pre and abs(scale_of(f_pre["env"]) - 1) < 0.002 and f_pre["mo"] and abs(f_pre["mo"][0] - (fx[0] + LY["env_mouth"][0])) < 0.6 and abs(f_pre["mo"][1] - (fx[1] + LY["env_mouth"][1])) < 0.6
            and flap_deg(f_pre["flap"]) < 1.0 and rise_of(f_pre["paper"]) < 0.1 and f_pre["lines"] > 0.99 and f_pre["blur"] > 0.99
            and f_sl and f_sl["heartO"] > 0.999 and abs(scale_of(f_sl["heart"]) - 1) < 0.002 and abs(scale_of(f_sl["env"]) - 1) < 0.003)
    check("closed: as the shrink sets off the envelope stands as L1's zoom left it — 610:6's box (untransformed), the flap down, the sheet in the pocket with its lines, the room still blurred — and the seal is whole as its pop ends",
          ok_c, ((round(f_pre["tt"] - F), round(scale_of(f_pre["env"]), 4), round(flap_deg(f_pre["flap"]), 2), round(rise_of(f_pre["paper"]), 2), f_pre["lines"], f_pre["blur"]) if f_pre else None,
                 (round(f_sl["tt"] - F), f_sl["heartO"], round(scale_of(f_sl["heart"]), 4)) if f_sl else None))
    fa = [f for f in fr if E["away"] and E["away"] <= f["t"] <= E["away"] + C["zoom"] + 40 and f["c"]]
    A0 = (fx[0] + HD["c"][0], fx[1] + HD["c"][1]); A1 = HD["to"]
    def off_line(pnt):
        dx, dy = A1[0] - A0[0], A1[1] - A0[1]; return abs((pnt[0] - A0[0]) * dy - (pnt[1] - A0[1]) * dx) / math.hypot(dx, dy)
    check("the shrink: the envelope's centre travels straight from where it stood to the picture's envelope's centre (every frame within 1 px of the line), turning and shrinking about it",
          fa and max(off_line(f["c"]) for f in fa) < 1.0 and abs(fa[0]["c"][0] - A0[0]) < 1 and abs(fa[0]["c"][1] - A0[1]) < 1, (len(fa), round(max(off_line(f["c"]) for f in fa), 3) if fa else None))
    fl_ = next((f for f in fr if E["away"] and f["t"] >= E["away"] + C["zoom"] + 60), None)
    PIC = {"c": HD["to"], "h": (812.05, 173.18), "tl": (754.41, 158.58), "tr": (846.03, 124.32)}   # make_stamp_close_assets.py: the picture's envelope
    dists = {k: round(math.hypot(fl_[k][0] - PIC[k][0], fl_[k][1] - PIC[k][1]), 2) for k in PIC} if fl_ and all(fl_.get(k) for k in PIC) else None
    check(f"landed in her hand: the drawing's envelope on the picture's — its centre on the picture's envelope's (within 0.6 px), its heart on her envelope's heart (within 1 px), its corners on the outline (within 4.5 px: the drawings' proportions differ), scale {s_hand}, turned {HD['rot']} deg",
          dists and dists["c"] < 0.6 and dists["h"] < 1.0 and dists["tl"] < 4.5 and dists["tr"] < 4.5 and abs(scale_of(fl_["env"]) - s_hand) < 0.0006 and abs(rot_of(fl_["env"]) - HD["rot"]) < 0.05,
          (dists, round(scale_of(fl_["env"]), 5) if fl_ else None, round(rot_of(fl_["env"]), 3) if fl_ else None))
    fland = [f for f in fr if E["land"] and E["land"] - 20 <= f["t"] <= E["land"] + P["land_ms"] + 60]
    pulse_ok = fland and fland[0]["pulse"] > 0.99 and fland[-1]["pulse"] < 0.01 and all(b_["pulse"] <= a_["pulse"] + 1e-6 for a_, b_ in zip(fland, fland[1:]))
    check(f"the drawing's envelope dissolves into the picture's own as it lands ({P['land_ms']} ms, only fading, gone by {P['land_ms']} ms), the picture stays: 792:1253's in its box (0,-1 1280x721)",
          pulse_ok and fr[-1]["pic"] and all(abs(fr[-1]["pic"][i] - LY["final"][i]) < 0.6 for i in range(4)) and fr[-1]["layer"] == 1, ([round(f["pulse"], 3) for f in fland[::4]], fr[-1]["pic"]))
    fg = next((f for f in fr if f["sparks"] > 0), None); EB = LY["envelope"]
    check(f"then the gold glitter on her envelope, as before: {P['fin_sparks']} sparks and the glow over the envelope's box {EB} (its outline's box + the old margins) at {P['fin_glitter_at']} ms after the landing",
          fg and abs(fg["t"] - V - PLAN["glitter"]) < 40 and fg["sparks"] == P["fin_sparks"] and fg["glow"] == "stpGlow" and fg["gbox"] and all(abs(fg["gbox"][i] - EB[i]) < 1 for i in range(4)),
          (round(fg["t"] - V) if fg else None, fg["sparks"] if fg else None, [round(v, 1) for v in fg["gbox"]] if fg and fg["gbox"] else None))
    snd = lambda name: [x for x in pl if x["src"] == name and x["t"] >= F]
    pap, gli = snd("sfx_letter_paper.ogg"), snd("sfx_stamp_glitter.ogg")
    check(f"the sounds: L1's paper crackle once, at L1's volume (.7), {P['close_paper_at']} ms into the flap's fall (its burst on the fall and the seal); the glitter's chime once with the glitter (.7); no dissolve chime, no tap pop",
          len(pap) == 1 and pap[0]["vol"] == 0.7 and E["shut"] and abs(pap[0]["t"] - E["shut"] - P["close_paper_at"]) < 30 and len(gli) == 1 and gli[0]["vol"] == 0.7 and fg and abs(gli[0]["t"] - fg["t"]) < 40
          and not snd("sfx_stamp_final.ogg") and not snd("sfx_letter_pop.ogg"),
          ([(round(x["t"] - F), x["vol"]) for x in pap], [(round(x["t"] - F), x["vol"]) for x in gli], len(snd("sfx_stamp_final.ogg")), len(snd("sfx_letter_pop.ogg"))))
    check("the old finale's picture and chime are never fetched (out of the card); the new picture, its blurred room and L1's envelope layers are",
          "img_stamp_final.webp" not in reqs and "sfx_stamp_final.ogg" not in reqs and all(x in reqs for x in ("img_stamp_final_pinki.webp", "img_stamp_final_blur.webp", "img_letter_env_flap.webp", "sfx_letter_paper.ogg")),
          sorted(set(x for x in reqs if "final" in x or "env_" in x or "paper" in x)))
    cs_after = [t for t in csT if t >= F]
    cel = next((f for f in tr if f["t"] >= F and f["slide"] == "CEL" and f["end"]), None)
    check(f"the page hands over to the end screen {PLAN['done']} ms after the veil is full (completeSlide on the page's own clock, within 60 ms), the end screen up within 1.5 s, no round gate",
          len(cs_after) == 1 and abs(cs_after[0] - V - PLAN["done"]) < 60 and cel and cel["t"] - cs_after[0] < 1500 and not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"),
          ([round(t - V) for t in cs_after], round(cel["t"] - cs_after[0]) if cel and cs_after else None))
    check("no page errors in the traced run", not errs, errs[:3])
    b.close()

    # ================= run 2: the closed envelope, frozen (DevTools pauses the page's animations), as drawn; then leaving mid-way =================
    b = p.chromium.launch(channel="chrome", args=ARGS); pg, errs = page(b); cdp = pg.context.new_cdp_session(pg); cdp.send("Animation.enable")
    D = mount_l2(pg); drops(pg, D["rounds"]); pg.evaluate(OBS)
    pg.wait_for_function("!!document.querySelector('.stp-close')", timeout=15000, polling=10); V2 = ev(pg.evaluate("window.__cls"), "close", "(inserted)")
    pg.wait_for_function("!!document.querySelector('.stp-close.seal')", timeout=8000, polling=5)
    until(pg, V2, PLAN["away"] + 15); cdp.send("Animation.setPlaybackRate", {"playbackRate": 0}); pg.wait_for_timeout(120)   # the seal whole, the shrink not yet moved (it starts from rest)
    pg.screenshot(path=str(out / "c_closed.png")); st_c = pg.evaluate("(() => { const r = document.querySelector('.stp-close'); return { cls: r.className, env: getComputedStyle(r.querySelector('.ltr-env-pos')).transform, flap: getComputedStyle(r.querySelector('.ltr-flap')).transform, heart: +getComputedStyle(r.querySelector('.ltr-heart')).opacity }; })()")
    cdp.send("Animation.setPlaybackRate", {"playbackRate": 1})
    # as drawn: the dist's own layers (inner, body, flap, heart) stacked over the blurred room at 610:6's box ARE the drawing; judged on the
    # envelope's flat parts (inside its silhouette eroded 4 px, off the drawing's edges, outside the seal's box), as letter_check judges L1's
    bx, by, bw, bh = (int(round(v)) for v in LY["env_full"])
    Tt = Image.open(IM / "img_stamp_final_blur.webp").convert("RGB").resize((1280, 720), Image.LANCZOS)
    for n_ in ("inner", "body", "flap", "heart"):
        Ly = Image.open(IM / f"img_letter_env_{n_}.webp").convert("RGBA").resize((bw, bh), Image.LANCZOS); Tt.paste(Ly, (bx, by), Ly)
    sil = np.zeros((720, 1280), bool)
    for n_ in ("body", "flap"):
        a_ = np.asarray(Image.open(IM / f"img_letter_env_{n_}.webp").convert("RGBA").getchannel("A").resize((bw, bh), Image.LANCZOS)) > 250
        sy, sx = max(0, -by), max(0, -bx); Y0, X0 = max(0, by), max(0, bx); hh, ww = min(bh - sy, 720 - Y0), min(bw - sx, 1280 - X0)
        sil[Y0:Y0 + hh, X0:X0 + ww] |= a_[sy:sy + hh, sx:sx + ww]
    er = np.asarray(Image.fromarray(sil.astype(np.uint8) * 255).filter(ImageFilter.MinFilter(9))) > 0
    gd = np.asarray(Tt.convert("L").filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(5))).astype(int)
    flat = er & (gd < 12); flat[240:470, 540:800] = False
    Zs = Image.open(out / "c_closed.png").convert("RGB"); dz = np.asarray(ImageChops.difference(Zs, Tt)).astype(float).sum(axis=2)
    dzo = float(dz[~sil].mean())
    Image.fromarray(np.clip(dz * 3, 0, 255).astype("uint8")).save(out / "c_closed_asdrawn_diff.png")
    check("frozen as it closes (the seal back, the shrink not yet moved): the envelope IS the drawing as drawn — its flat parts against the dist's layers stacked at 610:6's box (mean < 4, under 300 px over 40: an added line or a re-cut is thousands) — over 792:1253's blurred room (mean < 4 outside it)",
          dz[flat].mean() < 4 and int((dz[flat] > 40).sum()) < 300 and dzo < 4 and "seal" in st_c["cls"] and scale_of(st_c["env"]) > 0.999 and st_c["heart"] > 0.999,
          (round(float(dz[flat].mean()), 2), int((dz[flat] > 40).sum()), int(flat.sum()), round(dzo, 2), round(scale_of(st_c["env"]), 5), st_c["heart"]))
    # leaving mid-way (the dev nav), with the crackle sounding: its sounds stop, its timers die, its scene goes, no error
    pg.wait_for_function("window._plays.some(p => p.src === 'sfx_letter_paper.ogg' && !p.el.paused) || window._plays.filter(p => p.src === 'sfx_letter_paper.ogg').length > 0", timeout=4000, polling=10)
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'P2'))"); pg.wait_for_timeout(5000); pl2 = pg.evaluate(PLAYS)
    check("leaving mid-finale (to P2, with the crackle sounding): the page's sounds stop, its hook and timers are cleared (nothing of it after), its scene is gone, no error",
          all(x["paused"] for x in pl2 if "stamp" in x["src"] or "letter" in x["src"]) and pg.evaluate("window.oceanCleanup == null && !document.querySelector('.stp') && !document.querySelector('.stp-close')")
          and not any(x["src"] == "sfx_stamp_glitter.ogg" for x in pl2) and pg.evaluate("CARD.slides[state.idx].id") == "P2" and not errs, (errs[:2], [(x["src"], x["paused"]) for x in pl2 if "letter" in x["src"]]))
    b.close()

    # ================= run 3: the last frame before the glitter, frozen, against Figma 792:1253's render; the glitter shot =================
    b = p.chromium.launch(channel="chrome", args=ARGS); pg, errs = page(b); cdp = pg.context.new_cdp_session(pg); cdp.send("Animation.enable")
    D = mount_l2(pg); drops(pg, D["rounds"]); pg.evaluate(OBS)
    pg.wait_for_function("!!document.querySelector('.stp-close')", timeout=15000, polling=10); V3 = ev(pg.evaluate("window.__cls"), "close", "(inserted)")
    shots = {}   # live shots on the way (this run's timing is not judged), for the eye and the sheet's share: L1's moments 3.0 / 2.25 / 1.7 / 0.6 s mirrored
    for name, ms in (("c1_sheet", m(3000)), ("c2_open", m(2250)), ("c3_shut", m(1700)), ("c4_away", m(600))):
        until(pg, V3, ms); t_s = pg.evaluate("performance.now()"); pg.screenshot(path=str(out / (name + ".png"))); shots[name] = (round(t_s - V3), round(pg.evaluate("performance.now()") - V3))
    print("INFO the live shots (ms after the veil is full: asked, done):", shots)
    S1 = np.asarray(Image.open(out / "c1_sheet.png").convert("RGB")).astype(int); sheet = float(((S1[..., 0] > 228) & (S1[..., 2] > 222)).mean())
    check("the sheet fills the screen as the veil goes (the shot at L1's 3.0 s mirrored — that one read 98 %): over 90 % sheet pixels", sheet > 0.9, (round(sheet, 3), shots["c1_sheet"]))
    pg.wait_for_function("!!document.querySelector('.stp-close.land')", timeout=8000, polling=5)
    until(pg, V3, PLAN["land"] + P["land_ms"] + 80); cdp.send("Animation.setPlaybackRate", {"playbackRate": 0}); pg.wait_for_timeout(120)
    pg.screenshot(path=str(out / "c_final.png"))   # (the page's timers run on while its animations stand: a glitter begun now stands at its first, unseen frame)
    st_f = pg.evaluate("(() => { const r = document.querySelector('.stp-close'), gl = r.querySelector('.stp-glit .stp-glow'); return { pulse: +getComputedStyle(r.querySelector('.ltr-env-pos')).opacity, blur: +getComputedStyle(r.querySelector('.ltr-blur')).opacity, glit: Math.max(0, gl ? +getComputedStyle(gl).opacity : 0, ...[...r.querySelectorAll('.stp-glit .stp-spark')].map(e => +getComputedStyle(e).opacity)), veil: +getComputedStyle(document.querySelector('.stp-veil')).opacity }; })()")
    cdp.send("Animation.setPlaybackRate", {"playbackRate": 1})
    A_ = np.asarray(Image.open(out / "c_final.png").convert("RGB")).astype(float); B_ = np.asarray(Image.open(RENDER).convert("RGB")).astype(float)
    d_ = np.abs(A_ - B_).sum(axis=2); x0, y0, w0, h0 = LY["envelope"]; de = float(d_[y0:y0 + h0, x0:x0 + w0].mean())
    Image.fromarray(np.clip(d_ * 3, 0, 255).astype("uint8")).save(out / "c_final_diff.png")
    check("frozen once landed (before the glitter shows): the whole screen IS Figma 792:1253 — against its render: mean < 6 of 765 over the frame, < 8 over the envelope's box (no trace of the drawing's envelope left); the room sharp, the veil gone",
          d_.mean() < 6 and de < 8 and st_f["pulse"] < 0.01 and st_f["blur"] < 0.01 and st_f["glit"] < 0.01 and st_f["veil"] < 0.01, (round(float(d_.mean()), 2), round(de, 2), st_f))
    pg.wait_for_function("document.querySelectorAll('.stp-glit.on .stp-spark').length > 0", timeout=5000, polling=10); pg.wait_for_timeout(450)
    cdp.send("Animation.setPlaybackRate", {"playbackRate": 0}); pg.wait_for_timeout(100); pg.screenshot(path=str(out / "c_glitter.png")); cdp.send("Animation.setPlaybackRate", {"playbackRate": 1})
    G_ = np.asarray(Image.open(out / "c_glitter.png").convert("RGB")).astype(float); dg = np.abs(G_ - B_).sum(axis=2)
    gold = float(((G_[..., 0] - G_[..., 2]) > (B_[..., 0] - B_[..., 2]) + 6)[y0 - 20:y0 + h0 + 20, x0 - 20:x0 + w0 + 20].mean())
    check("mid-glitter: the gold shows over her envelope and nowhere else (the picture outside the glitter's reach unchanged: mean < 6)",
          gold > 0.05 and float(np.delete(dg, np.s_[max(0, y0 - 40):y0 + h0 + 40], axis=0).mean()) < 6, (round(gold, 3),))
    pg.wait_for_function("CARD.slides[state.idx].id === 'CEL' && document.body.classList.contains('is-end')", timeout=15000)
    check("no page errors in the frozen runs", not errs, errs[:3])
    b.close()

    # ================= runs 4 + 5: smoothness, bare (only the frames' times), each in a fresh browser: the finale, then L1's opening =================
    b = p.chromium.launch(channel="chrome", args=ARGS); pg, errs = page(b)
    D = mount_l2(pg); drops(pg, D["rounds"])
    pg.evaluate("(() => { const s = document.querySelector('.stp'), v = s.querySelector('.stp-veil'); const mo = new MutationObserver(() => { const t = performance.now(); if (v.classList.contains('fall') && !window.__F) window.__F = t; if (s.querySelector(':scope > .stp-close') && !window.__V) window.__V = t; }); mo.observe(v, { attributes: true, attributeFilter: ['class'] }); mo.observe(s, { childList: true }); })()")   # two elements: next to nothing
    pg.evaluate(BARE); pg.wait_for_function("!!window.__F", timeout=15000, polling=10); F4 = pg.evaluate("window.__F")
    pg.wait_for_function("CARD.slides[state.idx].id === 'CEL'", timeout=15000, polling=200); ft = pg.evaluate("window.__stopBare = true, window.__ft"); V4 = pg.evaluate("window.__V || 0")
    gaps = [(round(ft[i] - F4), round(ft[i + 1] - ft[i], 1)) for i in range(len(ft) - 1) if 0 <= ft[i] - F4 and ft[i] <= V4 + PLAN["done"]]
    hold = [g_ for g_ in gaps if V4 and V4 - F4 - 20 <= g_[0] <= V4 - F4 + P["close_hold"] - 20]   # under the full veil: unseen
    worst = max(gaps, key=lambda g_: g_[1]) if gaps else None
    b.close()
    b = p.chromium.launch(channel="chrome", args=ARGS); pg, errs5 = page(b)
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'L1'))"); pg.wait_for_function("!!document.querySelector('.ltr.ready')", timeout=40000, polling=100)
    pg.evaluate(BARE); bb = pg.locator(".ltr-env-pos").bounding_box(); t5 = pg.evaluate("performance.now()"); pg.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
    pg.wait_for_function("CARD.slides[state.idx].id === 'L2'", timeout=15000, polling=200); pg.wait_for_timeout(300); ft5 = pg.evaluate("window.__stopBare = true, window.__ft")
    gaps5 = [(round(ft5[i] - t5), round(ft5[i + 1] - ft5[i], 1)) for i in range(len(ft5) - 1) if 0 <= ft5[i] - t5 <= T]
    worst5 = max(gaps5, key=lambda g_: g_[1]) if gaps5 else None
    b.close()
    vf = V4 - F4 if V4 else 0
    seen = [g_ for g_ in gaps if g_ not in hold and g_[0] < vf + PLAN["glitter"] - 20]; glit = [g_ for g_ in gaps if g_[0] >= vf + PLAN["glitter"] - 20]
    worst = max(seen, key=lambda g_: g_[1]) if seen else None
    print("INFO frame gaps over 25 ms — the finale (ms after the fall's start; the veil full at", round(vf), "):", [g_ for g_ in gaps if g_[1] > 25][:14], " L1's opening:", [g_ for g_ in gaps5 if g_[1] > 25][:12])
    print("INFO the glitter's frames ([stamp-final]'s effect, unchanged): over 25 ms", [g_ for g_ in glit if g_[1] > 25], "| in the full veil's hold (unseen):", [g_ for g_ in hold if g_[1] > 25])
    check("smooth: the new work's frames — the veil's fall and the transition from the lift to the landing (bare, a fresh browser; the layer's first paint falls in the full veil's hold, unseen) — no gap over 50 ms, at most 3 over 34 ms (L1's opening measured the same way alongside)",
          seen and worst[1] < 50 and sum(1 for g_ in seen if g_[1] > 34) <= 3 and not errs, (len(seen), worst, sum(1 for g_ in seen if g_[1] > 34), "L1:", len(gaps5), worst5, sum(1 for g_ in gaps5 if g_[1] > 34)))
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
