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
LID = (26, 18, 24)


def blink_pieces(person, emotion):
    name = "room13-fullbody-%s-%s.webp" % (person, emotion)
    spr = np.array(Image.open(os.path.join(ASSETS, name)).convert("RGBA")).astype(int)
    x0, y0, x1, y1 = EYE_SEARCH
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
        eye = ndimage.binary_closing(m | (white & box), iterations=2)
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
        big = ndimage.binary_dilation(eye, iterations=4)   # 눈 테두리 안티에일리어싱까지
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
            keep = big & ~eye & (lum < 110)
            klab, kn = ndimage.label(keep)
            if kn:
                ksz = ndimage.sum(keep, klab, range(1, kn + 1))
                keep = np.isin(klab, [i + 1 for i, v in enumerate(ksz) if v >= 25])
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
    meta["blink"] = {"timeline": [["half", .05], ["closed", .09], ["half", .05]],
                     "interval": [2.6, 5.2], "people": blink}
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print("wrote", META_FILE, "blink:", {k: sorted(v) for k, v in blink.items()})


if __name__ == "__main__":
    main()
