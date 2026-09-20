# finalstretch.org

The website for **The Final Stretch Project** — a free, open-source project building iOS apps that carry public data the rest of the way to the people it's about.

## What this is

A fully static site: plain HTML and CSS. Deliberately:

- **Almost no JavaScript.** The single script on the site is ~40 inline lines in `index.html` that drive the app carousel (arrows + autoplay). It stores nothing and makes no network requests — the privacy page and footer say exactly this, so keep it true if you touch it.
- **No analytics, no cookies.** The footer says so, and it has to stay true.
- **No external requests.** System font stacks only (sans UI + monospace accents); the favicon is an inline SVG data URI. The page loads nothing from any third party.
- **Accessible.** Semantic landmarks, skip link, visible focus styles, rem-based sizing (respects browser text-size settings), dark mode via `prefers-color-scheme`, reduced-motion support (disables carousel autoplay and scroll animations).
- **Visual identity:** cool slate/graphite neutrals with a repo-blue accent (`#0969da` light / `#1f6feb` dark) and monospace kickers/tags — an open-source, GitHub-adjacent look rather than a marketing-site one. All tokens live in the `:root` block of `style.css`. Scroll-driven reveal animations are progressive enhancement via CSS `animation-timeline`.

## Files

| File | Purpose |
|---|---|
| `index.html` | The main site (single page; nav links are same-page anchors) |
| `logo-seal.png` | The embossed seal (1024×1024, transparent background): coined relief with "THE FINAL STRETCH PROJECT" / "FINALSTRETCH.ORG" arced around the rim and the route mark in the centre (open node = data → dotted run → solid final segment → filled node = person, reached). For large uses: GitHub org avatar, README banner, print. Regenerate with `python3 brand/emboss.py` after editing `brand/mask.svg` (needs Pillow + numpy; macOS only — it rasterizes via `qlmanage`). |
| `logo-header.png` | 256px header medallion: same coin, no rim lettering (illegible small), enlarged deeper-embossed centre mark. Regenerate with `python3 brand/emboss.py header` (mask: `brand/mask-header.svg`). |
| `logo-hero.webp` | 560px seal stamped across the hero's top-right corner (~38KB, lossy WebP with alpha — the radial gradient bands if quantized as PNG, so keep it WebP). Its artwork is rotated 90° CCW (`brand/mask-hero.svg`) so "THE FINAL STRETCH PROJECT" arcs through the visible bottom-left of the crop, and it is re-lit at that orientation — never rotate the finished render instead, that flips the emboss lighting. Regenerate: `python3 brand/emboss.py hero`. |
| `logo.svg` | Vector version of the seal (flat-emboss approximation). The favicon deliberately uses a simplified flat medallion of the same mark — embossed rim text is illegible at 16px. Keep all logo assets in sync if the mark changes. |
| `trialhead-icon.webp`, `rxcall-icon.webp` | 256px app icons shown in the app cards and phone mockup (from the full-size sources `trialhead-logo-2048.png` / `rxcall-icon-4096.png`, which stay in the repo as masters). Rounded corners come from CSS, not the files. |
| `brand/` | Seal render pipeline: `base.svg` (coin), `mask.svg` (raised elements), `emboss.py` (height-map lighting → `logo-seal.png`). |
| `privacy.html` | Project-wide privacy policy (site + apps overview, links to per-app policies) |
| `trialhead/privacy.html`, `trialhead/support.html` | Trialhead's Privacy Policy URL and Support URL for App Store Connect |
| `rxcall/privacy.html`, `rxcall/support.html` | Rxcall's Privacy Policy URL and Support URL for App Store Connect |
| `style.css` | All styling, light + dark |
| `404.html` | Not-found page (GitHub Pages and Cloudflare Pages pick this up automatically) |

## Copy rules (from the project handoff)

Before editing any text, know these constraints:

1. The project is **"a free, open-source project"** — never "nonprofit," "Foundation," or "501(c)(3)" until the entity actually exists.
2. **No donation links** or payment mechanisms of any kind.
3. **Never claim no comparable app exists.** The differentiator is neutrality (free, no ads, no data collection, no interested funding), not uniqueness.
4. The clinical trial app **never asserts eligibility** — site copy must not imply it matches, scores, or qualifies anyone.

## Previewing locally

Just open `index.html` in a browser, or:

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deploying

Any static host works. The zero-cost options:

**GitHub Pages** (fits the project's existing GitHub org):
1. Push this directory to a repo (e.g. `finalstretch.org` or `website`) in the org.
2. Settings → Pages → deploy from the `main` branch, root folder.
3. Add `finalstretch.org` as the custom domain (this creates a `CNAME` file) and enable *Enforce HTTPS*.
4. At the DNS provider: `A` records for the apex pointing at GitHub Pages IPs (185.199.108.153, .109., .110., .111.) and a `CNAME` record for `www` pointing at `<org>.github.io`.

**Cloudflare Pages / Netlify:** connect the repo, no build command, output directory `/`. Both handle the apex domain and HTTPS directly.

Note: the site repo lives under the same governance as the app repos — open a PR, the other sibling reviews, no direct pushes to `main`.
