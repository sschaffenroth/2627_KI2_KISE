# DS 03 — Arbeitsblatt

**Histogramm: Taugt die Aufnahme? · 06.10.2026**

---

## Vorbereitung — Python einrichten

Falls ihr Anaconda benutzt: Legt einmal die Umgebung [env] an.

```
conda create -n [env] python=3.13
conda activate [env]
conda install numpy opencv matplotlib
python -m pip install pyrealsense2
```

Danach in VS Code über **Datei → Ordner öffnen** einen eigenen Ordner für Skripte und Bilder öffnen.

---

## P1 — Die Aufnahmeserie (etwa 25 min)
Nehmt zuerst verschieden beleuchtete Bilder vom gleichen Objekt auf.

Das Aufnahmeskript `05_aufnahme.py` liegt im Kurs-Repository. Ladet es in euren Ordner. Wie ihr damit ein Bild aufnehmt, steht im Spickzettel unter „Bilder aufnehmen".

Nehmt euer Bauteil unter allen vier Beleuchtungen auf, ein Bild je Beleuchtung. Gespeichert wird über das Menü des Kamerafensters, jedes Bild unter seinem eigenen Dateinamen. Kamera und Bauteil bleiben an derselben Stelle.

| Beleuchtung | Licht |
|---|---|
| `hell` | Lampe direkt von vorn aufs Bauteil |
| `seitlich` | Lampe flach von der Seite, das Licht streift über die Oberfläche |
| `misch` | Lampe aus, nur das Licht im Raum: Tageslicht und Deckenlicht |
| `dunkel` | alle gleichzeitig, auf Ansage: Rollos zu, Licht aus, nur Restlicht |

> **Die Kamera klappt nicht?** Nehmt die Notfall-Serie — Spickzettel, Notfall.

---

## P2 — Euer Prüfprogramm (etwa 12 min)

Jetzt schreibt ihr selbst: ein neues Skript im Ordner eurer Bilder. Für die Schritte 1 bis 3 stehen die Befehle im Spickzettel unter derselben Nummer.

1. Ladet eure vier Aufnahmen und rechnet sie in Graustufen um.
2. Zeichnet die vier Histogramme in **ein** Diagramm, mit Legende.
3. Gebt für jede Aufnahme aus: Mittelwert, Streuung, Pixel bei 0, Pixel bei 255.

| Aufnahme | Mittelwert | Streuung | Pixel bei 0 | Pixel bei 255 |
|---|---|---|---|---|
| `hell` | | | | |
| `dunkel` | | | | |
| `seitlich` | | | | |
| `misch` | | | | |


---

## P3 — Clipping (etwa 5 min)

4. Erweitert euer Programm: Welcher **Anteil** der Pixel steht genau bei 0, welcher genau bei 255?

| Aufnahme | Anteil bei 0 in % | Anteil bei 255 in % |
|---|---|---|
| `hell` | | |
| `dunkel` | | |

Welche eurer Aufnahmen taugt am wenigsten — und warum hilft Nachbearbeitung da nicht?

---

## P4 — Euer Programm urteilt (nach Ansage)

5. Legt selbst Grenzen fest: Ab wann ist eine Aufnahme `ausgebrannt`, `zu dunkel` oder `flau`? 

Schreibt ein Programm, dass Aufnahmen automatisch auswertet, ob es zu dunkel, ausgebrannt, etc. ist.

Statt einer Datei kann euer Programm das Bild auch direkt von der Kamera holen — Spickzettel, „Die Kamera im eigenen Programm".

---

## P5 — Prüfungsformat: Kennwerte zuordnen (wer fertig ist)

> Von einem Bauteil wurden drei Aufnahmen gemacht, jede **1280 × 960 Pixel** in Graustufen, also **1 228 800 Pixel** je Bild.

| | Aufnahme A | Aufnahme B | Aufnahme C |
|---|---|---|---|
| Mittelwert | 126,0 | 221,4 | 28,7 |
| Streuung | 38,0 | 32,9 | 18,6 |
| Pixel mit Wert 0 | 570 | 0 | 103 770 |
| Pixel mit Wert 255 | 426 | 324 360 | 0 |

Bedingungen: **1** Baustrahler frontal · **2** Rollos zu, nur Restlicht · **3** Tageslicht plus Deckenleuchte

a) Ordnet zu und begründet jeweils mit **einer** Zahl: 1 → … weil … · 2 → … weil … · 3 → … weil

b) Anteil der geclippten Pixel bei B: … % bei C: … %

c) B hat eine **kleinere** Streuung als A. Ist B das gleichmäßigere Bild? Begründet.

d) Welche Aufnahme lässt sich durch Nachbearbeitung retten, welche nicht — und warum?

---

## Wer noch Zeit hat

- Nehmt euer **fehlerhaftes** Bauteil auf. Sieht man den Fehler im Histogramm?
- Nehmt den Untergrund **ohne** Bauteil auf, unter derselben Beleuchtung. Legt beide Histogramme übereinander: Welcher Berg gehört zum Untergrund, welcher zum Bauteil?
