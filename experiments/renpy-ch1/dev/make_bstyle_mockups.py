"""B안(수첩 스타일) 화면 시안을 실제 게임 배경·인물로 만든다 (2026-10-23).

소유자 지시: "D 넣고 B안 시안 만들어줘. 폰트는 이제 고딕채로 하고".
참고 시안: 소유자가 보낸 B안 6장(생성 이미지). 그림(로고·스티커 지도·새 자세)은 쓰지 않고,
판·이름표·카드·버튼 같은 화면 부품만 코드로 그려 지금 게임 그림 위에 얹는다. 게임에는 아직 넣지 않는다.

  python3 dev/make_bstyle_mockups.py FONT_DIR OUT_DIR
FONT_DIR 에 Pretendard-Regular/SemiBold/Bold.otf (SIL OFL 1.1) 가 있어야 한다.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'game/assets'
B = ROOT.parents[1] / 'design/resource-intake-20261023/b-ui/assets'   # 소유자 납품 B안 부품 26종
INSETS = {'b_panel_dialogue': (64, 52, 80, 32), 'b_panel_card': (58, 32, 30, 26), 'b_panel_card_hover': (58, 32, 30, 26),
          'b_panel_card_done': (58, 32, 30, 26), 'b_panel_book': (104, 100, 116, 48), 'b_panel_small': (24, 20, 24, 20),
          'b_button': (24, 18, 24, 18), 'b_button_primary': (24, 18, 24, 18), 'b_ribbon_name': (20, 12, 40, 12),
          'b_tab_title': (40, 14, 40, 14), 'b_bubble_tag': (24, 14, 24, 22)}
FONT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
W, H = 1280, 720

PAPER = (247, 238, 218)
PAPER_EDGE = (205, 180, 140)
INK = (58, 42, 32)
INK_2 = (126, 104, 86)
RED = (196, 64, 56)
RED_DARK = (150, 44, 40)
TAPE = [(222, 120, 110, 170), (120, 170, 160, 170), (226, 196, 120, 170)]


def asset(name):
    return Image.open(B / f'{name}.png').convert('RGBA')


def frame(base, name, box):
    """Ren'Py Frame 처럼 네 모서리는 그대로, 가장자리와 가운데만 늘려 붙인다(납품 metadata 의 제안 경계)."""
    im = asset(name)
    l, t, r, b = INSETS.get(name, (16, 16, 16, 16))
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = x1 - x0, y1 - y0
    sw, sh = im.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    xs = [(0, l, 0, l), (l, sw - r, l, w - r), (sw - r, sw, w - r, w)]
    ys = [(0, t, 0, t), (t, sh - b, t, h - b), (sh - b, sh, h - b, h)]
    for sx0, sx1, dx0, dx1 in xs:
        for sy0, sy1, dy0, dy1 in ys:
            if dx1 <= dx0 or dy1 <= dy0 or sx1 <= sx0 or sy1 <= sy0:
                continue
            out.alpha_composite(im.crop((sx0, sy0, sx1, sy1)).resize((dx1 - dx0, dy1 - dy0), Image.LANCZOS), (dx0, dy0))
    base.alpha_composite(out, (x0, y0))


def bribbon(base, x, y, who, size=24):
    d = ImageDraw.Draw(base)
    tw = d.textlength(who, font=font('Bold', size))
    frame(base, 'b_ribbon_name', (x, y, x + tw + 84, y + 54))
    d = ImageDraw.Draw(base)
    d.text((x + 28, y + 11), who, font=font('Bold', size), fill=(255, 250, 240))


def icon(base, name, cx, cy, size):
    im = asset(name).resize((size, size), Image.LANCZOS)
    base.alpha_composite(im, (int(cx - size / 2), int(cy - size / 2)))


def bbutton(base, box, text, primary=False, ic=None, size=20):
    frame(base, 'b_button_primary' if primary else 'b_button', box)
    d = ImageDraw.Draw(base)
    f = font('SemiBold', size)
    tw = d.textlength(text, font=f)
    x0, y0, x1, y1 = box
    gap = 30 if ic else 0
    tx = (x0 + x1 - tw - gap) / 2 + gap
    if ic:
        icon(base, ic, tx - 20, (y0 + y1) / 2, 38)
    d.text((tx, (y0 + y1) / 2 - size * 0.62), text, font=f, fill=(255, 250, 240) if primary else INK)


def font(weight, size):
    return ImageFont.truetype(str(FONT / f'Pretendard-{weight}.otf'), size)


def cover(path, crop_x=None):
    im = Image.open(path).convert('RGB')
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2 if crop_x is None else crop_x
    return im.crop((x, (im.height - H) // 2, x + W, (im.height - H) // 2 + H)).convert('RGBA')


def shadow(base, box, radius, blur=10, alpha=90, off=(0, 6)):
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 + off[0], y0 + off[1], x1 + off[0], y1 + off[1]), radius, fill=(30, 20, 10, alpha))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))


def paper(base, box, radius=14, rings=True, tape=True):
    """크림색 수첩 판. 왼쪽에 스프링 고리, 모서리에 테이프."""
    shadow(base, box, radius)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius, fill=PAPER + (250,), outline=PAPER_EDGE, width=3)
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 + 8, y0 + 8, x1 - 8, y1 - 8), radius - 6, outline=(230, 214, 186), width=2)
    if rings:
        n = max(2, (y1 - y0) // 46)
        for i in range(n):
            cy = y0 + (y1 - y0) * (i + 0.5) / n
            d.ellipse((x0 - 14, cy - 10, x0 + 14, cy + 10), outline=(80, 66, 56), width=4)
            d.ellipse((x0 + 10, cy - 4, x0 + 18, cy + 4), fill=(120, 100, 84))
    if tape:
        tape_strip(base, (x1 - 60, y0 - 12), 84, 26, -14, TAPE[0])


def tape_strip(base, at, w, h, angle, color):
    t = Image.new('RGBA', (w, h), color)
    td = ImageDraw.Draw(t)
    for x in range(0, w, 7):
        td.line((x, 0, x, 2), fill=(255, 255, 255, 60))
    t = t.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(t, (int(at[0]), int(at[1])))


def ribbon(base, xy, text, size=24):
    """빨간 리본 이름표. 글자는 흰 고딕 굵게."""
    f = font('Bold', size)
    d = ImageDraw.Draw(base)
    tw = d.textlength(text, font=f)
    x, y = xy
    w, h = tw + 44, size + 20
    tag = Image.new('RGBA', (int(w) + 20, int(h) + 10), (0, 0, 0, 0))
    td = ImageDraw.Draw(tag)
    td.polygon([(0, 4), (w, 0), (w - 10, h / 2), (w, h), (4, h + 4)], fill=RED + (255,))
    td.text((20, 8), text, font=f, fill=(255, 250, 240))
    tag = tag.rotate(2, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(tag, (int(x), int(y)))


def acorn(d, cx, cy, r=10, col=(140, 92, 50)):
    d.ellipse((cx - r * 0.8, cy - r * 0.3, cx + r * 0.8, cy + r * 1.1), fill=col)
    d.pieslice((cx - r, cy - r * 0.9, cx + r, cy + r * 0.5), 180, 360, fill=(96, 64, 40))
    d.line((cx, cy - r * 0.9, cx + 2, cy - r * 1.3), fill=(96, 64, 40), width=2)


def button(base, box, text, primary=False, icon=None, size=20):
    d = ImageDraw.Draw(base)
    fill = RED if primary else (250, 244, 230)
    out = RED_DARK if primary else PAPER_EDGE
    d.rounded_rectangle(box, 12, fill=fill, outline=out, width=2)
    f = font('SemiBold', size)
    tw = d.textlength(text, font=f)
    x0, y0, x1, y1 = box
    off = 14 if icon else 0
    tx = (x0 + x1 - tw) / 2 + off
    d.text((tx, (y0 + y1) / 2 - size * 0.62), text, font=f, fill=(255, 250, 240) if primary else INK)
    if icon == 'acorn':
        acorn(d, tx - 20, (y0 + y1) / 2 - 2, 8, (255, 240, 225) if primary else (140, 92, 50))


def label_top(base, text):
    d = ImageDraw.Draw(base)
    f = font('SemiBold', 15)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((W / 2 - tw / 2 - 12, 8, W / 2 + tw / 2 + 12, 34), 8, fill=(20, 16, 12, 150))
    d.text((W / 2 - tw / 2, 12), text, font=f, fill=(250, 244, 230))


def sprite(base, path, height, x, y_bottom):
    im = Image.open(path).convert('RGBA')
    bb = im.getbbox()
    im = im.crop(bb)
    s = height / im.height
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    base.alpha_composite(im, (int(x - im.width / 2), int(y_bottom - im.height)))


def say_box(base, who, line, links=True):
    frame(base, 'b_panel_dialogue', (40, 536, 1240, 696))
    bribbon(base, 92, 506, who)
    d = ImageDraw.Draw(base)
    d.text((112, 592), line, font=font('Regular', 30), fill=INK)
    if links:
        f = font('Regular', 17)
        d.text((1010, 606), '기록 · 자동 · 더보기', font=f, fill=INK_2)
        icon(base, 'b_icon_next', 1190, 616, 30)


def dialogue():
    b = cover(A / 'carriage.png')
    sprite(b, A / 'room13-carriage-daram-seat-bravado.webp', 560, 820, 600)
    say_box(b, '다람', '예쁘다. 꼭 별 같아. 불이 하나도 안 떨려.')
    label_top(b, 'B안 · 대사창 · 납품 부품 적용 시안(미적용) · 고딕체')
    return b


def choice():
    b = cover(A / 'room13-pixel-panorama-square-evening.webp')
    b.alpha_composite(Image.new('RGBA', (W, H), (10, 8, 20, 90)))
    frame(b, 'b_panel_small', (300, 140, 980, 222))
    d = ImageDraw.Draw(b)
    f = font('Bold', 30)
    t = '누군가 너울의 팔을 잡아당긴다.'
    d.text(((300 + 980 - d.textlength(t, font=f)) / 2, 160), t, font=f, fill=INK)
    tapes = ['b_tape_red', 'b_tape_teal', 'b_tape_yellow']
    opts = ['너울 앞을 막는다', '현장 감독자에게 보호를 맡긴다', '막지 않는다']
    for i, o in enumerate(opts):
        y = 246 + i * 100
        frame(b, 'b_panel_card_hover' if i == 1 else 'b_panel_card', (320, y, 960, y + 88))
        d = ImageDraw.Draw(b)
        d.text((392, y + 26), f'{i + 1}', font=font('Bold', 28), fill=RED)
        d.text((428, y + 28), '·  ' + o, font=font('Regular', 27), fill=INK)
    d.text((1120, 680), '기록 · 더보기', font=font('Regular', 17), fill=(250, 244, 230))
    label_top(b, 'B안 · 선택창 · 납품 부품 적용 시안(미적용) · 빨간 테두리는 포커스, 정답 아님')
    return b


def question():
    b = cover(A / 'room13-pixel-panorama-square-afternoon.webp')
    sprite(b, A / 'room13-canonical-default-resident_bori.webp', 560, 250, 720)
    bribbon(b, 130, 630, '보리')
    frame(b, 'b_panel_book', (470, 96, 1240, 650))
    frame(b, 'b_tab_title', (560, 60, 930, 132))
    d = ImageDraw.Draw(b)
    icon(b, 'b_icon_acorn', 612, 96, 40)
    d.text((640, 80), '묻고 싶은 이야기', font=font('Bold', 26), fill=(255, 250, 240))
    qs = [('창고 문 앞 장작', False), ('아이들이 자는 자리', True), ('수레에 덮은 담요', False)]
    for i, (q, done) in enumerate(qs):
        y = 168 + i * 96
        frame(b, 'b_panel_card_done' if done else 'b_panel_card', (560, y, 1190, y + 88))
        icon(b, 'b_icon_acorn_done' if done else 'b_icon_acorn', 620, y + 46, 48)
        d = ImageDraw.Draw(b)
        d.text((650, y + 28), q, font=font('SemiBold', 27), fill=INK if not done else INK_2)
    for i, (t, p, ic) in enumerate([('자료 보여주기', True, None), ('기록', False, 'b_icon_book'), ('더보기', False, 'b_icon_more'), ('돌아가기', False, 'b_icon_back')]):
        x = 560 + i * 160
        bbutton(b, (x, 556, x + 152, 608), t, primary=p, ic=ic, size=18)
    label_top(b, 'B안 · 질문창 · 납품 부품 적용 시안(미적용) · 질문 문구는 예시')
    return b


def investigate():
    b = cover(A / 'gate-wide/gate-wide-morning.webp', crop_x=420)
    frame(b, 'b_panel_small', (24, 20, 264, 80))
    icon(b, 'b_icon_pin', 56, 50, 44)
    d = ImageDraw.Draw(b)
    d.text((80, 36), '눈에 막힌 입구', font=font('SemiBold', 22), fill=INK)
    for i, (t, ic) in enumerate([('지도', 'b_icon_map'), ('기록', 'b_icon_book')]):
        x = 1060 + i * 106
        frame(b, 'b_panel_small', (x, 18, x + 98, 96))
        icon(b, ic, x + 49, 44, 46)
        d = ImageDraw.Draw(b)
        d.text((x + 49 - d.textlength(t, font=font('SemiBold', 16)) / 2, 68), t, font=font('SemiBold', 16), fill=INK)
    frame(b, 'b_bubble_tag', (140, 386, 290, 442))
    d = ImageDraw.Draw(b)
    d.text((168, 396), '마차 바퀴', font=font('SemiBold', 20), fill=INK)
    frame(b, 'b_panel_dialogue', (40, 536, 1240, 696))
    icon(b, 'b_icon_magnifier', 118, 590, 44)
    d = ImageDraw.Draw(b)
    d.text((142, 576), '조사', font=font('Bold', 24), fill=INK)
    d.text((112, 624), '바퀴살 사이에 얼음이 끼어 있다. 굴러온 길은 눈에 덮였다.', font=font('Regular', 27), fill=INK)
    bbutton(b, (1040, 596, 1196, 648), '돌아가기', ic='b_icon_back', size=19)
    label_top(b, 'B안 · 조사창 · 납품 부품 적용 시안(미적용) · 조사 대상·문장은 예시')
    return b


def main_menu():
    b = cover(A / 'room13-pixel-panorama-square-evening.webp')
    logo = asset('b_logo').resize((720, 240), Image.LANCZOS)
    b.alpha_composite(logo, (40, 30))
    frame(b, 'b_main_panel', (40, 330, 700, 650))
    for i, (t, p, ic) in enumerate([('이어하기', True, 'b_icon_next'), ('처음부터', False, 'b_icon_acorn'), ('불러오기', False, 'b_icon_book'), ('설정', False, 'b_icon_more')]):
        x = 130 + (i % 2) * 270
        y = 410 + (i // 2) * 96
        bbutton(b, (x, y, x + 250, y + 70), t, primary=p, ic=ic, size=24)
    label_top(b, 'B안 · 메인화면 · 납품 로고·판 적용 시안(미적용) · 배경은 현행 광장 저녁')
    return b


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [('01_대사창', dialogue), ('02_선택창', choice), ('03_질문창', question), ('04_조사창', investigate), ('05_메인화면', main_menu)]:
        fn().convert('RGB').save(OUT / f'{name}.png')
        print(OUT / f'{name}.png')


if __name__ == '__main__':
    main()
