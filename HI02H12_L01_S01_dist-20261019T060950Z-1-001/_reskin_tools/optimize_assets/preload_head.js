/* ===== [preload-head] (2026-11-15) EVERY ASSET FETCHED IN THE BACKGROUND, THEN PLAYED FROM MEMORY =====
   [load-bar-off] (2026-11-16): no loading bar on the cover any more and the play button does not wait for this: the files go on
   loading behind the lesson; a page that needs a file before its fetch is done loads it from its own URL, as without this, and
   goes first: while the page waits for a file (a sound or a picture it loads itself, a fetch of it), no new fetch starts and no
   picture is warmed (yieldTo / yieldFor).
   Written in by optimize.py (build.py's last step) at the very top of app.js, before any engine code makes a sound or a picture.
   MANIFEST = every file under assets/ the lesson can use: [path, bytes on disk, audio length in ms (0 for the rest), 1 = fetched first
   (what the cover itself asks for first: the bird's wave animation, the welcome)].
   - The files are fetched smallest first (the cover's pictures and sounds land in the first seconds, never starved behind the big
     animations), five at a time, each streamed so the progress moves by real bytes (weighted by the sizes on disk, refined by the
     server's Content-Length when the body is not compressed). A transfer that fails, stalls (15 s without a byte) or runs past
     its cap counts as done and its elements keep the file's own URL — nothing can hold the lesson back. Under file:// (fetch is
     blocked there) nothing is fetched or patched at all: the lesson runs exactly as before.
   - A fetched file lives on as a blob: URL. Every picture / sound the page then makes with that file's URL gets the blob instead,
     so "loaded" means local: img.src / audio.src, new Audio(src), and fetch() of the file (the title bird and the gate bird
     fetch theirs). A URL with a query (the cache-busters that restart an animated picture) gets a fresh blob URL each time —
     what restarts it — and, while its file is still on its way, waits for it rather than downloading it a second time. Reading
     .src / .currentSrc gives back the file's own URL, so every check of "which clip is this" keeps working. A blob that fails to
     play reverts to the file's own URL, once (and a sound that was asked to play plays from there). Every picture is also loaded
     once by its own URL after its fetch, so the page's image cache holds it for the uses no src setter sees (style.css, inline
     styles, HTML strings); the preload completes when those are in too.
   window.__preload: done, fraction, whenDone(fn), onProgress(fn), stats(). ===== */
(function(){ "use strict";
  var MANIFEST = __PRELOAD_MANIFEST__;
  var CONC = 5, STALL_MS = 15000, CAP_MIN_MS = 30000, CAP_BYTES_PER_S = 20000;
  var TYPES = { ogg:"audio/ogg", mp3:"audio/mpeg", webp:"image/webp", png:"image/png", gif:"image/gif", svg:"image/svg+xml",
                woff2:"font/woff2", jpg:"image/jpeg", jpeg:"image/jpeg", json:"application/json" };
  var base = document.baseURI;
  var nativeFetch = (typeof window.fetch === "function") ? window.fetch.bind(window) : null;
  var canBlob = !!(nativeFetch && window.Blob && window.URL && URL.createObjectURL && window.Response);
  var active = location.protocol !== "file:" && canBlob;
  function absOf(u){ try { return new URL(String(u), base).href; } catch(e){ return String(u); } }
  function bare(u){ var i = u.search(/[?#]/); return i < 0 ? u : u.slice(0, i); }
  function hasQuery(u){ return /[?#]/.test(String(u)); }

  var entries = [], byKey = new Map(), reverse = new Map(), doneFns = [], progFns = [], warm = [];
  MANIFEST.forEach(function(m){
    var e = { path: m[0], key: bare(absOf(m[0])), bytes: m[1], ms: m[2] || 0, first: !!m[3], want: m[1], got: 0,
              state: "queued", blob: null, url: null, waiters: [] };
    entries.push(e); byKey.set(e.key, e);
  });
  function entryOf(u){ if(u == null || u === "") return null; var s = String(u); if(/^(blob|data):/i.test(s)) return null; return byKey.get(bare(absOf(s))) || null; }

  var P = window.__preload = {
    active: active, done: false, fraction: 0, startedAt: performance.now(), finishedAt: 0, failed: [], reverts: [], deferred: 0, served: 0,
    entry: entryOf,
    durationMs: function(u){ var e = entryOf(u); return e ? e.ms : 0; },
    blobURL: function(u){ var e = entryOf(u); return e && e.url || null; },
    whenDone: function(fn){ if(P.done){ try { fn(); } catch(x){} } else doneFns.push(fn); },
    onProgress: function(fn){ progFns.push(fn); try { fn(P.fraction); } catch(x){} },
    stats: function(){ var s = { files: entries.length, done: 0, failed: 0, loading: 0, queued: 0, streamed: 0, bytes: 0, got: 0 };
      entries.forEach(function(e){ s[e.state === "done" ? "done" : e.state === "failed" ? "failed" : e.state === "loading" ? "loading" : e.state === "streamed" ? "streamed" : "queued"]++; s.bytes += e.want; s.got += Math.min(e.got, e.want); });
      s.fraction = P.fraction; s.done_flag = P.done; s.ms = Math.round((P.finishedAt || performance.now()) - P.startedAt);
      s.failedList = P.failed.slice(); s.reverts = P.reverts.slice(); s.deferred = P.deferred; s.served = P.served; return s; }
  };

  // ---------- progress (monotonic) ----------
  var shown = 0, progQueued = false;
  function progress(){
    var tot = 0, got = 0;
    for(var i = 0; i < entries.length; i++){ var e = entries[i]; tot += e.want; got += Math.min(e.got, e.want); }
    var f = tot ? got / tot : 1; if(f > shown) shown = Math.min(1, f);
    P.fraction = P.done ? 1 : Math.min(shown, 0.999);
    if(progQueued) return; progQueued = true;
    (window.requestAnimationFrame || setTimeout)(function(){ progQueued = false; progFns.forEach(function(fn){ try { fn(P.fraction); } catch(x){} }); });
  }
  function finish(){
    if(P.done) return; P.done = true; P.fraction = 1; P.finishedAt = performance.now();
    progFns.forEach(function(fn){ try { fn(1); } catch(x){} });
    doneFns.splice(0).forEach(function(fn){ try { fn(); } catch(x){} });
    try { window.dispatchEvent(new CustomEvent("preloaddone", { detail: P.stats() })); } catch(x){}
  }
  if(!active || !entries.length){ entries.forEach(function(e){ e.state = "skipped"; }); finish(); return; }

  // ---------- the queue: smallest first, five at a time, a page request jumps it ----------
  var queue = entries.slice().sort(function(a, b){ return (b.first - a.first) || (a.bytes - b.bytes); }), qi = 0, running = 0, settled = 0, warming = 0, hold = 0;   // the cover's own first, then smallest first
  function next(){ if(hold > 0) return; while(warmWait.length) startWarm(warmWait.shift());
    while(running < CONC && qi < queue.length){ var e = queue[qi++]; if(e.state === "queued"){ running++; load(e); } } }
  function bump(e){ if(e && e.state === "queued"){ running++; load(e); } }   // the page needs it now: start it at once
  // [load-bar-off] (2026-11-16) the page first: the lesson can start before the preload is done, and a file the page then waits for
  // must not queue behind the preload's transfers (a browser opens only a few connections per server): while a sound it plays from
  // the network has no data yet (yieldTo) or a file it needs is still on its way (yieldFor: a fetch() of it, a restarted picture, an
  // <img>), no new fetch starts (those in flight finish), until it can play / arrives, fails, or 8 s pass
  var YIELD_MS = 8000, YIELD_EV = ["canplay", "loadeddata", "error"], YIELD_EV_IMG = ["load", "error"];
  function yieldTo(el){
    if(el.__plYield) return; el.__plYield = true; hold++;
    var t = 0, over = false, evs = (el instanceof HTMLImageElement) ? YIELD_EV_IMG : YIELD_EV;
    var end = function(){ if(over) return; over = true; clearTimeout(t); el.__plYield = false; hold--;
      evs.forEach(function(n){ el.removeEventListener(n, end); }); next(); };
    evs.forEach(function(n){ el.addEventListener(n, end); }); t = setTimeout(end, YIELD_MS);
  }
  function yieldFor(e){
    if(!e || e.__plYield || (e.state !== "queued" && e.state !== "loading")) return; e.__plYield = true; hold++;
    var t = 0, over = false;
    var end = function(){ if(over) return; over = true; clearTimeout(t); e.__plYield = false; hold--; next(); };
    e.waiters.push(end); t = setTimeout(end, YIELD_MS);
  }
  // a file the page streams itself from its URL for good (the music bed, when it is asked to play before its fetch began) is not
  // fetched as well: it counts as in
  function streamed(e){ if(!e || e.state !== "queued") return; e.state = "streamed"; e.got = e.want; settled++; progress(); maybeFinish(); }
  function maybeFinish(){ if(settled >= entries.length && warming === 0) finish(); }
  // a picture is also loaded once by its own URL (the file is in the HTTP cache by now: a revalidation at most), so the page's image
  // cache holds it for every use the src patch cannot see: style.css, inline styles, HTML strings
  var warmWait = [];
  function warmImage(e){ warming++; if(hold > 0) warmWait.push(e); else startWarm(e); }   // [load-bar-off] not while the page waits for a file
  function startWarm(e){
    var im = new Image(), t = 0, over = false;
    var end = function(){ if(over) return; over = true; clearTimeout(t); warming--; maybeFinish(); };
    im.onload = end; im.onerror = end; t = setTimeout(end, STALL_MS);
    try { imgSrc.set.call(im, e.path); warm.push(im); } catch(x){ end(); }
  }
  function settle(e){
    running--; settled++;
    if(e.blob){ try { e.url = URL.createObjectURL(e.blob); reverse.set(e.url, e.key); } catch(x){ e.url = null; } }
    if(e.url && /^image\//.test(e.blob.type)) warmImage(e);
    if(e.url && /\.woff2$/i.test(e.path)) warmFont(e);
    e.waiters.splice(0).forEach(function(w){ try { w(); } catch(x){} });
    progress();
    next(); maybeFinish();
  }
  function load(e){
    e.state = "loading";
    var ctl = window.AbortController ? new AbortController() : null, over = false, stall = 0, cap = 0, cl = 0, enc = null;
    function clearT(){ clearTimeout(stall); clearTimeout(cap); }
    function fail(why){ if(over) return; over = true; clearT(); try { if(ctl) ctl.abort(); } catch(x){}
      e.state = "failed"; e.got = e.want; P.failed.push(e.path + " (" + why + ")"); settle(e); }
    function ok(blob){ if(over) return; over = true; clearT(); e.state = "done"; e.blob = blob; e.got = e.want; settle(e); }
    function armStall(){ clearTimeout(stall); stall = setTimeout(function(){ fail("stalled"); }, STALL_MS); }
    cap = setTimeout(function(){ fail("timeout"); }, CAP_MIN_MS + e.bytes / CAP_BYTES_PER_S * 1000);
    armStall();
    var type = TYPES[(e.path.split(".").pop() || "").toLowerCase()] || "";
    nativeFetch(e.path, { signal: ctl ? ctl.signal : undefined, credentials: "same-origin" }).then(function(res){
      if(over) return;
      if(!res.ok){ fail("HTTP " + res.status); return; }
      cl = +(res.headers.get("content-length") || 0); enc = res.headers.get("content-encoding");
      if(cl > 0 && !enc && cl !== e.want){ e.want = cl; }
      type = type || res.headers.get("content-type") || "";
      if(!res.body || !res.body.getReader){ return res.blob().then(function(b){ ok(type ? new Blob([b], { type: type }) : b); }); }
      var reader = res.body.getReader(), parts = [], n = 0;
      var pump = function(){ return reader.read().then(function(r){
        if(over){ try { reader.cancel(); } catch(x){} return; }
        if(r.done){ if(cl > 0 && !enc && n !== cl){ fail("short body " + n + "/" + cl); return; } ok(new Blob(parts, { type: type })); return; }
        parts.push(r.value); n += r.value.byteLength; e.got = n; armStall(); progress(); return pump(); }); };
      return pump();
    }).catch(function(err){ fail((err && err.name) || "error"); });
  }
  function warmFont(e){
    try { var name = decodeURIComponent(e.path.split("/").pop());
      [].forEach.call(document.styleSheets, function(sh){ var rules; try { rules = sh.cssRules; } catch(x){ return; }
        [].forEach.call(rules || [], function(r){ if(!(window.CSSFontFaceRule && r instanceof CSSFontFaceRule)) return;
          var src = r.style.getPropertyValue("src") || ""; if(src.indexOf(name) < 0) return;
          var fam = (r.style.getPropertyValue("font-family") || "").trim(), wt = (r.style.getPropertyValue("font-weight") || "400").trim().split(/\s+/)[0];
          if(fam && document.fonts && document.fonts.load) document.fonts.load(wt + " 32px " + fam).catch(function(){}); }); });
    } catch(x){}
  }

  // ---------- the resolver: a fetched file's URL -> its blob ----------
  function freshURL(e, origAbs){ var u = URL.createObjectURL(e.blob); reverse.set(u, origAbs); return u; }
  function blobFor(u){ var e = entryOf(u); if(!e || e.state !== "done" || !e.url) return null; P.served++;
    return hasQuery(u) ? freshURL(e, absOf(u)) : e.url; }
  function patchSrc(proto, isMedia){
    var d = Object.getOwnPropertyDescriptor(proto, "src"), dc = Object.getOwnPropertyDescriptor(proto, "currentSrc");
    if(!d || !d.get || !d.set) return d;
    Object.defineProperty(proto, "src", { configurable: true, enumerable: d.enumerable,
      get: function(){ if(this.__plPending) return this.__plPending; var v = d.get.call(this), o = reverse.get(v); return o !== undefined ? o : v; },
      set: function(v){
        var el = this, s = String(v), e = entryOf(s);
        el.__plTok = (el.__plTok || 0) + 1; el.__plPending = null;
        if(!e){ d.set.call(el, v); return; }
        if(e.state === "done" && e.url){ var b = blobFor(s); el.__plReverted = false; armEl(el); d.set.call(el, b); return; }
        // a file still on its way: a sound that does not want its data yet (preload="none") or a restart URL of a picture waits
        // for it rather than downloading it twice (the picture's fetch moves to the front); a sound wanted now loads from its own URL
        // as before (Chrome refuses play() on an element with no source at once), and so does a waiting sound the moment the page
        // wants its data (streamNow)
        if(((isMedia && el.preload === "none") || (!isMedia && hasQuery(s))) && (e.state === "queued" || e.state === "loading")){
          var tok = el.__plTok; el.__plPending = absOf(s); P.deferred++;
          if(!isMedia){ bump(e); yieldFor(e); }
          e.waiters.push(function(){ if(el.__plTok !== tok) return; el.__plPending = null; var b2 = blobFor(s); if(b2){ el.__plReverted = false; armEl(el); d.set.call(el, b2); } else d.set.call(el, s); });
          return; }
        // [load-bar-off] a picture or a sound the page loads itself goes first: the preload pauses until it is in (a picture is no longer
        // turned into a fetch at the front: as before the preloader, it loads at the browser's own priority, a picture in view first)
        if(e.state === "queued" || e.state === "loading") yieldTo(el);
        d.set.call(el, v);
      } });
    if(dc && dc.get) Object.defineProperty(proto, "currentSrc", { configurable: true, enumerable: dc.enumerable,
      get: function(){ var v = dc.get.call(this), o = reverse.get(v); return o !== undefined ? o : v; } });
    return d;
  }
  var imgSrc = patchSrc(HTMLImageElement.prototype, false);
  var mediaSrc = patchSrc(HTMLMediaElement.prototype, true);
  function srcDesc(el){ return (el instanceof HTMLImageElement) ? imgSrc : mediaSrc; }

  // [load-bar-off] (2026-11-16) a sound waiting for its fetch stops waiting when the page wants its data — it is asked to play, or its
  // preload is turned on (the music bed reads ahead from the start, as it did before the preloader): it streams from its own URL at
  // once and goes first (yieldTo); a fetch not begun yet is dropped (the element streams the file itself)
  function streamNow(el){ var u = el.__plPending; if(!u || !mediaSrc) return;
    el.__plTok = (el.__plTok || 0) + 1; el.__plPending = null; streamed(entryOf(u)); yieldTo(el); mediaSrc.set.call(el, u); }
  var preloadDesc = Object.getOwnPropertyDescriptor(HTMLMediaElement.prototype, "preload");
  if(preloadDesc && preloadDesc.get && preloadDesc.set) Object.defineProperty(HTMLMediaElement.prototype, "preload", { configurable: true, enumerable: preloadDesc.enumerable,
    get: function(){ return preloadDesc.get.call(this); },
    set: function(v){ preloadDesc.set.call(this, v);
      if(this.__plPending && String(v).toLowerCase() !== "none"){ var e = entryOf(this.__plPending); if(e && e.state === "queued") streamNow(this); } } });   // in flight: its blob comes soon

  // a blob that fails reverts to the file's own URL, once; the page's own error handlers never see that failure
  function onErr(ev){
    var el = ev.target; if(!el || el.__plReverted || !(el instanceof HTMLImageElement || el instanceof HTMLMediaElement)) return;
    var d = srcDesc(el); if(!d) return;
    var cur = d.get.call(el), orig = reverse.get(cur); if(orig === undefined) return;
    el.__plReverted = true; ev.stopImmediatePropagation(); P.reverts.push(orig);
    d.set.call(el, orig);
    if(el instanceof HTMLMediaElement && el.__plWantPlay && !el.__plPlayPending){ try { var pr = nativePlay.call(el); if(pr && pr.catch) pr.catch(function(){}); } catch(x){} }
  }
  document.addEventListener("error", onErr, true);
  function armEl(el){ if(el.__plArmed) return; el.__plArmed = true; el.addEventListener("error", onErr, true); }   // detached elements (new Audio) too

  // new Audio(src) goes through the patched setter
  var NA = window.Audio;
  if(NA){ var PA = function Audio(src){ var a = new NA(); if(arguments.length && src !== undefined) a.src = src; return a; };
    PA.prototype = NA.prototype; window.Audio = PA; }

  // play(): a sound whose blob had to revert plays from the file's own URL
  var HP = HTMLMediaElement.prototype, nativePlay = HP.play, nativePause = HP.pause;
  HP.play = function(){
    var el = this; el.__plWantPlay = true;
    if(el.__plPending) streamNow(el);   // [load-bar-off] a sound still waiting for its fetch plays from its own URL at once
    var p = nativePlay.apply(el, arguments);
    if(!p || typeof p.then !== "function" || !mediaSrc || reverse.get(mediaSrc.get.call(el)) === undefined) return p;
    el.__plPlayPending = (el.__plPlayPending || 0) + 1;
    return p.then(function(v){ el.__plPlayPending--; return v; }, function(err){ el.__plPlayPending--;
      if(el.__plReverted && err && (err.name === "AbortError" || err.name === "NotSupportedError")) return nativePlay.call(el);
      throw err; });
  };
  HP.pause = function(){ this.__plWantPlay = false; return nativePause.apply(this, arguments); };

  // fetch() of a fetched (or queued) file: answered from memory, never downloaded twice
  function blobResponse(e){ return new Response(e.blob, { status: 200, statusText: "OK", headers: { "Content-Type": e.blob.type || "application/octet-stream" } }); }
  window.fetch = function(input, init){
    try {
      var m = (init && init.method) || (input && typeof input === "object" && input.method) || "GET";
      if(String(m).toUpperCase() === "GET"){
        var u = typeof input === "string" ? input : (input && input.url) || String(input), e = entryOf(u);
        if(e && (e.state === "done" || e.state === "queued" || e.state === "loading")){
          P.served++;
          if(e.state === "done" && e.blob) return Promise.resolve(blobResponse(e));
          bump(e); yieldFor(e);
          return new Promise(function(res, rej){ e.waiters.push(function(){ if(e.blob) res(blobResponse(e)); else nativeFetch(input, init).then(res, rej); }); });
        }
      }
    } catch(x){}
    return nativeFetch.apply(window, arguments);
  };

  next();
})();
/* ===== [preload-head] end ===== */
