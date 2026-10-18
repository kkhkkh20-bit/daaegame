"""Exact .65 native-detail scope: only the reviewed 36 additions to .64 registries."""
import copy, hashlib, json, unittest
from investigation_canonical_overlay import receipt, restored_registries
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APPROVED=[['assets/room13-pixel-acting.json', '/daram/neutral/native_detail', 'assets/room13-pixel-world-daram-gray-gutter.webp'], ['assets/room13-pixel-acting.json', '/daram/thinking/native_detail', 'assets/room13-pixel-world-family-extra-gray.webp'], ['assets/room13-pixel-acting.json', '/daram/distressed/native_detail', 'assets/room13-pixel-world-family-extra-gray.webp'], ['assets/room13-pixel-acting.json', '/daram/expressive/native_detail', 'assets/room13-pixel-world-daram-gray-gutter.webp'], ['assets/room13-pixel-acting.json', '/daram/action_1/native_detail', 'assets/room13-pixel-world-daram-gray-gutter.webp'], ['assets/room13-pixel-acting.json', '/daram/action_2/native_detail', 'assets/room13-pixel-world-daram-gray-gutter.webp'], ['assets/room13-pixel-acting.json', '/daram/inspect_floor/native_detail', 'assets/room13-pixel-world-daram-gray-gutter.webp'], ['assets/room13-pixel-acting.json', '/daram/panic/native_detail', 'assets/room13-pixel-world-daram-gray-gutter.webp'], ['assets/room13-pixel-acting.json', '/daram/joy/native_detail', 'assets/room13-pixel-world-family-extra-gray.webp'], ['assets/room13-pixel-acting.json', '/karo/neutral/native_detail', 'assets/room13-pixel-acting-karo.webp'], ['assets/room13-pixel-acting.json', '/karo/thinking/native_detail', 'assets/room13-pixel-acting-karo.webp'], ['assets/room13-pixel-acting.json', '/karo/distressed/native_detail', 'assets/room13-pixel-acting-karo.webp'], ['assets/room13-pixel-acting.json', '/karo/expressive/native_detail', 'assets/room13-pixel-acting-karo.webp'], ['assets/room13-pixel-acting.json', '/karo/action_1/native_detail', 'assets/room13-pixel-acting-karo.webp'], ['assets/room13-pixel-acting.json', '/karo/action_2/native_detail', 'assets/room13-pixel-acting-karo.webp'], ['assets/room13-pixel-acting.json', '/karo/living_axlewrap/native_detail', 'assets/room13-action-karo-living_axlewrap.webp'], ['assets/room13-pixel-acting.json', '/resident_kalbaram/neutral/native_detail', 'assets/room13-role-resident_kalbaram.webp'], ['assets/room13-pixel-acting.json', '/resident_kalbaram/thinking/native_detail', 'assets/room13-role-resident_kalbaram.webp'], ['assets/room13-pixel-acting.json', '/resident_kalbaram/distressed/native_detail', 'assets/room13-role-resident_kalbaram.webp'], ['assets/room13-pixel-acting.json', '/resident_kalbaram/expressive/native_detail', 'assets/room13-role-resident_kalbaram.webp'], ['assets/room13-map-action27.json', '/rows/32/spec/native_detail', 'assets/map-action27/FO-1--resident_kalbaram.webp'], ['assets/room13-pixel-acting.json', '/resident_piko/neutral/native_detail', 'assets/room13-role-resident_piko.webp'], ['assets/room13-pixel-acting.json', '/resident_piko/thinking/native_detail', 'assets/room13-role-resident_piko.webp'], ['assets/room13-pixel-acting.json', '/resident_piko/distressed/native_detail', 'assets/room13-role-resident_piko.webp'], ['assets/room13-pixel-acting.json', '/resident_piko/expressive/native_detail', 'assets/room13-role-resident_piko.webp'], ['assets/room13-pixel-acting.json', '/doto/neutral/native_detail', 'assets/room13-role-doto.webp'], ['assets/room13-pixel-acting.json', '/doto/thinking/native_detail', 'assets/room13-role-doto.webp'], ['assets/room13-pixel-acting.json', '/doto/distressed/native_detail', 'assets/room13-role-doto.webp'], ['assets/room13-pixel-acting.json', '/doto/expressive/native_detail', 'assets/room13-role-doto.webp'], ['assets/room13-pixel-acting.json', '/resident_jongjong/neutral/native_detail', 'assets/room13-role-resident_jongjong.webp'], ['assets/room13-pixel-acting.json', '/resident_jongjong/thinking/native_detail', 'assets/room13-role-resident_jongjong.webp'], ['assets/room13-pixel-acting.json', '/resident_jongjong/distressed/native_detail', 'assets/room13-role-resident_jongjong.webp'], ['assets/room13-pixel-acting.json', '/resident_jongjong/expressive/native_detail', 'assets/room13-role-resident_jongjong.webp'], ['assets/room13-map-action27.json', '/rows/19/spec/native_detail', 'assets/map-action27/SQ-2--resident_piko.webp'], ['assets/room13-map-action27.json', '/rows/23/spec/native_detail', 'assets/map-action27/PO-3--resident_jongjong.webp'], ['assets/room13-map-action27.json', '/rows/38/spec/native_detail', 'assets/map-action27/CL-1--resident_piko.webp']]
BASE_DIGESTS={'assets/room13-pixel-acting.json': 'fef53250b9d78c752277601f20ab7e5b98534b352f489e8dc06b361807099127', 'assets/room13-map-action27.json': 'f3f896dc254c1b510b61b1d77b3694259d252a04ab41c28adef493017550192b'}

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=True,separators=(",",":")).encode()).hexdigest()

def validate(registries):
    restored=restored_registries(registries, receipt(ROOT))
    assert len(APPROVED)==36
    for path,pointer,asset in APPROVED:
        row=restored[path]
        parts=pointer.strip("/").split("/")
        for part in parts[:-1]: row=row[int(part)] if isinstance(row,list) else row[part]
        assert row["file"]==asset and row.get("native_detail") is True
        del row["native_detail"]
    for path,expected in BASE_DIGESTS.items():
        assert digest(restored[path])==expected, path

class NativeDetailScope(unittest.TestCase):
    def setUp(self):
        self.reg={path:json.loads((ROOT/"game"/path).read_text()) for path in BASE_DIGESTS}
    def test_only_exact_36_flags_change_and_all_other_specs_stay_identical(self):
        validate(self.reg)
    def test_unapproved_flag_is_rejected(self):
        self.reg["assets/room13-map-action27.json"]["rows"][0]["spec"]["native_detail"]=not self.reg["assets/room13-map-action27.json"]["rows"][0]["spec"].get("native_detail",False)
        with self.assertRaises(AssertionError):validate(self.reg)
    def test_changed_request_id_is_rejected(self):
        self.reg["assets/room13-map-action27.json"]["rows"][19]["request_id"]="UNAPPROVED"
        with self.assertRaises(AssertionError):validate(self.reg)
    def test_approved_flag_removal_is_rejected(self):
        self.reg["assets/room13-pixel-acting.json"]["daram"]["neutral"]["native_detail"]=False
        with self.assertRaises(AssertionError):validate(self.reg)
