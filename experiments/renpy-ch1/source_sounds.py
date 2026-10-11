"""Render the existing v2 procedural sound recipes as offline PCM for Ren'Py.

The source is dev/wip-v2/inn_audio.js. These are effects, not new music or voices.
Wood doors remain byte-for-byte copies of the attributed recordings.
"""
import math
import random
import struct
import wave
from pathlib import Path

RATE = 22050

def render_typing(path):
    """Audible soft, short taps with silence between them, never a sustained tone."""
    rng = random.Random(20261011)
    samples = []
    for frequency in (680, 740, 700, 770):
        for i in range(int(.072*RATE)):
            t = i/RATE
            env = min(1,t/.0015)*math.exp(-t/.006) if t<.030 else 0
            value = env*(.16*math.sin(2*math.pi*frequency*t)+.045*(rng.random()*2-1))
            samples.append(round(max(-.22,min(.22,value))*32767))
    with wave.open(str(path),'wb') as file:
        file.setnchannels(1);file.setsampwidth(2);file.setframerate(RATE)
        file.writeframes(b''.join(struct.pack('<h',s) for s in samples))

def render(destination):
    rng = random.Random(20261011)
    recipes = {
        'tap': [(460,.032,.04,0)], 'select': [(587.33,.055,.035,0)],
        'found': [(587.33,.18,.075,0),(880,.18,.075,.08)],
        'pop9': [(880,.12,.06,0),(1320,.12,.06,.05),(1760,.12,.06,.1)],
        'slam': [(100,.26,.4,0)], 'impact': [(98,.5,.3,0)],
        'cut9': [(70,.6,.4,0),(2200,.05,.05,0)],
        'low9': [(98,.9,.08,0),(147,.6,.025,.02)],
        'shock9': [(1500,.16,.07,0),(110,.28,.3,0)],
        'heartbeat': [(58,.16,.28,0),(52,.14,.196,.29)],
        'bell10': [(f,d,v,i*.75) for i in range(10)
                   for f,d,v in [(196,3,.16),(392,1.6,.05),(470,1.2,.025)]],
        'knock': [(160,.1,.16,i*.22) for i in range(3)],
        'steps': [(95,.085,.075,i*.29) for i in range(3)],
        'lock': [(800,.04,.06,0),(240,.09,.12,.06)],
        'page': [],
        'silence': [],
    }
    durations={'heartbeat':1.04,'page':.14,'silence':.35}
    for name, tones in recipes.items():
        duration=max(durations.get(name,0),max((at+d for f,d,v,at in tones),default=.14))
        samples=[0.0]*int((duration+.04)*RATE)
        for frequency,seconds,volume,at in tones:
            start=int(at*RATE);length=int(seconds*RATE)
            for i in range(length):
                t=i/RATE;env=min(1,t/.004)*math.exp(-5*t/seconds)
                samples[start+i]+=volume*env*math.sin(2*math.pi*frequency*t)
        if name in ('page','steps','lock','knock','slam','impact','shock9','cut9'):
            for i in range(min(len(samples),int(.12*RATE))):
                samples[i]+=(rng.random()*2-1)*.035*math.exp(-30*i/RATE)
        with wave.open(str(destination/('source-'+name+'.wav')),'wb') as file:
            file.setnchannels(1);file.setsampwidth(2);file.setframerate(RATE)
            file.writeframes(b''.join(struct.pack('<h',round(max(-.8,min(.8,s))*32767)) for s in samples))
    # The restored anonymous hook accelerates independently of dialogue speed.
    # RenPy owns this channel, so save/menu/rollback do not leave web timers alive.
    for index,bpm in enumerate((55,65,76,88,102,116,130)):
        duration=60/bpm
        samples=[]
        for i in range(round(duration*RATE)):
            t=i/RATE; value=0
            for at,freq,gain in ((0,58,.18),(.13,52,.12)):
                dt=t-at
                if 0<=dt<.115:
                    value+=gain*min(1,dt/.008)*math.exp(-dt/.032)*math.sin(2*math.pi*freq*dt)
            samples.append(round(value*32767))
        with wave.open(str(destination/('cold-heart-'+str(index)+'.wav')),'wb') as file:
            file.setnchannels(1);file.setsampwidth(2);file.setframerate(RATE)
            file.writeframes(b''.join(struct.pack('<h',s) for s in samples))
