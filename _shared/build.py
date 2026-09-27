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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "_shared"
FLAG = re.compile(r"(\[CONFIRM[^\]]*\]|\{\{SWAP\}\}[^<\n]*)")
# Files that stay in the repo but must never be served.
PRIVATE_PER_CREATOR = ["dossier.md", "offer-deck-filled.md", "README.md", "content.json"]
PRIVATE_SITE = ["/HOUSE.md", "/README.md", "/_shared/*", "/.claude/*", "/netlify.toml"]

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


def page(title, css, body, extra_head=""):
    return f"""<!doctype html>
<html lang="en">
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
            f'<div class="case reveal"><span class="case__metric">{t(x["metric"])}</span><p class="case__name">{t(x["name"])}</p><p class="case__text">{t(x["text"])}</p></div>'
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
    head = '<script src="https://assets.calendly.com/assets/external/widget.js" async></script>\n'
    return page(f'{c["brandName"]}', (SHARED / "pitch-master.css").read_text(), body, head)


# ---------- creator funnel (creator brand) ----------

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
                f'<label class="opt"><input type="{kind}" name="{name}" value="{a(o)}"{req}> {html.escape(o)}</label>' for o in q["options"]
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
<section><div class="wrap"><div class="sec-head"><span class="eyebrow reveal">The problem</span><h2 class="reveal">{t(s["problem"]["title"])}</h2></div><div class="grid3">{numbered(s["problem"]["cards"])}</div></div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow reveal">The method</span><h2 class="reveal">{t(s["mechanism"]["title"])}</h2><p class="lead reveal">{t(s["mechanism"]["body"])}</p></div><div class="pillars">{pillars}</div></div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow reveal">The mentorship</span><h2 class="reveal">{t(s["deliverables"]["title"])}</h2></div><div class="grid3">{numbered(s["deliverables"]["items"])}</div></div></section>
<section><div class="wrap"><div class="sec-head"><span class="eyebrow reveal">Proof</span><h2 class="reveal">{t(s["proof"]["title"])}</h2></div><div class="proof-grid">{proof}</div><p class="note">{t(s["proof"]["note"])}</p></div></section>
<section><div class="wrap narrow"><div class="sec-head"><span class="eyebrow reveal">The process</span><h2 class="reveal">{t(s["howItWorks"]["title"])}</h2></div><ol class="steps">{steps(s["howItWorks"]["steps"])}</ol></div></section>
<section id="apply"><div class="wrap narrow">
  <div class="sec-head"><span class="eyebrow reveal">Application</span><h2 class="reveal">{t(s["qualification"]["title"])}</h2><p class="lead reveal">Six questions, about two minutes.</p></div>
  <form class="apply" action="thank-you/" method="get">
    {''.join(qs)}
    <fieldset class="reveal"><legend><span>✓</span>Your details</legend>{contact}</fieldset>
    <div><button class="btn" type="submit">{t(s["finalCta"]["cta"])} {ARROW}</button></div>
    <p class="note">Preview: the form isn't connected yet <span class="flag">[CONFIRM] form tool + qualification logic</span></p>
  </form>
</div></section>
<section class="final"><div class="wrap narrow"><h2 class="reveal">{t(s["finalCta"]["title"])}</h2><p class="lead reveal">{t(s["finalCta"]["body"])}</p><a class="btn reveal" href="#apply">{t(s["finalCta"]["cta"])} {ARROW}</a></div></section>
"""
    return page(f'{c["brandName"]}: Mentorship', brand_css(c), funnel_shell(c, inner, "#apply"))


def build_thankyou(c):
    inner = f"""
<section class="hero"><div class="wrap narrow">
  <span class="eyebrow reveal">Application received</span>
  <h1 class="reveal">Last step: pick your call time.</h1>
  <p class="lead reveal">If your application is a fit, book a slot below. You'll get a confirmation email right away.</p>
  <div class="vsl reveal" role="img" aria-label="Calendar placeholder"><div class="vsl__play">{PLAY}</div><p class="vsl__note"><span class="flag">[CONFIRM] Simran's booking calendar embed</span></p></div>
</div></section>
<section><div class="wrap narrow"><div class="sec-head"><span class="eyebrow reveal">Before the call</span><h2 class="reveal">Three things to do now</h2></div>
  <ol class="steps">{steps([
      {"title": "Check your inbox", "body": "A confirmation plus a few short emails so the call is useful."},
      {"title": "Prepare your last 10–20 trades", "body": "Journal, screenshots or a broker statement are all fine."},
      {"title": "Only trust official links", "body": "We never ask for payment via Telegram DM or WhatsApp."}])}</ol>
  <p class="note"><a href="../">← Back to the page</a></p>
</div></section>"""
    return page(f'{c["brandName"]}: Booked', brand_css(c), funnel_shell(c, inner))


MERGE_TAG = re.compile(r"(\{\{[a-z_]+\}\})")


def tags(s):
    return MERGE_TAG.sub(r"<code>\1</code>", t(s))


def build_emails(c):
    mails = "".join(
        f"""<article class="mail reveal"><div class="mail__head"><span class="mail__type">Email {e["emailNumber"]} · {t(e["type"])}</span><span class="mail__subj">{t(e["subject"])}</span><span class="mail__prev">{t(e["previewText"])}</span></div>
<div class="mail__body">{tags(e["body"])}</div></article>"""
        for e in c["preCallEmails"]
    )
    inner = f"""<section class="hero"><div class="wrap narrow"><span class="eyebrow reveal">Email sequence · booked to call</span><h1 class="reveal">The pre-call sequence</h1>
<p class="lead reveal">{len(c["preCallEmails"])} emails from booking to the morning of the call. Placeholders like <code>{{{{first_name}}}}</code> are filled by the email tool.</p><div class="doc">{mails}</div></div></section>"""
    return page(f'{c["brandName"]}: Pre-call emails', brand_css(c), funnel_shell(c, inner))


def build_ads(c):
    ads = "".join(
        f"""<article class="mail reveal"><div class="mail__head"><span class="mail__type">Angle {n:02d} · {t(x["angle"])}</span><span class="mail__subj">“{t(x["hook"])}”</span></div>
<div class="mail__body">{t(x["script"])}</div></article>"""
        for n, x in enumerate(c["adScripts"], 1)
    )
    inner = f"""<section class="hero"><div class="wrap narrow"><span class="eyebrow reveal">Ad creatives · video</span><h1 class="reveal">Ad creative scripts</h1>
<p class="lead reveal">{len(c["adScripts"])} angles for retargeting. Rule for every ad: no return or profit claims, no trade calls, and a risk notice on screen.</p><div class="doc">{ads}</div></div></section>"""
    return page(f'{c["brandName"]}: Ad scripts', brand_css(c), funnel_shell(c, inner))


def house_cases():
    """Case studies from HOUSE.md: only filled entries (no [placeholders]) are used."""
    txt = (ROOT / "HOUSE.md").read_text()
    out = []
    for m in re.finditer(r"\d+\. Kunde: (.+)\n\s+Ergebnis: (.+)\n\s+Zeitraum: (.+)\n\s+Beweis: (.+)", txt):
        name, res, period, _ = (g.strip() for g in m.groups())
        if "[" in name or "[" in res:
            continue
        out.append({"metric": f"{res} {period}", "name": name, "text": ""})
    return out


def write_redirects():
    lines = ["# Generated by _shared/build.py: internal notes stay in the repo but are never served."]
    lines += [f"{p}  /404.html  404!" for p in PRIVATE_SITE]
    for cj in sorted(ROOT.glob("*/content.json")):
        slug = cj.parent.name
        lines += [f"/{slug}/{f}  /404.html  404!" for f in PRIVATE_PER_CREATOR]
    (ROOT / "_redirects").write_text("\n".join(lines) + "\n")


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
    print("wrote _redirects")


if __name__ == "__main__":
    main()
