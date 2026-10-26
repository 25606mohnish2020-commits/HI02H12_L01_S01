"""The round gate rules [gate-p2] + [gate-cel] (CARD.round3_gate_after = "P2"): G4 -> P1 is a plain page change (no gate at
the guided -> practice boundary); P2, the last page since the ported P3-P6 were removed, ends in the round-3 gate before the
letter page L1 ([gate-cel] lifted the engine's no-gate-before-the-celebration rule for P2 while the end screen followed it):
the peeking Swiftie (silent), then "अब आपकी बारी!" revealed as vo_pt_practice sounds at the animation's mouth-open point, then L1
once that VO has ended — on EVERY run of P2 in one load; L1 -> the end screen with no further gate (letter_check.py has L1 itself).
usage: python -I -X utf8 gate_check.py <index.html> <outdir>
Screenshots: gate_after_p2.png (the gate: title shown, its VO sounding), end_after_p2.png (the end screen reached through L1)."""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)

LEAVE = """() => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); }"""
# the gate sampled every frame (as smoke.py's GATE_LOG): open?, title revealed?, its text, the peeking Swiftie shown?, the clip
GATE_LOG = """() => { window._gate = []; let last = ''; const step = () => {
  const g = document.getElementById('phaseGate'), img = document.getElementById('phaseGateImg'), a = currentAudio;
  const r = { slide: CARD.slides[state.idx].id, show: g.classList.contains('show'), speaking: g.classList.contains('text-speaking'),
    title: document.getElementById('phaseGateTitle').textContent, peek: img.style.visibility !== 'hidden',
    clip: a ? a.src.split('/').pop().split('?')[0] : null, playing: isPlaying };
  const k = JSON.stringify(r); if (k !== last) { last = k; r.ms = performance.now(); window._gate.push(r); }
  requestAnimationFrame(step); }; requestAnimationFrame(step); }"""

def gate_after(log, frm, to, title, clip, opens_expected):
    """the gate as the child sees it: the openings so far are exactly opens_expected; after the last one the peeking Swiftie
    first (silent), then the title as the clip sounds; `to` only once that VO has ended (the gate gone)"""
    opens = [i for i, r in enumerate(log) if r["show"] and (i == 0 or not log[i - 1]["show"])]
    if [log[i]["slide"] for i in opens] != opens_expected: return False, [log[i]["slide"] for i in opens]
    o = opens[-1]
    nxt = next((i for i, r in enumerate(log) if i > o and r["slide"] == to), None)
    if nxt is None: return False, "no " + to
    gate = log[o:nxt]
    peek = next((r for r in gate if r["peek"] and not r["speaking"]), None)
    vo = next((r for r in gate if r["speaking"] and r["clip"] == clip and r["playing"]), None)
    ended = any(r["clip"] == clip and not r["playing"] for r in gate)
    ok = bool(peek and vo and ended and vo["title"] == title and vo["ms"] - peek["ms"] > 3000
              and all(r["slide"] == frm and r["show"] for r in gate) and not log[nxt]["show"])
    return ok, f"peek {round(peek['ms'] - log[o]['ms']) if peek else None} ms, VO + title {round(vo['ms'] - log[o]['ms']) if vo else None} ms after it opened, {to} {round(log[nxt]['ms'] - log[o]['ms'])} ms"

def openings(log):
    return [log[i]["slide"] for i in range(len(log)) if log[i]["show"] and (i == 0 or not log[i - 1]["show"])]

def right_tap(pg, pid, label):
    pg.evaluate(f"mountSlide(CARD.slides.findIndex(s => s.id === '{pid}'))")
    pg.wait_for_function("!isPlaying && currentAudio && currentAudio.src.includes('vo_g4_prompt')", timeout=15000, polling=20); pg.wait_for_timeout(300)
    i = pg.evaluate(f"[...document.querySelectorAll('#slideHost .so-pill')].findIndex(p => p.textContent.trim() === {json.dumps(label)})")
    pg.click(f"#slideHost .opt-cell >> nth={i}")

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE); pg.evaluate(GATE_LOG)
    check("the card asks for the round-3 gate after P2", pg.evaluate("CARD.round3_gate_after") == "P2")
    ids = pg.evaluate("CARD.slides.map(s => s.id)")
    check("the pages: ... G4, P1, P2, L1 (the letter page), L2 (the stamp page), then the end screen (15 in all; the ported P3-P6 gone)",
          ids == ["T0", "T0B", "T1", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "L1", "L2", "CEL"], ids)
    # 1. G4 -> P1: a plain page change, no gate (the guided -> practice boundary no longer opens one)
    right_tap(pg, "G4", "लड़की पतंग उड़ा रही है ।")
    pg.wait_for_function("CARD.slides[state.idx].id === 'P1'", timeout=30000); pg.wait_for_timeout(200)
    check("G4 -> P1 straight on, no gate opening", openings(pg.evaluate("window._gate")) == [] and pg.evaluate("CARD.slides[state.idx].id") == "P1", openings(pg.evaluate("window._gate")))
    # 2. P2 -> the round-3 gate -> L1, the letter page, twice in one load (a re-run from L1 crosses it again); on run 1 L1 is
    #    played through (the tap on the pulsing envelope) to the end screen, with no further gate
    L1_UP = ("CARD.slides[state.idx].id === 'L1' && !!document.querySelector('.ltr') && !document.querySelector('.ltr.b-in')"
             " && !document.getElementById('phaseGate').classList.contains('show') && !document.body.classList.contains('gating')"
             " && !document.getElementById('stage').classList.contains('blurred')")
    for run, opens_expected in ((1, ["P2"]), (2, ["P2", "P2"])):
        right_tap(pg, "P2", "मेरे पास लाल, नीली, हरी और पीली पेंसिल हैं ।")
        pg.wait_for_function("document.getElementById('phaseGate').classList.contains('text-speaking')", timeout=20000)
        if run == 1: pg.wait_for_timeout(400); pg.screenshot(path=str(out / "gate_after_p2.png"))
        pg.wait_for_function("CARD.slides[state.idx].id === 'L1' && !!document.querySelector('.ltr')", timeout=40000); pg.wait_for_timeout(300)
        check(f'P2 run {run} in the same load -> the gate (the peeking Swiftie, then "अब आपकी बारी!" as vo_pt_practice sounds) -> L1, the letter page',
              *gate_after(pg.evaluate("window._gate"), "P2", "L1", "अब आपकी बारी!", "vo_pt_practice.ogg", opens_expected))
        check(f"P2 run {run}: the letter page is up after the gate (its first scene, the girl writing), the gate closed and the stage unblurred", pg.evaluate(L1_UP))
        if run == 1:
            pg.wait_for_function("!!document.querySelector('.ltr.ready')", timeout=20000)
            bb = pg.locator(".ltr-env-pos").bounding_box(); pg.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
            pg.wait_for_function("CARD.slides[state.idx].id === 'L2' && !!document.querySelector('.stp')", timeout=15000)
            check("L1: the tap on the pulsing envelope opens it and L2, the stamp page, follows with no gate", openings(pg.evaluate("window._gate")) == ["P2"]
                  and not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"))
            pg.wait_for_function("CARD.slides[state.idx].id === 'CEL' && document.body.classList.contains('is-end')", timeout=45000); pg.wait_for_timeout(1500)
            pg.screenshot(path=str(out / "end_after_p2.png"))
            check("L2 plays itself through (the stamp printed) and the CELEBRATION end screen follows, with no further gate", openings(pg.evaluate("window._gate")) == ["P2"]
                  and pg.evaluate("document.getElementById('endScreen').classList.contains('show') && !document.getElementById('phaseGate').classList.contains('show')"))
            # this run jumps in at G4, so punct_build_done (G1-G3) is legitimately missing here; phase_transition now fires on
            # P2's gate. smoke.py plays the whole game and checks that the validator passes outright. Also checked: nothing the
            # removed pages fired is still expected (qtype_sort_done, P6's).
            rep = pg.evaluate("GameBus.validatorReport"); expected = pg.evaluate("CARD.signals_expected")
            check("the end screen's validator: only the skipped pages' punct_build_done is missing (P2's gate fired phase_transition); qtype_sort_done not expected",
                  "qtype_sort_done" not in expected and set(rep.get("missing_signals") or []) == {"punct_build_done"}, rep.get("missing_signals"))
            ms = pg.evaluate("GameBus.signals.filter(s => s.signal === 'mastery_score').map(s => [s.hits, s.attempts, s.value])")
            check("mastery_score from the practice page played (P2 here: 1 hit of 1)", ms == [[1, 1, 1]], ms)
    check("no page errors", not errs, errs[:3])
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
