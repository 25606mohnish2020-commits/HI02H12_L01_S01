"""[optimize] (2026-11-15) before / after sizes: the dist's media by type, the code, what a player downloads, what Vercel deploys.
usage: python -I -X utf8 optimize_sizes.py <old dist folder> <new dist folder> [<repo root> for the deploy set]"""
import fnmatch, gzip, json, pathlib, re, subprocess, sys

old, new = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
repo = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
TYPE = {".ogg": "audio (ogg)", ".mp3": "audio (mp3)", ".wav": "audio (wav)", ".webp": "images (webp)", ".png": "images (png)",
        ".gif": "images (gif)", ".svg": "images (svg)", ".woff2": "fonts", ".js": "code", ".css": "code", ".html": "code"}
SKIP_DIRS = ("voiceovers_batch",)
def inventory(d):
    rows = {}
    for p in d.rglob("*"):
        if not p.is_file(): continue
        rel = p.relative_to(d).as_posix()
        if rel.startswith(SKIP_DIRS) or p.suffix.lower() in (".pptx", ".xlsx"): continue   # design docs / raw recordings: never deployed
        rows[rel] = p.stat().st_size
    return rows
A, B = inventory(old), inventory(new)
def by_type(rows):
    out = {}
    for rel, s in rows.items():
        k = TYPE.get(pathlib.PurePosixPath(rel).suffix.lower(), "other")
        out.setdefault(k, [0, 0]); out[k][0] += 1; out[k][1] += s
    return out
ta, tb = by_type(A), by_type(B)
MB = lambda b: f"{b / 1048576:7.2f} MB"
print(f"{'type':16s} {'before':>22s} {'after':>22s}")
for k in sorted(set(ta) | set(tb)):
    a, b = ta.get(k, [0, 0]), tb.get(k, [0, 0])
    print(f"{k:16s} {a[0]:4d} files {MB(a[1])}   {b[0]:4d} files {MB(b[1])}")
print(f"{'dist total':16s} {len(A):4d} files {MB(sum(A.values()))}   {len(B):4d} files {MB(sum(B.values()))}")
for f in ("index.html", "style.css", "app.js"):
    a, b = (old / f).read_bytes(), (new / f).read_bytes()
    print(f"  {f:11s} {len(a)/1024:7.0f} KB (gzip {len(gzip.compress(a, 9))/1024:5.0f}) -> {len(b)/1024:7.0f} KB (gzip {len(gzip.compress(b, 9))/1024:5.0f})")
# what a player downloads: the new build preloads its manifest; the old one fetched whatever the pages asked for (all of it at most)
m = re.search(r"var MANIFEST = (\[.*?\]);", (new / "app.js").read_text(encoding="utf-8"))
man = json.loads(m.group(1)) if m else []
print(f"preloaded by the new build: {len(man)} files {MB(sum(x[1] for x in man))} (+ code {MB(sum((new / f).stat().st_size for f in ('index.html', 'style.css', 'app.js')))})")
if repo:
    git = lambda *a: subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True).stdout
    head = [l.split(None, 4) for l in git("ls-tree", "-r", "-l", "HEAD").splitlines()]
    head_bytes = sum(int(x[3]) for x in head if x[3].isdigit())
    files = git("ls-files", "-c", "-o").splitlines()                       # the working tree: tracked + new files
    ign = set(git("ls-files", "-c", "-o", "-i", "--exclude-from=.vercelignore").splitlines())
    keep = [f for f in files if f not in ign and (repo / f).exists()]
    print(f"deployed to Vercel: today (HEAD, no .vercelignore: every file of the commit) {len(head)} files {MB(head_bytes)}; "
          f"after (the working tree through .vercelignore) {len(keep)} files {MB(sum((repo / f).stat().st_size for f in keep))}")
