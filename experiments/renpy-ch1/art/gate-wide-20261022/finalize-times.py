"""오후·저녁 외곽 정리, 원본 보존, 미리보기 및 검증."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
from scipy.ndimage import gaussian_filter1d
import numpy as np

out = Path(__file__).resolve().parent
root = out.parent.parent
for time in ('afternoon', 'evening'):
    src = Image.open(root / f'game/assets/room13-pixel-ready-gate0173-{time}.webp').convert('RGB').resize((1920, 720), Image.Resampling.NEAREST)
    gen = Image.open(out / f'generated-{time}.png').convert('RGB')
    gen = gen.resize((2560, 960), Image.Resampling.LANCZOS)
    gen = gen.resize((1280, 480), Image.Resampling.BOX).resize((2560, 960), Image.Resampling.NEAREST)
    original = np.asarray(gen).astype(float)
    a = original.copy()
    b = np.asarray(src).astype(float)
    # 하늘의 넓은 색상 단차를 중앙 바깥 위쪽에서만 완화한다.
    sky_delta = gaussian_filter1d(b[0]-original[200, 320:2240], 16, axis=0)
    for distance in range(1, 161):
        a[200-distance, 320:2240] += (1-distance/161) ** 2 * sky_delta
    original = a.copy()
    for k in range(1, 7):
        weight = (7-k)/7
        a[200:920, 320-k] += weight * (b[:, 0]-original[200:920, 320])
        a[200:920, 2239+k] += weight * (b[:, -1]-original[200:920, 2239])
        a[200-k, 320:2240] += weight * (b[0]-original[200, 320:2240])
        a[919+k, 320:2240] += weight * (b[-1]-original[919, 320:2240])
    final = Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
    final.paste(src, (320, 200))
    final.save(out / f'gate-wide-{time}.png')
    preview = final.resize((1920, 720), Image.Resampling.NEAREST)
    draw = ImageDraw.Draw(preview)
    draw.rectangle((0, 0, 1279, 719), outline=(255, 70, 100), width=2)
    draw.rectangle((640, 0, 1919, 719), outline=(35, 235, 210), width=2)
    preview.save(out / f'preview-75-{time}.png')
    assert final.size == (2560, 960)
    assert ImageChops.difference(final.crop((320, 200, 2240, 920)), src).getbbox() is None
    assert preview.size == (1920, 720)
    print(f'{time}: 2560×960, 중앙 모든 RGB 픽셀 동일, 미리보기 1920×720 검증 통과')
