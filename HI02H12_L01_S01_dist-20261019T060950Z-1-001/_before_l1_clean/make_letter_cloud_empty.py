"""[l1-cloud] (2026-11-04) L1's memory cloud WITHOUT the grandfather — the patch that fades in over him at the letter's moment, so he
disappears from the SAME cloud (its rim, its pastel glow, the hearts and the bushes all stay) and the letter grows in it.

usage: python -I -X utf8 make_letter_cloud_empty.py [--debug <dir>]
reads   letter_assets/img_letter_cloud_grandpa.webp   the cloud with the grandfather (820x820 RGBA; the user's PNG of 2026-10-26)
writes  letter_assets/img_letter_cloud_empty.webp     an RGBA PATCH, lossless: inside his outline (grown a few px) the cloud's own
                                                      background painted in, opaque; outside it alpha 0 (its RGB there = the cloud's,
                                                      so the soft edge of the patch shows no seam). Laid over the grandpa cloud in the
                                                      same box it IS the empty cloud; faded in, only he goes.
How: his figure = the WARM pixels (R - G > WARM: his hair, skin, shirt, sleeves and vest are all >= ~20; the cloud's cream, yellow,
greens and mist are ~0) inside a generous outline traced around him (FIG_BOUND, image px; it keeps the three pink hearts — also warm
— outside), closed (CLOSE px: the vest's speckles where it dissolves into the mist join up), its holes filled (the glasses, the eyes,
the pale collar), grown GROW px (his anti-aliased edge), and kept inside the cloud's opaque body (alpha >= 250, eroded 3 px) so the
rim is never touched. The fill: a harmonic (Laplace) fill from the background around him — multigrid Jacobi, numpy only — which
continues the cream glow over his head, the bushes' green behind his shoulders and the white mist under him; plus the background's
own grain, its strength filled in the same way from a ring around him. The patch's alpha = 1 inside, falling to 0 over FEATHER px
outside, where its RGB equals the cloud's (so the feather is invisible).
Also writes letter_assets/img_letter_blur_t.webp — the zoom's backdrop for the room that now STAYS on screen (792:1245, the girl
thinking; the pensive picture is gone from the page): made exactly as img_letter_blur_p was from 792:1249 (its render blurred,
Gaussian 7.5 px, 90 % over white, 1280x720, WebP q90 — that recipe re-makes blur_p within WebP noise: mean 0.8 / 765).
--debug writes the mask overlay, the empty cloud on grey and the two side by side."""
import sys, pathlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
LA = HERE / "letter_assets"
DBG = pathlib.Path(sys.argv[sys.argv.index("--debug") + 1]) if "--debug" in sys.argv else None
WARM, CLOSE, GROW, FEATHER = 12, 9, 5, 4
# a generous outline around him (image px, clockwise from the bottom left): left of the left sleeve, over the left shoulder, past the
# ear, round the hair's strands, down between the right ear and the right pink heart (x >= 607), out round the right sleeve, and under
# him through the mist (the cloud's own edge clips it there)
FIG_BOUND = [(100, 760), (100, 660), (105, 600), (113, 584), (119, 576), (124, 568), (130, 560), (137, 552), (144, 544), (151, 536),
             (158, 528), (166, 520), (174, 512), (184, 504), (198, 496), (218, 488), (236, 478),   # 12 px outside his left sleeve's outline (measured
             # row by row: x 248 at y 480 ... 125 at y 584), so the bushes' small white heart (x 107..140, y 523..550) stays out
             (242, 420), (240, 330), (262, 280), (280, 238), (300, 200),
             (330, 172), (380, 155), (440, 152), (500, 165), (548, 188), (588, 220), (614, 254), (630, 300), (632, 350), (622, 396),
             (600, 414), (596, 450), (596, 492), (612, 512), (642, 545), (662, 600), (668, 660), (655, 760)]

src = Image.open(LA / "img_letter_cloud_grandpa.webp").convert("RGBA")
A = np.asarray(src).astype(np.float64); H, W = A.shape[:2]
rgb, alpha = A[..., :3], A[..., 3]

def binimg(m): return Image.fromarray((m * 255).astype(np.uint8))
def dilate(m, px): return np.asarray(binimg(m).filter(ImageFilter.MaxFilter(2 * px + 1))) > 127
def erode(m, px): return np.asarray(binimg(m).filter(ImageFilter.MinFilter(2 * px + 1))) > 127
def fill_holes(m):
    """everything not reachable from the border through ~m is part of m"""
    im = binimg(~m).copy()   # 255 = open
    pad = Image.new("L", (W + 2, H + 2), 255); pad.paste(im, (1, 1))
    ImageDraw.floodfill(pad, (0, 0), 128)
    reached = np.asarray(pad)[1:-1, 1:-1] == 128
    return ~reached

# ---- his figure
bound = Image.new("L", (W, H), 0); ImageDraw.Draw(bound).polygon(FIG_BOUND, fill=255); bound = np.asarray(bound) > 127
body = erode(alpha >= 250, 3)                                     # the cloud's opaque body, its rim left alone
warm = np.asarray(Image.fromarray(np.clip(rgb[..., 0] - rgb[..., 1] + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(float) - 128 > WARM
fig = warm & bound & body
fig = erode(dilate(fig, CLOSE), CLOSE)                            # closing: the speckles and the thin gaps join up
fig = fill_holes(fig) & bound & body                              # the glasses, the eyes, the pale collar
mask = dilate(fig, GROW) & bound & body                           # his anti-aliased edge
print(f"figure {int(fig.sum())} px, mask {int(mask.sum())} px, bbox x {np.nonzero(mask.any(0))[0][[0, -1]]} y {np.nonzero(mask.any(1))[0][[0, -1]]}")

# ---- harmonic fill (multigrid Jacobi): unknown = mask, known = the rest of the cloud's body
def harmonic(img, unknown, iters=(400, 200, 120, 80, 60, 50, 40, 40, 40)):
    known = ~unknown
    pyr = [(img * known[..., None], known.astype(np.float64))]
    while min(pyr[-1][1].shape) > 12:
        I, Wt = pyr[-1]; h, w = Wt.shape; h2, w2 = (h + 1) // 2, (w + 1) // 2
        Ip = np.zeros((h2 * 2, w2 * 2, I.shape[2])); Ip[:h, :w] = I; Wp = np.zeros((h2 * 2, w2 * 2)); Wp[:h, :w] = Wt
        pyr.append((Ip.reshape(h2, 2, w2, 2, -1).sum(axis=(1, 3)), Wp.reshape(h2, 2, w2, 2).sum(axis=(1, 3))))
    sol = None
    for lv in range(len(pyr) - 1, -1, -1):
        I, Wt = pyr[lv]; h, w = Wt.shape
        fixed = Wt > (0.999 if lv == 0 else 0.5)                   # the finest level: the true pixels; coarser: mostly-known cells
        val = np.where(Wt[..., None] > 0, I / np.maximum(Wt, 1e-9)[..., None], 0.0)
        x = np.repeat(np.repeat(sol, 2, axis=0), 2, axis=1)[:h, :w] if sol is not None else np.where(fixed[..., None], val, val[fixed].mean(axis=0))
        x = np.where(fixed[..., None], val, x)
        for _ in range(iters[min(len(iters) - 1, len(pyr) - 1 - lv)] if lv else iters[0]):
            p = np.pad(x, ((1, 1), (1, 1), (0, 0)), mode="edge")
            nb = (p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]) / 4
            x = np.where(fixed[..., None], val, nb)
        sol = x
    return sol

region = mask | body                                              # outside the body the fill has nothing to say
fillable = mask.copy()
F = harmonic(np.where(region[..., None], rgb, 255.0), fillable)
# the grain: the background's residual against a 2 px blur, its local strength (std over 9 px) filled in harmonically too
blur = np.asarray(Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float64)
res2 = ((rgb - blur) ** 2).mean(axis=2)
def boxmean(m, r):   # the mean over a (2r+1)^2 window (edges clamped), numpy only
    p = np.pad(m, r, mode="edge"); c = np.cumsum(np.cumsum(np.pad(p, ((1, 0), (1, 0))), axis=0), axis=1); k = 2 * r + 1
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)
loc = np.sqrt(np.maximum(boxmean(np.clip(res2, 0, 255 ** 2 / 64), 4), 0))   # (cumsum round-off can dip a hair under 0)
ring = dilate(mask, 12) & ~dilate(mask, 2) & body
sig = harmonic(np.where(ring[..., None], loc[..., None], 0.0), mask | ~(ring | mask))[..., 0]
rng = np.random.default_rng(20261104)
noise = rng.normal(0, 1, (H, W, 1)) * np.array([1.0, 0.85, 1.6])   # the bushes' grain is strongest in blue (measured 2.9 / 2.4 / 5.5)
noise = np.asarray(Image.fromarray(np.clip(noise * 40 + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float64) - 128
noise = noise / max(1e-6, noise[mask].std()) * 0.8               # unit-ish, a touch under the measured level
F = np.clip(F + noise * sig[..., None], 0, 255)

# ---- the patch: the fill inside the mask; alpha 1 there, feathered to 0 outside over FEATHER px (RGB there = the cloud's own)
out_rgb = np.where(mask[..., None], F, rgb)
feat = np.asarray(binimg(mask).filter(ImageFilter.MaxFilter(2 * FEATHER + 1)).filter(ImageFilter.GaussianBlur(FEATHER / 2))).astype(np.float64) / 255
feat = np.where(mask, 1.0, np.minimum(feat, 1.0)) * body
patch = np.dstack([np.clip(np.round(out_rgb), 0, 255), np.round(feat * 255)]).astype(np.uint8)
im = Image.fromarray(patch, "RGBA")
im.save(LA / "img_letter_cloud_empty.webp", "WEBP", lossless=True, quality=100, method=6, exact=True)   # exact: keep the RGB under alpha 0 too
back = np.asarray(Image.open(LA / "img_letter_cloud_empty.webp").convert("RGBA")).astype(int)
assert np.abs(back - patch.astype(int)).max() == 0, "lossless round trip"
print("img_letter_cloud_empty.webp", (LA / "img_letter_cloud_empty.webp").stat().st_size, "B (lossless, round trip exact)")

# ---- the zoom's backdrop for the thinking room (792:1245's render, the recipe of img_letter_blur_p / img_stamp_final_blur)
import io
ren = Image.open(LA / "fig_792-1245_render.png").convert("RGB"); assert ren.size == (1280, 720), ren.size
bl = np.clip(np.round(0.9 * np.asarray(ren.filter(ImageFilter.GaussianBlur(7.5))).astype(float) + 0.1 * 255), 0, 255).astype("uint8")
buf = io.BytesIO(); Image.fromarray(bl).save(buf, "WEBP", quality=90, method=6); (LA / "img_letter_blur_t.webp").write_bytes(buf.getvalue())
print("img_letter_blur_t.webp", len(buf.getvalue()), "B")

if DBG:
    DBG.mkdir(parents=True, exist_ok=True)
    grey = Image.new("RGBA", (W, H), (150, 170, 190, 255))
    g1 = grey.copy(); g1.alpha_composite(src)
    g2 = g1.copy(); g2.alpha_composite(im)                         # the patch over the grandpa cloud = what the page shows at the end
    ov = np.asarray(g1.convert("RGB")).astype(np.float64)
    ov[mask] = ov[mask] * 0.5 + np.array([255, 0, 0]) * 0.5
    edge = mask & ~erode(mask, 1); ov[edge] = [255, 0, 0]
    bnd = Image.new("L", (W, H), 0); ImageDraw.Draw(bnd).line(FIG_BOUND + [FIG_BOUND[0]], fill=255, width=1)
    ov[np.asarray(bnd) > 0] = [0, 0, 255]
    Image.fromarray(ov.astype(np.uint8)).save(DBG / "cloud_mask.png")
    g2.convert("RGB").save(DBG / "cloud_empty_on_grey.png")
    pair = Image.new("RGB", (W * 2, H)); pair.paste(g1.convert("RGB"), (0, 0)); pair.paste(g2.convert("RGB"), (W, 0)); pair.save(DBG / "cloud_pair.png")
