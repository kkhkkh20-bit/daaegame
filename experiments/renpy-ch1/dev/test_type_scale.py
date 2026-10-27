"""2026-10-27 타이포그래피 시안(R13_TYPE_V2): 단계표 값과 「꺼짐 동등성」.

꺼진 동안 화면이 이전과 같아야 하므로, r13_type/r13_type_color 는 반드시
`... if R13_TYPE_V2 else <이전 값>` 꼴 안에서만 쓰이거나, 함수 머리의
`if R13_TYPE_V2:return ...` 한 줄 뒤에 이전 반환이 남아 있어야 한다."""
import re,unittest
from pathlib import Path
GAME=Path(__file__).resolve().parents[1]/'game'
SCALE=GAME/'systems'/'room13_type_scale.rpy'
# 시안이 손대는 파일. 다른 파일에서 r13_type 를 쓰면 범위를 벗어난 것이다.
TOUCHED=['screens.rpy','systems/room13_night_ui.rpy','systems/room13_notebook_choices.rpy',
         'room13_notebook.rpy','systems/room13_evidence_view.rpy',
         # 2026-10-27 2차: 현장·지도·설정·질문·단축키·더보기 판(더보기 판 화면은 footer_concept 에 있다).
         'room13_screens.rpy','room13_map_village_b.rpy','systems/room13_side_questions.rpy',
         'systems/room13_shortcuts.rpy','systems/room13_footer_concept.rpy']
GUARDED=re.compile(r'r13_type(?:_color)?\("[a-z]+"\)\s+if R13_TYPE_V2 else ')
HEAD=re.compile(r'^\s+if R13_TYPE_V2:\s*return r13_type(?:_color)?\("[a-z]+"\)')

def load_scale(touch=False,large=False,small=False):
    """init python 블록을 Ren'Py 없이 실행한다. r13_read_size 는 room13_readability.rpy 와 같은 식."""
    src=SCALE.read_text(encoding='utf-8')
    body=src.split('init 59 python:',1)[1]
    code='\n'.join(line[4:] if line.startswith('    ') else line for line in body.splitlines())
    def r13_read_size(base,large_=None):
        if not large:
            return int(max(base-3,round(base*.9))) if small else int(base)
        return int(large_ if large_ is not None else max(base+4,round(base*1.25)))
    ns={'r13_touch_ui':lambda:touch,'r13_read_size':r13_read_size}
    exec(code,ns)
    return ns

class TypeScale(unittest.TestCase):
    def test_switch_is_on(self):
        # 2026-10-27 소유자 "적용". 끄면 이전 값으로 돌아가는 구조는 그대로다.
        self.assertIn('define R13_TYPE_V2 = True',SCALE.read_text(encoding='utf-8'))

    def test_levels_rise_in_every_setting(self):
        for touch in (False,True):
            for large,small in ((False,False),(True,False),(False,True)):
                ns=load_scale(touch,large,small)
                sizes=[ns['r13_type'](l) for l in ns['R13_TYPE_LEVELS']]
                self.assertEqual(sizes,sorted(sizes),(touch,large,small,sizes))
                self.assertEqual(len(set(sizes)),len(sizes),(touch,large,small,sizes))
                self.assertGreaterEqual(min(sizes),16)

    def test_scale_values(self):
        ns=load_scale()
        self.assertEqual([ns['r13_type'](l) for l in ns['R13_TYPE_LEVELS']],[22,24,26,28,30,36,38])
        ns=load_scale(large=True)
        self.assertEqual([ns['r13_type'](l) for l in ns['R13_TYPE_LEVELS']],[26,28,30,32,34,38,40])
        ns=load_scale(touch=True)
        self.assertEqual([ns['r13_type'](l) for l in ns['R13_TYPE_LEVELS']],[26,28,30,32,34,36,38])
        ns=load_scale(small=True)
        self.assertEqual(ns['r13_type']('body'),22)

    def test_colors_are_hex(self):
        ns=load_scale()
        for token in ('ink','muted','disabled','accent','inverse'):
            self.assertRegex(ns['r13_type_color'](token),r'^#[0-9a-f]{6}$')

    def test_every_use_is_guarded_by_switch(self):
        unguarded=[];outside=[]
        for f in sorted(GAME.rglob('*.rpy')):
            if 'qa_tests' in f.parts or f==SCALE:continue
            rel=f.relative_to(GAME).as_posix()
            for n,line in enumerate(f.read_text(encoding='utf-8').splitlines(),1):
                uses=len(re.findall(r'r13_type(?:_color)?\(',line))
                if not uses:continue
                if rel not in TOUCHED:outside.append('%s:%d'%(rel,n))
                if HEAD.match(line):continue
                if len(GUARDED.findall(line))!=uses:unguarded.append('%s:%d %s'%(rel,n,line.strip()))
        self.assertEqual(outside,[],'r13_type outside the three proposal areas')
        self.assertEqual(unguarded,[],'every r13_type use needs "... if R13_TYPE_V2 else <old>"')

    def test_head_guards_keep_old_return(self):
        # 함수 머리에서 켤 때는 바로 다음 줄에 이전 return 이 남아 있어야 꺼짐이 같다.
        for rel in TOUCHED:
            lines=(GAME/rel).read_text(encoding='utf-8').splitlines()
            for i,line in enumerate(lines):
                if HEAD.match(line):
                    self.assertTrue(lines[i+1].strip().startswith('return'),'%s:%d'%(rel,i+1))

if __name__=='__main__':unittest.main()
