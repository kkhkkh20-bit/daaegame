"""A04 화면 fixture: 광장/숲 좌우 카메라, 얼굴/필수 물건과 고정 조작의 겹침.

새 게임 이후 날짜·장소·장면·라벨은 명시적 검수 fixture이며 자연 진행으로 주장하지 않는다.
준비된 ROOM13_URL만 사용한다. ROOM13_LAYOUT_BASELINE=1은 개선 전 계측으로 기하 단언을 생략한다.
"""
import asyncio,json,os,traceback
from pathlib import Path
from playwright.async_api import async_playwright
from qa_play_review_field import FieldQA,FOCUS,overlap

OUT=Path(os.environ.get('ROOM13_QA_OUT','/tmp/room13-qa/additional-field-layout'))
URL=os.environ.get('ROOM13_URL','http://127.0.0.1:8765/preview/room13-dev/')
BASELINE=bool(os.environ.get('ROOM13_LAYOUT_BASELINE'))
SIZES=[('pc',1280,720),('phone',844,390),('small-phone',740,360)]
OUT.mkdir(parents=True,exist_ok=True)
PROBE='''import renpy
s=renpy.store;rows=s.r13_stage_people();offset=s.r13_world_offset();zoom=s.r13_field_zoom()
def project(rect):
 x,y,w,h=rect;return [(x-offset)*zoom,y*zoom,w*zoom,h*zoom]
result=dict(offset=offset,zoom=zoom,world=s.r13_world_width(),actors=rows,
 faces={a['person']:project(s.r13_actor_face_target(a) or a['rect']) for a in rows},
 labels=s.r13_actor_nameplates(rows),ui=s.r13_field_ui_rects(),
 objects={k:project(v['rect']) for k,v in s.ROOM13['objects'][s.room13['location']].items() if k in ('lamp','v111_box')})
'''

async def main():
 report=dict(scope=__doc__,baseline=BASELINE,measurements=[],checks=[],page_errors=[])
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport=dict(width=1280,height=720),has_touch=True);q=FieldQA(page,OUT)
  page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
  try:
   await page.goto(URL);await page.wait_for_function("typeof renpy_exec==='function'",timeout=300000);await q.wait('main_menu')
   report['version']=await q.py('import renpy;result=renpy.config.version')
   await q.py('import renpy;renpy.store.preferences.text_cps=0;result=True');await q.press('처음부터');await q.wait('say')
   for location,gate in [('square','lamp_rope'),('forest','box_inspect')]:
    # Prepare a complete stage fixture; label entry creates its own hub/viewport.
    await q.py("import renpy;s=renpy.store;s.r13_edit(day=2,period=0,location="+repr(location)+");s.r13_v111_set('day',2);s.room13['v111']['scene']='MS14_D02_S01';s.r13_v111_talk_person=None;s.r13_goal_open=False;s.r13_v111_context("+repr(gate)+");s.r13_v111_arrive(['daram','resident_lamplighter']);result=True")
    await q.jump_fixture('r13_v111_'+gate);await q.wait('r13_hub')
    for tag,width,height in (SIZES[:1] if BASELINE else SIZES):
     for large in (False,True):
      await q.setting_fixture(width,height,large)
      for side,x in [('left',48),('right',1232)]:
       await q.input(x,276);await asyncio.sleep(1)
       layout=await q.py(PROBE)
       offenders=[]
       for person,face in layout['faces'].items():
        visible=(max(0,face[0]),max(0,face[1]),max(0,min(1280,face[0]+face[2])-max(0,face[0])),max(0,min(720,face[1]+face[3])-max(0,face[1])))
        if visible[2]*visible[3] and any(overlap(visible,u)>1 for u in layout['ui']):offenders.append(person)
       layout.update(location=location,size=tag,large=large,side=side,face_ui_overlap=offenders)
       report['measurements'].append(layout)
       await q.shot('-'.join((location,tag,'large' if large else 'normal',side)))
       if not BASELINE:assert not offenders,layout
   assert not report['page_errors'],report['page_errors']
   report['status']='measured-baseline' if BASELINE else 'passed-pending-visual-review'
  except Exception:
   report['status']='failed';report['error']=traceback.format_exc();await page.screenshot(path=str(OUT/'failure.png'))
  finally:
   (OUT/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(dict(status=report.get('status'),count=len(report['measurements']),error=report.get('error')),ensure_ascii=False),flush=True)
   await browser.close()
 if report['status']=='failed':raise SystemExit(1)

if __name__=='__main__':asyncio.run(main())
