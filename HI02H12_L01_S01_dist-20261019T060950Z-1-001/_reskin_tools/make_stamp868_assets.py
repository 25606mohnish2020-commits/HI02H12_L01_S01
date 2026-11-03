"""[stamp-868] L2's new bitmaps from the Figma frames 868:3 (the angled table + the bird) and 868:17..868:74 (the overhead table of
every round): the frames' own image fills (get_design_context / download_assets, saved under scratchpad/fig868), sized for the
page, into _reskin_tools/stamp_assets/ as img_stamp8_*.webp, plus the reference's whoosh and the frames' renders (the checks).
usage: python -I -X utf8 make_stamp868_assets.py <scratchpad/fig868> <_reskin_tools/stamp_assets> <ref sfx_whoosh.ogg>
Then composes both frames from the written layers (offline, PIL) and prints the mean difference to Figma's renders."""
import sys, json, shutil, pathlib
import numpy as np
from PIL import Image, ImageFilter, ImageSequence
FIG, OUT, WHOOSH = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
C, N3 = FIG / "ctx", FIG / "nodes3"
info = {}

def save(im, name, lossless=True, q=95):
    p = OUT / f"{name}.webp"
    if lossless: im.save(p, "WEBP", lossless=True, quality=100, method=6, exact=True)
    else: im.save(p, "WEBP", quality=q, alpha_quality=100, method=6)
    print(f"{name}.webp {im.size} {im.mode} {p.stat().st_size // 1024} KB"); return p

def cover(sw, sh, x, y, w, h):   # object-fit: cover of a sw x sh picture in the box: its drawn box
    s = max(w / sw, h / sh); dw, dh = sw * s, sh * s
    return [round(x + (w - dw) / 2, 3), round(y + (h - dh) / 2, 3), round(dw, 3), round(dh, 3)]

# ---- 868:3, the angled view: the table + card (its sentence painted in), the postmark (30 %), the tray, the two standing stamps
A = Image.open(C / "a_image293.png").convert("RGB"); aw, ah = A.size
info["a_bg"] = cover(aw, ah, -1, -1, 1282, 722)                     # "image 293": -1,-1 1282x722, cover
s, ox, oy = info["a_bg"][2] / aw, info["a_bg"][0], info["a_bg"][1]
# the painted sentence lifted out: the paper under it filled (a smooth fit of the paper around it + its own fine grain), and the
# original pixels kept as a cut-out layer over it (opaque on the filled pixels, feathered over untouched paper), so the two
# compose to the frame exactly and the cut-out can fade while the live sentence takes its place
a = np.asarray(A).astype(float)
X = lambda x: (x - ox) / s; Y = lambda y: (y - oy) / s
x0, x1, y0, y1 = int(X(343)) - 24, int(X(869)) + 24, int(Y(224)) - 24, int(Y(279)) + 24
reg = a[y0:y1, x0:x1]
# the letters and their anti-aliased fringe: off the paper by more than 6 levels in any channel against a first smooth fit of the
# region (the paper sums ~730; the fringe carries colour)
ink = reg.sum(axis=2) < 700
H, W = reg.shape[:2]; yy, xx = np.mgrid[0:H, 0:W]; u, v = xx / W - .5, yy / H - .5
basis = np.stack([np.ones_like(u), u, v, u * u, u * v, v * v, u ** 3, u * u * v, u * v * v, v ** 3], axis=-1)
far0 = ~np.asarray(Image.fromarray((ink * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9))).astype(bool)
sm0 = np.stack([basis @ np.linalg.lstsq(basis[far0], reg[..., ch][far0], rcond=None)[0] for ch in range(3)], axis=-1)
ink |= (np.abs(reg - sm0) > 6).any(axis=2)
fill = np.asarray(Image.fromarray((ink * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9))).astype(bool)   # + 4 px
ring = ~np.asarray(Image.fromarray((fill * 255).astype("uint8")).filter(ImageFilter.MaxFilter(5))).astype(bool)
smooth = np.zeros_like(reg)
for ch in range(3):
    coef, *_ = np.linalg.lstsq(basis[ring], reg[..., ch][ring], rcond=None); smooth[..., ch] = basis @ coef
rng = np.random.default_rng(868)
grain = rng.normal(0, 0.55, reg.shape[:2])[..., None]                # the paper's own fine grain (0.5-0.56 levels, measured)
out = reg.copy(); out[fill] = (smooth + grain)[fill]
resid = (reg - smooth)[ring]; print("paper fit residual (levels): mean %.2f std %.2f" % (np.abs(resid).mean(), resid.std()))
a2 = a.copy(); a2[y0:y1, x0:x1] = out
save(Image.fromarray(np.clip(a2 + 0.5, 0, 255).astype("uint8")), "img_stamp8_a_bg", lossless=False, q=95)
alpha = np.asarray(Image.fromarray((fill * 255).astype("uint8")).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(2))).astype(float)
alpha = np.maximum(alpha, fill * 255.0)                               # opaque wherever the paper was filled
cut = np.dstack([reg, alpha]).astype("uint8")
save(Image.fromarray(cut, "RGBA"), "img_stamp8_a_text")
info["a_text"] = [round(ox + x0 * s, 3), round(oy + y0 * s, 3), round(W * s, 3), round(H * s, 3)]
# the postmark (30 %): "Object" inset 6.23% 22% 89.06% 71.61% of image 293's box; its picture at 0.92% / 0.79%, 98.25% x 97.04%
bx, by, bw, bh = -1 + .7161 * 1282, -1 + .0623 * 722, 1282 * (1 - .22 - .7161), 722 * (1 - .0623 - .8906)
info["a_post"] = [round(bx + .0092 * bw, 3), round(by + .0079 * bh, 3), round(.9825 * bw, 3), round(.9704 * bh, 3)]
save(Image.open(C / "a_object.png").convert("RGBA"), "img_stamp8_a_post")
tray = Image.open(C / "a_tray.png").convert("RGBA")                   # "stamp-tray 2": centred, top 529.62, 572x191, cover
info["a_tray"] = cover(*tray.size, 354, 529.62, 572, 191)
save(tray.resize((1144, 382), Image.LANCZOS), "img_stamp8_a_tray")
for nm, f, box in (("danda", "a_danda.png", [492.003, 497.343, 99.958, 155.756]), ("quest", "a_quest.png", [682, 491, 107, 170])):
    im = Image.open(C / f).convert("RGBA"); info["a_" + nm] = cover(*im.size, *box)
    st2 = im.resize((round(box[2] * 2), round(box[3] * 2)), Image.LANCZOS); save(st2, "img_stamp8_a_" + nm)
    # its "ठप्पा" glow, baked (2x): a warm gold halo along its outline (the stamp's alpha blurred, sigma 4.5 px, at .95) under a thin bright
    # rim (sigma 1 px, at .95) — CSS's drop-shadow(0 0 9px rgba(255,196,60,.95)) drop-shadow(0 0 2px rgba(255,246,204,.95)), as a picture
    # (an opacity / scale animation of a picture costs the GPU nothing; an animated filter dropped frames as it ended), 24 px all round
    PAD = 24; a = np.zeros((st2.size[1] + 4 * PAD, st2.size[0] + 4 * PAD), float); a[2 * PAD:2 * PAD + st2.size[1], 2 * PAD:2 * PAD + st2.size[0]] = np.asarray(st2.getchannel("A")) / 255.0
    def blur(m, s): return np.asarray(Image.fromarray((m * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(s))).astype(float) / 255.0
    g, w = blur(a, 9) * 0.95, blur(a, 2) * 0.95                                    # (2x: 4.5 and 1 display px)
    al = w + g * (1 - w); rgb = (np.array([255, 246, 204]) * w[..., None] + np.array([255, 196, 60]) * (g * (1 - w))[..., None]) / np.maximum(al, 1e-6)[..., None]
    save(Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.clip(al * 255, 0, 255)]).astype("uint8"), "RGBA"), "img_stamp8_a_glow_" + nm)
    info["a_glow_" + nm] = [round(box[0] - PAD, 3), round(box[1] - PAD, 3), round(box[2] + 2 * PAD, 3), round(box[3] + 2 * PAD, 3)]
# the bird: the frame's GIF fill (486x534, 36 frames of 60 ms) drawn at 0,451 231x254 — cut to the frames' union box, 1.5x the
# drawn size, in a 6 x 6 sheet of 330x378 cells (220x252 drawn: whole px, so a frame step is a whole-px move; a 2-3 px clear edge)
G = Image.open(C / "a_sprite.png"); frames = [f.convert("RGBA") for f in ImageSequence.Iterator(G)]
durs = [f.info.get("duration", 60) for f in ImageSequence.Iterator(Image.open(C / "a_sprite.png"))]
ub = None
for f in frames:
    b = f.getchannel("A").getbbox(); ub = b if ub is None else (min(ub[0], b[0]), min(ub[1], b[1]), max(ub[2], b[2]), max(ub[3], b[3]))
kx, ky = 231 / G.size[0], 254 / G.size[1]
CW, CH, FW, FH = 330, 378, 325, 375; px, py = (CW - FW) / 2, (CH - FH) / 2
sheet = Image.new("RGBA", (6 * CW, 6 * CH), (0, 0, 0, 0))
for i, f in enumerate(frames):
    fr = f.crop(ub).resize((FW, FH), Image.LANCZOS)
    sheet.alpha_composite(fr, (int((i % 6) * CW + px), int((i // 6) * CH + py)))
save(sheet, "img_stamp8_bird", lossless=False, q=90)   # 1.0 MB (lossless: 3.3 MB; q90 differs by 2.6 levels on average, its alpha exact)
info["bird"] = {"n": len(frames), "cols": 6, "ms": durs[0], "cell": [CW / 1.5, CH / 1.5],
                "box": [round(0 + ub[0] * kx - int(px) / 1.5, 3), round(451 + ub[1] * ky - int(py) / 1.5, 3), CW / 1.5, CH / 1.5],
                "union_gif": list(ub), "frame_ms": durs}
info["bird"]["foot"] = [39 + 137 / 2, 682 + 23 / 2]                   # the ellipse's centre (868:7: 39,682 137x23): the bird's feet
# ---- 868:17 .. 868:74, the overhead table (every round): the wood, the card + its postmark (60 %), the tray, the three stamps
wood = Image.open(C / "b_wood.png").convert("RGB"); info["wood"] = cover(*wood.size, 0, -1, 1280, 721)
save(wood, "img_stamp8_wood", lossless=False, q=95)
card = Image.open(C / "b_card.png").convert("RGBA"); info["card"] = cover(*card.size, 220, -30, 840, 630)
save(card, "img_stamp8_card", lossless=False, q=95)
bx, by, bw, bh = 220 + .8143 * 840, -30 + .1444 * 630, 840 * (1 - .1036 - .8143), 630 * (1 - .1444 - .8032)
info["post"] = [round(bx + .0056 * bw, 3), round(by + .0124 * bh, 3), round(.9922 * bw, 3), round(.9837 * bh, 3)]
save(Image.open(C / "b_object.png").convert("RGBA"), "img_stamp8_post")
tr = Image.open(C / "b_tray.png").convert("RGBA"); info["tray"] = cover(*tr.size, 346, 524, 588, 196)
save(tr.resize((1176, 392), Image.LANCZOS), "img_stamp8_tray")
for nm, f in (("danda", "b_danda.png"), ("question", "b_quest.png"), ("comma", "c_comma.png")):
    save(Image.open(C / f).convert("RGBA").resize((256, 256), Image.LANCZOS), "img_stamp8_" + nm)
shutil.copy2(WHOOSH, OUT / "sfx_stamp_whoosh.ogg"); print("sfx_stamp_whoosh.ogg (the reference's, byte for byte)")
for k, f in (("3", "n868-3/export.png"), ("17", "n868-17/export.png"), ("31", "n868-31/shot.png"), ("44", "n868-44/shot.png"), ("59", "n868-59/shot.png"), ("74", "n868-74/shot.png")):
    Image.open(FIG / f).convert("RGB").save(OUT / f"stamp868_{k}_render.png")
(OUT / "stamp868_layout.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in info.items() if k != "bird"}))
print("bird", {k: v for k, v in info["bird"].items() if k != "frame_ms"})

# ---- the check: both frames composed from the written layers, against Figma's renders (outside the text, which the page sets live)
def paste(canvas, name, box, op=1.0):
    im = Image.open(OUT / f"{name}.webp").convert("RGBA")
    x, y, w, h = box; im = im.resize((max(1, round(w)), max(1, round(h))), Image.LANCZOS)
    if op < 1: im.putalpha(Image.fromarray((np.asarray(im.getchannel("A")).astype(float) * op).astype("uint8")))
    canvas.alpha_composite(im, (round(x), round(y)))
cA = Image.new("RGBA", (1280, 720), (242, 247, 250, 255))
paste(cA, "img_stamp8_a_bg", info["a_bg"]); paste(cA, "img_stamp8_a_text", info["a_text"]); paste(cA, "img_stamp8_a_post", info["a_post"], .3)
paste(cA, "img_stamp8_a_tray", info["a_tray"]); paste(cA, "img_stamp8_a_danda", info["a_danda"]); paste(cA, "img_stamp8_a_quest", info["a_quest"])
b0 = info["bird"]["box"]; cell = sheet.crop((0, 0, CW, CH)); cell = cell.resize((round(CW / 1.5), round(CH / 1.5)), Image.LANCZOS); cA.alpha_composite(cell, (round(b0[0]), round(b0[1])))
R3 = Image.open(FIG / "n868-3/export.png").convert("RGB")
d = np.abs(np.asarray(cA.convert("RGB")).astype(int) - np.asarray(R3).astype(int)).sum(axis=2)
print("868:3 composed vs render: mean %.2f / 765 (the tray's and stamps' drop shadow and the bird's ellipse are page CSS, not in this composite)" % d.mean())
cA.convert("RGB").save(FIG / "compose_868_3.png")
