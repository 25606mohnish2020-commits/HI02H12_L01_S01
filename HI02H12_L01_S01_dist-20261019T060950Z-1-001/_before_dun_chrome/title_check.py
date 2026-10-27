"""Verify the title page against the Figma frame and check Swiftie <-> landing-VO sync.
usage: python -I title_check.py <index.html> <figma_target.png> <outdir>
1. 1280x720 viewport, autoplay BLOCKED (so Swiftie rests on the still): screenshot + per-pixel diff vs the
   Figma render, masking only the two engine controls the frame does not contain (play button, 🔊 chip).
2. Every title element's rendered box vs the frame's numbers (in 1280-frame px).
3. 1333x750, autoplay ALLOWED: sample VO state and which Swiftie is shown every 100 ms through the greeting.
"""
import sys, pathlib, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageDraw

html = pathlib.Path(sys.argv[1]).resolve(); target = Image.open(sys.argv[2]).convert("RGB")
out = pathlib.Path(sys.argv[3]).resolve(); out.mkdir(parents=True, exist_ok=True)

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
  "#sgSwiftie":         (5, 371, 245, 245),
}
BOXES = """(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
  if (!e) { o[s] = null; continue; } const r = e.getBoundingClientRect(); o[s] = [r.left, r.top, r.width, r.height]; } return o; }"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--mute-audio"])          # default policy: autoplay blocked
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    bad = []; pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(4000)
    shot = out / "title_1280.png"; pg.screenshot(path=str(shot))
    boxes = pg.evaluate(BOXES, list(EXPECT) + [".sg-btn", ".sg-vo"])
    print("== geometry (rendered vs frame, px) ==")
    worst = 0
    for s, exp in EXPECT.items():
        got = boxes[s]; d = max(abs(g - e) for g, e in zip(got, exp)) if got else 999; worst = max(worst, d)
        print(f"  {'OK ' if d <= 1.0 else 'OFF'} {s:20s} got {[round(v,1) for v in got]}  frame {list(exp)}  max|d|={d:.2f}")
    print("  worst deviation %.2f px" % worst)
    # pixel diff, masking the two engine controls
    img = Image.open(shot).convert("RGB")
    mask = Image.new("L", img.size, 255); dr = ImageDraw.Draw(mask)
    for s in (".sg-btn", ".sg-vo"):
        l, t, w, h = boxes[s]; dr.rectangle([l - 2, t - 2, l + w + 2, t + h + 2], fill=0)
    diff = ImageChops.difference(img, target).convert("L")
    vals = [d for d, m in zip(diff.getdata(), mask.getdata()) if m]
    big = sum(1 for v in vals if v > 40)
    print("== pixel diff vs Figma render (controls masked) ==")
    print("  mean |diff| %.2f / 255   pixels off by >40: %d of %d (%.2f%%)" % (sum(vals) / len(vals), big, len(vals), 100 * big / len(vals)))
    heat = diff.point(lambda v: 255 if v > 40 else v * 3); heat.save(out / "title_diff_heat.png")
    side = Image.new("RGB", (1280, 1440)); side.paste(target, (0, 0)); side.paste(img, (0, 720)); side.save(out / "figma_vs_build.png")
    print("  page errors:", errs[:3], " failed requests:", bad[:5])
    b.close()

    # ---- sync timeline ----
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.goto(html.as_uri())
    STATE = """() => { const a = (typeof currentAudio !== 'undefined') ? currentAudio : null;
      const an = document.getElementById('sgSwiftieAnim'), st = document.getElementById('sgSwiftie');
      return { t: performance.now(), vo: !!(a && !a.paused && !a.ended && isPlaying), at: a ? a.currentTime : 0,
               src: a ? a.src.split('/').pop() : null, anim: an.classList.contains('on'), still: !st.classList.contains('off'),
               animSrc: (an.getAttribute('src') || '').split('/').pop() }; }"""
    samples = []
    for _ in range(130):
        samples.append(pg.evaluate(STATE)); pg.wait_for_timeout(100)
    # replay the greeting with the 🔊 chip: Swiftie must wave again, then rest
    pg.click("#sgVo", force=True)
    for _ in range(110):
        samples.append(pg.evaluate(STATE)); pg.wait_for_timeout(100)
    # leaving the landing mid-line must drop the wave at once
    pg.click("#sgVo", force=True); pg.wait_for_timeout(1500)
    pre = pg.evaluate(STATE)
    pg.evaluate("stopAudio(); document.getElementById('startGate').classList.add('hidden'); document.body.classList.remove('is-start')")
    pg.wait_for_timeout(200); post = pg.evaluate(STATE)
    print("== cut-off check == before: anim_shown=%s  after leaving landing: anim_shown=%s still_shown=%s" % (pre["anim"], post["anim"], post["still"]))
    b.close()

print("== Swiftie vs landing VO (100 ms samples) ==")
mism = [s for s in samples if s["vo"] != s["anim"]]
runs, prev = [], None
for s in samples:
    key = (s["vo"], s["anim"], s["still"])
    if key != prev: runs.append((round(s["t"] / 1000, 2), s["vo"], s["anim"], s["still"], s["src"], round(s["at"], 2), s["animSrc"])); prev = key
for r in runs: print("  t=%6.2fs  vo_sounding=%-5s anim_shown=%-5s still_shown=%-5s clip=%s @%ss  %s" % r)
print("  samples where Swiftie's state != VO state: %d of %d" % (len(mism), len(samples)))
starts = [s for s in samples if s["anim"]]; print("  anim restarts seen (distinct srcs):", len({s["animSrc"] for s in starts}))
