# Werkzeugkasten · Eure Fotos als Datensatz

Die Befehle der Stunde, geordnet nach den vier Teilen des Notebooks. Die Schritte und Namen sind die aus dem Buch, Kapitel 3, S. 81–88.

```python
import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torch.optim import SGD
```

---

## Teil 1 · Eure Fotos als Tensoren

| Befehl | danach |
|---|---|
| `bild = cv2.imread(pfad)` | (Höhe, Breite, 3), `uint8`, Farbfolge **BGR** |
| `cv2.cvtColor(bild, cv2.COLOR_BGR2RGB)` | Farbfolge RGB |
| `cv2.resize(bild, (64, 64))` | (64, 64, 3). Achtung: erst Breite, dann Höhe |
| `torch.tensor(bild).permute(2, 0, 1)` | (3, 64, 64): Kanal nach vorn |
| `sorted(os.listdir(ordner))` | Klassenordner alphabetisch; Position = Klassennummer |
| `for nummer, klasse in enumerate(klassen):` | jeder Name mit seiner Nummer 0, 1, 2 … |
| `datei.lower().endswith(('.jpg', '.jpeg', '.png'))` | nur Fotos zählen |
| `torch.stack(bilder)` | Liste von (3, 64, 64) wird ein Tensor (Anzahl, 3, 64, 64) |
| `tr_images, tr_targets, klassen = fotos_laden(…)` | Fotos, Klassennummern, Klassennamen (Namen wie im Buch) |
| `plt.imshow(t.permute(1, 2, 0))` | anzeigen: dafür den Kanal wieder nach hinten |

## Teil 2 · Dataset und DataLoader

| Methode | liefert oder macht | wird aufgerufen von |
|---|---|---|
| `__init__(self, x, y)` | `x.float() / 255`, `x.view(-1, 3 * 64 * 64)`, merkt sich `x` und `y` | `FotoDataset(tr_images, tr_targets)` |
| `__getitem__(self, ix)` | das Paar `(x[ix], y[ix])` | `ds[ix]` |
| `__len__(self)` | die Anzahl der Fotos | `len(ds)` |

| Befehl | bedeutet |
|---|---|
| `DataLoader(train, batch_size=8, shuffle=True)` | Stapel zu je 8, vor jeder Epoche neu gemischt |
| `DataLoader(val, batch_size=8, shuffle=False)` | Testfotos: nicht mischen |
| `trn_dl, val_dl = get_data()` | beide DataLoader auf einmal, wie im Buch |
| `x, y = next(iter(trn_dl))` | genau einen Stapel holen: `x` (8, 12288), `y` (8,) |
| `len(trn_dl)` | Stapel je Epoche = Lernschritte je Epoche |

## Teil 3 · Netz, Verlust, Optimierer

| Befehl | bedeutet |
|---|---|
| `nn.Linear(3 * 64 * 64, 1000)` | 12 288 Eingänge, 1 000 Neuronen |
| `nn.Linear(1000, len(klassen))` | ein Ausgang je Klasse |
| `nn.CrossEntropyLoss()` | Verlust für Klassen; bekommt die Rohwerte des Netzes und die Klassennummer |
| `SGD(model.parameters(), lr=1e-2)` | Gewichte nach jedem Stapel ein Stück bergab |
| `model, loss_fn, optimizer = get_model()` | alle drei auf einmal, wie im Buch |
| `sum(p.numel() for p in model.parameters())` | Zahl der Gewichte |

## Teil 4 · Trainieren und Treffer zählen

| Befehl | bedeutet |
|---|---|
| `model.train()` / `model.eval()` | Lernmodus / Prüfmodus |
| `batch_loss.backward()` | Richtung für jedes Gewicht ausrechnen |
| `optimizer.step()` | Gewichte verstellen |
| `optimizer.zero_grad()` | Richtungen löschen, bevor der nächste Stapel kommt |
| `@torch.no_grad()` | in dieser Funktion wird nichts gelernt |
| `max_values, argmaxes = prediction.max(-1)` | größter Wert je Zeile und seine Position (= getippte Klasse) |
| `argmaxes == y` | für jedes Foto `True` (Treffer) oder `False` |
| `np.mean(liste)` | Mittelwert; bei `True`/`False` die Trefferquote |

| Rechnung | |
|---|---|
| Lernschritte je Epoche | Fotos / Stapelgröße, aufgerundet (FashionMNIST: 60 000 / 32 ≈ 1 875) |
| Gewichte einer Schicht `Linear(ein, aus)` | ein · aus + aus |
| Verlust beim Raten | 0,69 bei 2 Klassen, 1,10 bei 3 Klassen |

---

## Fehler und was sie heißen

| Meldung | Ursache |
|---|---|
| `!_src.empty() in function 'cvtColor'` | `cv2.imread` hat das Foto nicht gefunden (Pfad) oder nicht lesen können (`.heic`) |
| `NotADirectoryError` | im Trainingsordner liegt eine Datei, wo nur Klassenordner sein sollen |
| `TypeError: Invalid shape (3, 64, 64) for image data` | `imshow` braucht den Kanal hinten: `.permute(1, 2, 0)` |
| `RuntimeError: stack expects each tensor to be equal size` | Fotos verschieden groß: `cv2.resize` fehlt |
| `view size is not compatible with input tensor's size and stride` | `view` auf einen Tensor direkt nach `permute`: erst `torch.stack` (wie in `fotos_laden`) oder `.contiguous()` |
| `mat1 and mat2 shapes cannot be multiplied` | das Foto ist nicht flach oder die Zahl in `nn.Linear` passt nicht zu 3 · 64 · 64 |
| `Target 2 is out of bounds` | weniger Ausgänge als Klassen: `nn.Linear(1000, len(klassen))` |
| Verlust bleibt bei 0,69 | das Netz rät; bei 80 Fotos und einem flachen Netz erwartet (Teil 4) |

---

Zum Nachschlagen: *Modern Computer Vision with PyTorch*, Kap. 3, S. 81–88 (FashionMNIST, `FMNISTDataset`, `get_data`, `get_model`, `train_batch`, `accuracy`, Skalieren) und S. 90–95 (Stapelgröße, Validierung).
