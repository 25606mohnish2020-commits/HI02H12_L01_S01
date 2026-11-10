"""The stamp page L2 ([stamp-fig] + [stamp-drag] + [stamp-rounds] + [stamp-remind] + [stamp-final]; [stamp-868] 2026-11-03: the Figma frames
868:3 — the angled table with the bird — and 868:17 / 868:31 / 868:44 / 868:59 / 868:74 — the overhead table, one per round): mounted
straight (as the dev nav would). The page plays itself: the angled table as the letter page's veil lifts, the bird's entrance (the
reference title page's, on its whoosh), the instruction with the bird's GIF on the clip's clock and the stamps' glow on its "ठप्पा",
the bird's exit (backwards, the whoosh again), the camera move onto the overhead table, round 1's sentence read with the word light,
the box's 3 s blink. From there this script is the child: round 1 — it lets the guidance run (and come again after 7 s), takes hold of
the guiding stamp mid-glide, drops it far off, drops the wrong stamp on the box, taps a stamp, drops the right stamp on the box off its
centre; each later round — the clearing, its stamps' pops at once ([l2-quiet] 2026-11-04: NO line as the round opens), its sentence rising in
and read, its boxes' blink, no guidance (the round's own line only after 7 s idle), a wrong stamp on the box, then the right one on each box in turn; after the last round
the finale; a re-run; a mid-way exit with a stamp in hand. [stamp-close] (2026-11-04) the finale = L1's envelope transition backwards, then Figma 792:1253 with the
glitter — stamp_close_check.py has it beat by beat; here its moment, layer, sounds, landing, glitter and hand-over. The page's own frame trace (rAF) and a hook on every media play record the
beats; they are checked against each other and against the clips' own clocks, so Playwright's own lag never fails a good build. The
angled view (the bird landed), the overhead view (after the move) and every round's box moment (the blink paused) are compared with
the frames' renders. usage: python -I -X utf8 stamp_check.py <index.html> <outdir> [<stamp_assets dir with stamp868_*_render.png>]"""
import sys, re, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np
html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
here = pathlib.Path(__file__).resolve().parent
REF = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else here / "stamp_assets"
final_render = here / "stamp_assets" / "fig_792-1253_render.png"   # [stamp-close] the finale's last screen: Figma 792:1253's render
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)
def lit_first(times, wend, t):
    """[word-sync] the first word lit at clip time t: the stretch [start, next start) holding t (words sharing a start light together),
    the last up to the last word's end; -1 before the first word and after the end"""
    if t is None or (wend is not None and t >= wend): return -1
    st = None
    for x in times:
        if t >= x: st = x
    return times.index(st) if st is not None else -1
def sent_sync(tr, clip, wt, wend, since):
    fr_ = [f for f in tr if f["t"] >= since and f["vo"] and f["vo"][0] == clip + ".ogg" and not f["vo"][2] and f["vo"][1] > 0]
    return fr_, [f for f in fr_ if f["hot"] not in (lit_first(wt, wend, f["vo"][1]), lit_first(wt, wend, f["vo"][1] - 0.05))]
LEAVE = """() => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); }"""
HOOK = """(() => { window._plays = []; const P = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function(){ try{ window._plays.push({ src: String(this.src || '').split('/').pop().split('?')[0], t: performance.now(), el: this }); }catch(e){} return P.apply(this, arguments); }; })()"""
PLAYS = "() => window._plays.map(p => ({ src: p.src, t: p.t, paused: p.el.paused, cur: p.el.currentTime, dur: p.el.duration, vol: p.el.volume }))"
RECT = """(sel) => { const e = document.querySelector(sel); if(!e) return null; const b = document.getElementById('stage').getBoundingClientRect(), k = b.width / 1280, r = e.getBoundingClientRect();
  return [(r.left - b.left) / k, (r.top - b.top) / k, r.width / k, r.height / k]; }"""
TRACE = """() => { window.__tr = []; const st = document.getElementById('stage');
  const cs = completeSlide; completeSlide = function(){ window.__csT = performance.now(); return cs.apply(this, arguments); };   // when the page hands over (its own clock)
  const q = (e) => { if(!e) return null; const b = st.getBoundingClientRect(), k = b.width / 1280, r = e.getBoundingClientRect(); return [(r.left - b.left) / k, (r.top - b.top) / k, r.width / k, r.height / k]; };
  const op = (s) => { const e = document.querySelector(s); return e ? +getComputedStyle(e).opacity : null; };
  const tf = (s) => { const e = document.querySelector(s); return e ? getComputedStyle(e).transform : null; };
  (function loop(){ const r = document.querySelector('.stp'); if(!r){ window.__trEnd = performance.now(); return; } const ss = [...document.querySelectorAll('.stp-stamp')];
    const bm = document.querySelector('.stp-bmove'), bt = document.querySelector('.stp-btilt'), sh = document.querySelector('.stp-bsheet'), se = document.querySelector('.stp-sent');
    window.__tr.push({ t: performance.now(), round: r.dataset.round, lit: r.classList.contains('lit'), live: r.classList.contains('live'),
      bird: bm ? { op: +getComputedStyle(bm).opacity, tr: getComputedStyle(bm).translate, rot: getComputedStyle(bt).rotate, f: getComputedStyle(bt).filter, sheet: sh.style.transform } : null,
      glow: [...document.querySelectorAll('.stp-a-stamp')].map(s => s.classList.contains('thappa')), nA: document.querySelectorAll('.stp-a, .stp-a-tray, .stp-a-stamp').length, nH: document.querySelectorAll('.stp-a-halo.thappa').length,
      aOp: op('.stp-a'), aTxt: op('.stp-a-text'), aTray: op('.stp-a-tray'), tray: op('.stp-tray'), bo: tf('.stp-bo'), ao: tf('.stp-ao'), bi: tf('.stp-bi'), ai: tf('.stp-ai'),
      sOp: se ? +getComputedStyle(se).opacity : null, sBox: q(se), imgs: ss.map(s => s.querySelector('img').className + '|' + s.querySelector('img').src.split('/').pop() + '|' + getComputedStyle(s).display + '|' + (+getComputedStyle(s.querySelector('img')).opacity).toFixed(3)),
      words: document.querySelectorAll('.stp-sent .sfig-w.on').length, nwords: document.querySelectorAll('.stp-sent .sfig-w').length, rise: se ? se.classList.contains('sfig-rise') : false,
      hot: [...document.querySelectorAll('.stp-sent .sfig-w')].findIndex(w => w.classList.contains('hot')),
      slots: [...document.querySelectorAll('.stp-slot')].map(s => ({ cl: s.className, op: +getComputedStyle(s).opacity, anim: getComputedStyle(s).animationName, box: q(s), mark: !!s.querySelector('.stp-mark.in') })),
      fin: (() => { const f = document.querySelector('.stp-close'); if(!f) return null; const i = f.querySelector('.stp-fin-pic'), w = document.querySelector('.stp-glit.on .stp-glow'); return { op: +getComputedStyle(f).opacity, cls: f.className, src: i ? i.src.split('/').pop() : '', sparks: document.querySelectorAll('.stp-glit.on .stp-spark').length, glow: w ? getComputedStyle(w).animationName : '', gbox: q(f.querySelector('.stp-glit')), pulse: +getComputedStyle(f.querySelector('.ltr-env-pos')).opacity, blur: +getComputedStyle(f.querySelector('.ltr-blur')).opacity }; })(),
      mark: !!document.querySelector('.stp-mark.in'), st: ss.map(q), cl: ss.map(s => s.className), stf: ss.map(s => getComputedStyle(s).transform), conf: !!document.querySelector('.fx-confetti'),
      veil: +getComputedStyle(document.querySelector('.stp-veil')).opacity, nav: getComputedStyle(document.getElementById('navBtn')).display,
      vo: (typeof currentAudio !== 'undefined' && currentAudio) ? [String(currentAudio.src).split('/').pop(), currentAudio.currentTime, currentAudio.ended] : null });
    requestAnimationFrame(loop); })(); }"""
def shot(pg, name): pg.screenshot(path=str(out / name)); return out / name
def first(tr, cond, since=0):
    for f in tr:
        if f["t"] >= since and cond(f): return f
    return None
def last(tr, cond, before=1e18):
    hit = None
    for f in tr:
        if f["t"] <= before and cond(f): hit = f
    return hit
has = lambda cls, name: bool(cls) and name in cls.split()
cen = lambda r: (r[0] + r[2] / 2, r[1] + r[3] / 2)   # [stamp-868] a stamp seen from above: its centre is what is taken and judged
near = lambda a, c, tol: a is not None and c is not None and abs(a[0] - c[0]) < tol and abs(a[1] - c[1]) < tol
boxnear = lambda a, c, tol: a is not None and all(abs(a[i] - c[i]) < tol for i in range(4))
imgcls = lambda f, k: f["imgs"][k].split("|")[0].split() if len(f["imgs"]) > k else []
imgsrc = lambda f, k: f["imgs"][k].split("|")[1] if len(f["imgs"]) > k else ""
imgop = lambda f, k: float(f["imgs"][k].split("|")[3]) if len(f["imgs"]) > k else 0
shown_n = lambda f: sum(1 for k in range(len(f["imgs"])) if f["imgs"][k].split("|")[2] != "none")
px = lambda s: float(re.match(r"(-?[\d.e-]+)", s).group(1)) if s and s not in ("none",) and re.match(r"(-?[\d.e-]+)", s) else 0.0
def m3(s):   # a computed matrix3d / matrix as the 3x3 planar map it applies to (x, y, 1)
    if not s or s == "none": return np.eye(3)
    v = [float(x) for x in re.findall(r"-?[\d.]+(?:e-?\d+)?", s[s.index("(") + 1:])]   # (after the name: "matrix3d" has a digit)
    if s.startswith("matrix3d"): return np.array([[v[0], v[4], v[12]], [v[1], v[5], v[13]], [v[3], v[7], v[15]]])
    return np.array([[v[0], v[2], v[4]], [v[1], v[3], v[5]], [0, 0, 1]])
def ap(H, p): w = H @ np.array([p[0], p[1], 1.0]); return (w[0] / w[2], w[1] / w[2])
def frame_of(tfs, cell):
    m = re.match(r"translate\((-?[\d.]+)px,\s*(-?[\d.]+)px\)", tfs or "")
    return 0 if not m else int(round(-float(m.group(1)) / cell[0])) + 6 * int(round(-float(m.group(2)) / cell[1]))
def ink(img1280, x0, y0, x1, y1, thr=200):
    a = np.asarray(img1280).astype(int)[int(y0):int(y1), int(x0):int(x1)]; m = a.sum(axis=2) < thr; ys, xs = np.nonzero(m)
    return (int(xs.min() + x0), int(ys.min() + y0), int(xs.max() + x0), int(ys.max() + y0)) if len(xs) else None
def rows_of(img1280, boxes, y_lim=520):
    """each text row's ink (y0, y1, the densest row = its headline, x0, x1) on a 1280x720 shot, the boxes masked out"""
    a = np.asarray(img1280).astype(int); m = a.sum(axis=2) < 200; m[y_lim:, :] = False
    for b_ in boxes:   # (x, y) = a 90 box; [stamp-box] (x, y, w, h) any box
        bx, by, bw, bh = (list(b_) + [90, 90])[:4] if len(b_) == 2 else b_; bx, by = int(bx), int(by)
        m[max(0, by - 2):by + int(bh) + 2, max(0, bx - 2):bx + int(bw) + 2] = False
    ys = np.nonzero(m.any(axis=1))[0]
    if not len(ys): return []
    groups = []; s0 = p0 = ys[0]
    for y in ys[1:]:
        if y - p0 > 6: groups.append((s0, p0)); s0 = y
        p0 = y
    groups.append((s0, p0)); res = []
    for (y0, y1) in groups:
        xs = np.nonzero(m[y0:y1 + 1].any(axis=0))[0]; dens = m[y0:y1 + 1].sum(axis=1)
        res.append((int(y0), int(y1), int(y0 + np.argmax(dens)), int(xs.min()), int(xs.max())))
    return res
# [stamp-box] (2026-11-10) the boxes are BOX square (were the frames' 90): each keeps its frame's left edge and vertical centre; a box between
# two words (mid) has its room in the row 90 - BOX narrower and moves with its re-centred row by half that. FIG = the frames' 90 boxes
# (x, y, mid) per round, as drawn in 868:17 / 31 / 44 / 59 / 74.
BOX = 60; BOXD = 90 - BOX
FIG = [[(859, 226, False)], [(439, 293, True)], [(836, 232, False)], [(902, 193, False), (731, 266, False)],
       [(596, 45, True), (886, 135, False), (879, 248, False), (699, 422, False)]]
def box_drawn(img1280, x, y, w, h):
    """[stamp-box] a box as the page draws it, on a 1280x720 shot: its fill (the inside, 6 px in, #FD9337 within 14 per channel), its
    dashed stroke (the share of dark pixels along the line 1 px inside its edge: 0.6..0.92 — dashes and gaps, as both boxes draw them)
    and nothing orange beyond it (the ring 3..5 px outside it not orange: the box no bigger than w x h)"""
    a = np.asarray(img1280).astype(int); x, y, w, h = int(round(x)), int(round(y)), int(round(w)), int(round(h))
    fill = a[y + 6:y + h - 6, x + 6:x + w - 6].reshape(-1, 3).mean(axis=0); fill_ok = bool(np.all(np.abs(fill - [253, 147, 55]) < 14))
    edge = np.concatenate([a[y + 1, x + 1:x + w - 1], a[y + h - 2, x + 1:x + w - 1], a[y + 1:y + h - 1, x + 1], a[y + 1:y + h - 1, x + w - 2]])
    dark = float((edge.sum(axis=1) < 300).mean())
    ring = np.concatenate([a[y - 5:y - 2, x:x + w].reshape(-1, 3), a[y + h + 2:y + h + 5, x:x + w].reshape(-1, 3), a[y:y + h, x - 5:x - 2].reshape(-1, 3), a[y:y + h, x + w + 2:x + w + 5].reshape(-1, 3)])
    orange = float(((np.abs(ring - [253, 147, 55]) < 30).all(axis=1)).mean())
    return fill_ok and 0.6 <= dark <= 0.92 and orange < 0.05, (np.round(fill).tolist(), round(dark, 2), round(orange, 3))
def diff(a_path, b_path, name):
    A = Image.open(a_path).convert("RGB").resize((1280, 720), Image.LANCZOS); B = Image.open(b_path).convert("RGB")
    d = np.asarray(ImageChops.difference(A, B)).astype(float).sum(axis=2)
    Image.fromarray(np.clip(d * 2, 0, 255).astype("uint8")).save(out / (name + "_diff.png")); return A, B, d

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(HOOK)
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE)
    now = lambda: pg.evaluate("performance.now()")
    def until(base, ms): pg.wait_for_function(f"performance.now() - {base} >= {ms}", timeout=ms + 8000, polling=20)
    fp = lambda x, y: pg.evaluate("([x, y]) => { const b = document.getElementById('stage').getBoundingClientRect(), k = b.width / 1280; return [b.left + x * k, b.top + y * k]; }", [x, y])
    def drag(a, c, steps=12):   # the child's drag, frame px: down, a dozen moves, up
        x0, y0 = fp(*a); x1, y1 = fp(*c)
        pg.mouse.move(x0, y0); pg.mouse.down(); pg.wait_for_timeout(80)
        for i in range(1, steps + 1): pg.mouse.move(x0 + (x1 - x0) * i / steps, y0 + (y1 - y0) * i / steps); pg.wait_for_timeout(16)
        pg.wait_for_timeout(60); pg.mouse.up()
    ids = pg.evaluate("CARD.slides.map(s => s.id)")
    check("the pages: ... P2, L1 (the letter page), L2 (the stamp page), then the end screen (17)", ids == ["T0", "T0B", "T1", "T1B", "T1C", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "L1", "L2", "CEL"], ids)
    D = pg.evaluate("CARD.slides.find(s => s.id === 'L2').data"); P = D["pace"]; RS = D["rounds"]; LY = D["layout"]
    slots_of = lambda R: R.get("slots") or [R["slot"]]
    check("[stamp-868] five rounds on 868:17 (the ?, with the guidance), 868:31 (the comma, two rows), 868:44 (the danda), 868:59 (the ? for two questions: TWO boxes), 868:74 (the letter's closing lines: FOUR boxes — the comma, the ?, the danda twice; no sign-off); every box 60x60 ([stamp-box]); the stamps in the frames' order (। ? / । , / । , ?)",
          len(RS) == 5 and [R["frame"] for R in RS] == ["868:17", "868:31", "868:44", "868:59", "868:74"] and [R["mark"] for R in RS] == ["?", ",", "।", "?", "।"] and [R["pick"] for R in RS] == [1, 1, 0, 2, 0]
          and [len(R["stamps"]) for R in RS] == [2, 2, 3, 3, 3] and RS[0]["guide"] is True and all(R["guide"] is False for R in RS[1:]) and [len(slots_of(R)) for R in RS] == [1, 1, 1, 2, 4]
          and all(s_["w"] == BOX and s_["h"] == BOX for R in RS for s_ in slots_of(R)) and [S_.get("mark", RS[4]["mark"]) for S_ in RS[4]["slots"]] == [",", "?", "।", "।"] and [S_.get("pick", RS[4]["pick"]) for S_ in RS[4]["slots"]] == [1, 2, 0, 0]
          and not RS[4].get("sign") and RS[2]["stamps"] == ["img_stamp8_danda", "img_stamp8_comma", "img_stamp8_question"] and "band_hi" not in D,
          [(R["frame"], R["mark"], R["pick"], len(R["stamps"]), len(slots_of(R))) for R in RS])
    gw = lambda R: [g_["w"] for g_ in (R["sent"].get("gap") if isinstance(R["sent"].get("gap"), list) else [R["sent"]["gap"]] if R["sent"].get("gap") else [])]
    check(f"[stamp-box] every box {BOX}x{BOX} at its frame's left edge and vertical centre (a box between two words: its room in the row {BOXD} px narrower — 868:31's 90 -> 60, 868:74's 97 -> 67 — and the box {BOXD // 2} px right, with the re-centred row), 11 px corners and the smaller box's dash runs; the thud at .54 (40 % below .9)",
          all(abs(s_["x"] - (fx + (BOXD / 2 if mid else 0))) < 0.01 and abs(s_["y"] - (fy + BOXD / 2)) < 0.01 for R, F in zip(RS, FIG) for s_, (fx, fy, mid) in zip(slots_of(R), F))
          and [len(slots_of(R)) for R in RS] == [len(F) for F in FIG] and gw(RS[1]) == [60, 3] and gw(RS[4]) == [67] and not gw(RS[0]) and not gw(RS[2]) and not gw(RS[3])
          and LY["box_r"] == 11 and LY["box_dash"] == "7 5.5 13 5.5 29.71 5.5 13 5.5 29.71 5.5 13 5.5 29.71 5.5 13 5.5 22.71" and P.get("thud_vol") == 0.54,
          ([[(s_["x"], s_["y"], s_["w"]) for s_ in slots_of(R)] for R in RS], gw(RS[1]), gw(RS[4]), LY["box_r"], P.get("thud_vol")))
    def geo(R):
        SLS = slots_of(R); SCS = [(S_["x"] + S_["w"] / 2, S_["y"] + S_["h"] / 2) for S_ in SLS]; bx = R["boxes"]; tp = R["tips"]
        PKS = [S_.get("pick", R["pick"]) for S_ in SLS]; MKS = [S_.get("mark", R["mark"]) for S_ in SLS]
        handles = [(bb[0] + bb[2] / 2, bb[1] + bb[3] / 2) for bb in bx]   # [stamp-868] where the child takes hold: the stamp's middle
        onto = lambda k, ox=0, oy=0, j=0: (handles[k][0] + SCS[j][0] - (bx[k][0] + tp[k][0]) + ox, handles[k][1] + SCS[j][1] - (bx[k][1] + tp[k][1]) + oy)
        return dict(SL=SLS[0], sc=SCS[0], SLS=SLS, SCS=SCS, PKS=PKS, MKS=MKS, bx=bx, tp=tp, h=handles, onto=onto)
    G = [geo(R) for R in RS]; SL, sc, S0, S1, g0, g1, on_ = G[0]["SL"], G[0]["sc"], G[0]["bx"][0], G[0]["bx"][1], G[0]["h"][0], G[0]["h"][1], G[0]["onto"]; WT = RS[0]["sentence"]["word_times"]
    check("each round's stamps are taken by their middle and judged by their centre (tips = half their box), lifted to 1.1, pressed at .96; the boxes' drop tolerance 60 px",
          all(R["tips"][k] == [R["boxes"][k][2] / 2, R["boxes"][k][3] / 2] for R in RS for k in range(len(R["boxes"]))) and P["lift_scale"] == 1.1 and P["press_scale"] == 0.96 and P["tol_x"] == 60 and P["tol_y"] == 60 and P["hover_up"] == 0 and P["press_down"] == 0)
    # the later rounds: which stamp is dropped wrong, where the right one is dropped (off its centre)
    LATER = [dict(ri=1, wrong=0, offs=[(12, 9)]), dict(ri=2, wrong=1, offs=[(-20, 15)]), dict(ri=3, wrong=1, offs=[(18, -12), (-14, 14)]),
             dict(ri=4, wrong=0, offs=[(10, 7), (-12, 12), (14, -9), (-9, -13)])]
    t0 = pg.evaluate("(() => { const t = performance.now(); mountSlide(CARD.slides.findIndex(s => s.id === 'L2')); return t; })()")
    pg.evaluate(TRACE)
    ZM = 680 * P["bird_tempo"]
    # ---- live shots at the beats (the checks read the page's own trace): the bird landed (the angled view), after the move (the overhead
    #      view, before its box), the box (its blink paused at full opacity)
    until(t0, P["bird_at"] + ZM + 60); z3 = shot(pg, "l2_angled.png")
    pg.wait_for_function("!document.querySelector('.stp-bird')", timeout=30000, polling=20); until(now(), 120); z17 = shot(pg, "l2_overhead.png")
    pg.wait_for_function("!!document.querySelector('.stp-slot.in')", timeout=15000); ta = pg.evaluate("getComputedStyle(document.querySelector('.stp-stamp.s0')).touchAction")
    pg.wait_for_function("!!document.querySelector('.stp-slot.in:not(.blink)')", timeout=8000, polling=10); zb = shot(pg, "l2_box.png")   # the box standing still after its blink, before the guidance
    # ---- the child's part, round 1: the guidance runs, comes again after 7 s; a grab mid-guidance; the drops
    pg.wait_for_function("!!document.querySelector('.stp-stamp.s1.lift')", timeout=9000); t_h1 = now(); until(t_h1, P["glide"] + 100); shot(pg, "l2_hint.png")
    pg.wait_for_function("!document.querySelector('.stp-stamp.s1.lift')", timeout=8000)
    pg.wait_for_function("!!document.querySelector('.stp-stamp.s1.lift')", timeout=12000); t_h2 = now(); until(t_h2, 700)
    r = pg.evaluate(RECT, ".stp-stamp.s1"); x, y = fp(r[0] + r[2] / 2, r[1] + r[3] / 2); pg.mouse.move(x, y); pg.mouse.down(); pg.wait_for_timeout(120)
    x1, y1 = fp(150, 380)
    for i in range(1, 13): pg.mouse.move(x + (x1 - x) * i / 12, y + (y1 - y) * i / 12); pg.wait_for_timeout(16)
    pg.wait_for_timeout(60); pg.mouse.up(); t_d1 = now(); until(t_d1, 150); wbox = pg.evaluate(RECT, ".stp-stamp.s1"); wbg = pg.evaluate("getComputedStyle(document.querySelector('.stp-stamp.s1')).backgroundColor")
    wshot = shot(pg, "l2_wrong.png"); until(t_d1, P["wiggle"] + P["reset"] + 300)
    drag(g0, on_(0)); t_d2 = now(); until(t_d2, P["wiggle"] + P["reset"] + 300)
    xt, yt = fp(*g1); pg.mouse.move(xt, yt); pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.move(xt + 3, yt + 2); pg.mouse.up(); t_tap = now(); until(t_tap, 450)
    drag(g1, on_(1, 30, 20)); t_d3 = now(); until(t_d3, P["snap"] + P["press"] - 30); shot(pg, "l2_press.png")
    pg.wait_for_function("!!document.querySelector('.stp-slot.gone')", timeout=8000); until(now(), 450); done = shot(pg, "l2_done.png")
    # the confetti seen by the frame trace (not merely present now: a shot slowed by the machine can outlast its life)
    pg.wait_for_function(f"!!document.querySelector('.fx-confetti') || window.__tr.some(f => f.conf && f.t > {t_d3})", timeout=8000); until(now(), 500); shot(pg, "l2_confetti.png")
    # ---- the later rounds: the clearing, the round set, the boxes; 7 s idle (the round's line again), a wrong drop, the right drops
    LT = []
    for L_ in LATER:
        ri = L_["ri"]; g = G[ri]; rec = dict(L_); nsl = len(g["SLS"])
        pg.wait_for_function(f"document.querySelector('.stp').dataset.round === '{ri}'", timeout=9000); t_set = now(); until(t_set, 150); shot(pg, f"l2_r{ri}_set.png")
        pg.wait_for_function("!!document.querySelector('.stp.live')", timeout=30000); t_live = now()
        pg.wait_for_function("[...document.querySelectorAll('.stp-slot')].every(s => s.classList.contains('in') && !s.classList.contains('blink'))", timeout=8000, polling=10)
        rec["z"] = shot(pg, f"l2_r{ri}_box.png")   # the boxes standing still after their blink
        until(t_live, P["idle_ms"] + 900); shot(pg, f"l2_r{ri}_idle.png")
        pg.wait_for_function("!isPlaying", timeout=10000)
        drag(g["h"][L_["wrong"]], g["onto"](L_["wrong"])); rec["t_wrong"] = now(); until(rec["t_wrong"], P["wiggle"] + P["reset"] + 300)
        rec["dones"] = []
        for j in range(nsl):
            if j: pg.wait_for_function(f"document.querySelectorAll('.stp-slot.gone').length >= {j} && !!document.querySelector('.stp.live')", timeout=8000); until(now(), 300)
            sfx_ = "" if j == 0 else str(j + 1)
            pk = g["PKS"][j]; drag(g["h"][pk], g["onto"](pk, *L_["offs"][j], j)); rec["t_drop"] = now(); until(rec["t_drop"], P["snap"] + P["press"] - 30); shot(pg, f"l2_r{ri}_press{sfx_}.png")
            pg.wait_for_function(f"document.querySelectorAll('.stp-slot.gone').length >= {j + 1}", timeout=8000); until(now(), 450); rec["dones"].append(shot(pg, f"l2_r{ri}_done{sfx_}.png"))
        pg.wait_for_function(f"!!document.querySelector('.fx-confetti') || window.__tr.some(f => f.conf && f.t > {rec['t_drop']})", timeout=8000); until(now(), 500); shot(pg, f"l2_r{ri}_confetti.png")
        LT.append(rec)
    # [stamp-close] the finale: L1's envelope transition backwards; the shot once the envelope has landed in her hand (792:1253), the glitter's
    pg.wait_for_function("!!document.querySelector('.stp-close.land')", timeout=20000, polling=10); t_land = now(); until(t_land, P["land_lead"] + P["land_ms"] + 30); fin_shot = shot(pg, "l2_final.png")
    until(t_land, P["land_lead"] + P["fin_glitter_at"] + 500); shot(pg, "l2_glitter.png")
    pg.wait_for_function("CARD.slides[state.idx].id === 'CEL' && document.body.classList.contains('is-end')", timeout=15000); t_cel = now()
    tr = pg.evaluate("window.__tr"); pl = pg.evaluate(PLAYS); tr_end = pg.evaluate("window.__trEnd || 0"); cs_t = pg.evaluate("window.__csT || 0")
    snd = lambda name: [x for x in pl if x["src"] == name + ".ogg"]
    T = lambda f: round(f["t"] - t0) if f else None
    # ==== 1. the angled table (868:3) under the lifting veil; the bird not yet in
    f0 = tr[0]
    check("mounts as a whole-stage page: no आगे, the veil lifting from the first frames, the angled table (868:3) up (its layers at full opacity, its painted sentence on), the bird, the overhead tray and stamps and the live sentence unseen (at .005: painted from the first frame)",
          f0["nav"] == "none" and f0["aOp"] == 1 and f0["aTxt"] == 1 and f0["nA"] == 4 and f0["bird"]["op"] <= 0.006 and f0["tray"] <= 0.006 and f0["sOp"] <= 0.006 and all(imgop(f0, k) <= 0.006 for k in range(2))
          and T(first(tr, lambda f: f["lit"])) < 250 and first(tr, lambda f: f["veil"] < 0.05) is not None and T(first(tr, lambda f: f["veil"] < 0.05)) < 1300,
          (f0["nav"], f0["aOp"], f0["nA"], f0["bird"]["op"], f0["tray"], f0["sOp"], T(first(tr, lambda f: f["veil"] < 0.05))))
    # ==== 2. the bird's entrance: the reference title page's zoom, on its whoosh
    wh = snd("sfx_stamp_whoosh"); bf = [f for f in tr if f["bird"] and P["bird_at"] - 100 < f["t"] - t0 < P["bird_at"] + ZM + 200]
    trs = [(f["t"] - t0, px(f["bird"]["tr"]), f["bird"]["op"], px(f["bird"]["rot"]), f["bird"]["f"]) for f in bf]
    fstart = next((x for x in trs if x[1] < -100), None); fpeak = max((x for x in trs if x[0] > P["bird_at"] + 0.4 * ZM), key=lambda x: x[1], default=None)
    flast = trs[-1] if trs else None; blurs = [x[4] for x in trs if x[0] < P["bird_at"] + 0.3 * ZM]
    check(f"the bird's entrance at {P['bird_at']} ms, on the reference's whoosh at .75 (within 80 ms): it comes in from 200 px out to the left (fading in), glides to its place with its 6 px overshoot (the frames' peak 3.5..6 px past it, a third of the way in: the eased timeline's 75 %) and settles at 0 by {round(ZM)} ms — leaning (5 deg, then -3, then 0) with a blur that clears",
          len(wh) >= 1 and abs(wh[0]["t"] - t0 - P["bird_at"]) < 80 and abs(wh[0]["vol"] - P["whoosh_vol"]) < 0.01 and fstart and fstart[1] < -150 and fpeak and 3.5 <= fpeak[1] <= 6.01 and fpeak[0] - P["bird_at"] < 0.6 * ZM
          and flast and abs(flast[1]) < 0.05 and flast[2] == 1 and max(x[3] for x in trs) > 4 and min(x[3] for x in trs) < -2 and any("blur" in (b_ or "") and px(b_.replace("blur(", "")) > 1 for b_ in blurs),
          (round(wh[0]["t"] - t0) if wh else None, wh[0]["vol"] if wh else None, fstart[1] if fstart else None, (round(fpeak[0]), round(fpeak[1], 2)) if fpeak else None, round(max(x[3] for x in trs), 2) if trs else None, round(min(x[3] for x in trs), 2) if trs else None))
    # ==== 3. the instruction with the bird's GIF on its clock; the glow on "ठप्पा"
    voi = lambda f: f["vo"] and f["vo"][0] == "vo_stamp_intro.ogg"
    f_is = first(tr, lambda f: voi(f) and f["vo"][1] > 0); f_ie = first(tr, lambda f: voi(f) and f["vo"][2])
    intro = snd("vo_stamp_intro"); intro1 = [x for x in intro if x["t"] < t_d3]
    check(f"the instruction (vo_stamp_intro) starts {P['vo_gap']} ms after the bird has landed (within 150), once", len(intro1) == 1 and abs(intro1[0]["t"] - t0 - P["bird_at"] - ZM - P["vo_gap"]) < 150,
          round(intro1[0]["t"] - t0) if intro1 else None)
    cell = LY["bird"]["cell"]; NF = LY["bird"]["n"]; dur = next((x["dur"] for x in intro1), None) or P["intro_ms"] / 1000
    gif = [(f["vo"][1], frame_of(f["bird"]["sheet"], cell)) for f in tr if voi(f) and 0 < f["vo"][1] < dur - 0.02 and not f["vo"][2] and f["bird"]]
    off = [(round(t_, 3), g_) for t_, g_ in gif if min(abs(g_ - int(t_ / dur * P["bird_loops"] * NF) % NF), NF - abs(g_ - int(t_ / dur * P["bird_loops"] * NF) % NF)) > 1]
    seen = {g_ for _, g_ in gif}; f_after = first(tr, lambda f: f["bird"], since=f_ie["t"] + 30) if f_ie else None
    check(f"the bird's GIF plays on the clip's own clock: in every frame while it speaks, its sheet shows frame ⌊t / {round(dur, 3)} s x {P['bird_loops']} x {NF}⌋ mod {NF} (within one frame) — all {NF} frames shown — and the first frame again as it ends",
          len(gif) > 200 and not off and len(seen) >= NF - 1 and f_after and frame_of(f_after["bird"]["sheet"], cell) == 0, (len(gif), off[:5], len(seen), frame_of(f_after["bird"]["sheet"], cell) if f_after else None))
    fgl = first(tr, lambda f: all(f["glow"]) and f["glow"])
    gl_t = fgl["vo"][1] if fgl and fgl["vo"] and voi(fgl) else None
    gan = pg.evaluate("(() => ['stp-a-stamp thappa', 'stp-a-halo thappa'].map(c_ => { const s = document.createElement('img'); s.className = c_; document.body.appendChild(s); const c = getComputedStyle(s); const r = c.animationName + ' ' + c.animationDuration; s.remove(); return r; }))()")
    check(f"on the clip's \"ठप्पा\" ({P['thappa'] / 1000} s on its clock: the ठ's burst at 5.14 s) BOTH standing stamps glow and pulse — each one's baked halo fading up behind it (stpHalo), both pulsing twice by 4 % about the stamp's base (stpPulse), 1.6 s — first seen within 50 ms after",
          gl_t is not None and 0 <= gl_t - P["thappa"] / 1000 < 0.05 and gan == ["stpPulse 1.6s", "stpHalo 1.6s"] and fgl["nH"] == 2, (round(gl_t, 3) if gl_t is not None else None, gan, fgl["nH"] if fgl else None))
    # ==== 4. the bird's exit: the entrance backwards, the whoosh again
    exf = [f for f in tr if f["bird"] and f_ie and f_ie["t"] + P["exit_gap"] - 50 < f["t"] < f_ie["t"] + P["exit_gap"] + ZM + 150]
    xs_ = [(f["t"] - f_ie["t"], px(f["bird"]["tr"]), f["bird"]["op"]) for f in exf]
    fend = next((x for x in xs_ if x[1] < -199 and x[2] < 0.01), None); pk2 = max((x for x in xs_), key=lambda x: x[1], default=None)
    fst = next((x for x in xs_ if x[0] > P["exit_gap"] + 40), None)
    check(f"{P['exit_gap']} ms after the instruction ends the bird leaves the way it came, backwards ({round(ZM)} ms: the entrance's moves in reverse — easing off its place a little to the right, its overshoot's 6 px, then out to the left, fading), its whoosh mirrored too: ending as the bird is gone (it starts {P['whoosh_ms']} ms before)",
          f_ie and len(wh) >= 2 and abs(wh[1]["t"] - f_ie["t"] - P["exit_gap"] - ZM + P["whoosh_ms"]) < 120 and fst and fst[1] >= -0.5 and pk2 and 3.5 <= pk2[1] <= 6.01 and pk2[0] - P["exit_gap"] > 0.4 * ZM and fend and abs(fend[0] - P["exit_gap"] - ZM) < 150,
          (round(wh[1]["t"] - f_ie["t"]) if len(wh) > 1 and f_ie else None, (round(pk2[0]), round(pk2[1], 2)) if pk2 else None, round(fend[0]) if fend else None))
    # ==== 5. the camera move: every frame, the card's corners as each layer's map draws them (from the layers' computed matrices)
    QA, QB, DA, DB = LY["a_quad"], LY["b_quad"], LY["a_dash"], LY["b_dash"]
    mv = [f for f in tr if f["bo"] and f["bo"].startswith("matrix3d")]
    if mv:
        dur_mv = mv[-1]["t"] - mv[0]["t"]; gaps = [b_["t"] - a_["t"] for a_, b_ in zip(mv, mv[1:])]
        # frame by frame (a map near the identity serializes as a 2D matrix(...): m3 reads both)
        qb = [[ap(m3(f["bo"]), c) for c in QB] for f in mv]; qa = [[ap(m3(f["ao"]), c) for c in QA] for f in mv]
        db_ = [[ap(m3(f["bi"]), c) for c in DB] for f in mv]; da_ = [[ap(m3(f["ai"]), c) for c in DA] for f in mv]
        same = max(max(abs(x - y) for p_, q_ in zip(a1, b1) for x, y in zip(p_, q_)) for a1, b1 in zip(qa, qb)) if qa else None
        samed = max(max(abs(x - y) for p_, q_ in zip(a1, b1) for x, y in zip(p_, q_)) for a1, b1 in zip(da_, db_)) if da_ else None
        mono = all(abs(qb[i + 1][0][1] - qb[i][0][1]) < 6 and (qb[i + 1][0][1] - qb[i][0][1]) >= -0.01 for i in range(len(qb) - 1))   # the top-left corner only goes down (9.9 -> 20.5), a little a frame
        start_ok = max(abs(x - y) for p_, q_ in zip(qb[0], QA) for x, y in zip(p_, q_)) < 2
    fmv0 = mv[0] if mv else None; ex_end = fend[0] + f_ie["t"] if fend and f_ie else None
    check(f"the camera move starts {P['cam_gap']} ms after the bird has gone (within 150) and lasts {P['cam_ms']} ms (within 100): the overhead table (868:17) drawn through the map that takes its card from 868:3's corners to its own, the angled one through the map that takes ITS card to the same corners, in every frame (within 1.5 px), their dashed borders likewise",
          mv and ex_end and abs(fmv0["t"] - ex_end - P["cam_gap"]) < 150 and abs(dur_mv - P["cam_ms"]) < 100 and start_ok and same is not None and same < 1.5 and samed is not None and samed < 1.5 and mono,
          (round(fmv0["t"] - ex_end) if mv and ex_end else None, round(dur_mv) if mv else None, round(same, 3) if mv and same is not None else None, round(samed, 3) if mv and samed is not None else None, mono if mv else None))
    after = first(tr, lambda f: f["bo"] == "none" and not f["nA"], since=mv[-1]["t"] if mv else 0)
    aops = [f["aOp"] for f in mv if f["aOp"] is not None]
    check("the angled table fades over the overhead one (its opacity only falls, 1 -> 0 by 70 % of the move), its painted sentence hands over to the live one in the first 12 % — the live one fading in where it stood (its ink box on the painted one's) and gliding to its own place; at the end the angled layers, its tray and stamps and the bird are gone and the overhead table stands as drawn (no transform)",
          mv and aops and aops[0] == 1 and all(b_ <= a_ + 1e-6 for a_, b_ in zip(aops, aops[1:])) and min(aops) == 0 and mv[0]["sOp"] < 0.05 and max((f["aTxt"] or 0) for f in mv if f["t"] > mv[0]["t"] + 0.13 * P["cam_ms"]) < 0.01
          and after and after["sOp"] == 1 and boxnear(after["sBox"], [RS[0]["sent"]["x"], RS[0]["sent"]["y"], RS[0]["sent"]["w"], RS[0]["sent"]["h"]], 1.5) and all(imgop(after, k) == 1 for k in range(2)) and after["tray"] == 1,
          (aops[:1] + aops[-1:] if mv else None, mv[0]["sOp"] if mv else None, after["sBox"] if after else None))
    # the overhead view right after the move, against 868:17 outside its box (not shown yet)
    if (REF / "stamp868_17_render.png").exists():
        A_, B_, d17 = diff(z17, REF / "stamp868_17_render.png", "l2_overhead"); m_ = np.ones(d17.shape, bool); m_[220:322, 853:955] = False
        check("after the move the stage IS 868:17 (outside its box, which comes later): the shot against Figma's render, mean difference < 6 of 765", d17[m_].mean() < 6, round(float(d17[m_].mean()), 2))
    if (REF / "stamp868_3_render.png").exists():
        A_, B_, d3 = diff(z3, REF / "stamp868_3_render.png", "l2_angled")
        check("the angled view with the bird landed IS 868:3 (the shot against Figma's render: mean difference < 8 of 765; the painted sentence, the stamps and the bird in their places)", d3.mean() < 8, round(float(d3.mean()), 2))
    # ==== 6. round 1: the sentence read (it came through the move: no rise), the box's blink, the stamps the child's
    sent = snd("vo_stamp_sent"); WE = RS[0]["sentence"].get("word_end"); f_mv_end = mv[-1] if mv else None
    check(f"round 1's sentence is read {P['read_gap']} ms after the move (within 150), once — not rising in (it is there: every word on from the move's start, no rise)",
          len(sent) == 1 and f_mv_end and abs(sent[0]["t"] - f_mv_end["t"] - P["read_gap"]) < 150 and all(f["words"] == len(WT) for f in tr if f["round"] == "0" and mv and mv[0]["t"] <= f["t"] <= sent[0]["t"]) and not any(f["rise"] for f in tr if f["round"] == "0"),
          (round(sent[0]["t"] - f_mv_end["t"]) if sent and f_mv_end else None))
    syn, offw = sent_sync(tr, "vo_stamp_sent", WT, WE, 0)
    check("each word lit as the clip reaches it, one at a time, none after the last word's end ([word-sync], the exact light of before)", len(syn) > 20 and not offw and len({f["hot"] for f in syn if f["hot"] >= 0}) >= len(set(WT)) - 1,
          (len(syn), len(offw), sorted({f["hot"] for f in syn})))
    slotz = lambda f, j: f["slots"][j] if len(f["slots"]) > j else None
    fsl = first(tr, lambda f: slotz(f, 0) and has(slotz(f, 0)["cl"], "in")); f_se = first(tr, lambda f: f["vo"] and f["vo"][0] == "vo_stamp_sent.ogg" and f["vo"][2])
    fbe = first(tr, lambda f: slotz(f, 0) and has(slotz(f, 0)["cl"], "in") and not has(slotz(f, 0)["cl"], "blink"), since=fsl["t"] + 500) if fsl else None
    ops = [slotz(f, 0)["op"] for f in tr if fsl and fbe and fsl["t"] < f["t"] < fbe["t"]]
    dips = sum(1 for a_, b_, c_ in zip(ops, ops[1:], ops[2:]) if b_ < 0.08 and b_ <= a_ and b_ <= c_)
    check(f"the orange box appears as the clip ends (within 300 ms) and blinks for {P['blink_ms'] / 1000:g} s — appearing and disappearing ({P['blinks']} times: stpBoxBlink, its opacity down to under .05 and back) — then stays",
          fsl and fbe and f_se and abs(fsl["t"] - f_se["t"]) < 300 and abs(fbe["t"] - fsl["t"] - P["blink_ms"]) < 150 and slotz(fsl, 0)["anim"] == "stpBoxBlink" and ops and min(ops) < 0.05 and dips == P["blinks"]
          and boxnear(slotz(fsl, 0)["box"], [SL["x"], SL["y"], SL["w"], SL["h"]], 1.5),
          (round(fsl["t"] - f_se["t"]) if fsl and f_se else None, round(fbe["t"] - fsl["t"]) if fbe and fsl else None, slotz(fsl, 0)["anim"] if fsl else None, round(min(ops), 3) if ops else None, dips))
    fli = first(tr, lambda f: f["live"])
    check("the stamps are the child's from the moment the box appears (.live, the drag handles' touch-action none), not before", fli and fsl and abs(fli["t"] - fsl["t"]) < 40 and ta == "none", (T(fli), T(fsl), ta))
    if (REF / "stamp868_17_render.png").exists():
        A_, B_, db17 = diff(zb, REF / "stamp868_17_render.png", "l2_box")
        # [stamp-box] the frame's 90 box is drawn smaller now: the whole frame compared outside that box's square (and 6 px round it);
        # the box itself judged as drawn (its fill, its dashes, nothing orange beyond its 60 px) at its place
        km = np.ones(db17.shape, bool); km[220:322, 853:955] = False
        bok, binfo = box_drawn(A_, SL["x"], SL["y"], SL["w"], SL["h"])
        check("the box moment against Figma's 868:17 render: the whole frame outside the frame's box (mean < 6 of 765); [stamp-box] the box drawn 60x60 at its place (its fill, its dashed stroke, no orange beyond it)", db17[km].mean() < 6 and bok, (round(float(db17[km].mean()), 2), binfo))
    # ==== 7. the guidance: 0.5 s after the blink, the ? stamp glides SLOWLY over the box (its centre onto the box's centre, lifted to 1.1), hovers, glides home
    fh1 = first(tr, lambda f: has(f["cl"][1], "lift"), since=fsl["t"] if fsl else 0)
    fat = min((f for f in tr if fh1 and fh1["t"] <= f["t"] <= fh1["t"] + P["glide"] + 300 and f["st"][1]), key=lambda f: abs(cen(f["st"][1])[0] - sc[0]) + abs(cen(f["st"][1])[1] - sc[1]), default=None)
    fmid = min((f for f in tr if fh1 and f["st"][1]), key=lambda f: abs(f["t"] - (fh1["t"] + P["glide"] * 2 / 3)), default=None)
    dmid = (abs(cen(fmid["st"][1])[0] - sc[0]) + abs(cen(fmid["st"][1])[1] - sc[1])) if fmid else None
    scale_at = fat["st"][1][2] / S1[2] if fat else None
    check("the guidance starts 0.5 s after the blink ends: the ? stamp lifts and glides over the box in 1.5 s (its centre within 4 px of the box's as the glide ends, lifted to 1.1; still 15+ px away two thirds in — a slow glide)",
          fh1 and fbe and abs(fh1["t"] - fbe["t"] - P["hint_at"]) < 150 and fat and abs(fat["t"] - fh1["t"] - P["glide"]) < 200 and near(cen(fat["st"][1]), sc, 4) and abs(scale_at - P["lift_scale"]) < 0.02 and dmid and dmid > 15,
          (round(fh1["t"] - fbe["t"]) if fh1 and fbe else None, round(fat["t"] - fh1["t"]) if fat else None, [round(v, 1) for v in cen(fat["st"][1])] if fat else None, list(sc), round(scale_at, 3) if scale_at else None, round(dmid, 1) if dmid else None))
    fh1e = first(tr, lambda f: not has(f["cl"][1], "lift"), since=fh1["t"] + 500) if fh1 else None
    home = lambda f, k, bx: f["st"][k] and boxnear(f["st"][k], bx, 1.5)
    fhome1 = first(tr, lambda f: home(f, 1, S1), since=fh1["t"] + 1000) if fh1 else None
    thud = snd("sfx_stamp_press"); fm = first(tr, lambda f: f["mark"]); fgn = first(tr, lambda f: slotz(f, 0) and has(slotz(f, 0)["cl"], "gone"))
    check("it hovers there and glides home (set down ~2.9 s after it lifted, its box within 1.5 px of its place) — nothing printed, no thud, the box still there",
          fh1 and fh1e and abs(fh1e["t"] - fh1["t"] - (P["glide"] + P["hold"] + P["back"] - 150)) < 200 and fhome1 and fhome1["t"] < fh1e["t"] + 250 and fm and fm["t"] > t_d3 - 50 and fgn and fgn["t"] > t_d3 and not [x for x in thud if x["t"] < t_d3],
          (round(fh1e["t"] - fh1["t"]) if fh1 and fh1e else None, T(fhome1)))
    fh2 = first(tr, lambda f: has(f["cl"][1], "lift"), since=fh1e["t"] + 100) if fh1e else None
    check("the guidance comes again 7 s after it was set down (within 7.0..7.5 s: the page's 200 ms tick), and not before", fh2 and 6900 < fh2["t"] - fh1e["t"] < 7500, round(fh2["t"] - fh1e["t"]) if fh2 and fh1e else None)
    fg = first(tr, lambda f: has(f["cl"][1], "drag"), since=fh2["t"] if fh2 else 0); ig = tr.index(fg) if fg else -1
    jump = max(abs(cen(tr[ig]["st"][1])[i] - cen(tr[ig - 1]["st"][1])[i]) for i in (0, 1)) if ig > 0 and tr[ig]["st"][1] and tr[ig - 1]["st"][1] else None
    fd1 = first(tr, lambda f: not has(f["cl"][1], "drag"), since=fg["t"] + 100) if fg else None
    moved = (cen(fd1["st"][1])[0] - cen(fg["st"][1])[0], cen(fd1["st"][1])[1] - cen(fg["st"][1])[1]) if fd1 and fg else None
    want_move = (150 - (r[0] + r[2] / 2), 380 - (r[1] + r[3] / 2))
    check("taking hold of the guiding stamp mid-glide stops the guidance where it is (no jump: its centre moves under 10 px across the grab frame) and it follows the finger (its centre moved with the finger within 8 px)",
          fg and 0.5 < (fg["t"] - fh2["t"]) / 1000 < 1.3 and jump is not None and jump < 10 and moved and abs(moved[0] - want_move[0]) < 8 and abs(moved[1] - want_move[1]) < 8,
          (round(fg["t"] - fh2["t"]) if fg and fh2 else None, round(jump, 1) if jump is not None else None, [round(v) for v in moved] if moved else None, [round(v) for v in want_move]))
    wrongs = snd("sfx_wrong_new"); fw1 = first(tr, lambda f: has(f["cl"][1], "stp-wrong"), since=fg["t"]) if fg else None
    fback1 = first(tr, lambda f: home(f, 1, S1) and not has(f["cl"][1], "lift"), since=fd1["t"]) if fd1 else None
    check("dropped far off the box: the incorrect buzz sounds as it lands (within 60 ms), it wiggles there (.stp-wrong, the kit's wgNo on its picture), then glides back to its place (set down within 1.4 s), nothing printed",
          fd1 and fw1 and abs(fw1["t"] - fd1["t"]) < 60 and len(wrongs) >= 1 and abs(wrongs[0]["t"] - fw1["t"]) < 60 and fback1 and fback1["t"] - fd1["t"] < P["wiggle"] + P["reset"] + 450 and not fback1["mark"]
          and pg.evaluate("(() => { const s = document.createElement('div'); s.className = 'stp-stamp stp-wrong'; const i = document.createElement('img'); i.className = 'shown'; s.appendChild(i); document.body.appendChild(s); const a = getComputedStyle(i).animationName; s.remove(); return a; })()") == "wgNo",
          (round(wrongs[0]["t"] - fd1["t"]) if wrongs and fd1 else None, round(fback1["t"] - fd1["t"]) if fback1 and fd1 else None))
    WA = np.asarray(Image.open(wshot).convert("RGB").resize((1280, 720), Image.LANCZOS)).astype(float); wx, wy, ww, wh_ = [int(round(v)) for v in wbox]
    corner = WA[wy + 1:wy + 6, wx + 1:wx + 6].mean(); beside = WA[wy:wy + wh_, max(0, wx - 14 - 12):wx - 14].mean()
    check("no white box behind a stamp dropped on the bare wood: its element's background stays transparent while it wiggles, and the corner of its box in the shot is the wood's colour (not white)",
          wbg in ("rgba(0, 0, 0, 0)", "transparent") and corner < 215 and abs(corner - beside) < 30, (wbg, round(corner, 1), round(beside, 1)))
    fg2 = first(tr, lambda f: has(f["cl"][0], "drag"), since=fd1["t"] if fd1 else 0); fd2 = first(tr, lambda f: not has(f["cl"][0], "drag"), since=fg2["t"] + 100) if fg2 else None
    c2 = cen(tr[tr.index(fd2) - 1]["st"][0]) if fd2 else None
    fback2 = first(tr, lambda f: home(f, 0, S0) and not has(f["cl"][0], "lift"), since=fd2["t"]) if fd2 else None
    check("the । stamp dropped ON the box (its centre on the box's centre): the incorrect buzz, the wiggle, back to its place — nothing printed, the box still there",
          fd2 and near(c2, sc, 6) and len(wrongs) >= 2 and abs(wrongs[1]["t"] - fd2["t"]) < 60 and first(tr, lambda f: has(f["cl"][0], "stp-wrong"), since=fd2["t"] - 20)
          and fback2 and fback2["t"] - fd2["t"] < P["wiggle"] + P["reset"] + 450 and not fback2["mark"] and not has(slotz(fback2, 0)["cl"], "gone"),
          ([round(v) for v in c2] if c2 else None, round(wrongs[1]["t"] - fd2["t"]) if len(wrongs) > 1 and fd2 else None, round(fback2["t"] - fd2["t"]) if fback2 and fd2 else None))
    ftap = first(tr, lambda f: has(f["cl"][1], "drag"), since=fback2["t"]) if fback2 else None
    fafter = min((f for f in tr if ftap and f["st"][1]), key=lambda f: abs(f["t"] - (ftap["t"] + 400)), default=None)
    check("a tap on a stamp (a move under 10 px) is a touch, not a placing: no buzz, the stamp is set back down where it is", ftap and len([x for x in wrongs if ftap["t"] < x["t"] < t_d3]) == 0 and fafter and home(fafter, 1, S1) and not has(fafter["cl"][1], "lift"),
          (T(ftap), [round(v, 1) for v in fafter["st"][1]] if fafter else None))
    fg3 = first(tr, lambda f: has(f["cl"][1], "drag"), since=ftap["t"] + 300) if ftap else None; fd3 = first(tr, lambda f: not has(f["cl"][1], "drag"), since=fg3["t"] + 100) if fg3 else None
    win = [f for f in tr if fd3 and fd3["t"] <= f["t"] <= fd3["t"] + P["snap"] + P["press"] + 300 and f["st"][1]]
    fpress = min(win, key=lambda f: abs(cen(f["st"][1])[0] - sc[0]) + abs(cen(f["st"][1])[1] - sc[1]) + abs(f["st"][1][2] / S1[2] - P["press_scale"]) * 100) if win else None
    c3 = cen(fpress["st"][1]) if fpress else None; cd = cen(tr[tr.index(fd3) - 1]["st"][1]) if fd3 else None
    check("the ? stamp dropped on the box (its centre 30 px right, 20 px low of the box's) snaps over it and presses: its centre on the box's (within 4 px), pressed to .96, ~0.36 s after the drop",
          fd3 and near(cd, (sc[0] + 30, sc[1] + 20), 8) and fpress and abs(fpress["t"] - fd3["t"] - (P["snap"] + P["press"])) < 150 and near(c3, sc, 4) and abs(fpress["st"][1][2] / S1[2] - P["press_scale"]) < 0.02,
          ([round(v) for v in cd] if cd else None, round(fpress["t"] - fd3["t"]) if fpress and fd3 else None, [round(v, 1) for v in c3] if c3 else None, round(fpress["st"][1][2] / S1[2], 3) if fpress else None))
    thud1 = [x for x in thud if fd3 and x["t"] < fd3["t"] + 2000]
    check("the stamp thud sounds as it presses (0.28 s after the drop), [stamp-box] at .54 (every one of the page's thuds: 40 % below the .9 it was), and the mark is printed at 0.4 s", len(thud1) == 1 and fd3 and abs(thud1[0]["t"] - fd3["t"] - P["thud_at"]) < 80 and fm and abs(fm["t"] - fd3["t"] - P["mark_at"]) < 80
          and thud and all(abs(x["vol"] - 0.54) < 0.005 for x in thud),
          (round(thud1[0]["t"] - fd3["t"]) if thud1 and fd3 else None, round(fm["t"] - fd3["t"]) if fm and fd3 else None, sorted(set(round(x["vol"], 3) for x in thud))))
    fh3 = first(tr, lambda f: home(f, 1, S1) and not has(f["cl"][1], "lift"), since=fm["t"]) if fm else None
    check("the stamp lifts and glides back to its place in the tray (within 1.5 px), set down by 1.8 s after the drop", fh3 is not None and fh3["t"] - fd3["t"] < P["back_at"] + P["back_home"] + 200, round(fh3["t"] - fd3["t"]) if fh3 else None)
    corr = snd("sfx_correct_new"); corr1 = [x for x in corr if fd3 and x["t"] < fd3["t"] + 3000]
    check("the box goes 1.6 s after the drop, on the correct chime (within 60 ms), and the mark stays while the round lasts",
          fgn and fd3 and abs(fgn["t"] - fd3["t"] - P["gone_at"]) < 100 and len(corr1) == 1 and abs(corr1[0]["t"] - fgn["t"]) < 60 and first(tr, lambda f: f["t"] > fgn["t"] + 2000)["mark"],
          (round(fgn["t"] - fd3["t"]) if fgn and fd3 else None, round(corr1[0]["t"] - fgn["t"]) if corr1 and fgn else None))
    fcf = first(tr, lambda f: f["conf"]); cel = [x for x in snd("sfx_celebrate") if fd3 and x["t"] < fd3["t"] + 3500]
    check("confetti comes 2.1 s after the drop, on its own sound (within 100 ms)", fcf and fd3 and abs(fcf["t"] - fd3["t"] - P["confetti_at"]) < 180 and len(cel) == 1 and abs(cel[0]["t"] - fcf["t"]) < 180,
          (round(fcf["t"] - fd3["t"]) if fcf and fd3 else None, round(cel[0]["t"] - fcf["t"]) if cel and fcf else None))
    # the printed mark: across on the box's centre, standing on its row's baseline (the row's ink headline as on the render; the mark's ink
    # within the row's ink band, its bottom on the row's — the danda / ? stand on the baseline as the letters do)
    # the row's baseline as CSS lays it: the line box's top + the half leading + the font's ascent ('Story Baloo 2': Noto's 0.896 / 0.408 em)
    baseline = lambda se_, row: se_["y"] + row * se_["lh"] + (se_["lh"] - 1.304 * se_["size"]) / 2 + 0.896 * se_["size"]
    DN = Image.open(done).convert("RGB").resize((1280, 720), Image.LANCZOS); b1 = baseline(RS[0]["sent"], SL.get("row", 0))
    mk_ink = ink(DN, SL["x"] + 2, SL["y"] + 2, SL["x"] + SL["w"] - 2, SL["y"] + SL["h"] - 2)   # [stamp-box] inside the box (was + 88: the 90 box)
    check("the printed ? stands in the box across its centre (its ink's middle within 3 px of the box's) and on the sentence's baseline, as if typed there (its foot within 3 px of it)",
          mk_ink and abs((mk_ink[0] + mk_ink[2]) / 2 - sc[0]) < 3 and abs(mk_ink[3] - b1) <= 3, (mk_ink, round(b1, 1), sc))
    lifts1 = [tr[i]["t"] for i in range(1, len(tr)) if has(tr[i]["cl"][1], "lift") and not has(tr[i - 1]["cl"][1], "lift")]
    # ==== 8. [stamp-rounds] each later round: the clearing, the round set, its line, its pops, its sentence, its boxes; no guidance,
    #         the round's line again after 7 s; the wrong drop; the right drops; the boxes gone, confetti
    prev_drop = fd3; prev_n = len(RS[0]["stamps"]); pops = snd("sfx_stamp_pop")
    popping = lambda f, k: "pop" in imgcls(f, k) or "shown" in imgcls(f, k)
    for L_ in LT:
        ri = L_["ri"]; R = RS[ri]; g = G[ri]; SLS, SCS = g["SLS"], g["SCS"]; nsl = len(SLS); WTr = R["sentence"]["word_times"]; n = len(R["stamps"]); wk = L_["wrong"]; PKS, MKS = g["PKS"], g["MKS"]
        unp = lambda f, k: "unpop" in imgcls(f, k)
        fu = [first(tr, lambda f, k=k: unp(f, k), since=prev_drop["t"]) for k in range(prev_n)] if prev_drop else []
        fr = first(tr, lambda f: f["round"] == str(ri))
        check(f"round {ri} -> {ri + 1}: 4.4 s after the drop its {prev_n} stamps shrink away (their pop backwards, 350 ms apart, no pop sound), the sentence goes word by word in reverse, the box fades with its mark",
              all(fu) and abs(fu[0]["t"] - prev_drop["t"] - P["done_at"]) < 180 and all(abs(fu[k]["t"] - fu[k - 1]["t"] - P["pop_gap"]) < 110 for k in range(1, prev_n)) and not [x for x in pops if fu[0]["t"] - 200 < x["t"] < (fr["t"] if fr else 1e12) - 20]
              and first(tr, lambda f: f["words"] == 0, since=fu[0]["t"]) and first(tr, lambda f: f["slots"] and all(s_["op"] < 0.05 for s_ in f["slots"]), since=fu[0]["t"]),
              ([round(f["t"] - prev_drop["t"]) for f in fu] if all(fu) else None))
        boxes_ok = lambda f: f and len(f["slots"]) == nsl and all(boxnear(f["slots"][j]["box"], [SLS[j]["x"], SLS[j]["y"], SLS[j]["w"], SLS[j]["h"]], 1.5) for j in range(nsl))
        check(f"1.3 s into the clearing round {ri + 1} ({R['frame']}) is set: its sentence built ({len(WTr)} words, none shown), {nsl} empty box{'es' if nsl > 1 else ''} at {'their' if nsl > 1 else 'its'} place, {n} stamp divs with the round's pictures at the frame's boxes",
              fr and fu and abs(fr["t"] - fu[0]["t"] - P["next_at"]) < 120 and fr["nwords"] == len(WTr) and fr["words"] == 0 and not any(has(s_["cl"], "in") for s_ in fr["slots"]) and not fr["mark"] and shown_n(fr) == n
              and all(imgsrc(fr, k) == R["stamps"][k] + ".webp" for k in range(n)) and all(boxnear(fr["st"][k], R["boxes"][k], 1.5) for k in range(n)) and boxes_ok(fr),
              (round(fr["t"] - fu[0]["t"]) if fr and fu else None, [imgsrc(fr, k) for k in range(len(fr["imgs"]))] if fr else None, [[round(v, 1) for v in s_["box"]] for s_ in fr["slots"]] if fr else None))
        clipI = R.get("intro_audio") or "vo_stamp_intro"; introR = snd(clipI); voiR = lambda f, c=clipI: f["vo"] and f["vo"][0] == c + ".ogg"
        t_pop0 = fr["t"] if fr else 0   # [l2-quiet] no line first: the round's stamps pop in as it is set
        fpr = [first(tr, lambda f, k=k: popping(f, k), since=fr["t"]) for k in range(n)] if fr else [None] * n; popsr = [x for x in pops if fr and t_pop0 - 50 < x["t"] < t_pop0 + n * P["pop_gap"] + 500]
        fslr0 = first(tr, lambda f: len(f["slots"]) == nsl and all(has(s_["cl"], "in") for s_ in f["slots"]), since=fr["t"]) if fr else None
        opened = [x for x in introR if fr and fslr0 and fr["t"] - 100 < x["t"] < fslr0["t"]]   # the round's line played from its setting to its boxes' appearance
        check(f"round {ri + 1}: [l2-quiet] NO line as the round opens (its {clipI} not played from the round's setting to its boxes) — its {n} stamps pop in at once, 350 ms apart, each on its pop",
              fr and fslr0 and not opened and all(fpr) and len(popsr) == n and abs(fpr[0]["t"] - t_pop0) < 150 and all(abs(fpr[k]["t"] - fpr[k - 1]["t"] - P["pop_gap"]) < 110 for k in range(1, n))
              and all(abs(popsr[k]["t"] - fpr[k]["t"]) < 60 for k in range(n)), ([round(f["t"] - t_pop0) for f in fpr] if all(fpr) and fr else None, [round(x["t"] - fr["t"]) for x in opened] if fr else None))
        clip = R["sentence"]["audio"]; sentr = snd(clip); WEr = R["sentence"].get("word_end")
        fwr0 = first(tr, lambda f: f["words"] > 0 and f["round"] == str(ri), since=fr["t"]) if fr else None
        f_er = first(tr, lambda f: f["vo"] and f["vo"][0] == clip + ".ogg" and f["vo"][2], since=fr["t"] if fr else 0)
        rw = sorted({f["words"] for f in tr if f["round"] == str(ri) and (not fr or f["t"] >= fr["t"]) and (not f_er or f["t"] <= f_er["t"])})
        synr, offr = sent_sync(tr, clip, WTr, WEr, fr["t"] if fr else 0)
        check(f"round {ri + 1}'s sentence rises in whole 0.7 s after the last pop, its clip ~0.45 s after that, each word lit as the clip reaches it ([word-sync])",
              len(sentr) == 1 and all(fpr) and fwr0 and abs(fwr0["t"] - fpr[-1]["t"] - P["sent_at"]) < 150 and 400 <= sentr[0]["t"] - fwr0["t"] <= 800 and set(rw) <= {0, len(WTr)} and len(synr) > 20 and not offr,
              (round(fwr0["t"] - fpr[-1]["t"]) if fwr0 and all(fpr) else None, round(sentr[0]["t"] - fwr0["t"]) if sentr and fwr0 else None, rw, len(synr), len(offr)))
        fslr = first(tr, lambda f: len(f["slots"]) == nsl and all(has(s_["cl"], "in") for s_ in f["slots"]), since=fr["t"]) if fr else None
        fber = first(tr, lambda f: len(f["slots"]) == nsl and all(has(s_["cl"], "in") and not has(s_["cl"], "blink") for s_ in f["slots"]), since=fslr["t"] + 500) if fslr else None
        opsr = [min(s_["op"] for s_ in f["slots"]) for f in tr if fslr and fber and fslr["t"] < f["t"] < fber["t"]]
        flir = first(tr, lambda f: f["live"], since=fr["t"]) if fr else None
        check(f"round {ri + 1}: {'the box' if nsl == 1 else 'all ' + str(nsl) + ' boxes, together,'} appear{'s' if nsl == 1 else ''} as the clip ends and blink{'s' if nsl == 1 else ''} 3 s (stpBoxBlink, down to under .05); the stamps the child's again",
              fslr and fber and f_er and abs(fslr["t"] - f_er["t"]) < 300 and abs(fber["t"] - fslr["t"] - P["blink_ms"]) < 150 and all(s_["anim"] == "stpBoxBlink" for s_ in fslr["slots"]) and opsr and min(opsr) < 0.05 and boxes_ok(fslr) and flir and abs(flir["t"] - fslr["t"]) < 40,
              (round(fslr["t"] - f_er["t"]) if fslr and f_er else None, round(fber["t"] - fslr["t"]) if fber and fslr else None, round(min(opsr), 3) if opsr else None))
        fgw = first(tr, lambda f: has(f["cl"][wk], "drag"), since=fslr["t"]) if fslr else None; fdw = first(tr, lambda f: not has(f["cl"][wk], "drag"), since=fgw["t"] + 100) if fgw else None
        rem = [x for x in introR if fslr and fgw and fslr["t"] < x["t"] < fgw["t"]]
        nolift = fr and fgw and not [f for f in tr if fr["t"] < f["t"] < fgw["t"] and any(has(c_, "lift") for c_ in f["cl"])]
        check(f"round {ri + 1}: NO guidance — no stamp lifts before the child's own drop; 7 s after the box{'es' if nsl > 1 else ''} appeared without a touch (7.0..7.6 s) the round's own line ({clipI}) is said again, once",
              nolift and len(rem) == 1 and 6900 < rem[0]["t"] - fslr["t"] < 7600, (round(rem[0]["t"] - fslr["t"]) if rem and fslr else None, len(rem), "" if nolift else "a stamp lifted before the drop"))
        wr = [x for x in wrongs if fdw and abs(x["t"] - fdw["t"]) < 150]
        fbackw = first(tr, lambda f: home(f, wk, g["bx"][wk]) and not has(f["cl"][wk], "lift"), since=fdw["t"]) if fdw else None
        check(f"round {ri + 1}: the wrong stamp (#{wk}) dropped on the box: the incorrect buzz (within 60 ms), the wiggle, back to its place — nothing printed",
              fdw and len(wr) == 1 and abs(wr[0]["t"] - fdw["t"]) < 60 and first(tr, lambda f: has(f["cl"][wk], "stp-wrong"), since=fdw["t"] - 20) and fbackw and fbackw["t"] - fdw["t"] < P["wiggle"] + P["reset"] + 450 and not fbackw["mark"],
              (round(wr[0]["t"] - fdw["t"]) if wr and fdw else None, round(fbackw["t"] - fdw["t"]) if fbackw and fdw else None))
        since_ = fdw["t"] if fdw else 0; fdrs = []
        for j in range(nsl):
            SLj, scj = SLS[j], SCS[j]; ox, oy = L_["offs"][j]; pk, mk = PKS[j], MKS[j]; tag = f"round {ri + 1}" + (f", box {j + 1}" if nsl > 1 else "")
            fgr = first(tr, lambda f: has(f["cl"][pk], "drag"), since=since_); fdr = first(tr, lambda f: not has(f["cl"][pk], "drag"), since=fgr["t"] + 100) if fgr else None
            winr = [f for f in tr if fdr and fdr["t"] <= f["t"] <= fdr["t"] + P["snap"] + P["press"] + 300 and f["st"][pk]]
            fpressr = min(winr, key=lambda f: abs(cen(f["st"][pk])[0] - scj[0]) + abs(cen(f["st"][pk])[1] - scj[1]) + abs(f["st"][pk][2] / g["bx"][pk][2] - P["press_scale"]) * 100) if winr else None
            cr_ = cen(fpressr["st"][pk]) if fpressr else None; cdr = cen(tr[tr.index(fdr) - 1]["st"][pk]) if fdr else None
            fmr = first(tr, lambda f: slotz(f, j) and slotz(f, j)["mark"], since=fr["t"]) if fr else None; thudr = [x for x in thud if fdr and abs(x["t"] - fdr["t"] - P["thud_at"]) < 400]
            check(f"{tag}: the {mk} stamp dropped on the box ({ox:+} px, {oy:+} px off its centre) snaps over it and presses (its centre on the box's within 4 px, at .96); the thud at 0.28 s, the mark printed there at 0.4 s",
                  fdr and near(cdr, (scj[0] + ox, scj[1] + oy), 8) and fpressr and near(cr_, scj, 4) and abs(fpressr["t"] - fdr["t"] - (P["snap"] + P["press"])) < 150
                  and len(thudr) == 1 and abs(thudr[0]["t"] - fdr["t"] - P["thud_at"]) < 80 and fmr and abs(fmr["t"] - fdr["t"] - P["mark_at"]) < 80,
                  ([round(v) for v in cdr] if cdr else None, [round(v, 1) for v in cr_] if cr_ else None, list(scj), round(thudr[0]["t"] - fdr["t"]) if thudr and fdr else None, round(fmr["t"] - fdr["t"]) if fmr and fdr else None))
            fhr = first(tr, lambda f: home(f, pk, g["bx"][pk]) and not has(f["cl"][pk], "lift"), since=fmr["t"]) if fmr else None
            fgnr = first(tr, lambda f: slotz(f, j) and has(slotz(f, j)["cl"], "gone"), since=fr["t"]) if fr else None; corrr = [x for x in corr if fdr and fdr["t"] < x["t"] < fdr["t"] + 2500]
            check(f"{tag}: the stamp glides home (by 1.8 s); the box goes at 1.6 s on the correct chime (within 60 ms)", fhr and fdr and fhr["t"] - fdr["t"] < P["back_at"] + P["back_home"] + 200 and fgnr and abs(fgnr["t"] - fdr["t"] - P["gone_at"]) < 100
                  and len(corrr) == 1 and abs(corrr[0]["t"] - fgnr["t"]) < 60, (round(fhr["t"] - fdr["t"]) if fhr and fdr else None, round(fgnr["t"] - fdr["t"]) if fgnr and fdr else None))
            DNr = Image.open(L_["dones"][j]).convert("RGB").resize((1280, 720), Image.LANCZOS); mi = ink(DNr, SLj["x"] + 2, SLj["y"] + 2, SLj["x"] + SLj["w"] - 2, SLj["y"] + SLj["h"] - 2)   # [stamp-box] inside the box (was + 88)
            bj = baseline(R["sent"], SLj.get("row", 0))
            ok_mark = mi and abs((mi[0] + mi[2]) / 2 - scj[0]) < 3 and ((mi[1] < bj - 2 and mi[3] > bj + 2) if mk == "," else abs(mi[3] - bj) <= 3)
            how = "crossing it: its head above, its tail below" if mk == "," else "its foot within 3 px of it"
            check(f"{tag}: the printed {mk} stands in the box across its centre (its ink's middle within 3 px of the box's) and on its row's baseline, as if typed there ({how})",
                  ok_mark, (mi, round(bj, 1), scj))
            if j < nsl - 1:
                fre = first(tr, lambda f: f["live"], since=fdr["t"] + 500) if fdr else None
                celx = [x for x in snd("sfx_celebrate") if fdr and fdr["t"] < x["t"] < fdr["t"] + 3000]; confx = [f for f in tr if fdr and fdr["t"] < f["t"] < fdr["t"] + 3000 and f["conf"]]
                check(f"{tag}: with box {j + 2} still empty — NO confetti after this drop; the stamps are the child's again as the box goes (1.6 s, within 100 ms)",
                      fre and abs(fre["t"] - fdr["t"] - P["gone_at"]) < 100 and not celx and not confx, (round(fre["t"] - fdr["t"]) if fre and fdr else None, len(celx), len(confx)))
                since_ = fdr["t"] + 100
            fdrs.append(fdr)
        fdr = fdrs[-1]
        fcfr = first(tr, lambda f: f["conf"], since=fdr["t"]) if fdr else None; celr = [x for x in snd("sfx_celebrate") if fdr and fdr["t"] < x["t"] < fdr["t"] + P["done_at"] - 300]
        check(f"round {ri + 1}: confetti 2.1 s after the {'last ' if nsl > 1 else ''}drop, on its own sound (within 100 ms)", fcfr and fdr and abs(fcfr["t"] - fdr["t"] - P["confetti_at"]) < 180 and len(celr) == 1 and abs(celr[0]["t"] - fcfr["t"]) < 180,
              (round(fcfr["t"] - fdr["t"]) if fcfr and fdr else None, round(celr[0]["t"] - fcfr["t"]) if celr and fcfr else None))
        nxt = first(tr, lambda f: f["round"] == str(ri + 1)); t_hi = nxt["t"] if nxt else 1e12
        liftsr = {k: len([i for i in range(1, len(tr)) if fr and fr["t"] < tr[i]["t"] < t_hi and has(tr[i]["cl"][k], "lift") and not has(tr[i - 1]["cl"][k], "lift")]) for k in range(n)}
        expl = {k: sum(1 for j in range(nsl) if PKS[j] == k) + (1 if k == wk else 0) for k in range(n)}
        check(f"round {ri + 1}: each stamp lifted only in the child's hand — once per box it is right for, plus the wrong drop's: {expl}", liftsr == expl, liftsr)
        # the box moment against the frame's render (the blink paused at full opacity): the frame, each row's ink, the boxes
        rp = REF / ("stamp868_%s_render.png" % R["frame"].split(":")[1])
        if rp.exists():
            A2, B2, d2 = diff(L_["z"], rp, f"l2_r{ri}_box")
            # [stamp-box] both the frame's 90 boxes and the page's smaller ones masked out of the rows; a row holding a box between two
            # words (mid) is BOXD narrower than the render's: its ends BOXD / 2 in on each side; the whole frame compared outside the boxes
            # (the frame's, 6 px round them) and those rows; each box judged as drawn at its place
            figb = [(fx, fy, 90, 90) for (fx, fy, _) in FIG[ri]]; ours = [(s_["x"], s_["y"], s_["w"], s_["h"]) for s_ in SLS]
            mine, theirs = rows_of(A2, figb + ours), rows_of(B2, figb + ours)
            mid_rows = [t_ for t_ in theirs if any(mid and fy < t_[1] and t_[0] < fy + 90 for (fx, fy, mid) in FIG[ri])]
            sh = lambda t_: BOXD / 2 if t_ in mid_rows else 0
            okr = len(mine) == len(theirs) and all(abs(m_[2] - t_[2]) <= 1 and abs(m_[3] - t_[3] - sh(t_)) <= 3 and abs(m_[4] - t_[4] + sh(t_)) <= 3 for m_, t_ in zip(mine, theirs))
            km = np.ones(d2.shape, bool)
            for (fx, fy, _, _) in figb: km[max(0, fy - 6):fy + 96, max(0, fx - 6):fx + 96] = False
            for t_ in mid_rows: km[max(0, t_[0] - 6):t_[1] + 7, :] = False
            bdr = [box_drawn(A2, *b_) for b_ in ours]
            check(f"round {ri + 1} against Figma's {R['frame']} render: the whole frame close outside its boxes (mean < 6 of 765), every text row's ink where the render's is (its headline within 1 px, its ends within 3 px; [stamp-box] a row with a box between two words {BOXD // 2} px in at each end), every box drawn 60x60 at its place (its fill, its dashes, no orange beyond it)",
                  d2[km].mean() < 6 and okr and all(b_[0] for b_ in bdr), (round(float(d2[km].mean()), 2), [(m_[2], m_[3], m_[4]) for m_ in mine], "render:", [(t_[2], t_[3], t_[4]) for t_ in theirs], [b_[1] for b_ in bdr]))
        L_["fdr"] = fdr; prev_drop = fdr; prev_n = n
    fr1 = first(tr, lambda f: f["round"] == "1")
    check("the right-hand stamp lifted four times in round 1 (two guidances, the far drop, the right drop): no guidance while the child was at work", fr1 and len([t for t in lifts1 if t < fr1["t"]]) == 4, len([t for t in lifts1 if fr1 and t < fr1["t"]]))
    # ==== 9. [stamp-close] after the last round's confetti: L1's envelope transition backwards, then 792:1253 with the glitter (stamp_close_check.py
    #      has every beat against L1's own, frame by frame); here: its moment, its layer under the full veil, its sounds, the landing, the glitter
    C_ = P["close"]; T_ = C_["zoom"] + C_["done_at"]; R0_ = P["close_hold"] - (T_ - (C_["zoom"] + C_["veil_at"] + C_["veil_ms"])); m_ = lambda t: R0_ + T_ - t
    fdl = LT[-1]["fdr"]; vf = first(tr, lambda f: f["veil"] > 0.01, since=fdl["t"]) if fdl else None; ff = first(tr, lambda f: f["fin"] is not None, since=fdl["t"]) if fdl else None
    papsnd = [x for x in snd("sfx_letter_paper") if fdl and x["t"] > fdl["t"]]; glsnd = [x for x in snd("sfx_stamp_glitter") if fdl and x["t"] > fdl["t"]]; finsnd = [x for x in snd("sfx_stamp_final") if fdl and x["t"] > fdl["t"]]
    check("the finale begins 4.4 s after the last drop (the old finale's moment): the veil falls over the table, and the envelope's layer (L1's end state: zoomed, open, the sheet up, dived in) goes in only under the full veil",
          vf and fdl and abs(vf["t"] - fdl["t"] - P["done_at"]) < 260 and ff and ff["veil"] > 0.999 and all(c_ in ff["fin"]["cls"].split() for c_ in ("ltr", "ltr-rev", "zoom", "letter-in", "paper", "dive")),
          (round(vf["t"] - fdl["t"]) if vf and fdl else None, ff["veil"] if ff else None, ff["fin"]["cls"] if ff else None))
    fz = first(tr, lambda f: f["fin"] and "zoom" not in f["fin"]["cls"].split(), since=ff["t"]) if ff else None; fl_ = first(tr, lambda f: f["fin"] and "land" in f["fin"]["cls"].split(), since=ff["t"]) if ff else None
    check("then backwards, step by step (the classes taken back: dive, paper; shut and seal; zoom; then land) — the paper crackle once at .7 after the flap starts down, the glitter's chime once at .7, no dissolve chime",
          ff and fz and fl_ and fz["t"] < fl_["t"] and len(papsnd) == 1 and papsnd[0]["vol"] == 0.7 and papsnd[0]["t"] > ff["t"] and len(glsnd) == 1 and glsnd[0]["vol"] == 0.7 and not finsnd,
          (round(papsnd[0]["t"] - ff["t"]) if papsnd and ff else None, round(glsnd[0]["t"] - ff["t"]) if glsnd and ff else None, len(finsnd)))
    fg_ = first(tr, lambda f: f["fin"] and f["fin"]["sparks"] > 0, since=ff["t"]) if ff else None; EB = LY["envelope"]
    check(f"the envelope in her hand glitters gold, as before: {P['fin_sparks']} sparks and the glow over its box {EB}, {P['fin_glitter_at']} ms after it lands (within 120), with its chime (within 60 ms)",
          fg_ and fl_ and abs(fg_["t"] - fl_["t"] - P["land_lead"] - P["fin_glitter_at"]) < 120 and fg_["fin"]["sparks"] == P["fin_sparks"] and fg_["fin"]["glow"] == "stpGlow" and boxnear(fg_["fin"]["gbox"], EB, 1.5) and glsnd and abs(glsnd[0]["t"] - fg_["t"]) < 60,
          (round(fg_["t"] - fl_["t"]) if fg_ and fl_ else None, fg_["fin"]["sparks"] if fg_ else None))
    FS = np.asarray(Image.open(fin_shot).convert("RGB").resize((1280, 720), Image.LANCZOS)).astype(float); FR = np.asarray(Image.open(final_render).convert("RGB")).astype(float) if final_render.exists() else None
    dfin = float(np.abs(FS - FR).sum(axis=2).mean()) if FR is not None else None
    check("once it has landed the whole stage IS Figma 792:1253 (the shot against its render: mean < 8 of 765), its picture 792:1253's", dfin is not None and dfin < 8 and ff and ff["fin"]["src"] == "img_stamp_final_pinki.webp", round(dfin, 2) if dfin is not None else "no render")
    check(f"then the page hands over to the end screen fin_done after the glitter (completeSlide on the page's own clock: {m_(0) + P['fin_glitter_at'] + P['fin_glitter_ms'] + P['fin_done']} ms after the layer goes in, within 150 ms), the end screen up within 1.5 s of that, no round gate",
          ff and cs_t and abs(cs_t - ff["t"] - (m_(0) + P["fin_glitter_at"] + P["fin_glitter_ms"] + P["fin_done"])) < 150 and 0 <= t_cel - cs_t < 1500 and not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"),
          (round(cs_t - ff["t"]) if ff and cs_t else None, round(t_cel - cs_t) if cs_t else None))
    until(t_cel, 800); shot(pg, "l2_end.png"); pl = pg.evaluate(PLAYS); own = [x for x in pl if x["src"].startswith("sfx_stamp") or x["src"] == "sfx_letter_paper.ogg"]
    check("leaving the page stopped its own sounds (the whoosh twice, the pops 2 + 3 + 3 + 3 for the later rounds, the thud nine times: once a box, [stamp-close] the finale's paper crackle and glitter chime)", len(own) == 24 and all(x["paused"] for x in own),
          sorted(__import__("collections").Counter(x["src"] for x in own).items()))
    # ==== 10. a re-run, and leaving mid-way (the dev nav) with a stamp in hand: a clean stop
    # the re-run also measures the page's smoothness bare: only its frames' times (no reads), from the mount to the box
    pg.evaluate("window._plays = []"); pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'L2'))")
    pg.evaluate("() => { window._ft = []; const t0 = performance.now(); const f = (n) => { window._ft.push(n - t0); if(!document.querySelector('.stp-slot.in')) requestAnimationFrame(f); }; requestAnimationFrame(f); }")
    pg.wait_for_timeout(2500)
    check("a re-run from the end screen starts the page over (the angled table, the bird come in, round 1 set)", pg.evaluate("!!document.querySelector('.stp .stp-a') && !!document.querySelector('.stp-bird') && document.querySelector('.stp').dataset.round === '0'") and len(pg.evaluate(PLAYS)) >= 1)
    pg.wait_for_function("!!document.querySelector('.stp-slot.in')", timeout=30000, polling=500); ft = pg.evaluate("window._ft")
    fg_gaps = [(round(ft[i]), round(ft[i + 1] - ft[i], 1)) for i in range(len(ft) - 1) if ft[i] > 450]
    check("the intro, the bird, the glow, the exit and the camera move run smoothly (the re-run's own frames, nothing read from the page: no gap over 50 ms after the veil's first 0.45 s)", fg_gaps and max(g_[1] for g_ in fg_gaps) < 50,
          (len(ft), max(fg_gaps, key=lambda g_: g_[1]) if fg_gaps else None))
    pg.wait_for_function("!!document.querySelector('.stp.live')", timeout=30000); xt, yt = fp(*g1); pg.mouse.move(xt, yt); pg.mouse.down(); pg.mouse.move(xt + 60, yt - 80); pg.wait_for_timeout(100)
    held = pg.evaluate("document.querySelector('.stp-stamp.s1').className")
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'P2'))"); pg.wait_for_timeout(500); pg.mouse.up(); pg.wait_for_timeout(300); pl = pg.evaluate(PLAYS)
    check("leaving mid-way (to P2) with a stamp in hand: the page's sounds stop, its hook and timers are cleared, its scene is gone, no error", "drag" in held.split() and all(x["paused"] for x in pl if "stamp" in x["src"])
          and pg.evaluate("window.oceanCleanup == null") and pg.evaluate("!document.querySelector('.stp')"), (held, [(x["src"], x["paused"]) for x in pl if "stamp" in x["src"]]))
    check("no page errors", not errs, errs[:3])
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
