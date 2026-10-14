# Title decoration uses broad quiet shapes: no grain, speckles, or raster textures.
init 60 python:
    class R13TitleVeil(renpy.Displayable):
        def render(self,width,height,st,at):
            w=max(1,int(width)); h=max(1,int(height))
            out=renpy.Render(w,h); c=out.canvas()
            # Soft falloff keeps the lamp-lit inn visible behind the masthead.
            for x in range(min(w,850)):
                u=max(0.0,1.0-x/850.0)
                alpha=int(232*u*u)
                c.rect((9,24,31,alpha),(x,0,1,h))
            return out

    class R13RoomTag(renpy.Displayable):
        def render(self,width,height,st,at):
            out=renpy.Render(64,90); c=out.canvas()
            c.line('#dab57a',(32,0),(31,14),2)
            points=[(17,14),(47,15),(60,30),(59,83),(7,84),(5,30)]
            c.polygon('#172c32',points)
            c.lines('#d4b176',True,points,2)
            c.circle('#d4b176',(32,24),3,1)
            c.line('#947954',(17,73),(48,74),1)
            return out

    class R13TitleLink(renpy.Displayable):
        def __init__(self,focused=False,**kwargs):
            super(R13TitleLink,self).__init__(**kwargs)
            self.focused=focused
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            out=renpy.Render(w,h);c=out.canvas()
            if self.focused:
                c.rect('#122a3290',(0,0,w,h))
                c.line('#e6c38a',(17,h-5),(min(w-20,179),h-5),2)
                c.polygon('#e6c38a',[(2,h//2-4),(7,h//2),(2,h//2+4)])
            return out

init 63:
    style r13_title_button is r13_button:
        background R13TitleLink()
        hover_background R13TitleLink(True)
        padding (18,8)
    style r13_title_button_text is r13_button_text:
        font 'assets/Room13Title.ttf'
        color '#f3ecdf'
        hover_color '#ffe0a1'
        insensitive_color '#849592'
        size 31
        outlines [(1,'#0b1823b0',0,1)]

init 81:
    style r13_title_primary is r13_title_button:
        xsize 324
        ysize 66
        padding (22,12)
        background Solid("#e5cea7")
        hover_background Solid("#f7e3bb")
        insensitive_background Solid("#243a3d")
    style r13_title_primary_text is r13_title_button_text:
        color "#183536"
        hover_color "#142728"
        insensitive_color "#a9bfbe"
        size 29
        outlines []
    style r13_title_aux is r13_title_button:
        padding (8,10)
    style r13_title_aux_text is r13_title_button_text:
        size 18
        color "#d2d6c7"
