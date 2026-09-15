# עו״ד מורן זילכה מזור — Law & Mediation Landing Page

Hebrew (RTL) landing page for **Moran Zilka Mazor**, an Israeli family-law attorney and
certified mediator.

**Static only** — plain HTML, CSS and vanilla JS. No build step, no backend, no API,
no database. Drop the folder on any static host and it works.

Live: https://talmoda.github.io/moran-zilka-mazor/

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
index.html            # header · hero · benefits · practice (6 cards + dialogs) ·
                      # mediation · about · quote carousel · FAQ · contact · footer
accessibility.html    # הצהרת נגישות — required for Israeli business sites
privacy.html          # מדיניות פרטיות ותנאי שימוש
404.html
robots.txt, sitemap.xml
assets/
  css/style.css       # single stylesheet
  js/site.js          # mobile nav, scroll reveal, nav spy, quote carousel,
                      # practice dialogs, accessibility toolbar
  monogram.svg        # MZ monogram, traced out of the client's logo
  wordmark.svg        # "MORAN ZILKA MAZOR" lettering, same source
  favicon.svg
  img/hero.jpg        # hero photo
  img/about.jpg       # about photo — replace with the client's portrait
  img/og-cover.png    # generated social share card
brand/                # the original logo files (not served)
CONTENT.md            # Hebrew checklist of everything the client still has to supply
```

`monogram.svg`, `wordmark.svg` and `favicon.svg` were extracted from the client's logo SVG
by isolating the relevant `<path>` elements and computing a tight `viewBox`, so the site
uses real vectors of her logo rather than a screenshot of it.

## Photos

`hero.jpg` and `about.jpg` are the two free-licence Unsplash photos from the reference
design, downloaded and served locally rather than hotlinked. **`about.jpg` shows other
people and must be replaced with the client's own portrait** — see `CONTENT.md`.

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
grep -rl 'office@zilka-mazor.co.il' --include='*.html' . | xargs sed -i 's/office@zilka-mazor.co.il/NEW@EMAIL/g'

# domain (canonical, og:url, sitemap, robots)
grep -rl 'www.zilka-mazor.co.il' . | xargs sed -i 's#www.zilka-mazor.co.il#NEW-DOMAIN#g'
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
