# Original compact pixel pictograms, drawn with the UI palette; no bitmap downloads.
init 58 python:
    class R13AntiqueIcon(renpy.Displayable):
        def __init__(self,kind,size=24,**kwargs):
            super(R13AntiqueIcon,self).__init__(**kwargs)
            self.kind=kind;self.size=size
        def render(self,width,height,st,at):
            r=renpy.Render(self.size,self.size);c=r.canvas();z=self.size/32.0
            ink='#392b25';gold='#b88b49';light='#efd49b';paper='#eedbb1';shade='#bda077';leather='#87503b'
            def poly(col,points):c.polygon(col,[(int(x*z),int(y*z)) for x,y in points])
            def box(col,x,y,w,h):c.rect(col,(int(x*z),int(y*z),max(1,int(w*z)),max(1,int(h*z))))
            def line(col,a,b,n=1):c.line(col,(int(a[0]*z),int(a[1]*z)),(int(b[0]*z),int(b[1]*z)),max(1,int(n*z)))
            k=self.kind
            if k=='check':
                box(ink,2,2,28,28);box(shade,4,4,24,24);box(paper,5,5,22,22)
                line('#657451',(8,16),(14,22),3);line('#657451',(14,22),(25,9),3)
            elif k=='investigate':
                poly(ink,[(18,16),(29,26),(25,30),(15,19)])
                poly(leather,[(19,19),(27,26),(25,28),(18,21)])
                ring=[(8,2),(17,2),(23,8),(23,16),(17,22),(8,22),(2,16),(2,8)]
                poly(ink,ring);poly(gold,[(8,4),(16,4),(21,9),(21,15),(16,20),(9,20),(4,15),(4,9)])
                poly('#637d7c',[(9,7),(15,7),(18,10),(18,14),(15,17),(10,17),(7,14),(7,10)])
                line('#d5e1cf',(9,9),(14,9),2);line(light,(5,8),(8,5),2)
            elif k=='record':
                poly(ink,[(6,2),(25,2),(28,5),(28,28),(8,31),(4,27),(4,5)])
                box(shade,8,4,17,25);box(paper,10,7,15,20)
                poly(leather,[(5,4),(22,4),(22,28),(6,28)])
                box('#a56643',7,5,3,21);box(gold,17,13,10,6);box(light,19,14,4,2)
                box('#ae4f3e',13,27,4,4);line('#bf8756',(11,7),(19,7))
            elif k in ('present','evidence'):
                poly(ink,[(2,7),(28,7),(30,9),(30,25),(2,25)])
                box(shade,4,10,24,13);box(paper,4,8,24,13)
                line('#a58660',(4,10),(16,18),2);line('#a58660',(28,10),(16,18),2)
                box('#783b32',13,15,7,6);box('#b65841',14,15,5,4);box('#da8a5a',15,15,2,1)
                if k=='present':
                    poly(ink,[(12,25),(19,23),(24,24),(22,29),(10,31),(5,28),(5,25)])
                    poly('#cea779',[(8,26),(13,27),(19,25),(21,25),(20,27),(11,29)])
            elif k=='map':
                poly(ink,[(1,7),(10,3),(20,7),(30,3),(30,26),(21,30),(11,26),(1,30)])
                poly(paper,[(3,8),(10,5),(19,9),(28,6),(28,25),(21,28),(11,24),(3,27)])
                poly(shade,[(11,6),(19,9),(20,26),(12,24)])
                line('#749080',(5,12),(9,17),2);line('#749080',(9,17),(17,14),2);line('#749080',(17,14),(25,21),2)
                line('#994d38',(22,11),(26,15),2);line('#994d38',(26,11),(22,15),2)
            elif k=='dialogue':
                poly(ink,[(1,3),(24,3),(24,19),(14,19),(8,25),(8,19),(1,19)])
                box(paper,3,5,19,12);line(shade,(6,9),(18,9),2)
                poly(ink,[(15,14),(31,14),(31,27),(28,27),(28,31),(23,27),(15,27)])
                box(gold,17,16,12,9);line(light,(19,19),(26,19),2)
            elif k in ('backlog','testimony'):
                box(ink,6,2,21,27);box(shade,8,4,17,23)
                box(ink,2,6,22,24);box(paper,4,8,18,20)
                for y in (12,16,20):line('#94754f',(7,y),(18,y))
                box(leather,5,25,15,2)
                if k=='dialogue':
                    box(gold,16,7,12,9);poly(gold,[(18,15),(18,20),(23,15)])
                    box(light,18,9,7,2)
                elif k=='testimony':
                    poly(ink,[(16,26),(20,11),(28,3),(30,5),(26,16),(20,20)])
                    poly(light,[(20,18),(22,10),(28,5),(26,14)])
                    line(gold,(18,25),(26,9),1)
            elif k=='auto':
                box(ink,5,2,23,4);box(gold,7,3,19,2);box(ink,5,27,23,4);box(gold,7,28,19,2)
                poly(ink,[(8,6),(25,6),(24,11),(19,16),(24,22),(25,27),(8,27),(9,22),(14,16),(9,11)])
                poly('#637978',[(11,7),(22,7),(21,11),(17,15),(21,22),(22,26),(11,26),(12,22),(16,16),(12,11)])
                poly(light,[(12,10),(21,10),(17,15)]);poly(gold,[(12,25),(16,20),(18,20),(22,25)])
                box(light,16,16,1,5)
            elif k=='skip':
                # Two arrowheads (0.18.46): skip the rest of this conversation.
                poly(ink,[(3,6),(16,16),(3,26)]);poly(ink,[(15,6),(28,16),(15,26)])
                poly(gold,[(5,10),(13,16),(5,22)]);poly(gold,[(17,10),(25,16),(17,22)])
                box(light,6,12,1,4);box(light,18,12,1,4)
            elif k=='settings':
                teeth=[(12,1),(20,1),(20,5),(24,6),(27,3),(30,6),(27,10),(28,12),(31,12),(31,20),(27,20),(26,24),(29,27),(26,30),(22,27),(20,28),(20,31),(12,31),(12,27),(8,26),(5,29),(2,26),(5,22),(4,20),(1,20),(1,12),(5,12),(6,8),(3,5),(6,2),(10,5),(12,4)]
                poly(ink,teeth)
                poly(gold,[(16+(x-16)*.88,16+(y-16)*.88) for x,y in teeth])
                line(light,(13,3),(18,3),2);line(light,(4,13),(4,18),2)
                poly('#dec18a',[(12,8),(20,8),(24,12),(24,20),(20,24),(12,24),(8,20),(8,12)])
                poly(ink,[(13,10),(19,10),(22,13),(22,19),(19,22),(13,22),(10,19),(10,13)])
                poly('#65665d',[(14,13),(18,13),(20,15),(20,18),(18,20),(14,20),(12,18),(12,15)])
            elif k in ('meeting_round','meeting_stone'):
                poly(ink,[(2,12),(8,7),(24,7),(30,12),(30,23),(24,28),(8,28),(2,23)])
                poly('#b5aea0' if k=='meeting_stone' else leather,[(4,12),(9,9),(23,9),(28,12),(28,21),(23,25),(9,25),(4,21)])
                line(light,(9,11),(23,11),2)
                for x in (7,15,23):box(gold,x,1,4,4)
                if k=='meeting_stone':line(ink,(17,12),(14,17),1);line(ink,(14,17),(20,21),1)
            elif k in ('meeting_field','meeting_room'):
                if k=='meeting_room':
                    line(leather,(1,10),(16,1),2);line(leather,(16,1),(31,10),2)
                    line(leather,(3,10),(3,30),2);line(leather,(29,10),(29,30),2)
                for x,y in ((6,13),(14,9),(22,13)):
                    box(ink,x-2,y-2,7,7);box(paper,x-1,y-1,5,5)
                    box(gold,x-3,y+6,9,9)
                line(shade,(4,29),(29,29),2)
            elif k=='relations':
                line(gold,(8,8),(24,8),2);line(gold,(8,8),(16,25),2);line(gold,(24,8),(16,25),2)
                for x,y in ((3,3),(19,3),(11,20)):
                    box(ink,x,y,10,10);box(paper,x+2,y+2,6,6);box(gold,x+4,y+4,2,2)
            elif k=='people':
                poly(ink,[(11,3),(21,3),(25,7),(25,16),(21,20),(28,24),(28,30),(4,30),(4,24),(11,20),(7,16),(7,7)])
                box(shade,10,6,12,12);box(paper,12,7,8,10)
                poly(leather,[(11,21),(21,21),(25,25),(25,28),(7,28),(7,25)])
                box(gold,14,22,4,5)
            return r

screen r13_antique_button(caption,icon,command,enabled=True,compact=False,chosen=False,width=None):
    button:
        xsize (width or (104 if compact else 144 if persistent.room13_large_text else 136))
        ysize (56 if compact else 64)
        padding (5,0)
        background R13TouchSurface(focused=chosen)
        hover_background R13TouchSurface(focused=True)
        selected_background R13TouchSurface(focused=True)
        insensitive_background R13TouchSurface(disabled=True)
        action command sensitive enabled selected chosen
        alt caption tooltip (None if caption=="생각" else caption)
        hbox:
            xalign .5 yalign .75 spacing (4 if compact else 6)
            add R13AntiqueIcon(icon,size=22 if compact else 30) yalign .5 alpha (1.0 if enabled else .35)
            text caption:
                font r13_ui_font() size (r13_read_size(20,22) if compact else r13_read_size(20,24))
                color ("#efe2c2" if enabled else "#a59a86") hover_color "#fff0ce"
                yalign .5
