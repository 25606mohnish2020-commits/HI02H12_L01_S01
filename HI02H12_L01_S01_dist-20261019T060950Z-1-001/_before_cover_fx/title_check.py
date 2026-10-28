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
   breathing) and a tapped star pops.
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
  ".sgf-title":         (85+251.58, 134+12.02, 593.83, 109.99),
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
BOXES = """(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
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
               chipOff: vo.classList.contains('sg-vo-off'), bird: (bird.getAttribute('src') || '').split('/').pop().split('?')[0], loaded: document.body.classList.contains('loaded') }; }"""
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
    # the chip replays the welcome; the button stays; the bird replays it too
    pg.click("#sgVo", force=True); pg.wait_for_timeout(800); s1 = pg.evaluate(STATE)
    check("a tap on the chip replays the welcome; the play button stays in", s1["vo"] and s1["src"] == "vo_landing.ogg" and s1["btn"] and s1["ready"], (s1["src"], s1["btn"]))
    pg.evaluate("stopAudio()"); pg.wait_for_timeout(300)
    pg.click("#sgMascot", force=True); pg.wait_for_timeout(800); s2 = pg.evaluate(STATE)
    check("a tap on the bird replays the welcome", s2["vo"] and s2["src"] == "vo_landing.ogg", s2["src"])
    pg.evaluate("stopAudio()")
    check("no page errors", not errs, errs[:3])
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
