import json,subprocess,hashlib,statistics
import numpy as np
from pathlib import Path
p=Path('/workspace/trail-perf-baseline');summary={}
for case in ('no-capture','capture'):
 x=json.loads((p/(case+'.json')).read_text());r=x['trace'];groups={}
 for arrival in ('buri','seryeon'):
  tr=[v for v in r if v['kind']=='transition' and v['arrival']==arrival and v['st']<.8]
  active=[v for v in tr if v['st']<.34]
  groups[arrival]={'local_times':[round(v['st'],4) for v in tr],'active_calls':len(active),'first_gap_ms':round((tr[1]['t']-tr[0]['t'])*1000,2),'timeline_start':tr[0]['t']-x['anchor']-tr[0]['st']}
 roots=[v for v in r if v['kind']=='root' and (1.9<v['st']<2.8 or 5.4<v['st']<6.3)]
 primary=[v for v in r if v['kind']=='layer' and 'background' in v['components']]
 d=np.diff(x['raf']);summary[case]={'transitions':groups,'root_render_ms_max':max(v['ms'] for v in roots),'root_ids_during_transitions':len(set(v['id'] for v in roots)),'primary_views':[{'local_time':v['st'],'view':v['view']} for v in primary],'raf_median_ms':float(np.median(d)),'raf_max_ms':float(max(d))}
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v','-show_entries','frame=best_effort_timestamp_time','-of','json',str(p/'capture.mp4')]))
ts=[float(f['best_effort_timestamp_time']) for f in meta['frames']]
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p/'capture.mp4'),'-vf','crop=1280:500:0:60,scale=160:64,format=gray','-vsync','0','-f','rawvideo','-'])
f=np.frombuffer(raw,dtype=np.uint8).reshape(-1,64,160);assert len(f)==len(ts),(len(f),len(ts))
hashes=[hashlib.sha256(v.tobytes()).hexdigest() for v in f]
mae=np.r_[0,np.abs(np.diff(f.astype(float),axis=0)).mean(axis=(1,2))]
static=[mae[i] for i,t in enumerate(ts) if 3.0<t<4.0];threshold=max(.5,float(np.percentile(static,99))*2)
video={'frame_count':len(f),'distinct_exact_frames':len(set(hashes)),'exact_adjacent_duplicates':sum(a==b for a,b in zip(hashes,hashes[1:])),'static_noise_mae_99':float(np.percentile(static,99)),'movement_mae_threshold':threshold,'windows':{}}
for arrival,g in summary['capture']['transitions'].items():
 start=g['timeline_start'];indices=[i for i,t in enumerate(ts) if start-.1<=t<=start+.55]
 video['windows'][arrival]={'window':[start-.1,start+.55],'frames':[{'index':i,'pts':ts[i],'mae_from_previous':float(mae[i]),'hash':hashes[i]} for i in indices],'significant_changes':int(sum(mae[i]>threshold for i in indices))}
summary['mp4']=video;(p/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
