"""G4's picture in the reference game's P4 frame: the picture shown bare at 315px high, its grey frame IN the bitmap.
usage: python -I g4_picture.py <source picture> [g4_assets/img_g4_kite_gry.webp] [width]

P4's own picture (pic_bird_peck_gry.webp, read from the live page) is 1570x1058 with a #DADADA ring baked in: outer corner
radius 86, ring 15, inner (picture) corner radius 69, transparent outside the ring — fitted against that bitmap (mean alpha
error 0.36 / 255 over the frame band). The page shows it at height 315 / width auto, so the source keeps its own shape: it
is scaled to the same 1058px height (the frame then lands on screen exactly as P4's) and the ring is drawn over its edge.
[pics-pinki] Given a width (this lesson's frames are 1411 wide, from 1448x1086 sources), a source of another shape covers
width x 1058 instead, centred, so its frame lands exactly where the earlier one did; the trim (the 1447x1087 kite: about a
pixel top and bottom) is under the ring.
"""
import sys, pathlib
from PIL import Image, ImageDraw

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path(__file__).resolve().parent / "g4_assets" / "img_g4_kite_gry.webp"
H, R_OUT, RING, R_IN, GREY, SS = 1058, 86, 15, 69, (218, 218, 218), 4

pic = Image.open(SRC).convert("RGB")
if len(sys.argv) > 3:   # [pics-pinki] cover W x H: the centred band of the source with the frame's shape
    W = int(sys.argv[3]); sw, sh = min(pic.width, pic.height * W / H), min(pic.height, pic.width * H / W)
    pic = pic.resize((W, H), Image.LANCZOS, box=((pic.width - sw) / 2, (pic.height - sh) / 2, (pic.width + sw) / 2, (pic.height + sh) / 2))
else:
    W = round(pic.width * H / pic.height)
    pic = pic.resize((W, H), Image.LANCZOS)

def mask(box, r):   # an anti-aliased rounded-rect mask (drawn 4x, then reduced)
    m = Image.new("L", (W * SS, H * SS), 0)
    ImageDraw.Draw(m).rounded_rectangle([v * SS for v in box], radius=r * SS, fill=255)
    return m.resize((W, H), Image.LANCZOS)

outer = mask((0, 0, W - 1 / SS, H - 1 / SS), R_OUT)
inner = mask((RING, RING, W - RING - 1 / SS, H - RING - 1 / SS), R_IN)
img = Image.new("RGBA", (W, H), GREY + (0,))
img.paste(Image.new("RGBA", (W, H), GREY + (255,)), (0, 0), outer)     # the grey card
img.paste(pic.convert("RGBA"), (0, 0), inner)                          # the picture inside the ring
OUT.parent.mkdir(exist_ok=True)
img.save(OUT, "WEBP", quality=90, method=6)
print(OUT, img.size)
