"""교체 이후에도 제작 ZIP이 기존 화면의 파일 참조를 보존하는지 확인한다."""
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'game/python-packages'))
from r13_assets import Registry
from asset_toolbox_export import request_zip, source_usage


class AssetToolboxExport(unittest.TestCase):
    def test_reassigned_group_reports_original_file_and_all_consumers(self):
        with tempfile.TemporaryDirectory() as temporary:
            project=Path(temporary)
            assets=project/'game/assets'
            assets.mkdir(parents=True)
            (assets/'old.png').write_bytes(b'original')
            (assets/'new.png').write_bytes(b'replacement')
            (project/'game/title.rpy').write_text('add "assets/old.png"\n',encoding='utf-8')
            (project/'game/options.rpy').write_text('add r13_asset("logo.copy")\n',encoding='utf-8')
            (project/'game/qa_tests').mkdir()
            (project/'game/qa_tests/test.rpy').write_text('add "assets/old.png"\n',encoding='utf-8')
            catalog={'version':1,'assets':{
                key:dict(path='assets/'+key+'.png',media='image',size=[1,1],tags=[])
                for key in ('old','new')}}
            bindings={'version':1,'bindings':{
                key:dict(group='logo',match=['asset:old'],states=['basic'],consumers=[consumer])
                for key,consumer in [('logo','메인'),('logo.copy','설정'),('file:assets/old.png','파일 별칭')]}}
            model=Registry(catalog,bindings)
            model.assign('logo','new')
            usage=source_usage(project,model,'logo')
            self.assertEqual(set(usage['direct_references']),{'game/title.rpy:1','game/options.rpy:1'})
            self.assertEqual(usage['declared_consumers'],['메인','설정','파일 별칭'])
            with zipfile.ZipFile(io.BytesIO(request_zip(project,model,'logo'))) as archive:
                self.assertEqual(json.loads(archive.read('usage.json')),usage)
                self.assertEqual(archive.read('originals/assets/new.png'),b'replacement')
                self.assertEqual(len(json.loads(archive.read('matching.json'))['items']),3)
            self.assertEqual((assets/'old.png').read_bytes(),b'original')
            self.assertEqual((assets/'new.png').read_bytes(),b'replacement')


if __name__=='__main__':unittest.main()
