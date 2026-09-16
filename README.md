# משרד עורכי דין מורן מזור — Criminal Defence Landing Page

Hebrew (RTL) landing page for **Moran Mazor**, an Israeli criminal defence attorney.
All copy on the site is the client's own text, supplied verbatim.

**Static only** — plain HTML, CSS and vanilla JS. No build step, no backend, no API,
no database. Drop the folder on any static host and it works.

Live: https://talmoda.github.io/moran-mazor/

## Design

Built to match a reference landing page the client chose: navy header and panels, gold
accents, light content sections, photo hero, icon cards, split about section and a
three-column contact block.

| Token | Value |
|---|---|
| navy (header, panels, footer) | `#0B2641` / `#102C48` / `#17395C` |
| gold (CTA, icons, rules) | `#C9A257`, light `#D7B16B`, dark `#B18B3A` |
| section backgrounds | `#F5F4F1` / `#F1F0EE` |
| text / muted | `#18344C` / `#66788A` |
| type | Heebo (headings + body), Assistant (fallback) |

All of it lives in the `:root` block at the top of `assets/css/style.css`.

## Structure

```
index.html            # header · hero · three principles · eleven practice areas
                      # (cards + <dialog> details) · about · approach · quote ·
                      # contact · footer
accessibility.html    # הצהרת נגישות — required for Israeli business sites
privacy.html          # מדיניות פרטיות ותנאי שימוש
404.html
robots.txt, sitemap.xml
assets/
  css/style.css       # single stylesheet
  js/site.js          # mobile nav, scroll reveal, nav spy, header shrink +
                      # scroll progress, practice dialogs, accessibility toolbar
  logo.svg            # full MM lockup, gold on dark
  logo-light.svg      # full MM lockup for light backgrounds
  monogram.svg        # MM mark, gold
  monogram-white.svg  # MM mark, white
  favicon.svg
  img/hero.jpg        # hero photo
  img/about.jpg       # about photo — replace with the client's portrait
  img/og-cover.png    # generated social share card
brand/                # the original logo files (not served)
CONTENT.md            # Hebrew checklist of everything the client still has to supply
```

## Logo

The client asked for a logo in the style of a reference card she sent. It is an **MM**
crest for Moran Mazor: two **M** glyphs woven together with the overlap in a deeper gold,
set inside an art-deco frame with chamfered corners, a double rule and diamond finials,
over **LAW OFFICE** and **משפט פלילי**.

`tools/build-logo.py` generates the whole family. It pulls the three OFL fonts (Playfair
Display for the M, Cinzel for LAW OFFICE, Frank Ruhl Libre for the Hebrew), instances the
variable fonts at the right weight, and converts the glyphs to **outlines** with
fontTools, so the logo renders identically everywhere without a webfont. The woven
overlap is a `clipPath` of the first M filled with a darker gradient. Overlap, frame
margin, sizes and wording are parameters at the top of the script. Variants: full lockup
for dark and light backgrounds, the crest in gold, light and white, a frameless mark for
tiny uses, and a square icon. PNG exports and an overview sheet live in `brand/exports/`.

The previous art-deco MZL logo is kept in `brand/` for history and is no longer used.

## Photos

`hero.jpg` and `about.jpg` are the two free-licence Unsplash photos from the reference
design, downloaded and served locally rather than hotlinked. **`about.jpg` shows other
people and must be replaced with the client's own portrait** — see `CONTENT.md`.

`brand/exports/` holds PNG renders of the logo (full lockup, mark, icon) for use outside
the web, alongside the SVG sources.

To swap the hero photo without touching CSS, set the custom property on the section:

```html
<section class="hero" style="--hero-img:url('assets/img/my-photo.jpg')">
```

## There is no contact form — deliberately

A form needs a server to receive submissions. Instead, the contact section offers three
direct actions: WhatsApp (pre-filled message), phone and email. Nothing is stored, there
is no third-party form service to pay for, and the enquiry lands straight in the client's
WhatsApp or inbox. Adding a real form later is a small change.

## Updating the placeholder details

The site ships with obvious placeholders. Replace them everywhere in one pass:

```bash
cd MoranZilkaMazor

# phone (display, tel: link, JSON-LD)
grep -rl '050-000-0000'     --include='*.html' . | xargs sed -i 's/050-000-0000/054-123-4567/g'
grep -rl '+972500000000'    --include='*.html' . | xargs sed -i 's/+972500000000/+972541234567/g'
grep -rl '+972-50-000-0000' --include='*.html' . | xargs sed -i 's/+972-50-000-0000/+972-54-123-4567/g'

# whatsapp
grep -rl '972500000000' --include='*.html' . | xargs sed -i 's/972500000000/972541234567/g'

# email
grep -rl 'office@mazor-law.co.il' --include='*.html' . | xargs sed -i 's/office@mazor-law.co.il/NEW@EMAIL/g'

# domain (canonical, og:url, sitemap, robots)
grep -rl 'www.mazor-law.co.il' . | xargs sed -i 's#www.mazor-law.co.il#NEW-DOMAIN#g'
```

Remaining `[...]` placeholders (office address, service area, physical accessibility) are
listed in **[CONTENT.md](CONTENT.md)**, written in Hebrew for the client.

## Accessibility

Israeli business sites are required to be accessible. Implemented here **without any
third-party widget** (no external script, no cookie, nothing to pay for):

- Accessibility toolbar: text size, high-contrast mode, link highlighting, readable font,
  motion stop, reset. Preferences persist in `localStorage`.
- Full keyboard navigation, visible focus ring, skip-to-content link.
- Practice-area details use native `<dialog>` (Esc to close, focus returns to the card).
- Honours `prefers-reduced-motion`; the quote carousel does not autoplay under it.
- `accessibility.html` is the statement itself (ת״י 5568 / WCAG 2.1 AA).

## Motion

Hero content rises in on a stagger behind a slow Ken Burns drift on the photo; sections
reveal on scroll; a gold progress bar tracks scroll in the header, which shrinks past 40px;
icons lift on hover, the gold buttons catch a shine sweep, and the WhatsApp button pulses.
All chevrons are drawn from CSS borders, because ‹ and › are bidi-mirrored and flip in RTL.
Everything is CSS-driven and fully disabled by both `prefers-reduced-motion` and the
"עצירת אנימציות" toggle in the accessibility menu.

## Local preview

```bash
python -m http.server 8080
# → http://localhost:8080
```

## Hosting

**GitHub Pages** (currently used): repo → Settings → Pages → Source `main`, folder `/`.

**Cloudflare Pages** (recommended for Israeli traffic): connect the repo, empty build
command, output directory `/`. Faster edge presence in the region.

No build step means either host deploys in seconds on every push.

## Credit

The footer carries a "נבנה על ידי Dayanamic" credit linking to
[dayanamic.com/he](https://dayanamic.com/he), using the Dayanamic mark from
`assets/img/dayanamic-mark.svg`.
