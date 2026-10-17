# 0.19.7 (owner: 다람이 놀래키는 소리를 밝고 튀게). Usage: python3 dev/make_sfx_surprise.py game/assets/sfx-surprise.wav
# Bright, bouncy "surprise!" cue: a springy boing that leaps up, then a quick sparkle arpeggio.
import numpy as np, wave, sys
sr=44100
def env(n,a,d):
    t=np.arange(n)/sr; e=np.minimum(1,t/a)*np.exp(-t/d); return e
out=np.zeros(int(sr*0.62))
# 1) boing: pitch jumps 330->990Hz with a springy wobble, soft square-ish (odd harmonics) for cartoon brightness
n=int(sr*0.26); t=np.arange(n)/sr
f=330+660*(1-np.exp(-t/0.035))+60*np.sin(2*np.pi*18*t)*np.exp(-t/0.08)
ph=2*np.pi*np.cumsum(f)/sr
boing=(np.sin(ph)+0.33*np.sin(3*ph)+0.12*np.sin(5*ph))*env(n,0.004,0.09)
out[:n]+=0.55*boing
# 2) sparkle: C6 E6 G6 C7 bell pings, 45ms apart
for i,hz in enumerate([1046.5,1318.5,1568.0,2093.0]):
    s=int(sr*(0.09+0.045*i)); m=int(sr*0.3); tt=np.arange(m)/sr
    tone=(np.sin(2*np.pi*hz*tt)+0.4*np.sin(2*np.pi*hz*2.01*tt)+0.15*np.sin(2*np.pi*hz*3.02*tt))*env(m,0.002,0.07+0.02*i)
    out[s:s+m]+=0.28*tone[:len(out)-s]
out*=np.minimum(1,(len(out)-np.arange(len(out)))/(sr*0.03))
out=out/np.abs(out).max()*0.45*32767
w=wave.open(sys.argv[1],'w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(out.astype(np.int16).tobytes());w.close()
