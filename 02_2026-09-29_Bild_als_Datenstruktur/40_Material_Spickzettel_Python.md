# Spickzettel — Bilder mit NumPy und OpenCV

**DS 02 · Das Bild als Datenstruktur · 29.09.2026 · Klassensatz, bleibt bei euch**

Alle Befehle stehen fertig in `05_bildwerkstatt.py`. Hier steht, **was sie tun** — in
derselben Reihenfolge wie im Skript und auf dem Arbeitsblatt. Ganz hinten: Befehle zum
Ausprobieren, für die Hausaufgabe und was bei Fehlermeldungen hilft.

---

## Teil 0 — Die Werkstatt

### Drei Bibliotheken

```python
import cv2                          # OpenCV: laden, speichern, skalieren, Farben umrechnen
import numpy as np                  # das Zahlenfeld: auswählen, rechnen, zählen
import matplotlib.pyplot as plt     # der Bildschirm: Zahlen wieder als Bild zeigen
```

### a) Bild laden

```python
roh = cv2.imread("/content/bauteil.jpg")          # Colab
roh = cv2.imread(r"C:\Users\...\bauteil.jpg")     # lokal, mit r vor dem Pfad
```

Das Ergebnis ist ein NumPy-Array. Ist der Pfad falsch, gibt es **keine Fehlermeldung**,
sondern `None` — erst die nächste Zeile scheitert.

### b) Farben richtig stellen

```python
bild = cv2.cvtColor(roh, cv2.COLOR_BGR2RGB)
```

OpenCV speichert die drei Kanäle als **Blau, Grün, Rot**, alle anderen — auch `plt` — erwarten
**Rot, Grün, Blau**. Ohne diese Zeile wird Rost blau. Ab hier arbeitet ihr nur noch mit `bild`.

### Bild anzeigen

```python
plt.imshow(bild)                     # Farbbild (RGB)
plt.title("mein Bauteil")
plt.show()

plt.imshow(grau, cmap="gray")        # Graustufenbild: braucht eine Farbskala
plt.show()

plt.subplot(1, 2, 1); plt.imshow(bild_a)     # zwei nebeneinander: 1 Zeile, 2 Spalten, Bild 1
plt.subplot(1, 2, 2); plt.imshow(bild_b)     #                                        Bild 2
plt.show()
```

Die Achsen zeigen Zeilen- und Spaltennummern. Weg damit: `plt.xticks([])`, `plt.yticks([])`.
Im Skript erledigen das die Helfer `zeigen(bild, "Titel")` und
`vergleich((bild_a, "a"), (bild_b, "b"))`.

### c) Ein einzelner Pixel

```python
bild[y, x]          # zum Beispiel bild[100, 200]
```

**Zeile zuerst**, dann Spalte. Das Ergebnis sind drei Werte: **Rot, Grün, Blau**, je 0 bis 255.

### d) Einen Bereich setzen

```python
rot = bild.copy()                        # Kopie, sonst ändert ihr das Original mit
rot[400:600, 400:600] = [255, 0, 0]      # Rot, Grün, Blau
```

`400:600` heißt „von 400 bis vor 600".

### e) Wie groß ist das Bild? — die Felder von `bild`

| Befehl | liefert | Beispiel |
|---|---|---|
| `bild.shape` | Höhe, Breite, Kanäle | `(3000, 4000, 3)` |
| `bild.ndim` | Zahl der Achsen: 3 bei Farbe, 2 bei Grau | `3` |
| `bild.size` | **Zahl der Werte** = Höhe × Breite × Kanäle | `36000000` |
| `bild.dtype` | Datentyp jedes Werts; `uint8` heißt 0 bis 255 | `uint8` |
| `bild.nbytes` | Speicher in Byte; bei `uint8` gleich `size` | `36000000` |
| `bild.min()`, `bild.max()`, `bild.mean()` | kleinster, größter, mittlerer Wert | `0`, `255`, `115.0` |

**Die Größe messt ihr in dieser Stunde immer mit `size`** — genau so viele Zahlen muss das
Netz anfassen.

---

## Teil 1 — Ausschneiden

```python
ausschnitt = bild[Y:Y + 224, X:X + 224]
```

Ein Quadrat von 224 × 224 Pixeln, linke obere Ecke bei Zeile `Y`, Spalte `X`. Ragt es über
den Rand, wird es stillschweigend kleiner — `ausschnitt.shape` prüfen.

## Teil 2 — Skalieren

```python
klein = cv2.resize(bild, (224, 224))       # (Breite, Höhe) — andersherum als shape!
```

## Teil 3 — Kanäle: braucht ihr die Farbe?

Ein Farbbild sind **drei Zahlenfelder übereinander**, eins je Grundfarbe. Einzeln
angezeigt ist jedes ein Graubild: hell heißt „viel von dieser Farbe".

```python
bild[:, :, 0]        # nur Rot     (: heißt „alles": alle Zeilen, alle Spalten)
bild[:, :, 1]        # nur Grün
bild[:, :, 2]        # nur Blau
grau = cv2.cvtColor(bild, cv2.COLOR_RGB2GRAY)    # ein Wert je Pixel
```

Der Grauwert ist ein gewichteter Mittelwert: **0,299 · R + 0,587 · G + 0,114 · B**.
Beispiel Rostpixel [216, 151, 57]: 64,6 + 88,6 + 6,5 = 159,7 → **160**.
`grau.shape` hat nur noch zwei Zahlen — `size` ist ein Drittel.

**Die Frage dahinter:** Steckt euer Merkmal in der Farbe (Rost, Markierung) oder in Form und
Helligkeit (Riss, Bohrung, Kante)? Im ersten Fall kostet Grau das Merkmal, im zweiten nichts.

## Teil 4 — Bittiefe: wie viele Helligkeitsstufen braucht ihr?

Jeder Wert kann **256 Stufen** haben (0 bis 255), dafür braucht man **8 bit**. Weniger Stufen
heißt weniger bit je Wert:

| Stufen | 256 | 16 | 4 | 2 |
|---|---|---|---|---|
| bit je Wert | 8 | 4 | 2 | 1 |
| Breite einer Schublade | 1 | 16 | 64 | 128 |

**So rundet man auf 4 Stufen:** Die 256 Werte kommen in 4 Schubladen zu je 64. Jeder Wert
bekommt den Anfang seiner Schublade:

| Wert | 0 … 63 | 64 … 127 | 128 … 191 | 192 … 255 |
|---|---|---|---|---|
| wird zu | 0 | 64 | 128 | 192 |

```python
schritt = 256 // 4                        # 64 — Breite einer Schublade
vier = (grau // schritt) * schritt        # Beispiel 200:  200 // 64 = 3,  3 * 64 = 192
```

`//` teilt **ohne Rest** (200 // 64 = 3, nicht 3,125) — das ist die Schubladennummer. Mal 64
ergibt den Anfang der Schublade. Für 16 Stufen ist `schritt` 16, für 2 Stufen 128. Im Skript
macht das die Funktion `stufen(bild, n)`.

`size` bleibt gleich: Es sind genauso viele Werte — jeder kann nur weniger Verschiedenes sagen.

## Teil 5 — JPEG

```python
bgr = cv2.cvtColor(bild, cv2.COLOR_RGB2BGR)        # imwrite will wieder BGR
cv2.imwrite("klein.jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, 10])     # Qualität 0 bis 100
cv2.imwrite("gross.png", bgr)                                     # ohne Verlust
os.path.getsize("klein.jpg")            # Dateigröße in Byte (braucht: import os)
unterschied = cv2.absdiff(bild_a, bild_b)   # Abweichung je Wert
```

## Teil 6 — Eure Vorverarbeitung

Nichts Neues — Ausschneiden, Skalieren, Grau und Stufen hintereinander:

```python
netz = bild[Y:Y + SEITE, X:X + SEITE]
netz = cv2.resize(netz, (224, 224))
```

---

## Zum Ausprobieren

```python
bild[:, ::-1]                    # spiegeln: Spalten rückwärts lesen
bild[::-1, :]                    # auf den Kopf: Zeilen rückwärts
bild[:, :, [1, 2, 0]]            # Kanäle vertauschen
spiel = bild.copy(); spiel[:, :, 0] = 0      # Rotkanal abschalten
255 - bild                       # invertieren: aus hell wird dunkel
klein = cv2.resize(bild, (32, 32))           # verpixeln: erst klein ...
cv2.resize(klein, (breite, hoehe), interpolation=cv2.INTER_NEAREST)   # ... dann groß
bild.size / netz.size            # Reduktionsfaktor
```

**Aufhellen ohne Überlauf.** `uint8` kann nur 0 bis 255: `250 + 60` ergibt 54, nicht 310 —
helle Stellen werden schwarz. So geht es richtig:

```python
heller = np.clip(bild.astype(np.int16) + 60, 0, 255).astype(np.uint8)
```

---

## Hausaufgabe

```python
def name(b, seite):          # Funktion mit zwei Eingaben
    ...
    return ergebnis          # gibt etwas zurück

h, w = b.shape[:2]           # nur Höhe und Breite, egal ob Farbe oder Grau
min(h, w)                    # die kleinere der beiden Zahlen
for k in range(8):           # k läuft von 0 bis 7
    ...
(klasse == k).sum()          # zählt, wie viele Werte gleich k sind
plt.bar(range(8), anzahlen)  # Balkendiagramm
```

---

## Wenn etwas nicht geht

| Meldung | Bedeutet meistens |
|---|---|
| `'NoneType' object has no attribute 'shape'` | Der Pfad stimmt nicht — Teil 0 a |
| `IndexError: index … is out of bounds` | y und x vertauscht — Teil 0 c |
| Bild nach `resize` hochkant statt quer | (Breite, Höhe) vertauscht — Teil 2 |
| Farben sehen falsch aus (Rost blau) | `COLOR_BGR2RGB` vergessen — Teil 0 b |
| Bild erscheint schwarz oder falsch hell | Überlauf bei `uint8` — Zum Ausprobieren |
| `TypeError: Image data of dtype … cannot be displayed` | Es ist kein `uint8` mehr — `.astype(np.uint8)` |

**Fehlermeldungen liest man von unten nach oben.** Die letzte Zeile sagt, was schiefging;
die Zeile darüber, wo.
