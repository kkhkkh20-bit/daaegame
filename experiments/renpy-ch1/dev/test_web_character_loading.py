"""Progressive character art must never expose a low-resolution stand-in."""
import io
import json
import subprocess
import unittest
from PIL import Image
from build_web import ROOT, LOADER, character_files, character_prefetch, placeholder


class CharacterLoading(unittest.TestCase):
    def test_character_placeholder_retains_size_and_has_no_visible_pixels(self):
        source = io.BytesIO()
        Image.new('RGBA', (160, 320), 'red').save(source, 'PNG')
        size, data = placeholder(source.getvalue(), transparent=True)
        image = Image.open(io.BytesIO(data)).convert("RGBA")
        self.assertEqual(size, image.size)
        self.assertIsNone(image.getbbox())
        _, background = placeholder(source.getvalue())
        self.assertIsNotNone(Image.open(io.BytesIO(background)).getbbox())

    def test_cast_and_all_source_profiles_are_classified(self):
        files = character_files(ROOT / 'game')
        self.assertIn('assets/room13-pixel-world-daram-gray-gutter.webp', files)
        self.assertIn('assets/dialogue-source-master/granny/760/neutral.webp', files)  # 예전 판도 공개본에 남긴다
        self.assertIn('assets/dialogue-source-master-v2/granny/760/neutral.webp', files)
        self.assertIn('assets/dialogue-player-facing/cast20261108/resident_piko/neutral.webp',files)
        self.assertIn('assets/dialogue-player-facing/gaze116/granny/neutral.webp',files)
        self.assertIn('assets/field-dot-v2/karo/neutral.webp',files)
        self.assertNotIn('assets/room13-title-winter020.webp', files)

    def test_day_one_warms_only_runtime_profile_in_story_order(self):
        files = character_prefetch(ROOT / 'game')
        self.assertEqual(len(files), len(set(files)))
        table = json.loads((ROOT / 'game/assets/room13-dialogue-size-fit.json').read_text())['people']
        field = json.loads((ROOT / 'game/assets/room13-field-dot-v2.json').read_text())['people']
        neutral = lambda who: table[who]['profiles']['840']['frames']['neutral']['file']
        self.assertLess(files.index(neutral('karo')), files.index(neutral('granny')))
        self.assertIn(neutral('neoul'), files)
        self.assertIn(field['karo']['poses']['neutral']['file'],files)
        # 일반대화에 쓰지 않는 옛 작화와 표정 전부를 중복 다운로드하지 않는다.
        legacy=json.loads((ROOT / 'game/assets/room13-dialogue-talk-art.json').read_text())['people']
        self.assertNotIn(legacy['karo']['profiles']['840']['frames']['neutral']['file'],files)
        self.assertNotIn(table['karo']['profiles']['840']['frames']['joy']['file'],files)
        self.assertTrue(all('/dad/' not in file for file in files))
        self.assertLess(len(files),20)

    def test_selected_people_warm_current_portraits_without_changing_released_files(self):
        table = json.loads((ROOT / 'game/assets/room13-dialogue-size-fit.json').read_text())['people']
        for who in ('resident_piko','resident_kongi','resident_ubak','seryeon'):
            files=character_prefetch(ROOT/'game',[who])
            self.assertEqual(files[0],table[who]['profiles']['840']['frames']['neutral']['file'])
            self.assertLessEqual(len(files),2)
            self.assertTrue(all((ROOT/'game'/path).is_file() for path in files))
        # 예열에서 빠진 특수/옛 파일은 character_files/빌드의 점진 로더에서 계속 제공한다.
        files=character_files(ROOT/'game')
        self.assertIn('assets/dialogue-context-master/resident_ubak/840/intake21_ubak_angry.webp',files)

    def test_background_fetch_waits_for_input_and_shares_one_deduplicated_queue(self):
        script = """const assert=require('assert');const Module={preRun:[]};
let handlers={},active=0,max=0,seen=[];
const document={baseURI:'https://example.test/',hidden:false,addEventListener(e,f){handlers[e]=f}};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function until(check){for(let i=0;i<500;i++){if(check())return;await sleep(5)}throw Error('예열 완료 대기 초과')}
global.fetch=async(url,options)=>{active++;max=Math.max(max,active);seen.push([String(url),options.priority]);
return {ok:true,async blob(){await sleep(20);active--;}}};
""" + LOADER + """
(async()=>{
 r13Prefetch=['a','b','c'];await r13PrefetchLater();await sleep(30);assert.equal(seen.length,0);
 handlers.pointerdown();await until(()=>seen.length===1);
 r13Transport={by_day:{'2':['a','d','d','e'],'3':['d','e','f'],'4':['f','g']}};
 r13PrefetchDay(2);r13PrefetchDay(3);
 await until(()=>seen.length===4&&active===0);
 assert.equal(max,1);assert(seen.every(x=>x[1]==='low'));
 assert.deepEqual(seen.map(x=>new URL(x[0]).pathname),['/a','/d','/e','/f']);
 document.hidden=true;r13PrefetchDay(4);await sleep(80);assert.equal(seen.length,4);
 document.hidden=false;handlers.visibilitychange();await until(()=>seen.length===5&&active===0);
 assert.equal(new URL(seen[4][0]).pathname,'/g');
 r13Transport.by_day['7']=['h','old-seven'];r13Prefetch=['a','first'];
 r13PrefetchDay(7);await until(()=>seen.some(x=>new URL(x[0]).pathname==='/h'));
 r13PrefetchDay(1);await until(()=>seen.some(x=>new URL(x[0]).pathname==='/first')&&active===0);
 assert(!seen.some(x=>new URL(x[0]).pathname==='/old-seven'));
 r13Transport.by_day['8']=['i','old-eight'];r13PrefetchDay(8);
 await until(()=>seen.some(x=>new URL(x[0]).pathname==='/i'));
 r13PrefetchDay(99);await sleep(120);
 assert(!seen.some(x=>new URL(x[0]).pathname==='/old-eight'));
 assert.equal(max,1);
})().catch(e=>{console.error(e);process.exit(1)});
"""
        subprocess.run(['node', '-e', script], check=True, capture_output=True, text=True)


class LoadingAudio(unittest.TestCase):
    def test_blocked_autoplay_first_gesture_and_single_handoff(self):
        script = """const assert=require('assert');let events={},plays=0,pauses=0;
const document={body:{appendChild(){}},addEventListener(e,f){events[e]=f},removeEventListener(e){delete events[e]}};
const window={addEventListener(){}};
class Audio {constructor(){this.paused=true;this.currentTime=12.5}play(){plays++;if(plays===1)return Promise.reject(Error('blocked'));this.paused=false;return Promise.resolve()}pause(){pauses++;this.paused=true}removeAttribute(){}load(){}}
""" + (ROOT / 'dev/title-loader-audio.js').read_text() + """
(async()=>{await Promise.resolve();assert.equal(plays,1);assert(events.touchstart);events.pointerdown();await Promise.resolve();assert.equal(plays,2);
assert.equal(window.r13LoadingAudio.audio.paused,false);assert.equal(window.r13LoadingAudio.handoff(),12.5);
assert.equal(pauses,1);assert.equal(Object.keys(events).length,0);assert.equal(window.r13LoadingAudio.handoff(),0);})();
"""
        subprocess.run(['node', '-e', script], check=True, capture_output=True, text=True)


if __name__ == '__main__':
    unittest.main()
