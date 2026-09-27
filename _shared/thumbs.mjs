// Render preview thumbnails for the pitch page's deliverable cards.
// Usage: serve the repo root on :8788, then `node _shared/thumbs.mjs <slug>`.
// Needs Playwright; set PW=/path/to/node_modules/playwright/index.mjs if it isn't resolvable here.
import { mkdirSync } from 'node:fs';
const { chromium } = await import(process.env.PW || 'playwright');
const slug = process.argv[2];
const base = `http://127.0.0.1:8788/${slug}/`;
const shots = { funnel: 'funnel/', 'thank-you': 'funnel/thank-you/', ads: 'ads/', emails: 'emails/' };
const out = new URL(`../${slug}/assets/previews/`, import.meta.url).pathname;
mkdirSync(out, { recursive: true });
const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
const p = await b.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1, reducedMotion: 'reduce' });
for (const [name, path] of Object.entries(shots)) {
  await p.goto(base + path, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: '.demo{display:none!important}' });
  await p.waitForTimeout(300);
  await p.screenshot({ path: `${out}${name}.jpg`, type: 'jpeg', quality: 78 });
  console.log('wrote', `${slug}/assets/previews/${name}.jpg`);
}
await b.close();
