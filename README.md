# Moran Zilka Mazor — Law & Mediation Office

Hebrew (RTL) one-page site for **Moran Zilka Mazor**, an Israeli family-law attorney and
certified mediator. Art-deco aesthetic derived from her logo: deep navy `#08152C`,
gold `#C7AA7C`, hairline geometry, sunburst motifs.

**Static only** — plain HTML, CSS and vanilla JS. No build step, no backend, no API,
no database. Drop the folder on any static host and it works.

---

## Quick start

```bash
# any static server works
python -m http.server 8080
# → http://localhost:8080
```

There is nothing to install and nothing to compile.

## Structure

```
index.html            # the landing page (hero, pillars, about, practice, mediation,
                      # process, credo, FAQ, contact)
accessibility.html    # הצהרת נגישות — required for Israeli business sites
privacy.html          # מדיניות פרטיות ותנאי שימוש
404.html
robots.txt, sitemap.xml
assets/
  css/style.css       # single stylesheet, design tokens at the top
  js/site.js          # sticky header, mobile menu, scroll reveal, form, a11y toolbar
  monogram.svg        # MZ monogram, traced out of the original logo
  wordmark.svg        # "MORAN ZILKA MAZOR" lettering, traced out of the original logo
  favicon.svg
  logo-art-deco.svg   # the full original logo (source of the two above)
  img/                # logo renders + generated og-cover.png
CONTENT.md            # Hebrew checklist of everything the client still has to supply
```

`monogram.svg` and `wordmark.svg` were extracted from `logo-art-deco.svg` by isolating the
relevant `<path>` elements and computing a tight `viewBox`, so the site uses real vectors of
her logo rather than a screenshot of it. The Hebrew line under the wordmark is live text
(the traced version of it was uneven), set in Frank Ruhl Libre.

## Type & colour

| Role | Family |
|---|---|
| Display / headings (Hebrew) | Frank Ruhl Libre |
| Body (Hebrew) | Assistant |
| Latin accents, numerals, eyebrows | Cormorant Garamond |

Loaded from Google Fonts. Every colour, size and spacing value is a CSS custom property in
the `:root` block at the top of `assets/css/style.css`.

## The contact form has no backend — by design

On submit, `site.js` composes the message client-side and opens either
`https://wa.me/<number>?text=…` or a `mailto:` link. Nothing is stored or transmitted by the
site itself. That keeps hosting free, removes any privacy/GDPR surface, and matches the
"landing page, no server" brief.

The WhatsApp number and email used by the form live in the `CONTACT` object at the top of
`assets/js/site.js`. The same values also appear as plain links in the HTML (so they work
with JS disabled) — see below for updating both at once.

## Updating the placeholder details

The site ships with obvious placeholders. Replace them everywhere in one pass:

```bash
cd MoranZilkaMazor

# phone (three formats: display, tel: link, JSON-LD)
grep -rl '050-000-0000'      --include='*.html' . | xargs sed -i 's/050-000-0000/054-123-4567/g'
grep -rl '+972500000000'     --include='*.html' . | xargs sed -i 's/+972500000000/+972541234567/g'
grep -rl '+972-50-000-0000'  --include='*.html' . | xargs sed -i 's/+972-50-000-0000/+972-54-123-4567/g'

# whatsapp (html links + site.js)
grep -rl '972500000000' --include='*.html' --include='*.js' . | xargs sed -i 's/972500000000/972541234567/g'

# email
grep -rl 'office@zilka-mazor.co.il' --include='*.html' --include='*.js' . | xargs sed -i 's/office@zilka-mazor.co.il/NEW@EMAIL/g'

# domain (canonical, og:url, sitemap, robots)
grep -rl 'www.zilka-mazor.co.il' . | xargs sed -i 's#www.zilka-mazor.co.il#NEW-DOMAIN#g'
```

Remaining `[...]` placeholders (office address, year of admission, service area, physical
accessibility) are listed in **[CONTENT.md](CONTENT.md)**, written in Hebrew for the client.

### Portrait photo

In `index.html`, inside `.portrait__frame`, replace the `.portrait__ph` div with:

```html
<img src="assets/img/moran.jpg" alt="מורן זילכה מזור, עורכת דין ומגשרת">
```

Use a vertical 4:5 image (e.g. 1200×1500).

### Social-media icon regeneration

`assets/img/og-cover.png` (1200×630, used for WhatsApp/Facebook previews) was rendered from
`_og.html` with headless Chrome. To regenerate after a branding change, re-create that file
and screenshot it at 1200×630.

## Accessibility

Israeli business sites are required to be accessible. Implemented here **without any
third-party widget** (no external script, no cookie, nothing to pay for):

- Custom accessibility toolbar: text size, high-contrast mode, link highlighting, readable
  font, motion stop, reset. Preferences persist in `localStorage`.
- Full keyboard navigation, visible focus ring, skip-to-content link.
- Semantic headings, `aria-*` on interactive controls, alt text on images.
- Honours `prefers-reduced-motion`.
- `accessibility.html` is the statement itself (ת״י 5568 / WCAG 2.1 AA).

## Hosting

Both options are free and support a custom domain with HTTPS.

**GitHub Pages** (currently used): repo → Settings → Pages → Source: `main`, folder `/`.
Serves `index.html`, `404.html` and custom domains out of the box. For a custom domain add a
`CNAME` file containing the domain and point DNS at GitHub.

**Cloudflare Pages** (recommended for Israeli traffic): connect the repo, leave the build
command empty and set the output directory to `/`. Faster edge presence in the region and
free unlimited bandwidth.

No build step means either host deploys in seconds on every push.

## Browser support

Modern evergreen browsers. Uses `IntersectionObserver`, CSS logical properties,
`clamp()`, `conic-gradient` and `100svh`; degrades to a readable static page if any of
them are missing.
