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
   SAFE: canvas draws only; the loop stops off the cover; reduced motion = eyes that look at the child and blink; any error removes
   the overlays, which leaves the painted eyes. */
(function(){
  "use strict";
  const FACES = __FACES__;                                   // build.py: title_assets/cover_eyes_data.json (title_eyes_measure.py)
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
    react(name){ if(reduce || !EXPR[name]) return; expr = EXPR[name]; exprName = name; exprUntil = now() + expr.ms;
      if(name === "wince") faces.forEach(F => blink(F, now(), 170, true)); },
    debug(){ return faces.map(F => ({ g: { x: +F.g.x.toFixed(3), y: +F.g.y.toFixed(3) }, blinks: F.blinks, lid: +blinkU(F, now()).toFixed(2), on: !!(F.cv && F.cv.style.display === "block"), expr: expr && now() < exprUntil ? exprName : null })); }
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
        if(!reduce) gaze(F, dt, tn, T); else { F.g.x = 0; F.g.y = 0; }
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
