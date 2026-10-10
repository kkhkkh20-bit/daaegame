"""Audit encoded music for clipping, loudness, stereo and playable loop boundaries.

Signal checks do not establish artistic quality or replace listening on devices.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import numpy as np

SOURCE=Path(__file__).resolve().parent
OUT=SOURCE.parent.parent/'audio/v2'
tracks=json.loads((OUT/'score-piano-v2.json').read_text())
assert len(tracks)==16,len(tracks)
total=0
for track in tracks:
    path=OUT/track['file'];total+=path.stat().st_size
    assert hashlib.sha256(path.read_bytes()).hexdigest()==track['sha256'],path
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','f32le','-ar','44100','-ac','2','pipe:1'])
    pcm=np.frombuffer(raw,np.float32).reshape(-1,2)
    assert np.isfinite(pcm).all() and np.max(np.abs(pcm))<.9,path
    assert float(np.sqrt(np.mean(pcm*pcm)))>.015,path
    assert abs(len(pcm)/44100-track['seconds'])<.01,(path,len(pcm)/44100,track['seconds'])
    assert float(np.sqrt(np.mean((pcm[:,0]-pcm[:,1])**2)))>.001,path
    boundary=min(len(pcm),round(track['seconds']*44100))-1
    jump=float(np.max(np.abs(pcm[0]-pcm[boundary])))
    assert jump<.012,(path,'loop boundary',jump)
    result=subprocess.run(['ffmpeg','-v','info','-i',str(path),'-af','loudnorm=print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    measured=json.JSONDecoder().raw_decode(result.stderr[result.stderr.rfind('{'):].lstrip())[0]
    assert float(measured['input_tp'])<=-1.5,(path,measured)
    assert -26<float(measured['input_i'])<-16,(path,measured)
    print(track['name'],'OK',{'seconds':round(track['seconds'],2),'lufs':measured['input_i'],'true_peak':measured['input_tp'],'edge':round(jump,6)},flush=True)
print('16 encoded stereo scores OK; size',round(total/1024**2,2),'MiB',flush=True)
