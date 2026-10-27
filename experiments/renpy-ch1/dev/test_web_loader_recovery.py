import json,subprocess,unittest
from build_web import LOADER
class LoaderRecovery(unittest.TestCase):
 def test_retry_truncation_and_failed_preload_never_start_runtime(self):
  script='''const assert=require('assert');let removed=0,buttons=[],errors=[];
const Module={preRun:[],addRunDependency(){},removeRunDependency(){removed++}};
const el=tag=>({tagName:tag,children:[],style:{},attrs:{},appendChild(c){this.children.push(c);return c},setAttribute(k,v){this.attrs[k]=v},focus(){}});
const statusTextDiv=el('div'),head=el('head'),classes=[];
const document={baseURI:'https://example.test/game/',createElement:el,head,documentElement:{classList:{add(c){classes.push(c)}}},
 getElementById(id){return id==='statusTextDiv'?statusTextDiv:buttons.find(b=>b.id===id)},body:{appendChild(b){buttons.push(b)}}};
const location={reload(){}};
const reportError=(...args)=>errors.push(args);
let gameZipDownloaded=0,gameZipSize=0;const updateDownloadProgress=()=>{};
let bytes=3,calls=0;
global.fetch=async()=>{calls++;return new Response(new Uint8Array(bytes))};
'''+LOADER+'''
(async()=>{
 let progress=0;
 const ok=await r13Fetch('https://example.test/a',n=>progress+=n,3);assert.equal(ok.length,3);assert.equal(calls,1);
 calls=0;progress=0;
 await assert.rejects(r13Fetch('https://example.test/b',n=>progress+=n,4),/incomplete download/);
 assert.equal(calls,3);assert.equal(progress,0);
 calls=0;global.fetch=async()=>{calls++;if(calls===1)throw Error('offline');return new Response(new Uint8Array(3))};
 assert.equal((await r13Fetch('https://example.test/c',()=>{},3)).length,3);assert.equal(calls,2);
 global.fetch=async()=>{throw Error('offline')};runLoadGameZip();await new Promise(r=>setTimeout(r,30));
 assert.equal(removed,0);assert.equal(buttons.length,1);assert.equal(errors.length,1);
 // One panel: Korean explanation + retry button; engine log folded into details.
 const panel=buttons[0];assert.equal(panel.id,'r13-load-error');assert(classes.includes('r13-load-failed'));
 const [title,message,retry,details]=panel.children;
 assert.equal(retry.tagName,'button');assert(retry.textContent.includes('저장 기록'));assert(/연결을 확인/.test(message.textContent));
 assert.equal(details.tagName,'details');assert(details.children.includes(statusTextDiv));
 runLoadGameZip();await new Promise(r=>setTimeout(r,30));assert.equal(buttons.length,1);
})().catch(e=>{console.error(e);process.exit(1)});
'''
  subprocess.run(['node','-e',script],check=True,capture_output=True,text=True)

class ProgressiveVersioning(unittest.TestCase):
 def test_changed_art_gets_new_cache_key_without_changing_engine_file_path(self):
  script='''const assert=require('assert');let calls=[];
const Module={preRun:[]};const document={baseURI:'https://example.test/preview/'};
const XMLHttpRequest=class {open(...args){calls.push(args)}};
'''+LOADER+'''
r13AssetVersions={'game/assets/portrait.webp':'first'};
new XMLHttpRequest().open('GET','game/assets/portrait.webp',true);
assert.equal(calls[0][1],'https://example.test/preview/game/assets/portrait.webp?v=first');
r13AssetVersions['game/assets/portrait.webp']='next';
new XMLHttpRequest().open('GET','game/assets/portrait.webp',true);
assert(calls[1][1].endsWith('?v=next'));
new XMLHttpRequest().open('GET','https://other.test/game/assets/portrait.webp',true);
assert.equal(calls[2][1],'https://other.test/game/assets/portrait.webp');
'''
  subprocess.run(['node','-e',script],check=True,capture_output=True,text=True)


class ProgressiveDirectories(unittest.TestCase):
 def test_late_nested_assets_have_directories_without_being_downloaded_at_boot(self):
  script='''const assert=require('assert');let dirs=[],requests=[];
const Module={preRun:[]};const document={baseURI:'https://example.test/preview/'};
const FS={mkdir(p){dirs.push(p)},open(){return {}},write(){},close(){}};
let gameZipSize=0,gameZipDownloaded=0;const updateDownloadProgress=()=>{};const reportError=(...args)=>{throw Error(args)};
const transport={archive_bytes:3,preload:[],asset_versions:{'game/assets/late/nested/portrait.webp':'hash'},parts:[{file:'game.part01',bytes:3,sha256:'x'}]};
global.fetch=async(url)=>{requests.push(String(url));return String(url).includes('game-transport.json')?new Response(JSON.stringify(transport)):new Response(new Uint8Array(3))};
'''+LOADER+'''
(async()=>{await loadGameZip();assert(dirs.includes('/game/assets/late/nested'));assert.equal(requests.length,2);assert(!requests.some(x=>x.includes('portrait.webp')));})().catch(e=>{console.error(e);process.exit(1)});
'''
  subprocess.run(['node','-e',script],check=True,capture_output=True,text=True)


class LoadFailureLayout(unittest.TestCase):
 def test_failure_hides_loading_hint_and_status_line_and_keeps_touch_target(self):
  # External QA 0.20.66: the error text overlapped the loading hint by 20-34px.
  import re
  from build_web import LOADER
  css=LOADER[LOADER.index('R13_LOAD_ERROR_CSS = ['):LOADER.index('].join')]
  self.assertIn('.r13-load-failed #loading-brand,.r13-load-failed #statusDiv{display:none!important}',css)
  button=re.search(r'#r13-load-error button\{([^}]*)\}',css).group(1)
  self.assertGreaterEqual(int(re.search(r'min-height:(\d+)px',button).group(1)),44)
  self.assertIn('max-height:calc(100vh - 24px);overflow:auto',css)
  self.assertNotIn('scrollTop',LOADER[LOADER.index('function r13ShowLoadFailure'):LOADER.index('function runLoadGameZip')])

if __name__=='__main__':unittest.main()
