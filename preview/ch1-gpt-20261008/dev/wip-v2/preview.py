"""Serve the isolated v2 build with existing preview assets, without deploying."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse

SOURCE = Path(__file__).resolve().parent
ASSETS = SOURCE.parent.parent

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ASSETS), **kwargs)

    def translate_path(self, path):
        name = path.split('?', 1)[0]
        if name in ('/', '/play_v2.html', '/playT.html'):
            return str(SOURCE / 'build' / ('playT.html' if name == '/playT.html' else 'play_v2.html'))
        return super().translate_path(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    print(f'v2 preview: http://127.0.0.1:{args.port}/play_v2.html', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
