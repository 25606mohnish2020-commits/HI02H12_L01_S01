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
import re, json, shutil, pathlib, sys, base64, math

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
# [t0b-fig] (2026-11-01) laid out as frame 704:2, which has NO title: data.title_hi is gone, so the module's title stays empty
# (the intro line vo_story_r0 still sounds first, the box still comes in when it ends); prompt_hi keeps the page's name
for k in ("r0", "r1", "c1", "c2"):
    lines[k] = json.loads((SCR / "story_assets" / f"vo_story_{k}.words.json").read_text(encoding="utf-8"))
_vr0 = json.loads((SCR / "vo_rec" / "derived.json").read_text(encoding="utf-8"))["cues"]
card["slides"].insert(1, {"id": "T0B", "phase": "tutorial", "eis": "iconic", "type": "STORY_RELISTEN",
    "prompt_hi": "आइए वाक्य सुनें।",
    "audio": {"intro": "vo_story_r0", "narration": "vo_story_c1", "narration_2": "vo_story_c2", "explain": "vo_story_r1", "moral": "vo_story_moral"},
    "data": {"intro_audio": "vo_story_r0",
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
# [recap-fig2] (2026-11-01) frame 764:144: ONE mark — पूर्ण विराम — its sign, its name, the example sentence and the frame's picture; no
# title (the lead and intro lines sound over the card alone). The use ("बात पूरी होने पर") is said, not shown. (Was 508:2's three rows;
# the अल्प विराम / प्रश्नवाचक rows' clips stay registered: T3 / T4 name their marks with vo_recap_prashn_name / vo_recap_alp_name.)
card["slides"][i_t1] = {"id": "T1", "phase": "tutorial", "eis": "symbolic", "type": "MARKS_RECAP",
    "prompt_hi": rl["purn_name"]["shown"], "audio": {"prompt": "vo_recap_intro"},
    "data": {"intro_audio": "vo_recap_intro", "mark": "।", "image_id": "img_recap_girl",
             "name": part("purn_name"), "when": part("purn_when"), "example": part("purn_eg"),
             "pic_sfx": "sfx_fb_correct.ogg"}}   # [recap-sfx] the reference's horse sound (hi02h11l02s04-file5 T2's fbCorrect), bytes as given
card["assets"]["image"]["img_recap_girl"] = "assets/Images/img_recap_girl.webp"   # node 764:753's source bitmap (1024x1536, WebP q90, alpha exact)
# [recap-alp] (2026-11-01) frame 764:755: the same page for अल्प विराम, right after T1 (T1B) — the sign ",", its name, the example
# "आम, केला, संतरा और सेब" (both commas kept lit, each from its word), the fruit picture (node 524:350's bitmap = T4's img_demo3_fruits)
# with T1's sounds; the recorded अल्प-विराम lines (the use is said, not shown). No lead / intro line — those open T1 only — so its
# name beat starts 0.7 s after the page appears.
card["slides"].insert(i_t1 + 1, {"id": "T1B", "phase": "tutorial", "eis": "symbolic", "type": "MARKS_RECAP",
    "prompt_hi": rl["alp_name"]["shown"], "audio": {"prompt": "vo_recap_alp_name"},
    "data": {"variant": "alp", "mark": ",", "image_id": "img_demo3_fruits",
             "name": part("alp_name"), "when": part("alp_when"), "example": part("alp_eg"),
             "pic_sfx": "sfx_fb_correct.ogg"}})
# [recap-prashn] (2026-11-01) frame 764:945: the same page for प्रश्नवाचक चिह्न, right after T1B (T1C) — the sign "?", its name, the
# example "तुम्हारा घर कहाँ है ?" (its ? kept lit), the house picture (node 766:1140's source bitmap) with T1's sounds; the recorded
# प्रश्नवाचक lines (the use is said, not shown). No lead / intro line, as T1B.
card["slides"].insert(i_t1 + 2, {"id": "T1C", "phase": "tutorial", "eis": "symbolic", "type": "MARKS_RECAP",
    "prompt_hi": rl["prashn_name"]["shown"], "audio": {"prompt": "vo_recap_prashn_name"},
    "data": {"variant": "prashn", "mark": "?", "image_id": "img_recap_house",
             "name": part("prashn_name"), "when": part("prashn_when"), "example": part("prashn_eg"),
             "pic_sfx": "sfx_fb_correct.ogg"}})
card["assets"]["image"]["img_recap_house"] = "assets/Images/img_recap_house.webp"   # node 766:1140's source bitmap (1536x1024, WebP q90, alpha exact)
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
DEMO_KEYS = ["intro", "sent", "purn", "full", "explain"]   # [t2-scene] + explain (the line over the tiles); purn and full stay copied as before (T2 no longer plays them; the [vo-rec] step below expects the recording vo_demo1_full in the dist)
DEMO_BAND = "विराम चिह्न का वाक्य में प्रयोग ।"   # [band-title] (2026-10-28) the title bar's line on T2 / T3 / T4 (frame 656:2's), in place of the intro line's shown text; the intro clip sounds as before
SENT50 = {"x": 0, "y": 18, "w": 719 - 63, "size": 50, "lh": 110, "ws": 0}   # [sent-50] (2026-10-28) T2 / T3 / G1 / G2: the sentence at 50px (the 50px pages' -3px word spacing) in the same line box (y 18, 110px) as the 64px one; its text box is the 719px bar LESS the slot's column (a 4px gap + the 59px slot), so the centred sentence and the slot 4px after it are centred on the bar TOGETHER (asked twice: first "the sentence centred", then "both together"); each page's slot x = its ink's right edge + 4 (frame px, measured in Chrome)
dl = {k: json.loads((SCR / "demo1_assets" / f"vo_demo1_{k}.words.json").read_text(encoding="utf-8")) for k in DEMO_KEYS}
i_t2 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "T2")
assert card["slides"][i_t2]["type"] == "BUILD_PUNCT" and card["slides"][i_t2]["data"].get("auto"), "T2 is not the first auto demo"
dpart = lambda k: {"text_hi": dl[k]["shown"], "audio": f"vo_demo1_{k}", "word_times": [t[0] for t in dl[k]["word_times"]], "word_end": dl[k]["word_times"][-1][1]}
# [t2-scene] (asked 2026-11-01): T2 is now frame 706:188 "2 T0B" — the hallway scene on T0B / T1's card (the standing Swiftie and
# the 🔊 chip where page 3 T1 has them), its own module PUNCT_SCENE (PUNCT_DEMO stays T3's / T4's): the intro line over the picture
# alone; the sentence + the empty slot (T1's text pop); the sentence's clip, word by word; then 2 s of the user's school sound with a
# small pop of the girl ([t2-scene2] 2026-11-01: she stands in her place from the first frame — was a walk in from the doorway under
# the sound); the slot blinking orange 2 s while the three mark tiles pop in
# (the user's pop) — [t2-scene3] 2026-11-01: the blink 4 s and the tiles one by one, 350 ms apart, each with its own pop;
# [t2-scene4] the same day: the blink 6 s, SLOW (1.2 s cycles) and the WHOLE box at once (fill + ring + the pulse's glow);
# [t2-scene5] the same day: 7 s, the whole box FADING out and in (opacity) on slow 1.75 s cycles, its orange look static; the
# explanation "सरल वाक्य में बात पूरी होने पर हम पूर्णविराम का प्रयोग करते हैं ।" lighting the danda's tile at
# "पूर्णविराम"; the other two dim; the lit tile pulsing until the CHILD taps it; then green, the kit's correct sound, the mark in
# the slot, the slot's box gone, on to T3. The explanation is a placeholder take (recap_vo.py demo1 explain: edge-tts, no recording
# of it yet); its word times are the synthesiser's own.
# [t2-quiet] (asked 2026-11-02): "remove the sound effect and the pop animation of the girl synced with it" — data.girl_pop false and no
# data.pic_sfx skip stage 3, so the slot's blink starts 0.3 s after the sentence's clip and the tiles pop with it. (A wave of her
# hand was built in their place and on T3 — [girl-wave] — and withdrawn on the user's word: T2 without it, T3's glance as before.)
_cue = dl["explain"]["shown"].split().index("पूर्णविराम")
card["slides"][i_t2] = {"id": "T2", "phase": "tutorial", "eis": "enactive", "type": "PUNCT_SCENE",
    "prompt_hi": dl["intro"]["text"], "audio": {"prompt": "vo_demo1_intro"},
    "data": {"intro_audio": "vo_demo1_intro", "bg_id": "img_demo1_hall", "image_id": "img_demo1_girl_walk",
             "sentence": dpart("sent"), "mark": "।", "explain": dict(dpart("explain"), cue_word=_cue),
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "girl_pop": False,   # [t2-quiet] (2026-11-02) no school sound and no pop of the girl any more (was "pic_sfx": "sfx_demo1_school.mp3", "pic_sfx_ms": 2000 — the file stays in the dist, unused): she stands still as painted and the blink follows the sentence's clip, as T3's ([t3-girl]); the [girl-wave] wave built in their place was withdrawn the same day
             "blink_ms": 7000, "blink_cycle_ms": 1750, "tiles_sfx": "sfx_demo1_pop.mp3", "tiles_gap_ms": 350},   # [t2-scene5] the blink 7 s (2 -> 4 -> 6 -> 7) in SLOW 1.75 s cycles = four fades of the whole box (the module rounds blink_ms / blink_cycle_ms; [t2-scene4] had 1.2 s on / off cycles, [t2-scene3] ~667 ms); the user's dragon-studio-pop-402323 (1).mp3 (0.72 s) ONCE PER TILE as the tiles pop in one by one, 350 ms apart ([t2-scene3]; was all three 90 ms apart under one pop)
    "signals": {"on_complete": []}}
for k in DEMO_KEYS:
    card["assets"]["audio"][f"vo_demo1_{k}"] = f"assets/Audio/vo_demo1_{k}.ogg"
    card["assets"]["audio_text"][f"vo_demo1_{k}"] = dl[k]["text"]
# [t2-scene] the frame's bitmaps: the hallway (node 710:601's source, 1672x941) and the walking girl (node 746:2534's, 1024x1536)
card["assets"]["image"]["img_demo1_hall"] = "assets/Images/img_demo1_hall.webp"
card["assets"]["image"]["img_demo1_girl_walk"] = "assets/Images/img_demo1_girl_walk.webp"
card["_emoji_fallback"]["img_demo1_hall"] = "🏫"; card["_emoji_fallback"]["img_demo1_girl_walk"] = "✏️"
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

# [t3-scene] (asked 2026-11-01): T3 is now frame 724:2016 "7 T3" — a second scene on T2's PUNCT_SCENE module (data.variant "ask",
# card class dsc-v-ask): the frame's classroom picture (its "image 261", 1816x866, 0,-4 1088x519 of the card) in T2's card with T2's
# standing girl in T2's place (the frame draws no girl — its only figure is the Swiftie placeholder; the user asked for "the image
# with the standing girl", and the frame's speech bubble points its tail at where T2's girl stands); no intro line: the scene stands
# for data.open_ms = 1 s, then the frame's speech bubble (its vector group, kept as an SVG with its own shadows) POPS in with the
# sentence "तुम्हारा नाम क्या है" and the frame's yellow dashed slot (907,174 59x100, #FFF1B6) inside it, to the user's sharp pop
# (creatorshome-sharp-pop-328170.mp3, data.box_sfx — in place of T1's soft tone); then T2's flow: the RECORDED sentence (vo_demo2_sent,
# its re-derived word times) with the words lit, 2 s of the school sound with the girl's small pop, the slot's slow whole-box blink
# with the tiles popping in one by one, the RECORDED explanation "यह एक सवाल है, सवाल के अंत में प्रश्नवाचक चिह्न लगाया जाता है ।"
# (vo_demo2_explain — the [vo-rec] take, its whisper word times from vo_rec/transcripts.json) lighting the "?" tile at "प्रश्नवाचक",
# the other two dim, the "?" pulsing until the child taps it, its border green, the "?" in the slot, the box gone, on to T4 by
# itself. The frame orders its tiles । ? , (T2's are । , ?), so the "?" is the MIDDLE tile here. PUNCT_DEMO stays for T4 only.
# [t3-girl] (asked the same day): "remove the existing girl and the sound effect synced with her; make the exact same girl as in the
# frame" — the frame now has her: "image 272" (its fill 1024x1535, drawn 213,212 257x385, ABOVE the tiles and the bubble — the
# frame's last node) with her own shadow "Ellipse 3767" (277,558 118x37, #D3A06F at .4). She stands there from the first frame with
# NO animation and NO sound: T2's girl, its 2 s of the school sound and her small pop are gone from T3 (data.girl_pop false and no
# pic_sfx: the module skips that beat — the blink follows the sentence's clip by 0.3 s). Read as "without any animation and [without]
# the sound effect": the message removes the sound and names no new one.
# [t3-look] (asked 2026-11-02): "when the options appear the girl should look towards them and move her arms, then look back to
# the screen in the exact same position; repeat every 5 seconds; perfect and smooth". As the FIRST tile pops the girl's eyes slide
# toward the tiles, she leans a little their way and her open hand lifts and bobs twice ("which one?"); by 2.3 s she is back
# exactly as painted, and the cycle repeats every data.girl_look.every_ms (5 s; [t3-look7] 7 s) until the child's tap (the class leaves only in a
# rest phase, so she is never caught mid-move). The girl is her own bitmap cut into LAYERS by girl_rig.py (demo2_assets/girl_rig/:
# the body with a hole for the forearm, the two eyes' interiors with a sclera disc and the completed iris, the forearm about the
# elbow, the braid tip over it — see that script's docstring) and moved by CSS transforms only; the sheets are inlined in the CSS
# as data URIs (nothing to wait for), the geometry in the girl's box px from rig.json, the amounts (the eyes' travel, the arm's
# lift, the lean) in the card data as CSS variables, the choreography (the keyframes) in the CSS.
_rig = json.loads((SCR / "demo2_assets" / "girl_rig" / "rig.json").read_text(encoding="utf-8"))
GIRL_BOX = (257, 385); _gsx, _gsy = GIRL_BOX[0] / _rig["bitmap"][0], GIRL_BOX[1] / _rig["bitmap"][1]   # the frame's 257x385 over the 1024x1535 bitmap
LOOK = {"every_ms": 7000, "active_ms": 2300, "gx": round(9 * _gsx, 2), "gy": round(4.5 * _gsy, 2), "arm_deg": 11, "lean_deg": 2}   # the eyes 9 / 4.5 bitmap px toward the tiles, the forearm 11 degrees up, the lean 2 degrees
_vr_t3 = json.loads((SCR / "vo_rec" / "transcripts.json").read_text(encoding="utf-8"))   # vo_rec.py's whisper word times per recording
_x3 = _vr_t3["vo_demo2_explain.wav"]; _x3_words = [w[0] for w in _x3["words"]]
assert " ".join(_x3_words) == _x3["text"] == "यह एक सवाल है, सवाल के अंत में प्रश्नवाचक चिह्न लगाया जाता है ।", _x3["text"]
assert dl2["sent"]["shown"] == "तुम्हारा नाम क्या है" and len(dl2["sent"]["word_times"]) == 4, dl2["sent"]
card["slides"][i_t3] = {"id": "T3", "phase": "tutorial", "eis": "enactive", "type": "PUNCT_SCENE",
    "prompt_hi": dl2["sent"]["text"], "audio": {},
    "data": {"variant": "ask", "intro_audio": None, "open_ms": 1000, "bg_id": "img_demo2_room", "image_id": "img_demo2_girl_ask", "girl_pop": False,   # [t3-girl] the frame's girl, still
             "girl_rig": True, "girl_look": LOOK,   # [t3-look] her layers (the CSS) and the glance's amounts / timing
             "bubble_id": "img_demo2_bubble", "box_sfx": "sfx_demo2_sharp_pop.mp3", "slot_w": 59, "slot_h": 100,   # the frame's slot (T2's is 53x90)
             "sentence": dpart2("sent"), "mark": "?",
             "explain": {"text_hi": _x3["text"], "audio": "vo_demo2_explain", "word_times": [w[1] for w in _x3["words"]], "word_end": _x3["words"][-1][2], "cue_word": _x3_words.index("प्रश्नवाचक")},
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}, {"mark": ",", "name_hi": "अल्प विराम"}],   # the frame's order
             "blink_ms": 7000, "blink_cycle_ms": 1750, "tiles_sfx": "sfx_demo1_pop.mp3", "tiles_gap_ms": 350},   # T2's blink and tiles
    "signals": {"on_complete": []}}
card["assets"]["image"]["img_demo2_room"] = "assets/Images/img_demo2_room.webp"
card["assets"]["image"]["img_demo2_bubble"] = "assets/Images/img_demo2_bubble.svg"
card["assets"]["image"]["img_demo2_girl_ask"] = "assets/Images/img_demo2_girl_ask.webp"   # [t3-girl] the frame's "image 272" fill (1024x1535, q90, alpha exact)
del card["assets"]["image"]["img_demo2_girl"]; del card["_emoji_fallback"]["img_demo2_girl"]   # [demo2-girl]'s cut-out: no page shows it now
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
# [t4-scene] (asked 2026-11-02): T4 is now frame 723:1575 "8 T4" — a third scene on T2's PUNCT_SCENE module (data.variant "list",
# card class dsc-v-list), in place of the [demo-fig] PUNCT_DEMO page (frame 523:320, its title bar, picture box, sentence bar and
# second reading, all gone with it). The frame: T2's card (96,106 1088x508) with a park landscape ("image 264", 1815x866, drawn
# rotate(180) + flipY = mirrored, at -102,-124 1371x654 of the card; the bitmap is mirrored once in img_demo3_park.webp), the girl
# with a fruit basket ("image 276", 1024x1535 at 240,257 224x336, the frame's last node) on an opaque #FEB564 ellipse (729:2321,
# 257,546 190x47), the sentence "मेरे पास आम    केला    सेब और संतरा है ।" (Baloo 2 ExtraBold 55 #012F76, centred on 640.5, box
# top 147, 893 wide) with TWO white dashed slots 37x42.606 at 495,188 and 645,188 in its four-space runs, the tiles । , ? (T2's
# order) at 494.09 / 721 / 951.818, 447 over #FEB564 ellipses, its own Swiftie (not used: T1's standing Swiftie and chip, as T2 /
# T3). The flow, as asked: the picture and the girl, standing, from the first frame (no intro line: data.open_ms 1 s); then the
# sentence rises in whole with both empty slots popping in and T1's text pop (T2's stage 2: no bubble, no box sound); its RECORDED
# clip vo_demo3_sent with the words lit ([word-sync]); then T2's options flow — both slots blink together for 7 s while the tiles
# pop in one by one, each with its pop (no school sound / girl pop: no data.pic_sfx, data.girl_pop false, as T3); then the
# RECORDED explanation vo_demo3_explain "इस वाक्य में कई सारे नाम एक साथ लिखे गए हैं । जब हमें इस तरह कई नाम लिखने हों तो उनके
# बीच अल्पविराम आता है ।" (the [vo-rec] take; its whisper word times from vo_rec/transcripts.json) lighting the "," tile — the
# MIDDLE one — at "अल्पविराम" (7.06 s), the other two dim, the pulse, the child's tap, its border green, the comma in the left slot
# and 0.3 s later in the right one (data.mark_stagger_ms, the [demo-fig] page's stagger), each box gone 0.45 s after its comma, on
# to G1 by itself through the round's gate. The words before the slots carry the gaps (data.sentence.gaps -> .dsc-gap, its width
# CSS). vo_demo3_full / alp stay registered and shipped (unplayed, as T3's old clips); img_demo3_fruits stays (T1B shows it).
# [t4-basket] (asked 2026-11-02): "when the options appear the girl standing should show an animation of looking inside the fruit
# basket by raising the fruit basket a little bit she is carrying, and then looking back to the screen in the exact same position
# as shown; repeat every 7 seconds; perfect and smooth". As the first tile pops (stage 4, where T3's glance starts) .look runs one
# 7 s cycle on her layers (girl_rig_t4.py -> demo3_assets/girl_rig/, every window her own bitmap, so at rest she IS the painting):
# the basket with both hands rises 16 bitmap px (3.5 px on the page) over 0.65 s, her forearm sheared about the elbow so its
# wrist rises with the hand exactly; from 0.15 s her head with both braids dips 7 px (1.5 px) and her irises drop into the basket
# (6 px, a touch toward its middle) and drift over the fruit (to 4 px right by 1.3 s); from 1.65 s her eyes come back to the screen
# (as painted by 2.05 s), her head rises (2.25 s), the basket comes down (2.35 s) — the rest of the 7 s she is the painting, and
# the cycle repeats until the child's tap (the class leaves only in a rest phase, as T3's glance). Behind what the lift uncovers
# (under the basket, the handle's arc, the hands, the forearm) her dress / bodice / the background is the static picture copied
# from just past each band (girl_rig_t4.py: one offset per band, Poisson-matched at the seams). The amounts in her 224x336 box:
_rig4 = json.loads((SCR / "demo3_assets" / "girl_rig" / "rig.json").read_text(encoding="utf-8"))
GIRL4_BOX = (224, 336); _g4sx, _g4sy = GIRL4_BOX[0] / _rig4["bitmap"][0], GIRL4_BOX[1] / _rig4["bitmap"][1]   # the frame's 224x336 over the 1024x1535 bitmap
_lift4 = _rig4["lift"] * _g4sy; _sh4 = _rig4["shear"]
LOOK4 = {"every_ms": 7000, "active_ms": 2400, "anim": "dscBasketLift", "lift_px": round(_lift4, 3), "dip_px": round(_rig4["dip"] * _g4sy, 3),
         "shear_deg": round(math.degrees(math.atan(_lift4 / ((_sh4["x_w"] - _sh4["x_e"]) * _g4sx))), 4), "elbow_x": round(_sh4["x_e"] * _g4sx, 3),
         "gaze": [[round(1.5 * _g4sx, 3), round(6 * _g4sy, 3)], [round(4 * _g4sx, 3), round(6 * _g4sy, 3)]]}   # the irises: in (1.5, 6) then over the fruit (4, 6) bitmap px
_vr_t4 = json.loads((SCR / "vo_rec" / "transcripts.json").read_text(encoding="utf-8"))["vo_demo3_explain.wav"]
_x4_words = [w[0] for w in _vr_t4["words"]]
assert _x4_words.count("अल्पविराम") == 1 and _vr_t4["text"].startswith("इस वाक्य में कई सारे नाम"), _vr_t4["text"]
_sent4 = dict(dpart3("sent"), gaps=[2, 3])   # the slots sit after "आम" (word 2) and after "केला" (word 3)
assert _sent4["text_hi"] == "मेरे पास आम केला सेब और संतरा है ।" and len(_sent4["word_times"]) == 9 and _sent4["text_hi"].split()[2:4] == ["आम", "केला"], _sent4
card["slides"][i_t4] = {"id": "T4", "phase": "tutorial", "eis": "enactive", "type": "PUNCT_SCENE",
    "prompt_hi": dl3["sent"]["text"], "audio": {},
    "data": {"variant": "list", "intro_audio": None, "open_ms": 1000, "bg_id": "img_demo3_park", "image_id": "img_demo3_girl_basket", "girl_pop": False,   # the frame's girl, standing from the first frame
             "girl_rig": "basket", "girl_look": LOOK4,   # [t4-basket] her layers (the CSS) and the look into the basket's amounts / timing
             "slots": 2, "slot_w": 37, "slot_h": 42.606, "mark_stagger_ms": 300,   # the frame's two slots; the comma left, then right
             "sentence": _sent4, "mark": ",",
             "explain": {"text_hi": _vr_t4["text"], "audio": "vo_demo3_explain", "word_times": [w[1] for w in _vr_t4["words"]], "word_end": _vr_t4["words"][-1][2], "cue_word": _x4_words.index("अल्पविराम")},
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],   # the frame's order (T2's)
             "blink_ms": 7000, "blink_cycle_ms": 1750, "tiles_sfx": "sfx_demo1_pop.mp3", "tiles_gap_ms": 350},   # T2's blink and tiles
    "signals": {"on_complete": []}}
for k in DEMO3_CLIPS:   # [demo-intro] without the intro
    card["assets"]["audio"][f"vo_demo3_{k}"] = f"assets/Audio/vo_demo3_{k}.ogg"
    card["assets"]["audio_text"][f"vo_demo3_{k}"] = dl3[k]["text"]
card["assets"]["image"]["img_demo3_fruits"] = "assets/Images/img_demo3_fruits.webp"
card["_emoji_fallback"]["img_demo3_fruits"] = "✏️"
card["assets"]["image"]["img_demo3_park"] = "assets/Images/img_demo3_park.webp"   # [t4-scene] the frame's "image 264" fill, mirrored (1815x866, q90)
card["assets"]["image"]["img_demo3_girl_basket"] = "assets/Images/img_demo3_girl_basket.webp"   # [t4-scene] the frame's "image 276" fill (1024x1535, q90, alpha exact)
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
# [g1-scene] (asked 2026-11-02): G1 is now frame 715:856 "9 G1" — the first pick on T2's PUNCT_SCENE module (data.scene true,
# variant "pick", card class dsc-v-pick; the type stays PUNCT_PICK — the engine's whole-stage frame, the answerable type, the
# round — and the alias below sends a PUNCT_PICK page with data.scene to the scene module), in place of the [g1-pinki] page on the
# PUNCT_DEMO module (frame 656:66's title bar, picture box, sentence bar and data.layout all go with it; img_g1_girl_ball stays in
# the dist, unused). The frame: T2's card (96,106 1088x508) filled by a room picture ("image 274", 1829x860, drawn WHOLE at -3,-3
# 1095x514.872 of the card — the box has the bitmap's aspect; it covers the #404040 rectangle under it), the girl with the ball
# ("image 273", 1024x1536, at 133,57 252x378 of the card — the frame's last node) on her ellipse (749:2547, 154,395 158x34, #E1B48E
# .5 at .6), the sentence 714:845 "पिंकी गेंद से खेल रही थी " (Baloo 2 ExtraBold 55 #012F76, centred in a 557 box at 368,81 of the
# card; its text ends in a space), the white slot 724:2228 53x90 at 899,80 of the card (2px dashed rgba(86,86,86,.85), 8px corners),
# the tiles । , ? (T2's order, faces and mark offsets) at 494.09 / 721 / 951.818, 397 over #E1B48E .6 ellipses (118x26 at y 496),
# its own Swiftie 715:1051 (not used: T1's standing Swiftie and chip, as T2-T4), a hidden title bar. The flow, as asked: the
# instruction line vo_g1_intro over the picture and the girl, standing (T2's stage 1); 0.5 s after it the sentence rises in whole
# with the empty slot popping in and T1's text pop; its clip vo_g1_sent with the words lit ([word-sync]); 0.3 s later T2's options
# flow — the slot blinks 7 s (the slow whole-box fades) while the tiles pop in one by one, 350 ms apart, each with its pop (no
# school sound / girl pop: as T3 / T4) — and each tile is the CHILD's from the frame it pops in: no explanation, no pulse, all
# three tappable. The feedback is this page's own as before (the module's [g1-scene] pick mode): a wrong tile wiggles (wgNo) with
# the kit's wrong buzz, then the [vo-rec] hint ladder (hint 1 / hint 2 half a second after; the 3rd wrong tap the pointing hand
# under the right tile, the other two dead and dim, no line — [hand-quiet]); the right one is pressed (dmfTap, its colours kept),
# its mark lands in the slot in that frame with the kit's correct sound, the confetti and the happy Swiftie, "शाबाश!" (vo_ok)
# sounds and PACE.tail (1 s) later the page moves on to G2 (after the hand: no line, 1.7 s); [tap-lock] no tile answers while a
# feedback sound or line plays; the sentence's clip and its word light play ONCE ([g1-quiet], asked twice the same day: "once the
# VO of the sentence is over, the VO and the highlight animation should not repeat") — the engine's idle reminder is off here
# (data.no_idle_vo; it had re-read the sentence 7 s after the tiles went live, right as the blink ended) and the 🔊 chip, while the
# tiles are the child's, says the instruction line vo_g1_intro again instead (as the chip does on the lesson's ordinary pages).
# The clips are the ones in use before: vo_g1_intro and the hint / praise lines recorded ([vo-rec]), vo_g1_sent the TTS take
# (the recording says राजू). [g1-quiet] also: a wrong tile's wiggle had replayed its pop-in (dscTileIn) as the wiggle's class left
# — the animation list keeps dscTileIn first (style.css; the [t2-scene5] gotcha), fixed before the question was asked.
card["slides"][i_g1] = {"id": "G1", "phase": "guided", "eis": "enactive", "type": "PUNCT_PICK",
    "prompt_hi": gl["intro"]["shown"], "audio": {"prompt": "vo_g1_intro"},
    "data": {"scene": True, "variant": "pick", "intro_audio": "vo_g1_intro", "bg_id": "img_g1_room", "image_id": "img_g1_girl_ball2", "girl_pop": False,   # the frame's room and girl, standing from the first frame
             "sentence": {"text_hi": gl["sent"]["shown"], "audio": "vo_g1_sent", "word_times": [t[0] for t in gl["sent"]["word_times"]], "word_end": gl["sent"]["word_times"][-1][1]},
             "mark": "।", "mark_audio": "vo_demo1_purn",   # ([vo-rec] sets the name, the praise and the hint lines below)
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],   # the frame's order (T2's)
             "blink_ms": 7000, "blink_cycle_ms": 1750, "tiles_sfx": "sfx_demo1_pop.mp3", "tiles_gap_ms": 350,   # T2's blink and tiles
             "no_idle_vo": True},   # [g1-quiet] (asked 2026-11-02): the sentence's clip and its word light play ONCE — the engine's idle reminder (after 7 s of quiet once the tiles are the child's, which fell right at the blink's end) is off on this page, and the 🔊 chip says the instruction line again (the module)
    "signals": {"on_complete": ["punct_build_done"]}}
for k in G1_KEYS:
    card["assets"]["audio"][f"vo_g1_{k}"] = f"assets/Audio/vo_g1_{k}.ogg"
    card["assets"]["audio_text"][f"vo_g1_{k}"] = gl[k]["text"]
card["assets"]["image"]["img_g1_girl_ball"] = "assets/Images/img_g1_girl_ball.webp"   # [g1-pinki]
card["_emoji_fallback"]["img_g1_girl_ball"] = "✏️"
card["assets"]["image"]["img_g1_room"] = "assets/Images/img_g1_room.webp"   # [g1-scene] the frame's "image 274" fill (1829x860, q90)
card["assets"]["image"]["img_g1_girl_ball2"] = "assets/Images/img_g1_girl_ball2.webp"   # [g1-scene] the frame's "image 273" fill (1024x1536, q90, alpha exact)
card["_emoji_fallback"]["img_g1_room"] = "🏠"; card["_emoji_fallback"]["img_g1_girl_ball2"] = "✏️"
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
# [g2-scene] (asked 2026-11-02): G2 is now frame 716:1058 "10 G2" — G1's scene pick ([g1-scene]: the PUNCT_SCENE module's pick
# mode, type PUNCT_PICK + data.scene, variant "pick2", card class dsc-v-pick2) with the "?" the answer, in place of the [g2-girl]
# page on the PUNCT_DEMO module (frame 600:197's title bar, picture box, sentence bar and data.layout go with it; img_g2_girl_bag
# and img_g2_boy_bag stay in the dist, unused). The frame: T2's card (96,106 1088x508) filled by a street picture ("image 266",
# 1815x866 — the same size as T4's park bitmap but a different picture, drawn WHOLE at -34,-5 1152.714x550 of the card: the box
# has the bitmap's aspect); the girl with the yellow bag, walking ("image 275", 1024x1536, at 934,227 236x354 of the STAGE — a
# child of the frame, not the card, drawn last; her box lies inside the card's padding box, and her ink clear of the tiles) on her
# ellipse (750:2551, 969,534 145x38, #E99560 .41); the sentence 724:2257 "तुम कहाँ जा रहे हो" (Baloo 2 ExtraBold 55 #012F76, centred
# in a 479 box at 363,189 of the stage); the white slot 724:2258 59x100 (T3's size) at 791,184; the tiles । , ? (T2's order, faces
# and mark offsets) at 334.09 / 561 / 791.82, 426 — NO ellipses under them in this frame; its own Swiftie 716:1250 (not used: T1's
# standing Swiftie and chip, as T2-T4 / G1); a hidden title bar, a hidden "image 218" and a stray copy of the T3 frame parked at
# y -3415 (outside the frame: not drawn). The flow is G1's to the letter (the same data keys): the instruction line vo_g1_intro
# over the picture and the girl; the sentence rising with the slot popping in and T1's text pop; its RECORDED clip vo_g2_sent with
# the words lit, once ([g1-quiet]: no idle re-read, the chip says the instruction line again); the 7 s blink with the tiles popping
# in one by one, each the child's as it pops; a wrong tile's wiggle + buzz + the hint ladder (hint 1, hint 2, the hand on the 3rd);
# the right tile ("?", the third) pressed, its mark in the slot with the correct sound, the confetti and "शाबाश!", G3 1 s later.
card["slides"][i_g2] = {"id": "G2", "phase": "guided", "eis": "enactive", "type": "PUNCT_PICK",
    "prompt_hi": gl["intro"]["shown"], "audio": {"prompt": "vo_g1_intro"},
    "data": {"scene": True, "variant": "pick2", "intro_audio": "vo_g1_intro", "bg_id": "img_g2_street", "image_id": "img_g2_girl_bag2", "girl_pop": False,   # the frame's street and girl, standing from the first frame
             "slot_w": 59, "slot_h": 100,   # the frame's slot (T3's size)
             "sentence": {"text_hi": gl2["shown"], "audio": "vo_g2_sent", "word_times": [t[0] for t in gl2["word_times"]], "word_end": gl2["word_times"][-1][1]},
             "mark": "?", "mark_audio": "vo_demo2_prashn",   # ([vo-rec] sets the name, the praise and the hint lines below)
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],   # the frame's order (T2's)
             "blink_ms": 7000, "blink_cycle_ms": 1750, "tiles_sfx": "sfx_demo1_pop.mp3", "tiles_gap_ms": 350,   # T2's blink and tiles
             "no_idle_vo": True},   # [g1-quiet] as G1: the sentence's clip and its word light play once
    "signals": {"on_complete": ["punct_build_done"]}}
card["assets"]["audio"]["vo_g2_sent"] = "assets/Audio/vo_g2_sent.ogg"
card["assets"]["audio_text"]["vo_g2_sent"] = gl2["text"]
card["assets"]["image"]["img_g2_girl_bag"] = "assets/Images/img_g2_girl_bag.webp"   # [g2-girl]
card["_emoji_fallback"]["img_g2_girl_bag"] = "✏️"
card["assets"]["image"]["img_g2_street"] = "assets/Images/img_g2_street.webp"   # [g2-scene] the frame's "image 266" fill (1815x866, q90)
card["assets"]["image"]["img_g2_girl_bag2"] = "assets/Images/img_g2_girl_bag2.webp"   # [g2-scene] the frame's "image 275" fill (1024x1536, q90, alpha exact)
card["_emoji_fallback"]["img_g2_street"] = "🏫"; card["_emoji_fallback"]["img_g2_girl_bag2"] = "✏️"
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
# [g3-scene] (asked 2026-11-02): G3 is now frame 716:1262 "11 G3" — G1's scene pick ([g1-scene]: the PUNCT_SCENE module's pick
# mode, type PUNCT_PICK + data.scene, variant "pick3", card class dsc-v-pick3) with the "," the answer, landing in the sentence's
# OWN slot (T4's in-sentence slot: data.sentence.gaps names the word the gap follows, the gap's width and the slot's place are the
# variant's CSS), in place of the [pick-fig] page on the PUNCT_DEMO module (frame 528:424's title bar, picture box, sentence bar,
# its per-side-dashed small slot and data.layout go with it; img_g3_flowers stays in the dist, unused). The frame: T2's card
# (96,106 1088x508) filled by a garden picture ("image 284", 1671x941 — T2's hallway bitmap's size, a different picture; drawn at
# -15,-120 1117x630 of the card, cover — the box's aspect is the bitmap's to 0.2%, so nothing to speak of is cropped); the girl
# pointing at the flowers ("image 283", 1024x1536, at 138,135 218x328 of the card) on her ellipse (810:14, 147,433 172x38, #97CF28
# at .4); the sentence 807:6 "बाग में गुलाब    गेंदा और चमेली के फूल हैं ।" (Baloo 2 ExtraBold 55 #012F76, centred in a 893 box at
# 98,36 of the card, with a four-space run after गुलाब where the white slot 807:7 33x38 sits at 388,83 — 2px dashed
# rgba(86,86,86,.85), 8px corners; the sentence already ending with its danda); the tiles । , ? (T2's order, faces and mark
# offsets) at 474.09 / 701 / 931.82, 467 over opaque #97CF28 ellipses (118x26 at y 566, on the grass); its own Swiftie 716:1454
# (not used: T1's standing Swiftie and chip, as T2-T4 / G1 / G2); a hidden title bar and a hidden "image 218". The flow is G1's to
# the letter (the module unchanged): the instruction line vo_g1_intro over the picture and the girl, standing; 0.5 s later the
# sentence rising whole with the small slot popping in and T1's text pop; its RECORDED clip vo_g3_sent with the ten words lit
# (the danda a word of its own), once ([g1-quiet]: no idle re-read, the chip says the instruction line again); the 7 s blink with
# the tiles popping in one by one, each the child's as it pops; a wrong tile's wiggle + buzz + the hint ladder (hint 1, hint 2, the
# hand on the 3rd); the right tile (",", the middle one) pressed, its comma in the slot (its ink centred) with the correct sound,
# the confetti and "शाबाश!", G4 1 s later.
card["slides"][i_g3] = {"id": "G3", "phase": "guided", "eis": "enactive", "type": "PUNCT_PICK",
    "prompt_hi": gl["intro"]["shown"], "audio": {"prompt": "vo_g1_intro"},
    "data": {"scene": True, "variant": "pick3", "intro_audio": "vo_g1_intro", "bg_id": "img_g3_garden", "image_id": "img_g3_girl_point", "girl_pop": False,   # the frame's garden and girl, standing from the first frame
             "slot_w": 33, "slot_h": 38,   # the frame's small slot, inside the sentence
             "sentence": {"text_hi": gl3["shown"], "audio": "vo_g3_sent", "word_times": [t[0] for t in gl3["word_times"]], "word_end": gl3["word_times"][-1][1],
                          "gaps": [2]},   # the slot sits after गुलाब (word 2): the gap's width is the variant's CSS (.dsc-gap)
             "mark": ",", "mark_audio": "vo_demo3_alp",   # ([vo-rec] sets the name, the praise and the hint lines below)
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],   # the frame's order (T2's)
             "blink_ms": 7000, "blink_cycle_ms": 1750, "tiles_sfx": "sfx_demo1_pop.mp3", "tiles_gap_ms": 350,   # T2's blink and tiles
             "no_idle_vo": True},   # [g1-quiet] as G1: the sentence's clip and its word light play once
    "signals": {"on_complete": ["punct_build_done"]}}
card["assets"]["audio"]["vo_g3_sent"] = "assets/Audio/vo_g3_sent.ogg"
card["assets"]["audio_text"]["vo_g3_sent"] = gl3["text"]
card["assets"]["image"]["img_g3_flowers"] = "assets/Images/img_g3_flowers.webp"
card["_emoji_fallback"]["img_g3_flowers"] = "✏️"
card["assets"]["image"]["img_g3_garden"] = "assets/Images/img_g3_garden.webp"   # [g3-scene] the frame's "image 284" fill (1671x941, q90)
card["assets"]["image"]["img_g3_girl_point"] = "assets/Images/img_g3_girl_point.webp"   # [g3-scene] the frame's "image 283" fill (1024x1536, q90, alpha exact)
card["_emoji_fallback"]["img_g3_garden"] = "🌳"; card["_emoji_fallback"]["img_g3_girl_point"] = "✏️"
# [g3-grow] (asked 2026-11-02): "when the page starts and the image in the blue frame and the girl is shown, the plants in the image
# should show a growing animation for once, synced with this sound effect (freesound_community-014_plantacreciendo-003-44289.mp3),
# the three plants growing to their original size shown in the image, and the girl's eyes moving towards the plants and then towards
# the screen; only after that the sentence should come and the whole flow continue as it is; keep repeating the eyes' movement every
# 7 seconds; perfect and smooth". The garden's three plants (the rose, the marigold, the jasmine) are cut from its bitmap by
# plant_rig_g3.py (g3_assets/plant_rig/: the garden WITHOUT them — the lawn and the tree line behind them rebuilt from the same
# rows, the soil's top edge carried across under the stems, lossless so every other pixel is the painting's — and each plant as its
# own RGBA cut-out whose edge is un-mixed from that garden, so plant-over-garden IS the painting, max 1 level). The page opens on the
# garden without them (data.bg_id = img_g3_garden_bare; img_g3_garden stays in the dist, unused); once the garden and the plants are
# decoded and no sooner than start_ms (past the page's .34 s slide-in) each plant GROWS out of its soil from its stem's base —
# shooting up first (dscPlantH: its height, from .03 past its size to 1.08, a little under, a little over, home) and spreading a
# beat behind (dscPlantW: its width from .22, past to 1.05, home) — the three one after another, each reaching its overshoot on one
# of the sound's three loudest creaks (0.55, 1.075 and 1.35 s into it: delays 0 / 495 / 770 ms, 58% of 1 s), the jasmine home at
# 1.77 s as the sound dies away (1.9 s). The user's sound is 37 dB under the lesson's voice (-55.5 LUFS): raised 29 dB as it is
# (g3_assets/sfx_g3_grow.mp3, -26.9 LUFS, peak -2 dB, not shifted; the user's bytes kept as sfx_g3_grow_source.mp3). The girl's eyes
# are layers of her own bitmap (girl_rig_g3.py: each eye's interior masked, a cover over the painted iris, the iris — her face is
# three-quarter, the irises upright ellipses — completed where it runs on under the outline); look_ms into the growth her irises
# slide down and to her left, to the plants (data.girl_look.gaze: 4 / 10 bitmap px), hold while they grow, and are back exactly as
# painted ("the screen", as T4's "back to the screen in the exact same position") by 2.1 s; the glance repeats every 7 s until the
# answer (lookOff: only in a rest phase). then_ms after the growth began the page goes on exactly as before: the instruction line,
# 0.5 s, the sentence, the tiles (the glance's cycle runs on across them).
_prig3 = json.loads((SCR / "g3_assets" / "plant_rig" / "rig.json").read_text(encoding="utf-8"))
_erig3 = json.loads((SCR / "g3_assets" / "girl_rig" / "rig.json").read_text(encoding="utf-8"))
assert [q["name"] for q in _prig3["plants"]] == ["rose", "marigold", "jasmine"] and _prig3["bitmap"] == [1671, 941], _prig3["bitmap"]
assert all(q["rest_err_decoded"]["max"] <= 1.5 for q in _prig3["plants"]) and _prig3["bare"]["outside_holes_max_diff"] == 0, "plant_rig_g3.py: plant over bare is not the painting"
assert _erig3["bitmap"] == [1024, 1536] and _erig3["rest_diff"]["max"] <= 4, "girl_rig_g3.py: the eyes at rest are not the painting"
G3_BGS = 630 / 941; G3_BGX = -27 + (1117 - 1671 * G3_BGS) / 2; G3_BGY = -132   # the garden's cover in its 1117x630 box at -27,-132 (the height binds: 0.87 px off each side)
G3_GS = 328 / 1536; G3_GX = (218 - 1024 * G3_GS) / 2                           # the girl's cover in her 218x328 box (0.33 px off each side)
GROW3 = {"plants": [f"img_g3_plant_{q['name']}" for q in _prig3["plants"]], "sfx": "sfx_g3_grow.mp3", "sfx_vol": 0.9,
         "start_ms": 600, "dur_ms": 1000, "delays_ms": [0, 495, 770], "look_ms": 300, "then_ms": 2700}
LOOK3 = {"every_ms": 7000, "active_ms": 2100, "anim": "dscEyesLook", "warm_ms": 380, "gaze": [round(_erig3["gaze"][0] * G3_GS, 3), round(_erig3["gaze"][1] * G3_GS, 3)]}
card["slides"][i_g3]["data"].update({"bg_id": "img_g3_garden_bare", "grow": GROW3, "girl_rig": "eyes", "girl_look": LOOK3})
card["assets"]["image"]["img_g3_garden_bare"] = "assets/Images/img_g3_garden_bare.webp"; card["_emoji_fallback"]["img_g3_garden_bare"] = "🌳"
for _q in _prig3["plants"]:
    card["assets"]["image"][f"img_g3_plant_{_q['name']}"] = f"assets/Images/img_g3_plant_{_q['name']}.webp"; card["_emoji_fallback"][f"img_g3_plant_{_q['name']}"] = "🌱"
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
assert [s["id"] for s in card["slides"]] == ["T0", "T0B", "T1", "T1B", "T1C", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "CEL"], "unexpected page list after the removal"   # [recap-alp] + T1B, [recap-prashn] + T1C
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
assert [s["id"] for s in card["slides"]] == ["T0", "T0B", "T1", "T1B", "T1C", "T2", "T3", "T4", "G1", "G2", "G3", "G4", "P1", "P2", "L1", "L2", "CEL"]   # [recap-alp] + T1B, [recap-prashn] + T1C
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
function sfigNarrate(L, live, onEnd, S){
  const Y = S || L;   // [recap-fig2] the line whose words light on the clip: the line itself, or another (T1's sign on the name's clip)
  let done = false;
  const end = ()=>{
    if(done || !live()) return;
    done = true;
    if(Y.unsync) Y.unsync();
    sfigShow(L, L.words.length);
    onEnd();
  };
  const read = ()=>{
    if(!live()) return;
    play(L.src, end);
    sfigSync(Y);
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
      /* [relisten-sfx] (2026-11-01) T1's text sounds ([recap-sfx]: the reference hi02h11l02s04-file5 page 2's sfxPopSoft, the
         engine's own _tone): each sentence gets the soft pop as it rises in — only on a real appearance, so the 🔊 replay (the
         sentences already on screen) is silent, as T1's is */
      const popSoft = ()=> _tone([720], "sine", 0.10, 0.07);
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
        const readLine = (k)=>{
          if(!Ls[k].shown) popSoft();   // [relisten-sfx] the sentence rises in now (sfigNarrate); a replay's, already there, is silent
          sfigNarrate(Ls[k], live, ()=>{ if(k + 1 < Ls.length) setTimeout(()=>{ if(live()) readLine(k + 1); }, 600); else explain(); });
        };
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
recap_mod = r"""  /* ===== [recap-fig] MARKS_RECAP — the mark page after the read-again page. [recap-fig2] (2026-11-01): laid out as FLN-by-MJ
     frame 764:144 "html_Guided_instructions" (was 508:2, the three-marks recap in rows) — ONE mark: the sign in its white box
     with its name beside it, the example sentence in a white box under them, the picture at the right — on T0B's card, grid,
     Swiftie and 🔊 chip. Everything arrives WITH its narration: the lead line ([vo-rec]) and the intro line sound over the
     card alone (the frame has no title); then the box + sign pop in as the name rises in whole, and the name's clip lights the
     SIGN (the words' orange + pop, [word-sync]) for as long as it says the name; the use's clip sounds with nothing new on
     screen; then the sentence's box pops in as the sentence rises in whole and its clip follows — as it reaches the sentence's
     first word the picture pops in and the words light one by one; the mark at the sentence's end keeps its orange once lit.
     आगे (T0's place) only ever shows LIVE, when the example has been read; the 🔊 chip is ignored while the page reads itself
     (the sequence drives itself) and afterwards reads it again from the name — everything staying, the sign and the words lit
     again, the kept mark cleared until it is lit again — hiding आगे until that replay ends. ===== */
  MARKS_RECAP: {
    mount(host, slide){
      const d = slide.data || {}, GAP = 300, GAP_MARK = 700;
      const A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const fig = sfigMount(host,
        '<div class="rcf-row' + (d.variant ? ' rcf-v-' + d.variant : '') + '"><div class="rcf-sign"><div class="rcf-mark"><p><span class="sfig-w on"></span></p></div></div>' +   // [recap-alp] a frame's own placements: .rcf-v-<variant>
        '<div class="rcf-name"><p></p></div><div class="rcf-ebox"></div><div class="rcf-eg"><p></p></div>' +
        '<div class="rcf-pic"><img src="' + imgSrc(d.image_id) + '" alt="" draggable="false"></div></div>');
      const card = host.closest(".tut-card"); if(card) card.classList.add("sfig-round", "sfig-recap");
      const sign = fig.querySelector(".rcf-sign"), glyph = fig.querySelector(".rcf-mark .sfig-w"),
            ebox = fig.querySelector(".rcf-ebox"), pic = fig.querySelector(".rcf-pic");
      glyph.textContent = d.mark || "";
      const nm = d.name || {}, wh = d.when || {}, eg = d.example || {};
      const Lname = sfigLine(fig.querySelector(".rcf-name p"), nm.text_hi, nm.word_times, nm.audio, nm.word_end);
      const Leg = sfigLine(fig.querySelector(".rcf-eg p"), eg.text_hi, eg.word_times, eg.audio, eg.word_end);
      // the sign reads as a one-word line on the name's clip (sfigSync): lit from the clip's first word to its last word's end
      const Lsign = { p: glyph.parentElement, words: [glyph], share: [0], times: [Lname.times ? Lname.times[0] : 0],
                      end: Lname.end, src: Lname.src, file: Lname.file, shown: true };
      // the sentence's marks keep their orange once the clip has lit them: a token of punctuation alone (T1's "।") whole; a mark
      // ending a word ([recap-alp] T1B's "आम," / "केला,") split off into its own span, so the word lights and goes as the others
      // do and only its mark stays lit
      const keeps = [];
      Leg.words.forEach((w, i)=>{
        if(/^[।?,!]+$/.test(w.textContent)){ keeps.push({ el: w, i }); return; }
        const m = w.textContent.match(/^(.+?)([।?,!]+)$/);
        if(m){ w.textContent = m[1]; const s = document.createElement("span"); s.className = "rcf-mk"; s.textContent = m[2]; w.appendChild(s); keeps.push({ el: s, i }); }
      });
      const egTimes = Leg.times || [];
      // the picture at the sentence's first word; each kept mark at its own word's start
      const cues = [egTimes[0] || 0].concat(egTimes.length ? keeps.map(k=> egTimes[k.i]) : []);

      state.ownsAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
      setSwMood("talk");
      const alive = ()=> fig.isConnected;
      let run = 0;
      const armNav = ()=>{ if(!alive()) return; state.demoRunning = false; setNavActive(true); setSwMood("point"); };
      // a clip with nothing to light: it sounds, then onEnd (a watchdog stops a stalled clip, as sfigNarrate's)
      const say = (src, live, onEnd)=>{
        if(!src){ onEnd(); return; }
        let done = false; const end = ()=>{ if(done || !live()) return; done = true; onEnd(); };
        play(src, end);
        setTimeout(()=>{ if(!done && live()){ stopAudio(); end(); } }, authoredVoHoldMs(src) + 10000);
      };
      // cues (seconds on the clip's own clock) on the clip `file`, which sfigNarrate starts after the text's rise: waits for it,
      // then onCue(i) as each is reached; the ones not reached when the clip is gone fire then, so nothing is skipped
      const cueOn = (file, onCue, live)=>{
        let next = 0; const t0 = Date.now();
        const own = (a)=> !!a && decodeURIComponent(String(a.currentSrc || a.src || "").split("/").pop()) === file;
        const wait = ()=>{ if(!live()) return;
          const a = currentAudio;
          if(!own(a)){ if(Date.now() - t0 < SENT_IN_MS + 3000) nextFrame(wait); else while(next < cues.length) onCue(next++); return; }
          const tick = ()=>{ if(!live()) return;
            const gone = a.ended || currentAudio !== a || (a.paused && a.currentTime > 0);
            while(next < cues.length && (gone || a.currentTime + 0.04 >= cues[next])) onCue(next++);
            if(next < cues.length) nextFrame(tick); };
          tick(); };
        wait();
      };
      /* [recap-sfx] (2026-11-01) the sounds of the reference hi02h11l02s04-file5's page 2 (T2, MATRA_BUILD), read live: each thing
         that APPEARS gets its sfxPopSoft — _tone([720], "sine", 0.10, 0.07), the engine's own _tone — and the picture gets the
         horse's: its fbCorrect = the file sfx_fb_correct (data.pic_sfx, the reference's bytes) at .55. Only on a real appearance:
         a replay, with everything already on screen, is silent, as the reference's showPic() is */
      const popSoft = ()=> _tone([720], "sine", 0.10, 0.07);
      const appear = (el)=>{ if(el.classList.contains("in")) return false; el.classList.add("in"); return true; };
      if(d.pic_sfx && !_kitSfx.recapPic){ const a = _kitSfx.recapPic = new Audio("assets/Audio/" + d.pic_sfx); a.preload = "auto"; }   // fetched now, heard ~15 s later
      const readAll = ()=>{
        const mine = ++run, live = ()=> mine === run && alive();
        state.demoRunning = true;   // the chip is ignored until the page has been read; a replay hides आगे meanwhile
        setNavActive(false);
        keeps.forEach(k=> k.el.classList.remove("keep"));   // [word-sync] a replay keeps everything on screen; the kept light goes until it is lit again
        // 1. the box + sign pop in as the name rises; the name's clip lights the sign
        if(appear(sign)) popSoft();
        sfigNarrate(Lname, live, ()=>{
          // 2. the use's clip, nothing new on screen
          setTimeout(()=>{ if(!live()) return; say(A(wh.audio), live, ()=>{
            // 3. the sentence's box pops in as the sentence rises; its clip: the picture pops in at the first word, the words
            //    light one by one, the mark at the end keeps its light
            setTimeout(()=>{ if(!live()) return;
              if(appear(ebox)) popSoft();
              const onCue = (i)=>{ if(i === 0){ if(appear(pic) && d.pic_sfx) playKitSfx("recapPic", d.pic_sfx, .55); }
                                   else if(keeps[i - 1]) keeps[i - 1].el.classList.add("keep"); };
              sfigNarrate(Leg, live, ()=>{ cues.forEach((_, i)=> onCue(i)); armNav(); });
              cueOn(Leg.file, onCue, live);
            }, GAP); }); }, GAP);
        }, Lsign);
      };
      // the lead line ([vo-rec], data.lead_audio) then the intro line (data.intro_audio), both over the card alone; then the mark
      state.demoRunning = true;
      let introDone = false;
      const afterIntro = ()=>{ if(introDone || !alive()) return; introDone = true; setTimeout(()=>{ if(alive()) readAll(); }, GAP_MARK); };
      say(A(d.lead_audio), alive, ()=> say(A(d.intro_audio), alive, afterIntro));
      state.replayAudio = readAll;
    }
  },

"""
js = sub1(js, r"^  PHASE_TRANSITION: \{", lambda m: recap_mod + m.group(0), re.M, "PHASE_TRANSITION anchor (recap)")
scene_mod = r"""  /* ===== [t2-scene] PUNCT_SCENE — T2, the first example (FLN-by-MJ frame 706:188 "2 T0B"), on T0B / T1's card (.sfig-round:
     the frame's 1088x508 card at 96,106, 64px corners; the standing Swiftie and the 🔊 chip where page 3 T1 has them): the
     frame's hallway picture fills the card; the sentence "पिंकी स्कूल जा रही है" with an empty dashed slot after it; the girl
     walking in from the doorway; three mark tiles. It drives itself up to the tap:
     1. the intro line (data.intro_audio) over the picture alone — no sentence, no girl, no tiles;
     2. 0.5 s after it the sentence rises in whole and the slot pops in, with T1's text pop ([recap-sfx] popSoft); 0.45 s later
        the sentence's clip, each word lit as it is read ([word-sync]);
     3. 0.3 s after the clip data.pic_sfx (the user's school sound) for data.pic_sfx_ms (2 s), faded out over its last 0.4 s, and
        the girl — in her place since the first frame ([t2-scene2]; she walked in from the doorway before) — gives a small pop
        (CSS dscPop) as it starts;
     4. 0.3 s after the sound the slot blinks for data.blink_ms ([t2-scene5]: 7 s in SLOW data.blink_cycle_ms = 1.75 s cycles —
        the WHOLE box, wearing its orange look (its fill the orange's tint, its ring the words' orange, its glow the pulsing tile's
        rgba(232,106,0,.6) 5px), FADES out and back in four times — 0.56 s fades, 0.21 s unseen, 0.42 s seen — and ends seen, the
        look easing back to plain; [t2-scene4] switched the look on / off on 1.2 s cycles, [t2-scene2] held the orange for half
        of a ~0.67 s cycle) and, as the blink starts, the three tiles pop in ONE BY ONE (data.tiles_gap_ms
        = 350 ms apart, each from small past its size — dscTileIn) each with its own data.tiles_sfx (the user's pop) in its frame
        ([t2-scene3]; before, all three came in 90 ms apart under a single pop);
     5. 0.3 s after the blink the explanation (data.explain): as it reaches its cue word (data.explain.cue_word, "पूर्णविराम") the
        danda's tile lights — the words' orange on its mark (+ p2WordPop) and an orange border + glow on its face; 0.3 s after
        the clip the other two tiles go dim (.off, [t2-scene2]: .6, not the demos' .35) and dead; 0.3 s later the lit tile
        pulses (dscPulse; its orange glow breathing .6 -> .7, [t2-scene3]: a little stronger than the .45 / .55 before) and is the
        CHILD's: the page waits for the tap (the 🔊 chip reads the sentence again meanwhile);
     6. the tap: the tile's BORDER turns green ([t2-scene2]: the face stays white, the mark its blue), the kit's correct sound
        (sfxCorrect), the mark lands in the slot (its INK centred, the demos' centreInk), 0.45 s later the slot's box goes (the
        mark stays) and 1.2 s after that the page moves on by itself: no आगे here.
     [t3-scene] T3 (frame 724:2016 "7 T3") runs on this module too, as data.variant "ask" (the card gets dsc-v-ask; its geometry is
        CSS): no intro line (data.intro_audio null — the scene stands for data.open_ms), a speech bubble (data.bubble_id, an SVG)
        popping in with the sentence and the slot in stage 2 to data.box_sfx (the user's sharp pop) instead of T1's tone, the slot's
        box data.slot_w x data.slot_h, the recorded explanation, the "?" as the middle tile; everything else as T2.
     [t3-girl] T3's girl is the frame's own (data.image_id), still from the first frame: data.girl_pop false and no data.pic_sfx skip
        stage 3, so the blink starts 0.3 s after the sentence's clip.
     [t3-look] With data.girl_rig the girl is LAYERS of her bitmap (.dsc-grig: the body, the two eyes, the forearm, the braid tip —
        the masks and their geometry are the CSS's, from girl_rig.py) and, as the first tile pops (stage 4), .look starts her
        glance: the eyes slide toward the tiles, a small lean their way, the open hand lifts and bobs, all back exactly as painted
        by data.girl_look.active_ms (2.3 s) of an every_ms (5 s) cycle that repeats until the tap — the class is taken off only in
        a rest phase of the cycle, so she is never caught mid-move.
     [t4-basket] With data.girl_rig "basket" (T4) the layers are girl_rig_t4.py's (.dsc-brig: the patch behind what the lift
        uncovers, the body, the forearm, the elbow's fold over it, the head group — the head, both braids, the eyes inside it —,
        the basket with both hands) and the same .look, as the first tile pops, runs her look into the basket (data.girl_look:
        the amounts in her box px; lookOff reads data.girl_look.anim's clock).
     [t4-scene] T4 (frame 723:1575 "8 T4") runs on this module too, as data.variant "list": TWO slots (data.slots, each a
        .dsc-slot sN, placed by the variant's CSS) inside the sentence — the words before them (data.sentence.gaps) carry the gaps
        (.dsc-gap) — that pop in, blink and fill together; on the tap the mark lands in each in turn, data.mark_stagger_ms apart,
        each box going 0.45 s after its mark, the page moving on 1.2 s after the last. One slot (T2, T3): as before.
     [g1-scene] G1 (frame 715:856 "9 G1", type PUNCT_PICK with data.scene, variant "pick") runs on this module as the CHILD's pick
        — and since [g2-scene] / [g3-scene] G2 and G3 too (frames 716:1058 "10 G2", variant "pick2", the "?" the answer, and
        716:1262 "11 G3", variant "pick3", the "," landing in the sentence's own slot: data.sentence.gaps as T4's; the geometry the CSS's):
        stages 1, 2 and 4 as T2's (the intro line, the sentence and the slot, the blink with the tiles popping in), and from the
        frame each tile pops in it is live — no explanation (stage 5), no lit tile, no pulse, all three tappable. The feedback is
        the pick page's (PUNCT_DEMO's tap mode) as before on G1: a wrong tile wiggles (wgNo) with the kit's wrong buzz, then the
        hint ladder (data.hint1_audio / hint2_audio 0.5 s after; the 3rd wrong tap the pointing hand under the right tile, the
        other two dead and dim, no line); the right one presses (dmfTap, its colours kept), its mark lands in the slot in that
        frame with the kit's correct sound, the confetti and the happy Swiftie, "शाबाश!" (data.ok_audio) and PACE.tail later the
        page moves on (after the hand: no line, 1.7 s). No tile answers while a feedback sound or line plays ([tap-lock]); the
        🔊 chip says the instruction line again — the sentence and its word light play once on G1 ([g1-quiet]; the engine's
        idle reminder is off there: data.no_idle_vo). ===== */
  PUNCT_SCENE: {
    mount(host, slide){
      const d = slide.data || {}, S = d.sentence || {}, X = d.explain || {}, opts = d.options || [];
      const A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const sw = d.slot_w || 53, sh = d.slot_h || 90;   // [t3-scene] the slot's box: T2's 53x90, T3's 59x100 (the ring drawn to size)
      const nSlots = Math.max(1, d.slots || 1);   // [t4-scene] T4's two slots inside its sentence
      // [t3-look] with data.girl_rig the girl is her bitmap in layers (every layer a window on the same image, masked by the CSS):
      // the body, each eye (the window, the sclera disc, the iris), the forearm, the braid tip; without it, the one image as before
      const gimg = '<img class="dsc-gwin" src="' + imgSrc(d.image_id) + '" alt="" draggable="false">';
      // [t4-basket] data.girl_rig "basket" (T4): the patch behind what the lift uncovers, the body, the forearm (sheared about the
      // elbow's line), the elbow's fold over it, the head group (the head with both braids; the eyes inside it), the basket with
      // both hands — every window the same bitmap, masked by the CSS
      const bwin = (c)=> '<img class="' + c + '" src="' + imgSrc(d.image_id) + '" alt="" draggable="false">';
      const basketHtml = '<div class="dsc-girl"><span class="dsc-shade"></span><div class="dsc-brig"><span class="dsc-bunder"></span>' + bwin("dsc-bbody") + bwin("dsc-bfore") + bwin("dsc-belbow") +
        '<div class="dsc-bhead">' + bwin("dsc-bheadw") + [1, 2].map(k=> '<div class="dsc-beye e' + k + '">' + bwin("dsc-bwin") + '<span class="dsc-bfill"></span><span class="dsc-biris"></span></div>').join("") + '</div>' +
        bwin("dsc-bbasket") + '</div></div>';
      // [g3-grow] data.girl_rig "eyes" (G3): her one image as before and, over it, each eye's interior (masked by its sheet) holding
      // the cover over the painted iris and the iris itself, which slides; nothing else of her is touched
      const eyesHtml = '<div class="dsc-girl"><span class="dsc-shade"></span><img src="' + imgSrc(d.image_id) + '" alt="" draggable="false"><div class="dsc-erig">' +
        [1, 2].map(k=> '<div class="dsc-eeye e' + k + '"><span class="dsc-efill"></span><span class="dsc-eiris"></span></div>').join("") + '</div></div>';
      // [g3-grow] data.grow: the garden's plants, each its own cut-out over the garden without them (data.bg_id), growing from its stem
      const G = d.grow || null;
      const plantsHtml = G ? '<div class="dsc-plants">' + G.plants.map((id, k)=> '<div class="dsc-plant p' + (k + 1) + '"><img src="' + imgSrc(id) + '" alt="" draggable="false"></div>').join("") + '</div>' : '';
      const girlHtml = d.girl_rig === "eyes" ? eyesHtml : d.girl_rig === "basket" ? basketHtml : d.girl_rig
        ? '<div class="dsc-girl"><span class="dsc-shade"></span><div class="dsc-grig">' + gimg.replace("dsc-gwin", "dsc-gbody") +
          '<div class="dsc-geye e1">' + gimg + '<span class="dsc-gfill"></span><span class="dsc-giris"></span></div>' +
          '<div class="dsc-geye e2">' + gimg + '<span class="dsc-gfill"></span><span class="dsc-giris"></span></div>' +
          '<div class="dsc-garm">' + gimg + '</div><div class="dsc-gpatch">' + gimg + '</div></div></div>'
        : '<div class="dsc-girl"><span class="dsc-shade"></span><img src="' + imgSrc(d.image_id) + '" alt="" draggable="false"></div>';
      const fig = sfigMount(host,
        '<div class="dsc-bg"><img src="' + imgSrc(d.bg_id) + '" alt="" draggable="false">' + plantsHtml + girlHtml + '</div>' +
        (d.bubble_id ? '<img class="dsc-bubble" src="' + imgSrc(d.bubble_id) + '" alt="" draggable="false">' : '') +   // [t3-scene] the frame's speech bubble, popping in with the sentence
        '<p class="dsc-sent"></p>' +
        Array.from({ length: nSlots }, (_, k)=> '<div class="dsc-slot' + (nSlots > 1 ? ' s' + (k + 1) : '') + '"><svg class="dsc-dash" width="' + sw + '" height="' + sh + '" viewBox="0 0 ' + sw + ' ' + sh + '" aria-hidden="true"><rect x="1" y="1" width="' + (sw - 2) + '" height="' + (sh - 2) + '" rx="7" ry="7"/></svg><span class="dsc-mark"></span></div>').join("") +   // [t4-scene] data.slots of them (T2 / T3: one)
        opts.map((_, k)=> '<div class="dsc-tile t' + (k + 1) + '"><span class="dsc-tshade"></span><div class="dsc-base"></div><div class="dsc-face"></div><p class="dsc-sym"></p></div>').join(""));
      const card = host.closest(".tut-card"); if(card){ card.classList.add("sfig-round", "sfig-scene"); if(d.variant) card.classList.add("dsc-v-" + d.variant); }   // [t3-scene] the variant's geometry by CSS
      const sentEl = fig.querySelector(".dsc-sent"), slots = Array.from(fig.querySelectorAll(".dsc-slot")), marks = slots.map(sl=> sl.querySelector(".dsc-mark")),
            girl = fig.querySelector(".dsc-girl"), tiles = Array.from(fig.querySelectorAll(".dsc-tile")), bubble = fig.querySelector(".dsc-bubble");
      marks.forEach(mk=>{ mk.textContent = d.mark || ""; });
      tiles.forEach((t, k)=>{ t.querySelector(".dsc-sym").textContent = opts[k].mark || ""; });
      const pick = Math.max(0, opts.findIndex(o=> o.mark === d.mark));
      const beat = !!d.pic_sfx || d.girl_pop !== false;   // [t3-girl] stage 3 (the sound + the girl's pop) only where the page has it: T3's girl stands still
      const picking = slide.type === "PUNCT_PICK";   // [g1-scene] G1: the tiles are the child's as they pop in, with the pick page's feedback
      const L = sfigLine(sentEl, S.text_hi, S.word_times, S.audio, S.word_end);
      (S.gaps || []).forEach(i=>{ if(L.words[i]) L.words[i].classList.add("dsc-gap"); });   // [t4-scene] the words the slots follow: their gap's width is the variant's CSS
      // [t3-look] the glance (data.girl_look, on the rig): the amounts and the cycle as CSS variables on the girl; .look starts the
      // cycle (dscLookEye / dscLookLean / dscLookArm, every_ms long, the gesture over its first active_ms, then at rest); lookOff
      // (the tap) takes the class off only in a rest phase of the cycle — read from the running animation's own clock
      const look = d.girl_rig && d.girl_look; let lookT0 = -1;
      if(look){ const v = (k, val)=> girl.style.setProperty(k, val);
        v("--look-ms", (look.every_ms || 5000) + "ms"); v("--look-gx", (look.gx || 0) + "px"); v("--look-gy", (look.gy || 0) + "px");
        v("--look-arm", (look.arm_deg || 0) + "deg"); v("--look-lean", (look.lean_deg || 0) + "deg"); }
      const lookOn = ()=>{ if(!look || lookT0 >= 0) return; girl.classList.add("look"); lookT0 = performance.now(); };
      const lookOff = ()=>{ if(lookT0 < 0) return; const every = look.every_ms || 5000, active = look.active_ms || 2300;
        let ph = (performance.now() - lookT0) % every; lookT0 = -1;
        try{ const a = girl.getAnimations({ subtree:true }).find(x => x.animationName === (look.anim || "dscLookArm")); if(a && a.currentTime != null) ph = a.currentTime % every; }catch(e){}   // [t4-basket] T4's clock: dscBasketLift
        after(ph < active ? active - ph + 40 : 0, ()=> girl.classList.remove("look")); };

      state.ownsAudio = true; state.demoRunning = true; setNavActive(false);
      $("navBtn").style.display = "none";   // the page advances itself
      setSwMood("talk");
      const alive = ()=> fig.isConnected;
      const after = (ms, fn)=> setTimeout(()=>{ if(alive()) fn(); }, ms);
      const popSoft = ()=> _tone([720], "sine", 0.10, 0.07);   // [recap-sfx] T1's text pop (the reference's sfxPopSoft)
      // the user's two sounds, fetched now (heard seconds later): the school after the sentence, the pop with EACH tile — one
      // Audio per tile ([t2-scene3]): playKitSfx restarts a shared element, which would cut each pop's tail as the next tile comes
      const kit = (name, file)=>{ if(file && !_kitSfx[name]){ const a = _kitSfx[name] = new Audio("assets/Audio/" + file); a.preload = "auto"; } };
      kit("scenePic", d.pic_sfx); tiles.forEach((_, k)=> kit("scenePop" + k, d.tiles_sfx)); kit("sceneBox", d.box_sfx);   // [t3-scene] the bubble's pop
      kit("sceneGrow", G && G.sfx);   // [g3-grow] the plants' sound
      // the tiles' pops: the kit's play (held as an effect by [tap-lock]'s sfxBusy) — in the pick ([g1-scene]) played UNTRACKED: they
      // are the tiles' entrance, not feedback, and a tile tapped as it pops in answers at once (the buzz, the chime, the lines and
      // the sounds of the other pages still hold the taps)
      const popTile = (k)=>{ if(!picking){ playKitSfx("scenePop" + k, d.tiles_sfx, .8); return; }
        const a = _kitSfx["scenePop" + k]; if(!a) return; try{ a.volume = .8; a.currentTime = 0; const pr = a.play(); if(pr && pr.catch) pr.catch(()=>{}); }catch(e){} };
      // a clip with nothing to light (T1's say): it sounds, then onEnd; a watchdog stops a stalled clip
      const say = (src, onEnd)=>{
        if(!src){ onEnd(); return; }
        let done = false; const end = ()=>{ if(done || !alive()) return; done = true; onEnd(); };
        play(src, end);
        setTimeout(()=>{ if(!done && alive()){ stopAudio(); end(); } }, authoredVoHoldMs(src) + 10000);
      };
      // one cue (seconds on the clip's own clock) on the clip `file` (T1's cueOn): waits for it to sound, then onCue as the cue is
      // reached — or when the clip is gone before it, so nothing is skipped
      const cueOn = (file, cue, onCue)=>{
        let fired = false; const t0 = Date.now();
        const fire = ()=>{ if(fired) return; fired = true; onCue(); };
        const own = (a)=> !!a && decodeURIComponent(String(a.currentSrc || a.src || "").split("/").pop()) === file;
        const wait = ()=>{ if(!alive() || fired) return;
          const a = currentAudio;
          if(!own(a)){ if(Date.now() - t0 < 3000) nextFrame(wait); else fire(); return; }
          const tick = ()=>{ if(!alive() || fired) return;
            const gone = a.ended || currentAudio !== a || (a.paused && a.currentTime > 0);
            if(gone || a.currentTime + 0.04 >= cue) fire(); else nextFrame(tick); };
          tick(); };
        wait();
      };
      // the mark's INK on the slot's centre (the demos' centreInk): the danda sits right of and above its line box's centre
      function centreInk(el){
        try{
          const cs = getComputedStyle(el), c = document.createElement("canvas").getContext("2d");
          c.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
          const t = c.measureText(el.textContent);
          if(!t.width || !isFinite(t.fontBoundingBoxAscent)) return;
          const base = (el.offsetHeight - t.fontBoundingBoxAscent - t.fontBoundingBoxDescent) / 2 + t.fontBoundingBoxAscent;
          const ix = (t.actualBoundingBoxRight - t.actualBoundingBoxLeft) / 2 - el.offsetWidth / 2;
          const iy = base + (t.actualBoundingBoxDescent - t.actualBoundingBoxAscent) / 2 - el.offsetHeight / 2;
          el.style.setProperty("--ix", ix.toFixed(2) + "px"); el.style.setProperty("--iy", iy.toFixed(2) + "px");
        }catch(e){}
      }
      // 2. the sentence rises in whole and the slot pops in — inside the speech bubble popping in, where the page has one ([t3-scene]) —
      //    with T1's pop, or the page's own box sound (data.box_sfx); the clip 0.45 s after the rise, each word lit
      const stage2 = ()=>{
        if(bubble) bubble.classList.add("in");
        slots.forEach(sl=> sl.classList.add("in")); if(d.box_sfx) playKitSfx("sceneBox", d.box_sfx, .8); else popSoft();
        sfigNarrate(L, alive, ()=> after(300, beat ? stage3 : stage4)); };
      // 3. the school sound for pic_sfx_ms, faded out over its last 0.4 s; the girl's small pop (dscPop) as it starts
      const stage3 = ()=>{
        const ms = d.pic_sfx_ms || 2000, FADE = 400;
        girl.classList.remove("pop"); void girl.offsetWidth; girl.classList.add("pop");
        if(d.pic_sfx){
          playKitSfx("scenePic", d.pic_sfx, .5);
          const t0 = performance.now() + ms - FADE;
          const step = ()=>{ const a = _kitSfx.scenePic; if(!a) return;
            if(!alive()){ a.pause(); a.dispatchEvent(new Event("ended")); return; }
            const k = Math.max(0, Math.min(1, (performance.now() - t0) / FADE)); a.volume = .5 * (1 - k);
            if(k < 1) nextFrame(step); else { a.pause(); a.currentTime = 0; a.dispatchEvent(new Event("ended")); } };   // "ended": the engine's sfx hold ([tap-lock] sfxTrack) ends with it
          nextFrame(step);
        }
        after(ms, ()=> after(300, stage4));
      };
      // 4. the slot blinks over blink_ms in blink_cycle_ms cycles ([t2-scene5]: 7 s of slow 1.75 s cycles = four fades of the whole
      //    box in its orange look; the CSS gets the cycle and the count) — and the tiles pop in ONE BY ONE as it starts, tiles_gap_ms
      //    apart, each with its own pop in the frame its pop (dscTileIn) begins
      const stage4 = ()=>{
        const ms = d.blink_ms || 2000, n = Math.max(1, Math.round(ms / (d.blink_cycle_ms || 667))), gap = d.tiles_gap_ms || 350;
        slots.forEach(sl=>{ sl.style.setProperty("--blink-ms", (ms / n) + "ms"); sl.style.setProperty("--blink-n", n); sl.classList.add("blink"); });
        tiles.forEach((t, k)=>{
          const go = ()=>{ t.classList.add("in"); if(d.tiles_sfx) popTile(k); if(!k) lookOn(); if(picking) armTile(k); };   // [t3-look] the girl looks as the first tile pops; [g1-scene] the tile the child's as it pops
          if(k) after(k * gap, go); else go();
        });
        after(ms, ()=>{ slots.forEach(sl=> sl.classList.remove("blink")); if(!picking) after(300, stage5); });   // [g1-scene] the pick: no explanation, the page waits for the child
      };
      // 5. the explanation: the danda's tile lights as the clip says its cue word; after the clip the other two go dim and dead,
      //    then the lit tile pulses and is the child's
      const stage5 = ()=>{
        const src = A(X.audio), times = X.word_times || [], ci = X.cue_word != null ? X.cue_word : times.length - 1;
        const light = ()=>{ if(alive()) tiles[pick].classList.add("lit"); };
        say(src, ()=> after(300, ()=>{ light(); tiles.forEach((t, k)=>{ if(k !== pick) t.classList.add("off"); }); after(300, arm); }));
        if(src && times[ci] != null) cueOn(src.split("/").pop(), times[ci], light);
      };
      let armed = false;
      const arm = ()=>{
        armed = true; state.demoRunning = false; setSwMood("point");
        const t = tiles[pick]; t.classList.add("pulse", "live"); t.onclick = tap;
      };
      // the 🔊 chip: ignored while the page drives itself (state.demoRunning); once the tile is the child's it reads the sentence again
      state.replayAudio = ()=>{ if(!armed || isPlaying || !alive()) return; sfigNarrate(L, alive, ()=>{}); };
      // 6. the tap: the border green, the kit's correct sound, the mark lands in the slot, the slot's box goes, the page moves on
      function tap(){
        if(!armed || !alive()) return;
        armed = false; state.locked = true; state.demoRunning = true;
        if(isPlaying) stopAudio();
        lookOff();   // [t3-look] no new glance after the answer; a running one finishes its move first
        const t = tiles[pick]; t.onclick = null; t.classList.remove("pulse", "live"); t.classList.add("done");
        sfxCorrect(); setSwMood("happy");
        const stg = d.mark_stagger_ms || 0;   // [t4-scene] the marks land in turn (one slot: at once, as before)
        // [t4-scene] T4 ends the tutorial: the gate into the guided round follows it EVERY time it ends, as it did after the
        // [demo-fig] page — the engine opens each round's gate once per load, so the round is cleared first (a re-run from the
        // dev nav's list crosses it again); T2 / T3 end inside the tutorial round, where this does nothing
        const finish = ()=>{ const nx = CARD.slides[state.idx + 1], nr = nx && PHASE_ROUND[nx.phase];
          if(nr && nr !== PHASE_ROUND[slide.phase]) _gatedPhases.delete(nr);
          completeSlide(true); };
        slots.forEach((sl, k)=>{
          const land = ()=>{ centreInk(marks[k]); marks[k].classList.add("in"); after(450, ()=>{ sl.classList.add("gone"); if(k === slots.length - 1) after(1200, finish); }); };
          if(k) after(k * stg, land); else land();
        });
      }
      // [g1-scene] the pick (type PUNCT_PICK): each tile is the child's from the frame it pops in (armTile); the feedback is the pick
      // page's own, as before on G1 — a wrong tile wiggles (the engine's wgNo) with the kit's wrong buzz and the deck's hint ladder
      // (hint 1, hint 2, 0.5 s after the wiggle; the 3rd wrong tap, [hand-quiet]: the pointing hand under the right tile, the other
      // two dead and dim, no line, nothing spoken again); the right one presses (dmfTap, its colours kept), its mark lands in the
      // slot in that frame (several slots: data.mark_stagger_ms apart) with the kit's correct sound, the confetti and the happy
      // Swiftie, "शाबाश!" (data.ok_audio) sounds and PACE.tail later the page moves on (after the hand: no line, 1.7 s). [tap-lock]:
      // no tile answers while a feedback sound or line plays; the 🔊 chip says the instruction line again (state.replayAudio; the
      // sentence and its word light play ONCE on this page — [g1-quiet]; the engine's idle reminder is off here: data.no_idle_vo)
      // — a tap cuts that line short and answers at once
      let live = false, fbAudio = null, hintHand = null;
      const placeHintHand = ()=>{ if(!hintHand || !hintHand.parentNode) return; const st = document.querySelector(".slide-stage"), r = tiles[pick].getBoundingClientRect(), sw = st.getBoundingClientRect();
        const scale = sw.width / st.offsetWidth || 1; hintHand.style.left = ((r.left - sw.left) / scale + r.width / scale / 2 - 48) + "px"; hintHand.style.top = Math.min((r.bottom - sw.top) / scale + 4, st.offsetHeight - 96) + "px"; };
      const showHand = ()=>{ if(hintHand) return; const st = document.querySelector(".slide-stage"); if(!st) return;
        hintHand = document.createElement("img"); hintHand.className = "reveal-hand dmf-hand"; hintHand.src = "assets/UI/nudge_hand_new.svg"; hintHand.alt = "";
        st.appendChild(hintHand); placeHintHand(); requestAnimationFrame(placeHintHand); };
      const hintLadder = (n)=>{
        if(n >= 3){ showHand(); tiles.forEach((t, k)=>{ if(k !== pick){ t.onclick = null; t.classList.remove("live"); t.classList.add("off"); } }); return; }   // the wiggle just started runs out on its own
        const id = n <= 1 ? d.hint1_audio : d.hint2_audio;
        after(500, ()=>{ if(!live || isPlaying) return; if(id){ play(A(id), ()=>{}); fbAudio = currentAudio; } });   // a hint line is feedback: no tile answers while it speaks
      };
      function armTile(k){
        if(!live){ live = true; state.demoRunning = false; setSwMood("point");
          // [g1-quiet] the 🔊 chip: the instruction line (data.intro_audio) again — NOT the sentence: its clip and its word light play
          // once on this page (asked twice: "the VO and the highlight animation of the sentence should not repeat"); the engine's
          // idle reminder, which would call this too, is off here (data.no_idle_vo)
          state.replayAudio = ()=>{ if(!live || isPlaying || sfxBusy() || hintHand || !alive()) return; say(A(d.intro_audio), ()=>{}); }; }
        const t = tiles[k]; t.classList.add("live"); t.onclick = ()=> pickTap(k);
        t.onanimationend = (e)=>{ if(e.target === t && e.animationName === "wgNo") t.classList.remove("wiggle"); };
      }
      function pickTap(k){
        if(!live || !alive()) return;
        if(sfxBusy() || (isPlaying && currentAudio && currentAudio === fbAudio)) return;   // [tap-lock]
        if(isPlaying) stopAudio();   // the re-read is no feedback: a tap cuts it short and answers at once
        L.words.forEach(w=> w.classList.remove("hot"));
        const t = tiles[k], ok = k === pick, opt = opts[k] || {};
        GameBus.sendQuestionAnswered(slide, { is_correct: ok, score: ok && state.attempts === 0 ? 1 : 0, attempt: state.attempts + 1,
          ui_index: k, original_index: k, text: opt.name_hi || opt.mark || null });
        if(!ok){
          state.attempts++; sfxWrongSoft(); setSwMood("tryagain");
          GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
          t.classList.remove("wiggle"); void t.offsetWidth; t.classList.add("wiggle");
          hintLadder(state.attempts);
          return;
        }
        live = false; state.locked = true; state.demoRunning = true; const guided = !!hintHand; if(hintHand){ hintHand.remove(); hintHand = null; }   // the hand goes with the answer
        lookOff();   // [t3-look] (no rig on G1; kept for a rigged girl)
        slots.forEach(sl=> sl.classList.remove("blink"));
        tiles.forEach((x, j)=>{ x.onclick = null; x.classList.remove("wiggle", "live"); if(j === pick) x.classList.add("on"); });   // only the tapped tile answers: the other two stay as they are
        const stg = d.mark_stagger_ms || 300;
        marks.forEach((m, j)=>{ const land = ()=>{ centreInk(m); m.classList.add("in"); }; if(j) after(j * stg, land); else land(); });
        sfxCorrect(); confettiCannon(); setSwMood("happy");
        GameBus.emit("punct_build_done", { slide_id: slide.id, phase: slide.phase, value: true,
          first_try: state.attempts === 0, wrong: state.attempts, latency_ms: Date.now() - state.slideStart });
        if(guided){ after(1700 + (marks.length - 1) * stg, ()=> completeSlide(true)); return; }   // after the hand: no praise line
        say(A(d.ok_audio || d.mark_audio), ()=> after(PACE.tail, ()=> completeSlide(true)));   // "शाबाश!", then the page moves on
      }
      // 1. the intro line over the picture alone (the standing Swiftie and the chip with it); the sentence 0.5 s after it — or, with
      //    no intro line ([t3-scene] T3), the scene alone for data.open_ms (1 s) before the bubble pops
      let introDone = false;
      const opening = ()=> say(A(d.intro_audio), ()=>{ if(introDone) return; introDone = true; after(d.open_ms || 500, stage2); });
      // [g3-grow] the page opens on the garden without its plants: once the garden and the plants are decoded, and no sooner than
      // data.grow.start_ms (past the page's slide-in), they GROW out of their soil one after another (the CSS: .grow) to the user's
      // sound in that frame, the girl's eyes going to them data.grow.look_ms in (her glance, data.girl_look, every 7 s from then)
      // and back; data.grow.then_ms after the growth began the page goes on exactly as before (the instruction line, the sentence,
      // the tiles). A garden that never decodes holds nothing up for more than 5 s.
      if(G){
        const pics = [fig.querySelector(".dsc-bg > img")].concat(Array.from(fig.querySelectorAll(".dsc-plant img")));
        const decoded = Promise.all(pics.map(im=> (im && im.decode) ? im.decode().catch(()=>{}) : Promise.resolve()));
        const wait = (ms)=> new Promise(r=> setTimeout(r, ms));
        Promise.race([Promise.all([decoded, wait(G.start_ms || 600)]), wait(5000)]).then(()=>{
          if(!alive()) return;
          fig.querySelector(".dsc-plants").classList.add("grow");
          if(G.sfx) playKitSfx("sceneGrow", G.sfx, G.sfx_vol == null ? .9 : G.sfx_vol);
          after(G.look_ms || 0, lookOn);
          after(G.then_ms || 2700, opening);
        });
      } else opening();
      // [t3-look7] the first glance's GPU work done ahead: on a cold browser the first frame that draws the masked layers TILTED
      // compiles the GPU's shaders (measured: an 83-117 ms frame as the arm began to lift, in 6 of 6 fresh browsers; with this, 33-62 ms). The rig's
      // layers are composited from mount (style.css: will-change), and here, in the still moment after the page's slide-in and
      // before the bubble (560 ms in, open_ms 1 s), .warm tilts them by a thousandth of a degree / px for 150 ms — at most 4 levels
      // on her pixels, measured — once her bitmap is drawn; later (her bitmap still loading), as soon as it is, if the glance has
      // not begun
      if(look){ const body = girl.querySelector(".dsc-gbody, .dsc-bbody, :scope > img");   // [t4-basket] T4's body window too; [g3-grow] G3's one image, warmed at 0.38 s (data.girl_look.warm_ms: before its growth and its first glance)
        const warm = ()=>{ if(girl.classList.contains("look")) return; girl.classList.add("warm"); after(150, ()=> girl.classList.remove("warm")); };
        after(look.warm_ms || 560, ()=>{ if(!body || (body.complete && body.naturalWidth > 0)) warm(); else body.addEventListener("load", ()=>{ if(alive()) warm(); }, { once:true }); }); }
    }
  },

"""
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
js = sub1(js, r"^  /\* ===== \[demo-fig\] PUNCT_DEMO ", lambda m: scene_mod + m.group(0), re.M, "PUNCT_DEMO anchor (scene)")   # [t2-scene] in front of the demo module (the [vo-rec] patch below anchors on what follows it)
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
          lambda m: m.group(0) + "\nSlideModules.PUNCT_PICK            = { mount(host, slide){ return ((slide.data || {}).scene ? SlideModules.PUNCT_SCENE : SlideModules.PUNCT_DEMO).mount(host, slide); } };   // [pick-fig] the run-on demo's page with the tap left to the child (no page now); [g1-scene] G1, [g2-scene] G2 and [g3-scene] G3 (data.scene): the scene module's page, its tiles the child's", re.M, "alias block (pick)")
js = sub1(js, r'  SEQUENCE_DRAG: "drag",',
          lambda m: m.group(0) + '\n  EVIDENCE_QA: "mcq", BUILD_PUNCT: "build", SORT_QTYPE: "drag", SORT_WORDS: "drag", PUNCT_PICK: "mcq", SENT_PICK: "mcq",   /* [reskin] this lesson\'s answerable types */', 0, "QUESTION_FORMAT")
# [sent-fig] G4, P1 + P2 (SENT_PICK) repeat their instruction after every 5 s of quiet itself (the reference P4's rule), so the engine's
# one-off 7 s idle reminder stays off there; and the stage carries .sent-page for P4's look (style.css [sent-fig])
js = sub1(js, r"if\(\['MATCH_THE_PAIR','MATCH_VACHAN_PAIRS','FILL_VACHAN_DRAG'\]\.includes\(",
          "if((CARD.slides[state.idx]?.data || {}).no_idle_vo || ['MATCH_THE_PAIR','MATCH_VACHAN_PAIRS','FILL_VACHAN_DRAG','SENT_PICK','LETTER_STORY','STAMP_DEMO'].includes(", 0, "armIdleVo exclusions (sent, letter, stamp)")   # [letter-fig] no idle reminder on the story page; [g1-quiet] nor on a page whose data says no_idle_vo (G1: its sentence is read once)
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
   .story-caption, read as computed in Chrome): white, 26 px corners, the shadow below. [poem-box2] (2026-10-31) ONE size for all
   four beats (the user: no re-sizing between them) and more white above and below the line: 566 x 94 stage px = the longest
   sentence's ink (beat 1, 502 x 30) with 32 px of white on every side; placed midway between the picture frame's bottom (frame 241)
   and आगे's top (frame 410.6): the box's centre is the sentences' ink centre, 4.5 frame px above their line box's centre (the
   matras rise above the headline). Stage px, divided by --fig-s like the shadow. Was (10-31 [poem-box]) the beat's sentence + 2 x 25
   wide and 59.12 tall, re-fitted at each turn; before that Figma's node 436:412: 436x119 at 314,250, 20 px corners */
.sfig-textbox{position:absolute;left:532px;top:326.12px;width:calc(566px / var(--fig-s));height:calc(94px / var(--fig-s));
  transform:translate(-50%,-50%);background:#FFFFFF;border-radius:calc(26px / var(--fig-s));
  box-shadow:0 calc(5px / var(--fig-s)) 0 rgba(11,42,90,.10),0 calc(10px / var(--fig-s)) calc(26px / var(--fig-s)) rgba(11,42,90,.12);}
/* [textbox-shadow] (2026-10-30) the shadow is the reference story's (hind-dear-story.vercel.app, Page 1 S01): its white sentence box
   (.stage.tut.l02-story .mr-read .mr-caption) casts a crisp 5 px navy lip and a soft 10 / 26 px navy glow under it, the same on every
   frame of the page; its stage px, divided by --fig-s so that .sfig-in's scale puts them on screen at exactly 5 / 10 / 26 px
   (was Figma's 0 4px 19.7px rgba(177,177,177,.25)) */
/* [poem-box] the caption's type: Baloo 2 declared 600 (only the 700 and 800 faces are embedded — the reference's own files,
   byte for byte — so it renders in the 700 face, as there), 29 px on a 37.12 px line (1.28), 0.2em word spacing of its 28 px
   box = 5.6 px; one line, every beat on one centre. [poem-box2] that centre is 22 stage px (21.125 frame px) below the 10-31 one
   (309.5, the old box's), so the ink lands on the new box's centre and the glyphs keep the same pixel phase (a half-pixel y renders
   them softer). The colour stays this page's #002F76. Was 'Story Baloo 2' 800, 26 px (beat 1) / 28 px, line-height normal.
   [t0-font] (2026-11-01) the user: "increase the size of the font a little, keep the text in the centre of the white box" — 31 px
   (was 29), line and word spacing scaled with it (39.68 = 1.28 x 31; 6 px), the box untouched. The ink's centre is now 5.0 stage px
   (4.81 frame px) above the line box's centre, so the line box sits that much below the box's centre (326.12): top 330.93. Chrome
   snaps these glyphs to whole frame px, so any top from 330.5 to 331.25 renders the same pixels (30 px of white above and below
   beats 2 and 4); 330.93 is mid-step. The longest sentence (beat 1) is 537 px of ink in the 566 px box (14 / 15 px either side) */
.sfig-text{position:absolute;left:532px;top:330.93px;transform:translate(-50%,-50%);white-space:nowrap;width:max-content;
  font-family:var(--font-hi);font-weight:600;font-size:calc(31px / var(--fig-s));line-height:calc(39.68px / var(--fig-s));
  word-spacing:calc(6px / var(--fig-s));color:#002F76;text-align:center;}
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
/* [t0b-fig] (2026-11-01) frame 704:2: node 704:183 is 574x283 at 257,54 of the card (245,42 here) — centred on 532 — with its
   4px stroke drawn OUTSIDE it (its render is 582x291 at 349,156 frame px) and 20px corners, i.e. 24px on the stroke's outer
   edge. Was node 488:371 / 654:748: 683x219 at 191,144 (187,140 691x227 with the stroke) */
.sfig-sbox{position:absolute;left:241px;top:38px;width:582px;height:291px;background:#FFFFFF;border:4px solid #DADADA;
  border-radius:24px;opacity:0;transform:scale(.9);}
/* [t0b-fig] the frame's second grid tile (node 704:181) sits 2 px left of 488:369's: 529.969 (card x 541.969 - 12); [recap-fig2]
   T1's frame 764:144 has it there too (node 764:323) */
.sfig-round .sfig-in:has(.sfig-sbox) .sfig-grid.g2, .sfig-recap .sfig-grid.g2{left:calc(529.969px - 112px / var(--fig-s) + 108px);}
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
/* [t0b-fig] (2026-11-01) frame 704:2: the two sentence nodes are centred in the box — 704:184 on 287,70 and 704:185 on 287,213
   of it (532,112 and 532,255 here), 50px, line-height normal — set in page 1 T0's type (.sfig-text: Baloo 2 declared 600, which
   renders the embedded 700 face, #002F76) at the frame's size; one line each, centred on the node's centre. Was frame 654:567's
   30px 'Story Baloo 2' 800, 401 / 390 wide on 540.5,204.5 / 540,302.5 */
.sfig-stext.sfig-lines{display:block;left:0;top:0;width:auto;height:auto;}
.sfig-stext.sfig-lines p{position:absolute;margin:0;transform:translate(-50%,-50%);white-space:nowrap;width:max-content;
  font-family:var(--font-hi);font-weight:600;font-size:50px;line-height:normal;}
.sfig-stext.sfig-lines p.l1{left:532px;top:112px;}   /* node 704:184 */
.sfig-stext.sfig-lines p.l2{left:532px;top:255px;}   /* node 704:185 */
.sfig-sent{display:inline-block;padding:2px 14px;margin:-2px -14px;border-radius:12px;
  transition:background-color .35s ease-out,transform .45s cubic-bezier(.2,.9,.3,1.2);}
.sfig-sent.hl{background:#FFF1B6;transform:scale(1.06);}
.sfig-mk{display:inline-block;transition:color .3s ease-out,transform .45s cubic-bezier(.2,.9,.3,1.3);}
.sfig-mk.on{color:#E86A00;transform:scale(1.4);}
"""
recap_css = """
/* ===== [recap-fig] T1 (MARKS_RECAP) — [recap-fig2] (2026-11-01) laid out as frame 764:144 "html_Guided_instructions": T0B's card,
   grid (its second tile at 764:323's x, as 704:2's), Swiftie and 🔊 chip (the frame's own Swiftie, 245 px at 35,415, is not used:
   T0's stay, as asked), and the frame's own content in .sfig-in's px (= the frame's card px - 12, its border): the sign's white
   box, the name beside it, the sentence's white box under them (T0's shadow, the frame's size) and the picture at the right.
   No title. आगे at T0's place (the engine's rule for these cards; the three-row page had moved it under the card). Was frame
   508:2: the title and three rows (sign box, name, use, yellow example box) in Noto / Baloo Bhai 2 metrics. ===== */
.rcf-row{position:absolute;left:0;top:0;width:1064px;height:484px;pointer-events:none;}
/* the sign's box: node 764:326, 175x169.355 at 199,65 (card px) with its 4px stroke drawn OUTSIDE (the render: 195..378 x 61..238.4)
   and 10px corners, i.e. 14px on the stroke's outer edge; it pops in with the name */
.rcf-sign{position:absolute;left:183px;top:49px;width:183px;height:177.355px;background:#FFFFFF;border:4px solid #DADADA;
  border-radius:14px;opacity:0;transform:scale(.9);}
.rcf-sign.in, .rcf-ebox.in{animation:sfigBoxIn .5s cubic-bezier(.2,.9,.3,1.2) both;}   /* pops in as its text rises */
/* the sign: node 764:329 "। " (a trailing space), Baloo 2 SemiBold 128px — here the family's 600 (the embedded 700 face, as T0's
   text); placed by INK: the render's danda is 16x84 centred on 286,144 of the card = 87,79 of the box's padding box. It lights as
   a word does (.sfig-w.hot: the orange + p2WordPop) while the name's clip says the name */
.rcf-mark{position:absolute;left:87.5px;top:85.5px;transform:translate(-50%,-50%);}   /* the line box 0.5 right / 6.5 lower: the 700 face's danda sits high in it (measured in Chrome) */
.rcf-mark p{margin:0;font-family:var(--font-hi);font-weight:600;font-size:128px;line-height:normal;color:#002F76;white-space:pre;}
/* the name: node 764:334, Baloo 2 ExtraBold 64px #012F76, 1075 wide centred on x 580.5, top 98 (card px); its ink in the render
   253x80 centred on 580.5,148 -> 568.5,136 here. The sentence: node 764:340 " पिंकी स्कूल गई ।" (its leading space counted),
   ExtraBold 40px, centred on x 487.5, top 289; its ink 249x51 centred on 488.5,319.5 -> 476.5,307.5 here (3.5 px below its box's
   centre, as the frame has it). Both centred by transform, so the rise ([word-sync], on the p's own translate / scale) keeps it */
.rcf-name, .rcf-eg{position:absolute;transform:translate(-50%,-50%);width:max-content;white-space:nowrap;
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;color:#012F76;text-align:center;}
.rcf-name{left:569.5px;top:141px;font-size:64px;line-height:normal;}      /* line boxes centred where Chrome's ink lands on the render's (measured): */
.rcf-eg{left:480px;top:310.5px;font-size:40px;line-height:normal;}        /* the name 1 / 5 px, the sentence 3.5 / 3 px past the ink targets above */
.rcf-name p, .rcf-eg p{margin:0;}
/* the sentence's white box: node 764:752, 578x84 at 199,274 (card px), 20px corners, no stroke; the frame's shadow (0 4 19.7
   rgba(177,177,177,.25)) replaced by page 1 T0's ([textbox-shadow]: a 5 px lip + a 10 / 26 px glow, stage px / --fig-s), as asked */
.rcf-ebox{position:absolute;left:187px;top:262px;width:578px;height:84px;background:#FFFFFF;border-radius:20px;opacity:0;transform:scale(.9);
  box-shadow:0 calc(5px / var(--fig-s)) 0 rgba(11,42,90,.10),0 calc(10px / var(--fig-s)) calc(26px / var(--fig-s)) rgba(11,42,90,.12);}
/* the picture: node 764:753, 176x264 at 835,91 (card px) with the frame's 0 2 2 rgba(0,0,0,.25) drop shadow; it pops in as the
   example's clip reaches the sentence's first word. [recap-sfx] (2026-11-01) the way the horse comes in on the reference
   hi02h11l02s04-file5's page 2 (.mb-v2 .mb-pic, read as computed): waiting at opacity 0 / scale .82, then a TRANSITION —
   opacity .4s ease, transform .45s cubic-bezier(.34,1.4,.6,1), i.e. up through 1.009 and back (was rcfPicIn, .7 -> 1 in .5 s) */
.rcf-pic{position:absolute;left:823px;top:79px;width:176px;height:264px;opacity:0;transform:scale(.82);
  transition:opacity .4s ease,transform .45s cubic-bezier(.34,1.4,.6,1);filter:drop-shadow(0 2px 2px rgba(0,0,0,.25));}
.rcf-pic img{display:block;width:100%;height:100%;}
.rcf-pic.in{opacity:1;transform:none;}
/* the mark at the sentence's end keeps the words' orange once its clip has lit it ([recap-alp]: or a mark ending a word, .rcf-mk) */
.rcf-eg .sfig-w.keep, .rcf-eg .rcf-mk.keep{color:#E86A00;}
/* [recap-alp] (2026-11-01) T1B, the अल्प विराम page = frame 764:755 (variant "alp"), T1's design with the frame's own placements (card
   px - 12, as above): the sign's box 764:937 175x169.355 at 209,65 (stroke OUTSIDE: 193,49 here) and the sentence's box 764:940
   578x84 at 209,274 — both 10 px right of T1's; the ",", the name and the sentence by their INK in the frame's render (centres, card
   px: the comma 294.5,157.5 = 85.5,92.5 of its box's padding box; अल्प विराम 592.5,139; आम, केला, संतरा और सेब 498.5,311) with the
   line boxes placed where Chrome's ink lands on them (measured, as T1's); the picture 524:350 219x146 at 816,143 — the frame's
   bitmap is T4's img_demo3_fruits (the same image) — with no shadow (the node has none; T1's girl has one) */
.rcf-v-alp .rcf-sign{left:193px;}
.rcf-v-alp .rcf-mark{left:88px;top:61px;}            /* the comma's line box: its ink sits 31.5 px below the box's centre */
.rcf-v-alp .rcf-name{left:579px;top:141px;}
.rcf-v-alp .rcf-ebox{left:197px;}
.rcf-v-alp .rcf-eg{left:485.5px;top:306px;}
.rcf-v-alp .rcf-pic{left:804px;top:131px;width:219px;height:146px;filter:none;}
/* [recap-prashn] (2026-11-01) T1C, the प्रश्नवाचक चिह्न page = frame 764:945 (variant "prashn"), T1's design with the frame's own
   placements (card px - 12): the sign's box 764:1127 at 199,65 (T1's place) and the sentence's box 764:1129 at 199,274, 580 wide (2
   px wider than T1's); the "?", the name and the sentence by their INK in the frame's render (centres, card px: the ? 286.5,145.5;
   प्रश्नवाचक चिह्न 592.5,145; तुम्हारा घर कहाँ है ? 486.5,314.5) with the line boxes placed where Chrome's ink lands on them
   (measured, as T1's); the picture 766:1140 216x144 at 822,168 with the node's 0 2 2 rgba(0,0,0,.25) shadow (T1's girl's). The
   frame sets both its ?s in Noto Sans Devanagari (the sign SemiBold 128 px, the sentence's ExtraBold 40 px) where the rest is
   Baloo 2: 'Story Noto Q' below, that face for U+003F alone, the weight from the rule (600 / 800) */
.rcf-v-prashn .rcf-mark{left:88.5px;top:92px;}
.rcf-v-prashn .rcf-mark p{font-family:'Story Noto Q',var(--font-hi);}
.rcf-v-prashn .rcf-name{left:581px;top:141px;}
.rcf-v-prashn .rcf-ebox{width:580px;}
.rcf-v-prashn .rcf-eg{left:477px;top:305.5px;font-family:'Story Noto Q','Story Baloo 2',var(--font-hi);}
.rcf-v-prashn .rcf-pic{left:810px;top:156px;width:216px;height:144px;}
"""
# [recap-prashn] the frame's "?" face: Google Fonts' subset of Noto Sans Devanagari for "?" alone (variable wght 100-900, 1.5 KB, OFL;
# recap_assets/recap_font_noto_q.woff2), inlined so it is there the moment the sign shows; unicode-range keeps every other character
# on the rule's next family. Its line metrics (896 / -408, USE_TYPO) are 'Story Baloo 2''s overrides, so no line box changes
recap_css += ("@font-face{font-family:'Story Noto Q';font-style:normal;font-weight:100 900;font-display:block;unicode-range:U+3F;"
              "src:url(data:font/woff2;base64," + base64.b64encode((SCR / "recap_assets" / "recap_font_noto_q.woff2").read_bytes()).decode()
              + ") format(\"woff2\");}\n")
scene_css = """
/* ===== [t2-scene] (2026-11-01) T2, the first example page (frame 706:188 "2 T0B", PUNCT_SCENE), on T0B / T1's card (.sfig-round,
   above: the frame's 1088x508 card at 96,106 with its 12px border and 64px corners; the standing Swiftie and the 🔊 chip where
   page 3 T1 has them — the frame's own Swiftie 706:369 is not used, as asked). Positions in .sfig-in px = card px - 12.
   The hallway picture 710:601 (its 1672x941 bitmap) 1088x613 at 0,-113 of the card, clipped to the card's padding box (its
   corners: the card's 64px less the 12px border); the sentence 704:200 "पिंकी स्कूल जा रही है" Baloo 2 ExtraBold 55px #012F76 (its
   ink in the render 432x69 centred on 793,228.5 of the page -> 685,110.5 here; the line box placed where Chrome's ink lands on
   it, measured); the slot 704:201 53x90 at 1013,187 (page), white, 8px corners, a 2px dashed rgba(86,86,86,.85) stroke inside
   (the dashes as the demos' slot draws them, 10 on 5 off); the girl 746:2534 239x358 at 264,215 (her bitmap, 1024x1536) with her
   floor shadow 746:2535 (160x36 at 307,520: #B4ABA2 at .29 x .5); the tiles 706:569 / 573 / 577: a #D9D9D9 base 117.819x116.498
   at 564.09 / 791 / 1021.818, 397 (18px corners, 0 4 4 rgba(0,0,0,.25)) under a white face 115.743x110.983 at +1.04,+1.38
   (2.386px #D5D8DF inside, 18px corners), each over a grey ellipse 711:603-606 (118x26 at y 496, #8F8F8F .6); the marks 706:572 /
   576 / 580 in the frame's Noto Sans Devanagari SemiBold 64px #002F76 ('Story Noto Marks' below: that face for "।", "," and "?"
   alone), 483-wide boxes centred on 619.5,454.5 / 849.5,439.5 / 1080.32,454.5 (page) ===== */
.dsc-bg{position:absolute;left:0;top:0;width:1064px;height:484px;overflow:hidden;border-radius:calc(64px - 12px / var(--fig-s));}
.dsc-bg > img{position:absolute;left:-12px;top:-125px;width:1088px;height:613px;}
.sfig-scene .dsc-sent{position:absolute;left:685.5px;top:115.5px;transform:translate(-50%,-50%);margin:0;width:max-content;white-space:nowrap;text-align:center;
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;font-size:55px;line-height:normal;color:#012F76;}
.dsc-slot{position:absolute;left:905px;top:69px;width:53px;height:90px;background:#FFFFFF;border-radius:8px;opacity:0;transform:scale(.9);transition:background-color .4s,box-shadow .25s;}
.dsc-slot.in{opacity:1;transform:none;animation:sfigBoxIn .5s cubic-bezier(.2,.9,.3,1.2) both;}   /* pops in as the sentence rises */
.dsc-dash{position:absolute;left:0;top:0;display:block;fill:none;stroke:rgba(86,86,86,.85);stroke-width:2;stroke-dasharray:10 5;transition:opacity .4s,stroke .25s;}
/* the blink — [t2-scene5]: the WHOLE box APPEARS and DISAPPEARS, slowly (the module's --blink-ms = data.blink_cycle_ms 1.75 s,
   --blink-n = blink_ms / that = 4). While it blinks the box wears its orange look — the fill the orange's .2 tint (#FAE1CC, an OPAQUE
   colour: an rgba fill would show the hallway through the box), the ring the words' orange, the glow the pulsing tile's
   rgba(232,106,0,.6) 5px (dscGlow's rest look) — eased in and out by the slot's own .4 / .25 s transitions, and its OPACITY fades
   1 -> 0 -> 1 over each cycle (0.56 s fades, 0.21 s unseen, 0.42 s seen), the last cycle ending seen. sfigBoxIn (the slot's pop-in)
   stays FIRST in the animation list: a list that dropped it would cancel it as the blink starts and run it again as the blink
   ends (a second pop of the box). [t2-scene4] switched the look on / off on 1.2 s cycles; [t2-scene2] held the orange for half of
   a ~0.67 s cycle, ring + glow only. */
.dsc-slot.in.blink{background-color:#FAE1CC;box-shadow:0 0 0 5px rgba(232,106,0,.6);
  animation:sfigBoxIn .5s cubic-bezier(.2,.9,.3,1.2) both,dscBlink var(--blink-ms,1750ms) ease-in-out var(--blink-n,4);}
.dsc-slot.blink .dsc-dash{stroke:#E86A00;}
@keyframes dscBlink{0%,12%,88%,100%{opacity:1;}44%,56%{opacity:0;}}
/* the mark, in the sentence's face, its INK centred on the slot (--ix / --iy measured by the module from the font) */
.dsc-slot .dsc-mark{position:absolute;left:50%;top:50%;opacity:0;--ix:0px;--iy:0px;white-space:pre;
  transform:translate(calc(-50% - var(--ix)),calc(-50% - var(--iy))) scale(.4);transform-origin:calc(50% + var(--ix)) calc(50% + var(--iy));
  font-family:'Story Baloo 2',var(--font-hi);font-weight:800;font-size:55px;line-height:normal;color:#012F76;
  transition:opacity .35s ease-out,transform .45s cubic-bezier(.2,.9,.3,1.3);}
.dsc-slot .dsc-mark.in{opacity:1;transform:translate(calc(-50% - var(--ix)),calc(-50% - var(--iy)));}
.dsc-slot.gone{background:transparent;box-shadow:none;}      /* the box goes, the mark stays */
.dsc-slot.gone .dsc-dash{opacity:0;}
/* the girl: her box where the frame has her, there from the first frame ([t2-scene2] 2026-11-01: no walk — she had come in from the
   doorway, down the steps, over 3.4 s); a small pop about her feet (her ink ends 348/358 down the box) as the school sound starts */
.dsc-girl{position:absolute;left:156px;top:97px;width:239px;height:358px;transform-origin:50% 97.2%;}
.dsc-girl > img{position:absolute;left:0;top:0;width:239px;height:358px;}
.dsc-shade{position:absolute;left:43px;top:305px;width:160px;height:36px;border-radius:50%;background:rgba(180,171,162,.145);}
.dsc-girl.pop{animation:dscPop .5s ease-out;}
@keyframes dscPop{0%,100%{transform:scale(1);}40%{transform:scale(1.045);}}
/* the tiles: [t2-scene3] each POPS in on its own (dscTileIn: from .4 of its size past 1.08 to 1 over .45 s, with the user's pop) —
   the opacity by transition and the pop with NO fill, so the dim state after is not fought by the animation's end (the [t2-scene]
   gotcha); before, all three eased in (scale .9 -> 1) 90 ms apart */
.dsc-tile{position:absolute;top:279px;width:117.819px;height:116.498px;opacity:0;transform:scale(.4);transform-origin:50% 50%;transition:opacity .22s ease-out;}
.dsc-tile.t1{left:456.09px;} .dsc-tile.t2{left:683px;} .dsc-tile.t3{left:913.818px;}
.dsc-tile.in{opacity:1;transform:none;animation:dscTileIn .45s ease-out;}
@keyframes dscTileIn{0%{transform:scale(.4);}60%{transform:scale(1.08);}100%{transform:scale(1);}}
.dsc-tshade{position:absolute;left:0;top:99px;width:118px;height:26px;border-radius:50%;background:rgba(143,143,143,.6);}
.t1 .dsc-tshade{left:-1.09px;} .t3 .dsc-tshade{top:99.498px;}
.dsc-base{position:absolute;left:0;top:0;width:117.819px;height:116.498px;background:#D9D9D9;border-radius:18px;box-shadow:0 4px 4px rgba(0,0,0,.25);}
.dsc-face{position:absolute;left:1.04px;top:1.38px;width:115.743px;height:110.983px;box-sizing:border-box;background:#FFFFFF;border:2.386px solid #D5D8DF;border-radius:18px;
  transition:border-color .25s,background-color .25s,box-shadow .25s;}
.dsc-sym{position:absolute;margin:0;width:483px;translate:-50% -50%;text-align:center;white-space:pre;pointer-events:none;   /* [tile-hit] the box is wider than the tile: the tile takes the tap */
  font-family:'Story Noto Marks',var(--font-hi);font-weight:600;font-size:64px;line-height:normal;color:#002F76;transition:color .25s;}
.t1 .dsc-sym{left:56.41px;top:56.5px;} .t2 .dsc-sym{left:58.5px;top:41px;} .t3 .dsc-sym{left:59.5px;top:56.5px;}   /* the line boxes where Chrome's ink lands on the render's (measured) */
/* lit as the explanation names the mark: the words' orange (+ G4's pop) on the mark, a 3px orange border + a solid glow on the face
   ([t2-scene2]: the glow .45 and 5px, was .22 and 6px — too faint) */
.dsc-tile.lit .dsc-face{border-color:#E86A00;border-width:3px;box-shadow:0 0 0 5px rgba(232,106,0,.45);}
.dsc-tile.lit .dsc-sym{color:#E86A00;transform-origin:50% 60%;animation:p2WordPop .28s ease-out 1;}
.dsc-tile.off{opacity:.6;filter:saturate(.7);transition:opacity .3s,filter .3s;pointer-events:none;}   /* dim and dead ([t2-scene2]: .6, not the demos' .35 — too faint) */
.dsc-tile.live{cursor:pointer;}
.dsc-tile.pulse{animation:dscPulse 1.1s ease-in-out infinite;transform-origin:50% 50%;}
.dsc-tile.pulse .dsc-face{animation:dscGlow 1.1s ease-in-out infinite;}
@keyframes dscPulse{0%,100%{transform:scale(1);}50%{transform:scale(1.06);}}
@keyframes dscGlow{0%,100%{box-shadow:0 0 0 5px rgba(232,106,0,.6);}50%{box-shadow:0 0 0 10px rgba(232,106,0,.7);}}   /* [t2-scene3] the glow a little stronger while the tile is the child's (.6 / .7, was .45 / .55) */
/* tapped: the press (the demos' dmfTap), then the BORDER green (the engine's --correct) — [t2-scene2]: the face stays white and the
   mark its blue (was the face --correct-bg with a green glow and the mark green) */
.dsc-tile.done{animation:dmfTap .45s ease-out;}
.dsc-tile.done .dsc-face{border-color:var(--correct,#00B132);border-width:3px;background:#FFFFFF;box-shadow:none;}
.dsc-tile.done .dsc-sym{color:#002F76;animation:none;}
"""
# [t2-scene] the frame's face for the tiles' marks: Google Fonts' Noto Sans Devanagari SemiBold subset for "।", "," and "?" (css2
# ?text=%3F%2C%E0%A5%A4 at wght 600: a static 0.9 KB woff2, OFL; demo1_assets/demo1_font_noto_marks.woff2), inlined as 'Story Noto
# Marks' with a unicode-range of those three, so any other character falls to the rule's next family
scene_css += ("@font-face{font-family:'Story Noto Marks';font-style:normal;font-weight:600;font-display:block;unicode-range:U+2C,U+3F,U+964;"
              "src:url(data:font/woff2;base64," + base64.b64encode((SCR / "demo1_assets" / "demo1_font_noto_marks.woff2").read_bytes()).decode()
              + ") format(\"woff2\");}\n")
# [t3-scene] T3's geometry (frame 724:2016 "7 T3"; stage px less the padding box's 108,118): the room picture 0,-4 1088x519 of the
# card; the speech bubble's group 402.995,163 639.666x122.489 — the SVG carries its shadows, 651.745x135.269 from 397.306,160.610
# (the body rect at 29.7686,2.39 inside it = the frame's 427.074,163); the sentence's box 477,180 479x88 (centre 716.5,224); the slot
# 907,174 59x100, #FFF1B6 with the same dashes; the tiles 465.09 / 692 / 922.818 at 453 with T2's shadows; the "?" and "," swap
# tiles, so their measured line boxes go with the MARK. [t3-girl] The girl is the frame's "image 272" 213,212 257x385 (105,94 of the
# padding box) with her shadow 277,558 118x37 (64,346 of her box), painted above the tiles and the bubble (z-index 1) as the frame's
# last nodes are.
scene_css += r"""
/* ===== [t3-scene] T3 = frame 724:2016 "7 T3" on the scene module: the "ask" variant (.dsc-v-ask) ===== */
.dsc-v-ask .dsc-bg > img{left:-12px;top:-16px;width:1088px;height:519px;object-fit:cover;}
.dsc-bubble{position:absolute;left:289.306px;top:42.61px;width:651.745px;height:135.269px;opacity:0;transform:scale(.5);transform-origin:1% 78%;pointer-events:none;}   /* the origin at the tail's tip */
.dsc-bubble.in{opacity:1;transform:none;animation:dscBubbleIn .5s cubic-bezier(.2,.9,.3,1.2) both;}   /* pops out of its tail as the sentence rises */
@keyframes dscBubbleIn{from{opacity:0;transform:scale(.5);}to{opacity:1;transform:none;}}
.dsc-v-ask .dsc-sent{left:608.5px;top:109px;}   /* the box's centre 716.5,224 on the stage would be top 106: Chrome's Baloo ink sat 3 px above the render's there (measured) */
.dsc-v-ask .dsc-slot{left:799px;top:56px;width:59px;height:100px;background:#FFF1B6;}
.dsc-v-ask .dsc-slot.in.blink{background-color:#FAD692;}   /* the frame's yellow warmed by the orange's .2, as the white slot's #FAE1CC */
.dsc-v-ask .dsc-slot.gone{background:transparent;}
.dsc-v-ask .dsc-tile{top:335px;} .dsc-v-ask .dsc-tile.t1{left:357.09px;} .dsc-v-ask .dsc-tile.t2{left:584px;} .dsc-v-ask .dsc-tile.t3{left:814.818px;}
.dsc-v-ask .t2 .dsc-sym{left:59.5px;top:56.5px;} .dsc-v-ask .t3 .dsc-sym{left:58.5px;top:41px;}   /* "?" on the middle tile, "," on the right one */
.dsc-v-ask .dsc-girl{left:105px;top:94px;width:257px;height:385px;z-index:1;}   /* [t3-girl] the frame's girl, above the tiles and the bubble */
.dsc-v-ask .dsc-girl > img{width:257px;height:385px;}
.dsc-v-ask .dsc-shade{left:64px;top:346px;width:118px;height:37px;background:rgba(211,160,111,.4);}   /* her own shadow, Ellipse 3767 */
"""
# [t4-scene] T4's geometry (frame 723:1575 "8 T4"; stage px less the padding box's 108,118): the park picture -102,-124 1371x654 of the
# card (mirrored in the file); the sentence centred on 640.5 (box top 147, 893 wide), its gaps after "आम" / "केला" sized so the words
# sit where the render's do (measured); the two slots 495,188 and 645,188, 37x42.606, white with T2's dashes; the tiles 494.09 / 721
# / 951.818 at 447 in T2's order (T2's mark offsets apply as they are) over opaque #FEB564 ellipses; the girl 240,257 224x336 above
# everything (the frame's last node) on her #FEB564 ellipse 257,546 190x47 (17,289 of her box)
scene_css += r"""
/* ===== [t4-scene] T4 = frame 723:1575 "8 T4" on the scene module: the "list" variant (.dsc-v-list) ===== */
.dsc-v-list .dsc-bg > img{left:-114px;top:-136px;width:1371px;height:654px;object-fit:cover;}
.dsc-v-list .dsc-sent{left:533.5px;top:76px;}   /* the box centre 532.5,73: Chrome's Baloo ink sat 1 px left and 3 px above the render's there (measured, word by word) */
.dsc-v-list .dsc-sent .dsc-gap{margin-right:__GAP__px;}   /* the frame's four-space runs where the slots sit */
.dsc-v-list .dsc-slot{top:70px;width:37px;height:42.606px;} .dsc-v-list .dsc-slot.s1{left:387px;} .dsc-v-list .dsc-slot.s2{left:537px;}
.dsc-v-list .dsc-tile{top:329px;} .dsc-v-list .dsc-tile.t1{left:386.09px;} .dsc-v-list .dsc-tile.t2{left:613px;} .dsc-v-list .dsc-tile.t3{left:843.818px;}
.dsc-v-list .dsc-tshade{background:#FEB564;}   /* the frame's tile ellipses: opaque #FEB564 on the path */
.dsc-v-list .dsc-girl{left:132px;top:139px;width:224px;height:336px;z-index:1;}
.dsc-v-list .dsc-girl > img{width:224px;height:336px;object-fit:cover;}
.dsc-v-list .dsc-shade{left:17px;top:289px;width:190px;height:47px;background:#FEB564;}   /* her ellipse, 729:2321 */
/* ===== [g1-scene] G1 = frame 715:856 "9 G1" on the scene module: the "pick" variant (.dsc-v-pick) ===== */
.dsc-v-pick .dsc-bg > img{left:-15px;top:-15px;width:1095px;height:514.872px;}   /* the room, drawn whole (the box has the bitmap's aspect) */
.dsc-v-pick .dsc-sent{left:__PSX__px;top:__PSY__px;}   /* the box's centre 634.5,113 of the padding box: Chrome's Baloo ink sat 1 px left and 1 px below the render's there (measured, word by word) */
.dsc-v-pick .dsc-slot{left:887px;top:68px;}   /* T2's 53x90 white slot, 18 px further left, 1 px higher */
.dsc-v-pick .dsc-tile.t1{left:386.09px;} .dsc-v-pick .dsc-tile.t2{left:613px;} .dsc-v-pick .dsc-tile.t3{left:843.818px;}   /* T2's row, 70 px further left (T4's columns) */
.dsc-v-pick .dsc-tshade{background:rgba(225,180,142,.6);}   /* the frame's tile ellipses: #E1B48E at .6 on the floor */
.dsc-v-pick .dsc-girl{left:121px;top:45px;width:252px;height:378px;}
.dsc-v-pick .dsc-girl > img{width:252px;height:378px;}
.dsc-v-pick .dsc-shade{left:21px;top:338px;width:158px;height:34px;background:rgba(225,180,142,.3);}   /* her ellipse 749:2547: #E1B48E .5 in a .6 node */
/* the pick's tiles ([g1-scene]): a wrong one shakes with the engine's wrong-answer wiggle (wgNo, one --fx-beat), its colours
   unchanged — dscTileIn (the tile's pop-in) stays FIRST in the animation list: a list that dropped it would run it again as the
   wiggle's class leaves (the [t2-scene5] gotcha: a second pop of the tile after every wrong tap); the right one presses (the demos'
   dmfTap) and keeps its colours — no green, no glow (the pick page's look, as before) */
.dsc-tile.in.wiggle{animation:dscTileIn .45s ease-out,wgNo var(--fx-beat) ease-in-out both;}
.dsc-tile.in.on{animation:dscTileIn .45s ease-out,dmfTap .45s ease-out;}
/* ===== [g2-scene] G2 = frame 716:1058 "10 G2" on the scene module: the "pick2" variant (.dsc-v-pick2) — G1's page with the frame's own geometry ===== */
.dsc-v-pick2 .dsc-bg > img{left:-46px;top:-17px;width:1152.714px;height:550px;}   /* the street, drawn whole (the box has the bitmap's aspect) */
.dsc-v-pick2 .dsc-sent{left:__QSX__px;top:__QSY__px;}   /* the box's centre 494.5,115 of the padding box: Chrome's Baloo ink sat 0.5 px right and 3 px above the render's there (measured, word by word) */
.dsc-v-pick2 .dsc-slot{left:683px;top:66px;width:59px;height:100px;}   /* T3's 59x100 slot, white */
.dsc-v-pick2 .dsc-tile{top:308px;} .dsc-v-pick2 .dsc-tile.t1{left:226.09px;} .dsc-v-pick2 .dsc-tile.t2{left:453px;} .dsc-v-pick2 .dsc-tile.t3{left:683.82px;}
.dsc-v-pick2 .dsc-tshade{display:none;}   /* no ellipses under the tiles in this frame */
.dsc-v-pick2 .dsc-girl{left:826px;top:109px;width:236px;height:354px;}
.dsc-v-pick2 .dsc-girl > img{width:236px;height:354px;}
.dsc-v-pick2 .dsc-shade{left:35px;top:307px;width:145px;height:38px;background:rgba(233,149,96,.41);}   /* her ellipse 750:2551: #E99560 at .41 */
/* ===== [g3-scene] G3 = frame 716:1262 "11 G3" on the scene module: the "pick3" variant (.dsc-v-pick3) — G1's page with the frame's own geometry, the slot inside the sentence ===== */
.dsc-v-pick3 .dsc-bg > img{left:-27px;top:-132px;width:1117px;height:630px;object-fit:cover;}   /* the garden: the box's aspect is the bitmap's to 0.2% */
.dsc-v-pick3 .dsc-sent{left:__RSX__px;top:__RSY__px;}   /* the box's centre 532.5,68 of the padding box: Chrome's Baloo ink sat 0.5 px right and 3 px above the render's there (measured, word by word; every word within 1 px, the gap 33 as T4's) */
.dsc-v-pick3 .dsc-sent .dsc-gap{margin-right:__RGAP__px;}   /* the frame's four-space run after गुलाब, where the slot sits */
.dsc-v-pick3 .dsc-slot{left:376px;top:71px;width:33px;height:38px;}   /* the frame's small slot, white */
.dsc-v-pick3 .dsc-tile{top:349px;} .dsc-v-pick3 .dsc-tile.t1{left:366.09px;} .dsc-v-pick3 .dsc-tile.t2{left:593px;} .dsc-v-pick3 .dsc-tile.t3{left:823.82px;}
.dsc-v-pick3 .dsc-tshade{background:#97CF28;}   /* the frame's tile ellipses: opaque #97CF28 on the grass */
.dsc-v-pick3 .dsc-girl{left:126px;top:123px;width:218px;height:328px;}
.dsc-v-pick3 .dsc-girl > img{width:218px;height:328px;object-fit:cover;}
.dsc-v-pick3 .dsc-shade{left:9px;top:298px;width:172px;height:38px;background:rgba(151,207,40,.4);}   /* her ellipse 810:14 (147,433 of the card: 9,298 of HER box — the first build had added the card's 12 px twice; scene_check caught it): #97CF28 at .4, reaching 8 px below her box */
""".replace("__GAP__", "33").replace("__QSX__", "495").replace("__QSY__", "118").replace("__RSX__", "533").replace("__RSY__", "71").replace("__RGAP__", "33").replace("__PSX__", "635.5").replace("__PSY__", "116")   # measured: each gap 40 + the space (11) = 7 px wider than the render's at 40
# [t3-look] the girl's layers: every layer fills her box and windows her bitmap (so at rest the composite IS the painting), each
# masked by its sheet from girl_rig.py (demo2_assets/girl_rig/, inlined here); the eyes' discs / irises and the elbow pivot in her
# box px (the 257x385 box over the 1024x1535 bitmap). The glance = three CSS animations on .look, all every_ms long and in step:
#   dscLookEye  the irises slide to (--look-gx, --look-gy) over 0.25 s (eased both ends: under 0.3 px a frame), hold, and are back by 2.05 s;
#   dscLookLean the whole figure shears from her feet toward the tiles (--look-lean) over 0.5 s, holds, back by 2.3 s;
#   dscLookArm  the forearm turns about the elbow up to --look-arm by 0.5 s (a touch past, settling), bobs twice (to 65 % and
#               back) over the next second, and is down by 2.2 s — never below 0, so its kept band under the braid never shows;
# the rest of the cycle (2.3 s .. every_ms) is the painting. [t3-look7] (asked 2026-11-02): the cycle 7 s (was 5 s); the keyframes
# are now written from the gesture's times in ms (_KF) as percentages of LOOK["every_ms"], so the gesture is the 5 s build's to the
# millisecond and only the rest after it grows (2.7 s -> 4.7 s).
def _look_kf():
    """[t3-look7] the glance's three keyframe sets, their stops given in ms of the gesture and written as % of the cycle"""
    ev = LOOK["every_ms"]; pc = lambda t: f"{100 * t / ev:.4g}%"
    assert LOOK["active_ms"] == 2300 and ev >= LOOK["active_ms"] + 500, LOOK
    A = lambda k: f"rotate(calc(var(--look-arm,0deg) * {k}))"
    eye = [((0,), "translate(0,0)", "cubic-bezier(.4,0,.2,1)"), ((250, 1750), "translate(var(--look-gx,0px),var(--look-gy,0px))", "cubic-bezier(.4,0,.3,1)"), ((2050, ev), "translate(0,0)", None)]
    lean = [((0,), "skewX(0deg)", "cubic-bezier(.4,0,.2,1)"), ((500, 1700), "skewX(calc(var(--look-lean,0deg) * -1))", "cubic-bezier(.4,0,.2,1)"), ((2300, ev), "skewX(0deg)", None)]
    arm = [((0, 100), "rotate(0deg)", "cubic-bezier(.3,.9,.4,1.25)"), ((500,), A(-1), "ease-in-out"), ((800,), A(-.65), "ease-in-out"), ((1100,), A(-1.05), "ease-in-out"),
           ((1400,), A(-.65), "ease-in-out"), ((1650,), A(-.9), "cubic-bezier(.4,0,.3,1)"), ((2200, ev), "rotate(0deg)", None)]
    def kf(name, stops):
        body = "".join(",".join(pc(t) for t in ts) + "{transform:" + tf + ";" + (f"animation-timing-function:{fn};" if fn else "") + "}" for ts, tf, fn in stops)
        return "@keyframes " + name + "{" + body + "}\n"
    return kf("dscLookEye", eye) + kf("dscLookLean", lean) + kf("dscLookArm", arm)
_RIG_DIR = SCR / "demo2_assets" / "girl_rig"
_rig_sheets = [f"demo2_girl_{k}.png" for k in ("body_mask", "arm_mask", "patch_mask", "eye1_mask", "eye2_mask", "iris1", "iris2")]
assert all((_RIG_DIR / v).exists() for v in _rig_sheets), "missing rig sheets: run girl_rig.py"
_durl = lambda name: "url(data:image/png;base64," + base64.b64encode((_RIG_DIR / name).read_bytes()).decode() + ")"
_px = lambda v: f"{v:.2f}px"
_piv = _rig["elbow"]["pivot"]
_eye_css = ""
for _i, _e in enumerate(_rig["eyes"], 1):
    _f = _e["iris"]; _ox, _oy, _sz, _ = _e["iris_box"]; _sc = _e["sclera"]
    _eye_css += (f".dsc-geye.e{_i}{{--m:{_durl(f'demo2_girl_eye{_i}_mask.png')};}}\n"
                 f".dsc-geye.e{_i} .dsc-gfill{{left:{_px((_f['cx'] - _f['r'] - 1) * _gsx)};top:{_px((_f['cy'] - _f['r'] - 1) * _gsy)};width:{_px(2 * (_f['r'] + 1) * _gsx)};height:{_px(2 * (_f['r'] + 1) * _gsy)};background:rgb({_sc[0]},{_sc[1]},{_sc[2]});}}\n"
                 f".dsc-geye.e{_i} .dsc-giris{{left:{_px(_ox * _gsx)};top:{_px(_oy * _gsy)};width:{_px(_sz * _gsx)};height:{_px(_sz * _gsy)};background:{_durl(f'demo2_girl_iris{_i}.png')} 0 0 / 100% 100% no-repeat;}}\n")
scene_css += ("\n/* ===== [t3-look] the girl in layers and her glance at the tiles (girl_rig.py; see build.py) ===== */\n"
    ".dsc-grig{position:absolute;left:0;top:0;width:100%;height:100%;transform-origin:50% 98.4%;}   /* the lean shears from her feet */\n"
    ".dsc-grig > *{position:absolute;left:0;top:0;width:100%;height:100%;-webkit-mask:var(--m) 0 0 / 100% 100% no-repeat;mask:var(--m) 0 0 / 100% 100% no-repeat;}\n"
    ".dsc-gwin{position:absolute;left:0;top:0;width:100%;height:100%;}\n"
    ".dsc-gfill{position:absolute;border-radius:50%;}\n"
    ".dsc-giris{position:absolute;}\n"
    f".dsc-gbody{{--m:{_durl('demo2_girl_body_mask.png')};}}\n"
    f".dsc-garm{{--m:{_durl('demo2_girl_arm_mask.png')};transform-origin:{_px(_piv[0] * _gsx)} {_px(_piv[1] * _gsy)};}}   /* the elbow */\n"
    f".dsc-gpatch{{--m:{_durl('demo2_girl_patch_mask.png')};}}\n"
    + _eye_css +
    ".dsc-grig,.dsc-giris,.dsc-garm{will-change:transform;}   /* [t3-look7] composited from mount (was from .look): the glance's start no longer switches how she is drawn */\n"
    ".dsc-girl.warm .dsc-grig{transform:skewX(-.001deg);} .dsc-girl.warm .dsc-giris{transform:translate(.001px,.001px);} .dsc-girl.warm .dsc-garm{transform:rotate(-.001deg);}   /* [t3-look7] the GPU warm-up (see the module) */\n"
    ".dsc-girl.look .dsc-grig{animation:dscLookLean var(--look-ms,5000ms) linear infinite;}\n"
    ".dsc-girl.look .dsc-giris{animation:dscLookEye var(--look-ms,5000ms) linear infinite;}\n"
    ".dsc-girl.look .dsc-garm{animation:dscLookArm var(--look-ms,5000ms) linear infinite;}\n"
    + _look_kf())
# [t4-basket] T4's girl in layers (girl_rig_t4.py: demo3_assets/girl_rig/, inlined): every layer fills her 224x336 box, the windows
# her bitmap stretched to it and masked by a full-size sheet at 100% 100% (the patch its own image); the eyes' discs / irises in her
# box px. The look = four CSS animations on .look, all every_ms long and in step (ms stops written as % of the cycle):
#   dscBasketLift  the basket + both hands up lift_px over 0.65 s (eased both ends), held to 1.75 s, down by 2.35 s;
#   dscBasketFore  the forearm's skewY about the elbow's line (elbow_x) on the same stops / easings — its wrist end rises exactly
#                  as the hand does (tan(shear) x the wrist's distance = lift_px);
#   dscBasketHead  the head group (head, braids, eyes) down dip_px from 0.15 s to 0.7 s, held to 1.7 s, up by 2.25 s;
#   dscBasketEye   the irises into the basket by 0.48 s (gaze[0]), over the fruit by 1.3 s (gaze[1]), back to the screen by 2.05 s.
_RIG4 = SCR / "demo3_assets" / "girl_rig"
_rig4_sheets = [f"demo3_girl_{k}.png" for k in ("under", "body_mask", "fore_mask", "elbow_mask", "head_mask", "basket_mask", "eye1_mask", "eye2_mask", "iris1", "iris2")]
assert all((_RIG4 / v).exists() for v in _rig4_sheets), "missing rig sheets: run girl_rig_t4.py"
_durl4 = lambda name: "url(data:image/png;base64," + base64.b64encode((_RIG4 / name).read_bytes()).decode() + ")"
_m4 = lambda name: f"--m:{_durl4(name)};"   # each sheet once, read by the shared mask rule (as T3's --m)
_eye4_css = ""
for _i, _e in enumerate(_rig4["eyes"], 1):
    _f = _e["iris"]; _ox, _oy, _sz, _ = _e["iris_box"]; _sc = _e["sclera"]
    _eye4_css += (f".dsc-beye.e{_i}{{{_m4(f'demo3_girl_eye{_i}_mask.png')}}}\n"
                  f".dsc-beye.e{_i} .dsc-bfill{{left:{_px((_f['cx'] - _f['r'] - 1) * _g4sx)};top:{_px((_f['cy'] - _f['r'] - 1) * _g4sy)};width:{_px(2 * (_f['r'] + 1) * _g4sx)};height:{_px(2 * (_f['r'] + 1) * _g4sy)};background:rgb({_sc[0]},{_sc[1]},{_sc[2]});}}\n"
                  f".dsc-beye.e{_i} .dsc-biris{{left:{_px(_ox * _g4sx)};top:{_px(_oy * _g4sy)};width:{_px(_sz * _g4sx)};height:{_px(_sz * _g4sy)};background:{_durl4(f'demo3_girl_iris{_i}.png')} 0 0 / 100% 100% no-repeat;}}\n")
def _basket_kf():
    """[t4-basket] the look's four keyframe sets, their stops in ms of the gesture written as % of the 7 s cycle"""
    ev = LOOK4["every_ms"]; pc = lambda t: f"{100 * t / ev:.4g}%"
    assert LOOK4["active_ms"] == 2400 and ev >= LOOK4["active_ms"] + 500, LOOK4
    L, Dp, Sk = LOOK4["lift_px"], LOOK4["dip_px"], LOOK4["shear_deg"]; (g1x, g1y), (g2x, g2y) = LOOK4["gaze"]
    up, down = "cubic-bezier(.45,0,.3,1)", "cubic-bezier(.45,0,.35,1)"
    lift = [((0,), "translateY(0px)", up), ((650, 1750), f"translateY(-{L}px)", down), ((2350, ev), "translateY(0px)", None)]
    fore = [((0,), "skewY(0deg)", up), ((650, 1750), f"skewY(-{Sk}deg)", down), ((2350, ev), "skewY(0deg)", None)]
    head = [((0, 150), "translateY(0px)", "cubic-bezier(.4,0,.3,1)"), ((700, 1700), f"translateY({Dp}px)", "cubic-bezier(.4,0,.3,1)"), ((2250, ev), "translateY(0px)", None)]
    eye = [((0, 100), "translate(0px,0px)", "cubic-bezier(.4,0,.2,1)"), ((480, 1000), f"translate({g1x}px,{g1y}px)", "cubic-bezier(.45,0,.4,1)"),
           ((1300, 1650), f"translate({g2x}px,{g2y}px)", "cubic-bezier(.4,0,.3,1)"), ((2050, ev), "translate(0px,0px)", None)]
    def kf(name, stops):
        body = "".join(",".join(pc(t) for t in ts) + "{transform:" + tf + ";" + (f"animation-timing-function:{fn};" if fn else "") + "}" for ts, tf, fn in stops)
        return "@keyframes " + name + "{" + body + "}\n"
    return kf("dscBasketLift", lift) + kf("dscBasketFore", fore) + kf("dscBasketHead", head) + kf("dscBasketEye", eye)
scene_css += ("\n/* ===== [t4-basket] T4's girl in layers and her look into the basket (girl_rig_t4.py; see build.py) ===== */\n"
    ".dsc-brig{position:absolute;left:0;top:0;width:100%;height:100%;}\n"
    ".dsc-brig > *,.dsc-bhead > *,.dsc-beye > img{position:absolute;left:0;top:0;width:100%;height:100%;}\n"
    ".dsc-bfill{position:absolute;border-radius:50%;} .dsc-biris{position:absolute;}\n"
    ".dsc-bbody,.dsc-bfore,.dsc-belbow,.dsc-bheadw,.dsc-bbasket,.dsc-beye{-webkit-mask:var(--m) 0 0 / 100% 100% no-repeat;mask:var(--m) 0 0 / 100% 100% no-repeat;}\n"
    f".dsc-bunder{{background:{_durl4('demo3_girl_under.png')} 0 0 / 100% 100% no-repeat;}}   /* her dress / bodice / the background behind what the lift uncovers */\n"
    f".dsc-bbody{{{_m4('demo3_girl_body_mask.png')}}}\n"
    f".dsc-bfore{{{_m4('demo3_girl_fore_mask.png')}transform-origin:{_px(LOOK4['elbow_x'])} 0px;}}   /* the forearm, sheared from the elbow's line */\n"
    f".dsc-belbow{{{_m4('demo3_girl_elbow_mask.png')}}}   /* the upper arm's fold, over the forearm */\n"
    f".dsc-bheadw{{{_m4('demo3_girl_head_mask.png')}}}\n"
    f".dsc-bbasket{{{_m4('demo3_girl_basket_mask.png')}}}\n"
    + _eye4_css +
    ".dsc-bfore,.dsc-bbasket,.dsc-bhead,.dsc-biris{will-change:transform;}   /* composited from mount, as T3's layers ([t3-look7]) */\n"
    ".dsc-girl.warm .dsc-bfore{transform:skewY(-.001deg);} .dsc-girl.warm .dsc-bbasket{transform:translateY(-.001px);} .dsc-girl.warm .dsc-bhead{transform:translateY(.001px);} .dsc-girl.warm .dsc-biris{transform:translate(.001px,.001px);}   /* the GPU warm-up (see the module) */\n"
    ".dsc-girl.look .dsc-bbasket{animation:dscBasketLift var(--look-ms,7000ms) linear infinite;}\n"
    ".dsc-girl.look .dsc-bfore{animation:dscBasketFore var(--look-ms,7000ms) linear infinite;}\n"
    ".dsc-girl.look .dsc-bhead{animation:dscBasketHead var(--look-ms,7000ms) linear infinite;}\n"
    ".dsc-girl.look .dsc-biris{animation:dscBasketEye var(--look-ms,7000ms) linear infinite;}\n"
    + _basket_kf())
# [g3-grow] G3's plants (plant_rig_g3.py: g3_assets/plant_rig/, the cut-outs shipped as files, decoded before they grow) over the
# garden without them, each box the cut-out's own in the garden's cover mapping, its origin the stem's base; and G3's girl's eyes
# (girl_rig_g3.py: g3_assets/girl_rig/, inlined): each eye a mask sheet at her box (cover, as her image), the cover and the iris as
# images at the iris's box. The growth: dscPlantH (the height and the fade-in) on the image, dscPlantW (the width, a beat behind)
# on its box, both data.grow.dur_ms long, each plant data.grow.delays_ms[k] late; the glance: dscEyesLook, every_ms long, the
# irises to the gaze over 0.45 s, held to 1.65 s, home by 2.1 s.
_R3 = SCR / "g3_assets" / "girl_rig"
_r3_sheets = [f"g3_girl_{k}.png" for k in ("eye1_mask", "eye2_mask", "fill1", "fill2", "iris1", "iris2")]
assert all((_R3 / v).exists() for v in _r3_sheets), "missing rig sheets: run girl_rig_g3.py"
_durl3 = lambda name: "url(data:image/png;base64," + base64.b64encode((_R3 / name).read_bytes()).decode() + ")"
_plant_css = ""
for _k, _q in enumerate(_prig3["plants"], 1):
    _bx, _by, _bw, _bh = _q["box"]; _ox, _oy = (_q["base"][0] - _bx) * G3_BGS, (_q["base"][1] - _by) * G3_BGS
    _plant_css += (f".dsc-v-pick3 .dsc-plant.p{_k}{{left:{_px(G3_BGX + _bx * G3_BGS)};top:{_px(G3_BGY + _by * G3_BGS)};width:{_px(_bw * G3_BGS)};height:{_px(_bh * G3_BGS)};"
                   f"transform-origin:{_px(_ox)} {_px(_oy)};--g-delay:{GROW3['delays_ms'][_k - 1]}ms;}}   /* the {_q['name']}: its stem's base at {_q['base'][0]},{_q['base'][1]} of the garden */\n"
                   f".dsc-v-pick3 .dsc-plant.p{_k} > img{{transform-origin:{_px(_ox)} {_px(_oy)};}}\n")
_eye3_css = ""
for _i, _e in enumerate(_erig3["eyes"], 1):
    _ox, _oy, _sz, _ = _e["iris_box"]
    _at = f"left:{_px(G3_GX + _ox * G3_GS)};top:{_px(_oy * G3_GS)};width:{_px(_sz * G3_GS)};height:{_px(_sz * G3_GS)};"
    _eye3_css += (f".dsc-eeye.e{_i}{{--m:{_durl3(f'g3_girl_eye{_i}_mask.png')};}}\n"
                  f".dsc-eeye.e{_i} .dsc-efill{{{_at}background:{_durl3(f'g3_girl_fill{_i}.png')} 0 0 / 100% 100% no-repeat;}}\n"
                  f".dsc-eeye.e{_i} .dsc-eiris{{{_at}background:{_durl3(f'g3_girl_iris{_i}.png')} 0 0 / 100% 100% no-repeat;}}\n")
def _grow_kf():
    """[g3-grow] the growth (stops in ms of data.grow.dur_ms written as %) and the glance (ms of the 7 s cycle written as %)"""
    D = GROW3["dur_ms"]; pc = lambda t, ev: f"{100 * t / ev:.4g}%"
    sw = "cubic-bezier(.45,0,.55,1)"   # each swing of the settle eases out of one extreme into the next
    H = [((0,), "transform:scaleY(.03);opacity:0;", "cubic-bezier(.3,.6,.4,1)"), ((80,), "opacity:1;", None), ((580,), "transform:scaleY(1.08);", sw),
         ((760,), "transform:scaleY(.965);", sw), ((900,), "transform:scaleY(1.012);", sw), ((D,), "transform:none;opacity:1;", None)]
    Wd = [((0,), "transform:scaleX(.22);", "cubic-bezier(.35,.25,.4,1)"), ((620,), "transform:scaleX(1.05);", sw), ((800,), "transform:scaleX(.985);", sw),
          ((930,), "transform:scaleX(1.004);", sw), ((D,), "transform:none;", None)]
    ev = LOOK3["every_ms"]; gx, gy = LOOK3["gaze"]
    assert LOOK3["active_ms"] == 2100 and ev >= LOOK3["active_ms"] + 500, LOOK3
    E = [((0,), "transform:translate(0px,0px);", "cubic-bezier(.4,0,.2,1)"), ((450, 1650), f"transform:translate({gx}px,{gy}px);", "cubic-bezier(.4,0,.3,1)"), ((2100, ev), "transform:translate(0px,0px);", None)]
    def kf(name, stops, total):
        body = "".join(",".join(pc(t, total) for t in ts) + "{" + decl + (f"animation-timing-function:{fn};" if fn else "") + "}" for ts, decl, fn in stops)
        return "@keyframes " + name + "{" + body + "}\n"
    return kf("dscPlantH", H, D) + kf("dscPlantW", Wd, D) + kf("dscEyesLook", E, ev)
scene_css += ("\n/* ===== [g3-grow] G3's plants growing out of their soil and the girl's glance at them (plant_rig_g3.py, girl_rig_g3.py; see build.py) ===== */\n"
    ".dsc-plants{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;}\n"
    ".dsc-plant{position:absolute;} .dsc-plant > img{position:absolute;left:0;top:0;width:100%;height:100%;}\n"
    ".dsc-plants:not(.grow) .dsc-plant{visibility:hidden;}   /* the page opens on the garden without them */\n"
    f".dsc-plants.grow .dsc-plant{{animation:dscPlantW {GROW3['dur_ms']}ms linear var(--g-delay,0ms) both;}}\n"
    f".dsc-plants.grow .dsc-plant > img{{animation:dscPlantH {GROW3['dur_ms']}ms linear var(--g-delay,0ms) both;}}\n"
    + _plant_css +
    ".dsc-erig{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none;}\n"
    ".dsc-eeye{position:absolute;left:0;top:0;width:100%;height:100%;-webkit-mask:var(--m) 50% 50% / cover no-repeat;mask:var(--m) 50% 50% / cover no-repeat;}   /* her image's own cover */\n"
    ".dsc-efill,.dsc-eiris{position:absolute;}\n"
    + _eye3_css +
    ".dsc-eiris{will-change:transform;}   /* composited from mount, as T3's / T4's irises */\n"
    ".dsc-girl.warm .dsc-eiris{transform:translate(.001px,.001px);}   /* the GPU warm-up (see the module) */\n"
    ".dsc-girl.look .dsc-eiris{animation:dscEyesLook var(--look-ms,7000ms) linear infinite;}\n"
    + _grow_kf())
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
       + feedback_rules + fit_rules + title_css + story_css + recap_css + demo_css + scene_css + sent_css + letter_css + stamp_css)

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
# [t4-scene] T4's PUNCT_DEMO hooks (mark_audio vo_recap_alp_name, explain_audio vo_demo3_explain, again_audio vo_demo_again) are gone:
# T4 is a scene whose explanation (vo_demo3_explain) is in its own data; [t2-scene] / [t3-scene] dropped T2's and T3's the same way
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
# [recap-fig2] the [vo-rec] lead line (data.lead_audio, set below) is played by the module itself now
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
# [recap-fig2] T1's picture (frame 764:144's node 764:753, its source bitmap as WebP), kept in recap_assets/
for name, sub in (("img_recap_girl.webp", "Images"), ("sfx_fb_correct.ogg", "Audio"),   # [recap-sfx] the picture's sound
                  ("img_recap_house.webp", "Images")):   # [recap-prashn] T1C's picture (node 766:1140's source bitmap)
    f, dst = SCR / "recap_assets" / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing recap asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7c. [recap-fig] the recap's clips (kept next to this script, in recap_assets/, made by recap_vo.py) ----------
RECAP_SRC = SCR / "recap_assets"
for k in RECAP_KEYS:
    f, dst = RECAP_SRC / f"vo_recap_{k}.ogg", DIST / "assets" / "Audio" / f"vo_recap_{k}.ogg"
    assert f.exists(), f"missing recap clip {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7d. [demo-fig] the demo's clips and pictures (demo1_assets/: recap_vo.py demo1; the two Figma bitmaps) ----------
DEMO_SRC = SCR / "demo1_assets"
for name, sub in [(f"vo_demo1_{k}.ogg", "Audio") for k in DEMO_KEYS] + [("demo1_head.webp", "UI"),   # [t2-scene] the scene's bitmaps and the user's two sounds (bytes as given)
                  ("img_demo1_hall.webp", "Images"), ("img_demo1_girl_walk.webp", "Images"), ("sfx_demo1_school.mp3", "Audio"), ("sfx_demo1_pop.mp3", "Audio")]:
    f, dst = DEMO_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing demo asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
for name, sub in (("img_demo1_girl.webp", "Images"),):   # [t2-scene] T2's old cut-out picture: no page uses it now
    (DIST / "assets" / sub / name).unlink(missing_ok=True)

# ---------- 7e. [demo-fig] T3's clips and picture (demo2_assets/: recap_vo.py demo2; the frame's "image 229"; its head is
#               byte-for-byte T2's demo1_head.webp) ----------
DEMO2_SRC = SCR / "demo2_assets"
for name, sub in [(f"vo_demo2_{k}.ogg", "Audio") for k in DEMO2_CLIPS] + [("img_demo2_room.webp", "Images"), ("img_demo2_bubble.svg", "Images"), ("img_demo2_girl_ask.webp", "Images"), ("sfx_demo2_sharp_pop.mp3", "Audio")]:   # [t3-scene] the frame's room (image 261, 1816x866 q90) and bubble (its vector group, as exported), the user's sharp pop (bytes as given)
    f, dst = DEMO2_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing demo asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
(DIST / "assets" / "Audio" / "vo_demo2_intro.ogg").unlink(missing_ok=True)   # [demo-intro] the intro line is off the page
(DIST / "assets" / "Images" / "img_demo2_girl.webp").unlink(missing_ok=True)   # [t3-scene] [demo2-girl]'s cut-out: no page shows it now

# ---------- 7f. [demo-fig] T4's clips and picture (demo3_assets/: recap_vo.py demo3; the frame's "image 230"; its head is
#               byte-for-byte T2's demo1_head.webp) ----------
DEMO3_SRC = SCR / "demo3_assets"
for name, sub in [(f"vo_demo3_{k}.ogg", "Audio") for k in DEMO3_CLIPS] + [("img_demo3_fruits.webp", "Images"), ("img_demo3_park.webp", "Images"), ("img_demo3_girl_basket.webp", "Images")]:   # [t4-scene] the frame's landscape (mirrored) and girl
    f, dst = DEMO3_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing demo asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
(DIST / "assets" / "Audio" / "vo_demo3_intro.ogg").unlink(missing_ok=True)   # [demo-intro] the intro line is off the page

# ---------- 7g. [pick-fig] G1's clips and picture (g1_assets/: recap_vo.py g1; the frame's "image 231"; its head is
#               byte-for-byte T2's demo1_head.webp; the name on the right tap is T2's vo_demo1_purn) ----------
G1_SRC = SCR / "g1_assets"
for name, sub in [(f"vo_g1_{k}.ogg", "Audio") for k in G1_KEYS] + [("img_g1_girl_ball.webp", "Images"), ("img_g1_room.webp", "Images"), ("img_g1_girl_ball2.webp", "Images")]:   # [g1-scene] + the frame's room and girl
    f, dst = G1_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing G1 asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
# ---------- 7h. [pick-fig] G2's sentence clip and picture (g2_assets/: recap_vo.py g2; the frame's "image 239"; its title bar is
#               T4's to the pixel, its instruction G1's vo_g1_intro, its name on the right tap T3's vo_demo2_prashn) ----------
G2_SRC = SCR / "g2_assets"
for name, sub in (("vo_g2_sent.ogg", "Audio"), ("img_g2_girl_bag.webp", "Images"), ("img_g2_street.webp", "Images"), ("img_g2_girl_bag2.webp", "Images")):   # [g2-scene] + the frame's street and girl
    f, dst = G2_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing G2 asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
# ---------- 7i. [pick-fig] G3's sentence clip and picture (g3_assets/: recap_vo.py g3; the frame's "image 233"; its title bar
#               is G1's to the pixel, its instruction vo_g1_intro, its name on the right tap T4's vo_demo3_alp) ----------
G3_SRC = SCR / "g3_assets"
for name, sub in (("vo_g3_sent.ogg", "Audio"), ("img_g3_flowers.webp", "Images"), ("img_g3_garden.webp", "Images"), ("img_g3_girl_point.webp", "Images"),   # [g3-scene] + the frame's garden and girl
                  ("plant_rig/img_g3_garden_bare.webp", "Images"), ("plant_rig/img_g3_plant_rose.webp", "Images"), ("plant_rig/img_g3_plant_marigold.webp", "Images"),
                  ("plant_rig/img_g3_plant_jasmine.webp", "Images"), ("sfx_g3_grow.mp3", "Audio")):   # [g3-grow] the garden without its plants, the three plants, the raised sound
    f, dst = G3_SRC / name, DIST / "assets" / sub / pathlib.Path(name).name
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
