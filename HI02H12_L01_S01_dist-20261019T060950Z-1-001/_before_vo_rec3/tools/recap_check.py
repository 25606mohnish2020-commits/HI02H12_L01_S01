"""Verify a mark page (MARKS_RECAP) against its Figma frame and its timing: T1, the पूर्ण-विराम page ([recap-fig2], FLN-by-MJ frame
764:144), or T1B, the अल्प-विराम page right after it ([recap-alp], frame 764:755: T1's design and behaviour with the frame's own
placements, no opening lines), or T1C, the प्रश्नवाचक-चिह्न page after that ([recap-prashn], frame 764:945, likewise; its two "?"
in the frame's Noto Sans Devanagari, 'Story Noto Q').
usage: python -I -X utf8 recap_check.py <index.html> <render 1280x720> <outdir> [T1|T1B|T1C]
       T1: recap2_figma_render_1280x720.png (the default page); T1B: recap_alp_figma_render_1280x720.png;
       T1C: recap_prashn_figma_render_1280x720.png
1. At 1333x750, the page mounted on its own: no title (the frames have none). T1: the lead line ("आपने देखा, ...", vo_recap_lead,
   [vo-rec]) then the intro line ("आइए समझते हैं कि कौन-से चिह्न का प्रयोग कब किया जाता है ।", vo_recap_intro) sound over the card
   alone — nothing of the mark shows before the intro has ended — and 0.7 s after it the mark comes; T1B / T1C: no line first, the mark
   comes 0.7 s after the page appears. Then: the sign's box + sign pop in as the name rises in whole, and the name's clip (0.45 s
   later) lights the SIGN — the words' orange + pop — from its first word to its last word's end (the name's own words never lit);
   0.3 s after it the use's clip sounds with nothing new on screen; 0.3 s after that the sentence's white box pops in as the
   sentence rises in whole, its clip 0.45 s later: as the clip reaches the sentence's first word the picture pops in, the words
   light one by one ([word-sync]), and each mark in the sentence (T1's "।", T1B's two commas, T1C's "?") keeps its orange from its own word on;
   आगे shows the reference's disabled pill ([dun-chrome]) until the sentence's clip has ended, then goes live, breathing, at T0's
   place; a 🔊 tap early (T1: in the intro; T1B: before the mark) or in the breath after the name is ignored (every clip plays
   once); a 🔊 tap afterwards reads the page again from the name (everything staying; the kept marks cleared, the sign and the words
   lit again, the marks kept again) with आगे hidden meanwhile; आगे leads on (T1 -> T1B -> T1C -> T2, no gate); past the Figma pages (G4)
   no story styling is left.
   [recap-sfx] The sounds of the reference hi02h11l02s04-file5's page 2 (T2), logged in the page (the engine's _tone and every
   <audio> play, on the samples' clock): the soft pop (_tone [720] sine 0.10 / 0.07, its sfxPopSoft) as the sign's box + name appear
   and as the sentence's box + sentence appear, the horse's sound (sfx_fb_correct.ogg at .55) as the picture appears — each once,
   in the frame it appears, and nothing else; the replay silent (nothing appears again). The picture comes in as the horse does: the
   computed transition is the reference's, and its opacity / scale every frame follow the reference's own trace.
2. The card is the frame's (96,106 1088x508 x 1333/1280, 64px corners); Swiftie, the 🔊 chip and आगे are exactly page 1 T0's
   (stage px: 76,472 190; 202,606 58; 581.5,550 170x62) — the frames' own Swiftie (35,415 245) is not used, as asked.
3. 1280x720 viewport (stage px x 1333/1280 = frame px): the sign's box, the sentence's box and the picture vs the frame's nodes;
   the sign, name and sentence by their INK vs the Figma render (centres within 1.5 px; the name and sentence in the frame's
   Baloo 2 ExtraBold = the lesson's 800 face, so their ink is the render's size; the sign's SemiBold renders here in the embedded
   700 face, a little bolder); the type; the sentence box's shadow = page 1 T0's ([textbox-shadow]) with the frame's 578x84 and
   20 px corners; the picture's shadow (T1's girl: the frame's drop shadow; T1B's fruits: none); per-pixel diffs vs the render over
   the boxes and the whole card (less Swiftie / chip / आगे, the three ink bands, the sentence box's shadow band — the frame's own
   shadow differs by design — and the picture, which is compared on its own: the same bitmap, resampled).
[recap-eg] (2026-11-04) T1's and T1B's examples and pictures are the user's ("मुझे आम खाना पसंद है।" + the girl with a mango; "मुझे लाल,
हरा और पीला रंग पसंद है ।" + the girl painting), not the renders': their sentence is judged by its ink centred on its white box (the
box interior is masked from the card diff), their picture against the user's own bitmap drawn into its box, and only the page's own
mark is kept (T1B's closing "।" lights and goes with its word).
"""
import sys, re, io, json, pathlib
import numpy as np
from playwright.sync_api import sync_playwright
from PIL import Image

html = pathlib.Path(sys.argv[1]).resolve(); target = Image.open(sys.argv[2]).convert("RGB")
out = pathlib.Path(sys.argv[3]).resolve(); out.mkdir(parents=True, exist_ok=True)
PAGE = sys.argv[4] if len(sys.argv) > 4 else "T1"
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)

FS = 1333 / 1280
AS_T0 = {   # stage px: the frame's card box; page 1 T0's Swiftie, chip and आगे
  ".tut-card.sfig-card": (96 * FS, 106 * FS, 1088 * FS, 508 * FS),
  ".sfig-swiftie":       (76, 472, 190, 190),
  ".tut-audio":          (202, 606, 58, 58),
  "#navBtn":             (581.5, 550, 170, 62),   # [dun-chrome] the reference's text pill, where T0 has it
}
CX, CY = 96, 106   # the frames' card origin (page px at 1280x720)
PAGES = {
  "T1": {   # frame 764:144 (its metadata: a group's children are in CARD px)
    # [recap-eg] (2026-11-04) the example and the picture are the user's (not in the render): "new_eg" judges the sentence by its ink
    # centred on its box, "pic_src" the picture against the user's own bitmap; the box interior is masked from the card diff
    "key": "purn", "mark": "।", "image": "img_recap_mango", "variant": None, "name": "पूर्ण विराम", "sent": "मुझे आम खाना पसंद है।",
    "lead": "vo_recap_lead", "intro": "vo_recap_intro", "next": "T1B", "new_eg": True, "pic_src": "recap_assets/src_recap_mango.png",
    "FRAME": {".rcf-sign": (CX+199-4, CY+65-4, 183, 177.355),   # node 764:326: 175x169.355 + its 4px OUTSIDE stroke
              ".rcf-ebox": (CX+199, CY+274, 578, 84),           # node 764:752
              ".rcf-pic":  (CX+835, CY+91, 176, 264)},          # node 764:753 (the user's 1024x1536 mango girl in it, as the old girl)
    "INK": {"sign": (310, 186, 460, 326), "name": (480, 200, 900, 320)},
    "TOL": {"sign": (6, 2), "name": (3, 2), "sentence": (3, 2)},   # (width, height) px: the sign's 600 face vs the embedded 700
    "BY_DESIGN": [(355, 190, 410, 310), (535, 203, 820, 303), (CX+199+8, CY+274+6, CX+199+578-8, CY+274+84-4), (280, 462, 890, 512),
                  (CX+835-6, CY+91-4, CX+835+176+6, CY+91+264+10)],
    "pic_filter": "drop-shadow(rgba(0, 0, 0, 0.25) 0px 2px 2px)"},
  "T1B": {   # frame 764:755
    # [recap-eg] (2026-11-04) the user's sentence and picture (the girl painting, 1199x1312, in the fruits' width and centre)
    "key": "alp", "mark": ",", "image": "img_recap_paint", "variant": "alp", "name": "अल्प विराम", "sent": "मुझे लाल, हरा और पीला रंग पसंद है ।",
    "lead": None, "intro": None, "next": "T1C", "new_eg": True, "pic_src": "recap_assets/src_recap_paint.png",
    "FRAME": {".rcf-sign": (CX+209-4, CY+65-4, 183, 177.355),   # node 764:937
              ".rcf-ebox": (CX+209, CY+274, 578, 84),           # node 764:940
              ".rcf-pic":  (CX+816, CY+96.18, 219, 239.65)},    # node 524:350's width and centre (816,143 219x146), the new bitmap's aspect
    "INK": {"sign": (316, 182, 470, 330), "name": (490, 200, 920, 320)},
    "TOL": {"sign": (6, 4), "name": (3, 2), "sentence": (3, 2)},   # the comma's 700 face: 27x36 for the render's 23x33
    "BY_DESIGN": [(368, 238, 414, 290), (540, 205, 840, 285), (CX+209+8, CY+274+6, CX+209+578-8, CY+274+84-4), (290, 462, 900, 512),
                  (CX+816-6, CY+96-4, CX+816+219+6, CY+96+240+10)],   # the new picture's box (it covers the render's fruits too)
    "pic_filter": "none"},
  "T1C": {   # frame 764:945
    "key": "prashn", "mark": "?", "image": "img_recap_house", "variant": "prashn", "name": "प्रश्नवाचक चिह्न", "sent": "तुम्हारा घर कहाँ है ?",
    "lead": None, "intro": None, "next": "T2",
    "FRAME": {".rcf-sign": (CX+199-4, CY+65-4, 183, 177.355),   # node 764:1127 (T1's place)
              ".rcf-ebox": (CX+199, CY+274, 580, 84),           # node 764:1129 (2 px wider than T1's)
              ".rcf-pic":  (CX+822, CY+168, 216, 144)},         # node 766:1140
    "INK": {"sign": (310, 180, 460, 330), "name": (480, 200, 920, 320), "sentence": (310, 384, 860, 458)},
    "TOL": {"sign": (1, 1), "name": (2, 2), "sentence": (2, 2)},   # the ?s in the frame's own face, so their ink is the render's
    "BY_DESIGN": [(350, 198, 415, 305), (500, 209, 877, 293), (434, 388, 733, 453), (280, 462, 890, 512),
                  (CX+822-6, CY+168-4, CX+822+216+6, CY+168+144+10)],
    "pic_filter": "drop-shadow(rgba(0, 0, 0, 0.25) 0px 2px 2px)",
    "font_mark": '"Story Noto Q"', "font_eg": '"Story Noto Q"'},
}
P = PAGES[PAGE]; K = P["key"]; SENT = P["sent"]; FRAME = P["FRAME"]; INK = P["INK"]
KEEP_WI = [i for i, w in enumerate(SENT.split()) if w.endswith(P["mark"])]   # the words whose mark stays lit ([recap-eg]: the page's own mark only)
NKEEP = len(KEEP_WI)
x0p, y0p, x1p, y1p = FRAME[".rcf-pic"][0], FRAME[".rcf-pic"][1], FRAME[".rcf-pic"][0] + FRAME[".rcf-pic"][2], FRAME[".rcf-pic"][1] + FRAME[".rcf-pic"][3]
PIC = (int(x0p), int(y0p), int(x1p), int(y1p))
WHOLE = (80, 90, 1200, 640)      # frame px: the card with its border and shadow
OWN_T0 = [(25, 400, 290, 720),   # ...less Swiftie (the frames' at 35,415 245x245 and T0's) + the 🔊 chip,
          (535, 490, 745, 600)]  # and आगे (not in the frames)
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
# one frame: the clip (lead / intro / <key>_name / _when / _eg), its clock, the sign's box and light, the name's shown / lit words, the
# sentence's box, shown / lit words and kept marks, the picture (and its computed opacity / transform), आगे
SAMPLE = r"""() => { const a = currentAudio, src = a ? a.src.split('/').pop() : '', nav = document.getElementById('navBtn'), q = (s) => document.querySelector(s);
  const m = src.match(/vo_recap_(\w+)\.ogg/), hot = (s) => [...document.querySelectorAll(s + ' .sfig-w')].map((w, i) => w.classList.contains('hot') ? i : -1).filter(i => i >= 0);
  return { clip: m ? m[1] : null, t: a ? a.currentTime : null, playing: isPlaying, ready: !!q('.rcf-row'),
    signIn: !!q('.rcf-sign.in'), signHot: !!q('.rcf-mark .sfig-w.hot'), nameShown: document.querySelectorAll('.rcf-name .sfig-w.on').length, nameHot: hot('.rcf-name'),
    eboxIn: !!q('.rcf-ebox.in'), egShown: document.querySelectorAll('.rcf-eg .sfig-w.on').length, egHot: hot('.rcf-eg'), keep: document.querySelectorAll('.rcf-eg .keep').length,
    picIn: !!q('.rcf-pic.in'), picOp: q('.rcf-pic') ? +(+getComputedStyle(q('.rcf-pic')).opacity).toFixed(3) : null,
    picTr: q('.rcf-pic') ? getComputedStyle(q('.rcf-pic')).transform : null,
    navVisible: nav.classList.contains('visible'), nav: nav.classList.contains('active'), ms: performance.now() }; }"""
# [recap-sfx] every sound the page makes: the engine's procedural _tone and every <audio> play, on the samples' clock
SOUNDS = """() => { window._snd = []; const T = window._tone;
  window._tone = function(f, ty, d, v){ window._snd.push({ ms: performance.now(), kind: 'tone', f: f.join('/'), ty, d, v }); return T.apply(this, arguments); };
  const P = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function(){ window._snd.push({ ms: performance.now(), kind: 'media', src: decodeURIComponent(String(this.currentSrc || this.src).split('/').pop()), vol: +this.volume.toFixed(3) });
    return P.apply(this, arguments); }; }"""
# [recap-sfx] the reference's horse coming in (hi02h11l02s04-file5 T2, .mb-p3 .mb-pic, traced every frame at 1333x750): ms after the
# frame its waiting class went -> opacity, scale
REF_PIC = [(16, .025, .8461), (33, .07, .8704), (50, .136, .8926), (66, .22, .9125), (83, .314, .9305), (100, .407, .9461), (117, .497, .9601),
           (133, .575, .9717), (150, .645, .9816), (166, .705, .9896), (183, .757, .9961), (200, .802, 1.0011), (216, .84, 1.0048), (233, .873, 1.0073),
           (250, .901, 1.0088), (266, .925, 1.0095), (283, .944, 1.0094), (300, .96, 1.0089), (316, .973, 1.0079), (333, .983, 1.0067),
           (350, .991, 1.0054), (366, .996, 1.004), (383, .999, 1.0027), (400, 1, 1.0016), (416, 1, 1.0008), (433, 1, 1.0002), (450, 1, 1.0)]
# the timeline is sampled IN the page, every frame; the two 🔊 taps are made in the page too, at their exact moments: the early one
# (T1: 1 s into the intro line; T1B: 0.3 s after the page has mounted, before the mark) and the one in the breath after the name
EARLY = "s.clip === 'intro' && s.playing && s.t > 1" if P["intro"] else "s.ready && performance.now() - window._t0 > 300"
TIMELINE = "(sample) => { window._tl = []; window._taps = []; window._t0 = performance.now(); const S = eval(sample); const step = () => { const s = S(); window._tl.push(s);" \
    " const chip = document.querySelector('.tut-audio');" \
    f" if (chip && !window._taps.includes('early') && {EARLY}) {{ window._taps.push('early'); chip.click(); }}" \
    f" if (s.clip === '{K}_name' && s.playing) window._seen0 = true;" \
    f" if (chip && !window._taps.includes('breath') && window._seen0 && s.clip === '{K}_name' && !s.playing) {{ window._taps.push('breath'); chip.click(); }}" \
    " if (!s.nav) requestAnimationFrame(step); }; requestAnimationFrame(step); }"
PULSING = "getComputedStyle(document.getElementById('navBtn'), '::after').animationName"

def lit_want(times, wend, t):
    """[word-sync] the word(s) lit at clip time t: the stretch [start, next start) holding t (words sharing a start light together),
    the last up to the last word's end; nothing after it"""
    if t is None or (wend is not None and t >= wend): return []
    st = None
    for x in times:
        if t >= x: st = x
    return [i for i, x in enumerate(times) if st is not None and x == st]

def ink(img, region):
    """the box of pixels at least 15 % of the way from white to the navy, in a region of a 1280x720 shot"""
    x0, y0, x1, y1 = region; A = np.asarray(img.crop(region).convert("RGB"), int)
    m = np.clip((765 - A.sum(axis=2)) / (765 - 165), 0, 1) >= 0.15
    ys, xs = np.nonzero(m)
    if not len(xs): return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1)

print(f"== {PAGE} ({P['name']}) ==")
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs, bad = [], []

    # ---- 1-2. timing at 1333x750
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    # the engine makes its AudioContext on the first sound (_ac); in the lesson the start tap and the pages before have long made it,
    # but a page mounted on its own would make it on the sign's pop, and new AudioContext() holds that frame 30-60 ms: made here first
    pg.evaluate("_ac()"); pg.wait_for_timeout(300)
    pg.evaluate(NAVLOG); pg.evaluate(SOUNDS); pg.evaluate(TIMELINE, SAMPLE); pg.evaluate(GOTO, PAGE)
    d = pg.evaluate("CARD.slides[state.idx].data")
    NT, NE = d["name"]["word_times"], d["name"].get("word_end"); ET, EE = d["example"]["word_times"], d["example"].get("word_end")
    check(f"the page's data: the mark \"{P['mark']}\" with its picture ({P['image']}), the name / use / example on vo_recap_{K}_name / _when / _eg, "
          f"the opening lines {P['lead']} / {P['intro']}, variant {P['variant']}, NO title",
          d.get("mark") == P["mark"] and d.get("image_id") == P["image"] and d["name"]["audio"] == f"vo_recap_{K}_name" and d["when"]["audio"] == f"vo_recap_{K}_when"
          and d["example"]["audio"] == f"vo_recap_{K}_eg" and d["example"]["text_hi"] == SENT and d["name"]["text_hi"] == P["name"]
          and d.get("lead_audio") == P["lead"] and d.get("intro_audio") == P["intro"] and d.get("variant") == P["variant"] and not d.get("title_hi") and "rows" not in d,
          {k: d.get(k) for k in ("mark", "image_id", "lead_audio", "intro_audio", "variant", "title_hi")})
    check("no title element on the page (the frame has none)", not pg.evaluate("!!document.querySelector('.sfig-title')"))
    if P["intro"]:
        pg.wait_for_function("isPlaying && currentAudio && currentAudio.src.includes('vo_recap_intro.') && currentAudio.currentTime > 1", timeout=20000, polling=20)
        pg.screenshot(path=str(out / "a_intro_1333.png"))
    pg.wait_for_function("!!document.querySelector('.rcf-mark .sfig-w.hot')", timeout=30000, polling=10); pg.wait_for_timeout(300)
    pg.screenshot(path=str(out / "b_sign_lit_1333.png"))
    pg.wait_for_function("document.querySelector('.rcf-pic').classList.contains('in') && !!document.querySelector('.rcf-eg .sfig-w.hot')", timeout=40000, polling=10); pg.wait_for_timeout(500)
    pg.screenshot(path=str(out / "c_sentence_1333.png"))
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=90000, polling=20)
    pg.wait_for_timeout(300); pg.screenshot(path=str(out / "d_end_1333.png"))
    samples, taps = pg.evaluate("window._tl"), pg.evaluate("window._taps")
    samples = [s for s in samples if s["ready"]]   # a frame sampled before GOTO has mounted the page has no row yet
    with open(out / "timeline.json", "w", encoding="utf-8") as f: json.dump(samples, f, indent=0)
    ms = lambda i: samples[i]["ms"]
    first = lambda cond, start=0: next(i for i in range(start, len(samples)) if cond(samples[i]))
    start_of = lambda c, i0=0: first(lambda s: s["clip"] == c and s["playing"], i0)
    end_of = lambda c, i0: first(lambda s: s["clip"] != c or not s["playing"], i0 + 1)
    quiet = lambda s: not (s["signIn"] or s["signHot"] or s["nameShown"] or s["eboxIn"] or s["egShown"] or s["picIn"] or s["keep"])
    if P["intro"]:
        i_lead = start_of("lead"); i_leade = end_of("lead", i_lead); i_intro = start_of("intro", i_leade); i_open = end_of("intro", i_intro)
        check("the lead line then the intro line sound first, over the card alone (nothing of the mark shows before the intro has ended)",
              i_lead < i_leade <= i_intro < i_open and all(quiet(s) for s in samples[:i_open]), (round(ms(i_leade) - ms(i_lead)), round(ms(i_open) - ms(i_intro))))
        CLIPS = ["lead", "intro"]
    else:
        i_open = 0
        check("no opening line: the page is silent and empty until its mark comes", not any(s["clip"] and s["playing"] for s in samples if not s["signIn"])
              and all(quiet(s) for s in samples[:first(lambda s: s["signIn"])]))
        CLIPS = []
    i_nm = start_of(f"{K}_name", i_open); i_nme = end_of(f"{K}_name", i_nm); i_wh = start_of(f"{K}_when", i_nme); i_whe = end_of(f"{K}_when", i_wh)
    i_eg = start_of(f"{K}_eg", i_whe); i_ege = end_of(f"{K}_eg", i_eg)
    starts = lambda clip: sum(1 for i, s in enumerate(samples) if s["clip"] == clip and s["playing"]
                              and (i == 0 or not (samples[i - 1]["clip"] == clip and samples[i - 1]["playing"])))
    CLIPS += [f"{K}_name", f"{K}_when", f"{K}_eg"]
    check("🔊 taps early and in the breath after the name were ignored (each clip plays once)",
          taps == ["early", "breath"] and all(starts(c) == 1 for c in CLIPS), f"taps made: {taps}, starts {[starts(c) for c in CLIPS]}")
    # the name beat
    i_sign = first(lambda s: s["signIn"]); i_nr = first(lambda s: s["nameShown"] > 0)
    check(("0.7 s after the intro" if P["intro"] else "0.7 s after the page appears") + " the sign's box pops in as the name rises in whole (same frame), the name's clip ~0.45 s after the rise",
          600 <= ms(i_sign) - ms(i_open) <= 1000 and abs(ms(i_nr) - ms(i_sign)) <= 60 and {s["nameShown"] for s in samples} <= {0, len(NT)}
          and 400 <= ms(i_nm) - ms(i_nr) <= 800, (round(ms(i_sign) - ms(i_open)), round(ms(i_nr) - ms(i_sign)), round(ms(i_nm) - ms(i_nr))))
    timed = [s for s in samples[i_nm:i_nme] if s["clip"] == f"{K}_name" and s["playing"] and s["t"] is not None]
    want_sign = lambda t: bool(lit_want([NT[0]], NE, t))
    off = [s for s in timed if s["signHot"] not in (want_sign(s["t"]), want_sign(s["t"] - 0.05))]
    check("the SIGN is lit (orange, popped) from the name clip's first word to its last word's end — and at no other time; the name's words never lit",
          len(timed) > 20 and not off and any(s["signHot"] for s in timed) and not any(s["signHot"] for s in samples[:i_nm] + samples[i_nme:])
          and not any(s["nameHot"] for s in samples), f"{len(timed)} samples, {len(off)} off, lit {sum(1 for s in timed if s['signHot'])}")
    look = pg.evaluate("""() => { const w = document.querySelector('.rcf-mark .sfig-w'); w.classList.add('hot'); const c = getComputedStyle(w);
      const r = [c.color, c.animationName, c.animationDuration]; w.classList.remove('hot'); return r; }""")
    check("the sign's light is the words' (#E86A00 + p2WordPop .28 s, [word-sync])", look == ["rgb(232, 106, 0)", "p2WordPop", "0.28s"], look)
    # the use
    check("the use's clip starts ~0.3 s after the name's and nothing new shows while it sounds",
          200 <= ms(i_wh) - ms(i_nme) <= 700 and not any(s["eboxIn"] or s["egShown"] or s["picIn"] or s["keep"] for s in samples[:i_whe]), round(ms(i_wh) - ms(i_nme)))
    # the sentence beat
    i_ebox = first(lambda s: s["eboxIn"]); i_er = first(lambda s: s["egShown"] > 0)
    check("~0.3 s after the use the sentence's box pops in as the sentence rises in whole (same frame), its clip ~0.45 s after the rise",
          200 <= ms(i_ebox) - ms(i_whe) <= 700 and abs(ms(i_er) - ms(i_ebox)) <= 60 and {s["egShown"] for s in samples} <= {0, len(ET)}
          and 400 <= ms(i_eg) - ms(i_er) <= 800, (round(ms(i_ebox) - ms(i_whe)), round(ms(i_er) - ms(i_ebox)), round(ms(i_eg) - ms(i_er))))
    i_pic = first(lambda s: s["picIn"])
    check(f"the picture pops in as the clip reaches the sentence's first word ({ET[0]} s on its clock, within -0.05/+0.15 s), not before",
          i_eg <= i_pic < i_ege and -0.05 <= samples[i_pic]["t"] - ET[0] <= 0.15 and not any(s["picIn"] for s in samples[:i_pic]), round(samples[i_pic]["t"] - ET[0], 2) if i_pic >= i_eg else None)
    timed = [s for s in samples[i_eg:i_ege] if s["clip"] == f"{K}_eg" and s["playing"] and s["t"] is not None]
    off = [s for s in timed if s["egHot"] not in (lit_want(ET, EE, s["t"]), lit_want(ET, EE, s["t"] - 0.05))]
    seen = {tuple(s["egHot"]) for s in timed if s["egHot"]}
    check("each word of the sentence lit as the clip reaches it, one at a time, none after the last word's end ([word-sync])",
          len(timed) > 20 and not off and len(seen) >= len(set(ET)) - 1, f"{len(timed)} samples, {len(off)} off, {len(seen)} lit states / {len(set(ET))} stretches")
    kd = []
    for k, wi in enumerate(KEEP_WI):
        i_k = first(lambda s: s["keep"] >= k + 1)
        kd.append(round(samples[i_k]["t"] - ET[wi], 2) if i_eg <= i_k < i_ege else None)
    counts = [s["keep"] for s in samples]
    check(f"each mark of the sentence ({NKEEP}) keeps its orange from its own word (within -0.05/+0.15 s) to the end, never before",
          all(x is not None and -0.05 <= x <= 0.15 for x in kd) and counts == sorted(counts) and counts[-1] == NKEEP and not any(s["keep"] for s in samples[:i_eg]), kd)
    kcol = pg.evaluate("[...document.querySelectorAll('.rcf-eg .keep')].map(e => [e.textContent, getComputedStyle(e).color])")
    check("the kept marks are the words' orange, and only the marks", len(kcol) == NKEEP and all(c == "rgb(232, 106, 0)" and re.fullmatch(r"[।?,!]+", t) for t, c in kcol), kcol)
    # [recap-sfx] the reference's sounds, each in the frame its thing appears, and nothing else during the reading
    snd = [e for e in pg.evaluate("window._snd") if samples[0]["ms"] - 50 <= e["ms"] <= ms(i_ege) + 500]
    pops = [e for e in snd if e["kind"] == "tone" and e["f"] == "720" and e["ty"] == "sine" and e["d"] == 0.1 and e["v"] == 0.07]
    horse = [e for e in snd if e["kind"] == "media" and e["src"] == "sfx_fb_correct.ogg"]
    others = [e for e in snd if e not in pops and e not in horse and not (e["kind"] == "media" and e["src"].startswith("vo_"))]
    check("the soft pop (the reference's sfxPopSoft: _tone 720 Hz sine, 0.10 s, 0.07) sounds as the sign's box + name appear and as the sentence's box + sentence appear — twice, each within 50 ms of its frame",
          len(pops) == 2 and abs(pops[0]["ms"] - ms(i_sign)) <= 50 and abs(pops[1]["ms"] - ms(i_ebox)) <= 50,
          [round(e["ms"] - ms(i_sign)) for e in pops[:1]] + [round(e["ms"] - ms(i_ebox)) for e in pops[1:2]] + [len(pops)])
    check("the horse's sound (the reference's fbCorrect: sfx_fb_correct.ogg at .55) as the picture appears — once, within 50 ms of its frame",
          len(horse) == 1 and abs(horse[0]["ms"] - ms(i_pic)) <= 50 and horse[0]["vol"] == 0.55, [(round(e["ms"] - ms(i_pic)), e["vol"]) for e in horse])
    check("no other sound effect during the reading (only the voice clips besides)", not others, others[:4])
    pi = [s for s in samples if s["picOp"] is not None]
    j0 = next(k for k, s in enumerate(pi) if s["picIn"])
    def sc(tr): return 1.0 if tr in (None, "none") else float(tr.split("(")[1].split(",")[0])
    # the curve from the last frame still waiting: the class flips between two samples, and whether the first sample after it already
    # shows a frame of the transition depends on the rAF order (the cue's tick vs the sampler's), so the waiting frame bounds its start
    t_in = pi[j0]["ms"]; curve = [(s["ms"] - t_in, s["picOp"], sc(s["picTr"])) for s in pi[max(j0 - 1, 0):] if s["ms"] - t_in <= 600]
    def at(t, k):   # our curve at t ms after the class went on (k 0 = opacity, 1 = scale), linearly interpolated
        for (a, *va), (b2, *vb) in zip(curve, curve[1:]):
            if a <= t <= b2: return va[k] + (vb[k] - va[k]) * ((t - a) / (b2 - a) if b2 > a else 0)
        return curve[-1][k + 1]
    # the two traces are sampled on different frames, so a frame's worth of slack: each reference point is compared with ours
    # anywhere within ±17 ms of it
    def near(t, k, want): return min(abs(at(t + dt, k) - want) for dt in (-17, -8, 0, 8, 17))
    d_op = max(near(t, 0, o) for t, o, _ in REF_PIC); d_sc = max(near(t, 1, v) for t, _, v in REF_PIC)
    before = [s for s in pi[:j0] if s["ms"] > t_in - 200]
    check("the picture comes in as the reference's horse: from opacity 0 / scale .82, its opacity and scale every frame on the reference's trace (within .05 / .006), up through ~1.009 and settled by 0.5 s",
          before and all(s["picOp"] == 0 and abs(sc(s["picTr"]) - .82) < 1e-3 for s in before) and d_op <= .05 and d_sc <= .006
          and 1.007 <= max(v for _, _, v in curve) <= 1.011 and all(o == 1 and abs(v - 1) < 1e-3 for t, o, v in curve if t >= 500),
          f"max d opacity {d_op:.3f}, max d scale {d_sc:.4f}, peak {max(v for _, _, v in curve):.4f}")
    tr = pg.evaluate("() => { const c = getComputedStyle(document.querySelector('.rcf-pic')); return [c.transitionProperty, c.transitionDuration, c.transitionTimingFunction, c.transitionDelay, c.animationName]; }")
    check("the picture's computed transition is the reference horse's (opacity .4s ease, transform .45s cubic-bezier(.34,1.4,.6,1), no animation)",
          tr == ["opacity, transform", "0.4s, 0.45s", "ease, cubic-bezier(0.34, 1.4, 0.6, 1)", "0s, 0s", "none"], tr)
    check("आगे stays away (not live) until the sentence's clip has ended", not any(s["nav"] for s in samples[:i_ege]))
    check("आगे opens (live, breathing) within 0.5 s of the clip's end", samples[-1]["nav"] and 0 <= ms(len(samples) - 1) - ms(i_ege) <= 500 and pg.evaluate(PULSING) == "navBreathe",
          f"{ms(len(samples) - 1) - ms(i_ege):.0f} ms after the clip ended")
    pg.evaluate("document.getElementById('navBtn').style.animation = 'none'")   # measure आगे at rest, not mid-pulse
    boxes = pg.evaluate(BOXES, list(AS_T0)); worst = 0
    pg.evaluate("document.getElementById('navBtn').style.animation = ''")
    print("== card vs the frame; Swiftie / chip / आगे vs page 1 T0 (stage px) ==")
    for sel, exp in AS_T0.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, dd)
        print(f"  {sel:22s} got {[round(v,2) for v in got]}  want {[round(v,2) for v in exp]}  max|d|={dd:.2f}")
    check("card box is the frame's; Swiftie, 🔊 chip and आगे are exactly page 1 T0's (within 0.5 px)", worst <= 0.5, f"worst {worst:.2f}px")
    radius = pg.evaluate("getComputedStyle(document.querySelector('.tut-card.sfig-card')).borderTopLeftRadius")
    check("the card has the frame's 64px corners (x 1333/1280)", abs(float(radius[:-2]) - 64 * FS) < 0.05, radius)
    # the replay
    pg.wait_for_timeout(1200)
    pg.click(".tut-audio", force=True); pg.wait_for_timeout(300)
    r = pg.evaluate(SAMPLE)
    check("🔊 afterwards reads the page again from the name: everything staying (box, sign, name, sentence box, sentence, picture), the kept marks cleared, the sign lit on the name's clip",
          r["clip"] == f"{K}_name" and r["playing"] and r["signIn"] and r["nameShown"] == len(NT) and r["eboxIn"] and r["egShown"] == len(ET) and r["picIn"]
          and r["keep"] == 0 and r["signHot"] in (want_sign(r["t"]), want_sign(r["t"] - 0.05)), r)
    check("आगे is hidden while the replay sounds", not r["navVisible"])
    t_rep = pg.evaluate("performance.now()") - 400
    pg.wait_for_function(f"document.querySelectorAll('.rcf-eg .keep').length === {NKEEP}", timeout=30000, polling=20)
    pg.wait_for_function("!isPlaying && document.getElementById('navBtn').classList.contains('active')", timeout=30000)
    pg.wait_for_timeout(300)
    check("...the replay runs the whole reading again (the marks kept once more) and आगे comes back live, breathing", pg.evaluate(PULSING) == "navBreathe")
    rep = [e for e in pg.evaluate("window._snd") if e["ms"] >= t_rep and not (e["kind"] == "media" and e["src"].startswith("vo_"))]
    check("[recap-sfx] the replay makes no pop and no horse sound (nothing appears again)", not rep, rep[:4])
    log = [e for e in pg.evaluate("window._navLog") if e["slide"] == PAGE]
    first_on = next((e for e in log if e["img"] == "ON"), None)   # [dun-chrome] the reference's pill: disabled art through the clips, live once the last has ended
    check("आगे shows the reference's disabled pill from the start, through every clip (frame by frame, incl. the replay), and goes live only once the sentence's clip has ended",
          log and log[0]["img"] == "DISABLED" and first_on is not None and first_on["clip"] == f"vo_recap_{K}_eg.ogg" and not first_on["playing"],
          [(round(e["ms"]), e["img"], e["clip"], e["playing"]) for e in log])
    check("आगे is never live while a VO plays", not any(e["img"] == "ON" and e["playing"] for e in log))
    pg.click("#navBtn", force=True)   # force: the active pill pulses forever, so it is never "stable"
    pg.wait_for_function(f"CARD.slides[state.idx].id === '{P['next']}'", timeout=10000)
    NEXT = {"T1B": ("rcf-v-alp", "the अल्प-विराम page"), "T1C": ("rcf-v-prashn", "the प्रश्नवाचक-चिह्न page")}
    landed = (f"!!document.querySelector('.tut-card.sfig-recap .rcf-row.{NEXT[P['next']][0]}')" if P["next"] in NEXT
              else "!!document.querySelector('.tut-card.sfig-round .dsc-bg')")   # [t2-scene] T2 = the hallway scene on T1's card
    check(f"आगे leads to {P['next']} ({NEXT[P['next']][1] if P['next'] in NEXT else 'the hallway scene, see scene_check.py'}), no extra gate",
          not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')") and pg.evaluate(landed))
    pg.wait_for_timeout(1500); pg.screenshot(path=str(out / f"e_{P['next']}_after.png"))
    pg.evaluate(GOTO, "G4"); pg.wait_for_timeout(600)
    STAGE = "[!!document.querySelector('.sfig-card'), document.getElementById('stage').className, getComputedStyle(document.getElementById('stage')).backgroundColor]"
    seen_g4 = pg.evaluate(STAGE)
    fresh = b.new_page(viewport={"width": 1333, "height": 750}); fresh.goto(html.as_uri()); fresh.wait_for_timeout(1500)
    fresh.evaluate(GOTO, "G4"); fresh.wait_for_timeout(600); clean = fresh.evaluate(STAGE)
    fresh.evaluate(GOTO, "T0"); fresh.wait_for_selector(".sfig-textbox"); t0_shadow = fresh.evaluate("getComputedStyle(document.querySelector('.sfig-textbox')).boxShadow"); fresh.close()
    # G4 (the first page past the Figma ones) keeps its own theme (thm-toybox, a pale blue stage): it must look exactly as it does when mounted on its own
    check("no story styling is left past the Figma pages (G4 as when mounted on its own)", not seen_g4[0] and seen_g4 == clean, (seen_g4, clean))
    pg.close()

    # ---- 3. geometry + pixel diff at 1280x720
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate(GOTO, PAGE)
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=90000)
    pg.evaluate("document.querySelectorAll('.rcf-eg .keep').forEach(w => w.classList.remove('keep'))")   # the frame draws the sentence plain
    pg.wait_for_timeout(700)
    shot = out / "f_end_1280.png"; pg.screenshot(path=str(shot))
    boxes = pg.evaluate(BOXES, list(FRAME)); worst = 0
    print("== boxes vs the frame (px) ==")
    for sel, exp in FRAME.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, dd)
        print(f"  {sel:12s} got {[round(v,2) for v in got]}  frame {[round(v, 3) for v in exp]}  max|d|={dd:.2f}")
    check("the sign's box, the sentence's box and the picture within 1 px of the frame's nodes", worst <= 1.0, f"worst {worst:.2f}px")
    radii = pg.evaluate("[getComputedStyle(document.querySelector('.rcf-sign')).borderTopLeftRadius, getComputedStyle(document.querySelector('.rcf-ebox')).borderTopLeftRadius, getComputedStyle(document.querySelector('.rcf-sign')).borderTopWidth]")
    check("the sign's box: 10px corners + its 4px #DADADA stroke (14px outside); the sentence's box: 20px corners", radii == ["14px", "20px", "4px"], radii)
    shadow = pg.evaluate("getComputedStyle(document.querySelector('.rcf-ebox')).boxShadow")
    check("the sentence box's shadow is exactly page 1 T0's ([textbox-shadow]), computed the same", shadow == t0_shadow, (shadow, t0_shadow))
    pf = pg.evaluate("getComputedStyle(document.querySelector('.rcf-pic')).filter")
    check(f"the picture's shadow is the frame's ({P['pic_filter']})", pf == P["pic_filter"], pf)
    lines = pg.evaluate("""() => [...document.querySelectorAll('.rcf-name p, .rcf-eg p')].map(p => { const ws = [...p.querySelectorAll('.sfig-w')];
      const tops = [...new Set(ws.map(w => Math.round(w.getBoundingClientRect().top)))];
      return tops.map(t => ws.filter(w => Math.round(w.getBoundingClientRect().top) === t).map(w => w.textContent).join(' ')); })""")
    print("  text lines:", lines)
    check("the name and the sentence are the frame's, on one line each", lines == [[P["name"]], [SENT]])
    fonts = pg.evaluate("""([m, q]) => { const f = (s) => { const c = getComputedStyle(document.querySelector(s)); return [c.fontFamily.split(',')[0], c.fontWeight, c.fontSize, c.color]; };
      return [f('.rcf-mark p'), f('.rcf-name'), f('.rcf-eg'), document.fonts.check("600 128px 'Baloo 2'", m) && document.fonts.check("800 64px 'Story Baloo 2'", 'विराम')
              && (!q || document.fonts.check("600 128px 'Story Noto Q'", '?') && document.fonts.check("800 40px 'Story Noto Q'", '?'))]; }""",   # T1C's ? face: a face loads only once used, so only there
                       [P["mark"], "font_mark" in P])
    fm, fe = P.get("font_mark", '"Baloo 2"'), P.get("font_eg", '"Story Baloo 2"')
    check("type: the sign in the frame's face (T1 / T1B: the family's 600 = the embedded 700 face, as T0's text; T1C: Noto Sans Devanagari SemiBold) at its 128px #002F76; "
          "the name and sentence Baloo 2 800 at 64 / 40px #012F76 (T1C's ? in Noto ExtraBold), every face loaded",
          fonts[0] == [fm, "600", "128px", "rgb(0, 47, 118)"] and fonts[1] == ['"Story Baloo 2"', "800", "64px", "rgb(1, 47, 118)"]
          and fonts[2] == [fe, "800", "40px", "rgb(1, 47, 118)"] and fonts[3], fonts)
    mine = Image.open(shot).convert("RGB")
    print("== text ink vs the Figma render (page px): centre and size ==")
    for name, region in INK.items():
        a, t = ink(mine, region), ink(target, region)
        if not a or not t: check(f"{name}: ink found on both", False, (a, t)); continue
        dc = ((a[0] + a[2]) / 2 - (t[0] + t[2]) / 2, (a[1] + a[3]) / 2 - (t[1] + t[3]) / 2)
        ds = ((a[2] - a[0]) - (t[2] - t[0]), (a[3] - a[1]) - (t[3] - t[1]))
        tw, th = P["TOL"][name]
        print(f"  {name:9s} page {[int(v) for v in a]} ({a[2]-a[0]}x{a[3]-a[1]})  render {[int(v) for v in t]} ({t[2]-t[0]}x{t[3]-t[1]})  centre d=({dc[0]:+.1f},{dc[1]:+.1f})  size d=({ds[0]:+d},{ds[1]:+d})")
        check(f"{name}: its ink sits where the render's does (centre within 1.5 px), its size within {tw} x {th} px",
              abs(dc[0]) <= 1.5 and abs(dc[1]) <= 1.5 and abs(ds[1]) <= th and abs(ds[0]) <= tw, (dc, ds))
    if P.get("new_eg"):   # [recap-eg] the user's sentence (the render has the old one): its ink centred on its box, on one line, inside it
        bx, by, bw, bh = boxes[".rcf-ebox"]
        a = ink(mine, (int(bx) + 8, int(by) + 6, int(bx + bw) - 8, int(by + bh) - 6))
        dc = ((a[0] + a[2]) / 2 - (bx + bw / 2), (a[1] + a[3]) / 2 - (by + bh / 2))
        print(f"  sentence  page {[int(v) for v in a]} ({a[2]-a[0]}x{a[3]-a[1]})  box {[round(v, 1) for v in (bx, by, bw, bh)]}  centre d from the box's=({dc[0]:+.1f},{dc[1]:+.1f})"
              f"  side white {a[0] - bx:.0f} / {bx + bw - a[2]:.0f}")
        check("sentence (the user's): its ink centred on its white box across (within 1 px) and down (within 5 px: the frame's baseline kept — its own sentence sat 3.5 px low), "
              "at least 10 px of white each side, the type's height (48-54 px of ink at 40 px)",
              abs(dc[0]) <= 1.0 and abs(dc[1]) <= 5 and a[0] - bx >= 10 and bx + bw - a[2] >= 10 and 48 <= a[3] - a[1] <= 54, dc)
    A = np.asarray(mine, np.int16); B = np.asarray(target, np.int16)
    pad = np.pad(B, ((1, 1), (1, 1), (0, 0)), mode="edge")
    near = np.min([np.abs(A - pad[1+dy:1+dy+A.shape[0], 1+dx:1+dx+A.shape[1]]).max(axis=2)
                   for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
    if P.get("pic_src"):   # [recap-eg] the user's picture: the page against the user's bitmap drawn into the picture's box over the page without it
        src = Image.open(SCRIPT_DIR / P["pic_src"]).convert("RGBA")
        info = pg.evaluate("(() => { const i = document.querySelector('.rcf-pic img'); return [decodeURIComponent(i.currentSrc.split('/').pop()), i.naturalWidth, i.naturalHeight, i.complete]; })()")
        check(f"the picture is the user's ({P['image']}.webp, {src.size[0]}x{src.size[1]} like {P['pic_src']}), loaded", info == [P["image"] + ".webp", src.size[0], src.size[1], True], info)
        pg.evaluate("document.querySelector('.rcf-pic').style.visibility = 'hidden'"); pg.wait_for_timeout(300)
        bare = Image.open(io.BytesIO(pg.screenshot())).convert("RGBA")
        pg.evaluate("document.querySelector('.rcf-pic').style.visibility = ''"); pg.wait_for_timeout(200)
        px_, py_, pw_, ph_ = boxes[".rcf-pic"]; W, H = round(pw_), round(ph_)
        lay = Image.new("RGBA", bare.size, (0, 0, 0, 0)); lay.paste(src.resize((W, H), Image.LANCZOS), (round(px_), round(py_)))
        want = np.asarray(Image.alpha_composite(bare, lay).convert("RGB"), np.int16); opaque = np.asarray(lay)[..., 3] >= 243
        padw = np.pad(want, ((1, 1), (1, 1), (0, 0)), mode="edge")
        nearw = np.min([np.abs(A - padw[1+dy:1+dy+A.shape[0], 1+dx:1+dx+A.shape[1]]).max(axis=2) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
        pc = nearw[opaque]
        print(f"  the picture vs the user's bitmap in its box (within 1 px, its opaque {int(opaque.sum())} px): mean {pc.mean():.2f} levels, {100 * (pc > 48).mean():.2f}% over 48")
        check("the picture is the user's bitmap, undistorted in its box (within 1 px: mean diff under 12 levels, under 6% of its area over 48)", pc.mean() < 12 and (pc > 48).mean() < 0.06)
    else:
        x0, y0, x1, y1 = PIC; pc = near[y0:y1, x0:x1]
        print(f"  the picture vs the render (within 1 px): mean {pc.mean():.2f} levels, {100 * (pc > 48).mean():.2f}% over 48")
        check("the picture is the frame's bitmap, where the frame has it (within 1 px: mean diff under 12 levels, under 6% of its area over 48)", pc.mean() < 12 and (pc > 48).mean() < 0.06)
    keep = np.zeros(near.shape, bool); x0, y0, x1, y1 = WHOLE; keep[y0:y1, x0:x1] = True
    for x0, y0, x1, y1 in OWN_T0 + P["BY_DESIGN"]: keep[y0:y1, x0:x1] = False
    m = (near > 32) & keep; px = int(keep.sum())
    solid = m.copy(); solid[1:-1, 1:-1] &= m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:]
    solid[0, :] = solid[-1, :] = False; solid[:, 0] = solid[:, -1] = False
    print(f"  pixel diff vs Figma render over the whole card, less Swiftie/chip/आगे, the ink bands, the box's shadow band and the picture (within 1 px): "
          f"{int(m.sum())} of {px} px ({100*m.sum()/px:.2f}%), of them solid: {int(solid.sum())} ({100*solid.sum()/px:.3f}%)")
    Image.fromarray(np.where(m, 255, np.where(keep, 0, 60)).astype(np.uint8)).save(out / "f_diff_mask_card.png")
    # what is left within 1 px is anti-aliasing: a 1-px line along the boxes' and the card's edges; a misplaced box shows as whole shapes
    check("the whole card (edges, corners, grid, the two boxes) pixel-matches the Figma render (solid diffs under 0.05% of the area)", solid.sum() / px < 0.0005)
    pg.close()
    b.close()
check("no page errors", not errs, errs[:3]); check("no failed requests", not bad, bad[:5])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
