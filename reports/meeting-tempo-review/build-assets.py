from pathlib import Path
import subprocess,json,hashlib
root=Path('/workspace/daaegame-reactions/experiments/renpy-ch1');rows=[]
for name in ['council','pressure']:
 src=root/'game/assets'/('bgm-'+name+'.mp3')
 for stage,rate in [(1,1.06),(2,1.12)]:
  out=root/'game/assets'/('bgm-'+name+'-tempo'+str(stage)+'.ogg')
  subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-af',f'rubberband=tempo={rate}:pitch=1','-c:a','libvorbis','-q:a','4',str(out)],check=True)
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(out)]))
  rows.append(dict(file=str(out.relative_to(root)),source=str(src.relative_to(root)),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),stage=stage,tempo_ratio=rate,pitch_ratio=1,duration=duration))
(root/'game/assets/meeting-tempo-derivatives.json').write_text(json.dumps(rows,indent=2)+'\n')
print(rows)
