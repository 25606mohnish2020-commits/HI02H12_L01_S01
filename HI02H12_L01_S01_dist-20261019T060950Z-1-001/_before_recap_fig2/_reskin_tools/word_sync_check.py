"""[word-sync] (2026-10-30) every text read with a clip, against the reference T1's behaviour (hi-02-h04-l01-s01-dun, STORY-INTRO-JS):
usage: python -I -X utf8 word_sync_check.py <index.html> [T0 T0B T1 T2 T3 T4 G1 G2 G3 L2r1 .. L2r5]   (default: all of them;
       L2r<i> mounts the stamp page with round i first)
Per page a rAF trace on the page's own clock of every narrated line (.sfig-w words grouped by their text element): words shown,
words lit (.hot), the rise (.sfig-rise: siSentIn), the playing clip and its currentTime. Per line, from its card data (word_times,
word_end, audio): the words appear ALL in one frame with the rise; the clip starts ~0.45 s after it (SENT_IN_MS); while it plays
the lit words are exactly those whose stretch [start, next start) holds currentTime (one frame's lag), none after the last word's
end and none with no clip (the demos' second reading lights words on its own *_full clip); the lit look is #E86A00 + p2WordPop .28 s.
"""
import sys, json, pathlib
from playwright.sync_api import sync_playwright
html = pathlib.Path(sys.argv[1]).resolve(); ids = sys.argv[2:] or ["T0", "T0B", "T1", "T2", "T3", "T4", "G1", "G2", "G3", "L2r1", "L2r2", "L2r3", "L2r4", "L2r5"]
LEAVE = """() => { for (const id of ['startGate','bootLoader']) { const e = document.getElementById(id); if (e) { e.classList.add('hidden'); if (id === 'bootLoader') e.remove(); } } document.body.classList.remove('is-start'); document.body.classList.add('loaded'); }"""
DUR = {"T0": 42000, "T0B": 30000, "T1": 60000, "T2": 16000, "T3": 16000, "T4": 18000, "G1": 22000, "G2": 22000, "G3": 22000, "L2": 26000}
TRACE = r"""(dur) => new Promise(res => {
  const t0 = performance.now(), fr = [];
  const lines = () => { const m = new Map(); document.querySelectorAll('.sfig-w').forEach(w => { const p = w.parentElement.closest('p, .sfig-sent') || w.parentElement; if (!m.has(p)) m.set(p, []); m.get(p).push(w); }); return [...m.entries()]; };
  (function tick(){
    const t = performance.now() - t0;
    const a = (typeof currentAudio !== 'undefined') ? currentAudio : null;
    const f = { t: Math.round(t), clip: a ? decodeURIComponent(String(a.currentSrc || a.src || '').split('/').pop()) : null, ct: a ? +a.currentTime.toFixed(3) : null, paused: a ? a.paused : null, ended: a ? a.ended : null, L: [] };
    lines().forEach(([p, ws], k) => {
      const cs = getComputedStyle(p);
      const shown = ws.filter(w => +getComputedStyle(w).opacity > .5).length;
      const hot = ws.map((w, i) => w.classList.contains('hot') ? i : -1).filter(i => i >= 0);
      const hw = ws.find(w => w.classList.contains('hot')), hcs = hw ? getComputedStyle(hw) : null;
      f.L.push({ key: (p.className || p.tagName) + ':' + ws.map(w => w.textContent).join(' ').slice(0, 24), n: ws.length, shown, hot,
        rise: p.classList.contains('sfig-rise'), anim: cs.animationName, op: +(+cs.opacity).toFixed(3), tr: cs.translate, sc: cs.scale,
        hotLook: hcs ? hcs.color + '|' + hcs.animationName + '|' + hcs.animationDuration : null });
    });
    fr.push(f);
    if (t < dur) requestAnimationFrame(tick); else res(fr);
  })();
})"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    pg = b.new_page(viewport={"width": 1333, "height": 750}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    for sid in ids:
        pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate(LEAVE)
        real = sid
        if sid.startswith("L2r"):   # a later stamp round, mounted as the first
            i = int(sid[3:]) - 1; real = "L2"
            pg.evaluate(f"(() => {{ const d = CARD.slides.find(s => s.id === 'L2').data; d.rounds = [d.rounds[{i}]].concat(d.rounds.filter((_, k) => k !== {i})); }})()")
        data = pg.evaluate(f"CARD.slides.find(s => s.id === '{real}').data")
        if sid.startswith("L2r"): data = dict(data, rounds=data["rounds"][:1])
        pg.evaluate(f"mountSlide(CARD.slides.findIndex(s => s.id === '{real}'))")
        fr = pg.evaluate(TRACE, DUR.get(sid, 26000 if sid.startswith('L2') else 20000))
        res[sid] = {"data": data, "frames": fr}
        print(sid, len(fr), "frames; errors so far:", errs[:2], flush=True)
    b.close()
R = res

# ---- the judge


def lines_of(sid, d):
    """(text, word_times, word_end, clip file) for every narrated line of a page's data."""
    out = []
    def add(x):
        if isinstance(x, dict) and x.get("text_hi") and x.get("word_times") and x.get("audio"):
            out.append((x["text_hi"], x["word_times"], x.get("word_end"), x["audio"]))
    for b in d.get("beats", []) or []: add(b)
    for l in d.get("lines", []) or []: add(l)
    for r in d.get("rows", []) or []:
        for k in ("name", "when", "example"): add(r.get(k))
    add(d.get("sentence"))
    for r in d.get("rounds", []) or []: add(r.get("sentence"))
    return out

bad_total = 0
for sid, v in R.items():
    d, fr = v["data"], v["frames"]
    print(f"== {sid}")
    for text, wt, we, audio in lines_of(sid, d):
        words = text.replace("\n", " ").split()
        key_words = " ".join(words)[:24]
        series = [(f, next((l for l in f["L"] if l["key"].split(":", 1)[1] == key_words), None)) for f in fr]
        series = [(f, l) for f, l in series if l]
        if not series: print(f"   [{key_words}] not on this run's screen"); continue
        n = series[0][1]["n"]
        # 1. appearance: shown counts seen
        counts = sorted({l["shown"] for f, l in series})
        partial = [c for c in counts if 0 < c < n]
        f_show = next((f for f, l in series if l["shown"] == n), None)
        f_rise = next((f for f, l in series if l["rise"]), None)
        rise_frames = [(f["t"], l["op"], l["tr"], l["sc"]) for f, l in series if l["rise"]]
        # 2. the clip's start: first frame with this line's clip at currentTime > 0
        clipname = audio + ".ogg"
        f_play = next((f for f, l in series if f["clip"] == clipname and f["ct"] and f["ct"] > 0 and not f["paused"]), None)
        # 3. highlight: compare lit set with the expected set per frame while the clip plays
        starts = wt; end = we
        def expect(ct):
            if ct is None: return []
            if end is not None and ct >= end: return []
            s = None
            for x in starts:
                if ct >= x: s = x
            return [i for i, x in enumerate(starts) if s is not None and x == s]
        mism = []; looks = set(); lit_after_end = 0
        for f, l in series:
            if f["clip"] == clipname and f["ct"] is not None and not f["ended"] and not (f["paused"] and f["ct"] == 0):
                e = expect(f["ct"])
                if l["hot"] != e: mism.append((f["t"], f["ct"], l["hot"], e))
            if l["hotLook"]: looks.add(l["hotLook"])
            if l["hot"] and not (f["clip"] == clipname and not f["ended"]) and not (f["clip"] or "").endswith("_full.ogg"): lit_after_end += 1   # the demos' second reading lights words on its own clip
        # the lit set may lag the clip's clock by a frame or two (~33 ms): count only mismatches lasting more than two frames
        persist = 0; run_ = 1
        for i, m in enumerate(mism):
            run_ = run_ + 1 if i and mism[i - 1][0] >= m[0] - 40 else 1
            if run_ == 3: persist += 1
        ok = not partial and f_show is not None and f_rise is not None and abs((f_rise["t"]) - (f_show["t"])) <= 34 and persist == 0 and lit_after_end <= 2
        delay = (f_play["t"] - f_rise["t"]) if (f_play and f_rise) else None
        bad_total += 0 if ok else 1
        print(f"   [{key_words}] {'OK ' if ok else 'BAD'} words {n}: shown counts {counts}{' PARTIAL ' + str(partial) if partial else ''}; all shown at {f_show and f_show['t']} ms, rise at {f_rise and f_rise['t']} ms"
              f" ({len(rise_frames)} rise frames, first {rise_frames[0][1:] if rise_frames else None}); clip starts {delay} ms after the rise;"
              f" highlight mismatches {len(mism)} (persisting {persist}); lit with no clip {lit_after_end}; looks {sorted(looks)}")
print("lines not OK:", bad_total)
sys.exit(1 if bad_total else 0)
