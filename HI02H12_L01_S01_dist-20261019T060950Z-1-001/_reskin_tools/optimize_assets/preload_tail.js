/* ===== [preload-tail] (2026-11-15) no wait on a sound that can hang =====
   Written in by optimize.py at the very end of app.js (everything else is defined by then).
   [load-bar-off] (2026-11-16): the cover's loading bar (its view was here) is gone; the play button comes at the welcome's end
   as before, and the files go on loading behind it.
   - Every clip the engine plays (play(): the welcome, the instructions, the gates' lines, every page's VO that a button or the
     next step waits for) has three ways to its end: its own "ended", its error (the engine's silent authored beat), and a
     watchdog: if it has not started 9 s (+ its length) after it was asked for, or runs 3.5 s past its length, it is ended for the
     page ("ended" is dispatched, so the engine's own end path runs). The watchdog never touches a clip the engine has already let
     go of (stopped, ended, refused by autoplay). It reports plmediastuck / plmediafail on window (the cover listens). ===== */
(function(){ "use strict";
  var P = window.__preload; if(!P) return;

  // ---------- the clip watchdog ----------
  var op = window.play; if(typeof op !== "function") return;
  var GRACE_MS = 3500, START_MS = 9000;
  var tell = function(type, detail){ try { window.dispatchEvent(new CustomEvent(type, { detail: detail })); } catch(x){} };
  function watch(a, src){
    a.__plWatch = true;
    var t = 0, over = false, known = (P.durationMs && P.durationMs(src)) || 0;
    var stop = function(){ over = true; clearTimeout(t); };
    var trip = function(why){
      if(over) return; over = true;
      if(typeof currentAudio === "undefined" || currentAudio !== a) return;   // the engine has already let go of this clip
      try { a.pause(); } catch(x){}
      var ev; try { ev = new Event("ended"); } catch(x){ ev = document.createEvent("Event"); ev.initEvent("ended", false, false); }
      a.dispatchEvent(ev);                                                     // the engine's own end path: setPlaying(false), onEnd
      tell("plmediastuck", { src: src, why: why });
    };
    var arm = function(ms, why){ clearTimeout(t); t = setTimeout(function(){ trip(why); }, ms); };
    arm(START_MS + known, "never started");
    a.addEventListener("playing", function(){ if(over) return;
      var d = (isFinite(a.duration) && a.duration > 0) ? a.duration * 1000 : known;
      arm(Math.max(0, d - a.currentTime * 1000) / (a.playbackRate || 1) + GRACE_MS, "ran past its length"); });
    a.addEventListener("ended", stop);
    a.addEventListener("pause", function(){ if(!over && (typeof currentAudio === "undefined" || currentAudio !== a)) stop(); });
    a.addEventListener("error", function(){ stop(); tell("plmediafail", { src: src }); });
  }
  window.play = function(src){
    var r = op.apply(this, arguments);
    try { var a = (typeof currentAudio !== "undefined") ? currentAudio : null; if(src && a && !a.__plWatch) watch(a, String(src)); } catch(x){}
    return r;
  };
})();
/* ===== [preload-tail] end ===== */
