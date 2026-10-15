# UI-only meeting seating plan. Uses existing portrait icons, not invented seated sprites.
default r13_meeting_scrolls = {}

init 99 python:
    class R13MeetingTable(renpy.Displayable):
        def render(self,width,height,st,at):
            result=renpy.Render(824,240);c=result.canvas()
            c.rect("#172e31",(0,0,824,240))
            c.polygon("#403328",[(52,84),(118,61),(706,61),(772,84),(772,158),(706,183),(118,183),(52,158)])
            c.polygon("#795d40",[(58,80),(122,56),(702,56),(766,80),(766,151),(702,175),(122,175),(58,151)])
            c.lines("#c6a16c",True,[(58,80),(122,56),(702,56),(766,80),(766,151),(702,175),(122,175),(58,151)],3)
            c.line("#87694a",(90,115),(734,115),2)
            return result

    def r13_meeting_seat_position(index,count):
        columns=(count+1)//2
        column=index%columns
        return (int((column+.5)*824/columns)-84,0 if index<columns else 148)

    class R13MeetingScrollChanged:
        def __init__(self,claim):self.claim=claim
        def __call__(self,value):
            value=max(0,int(value))
            offsets=dict(getattr(store,"r13_meeting_scrolls",{}))
            if offsets.get(self.claim)!=value:
                offsets[self.claim]=value;store.r13_meeting_scrolls=offsets
                renpy.retain_after_load()

    def r13_meeting_adjustment(claim):
        return ui.adjustment(value=getattr(store,"r13_meeting_scrolls",{}).get(claim,0),changed=R13MeetingScrollChanged(claim))

screen r13_meeting_seating(claim,session,speaker,ready):
    fixed:
        xsize 824 ysize 240
        add R13MeetingTable()
        text ("▸ "+R13_NAMES.get(speaker,speaker)+"의 발언") xalign .5 ypos 103 size r13_read_size(21,24) color "#ffe3a0"
        text "자리 색은 참석자 반응 · 결정은 확인한 근거로" xalign .5 ypos 130 size r13_read_size(14,16) color "#d4dfd8"
        $ seats=r13_debate_seats(session)
        for index,(who,stance) in enumerate(seats):
            $ sx,sy=r13_meeting_seat_position(index,len(seats))
            $ own_statements=[st for st in r13_debate_statements(claim) if st["who"]==who and r13_debate_visible(claim,st)]
            button:
                area (sx,sy,168,92) padding (4,3)
                background Solid("#d9b765" if who==speaker else "#344b49")
                hover_background Solid("#8e7950")
                action (Return(("select",own_statements[0]["id"])) if own_statements else NullAction()) sensitive ready
                tooltip (R13_NAMES.get(who,who)+" · "+R13_DEBATE_STANCE[session][stance])
                fixed:
                    xsize 160 ysize 86
                    add Solid("#243b3b",xsize=160,ysize=86)
                    if who in CAST:
                        add Transform(r13_art(who,"avatar_neutral"),xysize=(66,62),fit="contain",nearest=True) xalign .5 ypos 0
                    add Solid(("#a55c47","#9aab9e","#70b39a")[stance],xsize=9,ysize=9) xpos 143 ypos 6
                    text (("▸ " if who==speaker else "")+R13_NAMES.get(who,who)):
                        xalign .5 ypos 61 xsize 158 text_align .5 size r13_read_size(18,20)
                        color ("#ffe3a0" if who==speaker else "#e8e8d9") bold (who==speaker)
