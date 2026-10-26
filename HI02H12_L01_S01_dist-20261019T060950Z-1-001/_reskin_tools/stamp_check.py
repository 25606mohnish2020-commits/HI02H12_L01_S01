"""The stamp page L2 ([stamp-fig], frame 565:28): mounted straight (as the dev nav would), the whole page plays by itself. The page's
own frame trace (rAF: classes, the slot's opacity, the stamp's box, every frame) and a hook on every media play record the beats;
they are checked against each other and against the clips' word times, so Playwright's own lag never fails a good build. Shots:
l2_table.png (the sheet and the tray), l2_stamps.png, l2_sentence.png, l2_slot.png (the blink paused for the shot — compared
with Figma's render), l2_press.png (informative), l2_done.png (the mark left on the sheet), l2_end.png.
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
PLAYS = "() => window._plays.map(p => ({ src: p.src, t: p.t, paused: p.el.paused, cur: p.el.currentTime, dur: p.el.duration }))"
TRACE = """() => { window.__tr = []; const st = document.getElementById('stage');
  const q = (sel) => { const e = document.querySelector(sel); if(!e) return null; const b = st.getBoundingClientRect(), k = b.width / 1280, r = e.getBoundingClientRect(); return [(r.left - b.left) / k, (r.top - b.top) / k, r.width / k, r.height / k]; };
  (function loop(){ const r = document.querySelector('.stp'); if(!r) return; const slot = document.querySelector('.stp-slot');
    window.__tr.push({ t: performance.now(), lit: r.classList.contains('lit'), band: !!document.querySelector('.dmf-band.in'), sheet: !!document.querySelector('.stp-sheet.in'),
      tray: !!document.querySelector('.stp-tray.in'), stamps: [...document.querySelectorAll('.stp-stamp img')].map(i => i.className), words: document.querySelectorAll('.stp-sent .sfig-w.on').length,
      slot: slot.className, slotOp: +getComputedStyle(slot).opacity, mark: !!document.querySelector('.stp-mark.in'), st1: q('.stp-stamp.s1'), lift: !!document.querySelector('.stp-stamp.lift'),
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

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio", "--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.add_init_script(HOOK)
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE)
    def until(base, ms): pg.wait_for_function(f"performance.now() - {base} >= {ms}", timeout=ms + 8000, polling=20)
    ids = pg.evaluate("CARD.slides.map(s => s.id)")
    check("the pages: ... P2, L1 (the letter page), L2 (the stamp page), then the end screen (15)", ids == ["T0", "T0B", "T1", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "L1", "L2", "CEL"], ids)
    D = pg.evaluate("CARD.slides.find(s => s.id === 'L2').data"); P = D["pace"]; LY = D["layout"]; WT = D["sentence"]["word_times"]
    t0 = pg.evaluate("(() => { const t = performance.now(); mountSlide(CARD.slides.findIndex(s => s.id === 'L2')); return t; })()")
    pg.evaluate(TRACE)
    # live shots at the beats (informative; the checks read the page's own trace)
    pg.wait_for_function("!!document.querySelector('.stp-tray.in')", timeout=15000); until(pg.evaluate("performance.now()"), 550); shot(pg, "l2_table.png")
    pg.wait_for_function("document.querySelectorAll('.stp-stamp img.shown').length === 2", timeout=8000); until(pg.evaluate("performance.now()"), 200); shot(pg, "l2_stamps.png")
    pg.wait_for_function("!!document.querySelector('.stp-slot.in')", timeout=12000)
    pg.evaluate("document.querySelector('.stp-slot').style.animationPlayState = 'paused'"); until(pg.evaluate("performance.now()"), 350)
    z = shot(pg, "l2_slot.png"); pg.evaluate("document.querySelector('.stp-slot').style.animationPlayState = ''")
    pg.wait_for_function("!!document.querySelector('.stp-stamp.lift')", timeout=8000); t_g = pg.evaluate("performance.now()"); until(t_g, P["press_at"] + P["press"] - 60); shot(pg, "l2_press.png")
    pg.wait_for_function("!!document.querySelector('.stp-slot.gone')", timeout=8000); until(pg.evaluate("performance.now()"), 600); done = shot(pg, "l2_done.png")
    pg.wait_for_function("CARD.slides[state.idx].id === 'CEL' && document.body.classList.contains('is-end')", timeout=8000); t_cel = pg.evaluate("performance.now()")
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
    fp = [first(tr, lambda f, k=k: len(f["stamps"]) > k and ("pop" in f["stamps"][k] or "shown" in f["stamps"][k])) for k in (0, 1)]; pops = snd("sfx_stamp_pop")
    check("the two stamps pop into the tray 0.7 s after the sheet, 350 ms apart, each as its pop sounds", all(fp) and len(pops) == 2 and abs(fp[0]["t"] - fs_["t"] - P["stamps_at"]) < 120
          and abs(fp[1]["t"] - fp[0]["t"] - P["pop_gap"]) < 70 and all(abs(pops[k]["t"] - fp[k]["t"]) < 60 for k in (0, 1)), ([T(f) for f in fp], [round(x["t"] - t0) for x in pops]))
    # 4. the sentence, word by word on the clip's clock
    sent = snd("vo_stamp_sent"); fw = [first(tr, lambda f, n=n: f["words"] >= n) for n in range(1, len(WT) + 1)]
    check("the sentence's clip starts 0.7 s after the second pop", len(sent) == 1 and abs(sent[0]["t"] - fp[1]["t"] - P["sent_at"]) < 150, round(sent[0]["t"] - fp[1]["t"]) if sent else None)
    # each word's reveal frame against the clip's OWN clock at that frame (the page reveals word n when currentTime + 40 ms reaches its start)
    offs = [round(fw[i]["vo"][1] * 1000 - WT[i] * 1000) for i in range(len(WT))] if sent and all(fw) and all(f["vo"] and f["vo"][0].startswith("vo_stamp_sent") for f in fw) else None
    check("each of its 5 words appears as the clip reaches it (the clip's clock at the reveal frame within -60..+40 ms of the word's start)", offs is not None and all(-60 <= o <= 40 for o in offs), offs)
    check("the 5 words are all shown, in order, and none before the clip", all(fw) and all(fw[i]["t"] < fw[i + 1]["t"] for i in range(len(fw) - 1)) and fw[0]["t"] >= sent[0]["t"], [T(f) for f in fw])
    # 5. the slot appears as the clip ends and blinks 3.5 s
    fsl = first(tr, lambda f: "in" in f["slot"].split())
    f_se = first(tr, lambda f: f["vo"] and f["vo"][0].startswith("vo_stamp_sent") and f["vo"][2]); s_end = f_se["t"] if f_se else None   # the clip's first ended frame
    fbe = first(tr, lambda f: "in" in f["slot"].split() and "blink" not in f["slot"].split(), since=fsl["t"] + 500) if fsl else None
    dim = min((f["slotOp"] for f in tr if fsl and fbe and fsl["t"] < f["t"] < fbe["t"]), default=1)
    check("the empty slot appears as the clip ends (within 300 ms) and blinks for 3.5 s (its opacity dips below .5)", fsl and fbe and s_end and abs(fsl["t"] - s_end) < 300 and abs(fbe["t"] - fsl["t"] - P["blink_ms"]) < 150 and dim < 0.5,
          (T(fsl), round(fsl["t"] - s_end) if fsl and s_end else None, round(fbe["t"] - fsl["t"]) if fbe else None, round(dim, 2)))
    # 6. the stamp: the glide, the press on the thud, the mark, home again; the box goes, the mark stays
    fl = first(tr, lambda f: f["lift"]); home = LY["stamps"][1]   # the stamp's box on the frame (the first frames' rects are the card's entrance)
    want = (LY["slot"]["x"] + LY["slot"]["w"] / 2 + (LY["stamps"][1][0] + LY["stamps"][1][2] / 2 - (LY["stamps"][1][0] + LY["tips"][1][0])),
            LY["slot"]["y"] + LY["slot"]["h"] / 2 + P["press_down"] + (LY["stamps"][1][3] - LY["tips"][1][1]))
    tipof = lambda f: (f["st1"][0] + f["st1"][2] / 2, f["st1"][1] + f["st1"][3])
    win = [f for f in tr if fl and fl["t"] <= f["t"] <= fl["t"] + P["press_at"] + P["press"] + 400 and f["st1"]]
    fpress = min(win, key=lambda f: abs(tipof(f)[0] - want[0]) + abs(tipof(f)[1] - want[1])) if win else None   # the frame nearest the wanted point = the press
    tip = tipof(fpress) if fpress else None
    check("the ? stamp lifts as the blink ends and glides over the slot; pressed, its print point stands 20 px under the slot's centre (within 4 px)",
          fl and fbe and abs(fl["t"] - fbe["t"]) < 120 and fpress and abs(fpress["t"] - fl["t"] - (P["press_at"] + P["press"])) < 150 and abs(tip[0] - want[0]) < 4 and abs(tip[1] - want[1]) < 4,
          (T(fl), round(fpress["t"] - fl["t"]) if fpress else None, [round(v, 1) for v in tip] if tip else None, [round(v, 1) for v in want]))
    thud = snd("sfx_stamp_press"); fm = first(tr, lambda f: f["mark"])
    check("the stamp thud sounds as it presses (1.01 s into the glide) and the mark is printed 40 ms later", len(thud) == 1 and fl and abs(thud[0]["t"] - fl["t"] - P["thud_at"]) < 80 and fm and abs(fm["t"] - fl["t"] - P["mark_at"]) < 80,
          (round(thud[0]["t"] - fl["t"]) if thud and fl else None, round(fm["t"] - fl["t"]) if fm and fl else None))
    fh = first(tr, lambda f: f["st1"] and all(abs(f["st1"][i] - home[i]) < 1.5 for i in range(4)) and not f["lift"], since=fm["t"]) if fm else None
    if fh is None and fm: print("INFO the stamp's box at the end:", [round(v, 1) for v in tr[-1]["st1"]], "home:", home)
    check("the stamp lifts and glides back to its place in the tray (within 1.5 px), set down by 2.4 s into the move", fh is not None and fh["t"] - fl["t"] < P["back_at"] + P["back"] + 200, round(fh["t"] - fl["t"]) if fh else None)
    fg = first(tr, lambda f: "gone" in f["slot"].split())
    check("the slot's box goes 2.3 s into the move and the mark stays", fg and abs(fg["t"] - fl["t"] - P["gone_at"]) < 100 and tr[-1]["mark"] and "gone" in tr[-1]["slot"].split(), (round(fg["t"] - fl["t"]) if fg else None, tr[-1]["mark"]))
    c = ink_centre(done, (LY["slot"]["x"] - 2, LY["slot"]["y"] - 6, LY["slot"]["x"] + LY["slot"]["w"] + 2, LY["slot"]["y"] + LY["slot"]["h"] + 6))
    sc = (LY["slot"]["x"] + LY["slot"]["w"] / 2, LY["slot"]["y"] + LY["slot"]["h"] / 2)
    check("the printed ? sits with its ink on the slot's centre (within 3 px), on the sheet after the sentence", c and abs(c[0] - sc[0]) < 3 and abs(c[1] - sc[1]) < 3, (c, sc))
    check("the end screen follows 3.3 s into the move, with no round gate", fl and abs(t_cel - fl["t"] - P["done_at"]) < 200 and not pg.evaluate("document.getElementById('phaseGate').classList.contains('show')"), round(t_cel - fl["t"]) if fl else None)
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
        # the sentence's ink against the render's: its extent (x 455..745, y 342..372 on the render)
        a = np.asarray(A).astype(int); blk = (a[..., 0] < 90) & (a[..., 1] < 90) & (a[..., 2] < 90); sub = blk[325:395, 300:750]; ys, xs = np.where(sub)
        ext = (int(xs.min()) + 300, int(xs.max()) + 300, int(ys.min()) + 325, int(ys.max()) + 325) if len(xs) else None
        check("the sentence's ink lies where the render's does (its box within 4 px: x 455..745, y 342..372)", ext and abs(ext[0] - 455) <= 4 and abs(ext[1] - 745) <= 4 and abs(ext[2] - 342) <= 4 and abs(ext[3] - 372) <= 4, ext)
    # 8. leaving mid-way (the dev nav): a clean stop
    pg.evaluate("window._plays = []"); pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'L2'))"); pg.wait_for_timeout(2500)
    check("a re-run from the end screen starts the page over (the table, the bar with its line)", pg.evaluate("!!document.querySelector('.stp') && !!document.querySelector('.dmf-band.in')") and len(pg.evaluate(PLAYS)) >= 1)
    pg.evaluate("mountSlide(CARD.slides.findIndex(s => s.id === 'P2'))"); pg.wait_for_timeout(500); pl = pg.evaluate(PLAYS)
    check("leaving mid-way (to P2): the page's sounds stop, its hook is cleared, its scene is gone", all(x["paused"] for x in pl if "stamp" in x["src"]) and pg.evaluate("window.oceanCleanup == null") and pg.evaluate("!document.querySelector('.stp')"),
          [(x["src"], x["paused"]) for x in pl if "stamp" in x["src"]])
    check("no page errors", not errs, errs[:3])
    b.close()
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
