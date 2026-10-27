"""증거 비교 창 (plan5 m2a/m2b): data hooks, fallbacks and comparison state, without Ren'Py.

Native screen QA (lint, screen tests) still decides the layout; these tests pin the rules."""
import io
import json
import re
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
VIEW = (ROOT / "game/systems/room13_evidence_view.rpy").read_text()
NOTE = (ROOT / "game/room13_notebook.rpy").read_text()
BOOK = (ROOT / "game/room13_screens.rpy").read_text()
COMPARE = (ROOT / "game/room13_record_compare.rpy").read_text()
FACTS = ROOT / "game/v111/evidence-facts.json"
RECORDS = json.loads((ROOT / "game/v111/records.json").read_text())
CODE = textwrap.dedent(VIEW.split("init 330 python:\n", 1)[1].split("\ninit 331:", 1)[0])


class Transform(SimpleNamespace):
    def __init__(self, child, **kw):
        super().__init__(child=child, **kw)


class EvidenceView(unittest.TestCase):
    def build(self, files=None, values=None, active=True, touch=False):
        files = dict(files or {})
        self.values = dict(values or {})
        self.selected = []
        evidence = {
            "V111:E01": dict(name="초대 편지", kind="기록", establishes="다람이를 데리고 와 줘. 여관 13호실에서 기다릴게."),
            "V111:E06": dict(name="방의 메모", kind="기록", establishes="광장 등의 초롱에게 물어봐. 물건은 책상 아래에 두었어. (끝의 작은 도토리)"),
            "V111:E09": dict(name="엄마의 초상", kind="물증", establishes="눈과 입이 그려져 있다."),
            "E10": dict(name="밤이의 목격", kind="증언", establishes="밤이가 본 것."),
        }
        renpy = SimpleNamespace(loadable=lambda p: p in files,
                                file=lambda p: io.BytesIO(files[p].encode("utf-8")))
        env = dict(
            renpy=renpy, store=SimpleNamespace(room13={"records": {"V111:E01": {"day": 1}, "V111:E06": {"day": 2}}}),
            persistent=SimpleNamespace(room13_large_text=False),
            R13_V111={"evidence": {"E01": {"variants": {"observed": "x"}}, "E09": {"variants": {"unfinished": "a", "complete": "b"}}}},
            ROOM13={"evidence": evidence, "evidence_sources": {"E10": "bami"}},
            R13_RECORD_SHORT={}, R13_CONTROL=dict(text=22, large_text=24, padding=16),
            r13_v111_active=lambda: active, r13_v111_value=lambda k: self.values.get(k),
            r13_catalog_record=lambda k: evidence.get(k),
            r13_catalog_title=lambda k: evidence[k]["name"],
            r13_material_body=lambda ev: ev["establishes"],
            r13_record_icon=lambda k: "icon:" + k,
            r13_record_category=lambda k: "testimony" if evidence[k]["kind"] == "증언" else "evidence",
            r13_record_page_size=lambda: 12,
            r13_touch_ui=lambda: touch, r13_read_size=lambda base, large=None: base,
            R13_TYPE_V2=False,  # 2026-10-27 타이포 시안 스위치. 꺼진 상태를 검사한다

            r13_material_filter_choices=lambda current, allow=True: [("all", "전체"), ("testimony", "증언")],
            r13_record_select=lambda *a: self.selected.append(a),
            Transform=Transform, Fixed=lambda *c, **k: ("fixed", c, k), R13ControlSurface=lambda **k: ("surface", k),
            Function=lambda *a, **k: ("fn",) + a, Show=lambda n: ("show", n), NullAction=lambda: ("null",),
        )
        exec(compile(CODE, "evidence-view", "exec"), env)
        return env

    # -- data hooks -------------------------------------------------------------
    def test_base_key_only_for_v111_records(self):
        env = self.build()
        self.assertEqual(env["r13_evidence_base_key"]("V111:E01"), "E01")
        self.assertEqual(env["r13_evidence_base_key"]("V111:NW_STONE"), "NW_STONE")
        self.assertIsNone(env["r13_evidence_base_key"]("E01"))
        self.assertIsNone(env["r13_evidence_base_key"]("bag:lantern"))

    def test_held_variant_wins_and_first_authored_variant_is_the_fallback(self):
        env = self.build(values={"E09.variant": "complete"})
        self.assertEqual(env["r13_evidence_variant"]("V111:E09"), "complete")
        env = self.build()
        self.assertEqual(env["r13_evidence_variant"]("V111:E09"), "unfinished")
        self.assertEqual(env["r13_evidence_variant"]("V111:E01"), "observed")

    def test_facts_file_lines_for_the_held_variant(self):
        facts = {"E09": {"complete": ["코까지 그려져 있다.", "피코가 건넸다.", "셋째 줄", "넷째 줄"], "unfinished": ["코 자리가 비어 있다."]}}
        env = self.build(files={"v111/evidence-facts.json": json.dumps(facts)}, values={"E09.variant": "complete"})
        self.assertEqual(env["r13_evidence_facts"]("V111:E09"), ["코까지 그려져 있다.", "피코가 건넸다.", "셋째 줄"])
        self.values["E09.variant"] = "unfinished"
        self.assertEqual(env["r13_evidence_facts"]("V111:E09"), ["코 자리가 비어 있다."])

    def test_missing_file_key_or_variant_falls_back_to_record_text(self):
        for files in ({}, {"v111/evidence-facts.json": "{}"}, {"v111/evidence-facts.json": "not json"},
                      {"v111/evidence-facts.json": json.dumps({"E01": {"other": ["x"]}})},
                      {"v111/evidence-facts.json": json.dumps({"E01": {"observed": []}})}):
            env = self.build(files=files)
            self.assertEqual(env["r13_evidence_facts"]("V111:E01"), ["다람이를 데리고 와 줘.", "여관 13호실에서 기다릴게."])

    def test_fallback_drops_bracket_asides_and_caps_at_three_lines(self):
        env = self.build()
        lines = env["r13_evidence_facts"]("V111:E06")
        self.assertFalse(any("도토리" in line for line in lines))
        split = env["r13_evidence_split"]
        self.assertEqual(split("가. 나. 다. 라."), ["가.", "나.", "다 …"])
        packed = split("초소 입장 명단: 같은 도착일\n다돌\n신청 2명\n신규 일꾼 본인 1명\n동행 아동 모집 제외\n내일부터 장작 운반\n처리 너울.")
        self.assertLessEqual(len(packed), 3)
        self.assertIn("초소 입장 명단: 같은 도착일 · 다돌", packed[0])
        self.assertTrue(packed[-1].endswith("…"))
        self.assertEqual(split(""), [])

    def test_picture_prefers_evidence_art_then_enlarged_icon_and_keeps_testimony_portrait(self):
        env = self.build(files={"assets/evidence/E01.webp": ""})
        art = env["r13_evidence_picture"]("V111:E01", 336)
        self.assertEqual(art.child, "assets/evidence/E01.webp")
        self.assertTrue(art.nearest)
        self.assertEqual(art.xysize, (336, 336))
        icon = env["r13_evidence_picture"]("V111:E06", 336)
        self.assertEqual(icon.child, "icon:V111:E06")
        self.assertTrue(icon.nearest)
        # Testimony keeps the speaker's portrait from r13_record_icon even if art exists.
        env = self.build(files={"assets/evidence/E10.webp": ""})
        self.assertEqual(env["r13_evidence_picture"]("E10", 336).child, "icon:E10")

    def test_day_span_header(self):
        env = self.build()
        self.assertEqual(env["r13_evidence_day_span"](["V111:E01", "V111:E06"]), "1-2일째")
        self.assertEqual(env["r13_evidence_day_span"](["V111:E01"]), "1일째")
        self.assertEqual(env["r13_evidence_day_span"](["bag:x"]), "")

    # -- comparison state ---------------------------------------------------------
    def test_compare_fill_swap_single_and_live(self):
        env = self.build()
        begin, fill, swap = env["r13_compare_begin"], env["r13_compare_fill"], env["r13_compare_swap"]
        pair = begin("A")
        self.assertEqual(pair, ("A", None))
        pair = fill(pair, 1, "B")
        self.assertEqual(pair, ("A", "B"))
        self.assertEqual(fill(pair, 1, "C"), ("A", "C"))          # the other slot is replaced
        self.assertEqual(fill(pair, 0, "C"), ("C", "B"))          # slot 1 when chosen
        self.assertEqual(fill(pair, 1, "A"), ("A", "B"))          # never the same record twice
        self.assertEqual(swap(pair), ("B", "A"))
        self.assertEqual(env["r13_compare_single"](("A", "B")), "A")
        self.assertEqual(env["r13_compare_single"]((None, "B")), "B")
        live = env["r13_compare_live"]
        self.assertIsNone(live(None))
        self.assertEqual(live(("A", "gone"), lambda k: k != "gone"), ("A", None))
        self.assertIsNone(live(("gone", None), lambda k: k != "gone"))
        self.assertEqual(env["r13_compare_page"](list("abcdefghijklmn"), "n"), 1)
        self.assertEqual(env["r13_compare_page"](["a"], None), 0)

    # -- touch sizes ----------------------------------------------------------------
    def test_touch_controls_and_small_text(self):
        env = self.build(touch=True)
        self.assertGreaterEqual(env["r13_ev_button_height"]()*390/720, 44)
        self.assertGreaterEqual(env["r13_ev_fact_size"]()*390/720, 16)
        self.assertGreaterEqual(env["r13_ev_small_size"](), 18)
        self.assertGreaterEqual(env["r13_ev_label_size"]("올빼미 할아버지에게 보여주기", 296), 18)
        env = self.build()
        self.assertEqual(env["r13_ev_label_size"]("다람이에게 보여주기", 296), 22)
        self.assertLess(env["r13_ev_label_size"]("아주 긴 이름의 주민 할아버지에게 보여주기", 296), 22)

    def test_chips_end_left_of_close_and_right_of_tabs(self):
        for touch in (False, True):
            env = self.build(touch=touch)
            chips = [("전체", True, None), ("증언", False, None), ("전달 가능", False, None), ("지난 사건", False, None), ("지난 플레이", False, None)]
            boxes = env["r13_ev_chip_boxes"](chips)
            self.assertGreaterEqual(boxes[0][0], env["R13_EV_TAB_X"] + 5 * env["R13_EV_TAB_PITCH"])    # five top tabs
            self.assertLessEqual(boxes[-1][0] + boxes[-1][1], 1168)
            for (x, w), (nx, nw) in zip(boxes, boxes[1:]):
                self.assertLessEqual(x + w, nx)

    def test_first_tab_starts_after_the_title(self):
        # 0.20.5 (UI review): "자료 기록" and "보여주기" no longer run under the first tab.
        env = self.build()
        for title in ("기록", "자료 기록", "보여주기"):
            self.assertGreaterEqual(env["r13_ev_tab_x"](title), 60 + env["r13_ev_title_width"](title) + 20)
            self.assertGreaterEqual(env["r13_ev_tab_x"](title), env["R13_EV_TAB_X"])
        self.assertEqual(env["r13_ev_tab_x"]("기록"), env["R13_EV_TAB_X"])

    def test_all_filters_with_large_text_leave_tabs_and_touch_targets_clear(self):
        for touch in (False, True):
            env = self.build(touch=touch)
            env["r13_read_size"] = lambda base, large: large
            chips = [(label, False, None) for label in ("전체", "증언", "전달 가능", "지난 사건", "지난 플레이")]
            boxes = env["r13_ev_chip_boxes"](chips)
            self.assertGreaterEqual(boxes[0][0], 158+4*90+86+12)
            self.assertLessEqual(boxes[-1][0]+boxes[-1][1], 1168)
            if touch:
                self.assertTrue(all(width*390/720 >= 44 for x, width in boxes))
    def test_grid_names_keep_two_lines(self):
        env = self.build()
        for name in ("● 학교 장작 인수 기록", "흰 그릇을 받은 아이들의 아주 긴 이름", "공백없는아주긴자료이름입니다정말로"):
            self.assertLessEqual(len(env["r13_ev_two_lines"](name, 120, 18).split("\n")), 2)
        self.assertEqual(env["r13_ev_two_lines"]("방의 메모", 120, 18), "방의 메모")
    def test_book_tabs_have_no_dead_categories(self):
        env = self.build()
        self.assertEqual([k for k, t, a in env["r13_ev_record_tabs"]("r13_book")], ["all", "notes", "fork"])
        self.assertEqual([k for k, t, a in env["r13_ev_record_tabs"]("r13_book", True)], ["all"])
        self.assertEqual([k for k, t, a in env["r13_ev_record_tabs"]({})], ["all", "relations", "dialogue", "notes", "fork"])
        env = self.build(active=False)
        self.assertNotIn("fork", [k for k, t, a in env["r13_ev_record_tabs"]({})])

    # -- facts file and screens -------------------------------------------------------
    def test_facts_file_loads_and_matches_known_records(self):
        data = json.loads(FACTS.read_text())
        self.assertIsInstance(data, dict)
        known = dict(RECORDS["evidence"])
        for part in sorted((ROOT / "game/v111/newworld").glob("d*.json")):
            known.update(json.loads(part.read_text()).get("new_evidence", {}))
        for key, variants in data.items():
            self.assertIn(key, known, key)
            self.assertIsInstance(variants, dict)
            for variant, lines in variants.items():
                self.assertIsInstance(lines, list)
                self.assertTrue(all(isinstance(line, str) and line.strip() for line in lines), (key, variant))

    def test_records_and_book_share_the_browser_and_present_stays(self):
        self.assertIn('use r13_evidence_browser(entries,selected_record,page,_scope,pair,pair_slot,archive,("records",),header)', NOTE)
        self.assertIn('use r13_evidence_browser(entries,selected_record,page,"r13_book"', BOOK)
        self.assertIn('present,present_label,present_ok,Return(selected_record)', BOOK)
        self.assertIn('purpose in ("proof","compare") and detail in chosen', BOOK)  # 0.20.7: 「근거에 추가」/「근거에서 빼기」
        self.assertIn('(Return(False) if present or called else Hide("r13_book"))', BOOK)  # 0.20.6: a called book always returns
        self.assertIn("$ live_pair=None if present else r13_compare_live(pair)", VIEW)
        for screen in ("default pair=None", "default pair_slot=1"):
            self.assertIn(screen, NOTE)
            self.assertIn(screen, BOOK)

    def test_comparison_has_no_verdict_or_highlight(self):
        pair = VIEW.split("screen r13_evidence_pair(", 1)[1].split("\nscreen ", 1)[0]
        self.assertNotIn("r13_compare_result", pair)
        self.assertIn("맞는지 아닌지는 표시하지 않습니다.", pair)
        for word in ("정답", "오답", "일치", "같은 부분"):
            self.assertNotIn(word, pair)

    def test_source_fold_is_one_way_and_scroll_is_retained(self):
        single = VIEW.split("screen r13_evidence_single(", 1)[1].split("\nscreen ", 1)[0]
        # 0.20.7 (owner "다 해줘", Codex design 08): the same button folds the source again.
        self.assertIn('("출처 접기" if origin_open else "출처 펼치기")', single)
        self.assertIn('SetLocalVariable("origin_open",not origin_open)', single)
        self.assertIn("yadjustment detail_scroll", single)
        self.assertIn("r13_record_scroll_adjustment(view_context,detail,archive)", single)
        self.assertIn("r13_material_body(ev)", single)   # the long original text lives in the fold

    def test_dead_compare_tab_removed_and_old_save_screen_kept(self):
        self.assertNotIn("screen r13_compare_content", COMPARE)
        self.assertNotIn('tab=="compare"', NOTE)
        self.assertIn("screen r13_record_compare(called=False):", COMPARE)
        self.assertIn("def r13_compare_result(selected):", COMPARE)
        self.assertNotIn("screen r13_material_detail", NOTE)
        self.assertNotIn("r13_material_detail(", BOOK)

    def test_grid_rows_end_above_the_pager(self):
        bottom = self.build()["R13_EV_BOTTOM"]
        self.assertLessEqual(140 + 5 * 88, bottom - 88)
        self.assertGreaterEqual(88 * 360 / 720, 44)

    def test_all_current_names_fit_whole_words_without_ellipsis(self):
        env = self.build()
        known = dict(RECORDS["evidence"])
        for part in sorted((ROOT / "game/v111/newworld").glob("d*.json")):
            known.update(json.loads(part.read_text()).get("new_evidence", {}))
        for key, spec in known.items():
            for size in (18, 22, 24):
                name = spec["name"]
                lines = env["r13_ev_two_lines"](name, 174, size, 3).split("\n")
                self.assertEqual("".join(lines).replace(" ",""), name.replace(" ",""), (key, size, lines))
                self.assertTrue(all(env["r13_ev_text_units"](line)*size <= 174 for line in lines))
                self.assertLessEqual(len(lines), 3)
        self.assertNotIn("\n장", env["r13_ev_two_lines"]("반쯤 탄 수첩 장", 174, 24, 3))


if __name__ == "__main__":
    unittest.main()
