#!/usr/bin/env python3
"""Render a creator folder from its content.json.

Usage: python3 _shared/build.py <slug>

Layout and section order are fixed here; only content.json changes per creator.
The pitch page always uses pitch-master.css (HOUSE.md design master); the
creator funnel uses creator-funnel.css with the creator's brand tokens.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "_shared"
FLAG = re.compile(r"(\[CONFIRM[^\]]*\]|\{\{SWAP\}\}[^<\n]*)")


def t(s):
    """Escape text and highlight open [CONFIRM] / {{SWAP}} markers."""
    return FLAG.sub(r'<mark class="flag">\1</mark>', html.escape(s))


def page(title, css, body, lang="en", extra_head=""):
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{html.escape(title)}</title>
<style>{css}</style>
{extra_head}</head>
<body>
{body}
</body>
</html>
"""


def cards(items, cls="card"):
    return "".join(
        f'<div class="{cls}"><h3>{t(i["title"])}</h3><p>{t(i["body"])}</p></div>' for i in items
    )


def steps(items):
    return "".join(
        f'<li><span class="n">{n}</span><div><h3>{t(s["title"])}</h3><p>{t(s["body"])}</p></div></li>'
        for n, s in enumerate(items, 1)
    )


def proof(p):
    li = "".join(f'<div class="proof-slot">{t(i)}</div>' for i in p["items"])
    return f'<div class="proof-grid">{li}</div><p class="note">{t(p["note"])}</p>'


# ---------- pitch page (master design, identical for every creator) ----------

def build_pitch(c):
    p, s = c["pitch"], c["pitch"]["sections"]
    facts = "".join(
        f'<div class="fact"><strong>{t(f["value"])}</strong><span>{t(f["label"])}</span><small>{t(f["source"])}</small></div>'
        for f in p["facts"]
    )
    deliv = "".join(
        f'<a class="card link" href="{html.escape(d["href"])}"><h3>{t(d["title"])} <span aria-hidden="true">→</span></h3><p>{t(d["body"])}</p></a>'
        for d in s["deliverables"]["items"]
    )
    qual = "".join(f"<li>{t(i)}</li>" for i in s["qualification"]["items"])
    cal = html.escape(s["finalCta"]["calendly"])
    body = f"""
<header class="top"><div class="wrap"><span class="eyebrow">{t(p["eyebrow"])}</span></div></header>
<main>
<section class="hero"><div class="wrap hero-grid">
  <div>
    <h1>{t(p["headline"])}</h1>
    <p class="lead">{t(p["subheadline"])}</p>
    <a class="btn" href="#book">Book 30 minutes</a>
  </div>
  <figure class="portrait"><img src="{html.escape(c["image"])}" alt="{html.escape(c["name"])}" width="600" height="600"></figure>
</div>
<div class="wrap"><div class="vsl" role="img" aria-label="Video placeholder"><span>▶</span><p>{t(p["vslNote"])}</p></div></div>
</section>

<section><div class="wrap"><h2>The numbers</h2><div class="facts">{facts}</div></div></section>
<section><div class="wrap"><h2>{t(s["problem"]["title"])}</h2><div class="grid3">{cards(s["problem"]["cards"])}</div></div></section>
<section><div class="wrap narrow"><h2>{t(s["mechanism"]["title"])}</h2><p class="lead">{t(s["mechanism"]["body"])}</p></div></section>
<section><div class="wrap"><h2>{t(s["deliverables"]["title"])}</h2><div class="grid3">{deliv}</div></div></section>
<section><div class="wrap"><h2>{t(s["proof"]["title"])}</h2>{proof(s["proof"])}</div></section>
<section><div class="wrap narrow"><h2>{t(s["howItWorks"]["title"])}</h2><ol class="steps">{steps(s["howItWorks"]["steps"])}</ol></div></section>
<section><div class="wrap narrow"><h2>{t(s["qualification"]["title"])}</h2><ul class="checks">{qual}</ul></div></section>
<section id="book" class="final"><div class="wrap narrow">
  <h2>{t(s["finalCta"]["title"])}</h2><p class="lead">{t(s["finalCta"]["body"])}</p>
  <div class="calendly-inline-widget" data-url="{cal}?hide_gdpr_banner=1" style="min-width:280px;height:700px;"></div>
  <p class="fallback"><a href="{cal}" rel="noopener">Open the calendar in a new tab →</a></p>
  <p class="sign">{t(p["signoff"])}</p>
</div></section>
</main>
<footer><div class="wrap"><small>Research sources: <a href="dossier.md">dossier.md</a> · Prepared {html.escape(c["slug"])}</small></div></footer>
"""
    head = '<script src="https://assets.calendly.com/assets/external/widget.js" async></script>\n'
    css = (SHARED / "pitch-master.css").read_text()
    return page(f'{c["brandName"]}: call funnel proposal', css, body, extra_head=head)


# ---------- creator funnel (creator brand) ----------

def brand_css(c):
    b = c["brand"]
    tokens = ";".join(f"--{k}:{v}" for k, v in b.items() if not k.startswith("_"))
    return f":root{{{tokens}}}\n" + (SHARED / "creator-funnel.css").read_text()


def build_funnel(c):
    s = c["sections"]
    h = s["hero"]
    pillars = "".join(
        f'<div class="pillar"><span>{n:02d}</span><h3>{t(p["title"])}</h3><p>{t(p["body"])}</p></div>'
        for n, p in enumerate(s["mechanism"]["pillars"], 1)
    )
    qs = []
    for i, q in enumerate(s["qualification"]["questions"], 1):
        name = f"q{i}"
        if q["type"] == "text":
            field = f'<textarea name="{name}" rows="3" required></textarea>'
        else:
            kind = "checkbox" if q["type"] == "multi" else "radio"
            req = "" if kind == "checkbox" else " required"
            field = "".join(
                f'<label class="opt"><input type="{kind}" name="{name}" value="{html.escape(o)}"{req}> {html.escape(o)}</label>'
                for o in q["options"]
            )
        qs.append(f'<fieldset><legend><span>{i}</span> {t(q["q"])}</legend>{field}</fieldset>')
    contact = "".join(
        f'<label class="field">{html.escape(f)}<input name="{html.escape(f.lower().split()[0])}" required></label>'
        for f in s["qualification"]["contactFields"]
    )
    body = f"""
<header class="top"><div class="wrap"><span class="logo">{t(c["brandName"])}</span><a class="btn sm" href="#apply">{t(h["cta"])}</a></div></header>
<main>
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">{t(h["eyebrow"])}</span>
    <h1>{t(c["headline"])}</h1>
    <p class="lead">{t(c["subheadline"])}</p>
    <a class="btn" href="#apply">{t(h["cta"])}</a>
  </div>
  <figure class="portrait"><img src="../{html.escape(c["image"])}" alt="{html.escape(c["name"])}" width="600" height="600"></figure>
</div>
<div class="wrap"><div class="vsl" role="img" aria-label="Video placeholder"><span>▶</span><p>{t(h["vslNote"])}</p></div></div>
</section>
<section><div class="wrap"><h2>{t(s["problem"]["title"])}</h2><div class="grid3">{cards(s["problem"]["cards"])}</div></div></section>
<section><div class="wrap"><h2>{t(s["mechanism"]["title"])}</h2><p class="lead narrow">{t(s["mechanism"]["body"])}</p><div class="pillars">{pillars}</div></div></section>
<section><div class="wrap"><h2>{t(s["deliverables"]["title"])}</h2><div class="grid3">{cards(s["deliverables"]["items"])}</div></div></section>
<section><div class="wrap"><h2>{t(s["proof"]["title"])}</h2>{proof(s["proof"])}</div></section>
<section><div class="wrap narrow"><h2>{t(s["howItWorks"]["title"])}</h2><ol class="steps">{steps(s["howItWorks"]["steps"])}</ol></div></section>
<section id="apply"><div class="wrap narrow">
  <h2>{t(s["qualification"]["title"])}</h2>
  <form class="apply" action="thank-you/" method="get">
    {''.join(qs)}
    <fieldset><legend>Contact</legend>{contact}</fieldset>
    <button class="btn" type="submit">{t(s["finalCta"]["cta"])}</button>
    <p class="note">Preview: the form isn't connected to a tool yet. <mark class="flag">[CONFIRM] Typeform/form tool + qualification logic</mark></p>
  </form>
</div></section>
<section class="final"><div class="wrap narrow"><h2>{t(s["finalCta"]["title"])}</h2><p class="lead">{t(s["finalCta"]["body"])}</p><a class="btn" href="#apply">{t(s["finalCta"]["cta"])}</a></div></section>
</main>
<footer><div class="wrap"><small>{t(s["finalCta"]["disclaimer"])}</small></div></footer>
"""
    return page(f'{c["brandName"]}: Mentorship', brand_css(c), body)


def build_thankyou(c):
    body = f"""
<header class="top"><div class="wrap"><span class="logo">{t(c["brandName"])}</span></div></header>
<main><section><div class="wrap narrow">
  <span class="eyebrow">Application received</span>
  <h1>Last step: pick your call time.</h1>
  <p class="lead">If your application is a fit, book a slot below. You'll get a confirmation email right away.</p>
  <div class="vsl" role="img" aria-label="Calendar placeholder"><span>📅</span><p><mark class="flag">[CONFIRM] Simran's booking calendar embed</mark></p></div>
  <h2>Before the call</h2>
  <ol class="steps">
    <li><span class="n">1</span><div><h3>Check your inbox</h3><p>Confirmation plus a few short emails so the call is useful.</p></div></li>
    <li><span class="n">2</span><div><h3>Prepare your last 10–20 trades</h3><p>Journal, screenshots or broker statement are all fine.</p></div></li>
    <li><span class="n">3</span><div><h3>Only official links</h3><p>We never ask for payment via Telegram DM or WhatsApp.</p></div></li>
  </ol>
  <p><a href="../">← Back to the page</a></p>
</div></section></main>
<footer><div class="wrap"><small>{t(c["sections"]["finalCta"]["disclaimer"])}</small></div></footer>
"""
    return page(f'{c["brandName"]}: Booking', brand_css(c), body)


def build_deck(c):
    p, s = c["pitch"], c["pitch"]["sections"]
    slides = [
        f'<h1>{t(p["headline"])}</h1><p class="lead">{t(p["eyebrow"])}</p>',
        '<h2>The numbers</h2><div class="facts">' + "".join(
            f'<div class="fact"><strong>{t(f["value"])}</strong><span>{t(f["label"])}</span><small>{t(f["source"])}</small></div>'
            for f in p["facts"]) + "</div>",
        f'<h2>{t(s["problem"]["title"])}</h2><div class="grid3">{cards(s["problem"]["cards"])}</div>',
        f'<h2>{t(s["mechanism"]["title"])}</h2><p class="lead">{t(s["mechanism"]["body"])}</p>',
        f'<h2>{t(s["deliverables"]["title"])}</h2><div class="grid3">{cards(s["deliverables"]["items"])}</div>',
        f'<h2>{t(s["proof"]["title"])}</h2>{proof(s["proof"])}',
        f'<h2>{t(s["howItWorks"]["title"])}</h2><ol class="steps">{steps(s["howItWorks"]["steps"])}</ol>',
        f'<h2>{t(s["finalCta"]["title"])}</h2><p class="lead">{t(s["finalCta"]["body"])}</p><a class="btn" href="{html.escape(s["finalCta"]["calendly"])}">Book 30 minutes</a>',
    ]
    body = "<main class=\"deck\">" + "".join(
        f'<section class="slide"><div class="wrap">{sl}</div><span class="pg">{i}/{len(slides)}</span></section>'
        for i, sl in enumerate(slides, 1)
    ) + "</main>"
    css = (SHARED / "pitch-master.css").read_text() + DECK_CSS
    return page(f'{c["brandName"]}: Deck', css, body)


DECK_CSS = """
.deck{scroll-snap-type:y mandatory;height:100vh;overflow-y:auto}
.slide{min-height:100vh;display:flex;align-items:center;scroll-snap-align:start;position:relative;border-bottom:1px solid var(--line)}
.slide .pg{position:absolute;right:16px;bottom:12px;color:var(--muted);font-size:.8rem}
"""


def md_emails(c):
    out = [f'# Pre-Call-Sequenz: {c["brandName"]}\n', "Placeholders like `{{first_name}}` are filled by the email tool.\n"]
    for e in c["preCallEmails"]:
        out.append(f'\n## Email {e["emailNumber"]}: {e["type"]}\n\n**Subject:** {e["subject"]}  \n**Preview:** {e["previewText"]}\n\n{e["body"]}\n')
    return "".join(out)


def md_ads(c):
    out = [f'# Ad Scripts: {c["brandName"]}\n', "Rule: no return or profit claims, no trade calls, a risk notice in every ad.\n"]
    for n, a in enumerate(c["adScripts"], 1):
        out.append(f'\n## {n}. {a["angle"]}\n\n**Hook:** {a["hook"]}\n\n```\n{a["script"]}\n```\n')
    return "".join(out)


def main():
    slug = sys.argv[1]
    d = ROOT / slug
    c = json.loads((d / "content.json").read_text())
    files = {
        "index.html": build_pitch(c),
        "funnel/index.html": build_funnel(c),
        "funnel/thank-you/index.html": build_thankyou(c),
        "deck/index.html": build_deck(c),
        "emails/pre-call.md": md_emails(c),
        "ads/scripts.md": md_ads(c),
    }
    for rel, content in files.items():
        f = d / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content)
        print("wrote", f.relative_to(ROOT))


if __name__ == "__main__":
    main()
