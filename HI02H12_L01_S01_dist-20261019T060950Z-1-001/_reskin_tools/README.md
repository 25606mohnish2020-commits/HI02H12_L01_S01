# Re-skin tooling — HI02H12_L01_S01 on the Ek-aur-Anek chrome

`HI02H12_L01_S01_dist/` was rebuilt on 2026-10-19 so its landing, header, buttons, dev nav,
phase-transition gate and end screen are the ones from
https://github.com/siddharthsharma-ctrl/Ek-aur-Anek (`HI02H11_L03_S01_poem.html`).

How the build is put together
- Base = the reference's CSS, body markup and engine JS (`2026.07.28t-r4-unified`).
- Ported into it = this lesson's four modules (QTYPE_RECAP, BUILD_PUNCT, EVIDENCE_QA, SORT_QTYPE/SORT_WORDS),
  their `ev*` helpers and CSS, plus card.json and the lesson's own audio/images.
- The three PHASE_TRANSITION journey-map slides were dropped from the card: the reference flow uses the
  engine's peek gate (Swiftie + "चलिए, साथ में करें!" + `vo_pt_*`) between rounds instead.
- The originals of `index.html`, `style.css`, `app.js` are in `../_before_reskin/`. Assets were only added,
  never overwritten, so restoring those three files restores the old game.

Title page (added 2026-10-19)
- The landing is the Figma "Title Page" frame (FLN-by-MJ, node 386:17):
  https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=386-17
  It is built in the frame's own 1280x720 px and scaled once (1333/1280) onto the stage, so every element
  keeps the frame's placement and size. Assets are in `title_assets/` (copied into `assets/UI/title_*`);
  `title_assets_figma_render_1280x720.png` is Figma's own render, used as the visual target.
- The play button and the 🔊 chip are not in the frame; they keep their engine size and behaviour.
- The drifting star layer is switched off on the title page only (the frame's background already has its
  stars); it still runs on the end screen.
- Swiftie rests on the frame's "Hello" still and waves (new_landing_swiftee_anim.webp, frame 0 = that still)
  only while the landing greeting is sounding, then returns to the still the moment it stops.
- `python -I title_check.py ../HI02H12_L01_S01_dist/index.html title_assets_figma_render_1280x720.png out`
  checks every element's box against the frame, pixel-diffs against the Figma render, and logs Swiftie vs VO.

Story page (added 2026-10-20)
- Flow: title page -> शुरू करें -> the tutorial peek gate (pink "चलिए, शुरू करें!" + Swiftie peeking) -> the
  story page -> T1 (the three-marks recap) and on, unchanged.
- The story page is the Figma frame "html_Guided_instructions" (FLN-by-MJ, node 435:5):
  https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=435-5
  build.py inserts it as slide T0 (type STORY_LISTEN, phase tutorial) and adds the module + the [story-fig] CSS.
  The tutorial card takes the frame's card geometry; inside it everything is in the frame's own px, scaled
  1333/1280 like the title page. Note: the picture's 4px grey stroke is OUTSIDE its 430x224 frame in Figma
  (the code export draws it inside); the frame's text starts with a space, which is kept (line 1 sits half a
  space right). Text = Noto Sans Devanagari SemiBold 24px, bundled as two woff2 subsets.
- Two beats on the one layout (added 2026-10-21): line 1 = frame 435:5, then line 2 = frame 476:198
  (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=476-198) — only the picture (and its
  crop) and the text block differ. One second (PACE.tail) after line 1's VO ends, its text fades out and
  picture 2 fades up over picture 1 from a slight zoom (0.65 s); line 2's VO starts once it has landed.
  आगे appears (pulsing, as on every page) only when line 2's VO has ended. The 🔊 chip is ignored during the
  turn and afterwards replays line 2.
- आगे on this page never shows the engine's greyed-out pill (2026-10-21): it is hidden while any story VO
  sounds — including a 🔊 replay — and appears live + pulsing when line 2's VO ends. Each line has its own
  watchdog (last word start + 10 s): a clip that never reports its end is stopped, so even then आगे opens live.
  story_check.py logs the pill frame by frame and simulates that stall.
- Card size, Swiftie and the 🔊 chip follow the reference game's T1/T2 (2026-10-21,
  https://hi-02-h04-l01-s01-dun.vercel.app/, measured on its 1333x750 stage): card 100,96 1133x562, Swiftie
  76,472 190x190 (its start_mascot.webp is the same Hello art as title_swiftie_hello.png), chip 202,606 58x58.
  The picture, text box and grid did NOT move (.sfig-in keeps the frame's place; only the clip grew). The card
  keeps the frame's look (12px #5A8FEE border, 40px x 1333/1280 corners, shadow) — only its box changed.
- Each line's text appears word by word: card data.beats[i].word_times holds each word's start in that
  line's clip, read against the clip's own currentTime.
- Assets are in `story_assets/` (copied into assets/UI, assets/Images, assets/Audio by build.py);
  `story_figma_render_1280x720.png` / `story2_figma_render_1280x720.png` are Figma's own renders of the two
  frames, used as the visual targets.
- The VO clips `vo_story_s1.ogg` / `vo_story_s2.ogg` are SYNTHESISED (edge-tts hi-IN-SwaraNeural, rate -15% to
  match the game's pace) — placeholders until the VO team records them. `python -I -X utf8 story_vo.py s1|s2`
  regenerates ONE line + its timings (needs edge-tts >= 7.3; 7.2.x gets HTTP 403). For a human recording: drop
  it in as `story_assets/vo_story_<line>.ogg`, run `python -I -X utf8 align_story_vo.py <line> --write`
  (faster-whisper word timestamps), then rebuild.
- `python -I -X utf8 story_check.py ../HI02H12_L01_S01_dist/index.html story_figma_render_1280x720.png
  story2_figma_render_1280x720.png out` checks the flow, both lines' word-vs-VO sync, the turn, when आगे
  appears, and at the end of each beat every element's box + the pixel diff vs that frame's Figma render.
- `../_before_story/` holds the dist's index.html / style.css / app.js from before the story page;
  `../_before_story_beat2/` from before line 2 was added (the one-line story page);
  `../_before_story_nav/` from before the "never a greyed-out आगे" change;
  `../_before_story_ref_layout/` from before the card / Swiftie / chip took the reference game's geometry.

Read-again page T0B "आइए वाक्य सुनें।" (added 2026-10-21)
- Flow: ... -> story page T0 -> T0B -> T1 (unchanged). Figma frame 488:190
  (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=488-190), type STORY_RELISTEN.
- The title (Noto Sans Devanagari SemiBold 64px) appears the moment the intro VO `vo_story_r0`
  ("अब इन्हीं वाक्यों को फिर से सुनते हैं।") starts to sound — on the clip's own clock, not the earlier "playing"
  event. When that line ends the sentence box comes in (0.5 s), and once it has landed (0.65 s) `vo_story_r1`
  reads the punctuated sentences (SemiBold 28px) with T0's word-by-word reveal. आगे appears live + pulsing only
  when that VO ends; the 🔊 chip is ignored until the sentences start, then replays them.
- The card is this frame's own (node 488:367, 2026-10-21 second pass: "this exact figma layout and placement"):
  96,106 1088x508 x 1333/1280 = 100,110.39 1133x529 on the stage, 64px corners — so it is shorter than T0's
  reference-sized card. Its content (.sfig-in: title, sentence box, grid) sits exactly on the frame's padding box.
  Swiftie (76,472 190x190), the 🔊 chip (202,606 58x58) and आगे (567.5,522) stay at T0's screen positions, as asked,
  so Swiftie and the chip overhang this card's bottom-left edge a little more than on T0. The grid nodes 488:368 /
  488:369 land exactly where T0's 435:180 / 435:181 do.
- The sentence box and its text follow the frame as updated in Figma on 2026-10-21 afternoon (third pass: "the exact
  same dialoguebox ... and the updated text"): node 488:371 is, in the frame's fifth version (2026-10-21 evening),
  683x219 at 191,144 (centred on 532.5) with its 4px stroke OUTSIDE (render 691x227 at 187,140) and 20px corners
  (24px on the stroke's outer edge), and the title's centre moved to y 62.5, then to 65.5 in the sixth version
  (fourth version: box 636x234 at 214,129, title centre 59.5 — render archived as `*_v3_2026-10-21.png`, build in
  `../_before_relisten_box2/`; fifth: render `*_v4_2026-10-21.png`, build in `../_before_relisten_title/`); node 488:374 is
  631x280 centred on 532.5, bottom-aligned on y 369, four lines — the frame's fourth version (2026-10-21 evening)
  put "चिंटू" back at the start of the first sentence and widened the text block; the third version's render and
  clip are archived as `*_v2_2026-10-21.*`. The frame's first sentence has a space before its danda ("है ।”"):
  that danda is its own word span, timed with "है" (story_vo.py gives a punctuation-only token the previous word's
  time), so the page shows exactly the frame's text. The earlier box (552x205 at 256,134) and text are in the
  archived render `relisten_figma_render_1280x720_v1_2026-10-21.png` and clip `vo_story_r1_v1_2026-10-21.*`.
  Sentence line height is set to 37px: the font's normal is 1.304em and Figma rounds 28 x 1.304 to 37, Chrome to 36
  (the title's 83px is the same in both).
- T0 and T0B share helpers in app.js (sfigMount / sfigLine / sfigNarrate); T0's output was checked identical.
- Both clips are SYNTHESISED like T0's (`story_vo.py r0|r1`; `align_story_vo.py r0|r1`). For r1 the
  synthesiser's word starts are the right ones: whisper puts a few words that follow a long pause inside the
  silence (checked against the clip's energy).
- `python -I -X utf8 relisten_check.py ../HI02H12_L01_S01_dist/index.html relisten_figma_render_1280x720.png out`
  checks the timing (in-page, every frame), the card vs the frame and Swiftie/chip/आगे vs T0, the frame's
  geometry/line breaks/fonts, and pixel diffs vs Figma's render over the title + box and over the whole card (less
  Swiftie/chip/आगे; there it counts only SOLID diffs, since a 1-px anti-alias line along the border's edges is
  expected). `../_before_story_relisten/` holds the files from before T0B; `../_before_relisten_card/` from before
  T0B's card took the frame's box (it had T0's); `../_before_relisten_box/` (plus that version's vo_story_r1.ogg)
  from before the sentence box, text and VO followed the updated frame; `../_before_relisten_text3/` from before the
  text took the frame's fourth version ("चिंटू" back, wider text block).

Three-marks recap T1 "ये हैं तीन विराम चिह्न" (replaced 2026-10-24)
- Flow: ... -> T0B -> T1 -> T2 (unchanged). Figma frame 508:2
  (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=508-2), type MARKS_RECAP, in place of the
  ported QTYPE_RECAP cards (that module stays in app.js, unused; its clips vo_rc_* stay in assets/Audio, unreferenced).
- The card, grid, Swiftie (76,472 190x190) and 🔊 chip (202,606 58x58) are T0B's: the frame's card is the same box
  (96,106 1088x508, 64px corners, so the .sfig-round rules apply unchanged) and Swiftie + chip were asked to stay where
  the earlier pages have them (the frame's own Swiftie is 245px at 35,415). आगे is not in the frame and the rows fill the
  card down to the third example, so it is centred in the gap under the card (567.5,650 198x90 on the stage): T0's place
  for it (522, inside the card) would sit on "सवाल पूछने पर".
- Everything else is the frame's, in .sfig-in's frame px (= card px - 12): the title (node 508:184, Noto Sans Devanagari
  SemiBold 64px, centred on 544.5,64.5); the marks' boxes 93x90 at 166,127 / 256 / 385 with their 4px stroke OUTSIDE
  (render 101x98 at 162,123 ...) and 10px corners; the marks 64px centred on 209.5,174.5 / 212.5,304.5 / 212.5,438.5 —
  node 512:3 is "। " with a trailing space that Figma does NOT count when centring (the render's danda sits on the
  node's centre), so it is dropped; names / uses (520:260-262, 514:8, 517:24, 517:25) 28px #012F76 centred on x 372.5 /
  372.5 / 380.5 and 633.5, tops 148 / 275 / 414 and 148 / 278 / 414; the yellow boxes (514:12, 518:26, 519:28) #FFF1B6 at
  790,143 163x49 / 790,274 262x49 / 790,405 191x49, 8px corners, their 22px text 7 / 8 / 9 px from the top (8 / 9 / 10
  here, see fonts); node 514:10 " रीना स्कूल गई ।" keeps its leading space, which Figma counts (as on T0's first line).
- Fonts: the labels are "Baloo Bhai 2 SemiBold" in the frame — a font with NO Devanagari glyphs — so Figma renders them
  in its Noto Sans Devanagari fallback at SemiBold (of 400/500/600/700 only 600 reproduces the render's glyph widths,
  and pixel-matching the render over weight x word-spacing x nudge picks 600 too): they use the bundled 'Story Noto Sans
  Devanagari' 600. What Baloo Bhai 2 still sets: the LINE BOX (1.714em: 48px at 28px = the nodes' height, 38px at 22px;
  Noto's own "normal" puts the glyphs 6px / 4.5px too high) and the SPACES (its space is 2px narrower than Noto's at
  both sizes -> word-spacing:-2px; without it the uses come out 5-6px too wide). The examples' glyphs sit 1px lower in
  the render than Chrome's centring of the 38px box, hence tops 8 / 9 / 10. Result: every text's ink within 1px of the
  render, 14 solid differing pixels over the whole card.
- Timing: the title appears the moment the intro clip starts to sound (as T0B's); 0.7 s after it ends the nine beats
  follow — for each mark its name (the box + mark pop in as the clip starts), its use, its example (the yellow box pops
  in as the clip starts) — each text word by word on its clip's clock (sfigNarrate), 0.3 s between beats and 0.7 s
  before the next mark (~27 s in all). आगे only ever shows live, when the last example has been read; the 🔊 chip is
  ignored while the marks are being read (state.demoRunning) and afterwards reads the three marks again from the first
  (boxes staying, words re-arriving), with आगे hidden meanwhile.
- VO: ten SYNTHESISED clips (`python -I -X utf8 recap_vo.py recap all|<line>` with edge-tts >= 7.3 in a venv — the same voice
  and pace as the story pages; the synthesiser's ~1.1 s tail of silence is cut to 0.3 s) in recap_assets/ -> assets/Audio/
  vo_recap_*.ogg: intro "आइए समझते हैं कि कौन-से चिह्न का प्रयोग कब किया जाता है ।", then per mark the name ("पूर्ण विराम"),
  the use ("बात पूरी होने पर") and the example ("उदाहरण- रीना स्कूल गई ।" — SAYS "उदाहरण-", SHOWS the sentence; the shown
  words' times are the synthesiser's boundaries, a punctuation-only token "।" / "?" showing with the word before it).
  Placeholders until the VO team records them. The lesson already has human clips of the three names (vo_nm_purn /
  vo_nm_alp / vo_nm_prashn) — not used, so that the page keeps one voice until everything is recorded; to use them,
  point the three name parts at those ids in build.py and give them timings. For a human recording: drop it in as
  recap_assets/vo_recap_<line>.ogg, `python -I -X utf8 align_story_vo.py recap_<line> --write`, rebuild.
- `python -I -X utf8 recap_check.py ../HI02H12_L01_S01_dist/index.html recap_figma_render_1280x720.png out` checks the
  timing in-page every frame (title vs the intro, every beat's box and words vs its clip, the breaths, the two chip
  taps, आगे, the replay, आगे -> T2), the card / Swiftie / chip / आगे boxes, every element vs the frame, the fonts, each
  text's ink vs the Figma render and the pixel diffs. `recap_figma_render_1280x720.png` is Figma's own render of the
  frame. `../_before_recap_fig/` holds the dist's three files from before (T1 = the ported QTYPE_RECAP cards).

Run-on sentence demo T2 "सुनो यह वाक्य बिना रुके पढ़ा गया ।" (replaced 2026-10-24)
- Flow: ... -> T1 -> T2 -> T3 (unchanged; T3 / T4 are still the ported BUILD_PUNCT auto demos). Figma frame 519:32
  "G3 guided story question" (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=519-32), type
  PUNCT_DEMO, in place of the ported BUILD_PUNCT auto demo on this slide (its data — "रीना स्कूल गई वह खुश थी" with two
  dandas, vo_demo_q / vo_ro_d1 / vo_d1_explain / vo_ok_d1 / vo_d1_conclude — is no longer used; the clips stay in assets/Audio).
- The frame has NO card: its title bar, picture, sentence bar and mark tiles sit on the plain #F2F7FA stage. So the
  tutorial card loses its box (.sfig-full: no border, no background, the stage's padding 0) and .sfig-in is the whole
  1280x720 frame x 1333/1280. No standing Swiftie and no 🔊 chip on this page (2026-10-25, as asked — the first build
  kept T0's, which put two Swifties on screen and the wing over the first tile): the frame's only Swiftie is the head in
  its title bar. There is no आगे: the page advances by itself.
- Everything else is the frame's, in frame px: the title bar group 519:206 (36,26 1244x120, drop shadow 0 4px 2px
  25%): the pill 519:208 (3.897,18 1214.103x84, #CBE8FF, 4px white border INSIDE, stadium), its text 519:209 (32px,
  left-aligned at 139.55,18 in the pill, Baloo Bhai 2's 55px line box and -2px spaces; its trailing space not counted)
  and the Swiftie head 519:211 (116.513x120, #61D0FE, 5px #FDF9E9 ring inside, stadium, clipping the frame's 165px
  "Happy" bitmap at -16,5 — bundled as assets/UI/demo1_head.webp; it is not one of the engine's head poses); the picture
  box 521:285 (197,211 144x139, 2.386px #D5D8DF border inside, 14.316px corners) with "image 228" (80.052x120 at 227,221
  — a different girl from the lesson's img_school, bundled as assets/Images/img_demo1_girl.webp); the sentence bar
  519:218 (365,211 719x139, the same box, clipping), its text 519:223 (64px, a 479-wide centred box at 100,18 in the
  bar, Baloo Bhai 2's 110px line box, -4px spaces) and the empty slot 520:231 (59x100 at 583,20 in the bar, #FFF1B6,
  8px corners, 2px dashed rgba(86,86,86,.85) inside — an SVG stroke, dashes 10 on / 5 off as measured on the render,
  since a CSS dashed border's dashes cannot be set); the tiles (group 521:287): a #D9D9D9 base 227x169 at 197 / 527 /
  857, 443 (13.31px corners) under a white face 223x161 at +2,+2 (2.386px #D5D8DF border inside, 14.316px corners),
  the mark (64px Noto SemiBold, centred on 308.5,501.5 / 640.5,492.5 / 970.5,502.5 — 520:263's trailing space not
  counted) and the name (28px, centred on 310.5 / 640.5 / 970.5, tops 543 / 544 / 544, 48px line box, -2px spaces).
  All strokes on this frame are INSIDE their boxes (checked on the render). Pixel diff vs the render: 0.29% of the
  frame differs (glyph anti-aliasing), no solid differences.
- Timing: the title bar appears the moment the intro clip ("आइए कुछ वाक्यों के उदाहरण से समझते हैं ।") starts to sound;
  0.5 s after it ends the picture, the bar (with its empty slot) and the tiles come in, and once landed (0.65 s) the
  sentence "रीना स्कूल जा रही है" is read without a pause, its words arriving one by one with the clip; the moment that
  clip ends the slot blinks for 3.5 s (data.blink_ms) — three slow blinks of 1.17 s (2026-10-25; it was seven of 0.5 s);
  then "पूर्ण विराम" sounds while its tile is tapped for the child (the face presses down and comes back, its colours
  unchanged — no blue ring, 2026-10-25) and the other two go dim (the engine's faded look); 0.4 s after that line the
  mark lands in the slot, its INK on the slot's centre: Noto's danda sits 2.89px right of and 4.49px above its own
  line box's centre, so the module measures that offset from the font (canvas measureText) and shifts the mark by it,
  and the highlight's grow scales about the same point (the first build centred the line box, leaving the danda 2.5px
  right and 4.5px high); 0.7 s later the sentence is read again, "रीना स्कूल जा रही है, पूर्णविराम।", every tile dim,
  each word highlighted (yellow) as it is read and then the mark (blue ring, the mark grows); 1.5 s after that clip
  (data.hold_ms) the slot's box goes — the mark stays in the sentence — and 0.6 s later the page advances to T3 by
  itself. Each clip has the watchdog of the other Figma pages.
- VO: four SYNTHESISED clips (`python -I -X utf8 recap_vo.py demo1 all|<line>`, the same voice, tails trimmed) in
  demo1_assets/ -> assets/Audio/vo_demo1_*.ogg: intro, sent ("रीना स्कूल जा रही है", 5 word times), purn ("पूर्ण विराम";
  the lesson's human vo_nm_purn says the same and could replace it — see T1's note on keeping one voice), full
  ("रीना स्कूल जा रही है, पूर्णविराम।": 5 word times + the mark's). Placeholders until recorded; for a human recording:
  drop it in as demo1_assets/vo_demo1_<line>.ogg, `align_story_vo.py demo1_<line> --write`, rebuild.
- `python -I -X utf8 demo_check.py ../HI02H12_L01_S01_dist/index.html demo1_figma_render_1280x720.png out T2` checks the
  whole timeline in-page every frame (bar vs the intro, the boxes, the words vs the clip, the blink's length, pace and
  silence, the tap — colours unchanged — and the dimming, the mark, the second reading's highlights vs the clip, the box
  going, the self-advance to T3, no आगे), no Swiftie / chip, every element vs the frame, the fonts, each text's ink vs
  the render, the pixel diffs, and the danda's ink centred in the slot when landed and when highlighted.
  `../_before_demo_fixes/` holds the dist's three files from before the 2026-10-25 fixes. `demo1_figma_render_1280x720.png` is Figma's own render of the frame.
  `../_before_demo_fig/` holds the dist's three files from before (T2 = the ported BUILD_PUNCT auto demo).

Run-on sentence demo T3 "तुम्हारा नाम क्या है" (replaced 2026-10-25)
- Flow: ... -> T2 -> T3 -> T4 (unchanged; T4 is still the ported BUILD_PUNCT auto demo). Figma frame 521:288 "5 T3"
  (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=521-288), PUNCT_DEMO like T2, in place of the
  ported auto demo on this slide (its data — "तुम्हारा क्या नाम है" with vo_demo_q / vo_ro_d2 / vo_d2_explain / vo_ok_d2 /
  vo_d2_conclude / vo_mk_prashn — is no longer used; the clips stay in assets/Audio).
- The frame is T2's to the pixel except three things (the two renders differ only inside x 225..936, y 215..341):
  the sentence 521:300 "तुम्हारा नाम क्या है" (its 479-wide text box at 120,18 in the bar, not 100), the picture "image
  229" 523:318 (a boy, 130x128 at 204,215 — bundled as assets/Images/img_demo2_boy.webp) and the correct mark, "?".
  The title bar (text and its Swiftie head — byte-for-byte T2's bitmap, so demo1_head.webp is reused), the picture
  box, the sentence bar, the slot and the three tiles are T2's. The module takes the two differing boxes from
  data.layout (sent_x; img [x, y, w, h], frame px); T2's data has no layout, so T2 keeps the CSS's 519:32 boxes and
  is unchanged. Everything from T2's 2026-10-25 fixes holds here too: no standing Swiftie or 🔊 chip, three slow
  blinks, no blue on the tapped tile, the mark's INK centred in the slot (the "?" is measured the same way as the danda:
  its ink sits 7.5px above its line box's centre).
- Flow = T2's, step for step: the title bar on the intro line; the picture, bar and tiles; "तुम्हारा नाम क्या है" read
  without a pause, word by word; the slot blinks 3.5 s; "प्रश्नवाचक चिह्न" sounds as its tile (the third) is tapped and the
  other two dim; the "?" lands in the slot; the sentence is read again with the mark named, each word and then the "?"
  highlighted as they are read; 1.5 s later the slot's box goes and the page moves on to T4 by itself (no आगे).
- VO: four SYNTHESISED clips (`python -I -X utf8 recap_vo.py demo2 all|<line>`, T2's voice, tails trimmed) in
  demo2_assets/ -> assets/Audio/vo_demo2_*.ogg: intro = the title bar's own line, "सुनो, यह वाक्य बिना रुके पढ़ा गया ।"
  (T2's intro, "आइए कुछ वाक्यों के उदाहरण से समझते हैं", opens the examples, so it is not repeated here; the lesson's
  human vo_demo_q says this same line and could replace it); sent "तुम्हारा नाम क्या है" (4 word times); prashn
  "प्रश्नवाचक चिह्न" (the human vo_nm_prashn says the same); full "तुम्हारा नाम क्या है? प्रश्नवाचक चिह्न।" (4 word times + the
  mark's 2). The "?" in the second reading makes the synthesiser pause ~1 s before naming the mark; its pitch on
  "क्या है?" is the same falling contour as the run-on's (normal for a Hindi क्या-question) — a human recording can
  give it more question colour. Placeholders until recorded (`align_story_vo.py demo2_<line> --write` after a recording).
- `python -I -X utf8 demo_check.py ../HI02H12_L01_S01_dist/index.html demo2_figma_render_1280x720.png out T3` runs T2's
  checks against this frame (its picture and sentence boxes, the third tile tapped, the "?" centred, the self-advance to
  T4). `demo2_figma_render_1280x720.png` is Figma's own render of the frame. `../_before_demo2_fig/` holds the dist's
  three files from before (T3 = the ported BUILD_PUNCT auto demo).

Run-on sentence demo T4 "मेरे पास आम केला सेब और संतरा है ।" (replaced 2026-10-25)
- Flow: ... -> T3 -> T4 -> the engine's peek gate ("चलिए, साथ में करें!") -> G1 (unchanged: the old T4 crossed the same gate
  into the guided round). Figma frame 523:320 "6 T4" (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=523-320),
  PUNCT_DEMO like T2 / T3, in place of the ported auto demo on this slide (its data — "मेरे पास आम केला और सेब हैं" with
  vo_ro_d3 / vo_d3_explain / vo_ok_d3 / vo_d3_conclude / vo_mk_alp — is no longer used; the clips stay in assets/Audio).
- The frame keeps T2's title bar (its head bitmap again byte-for-byte demo1_head.webp) and tiles, and changes the rest:
  the picture box 523:334 moves to 144,211 and "image 230" (fruit, 144x96 at 144,229, drawn over the box; bundled as
  assets/Images/img_demo3_fruits.webp); the sentence bar 523:331 is 312,211 824x139; the sentence 523:332 is 50px in an
  893-wide centred box at -34,33 of the bar, "मेरे पास आम    केला    सेब और संतरा है ।" — a run of FOUR spaces after
  "आम" and after "केला", where the two 33x38 slots 523:333 / 524:352 sit (286,76 and 417,76 of the bar; #FFF1B6, 8px
  corners, 2px dashed stroke inside), and the sentence already ends with its danda. Their dashes are not T2's 10/5:
  Figma centres two dashes on each side — measured on the render, [margin, dash, gap, dash, margin] = 5,10,8,10,5 on
  the 38px sides and 4.5,9.5,5,9.5,4.5 on the 33px sides — so these slots draw one dashed line per side with those
  runs (the corners stay open, as in the render) over a solid rounded ring that only shows while the slot is lit.
  With that the slots are part of the pixel diff (T2/T3 leave their big slot's ring out): 0 solid differences.
- The 50px text, matched word by word against the render: Baloo Bhai 2's spaces are 3px narrower than Noto's at this
  size (word-spacing -3px), its line box puts the glyphs where an 84px one does, and the space before the closing
  danda is 4.5px narrower again (sentence.nudge pulls the danda in) — then every word's ink is within 1px of the render.
- Module: data.slots (each slot's box + dash runs), sentence.gaps / gap_spaces (the runs of spaces), sentence.nudge,
  mark_size (the comma at the sentence's 50px), mark_stagger_ms, full.targets and layout.{pic_x, bar, sent} are all
  optional; T2 and T3 have none of them and run exactly as before (checked).
- Flow = T2's, step for step, with two slots: the title bar on the intro line; the picture, bar and tiles; the sentence
  read without a pause, word by word; BOTH slots blink 3.5 s with the very same animation, started and stopped in the
  same frame; "अल्प विराम" sounds as its tile (the middle one) is tapped and the other two dim; a comma lands in each
  slot, left then right 0.3 s apart, its ink centred; the sentence is read again naming each comma where it sits —
  "मेरे पास आम, अल्पविराम, केला, अल्पविराम, सेब और संतरा है।" — each word lit as it is read and each slot lit while its
  "अल्पविराम" is spoken (full.targets: w0 w1 w2 s0 w3 s1 w4 w5 w6 w7); 1.5 s later both slots' boxes go (the commas stay)
  and the page moves on by itself (no आगे) through the round gate to G1.
- The gate after T4 (2026-10-25): the engine's round gate, unchanged — the blur, the peeking Swiftie
  (assets/UI/peeking.webp, its silent peek ~4.2 s), then "चलिए, साथ में करें!" in pink as vo_pt_guided sounds
  ("बहुत बढ़िया! अब हम साथ मिलकर शुरू करते हैं। चलिए, साथ में करें!"), then G1 when the VO ends. The engine shows each
  round's gate once per load, so a second run of T4 in the same load (the dev nav's list) used to go straight to G1;
  PUNCT_DEMO now clears the next round from `_gatedPhases` when its page ends at a round boundary (only T4 does), so
  T4's end crosses the gate every time. A child's run is unchanged (T4 ends once). smoke.py checks the gate after T4
  in the real flow (peek, then VO + title, then G1; no other gate since T1) and on two T4 runs from the dev nav.
  The dev nav's ▶ and its list still jump straight to a page (no gate), as before. `../_before_t4_gate/` = before.
- VO: four SYNTHESISED clips (`python -I -X utf8 recap_vo.py demo3 all|<line>`, T2's voice, tails trimmed) in
  demo3_assets/: intro = the title bar's line (as T3's), sent "मेरे पास आम केला सेब और संतरा है ।" (8 word times, the
  danda shown with "है"), alp "अल्प विराम" (the lesson's human vo_nm_alp says the same), full as above (10 times).
  Naming each comma in place is a choice: the alternative is T2's literal pattern, the sentence read with its pauses
  and "अल्पविराम" once at the end (both slots lit then) — a VO / one-line data change. Placeholders until recorded.
- `python -I -X utf8 demo_check.py ../HI02H12_L01_S01_dist/index.html demo3_figma_render_1280x720.png out T4` — T2's
  checks plus: two slots, blinking in lockstep with one animation; both marks landing in order and centred; each slot
  lit while its comma is named; the gate into G1. `demo3_figma_render_1280x720.png` is Figma's own render of the frame.
  `../_before_demo3_fig/` holds the dist's three files from before (T4 = the ported BUILD_PUNCT auto demo).

First sentence the child punctuates, G1 "राजू गेंद से खेल रहा था" (replaced 2026-10-25)
- Flow: ... -> T4 -> the round gate ("चलिए, साथ में करें!", unchanged) -> G1 -> G2 (unchanged). Figma frame 525:354 "7 G1"
  (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=525-354), type PUNCT_PICK = the PUNCT_DEMO module's
  tap mode (an alias in SlideModules; answerable, "mcq"), in place of the ported BUILD_PUNCT builder on this slide (its data —
  "राजू खेल रहा था उसकी गेंद खो गई" with two dandas, vo_build_q / vo_ro_g1 / vo_ok_g1 / vo_bp_* — is no longer used; the clips
  stay in assets/Audio). G2 onwards are still the ported builders.
- As asked: the title bar and its text appear exactly as on T4 (the bar comes in as its VO starts to sound), with this
  frame's line "वाक्य सुनिए और सही चिह्न लगाइए ।" as text and VO; the question and the options appear exactly as on T3 (the
  picture, the sentence bar with its empty slot and the three tiles come in, the sentence is read without a pause, word by
  word, then the slot's three slow blinks). From the moment the sentence has been read the tiles are the CHILD's: a wrong
  one wiggles — the engine's own wrong-answer shake (wgNo, one --fx-beat = 0.4 s) with its soft buzz — its colours
  unchanged, and stays tappable (no grey-out, no hint VO); the right one (पूर्ण विराम) is pressed, the other two dim, its
  mark lands in the yellow slot at once (ink-centred, as on T2) as its name sounds, with the engine's correct chime +
  confetti; 1 s (PACE.tail) after the name the page moves on to G2 by itself. No आगे, no standing Swiftie, no 🔊 chip.
- The frame is drawn on the whole stage like T2-T4, so mountSlide mounts PUNCT_PICK in the teaching frame (the engine
  header hidden) although its phase stays "guided" — the round gate, telemetry (question_started / question_answered /
  answer_wrong / punct_build_done with the wrong-tap count) and the engine's idle reminder still treat it as guided. The
  reminder (once per slide, after ~7 s of quiet with the tiles live) re-reads the sentence, each word highlighted as it
  is read; a tap cuts it short.
- The frame is T3's except: the title bar's text (its head is byte-for-byte demo1_head.webp again); the picture "image
  231" (a boy with a football, 124x124 at 207,219 — bundled as assets/Images/img_g1_boy_ball.webp); the sentence 525:366
  (64px, a 522-wide centred box at 60,18 in the bar — layout.sent); and two tiles: the first base 525:371 is 1px taller
  (197,442 227x170) and the middle tile 525:374 / 525:375 is 4px wider (base 525,443 231x169, face 527,445 227x161) —
  layout.tiles moves those boxes and keeps each mark and name on its frame centre. Followed the frame there (the ask was
  "the exact same layout as shown in this figma reference"); dropping layout.tiles from G1's data gives T3's tiles exactly.
  Pixel diff vs the render: 0.25% of the frame differs (glyph anti-aliasing), no solid differences; every box within
  0.5 px.
- VO: two SYNTHESISED clips (`python -I -X utf8 recap_vo.py g1 all|<line>`, T2's voice) in g1_assets/ -> assets/Audio/
  vo_g1_*.ogg: intro "वाक्य सुनिए और सही चिह्न लगाइए ।" and sent "राजू गेंद से खेल रहा था" (6 word times). The name on the right
  tap is T2's vo_demo1_purn ("पूर्ण विराम"). Placeholders until recorded (`align_story_vo.py g1_<line> --write` after a
  recording).
- `python -I -X utf8 pick_check.py ../HI02H12_L01_S01_dist/index.html g1_figma_render_1280x720.png out G1` checks the timeline
  in-page every frame (bar vs the intro, the boxes, the words vs the clip, the blink, the tiles going live and no earlier),
  the wrong taps (wiggle, colours, attempts, no mark), the right tap (press, dim, mark at once, the name, G2 a beat later, no
  gate, no आगे), the signals, the idle reminder, no header / Swiftie / chip, every box vs the frame, the fonts, each text's
  ink vs the render, the pixel diff, and the danda's ink centred in the slot. `g1_figma_render_1280x720.png` is Figma's own
  render. demo_check.py T4 now expects G1 to be this page after the gate; smoke.py taps it (two wrong tiles, then the
  right one) and drives the BUILD_PUNCT builder on G2 instead; the older checks' "no story styling past the Figma pages"
  step now mounts G2 (G3 since G2 became a Figma page). `../_before_g1_fig/` holds the dist's three files and build.py
  from before (G1 = the ported builder).

Second sentence the child punctuates, G2 "तुम कहाँ जा रहे हो" (replaced 2026-10-25)
- Flow: ... -> G1 -> G2 -> G3 (unchanged). Figma frame 600:197 "8 G2"
  (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=600-197), PUNCT_PICK like G1, in place of the ported
  BUILD_PUNCT builder on this slide (the same sentence and mark; its vo_ro_g2 / vo_ok_g2 clips stay in assets/Audio, unused).
  The प्रश्नवाचक चिह्न tile is the right one; flow, taps, wiggle, idle reminder and self-advance exactly as G1.
- The frame's title bar is T4's to the pixel (the render's band is identical to T3's / T4's) — its TEXT too, "सुनो यह वाक्य
  बिना रुके पढ़ा गया ।" — while the line it plays is G1's instruction "वाक्य सुनिए और सही चिह्न लगाइए ।" (vo_g1_intro, played
  again). Both as asked ("title bar and its text … exactly as Page 6 T4, along with the VO वाक्य सुनिए …"), so on this page
  the bar and its VO say different things (as on T2); to show G1's line instead, set G2's band_hi to gl["intro"]["shown"].
- The frame is T3's except the middle row: the sentence 600:209 (64px, T3's 479-wide box at 120,18 — layout.sent_x), the
  picture "image 239" 601:227 (a boy with a school bag, 102x136 at 218,213, drawn over its box; bundled as
  assets/Images/img_g2_boy_bag.webp) and the empty slot 600:210, 10px left of T3's (573,20 in the bar — layout.slot, new).
  The tiles are T3's exactly (G1's 1-4px tweaks are not in this frame). Pixel diff vs the render: 0.28% of the frame
  differs (glyph anti-aliasing), no solid differences; every box within 0.5 px; the "?" ink-centred in the slot.
- VO: one SYNTHESISED clip, the sentence (`python -I -X utf8 recap_vo.py g2 sent`, g2_assets/vo_g2_sent.ogg, 5 word times);
  the name on the right tap is T3's vo_demo2_prashn ("प्रश्नवाचक चिह्न"). Placeholder until recorded.
- `python -I -X utf8 pick_check.py ../HI02H12_L01_S01_dist/index.html g2_figma_render_1280x720.png out G2` (G1's checks on
  this frame; G3 next). smoke.py taps G2 too (a wrong tile, then "?") and drives the BUILD_PUNCT builder on G4 instead (two
  marks, through the round gate to P1); the older checks' "no story styling past the Figma pages" step now mounts G3.
  `../_before_g2_fig/` holds the dist's three files and build.py from before (G2 = the ported builder).

Third sentence the child punctuates, G3 "बाग में गुलाब, गेंदा और चमेली के फूल हैं ।" (replaced 2026-10-25)
- Flow: ... -> G2 -> G3 -> G4 (unchanged). Figma frame 528:424 "9 G3"
  (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=528-424), PUNCT_PICK like G1 / G2, in place of the
  ported EVIDENCE_QA pick on this slide ("आज सोमवार है कल मंगलवार होगा" — choose the right reading; its vo_pick_* / vo_ro_g3 /
  vo_o_g3_* clips stay in assets/Audio, unused; P2 / P3 are still that activity). The अल्प विराम tile is the right one;
  flow, taps, wiggle, idle reminder and self-advance exactly as G1.
- The title bar is G1's to the pixel (text = the instruction it plays, vo_g1_intro); the tiles are T3's / T4's. The middle
  row is laid out like T4's: the picture box at 144 with "image 233" (flowers, 140x140 at 146,211, drawn over the box;
  assets/Images/img_g3_flowers.webp), the sentence bar 312 824, the sentence 528:437 50px in an 893-wide centred box at
  -28,33 of the bar with a run of four spaces after "गुलाब" (sentence.gaps) where the one 33x38 slot 528:422 sits (278,70 in
  the bar; pixel-identical to T4's first slot, so T4's dash runs). The sentence already ends with its danda; as on T4 the
  space before it is 4.5px narrower in the render (sentence.nudge on span 9) — measured word by word, every word's ink then
  within 1 px. Pixel diff vs the render, the slot's dashes included: 0.25% (anti-aliasing), no solid differences; the comma
  ink-centred in the slot.
- Idle reminder (all three pages): a punctuation-only word shares the start of the word before it, so the two now light
  together ("हैं ।") — before, the highlight jumped from "फूल" straight to the danda.
- VO: one SYNTHESISED clip, the sentence read without a pause (`python -I -X utf8 recap_vo.py g3 sent`, 10 word times, the
  danda with "हैं"); the name on the right tap is T4's vo_demo3_alp ("अल्प विराम"). Placeholder until recorded.
- `python -I -X utf8 pick_check.py ../HI02H12_L01_S01_dist/index.html g3_figma_render_1280x720.png out G3` (G4 next).
  smoke.py taps G3 too (a wrong tile, then ",") and checks the EVIDENCE_QA pick on P2 instead; the older checks' "no story
  styling past the Figma pages" step now mounts G4. `../_before_g3_fig/` holds the dist's three files and build.py from
  before (G3 = the ported reading pick).

G4 "सही विराम चिह्न वाला वाक्य चुनिए ।" = the reference game's Page 11 (replaced 2026-10-25)
- As asked: "the exact same layout and the design of the page as of the Page 11 P4" of https://hi-02-h04-l01-s01-dun.vercel.app/
  (its page 11 in the dev nav's list = P4, a guided STORY_QUESTION "चित्र के लिए सही वाक्य चुनिए।": a picture above three sentence
  pills) with the user's picture (a girl flying a kite), the title "सही विराम चिह्न वाला वाक्य चुनिए ।" and three sentences that
  differ only in where the danda sits: "लड़की पतंग उड़ा रही है ।" (right), "लड़की । पतंग उड़ा रही है", "लड़की पतंग उड़ा । रही है".
  Type SENT_PICK (a module of its own, app.js [sent-fig]), in place of the ported BUILD_PUNCT builder ("बाग़ में गुलाब गेंदा और चमेली
  खिले हैं"); its clips stay in assets/Audio, unused. Flow: ... -> G3 -> G4 -> P1 (the round gate "अब आपकी बारी!" used to open
  here, at the guided -> practice boundary; since the gate change below it follows P2).
- The look, read from the live P4 (CSSOM + computed styles, pixel-diffed): the engine header in P4's look (its own variables set to
  P4's values — the band #DCEEFF with a 3px #B7DCFB edge and 75 / 10 padding, Swiftie's head 118px in a 140px header row — plus the
  🔊 chip at 94.5,80 with no SVG shadow and greyed while a line speaks, the title 32px ExtraBold #0B3D8C, P4's paler #F6FBFF stage,
  Swiftie's animated faces kept inside the round frame as P4 does); the picture bare at 315px high, centred, its grey frame IN the
  bitmap like P4's (g4_picture.py: P4's frame fitted on its own bitmap — outer radius 86, ring 15, inner 69 at 1058px high; the
  user's picture keeps its 4:3 shape at P4's height, 420px wide, since P4's rule is height 315 / width auto and cropping it to P4's
  bird's 1.48 shape would have cut the kite's tip or the girl's shoes); one row of three white 344x78 pills (28px ExtraBold, 3px
  #DADADA, 18px corners) with the 114.5px side padding that makes the row 1104 wide; no आगे, no hint bulb. With P4's own picture,
  title and sentences in P4's order, this page and the live P4 differ by 0 pixels at rest (and only in the 🔊 chip's animated waves
  while a line plays).
- The flow, P4's (its notes [P6-WRONG-QUIET] / [P6-REVIEW] / [P6-PROMPT-IDLE] / [P5-CORRECT-SFX] / [G1-P4-REVEAL-QUIET], checked live):
  the instruction on entry, again after every 5 s of quiet (no tap, nothing speaking, no read-out) with the picture's small silent
  pop-and-hold, and from the chip; a tap on a pill cuts any line. A wrong pill: the kit's wiggle + soft buzz (not read out), taps wait
  1 s, then the 1st: the try-again line (the pill dead until it ends); the 2nd: all three pills read one by one in row order, 0.5 s
  apart, each lifted while its line speaks; the 3rd: the reveal (the two wrong pills greyed and dead, the right one ringed green, the
  96px hand bobbing under it; a tap on the hand or just beside the pill counts). The right pill: the green ring and the picture's pop
  at once, 1 s with taps held (P4 plays its picture's own sound effect here — this picture has none, so the second is silent), then
  the kit's correct-select, the ding, the confetti and the happy Swiftie with the pill's own line, and 0.7 s later the page moves on;
  after the reveal (the guided tap): the same 1 s, then the ding + confetti alone, and it moves on (recorded as a revealed answer).
  A pill's words light up one at a time (orange, a slight pop) while its own line speaks; a lone danda lights during the pause it
  makes. The engine's one-off idle reminder is off on this page (it has its own repeat), and its vo-lock no longer swallows a tap on
  a pill while a line speaks (P4 lets that tap cut the line).
- VO: five SYNTHESISED clips (`python -I -X utf8 recap_vo.py g4 all|<line>`, the same voice) in g4_assets/: prompt (the title),
  try ("वाक्यों को ध्यान से पढ़िए और सही विराम चिह्न वाले वाक्य पर टैप करिए।" — P4's "चित्र को ध्यान से देखिए और उससे मिलते हुए वाक्य पर टैप करिए।"
  made for this page; a choice), and o1-o3, each sentence read with its own punctuation: the synthesiser pauses ~1 s at a danda,
  so the three readings are heard differently. build.py turns each clip's word timings into the pill's word-sync table (each word's
  start, then the last one's end; a lone danda from the end of the word before it). Placeholders until recorded.
- `python -I -X utf8 g4_check.py ../HI02H12_L01_S01_dist/index.html out [--ref g4_assets/ref_p4_bird_gry.png]` checks the whole flow
  in-page every frame (the right pill, the three wrong ones + the guided tap, the idle repeat, every word lit inside its clip window)
  and, with --ref (needs the network), the pixel match against the live P4 using P4's own picture (ref_p4_bird_gry.png, read from
  that page). smoke.py taps G4 (a wrong pill, then the right one, through the gate to P1) and drives the BUILD_PUNCT builder on P1
  instead. `../_before_g4_ref/` holds the dist's three files and build.py from before (G4 = the ported builder).

P1 "सही विराम चिह्न वाला वाक्य चुनिए ।" = the reference game's Page 11 again (replaced 2026-10-25)
- As asked: the same P4 layout and design as G4, with the user's picture (two boys looking at a picture book), the title
  "सही विराम चिह्न वाला वाक्य चुनिए ।" and three sentences that differ only in where the question mark sits: "क्या यह आपकी किताब है?"
  (right), "क्या? यह आपकी किताब है", "क्या यह आपकी? किताब है" — written as given, the "?" against its word. Type SENT_PICK (G4's very
  module: same look, same flow, same checks), in place of the ported BUILD_PUNCT builder ("क्या तुमने खाना खाया"); its clips stay in
  assets/Audio, unused. Still the first practice page: G4 -> P1 -> P2 (no gate before or after P1 — see the gate change below).
- What carries over from the builder: the practice phase, its eis, and data.mastery — P1 still counts in the end's mastery score
  (one attempt per page, a hit on a first try, as the builder counted it); G4 has no such flag and is not counted. The signal is
  now evidence_qa_first_try (the pick's), not punct_build_done (P4 and P5 still send that one).
- The picture: g4_picture.py over p1_assets/p1_book_source.png -> img_p1_book_gry.webp (P4's grey frame in the bitmap, 4:3 at
  P4's height, as G4's).
- VO: the title and the try-again line are G4's own clips (vo_g4_prompt, vo_g4_try: the same words), played again; three new
  SYNTHESISED clips (`python -I -X utf8 recap_vo.py p1 all|<line>`) in p1_assets/: o1-o3, each read with its own "?" — the
  synthesiser lifts and pauses ~1 s there, so "क्या? यह ..." and "क्या यह आपकी? किताब है" are heard broken where theirs sits; a word
  carrying its "?" stays lit through that pause. Placeholders until recorded.
- `python -I -X utf8 g4_check.py ../HI02H12_L01_S01_dist/index.html out --page P1 [--ref g4_assets/ref_p4_bird_gry.png]` — G4's
  checks on P1 (straight on to P2, mastery counted), and the same pixel match against the live P4. smoke.py taps P1 too (a wrong
  pill, then the right one, on to P2) and drives the BUILD_PUNCT builder on P4 instead (a wrong gap, then "," and "।").
  `../_before_p1_ref/` holds the dist's three files and build.py from before (P1 = the ported builder).

P2 "सही विराम चिह्न वाला वाक्य चुनिए ।" = the reference game's Page 11 once more (replaced 2026-10-25)
- As asked: the same P4 layout and design, with the user's picture (a girl holding coloured pencils in a stationery shop), the
  same title, and three sentences that differ only in their marks: "मेरे पास लाल । नीली । हरी और पीली पेंसिल हैं ।", "मेरे पास लाल नीली
  हरी और पीली पेंसिल हैं ।" and "मेरे पास लाल, नीली, हरी और पीली पेंसिल हैं ।" — the right one (the commas) is the third one listed.
  SENT_PICK again (build.py practice_pick(), shared with P1), in place of the ported EVIDENCE_QA pick ("राम खाना खाकर सोया"); its
  clips stay in assets/Audio, unused. P1 -> P2 -> the round gate -> L1, the letter page -> the end screen (pages 13-16
  removed, the gate opened before the end screen, then L1 added: see below). Practice phase, eis and data.mastery carried over.
- Two lines: these sentences measure 460-495px at P4's 28px ExtraBold, and P4's pill is a fixed 344px with nowrap (its own
  sentences all fit; three pills + two 36px gaps already fill the 1104px row, so the pills cannot widen). Copied literally, the
  text would spill out over the next pill. So when a sentence does not fit, SENT_PICK puts every pill of the page on two lines,
  all broken after the same word — the one that keeps the widest line narrowest; a lone "।" stays with its word — so the three
  still line up word for word ("मेरे पास लाल । नीली ।" / "मेरे पास लाल नीली" / "मेरे पास लाल, नीली," over "हरी और पीली पेंसिल हैं ।").
  The pills keep P4's width, font, colours and places and are centred on P4's row line (93px tall instead of 78); the picture
  does not move. Pages whose sentences fit one line (G4, P1) are untouched (their 0 px matches still hold).
- The picture: g4_picture.py over p2_assets/p2_pencils_source.png -> img_p2_pencils_gry.webp.
- VO: title + try-again = G4's clips again; three new SYNTHESISED clips (`python -I -X utf8 recap_vo.py p2 all|<line>`) in
  p2_assets/, each read as written: ~1 s at each "।" (heard as the sentence ending there), straight through with no mark, and a
  short pause at each comma. Lone dandas light in the pauses they make. Placeholders until recorded.
- `python -I -X utf8 g4_check.py ../HI02H12_L01_S01_dist/index.html out --page P2 [--ref g4_assets/ref_p4_bird_gry.png]` — the
  same checks (straight on to P3), the two-line rule (one height, centred on y 570.5, the same break word, no line opening with a
  mark, nothing spilling), and the 0 px match against the live P4 with P4's own short sentences. smoke.py taps P2 too and drives
  the EVIDENCE_QA pick on P3 instead. `../_before_p2_ref/` holds the dist's three files and build.py from before (P2 = the
  ported pick).

The round gate "अब आपकी बारी!" follows P2 (moved 2026-10-25)
- As asked: after P2 the transition screen — the peeking Swiftie, then the pink "अब आपकी बारी!" revealed as its VO
  (vo_pt_practice, "वाह! अब आपकी बारी।") starts at the animation's mouth-open point, 4.2 s in — then P3. It is the engine's own
  round-3 gate, unchanged in look, animation and VO; only WHEN it opens changed. The engine opens each round's gate at the phase
  boundary, which here was G4 -> P1 (guided -> practice), so the three P4-style pages G4, P1, P2 were split by it. Now
  G4 -> P1 and P1 -> P2 are plain page changes and the gate opens between P2 and P3, once (asked: move it, not add a second).
- How: the card carries `round3_gate_after: "P2"`; build.py [gate-p2] patches completeSlide so the round-3 gate is skipped at the
  phase boundary and opened on that page's end instead — and, like T4's gate, EVERY time that page ends (a re-run of P2 from
  the dev nav's list crosses it again; the engine's once-per-load rule is cleared for round 3 there). The tutorial -> guided
  gate after T4 is untouched. Nothing else in the file changes.
- Checked (while P3 followed P2) by gate_check.py: G4 -> P1 with no gate; P2 -> the gate -> P3 twice in one load, the peek
  then the title with its VO; a phase_transition per opening. `../_before_gate_p2/` holds the dist's three files and build.py
  from before (the gate at G4 -> P1).
- Dormant from the removal of pages 13-16 (next section) until 2026-10-26: P2 had become the last page, and the engine opens
  no round gate before the celebration (completeSlide's `next.type !== "CELEBRATION"` rule). Opened again before the end
  screen on request — see "The round gate after P2 opens before the end screen" below.

Pages 13-16 removed (asked 2026-10-25, built 2026-10-26)
- As asked: the dev nav's pages 13, 14, 15 and 16 — the ported P3 (EVIDENCE_QA "मीना ने पतंग उड़ाई ..."), P4 and P5 (BUILD_PUNCT
  "मेरे बस्ते में ...", "तुम्हें कौन-सा फल ...") and P6 (SORT_WORDS) — are dropped from the card (build.py [rm-p3p6]). The game is
  now 13 pages: T0, T0B, T1, T2, T3, T4, G1, G2, G3, G4, P1, P2, CEL — P2 reaches the end screen straight away. (Later that
  day L1, the letter page, was added after P2's gate: 14 pages, see "L1, the letter page" below.)
- Consequences handled: `qtype_sort_done` (fired only by P6) is dropped from signals_expected so the end screen's validator no
  longer reports a missing signal (`punct_build_done` still fires on G1-G3, `evidence_qa_first_try` on G4 / P1 / P2); the mastery
  score at the end now covers P1 and P2 (the only data.mastery pages left); the round gate after P2 went dormant (above; opened
  again before the end screen on 2026-10-26, next section). The
  removed pages' clips and pictures stay in assets/ and in the card's asset table, unused, and their modules stay in the
  engine unused — nothing else changes. smoke.py's builder / evidence-pick / sort steps are gone with the pages; it now runs
  from the start to the end screen and checks the validator there.
- Built 2026-10-26: the entry above was written on the 25th before build.py carried the patch — until the 26th the dist and
  build.py were byte-identical to `../_before_rm_p3p6/` (17 pages). Rebuilt and checked that day: app.js and style.css unchanged
  byte for byte, index.html different only in the card (slides, signals_expected, phase_distribution practice 7 -> 3); smoke.py
  33/33 from the start screen to the end screen, validator clean; gate_check.py's validator line now expects exactly the
  signals of the pages its jump-in run (from G4) skips to be missing — phase_transition (T4's gate), punct_build_done (G1-G3) —
  and qtype_sort_done neither expected nor missing (its earlier `passed === true` could only hold for a run from the start).
- `../_before_rm_p3p6/` holds the dist's three files and build.py from before (17 pages).

The round gate after P2 opens before the end screen (2026-10-26)
- As asked: after P2 (the dev nav's page 12) the transition screen — the peeking Swiftie, then the pink "अब आपकी बारी!" revealed
  as its VO (vo_pt_practice) starts at the animation's mouth-open point, 4.2 s in — then the CELEBRATION end screen. It is the
  engine's own round-3 gate, unchanged in look, animation, timing and VO, and it still opens EVERY time P2 ends ([gate-p2]).
- How: build.py [gate-cel] changes one condition in completeSlide. The engine never opens a round gate when the next page is
  the CELEBRATION; that rule is lifted for the round3_gate_after page (P2) alone, every other page keeps it. The gate mounts
  the end screen when it closes, and the end screen then runs exactly as before (its own animation, praise VO and button).
- Checked: app.js differs from `../_before_gate_cel/` in that one line only; index.html and style.css are byte-identical.
  smoke.py 34/34 from the start screen through T4's gate and P2's gate to the end screen, validator clean (phase_transition
  now also fires on P2's gate). gate_check.py: G4 -> P1 still with no gate; P2 -> the gate -> the end screen twice in one
  load, the peek then the title with its VO, the end screen up with the gate closed and the stage unblurred; screenshots
  gate_after_p2.png and end_after_p2.png.
- `../_before_gate_cel/` holds the dist's three files and build.py from before (P2 -> the end screen with no gate).
- Since L1 (next section) follows P2, the gate opens before L1 by the engine's ordinary rule; the [gate-cel] condition stays in
  place (harmless now) so the gate would still open if L1 were ever removed again.

L1, the letter page after P2's gate (2026-10-26)
- As asked: after P2's "अब आपकी बारी!" transition, one story page before the end screen, the Figma frames played as a scene with
  the user's five sound files: 538:2 (the girl writing) opens with the healing-magic shimmer (sfx_letter_magic); after 2 s it
  fades into 538:35 (the girl thinking); three thought bubbles pop from her head and the grandfather cloud grows in slowly
  (538:39) as the piano loop (bgm_letter_nostalgia) fades up, the engine's own background music ducked under it; in the same
  cloud the grandfather dissolves to white and the letter appears with the "idea" chime (sfx_letter_idea; 558:2's size, 189 px);
  it pulses and waits for the tap; the tap (sfx_letter_pop) zooms the envelope to 610:6 (71,-50 1138x758 over the room blurred
  7.5 px at 90 %, flattened to one picture) while the loop fades out; the seal pops, the flap swings open on the paper crackle
  (sfx_letter_paper), a lined sheet rises, a veil in the end screen's colour — then the end screen. No आगे, no header, no idle
  reminder; the envelope is the only tap. Timings (data.pace, ms): scene A 2000 | cross-fade 650 | bubbles from 2600 every 230 |
  cloud from 3300 over 1600 | hold 2600 | dissolve 1500 | letter in 650 (chime at 9000) | ready at 9750; after the tap: zoom 1200
  | flap + crackle at 1200 | sheet at 1700 | veil at 2700 | end screen at 3250.
- Pictures: the five frames are flat bitmaps (the cloud, grandfather and letter are baked into 538:39 / 558:2), so the user's two
  attached PNGs are the moving layers: 1.png = the grandfather cloud (fitted on the 538:39 render at 0.2508 x (862.09, 8.61), err
  5.8), 2.png = 610:6's "Glossy Heart-Sealed Envelope 1" byte for byte. The letter state keeps THAT cloud, whitened (same alpha,
  white RGB) — "in the same cloud" as asked — so it does not pixel-match 558:2's differently drawn cloud; the envelope is centred
  in it at 558:2's size. The envelope is cut along its drawn fold lines into body (the pocket), flap (seal footprint inpainted),
  inner (the inside, shaded) and heart; the flap turns about the top edge (rotate(-12.72deg) rotateX(a) rotate(12.72deg)), its
  back the plain cream of the mirrored front. Measured by the scratchpad's measure_*.py, made by make_letter_assets_*.py; all in
  letter_assets/ (img_letter_*.webp: scenes at 1400 px, cloud 820 px, envelope layers 1536x1024; the sounds as ogg, leading
  silence trimmed on the chime and the crackle, the pop -5 dB, the shimmer cut to 4 s).
- Engine: build.py [letter-fig] adds the LETTER_STORY module and CSS, L1 to the card (phase practice = round 3 continues, so no
  second gate before CEL), isTut for the whole-stage frame (as PUNCT_PICK), the idle-reminder exclusion, and the asset copy (7l).
  Every visual beat starts on its sound's "playing" event (150 ms fallback); window.oceanCleanup (clearHost runs it) stops every
  timer and sound and restores the background music when the page is left (the dev nav, the end screen).
- Checked: `python -I -X utf8 letter_check.py ../HI02H12_L01_S01_dist/index.html out [<dir with render_538-39/558-2/610-6.png>]`
  — the page mounted straight: every beat at its moment on the page's clock, each sound within 20 ms of its beat, the icon's
  box, the 610:6 box, the pulse, the opening, the end screen 3.3 s after the tap, every sound stopped on leaving, a clean re-run
  and a clean mid-way exit; against Figma's renders the grandfather stage (mean 11.3 / 255x3, cloud region 17.3) and the
  full-screen envelope (mean 8.5) are close. gate_check.py: P2 -> the gate -> L1 twice in one load, L1 -> the end screen with no
  gate. smoke.py 35/35 from the start screen to the end screen through L1's tap. `../_before_letter/` holds the dist's three
  files, build.py, smoke.py and gate_check.py from before (13 pages, P2 -> the gate -> the end screen).
- Later 2026-10-26, the two room pictures replaced (asked: "update these images ... don't degrade the quality and resolution"):
  the user's new versions of the girl writing and the girl thinking, 1672x941, stored LOSSLESS (img_letter_scene_a.webp /
  _b.webp, ~1.35 MB each, pixel-identical to the PNGs sent) in place of the frames' bitmaps at 1400 px. Nothing else changed
  (index.html, app.js, style.css byte-identical); the girl sits within 5 frame px of her old place, so the bubbles and the
  cloud stay where 538:39 put them. letter_check.py now judges the 538:39 comparison inside the cloud's own opaque pixels
  only (24.3 / 765 before and after the swap, so the pictures changed nothing about the cloud; the room art differs from the
  frame by the user's choice). `../_before_letter_scenes/` holds the two 1400 px pictures.
- Later 2026-10-26, the FULL opening ([letter-open]; asked: "the envelope should fully open instead of opening from the top only",
  and "corners of the envelope cut and displaced"). The envelope is now cut into FOUR flaps meeting at the fold lines' apex — top
  (the drawn flap), left, right and bottom (the pocket split along BL-apex / BR-apex, each side flap confined to its own half at
  the apex; the two new edges carry the envelope's own orange line) — over the inside (the whole silhouette, shaded). Each flap
  turns about its OWN edge (hinge = the edge's midpoint in the 1138x758 box, the edge's own angle: the drawing is not a true
  rectangle), away from the viewer, to 166-170 deg, so the envelope lies open like a cross; the sheet then rises out over the
  opened flaps (z-index while out). After the tap: pop + zoom to 610:6 (1.2 s, held) -> paper crackle + seal pops + top flap
  (0) -> side flaps (+0.45 s) as the view PULLS BACK to 0.56 about the frame's centre (so no flap reaches the frame's edge: the
  old "cut corners" were the single flap swinging above the frame) -> bottom flap (+0.75 s) -> sheet (+0.95 s) -> veil
  (+2.3 s) -> end screen (+2.85 s). The seal's footprint is now filled by a push-pull blur (the single normalised blur left a
  ring). Sounds: all five are fetched and decoded at mount, so each starts on its beat online too; the letter pops in in 0.45 s
  on the chime's first frame. The "aahaha" the user hears is sfx_letter_idea (the only voice-like clip on the page: a sustained
  ~210 Hz "aaa" then two "ha"s, 3.3 s) — it plays ONCE, at the letter's appearance; the game's own sfx_celebrate (a voiced
  cheer) still plays on every right answer and on the end screen, untouched. letter_check.py: the chime once; the four flaps'
  transforms; the frame's 4 px border unchanged between the zoomed and the open shots (0 px); the end screen ~4.1 s after the
  tap. gate_check 11/11, smoke 35/35. `../_before_letter_open/` holds the dist's three files, build.py, letter_check.py and the
  previous envelope layers (one flap + body).
- Later 2026-10-26, the opening REDONE ([letter-dive]; asked: "why did you disturb the design of the envelope? keep the design of the
  envelope exactly as before, and the opening effect should be at the whole screen as a transition screen, smoothly"). The four-flap
  cut is gone: it had ADDED two fold lines (BL-apex, BR-apex) and a shaded inside to the drawing, and its pull-back shrank the
  envelope. The envelope is again the drawing's own two-layer cut — body (the pocket), ONE flap, the inside, the heart — now stored
  LOSSLESS with the drawing's own pixels (scratchpad make_env_layers_exact.py: the seal's footprint filled by the push-pull method
  in BOTH the flap and the body, so the seal lives in the heart layer only); painting order inner < sheet < body < flap < heart, so
  closed it IS the drawing (the layers stacked vs 2.png: mean 0.36/765, 0 px over 30). After the tap: pop + zoom to 610:6 (1.2 s)
  -> paper crackle: the seal pops and the flap lifts TOWARD the viewer to 80 deg (1 s) — standing up, almost edge-on as a thin band
  under the top edge, so no part of it ever rises above that edge and nothing can be cut by the frame — and the sheet rises 35 px
  in the mouth (+0.35 s) -> the view DIVES into the envelope (+0.7 s, over 1.7 s): the box scaled 5.2x about the mouth's centre
  (layout.mouth = the incentre of the top-edge / fold-apex triangle, (568.8, 292.4) box px) onto the frame's centre, until only
  the sheet fills the screen, its ruled lines fading -> veil (+1.9 s) -> end screen (+2.45 s, ~3.7 s after the tap). The envelope
  never gets smaller than 610:6's box. letter_check.py: the layers; the closed envelope against the DRAWING itself (the dist's
  layers stacked over the blurred room, judged on the flat parts: mean 3.0, 0 px over 40; Figma's 610:6 render stays the frame
  target, mean 9.4 — its hard-edged heart resamples a little differently in the browser, a ring the earlier versions had too);
  the opening read from the page's OWN frame trace (rAF — Playwright's polls lag while the renderer is busy): the flap lifting at
  1.7 s, standing at 2.25 s with its tip 31 box px under the hinge and in no frame above it, the box >= 1138 in every frame after
  the zoom, the dive at 3.0 s (4.1x, 98 % sheet pixels in the shot), the end screen ~3.7 s after the tap; and a second opening
  with nothing else running: 151 frames, max gap 18 ms (60 fps). gate_check 11/11, smoke 35/35. `../_before_letter_dive/` holds
  the dist's three files, build.py, letter_check.py and the four-flap layers.

Stamp page L2 after the letter (added 2026-10-26, [stamp-fig]; asked: "after the letter covers the whole screen this screen should
appear ... the table and the title bar with its text and synced VO, then the letter sheet and the stamp holder, then both stamps
with a pop animation and this sound effect, then the sentence word by word with its VO, then the empty light yellow box blinking as
before for 3.5 s, then the correct stamp auto-drags to the box, stamps the symbol in its centre with this sound effect, goes back,
and the box disappears but not the symbol")
- The frame: FLN-by-MJ 565:28 "G3 guided story question" — https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=565-28.
  Built in the frame's 1280x720 px on the whole stage (.sfig-full, like the demos and L1). Places (get_metadata, checked on the
  render): the wood table 0,-1 1280x721 (the frame's bitmap, cover-fitted); the title bar = the demos' .dmf-band (the same group:
  36,26 1244x120, the pill's text at 139.55 — this render's text starts at x 180 like theirs — the same Swiftie head, so
  assets/UI/demo1_head.webp is reused; its line "वाक्य में सही स्थान पर ठप्पा लगाइए।"); the sheet "image 238" at 355,64 571x594 (the
  frame shows the 594x571 picture turned 90 deg — the turn picked by matching the render; the paper itself at 392..887 x 154..559);
  the stamp tray 427,565 426x142 with its 0 4 4 .48 shadow (a drop-shadow filter: it follows the tray's shape); the stamps 532,541
  74x116 (।) and 677,540 72x115 (?) — their print points (the middle of the face's bottom edge) at (36,113) / (35,114) in their
  boxes; the sentence "नमस्ते दादाजी, आप कैसे हैं" in the frame's 1075-wide centred box at 63,336 (48 tall, 30px, black — its ink
  455..745 x 342..372 on the render; the page sets the box 2 px lower because Noto's ink sits 2 px above Figma's fallback's, and
  lands at 454..746 x 342..372); the slot 751,331 36x58 #FFF1B6, 8px corners, a 2px dashed rgba(86,86,86,.85) stroke inside
  (its runs read off the render: 6 9 6 9 6 across, 6 7 4 10 4 10 4 7 6 down — drawn as the demos' per-side SVG lines).
- The flow (STAMP_DEMO, build.py [stamp-fig]; moments in data.pace, ms): the table under the letter page's cream veil, which lifts
  (0.6 s); at 0.4 s the title's line (vo_stamp_intro) — the bar appears the moment it is heard (the demos' rule); 0.5 s after the
  line: the sheet settles onto the table (from 28 px up, 0.55 s), the tray slides up 150 ms later; +0.7 s: the two stamps pop
  (scale 0 -> 1 about the base, 0.45 s) 350 ms apart, each on the user's pop (sfx_stamp_pop); +0.7 s: the sentence read without
  a pause (vo_stamp_sent), each word arriving at its start on the clip's own clock; as the clip ends the empty slot appears and
  blinks 3.5 s (the demos' dmfBlink, three slow blinks); then the ? stamp lifts (a drop shadow, over the sheet) and glides 0.9 s to
  hover 34 px above the slot, presses in 0.14 s so its print point stands 20 px under the slot's centre (standing on the slot)
  while the user's stamp thud (sfx_stamp_press, 1.01 s into the move) sounds; 40 ms later the ? is printed — the sentence's own
  30px black letter, its INK on the slot's centre (centreInk, as the demos), landing from a little large and tilted — the stamp
  lifts (0.18 s) and glides home (0.8 s, set down at 2.25 s); at 2.3 s the slot's box goes (fill and dashes fade), the ? stays;
  at 3.3 s the end screen (phase practice = round 3 still, no gate). No आगे, no header, no idle reminder.
- Sounds: the two mp3s as ogg (libvorbis q5, mono): the pop trimmed to start at its burst (0.10 s cut), the thud trimmed to 0.5 s
  before its strike (the strike 44 ms in). The page fetches its three sound objects and its two clips at mount. VO: TWO SYNTHESISED
  clips (`python -I -X utf8 recap_vo.py stamp all|intro|sent`, the same voice) in stamp_assets/ with their word timings
  (vo_stamp_*.words.json) — placeholders until recorded; a human recording goes in as stamp_assets/vo_stamp_<line>.ogg, then
  `align_story_vo.py stamp_<line> --write` and a rebuild. Bitmaps by the scratchpad's make_stamp_assets.py (the sheet, tray and
  stamps lossless; the table q95) — stamp_assets/img_stamp_*.webp; stamp_figma_render_1280x720.png is Figma's render of the frame.
- Checked: `python -I -X utf8 stamp_check.py ../HI02H12_L01_S01_dist/index.html out [stamp_figma_render_1280x720.png]` — the page
  mounted straight: every beat read from the page's OWN frame trace (rAF) and a hook on every media play, judged against each
  other and against the clips' own clocks (not Playwright's polls): the bar within 60 ms of the line's first sounding frame, the
  sheet 0.5 s after its ended frame, the pops within 60 ms of their stamps, each word's reveal frame within -60..+40 ms of its
  start on the clip's clock, the slot at the clip's ended frame and its 3.5 s blink (opacity to .2), the press point (770, 381) =
  the wanted one, the thud at 1.005 s and the mark at 1.05 s of the move, home at 2.18 s, the box gone at 2.3 s, the ? ink
  centred on the slot (769, 359.5), the end screen at 3.32 s; against Figma's render (the slot moment, its blink paused for the
  shot): frame mean 4.4, the sheet with its sentence and slot 6.3, the sentence's ink box within 1 px; a clean re-run and a clean
  mid-way exit. letter_check.py: L1's tap now hands over to L2 (~4 s). gate_check 11/11 (P2 -> gate -> L1 -> L2 -> end screen,
  no further gate), smoke 37/37. `../_before_stamp/` holds the dist's three files, build.py, recap_vo.py and the three checks from
  before (14 pages, L1 -> the end screen).
- Later 2026-10-26, [stamp-drag] (asked: "the blinking of the empty box a little smoother, the auto drag a little slower; the stamp
  should NOT apply — only shown as a guidance 0.5 s after [the blink], repeated only after 7 s of inactivity; both stamps draggable;
  a stamp placed at a wrong place, or the wrong stamp on the box: this incorrect sound + a wiggle + reset; the correct stamp on the
  box: applied with the same sound as now, the box disappears with this correct sound, and confetti with this sound"): the page is
  the child's from the moment the slot appears (.stp.live — before that the stamps take no drags). The blink was made softer
  (stpBlink, to .45) and then PUT BACK to the demos' dmfBlink the same day — asked: "just like that of the pages before".
  The guidance (data.pace: hint_at 500 after the blink; glide 1500, hold 450, back 1100): the ? stamp lifts, glides over the slot,
  hovers hover_up above the press point and glides home — it never presses or prints; it does not run if the child has already
  taken hold of a stamp, and it comes again after idle_ms (7000) without a touch (a 200 ms tick; the count starts over at every
  drop and after each guidance). Drags: pointer events with capture on each .stp-stamp (touch-action none); a stamp is taken from
  where it IS (the computed matrix: mid-guidance, mid-return — the guidance stops where it is), follows the finger at the lifted
  size (1.08, the frame's px through the stage's scale), and is judged on its PRINT POINT (data.layout.tips) against the slot's
  centre (tol_x 50, tol_y 70); a move under tap_px (10) is a touch, set back down silently. Wrong (off the slot, or the । stamp on
  it): sfxWrongSoft() — the kit's sfx_wrong_new.ogg IS the user's "standard sfx_incorrect_feedback.wav" (the same recording:
  correlation 1.000, 0.72 s; likewise sfx_correct_new.ogg = "standard sfx_correct_feedback.ogg" and sfx_celebrate.ogg = "standard
  sfx confetti.wav", so nothing new is shipped) — the kit's wgNo wiggle on the stamp's picture (its box keeps the drop place),
  then it glides home (wiggle 450 + reset 500); state.attempts counts it. The class is `stp-wrong`, NEVER a bare `wrong`: the
  engine's style.css has `:is(.wrong,.wrong-flash,.ocean-wrong){background-color:#fff!important}` (its "motion-only, never red"
  feedback rule), which boxed the dropped stamp WHITE over the wood in the first build — the user saw it ("why is there a white
  colored box"). The pops sound at .48 (asked: 40 % less than the first build's .8). Right (the ? stamp's print point within tol of the slot's
  centre): it snaps over the slot (snap 220) and presses (press 140) on the thud (thud_at 280), the mark is printed at 400 (its ink
  on the slot's centre, as before), lifts at 560, glides home from 800 (back_home 800); the box goes at 1600 on sfxCorrect(); the
  engine's confettiCannon() at 2100 (it plays sfxConfetti itself; fixed, z 100001, so over the whole stage); the end screen at
  4400 (completeSlide's afterConfetti only waits for .conf-shot, not this confetti — so the page waits itself). Leaving mid-drag:
  oceanCleanup releases the pointer capture, clears the idle tick.
- Checked: stamp_check.py is now the child too (after the setup beats, read from the page's own trace as before): the slot's blink
  (dmfBlink, opacity to .2), the pops' volume .48, .live with the slot, the guidance 500 after the blink, 1500 to the hover point
  (within 4 px; 15+ px away two thirds in), home at 2900, no thud/mark/gone; the guidance again at 7.0–7.5 s; a grab mid-glide (no
  jump over 10 px across the grab frame, the box moves with the finger within 8 px); the far drop (the buzz within 60 ms, .stp-wrong,
  NO white box: the element's background transparent and the box's corner over the wood the wood's colour in the shot, home within
  1.4 s); the । stamp on the slot (the same); a 3 px tap (nothing); the ? dropped 30 px right / 20 px low (the snap to
  the press point within 4 px at ~360, the thud at 280, the mark at 400, home by 1.8 s, the box gone at 1600 on the chime, confetti
  at 2100 on its sound, the ? ink on the centre within 3 px, the end screen at 4400, four lifts of the ? in all); the Figma render
  comparison as before; a re-run; leaving mid-way WITH a stamp in hand. smoke.py and gate_check.py drop the ? stamp on the slot
  themselves (the inline drag: 12 mouse moves from the stamp's handle). 32/32, letter_check, gate 11/11, smoke 38/38.
  `../_before_stamp_drag/` holds the dist's three files, build.py and the four checks from before (the self-stamping page);
  `../_before_stamp_fixes/` the drag build before the blink/white-box/pop fixes.

Rebuilding after a card/content change
1. Edit the ORIGINAL card in `../_before_reskin/index.html` (the build always starts from there),
   or edit `build.py` for chrome/CSS changes.
2. Clone the reference next to this file (or pass its path):
   `git clone https://github.com/siddharthsharma-ctrl/Ek-aur-Anek ref/Ek-aur-Anek`
3. `python -I build.py [ref/Ek-aur-Anek] [../HI02H12_L01_S01_dist]`

Checking it (needs Python 3.12, `pip install playwright`, and Chrome installed)
- `python -I shoot.py ../HI02H12_L01_S01_dist/index.html shots --gate` — screenshots of every screen.
- `python -I smoke.py ../HI02H12_L01_S01_dist/index.html` — drives the start button, the story page's आगे, the Figma pages
  through the gate into G1 and on through G2, G3 (wrong + right tiles), G4, P1 and P2 (wrong + right pill), P2's gate, L1 (the
  letter page to its pulsing envelope, then the tap), to the end screen (its validator clean), and the dev nav; prints PASS/FAIL
  per step.
- `python -I -X utf8 letter_check.py ../HI02H12_L01_S01_dist/index.html out` — the letter page beat by beat (see its section).

In the browser: open `index.html?dev=1` for the slide-jump bar (bottom-right) and the signal banner;
`index.html?slide=N` mounts slide N directly.
