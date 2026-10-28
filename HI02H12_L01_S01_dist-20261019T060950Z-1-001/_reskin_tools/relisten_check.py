"""Verify T0B "आइए वाक्य सुनें।" (STORY_RELISTEN) against its Figma frame and its timing.
usage: python -I -X utf8 relisten_check.py <index.html> <relisten_figma_render_1280x720.png> <outdir>
1. At 1333x750, the page mounted on its own: the title appears as the intro line ("अब इन्हीं वाक्यों को फिर से
   सुनते हैं।") starts to sound; the sentence box comes in only when that line has ended; the sentences' VO starts
   once the box has landed and reveals the words one by one with the clip; आगे shows the reference's disabled pill
   ([dun-chrome]) until that VO has ended, then goes live, breathing, where it is on T0; a 🔊 tap before the sentences is ignored,
   and afterwards replays the sentences; आगे leads to T1 (the three-marks recap); past the Figma pages (G4) no story
   styling is left over.
2. The card is the frame's (96,106 1088x508 x 1333/1280 = 100,110.39 1133x529.03 on the stage, 64px corners);
   Swiftie, 🔊 chip and आगे are the story page's (T0): Swiftie 76,472 190x190, chip 202,606 58x58,
   आगे 567.5,522 198x90.
3. 1280x720 viewport (stage px x 1333/1280 = frame px): title, sentence box and text block vs the frame, the
   sentences' line breaks, and per-pixel diffs vs the Figma render over the title + box and over the whole card
   (less Swiftie, the chip and आगे, which follow T0 rather than the frame).
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
FRAME = {   # frame px at 1280x720, from the Figma metadata / design context of node 488:190 (2026-10-21 evening, 5th version)
  ".sfig-sbox":  (96+12+191-4, 106+12+144-4, 691, 227),   # 683x219 box (centred on 532.5) + its 4px OUTSIDE stroke
  ".sfig-stext": (96+12+217, 106+12+89, 631, 280),          # node 488:374 (bottom-aligned on y 369)
}
TITLE_CENTRE = (96+12+532, 106+12+65.5)                      # node 488:376 (6th version of the frame)
LINES = ["चिंटू दौड़कर आया और बोला, “दादी! बिल्ली दूध पी रही है ।”", "दादी बोली, “उसे भगाओ, मत पीने दो।”",
         "चिंटू हैरान होकर बोला, “क्या? उसे सारा दूध पीने दूँ?” दादी", "हँसकर बोली, “अरे नहीं! उसे भगाओ। दूध मत पीने दो।”"]
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
SAMPLE = """() => { const a = currentAudio, src = a ? a.src : '', q = (s) => document.querySelector(s), nav = document.getElementById('navBtn');
  return { clip: src.includes('vo_story_r0') ? 'r0' : src.includes('vo_story_r1') ? 'r1' : null, t: a ? a.currentTime : null,
    playing: isPlaying, title: !!q('.sfig-title.in'), box: !!q('.sfig-sbox.in'),
    shown: document.querySelectorAll('.sfig-stext .sfig-w.on').length, navVisible: nav.classList.contains('visible'),
    nav: nav.classList.contains('active'), ms: performance.now() }; }"""
# the timeline is sampled IN the page, every frame, so screenshots taken meanwhile cannot skew it; the two 🔊 taps
# (1 s into the intro line, and the moment the box comes in) are made in the page too, at those exact moments
TIMELINE = "(sample) => { window._tl = []; window._taps = []; const S = eval(sample); const step = () => { const s = S(); window._tl.push(s);" \
    " const chip = document.querySelector('.tut-audio');" \
    " if (chip && !window._taps.includes('intro') && s.clip === 'r0' && s.playing && s.t > 1) { window._taps.push('intro'); chip.click(); }" \
    " if (chip && !window._taps.includes('landing') && s.box && s.clip === 'r0') { window._taps.push('landing'); chip.click(); }" \
    " if (!s.nav) requestAnimationFrame(step); }; requestAnimationFrame(step); }"

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs, bad = [], []

    # ---- 1-2. timing at 1333x750
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(NAVLOG); pg.evaluate(TIMELINE, SAMPLE); pg.evaluate(GOTO, "T0B")
    times = pg.evaluate("CARD.slides[state.idx].data.word_times")
    pg.wait_for_function("!!document.querySelector('.sfig-title.in')", timeout=10000, polling=20); pg.wait_for_timeout(700)
    pg.screenshot(path=str(out / "a_title_in_1333.png"))
    pg.wait_for_function("!!document.querySelector('.sfig-sbox.in')", timeout=20000, polling=20); pg.wait_for_timeout(550)
    pg.screenshot(path=str(out / "b_box_in_1333.png"))
    pg.wait_for_function("document.querySelectorAll('.sfig-stext .sfig-w.on').length >= 18", timeout=40000, polling=20)
    pg.screenshot(path=str(out / "c_mid_1333.png"))
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=60000, polling=20)
    pg.wait_for_timeout(300); pg.screenshot(path=str(out / "d_end_1333.png"))
    samples, taps = pg.evaluate("window._tl"), pg.evaluate("window._taps")
    tapped_intro, tapped_land = "intro" in taps, "landing" in taps
    with open(out / "timeline.json", "w", encoding="utf-8") as f: json.dump(samples, f, indent=0)

    i_play = next(i for i, s in enumerate(samples) if s["clip"] == "r0" and (s["t"] or 0) > 0)
    i_title = next(i for i, s in enumerate(samples) if s["title"])
    i_end0 = next(i for i, s in enumerate(samples) if s["clip"] == "r0" and not s["playing"] and i > i_play)
    i_box = next(i for i, s in enumerate(samples) if s["box"])
    i_vo1 = next(i for i, s in enumerate(samples) if s["clip"] == "r1" and s["playing"])
    i_end1 = next(i for i, s in enumerate(samples) if s["clip"] == "r1" and not s["playing"] and i > i_vo1)
    ms = lambda i: samples[i]["ms"]
    check("the title appears as the intro line starts to sound", abs(ms(i_title) - ms(i_play)) <= 150 and not samples[0]["title"],
          f"title at {ms(i_title) - ms(i_play):+.0f} ms from the clip's first played moment")
    check("the sentence box stays away while the intro line sounds", not any(s["box"] for s in samples[:i_end0]))
    check("the box comes in as the intro line ends", 0 <= ms(i_box) - ms(i_end0) <= 150, f"{ms(i_box) - ms(i_end0):.0f} ms after")
    check("the sentences' VO starts once the box has landed (~0.65 s)", 600 <= ms(i_vo1) - ms(i_box) <= 1000, f"{ms(i_vo1) - ms(i_box):.0f} ms")
    starts = lambda clip: sum(1 for i, s in enumerate(samples) if s["clip"] == clip and s["playing"]
                              and (i == 0 or not (samples[i - 1]["clip"] == clip and samples[i - 1]["playing"])))
    check("🔊 taps during the intro / the box landing were ignored (each clip plays once)", tapped_intro and tapped_land
          and starts("r0") == 1 and starts("r1") == 1, f"taps made: {taps}, intro starts {starts('r0')}, sentence starts {starts('r1')}")
    check("no sentence word shows before the sentences' VO", all(s["shown"] == 0 for s in samples[:i_vo1]))
    timed = [s for s in samples if s["clip"] == "r1" and s["playing"] and s["t"] is not None]
    early = [s for s in timed if s["shown"] > sum(1 for t in times if s["t"] + 0.04 >= t)]
    late = [s for s in timed if s["shown"] < sum(1 for t in times if s["t"] - 0.15 >= t)]
    check("sentences: words appear one by one with the clip", len(timed) > 200 and len({s["shown"] for s in timed}) >= len(times) - 2,
          f"{len(timed)} samples, {len({s['shown'] for s in timed})} distinct word counts, {len(times)} words")
    check("sentences: no word shows before the narration reaches it", not early, early[:2])
    check("sentences: no word lags its start time by >150 ms", not late, late[:2])
    check("आगे stays hidden until the sentences' VO has ended", not any(s["navVisible"] for s in samples[:i_end1]))
    check("आगे opens (pulsing) once the sentences' VO has ended", samples[-1]["nav"] and samples[-1]["shown"] == len(times)
          and pg.evaluate("getComputedStyle(document.getElementById('navBtn'), '::after').animationName") == "navBreathe",
          f"{ms(len(samples) - 1) - ms(i_end1):.0f} ms after the clip ended")
    pg.evaluate("document.getElementById('navBtn').style.animation = 'none'")   # measure आगे at rest, not mid-pulse
    boxes = pg.evaluate(BOXES, list(AS_T0)); worst = 0
    pg.evaluate("document.getElementById('navBtn').style.animation = ''")
    print("== card vs the frame; Swiftie / chip / आगे vs the story page (stage px) ==")
    for sel, exp in AS_T0.items():
        got = boxes[sel]; d = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, d)
        print(f"  {sel:22s} got {[round(v,2) for v in got]}  want {[round(v,2) for v in exp]}  max|d|={d:.2f}")
    check("card box is the frame's; Swiftie, 🔊 chip and आगे are exactly the story page's (within 0.5 px)", worst <= 0.5, f"worst {worst:.2f}px")
    radius = pg.evaluate("getComputedStyle(document.querySelector('.tut-card.sfig-card')).borderTopLeftRadius")
    check("the card has the frame's 64px corners (x 1333/1280)", abs(float(radius[:-2]) - 64 * 1333 / 1280) < 0.05, radius)
    pg.wait_for_timeout(1200)
    pg.click(".tut-audio", force=True); pg.wait_for_timeout(400)
    r = pg.evaluate(SAMPLE)
    check("🔊 afterwards replays the sentences from the first word, title and box staying",
          r["clip"] == "r1" and r["playing"] and r["shown"] < len(times) and r["title"] and r["box"])
    check("आगे is hidden while the replay sounds", not r["navVisible"])
    pg.wait_for_function("!isPlaying", timeout=40000)
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=2000)
    pg.wait_for_timeout(300)
    log = [e for e in pg.evaluate("window._navLog") if e["slide"] == "T0B"]
    first_on = next((e for e in log if e["img"] == "ON"), None)   # [dun-chrome] the reference's pill: disabled art through the clips, live once the last has ended
    check("आगे shows the reference's disabled pill from the start, through every clip (frame by frame, incl. the replay), and goes live only once the sentences' clip has ended",
          log and log[0]["img"] == "DISABLED" and first_on is not None and first_on["clip"] == "vo_story_r1.ogg" and not first_on["playing"],
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
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=60000)
    pg.wait_for_timeout(500)
    shot = out / "f_end_1280.png"; pg.screenshot(path=str(shot))
    boxes = pg.evaluate(BOXES, list(FRAME) + [".sfig-title p"]); worst = 0
    print("== title / box / text vs the frame (px) ==")
    for sel, exp in FRAME.items():
        got = boxes[sel]; d = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, d)
        print(f"  {sel:14s} got {[round(v,2) for v in got]}  frame {list(exp)}  max|d|={d:.2f}")
    tb = boxes[".sfig-title p"]; tc = (tb[0] + tb[2] / 2, tb[1] + tb[3] / 2)
    dt = max(abs(tc[0] - TITLE_CENTRE[0]), abs(tc[1] - TITLE_CENTRE[1])); worst = max(worst, dt)
    print(f"  title centre   got {[round(v,2) for v in tc]}  frame {list(TITLE_CENTRE)}  max|d|={dt:.2f}")
    check("title, sentence box and text block within 1 px of the frame", worst <= 1.0, f"worst {worst:.2f}px")
    lines = pg.evaluate("""() => { const ws = [...document.querySelectorAll('.sfig-stext .sfig-w')];
      const tops = [...new Set(ws.map(w => Math.round(w.getBoundingClientRect().top)))];
      return tops.map(t => ws.filter(w => Math.round(w.getBoundingClientRect().top) === t).map(w => w.textContent).join(' ')); }""")
    print("  text lines:", lines)
    check("the sentences break into the frame's 4 lines", lines == LINES)
    fonts = pg.evaluate("[getComputedStyle(document.querySelector('.sfig-title')).fontSize, getComputedStyle(document.querySelector('.sfig-stext')).fontSize, document.fonts.check(\"600 64px 'Story Noto Sans Devanagari'\", 'आइए')]")
    check("fonts: Noto Sans Devanagari SemiBold, 64px title / 28px sentences (frame px)", fonts[0] == "64px" and fonts[1] == "28px" and fonts[2], fonts)
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
    # (Figma blends its 12.5px border's edge, Chrome draws 12px). A misplaced edge, corner or grid line shows as a
    # SOLID band instead — a differing pixel whose 4 neighbours differ too (the T0-sized card here gave 9.3%).
    solid = m.copy(); solid[1:-1, 1:-1] &= m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:]
    solid[0, :] = solid[-1, :] = False; solid[:, 0] = solid[:, -1] = False
    print(f"  pixel diff vs Figma render over the whole card, less Swiftie/chip/आगे (within 1 px): {int(m.sum())} of {px} px"
          f" ({100*m.sum()/px:.2f}%), of them solid: {int(solid.sum())} ({100*solid.sum()/px:.3f}%)")
    Image.fromarray(np.where(m, 255, np.where(keep, 0, 60)).astype(np.uint8)).save(out / "f_diff_mask_card.png")
    check("the whole card (edges, corners, grid) pixel-matches the Figma render (solid diffs under 0.05% of the area)",
          solid.sum() / px < 0.0005)
    pg.close()
    b.close()
check("no page errors", not errs, errs[:3]); check("no failed requests", not bad, bad[:5])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
