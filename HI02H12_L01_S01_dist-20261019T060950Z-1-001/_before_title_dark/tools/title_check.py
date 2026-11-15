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
  ".sgf-question":      (85+841, 134+147, 138, 207),
  # [title-off] (2026-11-15) the frame's title art (.sgf-title, 85+251.58, 134+12.02, 593.83 x 109.99) is removed — see TITLE_BOX
  ".sgf-purn":          (85+97, 134+139, 219.473, 219.473),
  ".sgf-comma":         (85+502, 134+170, 95, 143),
  ".sgf-shadow.s1":     (85+141, 134+303, 132, 69),
  ".sgf-shadow.s2":     (85+473, 134+270, 142, 64),
  ".sgf-shadow.s3":     (85+857, 134+306, 115, 69),
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
HEAD_INFO = """(refShadow) => { const all = document.querySelectorAll('.sgf-heading'); if (all.length !== 1) return null;
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
BOXES ="""(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
  if (!e) { o[s] = null; continue; } const r = e.getBoundingClientRect(); o[s] = [r.left, r.top, r.width, r.height]; } return o; }"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--mute-audio"])          # default policy: autoplay blocked
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    bad = []; pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(4000)
    check("with autoplay blocked the welcome has not played: the play button is NOT on the page yet, the chip is off",
          pg.evaluate("getComputedStyle(document.getElementById('sgBtn')).display === 'none' && document.getElementById('sgVo').classList.contains('sg-vo-off')"))
    pg.evaluate("document.getElementById('sgBtn').classList.add('ready')"); pg.wait_for_timeout(700)   # to measure its box
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
    stops = ("rgb(255, 230, 0)", "rgb(255, 226, 0)", "rgb(253, 204, 2)", "rgb(253, 189, 1)", "rgb(255, 172, 2)", "rgb(255, 138, 2)")
    check("[title-color] ...in the picture's colours: the text (the fill's middle gold #FDCC02 since [title-stroke-off]) under its fill layer — the same line (same font, size, spacing, centring; "
          "24 px of room round the 73.6 px line) in the yellow-to-gold gradient #FFE600 > #FFE200 > #FDCC02 > #FDBD01 > #FFAC02 > #FF8A02, clipped to the letters, no shadow",
          hd is not None and hd["col"] == "rgb(253, 204, 2)" and af["clip"] == "text" and af["fill"] == "rgba(0, 0, 0, 0)" and af["bg"].startswith("linear-gradient(")
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
    yellow = sum(1 for (r, g, b_) in px if r > 240 and g > 165 and b_ < 70); maroon = sum(1 for (r, g, b_) in px if 35 < r < 115 and g < 35 and b_ < 35)
    white = sum(1 for (r, g, b_) in px if min(r, g, b_) > 240); blue = sum(1 for (r, g, b_) in px if r < 40 and g < 110 and b_ > 120)
    check("[title-stroke-off] ...painted: its yellow letters, white rim and deep-blue edge show in the screenshot, and no maroon outline is left",
          yellow > 3000 and maroon < 100 and white > 1000 and blue > 300, (yellow, maroon, white, blue, reg.size))
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
    b.close()

    # ---- the welcome, the play button, the chip, the bird, the sky ----
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(html.as_uri())
    # [cover-sky] the button's computed opacity at the very moment .ready lands (synchronous in the observer: the reveal's 0 % frame)
    pg.evaluate("""() => { const btn = document.getElementById('sgBtn'); window.__readyOpacity = null;
      new MutationObserver(() => { if (window.__readyOpacity === null && btn.classList.contains('ready')) window.__readyOpacity = getComputedStyle(btn).opacity; })
        .observe(btn, { attributes: true, attributeFilter: ['class'] }); }""")
    STATE = """() => { const a = (typeof currentAudio !== 'undefined') ? currentAudio : null; const btn = document.getElementById('sgBtn'), vo = document.getElementById('sgVo'), bird = document.getElementById('sgMascot');
      return { t: performance.now(), vo: !!(a && !a.paused && !a.ended && isPlaying), src: a ? a.src.split('/').pop().split('?')[0] : null,
               btn: getComputedStyle(btn).display !== 'none', ready: btn.classList.contains('ready'), breathe: btn.classList.contains('sg-breathe'), btnAnim: getComputedStyle(btn).animationName,
               chipOff: vo.classList.contains('sg-vo-off'), bird: (bird.getAttribute('src') || '').split('/').pop().split('?')[0], loaded: document.body.classList.contains('loaded'),
               hd: (() => { const e = document.querySelector('.sgf-heading'); if (!e) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.width, r.height, e.getAnimations().length]; })() }; }"""
    samples = []
    for _ in range(150):
        samples.append(pg.evaluate(STATE)); pg.wait_for_timeout(100)
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
