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
  var MANIFEST = [["assets/Audio/bgm_letter_nostalgia.ogg",195601,25800,0],["assets/Audio/sfx_celebrate.ogg",11465,1096,0],["assets/Audio/sfx_correct_new.ogg",10105,856,0],["assets/Audio/sfx_demo1_pop.ogg",10282,726,0],["assets/Audio/sfx_demo2_sharp_pop.ogg",12358,1025,0],["assets/Audio/sfx_fb_correct.ogg",21530,1326,0],["assets/Audio/sfx_g3_rope.ogg",22901,1882,0],["assets/Audio/sfx_g4_giggle.ogg",8539,1062,0],["assets/Audio/sfx_letter_magic.ogg",49281,4006,0],["assets/Audio/sfx_letter_paper.ogg",17395,1736,0],["assets/Audio/sfx_letter_pop.ogg",31309,2118,0],["assets/Audio/sfx_next_button.ogg",1529,106,0],["assets/Audio/sfx_p1_book.ogg",14561,1104,0],["assets/Audio/sfx_p2_pencils.ogg",129840,17300,0],["assets/Audio/sfx_play_button.ogg",3488,429,0],["assets/Audio/sfx_stamp_glitter.ogg",19970,1306,0],["assets/Audio/sfx_stamp_pop.ogg",5331,626,0],["assets/Audio/sfx_stamp_press.ogg",9532,1162,0],["assets/Audio/sfx_stamp_whoosh.ogg",3670,556,0],["assets/Audio/sfx_star_pop_new.ogg",3537,432,0],["assets/Audio/sfx_story_cat.ogg",8528,895,0],["assets/Audio/sfx_title_badge.ogg",22228,1494,0],["assets/Audio/sfx_wrong_new.ogg",6659,749,0],["assets/Audio/standard_background_music_2.ogg",2377336,240030,0],["assets/Audio/vo_build_hint1.ogg",36824,4006,0],["assets/Audio/vo_build_hint2.ogg",87998,9646,0],["assets/Audio/vo_build_hint3.ogg",28194,3246,0],["assets/Audio/vo_demo1_explain.ogg",47317,5006,0],["assets/Audio/vo_demo1_intro.ogg",57233,6406,0],["assets/Audio/vo_demo1_sent.ogg",21099,2566,0],["assets/Audio/vo_demo2_explain.ogg",55219,5966,0],["assets/Audio/vo_demo2_sent.ogg",17767,2086,0],["assets/Audio/vo_demo3_explain.ogg",80264,8606,0],["assets/Audio/vo_demo3_sent.ogg",45784,4966,0],["assets/Audio/vo_g1_intro.ogg",39894,4166,0],["assets/Audio/vo_g1_sent.ogg",22378,2486,0],["assets/Audio/vo_g2_sent.ogg",22976,1886,0],["assets/Audio/vo_g3_sent.ogg",42145,4406,0],["assets/Audio/vo_g4_hint1.ogg",36639,4086,0],["assets/Audio/vo_g4_hint2.ogg",33270,3486,0],["assets/Audio/vo_g4_o1.ogg",21392,2446,0],["assets/Audio/vo_g4_o2.ogg",40888,4726,0],["assets/Audio/vo_g4_o3.ogg",65962,5406,0],["assets/Audio/vo_g4_prompt.ogg",44279,4846,0],["assets/Audio/vo_landing.ogg",65671,7086,1],["assets/Audio/vo_letter_intro.ogg",94628,9966,0],["assets/Audio/vo_ok.ogg",22163,1806,0],["assets/Audio/vo_ok_pick.ogg",25431,2966,0],["assets/Audio/vo_p1_hint1.ogg",44346,4766,0],["assets/Audio/vo_p1_hint2.ogg",38748,4246,0],["assets/Audio/vo_p1_o1.ogg",20563,2206,0],["assets/Audio/vo_p1_o2.ogg",24415,2806,0],["assets/Audio/vo_p1_o3.ogg",30890,3366,0],["assets/Audio/vo_p1_prompt.ogg",47142,5046,0],["assets/Audio/vo_p2_hint1.ogg",35724,4006,0],["assets/Audio/vo_p2_hint2.ogg",53198,5646,0],["assets/Audio/vo_p2_o1.ogg",50059,5766,0],["assets/Audio/vo_p2_o2.ogg",50381,5766,0],["assets/Audio/vo_p2_o3.ogg",47999,5326,0],["assets/Audio/vo_p2_prompt.ogg",46040,4966,0],["assets/Audio/vo_pick_hint3.ogg",28336,3166,0],["assets/Audio/vo_pt_guided.ogg",50231,5526,0],["assets/Audio/vo_pt_practice.ogg",29831,2446,0],["assets/Audio/vo_pt_tutorial.ogg",48215,5366,0],["assets/Audio/vo_recap_alp_eg.ogg",43015,4846,0],["assets/Audio/vo_recap_alp_name.ogg",13079,1526,0],["assets/Audio/vo_recap_alp_when.ogg",65308,6846,0],["assets/Audio/vo_recap_intro.ogg",42279,4566,0],["assets/Audio/vo_recap_prashn_eg.ogg",27146,3086,0],["assets/Audio/vo_recap_prashn_name.ogg",16480,1846,0],["assets/Audio/vo_recap_prashn_when.ogg",39505,4166,0],["assets/Audio/vo_recap_purn_eg.ogg",32992,3646,0],["assets/Audio/vo_recap_purn_name.ogg",11896,1446,0],["assets/Audio/vo_recap_purn_when.ogg",35762,3766,0],["assets/Audio/vo_stamp1_hint2.ogg",70835,7566,0],["assets/Audio/vo_stamp1_hint3.ogg",74404,8046,0],["assets/Audio/vo_stamp2_hint2.ogg",61050,6646,0],["assets/Audio/vo_stamp2_hint3.ogg",102592,10486,0],["assets/Audio/vo_stamp3_hint2.ogg",63160,6806,0],["assets/Audio/vo_stamp3_hint3.ogg",55764,6446,0],["assets/Audio/vo_stamp3_intro.ogg",47897,5246,0],["assets/Audio/vo_stamp4_hint2.ogg",34450,3846,0],["assets/Audio/vo_stamp4_hint3_alp.ogg",43488,4766,0],["assets/Audio/vo_stamp4_hint3_prashn.ogg",52346,5566,0],["assets/Audio/vo_stamp4_hint3_purn.ogg",38654,4126,0],["assets/Audio/vo_stamp4_intro.ogg",51897,5566,0],["assets/Audio/vo_stamp_intro.ogg",43790,4886,0],["assets/Audio/vo_stamp_sent.ogg",25962,2806,0],["assets/Audio/vo_stamp_sent2.ogg",60852,6206,0],["assets/Audio/vo_stamp_sent3.ogg",26760,2926,0],["assets/Audio/vo_stamp_sent4.ogg",37728,4326,0],["assets/Audio/vo_stamp_sent5.ogg",107526,11566,0],["assets/Audio/vo_story_b1.ogg",36019,4006,0],["assets/Audio/vo_story_b2.ogg",32179,3686,0],["assets/Audio/vo_story_b3.ogg",30446,3566,0],["assets/Audio/vo_story_b4.ogg",30507,3486,0],["assets/Audio/vo_story_c1.ogg",22504,2646,0],["assets/Audio/vo_story_c2.ogg",24517,2846,0],["assets/Audio/vo_story_moral.ogg",72503,7566,0],["assets/Audio/vo_story_r0.ogg",24099,2726,0],["assets/Audio/vo_story_r1.ogg",109454,11606,0],["assets/Audio/vo_story_s0.ogg",21669,2326,0],["assets/Audio/vo_well_done.ogg",35057,3846,0],["assets/Images/img_demo1_girl_walk.webp",129610,0,0],["assets/Images/img_demo1_hall.webp",28872,0,0],["assets/Images/img_demo2_bubble.svg",2370,0,0],["assets/Images/img_demo2_girl_ask.webp",173918,0,0],["assets/Images/img_demo2_room.webp",22320,0,0],["assets/Images/img_demo3_girl_basket.webp",172726,0,0],["assets/Images/img_demo3_park.webp",63096,0,0],["assets/Images/img_g1_girl_ball2.webp",199696,0,0],["assets/Images/img_g1_room.webp",20004,0,0],["assets/Images/img_g2_girl_bag2.webp",185124,0,0],["assets/Images/img_g2_street.webp",38296,0,0],["assets/Images/img_g3_garden.webp",57334,0,0],["assets/Images/img_g3_garden_bare.webp",249898,0,0],["assets/Images/img_g3_girl_efill.webp",460,0,0],["assets/Images/img_g3_girl_eiris.webp",6376,0,0],["assets/Images/img_g3_girl_point.webp",179748,0,0],["assets/Images/img_g3_plant_jasmine.webp",30830,0,0],["assets/Images/img_g3_plant_marigold.webp",27476,0,0],["assets/Images/img_g3_plant_rose.webp",29516,0,0],["assets/Images/img_g4_kite.webp",138020,0,0],["assets/Images/img_letter_blur_t.webp",30030,0,0],["assets/Images/img_letter_cloud_clean.webp",4158,0,0],["assets/Images/img_letter_cloud_grandpa.webp",101930,0,0],["assets/Images/img_letter_env_body.webp",307080,0,0],["assets/Images/img_letter_env_flap.webp",148396,0,0],["assets/Images/img_letter_env_heart.webp",48180,0,0],["assets/Images/img_letter_env_inner.webp",32710,0,0],["assets/Images/img_letter_scene_t.webp",1264210,0,0],["assets/Images/img_letter_scene_w.webp",1241662,0,0],["assets/Images/img_p1_book.webp",206912,0,0],["assets/Images/img_p2_pencils.webp",181186,0,0],["assets/Images/img_recap_house.webp",159050,0,0],["assets/Images/img_recap_mango.webp",164652,0,0],["assets/Images/img_recap_paint.webp",291630,0,0],["assets/Images/img_stamp8_a_bg.webp",98002,0,0],["assets/Images/img_stamp8_a_danda.webp",54046,0,0],["assets/Images/img_stamp8_a_glow_danda.webp",21890,0,0],["assets/Images/img_stamp8_a_glow_quest.webp",22358,0,0],["assets/Images/img_stamp8_a_post.webp",6856,0,0],["assets/Images/img_stamp8_a_quest.webp",59866,0,0],["assets/Images/img_stamp8_a_text.webp",51902,0,0],["assets/Images/img_stamp8_a_tray.webp",224838,0,0],["assets/Images/img_stamp8_bird.webp",1025912,0,0],["assets/Images/img_stamp8_card.webp",116422,0,0],["assets/Images/img_stamp8_comma.webp",37638,0,0],["assets/Images/img_stamp8_danda.webp",47540,0,0],["assets/Images/img_stamp8_post.webp",25986,0,0],["assets/Images/img_stamp8_question.webp",41986,0,0],["assets/Images/img_stamp8_tray.webp",226660,0,0],["assets/Images/img_stamp8_wood.webp",80106,0,0],["assets/Images/img_stamp_final_blur.webp",31736,0,0],["assets/Images/img_stamp_final_pinki.webp",1272972,0,0],["assets/Images/img_story_pinki_ask.webp",134246,0,0],["assets/Images/img_story_pinki_cat.webp",141934,0,0],["assets/Images/img_story_pinki_listen.webp",142796,0,0],["assets/Images/img_story_pinki_maa.webp",159114,0,0],["assets/UI/bgdeco_spark.svg",220,0,0],["assets/UI/bgdeco_star.svg",391,0,0],["assets/UI/bgdeco_star_o.svg",448,0,0],["assets/UI/btn-next-arrow.svg",408,0,0],["assets/UI/btn-next-disabled-arrow.svg",417,0,0],["assets/UI/btn-next-disabled-pill.svg",588,0,0],["assets/UI/btn-next-disabled.svg",673,0,0],["assets/UI/btn-next-pill.svg",1268,0,0],["assets/UI/btn-next.svg",1271,0,0],["assets/UI/btn-play.svg",2645,0,0],["assets/UI/cel_idle.webp",651146,0,0],["assets/UI/cel_shabaash.webp",684852,0,0],["assets/UI/cel_talk.webp",650742,0,0],["assets/UI/demo1_head.webp",47908,0,0],["assets/UI/end_screen.webp",11284,0,0],["assets/UI/loader.webp",223334,0,0],["assets/UI/new_landing_swiftee_anim.webp",1837700,0,1],["assets/UI/nudge_hand_new.svg",6873,0,0],["assets/UI/peeking_talk_up.webp",1561680,0,0],["assets/UI/start_card.webp",2070,0,0],["assets/UI/start_mascot.webp",56946,0,0],["assets/UI/startnew_bg_plain.webp",16514,0,0],["assets/UI/story_font_baloo2_800.woff2",74512,0,0],["assets/UI/story_grid.svg",12700,0,0],["assets/UI/sw_head_celebrate_anim.webp",390546,0,0],["assets/UI/sw_head_hint_anim.webp",435706,0,0],["assets/UI/sw_head_talking.webp",37384,0,0],["assets/UI/sw_head_tryagain_anim.webp",429222,0,0],["assets/UI/title_bg.webp",15464,0,0],["assets/UI/title_char_comma.webp",113316,0,0],["assets/UI/title_char_comma_rig.webp",48232,0,0],["assets/UI/title_char_purn.webp",43890,0,0],["assets/UI/title_char_purn_rig.webp",17994,0,0],["assets/UI/title_char_question.webp",87746,0,0],["assets/UI/title_char_question_rig.webp",26336,0,0],["assets/UI/title_scene.webp",35614,0,0],["assets/UI/title_shadow_1.svg",691,0,0],["assets/UI/title_shadow_2.svg",691,0,0],["assets/UI/title_shadow_3.svg",687,0,0],["assets/UI/title_swiftie_hello.webp",40374,0,0]];
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
  EVIDENCE_QA: "mcq", BUILD_PUNCT: "build", SORT_QTYPE: "drag", SORT_WORDS: "drag", PUNCT_PICK: "mcq", SENT_PICK: "mcq",   /* [reskin] this lesson's answerable types */
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
  if(window.__bgm) return;   // [dun-chrome] the bed owns its volume (BGM-DUCK)
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
/* [tap-lock] is a sound effect sounding? The picks (G1-G3) and the sentence picks (G4 / P1 / P2) take no tap while an effect
   or a feedback line plays; each effect path marks itself busy for its length (a 6 s cap in case 'ended' never comes). */
let _sfxBusy = 0, _sfxUntil = 0;
function sfxTrack(a){ if(!a) return; let done = false; const end = ()=>{ if(done) return; done = true; _sfxBusy = Math.max(0, _sfxBusy - 1); };
  _sfxBusy++; a.addEventListener("ended", end, { once: true }); a.addEventListener("error", end, { once: true }); setTimeout(end, 6000); }
function sfxBusy(){ return _sfxBusy > 0 || performance.now() < _sfxUntil; }
function playSfx(id){
  if(!id) return;
  try{
    const a = new Audio("assets/Audio/" + id + "." + AUDIO_EXT);
    sfxTrack(a);   // [tap-lock]
    a.volume = 0.7;
    a.play().catch(()=>{});
  }catch(e){}
}
/* ---------- game-feel: procedural SFX (no audio files) + success particle burst ----------
   WebAudio resumes on the first user tap (autoplay policy), so taps/answers always sound. */
let _juiceAC = null;
function _ac(){ if(!_juiceAC){ try{ _juiceAC = new (window.AudioContext || window.webkitAudioContext)(); }catch(e){} }
  if(_juiceAC && _juiceAC.state === "suspended"){ try{ _juiceAC.resume(); }catch(e){} } return _juiceAC; }
function _tone(freqs, type, dur, vol){ _sfxUntil = Math.max(_sfxUntil, performance.now() + dur * 1000);   // [tap-lock]
  const c = _ac(); if(!c) return; const t0 = c.currentTime;
  freqs.forEach((f, i)=>{ const o = c.createOscillator(), g = c.createGain(); o.type = type; o.frequency.value = f;
    const t = t0 + i*(dur/freqs.length); g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t+0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur/freqs.length); o.connect(g).connect(c.destination); o.start(t); o.stop(t + dur/freqs.length); }); }
const sfxTap       = ()=> _tone([520], "sine", 0.09, 0.09);
const _kitSfx = Object.create(null);
function playKitSfx(name, file, volume){ if(isMuted) return; try{
  let a = _kitSfx[name]; if(!a){ a = _kitSfx[name] = new Audio("assets/Audio/" + file); a.preload = "auto"; }
  a.volume = volume == null ? .85 : volume; a.currentTime = 0;
  sfxTrack(a);   // [tap-lock]
  const p = a.play(); if(p && p.catch) p.catch(()=>{});
}catch(e){} }
const sfxCorrect   = ()=> playKitSfx("correct", "sfx_correct_new.ogg", .85);
const sfxWrongSoft = ()=> playKitSfx("wrong", "sfx_wrong_new.ogg", .85);
const sfxConfetti  = ()=> playKitSfx("confetti", "sfx_celebrate.ogg", .45);   // [dun-chrome] STD_SFX_VOL.confetti
const sfxPlayButton = ()=> playKitSfx("playButton", "sfx_play_button.ogg", .8);   // [dun-chrome] STD_SFX_VOL.play
const sfxNextButton = ()=> playKitSfx("nextButton", "sfx_next_button.ogg", .9);   // [dun-chrome] STD_SFX_VOL.next
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
const POP_SFX = "data:audio/ogg;base64,T2dnUwACAAAAAAAAAACvifmAAAAAAASzxYoBE09wdXNIZWFkAQE4AYC7AAAAAABPZ2dTAAAAAAAAAAAAAK+J+YABAAAA5zIhqwE+T3B1c1RhZ3MNAAAATGF2ZjYyLjEyLjEwMgEAAAAdAAAAZW5jb2Rlcj1MYXZjNjIuMjguMTAyIGxpYm9wdXNPZ2dTAAR4OQAAAAAAAK+J+YACAAAAdy3dVxP/JP8EwpiUhL5+g4RpfXRzwP8N+H9sEh+61nWV/ZQk7KAJ347pbk/x/AiGEJFde4bt0kLXU4MBGA4dsUaRH77KZDePkX+mch5Y2IGNlwOqsiuosT9mrWVzHMds6LgJ/qYTn+3DW9jnda/htWEy3XDin9b/v1mEhIRRGp/I/VV6HOnanoM4Z7Xh9HNu98/0vLsfxGvelYJg2AAAAAAAAAAAAAAAAAAAAAAAAAxrpFqnM0hZUu03Jur+CEm1KKedOrFfaSVdYxXrQWCkmhzJMRggbBt2v+Xj2jLl/25LnoNRVau1X/HNTWoCC7mLqmA/EE8E+H45waxwEt40gcM5THQK0lF9glxoiUry6F4VMhMvF/CL8uwMASOeAcdT+gQ0gQ0gUv/S/9L/0cz/S/9MABc+NOwDvssZ+J/xH9VqWIsjzfQ21gdiKDq8kRFC2gG1FAY0bqrP/+IoyRLhCIvkRBapr6ukmrLf8jDxBc4Pm9b5o0uqtBff2Zja3iyu6/YP1WvS0DRGfQKFVEy4mKf5QhSHnHLNyLi/wyVtOLcRJsHwxht8aGWgQZBrmgP+FKA2oZ3AkWRwAvzktF6KmuMuLiGhOBwioVOEXq1fM4iaFdIY3p5cUWCKNFShHEFVmGv5SFAB+YISCmcIkCCC8aKhtL6nYnBZP/jeYg5e9Zu8rWTwYV+kP9q6Vea6bwIF1dm+pKqQh9Eiq0C9bFLwVXEsfm2FED0nDzoVJyIn00vR+DkznMeoVYEL5VJeWfhTh9XBi7nP12+BslGunFJUDuBTF1XRexrP6Vy9/9Ry96vtwgvfPV6FslCt2RUDllTIogJNiuUD29yTn/H2ztKfwxrqwqe51+Cf7gwcQxAE8mDavK5YLPi9oJBb1J0fzSqqroa93T4ccNxg+lnUS1LueJFahQaOjUE0ea2Z0pnnVnstjrgb5+ybJJqjvx8kLxQHEJgNoHcDVvVXjtFcwA36BGypieImnhNuRtwbgxYf3JlXmOCBDcxkIWR2kVX2mlmC+EN5pEnBKmm0zcZGHfl4FfNrVB5zZOLWmiumNDukqA9c/6D+e8tpPqgGp4RT3x+dUrBsbYBITsK9Z3+uyjcMXLW/JJeyuoI3jHo6A6FfoasA+LG//cIYTTIcjI7yDO8tb10+/0cUDWblCAk9E5fjtZ0Wp9hIwiUNnvZBuhWnFGE0LVoLKYQZvdXAGtQLUrpGF8C3yeqMfDv4UWd6/a+Un3PkiqMayPmpTim+LYmSIRyw0cikPnfHpIqiE5mXN6YXeq7kZwo/5AMtNLprFhKRsb8QwfR9XW28oM14NwdKIGbV/SasDsIG2kuHFEzuo8M2nZESCwcfAWaExVPxbmc/bxayiVf7Eq8XlH3K3cLddGlZZtpkJUEZ/CB0Si+kSuc/gUl+GFi0M+qFTdbj+FKHGP45Jeza2vnyUdD9UxDsp/JRqTB6tP2HjdmezYrsc+2poPPEDCYiGSnl+B/EF+hezQl2OcwgT/zQ0PLglCEtOdE1KETDgezqX48NzIO0zMi7QX+V9AK3oSahF3krqdyXYfsxcd3VEVERa5DvI8RqN+r+f0xFOEXYUMe8R3dnDMW9+FHoUjPz9Jr3D+TElm/2AtSbqVzFmUDrP7+cbL33YrnWL9Hb4Rv8PUxWyhLM6hhXSwDPUivbbypD2WuMyh8cM/oFov+W0cjJsaAAZuhSBxmz17scIuJDltKOfGKlDJD8Qbm0L0NIP6YHtH5mcmgfbhipPsxB8vo+jQfdX/Hco1x4Ceu9sieRfTcLecXLQ/sATQzSe7ZAOEskexqO8n7Yn1AiI3Uzqgy2tESNhh5jlfpMmEOBd2Yb/elOZ6jrUvhT8dO2ayhFnSiLfh1BgBRnP3sjVWz7J9WpezyO0RtYf7eotxMNFjRqe+506G9C2w5m8gzZbiiCp1sTrV1pTFoEcCvRxYvUx4kLIdMGbdUhQug1k8+hvG04ZhcwOuNSBsZNbCULmrMLHJt/UzsUhs+AY3CeubftO4eq2l4YePhapNDCedQwOzY+1C+maKM2vNWUoA6IQ5ODbwpgXF+/TOTLuXu+pPjPIcwmE+a9nXqLoMzBMsAqL13e1cJ1ORjtjvrgFppUdIB1O84km3OmdptonShVoDLsBkXcXRSoFtOSJsaWHJVgWFNMl2h8z2tTJrCsfPvEGU3Nv2DxPXBJtciO+FnqFEknokuxyUhq/i4UVybAV6iVuBiYo3m9YSyHDgnOH7XtbfSStsdUBpO2ER4yHCmkhCg03YP5FuBgqNUjvUhqWd4vRMnIjxIcMOFC0lJaxGCfdzokYBs9MgWyiOl9ooXo4qmnljqlajW/bKw78A9oDQ6idXyP27Zc82LHNPzklxqV+FqWBRzBla7b1ed1zvRr6S0gTM7vha7QsnkjSVxI85t9bvOcqzVUAgQk4QRQKu23Z1vjMPUk64apoDK5bX5XkSQprsOOYGPtLbLcNPKkwmmHMYnqPq8I/Xmskfe7S/y0d/yfH3SwBFqy+FqY1RlxWyCBUd0eWJXUPDD/JlLY+CJowbXhZEdvtwTMPf0zk3rMYSuAgcuShB5Ltyi+qiNgngtJ/QEDpLG+QiRIlH+8b06jqTaCgYRWH1Ny5LGZRwNZdPPH2jM1uFkIf/VGhuZJNqLCCqs8xI0SEKoWHpW+Wza3nkex03H4XiqApemTzGFIwsk0RfBK2c4/hfsL3Sq1+7b4SMxxDqFu3mIpPpwylcNkExk0S5NkJr2uPeKEN92Y/RYGSoe52TIr+2Oq3zYHaRwgTby0Hla/JeS0wnWVdEDW1xtan67ooE9hU1AMfHoa1UtJvTzBuLN+FPheweHuGiLKL06t14KdDHF5v39s4+raqSTbL6HMl8alfwqdGR5B3oZzwhDSjCXwqLoVsf+v4Cb1TxqgXv1GPo7HHIQFALIztCkW2VZz4+Hzkx/Ue8lAsnwy/OXMJafFHOtFY7Rb+3NzFuZr0IoFDmEbr5z4fQqdQ2RSPrT2Xx+BVfKOQ5YhsoByCIxgjkR5v1phhB78LOCCnMiKxHMh1l92ML4/Xa4bcTcqEs5C86t844HuvH/e3XsDwNrpLB5D8uFma4btnuJTKjnTY+aQj1DMtTrQWzDTn5DFXB8FDHLys0a3SDjHKV+fi5aJ3iEht/CA/s+VjIPsxo5e2tcPCPQ5+cq9fjlATk0xBv4UelcXI0IFLYNfVTh7FtkmUAbb0mYDgelQ8dmcgmmoSBPv5iN8uDv4fY2GUgnKdv8fNN1mJAsfc8KAzQ0poGULTrrXGzN79VRg2oSp8t74x/dFJn+Q+SD6Z3L0hU+V7QK0MtyUljaJ9v+ZKG6flqqPKJPuyd5vwBDPsL3rYVGY6rIXCV+71iQN5W0yernmUHT9h5oCo5ZbKoxxyJ/FtENcGhicqO42wLoz5AGuYNqnikoWv6IxwgydAAAAEbLDYgavoVSgyfPW3ScelnqYmJtbjfQeYPKEzUstztxPheKUfh5k8XTtE6hF1zICDKkoDr6J6cKA7NvxrYZ1FUi/AunwNteRxN4883kWlOJP/4BxwPhGfvurMHVQ+QXFcQAAbhh86/iDff1q7H6T0G9jJp8OKn+2";
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
  const host = document.body, n = 100, dist = (window.innerHeight || 800) + 60;   // [dun-chrome] CONFETTI-REF: 100 pieces
  let maxLife = 0; const wrap = document.createElement("div"); wrap.className = "fx-confetti";
  for(let i=0;i<n;i++){
    const z = confettiRnd(.75,1.15), fall = confettiRnd(1.6,2.6)/z, delay = confettiRnd(0,.35);   // [dun-chrome] CONFETTI-REF: the fall 1.6-2.6 s
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
   // pitch climbs one step per block — HEAR the count
/* the teach scene: the crane drops N blocks ONE AT A TIME (ascending thunk + spoken count) then a
   cardinality "freeze" (vo_total_N). Reached from MEET_NUMBER via data.present==='crane'. */
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
  if((CARD.slides[state.idx]?.data || {}).no_idle_vo || ['MATCH_THE_PAIR','MATCH_VACHAN_PAIRS','FILL_VACHAN_DRAG','SENT_PICK','LETTER_STORY','STAMP_DEMO'].includes(CARD.slides[state.idx]?.type)){stopIdleVo();return;}
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
function pictureCell(picture, emoji, imgKey){
  const cell = document.createElement("div");
  cell.innerHTML = imgOrEmoji(imgKey, emoji, "pic-img", "pic-emoji") + `<span class="lbl">${picture||""}</span>`;
  return cell;
}
/* gender helpers: an option card showing a gender label (पुल्लिंग/स्त्रीलिंग),
   and a stimulus card showing the target gender label. */

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

/* counting helpers (maths): a numeral option card (big numeral + small number word),
   and a stimulus box showing a set of `count` identical objects to be counted. */
/* VISUAL-FIRST quantity: a HAND showing n fingers up (assets/UI/hand_1..5) — pre-reader,
   NO number-word text. Falls back to the numeral only if n is outside 1..5 or the art is missing. */
function fingerCount(n){ return `<span class="num-glyph">${n}</span>`; }   /* [optimize] its finger pictures (hand_1..5.png) never shipped; only a counting game's landing (CARD.landing_hero, none here) called it */
/* DISPLAY numeral: ALWAYS Arabic (1 2 3) on screen — kids learn the universal digit.
   Spoken VO stays Hindi (एक/दो/तीन) via the separate vo_num_/vo_total_ audio files. */
function devNumeral(n){ return String(n); }
/* DUAL-CODED counting option: the Devanagari NUMERAL the child is learning, big and on top,
   with a smaller finger-hand beneath it as a visual anchor. The point of counting is to learn the
   NUMBER SYMBOL, not just read a hand-sign — so the numeral leads and the hand supports. Falls back
   to the numeral alone if the hand art (1..5) is missing. */
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
/* HINT for "how many": instead of a text popup, COUNT the set FOR the child —
   highlight each object left→right, say एक/दो/तीन, show the numeral on top of it.
   The child sees + hears the count modelled, then answers from the options. */

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

/* STORY_SCENE poem captions: show each complete line immediately, then pulse whole words in
   playback order. The real clip's currentTime drives the word cue; authored VO timing is the
   fallback while a recording is not available. */


/* EVIDENCE comprehension helpers (H04 L03 शाब्दिक एवं अनुमान-आधारित बोध) — ADDITIVE (r4n); used only by
   STORY_READALONG / EVIDENCE_QA / FIND_EVIDENCE / QTYPE_RECAP. A passage = optional picture + the story
   text as sentence spans (each sentence has its own clip, so it can be read along / re-heard / tapped).
   evMark() lights the proof: literal → yellow highlight + "📖 उत्तर यहाँ लिखा है"; inference → dashed
   purple outline + "🔍 सुराग़" (the curriculum's "सुराग़ अलग टैग से दिखता है"). */
function evMark(lines, idxs, qtype){
  (idxs || []).forEach(i=>{ const l = lines[i];
    if(!l || l.classList.contains("ev-hl") || l.classList.contains("ev-clue")) return;
    l.classList.add(qtype === "inference" ? "ev-clue" : "ev-hl");
    const t = document.createElement("span"); t.className = "ev-tag";
    t.textContent = qtype === "inference" ? "🔍 सुराग़" : "📖 उत्तर यहाँ लिखा है";
    l.insertBefore(t, l.firstChild); });
}

/* ---------- [story-fig] THE STORY PAGES' FRAME + NARRATED TEXT ----------
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
    '<img class="sfig-swiftie" src="assets/UI/title_swiftie_hello.webp" alt="Swiftee" draggable="false">';
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


  /* ================= COMPARE_VACHAN — "शब्दों की तुलना" (deck pp.5,7,9,11) =================
     Two pictures (one object / many), the two word cards under them, and the spoken line in its
     OST box. Deck removals are honoured: NO heading, NO "एक गुब्बारा"/"बहुत सारे गुब्बारे"
     captions, NO "आ की मात्रा → ए की मात्रा" row. Deck animation note: the whole word appears
     first, and only AFTERWARDS does the changed tail pulse/glow. */



  /* ===== SHAPES (maths) — reuse the same scaffold/nudge/feedback as letters ===== */







  /* ===== COUNTING (maths) — OTO tap-count, cardinality, meet-number, make-set ===== */















  /* ===== NUMBER-SEQUENCE PATH (MTKGA01_L02_S04 — "completes a number sequence within 20") =====
     Three additive modules that share the .seq-* number-path skin. Numerals are crisp text glyphs
     (Baloo), only the tile chrome is rounded — content-true geometry (never round the number). */




  /* ===== ORDERING / SERIATION (MTKGA02_L02_S02 — "orders three objects by size, length, or weight") =====
     Additive modules sharing the .ord-* skin. Objects render at true magnitude (size scale / bar length);
     weight is assessed by 'pick the heaviest' (weight is not visual) — targeting the bigger=heavier
     misconception with a big-but-light distractor. */


  /* 16j NEW (g6 ordering tutorial): teach a 2-way attribute (बड़ा/छोटा · लंबा/छोटा · भारी/हल्का)
     BEFORE ordering three. Autonomous — points at each of 2 objects, speaks its label, then concludes
     + unlocks आगे. Reuses ord-stage. data:{by, items:[{img/emoji/color,mag}], label_audio:[id,id]}. */
























  /* ===== [reskin] PORTED from the HI02H05_L03_S01 engine (2026.07.21b-unified): the punctuation lesson's own
     content modules. Same helper contracts (mountTapOptions / makeDraggable / dragWrong / celebrateThenAdvance /
     startNudge / imgOrEmoji / audioFor / setNavActive / completeSlide); only the bus name changed (SwiftPAL -> GameBus). ===== */

  /* ===== [story-fig] STORY_LISTEN — the Figma story page, the first screen after the start gate's peek
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
      // [vo-rec] "आइए इन वाक्यों को सुनते हैं।" (data.intro_audio) before the story; the chip waits it out
      const introSrc = d.intro_audio ? ("assets/Audio/" + d.intro_audio + "." + AUDIO_EXT) : null;
      if(introSrc){ state.demoRunning = true; let introDone = false;
        const go = ()=>{ if(introDone || !alive()) return; introDone = true; state.demoRunning = false; start(); };
        play(introSrc, go); setTimeout(()=>{ if(!introDone && alive()){ stopAudio(); go(); } }, authoredVoHoldMs(introSrc) + 10000); }
      else start();
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

  /* ===== [recap-fig] MARKS_RECAP — the mark page after the read-again page. [recap-fig2] (2026-11-01): laid out as FLN-by-MJ
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
      // [recap-eg] (2026-11-04) only the PAGE's own mark (d.mark) does: T1B's sentence now ends in a "।", which lights and goes with
      // its word as the words do (T1's and T1C's sentences hold no other mark, so they are as before)
      const own = (s)=> !d.mark || [...s].every(ch=> ch === d.mark);
      const keeps = [];
      Leg.words.forEach((w, i)=>{
        if(/^[।?,!]+$/.test(w.textContent)){ if(own(w.textContent)) keeps.push({ el: w, i }); return; }
        const m = w.textContent.match(/^(.+?)([।?,!]+)$/);
        if(m && own(m[2])){ w.textContent = m[1]; const s = document.createElement("span"); s.className = "rcf-mk"; s.textContent = m[2]; w.appendChild(s); keeps.push({ el: s, i }); }
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
      /* [recap-eg] (2026-11-04) data.pic_decode: the picture's bitmap decoded now, ~15 s before it shows — a large one is otherwise decoded
         on its first paint and Chrome holds the entrance until then (T1B's 1199x1312 painting girl: 50 ms behind its sound; the old
         450x300 fruits: 0) — so it comes in on the frame its sound starts */
      if(d.pic_decode){ const im = pic.querySelector("img"); if(im && im.decode) im.decode().catch(()=>{}); }
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

  /* ===== [t2-scene] PUNCT_SCENE — T2, the first example (FLN-by-MJ frame 706:188 "2 T0B"), on T0B / T1's card (.sfig-round:
     the frame's 1088x508 card at 96,106, 64px corners; the standing Swiftie and the 🔊 chip where page 3 T1 has them): the
     frame's hallway picture fills the card; the sentence "पिंकी स्कूल जा रही है" with an empty dashed slot after it; the girl
     walking in from the doorway; three mark tiles. It drives itself up to the tap:
     1. the intro line (data.intro_audio) over the picture alone — no sentence, no girl, no tiles;
     2. 0.5 s after it the sentence rises in whole and the slot pops in, with T1's text pop ([recap-sfx] popSoft); 0.45 s later
        the sentence's clip, each word lit as it is read ([word-sync]);
     3. 0.3 s after the clip data.pic_sfx (the user's school sound) for data.pic_sfx_ms (2 s), faded out over its last 0.4 s, and
        the girl — in her place since the first frame ([t2-scene2]; she walked in from the doorway before) — gives a small pop
        (CSS dscPop) as it starts;
     4. 0.3 s after the sound the slot blinks for data.blink_ms ([blink-2] 2026-11-10: T2-T4 3.5 s = two cycles, the picks 7 s = four;
        [t2-scene5]: 7 s in SLOW data.blink_cycle_ms = 1.75 s cycles —
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
        hint ladder (data.hint1_audio / hint2_audio 0.5 s after — [hint2-lit] hint 2 lighting each sign's tile as it names it, on
        data.hint2_signs; the 3rd wrong tap the pointing hand under the right tile, the
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
      // the cover over the painted iris and the iris itself, which slides — the covers and the irises on two sheets her image's size
      // (data.girl_eyes), drawn with her image's box and cover; the rig shows only for the glance (the CSS); nothing else of her is touched
      const EY = d.girl_eyes || {};
      const eyesHtml = '<div class="dsc-girl"><span class="dsc-shade"></span><img src="' + imgSrc(d.image_id) + '" alt="" draggable="false"><div class="dsc-erig">' +
        [1, 2].map(k=> '<div class="dsc-eeye e' + k + '"><img class="dsc-efill" src="' + imgSrc(EY.fill) + '" alt="" draggable="false"><img class="dsc-eiris" src="' + imgSrc(EY.iris) + '" alt="" draggable="false"></div>').join("") + '</div></div>';
      // [g3-grow] data.grow: over the garden (the painting), the growth's layers — the garden without its plants (data.grow.bare)
      // and each plant on its own sheet, growing from its stem — all the garden's size, drawn with its box and cover
      const G = d.grow || null;
      const plantsHtml = G ? '<div class="dsc-plants"><img src="' + imgSrc(G.bare) + '" alt="" draggable="false">' + G.plants.map((id, k)=> '<div class="dsc-plant p' + (k + 1) + '"><img src="' + imgSrc(id) + '" alt="" draggable="false"></div>').join("") + '</div>' : '';
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
      const lookOn = ()=>{ if(!look || lookT0 >= 0) return; girl.classList.add("look"); if(look.hold) girl.classList.add("held"); lookT0 = performance.now(); };   // [g3-screen] look.hold: .held keeps her rest pose (the CSS's) once .look has gone
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
      // 4. the slot blinks over blink_ms in blink_cycle_ms cycles ([blink-2]: T2-T4 3.5 s = two fades, then the box stays seen; the picks
      //    [t2-scene5]'s 7 s of slow 1.75 s cycles = four fades of the whole
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
      // two dead and dim, [vo-rec3] hint 3's line with it, then nothing spoken again); the right one presses (dmfTap, its colours kept), its mark lands in the
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
      // [hint2-lit] (asked 2026-11-10) hint 2 names the three signs one after another ("वाक्य पूरा होने पर पूर्णविराम, वाक्य में रुकने पर
      // अल्प विराम और प्रश्न पूछने पर प्रश्नवाचक चिह्न लगाते हैं ।"): as the line names a sign, its tile lights in T2-T4's lit look (.lit: the
      // words' orange on the mark with its pop, the orange border and glow on the face, eased in and out by the face's own transitions)
      // and holds it until the line goes on to the next sign's part — the last one until the line ends. data.hint2_signs: per mark its
      // on / off on the clip's own clock (vo_rec.py: the words' sound onsets; off null = the line's end). Read off the clip every frame,
      // so a line that ends, stops or is replaced takes its light with it (a 20 s cap for a clip that never starts).
      const signLights = (a)=>{
        const lit = (d.hint2_signs || []).map(s=> ({ t: tiles[opts.findIndex(o=> o.mark === s.mark)], on: s.on, off: s.off })).filter(s=> s.t);
        if(!a || !lit.length) return;
        const cap = performance.now() + 20000;
        const tick = ()=>{
          const gone = !alive() || a.ended || currentAudio !== a || (a.paused && a.currentTime > 0) || performance.now() > cap, t = a.currentTime + 0.04;
          lit.forEach(s=> s.t.classList.toggle("lit", !gone && t >= s.on && (s.off == null || t < s.off)));
          if(!gone) nextFrame(tick); };
        nextFrame(tick);
      };
      const hintLadder = (n)=>{
        if(n >= 3){ showHand(); tiles.forEach((t, k)=>{ if(k !== pick){ t.onclick = null; t.classList.remove("live"); t.classList.add("off"); } });   // the wiggle just started runs out on its own
          if(n === 3) after(500, ()=>{ if(!live || isPlaying) return; if(d.hint3_audio){ play(A(d.hint3_audio), ()=>{}); fbAudio = currentAudio; } });   // [vo-rec3] "यह सही चिह्न है, इसपर टैप कीजिए ।" with the hand
          return; }
        const id = n <= 1 ? d.hint1_audio : d.hint2_audio;
        after(500, ()=>{ if(!live || isPlaying) return; if(id){ play(A(id), ()=>{}); fbAudio = currentAudio; if(n === 2) signLights(currentAudio); } });   // a hint line is feedback: no tile answers while it speaks; [hint2-lit] hint 2 lights the signs as it names them
      };
      // [pick-idle] (asked 2026-11-16 for G1-G3: "in the case of 7 seconds of inactivity from the user end this instruction Vo should
      // repeat"): data.idle_intro_ms — once the tiles are the child's, the instruction line (data.intro_audio) again after every
      // idle_intro_ms of quiet: no touch anywhere and nothing sounding (a line, a hint, an effect). Every touch and every sound starts the
      // count over, so the line comes 7 s after the last of them, and again 7 s after itself for as long as the child does nothing. Not
      // while the pointing hand shows (the chip's own rule: after the 3rd wrong tap only hint 3 speaks, [hand-quiet] / [vo-rec3]) and
      // never after the answer. A tap cuts the line short and answers, as for the chip's. The engine's idle reminder stays off here
      // (data.no_idle_vo): it speaks once per page only.
      const idleIntro = ()=>{
        const ms = d.idle_intro_ms; if(!ms || !d.intro_audio) return;
        let since = 0; const poke = ()=>{ since = 0; };
        document.addEventListener("pointerdown", poke, true);
        const tick = ()=>{
          if(!alive() || !live){ document.removeEventListener("pointerdown", poke, true); return; }
          if(isPlaying || sfxBusy() || hintHand) since = 0;
          else if(!since) since = Date.now();
          else if(Date.now() - since >= ms){ since = 0; GameBus.emit("idle_vo_replay", { slide_id: slide.id, phase: slide.phase }); say(A(d.intro_audio), ()=>{}); }
          setTimeout(tick, 100);
        };
        tick();
      };
      function armTile(k){
        if(!live){ live = true; state.demoRunning = false; setSwMood("point");
          // [g1-quiet] the 🔊 chip: the instruction line (data.intro_audio) again — NOT the sentence: its clip and its word light play
          // once on this page (asked twice: "the VO and the highlight animation of the sentence should not repeat"); the engine's
          // idle reminder, which would call this too, is off here (data.no_idle_vo)
          state.replayAudio = ()=>{ if(!live || isPlaying || sfxBusy() || hintHand || !alive()) return; say(A(d.intro_audio), ()=>{}); };
          idleIntro(); }   // [pick-idle]
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
        tiles.forEach((x, j)=>{ x.onclick = null; x.classList.remove("wiggle", "live", "lit"); if(j === pick) x.classList.add("on"); });   // only the tapped tile answers: the other two stay as they are ([hint2-lit] no sign light outlives hint 2)
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
      // the tiles). Grown, the layers fade into the painting under them (data.grow.fade_ms: the same picture) and leave the page —
      // from then on the garden is the painting itself, drawn as before (the finished layers, kept, held the sentence and the tiles on
      // layers of their own: their text drawn differently, measured). A garden that never decodes holds nothing up for more than 5 s.
      if(G){
        const pics = Array.from(fig.querySelectorAll(".dsc-bg > img, .dsc-plants img, .dsc-erig img"));
        const decoded = Promise.all(pics.map(im=> im.decode ? im.decode().catch(()=>{}) : Promise.resolve()));
        const wait = (ms)=> new Promise(r=> setTimeout(r, ms));
        Promise.race([Promise.all([decoded, wait(G.start_ms || 600)]), wait(5000)]).then(()=>{
          if(!alive()) return;
          const pl = fig.querySelector(".dsc-plants"); pl.classList.add("grow");
          if(G.sfx) playKitSfx("sceneGrow", G.sfx, G.sfx_vol == null ? .9 : G.sfx_vol);
          after(G.look_ms || 0, lookOn);
          after(G.then_ms || 2700, opening);
          Promise.all(pl.getAnimations({ subtree:true }).map(a=> a.finished)).then(()=>{ if(!alive()) return;
            pl.classList.add("done"); after((G.fade_ms || 200) + 60, ()=> pl.classList.add("gone")); }).catch(()=>{});
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
        after(650, ()=>{ sfigRise(L); after(SENT_IN_MS, ()=>{ narrate(L.src, [], ()=>{}, ()=> speakThen(d.explain_audio, stage3)); sfigSync(L); }); });   // [vo-rec] the explanation after the sentence; [word-sync] the whole sentence, then its clip with the word light
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
          hintLadder(state.attempts);   // [vo-rec]
          return;
        }
        // the right one: pressed (the other two untouched since [tap-lock]), its mark lands in the slot as its name sounds; then the page moves on
        live = false; state.locked = true; state.demoRunning = true;
        const guided = !!hintHand;   // [hand-quiet] after the hand: no praise line — the mark, the ding + confetti, 1.7 s, the page moves on
        if(hintHand){ hintHand.remove(); hintHand = null; }   // [vo-rec]
        blanks.forEach(b=> b.classList.remove("blink"));
        tiles.forEach((x, j)=>{ x.onclick = null; x.classList.remove("wiggle"); if(j === pick) x.classList.add("on"); });   // [tap-lock] only the tapped tile answers: the other two stay as they are (the demos' auto tap, stage4, still dims them)
        marks.forEach((m, j)=> after(j * (d.mark_stagger_ms || 300), ()=>{ centreInk(m); m.classList.add("in"); }));
        sfxCorrect(); confettiCannon(); setSwMood("happy");
        GameBus.emit("punct_build_done", { slide_id: slide.id, phase: slide.phase, value: true,
          first_try: state.attempts === 0, wrong: state.attempts, latency_ms: Date.now() - state.slideStart });
        if(guided){ after(1700 + (marks.length - 1) * (d.mark_stagger_ms || 300), ()=> completeSlide(true)); return; }   // [hand-quiet] no line after the guided tap
        narrate(A(d.ok_audio || d.mark_audio), [], ()=>{}, ()=> after(PACE.tail, ()=> completeSlide(true)));   // [vo-rec] "शाबाश!" (data.ok_audio) in the name's place
      }
      // 4. the mark's name: its tile is tapped for the child, the others go dim; then the mark lands in the slot(s), one
      //    after the other (data.mark_stagger_ms apart) when there are several
      function stage4(){
        showHand();   // [demo-hand] the pointing hand under the tile as it is tapped for the child (the picks' hand)
        tiles.forEach((t, k)=> t.classList.add(k === pick ? "on" : "off"));
        const gap = d.mark_stagger_ms || 300;
        narrate(A(d.mark_audio), [], ()=>{}, ()=>{
          marks.forEach((m, k)=> after(400 + k * gap, ()=>{ centreInk(m); m.classList.add("in"); }));
          after(400 + (marks.length - 1) * gap + 700, ()=> speakThen(d.again_audio, stage5));   // [vo-rec] "अब दोबारा देखिए ।" before the full reading
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
        narrate(A(F.audio), F.word_times || [], hot, ()=> speakThen(d.conclude_audio, ()=>{   // [vo-rec] the conclusion before the page moves on
          // 6. the slots' boxes go (the marks stay) and the page moves on by itself
          after(d.hold_ms || 1500, ()=>{ L.words.forEach(w=> w.classList.remove("hot")); blanks.forEach(b=>{ b.classList.remove("hot"); b.classList.add("gone"); });
            after(600, ()=>{
              // T4: the gate into the guided round (the peeking Swiftie, "चलिए, साथ में करें!" and its VO) follows this
              // page EVERY time it ends: the engine shows each round's gate once per load, so a re-run of T4 (the dev
              // nav's list) went straight to G1 — clearing the round here lets completeSlide cross the same gate again
              const nx = CARD.slides[state.idx + 1], nr = nx && PHASE_ROUND[nx.phase];
              if(nr && nr !== PHASE_ROUND[slide.phase]) _gatedPhases.delete(nr);
              completeSlide(true); }); });
        }));
      }
    }
  },

  /* ===== [sent-fig] SENT_PICK — G4, P1 and P2 "सही विराम चिह्न वाला वाक्य चुनिए ।", built on the reference game's Page 11 (P4, the
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
     - data.mastery (P1, P2, as the practice pages they replace): one mastery attempt per page, a hit on a first try.
     - [p2-side] data.layout "side" (P2, 2026-11-15; [g4p1-side] the same day G4 and P1 too, so P4's layout above is used by no page
       now): the row of https://hind-dear-story.vercel.app/ page 15 (G2) instead — the
       picture alone in a white card on the left, the three sentences stacked on the right, each on ONE line (no break); the
       picture's pops play on the whole card, and the reveal hand points into the right sentence's lower part as G2's does
       (its top 56px above the box's bottom edge) instead of standing under it, where it would cover the sentence below.
       Everything else as above.
     - [p2-tap] data.hand_tap (P2, 2026-11-15; [g4p1-tap] G4 and P1 too, same day): that reveal hand TAPS, as G2's does — it stays where it stands (no bob), its
       finger presses on a 1.3 s beat with G2's ripple and sparks opening round the tip (style.css [p2-tap]). ===== */
  SENT_PICK: {
    mount(host, slide){
      const d = slide.data || {}, A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const IDLE_MS = 5000, BEAT_MS = 1000, HOLD_MS = 1000, REVIEW_GAP_MS = 500, POP_MS = 1000, PROMPT_POP_MS = 3200, HIT_PAD = 24;
      const opts = (d.options || []).slice();
      for(let i = opts.length - 1; i > 0; i--){ const j = (Math.random() * (i + 1)) | 0; [opts[i], opts[j]] = [opts[j], opts[i]]; }
      const side = d.layout === "side";   // [p2-side] G2's row: the picture's card left, the sentences stacked right
      const row = document.createElement("div"); row.className = "q-row" + (side ? " sent-side" : "");
      const stim = document.createElement("div"); stim.className = "story-q-stim " + (side ? "sq-card" : "sq-bare");
      const thumb = document.createElement("img"); thumb.className = "story-q-thumb"; thumb.src = imgSrc(d.recall_image_id); thumb.alt = ""; thumb.draggable = false;
      stim.appendChild(thumb);
      const popEl = side ? stim : thumb;   // [p2-side] what the picture's pops move: the card with its picture there, the bare picture here
      const grid = document.createElement("div"); grid.className = side ? "opt-grid cols-1 sent-opts sent-col" : "opt-grid cols-3 sent-opts";
      if(side && d.opt_px) grid.style.setProperty("--so-fs", d.opt_px + "px");   // [g4p1-font] G4, P1: their sentences' size in the side row (P2: none, 28px)
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
        if(side || !alive() || grid.querySelector(".so-br") || !items.some(it=> it.pill.scrollWidth > it.pill.clientWidth)) return;   // [p2-side] G2's row: one line each, never broken
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
        if(pop && !popEl.classList.contains("p2-pop")){
          popEl.classList.remove("p6-pop"); void popEl.offsetWidth; popEl.classList.add("p6-pop");
          setTimeout(()=> popEl.classList.remove("p6-pop"), PROMPT_POP_MS + 250);
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
          if(state.attempts >= 2){ state.scaffoldLevel = Math.max(state.scaffoldLevel, 2);
            if(audioFor(slide, "hint2")){ play(audioFor(slide, "hint2"), ()=> it.cell.classList.remove("crossed")); fbAudio = currentAudio; return; }   // [vo-rec3] the deck's hint 2 line
            review(()=> it.cell.classList.remove("crossed")); return; }
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
        if(audioFor(slide, "hint3")){ play(audioFor(slide, "hint3"), ()=>{}); fbAudio = currentAudio; }   // [vo-rec] "यह सही वाक्य है, इसपर टैप कीजिए" — the hand follows once it is quiet; [tap-lock] feedback: nothing answers while it speaks
        const place = ()=>{
          if(!alive() || !right.cell.classList.contains("opt-guided")) return;
          if(isPlaying){ after(100, place); return; }
          const st = document.querySelector(".slide-stage"); if(!st) return;
          if(d.hand_tap){   // [p2-tap] P2 ([g4p1-tap] G4, P1 too): the reference G2's tapping hand — its finger presses on a 1.3 s beat with G2's ripple + sparks behind the tip (style.css [p2-tap]); no bob
            hand = document.createElement("div"); hand.className = "reveal-hand rh-tap";
            hand.innerHTML = '<span class="rh-fx" aria-hidden="true"><i class="rh-ro"></i><i class="rh-ri"></i><i class="rh-sp"></i></span>' +
                             '<img class="rh-img" src="assets/UI/nudge_hand_new.svg" alt="" draggable="false">';
          } else { hand = document.createElement("img"); hand.className = "reveal-hand"; hand.src = "assets/UI/nudge_hand_new.svg"; hand.alt = ""; }
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
        hand.style.top = (side ? (r.bottom - sw.top) / scale - 56 : Math.min((r.bottom - sw.top) / scale + 4, st.offsetHeight - HAND_H)) + "px";   // [p2-side] G2's pointNudgeAt: the fingertip in the box's lower part
      }
      // the guided pill counts a tap just beside it too (HIT_PAD design px), once nothing speaks
      const padTap = (e)=>{
        if(!alive()){ document.removeEventListener("click", padTap, true); return; }
        if(!right.cell.classList.contains("opt-guided") || isPlaying || hold) return;
        const t = e.target; if(!t || right.cell.contains(t) || (hand && hand.contains(t))) return;   // [p2-tap] the tapping hand is a box (its finger, its ripple): a tap on any of it is the hand's own
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
        popEl.classList.remove("p6-pop"); popEl.classList.add("p2-pop"); setTimeout(()=> popEl.classList.remove("p2-pop"), POP_MS + 250);
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
          const okSrc = audioFor(slide, "ok"), readIt = ()=> say(it, ()=> after(700, ()=> completeSlide(true)));   // [vo-rec] "शाबाश! यह सही वाक्य है ।" then the pill's own line
          if(okSrc) play(okSrc, readIt); else readIt();
        });
      }
    }
  },

  /* ===== [letter-fig] LETTER_STORY — the letter page, after P2's round gate. [l1-fig] (2026-11-03) the user's flow on Figma 792:1257
     -> 792:1245 -> 792:1249: 1. the girl writing comes in full screen on the magic shimmer's first frame; 2. then the narration
     (data.intro_audio) with the mild piano bed; on the narration's own clock: 3. on "दादाजी" (pace.dada) the girl thinking fades in
     and the grandfather's memory cloud appears (the bubbles pop one by one, the cloud grows in from their corner); 4. [l1-late] 2 s
     before the narration's speech ends (pace.letter) [l1-cloud] the room stays as it is and [l1-clean] the grandfather's whole
     picture fades out of the SAME cloud, leaving it clean white (data.cloud_clean: a patch of its own white over its body, the rim
     untouched), and once it is (pace.env_after) the letter grows in it, where it stands (no sound);
     5. once the narration has ended (and the letter has grown) it pulses and waits — the
     only tap: the pop, the envelope zooms to 610:6 over the blurred room, the seal pops, the flap swings open on the paper crackle,
     the sheet rises, the view dives into it, a veil — then the next page. Self-driving, no आगे. Timings in data.pace (ms), places
     in data.layout (frame px). ===== */
  LETTER_STORY: {
    mount(host, slide){
      const d = slide.data || {}, L = d.layout || {}, P = Object.assign({ w_in: 900, vo_at: 1200, music_vol: 0.2, music_in: 1200, dada: 840, letter: 9070,
        xfade: 650, bub_after: 300, bub_gap: 230, cloud_after: 1000, env_after: 700, ready_after: 300,
        zoom: 1200, paper_at: 350, dive_at: 700, dive: 1700, dive_scale: 5.2, veil_at: 1900, done_at: 2450 }, d.pace || {});
      const A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const sfx = d.sfx || {}, env = d.env || {}, sc = d.scenes || {}, SB = L.scenes || {};
      const cl = L.cloud || [790.58, -24.76, 352.24], bubs = L.bubbles || [], li = L.letter || [967.44, 151.52, 211.68], full = L.full || [71, -50, 1138, 758],
            mo = L.mouth || [568.8, 292.4];
      const box = (b)=> b ? 'left:' + b[0] + 'px;top:' + b[1] + 'px;width:' + b[2] + 'px;height:' + b[3] + 'px' : '';
      const fig = sfigMount(host,
        '<div class="ltr">' +
          ['w', 't', 'p'].filter(k=> sc[k]).map(k=> '<img class="ltr-scene ' + k + '" src="' + imgSrc(sc[k]) + '" alt="" draggable="false" style="' + box(SB[k]) + '">').join("") +   // each frame's picture in its own box ([l1-cloud] only those the card names: no p now)
          bubs.map(b=> '<span class="ltr-bub" style="left:' + (b[0] - b[2] / 2) + 'px;top:' + (b[1] - b[2] / 2) + 'px;width:' + b[2] + 'px;height:' + b[2] + 'px"></span>').join("") +
          '<div class="ltr-cloud" style="left:' + cl[0] + 'px;top:' + cl[1] + 'px;width:' + cl[2] + 'px;height:' + cl[2] + 'px">' +
            '<img class="ltr-cg" src="' + imgSrc(d.cloud) + '" alt="" draggable="false"><img class="ltr-cc" src="' + imgSrc(d.cloud_clean) + '" alt="" draggable="false"></div>' +   // [l1-clean] over the grandfather's picture: the same cloud, clean white
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
      // the envelope's icon state = the full-screen box (610:6) scaled down into the cloud, so the zoom moves the same element
      const s = li[2] / full[2];
      envPos.style.setProperty("--ltr-icon", "translate(" + (li[0] - li[2] / 2 - full[0]) + "px, " + (li[1] - (li[2] * full[3] / full[2]) / 2 - full[1]) + "px) scale(" + s + ")");
      // [l1-fig] the letter grows in where it stands, in the standing cloud: about the box's own centre, no slide
      envPos.style.setProperty("--ltr-go", (full[2] / 2) + "px " + (full[3] / 2) + "px");
      envPos.style.setProperty("--ltr-gt", "0px, 0px");
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
      [sfx.magic, sfx.pop, sfx.paper, d.music].forEach(id=>{ const src = A(id); if(!src) return;
        try{ const a = new Audio(src); a.preload = "auto"; a.load(); pre[id] = a; sounds.push(a); }catch(e){} });
      try{ const v = A(d.intro_audio); if(v) new Audio(v).load(); }catch(e){}   // [l1-fig] the narration too: it starts 1.2 s in
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
      // [l1-fig] the narration's moments, each run once on ITS clock (the clip's currentTime; the time since it was started if the
      // clip is not the one playing — it failed, or another took over); ready = the narration over AND the letter grown
      const cues = []; let voA = null, voT0 = 0, voDone = false, grown = false;
      const watch = ()=>{ if(!alive()) return;
        const t = (voA && currentAudio === voA) ? voA.currentTime * 1000 : performance.now() - voT0;
        cues.forEach(c=>{ if(!c.done && t >= c.ms){ c.done = true; c.fn(); } });
        if(cues.some(c=> !c.done)) requestAnimationFrame(watch); };
      const tryReady = ()=>{ if(!voDone || !grown || tapped || root.classList.contains("ready")) return; root.classList.add("ready"); state.demoRunning = false; armNudge(); };   // [l1-nudge] the envelope pulses: the 5 s starts
      // 1. the girl writing (792:1257) comes in full screen on the magic shimmer's first frame; 2. the narration vo_at after it, with
      //    the piano bed fading in under it (mild: pace.music_vol)
      sound(sfx.magic, 0.6, ()=>{ root.classList.add("w-in"); at(P.vo_at, ()=>{
        music = sound(d.music, 0.0001, ()=> fadeTo(music, P.music_vol, P.music_in), true);
        const src = A(d.intro_audio);
        const ended = ()=>{ if(voDone || !alive()) return; voDone = true; at(P.ready_after, tryReady); };
        voT0 = performance.now();
        if(src){ play(src, ended); voA = currentAudio; setTimeout(()=>{ if(!voDone && alive()){ stopAudio(); ended(); } }, authoredVoHoldMs(src) + 10000); }
        else at(P.letter + 1500, ended);
        requestAnimationFrame(watch);
      }); });
      // 3. on "दादाजी": the girl thinking (792:1245) fades in over her, the bubbles pop one by one, the cloud grows in from their corner
      cues.push({ ms: P.dada, fn: ()=>{ root.classList.add("t-in");
        bubEls.forEach((b, k)=> at(P.bub_after + k * P.bub_gap, ()=> b.classList.add("in")));
        at(P.cloud_after, ()=> cloud.classList.add("in")); } });
      // 4. [l1-late] 2 s before the speech ends: [l1-cloud] the room stays (792:1245) and [l1-clean] the grandfather's whole picture
      //    fades out of the same cloud (its clean white comes over its body, .5 s; the rim never changes), and once the cloud is clean
      //    white (env_after) the letter grows in it (the CSS: .9 s) — no sound
      cues.push({ ms: P.letter, fn: ()=>{ cloud.classList.add("clean");
        at(P.env_after, ()=>{ root.classList.add("letter-in"); at(900, ()=>{ grown = true; tryReady(); }); }); } });
      // [l1-nudge] (asked 2026-11-15: "when the envelope of the letter starts pulsating in the cloud like dialogue box then in the case
      // of 5 seconds of inactivity from the user end the exact same hand nudge should come with the same tapping animation on the
      // envelope of the letter as previous pages"): once the envelope pulses (.ready), nudge_ms (5 s) with no tap anywhere brings the
      // earlier pages' tapping hand onto it — the very element of P2's / G4's / P1's reveal hand in its rh-tap form (nudge_hand_new.svg,
      // its finger pressing on a 1.3 s beat with G2's ripple and sparks round the tip: the same CSS rules, widened to this page), placed
      // as theirs is: centred on the envelope, its top 56 px above the bottom edge of the envelope's box (.ltr-env-grow, which does not
      // pulse), so the fingertip is in the envelope's lower part. A tap anywhere before then starts the 5 s again; once shown the hand
      // stays, tapping, until the envelope is tapped (a tap on the hand is the envelope's tap); the envelope's tap takes it away
      const NUDGE_MS = P.nudge_ms || 5000;
      let nudgeT = 0, hand = null;
      const armNudge = ()=>{ clearTimeout(nudgeT); if(tapped || hand || !alive()) return; nudgeT = setTimeout(showNudge, NUDGE_MS); timers.push(nudgeT); };
      const poke = ()=>{ if(!alive() || tapped){ document.removeEventListener("pointerdown", poke, true); return; }
        if(!hand && root.classList.contains("ready")) armNudge(); };
      document.addEventListener("pointerdown", poke, true);
      const showNudge = ()=>{
        if(tapped || hand || !alive() || !root.classList.contains("ready")) return;
        const st = document.querySelector(".slide-stage"), grow = fig.querySelector(".ltr-env-grow"); if(!st || !grow) return;
        hand = document.createElement("div"); hand.className = "reveal-hand rh-tap ltr-hand";
        hand.innerHTML = '<span class="rh-fx" aria-hidden="true"><i class="rh-ro"></i><i class="rh-ri"></i><i class="rh-sp"></i></span>' +
                         '<img class="rh-img" src="assets/UI/nudge_hand_new.svg" alt="" draggable="false">';
        hand.style.setProperty("pointer-events", "auto", "important"); hand.style.cursor = "pointer";
        hand.onclick = (e)=>{ e.stopPropagation(); envPos.onclick(); };
        const r = grow.getBoundingClientRect(), sw = st.getBoundingClientRect(), scale = sw.width / st.offsetWidth || 1;
        hand.style.left = ((r.left - sw.left) / scale + r.width / scale / 2 - 48) + "px";
        hand.style.top = ((r.bottom - sw.top) / scale - 56) + "px";
        st.appendChild(hand);
      };
      const clearNudge = ()=>{ clearTimeout(nudgeT); document.removeEventListener("pointerdown", poke, true); if(hand){ hand.remove(); hand = null; } };
      // 5. the tap: the pop, the zoom to 610:6 over the blurred room (the loop fades out), then the opening and the next page
      let tapped = false;
      envPos.onclick = ()=>{
        if(tapped || !root.classList.contains("ready") || !alive()) return;
        tapped = true; state.demoRunning = true; clearNudge();   // [l1-nudge]
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

  /* ===== [stamp-fig] STAMP_DEMO — L2, the stamp page after the letter. [stamp-868] (2026-11-03) on the FLN-by-MJ frames 868:3 (the
     angled table with the bird) and 868:17 / 868:31 / 868:44 / 868:59 / 868:74 (the overhead table, one per round). It drives itself:
     1. the angled table on the whole stage (868:3: the card with its sentence, the tray, the two standing stamps) as the letter
     page's veil lifts, and the bird glides in from the left to its place — the reference title page's entrance of its two children
     (the glide, the lean, the blur, the speed lines, the dust, its whoosh); 2. the instruction (data.intro_audio) with the bird's GIF
     playing on the clip's own clock, and on its "ठप्पा" (pace.thappa) both standing stamps glow along their outline and pulse
     gently; 3. the bird leaves the way it came, backwards, on the same whoosh; 4. the camera move: the angled table becomes the
     overhead one (868:17) — the same card, sentence, tray and stamps; then ROUND BY ROUND (data.rounds, [stamp-rounds]): 5. the
     sentence is read, each word lit as it is read (round 1's is already there; a later round's rises in first, after its own line
     and its stamps' pops); 6. the empty box(es) blink for 3 s, appearing and disappearing — from now on the stamps are the child's to
     drag; [stamp-drag] in round 1 the guidance, 0.5 s after the blink: the right stamp lifts, glides slowly over the box, hovers and
     glides home WITHOUT printing; it comes again after every 7 s without a touch. A stamp dropped off the box, or the wrong one on it:
     the kit's buzz, a wiggle, back it glides. The right stamp on the box: it snaps over the box and presses on the thud — the mark
     is printed in the box, standing on its row's baseline — lifts and glides home; the box goes on the correct chime, the mark stays;
     the kit's confetti on its sound. With a round to follow: the stamps shrink away (their pop played backwards), the sentence goes
     word by word in reverse with the box and its mark, the next round's stamps pop in — a round without `guide` has NO guidance
     [stamp-remind]: after 7 s without a touch the title's line is said again instead. A round with several boxes (data.slots): all
     blink together; the right stamp on one prints there and that box goes on the chime, then the stamps are the child's again for
     the rest; the confetti after the last; a box may want its own stamp (sl.mark, sl.pick). After the LAST round's confetti
     [stamp-close] the finale: the letter page's envelope transition backwards (the veil, the pull-back out of the envelope, the sheet
     down, the flap shut on its paper crackle, the seal back, the closed envelope shrinking into Pinki's hand as the room of Figma
     792:1253 comes into focus), then [stamp-final] the envelope there glitters gold for fin_glitter_ms on its chime, and fin_done
     after it the page moves on (no आगे). Places in frame px (data.layout, each round's boxes), moments in data.pace (ms). ===== */
  STAMP_DEMO: {
    mount(host, slide){
      const d = slide.data || {}, LY = d.layout || {}, im = d.images || {}, sfx = d.sfx || {};
      const rounds = Array.isArray(d.rounds) && d.rounds.length ? d.rounds : [{}];
      const P = Object.assign({ bird_at: 400, bird_tempo: 2.2, whoosh_vol: 0.75, vo_gap: 200, bird_loops: 3, thappa: 5120, intro_ms: 6407, exit_gap: 300,
        cam_gap: 250, cam_ms: 2000, cam_text: 0.12, cam_a: [0.15, 0.7], cam_squash: 0.5, read_gap: 450,
        after_intro: 500, stamps_at: 700, pop_gap: 350, sent_at: 700, blink_ms: 3000, blinks: 3,
        hint_at: 500, glide: 1500, hover_up: 0, hold: 450, back: 1100, idle_ms: 7000, tol_x: 60, tol_y: 60, tap_px: 10, wiggle: 450, reset: 500,
        lift_scale: 1.1, press_scale: 0.96, snap: 220, press: 140, press_down: 0, thud_at: 280, mark_at: 400, lift_at: 560, back_at: 800, back_home: 800,
        gone_at: 1600, confetti_at: 2100, done_at: 4400, words_out: 40, next_at: 1300,
        close_veil: 600, close_hold: 250, close_paper_at: 420, land_lead: 100, land_ms: 250, fin_glitter_at: 400, fin_glitter_ms: 1300, fin_sparks: 16, fin_done: 700 }, d.pace || {});
      const A = (id)=> id ? ("assets/Audio/" + id + "." + AUDIO_EXT) : null;
      const box = (b)=> 'left:' + b[0] + 'px;top:' + b[1] + 'px;width:' + b[2] + 'px;height:' + b[3] + 'px';
      const pic = (cls, id, b)=> '<img class="' + cls + '" src="' + imgSrc(id) + '" alt="" draggable="false" style="' + box(b || [0, 0, 0, 0]) + '">';
      const BX0 = [[484, 569, 105, 105], [683, 565, 114, 114]], TIPS0 = [[52.5, 52.5], [57, 57]];
      const boxes0 = rounds[0].boxes || BX0, maxN = Math.max(1, ...rounds.map(R=> (R.stamps || []).length));   // divs for the most stamps any round has
      // the bird: 868:3's GIF fill as a sheet of its frames (layout.bird: cols, frames, the drawn cell, the clip box, its feet = the ellipse's centre)
      const BD = LY.bird || {}, FT = BD.foot || [107.5, 693.5], BB = BD.box || [11.975, 451.76, 220, 252], CELL = BD.cell || [220, 252], COLS = BD.cols || 6, NF = BD.n || 36,
            SH = LY.bird_shadow || [39, 682, 137, 23];
      const fig = sfigMount(host,
        '<div class="stp" data-round="0">' +
          // the overhead table (868:17 .. 868:74): the same wood still under it all (it fills the frame's edge while the table tilts), then
          // the wood, the card and its postmark as ONE layer (the camera move draws it through its projective map)
          pic("stp-under", im.wood, LY.wood) +
          '<div class="stp-b"><div class="stp-bo">' + pic("stp-wood", im.wood, LY.wood) + pic("stp-card", im.card, LY.card) + pic("stp-post", im.post, LY.post) + '</div>' +
            '<div class="stp-bi">' + pic("stp-card", im.card, LY.card) + pic("stp-post", im.post, LY.post) + '</div></div>' +
          // the angled table (868:3): its picture (the card's painted sentence lifted out, a_text, over the paper filled under it) and its
          // postmark — each table twice: its whole picture (-o, the move maps it by its card's edge) and its card's inside (-i, clipped
          // halfway between the edge and the dashed border; the move maps it by that border), so both the edges and the dashes of the
          // two drawings meet as they cross-fade (the frames inset their dashes differently: 868:3 ~27 / 12 / 25 / 26 px, 868:17 ~20 / 19 / 19 / 17)
          '<div class="stp-a"><div class="stp-ao">' + pic("stp-a-bg", im.a_bg, LY.a_bg) + '</div>' +
            '<div class="stp-ai">' + pic("stp-a-bg", im.a_bg, LY.a_bg) + pic("stp-a-post", im.a_post, LY.a_post) + pic("stp-a-text", im.a_text, LY.a_text) + '</div></div>' +
          pic("stp-tray", im.tray, LY.tray) + pic("stp-a-tray", im.a_tray, LY.a_tray) +
          Array.from({ length: maxN }, (_, k)=> '<div class="stp-stamp s' + k + '" style="' + (k < (rounds[0].stamps || []).length ? box(boxes0[k] || boxes0[0]) : 'display:none') + '"><img' + (rounds[0].stamps && rounds[0].stamps[k] ? ' src="' + imgSrc(rounds[0].stamps[k]) + '"' : '') + ' alt="" draggable="false"></div>').join('') +   /* [optimize] a slot round 1 does not use has no src at all (src="" fired an image error) */
          // the standing stamps, each over its "ठप्पा" glow (a baked halo along its outline: images.a_glows, layout.a_glows)
          (im.a_glows || []).map((id, k)=> pic("stp-a-halo h" + k, id, (LY.a_glows || [])[k])).join('') +
          (im.a_stamps || []).map((id, k)=> pic("stp-a-stamp a" + k, id, (LY.a_stamps || [])[k])).join('') +
          '<div class="stp-bird" style="left:' + FT[0] + 'px;top:' + FT[1] + 'px"><div class="stp-bmove">' +
            '<i class="stp-bshd" style="' + box([SH[0] - FT[0], SH[1] - FT[1], SH[2], SH[3]]) + '"></i><i class="stp-blines"><b></b><b></b><b></b></i>' +
            '<div class="stp-btilt"><div class="stp-bclip" style="' + box([BB[0] - FT[0], BB[1] - FT[1], CELL[0], CELL[1]]) + '">' +
              '<img class="stp-bsheet" src="' + imgSrc(im.bird) + '" alt="" draggable="false" style="width:' + (COLS * CELL[0]) + 'px;height:' + (Math.ceil(NF / COLS) * CELL[1]) + 'px"></div></div>' +
          '</div></div>' +
          '<div class="stp-veil"></div>' +
        '</div>');
      const card = host.closest(".tut-card"); if(card) card.classList.add("sfig-full");
      const q_ = (s)=> fig.querySelector(s);
      const root = q_(".stp"), aL = q_(".stp-a"), bO = q_(".stp-bo"), bI = q_(".stp-bi"), aO = q_(".stp-ao"), aI = q_(".stp-ai"),
            aText = q_(".stp-a-text"), tray = q_(".stp-tray"), aTray = q_(".stp-a-tray"),
            stamps = Array.from(fig.querySelectorAll(".stp-stamp")), aStamps = Array.from(fig.querySelectorAll(".stp-a-stamp")), aHalos = Array.from(fig.querySelectorAll(".stp-a-halo")), veil = q_(".stp-veil"),
            bird = q_(".stp-bird"), bMove = q_(".stp-bmove"), bTilt = q_(".stp-btilt"), bLines = q_(".stp-blines"), bSheet = q_(".stp-bsheet");
      // a quad, its corners rounded (rc px: a quadratic curve through each corner), as a clip-path polygon in the layer's own px
      const roundQuad = (Q, rc)=>{ const pts = [];
        for(let i = 0; i < 4; i++){ const p = Q[i], a = Q[(i + 3) % 4], b = Q[(i + 1) % 4], da = Math.hypot(a[0] - p[0], a[1] - p[1]), db = Math.hypot(b[0] - p[0], b[1] - p[1]);
          const p1 = [p[0] + (a[0] - p[0]) * rc / da, p[1] + (a[1] - p[1]) * rc / da], p2 = [p[0] + (b[0] - p[0]) * rc / db, p[1] + (b[1] - p[1]) * rc / db];
          for(let k = 0; k <= 6; k++){ const s = k / 6, u = 1 - s; pts.push([u * u * p1[0] + 2 * u * s * p[0] + s * s * p2[0], u * u * p1[1] + 2 * u * s * p[1] + s * s * p2[1]]); } }
        return "polygon(" + pts.map(q=> q[0].toFixed(1) + "px " + q[1].toFixed(1) + "px").join(",") + ")"; };
      const mid = (Q1, Q2)=> Q1.map((p, i)=> [(p[0] + Q2[i][0]) / 2, (p[1] + Q2[i][1]) / 2]);
      if(LY.a_quad && LY.a_dash) aI.style.clipPath = roundQuad(mid(LY.a_quad, LY.a_dash), 20);
      if(LY.b_quad && LY.b_dash) bI.style.clipPath = roundQuad(mid(LY.b_quad, LY.b_dash), 20);
      fig.querySelectorAll(".stp img").forEach(i=>{ try{ if(i.decode) i.decode().catch(()=>{}); }catch(e){} });
      // each halo pulses with its stamp, about the stamp's base (the same point of the frame)
      aHalos.forEach((h, k)=>{ const s = (LY.a_stamps || [])[k], g = (LY.a_glows || [])[k]; if(s && g) h.style.transformOrigin = (s[0] + s[2] / 2 - g[0]).toFixed(2) + "px " + (s[1] + s[3] - g[1]).toFixed(2) + "px"; });   // every picture decoded now, off the frames that show it first (the bird's sheet, the overhead card)
      state.ownsAudio = true; state.demoRunning = true; setNavActive(false); $("navBtn").style.display = "none";
      setSwMood("talk");
      const alive = ()=> fig.isConnected && CARD.slides[state.idx] === slide;
      const timers = []; const at = (ms, fn)=> timers.push(setTimeout(()=>{ if(alive()) fn(); }, ms));
      // the page's own sounds (the pops, the thud, the finale's chimes, the bird's whoosh), fetched now so each starts on its beat — online
      // too; every round's pictures and clip fetched now too, so a round starts without a load gap
      const sounds = [];
      const mk = (id)=>{ const src = A(id); if(!src) return null; try{ const a = new Audio(src); a.preload = "auto"; a.load(); sounds.push(a); return a; }catch(e){ return null; } };
      const pops = Array.from({ length: maxN }, ()=> mk(sfx.pop)), thud = mk(sfx.press), paperSnd = mk(sfx.paper), glitSnd = mk(sfx.glitter), whoosh = mk(sfx.whoosh);   // [stamp-close] the finale's crackle (L1's) and [stamp-final] its chime; [stamp-868] the whoosh
      [A(d.intro_audio)].concat(rounds.map(R=> A(R.sentence && R.sentence.audio))).forEach(src=>{ if(src) try{ new Audio(src).load(); }catch(e){} });
      rounds.forEach(R=> (R.stamps || []).forEach(id=>{ try{ const i = new Image(); i.src = imgSrc(id); }catch(e){} }));
      [im.final, im.fin_blur].concat(Object.values(im.env || {})).forEach(id=>{ if(id) try{ const i = new Image(); i.src = imgSrc(id); }catch(e){} });   // [stamp-close] the finale's pictures (792:1253, its blurred room, L1's envelope), fetched now
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
      // the gap span where a box sits —, its box(es) with the mark, its stamps' pictures and boxes, the right stamp and its two
      // places over each box. [stamp-868] seen from above, a stamp is taken and judged by its centre (tips) and scales about it:
      // HOVER = over the box's centre, lifted (lift_scale); PRESS = there, pressed down (press_scale)
      // [stamp-drag] the page's state: live = the stamps take drags; acted = the child has taken hold of one; drag = the drag in hand ([stamp-868] declared
      // ahead of setRound: the first round is set as the page mounts)
      let live = false, acted = false, solved = false, hinting = false, drag = null, idleIv = null, lastAct = 0, hintT = [];
      let R = null, r = -1, rWrong = 0, hintStamp = null;   // [vo-rec] the round's wrong drops (its hint ladder); the stamp the guidance holds
      // the box's dashed stroke: the frame's runs (layout.box_dash: each side 7 of the corner's dash, gap 5, 13, 6, 13, 5 — one dash
      // wraps each rounded corner) on a rect 1 px inside the box (its 2 px stroke inside the border, as Figma draws it)
      const DASH = LY.box_dash || "7 5 13 6 13 5 39.13 5 13 6 13 5 39.13 5 13 6 13 5 39.13 5 13 6 13 5 32.13", BR = LY.box_r != null ? LY.box_r : 17;
      function setRound(i){
        r = i; root.dataset.round = i; root.classList.toggle("nopost", (rounds[i] || {}).post === false);   // [stamp-868] 868:74's card has no postmark
        const D = rounds[i] || {}, S = D.sentence || {}, bx = D.boxes || BX0, tips = D.tips || TIPS0,
              se = D.sent || { x: 60, y: 241, w: 1075, h: 73, size: 50, lh: 73 },
              sls = Array.isArray(D.slots) && D.slots.length ? D.slots : [D.slot || { x: 859, y: 226, w: 90, h: 90 }];   // the round's boxes: one, or several (868:59, 868:74)
        const n = (D.stamps || []).length;   // this round's stamps; the divs beyond them are hidden
        stamps.forEach((s, k)=>{ s.className = "stp-stamp s" + k; if(k < n){ s.style.cssText = box(bx[k] || bx[0]); s.querySelector("img").src = imgSrc(D.stamps[k]); } else s.style.cssText = "display:none"; });
        const rows = String(S.text_hi || "").split("\n").length, lh = se.lh || Math.round(se.size * 1.714 * 10) / 10;
        const sentEl = document.createElement("p"); sentEl.className = "stp-sent";
        const pTop = se.y - (lh * rows - se.h) / 2;
        sentEl.style.cssText = 'left:' + se.x + 'px;top:' + pTop + 'px;width:' + se.w + 'px;height:' + (lh * rows) + 'px;font-size:' + se.size + 'px;line-height:' + lh + 'px';
        const pick = D.pick != null ? D.pick : 1, stamp = stamps[pick] || stamps[0];
        // each box: the frame's fill and dashes and its mark (its own, or the round's), its right stamp (its own pick, or the round's)
        // and that stamp's two places over it
        const slots = sls.map(sl=>{ const w = sl.w, h = sl.h, el = document.createElement("div"); el.className = "stp-slot"; el.style.cssText = box([sl.x, sl.y, w, h]);
          const pk = sl.pick != null ? sl.pick : pick, st = stamps[pk] || stamps[0], tp_ = tips[pk] || tips[0], sb_ = bx[pk] || bx[0];
          el.innerHTML = '<svg width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '" aria-hidden="true"><rect x="1" y="1" width="' + (w - 2) + '" height="' + (h - 2) + '" rx="' + (BR - 1) + '" ry="' + (BR - 1) + '" stroke-dasharray="' + DASH + '"/></svg>' +
              '<span class="stp-mark" style="font-size:' + se.size + 'px">' + (sl.mark || D.mark || '?') + '</span>';
          const dx = sl.x + w / 2 - (sb_[0] + tp_[0]), dy = sl.y + h / 2 + P.press_down - (sb_[1] + tp_[1]);
          // [stamp-fit] over a box the stamp is the box's size: fit = the box over the stamp's body at rest (layout.stamp_body), so
          // lifted over it / pressed onto it keep the frames' stamp-to-box proportions (1.1 / .96 of the box)
          const fit = Math.min(w, h) / (LY.stamp_body || Math.min(w, h));
          return { sl, w, h, el, row: sl.row || 0, mark: el.querySelector(".stp-mark"), done: false, pick: pk, stamp: st, fit,
                   HOVER: "translate(" + dx + "px, " + (dy - P.hover_up) + "px) scale(" + (P.lift_scale * fit) + ")", PRESS: "translate(" + dx + "px, " + dy + "px) scale(" + (P.press_scale * fit) + ")" }; });
        // the sign-off (data.sign): small lines under the sentence, shown with its last word
        const signs = (Array.isArray(D.sign) ? D.sign : []).map(sg=>{ const el = document.createElement("p"); el.className = "stp-sign";
          el.style.cssText = 'left:' + sg.x + 'px;top:' + sg.y + 'px;width:' + sg.w + 'px;height:' + sg.h + 'px;font-size:' + sg.size + 'px;line-height:' + sg.h + 'px'; el.textContent = sg.text || ""; return el; });
        root.insertBefore(sentEl, veil); slots.forEach(o=> root.insertBefore(o.el, veil)); signs.forEach(el=> root.insertBefore(el, veil));
        const L = sfigLine(sentEl, S.text_hi, S.word_times, S.audio, S.word_end);
        const gapEl = (wpx)=>{ const g = document.createElement("span"); g.className = "stp-gap"; g.style.width = wpx + "px"; return g; };
        (Array.isArray(se.gap) ? se.gap : se.gap ? [se.gap] : []).forEach(g=>{ if(L.words[g.before]) L.words[g.before].before(gapEl(g.w)); });   // the room a box sits in (or a row's lead)
        if(se.tail) sentEl.appendChild(gapEl(se.tail));                                           // the frame's trailing space: the last row centres a little left
        const s0 = slots[0];   // the first box's places stand for the round's (the guidance glides to it)
        R = { D, S, n, bx, tips, slots, signs, sl: s0.sl, w: s0.w, h: s0.h, sentEl, slot: s0.el, mark: s0.mark, L, pick, stamp, HOVER: s0.HOVER, PRESS: s0.PRESS,
              pLeft: se.x, pTop, lh };
        live = false; acted = false; solved = false; hinting = false; hintT = []; lastAct = Date.now(); rWrong = 0;
      }
      // 1. the table shows as the letter page's veil lifts: [stamp-868] the angled one (868:3). The first round is set at once — its
      //    sentence whole but unseen, posed over the painted one (it takes over in the camera move), its stamps and the overhead tray
      //    unseen, the overhead layer not painted until the move — and the bird glides in
      nextFrame(()=> nextFrame(()=>{ if(alive()) root.classList.add("lit"); }));
      const introSrc = A(d.intro_audio);
      setRound(0);
      const S0 = R.sentEl; S0.classList.add("sfig-whole"); sfigShow(R.L, R.L.words.length); R.L.shown = true;
      // the live sentence's pose in the angled view: its ink box as laid out on the overhead table (layout.b_text_ink) onto the painted
      // one's (layout.a_text_ink), about the p's own top-left; tfAt(F, e) = that pose eased toward its own place (e: 0 -> 1)
      const TXF = (()=>{ const a = LY.a_text_ink, b = LY.b_text_ink; if(!a || !b) return [1, 1, 0, 0];
        const sx = (a[2] - a[0]) / (b[2] - b[0]), sy = (a[3] - a[1]) / (b[3] - b[1]);
        return [sx, sy, a[0] - R.pLeft - sx * (b[0] - R.pLeft), a[1] - R.pTop - sy * (b[1] - R.pTop)]; })();
      const tfAt = (F, e)=> "matrix(" + (F[0] + (1 - F[0]) * e).toFixed(5) + ",0,0," + (F[1] + (1 - F[1]) * e).toFixed(5) + "," + (F[2] * (1 - e)).toFixed(3) + "," + (F[3] * (1 - e)).toFixed(3) + ")";
      S0.style.transformOrigin = "0 0"; S0.style.transform = tfAt(TXF, 0); S0.style.opacity = ".005";
      tray.style.opacity = ".005"; stamps.slice(0, R.n).forEach(s=>{ s.querySelector("img").style.opacity = ".005"; });   // (at .005: painted from the start, unseen — so the move's first frame paints nothing new)   // (the overhead layer paints under the angled one from the start, so the move begins without a first paint)
      // the GPU's first blurs (compiling its blur passes: 30-100 ms of dropped frames in a cold browser, measured) are paid in the page's
      // first 0.3 s, under the letter page's veil, not on the bird's entrance: its lean-blur runs once, unseen (the bird at its resting .005)
      bTilt.animate([{ filter: "blur(2px)" }, { filter: "blur(1px)", offset: .5 }, { filter: "blur(0px)" }], { duration: 300 });
      at(P.bird_at, ()=> zoomBird(false, ()=> at(P.vo_gap, birdTalk)));
      // [stamp-868] the bird's entrance = the reference title page's entrance of its two children (mtg2a01l04s01, PVLanding's zoom; its
      // tempo T 2.2): it fades in 200 px out to the left over the first 15 %, glides in with a 6 px overshoot, leaning into it with a
      // 2 px blur, three speed lines behind it, the dust its feet kick up 400·T ms in, on its whoosh (.75); out = the same moves played
      // backwards (the lines and the dust behind it on the way out), its whoosh too: ending as the bird is gone (whoosh_ms, the file's length)
      const ZM = 680 * P.bird_tempo;
      function zoomBird(out, then){
        if(out) at(Math.max(0, ZM - P.whoosh_ms), ()=> sound(whoosh, P.whoosh_vol)); else sound(whoosh, P.whoosh_vol);   // in: as it appears; out (backwards): ending as it is gone
        const o = (x)=> Object.assign({ duration: ZM, direction: out ? "reverse" : "normal" }, x);
        bMove.animate([{ translate: "-200px 0", opacity: 0 }, { translate: "-160px 0", opacity: 1, offset: .15 },
          { translate: "6px 0", opacity: 1, offset: .75, easing: "ease-in-out" }, { translate: "0 0", opacity: 1 }], o({ easing: "cubic-bezier(.12,.62,.3,1)", fill: "both" }));
        bTilt.animate([{ rotate: "5deg", filter: "blur(2px)" }, { rotate: "4deg", filter: "blur(1px)", offset: .45 },
          { rotate: "-3deg", filter: "blur(0px)", offset: .7 }, { rotate: "0deg", filter: "blur(0px)" }], o({ easing: "ease-out" }));
        bLines.classList.toggle("out", out);
        bLines.animate([{ opacity: 0, scale: ".3 1" }, { opacity: .5, scale: "1 1", offset: .3 }, { opacity: 0, scale: "1.2 1", offset: .65 }, { opacity: 0 }], o({ easing: "ease-out" }));
        at(out ? ZM - 400 * P.bird_tempo : 400 * P.bird_tempo, ()=> dust(out));
        at(ZM, then);
      }
      function dust(out){   // seven puffs from the feet, kicked back against the way it goes
        const s = out ? -1 : 1;
        for(let i = 0; i < 7; i++){
          const e = document.createElement("i"); e.className = "stp-dust";
          e.style.left = (FT[0] - s * 26 + (Math.random() - .5) * 24).toFixed(1) + "px"; e.style.top = (FT[1] - 6) + "px"; root.insertBefore(e, veil);
          const dx = -s * (14 + Math.random() * 44), dy = -(6 + Math.random() * 22);
          e.animate([{ translate: "0 0", scale: ".4", opacity: .85 }, { translate: dx.toFixed(1) + "px " + dy.toFixed(1) + "px", scale: (1.2 + Math.random() * .8).toFixed(2), opacity: 0 }],
                    { duration: 520 + Math.random() * 260, easing: "cubic-bezier(.2,.8,.4,1)", fill: "both" }).onfinish = ()=> e.remove();
        }
      }
      // 2. the instruction, the bird's GIF frame by frame on the clip's own clock — bird_loops loops of its frames over the clip, so it
      //    ends on its first frame, the pose it came in with — and on the clip's "ठप्पा" (pace.thappa, ms) both standing stamps glow and
      //    pulse; 3. at its end the bird goes out; 4. the camera move; 5. round 1's sentence read
      let bf = -1;
      const birdFrame = (i)=>{ if(i === bf) return; bf = i; bSheet.style.transform = "translate(" + (-(i % COLS) * CELL[0]) + "px," + (-Math.floor(i / COLS) * CELL[1]) + "px)"; };
      function birdTalk(){
        let done = false, glow = false; const t0 = performance.now(), file = introSrc ? introSrc.split("/").pop() : "";
        const end = ()=>{ if(done || !alive()) return; done = true; birdFrame(0);
          at(P.exit_gap, ()=> zoomBird(true, ()=> at(P.cam_gap, ()=> camera(()=> at(P.read_gap, ()=> stage4(true)))))); };
        play(introSrc, end);
        const a0 = currentAudio;
        const mine = ()=> !!a0 && a0 === currentAudio && decodeURIComponent(String(a0.currentSrc || a0.src || "").split("/").pop()) === file;
        const tick = ()=>{
          if(done || !alive()) return;
          const own = mine(), t = own ? a0.currentTime : (performance.now() - t0) / 1000, dur = own && isFinite(a0.duration) && a0.duration > 0 ? a0.duration : P.intro_ms / 1000;
          birdFrame(Math.floor(Math.min(t / dur, 0.9999) * P.bird_loops * NF) % NF);
          if(!glow && t * 1000 >= P.thappa){ glow = true; aStamps.concat(aHalos).forEach(s=> s.classList.add("thappa")); }   // the halo glows up, both pulse
          requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        at(authoredVoHoldMs(introSrc) + 10000, ()=>{ if(!done){ stopAudio(); end(); } });
      }
      // 4. the camera move (cam_ms), on the page's own frames: the card's corners glide from 868:3's (layout.a_quad, the paper's edges
      //    fitted on its render) to 868:17's (layout.b_quad), eased, and each table layer is drawn through the projective map that takes
      //    ITS card onto them (homog: four points onto four, carried by matrix3d), so the two drawings move as one table, the angled one
      //    fading over the overhead one (cam_a); the trays and the stamps change where they stand (the two frames have them in the same
      //    spots): the angled tray fades over the overhead one, each standing stamp settles onto its base (squashing to cam_squash, as
      //    seen from above) as the overhead stamp comes in; the live sentence takes over from the painted one in the first beat
      //    (cam_text, the two still one) and glides to its own place
      const homog = (s, q)=>{
        const M = [], v = [];
        for(let i = 0; i < 4; i++){ const x = s[i][0], y = s[i][1], u = q[i][0], w = q[i][1];
          M.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); v.push(u); M.push([0, 0, 0, x, y, 1, -w * x, -w * y]); v.push(w); }
        for(let c = 0; c < 8; c++){
          let p = c; for(let k = c + 1; k < 8; k++) if(Math.abs(M[k][c]) > Math.abs(M[p][c])) p = k;
          const tm = M[c]; M[c] = M[p]; M[p] = tm; const tv = v[c]; v[c] = v[p]; v[p] = tv;
          for(let k = 0; k < 8; k++){ if(k === c) continue; const f = M[k][c] / M[c][c]; if(!f) continue; for(let j = c; j < 8; j++) M[k][j] -= f * M[c][j]; v[k] -= f * v[c]; }
        }
        return v.map((x, i)=> x / M[i][i]);
      };
      const m3d = (h)=> "matrix3d(" + [h[0], h[3], 0, h[6], h[1], h[4], 0, h[7], 0, 0, 1, 0, h[2], h[5], 0, 1].map(x=> +x.toFixed(9)).join(",") + ")";
      const ease = (t)=> t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      const sstep = (a, b, t)=>{ const x = Math.max(0, Math.min(1, (t - a) / (b - a))); return x * x * (3 - 2 * x); };
      const boxTf = (fr, to)=> "matrix(" + (to[2] / fr[2]).toFixed(5) + ",0,0," + (to[3] / fr[3]).toFixed(5) + "," + (to[0] - fr[0]).toFixed(2) + "," + (to[1] - fr[1]).toFixed(2) + ")";   // a box onto another (origin 0 0)
      function camera(then){
        const QA = LY.a_quad, QB = LY.b_quad, DA = LY.a_dash || QA, DB = LY.b_dash || QB, TA = LY.a_tray, TB = LY.tray, AS = LY.a_stamps || [], SB = R.bx, D = P.cam_ms;
        const CT = P.cam_tray || [.2, .5, .3, .6], CS = P.cam_stamps || [.25, .6, .1, .45];   // [in from, in to, out from, out to] (fractions of the move)
        const AB = LY.a_bases || AS.map(b=> [b[0] + b[2] / 2, b[1] + b[3]]), imgs = stamps.slice(0, R.n).map(s=> s.querySelector("img"));
        if(!QA || !QB || !TA || !TB){ bI.remove(); aL.remove(); aTray.remove(); aStamps.concat(aHalos).forEach(s=> s.remove()); bird.remove(); tray.style.opacity = ""; S0.style.opacity = ""; S0.style.transform = ""; imgs.forEach(i=>{ i.style.opacity = ""; i.classList.add("shown"); }); then(); return; }
        aTray.style.transformOrigin = tray.style.transformOrigin = "0 0";
        aStamps.forEach((s, k)=>{ const b = AS[k]; if(b && AB[k]) s.style.transformOrigin = (AB[k][0] - b[0]).toFixed(2) + "px " + (AB[k][1] - b[1]).toFixed(2) + "px"; });
        const t0 = performance.now();
        const step = (now)=>{
          if(!alive()) return;
          const t = Math.min(1, Math.max(0, (now - t0) / D)), e = ease(t);
          const lq = (Q1, Q2)=> Q1.map((p, i)=> [p[0] + (Q2[i][0] - p[0]) * e, p[1] + (Q2[i][1] - p[1]) * e]), Qp = lq(QA, QB), Qd = lq(DA, DB);
          bO.style.transform = m3d(homog(QB, Qp)); bI.style.transform = m3d(homog(DB, Qd)); aO.style.transform = m3d(homog(QA, Qp)); aI.style.transform = m3d(homog(DA, Qd));
          aL.style.opacity = (1 - sstep(P.cam_a[0], P.cam_a[1], t)).toFixed(4);
          aText.style.opacity = (1 - sstep(0, P.cam_text, t)).toFixed(4); S0.style.opacity = Math.max(.005, sstep(0, P.cam_text, t)).toFixed(4); S0.style.transform = tfAt(TXF, e);
          const tb = TA.map((v, i)=> v + (TB[i] - v) * e); aTray.style.transform = boxTf(TA, tb); tray.style.transform = boxTf(TB, tb);
          aTray.style.opacity = (1 - sstep(CT[2], CT[3], t)).toFixed(4); tray.style.opacity = Math.max(.005, sstep(CT[0], CT[1], t)).toFixed(4);
          aStamps.forEach((s, k)=>{ const sb = SB[k], ab = AB[k]; if(!sb || !ab) return;
            const es = sstep(0, CS[3], t);   // it settles onto its base by the time it has faded
            s.style.transform = "translate(" + ((sb[0] + sb[2] / 2 - ab[0]) * es).toFixed(2) + "px," + ((sb[1] + sb[3] / 2 - ab[1]) * es).toFixed(2) + "px) scale(1," + (1 - (1 - P.cam_squash) * es).toFixed(4) + ")";
            s.style.opacity = (1 - sstep(CS[2], CS[3], t)).toFixed(4); });
          imgs.forEach(i=>{ i.style.opacity = Math.max(.005, sstep(CS[0], CS[1], t)).toFixed(4); i.style.transform = "scale(" + (.94 + .06 * e).toFixed(4) + ")"; });
          if(t < 1){ requestAnimationFrame(step); return; }
          // the overhead table, as drawn: the angled one, the bird and the painted sentence go; every layer back on its own place
          bO.style.transform = ""; bI.remove(); aL.remove(); aTray.remove(); aStamps.concat(aHalos).forEach(s=> s.remove()); bird.remove();
          tray.style.transform = ""; tray.style.opacity = ""; tray.style.transformOrigin = "";
          S0.style.opacity = ""; S0.style.transform = ""; S0.style.transformOrigin = ""; S0.classList.remove("sfig-whole");
          imgs.forEach(i=>{ i.style.opacity = ""; i.style.transform = ""; i.classList.add("shown"); });
          then();
        };
        requestAnimationFrame(step);
      }
      // 3. (a later round) the round's stamps (two, or three) pop into the tray, each on its pop
      function stage3(){
        const n = R.n;
        stamps.slice(0, n).forEach((s, k)=> at(k * P.pop_gap, ()=>{ const img = s.querySelector("img"); sound(pops[k], 0.48);   // 60 % of the first build's .8
          img.addEventListener("animationend", ()=>{ img.classList.remove("pop"); img.classList.add("shown"); }, { once: true }); img.classList.add("pop"); }));
        at((n - 1) * P.pop_gap + P.sent_at, stage4);
      }
      // 5. the sentence rises in whole — the sign-off with it — and is read SENT_IN_MS later, each word lit as it is read ([word-sync]);
      //    [stamp-868] round 1's is already there (it came through the camera move): read at once
      function stage4(shown){ const C = R, L = C.L; if(shown !== true) sfigRise(L, C.signs); at(shown === true ? 0 : SENT_IN_MS, ()=>{ narrate(L.src, [], ()=>{}, stage5); sfigSync(L); }); }
      // 6. the empty box(es) appear and blink (blink_ms: blinks times, appearing and disappearing); from this moment the stamps are the
      //    child's to drag (.live); in a round with `guide`, 0.5 s after the blink the guidance, unless the child has already taken hold of a stamp
      function stage5(){
        const slots = R.slots, guide = R.D.guide !== false;
        slots.forEach(o=>{ o.el.style.animationDuration = (P.blink_ms / P.blinks) + "ms"; o.el.classList.add("in", "blink"); });   // all together, when there are several
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
      // [vo-rec] a later round opens with its own instruction (rounds[i].intro_audio: the deck's line for that round) before its
      // stamps pop in; the idle reminder says that line too. [l2-quiet] (2026-11-04) data.intro_on_idle: a later round does NOT open
      // with it — its stamps pop in at once — and the line is said only by the idle reminder, after 7 s without a touch
      const roundSrc = ()=> (R && R.D.intro_audio) ? A(R.D.intro_audio) : introSrc;
      function roundIntro(then){ const src = R && R.D.intro_audio && !d.intro_on_idle ? A(R.D.intro_audio) : null; if(!src){ then(); return; }
        let done = false; const go = ()=>{ if(done || !alive()) return; done = true; at(P.after_intro, then); };
        play(src, go); at(authoredVoHoldMs(src) + 10000, ()=>{ if(!done){ stopAudio(); go(); } }); }
      function remind(){
        if(solved || drag || !live || isPlaying){ lastAct = Date.now(); return; }
        lastAct = Date.now(); play(roundSrc(), ()=>{ lastAct = Date.now(); });   // [vo-rec] the round's line
      }
      const move = (el, tf, ms, ease)=>{ el.style.transition = "transform " + ms + "ms " + ease + ", filter .3s"; el.style.transform = tf; };
      // glides a stamp home and sets it down (its shadow goes as it lands) — unless the child has taken hold of it again
      const putBack = (s, ms)=>{ move(s, "none", ms, "cubic-bezier(.4,0,.2,1)"); at(Math.max(0, ms - 150), ()=>{ if(!(drag && drag.el === s)) s.classList.remove("lift"); }); };
      // 6. the guidance: the right stamp lifts, glides SLOWLY over the box, hovers there and glides home — it does not print (that
      //    is the child's to do); stopped where it is the moment the child takes hold of a stamp
      const hat = (ms, fn)=>{ const id = setTimeout(()=>{ if(alive() && hinting) fn(); }, ms); hintT.push(id); timers.push(id); };
      function hint(force){   // [vo-rec] force = hint 3's glide in a round without guidance; the glide goes to the OPEN slot's stamp
        if(hinting || solved || drag || !live || !R || (R.D.guide === false && !force)) return;
        const o = R.slots.find(q=> !q.done) || R.slots[0], stamp = o.stamp, HOV = o.HOVER; hinting = true; hintT = []; hintStamp = stamp;
        stamp.classList.add("lift"); guideGlide(stamp, o, P.glide);   // [stamp-fit] was move(stamp, HOV, P.glide, "cubic-bezier(.45,0,.2,1)")
        hat(P.glide + P.hold, ()=> move(stamp, "none", P.back, "cubic-bezier(.4,0,.2,1)"));
        hat(P.glide + P.hold + P.back - 150, ()=> stamp.classList.remove("lift"));
        hat(P.glide + P.hold + P.back + 50, ()=>{ hinting = false; lastAct = Date.now(); });
      }
      function stopHint(taken){   // taken = the child took hold of the guiding stamp itself (it stays where it is, in hand)
        if(!hinting) return; hinting = false; hintT.forEach(clearTimeout); hintT = [];
        if(!taken) putBack(hintStamp || R.stamp, 350);
      }
      // [stamp-fit] the guidance's glide over the box, as a hand would drag it: the stamp's centre along the old glide's path and curve
      // (cubic-bezier(.45,0,.2,1), glide ms) frame by frame, its size the drag's (sizeAt: lifted as it leaves the tray — over its first
      // 15 % —, the box's own size as it nears the box), ending exactly on the box's HOVER; it stops where it is once the guidance stops
      // (a child taking hold of it finds it at the size a drag gives there: no jump)
      const easeGlide = ((x1, y1, x2, y2)=> (x)=>{ if(x <= 0) return 0; if(x >= 1) return 1; let lo = 0, hi = 1, t = x;
        for(let i = 0; i < 24; i++){ t = (lo + hi) / 2; const bx = 3 * (1 - t) * (1 - t) * t * x1 + 3 * (1 - t) * t * t * x2 + t * t * t; if(bx < x) lo = t; else hi = t; }
        return 3 * (1 - t) * (1 - t) * t * y1 + 3 * (1 - t) * t * t * y2 + t * t * t; })(.45, 0, .2, 1);
      function guideGlide(stamp, o, ms){
        const k = stamps.indexOf(stamp), from = curXY(stamp), mm = String(o.HOVER).match(/translate\(([-\d.e]+)px, ([-\d.e]+)px\)/), to = mm ? [+mm[1], +mm[2]] : [0, 0];
        const v = (getComputedStyle(stamp).transform || "").match(/matrix\(([^)]+)\)/), a = v ? v[1].split(",").map(Number) : null, s0 = a ? (Math.hypot(a[0], a[1]) || 1) : 1;
        const t0 = performance.now(); stamp.style.transition = "filter .3s";
        const step = (now)=>{
          if(!alive() || !hinting || hintStamp !== stamp) return;
          const u = Math.min(1, (now - t0) / ms), e = easeGlide(u), x = from[0] + (to[0] - from[0]) * e, y = from[1] + (to[1] - from[1]) * e;
          setTf(stamp, x, y, +(s0 + (sizeAt(k, x, y) - s0) * Math.min(1, u / 0.15)).toFixed(4));
          if(u < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      }
      // the child's drags: a stamp follows the finger from where it is (even mid-guidance, mid-return) at the lifted size; the
      // frame's px from the screen's through the stage's scale; the drop is judged by the stamp's centre (tips) against the box's
      const scaleNow = ()=> (root.getBoundingClientRect().width || 1280) / 1280;
      const curXY = (el)=>{ const m = getComputedStyle(el).transform, v = m && m !== "none" ? m.match(/matrix\(([^)]+)\)/) : null;
        if(!v) return [0, 0]; const a = v[1].split(",").map(Number); return [a[4] || 0, a[5] || 0]; };
      const setTf = (el, tx, ty, s)=>{ el.style.transform = "translate(" + tx.toFixed(2) + "px, " + ty.toFixed(2) + "px) scale(" + s + ")"; };
      // [stamp-fit] the size of a stamp in hand at (lx, ly): lift_scale away from the boxes; as its centre nears an empty box's drop zone
      // (tol_x / tol_y round the box's centre) it shrinks smoothly to the box's own size (fit), which it has all over the zone; the
      // nearest empty box decides (its distance outside the zone, the larger of the two axes'); a function of where the stamp is, so it
      // never jumps and grows back the same way as it is taken off
      const sizeAt = (k, lx, ly)=>{
        if(!R) return P.lift_scale;
        const b = R.bx[k] || R.bx[0], tp = R.tips[k] || R.tips[0], cx = b[0] + tp[0] + lx, cy = b[1] + tp[1] + ly; let near = null;
        R.slots.forEach(o=>{ if(o.done) return; const m = Math.max(Math.abs(cx - (o.sl.x + o.w / 2)) - P.tol_x, Math.abs(cy - (o.sl.y + o.h / 2)) - P.tol_y, 0); if(!near || m < near.m) near = { m, o }; });
        if(!near) return P.lift_scale;
        const e = Math.min(1, near.m / Math.max(1, P.fit_ramp != null ? P.fit_ramp : 60)), t = e * e * (3 - 2 * e);   // 0 in the zone, 1 fit_ramp px out
        return +(P.lift_scale * (near.o.fit + (1 - near.o.fit) * t)).toFixed(4);
      };
      // [stamp-fit] a drop with the stamp's centre on the tray (layout.tray_drop: its drawn body, 30 px larger, down to the stage's bottom)
      const onTray = (x, y)=>{ const z = LY.tray_drop; return !!z && x >= z[0] && x <= z[2] && y >= z[1] && y <= z[3]; };
      stamps.forEach((s, k)=>{
        s.addEventListener("pointerdown", (e)=>{
          if(!live || solved || drag || !R || (e.button != null && e.button > 0)) return;
          e.preventDefault(); acted = true; lastAct = Date.now();
          if(hinting) stopHint(s === hintStamp);
          const xy = curXY(s); s.style.transition = "none"; s.classList.remove("stp-wrong"); s.classList.add("lift", "drag"); setTf(s, xy[0], xy[1], sizeAt(k, xy[0], xy[1]));   // [stamp-fit] its size where it is taken (was lift_scale)
          drag = { el: s, k, id: e.pointerId, x0: e.clientX, y0: e.clientY, tx: xy[0], ty: xy[1], sc: scaleNow(), moved: 0, lx: xy[0], ly: xy[1] };
          try{ s.setPointerCapture(e.pointerId); }catch(err){}
        });
        s.addEventListener("pointermove", (e)=>{
          if(!drag || drag.el !== s || e.pointerId !== drag.id) return;
          const dx = (e.clientX - drag.x0) / drag.sc, dy = (e.clientY - drag.y0) / drag.sc;
          drag.moved = Math.max(drag.moved, Math.hypot(dx, dy)); drag.lx = drag.tx + dx; drag.ly = drag.ty + dy;
          setTf(s, drag.lx, drag.ly, sizeAt(k, drag.lx, drag.ly));   // [stamp-fit] the box's size near a box (was lift_scale throughout)
        });
        const up = (e)=>{
          if(!drag || drag.el !== s || e.pointerId !== drag.id) return;
          const dr = drag; drag = null; try{ s.releasePointerCapture(e.pointerId); }catch(err){}
          s.classList.remove("drag"); lastAct = Date.now();
          if(e.type === "pointercancel" || dr.moved < P.tap_px){ putBack(s, 220); return; }   // a touch (or the browser took the pointer), not a placing
          const b = R.bx[k] || R.bx[0], tp = R.tips[k] || R.tips[0], tipX = b[0] + tp[0] + dr.lx, tipY = b[1] + tp[1] + dr.ly;   // the stamp scales about its centre: the centre rides the translate
          // the box the stamp is on: of the boxes still empty, one within tol_x / tol_y of its centre (the nearer, when two are)
          const dist = (o)=> Math.hypot(tipX - (o.sl.x + o.w / 2), tipY - (o.sl.y + o.h / 2));
          const hit = R.slots.filter(o=> !o.done && Math.abs(tipX - (o.sl.x + o.w / 2)) <= P.tol_x && Math.abs(tipY - (o.sl.y + o.h / 2)) <= P.tol_y).sort((a, c)=> dist(a) - dist(c))[0];
          if(!hit && onTray(tipX, tipY)){ putBack(s, P.reset); return; }   // [stamp-fit] dropped on / by the tray: home in silence, no attempt
          if(hit && k === hit.pick) solve(hit); else wrong(s);
        };
        s.addEventListener("pointerup", up); s.addEventListener("pointercancel", up);
      });
      // a wrong drop (off the box, or the wrong stamp on it): the kit's incorrect buzz (the user's standard sfx_incorrect_feedback),
      // a wiggle where it was dropped, then it glides back to its place; the stamps stay the child's. The class is stp-wrong, never
      // a bare "wrong": the engine's style.css paints ANY .wrong element white (:is(.wrong,...){background-color:#fff!important})
      function wrong(s){
        state.attempts = (state.attempts || 0) + 1; sfxWrongSoft();
        rWrong++;   // [vo-rec] the deck's ladder: 1st = the wiggle alone; 2nd = hint 2's line; 3rd and later = hint 3's line (the open slot's own, by its mark) + the guidance glide
        if(rWrong >= 2){ const D = R.D, open = R.slots.find(q=> !q.done), mk = open ? String(open.mark.textContent || "").trim() : "";
          const id = rWrong === 2 ? D.hint2_audio : ((D.hint3_by_mark && D.hint3_by_mark[mk]) || D.hint3_audio || D.hint2_audio);
          at(P.wiggle + P.reset, ()=>{ if(drag || solved || isPlaying) return; if(id) play(A(id), ()=>{ lastAct = Date.now(); }); if(rWrong >= 3) hint(true); }); }
        s.classList.remove("stp-wrong"); void s.offsetWidth; s.classList.add("stp-wrong");
        at(P.wiggle, ()=>{ if(!(drag && drag.el === s)){ s.classList.remove("stp-wrong"); putBack(s, P.reset); } });
      }
      // the right drop: the stamp snaps over the box and presses onto it on the thud — the mark is printed there, on its row's
      // baseline — lifts and glides home; the box goes on the correct chime (the user's standard sfx_correct_feedback), the mark
      // stays; the kit's confetti on its sound (the user's standard sfx confetti); then the next round, or the page moves on
      function solve(o){
        const C = R, stamp = o.stamp, last = C.slots.every(q=> q === o || q.done);   // the box's own stamp; the round's last empty box? (one box: always)
        o.done = true; solved = true; live = false; root.classList.remove("live"); C.slots.forEach(q=> q.el.classList.remove("blink")); hintT.forEach(clearTimeout);
        if(last && idleIv){ clearInterval(idleIv); idleIv = null; }
        move(stamp, o.HOVER, P.snap, "cubic-bezier(.2,0,.2,1)");
        at(P.snap, ()=> move(stamp, o.PRESS, P.press, "cubic-bezier(.5,0,1,1)"));
        at(P.thud_at, ()=> sound(thud, P.thud_vol != null ? P.thud_vol : 0.9));   // [stamp-box] pace.thud_vol (.54: 40 % below the .9 it was)
        at(P.mark_at, ()=>{ centreInk(o.mark, o); o.mark.classList.add("in"); });
        at(P.lift_at, ()=> move(stamp, o.HOVER, 180, "cubic-bezier(0,0,.3,1)"));
        at(P.back_at, ()=> putBack(stamp, P.back_home));
        // the box goes on the chime; with a box still empty (868:59's other row, 868:74's others) the stamps are the child's again from
        // here — no confetti yet; the idle count starts over (the title's line after 7 s, as in any later round)
        at(P.gone_at, ()=>{ o.el.classList.add("gone"); sfxCorrect(); if(last && d.ok_audio) play(A(d.ok_audio), ()=>{}); /* [vo-rec] "शाबाश!" with the round's chime */ if(!last && R === C){ solved = false; live = true; root.classList.add("live"); lastAct = Date.now(); } });
        if(!last) return;
        at(P.confetti_at, ()=> confettiCannon());
        at(P.done_at, ()=>{ if(r + 1 < rounds.length) clearRound(C); else finale(); });   // [stamp-final] after the last round, the finale
      }
      // [stamp-close] after the last round's confetti, the finale: the letter page's envelope transition played BACKWARDS — the veil
      // falls over the table and lifts off the sheet filling the screen (where L1's dive ended); the view pulls back out of the
      // envelope (the sheet's ruled lines coming back), the sheet sinks into the pocket, the flap comes down on L1's paper crackle
      // (sfx.paper) and the seal comes back: the envelope closed, full screen, over the room of Figma 792:1253 blurred (images.fin_blur);
      // then — L1's zoom backwards — it shrinks into Pinki's raised hand (layout.hand: the drawing's envelope laid onto the picture's,
      // their hearts on one spot) as the room comes into focus (images.final, the frame's picture), the drawing's envelope dissolving into
      // the picture's own as it lands; fin_glitter_at later [stamp-final] the envelope there glitters gold for fin_glitter_ms on its chime,
      // and fin_done after it the page hands over to the end screen. Every beat comes at the moment that mirrors L1's: L1's moment t
      // after its tap (pace.close = L1's pace + its CSS lengths) at R0 + T - t on a clock that starts when the veil is full (T = L1's tap
      // to its page change; R0 = this clock's mirror of that change: the hold, less the forward's last 50 ms, when its veil was already
      // full); the curves are mirrored in the CSS (.ltr-rev). The layer is built in L1's end state (zoomed, open, the sheet risen, dived
      // in) the moment the veil's fall has really ended (its transitionend — a transition starts in the frame that resolves its class
      // change, which can come 30+ ms after it: a fixed timer showed the sheet through a veil still at 95 %; a fallback timer if the end is
      // never reported), and painted (decoded) in the hold, unseen: built as the veil began to fall, its first paint (six large pictures,
      // the box at 5.2x) cost 50-84 ms frames on the fall's first beats
      function finale(){
        const C = Object.assign({ zoom: 1200, paper_at: 350, dive_at: 700, dive: 1700, dive_scale: 5.2, veil_at: 1900, done_at: 2450,
          veil_ms: 500, sheet_ms: 900, flap_ms: 1000, seal_ms: 350, lines_ms: 1200, blur_ms: 900 }, P.close || {});
        const T = C.zoom + C.done_at, R0 = P.close_hold - (T - (C.zoom + C.veil_at + C.veil_ms)), m = (t)=> R0 + T - t;   // from the full veil
        const full = LY.env_full || [71, -50, 1138, 758], mo = LY.env_mouth || [568.8, 292.4], HD = LY.hand || {}, hc = HD.c || [592.47, 393.24], ht = HD.to || [810.54, 172.47],
              EB = LY.envelope || [741, 109, 139, 125], env = im.env || {}, ei = (cls, id)=> '<img class="' + cls + '" src="' + imgSrc(id) + '" alt="" draggable="false">';
        const fin = document.createElement("div"); fin.className = "stp-close ltr ltr-rev zoom letter-in paper dive";   // L1's classes as its transition ends
        fin.innerHTML = pic("stp-fin-pic", im.final, LY.final || [0, -1, 1280, 721]) + ei("ltr-blur", im.fin_blur) +
          '<div class="ltr-env-pos" style="' + box(full) + '"><div class="ltr-env-grow"><div class="ltr-env-pulse"><div class="ltr-env3d">' +
            ei("ltr-inner", env.inner) + '<div class="ltr-paper"></div>' + ei("ltr-body", env.body) + '<div class="ltr-flap">' + ei("", env.flap) + '</div>' + ei("ltr-heart", env.heart) +
          '</div></div></div></div><div class="stp-glit" style="' + box(EB) + '"></div>';
        const ep = fin.querySelector(".ltr-env-pos");
        // L1's dive (its box scaled about the mouth's centre, which lands on the frame's centre) and the landing: the box about the
        // drawing's envelope's centre (hand.c, box px) carried onto the picture's envelope's centre (hand.to, frame px), turned and scaled
        ep.style.setProperty("--ltr-dive", "translate(" + (640 - full[0] - C.dive_scale * mo[0]) + "px, " + (360 - full[1] - C.dive_scale * mo[1]) + "px) scale(" + C.dive_scale + ")");
        ep.style.setProperty("--ltr-icon", "translate(" + (ht[0] - full[0] - hc[0]).toFixed(2) + "px, " + (ht[1] - full[1] - hc[1]).toFixed(2) + "px) rotate(" + (HD.rot || 0) + "deg) scale(" + (HD.scale || 0.12) + ")");
        ep.style.setProperty("--ltr-ho", hc[0] + "px " + hc[1] + "px");
        [["--ltr-dive-ms", C.dive], ["--ltr-zoom-ms", C.zoom], ["--ltr-lines-delay", C.dive - C.lines_ms], ["--ltr-blur-delay", C.zoom - C.blur_ms], ["--ltr-land-ms", P.land_ms]]
          .forEach(([k, v])=> fin.style.setProperty(k, v + "ms"));
        veil.style.setProperty("--stp-veil-fall", P.close_veil + "ms"); veil.style.setProperty("--stp-veil-lift", C.veil_ms + "ms");
        veil.classList.add("fall");                                                       // the veil falls over the table (its lift as this page began, backwards; the class on the veil alone: on the page's root it re-styled the whole page)
        // the veil is full when its fall has really ended (its transitionend; a fallback timer if that is never reported): the layer goes
        // in under it, the sheet as L1's dive left it, and the beats run from there
        let veilFull = false;
        const onEnd = (e)=>{ if(e.target === veil && e.propertyName === "opacity") onFull(); };
        const onFull = ()=>{ if(veilFull || !alive()) return; veilFull = true; veil.removeEventListener("transitionend", onEnd);
          root.insertBefore(fin, veil); fin.querySelectorAll("img").forEach(i=>{ try{ if(i.decode) i.decode().catch(()=>{}); }catch(e){} });
          at(m(C.zoom + C.veil_at + C.veil_ms), ()=> veil.classList.add("lift"));          // the veil lifts off it as ...
          at(m(C.zoom + C.dive_at + C.dive), ()=> fin.classList.remove("dive"));           // ... the view pulls back out of the envelope (its ruled lines come back)
          at(m(C.zoom + C.paper_at + C.sheet_ms), ()=> fin.classList.remove("paper"));      // the sheet sinks into the pocket
          at(m(C.zoom + C.flap_ms), ()=> fin.classList.add("shut"));                        // the flap comes down ...
          at(m(C.zoom + C.flap_ms) + P.close_paper_at, ()=> sound(paperSnd, 0.7));          // ... on L1's paper crackle (its burst on the fall and the seal)
          at(m(C.zoom + C.seal_ms), ()=> fin.classList.add("seal"));                        // the seal comes back: closed, as drawn
          at(m(C.zoom), ()=> fin.classList.remove("zoom"));                                 // it shrinks into her hand as the room comes into focus
          at(m(0) - P.land_lead, ()=> fin.classList.add("land"));                           // the drawing's envelope dissolves into the picture's own
          at(m(0) + P.fin_glitter_at, ()=>{ glitter(fin.querySelector(".stp-glit"), EB[2], EB[3]); sound(glitSnd, 0.7); });   // [stamp-final] the glitter, as before
          at(m(0) + P.fin_glitter_at + P.fin_glitter_ms + P.fin_done, ()=>{ state.demoRunning = false; completeSlide(true); });
        };
        veil.addEventListener("transitionend", onEnd); at(P.close_veil + 400, onFull);
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
      // word in reverse (the arrival's opposite) and the box fades with its mark; then the next round is set and its stamps pop in
      function clearRound(C){
        stamps.slice(0, C.n).forEach((s, k)=> at(k * P.pop_gap, ()=>{ const img = s.querySelector("img"); img.classList.remove("shown");
          img.addEventListener("animationend", ()=>{ img.classList.remove("unpop"); }, { once: true }); img.classList.add("unpop"); }));
        C.signs.forEach(el=> el.classList.remove("on"));   // the sign-off came with the last word: it goes first
        C.L.words.slice().reverse().forEach((wd, i)=> at(i * P.words_out, ()=> wd.classList.remove("on")));
        C.slots.forEach(o=> o.el.classList.add("out"));
        at(P.next_at, ()=>{ C.sentEl.remove(); C.slots.forEach(o=> o.el.remove()); C.signs.forEach(el=> el.remove()); setRound(r + 1); roundIntro(stage3); });   // [vo-rec] the round's own instruction first
      }
      // the mark's INK across on the box's centre (the demos' centreInk): the glyph's ink is not centred in its own line box, so it is
      // shifted by its ink's offset, measured from the font itself (style.css: --ix / --iy); [stamp-868] and, in a box bigger than the
      // mark (90 px for a 44-50 px line), down onto its row's baseline (o.row of the round's sentence: its line box's top + the half
      // leading + the font's ascent), as if typed in the sentence — not at the box's middle, which the frames set for the box's look
      function centreInk(markEl, o){
        try{
          const cs = getComputedStyle(markEl), c = document.createElement("canvas").getContext("2d");
          c.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
          const t = c.measureText(markEl.textContent);
          if(!t.width || !isFinite(t.fontBoundingBoxAscent)) return;
          const asc = t.fontBoundingBoxAscent, desc = t.fontBoundingBoxDescent, base = (markEl.offsetHeight - asc - desc) / 2 + asc;
          const ix = (t.actualBoundingBoxRight - t.actualBoundingBoxLeft) / 2 - markEl.offsetWidth / 2;
          let iy = base + (t.actualBoundingBoxDescent - t.actualBoundingBoxAscent) / 2 - markEl.offsetHeight / 2;
          if(o && R && R.lh){ const rowBase = R.pTop + o.row * R.lh + (R.lh - asc - desc) / 2 + asc - o.sl.y; iy = o.h / 2 - markEl.offsetHeight / 2 + base - rowBase; }
          markEl.style.setProperty("--ix", ix.toFixed(2) + "px"); markEl.style.setProperty("--iy", iy.toFixed(2) + "px");
        }catch(e){}
      }
    }
  },


  CELEBRATION: {
    mount(host, slide){}   /* [optimize] replaced at load by the celebration port (SlideModules.CELEBRATION.mount = ...) */
  },

  /* ===== 16j: FLN sentence + repeated-sound modules — PORTED from the delivered 15b/15d engines.
     Fingerprinted first (two-diverged-engines lesson): same `-unified` lineage, IDENTICAL helper
     contracts (audioFor, setNavActive, completeSlide, mountTapOptions, state fields, sfxCorrect, sfxWrongSoft,
     confettiCannon/setSwMood/imgOrEmoji/letterCell/pictureCell). Verified each call resolves in 16i
     before porting — not a blind paste. Used by HI01H06 (READ/FIND/PICK_PIC) + HIKGH02_L01_S03_P2
     (SOUND/TAP_ALL). ===== */




  /* 16j NEW: sentence -> pick the matching picture (HI01H06 "वाक्य के लिए सही चित्र चुनो"). Sentence
     chips as the stimulus + 2 picture options via the tap-to-answer contract. */
};

/* VACHAN (एकवचन/बहुवचन) + any 2-category attribute reuse the GENERIC gender modules — identical
   mechanic, just different labels. A vachan game authors these types with the category in the
   "gender" field (e.g. "S"/"P"), the two labels, and (for pairs) f=singular / m=plural; it then
   inherits immediate tap-to-answer feedback, speak-word-on-tap, layered hints, and the engine
   guard for free. Named *_VACHAN (not *_NUMBER) to avoid colliding with MEET_NUMBER = counting. */

SlideModules.PUNCT_PICK            = { mount(host, slide){ return ((slide.data || {}).scene ? SlideModules.PUNCT_SCENE : SlideModules.PUNCT_DEMO).mount(host, slide); } };   // [pick-fig] the run-on demo's page with the tap left to the child (no page now); [g1-scene] G1, [g2-scene] G2 and [g3-scene] G3 (data.scene): the scene module's page, its tiles the child's

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
  document.querySelectorAll(".slide-stage .reveal-hand").forEach(h=> h.remove());   // [tap-lock] no page's pointing hand outlives it

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
  const isTut = ((slide.phase === "tutorial" || slide.type === "PUNCT_PICK" || slide.type === "LETTER_STORY" || slide.type === "STAMP_DEMO") && slide.type !== "PHASE_TRANSITION" && slide.type !== "CELEBRATION");
  $("stage").classList.toggle("tut", isTut);
  document.body.classList.toggle("tut-page", isTut);
  $("stage").classList.toggle("sent-page", slide.type === "SENT_PICK");   // [sent-fig] G4, P1 + P2: the reference P4's header + page look
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
function phaseBlurTransition(cb){ if(cb) cb(); }   /* [optimize] replaced at load by [GATE-REF-ANIM]'s gate (window.phaseBlurTransition) */

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
  /* [gate-p2] the round-3 gate ("अब आपकी बारी!") follows the page CARD.round3_gate_after (P2), not the phase boundary
     (G4 -> P1): the three P4-style pages G4, P1, P2 play as one run and the gate opens before the first builder page. It
     opens EVERY time that page ends (a re-run from the dev nav's list too), as T4's does: round 3 is cleared here first. */
  const lateGate = CARD.round3_gate_after, atLate = !!lateGate && slide.id === lateGate;
  if(atLate) _gatedPhases.delete("round3");
  const crosses = !lateGate ? nextRound !== curRound : atLate ? nextRound === "round3" : (nextRound !== curRound && nextRound !== "round3");
  if(next && nextRound && crosses
     && (atLate || next.type !== "CELEBRATION") && next.type !== "PHASE_TRANSITION"   /* [gate-cel] P2's gate opens before the end screen too */
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
  { const _sgT = $("sgTitle"); if(_sgT) _sgT.textContent = (CARD.title.hi || "").split(/[:：(]/)[0].trim(); }   /* [optimize] the old landing title is gone (DEAD_BLOCKS) */
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
  // ---- [engine JS] r4/P2 boot loader: loader.webp until assets warm, then it dismisses ITSELF into
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
    /* [dun-chrome] the reference's play button takes the tap at once (it is not shown until the welcome has been heard; a replay is cut) */
    /* [spec] activity_launched — the child tapped शुरू करें. Fired AFTER the vo-lock guard above, so a
       tap that is deliberately ignored (mid-greeting) does not report a launch that never happened. */
    GameBus.xapi("activity_launched", { type: "activity", id: CARD.skill_code }, null,
      { title: (CARD.title && (CARD.title[CARD.medium] || CARD.title.hi)) || null,
        grade: CARD.grade || null, total_slides: CARD.slides.length,
        platform: (window.SwiftPAL && window.SwiftPAL._platform) || "web" });
    stopAudio();          // silence the landing greeting BEFORE slide 0 speaks (no VO overlap)
    sfxPlayButton();      // supplied common play-button SFX
    /* [dun-chrome] the music bed starts with page 1 (BGM-DUCK), not on the play tap */
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



/* ===== [dun-chrome] the chrome of HI02H04_L01_S01 (hi-02-h04-l01-s01-dun.vercel.app) on this lesson — see build.py ===== */
/* ===== FLN ANIMATION KIT: core BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion = window.FLNMotion || {};
  M.still = function(){
    try{ return document.documentElement.classList.contains("no-anim") ||
      (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches); }
    catch(_){ return false; }
  };
  M.scale = function(){
    try{ return parseFloat(getComputedStyle(document.documentElement)
      .getPropertyValue("--scale")) || 1; }catch(_){ return 1; }
  };
  M.rect = function(r, sw){                    // screen rect -> stage coords (R1/R2)
    var s = M.scale();
    if(document.documentElement.classList.contains("rotated")){
      return { left:(r.top - sw.top)/s, top:(sw.right - r.right)/s, w:r.height/s, h:r.width/s };
    }
    return { left:(r.left - sw.left)/s, top:(r.top - sw.top)/s, w:r.width/s, h:r.height/s };
  };
  M.guard = function(fn){                      // R4
    try{ fn(); }catch(e){ try{ console.warn("[animation-kit]", e && e.message); }catch(_){} }
  };
  var _actx = null;
  M.audio = function(){
    try{
      var AC = window.AudioContext || window.webkitAudioContext; if(!AC) return null;
      _actx = _actx || new AC();
      if(_actx.state === "suspended") _actx.resume();
      return _actx;
    }catch(_){ return null; }
  };
  M.ready = function(fn){
    if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  };
})();
/* ===== FLN ANIMATION KIT: core END ===== */
/* ===== FLN ANIMATION KIT: still-mode BEGIN ===== */
/* activity adaptation (R5): this engine never set html.no-anim, so the kit's verification switch
   ?still=1 had nothing to key on. Sets the class that the reduced-motion CSS and M.still() read. */
(function(){ "use strict";
  var M = window.FLNMotion;
  M.guard(function(){
    if(/[?&]still=1(&|$)/.test(location.search)) document.documentElement.classList.add("no-anim");
  });
})();
/* ===== FLN ANIMATION KIT: still-mode END ===== */
/* ===== FLN ANIMATION KIT: sky-drift BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion;

  function build(o){
    var sky = typeof o.container === "string" ? document.querySelector(o.container) : o.container;
    if(!sky) return null;
    sky.textContent = "";
    var maxSize = 0, frag = document.createDocumentFragment();

    o.layers.forEach(function(L, li){
      for(var i = 0; i < o.lanes; i++){
        var a = ((360 / o.lanes) * i + L.rot) * Math.PI / 180;
        var cos = Math.cos(a), sin = Math.sin(a);
        var size = +((o.size[0] + Math.random() * (o.size[1] - o.size[0])) * L.scale).toFixed(2);
        if(size > maxSize) maxSize = size;
        var dur = +(o.dur[0] + Math.random() * (o.dur[1] - o.dur[0])).toFixed(1);
        var el = document.createElement("i");
        el.className = o.shapes[(i + li) % o.shapes.length];
        el.style.cssText =
          "--s:"  + size + "vmax;" +
          "--x1:" + (o.r0 * cos).toFixed(2) + "vmax;--y1:" + (o.r0 * sin).toFixed(2) + "vmax;" +
          "--x2:" + (o.r1 * cos).toFixed(2) + "vmax;--y2:" + (o.r1 * sin).toFixed(2) + "vmax;" +
          "--t:"  + dur + "s;" +
          "--d:-" + (Math.random() * dur).toFixed(1) + "s;" +     // negative = de-sync
          "--g:"  + (o.glow[0] + Math.random() * (o.glow[1] - o.glow[0])).toFixed(1) + "s;" +
          "--gd:-" + (Math.random() * 4).toFixed(1) + "s;" +
          "--o:"  + (o.opacity[0] + Math.random() * (o.opacity[1] - o.opacity[0])).toFixed(2) + ";";
        frag.appendChild(el);
      }
    });
    sky.appendChild(frag);

    // collision proof: lane arc at the tightest radius must be >= 1.5x the largest element
    var arc = (2 * Math.PI * o.r0) / o.lanes, ok = arc >= maxSize * 1.5;
    if(!ok && o.warn !== false){
      console.warn("[animation-kit] sky lanes too tight: arc " + arc.toFixed(2) +
        "vmax vs element " + maxSize.toFixed(2) + "vmax. Reduce lanes or size.");
    }
    return { arc:arc, maxSize:maxSize, safe:ok, count:sky.children.length };
  }

  M.sky = {
    defaults: {
      container:".sg-sky", lanes:29,
      layers:[{rot:0,scale:1},{rot:6.2,scale:0.62},{rot:-6.2,scale:0.55}],
      r0:22, r1:72, size:[0.8,2.6], dur:[18,34], glow:[3.0,4.8],
      opacity:[0.62,0.92], shapes:["s1","s2","s3","s4","s5"], warn:true
    },
    init: function(opts){
      var o = Object.assign({}, this.defaults, opts || {}), res = null;
      M.guard(function(){ res = build(o); });
      return res;
    }
  };
  M.ready(function(){ M.guard(function(){ if(!window.__skyManual) M.sky.init(); }); });
})();
/* ===== FLN ANIMATION KIT: sky-drift END ===== */
/* ===== FLN ANIMATION KIT: sky-burst BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion;

  function boom(o){                      // sine thud + noise tail + square crackles
    var actx = M.audio(); if(!actx) return;
    try{
      var t = actx.currentTime, out = actx.createGain();
      out.gain.value = o.volume; out.connect(actx.destination);

      var tg = actx.createGain();
      tg.gain.setValueAtTime(0.9, t);
      tg.gain.exponentialRampToValueAtTime(0.0001, t + 0.16);
      tg.connect(out);
      var osc = actx.createOscillator();
      osc.type = "sine";
      osc.frequency.setValueAtTime(420, t);
      osc.frequency.exponentialRampToValueAtTime(90, t + 0.16);
      osc.connect(tg); osc.start(t); osc.stop(t + 0.18);

      var n = actx.sampleRate * 0.45;
      var buf = actx.createBuffer(1, n, actx.sampleRate), d = buf.getChannelData(0);
      for(var i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 2.6);
      var src = actx.createBufferSource(); src.buffer = buf;

      for(var c = 0; c < o.crackles; c++){
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
      var bp = actx.createBiquadFilter();
      bp.type = "bandpass"; bp.frequency.value = 3400; bp.Q.value = 0.8;
      var ng = actx.createGain();
      ng.gain.setValueAtTime(0.0001, t);
      ng.gain.exponentialRampToValueAtTime(0.5, t + 0.03);
      ng.gain.exponentialRampToValueAtTime(0.0001, t + 0.45);
      src.connect(bp); bp.connect(ng); ng.connect(out); src.start(t + 0.02);
    }catch(_){}
  }

  function pop(el, r, o){
    el.classList.add("popped");
    // respawn on the next FLIGHT lap - the glow cycle is much shorter, so filter by name
    el.addEventListener("animationiteration", function back(e){
      if(e.animationName !== "sgFly") return;
      el.classList.remove("popped");
      el.removeEventListener("animationiteration", back);
    });

    var kind = "k-dot", cls = el.classList;
    for(var ci = 0; ci < cls.length; ci++){ if(o.kind[cls[ci]]) kind = o.kind[cls[ci]]; }

    var bs = Math.max(11, r.width);
    var b = document.createElement("div");
    b.className = "sg-burst " + kind;
    b.style.left = (r.left + r.width / 2) + "px";
    b.style.top  = (r.top  + r.height / 2) + "px";
    b.style.setProperty("--bs", bs + "px");
    b.appendChild(document.createElement("div")).className = "fl";

    var k = 0;
    for(var g = 0; g < o.rings.length; g++){
      var R = o.rings[g], off = Math.random() * Math.PI * 2;
      for(var i = 0; i < R.n; i++, k++){
        var a = off + i / R.n * Math.PI * 2;
        var dist = bs * R.rad * (0.78 + Math.random() * 0.44);
        var p = document.createElement("i");
        p.style.cssText =
          "--ps:"  + (bs * R.size * (0.8 + Math.random() * 0.5)).toFixed(1) + "px;" +
          "--dx:"  + (Math.cos(a) * dist).toFixed(1) + "px;" +
          "--dy:"  + (Math.sin(a) * dist).toFixed(1) + "px;" +
          "--gy:"  + (dist * o.gravity).toFixed(1) + "px;" +
          "--sd:"  + (R.dur + Math.random() * 0.22).toFixed(2) + "s;" +
          "--sdl:" + (Math.random() * 0.06).toFixed(3) + "s;" +
          "color:" + o.hues[k % o.hues.length];
        b.appendChild(p);
      }
    }
    document.body.appendChild(b);
    if(o.sound) boom(o);
    setTimeout(function(){ b.remove(); }, o.life);
  }

  M.skyBurst = {
    defaults: {
      container:".sg-sky", when:["is-start","is-end"],
      rings:[{n:9,rad:3.1,size:.58,dur:.80},{n:7,rad:1.8,size:.78,dur:.62}],
      hues:["#FCB717","#3B7DD8","#21A74A","#E5484D","#7048D6","#F1781D"],
      kind:{s1:"k-star",s2:"k-star",s3:"k-spark",s4:"k-dot",s5:"k-dot"},
      gravity:0.42, pad:12, padRatio:0.7, minAlpha:0.08, life:1200,
      sound:true, volume:0.22, crackles:4
    },
    init: function(opts){
      var o = Object.assign({}, this.defaults, opts || {});
      M.guard(function(){
        var sky = typeof o.container === "string"
          ? document.querySelector(o.container) : o.container;
        if(!sky) return;
        // capture phase: .sg-sky is pointer-events:none, so hit-test by rect (R6)
        document.addEventListener("pointerdown", function(e){
          if(M.still()) return;
          if(!o.when.some(function(c){ return document.body.classList.contains(c); })) return;
          var els = sky.querySelectorAll("i:not(.popped)");
          for(var i = 0; i < els.length; i++){
            var el = els[i], r = el.getBoundingClientRect();
            if(r.width < 2) continue;
            var pad = Math.max(o.pad, r.width * o.padRatio);   // ~4px targets need slack
            if(e.clientX < r.left - pad || e.clientX > r.right  + pad ||
               e.clientY < r.top  - pad || e.clientY > r.bottom + pad) continue;
            if(parseFloat(getComputedStyle(el).opacity) < o.minAlpha) continue;
            // claim the tap, or it also fires the button under the star
            e.stopPropagation(); e.preventDefault();
            pop(el, r, o);
            return;
          }
        }, true);
      });
    }
  };
  M.ready(function(){ M.guard(function(){ M.skyBurst.init(); }); });
})();
/* ===== FLN ANIMATION KIT: sky-burst END ===== */

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
  const reveal = ()=>{ if(b.classList.contains("ready")) return;
    // [title-seq] (2026-11-18) the welcome is over: NOW the symbols fly (cover_fly_js, "sgwelcomeend"; once, and only after a welcome
    // that really sounded), then the title sparkles in gold with the badge pop, and only after that ("sgflydone") the button comes.
    // (Was [title-fly2]: the flight ran inside the welcome and the button came at its end.) At most 16 s (~6.1 s flight + ~1.5 s
    // sparkle): a flight that never reports its end holds nothing up.
    const fly = window.__sgFly;
    if(fly && sounded && fly.phase === "wait" && !reveal.asked){ reveal.asked = true; try { window.dispatchEvent(new Event("sgwelcomeend")); } catch(e){} }
    if(fly && (fly.phase === "blue" || fly.phase === "green" || fly.phase === "gold") && !reveal.flyLate){
      if(!reveal.waiting){ reveal.waiting = true; window.addEventListener("sgflydone", ()=>{ reveal.waiting = false; sync(); }, { once:true });
        setTimeout(()=>{ if(reveal.waiting){ reveal.waiting = false; reveal.flyLate = true; sync(); } }, 16000); } return; }
    // [load-bar-off] (2026-11-16) no loading bar on the cover: the button no longer waits for the downloads (they go on behind it)
    b.disabled = false; b.classList.add("ready");
    let on = false; const breathe = ()=>{ if(on) return; on = true; b.classList.add("sg-breathe"); };
    b.addEventListener("animationend", breathe, { once:true }); setTimeout(breathe, 700); };   // 700 ms fallback: the pop-in is .52 s
  // "heard": the welcome's own element really sounded (its clock moved) — a blocked autoplay plays a silent beat in this engine,
  // and the reference keeps the button hidden then until the first tap has played the welcome (its pointerdown fallback is this
  // engine's too)
  let heard = false, sounded = false;   // [title-seq] sounded: the welcome really played (a failed / hung one is "heard" but flies nothing)
  const listen = setInterval(()=>{ if(!document.body.classList.contains("is-start")){ clearInterval(listen); return; }
    const a = currentAudio; if(isPlaying && a && !a.paused && a.currentTime > 0.25 && /vo_landing/.test(a.src)){
      heard = sounded = true; sync(); } }, 100);   // [title-seq] nothing flies while it sounds now (was [title-fly2]: "sgwelcomestart" here)
  // [optimize] a welcome that failed to load or hung (the engine then holds its silent beat; the clip watchdog ends a hung one)
  // counts as heard, so the button can never be held back by it; a welcome refused by autoplay is neither, and still waits for a tap
  const lost = (ev)=>{ const s = ev && ev.detail && ev.detail.src; if(s && /vo_landing/.test(s) && document.body.classList.contains("is-start")){ heard = true; sync(); } };
  window.addEventListener("plmediafail", lost); window.addEventListener("plmediastuck", lost);
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
      // dev-only: a small "download results" button (teacher/QA), never in child flow
      if(new URLSearchParams(location.search).has("dev") && !$("dlResults")){
        const dl = document.createElement("button"); dl.id = "dlResults"; dl.textContent = "⬇ results JSON";
        dl.style.cssText = "position:absolute;bottom:20px;left:20px;z-index:5;font-family:var(--font-hi);font-weight:700;font-size:16px;padding:8px 16px;border-radius:12px;border:2px solid #B7DCFB;background:#fff;color:var(--navy);cursor:pointer;";
        dl.onclick = ()=> GameBus.downloadResults();
        es.appendChild(dl);
      }
      eb.onclick = ()=>{
        if(eb.dataset.completed === "1") return;
        stdSfx("next");   // [STD-SFX] the end screen's आगे बढ़ें is a next button too
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
};
/* [CEL-VO-MTG2A04] (2026-10-09, user request): the celebration line is now MTG2A04_L01_S01's own vo_cel_prompt
   ("बहुत बढ़िया, दोस्त! तुमने कमाल कर दिया!", 2.94 s, github.com/CodeWithPiyush0/MTG204_L01_S01), re-containered to WAV under this
   lesson's existing id vo_well_done (assets/Audio/vo_well_done.wav), with that card's end_anim.bits (117 x 25 ms) so the beak
   follows the new clip. audio_text / prompt_hi carry the new text. Nothing else on the page changed. */
/* [CEL-SWIFTIE] (2026-10-08, user request) the celebration Swiftie of MTG2A04_L01_S01 (celArrowAfterVO + runCelSprite of that
   page, its rounds 2l-2r) on this lesson's celebration screen - see <style id="CEL-SWIFTIE-CSS">. The engine's CELEBRATION
   module is WRAPPED, not edited: its mount runs exactly as before (the celebration sound, the sunburst, the star burst, the
   signals, the button), then the sprite takes the mascot's place and the page owns the line (state.ownsAudio: mountSlide's
   auto-play is skipped, so the clip is heard once, after the jump). Timeline, all on one clock:
     jump      the शाबाश sheet 0-29 at 45 ms a frame (1.35 s) - silent but for the celebration sound - once the screen's
               opening work has settled (three smooth paints in a row, at most 0.7 s after the mount)
     landing   the शाबाश sheet 30-35 (beak shut, 0.27 s)
     the line  vo_well_done starts here; the WHOLE line is lip-synced on the talk sheet: a cursor walks the sheet forward (so
               the body keeps moving) but only lands on a frame whose beak matches the track at that instant - open on each
               syllable, shut in every dip (CARD.end_anim.bits, 25 ms a character, read one paint ahead)
     after     the idle sheet, its mouth-shut frames only, looping - she never "talks" in silence
   Two adaptations to this engine (the reference's lines are otherwise kept): the clip's clock is the engine's own <audio>
   element (currentAudio.currentTime - what the reference's _voiceClock reads for an <audio> clip; until it sounds, the paint
   clock from the first isPlaying), and the three sheets are warmed 1.5 s after load (this page has no asset gate). Nothing
   else changes. */
(function(){ "use strict";
  /* "once the VO finishes, the button is enabled and pulses" - on the celebration too. The engine shows its arrow at once;
     here it waits (dim, not pressable) until the celebration line has ended, then it pulses like an enabled arrow. */
  function celArrowAfterVO(){
    const eb = document.getElementById("endBtn"); if(!eb) return;
    eb.classList.remove("hint-glow", "cel-ready"); eb.classList.add("cel-wait");
    const t0 = performance.now(); let heard = false;
    (function tick(){
      if(!eb.isConnected) return;
      if(isPlaying) heard = true;
      if((heard && !isPlaying) || performance.now() - t0 > 15000){
        eb.classList.remove("cel-wait"); eb.classList.add("cel-ready"); return; }
      requestAnimationFrame(tick);
    })();
  }
  setTimeout(()=> (function wrapCel(tries){
    const C = (typeof SlideModules !== "undefined") && SlideModules.CELEBRATION;
    if(!C || !C.mount){ if(tries < 200) setTimeout(()=> wrapCel(tries + 1), 25); return; }
    if(C.__celWrapped) return; C.__celWrapped = true;
    const _mount = C.mount;
    C.mount = function(host, slide){
      const r = _mount.apply(this, arguments);
      try { celArrowAfterVO(); } catch(e){}
      try { runCelSprite(slide); } catch(e){}
      return r;
    };
  })(0), 0);
  /* the clip's own clock: how long the engine's current <audio> element has really been sounding, and whether it is over */
  function voiceClock(){
    let el0 = null, ended = false;
    return ()=>{
      if(ended) return { t:null, ended:true };
      const el = currentAudio;
      if(el && (!el0 || el === el0)){
        if(!el.paused && el.currentTime > 0){ el0 = el; return { t: el.currentTime * 1000, ended:false }; }
        if(el0 && el.ended) ended = true;
        return { t:null, ended };
      }
      if(el0) ended = true;                            /* the clip is over (or another took over) */
      return { t:null, ended };
    };
  }
  let _celGen = 0;
  /* THREE SHEETS, ONE CLOCK: jump first, then the line. While she talks the clock is the celebration VO itself, from the
     moment it is sounding: the cursor walks the talk sheet forward (so the body keeps moving naturally) but only ever lands on
     a frame whose mouth matches the VO at that instant - open on each syllable, shut in every dip. All three sheets share
     frame size and alignment, so switching never jumps. */
  function runCelSprite(slide){
    const A = CARD && CARD.end_anim;
    const im = document.querySelector("#endScreen .end-mascot");
    if(!A || !im || !A.bits || !A.shabaash) return;
    const gen = ++_celGen;
    let sp = document.getElementById("celSprite");
    if(!sp){
      sp = document.createElement("div"); sp.id = "celSprite"; sp.className = "cel-sprite";
      sp.innerHTML = '<div class="cel-art"></div>';
      im.parentNode.insertBefore(sp, im);
    }
    im.style.display = "none";
    const art = sp.querySelector(".cel-art");
    /* paint the talk + idle sheets once, invisibly, while the screen opens - so the browser decodes and uploads them now,
       not at the शाबाश -> talk switch (the reference measured a 130-180 ms stall there) */
    [A.talk, A.idle].forEach(sh => {
      const pp = document.createElement("div"); pp.className = "cel-art cel-prepaint";
      pp.style.aspectRatio = A.fw + " / " + A.fh; pp.style.backgroundImage = 'url("' + sh.src + '")';
      sp.appendChild(pp);
      requestAnimationFrame(()=> requestAnimationFrame(()=> setTimeout(()=> pp.remove(), 120)));
    });
    art.style.aspectRatio = A.fw + " / " + A.fh;
    let curSrc = "";
    const show = (sheet, i)=>{
      if(sheet.src !== curSrc){ art.style.backgroundImage = 'url("' + sheet.src + '")'; curSrc = sheet.src; }
      const c = i % A.cols, r = Math.floor(i / A.cols);
      art.style.backgroundPosition = (c * 100 / (A.cols - 1)) + "% " + (r * 100 / (A.cols - 1)) + "%";
      sp.dataset.sheet = sheet === A.shabaash ? "shabaash" : (sheet === A.idle ? "idle" : "talk");
      sp.dataset.f = i;
    };
    const S = A.shabaash, T = A.talk, I = A.idle;
    const OPEN = new Set(T.open);
    const bits = A.bits || "";
    const step = A.step_ms || 25;
    const loud = (t)=> bits.charAt(Math.floor(t / step)) === "1";
    const lenMs = bits.length * step;
    /* SHE JUMPS AND CELEBRATES FIRST, THEN SPEAKS: the page owns the audio (ownsAudio: the engine's auto-play is skipped)
         jump     शाबाश sheet 0-29 at 45 ms/frame (1.35 s) - silent but for the page's celebration sound
         landing  शाबाश sheet 30-35 (mouth shut, 0.27 s)
         the VO   starts here; the WHOLE line lip-syncs on the talk sheet
         after    idle sheet, mouth-shut frames only, looping */
    const JUMP = S.pre.concat(S.word), LAND = S.post, FMS = 45;
    const src = (typeof audioFor === "function") ? audioFor(slide, "prompt") : null;
    if(!src) return;                                   /* no clip: let the engine's own auto-play run */
    state.ownsAudio = true;
    show(S, JUMP[0]);
    let m0 = 0, lastF = 0, smooth = 0, vclock = null;
    let phase = "jump", tj = 0, t0 = 0, waitStart = 0, done = false, cursor = 0, curOpen = null, lastStep = 0;
    const idle = ()=>{
      let j = 0;
      (function tick(){
        if(gen !== _celGen || !sp.isConnected) return;
        show(I, I.loop[j % I.loop.length]); j++;
        setTimeout(tick, 110);
      })();
    };
    (function frame(){
      if(gen !== _celGen || !sp.isConnected || done) return;
      if(CARD.slides[state.idx] !== slide){ done = true; return; }
      const now = performance.now();
      /* the jump's clock starts once the screen's opening work has settled - three smooth paints in a row (sunburst, stars,
         sfx and the sheets' first decode stall the first ~0.2-0.5 s; a jump timed from the mount skipped half its frames).
         Capped at 0.7 s, so she never stands still longer. */
      if(!tj){
        if(!m0){ m0 = now; lastF = now; }
        smooth = (now - lastF < 40) ? smooth + 1 : 0; lastF = now;
        if(smooth >= 3 || now - m0 > 700) tj = now;
        else { requestAnimationFrame(frame); return; }
      }
      if(phase === "jump" || phase === "land"){
        const list = phase === "jump" ? JUMP : LAND, k = Math.floor((now - tj) / FMS);
        if(k < list.length){ show(S, list[k]); requestAnimationFrame(frame); return; }
        if(phase === "jump"){ phase = "land"; tj = now; show(S, LAND[0]); requestAnimationFrame(frame); return; }
        phase = "wait"; waitStart = now;
        play(src, ()=>{});                             /* the line starts as she lands */
        vclock = voiceClock();                         /* the clip's OWN clock, independent of a late paint */
      }
      if(phase === "wait"){
        if(isPlaying){ phase = "talk"; t0 = now; }
        else if(now - waitStart > 1800){ done = true; idle(); return; }     /* the VO never started */
        else { requestAnimationFrame(frame); return; }
      }
      const vt = vclock ? vclock().t : null;
      const t = vt != null ? vt : now - t0;
      if(!isPlaying || t > lenMs + 400){ done = true; idle(); return; }
      const want = loud(t + 16);                       /* one paint ahead: the frame shows on the NEXT paint */
      /* step the talk sheet forward: at once when the mouth must change, else every 80 ms */
      if(want !== curOpen || now - lastStep > 80){
        let k = 1;
        while(k < 36 && OPEN.has((cursor + k) % 36) !== want) k++;
        cursor = (cursor + k) % 36;
        show(T, cursor); curOpen = want; lastStep = now;
      }
      sp.dataset.t = Math.round(t); sp.dataset.w = want ? 1 : 0;   /* the sprite's own clock + choice (tests) */
      requestAnimationFrame(frame);
    })();
  }
  /* warm the three sheets during the lesson, so the end screen never opens on an empty box */
  (window.__afterWarm || (f=>{ const go = ()=>{ if(document.getElementById("sgBtn") && document.getElementById("sgBtn").classList.contains("ready")){ f(); return true; } return false; };
    if(!go()){ const mo = new MutationObserver(()=>{ if(go()) mo.disconnect(); }); const sb = document.getElementById("sgBtn"); if(sb) mo.observe(sb, { attributes:true, attributeFilter:["class"] }); } }))(()=>{ try { const A = CARD && CARD.end_anim; if(A && A.shabaash){   // [dun-chrome] warmed once the cover's play button is ready (the reference: after every page's art; 1.5 s after load slowed a page mounted straight away)
    window.__celWarm = [A.shabaash.src, A.talk.src, A.idle.src].map(u => { const i = new Image(); i.src = u; if(i.decode) i.decode().catch(()=>{}); return i; }); } } catch(e){} });
})();
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
  var GATE_MS = 4000;                                                          // the reference's minimum hold (this engine had no such constant: 2.8 s)
  var GATE_REF_SRC = "assets/UI/peeking_talk_up.webp";
  var GATE_CAPTION_AT_MS = { tutorial: 3725, guided: 3885, practice: 1220 };   /* [vo-rec2] the recorded lines' headline onsets (vo_rec.py; the reference's clips: 3660 / 3940 / 1120) */   // ms into vo_pt_tutorial / vo_pt_guided / vo_pt_practice at which the headline's words begin (silence analysis of the recordings: the last clause / after "वाह!")
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
    GameBus.emit("phase_transition", { to: toPhase });
    var capT = null;
    var clearGate = function(){
      gate.classList.remove("show", "pg-say", "pg-sink", "pg-up", "pg-talk");
      clearTimeout(capT); window.removeEventListener("resize", fitGateTitle);
      if(title){ title.textContent = ""; title.classList.remove("pg-pop"); title.style.removeProperty("top"); title.style.scale = ""; }
    };
    var closeGate = function(){ clearGate(); $("stage").classList.remove("blurred", "gating"); document.body.classList.remove("gating"); };
    var voId = PHASE_GATE_VO[toPhase];
    var voSrc = voId ? ("assets/Audio/" + voId + "." + AUDIO_EXT) : null;   // this engine's clip path rule
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
/* [BGM-DUCK] (2026-10-02, user request): a low background-music bed under pages 1-13 (slides 0-12, T1 to P6), ducked to a minimal
   level whenever ANY voice-over or sound effect plays and brought back when that sound has ended. The loader/landing (before page 1)
   and the celebration page (after P6) have no bed.
   - The bed: assets/Audio/bgm_standard_2.wav (the user's "Standard Background Music 2", 4:00, looped; re-encoded 256 -> 128 kbps,
     -16.6 LUFS), one <audio> element made at load so it buffers behind the landing. Element volume BASE 0.13 (about -18 dB: some
     16 LU under the -18 LUFS voice lines, so it never competes) and DUCK 0.03 (about -30 dB, ~28 LU under: a whisper); ramps of
     180 ms down and 600 ms up (a 16 ms timer, so they run in a background tab too), so a tap's click dips the bed softly and the
     bed swells back after a line. It fades in from silence on its first page and out (600 ms, then pause) when a page outside
     the range mounts; coming back into the range resumes it.
   - Detection WITHOUT touching any caller: every sound in this engine is either an Audio element (play(): the VO chain, playSfx,
     the train's whistle / chime / departure, the bird pop, the P5 correct sfx, the celebration) or a WebAudio source node (the
     engine's _tone taps and dings, the animation kit's sky-burst), so HTMLMediaElement.prototype.play and
     AudioScheduledSourceNode.prototype.start / stop are wrapped here: a media element keeps the bed ducked from its play() until
     its ended / pause / error (or a refused play()); a source node from its start(when) until its stop(when) + 120 ms, or 0.8 s
     when no stop is scheduled (a one-shot buffer). The bed's own element is left out. A set of sounding elements plus the nodes'
     deadlines decide; the bed rises again 150 ms after the last of them is over (so two lines back to back do not swell between).
   - Range: window.mountSlide is wrapped (last, after every other wrapper): slides 0-12 start or keep the bed, any other slide
     fades it out; a ?slide=N dev load (mounted before this block ran) is handled at the end. The first play is always after a
     tap in the normal flow (loader tap, then शुरू करें), so autoplay is allowed; should a browser still refuse, the next
     pointerdown / keydown retries.
   - iOS ignores an element's volume (always 1): there the bed plays at the file's level and cannot duck. Noted, not worked around.
   Nothing else changes: no caller, no VO, no sfx, no timing. window.__bgm exposes read-only state for verification. */
(function(){
  var FIRST = 0, LAST = CARD.slides.length - 2;                               // page 1 .. the last page before the celebration
  var SRC = "assets/Audio/standard_background_music_2.ogg", BASE = 0.13, DUCK = 0.03, DOWN_MS = 180, UP_MS = 600, OUT_MS = 600;
  if(typeof HTMLMediaElement === "undefined" || !HTMLMediaElement.prototype.play) return;
  var origPlay = HTMLMediaElement.prototype.play;
  var el = null, wanted = false, tapArmed = false;
  var sounding = new Set(), nodes = new Map();                                // elements playing now; source node -> deadline (ms)
  var level = 0, target = 0, rampFrom = 0, rampT0 = 0, rampMs = 0, stepTimer = 0, checkTimer = 0;
  function nodesUntil(){ var now = Date.now(), m = 0; nodes.forEach(function(t, n){ if(t <= now) nodes.delete(n); else if(t > m) m = t; }); return m; }
  function ducked(){ return sounding.size > 0 || nodesUntil() > Date.now(); }
  function apply(){ if(el){ try{ el.volume = Math.max(0, Math.min(1, level)); }catch(e){} } }
  function step(){ stepTimer = 0; var k = rampMs > 0 ? Math.min(1, (Date.now() - rampT0) / rampMs) : 1;
    level = rampFrom + (target - rampFrom) * k; apply();
    if(k < 1) stepTimer = setTimeout(step, 16);
    else if(!wanted && target === 0 && el){ try{ el.pause(); }catch(e){} } }
  function setTarget(v, ms){ if(v === target && Math.abs(level - v) < 1e-6) return;
    target = v; rampFrom = level; rampT0 = Date.now(); rampMs = ms; if(!stepTimer) step(); }
  function check(ms){ clearTimeout(checkTimer); checkTimer = setTimeout(update, ms); }
  function update(){ if(!wanted) return; var d = ducked(); setTarget(d ? DUCK : BASE, d ? DOWN_MS : UP_MS);
    var u = nodesUntil(); if(u > Date.now()) check(u - Date.now() + 40); }
  // ---- door 1: media elements ----
  HTMLMediaElement.prototype.play = function(){
    var m = this, r = origPlay.apply(this, arguments);
    if(m !== el){
      if(!sounding.has(m)){ sounding.add(m);
        var off = function(){ sounding.delete(m); m.removeEventListener("ended", off); m.removeEventListener("pause", off); m.removeEventListener("error", off); check(150); };
        m.addEventListener("ended", off); m.addEventListener("pause", off); m.addEventListener("error", off); }
      update();
      if(r && typeof r.then === "function") r.then(null, function(){ sounding.delete(m); check(150); });   // refused: nothing sounds
    }
    return r;
  };
  // ---- door 2: WebAudio source nodes (oscillators, buffers) ----
  var SN = window.AudioScheduledSourceNode;
  var protos = (SN && SN.prototype && SN.prototype.start) ? [SN.prototype]
    : [window.OscillatorNode, window.AudioBufferSourceNode].filter(function(C){ return C && C.prototype && C.prototype.start; }).map(function(C){ return C.prototype; });
  protos.forEach(function(P){
    var oStart = P.start, oStop = P.stop;
    var at = function(node, when){ var c = node.context, t = +when; if(!(t > 0)) t = 0; return Date.now() + Math.max(0, t - (c ? c.currentTime : 0)) * 1000; };
    P.start = function(when){ var r = oStart.apply(this, arguments); try{ nodes.set(this, at(this, when) + 800); update(); }catch(e){} return r; };
    if(oStop) P.stop = function(when){ var r = oStop.apply(this, arguments); try{ if(nodes.has(this)){ nodes.set(this, at(this, when) + 120); update(); } }catch(e){} return r; };
  });
  // ---- the bed ----
  try{ el = new Audio(); el.loop = true; el.preload = "none"; el.src = SRC; apply(); }catch(e){ el = null; }
  if(el) (window.__afterPage || function(n, f){ f(); })(0, function(){ try{ el.preload = "auto"; }catch(e){} });   // [ASSET-WARM] the 46 MB bed reads ahead once the title, the gate birds and T1's art are in (it was "auto" from load, racing the title)
  function armTap(){ if(tapArmed) return; tapArmed = true;
    var once = function(){ document.removeEventListener("pointerdown", once, true); document.removeEventListener("keydown", once, true); tapArmed = false; if(wanted) start(); };
    document.addEventListener("pointerdown", once, true); document.addEventListener("keydown", once, true); }
  function start(){ if(!el) return;
    if(el.paused){ var p = null; try{ p = origPlay.call(el); }catch(e){}            // origPlay: the bed is no "sound" to itself
      if(p && typeof p.then === "function") p.then(function(){ tapArmed = false; }, armTap); }
    update(); }
  function onSlide(idx){ var sl = CARD.slides[idx]; wanted = idx >= FIRST && idx <= LAST && !(sl && sl.no_bgm);   // [l1-quiet] a slide flagged no_bgm (L1, the letter page) has no bed: it fades out (OUT_MS) at that mount and starts again, as on the first page, when the next page mounts
    if(wanted) start(); else if(el) setTarget(0, OUT_MS); }
  var origMount = window.mountSlide;
  if(typeof origMount === "function") window.mountSlide = function(idx){ var r = origMount.apply(this, arguments); try{ onSlide(idx | 0); }catch(e){} return r; };
  var gate = document.getElementById("startGate");
  if(gate && gate.classList.contains("hidden") && typeof state === "object" && state) onSlide(state.idx | 0);   // ?slide=N: mounted before this block
  backgroundMusic = el;                                                       // this engine's own handle (its fades are no-ops now; the checks read its volume)
  window.__bgm = { get el(){ return el; }, get wanted(){ return wanted; }, get sounding(){ return sounding.size; },
    get nodesDuckMs(){ return Math.max(0, nodesUntil() - Date.now()); }, get level(){ return level; }, get target(){ return target; } };
})();
/* ---------- [cover-fx] sunlit dust motes over the title page's scene ----------
   (2026-10-29, user request: "apply the exact same effect on the background of the cover page" as https://mtcg2a04l02.vercel.app/.)
   That game's [landing dust] particle system, as it is - its .sg-fx layer sits exactly over our card's scene (the card is the same
   1114x456 with a 9 px frame, so the fx box is the same 1096x438), with the same light source (.sg-sun at 170,70) and the same soft
   lens flare (cover_fx.css). Real dust in a sunbeam, not sprites on rails:
   - VISIBLE ONLY WHERE LIT. Each speck's brightness = the sunlight at its position: a falloff spilling down-right from the sun
     (.sg-sun, read live), so motes glint near the light and fade out toward the shaded right side.
   - DRIFTS ON AIR, NOT ON THE LIGHT. Motion = a slow draught along the light (26deg, down-right) + smooth per-particle turbulence + a
     tiny gravity settle + damping (dust is light, drag dominates). No straight paths.
   - TUMBLES. Flakes glint as they rotate to face the sun: brightness pulses ^3.
   - DEPTH. z 0..1: far = tiny, sharp, slow, dim; near = larger, softer (out of focus), faster across the screen (parallax).
   - COMES FROM THE LIGHT: most specks re-enter in the sunlit corner and fade in there.
   Pauses off the cover and when the tab is hidden; one static frame under prefers-reduced-motion. Coordinates are .sg-fx-local
   design px (1096x438). */
(function(){
  const cv = document.getElementById("sgDust"); if(!cv || !cv.getContext) return;
  const ctx = cv.getContext("2d"), W = 1096, H = 438, N = 120;
  const reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  // soft round sprite (one draw per mote); small sizes read as crisp points
  const spr = document.createElement("canvas"); spr.width = spr.height = 32;
  (function(){ const g = spr.getContext("2d"), r = g.createRadialGradient(16,16,0,16,16,16);
    r.addColorStop(0, "rgba(255,251,236,1)"); r.addColorStop(.45, "rgba(255,244,215,.75)");
    r.addColorStop(1, "rgba(255,236,196,0)"); g.fillStyle = r; g.fillRect(0,0,32,32); })();

  /* light field = the sun (the .sg-sun anchor, read live) spilling in: an elongated falloff pointing down-right (~26deg) -
     bright near the light, gone by the shaded right side. */
  let sun = { x:170, y:70 };
  const LA = 26 * Math.PI / 180, LC = Math.cos(LA), LS = Math.sin(LA);
  function readSun(){
    const f = document.querySelector(".sg-fx .sg-sun");
    if(f) sun = { x:f.offsetLeft, y:f.offsetTop };            // .sg-sun is a 0x0 anchor AT the sun
  }
  function light(x, y){
    const dx = x - sun.x, dy = y - sun.y;
    const s = dx * LC + dy * LS, c = -dx * LS + dy * LC;       // along / across the spill
    const sa = s >= 0 ? s / 520 : s / 150;                     // reaches far into the scene, little behind the sun
    return Math.exp(-(sa * sa + (c / 230) * (c / 230)));
  }

  const rnd = (a, b) => a + Math.random() * (b - a);
  function spawn(p, fresh){
    p.z = Math.pow(Math.random(), 1.8);                        // bias far
    const r0 = Math.random();
    if(fresh){ p.x = rnd(-20, W * .75); p.y = rnd(-10, H); }
    else if(r0 < .7){ p.x = sun.x + rnd(-130, 70); p.y = sun.y + rnd(-60, 90); }
    else if(r0 < .85){ p.x = rnd(-30, -5); p.y = rnd(0, H * .6); }
    else { p.x = rnd(0, W * .4); p.y = rnd(-30, -5); }
    p.vx = rnd(-2, 2); p.vy = rnd(-2, 2);
    p.r  = 1.1 + p.z * 3.4;                                    // radius px
    p.f1 = rnd(.07, .19); p.f2 = rnd(.11, .27); p.ph1 = rnd(0, 6.3); p.ph2 = rnd(0, 6.3);
    p.spin = rnd(.6, 2.2); p.sph = rnd(0, 6.3);
    p.fade = fresh ? 1 : 0;                                    // ease in after respawn
    return p;
  }
  const P = Array.from({length:N}, () => spawn({}, true));

  function fit(){
    const cs = getComputedStyle(document.documentElement);
    const sc = (parseFloat(cs.getPropertyValue("--scale")) || 1) * (parseFloat(cs.getPropertyValue("--fig-s")) || 1);   // the stage's scale x the cover frame's
    const k = Math.min(sc * (window.devicePixelRatio || 1), 2);  // cap backing store for low-end GPUs
    cv.width = Math.round(W * k); cv.height = Math.round(H * k);
    ctx.setTransform(k, 0, 0, k, 0, 0);
    readSun();
    if(reduce) draw(8);                                        // resizing clears the canvas
  }

  function step(p, t, dt){
    const par = .45 + p.z * .9;                                // parallax: near crosses faster
    const ws = 13 + 4 * Math.sin(t * .09);                     // the draught along the light + slow global gusts
    const wx = ws * LC, wy = ws * LS + 1.2 * Math.sin(t * .07 + 1.3);
    const tx = 7 * Math.sin(t * p.f1 + p.ph1) + 4 * Math.sin(t * p.f2 * 1.7 + p.ph2);   // smooth turbulence (no visible loop)
    const ty = 6 * Math.cos(t * p.f2 + p.ph2) + 3 * Math.sin(t * p.f1 * 2.3 + p.ph1);
    const g  = .8 + p.z * .9;                                  // settling: heavier near flakes sink a touch faster
    const k = 1 - Math.exp(-1.6 * dt);                         // drag toward the local air velocity + Brownian jitter
    p.vx += ((wx + tx) - p.vx) * k + rnd(-1, 1) * 6 * dt;
    p.vy += ((wy + ty + g) - p.vy) * k + rnd(-1, 1) * 6 * dt;
    p.x += p.vx * par * dt; p.y += p.vy * par * dt;
    if(p.fade < 1) p.fade = Math.min(1, p.fade + dt / 1.5);
    if(p.x > W + 20 || p.y > H + 20 || p.x < -40 || p.y < -40) spawn(p, false);
  }

  function draw(t){
    ctx.clearRect(0, 0, W, H);
    ctx.globalCompositeOperation = "lighter";
    for(const p of P){
      const L = light(p.x, p.y);
      if(L < .02) continue;                                    // in shade: invisible, like real dust
      const glint = .5 + .5 * Math.pow(Math.max(0, Math.sin(t * p.spin + p.sph)), 3);
      const depth = .45 + .55 * (1 - Math.abs(p.z - .35));     // far dim, very near slightly defocused
      const a = Math.min(1, L * 1.7) * glint * depth * p.fade;
      if(a < .02) continue;
      const d = p.r * 2 * (p.z > .7 ? 1.35 : 1);               // near = out-of-focus blur disc
      ctx.globalAlpha = p.z > .7 ? a * .6 : a;
      ctx.drawImage(spr, p.x - d / 2, p.y - d / 2, d, d);
    }
    ctx.globalAlpha = 1;
  }

  let last = 0, t = 0;
  function frame(now){
    requestAnimationFrame(frame);
    if(!document.body.classList.contains("is-start")){ last = 0; return; }
    const dt = last ? Math.min((now - last) / 1000, .05) : 0; last = now; t += dt;
    for(const p of P) step(p, t, dt);
    draw(t);
  }
  window.__sgDust = { get t(){ return t; }, get n(){ return P.length; } };   // read-only, for the checks

  fit();
  window.addEventListener("resize", () => { clearTimeout(fit._t); fit._t = setTimeout(fit, 200); });
  window.addEventListener("load", fit);
  if(reduce){ for(let i = 0; i < 240; i++) for(const p of P) step(p, i / 30, 1 / 30); draw(8); }
  else requestAnimationFrame(frame);
})();
/* ---------- [cover-eyes] the title page's three characters' eyes come alive ----------
   (2026-10-29, user request: "apply the exact same effect of the eyes of the pencil" of https://mtcg2a04l02.vercel.app/ to the
   symbols on the cover.) The mtcg game's [pencil eyes] rig, on three upright faces instead of one quarter-turned pencil: the danda,
   the comma and the question mark of the Figma title page (title_assets/title_char_*.png), each with its own painted eyes (white
   eyeball in a dark outline, brown iris, black pupil, shines) and brows.
   RIG: per character a small canvas over its picture (in the picture's own box, above it). Per eye, clipped to the painted eyeball's
   inner edge (measured by title_eyes_measure.py: one axis-aligned ellipse per eye, in art px): a white eyeball with soft shading, an
   iris ~13% smaller than the painted one (so the look direction reads at this size), a pupil that widens and narrows, the painted
   shines, and eyelids in the body's own colour around the eye (sampled above, beside and below it) with a lash line. The brows are
   cut from the art (title_char_<n>_rig.png: the body under each brow with the brow painted out, plus each brow) and lift and tilt as
   pieces. The faces are upright: the brows sit above the eyes, the upper lids close from the top, the lower lids rise from below.
   BRAIN (the pencil's, shared by the three): each landing animation says where it is - SGEyes.look(id, element | {x,y} | fn,
   priority, ms) - and the eyes watch the most important live one; otherwise they wander between the child (straight out), Swiftee
   and, once it is up, the play button. Each face moves like real eyes: a fast jump (saccade, 50-170ms) to each new target, smooth
   following for moving things (with catch-up jumps), tiny drifts while they rest, a blink every 2-5s and often with a big jump -
   each on its own clock, so the three never move in lockstep. SGEyes.react(name) adds an expression for a moment: surprise (eyes
   grow, pupils narrow, brows up), wince (a squeeze blink, brows down), happy (lower lids up "^^", pupils wide), curious (one brow
   up, pupils wide). The pointer (mouse) draws every gaze for a moment; a tap, curious; the play button's arrival, a curious look.
   [title-fly] (2026-11-15): SGEyes.faceLook(name, target, ms) gives one face ("purn" | "comma" | "question") its own target for a
   while, ahead of the shared one (the flying symbols look at the title; the question mark keeps the shared brain, which the
   flights point at them); debug() names each face.
   SAFE: canvas draws only; the loop stops off the cover; reduced motion = eyes that look at the child and blink; any error removes
   the overlays, which leaves the painted eyes. */
(function(){
  "use strict";
  const FACES = [{"name": "purn", "sel": ".sgf-purn img", "art": [1254, 1254], "face": [625.4, 469.1], "rig": "assets/UI/title_char_purn_rig.webp", "eyes": [{"cx": 545.2, "cy": 467.1, "a": 53.2, "b": 55.5, "ring": 3.2, "iris": 39.0, "pupil": 24.5, "shines": [[-6.6, -18.0, 11.0]], "lid": ["#7de8fc", "#6ee1fb", "#70e1fc"]}, {"cx": 705.5, "cy": 471.1, "a": 53.5, "b": 55.6, "ring": 3.2, "iris": 38.8, "pupil": 24.0, "shines": [[-16.9, -18.3, 10.6]], "lid": ["#1bc6fc", "#24b9fb", "#56d7fb"]}], "brows": [{"clean": 0, "brow": 84, "box": [499, 342, 84, 67], "c": [539.7, 372.3], "tilt": 1}, {"clean": 168, "brow": 248, "box": [679, 345, 80, 68], "c": [720.5, 375.8], "tilt": -1}]}, {"name": "comma", "sel": ".sgf-comma", "art": [1022, 1538], "face": [522.6, 652.7], "rig": "assets/UI/title_char_comma_rig.webp", "eyes": [{"cx": 334.6, "cy": 692.1, "a": 108.3, "b": 117.6, "ring": 6.5, "iris": 70.2, "pupil": 42.0, "shines": [[21.9, -44.1, 20.3], [-61.6, -1.5, 13.2]], "lid": ["#9bf14d", "#8bed48", "#92eb46"]}, {"cx": 710.6, "cy": 613.2, "a": 103.2, "b": 119.3, "ring": 6.2, "iris": 70.0, "pupil": 43.0, "shines": [[-2.6, -40.5, 20.8], [59.5, -15.3, 13.0]], "lid": ["#5bdb3b", "#68e23e", "#81ea44"]}], "brows": [{"clean": 0, "brow": 151, "box": [204, 411, 151, 142], "c": [275.5, 469.8], "tilt": 1}, {"clean": 302, "brow": 482, "box": [596, 338, 180, 101], "c": [683.2, 381.1], "tilt": -1}]}, {"name": "question", "sel": ".sgf-question", "art": [1024, 1536], "face": [515.0, 353.0], "rig": "assets/UI/title_char_question_rig.webp", "eyes": [{"cx": 376.8, "cy": 385.7, "a": 90.6, "b": 81.2, "ring": 5.4, "iris": 51.8, "pupil": 33.5, "shines": [[19.3, -32.0, 14.9], [-45.5, -8.5, 8.2]], "lid": ["#c755fc", "#c452fc", "#c252fc"]}, {"cx": 653.3, "cy": 320.4, "a": 72.9, "b": 81.4, "ring": 4.4, "iris": 51.0, "pupil": 33.5, "shines": [[0.2, -29.5, 15.3], [43.3, -17.7, 6.3]], "lid": ["#c452fc", "#c251fc", "#c14ffc"]}], "brows": [{"clean": 0, "brow": 116, "box": [289, 205, 116, 99], "c": [343.1, 245.4], "tilt": 1}, {"clean": 232, "brow": 364, "box": [561, 144, 132, 60], "c": [621.9, 172.8], "tilt": -1}]}];                                   // build.py: title_assets/cover_eyes_data.json (title_eyes_measure.py)
  const IRIS_K = 0.87;                                       // the live iris / pupil / shines vs the painted ones (the pencil's ~13% smaller)
  const Z = 70;                                              // screen px "in front of" the eyes: how a screen point maps to a look direction
  const reduce = !!(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
  const now = ()=> performance.now();
  const lerp = (a, b, k)=> a + (b - a) * k, clamp01 = v => Math.max(0, Math.min(1, v));

  /* ---- expressions: every value springs toward its target; a reaction holds its targets for a while (shared by the faces) ---- */
  const NEUTRAL = { scale: 1, pupil: 1, lidU: 0, lidL: 0, lidH: 0, lift: 0, tilt: 0, liftB: 0 };
  const EXPR = {
    surprise: { ms: 900,  v: { scale: 1.07, pupil: 0.72, lift: 1, tilt: -0.08 } },
    wince:    { ms: 420,  v: { lift: -0.8, tilt: 0.2 } },     // + a squeeze: the lids snap shut and hold (see react)
    happy:    { ms: 1300, v: { lidH: 0.7, pupil: 1.12, lift: 0.5, tilt: -0.1 } },
    curious:  { ms: 1000, v: { pupil: 1.15, liftB: 1 } }
  };
  const P = {}; for(const k in NEUTRAL) P[k] = { v: NEUTRAL[k], vel: 0 };
  let expr = null, exprName = null, exprUntil = 0;
  const lidsBusy = tn => !!(expr && tn < exprUntil + 250 && expr.v.lidH) || P.lidH.v > 0.05;   // no natural blink across a happy squint
  function springs(dt, tn){
    const e = expr && tn < exprUntil ? expr : null;
    for(const k in P){
      const p = P[k], tgt = e && k in e.v ? e.v[k] : NEUTRAL[k];
      const K = k === "scale" ? 700 : 380, C = k === "scale" ? 24 : 36;         // the eyes pop a touch when they grow
      p.vel += (K * (tgt - p.v) - C * p.vel) * dt; p.v += p.vel * dt;
    }
  }

  /* ---- attention: id -> { t: Element | {x,y} | fn, pri, until, at } ---- */
  const src = new Map();
  const faces = [];
  const api = {
    look(id, t, pri, ms){ if(!t) return; const old = src.get(id);
      src.set(id, { t, pri: pri || 1, until: now() + (ms || 250), at: old && old.t === t ? old.at : now() }); },
    release(id){ src.delete(id); },
    // [title-fly] one face's own target for a while (the flying symbols look where they are going), over the shared brain's
    faceLook(name, t, ms){ const F = faces.find(f => f.cfg.name === name); if(F && t) F.ov = { t, until: now() + (ms || 250) }; },
    faceRelease(name){ const F = faces.find(f => f.cfg.name === name); if(F) F.ov = null; },
    react(name){ if(reduce || !EXPR[name]) return; expr = EXPR[name]; exprName = name; exprUntil = now() + expr.ms;
      if(name === "wince") faces.forEach(F => blink(F, now(), 170, true)); },
    debug(){ return faces.map(F => ({ name: F.cfg.name, g: { x: +F.g.x.toFixed(3), y: +F.g.y.toFixed(3) }, blinks: F.blinks, lid: +blinkU(F, now()).toFixed(2), on: !!(F.cv && F.cv.style.display === "block"), expr: expr && now() < exprUntil ? exprName : null })); }
  };
  window.SGEyes = api;

  /* layout reads are cached (80-500ms): the eyes must never force the page to re-layout on every frame (low-end tablets) */
  let mascotAt = -1e9, mascotP = null;
  const mascot = ()=>{ const tn = now(); if(tn - mascotAt < 400) return mascotP; mascotAt = tn; mascotP = null;
    for(const m of document.querySelectorAll(".sgf-swiftie-anim, .sgf-swiftie, .sg-mascot")){ const r = m.getBoundingClientRect(), cs = getComputedStyle(m);
      if(r.width && r.height && cs.visibility !== "hidden" && cs.display !== "none" && +cs.opacity > 0.05){ mascotP = { x: r.left + r.width * 0.5, y: r.top + r.height * 0.3 }; break; } }
    return mascotP; };
  const rects = new WeakMap();
  function centreOf(el, tn){ let c = rects.get(el);
    if(!c || tn - c.t > 80){ const r = el.getBoundingClientRect(); c = { t: tn, p: r.width || r.height ? { x: r.left + r.width / 2, y: r.top + r.height / 2 } : null }; rects.set(el, c); }
    return c.p; }
  const idle = { t: "child", until: 0 };
  function chooseIdle(){
    const btn = document.getElementById("sgBtn"), btnOn = !!(btn && btn.classList.contains("ready")), r = Math.random();
    if(btnOn && r < 0.32) return btn;                          // the play button, once it is up: an invitation
    if(r < (btnOn ? 0.47 : 0.3)) return mascot;
    if(r < 0.88) return "child";
    const card = document.querySelector(".sg-card"); if(!card) return "child";
    const c = card.getBoundingClientRect();                     // a glance somewhere on the card
    return { x: c.left + c.width * (0.15 + 0.7 * Math.random()), y: c.top + c.height * (0.2 + 0.6 * Math.random()) };
  }
  function pickTarget(tn){
    let best = null;
    for(const [id, s] of src){ if(s.until < tn){ src.delete(id); continue; }
      if(!best || s.pri > best.pri || (s.pri === best.pri && s.at > best.at)) best = s; }
    if(best) return best.t;
    if(tn >= idle.until){ idle.t = chooseIdle(); idle.until = tn + 1300 + Math.random() * 1900; }
    return idle.t;
  }

  /* ---- gaze: a look direction g in the unit disc (0,0 = straight out at the child), per face ---- */
  function aim(F, t, tn){
    if(t === "child") return { x: 0, y: 0 };
    let p = t;
    if(typeof t === "function") p = t();
    else if(t && t.getBoundingClientRect) p = centreOf(t, tn);
    if(!p) return { x: 0, y: 0 };
    const dx = p.x - F.E.x, dy = p.y - F.E.y, n = Math.sqrt(dx * dx + dy * dy + Z * Z);
    return { x: dx / n, y: dy / n };
  }
  function gaze(F, dt, tn, T){
    const a = aim(F, T, tn), g = F.g;
    if(tn > F.nextJit){ const m = 0.04 + Math.random() * 0.06, th = Math.random() * 6.2832;   // tiny drifts while it rests
      F.jit = { x: m * Math.cos(th), y: m * Math.sin(th) }; F.nextJit = tn + 700 + Math.random() * 1100; }
    const tx = a.x + F.jit.x, ty = a.y + F.jit.y, dx = tx - g.x, dy = ty - g.y, dist = Math.hypot(dx, dy);
    if(F.sac){                                                 // a saccade lands on where the target is NOW
      const k = Math.min(1, (tn - F.sac.t0) / F.sac.ms), e = 1 - Math.pow(1 - k, 3);
      g.x = F.sac.x0 + (tx - F.sac.x0) * e; g.y = F.sac.y0 + (ty - F.sac.y0) * e; if(k >= 1) F.sac = null;
    } else if(dist > 0.16){
      F.sac = { t0: tn, ms: 50 + 70 * Math.min(dist, 1.7), x0: g.x, y0: g.y };
      if(dist > 0.55 && tn - F.lastBlink > 1200 && !lidsBusy(tn) && Math.random() < 0.35) blink(F, tn);   // big jumps often come with a blink
    } else { const k = 1 - Math.exp(-dt * 12); g.x += dx * k; g.y += dy * k; }        // smooth following
  }

  /* ---- blinks (per face) ---- */
  function blink(F, tn, hold, force){                        // hold: ms fully shut (a blink 25, the wince's squeeze longer)
    if(F.blinkAt >= 0 && !force) return;
    F.blinkAt = tn; F.blinkHold = hold || 25; F.lastBlink = tn; F.nextBlink = tn + 2200 + Math.random() * 3300; F.blinks++;
    if(!hold && Math.random() < 0.12) F.dbl = tn + 330;      // now and then a double blink
  }
  function blinkU(F, tn){
    if(F.blinkAt < 0) return 0;
    const t = tn - F.blinkAt, o = 70 + F.blinkHold;
    if(t < 70){ const k = t / 70; return k * k; }            // closes fast...
    if(t < o) return 1;
    if(t < o + 135){ const k = (t - o) / 135; return (1 - k) * (1 - k); }   // ...opens a little slower
    F.blinkAt = -1; return 0;
  }

  /* ---- drawing (in each picture's art px: the canvas transform maps the art onto it) ---- */
  let irisC = null;
  const IRIS_TEX_R = 40;
  function makeIris(){
    const R = IRIS_TEX_R, K = 4, c = document.createElement("canvas"); c.width = c.height = Math.ceil(2 * R * K);
    const x = c.getContext("2d"); x.scale(K, K); x.translate(R, R);
    const gr = x.createRadialGradient(0, 0, 0, 0, 0, R);
    [[0, "#4a2106"], [0.5, "#7d3d0c"], [0.66, "#a15616"], [0.8, "#b46a22"], [0.9, "#8a4611"], [0.96, "#4b1f05"], [1, "#2a1003"]].forEach(s => gr.addColorStop(s[0], s[1]));
    x.beginPath(); x.arc(0, 0, R, 0, 6.2832); x.fillStyle = gr; x.fill(); x.save(); x.clip();
    let seed = 7; const rnd = ()=> (seed = (seed * 16807) % 2147483647) / 2147483647;
    for(let k = 0; k < 44; k++){                               // the iris's fibres, light and dark in turn
      const th = k / 44 * 6.2832 + rnd() * 0.08, r0 = R * (0.52 + rnd() * 0.06), r1 = R * (0.82 + rnd() * 0.12);
      x.strokeStyle = (k % 2 ? "rgba(222,150,72," : "rgba(58,22,4,") + (0.18 + rnd() * 0.2).toFixed(2) + ")"; x.lineWidth = (0.6 + rnd() * 1.1) * R / 30.5;
      x.beginPath(); x.moveTo(Math.cos(th) * r0, Math.sin(th) * r0); x.lineTo(Math.cos(th) * r1, Math.sin(th) * r1); x.stroke();
    }
    x.strokeStyle = "rgba(30,10,2,.55)"; x.lineWidth = 2.2 * R / 30.5; x.beginPath(); x.arc(0, 0, R - 1.1 * R / 30.5, 0, 6.2832); x.stroke();   // limbal ring
    x.restore(); return c;
  }
  function makeGradients(F){
    const ctx = F.ctx;
    F.cfg.eyes.forEach((e, i)=>{
      const ia = e.a - e.ring, ib = e.b - e.ring;
      const s = ctx.createRadialGradient(-0.2 * ia, -0.12 * ib, 2, 0, 0, Math.max(ia, ib) * 1.02);
      [[0, "#ffffff"], [0.55, "#fcfafa"], [0.8, "#f1edec"], [0.93, "#e2dcdc"], [1, "#cfc7cb"]].forEach(st => s.addColorStop(st[0], st[1]));
      F.sclera[i] = s;
      const lid = e.lid.map((c, k)=> c || e.lid[1] || e.lid[0] || "#888");   // the body's colour above / beside / below the eye: the lids' skin
      const l = ctx.createLinearGradient(0, -1.4 * ib, 0, 1.4 * ib);
      l.addColorStop(0, lid[0]); l.addColorStop(0.5, lid[1]); l.addColorStop(1, lid[2]);
      F.lidGrad[i] = l;
      const s2 = ctx.createLinearGradient(0, -ib, 0, ib);     // a lid is a dome over the eyeball: lit from above, shaded below
      s2.addColorStop(0, "rgba(255,255,255,.16)"); s2.addColorStop(0.5, "rgba(255,255,255,0)"); s2.addColorStop(1, "rgba(60,20,100,.16)");
      F.lidLight[i] = s2;
    });
  }
  /* EYELIDS (eye-local art px; t = x / ia from -1 to 1 across the eye). A lid covers the eye from one side (the top or the bottom)
     up to its edge y(t) = y1 + (y0 - y1)(1 - t^2): y1 at the ends, y0 in the middle. Blinks: the upper lid (from the top) and the
     lower lid (from the bottom) meet on the closed line y = YM + BM (1 - t^2) - bowed toward the face's bottom, like a closed eye.
     Happy: the lower lid rises with its edge bowed the other way, a "^". (The pencil's lids, turned upright.) */
  const YM = 0.1, BM = 0.34, YH = 0.05, BH = 0.38;           // fractions of the eye's inner half-height ib
  function lid(F, i, ia, ib, side, y1, y0, lashW, lashCol, shadowDy){
    const ctx = F.ctx, S = F.S, yc = 2 * y0 - y1;
    const path = ()=>{ ctx.beginPath(); ctx.moveTo(-ia - 5, side); ctx.lineTo(-ia - 5, y1); ctx.lineTo(-ia, y1);
      ctx.quadraticCurveTo(0, yc, ia, y1); ctx.lineTo(ia + 5, y1); ctx.lineTo(ia + 5, side); ctx.closePath(); };
    const edge = ()=>{ ctx.beginPath(); ctx.moveTo(-ia, y1); ctx.quadraticCurveTo(0, yc, ia, y1); };
    path(); ctx.save(); ctx.shadowColor = "rgba(40,20,60,.35)"; ctx.shadowBlur = 5 * S; ctx.shadowOffsetY = shadowDy * S;
    ctx.fillStyle = F.lidGrad[i]; ctx.fill(); ctx.restore();                     // the skin (the body's own colour around the eye)
    ctx.save(); path(); ctx.clip();
    ctx.fillStyle = F.lidLight[i]; ctx.fillRect(-ia - 6, -ib - 6, 2 * ia + 12, 2 * ib + 12);
    edge(); ctx.lineWidth = 8 * ib / 45; ctx.strokeStyle = "rgba(40,20,70,.2)"; ctx.stroke();   // the lid's thickness along its edge
    ctx.restore();
    edge(); ctx.lineWidth = lashW * ib / 45; ctx.lineCap = "round"; ctx.strokeStyle = lashCol; ctx.stroke();   // lash line
  }
  function lids(F, i, ia, ib, u, ul, h){
    const ym = YM * ib, bm = BM * ib;
    if(ul > 0.005){ const y1 = lerp(ib + 2, ym, ul); lid(F, i, ia, ib, ib + 6, y1, y1 + bm, 2.4, "rgba(34,16,38,.75)", -1); }
    if(h > 0.005){ const y1 = lerp(ib + 2 + BH * ib, -YH * ib, h); lid(F, i, ia, ib, ib + 6, y1, y1 - BH * ib, 2.6, "rgba(34,16,38,.85)", -1); }
    if(u > 0.005){ const y1 = lerp(-ib - bm - 2, ym, u); lid(F, i, ia, ib, -ib - 6, y1, y1 + bm, 3.6, "#221026", 1.2); }
  }
  function drawEye(F, e, i, bU){
    const ctx = F.ctx, ia = e.a - e.ring, ib = e.b - e.ring, sc = P.scale.v;
    const IR = e.iris * IRIS_K, PR = e.pupil * IRIS_K;
    const mx = ia - IR - 1.5, my = ib - IR - 1.5;
    let ox = F.g.x * mx * 1.25, oy = F.g.y * my * 1.25;
    const q = Math.hypot(ox / mx, oy / my); if(q > 1){ ox /= q; oy /= q; }      // the iris stays inside the eyeball
    ctx.save(); ctx.translate(e.cx, e.cy); if(Math.abs(sc - 1) > 0.001) ctx.scale(sc, sc);
    ctx.save(); ctx.beginPath(); ctx.ellipse(0, 0, ia + 0.9, ib + 0.9, 0, 0, 6.2832); ctx.clip();
    ctx.fillStyle = F.sclera[i]; ctx.fillRect(-ia - 3, -ib - 3, 2 * ia + 6, 2 * ib + 6);
    ctx.drawImage(irisC, ox - IR, oy - IR, 2 * IR, 2 * IR);
    ctx.fillStyle = "#080302"; ctx.beginPath(); ctx.arc(ox, oy, PR * P.pupil.v, 0, 6.2832); ctx.fill();
    e.shines.forEach((s, k)=>{ ctx.fillStyle = "#ffffff"; ctx.globalAlpha = k ? 0.85 : 1; ctx.beginPath(); ctx.arc(ox + s[0] * IRIS_K, oy + s[1] * IRIS_K, s[2] * IRIS_K, 0, 6.2832); ctx.fill(); });
    ctx.globalAlpha = 1;
    const sh = ctx.createLinearGradient(0, -ib, 0, -0.4 * ib);   // the soft shadow under the brow side (the top) of the eye
    sh.addColorStop(0, "rgba(80,50,110,.16)"); sh.addColorStop(1, "rgba(80,50,110,0)"); ctx.fillStyle = sh; ctx.fillRect(-ia - 3, -ib - 3, 2 * ia + 6, 0.6 * ib + 3);
    const u = clamp01(Math.max(bU, P.lidU.v)), ul = clamp01(Math.max(bU, P.lidL.v));
    lids(F, i, ia, ib, u, ul, clamp01(P.lidH.v));
    ctx.restore();
    if(sc > 1.002){ ctx.lineWidth = 3.8 * ib / 45; ctx.strokeStyle = "rgba(36,16,43,.92)"; ctx.beginPath(); ctx.ellipse(0, 0, e.a - e.ring / 2, e.b - e.ring / 2, 0, 0, 6.2832); ctx.stroke(); }
    const shut = Math.min(u, ul);                              // closed: the lid's skin softens the eyeball's dark outline, so it reads as a lid, not a hole
    if(shut > 0.3){ ctx.globalAlpha = 0.5 * (shut - 0.3) / 0.7; ctx.lineWidth = e.ring + 1; ctx.strokeStyle = F.lidGrad[i];
      ctx.beginPath(); ctx.ellipse(0, 0, e.a - e.ring / 2, e.b - e.ring / 2, 0, 0, 6.2832); ctx.stroke(); ctx.globalAlpha = 1; }
    ctx.restore();
  }
  function draw(F, bU){
    const ctx = F.ctx, cfg = F.cfg;
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, F.cv.width, F.cv.height);
    ctx.setTransform(F.S, 0, 0, F.S, 0, 0);
    if(F.rig){
      cfg.brows.forEach(br => { const [x, y, w, h] = br.box; ctx.drawImage(F.rig, br.clean, 0, w, h, x, y, w, h); });   // the body, brows removed
      cfg.brows.forEach((br, i)=>{
        const [x, y, w, h] = br.box, [bx, by] = br.c, L = P.lift.v + (i === 1 ? P.liftB.v : 0), dy = L >= 0 ? -L * cfg.browUp : -L * cfg.browDown;
        ctx.save(); ctx.translate(bx, by + dy); ctx.rotate(P.tilt.v * br.tilt); ctx.drawImage(F.rig, br.brow, 0, w, h, x - bx, y - by, w, h); ctx.restore();
      });
    }
    cfg.eyes.forEach((e, i)=> drawEye(F, e, i, bU));
  }
  let placedAt = -1e9;
  window.addEventListener("resize", ()=>{ placedAt = -1e9; });
  function place(F, tn){                                     // fit the canvas to the picture as laid out now (4x a second; at once after a resize)
    const img = F.img, [AW, AH] = F.cfg.art;
    if(tn - placedAt >= 250 || !F.layoutKey){
      const f = img.offsetWidth / AW;
      const sc = (parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--scale")) || 1) * (parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--fig-s")) || 1);
      const k = Math.min(3, Math.max(1, sc * (window.devicePixelRatio || 1)) * 1.5);
      const key = [img.offsetLeft, img.offsetTop, img.offsetWidth, img.offsetHeight, k].join();
      if(key !== F.layoutKey){
        F.layoutKey = key;
        F.cv.style.left = img.offsetLeft + "px"; F.cv.style.top = img.offsetTop + "px";
        F.cv.style.width = img.offsetWidth + "px"; F.cv.style.height = img.offsetHeight + "px";
        F.cv.width = Math.round(img.offsetWidth * k); F.cv.height = Math.round(img.offsetHeight * k); F.S = f * k;
        makeGradients(F);
      }
    }
    const r = img.getBoundingClientRect(), fs = r.width / AW, fy = r.height / AH;
    F.E.x = r.left + F.cfg.face[0] * fs; F.E.y = r.top + F.cfg.face[1] * fy;
  }

  /* ---- life cycle ---- */
  let raf = 0, last = 0, running = false;
  const gate = ()=> document.getElementById("startGate");
  const onLanding = ()=>{ const gt = gate(); return !!gt && !gt.classList.contains("hidden") && document.body.classList.contains("loaded"); };
  function stopAll(){ cancelAnimationFrame(raf); raf = 0; running = false; faces.forEach(F => { if(F.cv) F.cv.remove(); F.cv = null; }); faces.length = 0; }
  function frame(){
    raf = 0;
    if(!onLanding()){ running = false; faces.forEach(F => { if(F.cv) F.cv.style.display = "none"; }); return; }  // off the cover: stop (the gate observer restarts it)
    raf = requestAnimationFrame(frame);
    try {
      const tn = now(), dt = last ? Math.min(1 / 30, (tn - last) / 1000) : 0; last = tn;
      const T = reduce ? "child" : pickTarget(tn);
      if(!reduce) springs(dt, tn);
      if(tn - placedAt >= 250) { faces.forEach(F => place(F, tn)); placedAt = tn; } else faces.forEach(F => place(F, tn));
      for(const F of faces){
        F.cv.style.display = "block";
        if(!reduce) gaze(F, dt, tn, F.ov && F.ov.until > tn ? F.ov.t : T); else { F.g.x = 0; F.g.y = 0; }   // [title-fly] a face's own target first
        if(tn > F.nextBlink){ if(lidsBusy(tn)) F.nextBlink = tn + 400; else blink(F, tn); }
        if(F.dbl && tn > F.dbl){ F.dbl = 0; if(F.blinkAt < 0 && !lidsBusy(tn)) blink(F, tn); }
        draw(F, blinkU(F, tn));
      }
    } catch(err){ stopAll(); }                                   // anything wrong: the painted eyes stay
  }
  function start(){
    if(running || !faces.length) return;
    running = true; last = 0;
    const tn = now(); faces.forEach((F, i) => { F.nextBlink = tn + 1500 + i * 400 + Math.random() * 600; });
    api.look("swifty", mascot, 2, 2800);                       // Swiftee greets first: the three watch her
    if(!raf) raf = requestAnimationFrame(frame);
  }
  function init(){
    const todo = [];
    for(const cfg of FACES){
      const img = document.querySelector(cfg.sel); if(!img) continue;
      const b = cfg.eyes.reduce((s, e)=> s + e.b, 0) / cfg.eyes.length;
      cfg.browUp = 0.11 * b; cfg.browDown = 0.09 * b;          // art px the brows travel (the pencil's 5 / 4 on its 45 px eyes)
      todo.push({ cfg, img });
    }
    if(!todo.length) return;
    let pending = todo.length;
    const go = ()=>{
      if(todo.some(t => !t.img.complete || !t.img.offsetWidth)){ setTimeout(go, 120); return; }
      irisC = irisC || makeIris();
      for(const t of todo){
        const cv = document.createElement("canvas"); cv.className = "sgf-eyes"; cv.setAttribute("aria-hidden", "true");
        const F = { cfg: t.cfg, img: t.img, cv, ctx: cv.getContext("2d"), S: 1, layoutKey: "", sclera: [], lidGrad: [], lidLight: [], rig: t.rig || null,
                    E: { x: 0, y: 0 }, g: { x: -0.3 + 0.6 * Math.random(), y: 0 }, sac: null, jit: { x: 0, y: 0 }, nextJit: 0,
                    blinkAt: -1, blinkHold: 25, lastBlink: 0, nextBlink: 0, dbl: 0, blinks: 0 };
        (t.img.offsetParent || t.img.parentNode).appendChild(cv);
        faces.push(F);
      }
      if(onLanding()) start();
      new MutationObserver(()=>{ if(onLanding()) start(); }).observe(gate(), { attributes: true, attributeFilter: ["class"] });
      new MutationObserver(()=>{ if(onLanding()) start(); }).observe(document.body, { attributes: true, attributeFilter: ["class"] });
    };
    // the brows' rig sheets first (a sheet that fails to load leaves that face's painted brows still)
    todo.forEach(t => { const rig = new Image(); rig.onload = ()=>{ t.rig = rig; if(--pending === 0) go(); }; rig.onerror = ()=>{ if(--pending === 0) go(); }; rig.src = t.cfg.rig; });
    // the child's finger (or mouse): the three look at it for a moment
    const gt = gate();
    if(gt){
      gt.addEventListener("pointermove", ev => { if(ev.pointerType === "mouse") api.look("pointer", { x: ev.clientX, y: ev.clientY }, 6, 700); });
      gt.addEventListener("pointerdown", ev => { api.look("pointer", { x: ev.clientX, y: ev.clientY }, 6, 1100); api.react("curious"); });
    }
    // the play button arrives (.ready) once the welcome has been heard: look at it, curious
    const btn = document.getElementById("sgBtn");
    if(btn){ let seen = btn.classList.contains("ready");
      new MutationObserver(()=>{ if(!seen && btn.classList.contains("ready")){ seen = true; setTimeout(()=>{ api.look("play", btn, 4, 1600); api.react("curious"); }, 650); } })
        .observe(btn, { attributes: true, attributeFilter: ["class"] }); }
  }
  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
/* ---------- [title-fly] the cover's symbols fly into the title ----------
   (2026-11-15, asked with Figma FLN-by-MJ 956:2: "At the completion of the background VO at the title page the blue colored symbol
   will slowly fly at the end of the title text and will get merged into the art style and the color of the title font text, and
   the green colored symbol will also slowly fly to the title text ... and will get merged and integrated at the places of ,
   symbol in the title page text where as the purple colored symbol standing at the center will be observing both".)
   WHEN ([title-fly2], asked the same day: "the animation of the blue and green symbols should happen completely before the VO of the
   title page is completed and only after that the play button should appear in the same way as of now"): once per load, WHILE the
   welcome line plays - it starts as soon as the line is really sounding (the cover block's "heard": its clock past 0.25 s; it
   dispatches "sgwelcomestart" with the ms left in the clip) and the whole flight, the last glyph copy faded, is fitted into what is
   left of the line less T.tail (vo_landing.ogg: 7.09 s, its speech ending at ~6.65 s, so all is over by ~6.4 s): the natural
   timeline (lead 0.2 s, the danda 3.6 s, the comma 4.2 s starting when the danda is 62 % of its way) is scaled by f = what is left /
   that, between .6 and 1. The play button still appears at the line's end, as before; "sgflydone" lets it wait for the flight if a
   flight were ever still running then. (Was [title-fly]: after the line, at the button's reveal, 0.5 s lead, the comma after the danda.)
   WHAT (all in the card's own px, so a resize mid-flight changes nothing):
   1. the blue danda (.sgf-purn) crouches, lifts off (its shadow fades), and flies slowly in an arc to the end of the heading,
      shrinking; over its last fifth it fades into the heading's own "।" - a clone of the heading clipped to that one glyph,
      which grows in at 1.7x around the glyph and settles to exactly 1x on it (the title's font, gold fill, white rim, blue edge),
      with a soft glow and a few sparkles; the clone then fades away over the identical glyph beneath it;
   2. then the green comma (.sgf-commaw) does the same toward the heading's two commas: halfway up it splits in two (a twin that
      was hidden exactly under it, with a copy of its live eyes) and each half settles into one comma of the heading;
   3. the purple question mark stays where it stands and watches: its eyes follow the flying symbols (SGEyes.look, priority 8;
      between the two halves of the comma it glances from one to the other), curious at each lift-off, surprised at the first
      landing, happy at the end. The flying symbols' own eyes look at the title (SGEyes.faceLook).
   The heading itself is never animated: no change of its text, colours or box (the clones are separate elements).
   [title-punct] (asked 2026-11-16: "before the green and the blue symbols fly and gets integrated at the title heading text ... the
   symbols in the title heading text should not be visible at their places and when ... they get integrated then only the original
   title font and text colored symbols should be visible"): the heading's , , । are HIDDEN until their symbols land. The heading is
   clipped (clip-path, even-odd path) with one hole round each of the three glyphs - exactly the region its landing clone shows (the
   glyph's ink box + PAD: the glyph's own white rim, blue edge and soft drop, measured within 9 / 8 / 17 px of the ink; the next
   letters' paint starts 1-3 px outside the hole). From the first paint the CSS rule .sgf-heading.sgf-punct-off holds the holes
   (baked from this measure in Chrome); when the flight starts they are re-measured here and set inline. A hole closes the moment
   its clone has settled at exactly 1x on the glyph (the clone is a copy of the heading: identical pixels), so the title's own glyph
   is there under it before the clone fades away. When all three have landed the heading has no clip-path at all. Should no flight
   run (a welcome that failed or hung: the play button comes without one) or should it fail, the three glyphs are shown at once.
   [title-seq] (asked 2026-11-18: "First of all the Vo should play in the bg and after the VO is over then the green and the blue flying
   animation should take place and when these green and blue symbols gets integrated and placed then this [achievement badge pop]
   sound effect should come along with the golden sparkels animation in the heading title text synced and only after this the play
   button should appear"): the ORDER changes, the flight does not. 1. the welcome plays alone (nothing moves); 2. when it is over (the
   cover block's reveal(), i.e. the line has ended: "sgwelcomeend") the danda and the comma fly as before, at the pace they have had
   since [title-fly2] (T.pace = .84 of the natural timeline: that was its fit on the 7.09 s welcome; no fitting now); 3. the moment the
   last symbol is placed (the two commas' clones settled, the heading whole again) the user's badge pop (sfx_title_badge.ogg, 1.49 s:
   onset ~20 ms, peak ~60 ms, a shimmering tail ~-30 dB at 0.4 s, gone ~1.2 s) plays and, timed from its own "playing" event, the
   title sparkles in gold (sparkle(): a soft gold glow behind the words and a gold wash over the letters peaking with the pop, a white-
   gold gleam sweeping the letters left to right through the tail, gold stars twinkling on the three new symbols at the pop then on
   the letters as the gleam passes, gold dust rising; all gone by ~1.46 s); 4. only then (phase "done", "sgflydone") the play button
   pops in. The heading itself still never animates: the gold is drawn by separate layers (copies of the heading, stars, glow).
   [title-seq2] (asked 2026-11-18, right after: "each time the green and the blue symbol gets integrated play the sound effect"): the
   badge pop - with its golden sparkle, synced as before - comes at EACH integration: first when the blue danda's glyph is placed
   (sparkle("blue"): its stars on the new "।"; the commas, not placed yet, stay hidden in the gold too - the heading's copies take its
   clip of the moment), then when the green comma's two halves are placed (sparkle("green"): stars on the two new commas); the play
   button after the second, as before. ~2.4 s apart, so the two never overlap (should they, the first is ended at once).
   Motion: Web Animations (transform/opacity, keyframes sampled from the paths); side effects (bursts, expressions) on timers.
   SAFE: any error leaves the cover as it was before the flight (the heading whole). */
(function(){
  "use strict";
  // the pictures' ink boxes (alpha > 40), as fractions of each art's width/height (title_char_purn.webp 1254x1254, title_char_comma.webp 1022x1538)
  const INK = { purn: [0.3772, 0.0646, 0.6244, 0.9378], comma: [0.0783, 0.0559, 0.9315, 0.9304] };
  // ms, natural ("slowly"); [title-fly2] scaled to fit the welcome: lead, the danda, the comma's start at 62 % of the danda's flight, the
  // comma, the last copy's fade, and the margin kept before the clip's end (the speech ends ~0.45 s before it; all done ~0.25 s before that)
  const T = { lead: 200, blueMs: 3600, overlap: 0.62, greenMs: 4200, outMs: 450, tail: 700, left: 6700,
              pace: 0.84 };   // [title-seq] the pace the flight has had since [title-fly2] (its fit on the 7.09 s welcome), kept now that it runs after the line
  const N = 90;                                                                   // keyframes per flight
  const st = window.__sgFly = { phase: "wait", t0: 0, glyphs: null, flights: [], hidden: null, shown: [], golds: [] };   // [title-punct] hidden / shown; [title-seq2] golds: one record per sparkle
  const now = ()=> performance.now();
  const lerp = (a, b, k)=> a + (b - a) * k, clamp01 = v => Math.max(0, Math.min(1, v));
  const sine = u => 0.5 - 0.5 * Math.cos(Math.PI * clamp01(u));
  const outC = u => 1 - Math.pow(1 - clamp01(u), 3);
  const bez = (p0, p1, p2, p3, u)=>{ const v = 1 - u, a = v * v * v, b = 3 * v * v * u, c = 3 * v * u * u, d = u * u * u;
    return { x: a * p0.x + b * p1.x + c * p2.x + d * p3.x, y: a * p0.y + b * p1.y + c * p2.y + d * p3.y }; };
  const card = ()=> document.querySelector(".sg-fig .sg-card");
  // card px = the card's padding box (its children's left/top); the card's 9 px border is inside its client rect
  let crC = null, crAt = -1e9;
  function cardRect(){ const tn = now(); if(!crC || tn - crAt > 200){ const c = card(), r = c.getBoundingClientRect(); crC = { left: r.left, top: r.top, k: r.width / c.offsetWidth }; crAt = tn; } return crC; }
  const toScreen = p =>{ const c = cardRect(); return { x: c.left + (p.x + 9) * c.k, y: c.top + (p.y + 9) * c.k }; };
  const toLocal = (x, y)=>{ const c = cardRect(); return { x: (x - c.left) / c.k - 9, y: (y - c.top) / c.k - 9 }; };
  const heading = ()=> document.querySelector(".sg-card > .sgf-heading");

  /* [title-punct] a glyph's own region round its ink box, in the heading's px: the landing clone's clip and the heading's hole */
  const PAD = { x: 14, t: 12, b: 24 };
  const holeOf = b => [b.l - PAD.x, b.t - PAD.t, b.r + PAD.x, b.b + PAD.b];
  let holes = null;                                                               // the glyphs still hidden (measured); null = the CSS's holes
  function setHoles(list){
    const h = heading(); if(!h) return; holes = list;
    // the outer rectangle (the heading's 1096 x 74 box and all its paint, with room to spare) less one rectangle per hidden glyph
    h.style.clipPath = list.length ? 'path(evenodd, "M-200 -200H1296V300H-200Z' + list.map(g =>{ const q = holeOf(g.box).map(v => v.toFixed(2));
      return " M" + q[0] + " " + q[1] + "H" + q[2] + "V" + q[3] + "H" + q[0] + "Z"; }).join("") + '")' : "";
    h.classList.remove("sgf-punct-off");
    st.hidden = list.map(g => g.ch + "@" + g.i);
  }
  function showGlyph(g){ if(!holes) return; setHoles(holes.filter(x => x.i !== g.i)); st.shown.push({ ch: g.ch, i: g.i, at: now() }); }
  function showAll(){ const h = heading(); if(!h || (holes && !holes.length)) return; setHoles([]); st.shown.push({ ch: "all", at: now() }); }

  /* the heading's punctuation, left to right: each glyph's ink box in the heading's own px (for the clone's clip) and in card px */
  function measureGlyphs(){
    const h = document.querySelector(".sg-card > .sgf-heading"); if(!h) return null;
    const tn = [...h.childNodes].find(n => n.nodeType === 3); if(!tn) return null;
    const txt = tn.data, cs = getComputedStyle(h), hr = h.getBoundingClientRect(), u = hr.width / h.offsetWidth;
    const x = document.createElement("canvas").getContext("2d"); x.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
    const lh = parseFloat(cs.lineHeight), out = [];
    for(let i = 0; i < txt.length; i++){
      const ch = txt[i]; if(ch !== "," && ch !== "।") continue;
      const rg = document.createRange(); rg.setStart(tn, i); rg.setEnd(tn, i + 1); const rr = rg.getBoundingClientRect();
      const m = x.measureText(ch), asc = m.fontBoundingBoxAscent, desc = m.fontBoundingBoxDescent;
      const ox = (rr.left - hr.left) / u, base = (lh - (asc + desc)) / 2 + asc;          // one line: the box top is the line's top
      const box = { l: ox - m.actualBoundingBoxLeft, r: ox + m.actualBoundingBoxRight, t: base - m.actualBoundingBoxAscent, b: base + m.actualBoundingBoxDescent };
      const a = toLocal(hr.left + box.l * u, hr.top + box.t * u), b = toLocal(hr.left + box.r * u, hr.top + box.b * u);
      out.push({ ch, i, box, local: { l: a.x, t: a.y, r: b.x, b: b.y, cx: (a.x + b.x) / 2, cy: (a.y + b.y) / 2, w: b.x - a.x, h: b.y - a.y } });
    }
    return out;
  }
  /* the title's own glyph: the heading cloned and clipped to that glyph (+ its rim, edge and drop), in a card-sized wrapper that moves */
  function makeClone(g){
    const h = document.querySelector(".sg-card > .sgf-heading");
    const w = document.createElement("div"); w.className = "sgf-mergew"; w.setAttribute("aria-hidden", "true");
    const c = h.cloneNode(true); c.classList.add("sgf-hclone"); c.classList.remove("sgf-punct-off"); ["role", "aria-level", "aria-label"].forEach(a => c.removeAttribute(a));
    const [L, T_, R, B] = holeOf(g.box);                                         // [title-punct] the same region as the heading's hole
    c.style.clipPath = "polygon(" + [[L, T_], [R, T_], [R, B], [L, B]].map(q => q[0].toFixed(2) + "px " + q[1].toFixed(2) + "px").join(", ") + ")";
    w.style.transformOrigin = g.local.cx.toFixed(2) + "px " + g.local.cy.toFixed(2) + "px"; w.style.opacity = "0";
    w.appendChild(c); card().appendChild(w); return w;
  }
  /* a picture's ink: its centre in the wrapper's px (the transform origin), its centre in card px, its height */
  function inkOf(wrap, img, f){
    const k = cardRect().k, ir = img.getBoundingClientRect(), wr = wrap.getBoundingClientRect();
    const fx = (f[0] + f[2]) / 2, fy = (f[1] + f[3]) / 2;
    return { x: (ir.left - wr.left + fx * ir.width) / k, y: (ir.top - wr.top + fy * ir.height) / k, h: (f[3] - f[1]) * ir.height / k,
             S: toLocal(ir.left + fx * ir.width, ir.top + fy * ir.height) };
  }
  /* one flight at time t (0..1): a = the crouch, a..m the flight along path(e), m..1 the merge on glyph g */
  function sample(o, t){
    const h = o.ink.h, gh = o.g.local.h, S = o.ink.S;
    let p, sx = 1, sy = 1, r = 0, op = 1, cs = 1.7, co = 0, e = 0;
    if(t < o.a){ const k = Math.sin(Math.PI * t / o.a); sy = 1 - 0.12 * k; sx = 1 + 0.07 * k; p = { x: S.x, y: S.y + (1 - sy) * h / 2 }; }
    else if(t < o.m){
      const u = (t - o.a) / (o.m - o.a); e = sine(u); const q = o.path(e);
      const s = lerp(1, 1.7 * 0.95 * gh / h, e), sp = u < 0.25 ? Math.sin(Math.PI * u / 0.25) * 0.06 : 0;   // a little stretch as it rises
      sx = s * (1 - sp * 0.5); sy = s * (1 + sp);
      p = { x: q.x, y: q.y + Math.sin(u * Math.PI * 3) * 5 * (1 - u) }; r = o.sway * Math.sin(u * Math.PI * 2) * (1 - u);
    } else {
      const u = (t - o.m) / (1 - o.m); e = 1; p = { x: o.g.local.cx, y: o.g.local.cy };
      cs = lerp(1.7, 1, outC(u / 0.75)); sx = sy = cs * 0.95 * gh / h;                 // the picture inside the glyph as both shrink onto it
      op = 1 - clamp01((u - 0.1) / 0.65); co = clamp01(u / 0.6);
    }
    if(o.twin) op *= t < o.a ? 0 : clamp01((e - o.split) / 0.03);                     // the twin shows once the split begins
    return { p, sx, sy, r, op, cs, co };
  }
  function flight(o){
    const kf = [], kc = [], S = o.ink.S, G = o.g.local;
    for(let i = 0; i <= N; i++){
      const t = i / N, s = sample(o, t);
      kf.push({ offset: t, opacity: +s.op.toFixed(3), transform: "translate(" + (s.p.x - S.x).toFixed(2) + "px, " + (s.p.y - S.y).toFixed(2) + "px) rotate(" + s.r.toFixed(2) + "deg) scale(" + s.sx.toFixed(4) + ", " + s.sy.toFixed(4) + ")" });
      kc.push({ offset: t, opacity: +s.co.toFixed(3), transform: "translate(" + (s.p.x - G.cx).toFixed(2) + "px, " + (s.p.y - G.cy).toFixed(2) + "px) scale(" + s.cs.toFixed(4) + ")" });
    }
    kc[N].transform = "translate(0px, 0px) scale(1)"; kc[N].opacity = 1;                // exactly on the heading's glyph
    const cw = makeClone(o.g);
    o.el.style.transformOrigin = o.ink.x.toFixed(2) + "px " + o.ink.y.toFixed(2) + "px"; o.el.classList.add("sgf-flying");
    const opt = { duration: o.ms, delay: o.delay, fill: "both", easing: "linear" };
    o.el.animate(kf, opt); const ca = cw.animate(kc, opt);
    if(o.shadow) o.shadow.animate([{ opacity: 1, transform: "scale(1)" }, { opacity: 0, transform: "scale(.55)" }],
                                  { duration: o.ms * 0.3, delay: o.delay + o.ms * o.a * 0.6, fill: "forwards", easing: "ease-out" });
    o.start = st.t0 + o.delay; o.cw = cw;
    st.flights.push({ name: o.name, ch: o.g.ch, start: o.start, ms: o.ms, a: o.a, m: o.m, glyph: { cx: G.cx, cy: G.cy, w: G.w, h: G.h } });
    const dock = o.delay + o.ms * (o.m + 0.6 * (1 - o.m));
    setTimeout(()=> burst(G.cx, G.cy, true), dock);
    // [title-punct] once the clone has settled on the glyph (1x and opaque from 95 % of its own animation - its clock can start a frame or
    // more after this timer's, so it is read, and waited for on a slow device) the heading's own glyph is shown under it, then the clone
    // fades away over that identical glyph
    setTimeout(function land(){ const p = ca.effect ? ca.effect.getComputedTiming().progress : null;
      if(p !== null && p < 0.95 && ca.playState === "running"){ setTimeout(land, 20); return; }
      showGlyph(o.g); o.el.classList.add("sgf-gone"); const f = cw.animate([{ opacity: 1 }, { opacity: 0 }], { duration: T.outMs, fill: "forwards" });
      f.onfinish = ()=> cw.remove();
      if(o.name === "purn") sparkle("blue");                                       // [title-seq2] the blue danda is placed: the badge pop + the golden sparkle
      if(holes && !holes.length && st.phase === "green") sparkle("green"); }, o.delay + o.ms + 60);   // [title-seq] the green comma's two halves placed (the last): again, then the button
    return o;
  }
  /* a soft glow and a few sparkles where a symbol settles (and a small puff where the comma splits) */
  function burst(x, y, big){
    const b = document.createElement("div"); b.className = "sgf-burst"; b.setAttribute("aria-hidden", "true");
    b.style.left = x.toFixed(2) + "px"; b.style.top = y.toFixed(2) + "px";
    const glow = document.createElement("b"); b.appendChild(glow); card().appendChild(b);
    const gs = big ? 1 : 0.6;
    glow.animate([{ opacity: 0, transform: "scale(" + 0.3 * gs + ")" }, { opacity: big ? 0.9 : 0.7, transform: "scale(" + gs + ")", offset: 0.35 }, { opacity: 0, transform: "scale(" + 1.35 * gs + ")" }],
                 { duration: 750, easing: "ease-out", fill: "forwards" });
    const n = big ? 8 : 5;
    for(let k = 0; k < n; k++){
      const s = document.createElement("i"); s.style.background = k % 2 ? "#FFF3B8" : "#FFFFFF"; b.appendChild(s);
      const th = k / n * 6.2832 + Math.random() * 0.4, R = (big ? 36 : 22) + Math.random() * 16, z = 0.6 + Math.random() * 0.6;
      s.animate([{ opacity: 0, transform: "translate(0px, 0px) rotate(0deg) scale(.2)" },
                 { opacity: 1, transform: "translate(" + (0.45 * R * Math.cos(th)).toFixed(1) + "px, " + (0.45 * R * Math.sin(th)).toFixed(1) + "px) rotate(45deg) scale(" + z.toFixed(2) + ")", offset: 0.3 },
                 { opacity: 0, transform: "translate(" + (R * Math.cos(th)).toFixed(1) + "px, " + (R * Math.sin(th)).toFixed(1) + "px) rotate(120deg) scale(.1)" }],
                { duration: 820, easing: "cubic-bezier(.2,.7,.3,1)", fill: "forwards" });
    }
    setTimeout(()=> b.remove(), 1000);
  }
  const eyes = ()=> window.SGEyes || null;
  const react = n =>{ const E = eyes(); if(E) E.react(n); };

  function run(){
    const c = card(); if(!c || !document.body.classList.contains("is-start")) return false;
    const g = measureGlyphs(); if(!g || g.length !== 3 || g[0].ch !== "," || g[1].ch !== "," || g[2].ch !== "।") return false;
    const [c1, c2, dn] = g;
    const purnW = c.querySelector(".sgf-purn"), purnI = purnW && purnW.querySelector("img");
    const commaW = c.querySelector(".sgf-commaw"), commaI = commaW && commaW.querySelector(".sgf-comma");
    if(!purnI || !commaI) return false;
    setHoles(g.slice());                                                          // [title-punct] the holes, as measured here (= the CSS's in Chrome)
    // [title-seq] the timeline at the pace it has had since [title-fly2] (then fitted into what was left of the welcome: .84 on its 7.09 s);
    // it runs after the line now, so nothing is fitted (the last copy's 60 + outMs fade is not scaled, as before)
    const f = T.pace;
    const blueAt = T.lead * f, blueMs = T.blueMs * f, gAt = blueAt + blueMs * T.overlap, greenMs = T.greenMs * f, endAt = gAt + greenMs + 60 + T.outMs + 20;
    st.glyphs = g.map(x => Object.assign({ ch: x.ch }, x.local)); st.t0 = now(); st.phase = "blue";
    st.fit = { f, blueAt, blueMs, gAt, greenMs, endAt };
    const P = q => ({ x: q.local.cx, y: q.local.cy });
    // 1. the danda: an arc up and out to the right, then in to the end of the heading
    const bInk = inkOf(purnW, purnI, INK.purn), bS = bInk.S, bG = P(dn);
    const blue = flight({ name: "purn", el: purnW, ink: bInk, g: dn, ms: blueMs, delay: blueAt, a: 0.1, m: 0.8, sway: 7, shadow: c.querySelector(".sgf-shadow.s1"),
      path: e => bez(bS, { x: bS.x + 30, y: bS.y - 130 }, { x: bG.x + 110, y: bG.y + 30 }, bG, e) });
    // 2. the comma (leaving while the danda makes its approach): up toward the first comma, splitting halfway; the original takes the
    //    second comma, its twin the first
    const cInk = inkOf(commaW, commaI, INK.comma), cS = cInk.S, g1 = P(c1), g2 = P(c2);
    const M = { x: lerp(cS.x, g1.x, 0.55), y: lerp(cS.y, g1.y, 0.5) }, SPLIT = 0.42;
    const common = e => bez(cS, { x: cS.x, y: cS.y - 80 }, { x: M.x - 35, y: M.y + 35 }, M, e);
    const branch = (G, c1p, c2p) => e => e < SPLIT ? common(e / SPLIT) : bez(M, c1p, c2p, G, (e - SPLIT) / (1 - SPLIT));
    const tw = document.createElement("div"); tw.className = "sgf-commaw sgf-twin"; tw.setAttribute("aria-hidden", "true");
    const ti = document.createElement("img"); ti.src = commaI.getAttribute("src"); ti.alt = ""; ti.draggable = false; tw.appendChild(ti);
    const tc = document.createElement("canvas"); tc.className = "sgf-twin-eyes"; tw.appendChild(tc);
    commaW.after(tw);
    const green = flight({ name: "comma", el: commaW, ink: cInk, g: c2, ms: greenMs, delay: gAt, a: 0.1, m: 0.8, sway: 8, shadow: c.querySelector(".sgf-shadow.s2"),
      path: branch(g2, { x: M.x + 70, y: M.y - 35 }, { x: g2.x - 60, y: g2.y + 25 }) });
    const twin = flight({ name: "comma-twin", el: tw, ink: inkOf(tw, ti, INK.comma), g: c1, ms: greenMs, delay: gAt, a: 0.1, m: 0.8, sway: -8, twin: true, split: SPLIT,
      path: branch(g1, { x: M.x + 15, y: M.y - 45 }, { x: g1.x - 35, y: g1.y + 20 }) });
    // the twin's live eyes: a copy of the comma's eye canvas, every frame of the green flight
    const copyEyes = ()=>{ const src = commaW.querySelector("canvas.sgf-eyes");
      if(src && src.width){ if(tc.width !== src.width || tc.height !== src.height){ tc.width = src.width; tc.height = src.height; }
        tc.style.left = src.style.left; tc.style.top = src.style.top; tc.style.width = src.style.width; tc.style.height = src.style.height;
        const x = tc.getContext("2d"); x.clearRect(0, 0, tc.width, tc.height); x.drawImage(src, 0, 0); }
      if(now() < st.t0 + gAt + greenMs + 100 && document.body.classList.contains("is-start")) requestAnimationFrame(copyEyes); };
    setTimeout(()=> requestAnimationFrame(copyEyes), gAt);
    // the split's puff, at the split point (where the eased flight reaches SPLIT)
    const uS = Math.acos(1 - 2 * SPLIT) / Math.PI, tS = 0.1 + 0.7 * uS;
    setTimeout(()=>{ const q = sample(green, tS).p; burst(q.x, q.y, false); }, gAt + greenMs * tS);
    // 3. who looks where: the question mark (the shared brain, priority 8) watches the flying symbol - the danda until it settles,
    //    then the comma; the flyers look at the title
    const at = (o, tn)=> sample(o, clamp01((tn - o.start) / o.ms)).p;
    const blueDock = blue.start + blue.ms * (blue.m + 0.6 * (1 - blue.m));
    const watched = ()=>{ const tn = now();
      if(tn < blueDock) return toScreen(at(blue, tn));
      const t = (tn - green.start) / green.ms;
      if(t < tS + 0.04) return toScreen(at(green, tn));
      return toScreen(at(Math.floor((tn - green.start) / 550) % 2 ? green : twin, tn)); };   // between the two halves, a glance at each in turn
    const E = eyes();
    if(E){ setTimeout(()=> E.look("titlefly", watched, 8, endAt + 200), 50);
      setTimeout(()=> E.faceLook("purn", ()=> toScreen(bG), blueMs + 200), 100);
      setTimeout(()=> E.faceLook("comma", ()=> toScreen({ x: (g1.x + g2.x) / 2, y: g1.y }), greenMs + 200), gAt); }
    setTimeout(()=> react("curious"), blueAt + blueMs * 0.1);
    setTimeout(()=>{ st.phase = "green"; react("curious"); }, gAt + greenMs * 0.1);
    setTimeout(()=>{ try { if(st.phase === "green") prepare(); } catch(e){} }, gAt + greenMs * 0.1 + 60);   // [title-seq] the sparkle's layers, ahead (invisible)
    setTimeout(()=> react("surprise"), blueAt + blueMs * 0.92);
    setTimeout(()=>{ st.flownAt = now(); react("happy"); const e = eyes(); if(e){ e.release("titlefly"); e.faceRelease("purn"); e.faceRelease("comma"); }
      if(st.phase === "green"){ showAll(); sparkle("green"); } }, endAt);   // the last copy has faded ([title-seq] the gold has begun at the last landing; should a landing never have reported, it begins now)
    return true;
  }

  /* ---------- [title-seq] the badge pop and the golden sparkle on the title, each time a symbol is placed ([title-seq2]) ----------
     Timed from the sound's own "playing" event (t = 0; the file's pop: onset ~20 ms, peak ~60 ms; its shimmering tail decays to
     ~-30 dB at 0.4 s, -45 dB at 0.8 s, gone ~1.2 s). Everything in the heading's own px (layers counter-scaled as the heading is):
       glow  a soft gold glow behind the words: up to full at 70 ms (the pop's peak), down with the tail, gone at 1.1 s;
       wash  a copy of the heading whose fill is gold (bright gold tops to amber feet), over the letters: .8 at 70 ms, gone at 1 s;
       gleam a copy of the heading whose fill is one white-gold band, sweeping the letters left to right from 60 to 900 ms;
       stars gold four-point stars (56 px on the symbol(s) just placed, 40-48 over the words at the pop, from 20 ms), then 24 (30-44 px) on
             the letters, each as the gleam reaches it, smaller as the tail fades; each twinkles (grows, turns, shrinks) in 420-560 ms;
       dust  18 gold specks rising from the letters (60-560 ms), fading as they rise.
     All gone by ~1.46 s; at 1.52 s (the clip is 1.49 s) or when the clip ends, whichever is later (at most 3 s), the sparkle ends; after
     the green one the layers are removed and the flight is "done": the play button may come. Muted (the engine's mute) or refused: the sparkle runs on its own clock.
     Its layers are built (invisible) while the comma flies; at the pop every animation is pinned to the clip's own time zero. The
     stars and the dust are drawn on ONE canvas (sprites made once, every frame computed from the clip's clock with the keyframes and
     easings below): as 50 elements (clipped gradient shapes with glows) they were 50 composited layers and the frames stalled
     (0.5-0.7 s gaps in a software-rendered Chrome, where the flight itself runs ~30 fps); one canvas is one layer. */
  const G = { snd: "assets/Audio/sfx_title_badge.ogg", vol: 0.65, peak: 70, glowMs: 1100, washMs: 1000, washOp: 0.8,
              gleamAt: 60, gleamMs: 840, starsPop: 5, starsTrail: 24, dust: 18, endMs: 1520, capMs: 3000, waitPlayMs: 250 };
  // fetched with the cover (47 KB; needed ~13 s later); its own element, not the engine's voice player: the welcome's state and
  // landing-play-ready stay as they are (vol .65: the file peaks at +3.2 dB in float; at .65 -1.3 dB, about the welcome's loudness)
  const goldSnd = (()=>{ try { const a = new Audio(G.snd); a.preload = "auto"; return a; } catch(e){ return null; } })();
  /* the heading's words and marks (space-separated runs), their boxes in the heading's own px: x from the text's own boxes, y = ink */
  function measureRuns(){
    const h = heading(); if(!h) return null;
    const tn = [...h.childNodes].find(n => n.nodeType === 3); if(!tn) return null;
    const txt = tn.data, cs = getComputedStyle(h), hr = h.getBoundingClientRect(), u = hr.width / h.offsetWidth;
    const x = document.createElement("canvas").getContext("2d"); x.font = cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
    const lh = parseFloat(cs.lineHeight), out = [];
    for(let i = 0; i < txt.length;){
      if(txt[i] === " "){ i++; continue; } let j = i; while(j < txt.length && txt[j] !== " ") j++;
      const w = txt.slice(i, j), rg = document.createRange(); rg.setStart(tn, i); rg.setEnd(tn, j); const rr = rg.getBoundingClientRect();
      const m = x.measureText(w), base = (lh - (m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)) / 2 + m.fontBoundingBoxAscent;
      out.push({ w, mark: w === "," || w === "।", l: (rr.left - hr.left) / u, r: (rr.right - hr.left) / u, t: base - m.actualBoundingBoxAscent, b: base + m.actualBoundingBoxDescent });
      i = j;
    }
    return out;
  }
  /* the layers, built ahead while the comma flies (all invisible: opacity 0, the gleam's band off the letters), so that at the pop only
     the animations start - built at the pop, the first frame after it came ~80 ms late (50 new elements to style and paint) */
  let prep = null;
  function prepare(){
    if(prep) return prep;
    const c = card(), h = heading(), runs = measureRuns(); if(!c || !h || !runs || !runs.length) throw new Error("no heading");
    const L = Math.min(...runs.map(r => r.l)), R = Math.max(...runs.map(r => r.r)), Tp = Math.min(...runs.map(r => r.t)), B = Math.max(...runs.map(r => r.b));
    const mk = (cls, parent)=>{ const e = document.createElement("div"); e.className = cls; e.setAttribute("aria-hidden", "true"); (parent || c).appendChild(e); return e; };
    // the glow, behind the heading (heading px)
    const back = mk("sgf-gold back"), glow = mk("sgf-gglow", back);
    glow.style.left = (L - 70).toFixed(1) + "px"; glow.style.width = (R - L + 140).toFixed(1) + "px";
    glow.style.top = (Tp - 34).toFixed(1) + "px"; glow.style.height = (B - Tp + 68).toFixed(1) + "px";
    // the two copies of the heading (card px wrapper, as the landing clones'), then the stars' and the dust's layer over them
    const cw = mk("sgf-goldw");
    const copy = cls =>{ const k = h.cloneNode(true); k.className = "sgf-heading sgf-hclone " + cls; k.removeAttribute("style");
      ["role", "aria-level", "aria-label"].forEach(a => k.removeAttribute(a)); cw.appendChild(k); return k; };
    const wash = copy("sgf-gwash"), gleam = copy("sgf-ggleam");
    const front = mk("sgf-gold front");
    // the gleam's band sits in the middle of a 200 %-wide fill: at background-position p its centre is at W (1 - p); it enters left of
    // the first letter and leaves right of the last
    const xs = L - 90, xe = R + 90, bandAt = x => G.gleamAt + (x - xs) / (xe - xs) * G.gleamMs;
    // the stars' and the dust's canvas (heading px, CV.x/CV.y = its top-left; its pixels at the heading's screen scale x devicePixelRatio)
    const cv = document.createElement("canvas"); cv.className = "sgf-gcv"; front.appendChild(cv);
    const hr = h.getBoundingClientRect(), sc = Math.min(3, (hr.width / h.offsetWidth) * (window.devicePixelRatio || 1));
    cv.width = Math.round(CV.w * sc); cv.height = Math.round(CV.h * sc);
    return prep = { layers: [back, cw, front], glow, wash, gleam, W: h.offsetWidth, xs, xe, bandAt, runs, box: { l: L, r: R, t: Tp, b: B },
                    cv, sc, starImg: starSprite(), dustImg: dustSprite() };
  }
  /* one sparkle's stars and dust ([title-seq2]: made afresh for each): 56 px stars on the symbols just placed (marks), at the pop */
  function makeStars(P, marks){
    const S = { stars: [], dust: [] }, runs = P.runs;
    // the stars: (x, y) on the letters, size s, start at, length ms, full size at pk (the pop's stars early, with the sound's peak)
    const star = (x, y, s, at, ms, pk)=>{ S.stars.push({ x, y, s, at, ms, pk: pk || .35, r0: Math.random() * 40 - 20 }); };
    const words = runs.filter(r => !r.mark), wsum = words.reduce((s, r) => s + r.r - r.l, 0);
    const onLetters = ()=>{ let k = Math.random() * wsum, r = words[0]; for(const q of words){ if(k <= q.r - q.l){ r = q; break; } k -= q.r - q.l; }
      return { x: r.l + 6 + Math.random() * Math.max(1, r.r - r.l - 12), y: r.t + (0.15 + Math.random() * 0.6) * (r.b - r.t) }; };
    marks.forEach((m, i)=> star((m.l + m.r) / 2, (m.t + m.b) / 2, 56, 20 + i * 14, 600, .14));                 // the symbol(s) just placed, at the pop
    for(let i = 0; i < G.starsPop; i++){ const q = onLetters(); star(q.x, q.y, 40 + Math.random() * 8, 30 + i * 16, 560, .16); }
    const trail = []; for(let i = 0; i < G.starsTrail; i++) trail.push(onLetters()); trail.sort((a, b) => a.x - b.x);
    trail.forEach(q =>{ const at = Math.max(40, P.bandAt(q.x) - 50 + Math.random() * 60), k = Math.min(1, at / 900);
      star(q.x, q.y, (34 + Math.random() * 10) * (1 - 0.25 * k), at, 440 + Math.random() * 140); });
    // the dust
    for(let i = 0; i < G.dust; i++){ const q = onLetters();
      S.dust.push({ x: q.x, y: q.y, s: 5 + Math.random() * 4, dx: Math.random() * 24 - 12, dy: -(22 + Math.random() * 26), at: 60 + Math.random() * 500, ms: 700 + Math.random() * 200 }); }
    return S;
  }
  // the canvas's box round the heading (heading px): the biggest star's glow (56 x 2.2) on the marks, the dust rising 48 px above the letters
  const CV = { x: -70, y: -90, w: 1236, h: 260 };
  /* a star sprite (256 px; the star is 256 / 2.2 across, its soft glow fills the rest): a long four-point gold sparkle (white core, gold
     body, deep gold arm tips) with an orange-gold halo, a short diagonal twinkle over it, a warm glow round both */
  const STAR_PX = 256, STAR_K = 2.2;
  function starSprite(){
    const c = document.createElement("canvas"); c.width = c.height = STAR_PX; const x = c.getContext("2d"), m = STAR_PX / 2, s = STAR_PX / STAR_K;
    let g = x.createRadialGradient(m, m, 0, m, m, m);
    g.addColorStop(0, "rgba(255,238,160,.8)"); g.addColorStop(.537, "rgba(255,205,70,.32)"); g.addColorStop(.96, "rgba(255,190,40,0)");   // the CSS glow's 0 / 38 / 68 % of its farthest corner
    x.fillStyle = g; x.fillRect(0, 0, STAR_PX, STAR_PX);
    const shape = (r, w)=>{ x.beginPath(); x.moveTo(m, m - r); x.lineTo(m + w, m - w); x.lineTo(m + r, m); x.lineTo(m + w, m + w); x.lineTo(m, m + r);
      x.lineTo(m - w, m + w); x.lineTo(m - r, m); x.lineTo(m - w, m - w); x.closePath(); };
    x.save(); x.shadowColor = "rgba(255,170,0,.95)"; x.shadowBlur = s * 0.12;
    g = x.createRadialGradient(m, m, 0, m, m, s * 0.7071);
    [[0, "#FFFFFF"], [.14, "#FFFBE0"], [.34, "#FFE34D"], [.58, "#FFC000"], [1, "#E88E00"]].forEach(q => g.addColorStop(q[0], q[1]));
    x.fillStyle = g; shape(s / 2, s * 0.055); x.fill(); x.restore();
    x.save(); x.translate(m, m); x.rotate(Math.PI / 4); x.translate(-m, -m);
    g = x.createRadialGradient(m, m, 0, m, m, s * 0.6 * 0.7071);
    [[0, "#FFFFFF"], [.3, "#FFF0A0"], [1, "#FFC800"]].forEach(q => g.addColorStop(q[0], q[1]));
    x.fillStyle = g; shape(s * 0.3, s * 0.036); x.fill(); x.restore();
    return c;
  }
  /* a gold speck (64 px; the speck is 64 / 2 across, its halo the rest) */
  function dustSprite(){
    const c = document.createElement("canvas"); c.width = c.height = 64; const x = c.getContext("2d");
    x.shadowColor = "rgba(255,176,0,.85)"; x.shadowBlur = 10;
    const g = x.createRadialGradient(32, 32, 0, 32, 32, 16); [[0, "#FFFFFF"], [.45, "#FFE040"], [1, "#F5A800"]].forEach(q => g.addColorStop(q[0], q[1]));
    x.fillStyle = g; x.beginPath(); x.arc(32, 32, 16, 0, 2 * Math.PI); x.fill(); return c;
  }
  /* CSS's cubic-bezier(x1, y1, x2, y2) as a function of progress (bisection on x) */
  function cubicBez(x1, y1, x2, y2){
    const f = (a, b, u)=> 3 * a * u * (1 - u) * (1 - u) + 3 * b * u * u * (1 - u) + u * u * u;
    return v =>{ if(v <= 0) return 0; if(v >= 1) return 1; let lo = 0, hi = 1, u = v;
      for(let i = 0; i < 24; i++){ u = (lo + hi) / 2; if(f(x1, x2, u) < v) lo = u; else hi = u; } return f(y1, y2, u); };
  }
  const EASE_STAR = cubicBez(.2, .7, .3, 1), EASE_OUT = cubicBez(0, 0, .58, 1);
  /* one frame of the stars and the dust at time t (ms on the clip's clock); false once all are over */
  function drawSparkle(P, S, t){
    const x = P.cv.getContext("2d"), sc = P.sc; x.setTransform(1, 0, 0, 1, 0, 0); x.clearRect(0, 0, P.cv.width, P.cv.height);
    let live = false;
    for(const s of S.stars){ const u = (t - s.at) / s.ms; if(u >= 1) continue; live = true; if(u < 0) continue;
      const q = EASE_STAR(u); let op, rot, k;
      if(q < s.pk){ const v = q / s.pk; op = v; rot = s.r0 + 45 * v; k = .1 + .9 * v; }
      else { const v = (q - s.pk) / (1 - s.pk); op = 1 - v; rot = s.r0 + 45 + 65 * v; k = 1 - .85 * v; }
      if(op <= 0.001) continue;
      const w = s.s * STAR_K * k;
      x.globalAlpha = Math.min(1, op); x.setTransform(sc, 0, 0, sc, (s.x - CV.x) * sc, (s.y - CV.y) * sc); x.rotate(rot * Math.PI / 180);
      x.drawImage(P.starImg, -w / 2, -w / 2, w, w); }
    for(const d of S.dust){ const u = (t - d.at) / d.ms; if(u >= 1) continue; live = true; if(u < 0) continue;
      const q = EASE_OUT(u); let op, f, k;
      if(q < .25){ const v = q / .25; op = v; f = .3 * v; k = .4 + .6 * v; } else { const v = (q - .25) / .75; op = 1 - v; f = .3 + .7 * v; k = 1 - .4 * v; }
      if(op <= 0.001) continue;
      const w = d.s * 2 * k;
      x.globalAlpha = Math.min(1, op); x.setTransform(sc, 0, 0, sc, (d.x + d.dx * f - CV.x) * sc, (d.y + d.dy * f - CV.y) * sc);
      x.drawImage(P.dustImg, -w / 2, -w / 2, w, w); }
    x.globalAlpha = 1; return live;
  }
  let endCur = null;                                                              // the running sparkle's end (a new one ends it first)
  function sparkle(kind){
    const last = kind === "green";
    if(last){ if(st.phase !== "green") return; st.phase = "gold"; }
    if(st.golds.some(x => x.kind === kind)) return;                                // once each
    if(endCur) endCur();
    const c = card(), h = heading(); const g = { kind, asked: now(), at: null, snd: null, stars: 0, dust: 0 }; st.golds.push(g); if(last) st.gold = g;
    let done = false, started = false, anims = [], P = null;
    const end = ()=>{ if(done) return; done = true; g.endAt = now(); if(endCur === end) endCur = null;
      anims.forEach(a =>{ try { a.cancel(); } catch(e){} });                       // back to the layers' own invisible look
      try { P && P.cv.getContext("2d").clearRect(0, 0, P.cv.width, P.cv.height); } catch(e){}
      if(last){ try { c && c.querySelectorAll(".sgf-gold, .sgf-goldw").forEach(e => e.remove()); } catch(e){}
        st.phase = "done"; st.doneAt = now(); try { window.dispatchEvent(new Event("sgflydone")); } catch(e){} } };
    endCur = end;
    try {
      const ahead = !!prep; P = prepare(); g.ahead = ahead; g.box = P.box;
      const S = makeStars(P, P.runs.filter(r => r.w === (last ? "," : "।"))); g.stars = S.stars.length; g.dust = S.dust.length;
      g.starList = S.stars.map(s => [+s.x.toFixed(1), +s.y.toFixed(1), +s.s.toFixed(1), Math.round(s.at)]);   // (heading px, size, start ms) for the checks
      // the heading's copies take its clip of the moment: a symbol not placed yet stays hidden in the gold too ([title-punct])
      const clip = h ? h.style.clipPath : ""; P.wash.style.clipPath = clip; P.gleam.style.clipPath = clip; g.clip = clip;
      // t0 = the clip's own time zero on the page's clock: every animation is pinned to it (startTime), so a late first frame skips
      // ahead and the light never trails the sound
      const play = t0 =>{
        if(started || done) return; started = true; g.at = now(); g.t0 = t0;
        const A = (el, kf, opt)=>{ const a = el.animate(kf, opt); anims.push(a); return a; };
        const o = (ms, extra)=> Object.assign({ duration: ms, fill: "both", easing: "linear", delay: 0 }, extra || {});
        const pk = G.peak, p = x => (100 * (1 - x / P.W)).toFixed(2) + "% 0%";
        A(P.glow, [{ opacity: 0, transform: "scale(.82)" }, { opacity: 1, transform: "scale(1)", offset: pk / G.glowMs },
                   { opacity: .42, transform: "scale(1.04)", offset: 330 / G.glowMs }, { opacity: 0, transform: "scale(1.08)" }], o(G.glowMs));
        A(P.wash, [{ opacity: 0 }, { opacity: G.washOp, offset: pk / G.washMs }, { opacity: G.washOp * 0.4, offset: 400 / G.washMs }, { opacity: 0 }], o(G.washMs));
        A(P.gleam, [{ opacity: 1, backgroundPosition: p(P.xs) }, { opacity: 1, backgroundPosition: p(P.xe) }],
          o(G.gleamMs, { delay: G.gleamAt, pseudoElement: "::after", easing: "linear" }));
        anims.forEach(a =>{ try { a.startTime = t0; } catch(e){} });
        // the stars and the dust: every frame from the clip's clock (the frame's own time, as the animations above use)
        g.frames = 0;
        const frame = ts =>{ if(done) return; const tt = (typeof ts === "number" ? ts : now()) - t0; let live = false;
          try { live = drawSparkle(P, S, tt); g.frames++; } catch(e){ g.drawErr = String(e); }
          if(live) requestAnimationFrame(frame); else { try { P.cv.getContext("2d").clearRect(0, 0, P.cv.width, P.cv.height); } catch(e){} } };
        frame(now());                                                             // it schedules itself while anything is still to come
        // the end: the clip's length (or the sparkle's own), at most capMs, on the same clock
        const endMs = Math.max(G.endMs, goldSnd && isFinite(goldSnd.duration) && g.snd === "playing" ? goldSnd.duration * 1000 + 30 : 0);
        g.endMs = Math.min(G.capMs, endMs);
        setTimeout(end, Math.max(0, t0 + g.endMs - now())); };
      // the sound first: the sparkle starts the moment the clip is really playing (or on its own clock after waitPlayMs; at once if the
      // clip was still sounding from the sparkle before: a restart gives no new "playing")
      const muted = typeof isMuted !== "undefined" && isMuted;
      if(goldSnd && !muted){
        const wasOn = !goldSnd.paused && !goldSnd.ended;
        try { goldSnd.volume = G.vol; goldSnd.currentTime = 0; } catch(e){}
        if(!wasOn) goldSnd.addEventListener("playing", ()=>{ g.snd = "playing"; g.sndAt = now(); play(g.sndAt - Math.max(0, (goldSnd.currentTime || 0) * 1000)); }, { once: true });
        const pr = goldSnd.play(); if(pr && pr.catch) pr.catch(err =>{ g.snd = "refused"; play(now()); });
        if(wasOn){ g.snd = "restarted"; play(now()); }
        setTimeout(()=>{ if(!started){ g.snd = g.snd || "late"; play(now()); } }, G.waitPlayMs);
      } else { g.snd = muted ? "muted" : "none"; play(now()); }
    } catch(err){ st.err = String(err); g.err = String(err); if(last){ try { c && c.querySelectorAll(".sgf-gold, .sgf-goldw").forEach(e => e.remove()); } catch(x){} } end(); }
    setTimeout(end, G.capMs + G.waitPlayMs + 200);                                 // never holds the play button up
  }
  let fired = false;
  // [title-seq] the flight starts when the welcome is OVER (the cover block's reveal() at the line's end dispatches "sgwelcomeend"; was
  // [title-fly2] "sgwelcomestart" while it sounded)
  window.addEventListener("sgwelcomeend", ()=>{ if(fired) return; fired = true;
    try { if(!run()) showAll(); }                                                     // [title-punct] no flight: the heading whole at once
    catch(err){ st.phase = "error"; st.err = String(err); try { showAll(); } catch(e){} try { window.dispatchEvent(new Event("sgflydone")); } catch(e){} } });
  // [title-punct] the play button came and no symbol has flown (the welcome failed or hung): the heading whole, as before
  const btn = document.getElementById("sgBtn");
  if(btn) new MutationObserver(()=>{ if(btn.classList.contains("ready") && st.phase === "wait") showAll(); }).observe(btn, { attributes:true, attributeFilter:["class"] });
})();

/* ===== [dun-chrome] end ===== */

/* ---- [q-noto] (2026-11-15) the page's id on #slideHost (data-slide), set before each page mounts, so style.css can give one page's
   "?" the Noto face; and both Noto "?" faces loaded at once, so a mark's ink is measured in its own face (the modules' centreInk) ---- */
(function(){ "use strict";
  const om = window.mountSlide; if(typeof om !== "function") return;
  window.mountSlide = function(idx){
    try { const h = document.getElementById("slideHost"), s = CARD.slides[idx]; if(h) h.dataset.slide = s ? s.id : ""; } catch(e){}
    return om.apply(this, arguments); };
  try { if(document.fonts && document.fonts.load){ document.fonts.load("800 50px 'Story Noto Q'", "?"); document.fonts.load("700 31px 'Story Noto Q 700'", "?"); } } catch(e){}
})();

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
