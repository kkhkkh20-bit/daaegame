"""Village map v5 (from closed PR #8, ported to 0.18.5): source-level invariants.

Actual mouse/keyboard input and travel are checked in the browser by
dev/qa_worldmap.py and in Ren'Py by dev/run_renpy_tests.sh worldmap_travel.
"""
import r13_timeline_env  # noqa: F401  날짜표 상수 (game/systems/room13_timeline.rpy)
import ast, copy, hashlib, json, textwrap, types, unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
DESIGN = ROOT.parents[1] / "design/maps/20261014"
DATA = json.loads((GAME / "room13-cartography.json").read_text(encoding="utf-8"))
SCALE = 860 / 1672


def extract(ns, file, names):
    text = (GAME / file).read_text(encoding="utf-8")
    start = text.index(" python:\n") + len(" python:\n")
    lines = []
    for line in text[start:].splitlines():
        if line and not line.startswith((" ", "#")):
            break
        lines.append(line)
    tree = ast.parse(textwrap.dedent("\n".join(lines)))
    chosen = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names
              or isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets)]
    exec(compile(ast.Module(body=chosen, type_ignores=[]), file, "exec"), ns)


def namespace():
    ns = {"store": types.SimpleNamespace(room13={})}
    extract(ns, "room13_rules.rpy", {"r13_places"})
    ns["r13_has"] = lambda f: f in ns["store"].room13["flags"] or f in ns["store"].room13["evidence"]
    ns["_r13_route_places"] = ns["r13_places"]
    extract(ns, "room13_route_knowledge.rpy", {"r13_places", "r13_secret_route_available"})
    extract(ns, "room13_navigation.rpy", {"R13_MAP_NODES", "R13_LOCAL_CONNECTIONS", "r13_map_nodes",
        "r13_map_discovered", "r13_map_selection", "r13_local_connections", "r13_local_destination"})
    return ns


class WorldmapV5(unittest.TestCase):
    def test_existing_destinations_only(self):
        ns=namespace()
        self.assertEqual(set(DATA['regions']['village']['nodes']),set(ns['R13_MAP_NODES']['village']))
        self.assertEqual(set(DATA['regions']['mountain']['nodes']),{'forest','facility','greenhouse','altar'})

    def test_assets_and_mask_targets(self):
        from PIL import ImageDraw,ImageChops
        for region,spec in DATA['regions'].items():
            art=GAME/spec['art']
            self.assertEqual(hashlib.sha256(art.read_bytes()).hexdigest(),spec['sha256'])
            with Image.open(art) as im:self.assertEqual(im.size,tuple(DATA['size']))
            masks={}
            for key,node in spec['nodes'].items():
                x,y,w,h=node['bounds']
                mask=Image.new('L',tuple(DATA['size']))
                ImageDraw.Draw(mask).polygon([tuple(p) for p in node['polygon']],fill=255)
                masks[key]=mask
                for suffix in ('','-outline'):
                    with Image.open(GAME/('assets/room13-map-%s-%s%s.webp'%(region,key,suffix))) as im:
                        self.assertEqual(im.size,(w,h));self.assertIn('A',im.getbands())
                px,py=node['point']
                self.assertEqual(mask.getpixel((px,py)),255,key)
                # Both floating bars must leave the actual click point uncovered.
                ox,oy=spec.get('offset',(16,9))
                sx,sy=ox+px*1248/1672,oy+py*1248/1672
                self.assertTrue(9<sy<614,key)
                self.assertFalse(24<=sx<=274 and 20<=sy<=96,key)
            for i,(key,mask) in enumerate(masks.items()):
                for other,other_mask in list(masks.items())[i+1:]:
                    self.assertIsNone(ImageChops.multiply(mask,other_mask).getbbox(),(region,key,other))
            for key,node in spec['nodes'].items():
                for other,mask in masks.items():
                    if key!=other:self.assertEqual(mask.getpixel(tuple(node['point'])),0,(key,other))

    def test_secrets_have_separate_discovery_layers(self):
        self.assertEqual(set(DATA['reveals']),{'greenhouse','altar'})
        for key,spec in DATA['reveals'].items():
            with Image.open(GAME/spec['art']) as im:
                self.assertEqual(im.size,tuple(spec['bounds'][2:]))
                # Opaque ink patches prevent hidden tree lines bleeding through.
                self.assertIn(im.mode,('RGB','RGBA'))
        source=(GAME/'room13_worldmap_v5.rpy').read_text()
        self.assertIn('if r13_cart_cover_visible(secret):',source)
        self.assertNotIn('v5_label_',source)
        self.assertIn('action SetScreenVariable("selected",key)',source)

    def test_village_name_targets_fit_without_overlap(self):
        # Hand-lettered names retain invisible, separated UI targets above the
        # navigation footer. Geometry is measured on the approved illustration.
        boxes=[]
        spec=DATA['regions']['village'];ox,oy=spec.get('offset',(16,9))
        for key,node in spec['nodes'].items():
            x,y=node['label_point'];x=ox+round(x*1248/1672);y=oy+round(y*1248/1672)
            bx,by,bw,bh=node['label_bounds']
            self.assertTrue(bx<=node['label_point'][0]<=bx+bw,key)
            self.assertTrue(by<=node['label_point'][1]<=by+bh,key)
            width=max(90,round(bw*1248/1672)+16);height=max(42,round(bh*1248/1672)+8)
            box=(x-width//2,y-height//2,x+width//2,y+height//2)
            self.assertTrue(24<=box[0]<box[2]<=1256,key)
            self.assertTrue(9<box[1]<box[3]<614,key)
            self.assertFalse(box[0]<274 and box[1]<96,key)
            for other,b in boxes:
                self.assertFalse(box[0]<b[2] and b[0]<box[2] and box[1]<b[3] and b[1]<box[3],(key,other))
            boxes.append((key,box))

    def test_eligibility_and_hidden_places(self):
        ns = namespace()
        count = 0
        for day in (1, 4, 8, 14):
            for lodging in (False, True):
                for discovered in (False, True):
                    for opened in (False, True):
                        for case in ("pending", "occurred"):
                            for current in ("gate", "passage", "greenhouse", "altar"):
                                state = dict(day=day, location=current, flags=["lodging"] if lodging else [],
                                             evidence=[], case_state=case, passage_open=opened,
                                             secret_route_unlocked=discovered)
                                ns["store"].room13 = state
                                before = copy.deepcopy(state)
                                allowed = set(ns["r13_places"]())
                                self.assertEqual("guestroom" in allowed, lodging and case == "occurred")
                                for region in ns["R13_MAP_NODES"]:
                                    visible = {k for k, p in ns["r13_map_nodes"](region)}
                                    self.assertEqual("passage" in visible, region == "inn" and discovered and opened)
                                    self.assertNotIn("greenhouse", visible)
                                    self.assertNotIn("altar", visible)
                                    for stale in ("passage", "greenhouse", "altar", "invalid", None):
                                        selected = ns["r13_map_selection"](region, stale)
                                        self.assertTrue(selected in visible or selected is None)
                                self.assertEqual(before, state)
                                count += 1
        self.assertEqual(count, 256)


if __name__ == "__main__":
    unittest.main()
