"""A SENT_PICK page's picture for the side row ([p2-side] / [g4p1-side]): the user's picture bare (the row's white card frames it,
so no baked grey ring as g4_picture.py draws for P4's layout), exactly 4:3 at 1448x1086 — the card shows it at 444x333 — WebP q90.
A source of another shape is cut to its centred 4:3 band first (G4's 1447x1087 kite: half a pixel top and bottom); a 1448x1086
source is only re-encoded.
usage: python -I sent_bare_picture.py <source png> <out webp>"""
import sys, pathlib
from PIL import Image

W, H = 1448, 1086
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
pic = Image.open(src).convert("RGB")
if pic.size != (W, H):
    sw, sh = min(pic.width, pic.height * W / H), min(pic.height, pic.width * H / W)
    pic = pic.resize((W, H), Image.LANCZOS, box=((pic.width - sw) / 2, (pic.height - sh) / 2, (pic.width + sw) / 2, (pic.height + sh) / 2))
pic.save(out, "WEBP", quality=90, method=6)
print(out, pic.size)
