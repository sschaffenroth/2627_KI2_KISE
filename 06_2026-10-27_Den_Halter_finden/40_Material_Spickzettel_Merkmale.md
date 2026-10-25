# Werkzeugkasten — Den Halter finden

Hier stehen Werkzeuge, keine Lösungen. Welche ihr für einen Auftrag braucht und in welcher Reihenfolge, entscheidet ihr selbst. In den Beispielen heißen die Bilder `farbe`, `grau`, `glatt` und `maske` — setzt eure eigenen Namen ein.

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
```

---

## Aus DS 02 bis DS 05

| Werkzeug | Was es tut |
|---|---|
| `farbe = cv2.imread("datei.jpg")` | lädt eine Aufnahme in Farbe — OpenCV speichert sie als Blau, Grün, Rot |
| `farbe = farbe[Y0:Y1, X0:X1]` | schneidet einen Ausschnitt aus: erst Zeilen, dann Spalten |
| `grau = cv2.cvtColor(farbe, cv2.COLOR_BGR2GRAY)` | macht aus dem Farbbild ein Graubild |
| `np.ones((n, n)) / (n * n)` | Glätten: der Mittelwertkern, n × n |
| `schwelle, maske = cv2.threshold(bild, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)` | Otsu: Der Rechner sucht die Schwelle und gibt sie mit der Maske zurück |
| `(maske > 0).sum() / maske.size * 100` | Anteil weiß in Prozent |
| `plt.imshow(bild, cmap="gray", vmin=0, vmax=255)` und `plt.show()` | zeigt ein Graubild oder eine Maske an |

## Glätten — diesmal für Otsu

```python
glatt = cv2.filter2D(grau, -1, np.ones((9, 9)) / 81)
```

| Teil des Befehls | Bedeutung |
|---|---|
| `grau` | das Bild, das geglättet wird |
| `-1` | das Ergebnis hat dieselbe Art wie das Original: ganze Zahlen von 0 bis 255 — so nimmt Otsu es an |
| `np.ones((9, 9)) / 81` | der 9 × 9-Mittelwertkern |

In DS 05 stand hier `cv2.CV_64F`, weil Sobel Minuszahlen liefert. Ein Mittelwert von Grauwerten bleibt immer zwischen 0 und 255 — mit `-1` geht nichts verloren.

## Umrisse finden — neu

```python
konturen, _ = cv2.findContours(maske, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

`cv2.findContours` sucht in einer Maske jede zusammenhängende weiße Fläche und gibt ihren **Umriss** (ihre **Kontur**) als Liste von Randpunkten zurück. Heraus kommt eine Liste solcher Umrisse. Der Unterstrich `_` nimmt die zweite Rückgabe auf, die hier nicht gebraucht wird.

| Teil des Befehls | Bedeutung |
|---|---|
| `maske` | eine Maske aus 0 und 255, so wie `cv2.threshold` sie liefert |
| `cv2.RETR_EXTERNAL` | nur die äußeren Umrisse — Löcher wie eine Bohrung zählen nicht als eigener Umriss |
| `cv2.CHAIN_APPROX_SIMPLE` | gerade Randstücke werden nur mit Anfang und Ende gespeichert — spart Punkte, ändert nichts an der Form |

| Werkzeug | Was es tut |
|---|---|
| `len(konturen)` | wie viele Umrisse es sind |
| `groesster = max(konturen, key=cv2.contourArea)` | der Umriss mit der größten Fläche: `max` misst mit `cv2.contourArea` jeden Umriss der Liste und gibt den größten zurück |
| `cv2.contourArea(groesster)` | die Fläche, die ein Umriss einschließt, in Pixeln |

## Ins Farbfoto zeichnen — neu

```python
cv2.drawContours(farbe, [groesster], -1, (0, 128, 255), 8)
```

| Teil des Befehls | Bedeutung |
|---|---|
| `farbe` | das Bild, in das gezeichnet wird — es wird dabei verändert |
| `[groesster]` | eine Liste der Umrisse, die gezeichnet werden; ein einzelner Umriss steht in eckigen Klammern |
| `-1` | alle Umrisse dieser Liste zeichnen |
| `(0, 128, 255)` | die Farbe als Blau, Grün, Rot: Orange |
| `8` | die Linienstärke in Pixeln |

### Ein Farbfoto anzeigen

```python
plt.imshow(cv2.cvtColor(farbe, cv2.COLOR_BGR2RGB))
plt.show()
```

In der ersten Zeile stecken **zwei Befehle in einem**. Python rechnet von innen nach außen:

| Teil des Befehls | Bedeutung |
|---|---|
| `cv2.cvtColor(farbe, cv2.COLOR_BGR2RGB)` | **1. Farben tauschen:** macht aus Blau, Grün, Rot die Reihenfolge Rot, Grün, Blau — so erwartet sie matplotlib. Das Ergebnis ist ein neues Bild, `farbe` selbst bleibt, wie es war |
| `plt.imshow(…)` | **2. Anzeigen:** zeichnet dieses getauschte Bild |

Hier steht **kein** `cmap="gray"`, und das ist richtig so: Ein Farbbild hat für jeden Pixel drei Werte und bringt seine Farben selbst mit. `cmap` und `vmin`/`vmax` braucht nur ein Graubild oder eine Maske mit einem Wert je Pixel — bei einem Farbbild übergeht matplotlib sie.

Wer es lieber in zwei Schritten schreibt:

```python
rgb = cv2.cvtColor(farbe, cv2.COLOR_BGR2RGB)
plt.imshow(rgb)
```

Der Umriss liegt nur dann richtig, wenn Farbfoto und Maske **denselben** Ausschnitt haben.

## Vier Aufnahmen in einem Fenster

| Werkzeug | Was es tut |
|---|---|
| `bildpfad = ["…misch….jpg", "…hell….jpg", "…seitlich….jpg", "…dunkel….jpg"]` | die vier Dateinamen in einer Liste |
| `for i in range(1, 5):` | `i` ist nacheinander 1, 2, 3, 4 — was eingerückt steht, passiert für jedes `i` |
| `bildpfad[i - 1]` | der Dateiname Nummer `i` — die Liste beginnt bei 0 |
| `plt.subplot(2, 2, i)` | das Fenster wird in 2 × 2 Felder geteilt; das nächste `plt.imshow` zeichnet ins Feld Nummer `i` |
| `plt.title("Text")` | eine Überschrift über das Feld |
| `str(zahl)` | macht aus einer Zahl Text, zum Beispiel für `plt.title(bildpfad[i - 1] + "  " + str(flaeche))` |
| `print(bildpfad[i - 1], schwelle, len(konturen), flaeche)` | gibt mehrere Werte in einer Zeile aus |

---

## Keine eigenen Aufnahmen?

Ladet im Kurs-Repository im Ordner `03_2026-10-06_Histogramm_Farbraeume` die Datei `sys03_notfall.zip` herunter und entpackt sie in den Ordner eures Skripts. Die Dateien heißen dann `notfall/00_halter_hell_01.jpg`, `…_seitlich_01.jpg`, `…_misch_01.jpg` und `…_dunkel_01.jpg`. Ein passender Ausschnitt: Zeilen 185 bis 790, Spalten 220 bis 1100.

Der Ausschnitt ist wichtig: Ohne ihn ist in `misch` die Tischplatte oben im Bild die größte weiße Fläche.

---

## Wenn etwas nicht geht

| Meldung oder Bild | Lösung |
|---|---|
| Otsu meldet einen Fehler (`THRESH_OTSU mode` … `CV_64F`) | Das Bild hat Kommazahlen. Beim Glätten `-1` statt `cv2.CV_64F` schreiben |
| `findContours` meldet einen Fehler (`Unsupported format` oder `CV_8UC1`) | Die Maske muss aus `cv2.threshold` kommen, nicht aus einem Vergleich wie `bild > 150` |
| `max()` meldet `empty` (`arg is an empty sequence` oder `iterable argument is empty`) | Die Liste der Umrisse ist leer: In der Maske ist kein einziger weißer Pixel. Maske anzeigen |
| Der Umriss sitzt verschoben neben dem Halter | Farbfoto und Maske haben nicht denselben Ausschnitt |
| Der Umriss ist blau statt orange, das Foto sieht bläulich aus | Beim Anzeigen fehlt `cv2.cvtColor(farbe, cv2.COLOR_BGR2RGB)` |
| Der Umriss geht um das ganze Bild oder um die Tischplatte | Ausschnitt fehlt — oder der Untergrund ist in der Maske weiß. Maske anzeigen |
| Euer Bauteil ist dunkel auf hellem Grund, und der Umriss geht um den Untergrund | `cv2.THRESH_BINARY_INV` statt `cv2.THRESH_BINARY`: Dann wird weiß, was dunkler ist als die Schwelle |
| Jedes Feld zeigt dasselbe Bild | In der Schleife steht noch der feste Dateiname statt `bildpfad[i - 1]` |
| Es öffnen sich vier Fenster nacheinander | `plt.show()` ist eingerückt — es gehört nach der Schleife |
| In einem Feld sind die Umrisse aus mehreren Durchläufen | Das Farbfoto wird in der Schleife nicht neu geladen |
| `'NoneType' object …` | Dateiname falsch, oder in VS Code ist nicht der Ordner mit euren Bildern geöffnet |
| `name 'np' is not defined` | `import numpy as np` fehlt oben im Skript |
