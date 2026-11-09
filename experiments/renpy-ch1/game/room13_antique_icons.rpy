# 납품된 B 수첩 아이콘을 재사용한다. 클래스 이름은 기존 저장 호환을 위해 둔다.
init 58 python:
    R13_SUPPLIED_UI_ICONS={
        "record":("ui-b-field/b_icon_book.png",(19,16,25,32)),
        "backlog":("ui-b-field/b_icon_book.png",(19,16,25,32)),
        "testimony":("ui-b-question/icon_document.png",(14,8,36,48)),
        "evidence":("ui-b-question/icon_document.png",(14,8,36,48)),
        "present":("ui-b-question/icon_document.png",(14,8,36,48)),
        "map":("ui-b-field/b_icon_map.png",(16,20,32,23)),
        "dialogue":("ui-b-field/b_icon_more.png",(16,20,32,24)),
        "settings":("ui-b-field/b_icon_more.png",(16,20,32,24)),
        "investigate":("ui-b-options/daram_diary_sticker_magnifier.png",(0,7,404,411)),
        "skip":("ui-b-dialogue/b_icon_next.png",(18,16,27,32)),
        "check":("ui-b-question/b_icon_acorn_done.png",(20,16,24,32)),
        "lock":("map-status/locked.png",(15,7,66,81)),
    }
    # 회의 종류는 옆의 제목이 구분한다. 회의 공통 표시는 같은 대화 말풍선을 쓴다.
    for _r13_icon_meeting in ("round","stone","field","room"):
        R13_SUPPLIED_UI_ICONS["meeting_"+_r13_icon_meeting]=R13_SUPPLIED_UI_ICONS["dialogue"]

    class R13AntiqueIcon(renpy.Displayable):
        def __init__(self,kind,size=24,**kwargs):
            super(R13AntiqueIcon,self).__init__(**kwargs)
            self.kind=kind;self.size=size
        def render(self,width,height,st,at):
            spec=R13_SUPPLIED_UI_ICONS.get(self.kind)
            if not spec:
                # 전용 납품이 없는 장식은 새로 그리지 않는다. 옆의 행동 글자가 의미를 전한다.
                return renpy.Render(self.size,self.size)
            path,crop=spec
            art=Crop(crop,r13_asset_path("file:assets/"+path))
            return renpy.render(Transform(art,xysize=(self.size,self.size),fit="contain",nearest=True),self.size,self.size,st,at)
