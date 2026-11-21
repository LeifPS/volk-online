# Entscheidungen: 11 Zeitalter im Grundspiel

Stand: 21.11.2026. Wird mit jeder Stufe ergänzt.

## Vorgaben von Leif (haben Vorrang vor dem Auftrag)
- Zukunft ist **keine Erweiterung**. Das Grundspiel hat jetzt 11 Zeitalter.
- Die Volkskarten sind fest im Grundspiel. Jedes Volk hat 11 Volkskarten (je Zeitalter eine). 20 sind neu (4 je Volk).
- Die Erweiterungen „Zivilisation“ und „Götter & Glaube“ sind erstmal **nicht spielbar** (nicht im Menü, nicht online). Code und Daten bleiben unangetastet im Repo liegen, damit sie später zurückkommen können. Künftig gehört alles ins Grundspiel.
- Die Zeitalter-VII-Karten geben wieder Wissen (Rechenzentrum W4, Raumfahrtzentrum K3+W3, Internationale Raumstation K3+W3+Ziehen 1, Himmelsbahnhof W3+K3).
- Alle neuen Karten liegen in einem neuen **Stapel IV** (Zeitalter VIII–XI).
- Neue Land-Rohstoffe: Seltene Erden, Deuterium, Titan, Helium-3. Antimaterie gibt es nur als Kartentext (Antimaterie-Rakete, Antimaterie-Fabrik), nicht als Land.
- Der Kartengenerator liegt jetzt im Repo unter `tools/karten`. Die Echtzeit-Repos volk, volk2, volk3 wurden nicht angefasst.

## Die neuen Zeitalter
| Nr. | Name | Farbe | Stadt-Stil |
|---|---|---|---|
| VIII | KI-Zeitalter | #5b8cff | Glastürme mit Dachgärten |
| IX | Fusionszeitalter | #f2a33a | weiße Kuppeln mit Lichtbändern |
| X | Weltraumzeitalter | #8e7cc3 | Raumhafen, Aufzugsmast, Habitat-Kuppeln |
| XI | Sternenzeitalter | #e6eef7 | Kristalltürme |

Technisch Zeitalter-Index 7 bis 10 (bisher 0 bis 6).

## Grafiken
Alle neuen Grafiken sind selbst gezeichnet (Pixel für Pixel per Code, `tools/karten/gen/zukunft_spr.py` und `zukunft_spr2.py`), nichts kopiert oder KI-generiert. 25 Einheiten, 21 Gebäude, 4 Wunder, 4 Rohstoffe, 20 Volkskarten-Motive, 12 Stadtbilder (je Zeitalter 3 Größen), 4 Zeitalter-Symbole. Stil: 16x16- bis 32x32-Pixel, Kontur, wenige Farben, wie die bestehenden Karten.

## Karten (Stapel IV)
- 25 Einheiten (1 Kopie, Exoskelett-Infanterie 2), 21 Gebäude, 19 Land-Karten, 4 Wunder, 20 Volkskarten.
- Stärken steigen etwa um 2 je Zeitalter weiter (VIII: 11–14, IX: 13–17, X: 14–17, XI: 18–22). Kosten ebenso (Einheiten 12–24, Gebäude 15–30).
- Jede Einheit mit Rohstoff-Symbolen braucht höchstens zwei neue/alte Rohstoffe. Raumschiffe brauchen ein Flugfeld (der Raumhafen zählt als Flugfeld).

## Zahlen (endgültig)
- Aufstieg kostet 6, 8, 10, 12, 14, 16, **18, 20, 22, 24** Gold.
- Kultursieg: **28** Kultur (vorher 12). Der Auftrag nannte 16; das beendete die Partien aber vor den neuen Zeitaltern (siehe Balance).
- Wissenschaftssieg: Der „Aufstieg“ aus dem Sternenzeitalter (XI) kostet pauschal **24** Gold und gewinnt. Eine Spielerin, die in dieser Runde erst aufgestiegen ist, kann frühestens in der nächsten Runde gewinnen.
- Stapel: I = Zeitalter I–II, II = III–IV, III = V–VII, IV = VIII–XI.
- Handlimit und Startwerte unverändert (3 Gold, 5 Karten + Volkskarte I, 25 Lebenspunkte).

## Karten je Zeitalter (Anzahl verschiedener Karten, ohne Wunder und Volkskarten)
| Zeitalter | Einheiten | Gebäude | Land |
|---|---|---|---|
| VIII KI | 6 | 6 | (Land-Karten von Stapel IV, siehe unten) |
| IX Fusion | 7 | 5 | – |
| X Weltraum | 7 | 6 | – |
| XI Sterne | 5 | 4 | – |
Stapel IV insgesamt 66 Karten (mit Kopien), darunter 19 Land-Karten mit den vier neuen Rohstoffen. Dazu 12 Weltwunder (4 neu: Weltgehirn, Künstliche Sonne, Weltraumaufzug, Sternenarche) und 55 Volkskarten (11 je Volk).

## Balance (Selbstspiel, Computer gegen Computer)
Methode: `node tests/bilanz.mjs 200 mittel 2,3,4`, je 200 Partien, Stufe „mittel“, zufällige Völker.

| Spieler | Median Runden | Kultur | Wissenschaft | Eroberung | Höchstes Zeitalter (Median) |
|---|---|---|---|---|---|
| 2 | 16 | 99 | 22 | 79 | VII |
| 3 | 19 | 115 | 70 | 15 | X |
| 4 | 20 | 102 | 85 | 13 | XI |

- Alle Partien enden regulär (0 Fehler, 0 zu lange). Das alte Spiel dauerte 10–11 Runden; jetzt 16–20 Runden, also **mehr als 50 % länger** (Abweichung vom Auftrag, bewusst: sonst kommen die neuen Zeitalter nie vor).
- Kultursieg 16 (Auftrag) ließ die meisten Partien enden, bevor jemand Zeitalter VIII erreichte. Kultur 28 und Wissenschaft 24 sind der Kompromiss, bei dem zu dritt und zu viert die neuen Zeitalter wirklich gespielt werden.
- Volks-Siegquoten: zu viert 18–35 % (ideal 25 %), zu dritt 26–40 % (ideal 33 %), zu zweit 41–58 % (ideal 50 %). Kein Volk fällt aus.
- Computer „stark“ gegen „mittel“ (nach Abstimmung mit `tests/tune.mjs`): gewinnt 72 % (2 Spieler), 43 % (3), 49 % (4). Zufall wäre 50 / 33 / 25 %.
- Schwäche: Zu zweit gewinnt die Eroberung häufig, weil zwei Spieler kaum bis in die neuen Zeitalter kommen. Das Einkommen wächst spät sehr stark (etwa +50 Gold je Runde in Runde 18), dadurch wird der Wissenschaftssieg nach Erreichen von XI fast automatisch.
- Karten, die der Computer „mittel“ nie spielt: Quantenrechner, KI-Labor, Orbitalstation, Weltgehirn, Sternenarche, Antimaterie-Rakete, Sternenkreuzer, Orbitalkanone (der Computer bewertet Wissen und Spezialeffekte spät im Spiel gering). Das ist eine Schwäche der KI, nicht der Karten; Menschen können sie nutzen. 42 von 50 neuen Karten werden zu dritt/viert gespielt.

## Erweiterungen
Götter & Glaube und Zivilisation sind vorerst aus: nicht im Menü, nicht online (Engine erzwingt `rel:false, civ:false`). Code, Daten und Tests bleiben im Repo und sind dormant.

## Commit-Hinweis
Der Commit 8f14961 (Generator ins Repo, Grafiken, Daten) trägt „Kleines Update:“, obwohl er für Spieler unsichtbar war; richtig wäre „Patch:“ gewesen. Nicht umgeschrieben.

## Tests
`tests/engine.test`, `wahl.test`, `wissen.test`, `volkkarte.test`, `civ.test`, `zukunft.test`, `regression.mjs` (feste Seeds), `validiere.mjs`, `bilanz.mjs`, `stark.mjs`. `online.test.mjs` braucht den lokalen Worker (wrangler) und wurde nicht ausgeführt, außer wie im Abschlussbericht vermerkt.
