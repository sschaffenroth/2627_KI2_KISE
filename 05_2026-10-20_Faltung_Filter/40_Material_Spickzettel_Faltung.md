# Werkzeugkasten — Faltung und Filter

Hier stehen Werkzeuge, keine Lösungen. Welche ihr für einen Auftrag braucht und in welcher Reihenfolge, entscheidet ihr selbst. In den Beispielen heißt das Bild `bild` — setzt eure eigenen Namen ein.

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
```

Neu ist `numpy`: Damit schreibt ihr einen Kern als Matrix. Ein Kern *K* ist eine kleine Matrix aus Gewichten, ein Ausschnitt des Bildes eine kleine Matrix aus Grauwerten — wie die Matrix *A* in DS 04.

---

## Aus DS 04

| Werkzeug | Was es tut |
|---|---|
| `bild = cv2.cvtColor(cv2.imread("datei.jpg"), cv2.COLOR_BGR2GRAY)` | lädt eine Aufnahme als Graubild |
| `bild[Y0:Y1, X0:X1]` | schneidet einen Ausschnitt aus: erst Zeilen, dann Spalten |
| `plt.imshow(bild, cmap="gray", vmin=0, vmax=255)` und `plt.show()` | zeigt ein Graubild an |
| `schwelle, maske = cv2.threshold(bild, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)` | Otsu: Schwelle und Maske |
| `maske.sum() / maske.size * 100` | Anteil weiß in Prozent (bei einer Maske aus Otsu: `(maske > 0).sum()`) |
| `for name in NAMEN:` | dasselbe für mehrere Aufnahmen — was eingerückt steht, passiert für jede |

---

## Eine Stelle und ihre Nachbarn

Zeigt ein Bild mit `plt.imshow` an und fahrt mit der Maus darüber: Unten im Fenster stehen `x`, `y` und der Grauwert an dieser Stelle.

| Werkzeug | Was es tut |
|---|---|
| `bild[Y, X]` | der Grauwert an einer Stelle — erst `y`, dann `x` |
| `bild[Y - 1:Y + 2, X - 1:X + 2]` | die 3 × 3-Nachbarschaft um die Stelle: die Zeile darüber, die Stelle, die Zeile darunter, genauso bei den Spalten |
| `feld.mean()` | Mittelwert eines Feldes |

## Einen Kern schreiben

```python
kern = np.array([[0, 0, 0],
                 [0, 1, 0],
                 [0, 0, 0]])
```

| Werkzeug | Was es tut |
|---|---|
| `np.array([[…], […], […]])` | eine Matrix, Zeile für Zeile — jede Zeile in eckigen Klammern |
| `np.ones((n, n))` | ein Kern aus n × n Einsen |
| `kern / 9` | teilt jeden Eintrag durch 9 |
| `kern.sum()` | die Gewichtssumme: alle Einträge zusammengezählt |

Auch eine Nachbarschaft aus einer Aufgabe könnt ihr so als `np.array` abschreiben.

## Falten

| Werkzeug | Was es tut |
|---|---|
| `(feld * kern).sum()` | Faltung an **einer** Stelle: Feld für Feld malnehmen (das `*` aus DS 04: Eintrag für Eintrag), alles zusammenzählen. `feld` und `kern` müssen gleich groß sein |
| `cv2.filter2D(bild, cv2.CV_64F, kern)` | Faltung an **jeder** Stelle: Heraus kommt ein neues Bild |

| Teil des Befehls | Bedeutung |
|---|---|
| `bild` | das Bild, das gefaltet wird |
| `cv2.CV_64F` | das Ergebnis in Kommazahlen — auch unter 0 und über 255, wie mit `60.0` in DS 04 |
| `kern` | der Kern |

Ein großer Kern braucht einen Moment: Bei 151 × 151 rechnet der Rechner ein, zwei Sekunden.

## Kerne, die ihr kennt

| Name | Kern |
|---|---|
| Mittelwert, 3 × 3 | neun Einsen, geteilt durch 9 — euer Aufwärmen |
| Glätten, n × n | `np.ones((n, n)) / (n * n)` — der Mittelwert einer größeren Umgebung |
| Sobel-x | `[[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]` — rechts minus links, die Mitte doppelt |
| eure Erfindung | aus Auftrag E: jede der neun Zahlen bekommt ein Gewicht |

Die **Gewichtssumme** (`kern.sum()`) verrät, was ein Kern fragt: 1 — wie hell ist es hier? 0 — wie verschieden ist es hier?

## Mit Bildern rechnen und vergleichen

| Werkzeug | Was es tut |
|---|---|
| `abs(bild)` | macht aus jeder Minuszahl eine Pluszahl: Aus −178 wird 178 |
| `bild + 60.0` · `bild * 2.0` | mit einer Zahl rechnen, wie in DS 04 — mit Punkt, damit nichts überläuft |
| `bild_a + bild_b` | zwei gleich große Bilder Pixel für Pixel zusammenzählen — genauso `-`, `*` |
| `bild_a > bild_b` | Maske: True, wo `bild_a` heller ist als `bild_b` an derselben Stelle |
| `bild_a > bild_b + 10.0` | dasselbe, aber erst ab 10 Grauwerten Unterschied |
| `bild.mean()` · `bild.std()` | Mittelwert · Streuung |

Ein Bild mit Minuszahlen zeigt `plt.imshow(…, vmin=0, vmax=255)` dort schwarz.

## Für „Wer noch Zeit hat"

| Name | Kern |
|---|---|
| Schärfen | `[[0, -1, 0], [-1, 5, -1], [0, -1, 0]]` |

---

## Keine eigenen Aufnahmen?

Ladet im Kurs-Repository im Ordner `03_2026-10-06_Histogramm_Farbraeume` die Datei `sys03_notfall.zip` herunter und entpackt sie in den Ordner eures Skripts. Die Dateien heißen dann `notfall/00_halter_hell_01.jpg`, `…_seitlich_01.jpg`, `…_misch_01.jpg` und `…_dunkel_01.jpg`. Ein passender Ausschnitt: Zeilen 185 bis 790, Spalten 220 bis 1100.

---

## Wenn etwas nicht geht

| Meldung oder Bild | Lösung |
|---|---|
| `name 'np' is not defined` | `import numpy as np` fehlt oben im Skript |
| Die Nachbarschaft hat nicht 3 × 3 Werte | Erst die Zeile, dann die Spalte. Die Maus zeigt `x` zuerst — im Skript kommt `y` zuerst |
| `operands could not be broadcast together` | `feld` und `kern` sind nicht gleich groß. Mit `.shape` prüfen |
| Die Faltung mit dem Mittelwertkern gibt eine viel zu große Zahl | Der Kern ist nicht durch die Anzahl seiner Einträge geteilt |
| Das Kantenbild ist fast schwarz, nur einzelne Linien | Die Minuszahlen werden schwarz angezeigt — nur die halbe Kante bleibt |
| Das Bild ist grau statt schwarz | `vmin=0, vmax=255` fehlt in `plt.imshow` |
| `-1` statt `cv2.CV_64F` geschrieben | Dann rechnet OpenCV in 0 bis 255 und schneidet alles unter 0 ab. `cv2.CV_64F` schreiben |
| `'NoneType' object has no attribute …` | Dateiname falsch, oder in VS Code ist nicht der Ordner mit euren Bildern geöffnet |
