"""The story page T0 ([story-fig] layout, [story-pinki] beats): FOUR beats on one layout — the Figma frames 652:3, 652:192,
660:127 and 653:381 (Pinki, her mother and the cat) — each a new picture in the grey-bordered frame and a new text that
rises in whole and is read 0.45 s later, each word lit as its recorded clip reaches it ([word-sync]; vo_story_b1..b4). The page opens on the recorded line "आइए इन वाक्यों को सुनते
हैं।" (vo_story_s0, [vo-rec]); between beats the finished text leaves one second after its clip, the next picture appears over
the last one and its clip starts once it has landed. आगे is the reference's pill ([dun-chrome]): disabled through the beats, live
and breathing once the LAST clip has ended; the 🔊 chip
replays the beat on screen from its first word, hiding आगे until that replay ends.
Checks: the real flow from the start gate (the opening line, each beat's word sync, the three turns, a 🔊 tap in the first turn
ignored, आगे's states frame by frame, the replay, आगे -> T0B); a stalled last clip (the watchdog opens आगे live); geometry and
pixel diffs of the picture against the four Figma renders at 1280x720; the white box and its type are the reference poem game's
caption ([poem-box], hi02h11l03s01poem-8cpz.vercel.app Page 1 T1: white, 26 px corners, its shadow; Baloo 2 declared 600 at 29 px on
37.12 px with 5.6 px word spacing, stage px) in ONE size for all four beats ([poem-box2]: 566 x 94, the same rect through the whole
flow), midway between the picture and आगे, the sentences' ink centred in it (line box centre 4.69 px below the box's); no word stays
lit or orange once a line has ended.
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
}
REFERENCE = {   # stage px on the reference game's T1/T2 (same on every beat)
  ".tut-card.sfig-card": (100, 96, 1133, 562),
  ".sfig-swiftie":       (76, 472, 190, 190),
  ".tut-audio":          (202, 606, 58, 58),
}
CONTENT = (416, 122, 864, 364)   # frame px region holding the picture (its frame + border), for the Figma pixel diff — [poem-box]
                                 # the text box below it is the reference poem game's caption now, not the frames' node 436:412
STAGE = 720 / 750                # stage px -> screen px at 1280x720 (the engine fits its 1333x750 stage by height)
# [poem-box] at the end of a beat: the box and the beat's text (screen px), the type in stage px, any lit / non-navy word
CAPTION = """(k) => { const box = document.querySelector('.sfig-textbox'), t = document.querySelector('.sfig-text.b' + k);
  const fig = document.querySelector('.sfig-in'), st = document.querySelector('.stage').getBoundingClientRect().width / 1333;
  const s = fig.getBoundingClientRect().width / fig.offsetWidth / st, br = box.getBoundingClientRect(), tr = t.getBoundingClientRect();
  const pr = document.querySelector('.sfig-pic').getBoundingClientRect(), nr = document.getElementById('navBtn').getBoundingClientRect();
  const bc = getComputedStyle(box), tc = getComputedStyle(t), ws = [...document.querySelectorAll('.sfig-w')];
  return { box: [br.left, br.top, br.width, br.height], text: [tr.left, tr.top, tr.width, tr.height], picBottom: pr.bottom, navTop: nr.top, radius: parseFloat(bc.borderTopLeftRadius) * s,
    bg: bc.backgroundColor, shadow: bc.boxShadow, family: tc.fontFamily, weight: tc.fontWeight, size: parseFloat(tc.fontSize) * s,
    lh: parseFloat(tc.lineHeight) * s, ws: parseFloat(tc.wordSpacing) * s, hot: ws.filter(w => w.classList.contains('hot')).length,
    orange: ws.filter(w => getComputedStyle(w).color !== 'rgb(0, 47, 118)').map(w => w.textContent) }; }"""
BEAT = [   # each beat's picture node (its offset and size inside the 430x224 box) and the frame's text lines
  # [story-pics] (2026-10-31) beats 1-3 carry the user's redrawn pictures, fitted to the box (16:9 / 1.92), not the frames' 2:1 nodes;
  # the renders have them pasted in (old renders: story_b*_figma_render_1280x720_v1_2026-10-28.png)
  {"img": (".sfig-img.b1", (108+317+0, 118+13-9, 430, 242)), "lines": ["पिंकी बोली, “माँ बिल्ली रसोई में जा रही है।”"]},   # node 668:314
  {"img": (".sfig-img.b2", (108+317+0, 118+13+0, 430, 224)), "lines": ["माँ ने कहा, “उसे रोको मत जाने दो।”"]},             # node 669:317
  {"img": (".sfig-img.b3", (108+317+0, 118+13+0, 430, 224)), "lines": ["पिंकी ने पूछा, “क्या, उसे जाने दूँ ?”"]},           # node 671:320
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
    hot: texts.map(x => [...x.querySelectorAll('.sfig-w')].map((w, i) => w.classList.contains('hot') ? i : -1).filter(i => i >= 0)),   // [word-sync] the lit word(s)
    box: (() => { const e = document.querySelector('.sfig-textbox'); if (!e) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; })(),   // [poem-box2]
    navVisible: nav.classList.contains('visible'), nav: nav.classList.contains('active'), ms: performance.now(),
    cat: (typeof _kitSfx !== 'undefined' && _kitSfx.storyBeat1) ? (_kitSfx.storyBeat1.paused ? 'paused' : 'playing') : null,   // [story-cat] beat 1's sound
    pop: pics[0] ? getComputedStyle(pics[0]).animationName : null }; }"""
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

def lit_want(times, wend, t):
    """[word-sync] the word(s) lit at clip time t: the stretch [start, next start) holding t, the last up to the last word's end
    (words sharing a start — a mark-only "?”" — light together); nothing after the end"""
    if t is None or (wend is not None and t >= wend): return []
    st = None
    for x in times:
        if t >= x: st = x
    return [i for i, x in enumerate(times) if st is not None and x == st]

def sync_checks(tag, samples, k, times, wend):
    """[word-sync] beat k (0-based): its text shows WHOLE (every word in the same frame, rising in), its clip starts ~0.45 s later,
    and while the clip plays the word lit is the one whose stretch holds the clip's time (the reference T1's wordSync)"""
    clip = f"b{k + 1}"; n = len(times)
    counts = sorted({s["shown"][k] for s in samples})
    check(f"{tag}: the whole text appears at once, never part of it", set(counts) <= {0, n}, counts)
    i_r = next((i for i, s in enumerate(samples) if s["shown"][k] == n), None)
    i_c = next((i for i, s in enumerate(samples) if s["clip"] == clip and s["playing"] and s["t"]), None)
    gap = samples[i_c]["ms"] - samples[i_r]["ms"] if i_r is not None and i_c is not None else None
    check(f"{tag}: it rises in and its clip starts ~0.45 s later (the reference's SENT_IN_MS)", gap is not None and 400 <= gap <= 800, f"{gap:.0f} ms" if gap is not None else None)
    timed = [s for s in samples if s["clip"] == clip and s["playing"] and s["t"] is not None]
    off = [s for s in timed if s["hot"][k] not in (lit_want(times, wend, s["t"]), lit_want(times, wend, s["t"] - 0.05))]   # one frame's lag allowed
    seen = {tuple(s["hot"][k]) for s in timed if s["hot"][k]}
    check(f"{tag}: each word lit as the clip reaches it, one at a time, none after the last word's end", len(timed) > 20 and not off and len(seen) >= len(set(times)) - 1,
          f"{len(timed)} samples, {len(off)} off, {len(seen)} lit states / {len(set(times))} stretches")

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
    i_r1 = first(lambda s: s["shown"][0] > 0)
    check("the opening line (vo_story_s0, “आइए इन वाक्यों को सुनते हैं।”) sounds first, beat 1's picture up and its text empty; once it has ended beat 1's text rises in and its clip follows ([word-sync])",
          i_s0 < i_s0e <= i_r1 <= i_b1 and all(s["pic"][0] for s in samples[:i_b1]) and ms(i_b1) - ms(i_s0e) <= 1250, f"beat 1 {ms(i_b1) - ms(i_s0e):.0f} ms after the line")
    WE = [bt.get("word_end") for bt in beats]
    for k in range(N): sync_checks(f"beat {k + 1}", samples, k, T[k], WE[k])
    bx_all = [s["box"] for s in samples[i_b1:] if s["box"]]   # [poem-box2] from beat 1's line to the end, through all three turns
    spread = max(max(v) - min(v) for v in zip(*bx_all)) if bx_all else None
    check("the white box keeps ONE size and place through all four beats and the turns ([poem-box2])", bx_all and spread < 0.05,
          f"{len(bx_all)} samples, max spread {spread:.3f} px" if bx_all else "no samples")
    # the turns between the beats
    i_end = [first(lambda s, k=k: s["clip"] == f"b{k + 1}" and s["shown"][k] == len(T[k]) and not s["playing"]) for k in range(N)]
    # [story-cat] as beat 1's line ends: its sound (sfx_story_cat.mp3, the kit element storyBeat1) once, with the picture's G4 pop
    firstor = lambda cond: next((i for i in range(len(samples)) if cond(samples[i])), None)
    i_cat = firstor(lambda s: s["cat"] == "playing"); i_pop = firstor(lambda s: s["pop"] == "p2BirdPop1s")
    cat_starts = sum(1 for i, s in enumerate(samples) if s["cat"] == "playing" and (i == 0 or samples[i - 1]["cat"] != "playing"))
    check("as beat 1's line ends its sound (sfx_story_cat.mp3) starts within 150 ms, together with the picture's little pop (G4's p2BirdPop1s) ([story-cat])",
          i_cat is not None and i_pop is not None and abs(ms(i_cat) - ms(i_end[0])) <= 150 and abs(ms(i_pop) - ms(i_cat)) <= 60
          and not any(s["cat"] == "playing" or s["pop"] == "p2BirdPop1s" for s in samples[:max(0, i_end[0] - 1)]),
          (None if i_cat is None else f"sound {ms(i_cat) - ms(i_end[0]):.0f} ms", None if i_pop is None else f"pop {ms(i_pop) - ms(i_end[0]):.0f} ms after the line's end"))
    check("...and only once on the page: no second start through the other beats, nor at the 🔊 tap in the first turn ([story-cat])", cat_starts == 1, cat_starts)
    for k in range(N - 1):
        i_gone = first(lambda s, k=k: s["gone"][k]); i_vo = first(lambda s, k=k: s["clip"] == f"b{k + 2}" and s["playing"])
        pause = ms(i_gone) - ms(i_end[k]); land = ms(i_vo) - ms(i_gone)
        check(f"beat {k + 1}'s text leaves one second after its clip ends", 900 <= pause <= 1300, f"{pause:.0f} ms")
        check(f"picture {k + 2} appears in the same beat as text {k + 1} leaves (over the last picture)", samples[i_gone]["pic"][k + 1] and not samples[i_gone - 1]["pic"][k + 1] and samples[i_gone]["pic"][k])
        i_rk = first(lambda s, k=k: s["shown"][k + 1] > 0); rise = ms(i_rk) - ms(i_gone)
        check(f"beat {k + 2}'s text rises in once picture {k + 2} has landed (~0.65 s), its clip ~0.45 s after that ([word-sync])", 600 <= rise <= 1000 and 1050 <= land <= 1500,
              f"text {rise:.0f} ms, clip {land:.0f} ms after the turn")
    check("the 🔊 tap during the first turn was ignored (beat 1 never restarts)", tapped and not any(s["clip"] == "b1" and s["playing"] for s in samples[i_end[0]:]))
    check("आगे stays hidden through every beat and turn", not any(s["navVisible"] for s in samples[:i_end[-1]]))
    check("आगे opens (pulsing) once the last clip has ended", samples[-1]["nav"] and samples[-1]["shown"][-1] == len(T[-1]) and pg.evaluate(PULSING) == "navBreathe",
          f"{ms(len(samples) - 1) - ms(i_end[-1]):.0f} ms after the clip ended")
    pg.wait_for_timeout(1200)
    pg.click(".tut-audio", force=True); pg.wait_for_timeout(400)
    r = pg.evaluate(SAMPLE)
    check("🔊 afterwards replays the last beat on its picture, its text staying on screen and lit word by word again ([word-sync])",
          r["clip"] == f"b{N}" and r["playing"] and r["shown"][-1] == len(T[-1]) and r["hot"][-1] in (lit_want(T[-1], beats[-1].get("word_end"), r["t"]), lit_want(T[-1], beats[-1].get("word_end"), r["t"] - 0.05)) and r["pic"][-1] and all(r["gone"][:-1]), r)
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
    check("Baloo 2 Bold (the 700 face the caption's declared 600 renders in, [poem-box]) is loaded for the story text",
          pg.evaluate("document.fonts.check(\"600 29px 'Baloo 2'\", 'पिंकी') && document.fonts.check(\"700 29px 'Baloo 2'\", 'पिंकी')"))
    for k, (beat, target) in enumerate(zip(BEAT, targets), 1):
        n = len(T[k - 1])
        if k < N:   # beat k complete, in the one-second pause before the turn
            pg.wait_for_function(f"!isPlaying && currentAudio && currentAudio.ended && currentAudio.src.includes('vo_story_b{k}.') && document.querySelectorAll('.sfig-text.b{k} .sfig-w.on').length === {n} && !document.querySelector('.sfig-text.b{k}').classList.contains('gone')", timeout=40000, polling=20)   # [word-sync] the clip has ENDED: the text is shown before it starts
            if k == 1:   # [story-cat] beat 1's line end brings the picture's 1 s pop: its peak is measured, then the pop is held off for the rest-state shot
                peak = pg.evaluate("""() => new Promise(res => { const el = document.querySelector('.sfig-img.b1'); let mx = 1; const t0 = performance.now();
                  const step = () => { const tr = getComputedStyle(el).transform; if (tr && tr !== 'none') mx = Math.max(mx, parseFloat(tr.split('(')[1]));
                    if (performance.now() - t0 < 350) requestAnimationFrame(step); else res(mx); }; requestAnimationFrame(step); })""")
                check("beat 1's picture pops as G4's does (p2BirdPop1s): its scale peaks at ~1.045 within the pop's first 0.35 s ([story-cat])", 1.03 <= peak <= 1.05, round(peak, 3))
                pg.evaluate("document.querySelector('.sfig-img.b1').style.animation = 'none'")   # the picture at rest for the layout and pixel checks
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
        cap = pg.evaluate(CAPTION, k); bx, tx = cap["box"], cap["text"]
        print(f"  caption box {[round(v, 2) for v in bx]}  text {[round(v, 2) for v in tx]}  {cap['family'].split(',')[0]} {cap['weight']} "
              f"{cap['size']:.2f}/{cap['lh']:.2f} ws {cap['ws']:.2f} radius {cap['radius']:.2f}")
        g1, g2 = (bx[1] - cap["picBottom"]) / STAGE, (cap["navTop"] - bx[1] - bx[3]) / STAGE
        dy = (tx[1] + tx[3] / 2 - bx[1] - bx[3] / 2) / STAGE
        check(f"beat {k}: the white box is the one size, 566 x 94, midway between the picture and आगे (stage px, [poem-box2])",
              abs(bx[2] - 566 * STAGE) <= 0.5 and abs(bx[3] - 94 * STAGE) <= 0.5 and abs(g1 - g2) <= 1.0,
              (round(bx[2] / STAGE, 2), round(bx[3] / STAGE, 2), f"gaps {g1:.2f} / {g2:.2f}"))
        check(f"beat {k}: the sentence sits centred in it — one line of 37.12, its ink on the box's centre (line box 4.69 px lower), centred across",
              abs(tx[3] - 37.12 * STAGE) <= 0.5 and abs(dy - 4.69) <= 0.6 and abs(bx[0] + bx[2] / 2 - tx[0] - tx[2] / 2) <= 0.5, f"dy {dy:.2f}")
        check(f"beat {k}: the box is white with 26 px corners and the caption's shadow",
              cap["bg"] == "rgb(255, 255, 255)" and abs(cap["radius"] - 26) <= 0.05
              and "rgba(11, 42, 90, 0.1)" in cap["shadow"] and "rgba(11, 42, 90, 0.12)" in cap["shadow"], (cap["bg"], round(cap["radius"], 3)))
        check(f"beat {k}: the caption's type — Baloo 2 declared 600, 29 px on 37.12 px, word spacing 5.6 px (stage px)",
              cap["family"].startswith('"Baloo 2"') and cap["weight"] == "600" and abs(cap["size"] - 29) < 0.01
              and abs(cap["lh"] - 37.12) < 0.01 and abs(cap["ws"] - 5.6) < 0.01)
        check(f"beat {k}: no word lit or orange once its line has ended", cap["hot"] == 0 and not cap["orange"], cap["orange"][:3])
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
        print(f"  pixel diff vs Figma render over the picture (within 1 px): {big} of {px} px differ by >32 levels ({100*big/px:.2f}%)")
        Image.fromarray(np.where((near > 32) & M, 255, 0).astype(np.uint8)).save(out / f"2_beat{k}_diff_mask.png")
        # what is left at this point is Figma's vs Chrome's anti-aliasing of thin edges (glyph strokes, grid lines,
        # the picture's edges); a misplaced or mis-sized element shows up as whole shapes, far above this bar
        check(f"beat {k}: the picture pixel-matches the Figma render (within 1 px: >32-level diffs under 5% of the area)", big / px < 0.05)
    pg.close()
    b.close()
check("no page errors", not errs, errs[:3]); check("no failed requests", not bad, bad[:5])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
