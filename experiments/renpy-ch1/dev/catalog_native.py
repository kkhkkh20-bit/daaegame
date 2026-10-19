"""Add real folder/profile navigation to generated native card clicks (still unrun)."""
import ast
from pathlib import Path

def rewrite_catalog_clicks(path):
    ns={}
    for name in ('recommended_model.py','recommended_opening_model.py','recommended_ep23_model.py','recommended_ep456_model.py'):
        exec((Path(__file__).parent/name).read_text(),ns)
    captions={v[0]:k for k,v in ns['r13_rec_cards'].items()}
    identities={key:(kind,title) for kind,title,keys in ns['r13_rec_identity_groups'].values() for key in keys}
    result=[]
    for line in path.read_text().splitlines():
        stripped=line.strip()
        if stripped.startswith('click '):
            try:caption=ast.literal_eval(stripped[6:])
            except (ValueError,SyntaxError):caption=None
            key=captions.get(caption)
            if key:
                folder=ns['r13_rec_card_episode'](key);kind,title=identities[key]
                result.extend(['    click '+repr('메인' if folder==0 else '사건 %d'%folder),
                    '    click '+repr('인물' if kind=='person' else '자료 · 현장'),
                    '    click '+repr(title)])
        result.append(line)
    path.write_text('\n'.join(result)+'\n')
