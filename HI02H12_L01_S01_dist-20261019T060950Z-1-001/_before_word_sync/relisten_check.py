"""Verify T0B "आइए वाक्य सुनें।" (STORY_RELISTEN, [relisten-pinki]: frame 654:567) against its Figma frame and its timing.
usage: python -I -X utf8 relisten_check.py <index.html> <relisten2_figma_render_1280x720.png> <outdir>
1. At 1333x750, the page mounted on its own: the title appears as the intro line ("अब इन्हीं वाक्यों को फिर से सुनते हैं।",
   vo_story_r0) starts to sound; the sentence box comes in only when that line has ended; once the box has landed the two
   contrast sentences are read one after the other, each word by word with its own recorded clip (vo_story_c1 "उसे रोको,
   मत जाने दो।", vo_story_c2 "उसे रोको मत, जाने दो।"); then the explanation (vo_story_r1) lifts sentence 1 on its yellow from
   its "पहले" and sentence 2 from its "जबकि" (the cues read off the clip by vo_rec.py), both off again when it ends; then the
   moral (vo_story_moral, 4.wav) lights the two commas orange, lifted, from its "विराम" — they stay lit; आगे shows the
   reference's disabled pill ([dun-chrome]) through all of it and goes live, breathing, once the moral has ended; a 🔊 tap
   before the sentences is ignored, and afterwards replays the whole reading (sentences, explanation, moral); आगे leads to T1
   (the three-marks recap); past the Figma pages (G4) no story styling is left over.
2. The card is the frame's (96,106 1088x508 x 1333/1280 = 100,110.39 1133x529.03 on the stage, 64px corners); Swiftie, 🔊
   chip and आगे are the story page's (T0): Swiftie 76,472 190x190, chip 202,606 58x58, आगे 581.5,550 170x62.
3. 1280x720 viewport (stage px x 1333/1280 = frame px): title, sentence box and the two sentence nodes vs the frame, each
   sentence on one line, and per-pixel diffs vs the Figma render over the title + box and over the whole card (less Swiftie,
   the chip and आगे, which follow T0 rather than the frame) — taken with the commas' end-of-page highlight cleared, since
   the frame draws the sentences plain.
"""
import sys, json, pathlib
import numpy as np
from playwright.sync_api import sync_playwright
from PIL import Image

html = pathlib.Path(sys.argv[1]).resolve(); target = Image.open(sys.argv[2]).convert("RGB")
out = pathlib.Path(sys.argv[3]).resolve(); out.mkdir(parents=True, exist_ok=True)
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)

FS = 1333 / 1280
AS_T0 = {   # stage px: the frame's card box; the story page's (= the reference game's) Swiftie and chip, and T0's आगे
  ".tut-card.sfig-card": (96 * FS, 106 * FS, 1088 * FS, 508 * FS),
  ".sfig-swiftie":       (76, 472, 190, 190),
  ".tut-audio":          (202, 606, 58, 58),
  "#navBtn":             (581.5, 550, 170, 62),   # [dun-chrome] the reference's text pill (T0's आगे)
}
FRAME = {   # frame px at 1280x720, from the design context of node 654:567
  ".sfig-sbox":  (96+12+191-4, 106+12+144-4, 691, 227),   # node 654:748: 683x219 (centred on 532.5) + its 4px OUTSIDE stroke
}
NODES = {   # the sentence nodes: centre (x, y) in frame px and width
  ".sfig-stext p.l1": ((96+12+540.5, 106+12+204.5), 401),   # node 654:752 (its centre 8 px right of the box's, as the frame has it)
  ".sfig-stext p.l2": ((96+12+540, 106+12+302.5), 390),     # node 654:753
}
TITLE_CENTRE = (96+12+532, 106+12+65.5)                      # node 654:749
LINES = ["उसे रोको, मत जाने दो।", "उसे रोको मत, जाने दो।"]
CONTENT = (280, 128, 1000, 492)  # frame px region holding the title + the sentence box, for the pixel diff
WHOLE = (80, 90, 1200, 640)      # frame px: the card with its border and shadow
OWN_T0 = [(25, 400, 290, 720),   # ...less Swiftie (the frame's at 35,415 245x245 and T0's) + the 🔊 chip,
          (535, 490, 745, 600)]  # and आगे (not in the frame)
BOXES = """(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
  if (!e) { o[s] = null; continue; } const r = e.getBoundingClientRect(); o[s] = [r.left, r.top, r.width, r.height]; } return o; }"""
GOTO = """(id) => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); mountSlide(CARD.slides.findIndex(s => s.id === id)); }"""
NAVLOG = """() => { window._navLog = []; const btn = document.getElementById('navBtn'); let last = ''; const t0 = performance.now();
  const step = () => { const cs = getComputedStyle(btn);   // [dun-chrome] a bare text button: live = .active (the disabled art otherwise), its ::after breathes (navBreathe)
    const shown = cs.visibility === 'visible' && parseFloat(cs.opacity) > 0.01 && cs.display !== 'none';
    const img = !shown ? 'none' : btn.classList.contains('active') ? 'ON' : 'DISABLED';
    const slide = CARD.slides[state.idx] ? CARD.slides[state.idx].id : null, key = [img, slide, isPlaying].join('|');
    if (key !== last) { last = key; window._navLog.push({ ms: performance.now() - t0, img, slide, playing: isPlaying,
      clip: currentAudio ? currentAudio.src.split('/').pop() : null }); }
    requestAnimationFrame(step); };
  requestAnimationFrame(step); }"""
# one frame: the clip (r0 / c1 / c2 / r1 / moral), its clock, the title and box, each sentence's shown words, the lit sentence
# (-1 = none), the lit commas, आगे
SAMPLE = """() => { const a = currentAudio, src = a ? a.src.split('/').pop() : '', m = src.match(/vo_story_(\\w+)\\.ogg/), q = (s) => document.querySelector(s), nav = document.getElementById('navBtn');
  return { clip: m ? m[1] : null, t: a ? a.currentTime : null, playing: isPlaying, title: !!q('.sfig-title.in'), box: !!q('.sfig-sbox.in'),
    shown: [...document.querySelectorAll('.sfig-stext p')].map(p => p.querySelectorAll('.sfig-w.on').length),
    hl: [...document.querySelectorAll('.sfig-sent')].findIndex(s => s.classList.contains('hl')), mk: document.querySelectorAll('.sfig-mk.on').length,
    navVisible: nav.classList.contains('visible'), nav: nav.classList.contains('active'), ms: performance.now() }; }"""
# the timeline is sampled IN the page, every frame, so screenshots taken meanwhile cannot skew it; the two 🔊 taps
# (1 s into the intro line, and the moment the box comes in) are made in the page too, at those exact moments
TIMELINE = "(sample) => { window._tl = []; window._taps = []; const S = eval(sample); const step = () => { const s = S(); window._tl.push(s);" \
    " const chip = document.querySelector('.tut-audio');" \
    " if (chip && !window._taps.includes('intro') && s.clip === 'r0' && s.playing && s.t > 1) { window._taps.push('intro'); chip.click(); }" \
    " if (chip && !window._taps.includes('landing') && s.box && s.clip === 'r0') { window._taps.push('landing'); chip.click(); }" \
    " if (!s.nav) requestAnimationFrame(step); }; requestAnimationFrame(step); }"
PULSING = "getComputedStyle(document.getElementById('navBtn'), '::after').animationName"

def sync_checks(tag, samples, k, clip, times):
    timed = [s for s in samples if s["clip"] == clip and s["playing"] and s["t"] is not None]
    shown = lambda s: s["shown"][k]
    early = [s for s in timed if shown(s) > sum(1 for t in times if s["t"] + 0.04 >= t)]
    late = [s for s in timed if shown(s) < sum(1 for t in times if s["t"] - 0.15 >= t)]
    check(f"{tag}: words appear one by one with its clip ({clip})", len(timed) > 40 and len({shown(s) for s in timed}) >= len(set(times)) - 1,
          f"{len(timed)} samples, {len({shown(s) for s in timed})} distinct word counts, {len(times)} words")
    check(f"{tag}: no word shows before the narration reaches it", not early, early[:2])
    check(f"{tag}: no word lags its start time by >150 ms", not late, late[:2])

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs, bad = [], []

    # ---- 1-2. timing at 1333x750
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(NAVLOG); pg.evaluate(TIMELINE, SAMPLE); pg.evaluate(GOTO, "T0B")
    d = pg.evaluate("CARD.slides[state.idx].data"); T = [ln["word_times"] for ln in d["lines"]]; CUES = d["explain_cues"]; MCUE = d["moral_cue"]
    check("the page's data: the frame's two sentences on vo_story_c1 / c2, the explanation vo_story_r1 with its two cues, the moral vo_story_moral with its cue",
          [ln["text_hi"] for ln in d["lines"]] == LINES and [ln["audio"] for ln in d["lines"]] == ["vo_story_c1", "vo_story_c2"] and d["explain_audio"] == "vo_story_r1"
          and len(CUES) == 2 and 0 < CUES[0] < CUES[1] and d["moral_audio"] == "vo_story_moral" and MCUE > 0, (CUES, MCUE))
    pg.wait_for_function("!!document.querySelector('.sfig-title.in')", timeout=10000, polling=20); pg.wait_for_timeout(700)
    pg.screenshot(path=str(out / "a_title_in_1333.png"))
    pg.wait_for_function("!!document.querySelector('.sfig-sbox.in')", timeout=20000, polling=20); pg.wait_for_timeout(550)
    pg.screenshot(path=str(out / "b_box_in_1333.png"))
    pg.wait_for_function("document.querySelectorAll('.sfig-stext p.l2 .sfig-w.on').length >= 2", timeout=40000, polling=20)
    pg.screenshot(path=str(out / "c_mid_1333.png"))
    pg.wait_for_function("!!document.querySelector('.sfig-sent.hl')", timeout=30000, polling=20); pg.wait_for_timeout(500)
    pg.screenshot(path=str(out / "c2_sentence1_lit_1333.png"))
    pg.wait_for_function("document.querySelectorAll('.sfig-mk.on').length === 2", timeout=40000, polling=20); pg.wait_for_timeout(500)
    pg.screenshot(path=str(out / "c3_commas_lit_1333.png"))
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=60000, polling=20)
    pg.wait_for_timeout(300); pg.screenshot(path=str(out / "d_end_1333.png"))
    samples, taps = pg.evaluate("window._tl"), pg.evaluate("window._taps")
    tapped_intro, tapped_land = "intro" in taps, "landing" in taps
    with open(out / "timeline.json", "w", encoding="utf-8") as f: json.dump(samples, f, indent=0)
    ms = lambda i: samples[i]["ms"]
    first = lambda cond, start=0: next(i for i in range(start, len(samples)) if cond(samples[i]))
    start_of = lambda c, i0=0: first(lambda s: s["clip"] == c and s["playing"], i0)
    end_of = lambda c, i0: first(lambda s: s["clip"] != c or not s["playing"], i0 + 1)   # the next clip may follow at once
    i_play = first(lambda s: s["clip"] == "r0" and (s["t"] or 0) > 0)
    i_title = first(lambda s: s["title"]); i_end0 = end_of("r0", i_play); i_box = first(lambda s: s["box"])
    i_c1 = start_of("c1"); i_c1e = end_of("c1", i_c1); i_c2 = start_of("c2", i_c1e); i_c2e = end_of("c2", i_c2)
    i_r1 = start_of("r1", i_c2e); i_r1e = end_of("r1", i_r1); i_m = start_of("moral", i_r1e); i_me = end_of("moral", i_m)
    check("the title appears as the intro line starts to sound", abs(ms(i_title) - ms(i_play)) <= 150 and not samples[0]["title"],
          f"title at {ms(i_title) - ms(i_play):+.0f} ms from the clip's first played moment")
    check("the sentence box stays away while the intro line sounds", not any(s["box"] for s in samples[:i_end0]))
    check("the box comes in as the intro line ends", 0 <= ms(i_box) - ms(i_end0) <= 150, f"{ms(i_box) - ms(i_end0):.0f} ms after")
    check("sentence 1's clip starts once the box has landed (~0.65 s)", 600 <= ms(i_c1) - ms(i_box) <= 1000, f"{ms(i_c1) - ms(i_box):.0f} ms")
    starts = lambda clip: sum(1 for i, s in enumerate(samples) if s["clip"] == clip and s["playing"]
                              and (i == 0 or not (samples[i - 1]["clip"] == clip and samples[i - 1]["playing"])))
    check("🔊 taps during the intro / the box landing were ignored (each clip plays once: intro, the two sentences, the explanation, the moral)",
          tapped_intro and tapped_land and all(starts(c) == 1 for c in ("r0", "c1", "c2", "r1", "moral")), f"taps made: {taps}, starts {[starts(c) for c in ('r0', 'c1', 'c2', 'r1', 'moral')]}")
    check("no sentence word shows before sentence 1's clip", all(s["shown"] == [0, 0] for s in samples[:i_c1]))
    sync_checks("sentence 1", samples, 0, "c1", T[0]); sync_checks("sentence 2", samples, 1, "c2", T[1])
    check("sentence 2's clip starts ~0.6 s after sentence 1's has ended, sentence 1 complete and standing, no sentence-2 word before it",
          500 <= ms(i_c2) - ms(i_c1e) <= 950 and all(s["shown"][1] == 0 for s in samples[:i_c2]) and samples[i_c2]["shown"][0] == len(T[0]), f"{ms(i_c2) - ms(i_c1e):.0f} ms after")
    check("the explanation (vo_story_r1) starts ~0.5 s after sentence 2's clip, both sentences complete, nothing lit yet",
          400 <= ms(i_r1) - ms(i_c2e) <= 900 and samples[i_r1]["shown"] == [len(T[0]), len(T[1])] and not any(s["hl"] >= 0 or s["mk"] for s in samples[:i_r1]), f"{ms(i_r1) - ms(i_c2e):.0f} ms after")
    r1 = [s for s in samples[i_r1:i_r1e] if s["clip"] == "r1" and s["t"] is not None]
    i_h1 = first(lambda s: s["hl"] == 0, i_r1); i_h2 = first(lambda s: s["hl"] == 1, i_h1)
    check(f"sentence 1 is lifted on its yellow as the explanation reaches \"पहले\" ({CUES[0]} s on the clip's clock, within -0.05/+0.15 s), sentence 2 as it reaches \"जबकि\" ({CUES[1]} s), sentence 1 off then",
          i_h1 < i_h2 < i_r1e and -0.05 <= samples[i_h1]["t"] - CUES[0] <= 0.15 and -0.05 <= samples[i_h2]["t"] - CUES[1] <= 0.15
          and all(s["hl"] == 0 for s in samples[i_h1 + 1:i_h2]) and all(s["hl"] == 1 for s in samples[i_h2:i_r1e] if s["clip"] == "r1" and s["playing"]) and not any(s["mk"] for s in samples[:i_r1e]),
          (round(samples[i_h1]["t"] - CUES[0], 2), round(samples[i_h2]["t"] - CUES[1], 2)))
    i_hoff = first(lambda s: s["hl"] == -1, i_h2)
    check("both sentences are plain again within 0.5 s of the explanation's end, and the moral (vo_story_moral) follows ~0.9 s after it",
          0 <= ms(i_hoff) - ms(i_r1e) <= 550 and 750 <= ms(i_m) - ms(i_r1e) <= 1300 and samples[i_m]["hl"] == -1, (round(ms(i_hoff) - ms(i_r1e)), round(ms(i_m) - ms(i_r1e))))
    i_mk = first(lambda s: s["mk"] == 2, i_m)
    check(f"the two commas light orange, lifted, as the moral reaches \"विराम\" ({MCUE} s on its clock, within -0.05/+0.15 s), none before, both staying lit to the end",
          i_m < i_mk < i_me and -0.05 <= samples[i_mk]["t"] - MCUE <= 0.15 and not any(s["mk"] for s in samples[:i_mk]) and all(s["mk"] == 2 for s in samples[i_mk:]), round(samples[i_mk]["t"] - MCUE, 2) if i_mk > i_m else None)
    check("आगे stays away (not live) until the moral has ended", not any(s["nav"] for s in samples[:i_me]))
    check("आगे opens (live, breathing) ~0.3 s after the moral ends", samples[-1]["nav"] and 200 <= ms(len(samples) - 1) - ms(i_me) <= 700 and pg.evaluate(PULSING) == "navBreathe",
          f"{ms(len(samples) - 1) - ms(i_me):.0f} ms after the clip ended")
    pg.evaluate("document.getElementById('navBtn').style.animation = 'none'")   # measure आगे at rest, not mid-pulse
    boxes = pg.evaluate(BOXES, list(AS_T0)); worst = 0
    pg.evaluate("document.getElementById('navBtn').style.animation = ''")
    print("== card vs the frame; Swiftie / chip / आगे vs the story page (stage px) ==")
    for sel, exp in AS_T0.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, dd)
        print(f"  {sel:22s} got {[round(v,2) for v in got]}  want {[round(v,2) for v in exp]}  max|d|={dd:.2f}")
    check("card box is the frame's; Swiftie, 🔊 chip and आगे are exactly the story page's (within 0.5 px)", worst <= 0.5, f"worst {worst:.2f}px")
    radius = pg.evaluate("getComputedStyle(document.querySelector('.tut-card.sfig-card')).borderTopLeftRadius")
    check("the card has the frame's 64px corners (x 1333/1280)", abs(float(radius[:-2]) - 64 * 1333 / 1280) < 0.05, radius)
    pg.wait_for_timeout(1200)
    pg.click(".tut-audio", force=True); pg.wait_for_timeout(400)
    r = pg.evaluate(SAMPLE)
    check("🔊 afterwards replays the reading from sentence 1's first word (title and box staying, the highlights cleared)",
          r["clip"] == "c1" and r["playing"] and r["shown"][0] < len(T[0]) and r["shown"][1] == 0 and r["hl"] == -1 and r["mk"] == 0 and r["title"] and r["box"], r)
    check("आगे is hidden while the replay sounds", not r["navVisible"])
    pg.wait_for_function("document.querySelectorAll('.sfig-mk.on').length === 2", timeout=40000, polling=20)
    pg.wait_for_function("!isPlaying && document.getElementById('navBtn').classList.contains('active')", timeout=30000)
    pg.wait_for_timeout(300)
    check("...the replay runs the whole reading again (the commas lit once more) and आगे comes back live, breathing", pg.evaluate(PULSING) == "navBreathe")
    log = [e for e in pg.evaluate("window._navLog") if e["slide"] == "T0B"]
    first_on = next((e for e in log if e["img"] == "ON"), None)   # [dun-chrome] the reference's pill: disabled art through the clips, live once the last has ended
    check("आगे shows the reference's disabled pill from the start, through every clip (frame by frame, incl. the replay), and goes live only once the moral has ended",
          log and log[0]["img"] == "DISABLED" and first_on is not None and first_on["clip"] == "vo_story_moral.ogg" and not first_on["playing"],
          [(round(e["ms"]), e["img"], e["clip"], e["playing"]) for e in log])
    check("आगे is never live while a VO plays", not any(e["img"] == "ON" and e["playing"] for e in log))
    pg.click("#navBtn", force=True)   # force: the active pill pulses forever, so it is never "stable"
    pg.wait_for_function("CARD.slides[state.idx].id === 'T1' && !!document.querySelector('.tut-card.sfig-recap .rcf-row')", timeout=10000)
    check("आगे leads to T1 (the three-marks recap, see recap_check.py), no extra gate", not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"))
    pg.wait_for_timeout(1500); pg.screenshot(path=str(out / "e_T1_after.png"))
    pg.evaluate(GOTO, "G4"); pg.wait_for_timeout(600)
    STAGE = "[!!document.querySelector('.sfig-card'), document.getElementById('stage').className, getComputedStyle(document.getElementById('stage')).backgroundColor]"
    seen = pg.evaluate(STAGE)
    fresh = b.new_page(viewport={"width": 1333, "height": 750}); fresh.goto(html.as_uri()); fresh.wait_for_timeout(1500)
    fresh.evaluate(GOTO, "G4"); fresh.wait_for_timeout(600); clean = fresh.evaluate(STAGE); fresh.close()
    # G4 (the first page past the Figma ones, G1-G3 being ones since 2026-10-25) keeps its own theme (thm-toybox, a pale blue stage): it must look exactly as it does when mounted on its own
    check("no story styling is left past the Figma pages (G4 as when mounted on its own)", not seen[0] and seen == clean, (seen, clean))
    pg.close()

    # ---- 3. geometry + pixel diff at 1280x720
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(GOTO, "T0B")
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=90000)
    pg.evaluate("document.querySelectorAll('.sfig-mk.on').forEach(m => m.classList.remove('on'))")   # the frame draws the sentences plain
    pg.wait_for_timeout(700)
    shot = out / "f_end_1280.png"; pg.screenshot(path=str(shot))
    boxes = pg.evaluate(BOXES, list(FRAME) + list(NODES) + [".sfig-title p"]); worst = 0
    print("== title / box / sentences vs the frame (px) ==")
    for sel, exp in FRAME.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, dd)
        print(f"  {sel:18s} got {[round(v,2) for v in got]}  frame {list(exp)}  max|d|={dd:.2f}")
    for sel, ((cx, cy), w) in NODES.items():
        g = boxes[sel]; gc = (g[0] + g[2] / 2, g[1] + g[3] / 2); dd = max(abs(gc[0] - cx), abs(gc[1] - cy), abs(g[2] - w)); worst = max(worst, dd)
        print(f"  {sel:18s} centre {[round(v,2) for v in gc]} width {round(g[2],2)}  frame ({cx}, {cy}) {w}  max|d|={dd:.2f}")
    tb = boxes[".sfig-title p"]; tc = (tb[0] + tb[2] / 2, tb[1] + tb[3] / 2)
    dt = max(abs(tc[0] - TITLE_CENTRE[0]), abs(tc[1] - TITLE_CENTRE[1])); worst = max(worst, dt)
    print(f"  title centre       got {[round(v,2) for v in tc]}  frame {list(TITLE_CENTRE)}  max|d|={dt:.2f}")
    check("title, sentence box and the two sentence nodes within 1 px of the frame", worst <= 1.0, f"worst {worst:.2f}px")
    lines = pg.evaluate("""() => [...document.querySelectorAll('.sfig-stext p')].map(p => { const ws = [...p.querySelectorAll('.sfig-w')];
      const tops = [...new Set(ws.map(w => Math.round(w.getBoundingClientRect().top)))];
      return tops.map(t => ws.filter(w => Math.round(w.getBoundingClientRect().top) === t).map(w => w.textContent).join(' ')); })""")
    print("  text lines:", lines)
    check("each sentence is the frame's, on one line", lines == [[l] for l in LINES])
    fonts = pg.evaluate("[getComputedStyle(document.querySelector('.sfig-title')).fontSize, getComputedStyle(document.querySelector('.sfig-stext p.l1')).fontSize, document.fonts.check(\"800 64px 'Story Baloo 2'\", 'आइए')]")
    check("fonts: Baloo 2 ExtraBold ([baloo-font]), 64px title / 30px sentences (frame px)", fonts[0] == "64px" and fonts[1] == "30px" and fonts[2], fonts)
    A = np.asarray(Image.open(shot).convert("RGB"), np.int16); B = np.asarray(target, np.int16)
    x0, y0, x1, y1 = CONTENT
    pad = np.pad(B, ((1, 1), (1, 1), (0, 0)), mode="edge")
    near = np.min([np.abs(A - pad[1+dy:1+dy+A.shape[0], 1+dx:1+dx+A.shape[1]]).max(axis=2)
                   for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)[y0:y1, x0:x1]
    big = int((near > 32).sum()); px = near.size
    print(f"  pixel diff vs Figma render over the title + box (within 1 px): {big} of {px} px differ by >32 levels ({100*big/px:.2f}%)")
    Image.fromarray(np.where(near > 32, 255, 0).astype(np.uint8)).save(out / "f_diff_mask.png")
    # anti-aliasing of glyph strokes and the box edge is what remains; a misplaced line or box shows as whole shapes
    check("title + box pixel-match the Figma render (within 1 px: >32-level diffs under 5% of the area)", big / px < 0.05)
    full = np.min([np.abs(A - pad[1+dy:1+dy+A.shape[0], 1+dx:1+dx+A.shape[1]]).max(axis=2)
                   for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
    keep = np.zeros(full.shape, bool); x0, y0, x1, y1 = WHOLE; keep[y0:y1, x0:x1] = True
    for x0, y0, x1, y1 in OWN_T0: keep[y0:y1, x0:x1] = False
    m = (full > 32) & keep; px = int(keep.sum())
    # what is left within 1 px is anti-aliasing: glyph outlines and a 1-px line along each edge of the card's border
    solid = int(((full > 32) & keep & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)).sum())
    print(f"  pixel diff vs Figma render over the whole card, less Swiftie/chip/आगे (within 1 px): {int(m.sum())} of {px} px ({100*m.sum()/px:.2f}%), of them solid: {solid} ({100*solid/px:.3f}%)")
    Image.fromarray(np.where(m, 255, 0).astype(np.uint8)).save(out / "f_diff_mask_card.png")
    check("the whole card (edges, corners, grid) pixel-matches the Figma render (solid diffs under 0.05% of the area)", solid / px < 0.0005)
    pg.close()
    b.close()
check("no page errors", not errs, errs[:3]); check("no failed requests", not bad, bad[:5])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
