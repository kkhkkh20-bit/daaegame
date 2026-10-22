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
    # Layout from the mockup frame: buttons end at y670 inside the sheet; top tabs from x158, 90 apart.
    R13_EV_BOTTOM=670
    R13_EV_TAB_X=158
    R13_EV_TAB_PITCH=90

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
        """0.20.5 (UI review): the first tab starts after the sheet title, never under it."""
        return max(R13_EV_TAB_X,60+r13_ev_title_width(title)+24)
    def r13_ev_two_lines(text,width,size):
        """0.20.5 (UI review): a grid name in at most two lines at this width, then "…".
        Words stay whole when they fit; a word longer than a line is cut."""
        cap=max(2,int(width//max(1,size)))
        lines=[""]
        for word in str(text).split(" "):
            while word:
                room=cap-len(lines[-1])-(1 if lines[-1] else 0)
                if len(word)<=room:
                    lines[-1]=(lines[-1]+" "+word) if lines[-1] else word;word=""
                elif lines[-1] and len(word)<=cap:
                    lines.append("")
                else:
                    cut=max(1,room);lines[-1]=(lines[-1]+(" " if lines[-1] else "")+word[:cut]);word=word[cut:]
                    if word:lines.append("")
        if len(lines)>2:
            lines=lines[:2];lines[1]=lines[1][:max(1,cap-1)].rstrip()+"…"
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
    def r13_ev_pair_picture(pair,bottom,title_size,top=142):
        """0.20.6 (Codex R04): the side-by-side picture shrinks so both titles and all fact lines
        end above the buttons (never under 180px, never over the approved 312px)."""
        fact=r13_ev_fact_size();need=0
        for key in r13_compare_slots(pair):
            if key is None:continue
            head=r13_ev_text_lines(r13_catalog_title(key),330,title_size)*(title_size+8)
            facts=sum(r13_ev_text_lines(line,402,fact)*(fact+6)+6 for line in r13_evidence_facts(key))
            need=max(need,head+facts+30)
        return max(180,min(312,bottom-12-top-need))
    def r13_ev_button_height():
        return 56 if r13_touch_ui() or persistent.room13_large_text else 48

    def r13_ev_small_size():
        # Touch: small text is never under 18px.
        return r13_read_size(18,21) if r13_touch_ui() else r13_read_size(15,18)  # 0.20.5 (Codex A04): large text on phones too

    def r13_ev_fact_size():
        return r13_read_size(20,24) if r13_touch_ui() else r13_read_size(19,23)

    def r13_ev_label_size(label,width):
        # A long name in a fixed-width control shrinks instead of spilling out (never under the small size).
        normal=r13_read_size(R13_CONTROL["text"],R13_CONTROL["large_text"])
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
        font r13_ui_font() size 24 color "#e3d6bd" hover_color "#fff6e2" selected_color "#fff6e2" xalign .5 yalign .5
    style r13ev_chip_button is button:
        background R13ControlSurface() hover_background R13ControlSurface(hovered=True)
        selected_background R13ControlSurface(chosen=True) selected_hover_background R13ControlSurface(chosen=True,hovered=True)
        padding (6,2)
    style r13ev_chip_button_text is text:
        font r13_ui_font() color "#efe3cc" hover_color "#fff6e2" selected_color "#fff6e2" xalign .5 yalign .5 text_align .5

# Brown sheet with the title, top tabs, close X and the gold rule (settings-window pieces).
screen r13_ink_record_shell(title,tabs,current="all",close_action=None,note=None):
    $ touch=r13_touch_ui()
    $ tab_h=56 if touch else 48
    add Solid("#05070fa6")
    add Frame(R13_NIGHT_UI+"panel.png",48,48) xpos 12 ypos 12 xysize (1256,696)
    $ tab_x=r13_ev_tab_x(title)
    text title xpos 60 ypos 40 size 34 color "#f6ecd8" font r13_ui_font()
    for index,(tab_key,tab_title,tab_action) in enumerate(tabs):
        fixed:
            xpos (tab_x+index*R13_EV_TAB_PITCH) ypos (66-tab_h//2) xysize (86,tab_h)
            if tab_key==current:
                add Transform(R13_NIGHT_UI+"opt_tab.png",xysize=(86,44)) align (.5,.5)
            textbutton tab_title:
                style "r13ev_tab_button" text_style "r13ev_tab_button_text" xysize (86,tab_h)
                selected tab_key==current action tab_action alt tab_title
    if note:
        text note xpos (tab_x+len(tabs)*R13_EV_TAB_PITCH+12) ypos 52 size r13_ev_small_size() color "#d9b46c" font r13_ui_font()
    button:
        id "r13_ev_close"
        xpos (1170 if touch else 1176) ypos (30 if touch else 34) xysize ((64,64) if touch else (52,52))
        background None hover_background Solid("#fff6e214")
        action close_action alt "닫기"
        add R13_NIGHT_UI+"close_x.png" align (.5,.5)
    add R13_NIGHT_UI+"diamond.png" xpos 56 ypos 99
    add Solid("#c9a86a99") xpos 66 ypos 103 xsize 1156 ysize 1

screen r13_ink_chips(chips):
    $ touch=r13_touch_ui()
    $ boxes=r13_ev_chip_boxes(chips)
    for index,(chip_label,chip_chosen,chip_action) in enumerate(chips):
        textbutton chip_label:
            style "r13ev_chip_button" text_style "r13ev_chip_button_text"
            xpos boxes[index][0] ypos (38 if touch else 46) xsize boxes[index][1] ysize (56 if touch else 40)
            text_size r13_ev_small_size() selected chip_chosen action chip_action

# Left column: small pictures, page by page. While comparing, a tap fills the chosen slot.
screen r13_evidence_grid(entries,detail,page,owner,pair=None,pair_slot=1,archive=False,header=""):
    $ touch=r13_touch_ui()
    $ wide=touch or bool(persistent.room13_large_text)
    $ cols=2 if wide else 3
    $ pitch_x=124 if wide else 84
    $ pitch_y=114 if wide else 118
    $ thumb=64 if wide else 74
    $ label_size=(18 if r13_touch_ui() else r13_read_size(15,18))  # 0.20.5: grid names keep their fitted size; the big text goes to the picture side
    $ label_chars=12 if wide else 10
    $ actual_page=r13_record_page(entries,page)
    $ page_size=r13_record_page_size()
    $ visible=entries[actual_page*page_size:][:page_size]
    $ first,second=r13_compare_slots(pair)
    text header xpos 64 ypos 118 size label_size color "#d9c9a8" font r13_ui_font()
    for index,key in enumerate(visible):
        $ cell_w=pitch_x-6
        $ cell_h=pitch_y-6
        $ chosen=(key==first) if pair else (key==detail)
        $ cell_action=(([Function(r13_record_select,owner,"pair",r13_compare_fill(pair,pair_slot,key),False)]+([] if archive else [Function(r13_record_mark_seen,key)]))
            if pair else Function(r13_record_select,owner,"detail",key,not archive))
        button:
            xpos (60+(index%cols)*pitch_x) ypos (148+(index//cols)*pitch_y) xysize (cell_w,cell_h)
            padding (0,0)
            background r13_ev_thumb_bg(cell_w,cell_h,thumb,chosen)
            hover_background r13_ev_thumb_bg(cell_w,cell_h,thumb,chosen,True)
            alt r13_catalog_title(key) action cell_action
            fixed:
                xysize (cell_w,cell_h)
                add Transform(r13_record_icon(key),xysize=(thumb-18,thumb-18),fit="contain",nearest=True) xpos (cell_w//2) xanchor .5 ypos (thumb//2) yanchor .5
                if not archive and r13_catalog_transferable(key):
                    add R13_NIGHT_UI+"diamond.png" xpos ((cell_w-thumb)//2+7) ypos 7
                if pair and key in (first,second):
                    text ("①" if key==first else "②") xpos ((cell_w+thumb)//2+4) xanchor 1.0 ypos -8 size 22 color "#fff0ce" outlines [(3,"#8b1f2a",0,0)] font r13_ui_font()
                text r13_ev_two_lines(("● " if not archive and r13_record_unread(key) else "")+r13_evidence_short(key,label_chars*2),cell_w-4,label_size):
                    xpos 0 ypos (thumb+4) xsize cell_w text_align .5 size label_size color "#e3d6bd" font r13_ui_font() line_spacing 0
    if r13_record_pages(entries)>1:
        $ ph=r13_ev_button_height()
        fixed:
            xpos 60 ypos (R13_EV_BOTTOM-ph) xysize (72,ph)
            use r13_control("‹",None,Function(r13_record_select,owner,"page",actual_page-1,False),enabled=actual_page>0,width=72,height=ph,control_id="r13_ev_prev")
        text ("%d / %d"%(actual_page+1,r13_record_pages(entries))) xpos 188 xanchor .5 ypos (R13_EV_BOTTOM-ph//2) yanchor .5 size label_size color "#d9c9a8" font r13_ui_font()
        fixed:
            xpos 244 ypos (R13_EV_BOTTOM-ph) xysize (72,ph)
            use r13_control("›",None,Function(r13_record_select,owner,"page",actual_page+1,False),enabled=actual_page+1<r13_record_pages(entries),width=72,height=ph,control_id="r13_ev_next")
    if not entries:
        text ("아직 모은 자료가 없습니다." if not r13_catalog_entries(archive) else "이 분류에 해당하는 자료가 없습니다.") xpos 64 ypos 160 xsize 252 size label_size color "#b8b0a2" font r13_ui_font()
    add Solid("#c9a86a66") xpos 330 ypos 116 xsize 1 ysize 564

screen r13_evidence_heading(key,width,title_size):
    hbox:
        spacing 10
        text r13_catalog_title(key) size title_size color "#f6ecd8" font r13_ui_font() xmaximum (width-90) yalign .5
        frame:
            yalign .5 padding (8,2) background Frame(R13_NIGHT_UI+"preview_box.png",8,8)
            text r13_evidence_kind_label(key) size r13_ev_small_size() color "#d9b46c" font r13_ui_font()

screen r13_evidence_picture_box(key,box):
    frame:
        xsize box ysize box padding (12,12) background Frame(R13_NIGHT_UI+"preview_box.png",8,8)
        add r13_evidence_picture(key,box-24) align (.5,.5)

screen r13_evidence_fact_list(key,width):
    vbox:
        spacing 6
        for line in r13_evidence_facts(key):
            hbox:
                spacing 10
                add R13_NIGHT_UI+"diamond.png" yoffset ((r13_ev_fact_size()-8)//2+2)
                text line size r13_ev_fact_size() color "#efe3cc" font r13_ui_font() xsize (width-18)

# One record: big picture, facts, and on the right the hint or the folded original text.
screen r13_evidence_single(detail,owner,archive=False,view_context=("records",),can_compare=False,present=False,present_label="",present_ok=False,present_action=None,stop_action=None,ready=True,statement=None,present_note=None,empty=False):
    default origin_open=False
    $ bh=r13_ev_button_height()
    $ touch=r13_touch_ui()
    $ small=r13_ev_small_size()
    $ buttons=(0 if origin_open or not detail else 1)+(2 if present else (1 if can_compare else 0))
    $ reading_bottom=R13_EV_BOTTOM-buttons*bh-max(0,buttons-1)*12-16
    if detail:
        if not archive and r13_record_unread(detail):
            timer .7 action Function(r13_record_mark_seen,detail)
        vbox:
            xpos 372 ypos 116 xsize 520 spacing 12
            use r13_evidence_heading(detail,520,(r13_read_size(28,32) if touch else r13_read_size(26,30)))
            fixed:
                xsize 520 ysize 360
                fixed:
                    xpos 80 xysize (360,360)
                    use r13_evidence_picture_box(detail,360)
            use r13_evidence_fact_list(detail,500)
    elif not empty:  # 0.20.5 (UI review): nothing to pick -> no "pick one" line; the grid says why
        text ("보여줄 자료를 왼쪽에서 직접 고르세요." if present else "자료를 선택하세요.") xpos 372 ypos 300 xsize 520 text_align .5 size r13_ev_fact_size() color "#b8b0a2" font r13_ui_font()
    for scroll_key index scroll_key in [r13_record_scroll_key(view_context,detail,archive)]:
        $ detail_scroll=r13_record_scroll_adjustment(view_context,detail,archive)
        viewport:
            id "r13_material_scroll"
            yadjustment detail_scroll
            area (916,116,304,max(60,reading_bottom-116)) mousewheel True draggable True scrollbars ("vertical" if (detail or present) else None)
            vbox:
                spacing 12
                if present:
                    if statement:
                        text (statement[0]+"의 발언") size small color "#d9b46c" font r13_ui_font()
                        text statement[1] size r13_ev_fact_size() color "#efe3cc" font r13_ui_font() xsize 280
                    else:
                        if present_note:
                            text present_note size small color "#d9b46c" font r13_ui_font() xsize 280
                        text "먼저 보여주고, 건넬지는 대화 후 결정합니다." size small color "#b8b0a2" font r13_ui_font() xsize 280
                elif can_compare and not origin_open:
                    text "이 자료와 함께 볼 자료가 있으면\n아래 「나란히 놓기」를 누르고\n왼쪽에서 하나 고릅니다." size small color "#b8b0a2" font r13_ui_font() xsize 280
                if detail and origin_open:
                    $ ev=r13_catalog_record(detail)
                    text ("들은 말" if ev.get("kind")=="증언" else "확인한 내용") size small color "#d9b46c" font r13_ui_font()
                    text r13_material_body(ev) size r13_ev_fact_size() color "#efe3cc" font r13_ui_font() xsize 280
                    if not archive and r13_catalog_transferable(detail):
                        text "전달 가능 · 보여준 뒤 결정" size small color "#d9b46c" font r13_ui_font() xsize 280
                    $ source_person=r13_material_source_person(detail) if not archive and not isinstance(owner,str) else None
                    if source_person:
                        fixed:
                            xysize (280,bh)
                            use r13_control(R13_NAMES[source_person]+" · 관계도 ›",None,Function(r13_open_record_relation,owner,source_person),width=280,height=bh,label_size=small,control_id="r13_ev_relation")
                    text ("지난 플레이에서 찾은 것 · 지금은 보여줄 수 없음" if archive else r13_catalog_origin(detail)) size small color "#b8b0a2" font r13_ui_font() xsize 280
                    if not archive and detail in ROOM13["evidence"]:
                        text r13_learning_record_status(detail) size small color "#b8b0a2" font r13_ui_font() xsize 280
                    if not archive and detail in room13.get("records",{}):
                        text ("얻은 곳: "+room13["records"][detail]["source"]) size small color "#b8b0a2" font r13_ui_font() xsize 280
    $ by=R13_EV_BOTTOM-bh
    if present:
        fixed:
            xpos 920 ypos by xysize (296,bh)
            use r13_control(("그만두기"),None,stop_action,enabled=ready,width=296,height=bh,control_id="r13_ev_stop")
        fixed:
            xpos 920 ypos (by-bh-12) xysize (296,bh)
            use r13_control(present_label,None,present_action,enabled=present_ok,primary=True,width=296,height=bh,label_size=r13_ev_label_size(present_label,296),control_id="r13_ev_present")
        $ by=by-2*(bh+12)
    elif can_compare:
        fixed:
            xpos 920 ypos by xysize (296,bh)
            use r13_control("⇆ 나란히 놓기",None,[Function(r13_record_select,owner,"pair",r13_compare_begin(detail),False),Function(r13_record_select,owner,"pair_slot",1,False)],enabled=bool(detail),primary=True,width=296,height=bh,control_id="r13_ev_pair")
        $ by=by-bh-12
    if detail and not origin_open:
        fixed:
            xpos 920 ypos by xysize (296,bh)
            use r13_control("출처 펼치기",None,SetLocalVariable("origin_open",True),width=296,height=bh,control_id="r13_ev_origin")

# Two records side by side, equal columns. No marks, no highlighting.
screen r13_evidence_pair(entries,pair,pair_slot,owner,archive=False):
    $ bh=r13_ev_button_height()
    $ by=R13_EV_BOTTOM-bh
    $ touch=r13_touch_ui()
    text "나란히 놓기 · 두 자료를 함께 봅니다. 맞는지 아닌지는 표시하지 않습니다." xpos 350 ypos 112 size r13_ev_small_size() color "#d9c9a8" font r13_ui_font()
    add Solid("#c9a86a66") xpos 782 ypos 150 xsize 1 ysize (by-162)
    add R13_NIGHT_UI+"diamond.png" xpos 778 ypos ((150+by-12)//2)
    $ pair_title=(r13_read_size(24,28) if touch else r13_read_size(24,27))
    $ pic=r13_ev_pair_picture(pair,by,pair_title)
    for column,key in enumerate(r13_compare_slots(pair)):
        vbox:
            xpos (350 if column==0 else 798) ypos 142 xsize 420 spacing 10
            if key is not None:
                use r13_evidence_heading(key,420,pair_title)
                fixed:
                    xsize 420 ysize pic
                    fixed:
                        xpos ((420-pic)//2) xysize (pic,pic)
                        use r13_evidence_picture_box(key,pic)
                use r13_evidence_fact_list(key,420)
            else:
                text ("%d번 자리"%(column+1)) size (24 if touch else r13_read_size(24,27)) color "#b8b0a2" font r13_ui_font()
                frame:
                    xsize pic ysize pic xoffset ((420-pic)//2) padding (24,24) background Frame(R13_NIGHT_UI+"preview_box.png",8,8)
                    text "왼쪽에서 함께 볼 자료를 고르세요." align (.5,.5) text_align .5 size r13_ev_fact_size() color "#b8b0a2" font r13_ui_font()
    $ single=r13_compare_single(pair)
    fixed:
        xpos 350 ypos by xysize (198,bh)
        use r13_control("한 장만 보기",None,[Function(r13_record_select,owner,"detail",single,not archive),Function(r13_record_select,owner,"page",r13_compare_page(entries,single),False),Function(r13_record_select,owner,"pair",None,False)],width=198,height=bh,control_id="r13_ev_single")
    fixed:
        xpos 566 ypos by xysize (198,bh)
        use r13_control("자리 바꾸기",None,Function(r13_record_select,owner,"pair",r13_compare_swap(pair),False),width=198,height=bh,control_id="r13_ev_swap")
    fixed:
        xpos 1012 ypos by xysize (206,bh)
        use r13_control(("⇆ %d번 바꾸기"%(2 if pair_slot else 1)),None,Function(r13_record_select,owner,"pair_slot",0 if pair_slot else 1,False),width=206,height=bh,control_id="r13_ev_slot")

# The whole 자료 view (records tab and the 보여주기 book).
screen r13_evidence_browser(entries,detail,page,owner,pair=None,pair_slot=1,archive=False,view_context=("records",),header="",present=False,present_label="",present_ok=False,present_action=None,stop_action=None,ready=True,statement=None,present_note=None):
    $ live_pair=None if present else r13_compare_live(pair)
    use r13_evidence_grid(entries,detail,page,owner,live_pair,pair_slot,archive,header)
    if live_pair:
        use r13_evidence_pair(entries,live_pair,pair_slot,owner,archive)
    else:
        use r13_evidence_single(detail,owner,archive,view_context,(not present and len(entries)>1),present,present_label,present_ok,present_action,stop_action,ready,statement,present_note,empty=not entries) id (view_context,detail,archive,persistent.room13_large_text)
