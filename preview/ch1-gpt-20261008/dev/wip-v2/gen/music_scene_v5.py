"""Original piano-free night/search cues. Committed audio is the runtime source."""
import json
import music_context_v4 as context

context.OUT = context.SOURCE.parents[1] / 'audio/v5'
context.TRACKS = {
    'night': dict(key='inn_night', bpm=92, tonic='D minor', bars=16,
                  form=['A']*8+['B']*8,
                  chords=['Dm','Dm','Bb','Am','Dm','Gm','Am','Dm']*2, target=-24),
    'search': dict(key='inn_search', bpm=112, tonic='D minor', bars=16,
                   form=['A']*8+['B']*8,
                   chords=['Dm','Bb','Gm','Am','Dm','F','Am','Dm',
                           'Gm','Dm','Bb','Am','Dm','Gm','Am','Dm'], target=-23.5)
}

def score(name):
    track=context.TRACKS[name]; beat=60/track['bpm']; events=[]
    def note(bar, off, lane, pitch, dur, velocity):
        dur=min(dur,4-off-.125)
        events.append(((bar*4+off)*beat,lane,pitch,dur*beat,velocity))
    for bar, chord in enumerate(track['chords']):
        tri=context.TRIADS[chord]; urgent=name=='search'; answering=bar>=8
        # Quiet, articulated eighths build motion without sharp percussion.
        for j in range(8):
            pitch=tri[(0,2,1,2,0,2,1,2)[j]]+(12 if urgent and answering else 0)
            note(bar,j*.5,5,pitch,.25,35 if urgent and j%2==0 else 26)
        for off in (0,2):note(bar,off,1,tri[0]-12,1.25,34 if urgent else 27)
        for pitch in tri[:2]:note(bar,0,2,pitch,3.5,20 if urgent else 15)
        # A small rising answer, then space for speech. All notes fit the chord.
        if bar%4 in (1,2):
            phrase=[(.5,0,1),(2,1,.75),(3,2,.75)] if urgent else [(1,2,1.5)]
            for off,idx,dur in phrase:
                note(bar,off,4 if urgent else 7,tri[idx]+12,dur,35 if urgent else 28)
    return sorted(events),round(track['bars']*4*beat*context.RATE)/context.RATE

context.score=score

if __name__=='__main__':
    context.OUT.mkdir(parents=True,exist_ok=True)
    rows=[context.render(name) for name in context.TRACKS]
    for row in rows:
        old=context.OUT/row['file'];new=context.OUT/(row['name']+'-scene-v5.mp3');old.rename(new);row['file']=new.name
    (context.OUT/'score-scene-v5.json').write_text(json.dumps(rows,indent=2)+'\n')
    path=context.SOURCE/'inn_music_tracks.js'
    mapping=json.JSONDecoder().raw_decode(path.read_text().split('window.__INN_MUSIC=',1)[1])[0]
    for row in rows:
        mapping[row['key']]=dict(bpm=row['bpm'],vol=.8,prog=row['chords'],mel=[],
                                media='audio/v5/'+row['file'],loopSeconds=row['seconds'])
    path.write_text('/* Original piano-free context and authored suspense cues. */\nwindow.__INN_MUSIC='+json.dumps(mapping,separators=(',',':'))+';\n')
    (context.OUT/'CREDITS.txt').write_text(
        'Original daaegame night and search score, 2026-10-11.\n'
        'Composition, arrangement and rendering: project original score.\n'
        'Cello, string ensemble, pizzicato, clarinet and bassoon: FluidR3_GM.\n'
        'Copyright 2000-2002, 2008 Frank Wen; 2008 Toby Smithe. MIT license.\n'
        'Full sample license: ../v2/FLUIDR3-LICENSE.txt.\n'
        'No piano, horse sounds, external soundtrack or transcribed melodies.\n')
