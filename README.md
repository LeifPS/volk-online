# Volk – Das Kartenspiel (online)

Browser-Version des Karten- und Brettspiels **Volk** – Grundspiel plus die Erweiterungen *Volkskarten* und *Götter & Glaube*.

- Gegen den Computer spielen (Leicht / Mittel / Stark)
- Module frei kombinierbar
- Pixel-Optik mit Stadtplan, Gebäuden und Heer

## Entwickeln

```bash
npm install
npm run dev      # lokal unter http://localhost:8787
npm run deploy   # Cloudflare Workers
```

Regel-Engine: `public/js/engine.js` (reine Logik, läuft im Browser und später auf dem Server).
Computer-Gegner: `public/js/ki.js`. Selbsttest: `npm test` (Computer gegen Computer, alle Modul-Kombinationen).
