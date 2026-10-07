# HOUSE.md

Feste Daten, die bei jedem Funnel-Bau automatisch verwendet werden. Einmal ausfüllen, danach nicht mehr pro Creator wiederholen.

## Agentur / Operator

- Name: keiner (kein Agentur-/Markenname verwenden)
- Logo: keins (Pitch-Seite ohne Logo bauen)
- Website (falls vorhanden): [URL]

## Booking

- Calendly-Link: https://calendly.com/maliksmouni/30min

## Ton & Stil

- Bevorzugter Ton: [z. B. direkt, kein Fluff / warm und beratend / etc.]
- Anrede-Stil: [Du/Sie, Vorname/Nachname]

## Eigene Case Studies (echte, verifizierte Ergebnisse)

Trage hier nur Ergebnisse ein, die du tatsächlich belegen kannst (Name/Pseudonym des Kunden, Ergebnis, Zeitraum, ggf. Beweis-Link/Screenshot). Diese werden als Proof in jedem neuen Funnel wiederverwendet - NICHT für den jeweiligen Prospect selbst erfunden.

1. Kunde: Karl Pierre
   Angebot: Neues Info-Produkt
   Ergebnis: $10K
   Zeitraum: in 2 Tagen
   Kennzahl: $10K in 2 days
   Text: Launched a new info product and did $10K in sales in the first two days.
   Beweis: assets/cases/karl-pierre.jpg (Überweisung meines Anteils, $2,000, 9. April 2025)
   Bildausschnitt: 50% 22%

2. Kunde: Creator (Name nicht öffentlich)
   Angebot: Neues High-Ticket-Angebot
   Ergebnis: 6 qualifizierte Calls
   Zeitraum: an einem Tag
   Kennzahl: 6 qualified calls in 1 day
   Text: Launched a new high-ticket offer and booked six qualified sales calls in a single day.
   Beweis: assets/cases/high-ticket-calls.jpg (Kalender, August 2025)

3. Kunde: Kunde (Name nicht öffentlich)
   Angebot: Launch
   Ergebnis: €5.3K ($6.2K) Umsatz, €3.9K ($4.6K) Cash collected
   Zeitraum: in 8 Tagen (21.–28. August)
   Kennzahl: €5.3K revenue in 8 days
   Text: €5.3K ($6.2K) in revenue and €3.9K ($4.6K) cash collected in eight days.
   Beweis: assets/cases/client-launch.jpg (Sales- und Zahlungs-Screenshots)

(weitere nach Bedarf ergänzen)

## Design-Master (Pitch-Seite)

Umgesetzt in `_shared/pitch-master.css` (Stil-Referenz: phil-pitch.pages.dev). [CONFIRM], falls du andere Werte willst.

- Hintergrund: #f5f2ec (warmes Papier, feine diagonale Struktur)
- Text: #1b1917 / Sekundär #5f5850
- Akzentfarbe: #7c5a16 (Bronze)
- Fonts: Bricolage Grotesque (Headlines), Inter (Text), JetBrains Mono (Labels), selbst gehostet in `assets/fonts/` (OFL)
- Grundstil: hell/editorial, zentrierter Hero mit großem Video, nummerierte „Four things I noticed“-Karten, Deliverables als Browser-Vorschauen, Calendly-Karte, Sticky-„Book a call“

## Besuchs-Alarm (Discord / Telegram)

Öffnet jemand eine Pitch-Seite oder ein Deliverable auf infooperate.com (oder der alten Adresse infooperate.pages.dev), geht eine Nachricht an den eigenen Discord-Kanal (Webhook) und/oder Telegram-Bot (Name, Seite, Stadt/Land, Gerät, Quelle, Button zum Instagram-Profil). Einrichtung: Cloudflare Pages `infooperate` → Settings → Variables and secrets (Production): `DISCORD_WEBHOOK_URL` und/oder `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`. Eigene Geräte einmal mit `?me=1` öffnen. Selbsttest: `/{slug}/?alerttest={Discord-Webhook-ID oder Telegram-Chat-ID}`.

