"""Optimize images for the site: WebP (600w + full) and JPEG fallback.
Run: python3 tools/optimize_images.py <app_img_dir> <hero_src>"""
import sys, os
from PIL import Image, ImageOps
app, hero = sys.argv[1], sys.argv[2]
out = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img')
def save(im, base, widths, jpg_w):
    im = ImageOps.exif_transpose(im).convert('RGB')
    for w in widths:
        r = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(f'{base}-{w}.webp', 'WEBP', quality=78, method=6)
    r = im if im.width <= jpg_w else im.resize((jpg_w, round(im.height * jpg_w / im.width)), Image.LANCZOS)
    r.save(f'{base}.jpg', 'JPEG', quality=80, optimize=True, progressive=True)
sizes = {}
for i in range(1, 30):
    im = Image.open(f'{app}/works/work{i}.jpg')
    save(im, f'{out}/works/work{i}', [600, 1000], 1000)
    sizes[i] = im.size
h = Image.open(hero)
save(h, f'{out}/hero/hero', [960, 1920], 1600)
save(Image.open(f'{app}/tom-studio.jpg'), f'{out}/tom-studio', [700, 1400], 1400)
# OG image 1200x630 from hero
hh = ImageOps.exif_transpose(h).convert('RGB'); W, H = hh.size; th = round(W * 630 / 1200)
top = max(0, min(H - th, int(H * .45 - th / 2)))
hh.crop((0, top, W, top + th)).resize((1200, 630), Image.LANCZOS).save(f'{out}/og.jpg', 'JPEG', quality=82, optimize=True)
# Icons from logo (on black, round-friendly)
logo = Image.open(f'{app}/logo-dark.png').convert('RGBA')
for s, name in [(32, 'favicon-32.png'), (180, 'apple-touch-icon.png'), (192, 'icon-192.png'), (512, 'icon-512.png'), (96, 'logo-96.png')]:
    bg = Image.new('RGBA', (s, s), (11, 10, 13, 255)); pad = round(s * .1)
    l = logo.copy(); l.thumbnail((s - 2 * pad, s - 2 * pad), Image.LANCZOS)
    bg.alpha_composite(l, ((s - l.width) // 2, (s - l.height) // 2)); bg.convert('RGB').save(f'{out}/{name}', optimize=True)
print({k: v for k, v in sizes.items()})
