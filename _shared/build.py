#!/usr/bin/env python3
"""Render a creator folder from its content.json.

Usage: python3 _shared/build.py <slug>
       node _shared/thumbs.mjs <slug>   (afterwards, refreshes the preview images)

Layout and section order are fixed here; only content.json changes per creator.
The pitch page always uses pitch-master.css (HOUSE.md design master); the
creator funnel uses creator-funnel.css with the creator's brand tokens.
Also writes the site-wide _redirects that keeps internal notes off the web.
"""
import html
import json
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "_shared"
FLAG = re.compile(r"(\[CONFIRM[^\]]*\]|\{\{SWAP\}\}[^<\n]*)")
# Files that stay in the repo but must never be served.
PRIVATE_PER_CREATOR = ["dossier.md", "offer-deck-filled.md", "README.md", "content.json"]
PRIVATE_SITE = ["/HOUSE.md", "/README.md", "/CLAUDE.md", "/_shared/*", "/.claude/*", "/functions/*", "/wrangler.jsonc", "/netlify.toml"]

ARROW = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M4 2l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
DOWN = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4l14 8-14 8z"/></svg>'
REVEAL_JS = """<script>
document.documentElement.classList.add('js');
addEventListener('DOMContentLoaded',()=>{const els=document.querySelectorAll('.reveal');
if(!('IntersectionObserver' in window)){els.forEach(e=>e.classList.add('in'));return}
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -8% 0px'});
els.forEach(e=>io.observe(e))});
</script>"""


def t(s):
    """Escape text and render open [CONFIRM] / {{SWAP}} markers as visible chips."""
    return FLAG.sub(r'<span class="flag">\1</span>', html.escape(s))


def a(s):
    return html.escape(s, quote=True)


def host(c):
    """Where a creator is served: "cloudflare" (default, via publish.py) or "netlify" (older creators, repo root)."""
    return c.get("host", "cloudflare")


def page(title, css, body, extra_head="", lang="en"):
    return f"""<!doctype html>
<html lang="{a(lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{html.escape(title)}</title>
<style>{css}</style>
{REVEAL_JS}
{extra_head}</head>
<body>
{body}
</body>
</html>
"""


def favicon(c, bg, fg):
    """Inline SVG favicon: rounded square with the brand's first letter (no extra file to publish)."""
    letter = html.escape(next((ch for ch in c["brandName"] if ch.isalnum()), "·").upper())
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{bg}"/>'
           f'<text x="32" y="45" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="38" font-weight="700" fill="{fg}">{letter}</text></svg>')
    return f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{urllib.parse.quote(svg)}">\n'


def funnel_favicon(c):
    return favicon(c, c["brand"]["accent"], c["brand"]["accent-ink"])


def vsl_thumb(c, prefix=""):
    """Latest YouTube upload thumbnail as the video placeholder (see _shared/yt_thumb.py)."""
    v = c.get("video")
    return f'<img class="vsl__img" src="{prefix}{a(v["thumb"])}" alt="" width="1280" height="720">' if v else ""


# ---------- pitch page (master design, identical for every creator) ----------

def beat(n, b):
    aside = ""
    if b.get("stats"):
        aside += "".join(f'<div class="aside__stat"><strong>{t(s["value"])}</strong><span>{t(s["label"])}</span></div>' for s in b["stats"])
    if b.get("quote"):
        aside += f"<blockquote>{t(b['quote'])}</blockquote>"
    if b.get("source"):
        aside += f'<p class="aside__src">{t(b["source"])}</p>'
    return f"""<article class="beat reveal">
  <span class="beat__idx">{n:02d}</span>
  <div><p class="beat__kicker">{t(b["kicker"])}</p><h3 class="beat__title">{t(b["title"])}</h3><p class="beat__text">{t(b["text"])}</p></div>
  <aside class="aside">{aside}</aside>
</article>"""


def pcard(i):
    return f"""<a class="pcard reveal" href="{a(i["href"])}">
  <div class="thumb"><div class="thumb__bar"><i></i><i></i><i></i><span class="thumb__url">{t(i["url"])}</span></div><img src="{a(i["thumb"])}" alt="" loading="lazy" width="1280" height="800"></div>
  <div class="pcard__body"><span class="pcard__kicker">{t(i["kicker"])}</span><span class="pcard__title">{t(i["title"])}</span><span class="pcard__desc">{t(i["desc"])}</span><span class="pcard__link">Open preview {ARROW}</span></div>
</a>"""


def og_tags(c):
    """Link preview (WhatsApp, iMessage, LinkedIn, email): title, line and the og.jpg card from thumbs.mjs."""
    site = json.loads((SHARED / "site.json").read_text())[host(c)].rstrip("/")
    h = c["pitch"]["headline"]
    line = f'{h["before"]} {h["mark"]}{"" if h["after"][:1] in ".,!?:;" else " "}{h["after"]}'.strip()
    url, img = f'{site}/{c["slug"]}/', f'{site}/{c["slug"]}/assets/og.jpg'
    title = f'Built for {c["brandName"]}'
    return "".join(f'<meta {k}="{a(n)}" content="{a(v)}">\n' for k, n, v in [
        ("property", "og:type", "website"), ("property", "og:url", url), ("property", "og:title", title),
        ("property", "og:description", line), ("property", "og:image", img),
        ("property", "og:image:width", "1200"), ("property", "og:image:height", "630"),
        ("name", "twitter:card", "summary_large_image"), ("name", "twitter:title", title),
        ("name", "twitter:description", line), ("name", "twitter:image", img), ("name", "description", line)])


def case_card(x):
    pos = f' style="object-position:{a(x["focus"])}"' if x.get("focus") else ""
    img = f'<div class="case__img"><img src="{a(x["image"])}" alt="" loading="lazy"{pos}></div>' if x.get("image") else ""
    return (f'<div class="case reveal">{img}<div class="case__body"><span class="case__metric">{t(x["metric"])}</span>'
            f'<p class="case__name">{t(x["name"])}</p><p class="case__text">{t(x["text"])}</p></div></div>')


def build_pitch(c, house_cases):
    p = c["pitch"]
    h = p["headline"]
    br = p["bridge"]
    groups = "".join(
        f"""<div class="group"><div class="group__head reveal"><div><span class="group__label">{t(g["label"])}</span><span class="group__count">{len(g["items"]):02d}</span></div></div>
<div class="cards{' cards--wide' if len(g['items']) == 1 else ''}">{''.join(pcard(i) for i in g["items"])}</div></div>"""
        for g in p["groups"]
    )
    cases = house_cases or []
    if cases:
        case_html = "".join(
            case_card(x)
            for x in cases
        )
    else:
        case_html = "".join(
            f'<div class="case case--empty reveal"><span class="flag">{{{{SWAP}}}} Case study {n} from HOUSE.md</span></div>' for n in (1, 2)
        )
    cal = a(p["cta"]["calendly"])
    body = f"""
<header class="topbar"><span>{t(c["brandName"])}</span></header>
<main>
<section class="hero"><div class="container">
  <p class="eyebrow reveal">{t(p["eyebrow"])}</p>
  <h1 class="display h-xl reveal">{t(h["before"])} <span class="mark">{t(h["mark"])}</span>{"" if h["after"][:1] in ".,!?:;" else " "}{t(h["after"])}</h1>
  <div class="vsl reveal" role="img" aria-label="Video walkthrough placeholder">{vsl_thumb(c)}<div class="vsl__play">{PLAY}</div></div>
</div></section>

<section class="section" id="bridge"><div class="container">
  <div class="bridge__head"><h2 class="display h-lg reveal">{t(br["title"])}</h2></div>
  <div class="beats">{''.join(beat(n, b) for n, b in enumerate(br["beats"], 1))}</div>
  <div class="bridge__close reveal"><p class="bridge__closing">{t(br["closing"])}</p></div>
</div></section>

<section class="section" id="deliverables"><div class="container">
  <div class="deliv__head"><h2 class="display h-lg reveal">{t(p["deliverablesTitle"])}</h2></div>
  {groups}
</div></section>

<section class="section"><div class="container">
  <h2 class="display h-lg reveal" style="text-align:center">{t(p["cases"]["title"])}</h2>
  <div class="cases">{case_html}</div>
</div></section>

<section class="section cta" id="cta"><div class="container">
  <h2 class="display h-lg reveal">{t(p["cta"]["title"])}</h2>
  <div class="cal reveal"><div class="calendly-inline-widget" data-url="{cal}?hide_gdpr_banner=1&amp;background_color=ffffff&amp;primary_color=7c5a16"></div></div>
</div></section>
</main>
<a class="sticky" href="#cta">Book a call</a>
<footer class="footer"><span>{t(p["footer"])}</span></footer>
"""
    head = og_tags(c) + '<script src="https://assets.calendly.com/assets/external/widget.js" async></script>\n'
    return page(f'{c["brandName"]}', (SHARED / "pitch-master.css").read_text(), body, favicon(c, "#7c5a16", "#f5f2ec") + head)


# ---------- creator funnel (creator brand) ----------

# Fixed labels of the funnel, thank-you, email and ad pages. A creator whose audience speaks
# another language overrides any of them in content.json → ui (plus ui.lang for <html lang>).
UI = {
    "lang": "en",
    "funnelTitle": "Mentorship",
    "problemEyebrow": "The problem",
    "methodEyebrow": "The method",
    "offerEyebrow": "The mentorship",
    "proofEyebrow": "Proof",
    "processEyebrow": "The process",
    "applyEyebrow": "Application",
    "applyLead": "Six questions, about two minutes.",
    "detailsLegend": "Your details",
    "bookedTitle": "Booked",
    "tyEyebrow": "Application received",
    "tyTitle": "Last step: pick your call time.",
    "tyLead": "If your application is a fit, book a slot below. You'll get a confirmation email right away.",
    "tyCalendarNote": "Booking calendar",
    "tyStepsEyebrow": "Before the call",
    "tyStepsTitle": "Three things to do now",
    "tySteps": [
        {"title": "Check your inbox", "body": "A confirmation plus a few short emails so the call is useful."},
        {"title": "Prepare your last 10–20 trades", "body": "Journal, screenshots or a broker statement are all fine."},
        {"title": "Only trust official links", "body": "We never ask for payment via Telegram DM or WhatsApp."}],
    "tyBack": "← Back to the page",
    "emailsTitle": "Pre-call emails",
    "emailsEyebrow": "Email sequence · booked to call",
    "emailsHeading": "The pre-call sequence",
    "emailsLead": "{n} emails from booking to the morning of the call. Placeholders like {tag} are filled by the email tool.",
    "emailLabel": "Email",
    "adsTitle": "Ad scripts",
    "adsEyebrow": "Ad creatives · video",
    "adsHeading": "Ad creative scripts",
    "adsLead": "{n} angles for retargeting. Rule for every ad: no return or profit claims, no trade calls, and a risk notice on screen.",
    "adLabel": "Angle",
}


def ui(c, key):
    return c.get("ui", {}).get(key, UI[key])


def brand_css(c):
    tokens = ";".join(f"--{k}:{v}" for k, v in c["brand"].items() if not k.startswith("_"))
    return f":root{{{tokens}}}\n" + (SHARED / "creator-funnel.css").read_text()


def logo(c):
    parts = c["brandName"].split(" ", 1)
    return f'<span class="logo">{t(parts[0])}{" <b>" + t(parts[1]) + "</b>" if len(parts) > 1 else ""}</span>'


def funnel_shell(c, inner, cta_href=None):
    s = c["sections"]
    cta = f'<a class="btn sm" href="{cta_href}">{t(s["hero"].get("navCta", s["hero"]["cta"]))}</a>' if cta_href else ""
    return f"""<div class="demo">{t(c["demoBanner"])}</div>
<header class="top"><div class="wrap">{logo(c)}{cta}</div></header>
<main>{inner}</main>
<footer><div class="wrap">{t(s["finalCta"]["disclaimer"])}</div></footer>"""


def numbered(items):
    return "".join(
        f'<div class="card reveal"><span class="num">{n:02d}</span><h3>{t(i["title"])}</h3><p>{t(i["body"])}</p></div>'
        for n, i in enumerate(items, 1)
    )


def steps(items):
    return "".join(
        f'<li class="reveal"><span class="n">{n}</span><div><h3>{t(x["title"])}</h3><p>{t(x["body"])}</p></div></li>'
        for n, x in enumerate(items, 1)
    )


def build_funnel(c):
    s = c["sections"]
    h = s["hero"]
    chips = "".join(f"<li>{t(x)}</li>" for x in h.get("chips", []))
    pillars = "".join(
        f'<div class="pillar reveal"><span>{n:02d}</span><h3>{t(p["title"])}</h3><p>{t(p["body"])}</p></div>'
        for n, p in enumerate(s["mechanism"]["pillars"], 1)
    )
    proof = "".join(f'<div class="proof-slot reveal">{t(i)}</div>' for i in s["proof"]["items"])
    qs = []
    for i, q in enumerate(s["qualification"]["questions"], 1):
        name = f"q{i}"
        if q["type"] == "text":
            field = f'<textarea name="{name}" rows="3" required></textarea>'
        else:
            kind = "checkbox" if q["type"] == "multi" else "radio"
            req = "" if kind == "checkbox" else " required"
            field = '<div class="opts">' + "".join(
                f'<label class="opt"><input type="{kind}" name="{name}" value="{a(o)}"{req}{" data-disqualify" if o in q.get("disqualify", []) else ""}> {html.escape(o)}</label>' for o in q["options"]
            ) + "</div>"
        qs.append(f'<fieldset class="reveal"><legend><span>{i}</span>{t(q["q"])}</legend>{field}</fieldset>')
    contact = "".join(
        f'<label class="field">{html.escape(f)}<input name="{a(f.lower().split()[0])}" required></label>'
        for f in s["qualification"]["contactFields"]
    )
    inner = f"""
<section class="hero"><div class="wrap">
  <div class="hero-grid">
    <div>
      <span class="eyebrow reveal">{t(h["eyebrow"])}</span>
      <h1 class="reveal">{t(c["headline"])}</h1>
      <p class="lead reveal">{t(c["subheadline"])}</p>
      <ul class="chips reveal">{chips}</ul>
      <a class="btn reveal" href="#apply">{t(h["cta"])} {ARROW}</a>
    </div>
    <figure class="portrait reveal"><img src="../{a(c["image"])}" alt="{a(c["name"])}" width="600" height="600"></figure>
  </div>
  <div class="vsl reveal" role="img" aria-label="Video placeholder">{vsl_thumb(c, "../")}<div class="vsl__play">{PLAY}</div><p class="vsl__note">{t(h["vslNote"])}</p></div>
</div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow reveal">{t(ui(c, "problemEyebrow"))}</span><h2 class="reveal">{t(s["problem"]["title"])}</h2></div><div class="grid3">{numbered(s["problem"]["cards"])}</div></div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow reveal">{t(ui(c, "methodEyebrow"))}</span><h2 class="reveal">{t(s["mechanism"]["title"])}</h2><p class="lead reveal">{t(s["mechanism"]["body"])}</p></div><div class="pillars">{pillars}</div></div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow reveal">{t(ui(c, "offerEyebrow"))}</span><h2 class="reveal">{t(s["deliverables"]["title"])}</h2></div><div class="grid3">{numbered(s["deliverables"]["items"])}</div></div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow reveal">{t(ui(c, "proofEyebrow"))}</span><h2 class="reveal">{t(s["proof"]["title"])}</h2></div><div class="proof-grid">{proof}</div><p class="note">{t(s["proof"]["note"])}</p></div></section>
<section><div class="wrap narrow"><div class="sec-head"><span class="eyebrow reveal">{t(ui(c, "processEyebrow"))}</span><h2 class="reveal">{t(s["howItWorks"]["title"])}</h2></div><ol class="steps">{steps(s["howItWorks"]["steps"])}</ol></div></section>
<section id="apply"><div class="wrap narrow">
  <div class="sec-head"><span class="eyebrow reveal">{t(ui(c, "applyEyebrow"))}</span><h2 class="reveal">{t(s["qualification"]["title"])}</h2><p class="lead reveal">{t(ui(c, "applyLead"))}</p></div>
  <form class="apply" id="apply-form" action="thank-you/" method="get">
    {''.join(qs)}
    <fieldset class="reveal"><legend><span>✓</span>{t(ui(c, "detailsLegend"))}</legend>{contact}</fieldset>
    <div><button class="btn" type="submit">{t(s["finalCta"]["cta"])} {ARROW}</button></div>
  </form>
  <div class="card notfit" id="not-fit" hidden><h3>{t(s["qualification"]["notFit"]["title"])}</h3><p>{t(s["qualification"]["notFit"]["body"])}</p></div>
  <script>
  document.getElementById('apply-form').addEventListener('submit',e=>{{
    if(!e.target.querySelector('input[data-disqualify]:checked'))return;
    e.preventDefault();e.target.hidden=true;const n=document.getElementById('not-fit');n.hidden=false;n.scrollIntoView({{behavior:'smooth',block:'center'}});
  }});
  </script>
</div></section>
<section class="final"><div class="wrap narrow"><h2 class="reveal">{t(s["finalCta"]["title"])}</h2><p class="lead reveal">{t(s["finalCta"]["body"])}</p><a class="btn reveal" href="#apply">{t(s["finalCta"]["cta"])} {ARROW}</a></div></section>
"""
    return page(f'{c["brandName"]}: {ui(c, "funnelTitle")}', brand_css(c), funnel_shell(c, inner, "#apply"), funnel_favicon(c), lang=ui(c, "lang"))


def build_thankyou(c):
    inner = f"""
<section class="hero"><div class="wrap narrow">
  <span class="eyebrow reveal">{t(ui(c, "tyEyebrow"))}</span>
  <h1 class="reveal">{t(ui(c, "tyTitle"))}</h1>
  <p class="lead reveal">{t(ui(c, "tyLead"))}</p>
  <div class="vsl reveal" role="img" aria-label="Calendar placeholder"><div class="vsl__play">{PLAY}</div><p class="vsl__note">{t(c.get("thankYouCalendarNote", ui(c, "tyCalendarNote")))}</p></div>
</div></section>
<section><div class="wrap narrow"><div class="sec-head"><span class="eyebrow reveal">{t(ui(c, "tyStepsEyebrow"))}</span><h2 class="reveal">{t(ui(c, "tyStepsTitle"))}</h2></div>
  <ol class="steps">{steps(ui(c, "tySteps"))}</ol>
  <p class="note"><a href="../">{t(ui(c, "tyBack"))}</a></p>
</div></section>"""
    return page(f'{c["brandName"]}: {ui(c, "bookedTitle")}', brand_css(c), funnel_shell(c, inner), funnel_favicon(c), lang=ui(c, "lang"))


MERGE_TAG = re.compile(r"(\{\{[a-z_]+\}\})")


def tags(s):
    return MERGE_TAG.sub(r"<code>\1</code>", t(s))


def build_emails(c):
    mails = "".join(
        f"""<article class="mail reveal"><div class="mail__head"><span class="mail__type">{t(ui(c, "emailLabel"))} {e["emailNumber"]} · {t(e["type"])}</span><span class="mail__subj">{t(e["subject"])}</span><span class="mail__prev">{t(e["previewText"])}</span></div>
<div class="mail__body">{tags(e["body"])}</div></article>"""
        for e in c["preCallEmails"]
    )
    lead = t(ui(c, "emailsLead")).replace("{n}", str(len(c["preCallEmails"]))).replace("{tag}", "<code>{{first_name}}</code>")
    inner = f"""<section class="hero"><div class="wrap narrow"><span class="eyebrow reveal">{t(ui(c, "emailsEyebrow"))}</span><h1 class="reveal">{t(ui(c, "emailsHeading"))}</h1>
<p class="lead reveal">{lead}</p><div class="doc">{mails}</div></div></section>"""
    return page(f'{c["brandName"]}: {ui(c, "emailsTitle")}', brand_css(c), funnel_shell(c, inner), funnel_favicon(c), lang=ui(c, "lang"))


def build_ads(c):
    ads = "".join(
        f"""<article class="mail reveal"><div class="mail__head"><span class="mail__type">{t(ui(c, "adLabel"))} {n:02d} · {t(x["angle"])}</span><span class="mail__subj">“{t(x["hook"])}”</span></div>
<div class="mail__body">{t(x["script"])}</div></article>"""
        for n, x in enumerate(c["adScripts"], 1)
    )
    lead = t(ui(c, "adsLead")).replace("{n}", str(len(c["adScripts"])))
    inner = f"""<section class="hero"><div class="wrap narrow"><span class="eyebrow reveal">{t(ui(c, "adsEyebrow"))}</span><h1 class="reveal">{t(ui(c, "adsHeading"))}</h1>
<p class="lead reveal">{lead}</p><div class="doc">{ads}</div></div></section>"""
    return page(f'{c["brandName"]}: {ui(c, "adsTitle")}', brand_css(c), funnel_shell(c, inner), funnel_favicon(c), lang=ui(c, "lang"))


def house_cases():
    """Case studies from HOUSE.md. Each entry is "N. Kunde: …" followed by indented "Key: value" lines;
    entries with [placeholders] are skipped. Card = Kennzahl (metric), Kunde · Angebot, Text, Beweis image."""
    txt = (ROOT / "HOUSE.md").read_text()
    out = []
    for block in re.split(r"\n(?=\d+\. Kunde:)", txt):
        m = re.match(r"\d+\. Kunde: (.+)", block)
        if not m:
            continue
        f = {"Kunde": m.group(1).strip()}
        f.update({k: v.strip() for k, v in re.findall(r"\n\s+([A-Za-zäöüÄÖÜß]+): (.+)", block)})
        if any("[" in f.get(k, "") for k in ("Kunde", "Ergebnis")):
            continue
        img = f.get("Beweis", "").split(" ")[0]
        who = f["Kunde"].replace(" (Name nicht öffentlich)", "")
        who = {"Kunde": "Client", "Creator": "Creator"}.get(who, who)
        out.append({
            "metric": f.get("Kennzahl") or f"{f.get('Ergebnis', '')} {f.get('Zeitraum', '')}".strip(),
            "name": f"{who} · {CASE_OFFER.get(f.get('Angebot', ''), f.get('Angebot', ''))}".strip(" ·"),
            "text": f.get("Text", ""),
            "image": "/" + img if img.startswith("assets/") else "",
            "focus": f.get("Bildausschnitt", ""),
        })
    return out


CASE_OFFER = {"Neues Info-Produkt": "new info product", "Neues High-Ticket-Angebot": "new high-ticket offer", "Launch": "offer launch"}


def write_redirects():
    lines = ["# Generated by _shared/build.py for Netlify: internal notes stay in the repo but are never served;",
             "# creators hosted on Cloudflare Pages (content.json → host) are blocked here too."]
    lines += [f"{p}  /404.html  404!" for p in PRIVATE_SITE]
    for cj in sorted(ROOT.glob("*/content.json")):
        slug = cj.parent.name
        lines += [f"/{slug}/{f}  /404.html  404!" for f in PRIVATE_PER_CREATOR]
        c = json.loads(cj.read_text())
        if c.get("status") == "draft" or host(c) != "netlify":
            # drafts: pushed but not public until "deploy it"; Cloudflare creators: served only there
            lines += [f"/{slug}  /404.html  404!", f"/{slug}/*  /404.html  404!"]
    (ROOT / "_redirects").write_text("\n".join(lines) + "\n")


GUARD_JS = """// Generated by _shared/build.py: Cloudflare Pages guard. Serves only live Cloudflare creators
// (minus their notes) plus shared assets, whatever the dashboard build settings are, so the
// research notes, content.json and repo files are never public even if the repo root is deployed.
//
// Visit alerts: when a real person opens a pitch page or one of its deliverables, a push goes to
// ntfy (https://ntfy.sh). The topic is a secret set in Cloudflare (Pages → Settings → Variables and
// Secrets → NTFY_TOPIC), never in this public repo; without it nothing is sent. Link-preview bots,
// prefetches and the owner's own devices (opened once with ?me=1, which sets a cookie) are skipped.
const ALLOW = __ALLOW__;
const PRIVATE = new Set(__PRIVATE__);
const CREATORS = __CREATORS__;
const PAGES = { "": "pitch page", "funnel/": "funnel page", "funnel/thank-you/": "booking page", "emails/": "email sequence", "ads/": "ad scripts" };
const BOTS = /bot|crawl|spider|slurp|preview|facebookexternalhit|facebot|whatsapp|telegram|slack|discord|skype|linkedin|pinterest|embedly|quora|vkshare|google(?:-|image|other|web)|feedfetcher|mediapartners|headless|playwright|puppeteer|lighthouse|pingdom|uptime|monitor|curl|wget|python|node-fetch|undici|axios|go-http|java\\/|okhttp|http-client|scrapy|cloudflare/i;

export async function onRequest(ctx) {
  let url, path;
  try { url = new URL(ctx.request.url); path = decodeURIComponent(url.pathname); } catch { return notFound(ctx); }
  const parts = path.split("/");
  const allowed = path === "/404" || path === "/404.html" || ALLOW.some(a => path === a.slice(0, -1) || path.startsWith(a));
  if (!allowed || PRIVATE.has(parts[parts.length - 1]) || parts.some(x => x.startsWith(".") || x.startsWith("_"))) return notFound(ctx);
  const res = await ctx.next();
  if (url.searchParams.get("me") === "1") {
    const r = new Response(res.body, res);
    r.headers.append("set-cookie", "io_me=1; Path=/; Max-Age=31536000; Secure; SameSite=Lax");
    return r;
  }
  try { maybeNotify(ctx, url, path, res.status); } catch (e) {}
  return res;
}

function maybeNotify(ctx, url, path, status) {
  const topic = ctx.env && ctx.env.NTFY_TOPIC;
  if (!topic || status !== 200 || ctx.request.method !== "GET") return;
  const m = path.match(/^\\/([a-z0-9-]+)\\/(.*)$/);
  if (!m || !CREATORS[m[1]] || !(m[2] in PAGES)) return;
  const h = ctx.request.headers, ua = h.get("user-agent") || "";
  if (!ua || BOTS.test(ua)) return;
  if (/(^|;\\s*)io_me=1/.test(h.get("cookie") || "")) return;
  const purpose = (h.get("sec-purpose") || h.get("purpose") || h.get("x-moz") || "").toLowerCase();
  if (purpose.includes("prefetch") || purpose.includes("prerender")) return;
  const c = CREATORS[m[1]], cf = ctx.request.cf || {};
  const where = [cf.city, cf.country].filter(Boolean).join(", ") || "unknown location";
  const device = /iphone/i.test(ua) ? "iPhone" : /ipad/i.test(ua) ? "iPad" : /android/i.test(ua) ? "Android" : /macintosh/i.test(ua) ? "Mac" : /windows/i.test(ua) ? "Windows" : "other device";
  const app = /instagram/i.test(ua) ? " (Instagram app)" : /fban|fbav/i.test(ua) ? " (Facebook app)" : /gsa\\//i.test(ua) ? " (Google app)" : "";
  let via = "direct / email";
  try { const ref = h.get("referer"); if (ref) { const rh = new URL(ref).hostname.replace(/^www\\./, ""); via = rh === url.hostname ? "their own click on the page" : rh; } } catch (e) {}
  const msg = {
    topic,
    title: `${c.name} opened the ${PAGES[m[2]]}`,
    message: `${m[1]} · ${where} · ${device}${app} · via ${via}`,
    tags: [m[2] === "" ? "eyes" : "point_right"],
    priority: m[2] === "" ? 4 : 3,
    click: c.instagram ? `https://www.instagram.com/${c.instagram}/` : url.origin + "/" + m[1] + "/",
  };
  ctx.waitUntil(fetch((ctx.env.NTFY_SERVER || "https://ntfy.sh").replace(/\\/$/, "") + "/", {
    method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(msg),
  }).catch(() => {}));
}

async function notFound(ctx) {
  const page = await ctx.env.ASSETS.fetch(new URL("/404.html", ctx.request.url), { redirect: "follow" });
  return new Response(page.ok ? page.body : "Not found", {
    status: 404,
    headers: { "content-type": "text/html; charset=utf-8", "x-robots-tag": "noindex, nofollow" },
  });
}
"""


def write_pages_guard():
    allow, creators = ["/assets/"], {}
    for cj in sorted(ROOT.glob("*/content.json")):
        c = json.loads(cj.read_text())
        if c.get("status") == "live" and host(c) == "cloudflare":
            allow.append(f"/{cj.parent.name}/")
            # name shown in the visit alert; tapping the alert opens their Instagram (content.json → instagram, else the slug)
            creators[cj.parent.name] = {"name": c["name"], "instagram": c.get("instagram", cj.parent.name)}
    out = ROOT / "functions" / "_middleware.js"
    out.parent.mkdir(exist_ok=True)
    out.write_text(GUARD_JS.replace("__ALLOW__", json.dumps(allow)).replace("__PRIVATE__", json.dumps(PRIVATE_PER_CREATOR))
                   .replace("__CREATORS__", json.dumps(creators, ensure_ascii=False)))


def main():
    slug = sys.argv[1]
    d = ROOT / slug
    c = json.loads((d / "content.json").read_text())
    files = {
        "index.html": build_pitch(c, house_cases()),
        "funnel/index.html": build_funnel(c),
        "funnel/thank-you/index.html": build_thankyou(c),
        "emails/index.html": build_emails(c),
        "ads/index.html": build_ads(c),
    }
    for rel, content in files.items():
        f = d / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)
        print("wrote", f.relative_to(ROOT))
    write_redirects()
    write_pages_guard()
    print("wrote _redirects, functions/_middleware.js")


if __name__ == "__main__":
    main()
