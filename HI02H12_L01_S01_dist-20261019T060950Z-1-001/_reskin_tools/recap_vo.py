"""Voice-over + per-word timings for the Figma pages after the story: T1 "ये हैं तीन विराम चिह्न" (frame 508:2, page
"recap"), T2, the first run-on sentence demo (frame 519:32, page "demo1"), T3, the second (frame 521:288, "demo2"),
T4, the third (frame 523:320, "demo3"), G1, the first sentence the child punctuates (frame 525:354, "g1"), G2, the
second (frame 600:197, "g2"), G3, the third (frame 528:424, "g3"), G4 (the reference game's P4 layout, "g4"), P1 and P2 (the
same layout again, "p1", "p2").

usage: python -I -X utf8 recap_vo.py <page> <line>|all [--voice hi-IN-SwaraNeural] [--rate=-15%] [--pitch=+0Hz]
       pages: recap (T1), demo1 (T2), demo2 (T3), demo3 (T4), g1 (G1), g2 (G2), g3 (G3), g4 (G4), p1 (P1), p2 (P2) — see LINES
       (needs edge-tts >= 7.3 — 7.2.x is refused by the server with HTTP 403 — and ffmpeg on PATH)
       Each run gives a slightly different take, so regenerate only the line(s) that changed.

T1 narrates ten lines: the intro (the title "ये हैं तीन विराम चिह्न" appears as it starts to sound), then for each mark
its name, when it is used and an example. The example lines SAY "उदाहरण- ..." but SHOW only the sentence, so their
timings cover the shown words only (the shown text is the spoken text's tail).
T2 narrates four: the intro (the title bar appears whole as it starts), the sentence read without a pause (its words
appear one by one), the mark's name (the tile is tapped for the child), and the sentence read again with the mark
named at its end (words and then the mark highlighted one by one). T3 the same four for its own sentence and mark;
its intro is the title bar's own line (T2's intro, "आइए कुछ वाक्यों के उदाहरण से समझते हैं", opens the examples), and its
second reading ends the sentence with "?" before naming the mark: the synthesiser then pauses ~1 s after the question
(its pitch on "क्या है?" is the same falling contour as the run-on's — normal for a Hindi क्या-question).
T4 the same four for a sentence that needs TWO commas (the frame's sentence already ends with its danda): the second
reading names each comma where it sits ("आम, अल्पविराम, केला, अल्पविराम, ...") so each slot can light as its comma is
named, the way T2's slot lights on "पूर्णविराम" at the sentence's end.
G1 narrates two: the title bar's own line, the instruction "वाक्य सुनिए और सही चिह्न लगाइए ।" (the bar appears as it
starts), and the sentence read without a pause (its words appear one by one); then the CHILD taps the mark. The name
said on the right tap is T2's "पूर्ण विराम" clip (vo_demo1_purn), the same voice, so it is not made again here.
G2 (frame 600:197, "g2") narrates only its sentence: its instruction is G1's very line (vo_g1_intro, played again) and the
name on the right tap is T3's "प्रश्नवाचक चिह्न" (vo_demo2_prashn).
G3 (frame 528:424, "g3") likewise: its sentence only (the frame's, already ending with its danda, read without a pause;
the danda is shown with "हैं"); instruction vo_g1_intro, name on the right tap T4's "अल्प विराम" (vo_demo3_alp).
G4 (the reference game's page-11 P4 layout, "g4") narrates five: the title's instruction (prompt), the first wrong tap's line
(try: P4's "चित्र को ध्यान से देखिए और उससे मिलते हुए वाक्य पर टैप करिए।" made for this page) and the three sentence options as
written, each read with its own punctuation — the synthesiser pauses at a danda, so "लड़की । पतंग ..." and "... उड़ा । रही है"
are heard broken where their danda sits. A pill lights its words from these timings (build.py: a lone danda lights during
the pause it makes).
P1 (the same P4 layout, "p1") narrates only its three sentence options, as written, each with its question mark where it
sits — the synthesiser lifts and pauses at a "?", so "क्या? यह ..." and "क्या यह आपकी? किताब है" are heard broken where theirs
sits. Its title is G4's very line ("सही विराम चिह्न वाला वाक्य चुनिए ।") and so is its try-again line: vo_g4_prompt and
vo_g4_try are played again, not made twice.
P2 ("p2") likewise: its three options only, as written — with the danda where it sits (heard as the sentence ending there:
"लाल । नीली । ..."), with no mark at all (heard run on, no pause) and with its commas (heard with a short pause at each).

Writes, next to this script:
  <page>_assets/vo_<page>_<line>.ogg          Opus 32 kbit/s mono 48 kHz, the same encoding as the game's other clips
  <page>_assets/vo_<page>_<line>.words.json   {"text": spoken, "shown": displayed, "word_times": [[start, end], ...]}
                                        one pair per DISPLAYED word, from the synthesiser's own word boundaries;
                                        build.py puts the starts in the card and the page reveals / highlights each
                                        word at its start on the clip's own clock. A line whose shown text is NOT what
                                        is spoken (the intros) gets one pair per shown word spanning the whole clip.
Voice: the same placeholder voice as the story pages (story_vo.py) — hi-IN-SwaraNeural at -15%, which matches the
game's recorded clips' pace. These are PLACEHOLDERS until the VO team records them; the lesson already has human
clips of the three names (vo_nm_purn / vo_nm_alp / vo_nm_prashn: "पूर्ण विराम" / "अल्प विराम" / "प्रश्नवाचक चिह्न"),
not used here so that each page keeps one voice until everything is recorded. For a human recording: drop it in as
<page>_assets/vo_<page>_<line>.ogg and re-derive the timings with align_story_vo.py <page>_<line> --write, then rebuild.
"""
import sys, json, asyncio, argparse, pathlib, subprocess, tempfile, unicodedata
import edge_tts

# (spoken text, shown text or None when they are the same) — the texts are the request's / the frame's, verbatim
LINES = {
  "recap": {
    "intro":       ("आइए समझते हैं कि कौन-से चिह्न का प्रयोग कब किया जाता है ।", "ये हैं तीन विराम चिह्न"),
    "purn_name":   ("पूर्ण विराम", None),
    "purn_when":   ("बात पूरी होने पर", None),
    "purn_eg":     ("उदाहरण- रीना स्कूल गई ।", "रीना स्कूल गई ।"),
    "alp_name":    ("अल्प विराम", None),
    "alp_when":    ("वाक्य में थोड़ा रुकने पर", None),
    "alp_eg":      ("उदाहरण- आम, केला, संतरा और सेब", "आम, केला, संतरा और सेब"),
    "prashn_name": ("प्रश्नवाचक चिह्न", None),
    "prashn_when": ("सवाल पूछने पर", None),
    "prashn_eg":   ("उदाहरण- तुम्हारा घर कहाँ है ?", "तुम्हारा घर कहाँ है ?"),
  },
  "demo1": {
    "intro":  ("आइए कुछ वाक्यों के उदाहरण से समझते हैं ।", "सुनो यह वाक्य बिना रुके पढ़ा गया ।"),
    "sent":   ("रीना स्कूल जा रही है", None),
    "purn":   ("पूर्ण विराम", None),
    "full":   ("रीना स्कूल जा रही है, पूर्णविराम।", None),
  },
  "demo2": {
    "intro":  ("सुनो, यह वाक्य बिना रुके पढ़ा गया ।", "सुनो यह वाक्य बिना रुके पढ़ा गया ।"),
    "sent":   ("तुम्हारा नाम क्या है", None),
    "prashn": ("प्रश्नवाचक चिह्न", None),
    "full":   ("तुम्हारा नाम क्या है? प्रश्नवाचक चिह्न।", None),
  },
  "demo3": {
    "intro":  ("सुनो, यह वाक्य बिना रुके पढ़ा गया ।", "सुनो यह वाक्य बिना रुके पढ़ा गया ।"),
    "sent":   ("मेरे पास आम केला सेब और संतरा है ।", None),
    "alp":    ("अल्प विराम", None),
    "full":   ("मेरे पास आम, अल्पविराम, केला, अल्पविराम, सेब और संतरा है।", None),
  },
  "g1": {
    "intro":  ("वाक्य सुनिए और सही चिह्न लगाइए ।", None),
    "sent":   ("राजू गेंद से खेल रहा था", None),
  },
  "g2": {
    "sent":   ("तुम कहाँ जा रहे हो", None),
  },
  "g3": {
    "sent":   ("बाग में गुलाब गेंदा और चमेली के फूल हैं ।", None),
  },
  "g4": {
    "prompt": ("सही विराम चिह्न वाला वाक्य चुनिए ।", None),
    "try":    ("वाक्यों को ध्यान से पढ़िए और सही विराम चिह्न वाले वाक्य पर टैप करिए।", None),
    "o1":     ("लड़की पतंग उड़ा रही है ।", None),
    "o2":     ("लड़की । पतंग उड़ा रही है", None),
    "o3":     ("लड़की पतंग उड़ा । रही है", None),
  },
  "p1": {
    "o1":     ("क्या यह आपकी किताब है?", None),
    "o2":     ("क्या? यह आपकी किताब है", None),
    "o3":     ("क्या यह आपकी? किताब है", None),
  },
  "p2": {
    "o1":     ("मेरे पास लाल । नीली । हरी और पीली पेंसिल हैं ।", None),
    "o2":     ("मेरे पास लाल नीली हरी और पीली पेंसिल हैं ।", None),
    "o3":     ("मेरे पास लाल, नीली, हरी और पीली पेंसिल हैं ।", None),
  },
}
SCR = pathlib.Path(__file__).resolve().parent

ap = argparse.ArgumentParser()
ap.add_argument("page", choices=sorted(LINES))
ap.add_argument("line")
ap.add_argument("--voice", default="hi-IN-SwaraNeural")
ap.add_argument("--rate", default="-15%")
ap.add_argument("--pitch", default="+0Hz")
args = ap.parse_args()
PAGE = LINES[args.page]
if args.line != "all" and args.line not in PAGE: raise SystemExit(f"lines of {args.page}: {', '.join(sorted(PAGE))}")
OUT = SCR / f"{args.page}_assets"

bare = lambda w: "".join(ch for ch in w if unicodedata.category(ch)[0] in "LM")   # letters + combining marks only

async def synth(text):
    comm = edge_tts.Communicate(text, args.voice, rate=args.rate, pitch=args.pitch, boundary="WordBoundary")
    audio, marks = bytearray(), []
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
        elif chunk["type"] == "WordBoundary":
            t0 = chunk["offset"] / 1e7
            marks.append((chunk["text"], t0, t0 + chunk["duration"] / 1e7))
    return bytes(audio), marks

def timings(marks, spoken, shown):
    """Start/end per SHOWN word. The synthesiser's boundaries may split or join tokens differently from the text
    (a hyphen, a danda), so the match is made letter by letter: every letter of the spoken text gets the time of
    the boundary token it came from, and a shown word takes the times of its own letters. A punctuation-only word
    (the frame's "।" / "?" after a space) is shown with the word before it."""
    letters = []   # (char, t0, t1) for every letter the synthesiser reported
    for tok, t0, t1 in marks:
        for ch in bare(tok): letters.append((ch, t0, t1))
    spoken_letters = bare(spoken)
    got = "".join(ch for ch, _, _ in letters)
    if got != spoken_letters:
        raise SystemExit(f"word boundaries do not cover the text:\n  heard  {got}\n  wanted {spoken_letters}")
    words = shown.split()
    shown_letters = "".join(bare(w) for w in words)
    # a shown text that is not what is spoken (an intro) appears whole: every word spans the clip
    if not spoken_letters.endswith(shown_letters):
        return [[round(marks[0][1], 3), round(marks[-1][2], 3)]] * len(words)
    pos = len(spoken_letters) - len(shown_letters)   # the shown text is the spoken text's tail
    times = []
    for w in words:
        n = len(bare(w))
        if n: times.append([round(letters[pos][1], 3), round(letters[pos + n - 1][2], 3)]); pos += n
        else: times.append(list(times[-1]))
    return times

OUT.mkdir(exist_ok=True)
for key in (sorted(PAGE) if args.line == "all" else [args.line]):
    spoken, shown = PAGE[key]
    shown_text = spoken if shown is None else shown
    audio, marks = asyncio.run(synth(spoken))
    times = timings(marks, spoken, shown_text)
    with tempfile.TemporaryDirectory() as td:
        mp3 = pathlib.Path(td) / "vo.mp3"; mp3.write_bytes(audio)
        # the synthesiser leaves ~1.1 s of silence after the last word; several such tails would make a page drag, so
        # the tail is cut to 0.3 s (the page adds its own breath between beats). Only the end is cut: the word times stand.
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-ac", "1", "-ar", "48000",
                        "-af", "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.3,areverse",
                        "-c:a", "libopus", "-b:a", "32k", str(OUT / f"vo_{args.page}_{key}.ogg")], check=True)
    (OUT / f"vo_{args.page}_{key}.words.json").write_text(json.dumps({"text": spoken, "shown": shown_text, "voice": args.voice,
        "rate": args.rate, "pitch": args.pitch, "word_times": times}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"== {key}: {spoken}   (boundaries: {' | '.join(m[0] for m in marks)})")
    for w, (t0, t1) in zip(shown_text.split(), times): print(f"   {t0:6.3f}-{t1:6.3f}  {w}")
