"""Record icon for Mom's memo M01 (0.18.48): a folded note with handwriting and the small acorn
she draws for Daram. Same look as room13-pixel-evidence0155 (dark outline, cream paper, big pixels).
Writes assets/room13-record-m01.webp (362x362, 36x36 grid at 10px). Run: python3 dev/make_memo_icon.py
"""
from pathlib import Path
from PIL import Image, ImageDraw
GAME = Path(__file__).resolve().parents[1] / "game"
G, S = 36, 10
INK, PAPER, SHADE, FOLD, LINE = (52, 32, 24, 255), (240, 222, 178, 255), (216, 190, 140, 255), (196, 168, 120, 255), (60, 52, 50, 255)
CAP, NUT, NUTL = (110, 66, 34, 255), (196, 132, 66, 255), (226, 170, 96, 255)
img = Image.new("RGBA", (G, G), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
# paper: a folded sheet, left page lit, right page in shade, dark outline all round
d.rectangle([5, 7, 31, 30], fill=INK)
d.rectangle([6, 8, 18, 29], fill=PAPER)
d.rectangle([19, 8, 30, 29], fill=SHADE)
d.line([(18, 8), (18, 29)], fill=FOLD)
d.line([(6, 29), (30, 29)], fill=FOLD)
# handwriting lines
for y in (11, 14, 17, 20, 23):
    d.line([(8, y), (16 if y != 23 else 13, y)], fill=LINE)
for y in (11, 14):
    d.line([(21, y), (28, y)], fill=LINE)
# the acorn mark Mom draws for Daram, bottom right
d.rectangle([21, 18, 28, 20], fill=INK)
d.rectangle([22, 18, 27, 19], fill=CAP)
d.point([(24, 17), (25, 17)], fill=INK)
d.polygon([(22, 21), (27, 21), (27, 24), (25, 26), (24, 26), (22, 24)], fill=INK)
d.polygon([(23, 21), (26, 21), (26, 24), (25, 25), (24, 25), (23, 24)], fill=NUT)
d.point([(23, 22), (23, 23)], fill=NUTL)
big = img.resize((G * S, G * S), Image.NEAREST)
out = Image.new("RGBA", (362, 362), (0, 0, 0, 0)); out.paste(big, (1, 1), big)
out.save(GAME / "assets/room13-record-m01.webp", "WEBP", lossless=True)
print("written")
