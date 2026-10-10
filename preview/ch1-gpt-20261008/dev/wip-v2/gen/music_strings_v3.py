"""Restrained non-piano score. Original, grid-aligned cello/string parts.

Uses the existing FluidR3 cache and mixing helpers. No piano samples or lane 0.
Render once; ordinary build/publish uses the checked-in MP3s and manifest.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile

import numpy as np
from scipy import signal
from scipy.io import wavfile
from music_piano_v2 import RATE, SF, orchestral, fold, room, periodic_filter, loudness

SOURCE = Path(__file__).resolve().parents[1]
OUT = SOURCE.parent.parent / 'audio/v3'
CHORDS = [([50, 57, 62], [53, 57, 62]),
          ([46, 53, 58], [53, 58, 62]),
          ([53, 60, 65], [53, 57, 60]),
          ([48, 55, 60], [52, 55, 60])]
TRACKS = {
    'title': ('inn_title', 72, 'quiet'),
    'travel': ('inn_travel', 76, 'warm'),
    'investigation': ('inn_inv', 80, 'investigation'),
    'serious': ('inn_serious', 64, 'quiet'),
    'meeting': ('inn_meet', 88, 'meeting'),
    'meeting-press': ('inn_meet_press', 104, 'press'),
    'climax': ('inn_climax', 96, 'meeting'),
    'climax-press': ('inn_climax_press', 112, 'press'),
    'after': ('inn_after', 72, 'warm'),
}


def score(bpm, style):
    beat = 60 / bpm
    events = []
    # Exactly 4/4, chord changes every two bars. No swing or timing jitter.
    order = [2, 3, 0, 1] if style == 'warm' else [0, 1, 2, 3]
    for bar in range(16):
        roots, chord = CHORDS[order[(bar // 2) % 4]]
        at = bar * 4 * beat
        if bar % 2 == 0:
            events.append((at, 1, roots[0], 8 * beat - .6, 27))
            for note in chord:
                events.append((at, 2, note, 8 * beat - .6, 24))
        if style != 'quiet':
            beats = (0, 1, 2, 3) if style == 'press' else (0, 2)
            velocity = {'warm': 15, 'investigation': 19,
                        'meeting': 26, 'press': 31}[style]
            for i, offset in enumerate(beats):
                events.append((at + offset * beat, 5, roots[i % 2], .45 * beat, velocity))
        # A short chord-tone phrase with space between statements, never a
        # separate chromatic melody fighting the accompaniment.
        if style in ('quiet', 'warm') and bar % 4 == 0:
            events.append((at + 2 * beat, 2, chord[2] + 12, 2 * beat, 20))
    return sorted(events), 16 * 4 * beat


def render(name, key, bpm, style):
    events, seconds = score(bpm, style)
    frames = round(seconds * RATE)
    print('Rendering', name, bpm, 'BPM', len(events), 'notes', flush=True)
    mix = fold(orchestral(events, frames + 6 * RATE), frames)
    mix = periodic_filter(mix, signal.butter(2, 75, fs=RATE, btype='highpass', output='sos'))
    mix = periodic_filter(mix, signal.butter(2, 4700, fs=RATE, output='sos'))
    mix = room(mix, .13, .9, 151)
    assert np.isfinite(mix).all()
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / 'strings.wav'
        wavfile.write(raw, RATE, mix.astype(np.float32))
        measured = loudness(raw)
        target = -24 if style == 'quiet' else -23
        gain_db = min(target - float(measured['input_i']), -3.5 - float(measured['input_tp']))
        mix *= 10 ** (gain_db / 20)
        wavfile.write(raw, RATE, mix.astype(np.float32))
        path = OUT / f'{name}-strings-v3.mp3'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(raw),
                        '-codec:a', 'libmp3lame', '-b:a', '192k',
                        '-metadata', f'title=daaegame {name} strings', str(path)], check=True)
    return {'name': name, 'key': key, 'bpm': bpm, 'bars': 16,
            'seconds': frames / RATE, 'file': path.name,
            'instruments': ['cello', 'string ensemble', 'pizzicato strings'],
            'beatsPerBar': 4, 'gridOnly': True,
            'notes': [{'at': round(at, 6), 'lane': lane, 'midi': n,
                       'duration': round(dur, 6), 'velocity': v}
                      for at, lane, n, dur, v in events],
            'integrated_lufs': round(float(measured['input_i']) + gain_db, 2),
            'true_peak_db': round(float(measured['input_tp']) + gain_db, 2),
            'loop_boundary_jump': float(np.max(np.abs(mix[0] - mix[-1]))),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    assert SF.exists(), 'Prepare the existing FluidR3 instrument cache first'
    OUT.mkdir(parents=True, exist_ok=True)
    tracks = [render(name, *settings) for name, settings in TRACKS.items()]
    (OUT / 'score-strings-v3.json').write_text(json.dumps(tracks, indent=2) + '\n')
    manifest = {t['key']: {'bpm': t['bpm'], 'vol': .8, 'prog': ['Dm'], 'mel': [],
                          'media': 'audio/v3/' + t['file'], 'loopSeconds': t['seconds']}
                for t in tracks}
    manifest['inn_cold'] = manifest['inn_serious'].copy()
    for character in ['seryeon', 'nabi', 'bami', 'doto', 'buri', 'neoul']:
        manifest['inn_t_' + character] = manifest['inn_inv'].copy()
    manifest['inn_t_innma'] = manifest['inn_after'].copy()
    for key, names in [('inn_meet', ['meeting-press', 'climax']),
                       ('inn_climax', ['climax-press', 'after'])]:
        manifest[key]['preload'] = [f'audio/v3/{n}-strings-v3.mp3' for n in names]
    (SOURCE / 'inn_music_tracks.js').write_text(
        '/* Generated original string score; no piano instruments. */\n'
        'window.__INN_MUSIC=' + json.dumps(manifest, separators=(',', ':')) + ';\n')
    (OUT / 'CREDITS.txt').write_text(
        'Original daaegame chapter-one string score (2026-10-10).\n'
        'Cello, string ensemble and pizzicato: FluidR3_GM.\n'
        'Copyright 2000-2002, 2008 Frank Wen; 2008 Toby Smithe. MIT license.\n'
        'Full instrument license is retained at ../v2/FLUIDR3-LICENSE.txt.\n'
        'No piano recordings are used in these tracks.\n')


if __name__ == '__main__':
    main()
