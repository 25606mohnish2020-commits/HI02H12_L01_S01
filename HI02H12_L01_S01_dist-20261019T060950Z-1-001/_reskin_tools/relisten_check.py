"""Verify T0B "आइए वाक्य सुनें।" (STORY_RELISTEN, [relisten-pinki]; laid out as frame 704:2 since [t0b-fig]) against its Figma
frame and its timing.
usage: python -I -X utf8 relisten_check.py <index.html> <relisten3_figma_render_1280x720.png> <outdir>
1. At 1333x750, the page mounted on its own: no title on screen (frame 704:2 has none, [t0b-fig]); the intro line ("अब इन्हीं
   वाक्यों को फिर से सुनते हैं।", vo_story_r0) sounds first; the sentence box comes in only when that line has ended; once the box has landed the two
   contrast sentences are read one after the other, each rising in whole and read 0.45 s later with each word lit as its own
   recorded clip reaches it ([word-sync]; vo_story_c1 "उसे रोको,
   मत जाने दो।", vo_story_c2 "उसे रोको मत, जाने दो।"); then the explanation (vo_story_r1) lifts sentence 1 on its yellow from
   its "पहले" and sentence 2 from its "जबकि" (the cues read off the clip by vo_rec.py), both off again when it ends; then the
   moral (vo_story_moral, 4.wav) lights the two commas orange, lifted, from its "विराम" — they stay lit; आगे shows the
   reference's disabled pill ([dun-chrome]) through all of it and goes live, breathing, once the moral has ended; a 🔊 tap
   before the sentences is ignored, and afterwards replays the whole reading (sentences, explanation, moral); आगे leads to T1
   (the three-marks recap); past the Figma pages (G4) no story styling is left over.
   [relisten-sfx] T1's text sounds ([recap-sfx], the reference hi02h11l02s04-file5 page 2's sfxPopSoft), logged in the page (the
   engine's _tone and every <audio> play, on the samples' clock): the soft pop (_tone [720] sine 0.10 / 0.07) as sentence 1 rises
   in and as sentence 2 rises in — each once, within 50 ms of its frame — and no other sound effect (the box, the highlights and
   the commas make none); the 🔊 replay silent (nothing appears again).
2. The card is the frame's (96,106 1088x508 x 1333/1280 = 100,110.39 1133x529.03 on the stage, 64px corners); Swiftie, 🔊
   chip and आगे are the story page's (T0): Swiftie 76,472 190x190, chip 202,606 58x58, आगे 581.5,550 170x62.
3. 1280x720 viewport (stage px x 1333/1280 = frame px): sentence box and the two sentence nodes' centres vs the frame, each
   sentence on one line, its ink centred where the render's is, the type page 1 T0's (Baloo 2 declared 600) at the frame's
   50px, and per-pixel diffs vs the Figma render over the box and over the whole card (less Swiftie, the chip and आगे, which
   follow T0 rather than the frame, and less the two sentences' ink bands: the frame sets them in Baloo 2 SemiBold, the page
   in T0's 700 face) — taken with the commas' end-of-page highlight cleared, since the frame draws the sentences plain.
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
FRAME = {   # frame px at 1280x720, from the design context of frame 704:2 ([t0b-fig])
  ".sfig-sbox":  (96+257-4, 106+54-4, 582, 291),   # node 704:183: 574x283 at 257,54 of the card (centred on 640) + its 4px OUTSIDE stroke
}
NODES = {   # the sentence nodes' centres (x, y) in frame px: 704:184 on 287,70 and 704:185 on 287,213 of the box
  ".sfig-stext p.l1": (96+257+287, 106+54+70),
  ".sfig-stext p.l2": (96+257+287, 106+54+213),
}
INK_BANDS = [(175, 290), (315, 430)]   # frame px rows holding each sentence's ink (inside the box, clear of its corners: x 380-900)
LINES = ["उसे रोको, मत जाने दो।", "उसे रोको मत, जाने दो।"]
CONTENT = (340, 147, 940, 456)   # frame px region holding the sentence box, for the pixel diff
WHOLE = (80, 90, 1200, 640)      # frame px: the card with its border and shadow
OWN_T0 = [(25, 400, 290, 720),   # ...less Swiftie (the frame's at 35,415 245x245 and T0's) + the 🔊 chip,
          (535, 490, 745, 600)]  # and आगे (not in the frame)
TYPE_T0 = [(420, 190, 860, 260),  # ...and the two sentences' ink, set in page 1 T0's type (Baloo 2's 700 face) where the frame
           (420, 333, 860, 403)]  # has Baloo 2 SemiBold: compared by ink box instead
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
  return { clip: m ? m[1] : null, t: a ? a.currentTime : null, playing: isPlaying, title: q('.sfig-title p') ? q('.sfig-title p').textContent : '', box: !!q('.sfig-sbox.in'),
    shown: [...document.querySelectorAll('.sfig-stext p')].map(p => p.querySelectorAll('.sfig-w.on').length),
    hot: [...document.querySelectorAll('.sfig-stext p')].map(p => [...p.querySelectorAll('.sfig-w')].map((w, i) => w.classList.contains('hot') ? i : -1).filter(i => i >= 0)),   // [word-sync]
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
# [relisten-sfx] every sound the page makes: the engine's procedural _tone and every <audio> play, on the samples' clock
SOUNDS = """() => { window._snd = []; const T = window._tone;
  window._tone = function(f, ty, d, v){ window._snd.push({ ms: performance.now(), kind: 'tone', f: f.join('/'), ty, d, v }); return T.apply(this, arguments); };
  const P = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function(){ window._snd.push({ ms: performance.now(), kind: 'media', src: decodeURIComponent(String(this.currentSrc || this.src).split('/').pop()), vol: +this.volume.toFixed(3) });
    return P.apply(this, arguments); }; }"""

def lit_want(times, wend, t):
    """[word-sync] the word(s) lit at clip time t: the stretch [start, next start) holding t (words sharing a start light together),
    the last up to the last word's end; nothing after it"""
    if t is None or (wend is not None and t >= wend): return []
    st = None
    for x in times:
        if t >= x: st = x
    return [i for i, x in enumerate(times) if st is not None and x == st]

def sync_checks(tag, samples, k, clip, times, wend):
    """[word-sync] sentence k shows WHOLE (all its words in one frame), its clip starts ~0.45 s after it rises in, and while the clip
    plays the word lit is the one whose stretch holds the clip's time (the reference T1's wordSync)"""
    n = len(times); counts = sorted({s["shown"][k] for s in samples})
    check(f"{tag}: the whole sentence appears at once, never part of it", set(counts) <= {0, n}, counts)
    i_r = next((i for i, s in enumerate(samples) if s["shown"][k] == n), None)
    i_c = next((i for i, s in enumerate(samples) if s["clip"] == clip and s["playing"] and s["t"]), None)
    gap = samples[i_c]["ms"] - samples[i_r]["ms"] if i_r is not None and i_c is not None else None
    check(f"{tag}: it rises in and its clip ({clip}) starts ~0.45 s later (the reference's SENT_IN_MS)", gap is not None and 400 <= gap <= 800, f"{gap:.0f} ms" if gap is not None else None)
    timed = [s for s in samples if s["clip"] == clip and s["playing"] and s["t"] is not None]
    off = [s for s in timed if s["hot"][k] not in (lit_want(times, wend, s["t"]), lit_want(times, wend, s["t"] - 0.05))]
    seen = {tuple(s["hot"][k]) for s in timed if s["hot"][k]}
    check(f"{tag}: each word lit as the clip reaches it, one at a time, none after the last word's end", len(timed) > 20 and not off and len(seen) >= len(set(times)) - 1,
          f"{len(timed)} samples, {len(off)} off, {len(seen)} lit states / {len(set(times))} stretches")

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs, bad = [], []

    # ---- 1-2. timing at 1333x750
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    # the engine makes its AudioContext on the first sound (_ac); in the lesson the start tap has long made it, but a page mounted
    # on its own would make it on the first pop, and new AudioContext() holds that frame 30-60 ms: made here first
    pg.evaluate("_ac()"); pg.wait_for_timeout(300)
    pg.evaluate(NAVLOG); pg.evaluate(SOUNDS); pg.evaluate(TIMELINE, SAMPLE); pg.evaluate(GOTO, "T0B")
    d = pg.evaluate("CARD.slides[state.idx].data"); T = [ln["word_times"] for ln in d["lines"]]; CUES = d["explain_cues"]; MCUE = d["moral_cue"]
    check("the page's data: the frame's two sentences on vo_story_c1 / c2, the explanation vo_story_r1 with its two cues, the moral vo_story_moral with its cue",
          [ln["text_hi"] for ln in d["lines"]] == LINES and [ln["audio"] for ln in d["lines"]] == ["vo_story_c1", "vo_story_c2"] and d["explain_audio"] == "vo_story_r1"
          and len(CUES) == 2 and 0 < CUES[0] < CUES[1] and d["moral_audio"] == "vo_story_moral" and MCUE > 0, (CUES, MCUE))
    pg.wait_for_function("isPlaying && currentAudio && currentAudio.src.includes('vo_story_r0.') && currentAudio.currentTime > 0.7", timeout=10000, polling=20)
    pg.screenshot(path=str(out / "a_intro_1333.png"))   # [t0b-fig] the intro line sounding over the card alone (no title)
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
    i_end0 = end_of("r0", i_play); i_box = first(lambda s: s["box"])
    i_c1 = start_of("c1"); i_c1e = end_of("c1", i_c1); i_c2 = start_of("c2", i_c1e); i_c2e = end_of("c2", i_c2)
    i_r1 = start_of("r1", i_c2e); i_r1e = end_of("r1", i_r1); i_m = start_of("moral", i_r1e); i_me = end_of("moral", i_m)
    check("no title at any moment (frame 704:2 has none, [t0b-fig]); the intro line is the first clip, sounding over the card alone",
          not d.get("title_hi") and all(s["title"] == "" for s in samples) and next(s["clip"] for s in samples if s["clip"]) == "r0"
          and not any(s["box"] or any(s["shown"]) for s in samples[:i_play + 1]), (d.get("title_hi"), {s["title"] for s in samples}))
    check("the sentence box stays away while the intro line sounds", not any(s["box"] for s in samples[:i_end0]))
    check("the box comes in as the intro line ends", 0 <= ms(i_box) - ms(i_end0) <= 150, f"{ms(i_box) - ms(i_end0):.0f} ms after")
    i_s1 = first(lambda s: s["shown"][0] > 0)
    check("sentence 1 rises in once the box has landed (~0.65 s), its clip ~0.45 s after that ([word-sync])", 600 <= ms(i_s1) - ms(i_box) <= 1000 and 1050 <= ms(i_c1) - ms(i_box) <= 1500,
          f"sentence {ms(i_s1) - ms(i_box):.0f} ms, clip {ms(i_c1) - ms(i_box):.0f} ms after the box")
    starts = lambda clip: sum(1 for i, s in enumerate(samples) if s["clip"] == clip and s["playing"]
                              and (i == 0 or not (samples[i - 1]["clip"] == clip and samples[i - 1]["playing"])))
    check("🔊 taps during the intro / the box landing were ignored (each clip plays once: intro, the two sentences, the explanation, the moral)",
          tapped_intro and tapped_land and all(starts(c) == 1 for c in ("r0", "c1", "c2", "r1", "moral")), f"taps made: {taps}, starts {[starts(c) for c in ('r0', 'c1', 'c2', 'r1', 'moral')]}")
    check("no sentence word shows before sentence 1 rises in", all(s["shown"] == [0, 0] for s in samples[:i_s1]))
    WE = [ln.get("word_end") for ln in d["lines"]]
    sync_checks("sentence 1", samples, 0, "c1", T[0], WE[0]); sync_checks("sentence 2", samples, 1, "c2", T[1], WE[1])
    i_s2 = first(lambda s: s["shown"][1] > 0, i_c1e)
    check("sentence 2 rises in ~0.6 s after sentence 1's clip has ended and its clip follows ~0.45 s later, sentence 1 standing, no sentence-2 word before its rise ([word-sync])",
          500 <= ms(i_s2) - ms(i_c1e) <= 950 and 950 <= ms(i_c2) - ms(i_c1e) <= 1450 and all(s["shown"][1] == 0 for s in samples[:i_s2]) and samples[i_c2]["shown"][0] == len(T[0]),
          f"sentence {ms(i_s2) - ms(i_c1e):.0f} ms, clip {ms(i_c2) - ms(i_c1e):.0f} ms after")
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
    # [relisten-sfx] T1's sounds: a pop as each sentence rises in, nothing else
    snd = [e for e in pg.evaluate("window._snd") if samples[0]["ms"] - 50 <= e["ms"] <= ms(i_me) + 500]
    pops = [e for e in snd if e["kind"] == "tone" and e["f"] == "720" and e["ty"] == "sine" and e["d"] == 0.1 and e["v"] == 0.07]
    others = [e for e in snd if e not in pops and not (e["kind"] == "media" and e["src"].startswith("vo_"))]
    check("[relisten-sfx] the soft pop (T1's = the reference's sfxPopSoft: _tone 720 Hz sine, 0.10 s, 0.07) as sentence 1 rises in and as sentence 2 rises in — twice, each within 50 ms of its frame",
          len(pops) == 2 and abs(pops[0]["ms"] - ms(i_s1)) <= 50 and abs(pops[1]["ms"] - ms(i_s2)) <= 50,
          [round(e["ms"] - ms(i)) for e, i in zip(pops, (i_s1, i_s2))] + [len(pops)])
    check("[relisten-sfx] no other sound effect during the page (the box, the sentences' highlights and the commas make none; only the voice clips besides)", not others, others[:4])
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
    t_rep = pg.evaluate("performance.now()")
    pg.click(".tut-audio", force=True); pg.wait_for_timeout(400)
    r = pg.evaluate(SAMPLE)
    check("🔊 afterwards replays the reading from sentence 1 (box and both sentences staying, sentence 1 lit word by word again, the highlights cleared) ([word-sync])",
          r["clip"] == "c1" and r["playing"] and r["shown"] == [len(T[0]), len(T[1])] and r["hot"][0] in (lit_want(T[0], WE[0], r["t"]), lit_want(T[0], WE[0], r["t"] - 0.05))
          and r["hl"] == -1 and r["mk"] == 0 and r["box"], r)
    check("आगे is hidden while the replay sounds", not r["navVisible"])
    pg.wait_for_function("document.querySelectorAll('.sfig-mk.on').length === 2", timeout=40000, polling=20)
    pg.wait_for_function("!isPlaying && document.getElementById('navBtn').classList.contains('active')", timeout=30000)
    pg.wait_for_timeout(300)
    check("...the replay runs the whole reading again (the commas lit once more) and आगे comes back live, breathing", pg.evaluate(PULSING) == "navBreathe")
    rep_snd = [e for e in pg.evaluate("window._snd") if e["ms"] >= t_rep and not (e["kind"] == "media" and e["src"].startswith("vo_"))]
    check("[relisten-sfx] the replay makes no pop (nothing appears again)", not rep_snd, rep_snd[:4])
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
    boxes = pg.evaluate(BOXES, list(FRAME) + list(NODES)); worst = 0
    print("== box / sentences vs the frame (px) ==")
    for sel, exp in FRAME.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, dd)
        print(f"  {sel:18s} got {[round(v,2) for v in got]}  frame {list(exp)}  max|d|={dd:.2f}")
    for sel, (cx, cy) in NODES.items():
        g = boxes[sel]; gc = (g[0] + g[2] / 2, g[1] + g[3] / 2); dd = max(abs(gc[0] - cx), abs(gc[1] - cy)); worst = max(worst, dd)
        print(f"  {sel:18s} centre {[round(v,2) for v in gc]} width {round(g[2],2)}  frame ({cx}, {cy})  max|d|={dd:.2f}")
    check("sentence box and the two sentence nodes' centres within 1 px of the frame (704:183 / 704:184 / 704:185)", worst <= 1.0, f"worst {worst:.2f}px")
    check("no title is drawn (frame 704:2 has none)", pg.evaluate("(document.querySelector('.sfig-title p') || {}).textContent || ''") == "")
    lines = pg.evaluate("""() => [...document.querySelectorAll('.sfig-stext p')].map(p => { const ws = [...p.querySelectorAll('.sfig-w')];
      const tops = [...new Set(ws.map(w => Math.round(w.getBoundingClientRect().top)))];
      return tops.map(t => ws.filter(w => Math.round(w.getBoundingClientRect().top) === t).map(w => w.textContent).join(' ')); })""")
    print("  text lines:", lines)
    check("each sentence is the frame's, on one line", lines == [[l] for l in LINES])
    # [t0b-fig] the type is page 1 T0's (.sfig-text: Baloo 2 declared 600 -> the embedded 700 face, #002F76) at the frame's 50px
    t0 = pg.evaluate("""() => { const c = getComputedStyle(document.querySelector('.sfig-stext p.l1')), d = getComputedStyle(document.querySelector('.sfig-stext p.l2'));
      return [c.fontFamily, c.fontWeight, c.fontSize, c.lineHeight, c.color, d.fontFamily + d.fontWeight + d.fontSize + d.color,
              document.fonts.check("600 50px 'Baloo 2'", 'उसे रोको') && document.fonts.check("700 50px 'Baloo 2'", 'उसे रोको')]; }""")
    check("type: page 1 T0's (Baloo 2 declared 600, #002F76) at the frame's 50px, line-height normal, both sentences", t0[0].startswith('"Baloo 2"') and t0[1] == "600"
          and t0[2] == "50px" and t0[3] == "normal" and t0[4] == "rgb(0, 47, 118)" and t0[5] == t0[0] + "600" + "50px" + "rgb(0, 47, 118)" and t0[6], t0)
    A = np.asarray(Image.open(shot).convert("RGB"), np.int16); B = np.asarray(target, np.int16)
    def ink(X, y0, y1, x0=380, x1=900):   # the box of pixels at least 15 % of the way from white to the navy
        sub = X[y0:y1, x0:x1].astype(int); m = np.clip((765 - sub.sum(axis=2)) / (765 - 165), 0, 1) >= 0.15
        ys, xs = np.nonzero(m); return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1)
    for k, (y0, y1) in enumerate(INK_BANDS, 1):
        a, f = ink(A, y0, y1), ink(B, y0, y1)
        dc = ((a[0] + a[2]) / 2 - (f[0] + f[2]) / 2, (a[1] + a[3]) / 2 - (f[1] + f[3]) / 2)
        print(f"  sentence {k} ink: page {[int(v) for v in a]} ({a[2]-a[0]}x{a[3]-a[1]})  render {[int(v) for v in f]} ({f[2]-f[0]}x{f[3]-f[1]})  centre d {dc[0]:+.1f},{dc[1]:+.1f}")
        check(f"sentence {k}'s ink sits where the render's does (centres within 1.5 px; the same height, within 3 % of its width — T0's bolder face)",
              abs(dc[0]) <= 1.5 and abs(dc[1]) <= 1.5 and abs((a[3] - a[1]) - (f[3] - f[1])) <= 2 and abs((a[2] - a[0]) / (f[2] - f[0]) - 1) <= 0.03, dc)
    pad = np.pad(B, ((1, 1), (1, 1), (0, 0)), mode="edge")
    full = np.min([np.abs(A - pad[1+dy:1+dy+A.shape[0], 1+dx:1+dx+A.shape[1]]).max(axis=2)
                   for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
    near = full.copy()
    for x0, y0, x1, y1 in TYPE_T0: near[y0:y1, x0:x1] = 0
    x0, y0, x1, y1 = CONTENT; near = near[y0:y1, x0:x1]
    big = int((near > 32).sum()); px = near.size
    print(f"  pixel diff vs Figma render over the box, less the sentences' ink (within 1 px): {big} of {px} px differ by >32 levels ({100*big/px:.2f}%)")
    Image.fromarray(np.where(near > 32, 255, 0).astype(np.uint8)).save(out / "f_diff_mask.png")
    # anti-aliasing of the box edge is what remains; a misplaced or mis-sized box shows as whole shapes
    check("the box pixel-matches the Figma render (within 1 px: >32-level diffs under 1% of the area)", big / px < 0.01)
    keep = np.zeros(full.shape, bool); x0, y0, x1, y1 = WHOLE; keep[y0:y1, x0:x1] = True
    for x0, y0, x1, y1 in OWN_T0 + TYPE_T0: keep[y0:y1, x0:x1] = False
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
sys.exit(1 if fails else 0)
