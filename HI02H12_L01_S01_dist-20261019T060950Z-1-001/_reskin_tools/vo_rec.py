"""The recorded voice-overs (2026-10-28, the user's `voiceovers/` folder, copied to vo_rec/) into the build. [vo-rec]

usage: python -I -X utf8 vo_rec.py [<dist folder>] [--retranscribe] [--gain <dB>]
  1. transcribes every wav with faster-whisper (small, Hindi, word timestamps; vo_rec/transcripts.json is the cache — delete it
     or pass --retranscribe to hear them again);
  2. re-containers every recording whose words are the page's into assets/Audio/<Audio ID>.ogg (Opus 48 kHz, like every clip
     here) — vo_stamp_sent4 is cut in two at the word boundary before "उनके" (the deck keeps the letter's last block as one line,
     the page plays it as rounds 4 and 5: vo_stamp_sent4 + vo_stamp_sent5);
  3. re-derives the word timings of every synced line (the *_assets/*.words.json files build.py reads) from the clip's own
     words: each shown word lined up with the heard word it is (a fuzzy, order-keeping match — whisper's spelling wobbles), the
     shown words it cannot hear (a bare mark, a word the clip says differently) spread over the gap between their neighbours;
  4. writes vo_rec/derived.json for build.py: the IDs applied (with the manifest's line as their text), the ones left out and
     why, the gate caption cue (the start of "चलिए" in vo_pt_tutorial), the split point.
Recordings whose words contradict the page are NOT applied (listed in derived.json "skipped"): the story recordings tell a
different story (1-4.wav, vo_story_s1, vo_story_r1), G1's sentence and hint 3 say "राजू" where the frame says "पिंकी"."""
import sys, json, pathlib, subprocess, re, unicodedata, difflib, shutil
import numpy as np, openpyxl

SCR = pathlib.Path(__file__).resolve().parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
DIST = pathlib.Path(args[0]).resolve() if args else SCR.parent / "HI02H12_L01_S01_dist"
REC = SCR / "vo_rec"; AUD = DIST / "assets" / "Audio"
GAIN = float(sys.argv[sys.argv.index("--gain") + 1]) if "--gain" in sys.argv else 0.0

# ---- 1. what was said ----
wb = openpyxl.load_workbook(DIST / "HI02H12_L01_S01_VO_Manifest.xlsx", data_only=True)
MAN = {str(r[0]): str(r[1]).strip() for r in wb.worksheets[0].iter_rows(values_only=True) if r[0] and str(r[0]).startswith("vo_")}
tcache = REC / "transcripts.json"
if tcache.exists() and "--retranscribe" not in sys.argv:
    T = json.loads(tcache.read_text(encoding="utf-8"))
else:
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8"); T = {}
    for f in sorted(REC.glob("*.wav")):
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
        samples = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
        segs, _ = model.transcribe(samples, language="hi", word_timestamps=True, initial_prompt=MAN.get(f.stem), beam_size=5)
        words = [[w.word.strip(), round(w.start, 3), round(w.end, 3)] for s in segs for w in s.words]
        T[f.name] = {"dur": round(len(samples) / 16000, 3), "text": " ".join(w[0] for w in words), "words": words, "manifest": MAN.get(f.stem)}
        print(f"heard {f.name:28s} {T[f.name]['text'][:80]}")
    tcache.write_text(json.dumps(T, ensure_ascii=False, indent=1), encoding="utf-8")

# ---- what is applied where ----
# the page's words as the recording says them, where the recording differs from the manifest (whisper heard "पिंकी" on the
# demo and the recap example — the artist worked from the renamed frames — and the recap's "when" line is the deck's fuller
# sentence while the frame shows its short form)
SPOKEN = {
  "vo_demo1_sent": "पिंकी स्कूल जा रही है", "vo_demo1_full": "पिंकी स्कूल जा रही है, पूर्णविराम।",
  "vo_recap_purn_eg": "उदाहरण- पिंकी स्कूल गई ।",
}
SHOWN_OVERRIDE = { "vo_recap_purn_eg": "पिंकी स्कूल गई ।" }   # the row's example reads as the voice says it
SKIP = {
  "1.wav": "a different story (heard: पिंकी बोली माँ बिल्ली रसोई में जा रही है) — no page carries it",
  "2.wav": "a different story (heard: पिंकी ने पूछा, क्या उसे जाने दूँ?) — no page carries it",
  "3.wav": "a different story (heard: माँ ने कहा, उसे रोको मत जाने दो) — no page carries it",
  "4.wav": "a different story's moral (heard: दोनों वाक्यों में शब्द एक जैसे हैं परन्तु विराम चिह्न अलग जगह ...) — no page carries it",
  "vo_story_s1.wav": "not the story page's run-on (heard: माँ ने कहा उसे रोको मत जाने दो, 3.9 s) — the TTS line stays",
  "vo_story_r1.wav": "not the re-read (heard: यहाँ पहले वाक्य का अर्थ है ... दूसरे वाक्य का अर्थ है ...) — the TTS line stays",
  "vo_g1_sent.wav": "says राजू गेंद से खेल रहा था; the frame (656:66) shows पिंकी गेंद से खेल रही थी — the TTS line stays",
  "vo_g1_hint3.wav": "says राजू ... (the sentence as recorded) — not played on G1 (hint 2's line is said again there)",
}
# the synced lines: Audio ID -> its words.json (the SHOWN words are what the page lights)
SYNC = {
  **{f"vo_recap_{k}": SCR / "recap_assets" / f"vo_recap_{k}.words.json" for k in ("purn_name", "purn_when", "purn_eg", "alp_name", "alp_when", "alp_eg", "prashn_name", "prashn_when", "prashn_eg")},
  "vo_demo1_sent": SCR / "demo1_assets" / "vo_demo1_sent.words.json", "vo_demo1_full": SCR / "demo1_assets" / "vo_demo1_full.words.json",
  "vo_demo2_sent": SCR / "demo2_assets" / "vo_demo2_sent.words.json", "vo_demo2_full": SCR / "demo2_assets" / "vo_demo2_full.words.json",
  "vo_demo3_sent": SCR / "demo3_assets" / "vo_demo3_sent.words.json", "vo_demo3_full": SCR / "demo3_assets" / "vo_demo3_full.words.json",
  "vo_g2_sent": SCR / "g2_assets" / "vo_g2_sent.words.json", "vo_g3_sent": SCR / "g3_assets" / "vo_g3_sent.words.json",
  **{f"vo_g4_{k}": SCR / "g4_assets" / f"vo_g4_{k}.words.json" for k in ("o1", "o2", "o3")},
  **{f"vo_p1_{k}": SCR / "p1_assets" / f"vo_p1_{k}.words.json" for k in ("o1", "o2", "o3")},
  **{f"vo_p2_{k}": SCR / "p2_assets" / f"vo_p2_{k}.words.json" for k in ("o1", "o2", "o3")},
  **{f"vo_stamp_{k}": SCR / "stamp_assets" / f"vo_stamp_{k}.words.json" for k in ("sent", "sent2", "sent3", "sent4", "sent5")},
}

def norm(s):   # letters and vowel signs only, the nukta dropped (whisper writes ज़/ज, ढ़/ढ either way), marks as the words the voice says for them
    s = {"।": "पूर्णविराम", "?": "प्रश्नवाचक", ",": "अल्पविराम"}.get(s.strip(), s)
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if (unicodedata.category(ch)[0] in "LM") and ch != "़")

def sim(a, b): return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() if a and b else 0.0

def align(shown, heard):
    """shown: the page's words; heard: [(word, start, end)]. Returns each shown word's [start, end]. Order-keeping fuzzy
    DP match (a pair counts from similarity .55); the unmatched shown words take the heard words left between their matched
    neighbours (right-aligned at the front, left-aligned at the back), else an even spread of the gap in time."""
    A = [norm(w) for w in shown]; B = [norm(h[0]) for h in heard]
    n, m = len(A), len(B); S = [[sim(a, b) for b in B] for a in A]
    best = [[0.0] * (m + 1) for _ in range(n + 1)]; back = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            c = [(best[i - 1][j], "u"), (best[i][j - 1], "l")]
            if S[i - 1][j - 1] >= 0.55: c.append((best[i - 1][j - 1] + S[i - 1][j - 1], "d"))
            best[i][j], back[i][j] = max(c)
    match = {}; i, j = n, m
    while i > 0 and j > 0:
        d = back[i][j]
        if d == "d": match[i - 1] = j - 1; i -= 1; j -= 1
        elif d == "u": i -= 1
        else: j -= 1
    starts = [None] * n
    for i_, j_ in match.items(): starts[i_] = heard[j_][1]
    # the gaps
    ms = sorted(match.items()); k = 0
    gaps = []
    prev_i, prev_j = -1, -1
    for i_, j_ in ms + [(n, m)]:
        if i_ - prev_i > 1: gaps.append((prev_i + 1, i_ - 1, prev_j + 1, j_ - 1))   # shown i0..i1 unmatched, heard j0..j1 free
        prev_i, prev_j = i_, j_
    end_t = heard[-1][2] if heard else 0
    for i0, i1, j0, j1 in gaps:
        ns, nh = i1 - i0 + 1, max(0, j1 - j0 + 1)
        if nh >= 1:
            # the free heard words, right-aligned when the gap is at the front (extras like "उदाहरण" come first), else left-aligned
            idx = list(range(j0, j1 + 1))
            take = idx[-ns:] if i0 == 0 else idx[:ns]
            for q in range(ns):
                h = take[min(q, len(take) - 1)] if q < len(take) else take[-1]
                starts[i0 + q] = heard[h][1] if q < len(take) else None
        t0 = heard[j0 - 1][2] if j0 - 1 >= 0 and j0 - 1 < len(heard) else 0.0
        t1 = heard[j1 + 1][1] if j1 + 1 < len(heard) else end_t
        for q in range(ns):
            if starts[i0 + q] is None: starts[i0 + q] = t0 + (t1 - t0) * (q + (0 if i0 + q == 0 else 0.5)) / max(1, ns)
    for q in range(n):   # never backwards
        if q and starts[q] < starts[q - 1]: starts[q] = starts[q - 1]
    ends = starts[1:] + [end_t]
    return [[round(a, 3), round(b, 3)] for a, b in zip(starts, ends)]

def encode(src_wav, dst_ogg, ss=None, to=None):
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if ss is not None: cmd += ["-ss", f"{ss:.3f}"]
    if to is not None: cmd += ["-to", f"{to:.3f}"]
    cmd += ["-i", str(src_wav)]
    if GAIN: cmd += ["-af", f"volume={GAIN}dB"]
    cmd += ["-c:a", "libopus", "-b:a", "96k", "-ar", "48000", str(dst_ogg)]
    subprocess.run(cmd, check=True)

applied, texts, skipped = {}, {}, {}
AUD.mkdir(parents=True, exist_ok=True)
# ---- 2+3. every named recording ----
for f in sorted(REC.glob("*.wav")):
    if f.name in SKIP: skipped[f.name] = SKIP[f.name]; continue
    vid = f.stem; heard = [tuple(w) for w in T[f.name]["words"]]
    if vid == "vo_stamp_sent4":   # the split: rounds 4 (two questions) and 5 (the rest of the letter)
        k = next(i for i, h in enumerate(heard) if norm(h[0]).startswith("उनक"))
        mid = round((heard[k - 1][2] + heard[k][1]) / 2, 3)
        encode(f, AUD / "vo_stamp_sent4.ogg", to=mid); encode(f, AUD / "vo_stamp_sent5.ogg", ss=mid)
        parts = {"vo_stamp_sent4": [h for h in heard[:k]], "vo_stamp_sent5": [(h[0], round(h[1] - mid, 3), round(h[2] - mid, 3)) for h in heard[k:]]}
        split_at = mid
    else:
        encode(f, AUD / f"{vid}.ogg"); parts = {vid: heard}
    for pid, hw in parts.items():
        texts[pid] = SPOKEN.get(pid, MAN.get(vid, T[f.name]["text"]))
        applied[pid] = {"file": f.name, "dur": round((hw[-1][2] if hw else T[f.name]["dur"]), 3), "heard": " ".join(h[0] for h in hw)}
        if pid in SYNC:
            tf = SYNC[pid]; data = json.loads(tf.read_text(encoding="utf-8"))
            shown = (SHOWN_OVERRIDE.get(pid) or data.get("shown") or data["text"]).split()
            data["text"] = texts[pid]
            if pid in SHOWN_OVERRIDE or "shown" in data: data["shown"] = SHOWN_OVERRIDE.get(pid, data.get("shown"))
            wt = align(shown, hw)
            if wt and len(wt) != len(shown): raise SystemExit(f"{pid}: {len(wt)} times for {len(shown)} shown words")
            data["word_times"] = wt; data["source"] = f"recording {f.name} (2026-10-28), faster-whisper word times, vo_rec.py"
            tf.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            applied[pid]["sync"] = {"file": str(tf.relative_to(SCR)), "n": len(wt), "starts": [t[0] for t in wt]}
            print(f"sync  {pid:22s} {' '.join(f'{w}@{t[0]:.2f}' for w, t in zip(shown, wt))}")
# ---- 4. the gate cue: the moment vo_pt_tutorial says its last phrase ("चलिए शुरू करें") ----
pt = [tuple(w) for w in T["vo_pt_tutorial.wav"]["words"]]
cue = next(h for h in pt if norm(h[0]).startswith("चल"))
derived = {"applied": applied, "texts": texts, "skipped": skipped, "gate_cue_ms": {"tutorial": int(round(cue[1] * 1000))},
           "stamp_sent4_split_s": split_at, "gain_db": GAIN, "note": "written by vo_rec.py; build.py reads texts, gate_cue_ms"}
(REC / "derived.json").write_text(json.dumps(derived, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"applied {len(applied)} clips, skipped {len(skipped)}; gate cue {derived['gate_cue_ms']} ms; sent4 split at {split_at} s")
