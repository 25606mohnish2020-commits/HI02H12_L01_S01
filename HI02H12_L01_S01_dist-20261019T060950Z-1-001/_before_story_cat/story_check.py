"""The story page T0 ([story-fig] layout, [story-pinki] beats): FOUR beats on one layout — the Figma frames 652:3, 652:192,
660:127 and 653:381 (Pinki, her mother and the cat) — each a new picture in the grey-bordered frame and a new text that
arrives word by word with its recorded clip (vo_story_b1..b4). The page opens on the recorded line "आइए इन वाक्यों को सुनते
हैं।" (vo_story_s0, [vo-rec]); between beats the finished text leaves one second after its clip, the next picture appears over
the last one and its clip starts once it has landed. आगे is the reference's pill ([dun-chrome]): disabled through the beats, live
and breathing once the LAST clip has ended; the 🔊 chip
replays the beat on screen from its first word, hiding आगे until that replay ends.
Checks: the real flow from the start gate (the opening line, each beat's word sync, the three turns, a 🔊 tap in the first turn
ignored, आगे's states frame by frame, the replay, आगे -> T0B); a stalled last clip (the watchdog opens आगे live); geometry and
pixel diffs against the four Figma renders at 1280x720.
usage: python -I -X utf8 story_check.py <index.html> <render_652-3.png> <render_652-192.png> <render_660-127.png> <render_653-381.png> <outdir>
       (the renders: story_b1..b4_figma_render_1280x720.png next to this script)
Screenshots in <outdir>: 1_gate.png, 3*_1333.png (the flow), 2_beat<k>_1280.png (+ _diff_mask.png), 3f_replay_1333.png, 4_T0B_after_story.png
"""
import sys, json, pathlib
import numpy as np
from playwright.sync_api import sync_playwright
from PIL import Image

html = pathlib.Path(sys.argv[1]).resolve()
targets = [Image.open(sys.argv[k]).convert("RGB") for k in (2, 3, 4, 5)]
out = pathlib.Path(sys.argv[6]).resolve(); out.mkdir(parents=True, exist_ok=True)
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)

COMMON = {   # frame px, from the Figma metadata / design context; identical in all four frames
  ".sfig-pic":           (108+317-4, 118+13-4, 438, 232),   # 430x224 frame + its 4px OUTSIDE stroke
  ".sfig-textbox":       (108+314, 118+250, 436, 119),
}
REFERENCE = {   # stage px on the reference game's T1/T2 (same on every beat)
  ".tut-card.sfig-card": (100, 96, 1133, 562),
  ".sfig-swiftie":       (76, 472, 190, 190),
  ".tut-audio":          (202, 606, 58, 58),
}
CONTENT = (416, 122, 864, 492)   # frame px region holding the picture + text box, for the Figma pixel diff
BEAT = [   # each beat's picture node (its offset and size inside the 430x224 box) and the frame's text lines
  {"img": (".sfig-img.b1", (108+317-14, 118+13-3, 458, 229)), "lines": ["पिंकी बोली, “माँ बिल्ली रसोई में जा रही है।”"]},   # node 668:314
  {"img": (".sfig-img.b2", (108+317-16, 118+13-4, 462, 231)), "lines": ["माँ ने कहा, “उसे रोको मत जाने दो।”"]},             # node 669:317
  {"img": (".sfig-img.b3", (108+317-14, 118+13-2, 458, 229)), "lines": ["पिंकी ने पूछा, “क्या, उसे जाने दूँ ?”"]},           # node 671:320
  {"img": (".sfig-img.b4", (108+317+0, 118+13-9, 430, 242)),  "lines": ["माँ ने कहा, “उसे रोको, मत जाने दो।”"]},            # node 653:563
]
BOXES = """(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
  if (!e) { o[s] = null; continue; } const r = e.getBoundingClientRect(); o[s] = [r.left, r.top, r.width, r.height]; } return o; }"""
LEAVE_TO = """(i) => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); mountSlide(i); }"""
# one frame: the clip (s0 = the opening line, b1..b4 = the beats), its clock, each beat's shown words / gone text / picture, आगे
SAMPLE = """() => { const a = currentAudio, src = a ? a.src : '', nav = document.getElementById('navBtn'), m = src.match(/vo_story_(\\w+)\\.ogg/);
  const texts = [...document.querySelectorAll('.sfig-text')], pics = [...document.querySelectorAll('.sfig-img')];
  return { clip: m ? m[1] : null, t: a ? a.currentTime : null, playing: isPlaying,
    shown: texts.map(x => x.querySelectorAll('.sfig-w.on').length), gone: texts.map(x => x.classList.contains('gone')), pic: pics.map(p => p.classList.contains('on')),
    navVisible: nav.classList.contains('visible'), nav: nav.classList.contains('active'), ms: performance.now() }; }"""
# every animation frame: which आगे art is on screen (none / ON = the live pill / DISABLED = the greyed-out one)
NAVLOG = """() => { window._navLog = []; const btn = document.getElementById('navBtn'); let last = ''; const t0 = performance.now();
  const step = () => { const cs = getComputedStyle(btn);   // [dun-chrome] a bare text button: live = .active (the disabled art otherwise), its ::after breathes (navBreathe)
    const shown = cs.visibility === 'visible' && parseFloat(cs.opacity) > 0.01 && cs.display !== 'none';
    const img = !shown ? 'none' : btn.classList.contains('active') ? 'ON' : 'DISABLED';
    const a = currentAudio, slide = CARD.slides[state.idx] ? CARD.slides[state.idx].id : null;
    const key = [img, slide, isPlaying].join('|');
    if (key !== last) { last = key; window._navLog.push({ ms: performance.now() - t0, img, slide, playing: isPlaying,
      clip: a ? a.src.split('/').pop() : null, story: !!document.querySelector('.sfig-card') }); }
    requestAnimationFrame(step); };
  requestAnimationFrame(step); }"""
LINES_OF = """(k) => { const ws = [...document.querySelectorAll('.sfig-text.b' + k + ' .sfig-w')];
  const tops = [...new Set(ws.map(w => Math.round(w.getBoundingClientRect().top)))];
  return tops.map(t => ws.filter(w => Math.round(w.getBoundingClientRect().top) === t).map(w => w.textContent).join(' ')); }"""
PULSING = "getComputedStyle(document.getElementById('navBtn'), '::after').animationName"

def sync_checks(tag, samples, k, times):
    """beat k (0-based): its words arrive one by one as its clip reaches them (on the clip's own clock), none early, none late"""
    clip = f"b{k + 1}"
    timed = [s for s in samples if s["clip"] == clip and s["playing"] and s["t"] is not None]
    shown = lambda s: s["shown"][k]
    early = [s for s in timed if shown(s) > sum(1 for t in times if s["t"] + 0.04 >= t)]
    late  = [s for s in timed if shown(s) < sum(1 for t in times if s["t"] - 0.15 >= t)]
    distinct = len(set(times))   # a mark-only word ("?”") arrives with the word before it
    check(f"{tag}: words appear one by one with the clip", len(timed) > 40 and len({shown(s) for s in timed}) >= distinct - 2,
          f"{len(timed)} samples while the clip played, {len({shown(s) for s in timed})} distinct word counts / {len(times)} words")
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
    beats = pg.evaluate("CARD.slides[state.idx].data.beats"); N = len(beats); T = [bt["word_times"] for bt in beats]
    check("four beats, the frames' texts (with their punctuation), each on its own recorded clip (vo_story_b1..b4)",
          N == 4 and [bt["text_hi"] for bt in beats] == [bt["lines"][0] for bt in BEAT] and [bt["audio"] for bt in beats] == [f"vo_story_b{k}" for k in (1, 2, 3, 4)]
          and all(len(t) == len(bt["text_hi"].split()) for t, bt in zip(T, beats)), [bt["text_hi"] for bt in beats])
    samples, shots, tapped = [], set(), False
    for _ in range(3200):
        s = pg.evaluate(SAMPLE); samples.append(s)
        if s["nav"]: break
        done1 = s["clip"] == "b1" and s["shown"][0] == len(T[0]) and not s["playing"]
        for name, cond in (("3a_beat1_mid", s["shown"][0] >= 4), ("3b_beat1_end", done1), ("3c_turn", s["pic"][1]), ("3d_beat2_mid", s["shown"][1] >= 4),
                           ("3e_beat3_mid", s["shown"][2] >= 4), ("3f_beat4_mid", s["shown"][3] >= 4)):
            if cond and name not in shots:
                shots.add(name); pg.screenshot(path=str(out / f"{name}_1333.png"))
        if not tapped and done1:
            tapped = True; pg.click(".tut-audio", force=True)   # a 🔊 tap in the pause before the turn must be ignored
        pg.wait_for_timeout(25)
    pg.screenshot(path=str(out / "3g_beat4_end_1333.png"))
    boxes = pg.evaluate(BOXES, list(REFERENCE)); worst = 0
    print("== card / Swiftie / chip vs the reference game (stage px) ==")
    for sel, exp in REFERENCE.items():
        got = boxes[sel]; d = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, d)
        print(f"  {sel:22s} got {[round(v,2) for v in got]}  reference {list(exp)}  max|d|={d:.2f}")
    check("card size, Swiftie and the 🔊 chip match the reference game's T1/T2 (within 0.5 px)", worst <= 0.5, f"worst {worst:.2f}px")
    with open(out / "sync_log.json", "w", encoding="utf-8") as f: json.dump({"beats": beats, "samples": samples}, f, indent=0)
    ms = lambda i: samples[i]["ms"]
    first = lambda cond, start=0: next(i for i in range(start, len(samples)) if cond(samples[i]))
    # the opening line, then beat 1
    i_s0 = first(lambda s: s["clip"] == "s0" and s["playing"]); i_s0e = first(lambda s: s["clip"] != "s0" or not s["playing"], i_s0 + 1)   # beat 1 follows at once: the ended frame may be missed
    i_b1 = first(lambda s: s["clip"] == "b1" and s["playing"])
    check("the opening line (vo_story_s0, “आइए इन वाक्यों को सुनते हैं।”) sounds first, beat 1's picture up and its text empty; beat 1's clip starts once it has ended",
          i_s0 < i_s0e <= i_b1 and all(s["shown"][0] == 0 and s["pic"][0] for s in samples[:i_b1]) and ms(i_b1) - ms(i_s0e) <= 800, f"beat 1 {ms(i_b1) - ms(i_s0e):.0f} ms after the line")
    for k in range(N): sync_checks(f"beat {k + 1}", samples, k, T[k])
    # the turns between the beats
    i_end = [first(lambda s, k=k: s["clip"] == f"b{k + 1}" and s["shown"][k] == len(T[k]) and not s["playing"]) for k in range(N)]
    for k in range(N - 1):
        i_gone = first(lambda s, k=k: s["gone"][k]); i_vo = first(lambda s, k=k: s["clip"] == f"b{k + 2}" and s["playing"])
        pause = ms(i_gone) - ms(i_end[k]); land = ms(i_vo) - ms(i_gone)
        check(f"beat {k + 1}'s text leaves one second after its clip ends", 900 <= pause <= 1300, f"{pause:.0f} ms")
        check(f"picture {k + 2} appears in the same beat as text {k + 1} leaves (over the last picture)", samples[i_gone]["pic"][k + 1] and not samples[i_gone - 1]["pic"][k + 1] and samples[i_gone]["pic"][k])
        check(f"beat {k + 2}'s clip starts once picture {k + 2} has landed (~0.65 s)", 600 <= land <= 1000, f"{land:.0f} ms after the turn")
        check(f"no beat-{k + 2} word shows before the turn", all(s["shown"][k + 1] == 0 for s in samples[:i_vo]))
    check("the 🔊 tap during the first turn was ignored (beat 1 never restarts)", tapped and not any(s["clip"] == "b1" and s["playing"] for s in samples[i_end[0]:]))
    check("आगे stays hidden through every beat and turn", not any(s["navVisible"] for s in samples[:i_end[-1]]))
    check("आगे opens (pulsing) once the last clip has ended", samples[-1]["nav"] and samples[-1]["shown"][-1] == len(T[-1]) and pg.evaluate(PULSING) == "navBreathe",
          f"{ms(len(samples) - 1) - ms(i_end[-1]):.0f} ms after the clip ended")
    pg.wait_for_timeout(1200)
    pg.click(".tut-audio", force=True); pg.wait_for_timeout(400)
    r = pg.evaluate(SAMPLE)
    check("🔊 afterwards replays the last beat on its picture from its first word", r["clip"] == f"b{N}" and r["playing"] and r["shown"][-1] < len(T[-1]) and r["pic"][-1] and all(r["gone"][:-1]))
    check("आगे is hidden while the replay sounds", not r["navVisible"])
    pg.screenshot(path=str(out / "3h_replay_1333.png"))
    pg.wait_for_function("!isPlaying", timeout=20000)
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=2000)
    check("आगे comes back live and pulsing when the replay ends", pg.evaluate(PULSING) == "navBreathe")
    pg.wait_for_timeout(300)
    pg.click("#navBtn", force=True)   # force: the active pill breathes forever, so it is never "stable"
    pg.wait_for_function("CARD.slides[state.idx].id === 'T0B' && !!document.querySelector('.sfig-card .sfig-title')", timeout=10000)
    log = [e for e in pg.evaluate("window._navLog") if e["slide"] == "T0"]
    with open(out / "nav_log.json", "w", encoding="utf-8") as f: json.dump(log, f, indent=0)
    print("  आगे on the story page:", [(round(e["ms"]), e["img"], e["clip"], e["playing"]) for e in log])
    first_on = next((e for e in log if e["img"] == "ON"), None)   # [dun-chrome] the reference's pill: disabled art through the clips, live once the last has ended
    first_story = next((e for e in log if e["clip"] and e["clip"].startswith("vo_story")), None)   # the entries before it are the gate's (the slide is T0 under it)
    check("आगे shows the reference's disabled pill from the story's first clip, through every beat (frame by frame, incl. a replay)", first_story is not None and first_story["img"] == "DISABLED",
          [(round(e["ms"]), e["img"], e["clip"], e["playing"]) for e in log][:6])
    check("आगे goes live only once the last clip has ended", first_on is not None and first_on["clip"] == f"vo_story_b{N}.ogg" and not first_on["playing"])
    check("आगे is never live while a story clip plays", not any(e["img"] == "ON" and e["playing"] for e in log))
    check("आगे leads to T0B (\"आइए वाक्य सुनें।\"), no extra gate", not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"))
    pg.wait_for_timeout(1500); pg.screenshot(path=str(out / "4_T0B_after_story.png"))
    pg.close()

    # ---- 3b. the last clip never starts or ends (a stalled media load): the watchdog must still finish the page
    #          and open आगे live — never leave the disabled pill under a "playing" clip
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(f"""() => {{ const orig = HTMLMediaElement.prototype.play;
      HTMLMediaElement.prototype.play = function(){{ return String(this.src).includes('vo_story_b{N}') ? Promise.resolve() : orig.call(this); }}; }}""")
    pg.evaluate(NAVLOG); pg.evaluate(LEAVE_TO, 0)
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=60000)
    pg.wait_for_timeout(400)   # let the logger see the pill fade in
    log = [e for e in pg.evaluate("window._navLog") if e["slide"] == "T0"]
    check("stalled last clip: the watchdog finishes the page and opens आगे live (the disabled pill until then)",
          log[-1]["img"] == "ON" and not any(e["img"] == "ON" and e["playing"] for e in log) and not pg.evaluate("isPlaying")
          and pg.evaluate(f"document.querySelectorAll('.sfig-text.b{N} .sfig-w.on').length") == len(T[-1]),
          [(round(e["ms"]), e["img"], e["clip"], e["playing"]) for e in log])
    pg.close()

    # ---- 4. geometry + pixel diff at 1280x720, at the end of each beat
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(LEAVE_TO, 0)
    pg.evaluate("document.fonts.ready")
    check("Noto Sans Devanagari SemiBold is loaded for the story text",
          pg.evaluate("document.fonts.check(\"600 26px 'Story Noto Sans Devanagari'\", 'पिंकी')"))
    for k, (beat, target) in enumerate(zip(BEAT, targets), 1):
        n = len(T[k - 1])
        if k < N:   # beat k complete, in the one-second pause before the turn
            pg.wait_for_function(f"!isPlaying && document.querySelectorAll('.sfig-text.b{k} .sfig-w.on').length === {n} && !document.querySelector('.sfig-text.b{k}').classList.contains('gone')", timeout=40000, polling=20)
            pg.wait_for_timeout(260)   # the last word's 0.26 s entrance
        else:
            pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=40000)
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
        check(f"beat {k}: text breaks into the frame's {len(beat['lines'])} line(s)", lines == beat["lines"])
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
