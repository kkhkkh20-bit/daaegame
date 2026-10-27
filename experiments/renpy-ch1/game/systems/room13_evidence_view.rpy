# 증거 비교 창 (owner-approved plan5 mockups m2a/m2b, 2026-10-22:
# docs/reviews/plan5-20261022/m2a_compare_one.png, m2b_compare_two.png).
# The 자료 tab of 기록 and the 보여주기 book share one browser:
#   left   small pictures (page grid), "자료 N개 · 1-2일째"
#   centre one big picture (about 360px) and 2-3 short observed facts
#   right  hint / the long original text inside 「출처 펼치기」, then the buttons
# 「나란히 놓기」 puts a second record beside the first: two equal columns, each a big picture
# and its facts. No right/wrong marks and no highlighting; the player compares.
# Data hooks (content is written elsewhere, everything falls back):
#   picture  game/assets/evidence/<key>.webp (key without "V111:"), else r13_record_icon(key)
#            scaled up with nearest-neighbour. Testimony keeps the speaker's portrait.
#   facts    game/v111/evidence-facts.json {"<key>": {"<variant>": ["line", ...]}}, the variant
#            held in this run (<key>.variant, set by the V1.1.1 'acquire' operation); else the
#            record text split into at most three short sentences.
# Presentation only: nothing here grants, reveals or changes a record.
init 330 python:
    import json as _r13_ev_json
    # 0.20.6 (Codex R03): in the Ren'Py store `dict`/`list` name the revertable types, so a plain
    # JSON dict failed isinstance(data,dict) and every authored summary was dropped. Check shape.
    from collections.abc import Mapping as _R13EvMapping, Sequence as _R13EvSequence
    def _r13_ev_is_lines(value):
        return isinstance(value,_R13EvSequence) and not isinstance(value,str)
    R13_EVIDENCE_FACTS_PATH="v111/evidence-facts.json"
    R13_EVIDENCE_ART_DIR="assets/evidence/"
    R13_EVIDENCE_FACT_LIMIT=3
    # 2026-10-27 수첩 공통 틀(systems/room13_notebook_shell.rpy): 내용은 R13_NB_INNER(132,140 ~ 1206,684) 안에만.
    #   왼쪽 목록 136~392, 세로 선 406, 가운데 420~890, 오른쪽 열 910~1206(버튼 폭 296 그대로).
    #   제목이 갈림길과 같은 x114 로 가서 첫 탭은 220 부터, 90 간격. 아래는 갈림길 하단 버튼 줄과 같은 684.
    R13_EV_BOTTOM=globals().get("R13_NB_BOTTOM",636)
    R13_EV_TAB_X=220
    R13_EV_TAB_PITCH=90
    R13_EV_TITLE_X=globals().get("R13_NB_TITLE_X",114)
    R13_EV_TOP=globals().get("R13_NB_TOP",140)      # 목록 머리글·가운데 제목·오른쪽 열의 위
    R13_EV_ROWS_Y=R13_EV_TOP+28                      # 목록 첫 줄
    R13_EV_GRID_X=136
    R13_EV_GRID_W=256
    R13_EV_DIVIDER_X=406
    R13_EV_CENTER_X=420
    R13_EV_CENTER_W=470
    R13_EV_RIGHT_X=910
    R13_EV_RIGHT_W=296
    R13_EV_RIGHT=globals().get("R13_NB_RIGHT",1206)
    R13_EV_TEXT_BOTTOM=globals().get("R13_NB_TEXT_BOTTOM",640)   # 맨글씨·뷰포트는 종이 안에서 끝난다

    def r13_evidence_facts_load(path=None):
        path=path or R13_EVIDENCE_FACTS_PATH
        if not renpy.loadable(path):return {}
        try:
            with renpy.file(path) as source:data=_r13_ev_json.load(source)
        except Exception:
            return {}
        return data if isinstance(data,_R13EvMapping) else {}
    R13_EVIDENCE_FACTS=r13_evidence_facts_load()

    def r13_evidence_base_key(key):
        """Content key of a V1.1.1/new-world record: 'V111:E01' -> 'E01'. Older records have none."""
        if isinstance(key,str) and key.startswith("V111:") and len(key)>5:return key[5:]
        return None

    def r13_evidence_variant(key):
        """The variant of this record held in the current run (first authored variant if unset)."""
        base=r13_evidence_base_key(key)
        if base is None:return None
        held=None
        try:
            if r13_v111_active():held=r13_v111_value(base+".variant")
        except Exception:
            held=None
        if held:return held
        variants=list((R13_V111.get("evidence",{}).get(base) or {}).get("variants",{}))
        return variants[0] if variants else None

    def r13_evidence_split(text,limit=R13_EVIDENCE_FACT_LIMIT,width=26):
        """Fallback facts: the record text as at most `limit` short lines.
        Short list items are packed together with ' · '; asides in brackets are left to the
        full text in 「출처 펼치기」 (owner: no answer clue written into the observed facts)."""
        import re
        text=re.sub(r"\s*[(（][^()（）]*[)）]","",str(text or ""))
        text=re.sub(r"\s*\{image=[^}]*\}","",text)  # 0.20.5: an inline mark belongs to the picture, not a fact line
        pieces=[]
        for chunk in re.split(r"\n+",text):
            for sentence in re.split(r"(?<=[.!?。…])\s+",chunk.strip()):
                sentence=sentence.strip(" ·")
                if sentence:pieces.append(sentence)
        lines=[]
        for piece in pieces:
            if lines and not re.search(r"[.!?。…]$",lines[-1]) and len(lines[-1])+3+len(piece)<=width:
                lines[-1]+=" · "+piece
            else:
                lines.append(piece)
        if len(lines)>limit:
            lines=lines[:limit]
            lines[-1]=lines[-1].rstrip(" .")+" …"
        return lines

    def r13_evidence_facts(key):
        base=r13_evidence_base_key(key)
        spec=R13_EVIDENCE_FACTS.get(base) if base else None
        if isinstance(spec,_R13EvMapping):
            # 0.20.5 (Codex B03): a later status (E35.status=received) outranks the acquired variant.
            status=None
            try:
                if r13_v111_active():
                    status=r13_v111_value(base+".status")
                    if base=="E09" and r13_v111_value("portrait")=="child_completed":status="child_completed"
            except Exception:
                status=None
            lines=spec.get(status) if status in spec else spec.get(r13_evidence_variant(key))
            if _r13_ev_is_lines(lines):
                lines=[str(line).strip() for line in lines if str(line).strip()]
                if lines:return lines[:R13_EVIDENCE_FACT_LIMIT]
        record=r13_catalog_record(key)
        return r13_evidence_split(r13_material_body(record)) if record else []

    _r13_evidence_art_cache={}
    def r13_evidence_art_path(key):
        base=r13_evidence_base_key(key)
        if not base:return None
        if base not in _r13_evidence_art_cache:
            path=R13_EVIDENCE_ART_DIR+base+".webp"
            _r13_evidence_art_cache[base]=path if renpy.loadable(path) else None
        return _r13_evidence_art_cache[base]

    def r13_evidence_portrait_person(key):
        if key not in ROOM13["evidence"] or r13_record_category(key)!="testimony":return None
        return ROOM13["evidence_sources"].get(key)

    def r13_evidence_picture(key,size):
        """The big picture: authored evidence art, else the list icon enlarged without smoothing."""
        if not r13_evidence_portrait_person(key):
            path=r13_evidence_art_path(key)
            if path:return Transform(path,xysize=(size,size),fit="contain",nearest=True)
        return Transform(r13_record_icon(key),xysize=(size,size),fit="contain",nearest=True)

    def r13_evidence_day_span(entries):
        records=(store.room13 or {}).get("records",{}) or {}
        days=sorted({records[k]["day"] for k in entries if isinstance(records.get(k),dict) and records[k].get("day") is not None})
        if not days:return ""
        return ("%d일째"%days[0]) if days[0]==days[-1] else ("%d-%d일째"%(days[0],days[-1]))

    def r13_evidence_kind_label(key):
        record=r13_catalog_record(key) or {}
        return record.get("kind") or "자료"

    def r13_ev_title_width(title,size=34):
        return sum(int(size*.3) if ch==" " else size for ch in str(title))
    def r13_ev_tab_x(title):
        """0.20.5 (UI review): the first tab starts after the sheet title, never under it.
        2026-10-27 공통 틀: 제목은 x114(갈림길과 같다), 크기는 hero 단계."""
        size=(r13_type("display"))
        return max(R13_EV_TAB_X,R13_EV_TITLE_X+r13_ev_title_width(title,size)+24)
    def r13_ev_text_units(text):
        # 0.20.12: a space or Latin letter is narrower than a Hangul syllable.
        return sum(.35 if c==" " else (.55 if ord(c)<0x1100 else 1.0) for c in text)

    def r13_ev_two_lines(text,width,size,max_lines=2):
        """0.20.5 (UI review): a grid name in at most two lines at this width, then "…".
        Words stay whole when they fit; a word longer than a line is cut.
        0.20.12: widths count Hangul as one unit and spaces/Latin as less, and the PC grid may use three lines."""
        cap=max(2.0,float(width)/max(1,size))
        units=r13_ev_text_units
        # Prefer complete words and balanced lines. In particular, never leave the final
        # "장" of "반쯤 탄 수첩 장" alone merely because a greedy line was almost full.
        words=str(text).replace("·","· ").split()
        def partitions(start,remaining):
            if start==len(words):return [()]
            if not remaining:return []
            candidates=[]
            for end in range(start+1,len(words)+1):
                line=" ".join(words[start:end])
                if units(line)>cap:break
                candidates.extend((line,)+tail for tail in partitions(end,remaining-1))
            return candidates
        candidates=partitions(0,max_lines)
        if candidates:
            def cost(lines):
                lengths=[units(line) for line in lines]
                orphan=100 if len(lines)>1 and lengths[-1]<=1 else 0
                punctuation=sum(100 for line in lines if line.startswith("·"))
                return (len(lines),orphan+punctuation+max(lengths)-min(lengths))
            return "\n".join(min(candidates,key=cost))
        lines=[""]
        for word in str(text).split(" "):
            while word:
                room=cap-units(lines[-1])-(.35 if lines[-1] else 0)
                if units(word)<=room:
                    lines[-1]=(lines[-1]+" "+word) if lines[-1] else word;word=""
                elif lines[-1] and units(word)<=cap:
                    lines.append("")
                else:
                    cut=1
                    while cut<len(word) and units(word[:cut+1])<=room:cut+=1
                    lines[-1]=(lines[-1]+(" " if lines[-1] else "")+word[:cut]);word=word[cut:]
                    if word:lines.append("")
        if len(lines)>max_lines:
            lines=lines[:max_lines];last=lines[-1]
            while last and units(last)+1>cap:last=last[:-1]
            lines[-1]=last.rstrip()+"…"
        return "\n".join(lines)

    def r13_evidence_short(key,limit):
        name=R13_RECORD_SHORT.get(key) or r13_catalog_title(key)
        return name if len(name)<=limit else name[:max(1,limit-1)]+"…"

    # Comparison state: a pair (slot 1, slot 2) and the slot a tapped picture fills.
    def r13_compare_slots(pair):
        slots=(tuple(pair or ())+(None,None))[:2]
        return slots[0],slots[1]

    def r13_compare_begin(detail):
        return (detail,None)

    def r13_compare_fill(pair,slot,key):
        """While comparing, a tapped picture fills the chosen slot. A record never fills both."""
        slots=list(r13_compare_slots(pair))
        if key is None or key in slots:return tuple(slots)
        slots[1 if slot else 0]=key
        return tuple(slots)

    def r13_compare_swap(pair):
        a,b=r13_compare_slots(pair)
        return (b,a)

    def r13_compare_single(pair):
        a,b=r13_compare_slots(pair)
        return a if a is not None else b

    def r13_compare_live(pair,known=None):
        """Drop records that no longer exist (old save, consumed item); no pair when both are gone."""
        if not pair:return None
        known=known or (lambda key:r13_catalog_record(key) is not None)
        a,b=[key if key is not None and known(key) else None for key in r13_compare_slots(pair)]
        return (a,b) if (a is not None or b is not None) else None

    def r13_compare_page(entries,key):
        return entries.index(key)//r13_record_page_size() if key in entries else 0

    def r13_ev_text_lines(text,width,size):
        """Rough rendered line count of one wrapped line of text (Korean glyphs about `size` wide)."""
        import math
        units=sum(.3 if ch==" " else 1 for ch in str(text))
        return max(1,int(math.ceil(units*size/max(1,width))))
    def r13_ev_pair_picture(pair,bottom,title_size,top=None):
        """0.20.6 (Codex R04): the side-by-side picture shrinks so both titles and all fact lines
        end above the buttons (never under 180px, never over the approved 312px)."""
        top=R13_EV_TOP+26 if top is None else top
        fact=r13_ev_fact_size();need=0
        for key in r13_compare_slots(pair):
            if key is None:continue
            head=r13_ev_text_lines(r13_catalog_title(key),300,title_size)*(title_size+8)
            facts=sum(r13_ev_text_lines(line,348,fact)*(fact+6)+6 for line in r13_evidence_facts(key))
            need=max(need,head+facts+30)
        return max(180,min(312,bottom-12-top-need))
    def r13_ev_button_height():
        # 2026-10-27 공통 틀: 하단 버튼은 공통 부품(R13_CONTROL)과 같은 높이(64 / 큰 글씨 80 / 휴대폰 88).
        # 844x390 displays the 720px canvas at 0.542x: 88 becomes 47.7 CSS px (44 at 740x360).
        if r13_touch_ui():return 88
        return R13_CONTROL.get("large_height",80) if persistent.room13_large_text else R13_CONTROL.get("height",64)
    def r13_ev_grid_pitch():
        """목록 한 줄의 높이. 다섯 줄과 쪽 버튼이 틀 아래(R13_EV_BOTTOM) 안에 들어오도록 88 에서 줄인다."""
        return min(88,(R13_EV_BOTTOM-r13_ev_button_height()-8-R13_EV_ROWS_Y)//5)

    def r13_ev_small_size():
        # Touch: small text is never under 18px.
        return r13_type("small")  # 2026-10-27 타이포 시안: 15px 를 18 로 올린다

    def r13_ev_fact_size():
        return r13_type("emphasis")  # 2026-10-27 타이포 시안: 자료 본문. 휴대폰은 30 에서 26 으로 준다

    def r13_ev_reading_size():
        return r13_type("small")  # 2026-10-27 타이포 시안: 출처·안내는 PC·휴대폰 모두 small

    def r13_ev_label_size(label,width):
        # A long name in a fixed-width control shrinks instead of spilling out (never under the small size).
        normal=r13_read_size(28,30) if r13_touch_ui() else r13_read_size(R13_CONTROL["text"],R13_CONTROL["large_text"])
        fit=(width-2*R13_CONTROL["padding"])//max(1,len(label))
        return max(r13_ev_small_size(),min(normal,fit))

    def r13_ev_thumb_bg(width,height,thumb,chosen=False,hovered=False):
        # The visible tile is the thumbnail square; the whole cell (picture + name) is pressable.
        return Fixed(Transform(R13ControlSurface(chosen=chosen,hovered=hovered),xysize=(thumb,thumb),xalign=.5),xysize=(width,height))

    def r13_ev_filter_chips(owner,current,allow_transfer=True,shelf=None,shelf_count=0,archive=None):
        """Top-bar chips: the existing material filters, 지난 사건 and 지난 플레이 (each a toggle)."""
        reset=[Function(r13_record_select,owner,"detail",None,False),Function(r13_record_select,owner,"page",0,False),
            Function(r13_record_select,owner,"pair",None,False)]
        chips=[]
        for key,title in r13_material_filter_choices(current,allow_transfer):
            label="전달" if key=="transfer" and r13_touch_ui() else title
            chips.append((label,current==key,[Function(r13_record_select,owner,"material_filter",key,False)]+reset))
        if shelf is not None and (shelf_count or shelf):
            chips.append(("지난 사건",bool(shelf),[Function(r13_record_select,owner,"shelf",not shelf,False)]+reset))
        if archive is not None:
            toggle=[Function(r13_record_select,owner,"archive",not archive,False)]
            if shelf is not None or not isinstance(owner,str):toggle.append(Function(r13_record_select,owner,"shelf",False,False))
            chips.append(("지난 플레이",bool(archive),toggle+reset))
        return chips

    def r13_ev_chip_boxes(chips,right=1168,gap=6):
        size=r13_ev_small_size()
        widths=[max(96,len(label)*size+18) for label,chosen,act in chips]
        # Reserve all five tabs even when large text exposes every filter.
        left=R13_EV_TAB_X+4*R13_EV_TAB_PITCH+86+12
        available=right-left-gap*max(0,len(widths)-1)
        if widths and sum(widths)>available:
            floor=88 if r13_touch_ui() else 72
            extra=sum(w-floor for w in widths)
            ratio=max(0,available-floor*len(widths))/max(1,extra)
            widths=[floor+int((w-floor)*ratio) for w in widths]
        x=right-sum(widths)-gap*max(0,len(widths)-1)
        boxes=[]
        for w in widths:
            boxes.append((x,w));x+=w+gap
        return boxes

    def r13_ev_record_tabs(owner,present=False):
        """Top tabs of the brown records sheet. The 보여주기 book shows only 자료."""
        if present:return [("all","자료",NullAction())]
        book=isinstance(owner,str)
        tabs=[]
        for key,title in (("all","자료"),("relations","사람"),("dialogue","대화"),("notes","메모")):
            if book and key in ("relations","dialogue"):continue   # the book always shows 자료
            if book and key=="notes":action=Show("r13_learning_notes")
            else:
                action=[Function(r13_record_select,owner,"category" if book else "tab",key),Function(r13_record_select,owner,"detail",None,False),
                    Function(r13_record_select,owner,"page",0,False),Function(r13_record_select,owner,"pair",None,False)]
            tabs.append((key,title,action))
        if r13_v111_active():tabs.append(("fork","갈림길",Show("r13_fork_screen")))
        return tabs

init 331:
    style r13ev_tab_button is button:
        background None hover_background None selected_background None padding (0,0)
    style r13ev_tab_button_text is text:
        font R13_UI_BOLD_FONT size r13_type("body") color "#493323" hover_color "#8d4b2d" selected_color "#fff6e2" xalign .5 yalign .5
    style r13ev_chip_button is button:
        background r13_field_button_art() hover_background r13_field_button_art()
        selected_background r13_field_button_art(True) selected_hover_background r13_field_button_art(True)
        padding (6,2)
    style r13ev_chip_button_text is text:
        font R13_UI_BOLD_FONT color "#503525" hover_color "#8d4b2d" selected_color "#fff6e2" xalign .5 yalign .5 text_align .5

# 2026-10-27 수첩 공통 틀: 제목·탭·닫기 X·금색 선은 systems/room13_notebook_shell.rpy 의 r13_notebook_shell 이 그린다.
# 이 이름은 기록 화면과 보여주기 책(room13_screens.rpy r13_book)이 그대로 쓰므로 남긴다.
screen r13_ink_record_shell(title,tabs,current="all",close_action=None,note=None):
    use r13_notebook_shell(title,close_action=close_action,tabs=tabs,current=current,note=note)

screen r13_ink_chips(chips):
    $ touch=r13_touch_ui()
    $ boxes=r13_ev_chip_boxes(chips)
    $ chip_h=88 if touch else 40
    for index,(chip_label,chip_chosen,chip_action) in enumerate(chips):
        textbutton chip_label:
            style "r13ev_chip_button" text_style "r13ev_chip_button_text"
            xpos boxes[index][0] ypos (R13_NB_HEAD_CY-chip_h//2) xsize boxes[index][1] ysize chip_h
            text_size min(r13_ev_small_size(),(boxes[index][1]-12)//max(1,len(chip_label))) selected chip_chosen action chip_action

# Left column: small pictures, page by page. While comparing, a tap fills the chosen slot.
screen r13_evidence_grid(entries,detail,page,owner,pair=None,pair_slot=1,archive=False,header=""):
    $ touch=r13_touch_ui()
    # Full names beside their own artwork. Five rows (88px, 틀 안에 못 들어오면 84 까지) remain touchable at 844x390.
    $ pitch_y=r13_ev_grid_pitch()
    $ thumb=60
    $ gx=R13_EV_GRID_X
    $ gy=R13_EV_ROWS_Y
    # 2026-10-27 시안 확인: 목록 칸은 높이가 고정이라 2줄 이름이 칸 밖으로 나왔다. 목록 이름만 22 를 넘기지 않는다.
    $ label_size=min(22,(r13_type("small")))
    $ actual_page=r13_record_page(entries,page)
    $ page_size=r13_record_page_size()
    $ visible=entries[actual_page*page_size:][:page_size]
    $ first,second=r13_compare_slots(pair)
    text header xpos (gx+4) ypos R13_EV_TOP xsize (R13_EV_GRID_W-4) size label_size color (r13_type_color("muted")) font R13_UI_BOLD_FONT
    for index,key in enumerate(visible):
        $ cell_w=R13_EV_GRID_W
        $ cell_h=pitch_y
        $ chosen=(key==first) if pair else (key==detail)
        $ cell_action=(([Function(r13_record_select,owner,"pair",r13_compare_fill(pair,pair_slot,key),False)]+([] if archive else [Function(r13_record_mark_seen,key)]))
            if pair else Function(r13_record_select,owner,"detail",key,not archive))
        if key in R13_DRAWER_BACK:
            # 2026-10-24 증거 서랍: 묶음 안 상세의 첫 줄은 묶음 목록으로 돌아가는 칸이다(나란히 놓기 중에도 같다).
            fixed:
                xpos gx ypos (gy+index*pitch_y) xysize (cell_w,cell_h)
                use r13_control(("‹ 지난 사건 목록" if key==R13_DRAWER_BACK[0] else "‹ 사람 목록"),None,r13_drawer_back(owner),width=cell_w,height=cell_h,label_size=label_size,control_id="r13_dr_back")
        else:
            button:
                xpos gx ypos (gy+index*pitch_y) xysize (cell_w,cell_h)
                padding (0,0)
                background r13_field_button_art(chosen)
                hover_background r13_field_button_art(chosen)
                alt r13_catalog_title(key) action cell_action
                fixed:
                    xysize (cell_w,cell_h)
                    # 2026-10-24 증거 서랍: 이름 아래 「N일 · 장소」 꼬리표와 귀퉁이 쪽지(v111 에서만. 옛 이야기는 이름만).
                    use r13_drawer_card_body(key,cell_w,cell_h,label_size,chosen,thumb,174)
                    if not archive and r13_catalog_transferable(key):
                        add r13_asset_path("file:"+(R13_NIGHT_UI+"diamond.png")) xpos 9 ypos 7
                    if pair and key in (first,second):
                        text ("①" if key==first else "②") xpos 65 xanchor 1.0 ypos 2 size r13_type("small") color "#fff0ce" outlines [(3,"#8b1f2a",0,0)] font R13_UI_BOLD_FONT
                    # 0.20.12: the unread mark sits on the picture's corner instead of taking name width.
                    if not pair and not archive and r13_drawer_unread(key):
                        text "●" xpos 65 xanchor 1.0 ypos 3 size r13_type("small") color "#f0c66a" font R13_UI_BOLD_FONT
    if r13_record_pages(entries)>1:
        $ ph=r13_ev_button_height()
        $ pw=88 if touch else 72
        fixed:
            xpos gx ypos (R13_EV_BOTTOM-ph) xysize (pw,ph)
            use r13_control("‹",None,Function(r13_record_select,owner,"page",actual_page-1,False),enabled=actual_page>0,width=pw,height=ph,control_id="r13_ev_prev")
        text ("%d / %d"%(actual_page+1,r13_record_pages(entries))) xpos (gx+R13_EV_GRID_W//2) xanchor .5 ypos (R13_EV_BOTTOM-ph//2) yanchor .5 size label_size color (r13_type_color("muted")) font R13_UI_BOLD_FONT
        fixed:
            xpos (gx+R13_EV_GRID_W-pw) ypos (R13_EV_BOTTOM-ph) xysize (pw,ph)
            use r13_control("›",None,Function(r13_record_select,owner,"page",actual_page+1,False),enabled=actual_page+1<r13_record_pages(entries),width=pw,height=ph,control_id="r13_ev_next")
    if not entries:
        text ("아직 모은 자료가 없습니다." if not r13_catalog_entries(archive) else "이 분류에 해당하는 자료가 없습니다.") xpos (gx+4) ypos (gy+20) xsize (R13_EV_GRID_W-4) size label_size color (r13_type_color("muted")) font R13_UI_BOLD_FONT
    add Solid("#c9a86a66") xpos R13_EV_DIVIDER_X ypos (R13_EV_TOP+4) xsize 1 ysize (R13_EV_TEXT_BOTTOM-R13_EV_TOP-4)

screen r13_evidence_heading(key,width,title_size):
    $ badge_size=r13_ev_small_size()
    $ badge_title=r13_evidence_kind_label(key)
    hbox:
        spacing 10
        text r13_catalog_title(key) size title_size color (r13_type_color("ink")) font R13_UI_BOLD_FONT xmaximum max(100,width-r13_ev_title_width(badge_title,badge_size)-26) yalign .5
        frame:
            yalign .5 padding (8,2) background None
            text badge_title size badge_size color (r13_type_color("accent")) font R13_UI_BOLD_FONT

screen r13_evidence_picture_box(key,box):
    frame:
        xsize box ysize box padding (12,12) background r13_field_paper()
        add r13_evidence_picture(key,box-24) align (.5,.5)

screen r13_evidence_fact_list(key,width):
    vbox:
        spacing 6
        for line in r13_evidence_facts(key):
            hbox:
                spacing 10
                add r13_asset_path("file:"+(R13_NIGHT_UI+"diamond.png")) yoffset ((r13_ev_fact_size()-8)//2+2)
                text line size r13_ev_fact_size() color (r13_type_color("ink")) font R13_UI_BOLD_FONT xsize (width-18)

# One record: big picture, facts, and on the right the hint or the folded original text.
screen r13_evidence_single(detail,owner,archive=False,view_context=("records",),can_compare=False,present=False,present_label="",present_ok=False,present_action=None,stop_action=None,ready=True,statement=None,present_note=None,empty=False,stop_label="돌아가기",present_help=None):
    default origin_open=False
    $ bh=r13_ev_button_height()
    $ touch=r13_touch_ui()
    $ small=r13_ev_reading_size()
    $ buttons=(1 if detail else 0)+(2 if present else (1 if can_compare else 0))  # 0.20.7: the source button stays (펼치기/접기)
    $ reading_bottom=R13_EV_BOTTOM-buttons*bh-max(0,buttons-1)*12-16
    $ cx=R13_EV_CENTER_X
    $ cw=R13_EV_CENTER_W-20
    $ rx=R13_EV_RIGHT_X
    $ rw=R13_EV_RIGHT_W-16
    if detail:
        if not archive and r13_drawer_unread(detail):
            timer .7 action [Function(r13_record_mark_seen,detail),Function(r13_drawer_mark_notes,detail)]
        viewport:
            id "r13_ev_single_reading"
            area (cx,R13_EV_TOP,R13_EV_CENTER_W,R13_EV_TEXT_BOTTOM-R13_EV_TOP)
            mousewheel True draggable True scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            vbox:
                xsize cw spacing 12
                use r13_evidence_heading(detail,cw,(r13_type("title")))
                $ picture=280 if touch else 360
                fixed:
                    xsize cw ysize picture
                    fixed:
                        xpos ((cw-picture)//2) xysize (picture,picture)
                        use r13_evidence_picture_box(detail,picture)
                use r13_evidence_fact_list(detail,cw)
                # 2026-10-24 증거 서랍: 접힌 쪽지(정정·결과 기록)는 원래 카드 내용 아래에 이어 읽는다.
                if not archive:
                    use r13_drawer_note_blocks(detail,cw)
    elif not empty:  # 0.20.5 (UI review): nothing to pick -> no "pick one" line; the grid says why
        text ("보여줄 자료를 왼쪽에서 직접 고르세요." if present else "자료를 선택하세요.") xpos cx ypos (R13_EV_TOP+160) xsize R13_EV_CENTER_W text_align .5 size r13_ev_fact_size() color (r13_type_color("muted")) font R13_UI_BOLD_FONT
    for scroll_key index scroll_key in [r13_record_scroll_key(view_context,detail,archive)]:
        $ detail_scroll=r13_record_scroll_adjustment(view_context,detail,archive)
        viewport:
            id "r13_material_scroll"
            yadjustment detail_scroll
            area (rx,R13_EV_TOP,R13_EV_RIGHT_W+8,max(60,reading_bottom-R13_EV_TOP)) mousewheel True draggable True scrollbars ("vertical" if (detail or present) else None)
            vscrollbar_unscrollable "hide"
            vbox:
                spacing 12
                if present:
                    if statement:
                        text (statement[0]+"의 발언") size small color (r13_type_color("accent")) font R13_UI_BOLD_FONT
                        text statement[1] size r13_ev_fact_size() color (r13_type_color("ink")) font R13_UI_BOLD_FONT xsize rw
                    else:
                        if present_note:
                            text present_note size small color (r13_type_color("accent")) font R13_UI_BOLD_FONT xsize rw
                        text (present_help or "먼저 보여주고, 건넬지는 대화 후 결정합니다.") size small color (r13_type_color("muted")) font R13_UI_BOLD_FONT xsize rw
                elif can_compare and not origin_open:
                    text "「나란히 놓기」를 누른 뒤 왼쪽에서 함께 볼 자료를 고르세요." size small color (r13_type_color("muted")) font R13_UI_BOLD_FONT xsize rw
                if detail and origin_open:
                    $ ev=r13_catalog_record(detail)
                    text ("들은 말" if ev.get("kind")=="증언" else "확인한 내용") size small color (r13_type_color("accent")) font R13_UI_BOLD_FONT
                    text r13_material_body(ev) size r13_ev_fact_size() color (r13_type_color("ink")) font R13_UI_BOLD_FONT xsize rw
                    if not archive and r13_catalog_transferable(detail):
                        text "전달 가능 · 보여준 뒤 결정" size small color (r13_type_color("accent")) font R13_UI_BOLD_FONT xsize rw
                    $ source_person=r13_material_source_person(detail) if not archive and not isinstance(owner,str) else None
                    if source_person:
                        fixed:
                            xysize (rw,bh)
                            use r13_control(R13_NAMES[source_person]+" · 관계도 ›",None,Function(r13_open_record_relation,owner,source_person),width=rw,height=bh,label_size=small,control_id="r13_ev_relation")
                    text ("지난 플레이에서 찾은 것 · 지금은 보여줄 수 없음" if archive else r13_catalog_origin(detail)) size small color (r13_type_color("muted")) font R13_UI_BOLD_FONT xsize rw
                    if not archive and detail in ROOM13["evidence"]:
                        text r13_learning_record_status(detail) size small color (r13_type_color("muted")) font R13_UI_BOLD_FONT xsize rw
                    if not archive and detail in room13.get("records",{}):
                        text ("얻은 곳: "+r13_record_source_label(detail)) size small color (r13_type_color("muted")) font R13_UI_BOLD_FONT xsize rw
    $ by=R13_EV_BOTTOM-bh
    if present:
        fixed:
            xpos rx ypos by xysize (R13_EV_RIGHT_W,bh)
            use r13_control(stop_label,None,stop_action,enabled=ready,width=R13_EV_RIGHT_W,height=bh,label_size=r13_ev_label_size(stop_label,R13_EV_RIGHT_W),control_id="r13_ev_stop")
        fixed:
            xpos rx ypos (by-bh-12) xysize (R13_EV_RIGHT_W,bh)
            use r13_control(present_label,None,present_action,enabled=present_ok,primary=True,width=R13_EV_RIGHT_W,height=bh,label_size=r13_ev_label_size(present_label,R13_EV_RIGHT_W),control_id="r13_ev_present")
        $ by=by-2*(bh+12)
    elif can_compare:
        fixed:
            xpos rx ypos by xysize (R13_EV_RIGHT_W,bh)
            use r13_control("⇆ 나란히 놓기",None,[Function(r13_record_select,owner,"pair",r13_compare_begin(detail),False),Function(r13_record_select,owner,"pair_slot",1,False)],enabled=bool(detail),primary=True,width=R13_EV_RIGHT_W,height=bh,label_size=r13_ev_label_size("⇆ 나란히 놓기",R13_EV_RIGHT_W),control_id="r13_ev_pair")
        $ by=by-bh-12
    if detail:
        # 0.20.7 (Codex design 08, owner "다 해줘"): the same button folds the source again.
        fixed:
            xpos rx ypos by xysize (R13_EV_RIGHT_W,bh)
            use r13_control(("출처 접기" if origin_open else "출처 펼치기"),None,SetLocalVariable("origin_open",not origin_open),width=R13_EV_RIGHT_W,height=bh,label_size=r13_ev_label_size("출처 펼치기",R13_EV_RIGHT_W),control_id="r13_ev_origin")

# Two records side by side, equal columns. No marks, no highlighting.
screen r13_evidence_pair(entries,pair,pair_slot,owner,archive=False):
    $ bh=r13_ev_button_height()
    $ by=R13_EV_BOTTOM-bh
    $ touch=r13_touch_ui()
    $ col_w=(R13_EV_RIGHT-R13_EV_CENTER_X-26)//2
    $ col1=R13_EV_RIGHT-col_w
    $ top=R13_EV_TOP+30
    text "나란히 놓기 · 두 자료를 함께 봅니다. 맞는지 아닌지는 표시하지 않습니다." xpos R13_EV_CENTER_X ypos (R13_EV_TOP-4) xsize (R13_EV_RIGHT-R13_EV_CENTER_X) size r13_ev_small_size() color (r13_type_color("muted")) font R13_UI_BOLD_FONT
    add Solid("#c9a86a66") xpos (R13_EV_CENTER_X+col_w+12) ypos (top+8) xsize 1 ysize (by-top-20)
    add r13_asset_path("file:"+(R13_NIGHT_UI+"diamond.png")) xpos (R13_EV_CENTER_X+col_w+8) ypos ((top+8+by-12)//2)
    $ pair_title=(r13_type("title"))
    $ pic=r13_ev_pair_picture(pair,by,pair_title,top)
    for column,key index (column,key) in enumerate(r13_compare_slots(pair)):
        viewport:
            id ("r13_ev_pair_reading_%d"%column)
            area ((R13_EV_CENTER_X if column==0 else col1),top,col_w,by-top-12)
            mousewheel True draggable True scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            vbox:
                xsize (col_w-12) spacing 10
                if key is not None:
                    use r13_evidence_heading(key,col_w-12,pair_title)
                    fixed:
                        xsize (col_w-12) ysize pic
                        fixed:
                            xpos ((col_w-12-pic)//2) xysize (pic,pic)
                            use r13_evidence_picture_box(key,pic)
                    use r13_evidence_fact_list(key,col_w-12)
                else:
                    text ("%d번 자리"%(column+1)) size pair_title color (r13_type_color("muted")) font R13_UI_BOLD_FONT
                    frame:
                        xsize pic ysize pic xoffset ((col_w-12-pic)//2) padding (24,24) background R13PaperFrame()
                        text "왼쪽에서 함께 볼 자료를 고르세요." align (.5,.5) text_align .5 size r13_ev_fact_size() color (r13_type_color("muted")) font R13_UI_BOLD_FONT
    $ single=r13_compare_single(pair)
    fixed:
        xpos R13_EV_CENTER_X ypos by xysize (198,bh)
        use r13_control("한 장만 보기",None,[Function(r13_record_select,owner,"detail",single,not archive),Function(r13_record_select,owner,"page",r13_compare_page(entries,single),False),Function(r13_record_select,owner,"pair",None,False)],width=198,height=bh,label_size=r13_ev_label_size("한 장만 보기",198),control_id="r13_ev_single")
    fixed:
        xpos (R13_EV_CENTER_X+198+16) ypos by xysize (198,bh)
        use r13_control("자리 바꾸기",None,Function(r13_record_select,owner,"pair",r13_compare_swap(pair),False),width=198,height=bh,label_size=r13_ev_label_size("자리 바꾸기",198),control_id="r13_ev_swap")
    fixed:
        xpos (R13_EV_RIGHT-206) ypos by xysize (206,bh)
        use r13_control(("⇆ %d번 바꾸기"%(2 if pair_slot else 1)),None,Function(r13_record_select,owner,"pair_slot",0 if pair_slot else 1,False),width=206,height=bh,label_size=r13_ev_label_size("⇆ 2번 바꾸기",206),control_id="r13_ev_slot")

# The whole 자료 view (records tab and the 보여주기 book).
screen r13_evidence_browser(entries,detail,page,owner,pair=None,pair_slot=1,archive=False,view_context=("records",),header="",present=False,present_label="",present_ok=False,present_action=None,stop_action=None,ready=True,statement=None,present_note=None,stop_label="돌아가기",present_help=None):
    $ live_pair=None if present else r13_compare_live(pair)
    use r13_evidence_grid(entries,detail,page,owner,live_pair,pair_slot,archive,header)
    if live_pair:
        use r13_evidence_pair(entries,live_pair,pair_slot,owner,archive)
    else:
        use r13_evidence_single(detail,owner,archive,view_context,(not present and len(entries)>1),present,present_label,present_ok,present_action,stop_action,ready,statement,present_note,empty=not entries,stop_label=stop_label,present_help=present_help) id (view_context,detail,archive,persistent.room13_large_text)
