"""로딩창은 메인화면과 같은 그림을 쓰고, 음악 안내 줄은 자동재생이 막혔을 때만 보인다."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from update_title_loader import ROOT, update_title_loader, loading_art, LOADING_ART
import make_loading_scene


class LoadingScene(unittest.TestCase):
    def test_composed_scene_is_1280x720_and_matches_main_menu_layers(self):
        scene = make_loading_scene.compose()
        self.assertEqual(scene.size, make_loading_scene.CANVAS)
        # screens.rpy main_menu 의 세 층과 같은 파일·배율·좌표여야 로딩이 끝날 때 그림이 튀지 않는다.
        menu = (ROOT / 'game/screens.rpy').read_text(encoding='utf-8')
        for rel, zoom, x, y in make_loading_scene.LAYERS:
            self.assertIn(Path(rel).name, menu)
        self.assertEqual([l[1:] for l in make_loading_scene.LAYERS], [(1280.0 / 1672, 0, 0), (.85, -18, 10), (610.0 / 1402, 754, 80)])
        shipped = ROOT / 'game' / LOADING_ART[0]
        self.assertTrue(shipped.exists())
        self.assertEqual(Image.open(shipped).size, make_loading_scene.CANVAS)
        # 예전 타이틀 그림이 아니라 새 그림이 먼저 선택된다.
        self.assertEqual(loading_art(ROOT / 'game'), shipped)

    def test_release_gets_new_scene_and_hidden_audio_hint(self):
        with tempfile.TemporaryDirectory() as tmp:
            release = Path(tmp) / 'release'; (release / 'game/assets').mkdir(parents=True)
            (release / 'index.html').write_text('<html><head></head><body><img id="presplash" src="loading-scene.png">\n'
                                                '<div id="loading-brand"><h1>x</h1></div>\n<script src="renpy-pre.js?v=1"></script></body></html>')
            (release / 'pwa_catalog.json').write_text(json.dumps({'files': []}))
            (release / 'build-manifest.json').write_text(json.dumps({'files': {}}))
            update_title_loader(release, ROOT / 'game')
            self.assertEqual((release / 'loading-scene.webp').read_bytes(), (ROOT / 'game' / LOADING_ART[0]).read_bytes())
            s = (release / 'index.html').read_text()
            self.assertIn('src="loading-scene.webp"', s)
            self.assertIn('<p class="loading-audio-hint" hidden>화면을 한 번 누르면 음악이 켜집니다</p>', s)
            self.assertIn('loading-audio-hint[hidden]{display:none}', s)
            self.assertIn('id="r13-loading-audio"', s)
            self.assertIn('loading-scene.webp', json.loads((release / 'pwa_catalog.json').read_text())['files'])

    def test_audio_hint_shows_only_while_autoplay_is_blocked(self):
        script = """const assert=require('assert');let events={},plays=0;const hint={hidden:true};
const document={body:{appendChild(){}},addEventListener(e,f){events[e]=f},removeEventListener(e){delete events[e]},querySelector(){return hint}};
const window={addEventListener(){}};
class Audio {constructor(){this.paused=true;this.currentTime=3}play(){plays++;if(plays===1)return Promise.reject(Error('blocked'));this.paused=false;return Promise.resolve()}pause(){this.paused=true}removeAttribute(){}load(){}}
""" + (ROOT / 'dev/title-loader-audio.js').read_text() + """
(async()=>{await Promise.resolve();await Promise.resolve();assert.equal(hint.hidden,false); // 거부되면 편다
events.pointerdown();await Promise.resolve();await Promise.resolve();assert.equal(hint.hidden,true); // 켜지면 접는다
})().catch(e=>{console.error(e);process.exit(1)});
"""
        subprocess.run(['node', '-e', script], check=True, capture_output=True, text=True)
        allowed = """const assert=require('assert');const hint={hidden:true};
const document={body:{appendChild(){}},addEventListener(){},removeEventListener(){},querySelector(){return hint}};
const window={addEventListener(){}};
class Audio {constructor(){this.paused=true}play(){this.paused=false;return Promise.resolve()}pause(){}removeAttribute(){}load(){}}
""" + (ROOT / 'dev/title-loader-audio.js').read_text() + """
(async()=>{await Promise.resolve();await Promise.resolve();assert.equal(hint.hidden,true); // 처음부터 허용되면 안 보인다
})().catch(e=>{console.error(e);process.exit(1)});
"""
        subprocess.run(['node', '-e', allowed], check=True, capture_output=True, text=True)


if __name__ == '__main__':
    unittest.main()
