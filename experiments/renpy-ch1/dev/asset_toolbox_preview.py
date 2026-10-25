"""현재 연결로 실제 Ren'Py 회의를 캡처한다. 게임과 저장은 임시 프로젝트에 격리한다."""
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import tempfile
import threading
import time


_LOCK=threading.Lock()
_CASE='toolbox_meeting_preview'
_SHOT='toolbox-meeting-current.png'
_TIMEOUT=180
_IGNORED={'saves','cache','__pycache__'}


class PreviewError(RuntimeError):
    pass


def _fingerprint(game):
    """실행 중 연결·원본·스크립트가 바뀌면 잘못된 비교본을 게시하지 않는다."""
    digest=hashlib.sha256()
    for path in sorted(game.rglob('*')):
        relative=path.relative_to(game)
        if any(p in _IGNORED for p in relative.parts) or path.suffix in ('.rpyc','.rpymc','.pyc'):
            continue
        if not path.is_file():continue
        stat=path.stat()
        digest.update(str(relative).encode('utf-8'))
        digest.update(('%d:%d'%(stat.st_size,stat.st_mtime_ns)).encode())
        if relative.as_posix() in ('asset-toolbox/catalog.json','asset-toolbox/bindings.json'):
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _fixture(game):
    # 이미 검증된 관리자 회의 fixture의 실제 화면 진입과 assertions를 그대로 쓴다.
    source=(game/'qa_tests/admin_meeting.rpy').read_text(encoding='utf-8')
    marker='    screenshot "admin-meeting-02-c2-live.png"'
    try:body=source.split('testcase admin_meeting_replay:\n',1)[1].split(marker,1)
    except IndexError as exc:raise PreviewError('회의 미리보기용 기존 QA fixture를 찾을 수 없습니다.') from exc
    if len(body)!=2:raise PreviewError('회의 QA의 캡처 지점이 바뀌었습니다. fixture를 갱신해 주세요.')
    body=body[0]
    # UI를 합성하지 않는다. 실제 게임 화면을 가상 1280×720 모니터에 전체화면 표시한다.
    header='testcase '+_CASE+':\n    $ preferences.fullscreen=True\n    $ preferences.text_cps=0\n'
    return header+body+'    screenshot "'+_SHOT+'"\n'


def _processes():
    result={}
    for entry in Path('/proc').iterdir():
        if not entry.name.isdigit():continue
        try:
            fields=(entry/'stat').read_text().rsplit(')',1)[1].split()
            result[int(entry.name)]=(int(fields[1]),fields[19],fields[0],
                (entry/'cmdline').read_bytes().split(b'\0'))
        except (OSError,ValueError,IndexError):pass
    return result


def _owned_processes(pid,stage=None):
    table=_processes();owned={pid}
    if stage is not None:
        exact=os.fsencode(stage)
        # Ren'Py는 별도 세션으로 분리될 수 있다. 정확한 임시 프로젝트+QA 이름만 허용한다.
        owned.update(p for p,(_,_,_,args) in table.items()
                     if exact in args and _CASE.encode() in args and b'test' in args)
    while True:
        children={p for p,(parent,_,_,_) in table.items() if parent in owned}
        if children<=owned:break
        owned.update(children)
    return {p:table[p][1] for p in owned if p in table}


def _alive(owned):
    table=_processes()
    # 시작 시각까지 확인해 PID가 재사용된 다른 프로세스에는 신호를 보내지 않는다.
    return {p:start for p,start in owned.items()
            if p in table and table[p][1]==start and table[p][2]!='Z'}


def _signal_owned(owned,sig):
    for pid in _alive(owned):
        try:os.kill(pid,sig)
        except ProcessLookupError:pass


def _stop(process,stage=None):
    owned=_owned_processes(process.pid,stage)
    children={p:start for p,start in owned.items() if p!=process.pid}
    _signal_owned(children,signal.SIGTERM)
    deadline=time.monotonic()+1
    while _alive(children) and time.monotonic()<deadline:time.sleep(.05)
    _signal_owned({p:start for p,start in owned.items() if p==process.pid},signal.SIGTERM)
    try:process.wait(timeout=1)
    except subprocess.TimeoutExpired:pass
    owned.update(_owned_processes(process.pid,stage))
    _signal_owned(owned,signal.SIGKILL)
    process.wait(timeout=3)
    deadline=time.monotonic()+1
    while _alive(owned) and time.monotonic()<deadline:time.sleep(.05)
    if _alive(owned):raise PreviewError('캡처용 자식 프로세스가 종료되지 않았습니다.')


def _write(path,contents):
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.'+path.name+'.',delete=False) as stream:
            temporary=Path(stream.name)
            stream.write(contents);stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,path)
    finally:
        if temporary and temporary.exists():temporary.unlink()


def capture(project):
    """images[{label,url}], captured_at, fingerprint를 반환한다. 실패 시 PreviewError."""
    if not _LOCK.acquire(blocking=False):raise PreviewError('이미 회의 화면을 캡처하고 있습니다. 완료 후 다시 시도해 주세요.')
    try:
        project=Path(project).resolve()
        if not (project/'game').is_dir():project=project/'experiments/renpy-ch1'
        game=project/'game'
        if not game.is_dir():raise PreviewError('Ren’Py 게임 프로젝트를 찾을 수 없습니다.')
        output=project/'docs/reviews/toolbox-preview'
        output.mkdir(parents=True,exist_ok=True)
        with (output/'.capture.lock').open('a+b') as lock:
            try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError as exc:raise PreviewError('다른 도구함에서 회의 화면을 캡처하고 있습니다.') from exc
            return _capture(project,output)
    finally:_LOCK.release()


def _capture(project,output):
    game=project/'game'
    sdk=Path(os.environ.get('RENPY_SDK','/tmp/renpy-8.5.3-sdk'))
    xvfb=Path('/tmp/r13-xvfb/usr/bin/xvfb-run')
    if not xvfb.is_file():
        found=shutil.which('xvfb-run')
        if not found:raise PreviewError('실제 화면 캡처에 필요한 xvfb-run을 찾을 수 없습니다.')
        xvfb=Path(found)
    if not (sdk/'renpy.sh').is_file():raise PreviewError('Ren’Py SDK가 없습니다. RENPY_SDK 경로를 설정해 주세요.')
    fingerprint=_fingerprint(game)
    fixture=_fixture(game)
    with tempfile.TemporaryDirectory(prefix='r13-toolbox-preview-') as temporary:
        root=Path(temporary);stage=root/'project'

        def copy_file(source,target):
            # 원본 그림은 읽기만 한다. 코드·JSON·설정·저장은 반드시 별도 파일로 복사한다.
            if Path(source).is_relative_to(game/'assets'):
                try:os.link(source,target);return target
                except OSError:pass
            return shutil.copy2(source,target)

        def ignore(directory,names):
            return [name for name in names if name in _IGNORED or name.endswith(('.rpyc','.rpymc','.pyc'))]

        shutil.copytree(game,stage/'game',copy_function=copy_file,ignore=ignore)
        (stage/'game/qa_tests/zz_toolbox_preview.rpy').write_text(fixture,encoding='utf-8')
        env=os.environ.copy()
        env['RENPY_PATH_TO_SAVES']=str(root/'isolated-saves')
        env['XDG_CACHE_HOME']=str(root/'isolated-cache')
        env['R13_ASSET_TOOLBOX']='0'  # 잠금된 복사본의 연결만 사용한다.
        env['SDL_AUDIODRIVER']='dummy'
        env['PYTHONUNBUFFERED']='1'
        env['PATH']=str(xvfb.parent)+os.pathsep+env.get('PATH','')
        log=root/'capture.log'
        command=[str(xvfb),'-a','-s','-screen 0 1280x720x24',str(sdk/'renpy.sh'),str(stage),'test',_CASE]
        with log.open('wb') as stream:
            process=subprocess.Popen(command,cwd=stage,env=env,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
            deadline=time.monotonic()+_TIMEOUT
            try:
                while time.monotonic()<deadline:
                    text=log.read_text(encoding='utf-8',errors='replace')
                    statuses=re.findall(r'Status:\s*([A-Z]+)',text)
                    if statuses:
                        if statuses[-1]!='PASSED':raise PreviewError('회의 화면 캡처 검증 실패:\n'+text[-3500:])
                        break
                    if process.poll() is not None:raise PreviewError('Ren’Py 실행이 완료 전에 종료됐습니다:\n'+text[-3500:])
                    time.sleep(.25)
                else:raise PreviewError('회의 화면 캡처 시간이 %d초를 초과했습니다.'%_TIMEOUT)
            finally:_stop(process,stage)
        shot=stage/'tests/screenshots'/_SHOT
        if not shot.is_file():raise PreviewError('회의 QA는 끝났지만 실제 캡처 파일이 없습니다.')
        from PIL import Image
        with Image.open(shot) as image:
            size=list(image.size);image.verify()
        if _fingerprint(game)!=fingerprint:
            raise PreviewError('캡처 중 에셋 연결 또는 게임 파일이 변경됐습니다. 변경을 마친 뒤 다시 캡처해 주세요.')
        current=output/'current.png';before=output/'before.png';metadata=output/'capture.json'
        previous={}
        if metadata.is_file():
            try:previous=json.loads(metadata.read_text(encoding='utf-8'))
            except (ValueError,OSError):pass
        images=[]
        if current.is_file():
            _write(before,current.read_bytes())
            images.append(dict(label='이전 캡처 · 같은 회의',url='/preview/before.png',
                               captured_at=previous.get('captured_at'),fingerprint=previous.get('fingerprint')))
        _write(current,shot.read_bytes())
        captured_at=datetime.now(timezone.utc).isoformat(timespec='seconds')
        images.append(dict(label='현재 연결 · 실제 회의 화면',url='/preview/current.png',captured_at=captured_at,fingerprint=fingerprint))
        result=dict(images=images,captured_at=captured_at,fingerprint=fingerprint,size=size,
                    renderer='RenPy',testcase=_CASE,source_fixture='admin_meeting_replay',
                    note='격리된 제작용 회의 fixture이며 자연 진행의 저장 기록은 사용하지 않습니다.')
        _write(metadata,(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
        return result
