# 동일한 상태 캔버스를 함께 잘라 투명 여백만 제외한다. 모든 상태의 배율·클릭 영역은 같다.
init 67 python:
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
            if self.asset_revision==r13_asset_revision():return
            role="button."+self.family
            spec=r13_asset_spec(role)
            self.crop=spec.get("render",{}).get("crop",[0,0]+spec["size"])
            natural=spec.get("render",{}).get("zoom",1.0)
            self.scale=min(float(self.width)/(self.crop[2]*natural),float(self.height)/(self.crop[3]*natural))
            self.skins={state:Transform(r13_asset(role,state),zoom=self.scale) for state in ("basic","pressed","selected","disabled")}
            self.asset_revision=r13_asset_revision()

        def visit(self):
            self.update_skins()
            return list(self.skins.values())+([self.icon] if self.icon else [])

        def render(self,width,height,st,at):
            self.update_skins()
            w,h=self.width,self.height
            state="disabled" if not self.enabled else "pressed" if self.pressed else "selected" if self.selected else "basic"
            out=renpy.Render(w,h)
            paper=renpy.render(self.skins[state],w,h,st,at)
            pw,ph=paper.get_size();out.blit(paper,((w-pw)//2,(h-ph)//2))
            render_spec=r13_asset_spec("button."+self.family,state).get("render",{})
            color=render_spec.get("text_color", "#8b8175" if not self.enabled else "#fff5e5" if self.family=="primary" else "#493324")
            text=Text(self.caption,font=R13_UI_BOLD_FONT,size=self.text_size,color=color)
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
