#!/usr/bin/env python3
"""도트 연출 프레임 생성기 (0.18.29).

원본 배경·인물 그림은 바꾸지 않는다. 원본 위에 올리는 프레임만 game/assets에 쓴다.

  python3 dev/make_dot_fx.py          # 전부 다시 만든다(결과는 항상 같다: 시드 고정)

만드는 것
- 여관 로비 벽난로: 시간대별(아침·오후·저녁) 12프레임 불꽃 시트.
  원래 그려진 불꽃 픽셀의 밝기만 4px 칸 단위로 위로 흐르게 바꾼다(팔레트 순환).
  쇠살대·장작(어두운 픽셀)은 항상 원본 그대로 앞에 남는다.
- 여관 저녁 불빛 번짐, 광장 저녁 가로등 빛: 4단계로 끊은 빛 판.
- 눈송이 2종(4px, 8px 십자).
- 다람이 대화 전신 눈 깜빡임: 표정마다 반쯤 감음·감음 2장(눈 주변만 잘라 둔 조각).
  joy는 원래 눈을 감고 있어 만들지 않는다.
- (0.18.31) 굴뚝 연기 조각, 증거 획득 반짝임 6프레임, 시간 전환용 4x4 디더 판.

좌표는 모두 원본 그림 픽셀 기준이다. 연결은 game/systems/room13_dot_fx.rpy.
"""
import json
import os

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "game", "assets")
CELL = 4
META_FILE = os.path.join(ASSETS, "room13-dot-fx.json")


def save(img, name):
    img.save(os.path.join(ASSETS, name), "WEBP", lossless=True, quality=100, method=6)
    return "assets/" + name


def load_rgb(name):
    return np.array(Image.open(os.path.join(ASSETS, name)).convert("RGB")).astype(int)


# ------------------------------------------------------------------ 벽난로
FIRE_RECT = (72, 252, 128, 156)   # 아궁이 안쪽 (2048x768 원본, 4의 배수)
FIRE_FRAMES = 12
FIRE_FPS = 9


def fire_sheet(period, seed=13):
    rng = np.random.default_rng(seed)
    src = load_rgb("room13-pixel-panorama-inn-%s.webp" % period)
    fx, fy, fw, fh = FIRE_RECT
    patch = src[fy:fy + fh, fx:fx + fw].copy()
    r = patch[..., 0]
    lum = patch.sum(2)
    edge_l = patch[:, 0:6].mean(1)
    edge_r = patch[:, -6:].mean(1)
    t = np.linspace(0, 1, fw)[None, :, None]
    wall = edge_l[:, None, :] * (1 - t) + edge_r[:, None, :] * t
    flame = (lum > wall.sum(2) + 40) & (r > 200)
    gw, gh = fw // CELL, fh // CELL
    # 세로로 이어지는 주기 노이즈: 프레임마다 2칸씩 위로 흘러 12프레임이 이음매 없이 돈다.
    period_rows = FIRE_FRAMES * 2
    noise = rng.random((period_rows, gw))
    noise = (noise + np.roll(noise, 1, 1) + np.roll(noise, -1, 1)) / 3
    noise = (noise + np.roll(noise, 1, 0)) / 2
    steps = np.array([.78, .90, 1.0, 1.10, 1.20])
    cells = flame.reshape(gh, CELL, gw, CELL).mean((1, 3)) > .25
    tip = cells & ~np.vstack([np.zeros((1, gw), bool), cells[:-1]])
    above_tip = np.vstack([tip[1:], np.zeros((1, gw), bool)]) & ~cells
    sparks = [(int(gw * .42), 0), (int(gw * .55), 5), (int(gw * .48), 9)]
    sheet = Image.new("RGB", (fw * FIRE_FRAMES, fh))
    light = []
    for f in range(FIRE_FRAMES):
        img = patch.astype(float).copy()
        nf = np.array([noise[(y + f * 2) % period_rows] for y in range(gh)])
        lvl = np.clip((nf * len(steps)).astype(int), 0, len(steps) - 1)
        fac = steps[lvl].repeat(CELL, 0).repeat(CELL, 1)[..., None]
        img[flame] = np.clip(img * fac, 0, 255)[flame]
        for y, x in zip(*np.nonzero(tip)):
            if nf[y, x] < .33:
                sl = (slice(y * CELL, (y + 1) * CELL), slice(x * CELL, (x + 1) * CELL))
                img[sl] = wall[sl]
        for y, x in zip(*np.nonzero(above_tip)):
            if nf[y, x] > .68:
                img[y * CELL:(y + 1) * CELL, x * CELL:(x + 1) * CELL] = (255, 196, 70)
        for sx, ph in sparks:
            k = (f + ph) % FIRE_FRAMES
            if k < 7:
                yy = gh - 12 - k * 2
                xx = sx + (1 if (k // 2) % 2 else 0)
                if 0 <= yy < gh:
                    img[yy * CELL:(yy + 1) * CELL, xx * CELL:(xx + 1) * CELL] = \
                        (255, 214, 110) if k < 4 else (232, 120, 40)
        img[lum < 300] = patch[lum < 300]
        sheet.paste(Image.fromarray(img.astype("uint8")), (f * fw, 0))
        light.append(float((steps[lvl] * cells).sum()))
    lo, hi = min(light), max(light)
    light = [round((v - lo) / (hi - lo + 1e-9), 2) for v in light]
    return save(sheet, "room13-fx-inn-fire-%s.webp" % period), light


def glow_plate(size, centers, color, block, name):
    w, h = size
    yy, xx = np.mgrid[0:h:block, 0:w:block]
    g = np.zeros(yy.shape)
    for cx, cy, rx, ry, power in centers:
        d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
        g = np.maximum(g, np.clip(1 - d, 0, 1) ** power)
    a = (np.floor(g * 4) / 4 * 255).astype("uint8")
    img = Image.new("RGBA", (a.shape[1], a.shape[0]), color + (0,))
    img.putalpha(Image.fromarray(a))
    return save(img.resize((w, h), Image.NEAREST), name)


# ------------------------------------------------------------------ 눈송이
def flakes():
    small = Image.new("RGBA", (4, 4), (226, 236, 250, 255))
    big = np.zeros((8, 8, 4), "uint8")
    big[0:8, 2:6] = (246, 250, 255, 255)
    big[2:6, 0:8] = (246, 250, 255, 255)
    big[0:2, 2:6] = (214, 228, 248, 255)
    big[6:8, 2:6] = (214, 228, 248, 255)
    return save(small, "room13-fx-snow-small.webp"), save(Image.fromarray(big), "room13-fx-snow-big.webp")


# ------------------------------------------------------------------ 눈 깜빡임
EYE_SEARCH = (140, 100, 440, 290)
# 0.18.37: 대화가 많은 인물. 자동으로 만든 뒤 사람이 본 결과 어색한 조합은 BLINK_SKIP에 적는다.
# 0.18.37 검수: karo(눈썹·깃털 오검출), granny·doto(안경), seryeon(머리카락이 눈을 가림), neoul·서리(눈가 무늬)는
# 자동 결과가 어색해 뺐다. joy는 모두 원래 눈을 감은 웃는 눈이라 뺐다.
BLINK_MORE = ("buri", "mom", "nabi", "bami")
BLINK_SKIP = {(p, "joy") for p in BLINK_MORE} | {("mom", "flustered")}
LID = (26, 18, 24)


def blink_pieces(person, emotion, search=None, general=False):
    name = "room13-fullbody-%s-%s.webp" % (person, emotion)
    spr = np.array(Image.open(os.path.join(ASSETS, name)).convert("RGBA")).astype(int)
    x0, y0, x1, y1 = search or EYE_SEARCH
    reg = spr[y0:y1, x0:x1]
    lum = reg[..., :3].sum(2)
    opaque = reg[..., 3] > 200
    dark = (lum < 150) & opaque
    white = (lum > 700) & (np.abs(reg[..., 0] - reg[..., 2]) < 24) & opaque
    lab, n = ndimage.label(dark)
    sizes = ndimage.sum(dark, lab, range(1, n + 1))
    boxes = ndimage.find_objects(lab)
    eyes = []
    for i, s in enumerate(sizes):
        ys, xs = boxes[i]
        h, w = ys.stop - ys.start, xs.stop - xs.start
        # 눈동자: 덩어리가 꽉 차 있고 크기가 25~90px. 머리 윤곽선(가늘고 긴 덩어리)은 빠진다.
        if s > 600 and 25 <= h <= 90 and 20 <= w <= 90 and s / float(h * w) > .35:
            eyes.append(i + 1)
    if general:
        # 다른 인물: 크기 기준을 넓히고, 높이가 비슷하고 좌우로 떨어진 두 덩어리를 한 쌍으로 고른다.
        eyes = []
        for i, sz in enumerate(sizes):
            ys, xs = boxes[i]
            h, w = ys.stop - ys.start, xs.stop - xs.start
            if 120 <= sz <= 4000 and 10 <= h <= 90 and 8 <= w <= 90 and sz / float(h * w) > .35:
                eyes.append(i + 1)
        best = None
        for a in eyes:
            for b in eyes:
                if a >= b:
                    continue
                ya = (boxes[a - 1][0].start + boxes[a - 1][0].stop) / 2.0
                yb = (boxes[b - 1][0].start + boxes[b - 1][0].stop) / 2.0
                xa = (boxes[a - 1][1].start + boxes[a - 1][1].stop) / 2.0
                xb = (boxes[b - 1][1].start + boxes[b - 1][1].stop) / 2.0
                ratio = min(sizes[a - 1], sizes[b - 1]) / max(sizes[a - 1], sizes[b - 1])
                if abs(ya - yb) <= 22 and 34 <= abs(xa - xb) <= 200 and ratio > .45:
                    score = sizes[a - 1] + sizes[b - 1] - abs(ya - yb) * 20
                    if best is None or score > best[0]:
                        best = (score, [a, b])
        eyes = best[1] if best else []
    else:
        eyes = sorted(eyes, key=lambda i: -sizes[i - 1])[:2]
    if len(eyes) != 2:
        return None
    union = np.zeros(dark.shape, bool)
    masks = []
    for e in eyes:
        m = lab == e
        ys, xs = ndimage.find_objects(m.astype(int))[0]
        box = np.zeros_like(m)
        box[max(0, ys.start - 8):ys.stop + 6, max(0, xs.start - 22):xs.stop + 22] = True
        seed = m | (white & box)
        if general:
            # 색 있는 홍채(주황·파랑 등): 눈동자 둘레 6px 안에서 위쪽 털색과 크게 다른 픽셀.
            fur_band = reg[max(0, ys.start - 14):max(1, ys.start - 4), xs.start:xs.stop, :3].reshape(-1, 3)
            fur_c = np.median(fur_band, axis=0) if len(fur_band) else np.array([128, 128, 128])
            near_m = ndimage.binary_dilation(m, iterations=6) & box & opaque
            far = np.abs(reg[..., :3] - fur_c).sum(2) > 150
            seed = seed | (near_m & far & (lum < 600))
        eye = ndimage.binary_closing(seed, iterations=2)
        eye = ndimage.binary_fill_holes(eye)
        lab2, _ = ndimage.label(eye)
        eye = lab2 == lab2[m][0]
        # 화난 표정처럼 눈썹이 눈 테두리에 붙어 있으면 같이 잡힌다. 흰자 윗선보다 6px 넘게
        # 위에 있는 부분은 눈이 아니므로 뺀다(눈썹은 원본 그대로 남는다).
        sclera = np.nonzero((white & eye).any(1))[0]
        if len(sclera):
            eye[:max(0, sclera.min() - 6)] = False
            lab3, _ = ndimage.label(eye)
            sizes3 = ndimage.sum(eye, lab3, range(1, lab3.max() + 1))
            eye = lab3 == (int(np.argmax(sizes3)) + 1)
        big = ndimage.binary_dilation(eye, iterations=7 if general else 4)   # 눈 테두리 안티에일리어싱까지
        masks.append((eye, big))
        union |= big
    # 눈을 덮는 털색은 눈 밖에서 가장 가까운 픽셀에서 가져온다. 속눈썹·눈썹 같은 검은 선은
    # 색의 출처에서 뺀다. 위 눈꺼풀은 눈 위쪽 털에서만, 감은 눈 아래쪽은 가장 가까운 쪽에서
    # 가져와 갈색 털과 크림색 얼굴의 경계가 원래 방향대로 이어진다(오른쪽 눈 갈색 겹침 수정).
    rows = np.arange(reg.shape[0])[:, None] * np.ones((1, reg.shape[1]), int)
    source = ~union & (lum >= 260) & opaque
    _, (iy, ix) = ndimage.distance_transform_edt(~source, return_indices=True)
    near = reg[iy, ix]
    out = {"half": reg.copy(), "closed": reg.copy()}
    for eye, big in masks:
        # 눈꺼풀은 한 가지 털색으로 칠한다(픽셀아트의 평평한 면). 위쪽 털색은 눈 바로 위 띠의
        # 중앙값, 아래쪽은 가장 가까운 바깥 픽셀이 밝으면 얼굴 크림색, 어두우면 털색.
        band_rows = np.nonzero(big.any(1))[0]
        top_e = band_rows.min()
        cols_e = np.nonzero(big.any(0))[0]
        ring = np.zeros_like(big)
        ring[max(0, top_e - 12):top_e, cols_e.min():cols_e.max() + 1] = True
        fur_src = ring & source & ~((reg[..., 0] > 170) & (reg[..., 1] < 90))
        fur = np.median(reg[fur_src][:, :3], axis=0) if fur_src.any() else np.array([150, 90, 50])
        around = ndimage.binary_dilation(big, iterations=8) & ~big & source
        light = around & (lum > 560)
        cream = np.median(reg[light][:, :3], axis=0) if light.any() else fur
        upper = np.zeros_like(reg)
        upper[..., :3] = fur
        upper[..., 3] = 255
        lower = np.zeros_like(reg)
        lower[..., :3] = np.where((near[..., :3].sum(2) > 560)[..., None], cream, fur)
        lower[..., 3] = 255
        rr, cc = np.nonzero(eye)
        top, bottom, left, right = rr.min(), rr.max(), cc.min(), cc.max()
        cx, hw = (left + right) / 2, (right - left) / 2
        for kind, (frac, depth) in (("half", (.46, 0)), ("closed", (.58, 8))):
            frame = out[kind]
            lid = {}
            for x in range(left - 1, right + 2):
                u = (x - cx) / (hw + 1e-9)
                lid[x] = int(top + (bottom - top) * frac + depth * max(0.0, 1 - u * u)) // 4 * 4
            # 눈 밖으로 번진 테두리 안에 있는 검은 선(눈썹·속눈썹 끝)은 원본 그대로 둔다.
            # 검은 선만(채도 낮음). 남색 홍채 끝 같은 색 픽셀은 덮는다.
            spread = reg[..., :3].max(2) - reg[..., :3].min(2)
            keep = big & ~eye & (lum < 110) & (spread < 45)
            klab, kn = ndimage.label(keep)
            if kn:
                ksz = ndimage.sum(keep, klab, range(1, kn + 1))
                eye_top = np.nonzero(eye.any(1))[0].min()
                cy = ndimage.center_of_mass(keep, klab, range(1, kn + 1))
                # 굵고 눈 위로 떨어진 선(눈썹)만 남긴다. 눈 윗테두리 조각은 덮는다.
                keep = np.isin(klab, [i + 1 for i, v in enumerate(ksz) if v >= 25 and (not general or cy[i][0] < eye_top - 2)])
            ys, xs = np.nonzero(big & ~keep)
            for y, x in zip(ys, xs):
                edge = lid.get(x, lid[left - 1] if x < left else lid[right + 1])
                if y < edge:
                    frame[y, x] = upper[y, x]
                elif kind == "closed":
                    frame[y, x] = lower[y, x]
            prev = None
            for x in range(left - 1, right + 2):
                if not 0 <= x < frame.shape[1]:
                    continue
                yl = lid[x]
                lo, hi = (yl, yl) if prev is None else (min(prev, yl), max(prev, yl))
                frame[lo:hi + 4, x, :3] = LID
                frame[lo:hi + 4, x, 3] = 255
                prev = yl
    ys, xs = np.nonzero(union)
    bx0, by0 = int(xs.min()) - 4, int(ys.min()) - 4
    bx1, by1 = int(xs.max()) + 5, int(ys.max()) + 9
    rect = [x0 + bx0, y0 + by0, bx1 - bx0, by1 - by0]
    files = {}
    for kind, frame in out.items():
        piece = Image.fromarray(frame[by0:by1, bx0:bx1].astype("uint8"), "RGBA")
        files[kind] = save(piece, "room13-fx-blink-%s-%s-%s.webp" % (person, emotion, kind))
    return {"rect": rect, **files}


# ------------------------------------------------------------------ 0.18.31
SMOKE_SOURCES = {
    # 광장 집 굴뚝 꼭대기(원본 2048x768 좌표). 입구는 연기가 이미 그려져 있어 넣지 않는다.
    "square": [[1475, 64], [696, 188], [1562, 99]],
}


def smoke_puffs():
    """연기 덩어리 3크기 x 3진하기. 둥근 도트 덩어리(4px 칸)."""
    files = {}
    shapes = {
        4: ["#"],
        8: [".##.", "####", "####", ".##."],
        12: ["..##..", ".####.", "######", "######", ".####.", "..##.."],
    }
    for px, rows in shapes.items():
        cell = px // len(rows) if px > 4 else 4
        for level, alpha in enumerate((110, 170, 220)):
            n = len(rows)
            img = Image.new("RGBA", (n * cell, n * cell), (0, 0, 0, 0))
            for y, row in enumerate(rows):
                for x, ch in enumerate(row):
                    if ch == "#":
                        for yy in range(y * cell, (y + 1) * cell):
                            for xx in range(x * cell, (x + 1) * cell):
                                img.putpixel((xx, yy), (214, 219, 230, alpha))
            files["%d-%d" % (px, level)] = save(img, "room13-fx-smoke-%d-%d.webp" % (px, level))
    return files


def sparkle_sheet():
    """증거 카드 아이콘 둘레 4각 별 반짝임 6프레임(128x128)."""
    stars = [(20, 30, 0), (100, 22, 1), (110, 92, 2), (28, 104, 1), (64, 8, 3), (8, 66, 2)]
    frames = 6
    sheet = Image.new("RGBA", (128 * frames, 128), (0, 0, 0, 0))
    gold, white = (255, 226, 140, 255), (255, 252, 236, 255)
    for f in range(frames):
        for sx, sy, delay in stars:
            k = f - delay
            if k < 0 or k > 2:
                continue
            arm = (1, 2, 1)[k]                       # 별 팔 길이(칸)
            ox = f * 128
            def cell(cx, cy, color):
                for yy in range(cy, cy + 4):
                    for xx in range(cx, cx + 4):
                        if 0 <= xx - ox < 128 and 0 <= yy < 128:
                            sheet.putpixel((xx, yy), color)
            cx, cy = ox + sx // 4 * 4, sy // 4 * 4
            cell(cx, cy, white)
            for a in range(1, arm + 1):
                for dx, dy in ((4 * a, 0), (-4 * a, 0), (0, 4 * a), (0, -4 * a)):
                    cell(cx + dx, cy + dy, gold)
    return save(sheet, "room13-fx-evidence-sparkle.webp")


def dither_plate():
    """시간 전환 ImageDissolve용 4x4 Bayer 판(4px 칸, 1280x720)."""
    bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
    tile = ((bayer + .5) / 16 * 255).astype("uint8").repeat(4, 0).repeat(4, 1)
    plate = np.tile(tile, (720 // 16, 1280 // 16))
    img = Image.fromarray(plate, "L")
    img.save(os.path.join(ASSETS, "room13-fx-dither.png"), optimize=True)
    return "assets/room13-fx-dither.png"


# ------------------------------------------------------------------ 0.18.37
# 실내 저녁 등불(원본 좌표). 검수한 등만 적는다.
LAMPS = {
    "school": [[1563, 199, 260]], "workshop": [[245, 137, 220], [1222, 268, 220]],
    "clinic": [[1015, 385, 240]], "store": [[1032, 100, 300]],
    "greenhouse": [[516, 311, 220]], "facility": [[730, 222, 240]],
}
INN_WINDOW = (648, 156, 456, 212)       # 여관 로비 창·문 유리 영역(x, y, w, h)


def lamp_plates():
    out = {}
    for loc, lamps in LAMPS.items():
        size = (2048, 768)
        rel = "assets/room13-pixel-ready-%s0177-evening.webp" % loc
        if os.path.exists(os.path.join(ROOT, "game", rel)):
            size = Image.open(os.path.join(ROOT, "game", rel)).size
        else:
            layout = json.load(open(os.path.join(ASSETS, "room13-world-layout.json"), encoding="utf-8"))
            size = Image.open(os.path.join(ROOT, "game", layout[loc]["files"]["evening"])).size
        centers = [(x, y, r, r, 1.6) for x, y, r in lamps]
        out[loc] = {"file": glow_plate(size, centers, (255, 186, 90), 4, "room13-fx-lamp-%s.webp" % loc),
                    "periods": ["evening"], "alpha": [0.10, 0.28]}
    return out


def window_mask():
    x, y, w, h = INN_WINDOW
    a = load_rgb("room13-pixel-panorama-inn-evening.webp")[y:y + h, x:x + w]
    pane = (a[..., 2] > a[..., 0] + 25) & (a[..., 2] > 70) & (a.sum(2) < 380)
    pane = ndimage.binary_opening(pane, iterations=1)
    img = Image.fromarray((pane * 255).astype("uint8"), "L").convert("RGBA")
    img.putalpha(Image.fromarray((pane * 255).astype("uint8"), "L"))
    return save(img, "room13-fx-inn-window-mask.webp")


def reaction_sounds():
    """짧은 8비트 반응음(소리 크기 작게). 22050Hz 16bit mono."""
    import wave
    rate = 22050
    def tone(segs, vol=.22):
        out = []
        for f0, f1, dur in segs:
            n = int(rate * dur)
            for i in range(n):
                f = f0 + (f1 - f0) * i / max(1, n)
                ph = (sum_ph[0] + f / rate) % 1.0
                sum_ph[0] = ph
                env = min(1.0, i / 60.0) * min(1.0, (n - i) / 120.0)
                out.append((1 if ph < .5 else -1) * vol * env)
        return out
    sounds = {
        "surprise": [(420, 420, .03), (520, 1240, .09)],
        "joy": [(660, 660, .05), (0, 0, .025), (990, 990, .06)],
        "angry": [(150, 120, .05), (0, 0, .02), (150, 120, .05), (0, 0, .02), (140, 110, .06)],
        "anxious": [(520, 470, .05), (0, 0, .03), (500, 440, .06)],
        "flustered": [(700, 560, .05), (560, 700, .05), (700, 560, .05)],
    }
    files = {}
    for name, segs in sounds.items():
        sum_ph = [0.0]
        data = []
        for f0, f1, dur in segs:
            if f0 == 0:
                data += [0.0] * int(rate * dur)
            else:
                data += tone([(f0, f1, dur)])
        pcm = (np.array(data) * 32767).astype("<i2").tobytes()
        path = os.path.join(ASSETS, "sfx-react-%s.wav" % name)
        w = wave.open(path, "wb")
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm); w.close()
        files[name] = "assets/sfx-react-%s.wav" % name
    return files


# 장면 그림(시네마틱) 연출: 등불 일렁임과 바깥 장면 눈. 좌표는 그 장면의 잘라낸 그림(832x466) 기준.
CINE_LAMPS = {
    "return": [[110, 80, 90]], "rescue": [[468, 110, 90]], "reunion": [[786, 180, 90]],
    "mountain": [[790, 244, 90]], "E0": [[724, 144, 80]], "E2": [[606, 224, 90]],
    "E3": [[162, 218, 60], [324, 292, 60], [658, 48, 70]], "E4": [[316, 318, 80]],
    "E5": [[786, 302, 80], [456, 58, 70]], "proof": [[92, 132, 150]],
}
CINE_SNOW = ("mountain", "E0", "E2")


def cine_plates():
    items = {it["id"]: it for it in json.load(open(os.path.join(ASSETS, "room13-cinematics.json"), encoding="utf-8"))["items"]}
    out = {}
    for key, lamps in CINE_LAMPS.items():
        if key not in items:
            continue
        w, h = items[key]["rect"][2:]
        out[key] = {"lamp": glow_plate((w, h), [(x, y, r, r, 1.6) for x, y, r in lamps], (255, 190, 96), 2,
                                       "room13-fx-cine-%s.webp" % key.lower()),
                    "alpha": [0.12, 0.32], "snow": key in CINE_SNOW}
    for key in CINE_SNOW:
        out.setdefault(key, {"snow": True})
    return out


# ------------------------------------------------------------------ 0.18.39 오프닝 컷씬
def carriage_window_mask():
    """빈 마차 안 그림(1386x780)을 1280x720으로 줄인 화면 기준, 창밖(밝은 하늘·눈·마을) 영역."""
    im = Image.open(os.path.join(ASSETS, "room13-pixel-carriage-empty-winter.webp")).convert("RGB").resize((1280, 720), Image.NEAREST)
    a = np.array(im).astype(int)
    sky = (a[..., 2] > 150) & (a[..., 2] > a[..., 0] + 20)
    lab, n = ndimage.label(sky)
    sizes = ndimage.sum(sky, lab, range(1, n + 1))
    keep = lab == (int(np.argmax(sizes)) + 1)
    ys, xs = np.nonzero(keep)
    box = np.zeros_like(keep)
    box[ys.min():ys.max() + 1, xs.min():xs.max() + 1] = True
    # 창틀(갈색 나무)만 빼고 창 안쪽 전체: 하늘에서 시작해 창틀 안쪽 사각형을 채운다.
    frame = (a[..., 0] > a[..., 2] + 40) & (a.sum(2) < 420)
    window = box & ~frame
    window = ndimage.binary_opening(window, iterations=2)
    img = Image.new("RGBA", (1280, 720), (255, 255, 255, 0))
    img.putalpha(Image.fromarray((window * 255).astype("uint8"), "L"))
    return save(img, "room13-fx-carriage-window-mask.webp"), [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


# ------------------------------------------------------------------ 0.18.41 메인 타이틀
# 타이틀 그림(1280x720 화면 기준)의 등불·창. 검수한 자리만.
TITLE_LIGHTS = [(418, 372, 70), (418, 622, 80), (992, 449, 70), (1187, 433, 70),
                (1089, 205, 90), (1100, 480, 110), (697, 283, 50)]


def title_glow():
    return glow_plate((1280, 720), [(x, y, r, r, 1.6) for x, y, r in TITLE_LIGHTS], (255, 186, 90), 4,
                      "room13-fx-title-glow.webp")


# ------------------------------------------------------------------ 0.18.47 그림책 톤
def _smooth_noise(w, h, cell, seed):
    rng = np.random.default_rng(seed)
    small = rng.random((h // cell + 2, w // cell + 2))
    img = Image.fromarray((small * 255).astype("uint8"), "L").resize((w + 2 * cell, h + 2 * cell), Image.BICUBIC)
    return np.array(img).astype(float)[cell:cell + h, cell:cell + w] / 255.0


def bleed_mask():
    """종이에 물감이 번지듯 바뀌는 전환(ImageDissolve) 판. 흰 곳부터 바뀐다: 가운데에서 바깥으로, 가장자리는 얼룩지게."""
    w, h = 1280, 720
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / 1.42
    n = .55 * _smooth_noise(w, h, 160, 3) + .3 * _smooth_noise(w, h, 48, 4) + .15 * _smooth_noise(w, h, 12, 5)
    v = 1.0 - (r * .62 + n * .38)
    v = (v - v.min()) / (v.max() - v.min())
    Image.fromarray((v * 255).astype("uint8"), "L").save(os.path.join(ASSETS, "room13-fx-bleed.png"), optimize=True)
    return "assets/room13-fx-bleed.png"


def storybook_frame():
    """그림책 장면 테두리: 가장자리가 따뜻한 어둠으로 얼룩지게 스며드는 비네트(가운데는 투명)."""
    w, h = 1280, 720
    yy, xx = np.mgrid[0:h, 0:w]
    dx = np.minimum(xx, w - 1 - xx) / 130.0
    dy = np.minimum(yy, h - 1 - yy) / 100.0
    d = np.minimum(dx, dy)
    n = _smooth_noise(w, h, 40, 9) * .55 + _smooth_noise(w, h, 10, 10) * .45
    a = np.clip(1.0 - d + (n - .5) * .55, 0, 1) ** 1.6
    rgba = np.zeros((h, w, 4), "uint8")
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = 26, 18, 12
    rgba[..., 3] = (a * 235).astype("uint8")
    return save(Image.fromarray(rgba, "RGBA"), "room13-fx-storybook-frame.webp")


def soft_glow(size, color, name, power=1.8):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a = np.clip(1 - r, 0, 1) ** power
    rgba = np.zeros((h, w, 4), "uint8")
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = color
    rgba[..., 3] = (a * 255).astype("uint8")
    return save(Image.fromarray(rgba, "RGBA"), name)


def edge_vignette():
    """제시·반박 순간: 화면 가장자리가 따뜻하게 어두워졌다 걷힌다."""
    w, h = 1280, 720
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / 1.42
    a = np.clip((r - .35) / .65, 0, 1) ** 1.5
    rgba = np.zeros((h, w, 4), "uint8")
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = 30, 18, 10
    rgba[..., 3] = (a * 255).astype("uint8")
    return save(Image.fromarray(rgba, "RGBA"), "room13-fx-edge-vignette.webp")


def main():
    meta = {"version": 1, "cell": CELL, "generator": "dev/make_dot_fx.py"}
    fire = {}
    for period in ("morning", "afternoon", "evening"):
        sheet, light = fire_sheet(period)
        fire[period] = {"sheet": sheet, "light": light}
    meta["inn_fire"] = {"rect": list(FIRE_RECT), "frames": FIRE_FRAMES, "fps": FIRE_FPS, "periods": fire}
    meta["inn_glow"] = {"file": glow_plate((2048, 768), [(140, 360, 900, 520, 2)], (255, 150, 60), 8,
                                           "room13-fx-inn-glow.webp"),
                        "periods": ["evening"], "alpha": [0.0, 0.10]}
    small, big = flakes()
    meta["snow"] = {"small": small, "big": big, "periods": ["evening"],
                    "locations": ["square", "gate", "altar"],
                    "layers": [{"count": 140, "size": 4, "vy": [26, 40], "sway": 10},
                               {"count": 28, "size": 8, "vy": [56, 80], "sway": 18}]}
    meta["lamp_glow"] = {"square": {"file": glow_plate((2048, 768), [(1137, 362, 120, 120, 1.6)],
                                                       (255, 196, 96), 4, "room13-fx-square-lampglow.webp"),
                                    "periods": ["evening"], "alpha": [0.18, 0.42]}}
    blink = {}
    for emotion in ("neutral", "flustered", "angry", "anxious", "surprise"):
        piece = blink_pieces("daram", emotion)
        if piece:
            blink.setdefault("daram", {})[emotion] = piece
    fullbody = json.load(open(os.path.join(ASSETS, "room13-fullbody-dialogue.json"), encoding="utf-8"))["people"]
    for person in BLINK_MORE:
        fx_, fy_, fw_, fh_ = fullbody[person]["figure"]
        search = (fx_, fy_, fx_ + fw_, fy_ + int(fh_ * .45))
        for emotion in ("neutral", "joy", "flustered", "angry", "anxious", "surprise"):
            if (person, emotion) in BLINK_SKIP:
                continue
            piece = blink_pieces(person, emotion, search, general=True)
            if piece:
                blink.setdefault(person, {})[emotion] = piece
    meta["smoke"] = {"sources": SMOKE_SOURCES, "puffs": smoke_puffs(),
                     "periods": ["morning", "afternoon", "evening"],
                     "every": .9, "life": 4.5, "rise": 72, "drift": 18}
    meta["evidence_sparkle"] = {"sheet": sparkle_sheet(), "frames": 6, "fps": 12, "size": [128, 128]}
    meta["dither"] = {"file": dither_plate(), "time": .5}
    meta["lamps"] = lamp_plates()
    meta["inn_window"] = {"rect": list(INN_WINDOW), "mask": window_mask(), "periods": ["evening"],
                          "layers": [{"count": 34, "size": 4, "vy": [22, 34], "sway": 6}]}
    # 0.18.39 (owner): synthesized reaction sounds removed (reaction_sounds() kept, unused).
    meta["cinematics"] = cine_plates()
    mask, box = carriage_window_mask()
    meta["storybook"] = {"bleed": bleed_mask(), "frame": storybook_frame(),
                         "card_glow": soft_glow((360, 360), (255, 214, 140), "room13-fx-card-glow.webp"),
                         "vignette": edge_vignette()}
    meta["title"] = {"glow": title_glow(), "alpha": [0.10, 0.30]}
    meta["opening"] = {"carriage_window": {"mask": mask, "box": box}}
    meta["blink"] = {"timeline": [["half", .05], ["closed", .09], ["half", .05]],
                     "interval": [2.6, 5.2], "people": blink}
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print("wrote", META_FILE, "blink:", {k: sorted(v) for k, v in blink.items()})


if __name__ == "__main__":
    main()
