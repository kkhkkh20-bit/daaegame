"""웹 로딩창 그림을 메인화면과 같은 구성으로 합성한다.

소유자(2026-10-27): "로딩창 이미지 바꿔줘야지 예전 다람탐정 나오잖아."
로딩창은 Ren'Py 가 뜨기 전 HTML 이 그리므로 화면(screens.rpy main_menu)을 그대로
쓸 수 없다. 대신 main_menu 가 얹는 세 층(엽서 배경·로고·캐스트 포스터)을 같은
좌표·배율로 한 장(1280x720)에 합쳐 둔다. 좌표가 screens.rpy 와 어긋나면 로딩이
끝나는 순간 그림이 튀어 보이므로, 여기 값은 그 파일의 add Transform 줄과 맞춘다.

    python3 dev/make_loading_scene.py            # game/assets/room13-loading-scene.webp 갱신
    python3 dev/make_loading_scene.py 출력경로    # 다른 자리에 쓸 때
"""
from pathlib import Path
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
OUT = GAME / "assets/room13-loading-scene.webp"
CANVAS = (1280, 720)
# screens.rpy main_menu 의 세 add Transform 줄: (파일, zoom, xpos, ypos)
LAYERS = (
    ("assets/ui-b-main/b_main_background_postcard.png", 1280.0 / 1672, 0, 0),
    ("assets/ui-b-main/b_logo.png", .85, -18, 10),
    ("assets/ui-b-main/b_main_cast_poster_plain.png", 610.0 / 1402, 754, 80),
)


def compose(game=GAME):
    game = Path(game)
    scene = Image.new("RGBA", CANVAS, (0, 0, 0, 255))
    for rel, zoom, x, y in LAYERS:
        layer = Image.open(game / rel).convert("RGBA")
        w, h = layer.size
        layer = layer.resize((round(w * zoom), round(h * zoom)), Image.LANCZOS)
        scene.alpha_composite(layer, (x, y))
    return scene.convert("RGB")


def main(out=OUT):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    # 무손실은 수 MB 라 첫 화면이 늦어진다. 엽서 그림은 품질 88 이면 눈으로 구분되지 않는다.
    compose().save(out, "WEBP", quality=88, method=6)
    print(out, out.stat().st_size)


if __name__ == "__main__":
    main(*sys.argv[1:2])
