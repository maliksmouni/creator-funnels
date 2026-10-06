---
name: creator-funnel
description: Baut aus einem Creator-Link (Instagram o. ä.) einen individuellen Creator-Funnel (Pitch-Seite, Call- oder Webinar-Funnel, Pre-Call-E-Mails, Ad-Scripts) auf Basis echter öffentlicher Recherche und deployed ihn über Cloudflare Pages. Nutzen, wenn ein neuer Funnel/Pitch für einen Creator erstellt werden soll, bei Änderungen an einem bestehenden Creator-Ordner oder bei "deploy it". Deployt automatisch, sobald die QA bestanden ist.
---

# Creator Funnel Skill

## Zweck

Baut aus einem Creator-Link (plus optional Name und Angebotsname) einen individuellen Creator-Funnel: eine Pitch-Seite an den Creator plus ein fertig gebauter Funnel in seiner Optik, Pre-Call-Sequenz und Ad-Scripts. Alles basiert auf echter Recherche statt erfundener Inhalte. Layout und Struktur bleiben über alle Creator hinweg identisch; nur `content.json` ändert sich.

Referenz-Umsetzungen: `trading-diva/` (Simran Nigam, Mentoring über einem Recorded Course) und `gustavo-zapz/` (Gustavo Zapz, Mentoring über einer $200/Monat-Community).

## Repo-Aufbau (fest)

```
HOUSE.md                    feste Operator-Daten + Design-Master (jeder Lauf liest das)
_shared/build.py            rendert alle Seiten eines Creators aus content.json
_shared/thumbs.mjs          macht die Vorschaubilder für die Deliverable-Karten, die Link-Vorschau-Karte (og.jpg) und die Instagram-Story (story.jpg)
_shared/yt_thumb.py         holt das Thumbnail des neuesten YouTube-Uploads als Video-Platzhalter
_shared/site.json           öffentliche Basis-URL je Host (für Link-Vorschau-Tags): cloudflare = https://infooperate.pages.dev, netlify = https://infooperate.netlify.app
_shared/pitch-master.css    Master-Design der Pitch-Seite (für alle Creator gleich)
_shared/creator-funnel.css  Funnel-Layout; Farben kommen aus content.json → brand
assets/fonts/               selbst gehostete OFL-Fonts (Bricolage Grotesque, Inter, JetBrains Mono)
_shared/publish.py          Cloudflare-Pages-Build: kopiert nur öffentliche Dateien live geschalteter Creator nach dist/
_headers, 404.html          noindex für alle Seiten, 404-Seite (werden mit nach dist/ kopiert)
_redirects                  Netlify (generiert): sperrt interne Dateien, Entwürfe und alle Cloudflare-Creator
{slug}/                     ein Ordner pro Creator (siehe Output-Struktur)
```

Seiten niemals von Hand editieren. Texte ändern: `content.json`, danach bauen (Phase 5).

## Setup (einmalig)

`HOUSE.md` im Projekt-Root enthält Operator-Name (optional), Logo (optional), Calendly-Link, Case Studies, Ton/Stil und den Design-Master. Case-Study-Format je Eintrag: `N. Kunde: …` plus eingerückte Zeilen `Angebot`, `Ergebnis`, `Zeitraum`, `Kennzahl` (Karte, Englisch), `Text` (ein Satz, Englisch), `Beweis: assets/cases/{name}.jpg (…)`, optional `Bildausschnitt: 50% 22%`. Screenshots liegen unter `/assets/cases/` (öffentlich, für alle Creator gleich). Der Design-Master ist in `_shared/pitch-master.css` umgesetzt. Case Studies aus `HOUSE.md` erscheinen automatisch auf der Pitch-Seite, sobald sie ausgefüllt sind (Einträge mit `[...]`-Platzhaltern werden ignoriert und als `{{SWAP}}` gezeigt). Die Datei wird bei jedem Lauf gelesen und nie pro Creator neu abgefragt.

## Input pro Lauf

Minimal: ein Link zum Hauptkanal des Creators (meist Instagram). Name und Angebotsname werden, wenn nicht angegeben, aus der Recherche ermittelt. Optional: Funnel-Typ (Call-Funnel oder Webinar-Funnel). Ohne Angabe gilt: Call-Funnel.

## Ablauf

### Phase 1: Recherche

Nur öffentlich zugängliche Informationen. Braucht Netzwerkzugriff (Environment auf „Full“ oder die Domains freigeben). Bewährte Zugriffswege:

| Quelle | Zugriff | Was holen |
|---|---|---|
| Instagram | `curl -H "x-ig-app-id: 936619743392459" "https://i.instagram.com/api/v1/users/web_profile_info/?username=HANDLE"` (die normale Profilseite leitet zum Login um) | full_name, biography, bio_links, Follower, Posts, letzte 12 Posts mit Views/Likes/Kommentaren/Captions, Profilbild |
| Instagram (Fallback) | Bei 401 „Please wait a few minutes“: **eine** Anfrage an `https://www.instagram.com/api/v1/users/web_profile_info/?username=HANDLE` mit Desktop-User-Agent + `x-ig-app-id` + `Referer`. Antwort sofort in eine eigene Datei speichern, nie mit einem Folgeversuch überschreiben. Kein Dauer-Retry. Sonst: Follower per Websuche (als `[CONFIRM]`) und den Nutzer nach den Bio-Links oder einem Screenshot fragen | wie oben |
| Eigene Website (aus Link-in-Bio) | curl, Text aus HTML ziehen; Unterseiten `/join`, `/pay`, `/pricing`, `/student-results`, `/faqs` prüfen; Plattform aus dem Quelltext (ClickFunnels, Kajabi, Stan, Skool …) | Angebot, Preis, Mitgliederzahl, Rabatt-/DM-Hinweise, veröffentlichte Schülerergebnisse |
| Podcast | `https://open.spotify.com/oembed?url=SHOW_URL` und `/embed/show/ID` (`__NEXT_DATA__`) | Showname, aktuelle Folge |
| YouTube | `curl -b "CONSENT=YES+1" https://www.youtube.com/@HANDLE/about` bzw. `/videos` und `/streams`, `ytInitialData` parsen (`lockupViewModel`) | Abonnenten, Videoanzahl, Gesamt-Views, Beitrittsdatum, Land, Beschreibung, letzte 10 Uploads, Livestreams, Avatar/Banner |
| Telegram | `https://t.me/KANAL` (Abonnenten, Beschreibung) und `https://t.me/s/KANAL` (letzte Posts mit Views) | Angebotslinks, VIP-/Paid-Hinweise, DM-Handles |
| Website / Checkout | curl; hinter JS/Bot-Check → Wert als `[CONFIRM]` markieren | Preis, Programm, Checkout-Plattform |
| Skool/Whop, Meta Ad Library, Reddit/Foren | Websuche; Meta Ad Library braucht Login → sonst `[CONFIRM]` | Community, Ads/Hooks, echte Kundenstimmen |

Headless Chromium vertraut dem Proxy-Zertifikat dieser Umgebung nicht. Für Screenshots externer Seiten die Requests per Playwright-`route` über Node-`fetch` laufen lassen (`NODE_USE_ENV_PROXY=1`, TLS-Prüfung bleibt an). Lokale Seiten brauchen das nicht.

Ergebnis: `{slug}/dossier.md` mit harten Fakten, **jede Zahl mit Quelle und Abrufdatum**.

Fallen bei Zahlen (nicht überziehen):
- YouTube-„1 month ago“ bedeutet 30–59 Tage. Frequenzen deshalb aus Datumsangaben ableiten (z. B. Datum im Stream-Titel), nicht aus den Alters-Buckets.
- „Fast täglich“ nur schreiben, wenn es die Daten hergeben; sonst „mehrmals pro Woche“ mit Zeitraum.
- Follower-Zahlen verschiedener Plattformen nicht zu „X Personen“ addieren (Überschneidung). Einzeln nennen.
- Views ≠ Zuschauer. Nichts wie „Tausende schauen jede Woche“ ohne Beleg.

### Phase 2: Wedge / Positionierung

Aus dem Dossier ableiten: Wo ist die Lücke zwischen Reichweite und Monetarisierung? Was ist der Ansatzpunkt für den Pitch? Nur belegte Fakten, keine Spekulation über Umsätze. Ergebnis in `{slug}/offer-deck-filled.md` (Wedge, Angebot an den Creator, Design-Tokens, offene Punkte).

### Phase 3: Content nach festem Schema (`{slug}/content.json`)

Struktur und Reihenfolge ändern sich nie, nur die Inhalte. Vorlage: `trading-diva/content.json`.

```
host (fehlt = "cloudflare"; nur die älteren Creator gustavo-zapz und trading-diva haben "netlify"), status ("draft" bis die QA in Phase 6 bestanden ist, dann automatisch "live"), slug, name, brandName, niche, offerName, image
brand: { bg, surface, line, text, muted, accent, accent-ink, signal }   ← Creator-Marke
headline, subheadline                                                   ← Funnel-Hero
demoBanner                                                              ← Pflicht, siehe Ehrlichkeitsregeln
video { thumb, youtubeId, title }        ← von yt_thumb.py gesetzt; Platzhalterbild für Pitch- und Funnel-Video

pitch:                                    ← Pitch-Seite an den Creator (Master-Design)
  eyebrow                                 z. B. "Already built for {brandName}"
  headline { before, mark, after }        kurz (max. ~10 Wörter) und konkret: was gebaut + das Angebot beim Namen,
                                          z. B. „I built the call funnel for your [Crown Strategy mentorship].“
                                          mark = Angebotsname des Creators. Keine Zahlenlisten, Umsatz nur mit Quelle.
  (Video = steht für die VSL, die der Creator für seinen Funnel aufnehmen würde; Thumbnail des neuesten Uploads als Platzhalter, kein Hinweistext, kein offener Punkt)
  bridge { title: "Four things I noticed", closing,
           beats[4]: { kicker, title, text, stats[{value,label}] | quote, source (nur bei Zitaten) } }
           Beat 1 = Reichweite vs. Angebot, 2 = ungenutztes warmes Publikum,
           3 = konkreter Engpass/Risiko, 4 = die Einwand-Vorwegnahme
  deliverablesTitle
  groups[]: { label, items[{ kicker, title, desc, href, url, thumb }] }
  cases { title, items (leer → kommt aus HOUSE.md) }
  cta { title, calendly (aus HOUSE.md) }
  footer

sections:                                 ← Funnel des Creators (seine Marke)
  hero { eyebrow, chips[], cta, navCta (kurz, z. B. "Apply"), vslNote }
  problem { title, cards[3] }
  mechanism { title, body, pillars[4] }
  deliverables { title, items[] }
  proof { title, items ({{SWAP}}), note }
  howItWorks { title, steps[] }
  qualification { title, questions[{q, type: choice|multi|text, options, disqualify[]}], contactFields,
                  notFit { title, body } }
                  disqualify = Antworten, die zum „Not a fit“-Hinweis führen statt zur Buchung
                  (Standard: „trade only money you can afford to lose“ = No, „ready to invest“ = No).
                  Das Formular speichert in der Demo nichts. Ein echtes Formular-Tool (z. B. Tally
                  oder Typeform) erst anschließen, wenn der Creator zugestimmt hat: sonst sammelt die Demo
                  echte Kontaktdaten unter seinem Namen. Kein „[CONFIRM] form tool“-Hinweis auf der Seite.
  finalCta { title, body, cta, disclaimer }

preCallEmails[6]: { emailNumber, type (Confirmation / Conviction / Objection handling /
                    Expectations / One day out / Morning of), subject, previewText, body }
adScripts[]: { angle, hook, script }
```

Funnel-Typ: Der Call-Funnel nutzt `funnel/` (Seite + Bewerbung) und `funnel/thank-you/`. Für einen Webinar-Funnel kommen `register/`, `thank-you/`, `replay/` sowie Pre-/Post-Webinar-Mails hinzu. `build.py` muss dafür erweitert werden; das Master-Design bleibt gleich.

### Festgelegte Entscheidungen des Nutzers (Pitch-Seite)

Diese Punkte hat der Nutzer ausdrücklich so bestimmt. Sie gelten für jeden Creator und sind im Template (`build.py` + `pitch-master.css`) umgesetzt. Nicht wieder einbauen, außer der Nutzer verlangt es:

| Bereich | So ist es | Nicht (mehr) vorhanden |
|---|---|---|
| Stil | Wie phil-pitch.pages.dev: Papier-Hintergrund, Grotesk-Headlines, Mono-Labels, Bronze | alter schlichter Stil |
| Headline | kurz, ~10 Wörter, nennt das Angebot beim Namen („I built the call funnel for your [Crown Strategy mentorship].“) | lange Headlines mit Zahlenaufzählungen, Umsatzversprechen ohne Quelle |
| Kopfzeile | nur der Brand-Name oben links (Tab-Titel = Brand-Name) | „· proposal“ |
| Hero | Eyebrow „Already built for {Brand}“, Headline, Video | Unterzeile, „Start here“, „See the deliverables“, Loom-/SWAP-Hinweis im Video |
| Video | steht für die **VSL des Creators** für seinen Funnel (kein Walkthrough des Nutzers). Platzhalter = Thumbnail des **neuesten** YouTube-Uploads (`yt_thumb.py`), Play-Button darüber; kein offener Punkt | leere dunkle Fläche, Loom-Hinweis |
| Four things I noticed | nur Titel, 4 nummerierte Karten mit Zahlen, Abschlusssatz | Eyebrow „Before the deliverables“, Quellenzeilen unter den Zahlen, Button „See what's built“ |
| Deliverables | gruppiert, kompakte Browser-Vorschauen, alle Karten gleich groß (max. ~430px) | große bzw. seitenbreite Karten, Link zum Dossier |
| Case Studies | 3 Karten aus `HOUSE.md`: oben der Beweis-Screenshot (`assets/cases/*.jpg`, Format 4:5, Ausschnitt per `Bildausschnitt`), darunter Kennzahl, „Kunde · Angebot“, ein Satz | Hinweistext darunter, erfundene Ergebnisse |
| Book a call | Überschrift + Calendly-Karte, Sticky-Button | Untertext, „Calendar not loading?“-Link |
| Signatur | keine | Absendername/Unterschrift |
| Link-Vorschau | og/twitter-Tags: Titel „Built for {Brand}“, Beschreibung = Headline, Bild = 1200×630-Karte (Eyebrow + Headline links, Video-Thumbnail mit Play-Button rechts) | nackte URL ohne Vorschau |
| Favicon | Inline-SVG (kein extra File): abgerundetes Quadrat mit dem ersten Buchstaben des Brand-Namens; Pitch-Seite Bronze #7c5a16 / Papier, Funnel-Seiten Creator-`accent` / `accent-ink` (`favicon()` in `build.py`) | kein Favicon (Browser-Standard) |
| Instagram-Story (Close Friends) | `story.jpg`, 1080×1920 im Pitch-Master-Stil: Eyebrow „Already built for {Brand}“, Pitch-Headline, Funnel-Vorschau im Browser-Rahmen („your call funnel“), „{Vorname}, the page, the application, the emails and the ads are ready.“, „Tap the link ↓“; darunter ≥ 340px frei für Link- und @Mention-Sticker (lange Headlines werden automatisch kleiner). Wird nach dem Livegang mit Anleitung an den Nutzer geschickt; posten kann nur der Nutzer (App) | automatisch posten (keine API für Close Friends/Link-Sticker) |
| Besuchs-Alarm | `functions/_middleware.js` (aus `build.py`) schickt beim Öffnen einer Pitch-Seite oder eines Deliverables eine Nachricht an den Discord-Kanal (Webhook) und/oder den Telegram-Bot des Nutzers („👀 {Name} opened the pitch page · Stadt, Land · Gerät · via …“ + Button „Open @handle on Instagram“; `content.json → instagram`, sonst Slug). Secrets nur in Cloudflare (Pages → Settings → Variables and secrets, Production): `DISCORD_WEBHOOK_URL` und/oder `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (nie im öffentlichen Repo). Übersprungen: Link-Vorschau-Bots, Prefetch, HEAD, eigene Geräte (einmal `?me=1` öffnen → Cookie). Selbsttest: `/{slug}/?alerttest={Discord-Webhook-ID oder Telegram-Chat-ID}` → Header `x-alert-result`. ntfy.sh funktioniert nicht (Gratis-Limit pro IP, Cloudflare-IPs immer über dem Tageslimit, 429). Lokal testen nur mit weggeschobenem `wrangler.jsonc` | Analytics-Skripte von Drittanbietern, ntfy.sh |
| Zusammenarbeit/Vergütung | steht nicht auf der Seite; der Nutzer bespricht das in der Cold-DM/E-Mail | Abschnitt „How we'd work together“ |

Neue Wünsche des Nutzers zum Design immer im Template umsetzen (nicht nur für einen Creator), in diese Tabelle eintragen, pushen und live prüfen.

### Phase 4: Design

Zwei getrennte Design-Systeme, nie mischen:
- **Pitch-Seite an den Creator:** immer `_shared/pitch-master.css` (Design-Master aus `HOUSE.md`). Warmes Papier (#f5f2ec), Bricolage Grotesque für Headlines, Inter für Text, JetBrains Mono für Labels, Bronze-Akzent (#7c5a16). Aufbau: zentrierter Hero mit markiertem Kernversprechen (ohne Unterzeile), großem Video (Platzhalter = Thumbnail des neuesten YouTube-Uploads, lokal gespeichert), ohne Buttons darunter, „Four things I noticed“ (ohne Eyebrow) als nummerierte Karten ohne Quellenzeilen, Abschlusssatz ohne Button, Deliverables gruppiert als kompakte Browser-Vorschauen (alle Karten gleich groß, max. ca. 430px breit, zentriert), Case Studies ohne Zusatznotiz, „Book a call“ nur mit Überschrift und Calendly-Karte (kein Untertext, kein Fallback-Link), Sticky-„Book a call“. Stil-Referenz: phil-pitch.pages.dev.
- **Funnel des Creators:** `_shared/creator-funnel.css` mit den Farben aus `content.json → brand`. Farben aus dem bestehenden Auftritt des Creators ableiten (YouTube-Banner, Profilbild, Website); Farbwerte per Bild-Quantisierung extrahieren, nie frei erfinden. Ohne definierte Markenpalette: als abgeleitet dokumentieren (intern `[CONFIRM]`). Typografie neutral (Inter), damit nichts vom Master-Design übernommen wird.
- Creator-Bild: aus dem öffentlichen Avatar (YouTube 900px bevorzugt). Ränder prüfen und zuschneiden: YouTube-Avatare haben oft fremde Thumbnail-Streifen am Rand. Speichern als `{slug}/assets/{name}.jpg`, max. 600px.

### Ehrlichkeitsregeln (nicht verhandelbar)

- Niemals Testimonials, Zitate, Kundenergebnisse oder Preise erfinden.
- Fehlende Information (z. B. Preis nicht öffentlich): nicht raten. Intern (`dossier.md`, `README.md`, `content.json`-Notizen) als `[CONFIRM]` führen.
- **Auf den Seiten steht nie ein `[CONFIRM]`.** Details, die unser Vorschlag sind (Session-Frequenz, Review-Format, Community-Plattform, Call-Länge), als konkreten Vorschlag ausformulieren und in `README.md` unter „Vorgeschlagene Standardwerte“ auflisten. Fakten, die fehlen (Preise, Kapazität, Regulierungsstatus), nicht erfinden, sondern den Satz so formulieren, dass er sie nicht braucht (z. B. „the investment is explained on the call“). Keine unbelegte Knappheit („limited spots“).
- Fehlendes Beweismaterial: `{{SWAP}}`, keine fiktiven Inhalte.
- Jede Zahl im Output muss auf eine konkrete Quelle aus Phase 1 zurückführbar sein. Die Quellen stehen im `dossier.md`, nicht auf der Pitch-Seite (Ausnahme: Herkunft eines wörtlichen Zitats).
- Reale Aussagen nur sinngemäß referenzieren. Wörtlich zitieren nur öffentliche Aussagen des Creators selbst, mit Quelle.
- Finanz-, Trading- und Gesundheitsnischen: keine Rendite- oder Ergebnisversprechen, keine Trade-Calls, Risikohinweis in jedem Ad und im Funnel-Footer. Regulatorik des Landes (z. B. SEBI in Indien, FTC/CFTC in den USA) als `[CONFIRM]` für eine Rechtsprüfung aufnehmen.
- Schülerergebnisse, die der Creator selbst veröffentlicht: im Funnel nur sinngemäß, mit Quelle („testimonial on {site}“) und dem Hinweis „Individual results, not typical“. In Ads keine Einkommenszahlen.
- Der Funnel in Creator-Optik ist ein Demo, bevor der Creator zustimmt. Deshalb trägt jede Funnel-Seite den `demoBanner` („Demo built for {Name}. Not their official site.“), damit er öffentlich nicht als offizielle Seite des Creators durchgeht.

### Phase 5: Bauen

```
python3 _shared/yt_thumb.py {slug} {youtube-handle}   # immer: neuestes Upload-Thumbnail als Video-Platzhalter
# Sind die letzten normalen Videos alt (> 6 Monate) und laufen regelmäßig Livestreams: `python3 _shared/yt_thumb.py {slug} {handle} streams` (neuester Stream)
python3 _shared/build.py {slug}          # schreibt index.html, funnel/, funnel/thank-you/, emails/, ads/ und _redirects
python3 -m http.server 8788 --bind 127.0.0.1 &   # vom Repo-Root aus (Fonts liegen unter /assets)
node _shared/thumbs.mjs {slug}           # Vorschaubilder → {slug}/assets/previews/*.jpg + Link-Vorschau-Karte {slug}/assets/og.jpg + Story {slug}/assets/story.jpg
```
`thumbs.mjs` braucht Playwright: `PW=/pfad/zu/node_modules/playwright/index.mjs` und `CHROME=/opt/pw-browsers/chromium-*/chrome-linux/chrome` setzen, falls nicht auflösbar. Playwright nie in ein `package.json` im Repo aufnehmen (Cloudflare würde es installieren).

### Phase 6: QA vor der Vorschau

- Farbkontrast: alle Text/Hintergrund-Paare beider Design-Systeme ≥ 4,5:1 (WCAG AA). Neue Brand-Farben immer nachrechnen.
- Mobile bei 375px: `document.documentElement.scrollWidth` darf auf keiner Seite > 375 sein. Häufige Ursachen: nicht umbrechende Chips/Flags, dekorative `::after`-Rahmen, Bilder ohne `height:auto`.
- Bilder: `img{height:auto}`, sonst verzerren `width`/`height`-Attribute die Darstellung.
- Screenshots von Pitch und Funnel (Desktop 1440 + Mobile 375) ansehen, nicht nur Zahlen prüfen.
- Drittanbieter-Requests: nur der Calendly-Embed auf der Pitch-Seite. Fonts selbst gehostet.
- Alle internen Links 200. Private Dateien (siehe unten) → 404.
- QA-Screenshots gehören ins Scratchpad, nicht ins Repo (`.gitignore` hat `qa-*.png`).

### Phase 7: Vorschau

Kein Warten auf Freigabe: Der Nutzer will vor dem Livegang nichts prüfen (Entscheidung 06.10.2026). Direkt nach bestandener QA weiter mit Phase 8. Screenshots nur auf Nachfrage; der Nutzer kann localhost aus der Cloud-Session nicht öffnen. Den Funnel in Creator-Optik nicht als öffentlichen Artifact-Link veröffentlichen.

### Phase 8: Deploy (automatisch nach bestandener QA)

Der Nutzer hat entschieden (06.10.2026): Jeder neue Funnel geht ohne „deploy it“ live, sobald Phase 6 vollständig bestanden ist. Entwurfs-Status: Neue Creator bekommen in `content.json` `"status": "draft"`, solange gebaut wird. `publish.py` kopiert dann nichts aus `/{slug}/` nach `dist/` (404), Zwischenstände können also gepusht werden, ohne öffentlich zu sein. Nach bestandener QA: `status` auf `"live"` setzen, bauen, auf den Arbeitsbranch **und** den Production-Branch `claude/add-skill-k8god6` pushen (Fast-Forward; ist der Production-Branch kein Vorfahre, zuerst mergen), live prüfen, Outreach. Besteht die QA nicht und lässt sich der Fehler nicht beheben: Entwurf bleiben lassen und dem Nutzer sagen, was fehlt. `[CONFIRM]`-Punkte in README/Dossier (z. B. vorgeschlagenes Angebot, unsicherer Standort) halten den Deploy nicht auf; sie werden im Abschlussbericht kurz genannt.

1. Committen: `Add funnel for {slug}` (neuer Creator) bzw. eine beschreibende Nachricht bei Änderungen. Pushen auf den Arbeitsbranch. Ist ein Creator bereits deployed, werden spätere Änderungswünsche direkt gebaut, gepusht und live geprüft.
2. Neue Creator laufen auf Cloudflare Pages; gustavo-zapz und trading-diva bleiben auf Netlify (`host: "netlify"`, Netlify-Setup unverändert: Repo-Root, kein Build-Command, `_redirects`). Cloudflare Pages: Projekt `infooperate` unter `https://infooperate.pages.dev` (auch in `_shared/site.json` → cloudflare), Production-Branch `claude/add-skill-k8god6`, Build-Command `python3 _shared/publish.py`, Output-Verzeichnis `dist`, Root leer. Private Dateien werden gar nicht hochgeladen (Allowlist in `publish.py`); zusätzlich sperrt `functions/_middleware.js` (von `build.py` generiert) alles außer live Cloudflare-Creatorn und `/assets/`, auch wenn im Dashboard die Build-Einstellungen fehlen. Neue private Dateien in `PRIVATE_PER_CREATOR` eintragen. Lokal prüfen: `python3 _shared/publish.py` und `npx wrangler pages dev dist` (und `npx wrangler pages dev .`). Zusätzlich existiert der ältere Worker `creator-funnels` (`https://creator-funnels.smounimalik.workers.dev`, `wrangler.jsonc`), nur damit der an gocholive verschickte Link weiter funktioniert.
3. Nach dem Push auf den Deploy warten (z. B. bis ein neuer Text live ist) und prüfen:
   - `/{slug}/`, `/{slug}/funnel/`, `/{slug}/funnel/thank-you/`, `/{slug}/emails/`, `/{slug}/ads/` → 200
   - `/{slug}/dossier.md`, `/{slug}/content.json`, `/{slug}/offer-deck-filled.md`, `/{slug}/README.md`, `/HOUSE.md`, `/_shared/*`, `/.claude/*` → 404
   - Header `x-robots-tag: noindex`
4. Die Live-Links an den Nutzer geben. Danach Outreach laut `CLAUDE.md`: Gmail-Entwurf mit Link-Platzhalter, `{slug}/assets/story.jpg` per Datei schicken (mit Close-Friends-Anleitung), dann den Instagram-Profil-Link des Creators als anklickbaren Link (kein Codeblock, damit er mobil direkt aufgeht) und am Ende den Pitch-Link als Codeblock zum Kopieren.

Hinweis: Das GitHub-Repo ist öffentlich. Dossier und Notizen sind dort sichtbar, auch wenn Cloudflare sie nicht ausliefert. Den Nutzer darauf hinweisen, solange das so ist.

## Output-Struktur pro Creator

```
{slug}/
  content.json          einzige Quelle für alle Texte (privat)
  dossier.md            Recherche mit Quellen (privat)
  offer-deck-filled.md  Wedge, Angebot, Design-Tokens (privat)
  README.md             offene [CONFIRM]/{{SWAP}}-Stellen + QA-Ergebnis (privat)
  index.html            Pitch-Seite (generiert)
  funnel/               Funnel-Seite + Bewerbung (generiert, Demo-Banner)
  funnel/thank-you/     Buchung/Bestätigung (generiert)
  emails/               Pre-Call-Sequenz als Seite (generiert)
  ads/                  Ad-Scripts als Seite (generiert)
  assets/               Creator-Bild + previews/*.jpg
```

## Nicht tun

- Kein Deploy, solange die QA (Phase 6) nicht bestanden ist; mit bestandener QA wird ohne Rückfrage deployt
- Keine Layout-Variation zwischen Creatorn bei der Pitch-Seite; Änderungen am Master-Design gelten für alle und gehören in `_shared/pitch-master.css` + `HOUSE.md`
- Keine erfundenen Kennzahlen, Testimonials, Zitate oder Preise
- Keine Vermischung der beiden Design-Systeme
- Generierte HTML-Dateien nicht von Hand ändern
- Keine internen Dateien öffentlich ausliefern; neue private Dateien in `build.py` (`PRIVATE_PER_CREATOR` / `PRIVATE_SITE`) eintragen
