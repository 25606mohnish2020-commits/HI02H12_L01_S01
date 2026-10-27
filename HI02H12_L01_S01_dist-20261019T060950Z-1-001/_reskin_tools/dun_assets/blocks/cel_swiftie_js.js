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
