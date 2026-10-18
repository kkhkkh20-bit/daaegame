import hashlib, importlib.util, json, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('resource_build',Path(__file__).with_name('build.py'))
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
class Extractor(unittest.TestCase):
    def test_deployed_renderer_url_matches_current_content(self):
        web=Path(__file__).parent/'web'
        deployed=b.REPO/'preview/resource-dashboard'
        self.assertEqual((web/'app.js').read_bytes(),(deployed/'app.js').read_bytes())
        digest=hashlib.sha256((web/'app.js').read_bytes()).hexdigest()[:16]
        self.assertIn(f'src="app.js?v={digest}"',(deployed/'index.html').read_text())
        self.assertNotIn('src="app.js"',(deployed/'index.html').read_text())

    def test_gallery_upgrade_preserves_evidence_and_is_idempotent(self):
        spec=importlib.util.spec_from_file_location('gallery',Path(__file__).with_name('gallery.py'))
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)/'reports/place-balance-01936';folder.mkdir(parents=True)
            evidence='<figure><a href="capture.png"><img src="capture.png"></a><figcaption>추가 검토 필요 · 전체 분기 검수 아님</figcaption></figure>'
            page=folder/'index.html';page.write_text('<!doctype html><meta charset="utf-8"><style></style>'+evidence)
            module.install(td);first=page.read_bytes();module.install(td)
            self.assertEqual(first,page.read_bytes());self.assertIn(evidence,page.read_text());self.assertEqual(page.read_text().count('src="ui.js"'),1)
    def test_literal_only_no_execution(self):
        text='init 150 python:\n    A = {"night": ("one", None)}\n    B = dangerous_call()\n\nlabel start:\n    pass\n'
        self.assertEqual(b.literal_tables(text),{'A':{'night':('one',None)}})
    def test_negative_priority_and_line_evidence(self):
        blocks=list(b.python_blocks('# header\ninit -5 python:\n    def choice():\n        return 1\nlabel start:\n    pass'))
        self.assertEqual(blocks[0][1]+blocks[0][0].body[0].lineno,3)
    def test_nested_assignment_is_not_runtime_constant(self):
        self.assertEqual(b.literal_tables('init 1 python:\n    def f():\n        A = 2\n'),{})
    def test_sparse_day_allowlist_and_bounds(self):
        self.assertEqual(b.declared_days({'min_day':2,'days':[3,8,13]}),[3,8,13])
        self.assertEqual(b.declared_days({'min_day':4,'max_day':10,'days':[3,8,13]}),[8])
    def test_visible_actor_capture_links_and_approved_seori(self):
        folder=b.REPO/'preview/resource-dashboard/characters'
        seori=json.loads((folder/'resident_seori.json').read_text())
        self.assertTrue(any(p['pose']=='inspect_paper_threequarter_front' for p in seori['placements']))
        captures=[c for c in seori['captures'] if 'place-balance-01936' in c['evidence']]
        self.assertTrue(captures)
        for c in captures:
            self.assertEqual(c['actor']['person'],'resident_seori')
            self.assertEqual(c['pose'],c['actor']['pose'])
    def test_real_generated_contract(self):
        path=b.REPO/'preview/resource-dashboard/data.json'
        if not path.exists():self.skipTest('run build.py first')
        j=json.loads(path.read_text());self.assertEqual(len(j['game_commit']),40)
        self.assertGreater(len(j['characters']),50);self.assertGreater(len(j['audio']),30)
        self.assertEqual(len(j['characters']),len({c['id'] for c in j['characters']}))
        for summary in j['characters']:
            c=json.loads((path.parent/summary['detail_url']).read_text())
            for a in c['assets']:
                self.assertFalse(a['runtime_observed'])
                self.assertFalse(a['media']['path'].startswith('/'))
                if a['status']=='missing':self.assertFalse(a['media']['exists'])
                if a['active_call']:self.assertTrue(a['conditions'])
            for s in c['schedule']:self.assertIn(s['day'],range(1,15))
            for p in c['placements']:
                self.assertTrue(p['guards']);self.assertTrue('캡처' in p['capture_status'])
        for a in j['audio']:
            self.assertTrue(a['media']['path'].startswith(str(b.GAME_REL)))
        self.assertNotIn('api_token',path.read_text().lower())
if __name__=='__main__':unittest.main()
