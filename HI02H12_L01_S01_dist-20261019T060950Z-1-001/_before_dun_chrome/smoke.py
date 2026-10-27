"""Functional smoke test of the re-skinned build: drive the real UI with clicks and check the engine advances."""
import sys, pathlib
from playwright.sync_api import sync_playwright
html = pathlib.Path(sys.argv[1]).resolve()
LEAVE = """() => { const sg=document.getElementById('startGate'); if(sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl=document.getElementById('bootLoader'); if(bl) bl.remove(); }"""
GOTO = "(id) => mountSlide(CARD.slides.findIndex(s => s.id === id))"   # by id: slide numbers moved when T0 was added
results = []
def check(name, ok, detail=""):
    results.append((name, ok)); print(("PASS " if ok else "FAIL ") + name + (" — " + str(detail) if detail else ""))

# the round gate, sampled every frame in the page: open?, title revealed?, its text, the peeking Swiftie shown?, the clip
GATE_LOG = """() => { window._gate = []; let last = ''; const step = () => {
  const g = document.getElementById('phaseGate'), img = document.getElementById('phaseGateImg'), a = currentAudio;
  const r = { slide: CARD.slides[state.idx].id, show: g.classList.contains('show'), speaking: g.classList.contains('text-speaking'),
    title: document.getElementById('phaseGateTitle').textContent, peek: img.style.visibility !== 'hidden',
    clip: a ? a.src.split('/').pop().split('?')[0] : null, playing: isPlaying };
  const k = JSON.stringify(r); if (k !== last) { last = k; r.ms = performance.now(); window._gate.push(r); }
  requestAnimationFrame(step); }; requestAnimationFrame(step); }"""
def gate_after(log, frm, to, title, clip, opens_expected):
    """a round gate as the child sees it: it opens on frm's end (the gate's openings so far must be exactly opens_expected,
    in order); the peeking Swiftie first (silent), then the title as the clip sounds; `to` only once that VO has ended
    (the gate gone)"""
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
def gate_after_t4(log):
    """the T4 -> G1 gate: the only opening so far; "चलिए, साथ में करें!" with vo_pt_guided"""
    return gate_after(log, "T4", "G1", "चलिए, साथ में करें!", "vo_pt_guided.ogg", ["T4"])

def wait_silence(pg, max_ms=15000):
    """wait until no VO is sounding (vo-lock off)"""
    pg.wait_for_function("!document.body.classList.contains('vo-lock')", timeout=max_ms)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(html.as_uri()); pg.wait_for_timeout(3000)

    # 1. landing -> play button -> peek gate -> tutorial slide 0 in the tut frame
    wait_silence(pg, 20000)
    pg.click("#sgBtn", force=True); pg.wait_for_timeout(1200)   # force: the play button pulses forever, so it is never "stable"
    gate_up = pg.evaluate("document.getElementById('phaseGate').classList.contains('show')")
    check("start button opens the peek gate", gate_up)
    pg.wait_for_function("document.body.classList.contains('tut-page') && !document.getElementById('phaseGate').classList.contains('show')", timeout=20000)
    check("gate closes into the story page (T0) inside the tutorial frame", pg.evaluate("CARD.slides[state.idx].id==='T0' && !!document.querySelector('.tut-card.sfig-card')"))
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=40000)
    pg.click("#navBtn", force=True)   # force: the active pill pulses forever, so it is never "stable"
    pg.wait_for_function("CARD.slides[state.idx].id==='T0B'", timeout=10000)
    check("story page's आगे opens T0B (\"आइए वाक्य सुनें।\")", pg.evaluate("!!document.querySelector('.tut-card.sfig-card .sfig-title')"))
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=60000)
    pg.click("#navBtn", force=True)
    pg.wait_for_function("CARD.slides[state.idx].id==='T1'", timeout=10000)
    check("T0B's आगे opens T1 (the three-marks recap) in the tutorial frame", pg.evaluate("!!document.querySelector('.tut-card.sfig-recap .rcf-row')"))
    pg.wait_for_function("document.getElementById('navBtn').classList.contains('active')", timeout=90000)
    pg.click("#navBtn", force=True)
    pg.evaluate(GATE_LOG)
    pg.wait_for_function("CARD.slides[state.idx].id==='T2'", timeout=10000)
    check("T1's आगे opens T2 (the run-on sentence demo) on the plain stage", pg.evaluate("!!document.querySelector('.tut-card.sfig-full .dmf-band')"))
    pg.wait_for_function("CARD.slides[state.idx].id==='T3'", timeout=40000)
    check("T2 runs itself through to T3, the second demo (no आगे)", pg.evaluate("!!document.querySelector('.tut-card.sfig-full .dmf-band') && getComputedStyle(document.getElementById('navBtn')).display === 'none'"))
    pg.wait_for_function("CARD.slides[state.idx].id==='T4'", timeout=40000)
    check("T3 runs itself through to T4, the third demo (no आगे)", pg.evaluate("!!document.querySelector('.tut-card.sfig-full .dmf-band') && document.querySelectorAll('.dmf-blank').length === 2 && getComputedStyle(document.getElementById('navBtn')).display === 'none'"))
    pg.wait_for_function("CARD.slides[state.idx].id==='G1'", timeout=60000)
    check("T4 runs itself through the round gate to G1, the Figma tap page (no आगे)",
          pg.evaluate("CARD.slides[state.idx].type === 'PUNCT_PICK' && !!document.querySelector('.tut-card.sfig-full .dmf-band')"))
    check("after T4 (and only there since T1) the gate: the peeking Swiftie, then \"चलिए, साथ में करें!\" with its VO, then G1", *gate_after_t4(pg.evaluate("window._gate")))

    # 2. G1 (PUNCT_PICK, see pick_check.py): once the sentence has been read, two wrong tiles (each wiggles, no mark), then
    #    the right one -> its mark in the slot -> auto-advance to G2
    pg.wait_for_function("!!document.querySelector('.sfig-in.dmf-live')", timeout=30000)
    pg.click(".dmf-tile.t2"); pg.wait_for_timeout(150)
    check("G1: a wrong tile wiggles, counts an attempt, no mark in the slot",
          pg.evaluate("document.querySelector('.dmf-tile.t2').classList.contains('wiggle') && state.attempts===1 && !document.querySelector('.dmf-mark.in')"))
    pg.wait_for_timeout(500); pg.click(".dmf-tile.t3"); pg.wait_for_timeout(150)
    check("G1: the other wrong tile too, and the page waits", pg.evaluate("state.attempts===2 && CARD.slides[state.idx].id==='G1' && !document.querySelector('.dmf-mark.in')"))
    pg.wait_for_timeout(500); pg.click(".dmf-tile.t1"); pg.wait_for_timeout(600)
    check("G1: the right tile (पूर्ण विराम) puts its mark in the slot", pg.evaluate("!!document.querySelector('.dmf-blank .dmf-mark.in') && document.querySelector('.dmf-mark').textContent==='।'"))
    pg.wait_for_function("CARD.slides[state.idx].id==='G2'", timeout=15000)
    check("G1 then moves on to G2 by itself, the second Figma tap page",
          pg.evaluate("CARD.slides[state.idx].type === 'PUNCT_PICK' && !!document.querySelector('.tut-card.sfig-full .dmf-band')"))
    # G2: a wrong tile, then the right one (प्रश्नवाचक चिह्न) -> "?" in the slot -> G3
    pg.wait_for_function("!!document.querySelector('.sfig-in.dmf-live')", timeout=30000)
    pg.click(".dmf-tile.t1"); pg.wait_for_timeout(150)
    check("G2: a wrong tile wiggles, no mark", pg.evaluate("document.querySelector('.dmf-tile.t1').classList.contains('wiggle') && state.attempts===1 && !document.querySelector('.dmf-mark.in')"))
    pg.wait_for_timeout(500); pg.click(".dmf-tile.t3"); pg.wait_for_timeout(600)
    check("G2: the right tile puts its \"?\" in the slot", pg.evaluate("!!document.querySelector('.dmf-blank .dmf-mark.in') && document.querySelector('.dmf-mark').textContent==='?'"))
    pg.wait_for_function("CARD.slides[state.idx].id==='G3'", timeout=15000)
    check("G2 then moves on to G3 by itself, the third Figma tap page (one small slot)",
          pg.evaluate("CARD.slides[state.idx].type === 'PUNCT_PICK' && !!document.querySelector('.tut-card.sfig-full .dmf-blank.dmf-own')"))
    # G3: a wrong tile, then the right one (अल्प विराम) -> "," in the slot -> G4
    pg.wait_for_function("!!document.querySelector('.sfig-in.dmf-live')", timeout=30000)
    pg.click(".dmf-tile.t3"); pg.wait_for_timeout(150)
    check("G3: a wrong tile wiggles, no mark", pg.evaluate("document.querySelector('.dmf-tile.t3').classList.contains('wiggle') && state.attempts===1 && !document.querySelector('.dmf-mark.in')"))
    pg.wait_for_timeout(500); pg.click(".dmf-tile.t2"); pg.wait_for_timeout(600)
    check("G3: the right tile puts its \",\" in the slot", pg.evaluate("!!document.querySelector('.dmf-blank .dmf-mark.in') && document.querySelector('.dmf-mark').textContent===','"))
    pg.wait_for_function("CARD.slides[state.idx].id==='G4'", timeout=15000)
    check("G3 then moves on to G4 by itself: the reference game's P4 page (picture + three sentence pills)",
          pg.evaluate("CARD.slides[state.idx].type === 'SENT_PICK' && document.getElementById('stage').classList.contains('sent-page') && document.querySelectorAll('#slideHost .sent-opt').length === 3"))
    # G4 (SENT_PICK, see g4_check.py): a wrong pill (wiggle, no line), then the right one -> green, its line, straight on to P1
    #    (the round gate now follows P2, not the guided -> practice boundary here)
    pg.wait_for_timeout(4000)
    right = pg.evaluate("[...document.querySelectorAll('#slideHost .so-pill')].findIndex(p => p.textContent.trim() === 'लड़की पतंग उड़ा रही है ।')")
    pg.click(f"#slideHost .opt-cell >> nth={(right + 1) % 3}"); pg.wait_for_timeout(150)
    check("G4: a wrong pill wiggles and counts an attempt", pg.evaluate("state.attempts===1 && !!document.querySelector('#slideHost .opt-cell.wg-wrong')"))
    pg.wait_for_timeout(1200); pg.click(f"#slideHost .opt-cell >> nth={right}"); pg.wait_for_timeout(200)
    check("G4: the right pill (लड़की पतंग उड़ा रही है ।) is marked green", pg.evaluate("!!document.querySelector('#slideHost .opt-cell.correct')"))
    pg.wait_for_function("CARD.slides[state.idx].id==='P1'", timeout=60000)
    check("G4 then moves straight on to P1 (no gate here): the same P4 page with its own picture and sentences",
          pg.evaluate("CARD.slides[state.idx].type === 'SENT_PICK' && document.getElementById('stage').classList.contains('sent-page') && document.querySelectorAll('#slideHost .sent-opt').length === 3 && !window._gate.some(r => r.slide === 'G4' && r.show)"))
    # P1 (SENT_PICK, see g4_check.py --page P1): a wrong pill, then the right one -> green, its line, straight on to P2
    pg.wait_for_timeout(4000)
    right = pg.evaluate("[...document.querySelectorAll('#slideHost .so-pill')].findIndex(p => p.textContent.trim() === 'क्या यह आपकी किताब है?')")
    pg.click(f"#slideHost .opt-cell >> nth={(right + 1) % 3}"); pg.wait_for_timeout(150)
    check("P1: a wrong pill wiggles and counts an attempt", pg.evaluate("state.attempts===1 && !!document.querySelector('#slideHost .opt-cell.wg-wrong')"))
    pg.wait_for_timeout(1200); pg.click(f"#slideHost .opt-cell >> nth={right}"); pg.wait_for_timeout(200)
    check("P1: the right pill (क्या यह आपकी किताब है?) is marked green", pg.evaluate("!!document.querySelector('#slideHost .opt-cell.correct')"))
    pg.wait_for_function("CARD.slides[state.idx].id==='P2'", timeout=60000)
    check("P1 then moves on to P2: the same P4 page again, its long sentences on two lines",
          pg.evaluate("CARD.slides[state.idx].type === 'SENT_PICK' && document.querySelectorAll('#slideHost .sent-opt').length === 3 && document.querySelectorAll('#slideHost .so-br').length === 3"))
    # P2 (SENT_PICK, see g4_check.py --page P2): a wrong pill, then the right one (the commas) -> green, its line, then the gate
    pg.wait_for_timeout(4000)
    right = pg.evaluate("[...document.querySelectorAll('#slideHost .so-pill')].findIndex(p => p.textContent.trim() === 'मेरे पास लाल, नीली, हरी और पीली पेंसिल हैं ।')")
    pg.click(f"#slideHost .opt-cell >> nth={(right + 1) % 3}"); pg.wait_for_timeout(150)
    check("P2: a wrong pill wiggles and counts an attempt", pg.evaluate("state.attempts===1 && !!document.querySelector('#slideHost .opt-cell.wg-wrong')"))
    pg.wait_for_timeout(1200); pg.click(f"#slideHost .opt-cell >> nth={right}"); pg.wait_for_timeout(200)
    check("P2: the right pill (मेरे पास लाल, नीली, हरी और पीली पेंसिल हैं ।) is marked green", pg.evaluate("!!document.querySelector('#slideHost .opt-cell.correct')"))
    # P2's end opens the round-3 gate ([gate-p2] + [gate-cel]): the peeking Swiftie, then "अब आपकी बारी!" as vo_pt_practice sounds,
    # then L1, the letter page ([letter-fig], letter_check.py has it beat by beat): it plays itself to the pulsing envelope, the
    # tap opens it, then the CELEBRATION end screen with no further gate
    pg.wait_for_function("CARD.slides[state.idx].id==='L1' && !!document.querySelector('.ltr')", timeout=60000)
    check("P2 then crosses the gate (VO + animation) into L1, the letter page; the gates since T1: T4's, then P2's",
          *gate_after(pg.evaluate("window._gate"), "P2", "L1", "अब आपकी बारी!", "vo_pt_practice.ogg", ["T4", "P2"]))
    pg.wait_for_function("!!document.querySelector('.ltr.ready')", timeout=20000)
    check("L1: the scene has played itself to the pulsing letter in the cloud, tappable, no आगे",
          pg.evaluate("getComputedStyle(document.getElementById('navBtn')).display === 'none' && !!document.querySelector('.ltr.ready .ltr-env-pos')"))
    bb = pg.locator(".ltr-env-pos").bounding_box(); pg.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
    pg.wait_for_function("CARD.slides[state.idx].id==='L2' && !!document.querySelector('.stp')", timeout=15000)
    check("the tap opens the envelope (zoom, flap, dive, veil) and L2, the stamp page, follows ([stamp-fig], stamp_check.py has it beat by beat)",
          pg.evaluate("getComputedStyle(document.getElementById('navBtn')).display === 'none' && !document.getElementById('phaseGate').classList.contains('show')"))
    pg.wait_for_function("!!document.querySelector('.stp.live')", timeout=40000)
    check("L2: the title, the sheet and the tray, the two stamps, the sentence, then the blinking slot — the stamps now the child's to drag",
          pg.evaluate("!!document.querySelector('.dmf-band.in') && !!document.querySelector('.stp-sheet.in') && !!document.querySelector('.stp-tray.in') && document.querySelectorAll('.stp-stamp img.shown').length === 2 && document.querySelectorAll('.stp-sent .sfig-w.on').length === 5 && !!document.querySelector('.stp-slot.in')"))
    # the child's drop ([stamp-drag]): the ? stamp dragged from the tray onto the slot, its print point on the slot's centre
    RS = pg.evaluate("CARD.slides.find(s => s.id === 'L2').data.rounds")
    fpx = lambda x, y: pg.evaluate("([x, y]) => { const b = document.getElementById('stage').getBoundingClientRect(), k = b.width / 1280; return [b.left + x * k, b.top + y * k]; }", [x, y])
    def stamp_drop(ri):   # [stamp-rounds] each of round ri's slots in turn gets its right stamp (the slot's own pick, or the round's) dragged from the tray, its print point on the slot's centre — the next slot once the previous box has gone and the stamps are the child's again (593:130: two slots; 593:151: four, each wanting its own stamp)
        R = RS[ri]
        for j, sl in enumerate(R.get("slots") or [R["slot"]]):
            k = sl.get("pick", R["pick"]); bx = R["boxes"][k]; tp = R["tips"][k]
            if j: pg.wait_for_function(f"document.querySelectorAll('.stp-slot.gone').length >= {j} && !!document.querySelector('.stp.live')", timeout=8000); pg.wait_for_timeout(300)
            g = fpx(bx[0] + bx[2] / 2, bx[1] + 40); d = fpx(bx[0] + bx[2] / 2 + sl["x"] + sl["w"] / 2 - (bx[0] + tp[0]), bx[1] + 40 + sl["y"] + sl["h"] / 2 - (bx[1] + tp[1]))
            pg.mouse.move(g[0], g[1]); pg.mouse.down(); pg.wait_for_timeout(80)
            for i in range(1, 13): pg.mouse.move(g[0] + (d[0] - g[0]) * i / 12, g[1] + (d[1] - g[1]) * i / 12); pg.wait_for_timeout(16)
            pg.wait_for_timeout(60); pg.mouse.up()
    stamp_drop(0)
    pg.wait_for_function("!!document.querySelector('.stp-mark.in')", timeout=5000)
    check("L2 round 1: the ? stamp dropped on the slot is pressed and the ? printed (stamp_check.py has the page beat by beat: the guidance, the wrong drops, the sounds)", pg.evaluate("!!document.querySelector('.stp-mark.in')"))
    # [stamp-rounds] after each confetti the stamps and the sentence go and the next round comes: round 2 (frame 579:47: the । and the
    # comma, the two-row sentence, the small slot), round 3 (592:89: three stamps, "मुझे उपहार बहुत पसंद हैं", the danda's slot), round 4
    # (593:130: three stamps, two questions on two rows, TWO slots for the ? — each box goes on its own chime, the confetti after the second),
    # round 5 (593:151: the letter's closing lines on five rows, FOUR slots each wanting its own stamp — the comma, the ?, the danda twice — and the sign-off)
    for ri in range(1, len(RS)):
        R = RS[ri]; nw = len(R["sentence"]["word_times"]); ns = len(R["stamps"]); pict = R["stamps"][R["pick"]]
        pg.wait_for_function(f"document.querySelector('.stp').dataset.round === '{ri}'", timeout=12000)
        pg.wait_for_function("!!document.querySelector('.stp.live')", timeout=25000)
        check(f"L2 round {ri + 1} ({R['frame']}): its {ns} stamps shown, its sentence's {nw} words read and shown, its slot blinking — the stamps the child's again",
              pg.evaluate(f"document.querySelectorAll('.stp-stamp img.shown').length === {ns} && document.querySelectorAll('.stp-sent .sfig-w.on').length === {nw} && !!document.querySelector('.stp-slot.in') && document.querySelector('.stp-stamp.s{R['pick']} img').src.endsWith('{pict}.webp')"))
        stamp_drop(ri); nsl = len(R.get("slots") or [R["slot"]])
        pg.wait_for_function(f"document.querySelectorAll('.stp-mark.in').length === {nsl}", timeout=5000)
        check(f"L2 round {ri + 1}: the {R['mark']} stamp dropped on {'the slot' if nsl == 1 else 'each of the ' + str(nsl) + ' slots'} is pressed and the {R['mark']} printed {'there' if nsl == 1 else 'in each'}", pg.evaluate(f"document.querySelectorAll('.stp-mark.in').length === {nsl}"))
    pg.wait_for_function("!!document.querySelector('.stp-final.in')", timeout=12000)   # [stamp-final] after the last round's confetti the final picture dissolves in
    check("L2 finale: after the last round's confetti the final picture (the girl with her letter) dissolves in over the whole stage, its asset served at 1280 px, before the end screen",
          pg.evaluate("document.querySelector('.stp-final img').src.endsWith('img_stamp_final.webp') && document.querySelector('.stp-final img').naturalWidth === 1280"))
    pg.wait_for_function("CARD.slides[state.idx].id==='CEL' && document.body.classList.contains('is-end')", timeout=15000)
    log = pg.evaluate("window._gate"); opens = [log[i]["slide"] for i in range(len(log)) if log[i]["show"] and (i == 0 or not log[i - 1]["show"])]
    check("the CELEBRATION end screen follows L2 with no further gate; 15 pages, the end screen last",
          opens == ["T4", "P2"] and pg.evaluate("CARD.slides.length === 15 && CARD.slides[14].id === 'CEL'"), opens)
    check("the end screen's validator: every expected signal fired", pg.evaluate("GameBus.validatorReport.passed === true"), pg.evaluate("GameBus.validatorReport.missing_signals"))

    # 3. dev nav present with ?dev=1
    pg.goto(html.as_uri() + "?dev=1"); pg.wait_for_timeout(2500)
    check("dev nav bar + jump dropdown render with ?dev=1", pg.evaluate("!!document.querySelector('#devNav select.dev-nav-sel') && document.querySelectorAll('#devNav option').length===CARD.slides.length"))
    # 4. T4 run twice in one load from the dev nav's list: its end crosses the gate both times (the engine shows each
    #    round's gate once per load; T4 clears it, so a review re-run is not sent straight to G1)
    for run in (1, 2):
        pg.select_option("#devNav select.dev-nav-sel", str(next(i for i, s in enumerate(pg.evaluate("CARD.slides.map(s => s.id)")) if s == "T4")))
        pg.wait_for_function("CARD.slides[state.idx].id==='T4'", timeout=5000); pg.evaluate(GATE_LOG)
        pg.wait_for_function("CARD.slides[state.idx].id==='G1'", timeout=60000)
        check(f"T4 from the dev nav's list, run {run} in the same load: its end crosses the gate (VO + animation) into G1", *gate_after_t4(pg.evaluate("window._gate")))
    check("no page errors", not errs, errs[:3])
    b.close()
print("\n%d/%d passed" % (sum(1 for _, ok in results if ok), len(results)))
