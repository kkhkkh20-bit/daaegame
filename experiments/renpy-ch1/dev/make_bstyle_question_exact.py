"""승인된 B안 질문창 시안을 1280×720 에 그대로 재현한다 (2026-10-23).

소유자 지시: "새로 디자인하지 말고 승인된 B안 시안을 재현해 주세요. 같은 1280×720 기준으로 패널·글자·버튼의
위치와 크기, 안쪽 여백을 시안과 맞춰 주세요. 에셋 파일의 투명 여백이 아니라 실제 그림이 보이는 영역을 기준으로
배치하세요. ... 먼저 질문창 한 화면만 원본 시안과 나란히 비교해서 보여 주세요. 부족한 부품은 임의의 사각형으로
대체하지 말고 정확히 요청해 주세요."

좌표는 원본 시안(1672×941, 16:9)을 0.7656 배로 줄인 1280×720 에서 잰 값이다. 부품은 알파 24 넘는 보이는 영역으로
잘라 그 영역을 목표 상자에 맞춘다. 납품에 없는 부품(카드 속 선화, 점선, 이름표, 문서 아이콘 등)은 그리지 않는다.

  python3 dev/make_bstyle_question_exact.py FONT_DIR MOCKUP_PNG OUT_DIR
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'game/assets'
B = ROOT.parents[1] / 'design/resource-intake-20261023/b-ui/assets'
S = ROOT.parents[1] / 'design/resource-intake-20261023/b-ui-stickers/assets'
FONT, MOCK, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
W, H = 1280, 720
INK = (52, 38, 30)
INK_DONE = (120, 104, 92)
WHITE = (255, 250, 242)


def font(weight, size):
    return ImageFont.truetype(str(FONT / f'Pretendard-{weight}.otf'), size)


def visible(path):
    im = Image.open(path).convert('RGBA')
    return im.crop(im.getchannel('A').point(lambda a: 255 if a > 24 else 0).getbbox())


def slice_into(base, im, box, ins):
    """보이는 그림(im)을 box 에 9-slice 로 맞춘다. ins 는 보이는 그림 기준 (왼, 위, 오, 아래)."""
    l, t, r, b = ins
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    w, h = x1 - x0, y1 - y0
    sw, sh = im.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for sx0, sx1, dx0, dx1 in ((0, l, 0, l), (l, sw - r, l, w - r), (sw - r, sw, w - r, w)):
        for sy0, sy1, dy0, dy1 in ((0, t, 0, t), (t, sh - b, t, h - b), (sh - b, sh, h - b, h)):
            if min(dx1 - dx0, dy1 - dy0, sx1 - sx0, sy1 - sy0) > 0:
                out.alpha_composite(im.crop((sx0, sy0, sx1, sy1)).resize((dx1 - dx0, dy1 - dy0), Image.LANCZOS), (dx0, dy0))
    base.alpha_composite(out, (x0, y0))


def part(base, name, box, ins):
    slice_into(base, visible(B / f'{name}.png'), box, ins)


def icon(base, name, cx, cy, h, folder=B, angle=0):
    im = visible(folder / f'{name}.png')
    im = im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)
    if angle:
        im = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def text_mid(d, x, cy, s, f, fill):
    top = f.getbbox(s)[1]; bot = f.getbbox(s)[3]
    d.text((x, cy - (top + bot) / 2), s, font=f, fill=fill)


def text_center(d, box, s, f, fill, dx=0):
    x0, y0, x1, y1 = box
    tw = d.textlength(s, font=f)
    text_mid(d, (x0 + x1 - tw) / 2 + dx, (y0 + y1) / 2, s, f, fill)


def cover(path):
    im = Image.open(path).convert('RGB')
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x, y, x + W, y + H)).convert('RGBA')


def question():
    b = cover(A / 'room13-pixel-panorama-square-afternoon.webp')
    # 인물: 원본 캐릭터(게임 스프라이트)를 쓴다. 시안의 상반신 그림은 납품 부품이 아니다.
    bori = visible(A / 'room13-canonical-default-resident_bori.webp')
    k = 575 / bori.height
    bori = bori.resize((round(bori.width * k), 575), Image.LANCZOS)
    b.alpha_composite(bori, (int(270 - bori.width / 2), 720 - 575))
    # 수첩(보이는 영역 x485–1230, y157–655)
    part(b, 'b_panel_book', (485, 157, 1230, 655), (86, 81, 97, 26))
    # 제목 탭(x562–922, y130–202), 도토리 아이콘 중심 (607,166), 글자 왼쪽 650
    part(b, 'b_tab_title', (562, 130, 922, 202), (30, 8, 30, 8))
    icon(b, 'b_icon_acorn', 607, 166, 36)
    d = ImageDraw.Draw(b)
    text_mid(d, 650, 166, '묻고 싶은 이야기', font('Bold', 31), WHITE)
    # 오른쪽 위 테이프는 수첩 그림(b_panel_book)에 이미 붙어 있다(시안은 빨강, 납품은 청록).
    # 질문 카드 세 장(x552–1185), 도토리 중심 x616, 글자 왼쪽 661
    cards = [('b_panel_card_hover', (249, 332), '마을에 관해서', False),
             ('b_panel_card_done', (349, 432), '장터에 관해서', True),
             ('b_panel_card', (450, 535), '이곳의 겨울에 관해서', False)]
    for name, (y0, y1), q, done in cards:
        part(b, name, (552, y0, 1185, y1), (41, 15, 13, 9))
        cy = (y0 + y1) / 2
        icon(b, 'b_icon_acorn_done' if done else 'b_icon_acorn', 616, cy, 40)
        d = ImageDraw.Draw(b)
        text_mid(d, 661, cy, q, font('SemiBold', 27), INK_DONE if done else INK)
    # 아래 버튼 넷(y569–615)
    buttons = [((552, 724), '자료 보여주기', True, None), ((735, 870), '기록', False, 'b_icon_book'),
               ((881, 1029), '더보기', False, 'b_icon_more'), ((1040, 1195), '돌아가기', False, 'b_icon_back')]
    for (x0, x1), t, primary, ic in buttons:
        part(b, 'b_button_primary' if primary else 'b_button', (x0, 569, x1, 615), (14, 10, 14, 10))
        d = ImageDraw.Draw(b)
        f = font('SemiBold', 19)
        tw = d.textlength(t, font=f)
        iw = 0
        if ic:
            v = visible(B / f'{ic}.png'); iw = round(v.width * 26 / v.height)
        group = tw + (iw + 9 if ic else 0)
        gx = (x0 + x1 - group) / 2
        if ic:
            icon(b, ic, gx + iw / 2, 592, 26)
        d = ImageDraw.Draw(b)
        text_mid(d, gx + (iw + 9 if ic else 0), 592, t, f, WHITE if primary else INK)
    # 오른쪽 책갈피(x1230–1270, y470–590)
    icon(b, 'sticker_bookmark', 1250, 530, 128, folder=S, angle=8)
    # 이름 리본(시안의 종이 이름표는 납품에 없어 납품된 이름 리본을 쓴다)
    part(b, 'b_ribbon_name', (100, 612, 236, 660), (10, 6, 30, 6))
    d = ImageDraw.Draw(b)
    text_mid(d, 124, 636, '보리', font('Bold', 25), WHITE)
    return b


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ours = question().convert('RGB')
    ours.save(OUT / '03_질문창_재현.png')
    mock = Image.open(MOCK).convert('RGB').resize((W, H), Image.LANCZOS)
    pair = Image.new('RGB', (W * 2 + 20, H + 50), (30, 26, 24))
    pair.paste(mock, (0, 50)); pair.paste(ours, (W + 20, 50))
    d = ImageDraw.Draw(pair)
    d.text((20, 12), '원본 시안(1672×941 → 1280×720)', font=font('SemiBold', 24), fill=(240, 232, 220))
    d.text((W + 40, 12), '재현(실제 게임 배경·인물 + 납품 부품, 보이는 영역 기준)', font=font('SemiBold', 24), fill=(240, 232, 220))
    pair.save(OUT / '03_질문창_비교.png')
    print(OUT / '03_질문창_비교.png')


if __name__ == '__main__':
    main()
