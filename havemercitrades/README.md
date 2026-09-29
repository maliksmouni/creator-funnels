# havemercitrades: Mercedith „Merci“ (HaveMerciTrades)

Aware-Outreach-Pitch für einen Call-Funnel für die „7-Week Private Mentorship“. Stand: 29.09.2026. Status: **draft** (auf Cloudflare und Netlify gesperrt). Ziel-URL nach „deploy it“: https://infooperate.pages.dev/havemercitrades/

Kontakt: merci@havemercitrades.com (vom Nutzer aus seiner Liste, 29.09.2026). Achtung: die Website havemercitrades.com ist offline (Shopify-Store geschlossen); die E-Mail-Domain hat aktive MX-Einträge (Google Workspace, geprüft 29.09.2026).

Seiten: `index.html` (Pitch), `funnel/`, `funnel/thank-you/`, `emails/`, `ads/` (Englisch). Texte nur in `content.json` ändern, dann `python3 _shared/build.py havemercitrades`.

## Offene `[CONFIRM]`-Stellen (intern)

1. Instagram 24,1K aus der Nutzer-Tabelle; Instagram-API rate-limitiert.
2. Mighty-Networks-Community: Preis/Pläne hinter Bot-Check.
3. Ob die Mentorship „small group“ ist (aus „3 filled, 2 left“ abgeleitet) und ob Live-NY-Sessions Teil der Mentorship sind.
4. Pronomen/Anrede: Seiten und Mails sprechen Merci in der 1. Person bzw. mit Namen an; keine Pronomen verwendet.
5. Markenfarben aus Banner/Avatar abgeleitet (Akzent abgedunkelt).
6. Meta Ad Library nicht geprüft.
7. **Compliance USA:** FTC, CFTC/NFA („trades called live“ in der Community). Vor Ads rechtlich prüfen.
8. (erledigt) MX-Einträge vorhanden.

## Vorgeschlagene Standardwerte auf den Seiten

| Seite | Vorschlag |
|---|---|
| Funnel · Inhalt | 7 Wochen Live-Klassen, Hausaufgaben nach jeder Klasse (aus ihrem Formular), Live-Nasdaq-Sessions, Ebook Vol. 3 (aus ihrem $550-Angebot), Trading-Plan + Journal, Community |
| Funnel · Methode | 4 Säulen (Structure, Setup, Risk, Reflection) aus ihren YouTube-Titeln und Shorts |
| Funnel · Bewerbung | 6 Fragen, angelehnt an ihr JotForm; Not-a-fit bei „No“ zu Hausaufgaben, Risikokapital, Investition |
| E-Mails | Call 20–30 Minuten; Hinweis auf gefälschte Accounts und „nie per DM zahlen“ |
| Ads | keine Einkommenszahlen, Risikohinweis im Bild |

## Offene `{{SWAP}}`-Stellen

Hinweis: Das Pitch-Video steht für ihre VSL (Thumbnail ihres neuesten Uploads). Kein offener Punkt.

- Funnel: Mercis Mentorship-VSL
- Funnel · Students: 3 Schülergeschichten (keine veröffentlichten Ergebnisse gefunden)

## QA

- Kontrast Funnel-Marke (hell): Text 12,7:1, Muted 6,5:1, Akzent auf Creme 5,5:1, Button-Text 5,5:1
- 375 px / 1440 px: kein horizontales Scrollen auf allen 5 Seiten; keine kaputten internen Links
- Drittanbieter: nur Calendly auf der Pitch-Seite
- Kein `[CONFIRM]` auf den Seiten
- Formular: qualifiziert → Buchung; „No“ bei Hausaufgaben, Risikokapital oder Investition → Not-a-fit
- Story: 386 px frei für Sticker
