---
name: creator-funnel
description: Baut aus Creator-Name + Instagram-Link + Angebotsname einen individuellen Creator-Funnel (Pitch-Seite, Landingpage, Pre-Call-E-Mails, Ad-Scripts) auf Basis echter öffentlicher Recherche. Nutzen, wenn ein neuer Funnel/Pitch für einen Creator erstellt werden soll oder bei "deploy it" für einen fertigen Funnel.
---

# Creator Funnel Skill

## Zweck

Baut aus einem Namen + Instagram-Link + Angebotsname automatisch einen individuellen Creator-Funnel (Pitch-Seite + Landingpage + Pre-Call-Sequenz + Ad-Scripts), basierend auf echter Recherche statt erfundener Inhalte. Layout und Struktur bleiben über alle Creator hinweg identisch - nur die Inhalte wechseln.

## Setup (einmalig)

Vor dem ersten Einsatz `HOUSE.md` im Projekt-Root anlegen mit den festen, wiederkehrenden Daten:

- Agentur-/Operator-Name
- Logo-Referenz
- Eigener Calendly-Link
- Eigene bestehende Case Studies (echte Ergebnisse, mit Zahlen und Zeitraum)
- Bevorzugter Ton/Stil

Diese Datei wird bei jedem Lauf gelesen und nie pro Creator neu abgefragt.

## Input pro Lauf

Ein Prompt mit minimal drei Angaben:
- Name des Creators
- Instagram-Link (oder anderer Haupt-Kanal)
- Name seines Angebots/Programms

## Ablauf

### Phase 1 - Recherche (mehrere Quellen parallel)

Sammle ausschließlich öffentlich zugängliche Informationen aus:
- Eigene Website/Funnel-Seite des Creators
- YouTube-Kanal (Upload-Frequenz, durchschnittliche Views der letzten 10 Videos, Themenschwerpunkt)
- Instagram/TikTok (Follower-Zahlen, Content-Stil)
- Skool/Whop, falls ein Community-Produkt existiert
- Meta Ad Library (laufen aktuell Ads, welche Hooks)
- Reddit/Foren (echte Formulierungen von Kunden/Kritikern zu seinem Angebot - nicht paraphrasiert erfinden, nur wirklich gefundene Aussagen sinngemäß referenzieren)

Ergebnis dieser Phase: eine `dossier.md` mit den harten Fakten (Follower je Plattform, Upload-Performance, aktuellem Funnel-Setup des Creators, seiner Positionierung, Preis falls öffentlich).

### Phase 2 - Wedge/Positionierung

Aus dem Dossier eine kurze strategische Einordnung ableiten: Was ist die Lücke zwischen Reichweite und Monetarisierung? Was ist der konkrete Ansatzpunkt für den Pitch? Diese Einordnung basiert ausschließlich auf den in Phase 1 gefundenen Fakten, keine Spekulation über Umsätze oder interne Zahlen, die nirgends öffentlich stehen.

### Phase 3 - Content-Erstellung nach festem Schema

Befülle IMMER die gleiche Struktur - Layout und Reihenfolge ändern sich nie, nur Inhalte:

```
slug
name
niche
headline
subheadline
sections:
  hero (Creator-Bild, Headline, VSL-Platzhalter)
  problem (3 Karten)
  mechanism
  deliverables
  proof / caseStudy-Referenzen (eigene, echte Case Studies aus HOUSE.md - niemals erfundene Ergebnisse für den Prospect selbst)
  howItWorks
  qualification (Typeform-Fragen)
  finalCta
preCallEmails: [
  { emailNumber, type (Confirmation/Conviction/Objection handling/Expectations/One day out/Morning of), subject, previewText, body }
]
adScripts: [
  { angle, hook, script }
]
```

### Phase 4 - Design

Zwei getrennte Design-Systeme:
- **Der Funnel für den Creator selbst** (falls Teil des Angebots) nutzt dessen eigene Marken-Farben/Fonts, recherchiert aus seinem bestehenden Auftritt - nicht neu erfunden.
- **Die Pitch-Seite an den Creator** nutzt IMMER das gleiche, feste Master-Design (definiert in `HOUSE.md`), unabhängig vom Creator.

### Ehrlichkeitsregeln (nicht verhandelbar)

- Niemals Testimonials, Zitate, Kundenergebnisse oder Preise erfinden.
- Fehlt eine Information (z. B. Programmpreis nicht öffentlich): als `[CONFIRM]` markieren, nicht raten.
- Fehlt Beweismaterial (z. B. keine öffentlichen Testimonial-Videos): Platzhalter als `{{SWAP}}` markieren, keine fiktiven Inhalte einsetzen.
- Jede Zahl im Output muss auf eine konkrete Quelle aus Phase 1 zurückführbar sein.
- Reale Kundenzitate aus Foren/Reviews immer sinngemäß referenzieren, niemals wortwörtlich unter neuem Namen wiederverwenden oder als eigene Aussage ausgeben.

### Phase 5 - QA-Checks vor Vorschau

- Farbkontrast auf beiden Design-Systemen prüfen
- Mobile-Ansicht bei 375px Breite prüfen
- Keine unnötigen Drittanbieter-Requests außer explizit benötigten (z. B. Calendly-Embed)
- Alle internen Links (register/thank-you/replay etc.) funktionsfähig

### Phase 6 - Lokale Vorschau (kein automatischer Deploy)

Build lokal bereitstellen (z. B. `localhost:8788`) und explizit warten. Erst nach separatem Befehl "deploy it" fortfahren.

### Phase 7 - Deploy (nur auf expliziten Befehl)

Bei "deploy it":
1. Alle Dateien committen mit Commit-Message im Format `Add funnel for {creator-slug}`
2. Push zum verbundenen GitHub-Repo
3. Hosting-Anbieter (Netlify/Vercel) deployed automatisch über die bestehende Repo-Verbindung

## Output-Struktur pro Creator

```
{slug}/
  index.html          - Pitch-Seite (Hero, Deliverable-Karten, Calendly)
  register/ thank-you/ replay/  - Funnel-Seiten
  deck/                - Slides
  ads/                 - statische + Carousel-Mocks, Scripts
  emails/              - pre-webinar, post-webinar, pre-call
  dossier.md           - Recherche-Ergebnis
  offer-deck-filled.md - befülltes Angebots-Dokument
README.md              - Liste offener [CONFIRM]/{{SWAP}}-Stellen für diesen Creator
```

## Nicht tun

- Keine automatische Veröffentlichung ohne expliziten Deploy-Befehl
- Keine Layout-Variation zwischen Creatorn bei der Pitch-Seite
- Keine erfundenen Kennzahlen, Testimonials oder Zitate
- Keine Vermischung der beiden Design-Systeme (Creator-Marke vs. Pitch-Master-Design)
