"""Build the art brief and evidence mapping from exported frozen sandbox-game data."""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=json.loads(Path('/tmp/daram-source-locations.json').read_text())
case_data=[];locations={};scenes=[]
for c in s['cases']:
 case_data.append({'id':c['id'],'title':c['title'],'time':c['time'],'locations':[c['id']+'-'+l['id'] for l in c['locations']]})
 for l in c['locations']:
  key=c['id']+'-'+l['id'];evidence=[];observations=[]
  for sp in l['spots']:
   point=s['hots'][sp['id']]
   evidence.append({'spotId':sp['id'],'evidenceId':sp['ev']['id'],'name':sp['name'],'evidence':sp['ev'],'text':sp['text'],'point':point,'sourcePoint':point,'uv':bool(sp.get('uv')),'inZoom':sp.get('inZoom')})
  for ob in l.get('obs',[]):observations.append({**ob,'point':[ob['x'],ob['y']]})
  zooms={o['zoom']:s['zooms'][o['zoom']] for o in observations if o.get('zoom') and o['zoom'] in s['zooms']}
  locations[key]={'id':key,'caseId':c['id'],'locationId':l['id'],'name':l['name'],'caseTitle':c['title'],'time':c['time'],'backgroundId':key,'evidence':evidence,'observations':observations,'zooms':zooms,'people':c.get('ppl',{}).get(l['id'],[]),'info':l.get('info',[])}
  instructions=[f'Location: {l["name"]}. In original mystery chapter {c["title"]}. Time/weather context: {c["time"]}.']
  instructions+=['Story-specific physical evidence targets, with EXACT CENTER placement in coordinates of a 360 by 200 panoramic scene (origin upper left, x horizontal, y vertical):']
  for e in evidence:
   if e['inZoom']:continue
   x,y=e['point'];detail=e['evidence']['desc']
   if e['uv']:
    instructions.append(f'At ({x},{y}), the ordinary physical surface bearing hidden UV-only markings: {e["name"]}. Markings MUST NOT be visible under normal light. Context (do not reveal it visually): {detail}')
   else:instructions.append(f'At ({x},{y}), draw the actual physical target {e["name"]}: {detail}')
  for o in observations:
   if o.get('zoom'):
    hidden=[e for e in evidence if e['inZoom']==o['zoom']]
    instructions.append(f'At ({o["x"]},{o["y"]}), draw inspectable CLOSED container {o["name"]}; hidden contents '+', '.join(e['evidence']['name'] for e in hidden)+' must remain INSIDE, not scattered visibly outside.')
   elif o.get('name') not in [e['name'] for e in evidence]:instructions.append(f'Secondary observation object at ({o["x"]},{o["y"]}): {o["name"]}.')
  instructions+=['Architecture and furniture must support these placements naturally. Documents, notices and calendars have NO legible writing; actual canonical wording is displayed in HTML on inspection. Clocks and mechanical objects are authentic, not decorative duplicates. Empty cabinets, missing stolen items, cut ropes, displaced parts and clues described above MUST stay in their described state. Do not invent another stolen stone/crown/clapper in the room. Very small hair/fiber/scratch clues live on the specified parent object, not as oversized unrelated props. No people or animal characters baked into this background; witnesses are rendered as separate sprites.']
  scenes.append({'id':key,'name':l['name'],'brief':'\n'.join(instructions)})
scenes.append({'id':'forest-path','name':'마을을 잇는 숲길','brief':'Quiet woodland stone path, old oaks, small wooden bridge, one brass lantern, misty dawn. No evidence props, no characters.'})
zoom_backgrounds={}
for zk,z in s['zooms'].items():
 if not any(it.get('ev') for it in z['items']):continue
 zid='zoom-'+zk;zoom_backgrounds[zk]=zid
 brief=f'Close inspection view INSIDE an OPEN container: {z["title"]}. Detailed warm wooden drawer/tray/box fills the scene, no people. This is the zoom view after opening; draw contents visibly, correctly placed on a 360x200 inner panorama.\n'
 for it in z['items']:
  brief+=f'At ({it["x"]},{it["y"]}): {it["name"]}. '+it.get('text',it.get('ev',{}).get('desc',''))+'\n'
 brief+='No legible writing. Do not show other exterior rooms or add unrelated props. Keep all actual content fully visible in the central 16:9 safe area.'
 scenes.append({'id':zid,'name':z['title'],'brief':brief})
base='''Production pixel-art backgrounds for the existing Daram Detective game. Make ONE atlas containing FOUR distinct panoramic scenes in an exact TWO COLUMNS by TWO ROWS grid: top left, top right, bottom left, bottom right. Overall canvas WIDE 16:9, each quadrant a full 16:9 landscape view. No borders, captions, lettering, map markers or UI. Handcrafted intricate pixel art, restrained outlines, lived-in warm wood and brass, cool indigo shadows, atmospheric mature woodland detective mystery, coherent material palette and natural perspective. No cartoon toy props or people. Crucial: EVERY evidence object in the brief must be physically present at its specified 360x200 normalized location WITHIN its own quadrant. Treat all coordinates as applying to the INNER 16:9 safe panorama, not to the entire atlas. If output dimensions are automatically 3:2, reserve quiet ceiling/sky and floor strips above and below EACH scene; ALL crucial props must remain inside the central 16:9 crop of that quadrant. The game renders that crop without stretching. Use only the actual story evidence described, never introduce a contradictory object. No readable writing baked into documents; original Korean evidence text is shown separately. Keep the bottom foreground modestly clear for character sprites without hiding evidence. Detailed readable furniture and clue silhouettes, realistic game scenery.\n'''
jobs=[]
for i in range(0,len(scenes),4):
 group=scenes[i:i+4];prompt=base
 for pos,scene in zip(['TOP LEFT','TOP RIGHT','BOTTOM LEFT','BOTTOM RIGHT'],group):prompt+='\n'+pos+' SCENE:\n'+scene['brief']+'\n'
 if len(group)<4:prompt+='\nBOTTOM RIGHT: quiet empty woodland road continuing the other forest scenery, no evidence, no characters.\n'
 jobs.append({'index':i//4+1,'ids':[v['id'] for v in group],'prompt':prompt})
(root/'scene-map.json').write_text(json.dumps({'version':3,'coordinateSpace':[360,200],'aspectRatio':[16,9],'source':'game.html CASES / HOTS / window.__ZOOM','sourceSha256':hashlib.sha256((root/'sandbox/game.html').read_bytes()).hexdigest(),'caseOrder':[c['id'] for c in case_data],'cases':case_data,'locationOrder':list(locations),'locations':locations,'zoomBackgrounds':zoom_backgrounds,'evidenceCount':sum(len(l['evidence']) for l in locations.values())},ensure_ascii=False,indent=2)+'\n')
(root/'scene-jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2)+'\n')
print(f'{len(locations)} locations; {sum(len(l["evidence"]) for l in locations.values())} evidence; {len(jobs)} background atlas jobs')
