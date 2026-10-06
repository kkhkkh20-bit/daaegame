"""Optional desktop-only single HTML. Mobile uses the hosted modular index.html."""
from pathlib import Path
import base64,json,re
root=Path(__file__).resolve().parent
art={p.stem:'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode() for p in (root/'assets').glob('*.png')}
def inline_css(name):
    css=(root/name).read_text()
    css=re.sub(r'url\(assets/([\w-]+)\.png\)',lambda m:'url('+art[m[1]]+')',css)
    return css.replace('url(assets/galmuri11.woff2)', 'url(data:font/woff2;base64,'+base64.b64encode((root/'assets/galmuri11.woff2').read_bytes()).decode()+')')
html=(root/'index.html').read_text()
html=re.sub(r'<link rel="stylesheet" href="([\w-]+\.css)(?:\?[^"]*)?">',lambda m:'<style>'+inline_css(m[1])+'</style>',html)
parts=re.findall(r'<script src="([\w-]+\.js)(?:\?[^"]*)?"[^>]*></script>',html)
script='window.ART='+json.dumps(art)+';\n'+'\n'.join((root/p).read_text() for p in parts)
html=re.sub(r'<script src="[\w-]+\.js(?:\?[^"]*)?"[^>]*></script>','',html).replace('</body>','<script>'+script.replace('</script','<\\/script')+'</script></body>')
(root/'play.html').write_text(html)
print('Built optional desktop chapter-one/play.html; mobile entry is index.html')
