# One set of cut-paper borders shared by every interactive surface.
init -80 python:
    def r13_sticker_button(primary=False,focused=False,disabled=False):
        row=2 if primary else 1 if focused else 0
        paper=Crop((64,64+293*row,1410,292),"assets/ui-b-sticker/button_sheet.png")
        # Scale the source uniformly first, then extend only its blank centre.
        surface=Frame(Transform(paper,zoom=1.0/3.0),27,16,27,16)
        return Transform(surface,alpha=.65) if disabled else surface
