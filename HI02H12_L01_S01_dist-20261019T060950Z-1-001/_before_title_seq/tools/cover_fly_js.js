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
   Motion: Web Animations (transform/opacity, keyframes sampled from the paths); side effects (bursts, expressions) on timers.
   SAFE: any error leaves the cover as it was before the flight (the heading whole). */
(function(){
  "use strict";
  // the pictures' ink boxes (alpha > 40), as fractions of each art's width/height (title_char_purn.png 1254x1254, title_char_comma.png 1022x1538)
  const INK = { purn: [0.3772, 0.0646, 0.6244, 0.9378], comma: [0.0783, 0.0559, 0.9315, 0.9304] };
  // ms, natural ("slowly"); [title-fly2] scaled to fit the welcome: lead, the danda, the comma's start at 62 % of the danda's flight, the
  // comma, the last copy's fade, and the margin kept before the clip's end (the speech ends ~0.45 s before it; all done ~0.25 s before that)
  const T = { lead: 200, blueMs: 3600, overlap: 0.62, greenMs: 4200, outMs: 450, tail: 700, left: 6700 };
  const N = 90;                                                                   // keyframes per flight
  const st = window.__sgFly = { phase: "wait", t0: 0, glyphs: null, flights: [], hidden: null, shown: [] };   // [title-punct] hidden / shown
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
      f.onfinish = ()=> cw.remove(); }, o.delay + o.ms + 60);
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

  function run(left){
    const c = card(); if(!c || !document.body.classList.contains("is-start")) return false;
    const g = measureGlyphs(); if(!g || g.length !== 3 || g[0].ch !== "," || g[1].ch !== "," || g[2].ch !== "।") return false;
    const [c1, c2, dn] = g;
    const purnW = c.querySelector(".sgf-purn"), purnI = purnW && purnW.querySelector("img");
    const commaW = c.querySelector(".sgf-commaw"), commaI = commaW && commaW.querySelector(".sgf-comma");
    if(!purnI || !commaI) return false;
    setHoles(g.slice());                                                          // [title-punct] the holes, as measured here (= the CSS's in Chrome)
    // [title-fly2] the timeline, fitted into what is left of the welcome (the last copy's 60 + outMs fade is not scaled)
    if(!(left > 0 && isFinite(left))) left = T.left;
    const f = Math.max(0.6, Math.min(1, (left - T.tail - 60 - T.outMs) / (T.lead + T.blueMs * T.overlap + T.greenMs)));
    const blueAt = T.lead * f, blueMs = T.blueMs * f, gAt = blueAt + blueMs * T.overlap, greenMs = T.greenMs * f, endAt = gAt + greenMs + 60 + T.outMs + 20;
    st.glyphs = g.map(x => Object.assign({ ch: x.ch }, x.local)); st.t0 = now(); st.phase = "blue";
    st.fit = { left, f, blueAt, blueMs, gAt, greenMs, endAt };
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
    setTimeout(()=> react("surprise"), blueAt + blueMs * 0.92);
    setTimeout(()=>{ st.phase = "done"; st.doneAt = now(); react("happy"); const e = eyes(); if(e){ e.release("titlefly"); e.faceRelease("purn"); e.faceRelease("comma"); }
      try { window.dispatchEvent(new Event("sgflydone")); } catch(err){} }, endAt);   // [title-fly2] the last copy has faded: the play button may come
    return true;
  }
  let fired = false;
  window.addEventListener("sgwelcomestart", ev =>{ if(fired) return; fired = true;
    try { if(!run(ev && ev.detail ? ev.detail.left : 0)) showAll(); }                 // [title-punct] no flight: the heading whole at once
    catch(err){ st.phase = "error"; st.err = String(err); try { showAll(); } catch(e){} try { window.dispatchEvent(new Event("sgflydone")); } catch(e){} } });
  // [title-punct] the play button came and no symbol has flown (the welcome failed or hung): the heading whole, as before
  const btn = document.getElementById("sgBtn");
  if(btn) new MutationObserver(()=>{ if(btn.classList.contains("ready") && st.phase === "wait") showAll(); }).observe(btn, { attributes:true, attributeFilter:["class"] });
})();
