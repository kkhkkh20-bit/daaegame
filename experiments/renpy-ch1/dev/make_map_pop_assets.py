"""0.20.11 지도 떠오르기 효과용 그림을 만든다.

장소 영역 그림(room13-map-village-<키>.webp)은 다각형 경계가 딱 잘려 있어, 그대로 키워 띄우면
오려 붙인 스티커처럼 보인다. 경계를 안쪽으로 조금 줄인 뒤 흐리게 풀어(부드러운 가장자리)
-pop.webp로 저장하고, 원래 자리를 흐리게 덮을 -base.webp도 만든다. 큰 강·깊은 숲은 떠오르지 않으므로 만들지 않는다.
    python3 dev/make_map_pop_assets.py
"""
import json
from pathlib import Path
from PIL import Image, ImageFilter

GAME = Path(__file__).resolve().parents[1] / "game"
cart = json.loads((GAME / "room13-cartography.json").read_text(encoding="utf-8"))
nodes = cart["regions"]["village"]["nodes"]
done = []
for key, node in nodes.items():
    art_key = node.get("art_key", key)
    if art_key in ("river", "forest") or art_key in done:
        continue
    src = Image.open(GAME / f"assets/room13-map-village-{art_key}.webp").convert("RGBA")
    alpha = src.getchannel("A").filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(5))
    out = src.copy()
    out.putalpha(alpha)
    out.save(GAME / f"assets/room13-map-village-{art_key}-pop.webp", lossless=True, method=6)
    # 떠오른 그림 아래에 깔 흐린 바탕: 원래 자리의 선을 흐려, 떠오른 그림과 겹쳐 두 줄로 보이지 않게 한다.
    base = src.filter(ImageFilter.GaussianBlur(5))
    base.putalpha(src.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(4)))
    base.save(GAME / f"assets/room13-map-village-{art_key}-base.webp", lossless=True, method=6)
    done.append(art_key)
print("만듦:", ", ".join(done))
