"""Attach read-only UI to a regenerated capture report without rewriting its evidence."""
from pathlib import Path
import shutil

def install(repo):
    target=Path(repo)/'reports/place-balance-01936'
    page=target/'index.html'
    if not page.exists():return
    html=page.read_text()
    if 'name="viewport"' not in html:
        html=html.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',1)
    if '<html' not in html:html=html.replace('<!doctype html>','<!doctype html><html lang="ko">',1)
    if 'src="ui.js"' not in html:
        html=html.replace('</style>','</style><link rel="stylesheet" href="ui.css"><link rel="stylesheet" href="../../preview/resource-dashboard/viewer.css"><script src="../../preview/resource-dashboard/viewer.js" defer></script><script src="ui.js" defer></script>',1)
    if html!=page.read_text():page.write_text(html)
    for source in (Path(__file__).parent/'gallery').iterdir():shutil.copy2(source,target/source.name)
