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
different story (1-4.wav, vo_story_s1, vo_story_r1), G1's sentence and hint 3 say "राजू" where the frame says "पिंकी".

[vo-rec2] (2026-11-05) the user's SECOND batch: the 74 lines of the regenerated VO manifest (every clip the build plays), each named
by its Audio ID, copied over the first batch's files in vo_rec/ (the first batch is kept in ../_before_vo_rec2/vo_rec/). The story's
beats, the two contrast sentences, the moral and the letter's last block now come as their OWN files (vo_story_b1..b4, c1, c2,
moral, vo_stamp_sent5), so 1-4.wav / vo_story_s1.wav are out of vo_rec/ and RENAME / TRIM / the sent4 split are idle (kept for a
combined take). G1's sentence and the recap examples are the pages' words now (no SKIP). New: T2's explanation and G1's sentence are
synced lines; the gate lines (vo_pt_*) and the celebration's vo_well_done are recordings too — derived.json carries their caption
cues (the speech onset of the headline's words) and the celebration's beak bits (the [dun-chrome] detector: RMS per 25 ms, open
above half the local max over +-12 frames and within 18 dB of the peak — it reproduces dun_assets/cel_bits.json bit for bit); and
the cues the pages time on their clips: L1's "दादाजी" + its speech end, L2's "ठप्पा" + the instruction's length. Two sync fixes in the
alignment: every said word starts where its sound does (whisper puts starts inside the pause before a word — the first word at 0.00
over the takes' ~0.27 s of room tone; 305 of 923 starts moved, up to 0.65 s), and said words left on one start (a joined word) share
the span to the next word by their letters. vo_g1_intro.wav of the second batch
is a different line ("वाह! क्या बात है!"): not copied, the first batch's take stays (KEPT_FIRST)."""
import sys, json, pathlib, subprocess, re, unicodedata, difflib, shutil, datetime
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
  "vo_recap_purn_eg": "उदाहरण- मुझे आम खाना पसंद है।",   # [vo-rec2] the [recap-eg] sentence, as the second batch says it (was "उदाहरण- पिंकी स्कूल गई ।")
  "vo_story_b1": "पिंकी बोली, “माँ बिल्ली रसोई में जा रही है।”", "vo_story_b2": "माँ ने कहा, “उसे रोको मत जाने दो।”",   # [story-pinki] the frames' texts
  "vo_story_b3": "पिंकी ने पूछा, “क्या, उसे जाने दूँ ?”", "vo_story_b4": "माँ ने कहा, “उसे रोको, मत जाने दो।”",
  "vo_story_c1": "उसे रोको, मत जाने दो।", "vo_story_c2": "उसे रोको मत, जाने दो।",   # [relisten-pinki] frame 654:567's lines
  "vo_story_moral": "दोनों वाक्यों में शब्द एक जैसे हैं परन्तु विराम चिह्न अलग जगह लगा होने से वाक्य का पूरा अर्थ ही बदल गया।",
  "vo_story_r1": "यहाँ पहले वाक्य का अर्थ है, बिल्ली को रोको, उसे अंदर मत जाने दो। जबकि दूसरे वाक्य का अर्थ है, बिल्ली को मत भगाओ, उसे अंदर जाने दो।",
}
SHOWN_OVERRIDE = {}   # [vo-rec2] (was {"vo_recap_purn_eg": "पिंकी स्कूल गई ।"}: the first batch's example) — the words.json "shown" is the page's
# [story-pinki] the four story recordings are the new story page's beats (frames 652:3, 652:192, 660:127, 653:381): the two
# "माँ ने कहा" takes are told apart by their pause — vo_story_s1.wav pauses after "मत" (frame 652:192, no comma),
# 3.wav after "रोको" (frame 653:381, "उसे रोको, मत जाने दो")
RENAME = { "1.wav": "vo_story_b1", "vo_story_s1.wav": "vo_story_b2", "2.wav": "vo_story_b3", "3.wav": "vo_story_b4",
           "4.wav": "vo_story_moral" }   # [relisten-pinki] the moral ("दोनों वाक्यों में शब्द एक जैसे हैं ...") on T0B
# [relisten-pinki] T0B's two contrast sentences are the two "माँ ने कहा ..." takes without their "माँ ने कहा,": a second clip cut
# from each wav in the pause before "उसे" (measured on the waveforms: 3.wav quiet 1.14-1.52 s, vo_story_s1.wav 1.16-1.58 s)
TRIM = { "3.wav": ("vo_story_c1", 1.40), "vo_story_s1.wav": ("vo_story_c2", 1.45) }   # wav -> (the cut clip's ID, its start in the wav)
# [vo-rec2] RENAME / TRIM are idle since 2026-11-05: the second batch has vo_story_b1..b4 / c1 / c2 / moral as files of their own and
# the first batch's 1-4.wav / vo_story_s1.wav are no longer in vo_rec/ (kept in ../_before_vo_rec2/vo_rec/)
SKIP = {
  "vo_g1_hint3.wav": "says राजू ... (the sentence as recorded) — not played on G1 (hint 2's line is said again there)",
  # [vo-rec2] (2026-11-05) the second batch says G1's sentence with पिंकी (vo_g1_sent.wav) and the [recap-eg] examples
  # (vo_recap_purn_eg.wav / vo_recap_alp_eg.wav), so they are applied — the recap_vo.py placeholder takes are gone
}
# [vo-rec2] files of the second batch NOT copied into vo_rec/ — the first batch's take of the line stays there (and is applied as before)
KEPT_FIRST = {
  "vo_g1_intro.wav": "the second batch's file says \"वाह! क्या बात है!\" (2.56 s; heard with and without the script as whisper's prompt), not "
                     "\"यह वाक्य सुनकर देखिए और वाक्य में सही जगह पर विराम चिह्न लगाइए ।\" — mislabeled; the first batch's take (5.76 s) stays: re-record it",
}
for _f in KEPT_FIRST: assert datetime.date.fromtimestamp((REC / _f).stat().st_mtime) < datetime.date(2026, 11, 5), f"{_f}: the second batch's file is in vo_rec/"
# the synced lines: Audio ID -> its words.json (the SHOWN words are what the page lights)
SYNC = {
  **{f"vo_recap_{k}": SCR / "recap_assets" / f"vo_recap_{k}.words.json" for k in ("purn_name", "purn_when", "purn_eg", "alp_name", "alp_when", "alp_eg", "prashn_name", "prashn_when", "prashn_eg")},
  "vo_demo1_sent": SCR / "demo1_assets" / "vo_demo1_sent.words.json", "vo_demo1_full": SCR / "demo1_assets" / "vo_demo1_full.words.json",
  "vo_demo1_explain": SCR / "demo1_assets" / "vo_demo1_explain.words.json",   # [vo-rec2] T2's explanation (its "पूर्णविराम" lights the danda's tile)
  "vo_g1_sent": SCR / "g1_assets" / "vo_g1_sent.words.json",                  # [vo-rec2] G1's sentence (recorded with पिंकी now)
  "vo_demo2_sent": SCR / "demo2_assets" / "vo_demo2_sent.words.json", "vo_demo2_full": SCR / "demo2_assets" / "vo_demo2_full.words.json",
  "vo_demo3_sent": SCR / "demo3_assets" / "vo_demo3_sent.words.json", "vo_demo3_full": SCR / "demo3_assets" / "vo_demo3_full.words.json",
  "vo_g2_sent": SCR / "g2_assets" / "vo_g2_sent.words.json", "vo_g3_sent": SCR / "g3_assets" / "vo_g3_sent.words.json",
  **{f"vo_g4_{k}": SCR / "g4_assets" / f"vo_g4_{k}.words.json" for k in ("o1", "o2", "o3")},
  **{f"vo_p1_{k}": SCR / "p1_assets" / f"vo_p1_{k}.words.json" for k in ("o1", "o2", "o3")},
  **{f"vo_p2_{k}": SCR / "p2_assets" / f"vo_p2_{k}.words.json" for k in ("o1", "o2", "o3")},
  **{f"vo_stamp_{k}": SCR / "stamp_assets" / f"vo_stamp_{k}.words.json" for k in ("sent", "sent2", "sent3", "sent4", "sent5")},
  **{f"vo_story_b{k}": SCR / "story_assets" / f"vo_story_b{k}.words.json" for k in (1, 2, 3, 4)},   # [story-pinki]
  **{f"vo_story_c{k}": SCR / "story_assets" / f"vo_story_c{k}.words.json" for k in (1, 2)},   # [relisten-pinki]
}

def norm(s):   # letters and vowel signs only, the nukta dropped (whisper writes ज़/ज, ढ़/ढ either way), marks as the words the voice says for them
    s = {"।": "पूर्णविराम", "?": "प्रश्नवाचक", ",": "अल्पविराम"}.get(s.strip(), s)
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if (unicodedata.category(ch)[0] in "LM") and ch != "़")

def sim(a, b): return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() if a and b else 0.0

LETTERS = re.compile(r"[ऄ-ॣ०-ॿ]")   # a Devanagari letter, matra or digit — not a mark (। ॥ ? , !)
def is_mark(w): return not LETTERS.search(w)

def align(shown, heard, dur=None, t0=0.0, v_end=None):
    """shown: the page's words; heard: [(word, start, end)]; dur: the clip's length (whisper's last end may overrun it).
    Returns each shown word's [start, end], the matched count and the said-word count. An order-keeping fuzzy DP match
    (a pair counts from similarity .55); the unmatched shown words take the heard words left between their matched
    neighbours (right-aligned at the front, where extras like "उदाहरण-" come first, else left-aligned) — so a mark the
    voice names ("लड़की पूर्णविराम पतंग") lights on its name; fewer free heard words than shown (whisper joined words) ->
    an even spread over the free span; none free -> a mark-only word (। ? ,) lights with the word before it, a said
    word sits inside the neighbouring heard word. Fewer than half of the said words matched (the recording says other
    words) -> an even spread over the clip's speech. No start past the clip's end."""
    n = len(shown)
    end_t = heard[-1][2] if heard else 0.0
    if dur: end_t = min(end_t, dur)
    A = [norm(w) for w in shown]; B = [norm(h[0]) for h in heard]
    m = len(B); S = [[sim(a, b) for b in B] for a in A]
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
    lex = [i for i in range(n) if not is_mark(shown[i])]; nl = len(lex); nm = sum(1 for i in match if not is_mark(shown[i]))
    starts = [None] * n
    if nl and nm * 2 < nl:   # the recording says other words: an even spread of the said words over its speech
        t0 = heard[0][1] if heard else 0.0
        for q, i in enumerate(lex): starts[i] = t0 + (end_t - t0) * q / nl
    else:
        for i_, j_ in match.items(): starts[i_] = heard[j_][1]
        gaps = []; prev_i, prev_j = -1, -1
        for i_, j_ in sorted(match.items()) + [(n, m)]:
            if i_ - prev_i > 1: gaps.append((prev_i + 1, i_ - 1, prev_j + 1, j_ - 1))   # shown i0..i1 unmatched, heard j0..j1 free
            prev_i, prev_j = i_, j_
        for i0, i1, j0, j1 in gaps:
            ns, nh = i1 - i0 + 1, max(0, j1 - j0 + 1)
            if nh >= ns:
                idx = list(range(j0, j1 + 1)); take = idx[-ns:] if i0 == 0 else idx[:ns]
                for q in range(ns): starts[i0 + q] = heard[take[q]][1]
            elif nh >= 1:
                a = heard[j0][1]; b_ = min(heard[j1][2], end_t, heard[j1 + 1][1] if j1 + 1 < m else end_t)
                for q in range(ns): starts[i0 + q] = a + (b_ - a) * q / ns
            else:
                said = [i for i in range(i0, i1 + 1) if not is_mark(shown[i])]; marks = [i for i in range(i0, i1 + 1) if is_mark(shown[i])]
                prev_end = min(heard[j0 - 1][2], end_t) if j0 - 1 >= 0 else 0.0; next_start = heard[j0][1] if j0 < m else end_t
                if j0 - 1 >= 0:   # nothing free after a heard word: the said words inside it
                    a = heard[j0 - 1][1]; b_ = min(heard[j0 - 1][2], end_t, next_start)
                    for q, i in enumerate(said): starts[i] = a + (b_ - a) * (q + 1) / (len(said) + 1)
                else:             # nothing free before the first heard word ([vo-rec2] from t0, where the voice starts — never in the room tone)
                    b_ = heard[0][1] if heard else end_t; a = min(t0, b_)
                    for q, i in enumerate(said): starts[i] = a + (b_ - a) * q / max(1, len(said))
                # a bare mark the voice does not name ("लाल । नीली ।" read with pauses) lights in the pause after its word:
                # mid-pause, at most 0.35 s after the word ends
                for i in marks: starts[i] = min(prev_end + 0.5 * max(0.0, next_start - prev_end), prev_end + 0.35)
    for i in range(n):
        if starts[i] is None: starts[i] = starts[i - 1] if i else 0.0   # a mark attached to its word ("है।”") shares its start
    # [vo-rec2] an unspoken closing mark ("है ?" with no "?" heard) lights where the voice ends (v_end: the last window within 35 dB of
    # the peak) — not at whisper's end for the last word, which can leave that word lit for 30 ms (T1C's "है" 2.62-2.65, the voice
    # running to 2.745); the line's light then runs 0.1 s past it
    if v_end and n and is_mark(shown[-1]) and (n - 1) not in match:
        vt = min(v_end, (dur or v_end) - 0.05)
        if vt > starts[n - 1]: starts[n - 1] = vt
        end_t = min(dur or (starts[n - 1] + 0.1), max(end_t, starts[n - 1] + 0.1))
    cap = max(0.0, end_t - 0.05)
    for q in range(n):   # never backwards, never past the clip's end
        if q and starts[q] < starts[q - 1]: starts[q] = starts[q - 1]
        if starts[q] > cap: starts[q] = cap
    # [vo-rec2] two said words never start together: a run of them on one start (whisper joined them — "माने" for "माँ ने" — and the
    # one left over had nothing free to take) shares the span up to the next word's start, by their letters
    q = 0
    while q < n:
        r = q
        while r + 1 < n and not is_mark(shown[r + 1]) and abs(starts[r + 1] - starts[q]) < 0.04: r += 1   # within 40 ms: no two said words start that close
        if r > q and not is_mark(shown[q]):
            a = starts[q]; b_ = next((starts[k] for k in range(r + 1, n) if starts[k] > starts[r] + 0.005), end_t)
            lens = [max(1, len(norm(shown[k]))) for k in range(q, r + 1)]; acc = 0
            for k in range(q, r + 1): starts[k] = a + (b_ - a) * acc / sum(lens); acc += lens[k - q]
        q = r + 1
    ends = starts[1:] + [end_t]
    return [[round(a, 3), round(b, 3)] for a, b in zip(starts, ends)], nm, nl

def owners(vid):
    """the *_assets folder(s) next to this script that keep this ID's clip: build.py copies THEIR .ogg into the dist on every
    build (the TTS clips of the recap rows, the demos, G1-G4 / P1 / P2, the stamp sentences), so the recording must land there
    too or the next build puts the TTS clip back over it (which is exactly what happened on 2026-10-28 until this was found: the
    dist carried the recordings' word times on the TTS clips). The TTS original is kept once as <ID>.tts.ogg."""
    return [d for d in sorted(SCR.glob("*_assets")) if (d / f"{vid}.ogg").exists() or (d / f"{vid}.tts.ogg").exists()]

def encode(src_wav, dst_ogg, ss=None, to=None):
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if ss is not None: cmd += ["-ss", f"{ss:.3f}"]
    if to is not None: cmd += ["-to", f"{to:.3f}"]
    cmd += ["-i", str(src_wav)]
    if GAIN: cmd += ["-af", f"volume={GAIN}dB"]
    cmd += ["-c:a", "libopus", "-b:a", "96k", "-ar", "48000", str(dst_ogg)]
    subprocess.run(cmd, check=True)
    for d in owners(dst_ogg.stem):
        tts = d / f"{dst_ogg.stem}.tts.ogg"
        if not tts.exists() and (d / dst_ogg.name).exists(): (d / dst_ogg.name).replace(tts)
        shutil.copy2(dst_ogg, d / dst_ogg.name)

applied, texts, skipped = {}, {}, {}
# [vo-rec2] a clip the regenerated manifest no longer lists (the first batch's unplayed extras: vo_demo*_conclude / full, vo_demo_again,
# vo_g2/g3_hint3) keeps the text the last run gave it (the old manifest's line), not whisper's spelling
PREV_TEXTS = json.loads((REC / "derived.json").read_text(encoding="utf-8")).get("texts", {}) if (REC / "derived.json").exists() else {}
split_at = None   # [vo-rec2] the sent4 split happens only for a combined take
AUD.mkdir(parents=True, exist_ok=True)
DROP_META = ("voice", "rate", "pitch", "gain_db")   # [vo-rec2] a words.json that was a TTS take's loses the synthesiser's settings once a recording replaces it
def lead_in(f, db=-35.0):
    """[vo-rec2] where the voice starts: the first 10 ms window (5 ms steps) within `db` of the clip's peak, less 10 ms. Whisper puts
    the first word at 0.00 although every take opens with ~0.27 s of room tone — that word would light that much before it is said."""
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
    r = np.array([np.sqrt(np.mean(x[i:i + 480] ** 2)) for i in range(0, max(1, len(x) - 480), 240)]) + 1e-9
    k = int(np.argmax(20 * np.log10(r / r.max()) > db)); return round(max(0.0, k * 0.005 - 0.01), 3)
def _env(fname):   # [vo-rec2] the clip's loudness in 10 ms windows every 5 ms, in dB under its peak
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(REC / fname), "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.float32); w, h = 480, 240
    r = np.array([np.sqrt(np.mean(x[i:i + w] ** 2)) for i in range(0, max(1, len(x) - w), h)]) + 1e-9
    return 20 * np.log10(r / r.max()), h / 48000
lead_fixed = {}
# ---- 2+3. every named recording ----
for f in sorted(REC.glob("*.wav")):
    if f.name in SKIP: skipped[f.name] = SKIP[f.name]; continue
    vid = RENAME.get(f.name, f.stem); heard = [tuple(w) for w in T[f.name]["words"]]
    li = lead_in(f) if heard else 0.0
    if heard:   # [vo-rec2] every said word starts where its sound does: whisper puts a word's start inside the pause before it (the first
        # word at 0.00 over the take's ~0.27 s of room tone; "तुम्हारा" at 1.22 s in T1C's example while the clip is quiet 0.87-1.50 s) —
        # a start inside a quiet run (below -35 dB of the peak for >= 60 ms) moves to the run's end, never later than the word's end
        # less 50 ms; a bare mark ("।") keeps its time: it is meant to light in the pause
        e_, hop_ = _env(f.name); q_ = e_ < -35.0; moved_ = []
        for k_, (w_, s_, en_) in enumerate(heard):
            i_ = int(s_ / hop_)
            if is_mark(w_) or i_ >= len(q_) or not q_[i_]: continue
            a_ = i_
            while a_ > 0 and q_[a_ - 1]: a_ -= 1
            b_ = i_
            while b_ < len(q_) and q_[b_]: b_ += 1
            if (b_ - a_) * hop_ < 0.06: continue
            ns_ = round(min(b_ * hop_ + 0.005, en_ - 0.05), 3)
            if ns_ - s_ > 0.02: heard[k_] = (w_, ns_, en_); moved_.append([w_, s_, ns_])
        if moved_: lead_fixed[f.name] = moved_
        v_end = round((len(e_) - 1 - int(np.argmax((e_ > -35.0)[::-1]))) * hop_ + 0.01, 3)   # [vo-rec2] the voice's end (for an unspoken closing mark)
    else: v_end = None
    rec_day = datetime.date.fromtimestamp(f.stat().st_mtime).isoformat()   # [vo-rec2] the batch the file came in (cp -p keeps the date)
    if vid == "vo_stamp_sent4" and not (REC / "vo_stamp_sent5.wav").exists():   # the split: rounds 4 (two questions) and 5 (the rest of the letter) — [vo-rec2] only for a combined take
        k = next(i for i, h in enumerate(heard) if norm(h[0]).startswith("उनक"))
        mid = round((heard[k - 1][2] + heard[k][1]) / 2, 3)
        encode(f, AUD / "vo_stamp_sent4.ogg", to=mid); encode(f, AUD / "vo_stamp_sent5.ogg", ss=mid)
        for d in owners("vo_stamp_sent4"): shutil.copy2(AUD / "vo_stamp_sent5.ogg", d / "vo_stamp_sent5.ogg")   # round 5's half next to round 4's
        parts = {"vo_stamp_sent4": [h for h in heard[:k]], "vo_stamp_sent5": [(h[0], round(h[1] - mid, 3), round(h[2] - mid, 3)) for h in heard[k:]]}
        split_at = mid
        durs = {"vo_stamp_sent4": mid, "vo_stamp_sent5": round(T[f.name]["dur"] - mid, 3)}
    else:
        encode(f, AUD / f"{vid}.ogg"); parts = {vid: heard}; durs = {vid: T[f.name]["dur"]}
        if f.name in TRIM:   # [relisten-pinki] the same take without its opening words, as a clip of its own
            cid, cut = TRIM[f.name]; encode(f, AUD / f"{cid}.ogg", ss=cut)
            parts[cid] = [(h[0], round(h[1] - cut, 3), round(h[2] - cut, 3)) for h in heard if h[1] >= cut - 0.05]; durs[cid] = round(T[f.name]["dur"] - cut, 3)
    for pid, hw in parts.items():
        texts[pid] = SPOKEN.get(pid) or MAN.get(vid) or PREV_TEXTS.get(pid) or T[f.name]["text"]
        applied[pid] = {"file": f.name, "dur": durs[pid], "heard_to": round(hw[-1][2], 3) if hw else None, "heard": " ".join(h[0] for h in hw)}   # dur: the clip's length (whisper's last end may overrun it)
        if pid in SYNC:
            tf = SYNC[pid]; data = json.loads(tf.read_text(encoding="utf-8"))
            shown = (SHOWN_OVERRIDE.get(pid) or data.get("shown") or data["text"]).split()
            data["text"] = texts[pid]
            if pid in SHOWN_OVERRIDE or "shown" in data: data["shown"] = SHOWN_OVERRIDE.get(pid, data.get("shown"))
            wt, nm, nl = align(shown, hw, applied[pid]["dur"], t0=(li if (heard and pid == vid) else 0.0), v_end=(v_end if pid == vid else None))   # [vo-rec2] t0 / v_end: the voice's start / end
            if wt and len(wt) != len(shown): raise SystemExit(f"{pid}: {len(wt)} times for {len(shown)} shown words")
            for k in DROP_META: data.pop(k, None)
            data["word_times"] = wt; data["source"] = f"recording {f.name} ({rec_day}), faster-whisper word times, vo_rec.py"
            tf.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            applied[pid]["sync"] = {"file": str(tf.relative_to(SCR)), "n": len(wt), "matched": f"{nm}/{nl}", "starts": [t[0] for t in wt]}
            print(f"sync  {pid:22s} [{nm}/{nl}] {' '.join(f'{w}@{t[0]:.2f}' for w, t in zip(shown, wt))}")
# ---- 4. the cues the pages time on their clips ----
# [relisten-pinki] T0B's cues on the clips' own clocks: the explanation lights sentence 1 at "पहले" and sentence 2 at "जबकि"; the
# moral lights the commas at "विराम"
def _at(fname, prefix): return round(next(h[1] for h in T[fname]["words"] if norm(h[0]).startswith(prefix)), 3)
def onset(fname, prefix, back=0.25, fwd=0.35, quiet_db=-30.0, min_quiet=0.03):
    """[vo-rec2] the moment a word's sound starts: whisper's start of the first word beginning with `prefix`, moved to the end of the
    quiet run (a pause, or a stop's closure: below quiet_db under the peak for >= min_quiet) nearest to it within -back..+fwd s —
    whisper's word starts wander 0.1-0.2 s into a pause or a closure (L2's "ठप्पा": whisper 4.94, its burst 5.12 on the first
    batch). No quiet run there (a voiced stop running on) -> whisper's start."""
    t = _at(fname, prefix); e, hop = _env(fname); lo, hi = int(max(0, t - back) / hop), min(len(e) - 1, int((t + fwd) / hop))
    runs, s = [], None
    for i in range(lo, hi + 1):
        q = e[i] < quiet_db
        if q and s is None: s = i
        if (not q or i == hi) and s is not None:
            if (i - s) * hop >= min_quiet and not q: runs.append(i * hop + 0.005)   # the first loud window's centre after the run
            s = None
    best = min(runs, key=lambda o: abs(o - t)) if runs else t
    return round(best, 3), t
def speech_end(fname):   # [vo-rec2] [l1-late]'s measure: ffmpeg silencedetect at -45 dB, the start of the silence that runs to the clip's end
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(REC / fname), "-af", "silencedetect=noise=-45dB:d=0.2", "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    st = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", err)]; en = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", err)]
    dur = T[fname]["dur"]   # ffmpeg closes the last silence at the end of the file (silence_end = the file's length)
    return round(st[-1], 3) if st and (len(st) > len(en) or en[-1] >= dur - 0.06) else dur
def beak_bits(ogg, step=0.025, win=12, rel=0.5, db=-18):   # [vo-rec2] the [dun-chrome] detector (reproduces dun_assets/cel_bits.json bit for bit at 48 kHz)
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ogg), "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.float32); h = int(48000 * step); n = int(len(x) / h)
    r = np.array([np.sqrt(np.mean(x[i * h:(i + 1) * h] ** 2)) for i in range(n)]); pk = r.max()
    return "".join("1" if (r[i] > rel * r[max(0, i - win):i + win + 1].max() and r[i] > pk * 10 ** (db / 20)) else "0" for i in range(n))
moral_wav = "vo_story_moral.wav" if "vo_story_moral.wav" in T else "4.wav"
cues = {"explain_s": [_at("vo_story_r1.wav", "पहल"), _at("vo_story_r1.wav", "जबक")], "moral_s": _at(moral_wav, "विराम")}
onsets = {}
# the gates' headlines arrive with their words (the gate script's GATE_CAPTION_AT_MS): "चलिए, शुरू करें!", "चलिए, साथ में करें!", "अब आपकी बारी!"
gate_cue = {}
for k, pre in (("tutorial", "चल"), ("guided", "चल"), ("practice", "अब")):
    if f"vo_pt_{k}.wav" in T and f"vo_pt_{k}" in applied:
        o, w = onset(f"vo_pt_{k}.wav", pre); gate_cue[k] = int(round(o * 1000)); onsets[f"vo_pt_{k}"] = {"word": pre, "whisper": w, "onset": o}
# L1: the thinking girl on "दादाजी" (pace.dada), the letter 2 s before the narration's speech ends ([l1-late]: pace.letter)
if "vo_letter_intro" in applied:
    o, w = onset("vo_letter_intro.wav", "दाद"); onsets["vo_letter_intro"] = {"word": "दाद", "whisper": w, "onset": o}
    cues["letter_dada_ms"] = int(round(o * 1000)); cues["letter_speech_end_s"] = speech_end("vo_letter_intro.wav")
# L2: the stamps' glow on the instruction's "ठप्पा" (pace.thappa); the instruction's length (pace.intro_ms, the bird's clock when the clip cannot be read)
if "vo_stamp_intro" in applied:
    o, w = onset("vo_stamp_intro.wav", "ठप"); onsets["vo_stamp_intro"] = {"word": "ठप", "whisper": w, "onset": o}
    cues["stamp_thappa_ms"] = int(round(o * 1000)); cues["stamp_intro_ms"] = int(round(applied["vo_stamp_intro"]["dur"] * 1000))
cel_bits = {"vo": "vo_well_done", "step_ms": 25, "bits": beak_bits(AUD / "vo_well_done.ogg"), "clip_s": applied["vo_well_done"]["dur"],
            "method": "dun_assets/cel_bits.json's detector on the recording (RMS per 25 ms, open above 0.5 x the local max over +-12 frames and within 18 dB of the peak)"} if "vo_well_done" in applied else None
derived = {"applied": applied, "texts": texts, "skipped": skipped, "kept_first": KEPT_FIRST, "snapped": lead_fixed, "gate_cue_ms": gate_cue, "cues": cues, "onsets": onsets, "cel_bits": cel_bits,
           "stamp_sent4_split_s": split_at, "gain_db": GAIN, "note": "written by vo_rec.py; build.py reads texts, gate_cue_ms, cues, cel_bits"}
(REC / "derived.json").write_text(json.dumps(derived, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"applied {len(applied)} clips, skipped {len(skipped)}; gate cue {derived['gate_cue_ms']} ms; sent4 split at {split_at} s")
