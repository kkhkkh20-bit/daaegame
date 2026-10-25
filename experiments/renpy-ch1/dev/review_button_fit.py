"""버튼 납품 독립 검수: 복사된 게임·저장에 한정해 실제 세 화면을 캡처한다."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

import asset_toolbox_preview as preview

FIXTURE='''testcase button_fit_review:
    $ _test.timeout=40
    $ preferences.fullscreen=True
    $ preferences.text_cps=0
    $ persistent.room13_large_text=False
    pause 2.0
    screenshot "main.png"
    move id "r13_cover_new"
    run Function(r13_qa_button_mouse,True)
    pause .3
    assert eval (renpy.get_widget("main_menu","r13_cover_new_visual").pressed)
    screenshot "main-pressed.png"
    run Function(r13_qa_button_mouse,False)
    pause until screen "say" timeout 30
    run Call("r13_qa_roam",dict(day=2,period=0,location="square",life_poc=True),("lodging",))
    click pos (640,400) until screen "r13_hub" timeout 40
    $ r13_black_card=False
    pause .7
    screenshot "square.png"
    run Hide("r13_hub")
    run Hide("say")
    run Function(renpy.hide,"r13_visitor")
    run Show("r13_qa_notebook_topics")
    pause .7
    screenshot "question.png"
    click id "r13_side_topic_2"
    assert eval (r13_qa_notebook_pick==2)
    $ persistent.room13_large_text=True
    $ r13_touch_ui=lambda: True
    run Function(renpy.restart_interaction)
    pause .7
    screenshot "question-touch.png"
    click id "r13_topics_next"
    pause .3
    screenshot "question-touch-page2.png"
    click id "r13_side_topic_1"
    assert eval (r13_qa_notebook_pick==3)
    click "돌아가기"
    assert not screen "r13_qa_notebook_topics"
'''

MEASURE='''
init 999 python:
    def r13_review_fit_measure():
        import json, os
        rows=[]
        for family,size,icon_width,gap,canvas,safe,captions in (
            ("main_primary",28,30,10,(184,76),(164,42),("이어하기","처음부터","불러오기","설정")),
            ("topic_primary",22,24,6,(146,64),(130,36),("자료 제시","기록","더보기","돌아가기")),
            ("topic_primary",24,24,6,(146,88),(130,36),("자료 제시","기록","더보기","돌아가기","자료 보여주기"))):
            for caption in captions:
                visual=R13ButtonStateVisual(caption,family,*canvas,icon=Solid("#493324",xysize=(icon_width,icon_width)),text_size=size)
                renpy.render(visual,*canvas,0,0)
                text=renpy.render(Text(caption,font=R13_UI_BOLD_FONT,size=size),*canvas,0,0)
                tw,th=text.get_size()
                fit=min(1.0,safe[0]/float(tw+icon_width+gap),safe[1]/float(max(th,icon_width)))
                assert visual.scale==1.0
                assert fit==1.0 or caption=="자료 보여주기"
                assert max(th,icon_width)*fit/2+2<=safe[1]/2
                rows.append(dict(family=family,caption=caption,text_size=size,text_render=[tw,th],fit=fit,scale=visual.scale,pressed_offset=2))
        with open(os.path.join(config.basedir,"fit-measurements.json"),"w") as stream:
            json.dump(rows,stream,ensure_ascii=False,indent=2)
'''


def capture(project, output, measure=False):
    project=Path(project).resolve();output=Path(output).resolve()
    output.mkdir(parents=True,exist_ok=True)
    preview._CASE='button_fit_review'
    xvfb=Path('/tmp/r13-xvfb/usr/bin/xvfb-run')
    if not xvfb.is_file():xvfb=Path(shutil.which('xvfb-run'))
    sdk=Path(os.environ.get('RENPY_SDK','/tmp/renpy-8.5.3-sdk'))
    with tempfile.TemporaryDirectory(prefix='r13-fit-review-capture-') as temporary:
        root=Path(temporary);stage=root/'project'
        shutil.copytree(project/'game',stage/'game',ignore=shutil.ignore_patterns(
            'saves','cache','__pycache__','*.rpyc','*.rpymc','*.pyc'))
        fixture=FIXTURE
        if measure:
            fixture=fixture.replace('    screenshot "main.png"','    run Function(r13_review_fit_measure)\n    screenshot "main.png"')+MEASURE
        (stage/'game/qa_tests/zz_button_fit_review.rpy').write_text(fixture,encoding='utf-8')
        env=dict(os.environ,RENPY_PATH_TO_SAVES=str(root/'saves'),XDG_CACHE_HOME=str(root/'cache'),
                 R13_ASSET_TOOLBOX='0',SDL_AUDIODRIVER='dummy',PYTHONUNBUFFERED='1')
        env['PATH']=str(xvfb.parent)+os.pathsep+env.get('PATH','')
        log=output/'capture.log'
        command=[str(xvfb),'-a','-s','-screen 0 1280x720x24',str(sdk/'renpy.sh'),str(stage),'test',preview._CASE]
        with log.open('wb') as stream:
            process=subprocess.Popen(command,cwd=stage,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
            try:
                deadline=time.monotonic()+180
                while time.monotonic()<deadline:
                    statuses=re.findall(r'Status:\s*([A-Z]+)',log.read_text(errors='replace'))
                    if statuses:
                        if statuses[-1]!='PASSED':raise RuntimeError('캡처 검증 실패: '+str(log))
                        break
                    if process.poll() is not None:raise RuntimeError('캡처가 먼저 종료됨: '+str(log))
                    time.sleep(.25)
                else:raise RuntimeError('캡처 180초 초과: '+str(log))
            finally:
                preview._stop(process,stage)
                # Retain completed screenshots even when a later checkpoint fails.
                for path in (stage/'tests/screenshots').glob('*.png'):
                    shutil.copy2(path,output/path.name)
        for path in (stage/'tests/screenshots').glob('*.png'):shutil.copy2(path,output/path.name)
        if measure:shutil.copy2(stage/'fit-measurements.json',output/'fit-measurements.json')
        owned=preview._alive(preview._owned_processes(process.pid,stage))
        if owned:raise RuntimeError('캡처 자식 프로세스 잔류')
        (output/'result.json').write_text(json.dumps({'status':'PASSED','remaining_processes':len(owned),
            'source':str(project),'screenshots':sorted(p.name for p in output.glob('*.png'))},indent=2)+'\n')
        print('실제 화면 캡처 통과:',output,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('project');parser.add_argument('output')
    parser.add_argument('--measure',action='store_true')
    args=parser.parse_args();capture(args.project,args.output,args.measure)
