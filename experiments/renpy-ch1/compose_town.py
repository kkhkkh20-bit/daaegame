"""Original bright village theme; normal builds use the committed audio.

FluidR3 licensed recorded GM instruments, not an external anime/game soundtrack.
32-bar ABA' form, C major, 116 BPM, 4/4, deliberately voiced consonant harmony.
Renderer helpers are existing project sample/mix utilities; no old tune reused.
"""
from pathlib import Path
import sys, json, hashlib, subprocess, tempfile
import numpy as np
from scipy.io import wavfile
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[1]/'preview/ch1-gpt-20261008/dev/wip-v2/gen'))
import music_context_v4 as audio
from music_piano_v2 import RATE, fold, room, loudness
# Existing renderer supports these seven lanes; instrument assignment is new.
audio.PROGRAMS={1:33,2:48,3:73,4:24,5:45,6:46,7:8}
INSTRUMENTS=['fingered bass','warm strings','flute melody','nylon guitar','pizzicato strings','harp','celesta']
BPM=116;BEAT=60/BPM
CHORDS={'C':(48,60,64,67),'G':(43,59,62,67),'Am':(45,60,64,69),'F':(41,60,65,69),'Dm':(38,62,65,69),'Em':(40,59,64,67)}
PROGRESSION=['C','G','Am','F','C','Dm','F','G','C','G','Am','F','Dm','G','C','G',
 'F','G','Em','Am','Dm','G','C','C','F','G','Am','F','Dm','G','C','G']
# Each bar is written as (beat, note, beat duration). Musical phrases resolve;
# dissonant random pitches and rigid per-chord triad climbing are avoided.
MELODY=[
 [(0,76,1),(1,79,.5),(1.5,76,.5),(2,74,.5),(2.5,72,1)],
 [(0,71,1),(1,74,1),(2,79,1.5)],
 [(0,76,.5),(.5,79,.5),(1,81,1),(2,79,.5),(2.5,76,1)],
 [(0,77,1.5),(1.5,76,.5),(2,74,1),(3,72,.75)],
 [(0,76,1),(1,79,1),(2,84,.75),(3,79,.75)],
 [(0,77,1),(1,74,.5),(1.5,72,.5),(2,74,1.5)],
 [(0,77,1),(1,81,.5),(1.5,79,.5),(2,77,1),(3,76,.75)],
 [(0,74,1.5),(1.5,71,.5),(2,72,.5),(2.5,74,1)],
 [(0,76,.75),(1,79,.75),(2,84,1.5)],
 [(0,83,1),(1,79,1),(2,74,1.5)],
 [(0,81,.5),(.5,79,.5),(1,76,1),(2,72,1.5)],
 [(0,77,1),(1,79,.5),(1.5,81,.5),(2,77,1.5)],
 [(0,77,.75),(1,74,.75),(2,69,1.5)],
 [(0,71,1),(1,74,1),(2,79,1)],
 [(0,76,1),(1,74,.5),(1.5,72,1.5)],
 [(1,71,.75),(2,74,.75),(3,79,.5)],
 [(0,81,1.5),(1.5,79,.5),(2,77,1.5)],
 [(0,79,1),(1,83,.5),(1.5,81,.5),(2,79,1.5)],
 [(0,79,.75),(1,76,.75),(2,71,1.5)],
 [(0,76,1),(1,79,.5),(1.5,81,.5),(2,84,1.5)],
 [(0,81,1),(1,77,1),(2,74,1.5)],
 [(0,79,1),(1,77,.5),(1.5,74,.5),(2,71,1)],
 [(0,76,.75),(1,79,.75),(2,84,1.5)],
 [(0,79,1),(1,76,.5),(1.5,74,.5),(2,72,1.5)],
 [(0,77,1),(1,81,1),(2,84,1.5)],
 [(0,83,1),(1,81,.5),(1.5,79,.5),(2,74,1.5)],
 [(0,81,1),(1,79,.5),(1.5,76,.5),(2,72,1.5)],
 [(0,77,1),(1,76,.5),(1.5,74,.5),(2,72,1.5)],
 [(0,74,1),(1,77,1),(2,81,1)],
 [(0,79,.75),(1,77,.75),(2,74,.75),(3,71,.75)],
 [(0,72,2.5)],
 [(1.5,67,.5),(2.5,71,.5),(3.5,74,.375)]
]
def main():
 events=[]
 def n(bar,off,lane,pitch,dur,v):
  events.append(((bar*4+off)*BEAT,lane,pitch,min(dur,4-off-.03)*BEAT,v))
 for bar,label in enumerate(PROGRESSION):
  bass,*tri=CHORDS[label];level=1 if bar>=16 else .88
  for off,p in [(0,bass),(2,bass+7)]:n(bar,off,1,p,.8,round(50*level))
  for pitch in tri:n(bar,0,2,pitch,3.8,25 if bar<16 else 29)
  for j,off in enumerate([0,.5,1,1.5,2,2.5,3,3.5]):
   n(bar,off,4,tri[[0,1,2,1,0,1,2,1][j]],.37,38 if j%2==0 else 30)
  for off in [1,3]:
   for p in tri[:2]:n(bar,off,5,p,.25,32)
  for off,p,dur in MELODY[bar]:
   n(bar,off,3,p,dur*.93,57 if bar<16 else 62)
   if bar>=24:n(bar,off,7,p,dur*.75,26)
  if bar%4==3:
   for j,p in enumerate(tri):n(bar,2.5+j*.5,6,p+12,.35,26)
 frames=round(32*4*BEAT*RATE)
 mix=fold(audio.orchestra(sorted(events),frames+6*RATE),frames)
 mix=room(mix,.10,.7,173)
 out=ROOT/'audio';out.mkdir(exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  raw=Path(td)/'town.wav';wavfile.write(raw,RATE,mix.astype(np.float32));m=loudness(raw)
  gain=min(-20-float(m['input_i']),-3-float(m['input_tp']));mix*=10**(gain/20)
  wavfile.write(raw,RATE,mix.astype(np.float32))
  dest=out/'town-bright.mp3';subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-c:a','libmp3lame','-b:a','192k','-metadata','title=Lanterns on the road — original village theme',str(dest)],check=True)
 result=dict(title='길가에 켜진 등',original=True,bpm=BPM,tonic='C major',meter='4/4',bars=32,seconds=frames/RATE,instruments=INSTRUMENTS,chords=PROGRESSION,melody=MELODY,loudness=loudness(dest),loop_boundary_jump=float(np.max(abs(mix[0]-mix[-1]))),sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
 (out/'town-score.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 (out/'town-credits.txt').write_text('Original composition and arrangement for daaegame, 2026-10-11.\nBright animation-style village theme; no external soundtrack or transcribed melody.\nRecorded GM instruments: FluidR3_GM. Copyright 2000-2002, 2008 Frank Wen; 2008 Toby Smithe. MIT license.\nFull license included in game/assets/sample-license.txt.\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('melody','chords')},ensure_ascii=False))
if __name__=='__main__':main()
