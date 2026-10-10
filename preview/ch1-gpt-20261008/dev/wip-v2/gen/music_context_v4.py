"""Four original, piano-free context cues with distinct themes and 4/4 scores.

Uses existing FluidR3_GM samples and periodic offline mixing helpers. No game OST
is downloaded or transcribed. Normal builds consume committed MP3s/manifest.
"""
from pathlib import Path
import ctypes as C
import hashlib
import json
import subprocess
import tempfile
import numpy as np
from scipy import signal
from scipy.io import wavfile
from music_piano_v2 import RATE, SF, fold, room, periodic_filter, loudness

SOURCE=Path(__file__).resolve().parents[1]
OUT=SOURCE.parents[1]/'audio/v4'
PROGRAMS={1:42,2:48,3:73,4:71,5:45,6:46,7:70}
INSTRUMENTS={1:'cello',2:'string ensemble',3:'flute',4:'clarinet',5:'pizzicato strings',6:'harp',7:'bassoon'}
TRIADS={'Dm':[50,53,57],'Bb':[46,50,53],'F':[53,57,60],'C':[48,52,55],
        'Gm':[43,46,50],'Am':[45,48,52],'A':[45,49,52],
        'G':[43,47,50],'D':[50,54,57],'Em':[40,43,47]}
TRACKS={
 'investigation':{'key':'inn_inv','bpm':88,'tonic':'D minor','bars':16,'form':['A']*8+['B']*8,
  'chords':['Dm','Bb','Dm','Am','F','C','Gm','Am','Gm','C','F','Bb','Dm','Gm','Am','Dm'],'target':-24},
 'serious':{'key':'inn_serious','bpm':56,'tonic':'D minor','bars':16,'form':['A']*8+['B']*8,
  'chords':['Dm','Dm','Gm','Gm','Bb','Bb','Dm','Dm','F','F','Gm','Gm','Am','Am','Dm','Dm'],'target':-24.6},
 'comic':{'key':'inn_comic','bpm':100,'tonic':'G major','bars':16,'form':['A']*8+['B']*8,
  'chords':['G','D','C','G','Em','C','Am','D','C','G','Am','D','Em','C','D','G'],'target':-24.6},
 'friend':{'key':'inn_friend','bpm':76,'tonic':'F major','bars':24,'form':['A']*8+['B']*8+['A2']*8,
  'chords':['F','Bb','C','F','Dm','Gm','C','F','Bb','F','Gm','C','Dm','Bb','C','C','F','Bb','C','F','Dm','Gm','C','F'],'target':-24}
}

def score(name):
    t=TRACKS[name];beat=60/t['bpm'];events=[]
    def n(bar,off,lane,pitch,dur,velocity):
        assert lane in PROGRAMS and lane!=0
        # All starts on the eighth-note grid; every note ends inside its bar.
        dur=min(dur,4-off-.125)
        assert dur>0
        events.append(((4*bar+off)*beat,lane,pitch,dur*beat,velocity))
    for bar,label in enumerate(t['chords']):
        ch=TRIADS[label];section=t['form'][bar];b=bar%8
        if name=='investigation':
            # Four quiet observations per bar. The bass pulse never becomes drums.
            for j,off in enumerate((0,1,2,3)):
                n(bar,off,5,ch[(0,2,1,2)[j]],.5,29 if j==0 else 23)
            if section=='A':
                phrase=[(.5,2,.5),(1.5,1,.5),(2.5,0,1)] if b%2==0 else [(1,1,.5),(2,2,1)]
                lane=4
            else:
                phrase=[(0,0,.5),(1,2,.5),(2.5,1,1)] if b%2==0 else [(.5,2,.5),(1.5,1,1.5)]
                lane=7 if b in (1,3,5,7) else 4
            for off,i,d in phrase:n(bar,off,lane,ch[i]+12,d,32 if lane==4 else 29)
            if b in (0,4):n(bar,0,1,ch[0]-12,3.5,23)
        elif name=='serious':
            # Cello statements are separated by whole bars of breath. No ostinato.
            n(bar,0,1,ch[0]-12,3.75,29 if b%2==0 else 20)
            if b%2==0:
                i=(0,1,2,1)[b//2] if section=='A' else (2,1,0,1)[b//2]
                n(bar,.5 if section=='A' else 1,1,ch[i],2.5,32)
            if b in (1,5):n(bar,2,6,ch[2]+12,1.5,20)
            if section=='B' and b in (0,4):n(bar,0,2,ch[1],3.5,16)
        elif name=='comic':
            # A tiny question, a pause, then a lower reply. Alternating bars rest.
            n(bar,0,5,ch[0],.5,28)
            if b%2==0:
                n(bar,1.5,5,ch[2],.5,23)
                phrase=[(.5,2,.5),(1,1,.5),(2.5,0,.5)] if section=='A' else [(0,0,.5),(.5,2,.5),(2,1,.5)]
                for off,i,d in phrase:n(bar,off,4 if section=='A' else 3,ch[i]+12,d,30)
            else:
                n(bar,2,7,ch[1],.5,30)
                if b in (3,7):n(bar,2.5,7,ch[0],.5,25)
        else:
            # Eight-bar flute greeting, a higher answering phrase, and a quiet return.
            n(bar,0,1,ch[0]-12,3.5,22)
            if bar%2==0:
                for pitch in ch[:2]:n(bar,0,2,pitch,3.5,17)
            for off,i in ((0,0),(1.5,1),(3,2)):n(bar,off,6,ch[i]+12,.75,23)
            if section=='A':phrase=[(0,0,1.5),(2,1,.75),(3,2,.75)]
            elif section=='B':phrase=[(.5,2,1),(2,1,1.5)] if b%2==0 else [(0,1,.75),(1,2,.75),(2.5,0,1)]
            else:phrase=[(0,2,1.5),(2,1,.75),(3,0,.75)]
            if b in (3,7):phrase=phrase[:1]  # leave room at the end of each sentence
            for off,i,d in phrase:n(bar,off,3,ch[i]+12,d,31 if section=='B' else 29)
    return sorted(events),round(t['bars']*4*beat*RATE)/RATE

def orchestra(events,frames):
    """Own GM program map; channel/lane zero is never played or configured."""
    lib=C.CDLL('libfluidsynth.so.3');ptr=C.c_void_p;integer=C.c_int
    def bind(name,restype,args):
        fn=getattr(lib,name);fn.restype=restype;fn.argtypes=args;return fn
    settings=bind('new_fluid_settings',ptr,[])()
    sn=bind('fluid_settings_setnum',integer,[ptr,C.c_char_p,C.c_double]);si=bind('fluid_settings_setint',integer,[ptr,C.c_char_p,integer])
    sn(settings,b'synth.sample-rate',RATE);sn(settings,b'synth.gain',.34)
    si(settings,b'synth.reverb.active',0);si(settings,b'synth.chorus.active',0)
    synth=bind('new_fluid_synth',ptr,[ptr])(settings)
    assert bind('fluid_synth_sfload',integer,[ptr,C.c_char_p,integer])(synth,str(SF).encode(),1)>=0
    pg=bind('fluid_synth_program_change',integer,[ptr,integer,integer]);cc=bind('fluid_synth_cc',integer,[ptr,integer,integer,integer])
    for lane,program in PROGRAMS.items():pg(synth,lane,program);cc(synth,lane,10,{1:55,2:71,3:67,4:58,5:43,6:80,7:62}[lane])
    on=bind('fluid_synth_noteon',integer,[ptr,integer,integer,integer]);off=bind('fluid_synth_noteoff',integer,[ptr,integer,integer]);write=bind('fluid_synth_write_float',integer,[ptr,integer,ptr,integer,integer,ptr,integer,integer])
    timeline=[]
    for at,lane,n,d,v in events:timeline.extend([(round(at*RATE),1,lane,n,v),(round((at+d)*RATE),0,lane,n,0)])
    out=np.zeros((frames,2),np.float32);cursor=0
    for position,typ,ch,n,v in sorted(timeline)+[(frames,2,0,0,0)]:
        position=min(position,frames)
        while cursor<position:
            size=min(4096,position-cursor);left=np.empty(size,np.float32);right=np.empty(size,np.float32)
            write(synth,size,left.ctypes.data,0,1,right.ctypes.data,0,1)
            out[cursor:cursor+size,0]=left;out[cursor:cursor+size,1]=right;cursor+=size
        if typ==1:on(synth,ch,n,v)
        elif typ==0:off(synth,ch,n)
    bind('delete_fluid_synth',None,[ptr])(synth);bind('delete_fluid_settings',None,[ptr])(settings)
    return out

def render(name):
    t=TRACKS[name];events,seconds=score(name);frames=round(seconds*RATE)
    print('Rendering',name,t['tonic'],t['bpm'],'BPM',len(events),'notes',flush=True)
    mix=fold(orchestra(events,frames+6*RATE),frames)
    mix=periodic_filter(mix,signal.butter(2,55,fs=RATE,btype='highpass',output='sos'))
    mix=periodic_filter(mix,signal.butter(2,6200,fs=RATE,output='sos'))
    mix=room(mix,.11 if name=='comic' else .17,1.1,151)
    assert np.isfinite(mix).all()
    with tempfile.TemporaryDirectory() as td:
        raw=Path(td)/'context.wav';wavfile.write(raw,RATE,mix.astype(np.float32));initial=loudness(raw)
        gain=min(t['target']-float(initial['input_i']),-4.5-float(initial['input_tp']))
        mix*=10**(gain/20);wavfile.write(raw,RATE,mix.astype(np.float32))
        path=OUT/f'{name}-context-v4.mp3'
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-codec:a','libmp3lame','-b:a','192k','-metadata',f'title=daaegame {name} original context v4',str(path)],check=True)
        measured=loudness(path)
    lanes=sorted({x[1] for x in events})
    return dict(name=name,key=t['key'],bpm=t['bpm'],tonic=t['tonic'],bars=t['bars'],beatsPerBar=4,gridSubdivision=2,gridOnly=True,
                form=t['form'],chords=t['chords'],triads=TRIADS,seconds=seconds,file=path.name,
                instruments=[INSTRUMENTS[x] for x in lanes],programs={x:PROGRAMS[x] for x in lanes},
                notes=[dict(at=round(at,6),lane=l,midi=n,duration=round(d,6),velocity=v) for at,l,n,d,v in events],
                integrated_lufs=float(measured['input_i']),true_peak_db=float(measured['input_tp']),
                loop_boundary_jump=float(np.max(abs(mix[0]-mix[-1]))),sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def main():
    assert SF.is_file();OUT.mkdir(parents=True,exist_ok=True)
    rows=[render(name) for name in TRACKS]
    (OUT/'score-context-v4.json').write_text(json.dumps(rows,indent=2)+'\n')
    path=SOURCE/'inn_music_tracks.js';mapping=json.JSONDecoder().raw_decode(path.read_text().split('window.__INN_MUSIC=',1)[1])[0]
    for row in rows:mapping[row['key']]={'bpm':row['bpm'],'vol':.8,'prog':row['chords'],'mel':[],'media':'audio/v4/'+row['file'],'loopSeconds':row['seconds']}
    aliases={'inn_cold':'inn_serious','inn_t_seryeon':'inn_serious','inn_t_nabi':'inn_friend','inn_t_karo':'inn_friend','inn_t_bami':'inn_comic','inn_t_doto':'inn_inv','inn_t_buri':'inn_friend','inn_t_neoul':'inn_serious','inn_t_innma':'inn_friend'}
    for alias,key in aliases.items():mapping[alias]=mapping[key].copy()
    path.write_text('/* Original piano-free v4 context cues; other v3 score retained. */\nwindow.__INN_MUSIC='+json.dumps(mapping,separators=(',',':'))+';\n')
    (OUT/'CREDITS.txt').write_text('Original daaegame chapter-one context score (2026-10-10).\nComposition, arrangement, mix and rendering: project original score.\nCello, strings, pizzicato, flute, clarinet, bassoon and harp: FluidR3_GM.\nCopyright 2000-2002, 2008 Frank Wen; 2008 Toby Smithe. MIT license.\nFull instrument license retained at ../v2/FLUIDR3-LICENSE.txt.\nNo piano instruments, external game music samples or transcribed melodies used.\nDesign reference: Capcom, The Adventures and Resolve of Music Creation (game function and immediately recognisable character themes).\nhttps://news.capcomusa.com/lets/browse/the-adventures-and-resolve-of-music-creation\nStructural reference: Danganronpa official OST distinguishes daily/search/debate contexts; no original track downloaded or inserted.\n')
if __name__=='__main__':main()
