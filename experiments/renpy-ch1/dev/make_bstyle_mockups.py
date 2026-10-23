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
    box = (40, 540, 1240, 690)
    paper(base, box)
    ribbon(base, (88, 516), who)
    d = ImageDraw.Draw(base)
    d.text((96, 588), line, font=font('Regular', 30), fill=INK)
    if links:
        f = font('Regular', 17)
        d.line((1010, 572, 1010, 660), fill=(220, 202, 172), width=2)
        d.text((1030, 604), '기록 · 자동 · 더보기', font=f, fill=INK_2)
        d.polygon([(1206, 604), (1206, 624), (1220, 614)], fill=INK)


def dialogue():
    b = cover(A / 'carriage.png')
    sprite(b, A / 'room13-carriage-daram-seat-bravado.webp', 560, 820, 600)
    say_box(b, '다람', '예쁘다. 꼭 별 같아. 불이 하나도 안 떨려.')
    label_top(b, 'B안 · 대사창 · 시안(미적용) · 고딕체')
    return b


def choice():
    b = cover(A / 'room13-pixel-panorama-square-evening.webp')
    b.alpha_composite(Image.new('RGBA', (W, H), (10, 8, 20, 90)))
    title = (300, 150, 980, 222)
    paper(b, title, rings=False)
    d = ImageDraw.Draw(b)
    f = font('Bold', 30)
    t = '누군가 너울의 팔을 잡아당긴다.'
    d.text(((300 + 980 - d.textlength(t, font=f)) / 2, 168), t, font=f, fill=INK)
    opts = ['너울 앞을 막는다', '현장 감독자에게 보호를 맡긴다', '막지 않는다']
    for i, o in enumerate(opts):
        y = 262 + i * 92
        box = (330, y, 950, y + 72)
        paper(b, box, radius=12, rings=False, tape=False)
        d = ImageDraw.Draw(b)
        tape_strip(b, (322, y - 8), 46, 18, -10, TAPE[i % 3])
        d.text((372, y + 18), f'{i + 1}', font=font('Bold', 28), fill=RED)
        d.text((410, y + 20), '·  ' + o, font=font('Regular', 27), fill=INK)
    d.text((1120, 680), '▶ 기록 · 더보기', font=font('Regular', 17), fill=(250, 244, 230))
    label_top(b, 'B안 · 선택창 · 시안(미적용) · 강조는 선택 정답이 아님')
    return b


def question():
    b = cover(A / 'room13-pixel-panorama-square-afternoon.webp')
    sprite(b, A / 'room13-canonical-default-resident_bori.webp', 560, 250, 720)
    ribbon(b, (150, 640), '보리')
    box = (480, 110, 1230, 640)
    paper(b, box)
    d = ImageDraw.Draw(b)
    tab = (520, 84, 820, 140)
    d.rounded_rectangle(tab, 12, fill=RED, outline=RED_DARK, width=2)
    acorn(d, 550, 110, 10, (255, 236, 220))
    d.text((572, 94), '묻고 싶은 이야기', font=font('Bold', 26), fill=(255, 250, 240))
    qs = [('창고 문 앞 장작', False), ('아이들이 자는 자리', True), ('수레에 덮은 담요', False)]
    for i, (q, done) in enumerate(qs):
        y = 170 + i * 100
        r = (520, y, 1190, y + 80)
        d.rounded_rectangle(r, 12, fill=(252, 247, 236) if not done else (238, 230, 214), outline=PAPER_EDGE, width=2)
        acorn(d, 560, y + 38, 12, (140, 92, 50) if not done else (176, 156, 130))
        d.text((588, y + 22), q, font=font('SemiBold', 27), fill=INK if not done else INK_2)
        if done:
            d.ellipse((1140, y + 26, 1166, y + 52), outline=INK_2, width=2)
            d.line((1146, y + 39, 1152, y + 46, 1161, y + 32), fill=INK_2, width=3)
    for i, (t, p) in enumerate([('자료 보여주기', True), ('기록', False), ('더보기', False), ('돌아가기', False)]):
        x = 520 + i * 172
        button(b, (x, 560, x + 160, 612), t, primary=p, size=19)
    label_top(b, 'B안 · 질문창 · 시안(미적용) · 질문 문구는 예시, 완료 표시는 상태 예시')
    return b


def investigate():
    b = cover(A / 'gate-wide/gate-wide-morning.webp', crop_x=420)
    d = ImageDraw.Draw(b)
    # 장소 이름표(왼쪽 위)와 지도·기록(오른쪽 위)
    paper(b, (28, 24, 250, 76), radius=12, rings=False, tape=False)
    d = ImageDraw.Draw(b)
    d.ellipse((46, 40, 62, 56), outline=RED, width=3)
    d.text((72, 36), '눈에 막힌 입구', font=font('SemiBold', 22), fill=INK)
    for i, t in enumerate(['지도', '기록']):
        x = 1076 + i * 96
        paper(b, (x, 24, x + 84, 84), radius=12, rings=False, tape=False)
        d = ImageDraw.Draw(b)
        d.text((x + 42 - d.textlength(t, font=font('SemiBold', 19)) / 2, 44), t, font=font('SemiBold', 19), fill=INK)
    # 물건 이름표(말풍선)
    tag = (150, 390, 280, 430)
    paper(b, tag, radius=10, rings=False, tape=False)
    d = ImageDraw.Draw(b)
    d.polygon([(170, 430), (186, 430), (172, 448)], fill=PAPER)
    d.text((170, 398), '마차 바퀴', font=font('SemiBold', 20), fill=INK)
    box = (40, 560, 1240, 690)
    paper(b, box)
    d = ImageDraw.Draw(b)
    acorn(d, 112, 600, 12)
    d.text((134, 584), '조사', font=font('Bold', 24), fill=INK)
    d.text((112, 626), '바퀴살 사이에 얼음이 끼어 있다. 굴러온 길은 눈에 덮였다.', font=font('Regular', 27), fill=INK)
    button(b, (1060, 596, 1210, 644), '돌아가기', size=19)
    label_top(b, 'B안 · 조사창 · 시안(미적용) · 조사 대상·문장은 예시')
    return b


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [('01_대사창', dialogue), ('02_선택창', choice), ('03_질문창', question), ('04_조사창', investigate)]:
        fn().convert('RGB').save(OUT / f'{name}.png')
        print(OUT / f'{name}.png')


if __name__ == '__main__':
    main()
