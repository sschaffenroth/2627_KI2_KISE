# DS 09 · Eure Fotos als Datensatz

**KI-Systementwicklung · 24.11.2026**

**Frage der Stunde:** Wie kommen eure Fotos stapelweise ins Netz, und lernt das Netz aus dem Buch sie?

```
Ordner mit Fotos  →  Tensoren  →  Dataset  →  DataLoader  →  Netz  →  Verlust  →  Gewichte verstellen
```

## Überblick

Das Notebook geht dieselben Schritte wie das Buch in Kapitel 3 (FashionMNIST), nur mit euren Fotos statt mit Kleidungsbildern. Die Namen der Funktionen sind dieselben wie im Buch: `get_data`, `get_model`, `train_batch`, `accuracy`.

| Teil | Thema | Im Buch | Zeit |
|---|---|---|---|
| 1 | Eure Fotos als Tensoren | S. 81–83 | 10 min |
| 2 | Dataset und DataLoader | S. 83–84, 88 | 14 min |
| 3 | Netz, Verlust, Optimierer | S. 85 | 8 min |
| 4 | Trainieren und Treffer zählen | S. 85–88 | 20 min |

Lest in jedem Teil zuerst den Text, dann führt den Code aus (Umschalt + Enter). Die Zellen von oben nach unten ausführen.

## Vorbereitung

Legt den Ordner `datensatz` neben dieses Notebook, mit `training/<klasse>/` und `test/<klasse>/`. Ohne eigene Fotos entpackt ihr `sys09_ersatzdatensatz.zip` an diese Stelle (gerechnete Zahnräder, `in_ordnung` und `fehlerhaft`). Oben rechts muss der Kernel `realsense` stehen.

Die erste Zelle lädt die Bibliotheken und zeigt, was im Ordner `datensatz` liegt. Darin müssen `training` und `test` stehen. Das Buch schickt alles mit `.to(device)` auf die Grafikkarte; die Schulrechner rechnen auf dem Prozessor, deshalb fehlt das hier.

```python
import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torch.optim import SGD

print(os.listdir('datensatz'))
```

---

## Teil 1 · Eure Fotos als Tensoren · 10 min

Im Buch liegen alle Kleidungsbilder schon fertig in einem Tensor `tr_images` mit der Form (60000, 28, 28), die Klassen in `tr_targets`. Eure Fotos liegen als Dateien in Ordnern. Deshalb bauen wir diese beiden Tensoren zuerst selbst.

`bild_laden` macht aus einer Datei einen Tensor, so wie ihr es aus DS 02 bis DS 04 kennt: `cv2.imread` liest das Foto als (Höhe, Breite, 3) mit ganzen Zahlen von 0 bis 255, `cvtColor` dreht die Farben von BGR auf RGB, `resize` bringt jedes Foto auf 64 × 64 Pixel. `permute(2, 0, 1)` setzt den Farbkanal nach vorn, so wie ein Netz für Bilder ihn erwartet: (3, 64, 64). Durch 255 wird erst im Dataset geteilt, wie im Buch.

`fotos_laden` geht durch alle Klassenordner. Die Ordnernamen werden alphabetisch sortiert, die Position in dieser Liste ist die Klassennummer: Die erste Klasse im Alphabet bekommt die 0, die nächste die 1. `enumerate` liefert zu jedem Namen gleich seine Nummer. Es zählen nur Dateien mit der Endung `.jpg`, `.jpeg` oder `.png`, damit Windows-Dateien wie `Thumbs.db` nicht als Foto gelten. `torch.stack` legt alle Fotos zu einem einzigen Tensor übereinander. Wir verwenden die Namen aus dem Buch: `tr_images` und `tr_targets` für das Training, `val_images` und `val_targets` für die Testfotos.

```python
def bild_laden(pfad, groesse=64):
    bild = cv2.imread(pfad)                          # (Höhe, Breite, 3), 0 bis 255, BGR
    bild = cv2.cvtColor(bild, cv2.COLOR_BGR2RGB)     # Farbfolge RGB
    bild = cv2.resize(bild, (groesse, groesse))      # (64, 64, 3)
    return torch.tensor(bild).permute(2, 0, 1)       # (3, 64, 64)

def fotos_laden(ordner):
    klassen = sorted(os.listdir(ordner))
    bilder, ziele = [], []
    for nummer, klasse in enumerate(klassen):
        for datei in sorted(os.listdir(os.path.join(ordner, klasse))):
            if datei.lower().endswith(('.jpg', '.jpeg', '.png')):
                bilder.append(bild_laden(os.path.join(ordner, klasse, datei)))
                ziele.append(nummer)
    return torch.stack(bilder), torch.tensor(ziele), klassen

tr_images, tr_targets, klassen = fotos_laden('datensatz/training')
val_images, val_targets, val_klassen = fotos_laden('datensatz/test')
print(tr_images.shape, tr_targets.shape, klassen)
print(val_images.shape, val_klassen == klassen)
```

Die Ausgabe zeigt (Anzahl Fotos, 3, 64, 64). Die letzte Zeile muss `True` zeigen: Training und Test brauchen dieselben Klassen in derselben Reihenfolge, sonst bedeuten dieselben Nummern Verschiedenes.

Bevor ein Netz mit den Fotos lernt, schauen wir sie an, wie das Buch die Kleidungsbilder in Abb. 3.10 zeigt: acht zufällige Trainingsfotos, jedes mit seinem Klassennamen. Ein Foto im falschen Ordner hat ein falsches Label, und das Netz lernt dann etwas Falsches, ohne dass eine Fehlermeldung kommt. Zum Anzeigen muss der Farbkanal wieder nach hinten, denn `plt.imshow` erwartet (Höhe, Breite, Kanäle): `permute(1, 2, 0)`.

```python
auswahl = torch.randperm(len(tr_images))[:8]
fig, ax = plt.subplots(2, 4, figsize=(10, 5))
for i, ix in enumerate(auswahl):
    zelle = ax[i // 4, i % 4]
    zelle.imshow(tr_images[ix].permute(1, 2, 0))
    zelle.set_title(klassen[tr_targets[ix]])
    zelle.axis('off')
plt.tight_layout()
plt.show()
```

---

## Teil 2 · Dataset und DataLoader · 14 min

Ein Netz lernt aus Paaren: zu jedem Foto die richtige Antwort, die Klasse. Ein **Dataset** ist die nummerierte Liste dieser Paare. Fragt man es nach Nummer 5, liefert es Foto Nummer 5 und die Nummer seiner Klasse. In PyTorch ist ein Dataset eine Klasse, die von `Dataset` erbt und drei Methoden hat. Unser `FotoDataset` ist gebaut wie das `FMNISTDataset` im Buch auf S. 84:

- `__init__(self, x, y)` bekommt alle Fotos und alle Klassennummern. Es teilt durch 255, damit alle Werte zwischen 0 und 1 liegen. Ohne das trifft das Netz im Buch nach fünf Epochen nur 12 %, mit Skalieren etwa 85 % (S. 88–89). Dann macht `view(-1, 3 * 64 * 64)` jedes Foto flach: aus (3, 64, 64) werden 12 288 Zahlen hintereinander, so wie im Buch aus 28 × 28 die 784 Zahlen. Das Netz aus dem Buch hat am Eingang eine Reihe von Zahlen, kein Bild.
- `__getitem__(self, ix)` gibt das Paar Nummer `ix` zurück; diese Methode ruft `ds[ix]` auf.
- `__len__(self)` gibt die Anzahl der Paare zurück; diese Methode ruft `len(ds)` auf.

Die Namen mit den doppelten Unterstrichen sind fest vorgegeben, nur unter diesen Namen findet PyTorch die Methoden.

Der **DataLoader** holt sich aus dem Dataset Paar für Paar und packt je 8 zu einem Stapel. Mit `shuffle=True` mischt er vor jeder Epoche, damit nicht alle Fotos einer Klasse hintereinander kommen. Die Testfotos werden nicht gemischt. Das Buch packt beides in eine Funktion `get_data`, wir auch. `next(iter(trn_dl))` holt genau einen Stapel heraus. Für jeden Stapel macht das Netz später einen Lernschritt; `len(trn_dl)` zeigt, wie viele Stapel eine Epoche hat.

```python
class FotoDataset(Dataset):
    def __init__(self, x, y):
        x = x.float() / 255                    # Werte von 0 bis 1
        x = x.view(-1, 3 * 64 * 64)            # jedes Foto flach: 12 288 Zahlen
        self.x, self.y = x, y

    def __getitem__(self, ix):
        x, y = self.x[ix], self.y[ix]
        return x, y

    def __len__(self):
        return len(self.x)

def get_data():
    train = FotoDataset(tr_images, tr_targets)
    trn_dl = DataLoader(train, batch_size=8, shuffle=True)
    val = FotoDataset(val_images, val_targets)
    val_dl = DataLoader(val, batch_size=8, shuffle=False)
    return trn_dl, val_dl

trn_dl, val_dl = get_data()
x, y = next(iter(trn_dl))
print(x.shape, y.shape, y)
print(len(trn_dl), 'Stapel je Epoche,', len(val_dl), 'Teststapel')
```

Ein Stapel `x` hat die Form (8, 12288): 8 Fotos mit je 12 288 Zahlen. `y` enthält die 8 Klassennummern dazu. Bei 80 Trainingsfotos sind es 10 Stapel, also 10 Lernschritte je Epoche.

---

## Teil 3 · Netz, Verlust, Optimierer · 8 min

`get_model` baut wie im Buch auf S. 85 drei Dinge auf einmal. Das **Netz** ist dasselbe wie im Buch: 12 288 Eingänge (bei FashionMNIST 784), eine Schicht mit 1 000 Neuronen und ReLU, und so viele Ausgänge, wie es Klassen gibt. Jeder Ausgang ist eine Zahl dafür, wie sehr das Netz auf diese Klasse tippt; die größte Zahl gewinnt.

Der **Verlust** ist hier `CrossEntropyLoss`, nicht `MSELoss` wie in DS 08: Wir sagen keine Zahl voraus, sondern eine Klasse. `CrossEntropyLoss` bekommt die Rohwerte des Netzes und die richtige Klassennummer und wird klein, wenn der richtige Ausgang deutlich vorn liegt. Ein Netz, das nur rät, hat bei zwei Klassen einen Verlust von etwa 0,69, bei drei Klassen etwa 1,10.

Der **Optimierer** `SGD` verstellt die Gewichte nach jedem Stapel ein Stück bergab, wie in DS 08. Die Lernrate 0,01 ist die aus dem Buch. `torch.manual_seed(0)` sorgt dafür, dass die Zufallszahlen am Anfang bei allen gleich sind.

```python
def get_model():
    model = nn.Sequential(
        nn.Linear(3 * 64 * 64, 1000),
        nn.ReLU(),
        nn.Linear(1000, len(klassen))
    )
    loss_fn = nn.CrossEntropyLoss()
    optimizer = SGD(model.parameters(), lr=1e-2)
    return model, loss_fn, optimizer

torch.manual_seed(0)
model, loss_fn, optimizer = get_model()
print(model)
print(sum(p.numel() for p in model.parameters()), 'Gewichte')

prediction = model(x)
print(prediction.shape, loss_fn(prediction, y).item())
```

Das ungelernte Netz liefert für den Stapel von eben 8 Zeilen mit je einer Zahl pro Klasse. Der Verlust liegt nahe am Wert fürs Raten. Über 12 Millionen Gewichte stecken fast alle in der ersten Schicht: 12 288 · 1 000.

---

## Teil 4 · Trainieren und Treffer zählen · 20 min

`train_batch` ist **ein Lernschritt** für einen Stapel, wie auf S. 85–86: `model.train()` schaltet das Netz in den Lernmodus, dann Vorhersage, Verlust, `backward` rechnet aus, in welche Richtung jedes Gewicht muss, `step` verstellt die Gewichte, `zero_grad` löscht die Richtungen für den nächsten Stapel. Zurück kommt der Verlust als Zahl.

`accuracy` zählt die Treffer. `@torch.no_grad()` sagt PyTorch, dass hier nichts gelernt wird; das spart Rechenzeit. `model.eval()` schaltet in den Prüfmodus. `prediction.max(-1)` sucht in jeder Zeile den größten Wert und liefert zwei Dinge: die Werte und ihre Positionen. Die Position (`argmaxes`) ist die Klasse, auf die das Netz tippt. `argmaxes == y` ist für jedes Foto `True` oder `False`.

Die Schleife läuft wie im Buch auf S. 86–87 über die Epochen und in jeder Epoche über alle Stapel. Nach jeder Epoche merken wir uns den mittleren Verlust, die Trefferquote auf den Trainingsfotos und die Trefferquote auf den Testfotos, die das Netz nie zum Lernen bekommt.

```python
def train_batch(x, y, model, optimizer, loss_fn):
    model.train()
    prediction = model(x)
    batch_loss = loss_fn(prediction, y)
    batch_loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    return batch_loss.item()

@torch.no_grad()
def accuracy(x, y, model):
    model.eval()
    prediction = model(x)
    max_values, argmaxes = prediction.max(-1)
    is_correct = argmaxes == y
    return is_correct.tolist()
```

```python
losses, accuracies, val_accuracies = [], [], []
for epoch in range(10):
    epoch_losses = []
    for x, y in trn_dl:
        epoch_losses.append(train_batch(x, y, model, optimizer, loss_fn))
    epoch_accuracies = []
    for x, y in trn_dl:
        epoch_accuracies.extend(accuracy(x, y, model))
    val_epoch_accuracies = []
    for x, y in val_dl:
        val_epoch_accuracies.extend(accuracy(x, y, model))
    losses.append(np.mean(epoch_losses))
    accuracies.append(np.mean(epoch_accuracies))
    val_accuracies.append(np.mean(val_epoch_accuracies))
    print(epoch + 1, round(losses[-1], 3), round(accuracies[-1], 2), round(val_accuracies[-1], 2))
```

Jede Zeile zeigt Epoche, Verlust, Trefferquote im Training und im Test. Die beiden Kurven zeigen dasselbe als Bild, wie Abb. 3.11 im Buch.

```python
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(range(1, 11), losses)
ax[0].set_title('Verlust im Training')
ax[0].set_xlabel('Epoche')
ax[1].plot(range(1, 11), accuracies, label='Training')
ax[1].plot(range(1, 11), val_accuracies, label='Test')
ax[1].set_title('Trefferquote')
ax[1].set_xlabel('Epoche')
ax[1].set_ylim(0, 1)
ax[1].legend()
plt.show()
```

Beim Ersatzdatensatz bleibt der Verlust bei etwa 0,69 und die Trefferquote bei etwa 50 %: Das Netz rät. Bei FashionMNIST kommt dasselbe Netz auf 85 %. Der Unterschied: Das Buch hat 60 000 Bilder, ihr habt 80. Und das Netz sieht jedes Foto als lange Reihe von Zahlen; es weiß nicht, welche Pixel Nachbarn sind. Liegt das Zahnrad etwas weiter links oder ist es gedreht, sind es für dieses Netz ganz andere Zahlen. Die Kette vom Foto bis zur Trefferquote läuft also, aber das Ergebnis ist noch nicht gut. In den nächsten Stunden suchen wir, wo wir optimieren können, und tauschen dafür jeweils ein Glied der Kette aus: in DS 10 das Netz (ein CNN aus Kapitel 4, das Nachbarschaften auswertet wie eure Filterkerne aus DS 05), in DS 11 das Training (Optimierer, Lernrate, Epochen), in DS 12 ein Netz, das schon an vielen Bildern vorgelernt hat. `get_data`, `train_batch` und `accuracy` bleiben dabei, wie sie sind.
