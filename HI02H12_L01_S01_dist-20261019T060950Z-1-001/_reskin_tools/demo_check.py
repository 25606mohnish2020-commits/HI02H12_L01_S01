"""Verify a run-on sentence demo page (PUNCT_DEMO) against its Figma frame and its timing:
   T2 = frame 519:32 ("रीना स्कूल जा रही है", पूर्ण विराम), T3 = frame 521:288 ("तुम्हारा नाम क्या है", प्रश्नवाचक चिह्न),
   T4 = frame 523:320 ("मेरे पास आम केला सेब और संतरा है ।", अल्प विराम, two slots).
usage: python -I -X utf8 demo_check.py <index.html> <render_1280x720.png> <outdir> [T2|T3|T4]     (default T2)
       renders: demo1_figma_render_1280x720.png (T2), demo2_... (T3), demo3_... (T4)
1. At 1333x750, the page mounted on its own: the title bar appears as the intro line starts to sound and nothing else
   shows before that line has ended; the picture, the sentence bar and the tiles come in 0.5 s after it; the sentence's
   clip starts once they have landed and its words arrive one by one (none early, none >150 ms late); the empty slot(s)
   blink for 3.5 s from the moment that clip ends — every slot the same animation, starting and stopping in the same
   frame — nothing sounding meanwhile; then the mark's name sounds with its tile tapped and the other two dim; the mark
   lands in each slot after that line (left to right, 0.3 s apart); the sentence's second reading follows, every tile
   dim, each word and each slot highlighted as the reading reaches it; 1.5 s after it the slots' boxes go and the page
   moves on by itself (T4: through the engine's peek gate into the guided round, as the old T4 did); आगे never shows.
   The blink is three slow blinks; the tapped tile keeps its colours (no blue ring).
2. No standing Swiftie and no 🔊 chip on this page; the tutorial card is the whole stage.
3. 1280x720 viewport (= frame px): every element's box vs the frame, the fonts, each text's ink vs the Figma render,
   per-pixel diffs vs the render (T2/T3 less the big slot's dashes, whose phase is not the render's), and the mark's
   ink centred in every slot (within 1 px) once it has landed and while that slot is highlighted.
"""
import sys, json, pathlib, io
import numpy as np
from playwright.sync_api import sync_playwright
from PIL import Image

html = pathlib.Path(sys.argv[1]).resolve(); target = Image.open(sys.argv[2]).convert("RGB")
out = pathlib.Path(sys.argv[3]).resolve(); out.mkdir(parents=True, exist_ok=True)
SLIDE = sys.argv[4] if len(sys.argv) > 4 else "T2"
BIG = [(583, 20, 59, 100)]    # 519:32's slot, in the bar's frame px
CONFIG = {   # per page: its clips, the mark's clip, the tapped tile, the frame's boxes (frame px), the next slide
  "T2": {"page": "demo1", "mark_clip": "purn", "pick": 0, "pic_x": 197, "img": (227, 221, 80.052, 120), "bar": (365, 719),
         "sent": (100, 18, 479, 64), "slots": BIG, "word": "रीना", "own": [(944, 227, 1011, 335)],
         "ink": {"sentence": (380, 214, 944, 346)}, "content": (170, 20, 1280, 620),
         "next": "T3", "gate": False, "next_ok": "CARD.slides[state.idx].type === 'PUNCT_DEMO' && !!document.querySelector('.sfig-full .dmf-band')",
         "next_what": "the second demo (PUNCT_DEMO)"},
  "T3": {"page": "demo2", "mark_clip": "prashn", "pick": 2, "pic_x": 197, "img": (204, 215, 130, 128), "bar": (365, 719),
         "sent": (120, 18, 479, 64), "slots": BIG, "word": "तुम्हारा", "own": [(944, 227, 1011, 335)],
         "ink": {"sentence": (380, 214, 944, 346)}, "content": (170, 20, 1280, 620),
         "next": "T4", "gate": False, "next_ok": "CARD.slides[state.idx].type === 'PUNCT_DEMO' && !!document.querySelector('.sfig-full .dmf-band')",
         "next_what": "the third demo (PUNCT_DEMO)"},
  "T4": {"page": "demo3", "mark_clip": "alp", "pick": 1, "pic_x": 144, "img": (144, 229, 144, 96), "bar": (312, 824),
         "sent": (-34, 33, 893, 50), "slots": [(286, 76, 33, 38), (417, 76, 33, 38)], "word": "मेरे", "own": [],
         # the sentence's ink in three parts — before, between and after the slots — so each word run is placed
         "ink": {"sent: मेरे पास आम": (330, 232, 614, 330), "sent: केला": (614, 232, 745, 330), "sent: सेब … है ।": (745, 232, 1125, 330)},
         "content": (130, 20, 1280, 620),
         "next": "G1", "gate": True, "next_ok": "CARD.slides[state.idx].type === 'PUNCT_PICK' && !!document.querySelector('.sfig-full .dmf-band')",
         "next_what": "the first sentence the child punctuates (PUNCT_PICK, the Figma frame 525:354 — see pick_check.py)"},
}[SLIDE]
NEXT, PICK, MK, NS = CONFIG["next"], CONFIG["pick"], CONFIG["mark_clip"], len(CONFIG["slots"])
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)

AS_T0 = {".tut-card.sfig-card": (0, 0, 1333, 750)}
BX, BW = CONFIG["bar"]
FRAME = {   # frame px (box = left, top, width, height), from the Figma metadata of the frame
  ".dmf-band": (36, 26, 1244, 120), ".dmf-pill": (36+3.897, 26+18, 1214.103, 84), ".dmf-head": (36, 26, 116.513, 120),
  ".dmf-head img": (36-16, 26+5, 165, 165),
  ".dmf-pic": (CONFIG["pic_x"], 211, 144, 139), ".dmf-pic img": CONFIG["img"], ".dmf-bar": (BX, 211, BW, 139),
  ".t1 .dmf-base": (197, 443, 227, 169), ".t2 .dmf-base": (527, 443, 227, 169), ".t3 .dmf-base": (857, 443, 227, 169),
  ".t1 .dmf-face": (199, 445, 223, 161), ".t2 .dmf-face": (529, 445, 223, 161), ".t3 .dmf-face": (859, 445, 223, 161),
}
for k, (x, y, w, h) in enumerate(CONFIG["slots"]): FRAME[f".dmf-bar > .dmf-blank:nth-of-type({k + 1})"] = (BX + x, 211 + y, w, h)
SX, SY, SW, SZ = CONFIG["sent"]
CENTRES = {   # text boxes: x centre or left, y centre or top
  ".dmf-pill p": ("l", 36+3.897+139.551, "t", 26+18+18), ".dmf-sent": ("c", BX+SX+SW/2, "t", 211+SY),
  ".t1 .dmf-sym": ("c", 308.5, "c", 501.5), ".t2 .dmf-sym": ("c", 640.5, "c", 492.5), ".t3 .dmf-sym": ("c", 970.5, "c", 502.5),
  ".t1 .dmf-name": ("c", 310.5, "t", 543), ".t2 .dmf-name": ("c", 640.5, "t", 544), ".t3 .dmf-name": ("c", 970.5, "t", 544),
}
INK = dict(CONFIG["ink"], **{   # page px regions holding one text each, for the ink-vs-render comparison
  "bar text": (176, 48, 760, 126), "sym 1": (260, 452, 360, 540), "sym 2": (590, 452, 690, 540), "sym 3": (920, 452, 1020, 540),
  "name 1": (255, 540, 400, 585), "name 2": (555, 540, 730, 600), "name 3": (865, 540, 1080, 600)})
OWN = CONFIG["own"]          # left out of the pixel diff
CONTENT = CONFIG["content"]
BOXES = """(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
  if (!e) { o[s] = null; continue; } const r = e.getBoundingClientRect(); o[s] = [r.left, r.top, r.width, r.height]; } return o; }"""
GOTO = """(id) => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); mountSlide(CARD.slides.findIndex(s => s.id === id)); }"""
SAMPLE = r"""() => { const a = currentAudio, src = a ? a.src.split('/').pop() : '', m = src.match(/vo_PAGE_(\w+)\.ogg/);
  const q = (s) => document.querySelector(s), has = (s, c) => { const e = q(s); return !!e && e.classList.contains(c); };
  const tiles = [...document.querySelectorAll('.dmf-tile')], blanks = [...document.querySelectorAll('.dmf-blank')], nav = q('#navBtn');
  const anim = (e) => { const cs = getComputedStyle(e); return cs.animationName + '|' + cs.animationDuration + '|' + cs.animationIterationCount; };
  return { clip: m ? m[1] : null, t: a ? a.currentTime : null, playing: isPlaying, slide: CARD.slides[state.idx].id,
    band: has('.dmf-band', 'in'), boxes: has('.dmf-pic', 'in') && has('.dmf-bar', 'in') && tiles.length === 3 && tiles.every(t => t.classList.contains('in')),
    shown: document.querySelectorAll('.dmf-sent .sfig-w.on').length,
    nSlots: blanks.length, blinkN: blanks.filter(b => b.classList.contains('blink')).length, blinkAnims: blanks.filter(b => b.classList.contains('blink')).map(anim),
    on: tiles.map(t => t.classList.contains('on')), off: tiles.map(t => t.classList.contains('off')),
    marksIn: [...document.querySelectorAll('.dmf-mark')].map(m => m.classList.contains('in')),
    hot: [...document.querySelectorAll('.dmf-sent .sfig-w')].findIndex(w => w.classList.contains('hot')), hotSlot: blanks.findIndex(b => b.classList.contains('hot')),
    gone: blanks.length > 0 && blanks.every(b => b.classList.contains('gone')), gate: !!document.getElementById('phaseGate') && document.getElementById('phaseGate').classList.contains('show'),
    face1: (() => { const f = q('.tPICK .dmf-face'); if (!f) return ''; const cs = getComputedStyle(f); return cs.borderTopColor + '|' + cs.boxShadow; })(),
    navShown: nav.classList.contains('visible') && getComputedStyle(nav).display !== 'none', ms: performance.now() }; }"""
SAMPLE = SAMPLE.replace("PAGE", CONFIG["page"]).replace("tPICK", "t" + str(PICK + 1))
TIMELINE = "(sample) => { window._tl = []; const S = eval(sample); const step = () => { const s = S(); window._tl.push(s);" \
    " if (s.slide !== 'NEXT') requestAnimationFrame(step); }; requestAnimationFrame(step); }"
TIMELINE = TIMELINE.replace("NEXT", NEXT)

def ink_bbox(img, region):
    x0, y0, x1, y1 = region
    a = np.asarray(img.crop(region).convert("RGB"), np.int16); r, b = a[..., 0], a[..., 2]
    m = (r < 140) & (b - r > 55); ys, xs = np.nonzero(m)
    return None if len(xs) == 0 else (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs, bad = [], []

    # ---- 1-2. timing at 1333x750
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(TIMELINE, SAMPLE); pg.evaluate(GOTO, SLIDE)
    d = pg.evaluate("CARD.slides[state.idx].data"); tS, tF = d["sentence"]["word_times"], d["full"]["word_times"]; nW = len(tS)
    targets = d["full"].get("targets") or [f"w{i}" if i < nW else "s0" for i in range(len(tF))]
    pg.wait_for_function("!!document.querySelector('.dmf-band.in')", timeout=10000, polling=20); pg.wait_for_timeout(700)
    pg.screenshot(path=str(out / "a_band_1333.png"))
    pg.wait_for_function("!!document.querySelector('.dmf-blank.blink')", timeout=20000, polling=20); pg.wait_for_timeout(100)
    pg.screenshot(path=str(out / "b_sentence_blink_1333.png"))
    pg.wait_for_function("!!document.querySelector('.dmf-tile.on')", timeout=20000, polling=20); pg.wait_for_timeout(600)
    pg.screenshot(path=str(out / "c_tapped_1333.png"))
    pg.wait_for_function("!!document.querySelector('.dmf-blank.hot')", timeout=20000, polling=20); pg.wait_for_timeout(150)
    pg.screenshot(path=str(out / "d_mark_hot_1333.png"))
    pg.wait_for_function("document.querySelectorAll('.dmf-blank.gone').length > 0", timeout=30000, polling=20); pg.wait_for_timeout(300)
    pg.screenshot(path=str(out / "e_end_1333.png"))
    pg.wait_for_function(f"CARD.slides[state.idx].id === '{NEXT}'", timeout=30000, polling=20)
    pg.wait_for_timeout(300); pg.screenshot(path=str(out / f"f_{NEXT}_after.png"))
    samples = pg.evaluate("window._tl")
    with open(out / "timeline.json", "w", encoding="utf-8") as f: json.dump(samples, f, indent=0)
    ms = lambda i: samples[i]["ms"]
    first = lambda cond, start=0: next(i for i in range(start, len(samples)) if cond(samples[i]))
    start_of = lambda k, i0=0: first(lambda s: s["clip"] == k and s["playing"], i0)
    end_of = lambda k, i0: first(lambda s: s["clip"] == k and not s["playing"], i0)
    mine = [s for s in samples if s["slide"] == SLIDE]
    i_play = first(lambda s: s["clip"] == "intro" and (s["t"] or 0) > 0)
    i_band = first(lambda s: s["band"]); i_end0 = end_of("intro", i_play)
    check("the title bar appears as the intro line starts to sound", abs(ms(i_band) - ms(i_play)) <= 150 and not samples[0]["band"],
          f"bar at {ms(i_band) - ms(i_play):+.0f} ms from the clip's first played moment")
    check("nothing else shows while the intro line sounds", not any(s["boxes"] or s["shown"] or any(s["on"]) or any(s["off"]) for s in samples[:i_end0]))
    i_boxes = first(lambda s: s["boxes"])
    check("the picture, the bar and the tiles come in 0.5 s after the intro", 450 <= ms(i_boxes) - ms(i_end0) <= 800, f"{ms(i_boxes) - ms(i_end0):.0f} ms")
    i_s1 = start_of("sent"); i_e1 = end_of("sent", i_s1)
    check("the sentence's clip starts once they have landed (~0.65 s)", 600 <= ms(i_s1) - ms(i_boxes) <= 1000, f"{ms(i_s1) - ms(i_boxes):.0f} ms")
    check("no word shows before the sentence's clip", all(s["shown"] == 0 for s in samples[:i_s1]))
    timed = [s for s in samples[i_s1:i_e1] if s["clip"] == "sent" and s["playing"] and s["t"] is not None]
    early = [s for s in timed if s["shown"] > sum(1 for t in tS if s["t"] + 0.04 >= t)]
    late = [s for s in timed if s["shown"] < sum(1 for t in tS if s["t"] - 0.15 >= t)]
    distinct_times = len(set(tS))   # a punctuation-only word ("।") arrives with the word before it
    check("the words arrive one by one with the clip, none early, none >150 ms late",
          len(timed) > 20 and len({s["shown"] for s in timed}) >= distinct_times - 1 and not early and not late,
          f"{len(timed)} samples, {len({s['shown'] for s in timed})} distinct counts / {nW} words, early {len(early)}, late {len(late)}")
    check(f"{NS} slot(s) on the page", samples[i_e1]["nSlots"] == NS, samples[i_e1]["nSlots"])
    i_bl = first(lambda s: s["blinkN"] > 0); i_bl_end = first(lambda s: s["blinkN"] == 0, i_bl)
    check("the slot(s) blink from the moment the sentence's clip ends", 0 <= ms(i_bl) - ms(i_e1) <= 150, f"{ms(i_bl) - ms(i_e1):.0f} ms after")
    check("every slot blinks with the exact same animation, starting and stopping in the same frame",
          all(s["blinkN"] in (0, NS) for s in samples) and len({a for s in samples for a in s["blinkAnims"]}) == 1,
          f"blinking counts seen {sorted({s['blinkN'] for s in samples})}, animations {sorted({a for s in samples for a in s['blinkAnims']})}")
    check("the blink lasts 3.5 s, nothing sounding meanwhile", abs(ms(i_bl_end) - ms(i_bl) - (d.get("blink_ms") or 3500)) <= 150
          and not any(s["playing"] for s in samples[i_bl:i_bl_end]), f"{ms(i_bl_end) - ms(i_bl):.0f} ms")
    name, dur, count = samples[i_bl]["blinkAnims"][0].split("|")
    period = float(dur[:-2]) / 1000 if dur.endswith("ms") else float(dur[:-1])
    check("the blink is slow: three blinks of ~1.17 s", name == "dmfBlink" and count == "3" and abs(period * 3 - 3.5) < 0.05, samples[i_bl]["blinkAnims"][0])
    i_s2 = start_of(MK, i_bl); i_e2 = end_of(MK, i_s2)
    nm = d["options"][PICK]["name_hi"]
    check(f"the mark's name (\"{nm}\") sounds right after the blink", 0 <= ms(i_s2) - ms(i_bl_end) <= 200, f"{ms(i_s2) - ms(i_bl_end):.0f} ms after")
    check(f"the correct tile is the {nm} one ({d['mark']})", d["options"][PICK]["mark"] == d["mark"])
    i_on = first(lambda s: bool(s["on"]) and s["on"][PICK])
    on_faces = {s["face1"] for s in samples if s["on"] and s["on"][PICK]}
    check("the tapped tile keeps its colours: its face's border stays #D5D8DF, no blue ring", on_faces == {"rgb(213, 216, 223)|none"}, on_faces)
    check("its tile is tapped and the other two dim as that line starts, not before",
          abs(ms(i_on) - ms(i_s2)) <= 150 and samples[i_on]["off"] == [k != PICK for k in range(3)] and samples[i_on]["on"] == [k == PICK for k in range(3)]
          and not any(any(s["on"]) or any(s["off"]) for s in samples[:i_bl_end]),
          f"tap at {ms(i_on) - ms(i_s2):+.0f} ms; dim {samples[i_on]['off']}")
    lands = [first(lambda s, k=k: len(s["marksIn"]) > k and s["marksIn"][k]) for k in range(NS)]
    gaps = [ms(i) - ms(i_e2) for i in lands]
    check("the mark lands in " + ("the slot ~0.4 s" if NS == 1 else f"each slot, left to right, ~0.4 s + 0.3 s apart") + " after that line",
          all(350 + 300 * k <= g <= 700 + 300 * k for k, g in enumerate(gaps)) and not any(any(s["marksIn"]) for s in samples[:i_e2]), [round(g) for g in gaps])
    i_mark = lands[-1]
    i_s3 = start_of("full", i_mark); i_e3 = end_of("full", i_s3)
    check("the second reading starts ~0.7 s after the (last) mark, every tile dim", 650 <= ms(i_s3) - ms(i_mark) <= 1000 and all(samples[i_s3]["off"]) and not any(samples[i_s3]["on"]),
          f"{ms(i_s3) - ms(i_mark):.0f} ms; dim {samples[i_s3]['off']}")
    timed = [s for s in samples[i_s3:i_e3] if s["clip"] == "full" and s["playing"] and s["t"] is not None]
    def state_of(n):
        t = targets[n - 1] if n > 0 else ""
        return (int(t[1:]) if t[:1] == "w" else -1, int(t[1:]) if t[:1] == "s" else -1)
    off_time = [s for s in timed if (s["hot"], s["hotSlot"]) not in {state_of(n) for n in range(sum(1 for t in tF if s["t"] - 0.15 >= t), sum(1 for t in tF if s["t"] + 0.04 >= t) + 1)}]
    seen = {(s["hot"], s["hotSlot"]) for s in timed}
    want_seen = {state_of(n) for n in range(1, len(tF) + 1)}
    check("each word, and each slot, is highlighted as the second reading reaches it (within -150/+40 ms)",
          len(timed) > 20 and not off_time and want_seen <= seen, f"{len(timed)} samples, states seen {sorted(seen)}, off-time {len(off_time)}")
    i_gone = first(lambda s: s["gone"])
    check("1.5 s after the second reading the slots' boxes go", 1400 <= ms(i_gone) - ms(i_e3) <= 1800, f"{ms(i_gone) - ms(i_e3):.0f} ms")
    if CONFIG["gate"]:
        i_gate = first(lambda s: s["gate"], i_gone)
        check(f"the page moves on by itself: the engine's peek gate into the guided round opens ~0.6 s later, then {NEXT}",
              500 <= ms(i_gate) - ms(i_gone) <= 2000 and samples[-1]["slide"] == NEXT, f"gate {ms(i_gate) - ms(i_gone):.0f} ms after; {NEXT} at {ms(len(samples) - 1) - ms(i_gone):.0f} ms")
    else:
        check(f"the page advances to {NEXT} by itself ~0.6 s later", samples[-1]["slide"] == NEXT and 500 <= ms(len(samples) - 1) - ms(i_gone) <= 1000, f"{ms(len(samples) - 1) - ms(i_gone):.0f} ms")
    check("आगे never shows on this page", not any(s["navShown"] for s in mine))
    starts = lambda k: sum(1 for i, s in enumerate(samples) if s["clip"] == k and s["playing"] and (i == 0 or not (samples[i-1]["clip"] == k and samples[i-1]["playing"])))
    check("each clip plays once", all(starts(k) == 1 for k in ("intro", "sent", MK, "full")), [starts(k) for k in ("intro", "sent", MK, "full")])
    check(f"{NEXT} is {CONFIG['next_what']}", pg.evaluate(CONFIG["next_ok"]))
    pg.evaluate(GOTO, SLIDE); pg.wait_for_function("!!document.querySelector('.dmf-band.in')", timeout=10000); pg.wait_for_timeout(300)
    boxes = pg.evaluate(BOXES, list(AS_T0)); worst = 0
    gone = pg.evaluate("""[...document.querySelectorAll('.sfig-swiftie, .tut-audio')].map(e => { const r = e.getBoundingClientRect(); return getComputedStyle(e).display + ' ' + r.width + 'x' + r.height; })""")
    check("no standing Swiftie and no 🔊 chip on this page", len(gone) >= 2 and all(g == "none 0x0" for g in gone), gone)
    print("== the card is the stage (stage px) ==")
    for sel, exp in AS_T0.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, dd)
        print(f"  {sel:22s} got {[round(v,2) for v in got]}  want {list(exp)}  max|d|={dd:.2f}")
    check("the card is the whole stage (within 0.5 px)", worst <= 0.5, f"worst {worst:.2f}px")
    pg.close()

    # ---- 3. geometry + pixel diff at 1280x720, at the frame's moment (sentence shown, slots empty, tiles plain)
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(GOTO, SLIDE)
    pg.wait_for_function("!!document.querySelector('.dmf-blank.blink')", timeout=30000, polling=20)
    pg.evaluate("document.querySelectorAll('.dmf-blank').forEach(b => b.classList.remove('blink'))"); pg.wait_for_timeout(350)
    shot = out / "g_frame_1280.png"; pg.screenshot(path=str(shot))
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
      document.fonts.check("600 32px 'Story Noto Sans Devanagari'", 'सुनो'), document.fonts.check("600 SIZEpx 'Story Noto Sans Devanagari'", 'WORD')]"""
      .replace("WORD", CONFIG["word"]).replace("SIZE", str(SZ)))
    check(f"fonts: Noto Sans Devanagari SemiBold — 32px bar, {SZ}px sentence, 64px marks, 28px names", fonts == ["32px", f"{SZ}px", "64px", "28px", True, True], fonts)
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
    keep = np.zeros(near.shape, bool); x0, y0, x1, y1 = CONTENT; keep[y0:y1, x0:x1] = True
    for x0, y0, x1, y1 in OWN: keep[y0:y1, x0:x1] = False
    m = (near > 32) & keep; px = int(keep.sum())
    print(f"  pixel diff vs Figma render over the content (within 1 px): {int(m.sum())} of {px} px differ by >32 levels ({100*m.sum()/px:.2f}%)")
    check("the content pixel-matches the Figma render (within 1 px: >32-level diffs under 3% of the area)", m.sum() / px < 0.03)
    keep = np.ones(near.shape, bool)
    for x0, y0, x1, y1 in OWN: keep[y0:y1, x0:x1] = False
    m = (near > 32) & keep; px = int(keep.sum())
    solid = m.copy(); solid[1:-1, 1:-1] &= m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:]
    solid[0, :] = solid[-1, :] = False; solid[:, 0] = solid[:, -1] = False
    what = "less the slot's ring" if OWN else "slots' dashes included"
    print(f"  pixel diff vs Figma render over the whole frame, {what} (within 1 px): {int(m.sum())} of {px} px"
          f" ({100*m.sum()/px:.2f}%), of them solid: {int(solid.sum())} ({100*solid.sum()/px:.3f}%)")
    Image.fromarray(np.where(m, 255, np.where(keep, 0, 60)).astype(np.uint8)).save(out / "g_diff_mask.png")
    check("the whole frame pixel-matches the Figma render (solid diffs under 0.05% of the area)", solid.sum() / px < 0.0005)
    # the mark's INK on each slot's centre: once it has landed, and while that slot is highlighted (grown)
    slots = pg.evaluate("[...document.querySelectorAll('.dmf-blank')].map(e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; })")
    def mark_ink(k):
        x, y, w, h = slots[k]; cx, cy = x + w / 2, y + h / 2
        a = np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert("RGB"), np.int16)
        x0, y0, x1, y1 = int(x) + 3, int(y) + 3, int(x + w) - 3, int(y + h) - 3   # inside the slot's ring, clear of its neighbours
        a = a[y0:y1, x0:x1]
        mm = (a[..., 0] < 60) & (a[..., 2] < 170) & (a[..., 2] - a[..., 0] > 55)   # navy ink only, not the blue highlight
        ys, xs = np.nonzero(mm)
        return (x0 + xs.min() + x0 + xs.max() + 1) / 2 - cx, (y0 + ys.min() + y0 + ys.max() + 1) / 2 - cy, xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
    pg.wait_for_function(f"document.querySelectorAll('.dmf-mark.in').length === {NS}", timeout=30000, polling=20); pg.wait_for_timeout(550)
    landed = [mark_ink(k) for k in range(NS)]; pg.screenshot(path=str(out / "h_marks_in_1280.png"))
    lit = []
    for k in range(NS):
        pg.wait_for_function(f"document.querySelectorAll('.dmf-blank')[{k}].classList.contains('hot')", timeout=20000, polling=20); pg.wait_for_timeout(450)
        lit.append(mark_ink(k)); pg.screenshot(path=str(out / f"i_slot{k + 1}_hot_1280.png"))
    vars_ = pg.evaluate("[...document.querySelectorAll('.dmf-mark')].map(m => getComputedStyle(m).getPropertyValue('--ix') + ' ' + getComputedStyle(m).getPropertyValue('--iy'))")
    for k in range(NS):
        r1, r2 = landed[k], lit[k]
        print(f"  slot {k + 1}: mark ink centre vs slot centre: landed ({r1[0]:+.2f}, {r1[1]:+.2f}) ink {r1[2]}x{r1[3]}; highlighted ({r2[0]:+.2f}, {r2[1]:+.2f}) ink {r2[2]}x{r2[3]}; offset {vars_[k]}")
        check(f"slot {k + 1}: the mark's ({d['mark']}) ink sits on the slot's centre once it has landed (within 1 px)", abs(r1[0]) <= 1 and abs(r1[1]) <= 1, f"({r1[0]:+.2f}, {r1[1]:+.2f})")
        check(f"slot {k + 1}: ...and stays there while it is highlighted and grown (within 1 px)", abs(r2[0]) <= 1 and abs(r2[1]) <= 1 and r2[3] > r1[3], f"({r2[0]:+.2f}, {r2[1]:+.2f}), {r1[3]} -> {r2[3]} px tall")
    pg.close()
    b.close()
check("no page errors", not errs, errs[:3]); check("no failed requests", not bad, bad[:5])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
