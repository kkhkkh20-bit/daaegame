"""조사 UI 공통 스티커: 새 벡터 원본, 원본 비율, 고정 모서리."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'experiments/renpy-ch1/game/assets/ui-field-stickers'
OUT.mkdir(exist_ok=True)
def write(name,w,h,body):
    svg=Path(__file__).parent/(name+'.svg')
    svg.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>')
    subprocess.run(['inkscape',str(svg),'--export-filename='+str(OUT/(name+'.png'))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
for name,w,h,tape in [('paper',160,64,False),('place',160,64,True),('primary',160,64,False),('label',96,36,False)]:
    for state,ink in [('basic','#29364b'),('hover','#be343f')]:
        fill='#d8414a' if name=='primary' else '#fff0d4'
        body=f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="10" fill="#fff9e9"/><rect x="6" y="6" width="{w-12}" height="{h-12}" rx="7" fill="{fill}" stroke="{ink}" stroke-width="3"/>'
        if tape:body+=f'<path d="M{w-39} 1l25 3 -2 10 -25 -3z" fill="#d8414a"/><path d="M{w-34} 3l-2 7m8-6 -2 7m8-6 -2 7" stroke="#fff0d4" opacity=".65" stroke-width="2"/>'
        write(name+'_'+state,w,h,body)
for direction in ['left','right']:
    for state,color in [('basic','#d8414a'),('hover','#b72938')]:
        body=f'<path d="M13 28L35 10Q40 6 40 14V21H59Q64 21 64 27V43Q64 49 59 49H40V56Q40 64 35 60L13 42Q5 35 13 28Z" fill="{color}" stroke="#fff8e6" stroke-width="8" stroke-linejoin="round"/><path d="M13 28L35 10Q40 6 40 14V21H59Q64 21 64 27V43Q64 49 59 49H40V56Q40 64 35 60L13 42Q5 35 13 28Z" fill="none" stroke="#29364b" stroke-width="2.5"/>'
        if direction=='right':body='<g transform="translate(72 0) scale(-1 1)">'+body+'</g>'
        write('arrow_'+direction+'_'+state,72,72,body)

write('diary',160,96,'<rect x="2" y="2" width="156" height="92" rx="16" fill="#fff8e8"/><rect x="6" y="6" width="148" height="84" rx="13" fill="#29364b"/><rect x="10" y="10" width="140" height="76" rx="10" fill="none" stroke="#c9a36a" stroke-width="1" stroke-dasharray="3 3"/><rect x="15" y="15" width="130" height="66" rx="8" fill="#e9d6b5"/><rect x="18" y="18" width="124" height="60" rx="7" fill="#fff0d4"/>')
write('ring',28,34,'<path d="M23 8C-2 0 -2 33 23 26" fill="none" stroke="#29364b" stroke-width="10" stroke-linecap="round"/><path d="M23 8C-2 0 -2 33 23 26" fill="none" stroke="#bd7d37" stroke-width="6" stroke-linecap="round"/><path d="M21 7C3 2 1 15 4 20" fill="none" stroke="#f7d393" stroke-width="2" stroke-linecap="round"/>')
