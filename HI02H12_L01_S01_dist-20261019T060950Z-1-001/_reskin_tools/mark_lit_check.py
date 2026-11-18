"""[mark-lit] (2026-11-18) G4 / P1 / P2: the 2nd wrong pill's hint 2 line lights every punctuation mark in the three sentences.
usage: python -I -X utf8 mark_lit_check.py <index.html> <outdir> [--old <the previous build's index.html>] [--page G4|P1|P2 ...]
1. (--old) at rest the pills are the previous build's, pixel for pixel (the marks' own spans move nothing): the same seeded order, the
   grid shot 2.5 s in, every moving layer outside the grid irrelevant (the shot is the grid only).
2. at rest the sentences are not split: no .p2-mk, every word one text node (a span boundary would shape the letters before a mark a
   sub-pixel differently); while lit each . , ? । is one .p2-mk.lit inside its word (G4 3, P1 3, P2 7); afterwards every word is its
   plain text again, the same words as before.
3. two wrong taps, every frame recorded (a rAF recorder: the clip that is current, its clock, paused / ended, the lit marks, the first
   mark's computed colour and animation): no mark lit through the instruction, the 1st wrong's buzz and the try-again line; from hint 2's
   first sounding frame (its clock > 0) ALL marks lit in #E86A00 (rgb(232, 106, 0)) with p2WordPop, held while it sounds (every frame);
   gone within 2 frames of its end (or of its clock stopping); none lit after. Then the 3rd wrong: the reveal (no light)."""
import sys, json, pathlib
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
OLD = pathlib.Path(sys.argv[sys.argv.index("--old") + 1]).resolve() if "--old" in sys.argv else None
PAGES = [a for i, a in enumerate(sys.argv) if i > 0 and sys.argv[i - 1] == "--page"] or ["G4", "P1", "P2"]
WANT_MARKS = {"G4": 3, "P1": 3, "P2": 7}
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""), flush=True)
    if not ok: fails.append(name)
LEAVE = """() => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded'); const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); }"""
MOUNT = """(id) => { const r = Math.random; Math.random = () => 0.99999; mountSlide(CARD.slides.findIndex(s => s.id === id)); Math.random = r; }"""
GRID = """() => { const g = document.querySelector('#slideHost .sent-opts'); const r = g.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }"""
WORDS = """() => { const w = [...document.querySelectorAll('#slideHost .p2-word')];
  return { mk: document.querySelectorAll('#slideHost .p2-mk').length, plain: w.every(x => x.childNodes.length === 1 && x.firstChild.nodeType === 3), words: w.map(x => x.textContent) }; }"""
REC = """() => { window.__ml = []; const f = () => { try { const a = (typeof currentAudio !== 'undefined') ? currentAudio : null, m = document.querySelectorAll('#slideHost .p2-mk');
    const lit = [...m].filter(x => x.classList.contains('lit') && x.parentElement.classList.contains('p2-word') && /^[।?,]$/.test(x.textContent)); const cs = lit.length ? getComputedStyle(lit[0]) : null;
    window.__ml.push({ t: performance.now(), src: a ? (a.src || '').split('/').pop().split('?')[0] : null, ct: a ? a.currentTime : 0, paused: a ? a.paused : true,
      ended: a ? a.ended : false, playing: !!(typeof isPlaying !== 'undefined' && isPlaying), lit: lit.length, n: m.length, color: cs ? cs.color : null, anim: cs ? cs.animationName : null }); } catch(e){}
  requestAnimationFrame(f); }; requestAnimationFrame(f); }"""
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    for page in PAGES:
        print(f"===== {page}")
        shots = {}
        for tag, src in (("new", html), ("old", OLD)):
            if src is None: continue
            pg = b.new_page(viewport={"width": 1333, "height": 750}); pg.goto(src.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE)
            pg.evaluate(MOUNT, page); pg.wait_for_timeout(2500)
            gx = pg.evaluate(GRID); f = out / f"{page}_{tag}_grid.png"
            pg.screenshot(path=str(f), clip={"x": gx[0] - 4, "y": gx[1] - 4, "width": gx[2] + 8, "height": gx[3] + 8}); shots[tag] = f
            if tag == "new":
                rest = pg.evaluate(WORDS)
                check(f"{page}: at rest the sentences are not split: no mark span, every word one text node", rest["mk"] == 0 and rest["plain"], rest)
            pg.close()
        if "old" in shots:
            A = np.asarray(Image.open(shots["new"]).convert("RGB")).astype(int); B = np.asarray(Image.open(shots["old"]).convert("RGB")).astype(int)
            same = A.shape == B.shape and int(np.abs(A - B).max()) == 0
            check(f"{page}: at rest the three sentences are the previous build's, pixel for pixel", same,
                  (A.shape, B.shape, int((np.abs(A - B).max(axis=2) > 0).sum()) if A.shape == B.shape else None))
        # the flow
        pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE); pg.evaluate(REC); pg.evaluate(MOUNT, page); pg.wait_for_timeout(1500)
        w0 = pg.evaluate(WORDS)
        wrong = pg.evaluate("""(id) => { const s = CARD.slides.find(x => x.id === id), right = s.data.options.find(o => o.correct).label_hi.trim();
          return [...document.querySelectorAll('#slideHost .sent-opt')].map((c, i) => [i, c.textContent.trim().replace(/\\s+/g, ' ') === right.replace(/\\s+/g, ' ')]).filter(x => !x[1]).map(x => x[0]); }""", page)
        quiet = "() => !isPlaying && !sfxBusy() && !state.hintActive"
        def tap(i):
            pg.locator("#slideHost .sent-opt").nth(i).click(force=True)
        tap(wrong[0]); t1 = pg.evaluate("performance.now()")
        pg.wait_for_timeout(1200); pg.wait_for_function(quiet, timeout=20000, polling=20); pg.wait_for_timeout(300)
        tap(wrong[1]); t2 = pg.evaluate("performance.now()")
        pg.wait_for_timeout(1200); pg.wait_for_function(quiet, timeout=25000, polling=20); pg.wait_for_timeout(800)
        tap(wrong[0]); pg.wait_for_timeout(2500)
        R = pg.evaluate("window.__ml"); hint2 = f"vo_{page.lower()}_hint2"
        before = [s for s in R if s["t"] < t2 + 900]
        h2 = [s for s in R if s["src"] and s["src"].startswith(hint2)]
        sounding = [s for s in h2 if not s["paused"] and not s["ended"] and s["ct"] > 0]
        first = next((i for i, s in enumerate(R) if s["src"] and s["src"].startswith(hint2) and not s["paused"] and s["ct"] > 0), None)
        lit_at = next((i for i, s in enumerate(R) if s["lit"] > 0), None)
        end_i = next((i for i in range(first or 0, len(R)) if first is not None and (R[i]["ended"] or R[i]["paused"] or not (R[i]["src"] or "").startswith(hint2))), None)
        off_i = next((i for i in range(end_i or 0, len(R)) if end_i is not None and R[i]["lit"] == 0), None)
        n = WANT_MARKS[page]
        check(f"{page}: no mark lit through the instruction, the 1st wrong tap's buzz and the try-again line", before and all(s["lit"] == 0 for s in before), (len(before), max((s["lit"] for s in before), default=None)))
        check(f"{page}: from hint 2's first sounding frame ALL {n} marks lit (within 2 frames of its clock starting)",
              first is not None and lit_at is not None and 0 <= lit_at - first <= 2 and R[lit_at]["lit"] == n, (first, lit_at, lit_at is not None and R[lit_at]["lit"]))
        held = [s for s in R[(lit_at or 0) + 1:(end_i or 0)]]
        check(f"{page}: ...held in the words' orange #E86A00 with p2WordPop on every frame while the line sounds",
              held and all(s["lit"] == n and s["color"] == "rgb(232, 106, 0)" and s["anim"] == "p2WordPop" for s in held), (len(held), {(s["lit"], s["color"], s["anim"]) for s in held}))
        check(f"{page}: ...and gone within 2 frames of the line's end; none lit after it", end_i is not None and off_i is not None and off_i - end_i <= 2 and all(s["lit"] == 0 for s in R[off_i:]),
              (end_i, off_i, end_i is not None and round(R[end_i]["t"] - R[first]["t"]) if first is not None else None))
        w1 = pg.evaluate(WORDS)
        check(f"{page}: afterwards every word is its plain text again, the same words as before the light", w1["mk"] == 0 and w1["plain"] and w1["words"] == w0["words"], (w1["mk"], w1["plain"], w1["words"] == w0["words"]))
        check(f"{page}: no page errors", not errs, errs[:3])
        pg.close()
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
