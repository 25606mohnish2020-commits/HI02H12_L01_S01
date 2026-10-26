"""Headless capture of every screen of a SwiftPAL game.
usage: python -I shoot.py <html path> <out dir> [--gate]
Captures: landing (with ?dev=1 so the dev nav shows), every slide, the end screen, a long-held
tutorial slide (so आगे has appeared), and — last, because it holds the stage for ~8s — the peek gate
at the moment its headline is on screen.
"""
import sys, os, pathlib, time
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
gate = "--gate" in sys.argv
url = html.as_uri() + "?dev=1"

LEAVE = """() => {
  const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove();
}"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}, device_scale_factor=1)
    errs = []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: errs.append("PAGEERROR " + str(e)))
    pg.goto(url); pg.wait_for_timeout(3200)
    pg.screenshot(path=str(out / "00_landing.png"))
    n = pg.evaluate("CARD.slides.length")
    types = pg.evaluate("CARD.slides.map(s=>s.id+':'+s.type)")
    print("slides", n, types)
    for i in range(n):
        pg.evaluate(LEAVE)
        pg.evaluate(f"mountSlide({i})")
        pg.wait_for_timeout(2600)
        pg.screenshot(path=str(out / f"{i+1:02d}_{types[i].replace(':','_')}.png"))
    # end screen, after its praise line has had time to finish
    pg.evaluate(LEAVE); pg.evaluate(f"mountSlide({n-1})"); pg.wait_for_timeout(6000)
    pg.screenshot(path=str(out / "zz_end_after_vo.png"))
    # the recap (T1) held long enough for its self-driving sequence (intro + nine beats, ~30 s) to arm आगे
    pg.evaluate(LEAVE); pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'T1'))")
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=60000)
    pg.wait_for_timeout(600); pg.screenshot(path=str(out / "zz_T1_after_vo.png"))
    if gate:
        pg.evaluate(LEAVE); pg.evaluate("mountSlide(0)"); pg.wait_for_timeout(800)
        pg.evaluate("phaseBlurTransition(()=>{}, 'guided')"); pg.wait_for_timeout(5400)
        pg.screenshot(path=str(out / "zz_phase_gate_guided.png"))
    print("console errors:", len(errs)); [print("  ", e[:200]) for e in errs[:15]]
    b.close()
