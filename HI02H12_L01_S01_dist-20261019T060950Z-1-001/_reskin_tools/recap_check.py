"""Verify T1 "ये हैं तीन विराम चिह्न" (MARKS_RECAP) against its Figma frame (FLN-by-MJ node 508:2) and its timing.
usage: python -I -X utf8 recap_check.py <index.html> <recap_figma_render_1280x720.png> <outdir>
1. At 1333x750, the page mounted on its own: the title appears as the intro line ("आइए समझते हैं कि कौन-से चिह्न का
   प्रयोग कब किया जाता है।") starts to sound and nothing of the rows shows before that line has ended; then the nine beats
   — for each mark the box + mark with its name, the use, the yellow box with the example — each box pops in as its
   own clip starts and the words arrive one by one with the clip (none early, none >150 ms late); a 🔊 tap during the
   intro or between beats is ignored (every clip plays once); आगे shows the reference's disabled pill ([dun-chrome]) until
   the last example has been read, then goes live, breathing, under the card; a 🔊 tap afterwards reads the marks again from the
   first (boxes staying, words re-arriving) with आगे hidden meanwhile; आगे leads to T2 (no gate); past the Figma pages
   (G4) no story styling is left.
2. Card, Swiftie and 🔊 chip exactly as on T0B / T0 (stage px); आगे centred in the gap under the card.
3. 1280x720 viewport (stage px x 1333/1280 = frame px): every element's box vs the frame, the fonts, each text's ink
   vs the Figma render (centre and size), and per-pixel diffs vs the render over the content and the whole card.
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
AS_T0B = {   # stage px: the frame's card box; the story page's Swiftie and chip; आगे under the card
  ".tut-card.sfig-card": (96 * FS, 106 * FS, 1088 * FS, 508 * FS),
  ".sfig-swiftie":       (76, 472, 190, 190),
  ".tut-audio":          (202, 606, 58, 58),
  "#navBtn":             (581.5, 678, 170, 62),   # [dun-chrome] the reference's text pill, under the card
}
KEYS = [f"{m}_{p}" for m in ("purn", "alp", "prashn") for p in ("name", "when", "eg")]
GAP, GAP_MARK = 300, 700
CX, CY = 96, 106   # the frame's card origin (page px at 1280x720)
FRAME = {   # frame px, from the Figma metadata of node 508:2 (box = left, top, width, height)
  ".r1 .rcf-sign": (CX+166-4, CY+127-4, 101, 98), ".r2 .rcf-sign": (CX+166-4, CY+256-4, 101, 98), ".r3 .rcf-sign": (CX+166-4, CY+385-4, 101, 98),
  ".r1 .rcf-eg":   (CX+790, CY+143, 163, 49),      ".r2 .rcf-eg":   (CX+790, CY+274, 262, 49),      ".r3 .rcf-eg":   (CX+790, CY+405, 191, 49),
}
CENTRES = {   # frame px: text boxes given by their centre (x) and top (y) — or centre (y) where the frame centres them
  ".sfig-title p":    ("c", CX+544.5, "c", CY+64.5),
  ".r1 .rcf-mark p":  ("c", CX+209.5, "c", CY+174.5), ".r2 .rcf-mark p": ("c", CX+212.5, "c", CY+304.5), ".r3 .rcf-mark p": ("c", CX+212.5, "c", CY+438.5),
  ".r1 .rcf-name":    ("c", CX+372.5, "t", CY+148), ".r2 .rcf-name": ("c", CX+372.5, "t", CY+275), ".r3 .rcf-name": ("c", CX+380.5, "t", CY+414),
  ".r1 .rcf-when":    ("c", CX+633.5, "t", CY+148), ".r2 .rcf-when": ("c", CX+633.5, "t", CY+278), ".r3 .rcf-when": ("c", CX+633.5, "t", CY+414),
  ".r1 .rcf-eg p":    ("c", CX+790+81.5, "t", CY+143+7), ".r2 .rcf-eg p": ("c", CX+790+131, "t", CY+274+8), ".r3 .rcf-eg p": ("c", CX+790+95.5, "t", CY+405+9),
}
# ink regions (page px) for the text-vs-render comparison: navy glyph pixels inside each region
INK = {
  "title":   (380, 118, 900, 222),
  "mark 1":  (262, 234, 354, 322), "mark 2": (262, 363, 354, 451), "mark 3": (262, 492, 354, 580),
  "name 1":  (380, 246, 560, 310), "name 2": (380, 373, 560, 437), "name 3": (366, 512, 590, 576),
  "when 1":  (620, 246, 840, 310), "when 2": (585, 376, 875, 440), "when 3": (620, 512, 840, 576),
  "eg 1":    (888, 251, 1047, 296), "eg 2": (888, 382, 1146, 427), "eg 3": (888, 513, 1075, 558),
}
WHOLE = (80, 90, 1200, 640)      # frame px: the card with its border and shadow
OWN = [(25, 400, 292, 720),      # ...less Swiftie (the frame's at 35,415 245x245; T0's at 76,472 190x190 on the stage) + the chip,
       (535, 620, 745, 720)]     # and आगे (not in the frame)
CONTENT = (292, 118, 1180, 600)  # the rows and title (the sign boxes' first 34 px fall in Swiftie's strip above)
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
SAMPLE = r"""() => { const a = currentAudio, src = a ? a.src.split('/').pop() : '', nav = document.getElementById('navBtn');
  const m = src.match(/vo_recap_(\w+)\.ogg/), rows = [...document.querySelectorAll('.rcf-row')];
  return { clip: m ? m[1] : null, t: a ? a.currentTime : null, playing: isPlaying,
    title: !!document.querySelector('.sfig-title.in'),
    pops: rows.flatMap(r => [r.querySelector('.rcf-sign').classList.contains('in'), r.querySelector('.rcf-eg').classList.contains('in')]),
    shown: rows.flatMap(r => ['.rcf-name', '.rcf-when', '.rcf-eg'].map(s => r.querySelectorAll(s + ' .sfig-w.on').length)),
    navVisible: nav.classList.contains('visible'), nav: nav.classList.contains('active'), ms: performance.now() }; }"""
# the timeline is sampled IN the page, every frame; the two 🔊 taps (1 s into the intro, and in the breath after the
# first name has been read) are made in the page too, at those exact moments
TIMELINE = "(sample) => { window._tl = []; window._taps = []; const S = eval(sample); const step = () => { const s = S(); window._tl.push(s);" \
    " const chip = document.querySelector('.tut-audio');" \
    " if (chip && !window._taps.includes('intro') && s.clip === 'intro' && s.playing && s.t > 1) { window._taps.push('intro'); chip.click(); }" \
    " if (s.clip === 'purn_name' && s.playing) window._seen0 = true;" \
    " if (chip && !window._taps.includes('breath') && window._seen0 && s.clip === 'purn_name' && !s.playing) { window._taps.push('breath'); chip.click(); }" \
    " if (!s.nav) requestAnimationFrame(step); }; requestAnimationFrame(step); }"

def ink_bbox(img, region, kind):
    x0, y0, x1, y1 = region
    a = np.asarray(img.crop(region).convert("RGB"), np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    if kind == "navy": m = (r < 140) & (b - r > 55)
    ys, xs = np.nonzero(m)
    if len(xs) == 0: return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1, int(m.sum()))

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs, bad = [], []

    # ---- 1-2. timing at 1333x750
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(NAVLOG); pg.evaluate(TIMELINE, SAMPLE); pg.evaluate(GOTO, "T1")
    rows = pg.evaluate("CARD.slides[state.idx].data.rows")
    times = [r[k]["word_times"] for r in rows for k in ("name", "when", "example")]
    pg.wait_for_function("!!document.querySelector('.sfig-title.in')", timeout=10000, polling=20); pg.wait_for_timeout(700)
    pg.screenshot(path=str(out / "a_title_in_1333.png"))
    pg.wait_for_function("!!document.querySelector('.r1 .rcf-eg.in')", timeout=30000, polling=20); pg.wait_for_timeout(900)
    pg.screenshot(path=str(out / "b_row1_1333.png"))
    pg.wait_for_function("!!document.querySelector('.r3 .rcf-sign.in')", timeout=60000, polling=20); pg.wait_for_timeout(900)
    pg.screenshot(path=str(out / "c_row3_1333.png"))
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=90000, polling=20)
    pg.wait_for_timeout(300); pg.screenshot(path=str(out / "d_end_1333.png"))
    samples, taps = pg.evaluate("window._tl"), pg.evaluate("window._taps")
    samples = [s for s in samples if s["pops"]]   # a frame sampled before GOTO has mounted T1 has no rows yet
    with open(out / "timeline.json", "w", encoding="utf-8") as f: json.dump(samples, f, indent=0)
    ms = lambda i: samples[i]["ms"]
    first = lambda cond: next(i for i, s in enumerate(samples) if cond(s))
    i_play = first(lambda s: s["clip"] == "intro" and (s["t"] or 0) > 0)
    i_title = first(lambda s: s["title"])
    i_end0 = first(lambda s: s["clip"] == "intro" and not s["playing"] and s["ms"] > ms(i_play))
    check("the title appears as the intro line starts to sound", abs(ms(i_title) - ms(i_play)) <= 150 and not samples[0]["title"],
          f"title at {ms(i_title) - ms(i_play):+.0f} ms from the clip's first played moment")
    check("nothing of the rows shows while the intro line sounds",
          not any(any(s["pops"]) or any(s["shown"]) for s in samples[:i_end0]))
    starts = lambda clip: sum(1 for i, s in enumerate(samples) if s["clip"] == clip and s["playing"]
                              and (i == 0 or not (samples[i - 1]["clip"] == clip and samples[i - 1]["playing"])))
    check("🔊 taps during the intro and in the breath after the first name were ignored (each clip plays once)",
          taps == ["intro", "breath"] and all(starts(k) == 1 for k in ["intro"] + KEYS),
          f"taps made: {taps}, starts: {[starts(k) for k in ['intro'] + KEYS]}")
    prev_end = i_end0; pops = [0, None, 1, 2, None, 3, 4, None, 5]; worst_gap = []
    for j, k in enumerate(KEYS):
        i_s = first(lambda s: s["clip"] == k and s["playing"])
        i_e = first(lambda s: s["clip"] == k and not s["playing"] and s["ms"] > ms(i_s))
        gap = ms(i_s) - ms(prev_end); want = GAP_MARK if j % 3 == 0 else GAP
        worst_gap.append((k, round(gap), want))
        if pops[j] is not None:
            i_p = first(lambda s: s["pops"][pops[j]])
            check(f"{k}: its box pops in as its clip starts", -250 <= ms(i_p) - ms(i_s) <= 150, f"{ms(i_p) - ms(i_s):+.0f} ms")
        check(f"{k}: no word shows before its clip", all(s["shown"][j] == 0 for s in samples[:i_s]))
        timed = [s for s in samples[i_s:i_e] if s["clip"] == k and s["playing"] and s["t"] is not None]
        early = [s for s in timed if s["shown"][j] > sum(1 for t in times[j] if s["t"] + 0.04 >= t)]
        late = [s for s in timed if s["shown"][j] < sum(1 for t in times[j] if s["t"] - 0.15 >= t)]
        check(f"{k}: words arrive one by one with the clip, none early, none >150 ms late",
              len(timed) > 20 and len({s["shown"][j] for s in timed}) >= len(times[j]) - 1 and not early and not late,
              f"{len(timed)} samples, {len({s['shown'][j] for s in timed})} distinct counts / {len(times[j])} words, early {len(early)}, late {len(late)}")
        prev_end = i_e
    check("the breaths between beats are the module's (300 ms; 700 ms before the next mark), within 250 ms",
          all(w - 20 <= g <= w + 250 for _, g, w in worst_gap), worst_gap)
    i_last_end = prev_end
    check("आगे stays hidden until the last example has been read", not any(s["navVisible"] for s in samples[:i_last_end]))
    check("आगे opens (pulsing) once the last example has been read", samples[-1]["nav"] and all(s == len(t) for s, t in zip(samples[-1]["shown"], times))
          and pg.evaluate("getComputedStyle(document.getElementById('navBtn'), '::after').animationName") == "navBreathe",
          f"{ms(len(samples) - 1) - ms(i_last_end):.0f} ms after the clip ended")
    pg.evaluate("document.getElementById('navBtn').style.animation = 'none'")   # measure आगे at rest, not mid-pulse
    boxes = pg.evaluate(BOXES, list(AS_T0B)); worst = 0
    pg.evaluate("document.getElementById('navBtn').style.animation = ''")
    print("== card vs the frame; Swiftie / chip vs the story pages; आगे under the card (stage px) ==")
    for sel, exp in AS_T0B.items():
        got = boxes[sel]; d = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, d)
        print(f"  {sel:22s} got {[round(v,2) for v in got]}  want {[round(v,2) for v in exp]}  max|d|={d:.2f}")
    check("card box is the frame's; Swiftie and 🔊 chip are exactly the story pages'; आगे is centred under the card (within 0.5 px)", worst <= 0.5, f"worst {worst:.2f}px")
    card_bottom = boxes[".tut-card.sfig-card"][1] + boxes[".tut-card.sfig-card"][3]
    check("आगे clears the card and the stage bottom", boxes["#navBtn"][1] >= card_bottom + 8 and boxes["#navBtn"][1] + boxes["#navBtn"][3] <= 742,
          f"card bottom {card_bottom:.1f}, pill {boxes['#navBtn'][1]:.1f}..{boxes['#navBtn'][1] + boxes['#navBtn'][3]:.1f}")
    pg.wait_for_timeout(1200)
    pg.click(".tut-audio", force=True); pg.wait_for_timeout(400)
    r = pg.evaluate(SAMPLE)
    check("🔊 afterwards reads the marks again from the first name, title and boxes staying, words re-arriving",
          r["clip"] == "purn_name" and r["playing"] and r["shown"][0] < len(times[0]) and r["title"] and all(r["pops"]))
    check("आगे is hidden while the replay sounds", not r["navVisible"])
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=90000)
    pg.wait_for_timeout(300)
    log = [e for e in pg.evaluate("window._navLog") if e["slide"] == "T1"]
    first_on = next((e for e in log if e["img"] == "ON"), None)   # [dun-chrome] the reference's pill: disabled art through the clips, live once the last has ended
    check("आगे shows the reference's disabled pill from the start, through every clip (frame by frame, incl. the replay), and goes live only once the last example's clip has ended",
          log and log[0]["img"] == "DISABLED" and first_on is not None and first_on["clip"] == "vo_recap_prashn_eg.ogg" and not first_on["playing"],
          [(round(e["ms"]), e["img"], e["clip"], e["playing"]) for e in log])
    check("आगे is never live while a VO plays", not any(e["img"] == "ON" and e["playing"] for e in log))
    pg.click("#navBtn", force=True)   # force: the active pill pulses forever, so it is never "stable"
    pg.wait_for_function("CARD.slides[state.idx].id === 'T2'", timeout=10000)
    check("आगे leads to T2 (the run-on sentence demo, see demo_check.py), no extra gate",
          not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')") and pg.evaluate("!!document.querySelector('.sfig-full .dmf-band')"))
    pg.wait_for_timeout(1500); pg.screenshot(path=str(out / "e_T2_after.png"))
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
    pg.evaluate(GOTO, "T1")
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=90000)
    pg.wait_for_timeout(600)
    shot = out / "f_end_1280.png"; pg.screenshot(path=str(shot))
    boxes = pg.evaluate(BOXES, list(FRAME) + list(CENTRES)); worst = 0
    print("== boxes vs the frame (px) ==")
    for sel, exp in FRAME.items():
        got = boxes[sel]; d = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, d)
        print(f"  {sel:16s} got {[round(v,2) for v in got]}  frame {list(exp)}  max|d|={d:.2f}")
    for sel, (kx, x, ky, y) in CENTRES.items():
        g = boxes[sel]; gx = g[0] + g[2] / 2; gy = g[1] + g[3] / 2 if ky == "c" else g[1]
        d = max(abs(gx - x), abs(gy - y)); worst = max(worst, d)
        print(f"  {sel:16s} got ({gx:.2f}, {gy:.2f}) [{'centre' if ky == 'c' else 'top'}]  frame ({x}, {y})  max|d|={d:.2f}")
    check("every box and text box within 1 px of the frame", worst <= 1.0, f"worst {worst:.2f}px")
    one_line = pg.evaluate("""() => [...document.querySelectorAll('.rcf-name p, .rcf-when p, .rcf-eg p, .sfig-title p')].every(p => {
      const ws = [...p.querySelectorAll('.sfig-w')]; const tops = new Set(ws.map(w => Math.round(w.getBoundingClientRect().top))); return tops.size <= 1; })""")
    check("every text stays on one line", one_line)
    fonts = pg.evaluate("""[getComputedStyle(document.querySelector('.sfig-title')).fontSize, getComputedStyle(document.querySelector('.rcf-mark')).fontSize,
      getComputedStyle(document.querySelector('.rcf-name')).fontSize, getComputedStyle(document.querySelector('.rcf-eg p')).fontSize,
      document.fonts.check("600 28px 'Story Noto Sans Devanagari'", 'बात'), document.fonts.check("600 22px 'Story Noto Sans Devanagari'", 'रीना')]""")
    check("fonts: Noto Sans Devanagari SemiBold — 64px title and marks, 28px names/uses, 22px examples", fonts == ["64px", "64px", "28px", "22px", True, True], fonts)
    mine = Image.open(shot).convert("RGB")
    print("== text ink vs the Figma render (page px): centre and size ==")
    worst_c = worst_s = 0
    for name, region in INK.items():
        a, t = ink_bbox(mine, region, "navy"), ink_bbox(target, region, "navy")
        if not a or not t: print(f"  {name:8s} NO INK {a} {t}"); worst_c = 99; continue
        dc = ((a[0] + a[2]) / 2 - (t[0] + t[2]) / 2, (a[1] + a[3]) / 2 - (t[1] + t[3]) / 2)
        ds = ((a[2] - a[0]) - (t[2] - t[0]), (a[3] - a[1]) - (t[3] - t[1]))
        tol = 10 if name == "eg 1" else 3   # [vo-rec] the पूर्ण-विराम example reads "पिंकी स्कूल गई ।" (the recording's word), the frame's "रीना ..." is 8 px narrower
        worst_c = max(worst_c, abs(dc[0]), abs(dc[1])); worst_s = max(worst_s, abs(ds[0]) - tol + 3, abs(ds[1]))
        print(f"  {name:8s} mine {a[:4]}  figma {t[:4]}  centre d=({dc[0]:+.1f},{dc[1]:+.1f})  size d=({ds[0]:+d},{ds[1]:+d})")
    check("each text's ink sits where the render's does (centre within 1.5 px, size within 3 px; the पूर्ण-विराम example, reading पिंकी for the frame's रीना since [vo-rec], within 10 px)",
          worst_c <= 1.5 and worst_s <= 3, f"centre {worst_c:.1f}px, size (over the allowance) {worst_s}px")
    A = np.asarray(mine, np.int16); B = np.asarray(target, np.int16)
    pad = np.pad(B, ((1, 1), (1, 1), (0, 0)), mode="edge")
    near = np.min([np.abs(A - pad[1+dy:1+dy+A.shape[0], 1+dx:1+dx+A.shape[1]]).max(axis=2)
                   for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
    x0, y0, x1, y1 = CONTENT; c = near[y0:y1, x0:x1]
    big = int((c > 32).sum()); px = c.size
    print(f"  pixel diff vs Figma render over the title + rows (within 1 px): {big} of {px} px differ by >32 levels ({100*big/px:.2f}%)")
    Image.fromarray(np.where(c > 32, 255, 0).astype(np.uint8)).save(out / "f_diff_mask.png")
    check("title + rows pixel-match the Figma render (within 1 px: >32-level diffs under 3% of the area)", big / px < 0.03)
    keep = np.zeros(near.shape, bool); x0, y0, x1, y1 = WHOLE; keep[y0:y1, x0:x1] = True
    for x0, y0, x1, y1 in OWN: keep[y0:y1, x0:x1] = False
    m = (near > 32) & keep; px = int(keep.sum())
    solid = m.copy(); solid[1:-1, 1:-1] &= m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:]
    solid[0, :] = solid[-1, :] = False; solid[:, 0] = solid[:, -1] = False
    print(f"  pixel diff vs Figma render over the whole card, less Swiftie/chip/आगे (within 1 px): {int(m.sum())} of {px} px"
          f" ({100*m.sum()/px:.2f}%), of them solid: {int(solid.sum())} ({100*solid.sum()/px:.3f}%)")
    Image.fromarray(np.where(m, 255, np.where(keep, 0, 60)).astype(np.uint8)).save(out / "f_diff_mask_card.png")
    check("the whole card (edges, corners, grid, boxes) pixel-matches the Figma render (solid diffs under 0.05% of the area)",
          solid.sum() / px < 0.0005)
    pg.close()
    b.close()
check("no page errors", not errs, errs[:3]); check("no failed requests", not bad, bad[:5])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
