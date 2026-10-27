"""2026-10-27: 새 이야기가 이동하는 장소는 모두 R13_PLACES 에 등록돼 있어야 한다.
옛 MS14 모드를 지우자 그 모드가 등록하던 솜이네 골목·솜이네 방·밝은 초소가 빠져 4일 아침에 KeyError 가 났다.
정적 검사: r13_v111_travel('장소') 의 장소마다 등록 문장이 어딘가에 있어야 한다."""
import re,glob,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sources():
    return {f:Path(f).read_text(encoding='utf-8') for f in glob.glob(str(ROOT/'game/*.rpy'))+glob.glob(str(ROOT/'game/systems/*.rpy'))}
class TravelPlaces(unittest.TestCase):
    def test_every_travel_destination_is_registered(self):
        src=sources();all_src=''.join(src.values())
        places={m.group(1) for s in src.values() for m in re.finditer(r"r13_v111_travel\(\s*['\"](\w+)['\"]",s)}
        self.assertIn('ms14_somi',places)
        rules=src[str(ROOT/'game/room13_rules.rpy')]
        table=re.search(r'R13_PLACES\s*=\s*\{(.*?)\n    \}',rules,re.S).group(1)
        registered=set(re.findall(r'^\s*"(\w+)"\s*:',table,re.M))
        registered|=set(re.findall(r'R13_PLACES(?:\.setdefault\(|\[)\s*["\'](\w+)["\']',all_src))
        # 2주차 장소(week2_rules)의 R13_PLACES.update({...}) 표
        for block in re.findall(r'R13_PLACES\.update\(\{(.*?)\}\)',all_src,re.S):
            registered|=set(re.findall(r'"(\w+)"\s*:\s*\(',block))
        registered|=set(re.findall(r'\(\s*"(v111_\w+)"\s*,\s*"[^"]+"\s*,\s*"[^"]+"\s*\)',all_src))
        missing=sorted(p for p in places if p not in registered)
        self.assertEqual(missing,[],'등록되지 않은 이동 장소: %s'%missing)
if __name__=='__main__':unittest.main()
