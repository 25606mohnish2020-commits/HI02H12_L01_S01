"""The letter page L1 ([letter-fig], the flow [l1-fig] 2026-11-03): mounted straight (as the dev nav would), the whole scene plays by
itself on the narration's clock and its sounds start with their visual beats; the envelope waits for the tap, zooms to 610:6, opens
and hands over to the stamp page. [l1-fig]: the girl writing (Figma 792:1257) comes in on the magic shimmer's first frame; the
narration (vo_letter_intro) 1.2 s later with the piano bed (.2); on its "दादाजी" (0.84 s) the girl thinking (792:1245), the bubbles,
the grandfather cloud; at its first sentence's end (4.30 s) the girl pensive (792:1249) and, on the "aahaha" (sfx_letter_aha), the
white cloud over the grandfather with the letter growing in it; once the narration has ended the letter pulses, tappable.
usage: python -I -X utf8 letter_check.py <index.html> <outdir> [<dir with render_610-6.png>]
Screenshots: l1_write.png (792:1257), l1_grandpa.png (792:1245 + the cloud), l1_letter.png (792:1249 + the letter), l1_zoom.png
(610:6), l1_flap.png, l1_open.png, l1_end.png; against the frames' renders (letter_assets/fig_792-*_render.png) outside the thought.
Samples come from the page's OWN frames (rAF) and the clip's own clock, so screenshot time does not drift them."""
import sys, json, pathlib
from playwright.sync_api import sync_playwright
html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
refs = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
FIG = pathlib.Path(__file__).resolve().parent / "letter_assets"   # [l1-fig] the three frames' renders
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
  return { cls: r.className, slide: CARD.slides[state.idx].id, wOp: +cs('.ltr-scene.w', 'opacity'), tOp: +cs('.ltr-scene.t', 'opacity'), pOp: +cs('.ltr-scene.p', 'opacity'),
    cloudOp: +cs('.ltr-cloud', 'opacity'), cloudCls: (document.querySelector('.ltr-cloud') || {}).className || '', growOp: +cs('.ltr-env-grow', 'opacity'), growTf: cs('.ltr-env-grow', 'transform'),
    cgOp: +cs('.ltr-cloud .ltr-cg', 'opacity'), cwOp: +cs('.ltr-cloud .ltr-cw', 'opacity'), blurOp: +cs('.ltr-blur', 'opacity'),
    bubs: [...document.querySelectorAll('.ltr-bub')].map(b => +getComputedStyle(b).opacity), pulseOp: +cs('.ltr-env-pulse', 'opacity'),
    pulseTf: cs('.ltr-env-pulse', 'transform'), envRect: env ? fr(env) : null, heartOp: +cs('.ltr-heart', 'opacity'), flapTf: cs('.ltr-flap', 'transform'),
    scenes: ['w', 't', 'p'].map(k => fr(document.querySelector('.ltr-scene.' + k))), cloudRect: fr(document.querySelector('.ltr-cloud')),
    veilOp: +cs('.ltr-veil', 'opacity'), isEnd: document.body.classList.contains('is-end'), nav: getComputedStyle(document.getElementById('navBtn')).display,
    bgm: (typeof backgroundMusic !== 'undefined' && backgroundMusic) ? +backgroundMusic.volume.toFixed(3) : null, demo: state.demoRunning,
    cleanup: typeof window.oceanCleanup === 'function' }; }"""
# [l1-fig] the page's own frames (rAF) from the mount to the letter's readiness: the moment, the narration's clock, the classes and
# the opacities — every beat is read off these, on the clip's clock where it hangs on it
TRACE_IN = """() => { window.__tin = []; (function loop(){ const r = document.querySelector('.ltr'); if(!r) return; const q = (s) => document.querySelector(s), o = (s) => +getComputedStyle(q(s)).opacity;
  const a = currentAudio, vo = !!a && String(a.src).includes('vo_letter_intro');
  window.__tin.push({ t: performance.now(), voT: vo ? a.currentTime : null, cls: r.className, cloudCls: q('.ltr-cloud').className, bubs: document.querySelectorAll('.ltr-bub.in').length,
    w: o('.ltr-scene.w'), tO: o('.ltr-scene.t'), p: o('.ltr-scene.p'), cloud: o('.ltr-cloud'), cg: o('.ltr-cg'), cw: o('.ltr-cw'), grow: o('.ltr-env-grow') });
  if(!r.classList.contains('ready') || window.__tin.length < 3) requestAnimationFrame(loop); })(); }"""
PLAYS = "() => window._plays.map(p => ({ src: p.src, t: p.t, loop: p.loop, paused: p.el.paused, cur: p.el.currentTime, vol: +p.el.volume.toFixed(3) }))"

def shot(pg, name): pg.screenshot(path=str(out / name)); return out / name
def compare(a, ref, name, region=None, mask=None, outside=None):
    """mean |diff| (sum of the three channels) over the 1280x720 frame (the 1333x750 shot scaled down), over a region (frame px) if given,
    inside a mask (an alpha picture placed in a [x, y, size] box, frame px) if given, and outside a box (the thought) if given"""
    path = (refs / ref) if refs and (refs / ref).exists() else (FIG / ref if (FIG / ref).exists() else None)
    if not path: return None
    from PIL import Image, ImageChops
    import numpy as np
    A = Image.open(a).convert("RGB").resize((1280, 720), Image.LANCZOS); B = Image.open(path).convert("RGB")
    d = np.asarray(ImageChops.difference(A, B)).astype(float).sum(axis=2)
    Image.fromarray(np.clip(d * 2, 0, 255).astype("uint8")).save(out / (name + "_diff.png"))
    res = {"mean": round(float(d.mean()), 2), "px_gt60": int((d > 60).sum())}
    if region:
        x0, y0, x1, y1 = region; r = d[y0:y1, x0:x1]; res["region_mean"] = round(float(r.mean()), 2); res["region_px_gt60"] = int((r > 60).sum())
    if outside:
        x0, y0, x1, y1 = outside; m = np.ones(d.shape, bool); m[y0:y1, x0:x1] = False; res["outside_mean"] = round(float(d[m].mean()), 2); res["outside_px_gt60"] = int((d[m] > 60).sum())
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
THOUGHT = (715, 0, 1190, 310)   # [l1-fig] the bubbles, the cloud and the letter (frame px): the renders have none

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(HOOK)
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE)
    def until(base, ms): pg.wait_for_function(f"performance.now() - {base} >= {ms}", timeout=ms + 8000, polling=20)
    ids = pg.evaluate("CARD.slides.map(s => s.id)")
    check("the pages: ... P2, L1 (the letter page), L2 (the stamp page), then the end screen (17)", ids == ["T0", "T0B", "T1", "T1B", "T1C", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "L1", "L2", "CEL"], ids)
    D = pg.evaluate("CARD.slides.find(s => s.id === 'L1').data"); LY, PC = D["layout"], D["pace"]
    t0 = pg.evaluate("(() => { const t = performance.now(); mountSlide(CARD.slides.findIndex(s => s.id === 'L1')); return t; })()"); pg.evaluate(TRACE_IN)
    # 1. [l1-fig] the girl writing (792:1257) comes in on the magic shimmer's first frame, full screen; no आगे, no header
    until(t0, 500); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); magic = first(pl, "sfx_letter_magic")
    bq = pg.evaluate("window.__bgm ? [window.__bgm.wanted, window.__bgm.el ? window.__bgm.el.paused : null, window.__bgm.target] : null")   # [l1-quiet]
    check("the music bed is off on this page: not wanted, its target 0, the element paused ([l1-quiet])", bq is not None and bq[0] is False and bq[1] is True and bq[2] == 0, bq)
    check("mounts as a whole-stage page: no आगे, the girl writing coming in (.w-in), the other two pictures, the letter's wrapper at 1/255 (painted so decoded, unseen), no cloud, the cleanup hook set",
          s and s["nav"] == "none" and "w-in" in s["cls"] and s["wOp"] > 0.2 and s["tOp"] < 0.01 and s["pOp"] < 0.01 and s["cloudOp"] == 0 and s["growOp"] < 0.01 and s["cleanup"],
          {k: s[k] for k in ("nav", "cls", "wOp", "tOp", "pOp", "cloudOp", "growOp", "cleanup")} if s else s)
    tin = pg.evaluate("window.__tin"); w_first = next((f for f in tin if "w-in" in f["cls"]), None)
    check("the magic shimmer sounds as the page opens and the picture starts to come in with it (its first frame within 300 ms of the sound's start: the module waits for its \"playing\")",
          magic is not None and magic["t"] - t0 < 300 and w_first is not None and -20 <= w_first["t"] - magic["t"] <= 300 and not any(f["w"] > 0.01 for f in tin if f["t"] < magic["t"]),
          (round(magic["t"] - t0) if magic else None, round(w_first["t"] - magic["t"]) if (w_first and magic) else None))
    want = [LY["scenes"][k] for k in ("w", "t", "p")]
    check("each picture is its frame's own box (792:1257 -262,-91 1563x880; 792:1245 -231,-42 1516x853; 792:1249 -237,-38 1520x856), within 1 px",
          all(abs(g[k2] - w_[i]) < 1 for g, w_ in zip(s["scenes"][1:], want[1:]) for i, k2 in enumerate(("x", "y", "w", "h"))), [{k: round(v, 1) for k, v in g.items()} for g in s["scenes"]])
    check("the envelope is the drawing's own layers: the body (the pocket), ONE flap, the inside, the heart — no re-cut side flaps",
          pg.evaluate("!!document.querySelector('.ltr-body') && document.querySelectorAll('.ltr-flap').length === 1 && !document.querySelector('.ltr-fl, .ltr-fr, .ltr-fb')"))
    until(t0, 1900); s = pg.evaluate(STATE); wr = shot(pg, "l1_write.png"); c1 = compare(wr, "fig_792-1257_render.png", "l1_write")
    check("by 1.9 s the girl writing stands, settled in 792:1257's box (its 1.6 s entrance over), alone", abs(s["scenes"][0]["x"] - want[0][0]) < 1 and abs(s["scenes"][0]["w"] - want[0][2]) < 1 and s["wOp"] == 1 and s["tOp"] < 0.01,
          ({k: round(v, 1) for k, v in s["scenes"][0].items()}, s["wOp"]))
    if c1: check("the girl writing against Figma's 792:1257 render (mean < 8 of 765: the browser's resampling)", c1["mean"] < 8, c1)
    # 2. the narration 1.2 s after the picture began, the piano bed with it (mild, .2)
    pg.wait_for_function("currentAudio && currentAudio.src.includes('vo_letter_intro') && isPlaying", timeout=8000, polling=10)
    until(t0, 3200); pl = pg.evaluate(PLAYS); vo = first(pl, "vo_letter_intro"); music = first(pl, "bgm_letter")
    check(f"the narration (vo_letter_intro) starts {PC['vo_at']} ms after the picture began (and the magic)", vo is not None and w_first is not None and abs(vo["t"] - w_first["t"] - PC["vo_at"]) < 200,
          round(vo["t"] - w_first["t"]) if (vo and w_first) else None)
    check(f"the piano loop starts with it, loops, sounds, faded up to the mild {PC['music_vol']}", music is not None and vo is not None and abs(music["t"] - vo["t"]) < 60 and music["loop"] and not music["paused"] and abs(music["vol"] - PC["music_vol"]) < 0.02,
          (round(music["t"] - vo["t"]), music["loop"], music["paused"], music["vol"]) if (music and vo) else None)
    # 3. on "दादाजी" (0.84 s on the narration's clock): the girl thinking fades in, the bubbles, the cloud — read off the page's frames
    pg.wait_for_function(f"currentAudio && currentAudio.src.includes('vo_letter_intro') && currentAudio.currentTime >= {(PC['letter'] - 400) / 1000}", timeout=15000, polling=20)
    s = pg.evaluate(STATE); g = shot(pg, "l1_grandpa.png"); c2 = compare(g, "fig_792-1245_render.png", "l1_grandpa", outside=THOUGHT)
    tin = pg.evaluate("window.__tin")
    def at(pred): return next((f for f in tin if pred(f)), None)
    f_t = at(lambda f: "t-in" in f["cls"]); before = [f for f in tin if f["voT"] is not None and f["voT"] < PC["dada"] / 1000 - 0.02]
    check(f"the girl thinking (792:1245) on \"दादाजी\" ({PC['dada'] / 1000} s on the narration's clock: its first frame within 50 ms after), nothing of her before",
          f_t is not None and f_t["voT"] is not None and 0 <= f_t["voT"] - PC["dada"] / 1000 <= 0.05 and all("t-in" not in f["cls"] and f["tO"] < 0.01 for f in before),
          round(f_t["voT"], 3) if f_t and f_t["voT"] is not None else None)
    tb = [at(lambda f, n=n: f["bubs"] >= n) for n in (1, 2, 3)]; f_c = at(lambda f: " in" in f["cloudCls"])
    dt = lambda f: round(f["t"] - f_t["t"]) if (f and f_t) else None
    check(f"the bubbles pop one by one ({PC['bub_after']} / +{PC['bub_gap']} / +{PC['bub_gap']} ms after her, within 60) and the cloud begins to grow in {PC['cloud_after']} ms after her (within 60), as before",
          all(x is not None for x in tb + [f_c]) and all(abs(dt(x) - (PC["bub_after"] + k * PC["bub_gap"])) <= 60 for k, x in enumerate(tb)) and abs(dt(f_c) - PC["cloud_after"]) <= 60,
          ([dt(x) for x in tb], dt(f_c)))
    check("the grandfather cloud stands before the letter's moment (opacity 1, its white twin at 1/255), the bubbles up, the girl thinking over the writing one",
          s["cloudOp"] > 0.99 and s["cgOp"] > 0.99 and s["cwOp"] < 0.01 and all(o > 0.99 for o in s["bubs"]) and s["tOp"] == 1 and s["pOp"] < 0.01, (s["cloudOp"], s["cgOp"], s["cwOp"], s["bubs"], s["tOp"]))
    cr = s["cloudRect"]; lc = LY["cloud"]
    check("the cloud in its place on the new girl (layout.cloud = the old thought carried onto her head: x 1.12 about (808,245) -> (730,240)) and its visible top inside the frame",
          abs(cr["x"] - lc[0]) < 1 and abs(cr["y"] - lc[1]) < 1 and abs(cr["w"] - lc[2]) < 1 and lc[1] + 98 / 820 * lc[2] > 0, ({k: round(v, 1) for k, v in cr.items()}, lc))
    if c2: check("the girl thinking against Figma's 792:1245 render outside the thought (mean < 8 of 765)", c2["outside_mean"] < 8, c2)
    # 4. at the first sentence's end (4.30 s): the girl pensive, the "aahaha", the white cloud over the grandfather, the letter growing in
    pg.wait_for_function("!!document.querySelector('.ltr.ready')", timeout=20000, polling=20)
    t_ready = pg.evaluate("performance.now()"); until(t_ready, 600); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS)
    tin = pg.evaluate("window.__tin"); aha = first(pl, "sfx_letter_aha")
    f_p = at(lambda f: "p-in" in f["cls"]); f_l = at(lambda f: "letter-in" in f["cls"]); f_w2 = at(lambda f: "white2" in f["cloudCls"])
    check(f"the girl pensive (792:1249) at the first sentence's end ({PC['letter'] / 1000} s on the narration's clock, its first frame within 50 ms after) and the \"aahaha\" clip started in that frame",
          f_p is not None and f_p["voT"] is not None and 0 <= f_p["voT"] - PC["letter"] / 1000 <= 0.05 and aha is not None and abs(aha["t"] - f_p["t"]) <= 40,
          (round(f_p["voT"], 3) if f_p and f_p["voT"] is not None else None, round(aha["t"] - f_p["t"]) if (aha and f_p) else None))
    check(f"on the \"aahaha\" ({PC['aha_lead']} ms into its clip: its first frame 40-200 ms after the clip's start, the browser's start latency included) the white cloud comes over the grandfather and the letter begins to grow, together; the grandfather goes from under it {PC['white']} ms later",
          f_l is not None and aha is not None and 40 <= f_l["t"] - aha["t"] <= 200 and "white" in f_l["cloudCls"] and f_w2 is not None and abs(f_w2["t"] - f_l["t"] - PC["white"] - 20) <= 60,
          (round(f_l["t"] - aha["t"]) if (f_l and aha) else None, round(f_w2["t"] - f_l["t"]) if (f_w2 and f_l) else None))
    swap = [f for f in tin if f_l and f_w2 and f_l["t"] <= f["t"] < f_w2["t"]]
    check("no dip as the cloud whitens: the grandfather stays whole under the white one until it is whole, the cloud itself at 1 throughout",
          len(swap) > 10 and all(f["cg"] == 1 and f["cloud"] == 1 for f in swap) and swap[-1]["cw"] > 0.97, (len(swap), min((f["cg"] for f in swap), default=None), swap[-1]["cw"] if swap else None))
    ready_vo = next((f for f in reversed(tin) if f["voT"] is not None), None)
    pl_vo = first(pl, "vo_letter_intro")
    check(f"tappable only once the narration has ended (~{PC['ready_after']} ms after) and the letter has grown: never before",
          ready_vo is not None and ready_vo["voT"] > 11.2 and t_ready - (pl_vo["t"] if pl_vo else 0) > 11000 and not any("ready" in f["cls"] for f in tin[:-1]),
          (round(ready_vo["voT"], 2) if ready_vo else None, round(t_ready - pl_vo["t"]) if pl_vo else None))
    settled = s["growTf"] == "none" or (s["growTf"].startswith("matrix(") and abs(float(s["growTf"][7:].split(",")[0]) - 1) < 0.001)
    check("then the white cloud stands with the letter in it (its growth done), the grandfather gone, pulsing and tappable",
          s["cloudOp"] > 0.99 and s["cgOp"] == 0 and s["cwOp"] == 1 and s["growOp"] == 1 and settled and "letter-in" in s["cls"] and "ready" in s["cls"] and s["pulseOp"] == 1 and not s["demo"],
          (s["cloudOp"], s["cgOp"], s["cwOp"], s["growOp"], s["growTf"], s["cls"]))
    check("the \"aahaha\" plays once, the narration once, the old chime never", sum(1 for x in pl if x["src"].startswith("sfx_letter_aha")) == 1 and sum(1 for x in pl if x["src"].startswith("vo_letter_intro")) == 1
          and not any(x["src"].startswith("sfx_letter_idea") for x in pl), [x["src"] for x in pl if "letter" in x["src"]])
    ts = [f["t"] for f in tin]; gaps = [y - x for x, y in zip(ts, ts[1:]) if x - t0 > 600]
    check("the beats run smoothly on the page's own frames (from 0.6 s to the letter's readiness: no gap over 100 ms)", len(gaps) > 200 and max(gaps) < 100,
          ("max gap %d ms over %d frames, mean %.1f" % (max(gaps), len(gaps) + 1, sum(gaps) / len(gaps))) if gaps else None)
    r = s["envRect"]; li = LY["letter"]
    check(f"the envelope icon: {li[2]} px wide, centred in the cloud at ({li[0]}, {li[1]})", r and abs(r["w"] - li[2]) < 3 and abs(r["x"] + r["w"] / 2 - li[0]) < 3 and abs(r["y"] + r["h"] / 2 - li[1]) < 3,
          {k: round(v, 1) for k, v in r.items()} if r else r)
    tf1 = s["pulseTf"]; until(t_ready, 900); tf2 = pg.evaluate(STATE)["pulseTf"]
    check("the envelope pulses (its scale changes over 0.3 s)", tf1 != tf2, (tf1, tf2))
    l = shot(pg, "l1_letter.png"); c3 = compare(l, "fig_792-1249_render.png", "l1_letter", outside=THOUGHT)
    if c3: check("the girl pensive against Figma's 792:1249 render outside the thought (mean < 8 of 765)", c3["outside_mean"] < 8, c3)
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
    if cmp_z: print("INFO the full-screen envelope against Figma's 610:6 render (its backdrop is the OLD room, blurred; [l1-fig] the page's is 792:1249's):", cmp_z)
    # the envelope AS DRAWN: the dist's own layers (inner, body, flap, heart) stacked over the blurred room at 610:6's box ARE the
    # drawing (make_env_layers_exact.py: lossless, the drawing's pixels); the shot is judged on the envelope's flat parts — inside
    # its silhouette eroded 4 px, off the drawing's own edges, outside the seal's box (its hard red edge resamples differently in
    # the browser and in PIL) — where an added line or a re-cut shows at once (the four-flap cut: thousands of px) and resampling does not
    from PIL import Image as _Im, ImageChops as _Ch, ImageFilter as _Fl
    import numpy as _np
    env_box = pg.evaluate("CARD.slides.find(s => s.id === 'L1').data.layout.full"); IM = html.parent / "assets" / "Images"
    bx, by, bw, bh = (int(round(v)) for v in env_box)
    T = _Im.open(IM / "img_letter_blur_p.webp").convert("RGB").resize((1280, 720), _Im.LANCZOS)
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
    def fmt(f): return (round(f["t"] - t_tap), f["heart"], f["cls"].replace("ltr w-in t-in p-in letter-in ", ""), {k: [round(v) for v in f[k]] for k in ("apex", "hinge", "env") if f[k]})
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
    until(t_end, 800); pl = pg.evaluate(PLAYS); bgm = pg.evaluate("(typeof backgroundMusic !== 'undefined' && backgroundMusic) ? (backgroundMusic.paused ? 0 : 1) : null")   # [dun-chrome] the bed runs (its level follows the sounds: ducked under L2's line just now)
    page_sounds = [x for x in pl if "letter" in x["src"]]
    bq = pg.evaluate("window.__bgm ? [window.__bgm.wanted, window.__bgm.el ? window.__bgm.el.paused : null, window.__bgm.target, +window.__bgm.level.toFixed(3)] : null")   # [l1-quiet]
    check("the bed starts again as the stamp page mounts, once the dive and the veil are over: wanted, playing, its target up (0.13, or the duck under L2's line) 0.8 s in ([l1-quiet])",
          bq is not None and bq[0] is True and bq[1] is False and bq[2] > 0, bq)
    check("leaving the page stopped every one of its sounds (the narration too) and the music bed runs on (ducked under the next page's line)", len(page_sounds) == 6 and all(x["paused"] for x in page_sounds) and (bgm is None or bgm > 0.05),
          ([(x["src"], x["paused"]) for x in page_sounds], bgm))
    check("no round gate between the letter page and the stamp page", not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"))
    shot(pg, "l1_end.png")
    # 7. a re-run from the end screen (the dev nav), then leaving it mid-way: a clean restart, a clean stop
    pg.evaluate("window._plays = []")
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'L1'))")
    pg.wait_for_function("currentAudio && currentAudio.src.includes('vo_letter_intro') && currentAudio.currentTime > 2.5", timeout=12000, polling=20)   # [l1-fig] the picture, the narration, its "दादाजी"
    s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); music = first(pl, "bgm_letter")
    check("re-run from the stamp page: the scene restarts from the first picture — the narration again, the girl thinking on its \"दादाजी\", no letter yet — and the loop starts again",
          s and "w-in" in s["cls"] and "t-in" in s["cls"] and "p-in" not in s["cls"] and "letter-in" not in s["cls"] and music is not None and not music["paused"], (s["cls"] if s else s, music is not None))
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
    # [l1-quiet] the bed fades out as the letter page mounts: from P2 (the bed up) to L1 — falling at 0.3 s, paused and at 0 by 0.9 s
    pg.wait_for_function("window.__bgm && window.__bgm.el && !window.__bgm.el.paused && window.__bgm.wanted", timeout=8000, polling=20)   # the bed up on P2 (ducked under its line)
    tq = pg.evaluate("(() => { const t = performance.now(); mountSlide(CARD.slides.findIndex(s => s.id === 'L1')); return t; })()")
    b0 = pg.evaluate("[window.__bgm.wanted, window.__bgm.target, +window.__bgm.level.toFixed(3), window.__bgm.el.paused]")
    until(tq, 300); b1 = pg.evaluate("[window.__bgm.wanted, window.__bgm.target, +window.__bgm.level.toFixed(3), window.__bgm.el.paused]")
    until(tq, 900); b2 = pg.evaluate("[window.__bgm.wanted, window.__bgm.target, +window.__bgm.level.toFixed(3), window.__bgm.el.paused]")
    check("coming from P2 with the bed up, the letter page's mount turns the bed off: not wanted and its target 0 at once, its level falling by 0.3 s, silent and paused by 0.9 s ([l1-quiet])",
          b0[0] is False and b0[1] == 0 and b1[2] <= b0[2] and b2[0] is False and b2[2] == 0 and b2[3] is True, (b0, b1, b2))
    check("no page errors", not errs, errs[:3])
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
