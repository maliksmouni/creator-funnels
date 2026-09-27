---
name: creator-funnel
description: Baut aus einem Creator-Link (Instagram o. ä.) einen individuellen Creator-Funnel (Pitch-Seite, Call- oder Webinar-Funnel, Pre-Call-E-Mails, Ad-Scripts) auf Basis echter öffentlicher Recherche und deployed ihn über Netlify. Nutzen, wenn ein neuer Funnel/Pitch für einen Creator erstellt werden soll, bei Änderungen an einem bestehenden Creator-Ordner oder bei "deploy it".
---

# Creator Funnel Skill

## Zweck

Baut aus einem Creator-Link (plus optional Name und Angebotsname) einen individuellen Creator-Funnel: eine Pitch-Seite an den Creator plus ein fertig gebauter Funnel in seiner Optik, Pre-Call-Sequenz und Ad-Scripts. Alles basiert auf echter Recherche statt erfundener Inhalte. Layout und Struktur bleiben über alle Creator hinweg identisch; nur `content.json` ändert sich.

Referenz-Umsetzung: `trading-diva/` (Simran Nigam, Call-Funnel für Mentoring).

## Repo-Aufbau (fest)

```
HOUSE.md                    feste Operator-Daten + Design-Master (jeder Lauf liest das)
_shared/build.py            rendert alle Seiten eines Creators aus content.json
_shared/thumbs.mjs          macht die Vorschaubilder für die Deliverable-Karten
_shared/pitch-master.css    Master-Design der Pitch-Seite (für alle Creator gleich)
_shared/creator-funnel.css  Funnel-Layout; Farben kommen aus content.json → brand
assets/fonts/               selbst gehostete OFL-Fonts (Bricolage Grotesque, Inter, JetBrains Mono)
_redirects, _headers, 404.html   Netlify: interne Dateien → 404, noindex (generiert bzw. fest)
{slug}/                     ein Ordner pro Creator (siehe Output-Struktur)
```

Seiten niemals von Hand editieren. Texte ändern: `content.json`, danach bauen (Phase 6).

## Setup (einmalig)

`HOUSE.md` im Projekt-Root enthält Operator-Name (optional), Logo (optional), Calendly-Link, Case Studies, Ton/Stil und den Design-Master. Der Design-Master ist in `_shared/pitch-master.css` umgesetzt. Case Studies aus `HOUSE.md` erscheinen automatisch auf der Pitch-Seite, sobald sie ausgefüllt sind (Einträge mit `[...]`-Platzhaltern werden ignoriert und als `{{SWAP}}` gezeigt). Die Datei wird bei jedem Lauf gelesen und nie pro Creator neu abgefragt.

## Input pro Lauf

Minimal: ein Link zum Hauptkanal des Creators (meist Instagram). Name und Angebotsname werden, wenn nicht angegeben, aus der Recherche ermittelt. Optional: Funnel-Typ (Call-Funnel oder Webinar-Funnel). Ohne Angabe gilt: Call-Funnel.

## Ablauf

### Phase 1: Recherche

Nur öffentlich zugängliche Informationen. Braucht Netzwerkzugriff (Environment auf „Full“ oder die Domains freigeben). Bewährte Zugriffswege:

| Quelle | Zugriff | Was holen |
|---|---|---|
| Instagram | `curl -H "x-ig-app-id: 936619743392459" "https://i.instagram.com/api/v1/users/web_profile_info/?username=HANDLE"` (die normale Profilseite leitet zum Login um) | full_name, biography, bio_links, Follower, Posts, letzte 12 Posts mit Views/Likes/Kommentaren/Captions, Profilbild |
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
slug, name, brandName, niche, offerName, image
brand: { bg, surface, line, text, muted, accent, accent-ink, signal }   ← Creator-Marke
headline, subheadline                                                   ← Funnel-Hero
demoBanner                                                              ← Pflicht, siehe Ehrlichkeitsregeln

pitch:                                    ← Pitch-Seite an den Creator (Master-Design)
  eyebrow                                 z. B. "Already built for {brandName}"
  headline { before, mark, after }        mark = hervorgehobenes Kernversprechen
  subheadline, vslNote ({{SWAP}} Loom)
  bridge { eyebrow, title: "Four things I noticed", closing,
           beats[4]: { kicker, title, text, stats[{value,label}] | quote, source } }
           Beat 1 = Reichweite vs. Angebot, 2 = ungenutztes warmes Publikum,
           3 = konkreter Engpass/Risiko, 4 = die Einwand-Vorwegnahme
  deliverablesTitle
  groups[]: { label, items[{ kicker, title, desc, href, url, thumb }] }
  cases { title, items (leer → kommt aus HOUSE.md), note }
  cta { title, sub, calendly (aus HOUSE.md) }
  footer

sections:                                 ← Funnel des Creators (seine Marke)
  hero { eyebrow, chips[], cta, navCta (kurz, z. B. "Apply"), vslNote }
  problem { title, cards[3] }
  mechanism { title, body, pillars[4] }
  deliverables { title, items[] }
  proof { title, items ({{SWAP}}), note }
  howItWorks { title, steps[] }
  qualification { title, questions[{q, type: choice|multi|text, options}], contactFields }
  finalCta { title, body, cta, disclaimer }

preCallEmails[6]: { emailNumber, type (Confirmation / Conviction / Objection handling /
                    Expectations / One day out / Morning of), subject, previewText, body }
adScripts[]: { angle, hook, script }
```

Funnel-Typ: Der Call-Funnel nutzt `funnel/` (Seite + Bewerbung) und `funnel/thank-you/`. Für einen Webinar-Funnel kommen `register/`, `thank-you/`, `replay/` sowie Pre-/Post-Webinar-Mails hinzu. `build.py` muss dafür erweitert werden; das Master-Design bleibt gleich.

### Phase 4: Design

Zwei getrennte Design-Systeme, nie mischen:
- **Pitch-Seite an den Creator:** immer `_shared/pitch-master.css` (Design-Master aus `HOUSE.md`). Warmes Papier (#f5f2ec), Bricolage Grotesque für Headlines, Inter für Text, JetBrains Mono für Labels, Bronze-Akzent (#7c5a16). Aufbau: zentrierter Hero mit markiertem Kernversprechen und großem Video, „Four things I noticed“ als nummerierte Karten mit Quellen, Deliverables gruppiert als Browser-Vorschauen, Case Studies, große Calendly-Karte, Sticky-„Book a call“. Stil-Referenz: phil-pitch.pages.dev.
- **Funnel des Creators:** `_shared/creator-funnel.css` mit den Farben aus `content.json → brand`. Farben aus dem bestehenden Auftritt des Creators ableiten (YouTube-Banner, Profilbild, Website); Farbwerte per Bild-Quantisierung extrahieren, nie frei erfinden. Ohne definierte Markenpalette: als abgeleitet dokumentieren und `[CONFIRM]` setzen. Typografie neutral (Inter), damit nichts vom Master-Design übernommen wird.
- Creator-Bild: aus dem öffentlichen Avatar (YouTube 900px bevorzugt). Ränder prüfen und zuschneiden: YouTube-Avatare haben oft fremde Thumbnail-Streifen am Rand. Speichern als `{slug}/assets/{name}.jpg`, max. 600px.

### Ehrlichkeitsregeln (nicht verhandelbar)

- Niemals Testimonials, Zitate, Kundenergebnisse oder Preise erfinden.
- Fehlende Information (z. B. Preis nicht öffentlich): `[CONFIRM]`, nicht raten.
- Fehlendes Beweismaterial: `{{SWAP}}`, keine fiktiven Inhalte.
- Jede Zahl im Output muss auf eine konkrete Quelle aus Phase 1 zurückführbar sein. Auf der Pitch-Seite steht die Quelle direkt am Beat.
- Reale Aussagen nur sinngemäß referenzieren. Wörtlich zitieren nur öffentliche Aussagen des Creators selbst, mit Quelle.
- Finanz-, Trading- und Gesundheitsnischen: keine Rendite- oder Ergebnisversprechen, keine Trade-Calls, Risikohinweis in jedem Ad und im Funnel-Footer. Regulatorik des Landes (z. B. SEBI in Indien) als `[CONFIRM]` für eine Rechtsprüfung aufnehmen.
- Der Funnel in Creator-Optik ist ein Demo, bevor der Creator zustimmt. Deshalb trägt jede Funnel-Seite den `demoBanner` („Demo built for {Name}. Not their official site.“), damit er öffentlich nicht als offizielle Seite des Creators durchgeht.

### Phase 5: Bauen

```
python3 _shared/build.py {slug}          # schreibt index.html, funnel/, funnel/thank-you/, emails/, ads/ und _redirects
python3 -m http.server 8788 --bind 127.0.0.1 &   # vom Repo-Root aus (Fonts liegen unter /assets)
node _shared/thumbs.mjs {slug}           # Vorschaubilder → {slug}/assets/previews/*.jpg
```
`thumbs.mjs` braucht Playwright: `PW=/pfad/zu/node_modules/playwright/index.mjs` und `CHROME=/opt/pw-browsers/chromium-*/chrome-linux/chrome` setzen, falls nicht auflösbar. Playwright nie in ein `package.json` im Repo aufnehmen (Netlify würde es installieren).

### Phase 6: QA vor der Vorschau

- Farbkontrast: alle Text/Hintergrund-Paare beider Design-Systeme ≥ 4,5:1 (WCAG AA). Neue Brand-Farben immer nachrechnen.
- Mobile bei 375px: `document.documentElement.scrollWidth` darf auf keiner Seite > 375 sein. Häufige Ursachen: nicht umbrechende Chips/Flags, dekorative `::after`-Rahmen, Bilder ohne `height:auto`.
- Bilder: `img{height:auto}`, sonst verzerren `width`/`height`-Attribute die Darstellung.
- Screenshots von Pitch und Funnel (Desktop 1440 + Mobile 375) ansehen, nicht nur Zahlen prüfen.
- Drittanbieter-Requests: nur der Calendly-Embed auf der Pitch-Seite. Fonts selbst gehostet.
- Alle internen Links 200. Private Dateien (siehe unten) → 404.
- QA-Screenshots gehören ins Scratchpad, nicht ins Repo (`.gitignore` hat `qa-*.png`).

### Phase 7: Vorschau

Lokal auf `localhost:8788` bauen. Der Nutzer kann localhost aus der Cloud-Session nicht öffnen: Screenshots schicken oder eine selbstständige HTML-Datei (Bild als data-URI) per Datei senden. Den Funnel in Creator-Optik nicht als öffentlichen Artifact-Link veröffentlichen.

### Phase 8: Deploy (nur auf „deploy it“)

1. Committen: `Add funnel for {slug}` (neuer Creator) bzw. eine beschreibende Nachricht bei Änderungen. Pushen auf den Arbeitsbranch.
2. Netlify baut automatisch aus dem verbundenen Repo. Stand: Site `https://starlit-kangaroo-62a92c.netlify.app`, Branch `claude/add-skill-k8god6`, kein Build-Command, Publish-Verzeichnis = Repo-Root.
3. Nach dem Push auf den Deploy warten (z. B. bis ein neuer Text live ist) und prüfen:
   - `/{slug}/`, `/{slug}/funnel/`, `/{slug}/funnel/thank-you/`, `/{slug}/emails/`, `/{slug}/ads/` → 200
   - `/{slug}/dossier.md`, `/{slug}/content.json`, `/{slug}/offer-deck-filled.md`, `/{slug}/README.md`, `/HOUSE.md`, `/_shared/*`, `/.claude/*` → 404
   - Header `x-robots-tag: noindex`
4. Die Live-Links an den Nutzer geben.

Hinweis: Das GitHub-Repo ist öffentlich. Dossier und Notizen sind dort sichtbar, auch wenn Netlify sie nicht ausliefert. Den Nutzer darauf hinweisen, solange das so ist.

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

- Kein Deploy ohne expliziten Befehl
- Keine Layout-Variation zwischen Creatorn bei der Pitch-Seite; Änderungen am Master-Design gelten für alle und gehören in `_shared/pitch-master.css` + `HOUSE.md`
- Keine erfundenen Kennzahlen, Testimonials, Zitate oder Preise
- Keine Vermischung der beiden Design-Systeme
- Generierte HTML-Dateien nicht von Hand ändern
- Keine internen Dateien öffentlich ausliefern; neue private Dateien in `build.py` (`PRIVATE_PER_CREATOR` / `PRIVATE_SITE`) eintragen
