# trading-diva: Simran Nigam („Trading Diva“)

Aware-Outreach-Pitch für einen Call-Funnel (Mentoring). Stand: 27.09.2026. Status: **lokale Vorschau, nicht deployed.**

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html` | Pitch-Seite an Simran (Master-Design, Calendly-Embed) |
| `funnel/` | Mentoring-Landingpage + Bewerbungsformular (ihre Optik) |
| `funnel/thank-you/` | Buchungs-/Bestätigungsseite |
| `emails/` | 6 Pre-Call-E-Mails (HTML-Vorschau in ihrer Optik) |
| `ads/` | 4 Ad-Scripts (HTML-Vorschau in ihrer Optik) |
| `assets/previews/` | Vorschaubilder für die Pitch-Seite (`node _shared/thumbs.mjs trading-diva`) |
| `dossier.md` | Recherche mit Quellen |
| `offer-deck-filled.md` | Wedge, Angebot, Design-Tokens |
| `content.json` | **Einzige Quelle für alle Texte.** Nach Änderungen neu bauen: `python3 _shared/build.py trading-diva` |

Nicht öffentlich: `dossier.md`, `offer-deck-filled.md`, `README.md` und `content.json` werden per `_redirects` auf 404 gesetzt. Die Funnel-Seiten tragen einen Demo-Banner.

Hinweis: `deck/` entfällt. Die Pitch-Seite selbst ist die Präsentation. Das Skill-Schema sieht `register/`, `replay/` vor. Die sind für Webinar-Funnels. Dieser Funnel ist ein Call-Funnel und nutzt deshalb `funnel/` + `funnel/thank-you/`.

## Offene `[CONFIRM]`-Stellen

**Vor dem Versand des Pitches an Simran:**
1. Video auf der Pitch-Seite = Platzhalter für ihre VSL (Thumbnail ihres neuesten Uploads), kein offener Punkt
2. Vergütungsmodell / Angebot von dir an sie (HOUSE.md, nicht definiert)
3. Tonalität / Anrede (HOUSE.md leer; aktuell: Englisch, „you“, direkt)
   Case Studies in HOUSE.md eintragen: sie erscheinen dann automatisch auf der Pitch-Seite

**Zum Creator (im Call mit Simran klären):**
4. Will sie überhaupt Mentoring/1:1 verkaufen? Name, Preis, Kapazität
5. Preis des Crown-Strategy-Kurses (Superprofile-Seite hinter Bot-Check)
6. Preis und Modell der VIP-Gruppe
7. Mentoring-Inhalte: Frequenz der Live-Sessions, Journal-Review-Format, Community-Plattform
8. Wer führt die Calls (Simran oder Team/Closer), Call-Länge
9. Ihr Buchungskalender + Formular-Tool (Typeform / Netlify Forms). Die Qualifizierungslogik ist gebaut: „No“ bei Risikokapital oder Investitionsbereitschaft → Not-a-fit-Hinweis, sonst → Buchungsseite. Das Formular speichert noch nichts.
10. Eigene Domain für den Funnel
11. Markenfarben/-schrift (aktuell aus Banner und Profilbild abgeleitet)
12. Meta Ad Library: laufen bereits Ads? (nicht geprüft)
13. **Compliance Indien (SEBI):** Status von Bildungs-Content vs. Beratung, VIP-Trade-Calls, Ad-Richtlinien für Finanzthemen. Vor dem Livegang rechtlich prüfen lassen.

## Vorgeschlagene Standardwerte auf den Seiten (mit Simran abstimmen)

Auf den Seiten steht kein `[CONFIRM]` mehr. Diese Punkte sind als Vorschlag ausformuliert:

| Seite | Vorschlag |
|---|---|
| Funnel · What's inside | Wöchentliche Live-Sessions (Nifty, Bank Nifty, Gold, BTC) |
| Funnel · What's inside | Journal-Reviews in einem festen Wochenblock |
| Funnel · What's inside | Eine offizielle Telegram-Gruppe nur für Mitglieder |
| Funnel · How it works | Call mit „Simran's team“ (wer genau die Calls führt, klären) |
| Funnel · Bewerbung | Frage 6 ohne Preisangabe; die Investition wird im Call erklärt |
| Alle Funnel-Seiten · Footer | Disclaimer ohne Hinweis auf Regulierungsstatus (SEBI-Prüfung bleibt offen, siehe oben) |
| Thank-you | Platzhalter „Booking calendar“ statt ihres Kalenders |
| E-Mail 4 | Call-Länge ca. 30 Minuten |
| Ad 2 | „Official page is linked in the caption“ statt Domain |
| Ad 4 | „Every application is reviewed personally“ statt „Limited spots“ (keine unbelegte Knappheit) |

## Offene `{{SWAP}}`-Stellen

- Pitch-Seite: 2 eigene Case Studies aus HOUSE.md (HOUSE.md ist noch leer)
- Funnel: Simrans Mentoring-VSL
- Funnel: 3 echte Schüler-Stories (nur mit Erlaubnis, keine gefunden)

## QA (Phase 6), Ergebnis

- Kontrast: alle Text/Hintergrund-Paare beider Design-Systeme ≥ 4,5:1 (WCAG AA). Minimum 5,6:1
- 375 px: kein horizontales Scrollen auf allen 5 Seiten
- Drittanbieter-Requests: nur `assets.calendly.com` auf der Pitch-Seite; Funnel-Seiten: keine
- Interne Links: alle erreichbar
- Formular: qualifizierte Antworten → Thank-you-Seite, disqualifizierende → Not-a-fit-Hinweis (4 Pfade getestet). Noch kein Tool angeschlossen.
