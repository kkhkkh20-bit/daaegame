"""Fetch pinned recording data outside Git; never ship the instrument libraries.

python3 gen/fetch_piano_samples.py
Optional location: DAAE_INSTRUMENT_CACHE=/some/cache
Only data files are extracted; Debian package scripts are not executed.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import subprocess
import urllib.parse
import urllib.request

CACHE = Path(os.environ.get('DAAE_INSTRUMENT_CACHE', '/workspace/.daaegame-instruments'))
REV = '3382bf9496bba2486f5ab0de55a264d1dfc38404'
REPO = 'sfzinstruments/SalamanderGrandPiano'
LAYERS = (4, 8, 12)
CENTERS = range(30, 88, 3)
NAMES = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

def filename(center, layer):
    return f'{NAMES[center % 12]}{center // 12 - 1}v{layer}.flac'

def download(url, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as response, path.with_suffix(path.suffix+'.part').open('wb') as out:
        while chunk := response.read(1024 * 1024):
            out.write(chunk)
    path.with_suffix(path.suffix+'.part').replace(path)

def main():
    base = CACHE/'salamander'
    with urllib.request.urlopen(f'https://api.github.com/repos/{REPO}/git/trees/{REV}?recursive=1', timeout=30) as response:
        tree = json.load(response)
    assert not tree.get('truncated')
    blobs = {x['path']: x for x in tree['tree'] if x['type']=='blob'}
    paths = ['LICENSE', 'README.md', 'Data/tune_ret.txt', 'Data/region.txt']
    paths += [f'Data/vel_{v:02d}.txt' for v in LAYERS]
    paths += ['Samples/'+filename(c,v) for c in CENTERS for v in LAYERS]
    def get(name):
        target = base/name
        if not target.exists():
            download(f'https://raw.githubusercontent.com/{REPO}/{REV}/'+urllib.parse.quote(name), target)
        data = target.read_bytes()
        sha = hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()
        assert sha == blobs[name]['sha'], f'Unexpected sample contents: {name}'
        return {'file': name, 'git_blob': sha, 'bytes': len(data)}
    with ThreadPoolExecutor(max_workers=6) as executor:
        manifest = list(executor.map(get, paths))
    (base/'manifest.json').write_text(json.dumps({'revision':REV,'files':manifest},indent=2)+'\n')
    print(f'Verified {len(manifest)} piano recording/data files from pinned revision {REV}', flush=True)
    deb = CACHE/'fluid-soundfont-gm_3.1-6_all.deb'
    sf = CACHE/'fluid/usr/share/sounds/sf2/FluidR3_GM.sf2'
    if not sf.exists():
        if not deb.exists():
            download('https://deb.debian.org/debian/pool/main/f/fluid-soundfont/'+deb.name, deb)
        subprocess.run(['dpkg-deb','-x',str(deb),str(CACHE/'fluid')],check=True)
    assert sf.stat().st_size > 100_000_000
    print('Orchestral SoundFont ready:',sf,flush=True)
    print('Debian package SHA256:',hashlib.sha256(deb.read_bytes()).hexdigest(),flush=True)

if __name__ == '__main__':
    main()
