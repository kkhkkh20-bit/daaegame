"""Copy original presentation functions verbatim and adapt their asset dependencies."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[2]
source=(root/'game.html').read_text()
# Share the existing brace-safe extractor without executing its build side effects.
module=(Path(__file__).with_name('extract_core.py')).read_text()
namespace={'source':source}
exec(module[module.index('def extract('):module.index('functions={')],namespace)
names=['flash','panicFx','banner','flyEvidence']
functions={name:namespace['extract'](name) for name in names}
header='''/* Original game.html presentation functions, with chapter asset adapters. */
(()=>{'use strict';
const CAST=PEOPLE;
const SFX=new Proxy({},{get:(_,name)=>()=>window.DaramAudio?.fx(name)});
const PANIC={culprit:[["뭐, 뭐라고?!","헉!"],["그, 그건… 그러니까…!","으윽!"],["말도 안 돼… 어떻게 그걸…!","크윽!"],["아아악! 아니야, 아니라고!","끝이다…"]],shy:[["히익! 그, 그거 보지 마!","히잉…"]],mistake:[["어…? 어어?! 그럼 내가…?","어라?"]]};
const HAND='<span aria-hidden="true">☛</span>';
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const quiet=()=>window.DaramEffects?.get()!=='standard'||matchMedia('(prefers-reduced-motion: reduce)').matches;
const evById=(_,id)=>EVIDENCE[id];
const tById=(_,id)=>TESTIMONIES[id]&&{who:TESTIMONIES[id].who};
const evIcon=id=>DaramEvidenceArt.thumb(id,EVIDENCE[id]?.title||id);
const pf=(id,mood)=>'<div class="legacy-portrait" style="background-image:url('+DaramArt.source(id)+');background-position:'+(mood==='nervous'?50:0)+'% 0" aria-hidden="true"></div>';
const spiky=()=>'<svg viewBox="0 0 300 100" aria-hidden="true"><path d="M0 30L30 25 20 0 65 16 80 0 110 14 140 0 155 13 185 0 200 16 240 0 250 22 300 10 280 44 300 65 263 70 275 100 230 84 200 100 175 87 145 100 120 86 83 100 65 85 22 100 30 75 0 80 15 55Z"/></svg>';
function quake(){if(quiet())return;document.getElementById('scene')?.animate([{transform:'translateX(0)'},{transform:'translateX(-4px)'},{transform:'translateX(4px)'},{transform:'none'}],{duration:240});}
// Keep original durations in basic mode; remove movement and shorten beats in reduced/off modes.
function setTimeout(fn,ms){return window.setTimeout(fn,quiet()?Math.min(ms,160):ms);}
'''
footer='''
window.DaramPresentation={
 flash:(text,bad,point)=>window.DaramEffects?.get()==='off'?Promise.resolve():flash(esc(text),bad,point),
 panic:(who,kind,level)=>window.DaramEffects?.get()==='off'?Promise.resolve():new Promise(resolve=>panicFx(who,kind,level,resolve)),
 banner:(text,sub)=>window.DaramEffects?.get()==='off'?Promise.resolve():banner(esc(text),esc(sub||'')),
 present(from,id){if(quiet())return Promise.resolve();return flyEvidence(from,id,{});}
};
})();
'''
(root/'chapter-one/legacy-presentation.js').write_text(header+'\n'.join(functions.values())+footer)
(root/'chapter-one/presentation-provenance.json').write_text(json.dumps({n:{'source':'game.html','line':source[:source.index('function '+n+'(')].count('\n')+1,'sha256':hashlib.sha256(f.encode()).hexdigest()} for n,f in functions.items()},indent=2)+'\n')
print('Copied original flash, panicFx, banner, flyEvidence')
