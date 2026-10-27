"""The letter page L1 ([letter-fig]): mounted straight (as the dev nav would), the whole scene plays by itself and its sounds
start with their visual beats; the envelope waits for the tap, zooms to 610:6, opens and hands over to the end screen.
usage: python -I -X utf8 letter_check.py <index.html> <outdir> [<dir with render_538-39.png render_558-2.png render_610-6.png>]
Screenshots: l1_a.png (538:2), l1_b.png (538:35), l1_grandpa.png (538:39), l1_hum.png (the chime's "ummm": the pensive girl, no cloud),
l1_grow.png (0.5 s after its "aahaha": the white cloud and the letter growing in together), l1_letter.png (558:2), l1_zoom.png (610:6), l1_open.png, l1_end.png; with the renders, *_diff.png and the pixel numbers. Samples are taken at set moments of the PAGE's clock
(performance.now() since the mount), so screenshot time does not drift them."""
import sys, json, pathlib
from playwright.sync_api import sync_playwright
html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
refs = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)
LEAVE = """() => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); }"""
# every media play, with its moment: Audio elements the page creates (the engine's VO/sfx and the page's own sounds)
HOOK = """(() => { window._plays = []; const P = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function(){ try{ window._plays.push({ src: String(this.src || '').split('/').pop().split('?')[0], t: performance.now(), loop: this.loop, el: this }); }catch(e){} return P.apply(this, arguments); }; })()"""
STATE = """() => { const r = document.querySelector('.ltr'); if(!r) return null; const cs = (sel, p) => { const e = document.querySelector(sel); return e ? getComputedStyle(e)[p] : null; };
  const env = document.querySelector('.ltr-env-pos'), st = document.getElementById('stage'), sr = st.getBoundingClientRect(), k = sr.width / 1333;
  const fr = (e) => { const b = e.getBoundingClientRect(); const s = 1333 / 1280 * k; return { x: (b.left - sr.left) / s, y: (b.top - sr.top) / s, w: b.width / s, h: b.height / s }; };
  return { cls: r.className, slide: CARD.slides[state.idx].id, bOp: +cs('.ltr-scene.b', 'opacity'), cOp: +cs('.ltr-scene.c', 'opacity'), cloudOp: +cs('.ltr-cloud', 'opacity'),
    cloudCls: (document.querySelector('.ltr-cloud') || {}).className || '', growOp: +cs('.ltr-env-grow', 'opacity'), growTf: cs('.ltr-env-grow', 'transform'),
    cgOp: +cs('.ltr-cloud .ltr-cg', 'opacity'), cwOp: +cs('.ltr-cloud .ltr-cw', 'opacity'), blurOp: +cs('.ltr-blur', 'opacity'),
    bubs: [...document.querySelectorAll('.ltr-bub')].map(b => +getComputedStyle(b).opacity), pulseOp: +cs('.ltr-env-pulse', 'opacity'),
    pulseTf: cs('.ltr-env-pulse', 'transform'), envRect: env ? fr(env) : null, heartOp: +cs('.ltr-heart', 'opacity'), flapTf: cs('.ltr-flap', 'transform'),
    veilOp: +cs('.ltr-veil', 'opacity'), isEnd: document.body.classList.contains('is-end'), nav: getComputedStyle(document.getElementById('navBtn')).display,
    bgm: (typeof backgroundMusic !== 'undefined' && backgroundMusic) ? +backgroundMusic.volume.toFixed(3) : null, demo: state.demoRunning,
    cleanup: typeof window.oceanCleanup === 'function' }; }"""
# the page's own frames (rAF) from the chime to the letter's readiness: the moment and the cloud's opacity — smoothness, and the
# cloud's return never faltering
TRACE_IN = """() => { window.__tin = []; (function loop(){ const r = document.querySelector('.ltr'); if(!r || r.classList.contains('ready')) return;
  const c = document.querySelector('.ltr-cloud'); window.__tin.push({ t: performance.now(), cloud: +getComputedStyle(c).opacity, cls: r.className }); requestAnimationFrame(loop); })(); }"""
PLAYS = "() => window._plays.map(p => ({ src: p.src, t: p.t, loop: p.loop, paused: p.el.paused, cur: p.el.currentTime, vol: +p.el.volume.toFixed(3) }))"

def shot(pg, name): pg.screenshot(path=str(out / name)); return out / name
def compare(a, ref, name, region=None, mask=None):
    """mean |diff| over the 1280x720 frame (the 1333x750 shot scaled down), over a region (frame px) if given, and inside a
    mask (an alpha picture placed in a [x, y, size] box, frame px) if given — the cloud's own pixels, whatever the room behind"""
    if not refs or not (refs / ref).exists(): return None
    from PIL import Image, ImageChops
    import numpy as np
    A = Image.open(a).convert("RGB").resize((1280, 720), Image.LANCZOS); B = Image.open(refs / ref).convert("RGB")
    d = np.asarray(ImageChops.difference(A, B)).astype(float).sum(axis=2)
    Image.fromarray(np.clip(d * 2, 0, 255).astype("uint8")).save(out / (name + "_diff.png"))
    res = {"mean": round(float(d.mean()), 2), "px_gt60": int((d > 60).sum())}
    if region:
        x0, y0, x1, y1 = region; r = d[y0:y1, x0:x1]; res["region_mean"] = round(float(r.mean()), 2); res["region_px_gt60"] = int((r > 60).sum())
    if mask:
        mp, box = mask; mx, my, mw = box[0], box[1], box[2]; mh = box[3] if len(box) > 3 else mw; n, nh = int(round(mw)), int(round(mh))
        al = np.zeros((nh, n), bool)
        for one in (mp if isinstance(mp, (list, tuple)) else [mp]):   # the union of the layers' alphas
            al |= np.asarray(Image.open(one).convert("RGBA").getchannel("A").resize((n, nh), Image.LANCZOS)) > 250   # fully opaque: the room behind cannot show through
        M = np.zeros((720, 1280), bool); x0, y0 = int(round(mx)), int(round(my)); sx, sy = max(0, -x0), max(0, -y0); X0, Y0 = max(0, x0), max(0, y0)
        h, w = min(nh - sy, 720 - Y0), min(n - sx, 1280 - X0)
        M[Y0:Y0 + h, X0:X0 + w] = al[sy:sy + h, sx:sx + w]
        res["mask_mean"] = round(float(d[M].mean()), 2); res["mask_px_gt60"] = int((d[M] > 60).sum())
    return res
def first(pl, prefix, since=0): return next((x for x in pl if x["src"].startswith(prefix) and x["t"] >= since), None)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(HOOK)
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE)
    def until(base, ms): pg.wait_for_function(f"performance.now() - {base} >= {ms}", timeout=ms + 8000, polling=20)
    ids = pg.evaluate("CARD.slides.map(s => s.id)")
    check("the pages: ... P2, L1 (the letter page), L2 (the stamp page), then the end screen (15)", ids == ["T0", "T0B", "T1", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "L1", "L2", "CEL"], ids)
    t0 = pg.evaluate("(() => { const t = performance.now(); mountSlide(CARD.slides.findIndex(s => s.id === 'L1')); return t; })()")
    # 1. scene A with the magic shimmer, no आगे, no header
    until(t0, 500); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); magic = first(pl, "sfx_letter_magic")
    check("mounts as a whole-stage page: no आगे, the first scene (538:2) alone (the letter's wrapper at 1/255: painted so decoded, unseen), the cleanup hook set", s and s["nav"] == "none" and s["bOp"] == 0 and s["cloudOp"] == 0 and s["growOp"] < 0.01 and s["cleanup"],
          {k: s[k] for k in ("nav", "bOp", "cloudOp", "growOp", "cleanup")} if s else s)
    check("the magic shimmer sounds as the page opens", magic is not None and magic["t"] - t0 < 300, round(magic["t"] - t0) if magic else None)
    shot(pg, "l1_a.png")
    check("the envelope is the drawing's own layers: the body (the pocket), ONE flap, the inside, the heart — no re-cut side flaps",
          pg.evaluate("!!document.querySelector('.ltr-body') && document.querySelectorAll('.ltr-flap').length === 1 && !document.querySelector('.ltr-fl, .ltr-fr, .ltr-fb')"))
    # 2. after 2 s the thinking girl (538:35) fades in
    until(t0, 1850); s = pg.evaluate(STATE); check("at 1.85 s the first scene still stands alone", s["bOp"] == 0, s["bOp"])
    until(t0, 2900); s = pg.evaluate(STATE); check("by 2.9 s the thinking girl (538:35) has faded in", s["bOp"] > 0.97, s["bOp"]); shot(pg, "l1_b.png")
    # 3. bubbles, then the cloud; the piano loop starts with the cloud, the engine's music ducks
    until(t0, 3650); s = pg.evaluate(STATE)
    check("at 3.65 s the three thought bubbles have popped and the cloud is growing in", len(s["bubs"]) == 3 and all(o > 0.9 for o in s["bubs"]) and 0.05 < s["cloudOp"] < 0.8, (s["bubs"], s["cloudOp"]))
    until(t0, 6000); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); music = first(pl, "bgm_letter")
    check("by 6 s the grandfather cloud stands (538:39)", s["cloudOp"] > 0.99 and s["cgOp"] > 0.99 and s["cwOp"] == 0, (s["cloudOp"], s["cgOp"], s["cwOp"]))
    check("the piano loop started with the cloud (3.3 s), loops, is sounding and has faded up", music is not None and 3200 < music["t"] - t0 < 3600 and music["loop"] and not music["paused"] and music["cur"] > 1 and music["vol"] > 0.4,
          (round(music["t"] - t0), music["loop"], music["paused"], round(music["cur"], 2), music["vol"]) if music else None)
    check("the engine's own background music is ducked under the loop", s["bgm"] is None or s["bgm"] <= 0.03, s["bgm"])
    cloud_box = pg.evaluate("CARD.slides.find(s => s.id === 'L1').data.layout.cloud")
    g = shot(pg, "l1_grandpa.png"); cmp_g = compare(g, "render_538-39.png", "l1_grandpa", region=(780, 0, 1280, 360),
                                                    mask=(html.parent / "assets" / "Images" / "img_letter_cloud_grandpa.webp", cloud_box))
    # the room pictures are the user's own versions (2026-10-26), not the frames' bitmaps, so only the cloud's own opaque pixels are
    # judged: 24.3 / 765 with the old room art and 24.3 with the new (the browser's downscale of the 820 px cloud against Figma's
    # render of the baked-in one); a wrong size or place would read far higher
    if cmp_g: check("the grandfather cloud against Figma's 538:39 render: close inside the cloud (mean < 30; frame and region are informative, the room art differs)", cmp_g["mask_mean"] < 30, cmp_g)
    # 4. [letter-idea] the chime, the moment the hold ends (7.5 s): on its "ummm" the cloud and the bubbles leave and the pensive
    #    girl (scene C) shows, no cloud; on its "aahaha" (2.37 s in) she brightens again and the SAME cloud grows in again, white,
    #    with the letter growing in it; then it pulses and waits
    until(t0, 7350); s = pg.evaluate(STATE)
    check("at 7.35 s, the end of the hold: the grandfather cloud still stands, the girl as before (scene C off)", s["cloudOp"] > 0.99 and s["cgOp"] > 0.99 and s["cOp"] < 0.01 and "c-in" not in s["cls"], (s["cloudOp"], s["cgOp"], s["cOp"]))
    until(t0, 8300); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); idea = first(pl, "sfx_letter_idea")
    check("the chime sounded as the hold ended (7.5 s)", idea is not None and 7400 < idea["t"] - t0 < 7800, round(idea["t"] - t0) if idea else None)
    check("at 8.3 s, the chime's \"ummm\": no cloud (gone back into its corner), no bubbles, the pensive girl (the user's 1.png) over the room, no letter yet",
          s["cloudOp"] == 0 and "out" in s["cloudCls"].split() and all(o == 0 for o in s["bubs"]) and s["cOp"] > 0.97 and "letter-in" not in s["cls"] and s["growOp"] == 0,
          (s["cloudOp"], s["cloudCls"], s["bubs"], s["cOp"], s["cls"], s["growOp"]))
    shot(pg, "l1_hum.png")
    t_idea = idea["t"] if idea else t0 + 7500
    pg.evaluate(TRACE_IN)
    until(t_idea, 2250); s = pg.evaluate(STATE)
    check("2.25 s into the chime (the silence before the \"aahaha\"): still no cloud, the bubbles popping again ahead of it, the girl still pensive",
          s["cloudOp"] == 0 and sum(1 for o in s["bubs"] if o > 0.5) >= 2 and "letter-in" not in s["cls"] and s["cOp"] > 0.97, (s["cloudOp"], s["bubs"], s["cls"], s["cOp"]))
    until(t_idea, 2850); s = pg.evaluate(STATE)
    check("0.45 s after the \"aahaha\" (2.37 s into the chime): the girl bright again (scene C off), the same cloud growing in again — white, the grandfather off — with the letter growing in it, not yet tappable",
          s["cOp"] < 0.05 and "in" in s["cloudCls"].split() and 0.05 < s["cloudOp"] < 0.85 and s["cgOp"] == 0 and s["cwOp"] == 1 and "letter-in" in s["cls"] and 0.05 < s["growOp"] < 0.85 and "ready" not in s["cls"],
          (s["cOp"], s["cloudCls"], s["cloudOp"], s["cgOp"], s["cwOp"], s["growOp"], s["cls"]))
    shot(pg, "l1_grow.png")   # the cloud and the letter in it growing together
    until(t_idea, 4100); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS)
    settled = s["growTf"] == "none" or (s["growTf"].startswith("matrix(") and float(s["growTf"][7:].split(",")[0]) > 0.999)   # the 1.6 s growth ends at 3.97 s
    check("by 4.1 s into the chime the white cloud stands with the letter in it (its growth done), pulsing and tappable",
          s["cloudOp"] > 0.99 and s["cgOp"] == 0 and s["cwOp"] == 1 and s["growOp"] == 1 and settled and "letter-in" in s["cls"] and "ready" in s["cls"] and s["pulseOp"] == 1 and not s["demo"],
          (s["cloudOp"], s["growOp"], s["growTf"], s["cls"]))
    check("the chime is the page's only voice-like sound and plays once", sum(1 for x in pl if x["src"].startswith("sfx_letter_idea")) == 1, [x["src"] for x in pl if "letter" in x["src"]])
    tr_in = pg.evaluate("window.__tin"); ts = [f["t"] - t_idea for f in tr_in]; gaps = [y - x for x, y in zip(ts, ts[1:])]
    after = [f["cloud"] for f in tr_in if f["t"] - t_idea >= 2400]
    check("the chime's beats run smoothly on the page's own frames (from the chime to the letter's readiness: no gap over 100 ms) and the cloud's return never falters (its opacity never falls after the \"aahaha\")",
          len(gaps) > 60 and max(gaps) < 100 and len(after) > 10 and all(y >= x - 1e-6 for x, y in zip(after, after[1:])),
          ("max gap %d ms over %d frames; %d frames after the aahaha" % (max(gaps), len(gaps) + 1, len(after))) if gaps else None)
    r = s["envRect"]
    check("the envelope icon: 558:2's size (189 px wide), centred in the cloud at (1020,166)", r and abs(r["w"] - 189) < 3 and abs(r["x"] + r["w"] / 2 - 1020) < 3 and abs(r["y"] + r["h"] / 2 - 166) < 3,
          {k: round(v, 1) for k, v in r.items()} if r else r)
    tf1 = s["pulseTf"]; until(t_idea, 4300); tf2 = pg.evaluate(STATE)["pulseTf"]
    check("the envelope pulses (its scale changes over 0.3 s)", tf1 != tf2, (tf1, tf2))
    l = shot(pg, "l1_letter.png"); cmp_l = compare(l, "render_558-2.png", "l1_letter", region=(780, 0, 1280, 360))
    if cmp_l: print("INFO the letter stage against Figma's 558:2 render (the designer's cloud differs from the kept one; informative only):", cmp_l)
    # 5. the tap: the pop, the zoom to 610:6, the loop fades out
    bb = pg.locator(".ltr-env-pos").bounding_box()
    pg.evaluate("(() => { const cs = completeSlide; completeSlide = function(){ window.__csT = performance.now(); return cs.apply(this, arguments); }; })()")   # the hand-over, on the page's own clock
    t_tap = pg.evaluate("performance.now()"); pg.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
    until(t_tap, 150); pl = pg.evaluate(PLAYS); s = pg.evaluate(STATE); pop = first(pl, "sfx_letter_pop")
    check("the tap: the pop sounds at once and the zoom begins", pop is not None and pop["t"] - t_tap < 250 and "zoom" in s["cls"] and "ready" not in s["cls"], (round(pop["t"] - t_tap) if pop else None, s["cls"]))
    # markers: 1x1 children at known box coords read the PROJECTED place of the 3-D flap (its own rect is the whole box's projection);
    # then the page records its own frames (rAF): the moment, the classes, the box, the markers, the seal — Playwright's polls lag
    # while the renderer is busy, the page's clock does not
    MARK = """() => { const f = document.querySelector('.ltr-flap'); if(!f.querySelector('.mk-apex')){ for (const [c, x, y] of [['mk-apex', 608.3, 468.3], ['mk-hinge', 538.6, 154.1]]) {
        const m = document.createElement('i'); m.className = c; m.style.cssText = 'position:absolute;left:' + x + 'px;top:' + y + 'px;width:1px;height:1px;pointer-events:none'; f.appendChild(m); } } }"""
    TRACE = """() => { window.__trace = []; const st = document.getElementById('stage');
      const q = (sel) => { const e = document.querySelector(sel); if(!e) return null; const b = st.getBoundingClientRect(), k = b.width / 1280, r = e.getBoundingClientRect(); return [(r.left - b.left) / k, (r.top - b.top) / k, r.width / k]; };
      (function loop(){ const r = document.querySelector('.ltr'); if(!r) return;
        window.__trace.push({ t: performance.now(), cls: r.className, env: q('.ltr-env-pos'), apex: q('.mk-apex'), hinge: q('.mk-hinge'), heart: +getComputedStyle(document.querySelector('.ltr-heart')).opacity,
          veil: +getComputedStyle(document.querySelector('.ltr-veil')).opacity });
        requestAnimationFrame(loop); })(); }"""
    pg.evaluate(MARK); pg.evaluate(TRACE)
    until(t_tap, 1300); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); r = s["envRect"]
    check("1.3 s after the tap the envelope fills the screen as 610:6 (71,-50 1138x758) over the blurred room", r and abs(r["x"] - 71) < 3 and abs(r["y"] + 50) < 3 and abs(r["w"] - 1138) < 4 and s["blurOp"] > 0.99,
          ({k: round(v, 1) for k, v in r.items()} if r else r, s["blurOp"]))
    music = first(pl, "bgm_letter")
    check("the piano loop has faded out by then", music is not None and (music["paused"] or music["vol"] < 0.05), (music["paused"], music["vol"]) if music else None)
    z = shot(pg, "l1_zoom.png"); cmp_z = compare(z, "render_610-6.png", "l1_zoom")
    if cmp_z: check("the full-screen envelope against Figma's 610:6 render: close (mean < 14)", cmp_z["mean"] < 14, cmp_z)   # its backdrop is 610:6's own blurred picture
    # the envelope AS DRAWN: the dist's own layers (inner, body, flap, heart) stacked over the blurred room at 610:6's box ARE the
    # drawing (make_env_layers_exact.py: lossless, the drawing's pixels); the shot is judged on the envelope's flat parts — inside
    # its silhouette eroded 4 px, off the drawing's own edges, outside the seal's box (its hard red edge resamples differently in
    # the browser and in PIL) — where an added line or a re-cut shows at once (the four-flap cut: thousands of px) and resampling does not
    from PIL import Image as _Im, ImageChops as _Ch, ImageFilter as _Fl
    import numpy as _np
    env_box = pg.evaluate("CARD.slides.find(s => s.id === 'L1').data.layout.full"); IM = html.parent / "assets" / "Images"
    bx, by, bw, bh = (int(round(v)) for v in env_box)
    T = _Im.open(IM / "img_letter_blur.webp").convert("RGB").resize((1280, 720), _Im.LANCZOS)
    for n in ("inner", "body", "flap", "heart"):
        Ly = _Im.open(IM / f"img_letter_env_{n}.webp").convert("RGBA").resize((bw, bh), _Im.LANCZOS); T.paste(Ly, (bx, by), Ly)
    sil = _np.zeros((720, 1280), bool)
    for n in ("body", "flap"):
        a = _np.asarray(_Im.open(IM / f"img_letter_env_{n}.webp").convert("RGBA").getchannel("A").resize((bw, bh), _Im.LANCZOS)) > 250
        sy, sx = max(0, -by), max(0, -bx); Y0, X0 = max(0, by), max(0, bx); hh, ww = min(bh - sy, 720 - Y0), min(bw - sx, 1280 - X0)
        sil[Y0:Y0 + hh, X0:X0 + ww] |= a[sy:sy + hh, sx:sx + ww]
    er = _np.asarray(_Im.fromarray(sil.astype(_np.uint8) * 255).filter(_Fl.MinFilter(9))) > 0
    gd = _np.asarray(T.convert("L").filter(_Fl.FIND_EDGES).filter(_Fl.MaxFilter(5))).astype(int)
    flat = er & (gd < 12); flat[240:470, 540:800] = False
    Zs = _Im.open(z).convert("RGB").resize((1280, 720), _Im.LANCZOS); dz = _np.asarray(_Ch.difference(Zs, T)).astype(float).sum(axis=2)
    _Im.fromarray(_np.clip(dz * flat * 4, 0, 255).astype("uint8")).save(out / "l1_zoom_asdrawn_diff.png")
    check("the envelope itself is the drawing as drawn (its flat parts against the stacked layers: mean < 4, under 300 px over 40 — an added line or a re-cut is thousands)",
          dz[flat].mean() < 4 and int((dz[flat] > 40).sum()) < 300, (round(float(dz[flat].mean()), 2), int((dz[flat] > 40).sum()), int(flat.sum())))
    # 6. the opening: the paper crackle with the seal popping and the flap swinging; the sheet rises; the veil; the end screen
    paper = first(pl, "sfx_letter_paper")
    check("the paper crackle started as the envelope finished zooming (1.2 s) and the top flap is opening", paper is not None and 1150 < paper["t"] - t_tap < 1450 and "open" in s["cls"], (round(paper["t"] - t_tap) if paper else None, s["cls"]))
    until(t_tap, 2250); shot(pg, "l1_flap.png")
    until(t_tap, 3000); t_shot = pg.evaluate("performance.now()") - t_tap
    t_s0 = pg.evaluate("performance.now()"); o = shot(pg, "l1_open.png"); print("INFO the 3 s shot took", round(pg.evaluate("performance.now()") - t_s0), "ms (the dive's scaled layers)")
    from PIL import Image as _Im
    import numpy as _np
    O = _np.asarray(_Im.open(o).convert("RGB").resize((1280, 720), _Im.LANCZOS)).astype(int)
    sheet = float(((O[..., 0] > 228) & (O[..., 2] > 222)).mean())   # the sheet's white (255,253,248) and its fading lilac lines; not the envelope's cream (b ~ 205), not the room
    pg.wait_for_function("CARD.slides[state.idx].id === 'L2' && !!document.querySelector('.stp')", timeout=6000)
    t_end = pg.evaluate("performance.now()"); cs_t = pg.evaluate("window.__csT || 0")
    check("the page hands over to the stamp page (L2) about 3.65 s after the tap (completeSlide on the page's own clock, after the dive and the veil; stamp_check.py has that page)", cs_t and 3300 < cs_t - t_tap < 4300 and t_end >= cs_t,
          (round(cs_t - t_tap) if cs_t else None, "seen by the test at", round(t_end - t_tap)))
    tr = pg.evaluate("window.__trace")
    def frame_at(ms): return min(tr, key=lambda f: abs(f["t"] - (t_tap + ms)))
    f = frame_at(3000)
    check("3.0 s after the tap (the page's frame): the view has dived into the envelope (the box over 3.5x the frame), the seal still gone, the veil not yet up",
          abs(f["t"] - t_tap - 3000) < 80 and f["env"][2] > 1138 * 3.5 and f["heart"] == 0 and f["veil"] < 0.05, (round(f["t"] - t_tap), round(f["env"][2]), f["heart"], f["veil"]))
    f = frame_at(t_shot)
    check("the shot there (%d ms; the veil %.2f): the sheet fills the screen (over 90 %% sheet pixels)" % (t_shot, f["veil"]), sheet > 0.9 or f["veil"] > 0.2, round(sheet, 3))
    def fmt(f): return (round(f["t"] - t_tap), f["heart"], f["cls"].replace("ltr b-in letter-in ", ""), {k: [round(v) for v in f[k]] for k in ("apex", "hinge", "env") if f[k]})
    f = frame_at(1700)
    check("1.7 s after the tap (the page's frame): the seal has popped off, the flap is lifting (its tip risen, still below its hinge), the sheet is rising, the view still 610:6's",
          abs(f["t"] - t_tap - 1700) < 80 and f["heart"] == 0 and "paper" in f["cls"] and "dive" not in f["cls"] and f["hinge"][1] + 20 < f["apex"][1] < 400, fmt(f))
    f = frame_at(2250)
    tip = (f["apex"][1] - f["hinge"][1]) / (f["env"][2] / 1138)   # the standing flap's tip under the hinge, in box px: ~31 lifted toward the viewer (80 deg), ~73 if folded away
    check("2.25 s after the tap (the page's frame): the flap stands open toward the viewer (its tip 20-50 box px under the hinge: almost edge-on, lifted up and out); the dive has begun",
          abs(f["t"] - t_tap - 2250) < 80 and "dive" in f["cls"] and 20 < tip < 50 and f["env"][2] > 1150, (fmt(f), round(tip, 1)))
    after_zoom = [f for f in tr if f["t"] - t_tap >= 1300 and f["env"]]
    check("the opening stays full-screen (no pull-back): in no frame after the zoom is the box smaller than 610:6's", after_zoom and min(f["env"][2] for f in after_zoom) >= 1136, round(min(f["env"][2] for f in after_zoom)) if after_zoom else None)
    moving = [f for f in tr if f["apex"] and f["hinge"] and "open" in f["cls"]]
    check("in no frame does any part of the flap rise above the envelope's top edge (its tip stays at or below the hinge), so nothing of it can be cut by the frame",
          moving and all(f["apex"][1] >= f["hinge"][1] - 2 for f in moving), (len(moving), round(min(f["apex"][1] - f["hinge"][1] for f in moving), 1) if moving else None))
    until(t_end, 800); pl = pg.evaluate(PLAYS); bgm = pg.evaluate("(typeof backgroundMusic !== 'undefined' && backgroundMusic) ? backgroundMusic.volume : null")
    page_sounds = [x for x in pl if "letter" in x["src"]]
    check("leaving the page stopped every one of its sounds and gave the engine its music back", len(page_sounds) == 5 and all(x["paused"] for x in page_sounds) and (bgm is None or bgm > 0.05),
          ([(x["src"], x["paused"]) for x in page_sounds], bgm))
    check("no round gate between the letter page and the stamp page", not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"))
    shot(pg, "l1_end.png")
    # 7. a re-run from the end screen (the dev nav), then leaving it mid-way: a clean restart, a clean stop
    pg.evaluate("window._plays = []")
    t1 = pg.evaluate("(() => { const t = performance.now(); mountSlide(CARD.slides.findIndex(s => s.id === 'L1')); return t; })()")
    until(t1, 4000); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); music = first(pl, "bgm_letter")
    check("re-run from the stamp page: the scene restarts from the first picture, the loop starts again", s and "b-in" in s["cls"] and "letter-in" not in s["cls"] and "c-in" not in s["cls"] and music is not None and not music["paused"], (s["cls"] if s else s, music is not None))
    # the opening once more with nothing else going on (no screenshots, no polls): the page's own frame times = smoothness
    pg.wait_for_function("!!document.querySelector('.ltr.ready')", timeout=15000)
    bb = pg.locator(".ltr-env-pos").bounding_box(); t2 = pg.evaluate("performance.now()"); pg.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
    pg.evaluate(MARK); pg.evaluate(TRACE)
    pg.wait_for_function("CARD.slides[state.idx].id === 'L2' && !!document.querySelector('.stp')", timeout=8000)
    tr2 = pg.evaluate("window.__trace"); ts = [f["t"] - t2 for f in tr2 if f["t"] - t2 >= 1150]; gaps = [b - a for a, b in zip(ts, ts[1:])]
    check("the opening runs smoothly (the page's own frame times from the crackle to the next page, nothing else running: no gap over 100 ms)", len(gaps) > 20 and max(gaps) < 100,
          ("max gap %d ms, %d frames, mean %.1f ms" % (max(gaps), len(gaps) + 1, sum(gaps) / len(gaps))) if gaps else None)
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'L1'))"); pg.wait_for_timeout(1000)
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'P2'))"); pg.wait_for_timeout(500); pl = pg.evaluate(PLAYS)
    check("leaving mid-way (to P2): the page's loop and sounds stop, its hook is cleared, its scene is gone", all(x["paused"] for x in pl if "letter" in x["src"]) and pg.evaluate("window.oceanCleanup == null") and pg.evaluate("!document.querySelector('.ltr')"),
          [(x["src"], x["paused"]) for x in pl if "letter" in x["src"]])
    check("no page errors", not errs, errs[:3])
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
