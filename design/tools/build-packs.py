"""Package the exact manifest assets without changing any image pixels."""
from pathlib import Path
import json,zipfile
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'manifest.json').read_text())
chars={root/c['src'] for c in m['characters'].values()}
backgrounds={root/b['src'] for b in m['backgrounds'].values()}
code={p for p in root.iterdir() if p.suffix in ['.html','.js','.css','.json','.txt']}
code.update(p for p in (root/'reference').iterdir() if p.is_file())
code.update(p for p in (root/'tools').iterdir() if p.suffix in ['.py','.cjs'])
code.update((root/'background-results').glob('*.json'))
code.update((root/'character-results-v4').glob('*.json'))
# Keep full-resolution PNGs intact; split large character delivery into two archives.
ordered_chars=sorted(chars-code)
mid=(len(ordered_chars)+1)//2
char_first=set(ordered_chars[:mid]);char_second=set(ordered_chars[mid:])
for name,paths in [('daram-design-pack.zip',code|char_first),('daram-characters-part2.zip',char_second),('daram-backgrounds-pack.zip',backgrounds)]:
 with zipfile.ZipFile(root/name,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(paths):
   assert p.is_file(),p
   z.write(p,'design/'+str(p.relative_to(root)))
 size=(root/name).stat().st_size
 assert size<95*1024*1024,(name,'exceeds safe repository file size')
 print(name,round(size/1024/1024,2),'MiB',len(paths),'files')
