"""Verify a sentence the child punctuates (PUNCT_PICK) against its Figma frame, its timing and its taps:
   G1 = frame 525:354 "7 G1" ("राजू गेंद से खेल रहा था", पूर्ण विराम), G2 = frame 600:197 "8 G2" ("तुम कहाँ जा रहे हो",
   प्रश्नवाचक चिह्न; the title bar is T4's — its text G3's, "वाक्य सुनिए और सही चिह्न लगाइए ।", since [band-title] 2026-10-28:
   its render's band is 528:424's pasted over its own, the frame still showing T4's line), G3 = frame 528:424 "9 G3" ("बाग में
   गुलाब    गेंदा और चमेली के फूल हैं ।", अल्प विराम; T4's layout with one small slot).
usage: python -I -X utf8 pick_check.py <index.html> <render_1280x720.png> <outdir> [G1|G2|G3]     (default G1)
       renders: g1_figma_render_1280x720.png (G1), g2_... (G2), g3_... (G3)
1. At 1333x750, the page mounted on its own: the title bar appears as the intro line ("वाक्य सुनिए और सही चिह्न लगाइए ।")
   starts to sound and nothing else shows before that line has ended; the picture, the sentence bar and the tiles come
   in 0.5 s after it; the sentence's clip starts once they have landed and its words arrive one by one with it; the
   slot blinks for 3.5 s (three slow blinks) from the moment that clip ends, and the tiles go live in that same moment —
   a tap before then does nothing. A wrong tile wiggles (the engine's wgNo, one --fx-beat), its colours unchanged,
   counts an attempt and stays tappable, and no mark appears; the right one is pressed (the whole option dips — base, face,
   mark and name — since [tile-tap] 2026-10-28), the others dim, its mark lands
   in the slot at once as its name sounds, later taps do nothing, and one beat after the name the page moves on to the
   next slide by itself — no round gate, आगे never shows. The page is the frame's whole stage: no engine header, no
   standing Swiftie, no 🔊 chip; its phase stays "guided"; punct_build_done is reported with the attempts.
2. The engine's idle reminder (once, after ~7 s of quiet with the tiles live) reads the sentence again, each word
   highlighted as the clip reaches it (as on G4 since [word-hot] 2026-10-28: orange #E86A00 with G4's p2WordPop, no yellow
   box); a tap cuts it short and clears the highlight.
3. 1280x720 viewport (= frame px): every element's box vs the frame, the fonts, each text's ink vs the Figma render,
   per-pixel diffs vs the render (less the slot's dashes, whose phase is not the render's), and the mark's ink centred
   in the slot (within 1 px) after the right tap.
"""
import sys, json, pathlib, io
import numpy as np
from playwright.sync_api import sync_playwright
from PIL import Image

html = pathlib.Path(sys.argv[1]).resolve(); target = Image.open(sys.argv[2]).convert("RGB")
out = pathlib.Path(sys.argv[3]).resolve(); out.mkdir(parents=True, exist_ok=True)
SLIDE = sys.argv[4] if len(sys.argv) > 4 else "G1"
T3_TILES = {".t1 .dmf-base": (197, 443, 227, 169), ".t2 .dmf-base": (527, 443, 227, 169), ".t3 .dmf-base": (857, 443, 227, 169),
            ".t1 .dmf-face": (199, 445, 223, 161), ".t2 .dmf-face": (529, 445, 223, 161), ".t3 .dmf-face": (859, 445, 223, 161)}
BIG = lambda x: (365 + x, 211 + 20, 59, 100)   # 519:32's slot, at x in its bar
CONFIG = {   # per page: the next slide, the right tile, its clips, the frame's boxes (frame px), the wrong taps to try,
             # the text regions for the ink comparison and what the pixel diff leaves out (the big slot's dashes: their phase)
  "G1": {"next": "G2", "pick": 0, "sent_clip": "g1_sent", "name_clip": "demo1_purn", "pic_x": 197, "img": (207, 214, 125, 131),   # [g1-pinki] 656:66's places
         "bar": (365, 719), "slot": BIG(612), "sent_c": (365+47.5+560/2, 211+18), "size": 64, "word": "पिंकी", "wrong": [2, 3, 2],
         "tiles": {".t1 .dmf-base": (197, 442, 227, 170), ".t2 .dmf-base": (525, 443, 231, 169), ".t3 .dmf-base": (857, 443, 227, 169),
                   ".t1 .dmf-face": (199, 444, 223, 162), ".t2 .dmf-face": (527, 445, 227, 161), ".t3 .dmf-face": (859, 445, 223, 161)},   # [g1-pinki] the first face 1 px taller
         "ink": {"sentence": (370, 214, 975, 346)}, "own": [(36, 26, 153, 146), (973, 227, 1040, 335)]},   # [g1-pinki] the slot 29 px further right
  "G2": {"next": "G3", "pick": 2, "sent_clip": "g2_sent", "name_clip": "demo2_prashn", "pic_x": 197, "img": (223, 216, 88, 132),   # [g2-girl] the user's picture at its native size
         "bar": (365, 719), "slot": BIG(573), "sent_c": (365+120+479/2, 211+18), "size": 64, "word": "तुम", "wrong": [1, 2, 1],
         "tiles": T3_TILES, "ink": {"sentence": (370, 214, 936, 346)}, "own": [(36, 26, 153, 146), (934, 227, 1001, 335)]},
  # T4's layout: the wide bar, a 50px sentence and one small slot whose dashes are drawn per side — in the pixel diff
  "G3": {"next": "G4", "pick": 1, "sent_clip": "g3_sent", "name_clip": "demo3_alp", "pic_x": 144, "img": (146, 211, 140, 140),
         "bar": (312, 824), "slot": (312+278, 211+70, 33, 38), "sent_c": (312-28+893/2, 211+33), "size": 50, "word": "बाग", "wrong": [1, 3, 1],
         "tiles": T3_TILES, "ink": {"sent: बाग में गुलाब": (330, 236, 590, 336), "sent: गेंदा … हैं ।": (623, 236, 1130, 336)}, "own": [(36, 26, 153, 146)]},
}[SLIDE]
TITLE = "वाक्य सुनिए और सही चिह्न लगाइए ।"   # the title bar's line on G1 / G2 / G3 (G1's instruction line; on G2 since [band-title])
NEXT, PICK, SENT, NAME, WRONG = CONFIG["next"], CONFIG["pick"], CONFIG["sent_clip"], "ok", CONFIG["wrong"]   # [vo-rec] the right tap is praised ("शाबाश!", vo_ok), the mark's name is not said
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)

BX, BW = CONFIG["bar"]
FRAME = dict({   # frame px (box = left, top, width, height), from the Figma metadata of the frame
  ".dmf-band": (36, 26, 1244, 120), ".dmf-pill": (36+3.897, 26+18, 1214.103, 84), ".dmf-head": (36, 26, 116.513, 120),
  ".dmf-head img": (36+5, 26+5, 116.513-10, 120-10),   # [dun-chrome] the engine's live head, filling the circle's padding box (was the frame's 165 px bitmap at -16,5)
  ".dmf-pic": (CONFIG["pic_x"], 211, 144, 139), ".dmf-pic img": CONFIG["img"], ".dmf-bar": (BX, 211, BW, 139),
  ".dmf-bar > .dmf-blank": CONFIG["slot"]}, **CONFIG["tiles"])
CENTRES = {   # text boxes: x centre or left, y centre or top
  ".dmf-pill p": ("l", 36+3.897+139.551, "t", 26+18+18), ".dmf-sent": ("c", CONFIG["sent_c"][0], "t", CONFIG["sent_c"][1]),
  ".t1 .dmf-sym": ("c", 308.5, "c", 501.5), ".t2 .dmf-sym": ("c", 640.5, "c", 492.5), ".t3 .dmf-sym": ("c", 970.5, "c", 502.5),
  ".t1 .dmf-name": ("c", 310.5, "t", 543), ".t2 .dmf-name": ("c", 640.5, "t", 544), ".t3 .dmf-name": ("c", 970.5, "t", 544),
}
INK = dict({"bar text": (176, 48, 760, 126)}, **CONFIG["ink"], **{   # page px regions holding one text each
  "sym 1": (260, 452, 360, 540), "sym 2": (590, 452, 690, 540), "sym 3": (920, 452, 1020, 540),
  "name 1": (255, 540, 400, 585), "name 2": (555, 540, 730, 600), "name 3": (865, 540, 1080, 600)})
OWN = CONFIG["own"]   # left out of the pixel diff
BOXES = """(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
  if (!e) { o[s] = null; continue; } const r = e.getBoundingClientRect(); o[s] = [r.left, r.top, r.width, r.height]; } return o; }"""
GOTO = """(id) => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); mountSlide(CARD.slides.findIndex(s => s.id === id)); }"""
SAMPLE = r"""() => { const a = currentAudio, src = a ? a.src.split('/').pop() : '', m = src.match(/vo_(\w+)\.ogg/);   // [vo-rec] any clip, keyed by its Audio ID without the vo_ prefix
  const q = (s) => document.querySelector(s), has = (s, c) => { const e = q(s); return !!e && e.classList.contains(c); };
  const tiles = [...document.querySelectorAll('.dmf-tile')], blanks = [...document.querySelectorAll('.dmf-blank')], nav = q('#navBtn');
  const anim = (e) => { const cs = getComputedStyle(e); return cs.animationName + '|' + cs.animationDuration + '|' + cs.animationIterationCount; };
  return { clip: m ? m[1] : null, t: a ? a.currentTime : null, playing: isPlaying, slide: CARD.slides[state.idx].id,
    band: has('.dmf-band', 'in'), boxes: has('.dmf-pic', 'in') && has('.dmf-bar', 'in') && tiles.length === 3 && tiles.every(t => t.classList.contains('in')),
    shown: document.querySelectorAll('.dmf-sent .sfig-w.on').length, live: has('.sfig-in', 'dmf-live'),
    blink: blanks.some(b => b.classList.contains('blink')), blinkAnim: blanks.length ? anim(blanks[0]) : '',
    on: tiles.map(t => t.classList.contains('on')), off: tiles.map(t => t.classList.contains('off')),
    wiggle: tiles.map(t => t.classList.contains('wiggle')), marksIn: [...document.querySelectorAll('.dmf-mark')].map(m => m.classList.contains('in')),
    press: (() => { const t = tiles[PICKI]; if (!t) return null; const f = t.querySelector('.dmf-face'), sy = t.querySelector('.dmf-sym'), nm = t.querySelector('.dmf-name');
      return [t.getBoundingClientRect().top, f.getBoundingClientRect().top, sy.getBoundingClientRect().top, nm.getBoundingClientRect().top, getComputedStyle(t).animationName, getComputedStyle(f).animationName]; })(),
    hot: [...document.querySelectorAll('.dmf-sent .sfig-w')].findIndex(w => w.classList.contains('hot')),
    hotLook: (() => { const w = document.querySelector('.dmf-sent .sfig-w.hot'); if (!w) return null; const cs = getComputedStyle(w), r = w.getBoundingClientRect();
      return [cs.color, cs.animationName, cs.animationDuration, cs.backgroundColor, cs.boxShadow, +(r.width / w.offsetWidth).toFixed(3)]; })(),
    attempts: state.attempts, gate: document.getElementById('phaseGate').classList.contains('show'), hand: !!document.querySelector('.reveal-hand.dmf-hand'),
    navShown: nav.classList.contains('visible') && getComputedStyle(nav).display !== 'none', ms: performance.now() }; }"""
SAMPLE = SAMPLE.replace("PICKI", str(PICK))   # [tile-tap] the right tile's press is measured
TIMELINE = "(sample) => { window._tl = []; const S = eval(sample); const step = () => { const s = S(); window._tl.push(s);" \
    " if (s.slide !== 'NEXT') requestAnimationFrame(step); }; requestAnimationFrame(step); }".replace("NEXT", NEXT)
FACES = """[...document.querySelectorAll('.dmf-face')].map(f => { const cs = getComputedStyle(f); return cs.borderTopColor + '|' + cs.boxShadow + '|' + cs.backgroundColor; })"""

def ink_bbox(img, region):
    x0, y0, x1, y1 = region
    a = np.asarray(img.crop(region).convert("RGB"), np.int16); r, b = a[..., 0], a[..., 2]
    m = (r < 140) & (b - r > 55); ys, xs = np.nonzero(m)
    return None if len(xs) == 0 else (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs, bad = [], []

    # ---- 1. timing and taps at 1333x750
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(TIMELINE, SAMPLE); pg.evaluate(GOTO, SLIDE)
    d = pg.evaluate("CARD.slides[state.idx].data"); tS = d["sentence"]["word_times"]; nW = len(tS)
    chrome = pg.evaluate("""() => { const v = (s) => { const e = document.querySelector(s); if (!e) return 'absent';
        const r = e.getBoundingClientRect(); return getComputedStyle(e).display === 'none' || r.width === 0 ? 'hidden' : 'shown'; };
      return { header: v('.header-row'), buddy: v('#swBuddy'), swiftie: v('.sfig-swiftie'), chip: v('.tut-audio'), hint: v('#hintBtn'),
               phase: CARD.slides[state.idx].phase, type: CARD.slides[state.idx].type, frame: !!document.querySelector('.tut-card.sfig-card.sfig-full') }; }""")
    check("the page is the frame's whole stage: no engine header, no standing Swiftie, no hint bulb",
          chrome["frame"] and all(chrome[k] in ("hidden", "absent") for k in ("header", "buddy", "swiftie", "hint")), chrome)
    check(f"{SLIDE} is PUNCT_PICK and its phase stays guided", chrome["type"] == "PUNCT_PICK" and chrome["phase"] == "guided")
    pg.wait_for_function("!!document.querySelector('.dmf-band.in')", timeout=10000, polling=20); pg.wait_for_timeout(700)
    pg.screenshot(path=str(out / "a_band_1333.png"))
    # [band-chip] (2026-10-28) the 🔊 chip is back, at the title bar's bird: G4's header chip at its shoulder spot (66 stage px at
    # 118.6,94.7), in with the bar; grey + untappable through the opening lines (until the tiles are the child's)
    CHIP = """() => { const c = document.querySelector('.tut-audio'); const r = c.getBoundingClientRect(), s = getComputedStyle(c);
      return { bb: [r.left, r.top, r.width, r.height], op: s.opacity, pe: s.pointerEvents, grey: s.filter.startsWith('grayscale(1)'),
               svg: !!c.querySelector('svg .wv1'), wv1: getComputedStyle(c.querySelector('.wv1')).animationName, live: !!document.querySelector('.sfig-in.dmf-live') }; }"""
    chip = pg.evaluate(CHIP)
    check("the 🔊 chip (the engine's speaker SVG) sits at the bar's bird as G4's header chip does: 66x66 at 118.6,94.7 (stage px)",
          chip["svg"] and max(abs(g - e) for g, e in zip(chip["bb"], (118.6, 94.7, 66, 66))) <= 1, [round(v, 1) for v in chip["bb"]])
    check("...grey and untappable through the page's opening lines (as the reference's header chip)",
          not chip["live"] and chip["grey"] and chip["pe"] == "none" and abs(float(chip["op"]) - .5) <= .05, (chip["op"], chip["pe"], chip["grey"]))
    # a tap while the sentence is being read does nothing
    pg.wait_for_function("document.querySelectorAll('.dmf-sent .sfig-w.on').length > 0", timeout=20000, polling=20)
    pg.click(f".dmf-tile.t{WRONG[0]}", force=True); pg.click(f".dmf-tile.t{PICK + 1}", force=True)
    early_tap = pg.evaluate("[state.attempts, !!document.querySelector('.dmf-tile.wiggle, .dmf-tile.on, .dmf-mark.in')]")
    check("a tap while the sentence is still being read does nothing", early_tap == [0, False], early_tap)
    pg.wait_for_function("!!document.querySelector('.sfig-in.dmf-live')", timeout=20000, polling=20); pg.wait_for_timeout(400)
    pg.screenshot(path=str(out / "b_live_blink_1333.png"))
    faces0 = pg.evaluate(FACES)
    # two wrong taps, then the right one
    pg.click(f".dmf-tile.t{WRONG[0]}"); pg.wait_for_timeout(120); pg.screenshot(path=str(out / "c_wrong_wiggle_1333.png"))
    wig = pg.evaluate(f"getComputedStyle(document.querySelector('.dmf-tile.t{WRONG[0]}')).animationName + '|' + getComputedStyle(document.querySelector('.dmf-tile.t{WRONG[0]}')).animationDuration")
    check("a wrong tap shakes that tile with the engine's own wrong-answer wiggle (wgNo, 0.4 s)", wig == "wgNo|0.4s", wig)
    pg.wait_for_timeout(600); faces1 = pg.evaluate(FACES)
    check("...its colours unchanged (face border, shadow, fill as before)", faces1 == faces0, (faces0, faces1))
    quiet = lambda: (pg.wait_for_function("!isPlaying", timeout=15000, polling=20), pg.wait_for_timeout(300))   # [vo-rec] the tap's hint line said
    quiet(); pg.click(f".dmf-tile.t{WRONG[1]}"); pg.wait_for_timeout(700)
    quiet(); pg.click(f".dmf-tile.t{WRONG[2]}"); pg.wait_for_timeout(700)   # the same wrong tile again: it stays tappable
    quiet(); pg.screenshot(path=str(out / "c2_hand_1333.png"))
    pg.click(f".dmf-tile.t{PICK + 1}"); pg.wait_for_timeout(700); pg.screenshot(path=str(out / "d_right_1333.png"))
    pg.click(f".dmf-tile.t{WRONG[1]}", force=True); pg.wait_for_timeout(100)
    check("after the right tap the tiles are done: a further tap does nothing", pg.evaluate("state.attempts === 3 && !document.querySelector('.dmf-tile.wiggle')"))
    pg.wait_for_function(f"CARD.slides[state.idx].id === '{NEXT}'", timeout=30000, polling=20)
    pg.wait_for_timeout(300); pg.screenshot(path=str(out / f"e_{NEXT}_after.png"))
    samples = pg.evaluate("window._tl")
    sig = pg.evaluate(f"GameBus.signals.filter(s => s.slide_id === '{SLIDE}' && s.signal === 'punct_build_done')")
    wrong_sig = pg.evaluate(f"GameBus.signals.filter(s => s.slide_id === '{SLIDE}' && s.signal === 'answer_wrong').length")
    with open(out / "timeline.json", "w", encoding="utf-8") as f: json.dump(samples, f, indent=0)
    ms = lambda i: samples[i]["ms"]
    first = lambda cond, start=0: next(i for i in range(start, len(samples)) if cond(samples[i]))
    start_of = lambda k, i0=0: first(lambda s: s["clip"] == k and s["playing"], i0)
    end_of = lambda k, i0: first(lambda s: s["clip"] == k and not s["playing"], i0)
    mine = [s for s in samples if s["slide"] == SLIDE]
    i_play = first(lambda s: s["clip"] == "g1_intro" and (s["t"] or 0) > 0)
    i_band = first(lambda s: s["band"]); i_end0 = end_of("g1_intro", i_play)
    check("the title bar appears as the intro line starts to sound", abs(ms(i_band) - ms(i_play)) <= 150 and not samples[0]["band"],
          f"bar at {ms(i_band) - ms(i_play):+.0f} ms from the clip's first played moment")
    check("nothing else shows while the intro line sounds", not any(s["boxes"] or s["shown"] or s["live"] for s in samples[:i_end0]))
    i_boxes = first(lambda s: s["boxes"])
    check("the picture, the bar and the tiles come in 0.5 s after the intro", 450 <= ms(i_boxes) - ms(i_end0) <= 800, f"{ms(i_boxes) - ms(i_end0):.0f} ms")
    i_s1 = start_of(SENT); i_e1 = end_of(SENT, i_s1)
    check("the sentence's clip starts once they have landed (~0.65 s)", 600 <= ms(i_s1) - ms(i_boxes) <= 1000, f"{ms(i_s1) - ms(i_boxes):.0f} ms")
    timed = [s for s in samples[i_s1:i_e1] if s["clip"] == SENT and s["playing"] and s["t"] is not None]
    early = [s for s in timed if s["shown"] > sum(1 for t in tS if s["t"] + 0.04 >= t)]
    late = [s for s in timed if s["shown"] < sum(1 for t in tS if s["t"] - 0.15 >= t)]
    check("the words arrive one by one with the clip, none early, none >150 ms late",
          len(timed) > 20 and len({s["shown"] for s in timed}) >= nW - 1 and not early and not late,
          f"{len(timed)} samples, {len({s['shown'] for s in timed})} distinct counts / {nW} words, early {len(early)}, late {len(late)}")
    i_bl = first(lambda s: s["blink"]); i_live = first(lambda s: s["live"])
    check("the slot blinks and the tiles go live the moment the sentence's clip ends", 0 <= ms(i_bl) - ms(i_e1) <= 150 and abs(ms(i_live) - ms(i_bl)) <= 20,
          f"blink {ms(i_bl) - ms(i_e1):.0f} ms after, live {ms(i_live) - ms(i_bl):+.0f} ms from the blink")
    name, dur, count = samples[i_bl]["blinkAnim"].split("|")
    period = float(dur[:-2]) / 1000 if dur.endswith("ms") else float(dur[:-1])
    check("the blink is T3's: three slow blinks of ~1.17 s", name == "dmfBlink" and count == "3" and abs(period * 3 - 3.5) < 0.05, samples[i_bl]["blinkAnim"])
    i_w1 = first(lambda s: s["attempts"] == 1); i_w2 = first(lambda s: s["attempts"] == 2); i_w3 = first(lambda s: s["attempts"] == 3)
    only = lambda t: [k + 1 == t for k in range(3)]
    check(f"each wrong tap counts an attempt and wiggles that tile only ({', '.join(d['options'][t - 1]['name_hi'] for t in WRONG)})",
          samples[i_w1]["wiggle"] == only(WRONG[0]) and samples[i_w2]["wiggle"] == only(WRONG[1]) and samples[i_w3]["wiggle"] == only(WRONG[2]))
    i_ok = first(lambda s: any(s["on"]))
    check("no mark, no pressed or dimmed tile before the right tap", not any(any(s["marksIn"]) or any(s["on"]) or any(s["off"]) for s in samples[:i_ok]))
    i_mark = first(lambda s: any(s["marksIn"]))
    # [tile-tap] the press is the whole option's: the tile, its face, mark and name dip together (dmfTap: 6 frame px at 35% of .45 s) and
    # come back; the face has no press of its own
    pre = samples[i_ok - 1]["press"]; win = [s for s in samples[i_ok:] if s["ms"] - ms(i_ok) <= 500 and s["press"]]; k = 1333 / 1280
    deep = max(([s["press"][j] - pre[j] for j in range(4)] for s in win), key=lambda v: v[0])
    check("the right tap presses the whole option: tile, face, mark and name dip together by 6 px (frame px) and come back; the face has no press of its own",
          5.0 <= deep[0] / k <= 7.0 and max(abs(v - deep[0]) for v in deep) <= 0.6 and any(s["press"][4] == "dmfTap" for s in win)
          and all(s["press"][5] == "none" for s in win) and abs(win[-1]["press"][0] - pre[0]) <= 0.6,
          f"deepest dip tile / face / mark / name {[round(v / k, 2) for v in deep]} px; animations seen {sorted({(s['press'][4], s['press'][5]) for s in win})}")
    check("the right tap: its tile pressed, the other two dim, its mark in the slot at once",
          samples[i_ok]["on"] == [k == PICK for k in range(3)] and samples[i_ok]["off"] == [k != PICK for k in range(3)] and ms(i_mark) - ms(i_ok) <= 160, f"mark {ms(i_mark) - ms(i_ok):.0f} ms after")   # [dun-chrome] the reference's 100-piece 1.5x burst is built on this tap: ~100 ms (was 50 with the 80-piece burst)
    i_bl_end = first(lambda s: not s["blink"], i_bl)
    check("the blink stops at the right tap if it is still running, else after its 3.5 s",
          (i_bl_end <= i_ok and abs(ms(i_bl_end) - ms(i_bl) - 3500) <= 150) or abs(ms(i_bl_end) - ms(i_ok)) <= 50, f"{ms(i_bl_end) - ms(i_bl):.0f} ms")
    i_s2 = start_of(NAME, i_ok); i_e2 = end_of(NAME, i_s2)
    check("the praise (“शाबाश!”, vo_ok) sounds as the tile is tapped — the mark's name is not said", 0 <= ms(i_s2) - ms(i_ok) <= 200, f"{ms(i_s2) - ms(i_ok):.0f} ms after")
    check(f"one beat (~1 s) after the praise the page moves on to {NEXT} by itself, with no round gate",
          samples[-1]["slide"] == NEXT and 900 <= ms(len(samples) - 1) - ms(i_e2) <= 1400 and not any(s["gate"] for s in samples),
          f"{ms(len(samples) - 1) - ms(i_e2):.0f} ms after the praise")
    # [vo-rec] the deck's hint ladder on the wrong taps: hint 1, hint 2, then hint 3 (hint 2 again where the page has none) with
    # the pointing hand under the right tile, gone at the right tap; each line 0.5 s after its tap
    H1, H2 = (d.get("hint1_audio") or "")[3:], (d.get("hint2_audio") or "")[3:]; H3 = (d.get("hint3_audio") or d.get("hint2_audio") or "")[3:]
    i_h1 = start_of(H1, i_w1); i_h2 = start_of(H2, i_w2); i_h3 = start_of(H3, i_w3)
    check(f"wrong tap 1: hint 1 ({H1}) 0.5 s after the wiggle; wrong tap 2: hint 2 ({H2}); wrong tap 3: hint 3 ({H3}" + (", hint 2 again)" if H3 == H2 else ")"),
          all(450 <= ms(i) - ms(w) <= 800 for i, w in ((i_h1, i_w1), (i_h2, i_w2), (i_h3, i_w3))) and i_h1 < i_w2 and i_h2 < i_w3,
          [round(ms(i) - ms(w)) for i, w in ((i_h1, i_w1), (i_h2, i_w2), (i_h3, i_w3))])
    check("the pointing hand (.reveal-hand.dmf-hand) comes with the third wrong tap, under the right tile, and goes at the right tap",
          not any(s["hand"] for s in samples[:i_w3]) and samples[i_h3]["hand"] and all(not s["hand"] for s in samples[i_ok + 2:]),
          (any(s["hand"] for s in samples[:i_w3]), samples[i_h3]["hand"], any(s["hand"] for s in samples[i_ok + 2:])))
    check("आगे never shows on this page", not any(s["navShown"] for s in mine))
    # counted on this page's samples only: the next page may open with the same clip (G2 replays G1's instruction)
    starts = lambda k: sum(1 for i, s in enumerate(mine) if s["clip"] == k and s["playing"] and (i == 0 or not (mine[i-1]["clip"] == k and mine[i-1]["playing"])))
    check("each clip plays once on this page (the hint lines as the ladder says; no idle reminder: the taps came within 7 s)",
          all(starts(k) == 1 for k in ("g1_intro", SENT, NAME, H1)) and starts(H2) == (2 if H3 == H2 else 1) and (H3 == H2 or starts(H3) == 1),
          [starts(k) for k in ("g1_intro", SENT, NAME, H1, H2, H3)])
    check("punct_build_done is reported once, with the two wrong tiles counted (3 wrong taps)",
          len(sig) == 1 and sig[0]["first_try"] is False and sig[0]["wrong"] == 3 and wrong_sig == 3, (sig, wrong_sig))
    pg.close()

    # ---- 2. the idle reminder: the sentence again, words highlighted as read; a tap cuts it short
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(TIMELINE, SAMPLE); pg.evaluate(GOTO, SLIDE)
    pg.wait_for_function("!!document.querySelector('.sfig-in.dmf-live')", timeout=20000, polling=20)
    t_live = pg.evaluate("performance.now()")
    pg.wait_for_function("document.querySelectorAll('.dmf-sent .sfig-w.hot').length > 0", timeout=15000, polling=20)
    t_hot = pg.evaluate("performance.now()"); pg.screenshot(path=str(out / "f_idle_reminder_1333.png"))
    pg.wait_for_function("!isPlaying && !document.querySelector('.dmf-sent .sfig-w.hot')", timeout=10000, polling=20)
    pg.wait_for_timeout(9000)   # the engine gives one reminder per slide
    samples = pg.evaluate("window._tl")
    i_l = next(i for i, s in enumerate(samples) if s["live"])
    reps = [i for i in range(i_l + 1, len(samples)) if samples[i]["clip"] == SENT and samples[i]["playing"] and not (samples[i-1]["clip"] == SENT and samples[i-1]["playing"])]
    check("~7 s of quiet with the tiles live: the engine's idle reminder reads the sentence again — once", len(reps) == 1 and 6500 <= samples[reps[0]]["ms"] - samples[i_l]["ms"] <= 9000,
          f"{len(reps)} replay(s), first {samples[reps[0]]['ms'] - samples[i_l]['ms']:.0f} ms after the tiles went live" if reps else "none")
    if reps:
        r0 = reps[0]; r1 = next(i for i in range(r0, len(samples)) if not samples[i]["playing"])
        timed = [s for s in samples[r0:r1] if s["clip"] == SENT and s["playing"] and s["t"] is not None]
        # n words reached -> the first word lit: the first one sharing word n-1's start (a punctuation-only word lights
        # with the word before it, "हैं ।")
        lead = lambda n: tS.index(tS[n - 1]) if n > 0 else -1
        off = [s for s in timed if s["hot"] not in {lead(n) for n in range(sum(1 for t in tS if s["t"] - 0.15 >= t), sum(1 for t in tS if s["t"] + 0.04 >= t) + 1)}]
        want = {lead(n) for n in range(2, nW + 1)}   # the first word may already be lit when the sampling catches the clip
        check("...each word highlighted as the reminder reaches it, the highlight gone after", len(timed) > 20 and not off and {s["hot"] for s in timed} >= want and samples[min(r1 + 5, len(samples) - 1)]["hot"] == -1,
              f"{len(timed)} samples, words seen {sorted({s['hot'] for s in timed})}, off-time {len(off)}")
        # [word-hot] the lit word looks and moves as G4's: the picks' orange, G4's p2WordPop (.28 s, up to a 1.1 scale), no yellow box
        looks = {tuple(s["hotLook"][:5]) for s in timed if s["hotLook"]}; k = 1333 / 1280; pops = [s["hotLook"][5] / k for s in timed if s["hotLook"]]
        check("...the word being read lit as on G4: orange #E86A00 with G4's p2WordPop (.28 s, up to a 1.1 scale), no yellow box or shadow",
              looks == {("rgb(232, 106, 0)", "p2WordPop", "0.28s", "rgba(0, 0, 0, 0)", "none")} and bool(pops) and 1.07 <= max(pops) <= 1.13 and min(pops) >= 0.98,
              f"looks {sorted(looks)}, pop {min(pops) if pops else 0:.3f}-{max(pops) if pops else 0:.3f}")
    check("...and the tiles stay live meanwhile", all(s["live"] for s in samples[i_l:]))
    pg.close()
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(GOTO, SLIDE)
    pg.wait_for_function("document.querySelectorAll('.dmf-sent .sfig-w.hot').length > 0", timeout=30000, polling=20); pg.wait_for_timeout(300)
    pg.click(f".dmf-tile.t{WRONG[0]}"); pg.wait_for_timeout(350)
    cut = pg.evaluate("[isPlaying, document.querySelectorAll('.dmf-sent .sfig-w.hot').length, state.attempts]")
    check("a tap during the reminder cuts it short and clears the highlight (the tap still counts)", cut == [False, 0, 1], cut)
    pg.wait_for_function("isPlaying", timeout=3000, polling=20)   # [vo-rec] hint 1 follows, 0.5 s after the tap
    h = pg.evaluate("currentAudio ? currentAudio.src.split('/').pop() : null")
    check("...and hint 1 follows it half a second later", h == f"vo_{(d.get('hint1_audio') or '')[3:]}.ogg", h)
    pg.close()

    # ---- 2b. [band-chip] the 🔊 chip: live (colour, tappable) once the tiles are the child's and nothing speaks; a tap reads the
    #      sentence again, word by word, the chip grey with its arcs blinking meanwhile; back to colour after
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(GOTO, SLIDE)
    pg.wait_for_function("!!document.querySelector('.sfig-in.dmf-live') && !isPlaying", timeout=30000, polling=20); pg.wait_for_timeout(150)
    c_live = pg.evaluate(CHIP)
    check("the 🔊 chip goes live (colour, tappable, arcs solid) the moment the tiles are the child's and nothing speaks",
          c_live["live"] and not c_live["grey"] and c_live["pe"] == "auto" and c_live["op"] == "1" and c_live["wv1"] == "none", (c_live["op"], c_live["pe"], c_live["grey"], c_live["wv1"]))
    pg.click(".tut-audio"); pg.wait_for_timeout(500)
    c_tap = pg.evaluate("""() => { const a = currentAudio; return [isPlaying, a ? a.src.split('/').pop().split('?')[0] : null, document.querySelectorAll('.dmf-sent .sfig-w.hot').length]; }""")
    c_mid = pg.evaluate(CHIP)
    check("a tap on it reads the sentence again, each word highlighted as it is read (the idle reminder's read)",
          c_tap[0] and c_tap[1] == f"vo_{SENT}.ogg" and c_tap[2] >= 1, c_tap)
    check("...the chip grey and untappable while it reads, its arcs blinking", c_mid["grey"] and c_mid["pe"] == "none" and c_mid["wv1"] == "wv1", (c_mid["grey"], c_mid["pe"], c_mid["wv1"]))
    pg.wait_for_function("!isPlaying", timeout=15000, polling=20); pg.wait_for_timeout(200)
    c_after = pg.evaluate(CHIP)
    check("...and in colour, tappable, arcs solid again once the read is over; the tiles still live",
          c_after["live"] and not c_after["grey"] and c_after["pe"] == "auto" and c_after["op"] == "1" and c_after["wv1"] == "none", (c_after["op"], c_after["pe"], c_after["grey"]))
    pg.close()

    # ---- 3. geometry + pixel diff at 1280x720, at the frame's moment (sentence shown, slot empty, tiles plain)
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(GOTO, SLIDE)
    pg.wait_for_function("!!document.querySelector('.dmf-blank.blink')", timeout=30000, polling=20)
    pg.evaluate("document.querySelectorAll('.dmf-blank').forEach(b => b.classList.remove('blink'))"); pg.wait_for_timeout(350)
    shot = out / "g_frame_1280.png"; pg.screenshot(path=str(shot))
    # [band-chip] the 🔊 chip is the engine's, not the frame's (like the bar's live bird head): its box, plus its shadow, is left out
    # of the pixel diff — measured, not assumed, so a chip off its place still fails the box check above
    cb = pg.evaluate(BOXES, [".tut-audio"])[".tut-audio"]
    OWN = list(OWN) + [(int(cb[0]) - 8, int(cb[1]) - 6, int(cb[0] + cb[2]) + 9, int(cb[1] + cb[3]) + 12)]
    boxes = pg.evaluate(BOXES, list(FRAME) + list(CENTRES)); worst = 0
    print("== boxes vs the frame (px) ==")
    for sel, exp in FRAME.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, dd)
        print(f"  {sel:38s} got {[round(v,2) for v in got]}  frame {[round(v,3) for v in exp]}  max|d|={dd:.2f}")
    for sel, (kx, x, ky, y) in CENTRES.items():
        g = boxes[sel]; gx = g[0] + g[2] / 2 if kx == "c" else g[0]; gy = g[1] + g[3] / 2 if ky == "c" else g[1]
        dd = max(abs(gx - x), abs(gy - y)); worst = max(worst, dd)
        print(f"  {sel:38s} got ({gx:.2f}, {gy:.2f})  frame ({x}, {y})  max|d|={dd:.2f}")
    check("every box and text box within 1 px of the frame", worst <= 1.0, f"worst {worst:.2f}px")
    fonts = pg.evaluate("""[getComputedStyle(document.querySelector('.dmf-pill p')).fontSize, getComputedStyle(document.querySelector('.dmf-sent')).fontSize,
      getComputedStyle(document.querySelector('.dmf-sym')).fontSize, getComputedStyle(document.querySelector('.dmf-name')).fontSize,
      document.fonts.check("600 32px 'Story Noto Sans Devanagari'", 'वाक्य'), document.fonts.check("600 SIZEpx 'Story Noto Sans Devanagari'", 'WORD')]""".replace("WORD", CONFIG["word"]).replace("SIZE", str(CONFIG["size"])))
    check(f"fonts: Noto Sans Devanagari SemiBold — 32px bar, {CONFIG['size']}px sentence, 64px marks, 28px names", fonts == ["32px", f"{CONFIG['size']}px", "64px", "28px", True, True], fonts)
    band_text = pg.evaluate("document.querySelector('.dmf-pill p').textContent")
    check("the title bar's line is G1's instruction line, " + TITLE, band_text == TITLE, band_text)
    mine_img = Image.open(shot).convert("RGB")
    print("== text ink vs the Figma render (page px): centre and size ==")
    worst_c = worst_s = 0
    for name, region in INK.items():
        a, t = ink_bbox(mine_img, region), ink_bbox(target, region)
        if not a or not t: print(f"  {name:20s} NO INK {a} {t}"); worst_c = 99; continue
        dc = ((a[0] + a[2]) / 2 - (t[0] + t[2]) / 2, (a[1] + a[3]) / 2 - (t[1] + t[3]) / 2)
        ds = ((a[2] - a[0]) - (t[2] - t[0]), (a[3] - a[1]) - (t[3] - t[1]))
        worst_c = max(worst_c, abs(dc[0]), abs(dc[1])); worst_s = max(worst_s, abs(ds[0]), abs(ds[1]))
        print(f"  {name:20s} mine {tuple(int(v) for v in a)}  figma {tuple(int(v) for v in t)}  centre d=({dc[0]:+.1f},{dc[1]:+.1f})  size d=({ds[0]:+d},{ds[1]:+d})")
    check("each text's ink sits where the render's does (centre within 1.5 px, size within 3 px)", worst_c <= 1.5 and worst_s <= 3, f"centre {worst_c:.1f}px, size {worst_s}px")
    A = np.asarray(mine_img, np.int16); B = np.asarray(target, np.int16)
    pad = np.pad(B, ((1, 1), (1, 1), (0, 0)), mode="edge")
    near = np.min([np.abs(A - pad[1+dy:1+dy+A.shape[0], 1+dx:1+dx+A.shape[1]]).max(axis=2) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
    keep = np.ones(near.shape, bool)
    for x0, y0, x1, y1 in OWN: keep[y0:y1, x0:x1] = False
    m = (near > 32) & keep; px = int(keep.sum())
    solid = m.copy(); solid[1:-1, 1:-1] &= m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:]
    solid[0, :] = solid[-1, :] = False; solid[:, 0] = solid[:, -1] = False
    what = "less the slot's ring" if OWN else "the slot's dashes included"
    print(f"  pixel diff vs Figma render over the whole frame, {what} (within 1 px): {int(m.sum())} of {px} px"
          f" ({100*m.sum()/px:.2f}%), of them solid: {int(solid.sum())} ({100*solid.sum()/px:.3f}%)")
    Image.fromarray(np.where(m, 255, np.where(keep, 0, 60)).astype(np.uint8)).save(out / "g_diff_mask.png")
    check("the whole frame pixel-matches the Figma render (>32-level diffs under 3%, solid diffs under 0.05% of the area)", m.sum() / px < 0.03 and solid.sum() / px < 0.0005)
    # the mark's INK on the slot's centre after the right tap
    pg.wait_for_function("!!document.querySelector('.sfig-in.dmf-live')", timeout=20000, polling=20)
    pg.click(f".dmf-tile.t{PICK + 1}"); pg.wait_for_timeout(600)
    x, y, w, h = pg.evaluate("(() => { const r = document.querySelector('.dmf-blank').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; })()")
    a = np.asarray(Image.open(io.BytesIO(pg.screenshot(path=str(out / "h_mark_in_1280.png")))).convert("RGB"), np.int16)
    x0, y0, x1, y1 = int(x) + 3, int(y) + 3, int(x + w) - 3, int(y + h) - 3
    a = a[y0:y1, x0:x1]; mm = (a[..., 0] < 60) & (a[..., 2] < 170) & (a[..., 2] - a[..., 0] > 55); ys, xs = np.nonzero(mm)
    dx = (x0 + xs.min() + x0 + xs.max() + 1) / 2 - (x + w / 2); dy = (y0 + ys.min() + y0 + ys.max() + 1) / 2 - (y + h / 2)
    check(f"the mark's ({d['mark']}) ink sits on the slot's centre after the right tap (within 1 px)", abs(dx) <= 1 and abs(dy) <= 1, f"({dx:+.2f}, {dy:+.2f}), ink {xs.max() - xs.min() + 1}x{ys.max() - ys.min() + 1}")
    pg.close()
    b.close()
check("no page errors", not errs, errs[:3]); check("no failed requests", not bad, bad[:5])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
