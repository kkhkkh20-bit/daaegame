"""Original piano/orchestral chapter score, recorded instruments and offline mix.

Prepare: python3 gen/fetch_piano_samples.py
Render:  python3 gen/music_piano_v2.py [--only title,investigation]
Requires NumPy, SciPy, ffmpeg and libfluidsynth. Libraries stay outside Git.
The saved MP3s and inn_piano_tracks.js suffice for normal build/publish.
"""
from pathlib import Path
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import argparse
import ctypes as C
import hashlib
import json
import math
import re
import subprocess
import tempfile
import numpy as np
from scipy import signal
from scipy.io import wavfile
from fetch_piano_samples import CACHE, REV, CENTERS, LAYERS, filename

SOURCE = Path(__file__).resolve().parents[1]
OUT = SOURCE.parent.parent/'audio/v2'
RATE = 44100
SF = CACHE/'fluid/usr/share/sounds/sf2/FluidR3_GM.sf2'

# A recognisable question: D–A–Bb–E. The semitone gives it unease; the answer
# descends F–E–D. Bb/F bring warmth; Ebmaj7(#11) and A(b9) keep a mystery open.
HARMONY = [[38,45,53,60,64], [34,41,53,57,62], [33,41,53,60,64], [40,48,55,62,67],
           [43,50,58,65,69], [39,46,55,62,69], [33,40,55,58,62], [33,40,55,58,61]]
BRIDGE = [HARMONY[1],HARMONY[0],HARMONY[4],HARMONY[2],
          [40,46,55,62,67],HARMONY[7],[41,48,57,62,69],HARMONY[7]]
PHRASE = [[(.65,74,.70),(1.5,69,.45),(2.15,70,.60),(3.05,76,.75)],
          [(.35,77,.70),(1.25,76,.55),(2.05,74,1.50)],
          [(.55,72,.60),(1.45,69,.60),(2.4,65,1.1)],
          [(.3,67,.70),(1.25,72,.75),(2.5,76,1.1)],
          [(.45,74,.75),(1.4,77,.70),(2.45,81,1.15)],
          [(.2,79,.65),(1.0,77,.55),(2.0,75,.70),(3.05,74,.65)],
          [(.5,70,1.0),(2.1,69,1.35)],[(.6,73,.9),(2.0,76,1.35)]]
BPHRASE = [[(.4,74,.7),(1.35,77,.7),(2.4,81,1.0),(3.5,79,.4)],
           [(.3,81,.6),(1.1,77,.6),(2.0,76,.6),(3.0,74,.7)],
           [(.4,82,.7),(1.35,81,.6),(2.2,79,.65),(3.15,74,.7)],
           [(.45,81,.8),(1.6,79,.55),(2.45,76,.65),(3.25,72,.6)],
           [(.25,79,.7),(1.15,82,.65),(2.1,81,.6),(3.05,79,.7)],
           [(.3,85,.7),(1.25,82,.6),(2.1,81,.6),(3.05,76,.7)],
           [(.4,77,.65),(1.3,76,.65),(2.25,74,.7),(3.25,69,.55)],PHRASE[7]]

@dataclass(frozen=True)
class Track:
    key: str
    title: str
    bpm: int
    bars: int
    style: str
    loudness: float
    volume: float = .9

TRACKS = {
 'title':Track('inn_title','열세 번째 침대 · 남겨진 질문',76,32,'title',-18),
 'travel':Track('inn_travel','셋이 읽던 책',84,24,'travel',-20),
 'investigation':Track('inn_inv','여백 속의 흔적',92,24,'investigation',-20),
 'serious':Track('inn_serious','베개 구석의 빈자리',68,16,'serious',-21),
 'meeting':Track('inn_meet','닫힌 원탁',96,24,'meeting',-19),
 'meeting-press':Track('inn_meet_press','흔들리는 다수',112,24,'press',-18),
 'climax':Track('inn_climax','거짓말의 균열',112,24,'climax',-18),
 'climax-press':Track('inn_climax_press','이제 대답해 주세요',126,24,'climax-press',-17.5),
 'after':Track('inn_after','다시 펼칠 책',72,24,'after',-21),
 'grandma':Track('inn_t_innma','이름 없는 손님의 집',72,16,'grandma',-21,.8),
 'seryeon':Track('inn_t_seryeon','공손한 빈칸',80,16,'seryeon',-21,.8),
 'nabi':Track('inn_t_nabi','수건 한 장의 온기',92,16,'nabi',-21,.8),
 'bami':Track('inn_t_bami','천장에서 본 세상',84,16,'bami',-21,.8),
 'doto':Track('inn_t_doto','못 본 것은 빈칸',96,16,'doto',-21,.8),
 'buri':Track('inn_t_buri','닫히지 않는 문',88,16,'buri',-21,.8),
 'neoul':Track('inn_t_neoul','같은 규칙으로',100,16,'neoul',-21,.8),
}

def make_score(track, name):
    rng = np.random.default_rng(int(hashlib.sha256(name.encode()).hexdigest()[:8],16))
    events=[];style=track.style
    action=style in ('press','climax','climax-press')
    quiet=style in ('after','grandma','serious','bami','seryeon')
    levels=([.42,.68,1,.48] if style=='title' else
            [.75,1,.82] if action else [.28,.48,.32] if quiet else [.45,.68,.5])
    tempos=[]
    def note(lane,n,t,d,v):
        # Consistent, repeatable performance: small timing/velocity movement.
        events.append((max(0,t+float(rng.normal(0,.009))),lane,int(n),d,int(np.clip(v+rng.normal(0,2.1),16,110))))
    for bar in range(track.bars):
        block=bar//8;idx=bar%8;base=bar*4
        level=levels[min(block,len(levels)-1)]
        bridge=block==(2 if track.bars==32 else 1) and track.bars>=24
        chord=(BRIDGE if bridge else HARMONY)[idx]
        if style=='nabi':chord=[HARMONY[2],HARMONY[1],HARMONY[3],HARMONY[0],HARMONY[2],HARMONY[4],HARMONY[6],HARMONY[7]][idx]
        # No time stretching: pressure versions are played at their own tempo.
        breathing=1+.018*math.sin((bar%8)*math.pi/4) if style in ('title','travel','after','grandma') else 1
        tempos.append(track.bpm*breathing)
        note(0,chord[0],base,2.15 if quiet else 1.7,40+level*14)
        if action:
            offsets=[.5,.75,1.5,2,2.5,3,3.5]
            for j,off in enumerate(offsets):note(0,chord[1+j%3],base+off,.36,45+level*15+(4 if j%3==0 else 0))
        elif style in ('investigation','meeting','doto','neoul','buri'):
            offsets=([.75,1.5,2.25,3.25] if style in ('investigation','doto') else [.5,1.25,2,2.75,3.5])
            for j,off in enumerate(offsets):note(0,chord[1+j%3],base+off,.48,37+level*12)
        else:
            for j,off in enumerate([1.1,2.05,2.95]):
                if quiet and idx%2 and j==2:continue
                note(0,chord[1+j%3],base+off,1.3 if quiet else 1.55,34+level*13)
        phrase=(BPHRASE if bridge else PHRASE)[idx]
        if style=='serious':phrase=[(.75,chord[-1]+12,1.4)] if bar%2==0 else []
        if style=='seryeon':phrase=PHRASE[(idx+5)%8] if bar%2==0 else []
        if style=='bami':phrase=[(.6,phrase[0][1]+12,1.25),(2.8,phrase[-1][1],.7)] if bar%2==0 else []
        if style in ('investigation','doto','buri') and bar%2:phrase=[]
        if style in ('after','grandma'):phrase=[(t,n-12,d*1.15) for t,n,d in phrase[:2]]
        for j,(off,n,dur) in enumerate(phrase):
            note(0,n,base+off,dur+(0.2 if quiet else 0),53+level*22+(3 if j==0 else -j))
        # Upper-note doubling is reserved for the developed theme and reversals.
        if (style=='title' and block==2) or (action and idx in (0,4)):
            for off,n,dur in phrase[:2]:
                if n+12<=87:note(0,n+12,base+off+.018,dur*.85,48+level*12)
        if style in ('climax','climax-press') and idx in (1,3,5):
            for j in range(4):note(0,chord[2+j%3]+12,base+2.125+j*.375,.24,60+level*12)
        # Recorded cello is a counterweight, not a continuous sub-bass drone.
        orchestra=style not in ('bami','doto','seryeon') and not(style=='title' and block==0 and idx<4)
        if orchestra and bar%2==0:note(1,chord[0]+12,base+.15,3.45,25+level*17)
        if orchestra and (block or style in ('meeting','press','climax','climax-press','serious','neoul')):
            for j,n in enumerate(chord[2:4]):note(2,n+12,base+.1+j*.025,3.6,19+level*16)
        if (style=='title' and block==2) or (action and idx in (0,4)):
            note(3,chord[2],base+.2,2.45,25+level*18)
        if style in ('travel','nabi') and idx in (1,5):note(4,chord[3]+12,base+3.1,.8,28)
        if style in ('investigation','doto','buri'):
            for j in range(2):note(5,chord[j+1],base+j*2+.05,.45,24+level*8)
        if style=='bami' and idx in (3,7):note(4,chord[3]+24,base+3,.8,22)
        if (style=='title' and block==2 and idx in (0,4)) or (action and idx in (0,4)):
            note(7,chord[0]+12,base,.45,35+level*12)
    seconds_per_bar=240/np.array(tempos)
    boundary=np.concatenate([[0],np.cumsum(seconds_per_bar)])
    def when(beat):
        i=min(int(beat//4),track.bars-1)
        return float(boundary[i]+(beat-i*4)*60/tempos[i])
    return sorted([(when(t),lane,n,when(t+d)-when(t),v) for t,lane,n,d,v in events]),float(boundary[-1])

def read_defines(path,prefix):
    return {int(k):float(v) for k,v in re.findall(r'#define \$'+prefix+r'(\d+)\s+(-?[\d.]+)',path.read_text())}

TUNING=read_defines(CACHE/'salamander/Data/tune_ret.txt','TUNE') if (CACHE/'salamander/Data/tune_ret.txt').exists() else {}
OFFSETS={v:read_defines(CACHE/f'salamander/Data/vel_{v:02d}.txt','OFF') for v in LAYERS} if TUNING else {}

@lru_cache(maxsize=32)
def recorded(center,layer):
    p=CACHE/'salamander/Samples'/filename(center,layer)
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-t','9','-ar',str(RATE),'-ac','2','-f','f32le','pipe:1'])
    a=np.frombuffer(raw,np.float32).reshape(-1,2).copy()
    index=(center-21)//3+1
    offset=max(0,int(OFFSETS[layer][index]*RATE/48000)-80)
    return a[offset:]

@lru_cache(maxsize=96)
def pitched(n,layer):
    center=min(CENTERS,key=lambda c:abs(c-n))
    assert abs(center-n)<=1,(center,n)
    index=(center-21)//3+1
    rate=Fraction(2**(-(n-center+TUNING[index]/100)/12)).limit_denominator(512)
    a=signal.resample_poly(recorded(center,layer),rate.numerator,rate.denominator,axis=0).astype(np.float32)
    a[:90]*=np.linspace(0,1,90,dtype=np.float32)[:,None]
    return a

def piano(events,frames):
    out=np.zeros((frames,2),np.float32)
    for at,lane,n,hold,vel in events:
        if lane:continue
        # Blend soft/medium/firm recorded layers instead of changing one tone's volume.
        centers=[40,61,93];pos=float(np.interp(vel,centers,[0,1,2]));lo=min(2,int(pos));hi=min(2,lo+1)
        weights=[(LAYERS[lo],1-(pos-lo)),(LAYERS[hi],pos-lo)] if lo!=hi else [(LAYERS[lo],1)]
        start=round(at*RATE);release=.65 if hold<.65 else 1.25
        length=min(frames-start,round((hold+release)*RATE));gate=min(length,round(hold*RATE))
        for layer,weight in weights:
            if weight<.01:continue
            data=pitched(n,layer);count=min(length,len(data));voice=data[:count].copy()
            if count>gate:voice[gate:]*=np.exp(-np.linspace(0,7.5,count-gate,dtype=np.float32))[:,None]
            out[start:start+count]+=voice*(weight*(vel/80)**.65)
    return out

def orchestral(events,frames):
    lib=C.CDLL('libfluidsynth.so.3');ptr=C.c_void_p;integer=C.c_int
    def bind(name,restype,args):
        fn=getattr(lib,name);fn.restype=restype;fn.argtypes=args;return fn
    settings=bind('new_fluid_settings',ptr,[])()
    sn=bind('fluid_settings_setnum',integer,[ptr,C.c_char_p,C.c_double])
    si=bind('fluid_settings_setint',integer,[ptr,C.c_char_p,integer])
    sn(settings,b'synth.sample-rate',RATE);sn(settings,b'synth.gain',.34)
    si(settings,b'synth.reverb.active',0);si(settings,b'synth.chorus.active',0)
    synth=bind('new_fluid_synth',ptr,[ptr])(settings)
    assert bind('fluid_synth_sfload',integer,[ptr,C.c_char_p,integer])(synth,str(SF).encode(),1)>=0
    pg=bind('fluid_synth_program_change',integer,[ptr,integer,integer]);cc=bind('fluid_synth_cc',integer,[ptr,integer,integer,integer])
    # cello, ensemble, French horn, celesta, pizzicato, harp, timpani
    for ch,prg in enumerate([0,42,48,60,8,45,46,47]):
        pg(synth,ch,prg);cc(synth,ch,10,[64,53,74,62,83,43,74,58][ch])
    on=bind('fluid_synth_noteon',integer,[ptr,integer,integer,integer]);off=bind('fluid_synth_noteoff',integer,[ptr,integer,integer])
    write=bind('fluid_synth_write_float',integer,[ptr,integer,ptr,integer,integer,ptr,integer,integer])
    timeline=[]
    for at,lane,n,d,v in events:
        if lane:timeline.extend([(round(at*RATE),1,lane,n,v),(round((at+d)*RATE),0,lane,n,0)])
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

def periodic_filter(a,sos):
    # The preceding cycle primes the filter; no artificial reset at a loop boundary.
    return signal.sosfilt(sos,np.tile(a,(2,1)),axis=0)[len(a):].astype(np.float32)

def fold(a,frames):
    out=a[:frames].copy()
    tail=a[frames:];out[:len(tail)]+=tail
    return out

def room(a,wet,rt60,seed):
    rng=np.random.default_rng(seed);n=round(rt60*RATE)
    impulse=np.zeros((n,2),np.float32)
    t=np.arange(n)/RATE
    diffuse=signal.sosfilt(signal.butter(2,5200,fs=RATE,output='sos'),rng.normal(0,1,(n,2)),axis=0)
    diffuse*=np.exp(-6.91*t/rt60)[:,None]
    diffuse/=np.sqrt(np.sum(diffuse*diffuse,axis=0))[None,:]
    impulse+=diffuse*.34
    for sec,gain in [(.023,.16),(.041,.13),(.068,.10),(.091,.07),(.127,.05)]:
        for ch in range(2):impulse[round((sec+ch*.006)*RATE),ch]+=gain
    out=a.copy()
    for ch in range(2):
        convolved=signal.fftconvolve(a[:,ch],impulse[:,ch])
        out[:,ch]+=wet*convolved[:len(a)]
        out[:len(convolved)-len(a),ch]+=wet*convolved[len(a):]
    return out

def loudness(path):
    p=subprocess.run(['ffmpeg','-v','info','-i',str(path),'-af','loudnorm=print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    return json.JSONDecoder().raw_decode(p.stderr[p.stderr.rfind('{'):].lstrip())[0]

def render(name,track):
    events,seconds=make_score(track,name);frames=round(seconds*RATE)
    count=frames+8*RATE
    print('Rendering',name,len(events),'notes',round(seconds,2),'seconds',flush=True)
    p=fold(piano(events,count),frames);o=fold(orchestral(events,count),frames)
    p=periodic_filter(p,signal.butter(2,38,fs=RATE,btype='highpass',output='sos'))
    p=periodic_filter(p,signal.butter(2,12500,fs=RATE,output='sos'))
    o=periodic_filter(o,signal.butter(2,100,fs=RATE,btype='highpass',output='sos'))
    dry_piano_rms=float(np.sqrt(np.mean(p*p)));dry_orchestra_rms=float(np.sqrt(np.mean(o*o)))
    orchestra_gain=(3.5 if track.style=='title' else 3.1 if track.style in ('meeting','press','climax','climax-press','serious') else 2.3)
    mix=room(p,.24,1.7,72)+room(o*orchestra_gain,.38,1.9,146)
    assert np.isfinite(mix).all()
    with tempfile.TemporaryDirectory() as td:
        raw=Path(td)/'mix.wav';wavfile.write(raw,RATE,mix.astype(np.float32))
        measured=loudness(raw)
        # Static mastering preserves the phrasing and loop seam. A peak ceiling
        # has priority over forcing every quiet cue to the same loudness.
        gain_db=min(track.loudness-float(measured['input_i']),-2.8-float(measured['input_tp']))
        mix*=10**(gain_db/20)
        wavfile.write(raw,RATE,mix.astype(np.float32))
        path=OUT/f'{name}-piano-v2.mp3'
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(raw),'-codec:a','libmp3lame','-b:a','224k','-ar',str(RATE),
                        '-metadata',f'title={track.title}','-metadata','artist=daaegame original score',str(path)],check=True)
    result={'name':name,'key':track.key,'title':track.title,'bpm':track.bpm,'bars':track.bars,
            'seconds':frames/RATE,'volume':track.volume,'file':path.name,
            'integrated_lufs':round(float(measured['input_i'])+gain_db,2),
            'true_peak_db':round(float(measured['input_tp'])+gain_db,2),
            'loudness_range':float(measured['input_lra']),
            'piano_rms_before_mix':dry_piano_rms,'orchestra_rms_before_mix':dry_orchestra_rms,
            'orchestra_mix_gain':orchestra_gain,
            'loop_boundary_jump':float(np.max(np.abs(mix[0]-mix[-1]))),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    print(result,flush=True)
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--only');args=parser.parse_args()
    assert TUNING and SF.exists(),'Run gen/fetch_piano_samples.py first'
    OUT.mkdir(parents=True,exist_ok=True)
    old=OUT/'score-piano-v2.json';data=json.loads(old.read_text()) if old.exists() else []
    saved={x['name']:x for x in data}
    names=args.only.split(',') if args.only else list(TRACKS)
    for name in names:saved[name]=render(name,TRACKS[name])
    data=[saved[n] for n in TRACKS if n in saved]
    old.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    songs={x['key']:{'bpm':x['bpm'],'vol':x['volume'],'prog':['Dm'],'mel':[],
                       'media':'audio/v2/'+x['file'],'loopSeconds':x['seconds']} for x in data}
    for key,buddies in {'inn_meet':['inn_meet_press','inn_climax'],
                        'inn_climax':['inn_climax_press','inn_t_innma']}.items():
        if key in songs:songs[key]['preload']=[songs[k]['media'] for k in buddies if k in songs]
    (SOURCE/'inn_piano_tracks.js').write_text('/* Generated by gen/music_piano_v2.py; original piano score. */\nwindow.__INN_PIANO='+json.dumps(songs,ensure_ascii=False,separators=(',',':'))+';\n')
    (OUT/'SALAMANDER-LICENSE.txt').write_bytes((CACHE/'salamander/LICENSE').read_bytes())
    (OUT/'FLUIDR3-LICENSE.txt').write_bytes((CACHE/'fluid/usr/share/doc/fluid-soundfont-gm/copyright').read_bytes())
    (OUT/'PIANO_CREDITS.txt').write_text(
        'Original composition, arrangement and mix: daaegame chapter-one v2, 2026-10-10.\n'
        'Score/renderer: dev/wip-v2/gen/music_piano_v2.py\n'
        'Piano recordings: Salamander Grand Piano V3, Yamaha C5, Alexander Holm, CC BY 3.0.\n'
        'Retuning: Markus Fiedler; SFZ mapping: kinwie.\n'
        f'Pinned source: https://github.com/sfzinstruments/SalamanderGrandPiano/tree/{REV}\n'
        'License: https://creativecommons.org/licenses/by/3.0/ (SALAMANDER-LICENSE.txt).\n'
        'Adaptations: velocity-layer blending, retuning, sample-rate conversion, performance envelopes, original score and room mix.\n'
        'Orchestral recordings: FluidR3 GM, Frank Wen (2000-2002, 2008), Toby Smithe (2008), MIT.\n'
        'Source: https://deb.debian.org/debian/pool/main/f/fluid-soundfont/fluid-soundfont-gm_3.1-6_all.deb\n'
        'Package SHA256: 9965fbcc6acee17d6f72b685d28c7f968ec64eba14645445b476d5c6cc2eee4c\n'
        'See FLUIDR3-LICENSE.txt. Instrument libraries are not bundled with the game.\n'
        'Earlier *-v1.mp3 tracks retain their existing CREDITS.txt/GPL-2.txt terms. Game/art licenses are separate.\n')

if __name__=='__main__':main()
