"""Build a quiet paired hoof rhythm from the project's existing wooden knock.
No external samples: the source, timing and mix remain reproducible.
"""
from pathlib import Path
import wave
import numpy as np
from scipy.signal import butter,sosfilt
ROOT=Path(__file__).resolve().parents[1]
def build():
    source=ROOT/'game/assets/source-knock.wav'
    with wave.open(str(source),'rb') as w:
        rate=w.getframerate();channels=w.getnchannels();width=w.getsampwidth();raw=w.readframes(w.getnframes())
    assert width==2
    sample=np.frombuffer(raw,dtype='<i2').astype(float).reshape(-1,channels).mean(axis=1)/32768
    peak=int(np.argmax(np.abs(sample)))
    hit=sample[max(0,peak-int(rate*.012)):peak+int(rate*.15)]
    hit=sosfilt(butter(2,[220,4800],btype='bandpass',fs=rate,output='sos'),hit)
    hit*=np.minimum(1,np.arange(len(hit))/(rate*.003))*np.exp(-np.arange(len(hit))/(rate*.045))
    hit/=max(.01,np.max(np.abs(hit)))
    duration=4.48;out=np.zeros(int(rate*duration))
    for cycle in range(4):
        for offset,pitch,level in [(0,1.10,.50),(.21,.94,.72),(.56,1.04,.45),(.77,.91,.64)]:
            t=cycle*1.12+offset;piece=np.interp(np.arange(0,len(hit),pitch),np.arange(len(hit)),hit)*level
            at=int(t*rate);end=min(len(out),at+len(piece));out[at:end]+=piece[:end-at]
    with wave.open(str(ROOT/'game/assets/sfx-carriage-hooves.wav'),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes((np.clip(out,-1,1)*22000).astype('<i2').tobytes())
    print('hoof loop',rate,'Hz',duration,'seconds, peak',round(float(np.max(np.abs(out))),3))
if __name__=='__main__':build()
