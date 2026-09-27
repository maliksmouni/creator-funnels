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
// Link-preview card (1200x630) in the pitch master style → {slug}/assets/og.jpg
const { readFileSync } = await import('node:fs');
const c = JSON.parse(readFileSync(new URL(`../${slug}/content.json`, import.meta.url)));
const h = c.pitch.headline, esc = s => s.replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
const thumb = c.video ? `http://127.0.0.1:8788/${slug}/${c.video.thumb}` : `http://127.0.0.1:8788/${slug}/${c.image}`;
const og = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
await og.goto('http://127.0.0.1:8788/404.html'); // same origin, so the self-hosted fonts load
await og.setContent(`<!doctype html><html><head><style>
@font-face{font-family:B;src:url(http://127.0.0.1:8788/assets/fonts/bricolage-grotesque-latin-wght-normal.woff2)}
@font-face{font-family:M;src:url(http://127.0.0.1:8788/assets/fonts/jetbrains-mono-latin-wght-normal.woff2)}
*{box-sizing:border-box;margin:0}body{width:1200px;height:630px;display:grid;grid-template-columns:1fr 520px;gap:48px;align-items:center;padding:64px;
background:radial-gradient(60% 60% at 100% 0%,rgba(124,90,22,.14),transparent 60%),repeating-linear-gradient(115deg,rgba(27,25,23,.02) 0 1px,transparent 1px 9px),linear-gradient(115deg,#f5f2ec,#ece7dd);color:#1b1917}
p{font:500 17px M;letter-spacing:.24em;text-transform:uppercase;color:#7c5a16;margin-bottom:24px}
h1{font:700 60px/1.02 B;letter-spacing:-.035em}h1 span{color:#7c5a16;text-decoration:underline;text-decoration-thickness:.07em;text-underline-offset:.12em}
.v{position:relative;border-radius:22px;overflow:hidden;box-shadow:0 40px 80px -40px rgba(27,25,23,.6);aspect-ratio:16/9}
.v img{width:100%;height:100%;object-fit:cover;display:block}.v i{position:absolute;inset:0;margin:auto;width:84px;height:84px;border-radius:50%;background:#7c5a16;box-shadow:0 0 0 12px rgba(124,90,22,.25)}
.v i:after{content:"";position:absolute;left:34px;top:26px;border-left:24px solid #fbf8f1;border-top:16px solid transparent;border-bottom:16px solid transparent}
</style></head><body><div><p>Already built for ${esc(c.brandName)}</p><h1>${esc(h.before)} <span>${esc(h.mark)}</span>${/^[.,!?:;]/.test(h.after) ? '' : ' '}${esc(h.after)}</h1></div>
<div class="v"><img src="${thumb}"><i></i></div></body></html>`, { waitUntil: 'networkidle' });
await og.evaluate(() => document.fonts.ready);
await og.screenshot({ path: new URL(`../${slug}/assets/og.jpg`, import.meta.url).pathname, type: 'jpeg', quality: 82 });
console.log('wrote', `${slug}/assets/og.jpg`);
await b.close();
