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
S = ROOT.parents[1] / 'design/resource-intake-20261023/b-ui-stickers/assets'   # 소유자 납품 스티커 12종
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


def sticker(base, name, cx, cy, size, angle=0, alpha=1.0):
    """스티커처럼: 살짝 기울이고 얕은 그림자를 깔아 판 가장자리에 겹쳐 붙인다."""
    im = Image.open(S / f'sticker_{name}.png').convert('RGBA')
    im = im.crop(im.getchannel('A').getbbox())
    k = size / max(im.size)
    im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    if angle:
        im = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    if alpha < 1:
        im.putalpha(im.getchannel('A').point(lambda a: int(a * alpha)))
    sh = Image.new('RGBA', im.size, (20, 12, 6, 0))
    sh.putalpha(im.getchannel('A').point(lambda a: int(a * 0.35)))
    sh = sh.filter(ImageFilter.GaussianBlur(4))
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    base.alpha_composite(sh, (x + 3, y + 5))
    base.alpha_composite(im, (x, y))


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


def say_box(base, who, line, face=None, links=True):
    frame(base, 'b_panel_dialogue', (36, 532, 1244, 700))
    tx = 112
    if face:
        sticker(base, face, 138, 606, 132, angle=-4)
        tx = 222
    bribbon(base, tx - 14, 504, who)
    d = ImageDraw.Draw(base)
    d.text((tx, 588), line, font=font('Medium' if (FONT / 'Pretendard-Medium.otf').exists() else 'Regular', 29), fill=INK)
    if links:
        f = font('SemiBold', 16)
        d.text((1006, 640), '기록  ·  자동  ·  더보기', font=f, fill=INK_2)
        icon(base, 'b_icon_next', 1198, 650, 30)
    sticker(base, 'snow_star', 1196, 532, 76, angle=8)


def dialogue():
    b = cover(A / 'carriage.png')
    sprite(b, A / 'room13-carriage-daram-seat-bravado.webp', 560, 820, 600)
    say_box(b, '다람', '예쁘다. 꼭 별 같아. 불이 하나도 안 떨려.', face='daram_delighted')
    label_top(b, 'B안 · 대사창 · 부품+스티커 시안(미적용) · 고딕체')
    return b


def choice():
    b = cover(A / 'room13-pixel-panorama-square-evening.webp')
    b.alpha_composite(Image.new('RGBA', (W, H), (10, 8, 20, 90)))
    frame(b, 'b_panel_small', (300, 128, 980, 212))
    sticker(b, 'bookmark', 322, 150, 96, angle=-6)
    sticker(b, 'snow_star', 972, 132, 70, angle=10)
    d = ImageDraw.Draw(b)
    f = font('Bold', 29)
    t = '누군가 너울의 팔을 잡아당긴다.'
    d.text(((300 + 980 - d.textlength(t, font=f)) / 2, 150), t, font=f, fill=INK)
    opts = ['너울 앞을 막는다', '현장 감독자에게 보호를 맡긴다', '막지 않는다']
    for i, o in enumerate(opts):
        y = 240 + i * 104
        frame(b, 'b_panel_card_hover' if i == 1 else 'b_panel_card', (330, y, 950, y + 88))
        d = ImageDraw.Draw(b)
        d.text((400, y + 25), f'{i + 1}', font=font('Bold', 30), fill=RED)
        d.text((436, y + 27), '·', font=font('Bold', 28), fill=INK_2)
        d.text((462, y + 27), o, font=font('SemiBold', 27), fill=INK)
    sticker(b, 'daram_scared_brave', 1110, 560, 230, angle=4)
    sticker(b, 'warm_hanging_lantern', 170, 300, 120, angle=-3)
    d = ImageDraw.Draw(b)
    d.text((1086, 688), '기록  ·  더보기', font=font('SemiBold', 16), fill=(250, 244, 230))
    label_top(b, 'B안 · 선택창 · 부품+스티커 시안(미적용) · 빨간 테두리는 포커스, 정답 아님')
    return b


def question():
    b = cover(A / 'room13-pixel-panorama-square-afternoon.webp')
    sprite(b, A / 'room13-canonical-default-resident_bori.webp', 560, 250, 720)
    bribbon(b, 130, 630, '보리')
    frame(b, 'b_panel_book', (470, 96, 1240, 650))
    frame(b, 'b_tab_title', (560, 60, 930, 132))
    sticker(b, 'bookmark', 1150, 104, 110, angle=0)
    sticker(b, 'snow_star', 1214, 116, 66, angle=12)
    d = ImageDraw.Draw(b)
    icon(b, 'b_icon_acorn', 612, 96, 40)
    d.text((640, 80), '묻고 싶은 이야기', font=font('Bold', 26), fill=(255, 250, 240))
    qs = [('창고 문 앞 장작', False, 'covered_wooden_cart'), ('아이들이 자는 자리', True, 'snow_cottage'), ('수레에 덮은 담요', False, 'snowy_fir_tree')]
    for i, (q, done, deco) in enumerate(qs):
        y = 166 + i * 100
        frame(b, 'b_panel_card_done' if done else 'b_panel_card', (560, y, 1190, y + 88))
        sticker(b, deco, 1108, y + 44, 70, angle=-3 if i % 2 else 3, alpha=0.45 if done else 0.85)
        icon(b, 'b_icon_acorn_done' if done else 'b_icon_acorn', 620, y + 45, 46)
        d = ImageDraw.Draw(b)
        d.text((652, y + 29), q, font=font('SemiBold', 26), fill=INK if not done else INK_2)
    sticker(b, 'pencil', 1090, 500, 150, angle=-18)
    for i, (t, p, ic) in enumerate([('자료 보여주기', True, None), ('기록', False, 'b_icon_book'), ('더보기', False, 'b_icon_more'), ('돌아가기', False, 'b_icon_back')]):
        x = 560 + i * 158
        bbutton(b, (x, 556, x + 150, 608), t, primary=p, ic=ic, size=17)
    label_top(b, 'B안 · 질문창 · 부품+스티커 시안(미적용) · 질문 문구는 예시')
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
    frame(b, 'b_panel_dialogue', (36, 532, 1244, 700))
    sticker(b, 'daram_eureka', 138, 606, 132, angle=-4)
    icon(b, 'b_icon_magnifier', 236, 578, 40)
    d = ImageDraw.Draw(b)
    d.text((260, 563), '조사', font=font('Bold', 24), fill=INK)
    d.text((222, 612), '바퀴살 사이에 얼음이 끼어 있다. 굴러온 길은 눈에 덮였다.', font=font('Regular', 26), fill=INK)
    bbutton(b, (1050, 600, 1200, 650), '돌아가기', ic='b_icon_back', size=18)
    sticker(b, 'stamp', 1196, 540, 70, angle=9)
    label_top(b, 'B안 · 조사창 · 부품+스티커 시안(미적용) · 조사 대상·문장은 예시')
    return b


def main_menu():
    b = cover(A / 'room13-pixel-panorama-square-evening.webp')
    b.alpha_composite(Image.new('RGBA', (W, H), (10, 8, 30, 50)))
    sticker(b, 'snowy_fir_tree', 1180, 150, 170, angle=4)
    sticker(b, 'snow_cottage', 900, 520, 230, angle=-3)
    sticker(b, 'warm_hanging_lantern', 1210, 440, 130, angle=2)
    logo = asset('b_logo').resize((690, 230), Image.LANCZOS)
    b.alpha_composite(logo, (44, 34))
    sticker(b, 'snow_star', 760, 70, 90, angle=12)
    frame(b, 'b_main_panel', (40, 320, 700, 660))
    sticker(b, 'bookmark', 660, 330, 110, angle=4)
    for i, (t, p, ic) in enumerate([('이어하기', True, 'b_icon_next'), ('처음부터', False, 'b_icon_acorn'), ('불러오기', False, 'b_icon_book'), ('설정', False, 'b_icon_more')]):
        x = 132 + (i % 2) * 262
        y = 404 + (i // 2) * 100
        bbutton(b, (x, y, x + 240, y + 72), t, primary=p, ic=ic, size=24)
    sticker(b, 'daram_delighted', 1060, 590, 250, angle=-5)
    sticker(b, 'pencil', 600, 640, 140, angle=-14)
    label_top(b, 'B안 · 메인화면 · 부품+스티커 시안(미적용)')
    return b


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [('01_대사창', dialogue), ('02_선택창', choice), ('03_질문창', question), ('04_조사창', investigate), ('05_메인화면', main_menu)]:
        fn().convert('RGB').save(OUT / f'{name}.png')
        print(OUT / f'{name}.png')


if __name__ == '__main__':
    main()
