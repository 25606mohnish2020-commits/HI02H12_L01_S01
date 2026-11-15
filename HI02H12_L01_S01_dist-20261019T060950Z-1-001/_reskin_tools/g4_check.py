"""Verify G4 or P1 (SENT_PICK): the reference game's Page 11 (P4, https://hi-02-h04-l01-s01-dun.vercel.app/) with this
lesson's picture, title and sentences — its look and its flow.
usage: python -I -X utf8 g4_check.py <index.html> <outdir> [--page G4|P1|P2] [--ref <P4's picture png>]
       G4 (the default) and P1 move straight on to the next page; P2 goes through the round-3 gate ("अब आपकी बारी!", [gate-p2])
       to L1, the letter page (since 2026-10-26; until then, with P3-P6 removed, it went straight to the end screen — this entry
       said "CEL" with no gate until [sent-font], 2026-10-27).
       P2's sentences are too long for P4's pill on one line: its pills keep P4's width and font on two lines, all broken
       after the same word, centred on the row's line. [p2-side] (2026-11-15) no longer: P2 is laid out as the row of
       https://hind-dear-story.vercel.app/ page 15 (G2) — the bare picture (1448 wide) in G2's white card on the left, the three
       sentences stacked in G2's option boxes on the right, each on ONE line, the row's middle on G2's line (y 402); the picture's
       pops play on the card and the reveal hand's top sits 56px above the right box's bottom (G2's pointNudgeAt).
       --g2: also read the live G2 and compare the places and looks it shares with P2 (card left edge and middle, card/box gap,
       box y's, heights and right edge, corners, rims, shadows, colours).
       [p2-tap] (2026-11-15) P2's reveal hand TAPS (the reference G2's tap) instead of bobbing: it stands still, its finger presses on
       a 1.3 s beat with G2's ripple + sparks art round the tip — traced frame by frame; with --g2 also frozen at 11 points of the
       cycle against the live G2's #nudgeHand. G4 / P1: the hand still bobs.
       [g4p1-side] (2026-11-15) G4 and P1 in the same side row as P2 (same places, their bare 1448-wide pictures; --g2 works for them);
       --ref (the P4 pixel match) no longer applies to any page and is skipped.
       [g4p1-tap] (2026-11-15) G4's and P1's reveal hands tap like P2's: all three pages get the tap checks (the bob check is unused).
       [g4p1-font] (2026-11-15) G4's and P1's sentences 44px (CFG fs), P2's 28px.
1. The right pill first: the instruction on entry; the tap marks it green at once and pops the picture, nothing sounds for
   1 s (taps wait), then the kit's correct-select, the confetti and the happy Swiftie, and its own line with each word lit
   while the clip is inside that word's window; 0.7 s after the line the page moves on (P2: to the end screen).
   Reported: evidence_qa_first_try (first try), slide_completed success; P1 also one mastery attempt and hit.
2. Three wrong pills, then the guided tap: each wrong tap wiggles the pill ONCE ([wiggle-1] 2026-11-10: the engine's wgNo alone, still from
   0.45 s — the crossed class's buzzShake had shaken it a second time at 0.64 s) (no line of its own), Swiftie tries again, taps
   wait 1 s; then the 1st: the try-again line (the page's hint 1), the pill dead ("crossed") until it ends; the 2nd: [vo-rec3]
   the page's hint 2 line (audio.hint2: vo_g4_hint2 / vo_p1_hint2 / vo_p2_hint2), the pill dead until it ends, no pill read out
   (was: all three pills read in row order — the old deck's hint 2), taps ignored meanwhile; the 3rd: the reveal — two pills greyed and dead, the right one ringed, the 96px hand under it.
   A tap on the hand: the green mark at once, 1 s, the ding + confetti, no line, and the page moves on (success false).
3. Left alone: the instruction again ~5 s after each time it ends (with the picture's pop-and-hold, not on entry); a tap
   during a repeat cuts it and counts. [tap-lock] 2026-10-28: while a FEEDBACK sound or line plays (the buzz, the try-again
   line, hint 3) no pill, not the hand and not the chip answers; the reveal hand is swept when another page mounts. No आगे,
   no hint bulb; the header chip, the picture and the pills where P4 has them.
4. --ref: the page with P4's own picture, title and sentences (same order) pixel-matches the live P4 at rest.
"""
import sys, json, pathlib
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
REF_PIC = sys.argv[sys.argv.index("--ref") + 1] if "--ref" in sys.argv else None
G2 = "--g2" in sys.argv   # [p2-side] compare P2 with the live https://hind-dear-story.vercel.app/ page 15 (G2)
PAGE = sys.argv[sys.argv.index("--page") + 1] if "--page" in sys.argv else "G4"
CFG = {"G4": {"next": "P1", "gate": False, "mastery": False, "right": "लड़की पतंग उड़ा रही है ।", "layout": "side", "pic_w": 1448, "hand_tap": True, "fs": "44px",   # [g4p1-side] P2's row; [g4p1-tap] its hand taps; [g4p1-font] 44px
              "labels": ["लड़की पतंग उड़ा रही है ।", "लड़की । पतंग उड़ा रही है", "लड़की पतंग उड़ा । रही है"]},
       "P1": {"next": "P2", "gate": False, "mastery": True, "right": "क्या यह आपकी किताब है?", "layout": "side", "pic_w": 1448, "hand_tap": True, "fs": "44px",   # [g4p1-side] P2's row; [g4p1-tap] its hand taps; [g4p1-font] 44px
              "labels": ["क्या यह आपकी किताब है?", "क्या? यह आपकी किताब है", "क्या यह आपकी? किताब है"]},
       "P2": {"next": "L1", "gate": True, "mastery": True, "right": "मेरे पास लाल, नीली, हरी और पीली पेंसिल हैं ।", "layout": "side", "pic_w": 1448, "hand_tap": True,   # [p2-side] was "lines": 2; [p2-tap] its reveal hand taps
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
  const cells = [...document.querySelectorAll('#slideHost .opt-cell')], th = document.querySelector('#slideHost .sq-card') || document.querySelector('#slideHost .story-q-thumb'), mi = document.getElementById('swBuddyImg');   // [p2-side] P2's pops play on the card
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
# [wiggle-1] every frame: each pill cell's sideways offset (the wiggles are translateX) and the CSS animations running on the cell itself
WIG = r"""() => { window._wig = []; const step = () => { const cells = [...document.querySelectorAll('#slideHost .opt-cell')];
  if (cells.length === 3) window._wig.push({ ms: performance.now(), tx: cells.map(c => +new DOMMatrix(getComputedStyle(c).transform).m41.toFixed(2)),
    an: cells.map(c => c.getAnimations().map(a => a.animationName).filter(Boolean)) });
  if (CARD.slides[state.idx].id !== window._stopAt) requestAnimationFrame(step); }; requestAnimationFrame(step); }"""

# [p2-tap] the tapping reveal hand: its structure and animations, a 2.7 s per-frame trace (press, place, ripple opacities), and the same
# hand frozen at points of its cycle measured against its own drawn art (for the comparison with the live G2's #nudgeHand)
G2FX = json.loads((pathlib.Path(__file__).resolve().parent / "p2_assets" / "g2_tap_fx.json").read_text(encoding="utf-8"))
TAPINFO = """() => { const h = document.querySelector('.reveal-hand'), img = h.querySelector('.rh-img'), fx = h.querySelector('.rh-fx');
  const A = e => { const cs = getComputedStyle(e); return [cs.animationName, cs.animationDuration, cs.animationTimingFunction, cs.animationIterationCount]; };
  const fcs = fx ? getComputedStyle(fx) : null;
  return { tag: h.tagName, handAnim: getComputedStyle(h).animationName, img: img ? A(img) : null, fx: fx ? [...fx.children].map(A) : [],
    art: fx ? [...fx.children].map(i => getComputedStyle(i).backgroundImage) : [], fxBox: fcs ? [fcs.left, fcs.top, fcs.width, fcs.height] : null,
    fxFirst: !!(fx && img && h.firstElementChild === fx && (fx.compareDocumentPosition(img) & Node.DOCUMENT_POSITION_FOLLOWING)),
    anims: h.getAnimations({ subtree: true }).map(a => [a.animationName, String(a.effect.target.className), a.effect.getTiming().duration, a.startTime]) }; }"""
TAPTRACE = """() => new Promise(res => { const h = document.querySelector('.reveal-hand'), img = h.querySelector('.rh-img'), fx = [...h.querySelectorAll('.rh-fx i')],
  c = document.querySelector('#slideHost .opt-cell.opt-guided'), an = img.getAnimations()[0], out = [], t0 = performance.now();
  const step = () => { const m = new DOMMatrix(getComputedStyle(img).transform), hr = h.getBoundingClientRect(), cr = c.getBoundingClientRect();
    out.push({ ms: performance.now() - t0, ph: an.currentTime % 1300, ty: m.f, sc: m.a, top: hr.top - cr.bottom, left: hr.left, op: fx.map(i => +getComputedStyle(i).opacity) });
    if (performance.now() - t0 < 2700) requestAnimationFrame(step); else res(out); };
  requestAnimationFrame(step); })"""
FROZEN = """([sel, imgSel, fxSel, ts]) => { const h = document.querySelector(sel), img = h.querySelector(imgSel), fx = h.querySelector(fxSel);
  const anims = h.getAnimations({ subtree: true }); anims.forEach(a => a.pause());
  const bw = img.offsetWidth, bh = img.offsetHeight, nw = img.naturalWidth, nh = img.naturalHeight, k = Math.min(bw / nw, bh / nh), aw = nw * k, ah = nh * k,
        ax = img.offsetLeft + (bw - aw) / 2, ay = img.offsetTop + (bh - ah) / 2, fcs = getComputedStyle(fx);
  const geo = [(parseFloat(fcs.left) - ax) / aw, (parseFloat(fcs.top) - ay) / aw, parseFloat(fcs.width) / aw].map(v => +v.toFixed(4));
  const rows = ts.map(t => { anims.forEach(a => a.currentTime = t); const m = new DOMMatrix(getComputedStyle(img).transform);
    return [t, +m.a.toFixed(4), +(m.f / aw).toFixed(4), [...fx.children].map(i => [+(+getComputedStyle(i).opacity).toFixed(3), +new DOMMatrix(getComputedStyle(i).transform).a.toFixed(3)])]; });
  anims.forEach(a => a.play());
  return { geo, rows, art: [...fx.children].map(i => getComputedStyle(i).backgroundImage), aw: +aw.toFixed(3) }; }"""
MEDIA_TRACE = """(() => { window.__media = []; const P = HTMLMediaElement.prototype, op = P.play, oq = P.pause;   // [g4-giggle] every play / pause, with its clock and volume
  P.play = function(){ window.__media.push({ ev: 'play', src: (this.currentSrc || this.src || '').split('/').pop(), at: performance.now(), vol: this.volume, ct: this.currentTime }); return op.apply(this, arguments); };
  P.pause = function(){ window.__media.push({ ev: 'pause', src: (this.currentSrc || this.src || '').split('/').pop(), at: performance.now(), vol: this.volume }); return oq.apply(this, arguments); }; })()"""
def run(pg):
    pg.add_init_script(MEDIA_TRACE); pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE)
    pg.evaluate(f"window._stopAt = '{NEXT}'"); pg.evaluate(SAMPLE); pg.evaluate(WIG); pg.evaluate(f"mountSlide(CARD.slides.findIndex(s => s.id === '{PAGE}'))")
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
      tbox: (() => { const r = document.querySelector('.story-q-thumb').getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; })(),
      card: (() => { const e = document.querySelector('#slideHost .sq-card'); if (!e) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; })(),
      br: document.querySelectorAll('#slideHost .so-br').length, fs: getComputedStyle(document.querySelector('.so-pill')).fontSize,
      pills: [...document.querySelectorAll('.so-pill')].map(p => { const r = p.getBoundingClientRect(); return [r.left, r.top, r.width, r.height, p.scrollWidth <= p.clientWidth]; }),
      lines: [...document.querySelectorAll('.so-pill')].map(p => { const ws = [...p.querySelectorAll('.p2-word')], tops = [...new Set(ws.map(w => Math.round(w.getBoundingClientRect().top)))];
        return tops.map(t => ws.filter(w => Math.round(w.getBoundingClientRect().top) === t).map(w => w.textContent).join(' ')); }) })""")
    check("the title band reads the instruction; no आगे and no hint bulb", look["title"] == d["prompt_hi"] == "सही विराम चिह्न वाला वाक्य चुनिए ।" and look["nav"] == "none" and look["hint"] == "none", look)
    head_ok = look["chip"] == [94.5, 80, 66] and look["thumb"][:2] == [146, 315] and abs(look["thumb"][2] - 666.5) <= 1
    if CFG.get("layout") == "side":   # [p2-side] G2's row (its card's left edge 114.5, the 64px card/box gap, its box y's 234 / 358 / 482 and height 88, the row's middle 402)
        check("G2's row: the chip at 94.5,80; the picture alone in a 492x365 card at x 114.5 centred on y 402 (picture 444x333 at 138.5,235.5); "
              "three 528x88 boxes stacked at x 670.5 (64px right of the card), y 234 / 358 / 482, each sentence on ONE line at " + CFG.get("fs", "28px") + ", nothing spilling, no break",
              look["chip"] == [94.5, 80, 66] and look["card"] == [114.5, 219.5, 492, 365] and look["tbox"] == [138.5, 235.5, 444, 333]
              and [q[:4] for q in look["pills"]] == [[670.5, 234, 528, 88], [670.5, 358, 528, 88], [670.5, 482, 528, 88]] and all(q[4] for q in look["pills"])
              and all(len(l) == 1 for l in look["lines"]) and look["br"] == 0 and look["fs"] == CFG.get("fs", "28px"), look)   # [g4p1-font] G4 / P1 44px, P2 28px
    elif CFG.get("lines", 1) == 1:
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
    check(f"{PAGE}'s own picture ({d['data']['recall_image_id']}) is the one shown", pic == [f"assets/Images/{d['data']['recall_image_id']}.webp", CFG.get("pic_w", 1411)], pic)   # [p2-side] P2's bare picture is 1448 wide
    pg.screenshot(path=str(out / "a_rest.png"))
    pg.click(f"#slideHost .opt-cell >> nth={right}"); pg.wait_for_timeout(300); pg.screenshot(path=str(out / "b_right_300.png"))
    pg.wait_for_timeout(1500); pg.screenshot(path=str(out / "c_right_1800.png"))
    pg.wait_for_function(f"CARD.slides[state.idx].id === '{NEXT}'", timeout=30000, polling=50); pg.wait_for_timeout(150)   # the sampler's next frame logs it
    tl = timeline(pg); sig = pg.evaluate(f"GameBus.signals.filter(s => s.slide_id === '{PAGE}')")
    ms = lambda i: tl[i]["ms"]; first = lambda c, s=0: next(i for i in range(s, len(tl)) if c(tl[i]))
    i_tap = first(lambda s: s["cls"][right].startswith("correct"))
    i_ck = first(lambda s: "ck-correct" in s["cls"][right], i_tap)
    rc = clip_of(opt[labels[right]])   # the right pill's own clip (o1 on G4 / P1, o3 on P2)
    i_ok = first(lambda s: s["clip"] == "ok" and s["playing"], i_tap); i_ok_e = first(lambda s: s["clip"] != "ok" or not s["playing"], i_ok)   # [vo-rec] the praise first; the pill's line follows at once (no "ended" frame)
    i_line = first(lambda s: s["clip"] == rc and s["playing"], i_ok)
    i_end = first(lambda s: s["clip"] == rc and not s["playing"], i_line)
    i_gate = first(gone, i_end)
    # [g4-giggle] G4's right tap: the page's own sound with the pop (the reference's G2 effect), ending with the hold; P1 / P2 have none
    med = pg.evaluate("window.__media || []"); sfx = d["data"].get("tap_sfx")
    if sfx:
        pl = [m for m in med if m["ev"] == "play" and m["src"] == sfx]; pa = [m for m in med if m["ev"] == "pause" and m["src"] == sfx]
        check(f"the right tap: {sfx} starts with the picture's pop (within 60 ms of the green mark) at the reference's .63, once on the page ([g4-giggle])",
              len(pl) == 1 and abs(pl[0]["at"] - ms(i_tap)) <= 60 and abs(pl[0]["vol"] - 0.63) < 0.005 and abs(pl[0]["ct"] - (d["data"].get("tap_sfx_from") or 0)) <= 0.05,   # [p2-pencils] from its first sound where the data says so
              [(round(m["at"] - ms(i_tap)), m["vol"], round(m["ct"], 3)) for m in pl])
        check("...and it ends with the 1 s hold: faded to silence over its last 150 ms and paused ~1 s after the tap, before the ding ([g4-giggle])",
              bool(pa) and 850 <= pa[-1]["at"] - ms(i_tap) <= 1150 and pa[-1]["vol"] <= 0.08 and pa[-1]["at"] <= ms(i_ok) + 60, [(round(m["at"] - ms(i_tap)), round(m["vol"], 3)) for m in pa])
    else:
        check("no tap sound on this page (G4 alone has one, [g4-giggle])", not any("giggle" in m["src"] for m in med))
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

    # ---- [tap-lock] the pointing hand never outlives its page: three wrong pills, the hand, a jump to T1 — no hand there
    pg = b.new_page(viewport={"width": 1333, "height": 750}); pg.on("pageerror", lambda e: errs.append(str(e)))
    d, labels, opt, right = run(pg); wr = [i for i in range(3) if i != right]
    pg.click(f"#slideHost .opt-cell >> nth={wr[0]}")
    pg.wait_for_function("!document.querySelector('#slideHost .opt-cell.crossed') && !isPlaying && !sfxBusy()", timeout=15000, polling=20); pg.wait_for_timeout(300)
    pg.click(f"#slideHost .opt-cell >> nth={wr[1]}")
    pg.wait_for_function("!state.hintActive && !document.querySelector('#slideHost .so-pill.p6-say') && !isPlaying && !sfxBusy()", timeout=30000, polling=20); pg.wait_for_timeout(300)
    pg.click(f"#slideHost .opt-cell >> nth={wr[0]}")
    pg.wait_for_function("!!document.querySelector('.reveal-hand')", timeout=15000, polling=20); pg.wait_for_timeout(300)
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'T1'))"); pg.wait_for_timeout(600)
    gone1 = pg.evaluate("[document.querySelectorAll('.reveal-hand').length, CARD.slides[state.idx].id]"); pg.wait_for_timeout(2500); gone2 = pg.evaluate("document.querySelectorAll('.reveal-hand').length")
    check("the reveal hand does not survive a jump to another page (T1): none there at once, none 2.5 s later ([tap-lock])", gone1 == [0, "T1"] and gone2 == 0, (gone1, gone2))
    pg.close()

    # ---- 2. three wrong pills, then the guided tap
    pg = b.new_page(viewport={"width": 1333, "height": 750}); pg.on("pageerror", lambda e: errs.append(str(e)))
    d, labels, opt, right = run(pg)
    wr = [i for i in range(3) if i != right]
    pg.click(f"#slideHost .opt-cell >> nth={wr[0]}"); pg.wait_for_timeout(150); pg.screenshot(path=str(out / "d_wrong1.png"))
    pg.wait_for_function(f"currentAudio && currentAudio.src.includes('{d['audio']['try_again']}') && isPlaying", timeout=10000, polling=20)   # [vo-rec] the page's try-again line (vo_g4_hint1 / vo_pick_hint1)
    pg.click(f"#slideHost .opt-cell >> nth={right}", force=True); pg.wait_for_timeout(100)   # [tap-lock] a tap while the try-again line speaks
    lockd = pg.evaluate("[state.attempts, !!document.querySelector('#slideHost .opt-cell.correct'), isPlaying]")
    check("a tap on another pill while the try-again line speaks does nothing: the pills wait for silence ([tap-lock])", lockd == [1, False, True], lockd)
    pg.wait_for_function("!document.querySelector('#slideHost .opt-cell.crossed')", timeout=15000, polling=20); pg.wait_for_timeout(300)
    pg.click(f"#slideHost .opt-cell >> nth={wr[1]}")
    pg.wait_for_function(f"currentAudio && currentAudio.src.includes('{d['audio']['hint2']}') && isPlaying", timeout=10000, polling=20); pg.wait_for_timeout(500)   # [vo-rec3] the page's hint 2 line
    pg.screenshot(path=str(out / "e_hint2.png"))
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
    if CFG.get("hand_tap"):   # [p2-tap] the hand taps (the reference G2's tap) instead of bobbing — read every frame for 2.7 s (two cycles)
        ti = pg.evaluate(TAPINFO); tr = pg.evaluate(TAPTRACE)
        pg.screenshot(path=str(out / "f_reveal_tap.png"))
        check("[p2-tap] the reveal hand taps instead of bobbing: it stands still on every frame (its top 56px above the right box's bottom, its left fixed), "
              "no animation on the hand itself (no guidedHandBob anywhere on it)",
              ti["tag"] == "DIV" and ti["handAnim"] == "none" and "guidedHandBob" not in [a[0] for a in ti["anims"]] and len(tr) > 100
              and all(abs(f["top"] + 56) < 0.01 for f in tr) and max(f["left"] for f in tr) - min(f["left"] for f in tr) < 0.01,
              (ti["tag"], ti["handAnim"], sorted({round(f["top"], 2) for f in tr})[:4], len(tr)))
        press = [f for f in tr if 0.45 * 1300 + 12 <= f["ph"] <= 0.62 * 1300 - 12]; rest = [f for f in tr if f["ph"] <= 12 or f["ph"] >= 1300 - 12]
        starts = [round(tr[k]["ms"]) for k in range(1, len(tr)) if tr[k]["ty"] > 5.3 and tr[k - 1]["ty"] <= 5.3]
        check("[p2-tap] ...its finger presses on G2's beat: rhTapP2 1.3 s ease-in-out infinite — down 5.344px and to .93 from 45 % to 62 % of each cycle, "
              "back at rest at 0 / 100 % (G2's nhTapNew, its 6px scaled with the hand); two presses 1.3 s apart in the trace",
              ti["img"] == ["rhTapP2", "1.3s", "ease-in-out", "infinite"] and press and rest
              and all(abs(f["ty"] - 5.344) < 0.01 and abs(f["sc"] - 0.93) < 0.001 for f in press) and all(f["ty"] < 0.2 and f["sc"] > 0.997 for f in rest)
              and abs(max(f["ty"] for f in tr) - 5.344) < 0.01 and len(starts) >= 2 and all(abs(b - a - 1300) <= 40 for a, b in zip(starts, starts[1:])),
              (ti["img"], len(press), len(rest), round(max(f["ty"] for f in tr), 3), round(min(f["sc"] for f in tr), 4), starts))
        check("[p2-tap] ...with G2's ripple + sparks round the fingertip on the same clock: three layers (nhRippleOuter / nhRippleInner / nhSparkPop, "
              "1.3 s ease-out infinite) wearing G2's own art (p2_assets/g2_tap_fx.json), one start time with the press, the layer before the finger (painted under it)",
              [a[:2] for a in ti["fx"]] == [["nhRippleOuter", "1.3s"], ["nhRippleInner", "1.3s"], ["nhSparkPop", "1.3s"]] and all(a[2] == "ease-out" and a[3] == "infinite" for a in ti["fx"])
              and ti["art"] == [f'url("{G2FX[k]}")' for k in ("ro", "ri", "sp")] and len({a[3] for a in ti["anims"]}) == 1 and len(ti["anims"]) == 4 and ti["fxFirst"]
              and all(max(f["op"]) < 0.001 for f in tr if 12 <= f["ph"] <= 0.38 * 1300 - 12) and max(max(f["op"]) for f in tr) > 0.9,
              (ti["fx"], [a[:2] for a in ti["anims"]], ti["art"][0][:40] if ti["art"] else None, ti["fxFirst"]))
        check("[p2-tap] ...the layer placed on the finger as G2's, scaled with the hand: 84.255px at -1.948,-28.133 of the 96px box "
              "(G2's 94.6px at -13.08,-31.48 of its 86x108 box x 0.8906 — 1.1 hand-widths, -0.1521 / -0.3673 of the drawn hand)",
              ti["fxBox"] and all(abs(float(v[:-2]) - w) <= 1 / 64 for v, w in zip(ti["fxBox"], (-1.948, -28.133, 84.255, 84.255))), ti["fxBox"])   # computed sizes snap to 1/64 px
    else:   # G4 / P1 keep the bob
        hb = pg.evaluate("(() => { const h = document.querySelector('.reveal-hand'); return [h.tagName, h.getAnimations().map(a => a.animationName)]; })()")
        check("the reveal hand still bobs here (guidedHandBob; only P2's taps, [p2-tap])", hb == ["IMG", ["guidedHandBob"]], hb)
    pg.click(".reveal-hand", force=True); pg.wait_for_timeout(200)   # force: the hand bobs forever, so it is never "stable"; pg.screenshot(path=str(out / "g_guided_tap.png"))
    pg.wait_for_function(f"CARD.slides[state.idx].id === '{NEXT}'", timeout=30000, polling=50); pg.wait_for_timeout(150)
    tl = timeline(pg); sig = pg.evaluate(f"GameBus.signals.filter(s => s.slide_id === '{PAGE}')")
    ms = lambda i: tl[i]["ms"]; first = lambda c, s=0: next(i for i in range(s, len(tl)) if c(tl[i]))
    i_w1 = first(lambda s: s["attempts"] == 1)
    check("wrong tap 1: the pill wiggles and goes dead, Swiftie tries again, no line of its own",
          "wg-wrong" in tl[i_w1]["cls"][wr[0]] and "crossed" in tl[i_w1]["cls"][wr[0]] and "tryagain" in tl[i_w1 + 2]["mood"]
          and not any(s["clip"] in ("o1", "o2", "o3") and s["playing"] for s in tl[i_w1:i_w1 + 40]), (tl[i_w1]["cls"], tl[i_w1 + 2]["mood"]))
    # [wiggle-1] (2026-11-10) each wrong tap wiggles the tapped pill ONCE: the engine's wgNo alone (the crossed class's old buzzShake had
    # run again as .wg-wrong left at 640 ms), the pill moving only in the wiggle's 0.4 s and still from 0.45 s to 0.95 s (the line / the reveal at 1 s)
    wig = pg.evaluate("window._wig")
    def shakes(t0, k):
        fr = [w for w in wig if t0 - 50 <= w["ms"] <= t0 + 950]
        return sorted({n for w in fr for n in w["an"][k]}), [round(w["ms"] - t0) for w in fr if abs(w["tx"][k]) > 0.3], len(fr)
    wg = [(n, k) + shakes(ms(first(lambda s, n=n: s["attempts"] == n)), k) for n, k in ((1, wr[0]), (2, wr[1]), (3, wr[0]))]
    check("[wiggle-1] every wrong tap (the 1st, 2nd and 3rd) wiggles the tapped pill ONCE: only the engine's wgNo runs on it (no second shake: buzzShake never), it moves only within the first 0.45 s and is still from then to 0.95 s",
          all(r[2] == ["wgNo"] and r[3] and max(r[3]) <= 450 and r[4] > 40 for r in wg), [(n, k, names, (min(mv), max(mv)) if mv else None, nf) for n, k, names, mv, nf in wg])
    i_try = first(lambda s: s["clip"] == "try" and s["playing"], i_w1); i_try_end = first(lambda s: s["clip"] == "try" and not s["playing"], i_try)
    i_unx = first(lambda s: not any("crossed" in c for c in s["cls"]), i_w1)
    check("...1 s later the try-again line; the pill is dead until it ends", 950 <= ms(i_try) - ms(i_w1) <= 1300 and abs(ms(i_unx) - ms(i_try_end)) <= 120,
          f"line {ms(i_try) - ms(i_w1):.0f} ms after the tap, un-crossed {ms(i_unx) - ms(i_try_end):+.0f} ms from its end")
    i_w2 = first(lambda s: s["attempts"] == 2)
    # [vo-rec3] the 2nd wrong pill: the page's own hint 2 line (was the three pills read out)
    i_h2 = first(lambda s: s["clip"] == "hint2" and s["playing"], i_w2); i_h2_end = first(lambda s: s["clip"] != "hint2" or not s["playing"], i_h2)
    i_unx2 = first(lambda s: not any("crossed" in c for c in s["cls"]), i_w2)
    check(f"[vo-rec3] wrong tap 2: 1 s later the page's hint 2 line ({d['audio'].get('hint2')}); the pill is dead until it ends; no pill read out",
          d["audio"].get("hint2") == f"vo_{PAGE.lower()}_hint2" and 950 <= ms(i_h2) - ms(i_w2) <= 1300 and abs(ms(i_unx2) - ms(i_h2_end)) <= 120
          and not any(s["clip"] in ("o1", "o2", "o3") and s["playing"] for s in tl[i_w2:i_h2_end]) and not any(any(s["say"]) for s in tl[i_w2:i_h2_end]),
          f"line {ms(i_h2) - ms(i_w2):.0f} ms after the tap, un-crossed {ms(i_unx2) - ms(i_h2_end):+.0f} ms from its end")
    check("...taps ignored meanwhile (the right pill tapped during hint 2's line did nothing)", held == [2, False], held)
    i_w3 = first(lambda s: s["attempts"] == 3)
    i_h3 = next((i for i in range(i_w3, len(tl)) if tl[i]["clip"] == "hint3" and tl[i]["playing"]), None)
    check("...the reveal's line (vo_pick_hint3, “यह सही वाक्य है, इस पर टैप कीजिए”) is said as the right pill is ringed", i_h3 is not None and ms(i_h3) - ms(i_w3) < 2000,
          round(ms(i_h3) - ms(i_w3)) if i_h3 is not None else None)   # [vo-rec]
    side = CFG.get("layout") == "side"   # [p2-side] G2's pointNudgeAt: the hand's top 56px above the box's bottom (bobbing +2..-14), not under it
    check("wrong tap 3: 1 s later the reveal — two pills greyed and dead, the right one ringed green, the 96px hand centred " + ("on its lower part (G2's place)" if side else "under it"),
          [x[0] for k, x in enumerate(rev["dim"]) if k != right] == ["opt-dim", "opt-dim"] and all(x[1] == "none" and x[2] == "0.5" and "grayscale(1)" in x[3] for k, x in enumerate(rev["dim"]) if k != right)
          and rev["dim"][right][0] == "opt-guided" and "rgb(0, 177, 50)" in rev["ring"] and "6px" in rev["ring"]
          and all(abs(v - 96) <= 0.01 for v in rev["hand"][:2]) and abs(rev["hand"][2] - rev["hand"][3]) <= 1 and ((-72 <= rev["hand"][4] <= -52) if side else (-16 <= rev["hand"][4] <= 8)), rev)
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

    # ---- 3. left alone: the idle repeat and a tap during it (it cuts the repeat: the instruction is no feedback, [tap-lock])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); pg.on("pageerror", lambda e: errs.append(str(e)))
    d, labels, opt, right = run(pg)
    pg.wait_for_timeout(21000)   # [vo-rec] the recorded prompt is ~4.7 s: three plays need ~20 s
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
    check("a tap during a repeat cuts it and counts (the instruction is no feedback, [tap-lock])", cut == [False, 1], cut)
    pg.close()

    # ---- 4. against the live P4 (its picture, title and sentences, in its order) — only for a page still in P4's layout ([g4p1-side]: none now)
    if REF_PIC and CFG.get("layout") == "side":
        print(f"(--ref skipped: {PAGE} is in the G2 side row now, not P4's layout — use --g2)")
    elif REF_PIC:
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

    # ---- 5. [p2-side] against the live G2 of https://hind-dear-story.vercel.app/ (page 15): the places and looks P2 takes from it
    if G2:
        GEO = """([card, pic, box, lbl]) => { const st = document.getElementById('stage'); const sr = st.getBoundingClientRect(), sc = sr.width / st.offsetWidth;
          const R = e => { const r = e.getBoundingClientRect(); return [(r.left - sr.left) / sc, (r.top - sr.top) / sc, r.width / sc, r.height / sc].map(v => +v.toFixed(1)); };
          const S = (e, ps) => { const cs = getComputedStyle(e); return ps.map(p => cs.getPropertyValue(p)); };
          const c = document.querySelector(card), boxes = [...document.querySelectorAll(box)];
          return { card: R(c), boxes: boxes.map(R), cardLook: S(c, ['border-radius', 'border-top', 'box-shadow', 'background-color']),
                   picRadius: getComputedStyle(document.querySelector(pic)).borderTopLeftRadius,
                   boxLook: S(boxes[0], ['border-radius', 'border-top', 'box-shadow', 'background-color', 'padding-left']),
                   text: S(document.querySelector(lbl), ['color', 'font-weight', 'font-family']) }; }"""
        q = b.new_page(viewport={"width": 1333, "height": 750})
        q.goto("https://hind-dear-story.vercel.app/", wait_until="load", timeout=60000); q.wait_for_timeout(3000); q.evaluate(LEAVE)
        q.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'G2'))"); q.wait_for_timeout(12000)   # its boxes come in one by one with the question
        g = q.evaluate(GEO, [".ev-passage", ".ev-pic", "#slideHost .ev-opt", "#slideHost .ev-opt-lbl"]); q.screenshot(path=str(out / "i_g2_live.png")); q.close()
        q = b.new_page(viewport={"width": 1333, "height": 750}); run(q)
        o = q.evaluate(GEO, ["#slideHost .sq-card", "#slideHost .story-q-thumb", "#slideHost .so-pill", "#slideHost .so-pill"]); q.screenshot(path=str(out / "i_p2_side.png")); q.close()
        mid = lambda r: r[1] + r[3] / 2
        check("[p2-side] the live G2's row: the card's left edge and middle, the card -> box gap, the box tops, heights and right edge are P2's",
              g["card"][0] == o["card"][0] and abs(mid(g["card"]) - mid(o["card"])) <= 1.5
              and abs((g["boxes"][0][0] - g["card"][0] - g["card"][2]) - (o["boxes"][0][0] - o["card"][0] - o["card"][2])) <= 0.5
              and [r[1] for r in g["boxes"]] == [r[1] for r in o["boxes"]] and {r[3] for r in g["boxes"]} == {r[3] for r in o["boxes"]} == {88}
              and {round(r[0] + r[2], 1) for r in g["boxes"]} == {round(r[0] + r[2], 1) for r in o["boxes"]}, (g["card"], g["boxes"], o["card"], o["boxes"]))
        check("[p2-side] ...and its looks: the card's 28px corners, 4px white rim, shadow and white; the picture's 18px corners; the boxes' 28px corners, "
              "2px white rim, shadow, white and 16px padding; the sentences' colour, weight and face",
              g["cardLook"] == o["cardLook"] and g["picRadius"] == o["picRadius"] and g["boxLook"] == o["boxLook"] and g["text"] == o["text"],
              {k: (g[k], o[k]) for k in ("cardLook", "picRadius", "boxLook", "text") if g[k] != o[k]})
        if CFG.get("hand_tap"):   # [p2-tap] the tap: G2's #nudgeHand after its 3rd wrong tap vs P2's reveal hand, both frozen at the same points of the 1.3 s cycle
            TS = [0, 200, 450, 585, 650, 720, 806, 900, 1000, 1120, 1250]
            q = b.new_page(viewport={"width": 1333, "height": 750})
            q.goto("https://hind-dear-story.vercel.app/", wait_until="load", timeout=60000); q.wait_for_timeout(3000); q.evaluate(LEAVE)
            q.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'G2'))"); q.wait_for_timeout(12000)
            for i in [0, 2, 0, 2, 0]:   # its wrong boxes are the 1st and 3rd (no shuffle)
                q.wait_for_function("!isPlaying && !state.hintActive", timeout=30000); q.wait_for_timeout(400)
                if q.evaluate("document.getElementById('nudgeHand').classList.contains('show')"): break
                q.query_selector_all("#slideHost .ev-opt")[i].click(force=True); q.wait_for_timeout(1200)
            q.wait_for_function("document.getElementById('nudgeHand').classList.contains('show')", timeout=30000); q.wait_for_timeout(300)
            gt = q.evaluate(FROZEN, ["#nudgeHand", "img", ".nh-tapfx", TS]); q.close()
            q = b.new_page(viewport={"width": 1333, "height": 750}); d2, labels2, opt2, right2 = run(q)
            for i in [k for k in (0, 1, 2) if k != right2] + [next(k for k in (0, 1, 2) if k != right2)]:
                q.wait_for_function("!state.hintActive && !document.querySelector('#slideHost .opt-cell.crossed') && !isPlaying && !sfxBusy()", timeout=30000, polling=20); q.wait_for_timeout(300)
                q.click(f"#slideHost .opt-cell >> nth={i}", force=True)
            q.wait_for_function("!!document.querySelector('.reveal-hand')", timeout=15000, polling=20); q.wait_for_timeout(300)
            ot = q.evaluate(FROZEN, [".reveal-hand", ".rh-img", ".rh-fx", TS]); q.close()
            dif = [(r[0], s[1:], r[1:]) for r, s in zip(gt["rows"], ot["rows"])
                   if abs(r[1] - s[1]) > 0.002 or abs(r[2] - s[2]) > 0.002 or any(abs(a[0] - c[0]) > 0.02 or abs(a[1] - c[1]) > 0.005 for a, c in zip(r[3], s[3]))]
            check("[p2-tap] the live G2's reveal hand: frozen at 11 points of the 1.3 s cycle, P2's finger has G2's press (scale, and drop in hand-widths) and its three "
                  "layers G2's opacity and growth at every point; the layer sits on the drawn hand where G2's does (in hand-widths) and wears G2's art",
                  not dif and all(abs(a - c) <= 0.002 for a, c in zip(gt["geo"], ot["geo"])) and gt["art"] == ot["art"] and len(gt["rows"]) == len(ot["rows"]) == len(TS),
                  {"geo": (gt["geo"], ot["geo"]), "hand widths": (gt["aw"], ot["aw"]), "differ at": dif[:3], "art same": gt["art"] == ot["art"]})
    b.close()
check("no page errors", not errs, errs[:3])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)   # [p2-tap] a FAIL now fails the run (it printed and exited 0 before)
