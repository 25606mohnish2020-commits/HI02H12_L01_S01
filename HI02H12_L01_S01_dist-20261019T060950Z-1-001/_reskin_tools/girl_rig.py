"""girl_rig.py — [t3-look] (2026-11-02) the T3 girl's glance rig, cut from her own bitmap (demo2_assets/img_demo2_girl_ask.webp,
the frame 724:2016's "image 272", 1024x1535, drawn 257x385).

The page shows her as LAYERS that all window the same bitmap (so at rest the composite is the painting, pixel for pixel) and move
by CSS transforms — see build.py [t3-look] and the PUNCT_SCENE module:
  body   the bitmap, with a HOLE where the open-palm forearm is (beyond the elbow's keep disk, beyond the braid tip's keep zone:
         the room shows through there when the arm lifts); demo2_girl_body_mask.png (white = kept)
  eyes   per eye, the bitmap clipped to the eye's INTERIOR (inside the painted outline's inner edge: demo2_girl_eye{1,2}_mask.png),
         a sclera-coloured disc over the painted iris, and the iris itself (demo2_girl_iris{1,2}.png: the painted iris, its part
         hidden under the outline / lid completed from its own radial profile) which slides toward the tiles
  arm    the forearm + hand from the elbow's cut line (demo2_girl_arm_mask.png), turning about the elbow: the outer elbow is a
         circular arc about that pivot, so the silhouette stays whole as it turns; the body keeps a disc there (R_keep) and a
         band under the braid tip (the braid lies OVER the forearm's upper edge), so no gap opens on either side
  patch  the braid tip (demo2_girl_patch_mask.png), painted last: the arm slides UNDER the hair as it lifts
Writes demo2_assets/girl_rig/ (the sheets, the irises, rig.json with the geometry in bitmap px) and, with --debug, overlays into
the folder given. All masks are full 1024x1535 L sheets (black outside), applied at the girl's box size by CSS, so nothing needs
an offset. Run: python -I girl_rig.py [--debug <dir>]
"""
import sys, json, pathlib, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SCR = pathlib.Path(__file__).resolve().parent
SRC = SCR / "demo2_assets" / "img_demo2_girl_ask.webp"
OUT = SCR / "demo2_assets" / "girl_rig"; OUT.mkdir(exist_ok=True)
DEBUG = pathlib.Path(sys.argv[sys.argv.index("--debug") + 1]) if "--debug" in sys.argv else None
if DEBUG: DEBUG.mkdir(parents=True, exist_ok=True)

im = Image.open(SRC).convert("RGBA"); W, H = im.size
assert (W, H) == (1024, 1535), (W, H)
A = np.asarray(im).astype(np.float32); rgb = A[..., :3]; alpha = A[..., 3]
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
mx = rgb.max(axis=2); mn = rgb.min(axis=2)
solid = alpha > 128
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)

def box_mask(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[y0:y1, x0:x1] = True; return m
def dilate(m, r):
    """binary dilation by a disc of radius r (px)"""
    k = int(math.ceil(r)); out = np.zeros_like(m)
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            if dx * dx + dy * dy > r * r + 1e-6: continue
            s = np.roll(np.roll(m, dy, 0), dx, 1); out |= s
    return out
def soft(m, px):
    """a 0..1 float mask with its edge blurred over ~px"""
    f = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(px / 2.0))
    return np.asarray(f).astype(np.float32) / 255.0
def save_mask(m, path):
    """a CSS mask sheet: the mask in the ALPHA channel (mask-mode match-source reads a raster image's alpha — a greyscale PNG
    without alpha masks nothing, measured on Chrome 156), white underneath"""
    a = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8), "L"); w = Image.new("L", a.size, 255)
    Image.merge("RGBA", [w, w, w, a]).save(path, optimize=True)
def fit_circle(pts):
    """algebraic least-squares circle through the points (N x 2) -> (cx, cy, r)"""
    x, y = pts[:, 0], pts[:, 1]
    M = np.column_stack([x, y, np.ones_like(x)]); b = -(x * x + y * y)
    (D, E, F), *_ = np.linalg.lstsq(M, b, rcond=None)
    cx, cy = -D / 2, -E / 2; return cx, cy, math.sqrt(cx * cx + cy * cy - F)
def boundary(m):
    """pixels of m with a 4-neighbour outside m"""
    e = np.zeros_like(m)
    e[1:, :] |= m[1:, :] & ~m[:-1, :]; e[:-1, :] |= m[:-1, :] & ~m[1:, :]
    e[:, 1:] |= m[:, 1:] & ~m[:, :-1]; e[:, :-1] |= m[:, :-1] & ~m[:, 1:]
    return e

# ---------- colour classes ----------
hair = solid & (mx < 100)                                                  # the braids' dark (the arm's outline is lighter: mx ~ 130-160)
skin = solid & (R > 185) & (G > 120) & (B > 80) & (R - B > 45) & (G < 215)  # the skin, lit and shaded
white = solid & (mn > 205)                                                 # the sclerae, the shines
dark = solid & (mx < 75)                                                   # the eyes' outlines, rims, pupils

report = {}

# ================= the arm =================
# The joint. The forearm's lower edge is a straight run (the rightmost solid pixel per row, y 520-600) that bends into the elbow's
# bottom below y ~610. The arm layer turns about a pivot P that sits on the inward normal of that edge at B, the point where the
# straight run ends: the keep circle (radius R = |B - P|) is tangent to the edge there and lies INSIDE the arm everywhere else
# (R no larger than the bend's radius of curvature below B), and the cut line L through P is perpendicular to the forearm, so it
# passes through B too. The body keeps everything inside the circle (static) and the layer turns what lies beyond it on the
# forearm's side of L: the only silhouette the hole's boundary crosses is B, where the turned edge (still tangent to the circle,
# at a point R*theta further on) leaves the static one by R(1 - cos theta) ~ 0.5 px. The elbow's bottom and the crease stay.
def edge_x(y):
    """the lower edge's sub-pixel x on row y: where alpha crosses 128 going right from the arm (x 640-1000)"""
    row = alpha[y, 640:1000]; xs = np.nonzero(row > 128)[0]
    if not len(xs): return None
    i = xs.max(); a0, a1 = row[i], row[i + 1] if i + 1 < len(row) else 0.0
    return 640 + i + (a0 - 128) / max(a0 - a1, 1e-6)
def edge_y(x):
    """the bottom's sub-pixel y in column x: where alpha crosses 128 going down (y 450-720)"""
    col = alpha[450:720, x]; ys = np.nonzero(col > 128)[0]
    if not len(ys): return None
    i = ys.max(); a0, a1 = col[i], col[i + 1] if i + 1 < len(col) else 0.0
    return 450 + i + (a0 - 128) / max(a0 - a1, 1e-6)
sil = [(edge_x(y), float(y)) for y in range(520, 646)] + [(float(x), edge_y(x)) for x in range(769, 688, -1) if edge_y(x) is not None and edge_y(x) < 700]
sil = np.array([q for q in sil if q[0] is not None], np.float32)
lp = sil[(sil[:, 1] >= 520) & (sil[:, 1] <= 590)]
a_, b_ = np.polyfit(lp[:, 1], lp[:, 0], 1)                                # x = a*y + b along the straight run
inside = (a_ * sil[:, 1] + b_) - sil[:, 0]                                # >0 = inside that line
yB = next(float(y) for (x, y), d in zip(sil, inside) if y >= 590 and d > 1.0) - 2   # the straight run ends where the edge is 1 px inside the line
iB = int(np.argmin(np.abs(sil[:, 1] - yB) + (sil[:, 1] < 500) * 1e9)); B = sil[iB].copy()
loc = sil[(sil[:, 1] >= yB - 10) & (sil[:, 1] <= yB + 3)]                 # the edge's direction AT B (a short window)
al, bl = np.polyfit(loc[:, 1], loc[:, 0], 1)
u = np.array([-al, -1.0]); u /= np.linalg.norm(u)                         # the forearm's direction at B, toward the hand (up-right)
n = np.array([1.0, -al]); n /= np.linalg.norm(n)                          # the outward normal there (down-right)
along = np.cumsum(np.r_[0, np.hypot(np.diff(sil[:, 0]), np.diff(sil[:, 1]))])
rho = []
for i in range(iB, len(sil)):                                             # the bend's radius of curvature below B (24 px windows)
    w = sil[(along >= along[i] - 12) & (along <= along[i] + 12)]
    if len(w) < 8: continue
    try: rho.append((float(along[i] - along[iB]), fit_circle(w)[2]))
    except Exception: pass
rho_min = min(r for s_, r in rho if 4 <= s_ <= 60)
best = None
for Rr in np.arange(44, 14, -0.5):                                        # the largest circle (<= 44) tangent at B that stays inside the arm elsewhere
    Pc = B - Rr * n
    dd = np.hypot(sil[:, 0] - Pc[0], sil[:, 1] - Pc[1]) - Rr
    far = np.hypot(sil[:, 0] - B[0], sil[:, 1] - B[1]) > 2.5
    if dd[far].min() >= -0.3: best = (float(Rr), Pc, float(dd[far].min())); break
assert best, "no keep circle clears the silhouette"
R_keep, Pc, clearance = best
cx, cy = float(Pc[0]), float(Pc[1]); P = (cx, cy)
report["elbow"] = {"pivot": [round(cx, 2), round(cy, 2)], "R_keep": round(float(R_keep), 2), "B": [round(float(B[0]), 1), round(float(B[1]), 1)],
                   "straight_run": {"a": round(float(a_), 4), "b": round(float(b_), 2), "rms": round(float(np.sqrt(((a_ * lp[:, 1] + b_ - lp[:, 0]) ** 2).mean())), 2)},
                   "u": [round(float(u[0]), 4), round(float(u[1]), 4)], "bend_rho_min": round(rho_min, 1), "clearance": round(clearance, 2)}
print("elbow: the lower edge's straight run x = %.3f y + %.1f (rms %.2f px, y 520-590) ends at B %.1f,%.1f; the edge's direction there %s, the bend's radius >= %.0f px; pivot %.1f,%.1f, R %.1f (the circle inside the arm by >= %.2f px elsewhere)"
      % (a_, b_, report["elbow"]["straight_run"]["rms"], B[0], B[1], np.round(u, 3), rho_min, cx, cy, R_keep, clearance))
side = (XX - cx) * u[0] + (YY - cy) * u[1]                                # signed distance along the forearm from the line through P across it (+ = the forearm)
CUT = 10.0                                                                # the layer's cut line sits 10 px up the forearm from P: the elbow's crease (its top end
                                                                          # reaches 8 px past P) stays whole with the body, instead of its top turning with the arm
# the arm layer: the forearm's side of the cut line (feathered over 6 px: the body is whole under it, inside the keep disc) within
# a polygon that leaves out the braid tip, the sleeve, the upper arm's left outline and the dress (bitmap px, placed on the
# gridded zooms: the braid's bottom edge y ~536 for x 735-775 and its right edge up to (786, 480); the ruffle's corner (725, 540);
# the upper arm's left outline x ~665-672 — the polygon's left side stays inside the skin at x 688)
POLY = [(688, 548), (735, 548), (776, 542), (786, 500), (792, 470), (812, 452), (850, 414), (1010, 414), (1010, 600), (930, 700), (700, 700), (688, 640)]
pm = Image.new("L", (W, H), 0); ImageDraw.Draw(pm).polygon(POLY, fill=255); poly = np.asarray(pm) > 0
hair_near = hair & box_mask(690, 430, 800, 552)                            # the braid's tip, where it meets the arm
hair_d1 = dilate(hair_near, 1.5)
cut_soft = np.clip((side - CUT) / 6.0 + 0.5, 0, 1)
arm_mask = np.where(poly & ~hair_d1, cut_soft, 0.0).astype(np.float32)
fore_hard = poly & (side > CUT) & ~hair_d1
dist_p = np.hypot(XX - cx, YY - cy)
keep_disc = np.clip((R_keep + 0.75 - dist_p) / 1.5, 0, 1)                 # 1 inside the circle, feathered over 1.5 px about R
hair_zone = dilate(hair_near, 14)                                         # the band under the braid tip: the arm's upper edge lives under the hair there
opaque = alpha >= 250
hole = fore_hard.astype(np.float32) * (1 - keep_disc * opaque); hole[hair_zone & opaque] = 0
hole[side < CUT + 3] = 0                                                  # the layer's cut feather (CUT +- 3) never meets the hole's edge
patch_mask = dilate(hair_near, 1.0).astype(np.float32)                   # hard: the patch and the body split these pixels exactly
body_mask = 1 - np.maximum(hole, patch_mask)
report["arm"] = {"poly": POLY, "hair_zone_px": 14, "cut_px": CUT, "cut_feather_px": 6, "layer_px": int((arm_mask > 0.5).sum()), "hole_px": int((hole > 0.5).sum()), "patch_px": int((patch_mask > 0.5).sum())}
touch = hair_near & dilate(fore_hard, 2)
ys, xs = np.nonzero(touch)
report["arm"]["braid_touch_box"] = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1] if len(xs) else None
print("arm layer", report["arm"]["layer_px"], "px, the body's hole", report["arm"]["hole_px"], "px, the braid patch", report["arm"]["patch_px"], "px; the braid tip meets the forearm in", report["arm"]["braid_touch_box"])
# the hand's reach from the pivot (how far the fingertips travel per degree)
hp = np.column_stack(np.nonzero(solid & box_mask(900, 400, 1010, 560)))[:, ::-1]
reach = float(np.hypot(hp[:, 0] - cx, hp[:, 1] - cy).max()); report["elbow"]["reach"] = round(reach, 1)
print("fingertips %.0f px from the pivot: %.1f px per degree (%.2f on the page)" % (reach, reach * math.pi / 180, reach * math.pi / 180 * 257 / 1024))

# ================= the eyes =================
EYES = [{"name": "eye1", "box": (440, 240, 535, 325)}, {"name": "eye2", "box": (578, 196, 652, 280)}]   # image-left, image-right
eye_out = []
for E in EYES:
    x0, y0, x1, y1 = E["box"]; bm = box_mask(x0, y0, x1, y1)
    pupil = dark & bm & (mx < 45)
    # the pupil's centre: the darkest blob's centroid (the outline is thinner and off-centre; take the pixels within 22 px of the box centre)
    bc = ((x0 + x1) / 2, (y0 + y1) / 2)
    pp = pupil & (np.hypot(XX - bc[0], YY - bc[1]) < 24)
    py, px = np.nonzero(pp); pc = (px.mean(), py.mean())
    # the iris's edge against the sclera: white pixels next to a non-white, non-skin pixel, 17-30 px from the pupil's centre
    wb = white & bm & dilate(bm & ~white & ~skin, 1.0)
    d_ = np.hypot(XX - pc[0], YY - pc[1]); cand = wb & (d_ > 17) & (d_ < 31)
    cp = np.column_stack(np.nonzero(cand))[:, ::-1].astype(np.float32)
    icx, icy, ir = fit_circle(cp)
    for _ in range(2):
        rs = np.abs(np.hypot(cp[:, 0] - icx, cp[:, 1] - icy) - ir); ok = rs < 1.5
        icx, icy, ir = fit_circle(cp[ok])
    rs = np.abs(np.hypot(cp[ok, 0] - icx, cp[ok, 1] - icy) - ir)
    # the eye's interior: from an inner point, along 360 rays, out to the first skin pixel (the outline's outer edge), then back in
    # over the outline to its inner edge; where the iris touches the outline the inner edge is read from the neighbouring angles
    wy, wx = np.nonzero(white & bm & (d_ < 42)); c = ((wx.mean() + icx) / 2, (wy.mean() + icy) / 2)
    NA = 360; r_in = np.full(NA, np.nan); r_out = np.zeros(NA)
    for k in range(NA):
        th = 2 * math.pi * k / NA; dx, dy = math.cos(th), math.sin(th)
        ro = None
        for t in np.arange(8, 60, 0.5):
            xx, yy = int(round(c[0] + dx * t)), int(round(c[1] + dy * t))
            if skin[yy, xx] or not solid[yy, xx]: ro = t; break
        if ro is None: ro = 59
        r_out[k] = ro
        ri = None
        for t in np.arange(ro - 0.5, 4, -0.5):
            xx, yy = int(round(c[0] + dx * t)), int(round(c[1] + dy * t))
            if not dark[yy, xx] and not skin[yy, xx]: ri = t + 0.5; break
        if ri is not None:
            # a point inside the iris circle (+1.5) means the walk went through the rim: no sclera at this angle
            px_, py_ = c[0] + dx * ri, c[1] + dy * ri
            if np.hypot(px_ - icx, py_ - icy) > ir + 1.5: r_in[k] = ri
    valid = ~np.isnan(r_in); idx = np.arange(NA)
    # the angles that could not be read (the iris's rim merges with the stroke there) take an ellipse fitted to those that could
    ang = 2 * math.pi * idx / NA
    vx, vy = c[0] + np.cos(ang[valid]) * r_in[valid], c[1] + np.sin(ang[valid]) * r_in[valid]
    M = np.column_stack([vx * vx, vx * vy, vy * vy, vx, vy]); coef, *_ = np.linalg.lstsq(M, -np.ones(len(vx)), rcond=None)
    Aq, Bq, Cq, Dq, Eq = coef
    def ell_r(th):   # the ellipse's radius along the ray from c (solve the conic for t >= 0)
        dx, dy = math.cos(th), math.sin(th); x0, y0 = c
        qa = Aq * dx * dx + Bq * dx * dy + Cq * dy * dy
        qb = 2 * Aq * x0 * dx + Bq * (x0 * dy + y0 * dx) + 2 * Cq * y0 * dy + Dq * dx + Eq * dy
        qc = Aq * x0 * x0 + Bq * x0 * y0 + Cq * y0 * y0 + Dq * x0 + Eq * y0 + 1
        disc = qb * qb - 4 * qa * qc
        if disc < 0: return float("nan")
        ts = [(-qb + sg * math.sqrt(disc)) / (2 * qa) for sg in (1, -1)]; ts = [t for t in ts if t > 0]
        return min(ts) if ts else float("nan")
    r_ell = np.array([ell_r(th) for th in ang])
    ell_err = float(np.abs(r_ell[valid] - r_in[valid]).mean())
    r_full = np.where(valid, r_in, r_ell)
    r_full = np.minimum(r_full, r_out - 2.0)                             # the stroke is at least 2 px thick everywhere
    # smooth over +-6 degrees (circular)
    kern = np.ones(13) / 13; r_s = np.convolve(np.concatenate([r_full[-6:], r_full, r_full[:6]]), kern, mode="valid")
    r_s = r_s - 0.6   # eroded a touch: the iris's sliding edge is clipped a hair before the outline, never over it
    # the interior mask, drawn 4x and downsampled (anti-aliased)
    S = 4; poly_pts = [((c[0] + math.cos(2 * math.pi * k / NA) * r_s[k]) * S, (c[1] + math.sin(2 * math.pi * k / NA) * r_s[k]) * S) for k in range(NA)]
    big = Image.new("L", (W * S, H * S), 0)
    # only the eye's neighbourhood is drawn big (memory): crop, draw, paste
    bx0, by0 = x0 - 10, y0 - 10; bw, bh = (x1 - x0) + 20, (y1 - y0) + 20
    sm = Image.new("L", (bw * S, bh * S), 0); ImageDraw.Draw(sm).polygon([(px_ - bx0 * S, py_ - by0 * S) for px_, py_ in poly_pts], fill=255)
    sm = sm.resize((bw, bh), Image.BOX)
    eye_mask = np.zeros((H, W), np.float32); eye_mask[by0:by0 + bh, bx0:bx0 + bw] = np.asarray(sm).astype(np.float32) / 255.0
    # the sclera's colour: the median of the white pixels of this eye
    sc = np.median(rgb[white & bm & (d_ < 42)], axis=0)
    # the iris: the painted disc, completed. visible = inside the interior (not under the outline); hidden pixels take the mean
    # colour of the visible ones at the same radius (the shines left out of that profile)
    rad = int(math.ceil(ir + 3)); ox, oy = int(math.floor(icx)) - rad, int(math.floor(icy)) - rad; sz = 2 * rad + 1
    iris = np.zeros((sz, sz, 4), np.float32)
    gy, gx = np.mgrid[0:sz, 0:sz]; fx, fy = ox + gx, oy + gy
    rr = np.hypot(fx + 0.0 - icx, fy + 0.0 - icy)
    inside = rr <= ir + 2.2
    shine = white[fy, fx]
    vis = inside & (eye_mask[fy, fx] > 0.5) & solid[fy, fx]                 # every painted pixel inside the interior stays as painted
    cols = rgb[fy, fx]
    prof_r = np.arange(0, ir + 2, 0.5); prof = np.zeros((len(prof_r), 3))
    for i, pr in enumerate(prof_r):
        sel = vis & ~shine & (np.abs(rr - pr) <= 0.75)                 # the profile: the painted iris without its shines / the sclera's sliver
        if sel.sum() < 3: sel = vis & ~shine & (np.abs(rr - pr) <= 1.5)
        prof[i] = cols[sel].mean(axis=0) if sel.sum() else (prof[i - 1] if i else sc)
    for i in range(len(prof_r)):   # fill any empty radii from the previous
        if not np.isfinite(prof[i]).all(): prof[i] = prof[i - 1]
    synth = np.stack([np.interp(rr, prof_r, prof[:, ch]) for ch in range(3)], axis=-1)
    iris[..., :3] = np.where(vis[..., None], cols, synth)
    iris[..., 3] = np.clip((ir + 2.2 - rr), 0, 1) * 255
    iris_im = Image.fromarray(np.clip(iris, 0, 255).astype(np.uint8), "RGBA")
    iris_im.save(OUT / f"demo2_girl_iris{E['name'][-1]}.png", optimize=True)
    save_mask(eye_mask, OUT / f"demo2_girl_{E['name']}_mask.png")
    hidden = int((inside & ~vis).sum())
    eo = {"name": E["name"], "iris": {"cx": round(float(icx), 2), "cy": round(float(icy), 2), "r": round(float(ir), 2), "fit_pts": int(ok.sum()), "fit_rms": round(float(np.sqrt((rs ** 2).mean())), 2), "hidden_px": hidden},
          "iris_box": [ox, oy, sz, sz], "pupil": [round(float(pc[0]), 1), round(float(pc[1]), 1)], "centre": [round(c[0], 1), round(c[1], 1)],
          "interior_r": {"min": round(float(r_s.min()), 1), "max": round(float(r_s.max()), 1), "valid_angles": int(valid.sum()), "ellipse_fit_err": round(ell_err, 2)},
          "sclera": [int(v_) for v_ in sc], "room": {"left": round(float(r_s[180] - (ir + (c[0] - icx))), 1), "right": round(float(r_s[0] - (ir - (c[0] - icx))), 1), "down": round(float(r_s[90] - (ir - (c[1] - icy))), 1), "up": round(float(r_s[270] - (ir + (c[1] - icy))), 1)}}
    eye_out.append(eo)
    print(f"{E['name']}: iris c {icx:.1f},{icy:.1f} r {ir:.1f} ({ok.sum()} pts, rms {eo['iris']['fit_rms']}), interior r {r_s.min():.1f}-{r_s.max():.1f} ({valid.sum()}/360 angles read, the ellipse fits them within {ell_err:.2f} px), sclera {eo['sclera']}, hidden {hidden} px, room {eo['room']}")
    E["mask"] = eye_mask; E["out"] = eo; E["iris_im"] = iris_im
report["eyes"] = eye_out

# ---------- the sheets ----------
save_mask(body_mask, OUT / "demo2_girl_body_mask.png"); save_mask(arm_mask, OUT / "demo2_girl_arm_mask.png"); save_mask(patch_mask, OUT / "demo2_girl_patch_mask.png")
report["sheets"] = {p.name: p.stat().st_size for p in sorted(OUT.glob("*.png"))}
report["bitmap"] = [W, H]
(OUT / "rig.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
print("sheets:", {k: f"{v / 1024:.1f}K" for k, v in report["sheets"].items()})

# ---------- a composite check: the layers at rest must give the painting back ----------
def over(dst, src, m):
    """src over dst where m (0..1) says how much of src; both RGBA float, premultiplied by their own alpha for the blend"""
    a_s = src[..., 3:4] / 255 * m[..., None]; a_d = dst[..., 3:4] / 255
    out_a = a_s + a_d * (1 - a_s)
    out_rgb = (src[..., :3] * a_s + dst[..., :3] * a_d * (1 - a_s)) / np.maximum(out_a, 1e-6)
    return np.concatenate([out_rgb, out_a * 255], axis=-1)
comp = A * np.concatenate([np.ones((H, W, 3)), body_mask[..., None]], axis=-1) * 1.0
comp = np.concatenate([A[..., :3], (alpha * body_mask)[..., None]], axis=-1)
for E in EYES:   # an eye = (the window, the sclera disc, the iris) composited as a group, THEN masked by the interior (as CSS masks the element)
    eo = E["out"]; grp = A.copy()
    disc = (np.hypot(XX - eo["iris"]["cx"], YY - eo["iris"]["cy"]) <= eo["iris"]["r"] + 1).astype(np.float32)
    fill = np.zeros((H, W, 4), np.float32); fill[..., :3] = eo["sclera"]; fill[..., 3] = 255; grp = over(grp, fill, disc)
    ir_ = np.asarray(E["iris_im"]).astype(np.float32); ox, oy, sz, _ = eo["iris_box"]
    lay = np.zeros((H, W, 4), np.float32); lay[oy:oy + sz, ox:ox + sz] = ir_; grp = over(grp, lay, np.ones((H, W)))
    comp = over(comp, grp, E["mask"])
comp = over(comp, A, arm_mask); comp = over(comp, A, patch_mask)
diff = np.abs(comp[..., :3] - A[..., :3]).max(axis=2) * (alpha > 0) + np.abs(comp[..., 3] - alpha)
print("rest composite vs the painting: max diff %.1f levels, %d px over 8, %d px over 24" % (diff.max(), (diff > 8).sum(), (diff > 24).sum()))
report["rest_diff"] = {"max": round(float(diff.max()), 1), "over8": int((diff > 8).sum()), "over24": int((diff > 24).sum())}
(OUT / "rig.json").write_text(json.dumps(report, indent=1), encoding="utf-8")

if DEBUG:
    def big(name, box, k, draw_fn=None):
        bg = Image.new("RGBA", im.size, (0, 160, 0, 255)); c = Image.alpha_composite(bg, im).crop(box).resize(((box[2] - box[0]) * k, (box[3] - box[1]) * k), Image.NEAREST)
        if draw_fn: draw_fn(ImageDraw.Draw(c), lambda x, y: ((x - box[0]) * k, (y - box[1]) * k))
        c.save(DEBUG / f"{name}.png")
    def elbow(d, T):
        d.ellipse([T(cx - R_keep, cy - R_keep), T(cx + R_keep, cy + R_keep)], outline=(0, 255, 255, 255), width=2)
        d.line([T(cx - n[0] * 90, cy - n[1] * 90), T(cx + n[0] * 90, cy + n[1] * 90)], fill=(255, 0, 255, 255), width=2)
        d.line([T(cx, cy), T(cx + u[0] * 120, cy + u[1] * 120)], fill=(255, 255, 255, 255), width=2)
        d.ellipse([T(T_[0] - 3, T_[1] - 3), T(T_[0] + 3, T_[1] + 3)], fill=(255, 255, 0, 255))
        for q in sil: d.point(T(q[0] + 0.5, q[1] + 0.5), fill=(255, 255, 0, 255))
        d.line([T(*p) for p in POLY] + [T(*POLY[0])], fill=(0, 0, 255, 255), width=2)
        d.ellipse([T(cx - 3, cy - 3), T(cx + 3, cy + 3)], fill=(255, 0, 0, 255))
    T_ = report["elbow"]["B"]
    big("dbg_elbow", (640, 400, 1000, 720), 3, elbow)
    # the masks as colour overlays
    ov = np.zeros((H, W, 4), np.uint8)
    ov[..., 0] = (hole * 255).astype(np.uint8); ov[..., 3] = (hole * 160).astype(np.uint8)                    # red = the body's hole
    o2 = np.zeros((H, W, 4), np.uint8); o2[..., 1] = 255; o2[..., 3] = (arm_mask * 110).astype(np.uint8)   # green = the arm layer
    o3 = np.zeros((H, W, 4), np.uint8); o3[..., 2] = 255; o3[..., 3] = (patch_mask * 200).astype(np.uint8)   # blue = the patch
    base = Image.alpha_composite(Image.new("RGBA", im.size, (40, 40, 40, 255)), im)
    for o in (ov, o2, o3): base = Image.alpha_composite(base, Image.fromarray(o, "RGBA"))
    base.crop((640, 400, 1000, 720)).resize((1080, 960), Image.NEAREST).save(DEBUG / "dbg_masks.png")
    for E in EYES:
        eo = E["out"]; x0, y0, x1, y1 = E["box"]
        def eye(d, T, eo=eo, E=E):
            d.ellipse([T(eo["iris"]["cx"] - eo["iris"]["r"], eo["iris"]["cy"] - eo["iris"]["r"]), T(eo["iris"]["cx"] + eo["iris"]["r"], eo["iris"]["cy"] + eo["iris"]["r"])], outline=(255, 255, 0, 255), width=1)
            m = E["mask"]; e = boundary(m > 0.5); ys, xs = np.nonzero(e)
            for x, y in zip(xs, ys): d.point(T(x + 0.5, y + 0.5), fill=(0, 255, 255, 255))
        big("dbg_" + E["name"], (x0 - 8, y0 - 8, x1 + 8, y1 + 8), 7, eye)
        E["iris_im"].resize((E["iris_im"].width * 7, E["iris_im"].height * 7), Image.NEAREST).save(DEBUG / f"dbg_{E['name']}_iris.png")
    # the composite at rest, and with the arm lifted 9 degrees + the eyes slid (8, 4) px, as the page would show (bitmap px)
    Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8), "RGBA").crop((400, 150, 1000, 720)).save(DEBUG / "dbg_rest.png")
    print("debug overlays in", DEBUG)
