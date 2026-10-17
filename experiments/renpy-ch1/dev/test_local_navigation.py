"""Local navigation access rules, independent of rendering and game time."""
import copy
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest


class LocalNavigation(unittest.TestCase):
    def setUp(self):
        source = (Path(__file__).resolve().parents[1] / "game/room13_navigation.rpy").read_text()
        code = source.split("init 60 python:\n", 1)[1].split("\nscreen r13_map", 1)[0]
        self.store = SimpleNamespace(room13={"location": "inn", "day": 1, "period": 0})
        self.allowed = ["inn", "square", "gate", "post", "workshop"]
        self.ns = {"store": self.store, "renpy": SimpleNamespace(Displayable=object),
                   "r13_places": lambda: self.allowed}
        exec(textwrap.dedent(code), self.ns)

    def test_all_inn_rooms_default_to_interior_map(self):
        for location in self.ns["R13_INN_LOCATIONS"]:
            self.assertEqual(self.ns["r13_map_region"](location), "inn")
        self.assertEqual(self.ns["r13_map_region"]("square"), "village")

    def test_underground_map_requires_actual_discovery_even_in_stale_save(self):
        self.ns['r13_ancient_open']=lambda:False
        self.store.room13['location']='ancient'
        self.assertEqual(self.ns['r13_map_region']('ancient'),'inn')
        self.assertNotIn('ancient',dict(self.ns['r13_map_nodes']('inn')))
        self.ns['r13_ancient_open']=lambda:True
        self.assertIn('ancient',dict(self.ns['r13_map_nodes']('inn')))

    def test_before_checkin_only_exit_is_available(self):
        self.assertEqual(self.ns["r13_local_connections"](), [("outside", "여관 밖으로")])
        self.assertIsNone(self.ns["r13_local_destination"]("hall"))

    def test_checked_in_adjacency_and_stale_selection(self):
        self.allowed += ["dining", "kitchen", "hall", "room13"]
        self.assertEqual([key for key, _ in self.ns["r13_local_connections"]()],
                         ["dining", "kitchen", "hall", "outside"])
        self.allowed.remove("hall")
        self.assertIsNone(self.ns["r13_local_destination"]("hall"))

    def test_hidden_passage_and_borrowed_room_remain_locked(self):
        self.allowed += ["hall", "room13"]
        self.store.room13["location"] = "room13"
        self.assertEqual(dict(self.ns["r13_local_connections"]()), {"hall": "복도로"})
        self.allowed.append("passage")
        self.assertEqual(self.ns["r13_local_destination"]("passage"), "passage")
        self.store.room13["location"] = "hall"
        self.assertNotIn("guestroom", dict(self.ns["r13_local_connections"]()))
        self.allowed.append("guestroom")
        self.assertIn("guestroom", dict(self.ns["r13_local_connections"]()))

    def test_map_preview_and_connections_do_not_change_state(self):
        before = copy.deepcopy(self.store.room13)
        self.ns["r13_local_connections"]()
        self.ns["r13_map_selection"]("village", "room13")
        self.assertEqual(self.store.room13, before)


if __name__ == "__main__":
    unittest.main()
