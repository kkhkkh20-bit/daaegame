"""Face selection must not invent an emotion or show the first-person father."""
import ast, hashlib, json, textwrap, unittest
from pathlib import Path
from types import SimpleNamespace
ROOT = Path(__file__).resolve().parents[1]

class BDialogueFaces(unittest.TestCase):
    def setUp(self):
        self.faces = json.loads((ROOT/'game/assets/room13-dialogue-b-faces.json').read_text())
        source = (ROOT/'game/room13_bdialogue_faces.rpy').read_text().split('init 171 python:\n', 1)[1]
        tree = ast.parse(textwrap.dedent(source))
        tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        self.env = dict(R13_BDIALOGUE_FACES=self.faces, renpy=SimpleNamespace(loadable=lambda path:(ROOT/'game'/path).is_file()))
        exec(compile(tree, 'faces', 'exec'), self.env)

    def test_only_matching_delivered_faces_are_used(self):
        pick=self.env['r13_bdialogue_face']
        for person, expressions in self.faces.items():
            for expression,path in expressions.items():self.assertEqual(pick(person,expression),path)
            self.assertIsNone(pick(person,'neutral'))
            self.assertIsNone(pick(person,'unapproved_emotion'))
        self.assertIsNone(pick('dad','joy'))
        self.assertIsNone(pick('daram','joy'))
        self.assertIsNone(pick(None,'joy'))
        self.assertEqual(pick('granny','surprise'),pick('granny','surprise_talk'))
        self.assertEqual(pick('granny','flustered'),pick('granny','anxious'))
        self.env['renpy'].loadable=lambda path:False
        self.assertIsNone(pick('granny','joy'))

    def test_delivery_bytes_are_preserved(self):
        source=ROOT.parents[1]/'design/resource-intake-20261024/b-char-primary50'
        rows=json.loads((source/'B_추가표정180_파일연결표.json').read_text())['rows']
        count=0
        for row in rows:
            path=self.faces.get(row['character_id'],{}).get(row['expression'])
            if path:
                self.assertEqual(hashlib.sha256((ROOT/'game'/path).read_bytes()).hexdigest(),row['face_sha256'])
                count+=1
        self.assertEqual(count,50)
