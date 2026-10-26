"""The letter page L1 ([letter-fig]): mounted straight (as the dev nav would), the whole scene plays by itself and its sounds
start with their visual beats; the envelope waits for the tap, zooms to 610:6, opens and hands over to the end screen.
usage: python -I -X utf8 letter_check.py <index.html> <outdir> [<dir with render_538-39.png render_558-2.png render_610-6.png>]
Screenshots: l1_a.png (538:2), l1_b.png (538:35), l1_grandpa.png (538:39), l1_letter.png (558:2), l1_zoom.png (610:6), l1_open.png,
l1_end.png; with the renders, *_diff.png and the pixel numbers. Samples are taken at set moments of the PAGE's clock
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
  return { cls: r.className, slide: CARD.slides[state.idx].id, bOp: +cs('.ltr-scene.b', 'opacity'), cloudOp: +cs('.ltr-cloud', 'opacity'),
    cgOp: +cs('.ltr-cloud .ltr-cg', 'opacity'), cwOp: +cs('.ltr-cloud .ltr-cw', 'opacity'), blurOp: +cs('.ltr-blur', 'opacity'),
    bubs: [...document.querySelectorAll('.ltr-bub')].map(b => +getComputedStyle(b).opacity), pulseOp: +cs('.ltr-env-pulse', 'opacity'),
    pulseTf: cs('.ltr-env-pulse', 'transform'), envRect: env ? fr(env) : null, heartOp: +cs('.ltr-heart', 'opacity'), flapTf: cs('.ltr-flap', 'transform'),
    veilOp: +cs('.ltr-veil', 'opacity'), isEnd: document.body.classList.contains('is-end'), nav: getComputedStyle(document.getElementById('navBtn')).display,
    bgm: (typeof backgroundMusic !== 'undefined' && backgroundMusic) ? +backgroundMusic.volume.toFixed(3) : null, demo: state.demoRunning,
    cleanup: typeof window.oceanCleanup === 'function' }; }"""
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
        mp, (mx, my, mw) = mask; n = int(round(mw))
        al = np.asarray(Image.open(mp).convert("RGBA").getchannel("A").resize((n, n), Image.LANCZOS)) > 250   # fully opaque: the room behind cannot show through
        M = np.zeros((720, 1280), bool); x0, y0 = int(round(mx)), int(round(my)); h, w = min(n, 720 - y0), min(n, 1280 - x0)
        M[y0:y0 + h, x0:x0 + w] = al[:h, :w]
        res["cloud_mean"] = round(float(d[M].mean()), 2); res["cloud_px_gt60"] = int((d[M] > 60).sum())
    return res
def first(pl, prefix, since=0): return next((x for x in pl if x["src"].startswith(prefix) and x["t"] >= since), None)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(HOOK)
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE)
    def until(base, ms): pg.wait_for_function(f"performance.now() - {base} >= {ms}", timeout=ms + 8000, polling=20)
    ids = pg.evaluate("CARD.slides.map(s => s.id)")
    check("the pages: ... P2, L1 (the letter page), then the end screen (14)", ids == ["T0", "T0B", "T1", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "L1", "CEL"], ids)
    t0 = pg.evaluate("(() => { const t = performance.now(); mountSlide(CARD.slides.findIndex(s => s.id === 'L1')); return t; })()")
    # 1. scene A with the magic shimmer, no आगे, no header
    until(t0, 500); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); magic = first(pl, "sfx_letter_magic")
    check("mounts as a whole-stage page: no आगे, the first scene (538:2) alone, the cleanup hook set", s and s["nav"] == "none" and s["bOp"] == 0 and s["cloudOp"] == 0 and s["pulseOp"] == 0 and s["cleanup"],
          {k: s[k] for k in ("nav", "bOp", "cloudOp", "pulseOp", "cleanup")} if s else s)
    check("the magic shimmer sounds as the page opens", magic is not None and magic["t"] - t0 < 300, round(magic["t"] - t0) if magic else None)
    shot(pg, "l1_a.png")
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
    if cmp_g: check("the grandfather cloud against Figma's 538:39 render: close inside the cloud (mean < 30; frame and region are informative, the room art differs)", cmp_g["cloud_mean"] < 30, cmp_g)
    # 4. the dissolve to white, then the letter with its chime
    until(t0, 8200); s = pg.evaluate(STATE)
    check("at 8.2 s the grandfather is dissolving into the same (white) cloud", 0.05 < s["cgOp"] < 0.95 and 0.05 < s["cwOp"] < 0.95, (s["cgOp"], s["cwOp"]))
    until(t0, 9900); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); idea = first(pl, "sfx_letter_idea")
    check("by 9.9 s the cloud is white and the letter has appeared in it, pulsing and tappable", s["cgOp"] == 0 and s["cwOp"] == 1 and "letter-in" in s["cls"] and "ready" in s["cls"] and s["pulseOp"] == 1 and not s["demo"], s["cls"])
    check("the chime sounded as the letter appeared (9.0 s)", idea is not None and 8900 < idea["t"] - t0 < 9300, round(idea["t"] - t0) if idea else None)
    r = s["envRect"]
    check("the envelope icon: 558:2's size (189 px wide), centred in the cloud at (1020,166)", r and abs(r["w"] - 189) < 3 and abs(r["x"] + r["w"] / 2 - 1020) < 3 and abs(r["y"] + r["h"] / 2 - 166) < 3,
          {k: round(v, 1) for k, v in r.items()} if r else r)
    tf1 = s["pulseTf"]; until(t0, 10200); tf2 = pg.evaluate(STATE)["pulseTf"]
    check("the envelope pulses (its scale changes over 0.3 s)", tf1 != tf2, (tf1, tf2))
    l = shot(pg, "l1_letter.png"); cmp_l = compare(l, "render_558-2.png", "l1_letter", region=(780, 0, 1280, 360))
    if cmp_l: print("INFO the letter stage against Figma's 558:2 render (the designer's cloud differs from the kept one; informative only):", cmp_l)
    # 5. the tap: the pop, the zoom to 610:6, the loop fades out
    bb = pg.locator(".ltr-env-pos").bounding_box()
    t_tap = pg.evaluate("performance.now()"); pg.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
    until(t_tap, 150); pl = pg.evaluate(PLAYS); s = pg.evaluate(STATE); pop = first(pl, "sfx_letter_pop")
    check("the tap: the pop sounds at once and the zoom begins", pop is not None and pop["t"] - t_tap < 250 and "zoom" in s["cls"] and "ready" not in s["cls"], (round(pop["t"] - t_tap) if pop else None, s["cls"]))
    until(t_tap, 1300); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); r = s["envRect"]
    check("1.3 s after the tap the envelope fills the screen as 610:6 (71,-50 1138x758) over the blurred room", r and abs(r["x"] - 71) < 3 and abs(r["y"] + 50) < 3 and abs(r["w"] - 1138) < 4 and s["blurOp"] > 0.99,
          ({k: round(v, 1) for k, v in r.items()} if r else r, s["blurOp"]))
    music = first(pl, "bgm_letter")
    check("the piano loop has faded out by then", music is not None and (music["paused"] or music["vol"] < 0.05), (music["paused"], music["vol"]) if music else None)
    z = shot(pg, "l1_zoom.png"); cmp_z = compare(z, "render_610-6.png", "l1_zoom")
    if cmp_z: check("the full-screen envelope against Figma's 610:6 render: close (mean < 14)", cmp_z["mean"] < 14, cmp_z)   # its backdrop is 610:6's own blurred picture
    # 6. the opening: the paper crackle with the seal popping and the flap swinging; the sheet rises; the veil; the end screen
    paper = first(pl, "sfx_letter_paper")
    check("the paper crackle started as the envelope finished zooming (1.2 s) and the flap is opening", paper is not None and 1150 < paper["t"] - t_tap < 1450 and "open" in s["cls"], (round(paper["t"] - t_tap) if paper else None, s["cls"]))
    until(t_tap, 2100); s = pg.evaluate(STATE)
    check("2.1 s after the tap: the seal has popped off, the flap is turning, the sheet is rising", s["heartOp"] == 0 and s["flapTf"] not in ("none", None) and "paper" in s["cls"], (s["heartOp"], (s["flapTf"] or "")[:40], s["cls"]))
    shot(pg, "l1_open.png")
    pg.wait_for_function("CARD.slides[state.idx].id === 'CEL' && document.body.classList.contains('is-end')", timeout=6000)
    t_end = pg.evaluate("performance.now()")
    check("the end screen follows (about 3.3 s after the tap, after the veil)", 3000 < t_end - t_tap < 4000, round(t_end - t_tap))
    until(t_end, 800); pl = pg.evaluate(PLAYS); bgm = pg.evaluate("(typeof backgroundMusic !== 'undefined' && backgroundMusic) ? backgroundMusic.volume : null")
    page_sounds = [x for x in pl if "letter" in x["src"]]
    check("leaving the page stopped every one of its sounds and gave the engine its music back", len(page_sounds) == 5 and all(x["paused"] for x in page_sounds) and (bgm is None or bgm > 0.05),
          ([(x["src"], x["paused"]) for x in page_sounds], bgm))
    check("no round gate between the letter page and the end screen", not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"))
    shot(pg, "l1_end.png")
    # 7. a re-run from the end screen (the dev nav), then leaving it mid-way: a clean restart, a clean stop
    pg.evaluate("window._plays = []")
    t1 = pg.evaluate("(() => { const t = performance.now(); mountSlide(CARD.slides.findIndex(s => s.id === 'L1')); return t; })()")
    until(t1, 4000); s = pg.evaluate(STATE); pl = pg.evaluate(PLAYS); music = first(pl, "bgm_letter")
    check("re-run from the end screen: the scene restarts from the first picture, the loop starts again", s and "b-in" in s["cls"] and "white" not in s["cls"] and music is not None and not music["paused"], (s["cls"] if s else s, music is not None))
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'P2'))"); pg.wait_for_timeout(500); pl = pg.evaluate(PLAYS)
    check("leaving mid-way (to P2): the page's loop and sounds stop, its hook is cleared, its scene is gone", all(x["paused"] for x in pl if "letter" in x["src"]) and pg.evaluate("window.oceanCleanup == null") and pg.evaluate("!document.querySelector('.ltr')"),
          [(x["src"], x["paused"]) for x in pl if "letter" in x["src"]])
    check("no page errors", not errs, errs[:3])
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
