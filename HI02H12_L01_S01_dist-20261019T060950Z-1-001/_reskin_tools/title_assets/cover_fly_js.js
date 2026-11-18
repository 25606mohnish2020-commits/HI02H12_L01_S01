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
   last symbol is placed (the two commas' clones settled, the heading whole again) the user's badge pop (sfx_title_badge.mp3, 1.49 s:
   onset ~20 ms, peak ~60 ms, a shimmering tail ~-30 dB at 0.4 s, gone ~1.2 s) plays and, timed from its own "playing" event, the
   title sparkles in gold (gold(): a soft gold glow behind the words and a gold wash over the letters peaking with the pop, a white-
   gold gleam sweeping the letters left to right through the tail, gold stars twinkling on the three new symbols at the pop then on
   the letters as the gleam passes, gold dust rising; all gone by ~1.46 s); 4. only then (phase "done", "sgflydone") the play button
   pops in. The heading itself still never animates: the gold is drawn by separate layers (copies of the heading, stars, glow).
   Motion: Web Animations (transform/opacity, keyframes sampled from the paths); side effects (bursts, expressions) on timers.
   SAFE: any error leaves the cover as it was before the flight (the heading whole). */
(function(){
  "use strict";
  // the pictures' ink boxes (alpha > 40), as fractions of each art's width/height (title_char_purn.png 1254x1254, title_char_comma.png 1022x1538)
  const INK = { purn: [0.3772, 0.0646, 0.6244, 0.9378], comma: [0.0783, 0.0559, 0.9315, 0.9304] };
  // ms, natural ("slowly"); [title-fly2] scaled to fit the welcome: lead, the danda, the comma's start at 62 % of the danda's flight, the
  // comma, the last copy's fade, and the margin kept before the clip's end (the speech ends ~0.45 s before it; all done ~0.25 s before that)
  const T = { lead: 200, blueMs: 3600, overlap: 0.62, greenMs: 4200, outMs: 450, tail: 700, left: 6700,
              pace: 0.84 };   // [title-seq] the pace the flight has had since [title-fly2] (its fit on the 7.09 s welcome), kept now that it runs after the line
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
      f.onfinish = ()=> cw.remove();
      if(holes && !holes.length && st.phase === "green") gold(); }, o.delay + o.ms + 60);   // [title-seq] the last symbol is placed: the badge pop + the golden sparkle
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
      if(st.phase === "green"){ showAll(); gold(); } }, endAt);   // the last copy has faded ([title-seq] the gold has begun at the last landing; should a landing never have reported, it begins now)
    return true;
  }

  /* ---------- [title-seq] the badge pop and the golden sparkle on the title, once the last symbol is placed ----------
     Timed from the sound's own "playing" event (t = 0; the file's pop: onset ~20 ms, peak ~60 ms; its shimmering tail decays to
     ~-30 dB at 0.4 s, -45 dB at 0.8 s, gone ~1.2 s). Everything in the heading's own px (layers counter-scaled as the heading is):
       glow  a soft gold glow behind the words: up to full at 70 ms (the pop's peak), down with the tail, gone at 1.1 s;
       wash  a copy of the heading whose fill is gold (bright gold tops to amber feet), over the letters: .8 at 70 ms, gone at 1 s;
       gleam a copy of the heading whose fill is one white-gold band, sweeping the letters left to right from 60 to 900 ms;
       stars gold four-point stars (56 px on the three new symbols, 40-48 over the words at the pop, from 20 ms), then 24 (30-44 px) on
             the letters, each as the gleam reaches it, smaller as the tail fades; each twinkles (grows, turns, shrinks) in 420-560 ms;
       dust  18 gold specks rising from the letters (60-560 ms), fading as they rise.
     All gone by ~1.46 s; at 1.52 s (the clip is 1.49 s) or when the clip ends, whichever is later (at most 3 s), the layers are removed
     and the flight is "done": the play button may come. Muted (the engine's mute) or refused: the sparkle runs on its own clock.
     Its layers are built (invisible) while the comma flies; at the pop every animation is pinned to the clip's own time zero. The
     stars and the dust are drawn on ONE canvas (sprites made once, every frame computed from the clip's clock with the keyframes and
     easings below): as 50 elements (clipped gradient shapes with glows) they were 50 composited layers and the frames stalled
     (0.5-0.7 s gaps in a software-rendered Chrome, where the flight itself runs ~30 fps); one canvas is one layer. */
  const G = { snd: "assets/Audio/sfx_title_badge.mp3", vol: 0.65, peak: 70, glowMs: 1100, washMs: 1000, washOp: 0.8,
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
    const P = prep = { layers: [back, cw, front], glow, wash, gleam, W: h.offsetWidth, xs, xe, box: { l: L, r: R, t: Tp, b: B }, stars: [], dust: [],
                       cv, sc, starImg: starSprite(), dustImg: dustSprite() };
    // the stars: (x, y) on the letters, size s, start at, length ms, full size at pk (the pop's stars early, with the sound's peak)
    const star = (x, y, s, at, ms, pk)=>{ P.stars.push({ x, y, s, at, ms, pk: pk || .35, r0: Math.random() * 40 - 20 }); };
    const words = runs.filter(r => !r.mark), marks = runs.filter(r => r.mark), wsum = words.reduce((s, r) => s + r.r - r.l, 0);
    const onLetters = ()=>{ let k = Math.random() * wsum, r = words[0]; for(const q of words){ if(k <= q.r - q.l){ r = q; break; } k -= q.r - q.l; }
      return { x: r.l + 6 + Math.random() * Math.max(1, r.r - r.l - 12), y: r.t + (0.15 + Math.random() * 0.6) * (r.b - r.t) }; };
    marks.forEach((m, i)=> star((m.l + m.r) / 2, (m.t + m.b) / 2, 56, 20 + i * 14, 600, .14));                 // the three new symbols, at the pop
    for(let i = 0; i < G.starsPop; i++){ const q = onLetters(); star(q.x, q.y, 40 + Math.random() * 8, 30 + i * 16, 560, .16); }
    const trail = []; for(let i = 0; i < G.starsTrail; i++) trail.push(onLetters()); trail.sort((a, b) => a.x - b.x);
    trail.forEach(q =>{ const at = Math.max(40, bandAt(q.x) - 50 + Math.random() * 60), k = Math.min(1, at / 900);
      star(q.x, q.y, (34 + Math.random() * 10) * (1 - 0.25 * k), at, 440 + Math.random() * 140); });
    // the dust
    for(let i = 0; i < G.dust; i++){ const q = onLetters();
      P.dust.push({ x: q.x, y: q.y, s: 5 + Math.random() * 4, dx: Math.random() * 24 - 12, dy: -(22 + Math.random() * 26), at: 60 + Math.random() * 500, ms: 700 + Math.random() * 200 }); }
    return P;
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
  function drawSparkle(P, t){
    const x = P.cv.getContext("2d"), sc = P.sc; x.setTransform(1, 0, 0, 1, 0, 0); x.clearRect(0, 0, P.cv.width, P.cv.height);
    let live = false;
    for(const s of P.stars){ const u = (t - s.at) / s.ms; if(u >= 1) continue; live = true; if(u < 0) continue;
      const q = EASE_STAR(u); let op, rot, k;
      if(q < s.pk){ const v = q / s.pk; op = v; rot = s.r0 + 45 * v; k = .1 + .9 * v; }
      else { const v = (q - s.pk) / (1 - s.pk); op = 1 - v; rot = s.r0 + 45 + 65 * v; k = 1 - .85 * v; }
      if(op <= 0.001) continue;
      const w = s.s * STAR_K * k;
      x.globalAlpha = Math.min(1, op); x.setTransform(sc, 0, 0, sc, (s.x - CV.x) * sc, (s.y - CV.y) * sc); x.rotate(rot * Math.PI / 180);
      x.drawImage(P.starImg, -w / 2, -w / 2, w, w); }
    for(const d of P.dust){ const u = (t - d.at) / d.ms; if(u >= 1) continue; live = true; if(u < 0) continue;
      const q = EASE_OUT(u); let op, f, k;
      if(q < .25){ const v = q / .25; op = v; f = .3 * v; k = .4 + .6 * v; } else { const v = (q - .25) / .75; op = 1 - v; f = .3 + .7 * v; k = 1 - .4 * v; }
      if(op <= 0.001) continue;
      const w = d.s * 2 * k;
      x.globalAlpha = Math.min(1, op); x.setTransform(sc, 0, 0, sc, (d.x + d.dx * f - CV.x) * sc, (d.y + d.dy * f - CV.y) * sc);
      x.drawImage(P.dustImg, -w / 2, -w / 2, w, w); }
    x.globalAlpha = 1; return live;
  }
  function gold(){
    if(st.phase !== "green") return; st.phase = "gold";
    const c = card(); const g = st.gold = { asked: now(), at: null, snd: null, stars: 0, dust: 0 };
    let done = false, started = false;
    const finish = ()=>{ if(done) return; done = true;
      try { c && c.querySelectorAll(".sgf-gold, .sgf-goldw").forEach(e => e.remove()); } catch(e){}
      st.phase = "done"; st.doneAt = now(); try { window.dispatchEvent(new Event("sgflydone")); } catch(e){} };
    try {
      const ahead = !!prep, P = prepare(); g.ahead = ahead; g.box = P.box; g.stars = P.stars.length; g.dust = P.dust.length;
      g.starList = P.stars.map(s => [+s.x.toFixed(1), +s.y.toFixed(1), +s.s.toFixed(1), Math.round(s.at)]);   // (heading px, size, start ms) for the checks
      // t0 = the clip's own time zero on the page's clock: every animation is pinned to it (startTime), so a late first frame skips
      // ahead and the light never trails the sound
      const play = t0 =>{
        if(started) return; started = true; g.at = now(); g.t0 = t0;
        const anims = [], A = (el, kf, opt)=>{ const a = el.animate(kf, opt); anims.push(a); return a; };
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
          try { live = drawSparkle(P, tt); g.frames++; } catch(e){ g.drawErr = String(e); }
          if(live) requestAnimationFrame(frame); else { try { P.cv.getContext("2d").clearRect(0, 0, P.cv.width, P.cv.height); } catch(e){} } };
        frame(now());                                                             // it schedules itself while anything is still to come
        // the end: the clip's length (or the sparkle's own), at most capMs, on the same clock
        const endMs = Math.max(G.endMs, goldSnd && isFinite(goldSnd.duration) && g.snd === "playing" ? goldSnd.duration * 1000 + 30 : 0);
        g.endMs = Math.min(G.capMs, endMs);
        setTimeout(finish, Math.max(0, t0 + g.endMs - now())); };
      // the sound first: the sparkle starts the moment the clip is really playing (or on its own clock after waitPlayMs)
      const muted = typeof isMuted !== "undefined" && isMuted;
      if(goldSnd && !muted){
        try { goldSnd.volume = G.vol; goldSnd.currentTime = 0; } catch(e){}
        goldSnd.addEventListener("playing", ()=>{ g.snd = "playing"; g.sndAt = now(); play(g.sndAt - Math.max(0, (goldSnd.currentTime || 0) * 1000)); }, { once: true });
        const pr = goldSnd.play(); if(pr && pr.catch) pr.catch(err =>{ g.snd = "refused"; play(now()); });
        setTimeout(()=>{ if(!started){ g.snd = g.snd || "late"; play(now()); } }, G.waitPlayMs);
      } else { g.snd = muted ? "muted" : "none"; play(now()); }
    } catch(err){ st.err = String(err); g.err = String(err); try { c && c.querySelectorAll(".sgf-gold, .sgf-goldw").forEach(e => e.remove()); } catch(x){} finish(); }
    setTimeout(finish, G.capMs + G.waitPlayMs + 200);                               // never holds the play button up
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
