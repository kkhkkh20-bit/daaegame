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
    # 0.20.5 (Codex S01): the final results each meeting really has (r13_nw_meeting_end calls in
    # room13_v111_days*.rpy; dev/test_fork_screen.py re-derives this). A retry is not a result.
    R13_FORK_OUTCOMES = dict(gate=('win','lose'),gate_post=('win','lose'),piko=('win','lose'))
    def r13_fork_outcomes(meeting):
        return R13_FORK_OUTCOMES.get(meeting,('win','partial','lose'))
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

    # 0.20.x 갈림길 (owner-approved plan5 m4, 2026-10-22): a meeting whose result decides someone's
    # fate carries a "?" person badge and the line R13_FORK_FATE_LINE. Never who, never the
    # conditions, never life or death. A meeting is listed here when one of its result paths in
    # room13_v111_days*.rpy writes a name on the transfer list (r13_nw_list, room13_v111_newworld_rules),
    # sends people away on the cart (departed:), takes someone into custody (DARAM_DETAINED,
    # grandmother_custody) or ends a life (*_alive False). dev/test_fork_screen.py re-derives the
    # set from those labels, so a new fate effect in a meeting shows up as a test failure.
    R13_FORK_FATE = frozenset(('lamp','gate_post','fire','room13','records','soup','blanket'))
    R13_FORK_FATE_LINE = '이 회의에서 누군가의 운명이 갈렸다.'

    def r13_fork_fate(meeting):
        """Badge only on a meeting already decided in this run (never on the one still ahead)."""
        return meeting in R13_FORK_FATE and r13_v111_value('meeting:'+meeting) in R13_FORK_RESULTS

    def r13_fork_day_label(day):
        return day.replace('일','일째',1) if day and '일' in day else day

    def r13_fork_columns():
        current = r13_fork_current()
        seen = persistent.r13_fork_seen or {}
        columns = []
        for i,(key,title,day,place) in enumerate(R13_FORK_MEETINGS):
            if i>current:break
            result = r13_v111_value('meeting:'+key)
            here = i==current
            # 0.20.5 (Codex S02): the shared record keeps the latest run's picture; an earlier
            # run's save shows the place background instead of another run's picture.
            mine = seen.get((key,result))
            if mine and mine.get('run',1)!=store.room13['v111'].get('fork_run',1):mine = None
            rows = [dict(kind='current',result=result,title=title,record=mine)]
            if not here:
                hidden = 0
                for other in r13_fork_outcomes(key):
                    if other==result:continue
                    record=seen.get((key,other))
                    if record:rows.append(dict(kind='old',result=other,title=title,record=record))
                    else:hidden += 1
                # Unseen results: one lock with a count only (no title, no result, no picture).
                if hidden:rows.append(dict(kind='locked',result=None,title=None,record=None,count=hidden))
            columns.append(dict(key=key,day=day,place=place,here=here,rows=rows,title=title,fate=(not here) and r13_fork_fate(key)))
        if current<11:columns.append(dict(key=None,day='그 너머',rows=[]))
        return columns

    def r13_fork_image(record,place='square'):
        if record and record.get('png'):
            return im.Data(record['png'],'fork.png')
        place = place if place in R13_PLACES else 'square'
        return r13_background(R13_PLACES[place][1])

    def r13_fork_initial_page():
        return min(max(0,len(r13_fork_columns())-6),max(0,min(r13_fork_current(),10)-4))

    def r13_fork_row_tops(rows,top=200,gap=16):
        """Card tops in one column: result cards are 116 high, the count lock 56."""
        tops=[];y=top
        for row in rows:
            tops.append(y);y+=(56 if row['kind']=='locked' else 116)+gap
        return tops

screen r13_fork_card(column,row,small=16):
    # 0.20.x: brown sheet and result cards as the approved mockup (plan5 m4_forks.png).
    if row['kind']=='locked':
        frame:
            xsize 175 ysize 56 padding (10,4) background Frame(R13_NIGHT_UI+'preview_box.png',8,8)
            hbox:
                align (.5,.5) spacing 10
                add R13AntiqueIcon('lock',size=22) yalign .5
                text ('다른 결과 %d'%row.get('count',1)) size (small+2) color '#e3d6bd' font r13_ui_font() yalign .5
    elif column['here']:
        frame:
            xsize 175 ysize 116 padding (8,8) background Frame(R13_NIGHT_UI+'opt_btn_selected.png',16,16)
            vbox:
                align (.5,.5) spacing 6
                add R13_NIGHT_UI+'diamond.png' xalign .5
                text '지금 여기' size (small+6) color '#fff6e2' font r13_ui_font() xalign .5
                text '결과 미정' size small color '#f2d28d' font r13_ui_font() xalign .5
    else:
        frame:
            xsize 175 ysize 116 padding (5,5) background Frame(R13_NIGHT_UI+'panel_small.png',12,12)
            vbox:
                spacing 4
                add Transform(r13_fork_image(row['record'],column['place']),xysize=(165,72),nearest=True,matrixcolor=SepiaMatrix() if row['kind']=='old' else BrightnessMatrix(0))
                fixed:
                    xysize (165,30)
                    text R13_FORK_RESULTS.get(row['result'],'지나감') xpos 4 yalign .5 size (small+2) color '#f6ecd8' font r13_ui_font()
                    text ('이번 회차' if row['kind']=='current' else '%d회차에서 봄'%(row['record'] or {}).get('run',1)) xalign 1.0 xoffset -4 yalign .5 size small color '#cdbb98' font r13_ui_font()

screen r13_fork_screen():
    modal True
    zorder 65
    default first = r13_fork_initial_page()
    default fate_open = None
    $ columns = r13_fork_columns()
    $ touch = r13_touch_ui()
    $ small = 18 if touch else 16
    $ ch = r13_control_height()
    $ by = 684-ch
    add Solid('#05070fa6')
    add Frame(R13_NIGHT_UI+'panel.png',48,48) xpos 12 ypos 12 xysize (1256,696)
    text '이야기의 갈림길' xpos 60 ypos 40 size 34 color '#f6ecd8' font r13_ui_font()
    text '기록 / 지나온 이야기' xpos 316 ypos 54 size small color '#cdbb98' font r13_ui_font()
    text ('%d회차 · %d일째' % (room13['v111'].get('fork_run',1),room13['day'])) xpos 1150 xanchor 1.0 ypos 52 size (small+2) color '#f6ecd8' font r13_ui_font()
    button:
        id 'r13_fork_close'
        xpos (1170 if touch else 1176) ypos (30 if touch else 34) xysize ((64,64) if touch else (52,52))
        background None hover_background Solid('#fff6e214')
        action Hide('r13_fork_screen') alt '닫기'
        add R13_NIGHT_UI+'close_x.png' align (.5,.5)
    add R13_NIGHT_UI+'diamond.png' xpos 56 ypos 99
    add Solid('#c9a86a99') xpos 66 ypos 103 xsize 1156 ysize 1
    # Legend (mockup row): this run, other runs, unseen (count only), a fate meeting.
    hbox:
        xpos 64 ypos 116 spacing 26
        hbox:
            spacing 8
            add Solid('#d9b46c') xysize (26,2) yalign .5
            text '이번 회차' size small color '#e3d6bd' font r13_ui_font()
        hbox:
            spacing 8
            add R13ForkDash(26,2,True) yalign .5
            text '다른 회차에서 본 결과' size small color '#e3d6bd' font r13_ui_font()
        hbox:
            spacing 6
            add R13AntiqueIcon('lock',size=18) yalign .5
            text '아직 보지 못한 결과 (개수만)' size small color '#e3d6bd' font r13_ui_font()
        hbox:
            spacing 6
            add R13ForkBadge(22) yalign .5
            text '누군가의 운명이 갈린 회의' size small color '#e3d6bd' font r13_ui_font()
    $ fate_box = None
    for offset,column in enumerate(columns[first:first+6]):
        $ cx = 68+offset*194
        text r13_fork_day_label(column['day']) xpos (cx+87) xanchor .5 ypos 150 size small color '#cdbb98' font r13_ui_font()
        if column['key'] is None:
            frame:
                xpos cx ypos 200 xsize 175 ysize 116 padding (8,8) background R13ForkDash(175,116)
                text '…\n아직 펼치지 않은\n이야기' align (.5,.5) text_align .5 size small color '#b8b0a2' font r13_ui_font()
        else:
            text column['title'] xpos (cx+87) xanchor .5 ypos 170 size (22 if touch else 24) color '#f6ecd8' font r13_ui_font()
            if first+offset<len(columns)-1 and offset<5:
                add Solid('#c9a86a99' if column['here'] else '#d9b46c') xpos (cx+175) ypos 257 xysize (19,2)
            $ row_ys = r13_fork_row_tops(column['rows'])
            for ri,row in enumerate(column['rows']):
                fixed:
                    xpos cx ypos row_ys[ri] xysize (175,(56 if row['kind']=='locked' else 116))
                    use r13_fork_card(column,row,small)
            if len(row_ys)>1:
                add R13ForkDash(2,row_ys[-1]+28-258) xpos (cx-10) ypos 258
                for tick_y in row_ys[1:]:
                    add R13ForkDash(10,2,True) xpos (cx-10) ypos (tick_y+28)
            if column['fate']:
                button:
                    xpos (cx+175-(56 if touch else 44)) ypos 200 xysize ((56,56) if touch else (44,44))
                    background None hover_background None
                    action SetScreenVariable('fate_open',None if fate_open==column['key'] else column['key'])
                    hovered SetScreenVariable('fate_open',column['key'])
                    unhovered SetScreenVariable('fate_open',None)
                    alt R13_FORK_FATE_LINE
                    add R13ForkBadge(32) align (.5,.5)
                if fate_open==column['key']:
                    $ fate_box = (min(max(40,cx+175-246),1000),326)
    # The fate line is drawn last so it sits above the cards below it.
    if fate_box:
        button:
            xpos fate_box[0] ypos fate_box[1] xsize 236 padding (14,10)
            background Frame(R13_NIGHT_UI+'preview_box.png',8,8)
            action SetScreenVariable('fate_open',None) alt R13_FORK_FATE_LINE
            text R13_FORK_FATE_LINE size small color '#f6ecd8' font r13_ui_font() xsize 208
    add R13_NIGHT_UI+'diamond.png' xpos 56 ypos (by-18)
    add Solid('#c9a86a99') xpos 66 ypos (by-14) xsize 1156 ysize 1
    text '지나온 길을 모아, 다음 이야기를 찾아요.' xpos 64 ypos (by+ch//2) yanchor .5 size small color '#cdbb98' font r13_ui_font()
    viewport:
        area (470,by,390,ch) draggable True mousewheel 'horizontal'
        hbox:
            spacing 16 yalign .5
            for ending,record in sorted((persistent.r13_fork_endings or {}).items()):
                hbox:
                    spacing 8
                    add Transform(r13_fork_image(record),xysize=(72,41),nearest=True) yalign .5
                    vbox:
                        yalign .5
                        text ('지난 결말 · %d회차'%record['run']) size small color '#b8b0a2' font r13_ui_font()
                        text R13_FORK_ENDINGS.get(ending,'') size small color '#e3d6bd' font r13_ui_font()
    fixed:
        xpos 880 ypos by xysize (80,ch)
        use r13_control('‹',None,SetScreenVariable('first',max(0,first-1)),width=80,enabled=first>0,control_id='r13_fork_prev')
    fixed:
        xpos 972 ypos by xysize (80,ch)
        use r13_control('›',None,SetScreenVariable('first',min(max(0,len(columns)-6),first+1)),width=80,enabled=first+6<len(columns),control_id='r13_fork_next')
    fixed:
        xpos 1080 ypos by xysize (136,ch)
        use r13_control('닫기',None,Hide('r13_fork_screen'),width=136,control_id='r13_fork_done')
    key 'K_LEFT' action SetScreenVariable('first',max(0,first-1))
    key 'K_RIGHT' action SetScreenVariable('first',min(max(0,len(columns)-6),first+1))
    key 'game_menu' action Hide('r13_fork_screen')

# Kept after the screens: dev/test_fork_screen.py runs only the init 322 block, without Ren'Py.
init 323 python:
    class R13ForkBadge(renpy.Displayable):
        """Small "?" person badge: a gold ring, a person outline and a question mark."""
        def __init__(self,size=32,**kwargs):
            super(R13ForkBadge,self).__init__(**kwargs)
            self.size=size
        def render(self,width,height,st,at):
            s=self.size;r=renpy.Render(s,s);c=r.canvas();m=s//2
            c.circle('#d9b46c',(m,m),m-1)
            c.circle('#2b211b',(m,m),m-3)
            c.circle('#f1e6d0',(m-s//8,m-s//8),max(2,s//9))
            c.polygon('#f1e6d0',[(m-s//8-s//5,m+s//4),(m-s//8+s//5,m+s//4),(m-s//8+s//8,m+s//16),(m-s//8-s//8,m+s//16)])
            q=renpy.render(Text('?',font=r13_ui_font(),size=max(10,s//2-2),color='#f2d28d'),s,s,st,at)
            r.blit(q,(m+s//10,max(0,m-s//3)))
            return r

    class R13ForkDash(renpy.Displayable):
        """A dashed gold line (horizontal or vertical), or a dashed box when both sides are long."""
        def __init__(self,width,height,horizontal=False,**kwargs):
            super(R13ForkDash,self).__init__(**kwargs)
            self.w=max(1,int(width));self.h=max(1,int(height));self.horizontal=horizontal
        def render(self,width,height,st,at):
            w,h=self.w,self.h
            if w>4 and h>4:
                # As a frame background the box takes the frame's size.
                w=max(1,int(width)) or w;h=max(1,int(height)) or h
            r=renpy.Render(w,h);c=r.canvas();col='#c9a86a99'
            if w>4 and h>4:
                for x in range(0,w,10):
                    c.rect(col,(x,0,min(5,w-x),1));c.rect(col,(x,h-1,min(5,w-x),1))
                for y in range(0,h,10):
                    c.rect(col,(0,y,1,min(5,h-y)));c.rect(col,(w-1,y,1,min(5,h-y)))
            elif self.horizontal or w>h:
                for x in range(0,w,6):c.rect(col,(x,0,min(3,w-x),h))
            else:
                for y in range(0,h,6):c.rect(col,(0,y,w,min(3,h-y)))
            return r
