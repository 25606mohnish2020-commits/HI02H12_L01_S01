"""Verify T2, the hallway scene (PUNCT_SCENE, [t2-scene] 2026-11-01, FLN-by-MJ frame 706:188 "2 T0B"), against its frame and its timing.
usage: python -I -X utf8 scene_check.py <index.html> <demo1b_figma_render_1280x720.png> <outdir>
1. At 1333x750, the page mounted on its own (the engine's AudioContext warmed first, as the start tap would have): the intro line
   (vo_demo1_intro) is the first clip and sounds over the hallway picture alone — the picture, the standing Swiftie and the 🔊 chip
   there from the first frame; no sentence word, no slot, no girl, no tile before it has ended; 0.5 s after it the slot pops in and
   the sentence rises in whole in the same frame, with T1's text pop (the reference's sfxPopSoft: _tone 720 sine 0.10 / 0.07) in that
   frame; the sentence's clip 0.45 s after the rise, each word lit as it is read ([word-sync]); 0.3 s after the clip the girl
   appears at the doorway and walks for data.walk_ms — opacity up from 0, her translate and scale rising monotonically from
   (-158,-159) x .6 to her place at 1 — with the school sound (sfx_demo1_school.mp3 at .5) starting in her first frame, fading over
   her last 0.7 s and paused as she arrives; 0.3 s after she has arrived the slot blinks (data.blink_ms: its ring and glow reach the
   words' orange three times) and as the blink starts the three tiles pop in (90 ms apart) with the pop (sfx_demo1_pop.mp3) in the
   first tile's frame; 0.3 s after the blink the explanation (vo_demo1_explain) — the danda's tile lights (.lit) as the clip reaches
   its cue word, not before; 0.3 s after the clip the other two tiles are dim and dead (.off); 0.3 s later the lit tile pulses
   (dscPulse, infinite) and is live. Taps: the 🔊 chip during the intro is ignored (every clip plays once), the danda's tile before it
   is live is ignored, the chip once it is live reads the sentence again (words lit, the tile still pulsing), the tap on the pulsing
   tile: green at once (.done), the kit's correct sound (sfx_correct_new.ogg at .85) in that frame, the mark in the slot (its ink
   centred), the slot's box gone 0.45 s later, T3 mounted ~1.2 s after that, no gate. Only those sounds (the pop, the school, the
   pop, the correct) besides the voice clips; आगे never shows.
2. The card, Swiftie, the 🔊 chip = page 3 T1's (stage px: the card 96,106 1088x508 x 1333/1280 with 64px corners; Swiftie 76,472
   190; the chip 202,606 58).
3. 1280x720 (= frame px), the tiles landed and the blink frozen: every box vs the frame's nodes (the picture 0,-113 1088x613 of the
   card; the slot 1013,187 53x90; the girl 264,215 239x358, her shadow 307,520 160x36; the tiles 564.09 / 791 / 1021.818, 397
   117.819x116.498, their faces and shadows); the sentence's and the three marks' ink vs the Figma render (centres within 1.5 px, sizes
   within 2 px: the marks are the frame's own Noto face, 'Story Noto Marks'); the type; the slot's white interior; per-pixel diffs vs
   the render over the card less Swiftie / chip (T1's, not the frame's), the slot (its dashes' phase is not the render's) and the
   text ink bands; the girl's region compared on its own (the same bitmap, resampled).
"""
import sys, re, json, pathlib
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
AS_T0 = {".tut-card.sfig-card": (96 * FS, 106 * FS, 1088 * FS, 508 * FS), ".sfig-swiftie": (76, 472, 190, 190), ".tut-audio": (202, 606, 58, 58)}
CX, CY = 96, 106
FRAME = {".dsc-bg > img": (CX + 0, CY - 113, 1088, 613), ".dsc-slot": (1013, 187, 53, 90), ".dsc-girl": (264, 215, 239, 358), ".dsc-shade": (307, 520, 160, 36),
         ".dsc-tile.t1": (564.09, 397, 117.819, 116.498), ".dsc-tile.t2": (791, 397, 117.819, 116.498), ".dsc-tile.t3": (1021.818, 397, 117.819, 116.498),
         ".t1 .dsc-face": (565.13, 398.38, 115.743, 110.983), ".t1 .dsc-tshade": (563, 496, 118, 26), ".t3 .dsc-tshade": (1021.818, 496.498, 118, 26)}
INK = {"sentence": (560, 180, 1010, 290), "mark1": (574, 405, 672, 505), "mark2": (801, 405, 899, 505), "mark3": (1032, 405, 1130, 505)}
WHOLE = (80, 90, 1200, 640)
OWN_T0 = [(25, 400, 290, 720)]                                   # Swiftie + the chip (T1's, not the frame's)
BY_DESIGN = [(1008, 182, 1071, 282), (570, 186, 1015, 268), (600, 420, 645, 480), (830, 440, 870, 470), (1055, 418, 1105, 478)]   # the slot, the ink bands
GIRL = (264, 215, 503, 573)
GOTO = """(id) => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); mountSlide(CARD.slides.findIndex(s => s.id === id)); }"""
BOXES = """(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
  if (!e) { o[s] = null; continue; } const r = e.getBoundingClientRect(); o[s] = [r.left, r.top, r.width, r.height]; } return o; }"""
NAVLOG = """() => { window._navLog = []; const btn = document.getElementById('navBtn'); let last = ''; const t0 = performance.now();
  const step = () => { const cs = getComputedStyle(btn); const shown = cs.visibility === 'visible' && parseFloat(cs.opacity) > 0.01 && cs.display !== 'none';
    const key = [shown, CARD.slides[state.idx] ? CARD.slides[state.idx].id : null].join('|');
    if (key !== last) { last = key; window._navLog.push({ ms: performance.now() - t0, shown, slide: CARD.slides[state.idx] ? CARD.slides[state.idx].id : null }); }
    requestAnimationFrame(step); }; requestAnimationFrame(step); }"""
SOUNDS = """() => { window._snd = []; const T = window._tone;
  window._tone = function(f, ty, d, v){ window._snd.push({ ms: performance.now(), kind: 'tone', f: f.join('/'), ty, d, v }); return T.apply(this, arguments); };
  const P = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function(){ window._snd.push({ ms: performance.now(), kind: 'media', src: decodeURIComponent(String(this.currentSrc || this.src).split('/').pop()), vol: +this.volume.toFixed(3) });
    return P.apply(this, arguments); }; }"""
# one frame of the page
SAMPLE = r"""() => { const a = currentAudio, src = a ? a.src.split('/').pop() : '', m = src.match(/vo_demo1_(\w+)\.ogg/), q = (s) => document.querySelector(s), qa = (s) => document.querySelectorAll(s);
  const g = q('.dsc-girl'), gc = g ? getComputedStyle(g) : null, slot = q('.dsc-slot'), ring = q('.dsc-dash rect'), lit = [...qa('.dsc-tile')].findIndex(t => t.classList.contains('lit'));
  const walk = _kitSfx.sceneWalk;
  return { ms: performance.now(), slide: CARD.slides[state.idx] ? CARD.slides[state.idx].id : null, clip: m ? m[1] : null, t: a ? a.currentTime : null, playing: isPlaying,
    ready: !!q('.dsc-bg'), bgLoaded: !!q('.dsc-bg > img') && q('.dsc-bg > img').complete && q('.dsc-bg > img').naturalWidth > 0,
    shown: qa('.dsc-sent .sfig-w.on').length, hot: [...qa('.dsc-sent .sfig-w')].map((w, i) => w.classList.contains('hot') ? i : -1).filter(i => i >= 0), rise: !!q('.dsc-sent.sfig-rise'),
    slotIn: !!slot && slot.classList.contains('in'), blink: !!slot && slot.classList.contains('blink'), glow: slot ? getComputedStyle(slot).boxShadow : null, ringStroke: ring ? getComputedStyle(ring).stroke : null,
    gone: !!slot && slot.classList.contains('gone'), markIn: !!q('.dsc-mark.in'),
    walk: !!g && g.classList.contains('walk'), here: !!g && g.classList.contains('here'), gOp: gc ? +(+gc.opacity).toFixed(3) : null, gTr: gc ? gc.translate : null, gSc: gc ? gc.scale : null,
    walkVol: walk ? +walk.volume.toFixed(3) : null, walkPaused: walk ? walk.paused : null,
    tilesIn: qa('.dsc-tile.in').length, lit, off: qa('.dsc-tile.off').length, pulse: !!q('.dsc-tile.pulse'), live: !!q('.dsc-tile.live'), done: !!q('.dsc-tile.done'),
    nav: getComputedStyle(document.getElementById('navBtn')).display }; }"""
# the timeline sampled in the page every frame; the taps made in the page at their moments: the chip 1 s into the intro (ignored),
# the danda's tile 0.5 s into the explanation (ignored), the chip 0.3 s after the tile is live (the sentence again), the tile 0.3 s
# after that reading has ended
TIMELINE = "(sample) => { window._tl = []; window._taps = []; const S = eval(sample); let liveAt = 0, rereadSeen = false, rereadEnded = 0;" \
    " const step = () => { const s = S(); window._tl.push(s); const chip = document.querySelector('.tut-audio'), tile = document.querySelector('.dsc-tile.t1');" \
    " if (chip && !window._taps.includes('intro') && s.clip === 'intro' && s.playing && s.t > 1) { window._taps.push('intro'); chip.click(); }" \
    " if (tile && !window._taps.includes('early') && s.clip === 'explain' && s.playing && s.t > 0.5) { window._taps.push('early'); tile.click(); }" \
    " if (s.live && !liveAt) liveAt = s.ms;" \
    " if (chip && liveAt && !window._taps.includes('chip') && s.ms - liveAt > 300) { window._taps.push('chip'); chip.click(); }" \
    " if (window._taps.includes('chip') && s.clip === 'sent' && s.playing) rereadSeen = true;" \
    " if (rereadSeen && !rereadEnded && !(s.clip === 'sent' && s.playing)) rereadEnded = s.ms;" \
    " if (tile && rereadEnded && !window._taps.includes('tap') && s.ms - rereadEnded > 300) { window._taps.push('tap'); tile.click(); }" \
    " if (s.slide !== 'T3' && (s.ms - (window._t0 || (window._t0 = s.ms))) < 120000) requestAnimationFrame(step); }; requestAnimationFrame(step); }"   # runs until T3 (the first frame may come before T2 has mounted)

def lit_want(times, wend, t):
    if t is None or (wend is not None and t >= wend): return []
    st = None
    for x in times:
        if t >= x: st = x
    return [i for i, x in enumerate(times) if st is not None and x == st]
def ink(img, region):
    A = np.asarray(img, int); x0, y0, x1, y1 = region; sub = A[y0:y1, x0:x1]
    m = (sub[..., 2] > sub[..., 0] + 40) & (sub.sum(axis=2) < 450); ys, xs = np.nonzero(m)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1) if len(xs) else None

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs, bad = [], []

    # ---- 1-2. timing at 1333x750
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate("_ac()"); pg.wait_for_timeout(300)   # the engine's AudioContext, as the start tap would have made it
    pg.evaluate(NAVLOG); pg.evaluate(SOUNDS); pg.evaluate(TIMELINE, SAMPLE); pg.evaluate(GOTO, "T2")
    d = pg.evaluate("CARD.slides[state.idx].data"); ST = d["sentence"]["word_times"]; SE = d["sentence"].get("word_end"); XT = d["explain"]["word_times"]; CUE = XT[d["explain"]["cue_word"]]
    check("the page's data: PUNCT_SCENE with the intro line, the hallway and the walking girl, the sentence (its clip and word times), the explanation with its cue word \"पूर्णविराम\", the three marks, the danda, the walk / blink / sounds",
          pg.evaluate("CARD.slides[state.idx].type") == "PUNCT_SCENE" and d["intro_audio"] == "vo_demo1_intro" and d["bg_id"] == "img_demo1_hall" and d["image_id"] == "img_demo1_girl_walk"
          and d["sentence"]["text_hi"] == "पिंकी स्कूल जा रही है" and d["sentence"]["audio"] == "vo_demo1_sent" and len(ST) == 5 and d["explain"]["audio"] == "vo_demo1_explain"
          and d["explain"]["text_hi"].split()[d["explain"]["cue_word"]] == "पूर्णविराम" and [o["mark"] for o in d["options"]] == ["।", ",", "?"] and d["mark"] == "।"
          and d["walk_ms"] == 3400 and d["walk_sfx"] == "sfx_demo1_school.mp3" and d["blink_ms"] == 2000 and d["tiles_sfx"] == "sfx_demo1_pop.mp3", {k: d.get(k) for k in ("bg_id", "image_id", "mark", "walk_ms", "blink_ms")})
    pg.wait_for_function("isPlaying && currentAudio && currentAudio.src.includes('vo_demo1_intro.') && currentAudio.currentTime > 0.7", timeout=10000, polling=20)
    pg.screenshot(path=str(out / "a_intro_1333.png"))
    pg.wait_for_function("!!document.querySelector('.dsc-girl.walk')", timeout=30000, polling=20); pg.wait_for_timeout(1500); pg.screenshot(path=str(out / "b_walk_1333.png"))
    pg.wait_for_function("!!document.querySelector('.dsc-tile.t3.in')", timeout=30000, polling=20); pg.wait_for_timeout(600); pg.screenshot(path=str(out / "c_tiles_1333.png"))
    pg.wait_for_function("!!document.querySelector('.dsc-tile.lit')", timeout=30000, polling=20); pg.wait_for_timeout(250); pg.screenshot(path=str(out / "d_lit_1333.png"))
    pg.wait_for_function("!!document.querySelector('.dsc-tile.pulse')", timeout=30000, polling=20); pg.wait_for_timeout(500); pg.screenshot(path=str(out / "e_pulse_1333.png"))
    look = pg.evaluate("""() => { const t = document.querySelector('.dsc-tile.t1'), f = t.querySelector('.dsc-face'), s = t.querySelector('.dsc-sym'); return [getComputedStyle(t).animationName, getComputedStyle(t).animationIterationCount, getComputedStyle(f).animationName, getComputedStyle(s).color]; }""")
    try: pg.wait_for_function("!!document.querySelector('.dsc-tile.done')", timeout=40000, polling=20)
    except Exception:
        print("DIAG taps", pg.evaluate("window._taps"), "samples", pg.evaluate("window._tl.length"), "last", pg.evaluate("window._tl[window._tl.length - 1]"), "errors", errs[:3]); raise
    pg.wait_for_timeout(500); pg.screenshot(path=str(out / "f_done_1333.png"))
    pg.wait_for_function("CARD.slides[state.idx].id === 'T3'", timeout=10000)
    samples, taps, snd = pg.evaluate("window._tl"), pg.evaluate("window._taps"), pg.evaluate("window._snd")
    samples = [s for s in samples if s["ready"] and s["slide"] == "T2"]
    with open(out / "timeline.json", "w", encoding="utf-8") as f: json.dump(samples, f, indent=0)
    ms = lambda i: samples[i]["ms"]
    first = lambda cond, start=0: next(i for i in range(start, len(samples)) if cond(samples[i]))
    start_of = lambda c, i0=0: first(lambda s: s["clip"] == c and s["playing"] and (s["t"] or 0) > 0, i0)
    end_of = lambda c, i0: first(lambda s: s["clip"] != c or not s["playing"], i0 + 1)
    i_in = start_of("intro"); i_ine = end_of("intro", i_in)
    check("the intro line is the first clip; the picture (loaded), the standing Swiftie and the 🔊 chip are there from the first frame; nothing else shows before the line has ended",
          next(s["clip"] for s in samples if s["clip"]) == "intro" and all(s["bgLoaded"] for s in samples[:i_ine])
          and not any(s["shown"] or s["slotIn"] or s["walk"] or s["here"] or s["tilesIn"] for s in samples[:i_ine])
          and pg.evaluate("(() => { const sw = document.querySelector('.sfig-swiftie'); return !!sw; })()"), (round(ms(i_ine) - ms(i_in)), ))
    i_slot = first(lambda s: s["slotIn"]); i_rise = first(lambda s: s["shown"] > 0)
    check("0.5 s after the intro the slot pops in and the sentence rises in WHOLE in the same frame", 350 <= ms(i_slot) - ms(i_ine) <= 800 and abs(ms(i_rise) - ms(i_slot)) <= 34
          and {s["shown"] for s in samples} <= {0, len(ST)} and samples[i_rise]["rise"], (round(ms(i_slot) - ms(i_ine)), round(ms(i_rise) - ms(i_slot))))
    i_sent = start_of("sent", i_rise); i_sente = end_of("sent", i_sent)
    check("the sentence's clip starts ~0.45 s after the rise ([word-sync])", 380 <= ms(i_sent) - ms(i_rise) <= 800, round(ms(i_sent) - ms(i_rise)))
    timed = [s for s in samples[i_sent:i_sente] if s["clip"] == "sent" and s["playing"] and s["t"] is not None]
    off = [s for s in timed if s["hot"] not in (lit_want(ST, SE, s["t"]), lit_want(ST, SE, s["t"] - 0.05))]
    check("each word lit as the clip reaches it, one at a time, none after the last word's end", len(timed) > 20 and not off and len({tuple(s["hot"]) for s in timed if s["hot"]}) >= len(set(ST)) - 1,
          f"{len(timed)} samples, {len(off)} off")
    i_walk = first(lambda s: s["walk"]); i_walke = first(lambda s: not s["walk"], i_walk); i_here = first(lambda s: s["here"], i_walk)
    check("0.3 s after the sentence's clip the girl's walk begins and lasts walk_ms, her place held (.here) from its end", 200 <= ms(i_walk) - ms(i_sente) <= 650 and abs(ms(i_walke) - ms(i_walk) - d["walk_ms"]) <= 120
          and abs(ms(i_here) - ms(i_walke)) <= 34, (round(ms(i_walk) - ms(i_sente)), round(ms(i_walke) - ms(i_walk))))
    def tr(s):
        m_ = re.findall(r"-?[\d.]+", s["gTr"] or "0 0"); x = float(m_[0]) if m_ else 0.0; y = float(m_[1]) if len(m_) > 1 else 0.0
        sc = float(re.findall(r"-?[\d.]+", s["gSc"] or "1")[0]) if s["gSc"] not in (None, "none") else 1.0
        return x, y, sc
    walk = [tr(s) + (s["gOp"],) for s in samples[i_walk:i_walke]]
    mono = all(walk[k + 1][0] >= walk[k][0] - 0.01 and walk[k + 1][1] >= walk[k][1] - 0.01 and walk[k + 1][2] >= walk[k][2] - 0.001 for k in range(len(walk) - 1))
    check("she comes in from the doorway: opacity up from 0, from (-158,-159) at .6 to her place at 1, every frame further right, lower and larger than the last",
          walk and walk[0][3] < .5 and walk[0][0] <= -150 and walk[0][1] <= -150 and walk[0][2] <= .62 and mono and samples[i_walke]["gOp"] == 1
          and abs(walk[-1][0]) <= 3 and abs(walk[-1][1]) <= 3 and walk[-1][2] >= .99, (walk[0], walk[len(walk) // 2], walk[-1]))
    school = [e for e in snd if e["kind"] == "media" and e["src"] == "sfx_demo1_school.mp3"]
    fade = [s for s in samples[i_walk:i_walke + 10] if s["walkVol"] is not None]
    vol_mid = next((s["walkVol"] for s in fade if s["ms"] - ms(i_walk) > 1000), None); vol_end = next((s["walkVol"] for s in fade if s["ms"] - ms(i_walk) > d["walk_ms"] - 150), None)
    paused_after = next((s["walkPaused"] for s in samples[i_walke:] if s["ms"] - ms(i_walke) > 120), None)
    check("the school sound (sfx_demo1_school.mp3 at .5) starts in her first frame, is faded over her last 0.7 s and paused as she arrives",
          len(school) == 1 and abs(school[0]["ms"] - ms(i_walk)) <= 50 and school[0]["vol"] == 0.5 and vol_mid == 0.5 and vol_end is not None and vol_end < 0.15 and paused_after is True,
          [(round(e["ms"] - ms(i_walk)), e["vol"]) for e in school] + [vol_mid, vol_end, paused_after])
    i_bl = first(lambda s: s["blink"], i_walke); i_ble = first(lambda s: not s["blink"], i_bl)
    # the ring's colour animates grey -> orange -> grey: a "peak" = a run of frames near the orange (r >= 200, b <= 60); three expected
    def orange(s_):
        m_ = re.findall(r"\d+", s_["ringStroke"] or ""); return len(m_) >= 3 and int(m_[0]) >= 200 and int(m_[2]) <= 60
    peaks = sum(1 for k in range(i_bl + 1, i_ble) if orange(samples[k]) and not orange(samples[k - 1]))
    glow = any(s["glow"] not in (None, "none") and "232, 106, 0" in s["glow"] for s in samples[i_bl:i_ble])
    check("0.3 s after she has arrived the slot blinks for blink_ms: its ring reaches the words' orange three times with the glow, plain again after",
          200 <= ms(i_bl) - ms(i_here) <= 650 and abs(ms(i_ble) - ms(i_bl) - d["blink_ms"]) <= 120 and peaks == 3 and glow
          and samples[i_ble + 3]["glow"] == "none" and "232, 106, 0" not in (samples[i_ble + 3]["ringStroke"] or ""), (round(ms(i_bl) - ms(i_here)), round(ms(i_ble) - ms(i_bl)), peaks))
    i_t1 = first(lambda s: s["tilesIn"] >= 1); i_t3 = first(lambda s: s["tilesIn"] >= 3)
    pop = [e for e in snd if e["kind"] == "media" and e["src"] == "sfx_demo1_pop.mp3"]
    check("the three tiles pop in as the blink starts (90 ms apart) with the pop (sfx_demo1_pop.mp3) in the first tile's frame",
          abs(ms(i_t1) - ms(i_bl)) <= 50 and 120 <= ms(i_t3) - ms(i_t1) <= 300 and len(pop) == 1 and abs(pop[0]["ms"] - ms(i_t1)) <= 50 and pop[0]["vol"] == 0.8,
          (round(ms(i_t1) - ms(i_bl)), round(ms(i_t3) - ms(i_t1)), [(round(e["ms"] - ms(i_t1)), e["vol"]) for e in pop]))
    i_x = start_of("explain", i_ble); i_xe = end_of("explain", i_x); i_lit = first(lambda s: s["lit"] >= 0)
    check(f"0.3 s after the blink the explanation sounds; the danda's tile lights as it reaches \"पूर्णविराम\" ({CUE} s on its clock, within -0.05/+0.15 s), none before",
          200 <= ms(i_x) - ms(i_ble) <= 650 and i_x <= i_lit < i_xe and samples[i_lit]["lit"] == 0 and -0.05 <= samples[i_lit]["t"] - CUE <= 0.15 and not any(s["lit"] >= 0 for s in samples[:i_lit]),
          (round(ms(i_x) - ms(i_ble)), round(samples[i_lit]["t"] - CUE, 2) if i_lit > i_x else None))
    i_off = first(lambda s: s["off"] == 2, i_x); i_pulse = first(lambda s: s["pulse"], i_off); i_live = first(lambda s: s["live"], i_off)
    check("0.3 s after the clip the other two tiles are dim and dead; 0.3 s later the lit tile pulses and is live; the lit tile never dims",
          200 <= ms(i_off) - ms(i_xe) <= 650 and 200 <= ms(i_pulse) - ms(i_off) <= 650 and abs(ms(i_live) - ms(i_pulse)) <= 34 and all(s["off"] <= 2 for s in samples) and all(s["lit"] == 0 for s in samples[i_lit:]),
          (round(ms(i_off) - ms(i_xe)), round(ms(i_pulse) - ms(i_off))))
    starts = lambda c: sum(1 for i, s in enumerate(samples) if s["clip"] == c and s["playing"] and (i == 0 or not (samples[i - 1]["clip"] == c and samples[i - 1]["playing"])))
    check("🔊 during the intro and the tile before it is live were ignored (the intro, the explanation once each; no .done before the live tile)",
          "intro" in taps and "early" in taps and starts("intro") == 1 and starts("explain") == 1 and not any(s["done"] for s in samples[:i_live]), (taps, starts("intro"), starts("explain")))
    i_rr = start_of("sent", i_live); i_rre = end_of("sent", i_rr)
    rr = [s for s in samples[i_rr:i_rre] if s["clip"] == "sent" and s["playing"] and s["t"] is not None]
    off2 = [s for s in rr if s["hot"] not in (lit_want(ST, SE, s["t"]), lit_want(ST, SE, s["t"] - 0.05))]
    check("🔊 once the tile is live reads the sentence again, each word lit, the tile still pulsing and nothing else changing",
          "chip" in taps and i_rr > i_live and len(rr) > 20 and not off2 and all(s["pulse"] and s["live"] and s["off"] == 2 and not s["done"] and s["tilesIn"] == 3 for s in rr), f"{len(rr)} samples, {len(off2)} off")
    i_done = first(lambda s: s["done"], i_rre); i_mark = first(lambda s: s["markIn"], i_live); i_gone = first(lambda s: s["gone"], i_done)
    corr = [e for e in snd if e["kind"] == "media" and e["src"] == "sfx_correct_new.ogg"]
    check("the tap: green at once with the kit's correct sound (sfx_correct_new.ogg at .85) in that frame, the mark in the slot in that frame, the pulse off, the slot's box gone 0.45 s later",
          "tap" in taps and abs(ms(i_mark) - ms(i_done)) <= 34 and len(corr) == 1 and abs(corr[0]["ms"] - ms(i_done)) <= 50 and corr[0]["vol"] == 0.85
          and not samples[i_done + 2]["pulse"] and not samples[i_done + 2]["live"] and 380 <= ms(i_gone) - ms(i_done) <= 650, (round(ms(i_mark) - ms(i_done)), [(round(e["ms"] - ms(i_done)), e["vol"]) for e in corr], round(ms(i_gone) - ms(i_done))))
    t_end = samples[-1]["ms"]
    check("T3 follows ~1.2 s after the box has gone, by itself (no आगे, no gate)", 1000 <= t_end - ms(i_gone) <= 1700 and pg.evaluate("CARD.slides[state.idx].id === 'T3' && !document.getElementById('phaseGate').classList.contains('show')")
          and all(s["nav"] == "none" for s in samples), round(t_end - ms(i_gone)))
    check("the pulse: dscPulse, infinite, on the whole tile, its face glowing (dscGlow), its mark the words' orange", look[0] == "dscPulse" and look[1] == "infinite" and look[2] == "dscGlow" and look[3] == "rgb(232, 106, 0)", look)
    pops = [e for e in snd if e["kind"] == "tone" and e["f"] == "720" and e["ty"] == "sine" and e["d"] == 0.1 and e["v"] == 0.07]
    others = [e for e in snd if samples[0]["ms"] - 50 <= e["ms"] <= t_end and e not in pops and e not in school and e not in pop and e not in corr and not (e["kind"] == "media" and e["src"].startswith("vo_"))]
    check("T1's text pop (the reference's sfxPopSoft) once, in the sentence's frame, and no other sound effect through the page", len(pops) == 1 and abs(pops[0]["ms"] - ms(i_rise)) <= 50 and not others,
          ([round(e["ms"] - ms(i_rise)) for e in pops], others[:4]))
    check("आगे never shows on this page", all(not e["shown"] for e in pg.evaluate("window._navLog") if e["slide"] == "T2"))
    pg.evaluate(GOTO, "T2"); pg.wait_for_timeout(1200)
    boxes = pg.evaluate(BOXES, list(AS_T0)); worst = 0
    print("== card / Swiftie / chip vs page 3 T1 (stage px) ==")
    for sel, exp in AS_T0.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, dd)
        print(f"  {sel:22s} got {[round(v,2) for v in got]}  want {[round(v,2) for v in exp]}  max|d|={dd:.2f}")
    check("the card, the standing Swiftie and the 🔊 chip are exactly page 3 T1's (within 0.5 px)", worst <= 0.5, f"worst {worst:.2f}px")
    radius = pg.evaluate("getComputedStyle(document.querySelector('.tut-card.sfig-card')).borderTopLeftRadius")
    check("the card has the frame's 64px corners (x 1333/1280)", abs(float(radius[:-2]) - 64 * FS) < 0.05, radius)
    pg.close()

    # ---- 3. geometry + pixel diff at 1280x720
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate("_ac()"); pg.evaluate(GOTO, "T2")
    pg.wait_for_function("!!document.querySelector('.dsc-tile.t3.in')", timeout=40000); pg.wait_for_timeout(650)
    pg.evaluate("document.querySelector('.dsc-slot').classList.remove('blink')"); pg.wait_for_timeout(350)   # the frame draws the slot plain
    shot = out / "g_frame_1280.png"; pg.screenshot(path=str(shot))
    boxes = pg.evaluate(BOXES, list(FRAME)); worst = 0
    print("== boxes vs the frame (px) ==")
    for sel, exp in FRAME.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, dd)
        print(f"  {sel:16s} got {[round(v,2) for v in got]}  frame {[round(v, 3) for v in exp]}  max|d|={dd:.2f}")
    check("the picture, the slot, the girl and her shadow, the tiles, their faces and shadows within 1 px of the frame's nodes", worst <= 1.0, f"worst {worst:.2f}px")
    st = pg.evaluate("""() => { const c = (s) => getComputedStyle(document.querySelector(s)); return [c('.dsc-bg').borderTopLeftRadius, c('.dsc-bg').overflow, c('.dsc-slot').borderRadius, c('.dsc-slot').backgroundColor,
      c('.dsc-dash').stroke, c('.dsc-dash').strokeWidth, c('.t1 .dsc-face').borderTopWidth, c('.t1 .dsc-face').borderTopColor, c('.t1 .dsc-face').borderRadius, c('.dsc-base').backgroundColor, c('.dsc-base').boxShadow]; }""")
    check("the picture clipped to the card's padding box with its inner corners; the slot white, 8px corners, a 2px rgba(86,86,86,.85) dashed ring; the tiles' faces 2.386px #D5D8DF, 18px corners, on a #D9D9D9 base with its 0 4 4 shadow",
          abs(float(st[0][:-2]) - (64 - 12 / FS)) < 0.05 and st[1] == "hidden" and st[2] == "8px" and st[3] == "rgb(255, 255, 255)" and st[4] == "rgba(86, 86, 86, 0.85)" and st[5] == "2px"
          and abs(float(st[6][:-2]) - 2.386) < 0.5 and st[7] == "rgb(213, 216, 223)" and st[8] == "18px" and st[9] == "rgb(217, 217, 217)" and st[10] == "rgba(0, 0, 0, 0.25) 0px 4px 4px 0px", st)
    fonts = pg.evaluate("""() => { const f = (s) => { const c = getComputedStyle(document.querySelector(s)); return [c.fontFamily.split(',')[0], c.fontWeight, c.fontSize, c.color]; };
      return [f('.dsc-sent'), f('.t1 .dsc-sym'), f('.dsc-mark'), document.fonts.check("600 64px 'Story Noto Marks'", '।,?') && document.fonts.check("800 55px 'Story Baloo 2'", 'पिंकी')]; }""")
    check("type: the sentence Baloo 2 800 at the frame's 55px #012F76; the tiles' marks in the frame's Noto Sans Devanagari SemiBold 64px #002F76 ('Story Noto Marks'); the landing mark the sentence's face; both faces loaded",
          fonts[0] == ['"Story Baloo 2"', "800", "55px", "rgb(1, 47, 118)"] and fonts[1] == ['"Story Noto Marks"', "600", "64px", "rgb(0, 47, 118)"] and fonts[2] == ['"Story Baloo 2"', "800", "55px", "rgb(1, 47, 118)"] and fonts[3], fonts)
    mine = Image.open(shot).convert("RGB")
    print("== text ink vs the Figma render (page px): centre and size ==")
    for name, region in INK.items():
        a, t = ink(mine, region), ink(target, region)
        if not a or not t: check(f"{name}: ink found on both", False, (a, t)); continue
        dc = ((a[0] + a[2]) / 2 - (t[0] + t[2]) / 2, (a[1] + a[3]) / 2 - (t[1] + t[3]) / 2); ds = ((a[2] - a[0]) - (t[2] - t[0]), (a[3] - a[1]) - (t[3] - t[1]))
        print(f"  {name:9s} page {[int(v) for v in a]} ({a[2]-a[0]}x{a[3]-a[1]})  render {[int(v) for v in t]} ({t[2]-t[0]}x{t[3]-t[1]})  centre d=({dc[0]:+.1f},{dc[1]:+.1f})  size d=({ds[0]:+d},{ds[1]:+d})")
        check(f"{name}: its ink sits where the render's does (centre within 1.5 px), its size within 2 px", abs(dc[0]) <= 1.5 and abs(dc[1]) <= 1.5 and abs(ds[0]) <= 2 and abs(ds[1]) <= 2, (dc, ds))
    A = np.asarray(mine, np.int16); B = np.asarray(target, np.int16)
    white = lambda y, x: tuple(A[y, x]) == (255, 255, 255)
    row = [x for x in range(1000, 1080) if white(232, x)]; col = [y for y in range(175, 290) if white(y, 1040)]
    check("the slot's white interior is the render's (x 1015..1064, y 189..275 within 1 px)", row and col and abs(min(row) - 1015) <= 1 and abs(max(row) + 1 - 1064) <= 1 and abs(min(col) - 189) <= 1 and abs(max(col) + 1 - 275) <= 1,
          ((min(row), max(row) + 1) if row else None, (min(col), max(col) + 1) if col else None))
    pad = np.pad(B, ((1, 1), (1, 1), (0, 0)), mode="edge")
    near = np.min([np.abs(A - pad[1+dy:1+dy+A.shape[0], 1+dx:1+dx+A.shape[1]]).max(axis=2) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
    x0, y0, x1, y1 = GIRL; gc = near[y0:y1, x0:x1]
    print(f"  the girl vs the render (within 1 px): mean {gc.mean():.2f} levels, {100 * (gc > 48).mean():.2f}% over 48")
    check("the girl is the frame's bitmap, where the frame has her (within 1 px: mean diff under 12 levels, under 6% of her box over 48)", gc.mean() < 12 and (gc > 48).mean() < 0.06)
    keep = np.zeros(near.shape, bool); x0, y0, x1, y1 = WHOLE; keep[y0:y1, x0:x1] = True
    for x0, y0, x1, y1 in OWN_T0 + BY_DESIGN + [GIRL]: keep[y0:y1, x0:x1] = False
    m = (near > 32) & keep; px = int(keep.sum())
    solid = m.copy(); solid[1:-1, 1:-1] &= m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:]; solid[0, :] = solid[-1, :] = False; solid[:, 0] = solid[:, -1] = False
    print(f"  pixel diff vs the render over the card, less Swiftie/chip, the slot, the ink bands and the girl (within 1 px): {int(m.sum())} of {px} px ({100*m.sum()/px:.2f}%), solid {int(solid.sum())} ({100*solid.sum()/px:.3f}%)")
    Image.fromarray(np.where(m, 255, np.where(keep, 0, 60)).astype(np.uint8)).save(out / "g_diff_mask.png")
    check("the card — the picture, the tiles, their shadows — pixel-matches the Figma render (solid diffs under 0.1% of the area)", solid.sum() / px < 0.001)
    pg.close(); b.close()
check("no page errors", not errs, errs[:3]); check("no failed requests", not bad, bad[:5])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
