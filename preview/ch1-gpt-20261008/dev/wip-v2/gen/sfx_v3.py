"""Build sampled chapter SFX; no synthesized oscillator or pitched bell.

Sources are existing game sound assets, with explicit per-asset media licenses.
Their recording sessions/equipment have not been independently verified.
Requires NumPy, SciPy and ffmpeg. Run from any directory; downloads are checked
against content hashes and retained with source license/attribution documents.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import urllib.request
import wave

import numpy as np
from scipy import signal


OUT = Path(__file__).resolve().parents[3] / 'audio/v3/sfx'
RATE = 44100
ASSETS = {
    'horse': {
        'url': 'https://raw.githubusercontent.com/0ad/0ad/master/binaries/data/mods/public/audio/actor/mounted/movement/mstep113.ogg',
        'sha256': 'e069e264983fa31700cf73aea6fc905790184d9d2b49d0f1327cd7ba162a6dfe',
        'author': 'Wildfire Games',
        'license': 'CC BY-SA 3.0',
        'license_url': 'https://creativecommons.org/licenses/by-sa/3.0/',
        'page': 'https://github.com/0ad/0ad/blob/master/binaries/data/mods/public/audio/actor/mounted/movement/mstep113.ogg',
    },
    'open': {
        'url': 'https://raw.githubusercontent.com/minetest/minetest_game/master/mods/doors/sounds/doors_door_open.ogg',
        'sha256': 'e256ed15794ef17a6a2df0c9a79b97e1e8e8d697ab063b4870a752ed4b791a73',
        'author': 'CGEffex; modified by BlockMen',
        'license': 'CC BY 3.0',
        'license_url': 'https://creativecommons.org/licenses/by/3.0/',
        'page': 'https://github.com/minetest/minetest_game/blob/master/mods/doors/sounds/doors_door_open.ogg',
    },
    'close': {
        'url': 'https://raw.githubusercontent.com/minetest/minetest_game/master/mods/doors/sounds/doors_door_close.ogg',
        'sha256': 'e556561e8463491639a59f5cebe2cbc7c9ee6967a9c2faf8f3df90a1931483d6',
        'author': 'bennstir',
        'license': 'CC BY 3.0',
        'license_url': 'https://creativecommons.org/licenses/by/3.0/',
        'page': 'https://github.com/minetest/minetest_game/blob/master/mods/doors/sounds/doors_door_close.ogg',
    },
}
DOCUMENTS = {
    '0AD-AUDIO-LICENSE.txt': 'https://raw.githubusercontent.com/0ad/0ad/master/binaries/data/mods/public/audio/LICENSE.txt',
    'MINETEST-DOORS-README.md': 'https://raw.githubusercontent.com/minetest/minetest_game/master/mods/doors/README.md',
    'MINETEST-DOORS-LICENSE.txt': 'https://raw.githubusercontent.com/minetest/minetest_game/master/mods/doors/license.txt',
    '0AD-HORSE-WALK.xml': 'https://raw.githubusercontent.com/0ad/0ad/master/binaries/data/mods/public/audio/actor/mounted/movement/walk.xml',
}


def fetch(url, path, digest=None):
    if not path.exists():
        path.write_bytes(urllib.request.urlopen(url, timeout=25).read())
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest and actual != digest:
        raise ValueError('Source hash changed: ' + str(path))
    return actual


def decode(path):
    raw = subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', str(path), '-ar', str(RATE), '-ac', '1',
        '-f', 'f32le', 'pipe:1'])
    return np.frombuffer(raw, np.float32).copy()


def soften(a, cutoff):
    # Static EQ and gain, with no pitch/time-stretching or new tonal layers.
    a = signal.sosfilt(signal.butter(2, 45, fs=RATE, btype='highpass', output='sos'), a)
    return signal.sosfilt(signal.butter(2, cutoff, fs=RATE, output='sos'), a)


def fade(a, attack=.003, release=.035):
    a = a.copy()
    start, end = min(len(a), round(attack*RATE)), min(len(a), round(release*RATE))
    a[:start] *= np.linspace(0, 1, start)
    a[-end:] *= np.linspace(1, 0, end)
    return a


def save(name, a, source_key, modifications, loop=False):
    assert np.isfinite(a).all()
    a *= .48 / max(.001, float(np.max(np.abs(a))))
    pcm = np.round(a*32767).astype('<i2')
    path = OUT/name
    with wave.open(str(path), 'wb') as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(RATE)
        output.writeframes(pcm.tobytes())
    source = ASSETS[source_key]
    result = {
        'file': name, 'duration_seconds': len(a)/RATE, 'sample_rate': RATE,
        'channels': 1, 'peak_dbfs': float(20*np.log10(max(np.max(abs(a)), 1e-10))),
        'rms_dbfs': float(20*np.log10(max(np.sqrt(np.mean(a*a)), 1e-10))),
        'clipped_samples': int(np.sum(abs(a) >= 1)),
        'loop': loop, 'loop_start_seconds': 0 if loop else None,
        'loop_end_seconds': len(a)/RATE if loop else None,
        'boundary_jump': float(abs(a[0]-a[-1])),
        'source': source, 'modifications': modifications,
        'license': source['license'], 'license_url': source['license_url'],
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    }
    if loop:
        result.update({'beat_period_seconds': .6, 'beats_per_loop': 2,
                       'impact_peak_seconds': [.09,.69],
                       'runtime_fade_in_seconds': .12,
                       'runtime_fade_out_seconds': .3,
                       'single_source_required': True})
    return result


def main():
    source_dir = OUT/'source'
    source_dir.mkdir(parents=True, exist_ok=True)
    for key, metadata in ASSETS.items():
        fetch(metadata['url'], source_dir/(key+'.ogg'), metadata['sha256'])
    documents = []
    for name, url in DOCUMENTS.items():
        digest = fetch(url, source_dir/name)
        documents.append({'file': 'source/'+name, 'url': url, 'sha256': digest})
    horse = soften(decode(source_dir/'horse.ogg'), 3000)
    loop = np.zeros(round(1.2*RATE), np.float64)
    # Two different recorded hoof impacts, separated by a clear 0.6-second beat.
    # The original asset has peaks near .37/.93/1.49 seconds; do not duplicate
    # a whole running clip over a separate synthetic clop scheduler.
    for source_start, target_start in [(.32,.04), (.88,.64)]:
        clip = fade(horse[round(source_start*RATE):round((source_start+.39)*RATE)])
        offset = round(target_start*RATE)
        loop[offset:offset+len(clip)] += clip
    rows = [save('horse-carriage-loop.wav', loop, 'horse',
                 'Two recorded impact excerpts (.32-.71s, .88-1.27s), placed at .04/.64s in a 1.2s two-beat loop; 45Hz high-pass/3kHz low-pass; 3ms attack/35ms release; fixed gain. No pitch shift.', True)]
    for key in ('open','close'):
        a = fade(soften(decode(source_dir/(key+'.ogg')), 3500), .002, .035)
        rows.append(save('wood-door-'+key+'.wav', a, key,
                         'Mono 44.1kHz PCM conversion; 45Hz high-pass/3.5kHz low-pass; 2ms attack/35ms release; fixed peak gain. Original timing retained; no bell, pitch shift or extra synthesized layer.'))
    manifest = {'version': 1, 'assets': rows, 'source_documents': documents,
                'listening_status': 'No direct listening tool was available. Source attribution, decoded waveforms, impact timing, clipping, spectral energy and output files were checked; human listening is still possible via these WAV files.'}
    (OUT/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    credits = ['Chapter-one v3 sampled sound effects', '',
               'These are adaptations of existing game audio assets, not new oscillator synthesis.',
               'Original recording sessions/equipment are not independently verified.',
               'No claim of direct listening is made by this build.', '',
               'horse-carriage-loop.wav',
               'Original author: Wildfire Games (Copyright 2009).',
               'Source: '+ASSETS['horse']['page'],
               'Author site: https://www.wildfiregames.com/',
               'License: CC BY-SA 3.0 — https://creativecommons.org/licenses/by-sa/3.0/',
               'This adapted horse audio is distributed under CC BY-SA 3.0.',
               'Changes: two impact excerpts, two-beat edit, EQ, fades, gain, WAV conversion.', '']
    for key in ('open','close'):
        x = ASSETS[key]
        credits += ['wood-door-'+key+'.wav', 'Original author: '+x['author']+'.',
                    'Source: '+x['page'],
                    'License: CC BY 3.0 — https://creativecommons.org/licenses/by/3.0/',
                    'Changes: EQ, short fades, gain, mono 44.1kHz WAV conversion; timing retained.', '']
    credits += ['Attribution/license evidence is retained in source/ alongside the original OGGs.',
                'The credits above accompany these files; no endorsement by the original authors is implied.',
                'This notice covers the sound assets only; the game and its other assets retain their own licenses.',
                'Rebuild: python3 dev/wip-v2/gen/sfx_v3.py; source audio is pinned by SHA-256.']
    (OUT/'SFX_CREDITS.txt').write_text('\n'.join(credits)+'\n')
    for row in rows:
        print(row['file'], round(row['duration_seconds'],6),
              round(row['peak_dbfs'],2), round(row['rms_dbfs'],2), row['clipped_samples'])


if __name__ == '__main__':
    main()
