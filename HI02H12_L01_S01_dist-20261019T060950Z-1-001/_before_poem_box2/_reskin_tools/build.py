"""Re-skin HI02H12_L01_S01 (punctuation) onto the Ek-aur-Anek reference chrome.

Base   = the reference build's CSS + body markup + engine JS (landing, boot loader, peek-gate
         transitions, dev nav, SVG nav/play buttons, mascot head, end screen, background music ...).
Ported = this lesson's four content modules (QTYPE_RECAP, BUILD_PUNCT, EVIDENCE_QA, SORT_QTYPE/SORT_WORDS),
         their evidence helpers + CSS, its card.json and its assets.
Added  = the Figma pages: the title page, the story pages T0 / T0B, the three-marks recap T1 (MARKS_RECAP, in
         place of the ported QTYPE_RECAP cards, which stay in the engine unused) and the first run-on sentence demo
         T2 + T3 + T4 (PUNCT_DEMO, in place of the ported BUILD_PUNCT auto demos; that module still serves the guided
         and practice builders) and G1 + G2 + G3, the first sentences the child punctuates (PUNCT_PICK, the same module's
         tap mode, in place of the ported G1 / G2 builders and the G3 reading pick); G4 = the reference game
         hi-02-h04-l01-s01's Page 11 (P4) picture-to-sentence question with this lesson's content (SENT_PICK); P1, P2 = the
         same page again, each with its own picture and sentences (SENT_PICK, in place of the first practice builder and
         the first evidence pick).
Removed = the ported practice pages P3, P4, P5 and P6 (the dev nav's pages 13-16; [rm-p3p6]), so P2 is the last page
         before the end screen: 13 pages.
Added  = L1, the thought-cloud letter page after P2's round gate (LETTER_STORY, [letter-fig]): the Figma frames 538:2 ->
         538:35 -> 538:39 -> 558:2 -> 610:6 played as one animated scene with the user's five sound files; 14 pages.
         [letter-idea] (2026-10-27): the chime sounds the moment the grandfather cloud has stood; on its "ummm" the cloud leaves
         and the girl is pensive (the user's third picture, no cloud), on its "aahaha" the same cloud grows in again, white, with
         the letter growing in it.
         [demo1-pinki] (2026-10-27): T2 re-pointed at the Figma frame 656:2 — the sentence "पिंकी स्कूल जा रही है" and its own
         picture (the girl in uniform walking); the layout, flow and sounds otherwise 519:32's; its two sentence clips re-made.
         [demo2-girl] (2026-10-27): T3's picture replaced by the user's (a girl in a pink dress waving), at its native size in the
         same picture box; nothing else of T3 touched.
         [g1-pinki] (2026-10-27): G1 re-pointed at the Figma frame 656:66 — the sentence "पिंकी गेंद से खेल रही थी" (its box and
         the slot moved right with it), its own picture (the girl with the ball), the first tile's face 1 px taller; otherwise
         525:354's; its sentence clip re-made.
         [g2-girl] (2026-10-27): G2's picture replaced by the user's (a girl in a pink dress with a yellow bag), at its native
         size in the same picture box; nothing else of G2 touched.
         [sent-font] (2026-10-27): G4, P1 and P2's two texts (the header's line, the pills' sentences) in the previous pages'
         face — Noto Sans Devanagari SemiBold — in place of the reference P4's Baloo 2 ExtraBold; sizes, lines, boxes as they were.
         [dun-chrome] (2026-10-27): the chrome of HI02H04_L01_S01 (hi-02-h04-l01-s01-dun.vercel.app): the cover's sky and play
         button, आगे, the bird in the title bars, the speaker chips, the phase gates and confetti, the music bed, the celebration.
         [cover-sky] (2026-10-28): the cover's sky is SEEN (the start gate transparent on the title page, as the reference's: it had
         been painting a second sunburst over the glow and the stars) and the play button's pop-in fades in from 0 (its
         opacity:1 !important, which beat the keyframe, dropped); two CSS lines in the [dun-chrome] block, nothing else.
         [band-chip] (2026-10-28): the speaker chip on the six title-bar pages T2-T4 and G1-G3 — the engine's .tut-audio chip (the
         same inline-SVG speaker as G4's header chip) shown again at the bar's bird, at G4's shoulder spot, with G4's states;
         CSS only (band_chip_css).
         [cel-vo] (2026-10-28): the celebration's line is the reference's own vo_well_done (its clip as Opus .ogg, its beak bits,
         its text) in place of vo_celebrate; the bird and the finish button were already the reference's.
         [vo-rec] (2026-10-28): the recorded voice-overs (the user's voiceovers/ folder, 75 wavs named by the VO manifest's Audio IDs)
         in their places — vo_rec.py (run before this) re-containers them, re-syncs every word-timed line from the clip's own
         words and reads the gate cue; here the card gets the new IDs and the deck's extra beats (explain / again / conclude
         lines, hint ladders, the letter narration, per-round stamp instructions, the praise lines) get their JS hooks.
         [story-pinki] (2026-10-28): the story page T0 is four beats from the frames 652:3, 652:192, 660:127, 653:381 (Pinki,
         her mother, the cat: new pictures, texts with their punctuation, the recorded takes 1 / vo_story_s1 / 2 / 3.wav as
         vo_story_b1..b4 via vo_rec.py, word-synced); same layout, module and beat animation; then आगे.
         [relisten-pinki] (2026-10-28): T0B is frame 654:567 — the title, the story's two contrast sentences each on its own
         clip (the T0 takes cut after "माँ ने कहा,", word-synced), the explanation (vo_story_r1) lighting each sentence as
         its meaning is told, the moral (4.wav) lighting the commas as it names the marks; then आगे.
         [band-title] (2026-10-28): the title bars of T2 / T3 / T4 read "विराम चिह्न का वाक्य में प्रयोग ।" (frame 656:2's line)
         and G2's reads G3's "वाक्य सुनिए और सही चिह्न लगाइए ।" — data.band_hi only; the spoken lines and all else unchanged.
         [demo-intro] (2026-10-28): T3 and T4 no longer speak their intro line "सुनो, यह वाक्य बिना रुके पढ़ा गया ।" (vo_demo2 /
         vo_demo3_intro: data.intro_audio null, the clips off the dist): the title bar comes on mount, the rest 1.3 s later.
         [tile-tap] (2026-10-28): on T2-T4 and G1-G3 the tapped option presses as a whole (base, face, mark, name), not its
         white face alone — the dmfTap animation moved from .dmf-face to .dmf-tile.on; nothing else.
         [p1-pic] (2026-10-28): P1's picture is the user's new one (two girls with the picture book), framed like P4's by
         g4_picture.py into the same file; nothing else.
         [word-hot] (2026-10-28): on T2-T4 and G1-G3 the word being read lights as on G4 — orange #E86A00 with G4's p2WordPop
         pop — in place of the light-yellow box (.dmf-sent .sfig-w.hot); timing, the slot highlight and all else unchanged.
         [sent-50] (2026-10-28): on T2 / T3 / G1 / G2 the sentence is 50px (same font) and it and the yellow slot 4px after its
         ink are centred in the bar together (data.layout.sent = SENT50 + each page's slot x); the mark, the bar and all else unchanged.
         [tap-lock] (2026-10-28): on G1-G3 and G4 / P1 / P2 only the tapped option answers (the picks' right tap no longer dims the
         other two tiles); while a FEEDBACK sound or line plays (the buzz, a hint / try-again line, hint 3, the chime) no other
         option, the hand or the chip answers (sfxBusy() + the feedback line's own Audio); a tap during the instruction or the
         idle re-read still cuts it and answers at once (this change's first build held those too: a tester's taps seemed to do
         nothing, since the instruction repeats after every 5 s of quiet); a page's pointing hand is swept at every mount.
         [tile-hit] (2026-10-28): on the pick pages a tap on a tile's mark or name lands on THAT tile — the text boxes, far wider
         than the tile, overflowed onto the next tiles and took their taps (G2 / G3 judged a tap by the wrong tile); .dmf-sym and
         .dmf-name take no pointer events (CSS only; nothing drawn changes).
         [hand-quiet] (2026-10-28): on G1-G3, once the pointing hand shows (the 3rd wrong tap) the other two tiles are dead and dim
         (.off + pointer-events:none) and nothing speaks any more — no hint 3, no idle re-read, no chip, and no praise line after
         the guided tap (the mark, the ding + confetti, 1.7 s, then the page moves on, as the sentence picks' guided tap does).
         [story-cat] (2026-10-28): T0 — as beat 1's line ends, the user's cat sound (assets/Audio/sfx_story_cat.mp3, 0.89 s) plays
         once (data.beat1_sfx, the kit player) and beat 1's picture gives G4's little pop (p2BirdPop1s, 1 s, .sfig-img.sfig-pop);
         the one-second pause and the turn to beat 2 are as before; a 🔊 replay of beat 1 does not repeat it.
         [demo-hand] (2026-10-28): T2 / T3 / T4 — the highlighted slot's ring and glow are the words' orange (#E86A00, was blue
         #386AF6), and the picks' pointing hand (showHand: .reveal-hand.dmf-hand, 96px, under the tile) appears as the right tile is
         auto-tapped and leaves as the second reading begins.
         [g4-giggle] (2026-10-28): G4 — the right tap's picture pop (the reference's p2BirdPop1s, unchanged) now comes with the
         user's giggle (assets/Audio/sfx_g4_giggle.mp3, data.tap_sfx): the reference game's G2 correct-tap effect — a fresh Audio
         at .63, faded over the last 150 ms of the 1 s hold and paused with it; the ding + confetti and all else as before.
         [p1-book] (2026-10-28): P1 the same way — the user's book-opening sound (assets/Audio/sfx_p1_book.mp3, data.tap_sfx)
         with the right tap's picture pop; the module's [g4-giggle] hook, no new code.
         [p2-pencils] (2026-10-28): P2 likewise — the user's pencils sound (assets/Audio/sfx_p2_pencils.mp3, data.tap_sfx); the
         17 s file is silent until 0.52 s, so data.tap_sfx_from = 0.51 starts it at its first shake (the hook's one new line).
         [l1-quiet] (2026-10-28): L1 (the letter page) has no music bed — the bed block's onSlide honours a slide's no_bgm flag:
         the bed fades out (0.6 s) as L1 mounts and starts again (its first-page fade-in) as L2 mounts, i.e. once the envelope's
         dive and veil are over; the page's own piano loop and sounds are as before.
         [cover-eyes] / [cover-fx] (2026-10-29): the title page's three characters get the mtcg2a04l02 game's live eyes (its
         [pencil eyes] rig on three upright faces: title_assets/cover_eyes_js.js, the geometry measured by title_eyes_measure.py
         into cover_eyes_data.json, the brows cut into title_char_*_rig.png) and the card's scene gets that game's lens flare and
         sunlit dust (cover_fx.css, cover_dust_js.js: the .sg-fx layer after the scene, the same 1096x438 box and light).
         [baloo-font] (2026-10-30): every text of the lesson's pages in Baloo 2 ExtraBold, the reference game's Page 1 T1 face —
         T0-G3 and L2 through 'Story Baloo 2' (the engine's own Baloo 2 800 file with Noto's line metrics, so no line box
         moves), G4 / P1 / P2 back on P4's own Baloo 2 (undoing [sent-font]); no word spacing (Baloo's spaces are the frames');
         the slots that sit after or between words moved with Baloo's wider ink (same gaps as before), G3's sentence 48 px.
         [textbox-shadow] (2026-10-30): T0's white text box casts the shadow of the reference story's Page 1 S01 sentence box
         (hind-dear-story.vercel.app): a 5 px navy lip + a 10 / 26 px navy glow, the same on-screen px; one CSS rule.
         [word-sync] (2026-10-30): every text read with a clip (T0's beats, T0B's sentences, T1's names / uses / examples, the first
         reading on T2-T4 / G1-G3 and the picks' re-read, L2's sentences) shows WHOLE, rising in as the reference T1's sentence does,
         and is read 0.45 s later with the reference's word light (one word at a time, dark orange + a small pop, on the clip's clock).
Idempotent: always rebuilds from the _before_reskin backup of the original files.
"""
import re, json, shutil, pathlib, sys

SCR  = pathlib.Path(__file__).resolve().parent
# usage: python -I build.py [<path to a clone of github.com/siddharthsharma-ctrl/Ek-aur-Anek>] [<path to the game's dist folder>]
REF_DIR  = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else SCR / "ref" / "Ek-aur-Anek"
REF_HTML = REF_DIR / "HI02H11_L03_S01_poem.html"
DIST = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else SCR.parent / "HI02H12_L01_S01_dist"
BACKUP = DIST.parent / "_before_reskin"

def must(pattern, text, flags=0, what=""):
    ms = list(re.finditer(pattern, text, flags))
    if len(ms) != 1:
        raise SystemExit(f"anchor '{what or pattern[:60]}' matched {len(ms)} times (need exactly 1)")
    return ms[0]

def sub1(text, pattern, repl, flags=0, what=""):
    must(pattern, text, flags, what)
    return re.sub(pattern, repl, text, count=1, flags=flags)

# ---------- 0. one-time backup of the original split bundle ----------
BACKUP.mkdir(exist_ok=True)
for f in ("index.html", "style.css", "app.js"):
    if not (BACKUP / f).exists():
        shutil.copy2(DIST / f, BACKUP / f)

ref     = REF_HTML.read_text(encoding="utf-8")
tgt_idx = (BACKUP / "index.html").read_text(encoding="utf-8")
tgt_css = (BACKUP / "style.css").read_text(encoding="utf-8")
tgt_js  = (BACKUP / "app.js").read_text(encoding="utf-8")
ocean_css = (REF_DIR / "assets" / "ocean-games.css").read_text(encoding="utf-8")

# ---------- 1. slice the reference ----------
ref_css  = must(r"<style>\n(.*?)\n</style>", ref, re.S, "ref <style>").group(1)
ref_body = must(r'<body class="is-start">\n(.*?)<script src="assets/ocean-vo-config.js"></script>', ref, re.S, "ref body").group(1)
i = ref.index('id="cardData">'); j = ref.index("<script>\n", i) + len("<script>\n"); k = ref.rindex("</script>")
ref_js = ref[j:k]
assert ref_js.lstrip().startswith("const CARD") and "boot();" in ref_js, "engine slice looks wrong"

# ---------- 2. slice the target ----------
card = json.loads(must(r'<script type="application/json" id="cardData">(.*?)</script>', tgt_idx, re.S, "tgt card").group(1))
def module(name):
    return must(r"^  %s: \{\n.*?^  \},\n" % name, tgt_js, re.S | re.M, "module " + name).group(0)
mods = [module(n) for n in ("QTYPE_RECAP", "BUILD_PUNCT", "EVIDENCE_QA", "SORT_QTYPE")]
ev_helpers = must(r"(/\* EVIDENCE comprehension helpers.*?)\n/\* ---------- 12\. SLIDE MODULES", tgt_js, re.S, "ev helpers").group(1)
mod_css = tgt_css[tgt_css.index("/* ===== EVIDENCE comprehension"):]
ported_js = (ev_helpers + "\n").replace("SwiftPAL.emit(", "GameBus.emit(")
ported_mods = "".join(mods).replace("SwiftPAL.emit(", "GameBus.emit(")

# ---------- 3. card: the reference flow uses the engine's peek-gate between rounds, not journey-map slides ----------
card["slides"] = [s for s in card["slides"] if s["type"] != "PHASE_TRANSITION"]
# [story-fig] the Figma story page opens the tutorial: start gate -> peek transition -> this -> T1. It tells the
# story in beats on one layout (new picture, new text, new narration each). [story-pinki] (2026-10-28): FOUR beats from
# the frames 652:3, 652:192, 660:127 and 653:381 — Pinki, her mother and the cat; the texts carry their punctuation, and
# beats 2 and 4 differ by one comma ("उसे रोको मत जाने दो" / "उसे रोको, मत जाने दो"). The clips are the recorded takes
# (vo_rec.py: 1.wav, vo_story_s1.wav, 2.wav, 3.wav -> vo_story_b1..b4), the per-word start times whisper's, re-synced to
# the frames' words. (Before: two beats, frames 435:5 / 476:198, the Chintu story in TTS: story_assets/vo_story_s1, s2.)
lines = {k: json.loads((SCR / "story_assets" / f"vo_story_{k}.words.json").read_text(encoding="utf-8")) for k in ("b1", "b2", "b3", "b4")}
beats = [{"image_id": img, "text_hi": lines[k]["text"], "word_times": [t[0] for t in lines[k]["word_times"]], "word_end": lines[k]["word_times"][-1][1],
          "audio": f"vo_story_{k}"} for k, img in (("b1", "img_story_pinki_cat"), ("b2", "img_story_pinki_listen"),
                                                     ("b3", "img_story_pinki_ask"), ("b4", "img_story_pinki_maa"))]
card["slides"].insert(0, {"id": "T0", "phase": "tutorial", "eis": "iconic", "type": "STORY_LISTEN",
    "prompt_hi": lines["b1"]["text"],
    "audio": {"narration": "vo_story_b1", "narration_2": "vo_story_b2", "narration_3": "vo_story_b3", "narration_4": "vo_story_b4"},
    "data": {"beats": beats}})
for b in beats:
    card["assets"]["audio"][b["audio"]] = f"assets/Audio/{b['audio']}.ogg"
    card["assets"]["audio_text"][b["audio"]] = b["text_hi"]
    card["assets"]["image"][b["image_id"]] = f"assets/Images/{b['image_id']}.webp"
# [story-fig] then "आइए वाक्य सुनें।": the intro line under the title, then the sentences. [relisten-pinki] (2026-10-28): the
# frame is 654:567 now — the title, then the story's two contrast sentences "उसे रोको, मत जाने दो।" / "उसे रोको मत, जाने दो।"
# each on its own recorded clip (the T0 takes without their "माँ ने कहा,": vo_story_c1 / c2, cut by vo_rec.py) and read word by
# word; then the explanation (vo_story_r1, the recording) lighting each sentence on its yellow as its meaning is told (cues =
# the clip's "पहले" and "जबकि", read by vo_rec.py); then the moral (vo_story_moral = 4.wav) lighting the two commas orange as it
# names the marks (cue = its "विराम"); then आगे. (Before: the Chintu story re-read in one block, frame 488:190, TTS vo_story_r1.)
for k in ("r0", "r1", "c1", "c2"):
    lines[k] = json.loads((SCR / "story_assets" / f"vo_story_{k}.words.json").read_text(encoding="utf-8"))
_vr0 = json.loads((SCR / "vo_rec" / "derived.json").read_text(encoding="utf-8"))["cues"]
card["slides"].insert(1, {"id": "T0B", "phase": "tutorial", "eis": "iconic", "type": "STORY_RELISTEN",
    "prompt_hi": "आइए वाक्य सुनें।",
    "audio": {"intro": "vo_story_r0", "narration": "vo_story_c1", "narration_2": "vo_story_c2", "explain": "vo_story_r1", "moral": "vo_story_moral"},
    "data": {"title_hi": "आइए वाक्य सुनें।", "intro_audio": "vo_story_r0",
             "lines": [{"text_hi": lines[k]["text"], "word_times": [t[0] for t in lines[k]["word_times"]], "word_end": lines[k]["word_times"][-1][1], "audio": f"vo_story_{k}"} for k in ("c1", "c2")],
             "explain_audio": "vo_story_r1", "explain_cues": _vr0["explain_s"], "moral_audio": "vo_story_moral", "moral_cue": _vr0["moral_s"],
             "text_hi": lines["c1"]["text"] + "\n" + lines["c2"]["text"]}})
for k in ("r0", "r1"):
    card["assets"]["audio"][f"vo_story_{k}"] = f"assets/Audio/vo_story_{k}.ogg"
    card["assets"]["audio_text"][f"vo_story_{k}"] = lines[k]["text"].replace("\n", " ")
# [recap-fig] T1 = the Figma three-marks recap "ये हैं तीन विराम चिह्न" (frame 508:2), in place of the ported QTYPE_RECAP
# cards: the title on the intro line, then for each mark its name, when it is used and an example, each read by its own
# clip with the story pages' word-by-word reveal. Clips + timings come from recap_assets/ (made by recap_vo.py; the
# example lines SAY "उदाहरण- ..." and SHOW the sentence, so their word_times cover the shown words).
RECAP_KEYS = ["intro"] + [f"{m}_{p}" for m in ("purn", "alp", "prashn") for p in ("name", "when", "eg")]
rl = {k: json.loads((SCR / "recap_assets" / f"vo_recap_{k}.words.json").read_text(encoding="utf-8")) for k in RECAP_KEYS}
i_t1 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "T1")
assert card["slides"][i_t1]["type"] == "QTYPE_RECAP", "T1 is not the three-marks recap"
part = lambda k: {"text_hi": rl[k]["shown"], "audio": f"vo_recap_{k}", "word_times": [t[0] for t in rl[k]["word_times"]], "word_end": rl[k]["word_times"][-1][1]}
card["slides"][i_t1] = {"id": "T1", "phase": "tutorial", "eis": "symbolic", "type": "MARKS_RECAP",
    "prompt_hi": rl["intro"]["shown"], "audio": {"prompt": "vo_recap_intro"},
    "data": {"title_hi": rl["intro"]["shown"], "intro_audio": "vo_recap_intro",
             "rows": [{"mark": mark, "name": part(f"{m}_name"), "when": part(f"{m}_when"), "example": part(f"{m}_eg")}
                      for m, mark in (("purn", "।"), ("alp", ","), ("prashn", "?"))]}}
for k in RECAP_KEYS:
    card["assets"]["audio"][f"vo_recap_{k}"] = f"assets/Audio/vo_recap_{k}.ogg"
    card["assets"]["audio_text"][f"vo_recap_{k}"] = rl[k]["text"]
# [demo-fig] T2 = the Figma "G3 guided story question" frame 519:32, the first run-on sentence demo, in place of the ported
# BUILD_PUNCT auto demo: the title bar on the intro line; the picture, the sentence bar (with its empty slot) and the three
# mark tiles; the sentence read without a pause, word by word; the slot blinks; "पूर्ण विराम" taps its tile for the child
# and dims the others; the mark lands in the slot; the sentence is read again with the mark named, words and mark
# highlighted as they are read; then the slot's box goes and the page advances by itself (no आगे). Clips + timings from
# demo1_assets/ (recap_vo.py demo1).
# [demo1-pinki] (asked 2026-10-27): the frame is now 656:2 — 519:32 to the pixel except its sentence, "पिंकी स्कूल जा रही है" (its
# ink 461..944 on the render; the browser shapes it the same width within 2 px but every word sat 3.5 px right of the render's in
# the old box, so the frame's text box is 3.5 px further left: data.layout.sent_x = 96.5 in the bar, the same 479 width), and its picture,
# the girl in uniform walking (its ink 229..308 x 214..344 on the render; cut from the user's 1280x720 render — the only source to
# hand — at that box plus a 1 px white margin on the left, right and bottom: data.layout.img = [228, 214, 82, 132], frame px, in
# place of 519:32's "image 228" box 227,221 80.052x120). The title line, the tiles, the slot and the flow are untouched; the
# two sentence clips (sent, full) were re-made by recap_vo.py demo1 with the new name, the intro and "पूर्ण विराम" kept.
DEMO_KEYS = ["intro", "sent", "purn", "full"]
DEMO_BAND = "विराम चिह्न का वाक्य में प्रयोग ।"   # [band-title] (2026-10-28) the title bar's line on T2 / T3 / T4 (frame 656:2's), in place of the intro line's shown text; the intro clip sounds as before
SENT50 = {"x": 0, "y": 18, "w": 719 - 63, "size": 50, "lh": 110, "ws": 0}   # [sent-50] (2026-10-28) T2 / T3 / G1 / G2: the sentence at 50px (the 50px pages' -3px word spacing) in the same line box (y 18, 110px) as the 64px one; its text box is the 719px bar LESS the slot's column (a 4px gap + the 59px slot), so the centred sentence and the slot 4px after it are centred on the bar TOGETHER (asked twice: first "the sentence centred", then "both together"); each page's slot x = its ink's right edge + 4 (frame px, measured in Chrome)
dl = {k: json.loads((SCR / "demo1_assets" / f"vo_demo1_{k}.words.json").read_text(encoding="utf-8")) for k in DEMO_KEYS}
i_t2 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "T2")
assert card["slides"][i_t2]["type"] == "BUILD_PUNCT" and card["slides"][i_t2]["data"].get("auto"), "T2 is not the first auto demo"
dpart = lambda k: {"text_hi": dl[k]["shown"], "audio": f"vo_demo1_{k}", "word_times": [t[0] for t in dl[k]["word_times"]], "word_end": dl[k]["word_times"][-1][1]}
card["slides"][i_t2] = {"id": "T2", "phase": "tutorial", "eis": "enactive", "type": "PUNCT_DEMO",
    "prompt_hi": dl["intro"]["shown"], "audio": {"prompt": "vo_demo1_intro"},
    "data": {"band_hi": DEMO_BAND, "intro_audio": "vo_demo1_intro", "image_id": "img_demo1_girl",
             "sentence": dpart("sent"), "mark": "।", "mark_audio": "vo_demo1_purn", "full": dpart("full"),
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500, "hold_ms": 1500, "layout": {"img": [228, 214, 82, 132], "sent": SENT50, "slot": [528.3, 20]}},   # [baloo-font] slot 521 -> 528.3: "है" ends 7.3 px further right in Baloo 2;   # [demo1-pinki] 656:2's picture box; [sent-50] the sentence at 50px centred in the bar (was 656:2's 64px box at 96.5), the slot 4px after its ink (was 583)
    "signals": {"on_complete": []}}
for k in DEMO_KEYS:
    card["assets"]["audio"][f"vo_demo1_{k}"] = f"assets/Audio/vo_demo1_{k}.ogg"
    card["assets"]["audio_text"][f"vo_demo1_{k}"] = dl[k]["text"]
card["assets"]["image"]["img_demo1_girl"] = "assets/Images/img_demo1_girl.webp"
card["_emoji_fallback"]["img_demo1_girl"] = "✏️"
# [demo-fig] T3 = the Figma frame 521:288 "5 T3", the second run-on sentence demo, in place of the ported BUILD_PUNCT auto
# demo ("तुम्हारा क्या नाम है"): T2's layout and flow with its own sentence ("तुम्हारा नाम क्या है", whose text box sits at
# 120 in the bar, not 100), its own picture ("image 229", a boy, 130x128 at 204,215) and its own mark ("?": the
# प्रश्नवाचक चिह्न tile is the one tapped). The band and the tiles are T2's to the pixel. data.layout carries the two
# differing boxes (frame px); without it the module keeps 519:32's (the CSS). Clips + timings from demo2_assets/
# (recap_vo.py demo2).
# [demo2-girl] (asked 2026-10-27): the picture is the user's own PNG (a girl in a pink dress waving, 90x135 with transparency,
# stored lossless as img_demo2_girl.webp) in place of the frame's "image 229" (the boy, img_demo2_boy — its file stays in the
# dist, unused): at its native size, its ink (84x130) centred in the picture box's interior -> data.layout.img = [223, 214, 90,
# 135] frame px (the old box was 204,215 130x128). The render demo2_figma_render_1280x720.png carries the girl in the boy's place
# (the 521:288 render kept as _v1_2026-10-25). Text, clips, flow untouched.
DEMO2_KEYS = ["intro", "sent", "prashn", "full"]
DEMO2_CLIPS = [k for k in DEMO2_KEYS if k != "intro"]   # [demo-intro] (2026-10-28) the intro line "सुनो, यह वाक्य बिना रुके पढ़ा गया ।" is off T3: not played, not in the dist (its source stays in demo2_assets/)
dl2 = {k: json.loads((SCR / "demo2_assets" / f"vo_demo2_{k}.words.json").read_text(encoding="utf-8")) for k in DEMO2_KEYS}
i_t3 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "T3")
_t3 = card["slides"][i_t3]
assert _t3["type"] == "BUILD_PUNCT" and _t3["data"].get("auto") and [m["mark"] for m in _t3["data"]["marks"]] == ["?"], "T3 is not the question-mark auto demo"
dpart2 = lambda k: {"text_hi": dl2[k]["shown"], "audio": f"vo_demo2_{k}", "word_times": [t[0] for t in dl2[k]["word_times"]], "word_end": dl2[k]["word_times"][-1][1]}
card["slides"][i_t3] = {"id": "T3", "phase": "tutorial", "eis": "enactive", "type": "PUNCT_DEMO",
    "prompt_hi": DEMO_BAND, "audio": {},   # [demo-intro] no intro line (was vo_demo2_intro); the engine's prompt text = the bar's line
    "data": {"band_hi": DEMO_BAND, "intro_audio": None, "image_id": "img_demo2_girl",   # [demo2-girl]
             "sentence": dpart2("sent"), "mark": "?", "mark_audio": "vo_demo2_prashn", "full": dpart2("full"),
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500, "hold_ms": 1500, "layout": {"sent": SENT50, "slot": [502.6, 20], "img": [223, 214, 90, 135]}},   # [baloo-font] slot 497 -> 502.6 ("है" +5.6 px);   # [demo2-girl] the picture at its native size, centred in the box; [sent-50] the sentence at 50px centred (was the 64px box at 120), the slot 4px after its ink (was 583)
    "signals": {"on_complete": []}}
for k in DEMO2_CLIPS:   # [demo-intro] without the intro
    card["assets"]["audio"][f"vo_demo2_{k}"] = f"assets/Audio/vo_demo2_{k}.ogg"
    card["assets"]["audio_text"][f"vo_demo2_{k}"] = dl2[k]["text"]
card["assets"]["image"]["img_demo2_girl"] = "assets/Images/img_demo2_girl.webp"   # [demo2-girl]
card["_emoji_fallback"]["img_demo2_girl"] = "✏️"
# [demo-fig] T4 = the Figma frame 523:320 "6 T4", the third run-on sentence demo, in place of the ported BUILD_PUNCT auto
# demo ("मेरे पास आम केला और सेब हैं"): T2's flow with अल्प विराम as the tapped tile and a sentence that needs TWO commas.
# The frame moves the picture box to 144 (its "image 230", fruit, 144x96 at 144,229, drawn over the box) and widens the
# sentence bar to 312 824; the sentence 523:332 "मेरे पास आम    केला    सेब और संतरा है ।" is 50px in an 893-wide box
# at -34,33 of the bar, with a run of four spaces after "आम" and after "केला" where the two 33x38 slots 523:333 / 524:352
# sit (at 286,76 and 417,76 of the bar); the sentence already ends with its danda. Both slots blink together and both
# receive the comma (left, then right); the second reading names each comma where it sits and lights that slot.
# data.slots / sentence.gaps / full.targets / layout.{pic_x, bar, sent} carry all of it; T2 / T3 have none of these
# keys, so their pages are unchanged. Clips + timings from demo3_assets/ (recap_vo.py demo3).
DEMO3_KEYS = ["intro", "sent", "alp", "full"]
DEMO3_CLIPS = [k for k in DEMO3_KEYS if k != "intro"]   # [demo-intro] (2026-10-28) the same intro line is off T4 too (vo_demo3_intro: not played, not in the dist)
dl3 = {k: json.loads((SCR / "demo3_assets" / f"vo_demo3_{k}.words.json").read_text(encoding="utf-8")) for k in DEMO3_KEYS}
i_t4 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "T4")
_t4 = card["slides"][i_t4]
assert _t4["type"] == "BUILD_PUNCT" and _t4["data"].get("auto") and "," in [m["mark"] for m in _t4["data"]["marks"]], "T4 is not the comma auto demo"
dpart3 = lambda k: {"text_hi": dl3[k]["shown"], "audio": f"vo_demo3_{k}", "word_times": [t[0] for t in dl3[k]["word_times"]], "word_end": dl3[k]["word_times"][-1][1]}
_full3 = dpart3("full")
# the second reading's tokens: मेरे पास आम, अल्पविराम, केला, अल्पविराम, सेब और संतरा है। -> sentence words 0-2, slot 0, word 3,
# slot 1, words 4-7 (the sentence's spans: मेरे पास आम केला सेब और संतरा है ।)
_full3["targets"] = ["w0", "w1", "w2", "s0", "w3", "s1", "w4", "w5", "w6", "w7"]
assert len(_full3["targets"]) == len(_full3["word_times"]), "T4: the second reading's tokens and its targets differ in number"
# measured against the frame's render (word by word): Baloo Bhai 2's spaces are 3px narrower than Noto's at 50px
# (layout.sent.ws), its line box puts the glyphs where an 84px one does here, and the space before the closing danda
# ("है ।") is 4.5px narrower still in the render — sentence.nudge pulls the danda (span 8) in by that much; with it
# every word's ink is within 1px of the render
_sent3 = dict(dpart3("sent"), gaps=[2, 3], gap_spaces=4, nudge={"3": 3.4, "4": 2.1})   # [baloo-font] the gaps' old ink widths in Baloo 2; no danda nudge (was {"8": -4.5})
assert _sent3["text_hi"].split()[2:4] == ["आम", "केला"], "T4: the slots no longer follow आम / केला"
# the slots' dashes, measured on the frame's render: two dashes centred on each side, [margin, dash, gap, dash, margin]
_slot = lambda x: {"x": x, "y": 76, "w": 33, "h": 38, "dash_h": [4.5, 9.5, 5, 9.5, 4.5], "dash_v": [5, 10, 8, 10, 5]}
card["slides"][i_t4] = {"id": "T4", "phase": "tutorial", "eis": "enactive", "type": "PUNCT_DEMO",
    "prompt_hi": DEMO_BAND, "audio": {},   # [demo-intro] no intro line (was vo_demo3_intro)
    "data": {"band_hi": DEMO_BAND, "intro_audio": None, "image_id": "img_demo3_fruits",
             "sentence": _sent3, "mark": ",", "mark_audio": "vo_demo3_alp", "mark_size": 50, "mark_stagger_ms": 300,
             "full": _full3, "slots": [_slot(280.7), _slot(420.1)],   # [baloo-font] 286 / 417 -> on the Baloo gaps
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500, "hold_ms": 1500,
             "layout": {"pic_x": 144, "img": [144, 229, 144, 96], "bar": [312, 824],
                        "sent": {"x": -31.7, "y": 33, "w": 893, "size": 50, "lh": 84, "ws": 0}}},   # [baloo-font] x -34 -> -31.7: the sentence's old centre
    "signals": {"on_complete": []}}
for k in DEMO3_CLIPS:   # [demo-intro] without the intro
    card["assets"]["audio"][f"vo_demo3_{k}"] = f"assets/Audio/vo_demo3_{k}.ogg"
    card["assets"]["audio_text"][f"vo_demo3_{k}"] = dl3[k]["text"]
card["assets"]["image"]["img_demo3_fruits"] = "assets/Images/img_demo3_fruits.webp"
card["_emoji_fallback"]["img_demo3_fruits"] = "✏️"
# [pick-fig] G1 = the Figma frame 525:354 "7 G1", the first sentence the CHILD punctuates, in place of the ported BUILD_PUNCT
# builder ("राजू खेल रहा था उसकी गेंद खो गई", two dandas): T4's title bar with its own line "वाक्य सुनिए और सही चिह्न लगाइए ।"
# (the bar appears as it starts to sound), then T3's picture, sentence bar (with its empty slot) and tiles coming in, the
# sentence "राजू गेंद से खेल रहा था" read without a pause, word by word, and the slot's three slow blinks — and then the
# tiles are the child's (type PUNCT_PICK = the PUNCT_DEMO module's tap mode): a wrong tile wiggles; the right one (पूर्ण
# विराम) is pressed, its mark lands in the slot as its name sounds, and the page moves on to G2 by itself. The frame keeps
# 519:32's boxes except the picture ("image 231", a boy with a football, 124x124 at 207,219), the sentence's text box (522
# wide at 60,18 in the bar) and two tiles (the first base 1px taller, the middle tile 4px wider) — data.layout. The name
# said on the right tap is T2's "पूर्ण विराम" clip (the same voice). Clips + timings from g1_assets/ (recap_vo.py g1).
# [g1-pinki] (asked 2026-10-27): the frame is now 656:66 — 525:354 to the pixel (title bar, tiles' bases, the third tile) except:
# the sentence "पिंकी गेंद से खेल रही थी" (its ink 416..969 on the render, 553 wide: WIDER than the old 522 box — and a line that
# overflows its box is start-aligned, not centred, so the box is now 560 wide, centred where the render's ink is: x 47.5 in the
# bar, centre 692.5), the slot 29 px further right (977..1035 on the render = x 612 in
# the bar: data.layout.slot), the picture — the girl with the ball (ink 208..330 x 214..343; cut from the user's 1280x720 render
# at that box plus a 1 px white margin left / right / bottom: data.layout.img = [207, 214, 125, 131], frame px, in place of
# "image 231"'s 207,219 124x124; img_g1_boy_ball's file stays in the dist, unused) — and the first tile's white face, whose top
# edge is 1 px higher (444; its bottom and sides as before). The sentence clip (sent) re-made by recap_vo.py g1 with the new
# words (6 word times); the instruction clip and the name on the right tap (vo_demo1_purn) untouched.
G1_KEYS = ["intro", "sent"]
gl = {k: json.loads((SCR / "g1_assets" / f"vo_g1_{k}.words.json").read_text(encoding="utf-8")) for k in G1_KEYS}
i_g1 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "G1")
_g1 = card["slides"][i_g1]
assert _g1["type"] == "BUILD_PUNCT" and _g1["phase"] == "guided" and not _g1["data"].get("auto"), "G1 is not the first guided builder"
card["slides"][i_g1] = {"id": "G1", "phase": "guided", "eis": "enactive", "type": "PUNCT_PICK",
    "prompt_hi": gl["intro"]["shown"], "audio": {"prompt": "vo_g1_intro"},
    "data": {"band_hi": gl["intro"]["shown"], "intro_audio": "vo_g1_intro", "image_id": "img_g1_girl_ball",   # [g1-pinki]
             "sentence": {"text_hi": gl["sent"]["shown"], "audio": "vo_g1_sent", "word_times": [t[0] for t in gl["sent"]["word_times"]], "word_end": gl["sent"]["word_times"][-1][1]},
             "mark": "।", "mark_audio": "vo_demo1_purn",
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500,
             "layout": {"img": [207, 214, 125, 131], "sent": SENT50, "slot": [553.6, 20],   # [baloo-font] slot 548 -> 553.6 ("थी" +5.6 px);   # [g1-pinki] 656:66's places; [sent-50] the sentence at 50px centred in the bar (was 656:66's 64px box 560 wide at 47.5, ws -4), the slot 4px after its ink (was 612)
                        "tiles": [{"base": [197, 442, 227, 170], "face": [199, 444, 223, 162]},
                                  {"base": [525, 443, 231, 169], "face": [527, 445, 227, 161]}, None]}},
    "signals": {"on_complete": ["punct_build_done"]}}
for k in G1_KEYS:
    card["assets"]["audio"][f"vo_g1_{k}"] = f"assets/Audio/vo_g1_{k}.ogg"
    card["assets"]["audio_text"][f"vo_g1_{k}"] = gl[k]["text"]
card["assets"]["image"]["img_g1_girl_ball"] = "assets/Images/img_g1_girl_ball.webp"   # [g1-pinki]
card["_emoji_fallback"]["img_g1_girl_ball"] = "✏️"
# [pick-fig] G2 = the Figma frame 600:197 "8 G2", G1's page and flow for "तुम कहाँ जा रहे हो" (the ported builder had the same
# sentence and mark): the प्रश्नवाचक चिह्न tile is the right one. The frame's title bar is T4's to the pixel — its text too,
# "सुनो यह वाक्य बिना रुके पढ़ा गया ।" — while the line it plays is G1's instruction "वाक्य सुनिए और सही चिह्न लगाइए ।" (both as
# asked; [band-title] 2026-10-28: the bar's text is G3's — the instruction line — since, as asked); the tiles are T3's (no G1 tweaks), the sentence box is T3's (479 wide at 120), the picture "image 239" (a boy with
# a school bag, 102x136 at 218,213) is drawn over its box, and the empty slot sits at 573,20 in the bar (T3's at 583) —
# data.layout.slot. Its sentence clip + timings from g2_assets/ (recap_vo.py g2); the instruction is vo_g1_intro and the name
# on the right tap T3's vo_demo2_prashn (the same voice).
# [g2-girl] (asked 2026-10-27): the picture is the user's own PNG (a girl in a pink dress with a yellow bag, 88x132 with
# transparency, stored lossless as img_g2_girl_bag.webp) in place of the frame's boy with the bag (img_g2_boy_bag — its file stays
# in the dist, unused): at its native size, its ink (84x127) centred in the picture box's interior -> data.layout.img = [223, 216,
# 88, 132] frame px (the old box was 218,213 102x136). The render g2_figma_render_1280x720.png carries the girl in the boy's place
# (the 600:197 render kept as _v1_2026-10-25). Text, clips, flow untouched.
gl2 = json.loads((SCR / "g2_assets" / "vo_g2_sent.words.json").read_text(encoding="utf-8"))
i_g2 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "G2")
_g2 = card["slides"][i_g2]
assert _g2["type"] == "BUILD_PUNCT" and _g2["phase"] == "guided" and [m["mark"] for m in _g2["data"]["marks"]] == ["?"], "G2 is not the question-mark builder"
assert " ".join(_g2["data"]["words"]) == gl2["shown"], "G2's sentence is not the frame's"
card["slides"][i_g2] = {"id": "G2", "phase": "guided", "eis": "enactive", "type": "PUNCT_PICK",
    "prompt_hi": gl["intro"]["shown"], "audio": {"prompt": "vo_g1_intro"},
    "data": {"band_hi": gl["intro"]["shown"], "intro_audio": "vo_g1_intro", "image_id": "img_g2_girl_bag",   # [g2-girl]; [band-title] the bar's text is G3's (the instruction line)
             "sentence": {"text_hi": gl2["shown"], "audio": "vo_g2_sent", "word_times": [t[0] for t in gl2["word_times"]], "word_end": gl2["word_times"][-1][1]},
             "mark": "?", "mark_audio": "vo_demo2_prashn",
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500,
             "layout": {"sent": SENT50, "img": [223, 216, 88, 132], "slot": [498, 20]}},   # [baloo-font] slot 496 -> 498 ("हो" +2 px);   # [g2-girl] the picture at its native size, centred in the box; [sent-50] the sentence at 50px centred (was the 64px box at 120), the slot 4px after its ink (was 573)
    "signals": {"on_complete": ["punct_build_done"]}}
card["assets"]["audio"]["vo_g2_sent"] = "assets/Audio/vo_g2_sent.ogg"
card["assets"]["audio_text"]["vo_g2_sent"] = gl2["text"]
card["assets"]["image"]["img_g2_girl_bag"] = "assets/Images/img_g2_girl_bag.webp"   # [g2-girl]
card["_emoji_fallback"]["img_g2_girl_bag"] = "✏️"
# [pick-fig] G3 = the Figma frame 528:424 "9 G3", G1's page and flow for "बाग में गुलाब, गेंदा और चमेली के फूल हैं ।" in place of
# the ported EVIDENCE_QA pick ("आज सोमवार है कल मंगलवार होगा", choose the right reading): the अल्प विराम tile is the right one.
# The title bar is G1's to the pixel (its text is the instruction it plays); the tiles are T3's / T4's; the middle row is laid
# out like T4's: the picture box at 144 with "image 233" (flowers, 140x140 at 146,211, drawn over the box), the sentence bar
# 312 824, the sentence 528:437 50px in an 893-wide centred box at -28,33 of the bar with a run of FOUR spaces after "गुलाब"
# where the one 33x38 slot 528:422 sits (278,70 in the bar; pixel-identical to T4's first slot, so T4's dash runs), the
# sentence already ending with its danda. Its sentence clip + timings from g3_assets/ (recap_vo.py g3); the instruction is
# vo_g1_intro and the name on the right tap T4's vo_demo3_alp (the same voice).
gl3 = json.loads((SCR / "g3_assets" / "vo_g3_sent.words.json").read_text(encoding="utf-8"))
i_g3 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "G3")
assert card["slides"][i_g3]["type"] == "EVIDENCE_QA" and card["slides"][i_g3]["phase"] == "guided", "G3 is not the guided reading pick"
assert gl3["shown"].split()[2:4] == ["गुलाब", "गेंदा"], "G3: the slot no longer follows गुलाब"
card["slides"][i_g3] = {"id": "G3", "phase": "guided", "eis": "enactive", "type": "PUNCT_PICK",
    "prompt_hi": gl["intro"]["shown"], "audio": {"prompt": "vo_g1_intro"},
    "data": {"band_hi": gl["intro"]["shown"], "intro_audio": "vo_g1_intro", "image_id": "img_g3_flowers",
             # the space before the closing danda ("हैं ।") is 4.5px narrower in the render, as on T4: measured word by word,
             # every word 2-3px left of the render and the danda 4.5px right of the rest without the nudge
             "sentence": {"text_hi": gl3["shown"], "audio": "vo_g3_sent", "word_times": [t[0] for t in gl3["word_times"]], "word_end": gl3["word_times"][-1][1],
                          "gaps": [2], "gap_spaces": 4, "nudge": {"3": 4.1}},   # [baloo-font] the gap's old ink width (37.1 px) in Baloo 2 at 48 px: गेंदा out 4.1 px; no danda nudge (was {"9": -4.5})   # [baloo-font] the gap's old ink width in Baloo 2; no danda nudge (was {"9": -4.5})
             "mark": ",", "mark_audio": "vo_demo3_alp", "mark_size": 48,
             "slots": [{"x": 279.3, "y": 70, "w": 33, "h": 38, "dash_h": [4.5, 9.5, 5, 9.5, 4.5], "dash_v": [5, 10, 8, 10, 5]}],
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500,
             "layout": {"pic_x": 144, "img": [146, 211, 140, 140], "bar": [312, 824],
                        "sent": {"x": -26.2, "y": 33, "w": 893, "size": 48, "lh": 84, "ws": 0}}},   # [baloo-font] 50 -> 48 px (and the stamped comma, mark_size): at 50 Baloo 2 ExtraBold's sentence ran to 16 px from the bar's end, at 48 it is as wide as the Noto one was (754 px); x -28 -> -26.2 keeps its old centre; the slot 278 -> 279.3, 1 px after गुलाब as before
    "signals": {"on_complete": ["punct_build_done"]}}
card["assets"]["audio"]["vo_g3_sent"] = "assets/Audio/vo_g3_sent.ogg"
card["assets"]["audio_text"]["vo_g3_sent"] = gl3["text"]
card["assets"]["image"]["img_g3_flowers"] = "assets/Images/img_g3_flowers.webp"
card["_emoji_fallback"]["img_g3_flowers"] = "✏️"
# [sent-fig] G4 = the reference game's Page 11 (P4 of https://hi-02-h04-l01-s01-dun.vercel.app/, a picture-to-sentence question):
# its layout, elements and flow with this lesson's picture (the girl flying a kite, framed like P4's by g4_picture.py), title
# "सही विराम चिह्न वाला वाक्य चुनिए ।" and three sentences that differ only in where the danda sits — type SENT_PICK, in place of the
# ported BUILD_PUNCT builder ("बाग़ में गुलाब गेंदा और चमेली खिले हैं"). Clips + timings from g4_assets/ (recap_vo.py g4).
G4_KEYS = ["prompt", "try", "o1", "o2", "o3"]
gl4 = {k: json.loads((SCR / "g4_assets" / f"vo_g4_{k}.words.json").read_text(encoding="utf-8")) for k in G4_KEYS}
i_g4 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "G4")
assert card["slides"][i_g4]["type"] == "BUILD_PUNCT" and card["slides"][i_g4]["phase"] == "guided", "G4 is not the guided builder"
_punct = lambda t: re.fullmatch(r"[।॥,.!?]+", t) is not None
def pill_times(w):
    """the reference's word-sync table for a pill: each shown token's start in its clip, then the last one's end. A lone danda
    lights during the pause it makes (from the end of the word before it); a closing one for a moment after the last word."""
    toks, wt = w["shown"].split(), w["word_times"]
    starts = [wt[k - 1][1] if (_punct(t) and k) else wt[k][0] for k, t in enumerate(toks)]
    return [round(x, 3) for x in starts] + [round(wt[-1][1] + (0.35 if _punct(toks[-1]) else 0), 3)]
card["slides"][i_g4] = {"id": "G4", "phase": "guided", "eis": "symbolic", "type": "SENT_PICK",
    "prompt_hi": gl4["prompt"]["shown"], "audio": {"prompt": "vo_g4_prompt", "try_again": "vo_g4_try"},
    "data": {"recall_image_id": "img_g4_kite_gry", "signal_name": "evidence_qa_first_try",
             "options": [dict({"label_hi": gl4[k]["shown"], "audio": f"vo_g4_{k}", "word_times": pill_times(gl4[k])}, **({"correct": True} if k == "o1" else {}))
                         for k in ("o1", "o2", "o3")]},
    "signals": {"on_complete": ["evidence_qa_first_try"]}}
assert [o["label_hi"] for o in card["slides"][i_g4]["data"]["options"]] == ["लड़की पतंग उड़ा रही है ।", "लड़की । पतंग उड़ा रही है", "लड़की पतंग उड़ा । रही है"]
for k in G4_KEYS:
    card["assets"]["audio"][f"vo_g4_{k}"] = f"assets/Audio/vo_g4_{k}.ogg"
    card["assets"]["audio_text"][f"vo_g4_{k}"] = gl4[k]["text"]
card["assets"]["image"]["img_g4_kite_gry"] = "assets/Images/img_g4_kite_gry.webp"
card["_emoji_fallback"]["img_g4_kite_gry"] = "✏️"
# [sent-fig] P1, P2 = the same reference P4 page again (SENT_PICK), each with its own picture (framed like P4's by g4_picture.py)
# and three sentences, under G4's title + instruction ("सही विराम चिह्न वाला वाक्य चुनिए ।": vo_g4_prompt, and G4's try-again
# line). Each stays the practice page it replaces (phase, eis) and still counts in the mastery score (data.mastery, as the
# ported page did). Clips + timings from <page>_assets/ (recap_vo.py <page>).
SENT_OPT_KEYS = ["o1", "o2", "o3"]
def practice_pick(sid, page, image_id, was, labels, right):
    lines = {k: json.loads((SCR / f"{page}_assets" / f"vo_{page}_{k}.words.json").read_text(encoding="utf-8")) for k in SENT_OPT_KEYS}
    i = next(i for i, s in enumerate(card["slides"]) if s["id"] == sid)
    old = card["slides"][i]
    assert old["type"] == was and old["phase"] == "practice" and old["data"].get("mastery") is True, f"{sid} is not the ported {was} practice page"
    card["slides"][i] = {"id": sid, "phase": "practice", "eis": old["eis"], "type": "SENT_PICK",
        "prompt_hi": gl4["prompt"]["shown"], "audio": {"prompt": "vo_g4_prompt", "try_again": "vo_g4_try"},
        "data": {"recall_image_id": image_id, "signal_name": "evidence_qa_first_try", "mastery": True,
                 "options": [dict({"label_hi": lines[k]["shown"], "audio": f"vo_{page}_{k}", "word_times": pill_times(lines[k])}, **({"correct": True} if k == right else {}))
                             for k in SENT_OPT_KEYS]},
        "signals": {"on_complete": ["evidence_qa_first_try"]}}
    assert [o["label_hi"] for o in card["slides"][i]["data"]["options"]] == labels, f"{sid}'s sentences are not the asked ones"
    for k in SENT_OPT_KEYS:
        card["assets"]["audio"][f"vo_{page}_{k}"] = f"assets/Audio/vo_{page}_{k}.ogg"
        card["assets"]["audio_text"][f"vo_{page}_{k}"] = lines[k]["text"]
    card["assets"]["image"][image_id] = f"assets/Images/{image_id}.webp"
    card["_emoji_fallback"][image_id] = "✏️"
# P1: two boys and a picture book ([p1-pic] 2026-10-28: now the user's picture of two girls with the picture book, framed the same
# way by g4_picture.py into the same img_p1_book_gry.webp; the old source and picture kept as *_v1_2026-10-25); the sentences differ
# only in where the question mark sits — in place of the ported
# BUILD_PUNCT builder ("क्या तुमने खाना खाया"). Still the first practice page (G4's round gate before it).
practice_pick("P1", "p1", "img_p1_book_gry", "BUILD_PUNCT",
              ["क्या यह आपकी किताब है?", "क्या? यह आपकी किताब है", "क्या यह आपकी? किताब है"], right="o1")
# P2: a girl with coloured pencils; a danda after each colour, no mark, or a comma after each (the right one, listed last) —
# in place of the ported EVIDENCE_QA pick ("राम खाना खाकर सोया"). Too long for P4's pill on one line: SENT_PICK sets them on two.
practice_pick("P2", "p2", "img_p2_pencils_gry", "EVIDENCE_QA",
              ["मेरे पास लाल । नीली । हरी और पीली पेंसिल हैं ।", "मेरे पास लाल नीली हरी और पीली पेंसिल हैं ।", "मेरे पास लाल, नीली, हरी और पीली पेंसिल हैं ।"], right="o3")
# [gate-p2] the round-3 gate ("अब आपकी बारी!": the peeking Swiftie, the title revealed as vo_pt_practice sounds) follows P2, not
# the guided -> practice boundary (G4 -> P1) where the engine would open it: G4, P1 and P2 play as one run of the same page and
# the gate opens before the first builder page, P3. The engine patch below reads this key. Since [rm-p3p6] below dropped
# P3-P6, the page after P2 is the CELEBRATION end screen, where the engine opens no round gate; [gate-cel] lets this one gate
# open there (asked 2026-10-26: after P2, the bird with the pink "अब आपकी बारी!" and its synced animation, then the end screen).
card["round3_gate_after"] = "P2"
# [rm-p3p6] Pages 13-16 removed (asked 2026-10-25, built 2026-10-26): the ported practice pages P3 (EVIDENCE_QA), P4 and P5
# (BUILD_PUNCT) and P6 (SORT_WORDS) are dropped from the card, so P2 is the last page before the CELEBRATION end screen and the
# game is 13 pages: T0, T0B, T1, T2, T3, T4, G1, G2, G3, G4, P1, P2, CEL. Their clips and pictures stay in assets/ and in the
# card's asset table, unused, and their modules stay in the engine, unused. `qtype_sort_done` fired only on P6, so it leaves
# signals_expected (the end screen's validator would otherwise report it missing); punct_build_done still fires on G1-G3 and
# evidence_qa_first_try on G4 / P1 / P2. The mastery score now covers P1 and P2, the only data.mastery pages left.
RM_PAGES = ["P3", "P4", "P5", "P6"]
_rm = [s for s in card["slides"] if s["id"] in RM_PAGES]
assert [s["id"] for s in _rm] == RM_PAGES and [s["type"] for s in _rm] == ["EVIDENCE_QA", "BUILD_PUNCT", "BUILD_PUNCT", "SORT_WORDS"], "pages 13-16 are not the ported P3-P6"
assert all(s["phase"] == "practice" and s["data"].get("mastery") is True for s in _rm)
card["slides"] = [s for s in card["slides"] if s["id"] not in RM_PAGES]
assert [s["id"] for s in card["slides"]] == ["T0", "T0B", "T1", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "CEL"], "unexpected page list after the removal"
assert "qtype_sort_done" in card["signals_expected"]
card["signals_expected"] = [x for x in card["signals_expected"] if x != "qtype_sort_done"]
assert not any(sig == "qtype_sort_done" for s in card["slides"] for sig in (s.get("signals") or {}).get("on_complete", [])), "a remaining page still fires qtype_sort_done"
# [letter-fig] L1 (asked 2026-10-26): after P2's round gate ("अब आपकी बारी!"), one self-driving story page before the end screen,
# the Figma frames played as a scene: 538:2 (the girl writing) with sfx_letter_magic -> after 2 s 538:35 (the girl thinking) ->
# the thought bubbles and the grandfather cloud (the user's 1.png = the cloud baked into 538:39) grow in slowly as the piano
# loop starts -> in the same cloud the grandfather dissolves to white and the letter (the user's 2.png = 610:6's envelope, at
# 558:2's size) appears with sfx_letter_idea -> it pulses, tappable -> the tap (sfx_letter_pop) zooms it to 610:6 (71,-50
# 1138x758 over the blurred room) -> the flap opens (sfx_letter_paper), the sheet rises, a veil -> the end screen. Numbers
# measured on the renders (scratchpad measure_*.py): the cloud = 1.png at 0.2508 x (862.09, 8.61); bubbles (centre, diameter);
# the envelope 188.9 px wide in 558:2, centred in the cloud. Phase practice = round 3 continues (no second gate before CEL).
# [letter-idea] (asked 2026-10-27): the chime (sfx_letter_idea: "ummm" from its first frame to 1.16 s, silence, "aahaha" from
# 2.37 s — read off the clip, see README) now sounds the moment the grandfather cloud has stood its hold, and drives what follows:
# on the "ummm" the cloud and the bubbles leave and the girl is pensive (scene_c = the user's 1.png of 2026-10-27: the same room,
# her face closed), no cloud; on the "aahaha" she brightens again (scene_b — which IS the user's 2.png of that day, byte for byte)
# and the SAME cloud grows in again, white now, the letter growing in it (the cloud's own entrance replayed, the bubbles popping
# again just ahead of it); then it pulses and waits for the tap. pace: hum_at / aha_at = those two moments in the chime (ms),
# rebub_gap = the bubbles' re-pop spacing ahead of the "aahaha", letter_in = the growth after which the letter is tappable. The
# dissolve (the grandfather fading to white inside the standing cloud) and the letter's own pop-in are gone.
LETTER_IMGS = {"img_letter_scene_a": "✏️", "img_letter_scene_b": "✏️", "img_letter_scene_c": "🤔", "img_letter_blur": "✏️", "img_letter_cloud_grandpa": "💭",
               "img_letter_cloud_white": "💭", "img_letter_env_body": "✉️", "img_letter_env_flap": "✉️", "img_letter_env_inner": "✉️", "img_letter_env_heart": "❤️"}
LETTER_SND = ["sfx_letter_magic", "sfx_letter_idea", "sfx_letter_pop", "sfx_letter_paper", "bgm_letter_nostalgia"]
for k, emo in LETTER_IMGS.items():
    card["assets"]["image"][k] = f"assets/Images/{k}.webp"; card["_emoji_fallback"][k] = emo
for k in LETTER_SND:
    card["assets"]["audio"][k] = f"assets/Audio/{k}.ogg"
i_p2 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "P2")
assert card["slides"][i_p2 + 1]["id"] == "CEL"
card["slides"].insert(i_p2 + 1, {"id": "L1", "phase": "practice", "eis": "iconic", "type": "LETTER_STORY", "prompt_hi": "", "audio": {},
    "data": {"scene_a": "img_letter_scene_a", "scene_b": "img_letter_scene_b", "scene_c": "img_letter_scene_c", "blur": "img_letter_blur",
             "cloud": "img_letter_cloud_grandpa", "cloud_white": "img_letter_cloud_white",
             "env": {"body": "img_letter_env_body", "flap": "img_letter_env_flap", "inner": "img_letter_env_inner", "heart": "img_letter_env_heart"},
             "sfx": {"magic": "sfx_letter_magic", "idea": "sfx_letter_idea", "pop": "sfx_letter_pop", "paper": "sfx_letter_paper"},
             "music": "bgm_letter_nostalgia",
             "layout": {"cloud": [862.09, 8.61, 314.5], "bubbles": [[814.7, 242.8, 8], [831.4, 230.5, 16], [854.0, 211.2, 26]],
                        "letter": [1020, 166, 189], "full": [71, -50, 1138, 758], "mouth": [568.8, 292.4]},
             "pace": {"a_hold": 2000, "xfade": 650, "bub_start": 2600, "bub_gap": 230, "cloud_start": 3300, "cloud_in": 1600, "hold": 2600,
                      "hum_at": 0, "aha_at": 2370, "rebub_gap": 160, "letter_in": 1300, "zoom": 1200, "paper_at": 350, "dive_at": 700, "dive": 1700, "dive_scale": 5.2,
                      "veil_at": 1900, "done_at": 2450}}})
# [stamp-fig] L2 = the Figma frame 565:28 "G3 guided story question" (the stamp page), after the letter page: the letter's sentence on a
# sheet on a wooden table, a tray with two stamps (। and ?), the demos' title bar. It drives itself: the table (under the letter
# page's veil, which lifts) and the title bar on its line (vo_stamp_intro); the sheet settles and the tray slides up; the two
# stamps pop in, each on the user's pop sound; the sentence is read without a pause, word by word (vo_stamp_sent); the empty
# slot appears and blinks 3.5 s (the demos' blink) — from that moment both stamps are the child's to drag. [stamp-drag]
# 0.5 s after the blink the guidance: the right stamp (?) lifts, glides slowly over the slot, hovers and glides home WITHOUT
# printing; it comes again after every 7 s without a touch. A stamp dropped anywhere but the slot, or the wrong stamp on the
# slot: the kit's incorrect buzz (= the user's standard sfx_incorrect_feedback), a wiggle, and it glides back. The right stamp on
# the slot: it presses on the user's stamp thud — the mark is printed on the slot's centre — glides home; the slot's box goes on
# the kit's correct chime (= the user's standard sfx_correct_feedback), the mark stays; the kit's confetti on its own sound (= the
# user's standard sfx confetti); then the end screen. (The three kit sounds and the user's files are the same recordings:
# correlation 1.000, the same lengths — checked 2026-10-26.)
# [stamp-rounds] (later 2026-10-26) a SECOND ROUND follows the confetti, frame 579:47: the stamps shrink away (their pop played
# backwards), the sentence goes word by word in reverse with the slot and its mark; the round's two stamps (। and the comma) pop
# in on their pops, its sentence "माँ ने मुझे मेरे जन्मदिन पर कई सारे / खिलौने [ ] पेन और किताबें दिलाई हैं ।" is read word by word
# (vo_stamp_sent2) on two rows in the frame's 448-wide box, the small slot (29x30 at 525,355) blinks, the drags follow as before
# — but NO guidance in this round [stamp-remind]: after 7 s without a touch the title's line is said again (and again after every
# further 7 s) — the comma is printed; after that round's confetti, a THIRD round the same way, frame 592:89: three stamps (। ? ,)
# pop in, "मुझे उपहार बहुत पसंद हैं" is read, the danda's slot blinks, the danda is printed; then a FOURTH round, frame 593:130: the
# same three stamps, "क्या आपको भी उपहार अच्छे लगते हैं / दादी जी कैसी हैं" is read on two rows, each row ending in its own empty slot
# — the TWO slots blink together; the "?" dropped on either prints it there and that box goes on the chime (the stamps are the
# child's again for the other), the confetti after the second; then a FIFTH round, frame 593:151: the letter's closing lines
# "उनके आम [ ] केले और / अमरूद के पौधे बड़े हुए या नहीं [ ] / आप मुझे पत्र लिखकर बताना [ ] / मैं आपके पत्र का इंतज़ार / करूँगी [ ]" on five
# rows with FOUR slots, each wanting its own stamp (the comma, the ?, the danda twice — a slot carries its own mark and pick), the
# sign-off "आपकी प्यारी / पिंकी 🩷" shown under them with the last word (not read); the same three stamps; each box goes on its own
# chime as its stamp is pressed, the confetti after the fourth. data.rounds holds the page's five frames.
# [stamp-final] (later 2026-10-26) after the LAST round's confetti, the finale: the whole stage dissolves slowly and smoothly (3 s)
# into the user's picture (the girl at her desk holding up the stamped letter, images.final) as its chime sounds (sfx.final, the
# user's "simple notification", 3.4 s, started with the dissolve); then the envelope in the picture glitters gold — a soft glow and
# sparks over it (layout.envelope) — for 1.3 s on the second chime (sfx.glitter, the user's "new notification 037"); 0.7 s later the
# end screen.
# Numbers measured on the frame (get_metadata) and its render; the clips + timings from stamp_assets/ (recap_vo.py stamp); the
# bitmaps = the frame's own assets (scratchpad make_stamp_assets.py: the sheet "image 238" turned as the frame shows it).
STAMP_KEYS = ["intro", "sent", "sent2", "sent3", "sent4", "sent5"]   # [stamp-rounds] sent2..sent5 = the later rounds' sentences (frames 579:47, 592:89, 593:130, 593:151)
sl_ = {k: json.loads((SCR / "stamp_assets" / f"vo_stamp_{k}.words.json").read_text(encoding="utf-8")) for k in STAMP_KEYS}
STAMP_IMGS = {"img_stamp_wood": "🪵", "img_stamp_sheet": "📄", "img_stamp_tray": "🧰", "img_stamp_danda": "।", "img_stamp_question": "?", "img_stamp_comma": ",",
              "img_stamp_final": "💌"}   # [stamp-final] the finale's picture (the user's 1672x941 PNG at 1280x720, lossless)
STAMP_SND = ["sfx_stamp_pop", "sfx_stamp_press",
             "sfx_stamp_final", "sfx_stamp_glitter"]   # [stamp-final] the user's universfield-simple-notification-152054 (3.4 s) and universfield-new-notification-037-485898 (1.3 s), as ogg
for k, emo in STAMP_IMGS.items():
    card["assets"]["image"][k] = f"assets/Images/{k}.webp"; card["_emoji_fallback"][k] = emo
for k in STAMP_SND:
    card["assets"]["audio"][k] = f"assets/Audio/{k}.ogg"
for k in STAMP_KEYS:
    card["assets"]["audio"][f"vo_stamp_{k}"] = f"assets/Audio/vo_stamp_{k}.ogg"; card["assets"]["audio_text"][f"vo_stamp_{k}"] = sl_[k]["text"]
i_l1 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "L1")
assert card["slides"][i_l1 + 1]["id"] == "CEL"
card["slides"].insert(i_l1 + 1, {"id": "L2", "phase": "practice", "eis": "enactive", "type": "STAMP_DEMO", "prompt_hi": sl_["intro"]["shown"],
    "audio": {"prompt": "vo_stamp_intro"},
    "data": {"band_hi": sl_["intro"]["shown"], "intro_audio": "vo_stamp_intro",
             "images": {"wood": "img_stamp_wood", "sheet": "img_stamp_sheet", "tray": "img_stamp_tray", "final": "img_stamp_final"},
             "sfx": {"pop": "sfx_stamp_pop", "press": "sfx_stamp_press", "final": "sfx_stamp_final", "glitter": "sfx_stamp_glitter"},
             # [stamp-final] envelope = the glitter's box over the envelope in the final picture (its paper x 795..883, y 182..258 at 1280x720)
             "layout": {"sheet": [355, 64, 571, 594], "tray": [427, 565, 426, 142], "envelope": [783, 168, 112, 102]},
             # [stamp-rounds] the rounds, one per frame: the sentence (its clip and word times), the mark, which stamp is right (pick),
             # the two stamps' pictures, their boxes in the tray and print points (the middle of the face's bottom edge, in the box),
             # the sentence's box (the frame's, 2 px lower: Noto's ink sits 2 px above Figma's fallback's; lh = the frame's row height
             # when there are two rows, gap = an empty span before word #before, w wide, where the slot sits, tail = an empty span
             # after the last word, the frame's trailing space: the last row centres 2 px left of the first), the slot's box and
             # its dash runs read off the frame's render — or `slots`, a list of such boxes, when a round has several (frames 593:130,
             # 593:151); a slot may carry its own mark and pick when the round's slots want different stamps (593:151). sign = small
             # text lines (the letter's sign-off) shown with the sentence's last word, cleared with the sentence
             "rounds": [
               # [baloo-font] (2026-10-30) every slot x below sits the same distance after its word's ink as it did in Noto (Baloo 2
               # ExtraBold's words end up to 5 px further right): 751 -> 755, 525 -> 522.4, 751 -> 753.7, 822 -> 825.9, 707 -> 711.3,
               # 633 -> 630.8, 804 -> 805.9, 798 -> 802.9, 679 -> 679.7
               # guide: the right stamp's guidance glide 0.5 s after the blink and after every 7 s idle (round 1 only); a round
               # without it says the title's line again after every 7 s without a touch instead [stamp-remind]
               {"frame": "565:28", "guide": True, "sentence": {"text_hi": sl_["sent"]["shown"], "audio": "vo_stamp_sent", "word_times": [t[0] for t in sl_["sent"]["word_times"]], "word_end": sl_["sent"]["word_times"][-1][1]},
                "mark": "?", "pick": 1, "stamps": ["img_stamp_danda", "img_stamp_question"],
                "boxes": [[532, 541, 74, 116], [677, 540, 72, 115]], "tips": [[36, 113], [35, 114]],
                "sent": {"x": 63, "y": 338, "w": 1075, "h": 48, "size": 30},
                "slot": {"x": 755, "y": 331, "w": 36, "h": 58, "dash_h": [6, 9, 6, 9, 6], "dash_v": [6, 7, 4, 10, 4, 10, 4, 7, 6]}},
               {"frame": "579:47", "guide": False, "sentence": {"text_hi": sl_["sent2"]["shown"], "audio": "vo_stamp_sent2", "word_times": [t[0] for t in sl_["sent2"]["word_times"]], "word_end": sl_["sent2"]["word_times"][-1][1]},
                "mark": ",", "pick": 1, "stamps": ["img_stamp_danda", "img_stamp_comma"],
                "boxes": [[532, 541, 74, 116], [677, 541, 72, 115]], "tips": [[36, 113], [36, 114]],
                "sent": {"x": 416, "y": 289, "w": 448, "h": 98, "size": 30, "lh": 49, "gap": {"before": 9, "w": 38.4}},   # [baloo-font] w 37 -> 38.4: the old ink gap in Baloo 2;   # no tail span: the danda's own side bearing already centres the row 2 px left, as the render
                "slot": {"x": 522.4, "y": 355, "w": 29, "h": 30, "dash_h": [4, 9, 3, 9, 4], "dash_v": [4, 9, 4, 9, 4]}},
               # the third round (frame 592:89): a statement, the danda's slot after it (round 1's box and dashes: the same group), THREE
               # stamps in the tray — । 462,541 (the right one), ? 607,540, the comma 750,540; the sentence's 1075-wide box at 78,336 (its
               # ink 483..747 x 342..378 on the render), set 2 px lower like the others
               {"frame": "592:89", "guide": False, "sentence": {"text_hi": sl_["sent3"]["shown"], "audio": "vo_stamp_sent3", "word_times": [t[0] for t in sl_["sent3"]["word_times"]], "word_end": sl_["sent3"]["word_times"][-1][1]},
                "mark": "।", "pick": 0, "stamps": ["img_stamp_danda", "img_stamp_question", "img_stamp_comma"],
                "boxes": [[462, 541, 74, 116], [607, 540, 72, 115], [750, 540, 72, 115]], "tips": [[36, 113], [35, 114], [36, 114]],
                "sent": {"x": 78, "y": 338, "w": 1075, "h": 48, "size": 30},
                "slot": {"x": 753.7, "y": 331, "w": 36, "h": 58, "dash_h": [6, 9, 6, 9, 6], "dash_v": [6, 7, 4, 10, 4, 10, 4, 7, 6]}},
               # the fourth round (frame 593:130): two questions on two rows (the frame's 402-wide box at 415,310, set 1 px lower: its
               # rows' ink then lies on the render's, 316..346 and 365..395), each row ending in its own slot for the "?": TWO slots
               # (36x58, round 1's box and dashes — the same group) at 822,305 and 707,354; the same three stamps as round 3, the ? right
               {"frame": "593:130", "guide": False, "sentence": {"text_hi": sl_["sent4"]["shown"], "audio": "vo_stamp_sent4", "word_times": [t[0] for t in sl_["sent4"]["word_times"]], "word_end": sl_["sent4"]["word_times"][-1][1]},
                "mark": "?", "pick": 1, "stamps": ["img_stamp_danda", "img_stamp_question", "img_stamp_comma"],
                "boxes": [[462, 541, 74, 116], [607, 540, 72, 115], [750, 540, 72, 115]], "tips": [[36, 113], [35, 114], [36, 114]],
                "sent": {"x": 415, "y": 311, "w": 402, "h": 98, "size": 30, "lh": 49},
                "slots": [{"x": 825.9, "y": 305, "w": 36, "h": 58, "dash_h": [6, 9, 6, 9, 6], "dash_v": [6, 7, 4, 10, 4, 10, 4, 7, 6]},
                          {"x": 711.3, "y": 354, "w": 36, "h": 58, "dash_h": [6, 9, 6, 9, 6], "dash_v": [6, 7, 4, 10, 4, 10, 4, 7, 6]}]},
               # the fifth round (frame 593:151): the letter's closing lines on FIVE rows (the frame's 339-wide box at 468,180, set 1 px
               # lower; its rows' ink 186..212, 235..271, 284..318, 333..364, 382..408 on the render), FOUR slots with their own marks and
               # stamps — the comma's (29x30 at 633,198, between आम and केले: a gap span before केले), the ?'s (30x45 at 804,228 after
               # नहीं), the dandas' (30x45 at 798,280 after बताना and 679,376 after करूँगी) — and the sign-off "आपकी प्यारी / पिंकी 🩷"
               # (16 px, 81-wide boxes at 427,449 and 427,481) shown with the last word, not read; the same three stamps. (The frame
               # draws the sheet 6 px higher than the others, 925,58: the sheet stays where every round has it.)
               {"frame": "593:151", "guide": False, "sentence": {"text_hi": sl_["sent5"]["shown"], "audio": "vo_stamp_sent5", "word_times": [t[0] for t in sl_["sent5"]["word_times"]], "word_end": sl_["sent5"]["word_times"][-1][1]},
                "mark": "।", "pick": 0, "stamps": ["img_stamp_danda", "img_stamp_question", "img_stamp_comma"],
                "boxes": [[462, 541, 74, 116], [607, 540, 72, 115], [750, 540, 72, 115]], "tips": [[36, 113], [35, 114], [36, 114]],
                "sent": {"x": 468, "y": 181, "w": 339, "h": 245, "size": 30, "lh": 49, "gap": {"before": 2, "w": 31.4}},   # [baloo-font] w 30 -> 31.4: the old ink gap in Baloo 2;   # the 30 px gap span: आम ends at 629 and केले starts at 665, as the render
                "sign": [{"text": "आपकी प्यारी", "x": 427, "y": 451, "w": 81, "h": 26, "size": 16}, {"text": "पिंकी 🩷", "x": 427, "y": 483, "w": 81, "h": 26, "size": 16}],   # 2 px lower than the frame: Noto's ink on the render's rows
                "slots": [{"x": 630.8, "y": 198, "w": 29, "h": 30, "mark": ",", "pick": 2, "dash_h": [4, 9, 3, 9, 4], "dash_v": [4, 10, 2, 10, 4]},
                          {"x": 805.9, "y": 228, "w": 30, "h": 45, "mark": "?", "pick": 1, "dash_h": [4, 10, 2, 10, 4], "dash_v": [4, 10, 3, 11, 3, 10, 4]},
                          {"x": 802.9, "y": 280, "w": 30, "h": 45, "dash_h": [4, 10, 2, 10, 4], "dash_v": [4, 10, 3, 11, 3, 10, 4]},
                          {"x": 679.7, "y": 376, "w": 30, "h": 45, "dash_h": [4, 10, 2, 10, 4], "dash_v": [4, 10, 3, 11, 3, 10, 4]}]}],
             "pace": {"intro_at": 400, "after_intro": 500, "sheet_in": 0, "tray_in": 150, "stamps_at": 700, "pop_gap": 350, "sent_at": 700,
                      "blink_ms": 3500,
                      # [stamp-drag] the guidance: hint_at after the blink, the glide out, the hover, the glide home; again after idle_ms
                      "hint_at": 500, "glide": 1500, "hover_up": 34, "hold": 450, "back": 1100, "idle_ms": 7000,
                      # the child's drop: the print point within tol of the slot's centre; a move under tap_px is a touch, not a placing
                      "tol_x": 50, "tol_y": 70, "tap_px": 10, "wiggle": 450, "reset": 500,
                      # the right drop: over the slot (snap), down (press) on the thud, the mark, up, home; the box goes; confetti; then at
                      # done_at the end — or, with a round to follow [stamp-rounds], the clearing: the words out words_out apart (in
                      # reverse), the stamps' pop backwards pop_gap apart, the next round's stamps popping in at next_at
                      "snap": 220, "press": 140, "press_down": 20, "thud_at": 280, "mark_at": 400, "lift_at": 560, "back_at": 800, "back_home": 800,
                      "gone_at": 1600, "confetti_at": 2100, "done_at": 4400, "words_out": 40, "next_at": 1300,
                      # [stamp-final] from the finale's start (done_at after the last drop): the dissolve's length (with its 3.4 s chime), the
                      # glitter's start and length (with its 1.3 s chime), its sparks, and the hand-over to the end screen
                      "fin_fade": 3000, "fin_glitter_at": 3400, "fin_glitter_ms": 1300, "fin_sparks": 16, "fin_done": 5400}},
    "signals": {"on_complete": []}})
assert [s["id"] for s in card["slides"]] == ["T0", "T0B", "T1", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "L1", "L2", "CEL"]
pd = {}
for s in card["slides"]: pd[s["phase"]] = pd.get(s["phase"], 0) + 1
card["phase_distribution"] = pd
card["signals_expected"] = ["phase_transition" if x == "phase_transition_shown" else x for x in card["signals_expected"]]
title_hi = card["title"]["hi"]

# ---------- 4. engine JS patches ----------
js = ref_js
js = sub1(js, r"if\(oceanCleanup\)\{oceanCleanup\(\);oceanCleanup=null;\}",
          'if(typeof oceanCleanup!=="undefined" && oceanCleanup){oceanCleanup();oceanCleanup=null;}', 0, "oceanCleanup")
js = sub1(js, r"  if\(\['MATCH_THE_PAIR','MATCH_VACHAN_PAIRS'\]\.includes\(slide\.type\) && next\?\.type === 'FILL_VACHAN_DRAG'\)\{\n.*?return;\n  \}\n",
          "", re.S, "ocean fish branch")
js = sub1(js, r'const endPraiseVo = "assets/Audio/ocean_correct_1\.mp3";',
          'const endPraiseVo = audioFor(slide, "prompt") || null;   // [reskin] this lesson\'s own celebration line (vo_celebrate)', 0, "endPraiseVo")
js = sub1(js, r"/\* ---------- 12\. SLIDE MODULES ---------- \*/",
          lambda m: ported_js + m.group(0), 0, "section 12")
js = sub1(js, r"^  PHASE_TRANSITION: \{",
          lambda m: "  /* ===== [reskin] PORTED from the HI02H12_L01_S01 engine (2026.07.21b-unified): the punctuation lesson's own\n"
                    "     content modules. Same helper contracts (mountTapOptions / makeDraggable / dragWrong / celebrateThenAdvance /\n"
                    "     startNudge / imgOrEmoji / audioFor / setNavActive / completeSlide); only the bus name changed (SwiftPAL -> GameBus). ===== */\n"
                    + ported_mods + "\n" + m.group(0), re.M, "PHASE_TRANSITION anchor")
story_js = r"""/* ---------- [story-fig] THE STORY PAGES' FRAME + NARRATED TEXT ----------
   Shared by STORY_LISTEN (T0) and STORY_RELISTEN (T0B), both built on the Figma "html_Guided_instructions"
   frames (FLN-by-MJ). sfigMount() turns the tutorial card into the frames' card: the grid, the page's own
   elements (`inner`, laid out in the frame's 1280x720 px — style.css [story-fig]) and the Hello Swiftie.
   sfigLine() makes a narrated text: one span per word ("\n" = a line break) plus its clip, word times and the last word's end.
   sfigNarrate() shows the text WHOLE and reads it, each word lit as it is read ([word-sync], below): word_times are each
   word's start (s) in the clip (whisper's word times, vo_rec.py), word_end the last word's end, read against the clip's
   own currentTime, so a late or slow start stays in sync; without times the clip is shared out by word length. */
function sfigMount(host, inner){
  const card = host.closest(".tut-card"); if(card) card.classList.add("no-prompt", "sfig-card");
  const fig = document.createElement("div"); fig.className = "sfig-in";
  const grid = (c)=> '<img class="sfig-grid ' + c + '" src="assets/UI/story_grid.svg" width="718.497" height="718.497" alt="" draggable="false">';
  fig.innerHTML = '<div class="sfig-clip">' + grid("g1") + grid("g2") + '</div>' + inner +
    '<img class="sfig-swiftie" src="assets/UI/title_swiftie_hello.png" alt="Swiftee" draggable="false">';
  host.appendChild(fig);
  return fig;
}
function sfigLine(p, text, wordTimes, audio, wordEnd){
  text = String(text || "").trim();
  p.setAttribute("aria-label", text.replace(/\s+/g, " "));
  const words = [];
  text.split("\n").forEach((row, r)=>{
    if(r) p.appendChild(document.createElement("br"));
    row.trim().split(/\s+/).forEach((w, i)=>{
      if(i) p.appendChild(document.createTextNode(" "));
      const s = document.createElement("span"); s.className = "sfig-w"; s.textContent = w;
      words.push(p.appendChild(s));
    });
  });
  const lens = words.map(w => Array.from(w.textContent).length), total = lens.reduce((a, c)=> a + c, 0) || 1;
  const share = lens.map((_, i)=> lens.slice(0, i).reduce((a, c)=> a + c, 0) / total);
  const times = Array.isArray(wordTimes) && wordTimes.length === words.length ? wordTimes : null;
  const src = audio ? ("assets/Audio/" + audio + "." + AUDIO_EXT) : null;
  return { p, words, share, times, end: wordEnd != null && isFinite(wordEnd) ? +wordEnd : null, src, file: src ? src.split("/").pop() : "", shown: false };
}
function sfigShow(L, n){ L.words.forEach((w, i)=> w.classList.toggle("on", i < n)); }
/* [word-sync] (2026-10-30) the reference game's sentence (hi-02-h04-l01-s01-dun, Page 1 T1; its STORY-INTRO-JS): the WHOLE
   sentence rises in at once (siSentIn: 0.45 s, opacity 0 -> 1 from 14 px lower at .96; style.css [word-sync]) and its clip starts
   as the rise ends (SENT_IN_MS); while the clip plays each word lights for exactly its stretch of the recording — dark orange
   with a small pop (the reference's .p2-word.on: #E86A00, p2WordPop .28 s), one at a time — and the light goes off at the last
   word's end, or as soon as the clip is cut (the reference's wordSync). sfigRise(L, extra) shows the line (and `extra`
   elements that come with it) that way; sfigSync(L) lights its words on the clip that has just started (currentAudio). */
const SENT_IN_MS = 450;
function sfigRise(L, extra){
  const more = extra || [];
  L.p.classList.add("sfig-whole");   // the words' own arrival transitions are off: they are all there at once
  sfigShow(L, L.words.length); more.forEach(el=> el.classList.add("on")); L.shown = true;
  [L.p].concat(more).forEach(el=>{
    el.classList.remove("sfig-rise"); void el.offsetWidth; el.classList.add("sfig-rise");
    let fin = false;
    const done = ()=>{ if(fin) return; fin = true; el.classList.remove("sfig-rise"); if(el === L.p) el.classList.remove("sfig-whole"); };
    el.addEventListener("animationend", function h(e){ if(e.target === el && e.animationName === "siSentIn"){ el.removeEventListener("animationend", h); done(); } });
    setTimeout(done, SENT_IN_MS + 250);
  });
}
function sfigSync(L){
  if(L.unsync) L.unsync();
  const a = currentAudio;
  if(!a || !L.file || decodeURIComponent(String(a.currentSrc || a.src || "").split("/").pop()) !== L.file) return;
  const ws = L.words;
  let raf = 0, lit, off = false;
  const stop = ()=>{ if(off) return; off = true; if(raf) cancelAnimationFrame(raf); ws.forEach(w=> w.classList.remove("hot")); if(L.unsync === stop) L.unsync = null; };
  L.unsync = stop;
  const tick = ()=>{
    raf = 0;
    if(!ws.length || !ws[0].isConnected || a.ended || currentAudio !== a || (a.paused && a.currentTime > 0)){ stop(); return; }
    const dur = isFinite(a.duration) && a.duration > 0 ? a.duration : 0;
    const starts = L.times || (dur ? L.share.map(s=> s * dur) : null);
    if(starts){
      const tt = a.currentTime, end = L.end != null ? L.end : (dur || Infinity);
      if(tt >= end){ stop(); return; }
      let s = null; starts.forEach(x=>{ if(tt >= x) s = x; });   // the word(s) whose stretch this is: words sharing a start ("है ।") light together
      if(s !== lit){ lit = s; ws.forEach((w, i)=> w.classList.toggle("hot", s !== null && starts[i] === s)); }
    }
    raf = requestAnimationFrame(tick);
  };
  tick();
}
/* live() = "still this run, on a mounted page"; onEnd runs once, with every word shown. A line not yet on screen rises in first
   and is read SENT_IN_MS later; a line already shown (a replay) is read at once. Watchdog: a clip that never reports its end
   must not strand the page. It stops the clip first, so आगे still opens live, never greyed out under a "playing" clip. */
function sfigNarrate(L, live, onEnd){
  let done = false;
  const end = ()=>{
    if(done || !live()) return;
    done = true;
    if(L.unsync) L.unsync();
    sfigShow(L, L.words.length);
    onEnd();
  };
  const read = ()=>{
    if(!live()) return;
    play(L.src, end);
    sfigSync(L);
    const last = L.end != null ? L.end : (L.times ? L.times[L.times.length - 1] : authoredVoHoldMs(L.src) / 1000);
    setTimeout(()=>{ if(!done && live()){ stopAudio(); end(); } }, (last + 10) * 1000);
  };
  if(L.shown) read(); else { sfigRise(L); setTimeout(read, SENT_IN_MS); }
}

"""
story_mod = r"""  /* ===== [story-fig] STORY_LISTEN — the Figma story page, the first screen after the start gate's peek
     transition. It tells the story in BEATS on one layout (FLN-by-MJ frames 435:5, then 476:198): the picture
     sits in its grey-bordered frame and the beat's text rises in WHOLE in the white box under it and is read, each
     word lit as it is read (sfigNarrate, [word-sync]). When a beat's narration ends, after the engine's one-second beat (PACE.tail), its text
     leaves, the next picture appears over the last one, and the next narration starts once that picture has
     landed. आगे only ever shows LIVE: it stays hidden (never the greyed-out pill the engine shows during a VO)
     while any narration sounds, and appears pulsing when the LAST narration ends; the 🔊 chip replays the beat
     on screen from its first word, hiding आगे again until that replay ends. ===== */
  STORY_LISTEN: {
    mount(host, slide){
      const d = slide.data || {};
      const beats = d.beats && d.beats.length ? d.beats
                  : [{ image_id: d.image_id, text_hi: d.text_hi, word_times: d.word_times, audio: (slide.audio || {}).narration }];
      const fig = sfigMount(host,
        '<div class="sfig-pic">' + beats.map((b, k)=> '<img class="sfig-img b' + (k + 1) + (k ? '' : ' on') + '" src="' +
          imgSrc(b.image_id) + '" alt="" draggable="false">').join("") + '</div>' +
        '<div class="sfig-textbox"></div>' + beats.map((_, k)=> '<div class="sfig-text b' + (k + 1) + '"><p></p></div>').join(""));
      const pics = fig.querySelectorAll(".sfig-img"), texts = fig.querySelectorAll(".sfig-text");
      const lines = beats.map((b, k)=> sfigLine(texts[k].querySelector("p"), b.text_hi, b.word_times, b.audio, b.word_end));

      state.ownsAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
      setSwMood("talk");
      const alive = ()=> fig.isConnected;
      let run = 0, cur = 0, popped = false;   // [story-cat] popped: beat 1's sound and pop happen once per visit
      // [poem-box] the white box wraps the sentence on screen (the reference poem game's caption): its width is the beat's text's
      // (style.css adds the padding and rim; box and texts share one centre); `smooth` = the move to the next sentence's width
      const box = fig.querySelector(".sfig-textbox");
      const fitBox = (k, smooth)=>{
        if(!smooth) box.style.transition = "none";
        box.style.setProperty("--sfig-tw", getComputedStyle(texts[k]).width);
        if(!smooth){ void box.offsetWidth; box.style.transition = ""; }
      };
      fitBox(0, false);
      if(document.fonts && document.fonts.ready) document.fonts.ready.then(()=>{ if(alive()) fitBox(cur, false); });   // the width once the face is in
      const armNav = ()=>{ if(!alive()) return; setNavActive(true); setSwMood("point"); };
      const start = ()=>{
        const mine = ++run;
        setNavActive(false);   // a replay hides आगे until its narration has ended
        sfigNarrate(lines[cur], ()=> mine === run && alive(), ()=>{
          if(cur === 0 && d.beat1_sfx && !popped){ popped = true;   // [story-cat] once, as beat 1's line ends: the beat's own sound with the picture's little pop (G4's)
            playKitSfx("storyBeat1", d.beat1_sfx, .8); pics[0].classList.add("sfig-pop"); }
          if(cur < lines.length - 1){
            state.demoRunning = true;   // the replay chip waits out the turn to the next beat
            setTimeout(()=>{ if(mine === run && alive()) turn(); }, PACE.tail);
          } else armNav();
        });
      };
      // next beat: the finished text leaves, the next picture appears over the last one, then its narration
      const turn = ()=>{
        texts[cur].classList.add("gone");
        cur++;
        fitBox(cur, true);   // [poem-box] the box takes the next sentence's width once this one has faded (.3 s), before it rises
        pics[cur].classList.add("on", "enter");
        setTimeout(()=>{ if(!alive()) return; state.demoRunning = false; start(); }, 650);
      };
      state.replayAudio = start;
      start();
    }
  },

  /* ===== [story-fig] STORY_RELISTEN — "आइए वाक्य सुनें।" (FLN-by-MJ frame 488:190), right after the story
     page: the same story again, now WITH its punctuation. The title appears as the intro line
     (data.intro_audio: "अब इन्हीं वाक्यों को फिर से सुनते हैं।") starts to sound; when that line ends the sentence
     box comes in, and once it has landed each sentence rises in whole and is read, each word lit as it is read
     (sfigNarrate, [word-sync]). Swiftie, the 🔊 chip, the card's box and आगे are the story page's. आगे only ever shows
     LIVE, when the sentences' narration ends; the 🔊 chip replays the sentences from their first word, hiding
     आगे again until that replay ends. ===== */
  STORY_RELISTEN: {
    mount(host, slide){
      const d = slide.data || {};
      // [relisten-pinki] d.lines: the frame's sentences, each with its own clip and word times (frame 654:567); without it, the
      // one text block (d.text_hi) read on d.audio, as before
      const multi = !!(d.lines && d.lines.length);
      const lines = multi ? d.lines : [{ text_hi: d.text_hi, word_times: d.word_times, audio: d.audio }];
      const fig = sfigMount(host, '<div class="sfig-title"><p></p></div><div class="sfig-sbox"></div>' +
        (multi ? '<div class="sfig-stext sfig-lines">' + lines.map((_, k)=> '<p class="l' + (k + 1) + '"><span class="sfig-sent"></span></p>').join("") + '</div>'
               : '<div class="sfig-stext"><p></p><p>&#8203;</p></div>'));
      const card = host.closest(".tut-card"); if(card) card.classList.add("sfig-round");
      const title = fig.querySelector(".sfig-title"), box = fig.querySelector(".sfig-sbox");
      title.querySelector("p").textContent = d.title_hi || "";
      const Ls = lines.map((ln, k)=> sfigLine(multi ? fig.querySelector(".sfig-stext p.l" + (k + 1) + " .sfig-sent") : fig.querySelector(".sfig-stext p"), ln.text_hi, ln.word_times, ln.audio, ln.word_end));
      // [relisten-pinki] a comma ending a word gets its own span, so the moral can light the marks alone
      const sents = multi ? [...fig.querySelectorAll(".sfig-sent")] : [], marks = [];
      if(multi) fig.querySelectorAll(".sfig-stext .sfig-w").forEach(w=>{ const m = w.textContent.match(/^(.+?)(,)$/);
        if(m){ w.textContent = m[1]; const s = document.createElement("span"); s.className = "sfig-mk"; s.textContent = m[2]; w.appendChild(s); marks.push(s); } });
      const A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const introSrc = A(d.intro_audio);

      state.ownsAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
      setSwMood("talk");
      const alive = ()=> fig.isConnected;
      let run = 0;
      const armNav = ()=>{ if(!alive()) return; setNavActive(true); setSwMood("point"); };
      const reset = ()=>{ sents.forEach(s=> s.classList.remove("hl")); marks.forEach(m=> m.classList.remove("on")); };
      // a clip with cues (seconds on its own clock): onCue(i) as each is reached, onEnd once it has ended (a watchdog stops a
      // stalled clip; the cues not yet reached fire at the end, so nothing is skipped)
      const speak = (src, cues, onCue, onEnd, live)=>{
        if(!src){ onEnd(); return; }
        let done = false, next = 0; const began = Date.now();
        const end = ()=>{ if(done || !live()) return; done = true; while(next < cues.length) onCue(next++); onEnd(); };
        play(src, end);
        const file = src.split("/").pop();
        setTimeout(()=>{ if(!done && live()){ stopAudio(); end(); } }, authoredVoHoldMs(src) + 10000);
        const tick = ()=>{ if(done || !live()) return;
          const a = currentAudio, own = !!a && decodeURIComponent(String(a.currentSrc || a.src || "").split("/").pop()) === file;
          const t = own ? a.currentTime : (Date.now() - began) / 1000;
          while(next < cues.length && t + 0.04 >= cues[next]) onCue(next++);
          if(next < cues.length) nextFrame(tick); };
        tick();
      };
      const readAll = ()=>{
        const mine = ++run; const live = ()=> mine === run && alive();
        setNavActive(false);   // a replay hides आगे until its narration has ended
        reset();   // [word-sync] a replay keeps the sentences on screen
        // [relisten-pinki] the explanation: each sentence lit (lifted, on its yellow) as its meaning is told; then the moral:
        // the commas lit orange, lifted, as it names the marks — they stay lit; then आगे
        const moral = ()=>{
          if(!multi || !d.moral_audio){ armNav(); return; }
          setTimeout(()=>{ if(!live()) return;
            speak(A(d.moral_audio), d.moral_cue != null ? [d.moral_cue] : [], ()=> marks.forEach(m=> m.classList.add("on")),
                  ()=> setTimeout(()=>{ if(live()) armNav(); }, 300), live); }, 500);
        };
        const explain = ()=>{
          if(!multi || !d.explain_audio){ moral(); return; }
          setTimeout(()=>{ if(!live()) return;
            speak(A(d.explain_audio), d.explain_cues || [], (i)=> sents.forEach((s, k)=> s.classList.toggle("hl", k === i)),
                  ()=> setTimeout(()=>{ if(!live()) return; sents.forEach(s=> s.classList.remove("hl")); moral(); }, 400), live); }, 500);
        };
        const readLine = (k)=> sfigNarrate(Ls[k], live, ()=>{ if(k + 1 < Ls.length) setTimeout(()=>{ if(live()) readLine(k + 1); }, 600); else explain(); });
        readLine(0);
      };
      // 1. the intro line, with the title appearing the moment it starts to sound
      state.demoRunning = true;   // the replay chip waits until the sentences are on screen
      const showTitle = ()=>{ if(alive()) title.classList.add("in"); };
      let introDone = false;
      const afterIntro = ()=>{
        if(introDone || !alive()) return;
        introDone = true; showTitle();
        // 2. the sentence box comes in; 3. once it has landed, the sentences are read
        box.classList.add("in");
        setTimeout(()=>{ if(!alive()) return; state.demoRunning = false; readAll(); }, 650);
      };
      play(introSrc, afterIntro);
      // the title starts the moment the clip's own clock starts moving ("playing" fires ~0.15 s before that)
      const a = currentAudio;
      const whenSounding = ()=>{
        if(!alive() || title.classList.contains("in")) return;
        if(a === currentAudio && a.currentTime > 0) showTitle(); else nextFrame(whenSounding);
      };
      if(a && introSrc && decodeURIComponent(String(a.src).split("/").pop()) === introSrc.split("/").pop()) whenSounding(); else showTitle();
      setTimeout(showTitle, 1500);   // a clip that is slow to start never keeps the title away
      // watchdog, as sfigNarrate's: an intro clip that never reports its end must not strand the page
      setTimeout(()=>{ if(!introDone && alive()){ stopAudio(); afterIntro(); } }, authoredVoHoldMs(introSrc) + 10000);
      state.replayAudio = readAll;
    }
  },

"""
js = sub1(js, r"/\* ---------- 12\. SLIDE MODULES ---------- \*/", lambda m: story_js + m.group(0), 0, "section 12 (story helpers)")
js = sub1(js, r"^  PHASE_TRANSITION: \{", lambda m: story_mod + m.group(0), re.M, "PHASE_TRANSITION anchor (story)")
recap_mod = r"""  /* ===== [recap-fig] MARKS_RECAP — "ये हैं तीन विराम चिह्न" (FLN-by-MJ frame 508:2), the three-marks recap after the
     read-again page. T0B's card, grid, Swiftie and 🔊 chip (the frame's card is that same box); the frame's own
     title and three rows: the mark in its white box, its name, when it is used, and an example in a yellow box.
     Everything arrives WITH its narration: the title as the intro line starts to sound (as on T0B); then, mark by
     mark, the box + mark pop in as the name's clip starts, the use follows with its clip, and the yellow box pops in
     as the example's clip starts — every text rising in whole, then read with each word lit (sfigNarrate), with a short
     breath between the beats and a longer one before the next mark. आगे only ever shows LIVE, when the last example
     has been read; the 🔊 chip is ignored while the marks are being read (the sequence drives itself) and afterwards
     reads the three marks again from the first, hiding आगे until that replay ends. ===== */
  MARKS_RECAP: {
    mount(host, slide){
      const d = slide.data || {}, rows = d.rows || [], GAP = 300, GAP_MARK = 700;
      const fig = sfigMount(host, '<div class="sfig-title"><p></p></div>' + rows.map((_, k)=>
        '<div class="rcf-row r' + (k + 1) + '"><div class="rcf-sign"><div class="rcf-mark"><p></p></div></div>' +
        '<div class="rcf-name"><p></p></div><div class="rcf-when"><p></p></div><div class="rcf-eg"><p></p></div></div>').join(""));
      const card = host.closest(".tut-card"); if(card) card.classList.add("sfig-round", "sfig-recap");
      const title = fig.querySelector(".sfig-title");
      title.querySelector("p").textContent = d.title_hi || "";
      const introSrc = d.intro_audio ? ("assets/Audio/" + d.intro_audio + "." + AUDIO_EXT) : null;
      // the beats in reading order: for each mark its name (with the box + mark), its use, its example (with the yellow box)
      const beats = [];
      fig.querySelectorAll(".rcf-row").forEach((row, k)=>{
        const r = rows[k] || {};
        row.querySelector(".rcf-mark p").textContent = r.mark || "";
        [["name", ".rcf-name", ".rcf-sign"], ["when", ".rcf-when", null], ["example", ".rcf-eg", ".rcf-eg"]].forEach(([key, sel, pop])=>{
          const p = r[key] || {};
          beats.push({ L: sfigLine(row.querySelector(sel + " p"), p.text_hi, p.word_times, p.audio, p.word_end),
                       pop: pop ? row.querySelector(pop) : null, mark: key === "name" });
        });
      });

      state.ownsAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
      setSwMood("talk");
      const alive = ()=> fig.isConnected;
      let run = 0;
      const armNav = ()=>{ if(!alive()) return; state.demoRunning = false; setNavActive(true); setSwMood("point"); };
      // beat i: its box pops in as its clip starts; the next beat after a breath (a longer one before the next mark)
      const read = (i, mine)=>{
        if(mine !== run || !alive()) return;
        if(i >= beats.length){ armNav(); return; }
        const b = beats[i];
        if(b.pop) b.pop.classList.add("in");
        sfigNarrate(b.L, ()=> mine === run && alive(), ()=>{
          const next = beats[i + 1];
          setTimeout(()=> read(i + 1, mine), next && next.mark ? GAP_MARK : GAP);
        });
      };
      const readAll = ()=>{
        const mine = ++run;
        state.demoRunning = true;   // the chip is ignored until the marks have been read; a replay hides आगे meanwhile
        setNavActive(false);
        read(0, mine);   // [word-sync] a replay keeps the texts on screen
      };
      // 1. the intro line, with the title appearing the moment it starts to sound (as on T0B)
      state.demoRunning = true;
      const showTitle = ()=>{ if(alive()) title.classList.add("in"); };
      let introDone = false;
      const afterIntro = ()=>{
        if(introDone || !alive()) return;
        introDone = true; showTitle();
        // 2. then the marks, one beat at a time
        setTimeout(()=>{ if(alive()) readAll(); }, GAP_MARK);
      };
      play(introSrc, afterIntro);
      // the title starts the moment the clip's own clock starts moving ("playing" fires ~0.15 s before that)
      const a = currentAudio;
      const whenSounding = ()=>{
        if(!alive() || title.classList.contains("in")) return;
        if(a === currentAudio && a.currentTime > 0) showTitle(); else nextFrame(whenSounding);
      };
      if(a && introSrc && decodeURIComponent(String(a.src).split("/").pop()) === introSrc.split("/").pop()) whenSounding(); else showTitle();
      setTimeout(showTitle, 1500);   // a clip that is slow to start never keeps the title away
      // watchdog, as sfigNarrate's: an intro clip that never reports its end must not strand the page
      setTimeout(()=>{ if(!introDone && alive()){ stopAudio(); afterIntro(); } }, authoredVoHoldMs(introSrc) + 10000);
      state.replayAudio = readAll;
    }
  },

"""
js = sub1(js, r"^  PHASE_TRANSITION: \{", lambda m: recap_mod + m.group(0), re.M, "PHASE_TRANSITION anchor (recap)")
demo_mod = r"""  /* ===== [demo-fig] PUNCT_DEMO — the run-on sentence demos (FLN-by-MJ frames 519:32 "G3 guided story question" = T2,
     521:288 "5 T3" = T3 and 523:320 "6 T4" = T4; T3 differs only in the sentence, the picture and the correct mark —
     data.layout; T4 also in the boxes' places and in having two slots, both blinking and both receiving the comma —
     data.slots, sentence.gaps, full.targets), right after the three-marks recap, on the whole stage (no card): the title bar with the Swiftie head, the picture
     and the sentence bar with its empty slot, the three mark tiles — no standing Swiftie and no 🔊 chip (2026-10-25:
     the frame has neither; its only Swiftie is the head in the title bar). It drives itself:
     1. the title bar appears as the intro line starts to sound (as on T0B); 2. the picture, the bar and the tiles come
     in, then the sentence is read without a pause, WORD BY WORD on the clip's clock; 3. the empty slot blinks for 3.5 s
     (three slow blinks); 4. "पूर्ण विराम": its tile is tapped for the child (pressed, its colours unchanged) and the
     others go dim, then the mark lands in the CENTRE of the slot (its ink, not its line box); 5. the sentence is read
     again with the mark named at its end — each word, then the mark, highlighted as it is read, every tile dim; 6. 1.5 s
     later the slot's box goes (the mark stays) and the page advances by itself: no आगे here (after T4, through the
     "चलिए, साथ में करें!" gate every time).
     [pick-fig] PUNCT_PICK (G1, frame 525:354 "7 G1"; G2, frame 600:197 "8 G2"; G3, frame 528:424 "9 G3") is the same page with the tap left to the CHILD: steps 1-3 as above,
     the tiles live from the moment the sentence has been read (as the slot starts to blink); a wrong tile wiggles (the engine's
     wgNo shake, the soft buzz) and stays tappable; the right one is pressed, the others dim, its mark lands in the slot as
     its name sounds (the engine's correct chime + confetti), and one beat after the name the page moves on by itself. ===== */
  PUNCT_DEMO: {
    mount(host, slide){
      const d = slide.data || {}, S = d.sentence || {}, F = d.full || {}, opts = d.options || [];
      const A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      // the empty slot(s): without data.slots, 519:32's one 59x100 slot (the CSS's, a dashed <rect>); a frame with its own
      // slots (T4: two 33x38) gives each one's box in the bar's frame px and its dash runs per side, as measured on the
      // frame's render — [margin, dash, gap, dash, margin], drawn as one dashed line per side (the rounded corners stay
      // open, as in the render) over a solid rounded rect that only shows while the slot is highlighted
      function slotHtml(sp){
        if(!sp) return '<div class="dmf-blank"><svg class="dmf-dash" width="59" height="100" viewBox="0 0 59 100" aria-hidden="true">' +
          '<rect x="1" y="1" width="57" height="98" rx="7" ry="7"/></svg><span class="dmf-mark"></span></div>';
        const w = sp.w, h = sp.h, da = (r)=> "0 " + r.join(" ");
        const side = (x1, y1, x2, y2, r)=> '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke-dasharray="' + da(r) + '"/>';
        return '<div class="dmf-blank dmf-own" style="left:' + (sp.x - 2.386) + 'px;top:' + (sp.y - 2.386) + 'px;width:' + w + 'px;height:' + h + 'px">' +
          '<svg class="dmf-dash" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '" aria-hidden="true">' +
          '<rect class="dmf-solid" x="1" y="1" width="' + (w - 2) + '" height="' + (h - 2) + '" rx="7" ry="7"/>' +
          side(0, 1, w, 1, sp.dash_h) + side(w - 1, 0, w - 1, h, sp.dash_v) + side(0, h - 1, w, h - 1, sp.dash_h) + side(1, 0, 1, h, sp.dash_v) +
          '</svg><span class="dmf-mark"></span></div>';
      }
      const fig = sfigMount(host,
        '<div class="dmf-band"><div class="dmf-pill"><p></p></div><div class="dmf-head"><img src="assets/UI/demo1_head.webp" alt="" draggable="false"></div></div>' +
        '<div class="dmf-pic"><img src="' + imgSrc(d.image_id) + '" alt="" draggable="false"></div>' +
        '<div class="dmf-bar"><p class="dmf-sent"></p>' + (d.slots && d.slots.length ? d.slots : [null]).map(slotHtml).join("") + '</div>' +
        opts.map((_, k)=> '<div class="dmf-tile t' + (k + 1) + '"><div class="dmf-base"></div><div class="dmf-face"></div><p class="dmf-sym"></p><p class="dmf-name"></p></div>').join(""));
      const card = host.closest(".tut-card"); if(card) card.classList.add("sfig-full");
      fig.querySelector(".dmf-pill p").textContent = d.band_hi || "";
      const tiles = Array.from(fig.querySelectorAll(".dmf-tile"));
      tiles.forEach((t, k)=>{ t.querySelector(".dmf-sym").textContent = opts[k].mark || ""; t.querySelector(".dmf-name").textContent = opts[k].name_hi || ""; });
      const band = fig.querySelector(".dmf-band"), pic = fig.querySelector(".dmf-pic"), bar = fig.querySelector(".dmf-bar"),
            blanks = Array.from(fig.querySelectorAll(".dmf-blank")), marks = Array.from(fig.querySelectorAll(".dmf-mark"));
      marks.forEach(m=>{ m.textContent = d.mark || ""; if(d.mark_size) m.style.fontSize = d.mark_size + "px"; });
      // a frame that places its sentence or picture differently from 519:32's (the CSS's) gives them in data.layout, in
      // frame px: sent_x = the sentence's text box left in the bar, img = the picture's [x, y, w, h] on the frame (T3);
      // pic_x = the picture box's left, bar = the sentence bar's [left, width], sent = the sentence's whole text box
      // {x, y, w (in the bar), size, lh (line box), ws (word spacing)} (T4)
      const lay = d.layout || {}, sentEl = fig.querySelector(".dmf-sent"), picX = lay.pic_x != null ? lay.pic_x : 197;
      if(lay.pic_x != null) pic.style.left = picX + "px";
      if(lay.bar){ bar.style.left = lay.bar[0] + "px"; bar.style.width = lay.bar[1] + "px"; }
      if(lay.sent_x != null) sentEl.style.left = (lay.sent_x - 2.386) + "px";   // less the bar's border
      // slot = 519:32's one slot moved to [x, y] in the bar (G2's sits at 573,20; T2's / T3's at 583,20)
      if(lay.slot && !(d.slots && d.slots.length)) Object.assign(fig.querySelector(".dmf-blank").style, { left: (lay.slot[0] - 2.386) + "px", top: (lay.slot[1] - 2.386) + "px" });
      if(lay.sent){ const t = lay.sent;
        Object.assign(sentEl.style, { left: (t.x - 2.386) + "px", top: (t.y - 2.386) + "px", width: t.w + "px", height: t.lh + "px",
                                      fontSize: t.size + "px", lineHeight: t.lh + "px", wordSpacing: t.ws + "px" }); }
      if(lay.img){ const [x, y, w, h] = lay.img;   // less the picture box's place (picX,211) and border
        Object.assign(pic.querySelector("img").style, { left: (x - picX - 2.386) + "px", top: (y - 211 - 2.386) + "px", width: w + "px", height: h + "px" }); }
      // tiles = each tile's grey base and white face [x, y, w, h] on the frame where they differ from 519:32's (null = the
      // CSS's); the mark and the name keep their centres on the frame (G1: the first base 1px taller, the middle tile 4px wider)
      (lay.tiles || []).forEach((tl, k)=>{ const t = tiles[k]; if(!tl || !t) return;
        const [bx, by, bw, bh] = tl.base, [fx, fy, fw, fh] = tl.face, dx = [197, 527, 857][k] - bx, dy = 443 - by;
        Object.assign(t.style, { left: bx + "px", top: by + "px", width: bw + "px", height: bh + "px" });
        Object.assign(t.querySelector(".dmf-base").style, { width: bw + "px", height: bh + "px" });
        Object.assign(t.querySelector(".dmf-face").style, { left: (fx - bx) + "px", top: (fy - by) + "px", width: fw + "px", height: fh + "px" });
        t.querySelectorAll(".dmf-sym, .dmf-name").forEach(e=>{ e.style.marginLeft = dx + "px"; e.style.marginTop = dy + "px"; }); });
      const L = sfigLine(sentEl, S.text_hi, S.word_times, S.audio, S.word_end);
      // the frame's own runs of spaces where a slot sits (T4: four after "आम" and after "केला"): sentence.gaps = the word
      // indices followed by such a run
      if(S.gaps && S.gaps.length){ sentEl.style.whiteSpace = "pre";
        S.gaps.forEach(i=>{ const n = L.words[i] && L.words[i].nextSibling; if(n && n.nodeType === 3) n.data = " ".repeat(S.gap_spaces || 4); }); }
      // sentence.nudge = {word index: px}: a word pulled in or out by a measured amount, where the frame's spacing differs
      // from what the browser's font gives (T4: the space before its closing danda)
      Object.entries(S.nudge || {}).forEach(([i, px])=>{ if(L.words[+i]) L.words[+i].style.marginLeft = px + "px"; });
      const pick = Math.max(0, opts.findIndex(o=> o.mark === d.mark)), picking = slide.type === "PUNCT_PICK";

      state.ownsAudio = true; state.demoRunning = true; setNavActive(false);
      $("navBtn").style.display = "none";   // the page advances itself
      setSwMood("talk");
      const alive = ()=> fig.isConnected;
      const after = (ms, fn)=> setTimeout(()=>{ if(alive()) fn(); }, ms);
      // plays a clip and reports, on the clip's own clock, how many of `times` it has reached (sfigNarrate's method);
      // onEnd runs once — a clip that never reports its end is stopped by the watchdog, so the page never strands
      const narrate = (src, times, onIndex, onEnd)=>{
        const began = Date.now(); let done = false, last = -1;
        const end = ()=>{ if(done || !alive()) return; done = true; if(times.length && last < times.length){ last = times.length; onIndex(last); } onEnd(); };
        play(src, end);
        const file = src ? src.split("/").pop() : "";
        const lastT = times.length ? times[times.length - 1] : authoredVoHoldMs(src) / 1000;
        setTimeout(()=>{ if(!done && alive()){ stopAudio(); end(); } }, (lastT + 10) * 1000);
        const tick = ()=>{
          if(done || !alive()) return;
          const a = currentAudio;
          const own = !!a && decodeURIComponent(String(a.currentSrc || a.src || "").split("/").pop()) === file;
          const t = own ? a.currentTime : (Date.now() - began) / 1000;
          let n = 0; while(n < times.length && t + 0.04 >= times[n]) n++;
          if(n !== last){ last = n; onIndex(n); }
          if(n < times.length) nextFrame(tick);
        };
        if(times.length) tick();
      };
      // 1. the title bar, appearing the moment the intro line starts to sound
      const introSrc = A(d.intro_audio);
      const showBand = ()=>{ if(alive()) band.classList.add("in"); };
      let introDone = false;
      const afterIntro = ()=>{ if(introDone || !alive()) return; introDone = true; showBand(); after(500, stage2); };
      play(introSrc, afterIntro);
      const a0 = currentAudio;
      const whenSounding = ()=>{
        if(!alive() || band.classList.contains("in")) return;
        if(a0 === currentAudio && a0.currentTime > 0) showBand(); else nextFrame(whenSounding);
      };
      if(a0 && introSrc && decodeURIComponent(String(a0.src).split("/").pop()) === introSrc.split("/").pop()) whenSounding(); else showBand();
      setTimeout(showBand, 1500);   // a clip that is slow to start never keeps the bar away
      setTimeout(()=>{ if(!introDone && alive()){ stopAudio(); afterIntro(); } }, authoredVoHoldMs(introSrc) + 10000);
      // 2. the picture, the sentence bar (with its empty slot) and the tiles come in; once landed, the whole sentence rises in
      //    and is read SENT_IN_MS later, each word lit as it is read ([word-sync])
      function stage2(){
        pic.classList.add("in"); bar.classList.add("in"); tiles.forEach(t=> t.classList.add("in"));
        after(650, ()=> narrate(L.src, L.times || [], n=> sfigShow(L, n), stage3));
      }
      // 3. the empty slot(s) blink (3.5 s) — every slot the same blink, started together
      function stage3(){
        blanks.forEach(b=>{ b.style.animationDuration = ((d.blink_ms || 3500) / 3) + "ms"; b.classList.add("blink"); });   // three slow blinks
        if(picking){ arm(); after(d.blink_ms || 3500, ()=> blanks.forEach(b=> b.classList.remove("blink"))); return; }
        after(d.blink_ms || 3500, ()=>{ blanks.forEach(b=> b.classList.remove("blink")); stage4(); });
      }
      // [pick-fig] PUNCT_PICK: from here the tiles are the child's. The idle reminder (the engine's one per slide, after 7 s
      // of quiet) reads the sentence again, each word highlighted as it is read
      // [hand-quiet] (2026-10-28) once the hand points (the 3rd wrong tap) nothing speaks any more: no hint 3, no idle re-read, no
      // chip, no praise after the guided tap; the other two tiles are dead and dim (CSS: .dmf-live .dmf-tile.off)
      let live = false, reread = 0, fbAudio = null;   // [tap-lock] fbAudio: the hint line now speaking, if any (feedback holds the tiles; the re-read does not)
      function arm(){
        live = true; state.demoRunning = false; fig.classList.add("dmf-live");
        tiles.forEach((t, k)=>{ t.onclick = ()=> tap(k);
          t.onanimationend = (e)=>{ if(e.target === t && e.animationName === "wgNo") t.classList.remove("wiggle"); }; });
        // [word-sync] each word lit as it is read (sfigSync: a punctuation-only word shares the start of the word before it, "हैं ।",
        // and the two light together); a tap cuts the clip and the light goes with it
        state.replayAudio = ()=>{ if(!live || isPlaying || sfxBusy() || hintHand) return; ++reread;   // [tap-lock] the chip waits for silence too; [hand-quiet] silent while the hand shows
          narrate(L.src, [], ()=>{}, ()=>{}); sfigSync(L); };
      }
      function tap(k){
        if(!live || !alive()) return;
        if(sfxBusy() || (isPlaying && currentAudio && currentAudio === fbAudio)) return;   // [tap-lock] while a feedback sound or line plays (the buzz, a hint line) no other tile answers
        if(isPlaying) stopAudio();   // the idle re-read is no feedback: a tap cuts it short and answers at once
        reread++; L.words.forEach(w=> w.classList.remove("hot"));
        const t = tiles[k], ok = k === pick, opt = opts[k] || {};
        GameBus.sendQuestionAnswered(slide, { is_correct: ok, score: ok && state.attempts === 0 ? 1 : 0, attempt: state.attempts + 1,
          ui_index: k, original_index: k, text: opt.name_hi || opt.mark || null });
        if(!ok){
          // a wrong tile wiggles, its colours unchanged, and stays tappable
          state.attempts++; sfxWrongSoft(); setSwMood("tryagain");
          GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
          t.classList.remove("wiggle"); void t.offsetWidth; t.classList.add("wiggle");
          setSwMood("tryagain");   // [dun-chrome] the title-bar bird's try-again face, as the reference's header bird
          return;
        }
        // the right one: pressed (the other two untouched since [tap-lock]), its mark lands in the slot as its name sounds; then the page moves on
        live = false; state.locked = true; state.demoRunning = true;
        blanks.forEach(b=> b.classList.remove("blink"));
        tiles.forEach((x, j)=>{ x.onclick = null; x.classList.remove("wiggle"); if(j === pick) x.classList.add("on"); });   // [tap-lock] only the tapped tile answers: the other two stay as they are (the demos' auto tap, stage4, still dims them)
        marks.forEach((m, j)=> after(j * (d.mark_stagger_ms || 300), ()=>{ centreInk(m); m.classList.add("in"); }));
        sfxCorrect(); confettiCannon(); setSwMood("happy");
        GameBus.emit("punct_build_done", { slide_id: slide.id, phase: slide.phase, value: true,
          first_try: state.attempts === 0, wrong: state.attempts, latency_ms: Date.now() - state.slideStart });
        narrate(A(d.mark_audio), [], ()=>{}, ()=> after(PACE.tail, ()=> completeSlide(true)));
      }
      // 4. the mark's name: its tile is tapped for the child, the others go dim; then the mark lands in the slot(s), one
      //    after the other (data.mark_stagger_ms apart) when there are several
      function stage4(){
        showHand();   // [demo-hand] the pointing hand under the tile as it is tapped for the child (the picks' hand)
        tiles.forEach((t, k)=> t.classList.add(k === pick ? "on" : "off"));
        const gap = d.mark_stagger_ms || 300;
        narrate(A(d.mark_audio), [], ()=>{}, ()=>{
          marks.forEach((m, k)=> after(400 + k * gap, ()=>{ centreInk(m); m.classList.add("in"); }));
          after(400 + (marks.length - 1) * gap + 700, stage5);
        });
      }
      // the danda's ink is not centred in its own line box (Noto's: it sits right of and above the box's centre), so the
      // mark is shifted by its ink's offset, measured from the font itself, to put the INK on the slot's centre; the
      // highlight's grow then scales about that same point (style.css: --ix / --iy, with the measured values as fallback)
      function centreInk(markEl){
        try{
          const cs = getComputedStyle(markEl), c = document.createElement("canvas").getContext("2d");
          c.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
          const t = c.measureText(markEl.textContent);
          if(!t.width || !isFinite(t.fontBoundingBoxAscent)) return;
          const base = (markEl.offsetHeight - t.fontBoundingBoxAscent - t.fontBoundingBoxDescent) / 2 + t.fontBoundingBoxAscent;
          const ix = (t.actualBoundingBoxRight - t.actualBoundingBoxLeft) / 2 - markEl.offsetWidth / 2;
          const iy = base + (t.actualBoundingBoxDescent - t.actualBoundingBoxAscent) / 2 - markEl.offsetHeight / 2;
          markEl.style.setProperty("--ix", ix.toFixed(2) + "px"); markEl.style.setProperty("--iy", iy.toFixed(2) + "px");
        }catch(e){}
      }
      // 5. the sentence again with the mark named: each word, and the mark, highlighted as it is read; every tile dim.
      //    full.targets says what each token of that reading lights ("w<i>" = the sentence's word i, "s<k>" = slot k);
      //    without it, the words in order and then the slot for every token after them (T2, T3: the name at the end)
      function stage5(){
        tiles.forEach(t=>{ t.classList.remove("on"); t.classList.add("off"); });
        if(hintHand){ hintHand.remove(); hintHand = null; }   // [demo-hand] the hand leaves as the second reading begins
        const nW = L.words.length, tg = F.targets || (F.word_times || []).map((_, i)=> i < nW ? "w" + i : "s0");
        const hot = (n)=>{ const t = n > 0 ? String(tg[n - 1] || "") : "", wi = t[0] === "w" ? +t.slice(1) : -1, si = t[0] === "s" ? +t.slice(1) : -1;
          L.words.forEach((w, i)=> w.classList.toggle("hot", i === wi)); blanks.forEach((b, k)=> b.classList.toggle("hot", k === si)); };
        narrate(A(F.audio), F.word_times || [], hot, ()=>{
          // 6. the slots' boxes go (the marks stay) and the page moves on by itself
          after(d.hold_ms || 1500, ()=>{ L.words.forEach(w=> w.classList.remove("hot")); blanks.forEach(b=>{ b.classList.remove("hot"); b.classList.add("gone"); });
            after(600, ()=>{
              // T4: the gate into the guided round (the peeking Swiftie, "चलिए, साथ में करें!" and its VO) follows this
              // page EVERY time it ends: the engine shows each round's gate once per load, so a re-run of T4 (the dev
              // nav's list) went straight to G1 — clearing the round here lets completeSlide cross the same gate again
              const nx = CARD.slides[state.idx + 1], nr = nx && PHASE_ROUND[nx.phase];
              if(nr && nr !== PHASE_ROUND[slide.phase]) _gatedPhases.delete(nr);
              completeSlide(true); }); });
        });
      }
    }
  },

"""
js = sub1(js, r"^  PHASE_TRANSITION: \{", lambda m: demo_mod + m.group(0), re.M, "PHASE_TRANSITION anchor (demo)")
sent_mod = r"""  /* ===== [sent-fig] SENT_PICK — G4, P1 and P2 "सही विराम चिह्न वाला वाक्य चुनिए ।", built on the reference game's Page 11 (P4, the
     picture-to-sentence question of https://hi-02-h04-l01-s01-dun.vercel.app/): its layout, its elements and its flow, with
     this lesson's picture, title, sentences and VO. Under the engine header (Swiftie's head + 🔊 chip + the title band, in
     P4's look: style.css [sent-fig]) the picture is shown bare at 315px high (its grey frame is in the bitmap, as P4's) above
     ONE row of three white sentence pills (in a random order, as the engine shuffles answers); no आगे. A pill's words light
     up one at a time (orange, a slight pop) while its own line speaks. Sentences too long for P4's pill (P2's) go on two
     lines, every pill broken after the same word.
     - entry: the title's instruction (audio.prompt); it speaks AGAIN after every 5 s of quiet (no tap anywhere, nothing
       speaking, no read-out) for as long as the page is open, the picture giving a small silent pop-and-hold with each
       repeat; the chip replays it too. A tap on a pill cuts the instruction (or a repeat) short and answers at once; since
       [tap-lock] (2026-10-28) nothing answers while a FEEDBACK sound or line plays (the buzz, the try-again line, hint 3):
       the pills, the hand and the chip wait for it to end.
     - a wrong pill: the kit's wiggle + the soft buzz (the pill is not read out), 1 s (taps wait), then — 1st wrong:
       audio.try_again; 2nd: all three pills read one by one in row order (each lifted, its words lit, 0.5 s apart; taps
       wait); 3rd (max_attempts): the reveal — the two wrong pills greyed out and dead, the right one ringed green and
       pulsing, the pointing hand bobbing under it (a tap on the hand, or just beside the pill, counts as a tap on it).
     - the right pill: the green ring at once and the picture's pop (1 s, taps wait — P4 plays its picture's sound here;
       this picture has none), then the kit's correct-select, the ding, the confetti and the happy Swiftie, its line with its
       words lit, and 0.7 s later the page moves on. After the reveal (the guided tap): the same 1 s, then the ding + the
       confetti alone, Swiftie back to rest, and the page moves on 0.7 s later (recorded as a revealed answer).
     - data.mastery (P1, P2, as the practice pages they replace): one mastery attempt per page, a hit on a first try. ===== */
  SENT_PICK: {
    mount(host, slide){
      const d = slide.data || {}, A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const IDLE_MS = 5000, BEAT_MS = 1000, HOLD_MS = 1000, REVIEW_GAP_MS = 500, POP_MS = 1000, PROMPT_POP_MS = 3200, HIT_PAD = 24;
      const opts = (d.options || []).slice();
      for(let i = opts.length - 1; i > 0; i--){ const j = (Math.random() * (i + 1)) | 0; [opts[i], opts[j]] = [opts[j], opts[i]]; }
      const row = document.createElement("div"); row.className = "q-row";
      const stim = document.createElement("div"); stim.className = "story-q-stim sq-bare";
      const thumb = document.createElement("img"); thumb.className = "story-q-thumb"; thumb.src = imgSrc(d.recall_image_id); thumb.alt = ""; thumb.draggable = false;
      stim.appendChild(thumb);
      const grid = document.createElement("div"); grid.className = "opt-grid cols-3 sent-opts";
      // each pill's sentence split into word spans (one inline box, so the spaces stay); a lone danda is a word of its own
      const items = opts.map((o, k)=>{
        const cell = document.createElement("div"); cell.className = "sent-opt opt-cell"; cell.dataset.key = String(k);
        const pill = document.createElement("span"); pill.className = "so-pill story-caption";
        const wrap = document.createElement("span"); wrap.className = "p2-words";
        const words = [];
        String(o.label_hi || "").trim().split(/(\s+)/).forEach(t=>{
          if(!t) return;
          if(/^\s+$/.test(t)){ wrap.appendChild(document.createTextNode(t)); return; }
          const sp = document.createElement("span"); sp.className = "p2-word"; sp.textContent = t; wrap.appendChild(sp); words.push(sp);
        });
        pill.appendChild(wrap); cell.appendChild(pill); grid.appendChild(cell);
        return { cell, pill, words, opt: o, index: (d.options || []).indexOf(o), src: A(o.audio),
                 times: Array.isArray(o.word_times) && o.word_times.length === words.length + 1 ? o.word_times : null };
      });
      row.appendChild(stim); row.appendChild(grid); host.appendChild(row);
      const right = items.find(it=> it.opt.correct === true);

      state.ownsAudio = true; setNavActive(false); $("navBtn").style.display = "none";
      setSwMood("talk");
      const alive = ()=> row.isConnected;
      const after = (ms, fn)=> setTimeout(()=>{ if(alive()) fn(); }, ms);
      let hold = false, reviewing = false, idleOn = true;

      // a sentence too long for P4's pill on one line (P4's own all fit): every pill of the page then takes two lines, all
      // broken after the same word (the one that keeps the widest line narrowest; a lone mark stays with its word), so the
      // sentences still line up word for word and differ only in their marks. P4's pill width and font stay.
      const fitLines = ()=>{
        if(!alive() || grid.querySelector(".so-br") || !items.some(it=> it.pill.scrollWidth > it.pill.clientWidth)) return;
        const groups = items.map(it=> it.words.reduce((g, w)=>{
          if(/^[।॥,.!?]+$/.test(w.textContent) && g.length) g[g.length - 1].push(w); else g.push([w]);
          return g; }, []));
        const n = Math.min(...groups.map(g=> g.length)); if(n < 2) return;
        const span = (a, b)=> b.getBoundingClientRect().right - a.getBoundingClientRect().left;
        let best = 1, bestW = Infinity;
        for(let k = 1; k < n; k++){
          const w = Math.max(...groups.map(g=> Math.max(span(g[0][0], g[k - 1].at(-1)), span(g[k][0], g.at(-1).at(-1)))));
          if(w < bestW){ bestW = w; best = k; }
        }
        groups.forEach(g=>{   // the break after the space that follows the word (a space at a line's end is not drawn)
          const sp = g[best - 1].at(-1).nextSibling, br = document.createElement("br"); br.className = "so-br";
          sp.parentNode.insertBefore(br, sp.nextSibling);
        });
      };
      fitLines(); requestAnimationFrame(fitLines); if(document.fonts) document.fonts.ready.then(fitLines);

      // a pill's own line, its words lit one at a time on the clip's clock (each word from its start to the next one's)
      let wordRaf = 0, wordEls = null;
      const wordStop = ()=>{ if(wordRaf){ cancelAnimationFrame(wordRaf); wordRaf = 0; } if(wordEls){ wordEls.forEach(w=> w.classList.remove("on")); wordEls = null; } };
      const say = (it, then)=>{
        wordStop();
        play(it.src, ()=>{ wordStop(); if(then) then(); });
        const a = currentAudio; if(!a || !it.times) return;
        wordEls = it.words; let cur = -1;
        const tick = ()=>{
          wordRaf = 0;
          if(currentAudio !== a || a.ended || !alive()){ wordStop(); return; }
          const t = a.currentTime; let i = -1;
          for(let k = 0; k < it.words.length; k++){ if(t >= it.times[k] && t < it.times[k + 1]){ i = k; break; } }
          if(i !== cur){ if(cur >= 0) it.words[cur].classList.remove("on"); if(i >= 0) it.words[i].classList.add("on"); cur = i; }
          if(t >= it.times[it.times.length - 1]){ wordStop(); return; }
          wordRaf = requestAnimationFrame(tick);
        };
        wordRaf = requestAnimationFrame(tick);
      };

      // the instruction: on entry, from the header chip, and after every IDLE_MS of quiet (with the picture's pop-and-hold)
      const promptSrc = audioFor(slide, "prompt");
      const speakPrompt = (pop)=>{
        if(pop && !thumb.classList.contains("p2-pop")){
          thumb.classList.remove("p6-pop"); void thumb.offsetWidth; thumb.classList.add("p6-pop");
          setTimeout(()=> thumb.classList.remove("p6-pop"), PROMPT_POP_MS + 250);
        }
        play(promptSrc, ()=>{});
      };
      state.replayAudio = ()=>{ if(!hold && !reviewing && !state.locked && !isPlaying && !sfxBusy()) speakPrompt(false); };   // [tap-lock] the chip waits for silence too
      let lastPoke = Date.now();
      const poke = ()=>{ lastPoke = Date.now(); };
      document.addEventListener("pointerdown", poke, true);
      const idleTick = ()=>{
        if(!alive()){ document.removeEventListener("pointerdown", poke, true); return; }
        if(idleOn){
          if(isPlaying || hold || reviewing || state.hintActive || state.locked) lastPoke = Date.now();   // a line, the read-out or a beat: the count starts over after it
          else if(Date.now() - lastPoke >= IDLE_MS){ lastPoke = Date.now(); speakPrompt(true); }
        }
        setTimeout(idleTick, 100);
      };
      speakPrompt(false);
      idleTick();

      const report = (it, ok)=> GameBus.sendQuestionAnswered(slide, { is_correct: ok, score: ok && state.attempts === 0 ? 1 : 0,
        attempt: state.attempts + 1, ui_index: items.indexOf(it), original_index: it.index, text: it.opt.label_hi || null });
      let fbAudio = null;   // [tap-lock] the feedback line now speaking (the try-again line, hint 3), if any: it holds the pills; the instruction does not
      items.forEach(it=>{ it.cell.onclick = ()=> tap(it); });
      function tap(it){
        const guided = it.cell.classList.contains("opt-guided");
        if(!alive() || hold || reviewing || state.hintActive) return;
        if(["crossed", "correct", "opt-dim"].some(c=> it.cell.classList.contains(c)) || (state.locked && !guided)) return;
        if(sfxBusy() || (isPlaying && currentAudio && currentAudio === fbAudio)) return;   // [tap-lock] while a feedback sound or line plays (the buzz, the try-again line, hint 3) no other pill answers
        stopNudge(); wordStop();
        if(isPlaying) stopAudio();   // the instruction and its repeats are no feedback: a tap cuts them short and answers at once
        if(it === right) ok(it, guided); else wrong(it);
      }
      function wrong(it){
        report(it, false);
        state.attempts++; sfxWrongSoft(); setSwMood("tryagain");
        GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
        items.forEach(x=>{ if(x !== it) x.cell.classList.remove("crossed"); });
        it.cell.classList.add("crossed");
        playWrongSelect(it.cell);
        const maxA = (CARD.scaffold_rules && CARD.scaffold_rules.max_attempts) || 3;
        state.hintActive = true;                                     // the wrong beat: taps wait
        after(BEAT_MS, ()=>{
          state.hintActive = false;
          if(state.attempts >= maxA){ reveal(); return; }
          if(state.attempts >= 2){ state.scaffoldLevel = Math.max(state.scaffoldLevel, 2); review(()=> it.cell.classList.remove("crossed")); return; }
          state.scaffoldLevel = Math.max(state.scaffoldLevel, 1);
          play(audioFor(slide, "try_again"), ()=> it.cell.classList.remove("crossed")); fbAudio = currentAudio;   // [tap-lock] feedback: no other pill answers while it speaks
        });
      }
      // the 2nd wrong tap: every pill read out, one by one in row order, each lifted while its line speaks
      function review(then){
        reviewing = true; state.hintActive = true;
        items.forEach(x=> x.cell.classList.remove("crossed"));
        let k = 0;
        const next = ()=>{
          if(!alive()) return;
          if(k >= items.length){ after(300, ()=>{ reviewing = false; state.hintActive = false; then(); }); return; }
          const it = items[k++];
          after(REVIEW_GAP_MS, ()=>{ it.pill.classList.add("p6-say"); say(it, ()=>{ it.pill.classList.remove("p6-say"); next(); }); });
        };
        next();
      }
      // the 3rd wrong tap: the decoys go grey and dead, the answer is ringed and pulses, the hand points at it once all is quiet
      let hand = null;
      function reveal(){
        state.locked = true; state.scaffoldLevel = 3; setSwMood("hint");
        items.forEach(x=>{ x.cell.classList.remove("crossed"); if(x !== right) x.cell.classList.add("opt-dim"); });
        right.cell.classList.add("opt-guided");
        GameBus.emit("answer_revealed", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts, reason: "wrong" });
        const place = ()=>{
          if(!alive() || !right.cell.classList.contains("opt-guided")) return;
          if(isPlaying){ after(100, place); return; }
          const st = document.querySelector(".slide-stage"); if(!st) return;
          hand = document.createElement("img"); hand.className = "reveal-hand"; hand.src = "assets/UI/nudge_hand_new.svg"; hand.alt = "";
          hand.style.setProperty("pointer-events", "auto", "important"); hand.style.cursor = "pointer";
          hand.onclick = (e)=>{ e.stopPropagation(); tap(right); };
          st.appendChild(hand); placeHand(); requestAnimationFrame(placeHand);
        };
        after(0, place);
      }
      // under the answer's pill, centred on it, kept inside the stage (the reference's reveal hand: 96px)
      function placeHand(){
        if(!hand || !hand.parentNode) return;
        const st = document.querySelector(".slide-stage"), r = right.cell.getBoundingClientRect(), sw = st.getBoundingClientRect();
        const scale = sw.width / st.offsetWidth || 1, HAND_H = 96;
        hand.style.left = ((r.left - sw.left) / scale + r.width / scale / 2 - 48) + "px";
        hand.style.top = Math.min((r.bottom - sw.top) / scale + 4, st.offsetHeight - HAND_H) + "px";
      }
      // the guided pill counts a tap just beside it too (HIT_PAD design px), once nothing speaks
      const padTap = (e)=>{
        if(!alive()){ document.removeEventListener("click", padTap, true); return; }
        if(!right.cell.classList.contains("opt-guided") || isPlaying || hold) return;
        const t = e.target; if(!t || right.cell.contains(t) || (hand && t === hand)) return;
        if(typeof e.clientX !== "number" || (e.clientX === 0 && e.clientY === 0)) return;
        const st = document.querySelector(".slide-stage"), scale = st ? (st.getBoundingClientRect().width / st.offsetWidth || 1) : 1;
        const r = right.cell.getBoundingClientRect(), pad = HIT_PAD * scale;
        if(e.clientX < r.left - pad || e.clientX > r.right + pad || e.clientY < r.top - pad || e.clientY > r.bottom + pad) return;
        e.stopPropagation(); e.preventDefault(); tap(right);
      };
      document.addEventListener("click", padTap, true);
      // the right pill (first tries, or the guided tap after the reveal)
      function ok(it, guided){
        hold = true; state.locked = true; idleOn = false;
        if(d.mastery){ state.masteryAttempts++; if(state.attempts === 0) state.masteryHits++; }
        it.cell.classList.add("correct");
        if(guided){ if(hand){ hand.remove(); hand = null; } it.cell.classList.remove("opt-guided"); }
        thumb.classList.remove("p6-pop"); thumb.classList.add("p2-pop"); setTimeout(()=> thumb.classList.remove("p2-pop"), POP_MS + 250);
        if(d.tap_sfx && !isMuted){ try{   // [g4-giggle] the reference's G2 correct-tap effect: the page's own sound with the picture's pop, at .63, ending with the 1 s hold (a 150 ms fade, then paused)
          const sx = new Audio("assets/Audio/" + d.tap_sfx); sx.volume = .63; if(d.tap_sfx_from) sx.currentTime = d.tap_sfx_from;   // [p2-pencils] a file with a silent lead-in starts at its first sound
          sfxTrack(sx); const pp = sx.play(); if(pp && pp.catch) pp.catch(()=>{});
          const v0 = sx.volume, t0 = Date.now() + HOLD_MS - 150;
          const fade = ()=>{ if(sx.paused || sx.ended) return; const k = Math.min(1, (Date.now() - t0) / 150); sx.volume = Math.max(0, v0 * (1 - k)); if(k < 1) setTimeout(fade, 16); else sx.pause(); };
          setTimeout(fade, HOLD_MS - 150); setTimeout(()=>{ try{ sx.pause(); }catch(e){} }, HOLD_MS);
        }catch(e){} }
        if(!guided){
          report(it, true);
          GameBus.emit(d.signal_name || "story_question_first_try", { slide_id: slide.id, phase: slide.phase, value: true,
            first_try: state.attempts === 0, attempts: state.attempts + 1, scaffold_level: state.scaffoldLevel, latency_ms: Date.now() - state.slideStart });
        }
        after(HOLD_MS, ()=>{
          hold = false;
          sfxCorrect(); confettiCannon();
          if(guided){ setSwMood("talk"); after(700, ()=> completeSlide(false)); return; }
          playCorrectSelect(it.cell); setSwMood("happy");
          say(it, ()=> after(700, ()=> completeSlide(true)));
        });
      }
    }
  },

"""
js = sub1(js, r"^  PHASE_TRANSITION: \{", lambda m: sent_mod + m.group(0), re.M, "PHASE_TRANSITION anchor (sent)")
# [letter-fig] LETTER_STORY: the thought-cloud letter page (see the card note above). The page is the frames' 1280x720 px in
# the whole-stage frame (.sfig-full); every visual beat starts on its sound's "playing" event (or 150 ms in, if the browser
# will not say), so picture and sound stay together; the piano loop ducks the engine's own background music while it plays.
letter_mod = r"""  /* ===== [letter-fig] LETTER_STORY — the thought-cloud letter page (FLN-by-MJ frames 538:2 -> 538:35 -> 538:39 -> 558:2 ->
     610:6), after P2's round gate. Self-driving, no आगे: the only tap is the envelope. 1. the girl writing (538:2) with the
     magic shimmer; after 2 s the thinking girl (538:35) fades in. 2. three thought bubbles pop, the grandfather cloud grows in
     slowly (538:39) and the piano loop starts. 3. [letter-idea] the chime, as soon as the cloud has stood: on its "ummm" the
     cloud and the bubbles leave and the girl is pensive (scene C, no cloud); on its "aahaha" she brightens again and the same
     cloud grows in once more, white, with the letter (558:2's size) growing in it; it pulses and waits for the tap. 4. the tap:
     the pop, the envelope zooms to 610:6 over the
     blurred room, the seal pops, the flap swings open on the paper crackle, the sheet rises, a veil — then the next page. The
     timings live in data.pace (ms), the places in data.layout (frame px). ===== */
  LETTER_STORY: {
    mount(host, slide){
      const d = slide.data || {}, L = d.layout || {}, P = Object.assign({ a_hold: 2000, xfade: 650, bub_start: 2600, bub_gap: 230,
        cloud_start: 3300, cloud_in: 1600, hold: 2600, hum_at: 0, aha_at: 2370, rebub_gap: 160, letter_in: 1300, zoom: 1200, paper_at: 350, dive_at: 700, dive: 1700,
        dive_scale: 5.2, veil_at: 1900, done_at: 2450 }, d.pace || {});
      const A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const sfx = d.sfx || {}, env = d.env || {};
      const cl = L.cloud || [862.09, 8.61, 314.5], bubs = L.bubbles || [], li = L.letter || [1020, 166, 189], full = L.full || [71, -50, 1138, 758],
            mo = L.mouth || [568.8, 292.4];
      const fig = sfigMount(host,
        '<div class="ltr">' +
          '<img class="ltr-scene a" src="' + imgSrc(d.scene_a) + '" alt="" draggable="false">' +
          '<img class="ltr-scene b" src="' + imgSrc(d.scene_b) + '" alt="" draggable="false">' +
          '<img class="ltr-scene c" src="' + imgSrc(d.scene_c) + '" alt="" draggable="false">' +
          bubs.map(b=> '<span class="ltr-bub" style="left:' + (b[0] - b[2] / 2) + 'px;top:' + (b[1] - b[2] / 2) + 'px;width:' + b[2] + 'px;height:' + b[2] + 'px"></span>').join("") +
          '<div class="ltr-cloud" style="left:' + cl[0] + 'px;top:' + cl[1] + 'px;width:' + cl[2] + 'px;height:' + cl[2] + 'px">' +
            '<img class="ltr-cg" src="' + imgSrc(d.cloud) + '" alt="" draggable="false"><img class="ltr-cw" src="' + imgSrc(d.cloud_white) + '" alt="" draggable="false"></div>' +
          '<img class="ltr-blur" src="' + imgSrc(d.blur) + '" alt="" draggable="false">' +
          '<div class="ltr-env-pos" role="button" aria-label="पत्र" style="left:' + full[0] + 'px;top:' + full[1] + 'px;width:' + full[2] + 'px;height:' + full[3] + 'px">' +
            '<div class="ltr-env-grow"><div class="ltr-env-pulse"><div class="ltr-env3d">' +
              '<img class="ltr-inner" src="' + imgSrc(env.inner) + '" alt="" draggable="false">' +
              '<div class="ltr-paper"></div>' +
              '<img class="ltr-body" src="' + imgSrc(env.body) + '" alt="" draggable="false">' +
              '<div class="ltr-flap"><img src="' + imgSrc(env.flap) + '" alt="" draggable="false"></div>' +
              '<img class="ltr-heart" src="' + imgSrc(env.heart) + '" alt="" draggable="false">' +
            '</div></div></div>' +
          '</div>' +
          '<div class="ltr-veil"></div>' +
        '</div>');
      const card = host.closest(".tut-card"); if(card) card.classList.add("sfig-full");
      const root = fig.querySelector(".ltr"), envPos = fig.querySelector(".ltr-env-pos"), cloud = fig.querySelector(".ltr-cloud"),
            bubEls = Array.from(fig.querySelectorAll(".ltr-bub"));
      // the envelope's icon state = the full-screen box (610:6) scaled down into the cloud at 558:2's size, so the zoom moves the same element
      const s = li[2] / full[2];
      envPos.style.setProperty("--ltr-icon", "translate(" + (li[0] - li[2] / 2 - full[0]) + "px, " + (li[1] - (li[2] * full[3] / full[2]) / 2 - full[1]) + "px) scale(" + s + ")");
      // [letter-idea] the letter grows in WITH the cloud: the cloud's entrance (the CSS: scale .55 and a (-30,40) slide about its
      // 12% 92% corner) written in the box's own px — that corner and that slide at 1/s — on a wrapper inside the icon, so the
      // cloud and the letter in it move as one
      envPos.style.setProperty("--ltr-go", ((cl[0] + 0.12 * cl[2] - (li[0] - li[2] / 2)) / s) + "px " + ((cl[1] + 0.92 * cl[2] - (li[1] - (li[2] * full[3] / full[2]) / 2)) / s) + "px");
      envPos.style.setProperty("--ltr-gt", (-30 / s) + "px, " + (40 / s) + "px");
      // [letter-dive] the opening is a whole-screen transition: the view dives INTO the open envelope, onto the sheet — the box
      // scaled by dive_scale about the mouth's centre (layout.mouth, box px: the incentre of the triangle top edge / fold apex,
      // the sheet behind it), which lands on the frame's centre, so at the end only the sheet is on the screen
      const ds = P.dive_scale;
      envPos.style.setProperty("--ltr-dive", "translate(" + (640 - full[0] - ds * mo[0]) + "px, " + (360 - full[1] - ds * mo[1]) + "px) scale(" + ds + ")");
      envPos.style.setProperty("--ltr-dive-ms", P.dive + "ms");
      state.ownsAudio = true; state.demoRunning = true; setNavActive(false); $("navBtn").style.display = "none";
      const alive = ()=> fig.isConnected && CARD.slides[state.idx] === slide;
      const timers = []; const at = (ms, fn)=> timers.push(setTimeout(()=>{ if(alive()) fn(); }, ms));
      const sounds = []; let fadeFrame = 0;
      // every sound of the page is fetched and decoded now, at mount, so that later play() starts it on its beat — online too
      const pre = {};
      [sfx.magic, sfx.idea, sfx.pop, sfx.paper, d.music].forEach(id=>{ const src = A(id); if(!src) return;
        try{ const a = new Audio(src); a.preload = "auto"; a.load(); pre[id] = a; sounds.push(a); }catch(e){} });
      // a sound; onStart runs when it is actually heard (or 150 ms in, if the browser gives no "playing" / refuses to play)
      const sound = (id, vol, onStart, loop)=>{
        const src = A(id); let started = false;
        const go = ()=>{ if(started) return; started = true; if(onStart && alive()) onStart(); };
        if(!src){ setTimeout(go, 0); return null; }
        const a = pre[id] || new Audio(src); delete pre[id]; a.volume = isMuted ? 0 : vol; a.loop = !!loop; if(!sounds.includes(a)) sounds.push(a);
        a.addEventListener("playing", go, { once: true });
        const p = a.play(); if(p && p.catch) p.catch(()=> go());
        setTimeout(go, 150);
        return a;
      };
      const fadeTo = (a, target, ms, then)=>{
        if(!a){ if(then) then(); return; }
        cancelAnimationFrame(fadeFrame); const from = a.volume, t0 = performance.now();
        const tick = (now)=>{ const t = Math.max(0, Math.min(1, (now - t0) / ms)); a.volume = isMuted ? 0 : from + (target - from) * t;   // rAF's stamp can precede t0 by a frame: never under 0 (a negative volume throws)
          if(t < 1) fadeFrame = requestAnimationFrame(tick); else if(then) then(); };
        fadeFrame = requestAnimationFrame(tick);
      };
      let music = null;
      const bgmBack = ()=> fadeBackgroundMusic(isPlaying ? BGM_VO_VOLUME : BGM_VOLUME);
      // clearHost runs this when the page is left (the next page, the dev nav): every timer and sound stops, the music comes back
      window.oceanCleanup = ()=>{ timers.forEach(clearTimeout); cancelAnimationFrame(fadeFrame);
        sounds.forEach(a=>{ try{ a.pause(); a.removeAttribute("src"); a.load(); }catch(e){} }); bgmBack(); state.demoRunning = false; };
      // 1. the girl writing (538:2) with the shimmer; after a_hold the thinking girl (538:35) fades in over her
      sound(sfx.magic, 0.6, null);
      at(P.a_hold, ()=> root.classList.add("b-in"));
      // 2. the thought bubbles pop one by one (nearest the head first), then the cloud grows in slowly; the piano loop starts with it
      bubEls.forEach((b, k)=> at(P.bub_start + k * P.bub_gap, ()=> b.classList.add("in")));
      at(P.cloud_start, ()=>{
        cloud.classList.add("in");
        fadeBackgroundMusic(0.02);
        music = sound(d.music, 0.0001, ()=> fadeTo(music, 0.45, 1200), true);
      });
      // 3. [letter-idea] the chime, the moment the cloud has stood its hold; its beats hang on the sound's own start: on the "ummm"
      //    (hum_at) the cloud shrinks back into the bubbles' corner and the bubbles pop out while the girl's pensive face fades over
      //    the room (scene C, no cloud); the bubbles pop again just ahead of the "aahaha", and on it (aha_at) her bright face is back
      //    and the SAME cloud grows in again — swapped to white while it was out — with the letter growing in it; then it pulses
      const tIdea = P.cloud_start + P.cloud_in + P.hold;
      at(tIdea, ()=> sound(sfx.idea, 0.7, ()=>{
        at(P.hum_at, ()=>{ cloud.classList.remove("in"); cloud.classList.add("out"); bubEls.forEach(b=> b.classList.remove("in")); root.classList.add("c-in"); });
        bubEls.forEach((b, k)=> at(P.aha_at - (bubEls.length - k) * P.rebub_gap, ()=> b.classList.add("in")));
        at(P.aha_at, ()=>{
          cloud.classList.add("white"); cloud.classList.remove("out"); cloud.classList.add("in");   // the same entrance as the grandfather's, white
          root.classList.remove("c-in"); root.classList.add("letter-in");                            // her bright face; the letter grows with the cloud
        });
        at(P.aha_at + P.letter_in + 100, ()=>{ root.classList.add("ready"); state.demoRunning = false; });
      }));
      // 4. the tap: the pop, the zoom to 610:6 over the blurred room (the loop fades out), then the opening and the next page
      let tapped = false;
      envPos.onclick = ()=>{
        if(tapped || !root.classList.contains("ready") || !alive()) return;
        tapped = true; state.demoRunning = true;
        root.classList.remove("ready"); root.classList.add("zoom");
        GameBus.emit("letter_opened", { slide_id: slide.id });
        sound(sfx.pop, 0.7, null);
        fadeTo(music, 0, 1300, ()=>{ if(music) music.pause(); bgmBack(); });
        at(P.zoom, ()=>{
          sound(sfx.paper, 0.7, ()=> root.classList.add("open"));        // the seal pops and the flap swings open as the paper crackles
          at(P.paper_at, ()=> root.classList.add("paper"));               // the sheet rises out of the pocket
          at(P.dive_at, ()=> root.classList.add("dive"));                 // the view dives into the envelope, onto the sheet: the whole screen
          at(P.veil_at, ()=> root.classList.add("veil"));
          at(P.done_at, ()=>{ state.demoRunning = false; completeSlide(true); });
        });
      };
    }
  },

"""
js = sub1(js, r"^  PHASE_TRANSITION: \{", lambda m: letter_mod + m.group(0), re.M, "PHASE_TRANSITION anchor (letter)")
stamp_mod = r"""  /* ===== [stamp-fig] STAMP_DEMO — L2, the stamp page after the letter (FLN-by-MJ frames 565:28 and 579:47, "G3 guided story
     question"): a sentence on a sheet on the wooden table, a tray with two stamps, the demos' title bar (.dmf-band). It drives
     itself: 1. the table, under the letter page's veil as it lifts, then the title bar appears the moment its line starts to
     sound (the demos' rule); 2. the sheet settles onto the table and the tray slides up; then ROUND BY ROUND (data.rounds,
     [stamp-rounds]): 3. the round's two stamps pop into the tray, each on its pop; 4. the sentence is read without a pause,
     WORD BY WORD on the clip's clock; 5. the empty slot appears and blinks for 3.5 s (the demos' three slow blinks) — from now
     on the two stamps are the child's to drag; 6. [stamp-drag] the guidance, 0.5 s after the blink: the right stamp lifts,
     glides slowly over the slot, hovers and glides home WITHOUT printing; it comes again after every 7 s without a touch. A
     stamp dropped off the slot, or the wrong one on it: the kit's buzz, a wiggle, back it glides. The right stamp on the slot:
     it snaps over the slot and presses on the thud — the mark is printed on the slot's CENTRE (its ink, as on the demos) —
     lifts and glides home; the slot's box goes on the correct chime, the mark stays; the kit's confetti on its sound. With a
     round to follow: the stamps shrink away (their pop played backwards), the sentence goes word by word in reverse with the
     slot and its mark, and the next round's stamps pop in (3. again) — a round without `guide` has NO guidance [stamp-remind]:
     after 7 s without a touch the title's line is said again instead (and again after every further 7 s). A round with TWO
     slots or more (data.slots, frames 593:130 and 593:151): all blink together; the right stamp on one prints there and that
     box goes on the chime, then the stamps are the child's again for the rest; the confetti after the last. A slot may want
     its own stamp (sl.mark, sl.pick — 593:151: the comma, the ?, the danda twice). data.sign: small text lines (the letter's
     sign-off) shown with the sentence's last word, gone with it. After the LAST round's confetti [stamp-final] the finale: the
     stage dissolves slowly into the final picture (images.final) over fin_fade as its chime sounds, the envelope in it glitters
     gold (a glow and fin_sparks sparks over layout.envelope) for fin_glitter_ms on the second chime, and at fin_done the page
     moves on (no आगे). Places in frame px (data.layout, each round's boxes), moments in data.pace (ms). ===== */
  STAMP_DEMO: {
    mount(host, slide){
      const d = slide.data || {}, LY = d.layout || {}, im = d.images || {}, sfx = d.sfx || {};
      const rounds = Array.isArray(d.rounds) && d.rounds.length ? d.rounds : [{}];
      const P = Object.assign({ intro_at: 400, after_intro: 500, sheet_in: 0, tray_in: 150, stamps_at: 700, pop_gap: 350, sent_at: 700, blink_ms: 3500,
        hint_at: 500, glide: 1500, hover_up: 34, hold: 450, back: 1100, idle_ms: 7000, tol_x: 50, tol_y: 70, tap_px: 10, wiggle: 450, reset: 500,
        snap: 220, press: 140, press_down: 20, thud_at: 280, mark_at: 400, lift_at: 560, back_at: 800, back_home: 800, gone_at: 1600, confetti_at: 2100, done_at: 4400,
        words_out: 40, next_at: 1300, fin_fade: 3000, fin_glitter_at: 3400, fin_glitter_ms: 1300, fin_sparks: 16, fin_done: 5400 }, d.pace || {});
      const A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const sh = LY.sheet || [355, 64, 571, 594], tr = LY.tray || [427, 565, 426, 142];
      const box = (b)=> 'left:' + b[0] + 'px;top:' + b[1] + 'px;width:' + b[2] + 'px;height:' + b[3] + 'px';
      const BX0 = [[532, 541, 74, 116], [677, 540, 72, 115]], TIPS0 = [[36, 113], [35, 114]];
      const boxes0 = rounds[0].boxes || BX0, maxN = Math.max(1, ...rounds.map(R=> (R.stamps || []).length));   // divs for the most stamps any round has
      const fig = sfigMount(host,
        '<div class="stp" data-round="0">' +
          '<img class="stp-wood" src="' + imgSrc(im.wood) + '" alt="" draggable="false">' +
          '<div class="dmf-band"><div class="dmf-pill"><p></p></div><div class="dmf-head"><img src="assets/UI/demo1_head.webp" alt="" draggable="false"></div></div>' +
          '<img class="stp-sheet" src="' + imgSrc(im.sheet) + '" alt="" draggable="false" style="' + box(sh) + '">' +
          '<img class="stp-tray" src="' + imgSrc(im.tray) + '" alt="" draggable="false" style="' + box(tr) + '">' +
          Array.from({ length: maxN }, (_, k)=> '<div class="stp-stamp s' + k + '" style="' + (k < (rounds[0].stamps || []).length ? box(boxes0[k] || boxes0[0]) : 'display:none') + '"><img src="' + (rounds[0].stamps && rounds[0].stamps[k] ? imgSrc(rounds[0].stamps[k]) : '') + '" alt="" draggable="false"></div>').join('') +
          '<div class="stp-veil"></div>' +
        '</div>');
      const card = host.closest(".tut-card"); if(card) card.classList.add("sfig-full");
      const root = fig.querySelector(".stp"), band = fig.querySelector(".dmf-band"), sheet = fig.querySelector(".stp-sheet"), tray = fig.querySelector(".stp-tray"),
            stamps = Array.from(fig.querySelectorAll(".stp-stamp")), veil = fig.querySelector(".stp-veil");
      fig.querySelector(".dmf-pill p").textContent = d.band_hi || "";
      state.ownsAudio = true; state.demoRunning = true; setNavActive(false); $("navBtn").style.display = "none";
      setSwMood("talk");
      const alive = ()=> fig.isConnected && CARD.slides[state.idx] === slide;
      const timers = []; const at = (ms, fn)=> timers.push(setTimeout(()=>{ if(alive()) fn(); }, ms));
      // the page's own sounds (two pops, the thud), fetched now so each starts on its beat — online too; every round's pictures and
      // clip fetched now too, so a round starts without a load gap
      const sounds = [];
      const mk = (id)=>{ const src = A(id); if(!src) return null; try{ const a = new Audio(src); a.preload = "auto"; a.load(); sounds.push(a); return a; }catch(e){ return null; } };
      const pops = Array.from({ length: maxN }, ()=> mk(sfx.pop)), thud = mk(sfx.press), finSnd = mk(sfx.final), glitSnd = mk(sfx.glitter);   // [stamp-final] the finale's two chimes
      [A(d.intro_audio)].concat(rounds.map(R=> A(R.sentence && R.sentence.audio))).forEach(src=>{ if(src) try{ new Audio(src).load(); }catch(e){} });
      rounds.forEach(R=> (R.stamps || []).forEach(id=>{ try{ const i = new Image(); i.src = imgSrc(id); }catch(e){} }));
      if(im.final) try{ const i = new Image(); i.src = imgSrc(im.final); }catch(e){}   // [stamp-final] the final picture, fetched now
      const sound = (a, vol)=>{ if(!a) return; try{ a.volume = isMuted ? 0 : vol; a.currentTime = 0; const p = a.play(); if(p && p.catch) p.catch(()=>{}); }catch(e){} };
      // clearHost runs this when the page is left (the next page, the dev nav): every timer and sound stops
      window.oceanCleanup = ()=>{ timers.forEach(clearTimeout); if(idleIv) clearInterval(idleIv); sounds.forEach(a=>{ try{ a.pause(); a.removeAttribute("src"); a.load(); }catch(e){} });
        if(drag){ try{ drag.el.releasePointerCapture(drag.id); }catch(e){} drag = null; } state.demoRunning = false; };
      // plays a clip and reports, on the clip's own clock, how many of `times` it has reached (the demos' narrate); onEnd runs
      // once — a clip that never reports its end is stopped by the watchdog, so the page never strands
      const narrate = (src, times, onIndex, onEnd)=>{
        const began = Date.now(); let done = false, last = -1;
        const end = ()=>{ if(done || !alive()) return; done = true; if(times.length && last < times.length){ last = times.length; onIndex(last); } onEnd(); };
        play(src, end);
        const file = src ? src.split("/").pop() : "";
        const lastT = times.length ? times[times.length - 1] : authoredVoHoldMs(src) / 1000;
        setTimeout(()=>{ if(!done && alive()){ stopAudio(); end(); } }, (lastT + 10) * 1000);
        const tick = ()=>{
          if(done || !alive()) return;
          const a = currentAudio;
          const own = !!a && decodeURIComponent(String(a.currentSrc || a.src || "").split("/").pop()) === file;
          const t = own ? a.currentTime : (Date.now() - began) / 1000;
          let n = 0; while(n < times.length && t + 0.04 >= times[n]) n++;
          if(n !== last){ last = n; onIndex(n); }
          if(n < times.length) nextFrame(tick);
        };
        if(times.length) tick();
      };
      // [stamp-rounds] the round at hand (R): its sentence — p.stp-sent built by sfigLine (a word span per word, <br> per row) with
      // the gap span where the slot sits —, its slot with the mark, its stamps' pictures and boxes, the right stamp and its two
      // places over the slot: its print point (the middle of its face's bottom edge, in its box: tips) lands press_down px under
      // the slot's centre (the stamp standing on the slot) after hovering hover_up px above that
      let R = null, r = -1;
      // the slot's dashed stroke, one line per side carrying the render's own dash runs ([margin, dash, gap, ...]); the rounded
      // corners stay open, as in the render (the demos' way)
      const da = (q)=> q && q.length ? '0 ' + q.join(' ') : '10 5';
      const side = (x1, y1, x2, y2, q)=> '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke-dasharray="' + da(q) + '"/>';
      function setRound(i){
        r = i; root.dataset.round = i;
        const D = rounds[i] || {}, S = D.sentence || {}, bx = D.boxes || BX0, tips = D.tips || TIPS0,
              se = D.sent || { x: 63, y: 338, w: 1075, h: 48, size: 30 },
              sls = Array.isArray(D.slots) && D.slots.length ? D.slots : [D.slot || { x: 751, y: 331, w: 36, h: 58 }];   // the round's slots: one, or two (frame 593:130)
        const n = (D.stamps || []).length;   // this round's stamps; the divs beyond them are hidden
        stamps.forEach((s, k)=>{ s.className = "stp-stamp s" + k; if(k < n){ s.style.cssText = box(bx[k] || bx[0]); s.querySelector("img").src = imgSrc(D.stamps[k]); } else s.style.cssText = "display:none"; });
        const rows = String(S.text_hi || "").split("\n").length, lh = se.lh || Math.round(se.size * 1.714 * 10) / 10;   // Baloo Bhai 2's line box, as on every Figma page
        const sentEl = document.createElement("p"); sentEl.className = "stp-sent";
        sentEl.style.cssText = 'left:' + se.x + 'px;top:' + (se.y - (lh * rows - se.h) / 2) + 'px;width:' + se.w + 'px;height:' + (lh * rows) + 'px;font-size:' + se.size + 'px;line-height:' + lh + 'px';
        const pick = D.pick != null ? D.pick : 1, stamp = stamps[pick] || stamps[0], tip = tips[pick] || tips[0], sb = bx[pick] || bx[0];
        // each slot: its box with the render's dash runs and its mark (its own, or the round's), its right stamp (its own pick, or
        // the round's) and that stamp's two places over it — HOVER (its print point hover_up px above the slot's centre) and PRESS
        // (press_down px under it: the stamp standing on the slot)
        const slots = sls.map(sl=>{ const w = sl.w, h = sl.h, el = document.createElement("div"); el.className = "stp-slot"; el.style.cssText = box([sl.x, sl.y, w, h]);
          const pk = sl.pick != null ? sl.pick : pick, st = stamps[pk] || stamps[0], tp_ = tips[pk] || tips[0], sb_ = bx[pk] || bx[0];
          el.innerHTML = '<svg width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '" aria-hidden="true">' +
              side(0, 1, w, 1, sl.dash_h) + side(w - 1, 0, w - 1, h, sl.dash_v) + side(0, h - 1, w, h - 1, sl.dash_h) + side(1, 0, 1, h, sl.dash_v) + '</svg>' +
              '<span class="stp-mark" style="font-size:' + se.size + 'px">' + (sl.mark || D.mark || '?') + '</span>';
          const dx = sl.x + w / 2 - (sb_[0] + tp_[0]), dy = sl.y + h / 2 + P.press_down - (sb_[1] + tp_[1]);
          return { sl, w, h, el, mark: el.querySelector(".stp-mark"), done: false, pick: pk, stamp: st,
                   HOVER: "translate(" + dx + "px, " + (dy - P.hover_up) + "px) scale(1.08)", PRESS: "translate(" + dx + "px, " + dy + "px) scale(1)" }; });
        // the sign-off (data.sign): small lines under the sentence, shown with its last word
        const signs = (Array.isArray(D.sign) ? D.sign : []).map(sg=>{ const el = document.createElement("p"); el.className = "stp-sign";
          el.style.cssText = 'left:' + sg.x + 'px;top:' + sg.y + 'px;width:' + sg.w + 'px;height:' + sg.h + 'px;font-size:' + sg.size + 'px;line-height:' + sg.h + 'px'; el.textContent = sg.text || ""; return el; });
        root.insertBefore(sentEl, veil); slots.forEach(o=> root.insertBefore(o.el, veil)); signs.forEach(el=> root.insertBefore(el, veil));
        const L = sfigLine(sentEl, S.text_hi, S.word_times, S.audio, S.word_end);
        const gapEl = (wpx)=>{ const g = document.createElement("span"); g.className = "stp-gap"; g.style.width = wpx + "px"; return g; };
        if(se.gap && L.words[se.gap.before]) L.words[se.gap.before].before(gapEl(se.gap.w));   // the room the slot sits in
        if(se.tail) sentEl.appendChild(gapEl(se.tail));                                           // the frame's trailing space: the last row centres a little left
        const s0 = slots[0];   // the first slot's box and places stand for the round's (the guidance glides to it)
        R = { D, S, n, bx, tips, slots, signs, sl: s0.sl, w: s0.w, h: s0.h, sentEl, slot: s0.el, mark: s0.mark, L, pick, stamp, HOVER: s0.HOVER, PRESS: s0.PRESS };
        live = false; acted = false; solved = false; hinting = false; hintT = []; lastAct = Date.now();
      }
      // 1. the table shows as the letter page's veil lifts; then the title bar appears the moment its line starts to sound
      nextFrame(()=> nextFrame(()=>{ if(alive()) root.classList.add("lit"); }));
      const introSrc = A(d.intro_audio);
      at(P.intro_at, ()=>{
        const showBand = ()=>{ if(alive()) band.classList.add("in"); };
        let introDone = false;
        const afterIntro = ()=>{ if(introDone || !alive()) return; introDone = true; showBand(); at(P.after_intro, stage2); };
        play(introSrc, afterIntro);
        const a0 = currentAudio;
        const whenSounding = ()=>{ if(!alive() || band.classList.contains("in")) return; if(a0 === currentAudio && a0.currentTime > 0) showBand(); else nextFrame(whenSounding); };
        if(a0 && introSrc && decodeURIComponent(String(a0.src).split("/").pop()) === introSrc.split("/").pop()) whenSounding(); else showBand();
        at(1500, showBand);   // a clip that is slow to start never keeps the bar away
        at(authoredVoHoldMs(introSrc) + 10000, ()=>{ if(!introDone){ stopAudio(); afterIntro(); } });
      });
      // 2. the sheet settles onto the table, the tray slides up under it; the first round is set
      function stage2(){
        at(P.sheet_in, ()=> sheet.classList.add("in"));
        at(P.tray_in, ()=> tray.classList.add("in"));
        at(P.stamps_at, ()=>{ setRound(0); stage3(); });
      }
      // 3. the round's stamps (two, or three) pop into the tray, each on its pop
      function stage3(){
        const n = R.n;
        stamps.slice(0, n).forEach((s, k)=> at(k * P.pop_gap, ()=>{ const img = s.querySelector("img"); sound(pops[k], 0.48);   // 60 % of the first build's .8
          img.addEventListener("animationend", ()=>{ img.classList.remove("pop"); img.classList.add("shown"); }, { once: true }); img.classList.add("pop"); }));
        at((n - 1) * P.pop_gap + P.sent_at, stage4);
      }
      // 4. the sentence rises in whole — the sign-off (593:151) with it — and is read SENT_IN_MS later, each word lit as it is read ([word-sync])
      function stage4(){ const C = R, L = C.L; sfigRise(L, C.signs); at(SENT_IN_MS, ()=>{ narrate(L.src, [], ()=>{}, stage5); sfigSync(L); }); }
      // 5. the empty slot appears and blinks (3.5 s: three slow blinks, the demos' dmfBlink); from this moment the two stamps are the child's
      //    to drag (.live); in a round with `guide`, 0.5 s after the blink the guidance, unless the child has already taken hold of a stamp
      function stage5(){
        const slots = R.slots, guide = R.D.guide !== false;
        slots.forEach(o=>{ o.el.style.animationDuration = (P.blink_ms / 3) + "ms"; o.el.classList.add("in", "blink"); });   // both together, when there are two
        live = true; root.classList.add("live"); lastAct = Date.now();
        at(P.blink_ms, ()=> slots.forEach(o=> o.el.classList.remove("blink")));
        if(guide) at(P.blink_ms + P.hint_at, ()=>{ if(!acted) hint(); });
        // after idle_ms without a touch: the guidance again (the count starts over after a drop and after each guidance) — or, in a
        // round without guidance [stamp-remind], the title's line again (the count starts over after it)
        if(idleIv) clearInterval(idleIv);
        idleIv = setInterval(()=>{
          if(!alive()){ clearInterval(idleIv); return; }
          if(!live || solved) return;
          if(drag || hinting || (!guide && isPlaying)){ lastAct = Date.now(); return; }
          if(Date.now() - lastAct >= P.idle_ms){ if(guide) hint(); else remind(); }
        }, 200);
      }
      // [stamp-remind] the title's line said again (never over another clip, never with a stamp in hand); the idle count starts over
      function remind(){
        if(solved || drag || !live || isPlaying){ lastAct = Date.now(); return; }
        lastAct = Date.now(); play(introSrc, ()=>{ lastAct = Date.now(); });
      }
      // [stamp-drag] the page's state: live = the stamps take drags; acted = the child has taken hold of one; drag = the drag in hand
      let live = false, acted = false, solved = false, hinting = false, drag = null, idleIv = null, lastAct = 0, hintT = [];
      const move = (el, tf, ms, ease)=>{ el.style.transition = "transform " + ms + "ms " + ease + ", filter .3s"; el.style.transform = tf; };
      // glides a stamp home and sets it down (its shadow goes as it lands) — unless the child has taken hold of it again
      const putBack = (s, ms)=>{ move(s, "none", ms, "cubic-bezier(.4,0,.2,1)"); at(Math.max(0, ms - 150), ()=>{ if(!(drag && drag.el === s)) s.classList.remove("lift"); }); };
      // 6. the guidance: the right stamp lifts, glides SLOWLY over the slot, hovers there and glides home — it does not print (that
      //    is the child's to do); stopped where it is the moment the child takes hold of a stamp
      const hat = (ms, fn)=>{ const id = setTimeout(()=>{ if(alive() && hinting) fn(); }, ms); hintT.push(id); timers.push(id); };
      function hint(){
        if(hinting || solved || drag || !live || !R || R.D.guide === false) return;
        const stamp = R.stamp; hinting = true; hintT = [];
        stamp.classList.add("lift"); move(stamp, R.HOVER, P.glide, "cubic-bezier(.45,0,.2,1)");
        hat(P.glide + P.hold, ()=> move(stamp, "none", P.back, "cubic-bezier(.4,0,.2,1)"));
        hat(P.glide + P.hold + P.back - 150, ()=> stamp.classList.remove("lift"));
        hat(P.glide + P.hold + P.back + 50, ()=>{ hinting = false; lastAct = Date.now(); });
      }
      function stopHint(taken){   // taken = the child took hold of the guiding stamp itself (it stays where it is, in hand)
        if(!hinting) return; hinting = false; hintT.forEach(clearTimeout); hintT = [];
        if(!taken) putBack(R.stamp, 350);
      }
      // the child's drags: a stamp follows the finger from where it is (even mid-guidance, mid-return) at the lifted size; the
      // frame's px from the screen's through the stage's scale; the drop is judged by the stamp's PRINT POINT against the slot
      const scaleNow = ()=> (root.getBoundingClientRect().width || 1280) / 1280;
      const curXY = (el)=>{ const m = getComputedStyle(el).transform, v = m && m !== "none" ? m.match(/matrix\(([^)]+)\)/) : null;
        if(!v) return [0, 0]; const a = v[1].split(",").map(Number); return [a[4] || 0, a[5] || 0]; };
      const setTf = (el, tx, ty, s)=>{ el.style.transform = "translate(" + tx.toFixed(2) + "px, " + ty.toFixed(2) + "px) scale(" + s + ")"; };
      stamps.forEach((s, k)=>{
        s.addEventListener("pointerdown", (e)=>{
          if(!live || solved || drag || !R || (e.button != null && e.button > 0)) return;
          e.preventDefault(); acted = true; lastAct = Date.now();
          if(hinting) stopHint(s === R.stamp);
          const xy = curXY(s); s.style.transition = "none"; s.classList.remove("stp-wrong"); s.classList.add("lift", "drag"); setTf(s, xy[0], xy[1], 1.08);
          drag = { el: s, k, id: e.pointerId, x0: e.clientX, y0: e.clientY, tx: xy[0], ty: xy[1], sc: scaleNow(), moved: 0, lx: xy[0], ly: xy[1] };
          try{ s.setPointerCapture(e.pointerId); }catch(err){}
        });
        s.addEventListener("pointermove", (e)=>{
          if(!drag || drag.el !== s || e.pointerId !== drag.id) return;
          const dx = (e.clientX - drag.x0) / drag.sc, dy = (e.clientY - drag.y0) / drag.sc;
          drag.moved = Math.max(drag.moved, Math.hypot(dx, dy)); drag.lx = drag.tx + dx; drag.ly = drag.ty + dy;
          setTf(s, drag.lx, drag.ly, 1.08);
        });
        const up = (e)=>{
          if(!drag || drag.el !== s || e.pointerId !== drag.id) return;
          const dr = drag; drag = null; try{ s.releasePointerCapture(e.pointerId); }catch(err){}
          s.classList.remove("drag"); lastAct = Date.now();
          if(e.type === "pointercancel" || dr.moved < P.tap_px){ putBack(s, 220); return; }   // a touch (or the browser took the pointer), not a placing
          const b = R.bx[k] || R.bx[0], tp = R.tips[k] || R.tips[0], tipX = b[0] + tp[0] + dr.lx, tipY = b[1] + tp[1] + dr.ly;   // the stamp scales about its base: the tip rides the translate
          // the slot the print point is on: of the slots still empty, one within tol_x / tol_y of it (the nearer, when both are)
          const dist = (o)=> Math.hypot(tipX - (o.sl.x + o.w / 2), tipY - (o.sl.y + o.h / 2));
          const hit = R.slots.filter(o=> !o.done && Math.abs(tipX - (o.sl.x + o.w / 2)) <= P.tol_x && Math.abs(tipY - (o.sl.y + o.h / 2)) <= P.tol_y).sort((a, c)=> dist(a) - dist(c))[0];
          if(hit && k === hit.pick) solve(hit); else wrong(s);
        };
        s.addEventListener("pointerup", up); s.addEventListener("pointercancel", up);
      });
      // a wrong drop (off the slot, or the wrong stamp on it): the kit's incorrect buzz (the user's standard sfx_incorrect_feedback),
      // a wiggle where it was dropped, then it glides back to its place; the stamps stay the child's. The class is stp-wrong, never
      // a bare "wrong": the engine's style.css paints ANY .wrong element white (:is(.wrong,...){background-color:#fff!important})
      function wrong(s){
        state.attempts = (state.attempts || 0) + 1; sfxWrongSoft();
        s.classList.remove("stp-wrong"); void s.offsetWidth; s.classList.add("stp-wrong");
        at(P.wiggle, ()=>{ if(!(drag && drag.el === s)){ s.classList.remove("stp-wrong"); putBack(s, P.reset); } });
      }
      // the right drop: the stamp snaps over the slot and presses onto it on the thud — the mark is printed, its ink on the slot's
      // centre — lifts and glides home; the slot's box goes on the correct chime (the user's standard sfx_correct_feedback), the
      // mark stays; the kit's confetti on its sound (the user's standard sfx confetti); then the next round, or the page moves on
      function solve(o){
        const C = R, stamp = o.stamp, last = C.slots.every(q=> q === o || q.done);   // the slot's own stamp; the round's last empty slot? (one slot: always)
        o.done = true; solved = true; live = false; root.classList.remove("live"); C.slots.forEach(q=> q.el.classList.remove("blink")); hintT.forEach(clearTimeout);
        if(last && idleIv){ clearInterval(idleIv); idleIv = null; }
        move(stamp, o.HOVER, P.snap, "cubic-bezier(.2,0,.2,1)");
        at(P.snap, ()=> move(stamp, o.PRESS, P.press, "cubic-bezier(.5,0,1,1)"));
        at(P.thud_at, ()=> sound(thud, 0.9));
        at(P.mark_at, ()=>{ centreInk(o.mark); o.mark.classList.add("in"); });
        at(P.lift_at, ()=> move(stamp, o.HOVER, 180, "cubic-bezier(0,0,.3,1)"));
        at(P.back_at, ()=> putBack(stamp, P.back_home));
        // the box goes on the chime; with a slot still empty (frame 593:130's other row) the stamps are the child's again from
        // here — no confetti yet; the idle count starts over (the title's line after 7 s, as in any later round)
        at(P.gone_at, ()=>{ o.el.classList.add("gone"); sfxCorrect(); if(!last && R === C){ solved = false; live = true; root.classList.add("live"); lastAct = Date.now(); } });
        if(!last) return;
        at(P.confetti_at, ()=> confettiCannon());
        at(P.done_at, ()=>{ if(r + 1 < rounds.length) clearRound(C); else finale(); });   // [stamp-final] after the last round, the finale
      }
      // [stamp-final] after the last round's confetti: the stage dissolves into the final picture (the girl holding up her stamped
      // letter) over fin_fade as its chime sounds (started together), the envelope glitters gold for fin_glitter_ms on the second
      // chime at fin_glitter_at, and at fin_done the page hands over to the end screen. The layer sits over everything (the title
      // bar too); its picture was fetched at mount
      function finale(){
        const EB = LY.envelope || [783, 168, 112, 102];
        const fin = document.createElement("div"); fin.className = "stp-final"; fin.style.transitionDuration = P.fin_fade + "ms";
        fin.innerHTML = '<img src="' + imgSrc(im.final) + '" alt="" draggable="false"><div class="stp-glit" style="' + box(EB) + '"></div>';
        root.appendChild(fin);
        nextFrame(()=> nextFrame(()=>{ if(!alive()) return; fin.classList.add("in"); sound(finSnd, 0.9); }));
        at(P.fin_glitter_at, ()=>{ glitter(fin.querySelector(".stp-glit"), EB[2], EB[3]); sound(glitSnd, 0.7); });
        at(P.fin_done, ()=>{ state.demoRunning = false; completeSlide(true); });
      }
      // the glitter: a soft gold glow over the envelope and fin_sparks four-point sparks scattered over it, each twinkling once (up and
      // away in .65 s) at its own moment within the chime
      function glitter(g, W, H){
        if(!g) return; let html = '<div class="stp-glow"></div>';
        for(let i = 0; i < P.fin_sparks; i++){
          const a = Math.random() * Math.PI * 2, rr = 0.3 + Math.random() * 0.7, x = W / 2 + Math.cos(a) * rr * W / 2, y = H / 2 + Math.sin(a) * rr * H / 2,
                s = 7 + Math.random() * 9, d = Math.random() * Math.max(0, P.fin_glitter_ms - 650);
          html += '<svg class="stp-spark" viewBox="0 0 24 24" aria-hidden="true" style="left:' + x.toFixed(1) + 'px;top:' + y.toFixed(1) + 'px;width:' + s.toFixed(1) + 'px;height:' + s.toFixed(1) + 'px;animation-delay:' + d.toFixed(0) + 'ms">' +
                  '<path d="M12 0L14.6 9.4 24 12 14.6 14.6 12 24 9.4 14.6 0 12 9.4 9.4Z"/><circle cx="12" cy="12" r="3"/></svg>';
        }
        g.style.setProperty("--glit", P.fin_glitter_ms + "ms"); g.innerHTML = html; g.classList.add("on");
      }
      // [stamp-rounds] between rounds: the stamps shrink away (their pop played backwards, pop_gap apart), the sentence goes word by
      // word in reverse (the arrival's opposite) and the slot's box fades with its mark; then the next round is set and its stamps pop in
      function clearRound(C){
        stamps.slice(0, C.n).forEach((s, k)=> at(k * P.pop_gap, ()=>{ const img = s.querySelector("img"); img.classList.remove("shown");
          img.addEventListener("animationend", ()=>{ img.classList.remove("unpop"); }, { once: true }); img.classList.add("unpop"); }));
        C.signs.forEach(el=> el.classList.remove("on"));   // the sign-off came with the last word: it goes first
        C.L.words.slice().reverse().forEach((wd, i)=> at(i * P.words_out, ()=> wd.classList.remove("on")));
        C.slots.forEach(o=> o.el.classList.add("out"));
        at(P.next_at, ()=>{ C.sentEl.remove(); C.slots.forEach(o=> o.el.remove()); C.signs.forEach(el=> el.remove()); setRound(r + 1); stage3(); });
      }
      // the mark's INK on the slot's centre (the demos' centreInk): the glyph's ink is not centred in its own line box, so it is
      // shifted by its ink's offset, measured from the font itself (style.css: --ix / --iy)
      function centreInk(markEl){
        try{
          const cs = getComputedStyle(markEl), c = document.createElement("canvas").getContext("2d");
          c.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
          const t = c.measureText(markEl.textContent);
          if(!t.width || !isFinite(t.fontBoundingBoxAscent)) return;
          const base = (markEl.offsetHeight - t.fontBoundingBoxAscent - t.fontBoundingBoxDescent) / 2 + t.fontBoundingBoxAscent;
          const ix = (t.actualBoundingBoxRight - t.actualBoundingBoxLeft) / 2 - markEl.offsetWidth / 2;
          const iy = base + (t.actualBoundingBoxDescent - t.actualBoundingBoxAscent) / 2 - markEl.offsetHeight / 2;
          markEl.style.setProperty("--ix", ix.toFixed(2) + "px"); markEl.style.setProperty("--iy", iy.toFixed(2) + "px");
        }catch(e){}
      }
    }
  },

"""
js = sub1(js, r"^  PHASE_TRANSITION: \{", lambda m: stamp_mod + m.group(0), re.M, "PHASE_TRANSITION anchor (stamp)")
js = sub1(js, r"^SlideModules\.MATCH_PAIRS           = SlideModules\.MATCH_THE_PAIR;",
          lambda m: m.group(0) + "\nSlideModules.SORT_WORDS            = SlideModules.SORT_QTYPE;   // [reskin] generic two-box word sort (custom data.bins), r4n", re.M, "alias block")
js = sub1(js, r"^SlideModules\.SORT_WORDS .*$",
          lambda m: m.group(0) + "\nSlideModules.PUNCT_PICK            = SlideModules.PUNCT_DEMO;   // [pick-fig] G1: the run-on demo's page with the tap left to the child", re.M, "alias block (pick)")
js = sub1(js, r'  SEQUENCE_DRAG: "drag",',
          lambda m: m.group(0) + '\n  EVIDENCE_QA: "mcq", BUILD_PUNCT: "build", SORT_QTYPE: "drag", SORT_WORDS: "drag", PUNCT_PICK: "mcq", SENT_PICK: "mcq",   /* [reskin] this lesson\'s answerable types */', 0, "QUESTION_FORMAT")
# [sent-fig] G4, P1 + P2 (SENT_PICK) repeat their instruction after every 5 s of quiet itself (the reference P4's rule), so the engine's
# one-off 7 s idle reminder stays off there; and the stage carries .sent-page for P4's look (style.css [sent-fig])
js = sub1(js, r"if\(\['MATCH_THE_PAIR','MATCH_VACHAN_PAIRS','FILL_VACHAN_DRAG'\]\.includes\(",
          "if(['MATCH_THE_PAIR','MATCH_VACHAN_PAIRS','FILL_VACHAN_DRAG','SENT_PICK','LETTER_STORY','STAMP_DEMO'].includes(", 0, "armIdleVo exclusions (sent, letter, stamp)")   # [letter-fig] no idle reminder on the story page
js = sub1(js, r'  document\.body\.classList\.toggle\("tut-page", isTut\);\n',
          lambda m: m.group(0) + '  $("stage").classList.toggle("sent-page", slide.type === "SENT_PICK");   // [sent-fig] G4, P1 + P2: the reference P4\'s header + page look\n',
          0, "mountSlide sent-page")
# [gate-p2] completeSlide opens each round's gate at the phase boundary, once per load. With CARD.round3_gate_after set, the
# round-3 gate is skipped at that boundary (G4 -> P1) and opened on that page's end instead (P2 -> P3) — and EVERY time that
# page ends (a re-run from the dev nav's list crosses it again), the way T4's gate does: round 3 is cleared there first.
js = sub1(js, r"  const nextRound = PHASE_ROUND\[next && next\.phase\], curRound = PHASE_ROUND\[slide\.phase\];\n  if\(next && nextRound && nextRound !== curRound\n",
          lambda m: '''  const nextRound = PHASE_ROUND[next && next.phase], curRound = PHASE_ROUND[slide.phase];
  /* [gate-p2] the round-3 gate ("अब आपकी बारी!") follows the page CARD.round3_gate_after (P2), not the phase boundary
     (G4 -> P1): the three P4-style pages G4, P1, P2 play as one run and the gate opens before the first builder page. It
     opens EVERY time that page ends (a re-run from the dev nav's list too), as T4's does: round 3 is cleared here first. */
  const lateGate = CARD.round3_gate_after, atLate = !!lateGate && slide.id === lateGate;
  if(atLate) _gatedPhases.delete("round3");
  const crosses = !lateGate ? nextRound !== curRound : atLate ? nextRound === "round3" : (nextRound !== curRound && nextRound !== "round3");
  if(next && nextRound && crosses
''', 0, "completeSlide round gate (gate-p2)")
# [gate-cel] the engine never opens a round gate before the CELEBRATION end screen. P2 is now the last page, so that rule would
# keep its gate shut: lifted for the round3_gate_after page alone (P2 -> the gate -> CEL); every other page keeps it.
js = sub1(js, r'     && next\.type !== "CELEBRATION" && next\.type !== "PHASE_TRANSITION"\n',
          '     && (atLate || next.type !== "CELEBRATION") && next.type !== "PHASE_TRANSITION"   /* [gate-cel] P2\'s gate opens before the end screen too */\n',
          0, "completeSlide no-gate-before-CELEBRATION rule (gate-cel)")
# [pick-fig] G1 is a guided page drawn on T4's whole-stage Figma frame (its own title bar, no engine header, no standing
# Swiftie or 🔊 chip), so it mounts in the same teaching frame the tutorial pages use; its phase stays "guided" (gates,
# idle reminder, telemetry)
js = sub1(js, r'  const isTut = \(slide\.phase === "tutorial" && ',
          '  const isTut = ((slide.phase === "tutorial" || slide.type === "PUNCT_PICK" || slide.type === "LETTER_STORY" || slide.type === "STAMP_DEMO") && ', 0, "isTut (pick, letter, stamp)")   # [letter-fig] L1 too: the whole-stage frame, no header
js = sub1(js, r'const SEL = "\.sort-item, \.dd-tile, \.cdm-objtile, \.cdm-card, \.combine-drag";',
          'const SEL = ".sort-item, .dd-tile, .cdm-objtile, .cdm-card, .combine-drag, .bp-tile, .ev-sort-item";   /* [reskin] + the punctuation / sort tiles */', 0, "drag VO gate SEL")
assert "SwiftPAL.emit(" not in js
title_js = r"""

/* ---------- [title-fig] TITLE-PAGE SWIFTIE MOVES WITH THE LANDING VO ----------
   The title page's Swiftie is the Figma frame's still "Hello" pose, which is also frame 0 and the last frame
   of the approved wave animation (new_landing_swiftee_anim.webp: 36 frames x 90 ms, plays once per load).
   She waves only while the landing greeting is actually sounding: the wave starts on the clip's first
   "playing" event, re-runs from frame 0 every 3.24 s while the line continues, and the moment the line stops
   (ended, cut by शुरू करें, or blocked by autoplay) she is back on the still Figma pose. Same rule as Swiftie
   everywhere else in the engine: she moves only while her voice is heard. */
(function(){
  const still = $("sgSwiftie"), anim = $("sgSwiftieAnim"); if(!still || !anim) return;
  const SRC = anim.dataset.src, CYCLE_MS = 36 * 90;
  let talking = false, timer = 0, watched = null, blob = null, shownUrl = null;
  // One download, then a fresh object URL per wave (a new URL is what restarts an animated image).
  // file:// pages cannot fetch(), so they fall back to a cache-busting query instead.
  if(location.protocol !== "file:"){ try{ fetch(SRC).then(r=> r.ok ? r.blob() : null).then(b=>{ blob = b; }).catch(()=>{}); }catch(e){} }
  const freshUrl = ()=> blob ? URL.createObjectURL(blob) : (SRC + "?r=" + Date.now());
  const dropUrl = (u)=>{ if(u && u.startsWith("blob:")) URL.revokeObjectURL(u); };
  const onLanding = ()=> document.body.classList.contains("is-start") && !$("startGate").classList.contains("hidden");
  const sounding = ()=>{ const a = currentAudio; return !!(isPlaying && a && !a.paused && !a.ended); };
  function rest(){
    talking = false; clearTimeout(timer); anim.onload = anim.onerror = null;
    still.classList.remove("off"); anim.classList.remove("on");
    anim.removeAttribute("src"); dropUrl(shownUrl); shownUrl = null;
  }
  function wave(){
    const url = freshUrl();
    anim.onload = ()=>{
      if(!talking) return;
      dropUrl(shownUrl); shownUrl = url;
      anim.classList.add("on"); still.classList.add("off");
      clearTimeout(timer);
      timer = setTimeout(()=>{ if(talking && sounding() && onLanding()) wave(); }, CYCLE_MS);
    };
    anim.onerror = rest;
    anim.src = url;
  }
  function talk(){ if(talking) return; talking = true; wave(); }
  function sync(){
    if(!onLanding() || !isPlaying){ if(talking) rest(); return; }
    const a = currentAudio; if(!a || talking) return;
    if(!a.paused && a.currentTime > 0){ talk(); return; }
    if(watched !== a){ watched = a;
      a.addEventListener("playing", ()=>{ if(a === currentAudio && isPlaying && onLanding()) talk(); }, { once:true }); }
  }
  // setPlaying() flips body.vo-lock at every clip start/end, and leaving the landing drops body.is-start
  new MutationObserver(sync).observe(document.body, { attributes:true, attributeFilter:["class"] });
})();
"""
js = sub1(js, r"^boot\(\);$", lambda m: m.group(0) + title_js, re.M, "boot() call")

# ---------- 5. CSS ----------
feedback_rules = ocean_css[ocean_css.index("/* Incorrect-answer feedback is motion-only"):]
fit_rules = """
/* ===== [reskin] FIT THE PORTED MODULES INTO THE REFERENCE CHROME ========================= */
/* EVIDENCE_QA option rows: the reference's later answer-card rulings fix every .opt-cell at ~230x250 and the
   themed grid gap at 30px, which outrank .ev-right's own row rules. These are sentence options (one per row), so
   the row geometry must win here. */
.stage:not(.tut) .ev-qa .ev-right .q-row .opt-cell{min-height:0 !important;height:104px !important;width:auto !important;max-width:none !important;padding:8px 22px !important;}
.stage:not(.tut) .ev-qa .ev-right .q-row .opt-grid.cols-1{grid-template-columns:minmax(0,440px) !important;gap:16px !important;}
/* Drop targets stay hit-testable while a tile's own name clip plays: the builder/sort tiles speak on
   press and drops are found with elementFromPoint, which skips pointer-events:none elements. The
   modules' own state.locked / hintActive guards still hold during feedback. */
body.vo-lock .bp-gap.dd-zone, body.vo-lock .ev-sort-bin.dd-zone{pointer-events:auto !important;}
/* Tutorial frame (.tut-card) offers ~318px of content height: compact the recap cards + the builder. */
.stage.tut .tut-prompt{white-space:normal;font-size:40px;line-height:1.15;min-height:96px;padding:10px 40px 0;}
.stage.tut .ev-recap{gap:22px;align-items:stretch;}
.stage.tut .ev-recap-card{padding:12px 16px;gap:6px;justify-content:center;}
.stage.tut .rc-ic.glyph{font-size:56px;min-width:56px;}
.stage.tut .ev-recap.n3 .rc-title{font-size:26px;}
.stage.tut .ev-recap.n3 .rc-body{font-size:19px;line-height:1.3;}
.stage.tut .ev-recap.n3 .rc-ex{font-size:18px;padding:5px 10px;}
.stage.tut .bp-stage{gap:14px;}
.stage.tut .bp-card{padding:10px 18px;gap:16px;}
.stage.tut .bp-pic{flex-basis:110px;height:110px;}
.stage.tut .bp-img{max-width:110px;max-height:110px;}
.stage.tut .bp-body{gap:8px;}
.stage.tut .bp-word{font-size:34px;}
.stage.tut .bp-tile{width:132px;height:96px;}
.stage.tut .bp-tile .bt-glyph{font-size:48px;}
.stage.tut .bp-tile .bt-name{font-size:16px;}
"""
title_css = """
/* ===== [title-fig] TITLE PAGE = the Figma "Title Page" frame (FLN-by-MJ, node 386:17) =====================
   Laid out in the frame's own 1280x720 px and scaled once onto the 1333x750 stage (1333/1280), so every
   element keeps the frame's placement and size relative to the screen. Numbers are copied from the frame;
   children of .sg-card are measured from its padding box (inside the 9px white border). The play button and
   the 🔊 chip are not in the frame: they keep their engine size in STAGE px (hence the /var(--fig-s)). */
:root{ --fig-s:1.04140625; }
body.is-start .start-bg{background-image:url("assets/UI/title_bg.png");}
/* the frame's background already carries its stars and sparkles; the drifting sky layer would double them */
body.is-start .sg-glow, body.is-start .sg-sky{display:none !important;}
.sg-fig{position:absolute;left:0;top:0;width:1280px;height:720px;transform:scale(var(--fig-s));transform-origin:0 0;}
.sg-fig img{pointer-events:none;max-width:none;}
.sg-fig .sg-card{position:absolute;left:76px;top:125px;width:1114px;height:456px;border:9px solid #FFFFFF;
  border-radius:44px;overflow:hidden;background:rgba(255,255,255,.65);box-shadow:none;display:block;gap:0;}
.sg-fig .sg-card::before{display:none;}
.sg-fig .sg-content{display:none;}          /* the title is the frame's title art now; boot() still fills #sgTitle */
.sgf-scene{position:absolute;left:-9px;top:-167px;width:1114px;height:627px;object-fit:cover;}
.sgf-question{position:absolute;left:841px;top:147px;width:138px;height:207px;object-fit:cover;}
/* frame: left calc(50%+.5px) centred, top calc(4.61% - 8.17px), bottom calc(71.27% + 3.83px), ratio 1339/248 */
.sgf-title{position:absolute;left:251.58px;top:12.02px;width:593.83px;height:109.99px;}
.sgf-shadow{position:absolute;display:block;}   /* each SVG keeps its own root size; offsets include its 25px blur bleed */
.sgf-shadow.s1{left:141px;top:303px;}          /* ellipse 166,328 82x19 */
.sgf-shadow.s2{left:473px;top:270px;}          /* ellipse 498,295 92x14 */
.sgf-shadow.s3{left:857px;top:306px;}          /* ellipse 882,331 65x19 */
.sgf-purn{position:absolute;left:97px;top:139px;width:219.473px;height:219.473px;display:flex;align-items:center;justify-content:center;}
.sgf-purn img{flex:none;width:218.993px;height:218.993px;object-fit:cover;transform:rotate(.13deg);}
.sgf-comma{position:absolute;left:502px;top:170px;width:95px;height:143px;object-fit:cover;}
.sgf-swiftie{position:absolute;left:5px;top:371px;width:245px;height:245px;object-fit:cover;z-index:2;}
/* the wave animation's frame 0 sits exactly on the still (alpha-box matched: scale .4166 of 560x550) */
.sgf-swiftie-anim{position:absolute;left:19.09px;top:376.5px;width:233.3px;height:229.14px;z-index:3;opacity:0;}
.sgf-swiftie-anim.on{opacity:1;}
.sgf-swiftie.off{opacity:0;}
.sg-fig .sg-btn{width:calc(140px / var(--fig-s));height:calc(140px / var(--fig-s));bottom:calc(27px / var(--fig-s) - 9px);}
/* the chip keeps its place on Swiftie's leg (same point of the wave art as before), straddling the card edge */
.sg-fig .sg-vo{left:172.65px;top:544.11px;bottom:auto;width:calc(58px / var(--fig-s));height:calc(58px / var(--fig-s));z-index:5;}
"""
story_css = """
/* ===== [story-fig] STORY PAGE = the Figma frames "html_Guided_instructions" (FLN-by-MJ, nodes 435:5 and 476:198)
   The first tutorial screen (STORY_LISTEN): two beats on one layout — the frames differ only in the picture
   (and its crop) and the text block. The tutorial card itself becomes the frame's card (node 435:178):
   its border box is the frame's 96,106 1088x508, and everything inside it is laid out in the frame's own px on
   .sfig-in (the card's 1064x484 padding box), scaled once by 1333/1280 like the title page. Swiftie is the
   frame's still Hello pose (the same file as the title page's). The आगे pill is not in the frame: it keeps its
   engine size, centred in the free grid under the text box. Text: Noto Sans Devanagari SemiBold 24px (bundled,
   Google Fonts' own devanagari + latin subsets), under its own family name so no other screen's font fallback
   changes.
   2026-10-21 — the card's box, Swiftie's place and the 🔊 chip follow the reference game's T1/T2 instead of
   the frame (https://hi-02-h04-l01-s01-dun.vercel.app/, measured on its stage): card 100,96 1133x562,
   Swiftie 76,472 190x190 (its start_mascot.webp is this same Hello art), chip 202,606 58x58. The picture, the
   text box and the grid keep their places on screen: .sfig-in stays where the frame's card put it, and only
   the clip grows to the bigger card. */
/* [baloo-font] (2026-10-30) every text of the lesson's own pages (T0-G3, L2) is Baloo 2 ExtraBold (800), the face of the reference
   game's Page 1 T1 (hi-02-h04-l01-s01-dun.vercel.app: its sentence is "Baloo 2" 800). It is the very font file the engine embeds
   as 'Baloo 2' 800, shipped as story_font_baloo2_800.woff2 under its own family name with Noto Sans Devanagari's line metrics
   (ascent 896 / descent 408 per 1000; Baloo's own are 1078 / 524): every line box and baseline stays where the Figma-matched
   layout put the Noto text, while the glyphs, weight and widths are Baloo's (its advances are within 2 % of Noto SemiBold's at
   the same px, so the sizes stay). Its space (0.2 em) is the frames' Baloo Bhai 2 space, so the -2 / -3 / -4 px word spacing
   that made Noto's spaces match it is gone. Was 'Story Noto Sans Devanagari' SemiBold (600), two subsets. */
@font-face{font-family:'Story Baloo 2';font-style:normal;font-weight:800;font-display:block;
  src:url("assets/UI/story_font_baloo2_800.woff2") format("woff2");ascent-override:89.6%;descent-override:40.8%;line-gap-override:0%;}
body.tut-page:has(.sfig-card), .stage.tut:has(.sfig-card){background:#F6FBFF;}
.stage.tut .slide-stage:has(.sfig-card){padding:96px 100px 92px;}     /* card border box 100,96 1133x562 (the reference's) */
/* border: the frame's 12px x 1333/1280 = 12.5px, which Chrome draws as 12px anyway (borders snap to whole pixels);
   stated as 12px so everything placed from the card's padding box below lands exactly */
.stage.tut .tut-card.sfig-card{border:12px solid #5A8FEE;border-radius:calc(40px * var(--fig-s));
  background:#F2F7FA;background-image:none;box-shadow:0 calc(8px * var(--fig-s)) calc(8.8px * var(--fig-s)) rgba(0,0,0,.25);}
.tut-card.sfig-card::after, .tut-card.sfig-card .tut-mascot{display:none;}
/* the chip is placed from the card's padding box (stage px): 202,606 on the stage */
.tut-card.sfig-card .tut-audio{left:90px;top:498px;bottom:auto;width:58px;height:58px;}
.stage.tut:has(.sfig-card) .nav-btn{bottom:138px;}
/* .sfig-in = the frame card's 1064x484 padding box, kept where the frame's card put it (that card's 96,106 x 1333/1280
   + its 12px border), so the picture, text and grid did not move when the card took the reference's box */
.sfig-in{position:absolute;left:calc(96px * var(--fig-s) - 100px);top:calc(106px * var(--fig-s) - 96px);width:1064px;height:484px;
  max-height:none;transform:scale(var(--fig-s));transform-origin:0 0;}
.sfig-in img{pointer-events:none;max-width:none;}
/* the card clips at its padding edge: the reference-sized card's padding box, in .sfig-in's frame px */
.sfig-clip{position:absolute;left:calc(100px / var(--fig-s) - 96px);top:calc(96px / var(--fig-s) - 106px);
  width:calc(1109px / var(--fig-s));height:calc(538px / var(--fig-s));overflow:hidden;border-radius:28px;}
.sfig-grid{position:absolute;width:718.497px;height:718.497px;transform:rotate(90deg);}
/* the grids keep the frame's place on screen: frame position (from the frame card's padding box) minus the
   bigger clip's offset from it */
.sfig-grid.g1{left:calc(-187px - 100px / var(--fig-s) + 96px);top:calc(-33.968px - 96px / var(--fig-s) + 106px);}   /* node 435:180 */
.sfig-grid.g2{left:calc(531.968px - 100px / var(--fig-s) + 96px);top:calc(-34px - 96px / var(--fig-s) + 106px);}    /* node 435:181 */
/* node 435:185 is 430x224 at 317,13 with a 4px stroke drawn OUTSIDE it (its render is 438x232), so the CSS
   border box grows by 4 each way and the picture still fills the full 430x224 */
.sfig-pic{position:absolute;left:313px;top:9px;width:438px;height:232px;border:4px solid #DADADA;border-radius:24px;
  overflow:hidden;background:#000;}
.sfig-pic img{position:absolute;object-fit:cover;}
/* [story-pinki] each beat's picture as its frame crops it into the 430x224 box (the image node's offset and size).
   [story-pics] (2026-10-31) the user's redrawn pictures replace all four (same files): 1 and 4 are 16:9 (1672x941 / 1672x940),
   2 and 3 the box's own 1.92 (1738x905), so each fills the box full width, centred — the frames' 2:1 nodes for the old bitmaps
   (b1 -14,-3 458x229; b2 -16,-4 462x231; b3 -14,-2 458x229) had cut the new pictures' cat off at the right edge */
.sfig-img.b1{left:0;top:-9px;width:430px;height:242px;}        /* 1672x941: as b4 (was node 668:314, frame 652:3) */
.sfig-img.b2{left:0;top:0;width:430px;height:224px;}           /* 1738x905: the box exactly (was node 669:317, frame 652:192) */
.sfig-img.b3{left:0;top:0;width:430px;height:224px;}           /* 1738x905: the box exactly (was node 671:320, frame 660:127) */
.sfig-img.b4{left:0;top:-9px;width:430px;height:242px;}        /* node 653:563 (frame 653:381) */
.sfig-img:not(.on){visibility:hidden;}
/* the next beat's picture appears over the last one: fades up from a slight zoom and settles into its crop */
.sfig-img.enter{animation:sfigPicIn .65s cubic-bezier(.2,.8,.3,1) both;}
.sfig-img.sfig-pop{animation:p2BirdPop1s 1s ease-in-out 1 both;transform-origin:50% 50%;will-change:transform;}   /* [story-cat] beat 1's picture pops as G4's picture does (p2BirdPop1s, 1 s) as its line ends, with its sound */
@keyframes sfigPicIn{from{opacity:0;transform:scale(1.08);}to{opacity:1;transform:none;}}
/* [poem-box] (2026-10-31) the box and its text are the reference poem game's caption (hi02h11l03s01poem-8cpz.vercel.app, Page 1 T1,
   .story-caption, read as computed in Chrome): white, a 3 px white rim, 26 px corners, 8 px / 22 px padding, the shadow below; it
   hugs its one line, so it is the beat's sentence + 2 x (22 + 3) px wide and 37.12 + 2 x (8 + 3) px tall (the rim is white on
   white: it is in the size), centred where the sentences are (the module sets --sfig-tw per beat and re-fits it as the finished
   sentence leaves — after its .3 s fade). Stage px, divided by --fig-s like the shadow. Was Figma's node 436:412: 436x119 at
   314,250, 20 px corners */
.sfig-textbox{position:absolute;left:532px;top:309.5px;width:calc(var(--sfig-tw, 482px) + 50px / var(--fig-s));height:calc(59.12px / var(--fig-s));
  transform:translate(-50%,-50%);background:#FFFFFF;border-radius:calc(26px / var(--fig-s));
  box-shadow:0 calc(5px / var(--fig-s)) 0 rgba(11,42,90,.10),0 calc(10px / var(--fig-s)) calc(26px / var(--fig-s)) rgba(11,42,90,.12);
  transition:width .3s cubic-bezier(.2,.8,.3,1) .3s;}
/* [textbox-shadow] (2026-10-30) the shadow is the reference story's (hind-dear-story.vercel.app, Page 1 S01): its white sentence box
   (.stage.tut.l02-story .mr-read .mr-caption) casts a crisp 5 px navy lip and a soft 10 / 26 px navy glow under it, the same on every
   frame of the page; its stage px, divided by --fig-s so that .sfig-in's scale puts them on screen at exactly 5 / 10 / 26 px
   (was Figma's 0 4px 19.7px rgba(177,177,177,.25)) */
/* [poem-box] the caption's type: Baloo 2 declared 600 (only the 700 and 800 faces are embedded — the reference's own files,
   byte for byte — so it renders in the 700 face, as there), 29 px on a 37.12 px line (1.28), 0.2em word spacing of its 28 px
   box = 5.6 px; one line, every beat centred on the box's centre (the old box's, 532,309.5 — the frames' four text nodes sat
   within half a pixel of it; beat 1's 310 put its glyphs on a half pixel, softer than the reference's). The colour stays this
   page's #002F76. Was 'Story Baloo 2' 800, 26 px (beat 1) / 28 px, line-height normal, in the frames' text boxes */
.sfig-text{position:absolute;left:532px;top:309.5px;transform:translate(-50%,-50%);white-space:nowrap;width:max-content;
  font-family:var(--font-hi);font-weight:600;font-size:calc(29px / var(--fig-s));line-height:calc(37.12px / var(--fig-s));
  word-spacing:calc(5.6px / var(--fig-s));color:#002F76;text-align:center;}
.sfig-text.gone{opacity:0;visibility:hidden;transition:opacity .3s ease-out,visibility 0s .3s;}   /* a finished beat's text leaves */
/* Swiftie at the reference's 76,472 190x190 on the stage (in .sfig-in's frame px) */
.sfig-swiftie{position:absolute;left:calc(64px / var(--fig-s) - 96px);top:calc(460px / var(--fig-s) - 106px);
  width:calc(190px / var(--fig-s));height:calc(190px / var(--fig-s));object-fit:cover;}
/* word-by-word: every word keeps its place from the start, so the lines never reflow as words arrive */
.sfig-w{display:inline-block;opacity:0;transform:translateY(8px) scale(.92);
  transition:opacity .22s ease-out,transform .26s cubic-bezier(.2,.9,.3,1.25);}
.sfig-w.on{opacity:1;transform:none;}
/* [word-sync] (2026-10-30) the reference T1's sentence (hi-02-h04-l01-s01-dun, #STORY-INTRO-CSS siSentIn and #P2-BIRD-POP-CSS
   .p2-word.on): the whole text rises in at once — 0.45 s, cubic-bezier(.2,.8,.3,1), from 14 px lower at .96 and transparent — on
   the individual translate / scale properties, so a text box's own centring transform is kept; its words skip their arrival
   transition meanwhile (.sfig-whole). The word being read: dark orange with a small pop (1 -> 1.1 -> 1, .28 s), one at a time. */
@keyframes siSentIn{0%{opacity:0;translate:0 14px;scale:.96;}100%{opacity:1;translate:0 0;scale:1;}}
.sfig-rise{animation:siSentIn .45s cubic-bezier(.2,.8,.3,1) 1 both;transform-origin:50% 50%;}
.sfig-whole .sfig-w, .stp-sign.sfig-rise{transition:none !important;}
.sfig-w.hot{color:#E86A00;transform-origin:50% 60%;animation:p2WordPop .28s ease-out 1;}
/* ===== [story-fig] T0B "आइए वाक्य सुनें।" (frame 488:190, STORY_RELISTEN): the frame's own card (node 488:367:
   border box 96,106 1088x508 x 1333/1280 = 100,110.39 1133x529 on the stage, 64px corners), grid, title and sentence
   box, in .sfig-in's frame px; Swiftie, the 🔊 chip and आगे stay where they are on the story page (T0) ===== */
.stage.tut .slide-stage:has(.sfig-round){padding:calc(106px * var(--fig-s)) 100px calc(750px - 614px * var(--fig-s));}
.stage.tut .tut-card.sfig-card.sfig-round{border-radius:calc(64px * var(--fig-s));}
.tut-card.sfig-card.sfig-round .tut-audio{top:calc(594px - 106px * var(--fig-s));}     /* 202,606 on the stage, as on T0 */
/* .sfig-in on the frame card's padding box exactly (108,118 x 1333/1280): the 12.5px border is drawn as 12px */
.sfig-round .sfig-in{left:calc(108px * var(--fig-s) - 112px);top:calc(12px * var(--fig-s) - 12px);}
.sfig-round .sfig-clip{left:calc(112px / var(--fig-s) - 108px);top:calc(12px / var(--fig-s) - 12px);
  width:calc(1109px / var(--fig-s));height:calc(508px - 24px / var(--fig-s));border-radius:calc(64px - 12px / var(--fig-s));}
/* nodes 488:368 / 488:369 put the grid where 435:180 / 435:181 put it on T0 */
.sfig-round .sfig-grid.g1{left:calc(-187px - 112px / var(--fig-s) + 108px);top:calc(-33.968px - 12px / var(--fig-s) + 12px);}
.sfig-round .sfig-grid.g2{left:calc(531.968px - 112px / var(--fig-s) + 108px);top:calc(-34px - 12px / var(--fig-s) + 12px);}
.sfig-round .sfig-swiftie{left:calc(76px / var(--fig-s) - 108px);top:calc(472px / var(--fig-s) - 118px);}   /* 76,472, as on T0 */
.sfig-title{position:absolute;left:322px;top:65.5px;width:420px;overflow-wrap:break-word;
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;font-size:64px;line-height:normal;
  color:#002F76;text-align:center;opacity:0;transform:translateY(calc(-50% + 18px)) scale(.92);
  transition:opacity .4s ease-out,transform .6s cubic-bezier(.2,.9,.3,1.25);}   /* node 488:376: centred on 532,59.5 */
.sfig-title.in{opacity:1;transform:translateY(-50%);}
/* node 488:371 (the frame as of 2026-10-21 evening, fifth version) is 683x219 at 191,144 — centred on 532.5 — with its
   4px stroke drawn OUTSIDE it (its render is 691x227 at 187,140) and 20px corners, i.e. 24px on the stroke's outer edge */
.sfig-sbox{position:absolute;left:187px;top:140px;width:691px;height:227px;background:#FFFFFF;border:4px solid #DADADA;
  border-radius:24px;opacity:0;transform:scale(.9);}
.sfig-sbox.in{animation:sfigBoxIn .5s cubic-bezier(.2,.9,.3,1.2) both;}
@keyframes sfigBoxIn{from{opacity:0;transform:scale(.9);}to{opacity:1;transform:none;}}
/* node 488:374 (the frame as of 2026-10-21 evening): 631 wide, centred on 532.5, bottom-aligned on y 369 (280 tall),
   ending with the frame's empty paragraph. Line height: the font's "normal" is 1.304em; Figma rounds 28 x 1.304 to
   37px, Chrome to 25+11 = 36px, so it is 37px */
.sfig-stext{position:absolute;left:217px;top:89px;width:631px;height:280px;display:flex;flex-direction:column;
  justify-content:flex-end;overflow-wrap:break-word;font-family:'Story Baloo 2',var(--font-hi);
  font-weight:800;font-size:28px;line-height:37px;color:#002F76;text-align:center;}
/* [relisten-pinki] frame 654:567: the two sentences are their own nodes in the box — 30px, 401 / 390 wide, centred on
   540.5,204.5 and 540,302.5 (the card's padding box; 8 px right of the box's centre, as the frame has them). The
   explanation lifts a sentence on its yellow (the demos' hot-word yellow); the moral lifts the commas in the picks' orange */
.sfig-stext.sfig-lines{display:block;left:0;top:0;width:auto;height:auto;}
.sfig-stext.sfig-lines p{position:absolute;margin:0;transform:translateY(-50%);font-size:30px;line-height:normal;}
.sfig-stext.sfig-lines p.l1{left:340px;top:204.5px;width:401px;}   /* node 654:752 */
.sfig-stext.sfig-lines p.l2{left:345px;top:302.5px;width:390px;}   /* node 654:753 */
.sfig-sent{display:inline-block;padding:2px 14px;margin:-2px -14px;border-radius:12px;
  transition:background-color .35s ease-out,transform .45s cubic-bezier(.2,.9,.3,1.2);}
.sfig-sent.hl{background:#FFF1B6;transform:scale(1.06);}
.sfig-mk{display:inline-block;transition:color .3s ease-out,transform .45s cubic-bezier(.2,.9,.3,1.3);}
.sfig-mk.on{color:#E86A00;transform:scale(1.4);}
"""
recap_css = """
/* ===== [recap-fig] T1 "ये हैं तीन विराम चिह्न" (frame 508:2, MARKS_RECAP): T0B's card, grid, Swiftie and 🔊 chip (the
   frame's card is the same 96,106 1088x508 box with 64px corners, so the .sfig-round rules above apply as they are);
   the frame's own title and three rows, in .sfig-in's frame px (= the frame's card px - 12, its border). The texts
   are Noto Sans Devanagari SemiBold: the title and marks are set in it in the frame, and the labels — "Baloo Bhai 2"
   in the frame, which has no Devanagari glyphs — render in Figma's Noto Sans Devanagari fallback. ===== */
.sfig-recap .sfig-title{left:291px;top:52.5px;width:483px;}   /* node 508:184: 483 wide, centred on 544.5,64.5 (card px) */
.rcf-row{position:absolute;left:0;top:0;width:1064px;height:484px;pointer-events:none;}
/* the marks' boxes: nodes 508:183 / 516:22 / 516:23, 93x90 at 166,127 / 166,256 / 166,385 (card px) with their 4px
   stroke drawn OUTSIDE (the render is 101x98 at 162,123 ...) and 10px corners, i.e. 14px on the stroke's outer edge */
.rcf-sign{position:absolute;left:150px;width:101px;height:98px;background:#FFFFFF;border:4px solid #DADADA;
  border-radius:14px;opacity:0;transform:scale(.9);}
.r1 .rcf-sign{top:111px;} .r2 .rcf-sign{top:240px;} .r3 .rcf-sign{top:369px;}
.rcf-sign.in, .rcf-eg.in{animation:sfigBoxIn .5s cubic-bezier(.2,.9,.3,1.2) both;}   /* pops in as its clip starts */
/* the marks: text nodes 512:3 / 512:4 / 515:21 — 483-wide centred boxes, centred on 209.5,174.5 / 212.5,304.5 /
   212.5,438.5 (card px), 64px — placed from their box's padding box. 512:3 is "। " with a trailing space, which
   Figma does NOT count when centring (the render's danda sits on the node's centre), so it is dropped here */
.rcf-mark{position:absolute;width:483px;transform:translate(-50%,-50%);font-family:'Story Baloo 2',var(--font-hi);
  font-weight:800;font-size:64px;line-height:normal;color:#002F76;text-align:center;white-space:pre;}
.r1 .rcf-mark{left:43.5px;top:47.5px;} .r2 .rcf-mark{left:46.5px;top:48.5px;} .r3 .rcf-mark{left:46.5px;top:53.5px;}
/* names and uses: nodes 520:260-262 and 514:8 / 517:24 / 517:25 — 1075-wide centred boxes, 48 tall, 28px, #012F76:
   centred on x 372.5 / 372.5 / 380.5 and 633.5, tops 148 / 275 / 414 and 148 / 278 / 414 (card px). The line box is
   Baloo Bhai 2's, not Noto's: 1.714 x 28 = 48px (the nodes' height), with the fallback glyphs centred in it. The spaces
   are Baloo Bhai 2's too, 2px narrower than Noto's at this size (the render's words sit that much closer; measured by
   pixel-matching the render over SemiBold/-0.5..-4px, see the README) */
.rcf-name, .rcf-when{position:absolute;width:1075px;height:48px;transform:translateX(-50%);
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;font-size:28px;line-height:48px;color:#012F76;text-align:center;}
.r1 .rcf-name{left:360.5px;top:136px;} .r2 .rcf-name{left:360.5px;top:263px;} .r3 .rcf-name{left:368.5px;top:402px;}
.r1 .rcf-when{left:621.5px;top:136px;} .r2 .rcf-when{left:621.5px;top:266px;} .r3 .rcf-when{left:621.5px;top:402px;}
/* the examples' yellow boxes: nodes 514:12 / 518:26 / 519:28 at 790,143 163x49 / 790,274 262x49 / 790,405 191x49
   (card px), 8px corners, clipping; their text 22px, centred, 7 / 8 / 9 px from the top, in Baloo Bhai 2's line box
   (1.714 x 22 = 38px, Figma's rounding; the render's glyphs sit 1px lower than that box centred in Chrome, hence
   8 / 9 / 10) and with Baloo Bhai 2's spaces, 2px narrower than Noto's. 514:10 starts with a space, which Figma
   counts (as on T0's first line) */
.rcf-eg{position:absolute;left:778px;height:49px;background:#FFF1B6;border-radius:8px;overflow:hidden;opacity:0;transform:scale(.9);}
.r1 .rcf-eg{top:131px;width:163px;} .r2 .rcf-eg{top:262px;width:262px;} .r3 .rcf-eg{top:393px;width:191px;}
.rcf-eg p{position:absolute;left:calc(50% - 537.5px);width:1075px;height:48px;   /* [word-sync] = left:50% + translateX(-50%), without the transform the rise would scale */
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;font-size:22px;line-height:38px;color:#012F76;text-align:center;}
.r1 .rcf-eg p{top:8px;} .r2 .rcf-eg p{top:9px;} .r3 .rcf-eg p{top:10px;}
.r1 .rcf-eg p::before{content:"\\a0";}
/* आगे is not in the frame and the frame's rows fill the card down to its third example, so T0's place for the pill
   (inside the card, 567.5,522) would sit on "सवाल पूछने पर": here it is centred in the gap under the card
   (card bottom 614 x 1333/1280 = 639.4 on the stage; the pill 198x90 at 567.5,650) */
.stage.tut:has(.sfig-recap) .nav-btn{bottom:10px;}
"""
demo_css = """
/* ===== [demo-fig] T2, the first run-on sentence demo (frame 519:32 "G3 guided story question", PUNCT_DEMO): the frame
   has no card — its title bar, picture, sentence bar and mark tiles sit on the plain #F2F7FA stage — so the tutorial
   card loses its box and .sfig-in is the whole 1280x720 frame (x 1333/1280). No standing Swiftie and no 🔊 chip on this
   page (2026-10-25, as asked; the frame's only Swiftie is the head in its title bar). The
   texts are Noto Sans Devanagari SemiBold with Baloo Bhai 2's line boxes and spaces, as on T1 (the frame's labels are
   "Baloo Bhai 2", which has no Devanagari glyphs: Figma renders them in its Noto fallback). Every strokes here is drawn
   INSIDE its box (checked on the render). ===== */
.stage.tut .slide-stage:has(.sfig-full){padding:0;}
.stage.tut .tut-card.sfig-card.sfig-full{border:0;border-radius:0;background:none;box-shadow:none;}
body.tut-page:has(.sfig-full), .stage.tut:has(.sfig-full){background:#F2F7FA;}
.sfig-full .sfig-in{left:0;top:0;width:1280px;height:720px;}
.sfig-full .sfig-clip{display:none;}
.sfig-full .sfig-swiftie, .tut-card.sfig-card.sfig-full .tut-audio{display:none;}
/* the title bar: group 519:206 at 36,26 1244x120 with its drop shadow; the pill 519:208 (3.897,18 1214.103x84, #CBE8FF,
   4px white border inside, stadium) and the Swiftie head 519:211 (116.513x120, #61D0FE, 5px #FDF9E9 ring inside,
   stadium, clipping its 165px "Happy" picture at -16,5). The pill's text 519:209: 32px at 139.55,18 in the pill, left
   aligned, in Baloo Bhai 2's line box (1.714 x 32 = 55px) with its spaces (-2px); its trailing space is not counted */
.dmf-band{position:absolute;left:36px;top:26px;width:1244px;height:120px;filter:drop-shadow(0 4px 2px rgba(0,0,0,.25));
  opacity:0;transform:translateY(-14px) scale(.97);transition:opacity .45s ease-out,transform .55s cubic-bezier(.2,.9,.3,1.2);}
.dmf-band.in{opacity:1;transform:none;}
.dmf-pill{position:absolute;left:3.897px;top:18px;width:1214.103px;height:84px;background:#CBE8FF;border:4px solid #FFFFFF;border-radius:999px;overflow:hidden;}
.dmf-pill p{position:absolute;left:135.551px;top:14px;width:1075px;height:48px;white-space:nowrap;
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;font-size:32px;line-height:55px;color:#012F76;}
.dmf-head{position:absolute;left:0;top:0;width:116.513px;height:120px;background:#61D0FE;border:5px solid #FDF9E9;border-radius:9999px;overflow:hidden;}
.dmf-head img{position:absolute;left:-21px;top:0;width:165px;height:165px;object-fit:cover;}
/* the picture box 521:285 (197,211 144x139, 2.386px #D5D8DF border inside, 14.316px corners) with "image 228" 521:283
   (80.052x120 at 227,221), and the sentence bar 519:218 (365,211 719x139, the same box, clipping) */
.dmf-pic, .dmf-bar, .dmf-tile{opacity:0;transform:scale(.9);transition:opacity .45s ease-out,transform .5s cubic-bezier(.2,.9,.3,1.2);}
.dmf-pic.in, .dmf-bar.in, .dmf-tile.in{opacity:1;transform:none;}
.dmf-pic{position:absolute;left:197px;top:211px;width:144px;height:139px;background:#FFFFFF;border:2.386px solid #D5D8DF;border-radius:14.316px;}
.dmf-pic img{position:absolute;left:27.614px;top:7.614px;width:80.052px;height:120px;object-fit:cover;}
.dmf-bar{position:absolute;left:365px;top:211px;width:719px;height:139px;background:#FFFFFF;border:2.386px solid #D5D8DF;border-radius:14.316px;overflow:hidden;}
/* the sentence 519:223: 64px, a 479-wide centred box at 100,18 in the bar (centred on 339.5), in Baloo Bhai 2's line
   box (1.714 x 64 = 110px) with its spaces (-4px at this size) */
.dmf-sent{position:absolute;left:97.614px;top:15.614px;width:479px;height:104px;white-space:nowrap;text-align:center;
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;font-size:64px;line-height:110px;color:#012F76;}
.dmf-sent .sfig-w{border-radius:10px;transition:opacity .22s ease-out,transform .26s cubic-bezier(.2,.9,.3,1.25);}
/* the word being read: [word-hot] (2026-10-28) G4's own look and motion in place of the light-yellow box — the word turns the
   picks' orange and pops once (SENT_PICK's .p2-word.on: #E86A00, p2WordPop .28s ease-out, origin 50% 60%); one word at a
   time, as G4 lights its pill's words; the slot's own highlight (.dmf-blank.hot) is unchanged */
.dmf-sent .sfig-w.hot{color:#E86A00;transform-origin:50% 60%;animation:p2WordPop .28s ease-out 1;}
/* the empty slot 520:231: 59x100 at 583,20 in the bar, #FFF1B6, 8px corners, a 2px dashed rgba(86,86,86,.85) stroke inside
   — drawn as an SVG stroke so the dashes are the render's (10 on, 5 off), which a CSS dashed border cannot be told */
.dmf-blank{position:absolute;left:580.614px;top:17.614px;width:59px;height:100px;background:#FFF1B6;border-radius:8px;
  transition:background-color .4s,box-shadow .25s;}
.dmf-dash{position:absolute;left:0;top:0;display:block;fill:none;stroke:rgba(86,86,86,.85);stroke-width:2;stroke-dasharray:10 5;transition:opacity .4s,stroke .25s;}
.dmf-blank.blink{animation:dmfBlink 1.16667s ease-in-out 3;}   /* three slow blinks = 3.5 s (the module sets blink_ms / 3) */
@keyframes dmfBlink{0%,100%{opacity:1;}50%{opacity:.2;}}
/* the mark: its INK centred on the slot — (--ix, --iy) is the ink's centre relative to the line box's centre, measured
   by the module from the font (the fallbacks are the bundled Noto SemiBold 64px danda's: 2.89px right, 4.49px up) */
.dmf-blank .dmf-mark{position:absolute;left:50%;top:50%;opacity:0;--ix:2.89px;--iy:-4.49px;white-space:pre;
  transform:translate(calc(-50% - var(--ix)),calc(-50% - var(--iy))) scale(.4);transform-origin:calc(50% + var(--ix)) calc(50% + var(--iy));
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;font-size:64px;line-height:normal;color:#012F76;
  transition:opacity .35s ease-out,transform .45s cubic-bezier(.2,.9,.3,1.3);}
.dmf-blank .dmf-mark.in{opacity:1;transform:translate(calc(-50% - var(--ix)),calc(-50% - var(--iy)));}
.dmf-blank.hot{box-shadow:0 0 0 6px rgba(232,106,0,.22);}                              /* the mark being named — [demo-hand] (2026-10-28) the words' orange, not blue (was rgba(56,106,246,.22)) */
.dmf-blank.hot .dmf-dash{stroke:#E86A00;stroke-dasharray:none;}                      /* [demo-hand] the ring too (was #386AF6); T4's solid ring inherits it */
.dmf-blank.hot .dmf-mark{transform:translate(calc(-50% - var(--ix)),calc(-50% - var(--iy))) scale(1.22);}
.dmf-blank.gone{background:transparent;box-shadow:none;}                               /* the box goes, the mark stays */
.dmf-blank.gone .dmf-dash{opacity:0;}
/* [demo-fig] a frame's own slots (T4's two 33x38): dashed per side (the lines carry the frame's dash runs), the rounded
   solid ring only while highlighted; the mark keeps the sentence's size (data.mark_size) */
.dmf-own .dmf-dash .dmf-solid{opacity:0;}
.dmf-blank.dmf-own.hot .dmf-dash .dmf-solid{opacity:1;}
.dmf-blank.dmf-own.hot .dmf-dash line{opacity:0;}
/* the mark tiles (group 521:287): a #D9D9D9 base 227x169 at 197 / 527 / 857, 443 (13.31px corners) under a white face
   223x161 at +2,+2 (2.386px #D5D8DF border inside, 14.316px corners) — the base shows 2px at the sides and 6px below;
   the mark (64px Noto, 483-wide centred boxes: 520:263 "। " — its trailing space not counted — centred on 308.5,501.5;
   520:264 on 640.5,492.5; 520:271 on 970.5,502.5) and the name (28px, 1075-wide centred boxes: 520:279-281 centred on
   310.5 / 640.5 / 970.5, tops 543 / 544 / 544) */
.dmf-tile{position:absolute;top:443px;width:227px;height:169px;}
.dmf-tile.t1{left:197px;} .dmf-tile.t2{left:527px;} .dmf-tile.t3{left:857px;}
.dmf-base{position:absolute;left:0;top:0;width:227px;height:169px;background:#D9D9D9;border-radius:13.31px;}
.dmf-face{position:absolute;left:2px;top:2px;width:223px;height:161px;background:#FFFFFF;border:2.386px solid #D5D8DF;border-radius:14.316px;
  transition:border-color .2s,box-shadow .2s;}
/* [tile-hit] (2026-10-28) the mark's and the name's text boxes are far wider than the tile (483 / 1075 px: the glyphs centre on the
   tile whatever their width) and overflow onto the next tiles, where the later tile's box sat on top and took the tap — a tap on
   tile 1's name reached tile 2 (on G3 the right tile's name was judged wrong). The texts take no pointer events now; the tile's
   own box (base + face) answers every tap on it. */
.dmf-sym{position:absolute;width:483px;transform:translate(-50%,-50%);text-align:center;white-space:pre;pointer-events:none;
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;font-size:64px;line-height:normal;color:#002F76;}
.t1 .dmf-sym{left:111.5px;top:58.5px;} .t2 .dmf-sym{left:113.5px;top:49.5px;} .t3 .dmf-sym{left:113.5px;top:59.5px;}
.dmf-name{position:absolute;left:113.5px;width:1075px;height:48px;transform:translateX(-50%);text-align:center;pointer-events:none;
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;font-size:28px;line-height:48px;color:#012F76;}
.t1 .dmf-name{top:100px;} .t2 .dmf-name{top:101px;} .t3 .dmf-name{top:101px;}
/* tapped for the child: the tile presses down and comes back, its colours unchanged (no blue selection ring,
   2026-10-25); the other tiles dim = the engine's faded option. [tile-tap] (2026-10-28): the press is the WHOLE
   option's — base, face, mark and name together (the mark and name are the tile's children, not the face's, so
   the old face-only press left them and the grey base still); auto tap on T2-T4, the child's on G1-G3 alike */
.dmf-tile.on{animation:dmfTap .45s ease-out;}
@keyframes dmfTap{0%{transform:none;}35%{transform:translateY(6px);}100%{transform:none;}}
.dmf-tile.off{opacity:.35;filter:saturate(.6);transition:opacity .3s,filter .3s;}
.dmf-live .dmf-tile.off{pointer-events:none;cursor:default;}   /* [hand-quiet] the picks' other two tiles once the hand points: dead */
/* [pick-fig] G1 (frame 525:354 "7 G1", PUNCT_PICK): the tiles are the child's once the sentence has been read; a wrong
   one shakes with the engine's own wrong-answer wiggle (wgNo, one --fx-beat), its colours unchanged */
.dmf-live .dmf-tile{cursor:pointer;}
.dmf-tile.wiggle{animation:wgNo var(--fx-beat) ease-in-out both;}
"""
# [letter-fig] the letter page, in the frames' 1280x720 px inside .sfig-full's .sfig-in. The envelope is one element in 610:6's
# box (71,-50 1138x758); its icon state is that box scaled into the cloud (--ltr-icon, set by the module), so the zoom is a
# transform transition. Its layers are the 1536x1024 picture cut up (img_letter_env_*), each stretched to the box: hinge =
# the top edge TL(191,329)-TR(1263,87) -> (538.6,154.1) at 1138/1536, tilted -12.72 deg; the heart's centre (814,537) -> (603,398).
letter_css = """
/* ===== [letter-fig] LETTER_STORY: frames 538:2 / 538:35 / 538:39 / 558:2 / 610:6 as one animated scene ===== */
.ltr{position:absolute;left:0;top:0;width:1280px;height:720px;overflow:hidden;}
.ltr > *{position:absolute;}
.ltr-scene{left:0;top:0;width:1280px;height:720px;object-fit:cover;}                      /* 538:2: the picture at 0,0 1280x720 */
.ltr-scene.b{top:-1px;height:721px;opacity:0;transition:opacity .65s ease-in-out;}       /* 538:35: image 235 at 0,-1 1280x721 */
.ltr.b-in .ltr-scene.b{opacity:1;}
.ltr-scene.c{top:-1px;height:721px;opacity:.005;transition:opacity .35s ease-in-out;}    /* [letter-idea] the pensive girl (the user's 1.png, the same room): over B on the chime's "ummm", off on its "aahaha"; at rest 1/255 (painted, so decoded, with the page's first frame — unseen; 0 would cost a 50-70 ms frame on the beat) */
.ltr.c-in .ltr-scene.c{opacity:1;}
.ltr-bub{border-radius:50%;background:#fff;box-shadow:0 1px 2px rgba(120,90,60,.15);transform:scale(0);opacity:0;
  transition:transform .32s cubic-bezier(.3,1.5,.5,1),opacity .2s ease-out;}
.ltr-bub.in{transform:none;opacity:1;}
.ltr-cloud{opacity:0;transform:scale(.55) translate(-30px,40px);transform-origin:12% 92%;will-change:transform,opacity;
  transition:opacity 1.2s ease-out,transform 1.6s cubic-bezier(.2,.7,.2,1);}             /* grows in from the bubbles' corner, slowly; its layer made at mount, not on the beat */
.ltr-cloud.in{opacity:1;transform:none;}
.ltr-cloud.out{opacity:0;transform:scale(.55) translate(-30px,40px);transition:opacity .45s ease-in,transform .6s cubic-bezier(.4,0,.7,.5);}   /* [letter-idea] on the chime's "ummm": back into the bubbles' corner, quickly */
.ltr-cloud img{position:absolute;left:0;top:0;width:100%;height:100%;}
.ltr-cloud .ltr-cw{opacity:.005;}                                                       /* 1/255: painted (so decoded) with the grandfather's entrance, unseen, not on the beat */
.ltr-cloud.white .ltr-cg{opacity:0;}                                                     /* the same cloud, white (558:2): swapped while it is out (unseen), ... */
.ltr-cloud.white .ltr-cw{opacity:1;}                                                     /* ... then grown in again (.in) on the "aahaha", the letter growing in it */
.ltr-blur{left:0;top:0;width:1280px;height:720px;opacity:0;transition:opacity .9s ease-in-out;}   /* 610:6's backdrop, flattened */
.ltr.zoom .ltr-blur{opacity:1;}
.ltr-env-pos{transform-origin:0 0;transform:var(--ltr-icon);pointer-events:none;transition:transform 1.2s cubic-bezier(.45,0,.2,1);}
.ltr.zoom .ltr-env-pos{transform:none;}                                                  /* = 610:6's envelope box */
/* [letter-idea] the letter grows in WITH the cloud on the chime's "aahaha": the cloud's own entrance (opacity 1.2 s; the scale and
   the slide from the bubbles' corner, 1.6 s) on a wrapper inside the icon, in the box's px (--ltr-go / --ltr-gt, set by the module:
   that corner and that slide at 1/s), so the cloud and the letter in it are one growing thought; none after, so the zoom and the
   dive see nothing of it. Its resting opacity is 1/255, not 0, and it has its own layer from mount (will-change): a layer at 0 is
   never rasterised, so the envelope's four lossless layers (6 MP) would be decoded on the beat itself — a 120-150 ms frame right
   on the "aahaha" (measured on the page's own frames) — while at 1/255 they are drawn (unseen: under a level) and so decoded with
   the page's first frame; the raster then is at the icon's small scale, cheap */
.ltr-env-grow{position:absolute;inset:0;transform-origin:var(--ltr-go,0 0);opacity:.005;transform:scale(.55) translate(var(--ltr-gt,0px,0px));
  will-change:transform,opacity;transition:opacity 1.2s ease-out,transform 1.6s cubic-bezier(.2,.7,.2,1);}
.ltr.letter-in .ltr-env-grow{opacity:1;transform:none;}
.ltr-env-pulse{position:absolute;inset:0;transform-origin:603px 398px;}                /* hidden by the grow wrapper until the "aahaha" */
.ltr.ready .ltr-env-pos{pointer-events:auto;cursor:pointer;}
.ltr.ready .ltr-env-pulse{opacity:1;animation:ltrPulse 1.2s ease-in-out infinite;}
.ltr.zoom .ltr-env-pulse{opacity:1;animation:none;}
@keyframes ltrPulse{0%,100%{transform:scale(1);}50%{transform:scale(1.07);}}
.ltr-env3d{position:absolute;inset:0;perspective:2600px;}
.ltr-env3d > *{position:absolute;left:0;top:0;width:100%;height:100%;}
.ltr-flap img{position:absolute;left:0;top:0;width:100%;height:100%;}
/* [letter-dive] the drawing as drawn, in its painting order: inner (behind), the sheet, the body (the pocket), the flap, the heart
   — closed, the flap covers the sheet exactly as drawn. The flap is hinged on the top edge (its midpoint in the 1138x758 box, the
   edge's own -12.72 deg tilt): rotate(t) rotateX(a) rotate(-t), the sign that lifts it TOWARD the viewer — up and out, as a real
   flap (the envelope's body and the sheet are behind it, which is also the painting order). It opens to 80 deg — standing up,
   seen almost edge-on as a thin band under the top edge — so no part of it ever rises above that edge: nothing of it can be cut
   by the frame, not even as the dive carries the top edge out of view; the sheet rises in the mouth to just under that band (its
   top edge is parallel to the envelope's). */
.ltr-flap{transform-origin:538.6px 154.1px;transform:rotate(-12.72deg) rotateX(0deg) rotate(12.72deg);}
.ltr.open .ltr-flap{animation:ltrFlap 1s cubic-bezier(.5,0,.3,1) both;}
@keyframes ltrFlap{from{transform:rotate(-12.72deg) rotateX(0deg) rotate(12.72deg);}to{transform:rotate(-12.72deg) rotateX(80deg) rotate(12.72deg);}}
/* the whole-screen transition: the view dives INTO the open envelope (the same element: a second transform transition; --ltr-dive,
   set by the module, = the box scaled by pace.dive_scale about the mouth's centre, which lands on the frame's centre) until only
   the sheet fills the screen; the veil then takes it to the end screen */
.ltr.dive .ltr-env-pos{transform:var(--ltr-dive);transition-duration:var(--ltr-dive-ms,1.7s);transition-timing-function:cubic-bezier(.45,0,.55,1);}
.ltr-heart{transform-origin:603.2px 398.2px;}
.ltr.open .ltr-heart{animation:ltrSeal .35s ease-in both;}
@keyframes ltrSeal{0%{transform:scale(1);opacity:1;}40%{transform:scale(1.18);opacity:1;}100%{transform:scale(.55);opacity:0;}}
/* the sheet inside: a plain white letter with faint lines, in the envelope's own tilt, rising out of the pocket */
.ltr-paper{left:279px;top:205px;width:635px;height:378px;border-radius:10px;background:#FFFDF8;box-shadow:0 2px 10px rgba(120,80,40,.18);
  transform:rotate(-12.72deg);transition:transform .9s cubic-bezier(.3,.7,.3,1);}
.ltr-paper::after{content:"";position:absolute;inset:0;border-radius:inherit;transition:opacity 1.2s ease-in;   /* its ruled lines ... */
  background:repeating-linear-gradient(to bottom,transparent 0 46px,#E9DCF2 46px 50px) 0 10px;}
.ltr.paper .ltr-paper{transform:rotate(-12.72deg) translateY(-35px);}                    /* risen in the mouth, to just under the standing flap */
.ltr.dive .ltr-paper::after{opacity:0;}                                                  /* ... fade as the view dives onto the sheet */
.ltr-veil{inset:0;background:#FDE9A8;opacity:0;pointer-events:none;transition:opacity .5s ease-in;}   /* the end screen's base colour */
.ltr.veil .ltr-veil{opacity:1;}
"""
# [stamp-fig] L2, the stamp page, in the frame's 1280x720 px inside .sfig-full's .sfig-in: the frame's places (get_metadata 565:28) —
# the wood 0,-1 1280x721; the title bar = the demos' group (36,26 1244x120, its text at 139.55 in the pill: measured the same on this
# render); "image 238" turned, 355,64 571x594 (the paper itself 392..887 x 154..559 on the render); the tray 427,565 426x142 with its
# 0 4 4 .48 shadow; the stamps 532,541 74x116 (।) and 677,540 72x115 (?); the sentence's 1075-wide centred box at 63,336 (48 tall,
# 30px: the ink 455..745 x 342..372 on the render, centred on 600); the slot 751,331 36x58 #FFF1B6, 8px corners, a 2px dashed
# rgba(86,86,86,.85) stroke inside (its runs, read off the render: 6 9 6 9 6 across, 6 7 4 10 4 10 4 7 6 down).
stamp_css = """
/* ===== [stamp-fig] L2, the stamp page (frame 565:28, STAMP_DEMO): the letter's sentence stamped, on the whole stage ===== */
.stp{position:absolute;left:0;top:0;width:1280px;height:720px;overflow:hidden;}
.stp > *{position:absolute;}
.stp-wood{left:0;top:-1px;width:1280px;height:721px;}                                        /* the table, as the frame crops it */
.stp-sheet{opacity:0;transform:translateY(-28px) scale(.97);transition:opacity .5s ease-out,transform .55s cubic-bezier(.2,.9,.3,1.15);}   /* settles onto the table */
.stp-sheet.in{opacity:1;transform:none;}
.stp-tray{filter:drop-shadow(0 4px 4px rgba(0,0,0,.48));opacity:0;transform:translateY(36px);transition:opacity .4s ease-out,transform .5s cubic-bezier(.2,.9,.3,1.15);}   /* slides up */
.stp-tray.in{opacity:1;transform:none;}
/* a stamp: its box glides (the module sets the transform), its picture pops in (about its base); once the slot is up (.live) it
   is a drag handle (touch-action none: the finger's move is the drag, not a scroll); .drag = in hand (no transition: it follows
   the finger); .stp-wrong = the kit's wiggle (wgNo) on its picture, so its box keeps the place it was dropped at [stamp-drag] —
   stp-wrong, not "wrong": the engine's :is(.wrong,.wrong-flash,.ocean-wrong){background-color:#fff!important} would box it white */
.stp-stamp{transform-origin:50% 100%;transition:filter .3s;touch-action:none;}
.stp.live .stp-stamp{cursor:grab;}
.stp-stamp.drag{transition:none!important;cursor:grabbing;}
.stp-stamp.stp-wrong img.shown{animation:wgNo var(--fx-beat) ease-in-out both;}
.stp-stamp img{position:absolute;left:0;top:0;width:100%;height:100%;opacity:0;transform-origin:50% 100%;}
.stp-stamp img.pop{animation:stpPop .45s cubic-bezier(.3,1.4,.5,1) both;}
.stp-stamp img.shown{opacity:1;}
.stp-stamp img.unpop{animation:stpPop .45s cubic-bezier(.3,1.4,.5,1) both reverse;}   /* [stamp-rounds] shrinks away: the pop backwards */
@keyframes stpPop{from{transform:scale(0);opacity:0;}to{transform:none;opacity:1;}}
.stp-stamp.lift{z-index:5;filter:drop-shadow(0 16px 8px rgba(0,0,0,.28));}                 /* lifted off the table, over the sheet */
/* the sentence: Noto Sans Devanagari SemiBold in Baloo Bhai 2's line box, black, centred; each word arrives as it is read */
.stp-sent{white-space:nowrap;text-align:center;font-family:'Story Baloo 2',var(--font-hi);font-weight:800;color:#000;margin:0;}
.stp-sent .sfig-w{display:inline-block;opacity:0;transform:translateY(6px);transition:opacity .22s ease-out,transform .26s cubic-bezier(.2,.9,.3,1.25);}
.stp-sent .sfig-w.on{opacity:1;transform:none;}
.stp-sent .stp-gap{display:inline-block;height:1px;vertical-align:baseline;}            /* [stamp-rounds] the room the slot sits in, between two words */
/* [stamp-rounds] the letter's sign-off (frame 593:151, data.sign): small centred lines under the sentence, arriving as a word does */
.stp-sign{white-space:nowrap;text-align:center;font-family:'Story Baloo 2',var(--font-hi);font-weight:800;color:#000;margin:0;opacity:0;transform:translateY(6px);transition:opacity .22s ease-out,transform .26s cubic-bezier(.2,.9,.3,1.25);}
.stp-sign.on{opacity:1;transform:none;}
/* the empty slot: the frame's box, the demos' blink (dmfBlink, three slow blinks = blink_ms — asked to be just like the pages
   before); .gone = the box goes, the mark stays */
.stp-slot{background:#FFF1B6;border-radius:8px;opacity:0;transition:opacity .3s,background-color .4s;}
.stp-slot.in{opacity:1;}
.stp-slot.blink{animation:dmfBlink 1.16667s ease-in-out 3;}
.stp-slot svg{position:absolute;left:0;top:0;display:block;fill:none;stroke:rgba(86,86,86,.85);stroke-width:2;transition:opacity .4s;}
.stp-slot.gone{background:transparent;}
.stp-slot.gone svg{opacity:0;}
.stp-slot.out{opacity:0;}                                                                /* [stamp-rounds] between rounds: fades with its mark */
/* the printed mark: the sentence's own letter (its font, size and black), its INK on the slot's centre (--ix / --iy measured by the
   module), pressed in: it lands from a little large and tilted, as a stamp's print */
.stp-mark{position:absolute;left:50%;top:50%;opacity:0;--ix:0px;--iy:0px;white-space:pre;line-height:normal;
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;color:#000;
  transform:translate(calc(-50% - var(--ix)),calc(-50% - var(--iy))) scale(1.35) rotate(-8deg);transform-origin:calc(50% + var(--ix)) calc(50% + var(--iy));
  transition:opacity .2s ease-out,transform .28s cubic-bezier(.2,.9,.3,1.3);}
.stp-mark.in{opacity:1;transform:translate(calc(-50% - var(--ix)),calc(-50% - var(--iy)));}
/* [stamp-final] the finale: the final picture over the whole stage (the title bar too), dissolving in over fin_fade (the module sets
   the duration); over the envelope a soft gold glow (fin_glitter_ms, --glit) and the sparks, each twinkling once (fill both: gone when done) */
.stp-final{left:0;top:0;width:1280px;height:720px;z-index:20;opacity:0;transition:opacity 3s ease-in-out;pointer-events:none;}
.stp-final.in{opacity:1;}
.stp-final > img{position:absolute;left:0;top:0;width:100%;height:100%;display:block;}
.stp-glit{position:absolute;--glit:1300ms;}
.stp-glit .stp-glow{position:absolute;left:-25%;top:-25%;width:150%;height:150%;border-radius:50%;background:radial-gradient(closest-side,rgba(255,226,130,.6),rgba(255,226,130,0));opacity:0;}
.stp-glit.on .stp-glow{animation:stpGlow var(--glit) ease-in-out both;}
.stp-glit .stp-spark{position:absolute;opacity:0;transform:translate(-50%,-50%) scale(0);fill:#FFD54F;filter:drop-shadow(0 0 3px rgba(255,214,0,.9));overflow:visible;}
.stp-glit .stp-spark circle{fill:#FFF8DC;}
.stp-glit.on .stp-spark{animation:stpSpark .65s ease-in-out both;}
@keyframes stpSpark{0%{transform:translate(-50%,-50%) scale(0) rotate(0deg);opacity:0;}45%{transform:translate(-50%,-50%) scale(1) rotate(60deg);opacity:1;}100%{transform:translate(-50%,-50%) scale(0) rotate(120deg);opacity:0;}}
@keyframes stpGlow{0%{opacity:0;}35%{opacity:1;}100%{opacity:0;}}
/* the hand-over from the letter page: its veil's colour over the table, lifting as this page starts */
.stp-veil{left:0;top:0;width:1280px;height:720px;background:#FDE9A8;pointer-events:none;transition:opacity .6s ease-out;}
.stp.lit .stp-veil{opacity:0;}
"""
sent_css = """
/* ===== [sent-fig] G4, P1 + P2 = the reference game's Page 11 (P4, https://hi-02-h04-l01-s01-dun.vercel.app/), SENT_PICK: its rules,
   read from the live page (CSSOM) and scoped to .stage.sent-page, so no other page changes. The picture bare at 315px high
   (its grey frame is in the bitmap), one row of three white sentence pills (344x78, 28px Baloo 2 ExtraBold, 3px #DADADA,
   18px corners), the 114.5px side padding that makes the row 1104 wide; the right pill's green ring, the read-out's lift,
   the orange word, the picture's pops, the reveal's grey decoys and the bobbing hand. ===== */
/* the header in P4's look (computed styles diffed against the live P4): the engine's own header variables set to P4's values —
   the band #DCEEFF with its 3px #B7DCFB edge and 75 / 10 padding, Swiftie's head 118px (P4's header row is 140 high, ours 150 by
   default) — then what the variables do not reach: the chip at 94.5,80 (on Swiftie's shoulder, in front), the title 32px
   ExtraBold #0B3D8C on a 1.15 line, and P4's paler stage */
.stage.sent-page{--band-bg:#DCEEFF;--band-edge:#B7DCFB;--band-pad-l:75px;--band-pad-r:10px;--mascot-size:118px;--hint-size:60px;--hint-right:128px;
  background-color:#F6FBFF;}
.stage.sent-page .header-row{height:140px;}
.stage.sent-page #audioChip{left:94.5px;top:80px;z-index:60;}
.stage.sent-page #audioChip svg{overflow:visible;}
.stage.sent-page #audioChip svg > g[filter]{filter:none !important;}   /* P4's chip: no SVG shadow under its white ring */
.stage.sent-page #audioChip.vo-disabled{opacity:.5 !important;filter:grayscale(1) brightness(1.2) !important;}   /* and greyed while a line speaks */
.stage.sent-page #promptText{font-weight:800;line-height:1.15;color:#0B3D8C;}   /* [baloo-font] P4's own Baloo 2 ExtraBold again (the reference T1's face; [sent-font] had made it Noto SemiBold) */
/* Swiftie's animated faces (try again, hint, happy) stay inside P4's round frame — the engine's own rule drops the frame for them */
.stage.sent-page .mascot-wrap.anim .mascot-circle{overflow:hidden !important;background:#9DDBF5 !important;border:4px solid #FFFFFF !important;
  box-shadow:0 6px 14px rgba(0,47,118,.2) !important;}
.stage.sent-page .mascot-wrap.anim .mascot-circle .mascot-img{position:absolute !important;inset:0 !important;width:110px !important;height:110px !important;
  object-fit:cover !important;}
.stage.sent-page .slide-stage{padding-left:114.5px;padding-right:114.5px;}
.stage.sent-page .story-q-stim.sq-bare{display:flex;align-items:center;gap:24px;flex-shrink:0;padding:0;background:transparent;border:0;
  box-shadow:none;border-radius:20px;margin-bottom:0;cursor:default;}
.stage.sent-page .story-q-stim.sq-bare .story-q-thumb{height:315px;width:auto;max-width:none;aspect-ratio:auto;object-fit:contain;
  border-radius:26px;box-shadow:none;}
.stage.sent-page .opt-grid.sent-opts{place-content:center;align-items:center;padding-top:6px;grid-template-columns:repeat(3, auto) !important;
  gap:36px !important;min-height:0 !important;max-width:none;}
.stage.sent-page .opt-grid.sent-opts .opt-cell{width:auto !important;max-width:none !important;min-height:0 !important;height:auto !important;
  padding:0 !important;background:transparent !important;box-shadow:none !important;border:0 !important;border-radius:0 !important;
  display:flex !important;flex-direction:row !important;align-items:center !important;gap:8px !important;justify-self:center;}
.stage.sent-page .sent-opt .so-pill{display:flex;flex-direction:row;flex-shrink:1;gap:normal;align-items:center;justify-content:center;width:344px;min-height:78px;max-width:900px;
  box-sizing:border-box;padding:10px 12px;font-family:var(--font-hi);font-size:28px;font-weight:800;line-height:1.2;color:var(--navy);   /* [baloo-font] P4's own face, size and line again */
  text-align:center;white-space:nowrap;background:#FFFFFF;border:3px solid #DADADA;border-radius:18px;box-shadow:0 4px 14px rgba(11,42,90,.1);
  transition:transform .28s;}
.stage.sent-page .sent-opt .so-pill .p2-words{display:inline;}
.stage.sent-page .sent-opt .so-pill .p2-word{display:inline-block;border-radius:10px;padding:0 .12em;margin:0 -.12em;transform-origin:50% 60%;}
.stage.sent-page .sent-opt .so-pill .p2-word.on{color:#E86A00;animation:p2WordPop .28s ease-out 1;}
.stage.sent-page .sent-opt .so-pill.p6-say{transform:scale(1.05);transition:transform .32s cubic-bezier(.34,1.6,.6,1);}
.stage.sent-page .opt-grid.sent-opts .opt-cell.opt-guided .so-pill,
.stage.sent-page .opt-grid.sent-opts .opt-cell.correct .so-pill{outline:6px solid var(--correct);outline-offset:-1px;}
.stage.sent-page .opt-grid.sent-opts .opt-cell .ck-fx,.stage.sent-page .opt-grid.sent-opts .opt-cell .wg-fx{border-radius:18px;}
/* a wrong pill: only the wiggle — P4's red ring on it is transparent, and the engine's greyed "crossed" look does not apply here */
.stage.sent-page .opt-grid.sent-opts .opt-cell.wg-wrong .so-pill,.stage.sent-page .opt-grid.sent-opts .opt-cell.wg-rel .so-pill{outline:6px solid transparent;outline-offset:-1px;}
.stage.sent-page .opt-grid.sent-opts .opt-cell.crossed{opacity:1 !important;filter:none !important;}
/* a tap while a line speaks counts on P4 (it cuts the line): the engine's vo-lock must not swallow it here (the module gates its own beats) */
body.vo-lock .stage.sent-page .opt-grid.sent-opts .opt-cell:not(.opt-dim):not(.crossed){pointer-events:auto !important;}
.stage.sent-page .opt-grid.sent-opts .opt-cell.crossed{pointer-events:none !important;}   /* as P4's: a crossed pill is dead until it is un-crossed */
/* P4's pills: the plain 3px hover lift (not the toybox theme's lift + scale) and no pop on the green mark */
.stage.sent-page .opt-grid.sent-opts .opt-cell:hover{transform:translateY(-3px);}
.stage.sent-page .opt-grid.sent-opts .opt-cell.correct{animation:none;}
.stage.sent-page .opt-grid.sent-opts .opt-cell.opt-dim{filter:grayscale(1) !important;opacity:.5 !important;pointer-events:none !important;cursor:default !important;}
.stage.sent-page .story-q-stim .story-q-thumb.p2-pop{animation:p2BirdPop1s 1s ease-in-out 1 both;transform-origin:50% 50%;will-change:transform;}
.stage.sent-page .story-q-stim .story-q-thumb.p6-pop:not(.p2-pop){animation:p6PromptPop 3.2s ease-in-out 1 both;transform-origin:50% 50%;will-change:transform;}
.stage.sent-page .reveal-hand{position:absolute;width:96px !important;height:96px !important;z-index:55;object-fit:contain;
  filter:drop-shadow(0 6px 10px rgba(0,0,0,.22));animation:guidedHandBob 1s ease-in-out infinite;}
@keyframes p2WordPop{0%{transform:scale(1);}45%{transform:scale(1.1);}100%{transform:scale(1);}}
@keyframes p2BirdPop1s{0%{transform:scale(1);animation-timing-function:cubic-bezier(.2,.8,.3,1);}20%{transform:scale(1.045);animation-timing-function:ease-in-out;}
  32%{transform:scale(1.03);animation-timing-function:linear;}72%{transform:scale(1.03);animation-timing-function:ease-in-out;}100%{transform:scale(1);}}
@keyframes p6PromptPop{0%{transform:scale(1);animation-timing-function:cubic-bezier(.2,.8,.3,1);}6.25%{transform:scale(1.045);animation-timing-function:ease-in-out;}
  10%{transform:scale(1.03);animation-timing-function:linear;}86%{transform:scale(1.03);animation-timing-function:ease-in-out;}100%{transform:scale(1);}}
@keyframes guidedHandBob{0%,100%{transform:translateY(2px);}50%{transform:translateY(-14px);}}
"""
css = (ref_css
       + "\n\n/* ===== [reskin] PORTED FROM THE HI02H12_L01_S01 ENGINE: evidence / sort / punctuation modules ===== */\n"
       + mod_css
       + "\n/* ===== [reskin] from the reference's ocean-games.css: wrong-answer feedback is motion-only ===== */\n"
       + feedback_rules + fit_rules + title_css + story_css + recap_css + demo_css + sent_css + letter_css + stamp_css)

# ---------- 6. index.html ----------
body = ref_body
body = sub1(body, r'<div class="sg-card has-title-art has-title-video">', '<div class="sg-card">', 0, "sg-card classes")
body = sub1(body, r'\n\s*<video class="sg-bg-video".*?</video>', "", re.S, "title video")
body = sub1(body, r'\n\s*<img class="sg-title-art"[^>]*>', "", 0, "title art")
body = sub1(body, r'\n\s*<img class="sg-birthday-girl"[^>]*>', "", 0, "birthday girl")
body = sub1(body, r'<div class="sg-title" id="sgTitle">[^<]*</div>', '<div class="sg-title" id="sgTitle">%s</div>' % title_hi, 0, "sgTitle")
# [title-fig] the landing becomes the Figma "Title Page" frame; the engine's own controls are carried over
gate = must(r"  <!-- TAP-TO-START.*?(?=  <!-- END / CELEBRATION -->)", body, re.S, "start gate block").group(0)
sg_content = must(r'<div class="sg-content">.*?<div class="sg-art" id="sgHero"></div>\s*</div>', gate, re.S, "sg-content").group(0)
sg_vo  = must(r'<button class="sg-vo".*?</button>', gate, re.S, "sg-vo").group(0)
sg_btn = must(r'<button class="sg-btn".*?</button>', gate, re.S, "sg-btn").group(0)
new_gate = f"""  <!-- TAP-TO-START — the Figma "Title Page" frame (FLN-by-MJ, node 386:17), built in its own 1280x720 px
       and scaled onto the 1333x750 stage, so every element keeps the frame's placement and size. -->
  <div class="start-gate" id="startGate">
    <div class="sg-fig">
      <div class="sg-card">
        <img class="sgf-scene" src="assets/UI/title_scene.png" alt="" draggable="false">
        <div class="sg-fx" aria-hidden="true"><div class="sg-sun"></div><div class="sg-flare2"><i class="fl-big"></i><i class="fl-violet"></i><i class="fl-haze"></i><i class="fl-glint"></i></div><canvas class="sg-dust" id="sgDust"></canvas></div>   <!-- [cover-fx] the mtcg cover's lens flare and sunlit dust: over the scene, under all else -->
        <img class="sgf-question" src="assets/UI/title_char_question.png" alt="" draggable="false">
        <img class="sgf-title" src="assets/UI/title_art.png" alt="{title_hi}" draggable="false">
        <img class="sgf-shadow s1" src="assets/UI/title_shadow_1.svg" width="132" height="69" alt="" draggable="false">
        <img class="sgf-shadow s2" src="assets/UI/title_shadow_2.svg" width="142" height="64" alt="" draggable="false">
        <img class="sgf-shadow s3" src="assets/UI/title_shadow_3.svg" width="115" height="69" alt="" draggable="false">
        <div class="sgf-purn"><img src="assets/UI/title_char_purn.png" alt="" draggable="false"></div>
        <img class="sgf-comma" src="assets/UI/title_char_comma.png" alt="" draggable="false">
        {sg_content}
        {sg_btn}
      </div>
      <img class="sgf-swiftie" id="sgSwiftie" src="assets/UI/title_swiftie_hello.png" alt="Swiftee" draggable="false">
      <img class="sgf-swiftie-anim" id="sgSwiftieAnim" data-src="assets/UI/new_landing_swiftee_anim.webp" alt="" draggable="false">
      {sg_vo}
    </div>
  </div>

"""
body = body.replace(gate, new_gate)

# ---------- [dun-chrome] (asked 2026-10-27) THE CHROME OF https://hi-02-h04-l01-s01-dun.vercel.app/ (HI02H04_L01_S01; the local
#            copy under "Suresh's File/HI02H04_L01_S01-20260916T080241Z-1-001" is byte-identical to the live page). The seven asks,
#            value for value from that page's own code (its blocks are kept verbatim in dun_assets/blocks/, read here):
#   1. the cover: the FLN animation kit's sky (breathing glow + 87 drifting stars, a hole over the card, stars that pop on a tap) over
#      the reference's plain sunburst (startnew_bg_plain.webp — its painted stars removed, so the moving ones are the only ones); the
#      play button = the reference's gold disc (btn-play.svg) 140x140 centred 2 px above the card's bottom, hidden until the welcome
#      has been heard, then popping in (sgBtnReveal) and breathing (sgBtnPulse), the standard play sound at 0.8 on the tap, which
#      cuts the welcome and opens the tutorial gate (no bgm yet: the bed starts with page 1); the reference's bird (its own wave
#      file, 208 px at the card's bottom-left, tappable = the welcome again) and its speaker chip at the bird's feet (70 px, grey
#      until the play button is ready and while a line speaks);
#   2. आगे = the reference's pill + arrow art (btn-next(-disabled)-pill/-arrow.svg, 170x62 on the tutorial pages, 190x62 elsewhere, in
#      the places this file already gives it), the disabled art showing wherever the button exists, the enabled art fading in over
#      it with navBreathe (1.4 s, 1.04), the standard next sound at 0.9;
#   3. the bird: the title bars' circles carry the engine's live head (the mascot image mirrored into every .dmf-head), so it
#      celebrates on a right tap, tries again on a wrong one and rests on the talking head — inside the circle, as the reference's
#      (not popping out of it); the header bird of G4/P1/P2 at the reference's 118 px; the cover's and the gates' and the
#      celebration's birds are the reference's own files (items 1, 5, 7);
#   4. the speaker chips: the glyph is already the reference's (the inline SVG is byte-identical); the cover chip at the bird's feet
#      as above; the header chip (G4/P1/P2) at the bird's shoulder with the reference's grey-while-a-line-speaks look (already so);
#      waves blink while a line speaks, solid at rest (already so);
#   5. the gates = [GATE-REF-ANIM]: the reference's peeking bird (peeking_talk_up.webp, 52.8 % of the screen, lifted in over 0.3 s),
#      the headline writing itself left to right the moment the line says its words (this lesson's own clips: 2850 / 3540 / 210 ms
#      into vo_pt_tutorial / _guided / _practice, read off them), a 4 s minimum hold, the first gate's bird sinking back; the
#      scrim at .35 over a plain blue field, the sky off while gating; confetti = [CONFETTI-REF]: 100 pieces, 1.5x, falling 1.6-2.6 s
#      over the whole window under the gate (z 5000), the standard confetti sound at 0.45;
#   6. the music bed = [BGM-DUCK]: the same track (standard_background_music_2.mp3 is bgm_standard_2 note for note), from page 1's
#      mount to the last page before the celebration, 0.13 at rest, ducked to 0.03 under ANY sound (voice, sfx, the letter page's
#      piano loop, the kit's pops; ramps 180 ms down / 600 ms up), faded out on the celebration, never on the cover;
#   7. the celebration = the reference's: its sunburst (end_screen.webp), the three-sheet Swiftie (cel_shabaash / talk / idle:
#      the jump, the landing, the line lip-synced on the talk sheet, then the idle loop), the standard confetti sound, the star
#      burst, no text, the gold arrow pill that waits dim while she speaks and then pulses; full-bleed (the screen is moved to
#      <body>). The LINE is this lesson's own (vo_celebrate; its beak bits derived the way the reference's were: dun_assets/
#      cel_bits.json), not the reference's vo_well_done.
#   Everything else is untouched. The sounds: the reference's sfx_std_play / next / confetti ARE this engine's sfx_play_button /
#   sfx_next_button / sfx_celebrate (correlation 1.000), so only their volumes change. ----------
DUN = SCR / "dun_assets"
dun_block = lambda name: "".join(l for l in (DUN / "blocks" / name).read_text(encoding="utf-8").splitlines(True)
                               if not re.match(r"\s*</?(script|style)[\s>]", l))   # the blocks are cut from the page: a stray tag line is dropped
dun_bits = json.loads((DUN / "cel_bits.json").read_text(encoding="utf-8"))
dun_ea = json.loads((DUN / "end_anim_ref.json").read_text(encoding="utf-8"))
DUN_UI = ["btn-play.svg", "btn-play-waiting.svg", "btn-next-pill.svg", "btn-next-arrow.svg", "btn-next-disabled-pill.svg", "btn-next-disabled-arrow.svg",
          "peeking_talk_up.webp", "cel_shabaash.webp", "cel_talk.webp", "cel_idle.webp", "end_screen.webp", "new_landing_swiftee_anim.webp",
          "bgdeco_star.svg", "bgdeco_star_o.svg", "bgdeco_spark.svg", "startnew_bg_plain.webp", "sw_lg_celebrating_anim.webp"]
# 1. the assets (the Ek-aur-Anek versions of the files that get overwritten are kept once in dun_assets/_replaced/)
_dun_kept = DUN / "_replaced"; _dun_kept.mkdir(exist_ok=True)
for name in DUN_UI:
    src, dst = DUN / "UI" / name, DIST / "assets" / "UI" / name
    assert src.exists(), f"missing dun asset {src}"
    if dst.exists() and dst.read_bytes() != src.read_bytes() and not (_dun_kept / name).exists(): shutil.copy2(dst, _dun_kept / name)
    if not dst.exists() or dst.read_bytes() != src.read_bytes(): shutil.copy2(src, dst)
# 2. the card: the celebration's sprite data (the reference's sheets, this lesson's line) and its standard confetti sound
card["end_anim"] = {"cols": dun_ea["cols"], "fw": dun_ea["fw"], "fh": dun_ea["fh"], "step_ms": dun_bits["step_ms"], "bits": dun_bits["bits"], "vo": dun_bits["vo"],
                    "shabaash": dun_ea["shabaash"], "talk": dun_ea["talk"], "idle": dun_ea["idle"]}
_cel = next(s for s in card["slides"] if s["type"] == "CELEBRATION"); _cel.setdefault("audio", {})["sfx"] = "sfx_std_confetti"
# ---------- [cel-vo] (asked 2026-10-28: "apply the exact same VO, bird animation and the finish button at the celebration screen as the
#            reference"). Probed side by side (the scratchpad's cel_probe.py): the bird (cel_shabaash -> cel_talk -> cel_idle, the
#            jump, the landing at ~1.9 s, 314x420 at 509.5,79 at rest) and the finish button (the gold pill 133.6x88 at 599.7,521,
#            4 px white ring, the arrow glyph, grey + untappable while she speaks, then celArrowPulse 1.3 s; the tap = the standard
#            next sound at 0.9 and the hand-over) were already the reference's ([dun-chrome] 7); the ONE difference was the LINE:
#            this lesson's vo_celebrate (4.7 s) in place of the reference's vo_well_done ("बहुत बढ़िया, दोस्त! तुमने कमाल कर दिया!",
#            2.94 s). Now the reference's own clip (dun_assets/Audio/vo_well_done.ogg: its wav re-containered to this engine's
#            Opus-48k .ogg, nothing resampled in time) with the reference card's own beak bits (dun_assets/cel_bits_ref.json,
#            117 x 25 ms) and text; the arrow therefore goes live when THIS line ends (~4.9 s in, as there). vo_celebrate.ogg stays
#            in assets/Audio, unused. ----------
_ref_bits = json.loads((DUN / "cel_bits_ref.json").read_text(encoding="utf-8"))
_src, _dst = DUN / "Audio" / "vo_well_done.ogg", DIST / "assets" / "Audio" / "vo_well_done.ogg"
assert _src.exists(), f"missing {_src}"
if not _dst.exists() or _dst.read_bytes() != _src.read_bytes(): shutil.copy2(_src, _dst)
card["assets"]["audio"]["vo_well_done"] = "assets/Audio/vo_well_done.ogg"
card["assets"]["audio_text"]["vo_well_done"] = _ref_bits["text"]
_cel["audio"]["prompt"] = "vo_well_done"; _cel["prompt_hi"] = _ref_bits["text"]
card["end_anim"]["vo"] = "vo_well_done"; card["end_anim"]["bits"] = _ref_bits["bits"]; card["end_anim"]["step_ms"] = _ref_bits["step_ms"]
# 3. the markup: the play button, the cover bird, आगे and the celebration screen as the reference draws them
body = sub1(body, r'<button class="sg-btn" id="sgBtn"[^>]*>.*?</button>',
            '<button class="sg-btn" id="sgBtn" type="button" aria-label="शुरू करें">शुरू करें</button>', re.S, "dun: #sgBtn markup")
body = sub1(body, r'<img class="sgf-swiftie" id="sgSwiftie"[^>]*>\s*<img class="sgf-swiftie-anim" id="sgSwiftieAnim"[^>]*>',
            '<img class="sg-mascot" id="sgMascot" data-src="assets/UI/new_landing_swiftee_anim.webp" alt="Swiftee" draggable="false">', re.S, "dun: cover bird markup")
body = sub1(body, r'<button class="nav-btn" id="navBtn" disabled aria-label="आगे">.*?</button>',
            '<button class="nav-btn" id="navBtn" disabled>आगे</button>', re.S, "dun: #navBtn markup")
body = sub1(body, r'<div class="end-screen" id="endScreen">.*?<button class="end-btn" id="endBtn"[^>]*>.*?</button>\s*</div>',
            """<div class="end-screen" id="endScreen">
    <div class="confetti" id="confetti"></div>
    <h1 class="end-title" id="endTitle"></h1>
    <div class="end-subtitle" id="endSubtitle"></div>
    <img class="end-mascot" src="assets/UI/sw_lg_celebrating_anim.webp" alt="Swiftee"
         onerror="this.replaceWith(Object.assign(document.createElement('span'),{className:'end-mascot',textContent:'🎉'}))">
    <button class="end-btn" id="endBtn" aria-label="आगे बढ़ें"></button>
  </div>""", re.S, "dun: end screen markup")
# 4. the engine: the standard set's volumes; the play tap neither waits for the welcome to end (the reference cuts it) nor starts
#    the music (the bed starts with page 1); the confetti's count and fall; the engine's own music fades become no-ops once the bed
#    owns the element (window.__bgm)
js = sub1(js, r'const sfxConfetti  = \(\)=> playKitSfx\("confetti", "sfx_celebrate\.ogg", \.85\);', 'const sfxConfetti  = ()=> playKitSfx("confetti", "sfx_celebrate.ogg", .45);   // [dun-chrome] STD_SFX_VOL.confetti', 0, "dun: sfxConfetti volume")
js = sub1(js, r'const sfxPlayButton = \(\)=> playKitSfx\("playButton", "sfx_play_button\.ogg", \.85\);', 'const sfxPlayButton = ()=> playKitSfx("playButton", "sfx_play_button.ogg", .8);   // [dun-chrome] STD_SFX_VOL.play', 0, "dun: sfxPlayButton volume")
js = sub1(js, r'const sfxNextButton = \(\)=> playKitSfx\("nextButton", "sfx_next_button\.ogg", \.85\);', 'const sfxNextButton = ()=> playKitSfx("nextButton", "sfx_next_button.ogg", .9);   // [dun-chrome] STD_SFX_VOL.next', 0, "dun: sfxNextButton volume")
js = sub1(js, r'       A second tap once the line ends proceeds normally\. \*/\n    if\(document\.body\.classList\.contains\("vo-lock"\)\) return;\n',
          '       A second tap once the line ends proceeds normally. */\n    /* [dun-chrome] the reference\'s play button takes the tap at once (it is not shown until the welcome has been heard; a replay is cut) */\n', 0, "dun: play tap vo-lock guard")
js = sub1(js, r'    startBackgroundMusic\(\); // user gesture unlocks the looping lesson soundtrack\n', '    /* [dun-chrome] the music bed starts with page 1 (BGM-DUCK), not on the play tap */\n', 0, "dun: bgm start on play")
js = sub1(js, r'const host = document\.body, n = 80, dist = \(window\.innerHeight \|\| 800\) \+ 60;', 'const host = document.body, n = 100, dist = (window.innerHeight || 800) + 60;   // [dun-chrome] CONFETTI-REF: 100 pieces', 0, "dun: confetti count")
js = sub1(js, r'const z = confettiRnd\(\.75,1\.15\), fall = confettiRnd\(1\.1,1\.8\)/z, delay = confettiRnd\(0,\.35\);', 'const z = confettiRnd(.75,1.15), fall = confettiRnd(1.6,2.6)/z, delay = confettiRnd(0,.35);   // [dun-chrome] CONFETTI-REF: the fall 1.6-2.6 s', 0, "dun: confetti fall")
js = sub1(js, r'function fadeBackgroundMusic\(target\)\{\n', 'function fadeBackgroundMusic(target){\n  if(window.__bgm) return;   // [dun-chrome] the bed owns its volume (BGM-DUCK)\n', 0, "dun: fadeBackgroundMusic guard")
js = sub1(js, r'function startBackgroundMusic\(\)\{\n', 'function startBackgroundMusic(){\n  if(window.__bgm) return;   // [dun-chrome] the bed starts itself with page 1 (BGM-DUCK)\n', 0, "dun: startBackgroundMusic guard")
# the celebration's own आगे बढ़ें tap (this engine's: the standard next sound, the completion events, the hand-over) — kept word for word
_cel_click = must(r'      eb\.onclick = \(\)=>\{\n        if\(eb\.dataset\.completed === "1"\) return;.*?\n      \};\n', js, re.S, "dun: CEL onclick").group(0)
_cel_click = _cel_click.replace('        clearTimeout(endVoTimer);\n        clearTimeout(endFreezeTimer);\n        sfxNextButton();\n', '        stdSfx("next");   // [STD-SFX] the end screen\'s आगे बढ़ें is a next button too\n')
assert 'stdSfx("next")' in _cel_click and "endVoTimer" not in _cel_click, "dun: CEL onclick adaptation"
_cel_dev = must(r'      // dev-only: a small "download results" button \(teacher/QA\), never in child flow\n      if\(new URLSearchParams\(location\.search\)\.has\("dev"\) && !\$\("dlResults"\)\)\{.*?\n      \}\n', js, re.S, "dun: CEL dev button").group(0)
# the reference's gate script, on this engine: GameBus for SwiftPAL, this engine's clip path rule, GATE_MS; the caption moments are the
# reference's own (3660 / 3940 / 1120 ms) since [gate-ref-vo] plays the reference's own vo_pt_* clips (before: 2850 / 3540 / 210, this
# lesson's clips)
_gate_js = dun_block("gate_js.js").replace("SwiftPAL.emit", "GameBus.emit")
_gate_js = _gate_js.replace('var voSrc = (voId && CARD.assets && CARD.assets.audio && CARD.assets.audio[voId]) || null;', 'var voSrc = voId ? ("assets/Audio/" + voId + "." + AUDIO_EXT) : null;   // this engine\'s clip path rule')
_gate_js = _gate_js.replace('  if(typeof phaseBlurTransition !== "function") return;\n', '  if(typeof phaseBlurTransition !== "function") return;\n  var GATE_MS = 4000;                                                          // the reference\'s minimum hold (this engine had no such constant: 2.8 s)\n')
assert "GATE_CAPTION_AT_MS = { tutorial: 3660, guided: 3940, practice: 1120 };" in _gate_js and "var GATE_MS = 4000" in _gate_js and "SwiftPAL" not in _gate_js, "dun: gate adaptation"
_bgm_js = dun_block("bgm_duck_js.js")
_bgm_js = _bgm_js.replace('  var FIRST = 0, LAST = 12;                                                   // T1 .. P6\n', '  var FIRST = 0, LAST = CARD.slides.length - 2;                               // page 1 .. the last page before the celebration\n')
_bgm_js = _bgm_js.replace('var SRC = "assets/Audio/bgm_standard_2.wav", BASE = 0.13', 'var SRC = "assets/Audio/standard_background_music_2.mp3", BASE = 0.13')
_bgm_js = _bgm_js.replace('  window.__bgm = { get el(){ return el; },', '  backgroundMusic = el;                                                       // this engine\'s own handle (its fades are no-ops now; the checks read its volume)\n  window.__bgm = { get el(){ return el; },')
_bgm_js = _bgm_js.replace('  function onSlide(idx){ wanted = idx >= FIRST && idx <= LAST; if(wanted) start(); else if(el) setTarget(0, OUT_MS); }\n',
    '  function onSlide(idx){ var sl = CARD.slides[idx]; wanted = idx >= FIRST && idx <= LAST && !(sl && sl.no_bgm);   // [l1-quiet] a slide flagged no_bgm (L1, the letter page) has no bed: it fades out (OUT_MS) at that mount and starts again, as on the first page, when the next page mounts\n'
    '    if(wanted) start(); else if(el) setTarget(0, OUT_MS); }\n')   # [l1-quiet]
assert "LAST = CARD.slides.length - 2" in _bgm_js and "standard_background_music_2.mp3" in _bgm_js and "backgroundMusic = el;" in _bgm_js and "!(sl && sl.no_bgm)" in _bgm_js, "dun: bgm adaptation"
_cel_js = dun_block("cel_swiftie_js.js")
# [cover-eyes] / [cover-fx] (2026-10-29): the title page's live eyes and ambient light, the mtcg2a04l02 game's [pencil eyes] rig and
# [landing dust] + lens flare (title_assets/cover_eyes_js.js, cover_dust_js.js, cover_fx.css); the faces' geometry comes from
# title_eyes_measure.py (title_assets/cover_eyes_data.json, in each picture's art px) and is injected as the rig's FACES
_eyes_data = json.loads((SCR / "title_assets" / "cover_eyes_data.json").read_text(encoding="utf-8"))
_FACE_SEL = {"purn": ".sgf-purn img", "comma": ".sgf-comma", "question": ".sgf-question"}
_faces = []
for _n in ("purn", "comma", "question"):
    _d = _eyes_data[_n]
    _faces.append({"sel": _FACE_SEL[_n], "art": _d["art"], "face": _d["face"], "rig": f"assets/UI/title_char_{_n}_rig.png",
                   "eyes": [{"cx": e["cx"], "cy": e["cy"], "a": e["a"], "b": e["b"], "ring": round(0.06 * e["a"], 1),   # the outline's width: 6 % of the eye (the pencil's 4.8 on 48)
                             "iris": e["iris_r"], "pupil": e["pupil_r"], "shines": e["shines"], "lid": e["lid"]} for e in _d["eyes"]],
                   "brows": [{"clean": b["clean"], "brow": b["brow"], "box": b["box"], "c": b["c"], "tilt": 1 if i == 0 else -1} for i, b in enumerate(_d["brows"]) if b]})
_eyes_js = (SCR / "title_assets" / "cover_eyes_js.js").read_text(encoding="utf-8").replace("__FACES__", json.dumps(_faces, ensure_ascii=False))
_dust_js = (SCR / "title_assets" / "cover_dust_js.js").read_text(encoding="utf-8")
cover_fx_css = (SCR / "title_assets" / "cover_fx.css").read_text(encoding="utf-8")
assert "__FACES__" not in _eyes_js and len(_faces) == 3 and all(len(f["eyes"]) == 2 and len(f["brows"]) == 2 for f in _faces), "cover-eyes: faces"
assert "SlideModules.CELEBRATION" in _cel_js and "runCelSprite" in _cel_js, "dun: cel block"
dun_js = r"""

/* ===== [dun-chrome] the chrome of HI02H04_L01_S01 (hi-02-h04-l01-s01-dun.vercel.app) on this lesson — see build.py ===== */
""" + dun_block("kit_core.js") + dun_block("sky_js.js") + r"""
/* ---- [STD-SFX] the standard set's volumes, on the three files this engine already ships (= the reference's, correlation 1.000) ---- */
const STD_SFX_VOL = { confetti: 0.45, correct: 0.6, incorrect: 0.6, next: 0.9, play: 0.8 };
function stdSfx(name){
  const f = { play: ["playButton", "sfx_play_button.ogg"], next: ["nextButton", "sfx_next_button.ogg"], confetti: ["confetti", "sfx_celebrate.ogg"],
              correct: ["correct", "sfx_correct_new.ogg"], incorrect: ["wrong", "sfx_wrong_new.ogg"] }[name];
  if(f) playKitSfx(f[0], f[1], STD_SFX_VOL[name] != null ? STD_SFX_VOL[name] : 0.7);
}
/* ---- body.vo-playing: the flag every ported rule reads (= this engine's isPlaying, set and cleared in setPlaying) ---- */
(function(){ "use strict"; const o = window.setPlaying; if(typeof o !== "function") return;
  window.setPlaying = function(on){ const r = o.apply(this, arguments); document.body.classList.toggle("vo-playing", !!on); return r; }; })();
/* ---- the cover: शुरू करें appears only once the welcome has been heard (this engine's landing-play-ready: the landing line has
   played and nothing speaks), pops in (sgBtnReveal) and breathes (.sg-breathe); the chip at the bird's feet follows its readiness
   (.sg-vo-off, [FEET-SPEAKER]); the bird is the reference's wave file, started afresh as the loader fades, a tap on it = the welcome again ---- */
(function(){ "use strict";
  const b = $("sgBtn"), vo = $("sgVo"), bird = $("sgMascot"); if(!b) return;
  b.disabled = false;
  const reveal = ()=>{ if(b.classList.contains("ready")) return; b.disabled = false; b.classList.add("ready");
    let on = false; const breathe = ()=>{ if(on) return; on = true; b.classList.add("sg-breathe"); };
    b.addEventListener("animationend", breathe, { once:true }); setTimeout(breathe, 700); };   // 700 ms fallback: the pop-in is .52 s
  // "heard": the welcome's own element really sounded (its clock moved) — a blocked autoplay plays a silent beat in this engine,
  // and the reference keeps the button hidden then until the first tap has played the welcome (its pointerdown fallback is this
  // engine's too)
  let heard = false;
  const listen = setInterval(()=>{ if(!document.body.classList.contains("is-start")){ clearInterval(listen); return; }
    const a = currentAudio; if(isPlaying && a && !a.paused && a.currentTime > 0.25 && /vo_landing/.test(a.src)){ heard = true; sync(); } }, 100);
  const sync = ()=>{ if(heard && document.body.classList.contains("landing-play-ready")) reveal();
    if(vo){ const off = !b.classList.contains("ready"); vo.classList.toggle("sg-vo-off", off); vo.setAttribute("aria-disabled", String(off)); } };
  new MutationObserver(sync).observe(document.body, { attributes:true, attributeFilter:["class"] });
  new MutationObserver(sync).observe(b, { attributes:true, attributeFilter:["class"] });
  sync();
  if(bird){
    const start = ()=>{ if(bird.getAttribute("src")) return; bird.src = bird.dataset.src + "?r=" + Date.now(); };
    if(document.body.classList.contains("loaded")) start();
    else new MutationObserver((m, o)=>{ if(document.body.classList.contains("loaded")){ start(); o.disconnect(); } }).observe(document.body, { attributes:true, attributeFilter:["class"] });
    setTimeout(start, 4000);
    bird.addEventListener("click", ()=>{ if(vo && !vo.classList.contains("sg-vo-off") && !isPlaying) vo.click(); });
  }
})();
/* ---- the bird in the title bars: every .dmf-head (the demos', the picks', the stamp page's frames) shows the engine's live head —
   the mascot image's src mirrored, so the same celebrate / try-again / hint faces play inside the circle (the reference's header
   bird; setSwMood drives #swBuddyImg exactly as before) ---- */
(function(){ "use strict";
  const live = ()=>{ const im = $("swBuddyImg"); if(!im) return; const want = im.getAttribute("src");
    document.querySelectorAll(".dmf-head img").forEach(h=>{ h.classList.add("dun-live"); if(h.getAttribute("src") !== want) h.setAttribute("src", want); }); };
  const im = $("swBuddyImg"); if(im) new MutationObserver(live).observe(im, { attributes:true, attributeFilter:["src"] });
  const om = window.mountSlide; if(typeof om === "function") window.mountSlide = function(){ const r = om.apply(this, arguments); try{ live(); }catch(e){} return r; };
  live();
})();
/* ---- the celebration screen moves to <body> (full-bleed, the reference's TOTA-END-REPARENT) ---- */
(function(){ function move(){ var e = document.getElementById("endScreen"); if(e && e.parentElement !== document.body) document.body.appendChild(e); }
  move(); setTimeout(move, 300); setTimeout(move, 1200); })();
/* ---- the celebration mount = the reference's (its sound, the sunburst, the star burst, no text, the signals, the button), with this
   engine's own आगे बढ़ें tap; the sprite runner below then takes the mascot's place and speaks the line after the jump ---- */
SlideModules.CELEBRATION.mount = function(host, slide){
  stdSfx("confetti");                                      // [STD-SFX] the standard confetti sound, at 0.45, on its own element
  state.ownsAudio = true;                                  // the line is the sprite runner's (after the jump), never the auto chain's
  const et = $("endTitle"); if(et) et.textContent = "";    // no text on the page: only the button carries writing
  const st = $("endSubtitle"); if(st) st.textContent = "";
  const es = $("endScreen"); es.classList.add("show");
  document.body.classList.add("is-end");                   // the sunburst backdrop (end_screen.webp) and the sky
  const c = $("confetti"); if(c) c.innerHTML = "";
  starBurst();                                             // the gold star burst from the centre
  const masteryScore = state.masteryAttempts ? (state.masteryHits/state.masteryAttempts) : 0;
  GameBus.emit("mastery_score", { value: masteryScore, hits: state.masteryHits, attempts: state.masteryAttempts });
  GameBus.emit("lesson_completed", { skill_code: CARD.skill_code, total_signals: GameBus.signals.length });
  runValidator();
  setNavActive(false);
  document.querySelectorAll(".fx-confetti").forEach(w => w.remove());   // no correct-answer confetti bleeds onto this page
  const eb = $("endBtn"); eb.dataset.completed = "0"; eb.disabled = false; eb.classList.add("show");
  state.endBtnPending = false;
""" + _cel_dev + _cel_click + r"""};
""" + _cel_js + _gate_js + _bgm_js + _dust_js + _eyes_js + r"""
/* ===== [dun-chrome] end ===== */
"""
js = js + dun_js
# ---------- [vo-rec] (asked 2026-10-28: "I have added the folder (voiceovers) which contains all the new VOs so now implement all
#            these VOs to their respective places and it must be sync"). vo_rec.py (run first; it keeps vo_rec/derived.json) heard
#            every recording (faster-whisper), re-containered the ones whose words are the page's into assets/Audio/<Audio ID>.ogg
#            (the manifest's IDs: the build's own slots where a line already had one, new IDs for the deck's lines the build never
#            played), cut the letter's last block into rounds 4 and 5, re-derived every synced line's word times from the clip's
#            own words, and read the gate's caption cue off vo_pt_tutorial. Here: the card learns the new IDs and the deck's beats
#            get their places —
#   T0 the story: "आइए इन वाक्यों को सुनते हैं।" (vo_story_s0) before the run-on (STORY_LISTEN intro_audio); the run-on and the re-read
#      keep their TTS lines: the story recordings (1-4.wav, vo_story_s1, vo_story_r1) tell a different, shorter story (derived.json
#      "skipped" has what they say); T0B's intro line (vo_story_r0) is the recording.
#   T1 the recap: the lead line "आपने देखा, ..." (vo_recap_lead, MARKS_RECAP lead_audio) before the intro; the nine row lines recorded
#      and re-synced (the पूर्ण विराम example now "पिंकी स्कूल गई ।", as the voice says it).
#   T2-T4 the demos: the sentence and the full reading recorded and re-synced (T3's and T4's full readings do not name the mark: the
#      slot lights in the voice's pause / at the end); the mark's name at the tile = the recap's recorded names (vo_recap_*_name);
#      the deck's extra lines in their places — T2: the conclusion after the full reading; T3: the explanation after the sentence,
#      "अब दोबारा देखिए ।" before the full reading, the conclusion after it; T4: the explanation and "अब दोबारा देखिए ।". The three
#      intros (the bar's line) have no recording: TTS still.
#   G1-G3 the picks: the intro line (vo_g1_intro) and G2's / G3's sentences recorded (G1's says राजू where the frame shows पिंकी: TTS
#      still); the right tile = "शाबाश!" (vo_ok) in the name's place; the deck's hint ladder on wrong taps: 1st = hint 1
#      (vo_build_hint1), 2nd = hint 2 (vo_build_hint2), 3rd+ = hint 3 (the page's own, vo_g2_hint3 / vo_g3_hint3; G1's says राजू, so
#      hint 2 again there) + the pointing hand under the right tile.
#   G4, P1, P2: the prompts (G4's recorded; P1 / P2 their own, vo_p1_prompt / vo_p2_prompt), the nine option lines recorded and
#      re-synced; the 1st wrong = hint 1 (vo_g4_hint1 / vo_pick_hint1, the try_again slot), the 2nd = the three pills read (the
#      engine's review = the deck's hint 2), the 3rd = hint 3 "यह सही वाक्य है, इसपर टैप कीजिए" (vo_pick_hint3) then the hand;
#      the right pill: "शाबाश! यह सही वाक्य है ।" (vo_ok_pick) then its own line.
#   L1 the letter: the narration (vo_letter_intro) over the girl writing; the scene's beats follow it.
#   L2 the stamps: the instruction recorded; each later round opens with the deck's line for it (rounds 2: vo_stamp_intro again;
#      3: "यह वाक्य सुनकर देखिए ..." = vo_g1_intro; 4 and 5: vo_stamp4_intro) and the idle reminder says that line; the sentences
#      recorded and re-synced (sent4 / sent5 cut from the one take); wrong drops: 1st = the wiggle, 2nd = hint 2, 3rd+ = hint 3
#      (rounds 4 / 5: the open slot's own line by its mark) + the guidance glide to the open slot; the round's last slot = "शाबाश!".
#   The gate: the tutorial caption's cue at the recorded "चलिए". Title: vo_landing recorded. The celebration keeps vo_well_done.
#   Not recorded (TTS still): vo_demo1/2/3_intro, vo_pt_guided, vo_pt_practice, the story's s1 / s2 / r1, G1's sentence. ----------
def rep1(text, old, new, what=""):
    n = text.count(old)
    if n != 1: raise SystemExit(f"[vo-rec] anchor '{what or old[:70]}' found {n} times (need exactly 1)")
    return text.replace(old, new)
VR = json.loads((SCR / "vo_rec" / "derived.json").read_text(encoding="utf-8"))
for vid, text in VR["texts"].items():
    card["assets"]["audio"][vid] = f"assets/Audio/{vid}.ogg"; card["assets"]["audio_text"][vid] = text
    assert (DIST / "assets" / "Audio" / f"{vid}.ogg").exists(), f"[vo-rec] missing {vid}.ogg — run vo_rec.py"
SL = {s["id"]: s for s in card["slides"]}
SL["T0"]["data"]["intro_audio"] = "vo_story_s0"
SL["T0"]["data"]["beat1_sfx"] = "sfx_story_cat.mp3"   # [story-cat] the user's stu9-cute-cat-352656.mp3 (0.89 s, as given): once, as beat 1's line ends, with the picture's pop
SL["T1"]["data"]["lead_audio"] = "vo_recap_lead"
for sid, mk in (("T2", "purn"), ("T3", "prashn"), ("T4", "alp")): SL[sid]["data"]["mark_audio"] = f"vo_recap_{mk}_name"
SL["T2"]["data"]["conclude_audio"] = "vo_demo1_conclude"
SL["T3"]["data"].update({"explain_audio": "vo_demo2_explain", "again_audio": "vo_demo_again", "conclude_audio": "vo_demo2_conclude"})
SL["T4"]["data"].update({"explain_audio": "vo_demo3_explain", "again_audio": "vo_demo_again"})
for sid, mk, h3 in (("G1", "purn", None), ("G2", "prashn", "vo_g2_hint3"), ("G3", "alp", "vo_g3_hint3")):
    SL[sid]["data"].update({"mark_audio": f"vo_recap_{mk}_name", "ok_audio": "vo_ok", "hint1_audio": "vo_build_hint1", "hint2_audio": "vo_build_hint2", "hint3_audio": h3})
SL["G4"]["audio"].update({"try_again": "vo_g4_hint1", "hint3": "vo_pick_hint3", "ok": "vo_ok_pick"})
SL["G4"]["data"]["tap_sfx"] = "sfx_g4_giggle.mp3"   # [g4-giggle] the user's jule_joule-giggling-like-a-little-girl-322689.mp3 (1.06 s, as given) with the right tap's pop
SL["P1"]["audio"].update({"prompt": "vo_p1_prompt", "try_again": "vo_pick_hint1", "hint3": "vo_pick_hint3", "ok": "vo_ok_pick"})
SL["P1"]["data"]["tap_sfx"] = "sfx_p1_book.mp3"   # [p1-book] the user's soumages-book-opening-345808.mp3 (1.10 s, as given) with the right tap's pop, as G4's giggle
SL["P2"]["audio"].update({"prompt": "vo_p2_prompt", "try_again": "vo_pick_hint1", "hint3": "vo_pick_hint3", "ok": "vo_ok_pick"})
SL["P2"]["data"]["tap_sfx"] = "sfx_p2_pencils.mp3"   # [p2-pencils] the user's freesound_community-pencils-shake-throw-33800.mp3 (17.3 s, as given) with the right tap's pop, as G4's giggle
SL["P2"]["data"]["tap_sfx_from"] = 0.51   # [p2-pencils] the file is silent until 0.52 s: it starts just before its first shake, so the sound lands with the pop (the reference's 1 s rule then plays that first second)
SL["L1"]["data"]["intro_audio"] = "vo_letter_intro"
SL["L1"]["no_bgm"] = True   # [l1-quiet] no music bed on the letter page: it fades out as L1 mounts and starts again (a 0.6 s fade-in) as L2 mounts after the envelope's dive
_rounds = SL["L2"]["data"]["rounds"]; SL["L2"]["data"]["ok_audio"] = "vo_ok"
_by_mark = {"।": "vo_stamp4_hint3_purn", "?": "vo_stamp4_hint3_prashn", ",": "vo_stamp4_hint3_alp"}
_rounds[0].update({"hint2_audio": "vo_stamp1_hint2", "hint3_audio": "vo_stamp1_hint3"})
_rounds[1].update({"intro_audio": "vo_stamp_intro", "hint2_audio": "vo_stamp2_hint2", "hint3_audio": "vo_stamp2_hint3"})
_rounds[2].update({"intro_audio": "vo_g1_intro", "hint2_audio": "vo_stamp3_hint2", "hint3_audio": "vo_stamp3_hint3"})
_rounds[3].update({"intro_audio": "vo_stamp4_intro", "hint2_audio": "vo_stamp4_hint2", "hint3_by_mark": _by_mark})
_rounds[4].update({"intro_audio": "vo_stamp4_intro", "hint2_audio": "vo_stamp4_hint2", "hint3_by_mark": _by_mark})
# the JS: the story's intro line
js = rep1(js, "      state.replayAudio = start;\n      start();\n",
"""      state.replayAudio = start;
      // [vo-rec] "आइए इन वाक्यों को सुनते हैं।" (data.intro_audio) before the story; the chip waits it out
      const introSrc = d.intro_audio ? ("assets/Audio/" + d.intro_audio + "." + AUDIO_EXT) : null;
      if(introSrc){ state.demoRunning = true; let introDone = false;
        const go = ()=>{ if(introDone || !alive()) return; introDone = true; state.demoRunning = false; start(); };
        play(introSrc, go); setTimeout(()=>{ if(!introDone && alive()){ stopAudio(); go(); } }, authoredVoHoldMs(introSrc) + 10000); }
      else start();
""", "story intro")
# the recap's lead line before its intro
_recap_tail = """      play(introSrc, afterIntro);
      // the title starts the moment the clip's own clock starts moving ("playing" fires ~0.15 s before that)
      const a = currentAudio;
      const whenSounding = ()=>{
        if(!alive() || title.classList.contains("in")) return;
        if(a === currentAudio && a.currentTime > 0) showTitle(); else nextFrame(whenSounding);
      };
      if(a && introSrc && decodeURIComponent(String(a.src).split("/").pop()) === introSrc.split("/").pop()) whenSounding(); else showTitle();
      setTimeout(showTitle, 1500);   // a clip that is slow to start never keeps the title away
      // watchdog, as sfigNarrate's: an intro clip that never reports its end must not strand the page
      setTimeout(()=>{ if(!introDone && alive()){ stopAudio(); afterIntro(); } }, authoredVoHoldMs(introSrc) + 10000);
      state.replayAudio = readAll;
    }
  },

  /* ===== [demo-fig] PUNCT_DEMO"""
js = rep1(js, _recap_tail,
"""      // [vo-rec] the lead line ("आपने देखा, ...", data.lead_audio) first, the title still out; then the intro as before
      const startIntro = ()=>{
        if(!alive()) return;
        play(introSrc, afterIntro);
        // the title starts the moment the clip's own clock starts moving ("playing" fires ~0.15 s before that)
        const a = currentAudio;
        const whenSounding = ()=>{
          if(!alive() || title.classList.contains("in")) return;
          if(a === currentAudio && a.currentTime > 0) showTitle(); else nextFrame(whenSounding);
        };
        if(a && introSrc && decodeURIComponent(String(a.src).split("/").pop()) === introSrc.split("/").pop()) whenSounding(); else showTitle();
        setTimeout(showTitle, 1500);   // a clip that is slow to start never keeps the title away
        // watchdog, as sfigNarrate's: an intro clip that never reports its end must not strand the page
        setTimeout(()=>{ if(!introDone && alive()){ stopAudio(); afterIntro(); } }, authoredVoHoldMs(introSrc) + 10000);
      };
      const leadSrc = d.lead_audio ? ("assets/Audio/" + d.lead_audio + "." + AUDIO_EXT) : null;
      if(leadSrc){ let leadDone = false; const go = ()=>{ if(leadDone || !alive()) return; leadDone = true; startIntro(); };
        play(leadSrc, go); setTimeout(()=>{ if(!leadDone && alive()){ stopAudio(); go(); } }, authoredVoHoldMs(leadSrc) + 10000); }
      else startIntro();
      state.replayAudio = readAll;
    }
  },

  /* ===== [demo-fig] PUNCT_DEMO""", "recap lead")
# [tap-lock] (2026-10-28) the engine: (1) a page's pointing hand never outlives its page — the picks' and the sentence picks'
# hands are appended to .slide-stage, which clearHost() leaves alone, so a dev-nav jump kept them on the next page (T1's CSS even
# blew the sentence picks' up to 405x508); (2) sfxBusy(): is a sound effect sounding? Every effect path (playSfx, the kit's
# playKitSfx, the procedural _tone) marks itself busy for its length, so the picks can refuse taps while an effect — not only
# a line — plays.
js = rep1(js, "  const slide = CARD.slides[idx];\n  clearHost();\n",
              "  const slide = CARD.slides[idx];\n  clearHost();\n"
              "  document.querySelectorAll(\".slide-stage .reveal-hand\").forEach(h=> h.remove());   // [tap-lock] no page's pointing hand outlives it\n", "tap-lock: strays")
js = rep1(js, "function playSfx(id){\n  if(!id) return;\n  try{\n    const a = new Audio(\"assets/Audio/\" + id + \".\" + AUDIO_EXT);\n",
              "/* [tap-lock] is a sound effect sounding? The picks (G1-G3) and the sentence picks (G4 / P1 / P2) take no tap while an effect\n"
              "   or a feedback line plays; each effect path marks itself busy for its length (a 6 s cap in case 'ended' never comes). */\n"
              "let _sfxBusy = 0, _sfxUntil = 0;\n"
              "function sfxTrack(a){ if(!a) return; let done = false; const end = ()=>{ if(done) return; done = true; _sfxBusy = Math.max(0, _sfxBusy - 1); };\n"
              "  _sfxBusy++; a.addEventListener(\"ended\", end, { once: true }); a.addEventListener(\"error\", end, { once: true }); setTimeout(end, 6000); }\n"
              "function sfxBusy(){ return _sfxBusy > 0 || performance.now() < _sfxUntil; }\n"
              "function playSfx(id){\n  if(!id) return;\n  try{\n    const a = new Audio(\"assets/Audio/\" + id + \".\" + AUDIO_EXT);\n    sfxTrack(a);   // [tap-lock]\n", "tap-lock: playSfx")
js = rep1(js, "  a.volume = volume == null ? .85 : volume; a.currentTime = 0;\n  const p = a.play(); if(p && p.catch) p.catch(()=>{});\n",
              "  a.volume = volume == null ? .85 : volume; a.currentTime = 0;\n  sfxTrack(a);   // [tap-lock]\n  const p = a.play(); if(p && p.catch) p.catch(()=>{});\n", "tap-lock: playKitSfx")
js = rep1(js, "function _tone(freqs, type, dur, vol){ const c = _ac(); if(!c) return; const t0 = c.currentTime;\n",
              "function _tone(freqs, type, dur, vol){ _sfxUntil = Math.max(_sfxUntil, performance.now() + dur * 1000);   // [tap-lock]\n  const c = _ac(); if(!c) return; const t0 = c.currentTime;\n", "tap-lock: _tone")
# the demos: a line between beats; the explanation, "अब दोबारा देखिए", the conclusion; the picks' "शाबाश!" and hint ladder
js = rep1(js, "        if(times.length) tick();\n      };\n      // 1. the title bar, appearing the moment the intro line starts to sound",
"""        if(times.length) tick();
      };
      // [vo-rec] an optional line between beats (data.explain_audio / again_audio / conclude_audio): a breath, the line, a breath
      const speakThen = (id, then)=>{ const src = A(id); if(!src){ then(); return; } after(350, ()=> narrate(src, [], ()=>{}, ()=> after(300, then))); };
      // [vo-rec] the deck's hint ladder on the picks' wrong taps: 1st = hint 1 (data.hint1_audio), 2nd = hint 2 — each line after the
      // wiggle; the 3rd ([hand-quiet] 2026-10-28): the pointing hand under the right tile until it is tapped, the other two tiles dead
      // and dim, and NO line (hint 3 / data.hint3_audio is no longer spoken; nothing speaks again on the page)
      let hintHand = null;
      const placeHintHand = ()=>{ if(!hintHand || !hintHand.parentNode) return; const st = document.querySelector(".slide-stage"), r = tiles[pick].getBoundingClientRect(), sw = st.getBoundingClientRect();
        const scale = sw.width / st.offsetWidth || 1; hintHand.style.left = ((r.left - sw.left) / scale + r.width / scale / 2 - 48) + "px"; hintHand.style.top = Math.min((r.bottom - sw.top) / scale + 4, st.offsetHeight - 96) + "px"; };
      // the pointing hand under the right tile (the reference's 96px reveal hand): the picks' third wrong tap ([hand-quiet]) and, since
      // [demo-hand] (2026-10-28), the demos' auto tap — it appears as the tile is tapped for the child and leaves as the second reading begins
      const showHand = ()=>{ if(hintHand) return; const st = document.querySelector(".slide-stage"); if(!st) return;
        hintHand = document.createElement("img"); hintHand.className = "reveal-hand dmf-hand"; hintHand.src = "assets/UI/nudge_hand_new.svg"; hintHand.alt = "";
        st.appendChild(hintHand); placeHintHand(); requestAnimationFrame(placeHintHand); };
      const hintLadder = (n)=>{
        if(n >= 3){   // [hand-quiet] the 3rd wrong tap: the hand under the right tile, the other two tiles dead and dim, no line
          showHand();
          tiles.forEach((t, k)=>{ if(k !== pick){ t.onclick = null; t.classList.add("off"); } });   // the wiggle just started runs out on its own
          return;
        }
        const id = n <= 1 ? d.hint1_audio : d.hint2_audio;
        after(500, ()=>{ if(!live || isPlaying) return; if(id){ play(A(id), ()=>{}); fbAudio = currentAudio; } });   // [tap-lock] a hint line is feedback: no tile answers while it speaks
      };
      // 1. the title bar, appearing the moment the intro line starts to sound""", "demo helpers")
js = rep1(js, "after(650, ()=> narrate(L.src, L.times || [], n=> sfigShow(L, n), stage3));",
              "after(650, ()=>{ sfigRise(L); after(SENT_IN_MS, ()=>{ narrate(L.src, [], ()=>{}, ()=> speakThen(d.explain_audio, stage3)); sfigSync(L); }); });   // [vo-rec] the explanation after the sentence; [word-sync] the whole sentence, then its clip with the word light", "demo explain")
js = rep1(js, "after(400 + (marks.length - 1) * gap + 700, stage5);",
              "after(400 + (marks.length - 1) * gap + 700, ()=> speakThen(d.again_audio, stage5));   // [vo-rec] \"अब दोबारा देखिए ।\" before the full reading", "demo again")
js = rep1(js, "        narrate(A(F.audio), F.word_times || [], hot, ()=>{\n          // 6. the slots' boxes go (the marks stay) and the page moves on by itself\n",
              "        narrate(A(F.audio), F.word_times || [], hot, ()=> speakThen(d.conclude_audio, ()=>{   // [vo-rec] the conclusion before the page moves on\n          // 6. the slots' boxes go (the marks stay) and the page moves on by itself\n", "demo conclude")
js = rep1(js, "              completeSlide(true); }); });\n        });\n      }\n    }\n  },\n\n  /* ===== [sent-fig] SENT_PICK",
              "              completeSlide(true); }); });\n        }));\n      }\n    }\n  },\n\n  /* ===== [sent-fig] SENT_PICK", "demo conclude close")
js = rep1(js, "narrate(A(d.mark_audio), [], ()=>{}, ()=> after(PACE.tail, ()=> completeSlide(true)));",
              "if(guided){ after(1700 + (marks.length - 1) * (d.mark_stagger_ms || 300), ()=> completeSlide(true)); return; }   // [hand-quiet] no line after the guided tap\n        narrate(A(d.ok_audio || d.mark_audio), [], ()=>{}, ()=> after(PACE.tail, ()=> completeSlide(true)));   // [vo-rec] \"शाबाश!\" (data.ok_audio) in the name's place", "pick ok")
js = rep1(js, "          setSwMood(\"tryagain\");   // [dun-chrome] the title-bar bird's try-again face, as the reference's header bird\n          return;\n",
              "          setSwMood(\"tryagain\");   // [dun-chrome] the title-bar bird's try-again face, as the reference's header bird\n          hintLadder(state.attempts);   // [vo-rec]\n          return;\n", "pick hints")
js = rep1(js, "        live = false; state.locked = true; state.demoRunning = true;\n",
              "        live = false; state.locked = true; state.demoRunning = true;\n        const guided = !!hintHand;   // [hand-quiet] after the hand: no praise line — the mark, the ding + confetti, 1.7 s, the page moves on\n        if(hintHand){ hintHand.remove(); hintHand = null; }   // [vo-rec]\n", "pick hand off")
# the sentence picks: hint 3's line at the reveal, the praise before the right pill's line
js = rep1(js, "        right.cell.classList.add(\"opt-guided\");\n        GameBus.emit(\"answer_revealed\", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts, reason: \"wrong\" });\n",
              "        right.cell.classList.add(\"opt-guided\");\n        GameBus.emit(\"answer_revealed\", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts, reason: \"wrong\" });\n"
              "        if(audioFor(slide, \"hint3\")){ play(audioFor(slide, \"hint3\"), ()=>{}); fbAudio = currentAudio; }   // [vo-rec] \"यह सही वाक्य है, इसपर टैप कीजिए\" — the hand follows once it is quiet; [tap-lock] feedback: nothing answers while it speaks\n", "sent hint3")
js = rep1(js, "          playCorrectSelect(it.cell); setSwMood(\"happy\");\n          say(it, ()=> after(700, ()=> completeSlide(true)));",
              "          playCorrectSelect(it.cell); setSwMood(\"happy\");\n          const okSrc = audioFor(slide, \"ok\"), readIt = ()=> say(it, ()=> after(700, ()=> completeSlide(true)));   // [vo-rec] \"शाबाश! यह सही वाक्य है ।\" then the pill's own line\n          if(okSrc) play(okSrc, readIt); else readIt();", "sent ok")
# the letter: the narration first, the scene's beats after it
js = rep1(js, "      sound(sfx.magic, 0.6, null);\n      at(P.a_hold, ()=> root.classList.add(\"b-in\"));",
              "      sound(sfx.magic, 0.6, null);\n      const runScene = ()=>{   // [vo-rec] the scene's beats, after the narration\n      at(P.a_hold, ()=> root.classList.add(\"b-in\"));", "letter scene open")
js = rep1(js, "      // 4. the tap: the pop, the zoom to 610:6 over the blurred room (the loop fades out), then the opening and the next page\n      let tapped = false;",
"""      };
      // [vo-rec] the page's narration (data.intro_audio: "पिंकी अपने दादाजी को पत्र में ...") over the girl writing; the scene's beats follow it
      const introSrc = A(d.intro_audio);
      if(introSrc){ let introDone = false; const go = ()=>{ if(introDone || !alive()) return; introDone = true; runScene(); };
        play(introSrc, go); setTimeout(()=>{ if(!introDone && alive()){ stopAudio(); go(); } }, authoredVoHoldMs(introSrc) + 10000); }
      else runScene();
      // 4. the tap: the pop, the zoom to 610:6 over the blurred room (the loop fades out), then the opening and the next page
      let tapped = false;""", "letter narration")
# the stamps: a round's own instruction, the hint ladder, the praise
js = rep1(js, "      let R = null, r = -1;\n", "      let R = null, r = -1, rWrong = 0, hintStamp = null;   // [vo-rec] the round's wrong drops (its hint ladder); the stamp the guidance holds\n", "stamp vars")
js = rep1(js, "hinting = false; hintT = []; lastAct = Date.now();\n      }\n      // 1. the table shows",
              "hinting = false; hintT = []; lastAct = Date.now(); rWrong = 0;\n      }\n      // 1. the table shows", "stamp round reset")
js = rep1(js, "setRound(r + 1); stage3(); });", "setRound(r + 1); roundIntro(stage3); });   // [vo-rec] the round's own instruction first", "stamp round intro call")
js = rep1(js, "      function remind(){\n",
"""      // [vo-rec] a later round opens with its own instruction (rounds[i].intro_audio: the deck's line for that round) before its
      // stamps pop in; the idle reminder says that line too
      const roundSrc = ()=> (R && R.D.intro_audio) ? A(R.D.intro_audio) : introSrc;
      function roundIntro(then){ const src = R && R.D.intro_audio ? A(R.D.intro_audio) : null; if(!src){ then(); return; }
        let done = false; const go = ()=>{ if(done || !alive()) return; done = true; at(P.after_intro, then); };
        play(src, go); at(authoredVoHoldMs(src) + 10000, ()=>{ if(!done){ stopAudio(); go(); } }); }
      function remind(){
""", "stamp roundIntro")
js = rep1(js, "lastAct = Date.now(); play(introSrc, ()=>{ lastAct = Date.now(); });", "lastAct = Date.now(); play(roundSrc(), ()=>{ lastAct = Date.now(); });   // [vo-rec] the round's line", "stamp remind")
_hint_old = """      function hint(){
        if(hinting || solved || drag || !live || !R || R.D.guide === false) return;
        const stamp = R.stamp; hinting = true; hintT = [];
        stamp.classList.add("lift"); move(stamp, R.HOVER, P.glide, "cubic-bezier(.45,0,.2,1)");
        hat(P.glide + P.hold, ()=> move(stamp, "none", P.back, "cubic-bezier(.4,0,.2,1)"));
        hat(P.glide + P.hold + P.back - 150, ()=> stamp.classList.remove("lift"));
        hat(P.glide + P.hold + P.back + 50, ()=>{ hinting = false; lastAct = Date.now(); });
      }
      function stopHint(taken){   // taken = the child took hold of the guiding stamp itself (it stays where it is, in hand)
        if(!hinting) return; hinting = false; hintT.forEach(clearTimeout); hintT = [];
        if(!taken) putBack(R.stamp, 350);
      }"""
js = rep1(js, _hint_old,
"""      function hint(force){   // [vo-rec] force = hint 3's glide in a round without guidance; the glide goes to the OPEN slot's stamp
        if(hinting || solved || drag || !live || !R || (R.D.guide === false && !force)) return;
        const o = R.slots.find(q=> !q.done) || R.slots[0], stamp = o.stamp, HOV = o.HOVER; hinting = true; hintT = []; hintStamp = stamp;
        stamp.classList.add("lift"); move(stamp, HOV, P.glide, "cubic-bezier(.45,0,.2,1)");
        hat(P.glide + P.hold, ()=> move(stamp, "none", P.back, "cubic-bezier(.4,0,.2,1)"));
        hat(P.glide + P.hold + P.back - 150, ()=> stamp.classList.remove("lift"));
        hat(P.glide + P.hold + P.back + 50, ()=>{ hinting = false; lastAct = Date.now(); });
      }
      function stopHint(taken){   // taken = the child took hold of the guiding stamp itself (it stays where it is, in hand)
        if(!hinting) return; hinting = false; hintT.forEach(clearTimeout); hintT = [];
        if(!taken) putBack(hintStamp || R.stamp, 350);
      }""", "stamp hint")
js = rep1(js, "if(hinting) stopHint(s === R.stamp);", "if(hinting) stopHint(s === hintStamp);", "stamp stopHint")
js = rep1(js, "        state.attempts = (state.attempts || 0) + 1; sfxWrongSoft();\n",
"""        state.attempts = (state.attempts || 0) + 1; sfxWrongSoft();
        rWrong++;   // [vo-rec] the deck's ladder: 1st = the wiggle alone; 2nd = hint 2's line; 3rd and later = hint 3's line (the open slot's own, by its mark) + the guidance glide
        if(rWrong >= 2){ const D = R.D, open = R.slots.find(q=> !q.done), mk = open ? String(open.mark.textContent || "").trim() : "";
          const id = rWrong === 2 ? D.hint2_audio : ((D.hint3_by_mark && D.hint3_by_mark[mk]) || D.hint3_audio || D.hint2_audio);
          at(P.wiggle + P.reset, ()=>{ if(drag || solved || isPlaying) return; if(id) play(A(id), ()=>{ lastAct = Date.now(); }); if(rWrong >= 3) hint(true); }); }
""", "stamp wrong ladder")
js = rep1(js, "at(P.gone_at, ()=>{ o.el.classList.add(\"gone\"); sfxCorrect();",
              "at(P.gone_at, ()=>{ o.el.classList.add(\"gone\"); sfxCorrect(); if(last && d.ok_audio) play(A(d.ok_audio), ()=>{}); /* [vo-rec] \"शाबाश!\" with the round's chime */", "stamp ok")   # a block comment: the line goes on
# the gate: [vo-rec] set the tutorial caption's cue at the recorded "चलिए" (2940 ms, VR["gate_cue_ms"]); since [gate-ref-vo] the three
# gates play the reference's own clips with the reference's own cues (the gate script keeps them verbatim), so no cue is patched here
# ---------- [gate-ref-vo] (asked 2026-10-29: "take the reference https://hi-02-h04-l01-s01-dun.vercel.app/ and apply the exact same
#            transition animation screens with pink hindi texts along with the exact same VOs of the transition screens ... where ever
#            used; rest keep everything exactly the same"). The three gates here (start -> T0 "चलिए, शुरू करें!", T4 -> G1 "चलिए, साथ
#            में करें!", P2 -> L1 "अब आपकी बारी!") already ran the reference's bird, lift, headline wipe, sink, hold and texts
#            ([dun-chrome] 5); probed side by side (scratchpad gate_probe.py / gate1_probe.py: every 40 ms, computed styles, play()
#            log) they differed in —
#   1. the LINES: this lesson's vo_pt_tutorial (the user's recording, 4.94 s), vo_pt_guided / vo_pt_practice (TTS) -> the reference's
#      own recordings (its vo_pt_*.wav, byte-identical on the live site and in the local copy, re-encoded to this engine's
#      Opus-48k .ogg like vo_well_done: dun_assets/Audio/vo_pt_*.ogg, same length, 0 lag, corr .999) with its card's texts;
#   2. the CAPTION moments: the reference's 3660 / 3940 / 1120 ms into those clips (above, the gate script verbatim);
#   3. the SCRIM: the reference's later TOTA-CONSIST-S05 rule darkens every gate to rgba(57,55,55,.6) (its PHASEGATE-ADD .35, which
#      [dun-chrome] had copied, is overridden there) -> .6 here too;
#   4. the FIRST gate's blur: the reference blurs the landing itself (filter blur(10px) on .start-gate) under a 10px backdrop blur;
#      here the engine's [28b] 15.8px backdrop and no filter -> the reference's pair.
#   The texts, the bird file (peeking_talk_up.webp, md5-identical), its size / lift / sink, the headline's look and wipe, the 4 s hold
#   were already identical and are untouched. vo_rec.py still writes the user's vo_pt_tutorial recording into assets/Audio when
#   re-run; this step copies the reference's clips over it on every build, so a re-run cannot bring the old line back. ----------
for _k, _txt in (("tutorial", "ध्यान से देखिए और मेरे साथ जानिए। चलिए, शुरू करें!"),
                 ("guided", "बहुत बढ़िया! अब हम साथ मिलकर शुरू करते हैं। चलिए, साथ में करें!"),
                 ("practice", "वाह! अब आपकी बारी।")):
    _src, _dst = DUN / "Audio" / f"vo_pt_{_k}.ogg", DIST / "assets" / "Audio" / f"vo_pt_{_k}.ogg"
    assert _src.exists(), f"[gate-ref-vo] missing {_src}"
    if not _dst.exists() or _dst.read_bytes() != _src.read_bytes(): shutil.copy2(_src, _dst)
    card["assets"]["audio"][f"vo_pt_{_k}"] = f"assets/Audio/vo_pt_{_k}.ogg"
    card["assets"]["audio_text"][f"vo_pt_{_k}"] = _txt   # the reference card's audio_text, as written there
vo_css = """
/* ===== [vo-rec] the pointing hand of the picks' hint 3 (G1-G3: the sentence picks' reveal hand, on the stage) ===== */
.stage .slide-stage .reveal-hand.dmf-hand{position:absolute;width:96px !important;height:96px !important;z-index:55;object-fit:contain;pointer-events:none;
  filter:drop-shadow(0 6px 10px rgba(0,0,0,.22));animation:guidedHandBob 1s ease-in-out infinite;}
/* ===== [vo-rec] end ===== */
"""
# 5. the CSS, last in the cascade
dun_css = ("\n/* ===== [dun-chrome] the chrome of HI02H04_L01_S01 (hi-02-h04-l01-s01-dun.vercel.app) — see build.py ===== */\n"
  "/* ---- the cover's sky: the kit's sky-drift + sky-burst + sky-adapt, the reference's block verbatim ---- */\n" + dun_block("sky_css.css") +
  r"""
/* this lesson's adaptations of the sky: the Figma title card is 1160x475 on the stage (the reference's is 1114x456), so its hole is
   40 px inside THAT box; the title page keeps its own background element (.start-bg): the reference's plain sunburst goes there,
   and the [title-fig] "no sky" rule is undone; while a gate is up the field is the plain blue (TOTA-GATE-NO-STARS) */
.sg-sky{--sg-hole-w:calc(1120px * var(--scale,1));--sg-hole-h:calc(435px * var(--scale,1));}
body.is-start .start-bg{background-image:url("assets/UI/startnew_bg_plain.webp") !important;}
body.is-start .sg-glow,body.is-start .sg-sky{display:block !important;}
body.gating .sg-glow,body.gating .sg-sky{display:none !important;}
body.gating .start-bg{background-image:none !important;background-color:#7FC8F4 !important;}
/* [cover-sky] (2026-10-28): the start gate must be TRANSPARENT on the title page, as the reference's is (its own rule
   `body.is-start .start-gate{background:transparent}`, which its sky-adapt block relies on). Without it the kit's
   `.start-gate{background-image:startnew_bg_plain}` above (meant for the gate OFF the title page) painted a second sunburst on
   the gate - which sits in the stage at z 80, above the fixed sky layer at z 0 - so the breathing glow and the 87 drifting
   stars were built but never seen. Same specificity as the reference's rule; nothing else on the cover changes. */
body.is-start .start-gate{background:transparent;}
/* ---- the cover: the play button (LANDING-START-AFTER-VO + LANDING-PLAY-BTN + PLAY-BTN-140 + NO-WAITING-PLAY-BTN, value for value,
   written for this title page's scaled frame: 140x140 on the stage, centred, its bottom edge 2 px above the card's bottom — the
   card's 9 px border is inside its box here, hence the -9px); hidden until .ready, then the pop-in, then the breathing; the tap
   lands even while a line speaks (the reference's: the welcome's replay is cut) ---- */
/* [cover-sky] (2026-10-28): no `opacity:1 !important` / `filter:none !important` on the READY button - an !important declaration
   beats a keyframe, so the pop-in's fade (sgBtnReveal 0 % = opacity 0) never ran and the disc appeared opaque at scale .55; the
   reference carries those two only on its waiting state (:not(.ready), display:none here). Nothing on this file dims .sg-btn. */
.sg-fig .sg-btn,.sg-fig .sg-btn.ready{position:absolute;left:50%;bottom:calc(2px / var(--fig-s) - 9px) !important;top:auto !important;transform:translateX(-50%);z-index:4;
  width:calc(140px / var(--fig-s)) !important;min-width:0 !important;max-width:none !important;height:calc(140px / var(--fig-s)) !important;
  padding:0 !important;border:0 !important;border-radius:0 !important;box-shadow:none !important;cursor:pointer;
  background:transparent url("assets/UI/btn-play.svg") center / 100% 100% no-repeat !important;
  font-size:0 !important;line-height:0 !important;color:transparent !important;overflow:visible !important;}
.start-gate .sg-btn:not(.ready){display:none !important;}
.start-gate .sg-btn.ready{display:inline-flex !important;animation:sgBtnReveal .52s cubic-bezier(.34,1.5,.6,1) !important;}
@keyframes sgBtnReveal{0%{opacity:0;transform:translateX(-50%) scale(.55) translateY(14px);}60%{opacity:1;transform:translateX(-50%) scale(1.08) translateY(0);}100%{opacity:1;transform:translateX(-50%) scale(1) translateY(0);}}
.start-gate .sg-btn.ready.sg-breathe{animation:sgBtnPulse 1.4s ease-in-out infinite !important;}
@keyframes sgBtnPulse{0%,100%{transform:translateX(-50%) scale(1);}50%{transform:translateX(-50%) scale(1.04);}}
.start-gate .sg-btn:not(.locked):active{transform:translateX(-50%) translateY(3px) !important;box-shadow:none !important;}
body.vo-lock .start-gate .sg-btn.ready,body.vo-lock .sg-btn.ready{pointer-events:auto !important;}
body.is-start.landing-play-ready .sg-card :not(.sg-btn):not(.sg-btn *){animation-play-state:running !important;}
/* the cover's bird: the reference's wave file, 208 px, its box 24 px left of and 12 px under the card's bottom-left corner
   (frame px of this title page: the card is 76,125 1114x456 at scale 1.0414); the chip at its feet: 70 px at 83 px from the card's
   left, 12 px under its bottom (FEET-SPEAKER), grey until the play button is ready and while a line speaks */
.sg-fig .sg-mascot{position:absolute;left:52.96px;top:396.35px;width:199.73px;height:auto;z-index:3;object-fit:contain;pointer-events:auto;cursor:pointer;animation:none;transform:none;}
.sg-fig .sg-vo{left:155.7px !important;top:525.3px !important;bottom:auto !important;width:calc(70px / var(--fig-s)) !important;height:calc(70px / var(--fig-s)) !important;display:block !important;z-index:5;}
.start-gate .sg-vo.sg-vo-off,body.vo-playing .start-gate .sg-vo,.sg-vo.vo-disabled{pointer-events:none !important;opacity:.5 !important;filter:grayscale(1) brightness(1.2) !important;}
.sg-vo svg{overflow:visible !important;} .sg-vo svg > g[filter]{filter:none !important;}
.sg-vo:not(.playing) .wv{animation:none !important;opacity:1 !important;}
/* ---- आगे: the reference's NAV-NEXT-BTN + NAV-PULSE, verbatim, then this engine's boxes: 170x62 on the tutorial pages, 190x62
   elsewhere (the reference's), in the places this file already gives the button; a page that hides the button inline keeps it
   hidden (the reference's pick pages do that with a card flag) ---- */
""" + dun_block("nav_css.css").replace("#navBtn{display:flex !important;", '#navBtn:not([style*="display: none"]){display:flex !important;') + dun_block("nav_pulse_css.css") + r"""
#navBtn{width:190px !important;height:62px !important;}
.stage.tut #navBtn{width:170px !important;height:62px !important;}
#navBtn.active{animation:none !important;}                                  /* the breathing is the art's (::after), never the box's */
#navBtn img{display:none !important;}
/* ---- the bird in the title bars: the engine's live head inside every frame's circle (.dmf-head), filling it as the engine's own
   circle does; the engine's header (G4/P1/P2): the reference's 118 px circle at 16.5,18 and its animated faces INSIDE the circle ---- */
.dmf-head img.dun-live{position:absolute !important;left:0 !important;top:0 !important;width:100% !important;height:100% !important;object-fit:cover !important;}
.stage.sent-page .mascot-wrap{width:118px !important;height:118px !important;left:16.5px !important;top:18px !important;}
.stage.sent-page .mascot-circle{background:#9DDBF5 !important;border:4px solid #FFFFFF !important;box-shadow:0 6px 14px rgba(0,47,118,.20) !important;overflow:hidden !important;border-radius:50% !important;}
.stage.sent-page .mascot-wrap.anim .mascot-circle .mascot-img,.stage.sent-page .mascot-circle .mascot-img{position:absolute !important;inset:0 !important;width:100% !important;height:100% !important;object-fit:cover !important;transform:none !important;}
/* ---- the speaker chips (HDR-SPEAKER's states): the header chip grey while a line speaks (already so on G4/P1/P2); waves blink
   only while a line speaks, solid at rest (TOTA-WAVES-IDLE) ---- */
""" + dun_block("waves_idle_css.css") + r"""
body.vo-playing #audioChip,body.vo-playing .mascot-wrap .audio-chip{pointer-events:none !important;opacity:.5 !important;filter:grayscale(1) brightness(1.2) !important;transition:none !important;}
/* ---- the gates: GATE-REF-ANIM (the bird, its lift, the headline's wipe, the first gate's sink), on the reference's scrim (.6: its
   TOTA-CONSIST-S05 rule over its PHASEGATE-ADD .35 — [gate-ref-vo]) with a 10px backdrop blur on every gate (the engine's [28b] gave
   the first one 15.8px), the bird fixed at the bottom centre (its PHASEGATE-ADD placement, which the lift keyframes assume) ---- */
.phase-gate.show{background:rgba(57,55,55,.6) !important;backdrop-filter:blur(10px) !important;-webkit-backdrop-filter:blur(10px) !important;}
body.is-start .phase-gate.show{background:rgba(57,55,55,.6) !important;backdrop-filter:blur(10px) !important;-webkit-backdrop-filter:blur(10px) !important;}
.phase-gate #phaseGateImg,.phase-gate img{position:fixed;left:50%;bottom:0;transform:translateX(-50%);height:clamp(120px,26vh,250px);width:auto;display:block;animation:none;}
""" + dun_block("gate_css.css") + r"""
.phase-gate.pg-ref .pg-title{opacity:1 !important;transition:none !important;}                /* this engine's title fades in on .text-speaking; here .pg-say shows it and pgWipe writes it */
.phase-gate.pg-ref:not(.pg-say) .pg-title{visibility:hidden !important;}
.phase-gate.pg-ref.pg-say .pg-title{visibility:visible !important;}
body.is-start.gating .start-gate{display:flex !important;visibility:visible !important;opacity:1 !important;pointer-events:none !important;filter:blur(10px) !important;}   /* [gate-ref-vo] the reference blurs the landing itself under the first gate (TOTA-CONSIST-S05: body.gating .start-gate{filter:blur(10px)}) */
/* ---- confetti (CONFETTI-REF): over the whole window under the gate, pieces 1.5x, sized with the stage ---- */
.fx-confetti{z-index:5000 !important;--fx-size:1.5;}
.fx-confetti .f{width:calc(var(--w) * var(--z) * var(--scale, 1) * var(--fx-size, 1));height:calc(var(--h) * var(--z) * var(--scale, 1) * var(--fx-size, 1));}
/* ---- the celebration: the reference's screen (TOTA-CELEBRATION-REFERENCE, TOTA-END-FULLBLEED, END-FINISH-BTN, CEL-SWIFTIE), verbatim;
   then this engine's own .end-btn box reset (it drew a 163x117 image button) ---- */
""" + dun_block("cel_ref_css.css") + dun_block("end_fullbleed_css.css") + dun_block("end_finish_btn_css.css") + dun_block("cel_swiftie_css.css") + r"""
#endBtn{width:auto !important;height:auto !important;line-height:1;}
#endBtn.show{display:inline-flex !important;align-items:center;}
.end-screen .end-mascot{position:static !important;transform:none !important;}
/* ===== [dun-chrome] end ===== */
""")
# ---------- [band-chip] (asked 2026-10-28): "From page 4 T2 to page 9 G3 why haven't you placed the speaker button icon just like the
#            other pages, with the exact same animation? Place the exact same speaker button icon on these pages with the same
#            animation effects; rest exactly the same." The six Figma-bar pages (T2, T3, T4 = PUNCT_DEMO; G1, G2, G3 = PUNCT_PICK)
#            mount in the tutorial card (the whole stage, .sfig-full), which already carries the engine's .tut-audio chip - the same
#            inline-SVG speaker as the header chip of G4 / P1 / P2, wired to replaySlideAudio and to setPlaying's .playing /
#            vo-disabled - but [demo-fig] hid it with the standing Swiftie on 2026-10-25 (the frame's only Swiftie is the head in
#            its title bar). Shown again, as G4's header chip is to ITS bird: G4's chip is 66 stage px at (94.5,80) by the 118 px
#            circle at (16.5,18) - its centre .8814 r right of and .6102 r below the circle's centre, on the bird's bottom-right
#            shoulder; the bars' circle (.dmf-head) is 121.34 x 124.97 stage px at (37.49,27.08), so the chip's box is
#            (118.6,94.7) 66 x 66 in stage px (the card IS the stage on these pages). The same look (the drop shadow on the
#            element, the in-SVG shadow off, hover 1.06 / press .95), the same states: grey (opacity .5, grayscale) and untappable
#            while a line speaks (body.vo-playing), the arcs blinking while it speaks (.playing, the engine's), solid at rest; it
#            comes in with the title bar (the bar's own fade + settle, .45 / .55 s) and - the reference's header-chip rule,
#            [SPK-AFTER-VO] - stays grey until the page's opening lines are over: on T2-T4 the demo runs itself to the end (the
#            engine refuses the chip's tap while state.demoRunning), on G1-G3 until the tiles are the child's (.sfig-in.dmf-live),
#            when a tap reads the sentence again, word by word (state.replayAudio, the idle reminder's read). No JS change. ----------
band_chip_css = r"""
/* ===== [band-chip] (2026-10-28) the speaker chip on the title-bar pages T2, T3, T4, G1, G2, G3 — G4's header chip at the bar's bird;
   see build.py ===== */
.tut-card.sfig-card.sfig-full .tut-audio{display:block;position:absolute;left:118.6px;top:94.7px;bottom:auto;width:66px;height:66px;z-index:41;cursor:pointer;
  --chip-op:1;opacity:var(--chip-op);transform:none;filter:drop-shadow(0 3px 6px rgba(0,0,0,.22));transition:transform .12s;}
.tut-card.sfig-card.sfig-full .tut-audio svg{filter:none;overflow:visible;}
.tut-card.sfig-card.sfig-full .tut-audio svg > g[filter]{filter:none;}        /* the chip's own shadow (above); the in-SVG one would clip the ring's bottom */
.tut-card.sfig-card.sfig-full .tut-audio:hover{transform:scale(1.06);}
.tut-card.sfig-card.sfig-full .tut-audio:active{transform:scale(.95);}
/* grey + untappable while a line speaks (G4's look, switched at once as there) and until the page's opening lines are over
   (T2-T4: the whole self-running demo; G1-G3: until the tiles are the child's) */
body.vo-playing .tut-card.sfig-card.sfig-full .tut-audio,
.tut-card.sfig-card.sfig-full:not(:has(.sfig-in.dmf-live)) .tut-audio{pointer-events:none;--chip-op:.5;filter:grayscale(1) brightness(1.2);}
/* in with the title bar: the bar's own entrance (.55 s settle, fading up to whichever opacity the state has — the keyframe's end
   reads --chip-op, so a grey chip lands on .5 and a live one on 1, with no fill to snap from); nothing until the bar is in */
.tut-card.sfig-card.sfig-full:not(:has(.dmf-band.in)) .tut-audio{opacity:0;transform:translateY(-14px) scale(.97);pointer-events:none;animation:none;}
.tut-card.sfig-card.sfig-full:has(.dmf-band.in) .tut-audio{animation:bandChipIn .55s cubic-bezier(.2,.9,.3,1.2);}
@keyframes bandChipIn{from{opacity:0;transform:translateY(-14px) scale(.97);}to{opacity:var(--chip-op,1);transform:none;}}
/* ===== [band-chip] end ===== */
"""
css = css + dun_css + band_chip_css + vo_css + cover_fx_css   # [cover-fx] / [cover-eyes]
html = f"""<!doctype html>
<html lang="hi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"><!-- [24a N9] pinch-zoom lock: a child two-finger-zooms the game off-centre in any real browser without it -->
<title>SwiftPAL · {card['skill_code']} · {title_hi}</title>
<link rel="stylesheet" href="style.css">
</head>
<body class="is-start">
{body}
<!-- ============ CARD DATA (embedded; in prod the compiler does this) ============ -->
<script type="application/json" id="cardData">{json.dumps(card, ensure_ascii=False)}</script>

<!-- ============ ENGINE ============ -->
<script src="app.js"></script>
</body>
</html>
"""

(DIST / "index.html").write_text(html, encoding="utf-8")
(DIST / "style.css").write_text(css, encoding="utf-8")
(DIST / "app.js").write_text(js, encoding="utf-8")

# ---------- 7a. [title-fig] the Figma title-page assets (kept next to this script) ----------
TITLE_SRC = SCR / "title_assets"
title_files = sorted(TITLE_SRC.glob("title_*"))
assert len(title_files) == 13, f"expected 13 title assets in {TITLE_SRC}, found {len(title_files)}"   # [cover-eyes] + the three rig sheets
for f in title_files:
    dst = DIST / "assets" / "UI" / f.name
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7b. [story-fig] the story page's assets (kept next to this script, in story_assets/) ----------
STORY_SRC = SCR / "story_assets"
for name, sub in (("story_grid.svg", "UI"), ("story_font_baloo2_800.woff2", "UI"),   # [baloo-font] (was the two Noto SemiBold subsets)
                  ("img_story_pinki_cat.webp", "Images"), ("img_story_pinki_listen.webp", "Images"),   # [story-pinki] the frames' pictures ([story-pics]: the user's redrawn ones)
                  ("img_story_pinki_ask.webp", "Images"), ("img_story_pinki_maa.webp", "Images"),       # (their clips: vo_rec.py)
                  ("vo_story_r0.ogg", "Audio"), ("vo_story_r1.ogg", "Audio"),
                  ("sfx_story_cat.mp3", "Audio")):   # [story-cat] beat 1's sound (the user's file, bytes as given)
    f, dst = STORY_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing story asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
for name in ("story_font_nsd600_deva.woff2", "story_font_nsd600_latin.woff2"):   # [baloo-font] the old face, unused now (its source stays in story_assets/)
    (DIST / "assets" / "UI" / name).unlink(missing_ok=True)
for name, sub in (("img_story_chintu.webp", "Images"), ("img_story_chintu_2.webp", "Images"), ("vo_story_s1.ogg", "Audio"), ("vo_story_s2.ogg", "Audio")):
    (DIST / "assets" / sub / name).unlink(missing_ok=True)   # [story-pinki] the Chintu beats' files: no page uses them now

# ---------- 7c. [recap-fig] the recap's clips (kept next to this script, in recap_assets/, made by recap_vo.py) ----------
RECAP_SRC = SCR / "recap_assets"
for k in RECAP_KEYS:
    f, dst = RECAP_SRC / f"vo_recap_{k}.ogg", DIST / "assets" / "Audio" / f"vo_recap_{k}.ogg"
    assert f.exists(), f"missing recap clip {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7d. [demo-fig] the demo's clips and pictures (demo1_assets/: recap_vo.py demo1; the two Figma bitmaps) ----------
DEMO_SRC = SCR / "demo1_assets"
for name, sub in [(f"vo_demo1_{k}.ogg", "Audio") for k in DEMO_KEYS] + [("demo1_head.webp", "UI"), ("img_demo1_girl.webp", "Images")]:
    f, dst = DEMO_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing demo asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7e. [demo-fig] T3's clips and picture (demo2_assets/: recap_vo.py demo2; the frame's "image 229"; its head is
#               byte-for-byte T2's demo1_head.webp) ----------
DEMO2_SRC = SCR / "demo2_assets"
for name, sub in [(f"vo_demo2_{k}.ogg", "Audio") for k in DEMO2_CLIPS] + [("img_demo2_girl.webp", "Images")]:   # [demo2-girl]
    f, dst = DEMO2_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing demo asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
(DIST / "assets" / "Audio" / "vo_demo2_intro.ogg").unlink(missing_ok=True)   # [demo-intro] the intro line is off the page

# ---------- 7f. [demo-fig] T4's clips and picture (demo3_assets/: recap_vo.py demo3; the frame's "image 230"; its head is
#               byte-for-byte T2's demo1_head.webp) ----------
DEMO3_SRC = SCR / "demo3_assets"
for name, sub in [(f"vo_demo3_{k}.ogg", "Audio") for k in DEMO3_CLIPS] + [("img_demo3_fruits.webp", "Images")]:
    f, dst = DEMO3_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing demo asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
(DIST / "assets" / "Audio" / "vo_demo3_intro.ogg").unlink(missing_ok=True)   # [demo-intro] the intro line is off the page

# ---------- 7g. [pick-fig] G1's clips and picture (g1_assets/: recap_vo.py g1; the frame's "image 231"; its head is
#               byte-for-byte T2's demo1_head.webp; the name on the right tap is T2's vo_demo1_purn) ----------
G1_SRC = SCR / "g1_assets"
for name, sub in [(f"vo_g1_{k}.ogg", "Audio") for k in G1_KEYS] + [("img_g1_girl_ball.webp", "Images")]:
    f, dst = G1_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing G1 asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
# ---------- 7h. [pick-fig] G2's sentence clip and picture (g2_assets/: recap_vo.py g2; the frame's "image 239"; its title bar is
#               T4's to the pixel, its instruction G1's vo_g1_intro, its name on the right tap T3's vo_demo2_prashn) ----------
G2_SRC = SCR / "g2_assets"
for name, sub in (("vo_g2_sent.ogg", "Audio"), ("img_g2_girl_bag.webp", "Images")):
    f, dst = G2_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing G2 asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
# ---------- 7i. [pick-fig] G3's sentence clip and picture (g3_assets/: recap_vo.py g3; the frame's "image 233"; its title bar
#               is G1's to the pixel, its instruction vo_g1_intro, its name on the right tap T4's vo_demo3_alp) ----------
G3_SRC = SCR / "g3_assets"
for name, sub in (("vo_g3_sent.ogg", "Audio"), ("img_g3_flowers.webp", "Images")):
    f, dst = G3_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing G3 asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7j. [sent-fig] G4's clips and picture (g4_assets/: recap_vo.py g4; img_g4_kite_gry.webp = g4_picture.py over the
#               user's picture, g4_kite_source.png) ----------
G4_SRC = SCR / "g4_assets"
for name, sub in [(f"vo_g4_{k}.ogg", "Audio") for k in G4_KEYS] + [("img_g4_kite_gry.webp", "Images"), ("sfx_g4_giggle.mp3", "Audio")]:   # [g4-giggle]
    f, dst = G4_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing G4 asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7k. [sent-fig] P1's and P2's clips and pictures (<page>_assets/: recap_vo.py <page>; the picture = g4_picture.py over
#               the user's picture, <page>_*_source.png; their title + try-again clips are G4's) ----------
for page, image_id, extra in (("p1", "img_p1_book_gry", [("sfx_p1_book.mp3", "Audio")]), ("p2", "img_p2_pencils_gry", [("sfx_p2_pencils.mp3", "Audio")])):   # [p1-book] / [p2-pencils] each page's tap sound rides along
    for name, sub in [(f"vo_{page}_{k}.ogg", "Audio") for k in SENT_OPT_KEYS] + [(f"{image_id}.webp", "Images")] + extra:
        f, dst = SCR / f"{page}_assets" / name, DIST / "assets" / sub / name
        assert f.exists(), f"missing {page.upper()} asset {f}"
        if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7l. [letter-fig] L1's pictures and sounds (letter_assets/: the frames' bitmaps and the user's two PNGs cut into layers by
#               the scratchpad's make_letter_assets_*.py; the three room pictures lossless (scene_c: [letter-idea], the pensive girl);
#               the user's five sound files as ogg, see README) ----------
LETTER_SRC = SCR / "letter_assets"
for name, sub in [(f"{k}.webp", "Images") for k in LETTER_IMGS] + [(f"{k}.ogg", "Audio") for k in LETTER_SND]:
    f, dst = LETTER_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing letter asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
# ---------- 7m. [stamp-fig] L2's bitmaps (stamp_assets/: the frame's own assets, by the scratchpad's make_stamp_assets.py), its two
#               clips (recap_vo.py stamp) and the user's two sound effects as ogg (see README) ----------
STAMP_SRC = SCR / "stamp_assets"
for name, sub in [(f"{k}.webp", "Images") for k in STAMP_IMGS] + [(f"{k}.ogg", "Audio") for k in STAMP_SND] + [(f"vo_stamp_{k}.ogg", "Audio") for k in STAMP_KEYS]:
    f, dst = STAMP_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing stamp asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7. assets the reference chrome needs ----------
SKIP = {"assets/UI/title_swifty_swimming.mp4", "assets/UI/start_card_sea.webp"}
refs = set(re.findall(r"assets/(?:UI|Audio)/[A-Za-z0-9_.&-]+", html + css + js))
for g in ("sw_head_*.webp", "sw_lg_hint_anim.webp", "bgdeco_*.svg"):
    refs.update("assets/UI/" + p.name for p in (REF_DIR / "assets" / "UI").glob(g))
for g in ("sfx_*.ogg", "standard_background_music_2.mp3"):
    refs.update("assets/Audio/" + p.name for p in (REF_DIR / "assets" / "Audio").glob(g))
copied, missing = [], []
for p in sorted(refs):
    if p in SKIP or not p.startswith(("assets/UI/", "assets/Audio/sfx_", "assets/Audio/standard_")): continue
    src, dst = REF_DIR / p, DIST / p
    if dst.exists(): continue
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst); copied.append(p)
    else:
        missing.append(p)
print("slides:", len(card["slides"]), [s["id"] for s in card["slides"]])
print("phase_distribution:", card["phase_distribution"])
print("index.html %d B · style.css %d B · app.js %d B" % tuple(len(x.encode("utf-8")) for x in (html, css, js)))
print("copied %d assets:" % len(copied), " ".join(p.split("/", 1)[1] for p in copied))
print("referenced but absent in reference (dynamic prefixes are expected here):", missing)
