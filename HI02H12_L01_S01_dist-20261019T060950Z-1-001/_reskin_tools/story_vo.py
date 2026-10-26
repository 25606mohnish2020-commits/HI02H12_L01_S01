"""Voice-over + per-word timings for the story pages' lines (Figma FLN-by-MJ nodes 435:5, 476:198 and 488:190).

usage: python -I -X utf8 story_vo.py s1|s2|r0|r1 [--voice hi-IN-SwaraNeural] [--rate=-15%] [--pitch=+0Hz]
       generates ONE line; the other line's files are left alone (a re-run gives a slightly different take)
       (needs edge-tts >= 7.3 — 7.2.x is refused by the server with HTTP 403 — and ffmpeg on PATH)

Writes, next to this script:
  story_assets/vo_story_<line>.ogg          Opus 32 kbit/s mono 48 kHz, the same encoding as the game's other clips
  story_assets/vo_story_<line>.words.json   one [start, end] pair in seconds per displayed word, from the
                                        synthesiser's own word boundaries; build.py puts them in the card and
                                        the page reveals each word at its start time on the clip's own clock.
Voice choice: the game's clips are a female voice at ~205-220 Hz median pitch; hi-IN-SwaraNeural is the
female Hindi voice, and -15% rate matches their pace (measured on vo_ro_d1: 2.25 s of speech vs 1.91 s).
If a human recording replaces the clip, re-derive the timings with align_story_vo.py.
"""
import sys, json, asyncio, argparse, pathlib, subprocess, tempfile, unicodedata
import edge_tts

# exactly the frames' texts: node 475:195 (minus its leading space), then node 476:384
TEXTS = {"s1": "चिंटू दौड़कर आया और बोला दादी बिल्ली दूध पी रही है दादी बोली उसे भगाओ मत पीने दो",
         "s2": "चिंटू हैरान होकर बोला क्या उसे सारा दूध पीने दूँ दादी हँसकर बोली अरे नहीं उसे भगाओ दूध मत पीने दो",
         # the read-again page (node 488:190): its intro line, then the box's punctuated sentences (node 488:374 as
         # of 2026-10-21 evening, its third version; "\n" = the frame's line breaks; it has a space before the first
         # danda), read WITH the pauses the punctuation asks for
         "r0": "अब इन्हीं वाक्यों को फिर से सुनते हैं।",
         "r1": "चिंटू दौड़कर आया और बोला, “दादी! बिल्ली दूध पी रही है ।”\n"
               "दादी बोली, “उसे भगाओ, मत पीने दो।”\n"
               "चिंटू हैरान होकर बोला, “क्या? उसे सारा दूध पीने दूँ?” दादी हँसकर बोली, “अरे नहीं! उसे भगाओ। दूध मत पीने दो।”"}
SCR = pathlib.Path(__file__).resolve().parent
OUT = SCR / "story_assets"

ap = argparse.ArgumentParser()
ap.add_argument("line", choices=sorted(TEXTS))
ap.add_argument("--voice", default="hi-IN-SwaraNeural")
ap.add_argument("--rate", default="-15%")
ap.add_argument("--pitch", default="+0Hz")
args = ap.parse_args()
TEXT = TEXTS[args.line]

async def synth():
    comm = edge_tts.Communicate(TEXT.replace("\n", " "), args.voice, rate=args.rate, pitch=args.pitch, boundary="WordBoundary")
    audio, marks = bytearray(), []
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
        elif chunk["type"] == "WordBoundary":
            t0 = chunk["offset"] / 1e7
            marks.append((chunk["text"], t0, t0 + chunk["duration"] / 1e7))
    return bytes(audio), marks

audio, marks = asyncio.run(synth())
words = TEXT.split()
# a displayed word carries its punctuation (“दादी!); the synthesiser's boundaries are the bare words. A token that is
# punctuation alone (the frame's "है ।”" has a space before the danda) is shown together with the word before it.
bare = lambda w: "".join(ch for ch in w if unicodedata.category(ch)[0] in "LM")
marks = [m for m in marks if bare(m[0])]
spoken = [w for w in words if bare(w)]
if [bare(m[0]) for m in marks] != [bare(w) for w in spoken]:
    raise SystemExit(f"word boundaries do not match the text:\n  {[m[0] for m in marks]}\n  {spoken}")

OUT.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as td:
    mp3 = pathlib.Path(td) / "vo.mp3"; mp3.write_bytes(audio)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-ac", "1", "-ar", "48000",
                    "-c:a", "libopus", "-b:a", "32k", str(OUT / f"vo_story_{args.line}.ogg")], check=True)
times, it = [], iter(marks)
for w in words:
    if bare(w): _, t0, t1 = next(it); times.append([round(t0, 3), round(t1, 3)])
    else: times.append(list(times[-1]))
(OUT / f"vo_story_{args.line}.words.json").write_text(json.dumps({"text": TEXT, "voice": args.voice, "rate": args.rate,
    "pitch": args.pitch, "word_times": times}, ensure_ascii=False, indent=1), encoding="utf-8")
for w, (t0, t1) in zip(words, times): print(f"{t0:6.3f}-{t1:6.3f}  {w}")
