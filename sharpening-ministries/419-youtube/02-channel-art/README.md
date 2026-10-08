# 4:19 Podcast — channel art pipeline

Headless HTML → PNG/JPG renders of every image YouTube asks for, in the 4:19 brand
(charcoal `#1C1B18`, antique gold `#8A6817` / `#D8B45A` on dark, bone/stone neutrals;
Rokkitt display, Libre Franklin body, Archivo labels).

| File in `out/` | Size | Where it goes in YouTube Studio |
|---|---|---|
| `profile-800x800.(png\|jpg)` | 800×800 | The real rope ring on canvas; profile picture for a 4:19 channel (the ministry channel uses the shield) |
| `banner-2560x1440.(png\|jpg)` | 2560×1440 | Customization → Branding → Banner image (≤ 6 MB) |
| `banner-ministry-2560x1440.(png\|jpg)` | 2560×1440 | Banner for the **Sharpening Ministries** channel, charcoal/gold palette, "Home of the 4:19 Podcast" |
| `banner-ministry-canvas-2560x1440.(png\|jpg)` | 2560×1440 | Same banner in the logo's own palette (canvas, rope, navy, gunmetal). Pick one. |
| `banner-GUIDES.png`, `banner-ministry-GUIDES.png` | 2560×1440 | Proof only: red = 1546×423 safe area, yellow = tablet, green = desktop |
| `podcast-cover-2000x2000.(png\|jpg)` | 2000×2000 | Square crop of the real logo (ring + net) for Create → New podcast → thumbnail |
| `thumb-ep1-bold-courageous-A.(png\|jpg)` | 1280×720 | Episode 1 custom thumbnail (concept A, guest portrait) |
| `thumb-ep2-six-months-later-B.(png\|jpg)` | 1280×720 | Episode 2 custom thumbnail (concept B, statement card) |
| `thumb-ep3-six-months-later-C.(png\|jpg)` | 1280×720 | Episode 3 custom thumbnail (concept C, group band) |

Everything in the banner that must survive cropping lives inside the centered 1546×423
safe area; the gold rules and net lines outside it are decorative and may crop.

## The real logo

`assets/419-podcast-logo.png` is the real 4:19 Podcast logo (1672×940: rope ring with navy accent,
cast net, gunmetal "4:19 PODCAST", "SHARPENING MINISTRIES"; canvas background). `prep-logo.py` cuts
the ring out as `assets/419-logo-circle.png` and writes the profile image and the square podcast
cover directly from the source pixels. `render.mjs` uses the ring automatically for every badge.
The SVG in `templates/logo.js` is only a fallback (`--vector`).

```bash
cd sharpening-ministries/419-youtube/02-channel-art
npm i -D playwright            # once; uses the Chromium Playwright ships with
python3 prep-logo.py           # ring cut-out, profile, podcast cover
node render.mjs --guides       # banners and thumbnails
```

The source is 1672 px wide, so the 2000×2000 cover is a mild upscale. If a larger or square export
of the logo exists, drop it in as `assets/419-podcast-logo.png` and re-run; nothing else changes.

If Chromium must run outside a sandbox (as in `419-logo/v2/tools/`), point `CHROME_PATH` at the
binary; the script passes it to Playwright's `executablePath`.

## Thumbnails with real photos

`templates/thumb.html` takes query parameters: `concept` (A, B, C), `ep`, `title` (HTML; wrap the
gold word in `<em>`), `sub` (HTML; `<b>` for bone-colored words) and `photo` (a `file://` URL to a
cut-out portrait on a dark background, ≥ 600×720). Edit the `jobs` array in `render.mjs` or add a
job per episode. Keep titles to 2–4 words; the frame is read at 168 px wide on phones.
