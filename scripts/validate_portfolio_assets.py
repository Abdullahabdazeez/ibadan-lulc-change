from pathlib import Path
from PIL import Image, ImageStat

OUT = Path('outputs/charts')
files = [
    'portfolio_area_comparison.png',
    'portfolio_net_change.png',
    'portfolio_new_builtup_origin.png',
    'portfolio_validation.png',
]

for name in files:
    path = OUT / name
    if not path.exists():
        raise SystemExit(f'MISSING: {path}')
    if path.stat().st_size < 20_000:
        raise SystemExit(f'FILE TOO SMALL: {path} ({path.stat().st_size} bytes)')
    with Image.open(path) as im:
        im.verify()
    with Image.open(path).convert('RGB') as im:
        w, h = im.size
        if w < 1500 or h < 900:
            raise SystemExit(f'LOW RESOLUTION: {path} = {w}x{h}')
        extrema = ImageStat.Stat(im).extrema
        if all(lo == hi for lo, hi in extrema):
            raise SystemExit(f'BLANK/UNIFORM IMAGE: {path}')
        print(f'PASS {name}: {w}x{h}, {path.stat().st_size} bytes')

print('QA PASS: all portfolio PNG assets are valid, high-resolution, and non-blank.')