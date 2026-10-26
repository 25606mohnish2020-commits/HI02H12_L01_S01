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
# story in two beats on one layout: frame 435:5, then frame 476:198 (new picture, new text, new narration).
# Texts, clips and per-word start times come from story_assets/ (made by story_vo.py, checked by align_story_vo.py).
lines = {k: json.loads((SCR / "story_assets" / f"vo_story_{k}.words.json").read_text(encoding="utf-8")) for k in ("s1", "s2")}
beats = [{"image_id": img, "text_hi": lines[k]["text"], "word_times": [t[0] for t in lines[k]["word_times"]],
          "audio": f"vo_story_{k}"} for k, img in (("s1", "img_story_chintu"), ("s2", "img_story_chintu_2"))]
card["slides"].insert(0, {"id": "T0", "phase": "tutorial", "eis": "iconic", "type": "STORY_LISTEN",
    "prompt_hi": lines["s1"]["text"], "audio": {"narration": "vo_story_s1", "narration_2": "vo_story_s2"},
    "data": {"beats": beats}})
for b in beats:
    card["assets"]["audio"][b["audio"]] = f"assets/Audio/{b['audio']}.ogg"
    card["assets"]["audio_text"][b["audio"]] = b["text_hi"]
    card["assets"]["image"][b["image_id"]] = f"assets/Images/{b['image_id']}.webp"
# [story-fig] then "आइए वाक्य सुनें।" (frame 488:190): the intro line under the title, then the punctuated sentences
for k in ("r0", "r1"):
    lines[k] = json.loads((SCR / "story_assets" / f"vo_story_{k}.words.json").read_text(encoding="utf-8"))
card["slides"].insert(1, {"id": "T0B", "phase": "tutorial", "eis": "iconic", "type": "STORY_RELISTEN",
    "prompt_hi": "आइए वाक्य सुनें।", "audio": {"intro": "vo_story_r0", "narration": "vo_story_r1"},
    "data": {"title_hi": "आइए वाक्य सुनें।", "intro_audio": "vo_story_r0", "text_hi": lines["r1"]["text"],
             "word_times": [t[0] for t in lines["r1"]["word_times"]], "audio": "vo_story_r1"}})
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
part = lambda k: {"text_hi": rl[k]["shown"], "audio": f"vo_recap_{k}", "word_times": [t[0] for t in rl[k]["word_times"]]}
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
DEMO_KEYS = ["intro", "sent", "purn", "full"]
dl = {k: json.loads((SCR / "demo1_assets" / f"vo_demo1_{k}.words.json").read_text(encoding="utf-8")) for k in DEMO_KEYS}
i_t2 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "T2")
assert card["slides"][i_t2]["type"] == "BUILD_PUNCT" and card["slides"][i_t2]["data"].get("auto"), "T2 is not the first auto demo"
dpart = lambda k: {"text_hi": dl[k]["shown"], "audio": f"vo_demo1_{k}", "word_times": [t[0] for t in dl[k]["word_times"]]}
card["slides"][i_t2] = {"id": "T2", "phase": "tutorial", "eis": "enactive", "type": "PUNCT_DEMO",
    "prompt_hi": dl["intro"]["shown"], "audio": {"prompt": "vo_demo1_intro"},
    "data": {"band_hi": dl["intro"]["shown"], "intro_audio": "vo_demo1_intro", "image_id": "img_demo1_girl",
             "sentence": dpart("sent"), "mark": "।", "mark_audio": "vo_demo1_purn", "full": dpart("full"),
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500, "hold_ms": 1500},
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
DEMO2_KEYS = ["intro", "sent", "prashn", "full"]
dl2 = {k: json.loads((SCR / "demo2_assets" / f"vo_demo2_{k}.words.json").read_text(encoding="utf-8")) for k in DEMO2_KEYS}
i_t3 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "T3")
_t3 = card["slides"][i_t3]
assert _t3["type"] == "BUILD_PUNCT" and _t3["data"].get("auto") and [m["mark"] for m in _t3["data"]["marks"]] == ["?"], "T3 is not the question-mark auto demo"
dpart2 = lambda k: {"text_hi": dl2[k]["shown"], "audio": f"vo_demo2_{k}", "word_times": [t[0] for t in dl2[k]["word_times"]]}
card["slides"][i_t3] = {"id": "T3", "phase": "tutorial", "eis": "enactive", "type": "PUNCT_DEMO",
    "prompt_hi": dl2["intro"]["shown"], "audio": {"prompt": "vo_demo2_intro"},
    "data": {"band_hi": dl2["intro"]["shown"], "intro_audio": "vo_demo2_intro", "image_id": "img_demo2_boy",
             "sentence": dpart2("sent"), "mark": "?", "mark_audio": "vo_demo2_prashn", "full": dpart2("full"),
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500, "hold_ms": 1500, "layout": {"sent_x": 120, "img": [204, 215, 130, 128]}},
    "signals": {"on_complete": []}}
for k in DEMO2_KEYS:
    card["assets"]["audio"][f"vo_demo2_{k}"] = f"assets/Audio/vo_demo2_{k}.ogg"
    card["assets"]["audio_text"][f"vo_demo2_{k}"] = dl2[k]["text"]
card["assets"]["image"]["img_demo2_boy"] = "assets/Images/img_demo2_boy.webp"
card["_emoji_fallback"]["img_demo2_boy"] = "✏️"
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
dl3 = {k: json.loads((SCR / "demo3_assets" / f"vo_demo3_{k}.words.json").read_text(encoding="utf-8")) for k in DEMO3_KEYS}
i_t4 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "T4")
_t4 = card["slides"][i_t4]
assert _t4["type"] == "BUILD_PUNCT" and _t4["data"].get("auto") and "," in [m["mark"] for m in _t4["data"]["marks"]], "T4 is not the comma auto demo"
dpart3 = lambda k: {"text_hi": dl3[k]["shown"], "audio": f"vo_demo3_{k}", "word_times": [t[0] for t in dl3[k]["word_times"]]}
_full3 = dpart3("full")
# the second reading's tokens: मेरे पास आम, अल्पविराम, केला, अल्पविराम, सेब और संतरा है। -> sentence words 0-2, slot 0, word 3,
# slot 1, words 4-7 (the sentence's spans: मेरे पास आम केला सेब और संतरा है ।)
_full3["targets"] = ["w0", "w1", "w2", "s0", "w3", "s1", "w4", "w5", "w6", "w7"]
assert len(_full3["targets"]) == len(_full3["word_times"]), "T4: the second reading's tokens and its targets differ in number"
# measured against the frame's render (word by word): Baloo Bhai 2's spaces are 3px narrower than Noto's at 50px
# (layout.sent.ws), its line box puts the glyphs where an 84px one does here, and the space before the closing danda
# ("है ।") is 4.5px narrower still in the render — sentence.nudge pulls the danda (span 8) in by that much; with it
# every word's ink is within 1px of the render
_sent3 = dict(dpart3("sent"), gaps=[2, 3], gap_spaces=4, nudge={"8": -4.5})
assert _sent3["text_hi"].split()[2:4] == ["आम", "केला"], "T4: the slots no longer follow आम / केला"
# the slots' dashes, measured on the frame's render: two dashes centred on each side, [margin, dash, gap, dash, margin]
_slot = lambda x: {"x": x, "y": 76, "w": 33, "h": 38, "dash_h": [4.5, 9.5, 5, 9.5, 4.5], "dash_v": [5, 10, 8, 10, 5]}
card["slides"][i_t4] = {"id": "T4", "phase": "tutorial", "eis": "enactive", "type": "PUNCT_DEMO",
    "prompt_hi": dl3["intro"]["shown"], "audio": {"prompt": "vo_demo3_intro"},
    "data": {"band_hi": dl3["intro"]["shown"], "intro_audio": "vo_demo3_intro", "image_id": "img_demo3_fruits",
             "sentence": _sent3, "mark": ",", "mark_audio": "vo_demo3_alp", "mark_size": 50, "mark_stagger_ms": 300,
             "full": _full3, "slots": [_slot(286), _slot(417)],
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500, "hold_ms": 1500,
             "layout": {"pic_x": 144, "img": [144, 229, 144, 96], "bar": [312, 824],
                        "sent": {"x": -34, "y": 33, "w": 893, "size": 50, "lh": 84, "ws": -3}}},
    "signals": {"on_complete": []}}
for k in DEMO3_KEYS:
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
G1_KEYS = ["intro", "sent"]
gl = {k: json.loads((SCR / "g1_assets" / f"vo_g1_{k}.words.json").read_text(encoding="utf-8")) for k in G1_KEYS}
i_g1 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "G1")
_g1 = card["slides"][i_g1]
assert _g1["type"] == "BUILD_PUNCT" and _g1["phase"] == "guided" and not _g1["data"].get("auto"), "G1 is not the first guided builder"
card["slides"][i_g1] = {"id": "G1", "phase": "guided", "eis": "enactive", "type": "PUNCT_PICK",
    "prompt_hi": gl["intro"]["shown"], "audio": {"prompt": "vo_g1_intro"},
    "data": {"band_hi": gl["intro"]["shown"], "intro_audio": "vo_g1_intro", "image_id": "img_g1_boy_ball",
             "sentence": {"text_hi": gl["sent"]["shown"], "audio": "vo_g1_sent", "word_times": [t[0] for t in gl["sent"]["word_times"]]},
             "mark": "।", "mark_audio": "vo_demo1_purn",
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500,
             "layout": {"img": [207, 219, 124, 124], "sent": {"x": 60, "y": 18, "w": 522, "size": 64, "lh": 110, "ws": -4},
                        "tiles": [{"base": [197, 442, 227, 170], "face": [199, 445, 223, 161]},
                                  {"base": [525, 443, 231, 169], "face": [527, 445, 227, 161]}, None]}},
    "signals": {"on_complete": ["punct_build_done"]}}
for k in G1_KEYS:
    card["assets"]["audio"][f"vo_g1_{k}"] = f"assets/Audio/vo_g1_{k}.ogg"
    card["assets"]["audio_text"][f"vo_g1_{k}"] = gl[k]["text"]
card["assets"]["image"]["img_g1_boy_ball"] = "assets/Images/img_g1_boy_ball.webp"
card["_emoji_fallback"]["img_g1_boy_ball"] = "✏️"
# [pick-fig] G2 = the Figma frame 600:197 "8 G2", G1's page and flow for "तुम कहाँ जा रहे हो" (the ported builder had the same
# sentence and mark): the प्रश्नवाचक चिह्न tile is the right one. The frame's title bar is T4's to the pixel — its text too,
# "सुनो यह वाक्य बिना रुके पढ़ा गया ।" — while the line it plays is G1's instruction "वाक्य सुनिए और सही चिह्न लगाइए ।" (both as
# asked); the tiles are T3's (no G1 tweaks), the sentence box is T3's (479 wide at 120), the picture "image 239" (a boy with
# a school bag, 102x136 at 218,213) is drawn over its box, and the empty slot sits at 573,20 in the bar (T3's at 583) —
# data.layout.slot. Its sentence clip + timings from g2_assets/ (recap_vo.py g2); the instruction is vo_g1_intro and the name
# on the right tap T3's vo_demo2_prashn (the same voice).
gl2 = json.loads((SCR / "g2_assets" / "vo_g2_sent.words.json").read_text(encoding="utf-8"))
i_g2 = next(i for i, s in enumerate(card["slides"]) if s["id"] == "G2")
_g2 = card["slides"][i_g2]
assert _g2["type"] == "BUILD_PUNCT" and _g2["phase"] == "guided" and [m["mark"] for m in _g2["data"]["marks"]] == ["?"], "G2 is not the question-mark builder"
assert " ".join(_g2["data"]["words"]) == gl2["shown"], "G2's sentence is not the frame's"
card["slides"][i_g2] = {"id": "G2", "phase": "guided", "eis": "enactive", "type": "PUNCT_PICK",
    "prompt_hi": gl["intro"]["shown"], "audio": {"prompt": "vo_g1_intro"},
    "data": {"band_hi": dl3["intro"]["shown"], "intro_audio": "vo_g1_intro", "image_id": "img_g2_boy_bag",
             "sentence": {"text_hi": gl2["shown"], "audio": "vo_g2_sent", "word_times": [t[0] for t in gl2["word_times"]]},
             "mark": "?", "mark_audio": "vo_demo2_prashn",
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500,
             "layout": {"sent_x": 120, "img": [218, 213, 102, 136], "slot": [573, 20]}},
    "signals": {"on_complete": ["punct_build_done"]}}
card["assets"]["audio"]["vo_g2_sent"] = "assets/Audio/vo_g2_sent.ogg"
card["assets"]["audio_text"]["vo_g2_sent"] = gl2["text"]
card["assets"]["image"]["img_g2_boy_bag"] = "assets/Images/img_g2_boy_bag.webp"
card["_emoji_fallback"]["img_g2_boy_bag"] = "✏️"
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
             "sentence": {"text_hi": gl3["shown"], "audio": "vo_g3_sent", "word_times": [t[0] for t in gl3["word_times"]],
                          "gaps": [2], "gap_spaces": 4, "nudge": {"9": -4.5}},
             "mark": ",", "mark_audio": "vo_demo3_alp", "mark_size": 50,
             "slots": [{"x": 278, "y": 70, "w": 33, "h": 38, "dash_h": [4.5, 9.5, 5, 9.5, 4.5], "dash_v": [5, 10, 8, 10, 5]}],
             "options": [{"mark": "।", "name_hi": "पूर्ण विराम"}, {"mark": ",", "name_hi": "अल्प विराम"}, {"mark": "?", "name_hi": "प्रश्नवाचक चिह्न"}],
             "blink_ms": 3500,
             "layout": {"pic_x": 144, "img": [146, 211, 140, 140], "bar": [312, 824],
                        "sent": {"x": -28, "y": 33, "w": 893, "size": 50, "lh": 84, "ws": -3}}},
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
# P1: two boys and a picture book; the sentences differ only in where the question mark sits — in place of the ported
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
   sfigLine() makes a narrated text: one span per word ("\n" = a line break) plus its clip and word times.
   sfigNarrate() plays that clip and reveals each word as the narration reaches it: word_times are each word's
   start (s) in the clip (the synthesiser's word boundaries, cross-checked with whisper — see
   _reskin_tools/story_vo.py), read against the clip's own currentTime, so a late or slow start stays in sync;
   a missing clip runs the same times on the wall clock, and without times the clip is shared out by word length. */
function sfigMount(host, inner){
  const card = host.closest(".tut-card"); if(card) card.classList.add("no-prompt", "sfig-card");
  const fig = document.createElement("div"); fig.className = "sfig-in";
  const grid = (c)=> '<img class="sfig-grid ' + c + '" src="assets/UI/story_grid.svg" width="718.497" height="718.497" alt="" draggable="false">';
  fig.innerHTML = '<div class="sfig-clip">' + grid("g1") + grid("g2") + '</div>' + inner +
    '<img class="sfig-swiftie" src="assets/UI/title_swiftie_hello.png" alt="Swiftee" draggable="false">';
  host.appendChild(fig);
  return fig;
}
function sfigLine(p, text, wordTimes, audio){
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
  return { words, share, times, src, file: src ? src.split("/").pop() : "" };
}
function sfigShow(L, n){ L.words.forEach((w, i)=> w.classList.toggle("on", i < n)); }
/* live() = "still this run, on a mounted page"; onEnd runs once, with every word shown. Watchdog: a clip that
   never reports its end must not strand the page. It stops the clip first, so आगे still opens live, never
   greyed out under a "playing" clip. */
function sfigNarrate(L, live, onEnd){
  const began = Date.now();
  let done = false;
  sfigShow(L, 0);
  const end = ()=>{
    if(done || !live()) return;
    done = true;
    sfigShow(L, L.words.length);
    onEnd();
  };
  play(L.src, end);
  const last = L.times ? L.times[L.times.length - 1] : authoredVoHoldMs(L.src) / 1000;
  setTimeout(()=>{ if(!done && live()){ stopAudio(); end(); } }, (last + 10) * 1000);
  const tick = ()=>{
    if(!live()) return;
    const a = currentAudio;
    const own = !!a && decodeURIComponent(String(a.currentSrc || a.src || "").split("/").pop()) === L.file;
    const t = own ? a.currentTime : (Date.now() - began) / 1000;
    const span = own && isFinite(a.duration) && a.duration > 0 ? a.duration : authoredVoHoldMs(L.src) / 1000;
    let n = 0;
    while(n < L.words.length && t + 0.04 >= (L.times ? L.times[n] : span * L.share[n])) n++;
    sfigShow(L, n);
    if(n < L.words.length) nextFrame(tick);
  };
  tick();
}

"""
story_mod = r"""  /* ===== [story-fig] STORY_LISTEN — the Figma story page, the first screen after the start gate's peek
     transition. It tells the story in BEATS on one layout (FLN-by-MJ frames 435:5, then 476:198): the picture
     sits in its grey-bordered frame and the beat's text arrives WORD BY WORD in the white box under it
     (sfigNarrate). When a beat's narration ends, after the engine's one-second beat (PACE.tail), its text
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
      const lines = beats.map((b, k)=> sfigLine(texts[k].querySelector("p"), b.text_hi, b.word_times, b.audio));

      state.ownsAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
      setSwMood("talk");
      const alive = ()=> fig.isConnected;
      let run = 0, cur = 0;
      const armNav = ()=>{ if(!alive()) return; setNavActive(true); setSwMood("point"); };
      const start = ()=>{
        const mine = ++run;
        setNavActive(false);   // a replay hides आगे until its narration has ended
        sfigNarrate(lines[cur], ()=> mine === run && alive(), ()=>{
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
     box comes in, and once it has landed the sentences are read with the story page's word-by-word reveal
     (sfigNarrate). Swiftie, the 🔊 chip, the card's box and आगे are the story page's. आगे only ever shows
     LIVE, when the sentences' narration ends; the 🔊 chip replays the sentences from their first word, hiding
     आगे again until that replay ends. ===== */
  STORY_RELISTEN: {
    mount(host, slide){
      const d = slide.data || {};
      const fig = sfigMount(host, '<div class="sfig-title"><p></p></div><div class="sfig-sbox"></div>' +
        '<div class="sfig-stext"><p></p><p>​</p></div>');
      const card = host.closest(".tut-card"); if(card) card.classList.add("sfig-round");
      const title = fig.querySelector(".sfig-title"), box = fig.querySelector(".sfig-sbox");
      title.querySelector("p").textContent = d.title_hi || "";
      const L = sfigLine(fig.querySelector(".sfig-stext p"), d.text_hi, d.word_times, d.audio);
      const introSrc = d.intro_audio ? ("assets/Audio/" + d.intro_audio + "." + AUDIO_EXT) : null;

      state.ownsAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
      setSwMood("talk");
      const alive = ()=> fig.isConnected;
      let run = 0;
      const armNav = ()=>{ if(!alive()) return; setNavActive(true); setSwMood("point"); };
      const readAll = ()=>{
        const mine = ++run;
        setNavActive(false);   // a replay hides आगे until its narration has ended
        sfigNarrate(L, ()=> mine === run && alive(), armNav);
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
     as the example's clip starts — every text WORD BY WORD on its clip's own clock (sfigNarrate), with a short
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
          beats.push({ L: sfigLine(row.querySelector(sel + " p"), p.text_hi, p.word_times, p.audio),
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
        beats.forEach(b=> sfigShow(b.L, 0));
        read(0, mine);
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
      const L = sfigLine(sentEl, S.text_hi, S.word_times, S.audio);
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
      // 2. the picture, the sentence bar (with its empty slot) and the tiles come in; once landed, the sentence is read
      //    without a pause, its words arriving one by one with the clip
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
      let live = false, reread = 0;
      function arm(){
        live = true; state.demoRunning = false; fig.classList.add("dmf-live");
        tiles.forEach((t, k)=>{ t.onclick = ()=> tap(k);
          t.onanimationend = (e)=>{ if(e.target === t && e.animationName === "wgNo") t.classList.remove("wiggle"); }; });
        // a punctuation-only word shares the start of the word before it ("हैं ।"): the two light together
        state.replayAudio = ()=>{ if(!live) return; const mine = ++reread;
          const hot = (n)=>{ if(mine !== reread) return; const t = n > 0 && L.times ? L.times[n - 1] : null;
            L.words.forEach((w, i)=> w.classList.toggle("hot", n > 0 && (L.times ? L.times[i] === t : i === n - 1))); };
          narrate(L.src, L.times || [], hot, ()=> hot(0)); };
      }
      function tap(k){
        if(!live || !alive()) return;
        if(isPlaying) stopAudio();   // a tap cuts the idle reminder short
        reread++; L.words.forEach(w=> w.classList.remove("hot"));
        const t = tiles[k], ok = k === pick, opt = opts[k] || {};
        GameBus.sendQuestionAnswered(slide, { is_correct: ok, score: ok && state.attempts === 0 ? 1 : 0, attempt: state.attempts + 1,
          ui_index: k, original_index: k, text: opt.name_hi || opt.mark || null });
        if(!ok){
          // a wrong tile wiggles, its colours unchanged, and stays tappable
          state.attempts++; sfxWrongSoft(); setSwMood("tryagain");
          GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
          t.classList.remove("wiggle"); void t.offsetWidth; t.classList.add("wiggle");
          return;
        }
        // the right one: pressed, the others dim, its mark lands in the slot as its name sounds; then the page moves on
        live = false; state.locked = true; state.demoRunning = true;
        blanks.forEach(b=> b.classList.remove("blink"));
        tiles.forEach((x, j)=>{ x.onclick = null; x.classList.remove("wiggle"); x.classList.add(j === pick ? "on" : "off"); });
        marks.forEach((m, j)=> after(j * (d.mark_stagger_ms || 300), ()=>{ centreInk(m); m.classList.add("in"); }));
        sfxCorrect(); confettiCannon(); setSwMood("happy");
        GameBus.emit("punct_build_done", { slide_id: slide.id, phase: slide.phase, value: true,
          first_try: state.attempts === 0, wrong: state.attempts, latency_ms: Date.now() - state.slideStart });
        narrate(A(d.mark_audio), [], ()=>{}, ()=> after(PACE.tail, ()=> completeSlide(true)));
      }
      // 4. the mark's name: its tile is tapped for the child, the others go dim; then the mark lands in the slot(s), one
      //    after the other (data.mark_stagger_ms apart) when there are several
      function stage4(){
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
       repeat; the chip replays it too. A tap on a pill cuts any line that is speaking.
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
      state.replayAudio = ()=>{ if(!hold && !reviewing && !state.locked) speakPrompt(false); };
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
      items.forEach(it=>{ it.cell.onclick = ()=> tap(it); });
      function tap(it){
        const guided = it.cell.classList.contains("opt-guided");
        if(!alive() || hold || reviewing || state.hintActive) return;
        if(["crossed", "correct", "opt-dim"].some(c=> it.cell.classList.contains(c)) || (state.locked && !guided)) return;
        stopNudge(); wordStop();
        if(isPlaying) stopAudio();   // a tap cuts whatever speaks (the instruction, the try-again line)
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
          play(audioFor(slide, "try_again"), ()=> it.cell.classList.remove("crossed"));
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
js = sub1(js, r"^SlideModules\.MATCH_PAIRS           = SlideModules\.MATCH_THE_PAIR;",
          lambda m: m.group(0) + "\nSlideModules.SORT_WORDS            = SlideModules.SORT_QTYPE;   // [reskin] generic two-box word sort (custom data.bins), r4n", re.M, "alias block")
js = sub1(js, r"^SlideModules\.SORT_WORDS .*$",
          lambda m: m.group(0) + "\nSlideModules.PUNCT_PICK            = SlideModules.PUNCT_DEMO;   // [pick-fig] G1: the run-on demo's page with the tap left to the child", re.M, "alias block (pick)")
js = sub1(js, r'  SEQUENCE_DRAG: "drag",',
          lambda m: m.group(0) + '\n  EVIDENCE_QA: "mcq", BUILD_PUNCT: "build", SORT_QTYPE: "drag", SORT_WORDS: "drag", PUNCT_PICK: "mcq", SENT_PICK: "mcq",   /* [reskin] this lesson\'s answerable types */', 0, "QUESTION_FORMAT")
# [sent-fig] G4, P1 + P2 (SENT_PICK) repeat their instruction after every 5 s of quiet itself (the reference P4's rule), so the engine's
# one-off 7 s idle reminder stays off there; and the stage carries .sent-page for P4's look (style.css [sent-fig])
js = sub1(js, r"if\(\['MATCH_THE_PAIR','MATCH_VACHAN_PAIRS','FILL_VACHAN_DRAG'\]\.includes\(",
          "if(['MATCH_THE_PAIR','MATCH_VACHAN_PAIRS','FILL_VACHAN_DRAG','SENT_PICK'].includes(", 0, "armIdleVo exclusions (sent)")
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
          '  const isTut = ((slide.phase === "tutorial" || slide.type === "PUNCT_PICK") && ', 0, "isTut (pick)")
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
@font-face{font-family:'Story Noto Sans Devanagari';font-style:normal;font-weight:600;font-display:block;
  src:url("assets/UI/story_font_nsd600_deva.woff2") format("woff2");
  unicode-range:U+0900-097F,U+1CD0-1CF4,U+1CF7-1CF9,U+200C-200D,U+20A8,U+20B9,U+20F0,U+25CC,U+A830-A839,U+A8E0-A8FF,U+11B00-11B0A;}
@font-face{font-family:'Story Noto Sans Devanagari';font-style:normal;font-weight:600;font-display:block;
  src:url("assets/UI/story_font_nsd600_latin.woff2") format("woff2");
  unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD;}
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
.sfig-img.b1{left:-3px;top:-11px;width:436px;height:245px;}    /* node 470:477 (frame 435:5) */
.sfig-img.b2{left:-9px;top:-14px;width:448px;height:252px;}    /* node 476:197 (frame 476:198) */
.sfig-img:not(.on){visibility:hidden;}
/* the next beat's picture appears over the last one: fades up from a slight zoom and settles into its crop */
.sfig-img.enter{animation:sfigPicIn .65s cubic-bezier(.2,.8,.3,1) both;}
@keyframes sfigPicIn{from{opacity:0;transform:scale(1.08);}to{opacity:1;transform:none;}}
.sfig-textbox{position:absolute;left:314px;top:250px;width:436px;height:119px;background:#FFFFFF;border-radius:20px;
  box-shadow:0 4px 19.7px rgba(177,177,177,.25);}   /* node 436:412 */
.sfig-text{position:absolute;transform:translateY(-50%);overflow-wrap:break-word;
  font-family:'Story Noto Sans Devanagari',var(--font-hi);font-weight:600;font-size:24px;line-height:normal;
  color:#002F76;text-align:center;}
.sfig-text.b1{left:328px;top:310px;width:408px;}    /* node 475:195: centred on 532,310 */
.sfig-text.b2{left:340px;top:309.5px;width:384px;}  /* node 476:384: centred on 532,309.5 */
.sfig-text.b1 p::before{content:"\\a0";}        /* frame 435:5's text starts with a space, which sets line 1 half a space right */
.sfig-text.gone{opacity:0;visibility:hidden;transition:opacity .3s ease-out,visibility 0s .3s;}   /* a finished beat's text leaves */
/* Swiftie at the reference's 76,472 190x190 on the stage (in .sfig-in's frame px) */
.sfig-swiftie{position:absolute;left:calc(64px / var(--fig-s) - 96px);top:calc(460px / var(--fig-s) - 106px);
  width:calc(190px / var(--fig-s));height:calc(190px / var(--fig-s));object-fit:cover;}
/* word-by-word: every word keeps its place from the start, so the lines never reflow as words arrive */
.sfig-w{display:inline-block;opacity:0;transform:translateY(8px) scale(.92);
  transition:opacity .22s ease-out,transform .26s cubic-bezier(.2,.9,.3,1.25);}
.sfig-w.on{opacity:1;transform:none;}
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
  font-family:'Story Noto Sans Devanagari',var(--font-hi);font-weight:600;font-size:64px;line-height:normal;
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
  justify-content:flex-end;overflow-wrap:break-word;font-family:'Story Noto Sans Devanagari',var(--font-hi);
  font-weight:600;font-size:28px;line-height:37px;color:#002F76;text-align:center;}
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
.rcf-mark{position:absolute;width:483px;transform:translate(-50%,-50%);font-family:'Story Noto Sans Devanagari',var(--font-hi);
  font-weight:600;font-size:64px;line-height:normal;color:#002F76;text-align:center;white-space:pre;}
.r1 .rcf-mark{left:43.5px;top:47.5px;} .r2 .rcf-mark{left:46.5px;top:48.5px;} .r3 .rcf-mark{left:46.5px;top:53.5px;}
/* names and uses: nodes 520:260-262 and 514:8 / 517:24 / 517:25 — 1075-wide centred boxes, 48 tall, 28px, #012F76:
   centred on x 372.5 / 372.5 / 380.5 and 633.5, tops 148 / 275 / 414 and 148 / 278 / 414 (card px). The line box is
   Baloo Bhai 2's, not Noto's: 1.714 x 28 = 48px (the nodes' height), with the fallback glyphs centred in it. The spaces
   are Baloo Bhai 2's too, 2px narrower than Noto's at this size (the render's words sit that much closer; measured by
   pixel-matching the render over SemiBold/-0.5..-4px, see the README) */
.rcf-name, .rcf-when{position:absolute;width:1075px;height:48px;transform:translateX(-50%);
  font-family:'Story Noto Sans Devanagari',var(--font-hi);font-weight:600;font-size:28px;line-height:48px;word-spacing:-2px;color:#012F76;text-align:center;}
.r1 .rcf-name{left:360.5px;top:136px;} .r2 .rcf-name{left:360.5px;top:263px;} .r3 .rcf-name{left:368.5px;top:402px;}
.r1 .rcf-when{left:621.5px;top:136px;} .r2 .rcf-when{left:621.5px;top:266px;} .r3 .rcf-when{left:621.5px;top:402px;}
/* the examples' yellow boxes: nodes 514:12 / 518:26 / 519:28 at 790,143 163x49 / 790,274 262x49 / 790,405 191x49
   (card px), 8px corners, clipping; their text 22px, centred, 7 / 8 / 9 px from the top, in Baloo Bhai 2's line box
   (1.714 x 22 = 38px, Figma's rounding; the render's glyphs sit 1px lower than that box centred in Chrome, hence
   8 / 9 / 10) and with Baloo Bhai 2's spaces, 2px narrower than Noto's. 514:10 starts with a space, which Figma
   counts (as on T0's first line) */
.rcf-eg{position:absolute;left:778px;height:49px;background:#FFF1B6;border-radius:8px;overflow:hidden;opacity:0;transform:scale(.9);}
.r1 .rcf-eg{top:131px;width:163px;} .r2 .rcf-eg{top:262px;width:262px;} .r3 .rcf-eg{top:393px;width:191px;}
.rcf-eg p{position:absolute;left:50%;width:1075px;height:48px;transform:translateX(-50%);
  font-family:'Story Noto Sans Devanagari',var(--font-hi);font-weight:600;font-size:22px;line-height:38px;word-spacing:-2px;color:#012F76;text-align:center;}
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
  font-family:'Story Noto Sans Devanagari',var(--font-hi);font-weight:600;font-size:32px;line-height:55px;word-spacing:-2px;color:#012F76;}
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
  font-family:'Story Noto Sans Devanagari',var(--font-hi);font-weight:600;font-size:64px;line-height:110px;word-spacing:-4px;color:#012F76;}
.dmf-sent .sfig-w{border-radius:10px;transition:opacity .22s ease-out,transform .26s cubic-bezier(.2,.9,.3,1.25),background-color .15s,box-shadow .15s;}
.dmf-sent .sfig-w.hot{background:#FFF1B6;box-shadow:0 0 0 6px #FFF1B6;}   /* the word being read */
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
  font-family:'Story Noto Sans Devanagari',var(--font-hi);font-weight:600;font-size:64px;line-height:normal;color:#012F76;
  transition:opacity .35s ease-out,transform .45s cubic-bezier(.2,.9,.3,1.3);}
.dmf-blank .dmf-mark.in{opacity:1;transform:translate(calc(-50% - var(--ix)),calc(-50% - var(--iy)));}
.dmf-blank.hot{box-shadow:0 0 0 6px rgba(56,106,246,.22);}                            /* the mark being named */
.dmf-blank.hot .dmf-dash{stroke:#386AF6;stroke-dasharray:none;}
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
.dmf-sym{position:absolute;width:483px;transform:translate(-50%,-50%);text-align:center;white-space:pre;
  font-family:'Story Noto Sans Devanagari',var(--font-hi);font-weight:600;font-size:64px;line-height:normal;color:#002F76;}
.t1 .dmf-sym{left:111.5px;top:58.5px;} .t2 .dmf-sym{left:113.5px;top:49.5px;} .t3 .dmf-sym{left:113.5px;top:59.5px;}
.dmf-name{position:absolute;left:113.5px;width:1075px;height:48px;transform:translateX(-50%);text-align:center;
  font-family:'Story Noto Sans Devanagari',var(--font-hi);font-weight:600;font-size:28px;line-height:48px;word-spacing:-2px;color:#012F76;}
.t1 .dmf-name{top:100px;} .t2 .dmf-name{top:101px;} .t3 .dmf-name{top:101px;}
/* tapped for the child: the face presses down and comes back, its colours unchanged (no blue selection ring,
   2026-10-25); the other tiles dim = the engine's faded option */
.dmf-tile.on .dmf-face{animation:dmfTap .45s ease-out;}
@keyframes dmfTap{0%{transform:none;}35%{transform:translateY(6px);}100%{transform:none;}}
.dmf-tile.off{opacity:.35;filter:saturate(.6);transition:opacity .3s,filter .3s;}
/* [pick-fig] G1 (frame 525:354 "7 G1", PUNCT_PICK): the tiles are the child's once the sentence has been read; a wrong
   one shakes with the engine's own wrong-answer wiggle (wgNo, one --fx-beat), its colours unchanged */
.dmf-live .dmf-tile{cursor:pointer;}
.dmf-tile.wiggle{animation:wgNo var(--fx-beat) ease-in-out both;}
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
.stage.sent-page #promptText{font-weight:800;line-height:1.15;color:#0B3D8C;}
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
  box-sizing:border-box;padding:10px 12px;font-family:var(--font-hi);font-size:28px;font-weight:800;line-height:1.2;color:var(--navy);
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
       + feedback_rules + fit_rules + title_css + story_css + recap_css + demo_css + sent_css)

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
assert len(title_files) == 10, f"expected 10 title assets in {TITLE_SRC}, found {len(title_files)}"
for f in title_files:
    dst = DIST / "assets" / "UI" / f.name
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7b. [story-fig] the story page's assets (kept next to this script, in story_assets/) ----------
STORY_SRC = SCR / "story_assets"
for name, sub in (("story_grid.svg", "UI"), ("story_font_nsd600_deva.woff2", "UI"), ("story_font_nsd600_latin.woff2", "UI"),
                  ("img_story_chintu.webp", "Images"), ("vo_story_s1.ogg", "Audio"),
                  ("img_story_chintu_2.webp", "Images"), ("vo_story_s2.ogg", "Audio"),
                  ("vo_story_r0.ogg", "Audio"), ("vo_story_r1.ogg", "Audio")):
    f, dst = STORY_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing story asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

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
for name, sub in [(f"vo_demo2_{k}.ogg", "Audio") for k in DEMO2_KEYS] + [("img_demo2_boy.webp", "Images")]:
    f, dst = DEMO2_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing demo asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7f. [demo-fig] T4's clips and picture (demo3_assets/: recap_vo.py demo3; the frame's "image 230"; its head is
#               byte-for-byte T2's demo1_head.webp) ----------
DEMO3_SRC = SCR / "demo3_assets"
for name, sub in [(f"vo_demo3_{k}.ogg", "Audio") for k in DEMO3_KEYS] + [("img_demo3_fruits.webp", "Images")]:
    f, dst = DEMO3_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing demo asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7g. [pick-fig] G1's clips and picture (g1_assets/: recap_vo.py g1; the frame's "image 231"; its head is
#               byte-for-byte T2's demo1_head.webp; the name on the right tap is T2's vo_demo1_purn) ----------
G1_SRC = SCR / "g1_assets"
for name, sub in [(f"vo_g1_{k}.ogg", "Audio") for k in G1_KEYS] + [("img_g1_boy_ball.webp", "Images")]:
    f, dst = G1_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing G1 asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)
# ---------- 7h. [pick-fig] G2's sentence clip and picture (g2_assets/: recap_vo.py g2; the frame's "image 239"; its title bar is
#               T4's to the pixel, its instruction G1's vo_g1_intro, its name on the right tap T3's vo_demo2_prashn) ----------
G2_SRC = SCR / "g2_assets"
for name, sub in (("vo_g2_sent.ogg", "Audio"), ("img_g2_boy_bag.webp", "Images")):
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
for name, sub in [(f"vo_g4_{k}.ogg", "Audio") for k in G4_KEYS] + [("img_g4_kite_gry.webp", "Images")]:
    f, dst = G4_SRC / name, DIST / "assets" / sub / name
    assert f.exists(), f"missing G4 asset {f}"
    if not dst.exists() or dst.read_bytes() != f.read_bytes(): shutil.copy2(f, dst)

# ---------- 7k. [sent-fig] P1's and P2's clips and pictures (<page>_assets/: recap_vo.py <page>; the picture = g4_picture.py over
#               the user's picture, <page>_*_source.png; their title + try-again clips are G4's) ----------
for page, image_id in (("p1", "img_p1_book_gry"), ("p2", "img_p2_pencils_gry")):
    for name, sub in [(f"vo_{page}_{k}.ogg", "Audio") for k in SENT_OPT_KEYS] + [(f"{image_id}.webp", "Images")]:
        f, dst = SCR / f"{page}_assets" / name, DIST / "assets" / sub / name
        assert f.exists(), f"missing {page.upper()} asset {f}"
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
