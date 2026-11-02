"""Verify a PUNCT_SCENE page — T2, the hallway scene ([t2-scene] 2026-11-01, FLN-by-MJ frame 706:188 "2 T0B"), or T3, the classroom
scene ([t3-scene] the same day, frame 724:2016 "7 T3") — against its frame and its timing.
usage: python -I -X utf8 scene_check.py <index.html> <render_1280x720.png> <outdir> [T2|T3|T4|G1|G2]     (default T2)
       renders: demo1b_figma_render_1280x720.png (T2), demo2b_figma_render_1280x720.png (T3), demo3b_... (T4), g1b_... (G1), g2b_... (G2)
   [g2-scene] G2 (frame 716:1058 "10 G2") = G1's pick with the frame's own geometry: the street picture drawn whole at -34,-5
   1152.714x550 of the card, the girl with the bag 934,227 236x354 on her ellipse 969,534 145x38, T3's 59x100 white slot at
   791,184, the tiles 334.09 / 561 / 791.82 at 426 with NO ellipses under them, the "?" (the third tile) the answer, the sentence
   clip vo_g2_sent (the recording), the instruction G1's; the same taps and checks as G1.
   [g1-scene] G1 (frame 715:856 "9 G1", type PUNCT_PICK with data.scene) runs the scene as the CHILD's pick: stages 1, 2 and 4 as
   T2's (the intro line vo_g1_intro, the sentence + the white slot, the 7 s blink with the tiles popping in), each tile live from
   the frame it pops in, no explanation / lit tile / pulse; the taps made in the page: the chip during the intro and a tile during
   the sentence's clip (ignored), a wrong tile 0.3 s after all three are live (the wiggle wgNo + the kit's wrong buzz in that frame,
   hint 1 vo_build_hint1 0.5 s after), the right tile 0.2 s after that (ignored: [tap-lock], the buzz sounds), the chip after hint
   1 (the instruction line again — never the sentence: [g1-quiet]), the other wrong tile after it (the wiggle, the buzz, hint 2 vo_build_hint2), the right tile
   after hint 2 (the press dmfTap with its colours kept, the mark in the slot in that frame, the correct sound, the confetti and its
   sound, "शाबाश!" vo_ok at once, G2 1 s after it; the slot's box stays). A second run: three wrong taps -> the pointing hand under
   the right tile, the other two dead and dim, a dead tile's tap nothing, the guided tap: the press, the mark, the confetti, no line,
   G2 1.7 s after.
1. At 1333x750, the page mounted on its own (the engine's AudioContext warmed first, as the start tap would have):
   T2: the intro line (vo_demo1_intro) is the first clip and sounds over the hallway picture alone — the picture, the standing Swiftie
   and the 🔊 chip there from the first frame, the girl in her place (no animation, [t2-scene2]); no sentence word, no slot, no tile
   [t3-look] T3's girl is her bitmap in layers (.dsc-grig: the body, two eyes, the forearm, the braid tip, each masked by a data-URI
   sheet) and, as the FIRST tile pops, .look starts her glance: the forearm up to 11 degrees by ~0.5 s and bobbing, the irises
   2.26 / 1.13 px toward the tiles within 0.3 s, the figure sheared 2 degrees from her feet; everything back at identity by 2.35 s
   and still until the cycle repeats 7 s after its start ([t3-look7]; was 5 s); smooth (no frame-to-frame jump); after the tap the class leaves only in
   a rest phase (every transform identity in that frame); her pixels at rest = the frame's bitmap (the rig paused at 3 s).
   before it has ended; 0.5 s after it the slot pops in and the sentence rises in whole in the same frame, with T1's text pop (the
   reference's sfxPopSoft: _tone 720 sine 0.10 / 0.07) in that frame.
   T3: no intro line — the picture, the frame's girl ([t3-girl]), the Swiftie and the chip alone for data.open_ms (1 s), nothing else; then the speech
   bubble (.dsc-bubble, dscBubbleIn from half its size) pops in with the slot and the rising sentence in the same frame, to the user's
   sharp pop (sfx_demo2_sharp_pop.mp3 at .8) in that frame; the sentence's clip (the recording) is the first clip.
   Then, on both: the sentence's clip 0.45 s after the rise, each word lit as it is read ([word-sync]); T2: 0.3 s after the clip the
   school sound (sfx_demo1_school.mp3 at .5) for data.pic_sfx_ms, full until its last 0.4 s, faded then and paused at its end, the girl
   giving her small pop (dscPop: up to ~1.045 about her feet, back within 0.7 s) in its first frame and standing still before and
   after; T3 ([t3-girl]): no school sound and no pop at all, the girl still (opacity 1, transform none) in every frame; 0.3 s after
   the sound (T3: after the sentence's clip) the slot blinks (data.blink_ms = 7 s in data.blink_cycle_ms = 1.75 s cycles, [t2-scene5]: the WHOLE box, in its
   orange look — the ring the words' orange, the fill the slot's own colour warmed by the orange (#FAE1CC on T2's white, #FAD692 on
   T3's yellow), the glow the pulsing tile's rgba(232,106,0,.6) 5px in every frame from 0.45 s in to the end — APPEARS and
   DISAPPEARS: its opacity 1 -> 0 -> 1 each cycle, four unseen troughs 1.75 s apart, no frame-to-frame jump over .12, fully seen
   between them and at the end; 0.45 s after the blink the box is plain — grey ring, its own fill, no glow — and its pop-in
   (sfigBoxIn) has NOT run again: opacity 1 and transform none through the 0.7 s after) and as the blink starts the three tiles pop in
   ONE BY ONE (data.tiles_gap_ms = 350 ms apart, each dscTileIn: from under .6 of its size past 1.04, at its size within 0.7 s) with
   the pop (sfx_demo1_pop.mp3 at .8) in EACH tile's frame; 0.3 s after the blink the explanation (vo_demo1_explain / the recorded
   vo_demo2_explain) — the right tile (T2 the danda's, the first; T3 the "?", the MIDDLE one) lights (.lit) as the clip reaches its cue
   word (पूर्णविराम / प्रश्नवाचक), not before; 0.3 s after the clip the other two tiles are dim and dead (.off, at .6); 0.3 s later the
   lit tile pulses (dscPulse, infinite; its face a 3px orange border with a glow breathing .6 -> .7, [t2-scene3]) and is live. Taps:
   the 🔊 chip during the first clip is ignored (every clip plays once), the right tile before it is live is ignored, the chip once it
   is live reads the sentence again (words lit, the tile still pulsing), the tap on the pulsing tile: its BORDER green at once (.done:
   the face white, the mark its blue), the kit's correct sound (sfx_correct_new.ogg at .85) in that frame, the mark in the slot (its
   ink centred), the slot's box gone 0.45 s later, the next page (T3 / T4) mounted ~1.2 s after that, no gate. Only those sounds (the
   box's pop, the school, the three pops, the correct) besides the voice clips; आगे never shows.
2. The card, Swiftie, the 🔊 chip = page 3 T1's (stage px: the card 96,106 1088x508 x 1333/1280 with 64px corners; Swiftie 76,472
   190; the chip 202,606 58).
3. 1280x720 (= frame px), the tiles landed and the blink frozen: every box vs the frame's nodes (T2: the picture 0,-113 1088x613 of
   the card, the slot 1013,187 53x90, the tiles 564.09 / 791 / 1021.818 at 397; T3: the picture 0,-4 1088x519, the bubble's SVG
   397.306,160.61 651.745x135.269, the slot 907,174 59x100, the tiles 465.09 / 692 / 922.818 at 453, the girl 213,212 257x385 and her
   shadow 277,558 118x37 ([t3-girl]); T2: the girl 264,215 239x358, her shadow 307,520 160x36; both: the tiles 117.819x116.498 with their faces and shadows); the sentence's and the three marks' ink vs the
   Figma render (centres within 1.5 px, sizes within 2 px: the marks are the frame's own Noto face, 'Story Noto Marks'); the type;
   the slot's interior (T2 white, T3 the frame's #FFF1B6); per-pixel diffs vs the render over the card less Swiftie / chip (T1's, not
   the frame's), the slot (its dashes' phase is not the render's), the text ink bands and the girl; the girl's region compared on its
   own (the frame's bitmap, resampled).
"""
import sys, re, json, pathlib
import numpy as np
from playwright.sync_api import sync_playwright
from PIL import Image

# [t4-scene] T4 = frame 723:1575 (render demo3b_figma_render_1280x720.png): no intro line and no bubble — open_ms, then both slots pop
# in with the rising sentence and T1's text pop; the comma lands in the left slot at the tap and in the right one 0.3 s later, each
# box gone 0.45 s after its comma; 1.2 s after the last the round's gate opens, then G1
html = pathlib.Path(sys.argv[1]).resolve(); target = Image.open(sys.argv[2]).convert("RGB")
out = pathlib.Path(sys.argv[3]).resolve(); out.mkdir(parents=True, exist_ok=True)
PAGE = sys.argv[4] if len(sys.argv) > 4 else "T2"
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail != "" else ""))
    if not ok: fails.append(name)

FS = 1333 / 1280
AS_T0 = {".tut-card.sfig-card": (96 * FS, 106 * FS, 1088 * FS, 508 * FS), ".sfig-swiftie": (76, 472, 190, 190), ".tut-audio": (202, 606, 58, 58)}
CX, CY = 96, 106
TILE = (117.819, 116.498); FACE = (115.743, 110.983)
C = {
  "T2": dict(prefix="demo1", intro=True, open_ms=500, bg="img_demo1_hall", girl="img_demo1_girl_walk", beat=True, GIRL=(264, 215, 503, 573), bubble=None, box_sfx=None, slot=(53, 90),
             sent="पिंकी स्कूल जा रही है", sent_clip="vo_demo1_sent", nwords=5, explain_clip="vo_demo1_explain", cue="पूर्णविराम", opts=["।", ",", "?"], mark="।", pick=0,
             next="T3", next_ok="CARD.slides[state.idx].id === 'T3' && CARD.slides[state.idx].type === 'PUNCT_SCENE' && !!document.querySelector('.tut-card.sfig-round .dsc-bg')", next_what="T3, the classroom scene",
             FRAME={".dsc-bg > img": (CX + 0, CY - 113, 1088, 613), ".dsc-slot": (1013, 187, 53, 90), ".dsc-girl": (264, 215, 239, 358), ".dsc-shade": (307, 520, 160, 36),
                    ".dsc-tile.t1": (564.09, 397) + TILE, ".dsc-tile.t2": (791, 397) + TILE, ".dsc-tile.t3": (1021.818, 397) + TILE,
                    ".t1 .dsc-face": (565.13, 398.38) + FACE, ".t1 .dsc-tshade": (563, 496, 118, 26), ".t3 .dsc-tshade": (1021.818, 496.498, 118, 26)},
             INK={"sentence": (560, 180, 1010, 290), "mark1": (574, 405, 672, 505), "mark2": (801, 405, 899, 505), "mark3": (1032, 405, 1130, 505)},
             BY_DESIGN=[(1008, 182, 1071, 282), (570, 186, 1015, 268), (600, 420, 645, 480), (830, 440, 870, 470), (1055, 418, 1105, 478)],   # the slot, the ink bands
             girl_in_render=True, slot_fill="rgb(255, 255, 255)", blink_fill="rgb(250, 225, 204)",
             slot_in=dict(rgb=(255, 255, 255), row_y=232, xs=(1000, 1080), col_x=1040, ys=(175, 290), want=(1015, 1064, 189, 275)), first_word="पिंकी", look=None),
  "T3": dict(prefix="demo2", intro=False, open_ms=1000, bg="img_demo2_room", girl="img_demo2_girl_ask", beat=False, GIRL=(213, 212, 470, 597), bubble="img_demo2_bubble", box_sfx="sfx_demo2_sharp_pop.mp3", slot=(59, 100),
             sent="तुम्हारा नाम क्या है", sent_clip="vo_demo2_sent", nwords=4, explain_clip="vo_demo2_explain", cue="प्रश्नवाचक", opts=["।", "?", ","], mark="?", pick=1,
             next="T4", next_ok="CARD.slides[state.idx].id === 'T4' && CARD.slides[state.idx].type === 'PUNCT_SCENE' && !!document.querySelector('.tut-card.sfig-round.dsc-v-list .dsc-bg')", next_what="T4, the third scene ([t4-scene])",
             FRAME={".dsc-bg > img": (CX + 0, CY - 4, 1088, 519), ".dsc-bubble": (397.306, 160.61, 651.745, 135.269), ".dsc-slot": (907, 174, 59, 100), ".dsc-girl": (213, 212, 257, 385), ".dsc-shade": (277, 558, 118, 37),
                    ".dsc-tile.t1": (465.09, 453) + TILE, ".dsc-tile.t2": (692, 453) + TILE, ".dsc-tile.t3": (922.818, 453) + TILE,
                    ".t1 .dsc-face": (466.13, 454.38) + FACE, ".t1 .dsc-tshade": (464, 552, 118, 26), ".t3 .dsc-tshade": (922.818, 552.498, 118, 26)},
             INK={"sentence": (470, 172, 900, 280), "mark1": (475, 461, 573, 561), "mark2": (702, 461, 800, 561), "mark3": (933, 461, 1031, 561)},
             BY_DESIGN=[(902, 169, 971, 279), (472, 184, 904, 266), (501, 476, 546, 536), (725, 474, 775, 534), (962, 496, 1002, 526)],   # the slot, the ink bands
             girl_in_render=True, slot_fill="rgb(255, 241, 182)", blink_fill="rgb(250, 214, 146)",
             slot_in=dict(rgb=(255, 241, 182), row_y=224, xs=(895, 980), col_x=936, ys=(165, 285), want=(909, 964, 176, 272)), first_word="तुम्हारा",
             look=dict(every_ms=7000, active_ms=2300, gx=2.26, gy=1.13, arm_deg=11, lean_deg=2)),   # [t3-look]; [t3-look7] every 7 s (was 5 s)
  "T4": dict(prefix="demo3", intro=False, open_ms=1000, bg="img_demo3_park", girl="img_demo3_girl_basket", beat=False, GIRL=(240, 257, 464, 593), bubble=None, box_sfx=None, slot=(37, 42.606),
             sent="मेरे पास आम केला सेब और संतरा है ।", sent_clip="vo_demo3_sent", nwords=9, explain_clip="vo_demo3_explain", cue="अल्पविराम", opts=["।", ",", "?"], mark=",", pick=1,
             next="G1", gate=True, nslots=2, stagger=300,
             next_ok="CARD.slides[state.idx].id === 'G1' && CARD.slides[state.idx].type === 'PUNCT_PICK' && !!document.querySelector('.tut-card.sfig-round.dsc-v-pick .dsc-bg')", next_what="G1 (PUNCT_PICK on the scene module, [g1-scene]), through the round's gate",
             FRAME={".dsc-bg > img": (CX - 102, CY - 124, 1371, 654), ".dsc-slot": (495, 188, 37, 42.606), ".dsc-slot.s2": (645, 188, 37, 42.606), ".dsc-girl": (240, 257, 224, 336), ".dsc-shade": (257, 546, 190, 47),
                    ".dsc-tile.t1": (494.0908, 447) + TILE, ".dsc-tile.t2": (721, 447) + TILE, ".dsc-tile.t3": (951.8184, 447) + TILE,
                    ".t1 .dsc-face": (495.1289, 448.3789) + FACE, ".t1 .dsc-tshade": (493, 546, 118, 26), ".t3 .dsc-tshade": (951.8184, 546.498, 118, 26)},
             INK={"sentence": (200, 140, 1080, 250), "mark1": (505, 455, 603, 555), "mark2": (732, 455, 830, 555), "mark3": (962, 455, 1060, 555)},
             BY_DESIGN=[(490, 183, 688, 236), (220, 150, 1055, 218), (546, 477, 559, 523), (770, 494, 787, 516), (995, 471, 1026, 524)],   # the slots, the ink bands
             girl_in_render=True, slot_fill="rgb(255, 255, 255)", blink_fill="rgb(250, 225, 204)",
             slot_in=[dict(rgb=(255, 255, 255), row_y=209, xs=(485, 545), col_x=524, ys=(178, 242), want=(497, 530, 190, 228)),
                      dict(rgb=(255, 255, 255), row_y=209, xs=(635, 695), col_x=674, ys=(178, 242), want=(647, 680, 190, 228))], first_word="मेरे", look=None),   # the columns where BOTH the render and the page have a dash top and bottom (the dashes' phase differs by design); the render's white there
  # [g1-scene] G1 = frame 715:856 (render g1b_figma_render_1280x720.png): the child's pick on the scene — the room picture drawn whole
  # at -3,-3 1095x514.872 of the card, the girl with the ball 229,163 252x378 on her ellipse 250,501 158x34, the white slot 995,186
  # 53x90, the tiles at T4's columns on T2's row
  "G1": dict(prefix="g1", pick_mode=True, intro=True, intro_clip="vo_g1_intro", open_ms=500, bg="img_g1_room", girl="img_g1_girl_ball2", beat=False, GIRL=(229, 163, 481, 541), bubble=None, box_sfx=None, slot=(53, 90),
             sent="पिंकी गेंद से खेल रही थी", sent_clip="vo_g1_sent", nwords=6, explain_clip=None, cue=None, opts=["।", ",", "?"], mark="।", pick=0,
             wrong=[1, 2], hints=["vo_build_hint1", "vo_build_hint2"], ok_clip="vo_ok",
             next="G2", next_ok="CARD.slides[state.idx].id === 'G2' && CARD.slides[state.idx].type === 'PUNCT_PICK' && !!document.querySelector('.tut-card.sfig-round.dsc-v-pick2 .dsc-bg')", next_what="G2 (the scene pick, [g2-scene])",
             FRAME={".dsc-bg > img": (CX - 3, CY - 3, 1095, 514.872), ".dsc-slot": (995, 186, 53, 90), ".dsc-girl": (229, 163, 252, 378), ".dsc-shade": (250, 501, 158, 34),
                    ".dsc-tile.t1": (494.0908, 397) + TILE, ".dsc-tile.t2": (721, 397) + TILE, ".dsc-tile.t3": (951.8184, 397) + TILE,
                    ".t1 .dsc-face": (495.1289, 398.3789) + FACE, ".t1 .dsc-tshade": (493, 496, 118, 26), ".t3 .dsc-tshade": (951.8184, 496.498, 118, 26)},
             INK={"sentence": (420, 172, 990, 288), "mark1": (505, 405, 603, 505), "mark2": (732, 405, 830, 505), "mark3": (962, 405, 1060, 505)},
             BY_DESIGN=[(990, 181, 1053, 281), (490, 188, 992, 260), (530, 420, 575, 480), (760, 440, 800, 470), (985, 418, 1035, 478)],   # the slot, the ink bands
             girl_in_render=True, slot_fill="rgb(255, 255, 255)", blink_fill="rgb(250, 225, 204)",
             slot_in=dict(rgb=(255, 255, 255), row_y=231, xs=(982, 1062), col_x=1022, ys=(174, 289), want=(997, 1046, 188, 274)), first_word="पिंकी", look=None),
  # [g2-scene] G2 = frame 716:1058 (render g2b_figma_render_1280x720.png): G1's pick, the "?" the answer, the frame's own geometry
  "G2": dict(prefix="g2", pick_mode=True, intro=True, intro_clip="vo_g1_intro", open_ms=500, bg="img_g2_street", girl="img_g2_girl_bag2", beat=False, GIRL=(934, 227, 1170, 581), bubble=None, box_sfx=None, slot=(59, 100),
             sent="तुम कहाँ जा रहे हो", sent_clip="vo_g2_sent", nwords=5, explain_clip=None, cue=None, opts=["।", ",", "?"], mark="?", pick=2,
             wrong=[0, 1], hints=["vo_build_hint1", "vo_build_hint2"], ok_clip="vo_ok", no_tshade=True,
             next="G3", next_ok="CARD.slides[state.idx].id === 'G3' && CARD.slides[state.idx].type === 'PUNCT_PICK' && !!document.querySelector('.tut-card.sfig-full .dmf-band')", next_what="G3 (PUNCT_PICK, the title-bar page)",
             FRAME={".dsc-bg > img": (CX - 34, CY - 5, 1152.714, 550), ".dsc-slot": (791, 184, 59, 100), ".dsc-girl": (934, 227, 236, 354), ".dsc-shade": (969, 534, 145, 38),
                    ".dsc-tile.t1": (334.0898, 426) + TILE, ".dsc-tile.t2": (561, 426) + TILE, ".dsc-tile.t3": (791.8203, 426) + TILE,
                    ".t1 .dsc-face": (335.1289, 427.3789) + FACE},
             INK={"sentence": (340, 175, 789, 285), "mark1": (344, 434, 442, 534), "mark2": (571, 434, 669, 534), "mark3": (802, 434, 900, 534)},
             BY_DESIGN=[(786, 179, 855, 289), (345, 185, 790, 265), (370, 449, 415, 509), (600, 469, 640, 499), (825, 447, 875, 507)],   # the slot, the ink bands
             girl_in_render=True, slot_fill="rgb(255, 255, 255)", blink_fill="rgb(250, 225, 204)",
             slot_in=dict(rgb=(255, 255, 255), row_y=234, xs=(778, 865), col_x=820, ys=(172, 297), want=(793, 848, 186, 282)), first_word="तुम", look=None),
}[PAGE]
NEXT, PICK, FIRST = C["next"], C["pick"], ("intro" if C["intro"] else "sent")
PICKM = bool(C.get("pick_mode")); INTRO_CLIP = C.get("intro_clip", "vo_demo1_intro")   # [g1-scene] the child's pick on the scene
NAMES = {f"{INTRO_CLIP}.ogg": "intro", f"{C['sent_clip']}.ogg": "sent"} | ({f"{C['explain_clip']}.ogg": "explain"} if C.get("explain_clip") else {})   # [g2-scene] the sample's clip names (G2's intro line is G1's clip)
WHOLE = (80, 90, 1200, 640)
OWN_T0 = [(25, 400, 290, 720)]                                   # Swiftie + the chip (T1's, not the frame's)
GIRL = C["GIRL"]
GOTO = """(id) => { const sg = document.getElementById('startGate'); if (sg) sg.classList.add('hidden');
  document.body.classList.remove('is-start'); document.body.classList.add('loaded');
  const bl = document.getElementById('bootLoader'); if (bl) bl.remove(); mountSlide(CARD.slides.findIndex(s => s.id === id)); }"""
BOXES = """(sels) => { const o = {}; for (const s of sels) { const e = document.querySelector(s);
  if (!e) { o[s] = null; continue; } const r = e.getBoundingClientRect(); o[s] = [r.left, r.top, r.width, r.height]; } return o; }"""
NAVLOG = """() => { window._navLog = []; const btn = document.getElementById('navBtn'); let last = ''; const t0 = performance.now();
  const step = () => { const cs = getComputedStyle(btn); const shown = cs.visibility === 'visible' && parseFloat(cs.opacity) > 0.01 && cs.display !== 'none';
    const key = [shown, CARD.slides[state.idx] ? CARD.slides[state.idx].id : null].join('|');
    if (key !== last) { last = key; window._navLog.push({ ms: performance.now() - t0, shown, slide: CARD.slides[state.idx] ? CARD.slides[state.idx].id : null }); }
    requestAnimationFrame(step); }; requestAnimationFrame(step); }"""
SOUNDS = """() => { window._snd = []; const T = window._tone;
  window._tone = function(f, ty, d, v){ window._snd.push({ ms: performance.now(), kind: 'tone', f: f.join('/'), ty, d, v }); return T.apply(this, arguments); };
  const P = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function(){ window._snd.push({ ms: performance.now(), kind: 'media', src: decodeURIComponent(String(this.currentSrc || this.src).split('/').pop()), vol: +this.volume.toFixed(3), slide: (typeof CARD !== 'undefined' && CARD.slides[state.idx]) ? CARD.slides[state.idx].id : null });
    return P.apply(this, arguments); }; }"""
# one frame of the page
SAMPLE = r"""() => { const a = currentAudio, src = a ? a.src.split('/').pop() : '', nm = NAMES, m = src.match(/vo_PREFIX_(\w+)\.ogg/) || src.match(/vo_(\w+)\.ogg/), q = (s) => document.querySelector(s), qa = (s) => document.querySelectorAll(s);
  const g = q('.dsc-girl'), gc = g ? getComputedStyle(g) : null, slot = q('.dsc-slot'), ring = q('.dsc-dash rect'), lit = [...qa('.dsc-tile')].findIndex(t => t.classList.contains('lit')), bub = q('.dsc-bubble');
  const sfx = _kitSfx.scenePic;
  return { ms: performance.now(), slide: CARD.slides[state.idx] ? CARD.slides[state.idx].id : null, clip: nm[src] || (m ? m[1] : null), t: a ? a.currentTime : null, playing: isPlaying,
    ready: !!q('.dsc-bg'), bgLoaded: !!q('.dsc-bg > img') && q('.dsc-bg > img').complete && q('.dsc-bg > img').naturalWidth > 0,
    shown: qa('.dsc-sent .sfig-w.on').length, hot: [...qa('.dsc-sent .sfig-w')].map((w, i) => w.classList.contains('hot') ? i : -1).filter(i => i >= 0), rise: !!q('.dsc-sent.sfig-rise'),
    slotIn: !!slot && slot.classList.contains('in'), blink: !!slot && slot.classList.contains('blink'), glow: slot ? getComputedStyle(slot).boxShadow : null, slotBg: slot ? getComputedStyle(slot).backgroundColor : null, slotOp: slot ? +(+getComputedStyle(slot).opacity).toFixed(3) : null, slotTf: slot ? getComputedStyle(slot).transform : null, ringStroke: ring ? getComputedStyle(ring).stroke : null,
    bubIn: !!bub && bub.classList.contains('in'), bubTf: bub ? getComputedStyle(bub).transform : null, bubOp: bub ? +(+getComputedStyle(bub).opacity).toFixed(3) : null, bubAn: bub ? getComputedStyle(bub).animationName : null,
    gone: !!slot && slot.classList.contains('gone'), markIn: !!q('.dsc-mark.in'),
    slots: [...qa('.dsc-slot')].map(e => [e.classList.contains('in'), e.classList.contains('blink'), e.classList.contains('gone'), !!e.querySelector('.dsc-mark.in'), +(+getComputedStyle(e).opacity).toFixed(3)]),
    gate: !!document.getElementById('phaseGate') && document.getElementById('phaseGate').classList.contains('show'),
    pop: !!g && g.classList.contains('pop'), gOp: gc ? +(+gc.opacity).toFixed(3) : null, gTf: gc ? gc.transform : null,
    look: !!g && g.classList.contains('look'), warm: !!g && g.classList.contains('warm'), arm: q('.dsc-garm') ? getComputedStyle(q('.dsc-garm')).transform : null, iris: q('.dsc-giris') ? getComputedStyle(q('.dsc-giris')).transform : null, lean: q('.dsc-grig') ? getComputedStyle(q('.dsc-grig')).transform : null,
    sfxVol: sfx ? +sfx.volume.toFixed(3) : null, sfxPaused: sfx ? sfx.paused : null,
    tTf: [...qa('.dsc-tile')].map(t => getComputedStyle(t).transform), tAn: [...qa('.dsc-tile')].map(t => getComputedStyle(t).animationName),
    faceGlow: lit >= 0 ? getComputedStyle(qa('.dsc-tile')[lit].querySelector('.dsc-face')).boxShadow : null,
    tilesIn: qa('.dsc-tile.in').length, lit, off: qa('.dsc-tile.off').length, pulse: !!q('.dsc-tile.pulse'), live: !!q('.dsc-tile.live'), done: !!q('.dsc-tile.done'),
    liveN: qa('.dsc-tile.live').length, wig: [...qa('.dsc-tile')].map(t => t.classList.contains('wiggle')), on: !!q('.dsc-tile.on'), att: state.attempts, hand: !!q('.slide-stage .reveal-hand.dmf-hand'), conf: !!q('.fx-confetti'), demo: !!state.demoRunning,
    nav: getComputedStyle(document.getElementById('navBtn')).display }; }""".replace("PREFIX", C["prefix"]).replace("NAMES", json.dumps(NAMES))
# the timeline sampled in the page every frame; the taps made in the page at their moments: the chip 1 s into the first clip (ignored),
# the right tile 0.5 s into the explanation (ignored), the chip 0.3 s after the tile is live (the sentence again), the tile 0.3 s
# after that reading has ended
TIMELINE = ("(sample) => { window._tl = []; window._taps = []; const S = eval(sample); let liveAt = 0, rereadSeen = false, rereadEnded = 0;"
    " const step = () => { const s = S(); window._tl.push(s); const chip = document.querySelector('.tut-audio'), tile = document.querySelector('.dsc-tile.tTILE');"
    " if (chip && !window._taps.includes('intro') && s.clip === 'FIRST' && s.playing && s.t > FIRST_T) { window._taps.push('intro'); chip.click(); }"
    " if (tile && !window._taps.includes('early') && s.clip === 'explain' && s.playing && s.t > 0.5) { window._taps.push('early'); tile.click(); }"
    " if (s.live && !liveAt) liveAt = s.ms;"
    " if (chip && liveAt && !window._taps.includes('chip') && s.ms - liveAt > 300) { window._taps.push('chip'); chip.click(); }"
    " if (window._taps.includes('chip') && s.clip === 'sent' && s.playing) rereadSeen = true;"
    " if (rereadSeen && !rereadEnded && !(s.clip === 'sent' && s.playing)) rereadEnded = s.ms;"
    " if (tile && rereadEnded && !window._taps.includes('tap') && s.ms - rereadEnded > 300) { window._taps.push('tap'); tile.click(); }"
    " if (s.slide !== 'NEXT' && (s.ms - (window._t0 || (window._t0 = s.ms))) < 120000) requestAnimationFrame(step); }; requestAnimationFrame(step); }"   # runs until the next page (the first frame may come before the page has mounted)
    ).replace("TILE", str(PICK + 1)).replace("FIRST_T", "1" if C["intro"] else "0.5").replace("FIRST", FIRST).replace("NEXT", NEXT)
# [g1-scene] the pick's timeline: the chip 1 s into the intro (ignored), a wrong tile 0.5 s into the sentence's clip (ignored: not live),
# the wrong tile W1 0.3 s after all three tiles are live, the right tile 0.2 s after that (ignored: the buzz sounds), the chip 0.3 s after
# hint 1 has ended (the sentence again), the wrong tile W2 0.3 s after that reading, the right tile 0.3 s after hint 2 has ended
TIMELINE_PICK = ("(sample) => { window._tl = []; window._taps = []; const S = eval(sample); let liveAt = 0, w1At = 0, h1Seen = false, h1End = 0, rrSeen = false, rrEnd = 0, h2Seen = false, h2End = 0;"
    " const T = (k) => document.querySelectorAll('.dsc-tile')[k];"
    " const step = () => { const s = S(); window._tl.push(s); const chip = document.querySelector('.tut-audio');"
    " if (chip && !window._taps.includes('intro') && s.clip === 'intro' && s.playing && s.t > 1) { window._taps.push('intro'); chip.click(); }"
    " if (!window._taps.includes('early') && s.clip === 'sent' && s.playing && s.t > 0.5 && T(W1)) { window._taps.push('early'); T(W1).click(); }"
    " if (s.liveN >= 3 && !liveAt) liveAt = s.ms;"
    " if (liveAt && !window._taps.includes('wrong1') && s.ms - liveAt > 300) { window._taps.push('wrong1'); w1At = s.ms; T(W1).click(); }"
    " if (w1At && !window._taps.includes('locked') && s.ms - w1At > 200) { window._taps.push('locked'); T(PICK).click(); }"
    " if (window._taps.includes('wrong1') && s.clip === 'H1' && s.playing) h1Seen = true;"
    " if (h1Seen && !h1End && !(s.clip === 'H1' && s.playing)) h1End = s.ms;"
    " if (chip && h1End && !window._taps.includes('chip') && s.ms - h1End > 300) { window._taps.push('chip'); chip.click(); }"
    " if (window._taps.includes('chip') && s.clip === 'intro' && s.playing) rrSeen = true;"
    " if (rrSeen && !rrEnd && !(s.clip === 'intro' && s.playing)) rrEnd = s.ms;"
    " if (rrEnd && !window._taps.includes('wrong2') && s.ms - rrEnd > 300) { window._taps.push('wrong2'); T(W2).click(); }"
    " if (window._taps.includes('wrong2') && s.clip === 'H2' && s.playing) h2Seen = true;"
    " if (h2Seen && !h2End && !(s.clip === 'H2' && s.playing)) h2End = s.ms;"
    " if (h2End && !window._taps.includes('tap') && s.ms - h2End > 300) { window._taps.push('tap'); T(PICK).click(); }"
    " if (s.slide !== 'NEXT' && (s.ms - (window._t0 || (window._t0 = s.ms))) < 120000) requestAnimationFrame(step); }; requestAnimationFrame(step); }"
    ).replace("W1", str(C.get("wrong", [1, 2])[0])).replace("W2", str(C.get("wrong", [1, 2])[1])).replace("PICK", str(PICK)).replace("H1", (C.get("hints") or ["vo_", "vo_"])[0][3:]).replace("H2", (C.get("hints") or ["vo_", "vo_"])[1][3:]).replace("NEXT", NEXT)
TL = TIMELINE_PICK if PICKM else TIMELINE

def lit_want(times, wend, t):
    if t is None or (wend is not None and t >= wend): return []
    st = None
    for x in times:
        if t >= x: st = x
    return [i for i, x in enumerate(times) if st is not None and x == st]
def ink(img, region):
    A = np.asarray(img, int); x0, y0, x1, y1 = region; sub = A[y0:y1, x0:x1]
    m = (sub[..., 2] > sub[..., 0] + 40) & (sub.sum(axis=2) < 450); ys, xs = np.nonzero(m)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1) if len(xs) else None
def scale_of(tf):
    m_ = re.findall(r"-?[\d.]+", tf or ""); return float(m_[0]) if tf not in (None, "none") and m_ else 1.0
def nil(g):   # Chrome writes a nil shadow several ways: none, a transparent black or orange 0-spread shadow, the spread a float residue
    if g in (None, "none"): return True
    m_ = re.fullmatch(r"rgba\(\d+, \d+, \d+, 0\) 0px 0px 0px ([\d.e+-]+)px", g); return bool(m_) and float(m_.group(1)) < 0.01
IDENT = ("none", "matrix(1, 0, 0, 1, 0, 0)")   # a finished fill-both animation holds its `to` (transform:none), which Chrome writes as the identity matrix

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--autoplay-policy=no-user-gesture-required", "--mute-audio"])
    errs, bad = [], []

    # ---- 1-2. timing at 1333x750
    pg = b.new_page(viewport={"width": 1333, "height": 750})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500)
    pg.evaluate("_ac()"); pg.wait_for_timeout(300)   # the engine's AudioContext, as the start tap would have made it
    pg.evaluate(NAVLOG); pg.evaluate(SOUNDS); pg.evaluate(TL, SAMPLE); pg.evaluate(GOTO, PAGE)
    d = pg.evaluate("CARD.slides[state.idx].data"); ST = d["sentence"]["word_times"]; SE = d["sentence"].get("word_end")
    XT = d["explain"]["word_times"] if not PICKM else []; CUE = XT[d["explain"]["cue_word"]] if not PICKM else None   # [g1-scene] the pick has no explanation
    if PICKM:
        check(f"[g1-scene] the page's data: PUNCT_PICK with data.scene (variant \"pick\"), the intro line {C['intro_clip']}, the picture and the girl (still, no pop, no sound), the sentence (its clip and {C['nwords']} word times), the marks {C['opts']}, the answer \"{C['mark']}\", no explanation, no bubble, the 53x90 slot, T2's blink and tiles; the hint lines {C['hints']}, the praise {C['ok_clip']}, no hint 3 line; the idle re-read off ([g1-quiet] no_idle_vo)",
              pg.evaluate("CARD.slides[state.idx].type") == "PUNCT_PICK" and d.get("scene") is True and d.get("variant") == "pick" and d.get("intro_audio") == C["intro_clip"] and d["bg_id"] == C["bg"] and d["image_id"] == C["girl"]
              and d.get("girl_pop") is False and not d.get("pic_sfx") and not d.get("bubble_id") and not d.get("box_sfx") and (d.get("slot_w", 53), d.get("slot_h", 90)) == C["slot"] and not d.get("explain")
              and d["sentence"]["text_hi"] == C["sent"] and d["sentence"]["audio"] == C["sent_clip"] and len(ST) == C["nwords"] and [o["mark"] for o in d["options"]] == C["opts"] and d["mark"] == C["mark"] and d["options"][PICK]["mark"] == C["mark"]
              and d["blink_ms"] == 7000 and d["blink_cycle_ms"] == 1750 and d["tiles_sfx"] == "sfx_demo1_pop.mp3" and d["tiles_gap_ms"] == 350
              and [d.get("hint1_audio"), d.get("hint2_audio")] == C["hints"] and d.get("ok_audio") == C["ok_clip"] and d.get("hint3_audio") is None and d.get("no_idle_vo") is True,   # [g1-quiet]
              {k: d.get(k) for k in ("scene", "variant", "intro_audio", "bg_id", "image_id", "girl_pop", "slot_w", "mark", "blink_ms", "hint1_audio", "hint2_audio", "ok_audio", "hint3_audio", "no_idle_vo")})
    else:
        check(f"the page's data: PUNCT_SCENE with {'the intro line' if C['intro'] else 'no intro line (open_ms ' + str(C['open_ms']) + ')'}, the picture and the girl, {'the bubble and the box sound, ' if C['bubble'] else ''}the sentence (its clip and word times), the explanation with its cue word \"{C['cue']}\", the marks {C['opts']}, the answer \"{C['mark']}\", the sound / blink / pop",
              pg.evaluate("CARD.slides[state.idx].type") == "PUNCT_SCENE" and d.get("intro_audio") == ("vo_demo1_intro" if C["intro"] else None) and (C["intro"] or d.get("open_ms") == C["open_ms"])
              and d["bg_id"] == C["bg"] and d["image_id"] == C["girl"] and d.get("bubble_id") == C["bubble"] and d.get("box_sfx") == C["box_sfx"] and (d.get("slot_w", 53), d.get("slot_h", 90)) == C["slot"]
              and d["sentence"]["text_hi"] == C["sent"] and d["sentence"]["audio"] == C["sent_clip"] and len(ST) == C["nwords"] and d["explain"]["audio"] == C["explain_clip"]
              and d["explain"]["text_hi"].split()[d["explain"]["cue_word"]] == C["cue"] and [o["mark"] for o in d["options"]] == C["opts"] and d["mark"] == C["mark"] and d["options"][PICK]["mark"] == C["mark"]
              and ((d.get("pic_sfx_ms"), d.get("pic_sfx"), d.get("girl_pop", True)) == ((2000, "sfx_demo1_school.mp3", True) if C["beat"] else (None, None, False))) and d["blink_ms"] == 7000 and d["blink_cycle_ms"] == 1750 and d["tiles_sfx"] == "sfx_demo1_pop.mp3" and d["tiles_gap_ms"] == 350,
              {k: d.get(k) for k in ("intro_audio", "open_ms", "bg_id", "image_id", "bubble_id", "box_sfx", "slot_w", "slot_h", "mark", "pic_sfx_ms", "blink_ms", "blink_cycle_ms", "tiles_gap_ms")})
    if C.get("nslots"):   # [t4-scene]
        check(f"[t4-scene] the page's data: {C['nslots']} slots ({C['slot'][0]}x{C['slot'][1]}), the marks {C['stagger']} ms apart, the gaps after \"आम\" and \"केला\" (words 2, 3)",
              d.get("slots") == C["nslots"] and d.get("mark_stagger_ms") == C["stagger"] and d["sentence"].get("gaps") == [2, 3] and d["sentence"]["text_hi"].split()[2:4] == ["आम", "केला"],
              {k: d.get(k) for k in ("slots", "mark_stagger_ms")} | {"gaps": d["sentence"].get("gaps")})
    if C["look"]:   # [t3-look]
        LK = C["look"]; gl = d.get("girl_look") or {}
        check(f"[t3-look] the page's data: girl_rig and girl_look (every {C['look']['every_ms'] / 1000:g} s, the gesture 2.3 s, the eyes 2.26 / 1.13 px, the arm 11 degrees, the lean 2 degrees)",
              d.get("girl_rig") is True and all(abs(gl.get(k, -1) - v) < 0.01 for k, v in LK.items()), gl)
        rig = pg.evaluate("""() => { const q = (s) => document.querySelector(s), L = [...document.querySelectorAll('.dsc-grig > *')];
          return { n: L.length, cls: L.map(e => e.className.split(' ')[0]), masked: L.map(e => { const c = getComputedStyle(e); return (c.maskImage || c.webkitMaskImage || '').startsWith('url("data:image/png') && (c.maskSize || c.webkitMaskSize) === '100% 100%'; }),
            wins: document.querySelectorAll('.dsc-grig img').length, same: [...document.querySelectorAll('.dsc-grig img')].every(i => i.getAttribute('src') === q('.dsc-gbody').getAttribute('src')),
            box: [...document.querySelectorAll('.dsc-grig, .dsc-grig > *')].every(e => Math.abs(e.getBoundingClientRect().width - q('.dsc-girl').getBoundingClientRect().width) < 0.5 && Math.abs(e.getBoundingClientRect().height - q('.dsc-girl').getBoundingClientRect().height) < 0.5),
            fills: [...document.querySelectorAll('.dsc-gfill')].map(e => getComputedStyle(e).backgroundColor), irises: [...document.querySelectorAll('.dsc-giris')].map(e => getComputedStyle(e).backgroundImage.startsWith('url("data:image/png')),
            origin: getComputedStyle(q('.dsc-garm')).transformOrigin, leanOrigin: getComputedStyle(q('.dsc-grig')).transformOrigin, plainImg: !!q('.dsc-girl > img'),
            still: ['.dsc-garm', '.dsc-giris', '.dsc-grig'].every(s => getComputedStyle(q(s)).transform === 'none' || getComputedStyle(q(s)).transform === 'matrix(1, 0, 0, 1, 0, 0)'), look: !!q('.dsc-girl.look'),
            promoted: ['.dsc-garm', '.dsc-giris', '.dsc-grig'].every(s => getComputedStyle(q(s)).willChange === 'transform') }; }""")
        check("[t3-look] the rig: five layers in .dsc-grig (the body, two eyes, the forearm, the braid tip), every one her box's size, masked by a data-URI sheet at 100% 100%; every window the same bitmap; the sclera discs and the irises in place; the forearm's origin at the elbow, the lean's at her feet; no plain image; all at identity at mount, and composited from mount (will-change: transform, [t3-look7])",
              rig["n"] == 5 and rig["cls"] == ["dsc-gbody", "dsc-geye", "dsc-geye", "dsc-garm", "dsc-gpatch"] and all(rig["masked"]) and rig["wins"] == 5 and rig["same"] and rig["box"]
              and len(rig["fills"]) == 2 and all(f.startswith("rgb(25") for f in rig["fills"]) and rig["irises"] == [True, True] and rig["origin"] == "188.91px 143.89px" and rig["leanOrigin"] == "128.5px 378.84px"
              and not rig["plainImg"] and rig["still"] and not rig["look"] and rig["promoted"], rig)
    if C["intro"]:
        pg.wait_for_function(f"isPlaying && currentAudio && currentAudio.src.includes('{INTRO_CLIP}.') && currentAudio.currentTime > 0.7", timeout=10000, polling=20)
    else: pg.wait_for_timeout(600)
    pg.screenshot(path=str(out / "a_open_1333.png"))
    pg.wait_for_function("!!document.querySelector('.dsc-girl.pop')" if C["beat"] else "!!document.querySelector('.dsc-slot.blink')", timeout=30000, polling=20); pg.wait_for_timeout(180); pg.screenshot(path=str(out / "b_beat_1333.png"))
    pg.wait_for_function("!!document.querySelector('.dsc-tile.t3.in')", timeout=30000, polling=20); pg.wait_for_timeout(600); pg.screenshot(path=str(out / "c_tiles_1333.png"))
    if PICKM:   # [g1-scene] the child's pick: the wiggles, the hint lines, the re-read, then the press
        pg.wait_for_function("!!document.querySelector('.dsc-tile.wiggle')", timeout=40000, polling=20); pg.wait_for_timeout(120); pg.screenshot(path=str(out / "d_wiggle_1333.png"))
        look = None
        try: pg.wait_for_function("!!document.querySelector('.dsc-tile.on')", timeout=90000, polling=20)
        except Exception:
            print("DIAG taps", pg.evaluate("window._taps"), "samples", pg.evaluate("window._tl.length"), "last", pg.evaluate("window._tl[window._tl.length - 1]"), "errors", errs[:3]); raise
        pg.wait_for_timeout(500); pg.screenshot(path=str(out / "f_done_1333.png"))
        look2 = pg.evaluate("""() => { const t = document.querySelector('.dsc-tile.on'), f = t.querySelector('.dsc-face'), s = t.querySelector('.dsc-sym'); const c = getComputedStyle(f);
          return [c.borderTopColor, c.borderTopWidth, c.backgroundColor, c.boxShadow, getComputedStyle(s).color, getComputedStyle(t).animationName]; }""")
    else:
        pg.wait_for_function("!!document.querySelector('.dsc-tile.lit')", timeout=30000, polling=20); pg.wait_for_timeout(250); pg.screenshot(path=str(out / "d_lit_1333.png"))
        pg.wait_for_function("!!document.querySelector('.dsc-tile.pulse')", timeout=30000, polling=20); pg.wait_for_timeout(500); pg.screenshot(path=str(out / "e_pulse_1333.png"))
        look = pg.evaluate("""(k) => { const T = document.querySelectorAll('.dsc-tile'), t = T[k], f = t.querySelector('.dsc-face'), s = t.querySelector('.dsc-sym'), dim = T[k === 0 ? 1 : 0];
          return [getComputedStyle(t).animationName, getComputedStyle(t).animationIterationCount, getComputedStyle(f).animationName, getComputedStyle(s).color,
          getComputedStyle(f).borderTopWidth, getComputedStyle(f).borderTopColor, getComputedStyle(dim).opacity]; }""", PICK)
        try: pg.wait_for_function("!!document.querySelector('.dsc-tile.done')", timeout=40000, polling=20)
        except Exception:
            print("DIAG taps", pg.evaluate("window._taps"), "samples", pg.evaluate("window._tl.length"), "last", pg.evaluate("window._tl[window._tl.length - 1]"), "errors", errs[:3]); raise
        pg.wait_for_timeout(500); pg.screenshot(path=str(out / "f_done_1333.png"))
        look2 = pg.evaluate("""() => { const t = document.querySelector('.dsc-tile.done'), f = t.querySelector('.dsc-face'), s = t.querySelector('.dsc-sym'); const c = getComputedStyle(f);
          return [c.borderTopColor, c.borderTopWidth, c.backgroundColor, c.boxShadow, getComputedStyle(s).color]; }""")
    pg.wait_for_function(f"CARD.slides[state.idx].id === '{NEXT}'", timeout=30000 if C.get("gate") else 10000)
    samples, taps, snd = pg.evaluate("window._tl"), pg.evaluate("window._taps"), pg.evaluate("window._snd")
    samples = [s for s in samples if s["ready"] and s["slide"] == PAGE]
    with open(out / "timeline.json", "w", encoding="utf-8") as f: json.dump(samples, f, indent=0)
    ms = lambda i: samples[i]["ms"]
    first = lambda cond, start=0: next(i for i in range(start, len(samples)) if cond(samples[i]))
    start_of = lambda c, i0=0: first(lambda s: s["clip"] == c and s["playing"] and (s["t"] or 0) > 0, i0)
    end_of = lambda c, i0: first(lambda s: s["clip"] != c or not s["playing"], i0 + 1)
    i_slot = first(lambda s: s["slotIn"]); i_rise = first(lambda s: s["shown"] > 0)
    i_open_end = end_of("intro", start_of("intro")) if C["intro"] else i_slot   # the opening: the intro line, or the bare scene for open_ms
    quiet = samples[:i_open_end]
    check(f"{'the intro line is the first clip and sounds' if C['intro'] else 'no clip sounds and nothing moves for open_ms'} over the picture, the girl in her place (still), the standing Swiftie and the 🔊 chip, there from the first frame; no sentence word, slot, pop or tile before {'it has ended' if C['intro'] else 'the bubble'}",
          next(s["clip"] for s in samples if s["clip"]) == FIRST and all(s["gOp"] == 1 and s["gTf"] == "none" for s in quiet)
          and all(s["bgLoaded"] for s in quiet if s["ms"] - samples[0]["ms"] >= 50)   # the bitmap's `complete` can flip one frame after the mount (seen once; a decode race, not the page)
          and not any(s["shown"] or s["slotIn"] or s["pop"] or s["tilesIn"] or s["bubIn"] for s in quiet) and (C["intro"] or not any(s["clip"] for s in quiet))
          and pg.evaluate("(() => { const sw = document.querySelector('.sfig-swiftie'); return !!sw; })()"), (round(ms(i_open_end) - ms(0)), ))
    if C["intro"]:
        check("0.5 s after the intro the slot pops in and the sentence rises in WHOLE in the same frame", 350 <= ms(i_slot) - ms(i_open_end) <= 800 and abs(ms(i_rise) - ms(i_slot)) <= 34
              and {s["shown"] for s in samples} <= {0, len(ST)} and samples[i_rise]["rise"], (round(ms(i_slot) - ms(i_open_end)), round(ms(i_rise) - ms(i_slot))))
    elif not C["bubble"]:   # [t4-scene] no intro line, no bubble: open_ms, then the slots and the whole sentence in one frame
        both = first(lambda s: s["slots"] and all(x[0] for x in s["slots"]))
        check(f"[t4-scene] open_ms ({C['open_ms']}) after the first frame ALL {C.get('nslots', 1)} slots pop in and the sentence rises in WHOLE, in the same frame",
              C["open_ms"] - 150 <= ms(i_slot) - ms(0) <= C["open_ms"] + 400 and both == i_slot and len(samples[i_slot]["slots"]) == C.get("nslots", 1) and abs(ms(i_rise) - ms(i_slot)) <= 34
              and {s["shown"] for s in samples} <= {0, len(ST)} and samples[i_rise]["rise"], (round(ms(i_slot) - ms(0)), both - i_slot, round(ms(i_rise) - ms(i_slot))))
    else:
        i_bub = first(lambda s: s["bubIn"]); bub_run = [s for s in samples[i_bub:] if s["ms"] - ms(i_bub) <= 600]
        bub_settled = all(s["bubTf"] in IDENT and s["bubOp"] == 1 for s in samples if 700 < s["ms"] - ms(i_bub) < 1500)
        check(f"[t3-scene] open_ms ({C['open_ms']}) after the first frame the speech bubble POPS in (dscBubbleIn: from half its size, past its size within 0.6 s, settled from 0.7 s) with the slot and the rising WHOLE sentence in the same frame",
              C["open_ms"] - 150 <= ms(i_bub) - ms(0) <= C["open_ms"] + 400 and abs(ms(i_slot) - ms(i_bub)) <= 34 and abs(ms(i_rise) - ms(i_bub)) <= 34
              and samples[i_bub]["bubAn"] == "dscBubbleIn" and scale_of(samples[i_bub]["bubTf"]) <= 0.7 and max(scale_of(s["bubTf"]) for s in bub_run) >= 1.0 and bub_settled
              and {s["shown"] for s in samples} <= {0, len(ST)} and samples[i_rise]["rise"],
              (round(ms(i_bub) - ms(0)), round(ms(i_slot) - ms(i_bub)), round(ms(i_rise) - ms(i_bub)), samples[i_bub]["bubAn"], round(scale_of(samples[i_bub]["bubTf"]), 3), round(max(scale_of(s["bubTf"]) for s in bub_run), 3), bub_settled))
    i_sent = start_of("sent", i_rise); i_sente = end_of("sent", i_sent)
    check("the sentence's clip starts ~0.45 s after the rise ([word-sync])", 380 <= ms(i_sent) - ms(i_rise) <= 800, round(ms(i_sent) - ms(i_rise)))
    timed = [s for s in samples[i_sent:i_sente] if s["clip"] == "sent" and s["playing"] and s["t"] is not None]
    off = [s for s in timed if s["hot"] not in (lit_want(ST, SE, s["t"]), lit_want(ST, SE, s["t"] - 0.05))]
    check("each word lit as the clip reaches it, one at a time, none after the last word's end", len(timed) > 20 and not off and len({tuple(s["hot"]) for s in timed if s["hot"]}) >= len(set(ST)) - 1,
          f"{len(timed)} samples, {len(off)} off")
    sfx = [e for e in snd if e["kind"] == "media" and e["src"] == "sfx_demo1_school.mp3"]
    if C["beat"]:
        i_pop = first(lambda s: s["pop"], i_sente)
        peak = max((scale_of(s["gTf"]) for s in samples[i_pop:] if s["ms"] - ms(i_pop) <= 600), default=1.0)
        still = all(s["gTf"] == "none" for s in samples[:i_pop]) and all(s["gTf"] == "none" for s in samples if s["ms"] - ms(i_pop) > 700)
        check("0.3 s after the sentence's clip the school sound (sfx_demo1_school.mp3 at .5) starts and the girl gives her small pop in that frame (dscPop: ~1.045 about her feet, back within 0.7 s), still before and after",
              200 <= ms(i_pop) - ms(i_sente) <= 650 and len(sfx) == 1 and abs(sfx[0]["ms"] - ms(i_pop)) <= 50 and sfx[0]["vol"] == 0.5 and 1.03 <= peak <= 1.05 and still,
              (round(ms(i_pop) - ms(i_sente)), [(round(e["ms"] - ms(i_pop)), e["vol"]) for e in sfx], round(peak, 4), still))
        t_sfx_end = ms(i_pop) + d["pic_sfx_ms"]
        vol_mid = next((s["sfxVol"] for s in samples[i_pop:] if s["ms"] - ms(i_pop) > 1000), None); vol_end = next((s["sfxVol"] for s in samples[i_pop:] if s["ms"] - ms(i_pop) > d["pic_sfx_ms"] - 120), None)
        paused_after = next((s["sfxPaused"] for s in samples[i_pop:] if s["ms"] - t_sfx_end > 120), None)
        check("the sound plays for pic_sfx_ms (2 s): full until its last 0.4 s, faded then, paused at its end", vol_mid == 0.5 and vol_end is not None and vol_end < 0.2 and paused_after is True, (vol_mid, vol_end, paused_after))
    else:
        i_pop = i_sente; t_sfx_end = ms(i_sente)   # [t3-girl] no beat: the blink follows the sentence's clip
        check("[t3-girl] no school sound and no pop: the girl stands still (opacity 1, transform none, never .pop) in every frame of the page",
              not sfx and all(s["gOp"] == 1 and s["gTf"] == "none" and not s["pop"] for s in samples), (len(sfx), sorted({(s["gOp"], s["gTf"], s["pop"]) for s in samples})[:3]))
    i_bl = first(lambda s: s["blink"], i_pop); i_ble = first(lambda s: not s["blink"], i_bl)
    # [t2-scene5] the box APPEARS and DISAPPEARS: its computed opacity 1 -> 0 -> 1 per blink_cycle_ms; a "trough" = a run of frames
    # under .05, blink_ms / blink_cycle_ms of them (the module rounds); its orange look (ring, fill, glow) is static through the blink
    cyc = d["blink_cycle_ms"]; n_bl = max(1, round(d["blink_ms"] / cyc))
    unseen = lambda s_: s_["slotOp"] is not None and s_["slotOp"] < 0.05
    tr_ms = [ms(k) for k in range(i_bl + 1, i_ble) if unseen(samples[k]) and not unseen(samples[k - 1])]
    gaps_bl = [round(b_ - a_) for a_, b_ in zip(tr_ms, tr_ms[1:])]
    jumps = max((abs(samples[k]["slotOp"] - samples[k - 1]["slotOp"]) for k in range(i_bl + 1, i_ble) if samples[k]["slotOp"] is not None and samples[k - 1]["slotOp"] is not None), default=0)
    seen_between = all(any(samples[k]["slotOp"] >= 0.99 for k in range(i_bl, i_ble) if a_ < ms(k) < b_) for a_, b_ in zip(tr_ms, tr_ms[1:]))
    after_bl = next(s_ for s_ in samples[i_ble:] if s_["ms"] - ms(i_ble) > 450)
    check(f"0.3 s after the {'sound' if C['beat'] else 'sentence (no beat, [t3-girl])'} the slot blinks for blink_ms ({d['blink_ms']} ms): the box fades out and in {n_bl} times, its troughs {cyc} ms apart ([t2-scene5] slow: no frame-to-frame opacity jump over .12), fully seen between them and at the end, plain 0.45 s after",
          200 <= ms(i_bl) - t_sfx_end <= 650 and abs(ms(i_ble) - ms(i_bl) - d["blink_ms"]) <= 120 and len(tr_ms) == n_bl and all(abs(g - cyc) <= 60 for g in gaps_bl)
          and jumps <= 0.12 and seen_between and samples[i_ble]["slotOp"] >= 0.97 and nil(after_bl["glow"]) and after_bl["slotBg"] == C["slot_fill"] and "232, 106, 0" not in (after_bl["ringStroke"] or ""),
          (round(ms(i_bl) - t_sfx_end), round(ms(i_ble) - ms(i_bl)), len(tr_ms), gaps_bl, round(jumps, 3), samples[i_ble]["slotOp"], (after_bl["slotBg"], after_bl["glow"], after_bl["ringStroke"])))
    look_bl = [s_ for s_ in samples[i_bl:i_ble] if s_["ms"] - ms(i_bl) >= 450]   # the look eases in over the slot's .25 / .4 s transitions
    ON = ("rgb(232, 106, 0)", C["blink_fill"], "rgba(232, 106, 0, 0.6) 0px 0px 0px 5px")
    check(f"[t2-scene5] the WHOLE box fades as one in its orange look: from 0.45 s into the blink to its end every frame has the ring the words' orange, the fill {C['blink_fill']} and the glow the pulsing tile's rgba(232,106,0,.6) 5px (the opacity alone moving)",
          len(look_bl) > 200 and all((s_["ringStroke"], s_["slotBg"], s_["glow"]) == ON for s_ in look_bl), (len(look_bl), sorted({(s_["ringStroke"], s_["slotBg"], s_["glow"]) for s_ in look_bl})[:3]))
    tail = [s_ for s_ in samples[i_ble:] if s_["ms"] - ms(i_ble) <= 700]
    check("[t2-scene5] the slot's pop-in (sfigBoxIn) does not run again when the blink ends: opacity 1 and the identity transform through the 0.7 s after (before: opacity 0 and scale .9 -> 1 over 0.5 s)",
          all(s_["slotOp"] >= 0.99 and s_["slotTf"] in IDENT for s_ in tail), [(round(s_["ms"] - ms(i_ble)), s_["slotOp"], s_["slotTf"]) for s_ in tail if not (s_["slotOp"] >= 0.99 and s_["slotTf"] in IDENT)][:5])
    i_tk = [first(lambda s, k=k: s["tilesIn"] >= k) for k in (1, 2, 3)]; i_t1 = i_tk[0]; gap = d["tiles_gap_ms"]
    pop = [e for e in snd if e["kind"] == "media" and e["src"] == "sfx_demo1_pop.mp3"]
    gaps = [round(ms(i_tk[k]) - ms(i_tk[k - 1])) for k in (1, 2)]
    pop_dt = [round(min(abs(e["ms"] - ms(i)) for e in pop), 1) if pop else 999 for i in i_tk]   # each tile's first frame to its nearest pop
    check(f"[t2-scene3] the three tiles come in ONE BY ONE as the blink starts ({gap} ms apart), the pop (sfx_demo1_pop.mp3 at .8) in EACH tile's first frame — three pops",
          abs(ms(i_t1) - ms(i_bl)) <= 50 and all(gap - 60 <= g <= gap + 60 for g in gaps) and len(pop) == 3 and all(dt <= 50 for dt in pop_dt) and all(e["vol"] == 0.8 for e in pop),
          (round(ms(i_t1) - ms(i_bl)), gaps, [(round(e["ms"] - ms(i_t1)), e["vol"]) for e in pop]))
    # each tile's pop: dscTileIn from under .6 of its size past 1.04, at its size (transform none) from 0.7 s on
    tpop = []
    for k, i in enumerate(i_tk):
        run = [s_ for s_ in samples[i:] if s_["ms"] - ms(i) <= 600]
        settled = all(s_["tTf"][k] == "none" for s_ in samples if 700 < s_["ms"] - ms(i) < 1500 and not s_["pulse"] and not s_["done"] and not s_.get("wig", [False] * 3)[k])   # [g1-scene] (the pick's wrong tap may wiggle it in that window)
        tpop.append((samples[i]["tAn"][k], round(scale_of(samples[i]["tTf"][k]), 3), round(max(scale_of(s_["tTf"][k]) for s_ in run), 3), settled))
    check("[t2-scene3] each tile POPS in (dscTileIn): under .6 of its size in its first frame, past 1.04 within 0.6 s, at its size from 0.7 s on",
          all(a == "dscTileIn" and s0 <= 0.6 and 1.04 <= pk <= 1.09 and st for a, s0, pk, st in tpop), tpop)
    extra = []   # [g1-scene] the pick's own sounds (the buzz, the confetti's) are counted below
    if not PICKM:
        i_x = start_of("explain", i_ble); i_xe = end_of("explain", i_x); i_lit = first(lambda s: s["lit"] >= 0)
        check(f"0.3 s after the blink the explanation sounds; the \"{C['mark']}\" tile (tile {PICK + 1}) lights as it reaches \"{C['cue']}\" ({CUE} s on its clock, within -0.05/+0.15 s), none before",
              200 <= ms(i_x) - ms(i_ble) <= 650 and i_x <= i_lit < i_xe and samples[i_lit]["lit"] == PICK and -0.05 <= samples[i_lit]["t"] - CUE <= 0.15 and not any(s["lit"] >= 0 for s in samples[:i_lit]),
              (round(ms(i_x) - ms(i_ble)), round(samples[i_lit]["t"] - CUE, 2) if i_lit > i_x else None))
        i_off = first(lambda s: s["off"] == 2, i_x); i_pulse = first(lambda s: s["pulse"], i_off); i_live = first(lambda s: s["live"], i_off)
        check("0.3 s after the clip the other two tiles are dim and dead; 0.3 s later the lit tile pulses and is live; the lit tile never dims",
              200 <= ms(i_off) - ms(i_xe) <= 650 and 200 <= ms(i_pulse) - ms(i_off) <= 650 and abs(ms(i_live) - ms(i_pulse)) <= 34 and all(s["off"] <= 2 for s in samples) and all(s["lit"] == PICK for s in samples[i_lit:]),
              (round(ms(i_off) - ms(i_xe)), round(ms(i_pulse) - ms(i_off))))
        starts = lambda c: sum(1 for i, s in enumerate(samples) if s["clip"] == c and s["playing"] and (i == 0 or not (samples[i - 1]["clip"] == c and samples[i - 1]["playing"])))
        check(f"🔊 during the first clip ({FIRST}) and the tile before it is live were ignored (the first clip once before the chip is live, the explanation once; no .done before the live tile)",
              "intro" in taps and "early" in taps and sum(1 for i, s in enumerate(samples[:i_live]) if s["clip"] == FIRST and s["playing"] and (i == 0 or not (samples[i - 1]["clip"] == FIRST and samples[i - 1]["playing"]))) == 1
              and starts("explain") == 1 and not any(s["done"] for s in samples[:i_live]), (taps, starts(FIRST), starts("explain")))
        i_rr = start_of("sent", i_live); i_rre = end_of("sent", i_rr)
        rr = [s for s in samples[i_rr:i_rre] if s["clip"] == "sent" and s["playing"] and s["t"] is not None]
        off2 = [s for s in rr if s["hot"] not in (lit_want(ST, SE, s["t"]), lit_want(ST, SE, s["t"] - 0.05))]
        check("🔊 once the tile is live reads the sentence again, each word lit, the tile still pulsing and nothing else changing",
              "chip" in taps and i_rr > i_live and len(rr) > 20 and not off2 and all(s["pulse"] and s["live"] and s["off"] == 2 and not s["done"] and s["tilesIn"] == 3 for s in rr), f"{len(rr)} samples, {len(off2)} off")
        i_done = first(lambda s: s["done"], i_rre); i_mark = first(lambda s: s["markIn"], i_live); i_gone = first(lambda s: s["gone"], i_done)
        corr = [e for e in snd if e["kind"] == "media" and e["src"] == "sfx_correct_new.ogg"]
        check("[t2-scene2] tapped: only the BORDER green (the engine's --correct, 3px), the face white, no glow, the mark its blue", look2 == ["rgb(0, 177, 50)", "3px", "rgb(255, 255, 255)", "none", "rgb(0, 47, 118)"], look2)
        check("the tap: the border green at once with the kit's correct sound (sfx_correct_new.ogg at .85) in that frame, the mark in the slot in that frame, the pulse off, the slot's box gone 0.45 s later",
              "tap" in taps and abs(ms(i_mark) - ms(i_done)) <= 34 and len(corr) == 1 and abs(corr[0]["ms"] - ms(i_done)) <= 50 and corr[0]["vol"] == 0.85
              and not samples[i_done + 2]["pulse"] and not samples[i_done + 2]["live"] and 380 <= ms(i_gone) - ms(i_done) <= 650, (round(ms(i_mark) - ms(i_done)), [(round(e["ms"] - ms(i_done)), e["vol"]) for e in corr], round(ms(i_gone) - ms(i_done))))
    else:   # [g1-scene] the child's pick
        W1, W2 = C["wrong"]; H1, H2 = [h[3:] for h in C["hints"]]; OKC = C["ok_clip"][3:]
        starts = lambda c: sum(1 for i, s in enumerate(samples) if s["clip"] == c and s["playing"] and (i == 0 or not (samples[i - 1]["clip"] == c and samples[i - 1]["playing"])))
        i_live = first(lambda s: s["liveN"] >= 1); i_on = first(lambda s: s["on"], i_live); before = samples[:i_on]
        check("[g1-scene] each tile is the child's from the frame it pops in (.live with its pop: 1, 2, 3 live; the page's drive off from the first), all three live until the answer; no tile lit, pulsing or dim and no hand before it; the blink runs its full 7 s regardless",
              all(samples[i]["liveN"] == k + 1 for k, i in enumerate(i_tk)) and i_live == i_t1 and not samples[i_live]["demo"] and samples[i_live - 1]["demo"]
              and not any(s["lit"] >= 0 or s["pulse"] or s["off"] or s["hand"] for s in before) and all(s["liveN"] == 3 for s in samples[i_tk[2]:i_on]) and i_ble < i_on and abs(ms(i_ble) - ms(i_bl) - d["blink_ms"]) <= 120,
              ([samples[i]["liveN"] for i in i_tk], samples[i_live - 1]["demo"], round(ms(i_ble) - ms(i_bl))))
        intro_before = sum(1 for i, s in enumerate(samples[:i_live]) if s["clip"] == "intro" and s["playing"] and (i == 0 or not (samples[i - 1]["clip"] == "intro" and samples[i - 1]["playing"])))
        check("the early tap (a tile 0.5 s into the sentence's clip) and 🔊 during the intro line were ignored: no wiggle and no attempt before the tiles are live, the intro line once before they are (the chip says it again later: [g1-quiet])",
              "early" in taps and "intro" in taps and not any(any(s["wig"]) or s["att"] for s in samples[:i_live]) and intro_before == 1, (taps[:2], intro_before))
        buzz = [e for e in snd if e["kind"] == "media" and e["src"] == "sfx_wrong_new.ogg"]
        i_w1 = first(lambda s: s["wig"][W1], i_live); i_w1e = first(lambda s: not s["wig"][W1], i_w1)
        i_h1 = start_of(H1, i_w1); i_h1e = end_of(H1, i_h1)
        check(f"[g1-scene] the first wrong tap (tile {W1 + 1}): it wiggles (wgNo, the class off within --fx-beat), the kit's wrong buzz (sfx_wrong_new.ogg at .85) in that frame, the attempt counted, no mark, every tile still the child's; hint 1 ({C['hints'][0]}) 0.5 s after",
              "wrong1" in taps and samples[i_w1 + 1]["att"] == 1 and len(buzz) >= 1 and abs(buzz[0]["ms"] - ms(i_w1)) <= 50 and buzz[0]["vol"] == 0.85 and 300 <= ms(i_w1e) - ms(i_w1) <= 650
              and not any(s["markIn"] for s in before) and all(s["liveN"] == 3 for s in samples[i_w1:i_on]) and 400 <= ms(i_h1) - ms(i_w1) <= 800,
              (round(ms(i_w1e) - ms(i_w1)), [(round(e["ms"] - ms(i_w1)), e["vol"]) for e in buzz[:1]], round(ms(i_h1) - ms(i_w1))))
        check("[tap-lock] the right tile tapped 0.2 s after the wrong one (the buzz still sounding) was ignored: no press, no mark, the attempt count unchanged through hint 1",
              "locked" in taps and not any(s["on"] or s["markIn"] for s in samples[:i_h1e]) and all(s["att"] == 1 for s in samples[i_w1 + 2:i_h1e]), (samples[i_h1e - 1]["att"],))
        i_rr = start_of("intro", i_h1e); i_rre = end_of("intro", i_rr)
        rr = [s for s in samples[i_rr:i_rre] if s["clip"] == "intro" and s["playing"] and s["t"] is not None]
        check("[g1-quiet] 🔊 after hint 1 says the instruction line again (vo_g1_intro) — NOT the sentence: no word lit, the three tiles the child's and nothing else changing",
              "chip" in taps and i_rr > i_h1e and len(rr) > 20 and all(not s["hot"] and s["liveN"] == 3 and not s["on"] and not s["markIn"] and s["off"] == 0 for s in rr), f"{len(rr)} samples")
        i_w2 = first(lambda s: s["wig"][W2], i_rre); i_h2 = start_of(H2, i_w2); i_h2e = end_of(H2, i_h2)
        check(f"[g1-scene] the second wrong tap (tile {W2 + 1}): the wiggle, the buzz in its frame, attempt 2, hint 2 ({C['hints'][1]}) 0.5 s after; no hand (that is the third tap's)",
              "wrong2" in taps and samples[i_w2 + 1]["att"] == 2 and len(buzz) == 2 and abs(buzz[1]["ms"] - ms(i_w2)) <= 50 and 400 <= ms(i_h2) - ms(i_w2) <= 800 and not any(s["hand"] for s in samples), (round(ms(i_h2) - ms(i_w2)), len(buzz)))
        i_w2e = first(lambda s: not s["wig"][W2], i_w2)
        still = [(k, round(ms(j) - ms(e)), samples[j]["tTf"][k]) for k, e in ((W1, i_w1e), (W2, i_w2e)) for j in range(e, len(samples)) if ms(j) - ms(e) <= 1000 and j < i_on and samples[j]["tTf"][k] not in IDENT]
        check("[g1-quiet] a wrong tile's pop-in (dscTileIn) does NOT run again as its wiggle ends: both wiggled tiles at their size (the identity transform) through the second after the wiggle's class has left; the sentence's clip sounded ONCE on the page (the intro line twice: the page's and the chip's), every word's light only during that one reading",
              not still and starts("sent") == 1 and starts("intro") == 2 and not any(s["hot"] for s in samples[i_sente:]), (still[:4], starts("sent"), starts("intro")))
        i_done = i_on; i_mark = first(lambda s: s["markIn"], i_live)
        corr = [e for e in snd if e["kind"] == "media" and e["src"] == "sfx_correct_new.ogg"]; cel = [e for e in snd if e["kind"] == "media" and e["src"] == "sfx_celebrate.ogg"]
        i_ok = start_of(OKC, i_on); i_oke = end_of(OKC, i_ok)
        check(f"the right tap (after hint 2): the tile presses with its mark in the slot in that frame, the kit's correct sound (sfx_correct_new.ogg at .85) and the confetti (.fx-confetti, its sfx_celebrate.ogg) in that tick (its frame is a long one: the 100 pieces are built in it); the other two tiles untouched (not dim), no green, the slot's box stays, no tile live; \"शाबाश!\" ({C['ok_clip']}) at once",
              "tap" in taps and i_on > i_h2e and abs(ms(i_mark) - ms(i_on)) <= 34 and len(corr) == 1 and abs(corr[0]["ms"] - ms(i_on)) <= 90 and corr[0]["vol"] == 0.85 and len(cel) == 1 and abs(cel[0]["ms"] - ms(i_on)) <= 90
              and any(s["conf"] for s in samples[i_on:i_on + 3]) and all(s["off"] == 0 and not s["done"] and not s["gone"] and s["liveN"] == 0 for s in samples[i_on + 1:]) and 0 <= ms(i_ok) - ms(i_on) <= 400,
              (round(ms(i_mark) - ms(i_on)), [(round(e["ms"] - ms(i_on)), e["vol"]) for e in corr], [round(e["ms"] - ms(i_on)) for e in cel], round(ms(i_ok) - ms(i_on))))
        check("[g1-scene] pressed: the tile's colours unchanged — its face's 2.386px #D5D8DF border, white, no glow, the mark its blue; the press is the demos' dmfTap",
              look2[0] == "rgb(213, 216, 223)" and abs(float(look2[1][:-2]) - 2.386) < 0.5 and look2[2] == "rgb(255, 255, 255)" and nil(look2[3]) and look2[4] == "rgb(0, 47, 118)" and look2[5].endswith("dmfTap"), look2)   # (dscTileIn stays first in the list)
        i_gone = i_oke   # the pick's box stays: the page's end is the praise line's
        extra = buzz + cel
    t_end = samples[-1]["ms"]
    if C.get("nslots", 1) > 1:   # [t4-scene] every slot pops, blinks and fades together; the marks land in turn, each box going 0.45 s after its mark
        n_ = C["nslots"]; lands = [first(lambda s, k=k: s["slots"][k][3], i_live) for k in range(n_)]; gones = [first(lambda s, k=k: s["slots"][k][2], i_done) for k in range(n_)]
        same = all(len({tuple(x[:2]) + (x[4],) for x in s["slots"]}) == 1 for s in samples[:i_done])
        check(f"[t4-scene] all {n_} slots identical in every frame before the tap (in / blinking / opacity); after it the comma lands in each in turn, {C['stagger']} ms apart (the first in the tap's frame), each box gone 0.45 s after its own comma",
              same and abs(ms(lands[0]) - ms(i_done)) <= 34 and all(abs(ms(b_) - ms(a_) - C["stagger"]) <= 50 for a_, b_ in zip(lands, lands[1:]))
              and all(380 <= ms(g_) - ms(l_) <= 650 for l_, g_ in zip(lands, gones)) and not any(s["slots"][k][3] for s in samples[:i_done] for k in range(n_)),
              (same, [round(ms(x) - ms(i_done)) for x in lands], [round(ms(g_) - ms(l_)) for l_, g_ in zip(lands, gones)]))
        i_gone = gones[-1]
    if PICKM:   # [g1-scene] the pick moves on PACE.tail after the praise line
        check(f"{C['next_what']} follows 1 s (PACE.tail) after \"शाबाश!\" has ended, by itself (no आगे, no gate)", 900 <= t_end - ms(i_oke) <= 1500 and pg.evaluate(C["next_ok"] + " && !document.getElementById('phaseGate').classList.contains('show')")
              and all(s["nav"] == "none" for s in samples), round(t_end - ms(i_oke)))
    elif C.get("gate"):   # [t4-scene] the round's gate after the tutorial's last page
        i_gate = first(lambda s: s["gate"], i_gone)
        check(f"[t4-scene] ~1.2 s after the last box has gone the round's gate opens (#phaseGate.show), by itself (no आगे); then {C['next_what']}",
              1000 <= ms(i_gate) - ms(i_gone) <= 1700 and not any(s["gate"] for s in samples[:i_gone]) and pg.evaluate(C["next_ok"]) and all(s["nav"] == "none" for s in samples[:i_gate]),
              round(ms(i_gate) - ms(i_gone)))
        t_end = ms(i_gate)   # the page's own sounds end here; the gate's are the gate's
    else:
      check(f"{C['next_what']} follows ~1.2 s after the box has gone, by itself (no आगे, no gate)", 1000 <= t_end - ms(i_gone) <= 1700 and pg.evaluate(C["next_ok"] + " && !document.getElementById('phaseGate').classList.contains('show')")
          and all(s["nav"] == "none" for s in samples), round(t_end - ms(i_gone)))   # (indented under the else above)
    if C["look"]:   # [t3-look] the glance on the timeline
        import math
        LK = C["look"]; EV, AC = LK["every_ms"], LK["active_ms"]
        num = lambda tf: [float(v) for v in re.findall(r"-?[\d.e+-]+", tf)] if tf and tf != "none" else [1, 0, 0, 1, 0, 0]
        arm = lambda s_: math.degrees(math.atan2(num(s_["arm"])[1], num(s_["arm"])[0]))   # rotate(theta): matrix(cos, sin, -sin, cos)
        eye = lambda s_: tuple(num(s_["iris"])[4:6])
        lean = lambda s_: math.degrees(math.atan(-num(s_["lean"])[2]))                     # skewX(a): matrix(1, 0, tan a, 1)
        i_t1 = first(lambda s_: s_["tilesIn"] >= 1); i_lk = first(lambda s_: s_["look"])
        tiny = lambda s_: abs(arm(s_)) < 0.01 and max(abs(v) for v in eye(s_)) < 0.01 and abs(lean(s_)) < 0.01
        check("[t3-look] .look starts in the frame the FIRST tile pops (no glance before it: every transform identity, or the warm-up's thousandths)", abs(i_lk - i_t1) <= 1 and not any(s_["look"] for s_ in samples[:i_t1])
              and all(tiny(s_) for s_ in samples[:i_t1]) and all(arm(s_) == 0 and eye(s_) == (0, 0) and lean(s_) == 0 for s_ in samples[:i_t1] if not s_["warm"]), (round(ms(i_lk) - ms(i_t1)), i_t1, i_lk))
        wf = [k for k in range(i_t1) if samples[k]["warm"]]
        runs_w = sum(1 for k in wf if k - 1 not in wf)
        check("[t3-look7] the GPU warm-up: .warm once, in the still moment after the slide-in and before the bubble (0.5-1 s after the page's first frame), 0.1-0.25 s long, the layers tilted by thousandths only (under 0.01 degree / px)",
              bool(wf) and runs_w == 1 and 500 <= ms(wf[0]) - ms(0) and ms(wf[-1]) < ms(i_slot) and 100 <= ms(wf[-1]) - ms(wf[0]) <= 250 and all(tiny(samples[k]) for k in wf) and any(arm(samples[k]) != 0 for k in wf),
              (round(ms(wf[0]) - ms(0)) if wf else None, round(ms(wf[-1]) - ms(wf[0])) if wf else None, runs_w, round(ms(i_slot) - ms(0))))
        t0 = ms(i_lk)
        cyc1 = [(ms(i) - t0, samples[i]) for i in range(i_lk, len(samples)) if ms(i) - t0 < EV]
        peak = min(arm(s_) for t_, s_ in cyc1 if 300 <= t_ <= 700); peak_t = next(t_ for t_, s_ in cyc1 if arm(s_) == peak)
        held = [arm(s_) for t_, s_ in cyc1 if 650 <= t_ <= 1500]; back = [(t_, arm(s_), eye(s_), lean(s_)) for t_, s_ in cyc1 if 2350 <= t_ <= EV - 50]
        ret_t = next((t_ for t_, s_ in cyc1 if t_ > 1500 and abs(arm(s_)) < 0.05 and eye(s_) == (0, 0) and abs(lean(s_)) < 0.01), None)
        check(f"[t3-look] the arm: up to -{LK['arm_deg']} degrees (a touch past) within 0.3-0.7 s, between -6 and -12 while it bobs (0.65-1.5 s), back at 0 by 2.35 s and 0 to the cycle's end",
              -LK["arm_deg"] - 1.5 <= peak <= -LK["arm_deg"] + 0.3 and held and all(-12 <= a <= -6 for a in held) and ret_t is not None and ret_t <= 2350 and back and all(a == 0 and e == (0, 0) and l == 0 for t_, a, e, l in back),
              (round(peak, 2), round(peak_t), (round(min(held), 1), round(max(held), 1)) if held else None, round(ret_t) if ret_t else None, len(back)))
        at = lambda t_: next(s_ for tt, s_ in cyc1 if tt >= t_)
        ex, ey = eye(at(300)); lx = lean(at(600))
        check(f"[t3-look] the eyes at ({LK['gx']}, {LK['gy']}) px by 0.3 s and held to 1.7 s, the lean at {LK['lean_deg']} degrees (sheared toward the tiles, from her feet) by 0.6 s and held to 1.7 s; neither ever past its mark",
              abs(ex - LK["gx"]) < 0.02 and abs(ey - LK["gy"]) < 0.02 and eye(at(1700)) == (ex, ey) and abs(lx - LK["lean_deg"]) < 0.05 and abs(lean(at(1700)) - lx) < 0.01
              and all(e[0] <= LK["gx"] + 0.02 and e[1] <= LK["gy"] + 0.02 and e[0] >= 0 and e[1] >= 0 and 0 <= l <= LK["lean_deg"] + 0.05 for t_, s_ in cyc1 for e, l in [(eye(s_), lean(s_))]), ((ex, ey), round(lx, 3)))
        steps = [(abs(arm(b_) - arm(a_)), abs(eye(b_)[0] - eye(a_)[0]), abs(lean(b_) - lean(a_)), round(tb - ta, 1)) for (ta, a_), (tb, b_) in zip(cyc1, cyc1[1:]) if tb - ta < 40]
        mx = max(st[0] for st in steps); me = max(st[1] for st in steps); ml = max(st[2] for st in steps)
        check("[t3-look] smooth: frame to frame the arm never turns more than 1.6 degrees, an iris never slides more than 0.45 px, the lean never changes more than 0.3 degrees; the arm never goes below 0 (its kept band under the braid would show)",
              mx <= 1.6 and me <= 0.45 and ml <= 0.3 and all(arm(s_) <= 0.001 for t_, s_ in cyc1), (round(mx, 2), round(me, 3), round(ml, 3), len(steps)))
        on_i = [i for i in range(i_lk + 1, len(samples)) if arm(samples[i]) < -1 and arm(samples[i - 1]) >= -1]
        onsets = [ms(i) - t0 for i in on_i]; slack = [ms(i) - ms(i - 1) for i in on_i]   # an onset is seen up to one frame late: that frame's length
        gaps_on = [round(b_ - a_) for a_, b_ in zip(onsets, onsets[1:])]
        check(f"[t3-look] the glance repeats every {EV} ms (its lift's onsets {EV} ms apart within 20 ms plus the frame each was seen in, at least once more before the tap)", len(onsets) >= 2 and all(abs(g - EV) <= 20 + max(sa, sb) for g, sa, sb in zip(gaps_on, slack, slack[1:])), (len(onsets), gaps_on[:6], [round(x) for x in slack[:6]]))
        # [t3-look7] the first glance on a cold browser (this check's browser is fresh): the warm-up keeps its start under 75 ms a frame
        # (without it: 83-117 ms frames as the arm began to lift; with it, measured 33-51 ms; a warm browser: 17 ms)
        long0 = [round(ms(i) - ms(i - 1)) for i in range(i_lk + 1, len(samples)) if ms(i) - t0 <= 400 and ms(i) - ms(i - 1) > 25]
        check("[t3-look7] the first glance's start on this (cold) browser: no frame over 75 ms in its first 0.4 s", all(x <= 75 for x in long0), long0)
        i_lke = first(lambda s_: not s_["look"], i_lk)
        rest_at_off = all(arm(samples[k]) == 0 and eye(samples[k]) == (0, 0) and lean(samples[k]) == 0 for k in (i_lke - 1, i_lke, i_lke + 1) if 0 <= k < len(samples))
        ph = (ms(i_done) - t0) % EV
        check(f"[t3-look] after the tap the class leaves only in a REST phase: every transform at identity in the frames around its going, which comes {'at once' if ph >= AC else 'once the running gesture has ended'} (within active_ms + 120 ms of the tap) and before the page leaves",
              i_lke >= i_done and rest_at_off and (ms(i_lke) - ms(i_done)) <= (AC - ph if ph < AC else 0) + 120 and not any(s_["look"] for s_ in samples[i_lke:]), (round(ms(i_lke) - ms(i_done)), round(ph), rest_at_off))
    if not PICKM:   # (the pick has no pulsing tile)
        check("the pulse: dscPulse, infinite, on the whole tile, its face glowing (dscGlow) with a 3px orange border, its mark the words' orange; the dim tiles at .6 ([t2-scene2])",
              look[0] == "dscPulse" and look[1] == "infinite" and look[2] == "dscGlow" and look[3] == "rgb(232, 106, 0)" and look[4] == "3px" and look[5] == "rgb(232, 106, 0)" and look[6] == "0.6", look)
        ga = [float(m.group(1)) for s_ in samples[i_pulse:i_done] if s_["faceGlow"] for m in [re.search(r"rgba\(232, 106, 0, ([\d.]+)\)", s_["faceGlow"])] if m]
        check("[t2-scene3] the pulsing tile's orange glow breathes between .6 and .7 (was .45 / .55)",
              bool(ga) and 0.58 <= min(ga) <= 0.62 and 0.68 <= max(ga) <= 0.72, (round(min(ga), 3) if ga else None, round(max(ga), 3) if ga else None, len(ga)))
    if C["box_sfx"]:
        box = [e for e in snd if e["kind"] == "media" and e["src"] == C["box_sfx"]]
        tones = [e for e in snd if e["kind"] == "tone" and samples[0]["ms"] - 50 <= e["ms"] <= t_end]
        check(f"[t3-scene] the user's sharp pop ({C['box_sfx']} at .8) once, in the bubble's frame, and no soft tone on the page", len(box) == 1 and abs(box[0]["ms"] - ms(i_slot)) <= 50 and box[0]["vol"] == 0.8 and not tones,
              ([(round(e["ms"] - ms(i_slot)), e["vol"]) for e in box], tones[:2]))
    else:
        box = [e for e in snd if e["kind"] == "tone" and e["f"] == "720" and e["ty"] == "sine" and e["d"] == 0.1 and e["v"] == 0.07]
        check("T1's text pop (the reference's sfxPopSoft) once, in the sentence's frame", len(box) == 1 and abs(box[0]["ms"] - ms(i_rise)) <= 50, [round(e["ms"] - ms(i_rise)) for e in box])
    others = [e for e in snd if samples[0]["ms"] - 50 <= e["ms"] <= t_end and e not in box and e not in sfx and e not in pop and e not in corr and e not in extra and not (e["kind"] == "media" and e["src"].startswith("vo_"))]
    check("no other sound effect through the page", not others, others[:4])
    check("आगे never shows on this page", all(not e["shown"] for e in pg.evaluate("window._navLog") if e["slide"] == PAGE))
    pg.evaluate(GOTO, PAGE); pg.wait_for_timeout(1200)
    boxes = pg.evaluate(BOXES, list(AS_T0)); worst = 0
    print("== card / Swiftie / chip vs page 3 T1 (stage px) ==")
    for sel, exp in AS_T0.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)); worst = max(worst, dd)
        print(f"  {sel:22s} got {[round(v,2) for v in got]}  want {[round(v,2) for v in exp]}  max|d|={dd:.2f}")
    check("the card, the standing Swiftie and the 🔊 chip are exactly page 3 T1's (within 0.5 px)", worst <= 0.5, f"worst {worst:.2f}px")
    radius = pg.evaluate("getComputedStyle(document.querySelector('.tut-card.sfig-card')).borderTopLeftRadius")
    check("the card has the frame's 64px corners (x 1333/1280)", abs(float(radius[:-2]) - 64 * FS) < 0.05, radius)
    pg.close()

    if PICKM:   # ---- 2b. [g1-scene] three wrong taps: the hand, the dead decoys, the guided tap without a line ([hand-quiet])
        W1, W2 = C["wrong"]
        pg = b.new_page(viewport={"width": 1333, "height": 750}); pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
        pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate("_ac()"); pg.wait_for_timeout(300); pg.evaluate(SOUNDS); pg.evaluate(GOTO, PAGE)
        pg.wait_for_function("document.querySelectorAll('.dsc-tile.live').length === 3", timeout=40000, polling=20)
        def quiet_(): pg.wait_for_function("!isPlaying && !sfxBusy()", timeout=20000, polling=20); pg.wait_for_timeout(300)
        def T(k): pg.click(f".dsc-tile.t{k + 1}", force=True)
        pg.wait_for_timeout(8500)   # [g1-quiet] 8.5 s of quiet with the tiles the child's: the engine's 7 s idle reminder must NOT re-read the sentence
        idle = pg.evaluate(f"[window._snd.filter(e => e.kind === 'media' && e.src === '{C['sent_clip']}.ogg').length, document.querySelectorAll('.dsc-sent .hot').length, isPlaying, !!_idleVoTimer]")
        check("[g1-quiet] 8.5 s of quiet once the tiles are the child's: the sentence's clip has sounded ONCE (no idle re-read), no word lit, nothing speaking, the idle ticker not running", idle[0] == 1 and idle[1] == 0 and not idle[2] and not idle[3], idle)
        T(W1); quiet_(); T(W2); quiet_(); T(W1); pg.wait_for_timeout(150); pg.screenshot(path=str(out / "h_hand_1333.png"))
        hand = pg.evaluate(f"""() => {{ const h = document.querySelector('.slide-stage .reveal-hand.dmf-hand'), t = document.querySelectorAll('.dsc-tile')[{PICK}]; if (!h) return null; const r = h.getBoundingClientRect(), tr = t.getBoundingClientRect();
          return [state.attempts, +(r.left + r.width / 2 - (tr.left + tr.width / 2)).toFixed(2), +(r.top - tr.bottom).toFixed(2), [...document.querySelectorAll('.dsc-tile')].map(x => [x.classList.contains('off'), x.classList.contains('live'), getComputedStyle(x).pointerEvents]), !!document.querySelector('.dsc-tile.on'), r.width]; }}""")
        check("[hand-quiet] the third wrong tap: the pointing hand (96px) centred under the right tile (its top within -12..12 px of the tile's bottom: the engine keeps the hand inside the stage, whose bottom clips and whose height varies by a few px, so here its fingertip sits at the tile's edge), the other two tiles dim and dead (.off, pointer-events none, no longer live), the right one still the child's, no press",
              hand is not None and hand[0] == 3 and abs(hand[1]) <= 2 and -12 <= hand[2] <= 12 and all(hand[3][k] == [k != PICK, k == PICK, "none" if k != PICK else "auto"] for k in range(3)) and not hand[4] and abs(hand[5] - 96) <= 1, hand)   # (the hand lives in .slide-stage, outside the card's scale: 96 px)
        quiet_(); n0 = len(pg.evaluate("window._snd")); T(W2); pg.wait_for_timeout(300)
        check("a dead tile tapped: nothing (no sound, no attempt, no wiggle)", pg.evaluate("state.attempts") == 3 and len(pg.evaluate("window._snd")) == n0 and not pg.evaluate("[...document.querySelectorAll('.dsc-tile')].some(t => t.classList.contains('wiggle'))"))
        t_tap = pg.evaluate("performance.now()"); T(PICK); pg.wait_for_timeout(250)
        st3 = pg.evaluate("[!!document.querySelector('.dsc-tile.on'), !!document.querySelector('.dsc-slot .dsc-mark.in'), !!document.querySelector('.fx-confetti'), !document.querySelector('.slide-stage .reveal-hand'), isPlaying]")
        pg.wait_for_function(f"CARD.slides[state.idx].id === '{NEXT}'", timeout=10000); t_next = pg.evaluate("performance.now()")
        snd3 = pg.evaluate("window._snd"); said = [e["src"] for e in snd3 if e["kind"] == "media" and e["src"].startswith("vo_") and e["ms"] > t_tap - 400 and e.get("slide") == PAGE]   # (G2's own intro line starts as it mounts: this page's sounds only)
        fx3 = [e["src"] for e in snd3 if e["kind"] == "media" and not e["src"].startswith("vo_") and e["ms"] > t_tap - 400 and e.get("slide") == PAGE]
        check(f"the guided tap (after the hand): the press, the mark in the slot, the confetti and the correct sound, the hand gone, NO line (no \"शाबाश!\"); {NEXT} ~1.7 s after",
              all(st3[:4]) and not st3[4] and not said and sorted(fx3) == ["sfx_celebrate.ogg", "sfx_correct_new.ogg"] and 1500 <= t_next - t_tap <= 2400, (st3, said, fx3, round(t_next - t_tap)))
        pg.close()

    # ---- 3. geometry + pixel diff at 1280x720
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("requestfailed", lambda r: bad.append(r.url))
    pg.goto(html.as_uri()); pg.wait_for_timeout(1500); pg.evaluate("_ac()"); pg.evaluate(GOTO, PAGE)
    pg.wait_for_function("!!document.querySelector('.dsc-tile.t3.in')", timeout=40000); pg.wait_for_timeout(650)
    pg.evaluate("document.querySelectorAll('.dsc-slot').forEach(e => e.classList.remove('blink'))"); pg.wait_for_timeout(600)   # the frame draws the slot plain (its fill's .4 s transition back, [t2-scene4])
    if C["look"]: pg.evaluate("() => { for (const a of document.querySelector('.dsc-girl').getAnimations({subtree:true})) { a.pause(); a.currentTime = 3000; } }"); pg.wait_for_timeout(100)   # [t3-look] the rig at rest (3 s into its cycle): her painting
    shot = out / "g_frame_1280.png"; pg.screenshot(path=str(shot))
    FRAME = C["FRAME"]; boxes = pg.evaluate(BOXES, list(FRAME)); worst = 0
    print("== boxes vs the frame (px) ==")
    for sel, exp in FRAME.items():
        got = boxes[sel]; dd = max(abs(g - e) for g, e in zip(got, exp)) if got else 99; worst = max(worst, dd)
        print(f"  {sel:16s} got {[round(v,2) for v in got] if got else None}  frame {[round(v, 3) for v in exp]}  max|d|={dd:.2f}")
    check("the picture, " + ("the bubble, " if C["bubble"] else "") + "the slot, the girl and her shadow, the tiles, their faces" + ("" if C.get("no_tshade") else " and shadows") + " within 1 px of the frame's nodes", worst <= 1.0, f"worst {worst:.2f}px")
    if C.get("no_tshade"):   # [g2-scene] the frame draws no ellipses under its tiles
        check("[g2-scene] no ellipse under the tiles (the frame has none): every .dsc-tshade display none", pg.evaluate("[...document.querySelectorAll('.dsc-tshade')].every(e => getComputedStyle(e).display === 'none')"))
    st = pg.evaluate("""() => { const c = (s) => getComputedStyle(document.querySelector(s)); return [c('.dsc-bg').borderTopLeftRadius, c('.dsc-bg').overflow, c('.dsc-slot').borderRadius, c('.dsc-slot').backgroundColor,
      c('.dsc-dash').stroke, c('.dsc-dash').strokeWidth, c('.t1 .dsc-face').borderTopWidth, c('.t1 .dsc-face').borderTopColor, c('.t1 .dsc-face').borderRadius, c('.dsc-base').backgroundColor, c('.dsc-base').boxShadow]; }""")
    check(f"the picture clipped to the card's padding box with its inner corners; the slot {C['slot_fill']}, 8px corners, a 2px rgba(86,86,86,.85) dashed ring; the tiles' faces 2.386px #D5D8DF, 18px corners, on a #D9D9D9 base with its 0 4 4 shadow",
          abs(float(st[0][:-2]) - (64 - 12 / FS)) < 0.05 and st[1] == "hidden" and st[2] == "8px" and st[3] == C["slot_fill"] and st[4] == "rgba(86, 86, 86, 0.85)" and st[5] == "2px"
          and abs(float(st[6][:-2]) - 2.386) < 0.5 and st[7] == "rgb(213, 216, 223)" and st[8] == "18px" and st[9] == "rgb(217, 217, 217)" and st[10] == "rgba(0, 0, 0, 0.25) 0px 4px 4px 0px", st)
    fonts = pg.evaluate("""(w) => { const f = (s) => { const c = getComputedStyle(document.querySelector(s)); return [c.fontFamily.split(',')[0], c.fontWeight, c.fontSize, c.color]; };
      return [f('.dsc-sent'), f('.t1 .dsc-sym'), f('.dsc-mark'), document.fonts.check("600 64px 'Story Noto Marks'", '।,?') && document.fonts.check("800 55px 'Story Baloo 2'", w)]; }""", C["first_word"])
    check("type: the sentence Baloo 2 800 at the frame's 55px #012F76; the tiles' marks in the frame's Noto Sans Devanagari SemiBold 64px #002F76 ('Story Noto Marks'); the landing mark the sentence's face; both faces loaded",
          fonts[0] == ['"Story Baloo 2"', "800", "55px", "rgb(1, 47, 118)"] and fonts[1] == ['"Story Noto Marks"', "600", "64px", "rgb(0, 47, 118)"] and fonts[2] == ['"Story Baloo 2"', "800", "55px", "rgb(1, 47, 118)"] and fonts[3], fonts)
    mine = Image.open(shot).convert("RGB")
    print("== text ink vs the Figma render (page px): centre and size ==")
    for name, region in C["INK"].items():
        a, t = ink(mine, region), ink(target, region)
        if not a or not t: check(f"{name}: ink found on both", False, (a, t)); continue
        dc = ((a[0] + a[2]) / 2 - (t[0] + t[2]) / 2, (a[1] + a[3]) / 2 - (t[1] + t[3]) / 2); ds = ((a[2] - a[0]) - (t[2] - t[0]), (a[3] - a[1]) - (t[3] - t[1]))
        print(f"  {name:9s} page {[int(v) for v in a]} ({a[2]-a[0]}x{a[3]-a[1]})  render {[int(v) for v in t]} ({t[2]-t[0]}x{t[3]-t[1]})  centre d=({dc[0]:+.1f},{dc[1]:+.1f})  size d=({ds[0]:+d},{ds[1]:+d})")
        check(f"{name}: its ink sits where the render's does (centre within 1.5 px), its size within 2 px", abs(dc[0]) <= 1.5 and abs(dc[1]) <= 1.5 and abs(ds[0]) <= 2 and abs(ds[1]) <= 2, (dc, ds))
    A = np.asarray(mine, np.int16); B = np.asarray(target, np.int16)
    for SI in (C["slot_in"] if isinstance(C["slot_in"], list) else [C["slot_in"]]):   # [t4-scene] every slot
        fill = lambda y, x, SI=SI: tuple(A[y, x]) == SI["rgb"]
        row = [x for x in range(*SI["xs"]) if fill(SI["row_y"], x)]; col = [y for y in range(*SI["ys"]) if fill(y, SI["col_x"])]
        w = SI["want"]
        check(f"the slot's interior is the frame's fill {SI['rgb']} (x {w[0]}..{w[1]}, y {w[2]}..{w[3]} within 2 px: the ring's anti-aliased inner edge on the 1280 grid's fractional positions)",
              row and col and abs(min(row) - w[0]) <= 2 and abs(max(row) + 1 - w[1]) <= 2 and abs(min(col) - w[2]) <= 2 and abs(max(col) + 1 - w[3]) <= 2,
              ((min(row), max(row) + 1) if row else None, (min(col), max(col) + 1) if col else None))
    pad = np.pad(B, ((1, 1), (1, 1), (0, 0)), mode="edge")
    near = np.min([np.abs(A - pad[1+dy:1+dy+A.shape[0], 1+dx:1+dx+A.shape[1]]).max(axis=2) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], axis=0)
    if C["girl_in_render"]:
        x0, y0, x1, y1 = GIRL; gc = near[y0:y1, x0:x1]
        print(f"  the girl vs the render (within 1 px): mean {gc.mean():.2f} levels, {100 * (gc > 48).mean():.2f}% over 48")
        check("the girl is the frame's bitmap, where the frame has her (within 1 px: mean diff under 12 levels, under 6% of her box over 48)", gc.mean() < 12 and (gc > 48).mean() < 0.06)
    else: print("  (the frame draws no girl: her region is left out of the pixel diff, she is T2's bitmap in T2's place — see the boxes)")
    keep = np.zeros(near.shape, bool); x0, y0, x1, y1 = WHOLE; keep[y0:y1, x0:x1] = True
    for x0, y0, x1, y1 in OWN_T0 + C["BY_DESIGN"] + [GIRL]: keep[y0:y1, x0:x1] = False
    m = (near > 32) & keep; px = int(keep.sum())
    solid = m.copy(); solid[1:-1, 1:-1] &= m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:]; solid[0, :] = solid[-1, :] = False; solid[:, 0] = solid[:, -1] = False
    print(f"  pixel diff vs the render over the card, less Swiftie/chip, the slot, the ink bands and the girl (within 1 px): {int(m.sum())} of {px} px ({100*m.sum()/px:.2f}%), solid {int(solid.sum())} ({100*solid.sum()/px:.3f}%)")
    Image.fromarray(np.where(m, 255, np.where(keep, 0, 60)).astype(np.uint8)).save(out / "g_diff_mask.png")
    check("the card — the picture, " + ("the bubble, " if C["bubble"] else "") + "the tiles, their shadows — pixel-matches the Figma render (solid diffs under 0.1% of the area)", solid.sum() / px < 0.001)
    pg.close(); b.close()
check("no page errors", not errs, errs[:3]); check("no failed requests", not bad, bad[:5])
print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAIL: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
