# Composition shared by conversations, questions and the compact reference HUD.
init 100 python:
    class R13TimeDial(renpy.Displayable):
        def render(self,width,height,st,at):
            r=renpy.Render(40,40);c=r.canvas()
            c.circle('#22292b',(20,20),19)
            c.circle('#a4aa98',(20,20),17)
            c.circle('#33454b',(20,20),14)
            night=store.room13.get("period",0)>=2
            if night:
                c.circle('#e5e3c5',(24,14),6)
                c.circle('#33454b',(27,12),5)
            else:
                c.circle('#e8c27d',(20,17),7)
                c.rect('#899d91',(7,25,27,7))
            return r

