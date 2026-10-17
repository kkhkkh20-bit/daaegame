"""Pure map-only conversion; no files or runtime registries are written here.

Call only after preserving/verifying an approved original. Matches the approved
Solbang map export's Lanczos resize -> nearest 2px grid; dialogue is not an input.
"""
from PIL import Image

def derive_map_image(original):
    source=original.convert('RGBA')
    if source.width<1 or source.height<1:raise ValueError('empty source')
    if source.getchannel('A').getextrema()[0]!=0:raise ValueError('transparent background required')
    if source.getchannel('A').getbbox() is None:raise ValueError('empty alpha')
    height=768;content_width=max(2,round(source.width*height/source.height))
    width=content_width+(content_width%2)
    canvas=Image.new('RGBA',(width,height))
    canvas.alpha_composite(source.resize((content_width,height),Image.Resampling.LANCZOS))
    image=canvas.resize((width//2,height//2),Image.Resampling.NEAREST).resize((width,height),Image.Resampling.NEAREST)
    # WebP canonicalizes hidden RGB; remove only fully transparent colour noise.
    image.putdata([(r,g,b,a) if a else (0,0,0,0) for r,g,b,a in image.getdata()])
    return image,dict(source_size=list(source.size),export_size=list(image.size),content_size=[content_width,height],grid=2,
        source_to_export=[content_width/source.width,height/source.height],padding_right=width-content_width)

def validate_map_image(image):
    if image.mode!='RGBA' or image.height!=768 or image.width%2:raise ValueError('expected even-width RGBA 768 map derivative')
    if image.getchannel('A').getextrema()[0]!=0:raise ValueError('alpha background lost')
    if image.getchannel('A').getbbox() is None:raise ValueError('empty alpha')
    small=image.resize((image.width//2,384),Image.Resampling.NEAREST)
    if small.resize(image.size,Image.Resampling.NEAREST).tobytes()!=image.tobytes():raise ValueError('2px grid mismatch')
