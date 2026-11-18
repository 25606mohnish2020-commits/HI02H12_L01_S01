/* [tab-pause] (asked 2026-11-18: "When any other tab is opened in the browser along with this tab then this file should pause
   completely at the place where it was left and if that tab in the browser is opened again then it should continue from the
   exact place where it was left"). Runs in <head>, before the engine and the preloader, so everything they do goes through it.
   While the page is hidden (document.visibilityState "hidden": another tab in front, the window minimised) the whole lesson stands
   still, and when it is seen again it carries on from that very moment, as if no time had passed:
   - the page's clock: performance.now(), Date.now(), the frame times handed to requestAnimationFrame and the Web Animations
     timeline's start times all run on ONE clock that stops while hidden (the real one less every hidden stretch), so every
     "how long since ..." the engine measures (idle prompts, holds, cue fallbacks, watchdogs) skips the hidden time;
   - timers: every setTimeout / setInterval is held with the time it still had to run and set going again with exactly that;
   - frames: animation-frame callbacks wait (the browser runs none in a hidden tab anyway);
   - sounds: every playing <audio>/<video> and Web Audio context is paused / suspended at its exact position and resumed from it;
     a sound asked for while hidden starts when the page is seen; the pause and resume themselves are invisible to the engine (their
     pause / play / playing events are swallowed - the engine's music ducking, its stuck-clip watchdog and its cue waits see no
     change, as for them nothing happened);
   - motion: CSS animations are held by one rule (:root.sgp-hidden, below), Web Animations and CSS transitions are paused and
     played again; an animation started while hidden starts held.
   Before the page is ever hidden all of this is a pass-through (the same timers, the same clock values). Animated picture files
   (the birds' WebP animations) are drawn by the browser itself, which stops them while the tab is hidden.
   window.__sgPause reports the state (hidden, total hidden ms, times hidden, log) for the checks. */
(function(){
  "use strict";
  var W = window, D = document, P = W.performance;
  if(!P || !P.now || W.__sgPause) return;
  var nativeNow = P.now.bind(P), nativeDateNow = Date.now;
  var NT = W.setTimeout, NCT = W.clearTimeout, NI = W.setInterval, NCI = W.clearInterval;
  var NRAF = W.requestAnimationFrame, NCAF = W.cancelAnimationFrame;
  var MP = W.HTMLMediaElement && HTMLMediaElement.prototype, nativePlay = MP && MP.play, nativePause = MP && MP.pause;
  var hidden = false, hidAt = 0, total = 0;
  var S = W.__sgPause = { hidden: false, total: 0, count: 0, log: [] };
  var log = function(what){ try { S.log.push([what, Math.round(nativeNow())]); if(S.log.length > 200) S.log.shift(); } catch(e){} };

  /* ---- the page's clock: the real one less every hidden stretch; it stands still while hidden ---- */
  var vnow = function(){ return (hidden ? hidAt : nativeNow()) - total; };
  var lag = function(){ return nativeNow() - vnow(); };                        // how far the page's clock is behind the real one
  P.now = function(){ return vnow(); };
  Date.now = function(){ return nativeDateNow() - lag(); };
  Date.__sgpReal = nativeDateNow;                                               // the wall clock (the lesson's analytics stamps keep it)

  /* ---- timers: held with what they still had to run ---- */
  var seq = 0x40000000, timers = new Map();
  var run = function(t){ if(typeof t.fn === "function") t.fn.apply(W, t.args); else (0, eval)(String(t.fn)); };
  var armT = function(id, t, ms){ t.kind = "to"; t.n = NT.call(W, function(){ t.n = null; if(!timers.has(id)) return; timers.delete(id); run(t); }, ms); };
  var armI = function(id, t){ t.kind = "iv"; t.n = NI.call(W, function(){ t.last = vnow(); run(t); }, t.ms); };
  var armIrest = function(id, t, ms){ t.kind = "to"; t.n = NT.call(W, function(){ t.n = null; if(!timers.has(id)) return; t.last = vnow(); armI(id, t); run(t); }, ms); };
  W.setTimeout = function(fn, ms){
    var id = ++seq, d = Math.max(0, +ms || 0), t = { fn: fn, args: Array.prototype.slice.call(arguments, 2), iv: false, ms: d, due: vnow() + d, n: null };
    timers.set(id, t); if(!hidden) armT(id, t, d); return id; };
  W.setInterval = function(fn, ms){
    var id = ++seq, d = Math.max(0, +ms || 0), t = { fn: fn, args: Array.prototype.slice.call(arguments, 2), iv: true, ms: d, last: vnow(), n: null };
    timers.set(id, t); if(!hidden) armI(id, t); else t.rest = d; return id; };
  W.clearTimeout = W.clearInterval = function(id){
    var t = timers.get(id);
    if(!t){ try { NCT.call(W, id); NCI.call(W, id); } catch(e){} return; }      // a timer from before this layer (none in this page)
    timers.delete(id); if(t.n != null){ (t.kind === "iv" ? NCI : NCT).call(W, t.n); t.n = null; } };
  var holdTimers = function(){ var now = vnow();
    timers.forEach(function(t){ if(t.n == null) return; (t.kind === "iv" ? NCI : NCT).call(W, t.n); t.n = null;
      if(t.iv) t.rest = t.kind === "iv" ? Math.max(0, t.last + t.ms - now) : Math.max(0, t.restDue - now); }); };
  var startTimers = function(){ var now = vnow();
    timers.forEach(function(t, id){ if(t.n != null) return;
      if(!t.iv) armT(id, t, Math.max(0, t.due - now));
      else { var r = t.rest != null ? t.rest : t.ms; t.restDue = now + r; t.rest = null; armIrest(id, t, r); } }); };

  /* ---- animation frames: wait while hidden; the frame time on the page's clock ---- */
  var rseq = 0x40000000, rafs = new Map();
  var armR = function(id, r){ r.n = NRAF.call(W, function(ts){ r.n = null; if(!rafs.has(id) || hidden) return; rafs.delete(id); r.cb(ts - total); }); };
  W.requestAnimationFrame = function(cb){ var id = ++rseq, r = { cb: cb, n: null }; rafs.set(id, r); if(!hidden) armR(id, r); return id; };
  W.cancelAnimationFrame = function(id){ var r = rafs.get(id); if(!r){ try { NCAF.call(W, id); } catch(e){} return; } rafs.delete(id); if(r.n != null){ NCAF.call(W, r.n); r.n = null; } };
  var startFrames = function(){ rafs.forEach(function(r, id){ if(r.n == null) armR(id, r); }); };

  /* ---- Web Animations: start times on the page's clock; paused while hidden ---- */
  try {
    var stD = Object.getOwnPropertyDescriptor(Animation.prototype, "startTime");
    if(stD && stD.get && stD.set) Object.defineProperty(Animation.prototype, "startTime", { configurable: true, enumerable: stD.enumerable,
      get: function(){ var v = stD.get.call(this); return v == null ? v : v - total; },
      set: function(v){ stD.set.call(this, v == null ? v : v + total); } });
    var ctD = W.AnimationTimeline && Object.getOwnPropertyDescriptor(AnimationTimeline.prototype, "currentTime");
    if(ctD && ctD.get) Object.defineProperty(AnimationTimeline.prototype, "currentTime", { configurable: true, enumerable: ctD.enumerable,
      get: function(){ var v = ctD.get.call(this); return v == null ? v : v - lag(); } });
  } catch(e){}
  var heldA = [];
  var isCssAnim = function(a){ return typeof CSSAnimation !== "undefined" && a instanceof CSSAnimation; };   // held by the CSS rule instead (keeps their CSS play-state control)
  var holdAnims = function(){ heldA = [];
    try { D.getAnimations().forEach(function(a){ if(!isCssAnim(a) && a.playState === "running"){ a.pause(); heldA.push(a); } }); } catch(e){} };
  var startAnims = function(){ heldA.forEach(function(a){ try { if(a.playState === "paused") a.play(); } catch(e){} }); heldA = []; };
  var NA = Element.prototype.animate;
  if(NA) Element.prototype.animate = function(){ var a = NA.apply(this, arguments);
    if(hidden){ try { if(a.playState === "running"){ a.pause(); heldA.push(a); } } catch(e){} } return a; };

  /* ---- sounds ---- */
  var media = new Set(), stopped = new Set(), deferred = new Set();
  var quiet = function(m){ if(m.__sgp) return; m.__sgp = { pause: 0, play: 0, playing: 0 };
    ["pause", "play", "playing"].forEach(function(type){
      m.addEventListener(type, function(e){ if(m.__sgp[type] > 0){ m.__sgp[type]--; e.stopImmediatePropagation(); } }, true); }); };
  if(MP){
    MP.play = function(){ media.add(this); quiet(this);
      if(hidden){ deferred.add(this); return Promise.resolve(); }              // asked for while hidden: it starts when the page is seen
      return nativePlay.apply(this, arguments); };
    MP.pause = function(){ deferred.delete(this); stopped.delete(this); return nativePause.apply(this, arguments); };
  }
  var holdMedia = function(){
    var all = new Set(media); try { D.querySelectorAll("audio, video").forEach(function(m){ all.add(m); }); } catch(e){}
    all.forEach(function(m){ if(m.paused || m.ended) return; quiet(m); media.add(m); m.__sgp.pause++; stopped.add(m);
      try { nativePause.call(m); } catch(e){ m.__sgp.pause = 0; } }); };
  var startMedia = function(){
    stopped.forEach(function(m){ m.__sgp.play++; m.__sgp.playing++;          // its own resume: unseen by the engine
      var done = function(){ m.__sgp.play = 0; m.__sgp.playing = 0; };
      try { var p = nativePlay.call(m); if(p && p.then) p.then(done, done); else done(); } catch(e){ done(); } });
    stopped.clear();
    deferred.forEach(function(m){ try { var p = nativePlay.call(m); if(p && p.catch) p.catch(function(){}); } catch(e){} });   // a fresh start: its events go to the engine
    deferred.clear(); };
  var ctxs = [];
  var wrapAC = function(name){ var N = W[name]; if(!N) return;
    try { var C = function(){ var c = Reflect.construct(N, arguments, new.target || C); ctxs.push(c); if(hidden && c.state !== "closed"){ c.__sgpRun = true; c.suspend(); } return c; };
      C.prototype = N.prototype; Object.setPrototypeOf(C, N); W[name] = C; } catch(e){} };
  wrapAC("AudioContext"); if(W.webkitAudioContext && W.webkitAudioContext !== W.AudioContext) wrapAC("webkitAudioContext");
  var holdCtx = function(){ ctxs.forEach(function(c){ if(c.state === "running"){ c.__sgpRun = true; try { c.suspend(); } catch(e){} } }); };
  var startCtx = function(){ ctxs.forEach(function(c){ if(c.__sgpRun){ c.__sgpRun = false; try { c.resume(); } catch(e){} } }); };

  /* ---- hidden / seen ---- */
  var hide = function(){
    if(hidden) return;
    hidden = true; hidAt = nativeNow(); S.hidden = true; S.count++; log("hidden");
    try { holdMedia(); } catch(e){} try { holdCtx(); } catch(e){}
    D.documentElement.classList.add("sgp-hidden"); try { D.getAnimations(); } catch(e){}   // the CSS hold takes effect now (a style flush)
    holdAnims(); holdTimers();
  };
  var show = function(){
    if(!hidden) return;
    total += nativeNow() - hidAt; hidden = false; S.hidden = false; S.total = Math.round(total); log("visible");
    D.documentElement.classList.remove("sgp-hidden"); try { D.getAnimations(); } catch(e){}
    startAnims(); try { startCtx(); } catch(e){} try { startMedia(); } catch(e){}
    startTimers(); startFrames();
  };
  D.addEventListener("visibilitychange", function(){ if(D.visibilityState === "hidden") hide(); else show(); });
  if(D.visibilityState === "hidden") hide();                                  // opened in a background tab: nothing starts until it is seen
})();
