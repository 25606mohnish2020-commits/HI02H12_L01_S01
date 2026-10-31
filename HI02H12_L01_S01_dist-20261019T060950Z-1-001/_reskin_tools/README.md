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
- Later 2026-10-27, T2 re-pointed at the Figma frame 656:2 ([demo1-pinki]; asked: "replace the text and the image asset on that
  page with this exact as shown in this figma reference and apply the exact same animations and the same effects, make the new
  VOs accordingly; rest exactly the same"). The user's 1280x720 render of 656:2 (now demo1_figma_render_1280x720.png; the 519:32
  render kept as demo1_figma_render_1280x720_v1_2026-10-24.png) is 519:32's to the pixel — title bar, tiles, slot, boxes — except
  two things (2.02 % of the frame): the sentence, "पिंकी स्कूल जा रही है" (its ink 461..944 on the render; the browser shapes it
  the same width within 2 px, but in the old box every word sat 3.5 px right of the render's — the frame's text box is 3.5 px
  further left, so data.layout.sent_x = 96.5 in the bar, the same centred 479 width), and the picture, the girl in uniform
  walking (ink 229..308 x 214..344). The Figma connector had no authorization in this session, so the picture is CUT FROM THE
  RENDER at 1x — the only source to hand — at its ink's box plus a 1 px white margin on the left, right and bottom (the top is
  flush with the picture box's border), 82x132 px on the box's own white, stored lossless as img_demo1_girl.webp (the 519:32
  girl, 320x480 with transparency, is in `../_before_demo1_pinki/demo1_assets/`); build.py gives T2 data.layout.img =
  [228, 214, 82, 132] (frame px, the module's T3 hook) in place of the CSS's 227,221 80.052x120 box. On a stage wider than
  1280 px that picture is upscaled — re-cut it from Figma's own asset (export "image" at 2x+) once the connector is authorized,
  the same way T3's / T4's were. recap_vo.py: demo1's sent / full lines are the new sentence ("पिंकी स्कूल जा रही है" /
  "पिंकी स्कूल जा रही है, पूर्णविराम।"), re-made (edge-tts 7.3.1 — 7.2.8 was installed and is refused with HTTP 403; upgraded);
  the intro and "पूर्ण विराम" clips are untouched, as is everything G1 / T3 / T4 share with T2 (the head bitmap, vo_demo1_purn,
  the intro). demo_check.py's T2 entry: the new picture box and first word. Nothing else in the file changed (index.html's
  T2 data and the three demo1 assets only). demo_check.py T2 against the new render: all pass — the picture box within 0.44 px,
  the sentence's ink within 0.5 px of the render's (size within 1), 0 solid pixel differences over the whole frame; T3 and
  T4 all pass; smoke 47/47; gate_check all pass. `../_before_demo1_pinki/` holds the dist's three files, build.py,
  recap_vo.py, demo_check.py, the 519:32 render and the old demo1_assets/.

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
- Later 2026-10-27, T3's picture replaced ([demo2-girl]; asked: "replace the image with this image, rest keep everything exactly
  the same"): the user's PNG, a girl in a pink dress waving, 90x135 with transparency (its ink 84x130), stored lossless with its
  alpha (exact) as demo2_assets/img_demo2_girl.webp -> assets/Images/, a new asset id (img_demo2_girl) in T3's data; the boy's
  file stays in the dist unused. Placed at its NATIVE size, its ink centred in the picture box's interior (2 px above and below):
  data.layout.img = [223, 214, 90, 135] frame px (the frame's "image 229" box was 204,215 130x128 — the boy filled the box's
  height; the girl is portrait, so the box takes her shape). At 1x it is upscaled on stages wider than 1280 px, like T2's. The
  render demo2_figma_render_1280x720.png (the visual target) now carries the girl in the boy's place — the interior painted
  white, the PNG composited at 223,214 — and the 521:288 render is kept as demo2_figma_render_1280x720_v1_2026-10-25.png.
  demo_check.py's T3 entry: the new picture box. Text, clips, timings, flow untouched. demo_check.py T3: all pass (the picture
  box within 0.44 px, the sentence within 0.5 px, 2 solid pixel differences); smoke 47/47. `../_before_demo2_girl/` holds the
  dist's three files, build.py, demo_check.py, the 521:288 render and the old demo2_assets/.

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
- Later 2026-10-27, G1 re-pointed at the Figma frame 656:66 ([g1-pinki]; asked: "replace the text and the image asset on that
  page with this exact as shown in this figma reference and apply the exact same animations and the same effects, make the new
  VOs accordingly; rest exactly the same"). The user's 1280x720 render of 656:66 (now g1_figma_render_1280x720.png; the 525:354
  render kept as g1_figma_render_1280x720_v1_2026-10-25.png) against the old one: the title bar, the tiles' bases and the third
  tile identical; the sentence "पिंकी गेंद से खेल रही थी" (ink 416..969, 553 wide — wider than the old 522 text box, and a
  line that overflows its box is START-aligned, not centred (the first build put it 17 px right): data.layout.sent is now 560
  wide at x 47.5 in the bar, its centre 692.5 on the render's ink, 64px as before), the slot 29 px further right (977..1035 = x 612 in the
  bar: data.layout.slot, the module's G2 hook), the picture — the girl with the ball (ink 208..330 x 214..343), CUT FROM THE
  RENDER at 1x (the Figma connector still unauthorized) at that box plus a 1 px white margin left / right / bottom (the top
  flush with the box's border), 125x131 lossless as g1_assets/img_g1_girl_ball.webp, a new asset id (img_g1_girl_ball; the
  boy's file stays in the dist unused), data.layout.img = [207, 214, 125, 131] — and the first tile's white face, whose top edge
  is 1 px higher on this frame (face [199, 444, 223, 162]; its bottom and sides, and the base, as before). recap_vo.py: g1's
  sent line is the new sentence, re-made (6 word times); the instruction clip and the name on the right tap (vo_demo1_purn) are
  untouched, and so is G2, which plays G1's instruction. pick_check.py's G1 entry: the new picture box, slot, sentence centre,
  first word, first face, ink region and the slot's own region. Flow, timings, wrong-tap wiggles, the engine's idle reminder: as
  before. pick_check.py G1 against the new render: all pass — the picture, slot and tile boxes within 0.5 px, the sentence's
  ink centre on the render's (0.0 px; size within 2), 0 solid pixel differences over the whole frame; smoke 47/47; gate_check
  all pass. `../_before_g1_pinki/` holds the dist's three files, build.py, recap_vo.py, pick_check.py, the 525:354 render and
  the old g1_assets/.

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
- Later 2026-10-27, G2's picture replaced ([g2-girl]; asked: "replace the image with this image, rest keep everything exactly the
  same"): the user's PNG, a girl in a pink dress with a yellow bag, 88x132 with transparency (its ink 84x127), stored lossless
  with its alpha (exact) as g2_assets/img_g2_girl_bag.webp -> assets/Images/, a new asset id (img_g2_girl_bag) in G2's data; the
  boy's file stays in the dist unused. Placed at its NATIVE size, its ink centred in the picture box's interior (3 px above,
  4 below): data.layout.img = [223, 216, 88, 132] frame px (the frame's box was 218,213 102x136). At 1x it is upscaled on stages
  wider than 1280 px, like T2's. The render g2_figma_render_1280x720.png (the visual target) now carries the girl in the boy's
  place — the interior painted white, the PNG composited at 223,216 — and the 600:197 render is kept as
  g2_figma_render_1280x720_v1_2026-10-25.png. pick_check.py's G2 entry: the new picture box. Text, clips, timings, flow
  untouched. pick_check.py G2: all pass (the picture box within 0.44 px, the sentence within 0.5 px, 2 solid pixel
  differences); smoke 47/47. `../_before_g2_girl/` holds the dist's three files, build.py, pick_check.py, the 600:197 render
  and the old g2_assets/.

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

The transition screens: the reference's lines, caption moments and scrim ([gate-ref-vo], 2026-10-29)
- Asked: "take the reference https://hi-02-h04-l01-s01-dun.vercel.app/ and apply the exact same transition animation screens with
  pink hindi texts along with the exact same VOs of the transition screens ... where ever used; rest keep everything exactly the
  same". Here the gates are: start -> T0 ("चलिए, शुरू करें!"), T4 -> G1 ("चलिए, साथ में करें!"), P2 -> L1 ("अब आपकी बारी!").
- Probed both pages side by side (the scratchpad's gate_probe.py: each gate opened directly, every 40 ms the gate's classes, the
  bird's box / animation / transform, the headline's box / text / computed look, the scrim, the clip and its time, every play();
  gate1_probe.py: the real first gate from the play button). The live reference = the local copy under Suresh's File byte for
  byte. Already the same: the texts, the bird (peeking_talk_up.webp, md5-identical), its size, lift and first-gate sink, the
  headline's font / colour / stroke / place / wipe, the 4 s hold, the gate script itself.
- Changed (build.py [gate-ref-vo] + the [dun-chrome] gate lines):
  1. the LINES: the reference's own vo_pt_tutorial / _guided / _practice (its .wav files, re-encoded to this engine's Opus-48k
     .ogg like vo_well_done; same decoded length, 0 lag, correlation .999, same loudness; dun_assets/Audio/vo_pt_*.ogg + .wav),
     with the reference card's texts. Before: the user's recording of vo_pt_tutorial (4.94 s) and TTS for the other two —
     `../_before_gate_ref_vo/Audio/` keeps them, and voiceovers/vo_pt_tutorial.wav is untouched. build.py copies the reference's
     clips on every build, so re-running vo_rec.py cannot bring the old line back;
  2. the CAPTION moments: the reference's 3660 / 3940 / 1120 ms into those clips (the gate script's line is now the reference's
     verbatim; [vo-rec]'s tutorial cue patch is gone);
  3. the SCRIM: rgba(57,55,55,.6) on every gate (the reference's TOTA-CONSIST-S05 rule; [dun-chrome] had copied its earlier
     PHASEGATE-ADD .35, which the reference itself overrides);
  4. the FIRST gate's blur: the reference's 10px backdrop blur plus the landing itself blurred 10px (was the engine's [28b] 15.8px
     backdrop with no filter).
  The dist differs from before in app.js (the caption line), style.css (the scrim + the start-gate blur), index.html (the
  tutorial clip's text) and the three clips. Not copied: the reference headline's max-width:86vw, which only matters below
  ~734 px of screen width, where it pushes the reference's own headline off-centre.
- Checked: the probe again — same clips, captions at 3725 / 3985 / 1148 ms (the reference: 3692 / 3971 / 1179 ms; both are
  timers from the gate's opening), the scrim / blur / bird / headline computed the same at every sample; the three headlines
  written out over a flat field are 0 px different from the reference's (title_pix.py); the first gate's field colour is the
  reference's to the pixel (85,113,131). gate_check.py (now also asserts the scrim, the 10px blur and the 2.32 s clip) ALL PASS;
  smoke.py 47/47 (run alone; run beside three other browser checks it once timed out at G4 -> P1, a page change with no gate). `../_before_gate_ref_vo/` holds build.py, gate_check.py, smoke.py, the dist's three files and the old clips.

No music bed on the letter page; it returns with the stamp page ([l1-quiet], 2026-10-29)
- Asked (page 13 L1): the background music should not play on this page; once the user taps the envelope and the transition is
  over, it should start again as it does now; everything else unchanged.
- Was: the bed ([BGM-DUCK]) runs under every page from the first to the last before the celebration, by index (FIRST 0 .. LAST =
  slides - 2), ducked under the letter page's narration, chime and piano loop; the page's own fadeBackgroundMusic() calls are
  no-ops since the bed owns its level.
- Built: the bed block's onSlide also reads the slide's no_bgm flag (wanted = in range AND not no_bgm), and L1's card entry carries
  no_bgm: true. So the bed fades out over 0.6 s (OUT_MS) as L1 mounts and is paused; the letter page plays with its own sounds
  alone; and when the envelope's dive and veil are over and L2 mounts, the bed starts again exactly as on its first page (its
  0.6 s fade-in, ducked under L2's line if one speaks) from where it paused. Nothing else moved: the dist differs from before
  in app.js (one line of the bed block) and index.html (the one flag); style.css byte-identical; the page's piano, chime,
  narration and the dive are untouched.
- Checked: letter_check.py — the bed not wanted, target 0 and paused at L1's mount; wanted, playing and its target up 0.8 s into
  L2; and, coming from P2 with the bed up, falling at 0.3 s and paused at 0 by 0.9 s after L1's mount: letter_check.py 42/42 (the scratchpad's chk29 log: 39 before + the three bed checks; its first run's fade block waited for a level the duck under P2's line never reaches, fixed to wait for the element to play); G4 / P1 / P2 27/27 each and smoke.py 47/47 on the same build (chk28).
  `../_before_l1_quiet/` holds build.py, letter_check.py, README.md and the dist's three files from before.

P2's right tap: the reference's picture pop with the pencils' sound ([p2-pencils], 2026-10-28)
- Asked (page 12 P2): the same as for G4 and P1 — the reference's page-5 (G2) image animation, synced with the user's sound
  "freesound_community-pencils-shake-throw-33800.mp3" (Downloads); everything else unchanged.
- The file: 17.3 s, mono 44.1 kHz, kept as given (bytes unchanged) at _reskin_tools/p2_assets/sfx_p2_pencils.mp3 and shipped as
  assets/Audio/sfx_p2_pencils.mp3. It is digital silence until 0.52 s (then the shaking, peaks near 0 dBFS). The reference's
  rule plays a tap sound for the 1 s hold only, so from 0 the tap would be followed by half a second of nothing: P2's data
  also says data.tap_sfx_from = 0.51 and the [g4-giggle] hook gained one line (a file with a lead-in starts at the given
  second — currentTime set before play(), the browser's default start position), so the shake lands with the pop and that
  first second of it plays, faded over the hold's last 150 ms and paused with it; the ding + confetti follow as before. G4
  and P1 start their files at 0 as before. The dist differs from before in app.js (the one line), index.html (two data
  fields) and the new audio file; style.css byte-identical. Say if a different second of the recording is wanted.
- Checked: g4_check.py's media trace now records the start position too (P2: 0.51 s; G4 / P1: 0): G4 27/27, P1 27/27, P2 27/27 and smoke.py 47/47 (chk28).
  `../_before_p2_pencils/` holds build.py, g4_check.py, README.md and the dist's three files from before.

P1's right tap: the reference's picture pop with the book's sound ([p1-book], 2026-10-28)
- Asked (page 11 P1): the same as for G4 — the reference's page-5 (G2) image animation, synced with the user's sound
  "soumages-book-opening-345808.mp3" (Downloads); everything else unchanged.
- Built: the file is kept as given (bytes unchanged, 1.10 s, stereo 44.1 kHz mp3) at _reskin_tools/p1_assets/sfx_p1_book.mp3,
  shipped by build.py's P1 asset copy as assets/Audio/sfx_p1_book.mp3, and P1's data names it (data.tap_sfx) — the module's
  [g4-giggle] hook does the rest: at the right tap the picture pops (the reference's p2BirdPop1s, unchanged) and the sound plays
  with it at .63, faded over the last 150 ms of the 1 s hold and paused with it; the ding + confetti follow as before. No new
  code; P2 stays without a tap sound. The dist differs from before in index.html (the one data field) and the new audio file;
  app.js and style.css byte-identical.
- Checked: g4_check.py's media trace on P1 (the sound with the mark at .63, once; paused ~1 s after the tap at ~0, before the
  ding), and P2 still without one: G4 27/27, P1 27/27, P2 27/27 and smoke.py 47/47 (the scratchpad's chk28 logs, the build that also carries [p2-pencils] and [l1-quiet]).
  `../_before_p1_book/` holds build.py, README.md and the dist's three files from before.

G4's right tap: the reference's picture pop with the giggle ([g4-giggle], 2026-10-28)
- Asked (page 10 G4): take https://hi-02-h04-l01-s01-dun.vercel.app/ as the reference and give G4 the exact same image animation as
  its page 5 G2, synced with the user's sound "jule_joule-giggling-like-a-little-girl-322689.mp3" (Downloads); everything else
  unchanged.
- The reference (its single-file build, cloned earlier into an older scratchpad: #P5-CORRECT-SFX-JS, CORRECT_SFX_BY_SLIDE[4] =
  the boy drinking water): on G2's correct tap the recall picture pops — p2BirdPop1s, 1 s (to 1.045 at 0.2 s, 1.03 held to
  0.72 s, back by 1 s) — and the page's own sound (sfx_drinking_water.wav) plays with it, a fresh Audio at volume .63, faded
  over the last 150 ms of the 1 s hold and paused with it; the green mark at the tap, the ding + confetti after the hold.
  Our G4 is the port of that game's P4 page and already pops its picture at the right tap with the very same keyframes and
  rule (compared value for value against the clone) — what it lacked was the page's own sound with the pop.
- Built: the giggle is kept as given (bytes unchanged, 1.06 s, mono 48 kHz mp3) at _reskin_tools/g4_assets/sfx_g4_giggle.mp3,
  shipped by build.py's G4 asset copy as assets/Audio/sfx_g4_giggle.mp3, and G4's data names it (data.tap_sfx). SENT_PICK's
  ok(): right where the picture gets .p2-pop, a page with data.tap_sfx plays it as the reference does — a fresh Audio at .63
  (sfxTrack'ed, so it counts as an effect for the tap hold), its volume ramped to 0 over the hold's last 150 ms in 16 ms steps
  and paused at 1 s, so it ends with the hold and the ding + confetti follow as before; muted = no sound. P1 and P2 have no
  tap_sfx and are unchanged. The dist differs from before in app.js (the hook), index.html (the one data field) and the new
  audio file; style.css byte-identical.
- Checked: g4_check.py now traces every media play / pause (an init script on HTMLMediaElement) — on G4 the giggle starts within
  60 ms of the green mark at .63, once on the page, and is paused ~1 s after the tap at volume ~0, before the ding; on P1 / P2
  no such sound: G4 27/27, P1 26/26, P2 26/26 (the scratchpad's chk27 logs); smoke.py 47/47.
  `../_before_g4_giggle/` holds build.py, g4_check.py, README.md and the dist's three files from before.

The demos' slot highlight in orange, the pointing hand at the auto tap ([demo-hand], 2026-10-28)
- Asked (pages 4 T2, 5 T3, 6 T4): when the empty box is highlighted with the mark inside it, its stroke should be the words'
  orange, not blue; and when the right option is auto-tapped, the same hand nudge (the picks') should appear at it; everything
  else unchanged.
- Built: (1) .dmf-blank.hot's ring is #E86A00 (the read word's orange, [word-hot]) and its 6 px glow rgba(232,106,0,.22), in place
  of the blue #386AF6 / rgba(56,106,246,.22); T4's solid ring inherits the same stroke, the mark's 1.22 scale and the grow are
  as before (two CSS values). (2) The shared module's hand code became one helper, showHand() — the same <img class="reveal-hand
  dmf-hand"> (nudge_hand_new.svg, 96 px, the guided bob, centred under the tile 4 px below it) the picks place at the third wrong
  tap — and stage 4 (the mark's name: the right tile tapped for the child) calls it as the tile presses; stage 5 (the second
  reading, every tile dim) removes it. So the hand points at the tapped tile through the name, the mark's landing and
  "अब दोबारा देखिए", and leaves as the sentence is read again. The picks' behaviour is unchanged (the same helper). Nothing else
  moved: the dist differs from before in style.css (two values) and app.js (the helper and two calls); index.html byte-identical.
- Checked: demo_check.py samples the hand (place, size, bob) and the hot slot's stroke and glow every frame: demo_check T2 43/43, T3 42/42, T4 43/43 (the scratchpad's chk26 logs: the three new checks included); pick_check G1 55/55 and
  smoke.py 47/47 on the same build (chk25; the hand helper is shared with the picks).
  `../_before_demo_hand/` holds build.py, demo_check.py, README.md and the dist's three files from before.

The story's first beat ends on the cat's sound and the picture's little pop ([story-cat], 2026-10-28)
- Asked (page 1 T0): after the VO of the first sentence is over, the user's sound "stu9-cute-cat-352656.mp3" (Downloads) plays
  once, synced with the little picture pop G4's picture gives; everything else unchanged.
- Built: the file is kept as given (bytes unchanged, 0.89 s, mono 22 kHz mp3) at _reskin_tools/story_assets/sfx_story_cat.mp3 and
  shipped by build.py's story-asset copy as assets/Audio/sfx_story_cat.mp3; T0's data names it (data.beat1_sfx). STORY_LISTEN:
  the moment beat 1's narration ends (sfigNarrate's end, before the one-second pause) the module plays it through the kit
  player (playKitSfx, volume .8, so mute and the music bed's ducking apply as to every effect) and gives beat 1's picture the
  class .sfig-pop — G4's own pop (p2BirdPop1s: up to a 1.045 scale at 0.2 s, back by 1 s, the one CSS line) on the picture
  alone; the grey frame clips the zoom as the frame's bitmap edge does on G4. Once per visit (a `popped` flag): the 🔊 chip's
  replay of beat 1 does not repeat it; the pause, the turn to beat 2 and all later beats are as before. Nothing else moved:
  the dist differs from before in app.js (the module), style.css (the one rule), index.html (the one data field) and the
  new audio file.
- Measured (story_check.py's sampler, every 25 ms): the sound starts in the same sample as beat 1's line ends (0 ms) and the pop
  with it (0 ms); one start on the whole page (none at the 🔊 tap in the first turn, none in beats 2-4); the picture's scale
  peaks at G4's 1.045 within the pop's first 0.35 s.
- Checked: story_check.py gained the three [story-cat] checks; its beat-1 layout and pixel shots, taken in the one-second pause
  (now the pop's second), hold the pop off for the rest state: story_check.py 61/61 (the scratchpad's chk24 logs; 58 before + the three new); smoke.py 47/47.
  `../_before_story_cat/` holds build.py, story_check.py, README.md and the dist's three files from before.

With the pointing hand the other tiles are dead and nothing speaks ([hand-quiet], 2026-10-28)
- Asked (pages 7 G1, 8 G2, 9 G3): when the hand nudge appears the other options should be disabled, and no VO should come at that
  time, even after the user taps the option the hand points at; everything else unchanged.
- Was: the third wrong tap wiggled its tile, placed the hand under the right tile and, 0.5 s later, spoke hint 3 (G2's and G3's own
  lines; G1, having none, said hint 2 again); the other two tiles stayed live (a tap wiggled them and said hint 3 again); the idle
  re-read came after 7 s of quiet and the chip read the sentence; the guided tap played the praise (vo_ok, "शाबाश!") before
  the page moved on.
- Built (PUNCT_PICK, the hint ladder's third rung): the third wrong tap places the hand, makes the other two tiles dead and dim
  (onclick off + .off, the demos' faded look; .dmf-live .dmf-tile.off also takes no pointer events — the one CSS line) and
  speaks nothing; the tile just tapped finishes its wiggle. From then on nothing speaks on the page: no hint 3, no idle
  re-read and no chip (state.replayAudio returns while the hand is up), and the guided tap presses the tile, lands the
  mark with the ding + confetti and no praise line, then the page moves on 1.7 s later (+0.3 s per extra mark) — the
  sentence picks' own guided-tap shape (mark, ding + confetti, no line). The un-guided right tap (fewer than three wrong
  taps) is unchanged: the praise, one beat, the page moves on. Nothing else moved: the dist differs from before in app.js
  (the module) and style.css (the one rule); index.html byte-identical; T2-T4 and the sentence picks untouched.
- Measured (the scratchpad's hand_probe.py, 1280x720, G1 / G2 / G3): at the third wrong tap (+120 ms) the hand is up, the two
  other tiles are .off (the tapped one still wiggling), no line; 1.2 s later no clip has started; a tap on a dead tile counts
  nothing; the chip says nothing; after 9 s of waiting still no clip (the re-read would have come at 7 s); the guided tap
  presses its tile and lands the mark at once with no clip, and the page moves on 1806-1888 ms later (G1 -> G2, G2 -> G3,
  G3 -> G4); no page errors.
- Checked: pick_check.py's main flow (three wrong taps, then the right one) now expects the quiet hand — the dead tiles and
  the silent chip, no line from the third tap to the page's end, the guided move-on 1.6-2.4 s after the tap, hint 3 and the
  praise never started — and its [tile-hit] block (one wrong tap, then the right one) still expects the praise and the
  move-on on the un-guided path: G1 55/55, G2 55/55, G3 54/54 (the scratchpad's chk22 logs); smoke.py 47/47; demo_check T2 40/40 (the CSS is shared).
  `../_before_hand_quiet/` holds build.py, pick_check.py, README.md and the dist's three files from before.

A tap on a tile's mark or name is that tile's: G2 / G3 judged taps by the wrong tile ([tile-hit], 2026-10-28)
- Asked (pages 8 G2 and 9 G3): a lot of problems tapping the right or wrong option — the tapped option, right or wrong, should be
  judged correctly and show its own right or wrong animation; everything else unchanged.
- Found (the scratchpad's g23_probe.py: each tile's parts and document.elementFromPoint at its visible points, at 1333x750 and
  1280x720): the tiles' own boxes are right (227x169 at 197 / 527 / 857), but the mark's and the name's text boxes are far
  wider than the tile — .dmf-sym 483 px and .dmf-name 1075 px, centred on the tile so the glyphs centre whatever their
  width (the frame's text nodes) — and so overflow onto the next tiles: tile 1's name box runs from x -236 to 884, over
  tiles 2 and 3. A later tile's box paints on top, so a tap on tile 1's NAME reached tile 2 and a tap on tile 2's name
  reached tile 3; the right third of a tile at the mark's height reached the next tile's mark too. The module judges by the
  tile that got the tap, so on G3 (the comma, tile 2) a tap on the wrong tile 1's name was judged right and the mark
  landed, and a tap on the right tile 2's name was judged wrong and tile 3 wiggled; on G2 (the ?, tile 3) taps on tile
  1's or 2's names wiggled the tile to their right. G1 (the danda, tile 1) mostly escaped, its answer being the first tile,
  which is why the earlier pick checks — Playwright clicks at each tile's box centre, where the tile's own mark sits — never
  saw it. Every judgement was right once the tap reached the right tile: the right / wrong animations themselves were
  never the fault.
- Built: .dmf-sym and .dmf-name take no pointer events (pointer-events:none, CSS only), so every tap on a tile's visible area
  — mark, name, face, base — falls to the tile's own box and the tile that was tapped is the tile that answers. Nothing
  drawn changes: the dist differs from before in style.css only (the one rule), index.html and app.js byte-identical;
  T2-T4 share the CSS but take no taps.
- Measured (g23_probe.py again): on G1, G2 and G3 at both viewports every probed point of every tile — the mark's and the
  name's glyph centres, the face centre, the tile's edges, the base's corners — now resolves to that tile; a real mouse tap
  on a wrong tile's name wiggles that tile alone, on the right tile's name presses it alone and lands the mark.
- Checked: pick_check.py gained the hit-test (seven points per tile) and the two mouse taps on the names: G1 52/52, G2 52/52, G3 51/51 (the scratchpad's chk21 logs); smoke.py 47/47; demo_check T2 40/40, T3 39/39, T4 40/40 (the CSS
  is shared with the demos; nothing drawn changed).
  `../_before_tile_hit/` holds build.py, pick_check.py, README.md and the dist's three files from before.

Only the tapped option answers, nothing answers while feedback sounds, no stray hand ([tap-lock], 2026-10-28)
- Asked (pages 7 G1, 8 G2, 9 G3, 10 G4, 11 P1, 12 P2): only the option tapped should show the right or wrong animation; why does
  the hand nudge (or anything else) sometimes stay on when jumping to another page; and while a VO or any sound effect plays,
  no other option or button should be tappable; everything else unchanged. Then, on the first build: why is the tapped option
  not showing its right or wrong animation at all?
- Found: (1) the picks' right tap pressed the tapped tile AND dimmed the other two (the demos' faded-option look); the wrong tap
  already wiggled only the tapped tile; on the sentence picks the right tap marks only the tapped pill and the wrong tap
  wiggles / crosses only the tapped pill. (2) Both page types append their pointing hand (the picks' after the 3rd wrong tap,
  the sentence picks' at the reveal) to .slide-stage — outside #slideHost, which is all clearHost() empties on a page change —
  so a dev-nav jump left the hand standing on the next page (reproduced: on T1 the sentence picks' hand even grew to 405x508
  under that page's CSS). Their idle loops and listeners do stop themselves (they check the page is still mounted). (3) A
  tap during a line CUT the line (the picks' idle re-read, the sentence picks' instruction / try-again line) and taps during a
  sound effect counted; the chips already refused taps during a line but not during an effect.
- Built: (1) the picks' right tap presses the tapped tile only — the other two stay as they are (the demos' auto tap, which
  is not a response, still dims them as before). The hint ladder is untouched: the sentence picks' 2nd wrong tap still reads
  all three pills in turn and the 3rd still reveals the answer (greyed decoys, ringed answer, the hand) — those are the
  reference's scaffold beats, not response animations; say so if they should go too. (2) The engine sweeps every
  .slide-stage .reveal-hand at the top of mountSlide (right after clearHost), so no page's hand outlives it. (3) The engine
  gained sfxBusy(): playSfx, the kit's playKitSfx (correct / wrong / confetti / star / buttons) and the procedural _tone mark
  themselves busy for their length (an 'ended' listener with a 6 s cap). The picks' tap() and the sentence picks' tap() — the
  tiles, the pills, the reveal hand and its pad — return while an effect sounds (sfxBusy()), and both pages' chip replays
  refuse while anything sounds (the engine's chip handler already refused during a line).
- The follow-up (same day): the first build held the options during EVERY line, the instruction and the idle re-read
  included. On G4 / P1 / P2 the instruction repeats after every 5 s of quiet and lasts about 4.4 s, on G1-G3 the re-read
  comes 6.5 s after the tiles go live and lasts about 2.7 s — so a tester tapping at a natural moment hit a held page about
  half the time and saw the tapped option do nothing, which read as "no right or wrong animation" (the scratchpad's
  feel_probe.py timelines). The ask was about feedback ("any OTHER option while one plays"), so the lock is now: a tap during
  the instruction, a repeat or the idle re-read cuts it and answers at once, as before; while a FEEDBACK sound or line plays
  — the buzz, the picks' hint 1 / 2 / 3, the sentence picks' try-again line and hint 3, the chime and the ok line — no other
  option, the hand or the chip answers. Each module keeps the feedback line's own Audio (fbAudio, set right after play() of a
  hint / try-again / hint-3 line) and tap() returns while sfxBusy() or that very clip is the one playing; the sentence picks'
  check now sits before stopNudge() / wordStop(), so a refused tap changes nothing. Nothing else moved: in both builds the
  dist differs from before in app.js only (index.html and style.css byte-identical); the T0-T4, L1, L2 and end-screen pages
  are not touched by the lock.
- Measured (the scratchpad's lock2_probe.py, 1280x720): G1 — a wrong tap during the idle re-read: counted, the tapped tile
  wiggles, the re-read cut and its highlight gone; a 2nd tap at +0.2 s (the buzz): still 1; the right tile during hint 1 and
  the chip during hint 1: nothing, the line plays on; the right tile in silence, or during the re-read: pressed, no tile
  dimmed. G4 — a wrong pill during the instruction: counted, crossed, the line cut; the right pill and the chip during the
  try-again line: nothing; the right pill during a repeat: the mark, the repeat cut. P1 — three wrong taps, the right
  (guided) pill during hint 3: nothing; once quiet with the hand shown: the mark. Earlier (lock_probe.py): G1 and G4, three
  wrong taps, the hand, a jump to T1: no .reveal-hand on T1 at once or 2.5 s later. No page errors anywhere.
- Checked: pick_check.py (the buzz hold, the hint-line hold, the re-read cut by a tap, the right tap's others untouched,
  the hand gone after a jump) and g4_check.py (the try-again-line hold, a repeat cut by a tap, the hand gone after a jump):
  on the narrowed build (the scratchpad's chk20 logs; app.js unchanged by the two changes after it) pick_check G1 49/49, G2 49/49,
  G3 48/48; g4_check G4 25/25, P1 25/25, P2 25/25; demo_check T2 40/40; smoke.py 47/47 once its own follow-up taps waited for
  quiet (it tapped again 0.5 s after a wrong tap, inside the hint line the hold now covers; a quiet(pg) helper, chk21).
  `../_before_tap_lock/` holds build.py, README.md, pick_check.py, g4_check.py, smoke.py and the dist's three files from
  before the first build; `../_before_tap_lock2/` the same (less smoke.py) from before the follow-up.

The big-slot pages' sentence at 50px, it and the slot centred together ([sent-50], 2026-10-28)
- Asked: on pages 4 T2, 5 T3, 7 G1 and 8 G2 make the main sentence 50px instead of 64 in the same font, place it at the centre
  of its box, and move the light-yellow blank box accordingly; everything else unchanged. Then, seeing it: the sentence and the
  empty box TOGETHER should be centred — as a pair they did not look centred.
- Before: the four big-slot pages set the sentence at 64px in each frame's text box (T2 at 96.5 in the bar, T3 / G2 at 120, G1
  560 wide at 47.5) with the slot at the frame's x (583 / 583 / 612 / 573) — on screen the ink ended 2.5-12.5 px before the slot
  and sat up to 32 px off the bar's centre (the frames' own placements).
- Built: data.layout.sent = SENT50 on all four — {x 0, y 18, w 719 - 63 = 656, size 50, lh 110, ws -3}: the text box is the
  719px bar LESS the slot's column (the 4px gap + the 59px slot), so the centred sentence and the slot right after it are
  centred on the bar as a pair (the first pass had the box the whole bar: the sentence alone centred and the pair 31.5 px right
  of centre — the user's eye was right); the font the same Story Noto Sans Devanagari SemiBold, the line box the 64px one (y 18,
  110px: the glyphs keep their vertical place), the word spacing the 50px pages' -3 (T4 / G3) — and each page's slot x = its
  sentence's ink right edge + 4 px, measured in Chrome at 1280x720 with the fonts loaded: T2 521.5, T3 496.5, G1 547.5, G2 495.5
  (the slot's size, y, dashes, blink and the mark in it unchanged; the mark stays 64px as the slot stays 59x100). The module
  needed no change (lay.sent / lay.slot were already its data). The built dist differs from before in those four slides'
  layout fields only (app.js, style.css and the rest of index.html byte-identical).
- Measured after the build (the scratchpad's sent50_measure.py): on all four pages the sentence is 50px / 110px, the pair's
  centre — from the ink's first column to the slot's right edge — 0.21-0.22 px (T2 -0.22, T3 -0.21, G1 -0.22, G2 -0.21) from the bar's centre (724.5), the sentence's vertical
  centre as before (280 / 280 / 277.5 / 280), and the slot's left edge 3.5 px after the ink's last column (the 4 px rule on the
  integer ink box).
- Checked: demo_check.py (T2 / T3) and pick_check.py (G1 / G2) carry the new boxes (the sentence box 656 wide at 0, 50px, the
  slots' new x) and, since the Figma frames still show the 64px text, measure the bar's interior directly (the sentence + slot
  pair centred within 1 px of 724.5, the slot 2.5-5 px after the ink, 45-62 px glyphs at y 276-283) and leave it out of the
  render diffs: demo_check.py T2 40 / 40, T3 39 / 39 (the pair centred within 0.22 px, the slot 3.5 px after the ink, 50px glyphs, the mark
  landing centred in the moved slot, every beat as before), T4 40 / 40 unchanged; pick_check.py G1 46 / 46, G2 46 / 46 (the
  same measures, the taps, hints and hand as before), G3 45 / 45 unchanged; smoke.py 47 / 47 on the same build.
  `../_before_sent50/` holds build.py, README.md, demo_check.py, pick_check.py and the dist's three files from before.

The read word lit as on G4 ([word-hot], 2026-10-28)
- Asked: on pages 4 T2, 5 T3, 6 T4, 7 G1, 8 G2 and 9 G3, when the words are highlighted one by one with the VO, light them in
  page 10 G4's orange with G4's exact word-by-word animation instead of the current light-yellow box; everything else unchanged.
- Built: the lit word on these pages is .dmf-sent .sfig-w.hot (the demos' second reading, word by word with the mark's name,
  and the pick pages' idle re-read); it was a light-yellow box (#FFF1B6 background + a 6 px ring). G4's lit word is SENT_PICK's
  .p2-word.on: colour #E86A00 and the p2WordPop animation (.28 s ease-out, once: scale 1 -> 1.1 at 45% -> 1, origin 50% 60%),
  one word at a time (the previous word returns to the sentence colour as the next lights). The demo/pick rule now says exactly
  that — color #E86A00, transform-origin 50% 60%, animation p2WordPop .28s ease-out 1 (the same keyframes, already in the
  stylesheet) — and the box's background-color / box-shadow transitions are gone with the box. One word at a time was already
  how these pages light (a punctuation-only token still lights with the word before it). Untouched: the words' arrival
  animation in the first reading, the timing of every highlight, the slot's own highlight (.dmf-blank.hot: the blue ring and
  the mark's 1.22 lift), the recap / story / stamp pages (their own rules). The dist differs from before in style.css only
  (that rule and its comment); index.html and app.js are byte-identical.
- Measured (the scratchpad's hot_probe.py, 1280x720, every frame of a read-out): T2's lit word rgb(232,106,0), animation
  p2WordPop 0.28 s, origin 50% 60%, transparent background, no shadow, each word's width peaking at 1.10x and back; G4's lit
  word reports the same colour, animation, duration and the same 1.10 peak (its stage is scaled 0.96 at that viewport).
- Checked: demo_check.py and pick_check.py now record the lit word's computed colour, animation, duration, background, shadow
  and width ratio in every frame of the read-out and require G4's values and a 1.07-1.13 peak: demo_check.py T2 39 / 39, T3 38 / 38, T4 40 / 40 (the second reading: every lit word rgb(232,106,0), p2WordPop 0.28 s, no
  background or shadow, the pop peaking at 1.112 / 1.102 / 1.105 of the word's width and back to 1.0 — every other beat and the
  frame match as before); pick_check.py G1 45 / 45, G2 45 / 45, G3 45 / 45 (the idle re-read's lit words the same, peaks 1.105 /
  1.107 / 1.107); smoke.py 47 / 47 on the same build.
  `../_before_word_hot/` holds build.py, README.md, demo_check.py, pick_check.py and the dist's three files from before.

P1's picture replaced ([p1-pic], 2026-10-28)
- Asked: at page 11 P1 replace the picture with the user's new one (two girls with the picture book, one pointing at its red
  car: a 1448x1086 PNG, the same size as the earlier source); everything else unchanged.
- Built: the new PNG is p1_assets/p1_book_source.png (the earlier one kept as p1_book_source_v1_2026-10-25.png) and
  g4_picture.py frames it exactly as before — P4's grey ring baked into the bitmap at 1058 px high, 1411 wide — into the same
  img_p1_book_gry.webp (the earlier picture kept as img_p1_book_gry_v1_2026-10-25.webp); the frame band of the new bitmap is
  identical to the old one's (same alpha, same grey), only the picture inside differs. The page's data, id, sentences, clips
  and layout are untouched; build.py gained only a comment and a docstring line, and the built dist differs from before in
  that one image file (index.html, app.js and style.css byte-identical).
- Checked: g4_check.py --page P1 23 / 23 (the page shows img_p1_book_gry.webp at its natural 1411 px width, the picture box 403x302 at
  438,140 of the page as before, the taps, hints, review and reveal as before); smoke.py 47 / 47 on the same build; no page
  errors or failed requests.
  `../_before_p1_pic/` holds build.py, README.md, the old source + framed picture (p1_assets/) and the dist's old copy.

The option tiles press as a whole ([tile-tap], 2026-10-28)
- Asked: on pages 4 T2, 5 T3, 6 T4, 7 G1, 8 G2 and 9 G3 the symbol options should be tappable as a whole: the complete option
  shows the tapping animation, not only the white box inside the grey stroke — for the auto tap and the child's tap alike;
  everything else unchanged.
- Found: the tap target was already the whole tile (.dmf-tile carries the onclick), but the press animation (dmfTap: a 6 px
  dip at 35% of .45 s and back) was on the white face alone (.dmf-tile.on .dmf-face). The mark and the name are the tile's
  children, not the face's, and the grey base is the tile's own layer — so on a tap the white box dipped under a mark, a name
  and a grey frame that stood still. The wrong-tap wiggle (wgNo) was on the tile already.
- Built: one CSS rule moved — .dmf-tile.on{animation:dmfTap .45s ease-out} — so base, face, mark and name press together on
  every tap: the demos' auto tap (T2 / T3 / T4, the module adds .on as the mark's name starts) and the child's right tap on
  G1 / G2 / G3. Same keyframes, same timing, same colours (the face's border and shadow rules are untouched: still no blue
  ring), the dim of the other two tiles unchanged. The dist differs from before in style.css only (that rule and its
  comment); index.html and app.js are byte-identical. Measured in Chrome at 1280x720 on G1: tile, base, face, mark and name
  all 5.7 px lower mid-press (the same frame), back at their rest tops 0.6 s later, the face with no animation of its own.
- Checked: demo_check.py and pick_check.py now sample the pressed tile's, its face's, mark's and name's tops in one frame and
  require them to dip together by 6 frame px (5-7, within 0.6 px of each other) and come back, the face animation-free: demo_check.py T2 38 / 38, T3 37 / 37, T4 39 / 39 (the auto tap: the tile, its face, mark and name dip together by 5.98 px
  and come back, the face animation-free, every other beat as before); pick_check.py G1 44 / 44, G2 44 / 44, G3 44 / 44 (the
  child's right tap: 5.98 / 5.69 / 5.98 px, the wrong taps' wiggle as before); smoke.py 47 / 47 on the same build.
  `../_before_tile_tap/` holds build.py, README.md, demo_check.py, pick_check.py and the dist's three files from before.

T3 and T4 without their intro line ([demo-intro], 2026-10-28)
- Asked: remove the title instruction VO "सुनो यह वाक्य बिना रुके पढ़ा गया" from pages 5 T3 and 6 T4; everything else unchanged.
- Built: that line is the two pages' intro clip (vo_demo2_intro and vo_demo3_intro, TTS: "सुनो, यह वाक्य बिना रुके पढ़ा गया ।";
  T2's intro clip says "आइए कुछ वाक्यों के उदाहरण से समझते हैं ।" and stays). On T3 and T4 data.intro_audio is now null and the
  slide's audio.prompt is gone (its prompt_hi, the engine's prompt text — hidden under the band on these pages — is the bar's
  line). The PUNCT_DEMO module needed no change: with no intro source it shows the title bar the moment the page mounts
  (its "else showBand()" path), the engine's play() fires the after-intro step 0.8 s later for a missing clip, and the same
  0.5 s beat follows — so the picture, the sentence bar and the tiles come in 1.3 s after the bar, the sentence's clip 0.65 s
  after they land, and everything from there (the blink, the name, the mark, the second reading, the explanation lines,
  T4's gate) runs as before. The two clips are off the dist (the asset map and assets/Audio; build.py unlinks them after the
  page's copy step, as it does the Chintu files); their sources and word files stay in demo2_assets/ and demo3_assets/.
  The built dist differs from before in those entries only (app.js and style.css byte-identical; index.html's cardData
  diffed field by field: the two slides' audio.prompt / data.intro_audio / prompt_hi and the two asset-map rows).
- Checked: demo_check.py learned pages without an intro line (the bar on mount, nothing sounding until the sentence's clip, no
  intro clip ever, the rest 1.1-1.7 s after the bar; T2 keeps the intro-line checks): T3 36 / 36 and T4 38 / 38 (the bar at 0-26 ms of the mount, the picture / bar / tiles 1.30-1.31 s after it, the sentence's clip
  0.65 s after they land, nothing sounding before it, the intro clip never heard, each remaining clip once, the beats and the
  frame match as before), T2 37 / 37 unchanged (its intro line still first); smoke.py 47 / 47 and gate_check.py 12 / 12 on
  the same build (T4's end still crosses the gate into G1). The first T4 run failed its new check only because the check
  required the bar to be absent from the sampler's first frame — the bar comes synchronously with the mount, so that frame
  may already show it; the condition is gone, the re-run passes with the same timings.
  `../_before_demo_intro/` holds build.py, demo_check.py, README.md and the dist's three files from before (the [band-title]
  build).

The demo and G2 title bars re-worded ([band-title], 2026-10-28)
- Asked: on pages 4 T2, 5 T3 and 6 T4 the title text becomes "विराम चिह्न का वाक्य में प्रयोग ।", and on page 8 G2 the title
  text becomes exactly page 9 G3's; everything else unchanged.
- Built: the title is the blue band's line, data.band_hi (the PUNCT_DEMO / PUNCT_PICK module's .dmf-pill p, 32px Noto SemiBold,
  left-aligned at 179.5,62 of the page, nowrap in a 1075px box). T2 / T3 / T4 had it from the demo intro lines' SHOWN text
  (demo*_assets/vo_demo*_intro.words.json: "सुनो यह वाक्य बिना रुके पढ़ा गया ।"); build.py now sets DEMO_BAND = the new line on
  all three. G2 had T4's text (frame 600:197's bar, [pick-fig]); it now takes G3's, gl["intro"]["shown"] = "वाक्य सुनिए और सही
  चिह्न लगाइए ।" (G1's instruction line, which is also what the three pick pages speak). Nothing else moves: the band's
  geometry is unchanged (the new lines are shorter: their ink ends at x 535 / 597 instead of 581), the intro clips still say
  what they said (the band's text was already independent of them — demo1's clip says "आइए कुछ वाक्यों के उदाहरण से समझते
  हैं ।"), slide.prompt_hi (the engine's prompt bar, hidden on these pages under the band) is untouched, and the built dist
  differs from before in those four strings only (app.js and style.css byte-identical; index.html's cardData diffed field
  by field).
- The reference renders: Figma frame 656:2 (T2) now carries the new line itself; 521:288 (T3), 523:320 (T4) and 600:197 (G2)
  still show the old one in Figma (528:424, G3, shows the instruction line). The band is pixel-identical across all these
  frames except its text ink (checked: 0 px differ outside x 180-595 of the text row), so the checks' renders now carry
  Figma's own rendering of each page's line: demo1 / demo2 / demo3_figma_render_1280x720.png have 656:2's band (36,26
  1208x120) pasted over their own, g2_figma_render_1280x720.png has 528:424's; the rest of each render is as before (the
  old files kept as demo1 / demo2 / g2 *_v2_2026-10-27.png and demo3 *_v1_2026-10-25.png). The band's ink in Chrome is
  within 1 px of centre and 2 px of size of Figma's (180-535 x 68-102 for the demo line, 180-597 x 68-105 for G2's).
- Checked: demo_check.py and pick_check.py now also assert the band's text (TITLE): demo_check.py T2 37 / 37, T3 37 / 37, T4 39 / 39 — the band's text is the new line and its ink sits on Figma's (mine 179-537 x
  68-103, the render's 179-535: centre 1.0 px, size 2 px), the content and whole-frame pixel diffs within their tolerances, every
  other beat as before; pick_check.py G1 43 / 43, G2 43 / 43 (its band now G3's line, ink 179-598 vs the render's 179-596), G3
  43 / 43; smoke.py 47 / 47 on the same build.
  `../_before_band_titles/` holds build.py, README.md, demo_check.py, pick_check.py and the dist's three files from before.

The re-listen page T0B: the two contrast sentences, their meanings, the moral ([relisten-pinki], 2026-10-28)
- Asked: at page 2 (T0B) replace the white box's text with Figma frame 654:567's; after the intro VO (vo_story_r0) the first and
  second sentences appear at the frame's placement and size with the same word-by-word animation synced to their VOs; then
  vo_story_r1 with a little zoom and the same light-yellow highlight behind the whole first sentence while the VO speaks of it,
  the same for the second; then 4.wav, in which the commas light in the same orange with a little zoom when the VO reaches
  that part; then the next button; all in smooth sync; everything else unchanged.
- Built (STORY_RELISTEN keeps its title / box / intro beat and the 🔊 chip; data-driven, the old one-block form still works):
  the box holds the frame's two sentence nodes — "उसे रोको, मत जाने दो।" (654:752: 401 wide, 30px, centred on 540.5,204.5 of
  the card's padding box) and "उसे रोको मत, जाने दो।" (654:753: 390 wide, centred on 540,302.5) — 8 px right of the box's
  centre, as the frame has them (its render: the ink centres at x 647 / 646.5 for a box centre of 640.5). data.lines gives
  each its clip and word times; sfigLine + sfigNarrate read them one after the other (0.6 s between), the words arriving
  on the clip's own clock as on T0. The clips are the user's two "माँ ने कहा ..." takes cut after their "माँ ने कहा," (vo_rec.py
  TRIM: 3.wav from 1.40 s -> vo_story_c1, the comma-after-रोको reading; vo_story_s1.wav from 1.45 s -> vo_story_c2, the
  comma-after-मत reading; the cuts in the pause before "उसे", measured on the waveforms), re-synced to the frame's words
  (story_assets/vo_story_c1 / c2.words.json). Then data.explain_audio = vo_story_r1 (the recording: "यहाँ पहले वाक्य का अर्थ है ...
  जबकि दूसरे वाक्य का अर्थ है ..."), 0.5 s after sentence 2: a cue list on the clip's clock (data.explain_cues, read by vo_rec.py
  off the clip: its "पहले" at 0.68 s and "जबकि" at 5.28 s) lifts sentence 1 (scale 1.06, 0.45 s) on the demos' hot-word yellow
  #FFF1B6 (.sfig-sent.hl, the box hugging the words), then sentence 2 in its place, both plain again 0.4 s after the clip.
  Then data.moral_audio = vo_story_moral (4.wav: "दोनों वाक्यों में शब्द एक जैसे हैं परन्तु विराम चिह्न अलग जगह लगा होने से ..."),
  0.5 s later: at its "विराम" (data.moral_cue 4.2 s) each sentence's comma — its own span (.sfig-mk) split off its word at
  mount — turns the picks' orange #E86A00 and lifts (scale 1.4, 0.45 s); they stay lit; 0.3 s after the clip आगे goes live.
  Each cued clip runs on a rAF tick of its own currentTime (cues not yet reached fire at its end; a 10 s watchdog past the
  authored length stops a stalled clip), so the beats sit on the voice, not on timers. The 🔊 chip replays the whole reading
  (sentences, explanation, moral) with the highlights cleared first; आगे is the reference's disabled pill until the moral
  has ended ([dun-chrome]). 4.wav and vo_story_r1.wav are no longer skipped by vo_rec.py (2 of the 75 remain: G1's राजू lines).
- Measured (the scratchpad's t0b_probe.py, 1280x720, every frame): r0 0-2.79 s; c1 3.44-5.98 (5 words); c2 6.59-9.14 (5);
  r1 9.65-19.95 with sentence 1 lit at 0.66 s of its clock and sentence 2 at 5.26, both off at +0.39 s; the moral 20.84-29.93
  with the commas lit at 4.18 s of its clock; आगे live at +0.32 s; no page errors.
- Checked: relisten_check.py rewritten for the page (usage: relisten2_figma_render_1280x720.png, the frame's render): 36 of 36 pass — the data (c1 / c2 / r1's two cues / the moral's cue), the title with the intro line, the box as it ends, each
  sentence word by word on its clip (no word early, none >150 ms late), sentence 2 0.6 s after sentence 1, the explanation 0.5 s
  after it with sentence 1 lit at "पहले" and sentence 2 at "जबकि" (both within 0.02 s of the cues), both plain 0.4 s after the clip,
  the commas lit at "विराम" (0.02 s), आगे the disabled pill through every clip and live 0.32 s after the moral, the 🔊 replay of
  the whole reading (highlights cleared, commas lit again, आगे back), आगे -> T1 with no extra gate, G4 clean of story styling,
  the title / box / two sentence nodes within 0.17 px of the frame on one line each in Noto SemiBold 64 / 30 px, the title + box
  pixel-matching the frame's render (0.94% of the area, 3 solid px over the whole card), no page errors or failed requests.
  Re-run after it on the same build: smoke.py 47 / 47, gate_check.py 12 / 12, story_check.py 58 / 58 (the T0 build untouched).
  `../_before_relisten_pinki/` holds build.py, vo_rec.py, relisten_check.py, README.md and the dist's three files from before
  (the files rebuilt from that build.py; their asset map also lists the three clips this change added, since derived.json
  is shared).

The story page T0 retold in four beats ([story-pinki], 2026-10-28)
- Asked: at page 1 (T0) replace the picture and the text with Figma frame 652:3's and make its VO; when that sentence is over,
  frame 652:192's picture and text on the same screen, then 660:127's, then 653:381's — each with the same synced animation —
  and then the next button; everything else unchanged. Then: the first two sentences centred in the white box like the third
  and fourth.
- Built: the STORY_LISTEN page keeps its layout, module and beat animation (the picture in the grey-bordered frame, the text
  word by word in the white box, the finished text leaving a second after its clip, the next picture over the last, its clip
  once it has landed, आगे once the last clip ends) and gets FOUR beats (data.beats; the module was already N-beat):
  1 "पिंकी बोली, “माँ बिल्ली रसोई में जा रही है।”" (652:3), 2 "माँ ने कहा, “उसे रोको मत जाने दो।”" (652:192), 3 "पिंकी ने पूछा,
  “क्या, उसे जाने दूँ ?”" (660:127), 4 "माँ ने कहा, “उसे रोको, मत जाने दो।”" (653:381) — the texts as the frames spell them,
  punctuation included (beats 2 and 4 differ by one comma). The pictures are the frames' own source bitmaps (download_assets:
  1774x887 for 1-3, 1672x941 for 4, saved as story_assets/img_story_pinki_{cat,listen,ask,maa}.webp) cropped by CSS exactly as
  each image node sits in its 430x224 box (.sfig-img.b1 -14,-3 458x229; .b2 -16,-4 462x231; .b3 -14,-2 458x229; .b4 0,-9
  430x242). The text boxes are the frames' nodes (.sfig-text.b1 427 wide centred on 532.5, 26px; .b2 / .b3 384 wide on 532,
  28px; .b4 395 wide on 531.5, 28px). The opening line "आइए इन वाक्यों को सुनते हैं।" (vo_story_s0, [vo-rec]) still comes first.
- The VOs: the four recorded takes in the user's batch ARE these lines (heard with whisper: 1.wav "पिंकी बोली माँ बिल्ली रसोई में
  जा रही है", 2.wav "पिंकी ने पूछा, क्या उसे जाने दूँ?", and two "माँ ने कहा उसे रोको मत जाने दो" — vo_story_s1.wav and 3.wav —
  told apart by their pause, measured on the waveforms: vo_story_s1.wav breathes after "मत" (beat 2, no comma), 3.wav after
  "रोको" (beat 4, "उसे रोको, मत जाने दो")). So no TTS was generated: vo_rec.py (RENAME) re-containers them as vo_story_b1..b4
  (Opus, assets/Audio), and re-derives each beat's word times from the recording (story_assets/vo_story_b*.words.json; a mark
  such as "?”" lights with the word before it). 4.wav (the moral: "दोनों वाक्यों में शब्द एक जैसे हैं परन्तु विराम चिह्न ...")
  and vo_story_r1.wav (the two meanings) belong to this story too but no page carries them yet: T0B still re-reads the Chintu
  story (its TTS lines), as asked ("rest keep everything exactly the same"). The Chintu beats' files (img_story_chintu*.webp,
  vo_story_s1 / s2.ogg) are removed from the dist; their sources stay in story_assets/.
- The centring: the frames' texts end with spaces (two on the first), which this build had first reproduced as trailing
  no-break spaces; on beats 1 and 2 that space wrapped onto a second line and lifted the text 17 px, and Figma's own renders
  show no such shift anyway (every sentence's ink within 1.5 px of the box's centre). The rule is gone: all four sentences now
  sit on the box's centre (ink centres within 0.5 px, measured in Chrome at 1280x720).
- Checked: story_check.py rewritten for N beats (usage: the four renders story_b1..b4_figma_render_1280x720.png): 58/58 — the opening line then the four beats' word sync (none early, none late), the three turns (text leaves at 1.0 s, picture at the turn, the next clip ~0.65 s later), a 🔊 tap in the first turn ignored, the disabled pill through the beats and the live, breathing one once the last clip ends, the replay of the last beat, a stalled last clip, every frame element within 1 px of its frame and each beat's picture + text box pixel-matching its render (under 5 %), आगे -> T0B; and the whole suite after it (see the [vo-rec] checks line).
  `../_before_story_pinki/` holds the dist's three files as built just before (rebuilt from the reversed edit, since both
  changes happened in one uncommitted session), build.py, README.md, story_check.py and the Chintu story assets from before.

The recorded voice-overs in their places ([vo-rec], 2026-10-28)
- Asked: "I have added the folder (voiceovers) which contains all the new VOs so now implement all these VOs to their respective
  places and it must be sync." The folder (`HI02H12_L01_S01_dist/voiceovers/`, 75 wavs, 24 kHz mono; copied to `vo_rec/` as the
  build's source) holds the 71 lines of the VO manifest (named by Audio ID) and four numbered takes. Every file was heard with
  faster-whisper (small, Hindi, word timestamps; `vo_rec/transcripts.json`) and checked against the manifest's script: 63 of the
  71 named lines are their script (whisper's spelling aside); the demo's sentence / full reading and the recap's पूर्ण-विराम
  example say "पिंकी" where the manifest says "रीना" (the artist worked from the renamed frames: used, the recap example's text
  changed to "पिंकी स्कूल गई ।" to match); G1's sentence and hint 3 say "राजू गेंद से खेल रहा था" where the frame (656:66) shows
  "पिंकी गेंद से खेल रही थी" (NOT used: the TTS sentence stays, hint 2 is said again in hint 3's place — re-record with पिंकी); the
  story recordings are a DIFFERENT story: 1.wav "पिंकी बोली माँ बिल्ली रसोई में जा रही है", 2.wav "पिंकी ने पूछा, क्या उसे जाने दूँ?",
  3.wav "माँ ने कहा, उसे रोको मत जाने दो", 4.wav "दोनों वाक्यों में शब्द एक जैसे हैं परन्तु विराम चिह्न अलग जगह लगा होने से वाक्य का पूरा
  अर्थ ही बदल गया", vo_story_s1 "माँ ने कहा उसे रोको मत जाने दो", vo_story_r1 "यहाँ पहले वाक्य का अर्थ है ... दूसरे वाक्य का अर्थ है ..."
  — none of it is the चिंटू / दादी story the pages T0 / T0B show (frames 435:5, 476:198, 488:190), so those six are NOT used and the
  story's run-on and re-read keep their TTS lines; the two intro lines (vo_story_s0, vo_story_r0) are the recordings.
  (Later that day the user re-pointed T0 at that very story — frames 652:3 ..: see [story-pinki]; 1 / 2 / 3.wav and
  vo_story_s1.wav are its four beats now; 4.wav and vo_story_r1.wav still wait for a page.)
- The pipeline: `python -I -X utf8 vo_rec.py` (then build.py) — re-containers each used recording to assets/Audio/<ID>.ogg
  (Opus 48 kHz, no gain: the recordings sit within 2-4 dB of the clips they replace), cuts vo_stamp_sent4 (15.4 s, the deck's one
  line for the letter's last block) into rounds 4 and 5 at the word boundary before "उनके" (4.34 s), re-derives every synced
  line's word times (the *_assets/*.words.json files build.py already reads) by lining the page's SHOWN words up with the clip's
  heard words (an order-keeping fuzzy match, nukta-blind, a bare mark matched to the word the voice says for it — "पूर्णविराम" for ।
  in the G4 options; words the clip does not say — T4's "अल्पविराम," tokens, the picks' bare ।/? — spread over the pause between
  their neighbours, so a slot lights in the voice's pause), and reads the gate caption's cue (the start of "चलिए" in
  vo_pt_tutorial: 2940 ms). `vo_rec/derived.json` carries the applied IDs + texts, the skipped files with reasons, the cue.
- build.py [vo-rec] gives the card the 68 clips (assets.audio + audio_text) and the deck's beats their places (JS hooks, all
  data-driven: a page without the field behaves as before):
  T0 "आइए इन वाक्यों को सुनते हैं।" (data.intro_audio) before the story, the chip waiting it out. T1 the lead "आपने देखा, ..."
  (data.lead_audio) before the intro, the title still out; the nine row lines recorded + re-synced. T2-T4: the sentence and the
  full reading recorded + re-synced; the mark's name at the tile = the recap's recorded names (vo_recap_*_name — the TTS
  vo_demo1_purn / demo2_prashn / demo3_alp retired); T2: the conclusion (vo_demo1_conclude) after the full reading; T3: the
  explanation (vo_demo2_explain) after the sentence, "अब दोबारा देखिए ।" (vo_demo_again) before the full reading, the conclusion
  after it; T4: the explanation and "अब दोबारा देखिए ।" (a 350 ms breath before each such line, 300 ms after; T3's / T4's full
  readings do not name the mark: the ? lights as the sentence ends, the commas in the pauses). G1-G3: the intro (vo_g1_intro) on
  all three, G2's / G3's sentences recorded; the right tile = "शाबाश!" (vo_ok, data.ok_audio) in the name's place; the deck's hint
  ladder on wrong taps — 1st = hint 1 (vo_build_hint1), 2nd = hint 2 (vo_build_hint2), 3rd and later = hint 3 (vo_g2_hint3 /
  vo_g3_hint3; G1: hint 2 again) + the pointing hand under the right tile until it is tapped (the sentence picks' reveal hand,
  .dmf-hand) — each line 0.5 s after the wiggle, skipped if something still speaks. G4 / P1 / P2: the prompts (vo_g4_prompt;
  P1 / P2 their own vo_p1_prompt / vo_p2_prompt), the nine option lines recorded + re-synced; the 1st wrong = hint 1 (vo_g4_hint1
  / vo_pick_hint1, the try_again slot), the 2nd = the three pills read (the engine's review = the deck's hint 2 note), the 3rd =
  "यह सही वाक्य है, इसपर टैप कीजिए" (vo_pick_hint3, audio.hint3) and then the hand; the right pill first try: "शाबाश! यह सही वाक्य
  है ।" (vo_ok_pick, audio.ok) then its own line with its words lit (the guided tap after the reveal: the ding + confetti alone, as
  before). L1: the narration (vo_letter_intro, 11.4 s) over the girl writing with the shimmer; the scene's beats (the thinking
  girl, the bubbles, the cloud, the chime, the letter) follow it. L2: the instruction recorded; each later round opens with the
  deck's line for it before its stamps pop in (round 2: vo_stamp_intro again; 3: "यह वाक्य सुनकर देखिए ..." = vo_g1_intro; 4 and 5:
  vo_stamp4_intro), the idle reminder says that round's line; the five sentences recorded + re-synced; wrong drops per round —
  1st = the wiggle alone, 2nd = hint 2 (vo_stampN_hint2), 3rd and later = hint 3 (vo_stampN_hint3; rounds 4 / 5: the open slot's
  own line by its mark — vo_stamp4_hint3_prashn / _purn / _alp) + the guidance glide to the open slot (hint(force): in a round
  without guidance too); a round's last slot = "शाबाश!" (vo_ok) with the chime. The title's welcome (vo_landing) and the first
  gate's line (vo_pt_tutorial, caption at 2940 ms) recorded. The celebration keeps the reference's vo_well_done ([cel-vo]).
- Still TTS (no recording in the batch): the three demo intros (the bar's line: vo_demo1_intro "आइए कुछ वाक्यों के उदाहरण से समझते
  हैं", vo_demo2/3_intro "सुनो, यह वाक्य बिना रुके पढ़ा गया"), the two later gates (vo_pt_guided, vo_pt_practice), the story's run-on
  and re-read (vo_story_s1 / s2 / r1), G1's sentence (vo_g1_sent). The VO manifest's "when" line for अल्प विराम is the deck's full
  sentence ("थोड़ा रुकने के लिए या अलग-अलग नाम ...") while the frame's row shows "वाक्य में थोड़ा रुकने पर": the row's words light
  over the first 1.2 s of the recording and the line runs on.
- Measured (the scratchpad's vo_flow_probe.py / vo_probe2.py / vo_probe3.py, every page driven, every play() logged): T0 s0 then s1;
  T0B r0 then r1; T1 lead 0 s, intro 6.9 s, purn_name 13.1, _when 15.1, _eg 17.6 ...; T2 intro, sent 5.1, purn_name 11.0, full
  13.8, conclude 17.9, T3 at 26.2; T3 intro, sent 5.0, explain 7.5, prashn_name 17.2, again 20.8, full 23.1, conclude 28.3; T4
  intro, sent, explain 9.4, alp_name 21.9, again 25.3, full 27.5, the gate; G1-G3: intro, the sentence, wrong 1 → hint1, wrong 2 →
  hint2, wrong 3 → hint3 (G1: hint2) + the hand, the right tile → sfx + vo_ok; G4 / P1 / P2: the prompt, wrong 1 → hint1, wrong 2 →
  the three pills, wrong 3 → hint3 then the hand; G4 right first try → vo_ok_pick 5.3 s then vo_g4_o1 8.3 s; L1 narration 0 s, the
  chime 19.0 s, the pop / paper on the tap; L2 intro 0.4, pops, sent 6.3, the right drop → thud, chime + vo_ok; round 2 opens with
  vo_stamp_intro (23.3 s), sent2, wrong 1 → the wiggle alone, wrong 2 → hint2, wrong 3 → hint3 with the right stamp lifting and
  gliding (27 samples of 100 ms), the right drop → vo_ok. No page errors anywhere. smoke.py 47/47 (its wait for the letter's
  pulsing envelope lengthened for the narration).
- Found by the page checks the same evening, fixed (all in the same tag): (1) build.py's asset steps copy each page's clips
  from its *_assets/ folder into the dist on EVERY build — so the 36 recordings vo_rec.py had written into assets/Audio
  (the recap rows, the demos' sentences and full readings, G1's intro, G2's / G3's sentences, G4 / P1 / P2's prompts and
  options, the stamp instruction and sentences) were put back to their TTS clips by the build that followed, with the
  recordings' word times on them. vo_rec.py now writes each recording into the folder build.py copies it from as well
  (the TTS original kept beside it as <ID>.tts.ogg), and an audit decodes every built clip against its recording's length
  (72 of 72 within 60 ms). (2) The alignment: whisper's last-word END may overrun the file (vo_demo3_sent: 4.72 s in a
  3.95 s clip), which put a mark's time past the clip's end; a line the recording says differently (the अल्प-विराम "when"
  row: 2 of 5 words matched) stacked three words at 0 s; whisper's joined words ("उड़ारही") gave two words one time.
  align() now clamps to the clip's length, spreads the shown words evenly when fewer than half match, spreads joined words
  over their span, and lets a bare mark take a free heard word (its spoken name, "लड़की पूर्णविराम पतंग") or else the word
  before it. (3) The engine's sfigNarrate tick could hide the last word again after the clip's end (the recap's "?" stayed
  off and its p wrapped): the tick now stops once the clip has ended. (4) The checks themselves: the three story-page
  checks still watched the pre-[dun-chrome] आगे (<img> arts, nextBtnPulse, a 198x90 box) and threw in the page — now the
  text pill (.active, its ::after navBreathe, 170x62), and its disabled art IS shown through the clips (the reference's
  way, as [dun-chrome] 2 says); demo_check / pick_check / g4_check / gate_check / letter_check / stamp_check learned the
  new beats (clip IDs, the explain / again / conclude lines, the praise before the pill's line, the hint ladder + hand,
  each page's own prompt, the narration before the letter scene, each round's own line before its pops, the 2940 cue).
- Checked (every page check + smoke on the final build of the day, after [story-pinki]): story_check 58/58 (the four-beat page, see [story-pinki]), relisten_check 26/26, recap_check 46/46, demo_check T2 36 / T3 36 / T4 38 all pass, pick_check G1 / G2 / G3 42 each all pass, g4_check G4 / P1 / P2 23 each all pass, stamp_check 126/126, letter_check 39/39, gate_check 12/12, title_check 16/16, smoke 47/47 — no page errors, no failed requests anywhere.
- `../_before_vo_rec/` holds the dist's three files, build.py, README.md, every check script, every *_assets/*.words.json (words/)
  and the 38 replaced clips (Audio/, from git HEAD) from before.

The celebration's line is the reference's ([cel-vo], 2026-10-28)
- Asked: take https://hi-02-h04-l01-s01-dun.vercel.app/ as the reference and "apply the exact same VO, bird animation and the finish
  button exactly the same at the celebration screen". Both celebration screens were probed in Chrome at 1333x750 (the
  scratchpad's cel_probe.py: the last slide mounted, then every 40 ms the sprite's sheet + frame + box, the finish button's class /
  box / look / animation, the clip and its clock, every play(); screenshots; then the tap). Already the same, value for value
  ([dun-chrome] 7): the standard confetti sound at 0.45 on the mount; the bird (.cel-art) on the शाबाश sheet - the jump 0-29 at
  45 ms a frame from the screen's first smooth paints, the landing 30-35 - then the talk sheet lip-synced to the line, then the
  idle loop; 314x420 at 509.5,79 at rest; the finish button (the gold pill 133.6x88 at 599.7,521, #FCB717, 4 px white ring, the
  arrow glyph 37.6x52) grey (.55, grayscale) and untappable while she speaks, then celArrowPulse 1.3 s; the tap = the standard
  next sound at 0.9 and the hand-over (ours also sends this engine's completion events and takes the tap once; the reference's
  button stays pressable - a difference of plumbing, not of look). The ONE difference was the LINE: this lesson's vo_celebrate
  (4.7 s, "बहुत बढ़िया! तुमने सही जगह रुकना ... सीख लिया।") in place of the reference's vo_well_done (2.94 s, "बहुत बढ़िया, दोस्त!
  तुमने कमाल कर दिया!") - and with it the beak's bits and the moment the arrow goes live (6.6 s in here, 4.9 s there).
- Now the reference's own clip and sync: its vo_well_done.wav re-containered to this engine's .ogg (Opus 48 kHz like every clip
  here; `dun_assets/Audio/vo_well_done.ogg`, 2.95 s, nothing changed in time), the reference card's own beak bits (117 x 25 ms,
  `dun_assets/cel_bits_ref.json`, with its text) and its text in the card: the CEL slide's audio.prompt + prompt_hi, assets.audio +
  audio_text, end_anim.vo + bits + step_ms (build.py [cel-vo], after the [dun-chrome] card step). vo_celebrate.ogg stays in
  assets/Audio, unused. NB the VO manifest (HI02H12_L01_S01_VO_Manifest.xlsx, 2026-10-28) still lists the celebration line as
  vo_celebrate with the old text; that row is now vo_well_done, "बहुत बढ़िया, दोस्त! तुमने कमाल कर दिया!" (the reference's recording
  is used as is, so nothing to record).
- Measured after (cel_probe.py, three runs each): the line's play() 1712 / 1712 / 2071 ms after the mount here, 1690-1704 there
  (the one slow run = the runner's own "three smooth paints or 0.7 s" start, a headless hiccup the reference's identical runner
  can have too); vo_well_done.ogg from the landing, 2.9 s, the talk sheet's beak following its bits; the arrow live 5.1-5.2 s
  in (4.9 there: the same gap after the line); the sprite and the button boxes identical to the reference's to 0.1 px; the tap:
  sfx_next_button at 0.9, lesson_complete + proceed posted. `../_before_cel_vo/` holds the dist's three files, build.py and
  README.md from before.

The speaker chip on the title-bar pages T2-T4, G1-G3 ([band-chip], 2026-10-28)
- Asked: "From page 4 T2 to page 9 G3 why haven't you placed the speaker button icon just like the other pages, along with the
  exact same animation? Place the exact same speaker button icon on these pages as well with the same animation effects. Rest keep
  everything exactly the same." The six pages are the Figma-bar pages (T2, T3, T4 = PUNCT_DEMO; G1, G2, G3 = PUNCT_PICK). They
  mount in the tutorial card (the whole stage, .sfig-full), which already carries the engine's .tut-audio chip - the very same
  inline-SVG speaker as the header chip of G4 / P1 / P2, wired to replaySlideAudio and to setPlaying's .playing / vo-disabled -
  but [demo-fig] had hidden it together with the standing Swiftie on 2026-10-25 (the frame's only Swiftie is the head in its
  title bar, and the chip had sat at that absent bird's feet). The chip is shown again, placed as G4's header chip is to ITS
  bird: G4's chip is 66 stage px at (94.5,80) by the 118 px circle at (16.5,18), i.e. its centre .8814 r right of and .6102 r
  below the circle's centre, on the bird's bottom-right shoulder; the bars' circle (.dmf-head) is 121.34 x 124.97 stage px at
  (37.49,27.08), so the chip's box is (118.6,94.7) 66 x 66 in stage px (the card IS the stage on these pages).
- The look and the states are G4's: the drop shadow on the element and the in-SVG shadow off (the ring's bottom would be
  clipped), hover 1.06 / press .95; grey (opacity .5, grayscale, brightness 1.2) and untappable while a line speaks
  (body.vo-playing), switched at once as there; the arcs blink while a line speaks (.playing, wv1 / wv2) and stand solid at rest;
  and - the reference's header-chip rule, [SPK-AFTER-VO] - grey until the page's opening lines are over: on T2-T4 the demo runs
  itself to the end (the engine's replaySlideAudio refuses the tap while state.demoRunning anyway), on G1-G3 until the tiles are
  the child's (.sfig-in.dmf-live); then a tap reads the sentence again, word by word highlighted (state.replayAudio, the same read
  as the 7 s idle reminder), the chip grey with its arcs blinking meanwhile. It comes in with the title bar (bandChipIn, the
  bar's own .55 s settle from -14 px / .97, fading up to whichever opacity the state has - the keyframe's end reads --chip-op,
  so a grey chip lands on .5, a live one on 1, no fill to snap from; nothing is drawn until the bar is in). CSS only
  (build.py's band_chip_css, appended after the [dun-chrome] block): the pages' modules, flows, clips, boxes and every other page
  (T0 / T0B / T1's card chip, G4-P2's header chip, L1, L2) are untouched. L2's bar (page 14) was not asked for and is as it was.
- Measured (the scratchpad's chip_probe.py, 1333x750): G1 - before the bar: opacity 0, untappable, scaled .97; with the bar in and
  the intro / sentence sounding: 66x66 at 118.6,94.7, grey (.5, grayscale), pointer-events none; the moment the tiles go live and
  nothing speaks: opacity 1, colour, tappable, arcs solid; a tap: vo_g1_sent plays again with the words lit (.hot), the chip grey
  and wv1 blinking; after it: colour again. T2 - 172 samples through the demo: always grey and untappable, state.demoRunning
  true throughout, arcs blinking exactly while a line speaks. demo_check.py (T2 / T3 / T4) and pick_check.py (G1 / G2 / G3) now
  expect the chip (its box, grey through the opening lines; the pick pages also: live once the tiles are, the tap's re-read, grey
  + blinking meanwhile, colour after) instead of "no chip", and leave the chip's measured box (plus its shadow) out of their
  pixel diff against the Figma render, as they do the bar's live bird head (the grey disc over the pale pill had added ~480
  solid differing px on the pick pages, just over their 0.05 % bar; ~330 on the demo pages, just under). Results: smoke 47/47;
  demo_check T2 36 / T3 36 / T4 38 all pass; pick_check G1, G2, G3 39 each, all pass. `../_before_band_chip/` holds the dist's
  three files, build.py, README.md, demo_check.py and pick_check.py from before.

The cover's sky seen, the play button's fade ([cover-sky], 2026-10-28)
- Asked (the cover alone, again): take https://hi-02-h04-l01-s01-dun.vercel.app/ as the reference and apply, exactly the same, the
  cover page's background animation and the play button's placement, position, sound, appearing animation and look. The reference
  page is unchanged since [dun-chrome] (md5 64ddd90b, the local copy still byte-identical). Both covers were probed in Chrome at
  1333x750 (the scratchpad's cover_probe.py: every 100 ms the sky and the glow, the button's class / box / computed opacity /
  animation, the bird, the chip, every play(); screenshots through the reveal and the tap) and compared value for value. Already the
  same in both: the glow (sgBreathe 6.5 s, the same gradient), the 87 stars on the kit's own lanes (the per-star size / speed /
  delay are random per load there and here alike), the hole 40 px inside the card, the button's art (btn-play.svg), 140 px,
  centred on the card with its bottom edge 2 px above the card's bottom, hidden until the welcome has ended, then sgBtnReveal
  .52 s cut over by sgBtnPulse 1.4 s / 1.04 at ~.3 s, the tap = the standard play sound at 0.8 and the tutorial line at once (the
  reference's sfx_std_play.wav is this file's sfx_play_button.ogg). Two things were NOT the same, both in the 10-27 port's own CSS:
  1. The stars and the glow were built (87 <i>, sgBreathe running) but never SEEN: the kit's sky-adapt rule
     `.start-gate{background-image:startnew_bg_plain.webp}` (meant for the gate off the title page) painted a second sunburst on
     the start gate, which sits in the stage at z 80 above the fixed sky layer at z 0. The reference keeps its gate transparent on
     the title page by its own early rule `body.is-start .start-gate{background:transparent}` (which its kit block silently relies
     on, and which this file never had: its gate's base rule is transparent, but the kit's later same-specificity rule won). That
     rule is now in the [dun-chrome] block. A side effect put right with it: the first gate's field is now the plain blue (the
     .start-bg's #7FC8F4, TOTA-GATE-NO-STARS) instead of the gate's own sunburst - the reference's look.
  2. The pop-in had no fade: the ported `.sg-fig .sg-btn, .sg-fig .sg-btn.ready` rule carried `opacity:1 !important;
     filter:none !important` (the reference has those two only on its waiting state, :not(.ready)), and an !important
     declaration beats a keyframe, so the disc appeared fully opaque at scale .55 instead of fading in from 0. Dropped; nothing on
     this file dims .sg-btn (grep: no opacity / filter rule on it).
- Measured after (cover_probe.py on the built page): at the moment .ready lands the button's computed opacity is 0 (was 1; the
  reference's is 0), at ready + 120 ms it is 1 at scale .99, then 140x140 at rest and breathing; the stars, sparks, rings and dots
  drift around the card and the glow breathes under it; the tap: sfx_play_button at 0.8, vo_pt_tutorial 30 ms later; the first
  gate: the blurred cover over the plain blue field, as the reference's tap+1.75 s shot. The build is still byte-identical to
  the previous dist but for the two CSS changes (the unchanged build.py was run first and reproduced the dist exactly; the clone
  of github.com/siddharthsharma-ctrl/Ek-aur-Anek that build.py takes as its first argument is not under _reskin_tools/ref - clone it
  into the scratchpad, depth 1, commit 677222f). title_check.py has two new checks: the start gate's computed background is
  none / transparent on the cover, and the button's opacity read synchronously by a MutationObserver when .ready lands is "0";
  ALL PASS (the frame's geometry within 0.28 px, the card's pixels 0.83 % off, the welcome / button / chip / bird / sky / burst
  as before); smoke.py 47/47. `../_before_cover_sky/` holds the dist's three files, build.py, README.md and title_check.py from
  before.

The chrome of HI02H04_L01_S01 on this file ([dun-chrome], 2026-10-27)
- Asked: take https://hi-02-h04-l01-s01-dun.vercel.app/ as the reference and apply, exactly the same, (1) the cover page's
  background animation and the play button's placement, sound, appearing animation and look, (2) the next button, its sound,
  placement, look and animation, (3) the bird animation and the bird animations in the title-bar circle wherever used, (4) the
  speaker button's placement, animation and functionality wherever used, (5) the confetti and the transition screens, (6) the
  background music exactly as there till the end, (7) the celebration screen replaced by that file's; everything else unchanged.
- The reference is the same SwiftPAL engine family as this file's chrome (Ek-aur-Anek is 2026.07.28t, the reference is
  2026.07.16i plus ~90 later override blocks). The local copy `Suresh's File/HI02H04_L01_S01-20260916T080241Z-1-001/
  HI02H04_L01_S01/HI02H04_L01_S01.html` is byte-identical to the live page (md5 64ddd90b), so its code and assets are the source.
  The blocks that carry the seven asks are kept verbatim in `dun_assets/blocks/` (cut by their own <style id> / <script id> and
  kit BEGIN/END markers; build.py reads them and applies the adaptations listed in its [dun-chrome] section); the reference's
  assets in `dun_assets/UI/` (the Ek-aur-Anek versions of the six files that get overwritten are kept once in
  `dun_assets/_replaced/`). Only three reference files were NOT needed: its sfx_std_play / next / confetti are this engine's
  sfx_play_button / sfx_next_button / sfx_celebrate (correlation 1.000, same cuts), so only their volumes changed (0.8 / 0.9 /
  0.45, the reference's STD_SFX_VOL); its bgm_standard_2.wav is this file's standard_background_music_2.mp3 note for note.
- 1 (cover): the FLN animation kit's sky - the breathing glow (sgBreathe) and 87 drifting stars (M.sky.init: 29 lanes x 3 layers,
  the kit's own builder, in place of the 29 static ones; the reference's bgdeco_star / star_o / spark art) with a hole 40 px
  inside the card and the sky-burst toy (a tapped star pops with a WebAudio pop) - over the reference's plain sunburst
  (startnew_bg_plain.webp, its painted stars removed) in place of the Figma frame's title_bg.png; the Figma card art is as it was.
  The play button is the reference's gold disc (btn-play.svg, 140x140 on the stage, centred, its bottom edge 2 px above the card's
  bottom - the card's 9 px border is inside its box, hence bottom:calc(2px / var(--fig-s) - 9px)), hidden until the welcome has
  been heard (this engine's landing-play-ready = the landing line has played and nothing speaks), then it pops in (sgBtnReveal
  .52 s) and breathes (sgBtnPulse 1.4 s / 1.04); its tap: the standard play sound at 0.8, the welcome cut, the tutorial gate - no
  music yet. The cover's bird is the reference's wave file (new_landing_swiftee_anim.webp, its version; 208 px, 24 px left of and
  12 px under the card's bottom-left corner, as there), started afresh as the loader fades so the whole wave is seen, tappable
  (the welcome again); the speaker chip sits at its feet (70 px, left 83 / bottom -12 of the card), grey until the play button is
  ready and while a line speaks. The Figma frame's own Swiftie (title_swiftie_hello + the wave-with-VO logic) is gone from the
  page; its [title-fig] script is left in app.js and returns at once (its elements are not there).
- 2 (aage): the reference's NAV-NEXT-BTN + NAV-PULSE verbatim: the button is a bare text button again (no <img>s), drawn by two
  pseudo-elements - the disabled pill + arrow (btn-next-disabled-pill / -arrow.svg) always, the enabled pill + arrow fading in over
  it in .3 s on .active and breathing (navBreathe 1.4 s / 1.04, on the art, never the box); 170x62 on the tutorial pages, 190x62
  elsewhere (the reference's boxes), in the bottoms this file already gives it (128 / 138 / 10 px: the Figma pages' places); a page
  that hides it inline (the self-advancing pages) keeps it hidden; the standard next sound at 0.9 on the tap.
- 3 (the bird): every Figma title bar's circle (.dmf-head on T2-T4, G1-G3, L2) shows the engine's LIVE head: the mascot image's
  src is mirrored into it (and on every mount), so it celebrates on a right tap, tries again on a wrong one (the pick module now
  calls setSwMood("tryagain") there) and rests on the talking head - inside the circle, as the reference's header bird (not
  popping out of it as the Ek-aur-Anek .anim rule did; the circle keeps the frame's own size and ring). G4/P1/P2's engine header:
  the reference's 118 px circle at 16.5,18 (#9DDBF5, 4 px white ring, overflow hidden) with its chip at the bird's shoulder
  (94.5,80 - already so). The cover's, the gates' and the celebration's birds are the reference's own files (1, 5, 7).
- 4 (the speaker chips): the glyph was already the reference's (the inline SVG of #audioChip and #sgVo is byte-identical); the
  cover chip as in 1; the header chip grey (opacity .5, grayscale) while a line speaks (body.vo-playing, set in setPlaying - the
  reference's flag; G4/P1/P2 had it as .vo-disabled already); the story pages' card chip was given the reference's place on
  2026-10-21; the waves blink only while a line speaks and stand solid at rest (TOTA-WAVES-IDLE). NOT ported: the reference's
  [SPK-AFTER-VO] "grey until the page's opening lines are over" - it keys on that lesson's own page scripts (autoPlayChain / its
  story intro), while this file's Figma pages own their audio flows, so the hold would never release there; the chip here is grey
  exactly while a line speaks.
- 5 (gates + confetti): the gate is the reference's GATE-REF-ANIM, verbatim but for this engine's clip path rule, GameBus for
  SwiftPAL and this lesson's own caption moments: its bird (peeking_talk_up.webp, 52.8 % of the screen, bottom-anchored, lifted in
  over .3 s already talking), the clip at once, the headline written left to right (pgWipe .9 s) at the moment the clip says its
  words - 2850 / 3540 / 210 ms into this lesson's vo_pt_tutorial / _guided / _practice (the last phrase group's onset, read off
  the clips the way the reference's 3660 / 3940 / 1120 were off its; the engine used to reveal the tutorial title at 3150 ms),
  the 4 s minimum hold (GATE_MS; the engine held 2.8 s), the first gate's bird sinking back (pgPeekDown .34 s); the scrim .35 +
  blur 10 (was .6) over a plain blue field (the sky off, the cover's sunburst dropped while gating); the cover visible unblurred
  behind the first gate. Confetti = CONFETTI-REF on this engine's own kit burst: 100 pieces (was 80), falling 1.6-2.6 s (was
  1.1-1.8), 1.5x (--fx-size, sized with --scale), the layer at z 5000 (under the gate; was 100001), the standard confetti sound at
  0.45 (was .85). afterConfetti (the wait before advancing) is this file's as before.
- 6 (the music): BGM-DUCK verbatim on this file's mp3: one <audio> made at load, started by the first page's mount (the play tap
  no longer starts it; the cover has no bed), 0.13 at rest, ducked to 0.03 under ANY sound - every Audio element's play() (voice,
  sfx, the letter page's piano loop, the stamp page's pops) and every WebAudio source node (the kit's pops, the engine's tones)
  through two prototype wrappers - 180 ms down, 600 ms up, 150 ms after the last sound; faded out (600 ms, then paused) when the
  celebration mounts, back on a page in range. This engine's own fadeBackgroundMusic / startBackgroundMusic are no-ops once the
  bed exists (window.__bgm), so the letter page's duck/restore calls do nothing (the bed ducks under its loop by itself) and
  `backgroundMusic` is the bed's element (the checks read its volume).
- 7 (the celebration): the reference's screen, verbatim: its sunburst end_screen.webp (its version) with the sky's soft radial
  hole, the CELEBRATION mount rewritten to the reference's (the standard confetti sound at 0.45, the star burst, no text, the
  signals, the arrow shown at once) with this engine's own aage-badhen tap (the standard next sound, the completion events, the
  hand-over); the screen moved to <body> (full-bleed, TOTA-END-FULLBLEED); the three-sheet Swiftie (cel_shabaash / cel_talk /
  cel_idle, 6x6 frames of 329x440; CEL-SWIFTIE: the jump 0-29 at 45 ms, the landing 30-35, THEN the line, lip-synced on the talk
  sheet from the card's end_anim.bits, then the idle loop) in the stock mascot's place (sw_lg_celebrating_anim.webp hidden); the
  gold arrow pill (END-FINISH-BTN: #FCB717, 4.54 px white ring, the 52 px arrow glyph, scaled by --scale) waiting dim and
  untappable while she speaks, then pulsing (celArrowPulse). The LINE is this lesson's own vo_celebrate, not the reference's
  vo_well_done: its beak bits (dun_assets/cel_bits.json, 187 x 25 ms) were derived by the detector that best reproduces the
  reference card's own bits on its clip (RMS per 25 ms, open above half the local max over +-12 frames and within 18 dB of the
  peak: 98.3 % agreement on vo_well_done). The card carries end_anim (the reference's frame lists, this clip's bits) and the
  celebration slide's sfx.
- Measured on the built page (chrome_shots2.py / dun_probe.py in the scratchpad, 1333x750): the play button ready 12.7 s in
  (after the 8.6 s welcome), 140x140 at 589,463, breathing; the tap: sfx_play_button at 0.8, vo_pt_tutorial at once, the story's
  line and the bed 4.7 s later; T0's aage 170x62 at 582,550, the disabled art, then the enabled art with navBreathe; the bed 0.13
  at rest / 0.03 under a line / 0.13 again a second after; a tapped star pops; the first gate over the unblurred cover on a plain
  field with the sky off; the guided gate: the bird 396 px lifted in, the headline at 3540 ms (96 px #CD0FD5 at top 271, wiped
  in), G1 at 5.2 s; G1's title-bar head: sw_head_talking -> tryagain on a wrong tap -> celebrate on the right one; 100 confetti
  pieces at z 5000; G4's bird 118 px at 17,18 with the chip at 95,80; the celebration: the shabaash sheet frames 0-35 over 2 s,
  the line at 2.47 s on the talk sheet, the arrow dim until it ends then pulsing, the bed paused; no page errors anywhere.
- The checkers: smoke.py and gate_check.py's gate helper now reads the reference beat (pg-up / pg-say, the clip at once, the
  headline at its cue, the page >= 3.9 s after the open); story_check / gate_check wait for .pg-say; title_check: see its note
  below once re-measured. `../_before_dun_chrome/` holds the dist's three files, build.py, README.md and every check script from
  before.

G4, P1 and P2 in the previous pages' typeface ([sent-font], 2026-10-27)
- Asked: "at pages 10 G4, 11 P1 and 12 P2 apply the exact same font style and the exact same font as of the previous pages; rest
  exactly the same". The three SENT_PICK pages carried the reference P4's text as ported — Baloo 2 ExtraBold (800) for the
  header's line (#promptText, 32px) and the pills' sentences (.so-pill, 28px) — while every page before them (T0-G3) sets
  'Story Noto Sans Devanagari' SemiBold (600) with the engine's --font-hi as the fallback. build.py [sent-font]: those two rules
  (style.css, scoped to .stage.sent-page so nothing else changes) now give that same face and weight; the sizes (32 / 28 px), the
  line heights (1.15 / 1.2), the pills' width, padding, colours, two-line breaking (fitLines re-runs on document.fonts.ready) and
  every timing are as they were. Probed on the built page (the scratchpad's fonts_probe.py: every visible text node's computed
  font): G1 "Story Noto Sans Devanagari" 600; G4 / P1 / P2 before: "Baloo 2" 800 on both texts; after: "Story Noto Sans
  Devanagari" 600 on both, the same px sizes and line boxes. g4_check.py: G4 all pass (22), P1 all pass (22), P2 all pass (22)
  — the pills' places, heights and two-line breaks as before; smoke 47/47. On the way, g4_check.py's P2 entry was stale: it still
  expected P2 to go straight to the end screen (true only between [rm-p3p6] and L1), so it timed out at the gate; it now
  expects the round gate, then L1. `../_before_sent_font/` holds the dist's three files, build.py and g4_check.py from before.

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
- Later 2026-10-27, the chime re-timed ([letter-idea]; asked: "after the grandfather cloud is shown, when the idea sound effect is
  played, at the ummm sound this image [the girl pensive] should be shown without any cloud, and when the aahaha sound comes the
  tappable envelope in the cloud should appear in this image [the girl bright] along with the same cloud appearing animation,
  synced smoothly with the sound effects; rest exactly the same"). The chime (sfx_letter_idea, 3.3 s) read off the clip (ffmpeg
  to PCM, RMS per 10 ms + a spectral peak): "ummm" from its first frame to 1.16 s (a hum at -28 dB, ~211 Hz rising to ~305 Hz),
  silence to 2.36 s, then "aahaha" from 2.37 s (-25 dB by 2.40 s, -17 dB at 2.46 s, the second "ha" at 2.64 s, out by 3.0 s). It
  now sounds the moment the grandfather cloud has stood its hold (7.5 s on the page's clock, where the dissolve used to begin) and
  the beats hang on its "playing" event: on the "ummm" (pace.hum_at = 0) the cloud shrinks back into the bubbles' corner (.out:
  opacity .45 s, transform .6 s) and the bubbles pop out, while the girl's pensive face fades over the room in .35 s (scene_c =
  the user's 1.png of 2026-10-27, 1672x941, stored LOSSLESS like the other two, the same room with her face closed; her bright
  face, 2.png, IS the page's scene_b byte for byte, so nothing else of the room changed); the bubbles pop again at aha_at - 3/2/1
  x rebub_gap (160 ms), and on the "aahaha" (pace.aha_at = 2370) the pensive face fades off (.35 s) and the SAME cloud grows in
  again — swapped to white while it was out (the images' 1.5 s cross-fade is gone; the swap is unseen) — with the cloud's own
  entrance (.in: opacity 1.2 s, scale .55 + the (-30,40) slide over 1.6 s from its 12% 92% corner) and the letter growing IN it:
  a wrapper (.ltr-env-grow) round the envelope's pulse layer runs that same entrance in the envelope box's px (--ltr-go /
  --ltr-gt from the module = that corner and that slide at 1/s, s = 189/1138), so the cloud and the letter in it are one growing
  thought; ready (tappable, pulsing) at aha_at + letter_in (1300) + 100 = 11.27 s on the page's clock (was 9.85 s). Gone: the
  dissolve (pace.dissolve; the grandfather fading to white inside the standing cloud) and the letter's own pop-in (ltrIn). The
  tap and everything after it are untouched; so are the frames before the chime. letter_check.py: at 7.35 s the grandfather
  still stands; the chime at 7.5 s, once; at 8.3 s no cloud (.out), no bubbles, the pensive girl, no letter (l1_hum.png); 2.25 s
  into the chime still no cloud and the bubbles re-popping; 0.45 s after the "aahaha" the bright girl, the white cloud and the
  letter both mid-growth (opacity 0.54, the grandfather off; l1_grow.png); by 4.1 s into it the cloud standing, the growth
  settled, the letter at 558:2's box, pulsing, tappable; the page's own frames from the chime to ready: no gap over 100 ms and
  the cloud's opacity never falling after the "aahaha"; the rest as before. Smoothness: on the page's own frames with nothing
  else running (the scratchpad's trace_chime.py: a rAF loop the page starts itself at 7 s, no Playwright polls, 7 s to ready) the
  first build had a 120-150 ms frame right on the "aahaha" and 50-70 ms on the "ummm" — a layer at opacity 0 is never
  rasterised, so the envelope's four lossless layers (6 MP) and the pensive picture were being decoded on the beat itself
  (img.decode() at mount did not help: the compositor had let those decodes go by then). So the growing wrapper (.ltr-env-grow,
  with its own layer from mount: will-change), the white cloud image and scene C now REST at opacity .005 (1/255: at 0 Skia
  skips the layer's contents outright) instead of 0 — painted, hence decoded, with the page's first frame / the grandfather's
  entrance, and invisible (under a level) — and the envelope's pulse layer carries no opacity of its own any more. After: max gap
  35 ms, mean 16.5 ms (60 fps) over 260 frames, on two runs. gate_check all pass, smoke 47/47, stamp_check all pass.
  `../_before_letter_idea/` holds the dist's three files, build.py and letter_check.py from before (the dissolve).

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
- Later 2026-10-26, [stamp-rounds] (asked: "after the confetti the stamps in the holder will disappear with the opposite of the
  animation in which they appeared and the complete sentence will also disappear and the new stamps will appear with the exact
  same animation as before as shown in this figma reference and the new sentence ... with the same synced animation as before and
  the blank box, stamps will again follow the exact same flow"): a SECOND ROUND from frame 579:47
  (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=579-47 — the next "G3 guided story question" under
  565:28 on the page; four more such frames follow it: 592:89, 592:110, 593:130, 593:151 — not asked for). The card's L2 data now
  holds `rounds` (both frames: sentence + clip + word times, mark, pick, the two stamps' pictures, boxes and print points, the
  sentence's box, the slot's box and dash runs); the module runs them in turn (setRound builds the round's sentence p and slot,
  swaps the stamps' pictures; `.stp[data-round]` says which). Round 2's frame: the same table, title bar, sheet, tray; the stamps
  । (the same picture) and the comma — "stamp-apostrophe 1" (72x115 at 677,541; its print point measured (36,114) like the ?'s)
  — saved lossless as stamp_assets/img_stamp_comma.webp (172x272); the sentence "माँ ने मुझे मेरे जन्मदिन पर कई सारे खिलौने [7
  spaces] पेन और किताबें दिलाई हैं ।" in a 448-wide centred box at 416,287 98 tall, Baloo Bhai 2 SemiBold 30 black = TWO rows of 49
  (the frame's "\n" is in the shown text, sfigLine's <br>): row 1 ink 293..327 x 456..824 on the render, row 2 342..373 x 436..517
  and 560..840 (the gap for the slot: 43 px of ink gap = a space + a 37 px .stp-gap span before word #9 "पेन"); the box set at y 289
  (the +2 of round 1) with line-height 49 lands row 1 at 294..327 x 456..823 and row 2 at 343..373 x 436..517 / 560..840; NO
  right padding (box-sizing is border-box here: it shrank the content and pulled the rows 6 px left) and no trailing span (the
  danda's own side bearing already centres row 2 2 px left of row 1, as the render). The slot 525,355 29x30, the same fill, radius
  and 2px dashed stroke, its runs read off the render: 4 9 3 9 4 across, 4 9 4 9 4 down. The spoken line: "माँ ने मुझे मेरे
  जन्मदिन पर कई सारे खिलौने, पेन और किताबें दिलाई हैं।" (recap_vo.py stamp sent2, the same voice; the shown text's "।" takes हैं's
  time: 15 shown words, the clip 6.66 s) — a placeholder until recorded, like the others.
  The flow between rounds (data.pace): at done_at (4.4 s after the right drop, the confetti fallen) clearRound: the stamps shrink
  away — `img.unpop` = the pop keyframes played in reverse (animation-direction reverse, the same .45 s curve), 350 ms apart, no
  sound — the words go out in reverse order 40 ms apart (words_out; their arrival's own transition backwards), the slot fades with
  its printed mark (.out, .3 s); at next_at (1.3 s) the round's sentence and slot are removed, setRound(1) builds the new ones
  and sets the pictures, and stage 3 runs again: the pops (on their sound, .48), the sentence word by word on its clip, the slot's
  3.5 s blink, .live, the drags (print point within 50/70 of the slot's centre; the । on it = wrong), the comma printed (centreInk
  on ","), the box gone on the chime, confetti; after the LAST round the end screen at done_at. The round-2 pictures and clip are
  fetched at mount. [stamp-remind] (asked right after: "the auto drag animation should not come from the second sentence, not
  even in the case of inactivity; from the second sentence the title instruction VO should repeat after 7 seconds of inactivity"):
  each round carries `guide` — round 1 true (the guidance 0.5 s after the blink and after every 7 s idle, as before), round 2 false:
  no guidance at all; the idle tick says the title's line (vo_stamp_intro, play()) again 7 s after the slot appeared without a
  touch, and again after every further 7 s (never over another clip, never with a stamp in hand; the count starts over after it).
- Checked: stamp_check.py now plays both rounds (48 steps): round 1 as before, then the clearing (unpop at 4.4 s ± .12, 350 apart,
  no pop sound; the word count only falls, 5 -> 0 within .5 s; the slot's opacity < .05; round 2 set at 1.3 s with 15 words built,
  none shown, a fresh slot at 525,355 29x30, the comma picture on s1), round 2 (the pops on their sounds, the clip .7 s after the
  second, 15 reveals within -60..+40 on the clip's clock, the slot at the clip's end with dmfBlink to .2, .live), NO guidance (no
  stamp lifts before the child's drop) and the title's line again 7.0..7.6 s after the slot, once; the । on the slot (buzz, wiggle, home), the
  comma dropped 10/8 off (snap to the press point within 4 px, thud 280, mark 400, home by 1.8 s, gone 1600 on the chime, confetti
  2100 on its sound, the comma's ink on the slot's centre within 3 px), the end screen 4.4 s after, 4 + 1 lifts; both slot moments
  against their renders (565:28: frame 4.4, sheet 6.3; 579:47: frame < 12, sheet < 20 — the two-row text's edges — each row's ink
  rows within 3 px and its runs within 4 px of the render's, the slot fill at 525..553 x 355..384); a re-run (round 0 again) and a
  mid-way exit with a stamp in hand. `python -I -X utf8 stamp_check.py ../HI02H12_L01_S01_dist/index.html out
  stamp_figma_render_1280x720.png stamp2_figma_render_1280x720.png`. smoke.py / gate_check.py drop the right stamp once per round
  (stamp_drop(ri) from data.rounds). `../_before_stamp_rounds/` holds the dist's three files, build.py, recap_vo.py and the three
  checks from before (one round).
- Later 2026-10-26, a THIRD round, frame 592:89 (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=592-89;
  asked word for word as the second). Its frame: the same table, title bar, sheet and tray; THREE stamps — । 462,541 74x116 (the
  right one: pick 0), ? 607,540 72x115, the comma 750,540 72x115 — the three pictures already in stamp_assets/; the sentence "मुझे
  उपहार बहुत पसंद हैं" in a 1075-wide centred box at 78,336 (its ink 483..747 x 342..378 on the render; set at y 338 like the others),
  the slot 751,331 36x58 = round 1's box and dash runs (the same Figma group). The spoken line "मुझे उपहार बहुत पसंद हैं।" (recap_vo.py
  stamp sent3, 2.83 s, 5 words) — a placeholder until recorded. The module takes ANY number of stamps per round now: divs for the
  most any round has (3), the extra hidden (display:none) in rounds with fewer; the round's count drives the pops (one Audio per
  div), the clearing and the sentence's start ((n - 1) x pop_gap + sent_at after the first pop). guide false (the title's line
  after 7 s idle, as round 2). The page's rounds: ? (guided) -> , -> ।; after the third confetti the end screen. Two more frames
  exist on the page (593:130 — done next, below — and 593:151).
- Checked: stamp_check.py plays all three rounds (63 steps; the later rounds through one loop: the clearing — the previous round's
  n stamps unpop 350 apart, the words out, the slot fades, the round set at 1.3 s with its n pictures shown and the rest hidden —
  the n pops on their sounds, the clip .7 s after the LAST pop, every word on the clip's clock, the slot's box and blink, .live, no
  guidance + the title's line at 7.0..7.6 s, the wrong stamp on the slot, the right one dropped off-centre, the thud/mark/home/
  chime/confetti beats, the mark's ink on the slot's centre, each stamp lifted only in hand); the hand-over to the end screen is
  judged on the page's own clock (completeSlide wrapped: 4.4 s after the last drop) — Playwright's wait lags 200-300 ms behind it;
  each round's slot moment against its render (round 3: frame 3.9, sheet 3.9, the sentence's ink rows within 3 px and its run
  within 4 px of the render's, the slot fill at 751..786 x 331..388). `python -I -X utf8 stamp_check.py ../HI02H12_L01_S01_dist/
  index.html out stamp_figma_render_1280x720.png stamp2_figma_render_1280x720.png stamp3_figma_render_1280x720.png`. smoke.py /
  gate_check.py / the live check drop the right stamp once per round (a loop over data.rounds). letter_check.py now judges L1's
  hand-over to L2 on the page's clock too (its 3 s screenshot of the dive's scaled layers can take 0.6 s+ and made the old
  Playwright-timed step read 7.5 s); its "bubbles popped at 3.65 s" step is timer-driven on L1 and has been seen to miss once
  under load — a re-run passes. The committed state before all the rounds is `_before_stamp_rounds/`.
- Later 2026-10-26 again, a FOURTH round, frame 593:130 (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=593-130;
  asked word for word as the third — "after the third sentence ... the blank boxes, stamps will again follow the exact same flow").
  Its frame: the same table, title bar, sheet and tray; round 3's three stamps (। 462,541 — ? 607,540, the right one — the comma
  750,540); TWO questions on two rows in a 402-wide centred box at 415,310: "क्या आपको भी उपहार अच्छे लगते हैं [ ]" / "दादी जी कैसी
  हैं [ ]", each row ending in its own empty slot — "Rectangle 147848" 36x58 at 822,305 and "Rectangle 147849" 36x58 at 707,354
  (round 1's box and dash runs: the same group). The render's rows' ink 316..346 (x 416..815) and 365..395 (x 531..700); the text
  is set at y 311 (lh 49, two rows): its rows then lie exactly on the render's. The spoken line "क्या आपको भी उपहार अच्छे लगते हैं?
  दादी जी कैसी हैं?" (recap_vo.py stamp sent4, 5.95 s, 11 words; the synthesiser lifts and pauses at each "?") — a placeholder
  until recorded. A round may have SEVERAL slots now (data.slots; the earlier rounds' data.slot still read): the module builds one
  .stp-slot per slot, each with its mark and the right stamp's HOVER / PRESS places over it; all of a round's slots appear and
  blink together (the demos' dmfBlink, 3.5 s); a drop is judged against the slots still empty (the nearer one within tol_x /
  tol_y); the right stamp on one prints the mark there and that box goes on the chime — and, with a slot still empty, the stamps
  are the child's again from that moment (.live back, NO confetti yet, the idle count starts over: the title's line after 7 s);
  the confetti and the hand-over come after the last slot. The wrong stamp on a slot, or any stamp off the empty slots (a solved
  slot counts as off): the buzz, the wiggle, back. guide false (the title's line after 7 s idle, as rounds 2-3). The page's rounds:
  ? (guided) -> , -> । -> ? ? (two slots); after the fourth confetti the end screen. One frame remained on the page (593:151 —
  done next, below).
- Fixed on the way: the letter page's fadeTo (its music's fade-in) clamps its progress at 0 — rAF's timestamp can precede the
  performance.now() taken when the frame was requested, and that negative progress once set a negative volume (DOMException "The
  volume provided (-0.000274917) is outside the range [0, 1]", caught by gate_check's "no page errors" on the three-round build).
- Checked: stamp_check.py plays all four rounds (86 steps, ALL PASS; a round with two slots: both slots traced — classes, opacity,
  box, mark — both appear and blink together as the clip ends (3517 ms of blink, down to .2), no guidance, the title's line at
  7.0 s idle, the comma on the first slot buzzes and wiggles (the buzz within 2 ms), the ? dropped on the first slot (+15, -10 px
  off its centre) snaps and presses (its print point within 1 px of the press point), the thud at 282 ms, its mark at 417 ms,
  home by 1534 ms, its box gone at 1600 ms on the chime (3 ms) with .live back the same frame and NO confetti; the ? on the second
  slot (-12, +12 px) the same (thud 286, mark 400, box 1616 on the chime), the confetti at 2099 ms on its sound (8 ms), the
  hand-over at 4396 ms on the page's clock; each mark's ink within .5 px of its slot's centre; the ? stamp lifted exactly twice in
  that round, the comma once, the danda never; the page's own sounds 2 + 2 + 3 + 3 pops and 5 thuds, all stopped on leaving) and
  its slot moment against the 593:130 render (frame mean 4.35, sheet 5.77, each row's ink rows exact and its runs within 1 px,
  each slot's fill exact to the pixel — the fill test now matches the slot's own #FFF1B6 within 20 px of its place, since the
  sheet's paper by the first slot passed the looser colour test). `python -I -X utf8 stamp_check.py ../HI02H12_L01_S01_dist/
  index.html out stamp_figma_render_1280x720.png stamp2_figma_render_1280x720.png stamp3_figma_render_1280x720.png
  stamp4_figma_render_1280x720.png`. smoke.py / gate_check.py / the live check drop the right stamp on each of a round's slots in
  turn (the second once the first's box has gone and .stp.live is back; a round's marks counted). The committed state before this
  round is commit 13c5c87 (three rounds).
- Later 2026-10-26 again, a FIFTH round, frame 593:151 (https://www.figma.com/design/R6YdoMpD5l2tL0rcT8pXiE/FLN-by-MJ?node-id=593-151;
  asked word for word as the fourth — "after the fourth sentences ... the blank boxes, stamps will again follow the exact same
  flow"). Its frame: the same table, title bar and tray, round 3's three stamps; the letter's closing lines on FIVE rows in a
  339-wide centred box at 468,180 — "उनके आम [ ] केले और / अमरूद के पौधे बड़े हुए या नहीं [ ] / आप मुझे पत्र लिखकर बताना [ ] / मैं आपके
  पत्र का इंतज़ार / करूँगी [ ]" — with FOUR slots wanting DIFFERENT stamps: the comma's "Rectangle 147848" 29x30 at 633,198 (between
  आम and केले), the ?'s "Rectangle 147849" 30x45 at 804,228, the dandas' "Rectangle 147850" 30x45 at 798,280 and "Rectangle
  147851" 30x45 at 679,376; under them the letter's sign-off "आपकी प्यारी" / "पिंकी 🩷" (16 px, 81-wide centred boxes at 427,449 and
  427,481). The frame draws the sheet 6 px higher than every other round (925,58): the sheet stays where the page has it. The
  render's rows' ink 186..212, 235..271, 284..318, 333..364, 382..408; the text set at y 181 (lh 49, five rows) lies on them
  exactly; the comma's room is a 30 px gap span before केले (आम ends at 629, केले starts at 665/666, as the render); the sign-off at
  y 451 / 483 (its rows' ink on the render's; "पिंकी" sits 3 px left of the render's because the system's 🩷 glyph is wider than
  Figma's). The 30x45 slots' dash runs read off the render: dash_h [4, 10, 2, 10, 4], dash_v [4, 10, 3, 11, 3, 10, 4]; the 29x30
  one's [4, 9, 3, 9, 4] / [4, 10, 2, 10, 4]. The spoken line "उनके आम, केले और अमरूद के पौधे बड़े हुए या नहीं? आप मुझे पत्र लिखकर बताना।
  मैं आपके पत्र का इंतज़ार करूँगी।" (recap_vo.py stamp sent5, 12.6 s, 22 words; the synthesiser pauses at the comma, the ? and the
  dandas) — a placeholder until recorded; the sign-off is shown, not read. The module: a slot may carry its OWN mark and pick
  (sl.mark, sl.pick; the round's are the fall-back) — its mark span and its stamp's HOVER / PRESS places are its own, a drop is
  judged against the hit slot's own stamp (the danda on the comma's slot is wrong, right on the dandas'), the press uses that
  stamp; data.sign = small text lines (p.stp-sign, Noto in the frame's 26 px line box) shown the moment the sentence's last word
  arrives, gone first in the clearing (they came last), removed with the sentence. guide false. The page's rounds: ? (guided) -> ,
  -> । -> ? ? -> , ? । । (four slots); after the fifth confetti the end screen. The page's frames are all in now.
- Checked: stamp_check.py plays all five rounds (118 steps, ALL PASS; round 5: all four slots traced and blinking together as the
  clip ends, the sign-off's two lines built with the round and arriving with the 22nd word, no guidance, the title's line at 7 s
  idle, the danda dropped on the comma's slot buzzes and wiggles, then each slot's own stamp in turn — the comma (+8, +6 px off
  the centre), the ? (-10, +10), the danda (+12, -8), the danda (-8, -12) — each snapping, pressing on the thud at 0.28 s, printing
  its own mark at 0.4 s, home by 1.6 s, its box gone at 1.6 s on the chime with .live back the same frame and NO confetti until
  the fourth, then the confetti at 2.1 s and the hand-over at 4.4 s; each mark's ink within 1 px of its slot's centre; the stamps
  lifted exactly once per slot they are right for plus the wrong drop (the danda 3x, the ? 1x, the comma 1x); the sign-off gone
  first in the clearing; the page's own sounds 2 + 2 + 3 + 3 + 3 pops and 9 thuds, all stopped on leaving) and its slot moment
  against the 593:151 render (frame mean 7.24, sheet 14.52 — the frame's sheet sits 6 px higher —, each row's ink rows exact and
  its runs within 2 px, each slot's fill where the render's is: the fill test now erodes the #FFF1B6 mask by a pixel and compares
  mine with the render's found the same way, since the fill shows through the stroke's 2 px gaps in the render and Chrome's
  LCD-antialiased text fringes 3 px from a slot passed the colour test). smoke.py / gate_check.py / the live check drag each
  slot's own stamp. The committed state before rounds 4 and 5 is commit 13c5c87 (three rounds); `_before_stamp_rounds/` still
  holds the one-round files.

Every page's text in the reference T1's face: Baloo 2 ExtraBold ([baloo-font], 2026-10-30)
- Asked: "take the reference of Page 1 T1 of https://hi-02-h04-l01-s01-dun.vercel.app/ and apply the exact same font everywhere in
  this file, the title or wherever the font is used, and adjust the sizes so the whole layout looks perfectly fine; rest exactly the
  same". The reference's T1 (its dev nav's page 1, STORY_SCENE) sets its one text, the sentence "लड़का पेड़ के नीचे बैठा है।", in
  "Baloo 2" ExtraBold (800), 32px — probed live in Chrome (scratchpad font_probe.py: computed font + CDP
  CSS.getPlatformFontsForNode, which reports the face actually drawn). The live page is byte-identical to the local copy under
  "Suresh's File/HI02H04_L01_S01-…/HI02H04_L01_S01.html"; its embedded Baloo 2 700 / 800 woff2 are byte-identical to the ones this
  engine already carries as 'Baloo 2' (--font-hi).
- Before: the engine's own chrome (the gates' pink titles, आगे, the end screen's button) was already Baloo 2 800 (the gates' "Lilita
  One" is not on the page, so every glyph is Baloo 2's — probed); the lesson's pages were not: T0-G3 and L2 in 'Story Noto Sans
  Devanagari' SemiBold (600), and G4 / P1 / P2 likewise since [sent-font]. The title page has no live text (its title is the Figma
  art, an image) and L1 / CEL show none either; the dev nav (?dev=1) keeps its own system / monospace face.
- How: build.py [baloo-font].
  1. One face for the lesson pages, 'Story Baloo 2' = the engine's Baloo 2 800 file (story_assets/story_font_baloo2_800.woff2,
     decoded from the embedded data URI, so the very font the reference draws) with Noto Sans Devanagari's line metrics
     (ascent-override 89.6 %, descent-override 40.8 %, line-gap 0 — Noto's hhea 896 / 408 per 1000; Baloo's own 1078 / 524). The
     glyphs, weight and advances are Baloo's; the line boxes and baselines are where the Figma-matched Noto layout had them, so
     nothing moves up or down (ink centres within ~2 px of before on every page, line breaks identical). Every rule that named the
     Noto face names it (font-weight 800); the two Noto subsets left the dist (their source stays in story_assets/).
  2. No word spacing: the -2 / -3 / -4 px (CSS, and data.layout.sent.ws) made Noto's 0.26 em spaces into the frames' Baloo Bhai 2
     spaces; Baloo 2's own space is that 0.2 em.
  3. G4 / P1 / P2 (the reference P4's port): back on P4's own rules — #promptText and .so-pill in the engine's 'Baloo 2' 800 with P4's
     line heights (1.15 / 1.2): [sent-font] undone. g4_check's pixel comparison with P4 passes again on all three.
  4. Sizes: Baloo 2 ExtraBold's advances at the same px are within 2 % of Noto SemiBold's, so every size stays — except G3's sentence,
     the longest (बाग में गुलाब, गेंदा और चमेली के फूल हैं ।): at 50px its bolder ink ran to 16 px from the bar's end (31 before);
     at 48px (data.layout.sent.size, and the stamped comma's mark_size) it is as wide as the Noto one was (ink 350..1106 vs
     350..1105 frame px).
  5. The slots that sit after or between words were placed against Noto's ink, and Baloo's bolder words are 2-10 % wider, so the
     last words ran 1-5 px into them. Each slot now sits the same distance from its word's ink as before (measured on the built
     pages with the scratchpad's slot_measure.py / stamp_measure.py, ink from canvas metrics of the computed font):
     T2 / T3 / G1 / G2 layout.slot 521 / 497 / 548 / 496 -> 528.3 / 502.6 / 553.6 / 498 (the sentence + slot pair still centred on
     the bar); T4: the two four-space gaps opened to their old ink widths (sentence.nudge {"3": 3.4, "4": 2.1}, the danda's -4.5
     nudge dropped — Baloo's own space before "।" already gives the old gap), the sentence box x -34 -> -31.7 (its old centre),
     the slots 286 / 417 -> 280.7 / 420.1; G3: nudge {"3": 4.1} (no danda nudge), x -28 -> -26.2, slot 278 -> 279.3; L2: the
     comma gap spans 37 -> 38.4 (round 2) and 30 -> 31.4 (round 5), the slots 751 -> 755, 525 -> 522.4, 751 -> 753.7,
     822 -> 825.9, 707 -> 711.3, 633 -> 630.8, 804 -> 805.9, 798 -> 802.9, 679 -> 679.7. Every gap reads back within 0.1 px of
     its old value.
  app.js is byte-identical (the marks' ink centring, the pills' two-line fitting and the canvas measuring all read the computed
  font); style.css changes only in those rules, index.html only in those numbers.
- Checks: smoke 47/47, title 25/25, story 61/61, gate 14/14, letter 43/43, stamp 36/36 (CORRECTION, later the same day: that run had crashed after round 1 on the
  fractional slot x's — see [word-sync]; the full run is 110/110), g4_check G4 / P1 / P2 28/28 each (incl. the pixel comparison with the reference's P4 — passing again now that
  [sent-font] is undone). The Figma pages keep their timing / flow / box checks; what fails is, by design, the comparison of the
  TEXT INK with the Figma renders, which Figma drew in its Noto fallback (the frames' "Baloo Bhai 2" has no Devanagari): demo T2
  40/43, T3 40/42, T4 41/43, pick G1 / G2 53/55, G3 52/55, recap 44/46, relisten 34/36 (relisten's two render comparisons
  failed on the build before this too) — "each text's ink sits where the render's does" (Baloo's words are 2-10 % wider, its "?"
  12 % shorter, its "," taller) and "the whole frame pixel-matches the Figma render". One more on T2: the stamped "।" while it
  is highlighted and grown (scale 1.22) reads 1.33 px left of the slot's centre (limit 1; landed 0.83) — an intensity-weighted
  centroid (scratchpad mark_centroid.py) puts it at 1.10 grown / 0.47 landed vs 0.43 / 0.14 in Noto; the module's run-time
  centring is MORE exact for Baloo's danda (canvas vs raster within 0.45 px, Noto's 0.9-1.7), the grown offset is Chrome's raster
  of the scaled glyph; T3's ? and T4's two commas sit within 0.5 px landed and grown. demo_check / pick_check's [sent-50] pair
  check now allows Baloo's glyph box (45-66 px tall, centre y 274-283: its ु reaches deeper, its ि / ी loops higher); the pairs
  sit within 1 px of the bar's centre with 3.1-4.1 px slot gaps. The checks' CONFIG slot / sentence numbers and font assertions
  follow the new values. Run the timing-sensitive checks one at a time: three lanes in parallel made relisten, T3's bar timing
  and story's music request fail on load alone (each passes run alone).
  `../_before_baloo_font/` holds the dist's three files, build.py and the check scripts from before.

Page 1 T0's text box: the reference story's shadow ([textbox-shadow], 2026-10-30)
- Asked: "take the reference of Page 1 S01 of https://hind-dear-story.vercel.app/ and apply the exact same shadow effect used at the white
  dialogue box for the hindi text on the white dialogue box of Page 1 T0; rest exactly the same". The reference's S01 (STORY_MIC_READ)
  sentence box is .mr-caption under `.stage.tut.l02-story .mr-read .mr-caption{… box-shadow:0 5px 0 rgba(11,42,90,.10),0 10px 26px
  rgba(11,42,90,.12) !important}` (its style.css, read live): a crisp 5 px navy lip plus a soft navy glow — the same computed value on
  every 300 ms sample of the page's first 18 s; its stage is 1:1 at 1333x750.
- Here: .sfig-textbox (T0's white box, Figma node 436:412) had Figma's `0 4px 19.7px rgba(177,177,177,.25)`; it now has the reference's
  two shadows, each length divided by --fig-s because the box lives in .sfig-in (transform: scale(--fig-s)): on screen 5 / 10 / 26 px,
  as the reference's. Nothing else: no border, colour, size or place changed (the reference box's 4 px white rim is not a shadow and
  this box has none). style.css only: that one rule; index.html and app.js byte-identical.
- Checked (scratchpad shadow_cmp.py: each box shot with and without its shadow, the shadow's opacity recovered per pixel toward
  rgb(11,42,90)): below the box and beside it the profile matches the reference's within one 8-bit level everywhere but the lip's
  anti-aliased bottom row (0.099 vs 0.074 — the two boxes' bottoms fall at different sub-pixel places, 506.6 vs 571.3), where the old
  Figma shadow differed by up to 0.139. story_check.py 61/61 (its picture + text box diff vs the Figma render 2.0-2.35 %, under 5 %).
  `../_before_textbox_shadow/` holds the dist's three files, build.py, story_check.py and this README from before.

Every VO-synced text: whole at once, then the reference's word light ([word-sync], 2026-10-30)
- Asked: "take the reference of page 1 T1 of https://hi-02-h04-l01-s01-dun.vercel.app/ and apply the exact same effect of the
  appearance of the whole hindi sentence at once instead of word by word animation of the sentence appearance, and when the VO of
  the sentence is played the exact same word by word orange highlight as in this reference file, at all the places of this file
  wherever the sentence is synced with the VO; rest exactly the same".
- The reference (its local byte-identical copy, Suresh's File/HI02H04_L01_S01-…/HI02H04_L01_S01.html; <script id="STORY-INTRO-JS">
  and #STORY-INTRO-CSS / #P2-BIRD-POP-CSS): T1's sentence pill rises in whole — siSentIn, 0.45 s, cubic-bezier(.2,.8,.3,1), from
  opacity 0, 14 px lower, scale .96 — and SENT_IN_MS (450 ms) later the sentence's clip plays; its wordSync puts .p2-word.on
  (color #E86A00, p2WordPop .28 s: 1 -> 1.10 -> 1, origin 50% 60%) on word k while start[k] <= currentTime < start[k+1], the last
  word until the end of the last word in the recording, one word at a time, and clears it at that end or as soon as the line is
  cut. Traced live (scratchpad ref_t1_trace.py): rise 27 frames, opacity 0 / .672 / .903 / .977 / .998 and lift 14 / 4.59 /
  1.35 / .33 / .03 px at +0 / 100 / 200 / 300 / 400 ms; the clip 500 ms after the rise; one word lit at a time, none after 2.292 s.
- Before: every narrated text here ARRIVED word by word (.sfig-w fading up as the clip reached it): T0's four beats, T0B's two
  sentences, T1's nine texts (names, uses, examples), the first reading of the sentence on T2-T4 and G1-G3, L2's five round
  sentences; the demos' second reading and the picks' idle re-read already lit words orange ([word-hot]); G4 / P1 / P2 are the
  reference P4's own pills (shown whole, words lit as read) and stay as they were.
- How (build.py [word-sync]): story_js gets SENT_IN_MS = 450, sfigRise(L, extra) — every word of the line on at once (their own
  arrival transition off meanwhile, .sfig-whole) and the line's element rising in with siSentIn (keyed on the individual
  translate / scale properties so a text box's own centring transform is kept; T1's example text box lost its translateX(-50%)
  for the same left in calc() so the rise scales about it) — and sfigSync(L) — the reference's wordSync on the clip that has just
  started: words sharing a start ("है ।") light together, nothing after the line's last word's end, cut lines clear at once.
  sfigNarrate (T0 / T0B / T1) is now: a line not yet shown rises in and is read SENT_IN_MS later; a line already shown (a 🔊 replay)
  is read at once — replays keep every text on screen (T0B / T1 no longer hide them first). T2-T4 / G1-G3: the sentence rises in
  once the bar has landed (the old 650 ms), its clip 450 ms later with the light; the picks' idle re-read uses sfigSync. L2: each
  round's sentence rises in at the old moment (0.7 s after the last pop) with its sign-off (593:151), its clip 450 ms later with the
  light. Every line's card data carries word_end (the last word's end from its *.words.json). Unchanged: the demos' second reading
  (words + slots lit on the full clip, held through the slots' 1.5 s), T0B's sentence / comma lights, every box, picture, sound.
- Timing: each FIRST reading starts 0.45 s later than before (the reference's order: the sentence is seen, then heard); the
  pages' other beats follow from there.
- Checks: scratchpad sync_trace.py + sync_check.py traced all 22 synced texts (T0 4, T0B 2, T1 9, T2-T4, G1-G3, L2 rounds 1-5)
  frame by frame: every one appears whole in a single frame with the rise, its clip ~0.45 s (466-515 ms) after, the lit word the
  recording's on every frame (single-frame lags only), nothing lit after the last word's end, look #E86A00 + p2WordPop .28 s.
  The project checks' word-by-word assertions were rewritten to the new behaviour (story / relisten / recap / demo / pick / stamp:
  "the whole text appears at once", "it rises in and its clip starts ~0.45 s later", "each word lit as the clip reaches it, none
  after the last word's end", the beat / box / round timings + 0.45 s, replays keep the text): run one at a time — smoke 47/47, story 54/54, relisten 34/36,
  recap 44/46, demo T2 40/43, T3 40/42, T4 41/43, pick G1 / G2 54/56, G3 53/55, stamp 110/110 ("ALL PASS"), gate, letter, title,
  g4 G4 / P1 / P2 all pass; every remaining failure is one that failed before this change too (the text-ink and whole-frame
  comparisons with the Figma renders, drawn in Noto, since [baloo-font]; relisten's two render comparisons, older still; T2's
  grown danda at 1.33 px). New: word_sync_check.py (the trace + judge above as a project check; all 26 lines OK, exit 0; it
  allows the light to lag the clip's clock by up to two frames). stamp_check.py's pixel helpers now round their windows to whole
  pixels: since [baloo-font] the stamp slots sit at fractional x (753.7, 522.4, ...) and the script had crashed (exit 1) after round
  1 — so the "stamp 36/36" under [baloo-font] below covered round 1 only; the full run is the 110/110 here.
  `../_before_word_sync/` holds the dist's three files, build.py, the README and the check scripts from before.

Page 1 T0's four pictures: the user's redrawn art ([story-pics], 2026-10-31)
- Asked: "At Page 1 T0 replace the images with these images at their respective places but rest keep everything exactly the
  same" — four attached pictures, the same scenes redrawn (Pinki now in braids, a grey cat): 1 pointing at the cat, 2 hand to
  her ear, 3 the "?", 4 with her mother — beats 1-4 in that order.
- Here: the same four files, story_assets/img_story_pinki_{cat,listen,ask,maa}.webp, now hold the user's pictures at their
  native size (1672x941, 1738x905, 1738x905, 1672x940; WebP q90 method 6 as g4_picture.py, 134-159 KB like the old ones);
  build step 7b copies them as before.
- One CSS change per picture shape (build.py, the .sfig-img rules): the old bitmaps were 2:1 and the frames' image nodes
  overhung the 430x224 box (b1 -14,-3 458x229; b2 -16,-4 462x231; b3 -14,-2 458x229) — kept for the new pictures they zoomed
  beat 1 by 6 % and cut the cat off at the right edge on beats 1-3 (previewed). The new ones fill the box full width, centred:
  b1 0,-9 430x242 (16:9, as b4 already was), b2 / b3 0,0 430x224 (1738x905 is the box's own 1.92); b4 unchanged (its new
  picture has the old one's shape). Frame, border, text, VO, beat timing, the cat sound and beat 1's pop are untouched.
- Checks: story_check.py's beat boxes follow the new rules, and its four Figma renders got the new pictures pasted into the
  picture box (scratchpad patch_story_renders.py; the old renders kept as story_b*_figma_render_1280x720_v1_2026-10-28.png):
  story 54/54 (ALL PASS, exit 0; picture + text box diffs 2.3-2.5 %, the picture's only resampling edges), smoke 47/47.
  An unchanged rebuild first reproduced the dist byte for byte; after the change git shows only the four pictures (dist +
  story_assets), style.css's .sfig-img lines and build.py. `../_before_story_pics/` holds the dist's three files, the old
  pictures, build.py, the README, story_check.py and the old renders.

Page 1 T0's white box and type: the reference poem game's caption ([poem-box], 2026-10-31)
- Asked: "Take the reference of https://hi02h11l03s01poem-8cpz.vercel.app/ and apply the exact same white box for the text at page 1
  T0 and the exact same font style and font size, but don't keep any word highlighted in orange even after the VO sync is over."
- The reference: its Page 1 = T1 (STORY_SCENE, Meera's balloons), the poem in `.story-caption`. That deployment is NOT the GitHub
  Ek-aur-Anek repo's file (a different build); read live in Chrome at 1333x750 (scratchpad poem_probe.py), computed: white, 3 px white
  rim, 26 px corners, padding 8 px / 22 px (a later rule overrides the 10 / 30 written first), shadow 0 5px 0 rgba(11,42,90,.10) +
  0 10px 26px rgba(11,42,90,.12) (already T0's, [textbox-shadow]), hugging its lines (max 1000 px); type Baloo 2 declared 600 —
  only the 700 and 800 faces are embedded, so it renders in the 700 face (byte-identical to this engine's own 'Baloo 2' 700) —
  29 px on 37.12 px (1.28), word spacing 5.6 px (0.2em of the box's 28 px), navy #0B3D8C. Its starred pair words (गुब्बारा /
  गुब्बारे) turn orange when spoken and STAY orange — the part the user does not want; T0 has no such words, and its own word light
  ([word-sync]) is off as soon as a line ends (unchanged).
- Here (build.py [poem-box]; T0 only — .sfig-textbox / .sfig-text are T0's alone): the box is one line high (37.12 + 2 x (8 + 3) =
  59.12 px) and the sentence + 2 x (22 + 3) px wide, 26 px corners, centred on the old box's centre (532, 309.5 frame px) — the
  rim is white on white, so it is in the size; all stage px divided by --fig-s (.sfig-in is scaled). The sentences: Baloo 2 600,
  29 px / 37.12 px, 5.6 px word spacing, one line, all four centred on that same point (the frames' per-beat centres were within
  half a pixel of it; beat 1's y 310 put its glyphs on a half pixel and softer than the reference's). STORY_LISTEN sets the box's
  --sfig-tw from the beat's computed text width at mount, again on document.fonts.ready, and at each turn — there with a .3 s
  width transition delayed .3 s, so the box narrows / widens once the finished sentence has faded and before the next one rises.
  Kept: this page's text colour #002F76 (the reference's is #0B3D8C — not named in the ask; one value to switch), the rise, the
  word light, timings, picture, Swiftie, chip, आगे. Was: Figma node 436:412 (436x119 at 314,250, 20 px corners), 'Story Baloo 2'
  800 at 26 px (beat 1) / 28 px, line-height normal, in the frames' text boxes.
- Checked: scratchpad poem_box_verify.py (34 PASS: per beat box = text + 50 px, 59.12 tall, centred within 0.5 px, 26 px corners,
  the type at 29.00 / 37.12 / 5.60 on screen, no word lit or orange after each line, after the last, after a 🔊 replay; the box
  starts resizing only once the old sentence has faded and has its new width when the next one shows); the reference caption
  given the same sentences in this page's colour comes out within 0.15 px of T0's box, and moved onto T0's box to the sub-pixel
  (poem_box_phase.py) the interiors match: 0.40-1.12 % of pixels differ by > 32 levels (glyph anti-aliasing). story_check.py now
  asserts the caption box / type / no-orange per beat and pixel-diffs only the picture against the Figma renders (the text box is
  no longer the frames'): 70/70 ALL PASS; smoke 47/47; word_sync_check T0 all lines OK. `../_before_poem_box/` holds the dist's
  three files, build.py, the README and story_check.py from before.

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
