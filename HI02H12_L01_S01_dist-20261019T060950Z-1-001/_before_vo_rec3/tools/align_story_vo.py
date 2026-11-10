"""Check (or re-derive) the story / recap pages' word timings against the clip itself.

usage: python -I -X utf8 align_story_vo.py s1|s2|r0|r1|<page>_<line> [<clip.ogg>] [--write]
  default clip: story_assets/vo_story_<line>.ogg; timings file: story_assets/vo_story_<line>.words.json
  <page>_<line> (recap_... for T1, demo1_... for T2, demo2_... for T3, demo3_... for T4, see recap_vo.py): <page>_assets/vo_<page>_<line>.ogg / .words.json —
  the stored times are the SHOWN words' (T1's example lines say "उदाहरण- ..." and show the sentence), so the spoken
  words are aligned and the tail kept
Runs faster-whisper (model "small", word timestamps) on the clip and lines its words up with that line's
words in order. Prints both sets of start times side by side. With --write, the whisper starts replace the
stored ones — use that after a human recording replaces the synthesised clip, then rerun build.py.
"""
import sys, json, pathlib, difflib, unicodedata
from faster_whisper import WhisperModel

SCR = pathlib.Path(__file__).resolve().parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
PAGES = ("recap", "demo1", "demo2", "demo3")
if not args or (args[0] not in ("s1", "s2", "r0", "r1") and not args[0].startswith(tuple(p + "_" for p in PAGES))): raise SystemExit(__doc__)
line = args[0]
if line.startswith(tuple(p + "_" for p in PAGES)):
    page, key = line.split("_", 1)
    clip = pathlib.Path(args[1]) if len(args) > 1 else SCR / f"{page}_assets" / f"vo_{page}_{key}.ogg"
    tfile = SCR / f"{page}_assets" / f"vo_{page}_{key}.words.json"
else:
    clip = pathlib.Path(args[1]) if len(args) > 1 else SCR / "story_assets" / f"vo_story_{line}.ogg"
    tfile = SCR / "story_assets" / f"vo_story_{line}.words.json"
data = json.loads(tfile.read_text(encoding="utf-8"))
words = data["text"].split()
# the recap's stored times belong to the shown words = the spoken text's tail (the intro's title is not spoken: its
# single time pair spans the clip, so it is only reported here, never rewritten)
shown = data.get("shown", data["text"]).split()
tail = len(words) - len(shown) if words[len(words) - len(shown):] == shown else None

import subprocess, numpy as np   # decode with ffmpeg: the installed PyAV is older than faster-whisper expects
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(clip), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
samples = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
model = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = model.transcribe(samples, language="hi", word_timestamps=True, initial_prompt=data["text"])
heard = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]

# align heard tokens to page words by text similarity, keeping order
# bare letters + marks: a page word carries its punctuation (“दादी!), whisper's words may not
norm = lambda s: "".join(ch for ch in s if unicodedata.category(ch)[0] in "LM")
sm = difflib.SequenceMatcher(a=[norm(w) for w in words], b=[norm(h[0]) for h in heard], autojunk=False)
starts = [None] * len(words)
for a0, b0, n in sm.get_matching_blocks():
    for k in range(n): starts[a0 + k] = heard[b0 + k][1]
stored = ([None] * tail + [t[0] for t in data["word_times"]]) if tail else [t[0] for t in data["word_times"]]
if len(stored) != len(words): stored = [None] * len(words)   # the intro: nothing stored per spoken word
print(f"heard: {' '.join(h[0] for h in heard)}")
print(" #  word        stored  whisper   diff")
diffs = []
for i, w in enumerate(words):
    ws = starts[i]
    d = None if ws is None or stored[i] is None else ws - stored[i]
    if d is not None: diffs.append(abs(d))
    print(f"{i+1:2d}  {w:10s} {'   -   ' if stored[i] is None else f'{stored[i]:7.3f}'}  {'   -   ' if ws is None else f'{ws:7.3f}'}  {'' if d is None else f'{d:+.3f}'}")
print(f"matched {len(diffs)}/{len(words)} words; mean |diff| {sum(diffs)/max(1,len(diffs)):.3f}s, max {max(diffs or [0]):.3f}s")
if "--write" in sys.argv:
    if None in starts: raise SystemExit("some words were not heard — not writing; fix by hand")
    if tail is None and "shown" in data: raise SystemExit("the shown text is not the spoken text's tail — not writing")
    ends = starts[1:] + [heard[-1][2]]
    data["word_times"] = [[round(a, 3), round(b, 3)] for a, b in zip(starts, ends)][tail or 0:]
    data["source"] = f"faster-whisper alignment of {clip.name}"
    tfile.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8"); print("written", tfile)
