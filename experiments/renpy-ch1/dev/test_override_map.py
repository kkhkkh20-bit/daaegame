"""Function override chains stay explicit: no dead layers, no same-priority layers,
and docs/OVERRIDE_MAP.md matches the scripts (python dev/override_map.py --write)."""
import unittest
from pathlib import Path
import override_map

class OverrideMap(unittest.TestCase):
    def setUp(self):
        self.chains = override_map.chains(override_map.scan())

    def test_no_dead_layers(self):
        dead = ["%s %s:%d" % (n, l["file"], l["line"]) for n, ls in self.chains.items() for l in ls if l.get("dead")]
        self.assertEqual(dead, [], "a later def replaces these without calling them; delete or capture them")

    def test_layers_never_share_an_init_priority(self):
        clash = {n: [l["prio"] for l in ls] for n, ls in self.chains.items()
                 if len({l["prio"] for l in ls}) != len(ls)}
        self.assertEqual(clash, {}, "order would depend on file names; give each layer its own init priority")

    def test_document_is_current(self):
        doc = (override_map.ROOT / "docs/OVERRIDE_MAP.md").read_text()
        self.assertEqual(doc, override_map.render(self.chains), "run: python dev/override_map.py --write")

if __name__ == "__main__":
    unittest.main()
