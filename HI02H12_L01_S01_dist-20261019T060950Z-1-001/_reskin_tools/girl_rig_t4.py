"""girl_rig_t4.py — [t4-basket] (2026-11-02) the T4 girl's look-into-the-basket rig, cut from her own bitmap
(demo3_assets/img_demo3_girl_basket.webp, the frame 723:1575's "image 276", 1024x1535, drawn 224x336).

The page shows her as LAYERS that window the same bitmap (so at rest the composite is the painting) and move by CSS transforms —
see build.py [t4-basket] and the PUNCT_SCENE module:
  under   her dress / bodice / the background behind what the motion uncovers (demo3_girl_under.png, its own RGBA image): the
          layers only move straight up (the lift) or down (the dip), so what lies behind an uncovered band is the continuation of
          the static picture just past it — each band is that picture COPIED from just below it (the lift) or above it (the dip)
          by the band's thickness (the lift's bands one offset: neighbouring columns agree), along a measured edge where one
          slants, then Poisson-matched to the static picture at every seam (the copy's texture kept: the pleats, the bodice's
          trims and dots, the background beside her other arm run on); bands with no static picture within 4 px: a harmonic fill
  body    the bitmap with a HOLE where the moving parts are (demo3_girl_body_mask.png)
  fore    her right forearm (the viewer's left) from a vertical line at the elbow (x_e) to the wrist (x_w), SHEARED (skewY about
          x_e): its displacement grows linearly from 0 at the elbow to exactly the basket's lift at the wrist, so both seams are
          continuous (a pure rotation about the elbow would move the wrist sideways, the hand not)
  elbow   the upper arm's fold over the forearm (the crease), static, drawn OVER the forearm: the forearm tucks under it
  basket  the basket, the fruits, the handle and both hands, translated straight up by LIFT
  head    the head above the jaw's cut WITH both braids and their bobbles (no cut crosses any hair; the neck, the shoulders, the
          sleeves stay), translated down by DIP, drawn under the basket (the braid tip goes behind the handle): the eyes
          (interior windows, sclera discs, completed irises as girl_rig.py's) ride inside it
Writes demo3_assets/girl_rig/ (the sheets, rig.json with the geometry in bitmap px) and, with --debug <dir>, overlays and the
rig's composite at the gesture's peak. Masks are full 1024x1535 sheets with the mask in ALPHA (Chrome masks by a raster's alpha).
Run: python -I -X utf8 girl_rig_t4.py [--debug <dir>]
"""
import sys, json, pathlib, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SCR = pathlib.Path(__file__).resolve().parent
SRC = SCR / "demo3_assets" / "img_demo3_girl_basket.webp"
OUT = SCR / "demo3_assets" / "girl_rig"; OUT.mkdir(exist_ok=True)
DEBUG = pathlib.Path(sys.argv[sys.argv.index("--debug") + 1]) if "--debug" in sys.argv else None
if DEBUG: DEBUG.mkdir(parents=True, exist_ok=True)

LIFT = 16.0    # bitmap px the basket rises (3.5 px on the page)
DIP = 7.0      # bitmap px the head dips (1.5 px on the page)
X_E, X_W = 382.0, 476.0   # the forearm's shear: 0 at the elbow's vertical line, LIFT at the wrist's

im = Image.open(SRC).convert("RGBA"); W, H = im.size
assert (W, H) == (1024, 1535), (W, H)
A = np.asarray(im).astype(np.float32); rgb = A[..., :3]; alpha = A[..., 3]
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
mx = rgb.max(axis=2); mn = rgb.min(axis=2)
solid = alpha > 0
opaque = alpha >= 250
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def box_mask(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[int(y0):int(y1), int(x0):int(x1)] = True; return m
def poly_mask(pts):
    pm = Image.new("L", (W, H), 0); ImageDraw.Draw(pm).polygon([tuple(p) for p in pts], fill=255); return np.asarray(pm) > 0
def dilate(m, r):
    k = int(math.ceil(r)); out = m.copy()
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            if dx * dx + dy * dy > r * r + 1e-6 or (dx == 0 and dy == 0): continue
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out
def erode(m, r): return ~dilate(~m, r)
def grow(seed, allowed, iters=4000):
    """flood fill (4-connected) from seed through allowed"""
    cur = seed & allowed
    for _ in range(iters):
        nxt = cur.copy()
        nxt[1:, :] |= cur[:-1, :]; nxt[:-1, :] |= cur[1:, :]; nxt[:, 1:] |= cur[:, :-1]; nxt[:, :-1] |= cur[:, 1:]
        nxt &= allowed
        if (nxt == cur).all(): return cur
        cur = nxt
    return cur
def save_mask(m, path):
    a = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8), "L"); w = Image.new("L", a.size, 255)
    Image.merge("RGBA", [w, w, w, a]).save(path, optimize=True)
def fit_circle(pts):
    x, y = pts[:, 0], pts[:, 1]
    M = np.column_stack([x, y, np.ones_like(x)]); b = -(x * x + y * y)
    (D, E, F), *_ = np.linalg.lstsq(M, b, rcond=None)
    cx, cy = -D / 2, -E / 2; return cx, cy, math.sqrt(cx * cx + cy * cy - F)
def boundary(m):
    e = np.zeros_like(m)
    e[1:, :] |= m[1:, :] & ~m[:-1, :]; e[:-1, :] |= m[:-1, :] & ~m[1:, :]
    e[:, 1:] |= m[:, 1:] & ~m[:, :-1]; e[:, :-1] |= m[:, :-1] & ~m[:, 1:]
    return e

# ---------- colour classes (sampled: the dress 254,85,131 / 252,89,135, its pleats darker; the trims 254,232,214; the skin
# 253,186,126 / 248,165,102; the basket's weave 253,173,79 / 236,147,52, its outline 154,50,31; the apple 180,25,23) ----------
hue = np.where(mx == R, 60 * (G - B) / np.maximum(mx - mn, 1), 0); sat = (mx - mn) / np.maximum(mx, 1)
pink = solid & (R > 100) & (hue < -14) & (sat > 0.25)                         # the dress's pinks to its dark-magenta outlines (hue < -14; the apple's red ~0)
light = solid & (mn > 165) & (B > 150)                                       # the trims, the dots, the motifs (and shines)
blend = solid & (R > 215) & (G - B < 25) & (mn > 60)                          # white-to-pink blends (the white work's rims)
dress = grow(pink & (sat > 0.4), pink | light | blend, iters=6000)             # the dress / bodice / sleeves with their white work
# the skin by saturation (measured: the cheek / forearm / hands 0.48-0.57; the basket's weave and handle 0.62-0.98, their hues
# the skin's): the strict class for the arms and hands, a looser one (the neck's shade reads 0.64) for the jaw's walk
skin = solid & (R > 195) & (B > 80) & (sat > 0.40) & (sat < 0.61) & (hue > 17) & (hue < 32)
skin_j = solid & (R > 190) & (B > 55) & (sat < 0.72) & (hue > 14) & (hue < 34)
hair = solid & (mx < 120) & (R - B < 35)
report = {"lift": LIFT, "dip": DIP}

# ================= the forearm (the viewer's left) =================
# measured on the 3x zoom: the upper arm's inner edge comes down to the crease (404,637)-(431,651), the forearm's upper outline
# runs from there to the hand's back (473,720), its lower outline from the elbow's bend (360,697) to (487,773); the wrist
# crosses at x ~476. SEP = the line the elbow patch keeps above: from the elbow's vertical line through the crease
SEP = [(X_E - 6, 668.0), (404.0, 638.5), (431.0, 652.5), (452.0, 667.0)]
ARM_POLY = SEP + [(466.0, 690.0), (472.0, 707.0), (478.0, 716.0), (X_W + 12, 716.0), (X_W + 12, 812.0), (X_E - 6, 812.0)]   # its top along the forearm's upper outline (the rim's left edge x ~467 stays out)
arm_zone = poly_mask(ARM_POLY)
arm_skin = skin & arm_zone & (XX >= X_E - 6)
arm_pix = arm_zone & solid & ~dress & (dilate(arm_skin, 3.5) | arm_skin)    # the skin + its outline (within 3.5 px of the skin)
arm_pix |= arm_zone & solid & dilate(arm_pix, 1.5) & ~opaque                 # the anti-aliased rim against the background
arm_pix |= arm_zone & dress & dilate(arm_pix, 1.5) & ~pink                    # the blend pixels of the rim against the dress

# ================= the basket + the fruits + the handle + both hands =================
POLY_B = [(448, 640), (470, 560), (520, 505), (610, 498), (700, 505), (760, 520), (805, 560), (815, 640), (818, 720), (815, 812),
          (700, 830), (600, 838), (X_W, 820), (X_W, 712), (448, 712)]
bzone = poly_mask(POLY_B)
HAND_L = box_mask(X_W, 690, 600, 815); HAND_R = box_mask(715, 680, 820, 815)
RARM = box_mask(680, 518, 752, 606)                                          # her other arm, seen inside the arc above the bananas
# the arm's skin (lit and shaded) flooded from inside it; its outline = the dark pixels beside it that also touch the background
# (its silhouette); the contacts with the handle / the bananas are THEIR outlines (they lie in front) and move with them
loose = solid & (R > 175) & (B > 40) & (hue > 12) & (hue < 36) & (sat < 0.80)
rarm_core = grow(box_mask(704, 570, 716, 580), loose & RARM)   # seeded in the arm BELOW the handle (it crosses the arm at y 520-555)
rarm = rarm_core | (dilate(rarm_core, 3.0) & dilate(~solid, 3.0) & RARM & solid & ~loose)
# the braid tip above the handle's outer edge (measured on the 3x zoom: 713,525 / 747,543 / 767,563 / 780,593 / 787,627)
BRAID_EX = poly_mask([(700, 440), (845, 440), (845, 640), (788, 626), (781, 592), (768, 561), (748, 541), (714, 523), (700, 522)])
cand = bzone & solid & ~dress & ~hair & ~rarm & ~BRAID_EX & ~arm_pix
seed = box_mask(560, 700, 680, 790)
basket = grow(seed, cand)
basket |= bzone & solid & dilate(basket, 1.5) & ~opaque & ~arm_pix          # the AA rim against the background (the right hand, the handle)
basket |= bzone & dress & dilate(basket, 1.5) & ~pink & ~arm_pix             # the blend pixels against the dress
# close pinholes (the fruits' shines read as 'light' next to no pink: they are already in; this catches 1-2 px specks)
holes = bzone & ~basket & erode(dilate(basket, 2.0), 2.0) & ~dress & ~arm_pix
basket |= holes
basket |= dilate(basket, 2.0) & dress & bzone & ~arm_pix & ~BRAID_EX         # the outline's blends into the dress move with it
basket |= dilate(basket, 2.0) & rarm & ~dilate(~solid, 2.0)                  # and those over her other arm (the handle lies in front of it)
rarm &= ~basket
fore = arm_pix & ~basket
fore |= dilate(fore, 2.0) & dress & arm_zone & ~basket
report["basket_px"] = int(basket.sum()); report["fore_px"] = int(fore.sum())
print("basket layer %d px, forearm layer %d px" % (basket.sum(), fore.sum()))

# the elbow patch: the upper arm just above SEP (its crease line included), static, over the forearm
sep_poly = [(X_E - 16, 640.0), (400.0, 610.0), (440.0, 630.0), (458.0, 660.0)] + SEP[::-1]
elbow_zone = poly_mask(sep_poly)
elbow = elbow_zone & solid & ~dress & ~basket
fore &= ~elbow

# ================= the head =================
# the cut: along the jaw's lower edge + 2 px into the neck (the face's flood takes in the ears; a walk down from the cheek stopped
# at the mouth, one up from the neck at the dress / the hair beside it)
face = grow(box_mask(520, 320, 560, 345), skin_j & box_mask(400, 150, 700, 432))   # the face's skin, bounded by its outline
def jaw_lower(x):
    """the jaw outline's lower edge in column x: below the face's lowest skin pixel, through the outline (solid, not skin)"""
    ys = np.nonzero(face[:, x])[0]
    if not len(ys): return None
    y = ys.max() + 1
    while y < 450 and solid[y, x] and not skin_j[y, x] and not hair[y, x]: y += 1
    return float(y)
fx_ = np.nonzero(face.any(axis=0))[0]
JX0, JX1 = int(fx_.min()), int(fx_.max())
jaw = [(x, jaw_lower(x)) for x in range(JX0, JX1 + 1)]
jaw = [(x, y) for x, y in jaw if y is not None and y > 330]
jx = np.array([p[0] for p in jaw], np.float32); jy = np.array([p[1] for p in jaw], np.float32)
k = 7; jy_s = np.convolve(np.pad(jy, k, mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="valid")
jy_s = np.maximum(jy_s, jy)                                                  # never above the outline's own lower edge
# the head = above the jaw's cut (x JX0..JX1; the face's flood takes in the ears) and, beside it, everything solid above y 392 but
# the dress; then BOTH braids with their bobbles, flooded from that hair down to their tips — no cut crosses any hair (a cut
# through a braid steps its silhouette as the head dips); the neck, the shoulders, the sleeves, the arms and the basket stay
cut_line = np.interp(XX[0], jx, jy_s + 2.0)
span = (XX[0] >= jx[0]) & (XX[0] <= jx[-1])
head_top = solid & ~dress & np.where(span[None, :], YY < cut_line[None, :], YY < 392)
hair_l = solid & (mx < 175) & (sat < 0.62) & (R - B < 50) & ~skin_j          # the braids' darks and their lighter strands
BOB = np.zeros((H, W), bool)                                                 # the bobbles: three spheres on each braid (4x zooms)
for _cx, _cy, _r in ((334, 486, 14.5), (349, 501, 14.5), (365, 505, 12.5), (751, 423, 13.5), (740, 438, 14.5), (724, 445, 13.5)):
    BOB |= np.hypot(XX - _cx, YY - _cy) <= _r
braid_ok = (hair_l | (BOB & solid & ~skin_j)) & ~basket & ~fore & ~elbow & ~rarm & box_mask(200, 330, 860, 660)
braids = grow(head_top & hair_l, braid_ok | head_top)
head = head_top | braids
head |= dilate(head, 1.5) & solid & ~basket & ~fore & ~elbow & ~rarm & ~(skin_j & (YY > 380))   # the hair's blends into the sleeves / shoulders
head_soft = head.astype(np.float32)
head_core = head
report["head_px"] = int(head.sum()); print("head layer %d px (the jaw from x %d to %d; the braids %d px)" % (head.sum(), jx[0], jx[-1], (braids & ~head_top).sum()))

# ================= the eyes (girl_rig.py's method) =================
EYES = [{"name": "eye1", "box": (450, 246, 540, 325)}, {"name": "eye2", "box": (592, 203, 670, 282)}]
white = solid & (mn > 205)
dark = solid & (mx < 75)
eye_out = []
for E in EYES:
    x0, y0, x1, y1 = E["box"]; bm = box_mask(x0, y0, x1, y1)
    pupil = dark & bm & (mx < 45)
    bc = ((x0 + x1) / 2, (y0 + y1) / 2)
    pp = pupil & (np.hypot(XX - bc[0], YY - bc[1]) < 26)
    py, px = np.nonzero(pp); pc = (px.mean(), py.mean())
    wb = white & bm & dilate(bm & ~white & ~skin, 1.0)
    d_ = np.hypot(XX - pc[0], YY - pc[1]); cand_e = wb & (d_ > 16) & (d_ < 33)
    cp = np.column_stack(np.nonzero(cand_e))[:, ::-1].astype(np.float32)
    icx, icy, ir = fit_circle(cp)
    for _ in range(3):
        rs = np.abs(np.hypot(cp[:, 0] - icx, cp[:, 1] - icy) - ir); ok = rs < 1.5
        icx, icy, ir = fit_circle(cp[ok])
    rs = np.abs(np.hypot(cp[ok, 0] - icx, cp[ok, 1] - icy) - ir)
    wy, wx = np.nonzero(white & bm & (d_ < 44)); c = ((wx.mean() + icx) / 2, (wy.mean() + icy) / 2)
    NA = 360; r_in = np.full(NA, np.nan); r_out = np.zeros(NA)
    for kk in range(NA):
        th = 2 * math.pi * kk / NA; dx, dy = math.cos(th), math.sin(th)
        ro = None
        for t in np.arange(8, 62, 0.5):
            xx, yy = int(round(c[0] + dx * t)), int(round(c[1] + dy * t))
            if skin[yy, xx] or not solid[yy, xx]: ro = t; break
        if ro is None: ro = 61
        r_out[kk] = ro
        ri = None
        for t in np.arange(ro - 0.5, 4, -0.5):
            xx, yy = int(round(c[0] + dx * t)), int(round(c[1] + dy * t))
            if not dark[yy, xx] and not skin[yy, xx]: ri = t + 0.5; break
        if ri is not None:
            px_, py_ = c[0] + dx * ri, c[1] + dy * ri
            if np.hypot(px_ - icx, py_ - icy) > ir + 1.5: r_in[kk] = ri
    valid = ~np.isnan(r_in); idx = np.arange(NA); ang = 2 * math.pi * idx / NA
    vx, vy = c[0] + np.cos(ang[valid]) * r_in[valid], c[1] + np.sin(ang[valid]) * r_in[valid]
    M = np.column_stack([vx * vx, vx * vy, vy * vy, vx, vy]); coef, *_ = np.linalg.lstsq(M, -np.ones(len(vx)), rcond=None)
    Aq, Bq, Cq, Dq, Eq = coef
    def ell_r(th):
        dx, dy = math.cos(th), math.sin(th); x0_, y0_ = c
        qa = Aq * dx * dx + Bq * dx * dy + Cq * dy * dy
        qb = 2 * Aq * x0_ * dx + Bq * (x0_ * dy + y0_ * dx) + 2 * Cq * y0_ * dy + Dq * dx + Eq * dy
        qc = Aq * x0_ * x0_ + Bq * x0_ * y0_ + Cq * y0_ * y0_ + Dq * x0_ + Eq * y0_ + 1
        disc = qb * qb - 4 * qa * qc
        if disc < 0: return float("nan")
        ts = [(-qb + sg * math.sqrt(disc)) / (2 * qa) for sg in (1, -1)]; ts = [t for t in ts if t > 0]
        return min(ts) if ts else float("nan")
    r_ell = np.array([ell_r(th) for th in ang])
    ell_err = float(np.abs(r_ell[valid] - r_in[valid]).mean())
    r_full = np.where(valid, r_in, r_ell)
    r_full = np.minimum(r_full, r_out - 2.0)
    kern = np.ones(13) / 13; r_s = np.convolve(np.concatenate([r_full[-6:], r_full, r_full[:6]]), kern, mode="valid") - 0.6
    S = 4; bx0, by0 = x0 - 12, y0 - 12; bw, bh = (x1 - x0) + 24, (y1 - y0) + 24
    poly_pts = [((c[0] + math.cos(2 * math.pi * kk / NA) * r_s[kk]) * S, (c[1] + math.sin(2 * math.pi * kk / NA) * r_s[kk]) * S) for kk in range(NA)]
    sm = Image.new("L", (bw * S, bh * S), 0); ImageDraw.Draw(sm).polygon([(px_ - bx0 * S, py_ - by0 * S) for px_, py_ in poly_pts], fill=255)
    sm = sm.resize((bw, bh), Image.BOX)
    eye_mask = np.zeros((H, W), np.float32); eye_mask[by0:by0 + bh, bx0:bx0 + bw] = np.asarray(sm).astype(np.float32) / 255.0
    sc = np.median(rgb[white & bm & (d_ < 44)], axis=0)
    rad = int(math.ceil(ir + 3)); ox, oy = int(math.floor(icx)) - rad, int(math.floor(icy)) - rad; sz = 2 * rad + 1
    iris = np.zeros((sz, sz, 4), np.float32)
    gy, gx = np.mgrid[0:sz, 0:sz]; fx, fy = ox + gx, oy + gy
    rr = np.hypot(fx + 0.0 - icx, fy + 0.0 - icy)
    inside = rr <= ir + 2.2
    shine = white[fy, fx]
    vis = inside & (eye_mask[fy, fx] > 0.0) & solid[fy, fx]          # every pixel the interior shows at all stays as painted (the rest exact)
    cols = rgb[fy, fx]
    prof_r = np.arange(0, ir + 2, 0.5); prof = np.zeros((len(prof_r), 3))
    for i, pr in enumerate(prof_r):
        sel = vis & ~shine & (np.abs(rr - pr) <= 0.75)
        if sel.sum() < 3: sel = vis & ~shine & (np.abs(rr - pr) <= 1.5)
        prof[i] = cols[sel].mean(axis=0) if sel.sum() else (prof[i - 1] if i else sc)
    synth = np.stack([np.interp(rr, prof_r, prof[:, ch]) for ch in range(3)], axis=-1)
    iris[..., :3] = np.where(vis[..., None], cols, synth)
    iris[..., 3] = np.clip((ir + 2.2 - rr), 0, 1) * 255
    iris_im = Image.fromarray(np.clip(iris, 0, 255).astype(np.uint8), "RGBA")
    iris_im.save(OUT / f"demo3_girl_iris{E['name'][-1]}.png", optimize=True)
    save_mask(eye_mask, OUT / f"demo3_girl_{E['name']}_mask.png")
    eo = {"name": E["name"], "iris": {"cx": round(float(icx), 2), "cy": round(float(icy), 2), "r": round(float(ir), 2), "fit_pts": int(ok.sum()), "fit_rms": round(float(np.sqrt((rs ** 2).mean())), 2), "hidden_px": int((inside & ~vis).sum())},
          "iris_box": [ox, oy, sz, sz], "pupil": [round(float(pc[0]), 1), round(float(pc[1]), 1)], "centre": [round(c[0], 1), round(c[1], 1)],
          "interior_r": {"min": round(float(r_s.min()), 1), "max": round(float(r_s.max()), 1), "valid_angles": int(valid.sum()), "ellipse_fit_err": round(ell_err, 2)},
          "sclera": [int(v_) for v_ in sc], "room": {"left": round(float(r_s[180] - (ir + (c[0] - icx))), 1), "right": round(float(r_s[0] - (ir - (c[0] - icx))), 1), "down": round(float(r_s[90] - (ir - (c[1] - icy))), 1), "up": round(float(r_s[270] - (ir + (c[1] - icy))), 1)}}
    eye_out.append(eo); E["mask"] = eye_mask; E["out"] = eo; E["iris_im"] = iris_im
    print(f"{E['name']}: iris c {icx:.1f},{icy:.1f} r {ir:.1f} ({ok.sum()} pts, rms {eo['iris']['fit_rms']}), interior r {r_s.min():.1f}-{r_s.max():.1f} ({valid.sum()}/360 read, ellipse err {ell_err:.2f}), sclera {eo['sclera']}, room {eo['room']}")
report["eyes"] = eye_out

# ================= the hole, what each motion uncovers, the under-patch =================
fore_f = fore.astype(np.float32)
def shear_cover(t):
    """the forearm's footprint once sheared by t (0..1 of the lift): q is covered if fore(q.x, q.y + s(q.x)) where s = shift"""
    s = np.clip((XX[0] - X_E) / (X_W - X_E), 0, None) * LIFT * t
    out = np.zeros((H, W), bool)
    for x in range(int(X_E) - 8, int(X_W) + 14):
        sh = int(round(s[x]))
        if sh <= 0: out[:, x] = fore[:, x]; continue
        out[:-sh, x] = fore[sh:, x]
    return out
hole = basket | fore | elbow | head_core                                     # the elbow patch draws its own pixels (no double rim)
uncov = np.zeros((H, W), bool)
for t in np.linspace(0.05, 1.0, 20):
    ts = int(round(LIFT * t)); td = int(round(DIP * t))
    cov = np.zeros((H, W), bool)
    cov[:-ts, :] |= basket[ts:, :] if ts else basket[:, :]
    cov |= shear_cover(t) | elbow
    if td: cov[td:, :] |= head_core[:-td, :]
    else: cov |= head_core
    uncov |= hole & ~cov
E_ = dilate(uncov, 1.0) & hole                                              # a pixel's margin
report["uncovered_px"] = int(E_.sum()); print("uncovered: %d px" % E_.sum())
# the fill: per column, each uncovered run copied from the static picture just past it (below, else above: the first pixel not in
# the hole within 4 px) by its thickness + 1; premultiplied, so the background copies as clear
pm = np.concatenate([rgb * (alpha[..., None] / 255.0), alpha[..., None]], axis=-1)
under = np.zeros((H, W, 4), np.float32)
# the slanted edges a copy follows (dx per dy): the dress's right edge below the basket, x = 0.385 y + 416.1 (rms 0.37 px, y 802-878);
# her other arm's right edge, (730,537)-(747,590)
EDGES = [(box_mask(690, 740, 770, 820), 0.385), (box_mask(722, 528, 766, 606), 0.32)]
EDGE_SLOPE = np.zeros((H, W), np.float32)
for _z, _k in EDGES: EDGE_SLOPE[_z] = _k
orphan = np.zeros((H, W), bool)
for x in range(W):
    col = E_[:, x]
    if not col.any(): continue
    ys = np.nonzero(col)[0]
    runs = np.split(ys, np.nonzero(np.diff(ys) > 1)[0] + 1)
    for run in runs:
        y_t, y_b = run.min(), run.max()
        yb = y_b + 1
        while yb < H and hole[yb, x] and yb - y_b <= 4: yb += 1               # the first static pixel just below
        ya = y_t - 1
        while ya >= 0 and hole[ya, x] and y_t - ya <= 4: ya -= 1              # ... or just above
        if yb < H and not hole[yb, x]: sgn, T = 1, (yb - y_t) + 1
        elif ya >= 0 and not hole[ya, x]: sgn, T = -1, (y_b - ya) + 1
        else: orphan[run, x] = True; continue
        T = max(T, int(LIFT) + 1) if sgn > 0 else T                            # the lift's bands share one offset
        for y in run:
            ys_ = y + sgn * T
            xi = int(round(x + EDGE_SLOPE[y, x] * (ys_ - y)))                    # along a measured edge next to it (else straight)
            if ys_ < 0 or ys_ >= H or xi < 0 or xi >= W or hole[ys_, xi]:
                ys_, xi = (yb, x) if sgn > 0 else (ya, x)                       # fall back: the first static pixel's value
            under[y, x] = pm[ys_, xi]
# orphans (no static pixel within 4 px either way: the head's top, bits between moving parts): a harmonic fill from the static
# picture (the background as clear) and the copied fill around
if orphan.any():
    known = ~hole | (E_ & ~orphan)                                          # the background counts (clear): the head's top fades to it
    ys_o, xs_o = np.nonzero(orphan)
    y0o, y1o, x0o, x1o = max(ys_o.min() - 3, 0), min(ys_o.max() + 4, H), max(xs_o.min() - 3, 0), min(xs_o.max() + 4, W)
    src_img = np.where(E_[..., None], under, pm)[y0o:y1o, x0o:x1o].copy()
    om = orphan[y0o:y1o, x0o:x1o]; kn = known[y0o:y1o, x0o:x1o] & ~om
    src_img[om] = 0
    for _ in range(600):
        acc = np.zeros_like(src_img); cnt = np.zeros(src_img.shape[:2], np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb = np.roll(np.roll(src_img, dy, 0), dx, 1); ok = np.roll(np.roll(kn | om, dy, 0), dx, 1)
            acc += nb * ok[..., None]; cnt += ok
        src_img = np.where(om[..., None], acc / np.maximum(cnt, 1)[..., None], src_img)
    blk = under[y0o:y1o, x0o:x1o]; blk[om] = src_img[om]; under[y0o:y1o, x0o:x1o] = blk
report["orphans"] = int(orphan.sum()); print("fill: %d px copied, %d orphans filled harmonically" % (int(E_.sum() - orphan.sum()), int(orphan.sum())))
# a Poisson pass over the whole fill: the copy's gradients kept inside it, the static picture's values matched across every seam
if E_.any():
    ys_e, xs_e = np.nonzero(E_)
    y0e, y1e, x0e, x1e = max(ys_e.min() - 2, 0), min(ys_e.max() + 3, H), max(xs_e.min() - 2, 0), min(xs_e.max() + 3, W)
    g = under[y0e:y1e, x0e:x1e].copy(); f = g.copy()
    em = E_[y0e:y1e, x0e:x1e]; st = (~hole)[y0e:y1e, x0e:x1e]; stv = pm[y0e:y1e, x0e:x1e]
    nbs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    sh = lambda a, dy, dx: np.roll(np.roll(a, dy, 0), dx, 1)
    lap_g = np.zeros_like(g); cnt = np.zeros(em.shape, np.float32)
    for dy, dx in nbs:
        okE = sh(em, dy, dx); okS = sh(st, dy, dx)
        lap_g += (g - sh(g, dy, dx)) * okE[..., None]; cnt += okE | okS     # the guidance inside the fill only (none across a seam)
    for _ in range(700):
        acc = np.zeros_like(f)
        for dy, dx in nbs:
            okE = sh(em, dy, dx); okS = sh(st, dy, dx) & ~okE
            acc += sh(f, dy, dx) * okE[..., None] + sh(stv, dy, dx) * okS[..., None]
        f = np.where(em[..., None], (acc + lap_g) / np.maximum(cnt, 1)[..., None], f)
    blk = under[y0e:y1e, x0e:x1e]; blk[em] = np.clip(f[em], 0, 255); under[y0e:y1e, x0e:x1e] = blk
under_rgba = np.zeros((H, W, 4), np.float32)
ua = under[..., 3]
under_rgba[..., :3] = np.where(ua[..., None] > 0, under[..., :3] / np.maximum(ua[..., None], 1e-6) * 255.0, 0)
under_rgba[..., 3] = np.where(alpha < 250, 0, ua)                           # behind her silhouette's own anti-aliased rim: the background
Image.fromarray(np.clip(under_rgba, 0, 255).astype(np.uint8), "RGBA").save(OUT / "demo3_girl_under.png", optimize=True)

# ---------- the sheets ----------
body_mask = 1.0 - hole.astype(np.float32)
save_mask(body_mask, OUT / "demo3_girl_body_mask.png")
save_mask(fore.astype(np.float32), OUT / "demo3_girl_fore_mask.png")
save_mask(elbow.astype(np.float32), OUT / "demo3_girl_elbow_mask.png")
save_mask(basket.astype(np.float32), OUT / "demo3_girl_basket_mask.png")
save_mask(head_soft, OUT / "demo3_girl_head_mask.png")
report["shear"] = {"x_e": X_E, "x_w": X_W, "tan": round(LIFT / (X_W - X_E), 5)}
report["sheets"] = {p.name: p.stat().st_size for p in sorted(OUT.glob("*.png"))}
report["bitmap"] = [W, H]
print("sheets:", {k_: f"{v / 1024:.1f}K" for k_, v in report["sheets"].items()})

# ---------- the composite (rest and peak), as CSS would draw it ----------
def over(dst, src_pm):
    """premultiplied src over premultiplied dst"""
    return src_pm + dst * (1 - src_pm[..., 3:4] / 255.0)
def lay(mask):
    return pm * mask[..., None]
def sample(img, mapx, mapy):
    """bilinear sample of an HxWx4 image at float coords (map from the output pixel to the source)"""
    x0 = np.floor(mapx).astype(int); y0 = np.floor(mapy).astype(int); fx = (mapx - x0)[..., None]; fy = (mapy - y0)[..., None]
    def g(yi, xi):
        ok = (xi >= 0) & (xi < W) & (yi >= 0) & (yi < H)
        out = np.zeros(mapx.shape + (4,), np.float32)
        out[ok] = img[yi[ok], xi[ok]]; return out
    return (g(y0, x0) * (1 - fx) * (1 - fy) + g(y0, x0 + 1) * fx * (1 - fy) + g(y0 + 1, x0) * (1 - fx) * fy + g(y0 + 1, x0 + 1) * fx * fy)
def composite(t_lift, t_dip, gaze):
    """t_lift / t_dip 0..1; gaze = [(gx, gy) per eye] in bitmap px"""
    out = np.zeros((H, W, 4), np.float32)
    up = np.concatenate([under_rgba[..., :3] * under_rgba[..., 3:4] / 255.0, under_rgba[..., 3:4]], axis=-1)
    out = over(out, up)
    out = over(out, lay(body_mask))
    s = np.clip((XX - X_E) / (X_W - X_E), 0, None) * LIFT * t_lift         # skewY: q <- (x, y + s(x))
    out = over(out, sample(lay(fore_f), XX, YY + s))
    out = over(out, lay(elbow.astype(np.float32)))
    # the head group: the head window + the eyes (each: window, sclera disc, iris moved by the gaze), then moved down by the dip
    grp = lay(head_soft)
    for E, (gx_, gy_) in zip(EYES, gaze):
        eo = E["out"]; eg = pm.copy()
        disc = (np.hypot(XX - eo["iris"]["cx"], YY - eo["iris"]["cy"]) <= eo["iris"]["r"] + 1).astype(np.float32)
        sc_ = np.zeros((H, W, 4), np.float32); sc_[..., :3] = eo["sclera"]; sc_[..., 3] = 255
        eg = over(eg, sc_ * disc[..., None])
        ir_ = np.asarray(E["iris_im"]).astype(np.float32); ox, oy, sz, _ = eo["iris_box"]
        il = np.zeros((H, W, 4), np.float32); il[oy:oy + sz, ox:ox + sz] = ir_
        il = np.concatenate([il[..., :3] * il[..., 3:4] / 255.0, il[..., 3:4]], axis=-1)
        eg = over(eg, sample(il, XX - gx_, YY - gy_))
        grp = over(grp, eg * E["mask"][..., None])
    out = over(out, sample(grp, XX, YY - DIP * t_dip))
    out = over(out, sample(lay(basket.astype(np.float32)), XX, YY + LIFT * t_lift))   # over the head group: the braid tip goes behind the handle
    return out
def unpm(c):
    a = c[..., 3:4]; return np.concatenate([np.where(a > 0, c[..., :3] / np.maximum(a, 1e-6) * 255.0, 0), a], axis=-1)
rest = unpm(composite(0, 0, [(0, 0), (0, 0)]))
diff = np.abs(rest[..., :3] - rgb).max(axis=2) * (alpha > 8) + np.abs(rest[..., 3] - alpha)
print("rest composite vs the painting: max diff %.1f levels, %d px over 8, %d px over 24" % (diff.max(), (diff > 8).sum(), (diff > 24).sum()))
if (diff > 8).any():
    yy_, xx_ = np.nonzero(diff > 8); print("  the off pixels' box:", xx_.min(), yy_.min(), xx_.max(), yy_.max(), "e.g.", list(zip(xx_[:6], yy_[:6])))
report["rest_diff"] = {"max": round(float(diff.max()), 1), "over8": int((diff > 8).sum()), "over24": int((diff > 24).sum())}
(OUT / "rig.json").write_text(json.dumps(report, indent=1), encoding="utf-8")

if DEBUG:
    def to_img(c, bg=(120, 200, 120)):
        u = unpm(c) if c is not None else None
        b = Image.new("RGBA", (W, H), bg + (255,)); b.alpha_composite(Image.fromarray(np.clip(u, 0, 255).astype(np.uint8), "RGBA")); return b.convert("RGB")
    peak = composite(1, 1, [(3, 6), (3, 6)])
    for name, c in (("rest", composite(0, 0, [(0, 0), (0, 0)])), ("peak", peak), ("half", composite(.5, .5, [(1.5, 3), (1.5, 3)]))):
        img = to_img(c); img.save(DEBUG / f"t4_{name}_full.png")
        img.crop((300, 180, 840, 860)).resize((1080, 1360), Image.LANCZOS).save(DEBUG / f"t4_{name}_2x.png")
        img.resize((224, 336), Image.LANCZOS).resize((672, 1008), Image.NEAREST).save(DEBUG / f"t4_{name}_page3x.png")
    # the masks as overlays
    base = to_img(pm).convert("RGBA")
    for m, col in ((hole & ~E_, (255, 0, 0, 90)), (E_, (255, 255, 0, 200)), (fore, (0, 0, 255, 90)), (elbow, (0, 255, 255, 140)), (basket, (255, 0, 255, 60))):
        o = np.zeros((H, W, 4), np.uint8); o[m] = col; base = Image.alpha_composite(base, Image.fromarray(o, "RGBA"))
    d = ImageDraw.Draw(base)
    d.line([(float(x_), float(y_)) for x_, y_ in zip(jx, jy_s + 2.0)], fill=(255, 255, 255, 255), width=1); d.line(SEP, fill=(0, 0, 0, 255), width=1)
    base.convert("RGB").crop((300, 180, 840, 860)).resize((1080, 1360), Image.NEAREST).save(DEBUG / "t4_masks_2x.png")
    Image.fromarray(np.clip(under_rgba, 0, 255).astype(np.uint8), "RGBA").crop((300, 480, 840, 860)).resize((1080, 760), Image.NEAREST).save(DEBUG / "t4_under_2x.png")
    dm = Image.fromarray(np.clip(diff * 4, 0, 255).astype(np.uint8), "L")
    dv = Image.merge("RGB", [dm, Image.new("L", (W, H), 0), Image.new("L", (W, H), 0)])
    Image.blend(to_img(pm), dv, 0.6).crop((300, 180, 840, 860)).resize((1080, 1360), Image.NEAREST).save(DEBUG / "t4_restdiff_2x.png")
    def region(box, name, k=4):
        b2 = to_img(pm).convert("RGBA")
        for m, col in ((rarm, (0, 255, 255, 150)), (basket, (255, 0, 255, 90)), (E_, (255, 0, 0, 150)), (head_core, (255, 255, 0, 70)), (fore, (0, 0, 255, 90))):
            o = np.zeros((H, W, 4), np.uint8); o[m] = col; b2 = Image.alpha_composite(b2, Image.fromarray(o, "RGBA"))
        b2.convert("RGB").crop(box).resize(((box[2] - box[0]) * k, (box[3] - box[1]) * k), Image.NEAREST).save(DEBUG / name)
    region((660, 490, 800, 620), "r_topright.png"); region((240, 320, 840, 640), "r_head.png", 2)
    print("debug in", DEBUG)
