# Zusammenfassung zur Kurzarbeit — Computer Vision

**Kurzarbeit am Di, 10.11.2026** · 20 Minuten · Taschenrechner erlaubt · Stoff: DS 03 bis DS 05

Zum Üben: das Übungsblatt zur Kurzarbeit im selben Ordner — dieselben Aufgabentypen, Lösungen am Ende.

---

## 1 Graubild und Histogramm (DS 03)

- Ein Graubild ist eine Matrix aus Grauwerten von **0 (schwarz) bis 255 (weiß)** — 8 Bit je Pixel.
- Eine Stelle heißt (*y*, *x*): **erst die Zeile, dann die Spalte**. Gezählt wird ab 0.
- Das **Histogramm** zählt, wie viele Pixel jeden Grauwert haben. Ein Berg ist eine große Fläche ähnlicher Helligkeit.
- **Mittelwert** = wie hell das Bild ist. **Streuung** = wie breit das Histogramm ist, also wie viel Kontrast es hat.

---

## 2 Punktoperationen: *B* = *c* · *A* + *d* (DS 04)

Jeder Pixel wird für sich umgerechnet, die Nachbarn spielen keine Rolle.

| | wirkt auf | im Histogramm |
|---|---|---|
| **+ *d*** | nur den Mittelwert: + *d* | der Berg wandert, die Breite bleibt |
| **· *c*** | Mittelwert · *c* und Streuung · *c* | der Berg wird breiter und wandert mit |

**Mittelwert und Streuung einer Zielaufnahme treffen — immer in dieser Reihenfolge:**

```
1.  c = Streuung Ziel : Streuung A
2.  d = Mittelwert Ziel − c · Mittelwert A
```

Erst *c*, weil nur *c* die Streuung ändert. Dann schiebt *d* den Mittelwert zurecht.

Beispiel: *A* hat Mittelwert 30 und Streuung 12, das Ziel 120 und 36.
*c* = 36 : 12 = 3, *d* = 120 − 3 · 30 = 30, also *B* = 3 · *A* + 30.

Häufiger Fehler: *d* = 120 − 30 — dabei fehlt das *c*.

**Abschneiden (8 Bit):** Was unter 0 fällt, wird 0, was über 255 steigt, wird 255. Im Beispiel wird ab dem Grauwert 76 abgeschnitten (3 · 76 + 30 = 258 → 255). Das lässt sich **nicht rückgängig machen**: Verschiedene Grauwerte landen alle auf 255, welcher Pixel welchen Wert hatte, steht nirgends mehr.

---

## 3 Schwelle und Otsu (DS 04)

- **Maske:** Pixel heller als die Schwelle → weiß (255), sonst schwarz (0).
- **Otsu** sucht die Schwelle selbst. Das klappt, wenn das Histogramm **zwei Berge mit einem Tal** hat (Untergrund und Bauteil): Die Schwelle landet im Tal.
- Otsu taugt nicht, wenn Bauteil und Untergrund gleich hell sind — zum Beispiel, wenn der Untergrund ausgebrannt ist (großer Berg bei 255). Dann gibt es kein Tal zwischen ihnen.

**Die Schwelle wird mitgerechnet.** Nach *B* = *c* · *A* + *d* mit *c* > 0 bleibt jeder hellere Pixel heller — die Reihenfolge ändert sich nicht. Dieselbe Maske erhält man deshalb mit der Schwelle *c* · *t* + *d*. Beispiel: Schwelle 40 in *A* → 3 · 40 + 30 = 150 in *B*.

**Wann es keine Schwelle gibt (Streiflicht):** Die gemessenen Pixel der Größe nach ordnen und mit B (Bauteil) und U (Untergrund) beschriften.

```
U 60  <  B 110  <  U 160  <  B 210
```

Wechseln sich B und U ab, gibt es keine Schwelle: Damit B 110 weiß wird, muss sie unter 110 liegen, damit U 160 schwarz wird, über 160 — beides zugleich geht nicht.

**Keine Punktoperation hilft dagegen:** Mit *c* > 0 bleibt die Reihenfolge, auch wenn Werte bei 0 oder 255 abgeschnitten werden. Eine Punktoperation kennt nur den Wert eines Pixels, nicht seinen Ort.

---

## 4 Faltung (DS 05)

**So wird gerechnet:** Den Kern mit seiner Mitte auf die Stelle legen, so wie er dasteht. Jede Zahl des Bildes mit dem Gewicht darüber malnehmen, alle neun Produkte zusammenzählen.

Für die Stelle (*y* = 1, *x* = 1) ist das die Umgebung aus den Zeilen 0 bis 2 und den Spalten 0 bis 2.

```
Umgebung          Mittelwertkern        Sobel-x
10  20  30        1/9  1/9  1/9         -1   0   1
40  50  60        1/9  1/9  1/9         -2   0   2
70  80  90        1/9  1/9  1/9         -1   0   1
```

```
Mittelwertkern:  10 + 20 + … + 90 = 450,   450 · 1/9 = 50

Sobel-x, Zeile für Zeile:
  Zeile 0:   −1 · 10  +  0 · 20  +  1 · 30   =  20
  Zeile 1:   −2 · 40  +  0 · 50  +  2 · 60   =  40
  Zeile 2:   −1 · 70  +  0 · 80  +  1 · 90   =  20
  zusammen:                                     80
```

| Kern | rechnet | Ergebnis |
|---|---|---|
| **Mittelwert** | Durchschnitt der neun Nachbarn | glättet; kleine Unterschiede verschwinden |
| **Sobel-x** | rechts minus links, mittlere Zeile doppelt | groß an senkrechten Kanten, 0 auf gleichmäßiger Fläche; Minus heißt: nach rechts wird es dunkler |
| **Sobel-y** | unten minus oben, mittlere Spalte doppelt | groß an waagerechten Kanten |

---

## 5 Die Gewichtssumme (DS 05)

**Gewichtssumme** = alle Einträge des Kerns zusammengezählt.

- Mittelwertkern: 9 · 1/9 = **1** — die Frage „Wie hell ist es hier?"
- Sobel-x: −1 + 0 + 1 − 2 + 0 + 2 − 1 + 0 + 1 = **0** — die Frage „Wie verschieden ist es hier?"

| Das ganze Bild wird … | Ergebnis der Faltung | am Beispiel oben |
|---|---|---|
| **um *d* heller** | ändert sich um *d* · Gewichtssumme | + 20: Mittelwert 50 → 70, Sobel-x bleibt 80 |
| **mit *c* malgenommen** | wird *c*-mal so groß, egal welche Gewichtssumme | · 2: Mittelwert 50 → 100, Sobel-x 80 → 160 |

Darum sieht ein Kantenbild bei gleichmäßig hellerem Licht genauso aus wie vorher: Bei Gewichtssumme 0 fällt das Plus heraus.

---

## Das kann ich

- *c* und *d* aus Mittelwert und Streuung bestimmen — erst *c*, dann *d* — und begründen, warum nur *c* die Streuung ändert.
- Pixel mit *B* = *c* · *A* + *d* umrechnen und an 0 und 255 abschneiden; erklären, warum Abschneiden nicht umkehrbar ist.
- Eine Schwelle mitrechnen: *t* in *A* wird *c* · *t* + *d* in *B*.
- Am Histogramm begründen, ob Otsu eine brauchbare Maske liefert.
- An vier Pixeln zeigen, dass es keine Schwelle gibt, und begründen, warum keine Punktoperation hilft.
- Mittelwertkern und Sobel-x an einer Stelle von Hand rechnen, mit Rechenweg Zeile für Zeile.
- Die Gewichtssumme bestimmen und vorhersagen, was „heller" und „mal" mit dem Ergebnis machen.
