# Studio site

English portfolio / services website for the studio. Static HTML + CSS + ~60 lines of JS, no framework, no backend.

- **Source:** `src/` (edit here)
- **Built site:** `docs/` (generated — GitHub Pages serves this folder; don't edit by hand)
- **Settings:** `site.config.json` — the one place for name, email, Telegram, domain

## Change studio name, email, Telegram, domain

Edit `site.config.json`:

| Key | What it is | Example |
|---|---|---|
| `STUDIO_NAME` | Name in header, footer, page title, OG image | `"Acme Studio"` |
| `TAGLINE` | Short line in the footer | `"Websites, automation & AI agents"` |
| `EMAIL` | Contact email (mailto links + contact form) | `"hello@acme.com"` |
| `TELEGRAM_HANDLE` | Telegram username, without `@` | `"acme_studio"` |
| `BOOKING_URL` | Where "Book a free 20-min call" goes. `#contact` = scroll to the form; or a Calendly/Cal.com link | `"https://cal.com/acme/20min"` |
| `SITE_URL` | Full site address, no trailing slash (used for canonical, OpenGraph, sitemap) | `"https://acme.com"` |
| `TIMEZONE` | Shown in FAQ and contact hours | `"UTC+3"` |

Then rebuild and push:

```bash
python tools/make_og.py   # only if STUDIO_NAME changed — re-renders the social preview image (needs Chrome + Pillow)
python build.py           # src/ -> docs/ with values filled in
git add -A && git commit -m "chore: update site config" && git push
```

GitHub Pages republishes automatically within ~1 minute.

## Connect the .com domain

1. Set `SITE_URL` to `https://yourdomain.com` and run `python build.py` — this writes `docs/CNAME`.
2. At the domain registrar, add DNS records:
   - `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` for `www` → `sergpt911.github.io`
3. Push. In GitHub → repo **Settings → Pages**, confirm the custom domain and tick **Enforce HTTPS** once the certificate is issued (can take up to an hour).

## Deploy (how it is set up)

- Repo: `SERGPT911/studio-site` (public — required for Pages on the free plan)
- Pages source: branch `main`, folder `/docs`
- No CI needed: the built files are committed.

## Content notes

- Case studies describe real, shipped work only. Screenshots: StashMap landing (besporyadka.net) and the app's own App Store screenshots; Ozon perfume cards from the actual store. The AgentDeck visual is an illustrative CSS mockup and is labelled as such.
- Prices are "from" prices; adjust in `src/index.html` (Services section).
- Business terms stated on the site that the owner should confirm: 50% upfront / 50% on delivery, 30 days of bug fixes after launch, reply within one business day, hours Mon–Fri 9:00–19:00.

## Files

```
site.config.json   settings (edit this)
build.py           builds docs/ from src/
tools/make_og.py   renders src/img/og.jpg (1200x630) from tools/og.html
src/index.html     page content
src/styles.css     styles
src/main.js        menu, scroll reveal, mailto form
src/img/           optimised WebP images (each < 200 KB)
src/fonts/         self-hosted Inter Tight + Instrument Serif (latin subset)
```
