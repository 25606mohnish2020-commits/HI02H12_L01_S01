const CARD = JSON.parse(document.getElementById('cardData').textContent);
  const AUDIO_EXT = (CARD.assets && CARD.assets.audio_ext) || "mp3";  // .mp3 (maths) / .ogg (Hindi FLN)
  const IMG_EXT   = (CARD.assets && CARD.assets.img_ext)   || "png";  // .png (working) / .webp (delivered/FLN) — twin of AUDIO_EXT (fixes A3)
  const ENGINE_VERSION = "2026.07.28t-r4-unified";  // 28t: A TAP DURING FEEDBACK AUDIO COUNTS INSTEAD OF VANISHING. The tap gate ignored a tap while ANY VO sounded — correct for the PROMPT (24a added it to stop spam-tapping), wrong for the hint clip that plays right after a wrong answer: a child who tapped again while hint1 was still speaking had that attempt SILENTLY DISCARDED. They tapped twice, the engine counted once, terminal help never came — the 2-attempt ladder defeated through a side door, on every tap mechanic in the fleet. `_fb` now marks feedback audio specifically: during it a tap is accepted and interrupts the clip (stopAudio first, so never two voices); during the prompt, taps are still ignored. Cleared on every ladder exit so it cannot leak into later prompt audio. Verified: attempts go 1 -> 2 on the second tap and terminal help fires. I could NOT reproduce the exact audio-mid-flight instant headless (clips end in <60ms there), so that specific moment rests on the 3-line gate being reviewable rather than on a measurement — stated plainly rather than claimed. PROCESS NOTE, because Yasir called out the churn and he was right: 28p-28s were four bumps in an hour and TWO of them existed only to fix regressions from the previous one (SORT_SHAPE misplacement, the stranded red state). The cost was never batching, it was shipping before verifying. This bump was made with the engine edited, the monolith regenerated and the game rebuilt at the OLD stamp, behaviour checked, and the version moved only once at the end — which is how the next ones should go.  28s: THE RED NEVER SETTLED TO GREY — my own 28r bug, caught by behavioural verification 20 minutes after writing it. The 700ms flash->lock timer opened with `if(state.helpShown) return;`, inherited from the code it replaced. But at the 2nd wrong, terminal help fires in the SAME beat, so helpShown was already true and the swap was skipped: measured on HI01H01_L02_S05 G1, the card sat RED and untappable at +1.7s and would have stayed that way. That is precisely the stuck-red-ring bug I fixed in 28d and have now reintroduced in a new form. The guard was correct for the OLD behaviour (do not UNBLOCK a card once terminal help owns the board) and wrong for the new one (swap the flash for the lock), and I copied it without re-deriving whether it still applied. Removed from all three paths; only the 'this cell turned out to be the answer' check remains. THE LESSON, written down for the third time: a guard inherited from replaced code must be re-justified against the new behaviour, not carried over.  28r: BOTH WRONG ATTEMPTS FLASH RED FIRST; ONLY THE SECOND ALSO DISABLES. Yasir 2026-07-28: "on second wrong attempt as well we are supposed to give the red glow first and then disable." He is right and 28p was half a fix: it restored red on the 1st wrong but sent the 2nd straight to the grey lock, so the child lost the 'that is not it' signal at the exact moment they most needed it. The red IS the feedback; the grey lock is an EXTRA consequence the 2nd attempt earns. Sequence now, every wrong tap: red buzz for 700ms -> then (2nd only) settle to grey and untappable. SAME FIX IN TWO MORE MECHANICS, where it turned out to be worse: SENTENCE_FIND and TAP_ALL_WITH_SOUND locked their chip PERMANENTLY ON THE FIRST WRONG TAP (.crossed / .nope, both pointer-events:none), so 27a's ruling 'a wrong card must NOT lock on the first miss' had never reached them at all — a child lost a chip for one miss on those slides while every other mechanic gave them a retry. All three paths now share the same flash-then-lock shape. Checked the whole class rather than only the site Yasir named: those were the only three places a wrong tap adds a lock class.  28q: FIXES MY OWN 28p BUG BEFORE IT SHIPPED. The SORT_GENDER terminal rung landed in SORT_SHAPE — I applied it with a first-occurrence string replace, and the `dragWrong(slide); // buzz + Swiftie...` + answer_wrong pair it keyed on is IDENTICAL in both modules, so it went to the wrong one. SORT_SHAPE then referenced `_sgWrong`, which does not exist in its scope: a ReferenceError on any wrong drop, on MTKGA03_L01_S01 P1/P2. Caught by BEHAVIOURAL verification (three real wrong drops on a SORT_GENDER slide showed attempts climbing 1-2-3 with no glow, no dim, no hand) — a syntax check and a rebuild both passed it, and static checks always would have. Nothing shipped: the dists and zips were still on 28o. Moved to SORT_GENDER and addressed via the module BLOCK rather than a global first-match, so the same class of mistake cannot repeat. LESSON, again: when two modules share boilerplate, never target it with an unanchored replace — extract the module's own text first, as the MEET_LETTER edit in 28p did.  28p (batch, 8 items, closes 8 requests): (1) THE HINT BULB IS REMOVED ENTIRELY — Yasir 2026-07-28 "we do not need that idea glow button at all". It appeared WITH A GLOW on the FIRST wrong (the add was above the ladder branch, not inside it) and was never phase-gated — 10 of 10 show-sites ungated — so it also offered help in round 3; on several mechanics TAPPING it flashed the answer ghost, i.e. reveal-on-demand with zero attempts. Hidden via CSS rather than deleting the node, because $("hintBtn") is dereferenced unguarded at all 10 sites and removing it would throw on the first wrong answer in every mechanic. (2) 1st WRONG IS RED AGAIN, ON A LIVE CARD — his ruling, and my own 28e over-correction: 28e said a DISABLED option is never red but implemented it on `.crossed`, the class used for BOTH the momentary buzz and the permanent lock, so it bleached the first-wrong flash too and left a grey disable with no red anywhere. Split into `.wrong-flash` (red, glowing, STILL TAPPABLE, removed after 700ms) and `.crossed` (28e's grey lock, from attempt 2). (3) LANDING HERO CAN GROW — raised THREE times (Yasir + the SME on both games) and also mine: 28i's max-height:180px cap was measured to be exactly the overflow boundary, because .sg-content.has-hero's 206px bottom margin shifted the block up so growth ate the title's headroom instead of the dead space below. Margin 206->120 and cap 180->250. MEASURED at Yasir's own 1919x977: title 7.7px -> 18px below the card edge, hero 166 -> 230px tall, dead space hero->button 92 -> 16px. (4) SORT_GENDER FINALLY HAS A TERMINAL RUNG — it was the sixth terminal-help path with NONE: buzz + try_again forever, no ceiling, no glow, no dim, no hand, so a child could be wrong indefinitely and a guided sort could never earn the hand. Counted PER TILE (a slide-wide streak resets on any correct drop) and routed through the shared terminalHold/travelNudge contract. (5) STORY_SCENE fits OUTSIDE the tutorial too — 27h was scoped to .stage.tut, so on test phases the caption sat behind the आगे pill (measured: 19px under a 136px-wide button on 5 slides of HIKGH07_L01_S02). (6) the tut teach picture may use the room it has (261px of art in a 581px card with 607px of width unused) without reintroducing 27h's overflow. (7) MEET_LETTER: the hardcoded '→' is gone (markup, so no card could remove it) and the auto demo no longer plants a hand on a single-letter slide — "points at the obvious and adds nothing". MEET_SHAPE/NUMBER/GENDER keep their arrows; he named MEET_LETTER. (8) bare .intro-letter glyph tiles are box-free like the pictures beside them.  STILL OPEN, deliberately not rushed into this bump: the other TWO MEET_LETTER asks — a word taught for both sounds (जल = ज + ल) must DISPLAY both letters, and the hand must sync to the glyph being spoken. The existing data.pair mode is not a substitute (it renders 1536px inside 1329px), so it needs real layout work and measurement; item (7) deliberately left no guessed 'is this two-letter' condition behind. Also still open: DEMO_COUNT before->after (a new capability), HIKGH07's baked-in scene backgrounds (art regen), Pehli's 11 dead .webp paths (card fix).  28o: TWO DRAG RULINGS FROM YASIR (2026-07-28). (1) THE HAND SHOWS THE MOVE. "on drag, the hand nudge guides the student precisely... move the hand nudge from the question card to the answer card." A static hand on the tile says 'this one' but never says WHERE it goes — which on a matching slide is the actual thing the child must work out. travelNudge() now slides the hand from the tile to its correct zone on a loop; terminalHold() takes an optional destination, so all three drag modules (MATCH_DRAG_N, MATCH_GENDER_PAIRS, SEQUENCE_DRAG) demonstrate the gesture while every TAP mechanic passes no destination and keeps the static point. Same phase rule as handOnAnswer (tutorial/guided only, never round 3), and the animation is stored on state so stopNudge cancels it — an infinite animation left running would follow the child into the next slide. Falls back to a static point without .animate(). (2) EVERY CARD THE SAME SIZE. "all the cards, both question and answer cards are to be of the same size in matching/dragging." They were three sizes: .dd-zone 150, .dd-tile 104, .dd-tile.pic-tile 134 — the thing you drag was smaller than the thing you drop onto. Unified on 150 (the largest, so nothing shrinks and the drag target gets easier). Deliberately excluded: .dd-tile.snapped (the 62px badge parked inside a filled zone — not a card) and .dd-stage.seq-words (word tiles size to their text; equal squares would clip long words, and sentence-building is not the matching mechanic).  28n: A NO-STIMULUS QUESTION RECLAIMS THE EMPTY SPACE (CSS only). After 28m stripped the 🔊 chip from the four audio-only stimuli, those slides looked half-empty and I flagged it to Yasir as a centring problem; he asked for a centring pass. I MEASURED FIRST and my flag was WRONG — the cells were already centred exactly (142px above, 142px below a 210px row in a 494px grid; .opt-grid already carries align-items:center + align-content:center), so a centring change would have done nothing. The real problem was that the tiles kept their with-a-stimulus size while the stimulus slot stood empty, so the space read as a void. The tiles now grow into it (min-height 210->300, glyph 96->112, pic 134->158), which also gives a KG thumb a bigger target. Scoped with :has() to rows WITHOUT a .stimulus-pic and excluding .stage.tut, so every slide that has a stimulus — and all the 27h tutorial-fit work — is untouched. Also RULED this round: the Swiftie header volume chip is template furniture and STAYS (Yasir 2026-07-28), which closes the flag 28m left open; 'no vol button' means the stimulus chips, not the shell's replay control.  28m: NO VOLUME BUTTON ANYWHERE. Yasir 2026-07-28: "we use vol button nowhere. if nothing then we keep question only." This closes the flag 28c deliberately left open: four stimuli have NO image (TAP_SHAPE_BY_NAME, TAP_LETTER_BY_SOUND, MASTERY_SILENT_PICK sound_to_letter + name_to_shape), so stripping their 🔊 + 'नाम सुनो'/'ध्वनि सुनो' chip looked like it would leave a blank card and I asked rather than guessed. The ruling is that a slide with nothing to show shows the QUESTION only — stimulus is now null on all four. The chip was ALSO the only way to re-hear the sound, so the FUNCTION moved to the header replay (state.replayAudio, set AFTER mount so mountTapOptions cannot overwrite it) rather than being deleted along with the affordance — a KG child must be able to hear the sound again. The 🔊 glyph also came off the three read-aloud BUTTONS (SENTENCE_READ 'पूरा पढ़ो', SENTENCE_SOUND and SENTENCE_PICK_PIC 'फिर सुनो'); those keep the button and their Hindi text, so nothing loses function there either. Touches 4 games: HI01H04_L02_S02 (8 slides), HI01H06_L01_S01 (7), HIKGH02_L01_S03_P2 (8), MTKGA03_L01_S01 (2). NOT TOUCHED, flagged for a ruling: the HEADER replay chip and the LANDING .sg-vo chip are still speaker icons. I left them because they are the only remaining way to re-hear a prompt, and because Yasir and the SME both reviewed screenshots showing the header chip today without flagging it — but if "nowhere" includes those, they need a text affordance first, not deletion.  28l: HARD RULE — NO QUESTION IS EVER SOLVED AUTOMATICALLY IN A TEST PHASE. Yasir 2026-07-28: "regardless of what interaction, as long as we in guided or practice, no question will be solved automatically." Only a tutorial slide may finish a question itself (there it is a demonstration). Two mechanics were still answering FOR the child on the last wrong attempt: PATTERN_BUILD and SEQUENCE_COMPLETE both ran `setTimeout(placeCorrect, 1000)`, so the engine filled the blank in and moved on — the child never answered. Yasir caught SEQUENCE_COMPLETE live on HIKGH04_L02_S02's build slides. Both now glow the correct tray tile, disable the rest, show the hand (phase-gated, so round 3 still gets none) and WAIT. MATCH_GENDER_PAIRS and SEQUENCE_DRAG already held the glow (25d) but never dimmed the distractors or pointed, so they route through the same helper now. The point of this bump is that the rule lives in ONE place — maySolveFor()/terminalHold()/clearHold() — because it has now drifted three times: 25d fixed two mechanics and left two auto-solving and two half-done, and each was re-reported separately (SORT_GENDER 06:32, SEQUENCE_COMPLETE 13:32) after I had already called the class closed. A new mechanic inherits the contract instead of re-deciding it. clearHold() releases the tray when the child does place it, or the disabled tiles would stay dead for the remaining blanks. STILL OPEN and deliberately not in this bump: SORT_GENDER has no terminal rung at all (a 6th path, different structure — bins not tiles); it does not auto-solve, it just gives audio only, so it is queued rather than rushed into this one.  28k: OPTIONAL MIDDLE HINT RUNG (`hint2`). The SME on Pehli Dhwani specified a THREE-rung ladder — rung 1 'फिर से कोशिश कीजिए।', rung 2 'शब्द को बोलकर देखिए, और पहली ध्वनि चुनिए।' (a strategy, NOT the answer), rung 3 the answer. Our ladder had two rungs, so rung 2 spoke `hint`, the level that names the answer; there was nowhere to put a strategy line. Six rung-2 sites (mountTapOptions, dragWrong, wrongClip, SORT, SENTENCE_FIND, TAP_ALL_WITH_SOUND) now call midHint(), which prefers `hint2` and falls back to `hint` — so a card that authors no hint2 behaves EXACTLY as before and the rest of the fleet keeps two rungs. CONFLICT, RAISED AND RULED: a third rung means the answer arrives on the 3rd wrong, so that deck's max_attempts goes to 3 and the card blocks after the 3rd attempt — which contradicts Yasir's standing 'blocks only after the 2nd wrong attempt'. I flagged it; he ruled 2026-07-28 'implement as per written by the SME'. It is therefore DECK-SCOPED to HIKGH02_L02_S01 only. Do not raise max_attempts or author hint2 on another game without the same explicit ask on that game's deck.  28j: THE GUIDING HAND, FIXED AT THE CHOKE POINT INSTEAD OF PER MECHANIC. Yasir found a hand in round 3 again (MTKGA01_L04_S01 P5, a COUNT_TAP practice slide) after I had gated handOnAnswer in 28f and startNudge in 28i. Cause: ~25 sites call pointNudgeAt DIRECTLY and bypassed both gates. Gating call sites one at a time is what produced three rounds of 'fixed'; the rule now lives in pointNudgeAt itself, default TUTORIAL ONLY, so every existing raw site becomes correct by construction and any future mechanic inherits it. handOnAnswer passes earned=true for terminal help, the one case Yasir allows in guided because two failed attempts paid for it. Round 3 gets no hand by ANY route. ALSO FIXED, both regressions from my own 28h placement change: (a) EMPTY SKY — the 'flip above if it would run off the stage' clamp put the hand 100-395px above a tall TAP_IN_SCENE hotspot, pointing at open air on 4 of 6 guided slides of HI01H07_L01_S02. Flipping is simply wrong for a hand that points UP; it now clamps INSIDE the stage instead, worst case overlapping the target's lower edge as it always used to. (b) A LABEL BELOW THE ANCHOR — anchoring to the passed element's bottom only helps if that element contains the text, and GENDER_INTRO passes the cat IMAGE while .cat-word sits below it, so 'below the image' landed on the word (56% covered on T3; 100% before 28h). Rather than teach each mechanic a smarter anchor, placement now MEASURES real text rects in the tile and drops below the lowest one that shares the column. Also: check_system's 'hand on answer, all phases' marker was a FALSE GREEN asserting the opposite of the live rule — renamed and re-keyed to the 28j choke point.  28i: WHY THE ROUND-3 HAND KEPT COMING BACK, plus four fleet-wide gaps. (1) THE ROUND-3 HAND BAN IS NOW ENGINE-ENFORCED. I reported this fixed three times and Yasir kept seeing it, because 28f only closed the answer/tap paths (handOnAnswer + HAND_PHASES) while the drag/count PROGRESS cue reaches the hand through startNudge, whose only round-3 guard was the CARD's scaffold_rules.nudge_timeout_ms — and 22 of 27 cards set `independent: 8000` (two also set practice). So on any drag or count slide in round 3, eight seconds of hesitation still produced a hand, in nearly every game in the fleet. Card data cannot be the guard for a hard rule: startNudge now refuses outside TUTORIAL and ignores a card that arms round 3. Tutorial-only, not {tutorial,guided}: the idle hand is UN-EARNED (a mount timer), and Yasir's rule is that any visual hint waits for 2 failed attempts — guided still gets its hand, but only through handOnAnswer at terminal help, which is where it is earned. Verified with a real 10.6s untouched wait on round-3 drag slides (P1/P3 SORT_GENDER, card arming practice+independent at 8000): no hand. (2) THE SAME FIX, ONE COPY OF IT — startNudge carried its own duplicate of the old positioning formula, so 28h's 'hand sits below the tile, never on its word' never reached a single progress cue; it delegates to pointNudgeAt now, so placement cannot drift between the two paths again. (3) SENTENCE_FIND SPEAKS THE TARGET WORD, NOT ALL FOUR (Yasir): the slide says 'जो शब्द सुनो, उस पर टैप करो।' and the engine read every option aloud, so nothing identified the word to tap — the task was unanswerable by design. Target-only is the default; the word-by-word read is opt-in via data.read_along:true. This REVERSES an SME ask from that same deck (21c flag #5) — flagged for Yasir, not silently dropped. Its trailing startNudge(slide,_tgt) — a pre-attempt hand on the answer, the third form 28f missed — is gone. (4) THE TWO-HINT LADDER REACHES THE PRODUCE MECHANICS. Yasir's 2026-07-25 'two hints everywhere, every game, every interaction type' landed for taps (24a) and drags (25a), but MAKE_SET / MAKE_EQUAL / BUILD_TO_NUMBER / TAP_ALL_WITH_SOUND grade their own wrong answers and inherited neither — and BUILD_TO_NUMBER passed `null`, i.e. its wrong-answer feedback was SILENT, text-only, to a child who cannot read. All four now call wrongClip(), one grader in one place; with no hint1/hint authored it returns the same try_again as before, so no card regresses. MAKE_NUMBER and COMBINE_COUNT reach completeSlide(true) only — no wrong path exists, so demanding a ladder was a checker false positive and they are excluded by name. (5) LANDING IMAGE HERO IS SIZED AT ALL — `.sg-hero img{height:118px}` has never matched anything (the element is .sg-art), so an image hero rendered at natural size: 1244x695 in a 1069x438 card, shoving the landing title to top:-106px, off screen. Same selector mismatch 16e fixed for count hands and left for images. (6) WIDTH-FIT MEASURES INK, NOT ADVANCE — the SME's original 'make the words fit inside the box', still unfixed. Devanagari paints wider than it advances, and the real bug was the BRANCH: a word whose advance fit never entered the shrink path, so its ink overflow was never considered (यह 66 ink vs 59 box, बकरी 138/132, एक 91/85, कहाँ 184/180 — all four had fitting advances). Fits whichever actually paints wider, so Latin/numerals are untouched. Also: engine_guard now WARNS (never blocks) when another session holds the engine lock — the stale-local-copy trap that produced a request against already-fixed 28g code.  28h: TWO FIXES Yasir named directly. (1) THE HAND NO LONGER COVERS THE WORD — pointNudgeAt planted the fingertip 56 design-px INSIDE the tile's bottom edge, which is fine on a bare picture tile (its only caller for years) and fatal the moment 28f started pointing it at an .opt-cell, whose bottom strip IS the label: measured 92x27px of the answer's word hidden under the hand, i.e. we glowed the answer and then covered it. The hand now starts just past the tile's bottom edge, clamped to flip ABOVE the tile if that would run off the stage foot rather than being silently clipped. Verified by measurement AND by looking: G1 hand t646 vs tile b641, label b627, vertical overlap 0, still centred, still tappable. (2) ONE GATE PER ROUND, NOT PER PHASE NAME — 28a made `independent` an alias of practice to fix a MISSING round-3 gate, and thereby created a DUPLICATE one: a card using both names crossed two 'different phases' and showed the identical 'अब आपकी बारी!' gate twice, back to back. 7 of 27 cards use both. Gates now dedupe on a ROUND id (PHASE_ROUND), so that pair collapses to one and any unmapped phase (mastery, or a future name) fails safe to NO gate — which is the ruling: three rounds, no round 4. Also closed as NOT-A-DEFECT: a report that the round-3 hand ban was still broken. Measured on P1 at 28h — terminal help fires, answer glows, stays tappable, handShown FALSE. 28f had already fixed it; the report read a stale source. The raw pointNudgeAt calls left in MEET_ORDER/COMPARE_TWO/the demo step chain are auto-DEMO teaching animations, not hints, and stay.  28g: 'going back from last screen gets swiftie stuck' — clearHost() dropped body.is-end but never removed .show from #endScreen, so the celebration layer (cheering Swiftie + 'बहुत बढ़िया!') stayed overlaid on the slide you navigated back to, covering the middle option. I had hit this myself and mis-triaged it as low severity ('a child cannot go back from celebration') — but REVIEW uses the dev nav, so it hit every review pass, and it also caused 60 phantom overlap findings in my audit sweep. Deliberately scoped to the end screen only: also clearing stage.blurred/gating here would un-blur the gray phase gate mid-flight, since mountSlide runs inside the gate's callback.  28f: ONE RULE FOR THE GUIDING HAND, in one place (handOnAnswer()) — Yasir 2026-07-28, two rulings merged: tutorial may show the hand (teaching); guided ONLY after 2 failed attempts; round 3 (practice / independent / mastery) NEVER, 'regardless of whatever name we save it by'. Also DELETED the idle/mount hand on answerable slides: startNudge fired at nudge_timeout_ms (guided 5000ms) — right after the prompt VO — pointing at the stimulus before the child had tried anything. A visual hint is now earned only by 2 failed attempts. All 5 terminal-help paths route through handOnAnswer, so the phase rule cannot drift per-mechanic again (27d put the hand in 1 of 5 and I reported it as 'every phase'). Demo/progress nudges inside the count and drag mechanics are untouched — teaching animations, not hints.  28e: (1) A DISABLED OPTION IS NEVER RED — .crossed / .sentence-word.crossed / .tap-all-item.nope now match the plain grey .faded lock. Two looks for one meaning was the complaint; this supersedes the red ring 27a introduced. 1st-wrong buzz/shake unaffected (28d unblocks that card after 700ms so it never rests as disabled). (2) TAP_IN_SCENE no longer PULSES the correct hotspot 6s after mount — that handed the answer over before the child tried (measured: identical at t=1s, only .correct-hot pulsing at t=7s). The glow now comes only from terminal help, where distractors also fade. (3) FIXED MY OWN 28a REGRESSION: the new SEQUENCE_COMPLETE picture stimulus pushed .seq-tray under the आगे pill (bottom ~30% of two tiles a dead zone on all 4 build slides). .seq-stage now top-anchors, tightens its gap and reserves the pill's lane.  NOT DONE, needs care: the fleet-default 'remove handnudge on idle' ruling — startNudge is also used by drag/count mechanics for PROGRESS cues, so disarming it globally would remove useful guidance, not just idle hints. Filed.  28d (three REGRESSIONS of my own, re-reported by Yasir): (1) the stuck RED RING — the 700ms unblock was guarded by `if(!state.locked)`, but state.locked is also set TRANSIENTLY while reveal_seq narrates, so a 700ms landing in that window skipped the removal and .crossed stayed FOREVER (permanent red ring, permanently dead card). Now keyed off this cell only (.correct / state.helpShown). I had found that same state.locked trap while fixing the idle-VO ticker, documented it there, and failed to propagate it back. (2) HAND NUDGE only existed on ONE of FIVE terminal-help paths — 27d added it to mountTapOptions.revealAnswer and I reported it as 'every phase', but practice/independent rounds are drags / sentence-finds / scene-taps. Added to MATCH_DRAG_N.terminalHelp, SENTENCE_FIND and TAP_IN_SCENE, each with stopNudge() first so the flow nudge cannot drag the hand off the answer. (3) STORY_SCENE picture drifted via `storyKenBurns` — killed engine-wide; a teaching picture must not move under a KG child. Root cause common to (1) and (2): verified narrowly, reported broadly.  28c: STORY_QUESTION stimulus is the IMAGE ONLY — the 🔊 glyph and the 'प्रश्न सुनो' label were hardcoded in the module (d.stim_hi only reworded the label), so no card could remove them. Tapping the picture still replays the question and the header chip still works: the affordance is gone, not the function. No thumb (mastery / hide_recall) now passes a null stimulus instead of rendering an empty card. The four AUDIO-ONLY chips (TAP_SHAPE_BY_NAME, TAP_LETTER_BY_SOUND, MASTERY_SILENT_PICK x2) are untouched — they have no image, so stripping them leaves a blank card; flagged for a ruling.  28b: PHASE GATE BACKGROUND GOES GRAY (Yasir + Figma ref). Scrim 35% -> rgba(64,64,70,.58) and backdrop-filter gains grayscale(.9) brightness(.92), so a colourful KG scene actually DESATURATES instead of merely dimming; grayscale rides the BACKDROP so the peeking Swiftie and the headline keep full colour. Also kills `body.is-start .phase-gate{background: transparent !important}` — the FIRST gate (landing->tutorial) had NO scrim at all, open as flag S2-a; this closes it. Verified by SCREENSHOTTING the gate (capture_pages cannot — it is a ~2s transient) on both the mid-lesson and is-start paths.  28a [code tags read `[27j]` — written before midnight, engine_bump rolled the date; grep [27j] for these six changes] (batched wave fixes, 6 module changes, all ADDITIVE — a card that does not opt in behaves exactly as before): SEQUENCE_COMPLETE takes an opt-in picture stimulus (d.img/picture/emoji) so build-the-word slides can show the thing being spelled; TAP_IN_SCENE gains the two-rung hint ladder + terminal help that GLOWS the target instead of solving it, and .tis-hot is now VISIBLE on every candidate (it was border:none/transparent, so a child had nothing to aim at); mountTapOptions finally speaks audio.correct after the tapped word (12 STORY_QUESTION slides were silent); MATCH_DRAG_N drop-zones speak on tap, reusing pair.match_audio; SENTENCE_FIND: rung 1 now plays hint1 (it played try_again), `hint` is spoken as the terminal line, and terminal help NO LONGER locks+completes the slide — RULE-9 breach, it was solving the answer for the child; PHASE_GATE_TITLE/VO gain `independent` as an ALIAS of practice — three rounds, not four: round 3 is named practice OR independent and a card using the latter got no round-3 gate. `mastery` is deliberately NOT gated (no round 4), so vo_pt_mastery stays unplayed and that verify_bundle warn is a checker artifact. Also: _tools/check_system.py now verifies the ENGINE READS hint1/hint per mechanic, closing a false green where authored hints could never play.  27h: F1 tutorial-frame fit — tall teach modules (STORY_SCENE .story-frame 900x432, GENDER_INTRO .gender-cat 430px) overflowed the 318px .tut-content and, because it is justify-content:center, split the overflow BOTH ways: heading 78-100% covered above, caption/word-chip behind the आगे pill below. Regression from the 25e/27c change that shortened every tut-card 87px. Now the picture SHRINKS (what the SME asked) instead of pushing the layout apart; scoped to .stage.tut so guided/practice are untouched. Cleared 6 requests across 4 games. · F2 shared baseline — centerInkGlyph ink-centred EACH glyph, so a word with an above-line matra sat up to 23px lower than a plain word inside one row (the SME's 'text alignment is not right', 7 of 17 pages). A row with >1 .ink-glyph now uses constant FONT metrics; a lone showcase glyph keeps ink-centring. Both verified by LOOKING at headless captures, not only by measuring.  ENGINE STAMP — the receipt (verify_bundle.py) asserts a built game carries THIS exact string; a stale/divergent engine → hard FAIL, so the wrong engine can never silently ship. BUMP IN LOCKSTEP with engine_guard.py + swiftpal_build.py + unified_build.py + verify_bundle.py on EVERY engine change (r2: drag/pattern feedback standard + PHASE_TRANSITION; r3c: off-white toybox bg, dual-coded counting options numeral+hand, full-body landing mascot, true-corner square/rect; r3d: Swiftie mouth-stops-when-silent (still frame), Arabic display numerals 1/2/3, landing shows full 1..n hand row, volume-chip aligned in header pill); r4: additive number-sequence path modules MEET_SEQUENCE + SEQUENCE_COMPLETE + SEQUENCE_NEXT (MTKGA01_L02_S04 "completes a number sequence within 20") — purely additive, existing lessons untouched. r4-landing (16c): landing recomposed to match reference — small corner mascot (230px, was 300), content re-centered (dropped padding-left:300 right-shift hack), VO chip moved from top-right to the mascot's shoulder (left:150/bottom:34, 58px). CSS-only; supersedes the 16b right-shift overlap fix.; 16d: TRUNK MERGE — unified the two diverged engine lines at base 12d: the 15e mechanics trunk (CONSERVE_COUNT + COUNT_ACTION + COUNT_DRAG_MATCH + ORDER_BY_WEIGHT + PICK_SET_BY_NUMBER, per_row/dense count-set grouping, bigNumCell numeral-only test options, title_first landing order) + the 16c r4 design trunk (boot loader, peek phase-transition, concept-strip landing, DS header, flat CTAs, sunburst/star-burst celebration, recomposed corner-mascot landing). Nothing dropped from either line. 16e: landing count-hero hand sizing FIXED — the .sg-hero sizing selectors never matched (template uses .sg-art); hands rendered natural-size, overflowing the card (title pushed outside the box, numeral-1 hidden behind the mascot — user-visible on MTKGA01_L02_S01). Retargeted to .sg-art .sg-hand/.sg-hand-cell/.sg-hand-num (112px; image-hero landings untouched). CSS-only. 16f: INTRO strip fit-or-wrap — old sizing assumed 1220px + a -100px breakout and punched wide strips (10 numerals, 7+ letters) through the tut-frame borders; now sized to the frame (960) and wrapping into two balanced rows below the 110px touch floor. Fixes MTKGA01_L02_S01 s00 (user-caught live) AND the HIKGH04_P2 letter-row daylight item. 21a (20a Figma-polish port): production expression heads (setSwMood sw_head_<expr>[_anim].webp + mascot.webp fallback), body-level start/end edge-layers + full-viewport dark blur phase-gate, inline SVG audio/hint/sg-vo chips, nudge_hand_new/nudge_tap_v2, SORT-01 opt-in one-by-one tray reveal + speak-on-match, INTRO picture mode (data.pics) + auto-INTRO instruction VO, transition-audio AUDIO_EXT fix, landing shape-tiles, self-disabling browser-TTS fallback for missing clips (ruled SHIP), F2F7FA ground + red/green-reserved sweep; merged WITH the live in-word-matra colouring + reveal_seq _sayThen strict-VO + MATCH_DRAG_N md-word WIP (nothing reverted). 21c (consolidated wave bump): +COMBINE_COUNT (Put-Together: drag group B onto A, merge to one row, tap-count total ≤10) and +TRACE_SHAPE (finger-trace the outline — a PRODUCE gesture; forgiving corridor, ~80% coverage → success, idle demo, upright/sharp/fixed-colour, no score/timer); MATCH_DRAG_N tap→LETTER (tap_audio) / correct-drop→WORD (match_audio) split (gated+fallback, siblings untouched); SEQUENCE_DRAG word-mode tap-a-tile→speak-word + glow-order + whole-sentence-read-at-end, SENTENCE_READ/SENTENCE_FIND word-by-word read-along hand-nudge (word-mode gated; letter-sequence untouched); landing gate cursor:default (hand-pointer on buttons only). All additive. 24a (HI01H08-fork port + N7-N10 audit bump): AUDIO GEN-TOKEN (_audioGen) — stopAudio/play supersede pattern kills echo/double-voice, orphaned clips, stale fallback-timer resume + cancelled-TTS resume (N7a); replay chips get navUnlock + guards (isPlaying / revealing / demoRunning / ownsAudio-without-replay) so फिर-सुनो mid-VO can no longer brick gated teach slides or gen-kill self-driving demo chains (N7b/N8); state.revealing gates drag + replay during reveal_seq/sortSeqReveal (N8 drag path); capture-phase DRAG VO-GATE on draggable tiles (isPlaying + 4s _voStart cap — speak-on-press tiles NOT over-blocked) (A1); mountTapOptions tap gate: one-tap-at-a-time _busy + 4s _vb + no taps during ANY VO + additive hint1 first-wrong clip (A2); auto walk-through INTRO/GENDER_INTRO ignore card taps until taught, then tap=replay (A3); playbackRate pinned 1.0 (A4); SORT tray ghost-slot .sort-ghost on placement (A5); MATCH_DRAG_N final-drop word no longer truncated by the celebrate VO (C); viewport pinch-zoom lock (N9); star-burst spark fill-mode both (N10). N11 (asset preload) deferred. 25a (drag hint ladder): dragWrong() now grades its spoken feedback like the tap path — 1st wrong plays the slide's hint1, 2nd+ plays hint (the level that GIVES the answer); all 12 drag wrong-drop sites inherit it with no call-site change, and cards without hint1/hint authored still play try_again unchanged (additive, zero sibling regression). Yasir ruling 2026-07-25: two hints everywhere, every game, every interaction type. 27c (autonomous teaching + tutorial fit): mountTapOptions honours slide.data.auto — a TEACHING slide now runs the whole beat itself (prompt on the picture -> teaching line on the right choice -> that choice goes green+pulses, wrong ones fade, its letter sounds -> आगे unlocks), taps dead throughout, no confetti/sfx; opt-in, and SENTENCE_SOUND/INTRO/GENDER_INTRO/MEET_* keep their own pre-existing auto paths (they return before mountTapOptions). CSS: .stage.tut q-rows that carry a picture stimulus lay it BESIDE the options — the 25e card leaves 273 design px and stimulus+gap+opt-cell need 434, so the grid track squashed to 43px and the cells spilled onto the picture (Yasir 2026-07-27, Antim T2/T3). 27g-fix (relabelled — 27d was taken by the terminal-help hand): the auto chain no longer points the hand at the picture stimulus — pointNudgeAt plants the fingertip 56px above an element bottom, i.e. straight over a .stimulus-pic .lbl, so the hand hid the very word being taught for the whole prompt beat.
  try { window.SWIFTPAL_ENGINE = ENGINE_VERSION; } catch(e){}
const $ = id => document.getElementById(id);

/* ---------- 1. SCALE THE 1333x750 STAGE ---------- */
function fit(){
  const vw = (window.visualViewport ? window.visualViewport.width  : document.documentElement.clientWidth)  || window.innerWidth;
  const vh = (window.visualViewport ? window.visualViewport.height : document.documentElement.clientHeight) || window.innerHeight;
  // contain-fit, scaling UP to fill the screen (no 1× cap, no margin) so a 16:9
  // viewport is covered edge-to-edge. Any leftover bars on non-16:9 are blue, not white.
  const s = Math.min(vw/1333, vh/750);
  document.documentElement.style.setProperty("--scale", s);
}
window.addEventListener("resize", fit);
window.addEventListener("load", fit);
if(window.visualViewport) window.visualViewport.addEventListener("resize", fit);
fit();

/* ---------- 2. SIGNAL BUS + OFFLINE TELEMETRY ---------- */
/* TELEMETRY: offline self-capture. Every signal is buffered to localStorage so
   the run survives a reload / works with NO host app. A full results record can
   be pulled via GameBus.downloadResults() (or the ?dev=1 button on the end
   screen). If `endpoint` is set AND the device is online, the final record is
   also POSTed — left null so the lesson is fully offline by default. */
const TELEMETRY = {
  endpoint: null,   // e.g. "https://lrs.example.com/swiftpal" — null = offline only
  storageKey: "swiftpal:run:" + CARD.skill_code + "_" + (CARD.part_label || "P1")
};

/* [spec] SWIFTPAL PLATFORM BRIDGE — routes every statement to the host: Android JavascriptInterface,
   iOS WKWebView, or web/electron postMessage. In the split-file games this is shipped as
   swiftpal-bridge.js; this book is a SINGLE-FILE offline monolith, so the same bridge is inlined here
   verbatim rather than added as a second file. Guarded with `||` so a host that injects its own
   window.SwiftPAL first always wins. */
window.SwiftPAL = window.SwiftPAL || (function(){
  const _platform = (window.Android && typeof window.Android.sendEvent === "function") ? "android"
    : (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.swiftpal) ? "ios"
    : (window.parent !== window) ? "web"
    : (window.opener) ? "electron" : "web";
  function _call(name, args){
    try{
      if(_platform === "android"){
        if(window.Android && typeof window.Android[name] === "function") window.Android[name](...args);
        else console.warn("[SwiftPAL Bridge] Android." + name + " not found");
      } else if(_platform === "ios"){
        window.webkit.messageHandlers.swiftpal.postMessage({ fn: name, args });
      } else {
        const target = (window.parent !== window) ? window.parent : (window.opener || null);
        if(target) target.postMessage({ source: "swiftpal", fn: name, args }, "*");
      }
    }catch(e){ console.warn("[SwiftPAL Bridge] _call error for " + name + ":", e); }
    try{ window.dispatchEvent(new CustomEvent("swiftpal:" + name, { detail: { fn: name, args } })); }catch(e){}
    try{ console.log("[SwiftPAL Bridge] " + _platform + "." + name, ...args); }catch(e){}
  }
  return {
    _platform: _platform,
    sendEvent(statement){ _call("sendEvent", [JSON.stringify(statement)]); }
  };
})();

/* [spec] URL-supplied journey binding, echoed verbatim into every xAPI statement's context.
   The host launches with ?context_id=...&journey_id=... (optionally &medium=); skill_code stays the
   stable content id of the book, so reusing it in another journey cannot collide. */
const _urlParams = new URLSearchParams(location.search);
const CONTEXT_ID = _urlParams.get("context_id") || null;
const JOURNEY_ID = _urlParams.get("journey_id") || null;
const MEDIUM_OVERRIDE = _urlParams.get("medium") || null;
/* [spec] question_format per answerable slide type (enum: mcq | timed_mcq | build | drag | tap_count).
   This card's answerable templates are STORY_QUESTION (listen to the story, pick the picture) and
   TAP_IN_SCENE (find and tap the thing in the picture) — both option/target picks, so both mcq. The
   drag/build families the shared engine can also serve are mapped too, with an "mcq" fallback for
   anything unlisted. The exact template always rides in context.template. */
const QUESTION_FORMAT = {
  STORY_QUESTION: "mcq", TAP_IN_SCENE: "mcq",
  TAP_LETTER_BY_NAME: "mcq", TAP_LETTER_BY_SOUND: "mcq", TAP_PICTURE_BY_LETTER: "mcq",
  TAP_LETTER_BY_PICTURE: "mcq", ODD_ONE_OUT: "mcq", TAP_GENDER: "mcq",
  TAP_PICTURE_BY_GENDER: "mcq", TAP_VACHAN: "mcq", TAP_PICTURE_BY_VACHAN: "mcq",
  MASTERY_SILENT_PICK: "mcq",
  SORT_GENDER: "drag", SORT_VACHAN: "drag", SORT_ATTR: "drag", SORT_SHAPE: "drag",
  MATCH_GENDER_PAIRS: "drag", MATCH_VACHAN_PAIRS: "drag", MATCH_DRAG_N: "drag",
  SEQUENCE_DRAG: "drag",
  EVIDENCE_QA: "mcq", BUILD_PUNCT: "build", SORT_QTYPE: "drag", SORT_WORDS: "drag", PUNCT_PICK: "mcq",   /* [reskin] this lesson's answerable types */
  MAKE_SET: "build", MAKE_NUMBER: "build", BUILD_TO_NUMBER: "build", PATTERN_BUILD: "build",
  CONSERVE_COUNT: "tap_count", COUNT_HOW_MANY: "tap_count", COUNT_TAP: "tap_count"
};
/* Answerable == present in the map above. Everything else (STORY_SCENE, INTRO, MEET_*,
   PHASE_TRANSITION, CELEBRATION, …) is a passive screen and reports screen_viewed instead. */
const ANSWERABLE_TYPES = new Set(Object.keys(QUESTION_FORMAT));

/* [spec] The game's internal bus is GameBus (window.GameBus). The global SwiftPAL name belongs to
   the bridge above, which GameBus.xapi() hands each statement to — this bus used to be called
   SwiftPAL itself, which would have collided with the bridge. */
const GameBus = window.GameBus = {
  signals: [],
  validatorReport: { missing_signals: [], errors: [], passed: false },
  firedSet: new Set(),
  startedAt: Date.now(),
  _qStats: {},   // { [question_id]: true|false } — was the FIRST attempt on that question correct? feeds activity_completed's score
  emit(name, payload){
    const evt = Object.assign({
      ts: Date.now(),
      skill_code: CARD.skill_code,
      lo_code: CARD.lo_code,
      signal: name
    }, payload || {});
    this.signals.push(evt);
    this.firedSet.add(name);
    try{ console.log("[signal]", name, evt); }catch(e){}
    /* [spec] NOISE CONTROL: the raw swiftpal:signal firehose (30+ internal signal names) is DEV-ONLY.
       Production hosts receive only the 7 xAPI verbs, identically shaped from every book. This used to
       postMessage unconditionally, so a host saw ~30 undocumented event names from this book alone. */
    if(_urlParams.has("dev")){
      try{ window.parent?.postMessage({type:"swiftpal:signal", payload: evt}, "*"); }catch(e){}
    }
    this.persist();
  },
  /* full results record (used for download / POST / end-of-lesson dump) */
  exportResults(){
    const ms = (typeof state!=="undefined") ? state.masteryAttempts : 0;
    const mh = (typeof state!=="undefined") ? state.masteryHits : 0;
    return {
      skill_code: CARD.skill_code, lo_code: CARD.lo_code, part: CARD.part_label || null,
      started_at: this.startedAt, exported_at: Date.now(),
      mastery: { hits: mh, attempts: ms, score: ms ? mh/ms : 0 },
      validatorReport: this.validatorReport,
      signals: this.signals
    };
  },
  /* silent: flush the running buffer to localStorage (survives reload / offline) */
  persist(){
    try{ localStorage.setItem(TELEMETRY.storageKey, JSON.stringify(this.exportResults())); }
    catch(e){ /* private mode / quota — non-fatal, postMessage + memory still work */ }
  },
  /* pull the run as a JSON file (teacher/dev; not in the child's flow) */
  downloadResults(){
    try{
      const blob = new Blob([JSON.stringify(this.exportResults(), null, 2)], {type:"application/json"});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url; a.download = CARD.skill_code + "_" + (CARD.part_label||"P1") + "_results.json";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(()=> URL.revokeObjectURL(url), 1000);
    }catch(e){ console.error("[telemetry] download failed", e); }
  },
  /* [spec] xapi(verb, object, result, ctx): build the standard { verb, object, result, context }
     statement and hand it to the platform bridge (inlined above). Falls back to a direct
     postMessage({type:"swiftpal:xapi", statement}) if the bridge is somehow absent (standalone dev). */
  xapi(verb, object, result, ctx){
    const statement = {
      verb: verb,
      object: object || null,
      result: result || null,
      context: Object.assign({
        skill_code: CARD.skill_code, lo_code: CARD.lo_code,
        medium: MEDIUM_OVERRIDE || CARD.medium || "hi",
        session_ms: Date.now() - this.startedAt,
        context_id: CONTEXT_ID, journey_id: JOURNEY_ID
      }, ctx || {})
    };
    if(window.SwiftPAL && typeof window.SwiftPAL.sendEvent === "function") window.SwiftPAL.sendEvent(statement);
    else try{ window.parent?.postMessage({ type: "swiftpal:xapi", statement }, "*"); }catch(e){}
    try{ console.log("[xAPI]", verb, statement); }catch(e){}
  },
  /* [spec] xapiForSlide: same as xapi(), auto-filling the per-question context every screen/question
     verb needs (question_id, question_index, template, question_format, phase). */
  xapiForSlide(verb, slide, object, result, extraCtx){
    this.xapi(verb, object, result, Object.assign({
      question_id: slide.id,
      question_index: (typeof state !== "undefined") ? state.idx : null,
      template: slide.type,
      question_format: QUESTION_FORMAT[slide.type] || "mcq",
      phase: slide.phase
    }, extraCtx || {}));
  },
  /* [spec] Build + emit the standard question_answered statement, and remember whether THIS question's
     FIRST attempt was correct — that map is what activity_completed's score is averaged from.
     result.score is 1 only on a first-attempt correct; attempt counts taps on this question. */
  sendQuestionAnswered(slide, r){
    if(r.attempt === 1 && !(slide.id in this._qStats)) this._qStats[slide.id] = !!r.is_correct;
    this.xapiForSlide("question_answered", slide,
      { type: r.objType || (r.mediaUrl ? "image" : "text"),
        id: (r.objId != null ? r.objId : ("opt_" + (r.ui_index != null ? r.ui_index : "x"))),
        text: (r.text != null ? r.text : null),
        mediaUrl: r.mediaUrl || null,
        ui_index: r.ui_index, original_index: r.original_index },
      { score: r.score, attempt: r.attempt, is_correct: r.is_correct });
  }
};

/* ---------- 3. AUDIO ---------- */
let isPlaying=false, currentAudio=null, _audioGen=0, _voStart=0, _landingVoHasPlayed=false;
let isMuted = false;
let backgroundMusic=null, bgmFadeFrame=0;
const BGM_VOLUME=.20, BGM_VO_VOLUME=.085;
function fadeBackgroundMusic(target){
  if(!backgroundMusic) return;
  if(bgmFadeFrame) cancelAnimationFrame(bgmFadeFrame);
  const from=backgroundMusic.volume, started=performance.now(), duration=560;
  const tick=now=>{
    const t=Math.min(1,(now-started)/duration), eased=t*t*(3-2*t);
    backgroundMusic.volume=from+(target-from)*eased;
    if(t<1) bgmFadeFrame=requestAnimationFrame(tick); else bgmFadeFrame=0;
  };
  bgmFadeFrame=requestAnimationFrame(tick);
}
function startBackgroundMusic(){
  if(!backgroundMusic){
    backgroundMusic=new Audio("assets/Audio/standard_background_music_2.mp3");
    backgroundMusic.loop=true;
    backgroundMusic.preload="auto";
    backgroundMusic.volume=isPlaying?BGM_VO_VOLUME:BGM_VOLUME;
  }
  const attempt=backgroundMusic.play();
  if(attempt&&attempt.catch) attempt.catch(()=>{});
}
function setMuted(m){ isMuted = m; if(m && typeof stopAudio==="function") stopAudio();
  document.querySelectorAll(".audio-chip").forEach(c => c.classList.toggle("muted", m)); }
function syncSpeakerDisabled(root=document){
  const selector = ".audio-chip, .tut-audio, .sg-vo, .read-whole-btn";
  const speakers = root.matches?.(selector) ? [root] : [...(root.querySelectorAll?.(selector) || [])];
  speakers.forEach(c=>{
    const disabled = !!isPlaying;
    c.classList.toggle("vo-disabled", disabled);
    c.setAttribute("aria-disabled", String(disabled));
    if(c.matches("button")) c.disabled = disabled;
  });
}
function setPlaying(on){
  // the dynamic Swiftie sits header-left; the audio chips pulse to signal playback. r4/F1: share the
  // .playing toggle across the header chip AND the tut-card replay chip (the header is hidden in the
  // tut frame, so the in-card .tut-audio is the only visible affordance and must react to VO too).
  isPlaying=on;
  fadeBackgroundMusic(on?BGM_VO_VOLUME:BGM_VOLUME);
  if(on && document.body.classList.contains("is-start")) _landingVoHasPlayed=true;
  document.body.classList.toggle("landing-play-ready",
    document.body.classList.contains("is-start") && !on && _landingVoHasPlayed);
  const landingVideo = $("sgBgVideo");
  if(landingVideo && document.body.classList.contains("is-start")) landingVideo.volume = on ? .08 : .32;
  /* [30g] VO LOCK — untappable, zero visual. See style.css. Driven off setPlaying (never a timer) so
     the lock cannot outlive the audio; toggled on `on` alone so it tracks the tap gate under mute. */
  document.body.classList.toggle("vo-lock", !!on);
  if(on) _voStart = Date.now();   // drag VO-gate 4s safety: stamp when a VO began so a stalled clip can't soft-lock the tiles
  document.querySelectorAll(".audio-chip, .tut-audio, .sg-vo, .read-whole-btn").forEach(c => c.classList.toggle("playing", on && !isMuted));
  syncSpeakerDisabled();
  syncNavButton();
  /* [h01 local] RULING_no_tapping_during_VO (Yasir 2026-07-29). The tap gate already refused taps
     while a VO played, but nothing on screen changed — so a tap during the prompt did nothing at
     all, with no acknowledgement. That silent non-response was the defect, not the blocking.
     body.vo-lock drives the VISIBLE half in CSS. Toggled here because setPlaying is the one choke
     point every end-of-audio path runs through (natural end, stopAudio, superseded generation,
     cancelled TTS, missing-clip fallback), so the lock can never outlive the sound — no timer of
     our own, per the ruling's "a slide stuck disabled is worse than the original bug".
     Gated on `on` alone, NOT on isMuted: the engine's own tap gate uses isPlaying regardless of
     mute, and showing "live" while taps are refused is exactly the bug being fixed. */
  /* [30f] the page-wide VO dim was REMOVED here — Yasir: "dont block the entire screen fam".
   It also set pointer-events:none, which stopped a tap during FEEDBACK audio from reaching the tap
   gate and so silently undid 28t (feedback taps must count). See the shared engine's note. */
}
/* stopAudio(): hard-stop the current clip AND bump the playback generation so any in-flight
   callback (a chain's onended, a fallback timer, a cancelled TTS onend) becomes a no-op. This is
   what prevents the "voice echo": a stale callback from an earlier tap/slide can no longer fire a
   NEW clip on top of the current one, or resume onto the next screen. */
function stopAudio(){
  _audioGen++;
  if(currentAudio){ try{ currentAudio.onended=null; currentAudio.onerror=null; currentAudio.pause(); }catch(e){} currentAudio=null; }
  try{ if(window.speechSynthesis) speechSynthesis.cancel(); }catch(e){}   // [20a] also stop the TTS placeholder
  setPlaying(false);
}
/* [20a REVIEW PLACEHOLDER] TTS fallback: until real VO is recorded, speak the clip's authored Hindi text
   (CARD.assets.audio_text[id]) via the browser so the game is audible for review. SELF-DISABLING — fires
   only when the MP3 is missing; once real clips ship, play() succeeds and this never runs. Returns true if
   it took over (so play() doesn't ALSO schedule a silent beat). */
function _ttsSay(src, onDone){
  /* [30o] THE TTS FALLBACK IS GONE (Yasir 2026-07-31): "there should be no way to fall back on tts,
     it is fine if we dont have audio, we will know if an audio is missing but having tts is worse."
     A synthetic voice MASKS a missing clip — it made a broken build sound finished. Silence is
     diagnostic. Kept as a stub, not deleted: an unfound call site would ReferenceError and take the
     slide chain down, whereas false routes it into the silent-beat path that already exists. */
  return false;
}

/* Duration of the authored VO while recordings are still absent. This keeps the speaker waves
   aligned with the words being revealed on screen; once a real clip exists, its onended event is
   authoritative instead. Short word clips stay short, while poem stanzas receive a natural read. */
function authoredVoHoldMs(src){
  if(!src) return 0;
  const file = String(src).split("/").pop() || "";
  const id = file.replace(/\.[^.]+$/, "");
  const txt = (CARD.assets && CARD.assets.audio_text && CARD.assets.audio_text[id]) || "";
  if(!txt) return 1200;
  const chars = Array.from(String(txt).replace(/[\s।,!?—–…“”'\-]/g, "")).length;
  return Math.max(900, Math.min(11000, 450 + chars * 92));
}

/* play(src, onEnd): real MP3 if path exists; an authored-duration silent beat if that recording
   has not been added yet. A genuinely empty slot stays visually silent: the chip remains visible,
   but its waves do not animate.
   ECHO GUARD [24a N7]: each call captures a generation token after stopAudio()'s bump; if a newer
   play()/stopAudio() has since run, this call's fire/onFail/fallback-beat bail — a superseded chain
   can never start a clip over the current one, orphan the new clip (stale onFail nulling currentAudio),
   or resume onto the next slide (fallback timers + cancelled-TTS onend die with the token too). */
function play(src, onEnd, onMissing){
  stopAudio();
  const myGen=_audioGen;
  if(!src){
    setTimeout(()=>{ if(myGen===_audioGen && onEnd) onEnd(); }, 800);
    return;
  }
  setPlaying(true);
  const plannedEnd = Date.now() + authoredVoHoldMs(src);
  let done=false; const fire=()=>{ if(done || myGen!==_audioGen)return; done=true; setPlaying(false); if(onEnd) onEnd(); };
  {
    const a=new Audio(src); currentAudio=a;
    a.playbackRate = 1.0;   // natural recorded pace — any pep-up factor makes HUMAN VO too fast (Yasir 2026-07-24)
    let handled=false;
    /* [30o-fix 2026-07-31] the 30o edit left the arrow body UNCLOSED — its `};` landed inside the //
       comment, so the parser ran on until `} else {` → SyntaxError → every script dead → the boot
       loader never dismissed ("file not loading"). Same truncation in both games; closer restored. */
    const onFail=()=>{ if(handled || myGen!==_audioGen)return; handled=true; currentAudio=null;
      /* [r39] A caller may offer a stand-in for a line that has not been recorded yet. Without one
         we keep the old behaviour: hold for the authored beat so the pacing survives, in silence. */
      if(onMissing){ setPlaying(false); onMissing(); return; }
      setTimeout(fire, Math.max(0, plannedEnd - Date.now())); };   // authored visual VO beat; never synthetic speech
    a.onended=fire;
    a.onerror=onFail;
    /* [30n] AN AUTOPLAY REFUSAL IS NOT A MISSING FILE. a.play() rejects both for a broken file — where
       _ttsSay is the intended review placeholder — and with NotAllowedError under the browser's autoplay
       policy, which fires on every load before the first gesture. Treating them alike made a game with
       complete human VO speak the OS voice on its landing, with the volume button as the gesture that
       finally let the real clip through. fire() here is NOT optional: setPlaying(true) already ran, so
       bailing without it leaves body.vo-lock on and the whole screen untappable. */
    a.play().catch((err)=>{
      const nm = err && err.name;
      if(nm === "NotAllowedError" || nm === "AbortError"){
        if(handled || myGen!==_audioGen) return;
        handled=true; currentAudio=null; fire(); return;   // silent; the first gesture starts the real clip
      }
      onFail();
    });
  }
}
/* [r39] SPEAK A LINE, WITH A STAND-IN.
   The lesson authors a clip per screen in card.json, but only the ocean games have recordings so
   far — everything else pointed at a vo_*.ogg that does not exist and therefore played silently.
   voSay() asks for the authored clip first and, when that file is not there, falls back to the
   generic line of the same kind (शाबाश! / दोबारा कोशिश करो।) that DOES exist, so praise and retry
   are voiced on every screen today. The moment a real recording is dropped in it takes priority
   again with no code change. `kind` may be omitted when no stand-in would make sense. */
function voSay(src, kind, onEnd){
  const fallback = kind && window.OCEAN_VO && OCEAN_VO[kind] ? ()=> oceanSay(kind, onEnd) : null;
  if(!src) return fallback ? fallback() : play(null, onEnd);
  return play(src, onEnd, fallback);
}

/* playSfx(id): fire-and-forget sound effect on its OWN Audio element so it can
   overlap the spoken VO (does NOT touch currentAudio / the play() chain).
   Silently no-ops if the file is missing or playback is blocked. */
function playSfx(id){
  if(!id) return;
  try{
    const a = new Audio("assets/Audio/" + id + "." + AUDIO_EXT);
    a.volume = 0.7;
    a.play().catch(()=>{});
  }catch(e){}
}
/* ---------- game-feel: procedural SFX (no audio files) + success particle burst ----------
   WebAudio resumes on the first user tap (autoplay policy), so taps/answers always sound. */
let _juiceAC = null;
function _ac(){ if(!_juiceAC){ try{ _juiceAC = new (window.AudioContext || window.webkitAudioContext)(); }catch(e){} }
  if(_juiceAC && _juiceAC.state === "suspended"){ try{ _juiceAC.resume(); }catch(e){} } return _juiceAC; }
function _tone(freqs, type, dur, vol){ const c = _ac(); if(!c) return; const t0 = c.currentTime;
  freqs.forEach((f, i)=>{ const o = c.createOscillator(), g = c.createGain(); o.type = type; o.frequency.value = f;
    const t = t0 + i*(dur/freqs.length); g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t+0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur/freqs.length); o.connect(g).connect(c.destination); o.start(t); o.stop(t + dur/freqs.length); }); }
const sfxTap       = ()=> _tone([520], "sine", 0.09, 0.09);
const _kitSfx = Object.create(null);
function playKitSfx(name, file, volume){ if(isMuted) return; try{
  let a = _kitSfx[name]; if(!a){ a = _kitSfx[name] = new Audio("assets/Audio/" + file); a.preload = "auto"; }
  a.volume = volume == null ? .85 : volume; a.currentTime = 0;
  const p = a.play(); if(p && p.catch) p.catch(()=>{});
}catch(e){} }
const sfxCorrect   = ()=> playKitSfx("correct", "sfx_correct_new.ogg", .85);
const sfxWrongSoft = ()=> playKitSfx("wrong", "sfx_wrong_new.ogg", .85);
const sfxConfetti  = ()=> playKitSfx("confetti", "sfx_celebrate.ogg", .85);
const sfxPlayButton = ()=> playKitSfx("playButton", "sfx_play_button.ogg", .85);
const sfxNextButton = ()=> playKitSfx("nextButton", "sfx_next_button.ogg", .85);
const sfxStarPop   = ()=> playKitSfx("starPop", "sfx_star_pop_new.ogg", .80);
/* [r32] STAR CHIME — one bright "ting" per star as it lands, rising across the three so the row
   reads as a little fanfare rather than the same note three times. Two partials and a fast
   exponential decay is what makes it read as a bell instead of a beep. */
const sfxStarTing = (i)=>{ const c = _ac(); if(!c || isMuted) return;
  const base = [784, 988, 1175][i] || 784, t = c.currentTime;
  [[base,.13],[base*2,.05]].forEach(([f,v])=>{
    const o = c.createOscillator(), g = c.createGain();
    o.type = "sine"; o.frequency.setValueAtTime(f, t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(v, t + 0.012);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.55);
    o.connect(g).connect(c.destination); o.start(t); o.stop(t + 0.6); }); };

/* [r30] BUBBLE POP — the supplied recording (soundreality-pop-sound-423716.mp3) replaces the
   synthesised pop MATCH_THE_PAIR used to fire. The source was 1.78s but the pop itself is only the
   0.17s transient between 0.11s and 0.29s; the rest was silence, and the 113ms of it at the FRONT
   delayed the sound audibly after a match. Trimmed to that transient with a short fade, mono,
   and inlined as a data URI (~4 KB) so the pop survives the HTML being served without its assets
   folder — the failure that lost every image on the first Vercel upload. Same mute rule as every
   other sfx. */
const POP_SFX = "data:audio/mpeg;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjYyLjEyLjEwMQAAAAAAAAAAAAAA//twwAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAANAAARJAAkJCQkJCQkNjY2NjY2NjZJSUlJSUlJSVtbW1tbW1ttbW1tbW1tbYCAgICAgICAkpKSkpKSkqSkpKSkpKSktra2tra2trbJycnJycnJ29vb29vb29vt7e3t7e3t7f////////8AAAAATGF2YzYyLjI4AAAAAAAAAAAAAAAAJASSAAAAAAAAESSWSKLYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/7cMQAAAAAAaQUAAAiDSegAy1QANbgYaiKgYjU/aB4DfMlADlAdbTQAzhmlAwwCw8DQoTAx0KvwCQONETv/kUD8QvsAUEP/AaCAYDKw0g/v/4CgHC3sL4BvgkhJ//4zAcaHzAHAgA4YA2Bja///C08PbCysBgJigCbHeiT////k+cNCWNiCFo3NP//mQTAjqQ/////4Y0aVeBwOB0uRweBwOBiIhADEJwzkw+Ao4lqw39MpuEWjWQjioqgBoGALCQABMAZABTGlAsIweQEYgWjjPT214zEMTnKjeeAAAM1QJ4w5GWwyR+MqztjQbGF4lmDojGOQXf/5z9T8TVg5jGgKjCQCjIEJTCQOKfvNfh9a/0wkAQyXG8eHMIBQkFoyKErufe5cx/X7zMFQbMWRTMQw/MRwjNeD+P/+3LEUAAeFVVzuf6gGkCbKrO28AAiBYMUAiw/888Of/7/9GCwIGBQDAoDDDkHTAsBw4AzBoGBIDQUCf//dc/H+/////8v78Uw91OcrQ53///5/6////////sRiHOSzfaSMSyWXEZgAAAgAAGiLcYAWkqd9x4IMAFVimDDpvUadNLmKWxydGKsBuC0Z8RFAQBAPBcTRawn0a2YKdIKDZBUl5J8TlZtWuP7QGOLS+ffUE5VSui5LTCy21jfxmtaf6tEzCjQ9yvcPvrG9+uPvW9/Vn0befFKhA1OwaEQ8eGhFMdANA0ViZYwCuTBq4FdCzp6JjyzuGnMAAAAAAAAuTLqRQtOtNSkqgo8DhwCZ20GLJQCJDLCc1GLNy6TXHM0iDOoXTMjkxMUCwA/i2NYyfmZ0en/uVanl9qTOf/7cMQiAJKZOUmtsNECW6InoZ4k8LUVHWuJXnGW3yCkzJCzJQsrLrEyvAGEma0s9ZSmvmFEDViFW2ZJ0H7l1sP4fc/eHeI83uPUPrN7jHZ5aZqniLiyi6VrAjw28RvAwTDbtGzvqgAAQPzThoBDZLHEjPgHPTDRZEJgOCDgIGpigGG/huYjdIIBAjAgKMS4AqERYMtavReklzg1o/BUDOHiI4REzJ2JqWSIgPBsHQu0ICUkaLxQxSRJupQ+hkvCUZJgKGUYkHVZxViqyxKLL0Ln6StIUcKNdFsYrF542z+nk/nrxz1HJbGv8ZGkjQVHCQkJAq7ztD1DiQ97/KoA/vv4YJEgCG9wxKSxgvCFpGC3SZBfpoFsmon6aoD5yJFmXA+aQJhiQrmBwsX6fekJy5ectQjkalZEZFb/+3LEHgCTvS00LjDRgkunJhnGFjgSlcB+XWFrzS2It0MEEfVQREYyRQJhKLTT5eOm4Tk8TH0cbjKcBJZBie5E6TLOfKahJPC8EkSyI0AqL6oLgXvvC2VJrPRsNut+/bb9PmJ5MV8dmdMHDDXPToNvIrc5S+5/0ICBvHsoSPFgICAkBA0ZaO5o4EmHDacxtB51tGJFyY9L5jFvGahaYBJBgcaFkyYLqXxGF3Fq9cyPzQNiUUT6lD1LW/QchBIS0Ss+jsVozYurW4vZrt2KWgMn7LIrFMkk1N0KWBtbj/fBba/B0auwdHHEREUQpqA1Sl+JCxS5TUNTUzmrps6NMsSFodo8myYMle2bqkAAABPZTAyKoGABh0SBA2MTEwdIJgqVnLCaZCX5/l+YQ3HpvAo6GkwoY7hQBDiRr//7cMQYAJN08SbObSvB4h4mKayhUDNrtPLH3lSwTKsXCXKiU2j6w7AsMWrV/WVZ4okuFe3yt3ZY11duRAJThI0BYu0yAdhU7iiQfEQKgmTBRCiREgaVQIdPxkXxVkyQLH04LLQukFNurbzy/8esbpZmdNpNI0aMJmGpJUoquWtfacABBdu/ktV0tZryxQAZGiYgMALCY+yZapsxnxijYdvwKSYyrn7YmIGICpSz1E4AoA4Q7cqvwPcHkYmH52VYGxDqOTruLoQBpJjd1IxBtrGowq2GCxTKI6ujr0yybFp13kgow2HBd0+UDqwGm1dXj0KS5FaFaEa69NVAQADP9Z0pWocl6vQFDRlSiaaCGQ0R95wSyJ002YgQHDnBqy6HTIKCocvVozYz7DsclMJYU6bkpWMzisTaVTv/+3LEH4CRINkgzbDWwskp4cHHlujTV0lCmq4yaSqKj0XETX2XHUNdswdPM1d46GTTme7xRwol7eArWTCTL00YgaS2fvNwLlgbEqz0YoLqCin7KiRvWvYdnrEXxdKcGvmmvJphQATocEAg+BCsN1UExyQzhDRMbNgyESjXYBNQJgkMYgAgOCYWAioWmLNeRYJVOVPcywIACRjBAgYp0oQOO76ZK93Bbp0xHKQYENWvR0JlmTwEmTOIeBdmqczFVaG7kjMr+zFCP8a8aM+clSyta7ZlGc7e9gx1KwGQuGxEN71xZVConJukjSKueslI0HfpbjRgYeRqOrL2W8ileiiKK+gg+xm2dQ9kebd7Ls/V//tV/6VIUqgQwEFmwYtGMgJqhOc4smLmZy5cYsrmQAxghiaCACoAJFLerP/7cMQUAZNs9RIN4Y9CCpljqael6GcuYjEFK7GQLVcdQZGYuoGHLNIrsnjeqTCku7l+ocQVgaeaS1CIwqUE2yOaiSEpXSBosXUElxcLO6KBELyWFeJi0oXPmaWzrs5GoSOddxYWzKkcRfoha7FRqr1I9pNP+FbCtcMIeNBZkJLLNJsMK/rNff0hQAFT90EWkSAMKgAqCBwsxUo100+lc6cQVlFVGbwoCQyIwYKjcHkbNy3sB4oQ2QAcKpLALAc86phslN+kaYsU9l5rbe1KgDwmJzTA8whauDoocr+hgrKmduN3sa2CcrRr7d007HBAyDZB9bRrzw9VtynLCTWLiU8/ILMU+a0Blb8S6AAAf8ZW2JcDglUDGOxMYVEQqVDZLGBZDMpoYcDIYqzrPCa2FgKHCAK8ujFaSPT/+3LEFwOTENsUTmmNAlmf4cG8MfCsxlrYAKAR3VuDBYQCXJS8WpnF1Phawc6FwZqB5Mjsdw64uBsUQtIr+NGC335hyEqjyyPVlTFHG1zyE7B+skFYvu+atyfaWLUTfRbhYVeDwMig6sQnD0aYFi6AVDUONCQ+yTw928kVuy5yj8pbHEe22GREzIrMUPQI3G07xiUOEsJil4cy7GLJpkhyYmBJjJcuBL5yfkcjVucptxbLWRU4O0csswUFcOXx+ls0usYBV1TRaKwRnD7cXJkjOlWyCu7MegeQS3dmWl1+LbXTFyIQWlX1eRLoIZRs18rK4vWDGNs/4xcepkqm4e6XZo7vVt+5/wjAqhrC8w8VX6UWJ3//1tfHm7toCgoVGM3JGZghh26B9xpvUQasqGqs5mKSReZhB+Ag1f/7cMQSAZDo6w4NbYvB2Jci9awloBu/EJJLn6XS77RWJLcTSTVRzXgwlZ0ols/Ep+1uPS2G1cYNLhmffFh0VdqiACTRUHYrnN1x219smjakQYSteN5Zx1Y4a7410LjKizXpVmaobjymu73TXtpHHD2pfcqhJbNIcnAAABzfzVt/W6LRUALmmfEG8XnHYGuZB+c1dQQFMCTuxBR2pBSWbME2IYdZYZvIMdxj1yA4Got9PvVpQCvsy84Mih5RU1Bpm33KUO3nmrBpbM+X/CG7/mpEQSC4sIVvX71B18s18jzUtS7t07HyokLLLEl3Lt11gAAAD8y1JI0h3Y0ZOHmKj5qIwayVHMpRkBoGlQBWzK5OXsS8aI1WzJJF74UCgKTJAC4jL3yVMhSy1pEVJJpN5BQTGgScJyMiWAX/+3LEJQEPnMcMzeUtAacYovWgmsJRGTGSY8QQUXnV7Mi3yVUEqcI609FcIt1PJSMrIYSVZoiNOH1tgHmNX3oH+R2fo7NTn9cAAAABIUn5/UjLKWUrCvoYAEAxQYPGURjRZkjIQkURFjsRispx3yRU0vldWXcXnEm+is/ugJWrLd0Ht3ooiM9z92Y02Mef7rPjcuMlt+NUSj+kzjNP88RsV5THPvYCpZpudcWyMUFrB49KwAAAAEApzv/Un3xdpma9BwAUIN6EroOZkgIHP4yhoGIlH9mX3VaczEASVIHgakUJFVkM3d/MMBtMXTgxpIK4vuRnFskeOzI+i12Se4LPES0qV33ZH5ekSkXZ76956VekRXsW7MwgAAEAEklSWG6uwY3NSseMmKy5rIKUx5TuAxKTxlvzyRSTIf/7cMREAAyUhRFMsM7RJI5i9BwkonFQyVhn/r/21sc/t1yViVdzffVv+xzr6fFgkxF9XXZU/X/Xnv+m/7mdl/S9gFAXKNZWzahs4NqNMvTCxY0alAHB1ap4F+p9wmvv9TQpIlQURAsiS9SsJiDRBFpYJaxu6/WE/zKYi7wSKYft4o66LQYdfMmC4ASBoRE6BDIFYgqiT61yPkC/Hu+cuarYx6yFCKE2YwWWIi4JKdBVpNCf9Vv/cjVLA75GCxAME0KFkzAODgKmNVjOABDJR7MJrXhjiKkxoailPxK09UTehWZJJTJVIWJA0JElM0FZsQTQyMoeTPAsrXIaAO1rkAPTkviQTjIcjZLc9CZUlLNqsqqQply4+e2s0XXrWa6ye2x/vd1CJzwTGgs8NYavcr52BjkulDElghL/+3LEfwPPPMjyDeUtge+Z3IHNMWgEYgeCVhnQpqbB/aRpPp0gBoxpvAJrShsq5kFwvAuWLFn2cuLY01qON3W4ZWBUZyCFyKXsllToxSjs01ekYdGGvT96NZymWw09TrMBfKHruFrdNXjOnixaQ5EgWFa+/UoevKxK6jHNhlGPQsNNylFS1UxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/7cMSWg88E1MgtYQ+IAAA0gAAABFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVU=";
let _popSfx = null;
const sfxPop = ()=>{ if(isMuted) return; try{
  if(!_popSfx){ _popSfx = new Audio(POP_SFX); _popSfx.preload = "auto"; }
  _popSfx.volume = .85; _popSfx.currentTime = 0;
  const p = _popSfx.play(); if(p && p.catch) p.catch(()=>{});
}catch(e){} };
/* In-lesson celebrations use the same retuned canvas burst as the end screen. */
function burstStars(){ const stage = document.querySelector(".slide-stage") || document.body; starBurstEffect(stage); }
/* dynamic Swiftie buddy: swap pose + a little pop on every reaction (correct/wrong/explain/celebrate) */
// [20a mascot-01] moods -> production EXPRESSIONS (head webp), not idle-gif basenames.
const SW_POSE = { talk:"talking", point:"talking", idle:"talking", happy:"celebrate", celebrate:"celebrate",
                  hint:"hint", teach:"hint", idea:"hint", tryagain:"tryagain" };
const SW_STILL = (() => { try { const q=new URLSearchParams(location.search);
  return q.has("still") || (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches); } catch(e){ return false; } })();
let swMood = "point";
/* Swiftie's mouth animates ONLY while a voice clip is sounding; the instant audio ends we freeze to
   the still closed-mouth frame. Driven off isPlaying (toggled by setPlaying at every clip start/end). */
function swApplyPose(){ /* [20a] retired: heads no longer couple to isPlaying (setSwMood drives them). */ }
function _swApplyPose_dead(){ const img = document.getElementById("swBuddyImg"); if(!img) return;
  img.src = "assets/UI/" + (isPlaying ? (SW_POSE[swMood] || SW_POSE.talk) + ".gif" : SW_REST + ".png");
  img.style.display = ""; }
function setSwMood(m){ swMood = m;
  const img = document.getElementById("swBuddyImg"), w = document.getElementById("swBuddy");
  if(!img) return;
  const expr = SW_POSE[m] || "talking";
  const animated = expr !== "talking" && !SW_STILL;   // resting face is the static talking head
  img.onerror = () => { img.onerror = null; img.src = "assets/UI/mascot.webp"; };   // [mascot-10]
  const bust = (animated && expr === "celebrate") ? ("?r=" + (state.slideStart || 1)) : "";  // [mascot-08] replay play-once
  img.src = "assets/UI/sw_head_" + expr + (animated ? "_anim" : "") + ".webp" + bust;
  if(w){ w.dataset.expr = expr; w.classList.toggle("anim", animated); } }
/* FLN toolkit's new correct-answer confetti: VIBGYOR paper pieces with a
   weighted star/rectangle/line/square mix and two distinct flutter regimes. */
const CONFETTI_COLORS = [
  ["#8B2FC9","#5E1C8C"],["#3F51B5","#27358A"],["#1E88E5","#135FA6"],
  ["#22B24C","#157A34"],["#FFD21E","#D9A800"],["#FF8A1E","#C75F00"],["#E5322D","#A81F1B"]
];
const CONFETTI_SHAPES = ["st","st","st","st","rc","rc","ln","ln","sq","sq"];
function confettiRnd(a,b){ return a + Math.random() * (b-a); }
function confettiCannon(withStars=true){
  sfxConfetti();
  document.querySelectorAll(".fx-confetti").forEach(x=>x.remove());
  const host = document.body, n = 80, dist = (window.innerHeight || 800) + 60;
  let maxLife = 0; const wrap = document.createElement("div"); wrap.className = "fx-confetti";
  for(let i=0;i<n;i++){
    const z = confettiRnd(.75,1.15), fall = confettiRnd(1.1,1.8)/z, delay = confettiRnd(0,.35);
    maxLife = Math.max(maxLife, fall + delay);
    const pair = CONFETTI_COLORS[i % CONFETTI_COLORS.length], flutter = Math.random() > .22;
    const rockT = flutter ? confettiRnd(.6,1.2) : confettiRnd(.75,1.5);
    const sway = flutter ? confettiRnd(10,34) : confettiRnd(2,8);
    const drift = flutter ? confettiRnd(-12,12) : confettiRnd(-45,45);
    const bob = flutter ? confettiRnd(3,7) : confettiRnd(2,4);
    const p = document.createElement("i"); p.className = "p";
    p.style.cssText =
      `--x:${confettiRnd(-2,98).toFixed(1)}%;--dist:${dist}px;--fall:${fall.toFixed(2)}s;`+
      `--delay:${delay.toFixed(2)}s;--drift:${drift.toFixed(0)}px;--sway:${sway.toFixed(0)}px;`+
      `--bob:${bob.toFixed(1)}px;--rockT:${rockT.toFixed(2)}s;--amp:${Math.round(confettiRnd(28,52))}deg;`+
      `--yaw:${Math.round(confettiRnd(-30,30))}deg;--tilt:${Math.round(confettiRnd(-25,25))}deg;`+
      `--z:${z.toFixed(2)};--dim:${(.72+(z-.75)/.4*.28).toFixed(2)};--c:${pair[0]};--c2:${pair[1]};`;
    const w = document.createElement("i"); w.className = "w";
    const f = document.createElement("i");
    const shapes = withStars ? CONFETTI_SHAPES : ["rc","rc","ln","ln","sq","sq"];
    f.className = `f ${shapes[Math.floor(Math.random()*shapes.length)]}${flutter ? "" : " tum"}`;
    w.appendChild(f); p.appendChild(w); wrap.appendChild(p);
  }
  host.appendChild(wrap); setTimeout(()=>wrap.remove(), (maxLife+.3)*1000);
}

/* Toolkit answer-feedback pair. Timers belong to the tile so a fast second tap
   cannot let the previous cleanup cut the new animation short. */
function clearAnswerSelectFx(el){
  if(el._answerFxTimers){ el._answerFxTimers.forEach(clearTimeout); }
  el._answerFxTimers = [];
  el.classList.remove("ck-correct","wg-wrong","wg-rel");
  el.querySelectorAll(".ck-fx,.wg-fx").forEach(x=>x.remove());
}
function laterAnswerFx(el, fn, ms){ const t=setTimeout(fn,ms); (el._answerFxTimers||(el._answerFxTimers=[])).push(t); }
function playCorrectSelect(el){
  clearAnswerSelectFx(el); void el.offsetWidth;
  const fx=document.createElement("span"); fx.className="ck-fx";
  const crown=document.createElement("span"); crown.className="ck-crown";
  const w=el.clientWidth||150,h=el.clientHeight||100,rx=w*.46,ry=h*.46;
  for(let i=0;i<5;i++){
    const t=i/4,a=(-158+t*136+confettiRnd(-7,7))*Math.PI/180,out=confettiRnd(.20,.34);
    const s=document.createElement("i"),x0=Math.cos(a)*rx,y0=Math.sin(a)*ry;
    s.style.cssText=`--ss:${confettiRnd(7,12).toFixed(1)}px;--x0:${x0.toFixed(1)}px;--y0:${y0.toFixed(1)}px;`+
      `--sx:${(x0+Math.cos(a)*w*out).toFixed(1)}px;--sy:${(y0+Math.sin(a)*h*out).toFixed(1)}px;--sr:${Math.round(confettiRnd(-140,140))}deg;`;
    crown.appendChild(s);
  }
  fx.appendChild(crown); el.classList.add("ck-correct"); el.appendChild(fx);
  laterAnswerFx(el,()=>crown.remove(),840);
}
function playWrongSelect(el, then){
  clearAnswerSelectFx(el); void el.offsetWidth;
  const fx=document.createElement("span"); fx.className="wg-fx";
  fx.appendChild(document.createElement("i")).className="wg-pulse";
  el.classList.add("wg-wrong"); el.appendChild(fx);
  laterAnswerFx(el,()=>{
    el.classList.add("wg-rel"); el.classList.remove("wg-wrong"); fx.remove();
    laterAnswerFx(el,()=>{ el.classList.remove("wg-rel"); if(then) then(); },260);
  },640);
}
/* ---------- Block Town helpers (flagship) ---------- */
const BT_COLORS = ["#F9695E","#FDC23C","#4EBE6A","#4EA3F0","#9B7BE8"];
function btBlock(i){ const b = document.createElement("div"); b.className = "blk"; b.style.background = BT_COLORS[i % BT_COLORS.length]; return b; }
function btThunk(n){ _tone([360 + n*46], "sine", 0.12, 0.10); }   // pitch climbs one step per block — HEAR the count
function btDust(plot){ const d = document.createElement("span"); d.className = "bt-dust"; d.textContent = "💨"; plot.appendChild(d); setTimeout(()=> d.remove(), 520); }
function btSkyline(done, total){ const s = document.createElement("div"); s.className = "bt-skyline";
  for(let i=0;i<total;i++){ const b = document.createElement("div"); b.className = "bt-bldg" + (i < done ? " done" : "");
    b.style.height = (26 + ((i*17) % 32)) + "px"; s.appendChild(b); } return s; }
/* the teach scene: the crane drops N blocks ONE AT A TIME (ascending thunk + spoken count) then a
   cardinality "freeze" (vo_total_N). Reached from MEET_NUMBER via data.present==='crane'. */
function btCraneMeet(host, slide){
  const d = slide.data, N = d.count;
  state.ownsAudio = true;   // the crane drops+counts blocks on its own timed VO — skip autoPlayChain
  const stage = document.createElement("div"); stage.className = "bt-stage";
  const board = document.createElement("div"); board.className = "bt-board";
  board.innerHTML = `<span class="bt-numeral">${N}</span>` + (d.word ? `<span class="bt-goallbl">${d.word}</span>` : "");   // Arabic numeral (from the integer, not card Devanagari)
  const track = document.createElement("div"); track.className = "bt-track"; const cells = [];
  for(let i=1;i<=N;i++){ const c = document.createElement("div"); c.className = "bt-nt"; track.appendChild(c); cells.push(c); }
  const yard = document.createElement("div"); yard.className = "bt-yard";
  const crane = document.createElement("div"); crane.className = "bt-crane"; crane.innerHTML = `<img src="assets/Images/obj_crane.png" alt="">`;
  const plotwrap = document.createElement("div"); plotwrap.className = "bt-plotwrap";
  const plot = document.createElement("div"); plot.className = "bt-plot ground";
  plot.style.setProperty("--bh", Math.max(20, Math.min(46, Math.floor(230/N) - 2)) + "px");
  plotwrap.appendChild(plot); yard.appendChild(crane); yard.appendChild(plotwrap);
  stage.appendChild(board); stage.appendChild(track); stage.appendChild(yard);
  host.appendChild(stage);
  state.gateNavUntilAudio = false; setNavActive(false);
  $("navBtn").onclick = ()=> completeSlide(true);
  let i = 0;
  const step = ()=>{
    if(i >= N){ if(d.topper){ const t = document.createElement("div"); t.className = "bt-topper snap"; t.innerHTML = `<img src="assets/Images/${d.topper}.png" alt="">`; plot.appendChild(t); }
      burstStars(); play("assets/Audio/vo_total_" + N + "." + AUDIO_EXT, ()=> setNavActive(true)); return; }
    const b = btBlock(i); b.classList.add("drop"); plot.appendChild(b); i++;
    if(cells[i-1]){ cells[i-1].classList.add("lit"); cells[i-1].textContent = i; }
    btThunk(i); btDust(plot);
    play("assets/Audio/vo_num_" + i + "." + AUDIO_EXT, ()=> setTimeout(step, 340));
  };
  // play the slide prompt FIRST, then start the crane count sequence — so the count VO never cuts the
  // prompt off (we own the audio here; mountSlide's autoPlayChain is skipped via state.ownsAudio).
  play(audioFor(slide, "prompt") || null, ()=> setTimeout(step, 400));
}
/* slide audio path: per slide, we look at slide.audio.prompt / .phoneme / etc.
   In this v0.1 the embedded card holds short ids; the compiler would replace
   them with base64 data URIs. We resolve to assets/Audio/{id}.mp3 with fallback. */
function audioFor(slide, key){
  if(!slide.audio || !slide.audio[key]) return null;
  return "assets/Audio/" + slide.audio[key] + "." + AUDIO_EXT;
}
/* audioText(slide,key): the exact Hindi line the VO for this slot speaks, so a
   popup can SHOW what it SAYS (shown == spoken). Looks up the build-injected
   CARD.assets.audio_text map by the slot's audio_id. null if unknown. */
function audioText(slide, key){
  const id = slide.audio && slide.audio[key];
  if(!id) return null;
  return (CARD.assets && CARD.assets.audio_text && CARD.assets.audio_text[id]) || null;
}
/* Play a SEQUENCE of audio sources back-to-back. Each one finishes (or
   falls back to silent beat if missing) before the next starts. */
function playChain(srcs, i, onDone){
  i = i || 0;
  if(i >= srcs.length){ if(onDone) onDone(); return; }
  play(srcs[i], () => playChain(srcs, i+1, onDone));
}
/* On slide mount, play prompt → phoneme/word_name → instruction in order.
   KG learners can't read prompt_hi — the chain gives them both the
   instruction AND the cue (letter sound or picture name) audibly.
   onDone fires after the whole chain finishes (used to gate the नav button). */
function autoPlayChain(slide, onDone){
  const order = ["prompt","phoneme","shape_name","word_name","instruction"];
  const chain = [];
  for(const k of order){
    const src = audioFor(slide, k);
    if(src) chain.push(src);
  }
  if(chain.length) playChain(chain, 0, onDone);
  else if(onDone) onDone();
}

/* nav button: enable/disable the kit-style pill. When it becomes active (the
   activity is done) but the child doesn't tap आगे, the hand-nudge points at it. */
function setNavActive(on){
  state.navRequested = !!on;
  syncNavButton();
  clearTimeout(state.navNudgeTimer);
  /* [20a nudge-03] no auto-nudge on आगे — buttons are known affordances (ruling); nudge is for learning elements only. */
}
function syncNavButton(){
  const btn = $("navBtn"); if(!btn) return;
  const inEligibleSlide = state.navVoEligible && !document.body.classList.contains("is-start") && btn.style.display !== "none";
  const visible = !!state.navRequested || (inEligibleSlide && isPlaying);
  const active = !!state.navRequested && !isPlaying;
  btn.disabled = !active;
  btn.setAttribute("aria-disabled", String(!active));
  btn.classList.toggle("visible", visible);
  btn.classList.toggle("active", active);
}
function nudgeNavBtn(){
  const btn = $("navBtn");
  if(!btn.classList.contains("active") || state.hintActive) return;
  const nh = $("nudgeHand");
  const r = btn.getBoundingClientRect();
  const sw = document.querySelector(".slide-stage").getBoundingClientRect();
  const scale = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--scale")) || 1;
  nh.style.left = ((r.left - sw.left)/scale + r.width/scale/2 - 48) + "px";
  nh.style.top  = ((r.top  - sw.top )/scale + r.height/scale/2 - 6) + "px";
  nh.classList.add("show","hint-glow");
}

/* ---------- 4. STATE ---------- */
const state = {
  idx: 0,
  navRequested: false,
  navVoEligible: false,
  slideStart: Date.now(),
  attempts: 0,
  audioReplays: 0,
  hintUsed: false,
  nudgeUsed: false,
  scaffoldLevel: 0,   // 0 none, 1 nudge, 2 hint, 3 reveal
  selectedKey: null,
  locked: false,
  hintActive: false,
  helpShown: false,   // [25d] terminal-help rung shown for this slide (no auto-answer)
  masteryHits: 0,
  masteryAttempts: 0,
  bubbleRetrySpoken: false,
  fillRetrySpoken: false,
  nudgeTimer: null
};

/* ---------- 5. NUDGE ----------
   target may be a CSS selector OR an element. Used for flow guidance (e.g. the "listen" button /
   prompt). It used to be forbidden to point at the correct answer; as of [27b] there is ONE
   sanctioned exception — a TUTORIAL slide whose answer is already being revealed (the .reveal-hold
   glow after the 2nd wrong attempt) also gets the hand, because at that rung the answer is on
   screen anyway. See revealAnswer() in mountTapOptions. Everywhere else the old rule stands. */
function startNudge(slide, target){
  clearTimeout(state.nudgeTimer);
  if(!target) return;
  /* [28i] THE ROUND-3 HAND BAN IS ENFORCED HERE, NOT LEFT TO CARD DATA.
     This is why Yasir's "no hand nudge in the 3rd round" kept coming back after I kept reporting it
     fixed. 28f closed the answer/tap paths (handOnAnswer + HAND_PHASES), but the drag/count PROGRESS
     cue arrives through here, and the only round-3 guard was the card's own
     scaffold_rules.nudge_timeout_ms[phase] — which 22 of 27 games set to `independent: 8000`
     (two also set practice). So on a drag or count slide in round 3, 8s of hesitation still produced
     a hand. Card data cannot be the guard for a hard rule; the engine refuses now, and a card that
     still arms round 3 is simply ignored rather than silently obeyed. */
  /* IDLE is stricter than TERMINAL HELP. handOnAnswer() allows guided, because there the hand is
     EARNED by two failed attempts. This path is the un-earned one — armed by a timer at mount — and
     Yasir's rule covers it exactly: "any form of visual hint will only be given after 2 failed
     attempts", and separately "in guided, a hand nudge appears right after VO is played but the hand
     nudge should appear only after 2 failed attempts". So the idle/progress hand lives in TUTORIAL
     only, where it is teaching rather than hinting. Round 2 keeps its hand via terminal help; round 3
     has none by either route. */
  if(!IDLE_HAND_PHASES.has(slide.phase)) return;
  const ms = (CARD.scaffold_rules.nudge_timeout_ms || {})[slide.phase];
  if(!ms) return;
  state.nudgeTimer = setTimeout(()=>{
    // [27e] ...and never once TERMINAL HELP owns the hand. The flow nudge is armed at mount, so at
    // guided (5000ms) it fired AFTER a 2-wrong reveal and re-pointed the hand away from the glowing
    // answer to the flow target — the hand was visible but pointing at nothing useful. Caught by
    // measuring the hand's rect against the correct cell's; `handShown:true` alone hid the bug, and
    // it silently affected the 27b tutorial hand too.
    if(state.locked || state.hintActive || state.helpShown) return;
    const el = (typeof target === "string") ? document.querySelector(target) : target;
    if(!el) return;
    /* [28i] ONE POSITIONING RULE, ONE COPY OF IT. This function carried its own duplicate of the old
       formula (top = elementBottom - 30), so the 28h "hand sits BELOW the tile, never on its word" fix
       landed in pointNudgeAt and silently did NOT apply to any progress cue — the same fingertip-over-
       the-label bug, still live on every drag and count tile. Delegated instead of re-implemented, so
       the next placement change cannot miss one of the two call paths again. */
    pointNudgeAt(el);
    state.nudgeUsed = true;
    state.scaffoldLevel = Math.max(state.scaffoldLevel, 1);
    GameBus.emit("nudge_invoked", { slide_id: slide.id, phase: slide.phase });
  }, ms);
}
function stopNudge(){
  clearTimeout(state.nudgeTimer);
  if(state._handTravel){ try { state._handTravel.cancel(); } catch(e){} state._handTravel = null; }
  $("nudgeHand").classList.remove("show");
}
/* [28o] ON A DRAG, THE HAND SHOWS THE MOVE — it does not just sit on the tile.
   Yasir 2026-07-28: "on drag, the hand nudge guides the student precisely... move the hand nudge from
   the question card to the answer card." A static hand on the tile says "this one" but never says WHERE
   it goes, which on a matching slide is the actual thing the child has to work out. The hand now starts
   on the tile and slides to the correct zone, on a loop, so the gesture itself is demonstrated.
   Positions are computed in DESIGN px against .slide-stage, exactly like pointNudgeAt, so it survives
   --scale. Kept as ONE WAAPI animation stored on state so stopNudge can cancel it — an infinite
   animation left running would follow the child into the next slide. Falls back to a static point if
   either element is missing or the browser has no .animate(). */
function travelNudge(fromEl, toEl, slide){
  if(!fromEl) return;
  if(!toEl || typeof $("nudgeHand").animate !== "function"){ handOnAnswer(fromEl, slide); return; }
  if(!slide || !HAND_PHASES.has(slide.phase)) return;      // same phase rule as handOnAnswer
  stopNudge();
  const nh = $("nudgeHand");
  const sw = document.querySelector(".slide-stage").getBoundingClientRect();
  const scale = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--scale")) || 1;
  const at = (el)=>{ const r = el.getBoundingClientRect();
    return { left: (r.left - sw.left)/scale + r.width/scale/2 - 48,
             top:  (r.top  - sw.top )/scale + r.height/scale + 4 }; };
  const a = at(fromEl), b = at(toEl);
  nh.style.left = a.left + "px"; nh.style.top = a.top + "px";
  nh.classList.add("show","hint-glow");
  state._handTravel = nh.animate(
    [ { left: a.left+"px", top: a.top+"px", offset: 0 },
      { left: a.left+"px", top: a.top+"px", offset: .18 },
      { left: b.left+"px", top: b.top+"px", offset: .72 },
      { left: b.left+"px", top: b.top+"px", offset: 1 } ],
    { duration: 1800, iterations: Infinity, easing: "ease-in-out" });
}
/* [28i] THE GRADED WRONG-ANSWER CLIP, for mechanics that grade their own feedback.
   Yasir's 2026-07-25 ruling is "two hints everywhere, every game, every interaction type". The tap path
   got it in 24a (mountTapOptions) and the drag path in 25a (dragWrong), but the PRODUCE mechanics grade
   their own wrong answers and so inherited neither: MAKE_SET played try_again on rung 1, MAKE_EQUAL had
   no ladder at all, TAP_ALL_WITH_SOUND played only try_again, and BUILD_TO_NUMBER passed `null` — its
   wrong-answer feedback was SILENT, text-only, to a pre-reader who cannot read it.
   Callers increment state.attempts BEFORE speaking, so attempts===1 is the first wrong. Additive: with
   no hint1/hint authored this returns exactly the try_again it returned before, so no card regresses —
   but check_system will now stop reporting these six games' authored hints as unreadable. */
/* [28k] OPTIONAL MIDDLE RUNG — the SME's three-hint ladder (Pehli Dhwani, Bindu 2026-07-28):
     rung 1  "फिर से कोशिश कीजिए।"                           (try again)
     rung 2  "शब्द को बोलकर देखिए, और पहली ध्वनि चुनिए।"       (a STRATEGY, not the answer)
     rung 3  the correct answer
   Our ladder had only two rungs, so rung 2 spoke `hint` — the level that NAMES the answer. A middle
   rung lets a card withhold the answer for one more attempt.
   ADDITIVE AND DECK-SCOPED: with no `hint2` authored this returns exactly the `hint` it returned
   before, so every other game keeps two rungs and Yasir's 2-attempt standard. Only a card that
   authors hint2 AND raises max_attempts to 3 gets a third rung — a deliberate deck-specific override,
   ruled by Yasir 2026-07-28 ("implement as per written by the SME") after the conflict with "blocks
   after the 2nd wrong attempt" was raised with him. Do NOT roll this out fleet-wide without the same
   explicit ask on that deck. */
function midHint(slide){
  return audioFor(slide, "hint2") || audioFor(slide, "hint") || audioFor(slide, "try_again") || null;
}
function wrongClip(slide){
  return (state.attempts <= 1)
    ? (audioFor(slide, "hint1") || audioFor(slide, "try_again") || null)
    : (midHint(slide));                                     /* [28k] rung 2 */
}
/* Show the hand-nudge immediately on a specific element (INTRO uses it to guide
   tapping each letter). Finger points up; fingertip sits just inside the tile's
   lower edge. References .slide-stage (the nudge's positioning context). */
/* [28f] THE ONE RULE FOR THE GUIDING HAND (Yasir 2026-07-28, two rulings merged):
     round 1 tutorial  -> hand allowed (it is teaching)
     round 2 guided    -> hand ONLY after 2 failed attempts (terminal help), never on idle
     round 3 practice / independent / mastery -> NO HAND AT ALL, "regardless of whatever name we
                          save it by"
   Every terminal-help path calls THIS, so the rule lives in one place. That matters: 27d put the hand
   in one of five paths and I reported it as "every phase", which is exactly how this drifted. Any new
   mechanic gets the rule for free by calling handOnAnswer() instead of pointNudgeAt().
   Also note the hand was COVERING the option label in Yasir's capture — another reason round 3 is
   better off without it. */
/* [28l] HARD RULE (Yasir 2026-07-28): "regardless of what interaction, as long as we in guided or
   practice, no question will be solved automatically."
   Only a TUTORIAL slide may finish a question by itself — there it is a teaching demonstration. In every
   test phase the terminal rung must GLOW the answer, DISABLE the other candidates, put the hand on it
   (handOnAnswer is itself phase-gated, so round 3 still gets no hand) and WAIT for the child.
   This existed per-mechanic and drifted three times: 25d fixed MATCH_DRAG_N and SENTENCE_FIND, and left
   PATTERN_BUILD and SEQUENCE_COMPLETE still calling placeCorrect() on a 1s timer — the engine filling in
   the answer. MATCH_GENDER_PAIRS and SEQUENCE_DRAG held the glow but never dimmed the distractors or
   showed the hand. One contract in one place so a new mechanic inherits it instead of re-deciding. */
const MAY_AUTOSOLVE = new Set(["tutorial"]);
function maySolveFor(slide){ return !!slide && MAY_AUTOSOLVE.has(slide.phase); }
function terminalHold(target, others, slide, dest){
  if(!target) return;
  target.classList.add("reveal-hold");
  [...(others || [])].forEach(x=>{
    if(x !== target && !x.classList.contains("used") && !x.classList.contains("snapped")
       && !x.classList.contains("matched")){
      x.classList.add("tile-disabled");
      x.style.setProperty("pointer-events","none","important");
      x.style.setProperty("opacity",".4","important");
    }
  });
  /* [28o] on a DRAG the caller passes the destination zone, so the hand demonstrates the move
     (tile -> its correct zone) instead of only naming the tile. Tap mechanics pass no dest and keep
     the static point. */
  if(dest) travelNudge(target, dest, slide); else handOnAnswer(target, slide);
}
function clearHold(container){
  if(!container) return;
  [...container.children].forEach(x=>{
    x.classList.remove("reveal-hold","tile-disabled");
    x.style.removeProperty("pointer-events"); x.style.removeProperty("opacity");
  });
}
const HAND_PHASES = new Set(["tutorial", "guided"]);
/* [28i] the UN-EARNED hand (idle timer / progress cue) is tutorial-only — see startNudge. */
const IDLE_HAND_PHASES = new Set(["tutorial"]);
function handOnAnswer(el, slide){
  if(!el || !slide || !HAND_PHASES.has(slide.phase)) return;
  stopNudge();          // the flow nudge must not drag the hand off the answer
  pointNudgeAt(el, true);   // earned by 2 failed attempts — the one case allowed outside tutorial
}
function pointNudgeAt(el, earned){
  if(!el) return;
  /* [28j] THE PHASE RULE LIVES HERE, because this is the only function that can enforce it.
     I gated startNudge (28i) and handOnAnswer (28f) and Yasir STILL found a hand in round 3 — on
     MTKGA01_L04_S01 P5, a COUNT_TAP practice slide. Reason: ~25 call sites call pointNudgeAt DIRECTLY,
     and every one of them bypassed both gates. COUNT_TAP's nudgeNext is the clearest case: the slide is
     child-driven in round 3, nothing is being demonstrated, and the hand points at the very object the
     child is meant to find. Gating each call site is what produced three rounds of "fixed" that were
     not; the rule has to sit at the single choke point instead.
     Default is TUTORIAL ONLY — so every existing raw call site (demo chains, progress cues, count
     nudges) becomes correct by construction, and any future mechanic inherits the rule for free.
     `earned` is the one opt-in: handOnAnswer passes it for terminal help, which Yasir does allow in
     guided because two failed attempts paid for it. Round 3 gets no hand by ANY route. */
  const _ph = (CARD.slides[state.idx] || {}).phase;
  if(!(earned ? HAND_PHASES : IDLE_HAND_PHASES).has(_ph)) return;
  const nh = $("nudgeHand");
  /* Placement is computed TWICE: now, and once more on the next frame. Measuring text rects only helps
     if the text has stopped moving, and a teach slide places the hand while its card is still animating
     in — GENDER_INTRO T3 measured 0% coverage on the first sample and 17% on the next, as .cat-word
     settled underneath an already-positioned hand. One rAF re-place costs nothing and makes the
     measurement match what the child actually sees. */
  requestAnimationFrame(()=>{ if(nh.classList.contains("show")) _placeNudge(el, nh); });
  _placeNudge(el, nh);
  nh.classList.add("show","hint-glow");
}
function _placeNudge(el, nh){
  if(!el || !el.getBoundingClientRect) return;
  const r = el.getBoundingClientRect();
  const sw = document.querySelector(".slide-stage").getBoundingClientRect();
  const scale = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--scale")) || 1;
  nh.style.left = ((r.left - sw.left)/scale + r.width/scale/2 - 48) + "px";
  /* [28h] THE HAND SITS BELOW THE TILE, NEVER ON ITS WORD.
     Yasir 2026-07-28: "hand nudge is overlapping the word, so the hand nudge is to be placed lower."
     The old line put the fingertip 56 design-px INSIDE the bottom edge — fine for a bare picture tile
     (the original caller), fatal once handOnAnswer() started pointing at .opt-cell, whose bottom strip
     IS the label. Measured on HI01H01_L02_S05 P1: hand 859-951 x 576-668 vs label 852-958 x 587-614,
     i.e. the hand covered 92 of the label's 106px width and ALL of its height — the child was shown
     the answer with the answer hidden under a hand.
     Now the hand's top starts just past the tile's bottom edge, so it can never cover tile content
     whatever the tile is. Clamped: if that would push it off the bottom of the stage, it goes ABOVE
     the tile instead (still adjacent, still unambiguous) rather than being silently clipped away. */
  /* [28j] PLACEMENT, corrected twice over. 28h moved the hand below the tile and introduced two new
     failures, both measured on real builds:
       (a) EMPTY SKY. The "flip above if it would run off the stage" clamp put the hand 100-395px ABOVE
           a tall TAP_IN_SCENE hotspot (a whole standing figure), i.e. in open sky pointing at nothing,
           on 4 of 6 guided slides of HI01H07_L01_S02. Flipping is wrong for this hand: it points UP,
           so above the target it points away from it. Clamp INSIDE the stage instead — at worst it
           overlaps the target's lower edge, which is where it used to live and is still unambiguous.
       (b) A LABEL BELOW THE ANCHOR. Anchoring to the bottom of the element PASSED IN only helps when
           that element contains the text. GENDER_INTRO passes the cat IMAGE while .cat-word sits below
           it inside the card, so "below the image" landed straight on the word — 56% covered on T3
           (better than 28h's 100%, still wrong). Assuming the anchor encloses the label is what made
           this a per-mechanic whack-a-mole, so instead of anchoring smarter we MEASURE: find real text
           rects near the landing spot and drop below the lowest one. That works for any mechanic,
           including ones not written yet. */
  const HAND_H = 96, GAP = 4, stageH = sw.height/scale;
  const top = (r.top - sw.top)/scale, h = r.height/scale;
  let below = top + h + GAP;
  // Push past any TEXT that sits below the anchor but shares its horizontal span (the label case).
  const _tile = el.closest(".opt-cell, .gender-cat, .sentence-word, .tut-card, .q-cell, .ms-item") || el.parentElement;
  if(_tile){
    _tile.querySelectorAll(".lbl, .cat-word, .sw-text, .opt-label, .story-q-opt-label, .pic-label, .count-badge")
      .forEach(t => {
        const tr = t.getBoundingClientRect();
        if(tr.width < 2 || tr.height < 2) return;
        if(tr.right < r.left || tr.left > r.right) return;      // not in this column — ignore
        const tb = (tr.bottom - sw.top)/scale;
        if(tb > below - HAND_H && tb + GAP > below) below = tb + GAP;   // clear it
      });
  }
  // Never off-stage, and never flipped above (see (a)) — clamp into the stage as a last resort.
  if(below + HAND_H > stageH) below = Math.max(0, stageH - HAND_H);
  nh.style.top = below + "px";
}

/* ---------- 6. IDLE VO REPLAY [27b] ----------
   Yasir 2026-07-27: "in guided and practice, when no interaction, make the vo play again at exactly
   after 7 seconds of no interaction." A child who stalls hears the question again instead of sitting
   in silence. Distinct from the hand-nudge above (that POINTS, this SPEAKS) and from the manual
   replay chip — same guards as the chip, but fired by inactivity rather than a tap.

   SCOPE = EVERY test phase (27d, Yasir 2026-07-27: the 7s replay "needs to be all uniform and done
   and perfected" for the 50-game batch). Was guided+practice only, which silently skipped
   `independent` and `mastery` — Antim's I1/I2 + M1-M3 had no idle replay while its G/P slides did.
   Inconsistency across a 50-game fleet is worse than either behaviour, so all four test phases now
   behave identically. `tutorial` stays excluded on purpose: teaching slides either self-play
   (data.auto) or gate on the child tapping through, so an idle timer there would talk over the
   lesson. CELEBRATION is excluded by type: it expects no interaction and self-narrates.

   FIRES EXACTLY ONCE PER SLIDE (27f, Yasir 2026-07-27: "it only needs to be repeated once ... once
   the audio is played after 7 second, no need to be replayed after that"). The first cut re-armed
   after every fire, so a child — or an unattended tab — heard the prompt again every 7s forever;
   he caught it as sound coming from a test tab I had left open. One reminder, then silence.
   A correct answer (state.locked) holds it, and the slide teardown clears it, so a timer can never
   leak across slides. 7000ms is the default, overridable per card via
   scaffold_rules.idle_vo_replay_ms. */
const IDLE_VO_PHASES = new Set(["guided", "independent", "practice", "mastery"]);
// 100ms tick so the fire lands within 0.1s of the target (a 500ms tick measured 7.1-8.0s in-browser,
// and he asked for EXACTLY 7s). Cost is 10 boolean checks/sec on test slides only.
const IDLE_VO_TICK = 100;
let _idleVoTimer = null, _idleSince = 0, _idleVoFired = false;
function stopIdleVo(){ clearInterval(_idleVoTimer); _idleVoTimer = null; _idleSince = 0; }
/* Called by mountSlide so the ONE allowed reminder is per SLIDE, not per lesson. Kept separate from
   stopIdleVo() on purpose: stopIdleVo is also called for transient reasons (wrong phase, teardown)
   and must NOT hand a slide a second reminder. */
function resetIdleVo(){ stopIdleVo(); _idleVoFired = false; }
/* The 7s is 7s of SILENCE AND no touching — the clock only runs while the game is quiet, so the
   replay lands 7s after the prompt stops, never on top of it. (First cut used a plain 7s setTimeout
   that re-armed a FULL 7s whenever it found audio playing, which stretched the real delay to as much
   as 14s — measured in-browser, it never fired. A ticker that resets the silence clock is exact.) */
function armIdleVo(){
  if(['MATCH_THE_PAIR','MATCH_VACHAN_PAIRS','FILL_VACHAN_DRAG'].includes(CARD.slides[state.idx]?.type)){stopIdleVo();return;}
  if(_idleVoFired){ stopIdleVo(); return; }      // [27f] one reminder per slide — already spent
  _idleSince = 0;                                // any (re)arm restarts the silence clock
  const slide = CARD.slides[state.idx];
  if(!slide || slide.type === "CELEBRATION" || !IDLE_VO_PHASES.has(slide.phase)){ stopIdleVo(); return; }
  if(_idleVoTimer) return;                       // ticker already running for this slide
  const ms = (CARD.scaffold_rules && CARD.scaffold_rules.idle_vo_replay_ms) || 7000;
  _idleVoTimer = setInterval(()=>{
    const s = CARD.slides[state.idx];
    if(!s || s.type === "CELEBRATION" || !IDLE_VO_PHASES.has(s.phase)){ stopIdleVo(); return; }
    // HOLD (not stop) on every transient busy flag. state.locked MUST be a hold: besides "answered
    // correctly" it is also set TRANSIENTLY while reveal_seq narrates the options one by one (see the
    // _enableAll() that clears it). Treating it as terminal killed the ticker 0.6s into every guided
    // slide — measured in-browser, which is the only way this was visible. Slide teardown is what
    // really ends the watch, and after a correct answer the hold simply means nothing more is spoken.
    if(state.locked || state.hintActive || isPlaying || state.revealing || state.demoRunning){ _idleSince = 0; return; }
    if(!_idleSince){ _idleSince = Date.now(); return; }
    if(Date.now() - _idleSince < ms) return;
    // [27f] ONE reminder, then done for this slide. Mark spent and stop the ticker BEFORE speaking,
    // so a pointerdown arriving during the replay cannot re-arm it.
    _idleVoFired = true;
    stopIdleVo();
    GameBus.emit("idle_vo_replay", { slide_id: s.id, phase: s.phase });
    if(state.replayAudio) state.replayAudio(); else autoPlayChain(s);
  }, IDLE_VO_TICK);
}
// ONE document-level listener for the whole session (a per-slide listener would pile up across the
// drag slides — the same trap the drag mechanics warn about). armIdleVo() itself re-checks phase, so
// a pointerdown on a tutorial slide is a cheap no-op.
document.addEventListener("pointerdown", ()=>{ armIdleVo(); }, true);

/* [B2] ANDROID WEBVIEW PINCH-ZOOM LOCK. The viewport meta in <head> carries user-scalable=no +
   maximum-scale=1, but Chrome/Android WebView DELIBERATELY IGNORES BOTH (accessibility policy,
   Chrome 48+), so on the actual target device nothing stopped a two-finger pinch — the reported
   "html getting zoomed in and out". touch-action:manipulation on html,body already kills DOUBLE-TAP
   zoom; this closes the pinch path. A touch sequence carrying 2+ points is never ours, so swallow
   it in the capture phase, before any mechanic's handler. Single-finger sequences (length === 1)
   fall straight through, so every drag, tap and trace still behaves exactly as before. */
try{
  const _killMultiTouch = (e)=>{ if(e.touches && e.touches.length > 1) e.preventDefault(); };
  document.addEventListener("touchstart", _killMultiTouch, {passive:false, capture:true});
  document.addEventListener("touchmove",  _killMultiTouch, {passive:false, capture:true});
  document.addEventListener("gesturestart",  (e)=> e.preventDefault(), {passive:false});   // iOS/WebKit only — Android never fires these
  document.addEventListener("gesturechange", (e)=> e.preventDefault(), {passive:false});
  document.addEventListener("gestureend",    (e)=> e.preventDefault(), {passive:false});
  document.addEventListener("wheel", (e)=>{ if(e.ctrlKey) e.preventDefault(); }, {passive:false});   // desktop/trackpad ctrl+wheel zoom
}catch(_){}

/* ---------- 7. HINT / FEEDBACK BOX ----------
   No button: the popup plays its VO, then auto-dismisses. onEnd runs after it
   closes (callers add a short pause there so the revealed answer shows). */
function showBox(emoji, text, theme, audioSrc, onEnd){
  { const hb=document.getElementById("hintBtn"); if(hb) hb.classList.remove("hint-glow"); }
  // CORRECT: no popup (lead review) — confetti cannons from both sides + Swiftie cheer, then onEnd.
  if(theme === "correct"){
    sfxCorrect(); confettiCannon(); setSwMood("celebrate");
    play(audioSrc || null, ()=> setTimeout(()=>{ if(onEnd) onEnd(); }, 300));
    return;
  }
  state.hintActive = true;
  // wrong/hint/reveal keep a light card (mechanics use it for a short cue); Swiftie reacts too.
  // one-Swiftie rule: the popup shows the reacting Swiftie (animated), so HIDE the header buddy
  // while it's open — never two Swifties on screen at once (MoM flag).
  const swMap = { wrong:"sw_lg_hint_anim", hint:"sw_lg_hint_anim", reveal:"sw_lg_hint_anim" };  // [20a mascot-11] overlay mascot: retired non-existent sw_anim_*.gif → production's shipped sw_lg_hint_anim.webp
  const sw = $("hintMascot");
  if(sw){ sw.style.display=""; sw.src = "assets/UI/" + (swMap[theme] || "sw_lg_hint_anim") + ".webp"; }
  const buddy = $("swBuddy"); if(buddy) buddy.style.visibility = "hidden";
  setSwMood(theme === "wrong" ? "tryagain" : "hint");
  $("hintBox").classList.remove("celebrate");
  sfxWrongSoft();
  const ht = $("hintText"); ht.textContent = text; ht.className = "hint-text " + theme;
  $("stage").classList.add("blurred");
  $("hintOverlay").classList.add("show","hint-glow");
  $("hintBtn").disabled = true;
  const hi = $("hintImg"); if(hi) hi.src = "assets/UI/hint_active.png";
  const close = ()=>{
    $("hintOverlay").classList.remove("show");
    $("stage").classList.remove("blurred");
    if(buddy) buddy.style.visibility = "";   // header Swiftie returns when the popup closes
    state.hintActive = false;
    if(hi) hi.src = "assets/UI/hint.png";
    if(!state.locked) $("hintBtn").disabled = false;
    if(onEnd) onEnd();
  };
  // auto-dismiss after the VO finishes (small buffer so it never just flashes); freeze the popup
  // Swiftie's mouth to the still frame the instant its line ends
  play(audioSrc, ()=>{ if(sw) sw.src = "assets/UI/sw_head_talking.webp"; setTimeout(close, 300); });
}

/* ---------- 8. TAP-OPTION HELPER (shared by 5 slide types) ---------- */
function mountTapOptions({slide, host, signalName, stimulus, options, isCorrect, optionRenderer, columnsHint, mastery, hintAction, nudgeTarget, shuffle}){
  state.attempts = 0; state.selectedKey = null; state.locked = false;
  state.audioReplays = 0; state.hintUsed = false; state.nudgeUsed = false; state.scaffoldLevel = 0; state.helpShown = false;
  // idle hand-nudge target: defaults to the stimulus (re-listen), but a slide can pass
  // nudgeTarget:null to suppress it entirely (e.g. "how many?" — nothing to re-tap).
  const _nudge = (nudgeTarget !== undefined) ? nudgeTarget : (stimulus || null);
  // optional custom hint (runs on the live slide instead of a text popup), e.g. a
  // count-demonstration. Wrapped to block option taps while it plays.
  const runHint = hintAction ? (after)=>{ state.hintActive = true; hintAction(()=>{ state.hintActive = false; if(after) after(); }); } : null;

  // Shuffle options once so the correct answer isn't pinned to one position (engine-wide anti
  // positional-bias — otherwise "always tap the same spot" can pass mastery). Opt out with
  // shuffle:false for inherently-ordered options (e.g. a number line).
  const _opts = (shuffle === false) ? options.slice()
    : (function(a){ a = a.slice(); for(let i=a.length-1;i>0;i--){ const j=(Math.random()*(i+1))|0; [a[i],a[j]]=[a[j],a[i]]; } return a; })(options);

  const wrap = document.createElement("div"); wrap.className = "q-row";
  if(stimulus){ wrap.appendChild(stimulus); }
  const grid = document.createElement("div");
  const cols = columnsHint || (_opts.length <= 2 ? 2 : _opts.length <= 3 ? 3 : 4);
  grid.className = "opt-grid cols-" + cols;
  // [24a A2] TAP GATE (fork-proven, gender #53+#56): one tap at a time — the tapped word must END
  // before the next tap counts (_busy, 4s _vb fail-safe so a superseded onEnd can't soft-lock), AND
  // taps are ignored while ANY VO sounds (prompt / feedback / idle-replay) — silent-VO spam-tap fix.
  let _busy = false;
  /* [28t] A TAP DURING FEEDBACK AUDIO MUST COUNT, NOT VANISH. The gate below ignores taps while ANY VO
     sounds — added in 24a to stop spam-tapping during the PROMPT, which is right. But the hint clip after
     a wrong answer is also "VO sounds", so a child who taps again while hint1 is still speaking had that
     attempt SILENTLY DISCARDED: they tapped twice, the engine counted once, and terminal help never
     arrived. That defeats the whole 2-attempt ladder through a side door.
     `_fb` marks feedback audio specifically. During it a tap is accepted and interrupts the clip (one
     voice at a time is preserved by stopAudio); during the prompt, taps are still ignored. */
  let _fb = false;
  _opts.forEach((opt, i) => {
    const cell = optionRenderer(opt, i);
    cell.classList.add("opt-cell");
    cell.dataset.key = String(i);
    cell.onclick = ()=>{
      if(state.locked || state.hintActive || _busy || (isPlaying && !_fb) || cell.classList.contains("crossed") || cell.classList.contains("correct") || cell.classList.contains("faded")) return;   /* [25d] .faded = an option disabled by terminal help; refuse it in JS too */
      stopNudge();
      if(_fb){ stopAudio(); _fb = false; }   /* [28t] a retry interrupts the hint — never two voices */
      // SME rule: SPEAK THE TAPPED WORD on EVERY tap (right or wrong), then the feedback — never two
      // voices at once (buzz/confetti are sfx, they ride alongside the word). opt.audio = word clip id.
      // Fallback wiring for LETTER options (SME: the tapped item's own sound speaks EVERYWHERE): options
      // authored as {letter:"आ"} carry no audio id, but the slide's data.phonemes map has each letter's
      // clip — derive it here centrally so every TAP_LETTER_* / mastery module inherits speak-on-tap
      // without per-module or per-card changes. Explicit opt.audio always wins.
      const _aid = opt.audio ||
                   (opt.letter && slide.data && slide.data.phonemes && slide.data.phonemes[opt.letter]) || null;
      const _word = _aid ? ("assets/Audio/" + _aid + "." + AUDIO_EXT) : null;
      // [24a A2] _busy covers the word-speak beat; the 4s _vb fail-safe clears the gate even if the
      // word's onEnd is superseded (e.g. the volume chip tapped mid-word) — gender #53 soft-lock fix.
      _busy = true;
      const _vb = setTimeout(()=>{ _busy = false; }, 4000);
      const _afterWord = (cb)=>{ const done = ()=>{ clearTimeout(_vb); _busy = false; cb(); };
        if(_word) play(_word, done); else done(); };
      if(isCorrect(opt, i)){
        state.locked = true; cell.classList.add("correct"); playCorrectSelect(cell); sfxCorrect(); confettiCannon(); setSwMood("happy");
        if(mastery){ state.masteryAttempts++; if(state.attempts === 0) state.masteryHits++; }
        GameBus.emit(signalName, { slide_id: slide.id, phase: slide.phase, value: true,
          first_try: state.attempts === 0, attempts: state.attempts + 1,
          scaffold_level: state.scaffoldLevel, latency_ms: Date.now()-state.slideStart });
        /* [spec] question_answered (correct). ui_index = position shown AFTER shuffle (_opts order);
           original_index = position authored in the card (options order). score is 1 only first-try. */
        GameBus.sendQuestionAnswered(slide, { is_correct: true, score: state.attempts === 0 ? 1 : 0, attempt: state.attempts + 1,
          ui_index: i, original_index: options.indexOf(opt),
          text: opt.label_hi || opt.word_hi || opt.name_hi || opt.letter || opt.key || null,
          mediaUrl: opt.img ? ((CARD.assets && CARD.assets.image && CARD.assets.image[opt.img]) || ("assets/Images/" + opt.img + "." + IMG_EXT)) : null });
        /* [27j] SPEAK audio.correct AFTER the tapped word. It was never read here: the correct branch
           only spoke the option's own word and went straight to completeSlide, so an SME's
           per-question correct feedback ("शाबाश! रवि ने सुबह दूध पिया।") was silent on every
           STORY_QUESTION — 12 slides across 2 games. It cannot be folded into the option's own audio
           because those slides use data.reveal_seq. TAP_IN_SCENE already played this id, which is why
           the ids are authored and valid, just unread. A card with no `correct` id behaves exactly as
           before (play(null) is a silent beat), so this is additive. */
        _afterWord(()=> play(audioFor(slide, "correct") || null,
                            ()=> setTimeout(()=> completeSlide(true), 700)));
      } else {
        state.attempts++; sfxWrongSoft(); setSwMood("tryagain");
        /* [28p] 1st WRONG = A RED FLASH ON A STILL-LIVE CARD. 2nd = GREY AND DISABLED.
           Yasir 2026-07-28: "1st wrong must flash a RED GLOW on a still-live card; disabling/greying
           belongs ONLY at 2 wrong attempts. Today it is the opposite." He is right, and it was my own
           28e over-correction: 28e ruled that a DISABLED option is never red, but implemented it on
           `.crossed`, which is the class used for BOTH states — so it also bleached the momentary
           first-wrong feedback and left a ~700ms grey disable with no red anywhere.
           Two classes now, one per meaning: `.wrong-flash` is the transient red buzz and keeps the card
           TAPPABLE (nothing is being taken away on a first miss), `.crossed` stays the grey permanent
           lock from the 2nd attempt. 28e's ruling is preserved exactly — red never rests on a disabled
           card — while red returns to the one place it belongs. */
        /* [28r] BOTH wrong attempts flash RED FIRST. Yasir 2026-07-28: "on second wrong attempt as
           well we are supposed to give the red glow first and then disable." The red IS the "that is
           not it" feedback, so it belongs on every wrong tap; the grey lock is an EXTRA consequence
           that only the 2nd earns. 28p gave the 2nd wrong the grey lock with no red at all, so the
           child lost the feedback exactly when they most needed it. Sequence now: red buzz -> (2nd
           only) settle to the grey disabled state. */
        cell.classList.add("wrong-flash");
        // [27a] RETRYABLE WRONG TAP (Yasir ruling 2026-07-27 — resolves the blocked behavioural
        // ruling (a) in _ENGINE_GAPS_CONFIRMED_2026-07-27.md, and matches the blessed strilling
        // fork): a wrong card must NOT lock on the first miss. It buzzes red, then UNBLOCKS so the
        // child can try that same card again — "they should only be blocked after 2nd wrong
        // attempt ... just disable the button after 2nd wrong attempt". From attempt 2 onward the
        // .crossed lock stays, so a single card cannot burn every attempt. Ships with the CSS half
        // (the ✕ ::after is gone from .opt-cell.crossed) — without it the giant ✕ would flash and
        // vanish, which the gaps doc flags as worse than either end state.
        /* [28d] THE UNBLOCK MUST NOT DEPEND ON state.locked. Yasir calls the stuck red ring "a
           constantly repeated issue", and this guard is why: state.locked is NOT only "answered
           correctly" — it is also set TRANSIENTLY while reveal_seq narrates the options (see the
           _enableAll() that clears it). If the 700ms landed inside that window the removal was
           SKIPPED, so .crossed stayed forever: a permanent red ring on a permanently dead card.
           I found that same state.locked trap later while fixing the idle-VO ticker and wrote it
           down there, but never propagated it back here — and I had SEEN the red persist in testing
           and wrongly explained it away as a frozen-timeline artifact.
           Now it keys off THIS cell only: it is still crossed, was never answered correctly, and
           terminal help has not taken over. Nothing shared, nothing transient. */
        playWrongSelect(cell, ()=>{
          if(cell.classList.contains("correct")) return;   // this cell ended up being the answer
          /* [28s] NO state.helpShown EARLY-RETURN HERE. That guard exists to stop the old code UNBLOCKING
             a card once terminal help owns the board — but this timer no longer unblocks, it swaps the RED
             FLASH for the GREY LOCK. At the 2nd wrong, terminal help fires in the same beat, so helpShown
             was already true and the swap was skipped: the card stayed RED FOREVER. That is the exact
             stuck-red-ring failure I fixed in 28d and reintroduced in a new form 700ms later. Removing the
             flash and applying the lock is correct whether or not terminal help is up — a wrong card should
             read the same as the distractors terminal help fades. */
          cell.classList.remove("wrong-flash");
          if(state.attempts >= 2) cell.classList.add("crossed");
        });
        // (do NOT count masteryAttempts here — the correct branch counts one attempt PER ITEM.)
        GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
        /* [spec] question_answered (wrong) — the spec wants EVERY answer tap reported, right or wrong. */
        GameBus.sendQuestionAnswered(slide, { is_correct: false, score: 0, attempt: state.attempts,
          ui_index: i, original_index: options.indexOf(opt),
          text: opt.label_hi || opt.word_hi || opt.name_hi || opt.letter || opt.key || null,
          mediaUrl: opt.img ? ((CARD.assets && CARD.assets.image && CARD.assets.image[opt.img]) || ("assets/Images/" + opt.img + "." + IMG_EXT)) : null });
        // LAYERED SCAFFOLD (A1): L1 re-listen → L2 hint → L3 REVEAL at max_attempts (never stuck).
        const _maxA = (CARD.scaffold_rules && CARD.scaffold_rules.max_attempts) || 3;
        $("hintBtn").classList.add("show","hint-glow");
        _afterWord(()=>{   // speak the tapped word FIRST, then the layered feedback VO (no overlap)
          _fb = true;                        /* [28t] from here the audio is FEEDBACK — a retry may interrupt it */
          if(state.attempts >= _maxA){ revealAnswer("wrong"); _fb = false; }
          else if(state.attempts >= 2){ state.scaffoldLevel = Math.max(state.scaffoldLevel, 2);
            if(runHint) runHint(); else play(midHint(slide), ()=>{ _fb = false; }); }   /* [28k] rung 2 */
          // [24a A2] 1st wrong: the slide's OWN hint1 clip when authored ("यह … नहीं है…"), else the
          // generic try_again — additive, cards without hint1 are byte-for-byte unchanged.
          else { state.scaffoldLevel = Math.max(state.scaffoldLevel, 1); play(audioFor(slide, "hint1") || audioFor(slide, "try_again") || null, ()=>{ _fb = false; }); }
        });
      }
    };
    grid.appendChild(cell);
  });
  wrap.appendChild(grid);
  host.appendChild(wrap);

  // ---- layered-hint helpers (A1/B2): reveal-on-max + a wired manual hint button ----
  function _correctCell(){ return [...grid.querySelectorAll(".opt-cell")].find(c => isCorrect(_opts[+c.dataset.key], +c.dataset.key)); }
  /* [25d] TERMINAL HELP — never hand the child the answer (Yasir 2026-07-27: "we are not supposed to
     give the correct answer by ourself anywhere at all, it is always the student who has to finalize
     it"). This used to lock the slide, mark the correct cell .correct, and auto-advance after 800ms —
     i.e. the game solved it for them. Now: the wrong options are hard-disabled, the correct one keeps
     an infinite glow and STAYS TAPPABLE, and nothing advances until the child taps it. Same contract
     as the drag mechanics' terminalHelp(). `state.locked` is deliberately NOT set, or the correct cell
     could not be tapped; `state.helpShown` marks the rung for telemetry + prevents re-entry. */
  function revealAnswer(reason){
    if(state.helpShown || state.locked) return;
    state.helpShown = true; state.scaffoldLevel = 3; setSwMood("hint");
    const el = _correctCell();
    [...grid.querySelectorAll(".opt-cell")].forEach(c => {
      if(c !== el){
        c.classList.add("faded");
        c.style.setProperty("pointer-events","none","important");   // CSS alone is defeatable
        c.style.setProperty("opacity",".35","important");
      }
    });
    if(el){
      el.classList.remove("pop-in");        // .pop-in animation outranks the glow, so strip it first
      el.classList.add("reveal-hold");      // infinite pulse — "keeps breathing until you tap it"
      // [27d] The hand lands on the glowing answer in EVERY phase (Yasir 2026-07-27: "hand nudge in
      // guided ... needs to be all uniform and done and perfected"). 27b gated this to tutorial on
      // his earlier wording; that made guided/practice/independent/mastery reveal the answer with a
      // glow but no hand, which is exactly the inconsistency the 50-game batch must not ship.
      // Safe in every phase because we only reach here via terminal help — the glow has ALREADY
      // revealed the answer, so the hand gives nothing away; it just makes "tap THIS one"
      // unmissable for a 5-year-old. The child still has to tap it (terminal help never
      // auto-completes), and the cell's own onclick calls stopNudge(), so the hand clears on tap.
      // stopNudge() FIRST kills any flow-nudge timer already in flight, so it cannot fire a moment
      // later and drag the hand off the answer (see the [27e] guard in startNudge).
      stopNudge();
      handOnAnswer(el, slide);
    }
    GameBus.emit("answer_revealed", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts, reason });
    // speak hint2 (the rung that NAMES the answer), then wait for the child — no auto-advance.
    play(audioFor(slide, "hint") || audioFor(slide, "reveal") || audioFor(slide, "correct") || audioFor(slide, "try_again") || null, ()=>{});
  }
  $("hintBtn").onclick = ()=>{ if(state.locked || state.hintActive) return;
    state.hintUsed = true; if(state.attempts < 1) state.attempts = 1;
    GameBus.emit("hint_shown", { slide_id: slide.id, manual: true });
    GameBus.xapiForSlide("hint_used", slide, { type: "hint", id: "bulb" }, null);   // [spec] hint bulb tapped
    if(runHint) runHint(); else play(audioFor(slide, "hint") || audioFor(slide, "try_again") || null, ()=>{}); };

  // Tap-to-answer standard: a WRONG tap = soft buzz + red ring, and the card UNBLOCKS after 700ms so
  // the child may retry it; from the 2nd wrong attempt the card stays disabled. NO red ✕ anywhere.
  // (Supersedes the earlier lead-review standard "soft buzz + ✕ + that card LOCKS" — reversed by
  // Yasir's ruling 2026-07-27, which also matches the blessed strilling fork. See [27a] above.)
  // a RIGHT tap = confetti cannons + Swiftie cheer, then auto-advance. No select-then-आगे for pick questions.
  $("navBtn").style.display = "none"; setNavActive(false);
  // [27c] AUTONOMOUS TEACHING (data.auto) — a TEACHING slide must run with ZERO child interaction
  // (Yasir 2026-07-27: "in teaching we need to have 0 student interaction ... the tapping part to be
  // done by student is also to be done by us itself"). Same contract as the INTRO / GENDER_INTRO /
  // MEET_WORD demos: we own the audio, every option tap is dead, and the chain answers the question
  // ITSELF — point at the picture and say the prompt → point at the right choice and say the teaching
  // line → mark it correct as its letter sounds → आगे unlocks. No confetti and no sfx: those are the
  // child's reward for answering, and nobody answered. Opt-in, so every non-auto slide is unchanged.
  if(slide.data && slide.data.auto){
    state.locked = true;              // option taps are no-ops for the life of the slide
    state.ownsAudio = true;           // suppress mountSlide's autoPlayChain — the chain plays the prompt
    state.demoRunning = true;         // [24a N8] a replay-chip tap must not gen-kill our own chain
    setSwMood("teach");
    $("navBtn").style.display = ""; setNavActive(false);   // आगे is the only control, and only once taught
    $("navBtn").onclick = ()=> completeSlide(true);
    const _correct = _correctCell();
    const _cOpt = _correct ? _opts[+_correct.dataset.key] : null;
    const _cAid = _cOpt && (_cOpt.audio ||
      (_cOpt.letter && slide.data.phonemes && slide.data.phonemes[_cOpt.letter]) || null);
    // NOTE the stimulus deliberately gets NO hand: pointNudgeAt() plants the fingertip 56px above
    // an element's bottom edge, which on a .stimulus-pic is exactly where its .lbl sits — the hand
    // covered the very word being taught ("घर") for the whole prompt beat. The hand's job here is to
    // carry the eye to the ANSWER, and there is nothing to tap on the picture anyway.
    const steps = [
      [null, audioFor(slide, "prompt")],
      [_correct || null, audioFor(slide, "instruction")],
      [_correct || null, _cAid ? "assets/Audio/" + _cAid + "." + AUDIO_EXT : null]
    ];
    // reveal = the same shape SENTENCE_SOUND's demo already uses: the answer goes green + pulses,
    // the other choices fade back, so a 5-year-old cannot mistake which one is being taught.
    const _reveal = ()=>{ if(!_correct) return;
      _correct.classList.add("correct", "reveal-pulse");
      [...grid.querySelectorAll(".opt-cell")].forEach(c => { if(c !== _correct) c.classList.add("faded"); }); };
    let si = 0, _demoDone = false;
    const finish = ()=>{ if(_demoDone) return; _demoDone = true;
      stopNudge(); state.demoRunning = false;
      _reveal();                                          // idempotent — the last step usually ran it
      setNavActive(true); };
    const step = ()=>{
      if(CARD.slides[state.idx] !== slide) return;        // navigated away → drop the chain
      if(si >= steps.length){ finish(); return; }
      const el = steps[si][0], src = steps[si][1]; si++;
      if(si === steps.length) _reveal();                  // answer lands WITH its sound
      if(el) pointNudgeAt(el);
      play(src || null, ()=> setTimeout(step, 500));
    };
    state.replayAudio = ()=> playChain(steps.map(s => s[1]).filter(Boolean), 0, ()=>{});
    setTimeout(step, 400);
    setTimeout(()=>{ if(CARD.slides[state.idx] === slide) finish(); }, steps.length * 5000 + 3000);   // FAIL-SAFE: never a dead आगे
    return;
  }
  // 16j: OPT-IN staggered option reveal + narrate-each-on-entry (SME wave "options एक-एक करके + सारे
  // बोलना"). Gate on slide.data.reveal_seq — ABSENT ⇒ default behaviour (all options at once), so every
  // existing/non-opted slide is byte-for-byte unchanged. When on: hide the cells, fade them in one by
  // one speaking each option's own clip (opt.audio, or the letter's phoneme), THEN enable taps + nudge.
  if(slide.data && slide.data.reveal_seq){
    // Options reveal one-by-one and each is spoken — but STRICTLY SEQUENCED so no VO ever overlaps
    // another: the prompt plays to COMPLETION, THEN each option word plays only after the previous
    // one ends (fixes "option words spoken before the prompt line finishes"). Every step carries a
    // hard fallback timer, plus a global force-enable, so a missing/blocked/late clip can never
    // soft-lock the game (the failure the old fixed-cadence version was guarding against).
    const _cells = [...grid.querySelectorAll(".opt-cell")];
    _cells.forEach(c => c.classList.add("opt-seq-hidden"));         // class controls hide (opacity+pointer) — reveal = remove class → natural state
    state.locked = true; state.ownsAudio = true;   // we narrate the prompt + options ourselves
    state.revealing = true;   // [24a N8] replay chip ignores taps mid-reveal (no stomping the reveal narration)
    let _done = false;
    const _enableAll = ()=>{ if(_done) return; _done = true; state.locked = false;
      state.revealing = false; state.ownsAudio = false;   // [24a N8] reveal over → the chip may replay the chain again
      _cells.forEach(c => c.classList.remove("opt-seq-hidden")); };   /* [28f] no idle hand */
    // play `src`, then run `next` when it ENDS; a per-clip fallback guarantees the chain always advances
    const _sayThen = (src, next)=>{
      if(_done || CARD.slides[state.idx] !== slide) return;         // [24a bug-hunt F1] _done → the 16s net already force-enabled; STOP the chain so its next play() can't gen-kill a correct tap's advance callback (soft-lock)
      let advanced = false, fb = null;
      const go = ()=>{ if(advanced || _done) return; advanced = true; if(fb) clearTimeout(fb); next(); };
      play(src || null, go);
      fb = setTimeout(go, 4500);                                    // safety net: never stall on one clip
    };
    const _revStep = (i)=>{
      if(_done || CARD.slides[state.idx] !== slide) return;         // [24a bug-hunt F1] navigated away OR net fired → abort the chain
      if(i >= _cells.length){ _enableAll(); return; }
      const c = _cells[i]; c.classList.remove("opt-seq-hidden");
      const opt = _opts[+c.dataset.key];
      const aid = (opt && opt.audio) || (opt && opt.letter && slide.data.phonemes && slide.data.phonemes[opt.letter]) || null;
      _sayThen(aid ? "assets/Audio/" + aid + "." + AUDIO_EXT : null, ()=> setTimeout(()=> _revStep(i + 1), 180));
    };
    _sayThen(audioFor(slide, "prompt") || null, ()=> _revStep(0));  // prompt FULLY, then options one at a time
    setTimeout(()=>{ if(CARD.slides[state.idx] === slide) _enableAll(); }, 16000);   // global safety net — never soft-lock
    return;
  }
  /* [28f] idle hand REMOVED on answerable slides — it fired at nudge_timeout_ms (guided 5000ms),
     i.e. right after the prompt VO, pointing at the stimulus before the child had tried anything.
     A visual hint is earned only by 2 failed attempts. Demo/progress nudges in the count and drag
     mechanics are untouched — those are teaching animations, not hints. */
}

/* ---------- 10. RENDER HELPERS ---------- */
/* Render a picture as the real PNG (assets/Images/<key>.png); if the file is
   missing it falls back to the emoji. Pass the image id (e.g. "pic_anaar"). */
/* [20a SORT-01] opt-in one-by-one tray reveal for SORT_GENDER/SORT_SHAPE (SME g3 pg12/17, asked 4x).
   Gated by slide.data.reveal_seq: hides the draggable tiles, fades them in one at a time speaking each
   item's own clip (tile.dataset.audio), then a SAFETY NET force-shows all so a missing/late clip can
   never soft-lock (mirrors the mountTapOptions reveal_seq). Sort games without reveal_seq are untouched. */
function sortSeqReveal(tray, slide){
  const tiles = [...tray.children];
  tiles.forEach(t => t.classList.add("sort-seq-hidden"));
  state.revealing = true;   // [24a N8] drag + replay chip both blocked while the tray is still revealing
  // [24a bug-hunt F2] narrate prompt→tiles OURSELVES (ownsAudio) so mountSlide's autoPlayChain does NOT
  // fire the prompt concurrently. The old fixed-cadence version let the prompt get CUT at 500ms and
  // TRUNCATED each tile clip at the 760ms tick (live in HI01H04_L03_S04 P1/M2). Now the prompt chain
  // plays to COMPLETION, THEN each tile reveals only after the previous tile's clip ENDS — mirroring the
  // mountTapOptions reveal_seq audio sequencing (not just its safety net).
  state.ownsAudio = true;
  state.replayAudio = ()=> autoPlayChain(slide);
  let i = 0, done = false;
  const enableAll = ()=>{ if(done) return; done = true; state.revealing = false; state.ownsAudio = false;
    tiles.forEach(t => t.classList.remove("sort-seq-hidden")); };
  // play `src`, run `next` when it ENDS; per-clip fallback so a missing/slow clip never stalls the chain
  const sayThen = (src, next)=>{
    if(done || CARD.slides[state.idx] !== slide) return;
    let advanced = false, fb = null;
    const go = ()=>{ if(advanced || done) return; advanced = true; if(fb) clearTimeout(fb); next(); };
    play(src || null, go); fb = setTimeout(go, 4500);
  };
  const step = ()=>{
    if(done || CARD.slides[state.idx] !== slide) return;         // navigated away / net fired -> abort
    if(i >= tiles.length){ enableAll(); return; }
    const t = tiles[i]; t.classList.remove("sort-seq-hidden"); i++;
    sayThen(t.dataset.audio ? "assets/Audio/" + t.dataset.audio + "." + AUDIO_EXT : null, ()=> setTimeout(step, 180));
  };
  autoPlayChain(slide, ()=> setTimeout(step, 250));               // prompt chain FULLY, then tiles one at a time
  setTimeout(()=>{ if(CARD.slides[state.idx] === slide) enableAll(); }, 16000);   // global safety net — never soft-lock
}
/* imgSrc(key): the manifest is the authority on a picture's path, so the bundle can mix formats —
   the poem's scene art ships as .png while the object icons are hand-drawn .svg. Falls back to
   the old assets/Images/<key>.<IMG_EXT> convention for any key the manifest doesn't list. */
function imgSrc(key){
  return (CARD.assets && CARD.assets.image && CARD.assets.image[key])
      || ("assets/Images/" + key + "." + IMG_EXT);
}
function imgOrEmoji(imgKey, emoji, imgClass, emojiClass){
  if(imgKey){
    const fb = String(emoji||"❓").replace(/'/g,"");
    return `<img class="${imgClass}" src="${imgSrc(imgKey)}" alt="" `+
      `onerror="var s=document.createElement('span');s.className='${emojiClass}';s.textContent='${fb}';this.replaceWith(s);">`;
  }
  return `<span class="${emojiClass}">${emoji||"❓"}</span>`;
}
/* [r21] A picture card hugs its own artwork: once an image has loaded, its card is given that
   image own width/height ratio, so a portrait illustration gets a portrait card instead of cream
   bars down both sides. Registered in the CAPTURE phase because "load" does not bubble, and on the
   document so it covers every picture the lesson will ever mount without per-module wiring. */
document.addEventListener("load", function(e){
  const img = e.target;
  if(!img || img.tagName !== "IMG" || !img.naturalWidth || !img.naturalHeight) return;
  const card = img.closest && img.closest(".story-frame, .cmpv-pic");
  if(card) card.style.setProperty("--pic-ratio", img.naturalWidth + " / " + img.naturalHeight);
}, true);

function letterCell(letter){
  const cell = document.createElement("div");
  cell.innerHTML = `<span class="big-glyph ink-glyph">${letter}</span>`;
  return cell;
}
/* ordering/seriation render (MTKGA02_L02_S02): an object at a given magnitude. by="size" scales the
   picture uniformly; by="length" draws a content-true rounded bar of width∝mag; by="weight" shows the
   picture at a uniform size (weight is not visual — the child uses known heaviness / the balance cue). */
function imgOrEmojiSized(img, emoji, px){
  const fb = String(emoji||"❓").replace(/'/g,"");
  if(img) return `<img class="ord-obj-img" style="width:${px}px;height:${px}px" src="${imgSrc(img)}" alt="" `+
    `onerror="var s=document.createElement('span');s.className='ord-obj-emoji';s.style.fontSize='${Math.round(px*0.82)}px';s.textContent='${fb}';this.replaceWith(s);">`;
  return `<span class="ord-obj-emoji" style="font-size:${Math.round(px*0.82)}px">${emoji||"❓"}</span>`;
}
function renderOrdObj(o, by){
  if(by === "length"){ const w = {1:130,2:210,3:300}[o.mag] || 200;
    return `<div class="ord-bar" style="width:${w}px;background:${o.color||"#F5A623"}"></div>`; }
  // size AND weight scale the picture by visual magnitude — so a BIG-but-LIGHT balloon looks big and
  // tempts the child (bigger=heavier misconception), while the small stone is the correct heaviest pick.
  const px = {1:80, 2:116, 3:154}[o.mag] || 116;
  return imgOrEmojiSized(o.img, o.emoji, px);
}
function pictureCell(picture, emoji, imgKey){
  const cell = document.createElement("div");
  cell.innerHTML = imgOrEmoji(imgKey, emoji, "pic-img", "pic-emoji") + `<span class="lbl">${picture||""}</span>`;
  return cell;
}
function stimulusLetter(letter){
  const el = document.createElement("div"); el.className = "stimulus-letter";
  el.innerHTML = `<span class="ink-glyph">${letter}</span>`;
  return el;
}
function stimulusPic(picture, emoji, imgKey){
  const el = document.createElement("div"); el.className = "stimulus-pic";
  el.innerHTML = imgOrEmoji(imgKey, emoji, "img", "emoji") + `<span class="lbl">${picture||""}</span>`;
  return el;
}
/* gender helpers: an option card showing a gender label (पुल्लिंग/स्त्रीलिंग),
   and a stimulus card showing the target gender label. */
function genderLabelCell(label, gender){
  const cell = document.createElement("div");
  cell.innerHTML = `<span class="gender-label${gender==="F"?" fem":""}">${label}</span>`;
  return cell;
}
function stimulusGender(label, gender){
  const el = document.createElement("div");
  el.className = "stimulus-gender" + (gender==="F"?" fem":"");
  el.textContent = label;
  return el;
}

/* shape helpers (maths): render circle/square/triangle/rectangle as inline SVG in
   any colour / size / rotation (LO: recognise regardless of orientation or size).
   No image assets needed — shapes are pure geometry, so the sample renders offline. */
function shapeSVG(shape, opts){
  opts = opts || {};
  const color = opts.color || "#386AF6";
  const size  = opts.size  || 120;
  const rot   = opts.rotate || 0;
  let inner = "";
  if(shape === "circle")         inner = `<circle cx="50" cy="50" r="42" fill="${color}"/>`;
  else if(shape === "square")    inner = `<rect x="12" y="12" width="76" height="76" rx="0" fill="${color}"/>`;   // TRUE corners — teachable geometry is never rounded
  else if(shape === "triangle")  inner = `<polygon points="50,9 91,89 9,89" fill="${color}"/>`;
  else if(shape === "rectangle") inner = `<rect x="6" y="28" width="88" height="44" rx="0" fill="${color}"/>`;    // TRUE corners
  const g = rot ? `<g transform="rotate(${rot} 50 50)">${inner}</g>` : inner;
  return `<svg class="shape-svg" viewBox="0 0 100 100" width="${size}" height="${size}" `+
         `xmlns="http://www.w3.org/2000/svg" aria-hidden="true">${g}</svg>`;
}
function shapeCell(o){
  const cell = document.createElement("div");
  cell.innerHTML = shapeSVG(o.shape, {color:o.color, size:130, rotate:o.rotate});
  return cell;
}
function stimulusShape(o){
  const el = document.createElement("div"); el.className = "stimulus-shape";
  el.innerHTML = shapeSVG(o.shape, {color:o.color, size:150, rotate:o.rotate});
  return el;
}

/* counting helpers (maths): a numeral option card (big numeral + small number word),
   and a stimulus box showing a set of `count` identical objects to be counted. */
function numberCell(numeral, word){
  const cell = document.createElement("div");
  cell.innerHTML = `<span class="num-glyph">${numeral}</span>` + (word ? `<span class="num-word">${word}</span>` : "");
  return cell;
}
/* VISUAL-FIRST quantity: a HAND showing n fingers up (assets/UI/hand_1..5) — pre-reader,
   NO number-word text. Falls back to the numeral only if n is outside 1..5 or the art is missing. */
function fingerCount(n, cls){ cls = cls || "finger-hand";
  if(!(n>=1 && n<=5)) return `<span class="num-glyph">${n}</span>`;
  return `<img class="${cls}" src="assets/UI/hand_${n}.png" alt="" ` +
    `onerror="var s=document.createElement('span');s.className='num-glyph';s.textContent='${n}';this.replaceWith(s);">`;
}
function fingerCell(n){ const c = document.createElement("div"); c.innerHTML = fingerCount(n, "opt-hand"); return c; }
/* DISPLAY numeral: ALWAYS Arabic (1 2 3) on screen — kids learn the universal digit.
   Spoken VO stays Hindi (एक/दो/तीन) via the separate vo_num_/vo_total_ audio files. */
function devNumeral(n){ return String(n); }
/* DUAL-CODED counting option: the Devanagari NUMERAL the child is learning, big and on top,
   with a smaller finger-hand beneath it as a visual anchor. The point of counting is to learn the
   NUMBER SYMBOL, not just read a hand-sign — so the numeral leads and the hand supports. Falls back
   to the numeral alone if the hand art (1..5) is missing. */
function numFingerCell(n){
  // outer div BECOMES the .opt-cell (mountTapOptions adds that class), so the stack lives in an
  // INNER .numfinger wrapper — otherwise ".opt-cell .numfinger x" selectors wouldn't match.
  const c = document.createElement("div");
  // hand art exists only for 1..5; beyond that fingerCount would fall back to a SECOND numeral
  // (numeral shown twice — hit when the counting range grew to 10), so skip the hand entirely.
  c.innerHTML = `<div class="numfinger"><span class="num-glyph">${devNumeral(n)}</span>${(n>=1&&n<=5) ? fingerCount(n, "nf-hand") : ""}</div>`;
  return c;
}
function stimulusCountSet(count, obj, scatter, perRow){
  // counts >10 render DENSE (smaller objects, wrapping); perRow groups the set in rows of exactly
  // N (the curriculum's "rows of 5/10" organisation for sets up to 20 — MTKGA01_L01_S04).
  const dense = count > 10 || !!perRow;
  const el = document.createElement("div"); el.className = "count-set" + (scatter ? " scattered" : "") + (dense ? " dense" : "");
  if(perRow && !scatter){ el.style.display = "grid"; el.style.gridTemplateColumns = `repeat(${perRow}, auto)`; }
  for(let i=0;i<count;i++){
    const c = document.createElement("span"); c.className = "cobj";
    // SCATTERED arrangement (SME/misconception: "total changes when objects are scattered") —
    // deterministic per-index jitter (stable across mounts/captures), never so large items overlap-hide.
    if(scatter) c.style.transform = `translateY(${((i*23)%25)-12}px) rotate(${((i*37)%21)-10}deg)`;
    c.innerHTML = imgOrEmoji(obj.img, obj.emoji, "cobj-img", "cobj-emoji");
    el.appendChild(c);
  }
  return el;
}
/* SME (S01 review deck): outside the tutorial, numeral options show the NUMBER ONLY, larger —
   no finger-hand support (fingers are a TEACHING aid, not a test aid). */
function bigNumCell(n){
  const c = document.createElement("div");
  c.innerHTML = `<span class="bignum-glyph">${devNumeral(n)}</span>`;
  return c;
}
/* COMPARE_SETS helpers (one-to-one matching → ज़्यादा / कम / बराबर).
   Two left-aligned rows (columns line up), a dashed connector drawn top[i]↔bottom[i]
   for each matched pair, and the unmatched leftover item(s) in the longer row glow —
   that glow IS the "which has more" proof. Offsets (not getBoundingClientRect) so it
   works even when the preview tab is throttled. */
function cmpObj(obj){
  const c = document.createElement("span"); c.className = "cobj";
  c.innerHTML = imgOrEmoji(obj.img, obj.emoji, "cobj-img", "cobj-emoji");
  return c;
}
function stimulusCompareSets(data){
  const nA = data.a_count, nB = data.b_count, A = data.a_object, B = data.b_object;
  const NS = "http://www.w3.org/2000/svg";
  const stage = document.createElement("div"); stage.className = "compare-stage";
  const rowA = document.createElement("div"); rowA.className = "cmp-row top";
  const rowB = document.createElement("div"); rowB.className = "cmp-row bot";
  const svg  = document.createElementNS(NS, "svg"); svg.setAttribute("class", "cmp-lines");
  for(let i=0;i<nA;i++) rowA.appendChild(cmpObj(A));
  for(let i=0;i<nB;i++) rowB.appendChild(cmpObj(B));
  stage.appendChild(rowA); stage.appendChild(svg); stage.appendChild(rowB);
  const btn = document.createElement("button"); btn.type = "button"; btn.className = "cmp-match-btn";
  btn.textContent = "🔗 मिलाओ"; stage.appendChild(btn);
  const min = Math.min(nA, nB);
  let drawn = false;
  function draw(){
    while(svg.firstChild) svg.removeChild(svg.firstChild);
    const IA = [...rowA.children], IB = [...rowB.children];
    const y1 = rowA.offsetTop + rowA.offsetHeight - 4;
    const y2 = rowB.offsetTop + 4;
    for(let i=0;i<min;i++){
      const x = IA[i].offsetLeft + IA[i].offsetWidth/2;
      const ln = document.createElementNS(NS, "line");
      ln.setAttribute("x1", x); ln.setAttribute("y1", y1);
      ln.setAttribute("x2", x); ln.setAttribute("y2", y2);
      ln.setAttribute("class", "cmp-line"); svg.appendChild(ln);
      setTimeout(()=> ln.classList.add("show"), 130*i);
    }
    const longer = nA > nB ? IA : nB > nA ? IB : null;   // null when equal (nothing left over)
    if(longer) for(let i=min;i<longer.length;i++)
      setTimeout(()=> longer[i].classList.add("leftover"), 130*min + 160);
  }
  // reveal the matching (child taps मिलाओ, or the hint/tutorial calls this). cb fires after it settles.
  stage._revealMatches = (cb)=>{ if(!drawn){ drawn = true; btn.disabled = true; draw(); }
    if(cb) setTimeout(cb, 130*min + 800); };
  btn.onclick = ()=> stage._revealMatches();
  if(data.show_matches){ btn.style.display = "none"; setTimeout(()=> stage._revealMatches(), 420); }
  return stage;
}
/* HINT for "how many": instead of a text popup, COUNT the set FOR the child —
   highlight each object left→right, say एक/दो/तीन, show the numeral on top of it.
   The child sees + hears the count modelled, then answers from the options. */
function demoCount(items, numerals, onDone){
  numerals = numerals || [];
  const clear = ()=> items.forEach(o=>{ o.classList.remove("counting"); const c=o.querySelector(".count-callout"); if(c) c.remove(); });
  clear();
  let i = 0;
  (function step(){
    if(i >= items.length){                       // last count landed → clear, then continue
      setTimeout(()=>{ clear(); if(onDone) onDone(); }, 1000);
      return;
    }
    const o = items[i];
    o.classList.add("counting");
    let cal = o.querySelector(".count-callout");
    if(!cal){ cal = document.createElement("span"); cal.className = "count-callout"; o.appendChild(cal); }
    cal.textContent = String(i+1);   // Arabic count callout; Hindi number-word is spoken separately
    play("assets/Audio/vo_num_" + (i+1) + "." + AUDIO_EXT, ()=>{ i++; setTimeout(step, 320); });
  })();
}
function demoCountSet(setEl, count, numerals, onDone){   // count the "how many?" stimulus set
  demoCount([...setEl.querySelectorAll(".cobj")].slice(0, count), numerals, onDone);
}

/* ---------- 10b. DEVANAGARI GLYPH INK-CENTERING ----------
   Devanagari glyphs carry matras above (ओ, औ, अं) and below (ऋ) the shirorekha,
   so plain flex `align-items:center` leaves them sitting high with a gap below —
   and the offset differs per glyph. Measure each glyph's real ink box (canvas
   actualBoundingBox) + its baseline in the DOM, then translateY so the INK is
   truly centred in its tile/box. Font-agnostic; recomputed on mount + fonts.ready. */
let _inkCtx = null;
function centerInkGlyph(span){
  if(!span || !span.parentElement) return;
  const glyph = (span.textContent || "").trim();
  if(!glyph) return;
  const box = span.parentElement;
  const cs = getComputedStyle(span);
  const fpx = parseFloat(cs.fontSize);
  if(!fpx) return;
  _inkCtx = _inkCtx || document.createElement("canvas").getContext("2d");
  // --- WIDTH-FIT (16m+): shrink font so the word never spills its box. Applies to EVERY
  // ink-glyph (drag tiles, mastery stimulus, tap tiles), not just MEET_LETTER's _mlFit —
  // that fix only touched the teaching slide, so माला/नाक/पापा still overflowed dd-tile /
  // stimulus-letter on the practice slides (Yasir catch #6). Baseline size captured once in
  // data-ink-base so this is idempotent across re-runs (mount + fonts.ready + resize).
  const _base = span.dataset.inkBase ? parseFloat(span.dataset.inkBase) : fpx;
  if(!span.dataset.inkBase) span.dataset.inkBase = String(_base);
  const _bcs = getComputedStyle(box);
  const _availW = box.clientWidth - (parseFloat(_bcs.paddingLeft)||0) - (parseFloat(_bcs.paddingRight)||0);
  _inkCtx.font = `${cs.fontWeight} ${_base}px ${cs.fontFamily}`;
  /* [28i] FIT THE INK, NOT THE ADVANCE — the SME's original "decrease the size of the words so that
     they all fit perfectly inside the box", which the 16m width-fit did not actually achieve.
     Devanagari PAINTS wider than it advances: the shirorekha and the matras overhang, so ink runs
     ~4-11px past measureText().width. The failure was not a wrong scale factor, it was the BRANCH: a
     word whose advance fits `_availW` never entered the shrink path at all, so its ink overflow was
     never even considered. Measured with this same canvas API at the real computed size on
     HI01H04_L02_S02: P6 यह ink 66 vs box 59, बकरी 138/132, एक 91/85, T4 कहाँ 184/180 — all four had a
     fitting advance and were therefore left alone. Fit whichever of the two actually paints wider, so
     a Latin/numeral glyph (ink <= advance) behaves exactly as before and nothing else in the fleet
     shifts. The 0.94 safety margin is kept; with ink as the base it is now margin rather than the
     only thing standing between the word and the border. */
  const _mB = _inkCtx.measureText(glyph);
  const _inkW = (isFinite(_mB.actualBoundingBoxLeft) && isFinite(_mB.actualBoundingBoxRight))
    ? (_mB.actualBoundingBoxLeft + _mB.actualBoundingBoxRight) : _mB.width;
  /* TWO BUDGETS, because ink and advance are not competing for the same space.
     The ADVANCE must fit the CONTENT box (unchanged from 16m — that is the layout contract).
     The INK must merely not cross the BORDER, and padding is exactly the room provided for overhang:
     .sentence-word carries 30px each side, so a word whose ink runs 5px past the content edge is
     2.5px into a 30px cushion — invisible. My first pass fitted ink to the content box and would have
     shrunk almost every Devanagari word in the fleet to buy nothing; for a KG reader, needlessly
     smaller text is a real cost. So each budget constrains its own measure and the tighter of the two
     wins. A word only shrinks for ink when the ink would actually reach the border. */
  const _availInk = box.clientWidth;                       // padding box = inside the border
  let _sc = 1;
  if(_availW   > 8 && _mB.width > _availW)   _sc = Math.min(_sc, _availW   / _mB.width);
  if(_availInk > 8 && _inkW     > _availInk) _sc = Math.min(_sc, _availInk / _inkW);
  let _fpx = _base;
  if(_sc < 1) _fpx = Math.max(20, _base * _sc * 0.94);
  if(Math.abs(_fpx - fpx) > 0.5) span.style.fontSize = _fpx + "px";
  _inkCtx.font = `${cs.fontWeight} ${_fpx}px ${cs.fontFamily}`;
  const m = _inkCtx.measureText(glyph);
  /* [27h] F2 — SHARED BASELINE FOR A ROW OF WORDS.
     Ink-centring (actualBoundingBox*) is measured from THIS glyph's own ink, so every word lands
     differently: a word with an above-line matra (और/मैं/की/कौन) has a taller ascent, gets pushed
     further DOWN, and one with a below-line matra (तुम/फूल) sits HIGHER. Measured on 27g in one row:
     T1 एक 39 / घर 43 / और 59 · G2 यह 55 / वह 55 / मैं 75 · P5 तुम 45 / फूल 46 / गेंद 68 / आम 61.
     That is a 23px spread inside a single row and it is exactly the SME's "text alignment of the
     words is not right" — written on 7 of 17 pages of one deck alone.
     Words in a row must share a BASELINE, so use FONT metrics (fontBoundingBox*), which are constant
     for a given font+size and therefore give every tile in the row the same dy.
     A LONE showcase glyph (MEET_LETTER's 200px letter) still uses ink metrics: there is no row to
     align with, and at that size font-box centring would sit it visibly low because the font box
     reserves descender room the letter does not use. */
  const _row = box.parentElement;
  const _inRow = !!_row && _row.querySelectorAll(".ink-glyph").length > 1;
  let a = m.actualBoundingBoxAscent, d = m.actualBoundingBoxDescent;
  if(_inRow && isFinite(m.fontBoundingBoxAscent) && isFinite(m.fontBoundingBoxDescent)){
    a = m.fontBoundingBoxAscent; d = m.fontBoundingBoxDescent;
  }
  if(!isFinite(a) || !isFinite(d)) return;
  const scale = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--scale")) || 1;
  span.style.transform = "";   // reset before measuring baseline
  const probe = document.createElement("span");
  probe.style.cssText = "display:inline-block;width:0;height:0;vertical-align:baseline;";
  span.appendChild(probe);
  const baseScreen = probe.getBoundingClientRect().top;
  span.removeChild(probe);
  const br = box.getBoundingClientRect();
  if(br.height < 5) return;    // not laid out yet
  const boxCenter = br.top + br.height/2;
  const inkCenter = baseScreen + ((d - a)/2) * scale;   // screen px
  const dy = (boxCenter - inkCenter) / scale;           // css px to move glyph down
  span.style.transform = `translateY(${dy}px)`;
}
function centerAllGlyphs(root){
  (root || document).querySelectorAll(".ink-glyph").forEach(centerInkGlyph);
}

/* ---------- 10c. IN-WORD MATRA COLOURING (AA / right-spacing matras) ----------
   Colour the matra RED *inside the word itself* (e.g. the ा in दादा) with no artifacts.
   Per-character fill CANNOT do this: द+ा shape as ONE cluster the browser colours as a
   unit — a <span>/<tspan> on the ा is ignored (colours by the base consonant), and forcing
   the ा into its own run inserts a dotted circle (◌ा). Verified at the pixel level. The clean
   way is a two-layer overlay: the whole word in the base colour + a RED copy of the SAME word
   clipped to just the matra's x-column(s). Both layers are the identical string at identical
   coords, so shaping is identical and the red lands exactly on the matra strokes (100% ink
   match vs the plain word, no ◌, no shift, no duplicate आ).
   ONLY valid for RIGHT-SPACING matras (matra owns its own right-hand column). Above/below/left
   matras (े ै ि ु ृ …) have no such column, so callers fall back to the old coloured callout.
   Extend the set ONLY after pixel-verifying the new matra's geometry. */
const RIGHT_SPACING_MATRAS = new Set(["ा"]);
const _COMB = /[ऀ-ःऺ-ॏ॑-ॗॢॣ]/;   // Devanagari combining marks
let _matraUid = 0, _mCv = null, _mCx = null;
/* Pixel-accurate RED column(s) for the matra(s) in `word`. The matra's vertical stroke ends at
   its advance, but its shirorekha (top bar) overhangs — a navy end-cap on the last matra, or the
   connector toward the next letter on a medial one. So: left = consonant advance; right = the next
   consonant's BODY left (found by scanning the LOWER band, below the continuous top bar) or the
   word's ink-right for the last cluster. That paints the whole matra + its bar red with no navy
   sliver, and stops before the next letter's body. Canvas raster uses the real Baloo 2 (recomputed
   on fonts.ready by refreshMatraWords, so fallback-metric first paints self-correct). */
function _matraClipCols(word, matra, fontPx){
  _mCx = _mCx || (_mCv = document.createElement("canvas")).getContext("2d");
  const ctx = _mCx, font = `800 ${fontPx}px "Baloo 2","Noto Sans Devanagari",sans-serif`;
  ctx.font = font;
  const ch = [...word], cl = []; let x = 0, i = 0;
  while(i < ch.length){ let j = i + 1, hasM = false;
    while(j < ch.length && _COMB.test(ch[j])){ if(ch[j] === matra) hasM = true; j++; }
    const cw = ctx.measureText(ch.slice(i, j).join("")).width;
    cl.push({ start: x, consW: ctx.measureText(ch[i]).width, cw, hasM }); x += cw; i = j; }
  const W = Math.ceil(x) + 4, H = Math.ceil(fontPx * 1.4);
  _mCv.width = W; _mCv.height = H; ctx.font = font; ctx.textBaseline = "alphabetic"; ctx.fillStyle = "#000";
  ctx.clearRect(0, 0, W, H); ctx.fillText(word, 0, Math.round(fontPx));
  const d = ctx.getImageData(0, 0, W, H).data, ink = (X, Y)=> d[(Y * W + X) * 4 + 3] > 40;
  let y0 = H, y1 = 0;
  for(let Y = 0; Y < H; Y++) for(let X = 0; X < W; X++){ if(ink(X, Y)){ if(Y < y0) y0 = Y; if(Y > y1) y1 = Y; break; } }
  const bTop = Math.round(y0 + (y1 - y0) * 0.40), bBot = Math.round(y1 - (y1 - y0) * 0.02);   // below the shirorekha
  const colInk = new Array(W).fill(false);
  for(let X = 0; X < W; X++) for(let Y = bTop; Y <= bBot; Y++){ if(ink(X, Y)){ colInk[X] = true; break; } }
  const runs = []; let s = null;
  for(let X = 0; X < W; X++){ if(colInk[X] && s === null) s = X; else if(!colInk[X] && s !== null){ runs.push([s, X - 1]); s = null; } }
  if(s !== null) runs.push([s, W - 1]);
  let inkRight = 0; for(let X = W - 1; X >= 0; X--){ let a = false; for(let Y = 0; Y < H; Y++){ if(ink(X, Y)){ a = true; break; } } if(a){ inkRight = X; break; } }
  const cols = [];
  cl.forEach((c, idx)=>{ if(!c.hasM) return;
    const advEnd = c.start + c.cw, left = c.start + c.consW;
    let right;
    if(idx === cl.length - 1){ right = inkRight + Math.max(4, fontPx * 0.06); }    // last cluster → generously past the end-cap (nothing to the right, so free)
    else { const before = runs.filter(r => r[0] < advEnd);                         // medial → the next consonant's body-left + ~1px, so the whole
           const matraRight = before.length ? before[before.length - 1][1] : advEnd; //   connector bar is red (only the body's faint AA edge is grazed)
           const next = runs.find(r => r[0] > matraRight);
           right = (next ? next[0] : advEnd) + Math.max(1, fontPx * 0.012); }
    cols.push([left, Math.max(right, advEnd)]);
  });
  return cols;
}
function _matraWordSVG(word, matra, fontPx){
  _mCx = _mCx || (_mCv = document.createElement("canvas")).getContext("2d");
  _mCx.font = `800 ${fontPx}px "Baloo 2","Noto Sans Devanagari",sans-serif`;
  const totalW = _mCx.measureText(word).width;
  const cols = _matraClipCols(word, matra, fontPx);
  const padX = fontPx * 0.12, asc = fontPx * 0.92, desc = fontPx * 0.30;
  const W = totalW + padX * 2, H = asc + desc, uid = "mw" + (++_matraUid);
  const esc = (s)=> String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  const tAttr = `x="${padX.toFixed(2)}" y="${asc.toFixed(2)}" text-anchor="start" font-family="'Baloo 2','Noto Sans Devanagari',sans-serif" font-weight="800" font-size="${fontPx}"`;
  const clip = cols.map(([a,b])=>`<rect x="${(a+padX).toFixed(2)}" y="0" width="${Math.max(0,b-a).toFixed(2)}" height="${H.toFixed(2)}"/>`).join("");
  return `<svg class="matra-word" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W.toFixed(2)} ${H.toFixed(2)}" width="${W.toFixed(2)}" height="${H.toFixed(2)}" role="img" aria-label="${esc(word)}">`
    + (cols.length ? `<defs><clipPath id="${uid}">${clip}</clipPath></defs>` : "")
    + `<text class="mw-base" ${tAttr}>${esc(word)}</text>`
    + (cols.length ? `<g class="mw-red" clip-path="url(#${uid})"><text ${tAttr}>${esc(word)}</text></g>` : "")
    + `</svg>`;
}
/* rebuild the matra SVGs (clip columns depend on font metrics — recompute once the web font
   has actually loaded, so a first paint with fallback metrics can't leave the red mis-clipped). */
function refreshMatraWords(root){
  (root || document).querySelectorAll(".meet-letter-box[data-mw-word]").forEach(box=>{
    box.innerHTML = _matraWordSVG(box.dataset.mwWord, box.dataset.mwMatra, parseFloat(box.dataset.mwFs) || 120);
  });
}

/* ---------- 11. DRAG-DROP PRIMITIVE ---------- */
/* [B3] SINGLE-DRAG OWNER. `dragging` below is a per-tile closure variable — one per makeDraggable
   call — so it could only ever answer "is THIS tile dragging", never "is ANY tile dragging". Two
   fingers on two tiles therefore each set their own flag and both tiles dragged at once; worse,
   onMove reads touches[0] unconditionally, so the second tile tracked the FIRST finger. This
   module-level owner is the missing cross-tile lock: exactly one tile may hold a drag at a time. */
let _dragOwner = null;
function makeDraggable(tileEl, onDrop, opts){
  let startX=0, startY=0, dx=0, dy=0, dragging=false;
  let scale = 1;
  const refScale = ()=> scale = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--scale")) || 1;
  function onDown(e){
    if(tileEl.classList.contains('fvd-tile') && (state.locked || tileEl.classList.contains('used')))return;
    if(tileEl.classList.contains("snapped") || tileEl.classList.contains("matched")) return;
    if(state.revealing) return;   // [24a N8] tray still revealing one-by-one → no grabs yet (parity with the tap path's lock)
    if(_dragOwner && _dragOwner !== tileEl) return;   // [B3] another tile already owns the drag — ignore this second finger
    refScale();
    dragging = true;
    _dragOwner = tileEl;
    // bind move/up on the document ONLY while dragging (removed in onUp) — otherwise every tile leaves
    // stale document listeners that pile up across the 11 drag slides.
    document.addEventListener("mousemove", onMove);
    document.addEventListener("touchmove", onMove, {passive:false});
    document.addEventListener("mouseup", onUp);
    document.addEventListener("touchend", onUp);
    document.addEventListener("touchcancel", onCancel);     // [24a bug-hunt F3] a cancelled touch (call, gesture-nav) must abort, not orphan listeners + leave the tile stuck mid-drag
    document.addEventListener("pointercancel", onCancel);
    const p = e.touches ? e.touches[0] : e;
    startX = p.clientX; startY = p.clientY;
    dx = 0; dy = 0;
    tileEl.classList.add("dragging");
    if(opts && opts.onPick) opts.onPick();   // e.g. show a nudge at the slot this tile belongs in
    e.preventDefault();
  }
  function onMove(e){
    if(!dragging) return;
    const p = e.touches ? e.touches[0] : e;
    dx = (p.clientX - startX) / scale; dy = (p.clientY - startY) / scale;
    tileEl.style.transform = `translate(${dx}px,${dy}px) scale(1.08)`;
    // highlight zone under — hide the tile from hit-testing so the dragged tile
    // (z-index 50, now covering the zone) doesn't mask the zone beneath it.
    const cx = p.clientX, cy = p.clientY;
    document.querySelectorAll(".dd-zone").forEach(z => z.classList.remove("hover"));
    tileEl.style.pointerEvents = "none";
    const under = document.elementFromPoint(cx, cy);
    tileEl.style.pointerEvents = "";
    const zone = under?.closest?.(".dd-zone");
    if(zone && !zone.classList.contains("filled")) zone.classList.add("hover");
    e.preventDefault();
  }
  function _unbind(){
    if(_dragOwner === tileEl) _dragOwner = null;   // [B3] release the lock here — both onUp and onCancel route through _unbind, so an OS interrupt can't wedge it
    document.removeEventListener("mousemove", onMove);
    document.removeEventListener("touchmove", onMove);
    document.removeEventListener("mouseup", onUp);
    document.removeEventListener("touchend", onUp);
    document.removeEventListener("touchcancel", onCancel);
    document.removeEventListener("pointercancel", onCancel);
  }
  function onCancel(){   // [24a bug-hunt F3] abort an interrupted drag: unbind + spring the tile back, never drop
    if(!dragging) return;
    dragging = false; _unbind();
    tileEl.classList.remove("dragging"); tileEl.style.transform = "";
    document.querySelectorAll(".dd-zone,.sort-bin").forEach(z => z.classList.remove("hover"));
  }
  function onUp(e){
    if(!dragging) return;
    dragging = false;
    _unbind();
    tileEl.classList.remove("dragging");
    const p = e.changedTouches ? e.changedTouches[0] : e;
    // hide the tile from hit-testing so we detect the zone underneath it
    tileEl.style.pointerEvents = "none";
    const under = document.elementFromPoint(p.clientX, p.clientY);
    tileEl.style.pointerEvents = "";
    const zone = under?.closest?.(".dd-zone");
    document.querySelectorAll(".dd-zone").forEach(z => z.classList.remove("hover"));
    if(zone && !zone.classList.contains("filled")){
      // snap
      tileEl.style.transform = "";
      onDrop(zone, tileEl);
    } else {
      tileEl.style.transform = "";
      if(Math.abs(dx) < 6 && Math.abs(dy) < 6 && opts && opts.onTap) opts.onTap();   // a tap (not a drag) → speak the word
    }
  }
  tileEl.addEventListener("mousedown", onDown);
  tileEl.addEventListener("touchstart", onDown, {passive:false});
}
/* [24a A1] DRAG VO-GATE (Yasir 2026-07-24, fork-proven in the HI01H08 gender file): while a VO is
   sounding, a press that would start a NEW drag is IGNORED, so picking up a tile can't cut the
   prompt/feedback voice — the drag equivalent of the tap gate in mountTapOptions. MUST run in the
   CAPTURE phase: MATCH_DRAG_N tiles carry their OWN speak-on-press listener (pointerdown, registered
   before makeDraggable's onDown) — an in-onDown `if(isPlaying)` check would see the tile's OWN audio
   and block every grab (total soft-lock). At capture time isPlaying still reflects the genuinely
   PRIOR VO. Gated on pointerdown + mousedown + touchstart so both the speak listener and onDown are
   swallowed. 4s safety via _voStart: a stalled clip must never freeze the tiles. Scoped to draggable
   game tiles only — replay chips, nav and tap-answer cells take presses as usual. */
(function installDragVoGate(){
  const SEL = ".sort-item, .dd-tile, .cdm-objtile, .cdm-card, .combine-drag, .bp-tile, .ev-sort-item";   /* [reskin] + the punctuation / sort tiles */
  // ONE decision PER PRESS, made at pointerdown (the earliest event, BEFORE the tile's own
  // speak-on-press listener can flip isPlaying). The same press's trailing mousedown/touchstart
  // INHERIT that decision — re-evaluating them would see the press's OWN audio and block the very
  // grab that was just allowed (the trap, resurrected through event-type ordering).
  let _decision = 0, _decidedAt = 0;   // 0 = none · 1 = allow · 2 = block
  function decide(e, now){
    const t = e.target && e.target.closest && e.target.closest(SEL);
    if(!t || t.classList.contains("snapped") || t.classList.contains("matched")){ _decision = 0; return 0; }
    _decidedAt = now;
    _decision = (isPlaying && now - _voStart < 4000) ? 2 : 1;  // 4s safety: a stuck VO must not freeze the tiles
    return _decision;
  }
  function gate(e){
    const now = Date.now();
    let d;
    if(e.type === "pointerdown" || !_decision || now - _decidedAt > 400){
      d = decide(e, now);                                      // fresh press (or no pointer events on this browser)
    } else {
      d = _decision;                                           // trailing event of the SAME press → inherit
    }
    if(d === 2){ e.stopImmediatePropagation(); if(e.cancelable) e.preventDefault(); }   // swallow before speak-on-press + onDown
  }
  document.addEventListener("pointerdown", gate, true);
  document.addEventListener("mousedown", gate, true);
  document.addEventListener("touchstart", gate, {capture:true, passive:false});
})();
/* [24a A5] When a sort card is placed in a bin it LEAVES a faint, same-size dashed placeholder in
   the tray at its exact original spot (Yasir 2026-07-24, parity with the production gender game).
   The ghost holds the flex slot so the remaining tray cards don't shift, and marks where the card
   came from. Sized BEFORE the tile moves/shrinks (offsetWidth is read while it still sits in the tray). */
function leaveTrayGhost(tile){
  if(!tile || tile._ghosted) return;
  const tray = tile.parentElement;
  // [25c] The guard used to accept ONLY ".sort-tray", so calling this from MATCH_DRAG_N silently
  // did nothing — match tiles live in a ".dd-row". Accept every drag-SOURCE row so "ghost slots
  // wherever we have dragging" (Yasir 2026-07-25) actually holds. .sort-ghost is plain flex CSS,
  // so it lays out correctly in either container.
  const SOURCE_ROWS = ["sort-tray", "dd-row", "tile-row", "match-row"];
  if(!tray || !SOURCE_ROWS.some(c => tray.classList.contains(c))) return;
  const g = document.createElement("div");
  g.className = "sort-ghost";
  g.style.width = tile.offsetWidth + "px";
  g.style.height = tile.offsetHeight + "px";
  tray.insertBefore(g, tile);
  tile._ghosted = true;
}
/* shared wrong-drop response for drag/sort/sequence modules: soft buzz + Swiftie try-again pose + the
   authored spoken recovery. Pre-readers need the SPOKEN recovery, not just the visual spring-back.
   [24b] TWO-LEVEL DRAG HINTS (Yasir 2026-07-25: "everywhere, regardless of game or type of
   interaction, we are going to have two hints"). The tap path already graded its feedback in
   mountTapOptions; drag had NO hint clip at all (only try_again). Now: 1st wrong -> the slide's
   `hint1`; 2nd and later -> `hint` (the level that GIVES the answer). Every drag mechanic inherits
   this because all 12 wrong-drop sites funnel through here. The count is tracked per-slide inside
   this helper, so NO call site changes. Fully ADDITIVE: a card with no hint1/hint authored still
   plays try_again exactly as before, so sibling games are byte-for-byte unchanged in behaviour. */
let _dwSlide = null, _dwN = 0;
function dragWrong(slide, tile){
  sfxWrongSoft(); setSwMood("tryagain");
  const sid = slide && slide.id;
  if(sid !== _dwSlide){ _dwSlide = sid; _dwN = 0; }   // new slide -> restart the ladder
  _dwN++;
  // [25b] PER-PAIR hint2 on drag (Yasir 2026-07-25): the 2nd hint must name the tile the child is
  // holding AND the picture it belongs to — "यह 'क' है, यह 'कमल' की पहली ध्वनि है।" A single
  // slide-level clip can't do that, so when the caller passes the dragged tile we look up that
  // pair's own `hint2_audio`. Falls through to the slide-level hint when a pair has none authored.
  if(_dwN > 1 && tile && slide && slide.data && Array.isArray(slide.data.pairs)){
    const L = (tile.textContent || "").trim();
    const pr = slide.data.pairs.find(p => String(p.letter || "").trim() === L);
    if(pr && pr.hint2_audio){
      play("assets/Audio/" + pr.hint2_audio + "." + AUDIO_EXT, ()=>{});
      return;
    }
  }
  const clip = (_dwN <= 1)
    ? (audioFor(slide, "hint1") || audioFor(slide, "try_again"))
    : (midHint(slide) || audioFor(slide, "hint1"));          /* [28k] rung 2 (drag) */
  play(clip || null, ()=>{});
}

/* shared SUCCESS response — the engine-wide answer-feedback standard (lead-confirmed): side confetti
   cannons + rising sfx + Swiftie celebrates + the authored "correct" VO, then AUTO-ADVANCE. Never a
   celebration popup, never a "press आगे to continue" gate on a solved activity. `revealed` = the child
   got there via the reveal scaffold → quieter settle (no confetti/cheer) + completeSlide(false) so
   mastery telemetry stays honest. */
function celebrateThenAdvance(slide, revealed){
  if(revealed){ play(audioFor(slide, "reveal") || null, ()=>{}); setTimeout(()=> completeSlide(false), 1400); return; }
  sfxCorrect(); confettiCannon(); setSwMood("celebrate");
  play(audioFor(slide, "correct") || null, ()=>{});
  setTimeout(()=> completeSlide(true), 1400);
}

/* Three-item plural art is a global visual grammar: blue drag cards and pair bubbles
   always use a compact 2-up / 1-down triangle, regardless of the noun or its asset format. */
function triangleArt(imgKey, emoji, mode){
  const singularKey = String(imgKey || "").replace(/_p$/, "_s");
  const singularEmoji = Array.from(String(emoji || "❓"))[0] || "❓";
  const pieces = [1,2,3].map(i => imgOrEmoji(singularKey, singularEmoji,
    `tri-piece tri-p${i}`, `tri-piece tri-p${i}`)).join("");
  /* Keep authored group art only where the individual characters/poses are intentionally
     different. Ordinary plurals use the global 2-up / 1-down visual grammar. */
  const authoredGroup = /^(obj_saheli_p|obj_ladka_p|obj_tali_p)$/.test(String(imgKey || ""));
  if(authoredGroup){
    return `<span class="tri-art tri-${mode}"><img class="tri-composite" src="${imgSrc(imgKey)}" alt="" onerror="this.style.display='none';this.nextElementSibling.style.display='block'"><span class="tri-fallback" style="display:none">${pieces}</span></span>`;
  }
  return `<span class="tri-art tri-${mode}"><span class="tri-fallback">${pieces}</span></span>`;
}

/* nextFrame(fn): run fn after layout, but ALSO run it in a hidden/background tab. Browsers pause
   requestAnimationFrame while a tab is hidden, so a lesson opened in a background tab (or behind
   another window on a school tablet) would otherwise never measure its layout or start its
   opening narration — the activity just sits there dead until the tab is focused. */
function nextFrame(fn){
  let done = false;
  const run = ()=>{ if(done) return; done = true; fn(); };
  requestAnimationFrame(run);
  setTimeout(run, 120);
}

/* ---------- READING PACE ----------
   A Grade-2 reader needs to actually READ a beat before it moves on. Every auto-advance in the
   lesson derives its timing from here, so the whole game paces the same and can be tuned in ONE
   place. readTime() scales with how much text is on screen; `tail` is the quiet beat that always
   follows a VO before anything changes, so a picture never swaps the instant a voice stops. */
const PACE = {
  lineStep: 1350,          // gap between the poem's lines arriving one by one
  perChar : 105,           // reading allowance per Devanagari character
  readMin : 3800,
  readMax : 11000,
  tail    : 1000,          // requested inter-screen beat: one second after VO
  readTime(text){
    const n = String(text || "").length;
    return Math.min(this.readMax, Math.max(this.readMin, n * this.perChar));
  }
};

/* ---------- review-deck helpers ---------- */
/* Deck pp.4,6,8,10 + pp.5,7,9,11: the target word is shown in ORANGE inside the poem line and
   inside the compared word. Authors mark it in card.json with *asterisks*; everything else is
   escaped, so a stanza can never inject markup. */
function hlText(s){
  return String(s == null ? "" : s)
    .replace(/[&<>]/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;" }[c]))
    .replace(/\*([^*]+)\*/g, '<b class="hl-orange">$1</b>');
}

/* STORY_SCENE poem captions: show each complete line immediately, then pulse whole words in
   playback order. The real clip's currentTime drives the word cue; authored VO timing is the
   fallback while a recording is not available. */
function storyTypeLine(raw){
  const p=document.createElement("div"); p.className="ln";
  const source=String(raw == null ? "" : raw);
  const plain=source.replace(/\*([^*]+)\*/g,"$1");
  p.setAttribute("aria-label",plain);
  const wordSegment=s=>{
    if(!(window.Intl&&Intl.Segmenter))return s.match(/\s+|[^\s]+/gu)||[];
    const parts=Array.from(new Intl.Segmenter("hi",{granularity:"word"}).segment(s));
    const merged=[];let prefix="";
    parts.forEach(part=>{
      const piece=part.segment;
      if(/^\s+$/u.test(piece)){if(prefix){merged.push(prefix);prefix="";}merged.push(piece);return;}
      if(part.isWordLike){merged.push(prefix+piece);prefix="";return;}
      if(merged.length&&!/^\s+$/u.test(merged[merged.length-1]))merged[merged.length-1]+=piece;
      else prefix+=piece;
    });
    if(prefix){
      const last=merged.length-1;
      if(last>=0&&!/^\s+$/u.test(merged[last]))merged[last]+=prefix;
      else merged.push(prefix);
    }
    return merged;
  };
  source.split(/(\*[^*]+\*)/g).filter(Boolean).forEach(part=>{
    const marked=part.startsWith("*")&&part.endsWith("*");
    const text=marked?part.slice(1,-1):part;
    wordSegment(text).forEach(piece=>{
      if(/^\s+$/u.test(piece)){p.appendChild(document.createTextNode(piece));return;}
      const span=document.createElement("span");
      span.className="poem-word"+(marked?" hl-orange":"");
      span.textContent=piece;
      const letters=Array.from(piece.replace(/[^\p{L}\p{M}\p{N}]/gu,"")).length;
      const pause=/[।!?]$/.test(piece)?4.5:/[,—–…:“”]$/.test(piece)?2.2:0;
      span.dataset.poemWeight=String(Math.max(1,letters)+pause);
      p.appendChild(span);
    });
  });
  p.classList.add("in");
  return p;
}

function storyTypeSync(lines, src, onComplete){
  const words=lines.flatMap(line=>Array.from(line.querySelectorAll(".poem-word")));
  const weights=words.map(w=>parseFloat(w.dataset.poemWeight)||1);
  const total=weights.reduce((n,w)=>n+w,0)||1;
  let token=0,raf=0,lastWord=-1;
  const reset=()=>{
    cancelAnimationFrame(raf);token++;lastWord=-1;
    words.forEach(w=>w.classList.remove("is-speaking"));
    lines.forEach(l=>l.classList.add("in"));
  };
  const start=()=>{
    reset(); const mine=token, began=Date.now(), fallbackMs=authoredVoHoldMs(src)||1200;
    play(src,()=>{
      if(mine!==token)return;
      words.forEach(w=>w.classList.remove("is-speaking"));lastWord=-1;
      if(onComplete)onComplete();
    });
    const expected=String(src||"").split("/").pop();
    const tick=()=>{
      if(mine!==token||!lines[0]||!lines[0].isConnected)return;
      const audio=currentAudio;
      const activeFile=audio?String(audio.currentSrc||audio.src||"").split("/").pop():"";
      let progress=Math.min(1,(Date.now()-began)/fallbackMs);
      if(audio&&(!expected||decodeURIComponent(activeFile)===expected)&&isFinite(audio.duration)&&audio.duration>0)
        progress=audio.currentTime/audio.duration;
      const target=progress*total;
      let acc=0,active=-1;
      for(let i=0;i<weights.length;i++){if(target<acc+weights[i]){active=i;break;}acc+=weights[i];}
      if(active!==lastWord){
        if(lastWord>=0&&words[lastWord])words[lastWord].classList.remove("is-speaking");
        if(active>=0&&words[active])words[active].classList.add("is-speaking");
        lastWord=active;
      }
      if(isPlaying) raf=requestAnimationFrame(tick);
    };
    raf=requestAnimationFrame(tick);
  };
  return {start,reset,finish(){reset();}};
}

/* EVIDENCE comprehension helpers (H04 L03 शाब्दिक एवं अनुमान-आधारित बोध) — ADDITIVE (r4n); used only by
   STORY_READALONG / EVIDENCE_QA / FIND_EVIDENCE / QTYPE_RECAP. A passage = optional picture + the story
   text as sentence spans (each sentence has its own clip, so it can be read along / re-heard / tapped).
   evMark() lights the proof: literal → yellow highlight + "📖 उत्तर यहाँ लिखा है"; inference → dashed
   purple outline + "🔍 सुराग़" (the curriculum's "सुराग़ अलग टैग से दिखता है"). */
function evPassage(p, opts){
  p = p || {}; opts = opts || {};
  const card = document.createElement("div"); card.className = "ev-passage" + (opts.big ? " big" : "") +
    (p.poem ? " poem" : "") + (p.portrait ? " portrait" : "") + (p.contain ? " contain" : "");
  if(p.image_id) card.insertAdjacentHTML("beforeend", `<div class="ev-pic">${imgOrEmoji(p.image_id, "📖", "ev-img", "ev-emoji")}</div>`);
  const txt = document.createElement("div"); txt.className = "ev-text";
  const lines = [];
  (p.lines || []).forEach((ln, i)=>{
    const s = document.createElement("span"); s.className = "ev-line"; s.dataset.idx = String(i);
    s.innerHTML = `<span class="ev-l-text">${ln.text}</span>`;
    s._src = ln.audio ? ("assets/Audio/" + ln.audio + "." + AUDIO_EXT) : null;
    txt.appendChild(s); txt.appendChild(document.createTextNode(" ")); lines.push(s);
  });
  card.appendChild(txt); card._lines = lines;
  return card;
}
function evMark(lines, idxs, qtype){
  (idxs || []).forEach(i=>{ const l = lines[i];
    if(!l || l.classList.contains("ev-hl") || l.classList.contains("ev-clue")) return;
    l.classList.add(qtype === "inference" ? "ev-clue" : "ev-hl");
    const t = document.createElement("span"); t.className = "ev-tag";
    t.textContent = qtype === "inference" ? "🔍 सुराग़" : "📖 उत्तर यहाँ लिखा है";
    l.insertBefore(t, l.firstChild); });
}
function evQtypeChip(qtype, label, icon){
  const el = document.createElement("div"); el.className = "ev-qtype " + (qtype === "inference" ? "inference" : "literal");
  const ic = icon || (qtype === "inference" ? "🔍" : "📖");
  const tx = label || (qtype === "inference" ? "अनुमान प्रश्न" : "सीधा प्रश्न");
  el.innerHTML = `<span class="ic">${ic}</span><span>${tx}</span>`;
  return el;
}

/* ---------- [story-fig] THE STORY PAGES' FRAME + NARRATED TEXT ----------
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

/* ---------- 12. SLIDE MODULES ---------- */
const SlideModules = {
  /* ================= MATCH_THE_PAIR =================
     Colourful bubbles scattered across the field. Each bubble carries ONE complete Hindi word plus
     a supporting icon — 1 icon for the एक form, 3 icons for the अनेक form — so a pre-reader can
     read the quantity even before the word. The child taps a word, then taps its एक/अनेक partner.

     A slide with data.demo runs the scripted teaching beat first (main instruction → tap
     instruction → hand-led guided example on the FIRST pair), then hands control to the child.
     Matched pairs pop and dock as a small pair card in the top-right tray; when the tray is full
     the whole set cheers and आगे activates (no auto-advance — the child sees every pair together).

     Feedback ladder on consecutive wrong second-taps (spec §7):
       1st  wiggle + soft retry sfx, first selection stays active, NO voice.
       2nd  wiggle + the first selection pulses + "फिर से देखिए…".
       3rd  the selection and its true partner pulse together, everything else fades, the pair is
            spoken aloud and the hand points at both — the child still makes the two taps. */
  MATCH_THE_PAIR: {
    mount(host, slide){
      const HUES = [["#FFD97A","#F3A81B"],["#A6DEFF","#4C9FE0"],["#FFB5C8","#EE7091"],
                    ["#BCEFA4","#5BC067"],["#D6C4FF","#9B7BE8"],["#FFC79A","#F3854A"]];
      const pairs  = slide.data.pairs.slice();
      const isDemo = !!slide.data.demo;
      const need   = pairs.length;
      if(isDemo) state.bubbleRetrySpoken = false; // one retry VO allowance for the whole bubble game

      state.ownsAudio = true;          // this module drives its own VO — keep autoPlayChain out
      state.attempts  = 0;
      state.locked    = true;          // stays locked through the intro/demo beat

      const A       = id => id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const slideA  = k  => audioFor(slide, k);
      const wordA   = w  => A(w && w.audio);

      /* ---- scaffold ---- */
      const wrap  = document.createElement("div"); wrap.className  = "mtp-stage";
      const field = document.createElement("div"); field.className = "mtp-field";
      const tray  = document.createElement("div"); tray.className  = "mtp-tray";
      tray.innerHTML = `<div class="mtp-tray-ttl">जोड़ियाँ</div>`;
      wrap.appendChild(field); wrap.appendChild(tray);
      host.appendChild(wrap);

      /* ---- one bubble per WORD (two per pair) ---- */
      oceanDecor(wrap);
      $("navBtn").style.display = "none";
      const bubbles = [];
      pairs.forEach((p, pi) => {
        [["s", p.s, 1], ["p", p.p, 3]].forEach(([num, w, count]) => {
          const b = document.createElement("div");
          b.className = "mtp-bubble";
          b.dataset.pairId = p.id; b.dataset.num = num;
          const icons = num === "p" ? triangleArt(String(p.icon || "").replace(/_s$/, "_p"), p.emoji, "bubble")
            : imgOrEmoji(p.icon, p.emoji, "mtp-ico", "mtp-ico-emo");
          b.innerHTML = `<span class="mtp-icons">${icons}</span><span class="mtp-word">${w.word_hi}</span>`;
          b.__word = w; b.__pair = p;
          b.addEventListener("click", ()=> onTap(b));
          field.appendChild(b); bubbles.push(b);
        });
      });

      /* Colour carries NO pairing information: a pair's two bubbles are deliberately given
         DIFFERENT hues, so the child must read the word rather than match by colour. */
      (function paint(){
        // bubbles[2k] / bubbles[2k+1] are the एक / अनेक halves of one pair — reshuffle until no
        // pair shares a hue (fallback stripe already satisfies that for any even bubble count).
        let hues = null;
        for(let t = 0; t < 200 && !hues; t++){
          const h = bubbles.map((_, i) => i % HUES.length).sort(()=> Math.random() - 0.5);
          let ok = true;
          for(let i = 0; i < h.length; i += 2) if(h[i] === h[i + 1]) ok = false;
          if(ok) hues = h;
        }
        if(!hues) hues = bubbles.map((_, i) => i % HUES.length);
        bubbles.forEach((b, i) => {
          b.style.setProperty("--c1", HUES[hues[i]][0]);
          b.style.setProperty("--c2", HUES[hues[i]][1]);
          b.style.setProperty("--floatDur", (4.2 + Math.random() * 1.8).toFixed(2) + "s");
          b.style.setProperty("--floatDelay", (-Math.random() * 3).toFixed(2) + "s");
        });
      })();

      /* ---- scatter: a jittered grid, with a partner-separation constraint so a pair never
             lands side by side (spec §1: "matching words should not appear next to each other") ---- */
      function layout(){
        const W = field.clientWidth, H = field.clientHeight, n = bubbles.length;
        if(!W || !H) return;
        let cols = Math.max(2, Math.min(n, Math.round(Math.sqrt(n * W / H))));
        let rows = Math.ceil(n / cols);
        while(rows > 1 && (H / rows) < 130 && cols < n){ cols++; rows = Math.ceil(n / cols); }
        const cw = W / cols, ch = H / rows;
        const d  = Math.max(112, Math.min(178, Math.floor(Math.min(cw, ch) * 0.88)));

        const cells = [];
        for(let r = 0; r < rows; r++) for(let c = 0; c < cols; c++) cells.push({r, c});
        const far = (a, b) => Math.max(Math.abs(a.r - b.r), Math.abs(a.c - b.c)) >= 2;
        let order = null;
        for(let t = 0; t < 400 && !order; t++){
          const sh = cells.slice().sort(()=> Math.random() - 0.5).slice(0, n);
          let ok = true;
          for(let i = 0; i < n && ok; i++) for(let j = i + 1; j < n && ok; j++){
            if(bubbles[i].dataset.pairId === bubbles[j].dataset.pairId && !far(sh[i], sh[j])) ok = false;
          }
          if(ok) order = sh;
        }
        if(!order) order = cells.slice().sort(()=> Math.random() - 0.5).slice(0, n);

        bubbles.forEach((b, i) => {
          const cell = order[i];
          // fill the whole cell with jitter, plus a per-column vertical stagger, so the field
          // reads as a scatter of bubbles rather than a table of them
          const jx = (Math.random() - .5) * Math.max(0, cw - d - 6);
          const jy = (Math.random() - .5) * Math.max(0, ch - d - 6);
          const stagger = ((cell.c % 2) ? 1 : -1) * Math.min(22, Math.max(0, (ch - d) / 3));
          const x  = Math.min(W - d, Math.max(0, cell.c * cw + (cw - d) / 2 + jx));
          const y  = Math.min(H - d, Math.max(0, cell.r * ch + (ch - d) / 2 + jy + stagger));
          b.style.width = b.style.height = d + "px";
          b.style.left  = Math.round(x) + "px";
          b.style.top   = Math.round(y) + "px";
          b.style.setProperty("--ico", Math.round(d * 0.205) + "px");
          const wEl = b.querySelector(".mtp-word");
          const len = (b.__word.word_hi || "").length || 1;
          let fs = Math.round(Math.min(d * 0.165, (d * 0.78) / (len * 0.50)));
          wEl.style.fontSize = Math.max(13, fs) + "px";
          // hard guard: shrink until the word actually fits the bubble's usable width
          let guard = 0;
          while(wEl.scrollWidth > d * 0.80 && fs > 12 && guard++ < 24){ fs--; wEl.style.fontSize = fs + "px"; }
        });
      }
      nextFrame(()=>{ layout(); startDrift(); });

      /* [r41] GENTLE DRIFT, COLLISIONS AND A RIPPLE WHERE THEY TOUCH.
         The bubbles used to bob on their own CSS keyframe and never meet. They now share one loop:
         each drifts slowly, bounces off the walls and off the others, and a ring of water opens
         wherever two of them touch. Speed is deliberately tiny — around 10-18 px a second, so a
         bubble takes the better part of a minute to cross the field — because a child has to be
         able to read a word while it moves. A selected bubble keeps drifting and remains inside the
         same collision simulation, so other bubbles can never pass through or overlap it. Only
         short feedback/solve animations temporarily hold a bubble still.

         SMOOTHNESS, learnt the hard way: the first cut wrote left/top every frame AND read
         offsetWidth / clientWidth back inside the same loop. Each of those reads forces the browser
         to redo layout right after the write, so all six bubbles re-laid-out on every single frame
         and the whole thing stuttered like a low frame rate. Now every measurement is taken once up
         front, and the drift rides the CSS `translate` PROPERTY — which is its own compositable
         property, separate from `transform`, so the select / burst / fly transforms still work
         untouched and nothing is laid out again per frame. */
      function startDrift(){
        if(matchMedia("(prefers-reduced-motion:reduce)").matches) return;
        if(!field.clientWidth || !bubbles[0] || !bubbles[0].offsetWidth){ nextFrame(startDrift); return; }
        /* every measurement taken ONCE — nothing below reads layout again */
        let W = field.clientWidth, H = field.clientHeight;
        const SZ = new Map(bubbles.map(b => [b, b.offsetWidth]));
        const remeasure = ()=>{ W = field.clientWidth; H = field.clientHeight;
          bubbles.forEach(b => SZ.set(b, b.offsetWidth)); };
        window.addEventListener("resize", remeasure);
        oceanAddCleanup(()=> window.removeEventListener("resize", remeasure));
        const held = b => b.classList.contains("ok") || b.classList.contains("burst") || b.classList.contains("fly")
                       || b.classList.contains("done") || b.classList.contains("wiggle");
        bubbles.forEach(b => {
          const a = Math.random() * Math.PI * 2, sp = 10 + Math.random() * 8;
          const bx = parseFloat(b.style.left) || 0, by = parseFloat(b.style.top) || 0;
          b.__d = { x: bx, y: by, bx, by, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp };
        });
        let last = performance.now();
        (function step(now){
          if(!onScreen()) return;                       // the slide went away; stop for good
          requestAnimationFrame(step);
          const dt = Math.min(0.05, (now - last) / 1000); last = now;
          if(!W || !H) return;
          const live = bubbles.filter(b => b.__d && alive(b) && !held(b));
          for(const b of live){
            const d = b.__d, s = SZ.get(b);
            d.x += d.vx * dt; d.y += d.vy * dt;
            if(d.x < 0)      { d.x = 0;     d.vx =  Math.abs(d.vx); }
            if(d.y < 0)      { d.y = 0;     d.vy =  Math.abs(d.vy); }
            if(d.x > W - s)  { d.x = W - s; d.vx = -Math.abs(d.vx); }
            if(d.y > H - s)  { d.y = H - s; d.vy = -Math.abs(d.vy); }
          }
          for(let i = 0; i < live.length; i++) for(let j = i + 1; j < live.length; j++){
            const A = live[i], B = live[j], a = A.__d, c = B.__d;
            const ra = SZ.get(A) / 2, rb = SZ.get(B) / 2;
            const ax = a.x + ra, ay = a.y + ra, bx = c.x + rb, by = c.y + rb;
            const dx = bx - ax, dy = by - ay, dist = Math.hypot(dx, dy), min = ra + rb;
            if(dist >= min || dist === 0) continue;
            const nx = dx / dist, ny = dy / dist, push = (min - dist) / 2 + 0.5;
            a.x -= nx * push; a.y -= ny * push; c.x += nx * push; c.y += ny * push;
            /* equal masses: swap the speed along the line of contact. No energy is added, so the
               field never winds itself up into something fast. */
            const va = a.vx * nx + a.vy * ny, vb = c.vx * nx + c.vy * ny;
            a.vx += (vb - va) * nx; a.vy += (vb - va) * ny;
            c.vx += (va - vb) * nx; c.vy += (va - vb) * ny;
          }
          /* the CSS translate property, not transform — composited, and it leaves transform free
             for the select / burst / fly states */
          for(const b of live){
            b.style.translate = (b.__d.x - b.__d.bx).toFixed(2) + "px " + (b.__d.y - b.__d.by).toFixed(2) + "px";
          }
        })(last);
      }

      /* ---- helpers ---- */
      const alive  = b => !b.classList.contains("done");
      const find   = (pid, num) => bubbles.find(b => b.dataset.pairId === pid && b.dataset.num === num && alive(b));
      const pulse  = (el, ms) => { if(!el) return;
        el.classList.remove("pulse"); void el.offsetWidth; el.classList.add("pulse");
        later(()=> el.classList.remove("pulse"), ms || 900); };
      const sparkAt = (el) => {
        const stg = document.querySelector(".slide-stage"); if(!stg) return;
        const r = el.getBoundingClientRect(), sr = stg.getBoundingClientRect();
        const sc = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--scale")) || 1;
        const cx = (r.left - sr.left) / sc + r.width / sc / 2, cy = (r.top - sr.top) / sc + r.height / sc / 2;
        const emo = ["⭐","✨","🌟","💫"];
        for(let i = 0; i < 9; i++){
          const s = document.createElement("span"); s.className = "spark"; s.textContent = emo[i % 4];
          const ang = Math.PI * 2 * (i / 9) + Math.random() * .4, dist = 46 + Math.random() * 62;
          s.style.left = cx + "px"; s.style.top = cy + "px";
          s.style.setProperty("--dx", (Math.cos(ang) * dist).toFixed(0) + "px");
          s.style.setProperty("--dy", (Math.sin(ang) * dist).toFixed(0) + "px");
          stg.appendChild(s); setTimeout(()=> s.remove(), 950);
        }
      };
      /* Reference-style soap-bubble burst: the shell deforms and vanishes, while a clean
         circular spray of tiny iridescent droplets expands from the exact bubble centre. */
      const bubbleBurstAt = (el) => {
        const stg = document.querySelector(".slide-stage"); if(!stg || !el) return;
        const r = el.getBoundingClientRect(), sr = stg.getBoundingClientRect();
        const sc = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--scale")) || 1;
        const fx = document.createElement("span"); fx.className = "bubble-pop-fx";
        fx.style.left = ((r.left - sr.left + r.width / 2) / sc) + "px";
        fx.style.top  = ((r.top  - sr.top  + r.height / 2) / sc) + "px";
        const ring = document.createElement("span"); ring.className = "bubble-pop-ring"; fx.appendChild(ring);
        const n = 22;
        for(let i = 0; i < n; i++){
          const d = document.createElement("span"); d.className = "bubble-droplet";
          const ang = Math.PI * 2 * (i / n) + (Math.random() - .5) * .22;
          const dist = 68 + Math.random() * 72;
          d.style.setProperty("--dx", (Math.cos(ang) * dist).toFixed(1) + "px");
          d.style.setProperty("--dy", (Math.sin(ang) * dist).toFixed(1) + "px");
          d.style.setProperty("--rot", (ang * 180 / Math.PI).toFixed(1) + "deg");
          d.style.setProperty("--sz", (5 + Math.random() * 8).toFixed(1) + "px");
          d.style.setProperty("--delay", (Math.random() * .055).toFixed(3) + "s");
          fx.appendChild(d);
        }
        stg.appendChild(fx); setTimeout(()=> fx.remove(), 900);
      };
      /* hold=true places the card (so it can be measured as the flight target) but leaves it
         hidden until the two bubbles actually land on it */
      const addPairCard = (p, hold) => {
        const c = document.createElement("div"); c.className = "mtp-pair-card";
        const oneArt = imgOrEmoji(p.icon, p.emoji, "mpc-icon", "mpc-icon-emo");
        const manyArt = triangleArt(String(p.icon || "").replace(/_s$/, "_p"), p.emoji, "result");
        c.innerHTML = `<span class="mpc-side mpc-one"><span class="mpc-art">${oneArt}</span><span class="mpc-w">${p.s.word_hi}</span></span>` +
                      `<span class="mpc-bridge"><span class="mpc-arrow">→</span></span>` +
                      `<span class="mpc-side mpc-many"><span class="mpc-art">${manyArt}</span><span class="mpc-w">${p.p.word_hi}</span></span>` +
                      "";
        tray.appendChild(c);
        if(!hold) nextFrame(()=> c.classList.add("in"));
        return c;
      };

      /* ---- interaction state ---- */
      /* [r36] MATCH_THE_PAIR was the one module r17 missed. Its opening beat rewrites the heading
         and plays "पहले एक शब्द पर…" from a timer ~2s after mount, and NOTHING checked that this
         slide was still on screen — so finishing the bubble game quickly carried that heading and
         that voice onto the NEXT slide, where they belong to no game at all. Every deferred step
         below now checks that this mount is still in the document. `onScreen` rather than
         `alive`: that name is already taken here for "this bubble has not been solved yet". */
      const onScreen = ()=> wrap.isConnected;
      const later = (fn, ms)=> setTimeout(()=>{ if(onScreen()) fn(); }, ms);

      let sel = null, wrongStreak = 0, solved = 0, guide = null, demoGuide = false;
      const idle = oceanIdle(wrap,isDemo ? 'instructionBubble' : null,()=>{
        const target=sel ? find(sel.dataset.pairId,sel.dataset.num==='s'?'p':'s') : bubbles.find(alive);
        if(!target)return;
        target.classList.add('pulse-hold');
        return ()=>target.classList.remove('pulse-hold');
      });

      const clearGuide = () => {
        bubbles.forEach(b => b.classList.remove("faded", "pulse-hold"));
        guide = null; demoGuide = false; stopNudge();
      };
      const armIdle = () => {
        if(onScreen() && !state.locked) idle.arm();
      };

      /* ---- the one correct-pair path (child match AND guided demo) ----
         The match must feel INSTANT: the moment the second tap lands both bubbles bounce green,
         then they fly across into the tray and become the pair card. The VO rides alongside the
         animation instead of gating it — a child who solved it should not wait to be told so. */
      function settle(b1, b2, withSahi, after){
        state.locked = true; stopNudge(); idle.clear();
        const p = b1.__pair;
        bubbleBurstAt(b1); bubbleBurstAt(b2);
        [b1, b2].forEach(b => { b.classList.remove("sel", "pulse-hold"); b.classList.add("ok", "burst"); });
        sfxPop();                             // pair success uses only the clean bubble-pop sound
        /* A pair gets the physical pop only. Spoken praise is reserved for completing the whole
           bubble screen, so three matches never become three repetitive praise lines. */
        let voiceDone=true,visualDone=false;
        const resume=()=>{if(!onScreen() || !voiceDone || !visualDone)return;
          if(solved>=need)finish();else{state.locked=false;if(after)after();armIdle();}};
        const BURST = 720;
        later(()=>{
          const card = addPairCard(p, false);
          [b1, b2].forEach(b => { b.classList.add("done"); b.style.display = "none"; });
          solved++;
          GameBus.emit("gender_pair_match", { slide_id: slide.id, phase: slide.phase,
            value: true, pair: p.id, attempts: state.attempts });
          visualDone=true;resume();
        }, BURST);
      }

      /* ---- spec §7 wrong ladder ---- */
      function wrongFeedback(b){
        state.locked = true; idle.clear();
        oceanRetrySfx();
        b.classList.remove("wiggle"); void b.offsetWidth; b.classList.add("wiggle","ocean-wrong");
        later(()=>{
          b.classList.remove("wiggle","ocean-wrong");
          const resumeWrong=()=>{if(onScreen()){state.locked=false;armIdle();}};
          if(!state.bubbleRetrySpoken){state.bubbleRetrySpoken=true;oceanSay('retry',resumeWrong);}else resumeWrong();
        }, 700);
      }

      function revealGuide(){
        const first   = sel;
        const partner = first && find(first.dataset.pairId, first.dataset.num === "s" ? "p" : "s");
        if(!first || !partner){ state.locked = false; return; }
        state.scaffoldLevel = Math.max(state.scaffoldLevel, 3);
        state.hintUsed = true;
        first.classList.remove("sel"); sel = null;                    // the child re-taps BOTH
        guide = new Set([first, partner]);
        /* Keep every option fully visible during terminal help. The correct pair pulses, but the
           child can still compare it against the unchanged surrounding bubbles. */
        first.classList.add("pulse-hold"); partner.classList.add("pulse-hold");
        setSwMood("hint");
        const p = first.__pair;
        playChain([slideA("listen"), wordA(p.s), wordA(p.p), slideA("now_tap")].filter(Boolean), 0, ()=>{
          if(!onScreen()) return;
          state.locked = false;
          pointNudgeAt(first);
          later(()=>{ if(guide && !sel) pointNudgeAt(partner); }, 1200);
        });
      }

      /* ---- taps ---- */
      function onTap(b){
        if(state.locked || !alive(b)) return;
        if(guide && !guide.has(b)) return;                 // guided rescue: only the two shown bubbles
        stopNudge();
        if(sel === b){ b.classList.remove("sel"); sel = null; wrongStreak = 0; armIdle(); return; }
        if(!sel){                                          // first of the two taps
          sfxTap(); sel = b; b.classList.add("sel"); wrongStreak = 0;
          // Instruction and feedback VO are supplied by OCEAN_VO; selection stays silent.
          if(guide){ const other = [...guide].find(x => x !== b); if(other) pointNudgeAt(other); }
          else armIdle();
          return;
        }
        state.attempts++;
        if(b.dataset.pairId === sel.dataset.pairId){       // ✓ pair
          const a = sel; sel = null; wrongStreak = 0;
          const wasGuided = !!guide, wasDemo = demoGuide;
          clearGuide();
          settle(a, b, wasDemo);                       // the demo pair earns the spoken "सही" line
          if(wasGuided && !wasDemo) state.scaffoldLevel = Math.max(state.scaffoldLevel, 3);
        } else {                                           // ✗ pair
          wrongStreak++;
          GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase,
            attempts: state.attempts, streak: wrongStreak });
          wrongFeedback(b);
        }
      }

      /* ---- level complete (spec §8) ---- */
      function finish(){
        if(!onScreen()) return;
        state.locked = true; stopNudge(); clearGuide(); idle.clear();
        $("promptText").textContent = "सभी जोड़ियाँ पूरी हुईं!";
        tray.classList.add("done");
        wrap.classList.add("fin", "result-story");       // every pair now assembles as a visual transformation
        tray.querySelector(".mtp-tray-ttl").textContent = "सभी जोड़ियाँ";
        const cards = [...tray.querySelectorAll(".mtp-pair-card")];
        cards.forEach((card, i)=> later(()=>{
          card.classList.add("story-in");
          if(i === cards.length - 1) later(()=>confettiCannon(false), 1900);
        }, 180 + i * 760));
        /* Speak the requested completion line only after the third card and confetti sound have
           finished, so the child hears it clearly instead of under overlapping effects. */
        later(()=>oceanSay("resultComplete"), 5300);
        setSwMood("celebrate");
        /* Three completed pairs are the learning result, not a passing frame. Hold them long
           enough for a young reader to scan all three before the inter-game swim begins. */
        /* The third card finishes its full join/shine beat at about 3.5s. Keep the complete set
           untouched for another three seconds so a young reader can process every pair. */
        later(()=>completeSlide(true),7600);
      }

      /* ---- opening beats (spec §2-4) ---- */
      const tapOST = audioText(slide, "tap_hint") || "पहले एक शब्द पर, फिर उसकी जोड़ी पर टैप कीजिए।";
      state.replayAudio = isDemo ? ()=>{idle.clear();oceanSay('instructionBubble',armIdle);} : null;

      function openThenPlay(){
        if(!onScreen()) return;
        /* Every bubble level keeps the written instruction visible. Only the first level voices it. */
        $("promptText").textContent=slide.prompt_hi || "";
        if(!isDemo){
          /* Level two opens directly: no repeated instruction text and no instruction VO. */
          state.locked=false;armIdle();return;
        }
        /* The first instruction introduces the mechanic. One complete pair gives two gentle
           pulses (about two seconds) while that VO is speaking; everything else stays fully sharp
           and at normal speed. Only after the instruction ends does the board unlock for play. */
        const introPair=pairs[0], introOne=find(introPair.id,"s"), introMany=find(introPair.id,"p");
        [introOne,introMany].forEach(b=>b&&b.classList.add("intro-pulse"));
        later(()=>[introOne,introMany].forEach(b=>b&&b.classList.remove("intro-pulse")),2000);
        oceanSay('instructionBubble',()=>{
          if(!onScreen())return;
          [introOne,introMany].forEach(b=>b&&b.classList.remove("intro-pulse"));
          state.locked=false;armIdle();
        });
        return;
        setSwMood("talk");
        $("promptText").textContent = slide.prompt_hi || "";
        play(slideA("prompt"), ()=>{});
        const p0 = pairs[0], b1 = find(p0.id, "s"), b2 = find(p0.id, "p");
        // paced off PACE so the child can actually follow each beat of the demonstration
        pulse(b1, 900);                                            // §2: एक bubble pulses…
        later(()=> pulse(b2, 900), PACE.lineStep);                  //     …then its अनेक partner
        later(()=>{
          $("promptText").textContent = tapOST;
          play(slideA("tap_hint"), ()=>{});
          if(!isDemo){ later(()=>{ state.locked = false; armIdle(); }, PACE.tail); return; }
          // §3: the hand shows WHERE the pair is — it no longer taps for the child.
          //     The old §4 auto-complete called settle() itself, so a child who touched गुब्बारा
          //     while the board was still locked saw BOTH bubbles pop a moment later and read it
          //     as "one tap burst the pair". A pair may only burst when the child has selected
          //     both halves, so the demo now ends by handing those two taps over.
          pulse(b1, 800);
          later(()=> pointNudgeAt(b1), 800);
          later(()=> pulse(b2, 800), 2400);
          later(()=> pointNudgeAt(b2), 3200);
          later(()=>{                                               // §4: the child completes it
            stopNudge();
            guide = new Set([b1, b2]); demoGuide = true;            // only these two are live
            bubbles.forEach(b => { if(alive(b) && !guide.has(b)) b.classList.add("faded"); });
            b1.classList.add("pulse-hold"); b2.classList.add("pulse-hold");
            setSwMood("point");
            play(slideA("now_tap"), ()=>{ if(!onScreen()) return; state.locked = false; pointNudgeAt(b1); });
          }, 4400);
        }, PACE.lineStep + 1600);
      }
      nextFrame(()=> nextFrame(()=>{ if(onScreen()) openThenPlay(); }));
    }
  },

  /* ================= PICK_VACHAN_WORD — deck pp.12-17 =================
     "सही शब्द चुनिए।"  A source word with its quantity picture, an arrow, and an empty drop box
     carrying the TARGET quantity picture + its एक/अनेक pill. Three word options sit below; the
     child taps one. Tapping the source word replays that word's VO (deck: "If child tap the word
     … its VO must play").

     Correct → Swiftee's "शाबाश! आपने सही शब्द चुना — X।", the card locks into the box, the other
     options fade out (deck).
     Wrong (deck p.18):
       1st  the card wiggles and bounces back. No lock, no red cross, NO VO, nothing else moves.
       2nd  wiggles back, the source word pulses once, the quantity picture pulses too, no option
            is highlighted, and the authored retry line plays.
       3rd  wiggles back and the CORRECT card pulses; the child still taps it, and that tap gets
            the word's VO + correct sfx + confetti. */
  PICK_VACHAN_WORD: {
    mount(host, slide){
      const d = slide.data;
      const qty = (w, n) => w.group
        ? imgOrEmoji(w.img, w.emoji, "pvw-group", "pvw-emo")
        : Array.from({length: n}, ()=> imgOrEmoji(w.img, w.emoji, "", "pvw-emo")).join("");

      /* [r26] BOTH sides carry their एक / अनेक pill. Only the target was labelled, so the screen
         named the quantity the child is moving TO but left the one they are moving FROM unnamed —
         and the whole question is a comparison between the two. Derived from the count rather than
         read from the card, so a label can never disagree with the pictures beside it. */
      const vachanOf = w => w.label || (Number(w.count) === 1 ? "एक" : "अनेक");

      const wrap = document.createElement("div"); wrap.className = "pvw";
      wrap.innerHTML =
        '<div class="pvw-row">' +
          '<div class="pvw-side">' +
            '<div class="pvw-pill">' + vachanOf(d.source) + '</div>' +
            '<div class="pvw-qty src-qty">' + qty(d.source, d.source.count) + '</div>' +
            '<div class="pvw-src">' + d.source.word_hi + '</div>' +
          '</div>' +
          '<div class="pvw-arrow">→</div>' +
          '<div class="pvw-side">' +
            '<div class="pvw-pill">' + vachanOf(d.target) + '</div>' +
            '<div class="pvw-qty tgt-qty">' + qty(d.target, d.target.count) + '</div>' +
            '<div class="pvw-box"></div>' +
          '</div>' +
        '</div>' +
        '<div class="pvw-opts"></div>';
      host.appendChild(wrap);

      const srcEl  = wrap.querySelector(".pvw-src");
      const srcQty = wrap.querySelector(".src-qty");
      const tgtQty = wrap.querySelector(".tgt-qty");
      const box    = wrap.querySelector(".pvw-box");
      const optRow = wrap.querySelector(".pvw-opts");

      const A = id => id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      state.attempts = 0; state.locked = false;
      $("navBtn").style.display = "none";          // tap-to-answer: the slide advances itself
      state.replayAudio = ()=> play(audioFor(slide, "prompt"), ()=>{});
      srcEl.onclick = ()=>{ if(state.locked) return; sfxTap(); play(A(d.source.audio), ()=>{}); };

      const opts = [];
      d.options.slice().sort(()=> Math.random() - 0.5).forEach(o => {
        const el = document.createElement("div"); el.className = "pvw-opt";
        el.textContent = o.word_hi; el.__opt = o;
        el.onclick = ()=> pick(el);
        optRow.appendChild(el); opts.push(el);
      });
      const correctEl = ()=> opts.find(e => e.__opt.correct);

      const pulse = (el, ms)=>{ el.classList.remove("pulse"); void el.offsetWidth; el.classList.add("pulse");
        setTimeout(()=> el.classList.remove("pulse"), ms || 1900); };

      function pick(el){
        if(state.locked) return;
        state.attempts++;
        if(el.__opt.correct){
          state.locked = true;
          sfxCorrect(); confettiCannon(); setSwMood("celebrate");
          el.classList.add("taken");
          box.textContent = el.__opt.word_hi; box.classList.add("filled");     // locks into the drop box
          opts.forEach(o => { if(o !== el) o.classList.add("gone"); });        // the rest fade
          GameBus.emit("vachan_recognise_first_try", {
            slide_id: slide.id, phase: slide.phase, value: true,
            first_try: state.attempts === 1, attempts: state.attempts,
            latency_ms: Date.now() - state.slideStart
          });
          idle.clear();
          const after = ()=> setTimeout(()=> completeSlide(state.attempts === 1), PACE.tail);
          if(state.scaffoldLevel >= 3) playChain([A(el.__opt.audio)].filter(Boolean), 0, after);
          else voSay(audioFor(slide, "correct"), "correct", after);   // praise, spoken even before this screen is recorded
          return;
        }
        // ---- wrong ----
        state.locked = true;
        idle.clear();
        oceanRetrySfx();
        el.classList.remove("wiggle"); void el.offsetWidth; el.classList.add("wiggle");
        GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
        setTimeout(()=>{
          el.classList.remove("wiggle");
          if(state.attempts === 1){ state.locked = false; return; }            // silent, nothing else moves
          if(state.attempts === 2){
            state.scaffoldLevel = Math.max(state.scaffoldLevel, 2);
            setSwMood("tryagain");
            pulse(srcEl); pulse(srcQty);                                       // no option highlighted
            voSay(audioFor(slide, "retry"), "retry", ()=>{ state.locked = false; idle.arm(); });
            return;
          }
          state.scaffoldLevel = Math.max(state.scaffoldLevel, 3);              // 3rd: show which one
          state.hintUsed = true;
          setSwMood("hint");
          const ce = correctEl(); if(ce) ce.classList.add("lit");
          pulse(tgtQty);
          state.locked = false;                                                // the child still taps it
          idle.arm();
        }, 620);
      }

      /* [r39] the same two idle beats the ocean games use: re-speak the instruction after 7s of
         doing nothing, and 7s after that draw the eye to the word being changed. The hint never
         points at the correct option — that stays the job of the 3-attempt ladder above. */
      const idle = oceanIdle(wrap, "instructionPick", ()=>{
        pulse(srcEl); pulse(srcQty);
        return ()=>{};
      });
      /* oceanIdle only starts counting when armed — the ocean games arm it once their instruction
         has finished. This screen does not own its audio (mountSlide speaks the prompt), so arm it
         here; the timer already defers itself while a clip is sounding. */
      idle.arm();

      setSwMood("point");
      startNudge(slide, srcEl);
    }
  },

  /* ================= FILL_VACHAN_DRAG — part 2, levelled =================
     Built to the demo `preview.html`: the activity is a small game of its OWN, with स्तर (levels)
     inside one slide rather than one slide per question.

       · a level holds several questions; a question is TWO sentence cards, each missing one word
       · the bank holds exactly the two answers (एक form / अनेक form), shuffled
       · both blanks are live from the start, and there is no "जाँचें" button — getting both right
         IS the check: star, confetti, both sentences read back, next question
       · finishing a level shows a स्तर-पूरा panel with an अगला स्तर button, because the next level
         moves the blank to a new place in the sentence and that deserves a beat
       · after the last level a summary of every pair is shown and आगे opens

     Difficulty climbs by what the child has to read to decide: level 1 cues on एक / बहुत-से before
     the blank, level 2 moves the word to a new place in the sentence. [r55] The verb-agreement level
     (रही है / रही हैं) that used to sit between them was removed, and the old level 3 is now स्तर 2.

     [r55] Which sentence sits on top is NOT fixed. It used to be — the एक sentence always above, the
     अनेक sentence always below — so a child could drop the एक word on top and the अनेक word below
     every time without reading either sentence. See `oneOnTop` below.

     Wrong drops keep the three-step ladder: silent bounce → the sentence pulses and is re-read →
     the correct tile and the blank glow and the answer is named, child still performs the drag. */
  FILL_VACHAN_DRAG: {
    mount(host, slide){
      const d = slide.data;
      const levels = d.levels || [{ name: "", questions: d.questions || [] }];
      const totalQ = levels.reduce((n, l) => n + l.questions.length, 0);
      const A = id => id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;

      state.ownsAudio = true; state.attempts = 0; state.locked = true;
      state.fillRetrySpoken = false; // one spoken retry allowance across every fill level
      $("navBtn").style.display = "none";
      setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);

      let li = 0, qi = 0, stars = 0;

      /* [r55] For each question, does the एक sentence go on top? Random per question, but never the
         same for a whole level — a level of three always has at least one question each way — so
         neither "एक goes on top" nor a strict alternation can stand in for reading the sentence.
         Kept local to this mount rather than written onto the lesson data, so going back and
         returning to the game deals a fresh order. */
      const oneOnTop = levels.map(L => {
        const n = L.questions.length;
        let o;
        do { o = Array.from({ length: n }, () => Math.random() < .5); }
        while(n > 1 && o.every(v => v === o[0]));
        return o;
      });

      const wrap = document.createElement("div"); wrap.className = "fvd";
      wrap.innerHTML =
        '<div class="fvd-top">' +
          '<div class="fvd-level"></div>' +
          '<div class="fvd-bar"><div class="fvd-bar-fill"></div></div>' +
          '<div class="fvd-stars"></div>' +
        '</div>' +
        '<div class="fvd-body"></div>';
      host.appendChild(wrap);
      const alive = ()=> wrap.isConnected;   // a stale timer from a previous mount must not act
      const later = (fn, ms)=> setTimeout(()=>{ if(alive()) fn(); }, ms);
      const levelLbl = wrap.querySelector(".fvd-level");
      const bar      = wrap.querySelector(".fvd-bar-fill");
      const starLbl  = wrap.querySelector(".fvd-stars");
      const body     = wrap.querySelector(".fvd-body");
      oceanDecor(wrap);
      let nextHint=()=>{};
      let firstDropDone=false, introGhostCleanup=()=>{};
      oceanAddCleanup(()=>introGhostCleanup());
      /* [r56] The idle reminder may re-speak the instruction only on a level's OPENING question,
         the one place the instruction VO belongs. On the questions after it the reminder skips the
         voice and goes straight to the visual hint. */
      const idle=oceanIdle(wrap,()=>qi===0 ? 'instructionFill' : null,()=>nextHint());

      const paintTop = ()=>{
        const L = levels[li];
        levelLbl.textContent = (L.name ? L.name + " · " : "") + (qi + 1) + "/" + L.questions.length;
        bar.style.width = Math.round(stars / totalQ * 100) + "%";
        starLbl.textContent = "★ " + stars;
      };

      /* ---------- one question ---------- */
      function renderQuestion(){
        if(!alive()) return;
        idle.clear();
        introGhostCleanup(); introGhostCleanup=()=>{};
        const q = levels[li].questions[qi];
        const placed = [null, null];
        let wrong = 0;
        state.locked = true;
        /* [r56] The instruction text stays on screen for the whole game, in every level and on every
           question. Only its VO is limited to the start of a level (below). */
        $("promptText").textContent=slide.prompt_hi || "";
        paintTop();

        const half = (text, slot)=>{
          const p = String(text).split("{blank}");
          return `<div class="fvd-card" data-slot="${slot}"><span>${hlText(p[0])}</span>` +
                 `<span class="fvd-blank dd-zone" data-slot="${slot}"></span>` +
                 `<span>${hlText(p[1] || "")}</span></div>`;
        };
        /* slot 0 is the top card and slot 1 the bottom one. The एक sentence is `q.a` and the अनेक
           sentence `q.b`; which of them takes the top slot is this question's draw. Everything after
           this — the drop check, the hint ghost, the green on the placed word — works from the
           slot a tile is aimed at, so it follows the sentence wherever it was put. */
        const top = oneOnTop[li][qi];
        const slotOf = { one: top ? 0 : 1, many: top ? 1 : 0 };
        body.innerHTML =
          '<div class="fvd-cards">' + (top ? half(q.a, 0) + half(q.b, 1) : half(q.b, 0) + half(q.a, 1)) + '</div>' +
          '<div class="fvd-bank"><div class="fvd-tiles"></div></div>';

        const cards  = [...body.querySelectorAll(".fvd-card")];
        const blanks = [...body.querySelectorAll(".fvd-blank")];
        const row    = body.querySelector(".fvd-tiles");

        const words = [{ w: q.one,  slot: slotOf.one,  form: "one",  audio: q.oneAudio },
                       { w: q.many, slot: slotOf.many, form: "many", audio: q.manyAudio }];
        if(Math.random() < 0.5) words.reverse();
        const tiles = words.map(o => {
          const t = document.createElement("div"); t.className = "fvd-tile";
          t.textContent = o.w; t.dataset.word = o.w; t.dataset.slot = String(o.slot); t.dataset.form = o.form; t.__a = o.audio;
          row.appendChild(t); return t;
        });

        const pulse = (el, ms)=>{ if(!el) return; el.classList.remove("pulse"); void el.offsetWidth;
          el.classList.add("pulse"); later(()=> el.classList.remove("pulse"), ms || 1900); };
        const clearGlow = ()=> tiles.forEach(t => t.classList.remove("lit"));
        nextHint=(iterations)=>{
          const tile=tiles.find(t=>!t.classList.contains('used'));
          return tile ? oceanGhost(tile,blanks[+tile.dataset.slot],wrap,iterations) : ()=>{};
        };

        function fill(slot, tile){
          state.locked=true;idle.clear();
          placed[slot] = tile.dataset.word; wrong = 0; clearGlow();
          blanks[slot].textContent = tile.dataset.word;
          blanks[slot].classList.add("filled");
          cards[slot].classList.add("done");
          tile.classList.add("used");
          paintTop();
          sfxCorrect();
          GameBus.emit("gender_pair_match", { slide_id: slide.id, phase: slide.phase,
            value: true, level: li + 1, question: qi + 1, blank: slot, form: tile.dataset.form,
            one_on_top: top, attempts: state.attempts });
          /* Correct blanks keep the short chime only. Spoken praise and confetti are reserved for
             completing the whole level, so a three-question level never repeats praise six times. */
          later(()=>{
            if(!alive()) return;
            if(!(placed[0] && placed[1])){ state.locked = false; idle.arm(); return; }
            stars++; paintTop();
            later(nextQuestion,850);
          },650);
        }

        function wrongDrop(slot, tile){
          state.locked = true; idle.clear(); oceanRetrySfx(); wrong++;
          tile.classList.remove("wiggle"); void tile.offsetWidth; tile.classList.add("wiggle","ocean-wrong");
          GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, level: li + 1, streak: wrong });
          later(()=>{
            tile.classList.remove("wiggle","ocean-wrong");
            const resume=()=>{if(alive()){state.locked=false;idle.arm();}};
            if(!state.fillRetrySpoken){state.fillRetrySpoken=true;oceanSay('retry',resume);}else resume();
          }, 1200);
        }

        tiles.forEach(tile => makeDraggable(tile, (zone, t)=>{
          if(!alive() || state.locked || zone.classList.contains("filled")) return;
          if(!firstDropDone){firstDropDone=true;introGhostCleanup();introGhostCleanup=()=>{};}
          const slot = +zone.dataset.slot;
          state.attempts++;
          if(+t.dataset.slot === slot) fill(slot, t); else wrongDrop(slot, t);
        }, { onTap: ()=> { if(!state.locked) idle.arm(); } }));

        setSwMood("talk");
        /* The speaker chip replays the instruction on demand on every question — the text is always
           on screen, so the child can always hear it. That is the child's choice, not an automatic
           VO, so it does not conflict with the rule below. */
        state.replayAudio = ()=>{idle.clear();oceanSay('instructionFill',()=>idle.arm());};
        /* [r56] The instruction VO plays at the START OF EVERY LEVEL — स्तर 1 and स्तर 2 each open
           with it — and on none of the questions inside a level. It used to play only once, at the
           very start of स्तर 1, so स्तर 2 began in silence. */
        if(qi===0){
          oceanSay('instructionFill', ()=>{
            if(!alive()) return;
            /* The demonstration ghost belongs to the first level only, where the drag is being
               taught; it repeats until the child's first real drop and never fills an answer. By
               स्तर 2 the child has already dropped, so an endless ghost there would never be
               cleared by a drop — it is deliberately not started again. */
            if(li===0) introGhostCleanup=nextHint(Infinity);
            state.locked = false; setSwMood("point"); idle.arm();
          });
        }else{
          /* the questions after a level's first one open directly, without the instruction VO */
          state.locked=false;setSwMood("point");idle.arm();
        }
      }

      /* ---------- between levels ---------- */
      function levelDone(){
        if(!alive()) return;
        idle.clear();
        state.locked = true; stopNudge();
        const L = levels[li];
        /* [r32] the supplied artwork for this beat. The title is a picture because it is a drawn
           lockup, not type we could set; the button stays a real <button> so it is still tappable
           and focusable. */
        const art = L.art ? `<img src="assets/UI/${L.art}" alt="${L.name} पूरा हुआ!">`
                          : `${L.name} पूरा हुआ!`;
        body.innerHTML =
          '<div class="fvd-panel"><div class="fvd-panel-stars">' +
            '<img src="assets/UI/ui_star.png" alt="">' +
            '<img src="assets/UI/ui_star.png" class="mid" alt="">' +
            '<img src="assets/UI/ui_star.png" alt="">' +
          '</div>' +
          `<div class="fvd-panel-ttl">${art}</div>` +
          '</div>';
        /* the stars land one at a time, left, middle, right, each with its own rising chime */
        const stars = [...body.querySelectorAll(".fvd-panel-stars img")];
        stars.forEach((el, k)=> later(()=>{ el.classList.add("pop"); sfxStarTing(k); }, 260 + k*300));
        const celebrationAt=260 + stars.length*300;
        later(()=>{
          confettiCannon();
          later(()=>oceanSay('correct',()=>later(()=>{li++;qi=0;renderQuestion();},650)),550);
        }, celebrationAt);
        setSwMood("celebrate");
      }

      /* ---------- all levels done ---------- */
      function finish(){
        if(!alive()) return;
        idle.clear();
        state.locked = true; stopNudge();
        const all = levels.flatMap(l => l.questions);
        body.innerHTML =
          '<div class="fvd-panel"><div class="fvd-panel-ttl">सभी वाक्य पूरे हुए!</div>' +
          '<div class="fvd-summary">' +
            all.map(q => `<span>${q.one} → ${q.many}</span>`).join("") +
          '</div></div>';
        confettiCannon(); burstStars(); setSwMood("celebrate");
        /* The authored long lesson-completion VO belongs on this final fill-result summary, while
           all completed sentence pairs are still visible—not on the separate mascot end screen. */
        const finale = CARD.slides.find(s => s.type === "CELEBRATION");
        const completionVo = finale ? audioFor(finale, "prompt") : null;
        later(()=> play(completionVo, ()=>later(()=>completeSlide(true),900)),650);
      }

      function nextQuestion(){
        if(!alive()) return;
        qi++;
        if(qi < levels[li].questions.length){ renderQuestion(); return; }
        if(li < levels.length - 1){ levelDone(); return; }
        finish();
      }

      renderQuestion();
    }
  },

  STORY_SCENE: {
    /* TEACH — one poem page, built to the review deck (pp.4,6,8,10):
         · no instructional panel — the picture and the poem own the whole card
         · the stanza's lines arrive ONE BY ONE, the एक/अनेक words burning orange
         · image 1 rides the first stanza, image 2 swaps in for the second
       data.beats = [{ img, emoji, lines:[ "…*गुब्बारा*…" ], audio }] */
    mount(host, slide){
      const d = slide.data || {};
      const beats = d.beats && d.beats.length ? d.beats
                  : [{ img: d.image_id, emoji: d.emoji, lines: [d.caption_hi || ""], audio: (slide.audio||{}).narration }];

      const wrap = document.createElement("div"); wrap.className = "story-scene";
      wrap.innerHTML = '<div class="story-stage"><div class="story-frame"></div></div>' +
                       '<div class="story-caption"></div>';
      host.appendChild(wrap);
      const frame = wrap.querySelector(".story-frame");
      const cap   = wrap.querySelector(".story-caption");
      // deck: "no instructional panel in this slide"
      const card = host.closest(".tut-card"); if(card) card.classList.add("no-prompt");

      const showPicture = (b) => {
        const art = String(b.img || "");
        frame.classList.toggle("saheli-card", art === "scn_saheli_s" || art === "scn_saheli_p");
        frame.classList.toggle("saheli-single", art === "scn_saheli_s");
        frame.classList.toggle("saheli-many", art === "scn_saheli_p");
        frame.innerHTML = imgOrEmoji(b.img, b.emoji, "story-img swap", "story-fallback");
      };
      /* Keep earlier poem lines only when each picture contributes one line. If a picture already
         carries a complete two-line stanza (the two opening balloon scenes), the next picture gets
         its own clean screen instead of turning the caption into an unintended four-line block. */
      const cumulativeBeats = beats.every(b => (b.lines || []).length <= 1);
      const appendLines = (b) => (b.lines || []).map(t => {
        const p = storyTypeLine(t);
        cap.appendChild(p); return p;
      });

      state.ownsAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
      setSwMood("talk");

      let i = 0, armed = false;
      const alive = ()=> wrap.isConnected;   // [r17] a timer outliving this mount must not act
      const armNav = ()=>{ if(armed || !alive()) return; armed = true; setNavActive(true); setSwMood("point"); };
      const runBeat = ()=>{
        if(!alive()) return;
        const b = beats[i];
        showPicture(b);
        if(!cumulativeBeats) cap.replaceChildren();
        const fresh = appendLines(b);
        cap.classList.toggle("many-lines", cap.children.length > 2);
        const src = b.audio ? ("assets/Audio/" + b.audio + "." + AUDIO_EXT) : null;
        const typing=storyTypeSync(fresh,src,()=>{
          if(!alive()) return;
          /* A picture-to-picture beat gets exactly one second. On the final line the Next button
             appears as soon as the VO ends, with no extra dead pause. */
          if(++i < beats.length) setTimeout(runBeat,1000); else armNav();
        });
        state.replayAudio = ()=> typing.start();
        typing.start();
      };
      runBeat();
      setTimeout(armNav, 45000);   // watchdog: आगे always eventually opens if VO buffers slowly
    }
  },

  /* ================= COMPARE_VACHAN — "शब्दों की तुलना" (deck pp.5,7,9,11) =================
     Two pictures (one object / many), the two word cards under them, and the spoken line in its
     OST box. Deck removals are honoured: NO heading, NO "एक गुब्बारा"/"बहुत सारे गुब्बारे"
     captions, NO "आ की मात्रा → ए की मात्रा" row. Deck animation note: the whole word appears
     first, and only AFTERWARDS does the changed tail pulse/glow. */
  COMPARE_VACHAN: {
    mount(host, slide){
      const d = slide.data || {};
      const wrap = document.createElement("div"); wrap.className = "cmpv";
      const card = host.closest(".tut-card"); if(card) card.classList.add("no-prompt");

      const picOf = w => {
        const art = String(w.img || "");
        const friendClass = art === "scn_saheli_s" ? " saheli-card saheli-single"
                          : art === "scn_saheli_p" ? " saheli-card saheli-many" : "";
        return `<div class="cmpv-pic${friendClass}">${imgOrEmoji(w.img, w.emoji, "", "cmpv-emo")}</div>`;
      };
      const wordOf = w => `<div class="cmpv-word">${hlText(w.stem)}<span class="chg">${hlText(w.change)}</span></div>`;
      wrap.innerHTML =
        `<div class="cmpv-pics">${picOf(d.s)}${picOf(d.p)}</div>` +
        `<div class="cmpv-words">${wordOf(d.s)}${wordOf(d.p)}</div>`;   // the explain line is VO only — spoken, never shown on screen
      host.appendChild(wrap);

      const words = [...wrap.querySelectorAll(".cmpv-word")];

      state.ownsAudio = true; state.navVoEligible = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
      setSwMood("talk");

      // Reveal the singular and plural cards at their own word in the poem VO, then highlight both.
      const alive = ()=> wrap.isConnected;   // [r17] see STORY_SCENE — clearHost() empties the host
      const revealWord = index=>{
        if(!alive()||!words[index])return;
        words[index].classList.add("in");
      };
      let cueRun=0,activeCueTimers=[];
      const cueClip=(src,cues,onEnd)=>{
        activeCueTimers.forEach(clearTimeout);
        const run=++cueRun,timers=[];
        activeCueTimers=timers;
        const schedule=(cue,ms)=>{
          const index=cues.indexOf(cue);
          clearTimeout(timers[index]);
          timers[index]=setTimeout(()=>{
            if(run!==cueRun)return;
            cue.done=true;cue.fire();
          },Math.max(0,ms));
        };
        cues.forEach(cue=>cue.done=false);
        cues.forEach(cue=>schedule(cue,authoredVoHoldMs(src)*cue.ratio));
        play(src,()=>{
          if(run!==cueRun)return;
          timers.forEach(clearTimeout);
          const pending=cues.filter(cue=>!cue.done);
          if(!pending.length){if(alive()&&onEnd)onEnd();return;}
          pending.forEach((cue,index)=>setTimeout(()=>{
            if(run!==cueRun)return;
            cue.done=true;cue.fire();
            if(index===pending.length-1&&alive()&&onEnd)onEnd();
          },index*520));
        });
        const audio=currentAudio;
        if(audio){
          const sync=()=>{
            if(!alive()||currentAudio!==audio)return;
            const seconds=Number(audio.duration);
            if(!Number.isFinite(seconds)||seconds<=0)return;
            cues.forEach(cue=>{
              if(cue.done)return;
              schedule(cue,seconds*1000*cue.ratio-audio.currentTime*1000);
            });
          };
          if(audio.readyState>=1)sync();
          else audio.addEventListener("loadedmetadata",sync,{once:true});
        }
      };
      const recapSrc=audioFor(slide,"recap");
      const recapId=String(recapSrc||"").split("/").pop().replace(/\.[^.]+$/,"");
      const recapText=(CARD.assets&&CARD.assets.audio_text&&CARD.assets.audio_text[recapId])||"";
      const ratioAt=(index,fallback)=>index>=0&&recapText.length
        ?Math.max(0,Math.min(.98,index/recapText.length)):fallback;
      const plural=String(d.p.stem||"")+String(d.p.change||"");
      const poemCues=[
        {word:0,ratio:ratioAt(recapText.indexOf(String(d.s.stem||"")+String(d.s.change||"")),.22),fire:()=>revealWord(0)},
        {word:1,ratio:ratioAt(recapText.indexOf(plural),.68),fire:()=>revealWord(1)}
      ];
      const narratePair=()=>{
        if(!alive())return;
        words.forEach(w=>w.classList.remove("in","lit"));
        setNavActive(false);setSwMood("talk");
        cueClip(recapSrc,poemCues,()=>{
          // Both labels are now visible. Highlight each changed ending only when its form is spoken.
          words.forEach(w=>w.classList.add("in"));
          const explainSrc=audioFor(slide,"explain");
          const explainId=String(explainSrc||"").split("/").pop().replace(/\.[^.]+$/,"");
          const explainText=(CARD.assets&&CARD.assets.audio_text&&CARD.assets.audio_text[explainId])||"";
          const ratioInExplain=(form,fallback)=>{
            const at=explainText.indexOf(form);
            return at>=0&&explainText.length?Math.max(0,Math.min(.98,at/explainText.length)):fallback;
          };
          const glowCues=[
            {ratio:ratioInExplain(String(d.s.stem||"")+String(d.s.change||""),.34),fire:()=>words[0]?.classList.add("lit")},
            {ratio:ratioInExplain(plural,.78),fire:()=>words[1]?.classList.add("lit")}
          ];
          cueClip(explainSrc,glowCues,()=>{
            if(!alive())return;
            setNavActive(true);setSwMood("point");
          });
        });
      };
      state.replayAudio=narratePair;
      narratePair();
      setTimeout(()=>{ if(alive() && !$("navBtn").classList.contains("active")) setNavActive(true); }, 45000);
    }
  },

  INTRO: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "intro-stage";
      // [20a INTRO-PICS] additive PICTURE mode (g2 deck: demo with pictures, speak each word
      // one-by-one) — gated on data.pics [{img,emoji,audio},...]; letters mode untouched.
      const pics = Array.isArray(slide.data.pics) && slide.data.pics.length ? slide.data.pics : null;
      const items = pics || slide.data.letters;
      const clipOf = i => pics ? (pics[i].audio || null)
                               : ((slide.data.phonemes && slide.data.phonemes[items[i]]) || null);
      const keyOf  = i => pics ? (pics[i].img || String(i)) : items[i];
      const tapped = new Set();
      let _autoDone = false;   // [24a A3] auto mode: flips true once every card has been taught → taps become replays
      const tiles = [];
      // [16f] Size tiles to the REAL container (tut-card frame ~990px inside). Fit one row at
      // MAXW=960; below the 110px touch floor, WRAP into two balanced rows. Pics may run larger.
      const GAP = 20, MAXW = 960, n = items.length;
      let rowsOf;
      const CAP = pics ? 250 : 184;
      let tSize = Math.min(CAP, Math.floor((MAXW - (n-1)*GAP) / n));
      if (tSize >= 110) { rowsOf = [n]; }
      else {
        const top = Math.ceil(n/2), bot = n - top;
        tSize = Math.min(CAP, Math.floor((MAXW - (top-1)*GAP) / top));
        rowsOf = [top, bot];
      }
      const tFont = Math.round(tSize * 0.565);
      const rowEls = rowsOf.map(() => {
        const r = document.createElement("div"); r.className = "intro-letters";
        r.style.gap = GAP + "px"; return r;
      });
      const rowFor = i => (rowsOf.length === 1 || i < rowsOf[0]) ? rowEls[0] : rowEls[1];
      function nudgeNext(){
        for(let i=0;i<items.length;i++){
          if(!tapped.has(keyOf(i))){ pointNudgeAt(tiles[i]); return; }
        }
        stopNudge();
      }
      items.forEach((it, i) => {
        const tile = document.createElement("div");
        tile.className = pics ? "intro-letter intro-pic" : "intro-letter";
        tile.style.width = tile.style.height = tSize + "px";
        if(!pics) tile.style.fontSize = tFont + "px";
        tile.innerHTML = pics ? imgOrEmoji(it.img, it.emoji, "intro-pic-img", "intro-pic-emoji")
                              : `<span class="ink-glyph">${it}</span>`;
        tile.onclick = ()=>{
          // [24a A3] auto walk-through: card taps are IGNORED until every card has been taught
          // (the child can't cut the lesson off / jump ahead mid-teaching); once teaching completes,
          // a tap REPLAYS that card (vachan NUMBER_INTRO parity — tap-to-replay unlocks after teach).
          if(slide.data.auto){
            if(!_autoDone) return;
            tile.classList.add("played");
            const clip = clipOf(i);
            play(clip ? "assets/Audio/" + clip + "." + AUDIO_EXT : null);
            GameBus.emit(pics ? "intro_pic_tap" : "intro_letter_tap", { slide_id: slide.id, letter: keyOf(i), replay: true });
            return;
          }
          tile.classList.add("played");
          const clip = clipOf(i);
          play(clip ? "assets/Audio/" + clip + "." + AUDIO_EXT : null);
          GameBus.emit(pics ? "intro_pic_tap" : "intro_letter_tap", { slide_id: slide.id, letter: keyOf(i) });
          tapped.add(keyOf(i));
          if(tapped.size >= items.length){ stopNudge(); setNavActive(true); }
          else { nudgeNext(); }
        };
        rowFor(i).appendChild(tile); tiles.push(tile);
      });
      rowEls.forEach(r => wrap.appendChild(r));
      host.appendChild(wrap);

      setNavActive(false);
      $("navBtn").onclick = ()=>{ if(tapped.size >= items.length) completeSlide(true); };
      nudgeNext();
      // [16h] Phase-1 autonomous mode: tiles highlight + speak one by one BY THEMSELVES.
      if(slide.data.auto){
        stopNudge(); state.ownsAudio = true;
        let ai = 0;
        const aStep = ()=>{
          if(CARD.slides[state.idx] !== slide) return;
          if(ai >= items.length){ stopNudge();
            // [20a INTRO-AUDIO-FIX] the auto chain DROPPED the instruction VO (Yasir live catch #7,
            // verified on HIKGH02_L02_S01) — play it after the self-play, before आगे unlocks.
            // A missing clip falls back to a silent beat and still unlocks.
            play(audioFor(slide, "instruction") || null, ()=>{
              if(CARD.slides[state.idx] !== slide) return;
              _autoDone = true;   // [24a A3] teaching complete → card taps become per-card replays
              state.replayAudio = ()=> play(audioFor(slide, "prompt") || audioFor(slide, "instruction") || null, ()=>{});   // [24a N8] chip replays post-teach
              $("navBtn").onclick = ()=> completeSlide(true); setNavActive(true);
            });
            return; }
          const tile = tiles[ai];
          tile.classList.add("played"); pointNudgeAt(tile);
          const clip = clipOf(ai);
          ai++;
          play(clip ? "assets/Audio/" + clip + "." + AUDIO_EXT : null, ()=> setTimeout(aStep, 380));
        };
        play(audioFor(slide, "prompt") || null, ()=> setTimeout(aStep, 500));
      }   // start by guiding the first tile
    }
  },

  MEET_LETTER: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "meet-stage";
      // 16L: fit the glyph to the box (MEET here shows whole WORDS like काम, not single letters →
      // 200px overflowed the 300px box). Size by cluster count.
      // data.matra = the matra char (e.g. "ा"). For RIGHT-SPACING matras we now colour it RED
      // INSIDE the word itself (_matraWordSVG two-layer overlay); other matras keep the callout.
      const _mlFit = (s)=>{ const n=[...(s||"")].length; return n<=1?200 : n<=2?152 : n<=3?120 : n<=4?96 : 78; };
      const _box = (txt, matra)=> {
        const iw = matra && RIGHT_SPACING_MATRAS.has(matra);
        return `<div class="meet-letter-box"${iw ? ` data-mw-word="${txt}" data-mw-matra="${matra}" data-mw-fs="${_mlFit(txt)}"` : ""}>`
          + (iw ? _matraWordSVG(txt, matra, _mlFit(txt))
                : `<span class="glyph ink-glyph" style="font-size:${_mlFit(txt)}px">${txt}</span>`)
          + `</div>`;
      };
      if(slide.data.pair){
        const pair = document.createElement("div"); pair.className = "meet-pair";
        slide.data.pair.forEach(p => {
          const item = document.createElement("div"); item.className = "meet-pair-item";
          item.innerHTML = `
            ${_box(p.letter)}
            
            <div class="meet-pic-box">
              ${imgOrEmoji(p.picture_img, p.picture_emoji, "pic-img", "pic-emoji")}
              <span class="pic-label">${p.word_hi}</span>
            </div>`;
          pair.appendChild(item);
        });
        wrap.appendChild(pair);
      } else {
        wrap.innerHTML = `
          ${_box(slide.data.letter, slide.data.matra)}
          
          <div class="meet-pic-box">
            ${imgOrEmoji(slide.data.picture_img, slide.data.picture_emoji, "pic-img", "pic-emoji")}
            <span class="pic-label">${slide.data.word_hi}</span>
          </div>`;
      }
      // Right-spacing matras (ा …) are now coloured RED in-word by _box → no callout needed.
      // Other matras (े ै ि …) can't be recoloured in-word, so keep the coloured ◌<matra> callout.
      if(slide.data.matra && !RIGHT_SPACING_MATRAS.has(slide.data.matra)){
        const col = document.createElement("div"); col.className = "meet-col";
        col.appendChild(wrap);
        const mh = document.createElement("div"); mh.className = "matra-hint";
        mh.innerHTML = `इस शब्द की मात्रा — <span class="matra-hl ink-glyph">◌${slide.data.matra}</span>`;
        col.appendChild(mh);
        host.appendChild(col);
      } else {
        host.appendChild(wrap);
      }
      // 16m: AUTONOMOUS demo (data.auto) — the 3-phase contract kills passive show-and-tell
      // ("यह काम है"). The hand POINTS at the word + speaks it, then POINTS at the matra callout +
      // speaks its sound (the matra being pointed/spoken is the feasible "highlight the matra"),
      // then the picture; आगे is locked till the demo finishes, then explicitly wired (dead-button).
      if(slide.data.auto){
        state.ownsAudio = true; state.demoRunning = true; setNavActive(false); setSwMood("teach");   // [24a N8]
        const boxEl = host.querySelector(".meet-letter-box");
        const pillEl = host.querySelector(".matra-hl");   // exists only in the callout (non-right-spacing) path
        const picEl = host.querySelector(".meet-pic-box");
        const steps = [];
        if(boxEl) steps.push([boxEl, audioFor(slide, "prompt") || audioFor(slide, "word_name")]);
        if(slide.data.matra){
          // point at the matra + speak its sound. In-word (red) matra → point the word box and
          // PULSE the red matra; callout matra → point the ◌<matra> pill (old behaviour).
          const mAudio = slide.data.matra_audio ? "assets/Audio/" + slide.data.matra_audio + "." + AUDIO_EXT : null;
          steps.push([pillEl || boxEl, mAudio, pillEl ? null : "matra"]);
        }
        if(picEl) steps.push([picEl, audioFor(slide, "word_name")]);
        let si = 0, _done = false;
        const finish = ()=>{ if(_done) return; _done = true; stopNudge(); state.demoRunning = false; $("navBtn").onclick = ()=> completeSlide(true); setNavActive(true); };
        const step = ()=>{
          if(CARD.slides[state.idx] !== slide) return;                 // navigated away → abort
          if(si >= steps.length){ finish(); return; }
          /* [28p] TWO OF YASIR'S FOUR MEET_LETTER ASKS (2026-07-28, कप + जल screenshots).
             ARROW: the literal "→" between the letter box and the picture was markup inside this module,
             so no card could ever remove it. Gone from both MEET_LETTER paths. MEET_SHAPE / MEET_NUMBER /
             MEET_GENDER keep theirs — he named MEET_LETTER.
             HAND: the demo planted the hand on the letter box and then the picture; on a slide with one
             letter and one picture that "points at the obvious and adds nothing". Dropped. The one place
             it earns its keep is a word taught for BOTH sounds (जल = ज + ल), synced to whichever glyph is
             being spoken — that depends on displaying both letters, which is STILL OPEN, so no
             "is this two-letter" condition is guessed at here. */
          const stp = steps[si]; si++;
          const mw = stp[2] === "matra" ? stp[0].querySelector(".matra-word") : null;
          if(mw) mw.classList.add("mw-pulse");
          play(stp[1] || null, ()=>{ if(mw) mw.classList.remove("mw-pulse"); setTimeout(step, 450); });
        };
        $("navBtn").onclick = ()=> completeSlide(true);                 // explicit (dead-button lesson)
        state.replayAudio = ()=> play(audioFor(slide, "prompt") || null, ()=>{});
        setTimeout(step, 400);
        setTimeout(()=>{ if(CARD.slides[state.idx] === slide) finish(); }, steps.length * 4000 + 3000);   // FAIL-SAFE: आगे never stays dead if audio blocks/stalls
        return;
      }
      // नav unlocks only after the VO has played once (students can't skip the model)
      state.gateNavUntilAudio = true;
      setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
    }
  },

  /* ===== SHAPES (maths) — reuse the same scaffold/nudge/feedback as letters ===== */
  SHAPE_INTRO: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "intro-stage";
      const row  = document.createElement("div"); row.className = "intro-shapes";
      const shapes = slide.data.shapes; const tapped = new Set(); const tiles = [];
      const GAP = 28, MAXW = 1220, n = shapes.length;
      const tSize = Math.max(120, Math.min(184, Math.floor((MAXW - (n-1)*GAP) / n)));
      row.style.gap = GAP + "px";
      function nudgeNext(){
        for(let i=0;i<shapes.length;i++){ if(!tapped.has(i)){ pointNudgeAt(tiles[i]); return; } }
        stopNudge();
      }
      shapes.forEach((sh, i) => {
        const tile = document.createElement("div"); tile.className = "intro-shape";
        tile.style.width = tile.style.height = tSize + "px";
        // name label (revealed on tap — child hears the name AND sees it on top of the shape)
        tile.innerHTML = `<span class="shape-name">${sh.name || ""}</span>` +
                         shapeSVG(sh.shape, {color: sh.color, size: Math.round(tSize*0.62), rotate: sh.rotate});
        tile.onclick = ()=>{
          tile.classList.add("played");
          play(sh.name_audio ? "assets/Audio/" + sh.name_audio + "." + AUDIO_EXT : null);
          GameBus.emit("intro_shape_tap", { slide_id: slide.id, shape: sh.shape });
          tapped.add(i);
          if(tapped.size >= shapes.length){ stopNudge(); setNavActive(true); }
          else { nudgeNext(); }
        };
        row.appendChild(tile); tiles.push(tile);
      });
      wrap.appendChild(row); host.appendChild(wrap);
      setNavActive(false);
      $("navBtn").onclick = ()=>{ if(tapped.size >= shapes.length) completeSlide(true); };
      nudgeNext();
    }
  },

  MEET_SHAPE: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "meet-stage";
      wrap.innerHTML = `
        <div class="meet-shape-box">
          ${shapeSVG(slide.data.shape, {color: slide.data.color, size: 190, rotate: slide.data.rotate})}
          <span class="label">${slide.data.name}</span>
        </div>
        <div class="meet-arrow">→</div>
        <div class="meet-pic-box">
          ${imgOrEmoji(slide.data.object_img, slide.data.object_emoji, "pic-img", "pic-emoji")}
          <span class="pic-label">${slide.data.object_hi}</span>
        </div>`;
      host.appendChild(wrap);
      state.gateNavUntilAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
    }
  },

  TRACE_SHAPE: {
    // [21c flag#2] PRODUCE gesture (re-adds the game's original trace, breaks pick-dominance): the child
    // FINGER-TRACES the named shape's outline — not a pick. Forgiving hit-corridor; ~80% of the outline
    // covered → success + side-confetti. Idle → a marker animates along the stroke to demonstrate. Shape
    // is UPRIGHT with SHARP corners (rotate forced 0, no rx — honours the locked 2D-shapes direction) and
    // a FIXED colour per shape. NO score / timer / number is ever shown. guide:"dotted" = full visible
    // dotted outline (Guided); guide:"faint" = low-opacity outline (Independent, less scaffold).
    // data:{shape, color, name?, name_audio?, guide:"dotted"|"faint"}
    // audio:{prompt, shape_name?, done, try_again?}   signals:{on_complete:["shape_trace_complete"]}
    mount(host, slide){
      const d = slide.data;
      const PATHS = {   // viewBox 0 0 100 100, matches shapeSVG geometry; TRUE corners
        circle:    "M 8,50 a 42,42 0 1 0 84,0 a 42,42 0 1 0 -84,0 Z",
        square:    "M 12,12 H 88 V 88 H 12 Z",
        triangle:  "M 50,9 L 91,89 L 9,89 Z",
        rectangle: "M 6,28 H 94 V 72 H 6 Z"
      };
      const shape = d.shape, color = d.color || "#386AF6";
      const dPath = PATHS[shape] || PATHS.square;
      const faint = d.guide === "faint";
      state.ownsAudio = true; setNavActive(false); setSwMood("point");

      const wrap = document.createElement("div"); wrap.className = "trace-stage";
      const box  = document.createElement("div"); box.className = "trace-box";
      box.innerHTML =
        `<svg class="trace-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
           <path class="trace-guide${faint ? " faint" : ""}" d="${dPath}" stroke="${color}" stroke-width="6"
                 ${faint ? "" : `stroke-dasharray="2 7"`}/>
           <path class="trace-ink" d="${dPath}" stroke="${color}" stroke-width="9"/>
           <g class="trace-dots"></g>
           <circle class="trace-marker" r="6" fill="${color}" style="display:none"/>
         </svg>`;
      wrap.appendChild(box); host.appendChild(wrap);

      const svg   = box.querySelector(".trace-svg");
      const guide = box.querySelector(".trace-guide");
      const inkP  = box.querySelector(".trace-ink");
      const dotsG = box.querySelector(".trace-dots");
      const marker= box.querySelector(".trace-marker");

      const total = inkP.getTotalLength();
      const N = 96, CORRIDOR = 11;   // user-units; a generous corridor for little fingers
      const pts = [], hit = new Array(N).fill(false);
      for(let i=0;i<N;i++) pts.push(inkP.getPointAtLength(total * i / N));
      pts.forEach(p=>{ const c = document.createElementNS("http://www.w3.org/2000/svg","circle");
        c.setAttribute("cx", p.x); c.setAttribute("cy", p.y); c.setAttribute("r", faint ? 1.5 : 2.1);
        c.setAttribute("fill", color); c.setAttribute("class","trace-dot"); dotsG.appendChild(c); });
      const dotEls = [...dotsG.children];
      inkP.style.strokeDasharray = String(total); inkP.style.strokeDashoffset = String(total);   // ink hidden until success flourish

      let done = false, active = false;
      const covered = ()=> hit.reduce((a,b)=> a + (b?1:0), 0);
      const toSvg = (cx, cy)=>{ const m = svg.getScreenCTM(); if(!m) return null;
        const p = svg.createSVGPoint(); p.x = cx; p.y = cy; return p.matrixTransform(m.inverse()); };

      // idle → demonstrate: a marker travels the outline ("trace like this")
      let idleTimer = null, demoRAF = null;
      const stopIdle = ()=>{ clearTimeout(idleTimer); if(demoRAF){ cancelAnimationFrame(demoRAF); demoRAF = null; } marker.style.display = "none"; };
      const runDemo = ()=>{ let s = 0; marker.style.display = "";
        const stepD = ()=>{ if(done || active){ marker.style.display = "none"; demoRAF = null; return; }
          s += total / 90; if(s > total) s = 0;
          const p = inkP.getPointAtLength(s); marker.setAttribute("cx", p.x); marker.setAttribute("cy", p.y);
          demoRAF = requestAnimationFrame(stepD); };
        stepD(); };
      const kickIdle = ()=>{ stopIdle(); idleTimer = setTimeout(()=>{ if(!done && !active) runDemo(); }, 2600); };

      function finish(){
        done = true; stopIdle(); stopNudge();
        guide.classList.add("done"); dotEls.forEach(x=> x.classList.add("on"));
        inkP.style.strokeDashoffset = "0";   // draw the full outline as the success flourish
        GameBus.emit("shape_trace_complete", { slide_id: slide.id, phase: slide.phase, shape, value: true,
          latency_ms: Date.now()-state.slideStart });
        sfxCorrect(); confettiCannon(); setSwMood("celebrate");
        play(audioFor(slide, "done") || null, ()=> setNavActive(true));
      }
      const markAt = (sp)=>{ if(!sp) return; let any = false;
        for(let i=0;i<N;i++){ if(hit[i]) continue;
          const dx = pts[i].x - sp.x, dy = pts[i].y - sp.y;
          if(dx*dx + dy*dy <= CORRIDOR*CORRIDOR){ hit[i] = true; dotEls[i].classList.add("on"); any = true; } }
        if(any && !done && covered() / N >= 0.8) finish();
      };

      const onDown = (e)=>{ if(done) return; active = true; stopIdle(); const t = e.touches ? e.touches[0] : e;
        markAt(toSvg(t.clientX, t.clientY)); if(e.cancelable) e.preventDefault(); };
      const onMove = (e)=>{ if(!active || done) return; const t = e.touches ? e.touches[0] : e;
        markAt(toSvg(t.clientX, t.clientY)); if(e.cancelable) e.preventDefault(); };
      const onUp   = ()=>{ if(active){ active = false; if(!done) kickIdle(); } };
      box.addEventListener("mousedown", onDown); box.addEventListener("touchstart", onDown, {passive:false});
      box.addEventListener("mousemove", onMove); box.addEventListener("touchmove", onMove, {passive:false});
      window.addEventListener("mouseup", onUp);   box.addEventListener("touchend", onUp);

      state.replayAudio = ()=> play(audioFor(slide, "prompt") || null, ()=>{});
      $("navBtn").onclick = ()=>{ if(done) completeSlide(true); };
      // prompt → shape name → arm the idle-demo (no auto-play double-fire: state.ownsAudio set above)
      play(audioFor(slide, "prompt") || null, ()=> play(audioFor(slide, "shape_name") || null, ()=> kickIdle()));
    }
  },

  TAP_SHAPE_BY_NAME: {
    mount(host, slide){
      mountTapOptions({
        slide, host, signalName: "shape_name_first_try",
          /* [28m] NO VOLUME BUTTON, ANYWHERE. Yasir 2026-07-28: "we use vol button nowhere. if
             nothing then we keep question only." This stimulus had NO image, so 28c left its 🔊 +
             "सुनो" chip alone and flagged it — stripping it looked like it would leave a blank card.
             The ruling settles it: nothing to show => show the QUESTION only, no chip. The chip was
             also the only way to re-hear the sound, so that function moves to the header replay
             (state.replayAudio, set after mount) instead of dying with the affordance. */
          stimulus: null,
        options: slide.data.options,
        isCorrect: (opt) => opt.shape === slide.data.target,
        optionRenderer: (opt) => shapeCell(opt)
      });
        /* [28m] the removed chip was the only way to re-hear the sound — keep the FUNCTION on the
           header replay. Set AFTER mount so mountTapOptions cannot overwrite it. */
        state.replayAudio = ()=>{ state.audioReplays++; play(audioFor(slide,"shape_name") || null, ()=>{}); };
    }
  },

  TAP_SHAPE_BY_PICTURE: {
    mount(host, slide){
      mountTapOptions({
        slide, host, signalName: "shape_env_first_try",
        stimulus: stimulusPic(slide.data.object_hi, slide.data.object_emoji, slide.data.object_img),
        options: slide.data.options,
        isCorrect: (opt) => opt.shape === slide.data.target,
        optionRenderer: (opt) => shapeCell(opt)
      });
    }
  },

  TAP_PICTURE_BY_SHAPE: {
    mount(host, slide){
      mountTapOptions({
        slide, host, signalName: "shape_object_first_try",
        stimulus: stimulusShape({shape: slide.data.shape, color: slide.data.color, rotate: slide.data.rotate}),
        options: slide.data.options,
        isCorrect: (opt) => opt.correct === true,
        optionRenderer: (opt) => pictureCell(opt.object_hi, opt.object_emoji, opt.object_img)
      });
    }
  },

  SORT_SHAPE: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "sort-stage shape-sort";
      const binsRow = document.createElement("div");
      binsRow.className = "sort-bins" + (slide.data.bins.length >= 4 ? " many" : "");
      slide.data.bins.forEach(b => {
        const bin = document.createElement("div");
        bin.className = "sort-bin dd-zone";            // dd-zone → drop detection
        bin.dataset.shape = b.shape;
        // header (faint reference shape + label) INSIDE the box, then a clear drop area
        bin.innerHTML = `<div class="bin-head-row"><span class="bin-ref">${shapeSVG(b.shape, {color:"#AEB9CC", size:34})}</span><span class="bin-title">${b.label}</span></div>`+
          `<div class="bin-items"></div>`;
        binsRow.appendChild(bin);
      });
      const tray = document.createElement("div"); tray.className = "sort-tray";
      const items = slide.data.items.slice().sort(()=> Math.random() - 0.5);
      items.forEach(it => {
        const t = document.createElement("div"); t.className = "sort-item"; t.dataset.shape = it.shape; if(it.audio) t.dataset.audio = it.audio;   // [20a SORT-01]
        t.innerHTML = shapeSVG(it.shape, {color: it.color, size: 70, rotate: it.rotate});
        tray.appendChild(t);
      });
      wrap.appendChild(binsRow); wrap.appendChild(tray);
      host.appendChild(wrap);

      state.attempts = 0; state.locked = false;
      let placed = 0; const need = slide.data.items.length;
      if(slide.data.reveal_seq) sortSeqReveal(tray, slide);   // [20a SORT-01] opt-in
      [...tray.children].forEach(tile => {
        makeDraggable(tile, (zone, t) => {
          const bin = zone.closest(".sort-bin"); if(!bin) return;
          state.attempts++;
          if(bin.dataset.shape === t.dataset.shape){
            leaveTrayGhost(t);   // [24a A5] capture the tray-slot size before .snapped shrinks/moves it
            t.classList.add("snapped");
            bin.querySelector(".bin-items").appendChild(t);
            placed++;
            if(t.dataset.audio && placed < need) play("assets/Audio/" + t.dataset.audio + "." + AUDIO_EXT, ()=>{});   // [20a SORT-01] speak-on-match
            GameBus.emit("shape_sort_item", { slide_id: slide.id, shape: t.dataset.shape, attempts: state.attempts });
            if(placed === need){
              state.locked = true;
              GameBus.emit("shape_sort_correct", {
                slide_id: slide.id, phase: slide.phase, value: true,
                attempts: state.attempts, latency_ms: Date.now() - state.slideStart
              });
              setTimeout(()=> celebrateThenAdvance(slide, false), 250);   // standard: confetti + VO + auto-advance, no popup
            }
          } else {
            bin.classList.add("hover"); bin.style.borderColor = "var(--wrong)";
            setTimeout(()=>{ bin.classList.remove("hover"); bin.style.borderColor = ""; }, 500);
            dragWrong(slide);   // buzz + Swiftie + spoken try_again (pre-readers need the spoken recovery)
            GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
          }
        });
      });
    }
  },

  /* ===== COUNTING (maths) — OTO tap-count, cardinality, meet-number, make-set ===== */
  COUNT_TAP: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "count-stage";
      const row  = document.createElement("div"); row.className = "count-row";
      const N = slide.data.count, obj = slide.data.object, nums = slide.data.numerals || [];
      // large sets (S04, up to 20): smaller tiles + optional rows-of-N grouping (curriculum: rows of 5/10)
      if(N > 10 || slide.data.per_row) row.classList.add("dense");
      if(slide.data.per_row){ row.style.display = "grid"; row.style.gridTemplateColumns = `repeat(${slide.data.per_row}, auto)`; }
      const items = []; let c = 0;
      for(let i=0;i<N;i++){
        const it = document.createElement("div"); it.className = "count-item";
        it.innerHTML = imgOrEmoji(obj.img, obj.emoji, "cobj-img", "cobj-emoji") + `<span class="count-badge"></span>`;
        row.appendChild(it); items.push(it);
      }
      wrap.appendChild(row); host.appendChild(wrap);

      function nudgeNext(){ const nx = items.find(x=>!x.classList.contains("counted")); if(nx) pointNudgeAt(nx); else stopNudge(); }
      items.forEach(it => {
        it.onclick = ()=>{
          if(it.classList.contains("counted")) return;   // one-to-one: never double-count
          c++; it.classList.add("counted");
          it.querySelector(".count-badge").textContent = String(c);   // Arabic running count; Hindi word spoken separately
          GameBus.emit("count_tap", { slide_id: slide.id, phase: slide.phase, n: c });
          if(c >= N){
            stopNudge();
            GameBus.emit("count_oto_complete", { slide_id: slide.id, phase: slide.phase,
              total: N, value: true, latency_ms: Date.now()-state.slideStart });
            // say the LAST number, then the total; enable आगे ONLY after "कुल N" finishes
            play("assets/Audio/vo_num_" + c + "." + AUDIO_EXT, ()=> setTimeout(()=>
              play("assets/Audio/vo_total_" + N + "." + AUDIO_EXT, ()=> setNavActive(true)), 300));
          } else {
            play("assets/Audio/vo_num_" + c + "." + AUDIO_EXT);    // one number word per touch
            nudgeNext();
          }
        };
      });
      setNavActive(false);
      $("navBtn").onclick = ()=>{ if(c >= N) completeSlide(true); };
      nudgeNext();
    }
  },

  COMBINE_COUNT: {
    // [21c] PUT-TOGETHER (MTKGA01_L03_S01 "Combines two small groups and counts the total, within 10").
    // The child DRAGS group B onto group A; the two sets visibly MERGE into ONE row, then the child
    // tap-counts the combined total one-by-one. The EVIDENCE is the set the child builds + counts, never
    // a numeral pick — the LO's mandated drag-and-combine. Misconception guards baked in:
    //   • one-to-one count: re-tapping a counted item is INERT → no double-counting the overlap where the
    //     two groups meet (the map's #1 error);
    //   • the merged set is a single clean row (never a pile) so the child can't lose track at the seam.
    // data.mode "demo" runs it AUTONOMOUSLY for the Phase-1 tutorial (a hand pushes B onto A, then it
    // counts itself — KG children who can't yet count WATCH the put-together happen).
    // data:{a, b, object, numerals?, mode?}   audio:{prompt, conclude?(demo)}
    mount(host, slide){
      const d = slide.data, A = d.a|0, B = d.b|0, N = A + B, obj = d.object;
      const demo = d.mode === "demo";
      state.ownsAudio = true; setNavActive(false); setSwMood(demo ? "teach" : "point");
      const wrap = document.createElement("div"); wrap.className = "combine-stage" + (demo ? " is-demo" : "");
      const layout = document.createElement("div"); layout.className = "combine-layout";
      const mat = document.createElement("div"); mat.className = "combine-mat dd-zone";   // group A = the fixed drop target
      const grpA = document.createElement("div"); grpA.className = "combine-grp";
      const grpB = document.createElement("div"); grpB.className = "combine-grp combine-drag";   // group B = the draggable cluster
      const mkItem = ()=>{ const it = document.createElement("div"); it.className = "count-item combine-item";
        it.innerHTML = imgOrEmoji(obj.img, obj.emoji, "cobj-img", "cobj-emoji") + `<span class="count-badge"></span>`; return it; };
      for(let i=0;i<A;i++) grpA.appendChild(mkItem());
      for(let i=0;i<B;i++) grpB.appendChild(mkItem());
      mat.appendChild(grpA);
      const plus = document.createElement("div"); plus.className = "combine-plus"; plus.textContent = "और";
      const bWrap = document.createElement("div"); bWrap.className = "combine-bwrap"; bWrap.appendChild(grpB);
      layout.appendChild(mat); layout.appendChild(plus); layout.appendChild(bWrap);
      wrap.appendChild(layout); host.appendChild(wrap);

      let c = 0; const merged = []; let counting = false;
      const stale = ()=> (state.idx !== undefined && CARD.slides[state.idx] !== slide);

      function finish(){   // last number already spoken by the caller → say the cardinal total, then settle
        GameBus.emit("combine_count_correct", { slide_id: slide.id, phase: slide.phase,
          a: A, b: B, total: N, value: true, latency_ms: Date.now()-state.slideStart });
        play("assets/Audio/vo_total_" + N + "." + AUDIO_EXT, ()=>{
          if(demo){ play(audioFor(slide, "conclude") || null, ()=>{ state.demoRunning = false; setNavActive(true); }); }   // [24a N8] demo chain over → chip live
          else { sfxCorrect(); confettiCannon(); setSwMood("celebrate"); setNavActive(true); }   // produce: celebrate in place, then unlock आगे
        });
      }
      function startCount(){
        counting = true;
        // collapse the two groups into ONE clean row (A first, then B), badges cleared — nothing to
        // double-count at the seam because it's a single continuous row the child counts straight through.
        const items = [...grpA.querySelectorAll(".combine-item"), ...grpB.querySelectorAll(".combine-item")];
        const row = document.createElement("div"); row.className = "count-row combine-merged" + (N > 8 ? " dense" : "");
        items.forEach(it=>{ it.classList.remove("counted","demo-hit"); const b = it.querySelector(".count-badge"); if(b) b.textContent = ""; row.appendChild(it); merged.push(it); });
        layout.className = "combine-layout merged"; layout.innerHTML = ""; layout.appendChild(row);
        const nudgeNext = ()=>{ const nx = merged.find(x=>!x.classList.contains("counted")); if(nx) pointNudgeAt(nx); else stopNudge(); };
        if(demo){
          (function stepC(){
            if(stale()) return;
            if(c >= N){ setTimeout(finish, 380); return; }
            const it = merged[c]; c++; it.classList.add("counted","demo-hit");
            it.querySelector(".count-badge").textContent = String(c); pointNudgeAt(it);
            play("assets/Audio/vo_num_" + c + "." + AUDIO_EXT, ()=> setTimeout(stepC, 430));
          })();
        } else {
          merged.forEach(it=>{ it.onclick = ()=>{
            if(it.classList.contains("counted")) return;   // one-to-one; re-tap INERT → never double-count the overlap
            c++; it.classList.add("counted"); it.querySelector(".count-badge").textContent = String(c);
            GameBus.emit("count_tap", { slide_id: slide.id, phase: slide.phase, n: c });
            if(c >= N){ stopNudge(); play("assets/Audio/vo_num_" + N + "." + AUDIO_EXT, finish); }
            else { play("assets/Audio/vo_num_" + c + "." + AUDIO_EXT); nudgeNext(); }
          }; });
          nudgeNext();
        }
      }
      function merge(){ if(counting) return; stopNudge(); grpB.classList.add("merging"); sfxTap();
        setTimeout(startCount, 600); }   // let the slide-in play, then count

      if(demo){
        state.demoRunning = true;   // [24a N8] a replay tap mid-demo would gen-kill the prompt→merge→count chain (soft-lock)
        pointNudgeAt(grpB);
        play(audioFor(slide, "prompt") || null, ()=> setTimeout(()=>{ if(!stale()) merge(); }, 750));
        state.replayAudio = ()=> play(audioFor(slide, (counting && c >= N) ? "conclude" : "prompt") || null, ()=>{});
      } else {
        makeDraggable(grpB, (zone)=>{ if(counting || zone !== mat) return; merge(); });   // drag group B onto group A
        $("navBtn").onclick = ()=>{ if(c >= N) completeSlide(true); };
        play(audioFor(slide, "prompt") || null, ()=>{ if(!counting) pointNudgeAt(grpB); });
        state.replayAudio = ()=> play(audioFor(slide, "prompt") || null, ()=>{});
      }
    }
  },

  CONSERVE_COUNT: {
    // MTKGA01_L01_S03 "the LAST counted number IS the total" + its core misconception ("the total
    // changes when objects move"). One slide, two beats: (A) the child tap-counts the set one-to-one
    // (badges + spoken एक/दो/…, ending "कुल N" — the freeze-the-final-number teach), then (B) the SAME
    // objects visibly MOVE to scattered spots (badges clear), the move line asks "अब कितनी हैं?" and
    // numeral options appear — correct is the SAME N; options include N±1 (the moved-so-changed error).
    // data:{count, object, numerals, options:[{value,audio}]} · audio:{prompt, move, try_again, hint, reveal}.
    // GENERALISED count-then-pick engine (S03 conservation + S02's tap-count items). One slide:
    // tap-count the set one-to-one (badges + spoken एक/दो/… → frozen "कुल N"), then numeral options.
    // data: {count, object, options, arrange?("row"|"scatter"|"circle"|"two_groups"), groups?[a,b],
    //        move?(default true = objects drift after counting; false = count-then-pick, no drift)}.
    // move:false emits cardinality_first_try; move:true emits conserve_count_first_try.
    mount(host, slide){
      const d = slide.data, N = d.count, obj = d.object;
      const arrange = d.arrange || "row";
      const doMove  = d.move !== false;
      state.ownsAudio = true; setNavActive(false);
      const wrap = document.createElement("div"); wrap.className = "count-stage conserve";
      const row  = document.createElement("div"); row.className = "count-row arr-" + arrange + (N > 8 ? " dense" : "");
      const items = []; let c = 0;
      const mkItem = ()=>{ const it = document.createElement("div"); it.className = "count-item";
        it.innerHTML = imgOrEmoji(obj.img, obj.emoji, "cobj-img", "cobj-emoji") + `<span class="count-badge"></span>`;
        items.push(it); return it; };
      if(arrange === "two_groups"){
        const g = d.groups || [Math.ceil(N/2), Math.floor(N/2)];
        g.forEach((gn, gi)=>{ const cl = document.createElement("div"); cl.className = "count-cluster";
          for(let i=0;i<gn;i++) cl.appendChild(mkItem()); row.appendChild(cl);
          if(gi === 0){ const plus = document.createElement("div"); plus.className = "count-plus"; plus.textContent = "और"; row.appendChild(plus); } });
      } else if(arrange === "circle"){
        for(let i=0;i<N;i++){ const it = mkItem(); const a = -Math.PI/2 + i*2*Math.PI/N, R = N > 6 ? 176 : 140;
          it.style.position = "absolute";
          it.style.left = `calc(50% + ${Math.round(Math.cos(a)*R)}px)`;
          it.style.top  = `calc(50% + ${Math.round(Math.sin(a)*R)}px)`;
          it.style.marginLeft = "-48px"; it.style.marginTop = "-48px"; row.appendChild(it); }
      } else {
        for(let i=0;i<N;i++){ const it = mkItem();
          if(arrange === "scatter") it.style.transform = `translateY(${((i*23)%25)-12}px) rotate(${((i*37)%21)-10}deg)`;
          row.appendChild(it); }
      }
      wrap.appendChild(row); host.appendChild(wrap);
      const nudgeNext = ()=>{ const nx = items.find(x=>!x.classList.contains("counted")); if(nx) pointNudgeAt(nx); else stopNudge(); };
      const askOptions = ()=>{
        mountTapOptions({
          slide, host, signalName: doMove ? "conserve_count_first_try" : "cardinality_first_try",
          stimulus: null, nudgeTarget: null,
          options: d.options,
          columnsHint: Math.min(d.options.length, 5),
          isCorrect: (opt) => opt.value === N,
          optionRenderer: (opt) => slide.phase === "tutorial" ? numFingerCell(opt.value) : bigNumCell(opt.value),
          mastery: slide.phase === "mastery"
        });
      };
      const afterCount = ()=>{
        if(doMove){
          items.forEach((it,i)=>{ const keep = slide.phase === "tutorial" &&
              it.querySelector(".count-badge").textContent === String(N);
            if(!keep) it.querySelector(".count-badge").textContent = "";
            it.classList.add("moved");
            it.style.transform = `translate(${((i*53)%81)-40}px, ${((i*37)%61)-30}px) rotate(${((i*29)%25)-12}deg)`; });
          sfxTap();
          setTimeout(()=>{ play(audioFor(slide, "move") || null, ()=>{}); askOptions(); }, 950);
        } else {
          play(audioFor(slide, "ask") || null, ()=>{}); askOptions();
        }
      };
      items.forEach(it => {
        it.onclick = ()=>{
          if(it.classList.contains("counted") || it.classList.contains("moved")) return;   // one-to-one; inert once moved
          c++; it.classList.add("counted");
          it.querySelector(".count-badge").textContent = String(c);
          GameBus.emit("count_tap", { slide_id: slide.id, phase: slide.phase, n: c });
          if(c >= N){
            stopNudge();
            play("assets/Audio/vo_num_" + c + "." + AUDIO_EXT, ()=> setTimeout(()=>
              play("assets/Audio/vo_total_" + N + "." + AUDIO_EXT, ()=> setTimeout(afterCount, 450)), 300));
          } else {
            play("assets/Audio/vo_num_" + c + "." + AUDIO_EXT);
            nudgeNext();
          }
        };
      });
      state.replayAudio = ()=> play(audioFor(slide, c >= N ? (doMove ? "move" : "ask") : "prompt") || null, ()=>{});
      play(audioFor(slide, "prompt") || null, ()=>{});
      nudgeNext();
    }
  },

  COUNT_ACTION: {
    // S02 themed tap-count: tap each object and it ENACTS to a target while counting — pop (balloon
    // vanishes), feed (flies to the monster's mouth), or basket (drops into the basket). After the last
    // one the frozen "कुल N" plays and numeral options appear. data:{count, object, options, theme
    // ("pop"|"feed"|"basket")}. audio:{prompt, ask, try_again, hint, reveal}.
    mount(host, slide){
      const d = slide.data, N = d.count, obj = d.object, theme = d.theme || "pop";
      state.ownsAudio = true; setNavActive(false);
      const wrap = document.createElement("div"); wrap.className = "count-stage act act-" + theme;
      let target = null;
      if(theme === "feed"){ target = document.createElement("div"); target.className = "act-target act-monster"; target.textContent = "👹"; wrap.appendChild(target); }
      if(theme === "basket"){ target = document.createElement("div"); target.className = "act-target act-basket";
        target.innerHTML = imgOrEmoji("obj_basket", "🧺", "act-basket-img", "act-basket-emoji"); wrap.appendChild(target); }
      const row = document.createElement("div"); row.className = "count-row act-row" + (N > 8 ? " dense" : "");
      const items = []; let c = 0;
      for(let i=0;i<N;i++){ const it = document.createElement("div"); it.className = "count-item act-item";
        it.innerHTML = imgOrEmoji(obj.img, obj.emoji, "cobj-img", "cobj-emoji") + `<span class="count-badge"></span>`;
        row.appendChild(it); items.push(it); }
      wrap.appendChild(row); host.appendChild(wrap);
      const nudgeNext = ()=>{ const nx = items.find(x=>!x.classList.contains("done")); if(nx) pointNudgeAt(nx); else stopNudge(); };
      const askOptions = ()=>{ mountTapOptions({
        slide, host, signalName: "cardinality_first_try", stimulus: null, nudgeTarget: null,
        options: d.options, columnsHint: Math.min(d.options.length, 5),
        isCorrect: (opt) => opt.value === N,
        optionRenderer: (opt) => slide.phase === "tutorial" ? numFingerCell(opt.value) : bigNumCell(opt.value),
        mastery: slide.phase === "mastery" }); };
      items.forEach(it => {
        it.onclick = ()=>{
          if(it.classList.contains("done")) return;
          c++; it.classList.add("done", "act-go");   // act-go = fly/pop animation (theme-scoped CSS)
          it.querySelector(".count-badge").textContent = String(c);
          if(theme === "feed" && target) target.classList.add("chomp");
          sfxTap();
          GameBus.emit("count_tap", { slide_id: slide.id, phase: slide.phase, n: c });
          if(c >= N){
            stopNudge();
            play("assets/Audio/vo_num_" + c + "." + AUDIO_EXT, ()=> setTimeout(()=>
              play("assets/Audio/vo_total_" + N + "." + AUDIO_EXT, ()=> setTimeout(()=>{
                play(audioFor(slide, "ask") || null, ()=>{}); askOptions(); }, 450)), 300));
          } else { play("assets/Audio/vo_num_" + c + "." + AUDIO_EXT); nudgeNext(); }
        };
      });
      state.replayAudio = ()=> play(audioFor(slide, c >= N ? "ask" : "prompt") || null, ()=>{});
      play(audioFor(slide, "prompt") || null, ()=>{});
      nudgeNext();
    }
  },

  COUNT_DRAG_MATCH: {
    // S02 drag items. mode "num_to_box": count the set, then DRAG the correct NUMBER CARD into the
    // answer box (#2, #9). mode "obj_to_num": count, then DRAG the object onto the correct NUMBER (#11).
    // data:{count, object, options:[{value}], mode}. audio:{prompt, ask, try_again, reveal}.
    mount(host, slide){
      const d = slide.data, N = d.count, obj = d.object, mode = d.mode || "num_to_box";
      state.ownsAudio = true; setNavActive(false);
      const wrap = document.createElement("div"); wrap.className = "count-stage dragmatch";
      const setRow = document.createElement("div"); setRow.className = "count-row show-set" + (N > 8 ? " dense" : "");
      const items = []; let c = 0;
      for(let i=0;i<N;i++){ const it = document.createElement("div"); it.className = "count-item";
        it.innerHTML = imgOrEmoji(obj.img, obj.emoji, "cobj-img", "cobj-emoji") + `<span class="count-badge"></span>`;
        setRow.appendChild(it); items.push(it); }
      wrap.appendChild(setRow);
      const dz = document.createElement("div"); dz.className = "cdm-zone";   // built after counting
      const tray = document.createElement("div"); tray.className = "cdm-tray";
      wrap.appendChild(dz); wrap.appendChild(tray); host.appendChild(wrap);
      const nudgeNext = ()=>{ const nx = items.find(x=>!x.classList.contains("counted")); if(nx) pointNudgeAt(nx); else stopNudge(); };
      const settleWin = (revealed)=>{ state.locked = true;
        GameBus.emit("cardinality_first_try", { slide_id: slide.id, phase: slide.phase, value: !revealed, latency_ms: Date.now()-state.slideStart });
        celebrateThenAdvance(slide, revealed); };
      const buildDrag = ()=>{
        // shuffle the numeral options
        const opts = d.options.slice(); for(let i=opts.length-1;i>0;i--){ const j=(Math.random()*(i+1))|0; [opts[i],opts[j]]=[opts[j],opts[i]]; }
        if(mode === "obj_to_num"){
          // number cards are the DROP ZONES; a single draggable object-chip is the tile
          dz.className = "cdm-numrow";
          opts.forEach(o=>{ const z = document.createElement("div"); z.className = "cdm-numzone dd-zone"; z.dataset.val = String(o.value);
            z.innerHTML = `<span class="bignum-glyph">${devNumeral(o.value)}</span>`; dz.appendChild(z); });
          const tile = document.createElement("div"); tile.className = "cdm-objtile";
          tile.innerHTML = imgOrEmoji(obj.img, obj.emoji, "cobj-img", "cobj-emoji"); tray.appendChild(tile);
          makeDraggable(tile, (zone)=>{ if(state.locked || !zone) return;
            if(parseInt(zone.dataset.val,10) === N){ zone.classList.add("filled","correct"); tile.classList.add("snapped"); settleWin(false); }
            else { zone.classList.add("wrong"); setTimeout(()=>zone.classList.remove("wrong"),500); dragWrong(slide);
              state.attempts=(state.attempts||0)+1; if(state.attempts>=(CARD.scaffold_rules.max_attempts||3)){ const zc=[...dz.children].find(z=>parseInt(z.dataset.val,10)===N); if(zc){zc.classList.add("filled","correct","reveal-glow"); tile.classList.add("snapped"); play(audioFor(slide,"reveal")||null,()=>{}); settleWin(true);} } }
          });
        } else {
          // one BOX is the drop zone; number cards are the draggable tiles
          dz.className = "cdm-box dd-zone"; dz.innerHTML = `<span class="cdm-box-q">?</span>`;
          opts.forEach(o=>{ const tile = document.createElement("div"); tile.className = "cdm-card"; tile.dataset.val = String(o.value);
            tile.innerHTML = `<span class="bignum-glyph">${devNumeral(o.value)}</span>`; tray.appendChild(tile);
            makeDraggable(tile, (zone)=>{ if(state.locked || zone !== dz) return;
              if(o.value === N){ dz.classList.add("filled","correct"); dz.innerHTML = `<span class="bignum-glyph">${devNumeral(N)}</span>`; tile.classList.add("snapped"); settleWin(false); }
              else { dz.classList.add("wrong"); setTimeout(()=>dz.classList.remove("wrong"),500); dragWrong(slide);
                state.attempts=(state.attempts||0)+1; if(state.attempts>=(CARD.scaffold_rules.max_attempts||3)){ dz.classList.add("filled","correct","reveal-glow"); dz.innerHTML=`<span class="bignum-glyph">${devNumeral(N)}</span>`; play(audioFor(slide,"reveal")||null,()=>{}); settleWin(true); } }
            });
          });
        }
        play(audioFor(slide, "ask") || null, ()=>{});
      };
      items.forEach(it => { it.onclick = ()=>{ if(it.classList.contains("counted")) return;
        c++; it.classList.add("counted"); it.querySelector(".count-badge").textContent = String(c);
        GameBus.emit("count_tap", { slide_id: slide.id, phase: slide.phase, n: c });
        if(c >= N){ stopNudge(); play("assets/Audio/vo_num_"+c+"."+AUDIO_EXT, ()=> setTimeout(()=>
          play("assets/Audio/vo_total_"+N+"."+AUDIO_EXT, ()=> setTimeout(buildDrag, 450)), 300)); }
        else { play("assets/Audio/vo_num_"+c+"."+AUDIO_EXT); nudgeNext(); }
      }; });
      state.attempts = 0; state.locked = false;
      state.replayAudio = ()=> play(audioFor(slide, c >= N ? "ask" : "prompt") || null, ()=>{});
      play(audioFor(slide, "prompt") || null, ()=>{});
      nudgeNext();
    }
  },

  DEMO_COUNT: {
    // [16h] PHASE-1 AUTONOMOUS TEACH (the lead's 3-phase contract, 2026-07-17): the game counts
    // BY ITSELF — KG children who cannot count yet WATCH the counting happen. All N objects are
    // visible; the demo hand moves to each in turn; a BIG running count above updates 1..N with
    // vo_num_N per touch; then the conclusion line plays ("ये पाँच सेब हैं!") and आगे unlocks.
    // NO required interaction, NO options — never a test. Zero (N=0): empty tray, straight to the
    // conclusion ("यहाँ कुछ नहीं — शून्य!"). data:{count, object} audio:{prompt?, conclude}
    mount(host, slide){
      const d = slide.data, N = d.count, obj = d.object;
      state.ownsAudio = true; setNavActive(false); setSwMood("teach");
      const wrap = document.createElement("div"); wrap.className = "demo-stage";
      const counter = document.createElement("div"); counter.className = "demo-count";
      counter.textContent = N === 0 ? "0" : "";
      const row = document.createElement("div"); row.className = "count-row demo-row" + (N > 8 && !d.per_row ? " dense" : "");
      if(d.per_row){ row.classList.add("perrow"); row.style.gridTemplateColumns = `repeat(${d.per_row}, auto)`; }
      const items = [];
      for(let k = 0; k < N; k++){
        const it = document.createElement("div"); it.className = "count-item demo-item";
        it.innerHTML = imgOrEmoji(obj.img, obj.emoji, "cobj-img", "cobj-emoji") + `<span class="count-badge"></span>`;
        row.appendChild(it); items.push(it);
      }
      if(N === 0){ row.classList.add("demo-empty"); }
      wrap.appendChild(counter); wrap.appendChild(row); host.appendChild(wrap);
      let i = 0;
      const conclude = ()=>{ stopNudge();
        play(audioFor(slide, "conclude") || null, ()=> setNavActive(true)); };
      const step = ()=>{
        if(state.idx !== undefined && CARD.slides[state.idx] !== slide) return;   // slide changed — stop
        if(i >= N){ setTimeout(conclude, 400); return; }
        const it = items[i];
        it.classList.add("counted", "demo-hit");
        it.querySelector(".count-badge").textContent = String(i + 1);
        counter.textContent = String(i + 1);
        counter.classList.remove("demo-pop"); void counter.offsetWidth; counter.classList.add("demo-pop");
        pointNudgeAt(it);
        i++;
        play("assets/Audio/vo_num_" + i + "." + AUDIO_EXT, ()=> setTimeout(step, 420));
      };
      play(audioFor(slide, "prompt") || null, ()=> setTimeout(step, 500));
      state.replayAudio = ()=> play(audioFor(slide, i >= N ? "conclude" : "prompt") || null, ()=>{});
    }
  },

  MEET_NUMBER: {
    mount(host, slide){
      if(slide.data && slide.data.present === "crane"){ return btCraneMeet(host, slide); }   // Block Town teach
      const wrap = document.createElement("div"); wrap.className = "meet-stage number-meet";
      const n = slide.data.count;
      // [16d] dual-code the numeral: hands for 1..5; for bigger numbers (teens) the Hindi number WORD.
      // Never the numeral twice — fingerCount's out-of-range fallback IS the numeral, which rendered
      // the "12 over 12" teach card the SME flagged on MTKGA01_L01_S04.
      const word = (slide.data.numerals || [])[n-1] || "";
      const second = (n>=1 && n<=5) ? fingerCount(n,'meet-hand') : (word ? `<span class="num-word">${word}</span>` : "");
      wrap.innerHTML = `
        <div class="meet-number-box"><span class="num-glyph">${n}</span>${second}</div>
        <div class="meet-arrow">→</div>`;
      // [16d] the teach set honors data.per_row (rows of 10 → a teen visibly reads as ten-and-ones)
      const setEl = stimulusCountSet(n, slide.data.object, false, slide.data.per_row);
      setEl.classList.add("meet-set");
      wrap.appendChild(setEl);
      host.appendChild(wrap);
      state.gateNavUntilAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
    }
  },

  COUNT_HOW_MANY: {
    mount(host, slide){
      const setEl = stimulusCountSet(slide.data.count, slide.data.object, slide.data.scatter, slide.data.per_row);
      mountTapOptions({
        slide, host, signalName: "cardinality_first_try",
        stimulus: setEl,
        nudgeTarget: null,   // nothing to re-tap here → no idle hand
        options: slide.data.options,
        columnsHint: Math.min(slide.data.options.length, 5),
        isCorrect: (opt) => opt.value === slide.data.count,
        // SME (S01 review deck): finger-hands are a TUTORIAL teaching aid only — in guided/
        // independent/practice/mastery the options are the NUMBER ALONE, larger.
        optionRenderer: (opt) => slide.phase === "tutorial" ? numFingerCell(opt.value) : bigNumCell(opt.value),
        mastery: slide.phase === "mastery",
        // HINT = count the set FOR the child (highlight + say एक/दो/तीन + numeral on top)
        hintAction: (done) => demoCountSet(setEl, slide.data.count, slide.data.numerals, done)
      });
    }
  },

  PICK_SET_BY_NUMBER: {
    // SME-designed REVERSE how-many (S01 review deck, new pages): a big NUMBER is the stimulus;
    // the options are small OBJECT SETS — tap the set with that many. Speak-on-tap = each set's own
    // count line ("इसमें तीन चीज़ें हैं।"), which doubles as the SME's wrong-tap hint; the ladder then
    // runs try_again → hint → reveal-glow as everywhere. data:{target, options:[{count, object:{img,emoji},
    // audio, correct}]}.
    mount(host, slide){
      const d = slide.data;
      const stim = document.createElement("div"); stim.className = "psn-stimulus";
      stim.innerHTML = `<span class="psn-num">${devNumeral(d.target)}</span>`;
      mountTapOptions({
        slide, host, signalName: "pick_set_first_try",
        stimulus: stim,
        nudgeTarget: null,
        options: d.options,
        columnsHint: Math.min(d.options.length, 3),
        isCorrect: (opt) => opt.correct === true,
        optionRenderer: (opt) => {
          const c = document.createElement("div"); c.className = "psn-cell";
          let inner = "";
          for(let i=0;i<opt.count;i++) inner += `<span class="psn-obj">${imgOrEmoji(opt.object.img, opt.object.emoji, "psn-img", "psn-emoji")}</span>`;
          c.innerHTML = `<div class="psn-set">${inner}</div>`;
          return c;
        },
        mastery: slide.phase === "mastery"
      });
    }
  },

  MAKE_SET: {
    mount(host, slide){
      const N = slide.data.target, obj = slide.data.object;
      const wrap = document.createElement("div"); wrap.className = "makeset-stage";
      wrap.innerHTML = `
        <div class="makeset-target"><span class="ms-label">डालो</span><span class="num-glyph">${devNumeral(slide.data.target)}</span>${imgOrEmoji(obj.img, obj.emoji, "ms-goal-obj", "ms-goal-emoji")}</div>
        <div class="makeset-frame" id="msFrame"></div>
        <button class="makeset-add" id="msAdd"><span class="ms-add-plus">＋</span>${imgOrEmoji(obj.img, obj.emoji, "ms-add-obj", "ms-add-emoji")}</button>`;
      host.appendChild(wrap);
      const frame = wrap.querySelector("#msFrame"), addBtn = wrap.querySelector("#msAdd");
      const numerals = slide.data.numerals || [];
      const MAXITEMS = 5;                          // never allow more than 5
      let c = 0; state.attempts = 0; state.locked = false; state.hintActive = false;
      const refreshNav = ()=> setNavActive(!state.locked && !state.hintActive && c === N);  // आगे activates ONLY at exactly N — no premature/wrong submit; child self-corrects by adding more / removing (×). Nudge on the add-button guides an idle child.
      function makeItem(){
        const it = document.createElement("div"); it.className = "ms-item";
        it.innerHTML = imgOrEmoji(obj.img, obj.emoji, "cobj-img", "cobj-emoji") + `<span class="ms-del" aria-label="हटाओ">×</span>`;
        const remove = (e)=>{ if(e) e.stopPropagation(); if(state.locked || state.hintActive) return; it.remove(); c--; refreshNav(); };
        // remove ONLY via the explicit × badge — tapping the object itself must NOT delete it
        // (the count tutorial teaches "tap the object to count it"; a placed apple that vanishes on tap
        //  would silently destroy the child's work)
        it.querySelector(".ms-del").onclick = remove;
        frame.appendChild(it); return it;
      }
      addBtn.onclick = ()=>{
        if(state.locked || state.hintActive) return;
        if(c >= MAXITEMS){ addBtn.classList.add("shake"); setTimeout(()=> addBtn.classList.remove("shake"), 420); return; }  // cap at 5
        c++; makeItem();
        play("assets/Audio/vo_num_" + c + "." + AUDIO_EXT);   // count up as you add
        GameBus.emit("make_set_add", { slide_id: slide.id, count: c });
        refreshNav();
      };
      // HINT = count what the child actually placed (highlight + say the number)
      const runHint = (after)=>{
        state.hintActive = true; refreshNav();
        demoCount([...frame.querySelectorAll(".ms-item")], numerals, ()=>{ state.hintActive = false; refreshNav(); if(after) after(); });
      };
      $("hintBtn").onclick = ()=>{ if(state.locked || state.hintActive) return;
        GameBus.emit("hint_shown", { slide_id: slide.id, manual: true }); runHint(); };
      // आगे = SUBMIT. correct → celebrate & advance. wrong → graduated scaffold, same as
      // everywhere: 1st = try again, 2nd = count-demo hint, 3rd = REVEAL (auto-fix to N,
      // count 1..N automatically, then move to the next slide).
      $("navBtn").onclick = ()=>{
        if(state.locked || state.hintActive || c !== N) return;   // gated to exactly N → only the correct-set path runs (self-correcting design)
        if(c === N){
          state.locked = true; refreshNav();
          GameBus.emit("make_set_correct", { slide_id: slide.id, phase: slide.phase,
            value: true, target: N, attempts: state.attempts + 1, latency_ms: Date.now()-state.slideStart });
          play("assets/Audio/vo_total_" + N + "." + AUDIO_EXT, ()=>
            celebrateThenAdvance(slide, false));   // standard: confetti + VO + auto-advance, no popup
          return;
        }
        state.attempts++;
        GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts, made: c, target: N });
        const maxA = (CARD.scaffold_rules && CARD.scaffold_rules.max_attempts) || 3;
        $("hintBtn").classList.add("show","hint-glow");
        if(state.attempts >= maxA){
          // 3rd wrong → reveal: correct the set to exactly N, count it 1..N, then advance
          state.locked = true; state.scaffoldLevel = 3; refreshNav();
          while(frame.querySelectorAll(".ms-item").length > N) frame.querySelector(".ms-item:last-child").remove();
          while(frame.querySelectorAll(".ms-item").length < N) makeItem();
          c = N;
          GameBus.emit("answer_revealed", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
          state.hintActive = true;
          // count the (now-correct) set 1..N, then say the total "कुल N", then advance
          demoCount([...frame.querySelectorAll(".ms-item")], numerals, ()=>{
            state.hintActive = false;
            play("assets/Audio/vo_total_" + N + "." + AUDIO_EXT, ()=> setTimeout(()=> completeSlide(false), 500));
          });
        } else if(state.attempts === 2){
          runHint();                                                   // 2nd wrong → count what they made
        } else {
          // 1st wrong → try again, WITH the spoken VO (was silent)
          showBox("", audioText(slide,"try_again") || "फिर से कोशिश करो।", "wrong", wrongClip(slide), ()=>{});   /* [28i] graded: hint1 on rung 1 */
        }
      };
      setNavActive(false);
      pointNudgeAt(addBtn);
    }
  },

  COMPARE_SETS: {
    // Two visible groups, TWO picture options — the child taps the object that has MORE (or LESS).
    // No बराबर chip (lead review): equality is taught in MEET_COMPARE + produced on the see-saw, so
    // a judge question always has one clear answer between the two objects. Tap-to-answer: a wrong
    // tap buzzes + crosses + locks that card; the right one confetti-cheers + advances.
    mount(host, slide){
      const d = slide.data;
      const stage = stimulusCompareSets(d);
      // JUDGE (test): hide the "मिलाओ" reveal button — its one-to-one reveal + leftover glow gives the
      // answer away (and on a "less" question it glows the MORE set, pointing at the WRONG option).
      // The two rows stay visible so the child still compares by eye. (Reveal stays only on MEET_COMPARE.)
      const mb = stage.querySelector(".cmp-match-btn"); if(mb) mb.style.display = "none";
      const answer = (d.ask === "less") ? (d.a_count < d.b_count ? "a" : "b")
                                        : (d.a_count > d.b_count ? "a" : "b");
      const options = [ {kind:"a", obj:d.a_object}, {kind:"b", obj:d.b_object} ];
      // (option shuffle is now centralized in mountTapOptions — no per-module reverse needed)
      mountTapOptions({
        slide, host, signalName: "compare_first_try",
        stimulus: stage,
        nudgeTarget: null,
        options,
        columnsHint: 2,
        isCorrect: (opt)=> opt.kind === answer,
        optionRenderer: (opt)=>{
          const cell = document.createElement("div");
          cell.innerHTML = imgOrEmoji(opt.obj.img, opt.obj.emoji, "pic-img", "cmp-chip-emoji")
            + `<span class="cmp-chip-lbl">${opt.obj.word_hi || ""}</span>`;
          return cell;
        },
        mastery: slide.phase === "mastery"
      });
    }
  },

  MEET_COMPARE: {
    // TEACH BY DOING (lead review): the child COUNTS each group by tapping its objects one-by-one
    // (running numeral + spoken एक/दो/तीन), the top group then the bottom. Then the one-to-one
    // match reveals, the leftover glows, and Swiftie EXPLAINS the outcome by name — e.g.
    // "एक सेब बच गया, सेब ज़्यादा हैं, केले कम" / "कुछ नहीं बचा, दोनों बराबर". आगे appears after.
    mount(host, slide){
      const d = slide.data;
      const wrap = document.createElement("div"); wrap.className = "meet-compare";
      const stage = stimulusCompareSets({a_object:d.a_object, a_count:d.a_count,
                                          b_object:d.b_object, b_count:d.b_count, show_matches:false});
      const mb = stage.querySelector(".cmp-match-btn"); if(mb) mb.style.display = "none";
      const verdict = document.createElement("div");
      verdict.className = "cmp-verdict " + (d.outcome || "more");
      verdict.textContent = d.label_hi || "";
      wrap.appendChild(stage); wrap.appendChild(verdict);
      host.appendChild(wrap);

      state.gateNavUntilAudio = false; state.locked = false; state.ownsAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=>{ if(state.locked) completeSlide(true); };

      // 🔊 replay: re-hear the teach line (and, once revealed, the explanation). autoPlayChain skips
      // count_intro/explain, so without this the header chip would be silent on teach slides.
      let revealed = false;
      state.replayAudio = ()=>{ const chain = [audioFor(slide, "count_intro")];
        if(revealed) chain.push(audioFor(slide, "explain"));
        playChain(chain.filter(Boolean), 0); };

      const rowA = [...stage.querySelectorAll(".cmp-row.top .cobj")];
      const rowB = [...stage.querySelectorAll(".cmp-row.bot .cobj")];

      // make one row countable-by-tapping; cb fires once every item in it is counted
      function countRow(items, cb){
        const nudgeNext = ()=>{ const nx = items.find(o=>!o.classList.contains("counted"));
          if(nx) pointNudgeAt(nx); else stopNudge(); };
        let n = 0;
        items.forEach(o=>{
          o.classList.add("tappable");
          o.onclick = ()=>{
            if(state.locked || o.classList.contains("counted")) return;
            o.classList.add("counted", "counting"); n++; sfxTap();
            let cal = o.querySelector(".count-callout");
            if(!cal){ cal = document.createElement("span"); cal.className = "count-callout"; o.appendChild(cal); }
            cal.textContent = n;
            play("assets/Audio/vo_num_" + n + "." + AUDIO_EXT, ()=>{});
            if(items.every(x=>x.classList.contains("counted"))){ stopNudge(); setTimeout(cb, 550); }
            else nudgeNext();
          };
        });
        nudgeNext();
        // [16h] Phase-1 autonomous mode (lead's 3-phase contract): the demo hand counts the row
        // BY ITSELF — drives the same handlers a child would, so behavior is identical.
        if(slide.data.auto){
          items.forEach(o=> o.classList.remove("tappable"));
          let ai = 0;
          (function autoTap(){
            if(CARD.slides[state.idx] !== slide || ai >= items.length) return;
            const o = items[ai++]; pointNudgeAt(o); if(o.onclick) o.onclick();
            setTimeout(autoTap, 950);
          })();
        }
      }

      // intro VO → count group A → count group B → reveal match + explain the outcome.
      // NB: uses non-autochain role names (count_intro / explain) so mountSlide's autoPlayChain
      // does NOT also fire the intro — this module owns its own audio sequence.
      play(audioFor(slide, "count_intro") || null, ()=>{
        countRow(rowA, ()=> countRow(rowB, ()=>{
          stage._revealMatches(()=>{
            verdict.classList.add("show","hint-glow"); setSwMood("point");
            state.locked = true; revealed = true; setNavActive(true);
            play(audioFor(slide, "explain") || null, ()=>{});
          });
        }));
      });
    }
  },

  MAKE_EQUAL: {
    // PRODUCE mechanic (see-saw): the left pan holds a fixed group; the child taps + जोड़ो to
    // add to the right pan (tap an added item to take it back). The beam tilts toward the heavier
    // side in real time; at equal it levels, locks, celebrates. Overshoot is enacted (invite to
    // remove), never a red ✗ — the KG "produce, don't pick" model.
    mount(host, slide){
      const d = slide.data, L = d.a_count, fixedObj = d.a_object, addObj = d.b_object;
      const MAXR = d.max || Math.max(L + 2, 6);
      const wrap = document.createElement("div"); wrap.className = "balance-stage";
      wrap.innerHTML = `
        <div class="balance">
          <div class="beam-wrap" id="beamWrap"><div class="beam"></div>
            <div class="pan pan-left"><div class="pan-grid" id="panL"></div></div>
            <div class="pan pan-right"><div class="pan-grid" id="panR"></div></div></div>
          <div class="fulcrum"></div>
        </div>
        <button class="balance-add" id="balAdd" type="button"></button>`;
      host.appendChild(wrap);
      const panL = wrap.querySelector("#panL"), panR = wrap.querySelector("#panR");
      const beam = wrap.querySelector("#beamWrap"), addBtn = wrap.querySelector("#balAdd");
      const balance = wrap.querySelector(".balance");
      addBtn.innerHTML = imgOrEmoji(addObj.img, addObj.emoji, "cobj-img", "cobj-emoji") + `<span>+ जोड़ो</span>`;
      for(let i=0;i<L;i++){ const c=document.createElement("span"); c.className="cobj";
        c.innerHTML = imgOrEmoji(fixedObj.img, fixedObj.emoji, "cobj-img", "cobj-emoji"); panL.appendChild(c); }
      let right = 0; state.locked = false; state.attempts = 0; let tipT = 0;
      const TILT = 6, TMAX = 15;
      const tilt = ()=>{ const diff = right - L; const deg = Math.max(-TMAX, Math.min(TMAX, diff*TILT));
        beam.style.transform = `translateX(-50%) rotate(${deg}deg)`; balance.classList.toggle("level", diff===0 && right>0); };
      const check = ()=>{ if(state.locked) return; const diff = right - L;
        if(diff===0 && right>0){ state.locked = true; setNavActive(true);
          GameBus.emit("make_equal_correct", { slide_id: slide.id, phase: slide.phase, value: true,
            count: right, target: L, attempts: state.attempts + 1, latency_ms: Date.now()-state.slideStart });
          showBox("⚖️", audioText(slide,"balanced") || "बराबर! दोनों बराबर हैं।", "correct", audioFor(slide,"balanced") || null, ()=>{});
        } else if(diff > 0){ state.attempts++;
          GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, made: right, target: L });
          if(Date.now()-tipT > 1200){ tipT = Date.now();
            showBox("", audioText(slide,"too_many") || "बहुत ज़्यादा! एक हटाओ।", "hint", audioFor(slide,"too_many") || wrongClip(slide), ()=>{}); } }   /* [28i] ladder fallback */
      };
      const addItem = ()=>{ const c=document.createElement("span"); c.className="cobj added";
        c.innerHTML = imgOrEmoji(addObj.img, addObj.emoji, "cobj-img", "cobj-emoji");
        c.onclick = ()=>{ if(state.locked) return; c.remove(); right = Math.max(0, right-1); tilt(); check(); };
        panR.appendChild(c); right++; };
      addBtn.onclick = ()=>{ if(state.locked) return;
        if(right >= MAXR){ addBtn.classList.add("shake"); setTimeout(()=> addBtn.classList.remove("shake"), 400); return; }
        addItem(); tilt(); sfxTap();
        // count EVERY added item aloud INCLUDING the final/target one (एक, दो, तीन) — then, on the
        // last count, the "बराबर" VO follows (check runs in the count's onEnd so the number isn't cut).
        if(right <= L) play("assets/Audio/vo_num_" + right + "." + AUDIO_EXT, right === L ? ()=> check() : ()=>{});
        else check();   // overshoot → "एक हटाओ" hint
      };
      setNavActive(false);
      $("navBtn").onclick = ()=>{ if(state.locked) completeSlide(true); };
      tilt();                 // START tilted toward the heavier (left) group — the see-saw is NOT level yet
      pointNudgeAt(addBtn);
    }
  },

  MEET_PATTERN: {
    // TEACH: show a repeating pattern and pulse the repeating UNIT (first data.unit_len cells) a few
    // times so the child sees "this part comes again". Nav gated on the VO, like MEET_NUMBER.
    mount(host, slide){
      const d = slide.data;
      const wrap = document.createElement("div"); wrap.className = "pattern-stage";
      const lbl = document.createElement("div"); lbl.className = "pat-unit-lbl"; lbl.textContent = "यह हिस्सा दोहराता है 🔁";
      const row = document.createElement("div"); row.className = "pattern-row";
      d.items.forEach(o=>{ const c = document.createElement("div"); c.className = "pat-cell";
        c.innerHTML = imgOrEmoji(o.img, o.emoji, "cobj-img", "cobj-emoji"); row.appendChild(c); });
      wrap.appendChild(lbl); wrap.appendChild(row); host.appendChild(wrap);
      state.gateNavUntilAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
      const cells = [...row.children]; let rep = 0;
      const glow = ()=>{ cells.forEach((c,i)=> { if(i < d.unit_len) c.classList.add("unit-glow"); });
        setTimeout(()=> cells.forEach(c=> c.classList.remove("unit-glow")), 1100); };
      glow(); const t = setInterval(()=>{ if(rep++ >= 2){ clearInterval(t); return; } glow(); }, 1700);
    }
  },

  PATTERN_BUILD: {
    // PRODUCE: a pattern with empty ghost slot(s) — at the END (extend) or in the MIDDLE (fill the
    // gap). Tap a tray item to drop it into the active slot; the correct item = data.items[slot].
    // Wrong taps bounce (enacted, no ✗). Fill every blank → complete. data:{items[],blanks[],tray[]}.
    mount(host, slide){
      const d = slide.data;
      const wrap = document.createElement("div"); wrap.className = "pattern-stage";
      const row = document.createElement("div"); row.className = "pattern-row";
      const cells = d.items.map((o,i)=>{
        const c = document.createElement("div");
        if(d.blanks.includes(i)){ c.className = "pat-ghost"; c.innerHTML = `<span class="qmark">?</span>`; }
        else { c.className = "pat-cell"; c.innerHTML = imgOrEmoji(o.img, o.emoji, "cobj-img", "cobj-emoji"); }
        row.appendChild(c); return c;
      });
      const tray = document.createElement("div"); tray.className = "pattern-tray";
      d.tray.forEach(o=>{ const t = document.createElement("div"); t.className = "pat-tray-item"; t._obj = o;
        t.innerHTML = imgOrEmoji(o.img, o.emoji, "cobj-img", "cobj-emoji"); tray.appendChild(t); });
      wrap.appendChild(row); wrap.appendChild(tray); host.appendChild(wrap);
      const blanks = d.blanks.slice(); let bi = 0, wrongStreak = 0, revealedAny = false;
      state.locked = false; state.attempts = 0;
      const key = (o)=> o.img || o.emoji;
      const activeGhost = ()=> cells[blanks[bi]];
      const markActive = ()=>{ cells.forEach(c=> c.classList.remove("active"));
        // idle nudge points at the ACTIVE BLANK ('?' slot = "put one here"), re-armed per blank —
        // NEVER at a tray answer; startNudge is phase-aware so it's silent in practice/mastery.
        if(bi < blanks.length){ activeGhost().classList.add("active"); startNudge(slide, activeGhost()); } else stopNudge(); };
      const flashHint = ()=>{ const want = d.items[blanks[bi]], g = activeGhost(); const prev = g.innerHTML;
        g.innerHTML = imgOrEmoji(want.img, want.emoji, "cobj-img", "cobj-emoji"); g.style.opacity = ".4";
        setTimeout(()=>{ if(g.classList.contains("pat-ghost")){ g.innerHTML = prev; g.style.opacity = ""; } }, 950); };
      const placeCorrect = ()=>{                      // one placement path (tap AND reveal)
        clearHold(tray);                                     /* [28l] release the terminal hold */
        const want = d.items[blanks[bi]], g = activeGhost();
        g.className = "pat-cell"; g.innerHTML = imgOrEmoji(want.img, want.emoji, "cobj-img", "cobj-emoji");
        g.classList.add("unit-glow"); setTimeout(()=> g.classList.remove("unit-glow"), 700); bi++;
        if(bi >= blanks.length){
          state.locked = true; stopNudge();
          GameBus.emit("pattern_extend_correct", { slide_id: slide.id, phase: slide.phase, value: !revealedAny,
            attempts: state.attempts + 1, latency_ms: Date.now()-state.slideStart });
          // engine standard: confetti + cheer + correct VO + AUTO-advance — no popup, no आगे gate.
          celebrateThenAdvance(slide, revealedAny);
        } else markActive();
      };
      markActive();
      tray.querySelectorAll(".pat-tray-item").forEach(t=>{
        t.onclick = ()=>{
          if(state.locked || bi >= blanks.length) return;
          stopNudge();
          const want = d.items[blanks[bi]];
          if(key(t._obj) === key(want)){
            wrongStreak = 0;
            placeCorrect();
          } else {
            state.attempts++;
            t.classList.add("shake"); setTimeout(()=> t.classList.remove("shake"), 420);
            activeGhost().classList.add("shake"); setTimeout(()=> activeGhost().classList.remove("shake"), 420);
            GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
            $("hintBtn").classList.add("show","hint-glow");
            // layered ladder, standard-aligned: L1 spoken try-again (buzz + Swiftie, no popup) →
            // L2 flash the answer ghost + spoken hint → L3 reveal ceiling: DEMONSTRATE the placement.
            if(++wrongStreak >= (CARD.scaffold_rules.max_attempts||3)){
              revealedAny = true; wrongStreak = 0;
              activeGhost().classList.add("reveal-glow");
              play(audioFor(slide,"reveal") || audioFor(slide,"hint") || null, ()=>{});
              /* [28l] was: setTimeout(placeCorrect, 1000) — the engine ANSWERED for the child. */
              if(maySolveFor(slide)) setTimeout(()=>{ placeCorrect(); }, 1000);
              else terminalHold([...tray.children].find(x=> key(x._obj) === key(d.items[blanks[bi]])
                                  && !x.classList.contains("used")), tray.children, slide);
            }
            else if(state.attempts >= 2){ flashHint(); play(midHint(slide), ()=>{}); }   /* [28k] rung 2 */
            else dragWrong(slide);
          }
        };
      });
      setNavActive(false);
      $("navBtn").onclick = ()=>{};   // completion is automatic now — आगे never gates a solved pattern
      $("hintBtn").onclick = ()=>{ if(!state.locked && bi < blanks.length) flashHint(); };
      // NB: the idle nudge is armed by markActive() → startNudge(activeGhost) above — it points at the
      // BLANK, phase-aware. (Bug fix: was pointNudgeAt(first tray tile) = an immediate hand on the WRONG
      // answer on most slides, and it showed even in mastery.)
    }
  },

  /* ===== NUMBER-SEQUENCE PATH (MTKGA01_L02_S04 — "completes a number sequence within 20") =====
     Three additive modules that share the .seq-* number-path skin. Numerals are crisp text glyphs
     (Baloo), only the tile chrome is rounded — content-true geometry (never round the number). */

  MEET_SEQUENCE: {
    // TEACH BY DOING: a number path; a token sits on the first cell. The child taps the glowing NEXT
    // cell to hop the token forward, each number spoken (vo_num_N) with an ascending thunk — so the
    // child ENACTS "numbers move forward one step at a time" (curriculum teach spec). Nav gates until
    // the token reaches the end, then Swiftie's explain line plays. data:{path:[n…], token?}.
    mount(host, slide){
      const d = slide.data, nums = d.path;
      state.ownsAudio = true; setNavActive(false); setSwMood("teach");
      const stage = document.createElement("div"); stage.className = "seq-stage";
      const path  = document.createElement("div"); path.className = "seq-path";
      const cw = nums.length > 7 ? 74 : 90;
      const cells = nums.map((n,i)=>{
        if(i){ const con = document.createElement("div"); con.className = "seq-connector"; path.appendChild(con); }
        const cell = document.createElement("div"); cell.className = "seq-cell";
        cell.style.width = cell.style.height = cw+"px"; cell.style.fontSize = Math.round(cw*0.56)+"px";
        cell.textContent = n; path.appendChild(cell); return cell;
      });
      stage.appendChild(path); host.appendChild(stage);
      const token = document.createElement("span"); token.className = "seq-token"; token.textContent = d.token || "🐤";
      let pos = 0;
      const place = ()=>{ cells.forEach((c,i)=> c.classList.toggle("lit", i <= pos));
        if(!cells[pos].contains(token)) cells[pos].appendChild(token); };
      const glowNext = ()=>{ cells.forEach((c,i)=> c.classList.toggle("active", i === pos+1));
        if(pos+1 < cells.length) startNudge(slide, cells[pos+1]); else stopNudge(); };
      place(); btThunk(1); play("assets/Audio/vo_num_" + nums[0] + "." + AUDIO_EXT, ()=>{}); glowNext();
      const advance = ()=>{
        if(pos >= cells.length-1) return;
        pos++; cells[pos].classList.remove("active"); place(); btThunk(pos+1);
        play("assets/Audio/vo_num_" + nums[pos] + "." + AUDIO_EXT, ()=>{});
        if(pos >= cells.length-1){ stopNudge();
          GameBus.emit("meet_sequence_done", { slide_id: slide.id, phase: slide.phase });
          setTimeout(()=> play(audioFor(slide, "explain") || null, ()=> setNavActive(true)), 500);
        } else glowNext();
      };
      cells.forEach((c,i)=>{ c.onclick = ()=>{ if(i === pos+1) advance(); }; });
      // 🔊 replay re-speaks the current number (module owns its audio; autoPlayChain is skipped)
      state.replayAudio = ()=> play("assets/Audio/vo_num_" + nums[pos] + "." + AUDIO_EXT, ()=>{});
      $("navBtn").onclick = ()=> completeSlide(true);
    }
  },

  SEQUENCE_COMPLETE: {
    // PRODUCE test: a number path with blank(s); tap a tray numeral into the active blank. Correct =
    // path[blankIdx]. Wrong = shake + soft buzz + spoken try_again; reveal (demonstrate) after
    // max_attempts. Fills left→right. data:{path:[n… , with the blank positions still holding the true
    // number], blanks:[idx…], tray:[n…] (numerals incl. misconception distractors)}.
    mount(host, slide){
      const d = slide.data;
      const stage = document.createElement("div"); stage.className = "seq-stage";
      const path  = document.createElement("div"); path.className = "seq-path";
      const cw = d.path.length > 7 ? 74 : 90;
      const cells = d.path.map((n,i)=>{
        if(i){ const con = document.createElement("div"); con.className = "seq-connector"; path.appendChild(con); }
        const cell = document.createElement("div");
        cell.style.width = cell.style.height = cw+"px"; cell.style.fontSize = Math.round(cw*0.56)+"px";
        if(d.blanks.includes(i)){ cell.className = "seq-cell seq-ghost"; cell.innerHTML = '<span class="seq-q">?</span>'; }
        else { cell.className = "seq-cell filled"; cell.textContent = n; }
        path.appendChild(cell); return cell;
      });
      const tray = document.createElement("div"); tray.className = "seq-tray";
      d.tray.forEach(n=>{ const t = document.createElement("div"); t.className = "seq-tile"; t._num = n; t.textContent = n; tray.appendChild(t); });
      /* [27j] OPT-IN PICTURE STIMULUS. HIKGH04_L02_S02's deck asks "Give the Picture of house/tap/
         BUS/JUG" on all 4 build-the-word slides, and the module had nowhere to hang one — it read
         only path/blanks/tray and never called mountTapOptions, so authoring d.img was inert.
         Reuses the same stimulusPic() every other module uses, so the picture looks identical to the
         rest of the fleet. Purely additive: a card without img/picture/emoji renders exactly as before,
         and .seq-stage is already a flex column so the picture simply stacks above the path. */
      if(d.img || d.picture || d.emoji){
        stage.appendChild(stimulusPic(d.picture, d.emoji, d.img));
      }
      stage.appendChild(path); stage.appendChild(tray); host.appendChild(stage);

      const blanks = d.blanks.slice(); let bi = 0, wrongStreak = 0, revealedAny = false;
      state.locked = false; state.attempts = 0;
      const activeGhost = ()=> cells[blanks[bi]];
      const markActive = ()=>{ cells.forEach(c=> c.classList.remove("active"));
        if(bi < blanks.length){ activeGhost().classList.add("active"); startNudge(slide, activeGhost()); } else stopNudge(); };
      const placeCorrect = ()=>{
        clearHold(tray);                                     /* [28l] release the terminal hold */
        const want = d.path[blanks[bi]], g = activeGhost();
        g.className = "seq-cell filled unit-glow"; g.textContent = want; setTimeout(()=> g.classList.remove("unit-glow"), 700);
        const tile = [...tray.children].find(x=> x._num === want && !x.classList.contains("used")); if(tile) tile.classList.add("used");
        bi++;
        if(bi >= blanks.length){
          state.locked = true; stopNudge();
          GameBus.emit("sequence_complete_correct", { slide_id: slide.id, phase: slide.phase, value: !revealedAny,
            attempts: state.attempts + 1, latency_ms: Date.now()-state.slideStart });
          celebrateThenAdvance(slide, revealedAny);
        } else markActive();
      };
      markActive();
      tray.querySelectorAll(".seq-tile").forEach(t=>{
        t.onclick = ()=>{
          if(state.locked || bi >= blanks.length || t.classList.contains("used")) return;
          stopNudge();
          if(t._num === d.path[blanks[bi]]){ wrongStreak = 0; placeCorrect(); }
          else {
            state.attempts++;
            t.classList.add("shake"); setTimeout(()=> t.classList.remove("shake"), 420);
            activeGhost().classList.add("shake"); setTimeout(()=> activeGhost().classList.remove("shake"), 420);
            GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
            $("hintBtn").classList.add("show","hint-glow");
            if(++wrongStreak >= (CARD.scaffold_rules.max_attempts || 3)){
              revealedAny = true; wrongStreak = 0;
              activeGhost().classList.add("reveal-glow");
              play(audioFor(slide, "reveal") || audioFor(slide, "hint") || null, ()=>{});
              /* [28l] was: setTimeout(placeCorrect, 1000) — the engine ANSWERED for the child. */
              if(maySolveFor(slide)) setTimeout(()=> placeCorrect(), 1000);
              else terminalHold([...tray.children].find(x=> x._num === d.path[blanks[bi]]
                                  && !x.classList.contains("used")), tray.children, slide);
            } else dragWrong(slide);
          }
        };
      });
      setNavActive(false); $("navBtn").onclick = ()=>{};   // completion is automatic — never gate a solved path
      $("hintBtn").onclick = ()=>{ if(!state.locked && bi < blanks.length){ const g = activeGhost();
        g.classList.add("reveal-glow"); setTimeout(()=> g.classList.remove("reveal-glow"), 800); } };
    }
  },

  SEQUENCE_NEXT: {
    // PICK test (what comes next / before): a number path with ONE '?' cell (null in data.path) is the
    // stimulus; the child taps the correct numeral option. Reuses mountTapOptions → full tap-to-answer
    // contract (wrong=buzz+✗+lock+try_again, right=confetti+advance) + speak-the-number-on-tap +
    // mastery scoring. data:{path:[n…,null,…], options:[{num, audio:"vo_num_N", correct}]}.
    mount(host, slide){
      const d = slide.data;
      const stim = document.createElement("div"); stim.className = "seq-stage";
      const path = document.createElement("div"); path.className = "seq-path";
      const cw = d.path.length > 7 ? 74 : 90;
      d.path.forEach((n,i)=>{
        if(i){ const con = document.createElement("div"); con.className = "seq-connector"; path.appendChild(con); }
        const cell = document.createElement("div");
        cell.style.width = cell.style.height = cw+"px"; cell.style.fontSize = Math.round(cw*0.56)+"px";
        if(n === null){ cell.className = "seq-cell seq-ghost active"; cell.innerHTML = '<span class="seq-q">?</span>'; }
        else { cell.className = "seq-cell filled"; cell.textContent = n; }
        path.appendChild(cell);
      });
      stim.appendChild(path);
      mountTapOptions({
        slide, host, signalName: "sequence_next_correct", stimulus: stim,
        options: d.options,
        optionRenderer: (o)=>{ const cell = document.createElement("div"); const s = document.createElement("span");
          s.className = "seq-optnum"; s.textContent = o.num; cell.appendChild(s); return cell; },
        isCorrect: (o)=> o.correct === true,
        mastery: slide.phase === "mastery",
        columnsHint: d.options.length,
        nudgeTarget: null
      });
    }
  },

  /* ===== ORDERING / SERIATION (MTKGA02_L02_S02 — "orders three objects by size, length, or weight") =====
     Additive modules sharing the .ord-* skin. Objects render at true magnitude (size scale / bar length);
     weight is assessed by 'pick the heaviest' (weight is not visual) — targeting the bigger=heavier
     misconception with a big-but-light distractor. */

  MEET_ORDER: {
    // TEACH BY DOING: the 3 objects are shown already in order (small→big / short→long / light→heavy);
    // the child taps each left→right to hear its rank name (सबसे छोटा / बीच का / सबसे बड़ा etc.), then an
    // explain line plays and नav unlocks. data:{by, items:[{mag,img/emoji/color}] (ascending), rank_audio:[id…],
    // arrow_lo, arrow_hi, hint_icon?}.
    mount(host, slide){
      const d = slide.data; state.ownsAudio = true; setNavActive(false); setSwMood("teach");
      const stage = document.createElement("div"); stage.className = "ord-stage ord-" + d.by;
      const arrow = document.createElement("div"); arrow.className = "ord-arrow";
      arrow.innerHTML = `<span>${d.arrow_lo||""}</span><span class="ord-arrowline"></span><span>${d.arrow_hi||""}</span>`;
      const row = document.createElement("div"); row.className = "ord-tray";
      const cells = d.items.map((o,i)=>{ const el = document.createElement("div"); el.className = "ord-item";
        el.style.opacity = ".5"; el.innerHTML = renderOrdObj(o, d.by); row.appendChild(el); return el; });
      if(d.hint_icon){ const hi = document.createElement("div"); hi.className = "ord-hint-icon"; hi.textContent = d.hint_icon; stage.appendChild(hi); }
      stage.appendChild(arrow); stage.appendChild(row); host.appendChild(stage);
      let tapped = 0;
      const nudgeNext = ()=>{ cells.forEach((c,i)=> c.classList.toggle("active", i === tapped));
        if(tapped < cells.length) startNudge(slide, cells[tapped]); else stopNudge(); };
      if(d.auto){
        // 16j: Phase-1 AUTONOMOUS mode (3-phase contract) — the demo touches each item L→R by
        // ITSELF, speaks its rank, then explains + unlocks आगे. Child watches. (Mirrors auto-INTRO.)
        stopNudge();
        state.demoRunning = true;   // [24a N8] replay chip must not gen-kill the rank chain
        let ai = 0;
        const aStep = ()=>{
          if(CARD.slides[state.idx] !== slide) return;
          if(ai >= cells.length){ stopNudge();
            GameBus.emit("meet_order_done", { slide_id: slide.id, phase: slide.phase });
            setTimeout(()=> play(audioFor(slide, "explain") || null, ()=>{ state.demoRunning = false; setNavActive(true); }), 300);
            return; }
          const c = cells[ai]; cells.forEach((x,j)=> x.classList.toggle("active", j === ai));
          c.style.opacity = "1"; c.classList.add("reveal-glow"); pointNudgeAt(c);
          setTimeout(()=> c.classList.remove("reveal-glow"), 600);
          const rid = d.rank_audio[ai]; ai++;
          play(rid ? "assets/Audio/" + rid + "." + AUDIO_EXT : null, ()=> setTimeout(aStep, 520));
        };
        setTimeout(aStep, 400);
      } else {
        nudgeNext();
        cells.forEach((c,i)=>{ c.onclick = ()=>{ if(i !== tapped) return; stopNudge();
          c.classList.remove("active"); c.style.opacity = "1"; c.classList.add("reveal-glow");
          setTimeout(()=> c.classList.remove("reveal-glow"), 600);
          play("assets/Audio/" + (d.rank_audio[i]) + "." + AUDIO_EXT, ()=>{}); tapped++;
          if(tapped >= cells.length){ stopNudge();
            GameBus.emit("meet_order_done", { slide_id: slide.id, phase: slide.phase });
            setTimeout(()=> play(audioFor(slide, "explain") || null, ()=> setNavActive(true)), 450);
          } else nudgeNext();
        }; });
      }
      state.replayAudio = ()=> play(audioFor(slide, "explain") || null, ()=>{});
      $("navBtn").onclick = ()=> completeSlide(true);
    }
  },

  /* 16j NEW (g6 ordering tutorial): teach a 2-way attribute (बड़ा/छोटा · लंबा/छोटा · भारी/हल्का)
     BEFORE ordering three. Autonomous — points at each of 2 objects, speaks its label, then concludes
     + unlocks आगे. Reuses ord-stage. data:{by, items:[{img/emoji/color,mag}], label_audio:[id,id]}. */
  COMPARE_TWO: {
    mount(host, slide){
      const d = slide.data; state.ownsAudio = true; state.demoRunning = true; setNavActive(false); setSwMood("teach");   // [24a N8]
      const stage = document.createElement("div"); stage.className = "ord-stage cmp2-stage ord-" + (d.by || "size");
      const row = document.createElement("div"); row.className = "ord-tray";
      const cells = d.items.map((o)=>{ const el = document.createElement("div"); el.className = "ord-item";
        el.style.opacity = ".5"; el.innerHTML = renderOrdObj(o, d.by); row.appendChild(el); return el; });
      stage.appendChild(row); host.appendChild(stage);
      let ai = 0;
      const aStep = ()=>{
        if(CARD.slides[state.idx] !== slide) return;
        if(ai >= cells.length){ stopNudge();
          GameBus.emit("compare_two_done", { slide_id: slide.id, phase: slide.phase });
          setTimeout(()=> play(audioFor(slide, "explain") || audioFor(slide, "conclude") || null, ()=>{ state.demoRunning = false; setNavActive(true); }), 300);
          return; }
        const c = cells[ai]; cells.forEach((x,j)=> x.classList.toggle("active", j === ai));
        c.style.opacity = "1"; c.classList.add("reveal-glow"); pointNudgeAt(c);
        setTimeout(()=> c.classList.remove("reveal-glow"), 600);
        const lid = (d.label_audio || [])[ai]; ai++;
        play(lid ? "assets/Audio/" + lid + "." + AUDIO_EXT : null, ()=> setTimeout(aStep, 520));
      };
      setTimeout(aStep, 400);
      state.replayAudio = ()=> play(audioFor(slide, "explain") || audioFor(slide, "conclude") || null, ()=>{});
      $("navBtn").onclick = ()=> completeSlide(true);
    }
  },

  ORDER_BY_ATTR: {
    // PRODUCE test: 3 scrambled objects + a left→right strip (arrow छोटा→बड़ा). Tap the smallest-remaining
    // → it fills the next slot. Wrong (not the current smallest) = shake + soft buzz + spoken try_again;
    // demonstrate after max_attempts. data:{by, items:[{mag,img/emoji/color}], arrow_lo, arrow_hi}.
    mount(host, slide){
      const d = slide.data;
      const stage = document.createElement("div"); stage.className = "ord-stage ord-" + d.by;
      const arrow = document.createElement("div"); arrow.className = "ord-arrow";
      arrow.innerHTML = `<span>${d.arrow_lo||""}</span><span class="ord-arrowline"></span><span>${d.arrow_hi||""}</span>`;
      const strip = document.createElement("div"); strip.className = "ord-strip";
      const n = d.items.length; const slots = [];
      for(let i=0;i<n;i++){ const sl = document.createElement("div"); sl.className = "ord-slot"; strip.appendChild(sl); slots.push(sl); }
      const tray = document.createElement("div"); tray.className = "ord-tray";
      const disp = d.items.slice(); for(let i=disp.length-1;i>0;i--){ const j=(Math.random()*(i+1))|0; [disp[i],disp[j]]=[disp[j],disp[i]]; }
      const sortedMags = d.items.map(o=>o.mag).slice().sort((a,b)=>a-b);
      const tiles = disp.map(o=>{ const el = document.createElement("div"); el.className = "ord-item"; el._mag = o.mag;
        el.innerHTML = renderOrdObj(o, d.by); tray.appendChild(el); return el; });
      stage.appendChild(arrow); stage.appendChild(strip); stage.appendChild(tray); host.appendChild(stage);
      let placed = 0, wrongStreak = 0, revealed = false; state.locked = false; state.attempts = 0;
      const wantMag = ()=> sortedMags[placed];
      const nextTile = ()=> tiles.find(x=> !x.classList.contains("used") && x._mag === wantMag());
      const markActive = ()=>{ slots.forEach((s,i)=> s.classList.toggle("active", i === placed));
        if(placed < n) startNudge(slide, nextTile()); else stopNudge(); };
      const placeInto = (tile)=>{ const slot = slots[placed]; slot.classList.remove("active"); slot.classList.add("filled");
        slot.innerHTML = tile.innerHTML; tile.classList.add("used"); placed++;
        if(placed >= n){ state.locked = true; stopNudge();
          GameBus.emit("order_by_attr_correct", { slide_id: slide.id, phase: slide.phase, value: !revealed,
            attempts: state.attempts + 1, latency_ms: Date.now()-state.slideStart });
          celebrateThenAdvance(slide, revealed);
        } else markActive();
      };
      markActive();
      tiles.forEach(t=>{ t.onclick = ()=>{ if(state.locked || t.classList.contains("used")) return; stopNudge();
        if(t._mag === wantMag()){ wrongStreak = 0; placeInto(t); }
        else { state.attempts++; t.classList.add("shake"); setTimeout(()=> t.classList.remove("shake"), 420);
          GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
          $("hintBtn").classList.add("show","hint-glow");
          if(++wrongStreak >= (CARD.scaffold_rules.max_attempts || 3)){ revealed = true; wrongStreak = 0;
            const c = nextTile(); if(c){ c.classList.add("reveal-glow"); play(audioFor(slide,"reveal")||null, ()=>{});
              setTimeout(()=>{ c.classList.remove("reveal-glow"); placeInto(c); }, 1000); }
          } else dragWrong(slide);
        }
      }; });
      setNavActive(false); $("navBtn").onclick = ()=>{};
      $("hintBtn").onclick = ()=>{ if(!state.locked){ const t = nextTile(); if(t){ t.classList.add("reveal-glow"); setTimeout(()=> t.classList.remove("reveal-glow"), 800); } } };
    }
  },

  PICK_EXTREME: {
    // PICK test: tap the object that is the MOST (सबसे बड़ा / सबसे लंबा / सबसे भारी). For weight, options
    // include a big-but-light distractor to break the bigger=heavier misconception. Reuses mountTapOptions
    // → tap-to-answer + speak-the-word-on-tap + mastery. data:{by, options:[{img/emoji/color,mag,label,audio,correct}]}.
    mount(host, slide){
      const d = slide.data;
      mountTapOptions({
        slide, host, signalName: "pick_extreme_correct", stimulus: null,
        options: d.options,
        optionRenderer: (o)=>{ const cell = document.createElement("div"); cell.className = "ord-pick";
          cell.innerHTML = renderOrdObj(o, d.by) + (o.label ? `<span class="lbl">${o.label}</span>` : ""); return cell; },
        isCorrect: (o)=> o.correct === true,
        mastery: slide.phase === "mastery",
        columnsHint: d.options.length,
        nudgeTarget: null
      });
    }
  },

  ORDER_BY_WEIGHT: {
    // PRODUCE test — WEIGHT seriation via A-vs-B COMPARISON (weight is not visual). Two pans: tap a tray
    // object → it loads the next empty pan; with BOTH loaded the beam tilts toward the heavier (it DROPS)
    // + thunk, and the lighter one RISES + pulses. Tap the lighter (risen) object to send it to the next
    // हल्का→भारी slot — accepted only if it is the lightest still unplaced; else it is the lighter of a
    // heavy pair (an even lighter one exists) → soft buzz + try_again, both return. The last object
    // auto-places (it is forced). Objects render at sizes that DON'T match weight (a big balloon can be
    // light) so the SCALE is the only cue. data:{items:[{wmag,dmag,img,emoji}], arrow_lo, arrow_hi}.
    mount(host, slide){
      const d = slide.data;
      const stage = document.createElement("div"); stage.className = "ord-stage ord-weight";
      const arrow = document.createElement("div"); arrow.className = "ord-arrow";
      arrow.innerHTML = `<span>${d.arrow_lo||"हल्का"}</span><span class="ord-arrowline"></span><span>${d.arrow_hi||"भारी"}</span>`;
      const scale = document.createElement("div"); scale.className = "owt-scale";
      scale.innerHTML = `<div class="owt-foot"></div><div class="owt-post"></div>` +
        `<div class="owt-beamwrap"><div class="owt-beam"></div><div class="owt-cap"></div>` +
        `<div class="owt-arm l"></div><div class="owt-arm r"></div>` +
        `<div class="owt-pan l"><div class="owt-load"></div></div><div class="owt-pan r"><div class="owt-load"></div></div></div>`;
      const beamwrap = scale.querySelector(".owt-beamwrap");
      const panEl = { l: scale.querySelector(".owt-pan.l"), r: scale.querySelector(".owt-pan.r") };
      const loadEl = { l: panEl.l.querySelector(".owt-load"), r: panEl.r.querySelector(".owt-load") };
      const strip = document.createElement("div"); strip.className = "ord-strip";
      const n = d.items.length; const slots = [];
      for(let i=0;i<n;i++){ const sl = document.createElement("div"); sl.className = "ord-slot"; strip.appendChild(sl); slots.push(sl); }
      const tray = document.createElement("div"); tray.className = "ord-tray";
      const disp = d.items.slice(); for(let i=disp.length-1;i>0;i--){ const j=(Math.random()*(i+1))|0; [disp[i],disp[j]]=[disp[j],disp[i]]; }
      const sortedW = d.items.map(o=>o.wmag).slice().sort((a,b)=>a-b);
      const tiles = disp.map(o=>{ const el = document.createElement("div"); el.className = "ord-item"; el._o = o; el._w = o.wmag; el._onpan = false;
        el.innerHTML = renderOrdObj({ mag: o.dmag, img: o.img, emoji: o.emoji }, "size"); tray.appendChild(el); return el; });
      stage.appendChild(arrow); stage.appendChild(scale); stage.appendChild(strip); stage.appendChild(tray);
      host.appendChild(stage);

      let placed = 0, wrongStreak = 0, revealed = false, busy = false; state.locked = false; state.attempts = 0;
      const pans = { l: null, r: null };
      const wantW = ()=> sortedW[placed];
      const nextTile = ()=> tiles.find(x=> !x.classList.contains("used") && x._w === wantW());
      const remaining = ()=> tiles.filter(x=> !x.classList.contains("used"));
      const markActive = ()=>{ slots.forEach((s,i)=> s.classList.toggle("active", i === placed));
        if(placed < n && !pans.l && !pans.r){ const t = nextTile(); if(t && !t._onpan) startNudge(slide, t); } else stopNudge(); };
      const resetPans = ()=>{ ["l","r"].forEach(k=>{ const t = pans[k]; if(t){ t._onpan = false; t.style.visibility = ""; }
        loadEl[k].innerHTML = ""; loadEl[k].classList.remove("lighter"); pans[k] = null; }); beamwrap.style.transform = "rotate(0deg)"; };
      const loadPan = (k, t)=>{ pans[k] = t; t._onpan = true; t.style.visibility = "hidden"; loadEl[k].innerHTML = imgOrEmojiSized(t._o.img, t._o.emoji, 56); };
      const compare = ()=>{ beamwrap.style.transform = `rotate(${(pans.r._w - pans.l._w) * 7}deg)`;   // heavier side drops
        btThunk(Math.max(pans.l._w, pans.r._w)); const lightK = pans.l._w < pans.r._w ? "l" : "r";
        loadEl[lightK].classList.add("lighter"); loadEl[lightK === "l" ? "r" : "l"].classList.remove("lighter"); };
      const placeToSlot = (t, cb)=>{ const slot = slots[placed]; slot.classList.remove("active"); slot.classList.add("filled");
        slot.innerHTML = renderOrdObj({ mag: t._o.dmag, img: t._o.img, emoji: t._o.emoji }, "size"); t.classList.add("used"); t._onpan = false; placed++;
        if(placed >= n){ state.locked = true; stopNudge();
          GameBus.emit("order_by_weight_correct", { slide_id: slide.id, phase: slide.phase, value: !revealed,
            attempts: state.attempts + 1, latency_ms: Date.now()-state.slideStart });
          celebrateThenAdvance(slide, revealed);
        } else markActive();
        if(cb) cb();
      };
      // when only one object remains it is forced — weigh it alone briefly, then place it.
      const autoLast = ()=>{ if(state.locked) return; const rem = remaining(); if(rem.length !== 1){ markActive(); return; }
        busy = true; const t = rem[0]; loadPan("l", t); beamwrap.style.transform = "rotate(-9deg)"; btThunk(t._w);
        setTimeout(()=>{ loadEl.l.innerHTML = ""; beamwrap.style.transform = "rotate(0deg)"; placeToSlot(t, ()=>{ busy = false; }); }, 850); };
      // tray tap → load the next empty pan (compare once both are full)
      tiles.forEach(t=>{ t.onclick = ()=>{ if(state.locked || busy || t.classList.contains("used") || t._onpan) return; stopNudge();
        if(!pans.l){ loadPan("l", t); }
        else if(!pans.r){ loadPan("r", t); compare(); }
      }; });
      // pan tap → try to place that pan's object (must be the LIGHTER of the two AND the lightest unplaced)
      ["l","r"].forEach(k=>{ panEl[k].onclick = ()=>{ if(state.locked || busy || !pans.l || !pans.r) return;
        const t = pans[k], other = pans[k === "l" ? "r" : "l"];
        if(t._w > other._w){ const lk = pans.l._w < pans.r._w ? "l" : "r";   // tapped the heavier one → re-pulse the lighter (hint), no penalty
          loadEl[lk].classList.remove("lighter"); void loadEl[lk].offsetWidth; loadEl[lk].classList.add("lighter"); return; }
        if(t._w === wantW()){ busy = true; wrongStreak = 0;   // correct: lighter AND globally lightest
          other._onpan = false; other.style.visibility = "";
          loadEl.l.innerHTML = ""; loadEl.r.innerHTML = ""; loadEl.l.classList.remove("lighter"); loadEl.r.classList.remove("lighter");
          pans.l = null; pans.r = null; beamwrap.style.transform = "rotate(0deg)";
          placeToSlot(t, ()=> setTimeout(()=>{ busy = false; autoLast(); }, 250));
        } else {   // lighter of the pair, but an even lighter one is still unplaced
          state.attempts++; GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts }); $("hintBtn").classList.add("show","hint-glow");
          if(++wrongStreak >= (CARD.scaffold_rules.max_attempts || 3)){ revealed = true; wrongStreak = 0; resetPans();
            const c = nextTile(); if(c){ c.classList.add("reveal-glow"); play(audioFor(slide, "reveal") || null, ()=>{});
              setTimeout(()=>{ c.classList.remove("reveal-glow"); busy = true; placeToSlot(c, ()=> setTimeout(()=>{ busy = false; autoLast(); }, 250)); }, 900); } }
          else { dragWrong(slide); resetPans(); }
        }
      }; });
      markActive();
      setNavActive(false); $("navBtn").onclick = ()=>{};
      $("hintBtn").onclick = ()=>{ if(!state.locked && !busy){ const t = nextTile(); if(t && !t._onpan){ t.classList.add("reveal-glow"); setTimeout(()=> t.classList.remove("reveal-glow"), 800); } } };
    }
  },

  BUILD_TO_NUMBER: {
    // Signature produce module. data: {target, mode:'guided'|'independent', topper, friend, goal_hi,
    // skyline_done, skyline_total}. Guided = dashed blueprint, auto-completes on fill. Independent =
    // free stack + "बन गया!" serve with world-enacted feedback (short/teeter, never a ✗). Ascending-
    // pitch thunk + spoken एक/दो/… per block. Geometry via offsets (throttle-safe).
    mount(host, slide){
      const d = slide.data, N = d.target, mode = d.mode || "independent";
      const stage = document.createElement("div"); stage.className = "bt-stage";
      const board = document.createElement("div"); board.className = "bt-board";
      board.innerHTML = `<span class="bt-numeral">${N}</span>` +
        (d.topper ? `<img class="bt-goalpic" src="assets/Images/${d.topper}.png" alt="">` : "") +
        (d.goal_hi ? `<span class="bt-goallbl">${d.goal_hi}</span>` : "");
      const track = document.createElement("div"); track.className = "bt-track"; const cells = [];
      for(let i=1;i<=N;i++){ const c = document.createElement("div"); c.className = "bt-nt"; track.appendChild(c); cells.push(c); }
      const yard = document.createElement("div"); yard.className = "bt-yard";
      const crane = document.createElement("div"); crane.className = "bt-crane"; crane.innerHTML = `<img src="assets/Images/obj_crane.png" alt="">`;
      const pile = document.createElement("div"); pile.className = "bt-pile";
      pile.innerHTML = `<div class="bt-pile-blocks"></div><span class="bt-pile-lbl">＋ ब्लॉक</span>`;
      const pb = pile.querySelector(".bt-pile-blocks");
      for(let i=0;i<3;i++){ const b = btBlock(i+1); b.style.left = (i*12) + "px"; b.style.bottom = (i*18) + "px"; pb.appendChild(b); }
      const plotwrap = document.createElement("div"); plotwrap.className = "bt-plotwrap";
      const plot = document.createElement("div"); plot.className = "bt-plot ground " + mode;
      plot.style.setProperty("--bh", Math.max(20, Math.min(46, Math.floor(230/N) - 2)) + "px");   // tall towers auto-shrink to fit
      plotwrap.appendChild(plot);
      const friend = document.createElement("div"); friend.className = "bt-friend";
      if(d.friend) friend.innerHTML = `<img src="assets/Images/${d.friend}.png" alt="">`;
      yard.appendChild(crane); yard.appendChild(pile); yard.appendChild(plotwrap); if(d.friend) yard.appendChild(friend);
      stage.appendChild(board); stage.appendChild(track); stage.appendChild(yard);
      if(d.skyline_total) stage.appendChild(btSkyline(d.skyline_done || 0, d.skyline_total));
      let serveBtn = null;
      if(mode === "independent"){ serveBtn = document.createElement("button"); serveBtn.type = "button"; serveBtn.className = "bt-serve"; serveBtn.textContent = "बन गया!"; stage.appendChild(serveBtn); }
      host.appendChild(stage);

      let count = 0; state.locked = false; state.attempts = 0;
      const lit = ()=> cells.forEach((c,i)=>{ const on = i < count; c.classList.toggle("lit", on); c.textContent = on ? (i+1) : ""; });
      const addSound = ()=>{ btThunk(count); btDust(plot); play("assets/Audio/vo_num_" + count + "." + AUDIO_EXT); };

      function success(){
        state.locked = true; if(serveBtn) serveBtn.disabled = true;
        if(d.topper){ const t = document.createElement("div"); t.className = "bt-topper snap"; t.innerHTML = `<img src="assets/Images/${d.topper}.png" alt="">`; plot.appendChild(t);
          if(d.topper === "top_rocket") setTimeout(()=> t.classList.add("rocket-go"), 750); }
        if(d.friend) friend.classList.add("hop");
        sfxCorrect(); burstStars();
        const lots = [...stage.querySelectorAll(".bt-bldg")]; const nextLot = lots[d.skyline_done || 0];
        if(nextLot) setTimeout(()=> nextLot.classList.add("done"), 380);
        GameBus.emit("build_to_number_correct", { slide_id: slide.id, phase: slide.phase, value: true, target: N, attempts: state.attempts + 1, latency_ms: Date.now()-state.slideStart });
        play("assets/Audio/vo_total_" + N + "." + AUDIO_EXT); setNavActive(true);
      }

      if(mode === "guided"){
        const ghosts = [];
        for(let i=0;i<N;i++){ const g = document.createElement("div"); g.className = "bp-slot"; plot.appendChild(g); ghosts.push(g); }
        ghosts[0].classList.add("next");
        pile.onclick = ()=>{ if(state.locked) return;
          const g = ghosts.find(x=> x.classList.contains("bp-slot"));
          if(!g){ showBox("", "बस इतने ही चाहिए!", "hint", null, ()=>{}); return; }
          g.className = "blk drop"; g.style.background = BT_COLORS[count % 5];
          count++; lit(); addSound();
          const nx = ghosts.find(x=> x.classList.contains("bp-slot")); if(nx) nx.classList.add("next");
          if(count === N) setTimeout(success, 280);
        };
      } else {
        pile.onclick = ()=>{ if(state.locked) return;
          const b = btBlock(count); b.classList.add("drop");
          b.onclick = (e)=>{ e.stopPropagation(); if(state.locked) return; b.remove(); count--; lit(); };
          plot.appendChild(b); count++; lit(); addSound(); };
        serveBtn.onclick = ()=>{ if(state.locked) return;
          if(count === N){ success(); return; }
          state.attempts++;
          GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts, made: count, target: N });
          if(count < N){ if(d.friend) friend.classList.add("peer");
            showBox("", "थोड़े और चाहिए!", "hint", wrongClip(slide),   /* [28i] was SILENT */ ()=>{ if(d.friend) friend.classList.remove("peer"); }); }
          else { const bs = [...plot.querySelectorAll(".blk")]; const top = bs[bs.length-1];
            if(top){ top.classList.add("wobble"); setTimeout(()=> top.classList.remove("wobble"), 520); }
            showBox("", "अरे! एक ब्लॉक हटाओ।", "hint", wrongClip(slide), ()=>{}); } };   /* [28i] was SILENT */
      }
      setNavActive(false);
      $("navBtn").onclick = ()=>{ if(state.locked) completeSlide(true); };
      pointNudgeAt(pile);
    }
  },

  MAKE_NUMBER: {
    // produce-the-numeral dial (grafted from Firefly Valley). A set of N built blocks; ＋/− dials a
    // 1–10 numeral; wrong is inert (build dim), exact match ignites the build + snaps its topper.
    mount(host, slide){
      const d = slide.data, N = d.count;
      const stage = document.createElement("div"); stage.className = "bt-stage";
      if(d.prompt2_hi){ const lbl = document.createElement("div"); lbl.className = "pat-unit-lbl"; lbl.textContent = d.prompt2_hi; stage.appendChild(lbl); }
      const yard = document.createElement("div"); yard.className = "bt-yard";
      const plotwrap = document.createElement("div"); plotwrap.className = "bt-plotwrap";
      const plot = document.createElement("div"); plot.className = "bt-plot ground"; plot.style.filter = "grayscale(.35) brightness(.95)";
      plot.style.setProperty("--bh", Math.max(20, Math.min(46, Math.floor(230/N) - 2)) + "px");
      for(let i=0;i<N;i++){ plot.appendChild(btBlock(i)); }
      plotwrap.appendChild(plot); yard.appendChild(plotwrap);
      const dial = document.createElement("div"); dial.className = "bt-dial";
      dial.innerHTML = `<button class="bt-dial-btn" data-d="-1" type="button">−</button><div class="bt-dial-val">1</div><button class="bt-dial-btn" data-d="1" type="button">＋</button>`;
      stage.appendChild(yard); stage.appendChild(dial); host.appendChild(stage);
      let val = 1; state.locked = false; const valEl = dial.querySelector(".bt-dial-val");
      const check = ()=>{ if(val === N && !state.locked){ state.locked = true; valEl.classList.add("match"); plot.style.filter = "";
        if(d.topper){ const t = document.createElement("div"); t.className = "bt-topper snap"; t.innerHTML = `<img src="assets/Images/${d.topper}.png" alt="">`; plot.appendChild(t); }
        sfxCorrect(); burstStars(); play("assets/Audio/vo_total_" + N + "." + AUDIO_EXT);
        GameBus.emit("make_number_correct", { slide_id: slide.id, phase: slide.phase, value: true, count: N, latency_ms: Date.now()-state.slideStart });
        setNavActive(true); } };
      dial.querySelectorAll(".bt-dial-btn").forEach(btn=> btn.onclick = ()=>{ if(state.locked) return;
        val = Math.max(1, Math.min(10, val + parseInt(btn.dataset.d, 10))); valEl.textContent = val; sfxTap(); check(); });
      setNavActive(false); $("navBtn").onclick = ()=>{ if(state.locked) completeSlide(true); };
    }
  },

  TAP_LETTER_BY_NAME: {
    mount(host, slide){
      mountTapOptions({
        slide, host, signalName: "letter_name_first_try",
        stimulus: null,
        options: slide.data.options,
        isCorrect: (opt) => opt.letter === slide.data.target,
        optionRenderer: (opt) => letterCell(opt.letter)
      });
    }
  },

  TAP_LETTER_BY_SOUND: {
    mount(host, slide){
      mountTapOptions({
        slide, host, signalName: "letter_sound_first_try",
          /* [28m] NO VOLUME BUTTON, ANYWHERE. Yasir 2026-07-28: "we use vol button nowhere. if
             nothing then we keep question only." This stimulus had NO image, so 28c left its 🔊 +
             "सुनो" chip alone and flagged it — stripping it looked like it would leave a blank card.
             The ruling settles it: nothing to show => show the QUESTION only, no chip. The chip was
             also the only way to re-hear the sound, so that function moves to the header replay
             (state.replayAudio, set after mount) instead of dying with the affordance. */
          stimulus: null,
        options: slide.data.options,
        isCorrect: (opt) => opt.letter === slide.data.target,
        optionRenderer: (opt) => letterCell(opt.letter)
      });
        /* [28m] the removed chip was the only way to re-hear the sound — keep the FUNCTION on the
           header replay. Set AFTER mount so mountTapOptions cannot overwrite it. */
        state.replayAudio = ()=>{ state.audioReplays++; play(audioFor(slide,"phoneme") || null, ()=>{}); };
    }
  },

  TAP_PICTURE_BY_LETTER: {
    mount(host, slide){
      mountTapOptions({
        slide, host, signalName: "letter_image_match_first_try",
        stimulus: stimulusLetter(slide.data.target_letter),
        options: slide.data.options,
        isCorrect: (opt) => opt.correct === true,
        optionRenderer: (opt) => pictureCell(opt.picture, opt.emoji, opt.img)
      });
    }
  },

  TAP_LETTER_BY_PICTURE: {
    mount(host, slide){
      mountTapOptions({
        slide, host, signalName: "image_letter_match_first_try",
        stimulus: stimulusPic(slide.data.picture, slide.data.emoji, slide.data.img),
        options: slide.data.options,
        isCorrect: (opt) => opt.letter === slide.data.target,
        optionRenderer: (opt) => letterCell(opt.letter)
      });
    }
  },

  ODD_ONE_OUT: {
    mount(host, slide){
      const sig = (slide.signals && slide.signals.on_complete && slide.signals.on_complete[0]) || "letter_recognise_first_try";
      const useShape = slide.data.options.some(o => o.shape);
      const usePic = slide.data.options.some(o => o.picture || o.word_hi || o.img);
      mountTapOptions({
        slide, host, signalName: sig,
        stimulus: null,
        options: slide.data.options,
        columnsHint: 4,
        isCorrect: (opt) => opt.is_odd === true,
        optionRenderer: (opt) => useShape
          ? shapeCell(opt)
          : usePic
            ? pictureCell(opt.word_hi || opt.picture, opt.emoji, opt.img)
            : letterCell(opt.letter),
        mastery: slide.phase === "mastery"
      });
    }
  },

  TAP_GENDER: {
    mount(host, slide){
      mountTapOptions({
        slide, host, signalName: "gender_match_first_try",
        stimulus: stimulusPic(slide.data.noun.word_hi, slide.data.noun.emoji, slide.data.noun.img),
        options: slide.data.options,
        columnsHint: 2,
        isCorrect: (opt) => opt.gender === slide.data.target_gender,
        optionRenderer: (opt) => genderLabelCell(opt.label, opt.gender),
        mastery: slide.phase === "mastery"
      });
    }
  },

  TAP_PICTURE_BY_GENDER: {
    mount(host, slide){
      mountTapOptions({
        slide, host, signalName: "gender_match_first_try",
        stimulus: stimulusGender(slide.data.label, slide.data.target_gender),
        options: slide.data.options,
        // tap-to-answer needs ONE unambiguous key — author marks the single intended picture
        // with correct:true (matches every other TAP_* module). The old `|| gender===target`
        // fallback silently accepted any same-gender distractor, defeating buzz+✗+lock.
        isCorrect: (opt) => opt.correct === true,
        optionRenderer: (opt) => pictureCell(opt.word_hi, opt.emoji, opt.img),
        mastery: slide.phase === "mastery"
      });
    }
  },

  GENDER_INTRO: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "gender-cats";
      const cats = slide.data.categories;
      const tapped = new Set();
      let _autoDone = false;   // [24a A3] auto walk-through: taps ignored until every category is taught
      const cardEls = [];
      cats.forEach(cat => {
        const card = document.createElement("div");
        card.className = "gender-cat " + (cat.gender === "F" ? "fem" : "masc");
        card.innerHTML =
          `<div class="cat-title">${cat.label}</div>` +
          imgOrEmoji(cat.anchor.img, cat.anchor.emoji, "cat-pic", "cat-emoji") +
          `<div class="cat-word">${cat.anchor.word_hi}</div>`;
        card.onclick = ()=>{
          // [24a A3] during the auto walk-through the cards are NOT tappable — a tap would gen-kill
          // the demo's own chain (echo guard) and stall it. After teaching completes, tap = replay.
          if(slide.data.auto && !_autoDone) return;
          card.classList.add("played");
          playChain(["assets/Audio/" + cat.label_audio + "." + AUDIO_EXT, "assets/Audio/" + cat.name_audio + "." + AUDIO_EXT], 0);
          tapped.add(cat.gender);
          GameBus.emit("gender_intro_tap", { slide_id: slide.id, gender: cat.gender });
          if(tapped.size >= cats.length){ stopNudge(); setNavActive(true); }
        };
        wrap.appendChild(card); cardEls.push(card);
      });
      host.appendChild(wrap);
      // 16m: AUTONOMOUS demo (data.auto) — point at each category, auto-play its label + anchor word,
      // then unlock आगे. Replaces passive touch-to-hear (3-phase contract).
      if(slide.data.auto){
        state.ownsAudio = true; state.demoRunning = true; setNavActive(false); setSwMood("teach");
        let ci = 0, _done = false;
        const finish = ()=>{ if(_done) return; _done = true; stopNudge();
          _autoDone = true; state.demoRunning = false;   // [24a A3/N8] teaching over → taps replay, chip re-enabled
          state.replayAudio = ()=> playChain(cats.reduce((a,c)=> a.concat(["assets/Audio/" + c.label_audio + "." + AUDIO_EXT, "assets/Audio/" + c.name_audio + "." + AUDIO_EXT]), []), 0, ()=>{});
          $("navBtn").onclick = ()=> completeSlide(true); setNavActive(true); };
        const step = ()=>{
          if(CARD.slides[state.idx] !== slide) return;
          if(ci >= cats.length){ finish(); return; }
          const cat = cats[ci], el = cardEls[ci]; el.classList.add("played"); pointNudgeAt(el); ci++;
          playChain(["assets/Audio/" + cat.label_audio + "." + AUDIO_EXT, "assets/Audio/" + cat.name_audio + "." + AUDIO_EXT], 0, ()=> setTimeout(step, 500));
        };
        $("navBtn").onclick = ()=> completeSlide(true);
        setTimeout(step, 400);
        setTimeout(()=>{ if(CARD.slides[state.idx] === slide) finish(); }, cats.length * 4500 + 3000);   // FAIL-SAFE: never dead-button
        return;
      }
      state.gateNavUntilAudio = true;   // nav unlocks after the concept VO
      setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
    }
  },

  MEET_GENDER: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "meet-gender";
      const n = slide.data.noun;
      wrap.innerHTML =
        `<div class="meet-pic-box">${imgOrEmoji(n.img, n.emoji, "pic-img", "pic-emoji")}<span class="pic-label">${n.word_hi}</span></div>` +
        `<div class="meet-arrow">→</div>` +
        `<div class="gender-badge${slide.data.gender === "F" ? " fem" : ""}">${slide.data.label}</div>`;
      host.appendChild(wrap);
      // 16m: AUTONOMOUS demo (data.auto) — point at the word + speak the model line, then point at the
      // ए/ऐ matra badge + speak it, then unlock आगे. Kills passive show-and-tell (3-phase contract).
      if(slide.data.auto){
        state.ownsAudio = true; state.demoRunning = true; setNavActive(false); setSwMood("teach");   // [24a N8]
        const steps = [];
        const picEl = wrap.querySelector(".meet-pic-box"), badgeEl = wrap.querySelector(".gender-badge");
        if(picEl) steps.push([picEl, audioFor(slide, "prompt")]);
        if(badgeEl) steps.push([badgeEl, slide.data.label_audio ? "assets/Audio/" + slide.data.label_audio + "." + AUDIO_EXT : null]);
        let si = 0, _done = false;
        const finish = ()=>{ if(_done) return; _done = true; stopNudge(); state.demoRunning = false; $("navBtn").onclick = ()=> completeSlide(true); setNavActive(true); };
        const step = ()=>{
          if(CARD.slides[state.idx] !== slide) return;
          if(si >= steps.length){ finish(); return; }
          const p = steps[si]; si++; pointNudgeAt(p[0]); play(p[1] || null, ()=> setTimeout(step, 450));
        };
        $("navBtn").onclick = ()=> completeSlide(true);
        state.replayAudio = ()=> play(audioFor(slide, "prompt") || null, ()=>{});
        setTimeout(step, 400);
        setTimeout(()=>{ if(CARD.slides[state.idx] === slide) finish(); }, steps.length * 4000 + 3000);   // FAIL-SAFE: never dead-button
        return;
      }
      state.gateNavUntilAudio = true;   // nav unlocks after the model VO
      setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
    }
  },

  SORT_GENDER: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "sort-stage";
      const binsRow = document.createElement("div"); binsRow.className = "sort-bins";
      slide.data.bins.forEach(b => {
        const bin = document.createElement("div");
        bin.className = "sort-bin dd-zone" + (b.gender === "F" ? " fem" : "");   // dd-zone → drop detection
        bin.dataset.gender = b.gender;
        bin.innerHTML = `<div class="bin-title">${b.label}</div><div class="bin-items"></div>`;
        binsRow.appendChild(bin);
      });
      const tray = document.createElement("div"); tray.className = "sort-tray";
      const items = slide.data.items.slice().sort(()=> Math.random() - 0.5);
      items.forEach(it => {
        const t = document.createElement("div"); t.className = "sort-item";
        t.dataset.gender = it.gender; if(it.audio) t.dataset.audio = it.audio;   // [20a SORT-01]
        t.innerHTML = imgOrEmoji(it.img, it.emoji, "img", "emoji") + `<span class="lbl">${it.word_hi}</span>`;
        tray.appendChild(t);
      });
      wrap.appendChild(binsRow); wrap.appendChild(tray);
      host.appendChild(wrap);

      state.attempts = 0; state.locked = false;
      let placed = 0; const need = slide.data.items.length;
      /* [28p] SORT_GENDER WAS THE SIXTH TERMINAL-HELP PATH WITH NO TERMINAL HELP AT ALL.
         Measured: its wrong branch buzzed and spoke try_again and did nothing else — no attempt
         ceiling, no glow, no dimming, no hand — so a child could be wrong indefinitely with no
         escalation, and a GUIDED sort could never earn the hand that Yasir's 2026-07-28 ruling
         grants after 2 failed attempts. Counted PER TILE, like MATCH_DRAG_N (25d): a slide-wide
         streak that any correct drop resets lets one hard item ride on the others' successes. */
      const _sgWrong = new Map();
      if(slide.data.reveal_seq) sortSeqReveal(tray, slide);   // [20a SORT-01] opt-in
      [...tray.children].forEach(tile => {
        makeDraggable(tile, (zone, t) => {
          const bin = zone.closest(".sort-bin"); if(!bin) return;
          state.attempts++;
          if(bin.dataset.gender === t.dataset.gender){
            leaveTrayGhost(t);   // [24a A5] capture the tray-slot size before .snapped shrinks/moves it
            t.classList.add("snapped");
            bin.querySelector(".bin-items").appendChild(t);
            placed++; _sgWrong.delete(t);          /* [28p] this tile is done */
            if(t.dataset.audio && placed < need) play("assets/Audio/" + t.dataset.audio + "." + AUDIO_EXT, ()=>{});   // [20a SORT-01] speak-on-match
            GameBus.emit("gender_sort_item", { slide_id: slide.id, gender: t.dataset.gender, attempts: state.attempts });
            if(placed === need){
              state.locked = true;
              GameBus.emit("gender_sort_correct", {
                slide_id: slide.id, phase: slide.phase, value: true,
                attempts: state.attempts, latency_ms: Date.now() - state.slideStart
              });
              setTimeout(()=> celebrateThenAdvance(slide, false), 250);   // standard: confetti + VO + auto-advance, no popup
            }
          } else {
            bin.classList.add("hover"); bin.style.borderColor = "var(--wrong)";
            setTimeout(()=>{ bin.classList.remove("hover"); bin.style.borderColor = ""; }, 500);
            dragWrong(slide);   // buzz + Swiftie + spoken try_again (pre-readers need the spoken recovery)
            GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
            /* [28p] terminal rung, via the SAME contract every other mechanic uses (28l/28o): glow the
               correct bin, dim the other bins, travel the hand from the tile to that bin, and WAIT — the
               child still makes the drop. maySolveFor() is not consulted because nothing is auto-solved
               here; terminalHold/travelNudge carry the phase rule themselves. */
            const _n = (_sgWrong.get(t) || 0) + 1; _sgWrong.set(t, _n);
            if(_n >= ((CARD.scaffold_rules && CARD.scaffold_rules.max_attempts) || 3)){
              const _goal = [...binsRow.children].find(b => b.dataset.gender === t.dataset.gender);
              if(_goal){
                _goal.classList.add("reveal-hold");
                [...binsRow.children].forEach(b => { if(b !== _goal) b.classList.add("tile-disabled"); });
                terminalHold(t, tray.children, slide, _goal);
                state.helpShown = true; state.scaffoldLevel = 3;
                GameBus.emit("answer_revealed", { slide_id: slide.id, phase: slide.phase,
                                                   attempts: state.attempts, reason: "wrong" });
              }
            }
          }
        });
      });
    }
  },

  MATCH_GENDER_PAIRS: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "dd-stage";
      const zoneRow = document.createElement("div"); zoneRow.className = "dd-row";
      const zones = slide.data.pairs.slice().sort(()=> Math.random() - 0.5);
      zones.forEach(p => {
        const z = document.createElement("div"); z.className = "dd-zone"; z.dataset.accept = p.id;
        z.innerHTML = imgOrEmoji(p.f.img, p.f.emoji, "zone-img", "zone-emoji") + `<span class="zone-lbl">${p.f.word_hi}</span>`;
        zoneRow.appendChild(z);
      });
      const tileRow = document.createElement("div"); tileRow.className = "dd-row"; tileRow.style.marginTop = "34px";
      const tiles = slide.data.pairs.slice().sort(()=> Math.random() - 0.5);
      tiles.forEach(p => {
        const t = document.createElement("div"); t.className = "dd-tile pic-tile"; t.dataset.pairId = p.id;
        t.innerHTML = imgOrEmoji(p.m.img, p.m.emoji, "zone-img", "zone-emoji") + `<span class="zone-lbl">${p.m.word_hi}</span>`;
        tileRow.appendChild(t);
      });
      wrap.appendChild(zoneRow); wrap.appendChild(tileRow);
      host.appendChild(wrap);

      state.attempts = 0; state.locked = false;
      let filled = 0, wrongStreak = 0, revealed = false; const need = slide.data.pairs.length;
      const settle = (zone, t)=>{                       // the one correct-placement path (drop AND reveal)
        zone.classList.add("filled","correct");
        // grey the matched masculine tile in place (pictures don't badge well)
        t.classList.add("matched"); t.style.transform = "";
        filled++;
        if(filled === need){ state.locked = true; setTimeout(()=> celebrateThenAdvance(slide, revealed), 250); }
      };
      // A8 reveal ceiling: after max consecutive misses, DEMONSTRATE one pair (pulse + auto-settle) so
      // the child is guided forward instead of dead-ending; run counts success=false via `revealed`.
      const revealOne = ()=>{
        const zone = [...zoneRow.children].find(z=> !z.classList.contains("filled")); if(!zone) return;
        const t = [...tileRow.children].find(x=> !x.classList.contains("matched") && x.dataset.pairId === zone.dataset.accept); if(!t) return;
        revealed = true; wrongStreak = 0;
        zone.classList.add("reveal-glow"); t.classList.add("reveal-glow");
        play(audioFor(slide,"reveal") || null, ()=>{});
        zone.classList.add("reveal-hold");                 /* [25d] glow and WAIT — never settle() it for the child */
        terminalHold(t, tileRow.children, slide, zone);   /* [28l] dim distractors + [28o] hand travels to the zone */
      };
      [...tileRow.children].forEach(tile => {
        makeDraggable(tile, (zone, t) => {
          if(state.locked || zone.classList.contains("filled")) return;
          state.attempts++;
          if(zone.dataset.accept === t.dataset.pairId){
            wrongStreak = 0;
            GameBus.emit("gender_pair_match", {
              slide_id: slide.id, phase: slide.phase, value: true,
              pair: t.dataset.pairId, attempts: state.attempts
            });
            settle(zone, t);
          } else {
            zone.classList.add("filled","wrong");
            setTimeout(()=> zone.classList.remove("filled","wrong"), 600);
            dragWrong(slide);
            GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
            if(++wrongStreak >= (CARD.scaffold_rules.max_attempts||3)) revealOne();
          }
        });
      });
    }
  },

  MATCH_DRAG_1: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "dd-stage";
      // zone (target picture)
      const zoneRow = document.createElement("div"); zoneRow.className = "dd-row";
      const zone = document.createElement("div"); zone.className = "dd-zone";
      zone.innerHTML = imgOrEmoji(slide.data.target.img, slide.data.target.emoji, "zone-img", "zone-emoji") + `<span class="zone-lbl">${slide.data.target.picture||""}</span>`;
      zone.dataset.accept = slide.data.letter.letter;
      zoneRow.appendChild(zone);
      // tile
      const tileRow = document.createElement("div"); tileRow.className = "dd-row"; tileRow.style.marginTop = "30px";
      const tile = document.createElement("div"); tile.className = "dd-tile"; tile.innerHTML = `<span class="ink-glyph">${slide.data.letter.letter}</span>`;
      tileRow.appendChild(tile);
      wrap.appendChild(zoneRow); wrap.appendChild(tileRow);
      host.appendChild(wrap);

      state.attempts = 0; state.locked = false;
      makeDraggable(tile, (zone, t) => {
        state.attempts++;
        const ok = (zone.dataset.accept === t.textContent.trim());
        if(ok){
          zone.classList.add("filled","correct");
          // snap tile into zone (badge is small — drop the ink-centering transform)
          t.classList.add("snapped");
          t.querySelector(".ink-glyph")?.style.removeProperty("transform");
          zone.appendChild(t);
          state.locked = true;
          GameBus.emit("letter_image_match_first_try", {
            slide_id: slide.id, phase: slide.phase, value: true,
            first_try: state.attempts === 1, attempts: state.attempts,
            latency_ms: Date.now()-state.slideStart
          });
          celebrateThenAdvance(slide, false);
        } else {
          zone.classList.add("filled","wrong");
          setTimeout(()=> zone.classList.remove("filled","wrong"), 600);
          dragWrong(slide);
          GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
          if(state.attempts >= (CARD.scaffold_rules.max_attempts||3)){
            state.locked = true;
            // reveal = DEMONSTRATE, don't just tell: snap the letter into its picture (dimmed pulse)
            // with the spoken reveal line, then move on as success=false.
            showBox("", audioText(slide,"reveal") || "कोई बात नहीं! इसे यहाँ रखो।", "reveal", audioFor(slide,"reveal"), ()=>{});
            setTimeout(()=>{
              zone.classList.add("filled","correct","reveal-glow");
              t.classList.add("snapped");
              t.querySelector(".ink-glyph")?.style.removeProperty("transform");
              zone.appendChild(t);
              setTimeout(()=> completeSlide(false), 1300);
            }, 900);
          }
        }
      });
    }
  },

  MATCH_DRAG_N: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "dd-stage";
      const zoneRow = document.createElement("div"); zoneRow.className = "dd-row";
      // shuffle zones so order ≠ tile order
      const zones = slide.data.pairs.slice().sort(()=> Math.random()-0.5);
      zones.forEach(p => {
        const z = document.createElement("div"); z.className = "dd-zone";
        z.innerHTML = imgOrEmoji(p.img, p.emoji, "zone-img", "zone-emoji") + `<span class="zone-lbl">${p.picture||""}</span>`;
        z.dataset.accept = p.letter;
        /* [27j] SPEAK-ON-TAP for the picture/word DROP-ZONE. Only the letter TILE had a listener, so
           a child could hear the letter but never the word — they had to guess which letter to drag.
           The SME deck asks for it on all 4 match slides: "शब्द पर छूने पर शब्द का नाम बोलना चाहिए".
           Reuses the pair's existing match_audio (the word clip already played on a correct drop), so
           no new VO is needed; p.zone_audio overrides if a card wants a different line. Gated on
           isPlaying so a tap cannot stomp the prompt, and dead once the zone is filled. Additive —
           a pair with neither id behaves exactly as before. */
        const zoneSrc = p.zone_audio || p.match_audio || p.word_audio;
        if(zoneSrc) z.addEventListener("pointerdown", ()=>{
          if(z.classList.contains("filled") || isPlaying) return;
          play("assets/Audio/" + zoneSrc + "." + AUDIO_EXT, ()=>{});
        });
        zoneRow.appendChild(z);
      });
      const tileRow = document.createElement("div"); tileRow.className = "dd-row"; tileRow.style.marginTop = "30px";
      const tiles = slide.data.pairs.slice().sort(()=> Math.random()-0.5);
      tiles.forEach(p => {
        const t = document.createElement("div"); t.className = "dd-tile"; t.innerHTML = `<span class="ink-glyph">${p.letter}</span>`;
        // [21c flag#4] TAP → LETTER sound, correct DROP → WORD (SME split). tap_audio = vo_ltr_<letter>,
        // match_audio = vo_word_<word>. Additive + gated: fall back to legacy letter_audio so sibling
        // MATCH games (no tap_audio/match_audio fields) stay byte-for-byte identical. Fire-and-forget on tap.
        const tapSrc = p.tap_audio || p.letter_audio;
        if(tapSrc) t.addEventListener("pointerdown", ()=>{ if(t.classList.contains("snapped")) return; play("assets/Audio/" + tapSrc + "." + AUDIO_EXT, ()=>{}); });   // [24a bug-hunt F5] a placed tile must not replay-and-cut the current VO (the A1 gate exempts snapped tiles)
        if(p.match_audio) t.dataset.matchAudio = p.match_audio;
        tileRow.appendChild(t);
      });
      wrap.appendChild(zoneRow); wrap.appendChild(tileRow);
      host.appendChild(wrap);

      state.attempts = 0; state.locked = false;
      let filled = 0, wrongStreak = 0, revealed = false; const need = slide.data.pairs.length;
      const settle = (zone, t)=>{                       // one correct-placement path (drop AND reveal)
        zone.classList.add("filled","correct");
        t.classList.add("snapped","md-word");           // md-word: caption-chip look for WORD tiles (not the letter badge)
        const ig = t.querySelector(".ink-glyph");
        if(ig){ ig.style.removeProperty("transform"); ig.style.removeProperty("font-size"); delete ig.dataset.inkBase; }
        zone.appendChild(t);
        if(ig) requestAnimationFrame(()=> centerInkGlyph(ig));   // re-fit the word into the small chip
        filled++;
        if(filled === need){ state.locked = true;
          // [24a C-fix] the LAST correct DROP also speaks its WORD (flag#4) — wait for it to end
          // before the celebrate VO (play() would cut it at ~250ms). 4s cap: a stalled clip can
          // never hold the celebration hostage. [bug-hunt F6] Skip the wait on the REVEAL path:
          // revealOne already spoke "reveal" and played no word to protect, so waiting would just let
          // that clip finish and then celebrateThenAdvance(revealed) would speak "reveal" a 2nd time.
          if(revealed){ setTimeout(()=> celebrateThenAdvance(slide, true), 250); }
          else {
            const t0 = Date.now();
            setTimeout(function waitWord(){
              if(CARD.slides[state.idx] !== slide) return;                // navigated away → abort
              if(!isPlaying || Date.now() - t0 > 4000){ celebrateThenAdvance(slide, false); return; }
              setTimeout(waitWord, 150);
            }, 250);
          }
        }
      };
      /* [25d] TERMINAL HELP replaces the old auto-solve (Yasir 2026-07-27, live-caught).
         The old `revealOne()` was three bugs in one: (a) it AUTO-PLACED the answer, which the blessed
         reference forbids — the child must always place it themselves; (b) it picked the FIRST unfilled
         zone, so after failing on म it silently solved क/कमल, a pair the child was not even attempting;
         (c) it spoke `reveal` = "सभी जोड़ियाँ सही हैं।" ("all the pairs are correct") when nothing was
         complete and the child had just been wrong twice. Lowering max_attempts to 2 made it fire sooner
         and this became very visible.
         New behaviour: the count is PER TILE (not a slide-wide streak that any correct drop reset), and
         on the last attempt we glow that tile + its correct zone, dim the other tiles, and wait — the
         child completes it. A drop on any other zone while locked springs back with no extra penalty. */
      const clearHelp = ()=>{
        [...zoneRow.children].forEach(z=> z.classList.remove("reveal-hold"));
        [...tileRow.children].forEach(x=>{
          x.classList.remove("reveal-hold","tile-disabled");
          x.style.removeProperty("pointer-events"); x.style.removeProperty("opacity");
        });
      };
      const terminalHelp = (t)=>{
        t._guideLock = true; revealed = true;   // revealed -> quieter settle + honest telemetry
        const gz = [...zoneRow.children].find(z=> z.dataset.accept === t.textContent.trim());
        if(gz) gz.classList.add("reveal-hold");
        t.classList.add("reveal-hold");
        /* [28d] THE HAND BELONGS ON EVERY TERMINAL-HELP PATH, NOT JUST THE TAP ONE.
           27d put pointNudgeAt in mountTapOptions.revealAnswer and I reported it as "the hand on the
           answer in every phase" — but there are FIVE terminal-help paths and only that one had it.
           Practice and independent rounds in these games are drags / sentence-finds / scene-taps, so
           they glowed with no hand, which is what Yasir is seeing. Point at the TILE the child must
           move (the actionable thing), and stop the flow nudge first so it cannot drag the hand away. */
        travelNudge(t, gz, slide);          /* [28o] tile -> its correct zone, looping */
        [...tileRow.children].forEach(x=>{
          if(x !== t && !x.classList.contains("snapped")){
            x.classList.add("tile-disabled");
            x.style.setProperty("pointer-events","none","important");
            x.style.setProperty("opacity",".4","important");
          }
        });
      };
      [...tileRow.children].forEach(tile => {
        tile._wrong = 0; tile._guideLock = false;
        makeDraggable(tile, (zone, t) => {
          if(state.locked || zone.classList.contains("filled")) return;
          const want = (zone.dataset.accept === t.textContent.trim());
          // guide-locked tile dropped on the WRONG box: penalty-free spring-back, keep guiding
          if(t._guideLock && !want){
            const gz = [...zoneRow.children].find(z=> z.dataset.accept === t.textContent.trim());
            if(gz) gz.classList.add("reveal-hold");
            t.classList.add("reveal-hold");
            return;
          }
          state.attempts++;
          if(want){
            wrongStreak = 0; t._wrong = 0; t._guideLock = false;
            GameBus.emit("letter_image_match_first_try", {
              slide_id: slide.id, phase: slide.phase, value: true,
              letter: t.textContent, attempts: state.attempts
            });
            if(t.dataset.matchAudio) play("assets/Audio/" + t.dataset.matchAudio + "." + AUDIO_EXT, ()=>{});   // [21c flag#4] correct drop → speak the WORD
            leaveTrayGhost(t);   // [25c] ghost slot: placeholder stays where the tile came from
            clearHelp();
            settle(zone, t);
          } else {
            zone.classList.add("filled","wrong");
            dragWrong(slide, t);   // [25b] per-pair hint2 names the tile + its picture
            GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
            setTimeout(()=> zone.classList.remove("filled","wrong"), 600);
            t._wrong++;
            if(t._wrong >= (CARD.scaffold_rules.max_attempts || 3) && !t._guideLock) terminalHelp(t);
          }
        });
      });
    }
  },

  SEQUENCE_DRAG: {
    mount(host, slide){
      const wrap = document.createElement("div"); wrap.className = "dd-stage" + (slide.data.word_mode ? " seq-words" : "");
      // slots row
      const slots = document.createElement("div"); slots.className = "seq-slots";
      slide.data.correct_order.forEach((L,i) => {
        const sl = document.createElement("div"); sl.className = "seq-slot";
        sl.dataset.accept = L; sl.dataset.idx = String(i);
        sl.classList.add("dd-zone");      // reuse drop logic
        sl.innerHTML = `<span class="ordinal">${i+1}</span>`;
        slots.appendChild(sl);
      });
      const tileRow = document.createElement("div"); tileRow.className = "dd-row"; tileRow.style.marginTop = "40px";
      slide.data.tiles.forEach(t => {
        const tl = document.createElement("div"); tl.className = "dd-tile"; tl.innerHTML = `<span class="ink-glyph">${t.letter}</span>`;
        if(t.audio) tl.dataset.audio = t.audio;   // tap-to-hear (SME: "शब्द पर click करने पर आवाज़ आनी चाहिए")
        tileRow.appendChild(tl);
      });
      wrap.appendChild(slots); wrap.appendChild(tileRow);
      host.appendChild(wrap);

      const wordMode = !!slide.data.word_mode;   // [21c flag#5] read-along/glow-order/whole-sentence gated to word mode; letter-sequence siblings untouched
      let placed = 0, wrongStreak = 0, revealed = false; const need = slide.data.correct_order.length;
      state.attempts = 0; state.locked = false;
      const settle = (zone, t)=>{ stopNudge();          // one correct-placement path (drop AND reveal)
        zone.classList.remove("dd-zone");
        zone.classList.add("filled","correct");
        zone.innerHTML = `<span class="ordinal">${parseInt(zone.dataset.idx,10)+1}</span><span class="ink-glyph">${t.textContent.trim()}</span>`;
        centerInkGlyph(zone.querySelector(".ink-glyph"));
        t.remove();
        placed++;
        if(placed === need){
          state.locked = true;
          GameBus.emit("letter_sequence_correct", {
            slide_id: slide.id, phase: slide.phase, value: !revealed,
            attempts: state.attempts, latency_ms: Date.now()-state.slideStart
          });
          if(wordMode){
            // deck (word mode): read the WHOLE sentence aloud at the end, THEN celebrate + advance
            play(audioFor(slide, "reveal") || null, ()=> setTimeout(()=> celebrateThenAdvance(slide, revealed), 300));
          } else {
            setTimeout(()=> celebrateThenAdvance(slide, revealed), 250);
          }
        } else if(wordMode){ glowNext(); }
      };
      // progressive sequence hint, WORD MODE only (SME "पहले आने वाला शब्द पहले glow करेगा फिर दूसरा, तीसरा..."):
      // glow the tile that belongs in the NEXT empty slot, guiding the child one word at a time, in order.
      const glowNext = ()=>{
        [...tileRow.children].forEach(x => x.classList.remove("reveal-glow"));
        const zone = [...slots.children].find(z => !z.classList.contains("filled")); if(!zone) return;
        const t = [...tileRow.children].find(x => x.textContent.trim() === zone.dataset.accept);
        if(t) t.classList.add("reveal-glow");
      };
      // A8 reveal ceiling: after max consecutive misses, demonstrate the NEXT slot in the order.
      const revealOne = ()=>{
        const zone = [...slots.children].find(z=> !z.classList.contains("filled")); if(!zone) return;
        const t = [...tileRow.children].find(x=> x.textContent.trim() === zone.dataset.accept); if(!t) return;
        revealed = true; wrongStreak = 0;
        zone.classList.add("reveal-glow"); t.classList.add("reveal-glow");
        play(audioFor(slide,"reveal") || null, ()=>{});
        zone.classList.add("reveal-hold");                 /* [25d] glow and WAIT — never settle() it for the child */
        terminalHold(t, tileRow.children, slide, zone);   /* [28l] dim distractors + [28o] hand travels to the zone */
      };
      [...tileRow.children].forEach(tile => {
        makeDraggable(tile, (zone, t) => {
          if(state.locked || zone.classList.contains("filled")) return;
          state.attempts++;
          const ok = (zone.dataset.accept === t.textContent.trim());
          if(ok){
            wrongStreak = 0;
            settle(zone, t);
          } else {
            zone.classList.add("wrong");
            setTimeout(()=> zone.classList.remove("wrong"), 600);
            dragWrong(slide);
            GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
            if(++wrongStreak >= (CARD.scaffold_rules.max_attempts||3)) revealOne();
          }
        }, wordMode ? { onTap: ()=>{ if(tile.dataset.audio) play("assets/Audio/" + tile.dataset.audio + "." + AUDIO_EXT, ()=>{}); } } : undefined);   // [21c flag#5] tap a word-tile → speak that word
      });
      if(wordMode) glowNext();   // [21c flag#5] glow the first word immediately; the auto-played prompt speaks over it
    }
  },

  MASTERY_SILENT_PICK: {
    mount(host, slide){
      const mode = slide.data.mode;
      let stimulus = null, options = null, isCorrect = null, optionRenderer = null;
      if(mode === "sound_to_letter"){
          /* [28m] NO VOLUME BUTTON, ANYWHERE. Yasir 2026-07-28: "we use vol button nowhere. if
             nothing then we keep question only." This stimulus had NO image, so 28c left its 🔊 +
             "सुनो" chip alone and flagged it — stripping it looked like it would leave a blank card.
             The ruling settles it: nothing to show => show the QUESTION only, no chip. The chip was
             also the only way to re-hear the sound, so that function moves to the header replay
             (state.replayAudio, set after mount) instead of dying with the affordance. */
          stimulus = null;
        options = slide.data.options;
        isCorrect = (opt) => opt.letter === slide.data.target;
        optionRenderer = (opt) => letterCell(opt.letter);
      } else if(mode === "picture_to_letter"){
        stimulus = stimulusPic(slide.data.picture, slide.data.emoji, slide.data.img);
        options = slide.data.options;
        isCorrect = (opt) => opt.letter === slide.data.target;
        optionRenderer = (opt) => letterCell(opt.letter);
      } else if(mode === "name_to_shape"){
          /* [28m] NO VOLUME BUTTON, ANYWHERE. Yasir 2026-07-28: "we use vol button nowhere. if
             nothing then we keep question only." This stimulus had NO image, so 28c left its 🔊 +
             "सुनो" chip alone and flagged it — stripping it looked like it would leave a blank card.
             The ruling settles it: nothing to show => show the QUESTION only, no chip. The chip was
             also the only way to re-hear the sound, so that function moves to the header replay
             (state.replayAudio, set after mount) instead of dying with the affordance. */
          stimulus = null;
        options = slide.data.options;
        isCorrect = (opt) => opt.shape === slide.data.target;
        optionRenderer = (opt) => shapeCell(opt);
      } else if(mode === "object_to_shape"){
        stimulus = stimulusPic(slide.data.object_hi, slide.data.object_emoji, slide.data.object_img);
        options = slide.data.options;
        isCorrect = (opt) => opt.shape === slide.data.target;
        optionRenderer = (opt) => shapeCell(opt);
      } else if(mode === "shape_to_object"){
        stimulus = stimulusShape({shape: slide.data.shape, color: slide.data.color, rotate: slide.data.rotate});
        options = slide.data.options;
        isCorrect = (opt) => opt.correct === true;
        optionRenderer = (opt) => pictureCell(opt.object_hi, opt.object_emoji, opt.object_img);
      } else { // letter_to_picture
        stimulus = stimulusLetter(slide.data.letter);
        options = slide.data.options;
        isCorrect = (opt) => opt.correct === true;
        optionRenderer = (opt) => pictureCell(opt.picture, opt.emoji, opt.img);
      }
      // SAME scaffold as the rest of the lesson — hint button after 1st wrong,
      // correct/incorrect feedback popups, reveal-on-3rd-wrong. Not silent.
      // `mastery:true` keeps the mastery_score tracking (first-try = hit).
      mountTapOptions({
        slide, host, signalName: "mastery_item",
        stimulus, options, isCorrect, optionRenderer, mastery: true
      });
        /* [28m] the removed chip was the only way to re-hear the sound — keep the FUNCTION on the
           header replay. Set AFTER mount so mountTapOptions cannot overwrite it. */
        state.replayAudio = ()=>{ state.audioReplays++; play(audioFor(slide,"phoneme") || audioFor(slide,"shape_name") || null, ()=>{}); };
    }
  },


  STORY_QUESTION: {
    // TEST: a comprehension question after story beats. A recall thumb (visual anchor) + 🔊 chip
    // form the stimulus; options are 2–3 picture chips. Tap-to-answer feedback is inherited from
    // mountTapOptions. Recall thumb is a CUE, hidden at mastery / when data.hide_recall so the
    // answer isn't leaked by thumb-reading.
    mount(host, slide){
      const d = slide.data || {};
      const stim = document.createElement("div"); stim.className = "story-q-stim"; stim.style.cursor = "pointer";
      const hideRecall = slide.phase === "mastery" || d.hide_recall === true;
      const thumb = (!hideRecall && d.recall_image_id)
        ? '<img class="story-q-thumb" src="assets/Images/' + d.recall_image_id + '.' + IMG_EXT + '" alt="" ' +
          'onerror="this.style.display=\'none\';"/>'
        : '';
      /* [28c] IMAGE ONLY IN THE STIMULUS CARD (Yasir 2026-07-28: "we are not supposed to have both
         the prashn suno and volume icon on the screen anywhere at all. only image in the
         container/card"). The 🔊 glyph and the label were HARDCODED here, so no card could remove
         them — `d.stim_hi` only reworded the label. Now the card holds the recall thumb and nothing
         else.
         The REPLAY still works: stim.onclick is kept, so tapping the picture replays the question,
         and the header volume chip on Swiftie replays it too — the affordance is removed, not the
         function. If the thumb is absent (mastery / d.hide_recall) there is nothing left to show, so
         pass null rather than render an empty card; mountTapOptions already guards `if(stimulus)`.
         NOT applied to the four audio-only chips (TAP_SHAPE_BY_NAME, TAP_LETTER_BY_SOUND,
         MASTERY_SILENT_PICK x2) — those have no image, so stripping the chip would leave a blank card
         and no cue that there is anything to listen to. Flagged for a ruling instead of guessed. */
      stim.innerHTML = thumb;
      stim.onclick = ()=>{ state.audioReplays++; play(audioFor(slide, "prompt") || null); };
      mountTapOptions({
        slide, host,
        signalName: d.signal_name || "story_question_first_try",
        stimulus: thumb ? stim : null,
        options: d.options,
        isCorrect: (opt) => opt.correct === true,
        optionRenderer: (opt) => {
          const cell = document.createElement("div");
          cell.innerHTML =
            imgOrEmoji(opt.img, opt.emoji, "story-q-opt-img", "story-q-opt-emoji") +
            (opt.label_hi ? '<span class="story-q-opt-label">' + opt.label_hi + '</span>' : '');
          return cell;
        },
        mastery: d.mastery === true,
        columnsHint: (d.options && d.options.length) <= 2 ? 2 : 3
      });
    }
  },

  TAP_IN_SCENE: {
    // "Tap the thing in the picture" — a PRODUCE-style comprehension mechanic (NOT an MCQ). A story
    // scene fills the frame; the child taps the target region(s) (e.g. the monkeys who took the caps).
    // A correct hotspot → confetti + advance; a miss → soft buzz + try_again VO; after a few idle
    // seconds the target gently pulses (hint). Data: {image_id, alt_hi, prompt, hotspots:[{x,y,w,h,
    // correct}] (as % of the frame), audio:{prompt,correct,try_again}}. Reusable for any "find X".
    mount(host, slide){
      const d = slide.data || {};
      const wrap = document.createElement("div"); wrap.className = "tis-scene";
      const frame = document.createElement("div");
      /* Object contours are derived per scene (see the ring block in the sheet), so the treatment is
         keyed on the ART, not on a slide id: a scene listed here gets the look-and-find outlines, any
         other TAP_IN_SCENE art keeps its existing capsule interaction until it has its own rings.
         Names are IN HOTSPOT ORDER — objectOutlines[i] must pair with d.hotspots[i]. The length check
         is the guard: if a card ever re-orders or adds a hotspot, the treatment switches itself off
         rather than hanging the wrong outline on the wrong answer. */
      const TIS_CONTOURS = {
        scene_subah: ["ravi","teddy","glass"],       /* G1 — Ravi is the answer, index 0 */
        scene_park:  ["ball","boymid","boyright"],   /* I2 — the ball is the answer, index 0 */
        scene_khoj:  ["khoj_ravi","khoj_girl","khoj_baby"],  /* M1 — Ravi is the answer, index 0 */
      };
      const contourNames = TIS_CONTOURS[d.image_id];
      const naturalFind = !!contourNames && contourNames.length === (d.hotspots || []).length;
      frame.className = "tis-frame" + (naturalFind ? " tis-look-find" : "");
      const img = document.createElement("img"); img.className = "tis-img";
      img.src = "assets/Images/" + d.image_id + "." + IMG_EXT; img.alt = d.alt_hi || "";
      frame.appendChild(img);
      const objectOutlines = [];
      if(naturalFind){
        /* one layer per candidate, in hotspot order — objectOutlines[i] pairs with hotspots[i].
           Inline data: URI because mask-image is CORS-restricted and these decks get reviewed
           straight off disk (file://), where an external mask silently never loads. */
        contourNames.forEach((name)=>{
          const outline = document.createElement("i"); outline.className = "tis-object-outline";
          outline.style.setProperty("--ring", "var(--tis-ring-" + name + ")");
          outline.setAttribute("aria-hidden","true");
          frame.appendChild(outline); objectOutlines.push(outline);
        });
      }
      let done = false, _tisAttempts = 0;
      /* [27j] TWO-RUNG HINT LADDER + TERMINAL HELP for TAP_IN_SCENE.
         It previously played try_again ONLY, so authored audio.hint1/audio.hint were never spoken —
         and because check_system passes on "ids authored + files exist", a 15/15 TAP_IN_SCENE game
         reported COMPLIANT while no hint could ever play. Same graded shape as mountTapOptions
         (24a A2) and dragWrong (25a): 1st wrong -> hint1, 2nd -> hint, at max_attempts -> terminal
         help. Terminal help GLOWS the correct hotspot and the child STILL TAPS IT — never auto-solve
         (rule 9: "never hand the child the answer"). */
      const miss = (tappedIndex)=>{   // [spec] tappedIndex: which hotspot was hit; undefined for a blank-scene tap
        if(done) return;
        /* [h01 2026-07-31] HARD VO GATE (Yasir ruling: no taps while ANY VO speaks - prompt or
           hint alike). TIS was the one tap mechanic with NO JS gate; it relied on the vo-lock CSS
           alone, and a tap slipping past that (or landing on the frame under a disabled hotspot)
           burned an attempt mid-prompt. Every path in: hotspot tap, frame tap. Silently ignored -
           no visual, per the same ruling. */
        if(isPlaying) return;
        _tisAttempts++; sfxWrongSoft(); setSwMood("tryagain");
        const _maxA = (CARD.scaffold_rules && CARD.scaffold_rules.max_attempts) || 3;
        if(_tisAttempts >= _maxA){
          frame.querySelectorAll(".tis-hot.correct-hot").forEach(el => el.classList.add("reveal-hold"));
          const correctOutlineIndex = (d.hotspots || []).findIndex(h => h.correct);
          objectOutlines.forEach((outline, index)=>outline.classList.add(index === correctOutlineIndex ? "is-guide" : "is-muted"));
          /* [h01 2026-07-31] RED FIRST, THEN FADE (RULING_wrong_answer_tap: 2nd wrong = red flash
             first, THEN the disabled state; red is never skipped). .faded lands later in the sheet
             than .wrong-flash at equal specificity, so applying it in the same beat killed the red
             before one frame rendered - the tapped box just vanished. Delay the fade past the
             flash; the green reveal-hold, hand and hint audio stay immediate. */
          setTimeout(()=>{ frame.querySelectorAll(".tis-hot:not(.correct-hot)").forEach(el => el.classList.add("faded")); }, 720);
          const _hot = frame.querySelector(".tis-hot.correct-hot");
          /* terminal help on the contours too, or the outlines would keep saying "all three are
             equal" while the hotspots say otherwise. Child still taps it (rule 9). */
          objectOutlines.forEach((o, k)=> o.classList.add(
            (d.hotspots || [])[k] && d.hotspots[k].correct ? "is-guide" : "is-muted"));
          if(_hot) handOnAnswer(_hot, slide);   /* [28d] hand on the answer, all paths */
          GameBus.emit("answer_revealed", { slide_id: slide.id, phase: slide.phase, attempts: _tisAttempts, reason: "wrong" });
          play(audioFor(slide,"hint") || audioFor(slide,"reveal") || audioFor(slide,"try_again") || null, ()=>{});
        } else if(_tisAttempts >= 2){
          play(midHint(slide), ()=>{});                        /* [28k] rung 2 */
        } else {
          play(audioFor(slide,"hint1") || audioFor(slide,"try_again") || null, ()=>{});
        }
        GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: _tisAttempts });
        /* [spec] question_answered (wrong) for TAP_IN_SCENE — every answer tap is reported, right or
           wrong. A blank-scene tap still burns an attempt here, so it is reported too, with a null
           option id: the child answered, just not on any candidate. */
        GameBus.sendQuestionAnswered(slide, { is_correct: false, score: 0, attempt: _tisAttempts,
          objType: "image",
          objId: (tappedIndex != null ? "hotspot_" + tappedIndex : "scene_blank"),
          ui_index: (tappedIndex != null ? tappedIndex : null),
          original_index: (tappedIndex != null ? tappedIndex : null),
          text: d.alt_hi || null,
          mediaUrl: (CARD.assets && CARD.assets.image && CARD.assets.image[d.image_id]) || null });
      };
      (d.hotspots || []).forEach((h, i) => {
        const hs = document.createElement("button"); hs.className = "tis-hot" + (h.correct ? " correct-hot" : "");
        hs.type = "button"; hs.setAttribute("aria-label", "Picture choice " + (i + 1));
        hs.style.left=h.x+"%"; hs.style.top=h.y+"%"; hs.style.width=h.w+"%"; hs.style.height=h.h+"%";
        /* [31a] --i phases the spotlight breath/ripple per candidate (negative delay = already running,
           so nobody sits still waiting its turn). Style only — identical treatment, no answer leak. */
        hs.style.setProperty("--i", i);
        /* [2026-08-04] Hover lights the PAIRED OUTLINE (object-shaped) instead of a glow inset into
           this rectangle — see the .is-hover note in the sheet. Presentation only: it adds and removes
           one class and touches no attempt counter, no audio and no answer state. Skipped once the
           slide is done or while a VO is speaking, so it can never contradict the graded feedback or
           imply the child may act during the prompt. */
        hs.onmouseenter = ()=>{ const o = objectOutlines[i];
          if(o && !done && !isPlaying) o.classList.add("is-hover"); };
        hs.onmouseleave = ()=>{ const o = objectOutlines[i]; if(o) o.classList.remove("is-hover"); };
        hs.onclick = (e)=>{ e.stopPropagation(); if(done) return;
          if(isPlaying) return;   /* [h01 2026-07-31] hard VO gate - see miss() */
          if(h.correct){ done=true; hs.classList.add("hit"); frame.classList.add("solved");
            objectOutlines.forEach((outline,index)=>outline.classList.add(index === i ? "is-correct" : "is-muted"));
            sfxCorrect(); confettiCannon(); setSwMood("happy");
            GameBus.emit(d.signal_name || "scene_tap_first_try", {slide_id:slide.id, phase:slide.phase, correct:true});
            /* [spec] question_answered (correct) for TAP_IN_SCENE. This template does NOT go through
               mountTapOptions, so without this the card's three tap-the-picture questions (G1/I2/M1)
               would report question_started and then nothing. The "option" here is a hotspot: its
               index is both the ui and the authored index (hotspots are never shuffled), and the media
               is the scene image the child is tapping into. */
            GameBus.sendQuestionAnswered(slide, { is_correct: true, score: _tisAttempts === 0 ? 1 : 0, attempt: _tisAttempts + 1,
              objType: "image", objId: "hotspot_" + i, ui_index: i, original_index: i,
              text: d.alt_hi || null,
              mediaUrl: (CARD.assets && CARD.assets.image && CARD.assets.image[d.image_id]) || null });
            play(audioFor(slide,"correct")||null, ()=> setTimeout(()=>completeSlide(true), 900)); }
          else { hs.classList.add("shake","wrong-flash");
            const outline = objectOutlines[i]; if(outline){ outline.classList.add("is-wrong"); setTimeout(()=>outline.classList.remove("is-wrong"),700); }
            setTimeout(()=>hs.classList.remove("wrong-flash"),700); miss(i); } };   // [spec] pass the tapped hotspot index through
        frame.appendChild(hs);
      });
      frame.onclick = (e)=>{   // blank scene tap: counts as a try, but leaves no mark on the picture
        if(done || isPlaying) return;
        /* [2026-08-04] The red .tis-scene-ripple disc that used to bloom at the touch point is gone —
           it stamped a red mark onto bare wall or floor, nowhere near a candidate. miss() is
           unchanged, so the buzz, the attempt count and the hint ladder behave exactly as before. */
        miss();
      };
      wrap.appendChild(frame); host.appendChild(wrap);
      $("navBtn").style.display = "none";   // advance on the correct tap — no आगे on a pick
      state.replayAudio = ()=> play(audioFor(slide,"prompt")||null, ()=>{});
      setSwMood("point");
      play(audioFor(slide,"prompt")||null, ()=>{});
      /* [28e] REMOVED: a 6s timer that pulsed the CORRECT hotspot alone, before the child had tried
         anything. Measured on the built game — at t=1s all three hotspots are identical; at t=7s only
         .correct-hot carries `tisPulse`. That hands over the answer for free (rule-9 class breach).
         Yasir 2026-07-28: "this is just like giving hints for the correct answer right from start ...
         only glow after second wrong attempt when all other options get disabled." The glow now comes
         ONLY from terminal help in miss() at max_attempts, where the distractors also fade. */
    }
  },

  /* ===== [reskin] PORTED from the HI02H12_L01_S01 engine (2026.07.21b-unified): the punctuation lesson's own
     content modules. Same helper contracts (mountTapOptions / makeDraggable / dragWrong / celebrateThenAdvance /
     startNudge / imgOrEmoji / audioFor / setNavActive / completeSlide); only the bus name changed (SwiftPAL -> GameBus). ===== */
  QTYPE_RECAP: {
    mount(host, slide){
      const d = slide.data || {};
      const wrap = document.createElement("div"); wrap.className = "ev-recap";
      const els = (d.cards || []).map(c=>{ const el = document.createElement("div"); el.className = "ev-recap-card " + (c.kind === "inference" ? "inference" : "literal");
        el.innerHTML = `<div class="rc-ic${c.icon ? " glyph" : ""}">${c.icon || (c.kind === "inference" ? "🔍" : "📖")}</div><div class="rc-title">${c.title_hi || ""}</div>` +
          `<div class="rc-body">${c.body_hi || ""}</div>` + (c.example_hi ? `<div class="rc-ex">${c.example_hi}</div>` : "");
        el._src = c.audio ? ("assets/Audio/" + c.audio + "." + AUDIO_EXT) : null;
        el.onclick = ()=>{ state.audioReplays++; play(el._src); };
        wrap.appendChild(el); return el; });
      if(els.length > 2){ wrap.style.gridTemplateColumns = `repeat(${els.length}, minmax(0, 330px))`; wrap.classList.add("n" + els.length); }
      host.appendChild(wrap);
      state.ownsAudio = true; setNavActive(false);
      $("navBtn").onclick = ()=>{ if(!$("navBtn").disabled) completeSlide(true); };
      let armed = false; const arm = ()=>{ if(armed) return; armed = true; els.forEach(e=> e.classList.remove("now")); setNavActive(true); setSwMood("point"); };
      const run = (i)=>{ els.forEach(e=> e.classList.remove("now")); if(i >= els.length){ arm(); return; }
        els[i].classList.add("now", "seen"); play(els[i]._src, ()=> setTimeout(()=> run(i + 1), 300)); };
      state.replayAudio = ()=> run(0);
      setSwMood("teach");
      const pre = audioFor(slide, "prompt");
      if(pre) play(pre, ()=> run(0)); else run(0);
      setTimeout(arm, 45000);
    }
  },
  BUILD_PUNCT: {
    mount(host, slide){
      const d = slide.data || {};
      const A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const wrap = document.createElement("div"); wrap.className = "bp-stage";
      const card = document.createElement("div"); card.className = "bp-card";
      if(d.image_id) card.insertAdjacentHTML("beforeend", `<div class="bp-pic">${imgOrEmoji(d.image_id, "✏️", "bp-img", "bp-emoji")}</div>`);
      const body = document.createElement("div"); body.className = "bp-body";
      const tools = document.createElement("div"); tools.className = "bp-tools";
      const runBtn = document.createElement("button"); runBtn.className = "bp-listen run"; runBtn.innerHTML = "🔊 बिना रुके";
      const okBtn = document.createElement("button"); okBtn.className = "bp-listen ok"; okBtn.innerHTML = "🔊 सही ठहराव"; okBtn.style.visibility = "hidden";
      const counter = document.createElement("div"); counter.className = "bp-count";
      tools.appendChild(runBtn); tools.appendChild(counter); tools.appendChild(okBtn);
      const line = document.createElement("div"); line.className = "bp-line";
      const need = {}; (d.marks || []).forEach(m=> need[m.gap] = m);
      const gaps = [], chips = [];
      (d.words || []).forEach((w, i)=>{
        const c = document.createElement("span"); c.className = "bp-word"; c.textContent = w; line.appendChild(c); chips.push(c);
        const g = document.createElement("span"); g.className = "bp-gap dd-zone"; g.dataset.gap = String(i);
        g.innerHTML = '<span class="bp-mark"></span>'; line.appendChild(g); gaps.push(g); });
      body.appendChild(tools); body.appendChild(line); card.appendChild(body);
      const tray = document.createElement("div"); tray.className = "bp-tray";
      let sel = null;
      const tiles = (d.palette || []).map(p=>{ const t = document.createElement("div"); t.className = "bp-tile";
        t.dataset.mark = p.mark; t.innerHTML = `<span class="bt-glyph">${p.mark}</span><span class="bt-name">${p.name_hi || ""}</span>`;
        t._src = A(p.audio); tray.appendChild(t); return t; });
      wrap.appendChild(card); wrap.appendChild(tray); host.appendChild(wrap);
      const total = (d.marks || []).length; let placed = 0;
      const setCount = ()=>{ counter.innerHTML = `✏️ <b>${placed}</b> / ${total}`; }; setCount();
      runBtn.onclick = ()=>{ if(state.hintActive) return; state.audioReplays++; chips.forEach(c=> c.classList.add("rush")); play(A(d.runon_audio), ()=> chips.forEach(c=> c.classList.remove("rush"))); };
      okBtn.onclick = ()=>{ if(state.hintActive) return; state.audioReplays++; play(A(d.correct_audio)); };
      const put = (g, mark)=>{ g.classList.add("filled", "correct"); g.querySelector(".bp-mark").textContent = mark; placed++; setCount(); };
      state.ownsAudio = true; state.attempts = 0; state.locked = false; state.scaffoldLevel = 0;
      const readCorrect = (after)=>{ okBtn.style.visibility = ""; line.classList.add("reading"); play(A(d.correct_audio), ()=>{ line.classList.remove("reading"); after(); }); };
      if(d.auto){
        $("hintBtn").style.display = "none"; const nav = $("navBtn"); nav.style.display = ""; setNavActive(false);
        nav.onclick = ()=>{ if(!nav.disabled) completeSlide(true); };
        let armed = false; const arm = ()=>{ if(armed) return; armed = true; setNavActive(true); setSwMood("point"); };
        const placeAll = (i, done)=>{ const ms = d.marks || []; if(i >= ms.length){ done(); return; }
          const m = ms[i], g = gaps[m.gap], t = tiles.find(x=> x.dataset.mark === m.mark);
          if(t) t.classList.add("pick"); g.classList.add("glow");
          setTimeout(()=>{ if(t) t.classList.remove("pick"); g.classList.remove("glow"); put(g, m.mark); sfxTap();
            play(A(m.audio), ()=> setTimeout(()=> placeAll(i + 1, done), 300)); }, 700); };
        const seq = ()=>{ placed = 0; gaps.forEach(g=>{ g.classList.remove("filled", "correct"); g.querySelector(".bp-mark").textContent = ""; }); setCount();
          okBtn.style.visibility = "hidden"; setSwMood("talk");
          play(audioFor(slide, "prompt") || null, ()=>{ chips.forEach(c=> c.classList.add("rush"));
            play(A(d.runon_audio), ()=>{ chips.forEach(c=> c.classList.remove("rush")); setSwMood("teach");
              play(audioFor(slide, "explain") || null, ()=> placeAll(0, ()=> readCorrect(()=>{ burstStars(); setSwMood("happy");
                play(audioFor(slide, "conclude") || null, arm); }))); }); }); };
        state.replayAudio = seq; seq(); setTimeout(arm, 90000);
        return;
      }
      let streak = 0;
      const maxA = (CARD.scaffold_rules && CARD.scaffold_rules.max_attempts) || 3;
      const nextNeed = ()=> (d.marks || []).find(m=> !gaps[m.gap].classList.contains("filled"));
      const finish = ()=>{ state.locked = true; tiles.forEach(t=> t.classList.remove("sel"));
        if(d.mastery){ state.masteryAttempts++; if(state.attempts === 0) state.masteryHits++; }
        GameBus.emit("punct_build_done", { slide_id: slide.id, phase: slide.phase, value: state.scaffoldLevel < 3,
          first_try: state.attempts === 0, wrong: state.attempts, latency_ms: Date.now() - state.slideStart });
        sfxCorrect(); confettiCannon(); setSwMood("happy");
        readCorrect(()=>{ const ec = d.echo ? audioFor(slide, "echo") : null;
          if(ec){ line.classList.add("echo"); play(ec, ()=> setTimeout(()=>{ line.classList.remove("echo"); completeSlide(state.scaffoldLevel < 3); }, 3500)); }
          else setTimeout(()=> completeSlide(state.scaffoldLevel < 3), 600); }); };
      const reveal = ()=>{ const m = nextNeed(); if(!m) return; state.scaffoldLevel = 3; streak = 0; state.hintActive = true; setSwMood("hint");
        const g = gaps[m.gap]; g.classList.add("glow");
        play(audioFor(slide, "reveal") || null, ()=>{ g.classList.remove("glow"); put(g, m.mark);
          play(A(m.audio), ()=>{ state.hintActive = false; if(placed === total) finish(); }); }); };
      const hint = ()=>{ const m = nextNeed(); if(!m) return; state.scaffoldLevel = Math.max(state.scaffoldLevel, 2); setSwMood("hint");
        const g = gaps[m.gap]; g.classList.add("glow"); setTimeout(()=> g.classList.remove("glow"), 3500);
        play(audioFor(slide, "hint") || null, ()=>{}); };
      const tryPlace = (g, mark)=>{ if(state.locked || state.hintActive || g.classList.contains("filled")) return;
        const want = need[g.dataset.gap];
        if(want && want.mark === mark){ streak = 0; put(g, mark); sfxCorrect(); setSwMood("happy");
          play(A(want.audio), ()=>{ if(placed === total) finish(); }); return; }
        state.attempts++; streak++; g.classList.add("wrong-flash"); setTimeout(()=> g.classList.remove("wrong-flash"), 600);
        sfxWrongSoft(); setSwMood("tryagain"); $("hintBtn").classList.add("show");
        GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts, gap: +g.dataset.gap, mark });
        if(streak >= maxA) reveal();
        else if(streak === 2) hint();
        else play((want && audioFor(slide, "wrong_mark")) || audioFor(slide, "try_again") || null, ()=>{}); };
      tiles.forEach(t=>{
        const pick = ()=>{ if(state.locked || state.hintActive) return; stopNudge(); tiles.forEach(x=> x.classList.remove("sel")); t.classList.add("sel"); sel = t.dataset.mark; play(t._src); };
        t.addEventListener("mousedown", pick); t.addEventListener("touchstart", pick, {passive:true});
        makeDraggable(t, (zone)=>{ const g = zone.closest(".bp-gap"); if(g) tryPlace(g, t.dataset.mark); }); });
      gaps.forEach(g=> g.addEventListener("click", ()=>{ if(sel) tryPlace(g, sel); }));
      $("hintBtn").onclick = ()=>{ if(state.locked || state.hintActive) return; state.hintUsed = true;
        GameBus.emit("hint_shown", { slide_id: slide.id, manual: true }); hint(); };
      $("navBtn").style.display = "none"; setNavActive(false);
      state.replayAudio = ()=> play(audioFor(slide, "prompt") || null, ()=>{});
      setSwMood("point"); play(audioFor(slide, "prompt") || null, ()=>{});
      startNudge(slide, tiles[0]);
    }
  },
  EVIDENCE_QA: {
    mount(host, slide){
      const d = slide.data || {}; const qt = d.qtype === "inference" ? "inference" : "literal";
      const wrap = document.createElement("div"); wrap.className = "ev-qa";
      const card = evPassage(d.passage); const lines = card._lines;
      const right = document.createElement("div"); right.className = "ev-right";
      wrap.appendChild(card); wrap.appendChild(right); host.appendChild(wrap);
      const chip = evQtypeChip(qt, d.chip_hi, d.chip_icon); chip.style.cursor = "pointer";
      chip.onclick = ()=>{ if(state.hintActive) return; state.audioReplays++; play(audioFor(slide, "prompt") || null); };
      const ev = d.evidence || [];
      const showEv = ()=> evMark(lines, ev, qt);
      const pulse = (on)=> ev.forEach(i=> lines[i] && lines[i].classList.toggle("ev-pulse", on));
      lines.forEach(l=> l.onclick = ()=>{ if(state.hintActive || d.auto) return; state.audioReplays++; play(l._src); });
      const hintAction = (done)=>{ showEv(); pulse(true); setSwMood("hint");
        play(audioFor(slide, "hint") || null, ()=>{ pulse(false); done(); }); };
      mountTapOptions({ slide, host: right, signalName: d.signal_name || "evidence_qa_first_try", stimulus: chip,
        options: d.options, isCorrect: o=> o.correct === true, columnsHint: 1, mastery: d.mastery === true,
        hintAction, nudgeTarget: null,
        optionRenderer: (o)=>{ const c = document.createElement("div"); c.className = "ev-opt" + ((o.img || o.emoji) ? "" : " text-only");
          if(o.correct) c.dataset.ok = "1";
          c.innerHTML = ((o.img || o.emoji) ? imgOrEmoji(o.img, o.emoji, "ev-opt-img", "ev-opt-emoji") : "") +
                        `<span class="ev-opt-lbl">${o.label_hi || ""}</span>`;
          return c; } });
      state.ownsAudio = true;
      if(d.highlight) showEv();
      if(d.auto){
        state.locked = true; stopNudge(); $("hintBtn").style.display = "none";
        const nav = $("navBtn"); nav.style.display = ""; setNavActive(false);
        nav.onclick = ()=>{ if(!nav.disabled) completeSlide(true); };
        const evSrcs = ev.map(i=> lines[i] && lines[i]._src).filter(Boolean);
        let armed = false; const arm = ()=>{ if(armed) return; armed = true; setNavActive(true); setSwMood("point"); };
        const seq = (done)=>{ setSwMood("teach");
          play(audioFor(slide, "prompt") || null, ()=> play(audioFor(slide, "explain_type") || null, ()=>{
            showEv(); pulse(true);
            playChain(evSrcs, 0, ()=>{ pulse(false);
              play(audioFor(slide, "explain_answer") || null, ()=>{
                const ok = right.querySelector('.opt-cell[data-ok="1"]');
                if(ok){ ok.classList.add("correct"); right.querySelectorAll(".opt-cell").forEach(c=>{ if(c !== ok) c.classList.add("faded"); }); }
                sfxCorrect(); burstStars(); setSwMood("happy"); if(done) done(); }); }); })); };
        state.replayAudio = ()=> seq(arm);
        seq(arm);
        setTimeout(arm, 60000);
      } else {
        state.replayAudio = ()=> play(audioFor(slide, "prompt") || null, ()=>{});
        play(audioFor(slide, "prompt") || null, ()=>{});
      }
    }
  },
  SORT_QTYPE: {
    mount(host, slide){
      const d = slide.data || {};
      const wrap = document.createElement("div"); wrap.className = "ev-sort";
      const bins = document.createElement("div"); bins.className = "ev-sort-bins";
      const mkBin = (kind, ic, title)=>{ const b = document.createElement("div"); b.className = "ev-sort-bin dd-zone " + kind;
        b.dataset.kind = kind; b.innerHTML = `<div class="esb-title"><span class="ic">${ic}</span>${title}</div><div class="esb-items"></div>`;
        bins.appendChild(b); return b; };
      const _bins = d.bins || [{kind:"literal", icon:"📖", title_hi:"कहानी में लिखा है"}, {kind:"inference", icon:"🔍", title_hi:"सोचकर पता चला"}];
      const bL = mkBin(_bins[0].kind, _bins[0].icon, _bins[0].title_hi), bI = mkBin(_bins[1].kind, _bins[1].icon, _bins[1].title_hi);
      const tray = document.createElement("div"); tray.className = "ev-sort-tray";
      const items = (d.items || []).slice();
      for(let i = items.length - 1; i > 0; i--){ const j = (Math.random()*(i+1))|0; [items[i], items[j]] = [items[j], items[i]]; }
      let sel = null;
      const tiles = items.map(it=>{ const t = document.createElement("div"); t.className = "ev-sort-item";
        t.dataset.kind = it.kind; t.innerHTML = `<span class="esi-text">${it.text}</span>`;
        t._src = it.audio ? ("assets/Audio/" + it.audio + "." + AUDIO_EXT) : null;
        const speak = ()=>{ if(t.classList.contains("snapped") || state.locked || state.hintActive) return; stopNudge(); state.audioReplays++;
          tiles.forEach(x=> x.classList.remove("sel")); t.classList.add("sel"); sel = t; play(t._src); };
        t.addEventListener("mousedown", speak); t.addEventListener("touchstart", speak, {passive:true});
        tray.appendChild(t); return t; });
      wrap.appendChild(bins); wrap.appendChild(tray); host.appendChild(wrap);
      state.attempts = 0; state.locked = false; state.ownsAudio = true;
      const maxA = (CARD.scaffold_rules && CARD.scaffold_rules.max_attempts) || 3;
      let placed = 0, streak = 0, revealed = false; const need = tiles.length;
      const settle = (bin, t)=>{ t.classList.remove("sel", "dragging"); t.classList.add("snapped"); t.style.transform = "";
        bin.querySelector(".esb-items").appendChild(t); placed++; if(sel === t) sel = null;
        if(placed === need){ state.locked = true;
          if(d.mastery){ state.masteryAttempts++; if(state.attempts === need) state.masteryHits++; }
          GameBus.emit("qtype_sort_done", { slide_id: slide.id, phase: slide.phase, value: !revealed,
            attempts: state.attempts, latency_ms: Date.now() - state.slideStart });
          setTimeout(()=> celebrateThenAdvance(slide, revealed), 300); } };
      const revealOne = ()=>{ const t = tiles.find(x=> !x.classList.contains("snapped")); if(!t) return;
        revealed = true; streak = 0; const bin = t.dataset.kind === bI.dataset.kind ? bI : bL;
        t.classList.add("reveal-glow"); bin.classList.add("reveal-glow"); state.hintActive = true;
        play(audioFor(slide, "reveal") || null, ()=>{ t.classList.remove("reveal-glow"); bin.classList.remove("reveal-glow");
          state.hintActive = false; settle(bin, t); }); };
      const tryDrop = (bin, t)=>{ if(state.locked || state.hintActive || t.classList.contains("snapped")) return;
        state.attempts++;
        if(bin.dataset.kind === t.dataset.kind){ streak = 0; sfxCorrect(); burstStars(); setSwMood("happy"); settle(bin, t); }
        else { t.style.transform = ""; bin.classList.add("wrong-flash"); setTimeout(()=> bin.classList.remove("wrong-flash"), 600);
          $("hintBtn").classList.add("show");
          GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
          if(++streak >= maxA){ sfxWrongSoft(); setSwMood("hint"); revealOne(); }
          else if(streak === 2){ sfxWrongSoft(); setSwMood("hint"); play(audioFor(slide, "hint") || null, ()=>{}); }
          else dragWrong(slide); } };
      tiles.forEach(t=> makeDraggable(t, (zone, tile)=>{ const bin = zone.closest(".ev-sort-bin"); if(bin) tryDrop(bin, tile); }));
      [bL, bI].forEach(b=> b.addEventListener("click", ()=>{ if(sel) tryDrop(b, sel); }));
      $("hintBtn").onclick = ()=>{ if(state.locked || state.hintActive) return; state.hintUsed = true;
        GameBus.emit("hint_shown", { slide_id: slide.id, manual: true }); setSwMood("hint"); play(audioFor(slide, "hint") || null, ()=>{}); };
      $("navBtn").style.display = "none"; setNavActive(false);
      state.replayAudio = ()=> play(audioFor(slide, "prompt") || null, ()=>{});
      setSwMood("point");
      play(audioFor(slide, "prompt") || null, ()=>{});
      startNudge(slide, tiles[0]);
    }
  },

  /* ===== [story-fig] STORY_LISTEN — the Figma story page, the first screen after the start gate's peek
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

  /* ===== [recap-fig] MARKS_RECAP — "ये हैं तीन विराम चिह्न" (FLN-by-MJ frame 508:2), the three-marks recap after the
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

  /* ===== [demo-fig] PUNCT_DEMO — the run-on sentence demos (FLN-by-MJ frames 519:32 "G3 guided story question" = T2,
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
     [pick-fig] PUNCT_PICK (G1, frame 525:354 "7 G1"; G2, frame 600:197 "8 G2") is the same page with the tap left to the CHILD: steps 1-3 as above,
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
        state.replayAudio = ()=>{ if(!live) return; const mine = ++reread;
          const hot = (n)=>{ if(mine === reread) L.words.forEach((w, i)=> w.classList.toggle("hot", i === n - 1)); };
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

  PHASE_TRANSITION: {
    // Additive "learning journey" beat between arc phases (the MoM "no sense of progression" fix).
    // Full-screen friendly panel: badge + "अब हम ___ करेंगे" headline + a 5-dot journey map with the
    // current step lit. The header Swiftie presents it (ONE-Swiftie rule — no second mascot). Learner-
    // paced: no auto-advance timer; आगे unlocks when the beat's VO ends (immediately if silent).
    // data:{ headline_hi, icon?, step (1-based), total_steps?, to_phase? }. Build scripts weave one of
    // these before each phase change; older cards without it are untouched (purely additive).
    mount(host, slide){
      const d = slide.data || {};
      const panel = document.createElement("div"); panel.className = "phase-transition";
      const total = d.total_steps || 5, step = Math.min(d.step || 1, total);
      let map = '<div class="pt-map">';
      for(let i = 1; i <= total; i++){
        map += `<span class="pt-step ${i < step ? 'done' : i === step ? 'current' : ''}"></span>`;
        if(i < total) map += '<span class="pt-connector"></span>';
      }
      map += '</div>';
      panel.innerHTML =
        `<div class="pt-badge">${d.icon || '🎯'}</div>` +
        `<div class="pt-headline">${d.headline_hi || slide.prompt_hi || ''}</div>` + map;
      host.appendChild(panel);
      setSwMood("teach");
      GameBus.emit("phase_transition_shown", { slide_id: slide.id, to_phase: d.to_phase || slide.phase, step });
      state.ownsAudio = true; state.locked = false; setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
      const vo = audioFor(slide, "prompt");
      if(vo) play(vo, ()=> setNavActive(true)); else setNavActive(true);
    }
  },

  CELEBRATION: {
    mount(host, slide){
      // celebration SFX — own Audio element so it overlaps the spoken VO chain
      playSfx(slide.audio && slide.audio.sfx ? slide.audio.sfx : "sfx_celebrate");
      /* The long authored completion line now plays on the final fill-result summary. This separate
         mascot screen owns audio so autoPlayChain cannot replay it here; only “शाबाश!” is spoken. */
      state.ownsAudio = true;
      const endPraiseVo = audioFor(slide, "prompt") || null;   // [reskin] this lesson's own celebration line (vo_celebrate)
      /* [r57] “शाबाश!” is spoken when Swiftie TALKS, not while she jumps. The approved GIF is 36
         frames × 90ms: frames 0–9 are the jump (open-beaked cheer, eyes shut, peak at frame 4, landing
         at frame 9), frames 10–17 she stands with her beak shut, and from frame 18 she waves and
         her beak opens and closes — the talking. The old timer started the VO at 90ms on the
         assumption that frame 1's open beak was speech, so the praise played over the jump. It now
         starts on frame 18; the 1.48s clip ends at about 3.1s, inside the talking frames, before the
         3.24s swap to the still pose. */
      const GIF_FRAME_MS = 90, TALK_START_FRAME = 18;
      const TALK_START_MS = TALK_START_FRAME * GIF_FRAME_MS;
      let endVoTimer = 0, endFreezeTimer = 0, endVoStarted = false;
      const startEndVoAtMouth = (delay = TALK_START_MS)=>{
        if(endVoStarted) return;
        endVoStarted = true;
        endVoTimer = setTimeout(()=>{ if(es.classList.contains("show")) play(endPraiseVo, ()=>{}); }, delay);
      };
      // show end screen overlay + a big Hindi headline (== the VO) so the finale feels like a reward
      /* [30i] NO text on the last page (Yasir): only the button carries writing. Emptied,
         not removed — .end-title:empty / .end-subtitle:empty are already display:none. */
      const et = $("endTitle"); if(et) et.textContent = "";
      const st = $("endSubtitle"); if(st) st.textContent = "";
      const es = $("endScreen"); es.classList.add("show","hint-glow");
      document.body.classList.add("is-end");   // r4: immersive sunburst backdrop (end_screen.webp)
      const endMascot = es.querySelector(".end-mascot");
      if(endMascot && endMascot.tagName === "IMG"){
        /* Restart the GIF when the end screen actually opens. Otherwise it has already been looping
           invisibly since page load and its mouth can be on an arbitrary frame when the VO begins. */
        endMascot.style.visibility = "hidden";
        endMascot.onload = ()=>{
          endMascot.style.animation = "none"; void endMascot.offsetWidth; endMascot.style.animation = "";
          endMascot.style.visibility = "visible";
          startEndVoAtMouth();
          /* Let the GIF play exactly once, then hold Swiftie in a calm neutral pose. Animated GIFs
             cannot be CSS-paused, so swap to the approved animation's neutral frame after 3.24s. */
          clearTimeout(endFreezeTimer);
          endFreezeTimer = setTimeout(()=>{
            if(!endMascot.isConnected) return;
            endMascot.onload = null; endMascot.onerror = null;
            endMascot.src = "assets/UI/swiftee_end_pause.png";
          }, 3240);
        };
        /* No animation to sync to → the praise plays straight away instead of waiting for frame 18. */
        endMascot.onerror = ()=>{ endMascot.style.visibility = "visible"; startEndVoAtMouth(0); };
        endMascot.src = "assets/UI/swiftee_end_page.gif?r=" + Date.now();
        /* [r57] Last-resort only, so the praise is never lost if the GIF stalls. It used to fire at
           1.5s and start the frame-18 countdown itself, so a GIF that was merely slow to load (it is
           1.7 MB, refetched each time to restart it) began its jump AFTER the voice was already
           counting down and the two no longer lined up. It now waits 4s, giving a slow load the
           chance to sync through onload, and if it does fire it speaks at once. */
        setTimeout(()=>{ if(!endVoStarted){ endMascot.style.visibility = "visible"; startEndVoAtMouth(0); } }, 4000);
      } else startEndVoAtMouth(0);
      const c = $("confetti"); c.innerHTML = "";
      starBurst();   // r4: gold star burst from centre (replaces flat falling confetti)
      const masteryScore = state.masteryAttempts ? (state.masteryHits/state.masteryAttempts) : 0;
      GameBus.emit("mastery_score", { value: masteryScore, hits: state.masteryHits, attempts: state.masteryAttempts });
      GameBus.emit("lesson_completed", { skill_code: CARD.skill_code, total_signals: GameBus.signals.length });
      runValidator();
      setNavActive(false);
      /* [h01 local] आगे बढ़ें IS THERE FROM THE START (Yasir 2026-07-29: "you are making the button
         appear after the VO is completed, the button should be there itself by default"). It used to
         be hidden and revealed by autoPlayChain's onDone, so the end screen sat with nothing to do on
         it for the length of the celebration line. Shown on mount instead; endBtnPending stays false
         so the later reveal is a no-op rather than a second, conflicting show.
         NOTE, checked rather than assumed: .end-btn is NOT in the vo-lock selector list, so unlike
         आगे on a normal slide this button is BOTH visible and TAPPABLE while the celebration line
         plays — a child can leave before the praise finishes. Left that way deliberately: locking it
         would mean a visible button that silently does nothing for ~4s, which is the exact
         non-response Yasir objected to, and leaving the end screen early costs the child nothing.
         Flagged for a ruling; add .end-btn to the vo-lock list if he wants it held. */
      const eb = $("endBtn"); eb.dataset.completed = "0"; eb.disabled = false; eb.classList.add("show", "hint-glow");
      state.endBtnPending = false;
      // dev-only: a small "download results" button (teacher/QA), never in child flow
      if(new URLSearchParams(location.search).has("dev") && !$("dlResults")){
        const dl = document.createElement("button"); dl.id = "dlResults"; dl.textContent = "⬇ results JSON";
        dl.style.cssText = "position:absolute;bottom:20px;left:20px;z-index:5;font-family:var(--font-hi);font-weight:700;font-size:16px;padding:8px 16px;border-radius:12px;border:2px solid #B7DCFB;background:#fff;color:var(--navy);cursor:pointer;";
        dl.onclick = ()=> GameBus.downloadResults();
        es.appendChild(dl);
      }
      eb.onclick = ()=>{
        if(eb.dataset.completed === "1") return;
        clearTimeout(endVoTimer);
        clearTimeout(endFreezeTimer);
        sfxNextButton();
        eb.dataset.completed = "1";
        eb.disabled = true;
        /* [spec] activity_completed — ONLY here, on the आगे बढ़ें tap, never at celebration mount, so a
           host that redirects on it still lets the child see the celebration and choose to move on.
           completed/progress are always true/100 (the event exists only at the end; there is no
           partial variant). score = first-try accuracy across all answered questions, 0–1 to 2dp —
           it is not always 1. [B5] the lesson_complete handshake rides the same tap. */
        const qVals = Object.values(GameBus._qStats);
        const firstTryScore = qVals.length ? Math.round((qVals.filter(Boolean).length / qVals.length) * 100) / 100 : 0;
        GameBus.xapi("activity_completed", { type: "activity", id: CARD.skill_code },
          { completed: true, progress: 100, score: firstTryScore, duration_ms: Date.now() - GameBus.startedAt },
          { title: (CARD.title && (CARD.title[CARD.medium] || CARD.title.hi)) || null });
        try{ window.parent?.postMessage({type:"swiftpal:lesson_complete", signals: GameBus.signals, validatorReport: GameBus.validatorReport}, "*"); }catch(e){}
        GameBus.emit("proceed_next", { skill_code: CARD.skill_code, part: CARD.part_label });
        try{ window.parent?.postMessage({type:"swiftpal:proceed", skill_code:CARD.skill_code, part:CARD.part_label}, "*"); }catch(e){}
      };
    }
  },

  /* ===== 16j: FLN sentence + repeated-sound modules — PORTED from the delivered 15b/15d engines.
     Fingerprinted first (two-diverged-engines lesson): same `-unified` lineage, IDENTICAL helper
     contracts (audioFor, setNavActive, completeSlide, mountTapOptions, state fields, sfxCorrect, sfxWrongSoft,
     confettiCannon/setSwMood/imgOrEmoji/letterCell/pictureCell). Verified each call resolves in 16i
     before porting — not a blind paste. Used by HI01H06 (READ/FIND/PICK_PIC) + HIKGH02_L01_S03_P2
     (SOUND/TAP_ALL). ===== */
  SENTENCE_READ: {
    mount(host, slide){
      const d = slide.data;
      const wrap = document.createElement("div"); wrap.className = "sentence-read";
      if(d.image || d.image_emoji){ const im = document.createElement("div"); im.className = "sentence-img";   // 16k: optional illustration above the line
        im.innerHTML = imgOrEmoji(d.image, d.image_emoji, "s-img", "s-emoji"); wrap.appendChild(im); }
      const strip = document.createElement("div"); strip.className = "sentence-strip";
      (d.words || []).forEach(w => {
        const chip = document.createElement("div"); chip.className = "sentence-word";
        chip.innerHTML = `<span class="sw-text ink-glyph">${w.text}</span>`;
        chip.onclick = ()=>{ chip.classList.add("said"); state.audioReplays++;
          if(w.audio) play("assets/Audio/" + w.audio + "." + AUDIO_EXT); };
        strip.appendChild(chip);
      });
      const readBtn = document.createElement("button"); readBtn.className = "read-whole-btn";
      readBtn.innerHTML = `पूरा पढ़ो`;                          /* [28m] no volume glyph */
      const wholeSrc = d.whole_audio ? ("assets/Audio/" + d.whole_audio + "." + AUDIO_EXT) : null;
      readBtn.onclick = ()=>{ state.audioReplays++; readBtn.classList.add("playing");
        strip.querySelectorAll(".sentence-word").forEach(c => c.classList.add("said"));
        play(wholeSrc, ()=>{ readBtn.classList.remove("playing"); readBtn.classList.add("done"); setNavActive(true); }); };
      wrap.appendChild(strip); wrap.appendChild(readBtn);
      host.appendChild(wrap);
      if(d.auto){
        // 16k: AUTONOMOUS tutorial read (3-phase contract) — the sentence reads ITSELF word-by-word,
        // then the whole line, then आगे unlocks. Child watches/listens (no required tap).
        state.ownsAudio = true; state.demoRunning = true; setNavActive(false); readBtn.style.display = "none";   // [24a N8]
        const chips = [...strip.querySelectorAll(".sentence-word")];
        let wi = 0;
        const wStep = ()=>{
          if(CARD.slides[state.idx] !== slide) return;                     // navigated away → abort
          if(wi >= chips.length){ chips.forEach(c => c.classList.add("said")); stopNudge();
            play(wholeSrc, ()=>{ state.demoRunning = false; setNavActive(true); }); return; }
          // read-along: the hand-nudge points at each word AS it is spoken (SME: "hand nudge on words being spoken")
          const c = chips[wi]; c.classList.add("said"); pointNudgeAt(c); const w = (d.words || [])[wi]; wi++;
          play(w && w.audio ? "assets/Audio/" + w.audio + "." + AUDIO_EXT : null, ()=> setTimeout(wStep, 300));
        };
        state.replayAudio = ()=> play(wholeSrc, ()=>{});
        $("navBtn").onclick = ()=> completeSlide(true);                     // explicit — dead-button lesson
        setTimeout(wStep, 450);
        return;
      }
      state.replayAudio = ()=> play(wholeSrc, ()=>{});
      setNavActive(false);
      $("navBtn").onclick = ()=> completeSlide(true);
    }
  },

  SENTENCE_FIND: {
    mount(host, slide){
      const d = slide.data;
      const wrap = document.createElement("div"); wrap.className = "sentence-find";
      if(d.image || d.image_emoji){ const im = document.createElement("div"); im.className = "sentence-img";   // 16k: optional illustration above the line
        im.innerHTML = imgOrEmoji(d.image, d.image_emoji, "s-img", "s-emoji"); wrap.appendChild(im); }
      const strip = document.createElement("div"); strip.className = "sentence-strip";
      state.attempts = 0; state.locked = false; state.scaffoldLevel = 0;
      const maxA = (CARD.scaffold_rules && CARD.scaffold_rules.max_attempts) || 3;
      const chips = [];
      (d.words || []).forEach(w => {
        const chip = document.createElement("div"); chip.className = "sentence-word tappable";
        chip.innerHTML = `<span class="sw-text ink-glyph">${w.text}</span>`;
        chip.__target = (w.target === true);
        const wordSrc = w.audio ? ("assets/Audio/" + w.audio + "." + AUDIO_EXT) : null;
        chip.onclick = ()=>{
          if(state.locked || chip.classList.contains("crossed") || chip.classList.contains("correct")) return;
          const after = (cb)=>{ if(wordSrc) play(wordSrc, cb); else cb(); };
          if(w.target === true){
            state.locked = true; chip.classList.add("correct"); sfxCorrect(); confettiCannon(); setSwMood("happy");
            if(slide.phase === "mastery"){ state.masteryAttempts++; if(state.attempts === 0) state.masteryHits++; }
            GameBus.emit("sentence_word_first_try", { slide_id: slide.id, phase: slide.phase, value: true,
              first_try: state.attempts === 0, attempts: state.attempts + 1, latency_ms: Date.now()-state.slideStart });
            after(()=> setTimeout(()=> completeSlide(true), 700));
          } else {
            /* [28r] same rule as the tap path: RED FIRST, and the lock only from the 2nd wrong.
               This mechanic locked the chip permanently on the FIRST wrong tap, so 27a ("a wrong card
               must not lock on the first miss") and Yasir's "red glow first, then disable" had never
               reached it at all. */
            state.attempts++; chip.classList.add("wrong-flash"); sfxWrongSoft(); setSwMood("tryagain");
            setTimeout(()=>{
              if(chip.classList.contains("correct")) return;   /* [28s] no helpShown guard — see the tap path */
              chip.classList.remove("wrong-flash");
              if(state.attempts >= 2) chip.classList.add("crossed");
            }, 700);
            $("hintBtn").classList.add("show","hint-glow");
            GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
            /* [27j] Three faults fixed here, all reported against HI01H04_L02_S02:
               1. rung 1 played try_again and NEVER looked up hint1, so the authored level-1 hint was
                  dead on every slide;
               2. the `attempts >= 2` rung was unreachable under the house max_attempts:2 because the
                  terminal branch fires first — so `hint` (the rung that NAMES the answer) never played
                  either. It is now spoken AS the terminal line, matching the pick path;
               3. RULE-9 BREACH: terminal help set state.locked, marked the target .correct and called
                  completeSlide(false) — it solved the slide FOR the child. Now it only GLOWS the target
                  and fades the rest; nothing locks and nothing advances until the child taps it,
                  exactly like mountTapOptions' revealAnswer. */
            after(()=>{
              if(state.attempts >= maxA){
                state.scaffoldLevel = 3; state.helpShown = true; setSwMood("hint");
                chips.forEach(c => {
                  if(c.__target){ c.classList.remove("crossed"); c.classList.add("reveal-hold"); }
                  else if(!c.classList.contains("correct")){
                    c.classList.add("faded");
                    c.style.setProperty("pointer-events","none","important");
                  }
                });
                const _tgt = chips.find(c => c.__target);
                if(_tgt) handOnAnswer(_tgt, slide);   /* [28d] hand on the answer, all paths */
                GameBus.emit("answer_revealed", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts, reason: "wrong" });
                play(audioFor(slide, "hint") || audioFor(slide, "reveal") || audioFor(slide, "try_again") || null, ()=>{});
              } else if(state.attempts >= 2){ state.scaffoldLevel = Math.max(state.scaffoldLevel, 2);
                play(midHint(slide), ()=>{}); }               /* [28k] rung 2 */
              else { state.scaffoldLevel = Math.max(state.scaffoldLevel, 1);
                play(audioFor(slide, "hint1") || audioFor(slide, "try_again") || null, ()=>{}); }
            });
          }
        };
        strip.appendChild(chip); chips.push(chip);
      });
      wrap.appendChild(strip); host.appendChild(wrap);
      $("hintBtn").onclick = ()=>{ if(state.locked) return; state.hintUsed = true;
        GameBus.emit("hint_shown", { slide_id: slide.id, manual: true });
        play(audioFor(slide, "hint") || audioFor(slide, "try_again") || null, ()=>{}); };
      $("navBtn").style.display = "none"; setNavActive(false);
      // [21c flag#5] read-along (SME deck P6/P7): speak the sentence word-by-word, glowing each word as it is heard,
      // THEN a hand-nudge points at the TARGET word to guide the tap ("hand nudge की help से बच्चा घर
      // शब्द पहचानेगा"). state.ownsAudio so the entry auto-play chain doesn't ALSO fire the prompt.
      /* [28i] SPEAK THE TARGET WORD, NOT THE WHOLE SENTENCE.
         Yasir 2026-07-28: the slide says "जो शब्द सुनो, उस पर टैप करो।" and the engine then read ALL
         FOUR words aloud — so nothing told the child which one to tap. The task is "tap the word you
         hear"; reading every option destroys it. Target-only is now the DEFAULT and the full
         word-by-word read is opt-in via data.read_along:true.
         NOTE FOR YASIR — this reverses an earlier SME ask: the read-along came from that deck's own
         P6/P7 note (21c flag #5, "hand nudge की help से बच्चा घर शब्द पहचानेगा"). Your ruling wins,
         but the SME will see their request gone, so it is flagged rather than silently dropped. Any
         card that still wants it sets data.read_along:true.
         The target is spoken with NO visual mark: adding .said to it (as the read-along does per word)
         would GLOW the answer before the child has tried, which is the thing we keep removing.
         ALSO REMOVED: the read-along ended in startNudge(slide, _tgt) — a hand planted on the answer
         right after the prompt VO, pre-attempt. 28f deleted the two startNudge(slide,_nudge) forms and
         missed this third one, which is exactly the "hand nudge appears right after VO" complaint. A
         visual hint here is earned only through handOnAnswer() at terminal help. */
      state.ownsAudio = true;
      const _tgt = chips.find(c => c.__target);
      const _clipFor = (i)=>{ const w = (d.words || [])[i];
        return w && w.audio ? "assets/Audio/" + w.audio + "." + AUDIO_EXT : null; };
      const _readAlong = ()=>{                                   // opt-in: data.read_along === true
        let i = 0;
        const step = ()=>{
          if(CARD.slides[state.idx] !== slide || state.locked) return;    // navigated away / already answered
          if(i >= chips.length) return;                                   // NO hand at the end (see above)
          const c = chips[i]; const src = _clipFor(i); i++;
          c.classList.add("said");
          play(src, ()=> setTimeout(step, 220));
        };
        step();
      };
      const _sayTarget = ()=>{
        if(CARD.slides[state.idx] !== slide || state.locked) return;
        play(_clipFor(chips.indexOf(_tgt)), ()=>{});                      // no .said, no nudge
      };
      const _speak = (d.read_along === true) ? _readAlong : _sayTarget;
      state.replayAudio = _speak;                                          // header 🔊 repeats the same thing
      play(audioFor(slide, "prompt") || null, ()=> setTimeout(_speak, 250));   // instruction, then the word to find
    }
  },

  TAP_ALL_WITH_SOUND: {
    mount(host, slide){
      const d = slide.data || {};
      const items = d.items || [];
      const need = items.filter(it => it.has === true).length;
      state.attempts = 0; state.locked = false;
      let found = 0;
      const wrap = document.createElement("div"); wrap.className = "tap-all";
      const head = document.createElement("div"); head.className = "tap-all-head";
      const badge = document.createElement("div"); badge.className = "tap-all-sound"; badge.style.cursor = "pointer";
      badge.innerHTML = `<span class="ink-glyph">${d.target_sound || ""}</span>`;
      badge.onclick = ()=>{ state.audioReplays++; play(audioFor(slide, "target") || null); };
      const counter = document.createElement("div"); counter.className = "tap-all-count";
      const setCount = ()=>{ counter.innerHTML = `<span class="c-found">${found}</span> / ${need}`; };
      head.appendChild(badge); head.appendChild(counter);
      const strip = document.createElement("div"); strip.className = "tap-all-strip";
      const chips = [];
      items.forEach(it => {
        const chip = document.createElement("div"); chip.className = "tap-all-item";
        chip.innerHTML = imgOrEmoji(it.img, it.emoji, "img", "emoji") + `<span class="lbl">${it.word_hi}</span>`;
        const src = it.audio ? ("assets/Audio/" + it.audio + "." + AUDIO_EXT) : null;
        chip.onclick = ()=>{
          if(state.locked || chip.classList.contains("got") || chip.classList.contains("nope")) return;
          const after = (cb)=>{ if(src) play(src, cb); else cb(); };
          if(it.has === true){
            chip.classList.add("got"); sfxCorrect(); found++; setCount();
            GameBus.emit("sound_found", { slide_id: slide.id, phase: slide.phase, word: it.word_hi });
            after(()=>{
              if(found >= need){
                state.locked = true; setSwMood("celebrate"); confettiCannon();
                if(slide.phase === "mastery"){ state.masteryAttempts++; if(state.attempts === 0) state.masteryHits++; }
                GameBus.emit(d.signal_name || "tap_all_correct", { slide_id: slide.id, phase: slide.phase,
                  value: state.attempts === 0, attempts: state.attempts, latency_ms: Date.now()-state.slideStart });
                play(audioFor(slide, "done") || audioFor(slide, "correct") || null,
                  ()=> setTimeout(()=> completeSlide(state.attempts === 0), 700));
              }
            });
          } else {
            /* [28r] same rule as the tap path: RED FIRST, and the lock only from the 2nd wrong.
               This mechanic locked the chip permanently on the FIRST wrong tap, so 27a ("a wrong card
               must not lock on the first miss") and Yasir's "red glow first, then disable" had never
               reached it at all. */
            state.attempts++; chip.classList.add("wrong-flash"); sfxWrongSoft(); setSwMood("tryagain");
            setTimeout(()=>{
              if(chip.classList.contains("correct")) return;   /* [28s] no helpShown guard — see the tap path */
              chip.classList.remove("wrong-flash");
              if(state.attempts >= 2) chip.classList.add("nope");
            }, 700);
            $("hintBtn").classList.add("show","hint-glow");
            GameBus.emit("answer_wrong", { slide_id: slide.id, phase: slide.phase, attempts: state.attempts });
            after(()=> play(wrongClip(slide), ()=>{}));   /* [28i] graded ladder */
          }
        };
        strip.appendChild(chip); chips.push(chip);
      });
      setCount();
      wrap.appendChild(head); wrap.appendChild(strip);
      host.appendChild(wrap);
      $("hintBtn").onclick = ()=>{ if(state.locked) return; state.hintUsed = true;
        GameBus.emit("hint_shown", { slide_id: slide.id, manual: true });
        play(audioFor(slide, "hint") || audioFor(slide, "try_again") || null, ()=>{}); };
      $("navBtn").style.display = "none"; setNavActive(false);
      state.replayAudio = ()=> play(audioFor(slide, "prompt") || null, ()=>{});
    }
  },

  SENTENCE_SOUND: {
    mount(host, slide){
      const d = slide.data || {};
      const stim = document.createElement("div"); stim.className = "sentence-sound-stim";
      const strip = document.createElement("div"); strip.className = "sentence-strip";
      (d.words || []).forEach(w => {
        const chip = document.createElement("div"); chip.className = "sentence-word";
        chip.innerHTML = `<span class="sw-text ink-glyph">${(typeof w === "string") ? w : w.text}</span>`;
        strip.appendChild(chip);
      });
      const whole = d.whole_audio ? ("assets/Audio/" + d.whole_audio + "." + AUDIO_EXT) : null;
      const spk = document.createElement("button"); spk.className = "read-whole-btn"; spk.innerHTML = "फिर सुनो";   /* [28m] no volume glyph */
      spk.onclick = ()=>{ if(state.demoRunning || isPlaying) return;   // [24a N8] a mid-demo/mid-VO replay would gen-kill the reveal chain (आगे brick)
        state.audioReplays++; strip.querySelectorAll(".sentence-word").forEach(c => c.classList.add("said"));
        play(whole, ()=>{}); };
      stim.appendChild(strip); stim.appendChild(spk);
      if(d.auto){
        // 16k: AUTONOMOUS tutorial demo (test-in-tutorial fix) — play the line, then REVEAL the
        // repeating sound (highlight the correct sound chip); no child pick. Then explain + आगे.
        state.ownsAudio = true; state.demoRunning = true; setNavActive(false);   // [24a N8]
        const qrow = document.createElement("div"); qrow.className = "q-row"; qrow.appendChild(stim);
        const grid = document.createElement("div"); grid.className = "opt-grid cols-" + ((d.options || []).length || 3);
        const cells = (d.options || []).map(opt => { const c = letterCell(opt.letter); c.classList.add("opt-cell"); grid.appendChild(c); return { c, opt }; });
        qrow.appendChild(grid); host.appendChild(qrow);
        const chips = [...strip.querySelectorAll(".sentence-word")];
        const reveal = ()=>{
          if(CARD.slides[state.idx] !== slide) return;                      // navigated away → abort
          chips.forEach(c => c.classList.add("said"));
          const t = cells.find(x => x.opt.letter === d.target_sound);
          if(t){ t.c.classList.add("correct", "reveal-pulse"); cells.forEach(x => { if(x !== t) x.c.classList.add("faded"); }); }
          GameBus.emit("sentence_sound_demo", { slide_id: slide.id, phase: slide.phase, sound: d.target_sound });
          setTimeout(()=> play(audioFor(slide, "explain") || audioFor(slide, "conclude") || null, ()=>{ state.demoRunning = false; setNavActive(true); }), 300);
        };
        state.replayAudio = ()=> play(whole, ()=>{});
        $("navBtn").onclick = ()=> completeSlide(true);                     // explicit — dead-button lesson
        play(whole, ()=> setTimeout(reveal, 400));
        return;
      }
      mountTapOptions({
        slide, host, signalName: d.signal_name || "sentence_sound_first_try",
        stimulus: stim, columnsHint: (d.options || []).length,
        options: d.options,
        isCorrect: (opt)=> opt.letter === d.target_sound,
        optionRenderer: (opt)=> letterCell(opt.letter),
        mastery: slide.phase === "mastery",
        nudgeTarget: null
      });
      state.replayAudio = ()=> play(whole, ()=>{});
    }
  },

  /* 16j NEW: sentence -> pick the matching picture (HI01H06 "वाक्य के लिए सही चित्र चुनो"). Sentence
     chips as the stimulus + 2 picture options via the tap-to-answer contract. */
  SENTENCE_PICK_PIC: {
    mount(host, slide){
      const d = slide.data || {};
      const stim = document.createElement("div"); stim.className = "sentence-sound-stim";
      const strip = document.createElement("div"); strip.className = "sentence-strip";
      (d.sentence_words || []).forEach(w => {
        const chip = document.createElement("div"); chip.className = "sentence-word";
        chip.innerHTML = `<span class="sw-text ink-glyph">${(typeof w === "string") ? w : w.text}</span>`;
        strip.appendChild(chip);
      });
      const whole = d.whole_audio ? ("assets/Audio/" + d.whole_audio + "." + AUDIO_EXT) : null;
      stim.appendChild(strip);
      if(whole){ const spk = document.createElement("button"); spk.className = "read-whole-btn"; spk.innerHTML = "फिर सुनो";   /* [28m] no volume glyph */
        spk.onclick = ()=>{ state.audioReplays++; strip.querySelectorAll(".sentence-word").forEach(c => c.classList.add("said")); play(whole, ()=>{}); };
        stim.appendChild(spk); }
      mountTapOptions({
        slide, host, signalName: d.signal_name || "sentence_pick_pic_first_try",
        stimulus: stim, columnsHint: (d.options || []).length,
        options: d.options,
        isCorrect: (opt)=> opt.correct === true,
        optionRenderer: (opt)=> pictureCell(opt.word_hi || "", opt.emoji, opt.img),
        mastery: slide.phase === "mastery",
        nudgeTarget: null
      });
      state.replayAudio = ()=> play(whole, ()=>{});
    }
  }
};

/* VACHAN (एकवचन/बहुवचन) + any 2-category attribute reuse the GENERIC gender modules — identical
   mechanic, just different labels. A vachan game authors these types with the category in the
   "gender" field (e.g. "S"/"P"), the two labels, and (for pairs) f=singular / m=plural; it then
   inherits immediate tap-to-answer feedback, speak-word-on-tap, layered hints, and the engine
   guard for free. Named *_VACHAN (not *_NUMBER) to avoid colliding with MEET_NUMBER = counting. */
SlideModules.VACHAN_INTRO          = SlideModules.GENDER_INTRO;
SlideModules.MEET_VACHAN           = SlideModules.MEET_GENDER;
SlideModules.TAP_VACHAN            = SlideModules.TAP_GENDER;
SlideModules.TAP_PICTURE_BY_VACHAN = SlideModules.TAP_PICTURE_BY_GENDER;
SlideModules.SORT_VACHAN           = SlideModules.SORT_GENDER;
SlideModules.MATCH_VACHAN_PAIRS    = SlideModules.MATCH_GENDER_PAIRS;

SlideModules.VACHAN_INTRO          = SlideModules.GENDER_INTRO;
SlideModules.MEET_VACHAN           = SlideModules.MEET_GENDER;
SlideModules.COMPARE_VACHAN        = SlideModules.COMPARE_VACHAN;   // deck 'शब्दों की तुलना'
SlideModules.TAP_VACHAN            = SlideModules.TAP_GENDER;
SlideModules.TAP_PICTURE_BY_VACHAN = SlideModules.TAP_PICTURE_BY_GENDER;
SlideModules.SORT_VACHAN           = SlideModules.SORT_GENDER;
SlideModules.MATCH_VACHAN_PAIRS    = SlideModules.MATCH_THE_PAIR;   // rebuilt as the tap-to-pair bubble game
SlideModules.MATCH_PAIRS           = SlideModules.MATCH_THE_PAIR;
SlideModules.SORT_WORDS            = SlideModules.SORT_QTYPE;   // [reskin] generic two-box word sort (custom data.bins), r4n
SlideModules.PUNCT_PICK            = SlideModules.PUNCT_DEMO;   // [pick-fig] G1: the run-on demo's page with the tap left to the child

/* ---------- 13. CONTROLLER ---------- */
/* FLN toolkit retune: fewer particles, lower launch speed and a much longer,
   softer decay. The same renderer is shared by in-lesson and end celebrations. */
function starBurstEffect(host, finaleOnly){
  /* Toolkit star burst is reserved for the ending screen. In-lesson burstStars()
     still routes here without the finale flag and therefore stays unchanged. */
  if(!finaleOnly) return;
  if(!host || document.documentElement.classList.contains("no-anim")) return;
  host.querySelectorAll("canvas.fx-starburst").forEach(c=>c.remove());
  const W=host.clientWidth||1333,H=host.clientHeight||750;
  const cv=document.createElement("canvas"); cv.className="fx-starburst"; cv.width=W; cv.height=H;
  cv.style.cssText="position:absolute;inset:0;width:100%;height:100%;z-index:65;pointer-events:none;";
  host.insertBefore(cv,host.firstChild);
  const ctx=cv.getContext("2d"),parts=[],k=W/1333;
  const COLORS=["#FFE400","#FFBD00","#E89400","#FFCA6C","#FDFFB8"];
  const opts={stars:32,circles:8,startV:14,decay:.975,ticks:150,shots:[0,220,440],spin:.18,starScale:1.8,circleScale:1};
  function starPath(r){
    ctx.beginPath();
    for(let i=0;i<10;i++){
      const rad = (i % 2 === 0) ? r : r/2;
      const a = Math.PI/5*i - Math.PI/2;
      ctx[i === 0 ? "moveTo" : "lineTo"](Math.cos(a)*rad, Math.sin(a)*rad);
    }
    ctx.closePath();
  }
  function add(n,scalar,shape){
      for(let i=0;i<n;i++){
        const a = Math.random()*Math.PI*2;
        parts.push({x:W/2,y:H*.52,ax:Math.cos(a),ay:Math.sin(a),
          vel:opts.startV*k*(.5+Math.random()),tick:0,scalar:scalar*k,shape,
          color:COLORS[Math.floor(Math.random()*COLORS.length)],
          rot:Math.random()*Math.PI*2,spin:(Math.random()-.5)*opts.spin});
      }
  }
  function shoot(){add(opts.stars,opts.starScale,"star");add(opts.circles,opts.circleScale,"circle");}
  opts.shots.forEach(ms=>ms?setTimeout(shoot,ms):shoot());
  const minFrames=Math.max(...opts.shots)/16+20; let frames=0;
  (function frame(){
    ctx.clearRect(0,0,W,H); let alive=false;
    for(const p of parts){
      if(p.tick>=opts.ticks)continue; alive=true;
      p.x+=p.ax*p.vel;p.y+=p.ay*p.vel;p.vel*=opts.decay;p.rot+=p.spin;p.tick++;
      ctx.globalAlpha=1-p.tick/opts.ticks;ctx.fillStyle=p.color;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot);
      if(p.shape === "star"){ starPath(8*p.scalar); ctx.fill(); }
      else { ctx.beginPath(); ctx.arc(0, 0, 6*p.scalar, 0, Math.PI*2); ctx.fill(); }
      ctx.restore();
    }
    frames++; if(alive||frames<minFrames)requestAnimationFrame(frame);
    else setTimeout(()=> cv.remove(), 300);
  })();
}
function starBurst(){ starBurstEffect($("confetti"), true); }
function clearHost(){
  if(typeof oceanCleanup!=="undefined" && oceanCleanup){oceanCleanup();oceanCleanup=null;}
  document.body.classList.remove("is-end");   // r4: clear immersive end state when leaving celebration
  /* [28g] "going back from last screen gets swiftie stuck" — clearHost dropped body.is-end but never
     took .show off #endScreen, so the celebration layer (big cheering Swiftie + "बहुत बढ़िया!") stayed
     ON TOP of whatever slide you landed on, covering the middle option card.
     I found this myself earlier tonight and mis-triaged it as low severity — "a child can never go back
     from celebration" — forgetting that REVIEW uses the dev nav, so it hits every review pass. It also
     produced 60 phantom overlap findings in my own audit sweep before I understood it.
     Tear the layer down here, where every slide mount already passes.
     Scoped to the END SCREEN only, on purpose: I first also cleared stage.blurred/gating and the
     phase gate here, but mountSlide runs INSIDE the gate's callback, so that would have un-blurred
     the gray gate mid-flight — breaking the transition built two bumps ago to fix a different report. */
  const _es = $("endScreen");
  if(_es) _es.classList.remove("show", "hint-glow");
  $("slideHost").innerHTML = "";
  state.navVoEligible = false;
  $("hintBtn").classList.remove("show");
  $("hintBtn").disabled = false;
  setNavActive(false);
  stopNudge();
  resetIdleVo();   // [27b] no idle-replay timer survives into the next slide; [27f] and the next
                   // slide gets its own single reminder (teardown is the one place the fired flag clears)
  stopAudio();
}

function mountSlide(idx){
  const titleVideo = $("sgBgVideo");
  if(titleVideo){ titleVideo.pause(); titleVideo.currentTime = 0; }
  state.idx = idx;
  state.slideStart = Date.now();
  state.attempts = 0; state.selectedKey = null; state.locked = false;
  state.hintUsed = false; state.nudgeUsed = false; state.scaffoldLevel = 0; state.hintActive = false; state.helpShown = false;
  state.audioReplays = 0; state.gateNavUntilAudio = false; state.endBtnPending = false;
  state.replayAudio = null;   // a module may set a slide-specific replay (e.g. teach slides whose
                              // audio roles aren't in the autoPlayChain order); else the chip replays the chain
  state.ownsAudio = false;    // a module that drives its OWN audio sequence sets this → skip autoPlayChain
                              // (else the auto prompt-chain stomps/truncates the module's timed VO)
  state.revealing = false;    // [24a N8] true while a reveal_seq/sortSeqReveal is mid-flight (blocks replay + drag)
  state.demoRunning = false;  // [24a N8] true while a self-driving teach chain runs (blocks the replay chips)
  const slide = CARD.slides[idx];
  clearHost();

  // header prompt
  $("promptText").textContent = slide.prompt_hi || "";

  // Hint button stays HIDDEN until the learner makes a wrong attempt, then it is
  // exposed (graduated scaffold). Mastery uses the SAME scaffold — not excluded.
  $("hintBtn").classList.remove("show");
  $("hintBtn").style.display = "";
  $("navBtn").style.display = "";        // restored by default; tap-to-answer slides hide it themselves
  // [16i] DEFAULT nav wiring — a module that enables आगे without overriding onclick still advances.
  // (DEMO_COUNT shipped an enabled-but-dead button; auto-INTRO inherited an unfulfillable tap guard.)
  $("navBtn").onclick = ()=> completeSlide(true);
  setSwMood("point");                    // Swiftie turns to present each new slide

  GameBus.emit("slide_entered", { slide_id: slide.id, phase: slide.phase, eis: slide.eis, type: slide.type, idx });
  /* [spec] passive screens (STORY_SCENE, INTRO, MEET screens, celebration) report screen_viewed;
     answerable ones report question_started instead. Both carry the same per-question context, so a
     host can pair a question_started with its later question_answered on question_id. */
  const _isAnswerable = ANSWERABLE_TYPES.has(slide.type);
  GameBus.xapiForSlide(_isAnswerable ? "question_started" : "screen_viewed", slide,
    { type: _isAnswerable ? "question" : "screen", id: slide.id }, null);

  // audio chip = replay the slide audio. Prefer a module-supplied replay (teach slides own their
  // count_intro/explain sequence, which autoPlayChain deliberately skips), else replay the chain.
  // [24a N7b] navUnlock is defined ONCE so BOTH the mount chain AND every replay re-apply it —
  // otherwise a replay's stopAudio() (echo guard) gen-kills the mount chain's onDone and आगे stays
  // stuck disabled forever (the फिर-सुनो-mid-VO brick on gated teach slides). Also releases a
  // pending celebration end-button for the same reason.
  const navUnlock = ()=>{
    if(state.gateNavUntilAudio) setNavActive(true);
    if(state.endBtnPending){ $("endBtn").classList.add("show","hint-glow"); state.endBtnPending = false; }
  };
  // [24a N8] replay chips ignore taps: while a VO is SOUNDING (a replay can no longer orphan a
  // mid-clip onDone → the "unlock rides the last clip's onEnd" modules can't be bricked); while a
  // reveal_seq/sort reveal runs (no stomping the one-by-one narration); while a self-driving demo
  // chain runs (a replay would gen-kill its chain); and on self-driving slides that offer no replay.
  const replaySlideAudio = ()=>{
    if(isPlaying || state.revealing || state.demoRunning || (state.ownsAudio && !state.replayAudio)) return;
    state.audioReplays++;
    GameBus.emit("audio_replay", { slide_id: slide.id, phase: slide.phase, count: state.audioReplays });
    GameBus.xapiForSlide("audio_replayed", slide, { type: "audio", id: "header_chip" }, null);   // [spec]
    if(state.replayAudio){ state.replayAudio(); navUnlock(); } else autoPlayChain(slide, navUnlock);
  };
  $("audioChip").onclick = replaySlideAudio;

  // mount the type
  const mod = SlideModules[slide.type];
  if(!mod){ console.error("[engine] no module for", slide.type); return; }
  // [engine JS] r4/F1 TEACHING FRAME: tutorial slides mount inside a grid-paper .tut-card (header hidden,
  // prompt in-card, standing Swiftie bottom-left + shoulder audio chip). Type-agnostic — any tutorial-phase
  // module renders into the card. Non-tutorial slides mount bare into slideHost as before.
  const isTut = ((slide.phase === "tutorial" || slide.type === "PUNCT_PICK") && slide.type !== "PHASE_TRANSITION" && slide.type !== "CELEBRATION");
  $("stage").classList.toggle("tut", isTut);
  document.body.classList.toggle("tut-page", isTut);
  let mountHost = $("slideHost");
  if(isTut){
    const card = document.createElement("div"); card.className = "tut-card";
    card.innerHTML = `<div class="tut-prompt">${slide.prompt_hi || ""}</div>` +
      `<img class="tut-mascot" src="assets/UI/start_mascot.webp" alt="" onerror="this.style.display='none'">` +
      `<span class="tut-audio" role="button" aria-label="फिर से सुनो"><svg viewBox="0 0 62 60" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Audio"><g filter="url(#tutChipShadow)"><rect x="8" y="4" width="46" height="44" rx="22" fill="url(#tutChipGrad)"/><rect x="6" y="2" width="50" height="48" rx="24" stroke="white" stroke-width="4"/><path d="M29.8466 19.0574C29.8804 19.0524 29.9145 19.0496 29.9487 19.0488C30.6094 19.0317 31.0021 19.5124 31.0015 20.1414C31.0008 20.9661 31.0003 21.7911 31.0005 22.6158L31.001 27.7212L31.0009 30.5591C31.0009 31.0364 31.0122 31.5472 30.9863 32.0228C30.9662 32.2709 30.902 32.4608 30.7251 32.643C30.3831 32.9952 29.8337 33.0842 29.4386 32.7671C29.0784 32.4781 28.7473 32.1159 28.4181 31.7862L26.4414 29.8087C26.1771 29.5426 25.9071 29.2636 25.6339 29.0081C25.0227 28.9649 24.3645 29.017 23.7487 28.9979C23.445 28.9885 23.1625 29.0211 22.8589 28.9606C22.3751 28.8616 22.0618 28.4823 22.0642 27.9824C22.0706 26.5937 22.0287 25.1949 22.0828 23.8081C22.0884 23.6626 22.2302 23.4334 22.3309 23.3252C22.454 23.1907 22.6146 23.0963 22.792 23.0543C23.0567 22.9904 23.5328 23.016 23.8224 23.0128C24.4143 23.0063 25.0171 23.0277 25.609 23.0073C25.6794 22.9529 25.8505 22.7743 25.919 22.706L26.5305 22.0945L28.5396 20.0838C28.9157 19.7059 29.3217 19.1749 29.8466 19.0574Z" fill="white"/><path class="wv wv2" d="M36.2367 18.6905C36.8783 18.6449 37.3041 19.231 37.6725 19.6829C38.7675 21.0046 39.4982 22.5894 39.7923 24.2804C40.2503 26.8763 39.6548 29.5478 38.1378 31.7035C37.8393 32.1274 37.508 32.5324 37.149 32.9063C36.9404 33.1236 36.7646 33.2558 36.4622 33.3081C36.2013 33.3412 35.9378 33.2717 35.7272 33.1144C35.5185 32.9615 35.3816 32.7298 35.3483 32.4733C35.2786 31.9235 35.5696 31.6821 35.8914 31.3297C36.0448 31.1639 36.1901 30.9908 36.3269 30.811C38.3669 28.136 38.4986 24.4654 36.6555 21.6511C36.4826 21.3899 36.2966 21.1376 36.0984 20.8951C35.8252 20.5652 35.3947 20.2691 35.3472 19.8184C35.2845 19.2225 35.6439 18.768 36.2367 18.6905Z" fill="white"/><path class="wv wv1" d="M33.3868 21.5044C33.9769 21.4549 34.2563 21.7845 34.5981 22.1981C35.1982 22.924 35.6149 23.7691 35.8211 24.6886C36.171 26.2384 35.8867 27.8637 35.0314 29.2026C34.7421 29.6568 34.2333 30.3745 33.6937 30.4946C33.1633 30.5437 32.6759 30.2927 32.5495 29.7376C32.3921 29.0462 32.9849 28.6956 33.3274 28.1763C34.2088 26.833 34.1932 25.0908 33.288 23.7635C33.0747 23.4522 32.6159 23.0564 32.5518 22.7133C32.4377 22.1027 32.7745 21.619 33.3868 21.5044Z" fill="white"/></g><defs><filter id="tutChipShadow" x="0" y="0" width="62" height="60" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/><feOffset dy="4"/><feGaussianBlur stdDeviation="2"/><feComposite in2="hardAlpha" operator="out"/><feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0"/><feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow"/><feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow" result="shape"/></filter><linearGradient id="tutChipGrad" x1="8" y1="26" x2="54" y2="26" gradientUnits="userSpaceOnUse"><stop stop-color="#1987FC"/><stop offset="1" stop-color="#1565F4"/></linearGradient></defs></svg></span>`;
    const inner = document.createElement("div"); inner.className = "tut-content";
    card.insertBefore(inner, card.querySelector(".tut-mascot"));
    card.querySelector(".tut-audio").onclick = replaySlideAudio;   // [24a N7b/N8] same guard + navUnlock as the header chip
    syncSpeakerDisabled(card); // tutorial replay control may be created after its opening VO has begun
    $("slideHost").appendChild(card);
    mountHost = inner;
  }
  mod.mount(mountHost, slide);
  // game-feel: animate the slide content in on every mount
  { const _sh = $("slideHost"); _sh.classList.remove("slide-in"); void _sh.offsetWidth; _sh.classList.add("slide-in"); }

  // fit-to-box + vertically ink-centre every Devanagari glyph. SYNC pass first so tiles are
  // correct immediately even when rAF is throttled (background / non-painting tab) or a module
  // built its tiles synchronously at mount; rAF second pass re-fits after slide-in layout +
  // font-load settle. (16n: the lone rAF pass could skip drag-tile / stimulus glyphs — Yasir #6.)
  centerAllGlyphs($("slideHost"));
  requestAnimationFrame(()=>{ centerAllGlyphs($("slideHost")); refreshMatraWords($("slideHost")); });

  // play the full VO chain automatically (prompt → phoneme/word_name → instruction).
  // If the slide gated its nav button on audio, enable it once the chain finishes
  // (so students can't skip before hearing it). SKIP when the module owns its audio
  // (state.ownsAudio) — else this chain stomps/truncates the module's own timed VO.
  if(!state.ownsAudio){
    autoPlayChain(slide, navUnlock);   // [24a N7b] same unlock the replay chips re-apply
  }
  armIdleVo();   // [27b] start the 7s silent-inactivity watch (all four TEST phases; no-op elsewhere)
                 // [27f] fires at most ONCE per slide
}

/* ---------- [engine JS] r4/P1 PHASE-TRANSITION PEEK GATE (Shruti's peek beat) ----------
   An automatic interstitial fired ON A PHASE BOUNDARY (not a slide type): blur the stage, Swiftie
   peeks up from the bottom under a big headline, hold ≥2s, then mount the next slide. Kept ALONGSIDE
   our journey-map PHASE_TRANSITION module (a distinct, author-placed slide type) — the gate below
   skips PHASE_TRANSITION + CELEBRATION so the two never double-fire. */
function afterConfetti(fn){
  // let a correct-answer confetti burst (.conf-shot) finish falling before we move on; 8s hard cap.
  const started = Date.now();
  (function check(){
    if(!document.querySelector(".conf-shot") || Date.now() - started > 8000){ fn(); return; }
    setTimeout(check, 200);
  })();
}
/* onscreen headline per gate (display only; distinct from any narration). Eligibility = phase IN this map. */
/* [27j] THERE ARE THREE ROUNDS, NOT FOUR (Yasir 2026-07-28).
   Round 3 is called `practice` in some cards and `independent` in others — the SAME round under two
   names — so `independent` is an ALIAS of practice and takes the identical headline. The earlier bug
   was that a card naming round 3 `independent` got NO round-3 gate at all (the gate is conditional on
   PHASE_GATE_TITLE[next.phase] existing); the fix is the alias, NOT a fourth gate. My first attempt
   added `independent` with its own wording plus a `mastery` gate — both wrong: distinct wording would
   make one round look like two, and there is no round 4.
   `mastery` is deliberately ABSENT: mastery slides continue round 3 without a transition. That also
   means vo_pt_mastery is never played, so a card shipping it carries dead audio — verify_bundle's
   "silent gates: [vo_pt_mastery]" warn is a CHECKER ARTIFACT, not a defect.
   VO ids stay optional: play() treats a missing clip as a silent beat and the 2s peek still holds. */
const PHASE_GATE_TITLE = { tutorial:"चलिए, शुरू करें!", guided:"चलिए, साथ में करें!",
                           practice:"अब आपकी बारी!", independent:"अब आपकी बारी!" };   // [16h] the lead’s official transition lines (VO = full sentences in the card manifest; NOTE aap-register — flagged)
const PHASE_GATE_VO    = { tutorial:"vo_pt_tutorial", guided:"vo_pt_guided",
                           practice:"vo_pt_practice", independent:"vo_pt_independent" };
/* Timed from the approved animated WebP itself: Swiftie finishes the silent peek and begins
   opening her mouth at ~4.2s. Transition VO must begin there, not when the image first loads. */
const PHASE_GATE_MOUTH_DELAY_MS = 4200;
/* [28h] which ROUND each phase belongs to — the dedup key for gates. practice === independent === the
   one round 3; `mastery` is absent on purpose (it continues round 3), and so is any future phase name,
   which fails safe to "no gate" rather than to a spurious extra one. */
const PHASE_ROUND = { tutorial:"tutorial", guided:"guided", practice:"round3", independent:"round3" };
const _gatedPhases = new Set();   // each ROUND gate plays ONCE (Start→tutorial, →guided, →round 3)
let _gateToken = 0;
function phaseBlurTransition(cb, toPhase){
  const tok = ++_gateToken;
  stopNudge(); stopAudio();
  const gate = $("phaseGate"), img = $("phaseGateImg");
  let titleSyncTimer = 0;
  const revealGateTitle = ()=>{
    if(titleSyncTimer){ clearInterval(titleSyncTimer); titleSyncTimer=0; }
    if(tok === _gateToken) gate.classList.add("text-speaking");
  };
  if(img){
    /* Do not reveal a cached final frame. Wait for a fresh animated WebP load, then restart
       both the artwork and the CSS entrance so every phase gate shows the full animation. */
    img.style.visibility = "hidden";
    img.onload = ()=>{
      if(tok !== _gateToken) return;
      img.style.animation = "none"; void img.offsetWidth; img.style.animation = "";
      img.style.visibility = "visible";
      /* Start the transition VO only when the refreshed animated artwork is ready. This keeps
         Swiftie's first visible movement and the first spoken syllable on the same frame. */
      requestAnimationFrame(beginSyncedPlayback);
    };
    img.onerror = ()=>{ if(tok === _gateToken){ img.style.visibility = "visible"; beginSyncedPlayback(); } };
    img.src = "assets/UI/peeking.webp?r=" + Date.now();
  }
  gate.classList.remove("text-speaking");
  const title = $("phaseGateTitle"); if(title) title.textContent = PHASE_GATE_TITLE[toPhase] || "";
  $("stage").classList.add("blurred", "gating");
  document.body.classList.add("gating");
  gate.classList.add("show","hint-glow");
  GameBus.emit("phase_transition", { to: toPhase });
  const closeGate = ()=>{ gate.classList.remove("show", "hint-glow", "text-speaking"); $("stage").classList.remove("blurred", "gating"); document.body.classList.remove("gating"); };
  // VO only if the card actually ships it; else a silent beat — the 2s min-hold keeps the peek visible.
  const voId = PHASE_GATE_VO[toPhase];
  const voSrc = voId ? ("assets/Audio/" + voId + "." + AUDIO_EXT) : null;   // [20a] use AUDIO_EXT path so generated clips resolve (was: assets.audio .mp3 map -> silent)
  let openedAt = 0, mediaStarted = false;
  let settling = false, closed = false;
  const finishGate = ()=>{
    if(settling || closed) return;
    settling = true;
    if(titleSyncTimer){ clearInterval(titleSyncTimer); titleSyncTimer=0; }
    if(tok !== _gateToken){ closeGate(); return; }               // a newer gate superseded us
    const hold = Math.max(250, 2800 - (Date.now() - openedAt));  // show the complete entrance + animated beat
    setTimeout(()=>{
      if(closed) return;
      closed = true;
      if(tok !== _gateToken){ closeGate(); return; }
      gate.classList.remove("show", "hint-glow");
      gate.classList.remove("text-speaking");
      $("stage").classList.remove("blurred");
      if(cb) cb();                              // mounts the next slide
      $("stage").classList.remove("gating");    // header returns once the slide is in
      document.body.classList.remove("gating");
    }, hold);
  };
  function beginSyncedPlayback(){
    if(mediaStarted || tok !== _gateToken) return;
    mediaStarted = true;
    openedAt = Date.now();
    setTimeout(()=>{
      if(tok !== _gateToken) return;
      if(toPhase === "tutorial"){
        /* vo_pt_tutorial begins with the instruction; its final phrase is “चलिए, शुरू करें!”.
           Reveal that matching on-screen line at the phrase cue, not during Swiftie's silent peek
           or while she is speaking the preceding sentence. The audio's 4.84s runtime places the
           phrase at about 3.15s; sample the real media clock so delayed playback stays in sync. */
        titleSyncTimer = setInterval(()=>{
          if(tok !== _gateToken || closed){ clearInterval(titleSyncTimer); titleSyncTimer=0; return; }
          const active = currentAudio;
          if(active && active.src && active.src.includes("vo_pt_tutorial") && active.currentTime >= 3.15)
            revealGateTitle();
        }, 50);
      } else revealGateTitle();
      play(voSrc, finishGate);
      /* Some browsers neither reject nor error a missing/undecodable media request. Never let that
         strand the lesson behind the gate: the independent watchdog advances exactly once. */
      setTimeout(finishGate, 6000);
    }, PHASE_GATE_MOUTH_DELAY_MS);
  }
  if(!img) beginSyncedPlayback();
  /* Asset-load fallback only; normally onload above starts the artwork and VO together. */
  setTimeout(beginSyncedPlayback, 1500);
}

function completeSlide(success){
  const slide = CARD.slides[state.idx];
  GameBus.emit("slide_completed", {
    slide_id: slide.id, phase: slide.phase, success: !!success,
    attempts: state.attempts, latency_ms: Date.now()-state.slideStart,
    scaffold_level: state.scaffoldLevel, hint_used: state.hintUsed,
    nudge_used: state.nudgeUsed, audio_replays: state.audioReplays
  });
  if(state.idx >= CARD.slides.length - 1){
    // last slide is CELEBRATION; nothing more
    return;
  }
  // advance only AFTER the correct-answer confetti has landed (to the gate AND to the next slide alike).
  const fromIdx = state.idx, nextIdx = state.idx + 1;
  const next = CARD.slides[nextIdx];
  /* [28h] ONE GATE PER ROUND, NOT PER PHASE NAME.
     `independent` and `practice` are two names for round 3 (Yasir 2026-07-28), so a card that uses
     BOTH crossed two "different phases" and got the identical 'अब आपकी बारी!' gate TWICE, back to
     back — the alias fixed the missing gate and introduced a duplicate one. Deduping by ROUND instead
     of by phase string collapses that pair, and a phase with no round (mastery) still gets no gate,
     which is the ruling: three rounds, no round 4. */
  const nextRound = PHASE_ROUND[next && next.phase], curRound = PHASE_ROUND[slide.phase];
  if(next && nextRound && nextRound !== curRound
     && next.type !== "CELEBRATION" && next.type !== "PHASE_TRANSITION"
     && PHASE_GATE_TITLE[next.phase] && !_gatedPhases.has(nextRound)){
    _gatedPhases.add(nextRound);
    afterConfetti(()=>{ if(state.idx === fromIdx) phaseBlurTransition(()=> mountSlide(nextIdx), next.phase); });
    return;
  }
  afterConfetti(()=>{ if(state.idx === fromIdx) mountSlide(nextIdx); });
}

/* ---------- 14. VALIDATOR (runtime self-check) ---------- */
function runValidator(){
  const missing = (CARD.signals_expected || []).filter(s => !GameBus.firedSet.has(s));
  GameBus.validatorReport.missing_signals = missing;
  GameBus.validatorReport.passed = missing.length === 0;
  console.log("[validator]", GameBus.validatorReport);
  /* [B5] swiftpal:lesson_complete DELIBERATELY DOES NOT FIRE HERE. runValidator() runs at
     CELEBRATION MOUNT, so announcing completion from this point told the host the activity was
     over while the "आगे बढ़ें" CTA was still on screen — the host redirected cueing → formative and
     the CTA was skipped without ever being tapped. The handshake now lives in the CTA's own
     onclick (see the endBtn handler), which is where HI01H05 / MTKGA02 already send it. This
     function stays purely a self-check: report, persist, optional telemetry POST. */
  // offline self-capture: write the final record to localStorage; optionally POST
  // it to a learning-record endpoint if one is configured AND the device is online.
  GameBus.persist();
  if(TELEMETRY.endpoint && navigator.onLine){
    try{ fetch(TELEMETRY.endpoint, {method:"POST", headers:{"Content-Type":"application/json"},
      body: JSON.stringify(GameBus.exportResults()), keepalive:true}).catch(()=>{}); }catch(e){}
  }
  // dev banner
  if(new URLSearchParams(location.search).has("dev")){
    const b = $("devBanner");
    if(missing.length === 0){ b.textContent = "✓ all expected signals fired"; b.className = "dev-banner show ok"; }
    else { b.textContent = "✗ missing signals: " + missing.join(", "); b.className = "dev-banner show"; }
  }
}

/* ---------- [engine JS] r4/#2 DATA-DRIVEN LANDING CONCEPT STRIP ----------
   A landing_hero of kind "concept_strip" renders N visual-example tiles from card data, so any game
   declares its landing preview in card.json instead of hand-editing HTML. Tile types: discs (size),
   bars (length), balance (weight — equal-size objects, heavier lower, never a size cue), image. */
const SG_BALANCE_SVG =
  '<svg viewBox="0 0 124 112" xmlns="http://www.w3.org/2000/svg">' +
  '<line x1="62" y1="30" x2="62" y2="86" stroke="#8AA0C8" stroke-width="6" stroke-linecap="round"/>' +
  '<polygon points="62,60 44,100 80,100" fill="#8AA0C8"/>' +
  '<g transform="rotate(-13 62 34)">' +
  '<rect x="14" y="30" width="96" height="11" rx="5.5" fill="#4EA3F0"/>' +
  '<circle cx="22" cy="20" r="14" fill="#FBD24B" stroke="#D9A21A" stroke-width="2.5"/>' +
  '<circle cx="102" cy="20" r="14" fill="#98A2B3" stroke="#5B6577" stroke-width="2.5"/>' +
  '</g></svg>';
function conceptTileHTML(c){
  const lbl = c && c.label ? ` aria-label="${c.label}"` : "";   // a11y only; not shown (pre-reader → visual+VO)
  switch(c && c.type){
    case "discs": {
      const sizes = c.sizes || [34, 54, 76];
      return `<div class="sg-ex sg-ex-size" role="img"${lbl}>` +
        sizes.map(s => `<span class="sg-disc" style="width:${s}px;height:${s}px"></span>`).join("") + `</div>`;
    }
    case "bars": {
      const widths = c.widths || [42, 72, 102];
      return `<div class="sg-ex sg-ex-len" role="img"${lbl}>` +
        widths.map(w => `<span class="sg-bar" style="width:${w}px"></span>`).join("") + `</div>`;
    }
    case "balance":
      return `<div class="sg-ex sg-ex-wt" role="img"${lbl}>` + SG_BALANCE_SVG + `</div>`;
    case "image":
      return `<div class="sg-ex" role="img"${lbl}><img src="${c.src}" alt="${c.label || ''}"></div>`;
    default:
      return "";
  }
}

/* ---------- 15. BOOT ---------- */
function boot(){
  // god-mode visual theme (opt-in via CARD.theme) — warms the whole stage; scoped CSS under .thm-*
  if(CARD.theme) $("stage").classList.add("thm-" + CARD.theme);
  // banner title = skill name only (strip "(भाग…)" and the ": letters" list)
  $("sgTitle").textContent = (CARD.title.hi || "").split(/[:：(]/)[0].trim();
  // 16j: landing subtitle line (r4 dropped it) + fix the stale document <title> (was hardcoded to
  // the ordering game on every FLN build). Both come from the card now.
  { const _sub = $("sgSub"); if(_sub) _sub.textContent = (CARD.subtitle_hi || ""); }
  /* This lesson's cover is intentionally title-only. Set the Hindi title on a gentle arch and
     remove the old "एक-अनेक" deck label without changing any other landing-screen element. */
  if(CARD.skill_code === "HI02H11_L03_S01"){
    const titleEl=$("sgTitle"), subEl=$("sgSub"), text=titleEl.textContent;
    titleEl.textContent=""; titleEl.classList.add("lesson-title-arc");
    const letters=(typeof Intl!=="undefined" && Intl.Segmenter)
      ? [...new Intl.Segmenter("hi",{granularity:"grapheme"}).segment(text)].map(x=>x.segment)
      : Array.from(text);
    letters.forEach((ch,index,all)=>{
      const span=document.createElement("span");
      span.className="arc-letter"+(ch===" "?" arc-space":""); span.textContent=ch;
      const mid=(all.length-1)/2 || 1, x=(index-mid)/mid;
      span.style.transform=`translateY(${Math.round(x*x*13)}px) rotate(${(x*2.1).toFixed(2)}deg)`;
      titleEl.appendChild(span);
    });
    if(subEl){subEl.textContent="";subEl.style.display="none";}
  }
  try{ document.title = "SwiftPAL · " + (CARD.skill_code || "") + " · " + (CARD.title.hi || "").split(/[:：(]/)[0].trim(); }catch(e){}
  // VISUAL-FIRST landing hero: SHOW the concept (shapes row / a finger-hand / an image), not just the title text
  (function(){ const hero = CARD.landing_hero, el = $("sgHero"); if(!hero || !el) return;
    if(hero.kind === "concept_strip"){
      // r4/#2: each cell is a .sg-acell (keeps the staggered fingerPop pop-in) wrapping a visual example.
      el.innerHTML = (hero.cells || []).map(c => `<div class="sg-acell">${conceptTileHTML(c)}</div>`).join("");
      return;   // keep the landing's tuned title size + spacing (this strip is sized for the full card)
    }
    if(hero.kind === "shapes" && typeof shapeSVG === "function")
      el.innerHTML = (hero.shapes||[]).map(s=> shapeSVG(s.shape, {color:s.color, size:104, rotate:s.rotate||0})).join("");
    else if(hero.kind === "count"){
      // counting game: preview the WHOLE 1..n sequence — a row of hands (1,2,3…), each with its Arabic numeral
      const hi = Math.min(Math.max(parseInt(hero.n,10)||3, 1), 5);   // clamp to available hand art (1..5)
      let cells = "";
      for(let i=1;i<=hi;i++){
        cells += `<div class="sg-hand-cell">${fingerCount(i, "sg-hand")}<span class="sg-hand-num">${devNumeral(i)}</span></div>`;
      }
      el.innerHTML = cells;
    }
    else if(hero.kind === "image") el.innerHTML = `<img src="${hero.src}" alt="">`;
    if(el.innerHTML){ el.classList.add("show","hint-glow"); $("sgTitle").classList.add("compact");
      const c = el.closest && el.closest(".sg-content"); if(c){ c.classList.add("has-hero");
        // SME (S01 review deck): landing reads TITLE first, image BELOW it, image smaller.
        if(hero.title_first) c.classList.add("title-first"); } }
  })();

  // [20a landing] shape-recognition games ship NO landing_hero -> the card fell back to a plain WORD
  // subtitle (unreadable to pre-readers). Derive icon tiles from shape_set instead (labels from the
  // card's own bins; colours are neutral brand tones, never red/green per ruling B5). Additive: only
  // fires when sgHero is still empty AND the card is a shape game.
  (function(){ const el = $("sgHero");
    if(!el || el.innerHTML || typeof shapeSVG !== "function" || !Array.isArray(CARD.shape_set) || !CARD.shape_set.length) return;
    const lab = {}; (CARD.slides||[]).forEach(s => ((s.data && s.data.bins) || []).forEach(b => { if(b.shape && b.label) lab[b.shape] = b.label; }));
    const DEF = { circle:"गोल", square:"चौकोर", triangle:"तिकोना", rectangle:"आयत" };
    const COL = { circle:"#386AF6", square:"#F0A020", triangle:"#9B7BE8", rectangle:"#12A0B8" };
    el.innerHTML = CARD.shape_set.map(sh =>
      `<div class="sg-acell">${shapeSVG(sh, {color: COL[sh] || "#386AF6", size:96})}<span class="sg-alabel">${lab[sh] || DEF[sh] || ""}</span></div>`).join("");
    el.classList.add("show","hint-glow"); $("sgTitle").classList.add("compact");
    const c = el.closest && el.closest(".sg-content"); if(c) c.classList.add("has-hero");   // hides the word subtitle
  })();

  // ----- landing-screen welcome VO (lead review) -----
  // A warm greeting on the title screen. Autoplay is often blocked before a gesture, so we also
  // (a) expose a pulsing 🔊 "listen" button, and (b) fire it on the first pointer-down. The whole
  // greeting lives HERE now (not on slide 0), which also kills the old overlap glitch where the
  // landing VO and slide-0 VO could talk over each other.
  const landSrc = (CARD.assets && CARD.assets.audio && CARD.assets.audio["vo_landing"]) || ("assets/Audio/vo_landing." + AUDIO_EXT);
  /* [h01 local] GREETING + TOPIC, BACK TO BACK (Yasir 2026-07-29). If the card supplies a
     `vo_greeting` clip it plays FIRST, then this game's own vo_landing, as one sequence — and
     because the 🔊 chip calls playLanding(), the chip replays BOTH in order for free.
     The point is re-recording: §3 wants every landing to open with the greeting, and baking it into
     each game's vo_landing would mean re-recording 27 full lines. One shared greeting clip in front
     of each game's EXISTING topic take costs one recording and keeps every current take valid.
     Opt-in: no vo_greeting in the card and this is byte-identical to the old single-clip behaviour.
     The gate is re-checked before the second clip, so a child who taps शुरू करें during the greeting
     does not get the topic line talking over slide 1. */
  const greetSrc = (CARD.assets && CARD.assets.audio && CARD.assets.audio["vo_greeting"]) || null;
  const _onLanding = ()=> !$("startGate").classList.contains("hidden");
  const playLanding = ()=>{
    if(!_onLanding()) return;
    if(greetSrc) play(greetSrc, ()=>{ if(_onLanding()) play(landSrc, ()=>{}); });
    else play(landSrc, ()=>{});
  };
  const sgVo = $("sgVo"); if(sgVo) sgVo.onclick = (e)=>{ e.stopPropagation(); if(isPlaying) return;
    GameBus.xapi("audio_replayed", { type: "audio", id: "landing_chip" }, null);   // [spec] replay chip on the start screen (no slide context yet)
    playLanding(); };
  // ---- [engine JS] r4/P2 boot loader: loader.gif until assets warm, then it dismisses ITSELF into
  // the landing (NO tap gate). DUAL auto-dismiss (window 'load' OR a 2.5s watchdog — never strand the
  // child), deduped by .done. The same handler adds body.loaded (unblocks the concept-strip stagger).
  /* [h01 local] Yasir 2026-07-31: this used to ALSO fire playLanding() here, before any user gesture
     (same defect fixed on HI01H04_L02_S02 the same day). Browsers block unmuted autoplay pre-gesture,
     so that call nearly always failed and fell through play()'s onFail into _ttsSay() — the BROWSER'S
     OS speech voice reading the landing text — i.e. a TTS voice on the landing even with every card
     clip human. Landing playback now starts ONLY from a genuine user gesture: the pointerdown-once
     fallback below (kept, with its [30m] audible-guard) or the 🔊 chip. Gesture-triggered play() is
     reliably allowed by autoplay policy, so the TTS fallback can no longer fire on this screen. */
  (function(){
    const bl = $("bootLoader"); if(!bl){ document.body.classList.add("loaded"); return; }
    // [16l] BRAND SPLASH MIN-HOLD: locally, window.load fires in ~100ms and the CG loader was
    // removed before it ever painted ("no CG logo at the start"). The loader now holds for a
    // minimum beat so the ConveGenius mark is always seen; the watchdog still caps the worst case.
    const T0 = performance.now(), MIN_MS = 1600;
    let fired = false;   // .done is the CSS fade trigger, so it must NOT double as the dedup flag
    const ready = ()=>{
      if(fired) return;   // load event + watchdog both land here → dedup
      fired = true;
      setTimeout(()=>{
        bl.classList.add("done");                  // NOW start the fade (after the brand beat)
        document.body.classList.add("loaded");     // starts the .sg-acell pop chain
        setTimeout(()=> bl.remove(), 450);
        /* [2026-08-04] Speak the greeting AS SOON AS THE DECK IS READY, which is what "it should play
           from the start" means. Safe to try now in a way the old pre-gesture autoplay was not: since
           [30n], play() treats a NotAllowedError as silence and never falls through to the OS TTS
           voice, so a blocked attempt costs nothing and the 🔊 chip / next gesture still starts it.
           Fires after the loader clears so the line is never talking under the splash. */
        setTimeout(playLanding, 500);
      }, Math.max(0, MIN_MS - (performance.now() - T0)));
    };
    if(document.readyState === "complete") ready();
    else window.addEventListener("load", ready);
    setTimeout(ready, 2500);   // watchdog: never strand the child on the loader
  })();
  /* Supplied title video: loop inside the landing card, with its own soundtrack. Browsers may block
     unmuted autoplay; in that case keep the visual looping muted and unlock its audio on the first
     non-Play interaction. Pressing Play stops it before the lesson begins. */
  const titleVideo = $("sgBgVideo");
  if(titleVideo){
    titleVideo.volume = .32;
    const attempt = titleVideo.play();
    if(attempt && attempt.catch) attempt.catch(()=>{
      titleVideo.muted = true;
      const mutedAttempt = titleVideo.play(); if(mutedAttempt && mutedAttempt.catch) mutedAttempt.catch(()=>{});
    });
    window.addEventListener("pointerdown", function unlockTitleVideo(ev){
      if(!document.body.classList.contains("is-start")){
        window.removeEventListener("pointerdown", unlockTitleVideo); return;
      }
      if(ev && ev.target && ev.target.closest && ev.target.closest("#sgBtn,.sg-btn")) return;
      titleVideo.muted = false; titleVideo.volume = .32;
      const resumed = titleVideo.play(); if(resumed && resumed.catch) resumed.catch(()=>{});
      window.removeEventListener("pointerdown", unlockTitleVideo);
    });
  }
  // landing VO best-effort on first interaction too (some browsers block autoplay pre-gesture)
  window.addEventListener("pointerdown", function once(ev){
    /* [2026-08-04] NEVER let शुरू करें be the gesture that starts the greeting. pointerdown fires
       BEFORE click, so a first tap on the start button used to (a) begin vo_landing, which set
       body.vo-lock, and then (b) hit the vo-lock guard in sgBtn.onclick — so the greeting played and
       the button did nothing. The child taps "start" and hears the intro instead of advancing.
       Ignore the start button here and let its own handler run; any other gesture still primes VO. */
    if(ev && ev.target && ev.target.closest && ev.target.closest("#sgBtn,.sg-btn")) return;
    window.removeEventListener("pointerdown", once);
    /* [30m] THE LANDING GREETING MUST NOT RESTART ON THE FIRST TAP (Yasir: "the landing VO does not
       seem fine"). This listener is ONLY an autoplay-policy fallback, but it fired unconditionally, so
       when autoplay HAD worked the first tap anywhere replayed the greeting from the top. Guard on
       whether sound is genuinely moving, NOT on "did we call play()" — on a blocked autoplay we DID
       call it, so a call-flag would kill the very fallback this line exists for. */
    const _a = (typeof currentAudio !== "undefined") ? currentAudio : null;
    const _audible = _a && !_a.paused && !_a.ended && _a.currentTime > 0;
    if(!_audible) playLanding(); });
    /* NOT { once:true } any more: with it, the listener was torn down even on the start-button
       early-return above, so the greeting could never be primed by a later tap. It now removes
       itself explicitly, and only on a gesture it actually acted on. */

  $("sgBtn").onclick = ()=>{
    /* [h01 local] Yasir 2026-07-31: RULING_no_tapping_during_VO applied to the landing screen too —
       शुरू करें must not cut the landing line off mid-sentence (same fix as HI01H04_L02_S02).
       body.vo-lock is already toggled by setPlaying() while any clip plays; this JS guard is
       belt-and-braces alongside the CSS pointer-events:none on .sg-btn (style.css) for the case where
       the SAME gesture that starts the clip also dispatches this click before the lock CSS lands.
       A second tap once the line ends proceeds normally. */
    if(document.body.classList.contains("vo-lock")) return;
    /* [spec] activity_launched — the child tapped शुरू करें. Fired AFTER the vo-lock guard above, so a
       tap that is deliberately ignored (mid-greeting) does not report a launch that never happened. */
    GameBus.xapi("activity_launched", { type: "activity", id: CARD.skill_code }, null,
      { title: (CARD.title && (CARD.title[CARD.medium] || CARD.title.hi)) || null,
        grade: CARD.grade || null, total_slides: CARD.slides.length,
        platform: (window.SwiftPAL && window.SwiftPAL._platform) || "web" });
    stopAudio();          // silence the landing greeting BEFORE slide 0 speaks (no VO overlap)
    sfxPlayButton();      // supplied common play-button SFX
    startBackgroundMusic(); // user gesture unlocks the looping lesson soundtrack
    _ac();                // unlock/resume WebAudio on the start gesture so the first clip never clips
    // [engine JS] r4/P1: peek gate into the tutorial. The landing stays visible-and-BLURRED behind the
    // peeking Swiftie + "चलिए शुरू करें"; it hides once the tutorial mounts (in the callback).
    _gatedPhases.add("tutorial");
    phaseBlurTransition(()=>{
      $("startGate").classList.add("hidden");
      document.body.classList.remove("is-start");   // blue bg only on the title screen
      mountSlide(0);
    }, "tutorial");
  };
  // tapping आगे clears any pending nav-nudge
  $("navBtn").addEventListener("click", ()=>{ sfxNextButton(); clearTimeout(state.navNudgeTimer); stopNudge(); });
  // [engine JS] r4 dev jump: ?slide=N skips the loader+gate and mounts slide N directly (QA/capture only)
  (function(){
    const j = parseInt(new URLSearchParams(location.search).get("slide"), 10);
    if(isNaN(j)) return;
    const bl = $("bootLoader"); if(bl) bl.remove();
    document.body.classList.add("loaded");
    $("startGate").classList.add("hidden");
    document.body.classList.remove("is-start");
    mountSlide(Math.max(0, Math.min(j, CARD.slides.length - 1)));
  })();
  // when the web font finishes loading, re-centre glyphs (metrics change vs fallback)
  if(document.fonts && document.fonts.ready){ document.fonts.ready.then(()=>{ centerAllGlyphs(); refreshMatraWords(); }); }
  // dev banner if ?dev=1 — show empty initially
  if(new URLSearchParams(location.search).has("dev") || new URLSearchParams(location.search).has("nav")){
    if($("devBanner")){ $("devBanner").textContent = "engine ready · slides=" + CARD.slides.length; $("devBanner").className = "dev-banner show"; }
    buildDevNav();
  }
}

/* [engine JS] DEV NAV — a review/QA slide navigator. Shows ONLY with ?dev=1 or ?nav=1 (children never
   see it). Jump to any slide by dropdown, step ◀▶, first/last, or back to the landing. Uses the
   engine's own mountSlide + state.idx; a light poll keeps the label synced when the game self-advances. */
function buildDevNav(){
  if(document.getElementById("devNav")) return;
  const bar = document.createElement("div"); bar.id = "devNav"; bar.className = "dev-nav";
  const mk = (txt, title)=>{ const b = document.createElement("button"); b.className = "dev-nav-btn"; b.textContent = txt; if(title) b.title = title; return b; };
  const land = mk("⌂", "landing"), first = mk("⏮", "first"), prev = mk("◀", "prev"), next = mk("▶", "next"), last = mk("⏭", "last");
  const sel = document.createElement("select"); sel.className = "dev-nav-sel"; sel.title = "jump to slide";
  CARD.slides.forEach((s, i)=>{ const o = document.createElement("option"); o.value = i; o.textContent = (i+1) + ". " + s.id + " · " + s.type; sel.appendChild(o); });
  const lbl = document.createElement("span"); lbl.className = "dev-nav-lbl";
  const cur = ()=> (state && typeof state.idx === "number") ? state.idx : 0;
  const leaveStart = ()=>{ const sg = $("startGate"); if(sg) sg.classList.add("hidden"); document.body.classList.remove("is-start"); document.body.classList.add("loaded"); const bl = $("bootLoader"); if(bl) bl.remove(); };
  const sync = ()=>{ const i = cur(); const s = CARD.slides[i]; if(document.activeElement !== sel) sel.value = i;
    lbl.textContent = (i+1) + "/" + CARD.slides.length + (s ? " · " + s.id : ""); };
  const go = (i)=>{ i = Math.max(0, Math.min(i, CARD.slides.length - 1)); leaveStart(); mountSlide(i); sync(); };
  land.onclick = ()=>{ const sg = $("startGate"); if(sg){ sg.classList.remove("hidden"); document.body.classList.add("is-start"); } };
  first.onclick = ()=> go(0); prev.onclick = ()=> go(cur() - 1); next.onclick = ()=> go(cur() + 1); last.onclick = ()=> go(CARD.slides.length - 1);
  sel.onchange = ()=> go(parseInt(sel.value, 10));
  bar.append(land, first, prev, sel, lbl, next, last);
  document.body.appendChild(bar);
  setInterval(sync, 300); sync();
}
boot();

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



/* ---------- LANDING SKY FIREWORK ----------
   Tap a drifting sky element -> it detonates into a firework of the same shape, with a short
   synthesised pop. The element then returns from the centre on its next lap.
   Hit-tested against each element's rect, so the sky layer stays pointer-events:none and the
   शुरू करें button / audio chip keep every tap they have today. */
(function(){
  var KIND = {s1:"k-star", s2:"k-star", s3:"k-spark", s4:"k-dot", s5:"k-dot"};
  /* bright, child-friendly hues pulled straight from THIS kit's own shape/object colours
     (the reds/blues/greens/yellows/purples used for triangles, balls, stars elsewhere in the
     lesson) — genuinely colourful, but on-brand rather than an invented neon rainbow. The
     softness now comes from the glow rendering below (white core + colour bloom), not from
     muting the hue itself. */
  var HUES = ["#FCB717","#3B7DD8","#21A74A","#E5484D","#7048D6","#F1781D"];
  var actx = null;

  function boom(){                      // short firework pop: thud + bright sparkle tail
    try{
      var AC = window.AudioContext || window.webkitAudioContext; if(!AC) return;
      actx = actx || new AC();
      if(actx.state === "suspended") actx.resume();
      var t = actx.currentTime, out = actx.createGain();
      out.gain.value = 0.22; out.connect(actx.destination);

      var tg = actx.createGain();       // the thud
      tg.gain.setValueAtTime(0.9, t);
      tg.gain.exponentialRampToValueAtTime(0.0001, t + 0.16);
      tg.connect(out);
      var o = actx.createOscillator();
      o.type = "sine";
      o.frequency.setValueAtTime(420, t);
      o.frequency.exponentialRampToValueAtTime(90, t + 0.16);
      o.connect(tg); o.start(t); o.stop(t + 0.18);

      var n = actx.sampleRate * 0.45, buf = actx.createBuffer(1, n, actx.sampleRate), d = buf.getChannelData(0);
      for(var i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 2.6);
      var src = actx.createBufferSource(); src.buffer = buf;
      for(var c = 0; c < 4; c++){                       // tiny after-crackles, like a small firework
        var cg = actx.createGain(), ct = t + 0.10 + Math.random() * 0.30;
        cg.gain.setValueAtTime(0.0001, ct);
        cg.gain.exponentialRampToValueAtTime(0.18, ct + 0.006);
        cg.gain.exponentialRampToValueAtTime(0.0001, ct + 0.07);
        cg.connect(out);
        var co = actx.createOscillator();
        co.type = "square";
        co.frequency.setValueAtTime(1500 + Math.random() * 2200, ct);
        co.connect(cg); co.start(ct); co.stop(ct + 0.08);
      }
      var bp = actx.createBiquadFilter(); bp.type = "bandpass"; bp.frequency.value = 3400; bp.Q.value = 0.8;
      var ng = actx.createGain();
      ng.gain.setValueAtTime(0.0001, t);
      ng.gain.exponentialRampToValueAtTime(0.5, t + 0.03);
      ng.gain.exponentialRampToValueAtTime(0.0001, t + 0.45);
      src.connect(bp); bp.connect(ng); ng.connect(out); src.start(t + 0.02);
    }catch(_){}
  }

  function pop(el, r){
    el.classList.add("popped");
    el.addEventListener("animationiteration", function back(e){        // next lap = respawn
      if(e.animationName !== "sgFly") return;   // ignore sgGlow's much shorter cycle — only the flight lap should un-pop it
      el.classList.remove("popped");
      el.removeEventListener("animationiteration", back);
    });
    var kind = "k-dot";
    el.classList.forEach(function(c){ if(KIND[c]) kind = KIND[c]; });
    var bs = Math.max(11, r.width);
    var b = document.createElement("div");
    b.className = "sg-burst " + kind;
    b.style.left = (r.left + r.width / 2) + "px";
    b.style.top  = (r.top + r.height / 2) + "px";
    b.style.setProperty("--bs", bs + "px");
    b.appendChild(document.createElement("div")).className = "fl";

    var RINGS = [{n:9, rad:3.1, size:.58, dur:.80}, {n:7, rad:1.8, size:.78, dur:.62}];
    var k = 0;
    for(var g = 0; g < RINGS.length; g++){
      var R = RINGS[g], off = Math.random() * Math.PI * 2;
      for(var i = 0; i < R.n; i++, k++){
        var a = off + i / R.n * Math.PI * 2;
        var dist = bs * R.rad * (0.78 + Math.random() * 0.44);
        var p = document.createElement("i");
        p.style.cssText =
          "--ps:" + (bs * R.size * (0.8 + Math.random() * 0.5)).toFixed(1) + "px;" +
          "--dx:" + (Math.cos(a) * dist).toFixed(1) + "px;" +
          "--dy:" + (Math.sin(a) * dist).toFixed(1) + "px;" +
          "--g:" + (dist * 0.42).toFixed(1) + "px;" +
          "--sd:" + (R.dur + Math.random() * 0.22).toFixed(2) + "s;" +
          "--sdl:" + (Math.random() * 0.06).toFixed(3) + "s;" +
          "color:" + HUES[k % HUES.length];
        b.appendChild(p);
      }
    }
    document.body.appendChild(b);
    boom();
    setTimeout(function(){ b.remove(); }, 1200);
  }

  function init(){
    var sky = document.querySelector(".sg-sky");
    if(!sky) return;
    document.addEventListener("pointerdown", function(e){
      if(!document.body.classList.contains("is-start") && !document.body.classList.contains("is-end")) return;
      var els = sky.querySelectorAll("i:not(.popped)");
      for(var i = 0; i < els.length; i++){
        var el = els[i], r = el.getBoundingClientRect();
        if(r.width < 2) continue;
        var pad = Math.max(12, r.width * 0.7);      // small targets need a forgiving hit box
        if(e.clientX < r.left - pad || e.clientX > r.right + pad ||
           e.clientY < r.top - pad  || e.clientY > r.bottom + pad) continue;
        if(parseFloat(getComputedStyle(el).opacity) < 0.08) continue;
        e.stopPropagation(); e.preventDefault();   // claim this tap — .sg-sky is pointer-events:none, so without this it also reaches (and re-fires) whatever real button sits underneath the star, e.g. the VO replay chip
        pop(el, r);
        return;
      }
    }, true);
  }
  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();

