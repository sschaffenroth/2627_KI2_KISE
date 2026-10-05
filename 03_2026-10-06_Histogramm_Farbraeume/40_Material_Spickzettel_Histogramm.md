# Spickzettel — Histogramm und Kennwerte

---

## Einmal einrichten

Falls ihr Anaconda benutzt:
Anlegen der Umgebung [env].
```
conda create -n [env] python=3.13
conda activate [env]
conda install numpy opencv matplotlib
python -m pip install pyrealsense2
```

Danach in VS Code:

- **Datei → Ordner öffnen:** ein eigener Ordner für Skripte und Bilder.

---

## Bilder aufnehmen (P1)

Das Aufnahmeskript ist fertig: `05_aufnahme.py` im Kurs-Repository, Ordner `03_2026-10-06_Histogramm_Farbraeume`. Ladet es in euren Ordner.

- Skript starten. Das Kamerafenster zeigt das Livebild.
- Gespeichert wird über das Menü des Kamerafensters: auf das Speichern-Symbol in der Leiste oben klicken, euren Ordner wählen und den Dateinamen mit `.jpg` am Ende eintippen, zum Beispiel `03_lagerbock_hell_01.jpg`.
- Für jede Beleuchtung ein eigener Dateiname.
- Zum Beenden das Kamerafenster schließen.

Belichtung und Weißabgleich sind im Skript fest eingestellt, damit die Kamera nicht ausgleicht, was ihr messen wollt.

---

## Das Prüfprogramm (P2)

Ein neues Skript im selben Ordner wie eure Bilder:

```python
import cv2
import matplotlib.pyplot as plt

NAMEN = ["03_lagerbock_hell_01.jpg",          # eure vier Dateinamen
         "03_lagerbock_dunkel_01.jpg",
         "03_lagerbock_seitlich_01.jpg",
         "03_lagerbock_misch_01.jpg"]
```

## 1 — Laden und in Graustufen umrechnen

```python
for name in NAMEN:
    bild = cv2.imread(name)
    grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
    print(name, grau.shape)
```

Alles, was unter dem `for` eingerückt ist, läuft einmal je Bild.

## 2 — Histogramm

```python
plt.hist(grau.ravel(), bins=256, range=(0, 256), histtype="step", label=name)
```

| Parameter | Bedeutung |
|---|---|
| `grau.ravel()` | alle Pixel als eine lange Liste — das Histogramm braucht keine Zeilen und Spalten |
| `bins=256` | Anzahl der Säulen: eine je Grauwert |
| `range=(0, 256)` | Bereich der x-Achse. Die letzte Säule reicht von 255 bis 256, so bekommt 255 eine eigene Säule |
| `histtype="step"` | nur die Umrisslinie — so sieht man vier Histogramme übereinander |
| `label=name` | Beschriftung in der Legende |
| `density=True` | zusätzlich möglich: relative Darstellung, siehe unten |

Dieser Befehl gehört in die Schleife. Die folgenden Zeilen kommen **nach** der Schleife und werden nicht eingerückt:

```python
plt.xlabel("Grauwert")
plt.ylabel("Anzahl Pixel")
plt.legend()
plt.show()
```

Drückt eine Säule alles flach? Dann vor `plt.show()` einfügen: `plt.ylim(0, 30000)`

**Relative Darstellung mit `density=True`**

```python
plt.hist(grau.ravel(), bins=256, range=(0, 256), histtype="step", label=name, density=True)
```

Die y-Achse zeigt dann nicht mehr die Anzahl, sondern den **Anteil** der Pixel: 0.05 heißt, 5 % aller Pixel haben diesen Grauwert. Alle Säulen zusammen ergeben 1. So lassen sich auch Bilder mit verschiedener Pixelzahl vergleichen.

## 3 — Kennwerte

```python
grau.mean()            # Mittelwert: wie hell
grau.std()             # Streuung: wie verschieden
(grau == 0).sum()      # Anzahl Pixel genau 0
(grau == 255).sum()    # Anzahl Pixel genau 255
```

So gebt ihr eine Zeile je Bild aus:

```python
print(f"{name}  Mittel {grau.mean():.1f}  Streuung {grau.std():.1f}")
```

---

## Notfall: Die Kamera klappt nicht

Ladet im Kurs-Repository im Ordner `03_2026-10-06_Histogramm_Farbraeume` die Datei `sys03_notfall.zip` herunter. Entpackt sie in den Ordner eures Skripts. Dann:

```python
NAMEN = ["notfall/00_halter_hell_01.jpg", "notfall/00_halter_dunkel_01.jpg",
         "notfall/00_halter_seitlich_01.jpg", "notfall/00_halter_misch_01.jpg"]
```

---

## Die Kamera im eigenen Programm

So holt ihr ein Bild direkt von der Kamera in euer Programm, ohne Datei — zum Beispiel, damit euer Programm in P4 sofort über das Bild urteilt.

```python
import pyrealsense2 as rs
import numpy as np
import cv2
```

**Kamera starten**

```python
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
profil = pipeline.start(config)
```

`1280, 720` ist Breite und Höhe in Pixeln. Bei `bgr8` liegen die Farben in derselben Reihenfolge wie bei OpenCV, und `30` steht für 30 Bilder pro Sekunde.

**Belichtung festhalten**

```python
kamera = profil.get_device().first_color_sensor()
kamera.set_option(rs.option.enable_auto_exposure, 0)
kamera.set_option(rs.option.exposure, 150)
kamera.set_option(rs.option.enable_auto_white_balance, 0)
kamera.set_option(rs.option.white_balance, 4600)
```

| Option | Bedeutung |
|---|---|
| `enable_auto_exposure, 0` | Belichtungsautomatik aus |
| `exposure, 150` | feste Belichtungszeit |
| `enable_auto_white_balance, 0` | Weißabgleich-Automatik aus |
| `white_balance, 4600` | fester Weißabgleich |

Diese Zeilen kommen **nach** `pipeline.start`. Nehmt dieselben Werte wie im Aufnahmeskript.

**Bild aufnehmen**

```python
for i in range(30):                          # die ersten Bilder verwerfen
    frames = pipeline.wait_for_frames()
bild = np.asanyarray(frames.get_color_frame().get_data()).copy()
pipeline.stop()
```

Nach dem Start braucht die Kamera einen Moment, bis die feste Belichtung gilt — deshalb die 30 Bilder Vorlauf. `bild` ist danach dasselbe wie nach `cv2.imread`. Weiter geht es wie in Schritt 1:

```python
grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
```


## Wenn etwas nicht geht

| Meldung | Lösung |
|---|---|
| `No module named 'pyrealsense2'` oder `'cv2'` | in VS Code ist nicht der Interpreter `realsense` gewählt |
| `QWindowsContext: OleInitialize() failed …` | nur ein Hinweis — das Programm läuft trotzdem |
| `No device connected` | Kabel prüfen, Kamera an einen blauen USB-3-Anschluss |
| `Couldn't resolve requests` | Kamera hängt an USB 2 — blauen Anschluss nehmen oder `640, 480` statt `1280, 720` |
| Kamera ist belegt | Läuft das Aufnahmeskript noch? Kamerafenster schließen, RealSense Viewer beenden |
| Bild lässt sich nicht speichern | der Dateiname braucht `.jpg` am Ende |
| Bild gespeichert, aber nicht zu finden | beim Speichern war ein anderer Ordner gewählt — noch einmal speichern und euren Ordner wählen |
| `'NoneType' object has no attribute …` | Dateiname falsch, oder in VS Code ist nicht der Ordner mit euren Bildern geöffnet |
| Nur ein Histogramm | `plt.show()` steht in der Schleife |
| `IndentationError` | Einrückung — immer 4 Leerzeichen |

---