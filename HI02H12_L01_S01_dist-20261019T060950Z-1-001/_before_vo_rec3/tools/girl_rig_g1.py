"""girl_rig_g1.py — [g1-ball] (2026-11-02) the G1 girl's ball-bounce rig, cut from her own bitmap
(g1_assets/img_g1_girl_ball2.webp, the frame 715:856's "image 273", 1024x1536, drawn 252x378).

The page shows her as LAYERS and the ball leaves her hands, thumps the floor and comes back (see build.py [g1-ball]):
  under   what the ball hid, PAINTED (demo: the user chose it): her bodice's side, her waist and the skirt's top with its edge,
          her far arm (the viewer's right) from the stub under the sleeve to the wrist — a shaded, outlined tube in her other
          arm's colours —, its cupped hand joining the real knuckles at the ball's right rim and the thumb tip at its top (own RGBA)
  body    the bitmap with a HOLE where the ball and the hands in front of it are
  ball    the ball as its own image: its hidden parts (under the near hand, the knuckles, the thumb) completed — the rim by its own
          ring at the same radius, the inside by a harmonic fill —, its outer anti-aliased rim recoloured to the ring with its
          coverage as alpha (no dress / background fringe as it falls)
  hands   the near hand and the far hand's knuckles / thumb tip, in FRONT of the ball, their own image: where they bordered the ball
          their rim is recoloured to the outline with its coverage (no ball colour on them in the air)
  eyes    girl_rig.py's (interior windows, sclera discs, completed irises): they follow the ball
Writes g1_assets/girl_rig/ (the sheets, rig.json) and, with --debug <dir>, previews (the ball away, at the floor).
Run: python -I -X utf8 girl_rig_g1.py [--debug <dir>]
"""
import sys, json, pathlib, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SCR = pathlib.Path(__file__).resolve().parent
SRC = SCR / "g1_assets" / "img_g1_girl_ball2.webp"
OUT = SCR / "g1_assets" / "girl_rig"; OUT.mkdir(exist_ok=True)
DEBUG = pathlib.Path(sys.argv[sys.argv.index("--debug") + 1]) if "--debug" in sys.argv else None
if DEBUG: DEBUG.mkdir(parents=True, exist_ok=True)

im = Image.open(SRC).convert("RGBA"); W, H = im.size
assert (W, H) == (1024, 1536), (W, H)
A = np.asarray(im).astype(np.float32); rgb = A[..., :3]; alpha = A[..., 3]
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
mx = rgb.max(axis=2); mn = rgb.min(axis=2)
hue = np.where(mx == R, 60 * (G - B) / np.maximum(mx - mn, 1), 0); sat = (mx - mn) / np.maximum(mx, 1)
solid = alpha > 0; opaque = alpha >= 250
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
report = {"bitmap": [W, H]}

def box_mask(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[int(y0):int(y1), int(x0):int(x1)] = True; return m
def dilate(m, r):
    k = int(math.ceil(r)); out = m.copy()
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            if dx * dx + dy * dy > r * r + 1e-6 or (dx == 0 and dy == 0): continue
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out
def grow(seed, allowed, iters=4000):
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
def save_rgba(arr, path, box=None):
    a = np.clip(arr, 0, 255).astype(np.uint8).copy(); a[a[..., 3] == 0, :3] = 0
    img = Image.fromarray(a, "RGBA")
    if box: img = img.crop(box)
    img.save(path, optimize=True)
def fit_circle(pts):
    x, y = pts[:, 0], pts[:, 1]
    M = np.column_stack([x, y, np.ones_like(x)]); b = -(x * x + y * y)
    (D, E, F), *_ = np.linalg.lstsq(M, b, rcond=None)
    cx, cy = -D / 2, -E / 2; return cx, cy, math.sqrt(cx * cx + cy * cy - F)
def harmonic(img, unknown, known, iters=800):
    """fill the unknown pixels of img (HxWxC) from the known ones (Jacobi; neither = no flux) on their bounding box"""
    if not unknown.any(): return img
    ys, xs = np.nonzero(unknown); y0, y1, x0, x1 = max(ys.min() - 2, 0), min(ys.max() + 3, H), max(xs.min() - 2, 0), min(xs.max() + 3, W)
    f = img[y0:y1, x0:x1].copy(); um = unknown[y0:y1, x0:x1]; km = known[y0:y1, x0:x1] & ~um
    sh = lambda a, dy, dx: np.roll(np.roll(a, dy, 0), dx, 1)
    f[um] = 0
    for _ in range(iters):
        acc = np.zeros_like(f); cnt = np.zeros(um.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ok = sh(km | um, dy, dx); acc += sh(f, dy, dx) * ok[..., None]; cnt += ok
        f = np.where(um[..., None], acc / np.maximum(cnt, 1)[..., None], f)
    out = img.copy(); out[y0:y1, x0:x1][um] = f[um]; return out

def fill(img, unknown, known, smooth=300):
    """fill the unknown pixels from the known ones: peel inward (each ring the mean of its known neighbours), then a harmonic
    smoothing of the filled pixels (the plain Jacobi from zero needs ~ (width)^2 sweeps and left the middle dark)"""
    if not unknown.any(): return img
    ys, xs = np.nonzero(unknown); y0, y1, x0, x1 = max(ys.min() - 2, 0), min(ys.max() + 3, H), max(xs.min() - 2, 0), min(xs.max() + 3, W)
    f = img[y0:y1, x0:x1].copy(); um = unknown[y0:y1, x0:x1].copy(); km = known[y0:y1, x0:x1] & ~um; todo = um.copy(); have = km.copy()
    sh = lambda a, dy, dx: np.roll(np.roll(a, dy, 0), dx, 1)
    nb8 = [(dy, dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dy or dx]
    for _ in range(600):
        if not todo.any(): break
        acc = np.zeros_like(f); cnt = np.zeros(um.shape, np.float32)
        for dy, dx in nb8:
            ok = sh(have, dy, dx); acc += sh(f, dy, dx) * ok[..., None]; cnt += ok
        new = todo & (cnt > 0)
        f[new] = acc[new] / cnt[new][..., None]; have |= new; todo &= ~new
    for _ in range(smooth):
        acc = np.zeros_like(f); cnt = np.zeros(um.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ok = sh(km | um, dy, dx); acc += sh(f, dy, dx) * ok[..., None]; cnt += ok
        f = np.where(um[..., None], acc / np.maximum(cnt, 1)[..., None], f)
    out = img.copy(); blk = out[y0:y1, x0:x1]; blk[um] = f[um]; out[y0:y1, x0:x1] = blk; return out
def catmull(pts_, n=24, closed=False):
    """a Catmull-Rom spline through the points (closed or open), n samples per span"""
    P = np.array(pts_, np.float64)
    if closed: P = np.vstack([P[-1], P, P[0], P[1]])
    else: P = np.vstack([P[0] * 2 - P[1], P, P[-1] * 2 - P[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed: out.append(P[-2])
    return np.array(out)

# ================= the ball =================
pts = []
c0 = (790.0, 700.0)
for ang in np.arange(-100, 100, 1.0):                                       # its silhouette against the background (the right half)
    th = math.radians(ang); dx, dy = math.cos(th), math.sin(th); prev = None
    for t in np.arange(120, 200, 0.25):
        x, y = c0[0] + dx * t, c0[1] + dy * t; v = alpha[int(round(y)), int(round(x))]
        if prev is not None and prev >= 128 > v: pts.append((x, y)); break
        prev = v
pts = np.array(pts); cx, cy, r = fit_circle(pts)
for _ in range(3):
    ok = np.abs(np.hypot(pts[:, 0] - cx, pts[:, 1] - cy) - r) < 1.5; cx, cy, r = fit_circle(pts[ok])
rho = np.hypot(XX - cx, YY - cy); theta = np.arctan2(YY - cy, XX - cx)
RIM_OUT = 5.5                                                               # the ring's blur reaches r + 5 over the skirt (measured: r+4 a blend, r+5 still 20 levels dark)
disc = rho <= r + RIM_OUT                                                   # the footprint with ALL of it (r + 1.6 / 3.5 left a dark arc on the skirt)
report["ball"] = {"cx": round(cx, 2), "cy": round(cy, 2), "r": round(r, 2), "fit_pts": int(ok.sum())}
print("ball: c %.2f, %.2f r %.2f (%d silhouette points)" % (cx, cy, r, ok.sum()))
# the floor: the standing foot's sole (the lowest solid pixel under her, x 440-700)
foot = solid & box_mask(440, 1300, 700, H)
FLOOR = float(np.nonzero(foot.any(axis=1))[0].max()) - 2.0
report["floor_y"] = FLOOR; print("floor (the standing sole) y %.0f: the ball drops %.1f px" % (FLOOR, FLOOR - (cy + r)))

# ================= the hands in front of the ball =================
skin = solid & (R > 195) & (B > 70) & (sat > 0.30) & (sat < 0.66) & (hue > 14) & (hue < 34)
outline = solid & (mx < 190) & (R - B > 35) & (R >= G)                    # the hands' brown strokes
NEAR = box_mask(598, 640, 740, 805)                                         # the near hand (the viewer's left) over the ball
near = grow(box_mask(640, 690, 660, 705), skin & NEAR)
FAR = box_mask(930, 640, 972, 752) | box_mask(890, 574, 922, 604)           # the far hand's knuckles at the right rim, its thumb tip at the top
far = skin & FAR                                                             # every knuckle bump and the thumb tip (one seed flooded one bump: they are divided by outlines)
hand_core = near | far
hand = hand_core | (dilate(hand_core, 4.5) & outline & (NEAR | FAR))      # with their outlines
hand |= dilate(hand, 2.5) & solid & NEAR & ~skin & disc & ((mx < 235) | (np.abs(R - G) < 40))   # the near hand's outlines' outer blends over the ball, all of their blur (the far hand's ring-side pixels stay the ball's)
hand |= dilate(hand, 1.5) & solid & (NEAR | FAR) & ~opaque                # and their anti-aliasing against the background
hand &= (XX >= 600)                                                         # the near forearm stays with the body (the ball never reaches x < 632)
report["hands_px"] = int(hand.sum()); print("hands in front: %d px" % hand.sum())

# ================= the ball image: completed, its rim recoloured =================
ring_out = r - 0.6                                                          # its dark ring's outer edge (the silhouette at alpha 128 = r)
ball_vis = disc & ~hand & opaque & (rho <= r - 1.0)
# TWO ball images, crossfaded as the ball leaves / returns to her hands: the REST image = the painting (the near hand's contact
# shadow on the ball, the residuals that make the hand's recoloured rim exact), shown only while she holds it; the CLEAN image =
# that shadow halo (8 px round the near hand) refilled too, the rim ring-coloured, shown in the air — one image cannot be both
HALO = dilate(hand & NEAR, 8.0) & ~hand & (rho <= r - 12)
_c = rgb / 255.0; _mx = _c.max(-1); _mn = _c.min(-1); _d = np.maximum(_mx - _mn, 1e-6)
_h = np.where(_mx == _c[..., 0], ((_c[..., 1] - _c[..., 2]) / _d) % 6, np.where(_mx == _c[..., 1], (_c[..., 2] - _c[..., 0]) / _d + 2, (_c[..., 0] - _c[..., 1]) / _d + 4)) * 60
_s = (_mx - _mn) / np.maximum(_mx, 1e-6)
PANELS = {"cap": (_s < 0.18) & (_mn > 0.70), "pink": (_s >= 0.18) & ((_h >= 290) | (_h < 8)), "orange": (_s >= 0.18) & (_h >= 8) & (_h < 36),
          "yellow": (_s >= 0.18) & (_h >= 36) & (_h < 78), "green": (_s >= 0.18) & (_h >= 78) & (_h < 175), "blue": (_s >= 0.18) & (_h >= 175) & (_h < 290)}
capm = PANELS["cap"] & ball_vis & (np.hypot(XX - 867, YY - 598) < 40)
POLE = (float(XX[capm].mean()), float(YY[capm].mean())); report["ball_pole"] = [round(POLE[0], 1), round(POLE[1], 1)]
def complete(vis):
    """the ball with every pixel outside vis completed: the rim band by its own ring at the same radius (the nearest visible angles
    either side), the inside panel by panel (the panels radiate from the white cap: a hidden pixel takes the panel of the visible
    ball on the line from the cap through it, and is filled from that panel's pixels only)"""
    hid = (rho <= r - 1.0) & ~vis; out = rgb.copy()
    band_ = hid & (rho >= r - 12)
    for yb, xb in zip(*np.nonzero(band_)):
        rr_ = rho[yb, xb]; th0 = theta[yb, xb]; got = []
        for sgn in (1, -1):
            for k in range(1, 240):
                th = th0 + sgn * k * (math.pi / 720); xi, yi = int(round(cx + rr_ * math.cos(th))), int(round(cy + rr_ * math.sin(th)))
                if vis[yi, xi]: got.append((k, rgb[yi, xi])); break
        if got: out[yb, xb] = sum(c / k for k, c in got) / sum(1.0 / k for k, _ in got)
    inn = hid & ~band_
    lab = np.full((H, W), -1, np.int8)
    for i_, m_ in enumerate(PANELS.values()): lab[m_ & vis & (rho <= r - 8)] = i_
    ys_i, xs_i = np.nonzero(inn); lab_h = np.full(len(ys_i), -1, np.int16)
    for k_, (yh, xh) in enumerate(zip(ys_i, xs_i)):
        vx, vy = xh - POLE[0], yh - POLE[1]; L = math.hypot(vx, vy); ux, uy = vx / L, vy / L
        for t in range(1, 160):
            for sg in (1, -1):
                xx, yy = int(round(xh + sg * ux * t)), int(round(yh + sg * uy * t))
                if 0 <= xx < W and 0 <= yy < H and lab[yy, xx] >= 0: lab_h[k_] = lab[yy, xx]; break
            if lab_h[k_] >= 0: break
    lab_hid = np.full((H, W), -1, np.int16); lab_hid[ys_i, xs_i] = lab_h
    for i_ in range(len(PANELS)):
        um_ = inn & (lab_hid == i_)
        if um_.any(): out = fill(out, um_, vis & (lab == i_), smooth=300)
    lft = inn & (lab_hid < 0)
    if lft.any(): out = fill(out, lft, vis | band_ | (inn & (lab_hid >= 0)), smooth=100)
    kk = np.zeros_like(out)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1): kk += np.roll(np.roll(out, dy, 0), dx, 1)
    out = np.where(inn[..., None], kk / 9.0, out)                            # the panels' joins softened (the painting's are soft)
    return out, {nm: int((lab_hid == i_).sum()) for i_, nm in enumerate(PANELS)}
pmv, _st_rest = complete(ball_vis)                                          # the rest image: only what the hand covers
pmc, _st_clean = complete(ball_vis & ~HALO)                                 # the clean image: the hand's shadow refilled too
report["panels_hidden"] = {"rest": _st_rest, "clean": _st_clean}
ball_rgba = np.zeros((H, W, 4), np.float32)
ball_rgba[..., :3] = pmv; ball_rgba[..., 3] = np.where(rho <= r - 1.0, 255, 0)
ball_clean = np.zeros((H, W, 4), np.float32)
ball_clean[..., :3] = pmc; ball_clean[..., 3] = np.where(rho <= r - 1.0, 255, 0)
rim = ((rho > r - 1.0) | ~opaque) & (rho <= r + RIM_OUT) & ~hand            # (solved after the patch, below); every not-opaque pixel is rim
ball_rgba[(rho > r + RIM_OUT)] = 0; ball_clean[(rho > r + RIM_OUT)] = 0

# the hands' rim over the ball: their outline colour, the coverage against the completed ball behind
hand_rgba = np.zeros((H, W, 4), np.float32); hand_rgba[..., :3] = rgb; hand_rgba[..., 3] = np.where(hand, alpha, 0)
o_col = np.median(rgb[outline & dilate(hand_core, 4.5) & (NEAR | FAR) & (mx < 150)], axis=0)
edge = hand & ~hand_core & ~dilate(hand_core, 1.0) & disc & opaque & NEAR & ~(outline & (mx < 150)) & (rho <= r - 1.0)   # the near hand's blends between a stroke and the ball (on the ball's own rim they stay as painted)
bb = pmv
cv = np.clip(((rgb - bb) * (o_col - bb)).sum(-1) / np.maximum(((o_col - bb) ** 2).sum(-1), 1), 0, 1)
hand_rgba[edge, :3] = o_col; hand_rgba[edge, 3] = cv[edge] * 255
report["hand_outline"] = [int(v) for v in o_col]

# ================= the hole =================
hole = disc | hand
body_mask = 1.0 - hole.astype(np.float32)

# ================= the painted patch behind the ball =================
S4 = 4
def sc(pts_): return [(x * S4, y * S4) for x, y in pts_]
def bez(p0, p1, p2, p3, n=60):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3) * np.array(p0) + 3 * ((1 - t) ** 2) * t * np.array(p1) + 3 * (1 - t) * t * t * np.array(p2) + t ** 3 * np.array(p3)
def aa_poly(pts_):
    """a polygon's coverage (0..1), drawn 4x and downsampled"""
    big = Image.new("L", (W * S4, H * S4), 0); ImageDraw.Draw(big).polygon(sc(pts_), fill=255)
    return np.asarray(big.resize((W, H), Image.BOX)).astype(np.float32) / 255.0
under = np.zeros((H, W, 4), np.float32)                                     # straight RGB + alpha
def paint(cov_, col, a_=1.0):
    """col (HxWx3 or 3) over the patch with coverage cov_ * a_"""
    k = np.clip(cov_ * a_, 0, 1)[..., None]
    c = np.broadcast_to(np.asarray(col, np.float32), (H, W, 3)) if np.ndim(col) == 1 else col
    out_a = k[..., 0] * 255 + under[..., 3] * (1 - k[..., 0])
    under[..., :3] = np.where(out_a[..., None] > 0, (c * k * 255 + under[..., :3] * under[..., 3:4] * (1 - k)) / np.maximum(out_a[..., None], 1e-6), 0)
    under[..., 3] = out_a

# ---- 1. the torso's side and the skirt behind the ball: their silhouette, their colours from the dress around ----
dress_pink = solid & (R > 100) & (hue < -14) & (sat > 0.25)
WAIST = (684.0, 640.0); ARMPIT = (668.0, 598.0); SKIRT_OUT = (733.0, 850.0)
edge_curve = bez(WAIST, (690.0, 700.0), (708.0, 790.0), SKIRT_OUT)          # the skirt's side flaring to where it shows below the ball
below = [(733.0, 850.0), (800.0, 935.0)]                                     # (and on: the visible edge, slope 0.82)
torso_poly = [(560.0, 540.0), (650.0, 540.0), ARMPIT, WAIST] + [tuple(p) for p in edge_curve[1:]] + below + [(560.0, 935.0)]
torso = aa_poly(torso_poly)
_light = solid & (mn > 165) & (B > 150); _blend = solid & (R > 215) & (G - B < 25) & (mn > 60)
dress_known = (dress_pink | ((_light | _blend) & dilate(dress_pink, 3.0))) & opaque & ~hole & box_mask(560, 500, 820, 1000) & ~skin   # the dress around: its pinks and its white work, nothing else
D_ = (torso > 0.01) & hole
guide = np.zeros((H, W, 3), np.float32)
for y in range(H):                                                          # the bodice / waistband rows (y < 650): from the left
    if y >= 650: break
    xs = np.nonzero(D_[y])[0]
    if not len(xs): continue
    T = xs.max() - xs.min() + 2
    for x in xs:
        xs_ = x - T
        guide[y, x] = rgb[y, xs_] if xs_ >= 0 and dress_known[y, xs_] else 0
for x in range(W):                                                          # the skirt's pleats (y >= 650): from below
    col = np.nonzero(D_[:, x] & (YY[:, 0] >= 650))[0]
    if not len(col): continue
    yb = col.max() + 1
    while yb < H and hole[yb, x]: yb += 1
    T = yb - col.min() + 1
    for y in col:
        ys_ = y + T
        guide[y, x] = rgb[ys_, x] if ys_ < H and dress_known[ys_, x] else 0
gmiss = D_ & (guide.sum(-1) == 0)
guide = fill(np.where(D_[..., None], guide, rgb), gmiss, dress_known | (D_ & ~gmiss), smooth=60)
# Poisson: the guide's gradients inside, the static dress's values across every seam
ys_e, xs_e = np.nonzero(D_); y0e, y1e, x0e, x1e = ys_e.min() - 2, ys_e.max() + 3, xs_e.min() - 2, xs_e.max() + 3
g = guide[y0e:y1e, x0e:x1e]; fpo = fill(np.where(D_[..., None], 0, rgb), D_, dress_known, smooth=0)[y0e:y1e, x0e:x1e].copy()
em = D_[y0e:y1e, x0e:x1e]; st = dress_known[y0e:y1e, x0e:x1e]; stv = rgb[y0e:y1e, x0e:x1e]
shf = lambda a, dy, dx: np.roll(np.roll(a, dy, 0), dx, 1)
lap = np.zeros_like(g); cntp = np.zeros(em.shape, np.float32)
for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    okE = shf(em, dy, dx); okS = shf(st, dy, dx) & ~okE
    lap += (g - shf(g, dy, dx)) * okE[..., None]; cntp += okE | okS
for _ in range(900):
    acc = np.zeros_like(fpo)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        okE = shf(em, dy, dx); okS = shf(st, dy, dx) & ~okE
        acc += shf(fpo, dy, dx) * okE[..., None] + shf(stv, dy, dx) * okS[..., None]
    fpo = np.where(em[..., None], (acc + lap) / np.maximum(cntp, 1)[..., None], fpo)
dfill_t = rgb.copy(); blk = dfill_t[y0e:y1e, x0e:x1e]; blk[em] = np.clip(fpo[em], 0, 255); dfill_t[y0e:y1e, x0e:x1e] = blk
paint(torso, dfill_t)
# the skirt edge's own darker outline (sampled where it shows below the ball)
eo_col = np.median(rgb[box_mask(735, 860, 800, 930) & dress_pink & (mx < 200)], axis=0)
def stroke(curve, w, col, a_=1.0):
    big = Image.new("L", (W * S4, H * S4), 0); ImageDraw.Draw(big).line(sc([tuple(p) for p in curve]), fill=255, width=int(w * S4), joint="curve")
    paint(np.asarray(big.resize((W, H), Image.BOX)).astype(np.float32) / 255.0, col, a_)
stroke(np.vstack([edge_curve, np.array(below)]), 3.5, eo_col)

# ---- 2. the far arm: a tube from the stub under the sleeve to the wrist, her other arm's colours ----
arm_sk = skin & box_mask(380, 520, 470, 660) & opaque                       # her other (near) upper arm
lit = np.percentile(rgb[arm_sk], 80, axis=0); shade = np.percentile(rgb[arm_sk], 12, axis=0)
a_out = np.median(rgb[outline & box_mask(330, 520, 480, 680) & (mx < 150)], axis=0)
report["arm_colours"] = {"lit": [int(v) for v in lit], "shade": [int(v) for v in shade], "outline": [int(v) for v in a_out]}
# the stub's edges where it meets the ball (measured on the 4x zoom: its left edge x ~665 at y 595, its right edge (736, 550))
# the stub (measured row by row): its right outline the line (713,520)-(736,550) — the direction (0.61, 0.79) —, its left edge
# under the sleeve's ruffle reaching x 666 at y 585: 77 px across, the axis through (682.7, 543.4)
cl = catmull([(658.3, 511.8), (682.7, 543.4), (722.0, 594.5), (760.0, 642.0), (800.0, 676.0), (850.0, 698.0), (892.0, 706.0)], n=20)
seg_len = np.r_[0, np.cumsum(np.hypot(np.diff(cl[:, 0]), np.diff(cl[:, 1])))]; L_ = seg_len[-1]
_s_stub = seg_len[np.argmin(np.hypot(cl[:, 0] - 682.7, cl[:, 1] - 543.4))] / L_
half_w = np.interp(seg_len / L_, [0, _s_stub, 0.42, 0.62, 1.0], [38.5, 38.5, 32.0, 28.0, 23.5])   # 77 px at the stub, ~62 at the elbow, 47 at the wrist
bx0, by0, bx1, by1 = 630, 480, 940, 780
sub_y, sub_x = np.mgrid[by0:by1, bx0:bx1].astype(np.float32)
best_d = np.full(sub_x.shape, 1e9, np.float32); best_s = np.zeros(sub_x.shape, np.float32); best_sg = np.zeros(sub_x.shape, np.float32)
for i in range(len(cl) - 1):
    p, q = cl[i], cl[i + 1]; v = q - p; ll = float(np.hypot(*v)); u_ = v / ll
    tx = np.clip(((sub_x - p[0]) * u_[0] + (sub_y - p[1]) * u_[1]) / ll, 0, 1)
    px_, py_ = p[0] + tx * v[0], p[1] + tx * v[1]
    dd = np.hypot(sub_x - px_, sub_y - py_)
    sg = np.sign((sub_x - p[0]) * u_[1] - (sub_y - p[1]) * u_[0])           # + = the arm's lower / outer side
    upd = dd < best_d; best_d = np.where(upd, dd, best_d); best_s = np.where(upd, (seg_len[i] + tx * ll) / L_, best_s); best_sg = np.where(upd, sg, best_sg)
hw = np.interp(best_s, seg_len / L_, half_w)
uu = best_d / hw * best_sg                                                    # -1 .. 1 across the arm
cover = np.clip(hw - best_d + 0.5, 0, 1)
shade_k = np.clip(0.30 + 0.55 * np.clip(uu, -1, 1) + 0.25 * uu * uu, 0, 1)   # lit on its upper side, shaded below and at the edges
arm_col = lit[None, None, :] * (1 - shade_k[..., None]) + shade[None, None, :] * shade_k[..., None]
olw = 3.6                                                                    # its outline's width (her strokes: 3.5-4 px)
oline = np.clip(best_d - (hw - olw) + 0.5, 0, 1) * cover
full_cov = np.zeros((H, W), np.float32); full_col = np.zeros((H, W, 3), np.float32)
full_cov[by0:by1, bx0:bx1] = cover; full_col[by0:by1, bx0:bx1] = arm_col * (1 - oline[..., None]) + a_out[None, None, :] * oline[..., None]
# the painted arm's skin matched to the real stub across the seam under the sleeve (it is in the sleeve's shade there)
stub_known = skin & opaque & ~hole & box_mask(650, 500, 760, 610)
oline_full = np.zeros((H, W), np.float32); oline_full[by0:by1, bx0:bx1] = oline
E_arm = (full_cov > 0.99) & hole & (oline_full < 0.02)
ys_a, xs_a = np.nonzero(E_arm); y0a, y1a, x0a, x1a = ys_a.min() - 2, ys_a.max() + 3, xs_a.min() - 2, xs_a.max() + 3
ga = full_col[y0a:y1a, x0a:x1a]; fa = ga.copy(); ema = E_arm[y0a:y1a, x0a:x1a]; sta = stub_known[y0a:y1a, x0a:x1a]; sva = rgb[y0a:y1a, x0a:x1a]
shf = lambda a, dy, dx: np.roll(np.roll(a, dy, 0), dx, 1)
lapa = np.zeros_like(ga); cnta = np.zeros(ema.shape, np.float32)
for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    okE = shf(ema, dy, dx); okS = shf(sta, dy, dx) & ~okE
    lapa += (ga - shf(ga, dy, dx)) * okE[..., None]; cnta += okE | okS
for _ in range(900):
    acc = np.zeros_like(fa)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        okE = shf(ema, dy, dx); okS = shf(sta, dy, dx) & ~okE
        acc += shf(fa, dy, dx) * okE[..., None] + shf(sva, dy, dx) * okS[..., None]
    fa = np.where(ema[..., None], (acc + lapa) / np.maximum(cnta, 1)[..., None], fa)
blk = full_col[y0a:y1a, x0a:x1a]; blk[ema] = np.clip(fa[ema], 0, 255); full_col[y0a:y1a, x0a:x1a] = blk
paint(full_cov, full_col)

# ---- 3. the far hand: a cupped palm from the wrist to the knuckles (the real ones in front), the thumb up to its real tip ----
# a hand gripping the ball's side from BEHIND, the ball gone: a "C" — the palm on the right (the knuckles, real, in front of it),
# the thumb curling from the palm's top up-left to its real tip at the ball's top-right rim, the wrist entering the palm's lower left
PALM = catmull([(899.0, 700.0), (904.0, 666.0), (913.0, 643.0), (926.0, 631.0), (936.0, 634.0), (942.0, 650.0), (946.0, 698.0), (943.0, 738.0),
                (931.0, 751.0), (913.0, 750.0), (900.0, 732.0)], n=16, closed=True)   # inside the ball but under the real knuckles (x 940-963, y 652-740)
palm_cov = aa_poly([tuple(p) for p in PALM])
pc = np.array([930.0, 690.0])
dpal = np.hypot(XX - pc[0], (YY - pc[1]) * 0.75) / 52.0
palm_col = lit[None, None, :] * (1 - np.clip(dpal, 0, 1)[..., None] * 0.7) + shade[None, None, :] * (np.clip(dpal, 0, 1)[..., None] * 0.7)
paint(palm_cov, palm_col)
stroke(np.vstack([PALM, PALM[:1]]), 3.4, a_out)
# the thumb: a short tapered tube (its own outline), from the palm's top to the real tip (897-914, 582-598)
TH = catmull([(937.0, 654.0), (931.0, 628.0), (921.0, 606.0), (911.0, 594.0), (905.5, 590.0)], n=14)   # its root well inside the palm (its end cap there, painted over)
tl = np.r_[0, np.cumsum(np.hypot(np.diff(TH[:, 0]), np.diff(TH[:, 1])))]; thw = np.interp(tl / tl[-1], [0, 1], [10.0, 8.5])                          # ~20 px at its root, the real tip's 17 at its end
tb = (880, 570, 960, 650); ty, tx = np.mgrid[tb[1]:tb[3], tb[0]:tb[2]].astype(np.float32)
bd = np.full(tx.shape, 1e9, np.float32); bw_ = np.zeros(tx.shape, np.float32)
for i in range(len(TH) - 1):
    p_, q_ = TH[i], TH[i + 1]; v = q_ - p_; ll = float(np.hypot(*v)); u_ = v / ll
    t_ = np.clip(((tx - p_[0]) * u_[0] + (ty - p_[1]) * u_[1]) / ll, 0, 1)
    dd = np.hypot(tx - (p_[0] + t_ * v[0]), ty - (p_[1] + t_ * v[1])); upd = dd < bd
    bd = np.where(upd, dd, bd); bw_ = np.where(upd, thw[i] + (thw[i + 1] - thw[i]) * t_, bw_)
tcov = np.clip(bw_ - bd + 0.5, 0, 1); tol = np.clip(bd - (bw_ - 3.4) + 0.5, 0, 1) * tcov
th_cov = np.zeros((H, W), np.float32); th_col = np.zeros((H, W, 3), np.float32)
th_cov[tb[1]:tb[3], tb[0]:tb[2]] = tcov
th_col[tb[1]:tb[3], tb[0]:tb[2]] = palm_col[tb[1]:tb[3], tb[0]:tb[2]] * (1 - tol[..., None]) + a_out[None, None, :] * tol[..., None]
paint(th_cov, th_col)
# the joint: the thumb's root and the palm are one piece of skin — their two outlines across it painted over by the root's inside
_tin = np.zeros((H, W), np.float32)
_root = np.zeros(tx.shape, bool)
for i in range(len(TH) - 1):
    if tl[i] / tl[-1] > 0.40: break
    p_, q_ = TH[i], TH[i + 1]; v = q_ - p_; ll = float(np.hypot(*v)); u_ = v / ll
    t_ = np.clip(((tx - p_[0]) * u_[0] + (ty - p_[1]) * u_[1]) / ll, 0, 1)
    _root |= np.hypot(tx - (p_[0] + t_ * v[0]), ty - (p_[1] + t_ * v[1])) < (thw[i] - 3.6)
_tin[tb[1]:tb[3], tb[0]:tb[2]] = _root
paint(_tin * (palm_cov > 0.5), palm_col)
# the fingers' creases running back from the knuckles into the palm
for yk in (674.0, 697.0, 719.0):
    stroke(np.array([(941.0, yk), (932.0, yk + 1.5), (924.0, yk + 4.0)]), 2.0, shade * 0.8 + a_out * 0.2, 0.75)
under_full = under.copy()                                                    # (the far-hand overlay, shown only in the air, takes it unclipped)
under[~hole] = 0                                                             # only what the ball can uncover

# ---- the rims, solved so that at rest the layers give the painting back ----
# the ball's outer rim: against the background the bitmap's own pixels (the ring with its alpha: clean in the air); against what is
# opaque behind it at rest (the patch: the dress, the arm), its coverage by projection between the patch and the ring's local
# colour (r - 2.5 on the same ray), its colour the rest of the blend — ball over patch = the painting, and in the air a ring-tinted
# edge instead of a dress-tinted one
covered_rest = ((rho <= r - 1.0) & opaque & ~hand) | (hand & (alpha >= 250)) | (rim & opaque)
under[~covered_rest] = 0
q = under[..., :3]; qa = under[..., 3] / 255.0
ring_loc = np.zeros((H, W, 3), np.float32)
for yb, xb in zip(*np.nonzero(rim)):
    th = theta[yb, xb]; ring_loc[yb, xb] = pmv[int(round(cy + (r - 2.5) * math.sin(th))), int(round(cx + (r - 2.5) * math.cos(th)))]
a_ = np.clip(((rgb - q) * (ring_loc - q)).sum(-1) / np.maximum(((ring_loc - q) ** 2).sum(-1), 1), 0, 1)
op_r = rim & opaque & (qa > 0.99)
# the REST image: exact — the coverage floored so the colour stays in gamut, the colour the rest of the blend
a_min = np.max(np.where(rgb > q, (rgb - q) / np.maximum(255 - q, 1e-3), (q - rgb) / np.maximum(q, 1e-3)), axis=-1)
a_r = np.clip(np.maximum(a_, a_min), 0, 1)
c_r = np.clip((rgb - (1 - a_r[..., None]) * q) / np.maximum(a_r[..., None], 1e-3), 0, 255)
ball_rgba[rim, :3] = rgb[rim]; ball_rgba[rim, 3] = alpha[rim]
ball_rgba[op_r, :3] = c_r[op_r]; ball_rgba[op_r, 3] = a_r[op_r] * 255
# the CLEAN image: a crisp anti-aliased circle at the silhouette's radius (r: alpha 128 against the background) in the ring's own
# local colour — the painting's edge blurs into the dress and the sleeve behind it (its tints, carried, read as wisps)
ball_clean[rim, :3] = ring_loc[rim]; ball_clean[rim, 3] = np.clip(r + 0.5 - rho[rim], 0, 1) * 255
# the near hand's rim (its outline colour, the coverage against the ball): the hidden ball pixel under it takes the residual
nb = edge & (rho <= r - 1.0) & (cv < 0.98)
bfix = np.clip((rgb - cv[..., None] * o_col) / np.maximum(1 - cv[..., None], 1e-3), 0, 255)
ball_rgba[nb, :3] = bfix[nb]
ball_rgba[hand & ~opaque & disc, 3] = 0                                      # under a hand pixel the painting shows through (the knuckles' edge): nothing behind it
ball_clean[hand & ~opaque & disc, 3] = 0
_ext = dilate(hole, 3.0) & ~hole & (alpha >= 250)
under[_ext, :3] = rgb[_ext]; under[_ext, 3] = 255
UB2 = (int(cx - r - 10), int(cy - r - 10), int(cx + r + 12), int(cy + r + 12))   # the patch's box with the overlap
report["under_px"] = int((under[..., 3] > 0).sum())
# 2. the far hand in the air: the painted palm and thumb with the real knuckles / thumb tip over them, their ball-side outline taken
# out (it cut the tip off the painted thumb: a dark "antenna"); faded in with the clean ball (none of it at rest)
FARZ = box_mask(886, 572, 970, 758)
seam = hand & FAR & (mx < 200) & dilate((rho < r - 1.5) & ~hand, 4.0)
fh = np.zeros((H, W, 4), np.float32)
fh[FARZ] = under_full[FARZ]                                                  # the painted palm and the WHOLE thumb (it runs along the rim, past the silhouette)
kn = hand & FAR & ~seam
_a = hand_rgba[..., 3:4] / 255.0
fh[..., :3] = np.where(kn[..., None], hand_rgba[..., :3] * _a + fh[..., :3] * (fh[..., 3:4] / 255.0) * (1 - _a), fh[..., :3] * (fh[..., 3:4] / 255.0))
fh[..., 3] = np.where(kn, hand_rgba[..., 3] + fh[..., 3] * (1 - _a[..., 0]), fh[..., 3])
fh[..., :3] = np.where(fh[..., 3:4] > 0, fh[..., :3] / np.maximum(fh[..., 3:4] / 255.0, 1e-6), 0)
fh[~FARZ] = 0
report["far_seam_px"] = int(seam.sum())

# ================= the eyes (girl_rig.py's method) =================
white = solid & (mn > 205); dark = solid & (mx < 75)
EYES = [{"name": "eye1", "box": (424, 254, 516, 334)}, {"name": "eye2", "box": (570, 202, 650, 284)}]
eye_out = []
for E in EYES:
    x0, y0, x1, y1 = E["box"]; bm = box_mask(x0, y0, x1, y1)
    pupil = dark & bm & (mx < 45); bc = ((x0 + x1) / 2, (y0 + y1) / 2)
    pp = pupil & (np.hypot(XX - bc[0], YY - bc[1]) < 26); py, px = np.nonzero(pp); pc_ = (px.mean(), py.mean())
    wb = white & bm & dilate(bm & ~white & ~skin, 1.0)
    d_ = np.hypot(XX - pc_[0], YY - pc_[1]); cand_e = wb & (d_ > 15) & (d_ < 32)
    cp = np.column_stack(np.nonzero(cand_e))[:, ::-1].astype(np.float32)
    icx, icy, ir = fit_circle(cp)
    for _ in range(3):
        rs = np.abs(np.hypot(cp[:, 0] - icx, cp[:, 1] - icy) - ir); okc = rs < 1.5; icx, icy, ir = fit_circle(cp[okc])
    rs = np.abs(np.hypot(cp[okc, 0] - icx, cp[okc, 1] - icy) - ir)
    wy, wx = np.nonzero(white & bm & (d_ < 44)); c = ((wx.mean() + icx) / 2, (wy.mean() + icy) / 2)
    NA = 360; r_in = np.full(NA, np.nan); r_out = np.zeros(NA)
    for kk in range(NA):
        th = 2 * math.pi * kk / NA; dx, dy = math.cos(th), math.sin(th); ro = None
        for t in np.arange(8, 62, 0.5):
            xx, yy = int(round(c[0] + dx * t)), int(round(c[1] + dy * t))
            if skin[yy, xx] or not solid[yy, xx]: ro = t; break
        if ro is None: ro = 61
        r_out[kk] = ro; ri = None
        for t in np.arange(ro - 0.5, 4, -0.5):
            xx, yy = int(round(c[0] + dx * t)), int(round(c[1] + dy * t))
            if not dark[yy, xx] and not skin[yy, xx]: ri = t + 0.5; break
        if ri is not None and np.hypot(c[0] + dx * ri - icx, c[1] + dy * ri - icy) > ir + 1.5: r_in[kk] = ri
    valid = ~np.isnan(r_in); ang = 2 * math.pi * np.arange(NA) / NA
    vx, vy = c[0] + np.cos(ang[valid]) * r_in[valid], c[1] + np.sin(ang[valid]) * r_in[valid]
    M = np.column_stack([vx * vx, vx * vy, vy * vy, vx, vy]); coef, *_ = np.linalg.lstsq(M, -np.ones(len(vx)), rcond=None)
    Aq, Bq, Cq, Dq, Eq = coef
    def ell_r(th):
        dx, dy = math.cos(th), math.sin(th); x0_, y0_ = c
        qa = Aq * dx * dx + Bq * dx * dy + Cq * dy * dy
        qb = 2 * Aq * x0_ * dx + Bq * (x0_ * dy + y0_ * dx) + 2 * Cq * y0_ * dy + Dq * dx + Eq * dy
        qc = Aq * x0_ * x0_ + Bq * x0_ * y0_ + Cq * y0_ * y0_ + Dq * x0_ + Eq * y0_ + 1
        disc_ = qb * qb - 4 * qa * qc
        if disc_ < 0: return float("nan")
        ts = [(-qb + sg * math.sqrt(disc_)) / (2 * qa) for sg in (1, -1)]; ts = [t for t in ts if t > 0]
        return min(ts) if ts else float("nan")
    r_ell = np.array([ell_r(th) for th in ang]); ell_err = float(np.abs(r_ell[valid] - r_in[valid]).mean())
    r_full = np.minimum(np.where(valid, r_in, r_ell), r_out - 2.0)
    r_s = np.convolve(np.concatenate([r_full[-6:], r_full, r_full[:6]]), np.ones(13) / 13, mode="valid") - 0.6
    S = 4; bx0e, by0e = x0 - 12, y0 - 12; bw, bh = (x1 - x0) + 24, (y1 - y0) + 24
    poly_pts = [((c[0] + math.cos(2 * math.pi * kk / NA) * r_s[kk]) * S, (c[1] + math.sin(2 * math.pi * kk / NA) * r_s[kk]) * S) for kk in range(NA)]
    sm = Image.new("L", (bw * S, bh * S), 0); ImageDraw.Draw(sm).polygon([(px_ - bx0e * S, py_ - by0e * S) for px_, py_ in poly_pts], fill=255)
    sm = sm.resize((bw, bh), Image.BOX)
    eye_mask = np.zeros((H, W), np.float32); eye_mask[by0e:by0e + bh, bx0e:bx0e + bw] = np.asarray(sm).astype(np.float32) / 255.0
    scl = np.median(rgb[white & bm & (d_ < 44)], axis=0)
    rad = int(math.ceil(ir + 3)); ox, oy = int(math.floor(icx)) - rad, int(math.floor(icy)) - rad; sz = 2 * rad + 1
    iris = np.zeros((sz, sz, 4), np.float32)
    gy, gx = np.mgrid[0:sz, 0:sz]; fx, fy = ox + gx, oy + gy
    rr = np.hypot(fx + 0.0 - icx, fy + 0.0 - icy); inside = rr <= ir + 2.2; shine = white[fy, fx]
    vis = inside & (eye_mask[fy, fx] > 0.0) & solid[fy, fx]
    cols = rgb[fy, fx]; prof_r = np.arange(0, ir + 2, 0.5); prof = np.zeros((len(prof_r), 3))
    for i, pr in enumerate(prof_r):
        sel = vis & ~shine & (np.abs(rr - pr) <= 0.75)
        if sel.sum() < 3: sel = vis & ~shine & (np.abs(rr - pr) <= 1.5)
        prof[i] = cols[sel].mean(axis=0) if sel.sum() else (prof[i - 1] if i else scl)
    synth = np.stack([np.interp(rr, prof_r, prof[:, ch]) for ch in range(3)], axis=-1)
    iris[..., :3] = np.where(vis[..., None], cols, synth); iris[..., 3] = np.clip((ir + 2.2 - rr), 0, 1) * 255
    iris_im = Image.fromarray(np.clip(iris, 0, 255).astype(np.uint8), "RGBA"); iris_im.save(OUT / f"g1_girl_iris{E['name'][-1]}.png", optimize=True)
    save_mask(eye_mask, OUT / f"g1_girl_{E['name']}_mask.png")
    eo = {"name": E["name"], "iris": {"cx": round(float(icx), 2), "cy": round(float(icy), 2), "r": round(float(ir), 2), "fit_pts": int(okc.sum()), "fit_rms": round(float(np.sqrt((rs ** 2).mean())), 2)},
          "iris_box": [ox, oy, sz, sz], "sclera": [int(v_) for v_ in scl],
          "room": {"left": round(float(r_s[180] - (ir + (c[0] - icx))), 1), "right": round(float(r_s[0] - (ir - (c[0] - icx))), 1), "down": round(float(r_s[90] - (ir - (c[1] - icy))), 1), "up": round(float(r_s[270] - (ir + (c[1] - icy))), 1)}}
    eye_out.append(eo); E["mask"] = eye_mask; E["out"] = eo; E["iris_im"] = iris_im
    print(f"{E['name']}: iris c {icx:.1f},{icy:.1f} r {ir:.1f} ({okc.sum()} pts, rms {eo['iris']['fit_rms']}), interior {valid.sum()}/360 read (ellipse err {ell_err:.2f}), room {eo['room']}")
report["eyes"] = eye_out

# ---------- the sheets ----------
BB = (int(cx - r - 4), int(cy - r - 4), int(cx + r + 6), int(cy + r + 6))   # the ball image's own box (bitmap px)
report["ball_box"] = list(BB)
def save_webp(arr, path, box, lossless=True):
    a = np.clip(arr, 0, 255).astype(np.uint8).copy(); a[a[..., 3] == 0, :3] = 0
    Image.fromarray(a, "RGBA").crop(box).save(path, "WEBP", lossless=lossless, quality=100 if lossless else 92, method=6, exact=True)
for _old in ("g1_girl_ball.png",):
    if (OUT / _old).exists(): (OUT / _old).unlink()
save_webp(ball_rgba, OUT / "g1_girl_ball_rest.webp", BB)
save_webp(ball_clean, OUT / "g1_girl_ball.webp", BB)
HB = (598, 570, 975, 806); report["hands_box"] = list(HB)
save_rgba(hand_rgba, OUT / "g1_girl_hands.png", HB)
UB = UB2; report["under_box"] = list(UB)
save_rgba(under, OUT / "g1_girl_under.png", UB)
FB = (886, 572, 970, 758); report["farhand_box"] = list(FB)
save_rgba(fh, OUT / "g1_girl_farhand.png", FB)
save_mask(body_mask, OUT / "g1_girl_body_mask.png")
report["sheets"] = {p.name: p.stat().st_size for p in sorted(list(OUT.glob("*.png")) + list(OUT.glob("*.webp")))}
(OUT / "rig.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
print("sheets:", {k_: f"{v / 1024:.1f}K" for k_, v in report["sheets"].items()})

# ---------- the composite (rest, and the ball away) ----------
def to_pm(a_): return np.concatenate([a_[..., :3] * a_[..., 3:4] / 255.0, a_[..., 3:4]], axis=-1)
pm = to_pm(A)
def over(dst, src): return src + dst * (1 - src[..., 3:4] / 255.0)
def shift(img, dy):
    out = np.zeros_like(img); d = int(round(dy))
    if d >= 0: out[d:] = img[:H - d]
    else: out[:d] = img[-d:]
    return out
def composite(ball_dy, gaze=((0, 0), (0, 0)), held=None):
    held = (ball_dy == 0) if held is None else held                          # the rest image while she holds it, the clean one in the air
    out = to_pm(under)
    out = over(out, pm * body_mask[..., None])
    for E, (gx_, gy_) in zip(EYES, gaze):
        eo = E["out"]; eg = pm.copy()
        disc_e = (np.hypot(XX - eo["iris"]["cx"], YY - eo["iris"]["cy"]) <= eo["iris"]["r"] + 1).astype(np.float32)
        scl_ = np.zeros((H, W, 4), np.float32); scl_[..., :3] = eo["sclera"]; scl_[..., 3] = 255; eg = over(eg, scl_ * disc_e[..., None])
        il = np.zeros((H, W, 4), np.float32); ox, oy, sz, _ = eo["iris_box"]; il[oy:oy + sz, ox:ox + sz] = np.asarray(E["iris_im"]).astype(np.float32)
        il = np.roll(np.roll(to_pm(il), int(round(gy_)), 0), int(round(gx_)), 1); eg = over(eg, il)
        out = over(out * (1 - 0), eg * E["mask"][..., None] + out * 0)  # (the eye group over the body, masked)
    out = over(out, shift(to_pm(ball_rgba if held else ball_clean), ball_dy))
    out = over(out, to_pm(hand_rgba))
    if not held: out = over(out, to_pm(fh))
    return out
def unpm(c_):
    a_ = c_[..., 3:4]; return np.concatenate([np.where(a_ > 0, c_[..., :3] / np.maximum(a_, 1e-6) * 255.0, 0), a_], axis=-1)
rest = unpm(composite(0))
diff = np.abs(rest[..., :3] - rgb).max(axis=2) * (alpha > 8) + np.abs(rest[..., 3] - alpha)
print("rest composite vs the painting: max diff %.1f levels, %d px over 8, %d px over 24" % (diff.max(), (diff > 8).sum(), (diff > 24).sum()))
if (diff > 24).any():
    ys_, xs_ = np.nonzero(diff > 24); print("  the off pixels' box:", xs_.min(), ys_.min(), xs_.max(), ys_.max())
report["rest_diff"] = {"max": round(float(diff.max()), 1), "over8": int((diff > 8).sum()), "over24": int((diff > 24).sum())}
(OUT / "rig.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
if DEBUG:
    def to_img(c_, bg=(205, 215, 225)):
        u = unpm(c_); b = Image.new("RGBA", (W, H), bg + (255,)); b.alpha_composite(Image.fromarray(np.clip(u, 0, 255).astype(np.uint8), "RGBA")); return b.convert("RGB")
    for name, dy in (("rest", 0), ("away", FLOOR - (cy + r)), ("half", (FLOOR - (cy + r)) * 0.4)):
        img = to_img(composite(dy)); img.save(DEBUG / f"g1_{name}_full.png")
        img.crop((540, 440, 1000, 900)).resize((920, 920), Image.LANCZOS).save(DEBUG / f"g1_{name}_2x.png")
    to_img(composite(FLOOR - (cy + r))).resize((252, 378), Image.LANCZOS).resize((504, 756), Image.NEAREST).save(DEBUG / "g1_away_page2x.png")
    print("debug in", DEBUG)
