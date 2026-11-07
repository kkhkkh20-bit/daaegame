"""다람 14장 작화의 표시 계약과 교체 범위를 순수 함수로 검사한다."""
import copy
import json
from pathlib import Path
import unittest

from PIL import Image

from import_daram_consistency import (CONTEXT,GENERAL,INACTIVE,REVISION,VISIBLE_HEIGHT_840,QUESTION_VISIBLE_HEIGHT,
                                      build_profiles,select_frames,updated_registries)

ROOT=Path(__file__).resolve().parents[1]


def source_rows():
    return {slot:dict(bounds=[30+i,20+i,960-i,1500-i],size=[1024,1536],
                      file='assets/dialogue-player-facing/'+REVISION+'/'+slot+'.webp',
                      source_master='art/test-source/'+slot+'.png',source_sha256='0'*64)
            for i,slot in enumerate(GENERAL+CONTEXT)}


class DaramConsistency(unittest.TestCase):
    def setUp(self):
        self.sources=source_rows()
        self.profiles=build_profiles(self.sources)
        self.player=json.loads((ROOT/'game/assets/room13-dialogue-player-facing.json').read_text())
        self.context=json.loads((ROOT/'game/assets/room13-dialogue-context-art.json').read_text())

    def test_fourteen_sources_keep_six_emotions_and_eight_active_gestures_separate(self):
        self.assertEqual(len(GENERAL),6);self.assertEqual(len(CONTEXT),8)
        self.assertFalse(set(INACTIVE)&set(GENERAL+CONTEXT))
        self.assertEqual({cue['slot'] for cue in self.context['bindings'] if cue['person']=='daram'},set(CONTEXT))
        with self.assertRaises(ValueError):build_profiles({k:v for k,v in self.sources.items() if k!='angry'})

    def test_uniform_scale_preserves_proportions_child_height_and_source_resolution(self):
        for height,profile in self.profiles.items():
            visible=QUESTION_VISIBLE_HEIGHT if height=='560' else VISIBLE_HEIGHT_840*int(height)/840
            for slot,frame in profile['frames'].items():
                left,top,right,bottom=self.sources[slot]['bounds'];scale=frame['scale']
                self.assertAlmostEqual((bottom-top)*scale,visible,delta=.00001)
                self.assertAlmostEqual(((right-left)*scale)/((bottom-top)*scale),(right-left)/(bottom-top))
                self.assertFalse(frame['nearest'])
                self.assertTrue(all(type(n) is int for n in frame['offset']))
                if height=='840':self.assertLessEqual(scale*1302/840,1)
        self.assertAlmostEqual(VISIBLE_HEIGHT_840*1.55,766.15466615)

    def test_general_and_context_share_canvas_and_keep_every_foot_in_question_view(self):
        general=select_frames(self.profiles,GENERAL)
        for slot in CONTEXT:
            context=select_frames(self.profiles,(slot,))
            for height in general:
                self.assertEqual(context[height]['canvas'],general[height]['canvas'])
        p=self.profiles['560']
        self.assertAlmostEqual(QUESTION_VISIBLE_HEIGHT/560,2/3)
        self.assertGreaterEqual(p['question_top'],118)
        for slot,frame in p['frames'].items():
            left,top,right,bottom=self.sources[slot]['bounds'];ox,oy=frame['offset'];s=frame['scale']
            self.assertGreaterEqual(ox+left*s,0)
            self.assertLessEqual(ox+right*s,p['canvas'][0])
            self.assertGreaterEqual(p['question_top']+oy+top*s,0)
            self.assertLessEqual(p['question_top']+oy+bottom*s,708)

    def test_import_changes_only_daram_general_and_active_contexts(self):
        before_player=copy.deepcopy(self.player);before_context=copy.deepcopy(self.context)
        player,context=updated_registries(self.player,self.context,self.profiles)
        self.assertEqual(self.player,before_player);self.assertEqual(self.context,before_context)
        for who,entry in self.player['people'].items():
            if who!='daram':self.assertEqual(player['people'][who],entry)
        for key,entry in self.context['entries'].items():
            if key not in {'daram:'+slot for slot in CONTEXT}:self.assertEqual(context['entries'][key],entry)
        self.assertEqual(context['bindings'],self.context['bindings'])
        for slot in INACTIVE:self.assertEqual(context['entries']['daram:'+slot],self.context['entries']['daram:'+slot])
        self.assertEqual(set(player['people']['daram']['profiles']['840']['frames']),set(GENERAL))
        for slot in CONTEXT:
            entry=context['entries']['daram:'+slot]
            self.assertEqual(entry['art_revision'],REVISION)
            self.assertEqual(set(entry['profiles']['840']['frames']),{slot})

    def test_unexpected_story_binding_is_rejected(self):
        changed=copy.deepcopy(self.context)
        changed['bindings'].append(dict(person='daram',slot=INACTIVE[0]))
        with self.assertRaises(ValueError):updated_registries(self.player,changed,self.profiles)

    def test_applied_fourteen_assets_keep_original_alpha_and_child_size(self):
        manifest=json.loads((ROOT/'art/daram-consistency-20261107/import-manifest.json').read_text())
        self.assertEqual(manifest['revision'],REVISION)
        self.assertEqual(set(manifest['sources']),set(GENERAL+CONTEXT))
        for slot,row in manifest['sources'].items():
            with Image.open(ROOT/row['source_master']) as original,Image.open(ROOT/'game'/row['file']) as runtime:
                self.assertEqual(original.size,runtime.size)
                self.assertGreaterEqual(runtime.width,1024);self.assertGreaterEqual(runtime.height,1536)
                self.assertEqual(original.getchannel('A').tobytes(),runtime.getchannel('A').tobytes())
                box=runtime.getchannel('A').point(lambda a:255 if a>=40 else 0).getbbox()
            entry=self.player['people']['daram'] if slot in GENERAL else self.context['entries']['daram:'+slot]
            self.assertEqual(entry['art_revision'],REVISION)
            normal=entry['profiles']['840']['frames'][slot]
            self.assertEqual(normal['file'],row['file'])
            self.assertAlmostEqual((box[3]-box[1])*normal['scale'],VISIBLE_HEIGHT_840,delta=.00001)
            self.assertLess(normal['scale']*1.55,1)
            question=entry['profiles']['560'];frame=question['frames'][slot]
            self.assertLessEqual(question['question_top']+frame['offset'][1]+box[3]*frame['scale'],708)
            self.assertGreaterEqual(question['question_top'],118)
            self.assertGreater(question['question_top']+frame['offset'][1]+box[1]*frame['scale'],0)
            self.assertAlmostEqual((box[3]-box[1])*frame['scale'],QUESTION_VISIBLE_HEIGHT,delta=.00001)


if __name__=='__main__':unittest.main()
