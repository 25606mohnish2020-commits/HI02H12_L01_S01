"""girl_rig_g3.py — [g3-grow] (2026-11-02) the G3 girl's eyes as layers, cut from her own bitmap (g3_assets/img_g3_girl_point.webp,
the frame 716:1262's "image 283", 1024x1536, drawn 218x328 cover) so they can glance at the plants and back (girl_rig.py's eyes —
T3's — on this girl; nothing else of her moves).

Per eye: the bitmap clipped to the eye's INTERIOR (inside the painted outline's inner edge: g3_girl_eye{1,2}_mask.png, a full
1024x1536 sheet, the mask in its alpha), a sclera-coloured cover over the painted iris (g3_girl_fill{1,2}.png: the iris's own painted
pixels, 1 px grown — its rim reaches past any fitted curve where the outline hides it, and a ring of it left uncovered stays behind
as a thin dark arc when the iris moves), and the iris itself (g3_girl_iris{1,2}.png:
the painted iris, its parts under the outline completed from its own radial profile) which slides. Her face is three-quarter, so
each iris is an upright ELLIPSE (T3's were circles): fitted, axis-aligned, to its arc against the white and its rim against the
thin outline on the right, where it is drawn touching the outline. At rest the layers are the
painting. Writes g3_assets/girl_rig/ (+ rig.json: the irises, the interiors' room, the sclera colours, in bitmap px) and, with
--debug <dir>, overlays and the glance's composites. Run: python -I girl_rig_g3.py [--debug <dir>]
"""
import sys, json, pathlib, math
import numpy as np
from PIL import Image, ImageDraw

SCR = pathlib.Path(__file__).resolve().parent
SRC = SCR / "g3_assets" / "img_g3_girl_point.webp"
OUT = SCR / "g3_assets" / "girl_rig"; OUT.mkdir(exist_ok=True)
DEBUG = pathlib.Path(sys.argv[sys.argv.index("--debug") + 1]) if "--debug" in sys.argv else None
if DEBUG: DEBUG.mkdir(parents=True, exist_ok=True)
GAZE = (4.0, 10.0)   # the glance at the plants, bitmap px: down and a little to her left (the plants lie below her eyes, to the right)

im = Image.open(SRC).convert("RGBA"); W, H = im.size
assert (W, H) == (1024, 1536), (W, H)
A = np.asarray(im).astype(np.float32); rgb = A[..., :3]; alpha = A[..., 3]
R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
mx = rgb.max(axis=2); mn = rgb.min(axis=2)
solid = alpha > 128
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
skin = solid & (R > 185) & (G > 120) & (B > 80) & (R - B > 45) & (G < 215)
white = solid & (mn > 205)
dark = solid & (mx < 75)

def box_mask(x0, y0, x1, y1):
    m = np.zeros((H, W), bool); m[y0:y1, x0:x1] = True; return m
def dilate(m, r):
    k = int(math.ceil(r)); out = m.copy()
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            if dx * dx + dy * dy > r * r + 1e-6 or (dx == 0 and dy == 0): continue
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out
def save_mask(m, path):
    """a CSS mask sheet: the mask in the ALPHA channel (Chrome masks by a raster's alpha), white underneath"""
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

# image-left (her right eye, the nearer) and image-right; the iris's rough centre and radius, read off the bitmap
EYES = [{"name": "eye1", "box": (400, 244, 504, 334), "guess": (468.0, 292.0, 22.0)},
        {"name": "eye2", "box": (538, 196, 624, 290), "guess": (591.0, 247.0, 20.0)}]
report = {"bitmap": [W, H], "gaze": list(GAZE), "eyes": []}
for E in EYES:
    x0, y0, x1, y1 = E["box"]; bm = box_mask(x0, y0, x1, y1)
    gx_, gy_, gr = E["guess"]
    # the iris's edge: against the sclera, white pixels next to a non-white, non-skin pixel within 9 px of the guessed circle; on
    # the right, where it meets the thin outline, the last brown pixel of each row (R 35..130, redder than green) before it
    wb = white & bm & dilate(bm & ~white & ~skin, 1.0)
    d0 = np.hypot(XX - gx_, YY - gy_); cand = wb & (np.abs(d0 - gr) < 9)
    cp = np.column_stack(np.nonzero(cand))[:, ::-1].astype(np.float64)
    brown = solid & ~skin & (R >= 35) & (R <= 130) & (R > G)
    rp = []
    for yy in range(int(gy_ - 14), int(gy_ + 15)):
        xs = np.nonzero(brown[yy, int(gx_):x1])[0]
        if len(xs): rp.append((int(gx_) + xs.max() + 0.5, yy + 0.5))
    pts = np.concatenate([cp + 0.5, np.array(rp)], axis=0)
    def fit_ellipse(q):
        """axis-aligned: x^2 + a y^2 + b x + c y + d = 0 -> (cx, cy, rx, ry)"""
        x, y = q[:, 0], q[:, 1]
        M = np.column_stack([y * y, x, y, np.ones_like(x)]); (a, b, c_, d), *_ = np.linalg.lstsq(M, -(x * x), rcond=None)
        cx, cy = -b / 2, -c_ / (2 * a); k = cx * cx + a * cy * cy - d
        return cx, cy, math.sqrt(k), math.sqrt(k / a)
    icx, icy, irx, iry = fit_ellipse(pts)
    for _ in range(3):
        rho = np.hypot((pts[:, 0] - icx) / irx, (pts[:, 1] - icy) / iry); res = np.abs(rho - 1) * (irx + iry) / 2; ok = res < 1.5
        icx, icy, irx, iry = fit_ellipse(pts[ok])
    rs = (np.abs(np.hypot((pts[ok, 0] - icx) / irx, (pts[ok, 1] - icy) / iry) - 1) * (irx + iry) / 2)
    ir = (irx + iry) / 2
    erho = lambda x_, y_: np.hypot((x_ - icx) / irx, (y_ - icy) / iry)   # the iris's elliptical radius (1 on its edge)
    # the eye's interior: from an inner point, along 360 rays, out to the first skin pixel (the outline's outer edge), then back in
    # over the outline to its inner edge; where the iris touches the outline the inner edge is read from an ellipse fitted to the rest
    wy, wx = np.nonzero(white & bm); c = ((wx.mean() + icx) / 2, (wy.mean() + icy) / 2)
    NA = 360; r_in = np.full(NA, np.nan); r_out = np.zeros(NA)
    for k in range(NA):
        th = 2 * math.pi * k / NA; dx, dy = math.cos(th), math.sin(th)
        ro = None
        for t in np.arange(6, 70, 0.5):
            xx, yy = int(round(c[0] + dx * t)), int(round(c[1] + dy * t))
            if skin[yy, xx] or not solid[yy, xx]: ro = t; break
        if ro is None: ro = 69
        r_out[k] = ro
        # back in from the skin: ACROSS the stroke — anything that is neither skin nor white: the black lash line above, the thin
        # light-brown line below, the dark red-brown one on the right, and the anti-aliasing round them — to the first light pixel
        # (the white's own edge). A reading only where that walk crossed no part of the iris: a ray through the iris walks on
        # across it to the white on its far side (that is the iris's own rim, not the opening's edge)
        ri = None; seen = False; thru = False
        for t in np.arange(ro - 0.5, 3, -0.5):
            xx, yy = int(round(c[0] + dx * t)), int(round(c[1] + dy * t))
            if erho(c[0] + dx * t, c[1] + dy * t) < 1.0: thru = True
            if skin[yy, xx]: continue
            if mn[yy, xx] > 150:
                if seen: ri = t + 0.5; break
                continue
            seen = True
        if ri is not None and not thru: r_in[k] = ri
    valid = ~np.isnan(r_in); idx = np.arange(NA); ang = 2 * math.pi * idx / NA
    vx, vy = c[0] + np.cos(ang[valid]) * r_in[valid], c[1] + np.sin(ang[valid]) * r_in[valid]
    M = np.column_stack([vx * vx, vx * vy, vy * vy, vx, vy]); coef, *_ = np.linalg.lstsq(M, -np.ones(len(vx)), rcond=None)
    Aq, Bq, Cq, Dq, Eq = coef
    def ell_r(th):
        dx, dy = math.cos(th), math.sin(th); xa, ya = c
        qa = Aq * dx * dx + Bq * dx * dy + Cq * dy * dy
        qb = 2 * Aq * xa * dx + Bq * (xa * dy + ya * dx) + 2 * Cq * ya * dy + Dq * dx + Eq * dy
        qc = Aq * xa * xa + Bq * xa * ya + Cq * ya * ya + Dq * xa + Eq * ya + 1
        disc = qb * qb - 4 * qa * qc
        if disc < 0: return float("nan")
        ts = [(-qb + sg * math.sqrt(disc)) / (2 * qa) for sg in (1, -1)]; ts = [t for t in ts if t > 0]
        return min(ts) if ts else float("nan")
    r_ell = np.array([ell_r(th) for th in ang])
    ell_err = float(np.abs(r_ell[valid] - r_in[valid]).mean())
    # where a ray crosses the iris the edge cannot be read by colour (the iris's own rim and pupil are as dark as the stroke):
    #  - the iris drawn touching a THIN outline (its far rim within 4 px of the skin — her eyes' right sides): the edge is the iris's
    #    far rim + 0.5 px (the iris's ellipse was fitted to that rim)
    #  - the iris running on under the thick lash line (its rim far inside the skin, or past it): the opening's own curve, fitted
    #    to the readings on the white's side (within 0.3 px of them), which runs on smoothly under the lash
    #  never within 1.5 px of the skin
    def iris_far(th):
        dx, dy = math.cos(th), math.sin(th); px0, py0 = c[0] - icx, c[1] - icy
        qa = (dx / irx) ** 2 + (dy / iry) ** 2; qb = 2 * (px0 * dx / irx ** 2 + py0 * dy / iry ** 2); qc = (px0 / irx) ** 2 + (py0 / iry) ** 2 - 1
        disc = qb * qb - 4 * qa * qc
        if disc < 0: return float("inf")
        t2 = (-qb + math.sqrt(disc)) / (2 * qa)
        return t2 if t2 > 0 else float("inf")
    r_if = np.array([iris_far(th) for th in ang])
    touch = np.isfinite(r_if) & (r_out - r_if <= 4.0) & (r_out - r_if >= 0.5)
    guess = np.where(touch, r_if + 0.5, np.where(np.isfinite(r_ell), r_ell, r_out - 3.0))
    r_full = np.where(valid, r_in, np.minimum(guess, r_out - 1.5))
    r_full = np.minimum(r_full, r_out - 1.5)
    kern = np.ones(13) / 13; r_s = np.convolve(np.concatenate([r_full[-6:], r_full, r_full[:6]]), kern, mode="valid")
    r_s = r_s - 0.6   # eroded a touch: the iris's sliding edge is clipped a hair before the outline, never over it
    S = 4; poly = [((c[0] + math.cos(2 * math.pi * k / NA) * r_s[k]) * S, (c[1] + math.sin(2 * math.pi * k / NA) * r_s[k]) * S) for k in range(NA)]
    bx0, by0 = x0 - 12, y0 - 12; bw, bh = (x1 - x0) + 24, (y1 - y0) + 24
    sm = Image.new("L", (bw * S, bh * S), 0); ImageDraw.Draw(sm).polygon([(px_ - bx0 * S, py_ - by0 * S) for px_, py_ in poly], fill=255)
    sm = sm.resize((bw, bh), Image.BOX)
    eye_mask = np.zeros((H, W), np.float32); eye_mask[by0:by0 + bh, bx0:bx0 + bw] = np.asarray(sm).astype(np.float32) / 255.0
    sc = np.median(rgb[white & bm], axis=0)
    # the iris: the painted disc, completed (hidden pixels: the mean colour of the visible ones at the same radius, shines left out)
    rad = int(math.ceil(max(irx, iry) + 3)); ox, oy = int(math.floor(icx)) - rad, int(math.floor(icy)) - rad; sz = 2 * rad + 1
    iris = np.zeros((sz, sz, 4), np.float32)
    gy, gx = np.mgrid[0:sz, 0:sz]; fx, fy = ox + gx, oy + gy
    rr = erho(fx + 0.0, fy + 0.0) * ir          # the elliptical radius in (mean) px
    inside = rr <= ir + 2.2
    shine = white[fy, fx]
    vis = inside & (eye_mask[fy, fx] > 0) & solid[fy, fx]   # painted wherever the interior reaches at all (its anti-aliased rim too)
    cols = rgb[fy, fx]
    prof_r = np.arange(0, ir + 2, 0.5); prof = np.zeros((len(prof_r), 3))
    for i, pr in enumerate(prof_r):
        sel = vis & ~shine & (np.abs(rr - pr) <= 0.75)
        if sel.sum() < 3: sel = vis & ~shine & (np.abs(rr - pr) <= 1.5)
        prof[i] = cols[sel].mean(axis=0) if sel.sum() else (prof[i - 1] if i else sc)
    synth = np.stack([np.interp(rr, prof_r, prof[:, ch]) for ch in range(3)], axis=-1)
    iris[..., :3] = np.where(vis[..., None], cols, synth)
    # the painted iris: the ellipse and every non-white, non-skin pixel of the interior near it, grown 1 px — the cover hides all
    # of it, and the iris layer is opaque over all of it (so at rest the cover never shows); beyond it the layer fades out over a
    # pixel inside the ellipse's rim and is empty outside the interior (else the outline / skin round it would travel with it)
    # the painted iris = the pixels of the interior (mask > .5) within 4 px of the fitted ellipse that are not the white and not
    # skin, AND that the iris's centre sees without crossing white outside its core: so the lash line's grey anti-aliasing beyond
    # the white sliver at her eyes' top right is not taken (carried with the iris it rode down as a grey streak), nor any of the
    # outline (covered it would turn white as the iris leaves); the highlight, in the core, is the iris's own. The anti-aliased
    # ring on the white's side (off-white, mn <= 235) within 2 px goes with it (it is the iris's edge).
    em = eye_mask[fy, fx]
    core = rr <= ir - 1
    lc_x, lc_y = icx - ox, icy - oy
    def seen_from_centre(mask_ok, blockers):
        out = np.zeros(mask_ok.shape, bool)
        for yy, xx in zip(*np.nonzero(mask_ok)):
            n = int(math.ceil(math.hypot(xx - lc_x, yy - lc_y) * 2)) + 1; ts = np.linspace(0, 1, n)[:-1]
            px_ = np.clip(np.round(lc_x + (xx - lc_x) * ts).astype(int), 0, sz - 1); py_ = np.clip(np.round(lc_y + (yy - lc_y) * ts).astype(int), 0, sz - 1)
            out[yy, xx] = not blockers[py_, px_].any()
        return out
    sclera_px = white[fy, fx] & ~core
    cand_p = (em > 0.5) & solid[fy, fx] & ~skin[fy, fx] & (((rr <= ir + 4) & ~white[fy, fx]) | ((rr <= ir + 2) & (mn[fy, fx] <= 235)) | core)
    pin = seen_from_centre(cand_p, sclera_px) | (core & (em > 0.5))
    # the layer = the painted iris + its continuation where it runs on UNDER the outline / lid: a pixel of the fitted ellipse (+1.5)
    # outside the painted iris joins only if the straight path to it from the iris's centre crosses no white outside the painted
    # iris (where a sliver of white lies between the iris and the outline — her eye2's top right — the fit runs past the iris:
    # taking what lies beyond the sliver would carry a strip of the outline down with the iris). On the interior it keeps its
    # painted colour (so at rest it is the painting); outside it, the iris's own radial profile
    wsl = white[fy, fx] & ~pin
    keep = seen_from_centre((rr <= ir + 1.5) & ~pin, wsl)
    region = pin | keep
    a_ell = np.clip(ir + 1.0 - rr, 0, 1)
    iris[..., 3] = np.where(pin, 1.0, np.where(keep, np.minimum(a_ell * 2, 1.0), 0.0)) * 255
    iris[..., :3] = np.where((region & (em > 0) & solid[fy, fx])[..., None], cols, synth)
    fill = np.zeros((sz, sz, 4), np.float32); fill[..., :3] = np.median(rgb[white & bm], axis=0); fill[..., 3] = pin * 255.0
    iris_im = Image.fromarray(np.clip(np.round(iris), 0, 255).astype(np.uint8), "RGBA")
    iris_im.save(OUT / f"g3_girl_iris{E['name'][-1]}.png", optimize=True)
    Image.fromarray(np.clip(np.round(fill), 0, 255).astype(np.uint8), "RGBA").save(OUT / f"g3_girl_fill{E['name'][-1]}.png", optimize=True)
    save_mask(eye_mask, OUT / f"g3_girl_{E['name']}_mask.png")
    hidden = int((inside & ~vis).sum())
    # how much of the iris the glance leaves in the opening (its area inside the interior, at rest and moved)
    def shown(dx, dy):
        lay = np.zeros((H, W), np.float32); a_ = iris[..., 3] / 255.0
        yy0, xx0 = int(round(oy + dy)), int(round(ox + dx)); lay[yy0:yy0 + sz, xx0:xx0 + sz] = a_
        return float((lay * eye_mask).sum())
    eo = {"name": E["name"], "iris": {"cx": round(float(icx), 2), "cy": round(float(icy), 2), "rx": round(float(irx), 2), "ry": round(float(iry), 2), "r": round(float(ir), 2), "fit_pts": int(ok.sum()), "fit_rms": round(float(np.sqrt((rs ** 2).mean())), 2), "hidden_px": hidden},
          "iris_box": [ox, oy, sz, sz], "centre": [round(c[0], 1), round(c[1], 1)],
          "interior_r": {"min": round(float(r_s.min()), 1), "max": round(float(r_s.max()), 1), "valid_angles": int(valid.sum()), "ellipse_fit_err": round(ell_err, 2)},
          "sclera": [int(v_) for v_ in sc], "iris_shown": {"rest": round(shown(0, 0)), "glance": round(shown(*GAZE))}}
    report["eyes"].append(eo)
    print(f"{E['name']}: iris c {icx:.1f},{icy:.1f} rx {irx:.1f} ry {iry:.1f} ({ok.sum()} pts, rms {eo['iris']['fit_rms']}), interior r {r_s.min():.1f}-{r_s.max():.1f} ({valid.sum()}/360 angles read, ellipse within {ell_err:.2f} px), sclera {eo['sclera']}, hidden {hidden} px, iris shown {eo['iris_shown']}")
    E["mask"] = eye_mask; E["out"] = eo; E["iris"] = iris; E["fill"] = fill

report["sheets"] = {p.name: p.stat().st_size for p in sorted(OUT.glob("*.png"))}
# ---------- the composite at rest (must give the painting back) and at the glance ----------
def over(dst, src, m):
    a_s = src[..., 3:4] / 255 * m[..., None]; a_d = dst[..., 3:4] / 255
    out_a = a_s + a_d * (1 - a_s)
    out_rgb = (src[..., :3] * a_s + dst[..., :3] * a_d * (1 - a_s)) / np.maximum(out_a, 1e-6)
    return np.concatenate([out_rgb, out_a * 255], axis=-1)
def composite(dx, dy):
    comp = A.copy()
    for E in EYES:
        eo = E["out"]; grp = A.copy()
        ox, oy, sz, _ = eo["iris_box"]
        fl = np.zeros((H, W, 4), np.float32); fl[oy:oy + sz, ox:ox + sz] = E["fill"]; grp = over(grp, fl, np.ones((H, W), np.float32))
        lay = np.zeros((H, W, 4), np.float32)
        lay[int(oy + dy):int(oy + dy) + sz, int(ox + dx):int(ox + dx) + sz] = E["iris"]
        grp = over(grp, lay, np.ones((H, W), np.float32))
        comp = over(comp, grp, E["mask"])
    return comp
rest = composite(0, 0)
diff = np.abs(rest[..., :3] - A[..., :3]).max(axis=2) * (alpha > 0) + np.abs(rest[..., 3] - alpha)
report["rest_diff"] = {"max": round(float(diff.max()), 1), "over8": int((diff > 8).sum()), "over24": int((diff > 24).sum())}
print("rest composite vs the painting:", report["rest_diff"], "| sheets:", {k: f"{v / 1024:.1f}K" for k, v in report["sheets"].items()})
(OUT / "rig.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
if DEBUG:
    gl = composite(*GAZE)
    for nm, (bx0, by0, bx1, by1) in (("eyes", (395, 190, 630, 340)),):
        a = np.concatenate([rest[by0:by1, bx0:bx1, :3], gl[by0:by1, bx0:bx1, :3]], axis=0)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize(((bx1 - bx0) * 3, (by1 - by0) * 2 * 3), Image.LANCZOS).save(DEBUG / f"g3eyes_{nm}.png")
    for E in EYES:
        x0, y0, x1, y1 = E["box"]; big = Image.fromarray(np.clip(A[y0:y1, x0:x1, :3], 0, 255).astype(np.uint8)).resize(((x1 - x0) * 6, (y1 - y0) * 6), Image.NEAREST)
        d = ImageDraw.Draw(big); eo = E["out"]
        T = lambda x, y: ((x - x0) * 6, (y - y0) * 6)
        d.ellipse([T(eo["iris"]["cx"] - eo["iris"]["rx"], eo["iris"]["cy"] - eo["iris"]["ry"]), T(eo["iris"]["cx"] + eo["iris"]["rx"], eo["iris"]["cy"] + eo["iris"]["ry"])], outline=(255, 255, 0), width=2)
        e = boundary(E["mask"] > 0.5); ys, xs = np.nonzero(e)
        for x, y in zip(xs, ys):
            if x0 <= x < x1 and y0 <= y < y1: d.point(T(x + 0.5, y + 0.5), fill=(0, 255, 255))
        big.save(DEBUG / f"g3_{E['name']}_fit.png")
    print("debug in", DEBUG)
