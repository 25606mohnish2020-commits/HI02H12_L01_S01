"""The stamp page L2 ([stamp-fig] + [stamp-drag] + [stamp-rounds] + [stamp-remind]; frames 565:28, 579:47, 592:89, 593:130, 593:151): mounted straight
(as the dev nav would). The page plays itself to the blinking slot; from there this script is the child: round 1 — it lets the
guidance run (and come again after 7 s), takes hold of the guiding stamp mid-glide, drops it far off, drops the wrong stamp on the
slot, taps a stamp, and drops the right stamp on the slot a little off its centre. After the confetti it watches the clearing (the
stamps' pop played backwards, the words out in reverse, the slot fading) and each later round (the new stamps' pops, the sentence
word by word, the slot): no guidance there — it waits 7 s for the title's line to be said again — drops a wrong stamp on the slot,
then the right one — on each of the round's slots in turn when it has several (593:130: two; 593:151: four, each wanting its own stamp — no confetti between, the stamps the child's again as each box goes); after the last round the end screen. The page's own frame trace (rAF: classes, the slot's opacity and box, the
stamps' boxes and pictures, every frame) and a hook on every media play record the beats; they are checked against each other and
against the clips' word times, so Playwright's own lag never fails a good build. Shots: l2_table.png, l2_stamps.png, l2_slot.png
(the blink paused — compared with Figma's 565:28 render), l2_hint.png, l2_wrong.png, l2_press.png, l2_done.png, l2_confetti.png,
then per later round r: l2_r<r>_set.png (the cleared sheet), l2_r<r>_slot.png (compared with the frame's render), l2_r<r>_idle.png,
l2_r<r>_press.png, l2_r<r>_done.png, l2_r<r>_confetti.png; l2_end.png.
usage: python -I -X utf8 stamp_check.py <index.html> <outdir> [<565:28 render> [<579:47 render> [<592:89 render> [<593:130 render> [<593:151 render>]]]]]  (1280x720 pngs)"""
import sys, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np
html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
refs = [pathlib.Path(a).resolve() for a in sys.argv[3:8]]
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)
LEAVE = """() => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); }"""
HOOK = """(() => { window._plays = []; const P = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function(){ try{ window._plays.push({ src: String(this.src || '').split('/').pop().split('?')[0], t: performance.now(), el: this }); }catch(e){} return P.apply(this, arguments); }; })()"""
PLAYS = "() => window._plays.map(p => ({ src: p.src, t: p.t, paused: p.el.paused, cur: p.el.currentTime, dur: p.el.duration, vol: p.el.volume }))"
RECT = """(sel) => { const e = document.querySelector(sel); if(!e) return null; const b = document.getElementById('stage').getBoundingClientRect(), k = b.width / 1280, r = e.getBoundingClientRect();
  return [(r.left - b.left) / k, (r.top - b.top) / k, r.width / k, r.height / k]; }"""
TRACE = """() => { window.__tr = []; const st = document.getElementById('stage');
  const cs = completeSlide; completeSlide = function(){ window.__csT = performance.now(); return cs.apply(this, arguments); };   // when the page hands over (its own clock)
  const q = (e) => { if(!e) return null; const b = st.getBoundingClientRect(), k = b.width / 1280, r = e.getBoundingClientRect(); return [(r.left - b.left) / k, (r.top - b.top) / k, r.width / k, r.height / k]; };
  (function loop(){ const r = document.querySelector('.stp'); if(!r){ window.__trEnd = performance.now(); return; } const slot = document.querySelector('.stp-slot'), ss = [...document.querySelectorAll('.stp-stamp')];
    window.__tr.push({ t: performance.now(), round: r.dataset.round, lit: r.classList.contains('lit'), live: r.classList.contains('live'), band: !!document.querySelector('.dmf-band.in'), sheet: !!document.querySelector('.stp-sheet.in'),
      tray: !!document.querySelector('.stp-tray.in'), imgs: ss.map(s => s.querySelector('img').className + '|' + s.querySelector('img').src.split('/').pop() + '|' + getComputedStyle(s).display),
      words: document.querySelectorAll('.stp-sent .sfig-w.on').length, nwords: document.querySelectorAll('.stp-sent .sfig-w').length,
      slot: slot ? slot.className : null, slotOp: slot ? +getComputedStyle(slot).opacity : null, slotAnim: slot ? getComputedStyle(slot).animationName : null, slotBox: q(slot),
      slots: [...document.querySelectorAll('.stp-slot')].map(s => ({ cl: s.className, op: +getComputedStyle(s).opacity, anim: getComputedStyle(s).animationName, box: q(s), mark: !!s.querySelector('.stp-mark.in') })), signs: [...document.querySelectorAll('.stp-sign')].map(s => s.className),   // every slot (two in 593:130's round, four in 593:151's); the sign-off lines (593:151)
      mark: !!document.querySelector('.stp-mark.in'), st: ss.map(q), cl: ss.map(s => s.className), conf: !!document.querySelector('.fx-confetti'),
      veil: +getComputedStyle(document.querySelector('.stp-veil')).opacity, nav: getComputedStyle(document.getElementById('navBtn')).display,
      vo: (typeof currentAudio !== 'undefined' && currentAudio) ? [String(currentAudio.src).split('/').pop(), currentAudio.currentTime, currentAudio.ended] : null });
    requestAnimationFrame(loop); })(); }"""
def shot(pg, name): pg.screenshot(path=str(out / name)); return out / name
def first(tr, cond, since=0):
    for f in tr:
        if f["t"] >= since and cond(f): return f
    return None
def ink_box_centre(path, x0, y0, x1, y1):
    A = np.asarray(Image.open(path).convert("RGB").resize((1280, 720), Image.LANCZOS)).astype(int)
    sub = A[y0:y1, x0:x1]; blk = (sub[..., 0] < 90) & (sub[..., 1] < 90) & (sub[..., 2] < 90); ys, xs = np.where(blk)   # the ink's BOX centre (a "?"'s centroid sits high)
    return (round((xs.min() + xs.max()) / 2 + x0, 1), round((ys.min() + ys.max()) / 2 + y0, 1), int(len(xs))) if len(xs) else None
def ink_runs(img1280, y0, y1, x0, x1, gap=12):
    a = np.asarray(img1280).astype(int); blk = (a[..., 0] < 90) & (a[..., 1] < 90) & (a[..., 2] < 90); sub = blk[y0:y1, x0:x1]
    rows = np.where(sub.any(axis=1))[0]; cols = np.where(sub.any(axis=0))[0]
    if not len(cols): return None
    runs = []; s = cols[0]; p = cols[0]
    for c in cols[1:]:
        if c > p + gap: runs.append((int(s) + x0, int(p) + x0)); s = c
        p = c
    runs.append((int(s) + x0, int(p) + x0)); return (int(rows.min()) + y0, int(rows.max()) + y0, runs)
has = lambda cls, name: bool(cls) and name in cls.split()
tipof = lambda r: (r[0] + r[2] / 2, r[1] + r[3])   # a stamp's print point on the frame: the middle of its box's base (it scales about its base)
near = lambda a, c, tol: a is not None and c is not None and abs(a[0] - c[0]) < tol and abs(a[1] - c[1]) < tol
boxnear = lambda a, c, tol: a is not None and all(abs(a[i] - c[i]) < tol for i in range(4))
imgcls = lambda f, k: f["imgs"][k].split("|")[0].split() if len(f["imgs"]) > k else []
imgsrc = lambda f, k: f["imgs"][k].split("|")[1] if len(f["imgs"]) > k else ""
shown_n = lambda f: sum(1 for k in range(len(f["imgs"])) if f["imgs"][k].split("|")[2] != "none")

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(HOOK)
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE)
    now = lambda: pg.evaluate("performance.now()")
    def until(base, ms): pg.wait_for_function(f"performance.now() - {base} >= {ms}", timeout=ms + 8000, polling=20)
    fp = lambda x, y: pg.evaluate("([x, y]) => { const b = document.getElementById('stage').getBoundingClientRect(), k = b.width / 1280; return [b.left + x * k, b.top + y * k]; }", [x, y])
    def drag(a, c, steps=12):   # the child's drag, frame px: down, a dozen moves, up
        x0, y0 = fp(*a); x1, y1 = fp(*c)
        pg.mouse.move(x0, y0); pg.mouse.down(); pg.wait_for_timeout(80)
        for i in range(1, steps + 1): pg.mouse.move(x0 + (x1 - x0) * i / steps, y0 + (y1 - y0) * i / steps); pg.wait_for_timeout(16)
        pg.wait_for_timeout(60); pg.mouse.up()
    ids = pg.evaluate("CARD.slides.map(s => s.id)")
    check("the pages: ... P2, L1 (the letter page), L2 (the stamp page), then the end screen (15)", ids == ["T0", "T0B", "T1", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "L1", "L2", "CEL"], ids)
    D = pg.evaluate("CARD.slides.find(s => s.id === 'L2').data"); P = D["pace"]; RS = D["rounds"]
    slots_of = lambda R: R.get("slots") or [R["slot"]]
    check("five rounds: 565:28 (the ? for the letter's sentence, with the guidance), 579:47 (the comma for the birthday sentence on two rows), 592:89 (the danda for 'मुझे उपहार बहुत पसंद हैं', three stamps), 593:130 (the ? for two questions on two rows: TWO slots), 593:151 (the letter's closing lines on five rows: FOUR slots — the comma, the ?, the danda twice — and the sign-off) — no guidance after the first",
          len(RS) == 5 and [R["mark"] for R in RS] == ["?", ",", "।", "?", "।"] and [R["pick"] for R in RS] == [1, 1, 0, 1, 0] and [len(R["stamps"]) for R in RS] == [2, 2, 3, 3, 3] and RS[0]["guide"] is True and all(R["guide"] is False for R in RS[1:])
          and "\n" in RS[1]["sentence"]["text_hi"] and "\n" in RS[3]["sentence"]["text_hi"] and RS[4]["sentence"]["text_hi"].count("\n") == 4 and [len(R["sentence"]["word_times"]) for R in RS] == [5, 15, 5, 11, 22] and [len(slots_of(R)) for R in RS] == [1, 1, 1, 2, 4]
          and [S_.get("mark", RS[4]["mark"]) for S_ in RS[4]["slots"]] == [",", "?", "।", "।"] and [S_.get("pick", RS[4]["pick"]) for S_ in RS[4]["slots"]] == [2, 1, 0, 0] and [sg["text"] for sg in RS[4]["sign"]] == ["आपकी प्यारी", "पिंकी 🩷"],
          [(R["frame"], R["mark"], R["pick"], len(R["stamps"]), len(R["sentence"]["word_times"]), len(slots_of(R))) for R in RS])
    def geo(R):
        SLS = R.get("slots") or [R["slot"]]; SCS = [(S_["x"] + S_["w"] / 2, S_["y"] + S_["h"] / 2) for S_ in SLS]; SL, sc = SLS[0], SCS[0]; bx = R["boxes"]; tp = R["tips"]   # the round's slots (two in 593:130's, four in 593:151's), the first standing for the round
        PKS = [S_.get("pick", R["pick"]) for S_ in SLS]; MKS = [S_.get("mark", R["mark"]) for S_ in SLS]   # each slot's right stamp and mark (its own, or the round's)
        handles = [(bb[0] + bb[2] / 2, bb[1] + 40) for bb in bx]   # where the child takes hold: the stamps' handles
        onto = lambda k, ox=0, oy=0, j=0: (handles[k][0] + SCS[j][0] - (bx[k][0] + tp[k][0]) + ox, handles[k][1] + SCS[j][1] - (bx[k][1] + tp[k][1]) + oy)   # the finger's place that puts the print point on slot j's centre (+ offset)
        return dict(SL=SL, sc=sc, SLS=SLS, SCS=SCS, PKS=PKS, MKS=MKS, bx=bx, tp=tp, h=handles, onto=onto)
    G = [geo(R) for R in RS]; SL, sc, S0, S1, g0, g1, on_ = G[0]["SL"], G[0]["sc"], G[0]["bx"][0], G[0]["bx"][1], G[0]["h"][0], G[0]["h"][1], G[0]["onto"]; WT = RS[0]["sentence"]["word_times"]
    # the later rounds: which stamp is dropped wrong, where the right one is dropped (off its centre), the render's ink to compare
    LATER = [dict(ri=1, wrong=0, offs=[(10, 8)], lines=[(280, 335, 380, 900, 12), (338, 392, 380, 900, 12)], fills=[(525, 553, 355, 384)], sheet_tol=20),
             dict(ri=2, wrong=1, offs=[(-20, 15)], lines=[(325, 395, 300, 900, 400)], fills=[(751, 786, 331, 388)], sheet_tol=12),
             # round 4 (593:130): the comma dropped wrong on the first slot; the ? on the first slot off its centre, then on the second
             dict(ri=3, wrong=2, offs=[(15, -10), (-12, 12)], lines=[(300, 352, 380, 900, 12), (353, 405, 380, 900, 12)], fills=[(822, 857, 305, 362), (707, 742, 354, 411)], sheet_tol=20),
             # round 5 (593:151): the danda dropped wrong on the comma's slot; then each slot's own stamp in turn (the comma, the ?, the danda, the danda)
             dict(ri=4, wrong=0, offs=[(8, 6), (-10, 10), (12, -8), (-8, -12)], lines=[(175, 228, 440, 870, 10), (228, 277, 440, 870, 10), (277, 326, 440, 870, 10), (326, 375, 440, 870, 10), (375, 425, 440, 870, 10)],
                  fills=[(633, 661, 198, 227), (804, 833, 228, 272), (798, 827, 280, 324), (679, 708, 376, 420)], sheet_tol=20)]
    t0 = pg.evaluate("(() => { const t = performance.now(); mountSlide(CARD.slides.findIndex(s => s.id === 'L2')); return t; })()")
    pg.evaluate(TRACE)
    # ---- live shots at the beats (informative; the checks read the page's own trace)
    pg.wait_for_function("!!document.querySelector('.stp-tray.in')", timeout=15000); until(now(), 550); shot(pg, "l2_table.png")
    pg.wait_for_function("document.querySelectorAll('.stp-stamp img.shown').length === 2", timeout=8000); until(now(), 200); shot(pg, "l2_stamps.png")
    pg.wait_for_function("!!document.querySelector('.stp-slot.in')", timeout=12000); ta = pg.evaluate("getComputedStyle(document.querySelector('.stp-stamp.s0')).touchAction")
    pg.evaluate("document.querySelector('.stp-slot').style.animationPlayState = 'paused'"); until(now(), 350)
    z = shot(pg, "l2_slot.png"); pg.evaluate("document.querySelector('.stp-slot').style.animationPlayState = ''")
    # ---- the child's part, round 1: the guidance runs, comes again after 7 s; a grab mid-guidance; the drops
    pg.wait_for_function("!!document.querySelector('.stp-stamp.s1.lift')", timeout=9000); t_h1 = now(); until(t_h1, P["glide"] + 100); shot(pg, "l2_hint.png")
    pg.wait_for_function("!document.querySelector('.stp-stamp.s1.lift')", timeout=8000); t_h1e = now()
    pg.wait_for_function("!!document.querySelector('.stp-stamp.s1.lift')", timeout=12000); t_h2 = now(); until(t_h2, 700)
    r = pg.evaluate(RECT, ".stp-stamp.s1"); x, y = fp(r[0] + r[2] / 2, r[1] + 40); pg.mouse.move(x, y); pg.mouse.down(); t_grab = now(); pg.wait_for_timeout(120)
    x1, y1 = fp(300, 250)
    for i in range(1, 13): pg.mouse.move(x + (x1 - x) * i / 12, y + (y1 - y) * i / 12); pg.wait_for_timeout(16)
    pg.wait_for_timeout(60); pg.mouse.up(); t_d1 = now(); until(t_d1, 150); wbox = pg.evaluate(RECT, ".stp-stamp.s1"); wbg = pg.evaluate("getComputedStyle(document.querySelector('.stp-stamp.s1')).backgroundColor")
    wshot = shot(pg, "l2_wrong.png"); until(t_d1, P["wiggle"] + P["reset"] + 300)
    drag(g0, on_(0)); t_d2 = now(); until(t_d2, P["wiggle"] + P["reset"] + 300)
    xt, yt = fp(*g1); pg.mouse.move(xt, yt); pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.move(xt + 3, yt + 2); pg.mouse.up(); t_tap = now(); until(t_tap, 450)
    drag(g1, on_(1, 30, 20)); t_d3 = now(); until(t_d3, P["snap"] + P["press"] - 30); shot(pg, "l2_press.png")
    pg.wait_for_function("!!document.querySelector('.stp-slot.gone')", timeout=8000); until(now(), 450); done = shot(pg, "l2_done.png")
    pg.wait_for_function("!!document.querySelector('.fx-confetti')", timeout=8000); until(now(), 500); shot(pg, "l2_confetti.png")
    # ---- the later rounds: the clearing, the round set, the slot; 7 s idle (the title's line again), a wrong drop, the right drop
    LT = []
    for L_ in LATER:
        ri = L_["ri"]; g = G[ri]; rec = dict(L_); nsl = len(g["SLS"])
        pg.wait_for_function(f"document.querySelector('.stp').dataset.round === '{ri}'", timeout=9000); t_set = now(); until(t_set, 150); shot(pg, f"l2_r{ri}_set.png")
        pg.wait_for_function("!!document.querySelector('.stp.live')", timeout=25000); t_live = now()
        pg.evaluate("document.querySelectorAll('.stp-slot').forEach(s => s.style.animationPlayState = 'paused')"); until(now(), 350)
        rec["z"] = shot(pg, f"l2_r{ri}_slot.png"); pg.evaluate("document.querySelectorAll('.stp-slot').forEach(s => s.style.animationPlayState = '')")
        until(t_live, P["idle_ms"] + 900); shot(pg, f"l2_r{ri}_idle.png")   # 7 s without a touch: the title's line again (no guidance in this round)
        pg.wait_for_function("!isPlaying", timeout=10000)
        drag(g["h"][L_["wrong"]], g["onto"](L_["wrong"])); rec["t_wrong"] = now(); until(rec["t_wrong"], P["wiggle"] + P["reset"] + 300)
        rec["dones"] = []
        for j in range(nsl):   # the right stamp on each slot in turn (two in 593:130's round: the second once the first's box has gone and the stamps are the child's again)
            if j: pg.wait_for_function(f"document.querySelectorAll('.stp-slot.gone').length >= {j} && !!document.querySelector('.stp.live')", timeout=8000); until(now(), 300)
            sfx_ = "" if j == 0 else str(j + 1)
            pk = g["PKS"][j]; drag(g["h"][pk], g["onto"](pk, *L_["offs"][j], j)); rec["t_drop"] = now(); until(rec["t_drop"], P["snap"] + P["press"] - 30); shot(pg, f"l2_r{ri}_press{sfx_}.png")
            pg.wait_for_function(f"document.querySelectorAll('.stp-slot.gone').length >= {j + 1}", timeout=8000); until(now(), 450); rec["dones"].append(shot(pg, f"l2_r{ri}_done{sfx_}.png"))
        rec["done"] = rec["dones"][-1]
        pg.wait_for_function("!!document.querySelector('.fx-confetti')", timeout=8000); until(now(), 500); shot(pg, f"l2_r{ri}_confetti.png")
        LT.append(rec)
    pg.wait_for_function("CARD.slides[state.idx].id === 'CEL' && document.body.classList.contains('is-end')", timeout=8000); t_cel = now()
    tr = pg.evaluate("window.__tr"); pl = pg.evaluate(PLAYS); tr_end = pg.evaluate("window.__trEnd || 0"); cs_t = pg.evaluate("window.__csT || 0")
    snd = lambda name: [x for x in pl if x["src"] == name + ".ogg"]
    T = lambda f: round(f["t"] - t0) if f else None
    # ==== 1. the table under the lifting veil; the title bar on its line
    f0 = tr[0]
    check("mounts as a whole-stage page: no आगे, the veil over the table lifting from the first frames, nothing else in yet; two stamp divs shown, the third (for round 3) hidden", f0["nav"] == "none" and not f0["band"] and not f0["sheet"]
          and first(tr, lambda f: f["lit"]) is not None and T(first(tr, lambda f: f["lit"])) < 150 and first(tr, lambda f: f["veil"] < 0.05) is not None and T(first(tr, lambda f: f["veil"] < 0.05)) < 1100 and len(f0["imgs"]) == 3 and shown_n(f0) == 2,
          (f0["nav"], T(first(tr, lambda f: f["lit"])), T(first(tr, lambda f: f["veil"] < 0.05)), f0["imgs"]))
    intro = snd("vo_stamp_intro"); fb = first(tr, lambda f: f["band"])
    voi = lambda f: f["vo"] and f["vo"][0] == "vo_stamp_intro.ogg"
    f_is = first(tr, lambda f: voi(f) and f["vo"][1] > 0)                      # the first frame in which the line is actually sounding
    f_ie = first(tr, lambda f: voi(f) and f["vo"][2])                           # the first frame after it has ended (currentAudio keeps the ended clip until the next play)
    intro1 = [x for x in intro if x["t"] < t_d3]   # the line at the start (said again in the later rounds after idling)
    check("the title's line sounds (~0.4 s in) and the title bar appears the moment it is heard (within 60 ms of the clip's first sounding frame)",
          len(intro1) == 1 and P["intro_at"] - 60 < intro[0]["t"] - t0 < P["intro_at"] + 400 and f_is and fb and -20 < fb["t"] - f_is["t"] < 60,
          (round(intro[0]["t"] - t0) if intro else None, T(f_is), T(fb)))
    # ==== 2. the sheet and the tray, after the line
    fs_, ft = first(tr, lambda f: f["sheet"]), first(tr, lambda f: f["tray"])
    check("the sheet settles onto the table 0.5 s after the line ends (on the clip's own clock), the tray slides up 150 ms later", fs_ and ft and f_ie and abs(fs_["t"] - (f_ie["t"] + P["after_intro"] + P["sheet_in"])) < 200 and 80 < ft["t"] - fs_["t"] < 260,
          (T(fs_), T(ft), T(f_ie)))
    # ==== 3. round 1: the two stamps pop in, each on its pop
    popping = lambda f, k: "pop" in imgcls(f, k) or "shown" in imgcls(f, k)
    fp_ = [first(tr, lambda f, k=k: popping(f, k)) for k in (0, 1)]; pops = snd("sfx_stamp_pop"); pops1 = [x for x in pops if x["t"] < t_d3]
    check("round 1: the two stamps pop into the tray 0.7 s after the sheet, 350 ms apart, each as its pop sounds (the pops at .48)", all(fp_) and len(pops1) == 2 and abs(fp_[0]["t"] - fs_["t"] - P["stamps_at"]) < 120
          and abs(fp_[1]["t"] - fp_[0]["t"] - P["pop_gap"]) < 70 and all(abs(pops1[k]["t"] - fp_[k]["t"]) < 60 for k in (0, 1)) and all(abs(x["vol"] - 0.48) < 0.01 for x in pops),
          ([T(f) for f in fp_], [round(x["t"] - t0) for x in pops1], [round(x["vol"], 2) for x in pops]))
    # ==== 4. round 1's sentence, word by word on the clip's clock
    sent = snd("vo_stamp_sent"); fw = [first(tr, lambda f, n=n: f["words"] >= n) for n in range(1, len(WT) + 1)]
    check("the sentence's clip starts 0.7 s after the second pop", len(sent) == 1 and abs(sent[0]["t"] - fp_[1]["t"] - P["sent_at"]) < 150, round(sent[0]["t"] - fp_[1]["t"]) if sent else None)
    offs = [round(fw[i]["vo"][1] * 1000 - WT[i] * 1000) for i in range(len(WT))] if sent and all(fw) and all(f["vo"] and f["vo"][0] == "vo_stamp_sent.ogg" for f in fw) else None
    check("each of its 5 words appears as the clip reaches it (the clip's clock at the reveal frame within -60..+40 ms of the word's start)", offs is not None and all(-60 <= o <= 40 for o in offs), offs)
    check("the 5 words are all shown, in order, and none before the clip", all(fw) and all(fw[i]["t"] < fw[i + 1]["t"] for i in range(len(fw) - 1)) and fw[0]["t"] >= sent[0]["t"], [T(f) for f in fw])
    # ==== 5. the slot appears as the clip ends and blinks 3.5 s; the stamps are the child's from that moment
    fsl = first(tr, lambda f: has(f["slot"], "in"))
    f_se = first(tr, lambda f: f["vo"] and f["vo"][0] == "vo_stamp_sent.ogg" and f["vo"][2]); s_end = f_se["t"] if f_se else None   # the clip's first ended frame
    fbe = first(tr, lambda f: has(f["slot"], "in") and not has(f["slot"], "blink"), since=fsl["t"] + 500) if fsl else None
    ops = [f["slotOp"] for f in tr if fsl and fbe and fsl["t"] + 200 < f["t"] < fbe["t"]]; dim = min(ops, default=1)
    bk = first(tr, lambda f: has(f["slot"], "blink"))["slotAnim"] if fsl else None
    check("the empty slot appears as the clip ends (within 300 ms) and blinks for 3.5 s just as the pages before (the demos' dmfBlink: three slow blinks, its opacity down to .2 and back)",
          fsl and fbe and s_end and abs(fsl["t"] - s_end) < 300 and abs(fbe["t"] - fsl["t"] - P["blink_ms"]) < 150 and bk == "dmfBlink" and 0.15 <= dim <= 0.3,
          (T(fsl), round(fsl["t"] - s_end) if fsl and s_end else None, round(fbe["t"] - fsl["t"]) if fbe else None, bk, round(dim, 2)))
    fli = first(tr, lambda f: f["live"])
    check("the stamps are the child's from the moment the slot appears (.live, the drag handles' cursor), not before", fli and fsl and abs(fli["t"] - fsl["t"]) < 40 and ta == "none", (T(fli), T(fsl), ta))
    # ==== 6. the guidance: 0.5 s after the blink, the ? stamp glides SLOWLY over the slot, hovers, glides home — no press, no print
    fh1 = first(tr, lambda f: has(f["cl"][1], "lift"), since=fsl["t"] if fsl else 0)
    hover = (sc[0], sc[1] + P["press_down"] - P["hover_up"])   # the print point hovering hover_up px above the press point
    fat = min((f for f in tr if fh1 and fh1["t"] <= f["t"] <= fh1["t"] + P["glide"] + 300 and f["st"][1]), key=lambda f: abs(tipof(f["st"][1])[0] - hover[0]) + abs(tipof(f["st"][1])[1] - hover[1]), default=None)
    fmid = min((f for f in tr if fh1 and f["st"][1]), key=lambda f: abs(f["t"] - (fh1["t"] + P["glide"] * 2 / 3)), default=None)
    dmid = (abs(tipof(fmid["st"][1])[0] - hover[0]) + abs(tipof(fmid["st"][1])[1] - hover[1])) if fmid else None
    check("the guidance starts 0.5 s after the blink ends: the ? stamp lifts and glides over the slot in 1.5 s (its print point within 4 px of the hover point as the glide ends; still 15+ px away two thirds in — a slow glide)",
          fh1 and fbe and abs(fh1["t"] - fbe["t"] - P["hint_at"]) < 150 and fat and abs(fat["t"] - fh1["t"] - P["glide"]) < 200 and near(tipof(fat["st"][1]), hover, 4) and dmid and dmid > 15,
          (round(fh1["t"] - fbe["t"]) if fh1 and fbe else None, round(fat["t"] - fh1["t"]) if fat else None, [round(v, 1) for v in tipof(fat["st"][1])] if fat else None, [round(v, 1) for v in hover], round(dmid, 1) if dmid else None))
    fh1e = first(tr, lambda f: not has(f["cl"][1], "lift"), since=fh1["t"] + 500) if fh1 else None
    home = lambda f, k, bx: f["st"][k] and boxnear(f["st"][k], bx, 1.5)
    fhome1 = first(tr, lambda f: home(f, 1, S1), since=fh1["t"] + 1000) if fh1 else None
    thud = snd("sfx_stamp_press"); fm = first(tr, lambda f: f["mark"]); fgn = first(tr, lambda f: has(f["slot"], "gone"))
    check("it hovers there and glides home (set down ~2.9 s after it lifted, its box within 1.5 px of its place) — nothing printed, no thud, the slot's box still there",
          fh1 and fh1e and abs(fh1e["t"] - fh1["t"] - (P["glide"] + P["hold"] + P["back"] - 150)) < 200 and fhome1 and fhome1["t"] < fh1e["t"] + 250
          and fm and fm["t"] > t_d3 - 50 and fgn and fgn["t"] > t_d3 and not [x for x in thud if x["t"] < t_d3],
          (round(fh1e["t"] - fh1["t"]) if fh1 and fh1e else None, T(fhome1), len([x for x in thud if x["t"] < t_d3])))
    fh2 = first(tr, lambda f: has(f["cl"][1], "lift"), since=fh1e["t"] + 100) if fh1e else None
    check("the guidance comes again 7 s after it was set down (within 7.0..7.5 s: the page's 200 ms tick), and not before", fh2 and 6900 < fh2["t"] - fh1e["t"] < 7500, round(fh2["t"] - fh1e["t"]) if fh2 and fh1e else None)
    # the grab mid-guidance: the stamp stays in hand where it is — no jump — and follows the finger
    fg = first(tr, lambda f: has(f["cl"][1], "drag"), since=fh2["t"] if fh2 else 0); ig = tr.index(fg) if fg else -1
    jump = max(abs(tr[ig]["st"][1][i] - tr[ig - 1]["st"][1][i]) for i in (0, 1)) if ig > 0 and tr[ig]["st"][1] and tr[ig - 1]["st"][1] else None
    fd1 = first(tr, lambda f: not has(f["cl"][1], "drag"), since=fg["t"] + 100) if fg else None
    moved = (fd1["st"][1][0] - fg["st"][1][0], fd1["st"][1][1] - fg["st"][1][1]) if fd1 and fg else None
    want_move = (300 - (r[0] + r[2] / 2), 250 - (r[1] + 40))
    check("taking hold of the guiding stamp mid-glide stops the guidance where it is (no jump: its box moves under 10 px across the grab frame) and it follows the finger (its box moved with the finger within 8 px)",
          fg and 0.5 < (fg["t"] - fh2["t"]) / 1000 < 1.3 and jump is not None and jump < 10 and moved and abs(moved[0] - want_move[0]) < 8 and abs(moved[1] - want_move[1]) < 8,
          (round(fg["t"] - fh2["t"]) if fg and fh2 else None, round(jump, 1) if jump is not None else None, [round(v) for v in moved] if moved else None, [round(v) for v in want_move]))
    # a drop far off the slot: the kit's incorrect buzz (the user's standard sfx_incorrect_feedback), a wiggle where it was dropped, back it glides
    wrongs = snd("sfx_wrong_new"); fw1 = first(tr, lambda f: has(f["cl"][1], "stp-wrong"), since=fg["t"]) if fg else None
    fback1 = first(tr, lambda f: home(f, 1, S1) and not has(f["cl"][1], "lift"), since=fd1["t"]) if fd1 else None
    check("dropped far off the slot: the incorrect buzz sounds as it lands (within 60 ms), it wiggles there (.stp-wrong, the kit's wgNo on its picture), then glides back to its place (set down within 1.4 s), nothing printed",
          fd1 and fw1 and abs(fw1["t"] - fd1["t"]) < 60 and len(wrongs) >= 1 and abs(wrongs[0]["t"] - fw1["t"]) < 60 and fback1 and fback1["t"] - fd1["t"] < P["wiggle"] + P["reset"] + 450 and not fback1["mark"]
          and pg.evaluate("(() => { const s = document.createElement('div'); s.className = 'stp-stamp stp-wrong'; const i = document.createElement('img'); i.className = 'shown'; s.appendChild(i); document.body.appendChild(s); const a = getComputedStyle(i).animationName; s.remove(); return a; })()") == "wgNo",
          (round(wrongs[0]["t"] - fd1["t"]) if wrongs and fd1 else None, round(fback1["t"] - fd1["t"]) if fback1 and fd1 else None))
    WA = np.asarray(Image.open(wshot).convert("RGB").resize((1280, 720), Image.LANCZOS)).astype(float); wx, wy, ww, wh = [int(round(v)) for v in wbox]
    corner = WA[wy + 2:wy + 14, wx + 2:wx + 14].mean(); beside = WA[wy:wy + wh, max(0, wx - 12 - ww):wx - 12].mean()   # the wood to the LEFT of the box (the sheet begins to its right)
    check("no white box behind a stamp dropped on the bare wood: its element's background stays transparent while it wiggles, and the corner of its box in the shot is the wood's colour (not white)",
          wbg in ("rgba(0, 0, 0, 0)", "transparent") and corner < 200 and abs(corner - beside) < 25, (wbg, round(corner, 1), round(beside, 1)))
    # the wrong stamp on the slot: the same
    fg2 = first(tr, lambda f: has(f["cl"][0], "drag"), since=fd1["t"] if fd1 else 0); fd2 = first(tr, lambda f: not has(f["cl"][0], "drag"), since=fg2["t"] + 100) if fg2 else None
    tip2 = tipof(tr[tr.index(fd2) - 1]["st"][0]) if fd2 else None
    fback2 = first(tr, lambda f: home(f, 0, S0) and not has(f["cl"][0], "lift"), since=fd2["t"]) if fd2 else None
    check("the । stamp dropped ON the slot (its print point on the slot's centre): the incorrect buzz, the wiggle, back to its place — nothing printed, the slot still there",
          fd2 and near(tip2, sc, 6) and len(wrongs) >= 2 and abs(wrongs[1]["t"] - fd2["t"]) < 60 and first(tr, lambda f: has(f["cl"][0], "stp-wrong"), since=fd2["t"] - 20)
          and fback2 and fback2["t"] - fd2["t"] < P["wiggle"] + P["reset"] + 450 and not fback2["mark"] and not has(fback2["slot"], "gone"),
          ([round(v) for v in tip2] if tip2 else None, round(wrongs[1]["t"] - fd2["t"]) if len(wrongs) > 1 and fd2 else None, round(fback2["t"] - fd2["t"]) if fback2 and fd2 else None))
    # a tap on a stamp (no move): nothing — no buzz, it stays
    ftap = first(tr, lambda f: has(f["cl"][1], "drag"), since=fback2["t"]) if fback2 else None
    fafter = min((f for f in tr if ftap and f["st"][1]), key=lambda f: abs(f["t"] - (ftap["t"] + 400)), default=None)
    check("a tap on a stamp (a move under 10 px) is a touch, not a placing: no buzz, the stamp is set back down where it is", ftap and len([x for x in wrongs if ftap["t"] < x["t"] < t_d3]) == 0 and fafter and home(fafter, 1, S1) and not has(fafter["cl"][1], "lift"),
          (T(ftap), [round(v, 1) for v in fafter["st"][1]] if fafter else None))
    # the right stamp on the slot, dropped 30 px right and 20 px low of its centre: it snaps over the slot and presses on the thud; the mark; home
    fg3 = first(tr, lambda f: has(f["cl"][1], "drag"), since=ftap["t"] + 300) if ftap else None; fd3 = first(tr, lambda f: not has(f["cl"][1], "drag"), since=fg3["t"] + 100) if fg3 else None
    want = (sc[0], sc[1] + P["press_down"])
    win = [f for f in tr if fd3 and fd3["t"] <= f["t"] <= fd3["t"] + P["snap"] + P["press"] + 300 and f["st"][1]]
    fpress = min(win, key=lambda f: abs(tipof(f["st"][1])[0] - want[0]) + abs(tipof(f["st"][1])[1] - want[1])) if win else None
    tip3 = tipof(fpress["st"][1]) if fpress else None; tipd = tipof(tr[tr.index(fd3) - 1]["st"][1]) if fd3 else None
    check("the ? stamp dropped on the slot (its print point 30 px right, 20 px low of the centre) snaps over the slot and presses: its print point 20 px under the slot's centre (within 4 px) ~0.36 s after the drop",
          fd3 and near(tipd, (sc[0] + 30, sc[1] + 20), 8) and fpress and abs(fpress["t"] - fd3["t"] - (P["snap"] + P["press"])) < 150 and near(tip3, want, 4),
          ([round(v) for v in tipd] if tipd else None, round(fpress["t"] - fd3["t"]) if fpress and fd3 else None, [round(v, 1) for v in tip3] if tip3 else None, [round(v, 1) for v in want]))
    thud1 = [x for x in thud if fd3 and x["t"] < fd3["t"] + 2000]
    check("the stamp thud sounds as it presses (0.28 s after the drop) and the mark is printed at 0.4 s", len(thud1) == 1 and fd3 and abs(thud1[0]["t"] - fd3["t"] - P["thud_at"]) < 80 and fm and abs(fm["t"] - fd3["t"] - P["mark_at"]) < 80,
          (round(thud1[0]["t"] - fd3["t"]) if thud1 and fd3 else None, round(fm["t"] - fd3["t"]) if fm and fd3 else None))
    fh3 = first(tr, lambda f: home(f, 1, S1) and not has(f["cl"][1], "lift"), since=fm["t"]) if fm else None
    check("the stamp lifts and glides back to its place in the tray (within 1.5 px), set down by 1.8 s after the drop", fh3 is not None and fh3["t"] - fd3["t"] < P["back_at"] + P["back_home"] + 200, round(fh3["t"] - fd3["t"]) if fh3 else None)
    corr = snd("sfx_correct_new"); corr1 = [x for x in corr if fd3 and x["t"] < fd3["t"] + 3000]
    check("the slot's box goes 1.6 s after the drop, on the correct chime (the user's standard sfx_correct_feedback, within 60 ms), and the mark stays while the round lasts",
          fgn and fd3 and abs(fgn["t"] - fd3["t"] - P["gone_at"]) < 100 and len(corr1) == 1 and abs(corr1[0]["t"] - fgn["t"]) < 60 and first(tr, lambda f: f["t"] > fgn["t"] + 2000)["mark"],
          (round(fgn["t"] - fd3["t"]) if fgn and fd3 else None, round(corr1[0]["t"] - fgn["t"]) if corr1 and fgn else None))
    fcf = first(tr, lambda f: f["conf"]); cel = [x for x in snd("sfx_celebrate") if fd3 and x["t"] < fd3["t"] + 3500]
    check("confetti comes 2.1 s after the drop, on its own sound (the user's standard sfx confetti, within 100 ms: the sound starts, then the 80 pieces are built)", fcf and fd3 and abs(fcf["t"] - fd3["t"] - P["confetti_at"]) < 100 and len(cel) == 1 and abs(cel[0]["t"] - fcf["t"]) < 100,
          (round(fcf["t"] - fd3["t"]) if fcf and fd3 else None, round(cel[0]["t"] - fcf["t"]) if cel and fcf else None))
    c = ink_box_centre(done, SL["x"] + 1, SL["y"] - 6, SL["x"] + SL["w"] - 1, SL["y"] + SL["h"] + 6)
    check("the printed ? sits with its ink on the slot's centre (within 3 px), on the sheet after the sentence", c and abs(c[0] - sc[0]) < 3 and abs(c[1] - sc[1]) < 3, (c, sc))
    lifts1 = [tr[i]["t"] for i in range(1, len(tr)) if has(tr[i]["cl"][1], "lift") and not has(tr[i - 1]["cl"][1], "lift")]
    # ==== 7. [stamp-rounds] each later round: the clearing after the confetti, the round set, its pops, its sentence, its slot; no guidance,
    #         the title's line again after 7 s; the wrong drop; the right drop; the box gone, confetti
    prev_drop = fd3; prev_n = len(RS[0]["stamps"])
    for L_ in LT:
        ri = L_["ri"]; R = RS[ri]; g = G[ri]; SLS, SCS = g["SLS"], g["SCS"]; nsl = len(SLS); WTr = R["sentence"]["word_times"]; n = len(R["stamps"]); wk = L_["wrong"]; PKS, MKS = g["PKS"], g["MKS"]
        slotz = lambda f, j: f["slots"][j] if len(f["slots"]) > j else None   # slot j's trace in a frame
        unp = lambda f, k: "unpop" in imgcls(f, k)
        fu = [first(tr, lambda f, k=k: unp(f, k), since=prev_drop["t"]) for k in range(prev_n)] if prev_drop else []
        fr = first(tr, lambda f: f["round"] == str(ri))
        check(f"round {ri} -> {ri + 1}: 4.4 s after the drop (the confetti fallen) its {prev_n} stamps shrink away — their pop played backwards, 350 ms apart — with no pop sound",
              all(fu) and abs(fu[0]["t"] - prev_drop["t"] - P["done_at"]) < 120 and all(abs(fu[k]["t"] - fu[k - 1]["t"] - P["pop_gap"]) < 70 for k in range(1, prev_n)) and not [x for x in pops if fu[0]["t"] - 200 < x["t"] < (fr["t"] if fr else 1e12) - 20],
              ([round(f["t"] - prev_drop["t"]) for f in fu] if all(fu) else None))
        seq = [f["words"] for f in tr if fu and fu[0]["t"] <= f["t"] <= fu[0]["t"] + 1000]
        fwo = first(tr, lambda f: f["words"] == 0, since=fu[0]["t"]) if fu and fu[0] else None
        fso = first(tr, lambda f: f["slots"] and all(s_["op"] < 0.05 for s_ in f["slots"]), since=fu[0]["t"]) if fu and fu[0] else None
        check(f"round {ri} -> {ri + 1}: the sentence goes word by word in reverse (the count only falls, to 0 within 0.8 s) and the slot's box fades with its mark (every slot's)", seq and all(b_ <= a_ for a_, b_ in zip(seq, seq[1:])) and fwo and fwo["t"] - fu[0]["t"] < 800 and fso and fso["t"] - fu[0]["t"] < 700,
              (seq[::8][:12], round(fwo["t"] - fu[0]["t"]) if fwo and fu else None, round(fso["t"] - fu[0]["t"]) if fso and fu else None))
        boxes_ok = lambda f: f and len(f["slots"]) == nsl and all(boxnear(f["slots"][j]["box"], [SLS[j]["x"], SLS[j]["y"], SLS[j]["w"], SLS[j]["h"]], 1.5) for j in range(nsl))
        check(f"1.3 s into the clearing round {ri + 1} is set: the new sentence built ({len(WTr)} words, none shown), {nsl} fresh empty slot{'s' if nsl > 1 else ''} at {'their places' if nsl > 1 else 'its place'}, {n} stamp divs shown with the round's pictures, nothing printed",
              fr and fu and abs(fr["t"] - fu[0]["t"] - P["next_at"]) < 120 and fr["nwords"] == len(WTr) and fr["words"] == 0 and len(fr["slots"]) == nsl and not any(has(s_["cl"], "in") for s_ in fr["slots"]) and not fr["mark"] and shown_n(fr) == n
              and all(imgsrc(fr, k) == R["stamps"][k] + ".webp" for k in range(n)) and boxes_ok(fr),
              (round(fr["t"] - fu[0]["t"]) if fr and fu else None, fr["nwords"] if fr else None, [imgsrc(fr, k) for k in range(len(fr["imgs"]))] if fr else None, [[round(v, 1) for v in s_["box"]] for s_ in fr["slots"]] if fr else None))
        fpr = [first(tr, lambda f, k=k: popping(f, k), since=fr["t"]) for k in range(n)] if fr else [None] * n; popsr = [x for x in pops if fr and fr["t"] - 50 < x["t"] < fr["t"] + n * P["pop_gap"] + 500]
        check(f"round {ri + 1}: its {n} stamps pop into the tray as the round is set, 350 ms apart, each as its pop sounds", all(fpr) and len(popsr) == n and fpr[0]["t"] - fr["t"] < 120 and all(abs(fpr[k]["t"] - fpr[k - 1]["t"] - P["pop_gap"]) < 70 for k in range(1, n))
              and all(abs(popsr[k]["t"] - fpr[k]["t"]) < 60 for k in range(n)), ([round(f["t"] - fr["t"]) for f in fpr] if all(fpr) and fr else None, [round(x["t"] - fr["t"]) for x in popsr] if fr else None))
        clip = R["sentence"]["audio"]; sentr = snd(clip); fwr = [first(tr, lambda f, m=m: f["words"] >= m, since=fr["t"]) for m in range(1, len(WTr) + 1)] if fr else []
        offsr = [round(fwr[i]["vo"][1] * 1000 - WTr[i] * 1000) for i in range(len(WTr))] if sentr and fwr and all(fwr) and all(f["vo"] and f["vo"][0] == clip + ".ogg" for f in fwr) else None
        check(f"round {ri + 1}'s clip starts 0.7 s after the last pop and each of its {len(WTr)} words appears as the clip reaches it (the clip's clock at the reveal frame within -60..+40 ms of the word's start)",
              len(sentr) == 1 and all(fpr) and abs(sentr[0]["t"] - fpr[-1]["t"] - P["sent_at"]) < 150 and offsr is not None and all(-60 <= o <= 40 for o in offsr), (round(sentr[0]["t"] - fpr[-1]["t"]) if sentr and all(fpr) else None, offsr))
        fslr = first(tr, lambda f: len(f["slots"]) == nsl and all(has(s_["cl"], "in") for s_ in f["slots"]), since=fr["t"]) if fr else None
        f_ser = first(tr, lambda f: f["vo"] and f["vo"][0] == clip + ".ogg" and f["vo"][2]); s_endr = f_ser["t"] if f_ser else None
        fber = first(tr, lambda f: len(f["slots"]) == nsl and all(has(s_["cl"], "in") and not has(s_["cl"], "blink") for s_ in f["slots"]), since=fslr["t"] + 500) if fslr else None
        opsr = [s_["op"] for f in tr if fslr and fber and fslr["t"] + 200 < f["t"] < fber["t"] for s_ in f["slots"]]; dimr = min(opsr, default=1)
        flir = first(tr, lambda f: f["live"], since=fr["t"]) if fr else None
        where = "; ".join(f"{S_['w']}x{S_['h']} at {S_['x']},{S_['y']}" for S_ in SLS)
        check(f"round {ri + 1}: {'the slot' if nsl == 1 else 'both slots, together,'} ({where}) appear{'s' if nsl == 1 else ''} as the clip ends and blink{'s' if nsl == 1 else ''} 3.5 s as before; the stamps are the child's again",
              fslr and fber and s_endr and abs(fslr["t"] - s_endr) < 300 and abs(fber["t"] - fslr["t"] - P["blink_ms"]) < 150 and all(s_["anim"] == "dmfBlink" for s_ in fslr["slots"]) and 0.15 <= dimr <= 0.3
              and boxes_ok(fslr) and flir and abs(flir["t"] - fslr["t"]) < 40,
              (round(fslr["t"] - s_endr) if fslr and s_endr else None, round(fber["t"] - fslr["t"]) if fber and fslr else None, round(dimr, 2), [[round(v, 1) for v in s_["box"]] for s_ in fslr["slots"]] if fslr else None))
        # no guidance; the title's line again after 7 s; the wrong drop (on the first slot); then the right stamp on each slot in turn
        fgw = first(tr, lambda f: has(f["cl"][wk], "drag"), since=fslr["t"]) if fslr else None; fdw = first(tr, lambda f: not has(f["cl"][wk], "drag"), since=fgw["t"] + 100) if fgw else None
        rem = [x for x in intro if fslr and fgw and fslr["t"] < x["t"] < fgw["t"]]
        f_rs = first(tr, lambda f: voi(f) and f["vo"][1] > 0, since=fslr["t"]) if fslr else None
        nolift = fr and fgw and not [f for f in tr if fr["t"] < f["t"] < fgw["t"] and any(has(c_, "lift") for c_ in f["cl"])]
        check(f"round {ri + 1}: NO guidance — neither after the blink nor after idling: no stamp lifts before the child's own drop; instead, 7 s after the slot appeared without a touch (7.0..7.6 s) the title's line is said again, once",
              nolift and len(rem) == 1 and 6900 < rem[0]["t"] - fslr["t"] < 7600 and f_rs and f_rs["t"] < fgw["t"], (round(rem[0]["t"] - fslr["t"]) if rem and fslr else None, len(rem), T(f_rs), "" if nolift else "a stamp lifted before the drop"))
        wr = [x for x in wrongs if fdw and abs(x["t"] - fdw["t"]) < 150]
        fbackw = first(tr, lambda f: home(f, wk, g["bx"][wk]) and not has(f["cl"][wk], "lift"), since=fdw["t"]) if fdw else None
        check(f"round {ri + 1}: the wrong stamp (#{wk}) dropped on the slot: the incorrect buzz (within 60 ms), the wiggle, back to its place — nothing printed",
              fdw and len(wr) == 1 and abs(wr[0]["t"] - fdw["t"]) < 60 and first(tr, lambda f: has(f["cl"][wk], "stp-wrong"), since=fdw["t"] - 20) and fbackw and fbackw["t"] - fdw["t"] < P["wiggle"] + P["reset"] + 450 and not fbackw["mark"],
              (round(wr[0]["t"] - fdw["t"]) if wr and fdw else None, round(fbackw["t"] - fdw["t"]) if fbackw and fdw else None))
        # the right stamp on each slot in turn: the snap, the press on the thud, the mark there, home; that box gone on the chime — with
        # a slot still empty (593:130), no confetti yet and the stamps the child's again as the box goes; the confetti after the last
        since_ = fdw["t"] if fdw else 0; fdrs = []
        for j in range(nsl):
            SLj, scj = SLS[j], SCS[j]; ox, oy = L_["offs"][j]; pk, mk = PKS[j], MKS[j]; tag = f"round {ri + 1}" + (f", slot {j + 1}" if nsl > 1 else "")
            fgr = first(tr, lambda f: has(f["cl"][pk], "drag"), since=since_); fdr = first(tr, lambda f: not has(f["cl"][pk], "drag"), since=fgr["t"] + 100) if fgr else None
            wantr = (scj[0], scj[1] + P["press_down"])
            winr = [f for f in tr if fdr and fdr["t"] <= f["t"] <= fdr["t"] + P["snap"] + P["press"] + 300 and f["st"][pk]]
            fpressr = min(winr, key=lambda f: abs(tipof(f["st"][pk])[0] - wantr[0]) + abs(tipof(f["st"][pk])[1] - wantr[1])) if winr else None
            tipr = tipof(fpressr["st"][pk]) if fpressr else None; tipdr = tipof(tr[tr.index(fdr) - 1]["st"][pk]) if fdr else None
            fmr = first(tr, lambda f: slotz(f, j) and slotz(f, j)["mark"], since=fr["t"]) if fr else None; thudr = [x for x in thud if fdr and abs(x["t"] - fdr["t"] - P["thud_at"]) < 400]
            check(f"{tag}: the {mk} stamp (its own) dropped on the slot ({ox:+} px, {oy:+} px off its centre) snaps over it and presses (its print point 20 px under the centre, within 4 px); the thud at 0.28 s, the mark printed there at 0.4 s",
                  fdr and near(tipdr, (scj[0] + ox, scj[1] + oy), 8) and fpressr and near(tipr, wantr, 4) and abs(fpressr["t"] - fdr["t"] - (P["snap"] + P["press"])) < 150
                  and len(thudr) == 1 and abs(thudr[0]["t"] - fdr["t"] - P["thud_at"]) < 80 and fmr and abs(fmr["t"] - fdr["t"] - P["mark_at"]) < 80,
                  ([round(v) for v in tipdr] if tipdr else None, [round(v, 1) for v in tipr] if tipr else None, [round(v, 1) for v in wantr], round(thudr[0]["t"] - fdr["t"]) if thudr and fdr else None, round(fmr["t"] - fdr["t"]) if fmr and fdr else None))
            fhr = first(tr, lambda f: home(f, pk, g["bx"][pk]) and not has(f["cl"][pk], "lift"), since=fmr["t"]) if fmr else None
            fgnr = first(tr, lambda f: slotz(f, j) and has(slotz(f, j)["cl"], "gone"), since=fr["t"]) if fr else None; corrr = [x for x in corr if fdr and fdr["t"] < x["t"] < fdr["t"] + 2500]
            check(f"{tag}: the stamp glides home (by 1.8 s); the box goes at 1.6 s on the correct chime (within 60 ms)", fhr and fdr and fhr["t"] - fdr["t"] < P["back_at"] + P["back_home"] + 200 and fgnr and abs(fgnr["t"] - fdr["t"] - P["gone_at"]) < 100
                  and len(corrr) == 1 and abs(corrr[0]["t"] - fgnr["t"]) < 60, (round(fhr["t"] - fdr["t"]) if fhr and fdr else None, round(fgnr["t"] - fdr["t"]) if fgnr and fdr else None, round(corrr[0]["t"] - fgnr["t"]) if corrr and fgnr else None))
            cr = ink_box_centre(L_["dones"][j], SLj["x"] + 1, SLj["y"] - 6, SLj["x"] + SLj["w"] - 1, SLj["y"] + SLj["h"] + 6)
            check(f"{tag}: the printed {mk} sits with its ink on the slot's centre (within 3 px)", cr and abs(cr[0] - scj[0]) < 3 and abs(cr[1] - scj[1]) < 3, (cr, scj))
            if j < nsl - 1:
                fre = first(tr, lambda f: f["live"], since=fdr["t"] + 500) if fdr else None
                celx = [x for x in snd("sfx_celebrate") if fdr and fdr["t"] < x["t"] < fdr["t"] + 3000]; confx = [f for f in tr if fdr and fdr["t"] < f["t"] < fdr["t"] + 3000 and f["conf"]]
                fafter = first(tr, lambda f: f["t"] > fgnr["t"] + 100) if fgnr else None
                check(f"{tag}: with slot {j + 2} still empty — NO confetti after this drop; the stamps are the child's again as the box goes (1.6 s, within 100 ms); the other slot's box still there, unprinted",
                      fre and abs(fre["t"] - fdr["t"] - P["gone_at"]) < 100 and not celx and not confx and fafter and slotz(fafter, j + 1) and not has(slotz(fafter, j + 1)["cl"], "gone") and not slotz(fafter, j + 1)["mark"],
                      (round(fre["t"] - fdr["t"]) if fre and fdr else None, len(celx), len(confx)))
                since_ = fdr["t"] + 100
            fdrs.append(fdr)
        fdr = fdrs[-1]
        if R.get("sign"):
            fsg = first(tr, lambda f: f["signs"] and all("on" in c_.split() for c_ in f["signs"]), since=fr["t"]) if fr else None; fwl = fwr[-1] if fwr and all(fwr) else None
            nxt_ = first(tr, lambda f: f["round"] == str(ri + 1)); fsgo = first(tr, lambda f: f["signs"] and not any("on" in c_.split() for c_ in f["signs"]), since=fdr["t"] + P["done_at"] - 200) if fdr else None
            check(f"round {ri + 1}: the sign-off's {len(R['sign'])} lines ({' / '.join(sg['text'] for sg in R['sign'])}) are built with the round (unshown), arrive with the sentence's last word (within 60 ms) and — when a round follows — go first in the clearing, before the words",
                  fr and len(fr["signs"]) == len(R["sign"]) and not any("on" in c_.split() for c_ in fr["signs"]) and fsg and fwl and abs(fsg["t"] - fwl["t"]) < 60 and (not nxt_ or (fsgo and fdr and abs(fsgo["t"] - fdr["t"] - P["done_at"]) < 120 and fsgo["t"] < nxt_["t"])),
                  (round(fsg["t"] - fwl["t"]) if fsg and fwl else None, round(fsgo["t"] - fdr["t"]) if fsgo and fdr else None))
        fcfr = first(tr, lambda f: f["conf"], since=fdr["t"]) if fdr else None; celr = [x for x in snd("sfx_celebrate") if fdr and fdr["t"] < x["t"] < fdr["t"] + P["done_at"] - 300]
        check(f"round {ri + 1}: confetti 2.1 s after the {'last ' if nsl > 1 else ''}drop, on its own sound (within 100 ms)", fcfr and fdr and abs(fcfr["t"] - fdr["t"] - P["confetti_at"]) < 100 and len(celr) == 1 and abs(celr[0]["t"] - fcfr["t"]) < 100,
              (round(fcfr["t"] - fdr["t"]) if fcfr and fdr else None, round(celr[0]["t"] - fcfr["t"]) if celr and fcfr else None))
        nxt = first(tr, lambda f: f["round"] == str(ri + 1)); t_hi = nxt["t"] if nxt else 1e12
        liftsr = {k: len([i for i in range(1, len(tr)) if fr and fr["t"] < tr[i]["t"] < t_hi and has(tr[i]["cl"][k], "lift") and not has(tr[i - 1]["cl"][k], "lift")]) for k in range(n)}
        expl = {k: sum(1 for j in range(nsl) if PKS[j] == k) + (1 if k == wk else 0) for k in range(n)}   # each stamp: once per slot it is right for, once more for the wrong drop
        check(f"round {ri + 1}: each stamp lifted only in the child's hand — once per slot it is right for, plus the wrong drop's: {expl}", liftsr == expl, liftsr)
        L_["fdr"] = fdr; prev_drop = fdr; prev_n = n
    fr1 = first(tr, lambda f: f["round"] == "1")
    check("the right-hand stamp lifted four times in round 1 (two guidances, the far drop, the right drop): no guidance while the child was at work", fr1 and len([t for t in lifts1 if t < fr1["t"]]) == 4, len([t for t in lifts1 if fr1 and t < fr1["t"]]))
    fdl = LT[-1]["fdr"]
    check("after the last round the page hands over to the end screen 4.4 s after the drop (completeSlide on the page's own clock, within 150 ms), the end screen up within 1.5 s of that, no round gate",
          fdl and cs_t and abs(cs_t - fdl["t"] - P["done_at"]) < 150 and 0 <= t_cel - cs_t < 1500 and not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"),
          (round(cs_t - fdl["t"]) if fdl and cs_t else None, "the end screen seen at", round(t_cel - fdl["t"]) if fdl else None, "the scene gone at", round(tr_end - fdl["t"]) if fdl and tr_end else None))
    until(t_cel, 800); shot(pg, "l2_end.png"); pl = pg.evaluate(PLAYS); own = [x for x in pl if x["src"].startswith("sfx_stamp")]
    check("leaving the page stopped its own sounds (the pops: 2 + 2 + 3 + 3 + 3, and the thud nine times: once a slot)", len(own) == 22 and all(x["paused"] for x in own), [(x["src"], x["paused"]) for x in own])
    # ==== 8. the slot moments against Figma's renders
    if refs and refs[0].exists():
        A = Image.open(z).convert("RGB").resize((1280, 720), Image.LANCZOS); B = Image.open(refs[0]).convert("RGB")
        d = np.asarray(ImageChops.difference(A, B)).astype(float).sum(axis=2)
        Image.fromarray(np.clip(d * 2, 0, 255).astype("uint8")).save(out / "l2_slot_diff.png")
        regions = {"frame": d.mean(), "title bar": d[26:146, 36:1280].mean(), "sheet + sentence + slot": d[150:565, 385:895].mean(), "tray + stamps": d[540:707, 427:853].mean()}
        check("round 1 against Figma's 565:28 render: the whole frame close (mean < 12), the sheet with its sentence and slot close (mean < 12: the text's own edges)", regions["frame"] < 12 and regions["sheet + sentence + slot"] < 12,
              {k: round(v, 2) for k, v in regions.items()})
        ext = ink_runs(A, 325, 395, 300, 750, gap=400)
        check("round 1's sentence ink lies where the render's does (its box within 4 px: x 455..745, y 342..372)", ext and abs(ext[2][0][0] - 455) <= 4 and abs(ext[2][-1][1] - 745) <= 4 and abs(ext[0] - 342) <= 4 and abs(ext[1] - 372) <= 4, ext)
    for L_ in LT:
        ri = L_["ri"]
        if len(refs) > ri and refs[ri].exists():
            A2 = Image.open(L_["z"]).convert("RGB").resize((1280, 720), Image.LANCZOS); B2 = Image.open(refs[ri]).convert("RGB")
            d2 = np.asarray(ImageChops.difference(A2, B2)).astype(float).sum(axis=2)
            Image.fromarray(np.clip(d2 * 2, 0, 255).astype("uint8")).save(out / f"l2_r{ri}_slot_diff.png")
            regions2 = {"frame": d2.mean(), "sheet + sentence + slot": d2[150:565, 385:895].mean(), "tray + stamps": d2[540:707, 427:853].mean()}
            check(f"round {ri + 1} against Figma's {RS[ri]['frame']} render: the whole frame close (mean < 12), the sheet with its sentence and slot close (mean < {L_['sheet_tol']}: the text's own edges)", regions2["frame"] < 12 and regions2["sheet + sentence + slot"] < L_["sheet_tol"],
                  {k: round(v, 2) for k, v in regions2.items()})
            mine = [ink_runs(A2, *ln) for ln in L_["lines"]]; theirs = [ink_runs(B2, *ln) for ln in L_["lines"]]
            ok = all(m and t and abs(m[0] - t[0]) <= 3 and abs(m[1] - t[1]) <= 3 and len(m[2]) == len(t[2]) and all(abs(m[2][i][j] - t[2][i][j]) <= 4 for i in range(len(t[2])) for j in (0, 1)) for m, t in zip(mine, theirs))
            check(f"round {ri + 1}'s sentence rows lie where the render's do (each row's ink rows within 3 px, its runs within 4 px)", ok, (mine, "render:", theirs))
            a2 = np.asarray(A2).astype(int); b2 = np.asarray(B2).astype(int)   # each slot's fill: the slot's own #FFF1B6 (a colour distance under 20) within 6 px of its place (593:151's second and third slots lie 8 px apart), ERODED by a pixel — the fill showing through the stroke's 2 px gaps and the LCD-antialiased fringe of a word 3 px away drop out — mine against the render's, found the same way
            def fillbox(a, fx0, fx1, fy0, fy1):
                w_ = a[fy0 - 6:fy1 + 7, fx0 - 6:fx1 + 7]; m = np.sqrt(((w_ - np.array([255, 241, 182])) ** 2).sum(axis=2)) < 20
                e = m[1:-1, 1:-1] & m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:] & m[:-2, :-2] & m[:-2, 2:] & m[2:, :-2] & m[2:, 2:]
                ys, xs = np.where(e); return (int(xs.min()) + fx0 - 5, int(xs.max()) + fx0 - 5, int(ys.min()) + fy0 - 5, int(ys.max()) + fy0 - 5) if len(xs) else None
            for j, (fx0, fx1, fy0, fy1) in enumerate(L_["fills"]):   # (two slots in 593:130's round, four in 593:151's)
                fm, ft = fillbox(a2, fx0, fx1, fy0, fy1), fillbox(b2, fx0, fx1, fy0, fy1)
                check(f"round {ri + 1}'s slot{' ' + str(j + 1) if len(L_['fills']) > 1 else ''} fill lies where the render's does (the slot at x {fx0}..{fx1}, y {fy0}..{fy1}: the fills' eroded boxes within 2 px of each other — the stroke's inner edge blends a pixel differently in Figma's renders —, inside the slot)", fm and ft and all(abs(fm[i] - ft[i]) <= 2 for i in range(4)) and fx0 <= fm[0] and fm[1] <= fx1 and fy0 <= fm[2] and fm[3] <= fy1, (fm, "render:", ft))
    # ==== 9. a re-run, and leaving mid-way (the dev nav) with a stamp in hand: a clean stop
    pg.evaluate("window._plays = []"); pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'L2'))"); pg.wait_for_timeout(2500)
    check("a re-run from the end screen starts the page over (the table, the bar with its line, round 1)", pg.evaluate("!!document.querySelector('.stp') && !!document.querySelector('.dmf-band.in') && document.querySelector('.stp').dataset.round === '0'") and len(pg.evaluate(PLAYS)) >= 1)
    pg.wait_for_function("!!document.querySelector('.stp.live')", timeout=20000); xt, yt = fp(*g1); pg.mouse.move(xt, yt); pg.mouse.down(); pg.mouse.move(xt + 60, yt - 80); pg.wait_for_timeout(100)
    held = pg.evaluate("document.querySelector('.stp-stamp.s1').className")
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'P2'))"); pg.wait_for_timeout(500); pg.mouse.up(); pg.wait_for_timeout(300); pl = pg.evaluate(PLAYS)
    check("leaving mid-way (to P2) with a stamp in hand: the page's sounds stop, its hook and timers are cleared, its scene is gone, no error", "drag" in held.split() and all(x["paused"] for x in pl if "stamp" in x["src"])
          and pg.evaluate("window.oceanCleanup == null") and pg.evaluate("!document.querySelector('.stp')"), (held, [(x["src"], x["paused"]) for x in pl if "stamp" in x["src"]]))
    check("no page errors", not errs, errs[:3])
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
