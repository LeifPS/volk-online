# Volk – Das Kartenspiel (online)

Browser-Version des Karten- und Brettspiels **Volk** – Grundspiel mit **11 Zeitaltern** (Antike bis Sternenzeitalter) und 11 Volkskarten je Volk. Die Erweiterungen *Götter & Glaube* und *Zivilisation* sind vorerst abgeschaltet.

- 🤖 Gegen den Computer (Leicht / Mittel / Stark)
- 🌐 Online gegen Menschen: **Raum-Code / Einladungslink** oder **Schnellsuche**, Computer füllt freie Plätze auf, Wiederverbinden nach Reload/Verbindungsabbruch
- 📜 Regeln, Bedienungshilfe und Karten-Lexikon im Spiel
- Pixel-Optik mit Stadtplan, Gebäuden, Land und Heer

## Aufbau

| Pfad | Inhalt |
|---|---|
| `public/` | die Website (statische Dateien) |
| `public/js/engine.js` | **Regel-Engine** – reine Logik, läuft im Browser *und* im Worker |
| `public/js/ki.js` | Computer-Gegner |
| `public/js/ui.js` | Spieltisch (Stadtplan, Hand, Kampf-/Blockfenster) |
| `public/js/online.js` | Lobby, Raum-Code, Schnellsuche, Wiederverbinden |
| `public/data/` | Kartensatz (`satz.json`) und Pixel-Sprites (`sprites.json`) |
| `src/worker.js` | Cloudflare Worker: leitet WebSockets in Räume, Schnellsuche |
| `src/raum.js` | Durable Object „Raum“: Lobby, maßgeblicher Spielzustand, Computer-Spieler, Vertretung bei Abwesenheit |
| `src/lobby.js` | Durable Object „Lobby“: offene Schnellsuche-Räume |
| `tests/` | `selfplay.mjs` (Computer gegen Computer), `online.test.mjs` (ganze Online-Partie gegen den lokalen Worker) |

Der Server ist maßgeblich: Jeder Zug wird dort mit derselben Engine geprüft. Spieler sehen nur ihre eigenen Handkarten (Gegner-Hände und Stapel werden vor dem Senden entfernt). Ist ein Mensch länger als 40 s getrennt, spielt der Computer seinen Zug; wer als Verteidiger 90 s nicht blockt, wird automatisch verteidigt.

## Entwickeln

```bash
npm install
npm run dev          # http://localhost:8787 (Website + Online-Räume lokal)
npm test             # Selbsttest Computer gegen Computer
node tests/online.test.mjs localhost:8787   # Online-Partie gegen den laufenden Dev-Server
```

## Veröffentlichen (Cloudflare Workers)

```bash
npx wrangler login
npm run deploy
```

Oder im Cloudflare-Dashboard: *Workers & Pages → Create → Import a repository* → `volk-online` auswählen; Build-Befehl leer, Deploy-Befehl `npx wrangler deploy`. Die Durable Objects (`Raum`, `Lobby`) legt die Migration in `wrangler.jsonc` beim ersten Deploy an (SQLite-Variante, läuft auch im Free-Tarif).

## Karten & Oberfläche

Die Karten auf dem Tisch sind **1:1 die gedruckten Karten** des Kartenspiels: `public/karten/<id>.webp` (Vorderseiten, Rückseiten `rueck_*`, Volkstafeln `tafel_<volk>`, Religionstafeln `reltafel_<id>`). Erschöpfte Einheiten liegen gedreht wie auf dem Tisch; auf der Volkstafel sitzen Herz-, Kultur- und Zeitalter-Marker an den echten Positionen. Symbole sind selbst gepixelt (`public/js/sprites.js`), Schrift: Pixelify Sans und Silkscreen (OFL).
