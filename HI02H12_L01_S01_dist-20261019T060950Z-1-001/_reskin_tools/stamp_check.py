"""The stamp page L2 ([stamp-fig] + [stamp-drag] + [stamp-rounds], frames 565:28 and 579:47): mounted straight (as the dev nav
would). The page plays itself to the blinking slot; from there this script is the child: it lets the guidance run (and come again
after 7 s), takes hold of the guiding stamp mid-glide, drops it far off, drops the wrong stamp on the slot, taps a stamp, and
drops the right stamp on the slot a little off its centre. After the confetti it watches the clearing (the stamps' pop played
backwards, the words out in reverse, the slot fading) and the second round (the new stamps' pops, the two-row sentence word by
word, the small slot), waits 7 s for the title's line to be said again (no guidance in that round), drops the wrong stamp, then
the right one, and sees the end screen. The page's own
frame trace (rAF: classes, the slot's opacity and box, both stamps' boxes and pictures, every frame) and a hook on every media
play record the beats; they are checked against each other and against the clips' word times, so Playwright's own lag never fails
a good build. Shots: l2_table.png, l2_stamps.png, l2_slot.png (the blink paused — compared with Figma's 565:28 render), l2_hint.png,
l2_wrong.png, l2_press.png, l2_done.png, l2_confetti.png, l2_r2_set.png (the cleared sheet), l2_r2_slot.png (compared with the
579:47 render), l2_r2_idle.png, l2_r2_press.png, l2_r2_done.png, l2_r2_confetti.png, l2_end.png.
usage: python -I -X utf8 stamp_check.py <index.html> <outdir> [<565:28 render 1280x720 png> [<579:47 render 1280x720 png>]]"""
import sys, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np
html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
ref = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
ref2 = pathlib.Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else None
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
  (function loop(){ const r = document.querySelector('.stp'); if(!r){ window.__trEnd = performance.now(); return; } const slot = document.querySelector('.stp-slot'), s0 = document.querySelector('.stp-stamp.s0'), s1 = document.querySelector('.stp-stamp.s1');
    window.__tr.push({ t: performance.now(), round: r.dataset.round, lit: r.classList.contains('lit'), live: r.classList.contains('live'), band: !!document.querySelector('.dmf-band.in'), sheet: !!document.querySelector('.stp-sheet.in'),
      tray: !!document.querySelector('.stp-tray.in'), imgs: [...document.querySelectorAll('.stp-stamp img')].map(i => i.className + '|' + i.src.split('/').pop()),
      words: document.querySelectorAll('.stp-sent .sfig-w.on').length, nwords: document.querySelectorAll('.stp-sent .sfig-w').length,
      slot: slot ? slot.className : null, slotOp: slot ? +getComputedStyle(slot).opacity : null, slotAnim: slot ? getComputedStyle(slot).animationName : null, slotBox: q(slot),
      mark: !!document.querySelector('.stp-mark.in'), st0: q(s0), st1: q(s1), c0: s0.className, c1: s1.className, conf: !!document.querySelector('.fx-confetti'),
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
    check("two rounds: 565:28 (the ? for the letter's sentence) then 579:47 (the comma for the birthday sentence, on two rows)",
          len(RS) == 2 and RS[0]["mark"] == "?" and RS[1]["mark"] == "," and RS[1]["stamps"][1] == "img_stamp_comma" and "\n" in RS[1]["sentence"]["text_hi"] and len(RS[1]["sentence"]["word_times"]) == 15,
          [(R["frame"], R["mark"], len(R["sentence"]["word_times"])) for R in RS])
    def geo(R):
        SL = R["slot"]; sc = (SL["x"] + SL["w"] / 2, SL["y"] + SL["h"] / 2); bx = R["boxes"]; tp = R["tips"]
        handles = [(bb[0] + bb[2] / 2, bb[1] + 40) for bb in bx]   # where the child takes hold: the stamps' handles
        onto = lambda k, ox=0, oy=0: (handles[k][0] + sc[0] - (bx[k][0] + tp[k][0]) + ox, handles[k][1] + sc[1] - (bx[k][1] + tp[k][1]) + oy)   # the finger's place that puts the print point on the slot's centre (+ offset)
        return SL, sc, bx, tp, handles, onto
    SL, sc, S_, TP, g_, on_ = geo(RS[0]); S0, S1 = S_; T0, T1 = TP; g0, g1 = g_; WT = RS[0]["sentence"]["word_times"]
    SL2, sc2, S2_, TP2, g2_, on2_ = geo(RS[1]); WT2 = RS[1]["sentence"]["word_times"]
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
    # ---- the clearing and round 2
    pg.wait_for_function("document.querySelector('.stp').dataset.round === '1'", timeout=9000); t_r2 = now(); until(t_r2, 150); shot(pg, "l2_r2_set.png")
    pg.wait_for_function("!!document.querySelector('.stp.live')", timeout=20000)
    pg.evaluate("document.querySelector('.stp-slot').style.animationPlayState = 'paused'"); until(now(), 350)
    z2 = shot(pg, "l2_r2_slot.png"); pg.evaluate("document.querySelector('.stp-slot').style.animationPlayState = ''")
    t_l2 = now(); until(t_l2, P["idle_ms"] + 700); shot(pg, "l2_r2_idle.png")   # 7 s without a touch: the title's line again (no guidance in this round)
    pg.wait_for_function("!isPlaying", timeout=10000)
    drag(g2_[0], on2_(0)); t_d4 = now(); until(t_d4, P["wiggle"] + P["reset"] + 300)
    drag(g2_[1], on2_(1, 10, 8)); t_d5 = now(); until(t_d5, P["snap"] + P["press"] - 30); shot(pg, "l2_r2_press.png")
    pg.wait_for_function("!!document.querySelector('.stp-slot.gone')", timeout=8000); until(now(), 450); done2 = shot(pg, "l2_r2_done.png")
    pg.wait_for_function("!!document.querySelector('.fx-confetti')", timeout=8000); until(now(), 500); shot(pg, "l2_r2_confetti.png")
    pg.wait_for_function("CARD.slides[state.idx].id === 'CEL' && document.body.classList.contains('is-end')", timeout=8000); t_cel = now()
    tr = pg.evaluate("window.__tr"); pl = pg.evaluate(PLAYS); tr_end = pg.evaluate("window.__trEnd || 0"); cs_t = pg.evaluate("window.__csT || 0")   # the page's hand-over, on its own clock
    snd = lambda name: [x for x in pl if x["src"] == name + ".ogg"]
    T = lambda f: round(f["t"] - t0) if f else None
    # ==== 1. the table under the lifting veil; the title bar on its line
    f0 = tr[0]
    check("mounts as a whole-stage page: no आगे, the veil over the table lifting from the first frames, nothing else in yet", f0["nav"] == "none" and not f0["band"] and not f0["sheet"]
          and first(tr, lambda f: f["lit"]) is not None and T(first(tr, lambda f: f["lit"])) < 150 and first(tr, lambda f: f["veil"] < 0.05) is not None and T(first(tr, lambda f: f["veil"] < 0.05)) < 1100,
          (f0["nav"], T(first(tr, lambda f: f["lit"])), T(first(tr, lambda f: f["veil"] < 0.05))))
    intro = snd("vo_stamp_intro"); fb = first(tr, lambda f: f["band"])
    voi = lambda f: f["vo"] and f["vo"][0] == "vo_stamp_intro.ogg"
    f_is = first(tr, lambda f: voi(f) and f["vo"][1] > 0)                      # the first frame in which the line is actually sounding
    f_ie = first(tr, lambda f: voi(f) and f["vo"][2])                           # the first frame after it has ended (currentAudio keeps the ended clip until the next play)
    intro1 = [x for x in intro if x["t"] < t_d3]   # the line at the start (said again in round 2 after idling)
    check("the title's line sounds (~0.4 s in) and the title bar appears the moment it is heard (within 60 ms of the clip's first sounding frame)",
          len(intro1) == 1 and P["intro_at"] - 60 < intro[0]["t"] - t0 < P["intro_at"] + 400 and f_is and fb and -20 < fb["t"] - f_is["t"] < 60,
          (round(intro[0]["t"] - t0) if intro else None, T(f_is), T(fb)))
    # ==== 2. the sheet and the tray, after the line
    fs_, ft = first(tr, lambda f: f["sheet"]), first(tr, lambda f: f["tray"])
    check("the sheet settles onto the table 0.5 s after the line ends (on the clip's own clock), the tray slides up 150 ms later", fs_ and ft and f_ie and abs(fs_["t"] - (f_ie["t"] + P["after_intro"] + P["sheet_in"])) < 200 and 80 < ft["t"] - fs_["t"] < 260,
          (T(fs_), T(ft), T(f_ie)))
    # ==== 3. round 1: the two stamps pop in, each on its pop
    popping = lambda f, k: len(f["imgs"]) > k and ("pop" in f["imgs"][k].split("|")[0].split() or "shown" in f["imgs"][k].split("|")[0].split())
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
    fh1 = first(tr, lambda f: has(f["c1"], "lift"), since=fsl["t"] if fsl else 0)
    hover = (sc[0], sc[1] + P["press_down"] - P["hover_up"])   # the print point hovering hover_up px above the press point
    fat = min((f for f in tr if fh1 and fh1["t"] <= f["t"] <= fh1["t"] + P["glide"] + 300 and f["st1"]), key=lambda f: abs(tipof(f["st1"])[0] - hover[0]) + abs(tipof(f["st1"])[1] - hover[1]), default=None)
    fmid = min((f for f in tr if fh1 and f["st1"]), key=lambda f: abs(f["t"] - (fh1["t"] + P["glide"] * 2 / 3)), default=None)
    dmid = (abs(tipof(fmid["st1"])[0] - hover[0]) + abs(tipof(fmid["st1"])[1] - hover[1])) if fmid else None
    check("the guidance starts 0.5 s after the blink ends: the ? stamp lifts and glides over the slot in 1.5 s (its print point within 4 px of the hover point as the glide ends; still 15+ px away two thirds in — a slow glide)",
          fh1 and fbe and abs(fh1["t"] - fbe["t"] - P["hint_at"]) < 150 and fat and abs(fat["t"] - fh1["t"] - P["glide"]) < 200 and near(tipof(fat["st1"]), hover, 4) and dmid and dmid > 15,
          (round(fh1["t"] - fbe["t"]) if fh1 and fbe else None, round(fat["t"] - fh1["t"]) if fat else None, [round(v, 1) for v in tipof(fat["st1"])] if fat else None, [round(v, 1) for v in hover], round(dmid, 1) if dmid else None))
    fh1e = first(tr, lambda f: not has(f["c1"], "lift"), since=fh1["t"] + 500) if fh1 else None
    home1 = lambda f: f["st1"] and boxnear(f["st1"], S1, 1.5)
    fhome1 = first(tr, home1, since=fh1["t"] + 1000) if fh1 else None
    thud = snd("sfx_stamp_press"); fm = first(tr, lambda f: f["mark"]); fgn = first(tr, lambda f: has(f["slot"], "gone"))
    check("it hovers there and glides home (set down ~2.9 s after it lifted, its box within 1.5 px of its place) — nothing printed, no thud, the slot's box still there",
          fh1 and fh1e and abs(fh1e["t"] - fh1["t"] - (P["glide"] + P["hold"] + P["back"] - 150)) < 200 and fhome1 and fhome1["t"] < fh1e["t"] + 250
          and fm and fm["t"] > t_d3 - 50 and fgn and fgn["t"] > t_d3 and not [x for x in thud if x["t"] < t_d3],
          (round(fh1e["t"] - fh1["t"]) if fh1 and fh1e else None, T(fhome1), len([x for x in thud if x["t"] < t_d3])))
    fh2 = first(tr, lambda f: has(f["c1"], "lift"), since=fh1e["t"] + 100) if fh1e else None
    check("the guidance comes again 7 s after it was set down (within 7.0..7.5 s: the page's 200 ms tick), and not before", fh2 and 6900 < fh2["t"] - fh1e["t"] < 7500, round(fh2["t"] - fh1e["t"]) if fh2 and fh1e else None)
    # the grab mid-guidance: the stamp stays in hand where it is — no jump — and follows the finger
    fg = first(tr, lambda f: has(f["c1"], "drag"), since=fh2["t"] if fh2 else 0); ig = tr.index(fg) if fg else -1
    jump = max(abs(tr[ig]["st1"][i] - tr[ig - 1]["st1"][i]) for i in (0, 1)) if ig > 0 and tr[ig]["st1"] and tr[ig - 1]["st1"] else None
    fd1 = first(tr, lambda f: not has(f["c1"], "drag"), since=fg["t"] + 100) if fg else None
    moved = (fd1["st1"][0] - fg["st1"][0], fd1["st1"][1] - fg["st1"][1]) if fd1 and fg else None
    want_move = (300 - (r[0] + r[2] / 2), 250 - (r[1] + 40))
    check("taking hold of the guiding stamp mid-glide stops the guidance where it is (no jump: its box moves under 10 px across the grab frame) and it follows the finger (its box moved with the finger within 8 px)",
          fg and 0.5 < (fg["t"] - fh2["t"]) / 1000 < 1.3 and jump is not None and jump < 10 and moved and abs(moved[0] - want_move[0]) < 8 and abs(moved[1] - want_move[1]) < 8,
          (round(fg["t"] - fh2["t"]) if fg and fh2 else None, round(jump, 1) if jump is not None else None, [round(v) for v in moved] if moved else None, [round(v) for v in want_move]))
    # a drop far off the slot: the kit's incorrect buzz (the user's standard sfx_incorrect_feedback), a wiggle where it was dropped, back it glides
    wrongs = snd("sfx_wrong_new"); fw1 = first(tr, lambda f: has(f["c1"], "stp-wrong"), since=fg["t"]) if fg else None
    fback1 = first(tr, lambda f: home1(f) and not has(f["c1"], "lift"), since=fd1["t"]) if fd1 else None
    check("dropped far off the slot: the incorrect buzz sounds as it lands (within 60 ms), it wiggles there (.stp-wrong, the kit's wgNo on its picture), then glides back to its place (set down within 1.4 s), nothing printed",
          fd1 and fw1 and abs(fw1["t"] - fd1["t"]) < 60 and len(wrongs) >= 1 and abs(wrongs[0]["t"] - fw1["t"]) < 60 and fback1 and fback1["t"] - fd1["t"] < P["wiggle"] + P["reset"] + 450 and not fback1["mark"]
          and pg.evaluate("(() => { const s = document.createElement('div'); s.className = 'stp-stamp stp-wrong'; const i = document.createElement('img'); i.className = 'shown'; s.appendChild(i); document.body.appendChild(s); const a = getComputedStyle(i).animationName; s.remove(); return a; })()") == "wgNo",
          (round(wrongs[0]["t"] - fd1["t"]) if wrongs and fd1 else None, round(fback1["t"] - fd1["t"]) if fback1 and fd1 else None))
    WA = np.asarray(Image.open(wshot).convert("RGB").resize((1280, 720), Image.LANCZOS)).astype(float); wx, wy, ww, wh = [int(round(v)) for v in wbox]
    corner = WA[wy + 2:wy + 14, wx + 2:wx + 14].mean(); beside = WA[wy:wy + wh, max(0, wx - 12 - ww):wx - 12].mean()   # the wood to the LEFT of the box (the sheet begins to its right)
    check("no white box behind a stamp dropped on the bare wood: its element's background stays transparent while it wiggles, and the corner of its box in the shot is the wood's colour (not white)",
          wbg in ("rgba(0, 0, 0, 0)", "transparent") and corner < 200 and abs(corner - beside) < 25, (wbg, round(corner, 1), round(beside, 1)))
    # the wrong stamp on the slot: the same
    fg2 = first(tr, lambda f: has(f["c0"], "drag"), since=fd1["t"] if fd1 else 0); fd2 = first(tr, lambda f: not has(f["c0"], "drag"), since=fg2["t"] + 100) if fg2 else None
    tip2 = tipof(tr[tr.index(fd2) - 1]["st0"]) if fd2 else None
    home0 = lambda f: f["st0"] and boxnear(f["st0"], S0, 1.5)
    fback2 = first(tr, lambda f: home0(f) and not has(f["c0"], "lift"), since=fd2["t"]) if fd2 else None
    check("the । stamp dropped ON the slot (its print point on the slot's centre): the incorrect buzz, the wiggle, back to its place — nothing printed, the slot still there",
          fd2 and near(tip2, sc, 6) and len(wrongs) >= 2 and abs(wrongs[1]["t"] - fd2["t"]) < 60 and first(tr, lambda f: has(f["c0"], "stp-wrong"), since=fd2["t"] - 20)
          and fback2 and fback2["t"] - fd2["t"] < P["wiggle"] + P["reset"] + 450 and not fback2["mark"] and not has(fback2["slot"], "gone"),
          ([round(v) for v in tip2] if tip2 else None, round(wrongs[1]["t"] - fd2["t"]) if len(wrongs) > 1 and fd2 else None, round(fback2["t"] - fd2["t"]) if fback2 and fd2 else None))
    # a tap on a stamp (no move): nothing — no buzz, it stays
    ftap = first(tr, lambda f: has(f["c1"], "drag"), since=fback2["t"]) if fback2 else None
    fafter = min((f for f in tr if ftap and f["st1"]), key=lambda f: abs(f["t"] - (ftap["t"] + 400)), default=None)
    check("a tap on a stamp (a move under 10 px) is a touch, not a placing: no buzz, the stamp is set back down where it is", ftap and len([x for x in wrongs if ftap["t"] < x["t"] < t_d3]) == 0 and fafter and home1(fafter) and not has(fafter["c1"], "lift"),
          (T(ftap), [round(v, 1) for v in fafter["st1"]] if fafter else None))
    # the right stamp on the slot, dropped 30 px right and 20 px low of its centre: it snaps over the slot and presses on the thud; the mark; home
    fg3 = first(tr, lambda f: has(f["c1"], "drag"), since=ftap["t"] + 300) if ftap else None; fd3 = first(tr, lambda f: not has(f["c1"], "drag"), since=fg3["t"] + 100) if fg3 else None
    want = (sc[0], sc[1] + P["press_down"])
    win = [f for f in tr if fd3 and fd3["t"] <= f["t"] <= fd3["t"] + P["snap"] + P["press"] + 300 and f["st1"]]
    fpress = min(win, key=lambda f: abs(tipof(f["st1"])[0] - want[0]) + abs(tipof(f["st1"])[1] - want[1])) if win else None
    tip3 = tipof(fpress["st1"]) if fpress else None; tipd = tipof(tr[tr.index(fd3) - 1]["st1"]) if fd3 else None
    check("the ? stamp dropped on the slot (its print point 30 px right, 20 px low of the centre) snaps over the slot and presses: its print point 20 px under the slot's centre (within 4 px) ~0.36 s after the drop",
          fd3 and near(tipd, (sc[0] + 30, sc[1] + 20), 8) and fpress and abs(fpress["t"] - fd3["t"] - (P["snap"] + P["press"])) < 150 and near(tip3, want, 4),
          ([round(v) for v in tipd] if tipd else None, round(fpress["t"] - fd3["t"]) if fpress and fd3 else None, [round(v, 1) for v in tip3] if tip3 else None, [round(v, 1) for v in want]))
    thud1 = [x for x in thud if fd3 and x["t"] < fd3["t"] + 2000]
    check("the stamp thud sounds as it presses (0.28 s after the drop) and the mark is printed at 0.4 s", len(thud1) == 1 and fd3 and abs(thud1[0]["t"] - fd3["t"] - P["thud_at"]) < 80 and fm and abs(fm["t"] - fd3["t"] - P["mark_at"]) < 80,
          (round(thud1[0]["t"] - fd3["t"]) if thud1 and fd3 else None, round(fm["t"] - fd3["t"]) if fm and fd3 else None))
    fh3 = first(tr, lambda f: home1(f) and not has(f["c1"], "lift"), since=fm["t"]) if fm else None
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
    # ==== 7. [stamp-rounds] the clearing after the confetti, then round 2 set
    unp = lambda f, k: len(f["imgs"]) > k and "unpop" in f["imgs"][k].split("|")[0].split()
    fu0 = first(tr, lambda f: unp(f, 0), since=fd3["t"]) if fd3 else None; fu1 = first(tr, lambda f: unp(f, 1), since=fd3["t"]) if fd3 else None
    fr1 = first(tr, lambda f: f["round"] == "1")
    check("4.4 s after the drop (the confetti fallen) the stamps shrink away — their pop played backwards, 350 ms apart — with no pop sound", fu0 and fu1 and abs(fu0["t"] - fd3["t"] - P["done_at"]) < 120 and abs(fu1["t"] - fu0["t"] - P["pop_gap"]) < 70
          and not [x for x in pops if fu0["t"] - 200 < x["t"] < (fr1["t"] if fr1 else 1e12) - 20], (round(fu0["t"] - fd3["t"]) if fu0 and fd3 else None, round(fu1["t"] - fu0["t"]) if fu0 and fu1 else None))
    seq = [f["words"] for f in tr if fu0 and fu0["t"] <= f["t"] <= fu0["t"] + 1000]
    fwo = first(tr, lambda f: f["words"] == 0, since=fu0["t"]) if fu0 else None
    fso = first(tr, lambda f: f["slotOp"] is not None and f["slotOp"] < 0.05, since=fu0["t"]) if fu0 else None
    check("the sentence goes word by word in reverse (the count only falls, 5 -> 0 within 0.5 s) and the slot's box fades with its mark", seq and all(b_ <= a_ for a_, b_ in zip(seq, seq[1:])) and fwo and fwo["t"] - fu0["t"] < 500 and fso and fso["t"] - fu0["t"] < 700,
          (seq[::8][:10], round(fwo["t"] - fu0["t"]) if fwo and fu0 else None, round(fso["t"] - fu0["t"]) if fso and fu0 else None))
    check("1.3 s into the clearing round 2 is set: the new sentence built (15 words, none shown), a fresh empty slot, the । and the comma stamp's pictures in place, nothing printed",
          fr1 and fu0 and abs(fr1["t"] - fu0["t"] - P["next_at"]) < 120 and fr1["nwords"] == 15 and fr1["words"] == 0 and not has(fr1["slot"], "in") and not fr1["mark"]
          and fr1["imgs"][0].endswith("img_stamp_danda.webp") and fr1["imgs"][1].endswith("img_stamp_comma.webp") and boxnear(fr1["slotBox"], [SL2["x"], SL2["y"], SL2["w"], SL2["h"]], 1.5),
          (round(fr1["t"] - fu0["t"]) if fr1 and fu0 else None, fr1["nwords"] if fr1 else None, fr1["imgs"] if fr1 else None, [round(v, 1) for v in fr1["slotBox"]] if fr1 and fr1["slotBox"] else None))
    # ==== 8. round 2: the pops, the two-row sentence word by word, the small slot, the stamps the child's
    fp2 = [first(tr, lambda f, k=k: popping(f, k), since=fr1["t"]) for k in (0, 1)] if fr1 else [None, None]; pops2 = [x for x in pops if fr1 and x["t"] > fr1["t"] - 50]
    check("round 2: the two stamps pop into the tray as the round is set, 350 ms apart, each as its pop sounds", all(fp2) and len(pops2) == 2 and fp2[0]["t"] - fr1["t"] < 120 and abs(fp2[1]["t"] - fp2[0]["t"] - P["pop_gap"]) < 70
          and all(abs(pops2[k]["t"] - fp2[k]["t"]) < 60 for k in (0, 1)), ([round(f["t"] - fr1["t"]) for f in fp2] if all(fp2) and fr1 else None, [round(x["t"] - fr1["t"]) for x in pops2] if fr1 else None))
    sent2 = snd("vo_stamp_sent2"); fw2 = [first(tr, lambda f, n=n: f["words"] >= n, since=fr1["t"]) for n in range(1, len(WT2) + 1)] if fr1 else []
    check("round 2's clip (माँ ने मुझे ...) starts 0.7 s after the second pop", len(sent2) == 1 and all(fp2) and abs(sent2[0]["t"] - fp2[1]["t"] - P["sent_at"]) < 150, round(sent2[0]["t"] - fp2[1]["t"]) if sent2 and all(fp2) else None)
    offs2 = [round(fw2[i]["vo"][1] * 1000 - WT2[i] * 1000) for i in range(len(WT2))] if sent2 and fw2 and all(fw2) and all(f["vo"] and f["vo"][0] == "vo_stamp_sent2.ogg" for f in fw2) else None
    check("each of its 15 words appears as the clip reaches it (the clip's clock at the reveal frame within -60..+40 ms of the word's start; the danda with हैं)", offs2 is not None and all(-60 <= o <= 40 for o in offs2), offs2)
    fsl2 = first(tr, lambda f: has(f["slot"], "in"), since=fr1["t"]) if fr1 else None
    f_se2 = first(tr, lambda f: f["vo"] and f["vo"][0] == "vo_stamp_sent2.ogg" and f["vo"][2]); s_end2 = f_se2["t"] if f_se2 else None
    fbe2 = first(tr, lambda f: has(f["slot"], "in") and not has(f["slot"], "blink"), since=fsl2["t"] + 500) if fsl2 else None
    ops2 = [f["slotOp"] for f in tr if fsl2 and fbe2 and fsl2["t"] + 200 < f["t"] < fbe2["t"]]; dim2 = min(ops2, default=1)
    fli2 = first(tr, lambda f: f["live"], since=fr1["t"]) if fr1 else None
    check("the small slot (29x30 at 525,355, between खिलौने and पेन) appears as the clip ends and blinks 3.5 s as before; the stamps are the child's again",
          fsl2 and fbe2 and s_end2 and abs(fsl2["t"] - s_end2) < 300 and abs(fbe2["t"] - fsl2["t"] - P["blink_ms"]) < 150 and fsl2["slotAnim"] == "dmfBlink" and 0.15 <= dim2 <= 0.3
          and boxnear(fsl2["slotBox"], [SL2["x"], SL2["y"], SL2["w"], SL2["h"]], 1.5) and fli2 and abs(fli2["t"] - fsl2["t"]) < 40,
          (round(fsl2["t"] - s_end2) if fsl2 and s_end2 else None, round(fbe2["t"] - fsl2["t"]) if fbe2 and fsl2 else None, round(dim2, 2), [round(v, 1) for v in fsl2["slotBox"]] if fsl2 and fsl2["slotBox"] else None))
    # ==== 9. round 2: no guidance — the title's line again after 7 s idle; the wrong drop, the right drop (the comma), the end screen
    home1b = lambda f: f["st1"] and boxnear(f["st1"], S2_[1], 1.5)
    fg4 = first(tr, lambda f: has(f["c0"], "drag"), since=fsl2["t"]) if fsl2 else None; fd4 = first(tr, lambda f: not has(f["c0"], "drag"), since=fg4["t"] + 100) if fg4 else None
    rem = [x for x in intro if fsl2 and x["t"] > fsl2["t"]]   # the title's line said again
    f_rs = first(tr, lambda f: voi(f) and f["vo"][1] > 0, since=fsl2["t"]) if fsl2 else None
    nolift = fr1 and fg4 and not [f for f in tr if fr1["t"] < f["t"] < fg4["t"] and (has(f["c0"], "lift") or has(f["c1"], "lift"))]
    check("round 2: NO guidance — neither after the blink nor after idling: no stamp lifts before the child's own drop; instead, 7 s after the slot appeared without a touch (7.0..7.6 s) the title's line is said again, once",
          nolift and len(rem) == 1 and 6900 < rem[0]["t"] - fsl2["t"] < 7600 and f_rs and f_rs["t"] < fg4["t"] and not first(tr, lambda f: f["mark"], since=fr1["t"]) or (first(tr, lambda f: f["mark"], since=fr1["t"])["t"] > t_d5 - 50 and nolift and len(rem) == 1 and 6900 < rem[0]["t"] - fsl2["t"] < 7600),
          (round(rem[0]["t"] - fsl2["t"]) if rem and fsl2 else None, len(rem), T(f_rs), "lifts before the drop" if not nolift else ""))
    home0b = lambda f: f["st0"] and boxnear(f["st0"], S2_[0], 1.5)
    fback4 = first(tr, lambda f: home0b(f) and not has(f["c0"], "lift"), since=fd4["t"]) if fd4 else None
    check("the । stamp dropped on the comma's slot: the incorrect buzz, the wiggle, back to its place — nothing printed", fd4 and len(wrongs) == 3 and abs(wrongs[2]["t"] - fd4["t"]) < 60 and first(tr, lambda f: has(f["c0"], "stp-wrong"), since=fd4["t"] - 20)
          and fback4 and fback4["t"] - fd4["t"] < P["wiggle"] + P["reset"] + 450 and not fback4["mark"], (round(wrongs[2]["t"] - fd4["t"]) if len(wrongs) > 2 and fd4 else None, round(fback4["t"] - fd4["t"]) if fback4 and fd4 else None))
    fg5 = first(tr, lambda f: has(f["c1"], "drag"), since=fd4["t"]) if fd4 else None; fd5 = first(tr, lambda f: not has(f["c1"], "drag"), since=fg5["t"] + 100) if fg5 else None
    want2 = (sc2[0], sc2[1] + P["press_down"])
    win2 = [f for f in tr if fd5 and fd5["t"] <= f["t"] <= fd5["t"] + P["snap"] + P["press"] + 300 and f["st1"]]
    fpress2 = min(win2, key=lambda f: abs(tipof(f["st1"])[0] - want2[0]) + abs(tipof(f["st1"])[1] - want2[1])) if win2 else None
    tip5 = tipof(fpress2["st1"]) if fpress2 else None; tipd5 = tipof(tr[tr.index(fd5) - 1]["st1"]) if fd5 else None
    fm2 = first(tr, lambda f: f["mark"], since=fr1["t"]) if fr1 else None; thud2 = [x for x in thud if fd5 and x["t"] > fd5["t"] - 50]
    check("the comma stamp dropped on the slot (10 px right, 8 px low of its centre) snaps over it and presses (its print point 20 px under the centre, within 4 px); the thud at 0.28 s, the comma printed at 0.4 s",
          fd5 and near(tipd5, (sc2[0] + 10, sc2[1] + 8), 8) and fpress2 and near(tip5, want2, 4) and abs(fpress2["t"] - fd5["t"] - (P["snap"] + P["press"])) < 150
          and len(thud2) == 1 and abs(thud2[0]["t"] - fd5["t"] - P["thud_at"]) < 80 and fm2 and abs(fm2["t"] - fd5["t"] - P["mark_at"]) < 80,
          ([round(v) for v in tipd5] if tipd5 else None, [round(v, 1) for v in tip5] if tip5 else None, [round(v, 1) for v in want2], round(thud2[0]["t"] - fd5["t"]) if thud2 and fd5 else None, round(fm2["t"] - fd5["t"]) if fm2 and fd5 else None))
    fh5 = first(tr, lambda f: home1b(f) and not has(f["c1"], "lift"), since=fm2["t"]) if fm2 else None
    fgn2 = first(tr, lambda f: has(f["slot"], "gone"), since=fr1["t"]) if fr1 else None; corr2 = [x for x in corr if fd5 and x["t"] > fd5["t"]]
    fcf2 = first(tr, lambda f: f["conf"], since=fd5["t"]) if fd5 else None; cel2 = [x for x in snd("sfx_celebrate") if fd5 and fd5["t"] < x["t"] < fd5["t"] + P["done_at"] - 300]
    check("the stamp glides home (by 1.8 s); the box goes at 1.6 s on the correct chime; confetti at 2.1 s on its sound", fh5 and fd5 and fh5["t"] - fd5["t"] < P["back_at"] + P["back_home"] + 200 and fgn2 and abs(fgn2["t"] - fd5["t"] - P["gone_at"]) < 100
          and len(corr2) == 1 and abs(corr2[0]["t"] - fgn2["t"]) < 60 and fcf2 and abs(fcf2["t"] - fd5["t"] - P["confetti_at"]) < 100 and len(cel2) == 1 and abs(cel2[0]["t"] - fcf2["t"]) < 100,
          (round(fh5["t"] - fd5["t"]) if fh5 and fd5 else None, round(fgn2["t"] - fd5["t"]) if fgn2 and fd5 else None, round(fcf2["t"] - fd5["t"]) if fcf2 and fd5 else None))
    c2 = ink_box_centre(done2, SL2["x"] + 1, SL2["y"] - 6, SL2["x"] + SL2["w"] - 1, SL2["y"] + SL2["h"] + 6)
    check("the printed comma sits with its ink on the small slot's centre (within 3 px), between खिलौने and पेन", c2 and abs(c2[0] - sc2[0]) < 3 and abs(c2[1] - sc2[1]) < 3, (c2, sc2))
    check("the page hands over to the end screen 4.4 s after round 2's drop (the confetti fallen; completeSlide on the page's own clock, within 150 ms), the end screen up within 1.5 s of that, no round gate",
          fd5 and cs_t and abs(cs_t - fd5["t"] - P["done_at"]) < 150 and 0 <= t_cel - cs_t < 1500 and not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"),
          (round(cs_t - fd5["t"]) if fd5 and cs_t else None, "the end screen seen at", round(t_cel - fd5["t"]) if fd5 else None, "the scene gone at", round(tr_end - fd5["t"]) if fd5 and tr_end else None))
    lifts = [tr[i]["t"] for i in range(1, len(tr)) if has(tr[i]["c1"], "lift") and not has(tr[i - 1]["c1"], "lift")]
    check("the right-hand stamp lifted four times in round 1 (two guidances, the far drop, the right drop) and once in round 2 (the right drop only): no guidance while the child was at work, none at all in round 2",
          fr1 and len([t for t in lifts if t < fr1["t"]]) == 4 and len([t for t in lifts if t > fr1["t"]]) == 1, (len([t for t in lifts if fr1 and t < fr1["t"]]), len([t for t in lifts if fr1 and t > fr1["t"]])))
    until(t_cel, 800); shot(pg, "l2_end.png"); pl = pg.evaluate(PLAYS); own = [x for x in pl if x["src"].startswith("sfx_stamp")]
    check("leaving the page stopped its own sounds (the two pops and the thud, played twice each)", len(own) == 6 and all(x["paused"] for x in own), [(x["src"], x["paused"]) for x in own])
    # ==== 10. the slot moments against Figma's renders
    if ref and ref.exists():
        A = Image.open(z).convert("RGB").resize((1280, 720), Image.LANCZOS); B = Image.open(ref).convert("RGB")
        d = np.asarray(ImageChops.difference(A, B)).astype(float).sum(axis=2)
        Image.fromarray(np.clip(d * 2, 0, 255).astype("uint8")).save(out / "l2_slot_diff.png")
        regions = {"frame": d.mean(), "title bar": d[26:146, 36:1280].mean(), "sheet + sentence + slot": d[150:565, 385:895].mean(), "tray + stamps": d[540:707, 427:853].mean()}
        check("round 1 against Figma's 565:28 render: the whole frame close (mean < 12), the sheet with its sentence and slot close (mean < 12: the text's own edges)", regions["frame"] < 12 and regions["sheet + sentence + slot"] < 12,
              {k: round(v, 2) for k, v in regions.items()})
        ext = ink_runs(A, 325, 395, 300, 750, gap=400)
        check("round 1's sentence ink lies where the render's does (its box within 4 px: x 455..745, y 342..372)", ext and abs(ext[2][0][0] - 455) <= 4 and abs(ext[2][-1][1] - 745) <= 4 and abs(ext[0] - 342) <= 4 and abs(ext[1] - 372) <= 4, ext)
    if ref2 and ref2.exists():
        A2 = Image.open(z2).convert("RGB").resize((1280, 720), Image.LANCZOS); B2 = Image.open(ref2).convert("RGB")
        d2 = np.asarray(ImageChops.difference(A2, B2)).astype(float).sum(axis=2)
        Image.fromarray(np.clip(d2 * 2, 0, 255).astype("uint8")).save(out / "l2_r2_slot_diff.png")
        regions2 = {"frame": d2.mean(), "sheet + sentence + slot": d2[150:565, 385:895].mean(), "tray + stamps": d2[540:707, 427:853].mean()}
        l1, l2 = ink_runs(A2, 280, 335, 380, 900), ink_runs(A2, 338, 392, 380, 900); r1, r2_ = ink_runs(B2, 280, 335, 380, 900), ink_runs(B2, 338, 392, 380, 900)
        check("round 2 against Figma's 579:47 render: the whole frame close (mean < 12), the sheet with its two-row sentence and slot close (mean < 20: the text's own edges)", regions2["frame"] < 12 and regions2["sheet + sentence + slot"] < 20,
              {k: round(v, 2) for k, v in regions2.items()})
        ok_rows = l1 and l2 and r1 and r2_ and abs(l1[0] - r1[0]) <= 3 and abs(l1[1] - r1[1]) <= 3 and abs(l2[0] - r2_[0]) <= 3 and abs(l2[1] - r2_[1]) <= 3
        ok_runs = l1 and l2 and len(l1[2]) == 1 and len(l2[2]) == 2 and abs(l1[2][0][0] - r1[2][0][0]) <= 4 and abs(l1[2][0][1] - r1[2][0][1]) <= 4 and all(abs(l2[2][i][j] - r2_[2][i][j]) <= 4 for i in (0, 1) for j in (0, 1))
        check("round 2's two rows lie where the render's do (each row's ink rows within 3 px; the first row's run and the second row's two runs, around the slot, within 4 px)", ok_rows and ok_runs, (l1, l2, "render:", r1, r2_))
        a2 = np.asarray(A2).astype(int); yel = (a2[..., 0] > 240) & (a2[..., 1] > 225) & (a2[..., 2] > 150) & (a2[..., 2] < 215); ys, xs = np.where(yel[300:420, 480:600])
        fill = (int(xs.min()) + 480, int(xs.max()) + 480, int(ys.min()) + 300, int(ys.max()) + 300) if len(xs) else None
        check("round 2's slot fill lies where the render's does (x 525..553, y 355..384, within 1 px)", fill and abs(fill[0] - 525) <= 1 and abs(fill[1] - 553) <= 1 and abs(fill[2] - 355) <= 1 and abs(fill[3] - 384) <= 1, fill)
    # ==== 11. a re-run, and leaving mid-way (the dev nav) with a stamp in hand: a clean stop
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
