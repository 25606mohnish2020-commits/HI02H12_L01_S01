"""[l1-nudge] (2026-11-15) Verify page 15 L1's hand nudge: once the letter's envelope pulses in the cloud (.ltr.ready), 5 s with no tap
brings the earlier pages' tapping hand (P2 / G4 / P1's reveal hand in its rh-tap form) onto the envelope.
usage: python -I -X utf8 l1_nudge_check.py <index.html> <outdir>
Runs (1333x750, autoplay allowed, muted):
 A. no input: no hand before 4.8 s after .ready; the hand at 5 s (within 0.4 s): the same element as P2's (div.reveal-hand.rh-tap with the
    ripple / inner ripple / sparks layer and nudge_hand_new.svg), 96x96, its finger pressing on rhTapP2 1.3 s and the three layers on
    nhRippleOuter / nhRippleInner / nhSparkPop 1.3 s, the drop shadow, tappable; placed as P2's: centred on the envelope's box
    (.ltr-env-grow, within 1 px) with its top 56 px above that box's bottom edge; it stays (still there 3 s later); a tap on the hand opens
    the letter (.zoom) and the hand is gone at once; the page then moves on to L2.
 B. a tap elsewhere (on the girl) 3 s after .ready: no hand at 5 s; the hand at 8 s (within 0.4 s).
 C. the envelope tapped 2 s after .ready: it opens, and no hand ever comes (checked to 7 s).
 D. the sentence pages' hand is unchanged: the reveal-hand rules apply to P2's stage exactly as before (same computed values on a probe).
"""
import sys, pathlib, time
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)
GOTO = """(id) => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); mountSlide(CARD.slides.findIndex(s => s.id === id)); }"""
# a recorder: the moment .ready lands and the moment the hand is attached (performance.now()), read synchronously in observers
REC = """() => { window.__n = { ready: null, hand: null, gone: null };
  new MutationObserver(() => { const r = document.querySelector('.ltr'); if (r && r.classList.contains('ready') && window.__n.ready === null) window.__n.ready = performance.now(); })
    .observe(document.getElementById('slideHost'), { attributes: true, subtree: true, attributeFilter: ['class'] });
  new MutationObserver(() => { const h = document.querySelector('.slide-stage > .reveal-hand.ltr-hand');
      if (h && window.__n.hand === null) window.__n.hand = performance.now(); if (!h && window.__n.hand !== null && window.__n.gone === null) window.__n.gone = performance.now(); })
    .observe(document.querySelector('.slide-stage'), { childList: true }); }"""
HAND = """() => { const h = document.querySelector('.slide-stage > .reveal-hand.ltr-hand'); if (!h) return null;
  const st = document.querySelector('.slide-stage'), sw = st.getBoundingClientRect(), k = sw.width / st.offsetWidth;
  const g = document.querySelector('.ltr-env-grow').getBoundingClientRect(), r = h.getBoundingClientRect(), c = getComputedStyle(h);
  const img = h.querySelector('img.rh-img'), fx = h.querySelector('.rh-fx'), an = e => { const s = getComputedStyle(e); return [s.animationName, s.animationDuration, s.animationIterationCount]; };
  return { cls: h.className, tag: h.tagName, img: img ? img.getAttribute('src') : null, fx: fx ? [...fx.children].map(i => i.className) : null,
    box: [r.width / k, r.height / k], cx: ((r.left + r.width / 2) - (g.left + g.width / 2)) / k, top: (r.top - g.bottom) / k, z: c.zIndex, pe: c.pointerEvents,
    filter: c.filter, animHand: c.animationName, animImg: img ? an(img) : null, animFx: fx ? [...fx.children].map(an) : null }; }"""
def until(pg, js, ms):
    t = time.time()
    while (time.time() - t) * 1000 < ms:
        if pg.evaluate(js): return True
        pg.wait_for_timeout(50)
    return False
def to_ready(pg):
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(GOTO, "L1"); pg.evaluate(REC)
    return until(pg, "window.__n.ready !== null", 40000)
def at(pg, ms):   # wait until ms after .ready
    pg.wait_for_function(f"performance.now() - window.__n.ready >= {ms}", timeout=ms + 20000, polling=20)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    # ---- A ----
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    ok = to_ready(pg)
    check("A. L1 reaches the pulsing envelope (.ltr.ready, the envelope's ltrPulse on)", ok and pg.evaluate("getComputedStyle(document.querySelector('.ltr-env-pulse')).animationName") == "ltrPulse")
    at(pg, 4800); early = pg.evaluate("!!document.querySelector('.slide-stage > .reveal-hand')")
    check("A. no hand in the first 4.8 s of the pulsing", not early)
    until(pg, "window.__n.hand !== null", 3000)
    n = pg.evaluate("window.__n"); dt = (n["hand"] - n["ready"]) if n["hand"] else None
    check("A. with no tap, the hand comes 5 s after the envelope starts pulsing (within 0.4 s)", dt is not None and 4950 <= dt <= 5400, dt and round(dt))
    pg.wait_for_timeout(700); h = pg.evaluate(HAND)
    check("A. ...the earlier pages' tapping hand: div.reveal-hand.rh-tap with the ripple / inner ripple / sparks layer and nudge_hand_new.svg",
          h is not None and h["tag"] == "DIV" and "reveal-hand" in h["cls"] and "rh-tap" in h["cls"] and h["img"] == "assets/UI/nudge_hand_new.svg" and h["fx"] == ["rh-ro", "rh-ri", "rh-sp"], h and (h["cls"], h["img"], h["fx"]))
    check("A. ...its tapping: the finger on rhTapP2 1.3 s (no bob), the layers on nhRippleOuter / nhRippleInner / nhSparkPop 1.3 s, all looping; 96x96, the drop shadow, z 55, tappable",
          h is not None and h["animImg"] == ["rhTapP2", "1.3s", "infinite"] and h["animHand"] == "none" and [a[0] for a in h["animFx"]] == ["nhRippleOuter", "nhRippleInner", "nhSparkPop"]
          and all(a[1] == "1.3s" and a[2] == "infinite" for a in h["animFx"]) and abs(h["box"][0] - 96) < 0.6 and abs(h["box"][1] - 96) < 0.6 and "drop-shadow" in h["filter"] and h["z"] == "55" and h["pe"] == "auto",
          h and {k: h[k] for k in ("animImg", "animHand", "animFx", "box", "filter", "z", "pe")})
    check("A. ...placed as P2's: centred on the envelope (within 1 px), its top 56 px above the bottom edge of the envelope's box (the fingertip in its lower part)",
          h is not None and abs(h["cx"]) <= 1 and abs(h["top"] + 56) <= 1, h and (round(h["cx"], 2), round(h["top"], 2)))
    pg.screenshot(path=str(out / "l1_nudge_hand.png"))
    at(pg, 8300); still = pg.evaluate("!!document.querySelector('.slide-stage > .reveal-hand.ltr-hand')")
    check("A. ...it stays, tapping, while nothing is tapped (still there 3 s later)", still)
    box = pg.evaluate("(() => { const r = document.querySelector('.slide-stage > .reveal-hand.ltr-hand').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; })()")
    pg.mouse.click(box[0], box[1]); pg.wait_for_timeout(120)
    s = pg.evaluate("[document.querySelector('.ltr').classList.contains('zoom'), !!document.querySelector('.slide-stage > .reveal-hand'), window.__n.gone !== null]")
    check("A. a tap on the hand opens the letter (.zoom) and the hand is gone at once", s == [True, False, True], s)
    went = until(pg, "CARD.slides[state.idx].id === 'L2'", 8000)
    check("A. ...and the page moves on to L2", went)
    check("A. no page errors", not errs, errs[:3]); pg.close()
    # ---- B ----
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    to_ready(pg); at(pg, 3000); pg.mouse.click(560, 300)      # the girl: no button there
    at(pg, 5600); mid = pg.evaluate("!!document.querySelector('.slide-stage > .reveal-hand')")
    until(pg, "window.__n.hand !== null", 4000)
    n = pg.evaluate("window.__n"); dt = (n["hand"] - n["ready"]) if n["hand"] else None
    check("B. a tap elsewhere 3 s into the pulsing starts the 5 s again: no hand at 5.6 s, the hand at 8 s (within 0.4 s)", not mid and dt is not None and 7950 <= dt <= 8450, (mid, dt and round(dt)))
    check("B. no page errors", not errs, errs[:3]); pg.close()
    # ---- C ----
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    to_ready(pg); at(pg, 2000)
    env = pg.evaluate("(() => { const r = document.querySelector('.ltr-env-grow').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; })()")
    pg.mouse.click(env[0], env[1]); pg.wait_for_timeout(100); z = pg.evaluate("document.querySelector('.ltr').classList.contains('zoom')")
    hand_seen = False; t0 = time.time()
    while time.time() - t0 < 5.2:
        if pg.evaluate("!!document.querySelector('.slide-stage > .reveal-hand')"): hand_seen = True; break
        pg.wait_for_timeout(100)
    check("C. the envelope tapped 2 s into the pulsing opens the letter, and no hand ever comes", z and not hand_seen, (z, hand_seen))
    check("C. no page errors", not errs, errs[:3]); pg.close()
    # ---- D ----
    pg = b.new_page(viewport={"width": 1333, "height": 750}); pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(GOTO, "P2"); pg.wait_for_timeout(2500)
    d = pg.evaluate("""() => { const st = document.querySelector('.slide-stage'), h = document.createElement('div'); h.className = 'reveal-hand rh-tap';
      h.innerHTML = '<span class="rh-fx"><i class="rh-ro"></i><i class="rh-ri"></i><i class="rh-sp"></i></span><img class="rh-img" src="assets/UI/nudge_hand_new.svg">'; st.append(h);
      const c = getComputedStyle(h), i = getComputedStyle(h.querySelector('.rh-img')), f = getComputedStyle(h.querySelector('.rh-fx')), o = getComputedStyle(h.querySelector('.rh-ro'));
      const v = [document.getElementById('stage').classList.contains('sent-page'), c.width, c.height, c.zIndex, c.filter, c.animationName, i.animationName, i.animationDuration, f.left, f.top, f.width, o.animationName, o.backgroundImage.slice(0, 40)]; h.remove(); return v; }""")
    check("D. P2's tapping hand keeps its computed look (96 px, z 55, the shadow, no bob, rhTapP2 1.3 s, the tap layer at -1.948/-28.133 84.255 px, the ripple art)",
          d[0] and d[1:4] == ["96px", "96px", "55"] and "drop-shadow" in d[4] and d[5] == "none" and d[6:8] == ["rhTapP2", "1.3s"]
          and all(abs(float(v[:-2]) - e) <= 1 / 64 for v, e in zip(d[8:11], (-1.948, -28.133, 84.255)))   # Chrome keeps lengths to 1/64 px
          and d[11] == "nhRippleOuter" and d[12].startswith('url("data:image/svg+xml'), d)
    pg.close(); b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
