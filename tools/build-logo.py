# -*- coding: utf-8 -*-
"""
מחולל הלוגו של משרד עורכי דין מורן מזור.

מונוגרמה: שתי אותיות M שזורות זו בזו, כשאזור החפיפה בגוון זהב עמוק יותר
כדי לתת תחושת מתכת שזורה. סביבן מסגרת ארט-דקו עם פינות חתוכות, קו כפול
ומעוינים במרכז הקצה העליון והתחתון. מתחת: LAW OFFICE ו"משפט פלילי".

האותיות מומרות לנתיבים (outlines) ולא נשארות כ-<text>, כדי שהלוגו ייראה
זהה בכל מקום גם כשהגופן לא נטען.

הרצה מתיקיית השורש:
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

SOURCES = {
    'playfair.ttf': 'ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf',
    'cinzel.ttf':   'ofl/cinzel/Cinzel%5Bwght%5D.ttf',
    'frank.ttf':    'ofl/frankruhllibre/FrankRuhlLibre%5Bwght%5D.ttf',
}

# ------------------------------------------------------------------ פרמטרים
OVERLAP = 0.28          # חפיפה בין שתי ה-M, כאחוז מרוחב האות
FRAME_MARGIN = 0.24     # שולי המסגרת סביב האותיות, ביחס לצד הגדול
GOLD = 'C9A257'

GRAD_DARK = [('0', '#F4E0B4'), ('0.34', '#D9B471'), ('0.56', '#B08A38'),
             ('0.78', '#E8CE96'), ('1', '#9C7530')]
GRAD_DARK_DEEP = [('0', '#AB8535'), ('0.5', '#856526'), ('1', '#6A511E')]
GRAD_LIGHT = [('0', '#C9A257'), ('0.45', '#A8822F'), ('0.78', '#C19A4C'), ('1', '#8A6A24')]
GRAD_LIGHT_DEEP = [('0', '#8A6A24'), ('0.5', '#6F551C'), ('1', '#5A4516')]

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
    """(path-d, advance, bbox) כנתיבים. עברית מסודרת מימין לשמאל."""
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
    return '<path d="M%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2fZ"/>' % (
        cx, cy - r, cx + r, cy, cx, cy + r, cx - r, cy)


def single_m(size=300.0):
    d, _w, bb = run(load('playfair.ttf', 700), 'M', size)
    return d, bb


def woven(uid, stops, deep, size=300.0):
    """שתי M-ים שזורות. מחזיר (markup, bbox)."""
    d, bb = single_m(size)
    mw = bb[2] - bb[0]
    dx = mw * (1.0 - OVERLAP)
    gid, did, cid = 'g' + uid, 'd' + uid, 'c' + uid
    markup = (
        '<defs>%s%s<clipPath id="%s"><path d="%s"/></clipPath></defs>'
        '<path d="%s" fill="url(#%s)"/>'
        '<g transform="translate(%.2f 0)"><path d="%s" fill="url(#%s)"/></g>'
        '<g clip-path="url(#%s)"><g transform="translate(%.2f 0)">'
        '<path d="%s" fill="url(#%s)"/></g></g>'
        % (grad(stops, gid), grad(deep, did), cid, d,
           d, gid,
           dx, d, gid,
           cid, dx, d, did))
    return markup, (bb[0], bb[1], bb[0] + dx + mw, bb[3])


def deco_frame(box, gold):
    """מסגרת ארט-דקו מרובעת: פינות חתוכות, קו כפול, מעוין למעלה ולמטה.

    מחזירה (markup, bbox של המסגרת).
    """
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    m = max(w, h) * FRAME_MARGIN
    fx0, fy0, fx1, fy1 = x0 - m, y0 - m, x1 + m, y1 + m
    side = max(fx1 - fx0, fy1 - fy0)
    cx, cy = (fx0 + fx1) / 2.0, (fy0 + fy1) / 2.0
    fx0, fx1 = cx - side / 2.0, cx + side / 2.0
    fy0, fy1 = cy - side / 2.0, cy + side / 2.0

    def cut_rect(inset, cut, sw, opacity=1.0):
        a, b, c, d = fx0 + inset, fy0 + inset, fx1 - inset, fy1 - inset
        return ('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f '
                'L%.1f %.1f L%.1f %.1f L%.1f %.1fZ" fill="none" stroke="#%s" '
                'stroke-width="%.2f" opacity="%s"/>'
                % (a + cut, b, c - cut, b, c, b + cut, c, d - cut, c - cut, d,
                   a + cut, d, a, d - cut, a, b + cut, gold, sw, opacity))

    parts = [
        cut_rect(0.0, side * 0.16, side * 0.016),
        cut_rect(side * 0.042, side * 0.135, side * 0.009, 0.6),
    ]
    r = side * 0.030
    parts.append('<g fill="#%s">%s%s</g>'
                 % (gold, diamond(cx, fy0, r), diamond(cx, fy1, r)))
    return ''.join(parts), (fx0, fy0, fx1, fy1)


def svg(body, box, pad, label=''):
    x0, y0, x1, y1 = box
    aria = ' role="img" aria-label="%s"' % label if label else ''
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.1f %.1f %.1f %.1f"%s>\n'
            '%s\n</svg>\n'
            % (x0 - pad, y0 - pad, (x1 - x0) + pad * 2, (y1 - y0) + pad * 2, aria, body))


def seal(uid, stops, deep, gold=GOLD):
    """המונוגרמה בתוך המסגרת. מחזיר (markup, bbox)."""
    mono, box = woven(uid, stops, deep)
    frame, fbox = deco_frame(box, gold)
    return mono + frame, fbox


def mark(uid, stops, deep, gold=GOLD):
    body, box = seal(uid, stops, deep, gold)
    side = box[2] - box[0]
    return svg(body, box, side * 0.025, 'MM')


def bare(uid, stops, deep):
    """המונוגרמה בלי מסגרת, לשימושים קטנים מאוד."""
    body, box = woven(uid, stops, deep)
    return svg(body, box, (box[2] - box[0]) * 0.04, 'MM')


def flat_mark(color, gold):
    """גרסה בצבע אחד, למקומות שבהם אין מקום לגרדיאנט."""
    d, bb = single_m()
    mw = bb[2] - bb[0]
    dx = mw * (1.0 - OVERLAP)
    box = (bb[0], bb[1], bb[0] + dx + mw, bb[3])
    mono = ('<g fill="%s"><path d="%s"/>'
            '<g transform="translate(%.2f 0)"><path d="%s"/></g></g>' % (color, d, dx, d))
    frame, fbox = deco_frame(box, gold)
    side = fbox[2] - fbox[0]
    return svg(mono + frame, fbox, side * 0.025, 'MM')


def lockup(uid, stops, deep, gold=GOLD, hebrew_color=None):
    seal_body, sbox = seal(uid, stops, deep, gold)
    side = sbox[2] - sbox[0]

    law_d, law_w, _ = run(load('cinzel.ttf', 500), 'LAW OFFICE', side * 0.115, tracking=side * 0.044)
    heb_d, heb_w, _ = run(load('frank.ttf', 500), 'משפט פלילי', side * 0.165,
                          tracking=side * 0.014, rtl=True)

    W = max(side, law_w, heb_w) * 1.16
    cx = W / 2.0
    # מזיזים את החותם למרכז הלוקאפ
    seal_dx = cx - (sbox[0] + side / 2.0)
    top = 0.0
    seal_dy = top - sbox[1]

    law_y = seal_dy + sbox[3] + side * 0.215
    rule_y = law_y + side * 0.105
    heb_y = rule_y + side * 0.215
    H = heb_y + side * 0.07

    p = ['<g transform="translate(%.2f %.2f)">%s</g>' % (seal_dx, seal_dy, seal_body)]
    p.append('<g fill="url(#g%s)" transform="translate(%.2f %.2f)"><path d="%s"/></g>'
             % (uid, cx - law_w / 2.0, law_y, law_d))
    half = max(heb_w / 2.0 + side * 0.055, side * 0.26)
    p.append('<g fill="#%s"><rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" opacity=".75"/></g>'
             % (gold, cx - half, rule_y, half * 2, side * 0.006))
    if hebrew_color:
        p.append('<g fill="%s" transform="translate(%.2f %.2f)"><path d="%s"/></g>'
                 % (hebrew_color, cx - heb_w / 2.0, heb_y, heb_d))
    else:
        p.append('<g fill="url(#g%s)" transform="translate(%.2f %.2f)"><path d="%s"/></g>'
                 % (uid, cx - heb_w / 2.0, heb_y, heb_d))

    return svg(''.join(p), (0, 0, W, H), side * 0.035, 'MM Law Office · משפט פלילי')


def favicon(uid, stops, deep):
    body, box = seal(uid, stops, deep)
    side = box[2] - box[0]
    k = 436.0 / side
    tx = 256.0 - (box[0] + side / 2.0) * k
    ty = 256.0 - (box[1] + (box[3] - box[1]) / 2.0) * k
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">\n'
            '<rect width="512" height="512" fill="#0B2641"/>\n'
            '<g transform="translate(%.2f %.2f) scale(%.4f)">%s</g>\n</svg>\n'
            % (tx, ty, k, body))


def write(path, data):
    io.open(path, 'w', encoding='utf-8').write(data)
    print('%-34s %6d bytes' % (path, len(data.encode('utf-8'))))


if not os.path.isdir(OUT):
    raise SystemExit('run from the project root')

ensure_fonts()
write(os.path.join(OUT, 'logo.svg'), lockup('d', GRAD_DARK, GRAD_DARK_DEEP))
write(os.path.join(OUT, 'logo-light.svg'),
      lockup('l', GRAD_LIGHT, GRAD_LIGHT_DEEP, gold='A8822F', hebrew_color='#1B3A56'))
write(os.path.join(OUT, 'monogram.svg'), mark('m', GRAD_DARK, GRAD_DARK_DEEP))
write(os.path.join(OUT, 'monogram-light.svg'), mark('ml', GRAD_LIGHT, GRAD_LIGHT_DEEP, gold='A8822F'))
write(os.path.join(OUT, 'monogram-bare.svg'), bare('b', GRAD_DARK, GRAD_DARK_DEEP))
write(os.path.join(OUT, 'monogram-white.svg'), flat_mark('#FFFFFF', 'FFFFFF'))
write(os.path.join(OUT, 'favicon.svg'), favicon('f', GRAD_DARK, GRAD_DARK_DEEP))
