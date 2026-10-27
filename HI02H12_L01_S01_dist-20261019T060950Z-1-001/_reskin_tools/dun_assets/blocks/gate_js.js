/* [GATE-REF-ANIM] (2026-10-08, user request) the gate beat of the reference lesson (its phaseBlurTransition, [H11-154] form), on this
   file's own gate: phaseBlurTransition is replaced here (its two callers - the start tap and completeSlide's phase boundary - call it
   by name, so they take this one), keeping this file's titles (PHASE_GATE_TITLE), lines (PHASE_GATE_VO through the card's audio map),
   the 4 s minimum hold (GATE_MS), the "never cut a line" rule (+200 ms after a line that outran the hold) and the GATE_MS + 7 s cap.
   Sequence, as in the reference: open (scrim + blur, .pg-up: the bird lifts in over 0.3 s already talking - nothing to wait for, the
   line starts at once, the reference's RISE_MS = 0) -> GATE_CAPTION_AT_MS into the line the headline is set and wipes in (.pg-say
   makes it visible, .pg-pop runs the wipe; fitGateTitle keeps it clear of the bird's crest, the reference's _fitGateTitle) -> once the
   line is over AND the hold has run: the first gate (.pg-talk) sinks the bird for 340 ms, then the screen clears and the next page
   mounts; the other gates clear at once. A fresh image URL per gate = the animation from its first frame (fetched once at boot into
   a blob, the way [GATE-STD-ANIM] did; the ?r= counter under file://). The reference's whoosh at the open (sfx_whoosh) is a sound,
   not an animation, and this lesson has no such file: not ported. */
(function(){ "use strict";
  if(typeof phaseBlurTransition !== "function") return;
  var GATE_REF_SRC = "assets/UI/peeking_talk_up.webp";
  var GATE_CAPTION_AT_MS = { tutorial: 3660, guided: 3940, practice: 1120 };   // ms into vo_pt_tutorial / vo_pt_guided / vo_pt_practice at which the headline's words begin (silence analysis of the recordings: the last clause / after "वाह!")
  var SINK_MS = 340;
  var gateRefBlob = null;
  if(location.protocol !== "file:") (window.__afterTitle || function(f){ f(); })(function(){ try{ return fetch(GATE_REF_SRC).then(function(r){ return r.ok ? r.blob() : null; }).then(function(b){ if(b) gateRefBlob = b; }).catch(function(){}); }catch(e){} });   // [ASSET-WARM] once the title art is in
  function fitGateTitle(){
    try{
      var t = $("phaseGateTitle"), im = $("phaseGateImg"), g = $("phaseGate");
      if(!t || !im || !t.textContent || !g || !g.classList.contains("show")){ window.removeEventListener("resize", fitGateTitle); return; }
      t.style.removeProperty("top"); t.style.scale = "";
      var ir = im.getBoundingClientRect(); if(!ir.height) return;
      var crest = ir.top + ir.height * 0.38, GAP = 12, EDGE = 8, W = window.innerWidth;
      var tr = t.getBoundingClientRect();
      var sc = Math.min(1, (W - 2 * EDGE) / tr.width);
      if(tr.top + tr.height * sc > crest - GAP){
        var room = crest - GAP - EDGE;
        sc = Math.min(sc, room / tr.height); sc = Math.max(0.35, sc);
        var top = Math.max(EDGE, crest - GAP - tr.height * sc);
        t.style.setProperty("top", top + "px", "important");
      }
      if(sc < 0.999){ t.style.transformOrigin = "50% 0"; t.style.scale = String(sc); }
    }catch(e){}
  }
  window.phaseBlurTransition = function(cb, toPhase){
    var tok = ++_gateToken;
    stopNudge(); stopAudio();
    var gate = $("phaseGate"), img = $("phaseGateImg"), title = $("phaseGateTitle");
    if(img){                                                   // the reference's bird, from its first frame
      if(img._gateUrl){ try{ URL.revokeObjectURL(img._gateUrl); }catch(e){} img._gateUrl = null; }
      img.removeAttribute("src"); void img.offsetWidth;
      if(gateRefBlob){ img._gateUrl = URL.createObjectURL(gateRefBlob); img.src = img._gateUrl; }
      else img.src = GATE_REF_SRC + "?r=" + Date.now();
    }
    if(title){ title.textContent = ""; title.classList.remove("pg-pop"); title.style.removeProperty("top"); title.style.scale = ""; }
    gate.classList.remove("pg-say", "pg-sink");
    gate.classList.add("pg-ref", "pg-up");
    gate.classList.toggle("pg-talk", toPhase === "tutorial");   // the first gate: he sinks on the way out, as in the reference
    $("stage").classList.add("blurred", "gating");
    document.body.classList.add("gating");
    gate.classList.add("show");
    SwiftPAL.emit("phase_transition", { to: toPhase });
    var capT = null;
    var clearGate = function(){
      gate.classList.remove("show", "pg-say", "pg-sink", "pg-up", "pg-talk");
      clearTimeout(capT); window.removeEventListener("resize", fitGateTitle);
      if(title){ title.textContent = ""; title.classList.remove("pg-pop"); title.style.removeProperty("top"); title.style.scale = ""; }
    };
    var closeGate = function(){ clearGate(); $("stage").classList.remove("blurred", "gating"); document.body.classList.remove("gating"); };
    var voId = PHASE_GATE_VO[toPhase];
    var voSrc = (voId && CARD.assets && CARD.assets.audio && CARD.assets.audio[voId]) || null;
    var openedAt = Date.now(), lineOver = false, timeUp = false, closed = false;
    var tearDown = function(){
      clearGate();
      $("stage").classList.remove("blurred");
      if(cb) cb();                              // mounts the next slide
      $("stage").classList.remove("gating");    // header returns once the slide is in
      document.body.classList.remove("gating");
    };
    var finish = function(){                                   // runs once BOTH the hold and the line are over
      if(closed || !(lineOver && timeUp)) return; closed = true;
      if(tok !== _gateToken){ closeGate(); return; }           // a newer gate superseded us
      if(gate.classList.contains("pg-talk")){ gate.classList.add("pg-sink"); setTimeout(tearDown, SINK_MS); }   // he goes back down first
      else tearDown();
    };
    setTimeout(function(){ timeUp = true; finish(); }, GATE_MS);
    setTimeout(function(){ lineOver = true; timeUp = true; finish(); }, GATE_MS + 7000);   // hard cap: never a stuck gate
    // the headline arrives with its words: set and wiped in GATE_CAPTION_AT_MS into the line
    capT = setTimeout(function(){
      if(tok !== _gateToken || !title) return;
      title.textContent = PHASE_GATE_TITLE[toPhase] || "";
      gate.classList.add("pg-say");
      title.classList.remove("pg-pop"); void title.offsetWidth; title.classList.add("pg-pop");
      fitGateTitle(); window.addEventListener("resize", fitGateTitle);
    }, GATE_CAPTION_AT_MS[toPhase] || 0);
    play(voSrc, function(){                                    // the line starts at once: he is up and talking already
      if(tok !== _gateToken){ closeGate(); return; }
      var beat = (Date.now() - openedAt >= GATE_MS) ? 200 : 0;   // a line that outran the hold: a short beat after it, then close
      setTimeout(function(){ lineOver = true; finish(); }, beat);
    });
  };
})();
