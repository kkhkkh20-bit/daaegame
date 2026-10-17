"""Temporary lint hook against the real final-init store. Never ships the hook."""
import os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
hook=ROOT/'game/zz_dialogue_binding_probe.rpy'
assert not hook.exists(), 'Do not overwrite an existing hook'
try:
 hook.write_text((ROOT/'dev/dialogue_provider_probe.rpy.txt').read_text())
 env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy')
 result=subprocess.run([sys.argv[1],str(ROOT),'lint'],env=env,capture_output=True,text=True)
 (ROOT/'docs/reviews/dialogue-beats/provider-lint-results.txt').write_text(result.stdout+result.stderr)
 import json
 data=json.loads((ROOT/'docs/reviews/dialogue-beats/provider-state-results.json').read_text())
 print('Provider cases:',data['cases'],'unresolved:',len(data['unresolved']))
 if data['unresolved']:print(json.dumps(data['unresolved'],ensure_ascii=False,indent=2))
 assert result.returncode==0 and not data['unresolved']
finally:
 hook.unlink(missing_ok=True);hook.with_suffix('.rpyc').unlink(missing_ok=True)
