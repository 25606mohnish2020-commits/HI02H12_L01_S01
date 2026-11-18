"""Verify the title page: the Figma frame's card against its render, and — since [dun-chrome] (2026-10-27) — the reference
game's cover around it: its sky, its play button appearing only once the welcome has been heard, its bird and the chip at the
bird's feet.
usage: python -I title_check.py <index.html> <figma_target.png> <outdir>
1. 1280x720 viewport, autoplay BLOCKED (the welcome cannot play by itself): screenshot + per-pixel diff vs the Figma render INSIDE
   THE CARD (the background is the reference's sunburst and drifting stars now, not the frame's), masking the reference's bird,
   play button and chip where they overlap the card.
2. Every title element's rendered box vs the frame's numbers (in 1280-frame px); the reference's three (the bird 208 px at the
   card's bottom-left, the play button 140 px centred 2 px above the card's bottom, the chip 70 px at the bird's feet) vs theirs.
3. 1333x750, autoplay ALLOWED: through the welcome the play button is absent and the chip is off; once the welcome has ended the
   button pops in (.ready) and breathes (.sg-breathe), the chip is live; a tap on the chip replays the welcome (the button stays);
   a tap on the bird replays it too; the bird's wave file is in place from the loader's fade; the sky is on (87 stars, the glow
   [cover-fx] / [cover-eyes] (2026-10-29): the pixel comparison hides the added light (.sg-fx) and the eye canvases (.sgf-eyes), which
   are on top of the frame's art by request; the fx layer sits right after the scene in the card's 9 px frame (1096x438), its
   flare breathes (sgFlare2, screen blend) and its dust canvas is alive; a live-eyes canvas covers each of the three characters'
   pictures, drawing, blinking on its own clock, every gaze following the mouse and turning curious at a tap; off the cover the
   canvases hide and the dust stops.
   breathing) and a tapped star pops.
[title-off] (2026-11-15) the frame's title art (रुको सोचो चिन्ह लगाओ) is removed: its box is masked in the Figma comparison (the
   render still has it); no title art element on the page.
[title-text] (2026-11-15, later) a heading in the mtcg2a04l02 cover's title look stands in the sky instead: one .sgf-heading in the
   card reading exactly "रुको , सोचो , चिह्न लगाओ ।"; Baloo 2 800 at 64 stage px, #F85A00, letter/word spacing .5/14 px and the
   reference rule's text-shadow (title_assets/ref_mtcg_sg_title.css, the rule as served) exactly; centred on the card, clear above the
   characters, painted; no animation or transition on it or the card, and its box never moves through the welcome. Its text box (+14 px)
   is masked in the Figma comparison too (the render has no heading). The old "only sky in the title box" check went with it.
[title-color] (2026-11-15, later) the heading in the user's picture's colours, same font/size/text/place: the text maroon #420202
   under a fill layer (::after, data-text, the same font and spacing) in the yellow-to-gold gradient, clipped to the letters; the
   text-shadow = a 3.5 px maroon outline ring on top of the reference's white rim and blue edge bands set out by it (blue #0345A1),
   the drop moved with it — 162 parts, regenerated here (the generator first proves it reproduces the reference rule's 98); data-text
   and aria-label = the exact text; painted yellow, maroon, white and deep blue; no animation on it, its fill layer or the card. The
   Figma mask widens to the text box + 18 px.
[title-stroke] (2026-11-15, later) the maroon outline 2.5 px (was 3.5), then on the same ask again 2.0 px: _colored(2.0, ...).
[title-stroke-off] (2026-11-15, later) the outline removed: the text-shadow is the reference rule's 98 parts with blue #0345A1, the text's
   own colour the fill's middle gold #FDCC02; painted check: no maroon pixels left.
[title-dark] (2026-11-15, later) the fill one family darker (#FFA800 > #FF9C00 > #FB8500 > #F57500 > #EE6500 > #E25400; text #FB8500);
   new check: every fill colour >= 1.9 : 1 against the white rim, the darkest >= 3 : 1 (the yellow one was 1.27 .. 2.36).
[title-dark2] (2026-11-15, after [title-fly]) the same ask again -> one more family darker (#FF9500 > #FA8200 > #F27000 > #E86000 >
   #DE5200 > #D04500; text #F27000): every fill colour >= 2.2 : 1, the darkest >= 4.5 : 1; the painted counts take the deeper orange.
[title-dark3] (2026-11-15, after [title-fly2]) the same words a third time -> #F08400 > #EA7300 > #E06200 > #D45500 > #C84900 > #B83C00
   (text #E06200): every fill colour >= 2.6 : 1, the darkest >= 5.5 : 1.
[title-fly] (2026-11-15, later) the card follows Figma FLN-by-MJ 956:2 (title_assets_figma_render_1280x720.png is that frame's render
   now; 386:17's is kept as ..._v1_386-17.png): the comma left, the question mark centre, the danda right, the new shadows. At the end
   of the welcome the danda flies into the heading's । and the comma (splitting in two) into its two commas while the question mark
   watches: checked in the autoplay run — nothing moves while the welcome plays; the flight starts within 1.2 s of its end; three
   flights (danda -> ।, comma -> 2nd comma, its twin -> 1st comma), each glyph box on the heading's painted letter (within 2 px), each
   glyph clone ending exactly on it (translate 0, scale 1, opacity 1) and clipped round it; the question mark looks right at the
   danda and left at the comma, the danda up at the title; at the end the two are gone from the ground, the question mark is where
   it stood, no clone or sparkle is left, and the heading (box, no animation, pixels) is as before the flight.
[title-fly2] (2026-11-15, later) the flight now runs INSIDE the welcome: nothing moves before the line sounds; it starts within 1.2 s of
   the line's first sample and is over (the last glyph copy faded) while the line still plays; the play button comes only after that,
   at the line's end as before. The before shot of the heading is the still page (autoplay blocked) at the autoplay run's viewport.
[title-punct] (2026-11-16) the heading's , , । are hidden until their symbols land. On the still page the heading carries
   .sgf-punct-off: an even-odd clip-path with one hole per glyph, each = that glyph's ink box (measured here: Range + canvas
   measureText, as the flight does) + 14 px each side, 12 above, 24 below (= its landing clone's region). With every moving layer
   stopped: inside the holes nothing of the heading is painted (= the page with no heading), outside them the heading is the whole
   heading's, pixel for pixel, and no heading paint crosses a hole's edge (no neighbour cut, nothing of a symbol left outside). In the
   autoplay run (a recorder on the heading's style/class): three holes until the flight, the holes it re-measures = the CSS's; each
   hole closes only once its clone has settled (its animation at >= 95 %: exactly 1x, opaque), the । first, then the two commas; then
   no clip at all. A play button that comes with no flight (page 1 forces .ready) shows the heading whole at once. The [title-fly]
   before/after comparison now leaves the holes out; inside them the heading after the flight = the heading whole.
"""
import sys, pathlib, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageDraw

html = pathlib.Path(sys.argv[1]).resolve(); target = Image.open(sys.argv[2]).convert("RGB")
out = pathlib.Path(sys.argv[3]).resolve(); out.mkdir(parents=True, exist_ok=True)
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)

FIG_S = 1333 / 1280                                   # the stage is 1333 px wide for the frame's 1280
EXPECT = {   # frame px (1280x720 frame coordinates) from Figma metadata / design context
  ".sg-fig .sg-card":   (76, 125, 1114, 456),
  ".sgf-scene":         (76, -33, 1114, 627),      # card padding origin (85,134) + (-9,-167)
  # [title-fly] Figma 956:2's places (386:17's were question 841,147 138x207; danda 97,139 219.473; comma 502,170 95x143; shadows
  # 141,303 132x69 / 473,270 142x64 / 857,306 115x69)
  ".sgf-question":      (85+488, 134+147, 120, 180),
  # [title-off] (2026-11-15) the frame's title art (.sgf-title, 85+251.58, 134+12.02, 593.83 x 109.99) is removed — see TITLE_BOX
  ".sgf-purn":          (85+818, 134+133, 208.527, 208.527),
  ".sgf-comma":         (85+177, 134+201, 82, 123),
  ".sgf-shadow.s1":     (85+858.53, 134+287.53, 127, 68),
  ".sgf-shadow.s2":     (85+149, 134+283, 129, 62),
  ".sgf-shadow.s3":     (85+499, 134+283, 106, 66),
  # [dun-chrome] the reference's cover controls, in frame px: the bird 208 stage px wide, 24 px left of and 12 px under the card's
  # bottom-left corner (its 560x550 file: 196.17 tall); the play button 140 stage px, centred, its bottom edge 2 stage px above the
  # card's bottom; the chip 70 stage px at 83 px from the card's left and 12 px under its bottom
  "#sgMascot":          (76 - 24 / FIG_S, 581 + 12 / FIG_S - 208 / FIG_S * 550 / 560, 208 / FIG_S, 208 / FIG_S * 550 / 560),
  "#sgBtn":             (76 + 1114 / 2 - 70 / FIG_S, 581 - 2 / FIG_S - 140 / FIG_S, 140 / FIG_S, 140 / FIG_S),   # centred on the CARD (76..1190), as the reference's is on its
  "#sgVo":              (76 + 83 / FIG_S, 581 + 12 / FIG_S - 70 / FIG_S, 70 / FIG_S, 70 / FIG_S),
}
TITLE_BOX = (85 + 251.58, 134 + 12.02, 593.83, 109.99)   # [title-off] where the title art stood (frame px); [title-text] the heading is there now
HEADING = "रुको , सोचो , चिह्न लगाओ ।"   # [title-text] the ask's own text: रुको , सोचो , चिह्न लगाओ ।
REF_RULE = (pathlib.Path(__file__).resolve().parent / "title_assets" / "ref_mtcg_sg_title.css").read_text(encoding="utf-8")
REF_SHADOW = REF_RULE[REF_RULE.index("text-shadow:") + len("text-shadow:"): REF_RULE.rindex(";")]
# [title-color] the shadow rings, generated: _reference() must give the reference rule's 98 parts; _colored() is the heading's list
import math, re
def _f(v):
    s = ("%.2f" % v).rstrip("0").rstrip("."); return "0" if s in ("-0", "") else s
def _ring(rx, ry, n, phase, dy, blur, col):
    return [f"{_f(rx * math.cos(math.radians(phase + k * 360 / n)))}px {_f(ry * math.sin(math.radians(phase + k * 360 / n)) + dy)}px "
            f"{(_f(blur) + 'px') if blur else '0'} {col}" for k in range(n)]
_SQ = 3.9 / 4.5
def _reference():
    return (_ring(4.5, 3.9, 32, 0, 0, 0, "#fff") + _ring(2.475, 2.145, 16, 11.25, 0, 0, "#fff") + _ring(4.5, 3.9, 32, 0, 4.8, .8, "#2F82DE")
            + _ring(2.475, 2.145, 16, 11.25, 4.8, 0, "#2F82DE") + ["0 4.8px 0 #2F82DE", "0 8px 12px rgba(0,40,120,.26)"])
def _colored(m, maroon, blue):
    return (_ring(m, _SQ * m, 32, 0, 0, 0, maroon) + _ring(.55 * m, .55 * _SQ * m, 16, 11.25, 0, 0, maroon)
            + _ring(m + 4.5, _SQ * m + 3.9, 32, 0, 0, 0, "#fff") + _ring(m + 2.475, _SQ * m + 2.145, 24, 7.5, 0, 0, "#fff")
            + _ring(m + 4.5, _SQ * m + 3.9, 32, 0, 4.8, .8, blue) + _ring(m + 2.475, _SQ * m + 2.145, 24, 7.5, 4.8, 0, blue)
            + [f"0 4.8px 0 {blue}", f"0 {_f(8 + _SQ * m)}px 12px rgba(0,40,120,.26)"])
_norm = lambda s: re.sub(r"\b0px\b", "0", re.sub(r"\s+", " ", s.strip()))
REF_REGEN_OK = [_norm(x) for x in REF_SHADOW.split(",\n")] == [_norm(x) for x in _reference()]
# [title-stroke-off] no outline any more (it went 3.5 -> 2.5 -> 2.0 px in [title-color]/[title-stroke], then was removed): the reference
# rule's own 98 parts with the picture's blue
HEAD_SHADOW = ", ".join(x.replace("#2F82DE", "#0345A1") for x in _reference())
HEAD_INFO = """(refShadow) => { const all = document.querySelectorAll('.sgf-heading:not(.sgf-hclone)'); if (all.length !== 1) return null;
  const e = all[0], cs = getComputedStyle(e), card = document.querySelector('.sg-fig .sg-card'), cr = card.getBoundingClientRect();
  const st = document.getElementById('stage'), ss = st.getBoundingClientRect().width / st.offsetWidth;
  const rg = document.createRange(); rg.selectNodeContents(e); const q = rg.getBoundingClientRect();
  const probe = document.createElement('div'); probe.style.textShadow = refShadow; document.body.append(probe); const refSh = getComputedStyle(probe).textShadow; probe.remove();
  const tops = ['.sgf-purn img', '.sgf-comma', '.sgf-question'].map(s => document.querySelector(s).getBoundingClientRect().top);
  const anims = e.getAnimations({ subtree: true }).map(a => a.animationName || a.transitionProperty || 'anim');   // incl. its ::after fill layer
  for (let x = e.parentElement; x && x.id !== 'startGate'; x = x.parentElement) anims.push(...x.getAnimations().map(a => a.animationName || a.transitionProperty || 'anim'));
  const a = getComputedStyle(e, '::after');
  const after = { content: a.content, clip: a.webkitBackgroundClip || a.backgroundClip, fill: a.webkitTextFillColor, bg: a.backgroundImage, pos: a.position, top: a.top, w: a.width,
    h: a.height, pt: a.paddingTop, lh: a.lineHeight, ff: a.fontFamily, fw: a.fontWeight, fsz: a.fontSize, ls: a.letterSpacing, ws: a.wordSpacing, sh: a.textShadow, ta: a.textAlign };
  return { dataText: e.dataset.text, label: e.getAttribute('aria-label'), after, inCard: e.parentElement === card, afterChars: !!(e.compareDocumentPosition(document.querySelector('.sgf-comma')) & Node.DOCUMENT_POSITION_PRECEDING),
    txt: e.textContent, text: [q.left, q.top, q.width, q.height], ff: cs.fontFamily, fw: cs.fontWeight, fsz: cs.fontSize, lh: cs.lineHeight, col: cs.color,
    ls: cs.letterSpacing, ws: cs.wordSpacing, nowrap: cs.whiteSpace === 'nowrap', shadowOk: cs.textShadow === refSh && refSh !== 'none',
    font: document.fonts.check('800 64px "Baloo 2"'), stagePx: e.getBoundingClientRect().height / ss, oneLine: q.height / ss < 110,
    centreOff: ((q.left + q.width / 2) - (cr.left + cr.width / 2)) / ss, clear: (Math.min(...tops) - (q.top + q.height)) / ss,
    anim: cs.animationName, trans: cs.transitionDuration, anims }; }"""
HEAD_CLIP = """() => { const e = document.querySelector('.sg-card > .sgf-heading:not(.sgf-hclone)'), r = e.getBoundingClientRect(); return [r.left - 30, r.top - 30, r.right + 30, r.bottom + 30]; }"""   # [title-fly]
BOXES ="""(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
  if (!e) { o[s] = null; continue; } const r = e.getBoundingClientRect(); o[s] = [r.left, r.top, r.width, r.height]; } return o; }"""
# [title-punct] the heading's punctuation: each glyph's ink box in the heading's own px (as cover_fly_js measures it), the heading's
# place and scale, its class and computed clip-path
PUNCT_INFO = """() => { const h = document.querySelector('.sg-card > .sgf-heading'); const tn = [...h.childNodes].find(n => n.nodeType === 3);
  const cs = getComputedStyle(h), hr = h.getBoundingClientRect(), u = hr.width / h.offsetWidth, lh = parseFloat(cs.lineHeight);
  const x = document.createElement('canvas').getContext('2d'); x.font = cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily; const ink = [];
  for (let i = 0; i < tn.data.length; i++) { const ch = tn.data[i]; if (ch !== ',' && ch !== '।') continue;
    const rg = document.createRange(); rg.setStart(tn, i); rg.setEnd(tn, i + 1); const rr = rg.getBoundingClientRect(), m = x.measureText(ch);
    const ox = (rr.left - hr.left) / u, base = (lh - (m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)) / 2 + m.fontBoundingBoxAscent;
    ink.push([ch, ox - m.actualBoundingBoxLeft, base - m.actualBoundingBoxAscent, ox + m.actualBoundingBoxRight, base + m.actualBoundingBoxDescent]); }
  return { off: h.classList.contains('sgf-punct-off'), clip: cs.clipPath, hl: hr.left, ht: hr.top, u, ink }; }"""
FREEZE = """() => { document.querySelectorAll('.sg-fx, .sgf-eyes, .sg-sky, .sg-glow, #sgMascot, #sgSwiftieAnim').forEach(e => e.style.visibility = 'hidden');
  document.getAnimations().forEach(a => a.pause()); }"""
PUNCT_REC = """() => { const h = document.querySelector('.sg-card > .sgf-heading'); window.__punctRec = [];
  const snap = () => window.__punctRec.push({ t: performance.now(), off: h.classList.contains('sgf-punct-off'), clip: getComputedStyle(h).clipPath,
    cw: [...document.querySelectorAll('.sgf-mergew')].map(w => { const a = w.getAnimations()[0], c = w.firstElementChild;
      return { p: a ? a.effect.getComputedTiming().progress : null, op: +getComputedStyle(w).opacity, l: c ? parseFloat((c.style.clipPath.match(/polygon\\(([-\\d.]+)px/) || [])[1]) : null }; }) });
  snap(); new MutationObserver(snap).observe(h, { attributes: true, attributeFilter: ['style', 'class'] }); }"""
def holes_of(clip):
    """the holes of an even-odd clip path: [l, t, r, b] per hole (the first rectangle is the outer one)"""
    if not clip or not clip.startswith("path(evenodd"): return None
    rects = []
    for sub in re.findall(r"M\s*([-\d.]+)\s+([-\d.]+)\s*H\s*([-\d.]+)\s*V\s*([-\d.]+)\s*H\s*[-\d.]+\s*Z", clip):
        l, t, r, b = map(float, sub); rects.append([l, t, r, b])
    return rects[1:] if rects and rects[0][:2] == [-200.0, -200.0] else None

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--mute-audio"])          # default policy: autoplay blocked
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    bad = []; pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(4000)
    check("with autoplay blocked the welcome has not played: the play button is NOT on the page yet, the chip is off",
          pg.evaluate("getComputedStyle(document.getElementById('sgBtn')).display === 'none' && document.getElementById('sgVo').classList.contains('sg-vo-off')"))
    pi0 = pg.evaluate(PUNCT_INFO)
    pg.evaluate("document.getElementById('sgBtn').classList.add('ready')"); pg.wait_for_timeout(700)   # to measure its box
    pi1 = pg.evaluate(PUNCT_INFO)
    check("[title-punct] a play button that comes with no flight (here the welcome never sounded) shows the heading whole at once: its three holes, then no clip",
          len(holes_of(pi0["clip"]) or []) == 3 and pi0["off"] and not pi1["off"] and pi1["clip"] == "none" and pg.evaluate("window.__sgFly.phase") == "wait",
          (pi0["off"], len(holes_of(pi0["clip"]) or []), pi1["off"], pi1["clip"][:40]))
    # [cover-fx] / [cover-eyes] the added light and the eye canvases sit on top of the frame's art: their place is checked here, and
    # they are hidden for the Figma comparison below (the frame has neither)
    fx = pg.evaluate("""() => { const fx = document.querySelector('.sg-card > .sg-fx'), sc = document.querySelector('.sgf-scene'), c = document.querySelector('.sg-card').getBoundingClientRect();
      if (!fx || !sc) return null; const r = fx.getBoundingClientRect(), k = c.width / 1114;
      return { afterScene: sc.nextElementSibling === fx, d: Math.max(Math.abs(r.left - (c.left + 9 * k)), Math.abs(r.top - (c.top + 9 * k)), Math.abs(r.width - (c.width - 18 * k)), Math.abs(r.height - (c.height - 18 * k))),
               parts: ['.sg-sun', '.sg-flare2 .fl-big', '.sg-flare2 .fl-violet', '.sg-flare2 .fl-haze', '.sg-flare2 .fl-glint', 'canvas.sg-dust'].map(q => !!fx.querySelector(q)) }; }""")
    check("the reference's light layer (.sg-fx: the sun anchor, the four flare discs, the dust canvas) sits right after the scene, filling the card inside its 9 px frame ([cover-fx])",
          fx is not None and fx["afterScene"] and fx["d"] <= 1.0 and all(fx["parts"]), fx)
    eyes = pg.evaluate("""() => ['.sgf-purn img', '.sgf-comma', '.sgf-question'].map(sel => { const img = document.querySelector(sel), ir = img.getBoundingClientRect();
      let best = null; for (const c of document.querySelectorAll('.sgf-eyes')) { const r = c.getBoundingClientRect(); const d = Math.max(Math.abs(r.left - ir.left), Math.abs(r.top - ir.top), Math.abs(r.width - ir.width), Math.abs(r.height - ir.height)); if (best === null || d < best) best = d; }
      return best; }); """)
    check("a live-eyes canvas covers each of the three characters' pictures (the danda, the comma, the question mark: boxes equal within 1 px) ([cover-eyes])",
          len(eyes) == 3 and all(d is not None and d <= 1.0 for d in eyes), eyes)
    pg.evaluate("document.querySelectorAll('.sg-fx, .sgf-eyes').forEach(e => e.style.visibility = 'hidden')"); pg.wait_for_timeout(150)
    shot = out / "title_1280.png"; pg.screenshot(path=str(shot))
    boxes = pg.evaluate(BOXES, list(EXPECT))
    print("== geometry (rendered vs frame, px) ==")
    worst = 0
    for s, exp in EXPECT.items():
        got = boxes[s]; d = max(abs(g - e) for g, e in zip(got, exp)) if got else 999; worst = max(worst, d)
        print(f"  {'OK ' if d <= 1.0 else 'OFF'} {s:20s} got {[round(v,1) for v in got] if got else None}  frame {[round(v, 2) for v in exp]}  max|d|={d:.2f}")
    check("every element within 1 px of its place (the frame's art; the reference's bird, play button and chip)", worst <= 1.0, "worst %.2f px" % worst)
    # pixel diff inside the card only, masking the reference's controls where they overlap it
    img = Image.open(shot).convert("RGB")
    mask = Image.new("L", img.size, 0); dr = ImageDraw.Draw(mask)
    l, t, w, h = EXPECT[".sg-fig .sg-card"]; dr.rectangle([l, t, l + w, t + h], fill=255)
    for s in ("#sgBtn", "#sgVo", "#sgMascot"):
        l, t, w, h = boxes[s]; dr.rectangle([l - 2, t - 2, l + w + 2, t + h + 2], fill=0)
    l, t, w, h = TITLE_BOX; dr.rectangle([l - 2, t - 2, l + w + 2, t + h + 2], fill=0)   # [title-off] the render still has the title there
    hd = pg.evaluate(HEAD_INFO, HEAD_SHADOW)
    if hd:   # [title-text] the render has no heading: its text box, widened by 18 px for the outline, the rim, the blue edge and the drop
        l, t, w, h = hd["text"]; dr.rectangle([l - 18, t - 18, l + w + 18, t + h + 18], fill=0)
    # [title-off] the frame's title art stays gone: no title art element, and the hidden #sgTitle still takes no space
    gone = pg.evaluate("[document.querySelectorAll('.sgf-title, img[src*=\"title_art\"]').length, (document.getElementById('sgTitle') || {}).offsetWidth || 0]")
    check("[title-off] the frame's title art (रुको सोचो चिन्ह लगाओ) is not on the page, and the hidden #sgTitle still takes no space", gone == [0, 0], gone)
    # [title-text] the heading in the reference cover's title look
    check("[title-text] one heading in the card, above the characters' layers, reading exactly the ask's text (रुको , सोचो , चिह्न लगाओ ।: the spaces before the commas and the । kept); "
          "[title-color] its fill layer's text (data-text) and its aria-label are that text too",
          hd is not None and hd["inCard"] and hd["afterChars"] and hd["txt"] == HEADING and hd["dataText"] == HEADING and hd["label"] == HEADING
          and hd["after"]["content"] == '"' + HEADING + '"', hd and (hd["txt"], hd["inCard"], hd["afterChars"], hd["dataText"] == HEADING, hd["label"] == HEADING, hd["after"]["content"][:12]))
    check("[title-text] ...in the reference cover's title type, kept: Baloo 2 800 (loaded) at 64 stage px, line-height 1.15, letter-spacing .5px, word-spacing 14px",
          hd is not None and hd["ff"].startswith('"Baloo 2"') and hd["fw"] == "800" and hd["fsz"] == "64px" and hd["lh"] == "73.6px"
          and hd["ls"] == "0.5px" and hd["ws"] == "14px" and hd["font"] and abs(hd["stagePx"] - 73.6) < 0.1,
          hd and {k: hd[k] for k in ("ff", "fw", "fsz", "lh", "ls", "ws", "font", "stagePx")})
    af = hd["after"] if hd else {}
    stops = ("rgb(240, 132, 0)", "rgb(234, 115, 0)", "rgb(224, 98, 0)", "rgb(212, 85, 0)", "rgb(200, 73, 0)", "rgb(184, 60, 0)")   # [title-dark3]
    check("[title-color] ...in the picture's colours: the text (the fill's middle colour, #E06200 since [title-dark3]) under its fill layer — the same line (same font, size, spacing, centring; "
          "24 px of room round the 73.6 px line) in the orange gradient, [title-dark3]'s darker one #F08400 > #EA7300 > #E06200 > #D45500 > #C84900 > #B83C00, clipped to the letters, no shadow",
          hd is not None and hd["col"] == "rgb(224, 98, 0)" and af["clip"] == "text" and af["fill"] == "rgba(0, 0, 0, 0)" and af["bg"].startswith("linear-gradient(")
          and all(s in af["bg"] for s in stops) and af["pos"] == "absolute" and af["top"] == "-24px" and af["w"] == "1096px" and abs(float(af["h"][:-2]) - 121.6) <= 1 / 64 and af["pt"] == "24px"
          and af["lh"] == "73.6px" and af["ff"] == hd["ff"] and af["fw"] == "800" and af["fsz"] == "64px" and af["ls"] == "0.5px" and af["ws"] == "14px" and af["ta"] == "center"
          and af["sh"] == "none", hd and (hd["col"], af))
    check("[title-stroke-off] ...its rim and edge with no outline: the text-shadow = the reference rule's own 98 parts (white ring, blue edge, soft drop) "
          "with the picture's blue #0345A1, exactly (the generator reproduces the reference rule first)",
          REF_REGEN_OK and hd is not None and hd["shadowOk"], (REF_REGEN_OK, hd and hd["shadowOk"]))
    check("[title-text] ...on one line, centred on the card (within 1 stage px), in the sky clear above the three characters' pictures",
          hd is not None and hd["nowrap"] and hd["oneLine"] and abs(hd["centreOff"]) <= 1 and hd["clear"] > 10, hd and {k: hd[k] for k in ("nowrap", "oneLine", "centreOff", "clear")})
    reg = img.crop(tuple(round(v) for v in (hd["text"][0] - 10, hd["text"][1], hd["text"][0] + hd["text"][2] + 10, hd["text"][1] + hd["text"][3]))) if hd else Image.new("RGB", (1, 1))
    px = list(reg.getdata())
    # [title-dark] the letters are gold-to-orange now (#FFA800 .. #E25400): counted as warm letter pixels
    yellow = sum(1 for (r, g, b_) in px if r > 175 and 50 < g < 170 and b_ < 60); maroon = sum(1 for (r, g, b_) in px if 35 < r < 115 and g < 35 and b_ < 35)   # [title-dark3] warm letters down to #B83C00
    white = sum(1 for (r, g, b_) in px if min(r, g, b_) > 240); blue = sum(1 for (r, g, b_) in px if r < 40 and g < 110 and b_ > 120)
    check("[title-stroke-off] ...painted: its gold-to-orange letters, white rim and deep-blue edge show in the screenshot, and no maroon outline is left",
          yellow > 3000 and maroon < 100 and white > 1000 and blue > 300, (yellow, maroon, white, blue, reg.size))
    # [title-dark] readable against the white rim the letters sit on: every colour of the fill at least 1.9 : 1, its darkest at least 3 : 1
    def _cr(rgb):
        c = [v / 255 for v in rgb]; c = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in c]
        return 1.05 / (.2126 * c[0] + .7152 * c[1] + .0722 * c[2] + .05)
    grad = [tuple(int(v) for v in m) for m in re.findall(r"rgb\((\d+), (\d+), (\d+)\)", af.get("bg", ""))]
    crs = [round(_cr(c), 2) for c in grad]
    check("[title-dark3] ...and readable on its white rim: every colour of the fill at least 2.6 : 1 against white, the darkest at least 5.5 : 1 "
          "([title-dark] asked 1.9 and 3, [title-dark2] 2.2 and 4.5)",
          bool(crs) and min(crs) >= 2.6 and max(crs) >= 5.5, crs)
    check("[title-text] ...with no animation or transition of its own (nor on its fill layer), nor on the card around it", hd is not None and hd["anim"] == "none" and hd["trans"] == "0s" and not hd["anims"],
          hd and (hd["anim"], hd["trans"], hd["anims"]))
    reg.save(out / "title_heading_region.png")
    diff = ImageChops.difference(img, target).convert("L")
    vals = [d for d, m in zip(diff.getdata(), mask.getdata()) if m]
    big = sum(1 for v in vals if v > 40)
    print("== pixel diff vs Figma render, inside the card (the controls masked) ==")
    print("  mean |diff| %.2f / 255   pixels off by >40: %d of %d (%.2f%%)" % (sum(vals) / len(vals), big, len(vals), 100 * big / len(vals)))
    check("the card is the frame's (inside it, under 1 % of pixels off by more than 40 levels)", big / len(vals) < 0.01)
    heat = diff.point(lambda v: 255 if v > 40 else v * 3); heat.save(out / "title_diff_heat.png")
    side = Image.new("RGB", (1280, 1440)); side.paste(target, (0, 0)); side.paste(img, (0, 720)); side.save(out / "figma_vs_build.png")
    check("no page errors, no failed requests", not errs and not bad, (errs[:3], bad[:5]))
    # [title-fly2] the heading before any flight (the flight now runs inside the welcome): the still page at the autoplay run's viewport
    p2 = b.new_page(viewport={"width": 1333, "height": 750}); p2.goto(html.as_uri()); p2.wait_for_timeout(4000)
    p2.evaluate("document.querySelectorAll('.sg-fx').forEach(e => e.style.visibility = 'hidden')"); p2.wait_for_timeout(100)
    p2.screenshot(path=str(out / "fly_before.png"))
    fly_before = {"clip": p2.evaluate(HEAD_CLIP), "fly": p2.evaluate("window.__sgFly ? window.__sgFly.phase : null")}
    # [title-punct] the still heading: its three holes on the glyphs' ink boxes, then three shots with every moving layer stopped -
    # the heading as it stands, the heading whole (the class taken off), no heading at all
    pi = p2.evaluate(PUNCT_INFO); css_holes = holes_of(pi["clip"])
    want = [[l - 14, t - 12, r + 14, b + 24] for (_, l, t, r, b) in pi["ink"]]
    check("[title-punct] before the symbols fly the heading's , , । are cut out: .sgf-punct-off, an even-odd clip-path with three holes, each on its glyph's "
          "ink box + 14 px each side, 12 above, 24 below (= its landing clone's region; within 0.01 px)",
          pi["off"] and [c for c, *_ in pi["ink"]] == [",", ",", "।"] and css_holes is not None and len(css_holes) == 3
          and max(abs(a - b) for h, w in zip(css_holes, want) for a, b in zip(h, w)) <= 0.01, (pi["off"], css_holes, [[round(v, 2) for v in w] for w in want]))
    p2.evaluate(FREEZE); p2.wait_for_timeout(150); p2.screenshot(path=str(out / "punct_holes.png"))
    p2.evaluate("document.querySelector('.sg-card > .sgf-heading').classList.remove('sgf-punct-off')"); p2.wait_for_timeout(150); p2.screenshot(path=str(out / "punct_whole.png"))
    p2.evaluate("document.querySelector('.sg-card > .sgf-heading').style.visibility = 'hidden'"); p2.wait_for_timeout(150); p2.screenshot(path=str(out / "punct_none.png"))
    p2.close()
    import numpy as np
    A = lambda n: np.asarray(Image.open(out / n).convert("RGB")).astype(int)
    PH, PW, PN = A("punct_holes.png"), A("punct_whole.png"), A("punct_none.png")
    yy, xx = np.mgrid[0:PH.shape[0], 0:PH.shape[1]]; lx = (xx + 0.5 - pi["hl"]) / pi["u"]; ly = (yy + 0.5 - pi["ht"]) / pi["u"]
    def in_rects(rs, grow):
        m = np.zeros(PH.shape[:2], bool)
        for l, t, r, b in rs: m |= (lx >= l - grow) & (lx <= r + grow) & (ly >= t - grow) & (ly <= b + grow)
        return m
    hole_m = in_rects(css_holes or [], 0); edge = in_rects(css_holes or [], 1.5) & ~in_rects(css_holes or [], -1.5)   # pixels split by a hole's edge
    region = (lx >= -40) & (lx <= 1136) & (ly >= -40) & (ly <= 120)
    d_hw = np.abs(PH - PW).max(axis=2); d_hn = np.abs(PH - PN).max(axis=2); d_wn = np.abs(PW - PN).max(axis=2)
    out_m, in_m = region & ~hole_m & ~edge, hole_m & ~edge
    ring = in_rects(css_holes or [], 2) & ~in_rects(css_holes or [], -2)
    check("[title-punct] ...so the symbols are not there and nothing else changes: inside the holes not a pixel of the heading (= no heading), outside them "
          "the heading whole, pixel for pixel; no heading paint crosses a hole's edge (no letter cut, nothing of a symbol left outside: <= 2 levels there); "
          "and the holes did hold the symbols (their pixels differ from the empty page)",
          bool(in_m.any()) and int(d_hn[in_m].max()) == 0 and int(d_hw[out_m].max()) == 0 and int(d_wn[ring].max()) <= 2 and int((d_wn[hole_m] > 40).sum()) > 1500,
          (int(d_hn[in_m].max()) if in_m.any() else None, int(d_hw[out_m].max()), int(d_wn[ring].max()), int((d_wn[hole_m] > 40).sum())))
    b.close()

    # ---- the welcome, the play button, the chip, the bird, the sky ----
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(html.as_uri())
    # [cover-sky] the button's computed opacity at the very moment .ready lands (synchronous in the observer: the reveal's 0 % frame)
    pg.evaluate("""() => { const btn = document.getElementById('sgBtn'); window.__readyOpacity = null;
      new MutationObserver(() => { if (window.__readyOpacity === null && btn.classList.contains('ready')) window.__readyOpacity = getComputedStyle(btn).opacity; })
        .observe(btn, { attributes: true, attributeFilter: ['class'] }); }""")
    pg.evaluate(PUNCT_REC)   # [title-punct] every change of the heading's class / style, with the glyph clones' state at that moment
    STATE ="""() => { const a = (typeof currentAudio !== 'undefined') ? currentAudio : null; const btn = document.getElementById('sgBtn'), vo = document.getElementById('sgVo'), bird = document.getElementById('sgMascot');
      return { t: performance.now(), vo: !!(a && !a.paused && !a.ended && isPlaying), src: a ? a.src.split('/').pop().split('?')[0] : null,
               btn: getComputedStyle(btn).display !== 'none', ready: btn.classList.contains('ready'), breathe: btn.classList.contains('sg-breathe'), btnAnim: getComputedStyle(btn).animationName,
               chipOff: vo.classList.contains('sg-vo-off'), bird: (bird.src || '').split('/').pop().split('?')[0], loaded: document.body.classList.contains('loaded'),
               hd: (() => { const e = document.querySelector('.sg-card > .sgf-heading:not(.sgf-hclone)'); if (!e) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.width, r.height, e.getAnimations().length]; })(),
               fly: window.__sgFly ? window.__sgFly.phase : null,   // [title-fly] the flight's phase and the two flyers' boxes, the question mark's box and gaze
               sym: ['.sgf-purn', '.sgf-commaw:not(.sgf-twin)', '.sgf-question'].map(s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.left * 10) / 10, Math.round(r.top * 10) / 10, Math.round(r.width * 10) / 10]; }),
               gz: window.SGEyes ? SGEyes.debug().map(f => [f.name, f.g.x, f.g.y]) : null }; }"""
    # [title-fly] the samples run on until the flight is over (at most 45 s); the heading region is shot (the card's light layer hidden)
    # after the flight (the before shot: the still page in the first browser); the three glyph clones' last keyframes are read as the flight starts
    CLONES = """() => [...document.querySelectorAll('.sgf-mergew')].map(w => { const a = w.getAnimations()[0], k = a ? a.effect.getKeyframes() : [], c = w.firstElementChild;
      return { last: k.length ? [k[k.length - 1].transform, k[k.length - 1].opacity] : null, clip: c ? c.style.clipPath : null, text: c ? c.dataset.text : null, hidden: w.getAttribute('aria-hidden') }; })"""
    def head_shot(path):
        pg.evaluate("document.querySelectorAll('.sg-fx').forEach(e => e.style.visibility = 'hidden')"); pg.wait_for_timeout(60)
        pg.screenshot(path=str(path)); pg.evaluate("document.querySelectorAll('.sg-fx').forEach(e => e.style.visibility = '')")
    samples = []; clones = None; fly_st = None
    while len(samples) < 150 or (samples[-1]["fly"] not in ("done", "error", None) and len(samples) < 450):   # None: a build without the flight
        s = pg.evaluate(STATE); samples.append(s)
        if clones is None and s["fly"] not in (None, "wait"): clones = pg.evaluate(CLONES); fly_st = pg.evaluate("JSON.parse(JSON.stringify(window.__sgFly))")
        pg.wait_for_timeout(100)
    fly_end = pg.evaluate("window.__sgFly ? [window.__sgFly.doneAt || null, window.__sgFly.fit || null] : [null, null]")
    first_vo = next((s for s in samples if s["vo"] and s["src"] == "vo_landing.ogg"), None)
    during = [s for s in samples if s["vo"] and s["src"] == "vo_landing.ogg"]
    after = next((s for s in samples if first_vo and s["t"] > first_vo["t"] and not s["vo"] and s["ready"]), None)
    check("the welcome plays by itself once the loader fades", first_vo is not None and first_vo["loaded"], round(first_vo["t"]) if first_vo else None)
    check("while the welcome plays the play button is absent and the chip is off", during and all(not s["btn"] and s["chipOff"] for s in during), len(during))
    check("once the welcome has ended the play button is in (.ready) and the chip is live", after is not None and not after["chipOff"], round(after["t"] - first_vo["t"]) if (after and first_vo) else None)
    late = [s for s in samples if after and s["t"] > after["t"] + 900]
    check("the play button then breathes (.sg-breathe, sgBtnPulse)", late and all(s["breathe"] and s["btnAnim"] == "sgBtnPulse" for s in late), len(late))
    shown = [s for s in samples if s["loaded"]]; hboxes = {tuple(round(v, 3) for v in s["hd"][:4]) for s in shown if s["hd"]}
    check("[title-text] the heading never moves: one box through the welcome and the play button's entrance, no animation on it, in every sample",
          shown and all(s["hd"] and s["hd"][4] == 0 for s in shown) and len(hboxes) == 1, (len(shown), len(hboxes), shown[0]["hd"] if shown else None))
    # ---- [title-fly] the symbols fly into the heading at the end of the welcome ----
    sym0 = next((s["sym"] for s in samples if s["loaded"]), None)
    fly_first = next((s for s in samples if s["fly"] not in (None, "wait")), None)
    fly_done = next((s for s in samples if s["fly"] == "done"), None)
    # [title-fly2] the flight runs inside the welcome: it waits until the line is sounding, starts at once, is over while the line still
    # plays, and the play button comes only after both (at the line's end, as before)
    check("[title-fly2] nothing flies before the welcome sounds: the danda and the comma stand still until the line starts",
          first_vo is not None and sym0 and all(s["fly"] == "wait" and s["sym"][:2] == sym0[:2] for s in samples if s["loaded"] and s["t"] < first_vo["t"]), (first_vo and round(first_vo["t"]), sym0))
    check("[title-fly2] ...the flight starts as the welcome sounds (within 1.2 s of its first sample: the line's clock past 0.25 s) and is over (the last glyph copy faded) while the welcome is still playing",
          fly_first is not None and first_vo is not None and -100 <= fly_first["t"] - first_vo["t"] <= 1200 and fly_done is not None and fly_done["vo"] and fly_done["src"] == "vo_landing.ogg"
          and after is not None and fly_end[0] is not None and fly_end[0] < after["t"],
          (fly_first and first_vo and round(fly_first["t"] - first_vo["t"]), fly_done and (fly_done["vo"], fly_done["src"]), after and fly_end[0] and round(after["t"] - fly_end[0]), fly_end[1], fly_st and fly_st.get("err")))
    check("[title-fly2] ...and only after that the play button appears, at the welcome's end as before (never during the flight)",
          after is not None and all(s["fly"] == "done" for s in samples if s["ready"]) and not any(s["ready"] for s in during), (after and round(after["t"] - first_vo["t"]),))
    fl = fly_st["flights"] if fly_st else []
    names = [(f["name"], f["ch"]) for f in fl]
    check("[title-fly] three flights: the blue danda into the heading's ।, the green comma into its second comma and the comma's twin into its first",
          names == [("purn", "।"), ("comma", ","), ("comma-twin", ",")] and fl[0]["glyph"]["cx"] > fl[1]["glyph"]["cx"] > fl[2]["glyph"]["cx"], names)
    check("[title-fly] ...each ends as the title's own glyph: a clone of the heading (its text, hidden from readers) clipped round that glyph, its last frame exactly "
          "on it (no offset, scale 1, opaque)",
          clones is not None and len(clones) == 3 and all(c["last"] and c["last"][0] == "translate(0px, 0px) scale(1)" and float(c["last"][1]) == 1 and (c["clip"] or "").startswith("polygon(")
          and c["text"] == HEADING and c["hidden"] == "true" for c in clones), clones)
    pg.wait_for_timeout(300); head_shot(out / "fly_after.png"); shot_after = pg.evaluate(HEAD_CLIP)
    cr = pg.evaluate("(() => { const c = document.querySelector('.sg-fig .sg-card'), r = c.getBoundingClientRect(); return [r.left, r.top, r.width / c.offsetWidth]; })()")
    ia = Image.open(out / "fly_after.png").convert("RGB"); offs = []
    for g in (fly_st or {}).get("glyphs") or []:
        L, T_, R_, B_ = (cr[0] + (g["l"] + 9) * cr[2], cr[1] + (g["t"] + 9) * cr[2], cr[0] + (g["r"] + 9) * cr[2], cr[1] + (g["b"] + 9) * cr[2])
        xs, ys = [], []
        for y in range(int(T_ - 10), int(B_ + 10)):
            for x in range(int(L - 10), int(R_ + 10)):
                r_, g_, b_ = ia.getpixel((x, y))
                if r_ > 170 and 50 < g_ < 190 and b_ < 70: xs.append(x); ys.append(y)   # the fill's letter pixels ([title-dark3]: to #B83C00)
        offs.append(round(max(abs(min(xs) - L), abs(max(xs) + 1 - R_), abs(min(ys) - T_), abs(max(ys) + 1 - B_)), 2) if xs else 99)
    check("[title-fly] ...the glyph boxes it flew to sit on the heading's painted ,  ,  । (within 2 px)", len(offs) == 3 and max(offs) <= 2, offs)
    tS = 0.1 + 0.7 * math.acos(1 - 2 * 0.42) / math.pi
    gz = lambda s, n: next(v for v in s["gz"] if v[0] == n)
    if len(fl) == 3:
        sb = [s for s in samples if s["gz"] and fl[0]["start"] + 600 <= s["t"] <= fl[0]["start"] + 2400]
        sg = [s for s in samples if s["gz"] and fl[1]["start"] + fl[1]["ms"] * tS + 300 <= s["t"] <= fl[1]["start"] + fl[1]["ms"] * 0.8]
    else: sb = sg = []
    qb = sum(1 for s in sb if gz(s, "question")[1] > 0.3); pb = sum(1 for s in sb if gz(s, "purn")[2] < -0.15); qg = sum(1 for s in sg if gz(s, "question")[1] < -0.2)
    check("[title-fly] the question mark watches: it looks right while the danda flies (and the danda looks up at the title), left while the comma's halves fly",
          sb and sg and qb >= 0.8 * len(sb) and pb >= 0.6 * len(sb) and qg >= 0.8 * len(sg), (qb, pb, len(sb), qg, len(sg)))
    end = pg.evaluate("[[...document.querySelectorAll('.sgf-purn, .sgf-commaw')].map(e => getComputedStyle(e).visibility), document.querySelectorAll('.sgf-mergew, .sgf-burst').length]")
    check("[title-fly] at the end the danda and the comma (and its twin) are gone from the ground, the question mark stands where it stood, no clone or sparkle is left",
          end[0] == ["hidden", "hidden", "hidden"] and end[1] == 0 and sym0 and samples[-1]["sym"][2] == sym0[2], (end, sym0 and sym0[2], samples[-1]["sym"][2]))
    # [title-punct] the holes through the welcome: three until the flight (the ones it re-measures = the CSS's), each closed only once its
    # clone has settled (>= 95 % of its animation: exactly 1x, opaque), the । first, then the two commas; at the end no clip at all
    rec = pg.evaluate("window.__punctRec || []")
    hs = [holes_of(r["clip"]) if r["clip"] != "none" else [] for r in rec]
    closes, bad_close = [], []
    for k in range(1, len(rec)):
        if hs[k] is None or hs[k - 1] is None: bad_close.append(("unreadable", k)); continue
        gone = [h for h in hs[k - 1] if not any(abs(h[0] - g[0]) < 0.02 for g in hs[k])]
        for h in gone:
            cl = [c for c in rec[k]["cw"] if c["l"] is not None and abs(c["l"] - h[0]) < 0.02]
            closes.append((round(h[0], 2), round(rec[k]["t"]), cl and round(cl[0]["p"], 3)))
            if not cl or cl[0]["p"] is None or cl[0]["p"] < 0.95 or cl[0]["op"] < 0.999: bad_close.append((round(h[0], 2), cl))
    first_fly = next((k for k, r in enumerate(rec) if not r["off"]), None)
    same = first_fly is not None and hs[0] and hs[first_fly] and len(hs[first_fly]) == 3 and max(abs(a - b) for h, w in zip(hs[0], hs[first_fly]) for a, b in zip(h, w)) <= 0.02
    check("[title-punct] through the welcome the , , । stay hidden until their symbols land: three holes until the flight starts (the holes it measures = the CSS's), "
          "each closed only when its clone has settled on the glyph (its animation at >= 95 %, opaque) - the । first, then the two commas - and no clip at all at the end",
          bool(rec) and rec[0]["off"] and len(hs[0] or []) == 3 and same and not bad_close and len(closes) == 3
          and css_holes is not None and closes[0][0] == round(css_holes[2][0], 2) and {c[0] for c in closes[1:]} == {round(css_holes[0][0], 2), round(css_holes[1][0], 2)}
          and rec[-1]["clip"] == "none" and not rec[-1]["off"] and pg.evaluate("getComputedStyle(document.querySelector('.sg-card > .sgf-heading')).clipPath") == "none",
          (len(rec), closes, bad_close, same, rec[-1]["clip"][:30] if rec else None))
    moved, dv, inner, iv = 0, [0], 0, [0]
    shot_before = fly_before["clip"] if fly_before else None   # [title-fly2] the still page (autoplay blocked, same viewport): the heading before any flight
    if shot_before:
        box = tuple(round(v) for v in shot_before)
        hb = Image.open(out / "fly_before.png").convert("RGB").crop(box); hn = ia.crop(box)
        hw = Image.open(out / "punct_whole.png").convert("RGB").crop(box)
        # [title-punct] the holes (+2 px) are left out of the before/after comparison; inside them the heading after the flight = the heading whole
        hm = Image.fromarray((in_rects(css_holes or [], 2.0).astype("uint8") * 255)).crop(box)
        dv = [v for v, m in zip(ImageChops.difference(hb, hn).convert("L").getdata(), hm.getdata()) if not m]; moved = sum(1 for v in dv if v > 40)
        iv = [v for v, m in zip(ImageChops.difference(hw, hn).convert("L").getdata(), hm.getdata()) if m]; inner = sum(1 for v in iv if v > 40)
    check("[title-fly] the heading is untouched by the flight: the same box in every sample (above) and the same pixels before and after it (under 0.3 % off by > 40) "
          "[title-punct] outside the three holes; inside them, after the flight, the title's own , , । (= the heading whole, under 0.3 % off by > 40)",
          shot_before is not None and shot_after == shot_before and moved / len(dv) < 0.003 and len(iv) > 1000 and inner / len(iv) < 0.003,
          shot_before and (moved, len(dv), inner, len(iv), shot_after == shot_before))
    check("the bird is the reference's wave file, in place from the loader's fade", all(s["bird"] == "new_landing_swiftee_anim.webp" for s in samples if s["loaded"]), {s["bird"] for s in samples})
    check("the sky is on: the kit's 87 drifting stars and the breathing glow", pg.evaluate("document.querySelectorAll('.sg-sky i').length === 87 && getComputedStyle(document.querySelector('.sg-glow')).animationName === 'sgBreathe' && getComputedStyle(document.querySelector('.sg-sky')).display === 'block'"),
          pg.evaluate("[document.querySelectorAll('.sg-sky i').length, getComputedStyle(document.querySelector('.sg-glow')).animationName]"))
    # [cover-sky] (2026-10-28) the sky is SEEN: the start gate (in the stage, z 80, over the fixed sky at z 0) paints nothing of its
    # own on the cover (the reference's body.is-start .start-gate{background:transparent}); and the pop-in fades in from 0
    gate_bg = pg.evaluate("(() => { const c = getComputedStyle(document.getElementById('startGate')); return [c.backgroundImage, c.backgroundColor]; })()")
    check("the start gate is transparent on the cover, so the glow and the stars show", gate_bg[0] == "none" and gate_bg[1] == "rgba(0, 0, 0, 0)", gate_bg)
    ready_op = pg.evaluate("window.__readyOpacity")
    check("the play button's pop-in starts from opacity 0 (sgBtnReveal's fade, not beaten by an !important)", ready_op == "0", ready_op)
    star = pg.evaluate("""() => { for (const el of document.querySelectorAll('.sg-sky i')) { const r = el.getBoundingClientRect(); if (r.width > 6 && parseFloat(getComputedStyle(el).opacity) > 0.3 && r.top > 20 && r.top < 100) return [r.left + r.width / 2, r.top + r.height / 2]; } return null; }""")
    if star: pg.mouse.click(star[0], star[1]); pg.wait_for_timeout(120)
    check("a tapped star pops (the kit's sky-burst)", bool(star) and pg.evaluate("document.querySelectorAll('.sg-burst').length >= 1 && document.querySelectorAll('.sg-sky i.popped').length >= 1"), star)
    # [sky-burst-fix] (2026-11-15) its colourful particles fly OUT and shrink as they fade — never back to the star: each particle's distance
    # from the burst's centre as a share of its own flight (--dx, --dy), and its size as a share of its own (--ps), at ~0.12 / 0.35 / 0.65 s
    BURST = """() => { const b = document.querySelector('.sg-burst'); if (!b) return null; const ox = parseFloat(b.style.left), oy = parseFloat(b.style.top), ps = [];
      for (const i of b.querySelectorAll('i')) { const r = i.getBoundingClientRect(), c = getComputedStyle(i);
        const D = Math.hypot(parseFloat(c.getPropertyValue('--dx')), parseFloat(c.getPropertyValue('--dy')));
        ps.push([Math.hypot(r.left + r.width / 2 - ox, r.top + r.height / 2 - oy) / D, r.width / parseFloat(c.getPropertyValue('--ps'))]); }
      const m = k => ps.reduce((s, p) => s + p[k], 0) / ps.length; return ps.length ? [+m(0).toFixed(3), +m(1).toFixed(3), ps.length] : null; }"""
    bs1 = pg.evaluate(BURST); pg.wait_for_timeout(230); bs2 = pg.evaluate(BURST); pg.wait_for_timeout(300); bs3 = pg.evaluate(BURST)
    check("[sky-burst-fix] ...its colourful particles fly out from the star and shrink as they fade: their distance grows (on its way out at ~0.35 s, at least .7 of "
          "their flight by ~0.65 s) and they end smaller than they start — none goes back to the star",
          None not in (bs1, bs2, bs3) and bs3[0] > bs2[0] > bs1[0] and bs3[0] >= 0.7 and bs3[1] <= 0.7, (bs1, bs2, bs3))
    # [cover-fx] the scene's ambient light: the flare breathing, the dust alive
    DUST = "(() => { const d = document.getElementById('sgDust'), x = d.getContext('2d'), im = x.getImageData(0, 0, d.width, d.height).data; let s = 0, n = 0; for (let i = 3; i < im.length; i += 4 * 97) { s += im[i]; n++; } return [s / n, window.__sgDust ? window.__sgDust.t : null]; })()"
    d1 = pg.evaluate(DUST); pg.wait_for_timeout(600); d2 = pg.evaluate(DUST)
    fl = pg.evaluate("(() => { const f = document.querySelector('.sg-fx .sg-flare2'); const c = getComputedStyle(f); return [c.animationName, c.animationDuration, c.mixBlendMode, getComputedStyle(document.getElementById('sgDust')).mixBlendMode]; })()")
    check("the card's scene carries the reference's light: the lens flare breathes (sgFlare2, 9 s, screen blend) and the sunlit dust is alive (its clock advancing, its specks moving) ([cover-fx])",
          fl == ["sgFlare2", "9s", "screen", "screen"] and d1[0] > 0.02 and d2[1] is not None and d2[1] > d1[1] and abs(d2[0] - d1[0]) > 0.0005, (fl, d1, d2))
    # [cover-eyes] the three faces: drawing, each blinking on its own clock, every gaze on the pointer, curious at a tap
    dbg = pg.evaluate("window.SGEyes ? SGEyes.debug() : null")
    check("the three characters' eyes are live: three faces drawing (their canvases shown) ([cover-eyes])", dbg is not None and len(dbg) == 3 and all(f["on"] for f in dbg), dbg)
    first_blink = [None, None, None]; t0b = pg.evaluate("performance.now()")
    for _ in range(160):
        dd = pg.evaluate("[performance.now(), SGEyes.debug().map(f => f.lid)]")
        for i, l in enumerate(dd[1]):
            if l > 0.5 and first_blink[i] is None: first_blink[i] = dd[0] - t0b
        if all(v is not None for v in first_blink): break
        pg.wait_for_timeout(50)
    counts = pg.evaluate("SGEyes.debug().map(f => f.blinks)")
    check("...each blinks (every face within 8 s), on its own clock (their lids are not shut in the same instants)",
          all(v is not None for v in first_blink) and all(c >= 1 for c in counts) and (max(first_blink) - min(first_blink)) > 60, (first_blink, counts))
    pg.mouse.move(120, 660); pg.wait_for_timeout(400); gl = pg.evaluate("SGEyes.debug().map(f => f.g.x)")
    pg.mouse.move(1250, 110); pg.wait_for_timeout(400); gr = pg.evaluate("SGEyes.debug().map(f => f.g.x)")
    check("...every gaze follows the child's mouse: all three look left with it at the lower left and right with it at the upper right", all(x < -0.3 for x in gl) and all(x > 0.3 for x in gr), (gl, gr))
    pg.mouse.click(660, 640); pg.wait_for_timeout(250)
    check("...and a tap makes them curious (the pencil's reaction)", pg.evaluate("SGEyes.debug().every(f => f.expr === 'curious')"), pg.evaluate("SGEyes.debug().map(f => f.expr)"))
    # the chip replays the welcome; the button stays; the bird replays it too
    pg.click("#sgVo", force=True); pg.wait_for_timeout(800); s1 = pg.evaluate(STATE)
    check("a tap on the chip replays the welcome; the play button stays in", s1["vo"] and s1["src"] == "vo_landing.ogg" and s1["btn"] and s1["ready"], (s1["src"], s1["btn"]))
    pg.evaluate("stopAudio()"); pg.wait_for_timeout(300)
    pg.click("#sgMascot", force=True); pg.wait_for_timeout(800); s2 = pg.evaluate(STATE)
    check("a tap on the bird replays the welcome", s2["vo"] and s2["src"] == "vo_landing.ogg", s2["src"])
    pg.evaluate("stopAudio()")
    # [cover-fx] / [cover-eyes] off the cover: the eye canvases hide, the dust's clock stops
    pg.evaluate("document.getElementById('startGate').classList.add('hidden'); document.body.classList.remove('is-start')"); pg.wait_for_timeout(400)
    t_a = pg.evaluate("window.__sgDust.t"); pg.wait_for_timeout(300)
    off = pg.evaluate("[[...document.querySelectorAll('.sgf-eyes')].map(c => c.style.display), window.__sgDust.t]")
    check("off the cover the eye canvases hide and the dust stops", off[0] == ["none", "none", "none"] and off[1] == t_a, (off, t_a))
    check("no page errors", not errs, errs[:3])
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)   # [title-off] a FAIL now fails the run (it printed and exited 0 before)
