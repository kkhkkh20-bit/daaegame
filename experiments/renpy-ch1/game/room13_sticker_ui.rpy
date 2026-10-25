# One set of cut-paper borders shared by every interactive surface.
init -80 python:
    def r13_sticker_button(primary=False,focused=False,disabled=False):
        role="surface.button."+("primary" if primary else "focused" if focused else "standard")
        surface=r13_asset(role)
        return Transform(surface,alpha=.65) if disabled else surface

# A runtime silhouette outline preserves each existing portrait and authored pose.
# It changes presentation only, never the underlying character/expression choice.
init 82 python:
    class R13StickerOutline(renpy.Displayable):
        def __init__(self,child,**kwargs):
            super(R13StickerOutline,self).__init__(**kwargs)
            self.child=renpy.displayable(child)
            self.edge=Transform(self.child,matrixcolor=ColorizeMatrix("#fff5df","#fff5df"))
        def visit(self):return [self.child,self.edge]
        def render(self,width,height,st,at):
            child=renpy.render(self.child,width,height,st,at)
            edge=renpy.render(self.edge,width,height,st,at)
            w,h=child.get_size();out=renpy.Render(w,h)
            for x,y in ((-5,0),(5,0),(0,-5),(0,5),(-4,-4),(-4,4),(4,-4),(4,4)):
                out.blit(edge,(x,y))
            out.blit(child,(0,0))
            return out
