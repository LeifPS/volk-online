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

## Zahlen
- Aufstieg kostet 6, 8, 10, 12, 14, 16, **18, 20, 22, 24**.
- Kultursieg: **16** (vorher 12).
- Wissenschaftssieg wandert ins **Sternenzeitalter (XI)**: Der „Aufstieg“ aus Zeitalter XI kostet 26 Gold und gewinnt das Spiel.
- Handlimit und Startwerte unverändert.

(Details zu Balance-Zahlen folgen nach den Selbstspiel-Läufen.)
