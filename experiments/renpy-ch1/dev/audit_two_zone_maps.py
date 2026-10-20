"""Read-only inventory: authored art, world coordinates and two-view shortfall."""
import ast
import json
import re
import textwrap
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def inventory():
    places = {}
    for path in sorted((ROOT/'game').rglob('*.rpy')):
        text = path.read_text()
        for match in re.finditer(r'^init[^\n]*python[^\n]*:\n((?:[ \t].*\n|\n)+)', text, re.M):
            try: tree = ast.parse(textwrap.dedent(match[1]))
            except SyntaxError: continue
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == 'R13_PLACES':
                            places.update(ast.literal_eval(node.value))
                        elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and target.value.id == 'R13_PLACES':
                            places[ast.literal_eval(target.slice)] = ast.literal_eval(node.value)
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                    call = node.value
                    if isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name) and call.func.value.id == 'R13_PLACES' and call.func.attr == 'update':
                        if call.args: places.update(ast.literal_eval(call.args[0]))
                        places.update({kw.arg:ast.literal_eval(kw.value) for kw in call.keywords})
    layouts=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())
    result=[]
    for location,(name,background) in sorted(places.items()):
        spec=layouts.get(location,{})
        width=spec.get('width',1280)
        files=spec.get('files',{})
        paths=set(files.values())
        for state in spec.get('state_files',{}).values(): paths.update(state.values())
        if not spec:
            if location == 'guestroom':
                paths.update('assets/room13-pixel-room-before-'+period+'.webp' for period in ('morning','afternoon','evening'))
            elif location in ('ms14_somi','ms14_guardroom'):
                paths.update(layouts['gate']['files'].values())
            elif location == 'ms14_stable':paths.add('assets/room13-pixel-wide-stable-afternoon.webp')
            elif location == 'ms14_somi_inside':paths.add('assets/room13-pixel-wide-somi-home-afternoon.webp')
        sources=[]
        for file in sorted(paths):
            with Image.open(ROOT/'game'/file) as image: size=list(image.size)
            sources.append(dict(file=file,native_size=size))
        result.append(dict(location=location,name=name,scene_key=background,width=width,height=720,
            endpoint_offsets=[0,max(0,width-1280)],overlap=max(0,2560-width),missing_width=max(0,2560-width),
            periods=spec.get('periods',['morning','afternoon','evening']),
            initial_x=spec.get('initial_x',0),sources=sources,objects=spec.get('objects',{}),
            late_objects=spec.get('late_objects',{}),slots=spec.get('slots',[]),
            requires_new_art=True,note='No panorama; existing scene fallback' if not spec else 'Existing continuous source; fewer than two full views'))
    return result

if __name__=='__main__':
    print(json.dumps(inventory(),ensure_ascii=False,indent=2))
