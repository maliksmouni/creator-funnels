# gocholive: Franklin Ovalles „Gocho“ (El Trading Club)

Aware-Outreach-Pitch für einen Call-Funnel (Rebuild des bestehenden GoHighLevel-Funnels für das „Programa de 0 a Trader“). Stand: 28.09.2026. Status: **live** seit 28.09.2026: https://infooperate.netlify.app/gocholive/.

Kontakt: franklin@eltradingclub.com (vom Nutzer per Screenshot geliefert, 28.09.2026). Auf eltradingclub.com (/privacy-policy, /terms-conditions) steht nur admin@eltrandingclub.com mit Tippfehler; diese Domain existiert nicht.

Seiten: `index.html` (Pitch, Englisch), `funnel/`, `funnel/thank-you/`, `emails/`, `ads/` (Spanisch über `content.json → ui`). Texte nur in `content.json` ändern, dann `python3 _shared/build.py gocholive`.

## Offene `[CONFIRM]`-Stellen (intern)

1. **Instagram-Zahl 81K** stammt nur aus einer Suchergebnis-Zusammenfassung (Instagram-API 401 / rate-limitiert). Eine ältere Drittseite nennt 54,6K. **Vor dem Versand auf dem Profil prüfen** und ggf. Beat 1 anpassen. Ebenso X 23,5K.
2. Bio-Links auf Instagram nicht gesehen (Rate-Limit). Führt die Bio auf eltradingclub.com?
3. Preis des Programms nicht öffentlich (Umfrage fragt Budget bis „Más de $3000“).
4. Gibt es schon Pre-Call-E-Mails/WhatsApp-Automationen? Auf der Seite sichtbar ist nur „Escríbenos al Whatsapp para confirmar la cita“.
5. Wer führt die Calls (Gocho oder ein Closer-Team)? Funnel sagt „el equipo de Gocho“.
6. Englischkenntnisse: Pitch-Seite ist Englisch (Template). Topstep-Feature spricht dafür. Ggf. DM auf Spanisch.
7. Markenfarben: aus dem CSS von eltradingclub.com; surface/line/muted abgeleitet.
8. Meta Ad Library: laufen Ads? (nicht geprüft, Login nötig)
9. **Compliance USA:** CFTC/NFA (Futures), FTC (Einkommensaussagen). Zielgruppe teils Lateinamerika. Vor Ads rechtlich prüfen.
10. gochotradereducation.com zeigt heute eine Glücksspielseite. Ob die Domain ihm gehörte, ist nicht belegt (Wayback offline). Nicht auf der Pitch-Seite; höchstens als Hinweis in der DM, nach Prüfung.
11. Seit ca. 8 Wochen kein neues YouTube-Video / kein Stream (Bucket „2 months ago“). Nicht auf der Pitch-Seite verwendet.

## Vorgeschlagene Standardwerte auf den Seiten

| Seite | Vorschlag |
|---|---|
| Funnel · Lead | Live-Trading statt Einkommenszahl: „Aprende a operar futuros del Nasdaq en vivo, con Gocho a tu lado.“ |
| Funnel · Inhalt | 1:1 seine 6 Programmpunkte von eltradingclub.com (nichts hinzugefügt) |
| Funnel · Methode | seine 3 Phasen, als 4 Säulen (Estudia, Valida, Opera en vivo, Fondeo con control) |
| Funnel · Bewerbung | 6 Fragen aus seiner Umfrage abgeleitet; „Not a fit“ bei minderjährig, „kein Risikokapital“, „nicht bereit zu investieren“ |
| Funnel · How it works | Call mit „el equipo de Gocho“ |
| E-Mail 4 | Call ca. 30 Minuten |
| Thank-you | „Nunca pedimos pagos por mensaje directo de Instagram o WhatsApp.“ |
| Ads | keine Einkommenszahlen, keine Knappheit, Risikohinweis im Bild |

## Offene `{{SWAP}}`-Stellen

Hinweis: Das Video auf der Pitch-Seite steht für seine VSL (Thumbnail seines neuesten Uploads). Das ist kein offener Punkt.

- Funnel: Gochos Programm-VSL
- Funnel · Alumnos: 3 Video-Testimonials von eltradingclub.com (Andreina D'Angelo, José Alejandro Pérez Conde, Wilmerson Serrano). Inhalte nicht angesehen, daher keine Aussagen übernommen.

## Template-Änderung

`_shared/build.py` hat jetzt `content.json → ui` (optionale Übersetzung aller festen Funnel-/Mail-/Ad-Labels + `lang`). Ohne `ui` bleibt alles Englisch wie bisher.

## QA

- Kontrast Funnel-Marke: Text 15:1, Muted 8,2:1, Gold auf Navy 8,1:1, Button-Text 8,1:1, Signal 12,3:1
- 375 px / 1440 px: kein horizontales Scrollen auf allen 5 Seiten; keine kaputten internen Links
- Drittanbieter: nur Calendly auf der Pitch-Seite
- Kein `[CONFIRM]` auf den Seiten
- Formular: qualifiziert → Buchung; „No“ bei Risikokapital → Not-a-fit
