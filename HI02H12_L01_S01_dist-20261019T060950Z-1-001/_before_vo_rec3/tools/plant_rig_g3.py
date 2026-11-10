"""plant_rig_g3.py — [g3-grow] (2026-11-02) G3's three plants cut from the garden (g3_assets/img_g3_garden.webp, the frame 716:1262's
"image 284", 1671x941, drawn -27,-132 1117x630 of the card's padding box, cover) so they can GROW out of their soil as the page opens.

Writes g3_assets/plant_rig/:
  img_g3_garden_bare.webp  the garden with the three plants taken out: the grass and the tree line behind them an offset copy of the
                           same rows (Poisson-matched at every seam), the soil behind the stems and the lower leaves rebuilt from the
                           soil around them (the mound's top edge carried across); LOSSLESS, so every pixel away from the plants is
                           the painting's
  img_g3_plant_{rose,marigold,jasmine}.webp  each plant (stem, leaves, flowers) as RGBA: its edge pixels un-mixed from the bare
                           garden behind them, so plant-over-bare gives the painting back; a sheet the garden's size with the plant
                           in its place (LOSSLESS), so the page draws it with the garden's own box and cover — on the garden's
                           pixels exactly (a cut-out in its own box was snapped to the device pixels on its own: up to half a
                           pixel off the painting, its edges up to 101 levels off at rest, measured)
  rig.json                 each plant's box in the sheet and its stem's base point (bitmap px), the checks
With --debug <dir>: overlays and the rest / mid-growth composites. Run: python -I plant_rig_g3.py [--debug <dir>]
"""
import sys, json, pathlib, math
import numpy as np
from PIL import Image

SCR = pathlib.Path(__file__).resolve().parent
SRC = SCR / "g3_assets" / "img_g3_garden.webp"
OUT = SCR / "g3_assets" / "plant_rig"; OUT.mkdir(exist_ok=True)
DEBUG = pathlib.Path(sys.argv[sys.argv.index("--debug") + 1]) if "--debug" in sys.argv else None
if DEBUG: DEBUG.mkdir(parents=True, exist_ok=True)

im = Image.open(SRC).convert("RGB"); W, H = im.size
assert (W, H) == (1671, 941), (W, H)
O = np.asarray(im).astype(np.float32)

def dilate(m, r):
    k = int(math.ceil(r)); out = m.copy()
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            if dx * dx + dy * dy > r * r + 1e-6 or (dx == 0 and dy == 0): continue
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out
def erode(m, r): return ~dilate(~m, r)
def grow(seed, allowed, iters=6000):
    """flood fill (4-connected) from seed through allowed"""
    cur = seed & allowed
    for _ in range(iters):
        nxt = cur.copy()
        nxt[1:, :] |= cur[:-1, :]; nxt[:-1, :] |= cur[1:, :]; nxt[:, 1:] |= cur[:, :-1]; nxt[:, :-1] |= cur[:, 1:]
        nxt &= allowed
        if (nxt == cur).all(): return cur
        cur = nxt
    return cur
def components(m):
    """4-connected labels of m (union-find over row runs) -> (labels, sizes)"""
    lab = np.zeros(m.shape, np.int32); n = 0; parent = [0]
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for y in range(m.shape[0]):
        row = m[y]; x = 0
        while x < m.shape[1]:
            if not row[x]: x += 1; continue
            x0 = x
            while x < m.shape[1] and row[x]: x += 1
            n += 1; parent.append(n); lab[y, x0:x] = n
            if y:
                for l in np.unique(lab[y - 1, x0:x]):
                    if l: ra, rb = find(int(l)), find(n); parent[max(ra, rb)] = min(ra, rb)
    roots = np.array([find(i) for i in range(n + 1)], np.int32); lab = roots[lab]
    sizes = np.bincount(lab.ravel(), minlength=n + 1); sizes[0] = 0
    return lab, sizes
def cg_poisson(target, guide, hole, iters=2000, tol=1e-6):
    """f = target outside `hole`; inside, lap f = lap guide (the guide's texture kept, every seam matched to the target): 5-point
    stencil, Dirichlet, solved per channel by conjugate gradients (matrix-free) on a crop"""
    hole = hole.copy(); hole[0, :] = hole[-1, :] = False; hole[:, 0] = hole[:, -1] = False
    nb = ((1, 0), (-1, 0), (0, 1), (0, -1))
    sh = lambda a, dy, dx: np.roll(np.roll(a, dy, 0), dx, 1)
    out = target.astype(np.float64).copy()
    for ch in range(target.shape[2]):
        t, g = target[..., ch].astype(np.float64), guide[..., ch].astype(np.float64)
        b = np.zeros_like(t)
        for dy, dx in nb:
            b += (g - sh(g, dy, dx))
            b += np.where(sh(hole, dy, dx), 0, sh(t, dy, dx))
        b = np.where(hole, b, 0)
        def A(x):
            y = 4 * x
            for dy, dx in nb: y -= np.where(sh(hole, dy, dx), sh(x, dy, dx), 0)
            return np.where(hole, y, 0)
        x = np.where(hole, g, 0)
        r = b - A(x); p = r.copy(); rs = (r * r).sum(); b2 = max((b * b).sum(), 1e-9)
        for _ in range(iters):
            Ap = A(p); al = rs / max((p * Ap).sum(), 1e-12)
            x += al * p; r -= al * Ap; rn = (r * r).sum()
            if rn / b2 < tol: break
            p = r + (rn / rs) * p; rs = rn
        out[..., ch] = np.where(hole, x, t)
    return out

# ---------- the three plants: generous boxes (bitmap px); the row band above the mounds ----------
PLANTS = [{"name": "rose", "box": (606, 508, 796, 668)}, {"name": "marigold", "box": (934, 518, 1118, 668)},
          {"name": "jasmine", "box": (1282, 508, 1478, 668)}]
Y_MOUND = 634   # at and below this row the stems and the lowest leaves lie over the soil (the mounds' tops are 638-652)
report = {"bitmap": [W, H], "plants": []}

for P in PLANTS:
    x0, y0, x1, y1 = P["box"]; bw, bh = x1 - x0, y1 - y0
    crop = O[y0:y1, x0:x1]; cr, cg, cb = crop[..., 0], crop[..., 1], crop[..., 2]
    YY = np.arange(y0, y1)[:, None] + np.zeros((1, bw)); XX = np.arange(x0, x1)[None, :] + np.zeros((bh, 1))
    # the row model of what is behind (the sky / tree line / grass are horizontal bands): each row's median colour 8-26 px left
    # and right of the box, interpolated across it
    L = np.median(O[y0:y1, x0 - 26:x0 - 8], axis=1); Rr = np.median(O[y0:y1, x1 + 8:x1 + 26], axis=1)
    t = (np.arange(bw) + 0.5) / bw
    Brow = L[:, None, :] * (1 - t)[None, :, None] + Rr[:, None, :] * t[None, :, None]
    # each pixel against the model's own row and the rows above / below it (the tree line's straight edge sits a pixel higher or
    # lower here and there: a one-row model alone draws a line along it)
    dd = [np.sqrt(((crop - np.roll(Brow, k, axis=0)) ** 2).sum(axis=2)) for k in (-1, 0, 1)]
    d = np.minimum(np.minimum(dd[0], dd[1]), dd[2])
    upper = YY < Y_MOUND
    green = (cg > cr + 6) & (cg > cb + 18)                           # leaves / stems (the soil is red over green)
    grassy = (cr > 150) & (cg > 200) & (cb < 140) & (cg - cr < 45)   # the lawn's yellow-green (a leaf is darker / greener)
    soil = (cr >= cg) & ~((cr > 200) & (cg > 200))                    # the mound's browns (not the white jasmine)
    plant_core = np.where(upper, d > 42, green & ~grassy)
    # the background: flooded in from the box's edge through everything that is not plant_core; the plant = the rest (its own
    # light parts, enclosed by its outline, are never reached)
    edge = np.zeros((bh, bw), bool); edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = True
    bgm = grow(edge & ~plant_core, ~plant_core)
    plant = ~bgm
    lab, sizes = components(plant)
    keep = sizes >= 60; keep[0] = False
    plant = keep[lab]
    P["plant"] = plant; P["Brow"] = Brow; P["d"] = d; P["soil"] = soil; P["green"] = green; P["grassy"] = grassy
    print(f"{P['name']}: plant {int(plant.sum())} px, bbox x {XX[plant].min():.0f}-{XX[plant].max():.0f} y {YY[plant].min():.0f}-{YY[plant].max():.0f}, components kept {int(keep.sum())}")


# ---------- the bare garden: what is behind each plant ----------
# The hole: the plant and two pixels round it (its anti-aliased rim). Two stages, both solved by conjugate gradients:
#  1. over the mounds (rows >= Y_SPLIT): the mound's top edge is read off every column where it shows and carried across the
#     hidden ones (straight between the nearest shown points); below it the soil is filled from the SOIL round the hole only, above
#     it the lawn from the LAWN only (two membrane solves, each blind to the other's pixels), the edge anti-aliased by its sub-pixel
#     height — no soil smeared into the grass, no grass into the soil;
#  2. above (rows < Y_SPLIT): a Poisson solve whose guide is the same rows copied from dx px away (dx chosen among clean stretches of
#     lawn so that the copy agrees best with the painting along the hole's rim: the tree line's edge lands at its own height) — on
#     the lawn only that copy's FINE texture over the row model (each row's own colour from both sides of the box), so no darker
#     patch of lawn is carried in — and matched to the painting (and to stage 1) at every seam.
# One pass: the hole is three pixels wider than the plant all round, so its rim (the Dirichlet values) is lawn / soil untouched by
# the plant's own anti-aliased edge (a two-pass version that re-solved round the pixels the matte called clean pulled the leaves'
# faint green rim into the fill: a ghost of the plant). The grass round each plant is a touch yellower than the open lawn (the
# painting's own light about it, B -5..-10 levels within 8 px); the fill continues that from its rim.
Y_SPLIT = 630
all_plants = np.zeros((H, W), bool)
for P in PLANTS:
    x0, y0, x1, y1 = P["box"]; all_plants[y0:y1, x0:x1] |= P["plant"]
forbid = dilate(all_plants, 8)
forbid[Y_SPLIT:, :] |= True                 # nothing at the mounds' height is taken from afar (every mound / shadow is down there)
forbid[:, :160] |= True; forbid[:, 1520:] |= True   # the grass tufts at both ends

def cg_solve(target, guide, hole, src, iters=4000, tol=1e-8, eps=1e-5):
    """in `hole`: lap f = lap guide, coupled only to hole / src neighbours; src pixels (outside the hole) are Dirichlet values, any
    other neighbour is Neumann (no flux); eps keeps a hole with no src neighbour well-posed (it then takes the guide)"""
    hole = hole.copy(); hole[0, :] = hole[-1, :] = False; hole[:, 0] = hole[:, -1] = False
    src = src & ~hole
    nb = ((1, 0), (-1, 0), (0, 1), (0, -1))
    sh = lambda a, dy, dx: np.roll(np.roll(a, dy, 0), dx, 1)
    on = [sh(hole | src, dy, dx) for dy, dx in nb]; hn = [sh(hole, dy, dx) for dy, dx in nb]; sn = [sh(src, dy, dx) for dy, dx in nb]
    diag = eps + sum(o.astype(np.float64) for o in on)
    out = target.astype(np.float64).copy()
    for ch in range(target.shape[2]):
        t, g = target[..., ch].astype(np.float64), guide[..., ch].astype(np.float64)
        b = eps * g
        for k, (dy, dx) in enumerate(nb):
            b += np.where(on[k], g - sh(g, dy, dx), 0) + np.where(sn[k], sh(t, dy, dx), 0)
        b = np.where(hole, b, 0)
        def A(x):
            y = diag * x
            for k, (dy, dx) in enumerate(nb): y -= np.where(hn[k], sh(x, dy, dx), 0)
            return np.where(hole, y, 0)
        x = np.where(hole, g, 0)
        r = b - A(x); p = r.copy(); rs = (r * r).sum(); b2 = max((b * b).sum(), 1e-9)
        for _ in range(iters):
            Ap = A(p); al = rs / max((p * Ap).sum(), 1e-12)
            x += al * p; r -= al * Ap; rn = (r * r).sum()
            if rn / b2 < tol: break
            p = r + (rn / rs) * p; rs = rn
        out[..., ch] = np.where(hole, x, t)
    return out

def blur_x(a, s):
    """a gaussian blur (sigma s px) ALONG THE ROWS of an H x W x C array, edges clamped (each row's level kept: no ringing off the
    tree line's horizontal edge)"""
    k = np.arange(-int(3 * s), int(3 * s) + 1); g = np.exp(-k * k / (2 * s * s)); g /= g.sum()
    pad = len(k) // 2
    a = np.pad(a, ((0, 0), (pad, pad), (0, 0)), mode="edge")
    return sum(g[i] * a[:, i:i + a.shape[1] - 2 * pad] for i in range(len(k)))

def fill_behind(P, hole, keep_px):
    """the bare crop for plant P with `hole` filled (keep_px: pixels of the hole to keep as painted — none on the first pass)"""
    x0, y0, x1, y1 = P["box"]; bw, bh = x1 - x0, y1 - y0
    crop = O[y0:y1, x0:x1].astype(np.float64)
    YY = np.arange(y0, y1)[:, None] + np.zeros((1, bw)); XX = np.arange(x0, x1)[None, :] + np.zeros((bh, 1))
    cr, cg_, cb = crop[..., 0], crop[..., 1], crop[..., 2]
    soil = (cr > cg_ + 8) & ~((cr > 200) & (cg_ > 200) & (cb > 160))   # every brown of the mound, its darkest back slope too (red over green)
    # stage 1: the mound's top edge, column by column. Where it shows (the first soil pixel at or below Y_SPLIT - 6 with the two
    # pixels above it shown) it is read to a sub-pixel, the readings filtered (one more than 2.5 px off the median of those within
    # +-3 columns is dropped) and joined straight across the hidden columns. Then, where the hole covers the edge but soil shows
    # RIGHT BELOW the hole (between the lowest leaves, beside a stem), the edge is at or above that pixel: such a reading may only
    # RAISE the edge there — the soil rises toward the stems (a dome), and an edge drawn straight between the flanks alone sat under
    # those bits of soil (they stood up as spikes); one deeper than the flanks' line (the mound's body under a stem) says nothing.
    cvis = np.full(bw, np.nan)
    for xx in range(bw):
        for yy in range(max(Y_SPLIT - 6 - y0, 2), bh):
            if soil[yy, xx]:
                if not (hole[yy, xx] or hole[yy - 1, xx] or hole[yy - 2, xx]):
                    up, me, dn = crop[yy - 1, xx], crop[yy, xx], crop[min(yy + 1, bh - 1), xx]
                    den = np.dot(dn - up, dn - up); f = float(np.clip(np.dot(me - up, dn - up) / den, 0, 1)) if den > 1 else 1.0
                    cvis[xx] = y0 + yy + (1 - f)                     # the edge's height: soil from here down
                break
    idx = np.arange(bw)
    def robust_line(r):
        k = ~np.isnan(r); sm = r.copy()
        for xx in np.nonzero(k)[0]:
            win = r[max(xx - 3, 0):xx + 4]; win = win[~np.isnan(win)]; med = np.median(win)
            if abs(r[xx] - med) > 2.5: k[xx] = False
            elif len(win) >= 3: sm[xx] = med
        assert k.sum() > 10, (P["name"], int(k.sum()))
        return np.interp(idx, idx[k], sm[k]), k
    c_flank, k1 = robust_line(cvis)
    rd = np.where(k1, cvis, np.nan)
    raised = 0
    for xx in np.nonzero(~k1)[0]:
        col = np.nonzero(hole[:, xx] & (YY[:, xx] >= Y_SPLIT - 6))[0]
        if not len(col): continue
        hb = col.max() + 1                                             # the first shown pixel below the hole
        if hb < bh and soil[hb, xx] and y0 + hb < c_flank[xx]: rd[xx] = y0 + hb; raised += 1
    c, known = robust_line(rd)
    P["edge_raised"] = raised
    w = np.clip(YY + 1 - c[None, :], 0, 1)[..., None]            # the soil's coverage of each pixel (row r spans r..r+1, soil from c down)
    m1 = hole & (YY >= Y_SPLIT)
    lawn = ~soil & ~hole
    def rows_from(srcm):
        """each hole pixel of m1: the nearest `srcm` pixels left and right in its own row (within 60 px), blended by distance; the
        painting everywhere else (a guide must agree with the values round the hole, or its gradient there drives the solve)"""
        g = crop.copy()
        for yy in np.nonzero(m1.any(axis=1))[0]:
            xs = np.nonzero(srcm[yy])[0]
            if not len(xs): continue
            for xx in np.nonzero(m1[yy])[0]:
                i = np.searchsorted(xs, xx); L_ = xs[i - 1] if i > 0 else None; R_ = xs[i] if i < len(xs) else None
                if L_ is not None and xx - L_ > 60: L_ = None
                if R_ is not None and R_ - xx > 60: R_ = None
                if L_ is None and R_ is None: L_ = xs[max(i - 1, 0)]
                if L_ is None: g[yy, xx] = crop[yy, R_]
                elif R_ is None: g[yy, xx] = crop[yy, L_]
                else: t_ = (xx - L_) / (R_ - L_); g[yy, xx] = (1 - t_) * crop[yy, L_] + t_ * crop[yy, R_]
        return g
    f_soil = cg_solve(crop, rows_from(soil & ~hole), m1, soil & ~hole)
    f_lawn = cg_solve(crop, rows_from(lawn), m1, lawn)
    st1 = np.where(m1[..., None], w * f_soil + (1 - w) * f_lawn, crop)
    # stage 2: the lawn and the tree line above the mounds
    up = hole & (YY < Y_SPLIT)
    ring = dilate(up, 1.0) & ~hole & (YY < Y_SPLIT)
    hy, hx = np.nonzero(up); ry, rx = np.nonzero(ring)
    best = None
    for dx in list(range(-330, -105, 2)) + list(range(106, 331, 2)):
        sx = hx + x0 + dx
        if sx.min() < 0 or sx.max() >= W or forbid[hy + y0, sx].any(): continue
        e = ((O[ry + y0, rx + x0 + dx] - O[ry + y0, rx + x0]) ** 2).sum(axis=1).mean()
        if best is None or e < best[0]: best = (e, dx)
    assert best is not None, P["name"]
    dxf = best[1]
    far = np.zeros((bh, bw, 3), np.float64)
    for yy in range(bh):
        xs = np.clip(np.arange(bw) + x0 + dxf, 0, W - 1); far[yy] = O[y0 + yy, xs]
    # the tree line's straight bottom edge: the copy's own edge (sub-pixel, where red crosses 160 going down) moved, column by
    # column, onto the line between the painting's edge just left and just right of the hole (else a 1-2 px step at each seam)
    def edge_at(colv):
        r = colv[:, 0]
        for yy in range(max(522 - y0, 1), min(552 - y0, bh)):
            if r[yy - 1] < 160 <= r[yy]: return yy - 1 + (160 - r[yy - 1]) / (r[yy] - r[yy - 1])
        return None
    tl = hole[max(522 - y0, 0):552 - y0].any(axis=0)
    if tl.any():
        cols = np.nonzero(tl)[0]; a, b = cols.min(), cols.max()
        eL = [e for e in (edge_at(crop[:, k]) for k in range(max(a - 6, 0), a - 1)) if e is not None]
        eR = [e for e in (edge_at(crop[:, k]) for k in range(b + 2, min(b + 7, bw))) if e is not None]
        if eL and eR:
            eL, eR = float(np.median(eL)), float(np.median(eR))
            ys = np.arange(bh, dtype=np.float64)
            for xx in range(max(a - 1, 0), min(b + 2, bw)):
                ec = edge_at(far[:, xx])
                if ec is None: continue
                et = eL + (eR - eL) * (xx - (a - 1)) / max((b + 1) - (a - 1), 1)
                src_y = np.clip(ys - (et - ec), 0, bh - 1)          # sample the copy that much higher / lower
                for ch in range(3): far[:, xx, ch] = np.interp(src_y, ys, far[:, xx, ch])
            P["treeline"] = [round(eL + y0, 2), round(eR + y0, 2)]
    Brow = P["Brow"].astype(np.float64)
    fine = Brow + (far - blur_x(far, 5.0))                        # the row model + the copy's fine texture along the row
    k = np.clip((YY - 541) / 10.0, 0, 1)[..., None]              # the copy itself at the tree line (its edge), the fine version below
    guide = far * (1 - k) + fine * k
    st2 = cg_solve(st1, guide, up, ~up)
    out = np.where(hole[..., None], np.clip(st2, 0, 255), crop)
    out[keep_px] = crop[keep_px]
    return out, dxf, math.sqrt(best[0]), c, known

def push_out(col, known, n):
    """spread the known pixels' colours n px outward (each new pixel the mean of its known 8-neighbours)"""
    col = col.copy(); known = known.copy()
    for _ in range(n):
        acc = np.zeros_like(col); cnt = np.zeros(known.shape, np.float64)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0: continue
                k = np.roll(np.roll(known, dy, 0), dx, 1); acc += np.roll(np.roll(col, dy, 0), dx, 1) * k[..., None]; cnt += k
        new = ~known & (cnt > 0)
        col[new] = acc[new] / cnt[new][..., None]; known |= new
    return col

def matte(P, Bk, hole):
    """alpha (1 inside, the rim's from projecting the painting onto the line bare -> plant colour) and the un-mixed colour"""
    plant = P["plant"]; x0, y0, x1, y1 = P["box"]; crop = O[y0:y1, x0:x1].astype(np.float64)
    core = erode(plant, 1.0)
    F = push_out(np.where(core[..., None], crop, 0), core, 4)
    FB = F - Bk; OB = crop - Bk; den = (FB ** 2).sum(axis=2)
    a = np.where(den > 400, np.clip((OB * FB).sum(axis=2) / np.maximum(den, 1e-6), 0, 1), plant.astype(np.float64))
    # the least alpha with which some colour in 0..255 over the bare gives the painting back (per channel: a pixel brighter than
    # the bare needs (O - B) / (255 - B), a darker one (B - O) / B); a rim pixel takes the larger of that and its projection, so
    # plant-over-bare IS the painting at rest, and what moves with the plant beyond its own edge differs from the bare garden it
    # moves over by no more than the painting differs from the fill there
    dO = crop - Bk
    need = np.where(dO > 0, dO / np.maximum(255 - Bk, 1e-6), np.where(dO < 0, -dO / np.maximum(Bk, 1e-6), 0)).max(axis=2)
    alpha = np.where(core, 1.0, np.where(hole, np.clip(np.maximum(a, need), 0, 1), 0.0))
    alpha = np.where(alpha < 1 / 255, 0, alpha)
    ex = (crop - (1 - alpha[..., None]) * Bk) / np.maximum(alpha[..., None], 1e-6)
    col = np.where(alpha[..., None] > 0, np.clip(ex, 0, 255), F)
    col = np.where(core[..., None], crop, col)
    return alpha, col

bare = O.copy().astype(np.float64)
rest_err = {}
for P in PLANTS:
    x0, y0, x1, y1 = P["box"]
    hole2 = dilate(P["plant"], 3.0)
    Bk, dxf, mis, c, known = fill_behind(P, hole2, np.zeros(hole2.shape, bool))
    alpha, col = matte(P, Bk, hole2)
    clean = hole2 & ~P["plant"] & (alpha == 0)
    crop = O[y0:y1, x0:x1].astype(np.float64)
    comp = alpha[..., None] * col + (1 - alpha[..., None]) * Bk
    err = np.abs(comp - crop).max(axis=2)
    rest_err[P["name"]] = {"max": round(float(err.max()), 1), "over4": int((err > 4).sum()), "over12": int((err > 12).sum())}
    bare[y0:y1, x0:x1] = Bk
    # the layer's box: the alpha's extent + 1 px
    ys, xs = np.nonzero(alpha > 0); bx0, by0, bx1, by1 = xs.min() - 1, ys.min() - 1, xs.max() + 2, ys.max() + 2
    rgba = np.concatenate([col, alpha[..., None] * 255], axis=2)[by0:by1, bx0:bx1]
    rgba[rgba[..., 3] < 0.5, :3] = 0
    sheet = np.zeros((H, W, 4)); sheet[y0 + by0:y0 + by1, x0 + bx0:x0 + bx1] = rgba   # the garden's size, the plant in its place
    Image.fromarray(np.clip(np.round(sheet), 0, 255).astype(np.uint8), "RGBA").save(OUT / f"img_g3_plant_{P['name']}.webp", lossless=True, quality=100, method=6, exact=True)
    # the stem's base: the lowest rows of the plant (the stem where the mound's front lip hides it), their middle
    pys, pxs = np.nonzero(P["plant"]); yb = pys.max(); bxs = np.nonzero(P["plant"][yb - 3:yb + 1].any(axis=0))[0]
    base = (float(x0 + bxs.mean() + 0.5), float(y0 + yb + 1))
    P.update(alpha=alpha, col=col, hole=hole2, bare=Bk, edge=c, edge_known=known, copy_dx=dxf,
             layer_box=[int(x0 + bx0), int(y0 + by0), int(bx1 - bx0), int(by1 - by0)], base=base)
    report["plants"].append({"name": P["name"], "box": P["layer_box"], "base": [round(base[0], 2), round(base[1], 2)], "copy_dx": dxf,
                             "rim_mismatch": round(mis, 1), "plant_px": int(P["plant"].sum()), "hole_px": int(hole2.sum()), "clean_px": int(clean.sum()),
                             "edge_shown_cols": int(known.sum()), "rest_err": rest_err[P["name"]],
                             "file": f"img_g3_plant_{P['name']}.webp", "bytes": (OUT / f"img_g3_plant_{P['name']}.webp").stat().st_size})
    print(f"{P['name']}: hole {int(hole2.sum())} px ({int(clean.sum())} rim px kept as painted), lawn from dx {dxf:+d} (rim mismatch {mis:.1f}), "
          f"the mound's edge shown in {int(known.sum())} of {x1 - x0} columns; layer {P['layer_box']}, base {base[0]:.1f},{base[1]:.1f}; "
          f"plant over bare vs the painting {rest_err[P['name']]}")

Image.fromarray(np.clip(np.round(bare), 0, 255).astype(np.uint8)).save(OUT / "img_g3_garden_bare.webp", lossless=True, quality=100, method=6)
chk = np.asarray(Image.open(OUT / "img_g3_garden_bare.webp").convert("RGB")).astype(np.float64)
outside = np.ones((H, W), bool)
for P in PLANTS:
    x0, y0, x1, y1 = P["box"]; outside[y0:y1, x0:x1] &= ~P["hole"]
report["bare"] = {"bytes": (OUT / "img_g3_garden_bare.webp").stat().st_size, "outside_holes_max_diff": float(np.abs(chk - O)[outside].max()),
                  "decoded_vs_built_max": float(np.abs(chk - np.clip(np.round(bare), 0, 255)).max())}
# the layers as decoded, over the decoded bare: the rest frame the page draws (before any resampling)
for P, rp in zip(PLANTS, report["plants"]):
    lx, ly, lw, lh = rp["box"]; Lf = np.asarray(Image.open(OUT / rp["file"]).convert("RGBA")).astype(np.float64)
    assert Lf.shape[:2] == (H, W) and Lf[..., 3].sum() == Lf[ly:ly + lh, lx:lx + lw, 3].sum(), "the sheet holds its plant only, in its box"
    L_ = Lf[ly:ly + lh, lx:lx + lw]
    a_ = L_[..., 3:4] / 255; comp = a_ * L_[..., :3] + (1 - a_) * chk[ly:ly + lh, lx:lx + lw]
    e = np.abs(comp - O[ly:ly + lh, lx:lx + lw]).max(axis=2)
    rp["rest_err_decoded"] = {"max": round(float(e.max()), 1), "over4": int((e > 4).sum()), "over12": int((e > 12).sum())}
print("bare:", report["bare"], "| decoded rest error:", {rp["name"]: rp["rest_err_decoded"] for rp in report["plants"]})
(OUT / "rig.json").write_text(json.dumps(report, indent=1), encoding="utf-8")

if DEBUG:
    def big(a, k=3): return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((a.shape[1] * k, a.shape[0] * k), Image.NEAREST)
    for P in PLANTS:
        x0, y0, x1, y1 = P["box"]
        c = O[y0:y1, x0:x1]; b = P["bare"]
        ov = c.copy(); ov[P["plant"]] = ov[P["plant"]] * 0.35 + np.array([255, 0, 255]) * 0.65
        big(np.concatenate([ov, b], axis=1)).save(DEBUG / f"bare_{P['name']}.png")
        big(np.concatenate([c[110:, :], b[110:, :]], axis=0), 6).save(DEBUG / f"mound_{P['name']}.png")
        # mid-growth: the layer scaled about the base over the bare (bilinear, as a browser draws it)
        out = []
        for sx_, sy_ in ((0.3, 0.25), (0.65, 0.7), (1.0, 1.0)):
            gy, gx = np.mgrid[0:y1 - y0, 0:x1 - x0].astype(np.float64)
            bxl, byl = P["base"][0] - x0, P["base"][1] - y0
            ux = (gx + 0.5 - bxl) / sx_ + bxl - 0.5; uy = (gy + 0.5 - byl) / sy_ + byl - 0.5
            pm = np.concatenate([P["col"] * P["alpha"][..., None], P["alpha"][..., None]], axis=2)
            xi = np.clip(np.floor(ux).astype(int), 0, x1 - x0 - 2); yi = np.clip(np.floor(uy).astype(int), 0, y1 - y0 - 2)
            fx = np.clip(ux - xi, 0, 1)[..., None]; fy = np.clip(uy - yi, 0, 1)[..., None]
            s = (pm[yi, xi] * (1 - fx) * (1 - fy) + pm[yi, xi + 1] * fx * (1 - fy) + pm[yi + 1, xi] * (1 - fx) * fy + pm[yi + 1, xi + 1] * fx * fy)
            ok = ((ux >= 0) & (ux <= x1 - x0 - 1) & (uy >= 0) & (uy <= y1 - y0 - 1))[..., None]
            s = s * ok
            out.append(s[..., :3] + (1 - s[..., 3:4]) * b)
        big(np.concatenate(out, axis=1), 2).save(DEBUG / f"grow_{P['name']}.png")
        Image.fromarray((P["alpha"] * 255).astype(np.uint8)).resize(((x1 - x0) * 3, (y1 - y0) * 3), Image.NEAREST).save(DEBUG / f"alpha_{P['name']}.png")
    big(bare[480:700, 560:1520], 1).save(DEBUG / "bare_strip.png")
    print("debug in", DEBUG)
