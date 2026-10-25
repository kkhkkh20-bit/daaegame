"""Module downloads round-trip without changing branch metadata or partially writing sources."""
import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import dialogue_modules as dm

class DialogueModules(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name);self.game=self.root/'game';(self.game/'v111/newworld').mkdir(parents=True)
  recs={f'MS14_D01_S01_L000{i}':dict(id=f'MS14_D01_S01_L000{i}',speaker='아빠',kind='dialogue',text=f'원문 {i}') for i in range(1,7)}
  recs['MS14_D01_S01_L0001']['text']='원문 </script> 줄\u2028사이\u2029끝'
  self.put('game/v111/records.json',dict(records=recs,evidence={'E1':dict(variants=dict(observed='자료 원문'))}))
  self.put('game/v111/field-bindings.json',{'wait1':dict(options=[dict(title='선택 원문',location='square')])})
  self.put('game/v111/newworld/d01.json',dict(replace={'MS14_D01_S01_L0002':dict(text='조건 대사',when='branch_yes'),'MS14_D01_S01_L0003':dict(text='현재 대사')},drop=['MS14_D01_S01_L0004'],after={'MS14_D01_S01_L0001':[dict(id='NW_AFTER',text='뒤 대사',speaker='다람',when='branch_no')]},blocks={}))
  self.put('game/v111/newworld/hidden_base.json',dict(blocks={'greet':[dict(id='NW_HIDDEN',text='숨은 인사',speaker='엄마')]}))
  (self.game/'main.rpy').write_text('''init 319 python:
    R13_NW_WHEN={
        "branch_yes":lambda: r13_v111_value("won") is True,
        "branch_no":lambda: not r13_v111_value("won"),
    }
    R13_V111_CARRIAGE_TEXT = {
        "MS14_D01_S01_L0006":"마차 대사",
    }
    R13_NW_WRONG_THOUGHTS={"쟁점":{1:"기록을 다시 읽자."}}
label start:
    $ r13_v111_scene('MS14_D01_S01')
    call r13_v111_lines(['MS14_D01_S01_L0001','MS14_D01_S01_L0002','MS14_D01_S01_L0003','MS14_D01_S01_L0004','MS14_D01_S01_L0006'])
    call r13_nw_block('greet')
    call r13_lines([("아빠","직접 대사",{"pose":("값","배치키")})],"direct")
    menu:
        "계속 간다":
            pass
''')
  self.out=self.root/'docs/dialogue-modules';self.template=self.root/'dev/dialogue-modules/index.html';self.template.parent.mkdir(parents=True);self.template.write_text('<script>const DATA=__DATA__;</script>')
 def put(self,path,value):
  p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(dm.encode(value))
 def collect(self):return dm.collect(self.root,self.out)
 def row(self,inventory,rid,origin=None):return next(r for r in inventory['rows'] if r['id']==rid and (origin is None or r['origin']==origin))
 def package(self,inv,rows):return dict(schema=dm.EDIT_SCHEMA,source_stamp=inv['stamp'],entries=copy.deepcopy(rows))
 def test_full_unchanged_export_is_valid_and_does_not_write(self):
  inv=self.collect();before=(self.game/'v111/records.json').read_bytes();report=dm.apply_package(self.package(inv,inv['rows']),self.root,self.out)
  self.assertEqual(report['changed'],0);self.assertEqual((self.game/'v111/records.json').read_bytes(),before)
 def test_base_edits_become_runtime_override_and_status_persists(self):
  inv=self.collect();row=self.row(inv,'MS14_D01_S01_L0001','base');p=self.package(inv,[row]);p['entries'][0].update(text='고친 실제 대사',review_status='reviewed')
  dm.apply_package(p,self.root,self.out,True)
  data=json.loads((self.game/'v111/newworld/d01.json').read_text());self.assertEqual(data['replace'][row['id']]['text'],'고친 실제 대사')
  now=self.collect();active=self.row(now,row['id'],'patch');self.assertEqual(active['review_status'],'reviewed');self.assertEqual(self.row(now,row['id'],'base')['usage'],'overridden')
 def test_conditional_text_and_fallback_can_be_edited_together(self):
  inv=self.collect();rid='MS14_D01_S01_L0002';p=self.package(inv,[self.row(inv,rid,'base'),self.row(inv,rid,'patch')]);p['entries'][0]['text']='기본 새 대사';p['entries'][1]['text']='조건 새 대사'
  dm.apply_package(p,self.root,self.out,True);v=json.loads((self.game/'v111/newworld/d01.json').read_text())['replace'][rid]
  self.assertEqual(v,[dict(text='조건 새 대사',when='branch_yes'),dict(text='기본 새 대사')])
 def test_stale_source_is_rejected_even_if_target_text_unchanged(self):
  inv=self.collect();p=self.package(inv,[self.row(inv,'NW_AFTER')]);p['entries'][0]['text']='수정'
  script=self.game/'main.rpy';script.write_text(script.read_text()+'\n# 다른 변경\n')
  with self.assertRaisesRegex(dm.ModuleError,'source_stamp'):dm.apply_package(p,self.root,self.out,True)
 def test_metadata_unknown_fields_and_duplicates_are_rejected(self):
  inv=self.collect();row=self.row(inv,'NW_AFTER')
  for key,value in [('when','branch_yes'),('path',['../escape']),('source_hash','bad'),('baseline_hash','bad'),('editable',1),('new_field','bad')]:
   p=self.package(inv,[row]);p['entries'][0][key]=value
   with self.assertRaises(dm.ModuleError):dm.apply_package(p,self.root,self.out,True)
  with self.assertRaisesRegex(dm.ModuleError,'중복'):dm.apply_package(self.package(inv,[row,row]),self.root,self.out,True)
 def test_readonly_text_is_rejected_but_review_status_allowed(self):
  inv=self.collect();row=self.row(inv,'MS14_D01_S01_L0003','base');self.assertFalse(row['editable']);p=self.package(inv,[row]);p['entries'][0]['text']='가려진 수정'
  with self.assertRaisesRegex(dm.ModuleError,'읽기 전용'):dm.apply_package(p,self.root,self.out,True)
  p['entries'][0]['text']=row['text'];p['entries'][0]['review_status']='needs_work';dm.apply_package(p,self.root,self.out,True)
  self.assertEqual(self.row(self.collect(),row['id'],'base')['review_status'],'needs_work')
 def test_invalid_later_entry_never_partially_writes(self):
  inv=self.collect();p=self.package(inv,[self.row(inv,'NW_AFTER'),self.row(inv,'NW_HIDDEN')]);p['entries'][0]['text']='정상수정';p['entries'][1]['id']='바뀐 ID'
  before=(self.game/'v111/newworld/d01.json').read_bytes()
  with self.assertRaises(dm.ModuleError):dm.apply_package(p,self.root,self.out,True)
  self.assertEqual((self.game/'v111/newworld/d01.json').read_bytes(),before);self.assertFalse((self.out/'review-status.json').exists())
 def test_replace_failure_rolls_back_every_written_file(self):
  inv=self.collect();p=self.package(inv,[self.row(inv,'NW_AFTER'),self.row(inv,'NW_HIDDEN')]);p['entries'][0]['text']='첫 변경';p['entries'][1]['text']='둘째 변경'
  files=[self.game/'v111/newworld/d01.json',self.game/'v111/newworld/hidden_base.json'];before={f:f.read_bytes() for f in files};real=os.replace;count=[0]
  def failing(a,b):
   count[0]+=1
   if count[0]==2:raise OSError('simulated replacement failure')
   return real(a,b)
  with patch.object(dm.os,'replace',side_effect=failing):
   with self.assertRaisesRegex(OSError,'simulated'):dm.apply_package(p,self.root,self.out,True)
  self.assertEqual({f:f.read_bytes() for f in files},before);self.assertFalse((self.out/'review-status.json').exists())
 def test_interpolation_and_control_tags_cannot_be_added(self):
  inv=self.collect();row=self.row(inv,'NW_AFTER')
  for text in ['바뀐 [unknown_variable]','{a=jump:evil}누르기{/a}']:
   p=self.package(inv,[row]);p['entries'][0]['text']=text
   with self.assertRaisesRegex(dm.ModuleError,'보간식/제어'):dm.apply_package(p,self.root,self.out,True)
 def test_rpy_span_roundtrip_escapes_code_and_does_not_edit_metadata(self):
  inv=self.collect();row=next(r for r in inv['rows'] if r['text']=='직접 대사');self.assertTrue(row['editable'])
  pose=next(r for r in inv['rows'] if r['text']=='배치키');self.assertFalse(pose['editable'])
  value="한글\n'); __import__('os').system('no execute') # \\\"";p=self.package(inv,[row]);p['entries'][0]['text']=value
  dm.apply_package(p,self.root,self.out,True);now=self.collect();self.assertTrue(any(r['text']==value and r['editable'] for r in now['rows']))
  self.assertIn(json.dumps(value,ensure_ascii=False),(self.game/'main.rpy').read_text())
 def test_build_escaping_and_branch_exports_cover_every_row(self):
  report=dm.build(self.root,self.out,self.template);inv=json.loads((self.out/'inventory.json').read_text());html=(self.out/'index.html').read_text();payload=html.split('const DATA=',1)[1].rsplit(';</script>',1)[0]
  self.assertEqual(json.loads(payload),inv);self.assertNotIn('</script> 줄',payload)
  self.assertEqual(sum(b['count'] for b in inv['branches']),len(inv['rows']))
  for branch in inv['branches']:
   exported=json.loads((self.out/branch['file']).read_text());self.assertEqual(len(exported['entries']),branch['count']);dm.validate(exported,inv)
  self.assertIn('branch_yes',inv['predicates']);self.assertIn('r13_v111_value',inv['predicates']['branch_yes'])
  self.assertEqual(report['rows'],len(inv['rows']));self.assertEqual(inv['reading'],{})
 def test_reading_is_utf8_html_with_edit_links_and_downloadable_source(self):
  (self.root/'dev').mkdir(exist_ok=True)
  (self.root/'dev/dialogue_day.py').write_text('# test reader')
  for day in range(2,15):self.put(f'game/v111/newworld/d{day:02}.json',{})
  sample='S01_L0001 아빠: 한글 <script>대사</script>\n'
  with patch.object(dm.subprocess,'check_output',return_value=sample):dm.build(self.root,self.out,self.template)
  inv=json.loads((self.out/'inventory.json').read_text())
  self.assertEqual(inv['reading']['1'],'reading/d01.html')
  self.assertEqual((self.out/'reading/d01.txt').read_text(),sample)
  page=(self.out/'reading/d01.html').read_text()
  self.assertIn('charset="utf-8"',page)
  self.assertIn('q=MS14_D01_S01_L0001',page)
  self.assertIn('&lt;script&gt;대사&lt;/script&gt;',page)
  self.assertNotIn('<script>대사</script>',page)
 def test_hidden_reading_appendix_keeps_day_conditions_and_original_order(self):
  def row(id,day,text,**kw):return dict(id=id,day=day,text=text,origin='patch',usage='active',file='game/v111/newworld/hidden_base.json',block='base_marks11',placement='blocks',speaker='엄마',when=None,**kw)
  inv=dict(rows=[row('NW_MAIN',11,'이미 본 줄'),row('NW_HIDDEN_A',11,'먼저 보는 줄'),dict(row('NW_HIDDEN_B',11,'갈래 줄'),when='base_open'),row('NW_OTHER',7,'다른 날'),dict(row('NW_UNKNOWN',11,'미확인'),usage='unknown')])
  raw='  +NW_MAIN (블록) 엄마: 이미 본 줄\n'
  result=dm.supplement_reading(inv,11,raw)
  self.assertEqual(result.count('NW_MAIN'),1)
  self.assertLess(result.index('NW_HIDDEN_A'),result.index('NW_HIDDEN_B'))
  self.assertIn('{base_open}',result)
  self.assertIn('모두 재생된다는 뜻이 아니다',result)
  self.assertNotIn('NW_OTHER',result);self.assertNotIn('NW_UNKNOWN',result)
  self.assertEqual(dm.supplement_reading(inv,14,raw),raw)
 def test_rpy_day_uses_label_not_position_or_previous_scene(self):
  (self.game/'later.rpy').write_text('label first:\n    $ r13_v111_scene(\'MS14_D08_S01\')\nlabel r13_v111_invite12:\n    call r13_lines([("아빠","열두째 날 직접 대사")],"intro")\n    $ renpy.display_menu([("여기서 기다린다",0)])\nlabel r13_common_helper:\n    call r13_lines([("아빠","공통 도움말")],"shared")\n')
  inv=self.collect()
  actual=next(r for r in inv['rows'] if r['text']=='열두째 날 직접 대사')
  self.assertEqual(actual['day'],12)
  self.assertEqual(actual['scene'],'r13_v111_invite12')
  self.assertIsNone(next(r for r in inv['rows'] if r['text']=='공통 도움말')['day'])
  self.assertIsNone(next(r for r in inv['rows'] if r['text']=='기록을 다시 읽자.')['day'])
  menu=next(r for r in inv['rows'] if r['text']=='여기서 기다린다')
  self.assertEqual((menu['origin'],menu['kind'],menu['day']),('rpy_menu','choice',12))
if __name__=='__main__':unittest.main()
