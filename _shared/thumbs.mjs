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
// Instagram story (1080x1920) for the Close Friends outreach → {slug}/assets/story.jpg
// Everything sits in one column from the top; the space below "Tap the link" stays empty for the
// user's link sticker and @mention (and above Instagram's reply bar). A console warning flags less than 300px.
const first = esc(c.name.split(' ')[0]);
const st = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await st.goto('http://127.0.0.1:8788/404.html');
await st.setContent(`<!doctype html><html><head><style>
@font-face{font-family:B;src:url(http://127.0.0.1:8788/assets/fonts/bricolage-grotesque-latin-wght-normal.woff2)}
@font-face{font-family:I;src:url(http://127.0.0.1:8788/assets/fonts/inter-latin-wght-normal.woff2)}
@font-face{font-family:M;src:url(http://127.0.0.1:8788/assets/fonts/jetbrains-mono-latin-wght-normal.woff2)}
*{box-sizing:border-box;margin:0}body{width:1080px;height:1920px;position:relative;overflow:hidden;color:#1b1917;font-family:I;
background:radial-gradient(900px 700px at 85% 0%,rgba(124,90,22,.10),transparent 70%),repeating-linear-gradient(135deg,rgba(27,25,23,.022) 0 2px,transparent 2px 12px),#f5f2ec}
.w{position:absolute;left:84px;right:84px;top:250px}
.e{font:600 26px M;letter-spacing:.22em;text-transform:uppercase;color:#7c5a16}
h1{font:700 92px/1.02 B;letter-spacing:-.025em;margin-top:34px}
h1 span{color:#7c5a16;text-decoration:underline;text-decoration-thickness:7px;text-underline-offset:12px;text-decoration-color:rgba(124,90,22,.45)}
.c{margin-top:70px;background:#fff;border-radius:28px;padding:14px;border:1px solid rgba(27,25,23,.1);box-shadow:0 40px 80px -30px rgba(27,25,23,.35)}
.bar{display:flex;align-items:center;gap:10px;padding:10px 12px 18px}.bar i{width:16px;height:16px;border-radius:50%;background:#e86a5b}
.bar i:nth-child(2){background:#e8b44b}.bar i:nth-child(3){background:#6cc36b}
.u{margin-left:14px;flex:1;background:#f1ede5;border-radius:10px;padding:10px 16px;font:21px M;color:#5f5850}
.c img{display:block;width:100%;height:auto;border-radius:16px}
.m{margin-top:40px;font-size:30px;line-height:1.4;color:#5f5850}.m b{color:#1b1917;font-weight:600}
.t{margin-top:48px;text-align:center;font:600 26px M;letter-spacing:.2em;text-transform:uppercase;color:#7c5a16}
</style></head><body><div class="w"><p class="e">Already built for ${esc(c.brandName)}</p>
<h1>${esc(h.before)} <span>${esc(h.mark)}</span>${/^[.,!?:;]/.test(h.after) ? '' : ' '}${esc(h.after)}</h1>
<div class="c"><div class="bar"><i></i><i></i><i></i><span class="u">your call funnel</span></div><img src="http://127.0.0.1:8788/${slug}/assets/previews/funnel.jpg"></div>
<p class="m"><b>${first}</b>, the page, the application, the emails and the ads are ready.</p>
<p class="t">Tap the link ↓</p></div></body></html>`, { waitUntil: 'networkidle' });
await st.evaluate(() => document.fonts.ready);
// Long headlines: shrink the h1 step by step until at least 340px stay free (down to 70px type).
const free = await st.evaluate(() => {
  const h1 = document.querySelector('h1'), room = () => 1920 - document.querySelector('.t').getBoundingClientRect().bottom;
  for (let px = 92; room() < 340 && px > 70; px -= 4) h1.style.fontSize = (px - 4) + 'px';
  return room();
});
if (free < 300) console.warn(`story.jpg: only ${Math.round(free)}px left for stickers, even at 70px type`);
else console.log(`story.jpg: ${Math.round(free)}px free for stickers`);
await st.screenshot({ path: new URL(`../${slug}/assets/story.jpg`, import.meta.url).pathname, type: 'jpeg', quality: 88 });
console.log('wrote', `${slug}/assets/story.jpg`);
// Preview for the first outreach email (1200px wide, shown at ~600px): the funnel in a browser frame on paper.
// The Gmail connector strips images from drafts, so the user drags this file into the email by hand.
const em = await b.newPage({ viewport: { width: 1200, height: 860 }, deviceScaleFactor: 1 });
await em.goto('http://127.0.0.1:8788/404.html');
await em.setContent(`<!doctype html><html><head><style>
@font-face{font-family:M;src:url(http://127.0.0.1:8788/assets/fonts/jetbrains-mono-latin-wght-normal.woff2)}
*{box-sizing:border-box;margin:0}body{width:1200px;padding:56px 64px 64px;background:repeating-linear-gradient(135deg,rgba(27,25,23,.022) 0 2px,transparent 2px 12px),#f5f2ec}
.c{background:#fff;border-radius:26px;padding:14px;border:1px solid rgba(27,25,23,.1);box-shadow:0 40px 80px -30px rgba(27,25,23,.35)}
.bar{display:flex;align-items:center;gap:10px;padding:8px 12px 16px}.bar i{width:15px;height:15px;border-radius:50%;background:#e86a5b}
.bar i:nth-child(2){background:#e8b44b}.bar i:nth-child(3){background:#6cc36b}
.u{margin-left:14px;flex:1;background:#f1ede5;border-radius:10px;padding:10px 16px;font:20px M;color:#5f5850}
.c img{display:block;width:100%;height:auto;border-radius:14px}
</style></head><body><div class="c"><div class="bar"><i></i><i></i><i></i><span class="u">your call funnel · built for ${esc(c.brandName)}</span></div>
<img src="http://127.0.0.1:8788/${slug}/assets/previews/funnel.jpg"></div></body></html>`, { waitUntil: 'networkidle' });
await em.evaluate(() => document.fonts.ready);
await em.locator('body').screenshot({ path: new URL(`../${slug}/assets/email.jpg`, import.meta.url).pathname, type: 'jpeg', quality: 80 });
console.log('wrote', `${slug}/assets/email.jpg`);
await b.close();
