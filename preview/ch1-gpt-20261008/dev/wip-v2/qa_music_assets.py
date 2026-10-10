"""Measure preserved v3, new v4 context audio, scores, URLs and attribution.

This checks files and notation; it does not claim subjective listening, natural
recording provenance beyond the upstream attribution, or engine transition QA.
Run after generating the nine string tracks and three sampled SFX.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.parse
import urllib.request

import numpy as np
from scipy import signal


BASE = Path(__file__).resolve().parent
PREVIEW = BASE.parents[1]
RATE = 44100
TRIADS = ({2,5,9}, {10,2,5}, {5,9,0}, {0,4,7})
WARM = {'travel','after'}


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(path):
    channels = int(subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries',
        'stream=channels', '-of', 'csv=p=0', str(path)], text=True).strip())
    raw = subprocess.check_output([
        'ffmpeg', '-v', 'error', '-i', str(path), '-ar', str(RATE),
        '-f', 'f32le', 'pipe:1'])
    return np.frombuffer(raw, np.float32).reshape(-1, channels)


def download(base_url, relative, local):
    parsed = urllib.parse.urlsplit(relative)
    assert not parsed.scheme and not relative.startswith('/') and '..' not in Path(relative).parts, relative
    with urllib.request.urlopen(urllib.parse.urljoin(base_url, relative), timeout=15) as response:
        assert response.status == 200, (relative, response.status)
        remote = response.read()
    assert hashlib.sha256(remote).hexdigest() == checksum(local), ('HTTP served a stale/different audio asset', relative)


def measure(row, path):
    assert checksum(path) == row['sha256'], ('Asset does not match score manifest', path)
    audio = decode(path)
    seconds = row.get('seconds', row.get('duration_seconds'))
    expected = round(seconds*RATE)
    # MP3 codec padding is allowed outside the authoritative loopEnd.
    assert expected <= len(audio) <= expected+int(.1*RATE), (path.name, expected, len(audio))
    audio = audio[:expected]
    assert np.isfinite(audio).all(), path.name
    assert not np.any(abs(audio) >= 1), ('Clipping in decoded asset', path.name)
    peak = float(np.max(abs(audio)))
    assert peak <= .8, ('Insufficient peak headroom', path.name, peak)
    seam = float(np.max(abs(audio[0]-audio[-1])))
    if row.get('loop', True):
        assert seam < .01, ('Large loop boundary discontinuity', path.name, seam)
    # Require a genuinely nonempty asset, not a silent file with a valid hash.
    rms = float(np.sqrt(np.mean(audio*audio)))
    assert rms > .001, ('Empty or unusably quiet audio', path.name)
    print(path.name, 'duration', round(seconds,6), 'peak_dBFS', round(20*np.log10(peak),2),
          'rms_dBFS', round(20*np.log10(rms),2), 'loop_jump', round(seam,6), flush=True)
    return audio


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:8000/')
    parser.add_argument('--offline', action='store_true', help='Skip HTTP byte-for-byte download checks')
    args = parser.parse_args()
    root = PREVIEW/'audio/v3'
    tracks = json.loads((root/'score-strings-v3.json').read_text())
    assert {row['name'] for row in tracks} == {
        'title','travel','investigation','serious','meeting','meeting-press',
        'climax','climax-press','after'}, 'Missing or unexpected string track'
    source = (BASE/'inn_music_tracks.js').read_text()
    mapping = json.JSONDecoder().raw_decode(source.split('window.__INN_MUSIC=',1)[1])[0]
    context_root = PREVIEW/'audio/v4'
    context = json.loads((context_root/'score-context-v4.json').read_text())
    files = {row['file']:row for row in tracks+context}
    for key, song in mapping.items():
        assert song['media'].startswith(('audio/v3/','audio/v4/')) and 'piano' not in song['media'], (key,song)
        assert not any(song.get(lane) for lane in ('mel','bass','pad','arp','dr','comp')), (
            'Sampled track also schedules an old synthesized accompaniment', key)
        row = files[Path(song['media']).name]
        assert abs(song['loopSeconds']-row['seconds']) <= 1/RATE, (key,song)
        for relative in [song['media']]+song.get('preload',[]):
            local = PREVIEW/relative
            assert local.is_file(), ('Broken music URL', key,relative)
    for row in tracks:
        assert row['beatsPerBar'] == 4 and row['bars'] == 16
        assert abs(row['seconds']-64*60/row['bpm']) <= 1/RATE
        for note in row['notes']:
            assert note['lane'] in (1,2,5), ('Piano or unexpected instrument lane', row['name'],note)
            beat = note['at']*row['bpm']/60
            assert abs(beat-round(beat)) < 2e-5, ('Off-grid attack', row['name'],note)
            chord_index = int((beat+1e-5)//8)%4
            if row['name'] in WARM:
                chord_index = (2,3,0,1)[chord_index]
            assert note['midi']%12 in TRIADS[chord_index], ('Note outside current triad', row['name'],note)
            assert note['duration'] > 0 and note['at']+note['duration'] <= row['seconds']+1e-5, note
        assert -26 <= row['integrated_lufs'] <= -22, ('Score is too loud for a restrained background',row['name'])
        audio = measure(row, root/row['file'])
        del audio
        if not args.offline:
            download(args.base_url, 'audio/v3/'+row['file'], root/row['file'])
    credits = (root/'CREDITS.txt').read_text()
    assert all(text in credits for text in ('FluidR3','Frank Wen','Toby Smithe','MIT')), credits
    assert (PREVIEW/'audio/v2/FLUIDR3-LICENSE.txt').is_file(), 'Missing instrument license'
    print('PASS nine non-piano tracks: triads, attack grid, headroom, loop seams, manifest paths and instrument credits',flush=True)

    # Context cues must be distinct authored scores, not tempo-adjusted copies.
    assert {r['key'] for r in context} == {'inn_inv','inn_serious','inn_comic','inn_friend'}
    expected_tonics={'inn_inv':'D minor','inn_serious':'D minor','inn_comic':'G major','inn_friend':'F major'}
    themes=[]
    assert len({r['sha256'] for r in context})==4, 'Duplicated context recordings'
    for row in context:
        assert row['beatsPerBar']==4 and row['bars'] in (16,24) and row['gridSubdivision']==2
        assert row['tonic']==expected_tonics[row['key']]
        assert len(row['chords'])==row['bars'] and len(row['form'])==row['bars']
        assert {'A','B'} <= set(row['form']), ('Missing distinct A/B sections',row['name'])
        assert abs(row['seconds']-row['bars']*4*60/row['bpm']) <= 1/RATE
        assert all(int(lane)>0 and int(program) not in range(8) for lane,program in row['programs'].items()), ('Piano instrument mapped',row['name'])
        motif=[];sections={'A':[],'B':[]}
        for note in row['notes']:
            assert str(note['lane']) in row['programs'] and note['lane']!=0
            beat=note['at']*row['bpm']/60
            assert abs(beat*2-round(beat*2))<3e-5, ('Off eighth-note grid',row['name'],note)
            bar=min(row['bars']-1,int((beat+1e-5)//4))
            chord=row['triads'][row['chords'][bar]]
            assert note['midi']%12 in {n%12 for n in chord}, ('Note outside active chord',row['name'],note,chord)
            assert 0<note['duration'] and note['at']+note['duration']<=row['seconds']+1e-5
            pattern=(round(beat%4,4),note['midi']%12,round(note['duration']*row['bpm']/60,4))
            motif.append(pattern)
            label=row['form'][bar]
            if label in sections:sections[label].append(pattern)
        assert sections['A']!=sections['B'], ('A/B merely repeats same phrase',row['name'])
        themes.append(motif)
        assert -25.2<=row['integrated_lufs']<=-22.8, ('Context outside -23 to -25 LUFS',row['name'],row['integrated_lufs'])
        assert row['true_peak_db']<=-3.5, ('Context lacks true-peak headroom',row['name'])
        assert mapping[row['key']]['media']=='audio/v4/'+row['file']
        assert abs(mapping[row['key']]['loopSeconds']-row['seconds'])<=1/RATE
        audio=measure(row,context_root/row['file']);del audio
        meter=subprocess.run(['ffmpeg','-v','info','-i',str(context_root/row['file']),'-af','loudnorm=print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
        measured=json.JSONDecoder().raw_decode(meter.stderr[meter.stderr.rfind('{'):].lstrip())[0]
        assert -25<=float(measured['input_i'])<=-23, ('Decoded MP3 loudness outside dialogue range',row['name'],measured)
        assert abs(float(measured['input_i'])-row['integrated_lufs'])<=.05, ('Stale loudness metadata',row['name'])
        assert float(measured['input_tp'])<=-3.5, ('Decoded MP3 true peak lacks headroom',row['name'])
        if not args.offline:download(args.base_url,'audio/v4/'+row['file'],context_root/row['file'])
    assert all(a!=b for i,a in enumerate(themes) for b in themes[i+1:]), 'Context cues only change tempo or timbre'
    for key in ('inn_title','inn_travel','inn_meet','inn_meet_press','inn_climax','inn_climax_press','inn_after'):
        assert mapping[key]['media'].startswith('audio/v3/'), ('Existing v3 cue replaced',key)
    ccredits=(context_root/'CREDITS.txt').read_text()
    assert all(x in ccredits for x in ('FluidR3','Frank Wen','Toby Smithe','MIT','../v2/FLUIDR3-LICENSE.txt'))
    print('PASS four distinct original context cues: A/B motifs, harmony/grid, -23 to -25 LUFS, headroom, loopEnd, URLs and credits',flush=True)

    sfx_root = root/'sfx'
    sfx = json.loads((sfx_root/'manifest.json').read_text())
    sfx_credits = (sfx_root/'SFX_CREDITS.txt').read_text()
    assert {x['file'] for x in sfx['assets']} == {
        'horse-carriage-loop.wav','wood-door-open.wav','wood-door-close.wav'}
    for document in sfx['source_documents']:
        assert checksum(sfx_root/document['file']) == document['sha256'], document
    for row in sfx['assets']:
        assert row['license'] in ('CC BY 3.0','CC BY-SA 3.0'), row
        assert row['license_url'] in sfx_credits and row['source']['page'] in sfx_credits, row
        source_name = 'horse' if row['loop'] else 'open' if 'open' in row['file'] else 'close'
        assert checksum(sfx_root/'source'/f'{source_name}.ogg') == row['source']['sha256']
        assert row['modifications'] and row['source']['author'] in sfx_credits
        audio = measure(row, sfx_root/row['file'])
        assert np.max(abs(audio[[0,-1]])) < 1/32768, ('Effect has unfaded endpoints',row['file'])
        if row['loop']:
            assert row['beats_per_loop'] == 2 and row['duration_seconds'] == 1.2
            assert row['loop_start_seconds'] == 0 and row['loop_end_seconds'] == 1.2
            mono = audio.mean(axis=1)
            envelope = np.sqrt(np.mean(mono.reshape(-1,441)**2,axis=1))
            peaks,_ = signal.find_peaks(envelope,height=envelope.max()*.4,distance=30)
            assert len(peaks) == 2 and abs((peaks[1]-peaks[0])*.01-.6)<.03, (
                'Horse loop does not have two separated hoof beats',peaks)
        else:
            assert row['loop_start_seconds'] is None and row['loop_end_seconds'] is None
        if not args.offline:
            download(args.base_url, 'audio/v3/sfx/'+row['file'], sfx_root/row['file'])
    assert 'distributed under CC BY-SA 3.0' in sfx_credits
    print('PASS sampled SFX: two-beat loop, one-shot doors, fades, headroom, original hashes and attribution',flush=True)
    print('PASS asset/score validation. Subjective listening and runtime transitions require separate review.',flush=True)


if __name__ == '__main__':
    main()
