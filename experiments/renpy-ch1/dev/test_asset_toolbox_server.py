"""실제 Registry와 HTTP 서버를 임시 프로젝트에서 검증한다. 사용자 JSON은 쓰지 않는다."""
import copy
import json
from pathlib import Path
import re
import selectors
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen


PROJECT=Path(__file__).resolve().parents[1]
STATES=('basic','pressed','selected','disabled')


class AssetToolboxHTTP(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory(prefix='r13-asset-http-')
        self.addCleanup(temporary.cleanup)
        self.project=Path(temporary.name)
        self.game=self.project/'game'
        self.data=self.game/'asset-toolbox'
        self.data.mkdir(parents=True)
        (self.game/'python-packages').mkdir()
        (self.game/'assets').mkdir()
        shutil.copy2(PROJECT/'game/python-packages/r13_assets.py',
                     self.game/'python-packages/r13_assets.py')
        assets={}
        for state in STATES:
            source=PROJECT/'game/assets/ui-button-states'/('primary_'+state+'.png')
            target=self.game/'assets'/source.name
            shutil.copy2(source,target)
            contents=target.read_bytes()
            self.assertEqual(contents[:8],b'\x89PNG\r\n\x1a\n')
            size=list(struct.unpack('>II',contents[16:24]))
            for pack in ('first','second'):
                assets[pack+'.'+state]={
                    'path':'assets/'+target.name,'media':'image','size':size,
                    'tags':['pack:'+pack,'state:'+state],'render':{},
                    'label':pack+' '+state}
        assets['broken.basic']=copy.deepcopy(assets['first.basic'])
        assets['broken.basic']['tags']=['pack:broken','state:basic']
        # 모델이 자동 추가하는 기본 태그까지 정규화해 저장 보존을 정확히 비교한다.
        for asset_id,asset in assets.items():
            asset['id']=asset_id
            asset['tags']=sorted(asset['tags']+['asset:'+asset_id])
        self.catalog={'version':1,'assets':assets,'fixture_note':'보존할 메타데이터'}
        rule={'label':'함께 바뀌는 버튼','match':['pack:first'],
              'states':list(STATES),'fallback':{'hover':'basic'},
              'group':'button-pair','media':'image','canvas_size':size,'refresh':'live'}
        self.bindings={'version':1,'bindings':{
            'button.left':copy.deepcopy(rule),'button.right':copy.deepcopy(rule),
            'button.untouched':dict(copy.deepcopy(rule),group='separate')},
            'fixture_note':'연결 메타데이터도 보존'}
        self.catalog_path=self.data/'catalog.json'
        self.bindings_path=self.data/'bindings.json'
        self.catalog_path.write_text(json.dumps(self.catalog,ensure_ascii=False),encoding='utf-8')
        self.bindings_path.write_text(json.dumps(self.bindings,ensure_ascii=False),encoding='utf-8')

        # port=0은 OS가 고른 독립 포트다. 공유 개발 서버나 게임 런타임을 사용하지 않는다.
        code=('import sys; from pathlib import Path; '
              'sys.path.insert(0,sys.argv[1]); '
              'from asset_toolbox_server import run; '
              'run(Path(sys.argv[2]),host="127.0.0.1",port=0)')
        self.log=tempfile.TemporaryFile()
        self.addCleanup(self.log.close)
        self.process=subprocess.Popen(
            [sys.executable,'-u','-c',code,str(PROJECT/'dev'),str(self.project)],
            stdout=subprocess.PIPE,stderr=self.log)
        self.addCleanup(self.stop_server)
        with selectors.DefaultSelector() as selector:
            selector.register(self.process.stdout,selectors.EVENT_READ)
            self.assertTrue(selector.select(timeout=8),'HTTP 서버 시작 제한 시간 초과')
        line=self.process.stdout.readline().decode('utf-8')
        match=re.search(r'http://127\.0\.0\.1:(\d+)/',line)
        if not match:
            self.log.seek(0)
            self.fail('서버 시작 실패: '+line+self.log.read().decode('utf-8',errors='replace'))
        self.base='http://127.0.0.1:'+match.group(1)
        status,body=self.request('/api/catalog')
        self.assertEqual(status,200)
        self.assertEqual(body['errors'],[])
        self.token=body['token']

    def stop_server(self):
        if self.process.poll() is None:
            self.process.terminate()
            try:self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill();self.process.wait(timeout=3)
        self.process.stdout.close()

    def request(self,path,body=None,headers=None):
        values={}
        payload=None
        if body is not None:
            values={'Content-Type':'application/json','X-Asset-Token':getattr(self,'token','')}
            payload=json.dumps(body).encode('utf-8')
        if headers is not None:values.update(headers)
        request=Request(self.base+path,data=payload,headers=values)
        try:response=urlopen(request,timeout=5)
        except HTTPError as exc:response=exc
        with response:
            contents=response.read()
            if response.headers.get('Content-Type','').startswith('application/json'):
                contents=json.loads(contents)
            return response.status,contents

    def test_group_assignment_replaces_file_atomically_and_preserves_other_roles(self):
        before=self.bindings_path.read_bytes()
        old_inode=self.bindings_path.stat().st_ino
        # 기존 파일을 열린 채로 두어 이름 교체와 파일 내용 덮어쓰기를 구분한다.
        with self.bindings_path.open('rb') as old_file:
            status,response=self.request('/api/assign',{'role':'button.left','asset_id':'second.selected'})
            self.assertEqual(status,200,response)
            self.assertEqual(old_file.read(),before)
        self.assertNotEqual(self.bindings_path.stat().st_ino,old_inode)
        saved=json.loads(self.bindings_path.read_text(encoding='utf-8'))
        self.assertEqual(saved['fixture_note'],self.bindings['fixture_note'])
        for role in ('button.left','button.right'):
            expected=dict(self.bindings['bindings'][role],match=['pack:second'])
            self.assertEqual(saved['bindings'][role],expected)
            for state in STATES:
                self.assertEqual(response['resolved'][role][state]['id'],'second.'+state)
        self.assertEqual(saved['bindings']['button.untouched'],self.bindings['bindings']['button.untouched'])
        self.assertEqual(json.loads(self.catalog_path.read_text(encoding='utf-8')),self.catalog)
        self.assertEqual(sorted(p.name for p in self.data.iterdir()),['bindings.json','catalog.json'])

    def test_incomplete_pack_is_rejected_without_touching_either_json(self):
        original={p:p.read_bytes() for p in (self.catalog_path,self.bindings_path)}
        status,response=self.request('/api/assign',{'role':'button.left','asset_id':'broken.basic'})
        self.assertEqual(status,422,response)
        self.assertIn('매칭',response['error'])
        for path,contents in original.items():self.assertEqual(path.read_bytes(),contents)
        self.assertEqual(sorted(p.name for p in self.data.iterdir()),['bindings.json','catalog.json'])

    def test_token_origin_fetch_site_and_host_reject_external_writes(self):
        before=self.bindings_path.read_bytes()
        for headers in ({'X-Asset-Token':''},{'X-Asset-Token':'wrong'},
                        {'Origin':'https://unrelated.example'},{'Sec-Fetch-Site':'cross-site'},
                        {'Host':'unrelated.example'}):
            with self.subTest(headers=headers):
                status,_=self.request('/api/assign',{'role':'button.left','asset_id':'second.basic'},headers)
                self.assertEqual(status,403)
                self.assertEqual(self.bindings_path.read_bytes(),before)
        self.assertEqual(self.request('/api/catalog',headers={'Host':'unrelated.example'})[0],403)
        self.assertEqual(self.request('/api/assign',{'role':'button.left','asset_id':'second.basic'},
                                      {'Origin':self.base,'Sec-Fetch-Site':'same-origin'})[0],200)

    def test_assets_cannot_escape_the_assets_directory(self):
        secret=self.game/'outside.png'
        secret.write_bytes(b'not-a-public-asset')
        (self.game/'assets/escape.png').symlink_to(secret)
        for path in ('/assets/../outside.png','/assets/%2e%2e/outside.png',
                     '/assets/%2e%2e%2foutside.png','/assets/escape.png',
                     '/assets/../asset-toolbox/catalog.json'):
            with self.subTest(path=path):
                status,body=self.request(path)
                self.assertEqual(status,404)
                self.assertNotIn('not-a-public-asset',str(body))
        status,body=self.request('/assets/primary_basic.png')
        self.assertEqual(status,200)
        self.assertEqual(body,(self.game/'assets/primary_basic.png').read_bytes())

    def test_tag_save_preserves_metadata_and_bindings_and_invalid_edit_is_not_saved(self):
        before=self.bindings_path.read_bytes()
        tags=self.catalog['assets']['first.basic']['tags']+['mood:동화']
        status,response=self.request('/api/tags',{'asset_id':'first.basic','tags':tags})
        self.assertEqual(status,200,response)
        expected=copy.deepcopy(self.catalog)
        expected['assets']['first.basic']['tags']=sorted(tags)
        self.assertEqual(json.loads(self.catalog_path.read_text(encoding='utf-8')),expected)
        self.assertEqual(self.bindings_path.read_bytes(),before)
        saved=self.catalog_path.read_bytes()
        status,response=self.request('/api/tags',{'asset_id':'first.basic','tags':['state:basic']})
        self.assertEqual(status,422,response)
        self.assertEqual(self.catalog_path.read_bytes(),saved)
        self.assertEqual(self.bindings_path.read_bytes(),before)


if __name__=='__main__':unittest.main()
