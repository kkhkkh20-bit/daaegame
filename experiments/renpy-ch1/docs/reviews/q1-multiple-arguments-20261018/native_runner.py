import asyncio,os,re,shutil,signal,json,time
from pathlib import Path
ROOT=Path('/workspace/daaegame-q1/experiments/renpy-ch1');OUT=Path('/tmp/daram-q1v-native');OUT.mkdir(exist_ok=True)
text=(ROOT/'dev/run_renpy_tests.sh').read_text()
tests=re.search(r'&& TESTS=\(([^)]+)\)',text).group(1).split()+['override_chain']
results=[];queue=asyncio.Queue()
for tc in tests:queue.put_nowait(tc)
async def worker(n):
 project=OUT/('worker%d'%n);project.mkdir(exist_ok=True)
 def ignore(path,names):return [x for x in names if x in ('cache','saves','__pycache__')]
 if (project/'game').exists():shutil.rmtree(project/'game')
 (project/'game').mkdir()
 for item in (ROOT/'game').iterdir():
  if item.name in ('cache','saves','__pycache__'):continue
  dest=project/'game'/item.name
  if item.name=='assets':dest.symlink_to(item,target_is_directory=True)
  elif item.is_dir():shutil.copytree(item,dest,ignore=ignore)
  else:shutil.copy2(item,dest)
 env=dict(os.environ,PATH='/tmp/daram-xvfb/usr/bin:'+os.environ['PATH'],SDL_AUDIODRIVER='dummy',RENPY_PATH_TO_SAVES=str(project/'user-saves'))
 while not queue.empty():
  tc=queue.get_nowait();path=OUT/(tc+'.txt');started=time.monotonic()
  for folder in ('game/saves','tests','user-saves'):shutil.rmtree(project/folder,ignore_errors=True)
  with path.open('w') as log:
   proc=await asyncio.create_subprocess_exec('xvfb-run','-a','-s','-screen 0 1280x720x24','/tmp/daram-sdk/renpy-8.5.3-sdk/renpy.sh',str(project),'test',tc,stdout=log,stderr=asyncio.subprocess.STDOUT,env=env,start_new_session=True)
   state='TIMEOUT'
   for i in range(400):
    await asyncio.sleep(1)
    text=path.read_text(errors='replace');matches=re.findall(r'Status: ([A-Z]+)',text)
    if matches:state=matches[-1];break
    if 'RenpyTestTimeoutError:' in text or 'An exception has occurred' in text or 'TypeError:' in text:state='ERROR';break
    if proc.returncode is not None:state='EXIT';break
   try:os.killpg(proc.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   try:await asyncio.wait_for(proc.wait(),3)
   except asyncio.TimeoutError:
    os.killpg(proc.pid,signal.SIGKILL);await proc.wait()
  shots=project/'tests/screenshots'
  if shots.exists():shutil.copytree(shots,OUT/'screenshots'/tc,dirs_exist_ok=True)
  row=dict(test=tc,status=state,seconds=round(time.monotonic()-started,1));results.append(row)
  (OUT/'results.json').write_text(json.dumps(results,indent=2));print(len(results),'/',len(tests),tc,state,flush=True)
async def main():
 print('STANDARD SUITE',len(tests),'tests; isolated stores and save directories',flush=True)
 await asyncio.gather(*(worker(i) for i in range(3)))
 print('DONE',sum(x['status']=='PASSED' for x in results),len(results),flush=True)
asyncio.run(main())
