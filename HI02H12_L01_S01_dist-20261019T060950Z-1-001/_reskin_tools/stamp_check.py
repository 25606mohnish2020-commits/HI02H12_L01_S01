"""The stamp page L2 ([stamp-fig] + [stamp-drag], frame 565:28): mounted straight (as the dev nav would). The page plays itself to the
blinking slot; from there this script is the child: it lets the guidance run (and come again after 7 s), takes hold of the guiding
stamp mid-glide, drops it far off, drops the wrong stamp on the slot, taps a stamp, and drops the right stamp on the slot a little
off its centre. The page's own frame trace (rAF: classes, the slot's opacity, both stamps' boxes, every frame) and a hook on every
media play record the beats; they are checked against each other and against the clips' word times, so Playwright's own lag never
fails a good build. Shots: l2_table.png, l2_stamps.png, l2_slot.png (the blink paused for the shot — compared with Figma's render),
l2_hint.png (the guidance hovering), l2_wrong.png (the far drop), l2_press.png, l2_done.png (the mark left on the sheet),
l2_confetti.png, l2_end.png.
usage: python -I -X utf8 stamp_check.py <index.html> <outdir> [<render 1280x720 png>]"""
import sys, pathlib
from playwright.sync_api import sync_playwright
html = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
ref = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
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
  const q = (sel) => { const e = document.querySelector(sel); if(!e) return null; const b = st.getBoundingClientRect(), k = b.width / 1280, r = e.getBoundingClientRect(); return [(r.left - b.left) / k, (r.top - b.top) / k, r.width / k, r.height / k]; };
  (function loop(){ const r = document.querySelector('.stp'); if(!r) return; const slot = document.querySelector('.stp-slot'), s0 = document.querySelector('.stp-stamp.s0'), s1 = document.querySelector('.stp-stamp.s1');
    window.__tr.push({ t: performance.now(), lit: r.classList.contains('lit'), live: r.classList.contains('live'), band: !!document.querySelector('.dmf-band.in'), sheet: !!document.querySelector('.stp-sheet.in'),
      tray: !!document.querySelector('.stp-tray.in'), stamps: [...document.querySelectorAll('.stp-stamp img')].map(i => i.className), words: document.querySelectorAll('.stp-sent .sfig-w.on').length,
      slot: slot.className, slotOp: +getComputedStyle(slot).opacity, mark: !!document.querySelector('.stp-mark.in'), st0: q('.stp-stamp.s0'), st1: q('.stp-stamp.s1'), c0: s0.className, c1: s1.className,
      conf: !!document.querySelector('.fx-confetti'),
      veil: +getComputedStyle(document.querySelector('.stp-veil')).opacity, nav: getComputedStyle(document.getElementById('navBtn')).display,
      vo: (typeof currentAudio !== 'undefined' && currentAudio) ? [String(currentAudio.src).split('/').pop(), currentAudio.currentTime, currentAudio.ended] : null });
    requestAnimationFrame(loop); })(); }"""
def shot(pg, name): pg.screenshot(path=str(out / name)); return out / name
def first(tr, cond, since=0):
    for f in tr:
        if f["t"] >= since and cond(f): return f
    return None
def ink_centre(path, region):
    from PIL import Image
    import numpy as np
    A = np.asarray(Image.open(path).convert("RGB").resize((1280, 720), Image.LANCZOS)).astype(int)
    x0, y0, x1, y1 = region; sub = A[y0:y1, x0:x1]; blk = (sub[..., 0] < 90) & (sub[..., 1] < 90) & (sub[..., 2] < 90)
    ys, xs = np.where(blk)   # the ink's BOX centre (the centroid of a "?" sits high: its hook holds more ink than its dot)
    return (round((xs.min() + xs.max()) / 2 + x0, 1), round((ys.min() + ys.max()) / 2 + y0, 1), int(len(xs))) if len(xs) else None
has = lambda cls, name: name in cls.split()
tipof = lambda r: (r[0] + r[2] / 2, r[1] + r[3])   # a stamp's print point on the frame: the middle of its box's base (it scales about its base)
near = lambda a, c, tol: a is not None and c is not None and abs(a[0] - c[0]) < tol and abs(a[1] - c[1]) < tol

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
    D = pg.evaluate("CARD.slides.find(s => s.id === 'L2').data"); P = D["pace"]; LY = D["layout"]; WT = D["sentence"]["word_times"]
    SL = LY["slot"]; sc = (SL["x"] + SL["w"] / 2, SL["y"] + SL["h"] / 2); S0, S1 = LY["stamps"]; T0, T1 = LY["tips"]
    g0 = (S0[0] + S0[2] / 2, S0[1] + 40); g1 = (S1[0] + S1[2] / 2, S1[1] + 40)   # where the child takes hold: the stamps' handles
    on0 = (g0[0] + sc[0] - (S0[0] + T0[0]), g0[1] + sc[1] - (S0[1] + T0[1]))      # the finger's place that puts the print point on the slot's centre
    on1 = (g1[0] + sc[0] - (S1[0] + T1[0]) + 30, g1[1] + sc[1] - (S1[1] + T1[1]) + 20)   # the right stamp dropped 30 px right and 20 px low of it
    t0 = pg.evaluate("(() => { const t = performance.now(); mountSlide(CARD.slides.findIndex(s => s.id === 'L2')); return t; })()")
    pg.evaluate(TRACE)
    # live shots at the beats (informative; the checks read the page's own trace)
    pg.wait_for_function("!!document.querySelector('.stp-tray.in')", timeout=15000); until(now(), 550); shot(pg, "l2_table.png")
    pg.wait_for_function("document.querySelectorAll('.stp-stamp img.shown').length === 2", timeout=8000); until(now(), 200); shot(pg, "l2_stamps.png")
    pg.wait_for_function("!!document.querySelector('.stp-slot.in')", timeout=12000); ta = pg.evaluate("getComputedStyle(document.querySelector('.stp-stamp.s0')).touchAction")
    bk = pg.evaluate("getComputedStyle(document.querySelector('.stp-slot')).animationName")
    pg.evaluate("document.querySelector('.stp-slot').style.animationPlayState = 'paused'"); until(now(), 350)
    z = shot(pg, "l2_slot.png"); pg.evaluate("document.querySelector('.stp-slot').style.animationPlayState = ''")
    # the child's part: the guidance runs, comes again after 7 s; a grab mid-guidance; the drops
    pg.wait_for_function("!!document.querySelector('.stp-stamp.s1.lift')", timeout=9000); t_h1 = now(); until(t_h1, P["glide"] + 100); shot(pg, "l2_hint.png")
    pg.wait_for_function("!document.querySelector('.stp-stamp.s1.lift')", timeout=8000); t_h1e = now()
    pg.wait_for_function("!!document.querySelector('.stp-stamp.s1.lift')", timeout=12000); t_h2 = now(); until(t_h2, 700)
    r = pg.evaluate(RECT, ".stp-stamp.s1"); x, y = fp(r[0] + r[2] / 2, r[1] + 40); pg.mouse.move(x, y); pg.mouse.down(); t_grab = now(); pg.wait_for_timeout(120)
    x1, y1 = fp(300, 250)
    for i in range(1, 13): pg.mouse.move(x + (x1 - x) * i / 12, y + (y1 - y) * i / 12); pg.wait_for_timeout(16)
    pg.wait_for_timeout(60); pg.mouse.up(); t_d1 = now(); until(t_d1, 150); wbox = pg.evaluate(RECT, ".stp-stamp.s1"); wbg = pg.evaluate("getComputedStyle(document.querySelector('.stp-stamp.s1')).backgroundColor")
    wshot = shot(pg, "l2_wrong.png"); until(t_d1, P["wiggle"] + P["reset"] + 300)
    drag(g0, on0); t_d2 = now(); until(t_d2, P["wiggle"] + P["reset"] + 300)
    xt, yt = fp(*g1); pg.mouse.move(xt, yt); pg.mouse.down(); pg.wait_for_timeout(80); pg.mouse.move(xt + 3, yt + 2); pg.mouse.up(); t_tap = now(); until(t_tap, 450)
    drag(g1, on1); t_d3 = now(); until(t_d3, P["snap"] + P["press"] - 30); shot(pg, "l2_press.png")
    pg.wait_for_function("!!document.querySelector('.stp-slot.gone')", timeout=8000); until(now(), 450); done = shot(pg, "l2_done.png")
    pg.wait_for_function("!!document.querySelector('.fx-confetti')", timeout=8000); until(now(), 500); shot(pg, "l2_confetti.png")
    pg.wait_for_function("CARD.slides[state.idx].id === 'CEL' && document.body.classList.contains('is-end')", timeout=8000); t_cel = now()
    tr = pg.evaluate("window.__tr"); pl = pg.evaluate(PLAYS)
    snd = lambda prefix: [x for x in pl if x["src"].startswith(prefix)]
    T = lambda f: round(f["t"] - t0) if f else None
    # 1. the table under the lifting veil; the title bar on its line
    f0 = tr[0]
    check("mounts as a whole-stage page: no आगे, the veil over the table lifting from the first frames, nothing else in yet", f0["nav"] == "none" and not f0["band"] and not f0["sheet"]
          and first(tr, lambda f: f["lit"]) is not None and T(first(tr, lambda f: f["lit"])) < 150 and first(tr, lambda f: f["veil"] < 0.05) is not None and T(first(tr, lambda f: f["veil"] < 0.05)) < 1100,
          (f0["nav"], T(first(tr, lambda f: f["lit"])), T(first(tr, lambda f: f["veil"] < 0.05))))
    intro = snd("vo_stamp_intro"); fb = first(tr, lambda f: f["band"])
    voi = lambda f: f["vo"] and f["vo"][0].startswith("vo_stamp_intro")
    f_is = first(tr, lambda f: voi(f) and f["vo"][1] > 0)                      # the first frame in which the line is actually sounding
    f_ie = first(tr, lambda f: voi(f) and f["vo"][2])                           # the first frame after it has ended (currentAudio keeps the ended clip until the next play)
    check("the title's line sounds (~0.4 s in) and the title bar appears the moment it is heard (within 60 ms of the clip's first sounding frame)",
          len(intro) == 1 and P["intro_at"] - 60 < intro[0]["t"] - t0 < P["intro_at"] + 400 and f_is and fb and -20 < fb["t"] - f_is["t"] < 60,
          (round(intro[0]["t"] - t0) if intro else None, T(f_is), T(fb)))
    # 2. the sheet and the tray, after the line
    fs_, ft = first(tr, lambda f: f["sheet"]), first(tr, lambda f: f["tray"])
    check("the sheet settles onto the table 0.5 s after the line ends (on the clip's own clock), the tray slides up 150 ms later", fs_ and ft and f_ie and abs(fs_["t"] - (f_ie["t"] + P["after_intro"] + P["sheet_in"])) < 200 and 80 < ft["t"] - fs_["t"] < 260,
          (T(fs_), T(ft), T(f_ie)))
    # 3. the two stamps pop in, each on its pop
    fp_ = [first(tr, lambda f, k=k: len(f["stamps"]) > k and ("pop" in f["stamps"][k] or "shown" in f["stamps"][k])) for k in (0, 1)]; pops = snd("sfx_stamp_pop")
    check("the two stamps pop into the tray 0.7 s after the sheet, 350 ms apart, each as its pop sounds — the pops at 60 % of the first build's volume (.48)", all(fp_) and len(pops) == 2 and abs(fp_[0]["t"] - fs_["t"] - P["stamps_at"]) < 120
          and abs(fp_[1]["t"] - fp_[0]["t"] - P["pop_gap"]) < 70 and all(abs(pops[k]["t"] - fp_[k]["t"]) < 60 for k in (0, 1)) and all(abs(x["vol"] - 0.48) < 0.01 for x in pops),
          ([T(f) for f in fp_], [round(x["t"] - t0) for x in pops], [round(x["vol"], 2) for x in pops]))
    # 4. the sentence, word by word on the clip's clock
    sent = snd("vo_stamp_sent"); fw = [first(tr, lambda f, n=n: f["words"] >= n) for n in range(1, len(WT) + 1)]
    check("the sentence's clip starts 0.7 s after the second pop", len(sent) == 1 and abs(sent[0]["t"] - fp_[1]["t"] - P["sent_at"]) < 150, round(sent[0]["t"] - fp_[1]["t"]) if sent else None)
    offs = [round(fw[i]["vo"][1] * 1000 - WT[i] * 1000) for i in range(len(WT))] if sent and all(fw) and all(f["vo"] and f["vo"][0].startswith("vo_stamp_sent") for f in fw) else None
    check("each of its 5 words appears as the clip reaches it (the clip's clock at the reveal frame within -60..+40 ms of the word's start)", offs is not None and all(-60 <= o <= 40 for o in offs), offs)
    check("the 5 words are all shown, in order, and none before the clip", all(fw) and all(fw[i]["t"] < fw[i + 1]["t"] for i in range(len(fw) - 1)) and fw[0]["t"] >= sent[0]["t"], [T(f) for f in fw])
    # 5. the slot appears as the clip ends and breathes 3.5 s; the stamps are the child's from that moment
    fsl = first(tr, lambda f: has(f["slot"], "in"))
    f_se = first(tr, lambda f: f["vo"] and f["vo"][0].startswith("vo_stamp_sent") and f["vo"][2]); s_end = f_se["t"] if f_se else None   # the clip's first ended frame
    fbe = first(tr, lambda f: has(f["slot"], "in") and not has(f["slot"], "blink"), since=fsl["t"] + 500) if fsl else None
    ops = [f["slotOp"] for f in tr if fsl and fbe and fsl["t"] + 200 < f["t"] < fbe["t"]]; dim = min(ops, default=1)
    check("the empty slot appears as the clip ends (within 300 ms) and blinks for 3.5 s just as the pages before (the demos' dmfBlink: three slow blinks, its opacity down to .2 and back)",
          fsl and fbe and s_end and abs(fsl["t"] - s_end) < 300 and abs(fbe["t"] - fsl["t"] - P["blink_ms"]) < 150 and bk == "dmfBlink" and 0.15 <= dim <= 0.3,
          (T(fsl), round(fsl["t"] - s_end) if fsl and s_end else None, round(fbe["t"] - fsl["t"]) if fbe else None, bk, round(dim, 2)))
    fli = first(tr, lambda f: f["live"])
    check("the stamps are the child's from the moment the slot appears (.live, the drag handles' cursor), not before", fli and fsl and abs(fli["t"] - fsl["t"]) < 40
          and ta == "none", (T(fli), T(fsl), ta))
    # 6. the guidance: 0.5 s after the blink, the ? stamp glides SLOWLY over the slot, hovers, glides home — no press, no print
    fh1 = first(tr, lambda f: has(f["c1"], "lift"), since=fsl["t"] if fsl else 0)
    hover = (sc[0], sc[1] + P["press_down"] - P["hover_up"])   # the print point hovering hover_up px above the press point
    fat = min((f for f in tr if fh1 and fh1["t"] <= f["t"] <= fh1["t"] + P["glide"] + 300 and f["st1"]), key=lambda f: abs(tipof(f["st1"])[0] - hover[0]) + abs(tipof(f["st1"])[1] - hover[1]), default=None)
    fmid = min((f for f in tr if fh1 and f["st1"]), key=lambda f: abs(f["t"] - (fh1["t"] + P["glide"] * 2 / 3)), default=None)
    dmid = (abs(tipof(fmid["st1"])[0] - hover[0]) + abs(tipof(fmid["st1"])[1] - hover[1])) if fmid else None
    check("the guidance starts 0.5 s after the blink ends: the ? stamp lifts and glides over the slot in 1.5 s (its print point within 4 px of the hover point as the glide ends; still 15+ px away two thirds in — a slow glide)",
          fh1 and fbe and abs(fh1["t"] - fbe["t"] - P["hint_at"]) < 150 and fat and abs(fat["t"] - fh1["t"] - P["glide"]) < 200 and near(tipof(fat["st1"]), hover, 4) and dmid and dmid > 15,
          (round(fh1["t"] - fbe["t"]) if fh1 and fbe else None, round(fat["t"] - fh1["t"]) if fat else None, [round(v, 1) for v in tipof(fat["st1"])] if fat else None, [round(v, 1) for v in hover], round(dmid, 1) if dmid else None))
    fh1e = first(tr, lambda f: not has(f["c1"], "lift"), since=fh1["t"] + 500) if fh1 else None
    home1 = lambda f: f["st1"] and all(abs(f["st1"][i] - S1[i]) < 1.5 for i in range(4))
    fhome1 = first(tr, home1, since=fh1["t"] + 1000) if fh1 else None
    thud = snd("sfx_stamp_press"); fm = first(tr, lambda f: f["mark"]); fgn = first(tr, lambda f: has(f["slot"], "gone"))
    check("it hovers there and glides home (set down ~2.9 s after it lifted, its box within 1.5 px of its place) — nothing printed, no thud, the slot's box still there",
          fh1 and fh1e and abs(fh1e["t"] - fh1["t"] - (P["glide"] + P["hold"] + P["back"] - 150)) < 200 and fhome1 and fhome1["t"] < fh1e["t"] + 250
          and fm and fm["t"] > t_d3 - 50 and fgn and fgn["t"] > t_d3 and not [x for x in thud if x["t"] < t_d3],
          (round(fh1e["t"] - fh1["t"]) if fh1 and fh1e else None, T(fhome1), len([x for x in thud if x["t"] < t_d3])))
    # the guidance again after 7 s without a touch, not before
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
    # no box behind the dropped stamp: its element stays transparent (the engine paints any bare .wrong white — the page's class is stp-wrong)
    # and, on the shot over the bare wood, the top-left corner of its box (no picture there) is the wood's colour, not white
    from PIL import Image
    import numpy as np
    WA = np.asarray(Image.open(wshot).convert("RGB").resize((1280, 720), Image.LANCZOS)).astype(float); wx, wy, ww, wh = [int(round(v)) for v in wbox]
    corner = WA[wy + 2:wy + 14, wx + 2:wx + 14].mean(); beside = WA[wy:wy + wh, max(0, wx - 12 - ww):wx - 12].mean()   # the wood to the LEFT of the box (the sheet begins to its right)
    check("no white box behind a stamp dropped on the bare wood: its element's background stays transparent while it wiggles, and the corner of its box in the shot is the wood's colour (not white)",
          wbg in ("rgba(0, 0, 0, 0)", "transparent") and corner < 200 and abs(corner - beside) < 25, (wbg, round(corner, 1), round(beside, 1)))
    # the wrong stamp on the slot: the same
    fg2 = first(tr, lambda f: has(f["c0"], "drag"), since=fd1["t"] if fd1 else 0); fd2 = first(tr, lambda f: not has(f["c0"], "drag"), since=fg2["t"] + 100) if fg2 else None
    tip2 = tipof(tr[tr.index(fd2) - 1]["st0"]) if fd2 else None
    home0 = lambda f: f["st0"] and all(abs(f["st0"][i] - S0[i]) < 1.5 for i in range(4))
    fback2 = first(tr, lambda f: home0(f) and not has(f["c0"], "lift"), since=fd2["t"]) if fd2 else None
    check("the । stamp dropped ON the slot (its print point on the slot's centre): the incorrect buzz, the wiggle, back to its place — nothing printed, the slot still there",
          fd2 and near(tip2, sc, 6) and len(wrongs) == 2 and abs(wrongs[1]["t"] - fd2["t"]) < 60 and first(tr, lambda f: has(f["c0"], "stp-wrong"), since=fd2["t"] - 20)
          and fback2 and fback2["t"] - fd2["t"] < P["wiggle"] + P["reset"] + 450 and not fback2["mark"] and not has(fback2["slot"], "gone"),
          ([round(v) for v in tip2] if tip2 else None, round(wrongs[1]["t"] - fd2["t"]) if len(wrongs) > 1 and fd2 else None, round(fback2["t"] - fd2["t"]) if fback2 and fd2 else None))
    # a tap on a stamp (no move): nothing — no buzz, it stays
    ftap = first(tr, lambda f: has(f["c1"], "drag"), since=fback2["t"]) if fback2 else None
    fafter = min((f for f in tr if ftap and f["st1"]), key=lambda f: abs(f["t"] - (ftap["t"] + 400)), default=None)
    check("a tap on a stamp (a move under 10 px) is a touch, not a placing: no buzz, the stamp is set back down where it is", ftap and len([x for x in wrongs if x["t"] > ftap["t"]]) == 0 and fafter and home1(fafter) and not has(fafter["c1"], "lift"),
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
    check("the stamp thud sounds as it presses (0.28 s after the drop) and the mark is printed at 0.4 s", len(thud) == 1 and fd3 and abs(thud[0]["t"] - fd3["t"] - P["thud_at"]) < 80 and fm and abs(fm["t"] - fd3["t"] - P["mark_at"]) < 80,
          (round(thud[0]["t"] - fd3["t"]) if thud and fd3 else None, round(fm["t"] - fd3["t"]) if fm and fd3 else None))
    fh3 = first(tr, lambda f: home1(f) and not has(f["c1"], "lift"), since=fm["t"]) if fm else None
    check("the stamp lifts and glides back to its place in the tray (within 1.5 px), set down by 1.8 s after the drop", fh3 is not None and fh3["t"] - fd3["t"] < P["back_at"] + P["back_home"] + 200, round(fh3["t"] - fd3["t"]) if fh3 else None)
    corr = snd("sfx_correct_new")
    check("the slot's box goes 1.6 s after the drop, on the correct chime (the user's standard sfx_correct_feedback, within 60 ms), and the mark stays",
          fgn and fd3 and abs(fgn["t"] - fd3["t"] - P["gone_at"]) < 100 and len(corr) == 1 and abs(corr[0]["t"] - fgn["t"]) < 60 and tr[-1]["mark"] and has(tr[-1]["slot"], "gone"),
          (round(fgn["t"] - fd3["t"]) if fgn and fd3 else None, round(corr[0]["t"] - fgn["t"]) if corr and fgn else None))
    fcf = first(tr, lambda f: f["conf"]); cel = [x for x in snd("sfx_celebrate") if fd3 and x["t"] < fd3["t"] + P["done_at"] - 300]   # the end screen's own celebration comes after
    check("confetti comes 2.1 s after the drop, on its own sound (the user's standard sfx confetti, within 60 ms)", fcf and fd3 and abs(fcf["t"] - fd3["t"] - P["confetti_at"]) < 100 and len(cel) == 1 and abs(cel[0]["t"] - fcf["t"]) < 60,
          (round(fcf["t"] - fd3["t"]) if fcf and fd3 else None, round(cel[0]["t"] - fcf["t"]) if cel and fcf else None))
    c = ink_centre(done, (SL["x"] - 2, SL["y"] - 6, SL["x"] + SL["w"] + 2, SL["y"] + SL["h"] + 6))
    check("the printed ? sits with its ink on the slot's centre (within 3 px), on the sheet after the sentence", c and abs(c[0] - sc[0]) < 3 and abs(c[1] - sc[1]) < 3, (c, sc))
    check("the end screen follows 4.4 s after the drop (the confetti fallen), with no round gate", fd3 and abs(t_cel - fd3["t"] - P["done_at"]) < 200 and not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"), round(t_cel - fd3["t"]) if fd3 else None)
    lifts = [i for i in range(1, len(tr)) if has(tr[i]["c1"], "lift") and not has(tr[i - 1]["c1"], "lift")]
    check("the ? stamp lifted four times in all: the two guidances, then only in the child's hand (the far drop, the right drop) — no guidance while the child was at work", len(lifts) == 4, len(lifts))
    until(t_cel, 800); shot(pg, "l2_end.png"); pl = pg.evaluate(PLAYS); own = [x for x in pl if x["src"].startswith("sfx_stamp")]
    check("leaving the page stopped its own sounds", len(own) == 3 and all(x["paused"] for x in own), [(x["src"], x["paused"]) for x in own])
    # 7. the slot moment against Figma's 565:28 render (the sentence shown, the empty slot, the stamps in the tray)
    if ref and ref.exists():
        from PIL import Image, ImageChops
        import numpy as np
        A = Image.open(z).convert("RGB").resize((1280, 720), Image.LANCZOS); B = Image.open(ref).convert("RGB")
        d = np.asarray(ImageChops.difference(A, B)).astype(float).sum(axis=2)
        Image.fromarray(np.clip(d * 2, 0, 255).astype("uint8")).save(out / "l2_slot_diff.png")
        regions = {"frame": d.mean(), "title bar": d[26:146, 36:1280].mean(), "sheet + sentence + slot": d[150:565, 385:895].mean(), "tray + stamps": d[540:707, 427:853].mean()}
        check("against Figma's 565:28 render: the whole frame close (mean < 12), the sheet with its sentence and slot close (mean < 12: the text's own edges)", regions["frame"] < 12 and regions["sheet + sentence + slot"] < 12,
              {k: round(v, 2) for k, v in regions.items()})
        a = np.asarray(A).astype(int); blk = (a[..., 0] < 90) & (a[..., 1] < 90) & (a[..., 2] < 90); sub = blk[325:395, 300:750]; ys, xs = np.where(sub)
        ext = (int(xs.min()) + 300, int(xs.max()) + 300, int(ys.min()) + 325, int(ys.max()) + 325) if len(xs) else None
        check("the sentence's ink lies where the render's does (its box within 4 px: x 455..745, y 342..372)", ext and abs(ext[0] - 455) <= 4 and abs(ext[1] - 745) <= 4 and abs(ext[2] - 342) <= 4 and abs(ext[3] - 372) <= 4, ext)
    # 8. a re-run, and leaving mid-way (the dev nav) with a stamp in hand: a clean stop
    pg.evaluate("window._plays = []"); pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'L2'))"); pg.wait_for_timeout(2500)
    check("a re-run from the end screen starts the page over (the table, the bar with its line)", pg.evaluate("!!document.querySelector('.stp') && !!document.querySelector('.dmf-band.in')") and len(pg.evaluate(PLAYS)) >= 1)
    pg.wait_for_function("!!document.querySelector('.stp.live')", timeout=20000); xt, yt = fp(*g1); pg.mouse.move(xt, yt); pg.mouse.down(); pg.mouse.move(xt + 60, yt - 80); pg.wait_for_timeout(100)
    held = pg.evaluate("document.querySelector('.stp-stamp.s1').className")
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'P2'))"); pg.wait_for_timeout(500); pg.mouse.up(); pg.wait_for_timeout(300); pl = pg.evaluate(PLAYS)
    check("leaving mid-way (to P2) with a stamp in hand: the page's sounds stop, its hook and timers are cleared, its scene is gone, no error", "drag" in held.split() and all(x["paused"] for x in pl if "stamp" in x["src"])
          and pg.evaluate("window.oceanCleanup == null") and pg.evaluate("!document.querySelector('.stp')"), (held, [(x["src"], x["paused"]) for x in pl if "stamp" in x["src"]]))
    check("no page errors", not errs, errs[:3])
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
