# Read-only recollections. No unlocks, travel, rollback, or automatic opening.
default persistent.r13_fork_runs = 0
default persistent.r13_fork_seen = {}
default persistent.r13_fork_endings = {}

init 322 python:
    R13_FORK_MEETINGS = (
        ('gate','입구 회의','1일','gate'),
        ('lamp','등 회의','3일','square'),
        ('gate_post','초소 회의','5일','gate'),
        ('fire','불 회의','7일','v111_fire'),
        ('room13','13호실 회의','10일 오후','room13'),
        ('records','기록 회의','10일 오후','room13'),
        ('hypothesis','가설 회의','11일','room13'),
        ('soup','수프 회의','12일','dining'),
        ('blanket','담요 회의','13일','square'),
        ('piko','피코 회의','13일','square'),
        ('altar','제단 회의','14일','altar'))
    R13_FORK_RESULTS = dict(win='이김',partial='부분',lose='짐')
    R13_FORK_ENDINGS = dict(left_name='남겨진 이름',frozen='얼어붙은 마을',family='함께 떠난 가족',partial='남은 사람들',violence='상처 입은 귀환',morning='마을의 아침',true='새로운 아침')

    def r13_fork_start():
        persistent.r13_fork_runs = (persistent.r13_fork_runs or 0)+1
        store.room13['v111']['fork_run'] = persistent.r13_fork_runs
        renpy.save_persistent()

    def r13_fork_capture():
        try:
            return renpy.screenshot_to_bytes((320,180))
        except Exception:
            return None

    def r13_fork_record(meeting,result):
        if meeting not in [m[0] for m in R13_FORK_MEETINGS] or result not in R13_FORK_RESULTS:return
        seen = dict(persistent.r13_fork_seen or {})
        seen[(meeting,result)] = dict(png=r13_fork_capture(),run=store.room13['v111'].get('fork_run',1))
        persistent.r13_fork_seen = seen
        renpy.save_persistent()

    def r13_fork_ending(key):
        if key not in R13_FORK_ENDINGS:return
        endings = dict(persistent.r13_fork_endings or {})
        endings[key] = dict(png=r13_fork_capture(),run=store.room13['v111'].get('fork_run',1))
        persistent.r13_fork_endings = endings
        renpy.save_persistent()

    def r13_fork_current():
        claim = getattr(store,'r13_meeting_claim',None)
        if getattr(store,'r13_meeting_active',False) and claim:
            for i,m in enumerate(R13_FORK_MEETINGS):
                if claim == 'NW:'+m[0]:return i
        decided = [i for i,m in enumerate(R13_FORK_MEETINGS) if r13_v111_value('meeting:'+m[0]) in R13_FORK_RESULTS]
        return min(11,max(decided)+1) if decided else 0

    def r13_fork_columns():
        current = r13_fork_current()
        seen = persistent.r13_fork_seen or {}
        columns = []
        for i,(key,title,day,place) in enumerate(R13_FORK_MEETINGS):
            if i>current:break
            result = r13_v111_value('meeting:'+key)
            here = i==current
            rows = [dict(kind='current',result=result,title=title,record=seen.get((key,result)))]
            if not here:
                for other in ('win','partial','lose'):
                    if other==result:continue
                    record=seen.get((key,other))
                    rows.append(dict(kind='old' if record else 'locked',result=other if record else None,title=title if record else None,record=record))
            columns.append(dict(key=key,day=day,place=place,here=here,rows=rows))
        if current<11:columns.append(dict(key=None,day='그 너머',rows=[]))
        return columns

    def r13_fork_image(record,place='square'):
        if record and record.get('png'):
            return im.Data(record['png'],'fork.png')
        place = place if place in R13_PLACES else 'square'
        return r13_background(R13_PLACES[place][1])

    def r13_fork_initial_page():
        return min(max(0,len(r13_fork_columns())-6),max(0,min(r13_fork_current(),10)-4))

screen r13_fork_card(column,row):
    frame:
        xsize 164 ysize 114 padding (5,5)
        background R13PaperPanel(row['kind']=='current',remembered=row['kind']=='old')
        if row['kind']=='locked':
            add R13AntiqueIcon('lock',size=30) align (.5,.5)
        else:
            vbox:
                spacing 0
                add Transform(r13_fork_image(row['record'],column['place']),xysize=(154,64),nearest=True,matrixcolor=SepiaMatrix() if row['kind']=='old' else BrightnessMatrix(0))
                text row['title'] size 18 color '#624b32' font r13_ui_font()
                text ('● 현재 위치' if column['here'] else ('누적 · ' if row['kind']=='old' else '')+R13_FORK_RESULTS.get(row['result'],'')) size 16 color ('#a05f3d' if column['here'] else '#8d7351') xalign 1.0

screen r13_fork_screen():
    modal True
    zorder 65
    default first = r13_fork_initial_page()
    $ columns = r13_fork_columns()
    add Solid('#211b1899')
    add R13PaperFrame() xpos 28 ypos 25 xysize (1224,670)
    text '이야기의 갈림길' xpos 58 ypos 58 size 30 color '#624b32' font r13_ui_font()
    text '기록 / 지나온 이야기' xpos 58 ypos 103 size 16 color '#8d7351'
    text ('%d회차 · %d일' % (room13['v111'].get('fork_run',1),room13['day'])) xpos 900 ypos 85 size 18 color '#624b32'
    fixed:
        xpos 1120 ypos 50 xysize (100,80)
        use r13_control('닫기',None,Hide('r13_fork_screen'),width=100)
    add Solid('#baa47b') xpos 58 ypos 130 xysize (1164,2)
    text '━ 이번 회차    ┄ 누적 발견    ▫ 미발견' xpos 62 ypos 150 size 18 color '#765b3d'
    $ here = r13_fork_current()
    text ('현재 · '+R13_FORK_MEETINGS[here][1] if here<11 else '지나온 이야기') xpos 980 ypos 150 size 16 color '#a05f3d'
    for offset,column in enumerate(columns[first:first+6]):
        $ cx=68+offset*196
        text column['day'] xpos cx ypos 200 xsize 164 text_align .5 size 20 color '#765b3d'
        if column['key'] is None:
            frame:
                xpos cx ypos 235 xsize 164 ysize 114 background R13PaperPanel() padding (8,8)
                text '···\n미발견' align (.5,.5) text_align .5 size 18 color '#b7a17a'
            text '아직 펼치지 않은\n이야기' xpos cx ypos 370 xsize 164 text_align .5 size 18 color '#a9916c'
        else:
            if first+offset<len(columns)-1 and offset<5:
                add Solid('#87633e' if not column['here'] else '#baa47b') xpos (cx+164) ypos 290 xysize (32,3)
            if len(column['rows'])>1:
                add Solid('#baa47b') xpos (cx-10) ypos 290 xysize (2,265)
            for ri,row in enumerate(column['rows']):
                if ri:
                    add Solid('#baa47b') xpos (cx-10) ypos (290+ri*131) xysize (10,2)
                fixed:
                    xpos cx ypos (235+ri*131) xysize (164,114)
                    use r13_fork_card(column,row)
    add Solid('#baa47b') xpos 58 ypos 620 xysize (1164,1)
    text '지나온 길을 모아, 다음 이야기를 찾아요.' xpos 62 ypos 651 size 16 color '#8d7351'
    fixed:
        xpos 490 ypos 628 xysize (80,80)
        use r13_control('‹',None,SetScreenVariable('first',max(0,first-1)),width=80,enabled=first>0)
    fixed:
        xpos 580 ypos 628 xysize (80,80)
        use r13_control('›',None,SetScreenVariable('first',min(max(0,len(columns)-6),first+1)),width=80,enabled=first+6<len(columns))
    viewport:
        area (760,627,450,56) draggable True mousewheel 'horizontal'
        hbox:
            spacing 16
            for ending,record in sorted((persistent.r13_fork_endings or {}).items()):
                hbox:
                    spacing 8
                    add Transform(r13_fork_image(record),xysize=(72,41),nearest=True)
                    vbox:
                        text ('누적 결말 · %d회차'%record['run']) size 16 color '#a18a65'
                        text R13_FORK_ENDINGS.get(ending,'') size 16 color '#8d7351'
    key 'K_LEFT' action SetScreenVariable('first',max(0,first-1))
    key 'K_RIGHT' action SetScreenVariable('first',min(max(0,len(columns)-6),first+1))
    key 'game_menu' action Hide('r13_fork_screen')
