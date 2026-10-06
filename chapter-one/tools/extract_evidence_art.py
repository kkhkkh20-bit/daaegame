"""Reuse the original evIcon function; scene items use actual scene crops in CSS."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1];src=(root.parent/'game.html').read_text();start=src.index('function evIcon(id){');end=src.index('\n}',start)+2;fn=src[start:end]
adapter=(root/'tools/evidence-art-adapter.js').read_text();(root/'evidence-art.js').write_text('/* Original evIcon from game.html; see evidence-art-provenance.json. */\n(()=>{\n'+fn+'\n'+adapter+'\n})();\n')
(root/'evidence-art-provenance.json').write_text(json.dumps({'source':'game.html','function':'evIcon','sha256':hashlib.sha256(fn.encode()).hexdigest(),'line':src[:start].count('\n')+1},indent=2)+'\n')
