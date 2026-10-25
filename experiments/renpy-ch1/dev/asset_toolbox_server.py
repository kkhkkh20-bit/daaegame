"""Local-only asset catalog editor. Run through asset_toolbox.py serve."""
from copy import deepcopy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
import mimetypes
import os
from pathlib import Path
import secrets
import tempfile
import threading
from urllib.parse import unquote, urlsplit


def run(project: Path, host='127.0.0.1', port=8787):
    if host not in ('127.0.0.1', 'localhost', '::1'):
        raise ValueError('에셋 도구함은 로컬 주소에서만 실행할 수 있습니다.')
    project=Path(project).resolve()
    if not (project/'game').is_dir():
        project=project/'experiments/renpy-ch1'
    game=project/'game'
    directory=game/'asset-toolbox'
    token=secrets.token_urlsafe(32)
    lock=threading.Lock()
    module_path=game/'python-packages/r13_assets.py'
    index=Path(__file__).with_name('asset-toolbox')/'index.html'

    def registry(catalog, bindings):
        spec=importlib.util.spec_from_file_location('r13_assets_toolbox',module_path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Registry(catalog,bindings)

    def read():
        return tuple(json.loads((directory/name).read_text(encoding='utf-8'))
                     for name in ('catalog.json','bindings.json'))

    def asset_path(relative):
        if not isinstance(relative,str) or not relative.startswith('assets/'):
            raise ValueError('이미지는 game/assets 아래 경로여야 합니다.')
        path=(game/relative).resolve()
        if not path.is_relative_to((game/'assets').resolve()) or not path.is_file():
            raise ValueError('에셋 파일이 없거나 허용 범위 밖의 경로입니다: '+relative)
        return path

    def inspect(catalog, bindings):
        errors=[]; resolved={}
        for asset_id,asset in catalog.get('assets',{}).items():
            try:
                asset_path(asset['path'])
                tags=asset.get('tags',[])
                if not isinstance(tags,list) or any(not isinstance(t,str) or not t.strip() for t in tags):
                    raise ValueError('태그는 빈 값 없는 문자열 목록이어야 합니다.')
                size=asset.get('size')
                if asset.get('media') in ('audio','font') or Path(asset['path']).suffix.lower() in ('.ogg','.mp3','.wav','.opus','.flac','.ttf','.otf','.woff','.woff2'):
                    continue
                if not isinstance(size,list) or len(size)!=2 or any(type(v) is not int or v<=0 for v in size):
                    raise ValueError('size는 양수 정수 두 개여야 합니다.')
                render=asset.get('render',{})
                crop=render.get('crop')
                if crop is not None:
                    if not isinstance(crop,list) or len(crop)!=4 or any(type(v) is not int for v in crop):
                        raise ValueError('crop은 정수 [x,y,너비,높이]여야 합니다.')
                    x,y,w,h=crop
                    if min(x,y)<0 or min(w,h)<=0 or x+w>size[0] or y+h>size[1]:
                        raise ValueError('crop이 원본 이미지 범위를 벗어났습니다.')
                frame=render.get('frame')
                if frame is not None:
                    if not isinstance(frame,list) or len(frame) not in (2,4) or any(type(v) is not int or v<0 for v in frame):
                        raise ValueError('frame은 음수가 아닌 정수 2개 또는 4개여야 합니다.')
                    borders=frame*2 if len(frame)==2 else frame
                    w,h=crop[2:] if crop else size
                    if borders[0]+borders[2]>w or borders[1]+borders[3]>h:
                        raise ValueError('frame 테두리가 이미지 범위를 벗어났습니다.')
                zoom=render.get('zoom',1)
                if type(zoom) not in (int,float) or not 0<zoom<=100:
                    raise ValueError('zoom은 0보다 큰 유한한 수여야 합니다.')
            except (ValueError,KeyError,TypeError) as exc:
                errors.append({'scope':asset_id,'message':str(exc)})
        try:
            model=registry(catalog,bindings)
            errors.extend({'scope':'연결 검증','message':message} for message in model.validate())
            for role,binding in bindings.get('bindings',{}).items():
                resolved[role]={}
                for state in dict.fromkeys(list(binding.get('states',['basic']))+list(binding.get('fallback',{}))):
                    try:
                        resolved[role][state]=model.resolve(role,state)
                    except Exception as exc:
                        if state in binding.get('states',['basic']):
                            errors.append({'scope':role+'/'+state,'message':str(exc)})
                        resolved[role][state]={'error':str(exc)}
        except Exception as exc:
            errors.append({'scope':'registry','message':str(exc)})
        return resolved,errors

    def write(name,value):
        directory.mkdir(parents=True,exist_ok=True)
        filename=None
        try:
            with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=directory,
                                             prefix='.'+name+'.',delete=False) as stream:
                filename=stream.name
                json.dump(value,stream,ensure_ascii=False,indent=2,allow_nan=False)
                stream.write('\n');stream.flush();os.fsync(stream.fileno())
            os.replace(filename,directory/name)
        finally:
            if filename and os.path.exists(filename):os.unlink(filename)

    class Handler(BaseHTTPRequestHandler):
        def allowed_host(self):
            expected={f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}',f'[::1]:{self.server.server_port}'}
            return self.headers.get('Host','') in expected

        def send(self,status,value,content_type='application/json; charset=utf-8'):
            data=json.dumps(value,ensure_ascii=False,allow_nan=False).encode() if content_type.startswith('application/json') else value
            self.send_response(status)
            self.send_header('Content-Type',content_type)
            self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
            self.end_headers();self.wfile.write(data)

        def snapshot(self):
            try:
                catalog,bindings=read()
                resolved,errors=inspect(catalog,bindings)
                return dict(catalog=catalog,bindings=bindings,resolved=resolved,errors=errors,token=token)
            except Exception as exc:
                return dict(catalog={'assets':{}},bindings={'bindings':{}},resolved={},
                            errors=[{'scope':'초기화','message':str(exc)}],token=token)

        def do_GET(self):
            if not self.allowed_host():return self.send(403,{'error':'로컬 Host만 허용합니다.'})
            path=unquote(urlsplit(self.path).path)
            if path=='/':
                return self.send(200,index.read_bytes(),'text/html; charset=utf-8')
            if path=='/api/catalog':
                with lock:payload=self.snapshot()
                return self.send(200,payload)
            if path.startswith('/assets/'):
                try:
                    target=asset_path(path[1:])
                    if target.suffix.lower() not in ('.png','.jpg','.jpeg','.webp','.gif','.svg','.avif','.ogg','.mp3','.wav','.opus','.flac','.ttf','.otf','.woff','.woff2'):
                        raise ValueError('등록 가능한 이미지·소리·글꼴 형식만 열 수 있습니다.')
                    return self.send(200,target.read_bytes(),mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
                except (ValueError,OSError):pass
            self.send(404,{'error':'파일을 찾을 수 없습니다.'})

        def do_POST(self):
            origin=self.headers.get('Origin')
            expected='http://'+self.headers.get('Host','')
            if (not self.allowed_host() or (origin is not None and origin!=expected)
                or self.headers.get('Sec-Fetch-Site') in ('cross-site','same-site')
                or not secrets.compare_digest(self.headers.get('X-Asset-Token',''),token)):
                return self.send(403,{'error':'이 도구함에서 시작한 로컬 요청만 저장할 수 있습니다.'})
            if self.headers.get('Content-Type','').split(';')[0]!='application/json':
                return self.send(415,{'error':'JSON 요청만 허용합니다.'})
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=262144:raise ValueError('요청 크기가 올바르지 않습니다.')
                body=json.loads(self.rfile.read(length))
                if not isinstance(body,dict):raise ValueError('JSON 객체가 필요합니다.')
                with lock:
                    catalog,bindings=deepcopy(read())
                    path=urlsplit(self.path).path
                    if path=='/api/assign':
                        role=body['role'];asset_id=body['asset_id']
                        model=registry(catalog,bindings)
                        model.assign(role,asset_id)
                        name='bindings.json';value=bindings
                    elif path=='/api/tags':
                        tags=body['tags']
                        if not isinstance(tags,list) or any(not isinstance(t,str) or not t.strip() or len(t)>180 for t in tags):
                            raise ValueError('태그는 180자 이내의 비어 있지 않은 문자열 목록이어야 합니다.')
                        registry(catalog,bindings).set_tags(body['asset_id'],list(dict.fromkeys(t.strip() for t in tags)))
                        name='catalog.json';value=catalog
                    else:return self.send(404,{'error':'알 수 없는 저장 동작입니다.'})
                    _,errors=inspect(catalog,bindings)
                    if errors:return self.send(422,{'error':'검증 오류가 있어 저장하지 않았습니다.','errors':errors})
                    write(name,value)
                    payload=self.snapshot()
                return self.send(200,payload)
            except (ValueError,KeyError,TypeError,OSError) as exc:
                return self.send(422,{'error':str(exc)})
            except Exception as exc:
                return self.send(422,{'error':str(exc)})

    server_type=ThreadingHTTPServer
    if host=='::1':
        import socket
        class IPv6Server(ThreadingHTTPServer):address_family=socket.AF_INET6
        server_type=IPv6Server
    server=server_type((host,port),Handler)
    print('에셋 도구함: http://{}:{}/'.format('['+host+']' if ':' in host else host,server.server_port),flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
