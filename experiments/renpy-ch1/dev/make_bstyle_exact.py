"""승인된 B안 질문창 시안을 1280×720 에 그대로 재현한다 (2026-10-23).

소유자 지시: "새로 디자인하지 말고 승인된 B안 시안을 재현해 주세요. 같은 1280×720 기준으로 패널·글자·버튼의
위치와 크기, 안쪽 여백을 시안과 맞춰 주세요. 에셋 파일의 투명 여백이 아니라 실제 그림이 보이는 영역을 기준으로
배치하세요. ... 먼저 질문창 한 화면만 원본 시안과 나란히 비교해서 보여 주세요. 부족한 부품은 임의의 사각형으로
대체하지 말고 정확히 요청해 주세요."

좌표는 원본 시안(1672×941, 16:9)을 0.7656 배로 줄인 1280×720 에서 잰 값이다. 부품은 알파 24 넘는 보이는 영역으로
잘라 그 영역을 목표 상자에 맞춘다. 납품에 없는 부품(카드 속 선화, 점선, 이름표, 문서 아이콘 등)은 그리지 않는다.

  python3 dev/make_bstyle_exact.py FONT_DIR ORIGINAL_DIR OUT_DIR
ORIGINAL_DIR 에 원본 시안(01_대사창, 04_조사창, 05_질문창, 06_선택창 .png)이 있어야 한다.
2026-10-23 소유자 "응 마음에 들어": 질문창과 같은 방법으로 대사창·선택창·조사창도 재현한다.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'game/assets'
B = ROOT.parents[1] / 'design/resource-intake-20261023/b-ui/assets'
S = ROOT.parents[1] / 'design/resource-intake-20261023/b-ui-stickers/assets'
Q = ROOT.parents[1] / 'design/resource-intake-20261023/b-ui-question-v2/assets'   # 질문창 보완 16종(카드·수첩 교체 포함)
FONT, ORIG, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
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


def src(name):
    """보완 납품(Q)에 있으면 그것을, 없으면 첫 납품(B)을 쓴다."""
    return Q / f'{name}.png' if (Q / f'{name}.png').exists() else B / f'{name}.png'


def part(base, name, box, ins):
    slice_into(base, visible(src(name)), box, ins)


def fit(base, name, box, tint=None, crop_frac=None):
    """보이는 그림을 box 안에 비율 유지로 맞춘다(가운데 정렬). tint 는 모양은 두고 색만 바꾼다."""
    im = visible(src(name))
    if crop_frac:
        im = im.crop((0, 0, im.width, round(im.height * crop_frac)))
    if tint:
        a = im.getchannel('A'); im = Image.new('RGBA', im.size, tint + (255,)); im.putalpha(a)
    x0, y0, x1, y1 = box
    k = min((x1 - x0) / im.width, (y1 - y0) / im.height)
    im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    base.alpha_composite(im, (int((x0 + x1 - im.width) / 2), int((y0 + y1 - im.height) / 2)))


def icon(base, name, cx, cy, h, folder=None, angle=0):
    im = visible(folder / f'{name}.png' if folder else src(name))
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
    part(b, 'b_panel_book', (485, 157, 1230, 655), (90, 84, 100, 30))
    fit(b, 'notebook_holes', (558, 206, 572, 240), crop_frac=0.64)        # 왼쪽 위 구멍 둘(종이 안쪽, 가장자리에 안 걸리게)
    fit(b, 'b_lineart_book_corner', (960, 186, 1118, 232))                # 오른쪽 위 마을 선화(빨간 테이프와 안 겹치게)
    fit(b, 'rule_dotted', (572, 236, 1180, 241))                          # 제목 아래 점선
    fit(b, 'rule_dotted', (572, 551, 1180, 556))                          # 버튼 위 점선(왼쪽 효과선과 안 겹치게)
    # 제목 탭(x562–922, y130–202), 도토리 아이콘 중심 (607,166), 글자 왼쪽 650
    part(b, 'b_tab_title', (562, 130, 922, 202), (30, 8, 30, 8))
    icon(b, 'b_icon_acorn', 607, 166, 36)
    fit(b, 'accent_rays_white', (622, 146, 640, 166))
    fit(b, 'accent_rays_white', (888, 162, 906, 182))
    d = ImageDraw.Draw(b)
    text_mid(d, 650, 166, '묻고 싶은 이야기', font('Bold', 31), WHITE)
    # 오른쪽 위 빨간 테이프는 보완 수첩 그림(b_panel_book)에 붙어 있다.
    # 질문 카드 세 장(x552–1185), 도토리 중심 x616, 글자 왼쪽 661
    cards = [('b_panel_card_hover', (249, 332), '마을에 관해서', False, 'b_lineart_village'),
             ('b_panel_card_done', (349, 432), '장터에 관해서', True, 'b_lineart_market'),
             ('b_panel_card', (450, 535), '이곳의 겨울에 관해서', False, 'b_lineart_winter')]
    for name, (y0, y1), q, done, art in cards:
        part(b, name, (552, y0, 1185, y1), (24, 20, 24, 20))
        fit(b, art, (930, y0 + 12, 1152, y1 - 12))   # 카드 접힌 귀와 안 겹치게
        cy = (y0 + y1) / 2
        icon(b, 'b_icon_acorn_done' if done else 'b_icon_acorn', 616, cy, 40)
        d = ImageDraw.Draw(b)
        text_mid(d, 661, cy, q, font('SemiBold', 27), INK_DONE if done else INK)
    fit(b, 'accent_rays_red', (628, 258, 646, 276))      # 고른 카드 도토리 옆
    fit(b, 'accent_rays_red', (549, 549, 563, 563))      # 자료 보여주기 왼쪽 위(종이 안쪽)
    # 아래 버튼 넷(y569–615)
    buttons = [((552, 724), '자료 보여주기', True, 'icon_document'), ((735, 870), '기록', False, 'icon_book_open'),
               ((881, 1029), '더보기', False, 'b_icon_more'), ((1040, 1195), '돌아가기', False, 'icon_arrow_left_bold')]
    for (x0, x1), t, primary, ic in buttons:
        part(b, 'b_button_primary' if primary else 'b_button', (x0, 569, x1, 615), (14, 10, 14, 10))
        d = ImageDraw.Draw(b)
        f = font('SemiBold', 19)
        tw = d.textlength(t, font=f)
        iw = 0
        if ic:
            v = visible(src(ic)); iw = round(v.width * 26 / v.height)
        group = tw + (iw + 9 if ic else 0)
        gx = (x0 + x1 - group) / 2
        if ic:
            fit(b, ic, (gx, 579, gx + iw, 605), tint=WHITE if primary else None)
        d = ImageDraw.Draw(b)
        text_mid(d, gx + (iw + 9 if ic else 0), 592, t, f, WHITE if primary else INK)
    # 오른쪽 책갈피(x1230–1270, y470–590)
    icon(b, 'sticker_bookmark', 1250, 530, 128, folder=S, angle=8)
    # 종이 이름표(x95–245, y605–665), 도토리 중심 (130,636), 이름 왼쪽 150
    fit(b, 'nameplate_paper', (95, 605, 245, 665))
    icon(b, 'b_icon_acorn', 130, 636, 30)
    d = ImageDraw.Draw(b)
    text_mid(d, 152, 636, '보리', font('Bold', 26), INK)
    return b


def sticker(base, name, box, angle=0):
    im = visible(S / f'sticker_{name}.png')
    if angle:
        im = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    x0, y0, x1, y1 = box
    k = min((x1 - x0) / im.width, (y1 - y0) / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    base.alpha_composite(im, (int((x0 + x1 - im.width) / 2), int((y0 + y1 - im.height) / 2)))


def vline_dotted(base, x, y0, y1):
    im = visible(src('rule_dotted')).rotate(90, expand=True)
    im = im.resize((max(2, im.width), y1 - y0), Image.LANCZOS)
    base.alpha_composite(im, (int(x - im.width / 2), y0))


def dialogue():
    """원본 01_대사창: 판 x30–1250·y568–702, 얼굴 스티커 x105–190, 이름 리본 x190–315·y548–585, 글자 x222·중심 y630."""
    b = cover(A / 'carriage.png')
    dar = visible(A / 'room13-carriage-daram-seat-bravado.webp')
    k = 520 / dar.height; dar = dar.resize((round(dar.width * k), 520), Image.LANCZOS)
    b.alpha_composite(dar, (int(760 - dar.width / 2), 600 - 520))
    part(b, 'b_panel_dialogue', (30, 568, 1250, 702), (40, 30, 60, 20))
    vline_dotted(b, 108, 600, 690)
    vline_dotted(b, 922, 580, 690)
    sticker(b, 'daram_stubborn', (100, 556, 196, 650), angle=-4)
    part(b, 'b_ribbon_name', (190, 548, 318, 586), (10, 6, 28, 6))
    fit(b, 'accent_rays_red', (322, 545, 342, 565))
    icon(b, 'b_tape_red', 86, 560, 12, angle=-12)    # 원본 테이프 너비 약 45
    d = ImageDraw.Draw(b)
    text_mid(d, 214, 567, '다람', font('Bold', 23), WHITE)
    text_mid(d, 222, 630, '예쁘다. 꼭 별 같아. 불이 하나도 안 떨려.', font('SemiBold', 27), INK)
    f = font('Medium', 16)
    text_mid(d, 952, 645, '기록   ·   자동   ·   더보기', f, INK)
    fit(b, 'b_icon_next', 1187, 636, 1203, 654, tint=INK) if False else fit(b, 'b_icon_next', (1187, 636, 1203, 654), tint=INK)
    return b


def choice():
    """원본 06_선택창: 제목 종이 x222–690·y215–310, 선택지 x212–728, 높이 약 80, 간격 16."""
    b = cover(A / 'room13-pixel-panorama-square-evening.webp')
    # 원본처럼 선택지 묶음 뒤를 어둡게 번지게 한다(그림자, 부품 아님).
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((190, 190, 760, 630), 40, fill=(12, 10, 24, 170))
    from PIL import ImageFilter
    b.alpha_composite(sh.filter(ImageFilter.GaussianBlur(28)))
    part(b, 'b_panel_card', (222, 215, 690, 310), (24, 20, 24, 20))
    fit(b, 'notebook_holes', (236, 236, 250, 290))
    icon(b, 'b_tape_red', 262, 216, 13, angle=-10)
    fit(b, 'accent_rays_red', (672, 232, 690, 250))   # 제목 글자와 안 겹치게 오른쪽 끝으로
    d = ImageDraw.Draw(b)
    t = '누군가 너울의 팔을 잡아당긴다.'
    f = font('Bold', 29)
    text_mid(d, (222 + 690 - d.textlength(t, font=f)) / 2 + 10, 262, t, f, INK)
    opts = [('1', '너울 앞을 막는다', 'b_panel_card_hover', 'b_tape_red'),
            ('2', '현장 감독자에게 보호를 맡긴다', 'b_panel_card', 'b_tape_teal'),
            ('3', '막지 않는다', 'b_panel_card', 'b_tape_yellow')]
    for i, (n, o, card, tape) in enumerate(opts):
        y0 = 335 + i * 97; y1 = y0 + 80
        part(b, card, (212, y0, 728, y1), (24, 20, 24, 20))
        fit(b, 'notebook_holes', (224, y0 + 12, 236, y1 - 12))
        icon(b, tape, 252, y0 + 2, 12, angle=-12)
        d = ImageDraw.Draw(b)
        cy = (y0 + y1) / 2
        text_mid(d, 284, cy, n, font('Bold', 29), (196, 64, 56) if i == 0 else INK)
        text_mid(d, 318, cy, '·', font('Bold', 27), INK)
        text_mid(d, 344, cy, o, font('SemiBold', 27), INK)
    fit(b, 'accent_rays_red', (730, 312, 752, 334))
    d = ImageDraw.Draw(b)
    text_mid(d, 1100, 690, '기록  ·  더보기', font('Medium', 16), (250, 244, 230))
    return b


def investigate():
    """원본 04_조사창: 장소 이름표 x28–245·y62–138, 지도·기록 x1068–1258·y57–120, 조사 판 x45–1250·y548–698."""
    b = cover(A / 'gate-wide/gate-wide-morning.webp')
    im = Image.open(A / 'gate-wide/gate-wide-morning.webp').convert('RGB')
    k = H / im.height; im = im.resize((round(im.width * k), H), Image.LANCZOS)
    b = im.crop((420, 0, 420 + W, H)).convert('RGBA')
    part(b, 'b_panel_small', (28, 62, 245, 138), (14, 12, 14, 12))
    icon(b, 'b_tape_red', 46, 66, 10, angle=-35)
    fit(b, 'b_icon_pin', (72, 86, 98, 114))
    d = ImageDraw.Draw(b)
    text_mid(d, 110, 100, '눈에 막힌 입구', font('SemiBold', 22), INK)
    for (x0, x1), t, ic in (((1068, 1157), '지도', 'b_icon_map'), ((1172, 1258), '기록', 'b_icon_book')):
        part(b, 'b_panel_small', (x0, 57, x1, 120), (14, 12, 14, 12))
        fit(b, ic, (x0 + 24, 64, x1 - 24, 94))
        d = ImageDraw.Draw(b)
        f = font('SemiBold', 14)
        text_mid(d, (x0 + x1) / 2 - d.textlength(t, font=f) / 2, 106, t, f, INK)
    fit(b, 'b_bubble_tag', (150, 386, 262, 428))
    d = ImageDraw.Draw(b)
    f = font('SemiBold', 17)
    text_mid(d, 206 - d.textlength('마차 바퀴', font=f) / 2, 404, '마차 바퀴', f, INK)
    part(b, 'b_panel_dialogue', (45, 548, 1250, 698), (40, 30, 60, 20))
    sticker(b, 'daram_stubborn', (118, 560, 248, 672), angle=-4)
    fit(b, 'accent_rays_red', (242, 578, 262, 598))
    fit(b, 'b_icon_acorn', (272, 584, 298, 612))
    d = ImageDraw.Draw(b)
    text_mid(d, 305, 598, '조사', font('Bold', 26), INK)
    fit(b, 'accent_rays_red', (366, 588, 382, 604))
    fit(b, 'rule_dotted', (275, 620, 1025, 625))
    d = ImageDraw.Draw(b)
    text_mid(d, 275, 643, '바퀴살 사이에 얼음이 끼어 있다. 굴러온 길은 눈에 덮였다.', font('Regular', 22), INK)
    part(b, 'b_button', (1050, 614, 1208, 652), (14, 10, 14, 10))
    fit(b, 'icon_arrow_left_bold', (1078, 624, 1102, 642))
    d = ImageDraw.Draw(b)
    text_mid(d, 1110, 633, '돌아가기', font('SemiBold', 18), INK)
    return b


def pair_image(mock_path, ours, title_l, title_r):
    mock = Image.open(mock_path).convert('RGB').resize((W, H), Image.LANCZOS)
    pair = Image.new('RGB', (W * 2 + 20, H + 50), (30, 26, 24))
    pair.paste(mock, (0, 50)); pair.paste(ours, (W + 20, 50))
    d = ImageDraw.Draw(pair)
    d.text((20, 12), title_l, font=font('SemiBold', 24), fill=(240, 232, 220))
    d.text((W + 40, 12), title_r, font=font('SemiBold', 24), fill=(240, 232, 220))
    return pair


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    right = '재현(실제 게임 배경·인물 + 납품 부품, 보이는 영역 기준)'
    for key, fn, orig in (('01_대사창', dialogue, '01_대사창'), ('02_선택창', choice, '06_선택창'),
                          ('03_질문창', question, '05_질문창'), ('04_조사창', investigate, '04_조사창')):
        ours = fn().convert('RGB')
        ours.save(OUT / f'{key}_재현.png')
        pair_image(ORIG / f'{orig}.png', ours, f'원본 시안 {orig}', right).save(OUT / f'{key}_비교.png')
        print(OUT / f'{key}_비교.png')


if __name__ == '__main__':
    main()
