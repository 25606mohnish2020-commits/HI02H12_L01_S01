"""[optimize] (2026-11-15) the post-build step that makes the dist light and fully preloaded.

build.py calls run() last, on the dist it has just written; it can also run by itself:
    python -I -X utf8 optimize.py ../HI02H05_L03_S01_dist

What it does, in order (every step is idempotent, so a rebuild gives the same dist):
 1. quarantine: the assets no page can use (optimize_assets/unused_assets.txt, decided from every static reference and
    a request log of the whole check suite) move out of the dist to optimize_assets/quarantine/ (nothing is deleted).
 2. media: MP3 -> Ogg Opus; Ogg Vorbis and Opus above 100 kb/s -> Ogg Opus (mono 64k, stereo 96k); PNG -> WebP (q85,
    alpha lossless; the rig / mask sheets lossless and pixel-exact); GIF -> animated WebP (q85, the same frames and
    timings). A converted file is used ONLY when it is smaller than its source; otherwise the source stays. Already-WebP
    pictures are left as they are (the lossless ones were stored that way at the user's "don't degrade" request), so are
    SVGs, fonts and Opus files at or below 100 kb/s. Sources that leave the dist are kept in optimize_assets/originals/.
    Results are cached by content (optimize_assets/cache/), so a rebuild re-encodes nothing that did not change.
    Browser support: Ogg Opus and WebP (still and animated) play in Chrome / Edge / Firefox and in recent Safari.
 3. inline media: the base64 PNGs in style.css -> lossless WebP, the inline MP3 pop in app.js -> Opus (when smaller).
 4. references: every renamed file is renamed in index.html (the card data too), style.css and app.js; then every
    "assets/..." reference left is checked to exist (a missing one stops the build).
 5. preload: the size table of every remaining asset (bytes on disk, audio lengths) and the preloader / blob resolver /
    media watchdogs (optimize_assets/preload_head.js at the top of app.js, preload_tail.js at the end), its loading bar
    (preload.css + the markup next to the play button).
"""
import base64, hashlib, io, json, math, os, pathlib, re, shutil, subprocess, sys, urllib.parse

SCR = pathlib.Path(__file__).resolve().parent
OPT = SCR / "optimize_assets"
CACHE = OPT / "cache"
ORIG = OPT / "originals"
QUAR = OPT / "quarantine"
RENAMES_JSON = OPT / "renames.json"
SETTINGS_V = "v1"
IMAGE_V = "i2"                           # stills / animations: the PSNR-guarded quality choice
OPUS_MONO_K, OPUS_STEREO_K = 64, 96
OPUS_REENCODE_ABOVE = 100_000            # bits/s: Opus files above this are re-encoded at the targets above
WEBP_Q = 85
# rig / mask sheets: read as exact pixels (eye rigs, CSS masks by alpha) -> lossless, exact RGB under transparency
LOSSLESS_NAMES = {"title_char_comma_rig.png", "title_char_purn_rig.png", "title_char_question_rig.png",
                  "img_g3_girl_efill.png", "img_g3_girl_eiris.png"}
MEDIA_EXT = {".mp3", ".ogg", ".png", ".gif"}


def log(*a):
    print("[optimize]", *a, flush=True)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def ffprobe(path: pathlib.Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffprobe failed on {path}: {r.stderr[:300]}")
    j = json.loads(r.stdout)
    a = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), {})
    f = j.get("format", {})
    return {"codec": a.get("codec_name"), "channels": int(a.get("channels") or 0), "rate": int(a.get("sample_rate") or 0),
            "duration": float(f.get("duration") or a.get("duration") or 0), "bit_rate": int(f.get("bit_rate") or 0),
            "size": int(f.get("size") or path.stat().st_size)}


def cache_get(key: str, ext: str):
    p = CACHE / f"{key}{ext}"
    m = CACHE / f"{key}.json"
    if m.exists():
        meta = json.loads(m.read_text(encoding="utf-8"))
        if meta.get("keep") or p.exists():
            return meta, (p.read_bytes() if p.exists() else None)
    return None, None


def cache_put(key: str, ext: str, meta: dict, data):
    CACHE.mkdir(parents=True, exist_ok=True)
    if data is not None:
        (CACHE / f"{key}{ext}").write_bytes(data)
        remember_output(data)
    (CACHE / f"{key}.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")


# every file this step writes is remembered by its hash: an output is never taken for a source again (a rebuild restores the
# originals next to last time's outputs; a short Opus effect of ours measures above 100 kb/s by its container alone)
OUTPUTS_JSON = CACHE / "outputs.json"
_outputs = None
def _load_outputs():
    global _outputs
    if _outputs is None:
        _outputs = set(json.loads(OUTPUTS_JSON.read_text(encoding="utf-8"))) if OUTPUTS_JSON.exists() else set()
        for m in CACHE.glob("*.json") if CACHE.exists() else []:     # every cached conversion's output counts too
            if m.name in ("outputs.json",) or m.name.startswith("dur_"): continue
            for ext in (".ogg", ".webp"):
                f = m.with_suffix(ext)
                if f.exists(): _outputs.add(sha(f.read_bytes()))
    return _outputs
def remember_output(data: bytes):
    o = _load_outputs(); h = sha(data)
    if h not in o:
        o.add(h); OUTPUTS_JSON.parent.mkdir(parents=True, exist_ok=True); OUTPUTS_JSON.write_text(json.dumps(sorted(o)), encoding="utf-8")
def is_output(data: bytes) -> bool:
    return sha(data) in _load_outputs()


# ---------------------------------------------------------------- encoders
def opus_bytes(src_bytes: bytes, src_ext: str, channels: int, kbps: int) -> bytes:
    """encode to Ogg Opus at kbps (VBR), keeping the channel count; the timeline is kept (ffmpeg honours the source's
    encoder delay and writes Opus pre-skip / end trim)"""
    tmp = CACHE / "_tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    i = tmp / ("in" + src_ext)
    o = tmp / "out.ogg"
    i.write_bytes(src_bytes)
    if o.exists():
        o.unlink()
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(i), "-map", "0:a:0", "-map_metadata", "-1", "-vn",
           "-c:a", "libopus", "-b:a", f"{kbps}k", "-vbr", "on", "-compression_level", "10", "-application", "audio",
           "-ac", str(max(1, min(2, channels))), str(o)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not o.exists():
        raise RuntimeError(f"ffmpeg opus failed: {r.stderr[:400]}")
    return o.read_bytes()


def probe_bytes(data: bytes, ext: str) -> dict:
    tmp = CACHE / "_tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    p = tmp / ("probe" + ext)
    p.write_bytes(data)
    return ffprobe(p)


def webp_still(src_bytes: bytes, lossless: bool, quality: int = None) -> bytes:
    from PIL import Image
    im = Image.open(io.BytesIO(src_bytes))
    im.load()
    has_alpha = im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info)
    im = im.convert("RGBA" if has_alpha else "RGB")
    out = io.BytesIO()
    if lossless:
        im.save(out, "WEBP", lossless=True, quality=100, method=6, exact=True)
    else:
        im.save(out, "WEBP", quality=quality or WEBP_Q, method=6, alpha_quality=100)
    return out.getvalue()


def gif_frames(src_bytes: bytes):
    from PIL import Image
    im = Image.open(io.BytesIO(src_bytes))
    frames, durs = [], []
    for k in range(getattr(im, "n_frames", 1)):
        im.seek(k)
        frames.append(im.convert("RGBA").copy())
        durs.append(int(im.info.get("duration", 100) or 100))
    gif_loop = im.info.get("loop", None)              # None: no NETSCAPE block = plays once; 0 = forever; N = N repeats
    loop = 1 if gif_loop is None else (0 if gif_loop == 0 else int(gif_loop) + 1)
    return frames, durs, loop


def webp_anim(src_bytes: bytes, quality=None):
    """GIF -> animated WebP with the GIF's own frames (composited), per-frame durations and loop count; quality None = lossless.
    (libwebp merges a run of identical frames into one with their summed duration: the timeline stays the same.)"""
    frames, durs, loop = gif_frames(src_bytes)
    out = io.BytesIO()
    kw = dict(lossless=True, quality=100) if quality is None else dict(quality=quality, alpha_quality=100)
    frames[0].save(out, "WEBP", save_all=True, append_images=frames[1:], duration=durs, loop=loop, method=6,
                   allow_mixed=False, minimize_size=False, **kw)
    return out.getvalue(), {"frames": len(frames), "durations_ms": sum(durs), "loop": loop}


def anim_psnr(src_bytes: bytes, out_bytes: bytes) -> float:
    """the worst frame's visible-pixel PSNR, each GIF frame against the WebP frame shown at the same moment"""
    import numpy as np
    from PIL import Image
    g_frames, g_durs, _ = gif_frames(src_bytes)
    w = Image.open(io.BytesIO(out_bytes)); w_frames = []
    for k in range(getattr(w, "n_frames", 1)):
        w.seek(k); w_frames.append(w.convert("RGBA").copy())
    # libwebp may merge identical frames: walk both timelines by the GIF's durations, re-reading the WebP's own frame order
    starts, t = [], 0
    for d in g_durs: starts.append(t); t += d
    w_idx, prev, worst = 0, None, 99.0
    for k, (gf, st) in enumerate(zip(g_frames, starts)):
        if k and prev is not None and np.array_equal(np.asarray(gf), np.asarray(prev)):
            continue                                     # a merged repeat: the same WebP frame is still showing
        if w_idx >= len(w_frames): return 0.0
        def prem(im):
            a = np.asarray(im).astype(np.float64); return np.concatenate([a[..., :3] * (a[..., 3:4] / 255.0), a[..., 3:4]], axis=-1)
        A, B = prem(gf), prem(w_frames[w_idx]); vis = (A[..., 3] > 0) | (B[..., 3] > 0)
        mse = float(((A - B)[vis] ** 2).mean()) if vis.any() else 0.0
        worst = min(worst, 99.0 if mse == 0 else 10 * math.log10(255 ** 2 / mse))
        w_idx += 1; prev = gf
    return worst


# ---------------------------------------------------------------- per-file decisions
BED_K, BED_MIN_S = 64, 60                  # a long stereo music bed (the 240 s background music, played at 13 % under the voice): 64k

def audio_target(info: dict) -> int:
    if info["channels"] > 1 and info["duration"] > BED_MIN_S: return BED_K
    return OPUS_MONO_K if info["channels"] <= 1 else OPUS_STEREO_K


def plan_audio(data: bytes, ext: str):
    """-> (out_bytes or None, meta); None = keep the source"""
    info = probe_bytes(data, ext)
    needs = (ext == ".mp3") or (ext == ".ogg" and (info["codec"] == "vorbis" or (info["codec"] == "opus" and info["bit_rate"] > OPUS_REENCODE_ABOVE)))
    if not needs:
        return None, {"keep": True, "why": f"{info['codec']} {info['bit_rate']//1000} kb/s is already efficient", "src": info}
    k = audio_target(info)
    out = opus_bytes(data, ext, info["channels"], k)
    oinfo = probe_bytes(out, ".ogg")
    if abs(oinfo["duration"] - info["duration"]) > 0.08:
        raise RuntimeError(f"duration changed {info['duration']} -> {oinfo['duration']}")
    if len(out) >= len(data) or (ext == ".ogg" and info["codec"] == "opus" and len(out) > 0.9 * len(data)):
        return None, {"keep": True, "why": f"Opus {k}k ({len(out)} B) is not (or not 10 %) smaller than the source ({len(data)} B)", "src": info}
    return out, {"keep": False, "kbps": k, "src": info, "out": oinfo}


def visible_psnr(src_bytes: bytes, out_bytes: bytes, frame=None) -> float:
    """PSNR over the pixels that show (colour premultiplied by alpha: what is under a transparent pixel never shows)"""
    import numpy as np
    from PIL import Image
    def arr(b):
        im = Image.open(io.BytesIO(b))
        if frame is not None: im.seek(frame)
        a = np.asarray(im.convert("RGBA")).astype(np.float64)
        return np.concatenate([a[..., :3] * (a[..., 3:4] / 255.0), a[..., 3:4]], axis=-1)
    A, B = arr(src_bytes), arr(out_bytes)
    if A.shape != B.shape: return 0.0
    vis = (A[..., 3] > 0) | (B[..., 3] > 0)
    if not vis.any(): return 99.0
    mse = float(((A - B)[vis] ** 2).mean())
    return 99.0 if mse == 0 else 10 * math.log10(255 ** 2 / mse)


PSNR_MIN = 35.0      # a lossy WebP must keep at least this (visible pixels); else a higher quality, else lossless


def plan_still(data: bytes, name: str):
    lossless = name in LOSSLESS_NAMES
    if lossless:
        out = webp_still(data, True)
        from PIL import Image, ImageChops
        a = Image.open(io.BytesIO(data)).convert("RGBA")
        b = Image.open(io.BytesIO(out)).convert("RGBA")
        assert a.size == b.size and ImageChops.difference(a, b).getbbox() is None, f"{name}: lossless round trip differs"
        q, psnr = "lossless", 99.0
    else:
        # the smallest of q85 / q92 / lossless that keeps PSNR_MIN on the visible pixels (q85 nearly always does)
        cands = []
        for qq in (WEBP_Q, 92):
            o = webp_still(data, False, qq); p = visible_psnr(data, o)
            cands.append((len(o), o, qq, p))
            if p >= PSNR_MIN: break
        o = webp_still(data, True); cands.append((len(o), o, "lossless", 99.0))
        ok = [c for c in cands if c[3] >= PSNR_MIN]
        _, out, q, psnr = min(ok, key=lambda c: c[0])
    if len(out) >= len(data):
        return None, {"keep": True, "why": f"WebP ({len(out)} B) not smaller than {len(data)} B"}
    return out, {"keep": False, "lossless": q == "lossless", "quality": q, "psnr": round(psnr, 1)}


def plan_gif(data: bytes):
    """the smallest of q85 / q92 / lossless whose worst frame keeps PSNR_MIN"""
    cands = []
    for qq in (WEBP_Q, 92):
        o, info = webp_anim(data, qq); p = anim_psnr(data, o)
        cands.append((len(o), o, qq, p, info))
        if p >= PSNR_MIN: break
    o, info = webp_anim(data, None); cands.append((len(o), o, "lossless", 99.0, info))
    _, out, q, psnr, info = min((c for c in cands if c[3] >= PSNR_MIN), key=lambda c: c[0])
    if len(out) >= len(data):
        return None, {"keep": True, "why": f"animated WebP ({len(out)} B) not smaller than {len(data)} B", **info}
    return out, {"keep": False, "quality": q, "psnr": round(psnr, 1), "lossless": q == "lossless", **info}


def decide(kind: str, data: bytes, name: str, ext: str):
    """cached by the source's content + the settings"""
    key = sha(data)[:24] + "_" + sha(f"{SETTINGS_V}|{kind}|{OPUS_MONO_K}|{OPUS_STEREO_K}|{OPUS_REENCODE_ABOVE}|{WEBP_Q}|{name in LOSSLESS_NAMES}".encode() + (f"|bed{BED_K}>{BED_MIN_S}".encode() if kind == "audio" else IMAGE_V.encode()))[:8]
    out_ext = ".ogg" if kind == "audio" else ".webp"
    meta, out = cache_get(key, out_ext)
    if meta is not None:
        return out, meta
    if kind == "audio":
        out, meta = plan_audio(data, ext)
    elif kind == "gif":
        out, meta = plan_gif(data)
    else:
        out, meta = plan_still(data, name)
    meta["src_bytes"] = len(data)
    meta["out_bytes"] = len(out) if out is not None else len(data)
    cache_put(key, out_ext, meta, out)
    return out, meta


# ---------------------------------------------------------------- steps
def quarantine(dist: pathlib.Path, report: dict):
    lst = OPT / "unused_assets.txt"
    if not lst.exists():
        return set()
    names = [l.split("#")[0].strip() for l in lst.read_text(encoding="utf-8").splitlines()]
    names = [n for n in names if n]
    moved = 0
    for rel in names:
        p = dist / rel
        if p.exists():
            q = QUAR / rel
            q.parent.mkdir(parents=True, exist_ok=True)
            if not q.exists() or q.read_bytes() != p.read_bytes():
                shutil.copy2(p, q)
            p.unlink()
            moved += 1
    report["quarantined_now"] = moved
    report["quarantine_list"] = len(names)
    return set(names)


def restore(dist: pathlib.Path) -> int:
    """put the dist back as build.py expects it before a rebuild: every file the last run converted (its original) or quarantined is
    copied back from optimize_assets/originals/ and quarantine/ (build.py checks some of them exist); run() redoes it all at the end,
    from its cache"""
    dist = pathlib.Path(dist).resolve(); n = 0
    for base in (ORIG, QUAR):
        if not base.exists(): continue
        for p in base.rglob("*"):
            if not p.is_file(): continue
            d = dist / p.relative_to(base)
            if not d.exists() or d.stat().st_size != p.stat().st_size or d.read_bytes() != p.read_bytes():
                d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, d); n += 1
    log(f"restored {n} converted / quarantined files into the dist for the build")
    return n


def quarantined_names() -> set:
    lst = OPT / "unused_assets.txt"
    return {l.split("#")[0].strip() for l in lst.read_text(encoding="utf-8").splitlines() if l.split("#")[0].strip()} if lst.exists() else set()


def stash(dist: pathlib.Path, p: pathlib.Path):
    rel = p.relative_to(dist).as_posix()
    q = ORIG / rel
    data = p.read_bytes()
    if not q.exists() or q.read_bytes() != data:
        q.parent.mkdir(parents=True, exist_ok=True)
        q.write_bytes(data)


def convert_files(dist: pathlib.Path, report: dict):
    renames = json.loads(RENAMES_JSON.read_text(encoding="utf-8")) if RENAMES_JSON.exists() else {}
    rows = []
    files = sorted(p for p in (dist / "assets").rglob("*") if p.is_file() and p.suffix.lower() in MEDIA_EXT)
    produced = set()
    for p in files:
        rel = p.relative_to(dist).as_posix()
        ext = p.suffix.lower()
        if not p.exists() or rel in produced:
            continue                                            # written earlier in this run (a source's new name)
        data = p.read_bytes()
        if is_output(data):
            rows.append((rel, rel, len(data), len(data), "kept: already this step's output"))
            continue
        kind = "audio" if ext in (".mp3", ".ogg") else ("gif" if ext == ".gif" else "still")
        out, meta = decide(kind, data, p.name, ext)
        if out is None:
            rows.append((rel, rel, len(data), len(data), "kept: " + meta.get("why", "")))
            continue
        new = p.with_suffix(".ogg" if kind == "audio" else ".webp")
        nrel = new.relative_to(dist).as_posix()
        if new != p and new.exists() and new.read_bytes() != out and not is_output(new.read_bytes()):
            # a file that is not this step's own (older) output already holds the name: never overwrite a live asset
            raise SystemExit(f"[optimize] {nrel} already exists and differs from the conversion of {rel} — resolve by hand")
        assert len(out) < len(data)
        remember_output(out)
        if new != p:
            stash(dist, p)
            new.write_bytes(out)
            p.unlink()
            renames[rel] = nrel
            produced.add(nrel)
        else:
            stash(dist, p)
            p.write_bytes(out)
            produced.add(rel)
        rows.append((rel, nrel, len(data), len(out), "converted " + ("lossless" if meta.get("lossless") else "")))
    # a file converted in an earlier run whose source no longer comes back (it lived only in the dist): still renamed;
    # a source quarantined since is no rename any more
    for q in quarantined_names():
        renames.pop(q, None)
    for old, new in list(renames.items()):
        if not (dist / new).exists() and not (dist / old).exists():
            log(f"note: {old} -> {new}: neither exists now (asset removed?)")
    RENAMES_JSON.parent.mkdir(parents=True, exist_ok=True)
    RENAMES_JSON.write_text(json.dumps(renames, indent=1, sort_keys=True), encoding="utf-8")
    report["files"] = rows
    return renames


DATA_URI = re.compile(r"data:(image/png|audio/mpeg);base64,([A-Za-z0-9+/=]+)")


def convert_data_uris(text: str, report: dict, where: str) -> str:
    stats = report.setdefault("inline", [])

    def sub(m):
        mime, b64 = m.group(1), m.group(2)
        data = base64.b64decode(b64)
        if mime == "image/png":
            out, meta = _inline_png(data)
            new_mime = "image/webp"
        else:
            out, meta = decide("audio", data, "inline.mp3", ".mp3")
            new_mime = "audio/ogg"
        if out is None:
            stats.append((where, mime, len(data), len(data), "kept"))
            return m.group(0)
        stats.append((where, mime + "->" + new_mime, len(data), len(out), "converted"))
        return f"data:{new_mime};base64," + base64.b64encode(out).decode()
    return DATA_URI.sub(sub, text)


def _inline_png(data: bytes):
    """the inline PNGs are mask / rig sheets: lossless WebP, pixel-exact (checked), cached by content"""
    key = sha(data)[:24] + "_" + sha(f"{SETTINGS_V}|inline-png-lossless".encode())[:8]
    meta, out = cache_get(key, ".webp")
    if meta is not None:
        return out, meta
    from PIL import Image, ImageChops
    out = webp_still(data, True)
    a = Image.open(io.BytesIO(data)).convert("RGBA")
    b = Image.open(io.BytesIO(out)).convert("RGBA")
    assert a.size == b.size and ImageChops.difference(a, b).getbbox() is None, "inline png: lossless round trip differs"
    if len(out) >= len(data):
        meta = {"keep": True, "why": "not smaller"}
        cache_put(key, ".webp", meta, None)
        return None, meta
    meta = {"keep": False, "lossless": True, "src_bytes": len(data), "out_bytes": len(out)}
    cache_put(key, ".webp", meta, out)
    return out, meta


def rewrite_refs(texts: dict, renames: dict, dist: pathlib.Path) -> dict:
    """rename every reference to a renamed file: its full path, and its bare file name where that name is unique"""
    all_names = {}
    for p in (dist / "assets").rglob("*"):
        if p.is_file():
            all_names.setdefault(p.name, set()).add(p.relative_to(dist).as_posix())
    for q in list(renames.keys()):
        all_names.setdefault(pathlib.PurePosixPath(q).name, set()).add(q)
    for k, t in texts.items():
        for old, new in sorted(renames.items(), key=lambda kv: -len(kv[0])):
            t = t.replace(old, new)
            oname, nname = pathlib.PurePosixPath(old).name, pathlib.PurePosixPath(new).name
            if len(all_names.get(oname, ())) <= 1 or all(x in renames for x in all_names.get(oname, ())):
                t = re.sub(r"(?<![A-Za-z0-9_.-])" + re.escape(oname) + r"(?![A-Za-z0-9_])", nname, t)
        texts[k] = t
    return texts


# dead references the pruners cannot see (an element's first picture that code always replaces before it shows, a picture for an
# element that does not exist): each must match exactly once, or the build stops — the engine has changed and this needs a look
DEAD_PATCHES = [
    ("index.html", '<img id="phaseGateImg" src="assets/UI/peeking.webp" alt="">', '<img id="phaseGateImg" alt="">',
     "the gate's bird: GATE-REF-ANIM sets its own picture (peeking_talk_up.webp) before every gate; peeking.webp (2.8 MB) was fetched at load and never shown"),
    ("index.html", 'src="assets/UI/sw_lg_celebrating_anim.webp" alt="Swiftee"', 'alt=""',
     "the end screen's mascot <img>: the celebration's sprite runner hides it in the same task the screen opens; its animation was fetched at load and never shown"),
    ("app.js", '$("sgTitle").textContent = (CARD.title.hi || "").split(/[:：(]/)[0].trim();',
     '{ const _sgT = $("sgTitle"); if(_sgT) _sgT.textContent = (CARD.title.hi || "").split(/[:：(]/)[0].trim(); }   /* [optimize] the old landing title is gone (DEAD_BLOCKS) */',
     "boot()'s one unguarded write to the old landing title (the Figma cover hides .sg-content; DEAD_BLOCKS removes it)"),
    ("app.js", 'if(hi) hi.src = "assets/UI/hint_active.png";', '',
     "#hintImg exists nowhere (the hint button is an inline SVG): the two hint pictures could never be asked for"),
    ("app.js", 'if(hi) hi.src = "assets/UI/hint.png";', '', "(same)"),
]


# whole markup blocks no code shows any more: (the opening tag that starts the block, why); the block = that <div> to its matching </div>,
# with the comment line just above it
DEAD_BLOCKS = [
    ('<div class="hint-overlay" id="hintOverlay">',
     "the engine's hint card: its only user (showBox) went with the dead modules; no code names #hintOverlay / #hintBox / #hintMascot / #hintText"),
    ('<div class="sg-content">',
     "the reference landing's title / subtitle / concept strip: hidden under the Figma cover (.sg-fig .sg-content{display:none}), only boot() wrote into it"),
]


def remove_blocks(html: str, report: dict) -> str:
    done = []
    for opener, why in DEAD_BLOCKS:
        n = html.count(opener)
        if n != 1:
            raise SystemExit(f"[optimize] dead block matched {n} times: {opener!r} ({why})")
        a = html.index(opener)
        depth, k = 0, a
        for m in re.finditer(r"<div\b|</div>", html[a:]):
            depth += 1 if m.group(0) != "</div>" else -1
            if depth == 0:
                k = a + m.end(); break
        assert depth == 0, f"unbalanced block {opener}"
        line_a = html.rfind("\n", 0, a) + 1
        prev_a = html.rfind("\n", 0, line_a - 1) + 1                       # the comment line right above, if it is one
        if html[prev_a:line_a].strip().startswith("<!--") and html[prev_a:line_a].strip().endswith("-->"): line_a = prev_a
        line_k = html.find("\n", k); line_k = len(html) if line_k < 0 else line_k + 1
        if html[k:line_k].strip() and not html[k:line_k].strip().startswith("<!--"): line_k = k   # keep whatever follows on that line
        html = html[:line_a] + html[line_k:]
        done.append(opener)
    report["dead_blocks"] = done
    return html


def stub_overridden(js: str, report: dict, html: str = "") -> str:
    """the engine's original phaseBlurTransition and CELEBRATION.mount are replaced at load (GATE-REF-ANIM, the celebration port);
    their old bodies (with the retired gate / end-screen pictures) can never run: kept as one-line stubs (the override's typeof
    guard still finds a function)"""
    sys.path.insert(0, str(SCR))
    from js_prune import _code_end
    done = []
    if "window.phaseBlurTransition = function" in js:
        m = re.search(r"^function phaseBlurTransition\(cb, toPhase\)\{", js, re.M)
        assert m, "stub: phaseBlurTransition"
        end = _code_end(js, m.end() - 1)
        js = js[:m.start()] + "function phaseBlurTransition(cb){ if(cb) cb(); }   /* [optimize] replaced at load by [GATE-REF-ANIM]'s gate (window.phaseBlurTransition) */" + js[end:]
        done.append("phaseBlurTransition")
    m = re.search(r"^function fingerCount\(n, cls\)\{", js, re.M)
    if m and '"landing_hero"' not in html:                                      # only a counting game's landing (CARD.landing_hero) calls it
        end = _code_end(js, m.end() - 1)
        js = js[:m.start()] + "function fingerCount(n){ return `<span class=\"num-glyph\">${n}</span>`; }   /* [optimize] its finger pictures (hand_1..5.png) never shipped; only a counting game's landing (CARD.landing_hero, none here) called it */" + js[end:]
        done.append("fingerCount")
    if "SlideModules.CELEBRATION.mount = function" in js:
        m = re.search(r"^  CELEBRATION: \{\n    mount\(host, slide\)\{", js, re.M)
        assert m, "stub: CELEBRATION.mount"
        end = _code_end(js, m.end() - 1)
        js = js[:m.start()] + "  CELEBRATION: {\n    mount(host, slide){}   /* [optimize] replaced at load by the celebration port (SlideModules.CELEBRATION.mount = ...) */" + js[end:]
        done.append("CELEBRATION.mount")
    report["stubbed"] = done
    return js


def prune_registry(html: str, quarantined: set, report: dict) -> str:
    """the card's asset registry (assets.audio / assets.image: id -> path) loses the entries of quarantined files (no slide and no code
    names those ids), and their audio_text; re-serialised exactly as build.py writes it (json.dumps, ensure_ascii=False)"""
    m = re.search(r'(<script type="application/json" id="cardData">)(.*?)(</script>)', html, re.S)
    assert m, "the card data"
    card = json.loads(m.group(2))
    dropped = []
    A = card.get("assets", {})
    for kind in ("audio", "image"):
        reg = A.get(kind, {})
        for i, p in list(reg.items()):
            if isinstance(p, str) and p in quarantined:
                del reg[i]; dropped.append(i)
                if kind == "audio" and isinstance(A.get("audio_text"), dict): A["audio_text"].pop(i, None)
    report["registry_dropped"] = dropped
    return html[:m.start(2)] + json.dumps(card, ensure_ascii=False) + html[m.end(2):]


def apply_dead_patches(texts: dict, report: dict) -> dict:
    for f, old, new, why in DEAD_PATCHES:
        n = texts[f].count(old)
        if n != 1:
            raise SystemExit(f"[optimize] dead-reference patch matched {n} times in {f}: {old[:80]!r} ({why})")
        texts[f] = texts[f].replace(old, new)
    report["dead_patches"] = [(f, why) for f, _, _, why in DEAD_PATCHES]
    return texts


REF_RE = re.compile(r"assets/(?:UI|Audio|Images)/[A-Za-z0-9_.&%-]+")


def audit_refs(texts: dict, dist: pathlib.Path, report: dict):
    """every literal assets/... path must exist (a path that is only a prefix of a dynamic name ends in '/' or '_'
    and is not matched by REF_RE's file-name part)"""
    missing = []
    for k, t in texts.items():
        for m in REF_RE.finditer(t):
            rel = urllib.parse.unquote(m.group(0))
            if rel.endswith(("_", "-", ".")) or "." not in rel.rsplit("/", 1)[-1]:
                continue
            if not (dist / rel).exists():
                ctx = t[max(0, m.start() - 70): m.end() + 30].replace("\n", " ")
                missing.append((k, rel, ctx))
    report["missing_refs"] = missing
    return missing


# fetched first, before the smallest-first queue: what the cover itself asks for before the bar can be full (the bird's wave
# animation is set as the loader fades, the welcome plays then)
PRELOAD_FIRST = ("assets/UI/new_landing_swiftee_anim.webp", "assets/Audio/vo_landing.ogg")


def build_manifest(dist: pathlib.Path, exclude: set):
    rows = []
    for p in sorted((dist / "assets").rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(dist).as_posix()
        if rel in exclude:
            continue
        ms = 0
        if p.suffix.lower() in (".ogg", ".mp3"):
            key = "dur_" + sha(p.read_bytes())[:24]
            meta, _ = cache_get(key, ".none")
            if meta is None:
                meta = {"ms": int(round(ffprobe(p)["duration"] * 1000))}
                cache_put(key, ".none", meta, None)
            ms = meta["ms"]
        rows.append([urllib.parse.quote(rel), p.stat().st_size, ms, 1 if rel in PRELOAD_FIRST else 0])
    return rows


def inject(dist: pathlib.Path, texts: dict, manifest: list):
    head = (OPT / "preload_head.js").read_text(encoding="utf-8")
    tail = (OPT / "preload_tail.js").read_text(encoding="utf-8")
    pcss = (OPT / "preload.css").read_text(encoding="utf-8")
    assert "__PRELOAD_MANIFEST__" in head
    head = head.replace("__PRELOAD_MANIFEST__", json.dumps(manifest, separators=(",", ":")))
    assert texts["app.js"].count("[preload-head]") == 0, "app.js already has the preloader"
    texts["app.js"] = head + "\n" + texts["app.js"] + "\n" + tail
    texts["style.css"] = texts["style.css"] + "\n" + pcss
    btn = '<button class="sg-btn" id="sgBtn"'
    assert texts["index.html"].count(btn) == 1, "the play button anchor"
    bar = ('<div class="sg-load" id="sgLoad" role="progressbar" aria-label="लोड हो रहा है" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">'
           '<div class="sg-load-track"><div class="sg-load-fill"></div><div class="sg-load-shine"></div></div>'
           '<div class="sg-load-pct" aria-hidden="true">0%</div></div>\n        ')   # [preload] the loading bar, in the play button's place
    texts["index.html"] = texts["index.html"].replace(btn, bar + btn)
    return texts


def css_url_assets(css: str) -> set:
    out = set()
    for m in re.finditer(r"url\(\s*[\"']?(assets/[^\"')]+)", css):
        out.add(urllib.parse.quote(urllib.parse.unquote(m.group(1))))
    return out


def skip_set() -> set:
    """paths build.py's reference-asset step must not bring back: the renamed sources and the quarantined files"""
    s = set()
    if RENAMES_JSON.exists():
        s.update(json.loads(RENAMES_JSON.read_text(encoding="utf-8")).keys())
    lst = OPT / "unused_assets.txt"
    if lst.exists():
        s.update(l.split("#")[0].strip() for l in lst.read_text(encoding="utf-8").splitlines() if l.split("#")[0].strip())
    return s


def run(dist: pathlib.Path, report_path=None):
    dist = pathlib.Path(dist).resolve()
    report = {}
    before = {p.relative_to(dist).as_posix(): p.stat().st_size for p in dist.rglob("*") if p.is_file()}
    quarantined = quarantine(dist, report)
    renames = convert_files(dist, report)
    texts = {n: (dist / n).read_text(encoding="utf-8") for n in ("index.html", "style.css", "app.js")}
    assert "[preload-head]" not in texts["app.js"], "optimize.run() needs the freshly built app.js (it is already optimised)"
    texts["style.css"] = convert_data_uris(texts["style.css"], report, "style.css")
    texts["app.js"] = convert_data_uris(texts["app.js"], report, "app.js")
    # dead code: the slide modules / functions no data uses, then the CSS nothing can match any more (js_prune.py, css_prune.py)
    import importlib.util as ilu
    def _mod(name):
        spec = ilu.spec_from_file_location(name, SCR / f"{name}.py"); m = ilu.module_from_spec(spec); spec.loader.exec_module(m); return m
    n_js, n_css = len(texts["app.js"]), len(texts["style.css"])
    texts = apply_dead_patches(texts, report)
    texts["index.html"] = remove_blocks(texts["index.html"], report)
    texts["index.html"] = prune_registry(texts["index.html"], quarantined, report)
    texts["app.js"] = stub_overridden(texts["app.js"], report, texts["index.html"])
    texts["app.js"], report["js_prune"] = _mod("js_prune").prune(texts["app.js"], texts["index.html"])
    texts["style.css"], report["css_prune"] = _mod("css_prune").prune(texts["style.css"], texts["index.html"], texts["app.js"])
    log(f"dead code: app.js {n_js} -> {len(texts['app.js'])} chars ({len(report['js_prune']['modules_removed'])} modules, "
        f"{len(report['js_prune']['functions_removed'])} functions), style.css {n_css} -> {len(texts['style.css'])} chars "
        f"({report['css_prune']['rules_removed']} rules, {len(report['css_prune']['keyframes_removed'])} keyframes, {len(report['css_prune']['vars_removed'])} properties)")
    texts = rewrite_refs(texts, renames, dist)
    # the audit reads the code without its comments (a note may still name a retired file)
    code = {"index.html": re.sub(r"<!--.*?-->", " ", texts["index.html"], flags=re.S),
            "style.css": re.sub(r"/\*.*?\*/", " ", texts["style.css"], flags=re.S),
            "app.js": _mod("js_prune").strip_js_comments(texts["app.js"])}
    missing = audit_refs(code, dist, report)
    if missing:
        for k, rel, ctx in missing:
            log(f"MISSING {rel} in {k}: …{ctx}…")
        raise SystemExit(f"[optimize] {len(missing)} reference(s) to files that do not exist")
    # a quarantined file must be named nowhere; a file named nowhere (not even by its stem: dynamic names) is reported
    final = code["index.html"] + "\n" + code["style.css"] + "\n" + code["app.js"]
    named = [q for q in quarantined if re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(pathlib.PurePosixPath(q).name) + r"(?![A-Za-z0-9_])", final)]
    if named:
        raise SystemExit(f"[optimize] quarantined but still referenced: {named}")
    unref = []
    for p in sorted((dist / "assets").rglob("*")):
        if p.is_file() and p.name not in final and not re.search(r"(?<![A-Za-z0-9_])" + re.escape(p.stem) + r"(?![A-Za-z0-9_])", final):
            unref.append(p.relative_to(dist).as_posix())
    report["named_nowhere"] = unref
    if unref:
        log(f"named nowhere (dynamic names expected, e.g. sw_head_<mood>[_anim].webp): {unref}")
    excl_path = OPT / "preload_exclude.txt"
    exclude = set()
    if excl_path.exists():
        exclude = {l.split("#")[0].strip() for l in excl_path.read_text(encoding="utf-8").splitlines() if l.split("#")[0].strip()}
    manifest = build_manifest(dist, exclude)
    texts = inject(dist, texts, manifest)
    for n, t in texts.items():
        (dist / n).write_text(t, encoding="utf-8")
    after = {p.relative_to(dist).as_posix(): p.stat().st_size for p in dist.rglob("*") if p.is_file()}
    report["bytes_before"] = sum(before.values())
    report["bytes_after"] = sum(after.values())
    report["manifest_files"] = len(manifest)
    report["manifest_bytes"] = sum(m[1] for m in manifest)
    conv = [r for r in report["files"] if r[2] != r[3]]
    log(f"{len(conv)} files converted ({sum(r[2] for r in conv)/1024:.0f} KB -> {sum(r[3] for r in conv)/1024:.0f} KB), "
        f"{report['quarantined_now']} quarantined now, {len(report.get('inline', []))} inline media, "
        f"preload {len(manifest)} files {report['manifest_bytes']/1048576:.2f} MB; dist {report['bytes_before']/1048576:.2f} -> {report['bytes_after']/1048576:.2f} MB")
    if report_path:
        pathlib.Path(report_path).write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    shutil.rmtree(CACHE / "_tmp", ignore_errors=True)
    return report


if __name__ == "__main__":
    d = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else SCR.parent / "HI02H05_L03_S01_dist"
    run(d, sys.argv[2] if len(sys.argv) > 2 else None)
