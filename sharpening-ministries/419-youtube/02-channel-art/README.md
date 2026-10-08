# 4:19 Podcast — channel art pipeline

Headless HTML → PNG/JPG renders of every image YouTube asks for, in the 4:19 brand
(charcoal `#1C1B18`, antique gold `#8A6817` / `#D8B45A` on dark, bone/stone neutrals;
Rokkitt display, Libre Franklin body, Archivo labels).

| File in `out/` | Size | Where it goes in YouTube Studio |
|---|---|---|
| `profile-800x800.(png\|jpg)` | 800×800 | Customization → Branding → Picture (shown as a circle) |
| `banner-2560x1440.(png\|jpg)` | 2560×1440 | Customization → Branding → Banner image (≤ 6 MB) |
| `banner-ministry-2560x1440.(png\|jpg)` | 2560×1440 | Banner for the **Sharpening Ministries** channel (one-channel setup: "Home of the 4:19 Podcast") |
| `banner-GUIDES.png`, `banner-ministry-GUIDES.png` | 2560×1440 | Proof only: red = 1546×423 safe area, yellow = tablet, green = desktop |
| `podcast-cover-3000x3000.(png\|jpg)` | 3000×3000 | Create → New podcast → square thumbnail |
| `thumb-ep1-bold-courageous-A.(png\|jpg)` | 1280×720 | Episode 1 custom thumbnail (concept A, guest portrait) |
| `thumb-ep2-six-months-later-B.(png\|jpg)` | 1280×720 | Episode 2 custom thumbnail (concept B, statement card) |
| `thumb-ep3-six-months-later-C.(png\|jpg)` | 1280×720 | Episode 3 custom thumbnail (concept C, group band) |

Everything in the banner that must survive cropping lives inside the centered 1546×423
safe area; the gold rules and net lines outside it are decorative and may crop.

## The logo in these renders is a vector recreation

The original medallion PNGs live only in Adrian's iCloud folder
(`~/Library/Mobile Documents/com~apple~CloudDocs/Sharpening/Podcast 419/`). `templates/logo.js`
holds an SVG recreation (gold medallion, mic, cast net, "4:19", PODCAST, Sharpening shield) so the
layouts could be built and proofed. **Before uploading, re-render with the real artwork:**

```bash
cd sharpening-ministries/419-youtube/02-channel-art
npm i -D playwright            # once; uses the Chromium Playwright ships with
node render.mjs --logo "$HOME/Library/Mobile Documents/com~apple~CloudDocs/Sharpening/Podcast 419/419 Poscast Logo Shiney.png" --guides
```

If Chromium must run outside a sandbox (as in `419-logo/v2/tools/`), point `CHROME_PATH` at the
binary; the script passes it to Playwright's `executablePath`.

## Thumbnails with real photos

`templates/thumb.html` takes query parameters: `concept` (A, B, C), `ep`, `title` (HTML; wrap the
gold word in `<em>`), `sub` (HTML; `<b>` for bone-colored words) and `photo` (a `file://` URL to a
cut-out portrait on a dark background, ≥ 600×720). Edit the `jobs` array in `render.mjs` or add a
job per episode. Keep titles to 2–4 words; the frame is read at 168 px wide on phones.
