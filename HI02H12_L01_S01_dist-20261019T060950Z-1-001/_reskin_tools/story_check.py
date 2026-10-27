"""Verify the story page (STORY_LISTEN, slide T0) against its two Figma frames and check the word reveal vs the VO.
usage: python -I -X utf8 story_check.py <index.html> <figma_render_beat1.png> <figma_render_beat2.png> <outdir>
       (the renders: story_figma_render_1280x720.png = frame 435:5, story2_figma_render_1280x720.png = frame 476:198)
1. Real flow at 1333x750: landing -> शुरू करें -> peek gate -> the story page is the screen the gate opens onto.
2. Each beat's word reveal vs its own clip: sampled every ~30 ms, a word may not show before its start time and
   must show within 150 ms of it.
3. The turn between beats: one second after line 1's VO ends its text leaves and picture 2 appears; line 2's VO
   starts once the picture has landed; a 🔊 tap during the turn is ignored; आगे stays hidden until line 2's VO
   has ended, then opens; the chip afterwards replays line 2; आगे leads to T0B ("आइए वाक्य सुनें।", see relisten_check.py).
4. The card's box, Swiftie and the 🔊 chip vs the reference game's T1/T2 (https://hi-02-h04-l01-s01-dun.vercel.app/,
   measured on its 1333x750 stage on 2026-10-21): card 100,96 1133x562, Swiftie 76,472 190x190, chip 202,606 58x58.
5. 1280x720 viewport (stage scale x fig scale = 1, so stage px == frame px): at the end of each beat, the
   picture and text box vs that frame, the text's line breaks, and a per-pixel diff vs that frame's Figma render
   over the picture + text box (the card outline, Swiftie and the chip follow the reference game, not the frame).
"""
import sys, json, pathlib
import numpy as np
from playwright.sync_api import sync_playwright
from PIL import Image

html = pathlib.Path(sys.argv[1]).resolve()
targets = [Image.open(sys.argv[2]).convert("RGB"), Image.open(sys.argv[3]).convert("RGB")]
out = pathlib.Path(sys.argv[4]).resolve(); out.mkdir(parents=True, exist_ok=True)
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)

COMMON = {   # frame px, from the Figma metadata / design context; identical in both frames
  ".sfig-pic":           (108+317-4, 118+13-4, 438, 232),   # 430x224 frame + its 4px OUTSIDE stroke
  ".sfig-textbox":       (108+314, 118+250, 436, 119),
}
REFERENCE = {   # stage px on the reference game's T1/T2 (same on both)
  ".tut-card.sfig-card": (100, 96, 1133, 562),
  ".sfig-swiftie":       (76, 472, 190, 190),
  ".tut-audio":          (202, 606, 58, 58),
}
CONTENT = (416, 122, 864, 492)   # frame px region holding the picture + text box, for the Figma pixel diff
BEAT = [
  {"img": (".sfig-img.b1", (108+317-3, 118+13-11, 436, 245)),          # node 470:477
   "lines": ["चिंटू दौड़कर आया और बोला दादी बिल्ली दूध", "पी रही है दादी बोली उसे भगाओ मत पीने दो"]},
  {"img": (".sfig-img.b2", (108+317-9, 118+13-14, 448, 252)),          # node 476:197
   "lines": ["चिंटू हैरान होकर बोला क्या उसे सारा दूध", "पीने दूँ दादी हँसकर बोली अरे नहीं उसे", "भगाओ दूध मत पीने दो"]},
]
BOXES = """(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
  if (!e) { o[s] = null; continue; } const r = e.getBoundingClientRect(); o[s] = [r.left, r.top, r.width, r.height]; } return o; }"""
LEAVE_TO = """(i) => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); mountSlide(i); }"""
SAMPLE = """() => { const a = currentAudio, src = a ? a.src : '', nav = document.getElementById('navBtn');
  const q = (s) => document.querySelector(s);
  return { clip: src.includes('vo_story_s1') ? 's1' : src.includes('vo_story_s2') ? 's2' : null,
    t: a ? a.currentTime : null, playing: isPlaying,
    s1: document.querySelectorAll('.sfig-text.b1 .sfig-w.on').length, s2: document.querySelectorAll('.sfig-text.b2 .sfig-w.on').length,
    gone1: q('.sfig-text.b1').classList.contains('gone'), pic2: q('.sfig-img.b2').classList.contains('on'),
    navVisible: nav.classList.contains('visible'), nav: nav.classList.contains('active'), ms: performance.now() }; }"""
# every animation frame: which आगे art is on screen (none / ON = the live pill / DISABLED = the greyed-out one)
NAVLOG = """() => { window._navLog = []; const btn = document.getElementById('navBtn'); let last = ''; const t0 = performance.now();
  const step = () => { const cs = getComputedStyle(btn), off = btn.querySelector('.btn-off'), on = btn.querySelector('.btn-on');
    const shown = cs.visibility === 'visible' && parseFloat(cs.opacity) > 0.01;
    const img = !shown ? 'none' : getComputedStyle(on).display !== 'none' ? 'ON' : getComputedStyle(off).display !== 'none' ? 'DISABLED' : '?';
    const a = currentAudio, slide = CARD.slides[state.idx] ? CARD.slides[state.idx].id : null;
    const key = [img, slide, isPlaying].join('|');
    if (key !== last) { last = key; window._navLog.push({ ms: performance.now() - t0, img, slide, playing: isPlaying,
      clip: a ? a.src.split('/').pop() : null, story: !!document.querySelector('.sfig-card') }); }
    requestAnimationFrame(step); };
  requestAnimationFrame(step); }"""
LINES_OF = """(k) => { const ws = [...document.querySelectorAll('.sfig-text.b' + k + ' .sfig-w')];
  const tops = [...new Set(ws.map(w => Math.round(w.getBoundingClientRect().top)))];
  return tops.map(t => ws.filter(w => Math.round(w.getBoundingClientRect().top) === t).map(w => w.textContent).join(' ')); }"""

def sync_checks(tag, samples, key, times):
    timed = [s for s in samples if s["clip"] == f"s{key}" and s["playing"] and s["t"] is not None]
    shown = lambda s: s[f"s{key}"]
    early = [s for s in timed if shown(s) > sum(1 for t in times if s["t"] + 0.04 >= t)]
    late  = [s for s in timed if shown(s) < sum(1 for t in times if s["t"] - 0.15 >= t)]
    check(f"{tag}: words appear one by one with the clip", len(timed) > 50 and len({shown(s) for s in timed}) >= len(times) - 2,
          f"{len(timed)} samples while the clip played, {len({shown(s) for s in timed})} distinct word counts")
    check(f"{tag}: no word shows before the narration reaches it", not early, early[:2])
    check(f"{tag}: no word lags its start time by >150 ms", not late, late[:2])
    first_t = next((s["t"] for s in timed if shown(s) >= 1), None)
    check(f"{tag}: first word appears as the clip starts speaking", first_t is not None and first_t < times[0] + 0.15,
          f"at {first_t:.3f}s, word starts {times[0]}s" if first_t is not None else "")

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs, bad = [], []

    # ---- 1-3. real flow at 1333x750
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(2500)
    pg.wait_for_function("!document.body.classList.contains('vo-lock')", timeout=25000)
    pg.evaluate(NAVLOG)
    pg.click("#sgBtn", force=True)
    pg.wait_for_function("document.getElementById('phaseGate').classList.contains('pg-say')", timeout=15000)   # [dun-chrome] the headline is in (GATE-REF-ANIM)
    pg.screenshot(path=str(out / "1_gate.png"))
    pg.wait_for_function("!!document.querySelector('.sfig-card') && !document.getElementById('phaseGate').classList.contains('show')", timeout=20000)
    check("the gate opens onto the story page (slide T0)", pg.evaluate("CARD.slides[state.idx].id") == "T0")
    beats = pg.evaluate("CARD.slides[state.idx].data.beats")
    t1, t2 = beats[0]["word_times"], beats[1]["word_times"]
    samples, shots, tapped = [], set(), False
    for _ in range(2000):
        s = pg.evaluate(SAMPLE); samples.append(s)
        if s["nav"]: break
        for name, cond in (("3a_beat1_mid", s["s1"] >= 9), ("3b_beat1_end", s["clip"] == "s1" and s["s1"] == len(t1) and not s["playing"]),
                           ("3c_turn", s["pic2"]), ("3d_beat2_mid", s["s2"] >= 10)):
            if cond and name not in shots:
                shots.add(name); pg.screenshot(path=str(out / f"{name}_1333.png"))
        if not tapped and s["clip"] == "s1" and s["s1"] == len(t1) and not s["playing"]:
            tapped = True; pg.click(".tut-audio", force=True)   # a 🔊 tap in the pause before the turn must be ignored
        pg.wait_for_timeout(25)
    pg.screenshot(path=str(out / "3e_beat2_end_1333.png"))
    boxes = pg.evaluate(BOXES, list(REFERENCE)); worst = 0
    print("== card / Swiftie / chip vs the reference game (stage px) ==")
    for sel, exp in REFERENCE.items():
        got = boxes[sel]; d = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, d)
        print(f"  {sel:22s} got {[round(v,2) for v in got]}  reference {list(exp)}  max|d|={d:.2f}")
    check("card size, Swiftie and the 🔊 chip match the reference game's T1/T2 (within 0.5 px)", worst <= 0.5, f"worst {worst:.2f}px")
    with open(out / "sync_log.json", "w", encoding="utf-8") as f: json.dump({"beats": beats, "samples": samples}, f, indent=0)

    sync_checks("line 1", samples, 1, t1)
    sync_checks("line 2", samples, 2, t2)
    i_end1 = next(i for i, s in enumerate(samples) if s["clip"] == "s1" and s["s1"] == len(t1) and not s["playing"])
    i_gone = next(i for i, s in enumerate(samples) if s["gone1"])
    i_vo2 = next(i for i, s in enumerate(samples) if s["clip"] == "s2" and s["playing"])
    i_end2 = next(i for i, s in enumerate(samples) if s["clip"] == "s2" and s["s2"] == len(t2) and not s["playing"])
    pause = samples[i_gone]["ms"] - samples[i_end1]["ms"]; land = samples[i_vo2]["ms"] - samples[i_gone]["ms"]
    check("line 1's text leaves one second after its VO ends", 900 <= pause <= 1300, f"{pause:.0f} ms")
    check("picture 2 appears in the same beat as line 1's text leaves", samples[i_gone]["pic2"] and not samples[i_gone - 1]["pic2"])
    check("line 2's VO starts once picture 2 has landed (~0.65 s)", 600 <= land <= 1000, f"{land:.0f} ms after the turn")
    check("the 🔊 tap during the turn was ignored (line 1 never restarts)",
          tapped and not any(s["clip"] == "s1" and s["playing"] for s in samples[i_end1:]))
    check("no line-2 word shows before the turn", all(s["s2"] == 0 for s in samples[:i_vo2]))
    check("आगे stays hidden through line 1, the turn and line 2", not any(s["navVisible"] for s in samples[:i_end2]))
    check("आगे opens (pulsing) once line 2's VO has ended", samples[-1]["nav"] and samples[-1]["s2"] == len(t2)
          and pg.evaluate("getComputedStyle(document.getElementById('navBtn')).animationName") == "nextBtnPulse",
          f"{samples[-1]['ms'] - samples[i_end2]['ms']:.0f} ms after the clip ended")
    pg.wait_for_timeout(1200)
    pg.click(".tut-audio", force=True); pg.wait_for_timeout(400)
    r = pg.evaluate(SAMPLE)
    check("🔊 afterwards replays line 2 on picture 2 from its first word", r["clip"] == "s2" and r["playing"] and r["s2"] < len(t2) and r["pic2"] and r["gone1"])
    check("आगे is hidden while the replay sounds", not r["navVisible"])
    pg.screenshot(path=str(out / "3f_replay_1333.png"))
    pg.wait_for_function("!isPlaying", timeout=20000)
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=2000)
    check("आगे comes back live and pulsing when the replay ends",
          pg.evaluate("getComputedStyle(document.getElementById('navBtn')).animationName") == "nextBtnPulse")
    pg.wait_for_timeout(300)
    pg.click("#navBtn", force=True)   # force: the active pill pulses forever, so it is never "stable"
    pg.wait_for_function("CARD.slides[state.idx].id === 'T0B' && !!document.querySelector('.sfig-card .sfig-title')", timeout=10000)
    log = [e for e in pg.evaluate("window._navLog") if e["slide"] == "T0"]
    with open(out / "nav_log.json", "w", encoding="utf-8") as f: json.dump(log, f, indent=0)
    print("  आगे on the story page:", [(round(e["ms"]), e["img"], e["clip"], e["playing"]) for e in log])
    check("the greyed-out आगे never shows on the story page (frame by frame, incl. a replay)", not any(e["img"] == "DISABLED" for e in log))
    first_on = next((e for e in log if e["img"] == "ON"), None)
    check("आगे first shows only once line 2's VO has ended", first_on is not None and first_on["clip"] == "vo_story_s2.ogg" and not first_on["playing"])
    check("आगे never shows while a story VO plays", not any(e["img"] != "none" and e["playing"] for e in log))
    check("आगे leads to T0B (\"आइए वाक्य सुनें।\"), no extra gate", not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"))
    pg.wait_for_timeout(1500); pg.screenshot(path=str(out / "4_T0B_after_story.png"))
    pg.close()

    # ---- 3b. line 2's clip never starts or ends (a stalled media load): the watchdog must still finish the page
    #          and open आगे live — never leave the greyed-out pill under a "playing" clip
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate("""() => { const orig = HTMLMediaElement.prototype.play;
      HTMLMediaElement.prototype.play = function(){ return String(this.src).includes('vo_story_s2') ? Promise.resolve() : orig.call(this); }; }""")
    pg.evaluate(NAVLOG); pg.evaluate(LEAVE_TO, 0)
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=45000)
    pg.wait_for_timeout(400)   # let the logger see the pill fade in
    log = [e for e in pg.evaluate("window._navLog") if e["slide"] == "T0"]
    check("stalled line-2 clip: the watchdog finishes the page and opens आगे live, never greyed out",
          not any(e["img"] == "DISABLED" for e in log) and log[-1]["img"] == "ON" and not pg.evaluate("isPlaying")
          and pg.evaluate("document.querySelectorAll('.sfig-text.b2 .sfig-w.on').length") == len(t2),
          [(round(e["ms"]), e["img"], e["clip"], e["playing"]) for e in log])
    pg.close()

    # ---- 4. geometry + pixel diff at 1280x720, at the end of each beat
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(LEAVE_TO, 0)
    pg.evaluate("document.fonts.ready")
    check("Noto Sans Devanagari SemiBold is loaded for the story text",
          pg.evaluate("document.fonts.check(\"600 24px 'Story Noto Sans Devanagari'\", 'चिंटू')"))
    for k, (beat, target) in enumerate(zip(BEAT, targets), 1):
        n = len(beats[k - 1]["word_times"])
        if k == 1:   # line 1 complete, in the one-second pause before the turn
            pg.wait_for_function(f"!isPlaying && document.querySelectorAll('.sfig-text.b1 .sfig-w.on').length === {n}", timeout=20000, polling=20)
            pg.wait_for_timeout(260)   # the last word's 0.26 s entrance
        else:
            pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=30000)
            pg.wait_for_timeout(300)
        shot = out / f"2_beat{k}_1280.png"; pg.screenshot(path=str(shot))
        expect = dict(COMMON); expect[beat["img"][0]] = beat["img"][1]
        boxes = pg.evaluate(BOXES, list(expect))
        worst = 0
        print(f"== beat {k}: geometry (rendered vs frame, px) ==")
        for s, exp in expect.items():
            got = boxes[s]; d = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, d)
            print(f"  {s:22s} got {[round(v,2) for v in got]}  frame {list(exp)}  max|d|={d:.2f}")
        check(f"beat {k}: every frame element within 1 px of the frame", worst <= 1.0, f"worst {worst:.2f}px")
        lines = pg.evaluate(LINES_OF, k); print("  text lines:", lines)
        check(f"beat {k}: text breaks into the frame's {len(beat['lines'])} lines", lines == beat["lines"])
        img = Image.open(shot).convert("RGB")
        A = np.asarray(img, np.int16); B = np.asarray(target, np.int16); M = np.zeros(A.shape[:2], bool)
        x0, y0, x1, y1 = CONTENT; M[y0:y1, x0:x1] = True
        # the engine fits its 1333x750 stage into 1280x720 at 0.96 (height-bound), not 1280/1333, so the page lands
        # ~0.5 px off the frame grid; "near" lets each pixel match any Figma pixel within 1 px
        pad = np.pad(B, ((1, 1), (1, 1), (0, 0)), mode="edge")
        near = np.min([np.abs(A - pad[1+dy:1+dy+A.shape[0], 1+dx:1+dx+A.shape[1]]).max(axis=2)
                       for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
        px = int(M.sum()); big = int(((near > 32) & M).sum())
        print(f"  pixel diff vs Figma render over the picture + text box (within 1 px): {big} of {px} px differ by >32 levels ({100*big/px:.2f}%)")
        Image.fromarray(np.where((near > 32) & M, 255, 0).astype(np.uint8)).save(out / f"2_beat{k}_diff_mask.png")
        # what is left at this point is Figma's vs Chrome's anti-aliasing of thin edges (glyph strokes, grid lines,
        # the picture's edges); a misplaced or mis-sized element shows up as whole shapes, far above this bar
        check(f"beat {k}: picture + text box pixel-match the Figma render (within 1 px: >32-level diffs under 5% of the area)", big / px < 0.05)
    pg.close()
    b.close()
check("no page errors", not errs, errs[:3]); check("no failed requests", not bad, bad[:5])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
