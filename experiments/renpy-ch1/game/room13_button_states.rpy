# 동일한 상태 캔버스를 함께 잘라 투명 여백만 제외한다. 모든 상태의 배율·클릭 영역은 같다.
init 67 python:
    R13_SOFT_FLAT_BUTTONS = True  # 2026-10-27 소유자 "추천안대로 해"로 켬
    import pygame as r13_button_pygame

    class R13ButtonStateVisual(renpy.Displayable):
        def __init__(self, caption, family, width, height, selected=False, enabled=True, icon=None, text_size=22, **kwargs):
            super(R13ButtonStateVisual,self).__init__(**kwargs)
            self.caption,self.family=caption,family
            self.width,self.height=int(width),int(height)
            self.selected,self.enabled=selected,enabled
            self.icon,self.text_size=icon,text_size
            self.pressed=False
            self.asset_revision=-1
            self.skins={}
            self.update_skins()

        def update_skins(self):
            if self.asset_revision==(r13_asset_revision(),getattr(store,"R13_SOFT_FLAT_BUTTONS",False)):return
            role="button."+self.family
            self.flat_scope=self.family.startswith(("question_flat_","map_flat_"))
            layout_family=("topic_" if self.family.startswith("question_flat_") else "")+self.family.rsplit("_",1)[-1] if self.flat_scope else self.family
            self.layout_role="button."+layout_family
            spec=r13_asset_spec(self.layout_role)
            self.crop=spec.get("render",{}).get("crop",[0,0]+spec["size"])
            natural=spec.get("render",{}).get("zoom",1.0)
            self.scale=min(float(self.width)/(self.crop[2]*natural),float(self.height)/(self.crop[3]*natural))
            self.skins={state:Transform(r13_asset(role,state),zoom=self.scale) for state in ("basic","pressed","selected","disabled")}
            self.paper_size=(max(1,int(round(self.crop[2]*natural*self.scale))),max(1,int(round(self.crop[3]*natural*self.scale))))
            primary=self.family in ("primary","main_primary","topic_primary")
            self.shared_skins={state:Transform(r13_sticker_button(primary=primary,focused=self.selected or state=="pressed",disabled=state=="disabled"),xysize=self.paper_size) for state in ("basic","pressed","selected","disabled")}
            if self.flat_scope:
                # 원본 전체를 균일 확대한다. 기존 종이 폭/높이 안에 알파 경계만 맞춘다.
                flat_scale=min(self.paper_size[0]/128.0,self.paper_size[1]/32.0)
                # 2026-10-26 소유자: 하단 「자료 제시·기록·더보기·돌아가기」가 눈이 아프다. 시안: 남색 굵은 테두리를
                # 갈색 계열로 낮추고(세피아), 빨간 주 버튼은 채도를 조금 낮춘다. R13_SOFT_FLAT_BUTTONS 가 켜질 때만.
                soft=getattr(store,"R13_SOFT_FLAT_BUTTONS",False)
                if soft and not self.family.endswith("primary"):
                    self.shared_skins={state:Transform(R13SoftButtonSurface(hovered=state=="pressed",chosen=state=="selected",disabled=state=="disabled"),xysize=self.paper_size) for state in ("basic","pressed","selected","disabled")}
                else:
                    tone=SaturationMatrix(.85) if soft else None
                    self.shared_skins={state:Transform(r13_asset(role,state),zoom=flat_scale,matrixcolor=tone) for state in ("basic","pressed","selected","disabled")}
            self.asset_revision=(r13_asset_revision(),getattr(store,"R13_SOFT_FLAT_BUTTONS",False))

        def visit(self):
            self.update_skins()
            return list(self.shared_skins.values())+([self.icon] if self.icon else [])

        def render(self,width,height,st,at):
            self.update_skins()
            w,h=self.width,self.height
            state="disabled" if not self.enabled else "pressed" if self.pressed else "selected" if self.selected else "basic"
            out=renpy.Render(w,h)
            pw,ph=self.paper_size
            paper=renpy.render(self.shared_skins[state],pw,ph,st,at)
            draw_w,draw_h=paper.get_size()
            out.blit(paper,((w-draw_w)//2,(h-draw_h)//2))
            render_spec=r13_asset_spec("button."+self.family,state).get("render",{})
            if self.flat_scope:
                render_spec=dict(r13_asset_spec(self.layout_role,state).get("render",{}))
                render_spec["text_color"]="#8b8175" if not self.enabled else "#fff5e5" if self.family.endswith("primary") else ("#4b3420" if getattr(store,"R13_SOFT_FLAT_BUTTONS",False) else "#263953")
            color=render_spec.get("text_color", "#8b8175" if not self.enabled else "#fff5e5" if self.family=="primary" else "#493324")
            text=Text(self.caption,font=R13_UI_TYPE["button"]["font"],size=self.text_size,color=color)
            tr=renpy.render(text,w,h,st,at);tw,th=tr.get_size()
            ir=renpy.render(self.icon,32,32,st,at) if self.icon else None
            iw,ih=ir.get_size() if ir else (0,0)
            gap=render_spec.get("icon_gap",8) if ir and self.caption else 0
            contentw=tw+iw+gap
            # 글자와 아이콘도 함께 균일 축소해 같은 비율의 종이 안에 유지한다.
            safe=render_spec.get("safe_size")
            safe_w,safe_h=(safe[0]*self.scale,safe[1]*self.scale) if safe else (pw-16,ph-6)
            fit=min(1.0,max(1,safe_w)/max(1,contentw),max(1,safe_h)/max(1,th,ih))
            children=[]
            if self.icon:children.append(Transform(self.icon,yalign=.5))
            if self.caption:children.append(Transform(text,yalign=.5))
            row=renpy.display.layout.MultiBox(layout="horizontal",spacing=gap)
            for child in children:row.add(child)
            content=renpy.render(Transform(row,zoom=fit),w,h,st,at)
            dy=int(round(2*self.scale)) if state=="pressed" else 0
            cw,ch=content.get_size();out.blit(content,((w-cw)//2,(h-ch)//2+dy))
            return out

        def event(self,ev,x,y,st):
            # 그림만 갱신하고 기존 Button의 클릭·드래그 판정과 액션은 그대로 사용한다.
            pressed=self.pressed
            if ev.type==r13_button_pygame.MOUSEBUTTONDOWN and getattr(ev,"button",0)==1:
                pressed=self.enabled and 0<=x<self.width and 0<=y<self.height
            elif ev.type==r13_button_pygame.MOUSEBUTTONUP or (ev.type==r13_button_pygame.MOUSEMOTION and not (0<=x<self.width and 0<=y<self.height)):
                pressed=False
            if pressed!=self.pressed:
                self.pressed=pressed;renpy.redraw(self,0)
            return None

screen r13_state_button(caption,command,width,height,family="standard",chosen=False,enabled=True,icon=None,text_size=22,control_id=None,first=False,hover_action=None):
    button:
        id (control_id or ("r13_state_"+caption))
        xysize (width,height) padding (0,0)
        background None hover_background None insensitive_background None
        activate_sound ("<volume 0.65>"+r13_asset_path("file:assets/diary-sounds/paper-selection.mp3"))
        action command sensitive enabled selected chosen default_focus first
        hovered hover_action
        alt caption
        add R13ButtonStateVisual(caption,family,width,height,chosen,enabled,icon,text_size) id ((control_id or ("r13_state_"+caption))+"_visual")
