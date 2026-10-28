"""[cover-eyes] measure the painted eyes and brows of the title page's three characters (title_assets/title_char_*.png), in each
picture's own art px, for the live-eyes rig (build.py's [cover-eyes] block, the mtcg2a04l02 reference's [pencil eyes] rig on
three faces). Per eye: the outer edge of its dark outline (an axis-aligned ellipse: centre + semi-axes), the outline's width,
the painted iris and pupil radii, the two shines' places on the iris, and the body's colour above / beside / below the eye
(the eyelids' skin). Per brow: its box and pivot. Also writes, per character, a rig sheet (the body under each brow with the
brow painted out, and each brow alone — the pieces the rig lifts and tilts) and an overlay picture to check the fit by eye.
usage: python -I -X utf8 title_eyes_measure.py <out_dir>   (writes <out_dir>/eyes.json, *_overlay.png, title_assets/title_char_<n>_rig.png)"""
import sys, json, pathlib
import numpy as np
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
CHARS = ("purn", "comma", "question")

def components(mask):
    """4-connected components of a boolean mask: (labels, [(area, cy, cx, y0, x0, y1, x1)])"""
    H, W = mask.shape; lab = np.zeros((H, W), np.int32); n = 0; comps = []
    ys, xs = np.nonzero(mask)
    for y, x in zip(ys, xs):
        if lab[y, x]: continue
        n += 1; stack = [(y, x)]; lab[y, x] = n; pts = []
        while stack:
            cy, cx = stack.pop(); pts.append((cy, cx))
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not lab[ny, nx]: lab[ny, nx] = n; stack.append((ny, nx))
        p = np.array(pts); comps.append((len(p), float(p[:, 0].mean()), float(p[:, 1].mean()), int(p[:, 0].min()), int(p[:, 1].min()), int(p[:, 0].max()) + 1, int(p[:, 1].max()) + 1))
    return lab, comps

res = {}
for name in CHARS:
    im = Image.open(HERE / "title_assets" / f"title_char_{name}.png").convert("RGBA"); W, H = im.size
    A = np.asarray(im).astype(int); rgb, al = A[..., :3], A[..., 3]
    ink = al > 200; ys, xs = np.nonzero(ink); top, bot = ys.min(), ys.max()
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    white = (mn > 212) & ink
    black = (mx < 70) & ink
    brown = (rgb[..., 0] > rgb[..., 2] + 25) & (rgb[..., 0] > rgb[..., 1] + 8) & (mx < 190) & ink & ~black     # the irises, the brows, the outline's warm darks
    dark = (mx < 110) & ink                                                                                      # outline + pupil + dark brows
    # hue / saturation (0..360, 0..1): the body is the character's own hue, saturated; the blush and mouth are pink / red
    r_, g_, b_ = rgb[..., 0] / 255., rgb[..., 1] / 255., rgb[..., 2] / 255.; v_ = np.maximum(np.maximum(r_, g_), b_); d_ = v_ - np.minimum(np.minimum(r_, g_), b_)
    sat = np.where(v_ > 0, d_ / np.maximum(v_, 1e-6), 0)
    hue = np.zeros_like(v_); nz = d_ > 1e-6
    hue[nz & (v_ == r_)] = (60 * ((g_ - b_) / np.maximum(d_, 1e-6)) % 360)[nz & (v_ == r_)]
    hue[nz & (v_ == g_)] = (60 * ((b_ - r_) / np.maximum(d_, 1e-6)) + 120)[nz & (v_ == g_)]
    hue[nz & (v_ == b_)] = (60 * ((r_ - g_) / np.maximum(d_, 1e-6)) + 240)[nz & (v_ == b_)]
    dom = float(np.median(hue[ink & (sat > 0.45) & (v_ > 0.3)]))
    hd = np.abs((hue - dom + 180) % 360 - 180)
    body = ink & (sat > 0.28) & (hd < 55) & ~brown & ~black
    pinkred = ink & (sat > 0.3) & ((hue < 18) | (hue > 325)) & (v_ > 0.45) & ~brown & ~black
    pale = ink & (sat < 0.3) & (v_ > 0.45) & ~brown & ~black                                                     # the sclera with its shading
    print(f'   {name}: body hue {dom:.0f} deg')
    # ---- the pupils: the two largest black blobs in the face's band (the top 45 % of the ink) seed the eyes
    band = black.copy(); band[int(top + 0.45 * (bot - top)):, :] = False
    _, comps = components(band); comps = [c for c in comps if c[0] > 150]; comps.sort(key=lambda c: -c[0])
    pupils = sorted(comps[:2], key=lambda c: c[2])   # left, right
    def flood(seed_y, seed_x, allowed):
        """the 4-connected region of `allowed` pixels around the seed"""
        reg = np.zeros((H, W), bool); stack = [(seed_y, seed_x)]; reg[seed_y, seed_x] = True
        while stack:
            cy_, cx_ = stack.pop()
            for ny, nx in ((cy_ - 1, cx_), (cy_ + 1, cx_), (cy_, cx_ - 1), (cy_, cx_ + 1)):
                if 0 <= ny < H and 0 <= nx < W and allowed[ny, nx] and not reg[ny, nx]: reg[ny, nx] = True; stack.append((ny, nx))
        return reg
    def ext(vals, ang, target):
        d = np.abs((np.array(ang) - target + np.pi) % (2 * np.pi) - np.pi); idx = np.argsort(d)[:max(3, len(vals) // 10)]; return float(np.median(np.array(vals)[idx]))
    eyes = []
    yy, xx = np.ogrid[:H, :W]
    for area, pcy, pcx, *_ in pupils:
        sy, sx = int(round(pcy)), int(round(pcx))
        # the eye: every non-body pixel (white, dark, brown) reachable from the pupil - the pupil, iris, sclera and the dark outline;
        # the body (blue / green / purple) bounds it, so the brows (body between) stay out
        eye = flood(sy, sx, ink & ~body & ~pinkred)
        ey, ex = np.nonzero(eye); ecy, ecx = ey.mean(), ex.mean()
        # the outline's outer edge per ray from the region's centroid, then an axis-aligned ellipse from the extremes (the 10 % of
        # rays nearest each axis: the question mark's lashes, on a few upper-outer angles, cannot pull it)
        pts = []
        for k in range(72):
            th = k / 72 * 2 * np.pi; c, s = np.cos(th), np.sin(th); last = None
            for r in range(1, 400):
                x, y = int(round(ecx + r * c)), int(round(ecy + r * s))
                if not (0 <= x < W and 0 <= y < H): break
                if eye[y, x]: last = r
                elif last is not None and r - last > 3: break
            if last: pts.append((ecx + last * c, ecy + last * s, th))
        X = [q[0] for q in pts]; Y = [q[1] for q in pts]; ang = [q[2] for q in pts]
        xr, xl = ext(X, ang, 0), ext(X, ang, np.pi); yd, yu = ext(Y, ang, np.pi / 2), ext(Y, ang, -np.pi / 2)
        cx, cy, a, b = (xl + xr) / 2, (yu + yd) / 2, (xr - xl) / 2, (yd - yu) / 2
        # the iris: the brown / black pixels of the eye connected to the pupil (closed over the shines with a 9 px window),
        # less the outline ring: the pixels farther than 0.82 of the way to the edge are the ring, not the iris
        inner = (((xx - cx) / a) ** 2 + ((yy - cy) / b) ** 2) < 0.82 ** 2
        from PIL import ImageFilter
        dk = Image.fromarray((((brown | black) & eye & inner) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
        dkm = (np.asarray(dk) > 127) & eye & inner
        if not dkm[sy, sx]:
            dy_, dx_ = np.nonzero(dkm); j = np.argmin((dy_ - sy) ** 2 + (dx_ - sx) ** 2); sy, sx = int(dy_[j]), int(dx_[j])
        iris = flood(sy, sx, dkm); iy, ix = np.nonzero(iris)
        icx, icy = (ix.min() + ix.max() + 1) / 2, (iy.min() + iy.max() + 1) / 2
        iris_r = float(((ix.max() + 1 - ix.min()) + (iy.max() + 1 - iy.min())) / 4)
        # the pupil proper: the largest near-black blob of the iris (the rim's dark brown stays out), closed over its shine notch
        _, pc = components((mx < 35) & iris); pc.sort(key=lambda c: -c[0])
        if pc:
            lab_p, _ = components((mx < 35) & iris); big = max(range(len(_)), key=lambda i: _[i][0]) + 1 if _ else 0
            pm = Image.fromarray(((lab_p == big) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(25)).filter(ImageFilter.MinFilter(25))
            py_, px_ = np.nonzero((np.asarray(pm) > 127) & iris)
            pupil_r = float(((px_.max() + 1 - px_.min()) + (py_.max() + 1 - py_.min())) / 4) if len(px_) else iris_r * 0.55
        else: pupil_r = iris_r * 0.55
        pcx, pcy = icx, icy
        # the outline ring's width: the eye region's extent beyond the sclera along the horizontal axis
        rw = []
        inner = 1 if len(eyes) == 0 else -1   # toward the face's centre: no lashes there (the question mark's are upper-outer), nor below
        for c, s_ in ((inner, 0), (0, 1)):
            run = 0; seen_w = False
            for r in range(1, 400):
                x, y = int(round(ecx + r * c)), int(round(ecy + r * s_))
                if not (0 <= x < W and 0 <= y < H) or not eye[y, x]: break
                if pale[y, x]: seen_w = True; run = 0      # the sclera, its grey shading included
                elif seen_w: run += 1
            if seen_w and run: rw.append(run)
        ring = float(np.median(rw)) if rw else 4.0; ring = float(min(max(ring, 0.04 * a), 0.14 * a))
        print(f'   {name} eye: region {int(eye.sum())} px, centroid ({ecx:.0f},{ecy:.0f}); ellipse c ({cx:.1f},{cy:.1f}) a {a:.1f} b {b:.1f}; iris c ({icx:.0f},{icy:.0f}) r {iris_r:.1f}; pupil r {pupil_r:.1f}')
        disc = ((xx - pcx) ** 2 + (yy - pcy) ** 2) < (iris_r * 0.98) ** 2
        _, sh = components(white & disc & eye); sh = sorted([c for c in sh if c[0] > 6], key=lambda c: -c[0])[:2]
        shines = [[round(c[2] - pcx, 1), round(c[1] - pcy, 1), round(float(np.sqrt(c[0] / np.pi)), 1)] for c in sh]
        # the lids' skin: the body colour just outside the outline, top / middle / bottom thirds (no white, dark, pink)
        ring_m = (((xx - cx) / (a * 1.12)) ** 2 + ((yy - cy) / (b * 1.12)) ** 2 >= 1) & (((xx - cx) / (a * 1.4)) ** 2 + ((yy - cy) / (b * 1.4)) ** 2 <= 1) & ink & ~white & ~dark & ~brown
        pink = (rgb[..., 0] > 200) & (rgb[..., 1] < 170) & (rgb[..., 2] > 120); ring_m &= ~pink
        cols = []
        for lo, hi in ((cy - 1.4 * b, cy - 0.45 * b), (cy - 0.45 * b, cy + 0.45 * b), (cy + 0.45 * b, cy + 1.4 * b)):
            sel = ring_m & (yy >= lo) & (yy < hi); px = rgb[sel]
            cols.append("#%02x%02x%02x" % tuple(int(v) for v in np.median(px, axis=0))) if len(px) else cols.append(None)
        eyes.append({"cx": round(float(cx), 1), "cy": round(float(cy), 1), "a": round(a, 1), "b": round(b, 1), "ring": round(ring, 1),
                     "iris_r": round(iris_r, 1), "pupil_r": round(pupil_r, 1), "shines": shines, "pupil_c": [round(pcx, 1), round(pcy, 1)], "lid": cols})
    # ---- the brows: brown strokes above each eye (within 2.6 b above the outline, 1.7 a wide), dilated 2 px for the cut
    brows = []
    sheet = []
    for e in eyes:
        cx, cy, a, b = e["cx"], e["cy"], e["a"], e["b"]
        box = (int(cx - 1.7 * a), int(cy - 2.8 * b), int(cx + 1.7 * a), int(cy - 1.05 * b))
        sub = np.zeros((H, W), bool); sub[box[1]:box[3], box[0]:box[2]] = True
        _, bc = components((brown | dark) & sub); bc.sort(key=lambda c: -c[0])
        if not bc: brows.append(None); continue
        area, bcy, bcx, y0, x0, y1, x1 = bc[0]
        m = np.zeros((H, W), bool)
        lab, _ = components((brown | dark) & sub)
        # the component's own pixels: re-label to pick the largest
        lab2, comps2 = components((brown | dark) & sub); biggest = max(range(len(comps2)), key=lambda i: comps2[i][0]) + 1
        m = lab2 == biggest
        # dilate 2 px
        for _ in range(2):
            m2 = m.copy(); m2[1:] |= m[:-1]; m2[:-1] |= m[1:]; m2[:, 1:] |= m[:, :-1]; m2[:, :-1] |= m[:, 1:]; m = m2
        y0, x0 = max(0, y0 - 4), max(0, x0 - 4); y1, x1 = min(H, y1 + 4), min(W, x1 + 4)
        brows.append({"box": [x0, y0, x1 - x0, y1 - y0], "c": [round(bcx, 1), round(bcy, 1)]})
        # the brow tile (the brow's pixels alone) and the clean tile (the body with the brow painted out: each column filled by
        # the straight blend of the nearest body pixels above and below the cut)
        tile = A[y0:y1, x0:x1].copy(); mm = m[y0:y1, x0:x1]
        brow = tile.copy(); brow[~mm] = 0
        clean = tile.copy()
        for x in range(x1 - x0):
            col = mm[:, x]
            if not col.any(): continue
            yy_ = np.nonzero(col)[0]; ya, yb = yy_.min() - 1, yy_.max() + 1
            ca = tile[max(0, ya), x] if ya >= 0 else tile[min(len(col) - 1, yb), x]
            cb = tile[min(len(col) - 1, yb), x] if yb < len(col) else ca
            for y in yy_:
                t = (y - ya) / max(1, (yb - ya)); clean[y, x] = np.round(ca * (1 - t) + cb * t)
        sheet.append((clean.astype(np.uint8), brow.astype(np.uint8)))
    # the rig sheet: [clean L | brow L | clean R | brow R], each tile its own box size, side by side at y 0
    if sheet:
        tw = sum(t[0].shape[1] * 2 for t in sheet); th = max(t[0].shape[0] for t in sheet)
        sh_im = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); x = 0; xs_ = []
        for clean, brow in sheet:
            sh_im.paste(Image.fromarray(clean), (x, 0)); xs_.append(x); x += clean.shape[1]
            sh_im.paste(Image.fromarray(brow), (x, 0)); xs_.append(x); x += brow.shape[1]
        sh_im.save(HERE / "title_assets" / f"title_char_{name}_rig.png")
        for i, br in enumerate([b for b in brows if b]): br["clean"] = xs_[2 * i]; br["brow"] = xs_[2 * i + 1]
    face = [round((eyes[0]["cx"] + eyes[1]["cx"]) / 2, 1), round((eyes[0]["cy"] + eyes[1]["cy"]) / 2, 1)]
    res[name] = {"art": [W, H], "eyes": eyes, "brows": brows, "face": face}
    # the overlay: outer ellipse (red), iris (yellow) at the painted place, pupil (cyan), shines (green), brow boxes (magenta)
    ov = im.copy(); d = ImageDraw.Draw(ov)
    for e in eyes:
        d.ellipse((e["cx"] - e["a"], e["cy"] - e["b"], e["cx"] + e["a"], e["cy"] + e["b"]), outline=(255, 0, 0, 255), width=3)
        d.ellipse((e["cx"] - e["a"] + e["ring"], e["cy"] - e["b"] + e["ring"], e["cx"] + e["a"] - e["ring"], e["cy"] + e["b"] - e["ring"]), outline=(255, 140, 0, 255), width=2)
        px, py = e["pupil_c"]
        d.ellipse((px - e["iris_r"], py - e["iris_r"], px + e["iris_r"], py + e["iris_r"]), outline=(255, 255, 0, 255), width=2)
        d.ellipse((px - e["pupil_r"], py - e["pupil_r"], px + e["pupil_r"], py + e["pupil_r"]), outline=(0, 255, 255, 255), width=2)
        for sx, sy, sr in e["shines"]: d.ellipse((px + sx - sr, py + sy - sr, px + sx + sr, py + sy + sr), outline=(0, 255, 0, 255), width=2)
    for br in brows:
        if br: x0, y0, w, h = br["box"]; d.rectangle((x0, y0, x0 + w, y0 + h), outline=(255, 0, 255, 255), width=3); d.ellipse((br["c"][0] - 4, br["c"][1] - 4, br["c"][0] + 4, br["c"][1] + 4), fill=(255, 0, 255, 255))
    d.ellipse((face[0] - 5, face[1] - 5, face[0] + 5, face[1] + 5), fill=(0, 0, 255, 255))
    e0 = eyes[0]; crop = (int(min(e["cx"] - 2.2 * e["a"] for e in eyes)), int(min(e["cy"] - 3.2 * e["b"] for e in eyes)), int(max(e["cx"] + 2.2 * e["a"] for e in eyes)), int(max(e["cy"] + 2 * e["b"] for e in eyes)))
    ov.crop(crop).save(out / f"{name}_overlay.png")
    print(name, json.dumps(res[name]))
(out / "eyes.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
(HERE / "title_assets" / "cover_eyes_data.json").write_text(json.dumps(res, indent=1), encoding="utf-8"); print("written", out / "eyes.json", "and title_assets/cover_eyes_data.json")
