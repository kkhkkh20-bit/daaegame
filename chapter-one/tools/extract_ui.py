"""Reuse original navigation SVGs and record styling; no engine changes."""
from pathlib import Path
import re,json,hashlib
from urllib.parse import quote
root=Path(__file__).resolve().parents[1];src=(root.parent/'game.html').read_text()
icons={}
for name in ['IC','NAVIC']:
 block=re.search(r'var '+name+r'=\{(.*?)\n\};',src,re.S).group(1)
 for key,svg in re.findall(r"(\w+):'(<svg.*?</svg>)'",block):icons[name+'.'+key]=svg
mapping={'#nav-scene':'NAVIC.scene','#nav-move':'IC.move','#nav-talk':'NAVIC.talk','#nav-note,#notebook':'NAVIC.note','#nav-fight':'IC.present','#nav-hint':'IC.bulb','#log':'IC.rec','#settings':'IC.set','[data-tab="evidence"]':'IC.present','[data-tab="testimony"]':'NAVIC.talk','[data-tab="timeline"]':'IC.rec'}
css='/* Navigation icon paths copied from original game.html IC/NAVIC. */\n'
for selector,key in mapping.items():
 svg=icons[key].replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ').replace('currentColor','#000')
 css+=selector+'{--menu-icon:url("data:image/svg+xml,'+quote(svg,safe='')+'")}\n'
(root/'original-icons.css').write_text(css)
(root/'ui-provenance.json').write_text(json.dumps({'source':'game.html','icons':list(mapping.values()),'record_styles':['crec2','cr-det','cr-ic','cr-tx','cr-grid','cr-th'],'dot_styles':'dotmode / Galmuri11','source_sha256':hashlib.sha256(src.encode()).hexdigest()},indent=2)+'\n')
