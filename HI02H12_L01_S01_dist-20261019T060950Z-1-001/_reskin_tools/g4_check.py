"""Verify G4 or P1 (SENT_PICK): the reference game's Page 11 (P4, https://hi-02-h04-l01-s01-dun.vercel.app/) with this
lesson's picture, title and sentences — its look and its flow.
usage: python -I -X utf8 g4_check.py <index.html> <outdir> [--page G4|P1|P2] [--ref <P4's picture png>]
       G4 (the default) and P1 move straight on to the next page; P2 goes through the round-3 gate ("अब आपकी बारी!", [gate-p2])
       to L1, the letter page (since 2026-10-26; until then, with P3-P6 removed, it went straight to the end screen — this entry
       said "CEL" with no gate until [sent-font], 2026-10-27).
       P2's sentences are too long for P4's pill on one line: its pills keep P4's width and font on two lines, all broken
       after the same word, centred on the row's line.
1. The right pill first: the instruction on entry; the tap marks it green at once and pops the picture, nothing sounds for
   1 s (taps wait), then the kit's correct-select, the confetti and the happy Swiftie, and its own line with each word lit
   while the clip is inside that word's window; 0.7 s after the line the page moves on (P2: to the end screen).
   Reported: evidence_qa_first_try (first try), slide_completed success; P1 also one mastery attempt and hit.
2. Three wrong pills, then the guided tap: each wrong tap wiggles the pill (no line of its own), Swiftie tries again, taps
   wait 1 s; then the 1st: the try-again line, the pill dead ("crossed") until it ends; the 2nd: all three pills read in row
   order, 0.5 s apart, each lifted while its clip plays and its words lit in sync (a lone danda lit in the pause it makes,
   a word carrying its "?" through the pause after it),
   taps ignored meanwhile; the 3rd: the reveal — two pills greyed and dead, the right one ringed, the 96px hand under it.
   A tap on the hand: the green mark at once, 1 s, the ding + confetti, no line, and the page moves on (success false).
3. Left alone: the instruction again ~5 s after each time it ends (with the picture's pop-and-hold, not on entry); a tap
   during a repeat cuts it. No आगे, no hint bulb; the header chip, the picture and the pills where P4 has them.
4. --ref: the page with P4's own picture, title and sentences (same order) pixel-matches the live P4 at rest.
"""
import sys, json, pathlib
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
REF_PIC = sys.argv[sys.argv.index("--ref") + 1] if "--ref" in sys.argv else None
PAGE = sys.argv[sys.argv.index("--page") + 1] if "--page" in sys.argv else "G4"
CFG = {"G4": {"next": "P1", "gate": False, "mastery": False, "right": "लड़की पतंग उड़ा रही है ।",
              "labels": ["लड़की पतंग उड़ा रही है ।", "लड़की । पतंग उड़ा रही है", "लड़की पतंग उड़ा । रही है"]},
       "P1": {"next": "P2", "gate": False, "mastery": True, "right": "क्या यह आपकी किताब है?",
              "labels": ["क्या यह आपकी किताब है?", "क्या? यह आपकी किताब है", "क्या यह आपकी? किताब है"]},
       "P2": {"next": "L1", "gate": True, "mastery": True, "right": "मेरे पास लाल, नीली, हरी और पीली पेंसिल हैं ।", "lines": 2,
              "labels": ["मेरे पास लाल । नीली । हरी और पीली पेंसिल हैं ।", "मेरे पास लाल नीली हरी और पीली पेंसिल हैं ।", "मेरे पास लाल, नीली, हरी और पीली पेंसिल हैं ।"]}}[PAGE]
NEXT = CFG["next"]; ON = "through the round gate to " + NEXT if CFG["gate"] else "straight on to " + NEXT
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)

LEAVE = """() => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); }"""
SAMPLE = r"""() => { window._tl = []; let last = ''; const step = () => {
  const a = currentAudio, f = a ? decodeURIComponent(a.src.split('/').pop()) : '', m = f.match(/vo_(?:g4|p1|p2)_(\w+)\.ogg/);
  // [vo-rec] the shared clips: the praise vo_ok_pick -> 'ok', the try-again line (vo_g4_hint1 on G4, vo_pick_hint1 on P1/P2) -> 'try', hint 3 vo_pick_hint3 -> 'hint3'
  const clipOf = !a ? null : m ? (m[1] === 'hint1' ? 'try' : m[1]) : /vo_ok_pick/.test(f) ? 'ok' : /vo_pick_hint1/.test(f) ? 'try' : /vo_pick_hint3/.test(f) ? 'hint3' : 'other';
  const cells = [...document.querySelectorAll('#slideHost .opt-cell')], th = document.querySelector('#slideHost .story-q-thumb'), mi = document.getElementById('swBuddyImg');
  const r = { slide: CARD.slides[state.idx].id, clip: clipOf, t: a ? +a.currentTime.toFixed(3) : null, playing: isPlaying,
    cls: cells.map(c => c.className.replace('sent-opt opt-cell', '').trim()), say: cells.map(c => !!c.querySelector('.so-pill.p6-say')),
    lit: cells.map(c => [...c.querySelectorAll('.p2-word')].findIndex(w => w.classList.contains('on'))),
    pop: th ? (th.classList.contains('p2-pop') ? 'p2' : th.classList.contains('p6-pop') ? 'p6' : '') : '', mood: mi ? mi.getAttribute('src').split('/').pop().split('.')[0] : '',
    hand: (() => { const h = document.querySelector('.reveal-hand'); if (!h) return null; const r = h.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.width)]; })(),
    gate: document.getElementById('phaseGate').classList.contains('show'), conf: document.querySelectorAll('.conf-shot, .fx-confetti').length > 0,
    attempts: state.attempts, locked: state.locked, hint: state.hintActive };
  const k = JSON.stringify(r); if (k !== last) { last = k; r.ms = performance.now(); window._tl.push(r); }
  if (r.slide !== window._stopAt) requestAnimationFrame(step); }; requestAnimationFrame(step); }"""
LABELS = "[...document.querySelectorAll('#slideHost .so-pill')].map(p => p.textContent.trim())"

def run(pg):
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE)
    pg.evaluate(f"window._stopAt = '{NEXT}'"); pg.evaluate(SAMPLE); pg.evaluate(f"mountSlide(CARD.slides.findIndex(s => s.id === '{PAGE}'))")
    d = pg.evaluate(f"CARD.slides.find(s => s.id === '{PAGE}')")
    pg.wait_for_function(f"!isPlaying && currentAudio && currentAudio.src.includes('{d['audio']['prompt']}')", timeout=15000, polling=20); pg.wait_for_timeout(400)   # [vo-rec] the page's own instruction clip
    labels = pg.evaluate(LABELS)
    opt = {o["label_hi"]: o for o in d["data"]["options"]}
    right = next(i for i, l in enumerate(labels) if opt[l].get("correct"))
    return d, labels, opt, right
def timeline(pg):
    # this page's samples only: the page with its three pills built, and the gate / the next page after it (whose own
    # cells, if any, are not this page's pills)
    return [s if s["slide"] == PAGE else dict(s, cls=[""] * 3, say=[False] * 3, lit=[-1] * 3)
            for s in pg.evaluate("window._tl") if (s["slide"] == PAGE and len(s["cls"]) == 3) or s["gate"] or s["slide"] == NEXT]
gone = lambda s: s["gate"] or s["slide"] == NEXT   # the page has moved on
clip_of = lambda o: o["audio"].split("_", 2)[2]   # vo_p1_o2 -> o2
def sync_ok(tl, k, times, clip):
    """every sample of pill k's clip: the lit word is the one whose window [times[i], times[i+1]) holds the clip time (±60 ms);
    nothing lit only outside the windows (±90 ms: the sampler can log a frame just before the page's own tick lights a word)"""
    bad, seen = [], set()
    for s in tl:
        if s["clip"] != clip or not s["playing"] or s["t"] is None: continue
        i = s["lit"][k]; t = s["t"]
        if i >= 0: seen.add(i)
        okw = [j for j in range(len(times) - 1) if times[j] - 0.12 <= t < times[j + 1] + 0.12]   # [dun-chrome] +-120 ms: the reference's heavier confetti falls under the line (was 60)
        if i >= 0 and i not in okw: bad.append((t, i))
        if i < 0 and any(times[j] + 0.15 <= t < times[j + 1] - 0.15 for j in range(len(times) - 1)): bad.append((t, i))
    return bad, seen

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio", "--allow-file-access-from-files"])
    errs = []

    # ---- 1. the right pill first
    pg = b.new_page(viewport={"width": 1333, "height": 750}); pg.on("pageerror", lambda e: errs.append(str(e)))
    d, labels, opt, right = run(pg)
    look = pg.evaluate("""() => ({ title: document.getElementById('promptText').textContent, nav: getComputedStyle(document.getElementById('navBtn')).display,
      hint: getComputedStyle(document.getElementById('hintBtn')).display, chip: (() => { const r = document.getElementById('audioChip').getBoundingClientRect(); return [r.left, r.top, r.width]; })(),
      thumb: (() => { const r = document.querySelector('.story-q-thumb').getBoundingClientRect(); return [r.top, r.height, Math.round(r.left + r.width / 2)]; })(),
      pills: [...document.querySelectorAll('.so-pill')].map(p => { const r = p.getBoundingClientRect(); return [r.left, r.top, r.width, r.height, p.scrollWidth <= p.clientWidth]; }),
      lines: [...document.querySelectorAll('.so-pill')].map(p => { const ws = [...p.querySelectorAll('.p2-word')], tops = [...new Set(ws.map(w => Math.round(w.getBoundingClientRect().top)))];
        return tops.map(t => ws.filter(w => Math.round(w.getBoundingClientRect().top) === t).map(w => w.textContent).join(' ')); }) })""")
    check("the title band reads the instruction; no आगे and no hint bulb", look["title"] == d["prompt_hi"] == "सही विराम चिह्न वाला वाक्य चुनिए ।" and look["nav"] == "none" and look["hint"] == "none", look)
    head_ok = look["chip"] == [94.5, 80, 66] and look["thumb"][:2] == [146, 315] and abs(look["thumb"][2] - 666.5) <= 1
    if CFG.get("lines", 1) == 1:
        check("P4's places: the chip at 94.5,80; the picture 315 high from y 146, centred; three 344x78 pills at x 114.5 / 494.5 / 874.5, y 531.5, each on one line",
              head_ok and [q[:4] for q in look["pills"]] == [[114.5, 531.5, 344, 78], [494.5, 531.5, 344, 78], [874.5, 531.5, 344, 78]] and all(q[4] for q in look["pills"])
              and all(len(l) == 1 for l in look["lines"]), look)
    else:
        n1 = [len(l[0].replace(" ।", "").split()) for l in look["lines"]]   # words on each pill's first line, a lone danda riding with its word
        check("P4's places with two-line pills: the chip at 94.5,80; the picture 315 high from y 146, centred; three 344-wide pills at x 114.5 / 494.5 / 874.5, "
              "of one height, centred on P4's row line (y 570.5), nothing spilling, each on two lines broken after the same word, no line opening with a mark",
              head_ok and [q[0] for q in look["pills"]] == [114.5, 494.5, 874.5] and all(q[2] == 344 and q[4] for q in look["pills"])
              and len({round(q[3], 2) for q in look["pills"]}) == 1 and 78 < look["pills"][0][3] <= 100 and all(abs(q[1] + q[3] / 2 - 570.5) <= 0.5 for q in look["pills"])
              and all(len(l) == 2 and not l[1].startswith(("।", ",", "?")) for l in look["lines"]) and len(set(n1)) == 1, (look["pills"], look["lines"]))
    check(f"the three sentences are the asked ones, the right one '{CFG['right']}'", sorted(labels) == sorted(CFG["labels"]) and labels[right] == CFG["right"], labels)
    pic = pg.evaluate("[document.querySelector('.story-q-thumb').getAttribute('src'), document.querySelector('.story-q-thumb').naturalWidth]")
    check(f"{PAGE}'s own picture ({d['data']['recall_image_id']}) is the one shown", pic == [f"assets/Images/{d['data']['recall_image_id']}.webp", 1411], pic)
    pg.screenshot(path=str(out / "a_rest.png"))
    pg.click(f"#slideHost .opt-cell >> nth={right}"); pg.wait_for_timeout(300); pg.screenshot(path=str(out / "b_right_300.png"))
    pg.wait_for_timeout(1500); pg.screenshot(path=str(out / "c_right_1800.png"))
    pg.wait_for_function(f"CARD.slides[state.idx].id === '{NEXT}'", timeout=30000, polling=50); pg.wait_for_timeout(150)   # the sampler's next frame logs it
    tl = timeline(pg); sig = pg.evaluate(f"GameBus.signals.filter(s => s.slide_id === '{PAGE}')")
    ms = lambda i: tl[i]["ms"]; first = lambda c, s=0: next(i for i in range(s, len(tl)) if c(tl[i]))
    i_tap = first(lambda s: s["cls"][right].startswith("correct"))
    i_ck = first(lambda s: "ck-correct" in s["cls"][right], i_tap)
    rc = clip_of(opt[labels[right]])   # the right pill's own clip (o1 on G4 / P1, o3 on P2)
    i_ok = first(lambda s: s["clip"] == "ok" and s["playing"], i_tap); i_ok_e = first(lambda s: s["clip"] == "ok" and not s["playing"], i_ok)   # [vo-rec] the praise first
    i_line = first(lambda s: s["clip"] == rc and s["playing"], i_ok)
    i_end = first(lambda s: s["clip"] == rc and not s["playing"], i_line)
    i_gate = first(gone, i_end)
    check("the tap: the green mark and the picture's pop at once, Swiftie unchanged, nothing sounding for the 1 s hold",
          tl[i_tap]["pop"] == "p2" and not any(s["playing"] for s in tl[i_tap:i_ok]) and 950 <= ms(i_ok) - ms(i_tap) <= 1250, f"the praise {ms(i_ok) - ms(i_tap):.0f} ms after the mark")
    check("after the hold: the kit's correct-select, the confetti and the happy Swiftie with the praise (vo_ok_pick, “शाबाश! यह सही वाक्य है ।”), then the pill's own line as it ends",
          abs(ms(i_ck) - ms(i_ok)) <= 120 and any(s["conf"] for s in tl[i_ok:i_ok + 30]) and "celebrate" in tl[i_ok + 5]["mood"] and -60 <= ms(i_line) - ms(i_ok_e) <= 250,
          (ms(i_ck) - ms(i_ok), tl[i_ok + 5]["mood"], ms(i_line) - ms(i_ok_e)))
    bad, seen = sync_ok(tl, right, opt[labels[right]]["word_times"], rc)
    check("its words light one at a time in sync with the clip (each within its window ±120 ms), the closing danda too",
          not bad and seen == set(range(len(opt[labels[right]]["word_times"]) - 1)), f"seen {sorted(seen)}, off {bad[:4]}")
    check(f"0.7 s after the line the page moves on, {ON}", 650 <= ms(i_gate) - ms(i_end) <= 2500 and tl[i_gate]["gate"] == CFG["gate"] and pg.evaluate("CARD.slides[state.idx].id") == NEXT,
          f"{'gate' if tl[i_gate]['gate'] else tl[i_gate]['slide']} {ms(i_gate) - ms(i_end):.0f} ms after the line")
    first_try = [s for s in sig if s["signal"] == "evidence_qa_first_try"]; done = [s for s in sig if s["signal"] == "slide_completed"]
    check("reported: evidence_qa_first_try (first try) and slide_completed success", len(first_try) == 1 and first_try[0]["first_try"] is True and done and done[0]["success"] is True, (first_try, done))
    mst = pg.evaluate("[state.masteryAttempts, state.masteryHits]")
    check("mastery score: " + ("one attempt, one hit (the first-try right pill)" if CFG["mastery"] else "not counted (only the practice pages are)"), mst == ([1, 1] if CFG["mastery"] else [0, 0]), mst)
    pg.close()

    # ---- 2. three wrong pills, then the guided tap
    pg = b.new_page(viewport={"width": 1333, "height": 750}); pg.on("pageerror", lambda e: errs.append(str(e)))
    d, labels, opt, right = run(pg)
    wr = [i for i in range(3) if i != right]
    pg.click(f"#slideHost .opt-cell >> nth={wr[0]}"); pg.wait_for_timeout(150); pg.screenshot(path=str(out / "d_wrong1.png"))
    pg.wait_for_function(f"currentAudio && currentAudio.src.includes('{d['audio']['try_again']}') && isPlaying", timeout=10000, polling=20)   # [vo-rec] the page's try-again line (vo_g4_hint1 / vo_pick_hint1)
    pg.wait_for_function("!document.querySelector('#slideHost .opt-cell.crossed')", timeout=15000, polling=20); pg.wait_for_timeout(300)
    pg.click(f"#slideHost .opt-cell >> nth={wr[1]}")
    pg.wait_for_function("!!document.querySelector('#slideHost .so-pill.p6-say')", timeout=10000, polling=20); pg.wait_for_timeout(500)
    pg.screenshot(path=str(out / "e_review.png"))
    pg.click(f"#slideHost .opt-cell >> nth={right}", force=True); pg.wait_for_timeout(100)
    held = pg.evaluate("[state.attempts, !!document.querySelector('#slideHost .opt-cell.correct')]")
    pg.wait_for_function("!state.hintActive && !document.querySelector('#slideHost .so-pill.p6-say') && !isPlaying", timeout=30000, polling=20); pg.wait_for_timeout(300)
    pg.click(f"#slideHost .opt-cell >> nth={wr[0]}")
    pg.wait_for_function("!!document.querySelector('.reveal-hand')", timeout=10000, polling=20); pg.wait_for_timeout(600)
    pg.screenshot(path=str(out / "f_reveal.png"))
    rev = pg.evaluate("""() => { const h = document.querySelector('.reveal-hand').getBoundingClientRect(), c = document.querySelector('#slideHost .opt-cell.opt-guided').getBoundingClientRect();
      return { hand: [h.width, h.height, Math.round(h.left + h.width / 2), Math.round(c.left + c.width / 2), Math.round(h.top - c.bottom)],
               dim: [...document.querySelectorAll('#slideHost .opt-cell')].map(x => [x.className.replace('sent-opt opt-cell', '').trim(), getComputedStyle(x).pointerEvents, getComputedStyle(x).opacity, getComputedStyle(x).filter]),
               ring: getComputedStyle(document.querySelector('#slideHost .opt-cell.opt-guided .so-pill')).outline }; }""")
    pg.click(".reveal-hand", force=True); pg.wait_for_timeout(200)   # force: the hand bobs forever, so it is never "stable"; pg.screenshot(path=str(out / "g_guided_tap.png"))
    pg.wait_for_function(f"CARD.slides[state.idx].id === '{NEXT}'", timeout=30000, polling=50); pg.wait_for_timeout(150)
    tl = timeline(pg); sig = pg.evaluate(f"GameBus.signals.filter(s => s.slide_id === '{PAGE}')")
    ms = lambda i: tl[i]["ms"]; first = lambda c, s=0: next(i for i in range(s, len(tl)) if c(tl[i]))
    i_w1 = first(lambda s: s["attempts"] == 1)
    check("wrong tap 1: the pill wiggles and goes dead, Swiftie tries again, no line of its own",
          "wg-wrong" in tl[i_w1]["cls"][wr[0]] and "crossed" in tl[i_w1]["cls"][wr[0]] and "tryagain" in tl[i_w1 + 2]["mood"]
          and not any(s["clip"] in ("o1", "o2", "o3") and s["playing"] for s in tl[i_w1:i_w1 + 40]), (tl[i_w1]["cls"], tl[i_w1 + 2]["mood"]))
    i_try = first(lambda s: s["clip"] == "try" and s["playing"], i_w1); i_try_end = first(lambda s: s["clip"] == "try" and not s["playing"], i_try)
    i_unx = first(lambda s: not any("crossed" in c for c in s["cls"]), i_w1)
    check("...1 s later the try-again line; the pill is dead until it ends", 950 <= ms(i_try) - ms(i_w1) <= 1300 and abs(ms(i_unx) - ms(i_try_end)) <= 120,
          f"line {ms(i_try) - ms(i_w1):.0f} ms after the tap, un-crossed {ms(i_unx) - ms(i_try_end):+.0f} ms from its end")
    i_w2 = first(lambda s: s["attempts"] == 2)
    order = [s["clip"] for i, s in enumerate(tl[i_w2:], i_w2) if s["clip"] in ("o1", "o2", "o3") and s["playing"] and not (tl[i - 1]["clip"] == s["clip"] and tl[i - 1]["playing"])]
    want = [clip_of(opt[l]) for l in labels]
    check("wrong tap 2: 1 s later all three pills are read in row order", order[:3] == want, (order, want))
    lifted = all(any(s["say"][k] and s["clip"] == want[k] and s["playing"] for s in tl[i_w2:]) for k in range(3))
    starts = [first(lambda s, c=c: s["clip"] == c and s["playing"], i_w2) for c in want]
    ends = [first(lambda s, c=c: s["clip"] == c and not s["playing"], st) for c, st in zip(want, starts)]
    gaps = [ms(starts[k + 1]) - ms(ends[k]) for k in range(2)]
    check("...each lifted while its clip plays, ~0.5 s apart", lifted and all(450 <= g <= 750 for g in gaps) and 950 <= ms(starts[0]) - ms(i_w2) <= 1700,
          f"first {ms(starts[0]) - ms(i_w2):.0f} ms after the tap, gaps {[round(g) for g in gaps]}")
    sync = [sync_ok(tl, k, opt[labels[k]]["word_times"], want[k]) for k in range(3)]
    check("...each pill's words lit in sync with its clip (" + {"G4": "the danda of 'लड़की । पतंग ...' / '... उड़ा । रही है' lit in its pause)", "P1": "'क्या?' / 'आपकी?' lit through the pause after it)",
                                                              "P2": "the dandas of 'लाल । नीली । ...' lit in their pauses, 'लाल,' / 'नीली,' through theirs)"}[PAGE],
          all(not bad and seen == set(range(len(opt[labels[k]]["word_times"]) - 1)) for k, (bad, seen) in enumerate(sync)),
          [(sorted(seen), bad[:2]) for bad, seen in sync])
    check("...taps ignored meanwhile (the right pill tapped during the read-out did nothing)", held == [2, False], held)
    i_w3 = first(lambda s: s["attempts"] == 3)
    i_h3 = next((i for i in range(i_w3, len(tl)) if tl[i]["clip"] == "hint3" and tl[i]["playing"]), None)
    check("...the reveal's line (vo_pick_hint3, “यह सही वाक्य है, इस पर टैप कीजिए”) is said as the right pill is ringed", i_h3 is not None and ms(i_h3) - ms(i_w3) < 2000,
          round(ms(i_h3) - ms(i_w3)) if i_h3 is not None else None)   # [vo-rec]
    check("wrong tap 3: 1 s later the reveal — two pills greyed and dead, the right one ringed green, the 96px hand centred under it",
          [x[0] for k, x in enumerate(rev["dim"]) if k != right] == ["opt-dim", "opt-dim"] and all(x[1] == "none" and x[2] == "0.5" and "grayscale(1)" in x[3] for k, x in enumerate(rev["dim"]) if k != right)
          and rev["dim"][right][0] == "opt-guided" and "rgb(0, 177, 50)" in rev["ring"] and "6px" in rev["ring"]
          and rev["hand"][:2] == [96, 96] and abs(rev["hand"][2] - rev["hand"][3]) <= 1 and -16 <= rev["hand"][4] <= 8, rev)
    i_g = first(lambda s: s["cls"][right].startswith("correct"), i_w3)
    i_gate = first(gone, i_g)
    check("the guided tap (on the hand): the green mark at once, the hand gone, 1 s, then the ding + confetti and no line",
          tl[i_g]["hand"] is None and not any(s["clip"] in ("o1", "o2", "o3") and s["playing"] for s in tl[i_g:]) and any(s["conf"] for s in tl[i_g:i_gate])
          and min(ms(i) for i in range(i_g, len(tl)) if tl[i]["conf"]) - ms(i_g) >= 950, f"confetti {min(ms(i) for i in range(i_g, len(tl)) if tl[i]['conf']) - ms(i_g):.0f} ms after")
    done = [s for s in sig if s["signal"] == "slide_completed"]; rv = [s for s in sig if s["signal"] == "answer_revealed"]
    mst = pg.evaluate("[state.masteryAttempts, state.masteryHits]")
    check(f"...and the page moves on {ON}, recorded as revealed" + (" (one mastery attempt, no hit)" if CFG["mastery"] else ""),
          done and done[0]["success"] is False and len(rv) == 1 and pg.evaluate("CARD.slides[state.idx].id") == NEXT and mst == ([1, 0] if CFG["mastery"] else [0, 0]), (done, rv, mst))
    pg.close()

    # ---- 3. left alone: the idle repeat, and a tap that cuts it
    pg = b.new_page(viewport={"width": 1333, "height": 750}); pg.on("pageerror", lambda e: errs.append(str(e)))
    d, labels, opt, right = run(pg)
    pg.wait_for_timeout(13500)
    tl = timeline(pg)
    ps = [i for i, s in enumerate(tl) if s["clip"] == "prompt" and s["playing"] and (i == 0 or not (tl[i - 1]["clip"] == "prompt" and tl[i - 1]["playing"]))]
    pe = [next(j for j in range(i, len(tl)) if not tl[j]["playing"]) for i in ps if any(not tl[j]["playing"] for j in range(i, len(tl)))]
    gaps = [tl[ps[k + 1]]["ms"] - tl[pe[k]]["ms"] for k in range(min(len(ps) - 1, len(pe)))]
    pops = [tl[i]["pop"] for i in ps]
    check("the instruction repeats ~5 s after each time it ends, with the picture's pop-and-hold (not on entry)",
          len(ps) >= 3 and all(4900 <= g <= 5500 for g in gaps) and pops[0] == "" and all(p == "p6" for p in pops[1:]), f"{len(ps)} plays, gaps {[round(g) for g in gaps]}, pops {pops}")
    pg.wait_for_function(f"isPlaying && currentAudio && currentAudio.src.includes('{d['audio']['prompt']}')", timeout=10000, polling=20); pg.wait_for_timeout(400)
    wr = [i for i in range(3) if i != right]
    pg.click(f"#slideHost .opt-cell >> nth={wr[0]}"); pg.wait_for_timeout(120)
    cut = pg.evaluate("[isPlaying, state.attempts]")
    check("a tap during a repeat cuts it and counts", cut == [False, 1], cut)
    pg.close()

    # ---- 4. against the live P4 (its picture, title and sentences, in its order)
    if REF_PIC:
        bird = pathlib.Path(REF_PIC).resolve().as_uri()
        RAND = "Math.random = (() => { let s = 7; return () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; })();"
        shots = {}; order = None
        for name, url in (("ref", "https://hi-02-h04-l01-s01-dun.vercel.app/"), ("ours", html.as_uri())):
            ctx = b.new_context(viewport={"width": 1333, "height": 750}); ctx.add_init_script(RAND); q = ctx.new_page()
            q.goto(url); q.wait_for_timeout(3000); q.evaluate(LEAVE)
            if name == "ref":
                q.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'P4'))"); q.wait_for_timeout(300); order = q.evaluate(LABELS)
            else:
                q.evaluate("""([bird, order, page]) => { const s = CARD.slides.find(x => x.id === page); s.prompt_hi = 'चित्र के लिए सही वाक्य चुनिए।';
                  CARD.assets.image.test_bird = bird; s.data.recall_image_id = 'test_bird';
                  s.data.options = order.map((l, i) => ({ label_hi: l, audio: s.data.options[i].audio, correct: l === 'चिड़िया दाना चुग रही है।' }));
                  const r = Math.random; Math.random = () => 0.99999; mountSlide(CARD.slides.findIndex(x => x.id === page)); Math.random = r; }""", [bird, order, PAGE])
            q.wait_for_timeout(5000); q.screenshot(path=str(out / f"h_{name}_p4content.png")); shots[name] = out / f"h_{name}_p4content.png"; ctx.close()
        A = np.asarray(Image.open(shots["ours"]).convert("RGB"), np.int16); B = np.asarray(Image.open(shots["ref"]).convert("RGB"), np.int16)
        dd = (np.abs(A - B).max(axis=2) > 32)
        check(f"with P4's own picture, title and sentences {PAGE} pixel-matches the live P4 at rest (>32-level diffs under 0.05%)", dd.sum() / dd.size < 0.0005, f"{int(dd.sum())} px")
    b.close()
check("no page errors", not errs, errs[:3])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
