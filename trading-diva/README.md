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
1. Loom-Walkthrough für das Video auf der Pitch-Seite
2. Vergütungsmodell / Angebot von dir an sie (HOUSE.md, nicht definiert)
3. Tonalität / Anrede (HOUSE.md leer; aktuell: Englisch, „you“, direkt)
   Case Studies in HOUSE.md eintragen: sie erscheinen dann automatisch auf der Pitch-Seite

**Zum Creator (im Call mit Simran klären):**
4. Will sie überhaupt Mentoring/1:1 verkaufen? Name, Preis, Kapazität
5. Preis des Crown-Strategy-Kurses (Superprofile-Seite hinter Bot-Check)
6. Preis und Modell der VIP-Gruppe
7. Mentoring-Inhalte: Frequenz der Live-Sessions, Journal-Review-Format, Community-Plattform
8. Wer führt die Calls (Simran oder Team/Closer), Call-Länge
9. Ihr Buchungskalender + Formular-Tool (Typeform o. ä.)
10. Eigene Domain für den Funnel
11. Markenfarben/-schrift (aktuell aus Banner und Profilbild abgeleitet)
12. Meta Ad Library: laufen bereits Ads? (nicht geprüft)
13. **Compliance Indien (SEBI):** Status von Bildungs-Content vs. Beratung, VIP-Trade-Calls, Ad-Richtlinien für Finanzthemen. Vor dem Livegang rechtlich prüfen lassen.

## Offene `{{SWAP}}`-Stellen

- Pitch-Seite: Loom-Walkthrough (3–5 Min.)
- Pitch-Seite: 2 eigene Case Studies aus HOUSE.md (HOUSE.md ist noch leer)
- Funnel: Simrans Mentoring-VSL
- Funnel: 3 echte Schüler-Stories (nur mit Erlaubnis, keine gefunden)

## QA (Phase 6), Ergebnis

- Kontrast: alle Text/Hintergrund-Paare beider Design-Systeme ≥ 4,5:1 (WCAG AA). Minimum 5,6:1
- 375 px: kein horizontales Scrollen auf allen 5 Seiten
- Drittanbieter-Requests: nur `assets.calendly.com` auf der Pitch-Seite; Funnel-Seiten: keine
- Interne Links: alle erreichbar
- Das Formular ist in der Vorschau nicht angeschlossen (Submit führt zur Thank-you-Seite)
