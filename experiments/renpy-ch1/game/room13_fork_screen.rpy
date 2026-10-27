# Read-only recollections. No unlocks, travel, rollback, or automatic opening.
default persistent.r13_fork_runs = 0
default persistent.r13_fork_seen = {}
default persistent.r13_fork_endings = {}
# 실행 중 win→grand 관찰을 구분하는 기록용 되돌림 정보(이야기 값 아님).
default r13_fork_win_prior = {}

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
    R13_FORK_RESULTS = dict(win='이김',partial='부분',lose='짐',grand='대승리')
    R13_FORK_GRAND_MEETINGS = frozenset(('fire','soup'))
    # 0.20.5 (Codex S01): the final results each meeting really has (r13_nw_meeting_end calls in
    # room13_v111_days*.rpy; dev/test_fork_screen.py re-derives this). A retry is not a result.
    R13_FORK_OUTCOMES = dict(gate=('win','lose'),gate_post=('win','lose'),piko=('win','lose'))
    def r13_fork_outcomes(meeting):
        if meeting in R13_FORK_FATE_RESULTS:return tuple(r for r,_ in R13_FORK_FATE_RESULTS[meeting])
        base=R13_FORK_OUTCOMES.get(meeting,('win','partial','lose'))
        return base+('grand',) if meeting in R13_FORK_GRAND_MEETINGS else base
    # 0.20.20 (소유자 2026-10-23 "다 해 줘", 승인 시안 docs/reviews/future-keys-20261023/fork_after_ending.png):
    # 회의 사이에 생사가 갈리는 판정 시점 칸을 넣는다. 이번 판의 결과만 이름이 보이고 나머지는 개수만.
    R13_FORK_FATE_POINTS = (
        ('fate_piko','3번 등 앞','2일 저녁','square'),
        ('fate_kkomi','장작 창고','6일 저녁','square'),
        ('fate_owl','13호','7일 밤','room13'),
        ('fate_nero','아랫길','11일 밤','square'),
        ('fate_soup','학교 배식','12일 낮','dining'),
        ('fate_crowd','광장','13일','square'))
    R13_FORK_FATE_RESULTS = dict(
        fate_piko=(('saved','들임'),('lost','꺼진 등')),
        fate_kkomi=(('saved','넷 인계'),('lost','타 버린 창고')),
        fate_owl=(('stone','식은 돌'),('promise','내려가지 않은 당번'),('repair','곁에 남은 수리공'),('lost','닫힌 문')),
        fate_nero=(('handover','인계'),('rescue','구조'),('lost','끊긴 등불')),
        fate_soup=(('early','조기 예방'),('premeal','먹기 전 중단'),('lost','작은 냄비')),
        fate_crowd=(('supervisor','감독자'),('block','막아섬'),('riot','올라간 주먹')))
    # 날짜 순서. 같은 날은 일어나는 차례대로(11일 회의 뒤 밤 출발, 12일 배식 뒤 수프 회의, 13일 회의 뒤 공개).
    R13_FORK_ORDER = ('gate','fate_piko','lamp','gate_post','fate_kkomi','fire','fate_owl','room13','records',
        'hypothesis','fate_nero','fate_soup','soup','blanket','piko','fate_crowd','altar')
    def r13_fork_points():
        spec = dict((m[0],m) for m in R13_FORK_MEETINGS+R13_FORK_FATE_POINTS)
        return [spec[k] for k in R13_FORK_ORDER]
    def r13_fork_is_fate_point(key):
        return key in R13_FORK_FATE_RESULTS
    def r13_fork_value(key):
        result=r13_v111_value(('fate:' if r13_fork_is_fate_point(key) else 'meeting:')+key)
        return 'grand' if key in R13_FORK_GRAND_MEETINGS and result=='win' and r13_v111_value('grand:'+key) is True else result
    def r13_fork_result_name(key,result):
        if r13_fork_is_fate_point(key):return dict(R13_FORK_FATE_RESULTS[key]).get(result,'지나감')
        return R13_FORK_RESULTS.get(result,'지나감')
    def r13_fork_set_fate(key,result):
        """판정 시점의 결과를 이번 판에 적고(한 번만) 갈림길 기록에 남긴다."""
        if r13_v111_value('fate:'+key) is None:
            r13_v111_set('fate:'+key,result)
            r13_fork_record(key,result)

    R13_FORK_ENDINGS = dict(left_name='남겨진 이름',frozen='얼어붙은 마을',family='가족을 택한 밤',partial='남은 사람들',violence='상처 입은 귀환',morning='마을의 아침',true='새로운 아침',wild_night='불타는 밤')

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
        if meeting not in R13_FORK_ORDER or result not in r13_fork_outcomes(meeting):return
        seen = dict(persistent.r13_fork_seen or {})
        run=store.room13['v111'].get('fork_run',1)
        if meeting in R13_FORK_GRAND_MEETINGS and result=='win':
            if r13_v111_value('grand:'+meeting) is True:
                result='grand'
            else:
                prior=dict(getattr(store,'r13_fork_win_prior',{}) or {})
                # 같은 결과를 반복 기록해도 원래 회차의 이김을 잃지 않는다.
                if meeting not in prior or prior[meeting]['run']!=run:
                    prior[meeting]=dict(run=run,previous=seen.get((meeting,'win')))
                store.r13_fork_win_prior=prior
        seen[(meeting,result)] = dict(png=r13_fork_capture(),run=store.room13['v111'].get('fork_run',1))
        persistent.r13_fork_seen = seen
        renpy.save_persistent()

    def r13_fork_promote_grand(meeting):
        """이야기에서 확정한 grand만 관찰한다. 화면을 여는 행위는 기록하지 않는다."""
        if meeting not in R13_FORK_GRAND_MEETINGS or r13_fork_value(meeting)!='grand':return
        run=store.room13['v111'].get('fork_run',1)
        seen=dict(persistent.r13_fork_seen or {})
        prior=dict(getattr(store,'r13_fork_win_prior',{}) or {})
        win=seen.get((meeting,'win'))
        saved=prior.get(meeting)
        # 이 실행에서 잠정 수집한 win만 교체한다. 구판 기록은 추측해서 삭제하지 않는다.
        if saved and saved['run']==run and win and win.get('run',1)==run:
            if saved['previous'] is None:seen.pop((meeting,'win'),None)
            else:seen[(meeting,'win')]=saved['previous']
            prior.pop(meeting,None)
            store.r13_fork_win_prior=prior
        seen[(meeting,'grand')]=dict(png=r13_fork_capture(),run=run)
        persistent.r13_fork_seen=seen
        renpy.save_persistent()

    def r13_fork_ending(key):
        if key not in R13_FORK_ENDINGS:return
        endings = dict(persistent.r13_fork_endings or {})
        endings[key] = dict(png=r13_fork_capture(),run=store.room13['v111'].get('fork_run',1))
        persistent.r13_fork_endings = endings
        renpy.save_persistent()

    def r13_fork_current():
        points = r13_fork_points()
        claim = getattr(store,'r13_meeting_claim',None)
        if getattr(store,'r13_meeting_active',False) and claim:
            for i,m in enumerate(points):
                if claim == 'NW:'+m[0]:return i
        decided = [i for i,m in enumerate(points) if r13_fork_value(m[0]) in r13_fork_outcomes(m[0])]
        return min(len(points)-1,max(decided)+1) if decided else 0

    # 0.20.x 갈림길 (owner-approved plan5 m4, 2026-10-22): a meeting whose result decides someone's
    # fate carries a "?" person badge and the line R13_FORK_FATE_LINE. Never who, never the
    # conditions, never life or death. A meeting is listed here when one of its result paths in
    # room13_v111_days*.rpy writes a name on the transfer list (r13_nw_list, room13_v111_newworld_rules),
    # sends people away on the cart (departed:), takes someone into custody (DARAM_DETAINED,
    # grandmother_custody) or ends a life (*_alive False). dev/test_fork_screen.py re-derives the
    # set from those labels, so a new fate effect in a meeting shows up as a test failure.
    R13_FORK_FATE = frozenset(('lamp','gate_post','fire','room13','records','soup','blanket','altar'))
    R13_FORK_FATE_LINE = '여기서 누군가의 운명이 갈렸다.'

    def r13_fork_fate(meeting):
        """Badge only on a meeting already decided in this run (never on the one still ahead)."""
        if r13_fork_is_fate_point(meeting):return r13_fork_value(meeting) in r13_fork_outcomes(meeting)
        return meeting in R13_FORK_FATE and r13_v111_value('meeting:'+meeting) in R13_FORK_RESULTS

    def r13_fork_day_label(day):
        return day.replace('일','일째',1) if day and '일' in day else day

    def r13_fork_columns():
        current = r13_fork_current()
        seen = persistent.r13_fork_seen or {}
        columns = []
        points = r13_fork_points()
        for i,(key,title,day,place) in enumerate(points):
            if i>current:break
            result = r13_fork_value(key)
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
        if current<len(points)-1:columns.append(dict(key=None,day='그 너머',rows=[]))
        return columns

    def r13_fork_image(record,place='square'):
        if record and record.get('png'):
            return im.Data(record['png'],'fork.png')
        place = place if place in R13_PLACES else 'square'
        return r13_background(R13_PLACES[place][1])

    def r13_fork_initial_page():
        return min(max(0,len(r13_fork_columns())-6),max(0,min(r13_fork_current(),len(R13_FORK_ORDER)-2)-4))

    # 2026-10-27: 종이 안(636) 하단 버튼 줄(휴대폰 80) 위에 세 줄이 들어오도록 시작 178·간격 8.
    def r13_fork_row_tops(rows,top=178,gap=8):
        """Card tops in one column: result cards are 116 high, the count lock 56."""
        tops=[];y=top
        for row in rows:
            tops.append(y);y+=(56 if row['kind']=='locked' else 116)+gap
        return tops

screen r13_fork_card(column,row,small=16):
    # 0.20.x: brown sheet and result cards as the approved mockup (plan5 m4_forks.png).
    if row['kind']=='locked':
        frame:
            xsize 175 ysize 56 padding (12,8) background r13_field_paper()
            hbox:
                align (.5,.5) spacing 10
                add R13AntiqueIcon('lock',size=22) yalign .5
                text ('다른 결과 %d'%row.get('count',1)) size (small+2) color '#354151' font R13_UI_BOLD_FONT yalign .5
    elif column['here']:
        frame:
            xsize 175 ysize 116 padding (8,8) background R13ControlSurface(primary=True)
            vbox:
                align (.5,.5) spacing 6
                add r13_asset_path("file:"+(R13_NIGHT_UI+'diamond.png')) xalign .5
                text '지금 여기' size (small+6) color '#fff6e2' font R13_UI_BOLD_FONT xalign .5
                text '결과 미정' size small color '#f2d28d' font R13_UI_BOLD_FONT xalign .5
    else:
        $ result_label=r13_fork_result_name(column['key'],row['result'])
        # Longer fate labels may use two lines; the run caption always has its own row.
        $ thumb_height=30 if len(result_label)>7 else 54
        frame:
            xsize 175 ysize 116 padding (12,8) background r13_field_paper()
            fixed:
                xysize (151,100)
                viewport:
                    xysize (151,thumb_height)
                    add Transform(r13_fork_image(row['record'],column['place']),xysize=(151,thumb_height),fit='cover',matrixcolor=SepiaMatrix() if row['kind']=='old' else BrightnessMatrix(0))
                text result_label xpos 0 ypos (thumb_height+2) xsize 151 size (small+2) line_spacing -2 color '#263b52' font R13_UI_BOLD_FONT
                text ('이번 회차' if row['kind']=='current' else '%d회차에서 봄'%(row['record'] or {}).get('run',1)) xpos 0 ypos 82 xsize 151 size r13_type("small") color '#756f66' font R13_UI_BOLD_FONT

screen r13_fork_card_stack(column,small,height):
    default scroll=ui.adjustment()
    viewport:
        xsize 175 ysize height
        yadjustment scroll mousewheel True draggable True
        vbox:
            spacing 16
            for row in column['rows']:
                use r13_fork_card(column,row,small)
    if scroll.range>0:
        vbar:
            xpos 177 xsize 4 ysize height adjustment scroll
            base_bar Solid('#d8c8b0') thumb Solid('#82684d')

screen r13_fork_screen():
    modal True
    zorder 65
    default first = r13_fork_initial_page()
    default fate_open = None
    $ columns = r13_fork_columns()
    $ touch = r13_touch_ui()
    $ small = 18 if touch else 16
    $ ch = r13_control_height()
    $ by = R13_NB_BOTTOM-ch   # 2026-10-27: 하단 버튼 줄도 종이 안(636)으로
    # 2026-10-27 수첩 공통 틀(systems/room13_notebook_shell.rpy): 판·제목·부제·회차·닫기 X·금색 선은 기록 화면과 같은 자리.
    use r13_notebook_shell('이야기의 갈림길',subtitle='기록 / 지나온 이야기',close_action=Hide('r13_fork_screen'),
        stamp=('%d회차 · %d일째' % (room13['v111'].get('fork_run',1),room13['day'])),rule_y=149)
    # Legend (mockup row): this run, other runs, unseen (count only), a fate meeting.
    hbox:
        xpos 114 ypos 162 spacing 22
        hbox:
            spacing 8
            add Solid('#d9b46c') xysize (26,2) yalign .5
            text '이번 회차' size small color '#354151' font R13_UI_BOLD_FONT
        hbox:
            spacing 8
            add R13ForkDash(26,2,True) yalign .5
            text '다른 회차에서 본 결과' size small color '#354151' font R13_UI_BOLD_FONT
        hbox:
            spacing 6
            add R13AntiqueIcon('lock',size=18) yalign .5
            text '아직 보지 못한 결과 (개수만)' size small color '#354151' font R13_UI_BOLD_FONT
        hbox:
            spacing 6
            add R13ForkBadge(22) yalign .5
            text '누군가의 운명이 갈린 곳' size small color '#354151' font R13_UI_BOLD_FONT
    $ fate_box = None
    for offset,column in enumerate(columns[first:first+6]):
        $ cx = 110+offset*182
        text r13_fork_day_label(column['day']) xpos (cx+87) xanchor .5 ypos 202 size small color '#756f66' font R13_UI_BOLD_FONT
        if column['key'] is None:
            frame:
                xpos cx ypos 264 xsize 175 ysize 116 padding (8,8) background R13ForkDash(175,116)
                text '…\n아직 펼치지 않은\n이야기' align (.5,.5) text_align .5 size small color '#756f66' font R13_UI_BOLD_FONT
        else:
            text column['title'] xpos (cx+87) xanchor .5 ypos 230 xmaximum 175 text_align .5 size (21 if touch else 22) color '#263b52' font R13_UI_BOLD_FONT
            if first+offset<len(columns)-1 and offset<5:
                add Solid('#c9a86a99' if column['here'] else '#d9b46c') xpos (cx+175) ypos 321 xysize (7,2)
            fixed:
                area (cx,264,182,by-288)
                use r13_fork_card_stack(column,small,by-288)
            if column['fate']:
                button:
                    xpos (cx+175-(56 if touch else 44)) ypos 264 xysize ((56,56) if touch else (44,44))
                    background None hover_background None
                    action SetScreenVariable('fate_open',None if fate_open==column['key'] else column['key'])
                    hovered SetScreenVariable('fate_open',column['key'])
                    unhovered SetScreenVariable('fate_open',None)
                    alt R13_FORK_FATE_LINE
                    add R13ForkBadge(32) align (.5,.5)
                if fate_open==column['key']:
                    $ fate_box = (min(max(40,cx+175-246),1000),388)
    # The fate line is drawn last so it sits above the cards below it.
    if fate_box:
        button:
            xpos fate_box[0] ypos fate_box[1] xsize 236 padding (14,10)
            background R13PaperFrame()
            action SetScreenVariable('fate_open',None) alt R13_FORK_FATE_LINE
            text R13_FORK_FATE_LINE size small color '#263b52' font R13_UI_BOLD_FONT xsize 208
    # 2026-10-27: 안내 글과 지난 결말 띠가 종이 가장자리(646) 아래에 걸쳤다. 버튼 줄은 그대로 두고 이 띠만 종이 안(640 위)으로 올린다.
    $ fy = by
    add r13_asset_path("file:"+(R13_NIGHT_UI+'diamond.png')) xpos 114 ypos (fy-18)
    add Solid('#c9a86a99') xpos 114 ypos (fy-14) xsize (R13_NB_RIGHT-114) ysize 1
    text '지나온 길을 모아, 다음 이야기를 찾아요.' xpos 114 ypos (fy+ch//2) yanchor .5 size small color '#756f66' font R13_UI_BOLD_FONT
    viewport:
        area (470,fy,R13_NB_RIGHT-R13_NB_BUTTON_W-2*R13_NB_GAP-160-12-470,ch) draggable True mousewheel 'horizontal'
        hbox:
            spacing 16 yalign .5
            for ending,record in sorted((persistent.r13_fork_endings or {}).items()):
                hbox:
                    spacing 8
                    add Transform(r13_fork_image(record),xysize=(72,41),fit='cover') yalign .5
                    vbox:
                        yalign .5
                        text ('지난 결말 · %d회차'%record['run']) size small color '#756f66' font R13_UI_BOLD_FONT
                        text R13_FORK_ENDINGS.get(ending,'') size small color '#354151' font R13_UI_BOLD_FONT xsize 220
    fixed:
        xpos (R13_NB_RIGHT-R13_NB_BUTTON_W-2*R13_NB_GAP-160) ypos by xysize (80,ch)
        use r13_control('‹',None,SetScreenVariable('first',max(0,first-1)),width=80,enabled=first>0,control_id='r13_fork_prev')
    fixed:
        xpos (R13_NB_RIGHT-R13_NB_BUTTON_W-R13_NB_GAP-80) ypos by xysize (80,ch)
        use r13_control('›',None,SetScreenVariable('first',min(max(0,len(columns)-6),first+1)),width=80,enabled=first+6<len(columns),control_id='r13_fork_next')
    use r13_nb_footer_button(0,'닫기',Hide('r13_fork_screen'),control_id='r13_fork_done')
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
            q=renpy.render(Text('?',font=R13_UI_BOLD_FONT,size=max(10,s//2-2),color='#f2d28d'),s,s,st,at)
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

# 기존 스토리 setter를 바꾸지 않고 확정 이벤트의 회상 기록만 관찰한다.
init 331 python:
    _r13_fork_observed_set=r13_v111_set
    def r13_v111_set(key,value):
        before=r13_v111_value(key)
        result=_r13_fork_observed_set(key,value)
        if value is True and before is not True and key in ('grand:fire','grand:soup'):
            r13_fork_promote_grand(key.split(':',1)[1])
        return result
