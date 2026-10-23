"""B안 메인(스티커 마을)을 납품 배치 좌표 그대로 조립한다 (2026-10-23).

소유자 지시: "메인은 제공될 스티커 마을 배경과 다람이 분리 에셋을 사용하세요." 납품(b-ui-main-v2)의
layout_1280x720.json 좌표와 크기를 그대로 쓴다(투명 여백 포함 캔버스 기준). 층 순서는 배경 → 로고 → 다람 →
메뉴 판 → 버튼 → 글자. 버튼 글자는 Pretendard SemiBold 25.

  python3 dev/make_bstyle_main_exact.py FONT_DIR ORIGINAL_MOCKUP OUT_DIR
"""
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
M = ROOT.parents[1] / 'design/resource-intake-20261023/b-ui-main-v2'
FONT, MOCK, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
INK = (52, 38, 30)
WHITE = (255, 250, 242)


def visible(im):
    return im.crop(im.getchannel('A').point(lambda a: 255 if a > 24 else 0).getbbox())


def slice_into(base, im, box, ins):
    l, t, r, bt = ins
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    w, h = x1 - x0, y1 - y0
    sw, sh = im.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for sx0, sx1, dx0, dx1 in ((0, l, 0, l), (l, sw - r, l, w - r), (sw - r, sw, w - r, w)):
        for sy0, sy1, dy0, dy1 in ((0, t, 0, t), (t, sh - bt, t, h - bt), (sh - bt, sh, h - bt, h)):
            if min(dx1 - dx0, dy1 - dy0, sx1 - sx0, sy1 - sy0) > 0:
                out.alpha_composite(im.crop((sx0, sy0, sx1, sy1)).resize((dx1 - dx0, dy1 - dy0), Image.LANCZOS), (dx0, dy0))
    base.alpha_composite(out, (x0, y0))


def row_version(lay, W, H):
    """원본 시안 배치: 메뉴 판 없이 아래쪽에 버튼 한 줄(원본에서 잰 보이는 영역 y618–667).
    원본의 찢어진 종이 띠, 버튼 아이콘(재생·새싹·폴더·톱니), 도토리·여우·부엉이·발자국 스티커는 납품에 없어 그리지 않는다."""
    b = Image.new('RGBA', (W, H))
    for l in lay['layers']:
        if l['file'].endswith('b_main_panel.png'):
            continue
        im = Image.open(M / l['file']).convert('RGBA').resize((l['width'], l['height']), Image.LANCZOS)
        b.alpha_composite(im, (l['x'], l['y']))
    f = ImageFont.truetype(str(FONT / 'Pretendard-Bold.otf'), 24)
    for (x0, x1), t, primary in (((120, 258), '이어하기', True), ((267, 409), '처음부터', False),
                                  ((418, 564), '불러오기', False), ((572, 684), '설정', False)):
        im = visible(Image.open(M / ('assets/b_button_primary.png' if primary else 'assets/b_button.png')).convert('RGBA'))
        slice_into(b, im, (x0, 618, x1, 667), (12, 10, 12, 10))
        d = ImageDraw.Draw(b)
        bb = f.getbbox(t)
        d.text(((x0 + x1) / 2 - (bb[2] - bb[0]) / 2 - bb[0], 642.5 - (bb[1] + bb[3]) / 2), t, font=f,
               fill=WHITE if primary else INK)
    return b


def main():
    lay = json.loads((M / 'layout_1280x720.json').read_text())
    W, H = lay['canvas']
    b = Image.new('RGBA', (W, H))
    for l in lay['layers']:
        im = Image.open(M / l['file']).convert('RGBA').resize((l['width'], l['height']), Image.LANCZOS)
        b.alpha_composite(im, (l['x'], l['y']))
    # 소유자 2026-10-23 "수첩 크기를 작게 하든, 아이콘을 키우든 해서 좀 꽉 채워줘": 납품 좌표의 버튼은 판 안에서
    # 작아 빈 곳이 많았다. 판의 종이 안쪽(보이는 영역 x120–578, y455–640)을 2×2 로 채우도록 버튼을 키운다.
    fb = ImageFont.truetype(str(FONT / 'Pretendard-Bold.otf'), 30)
    boxes = [(120, 455, 341, 538), (357, 455, 578, 538), (120, 556, 341, 639), (357, 556, 578, 639)]
    for bt, box in zip(lay['buttons'], boxes):
        im = visible(Image.open(M / bt['file']).convert('RGBA'))
        slice_into(b, im, box, (14, 10, 14, 10))
        d = ImageDraw.Draw(b)
        t = bt['text']; bb = fb.getbbox(t)
        cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
        d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[1] + bb[3]) / 2), t, font=fb,
               fill=WHITE if 'primary' in bt['file'] else INK)
    OUT.mkdir(parents=True, exist_ok=True)
    row = row_version(lay, W, H)
    row.convert('RGB').save(OUT / '05_메인_재현_원본배치.png')
    ours = b.convert('RGB')
    ours.save(OUT / '05_메인_재현.png')
    mock = Image.open(MOCK).convert('RGB').resize((W, H), Image.LANCZOS)
    pair = Image.new('RGB', (W * 3 + 40, H + 50), (30, 26, 24))
    pair.paste(mock, (0, 50)); pair.paste(row.convert('RGB'), (W + 20, 50)); pair.paste(ours, (W * 2 + 40, 50))
    d = ImageDraw.Draw(pair)
    f = ImageFont.truetype(str(FONT / 'Pretendard-SemiBold.otf'), 24)
    d.text((20, 12), '① 원본 시안 · 스티커 마을 메인', font=f, fill=(240, 232, 220))
    d.text((W + 40, 12), '② 원본 배치 재현(버튼 한 줄, 판 없음)', font=f, fill=(240, 232, 220))
    d.text((W * 2 + 60, 12), '③ 수첩 메뉴 판(버튼을 판 안쪽에 꽉 채움)', font=f, fill=(240, 232, 220))
    pair.save(OUT / '05_메인_비교.png')
    print(OUT / '05_메인_비교.png')


if __name__ == '__main__':
    main()
