"""[l1-clean] (2026-11-04) L1's memory cloud made CLEAN WHITE — the patch that fades in over the grandfather's picture at the letter's
moment, so the same cloud (its outline, its soft pink rim) is left fully clean and white BEFORE the letter grows in it.

usage: python -I -X utf8 make_letter_cloud_clean.py [--debug <dir>]
reads   letter_assets/img_letter_cloud_grandpa.webp   the cloud with the grandfather (820x820 RGBA; the user's PNG of 2026-10-26)
        letter_assets/fig_792-1245_render.png         Figma 792:1245's render (the room that stays on screen)
writes  letter_assets/img_letter_cloud_clean.webp     an RGBA PATCH, lossless: the cloud's own mist white (CLEAN, the median of the
                                                      outer 8 px of its opaque body) over the whole of that body (alpha >= 250: the
                                                      grandfather, his glow, the hearts, the bushes); its alpha ramps 1 -> 0 over
                                                      the cloud's alpha 250 -> 240 and is 0 on the rim itself (alpha < 240, the pink
                                                      fringe: measured free of any of the picture's colours). Laid over the grandfather's
                                                      cloud in the same box it IS that cloud, clean white; faded in, his picture goes and
                                                      the rim never changes (no second cloud over the first: the rim's density never
                                                      doubles).
        letter_assets/img_letter_blur_t.webp          the zoom's backdrop for 792:1245's room: its render blurred (Gaussian 7.5 px), 90 %
                                                      over white, 1280x720, WebP q90 — img_letter_blur_p's recipe (it re-makes blur_p
                                                      within WebP noise: mean 0.8 / 765)
--debug writes the clean cloud and the grandfather's cloud on the room's wall colour, side by side.
(It replaces [l1-cloud]'s make_letter_cloud_empty.py — the cloud with only the grandfather painted out, his pastel backdrop kept —
which the user found "not fully clean white"; that script and its patch are in ../_before_l1_clean/.)"""
import sys, io, pathlib
import numpy as np
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
LA = HERE / "letter_assets"
DBG = pathlib.Path(sys.argv[sys.argv.index("--debug") + 1]) if "--debug" in sys.argv else None

src = Image.open(LA / "img_letter_cloud_grandpa.webp").convert("RGBA")
A = np.asarray(src).astype(np.float64); rgb, al = A[..., :3], A[..., 3]
body = al >= 250
outer = body & ~(np.asarray(Image.fromarray((body * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(17))) > 127)   # its outer 8 px
CLEAN = np.round(np.median(rgb[outer], axis=0))
print("the cloud's own mist white (the outer 8 px of its body, median):", CLEAN.astype(int).tolist())
pa = np.clip((al - 240) / 10, 0, 1)                         # 1 over the body, 0 on the rim, a ramp over alpha 240..250
patch = np.dstack([np.broadcast_to(CLEAN, rgb.shape), np.round(pa * 255)]).astype(np.uint8)
im = Image.fromarray(patch, "RGBA")
im.save(LA / "img_letter_cloud_clean.webp", "WEBP", lossless=True, quality=100, method=6, exact=True)
back = np.asarray(Image.open(LA / "img_letter_cloud_clean.webp").convert("RGBA")).astype(int)
assert np.abs(back - patch.astype(int)).max() == 0, "lossless round trip"
print("img_letter_cloud_clean.webp", (LA / "img_letter_cloud_clean.webp").stat().st_size, "B (lossless, round trip exact);",
      int((pa >= 1).sum()), "px covered,", int(((pa > 0) & (pa < 1)).sum()), "px in the ramp")

ren = Image.open(LA / "fig_792-1245_render.png").convert("RGB"); assert ren.size == (1280, 720), ren.size
bl = np.clip(np.round(0.9 * np.asarray(ren.filter(ImageFilter.GaussianBlur(7.5))).astype(float) + 0.1 * 255), 0, 255).astype("uint8")
buf = io.BytesIO(); Image.fromarray(bl).save(buf, "WEBP", quality=90, method=6); (LA / "img_letter_blur_t.webp").write_bytes(buf.getvalue())
print("img_letter_blur_t.webp", len(buf.getvalue()), "B")

if DBG:
    DBG.mkdir(parents=True, exist_ok=True)
    wall = Image.new("RGBA", src.size, (238, 214, 196, 255))   # about the room's wall behind the cloud
    a1 = wall.copy(); a1.alpha_composite(src)
    a2 = a1.copy(); a2.alpha_composite(im)
    pair = Image.new("RGB", (src.size[0] * 2, src.size[1])); pair.paste(a1.convert("RGB"), (0, 0)); pair.paste(a2.convert("RGB"), (src.size[0], 0))
    pair.save(DBG / "cloud_clean_pair.png")
