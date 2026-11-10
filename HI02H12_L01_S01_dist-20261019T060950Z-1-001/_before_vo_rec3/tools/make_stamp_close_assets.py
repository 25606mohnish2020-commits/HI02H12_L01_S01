"""[stamp-close] L2's finale assets from Figma 792:1253 (FLN-by-MJ, "G3 guided story question": Pinki at her desk holding up the
sealed letter) and the numbers of the envelope's landing in her hand.

usage: python -I make_stamp_close_assets.py <dir with the frame's downloads> [<stamp_assets dir>]
  the dir holds raw1.png (download_assets rawImages: image 295's fill, 1672x941 — md5 eb12fc22... = get_design_context's
  imgImage295) and export_1253.png (the frame's 1280x720 export).
writes  img_stamp_final_pinki.webp  the fill, LOSSLESS at its native size (the frame draws it cover into 0,-1 1280x721)
        img_stamp_final_blur.webp   the backdrop of the closed envelope, made as L1's img_letter_blur_p was from 792:1249's render:
                                    the render blurred (Gaussian 7.5 px), 90 % over white, 1280x720, WebP q90
        fig_792-1253_render.png     the render (the checks' target)
prints  the envelope in the picture (its outline's four edges fitted, frame px), the drawn envelope (L1's closed layers stacked at
        the 1138x758 box scale, the same fit) and the similarity (scale, rotation, the two centres) that lays the drawing onto the
        picture's envelope — build.py's layout.hand — with both hearts' centres as the cross-check, and the glitter's box
        (layout.envelope = the envelope's outer box + the old finale's margins 12 / 14 / 12 / 12)."""
import sys, io, math, pathlib
import numpy as np
from PIL import Image, ImageFilter

D = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else pathlib.Path(__file__).resolve().parent / "stamp_assets"
LA = pathlib.Path(__file__).resolve().parent / "letter_assets"

# ---- the two pictures + the render
raw = Image.open(D / "raw1.png").convert("RGB"); assert raw.size == (1672, 941), raw.size
buf = io.BytesIO(); raw.save(buf, "WEBP", lossless=True, quality=100, method=6); data = buf.getvalue()
assert np.abs(np.asarray(Image.open(io.BytesIO(data)).convert("RGB")).astype(int) - np.asarray(raw).astype(int)).max() == 0, "lossless round trip"
(OUT / "img_stamp_final_pinki.webp").write_bytes(data); print("img_stamp_final_pinki.webp", len(data), "B (lossless, round trip exact)")
ren = Image.open(D / "export_1253.png").convert("RGB"); assert ren.size == (1280, 720), ren.size
ren.save(OUT / "fig_792-1253_render.png")
m = np.clip(np.round(0.9 * np.asarray(ren.filter(ImageFilter.GaussianBlur(7.5))).astype(float) + 0.1 * 255), 0, 255).astype("uint8")
b2 = io.BytesIO(); Image.fromarray(m).save(b2, "WEBP", quality=90, method=6); (OUT / "img_stamp_final_blur.webp").write_bytes(b2.getvalue())
print("img_stamp_final_blur.webp", len(b2.getvalue()), "B")

def samp(img, p):
    x, y = p; x0, y0 = int(math.floor(x)), int(math.floor(y)); fx, fy = x - x0, y - y0
    if x0 < 0 or y0 < 0 or x0 + 1 >= img.shape[1] or y0 + 1 >= img.shape[0]: return -1e9
    return img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy) + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy
def fit(pts):
    c = pts.mean(0); _, _, vt = np.linalg.svd(pts - c); d = vt[0]
    r = np.abs((pts - c) @ np.array([-d[1], d[0]])); k = r < max(1.0, np.percentile(r, 80))
    c = pts[k].mean(0); _, _, vt = np.linalg.svd(pts[k] - c); return c, vt[0]
def inter(L, a, b):
    (c1, d1), (c2, d2) = L[a], L[b]; t = np.linalg.solve(np.array([d1, -d2]).T, c2 - c1); return c1 + d1 * t[0]
def corners(L): return {"TL": inter(L, "top", "left"), "TR": inter(L, "top", "right"), "BR": inter(L, "right", "bottom"), "BL": inter(L, "bottom", "left")}

# ---- the envelope in the picture (raw px -> frame px): the outline is a thin orange line, the most saturated (R - B) pixel across each edge
S = max(1280 / 1672, 721 / 941); ox, oy = (1280 - 1672 * S) / 2, -1 + (721 - 941 * S) / 2
im = np.asarray(raw).astype(float); sat = im[..., 0] - im[..., 2]
def peak_pts(P, Q, half=6, skip=0.12):
    d = (Q - P) / np.linalg.norm(Q - P); n = np.array([-d[1], d[0]]); Ln = np.linalg.norm(Q - P); pts = []
    for t in np.arange(skip * Ln, (1 - skip) * Ln, 1.0):
        c = P + d * t; pts.append(max(((samp(sat, c + n * o), tuple(c + n * o)) for o in np.arange(-half, half + 0.01, 0.25)))[1])
    return np.array(pts)
TL, TR, BR = np.array([986.75, 209.0]), np.array([1105.0, 165.5]), np.array([1131.0, 244.75])   # rough, read off a 4x crop; the hand hides BL
Lp = {"top": fit(peak_pts(TL, TR)), "right": fit(peak_pts(TR, BR))}
Lp["bottom"] = fit(peak_pts(BR, BR - Lp["top"][1] * 55, skip=0.1))     # its visible right part (the hand covers the rest)
Lp["left"] = fit(peak_pts(TL, TL + Lp["right"][1] * 40, skip=0.1))     # above the hand
pic = {k: np.array([ox + p[0] * S, oy + p[1] * S]) for k, p in corners(Lp).items()}
for k, p in pic.items(): print("picture envelope", k, p.round(2))

# ---- the drawn envelope (L1's layers closed, at the box scale): its outline's centre line, by the profile's top band
base = Image.new("RGBA", (1536, 1024), (0, 0, 0, 0))
for k in ("inner", "body", "flap", "heart"): base.alpha_composite(Image.open(LA / f"img_letter_env_{k}.webp").convert("RGBA"))
bx = np.asarray(base.resize((1138, 758), Image.LANCZOS)).astype(float)
dark = np.where(bx[..., 3] > 200, (bx[..., 0] - bx[..., 2]) * (bx[..., 3] / 255) + (255 - bx[..., 1]) * 0.5, 0)
Q0 = {"TL": np.array([122.2, 239.9]), "TR": np.array([946.2, 48.1]), "BR": np.array([1063.1, 550.3]), "BL": np.array([239.0, 742.1])}   # its silhouette's min-area box
cq = sum(Q0.values()) / 4; Ld = {}
for name, (a, b) in {"top": ("TL", "TR"), "right": ("TR", "BR"), "bottom": ("BR", "BL"), "left": ("BL", "TL")}.items():
    P_, Q_ = Q0[a], Q0[b]; d = (Q_ - P_) / np.linalg.norm(Q_ - P_); n = np.array([-d[1], d[0]]); n = n if (cq - (P_ + Q_) / 2) @ n > 0 else -n
    Ln = np.linalg.norm(Q_ - P_); pts = []
    for t in np.arange(0.15 * Ln, 0.85 * Ln, 2.0):
        c = P_ + d * t; prof = [(o, samp(dark, c + n * o)) for o in np.arange(-4, 22, 0.25)]; vm = max(v for _, v in prof)
        sel = [(o, v) for o, v in prof if v >= 0.7 * vm]; pts.append(c + n * (sum(o * v for o, v in sel) / sum(v for _, v in sel)))
    Ld[name] = fit(np.array(pts))
drw = corners(Ld)
for k, p in drw.items(): print("drawn envelope", k, p.round(2))

# ---- the similarity drawing -> picture (Umeyama on the four corners)
K = ("TL", "TR", "BR", "BL"); X = np.array([drw[k] for k in K]); Y = np.array([pic[k] for k in K]); xm, ym = X.mean(0), Y.mean(0)
U, Sg, Vt = np.linalg.svd((Y - ym).T @ (X - xm)); Dg = np.eye(2); Dg[1, 1] = -1 if np.linalg.det(U @ Vt) < 0 else 1
Rm = U @ Dg @ Vt; s = float(np.trace(np.diag(Sg) @ Dg) / ((X - xm) ** 2).sum()); th = math.degrees(math.atan2(Rm[1, 0], Rm[0, 0]))
res = Y - (s * (Rm @ (X - xm).T).T + ym)
print("hand: c (box px)", xm.round(2), "to (frame px)", ym.round(2), "scale", round(s, 5), "rot", round(th, 3), "deg; corners off by", np.hypot(*res.T).round(2), "px")
red = lambda a: (a[..., 0] > 170) & (a[..., 1] < 110) & (a[..., 2] < 120) & (a[..., 0] - a[..., 1] > 90)
R1 = np.asarray(ren).astype(float); ys, xs = np.nonzero(red(R1[150:200, 785:840])); hp = np.array([xs.mean() + 785, ys.mean() + 150])
hb = np.asarray(Image.open(LA / "img_letter_env_heart.webp").convert("RGBA").resize((1138, 758), Image.LANCZOS)).astype(float)
ys, xs = np.nonzero(red(hb) & (hb[..., 3] > 128)); hd = s * Rm @ (np.array([xs.mean(), ys.mean()]) - xm) + ym
print("hearts: the picture's", hp.round(2), "the drawing's laid on it", hd.round(2), "-> off by", round(float(np.hypot(*(hd - hp))), 2), "px")
P4 = np.array(list(pic.values())); x0, y0 = np.floor(P4.min(0) - 1); x1, y1 = np.ceil(P4.max(0) + 1)
print("glitter box (layout.envelope)", [int(x0 - 12), int(y0 - 14), int(x1 - x0 + 24), int(y1 - y0 + 26)], "= the envelope's outer box", [int(x0), int(y0), int(x1), int(y1)], "+ 12 / 14 / 12 / 12")
