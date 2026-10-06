"""Build a portable HTML with local art embedded; no CDN or API calls."""
from pathlib import Path
import base64,json
root=Path(__file__).resolve().parent
def uri(p):
 return 'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
art={p.stem:uri(p) for p in (root/'assets').glob('*.png')}
css=(root/'style.css').read_text().replace('assets/reception.png',art['reception'])

html=(root/'index.html').read_text().replace('<link rel="stylesheet" href="style.css">','<style>'+css+'</style>')
script='window.ART='+json.dumps(art)+';\n'+(root/'boot.js').read_text()+'\n'+(root/'story.js').read_text()+'\n'+(root/'game.js').read_text()
html=html.replace('<script src="boot.js"></script><script src="story.js" onerror="chapterLoadError()"></script><script src="game.js" onerror="chapterLoadError()"></script>','<script>'+script.replace('</script','<\\/script')+'</script>')
(root/'play.html').write_text(html)
print('Built chapter-one/play.html (portable, self-contained)')
