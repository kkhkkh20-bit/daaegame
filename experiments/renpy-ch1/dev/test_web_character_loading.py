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
        self.assertNotIn('assets/room13-title-winter020.webp', files)

    def test_day_one_warms_only_runtime_profile_in_story_order(self):
        files = character_prefetch(ROOT / 'game')
        self.assertEqual(len(files), len(set(files)))
        self.assertTrue(all('/560/' not in f and '/760/' not in f for f in files))
        # 2026-10-26 전신 묶음으로 경로가 dialogue-source-master-v2 로 바뀐 인물이 있다. 연결표가 가리키는 파일로 본다.
        import json
        talk = json.loads((ROOT / 'game/assets/room13-dialogue-talk-art.json').read_text())['people']
        neutral = lambda who: talk[who]['profiles']['840']['frames']['neutral']['file']
        self.assertLess(files.index(neutral('karo')), files.index(neutral('granny')))
        self.assertIn(neutral('neoul'), files)

    def test_background_fetch_concurrency_is_bounded(self):
        script = """const assert=require('assert');const Module={preRun:[]};
const document={baseURI:'https://example.test/'};let active=0,max=0,seen=[];
global.fetch=async(url,options)=>{active++;max=Math.max(max,active);seen.push([String(url),options.priority]);
return {async blob(){await new Promise(r=>setTimeout(r,5));active--;}}};
""" + LOADER + """
r13Prefetch=['a','b','c','d'];
r13PrefetchLater().then(()=>{assert.equal(max,2);assert.equal(seen.length,4);assert(seen.every(x=>x[1]==='low'));}).catch(e=>{console.error(e);process.exit(1)});
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
