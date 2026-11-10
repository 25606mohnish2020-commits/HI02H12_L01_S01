"""girl_rig_t2.py — [girl-wave] (2026-11-02) the T2 girl's wave rig, cut from her own bitmap (demo1_assets/img_demo1_girl_walk.webp,
the frame 706:188's walking girl, 1024x1536, drawn 239x358).

She holds both bag straps with closed fists, so her wave is her RIGHT forearm (the viewer's left) turning up about the elbow with
the fist dissolving into an open palm on the way up — and back. The page shows her as LAYERS (see build.py [girl-wave] and the
PUNCT_SCENE module), bottom to top:
  patch  what lies BEHIND the forearm and the fist, repainted (demo1_girl_patch.png, RGBA, opaque over the body's hole only): the
         pink strap carried from its visible end above the fist to its visible end below the forearm (a cubic curve; its colour
         cross-section sampled from the visible strap, widths interpolated), the pinafore's navy as a plane fitted to the navy
         around the hole, the upper arm's hidden inner edge (skin + outline), the sleeve's corner
  body   the bitmap with a HOLE where the forearm and the fist are (beyond the elbow's keep disc: demo1_girl_body_mask.png)
  eyes   per eye, the bitmap clipped to the eye's interior (demo1_girl_eye{1,2}_mask.png), a sclera disc over the painted iris and
         the iris itself completed (demo1_girl_iris{1,2}.png), which slides to the eye's centre: she looks at the screen
  arm    the forearm + fist from the elbow's cut line (demo1_girl_arm_mask.png), turning about the elbow (as girl_rig.py's)
  palm   the same forearm with an OPEN hand in place of the fist (demo1_girl_palm.png, RGBA): the T3 girl's open palm
         (demo2_assets/img_demo2_girl_ask.webp — the same style and skin), mirrored (her right hand: the thumb to the viewer's
         right once the fingers point up), cut across the palm at its narrowest, scaled to the forearm's width, its fingers along
         the forearm, its outline shifted to this bitmap's maroon; faded in as the arm lifts, out as it lands
Writes demo1_assets/girl_rig/ (the sheets, rig.json with the geometry in bitmap px) and, with --debug, overlays into the folder
given. All sheets are full 1024x1536 (the masks white with the mask in ALPHA — Chrome masks by a raster's alpha), applied at the
girl's box size by CSS. Run: python -X utf8 -I girl_rig_t2.py [--debug <dir>]
"""
import sys, json, pathlib, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SCR = pathlib.Path(__file__).resolve().parent
SRC = SCR / "demo1_assets" / "img_demo1_girl_walk.webp"
SRC3 = SCR / "demo2_assets" / "img_demo2_girl_ask.webp"
OUT = SCR / "demo1_assets" / "girl_rig"; OUT.mkdir(exist_ok=True)
DEBUG = pathlib.Path(sys.argv[sys.argv.index("--debug") + 1]) if "--debug" in sys.argv else None
if DEBUG: DEBUG.mkdir(parents=True, exist_ok=True)

im = Image.open(SRC).convert("RGBA"); W, H = im.size
assert (W, H) == (1024, 1536), (W, H)
A = np.asarray(im).astype(np.float32); rgb = A[..., :3]; alpha = A[..., 3]
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
mx = rgb.max(axis=2); mn = rgb.min(axis=2)
solid = alpha > 128
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def box_mask(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[y0:y1, x0:x1] = True; return m
def dilate(m, r):
    k = int(math.ceil(r)); out = np.zeros_like(m)
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            if dx * dx + dy * dy > r * r + 1e-6: continue
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out
def erode(m, r): return ~dilate(~m, r)
def soft(m, px):
    f = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(px / 2.0))
    return np.asarray(f).astype(np.float32) / 255.0
def save_mask(m, path):
    a = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8), "L"); w = Image.new("L", a.size, 255)
    Image.merge("RGBA", [w, w, w, a]).save(path, optimize=True)
def save_rgba(arr, path):
    arr = arr.copy(); arr[arr[..., 3] < 0.5, :3] = 0                        # nothing under the transparent pixels (they compress away)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA").save(path, optimize=True)
def poly_mask(pts):
    pm = Image.new("L", (W, H), 0); ImageDraw.Draw(pm).polygon(pts, fill=255); return np.asarray(pm) > 0
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
def bilinear(img, x, y):
    """img (H,W,C) float sampled at float coords (arrays)"""
    x0 = np.floor(x).astype(int); y0 = np.floor(y).astype(int); fx = x - x0; fy = y - y0
    x0 = np.clip(x0, 0, W - 2); y0 = np.clip(y0, 0, H - 2)
    c00 = img[y0, x0]; c10 = img[y0, x0 + 1]; c01 = img[y0 + 1, x0]; c11 = img[y0 + 1, x0 + 1]
    return (c00 * (1 - fx)[..., None] * (1 - fy)[..., None] + c10 * fx[..., None] * (1 - fy)[..., None]
            + c01 * (1 - fx)[..., None] * fy[..., None] + c11 * fx[..., None] * fy[..., None])

# ---------- colour classes ----------
skin = solid & (R > 185) & (G > 120) & (B > 80) & (R - B > 45) & (G < 215) & (G - B > 20)   # (G - B: the strap's light pink 255,121,159 is not skin)
dark = solid & (R < 130) & (G < 95) & (B < 85) & (R > B)                 # the outlines (maroon 78,24,39), the pupils
pink = solid & (R > 200) & (G < 150) & (B > 120) & (B < 200)              # the bag's straps
navy = solid & (B > R + 20) & (B < 140) & (R < 70)                        # the pinafore
white = solid & (mn > 205)
report = {"bitmap": [W, H]}

# ================= the arm: her right forearm + fist (the viewer's left), beyond the elbow =================
P = np.array([416.0, 650.0]); R_KEEP = 35.0; CUT = 8.0; WRIST = 76.0
u = np.array([140.0, -60.0]); u /= np.linalg.norm(u)                       # along the forearm toward the fist (up-right)
n = np.array([-u[1], u[0]])                                                # across it (down-right)
POLY = [(393, 592), (430, 575), (470, 556), (478, 540), (562, 540), (562, 672), (520, 695), (441, 708)]
poly = poly_mask(POLY)
# the arm = the fist's / forearm's skin grown over its own outline (3.5 px) but never into the strap, the shirt or the pinafore,
# kept to the piece connected to the skin (no specks of the strap's edge lines)
seed = skin & poly; seed = erode(dilate(seed, 2.5), 2.5)                   # the creases filled
grow = dilate(seed, 3.5) & poly & ~pink & ~white & ~navy
arm_bool = seed.copy()
for _ in range(8):
    nxt = dilate(arm_bool, 1.0) & grow
    if (nxt == arm_bool).all(): break
    arm_bool = nxt
arm_bool = erode(dilate(arm_bool, 2.0), 2.0)
# the upper arm's lower end (no outline parts it from the forearm at the inner elbow) and the sleeve's corner stay with the body:
# left of the upper arm's hidden inner edge and above the forearm's upper edge nothing turns
arm_bool &= ~((XX < 442) & (YY < 626))
side = (XX - P[0]) * u[0] + (YY - P[1]) * u[1]                             # along u from the pivot
across = (XX - P[0]) * n[0] + (YY - P[1]) * n[1]
dist_p = np.hypot(XX - P[0], YY - P[1])
cut_soft = np.clip((side - CUT) / 6.0 + 0.5, 0, 1)
rim = dilate(arm_bool, 1.0) & ~arm_bool & ~((XX < 444) & (YY < 628))      # the anti-aliased rim: blends of the outline with what is behind (none along the layer's cut at the upper arm)
arm_full = arm_bool | rim
keep_disc = np.clip((R_KEEP + 0.75 - dist_p) / 1.5, 0, 1)
hole = arm_full.astype(np.float32) * (side > CUT + 3) * (1 - keep_disc)   # the body's hole: the whole arm, outline and rim included, a hard edge (the patch beneath meets the painting there)
hole[side < CUT + 2] = 0
hole[(XX < 444) & (YY < 628)] = 0                                         # the layer's cut at the upper arm (x 442) is not a painted edge: no hole along it, the body shows there
body_mask = 1 - hole
# the silhouette check of the keep circle: inside the arm (the skin + outline) everywhere
ring = (np.abs(dist_p - R_KEEP) < 0.7)
outside_arm = ring & ~(skin | dark | arm_bool)
oy_, ox_ = np.nonzero(outside_arm)
print("arm %d px (+ %d rim), the body's hole %d px; the keep circle (R %.0f about %s) crosses %d non-arm px%s" % (arm_bool.sum(), rim.sum(), (hole > 0.5).sum(), R_KEEP, P.tolist(), outside_arm.sum(),
      (" in x %d-%d y %d-%d" % (ox_.min(), ox_.max(), oy_.min(), oy_.max())) if len(ox_) else ""))
# the forearm's width across u near the wrist (for the hand's scale)
w2_rows = []
for s_ in np.arange(WRIST - 14, WRIST - 4, 1.0):
    sel = arm_bool & (np.abs(side - s_) < 0.5)
    if sel.sum(): t_ = across[sel]; w2_rows.append(t_.max() - t_.min() + 1)
w2 = float(np.median(w2_rows)); print("the forearm's width near the wrist: %.1f px" % w2)
# the fingertips' reach from the pivot (the fist's, for the record)
hp = np.column_stack(np.nonzero(arm_bool & (side > 40)))[:, ::-1]
reach_fist = float(np.hypot(hp[:, 0] - P[0], hp[:, 1] - P[1]).max())
report["elbow"] = {"pivot": P.round(2).tolist(), "R_keep": R_KEEP, "u": u.round(4).tolist(), "n": n.round(4).tolist(), "cut_px": CUT, "wrist_px": WRIST, "forearm_w": round(w2, 1), "reach_fist": round(reach_fist, 1)}
report["arm"] = {"poly": POLY, "arm_px": int(arm_bool.sum()), "rim_px": int(rim.sum()), "hole_px": int((hole > 0.5).sum())}

# ================= the patch: what lies behind the forearm and the fist =================
patch_region = soft(dilate(hole > 0.5, 3.0), 1.5)
# 1. the strap: its centre curve from above the fist to below the forearm
def strap_run(y):
    """the strap's pink run on row y within x 440-540 — the LONGEST contiguous run (a stray pink pixel must not stretch it): (x0, x1) or None"""
    row = pink[y, 440:540]; best = None; st = None
    for i in range(len(row) + 1):
        on = i < len(row) and row[i]
        if on and st is None: st = i
        if not on and st is not None:
            if best is None or i - st > best[1] - best[0]: best = (st, i - 1)
            st = None
    if best is None or best[1] - best[0] < 10: return None
    return 440 + best[0], 440 + best[1]
top_rows = [(y,) + strap_run(y) for y in range(500, 537) if strap_run(y)]   # clear of the fist's thumb (from y ~538), which clips the run's left side
top_c = np.array([((r[1] + r[2]) / 2.0, r[0]) for r in top_rows]); top_w = np.median([r[2] - r[1] + 1 for r in top_rows])
print("strap runs above the fist (y: x0-x1):", " ".join(f"{r[0]}:{r[1]}-{r[2]}" for r in top_rows[::4]))
(ta, tb) = np.polyfit(top_c[:, 1], top_c[:, 0], 1)                         # x = ta*y + tb above the fist
T0 = np.array([ta * 554 + tb, 554.0]); tT = np.array([ta, 1.0]); tT /= np.linalg.norm(tT)
low_rows = [(y,) + strap_run(y) for y in range(680, 706) if strap_run(y)]   # clear of the forearm's lower outline
low_c = np.array([((r[1] + r[2]) / 2.0, r[0]) for r in low_rows])
(la, lb) = np.polyfit(low_c[:, 1], low_c[:, 0], 1)                         # x = la*y + lb below the arm
B0 = np.array([la * 670 + lb, 670.0]); tB = np.array([la, 1.0]); tB /= np.linalg.norm(tB)
low_w_row = np.median([r[2] - r[1] + 1 for r in low_rows]); low_w = low_w_row * abs(tB[1])   # the run across the rows, perpendicular
print("strap above the fist: x = %.3f y + %.1f, %.0f px wide; below the arm: x = %.3f y + %.1f, %.0f px across the rows = %.1f px perpendicular" % (ta, tb, top_w, la, lb, low_w_row, low_w))
HL = 26.0                                                                  # short handles: the strap hangs nearly straight behind the fist and bends toward the bag only under the forearm
C0, C1, C2, C3 = T0, T0 + HL * tT, B0 - HL * tB, B0
print("strap curve: %s -> %s (handles %s, %s)" % (C0.round(1).tolist(), C3.round(1).tolist(), C1.round(1).tolist(), C2.round(1).tolist()))
ts = np.linspace(0, 1, 400)[:, None]
curve = (1 - ts) ** 3 * C0 + 3 * (1 - ts) ** 2 * ts * C1 + 3 * (1 - ts) * ts ** 2 * C2 + ts ** 3 * C3
dcur = 3 * (1 - ts) ** 2 * (C1 - C0) + 6 * (1 - ts) * ts * (C2 - C1) + 3 * ts ** 2 * (C3 - C2)
dcur /= np.linalg.norm(dcur, axis=1, keepdims=True); ncur = np.column_stack([dcur[:, 1], -dcur[:, 0]])   # the normal to the RIGHT of travel (down): (-dy... ) -> keep a consistent side
# the colour cross-section, sampled on the visible ends along their normals (d = offset along the normal, -26..26)
D = np.arange(-26, 27, 1.0)
def profile(centre_line, direction, y_from, y_to):
    nrm = np.array([direction[1], -direction[0]])
    cols = []
    for yv in np.arange(y_from, y_to, 1.0):
        c = np.array([centre_line(yv), yv])
        xs_ = c[0] + D * nrm[0]; ys_ = c[1] + D * nrm[1]
        cols.append(bilinear(rgb, xs_, ys_))
    return np.median(np.array(cols), axis=0)
prof_top = profile(lambda yv: ta * yv + tb, tT, 518, 546)
prof_low = profile(lambda yv: la * yv + lb, tB, 682, 704)
# the strap's half-width (incl. its dark edges): where the top profile stops being strap-like, from the centre outward
def half_width(prof):
    def strap_like(c): return (c[0] > 150 and c[1] < 140 and c[2] > 90) or (c.max() < 150 and c[0] >= c[2])
    r = 0
    for i in range(len(D) // 2, len(D)):
        if not strap_like(prof[i]): break
        r = D[i]
    l = 0
    for i in range(len(D) // 2, -1, -1):
        if not strap_like(prof[i]): break
        l = -D[i]
    return (l + r) / 2.0
hw_top, hw_low = half_width(prof_top), half_width(prof_low)
print("strap half-widths: above %.1f, below %.1f (profile samples)" % (hw_top, hw_low))
# 2. the pinafore's navy: the navy around the hole (the bodice side, right of the upper arm) blended smoothly into it — a
#    normalised Gaussian average (sigma 22 px) of the surrounding navy, so the fill meets its surroundings without a seam
ring_m = dilate(hole > 0.5, 60) & ~dilate(hole > 0.5, 2) & navy & (XX > 440)
ys_, xs_ = np.nonzero(ring_m)
wsum = Image.fromarray((ring_m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(22)); wsum = np.asarray(wsum).astype(np.float32) / 255
navy_fill = np.zeros((H, W, 3), np.float32)
for ch in range(3):
    chan = Image.fromarray((rgb[..., ch] * ring_m).astype(np.uint8)).filter(ImageFilter.GaussianBlur(22))
    navy_fill[..., ch] = np.asarray(chan).astype(np.float32) / np.maximum(wsum, 1e-3)
#    then relaxed to a harmonic fill inside the patch (Jacobi sweeps on the patch's box, the surrounding navy held): it meets the
#    pinafore's own shading at the hole's edge exactly, no tonal step
pb = np.nonzero(patch_region > 0.001); y0p, y1p, x0p, x1p = pb[0].min() - 2, pb[0].max() + 3, pb[1].min() - 2, pb[1].max() + 3
free = (patch_region > 0.001)[y0p:y1p, x0p:x1p]
held = navy[y0p:y1p, x0p:x1p] & ~free                                      # the real navy around (the strap, the skin, the sleeve are not navy: not held, not free either)
fill = navy_fill[y0p:y1p, x0p:x1p].copy(); src = rgb[y0p:y1p, x0p:x1p]
fill[held] = src[held]
upd = free | (~held & ~free)                                               # the non-navy neighbours (strap, arm) relax too: they only carry the navy across
for it in range(1500):
    nb = (np.roll(fill, 1, 0) + np.roll(fill, -1, 0) + np.roll(fill, 1, 1) + np.roll(fill, -1, 1)) / 4.0
    fill = np.where(upd[..., None], nb, fill)
navy_fill[y0p:y1p, x0p:x1p] = fill
navy_plane = navy_fill
resid = rgb[ys_, xs_] - navy_fill[ys_, xs_]; print("navy fill: %d ring px (rms %.1f about the Gaussian seed), harmonic inside the patch's %dx%d box" % (len(xs_), np.sqrt((resid ** 2).mean()), x1p - x0p, y1p - y0p))
coef = np.zeros((3, 3))
skin_col = np.median(rgb[skin & box_mask(380, 620, 440, 690)], axis=0); outline_col = np.median(rgb[dark & box_mask(430, 620, 520, 700)], axis=0)
print("skin", skin_col.round(0).tolist(), "outline", outline_col.round(0).tolist())
# 3. compose the patch
patch = np.zeros((H, W, 4), np.float32)
pr = patch_region > 0.001
py_, px_ = np.nonzero(pr); pts = np.column_stack([px_, py_]).astype(np.float32)
col = navy_plane[py_, px_].copy()
# the upper arm's hidden inner edge: skin left of x_edge(y), its 3 px outline just left of the edge
x_edge = 441.0 - (pts[:, 1] - 618.0) * 0.05
in_arm = (pts[:, 0] < x_edge) & (pts[:, 1] >= 610)
col[in_arm] = skin_col
in_outline = in_arm & (pts[:, 0] > x_edge - 3.2)
col[in_outline] = outline_col
# the sleeve's corner (white) above its bottom edge and left of its right edge — both edges fitted to the painting (the lowest
# white pixel per column x 392-436, the rightmost per row y 562-608)
sb = [(x, np.nonzero(white[580:626, x])[0].max() + 580) for x in range(392, 437) if np.nonzero(white[580:626, x])[0].size]
sr = [(y, np.nonzero(white[y, 430:476])[0].max() + 430) for y in range(562, 609) if np.nonzero(white[y, 430:476])[0].size]
sb_a, sb_b = np.polyfit([q[0] for q in sb], [q[1] for q in sb], 1); sr_a, sr_b = np.polyfit([q[0] for q in sr], [q[1] for q in sr], 1)
print("the sleeve's bottom edge y = %.3f x + %.1f; its right edge x = %.3f y + %.1f" % (sb_a, sb_b, sr_a, sr_b))
sleeve = (pts[:, 1] < sb_a * pts[:, 0] + sb_b - 0.5) & (pts[:, 0] < sr_a * pts[:, 1] + sr_b - 0.5)
col[sleeve] = np.median(rgb[white & box_mask(400, 560, 440, 600)], axis=0)
# the strap over everything: the nearest curve sample, the offset along its normal, the profile blended top -> bottom
dmat = np.hypot(pts[:, 0:1] - curve[:, 0][None, :], pts[:, 1:2] - curve[:, 1][None, :])
k_near = dmat.argmin(axis=1); tpar = ts[k_near, 0]
off = (pts[:, 0] - curve[k_near, 0]) * ncur[k_near, 0] + (pts[:, 1] - curve[k_near, 1]) * ncur[k_near, 1]
hw_t = hw_top * (1 - tpar) + hw_low * tpar
# the profiles are indexed by the offset at THEIR width; scale the offset to the top profile's width for sampling
def sample_prof(prof, d):
    i = np.clip((d - D[0]), 0, len(D) - 1.001); i0 = np.floor(i).astype(int); f = i - i0
    return prof[i0] * (1 - f)[:, None] + prof[i0 + 1] * f[:, None]
d_top = off * (hw_top / hw_t); d_low = off * (hw_low / hw_t)
strap_col = sample_prof(prof_top, d_top) * (1 - tpar)[:, None] + sample_prof(prof_low, d_low) * tpar[:, None]
cover = np.clip((hw_t + 0.5 - np.abs(off)), 0, 1)                           # 1 inside the strap, a 1 px soft edge
# the sampled profile's outermost pixel is already a blend with its own surroundings; blend with the plane's navy here
col = col * (1 - cover)[:, None] + strap_col * cover[:, None]
patch[py_, px_, :3] = col; patch[py_, px_, 3] = patch_region[py_, px_] * 255
# the arm layers' alpha: 1 over the arm, and over the RIM each pixel's coverage read from its colour — how far it sits from the
# patch's colour behind toward the outline's (the layers carry the outline's colour there): at rest, outline x cov over the patch
# gives the painting's blend back; in the air the edge is the outline's, no navy or white fringe
patch_rgb = rgb.copy(); patch_rgb[py_, px_] = col
ry_, rx_ = np.nonzero(rim)
bgc = patch_rgb[ry_, rx_]; pix = rgb[ry_, rx_]; dvec = outline_col[None, :] - bgc
cov = np.clip(((pix - bgc) * dvec).sum(1) / np.maximum((dvec ** 2).sum(1), 1.0), 0, 1)
rim_cov = np.zeros((H, W), np.float32); rim_cov[ry_, rx_] = cov
arm_mask = (arm_bool.astype(np.float32) + rim_cov) * cut_soft              # the fist-arm layer
print("the rim's coverage: mean %.2f over %d px" % (cov.mean(), len(cov)))
report["patch"] = {"strap_curve": [c.round(1).tolist() for c in (C0, C1, C2, C3)], "strap_hw": [round(float(hw_top), 1), round(float(hw_low), 1)],
                   "navy_plane": coef.round(4).tolist(), "navy_rms": round(float(np.sqrt((resid ** 2).mean())), 2), "px": int(pr.sum())}

# ================= the open palm: the T3 girl's hand onto this forearm =================
im3 = Image.open(SRC3).convert("RGBA"); W3, H3 = im3.size; assert (W3, H3) == (1024, 1535)
A3 = np.asarray(im3).astype(np.float32); rgb3 = A3[..., :3]; al3 = A3[..., 3]; solid3 = al3 > 128
YY3, XX3 = np.mgrid[0:H3, 0:W3].astype(np.float32)
# her forearm comes up steeply from the lower left into the wrist; the fingers point right. The region: the hand with the forearm's
# end (so the wrist is the narrowest cross-section, not a polygon's edge)
hp3 = Image.new("L", (W3, H3), 0); ImageDraw.Draw(hp3).polygon([(790, 416), (1015, 416), (1015, 540), (880, 540), (790, 562)], fill=255)
hand3 = solid3 & (np.asarray(hp3) > 0)
# the fingers' direction: the hand's top and bottom edges over x 888-940 (the fingers), averaged
tops = [(x, np.nonzero(hand3[:, x])[0].min()) for x in range(888, 941, 2)]; bots = [(x, np.nonzero(hand3[:, x])[0].max()) for x in range(888, 941, 2)]
st = np.polyfit([t[0] for t in tops], [t[1] for t in tops], 1)[0]; sb = np.polyfit([t[0] for t in bots], [t[1] for t in bots], 1)[0]
f3 = np.array([1.0, (st + sb) / 2.0]); f3 /= np.linalg.norm(f3)
n3 = np.array([-f3[1], f3[0]])                                             # across the fingers, "down" on the screen
hy, hx = np.nonzero(hand3); hpts = np.column_stack([hx, hy]).astype(np.float64); pc = hpts.mean(axis=0)
a3 = (hpts - pc) @ f3; b3 = (hpts - pc) @ n3
prof_w = []
for s_ in np.arange(a3.min() + 2, a3.max() - 2, 1.0):
    sel = np.abs(a3 - s_) < 0.5
    if sel.sum(): prof_w.append((s_, b3[sel].max() - b3[sel].min() + 1, b3[sel].min(), b3[sel].max()))
prof_w = np.array(prof_w)
# the wrist: the narrowest cross-section between the forearm (whose slant widens the sections at the left end) and the palm
# (the thumb widens them to the right): the lowest LOCAL minimum of the smoothed width profile left of the widest section
ws = np.convolve(prof_w[:, 1], np.ones(5) / 5, mode="same"); i_wide = prof_w[:, 1].argmax()
loc = [i for i in range(8, i_wide - 4) if ws[i] <= ws[i - 4] and ws[i] <= ws[i + 4] and ws[i] < ws[i - 8] - 1]
assert loc, "no wrist (no local minimum of the width profile)"
i_min = min(loc, key=lambda i: ws[i]); s_star, w3, bmin, bmax = prof_w[i_min]
c3 = pc + f3 * s_star + n3 * ((bmin + bmax) / 2.0)                         # the cut's centre, on the hand's own axis there
print("T3 hand: fingers along %s (top slope %.3f, bottom %.3f); width profile (s, w) every 8 px: %s" % (f3.round(3).tolist(), st, sb, [(int(r[0]), int(r[1])) for r in prof_w[::8]]))
print("the cut across the wrist at s=%.0f (w %.0f px, centre %s); scale %.3f to the forearm's %.1f" % (s_star, w3, c3.round(1).tolist(), w2 / w3, w2))
k = w2 / w3
a3_full = (XX3 - pc[0]) * f3[0] + (YY3 - pc[1]) * f3[1]; b3_full = (XX3 - pc[0]) * n3[0] + (YY3 - pc[1]) * n3[1]
near_cut = (a3_full < s_star + 6) & ((b3_full < bmin - 3) | (b3_full > bmax + 3))   # beside the cut only its own cross-section (no forearm spur)
hand_keep = hand3 & ~near_cut
hand_cut = soft(hand_keep, 1.2) * np.clip((a3_full - (s_star - 8)) / 4.0 + 0.5, 0, 1)
# the outline shifted to this bitmap's maroon (the dark pixels only)
lum3 = rgb3.mean(axis=2); wgt = np.clip((150 - lum3) / 80.0, 0, 1)[..., None]
shift = (outline_col - np.array([63.0, 43.0, 35.0]))
rgb3s = rgb3 + wgt * shift[None, None, :]
hand_img = np.concatenate([rgb3s, (hand_cut * al3)[..., None]], axis=-1)
hand_im = Image.fromarray(np.clip(hand_img, 0, 255).astype(np.uint8), "RGBA")
# the placement: dst = Wp + k*(a*u - b*n), (a, b) the hand's local coords about c3 (b flipped: the thumb to the +n side)
Wp = P + u * WRIST + n * 8.0                                              # the wrist's centre: 8 px off the pivot's axis (the forearm tapers toward it)
Ainv = (f3[0] * u[0] - n3[0] * n[0]) / k, (f3[0] * u[1] - n3[0] * n[1]) / k
Binv = (f3[1] * u[0] - n3[1] * n[0]) / k, (f3[1] * u[1] - n3[1] * n[1]) / k
Cx = c3[0] - Ainv[0] * Wp[0] - Ainv[1] * Wp[1]; Cy = c3[1] - Binv[0] * Wp[0] - Binv[1] * Wp[1]
placed = hand_im.transform((W, H), Image.AFFINE, (Ainv[0], Ainv[1], Cx, Binv[0], Binv[1], Cy), resample=Image.BICUBIC)
placed = np.asarray(placed).astype(np.float32)
# the arm layers' RIM: the bitmap's anti-aliased edge pixels are blends of the outline with the strap / pinafore / shirt behind;
# lifted over other ground they would fringe navy or white. The layers carry the outline's own colour there, with the mask's
# alpha as their coverage (the same look at rest, a clean edge in the air)
A_arm = A.copy(); A_arm[rim, :3] = outline_col
# the forearm segment: the fist-arm layer up to the wrist, its end ramped over the hand (the hand is whole under the ramp)
fore_ramp = np.clip((WRIST + 3 - side) / 6.0 + 0.5, 0, 1)
fore = A_arm.copy(); fore[..., 3] = alpha * arm_mask * fore_ramp
def over(dst, src):
    a_s = src[..., 3:4] / 255; a_d = dst[..., 3:4] / 255
    out_a = a_s + a_d * (1 - a_s)
    out_rgb = (src[..., :3] * a_s + dst[..., :3] * a_d * (1 - a_s)) / np.maximum(out_a, 1e-6)
    return np.concatenate([out_rgb, out_a * 255], axis=-1)
palm = over(placed, fore)
tip = np.column_stack(np.nonzero(palm[..., 3] > 128))[:, ::-1]
reach_palm = float(np.hypot(tip[:, 0] - P[0], tip[:, 1] - P[1]).max())
report["palm"] = {"t3_cut_s": round(float(s_star), 1), "t3_cut_w": round(float(w3), 1), "scale": round(float(k), 4), "wrist": Wp.round(1).tolist(), "fingers_along": f3.round(4).tolist(), "reach": round(reach_palm, 1), "outline_shift": shift.round(1).tolist()}
print("the palm layer reaches %.0f px from the elbow (the fist %.0f): %.2f px per degree on the page" % (reach_palm, reach_fist, reach_palm * math.pi / 180 * 239 / 1024))

# ================= the eyes (girl_rig.py's method; her irises sit toward the viewer's left: the slide takes them to the eyes' centres) =================
white_e = solid & (mn > 205); dark_e = solid & (mx < 75)
# the lids are thick and their edge against the skin is blended (brownish pixels, neither skin nor black): the walk back inward
# treats those as the lid too, and stops only at the sclera or the iris (a point inside the iris's circle = no sclera there)
lidlike = dark_e | (solid & ~skin & ~white_e & (mx < 200) & (R >= B))
EYES = [{"name": "eye1", "box": (478, 246, 548, 314)}, {"name": "eye2", "box": (596, 206, 680, 282)}]   # image-left, image-right
eye_out = []
for E in EYES:
    x0, y0, x1, y1 = E["box"]; bm = box_mask(x0, y0, x1, y1)
    pupil = dark_e & bm & (mx < 45)
    bc = ((x0 + x1) / 2, (y0 + y1) / 2)
    pp = pupil & (np.hypot(XX - bc[0], YY - bc[1]) < 26)
    pyy, pxx = np.nonzero(pp); pcn = (pxx.mean(), pyy.mean())
    wb = white_e & bm & dilate(bm & ~white_e & ~skin, 1.0)
    d_ = np.hypot(XX - pcn[0], YY - pcn[1]); cand = wb & (d_ > 17) & (d_ < 33)
    cp = np.column_stack(np.nonzero(cand))[:, ::-1].astype(np.float32)
    icx, icy, ir = fit_circle(cp)
    for _ in range(2):
        rs = np.abs(np.hypot(cp[:, 0] - icx, cp[:, 1] - icy) - ir); ok = rs < 1.5
        icx, icy, ir = fit_circle(cp[ok])
    rs = np.abs(np.hypot(cp[ok, 0] - icx, cp[ok, 1] - icy) - ir)
    wy, wx = np.nonzero(white_e & bm & (d_ < 44)); c = ((wx.mean() + icx) / 2, (wy.mean() + icy) / 2)
    NA = 360; r_in = np.full(NA, np.nan); r_out = np.zeros(NA)
    for kk in range(NA):
        th = 2 * math.pi * kk / NA; dx, dy = math.cos(th), math.sin(th)
        ro = None
        for t in np.arange(8, 60, 0.5):
            xx, yy = int(round(c[0] + dx * t)), int(round(c[1] + dy * t))
            if skin[yy, xx] or not solid[yy, xx]: ro = t; break
        if ro is None: ro = 59
        r_out[kk] = ro
        ri = None; invalid = False
        for t in np.arange(ro - 0.5, 4, -0.5):
            xx, yy = int(round(c[0] + dx * t)), int(round(c[1] + dy * t))
            if np.hypot(xx - icx, yy - icy) <= ir + 1.5: invalid = True; break
            if not lidlike[yy, xx] and not skin[yy, xx]: ri = t + 0.5; break
        if ri is not None and not invalid: r_in[kk] = ri
    valid = ~np.isnan(r_in); idx = np.arange(NA); ang = 2 * math.pi * idx / NA
    vx, vy = c[0] + np.cos(ang[valid]) * r_in[valid], c[1] + np.sin(ang[valid]) * r_in[valid]
    Mq = np.column_stack([vx * vx, vx * vy, vy * vy, vx, vy]); coefq, *_ = np.linalg.lstsq(Mq, -np.ones(len(vx)), rcond=None)
    Aq, Bq, Cq, Dq, Eq = coefq
    def ell_r(th):
        dx, dy = math.cos(th), math.sin(th); xx0, yy0 = c
        qa = Aq * dx * dx + Bq * dx * dy + Cq * dy * dy
        qb = 2 * Aq * xx0 * dx + Bq * (xx0 * dy + yy0 * dx) + 2 * Cq * yy0 * dy + Dq * dx + Eq * dy
        qc = Aq * xx0 * xx0 + Bq * xx0 * yy0 + Cq * yy0 * yy0 + Dq * xx0 + Eq * yy0 + 1
        disc = qb * qb - 4 * qa * qc
        if disc < 0: return float("nan")
        tt = [(-qb + sg * math.sqrt(disc)) / (2 * qa) for sg in (1, -1)]; tt = [t for t in tt if t > 0]
        return min(tt) if tt else float("nan")
    r_ell = np.array([ell_r(th) for th in ang]); ell_err = float(np.nanmean(np.abs(r_ell[valid] - r_in[valid])))
    r_full = np.where(valid, r_in, r_ell); r_full = np.where(np.isnan(r_full), r_out - 2.0, r_full)
    r_full = np.minimum(r_full, r_out - 2.0)
    kern = np.ones(13) / 13; r_s = np.convolve(np.concatenate([r_full[-6:], r_full, r_full[:6]]), kern, mode="valid") - 0.6
    S = 4; poly_pts = [((c[0] + math.cos(2 * math.pi * kk / NA) * r_s[kk]) * S, (c[1] + math.sin(2 * math.pi * kk / NA) * r_s[kk]) * S) for kk in range(NA)]
    bx0, by0 = x0 - 10, y0 - 10; bw, bh = (x1 - x0) + 20, (y1 - y0) + 20
    sm = Image.new("L", (bw * S, bh * S), 0); ImageDraw.Draw(sm).polygon([(qx - bx0 * S, qy - by0 * S) for qx, qy in poly_pts], fill=255)
    sm = sm.resize((bw, bh), Image.BOX)
    eye_mask = np.zeros((H, W), np.float32); eye_mask[by0:by0 + bh, bx0:bx0 + bw] = np.asarray(sm).astype(np.float32) / 255.0
    sc = np.median(rgb[white_e & bm & (d_ < 44)], axis=0)
    rad = int(math.ceil(ir + 3)); ox, oy = int(math.floor(icx)) - rad, int(math.floor(icy)) - rad; sz = 2 * rad + 1
    iris = np.zeros((sz, sz, 4), np.float32); gy, gx = np.mgrid[0:sz, 0:sz]; fxx, fyy = ox + gx, oy + gy
    rr = np.hypot(fxx + 0.0 - icx, fyy + 0.0 - icy); inside = rr <= ir + 2.2; shine = white_e[fyy, fxx]
    vis = inside & (eye_mask[fyy, fxx] > 0.5) & solid[fyy, fxx]; cols = rgb[fyy, fxx]
    prof_r = np.arange(0, ir + 2, 0.5); prof = np.zeros((len(prof_r), 3))
    for i, prr in enumerate(prof_r):
        sel = vis & ~shine & (np.abs(rr - prr) <= 0.75)
        if sel.sum() < 3: sel = vis & ~shine & (np.abs(rr - prr) <= 1.5)
        prof[i] = cols[sel].mean(axis=0) if sel.sum() else (prof[i - 1] if i else sc)
    synth = np.stack([np.interp(rr, prof_r, prof[:, ch]) for ch in range(3)], axis=-1)
    iris[..., :3] = np.where(vis[..., None], cols, synth); iris[..., 3] = np.clip((ir + 2.2 - rr), 0, 1) * 255
    iris_im = Image.fromarray(np.clip(iris, 0, 255).astype(np.uint8), "RGBA")
    iris_im.save(OUT / f"demo1_girl_iris{E['name'][-1]}.png", optimize=True); save_mask(eye_mask, OUT / f"demo1_girl_{E['name']}_mask.png")
    # the interior's centre (its mask's centroid) — where the iris slides to: she looks at the screen
    my, mxx = np.nonzero(eye_mask > 0.5); centre_int = (mxx.mean() + 0.5, my.mean() + 0.5)
    room = {"left": round(float(r_s[180] - (ir + (c[0] - icx))), 1), "right": round(float(r_s[0] - (ir - (c[0] - icx))), 1), "down": round(float(r_s[90] - (ir - (c[1] - icy))), 1), "up": round(float(r_s[270] - (ir + (c[1] - icy))), 1)}
    gx_ = centre_int[0] - icx; gy_ = centre_int[1] - icy
    eo = {"name": E["name"], "iris": {"cx": round(float(icx), 2), "cy": round(float(icy), 2), "r": round(float(ir), 2), "fit_pts": int(ok.sum()), "fit_rms": round(float(np.sqrt((rs ** 2).mean())), 2)},
          "iris_box": [ox, oy, sz, sz], "pupil": [round(float(pcn[0]), 1), round(float(pcn[1]), 1)], "centre": [round(c[0], 1), round(c[1], 1)], "interior_centre": [round(float(centre_int[0]), 1), round(float(centre_int[1]), 1)],
          "interior_r": {"min": round(float(r_s.min()), 1), "max": round(float(r_s.max()), 1), "valid_angles": int(valid.sum()), "ellipse_fit_err": round(ell_err, 2)},
          "sclera": [int(v_) for v_ in sc], "room": room, "to_centre": [round(float(gx_), 2), round(float(gy_), 2)]}
    my, mxx = np.nonzero(eye_mask > 0.5)
    eo["interior_box"] = [int(mxx.min()), int(my.min()), int(mxx.max()) + 1, int(my.max()) + 1]
    eye_out.append(eo); E["mask"] = eye_mask; E["out"] = eo; E["iris_im"] = iris_im
    print(f"{E['name']}: iris c {icx:.1f},{icy:.1f} r {ir:.1f} ({ok.sum()} pts, rms {eo['iris']['fit_rms']}), interior r {r_s.min():.1f}-{r_s.max():.1f} ({valid.sum()}/360 read, ellipse err {ell_err:.2f}), sclera {eo['sclera']}, room {room}, to the centre ({gx_:+.1f}, {gy_:+.1f})")
report["eyes"] = eye_out

# ---------- the sheets ----------
save_mask(body_mask, OUT / "demo1_girl_body_mask.png")
arm_sheet = A_arm.copy(); arm_sheet[..., 3] = alpha * arm_mask; save_rgba(arm_sheet, OUT / "demo1_girl_arm.png")   # its own image (the rim recoloured), not a masked window
old = OUT / "demo1_girl_arm_mask.png"
if old.exists(): old.unlink()
save_rgba(patch, OUT / "demo1_girl_patch.png"); save_rgba(palm, OUT / "demo1_girl_palm.png")
report["sheets"] = {p.name: p.stat().st_size for p in sorted(OUT.glob("*.png"))}
print("sheets:", {kk: f"{v / 1024:.1f}K" for kk, v in report["sheets"].items()})

# ---------- the composite at rest must give the painting back ----------
def over_m(dst, src, m):
    a_s = src[..., 3:4] / 255 * m[..., None]; a_d = dst[..., 3:4] / 255
    out_a = a_s + a_d * (1 - a_s)
    out_rgb = (src[..., :3] * a_s + dst[..., :3] * a_d * (1 - a_s)) / np.maximum(out_a, 1e-6)
    return np.concatenate([out_rgb, out_a * 255], axis=-1)
ones = np.ones((H, W), np.float32)
def composite(arm_deg=0.0, palm_op=0.0, eye_dx=0.0, eye_dy=0.0):
    comp = over_m(patch, A, body_mask)
    for E in EYES:
        eo = E["out"]; grp = A.copy()
        disc = (np.hypot(XX - eo["iris"]["cx"], YY - eo["iris"]["cy"]) <= eo["iris"]["r"] + 1).astype(np.float32)
        fill = np.zeros((H, W, 4), np.float32); fill[..., :3] = eo["sclera"]; fill[..., 3] = 255; grp = over_m(grp, fill, disc)
        ir_ = np.asarray(E["iris_im"]).astype(np.float32); ox, oy, sz, _ = eo["iris_box"]
        lay = np.zeros((H, W, 4), np.float32)
        if eye_dx or eye_dy:
            li = Image.fromarray(np.clip(ir_, 0, 255).astype(np.uint8), "RGBA").transform((sz, sz), Image.AFFINE, (1, 0, -eye_dx, 0, 1, -eye_dy), resample=Image.BICUBIC)
            ir_ = np.asarray(li).astype(np.float32)
        lay[oy:oy + sz, ox:ox + sz] = ir_; grp = over_m(grp, lay, ones)
        comp = over_m(comp, grp, E["mask"])
    armL = A_arm.copy(); armL[..., 3] = alpha * arm_mask * (1 - palm_op)
    palmL = palm.copy(); palmL[..., 3] *= palm_op
    for L in (armL, palmL):
        if arm_deg:
            Li = Image.fromarray(np.clip(L, 0, 255).astype(np.uint8), "RGBA").rotate(-arm_deg, resample=Image.BICUBIC, center=(float(P[0]), float(P[1])))
            L = np.asarray(Li).astype(np.float32)
        comp = over_m(comp, L, ones)
    return comp
comp = composite()
diff = np.abs(comp[..., :3] - A[..., :3]).max(axis=2) * (alpha > 0) + np.abs(comp[..., 3] - alpha)
print("rest composite vs the painting: max diff %.1f levels, %d px over 8, %d px over 24" % (diff.max(), (diff > 8).sum(), (diff > 24).sum()))
for nm_, bx_ in (("eye1", (470, 240, 555, 320)), ("eye2", (590, 200, 690, 290)), ("arm", (360, 520, 580, 730))):
    sub = diff[bx_[1]:bx_[3], bx_[0]:bx_[2]]; yy_, xx_ = np.nonzero(sub > 8)
    print("   %s: %d px over 8, %d over 24%s" % (nm_, (sub > 8).sum(), (sub > 24).sum(), (" at x %d-%d y %d-%d" % (bx_[0] + xx_.min(), bx_[0] + xx_.max(), bx_[1] + yy_.min(), bx_[1] + yy_.max())) if len(xx_) else ""))
report["rest_diff"] = {"max": round(float(diff.max()), 1), "over8": int((diff > 8).sum()), "over24": int((diff > 24).sum())}
# ... and at the PAGE's size (239x358, over a mid grey as the hallway would be): what a viewer could see
def at_page(arr):
    flat = Image.alpha_composite(Image.new("RGBA", (W, H), (128, 128, 128, 255)), Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA"))
    return np.asarray(flat.convert("RGB").resize((239, 358), Image.LANCZOS)).astype(np.float32)
pdiff = np.abs(at_page(comp) - at_page(A)).max(axis=2)
worst = np.argsort(diff.ravel())[-6:][::-1]
print("   the worst pixels (x, y, diff, painted -> composite):", [(int(i % W), int(i // W), int(diff.ravel()[i]), tuple(int(v) for v in A[i // W, i % W, :3]), tuple(int(v) for v in comp[i // W, i % W, :3])) for i in worst])
pw = np.argsort(pdiff.ravel())[-4:][::-1]; print("   at the page's size, the worst:", [(int(i % 239), int(i // 239), int(pdiff.ravel()[i])) for i in pw])
print("at the page's size (239x358): max diff %.1f levels, %d px over 4, %d over 8" % (pdiff.max(), (pdiff > 4).sum(), (pdiff > 8).sum()))
report["rest_diff_page"] = {"max": round(float(pdiff.max()), 1), "over4": int((pdiff > 4).sum()), "over8": int((pdiff > 8).sum())}
(OUT / "rig.json").write_text(json.dumps(report, indent=1), encoding="utf-8")

if DEBUG:
    bgc = (120, 170, 120, 255)
    def show(arr, box, k, name):
        c = Image.alpha_composite(Image.new("RGBA", (W, H), bgc), Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")).crop(box)
        c = c.resize(((box[2] - box[0]) * k, (box[3] - box[1]) * k), Image.LANCZOS); c.convert("RGB").save(DEBUG / name)
    show(comp, (300, 150, 720, 780), 1, "dbg_rest.png")
    gx1, gy1 = eye_out[0]["to_centre"]; gx2, gy2 = eye_out[1]["to_centre"]
    up = composite(-60, 1.0, (gx1 + gx2) / 2, (gy1 + gy2) / 2); show(up, (300, 150, 720, 780), 1, "dbg_up60_palm.png")
    show(composite(-60, 0.0), (300, 150, 720, 780), 1, "dbg_up60_fist.png")
    show(composite(-30, 0.5), (340, 480, 620, 760), 3, "dbg_up30_mix.png")
    show(composite(-60, 1.0), (340, 440, 620, 720), 3, "dbg_up60_zoom.png")
    show(over_m(patch, A, body_mask), (340, 500, 620, 760), 3, "dbg_body_patch.png")
    show(patch, (340, 500, 620, 760), 3, "dbg_patch.png"); show(palm, (380, 500, 660, 700), 3, "dbg_palm.png")
    d8 = np.zeros((H, W, 4), np.float32); d8[..., 0] = np.clip(diff * 4, 0, 255); d8[..., 3] = 255; show(d8, (300, 150, 720, 780), 1, "dbg_rest_diff.png")
    d9 = A.copy(); hot = diff > 12; d9[hot, :3] = [0, 255, 0]; d9[diff > 40, :3] = [255, 0, 255]; show(d9, (360, 520, 580, 730), 3, "dbg_arm_diff.png")
    for E in EYES:
        eo = E["out"]; x0, y0, x1, y1 = E["box"]
        c = Image.alpha_composite(Image.new("RGBA", (W, H), bgc), im).crop((x0 - 8, y0 - 8, x1 + 8, y1 + 8)); kq = 6
        c = c.resize((c.width * kq, c.height * kq), Image.NEAREST); d = ImageDraw.Draw(c); T = lambda x, y: ((x - (x0 - 8)) * kq, (y - (y0 - 8)) * kq)
        d.ellipse([T(eo["iris"]["cx"] - eo["iris"]["r"], eo["iris"]["cy"] - eo["iris"]["r"]), T(eo["iris"]["cx"] + eo["iris"]["r"], eo["iris"]["cy"] + eo["iris"]["r"])], outline=(255, 255, 0, 255), width=1)
        e = boundary(E["mask"] > 0.5); ys, xs = np.nonzero(e)
        for x, y in zip(xs, ys): d.point(T(x + 0.5, y + 0.5), fill=(0, 255, 255, 255))
        d.ellipse([T(eo["interior_centre"][0] - 2, eo["interior_centre"][1] - 2), T(eo["interior_centre"][0] + 2, eo["interior_centre"][1] + 2)], fill=(255, 0, 0, 255))
        c.convert("RGB").save(DEBUG / f"dbg_{E['name']}.png")
    eyes_up = composite(0, 0, (gx1 + gx2) / 2, (gy1 + gy2) / 2); show(eyes_up, (440, 180, 700, 340), 3, "dbg_eyes_centre.png"); show(comp, (440, 180, 700, 340), 3, "dbg_eyes_rest.png")
    print("debug overlays in", DEBUG)
