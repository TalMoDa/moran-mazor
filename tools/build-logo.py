# -*- coding: utf-8 -*-
"""
מחולל הלוגו של משרד עורכי דין מורן זילכה מזור.

מונוגרמה MM, קו דק עם מעוינים, LAW OFFICE, ומתחת "משפט פלילי".
האותיות מומרות לנתיבים (outlines) ולא נשארות כ-<text>, כדי שהלוגו ייראה
זהה בכל מקום גם כשהגופן לא נטען.

הרצה מתיקיית השורש של הפרויקט:
    python tools/build-logo.py
"""
import io
import os
import urllib.request

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.varLib.instancer import instantiateVariableFont

OUT = 'assets'
FONTS = os.path.join('tools', 'fonts')

# הגופנים (OFL) לא נשמרים ב-repo; מורידים בפעם הראשונה.
SOURCES = {
    'playfair.ttf': 'ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf',
    'cinzel.ttf':   'ofl/cinzel/Cinzel%5Bwght%5D.ttf',
    'frank.ttf':    'ofl/frankruhllibre/FrankRuhlLibre%5Bwght%5D.ttf',
}

GOLD_ON_DARK = [
    ('0',    '#F2DCAE'),
    ('0.30', '#D9B471'),
    ('0.52', '#B18B3A'),
    ('0.74', '#E6CB92'),
    ('1',    '#9E7833'),
]
GOLD_ON_LIGHT = [
    ('0',    '#C9A257'),
    ('0.45', '#A8822F'),
    ('0.75', '#C9A257'),
    ('1',    '#8A6A24'),
]

MONO_TRACK = -2      # צמידות בין שתי ה-M
_cache = {}


def ensure_fonts():
    if not os.path.isdir(FONTS):
        os.makedirs(FONTS)
    for name, rel in SOURCES.items():
        dest = os.path.join(FONTS, name)
        if not os.path.exists(dest):
            print('downloading', name)
            urllib.request.urlretrieve(
                'https://raw.githubusercontent.com/google/fonts/main/' + rel, dest)


def load(name, weight):
    key = (name, weight)
    if key not in _cache:
        font = TTFont(os.path.join(FONTS, name))
        if 'fvar' in font:
            font = instantiateVariableFont(font, {'wght': weight}, inplace=False)
        _cache[key] = font
    return _cache[key]


def run(font, text, size, tracking=0.0, rtl=False):
    """(path-d, advance, bbox) עבור מחרוזת, כנתיבים.

    ה-bbox הוא הגבולות האמיתיים של הקווים במערכת של ה-SVG (y יורד, קו
    הבסיס ב-0), כדי שאפשר יהיה לחתוך סימן בדיוק לפי האותיות.
    עברית נכתבת מימין לשמאל, ולכן התווים מסודרים בסדר הפוך.
    """
    upm = font['head'].unitsPerEm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    scale = size / float(upm)
    chars = list(reversed(text)) if rtl else list(text)
    fmt = lambda v: ('%.2f' % v).rstrip('0').rstrip('.')
    x = 0.0
    parts = []
    bounds = BoundsPen(gs)
    for ch in chars:
        gname = cmap.get(ord(ch))
        if gname is None:
            x += size * 0.32 + tracking
            continue
        glyph = gs[gname]
        xform = (scale, 0, 0, -scale, x, 0)
        pen = SVGPathPen(gs, ntos=fmt)
        glyph.draw(TransformPen(pen, xform))
        glyph.draw(TransformPen(bounds, xform))
        d = pen.getCommands()
        if d:
            parts.append(d)
        x += glyph.width * scale + tracking
    if chars:
        x -= tracking
    return ' '.join(parts), x, bounds.bounds


def grad(stops, gid):
    body = ''.join('<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in stops)
    return '<linearGradient id="%s" x1="0" y1="0" x2="0" y2="1">%s</linearGradient>' % (gid, body)


def diamond(cx, cy, r):
    return ('<path d="M%.1f %.1f %.1f %.1f %.1f %.1f %.1f %.1fZ"/>'
            % (cx, cy - r, cx + r, cy, cx, cy + r, cx - r, cy))


def monogram_paths():
    return run(load('playfair.ttf', 700), 'MM', 300, tracking=MONO_TRACK)


def lockup(stops, gid, rule_color, hebrew_color=None):
    mm_d, mm_w, _ = monogram_paths()
    law_d, law_w, _ = run(load('cinzel.ttf', 500), 'LAW OFFICE', 58, tracking=22)
    heb_d, heb_w, _ = run(load('frank.ttf', 500), 'משפט פלילי', 86, tracking=7, rtl=True)

    W = 1040.0
    cx = W / 2.0
    r1_y, r1_half = 372.0, 236.0
    r2_y = 500.0
    r2_half = max(126.0, heb_w / 2.0 + 18.0)
    H = 644.0

    p = ['<defs>%s</defs>' % grad(stops, gid), '<g fill="url(#%s)">' % gid]
    p.append('<g transform="translate(%.1f 300)"><path d="%s"/></g>' % (cx - mm_w / 2.0, mm_d))
    p.append('<g transform="translate(%.1f 452)"><path d="%s"/></g>' % (cx - law_w / 2.0, law_d))
    if hebrew_color is None:
        p.append('<g transform="translate(%.1f 590)"><path d="%s"/></g>' % (cx - heb_w / 2.0, heb_d))
    p.append('</g>')
    if hebrew_color is not None:
        p.append('<g fill="%s" transform="translate(%.1f 590)"><path d="%s"/></g>'
                 % (hebrew_color, cx - heb_w / 2.0, heb_d))

    p.append('<g fill="%s">' % rule_color)
    p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="1.6"/>' % (cx - r1_half, r1_y, r1_half * 2))
    p.append(diamond(cx - r1_half - 13, r1_y + 0.8, 6.5))
    p.append(diamond(cx + r1_half + 13, r1_y + 0.8, 6.5))
    p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="1.2"/>' % (cx - r2_half, r2_y, r2_half * 2))
    p.append('</g>')

    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" '
            'role="img" aria-label="MM Law Office · משפט פלילי">\n%s\n</svg>\n'
            % (W, H, '\n'.join(p)))


def mark(fill, defs=''):
    """המונוגרמה לבדה, חתוכה בדיוק לפי האותיות."""
    mm_d, _w, bb = monogram_paths()
    x0, y0, x1, y1 = bb
    pad = 6.0
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.1f %.1f %.1f %.1f" '
            'role="img" aria-label="MM">\n%s<g fill="%s"><path d="%s"/></g>\n</svg>\n'
            % (x0 - pad, y0 - pad, (x1 - x0) + pad * 2, (y1 - y0) + pad * 2,
               defs, fill, mm_d))


def favicon(stops, gid):
    mm_d, _w, bb = monogram_paths()
    x0, y0, x1, y1 = bb
    box = 344.0                       # רוחב האותיות בתוך המסגרת
    k = box / (x1 - x0)
    tx = 256.0 - (x0 + (x1 - x0) / 2.0) * k
    ty = 256.0 - (y0 + (y1 - y0) / 2.0) * k
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">\n'
            '<defs>%s</defs>\n'
            '<rect width="512" height="512" fill="#0B2641"/>\n'
            '<g fill="none" stroke="#C9A257" stroke-width="9">'
            '<rect x="30" y="30" width="452" height="452"/></g>\n'
            '<g fill="url(#%s)" transform="translate(%.2f %.2f) scale(%.4f)">'
            '<path d="%s"/></g>\n</svg>\n'
            % (grad(stops, gid), gid, tx, ty, k, mm_d))


def write(path, data):
    io.open(path, 'w', encoding='utf-8').write(data)
    print('%-34s %6d bytes' % (path, len(data.encode('utf-8'))))


if not os.path.isdir(OUT):
    raise SystemExit('run from the project root')

ensure_fonts()
write(os.path.join(OUT, 'logo.svg'), lockup(GOLD_ON_DARK, 'gd', '#C9A257'))
write(os.path.join(OUT, 'logo-light.svg'), lockup(GOLD_ON_LIGHT, 'gl', '#B18B3A', hebrew_color='#1B3A56'))
write(os.path.join(OUT, 'monogram.svg'), mark('url(#gm)', '<defs>%s</defs>\n' % grad(GOLD_ON_DARK, 'gm')))
write(os.path.join(OUT, 'monogram-white.svg'), mark('#FFFFFF'))
write(os.path.join(OUT, 'favicon.svg'), favicon(GOLD_ON_DARK, 'gf'))
