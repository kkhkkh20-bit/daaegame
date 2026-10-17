"""Inventory exact static scenes and unresolved dynamic r13_lines calls; no emotion guessing."""
import json,re,collections
from pathlib import Path
import line_cues
ROOT=Path(__file__).resolve().parents[1]
PLAIN={'neutral','joy','angry','anxious','surprise','flustered','thinking','distressed','expressive','panic','breakdown'}
def classify(identity,index,packet,people,direction):
 person=packet[0];meta=packet[2] if len(packet)>2 and isinstance(packet[2],dict) else {}
 if person is None:return 'narration'
 if meta.get('thought'):return 'thought'
 if person=='dad':return 'default_pov_speech'
 cue=direction.get(identity,{}).get(str(index),{})
 pose=cue.get('pose') if (cue.get('person'),cue.get('text'))==tuple(packet[:2]) else None
 pose=meta.get('pose',meta.get('expression',pose))
 if len(packet)>2 and isinstance(packet[2],str):pose=packet[2]
 if len(packet)>3:pose=packet[3]
 key=(pose or 'neutral').removeprefix('interview_')
 if key not in PLAIN:return 'authored_action_separate_review'
 if person not in people:return 'speaker_without_registered_art'
 return 'dialogue_expression_candidate'
def inventory():
 scenes=line_cues.scene_rows();people=json.loads((ROOT/'game/assets/room13-fullbody-dialogue.json').read_text())['people'];rows=[]
 cues=json.loads((ROOT/'game/assets/room13-dialogue-beats.json').read_text())['lines']
 direction=json.loads((ROOT/'game/assets/room13-line-direction.json').read_text())
 for identity,packets in scenes.items():
  for i,p in enumerate(packets):
   cue=cues.get(identity,{}).get(str(i));matched=bool(cue and (cue['person'],cue['text'])==tuple(p[:2]))
   rows.append(dict(identity=identity,index=i,person=p[0],text=p[1],packet=list(p),reviewed=matched,category=classify(identity,i,p,people,direction),review_alias=identity.startswith('topic:review:'),pov_sensitive=p[0] in ('dad','daram'),application_status=cue.get('application_status','reviewed') if matched else 'context_review_pending',context_before=[list(x) for x in packets[max(0,i-2):i]],context_after=[list(x) for x in packets[i+1:i+3]]))
 calls=[]
 for f in (ROOT/'game').rglob('*.rpy'):
  if 'qa_tests' in f.parts:continue
  for n,line in enumerate(f.read_text().splitlines(),1):
   if re.search(r'\b(?:call\s+)?r13_lines\(',line):calls.append({'file':str(f.relative_to(ROOT)),'line':n,'call':line.strip()})
 counts=collections.Counter(r['person'] for r in rows if r['person'])
 summary=dict(static_scenes=len(scenes),static_rows=len(rows),unique_speaker_text_pairs=len({(r['person'],r['text']) for r in rows}),registered_art_people=len(people),static_speakers=len(counts),per_person=dict(counts),registered_people_without_static_lines=sorted(set(people)-set(counts)),reviewed_rows=sum(r['reviewed'] for r in rows),runtime_art_ready=len(json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']),scope_limit='Static scene_rows excludes dynamically constructed lines and init-added topics; callsite list is a separate review queue. topic:review duplicates topic content.',callsites=len(calls))
 summary['categories_occurrences']=dict(collections.Counter(r['category'] for r in rows))
 summary['categories_excluding_review_aliases']=dict(collections.Counter(r['category'] for r in rows if not r['review_alias']))
 candidates=[r for r in rows if r['category']=='dialogue_expression_candidate']
 summary['expression_candidates_reviewed']=sum(r['reviewed'] for r in candidates)
 summary['expression_candidates_pending']=sum(not r['reviewed'] for r in candidates)
 summary['expression_candidates_pending_excluding_review_aliases']=sum(not r['reviewed'] and not r['review_alias'] for r in candidates)
 summary['pov_note']='Dad is default player; Daram may become POV in episode 2. These are static candidates, not guaranteed visible portraits. Dynamic packet transforms, meetings, and scene camera need runtime reconciliation.'
 summary['reviewed_authored_action_rows']=[{'identity':r['identity'],'index':r['index']} for r in rows if r['reviewed'] and r['category']=='authored_action_separate_review']
 out=ROOT/'docs/reviews/dialogue-beats';out.mkdir(parents=True,exist_ok=True)
 for name,data in [('inventory',rows),('summary',summary),('callsites',calls)]:
  (out/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 return summary
if __name__=='__main__':print(json.dumps(inventory(),ensure_ascii=False,indent=2))
