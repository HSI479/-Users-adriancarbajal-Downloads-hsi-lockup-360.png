#!/usr/bin/env node
// Headless render of the 4:19 YouTube channel art.
//   node render.mjs                  -> renders everything to ./out using the vector logo recreation
//   node render.mjs --logo "/path/419 Podcast Logo.png"   -> same, but with the real logo PNG
//   node render.mjs --guides         -> also writes banner-GUIDES.png with the safe-area overlays
// Requires: node 18+, playwright (npm i -D playwright) and a Chromium it can launch.
// Set PLAYWRIGHT_BROWSERS_PATH or CHROME_PATH if Chromium lives outside the default location.
import { chromium } from 'playwright';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const logoArg = args.includes('--logo') ? args[args.indexOf('--logo') + 1] : null;
const guides = args.includes('--guides');
const outDir = path.join(here, 'out');
fs.mkdirSync(outDir, { recursive: true });
const t = (f, qs = '') => pathToFileURL(path.join(here, 'templates', f)).href + qs;

const enc = (o) => Object.entries(o).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join('&');
const jobs = [
  { name: 'profile-800x800.png', url: t('profile.html'), w: 800, h: 800 },
  { name: 'banner-2560x1440.png', url: t('banner.html'), w: 2560, h: 1440 },
  { name: 'banner-ministry-2560x1440.png', url: t('banner-ministry.html'), w: 2560, h: 1440 },
  { name: 'podcast-cover-3000x3000.png', url: t('podcast-cover.html'), w: 3000, h: 3000 },
  { name: 'thumb-ep1-bold-courageous-A.png', url: t('thumb.html', '?' + enc({ concept: 'A', ep: 'EPISODE 1', title: 'Bold &amp; <em>Courageous</em>', sub: 'with <b>Mark Carter</b>, founder of The King’s Refuge' })), w: 1280, h: 720 },
  { name: 'thumb-ep2-six-months-later-B.png', url: t('thumb.html', '?' + enc({ concept: 'B', ep: 'EPISODE 2 · PART 1', title: 'Six Months <em>Later</em>', sub: 'Taylor, Walker &amp; Adrian on life after the <b>Hot Springs</b> men’s weekend' })), w: 1280, h: 720 },
  { name: 'thumb-ep3-six-months-later-C.png', url: t('thumb.html', '?' + enc({ concept: 'C', ep: 'EPISODE 3 · PART 2', title: 'What <em>Stuck</em>', sub: '<b>Six Months Later</b>, part 2: discipleship that lasts' })), w: 1280, h: 720 },
];
if (guides) jobs.push({ name: 'banner-GUIDES.png', url: t('banner.html', '?guides=1'), w: 2560, h: 1440 }, { name: 'banner-ministry-GUIDES.png', url: t('banner-ministry.html', '?guides=1'), w: 2560, h: 1440 });

const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined });
for (const j of jobs) {
  const page = await browser.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1 });
  if (logoArg) await page.addInitScript((src) => { window.LOGO_SRC = src; }, pathToFileURL(path.resolve(logoArg)).href);
  await page.goto(j.url);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(150);
  await page.screenshot({ path: path.join(outDir, j.name), type: 'png', fullPage: false });
  // JPEG twin for upload-size limits (banner <= 6 MB, podcast cover and thumbnails <= 2 MB)
  const jpg = j.name.replace(/\.png$/, '.jpg');
  await page.screenshot({ path: path.join(outDir, jpg), type: 'jpeg', quality: 92, fullPage: false });
  const kb = (f) => Math.round(fs.statSync(path.join(outDir, f)).size / 1024);
  console.log(`${j.name}  ${j.w}x${j.h}  png ${kb(j.name)} KB / jpg ${kb(jpg)} KB`);
  await page.close();
}
await browser.close();
