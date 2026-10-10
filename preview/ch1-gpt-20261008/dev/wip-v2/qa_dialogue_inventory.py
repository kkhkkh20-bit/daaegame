"""Read-only authored/runtime chapter-one dialogue inventory, not a rewrite."""
import json,re,tokenize,io,ast,statistics,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
OUT=Path('/tmp/dialogue-inventory');OUT.mkdir(exist_ok=True)
MAIN={'pro_new.js','script_a.js','script_b.js','gen/end_gen.js'}
def literals(text):
    # Scan JS strings while skipping comments/regex bodies; regex-only cues are
    # documented manually, and source literals are candidates, not live lines.
    i=0
    while i<len(text):
        if text.startswith('//',i):
            n=text.find('\n',i);i=len(text) if n<0 else n+1;continue
        if text.startswith('/*',i):
            n=text.find('*/',i+2);i=len(text) if n<0 else n+2;continue
        c=text[i]
        if c not in ('"',"'",'`'):
            i+=1;continue
        start=i;i+=1;value=[]
        while i<len(text):
            if text[i]=='\\' and i+1<len(text):
                value.append(text[i:i+2]);i+=2;continue
            if text[i]==c:break
            value.append(text[i]);i+=1
        i+=1;raw=''.join(value)
        try:v=json.loads('"'+raw+'"') if c=='"' else ast.literal_eval(c+raw+c) if c!="`" else raw
        except Exception:v=raw
        if isinstance(v,str) and re.search('[가-힣]',v):yield start,v

def main():
    outside=[]
    for path in sorted(ROOT.glob('*.js'))+sorted((ROOT/'patches').glob('*.py')):
        relative=str(path.relative_to(ROOT));text=path.read_text()
        if relative in MAIN:continue
        if path.suffix=='.py':
            pieces=[]
            for t in tokenize.generate_tokens(io.StringIO(text).readline):
                if t.type==tokenize.STRING:
                    try:pieces.append((t.start[0],ast.literal_eval(t.string)))
                    except Exception:pass
        else:pieces=[(1,text)]
        for start,part in pieces:
            if not isinstance(part,str):continue
            for offset,value in literals(part):
                if len(value)>1200 or ('{' in value and ':' in value and '<' in value):continue
                line=start+part[:offset].count('\n')
                outside.append({'source':relative,'line':line,'text':value,'length':len(value)})
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox'])
        page=browser.new_page();page.goto('http://127.0.0.1:8000/playT.html');page.wait_for_timeout(16000)
        runtime=page.evaluate(r'''()=>__T(`(()=>{const c=CASES.find(x=>x.id==='inn'),rows=[],meta=[],seen=new WeakSet();
          const speakers=new Set([...Object.keys(CAST),'narr','think','det0','det1','stage','obs']);
          function walk(o,path){if(!o||typeof o!=='object'||seen.has(o))return;seen.add(o);
            if(Array.isArray(o)&&speakers.has(o[0])&&typeof o[1]==='string'&&!/\.(suspects|witnesses|seats|cast)$/.test(path)){
              rows.push({path,speaker:o[0],text:o[7]||o[1]});return}
            if(!Array.isArray(o)&&typeof o.t==='string'&&typeof o.w==='string'){
              rows.push({path,speaker:o.w,text:o.t});return}
            if(!Array.isArray(o)&&typeof o.say==='string')rows.push({path:path+'.say',speaker:'cold',text:o.say});
            for(const k of Object.keys(o)){let v;try{v=o[k]}catch(e){continue}
              if(typeof v==='object')walk(v,path+'.'+k);
              else if(typeof v==='string'&&/[가-힣]/.test(v)&&v.length<1200)meta.push({path:path+'.'+k,text:v});}}
          walk(EP1INN,'EP');walk(c,'CASE');
          for(const n of ['BEATS','BATTLE','CONFESS','POST','WRONG','CHAT','BOOK','SHOW']){
            let o;try{o=eval(n)}catch(e){continue}if(o&&o.inn)walk(o.inn,n+'.inn')}
          return {rows,meta,caseKeys:Object.keys(c)};})()` )''')
        browser.close()
    groups={}
    for row in runtime['rows']:
        group=row['path'].split('.')[0];groups.setdefault(group,[]).append(row)
    stats={}
    for group,rows in groups.items():
        lengths=[len(r['text']) for r in rows];narr=[r for r in rows if r['speaker'] in ['narr','think','stage','obs']]
        stats[group]={'lines':len(rows),'meanChars':round(statistics.mean(lengths),1),'maxChars':max(lengths),'narrativeLines':len(narr),'narrativePercent':round(100*len(narr)/len(rows),1),'longest':sorted(rows,key=lambda r:len(r['text']),reverse=True)[:12]}
    current=[r for r in runtime['rows'] if r['path'].startswith('EP.') and '.COLD_V1.' not in r['path']]
    unique=[];seen=set()
    for row in current:
        key=(row['speaker'],re.sub('[{}]','',row['text']))
        if key not in seen:unique.append(row);seen.add(key)
    rec=[r for r in runtime['meta'] if r['path'].startswith('EP.TALK.') and r['path'].endswith('.rec')]
    def summary(rows):
        lengths=[len(r['text']) for r in rows];n=sum(r.get('speaker') in ['narr','think','stage','obs'] for r in rows)
        return {'lines':len(rows),'meanChars':round(statistics.mean(lengths),1) if lengths else 0,'maxChars':max(lengths,default=0),'narrativeLines':n,'narrativePercent':round(n*100/len(rows),1) if rows else 0}
    result={'stats':stats,'currentOnly':summary(current),'currentUnique':summary(unique),
            'recordSummaries':summary(rec),'limits':'Stored corpus, not observed play counts. Closed-over injected dialogue is not included. Source literals are candidates and may include UI/match strings.',
            'runtime':runtime,'outsideMainSourceLiterals':outside}
    (OUT/'inventory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    (OUT/'outside-main.tsv').write_text('\n'.join(f"{r['source']}:{r['line']}\t{r['length']}\t{r['text'].replace(chr(10),' / ')}" for r in outside))
    print(json.dumps(stats,ensure_ascii=False,indent=2));print('Inventory:',OUT)
if __name__=='__main__':main()
