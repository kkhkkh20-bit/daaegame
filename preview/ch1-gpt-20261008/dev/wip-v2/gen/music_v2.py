"""Original chapter-one leitmotif, rendered with the installed TimGM6mb instruments.

Rebuild: python3 gen/music_v2.py (NumPy, libfluidsynth, TimGM6mb, ffmpeg).
The score below is the editable source; rendered assets keep separate credits.
"""
from pathlib import Path
import ctypes as C
import json
import subprocess
import tempfile
import wave
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'audio/v2'
OUT.mkdir(parents=True, exist_ok=True)
RATE = 44100
SF = '/usr/share/sounds/sf2/TimGM6mb.sf2'
F = C.CDLL('libfluidsynth.so.3')
def bind(name, restype, args):
    f = getattr(F, name); f.restype = restype; f.argtypes = args; return f
ptr, integer, dbl = C.c_void_p, C.c_int, C.c_double
settings = bind('new_fluid_settings', ptr, [])()
bind('fluid_settings_setnum', integer, [ptr, C.c_char_p, dbl])(settings,b'synth.sample-rate',RATE)
bind('fluid_settings_setnum', integer, [ptr, C.c_char_p, dbl])(settings,b'synth.gain',.55)
new_synth = bind('new_fluid_synth', ptr, [ptr])
load = bind('fluid_synth_sfload', integer, [ptr,C.c_char_p,integer])
program = bind('fluid_synth_program_change',integer,[ptr,integer,integer])
control = bind('fluid_synth_cc',integer,[ptr,integer,integer,integer])
on = bind('fluid_synth_noteon',integer,[ptr,integer,integer,integer])
off = bind('fluid_synth_noteoff',integer,[ptr,integer,integer])
write = bind('fluid_synth_write_float',integer,[ptr,integer,ptr,integer,integer,ptr,integer,integer])
delete = bind('delete_fluid_synth',None,[ptr])

# A minor, borrowed F-major colour, suspended dominant: a warm place with an
# unanswered question. One motif recurs without a constant high-register loop.
CHORDS = [[45,52,60,71],[41,48,57,64],[48,55,59,64],[43,50,57,62],
          [45,52,60,64],[38,45,53,64],[41,48,57,64],[40,47,56,62]]
MOTIFS = [[69,76,74,72],[69,72,76],[67,71,72,76],[74,72,71],
          [69,72,76,79],[77,76,74],[72,69,67,64],[71,68,69]]

def score(kind, bpm):
    events=[]
    def note(ch,n,t,d,v):
        events.extend([(t,1,ch,n,v),(t+d,0,ch,n,0)])
    for bar in range(24):
        chord=CHORDS[bar%8]; base=bar*4
        section=bar//8
        # Widely spaced piano with a breath between phrases.
        for j,n in enumerate(chord[1:]):
            note(0,n,base+j*.45,2.8-j*.3,43+(bar%3)*3)
        if kind=='investigation':
            for j in range(8):
                note(2,chord[j%2],base+j*.5,.24,43 if j%2==0 else 30)
            if bar%2==0:
                for j,n in enumerate(chord[2:]): note(3,n+12,base+2+j*.5,.32,34)
        else:
            note(2,chord[0],base,3.6,39)
            if kind=='travel':
                for j,n in enumerate([chord[1],chord[2],chord[3],chord[2]]):
                    note(3,n,base+j*.85,.65,34)
        # Strings arrive after the first phrase; never a heavy sustained drone.
        if section and bar%2==0:
            for n in chord[1:3]: note(4,n,base,7.2,24 if kind=='investigation' else 29)
        if bar%8 in [3,7] and section==0: continue
        motif=MOTIFS[bar%8]
        for j,n in enumerate(motif):
            t=base+.55+j*.85
            if kind=='investigation':
                if bar%2: continue
                note(0,n-12,t,.55,48)
            else:
                channel=1 if section==1 else 0
                note(channel,n+(12 if section==2 and bar%8==4 else 0),t,.68 if j<len(motif)-1 else 1.5,53+(section==1)*5)
    return sorted(events),24*4*60/bpm

metadata=[]
for kind,bpm,title in [('title',70,'첫눈에 남긴 질문'),('travel',84,'숲길의 두 사람'),('investigation',96,'남아 있는 흔적')]:
    synth=new_synth(settings);assert load(synth,SF.encode(),1)>=0
    for ch,prg in enumerate([0,71,42,24,48]):
        program(synth,ch,prg);control(synth,ch,10,[52,78,64,44,64][ch]);control(synth,ch,91,48)
    events,duration=score(kind,bpm); events=[(round(t*60/bpm*RATE),typ,ch,n,v) for t,typ,ch,n,v in events]
    count=round((duration+4)*RATE); result=np.zeros((count,2),np.float32);cursor=0
    for position,typ,ch,n,v in events+[(count,2,0,0,0)]:
        while cursor<position:
            size=min(4096,position-cursor);l=np.empty(size,np.float32);r=np.empty(size,np.float32)
            write(synth,size,l.ctypes.data,0,1,r.ctypes.data,0,1)
            result[cursor:cursor+size,0]=l;result[cursor:cursor+size,1]=r;cursor+=size
        if typ==1:on(synth,ch,n,v)
        elif typ==0:off(synth,ch,n)
    delete(synth)
    # Bake the previous loop's release tail into its beginning. A small fade
    # prevents an initial click while allowing the full phrase to loop cleanly.
    loop=round(duration*RATE);tail=result[loop:];result=result[:loop]
    result[:len(tail)]+=tail
    result[:2205]*=np.linspace(0,1,2205)[:,None]
    result[-441:]*=np.linspace(1,0,441)[:,None]
    result*=.65/max(.001,float(np.max(np.abs(result))))
    with tempfile.NamedTemporaryFile(suffix='.wav') as temp:
        with wave.open(temp.name,'wb') as w:
            w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes((result*32767).astype('<i2').tobytes())
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',temp.name,'-codec:a','libmp3lame','-b:a','160k',str(OUT/f'{kind}-v1.mp3')],check=True)
    metadata.append({'key':kind,'title':title,'bpm':bpm,'bars':24,'seconds':duration,'peak':float(np.max(np.abs(result))),'rms':float(np.sqrt(np.mean(result**2)))})
    print(metadata[-1],flush=True)
(OUT/'score.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
(OUT/'CREDITS.txt').write_text('These credits apply only to title-v1.mp3, travel-v1.mp3 and investigation-v1.mp3.\nFor the newer *-piano-v2.mp3 files, see PIANO_CREDITS.txt and the accompanying licenses.\n\nOriginal score: daaegame chapter-one v2, 2026-10-10.\nEditable score: dev/wip-v2/gen/music_v2.py\nInstruments: TimGM6mb (Tim Brechbill, David Bolton), GPL-2.\nSoundFont source: https://github.com/musescore/musescore-old/commit/90c33ef9d87b3f5ff92efd3b07d89eb455fb1fef\nThese rendered audio assets are provided under GPL-2; game/art licenses are separate.\n')
(OUT/'GPL-2.txt').write_bytes(Path('/usr/share/common-licenses/GPL-2').read_bytes())
