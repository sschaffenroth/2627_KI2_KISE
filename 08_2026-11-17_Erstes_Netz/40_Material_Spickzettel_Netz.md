# Werkzeugkasten · Das erste Netz in PyTorch

Was die Befehle aus dem Buch (Kapitel 2, S. 52–63) bedeuten. Den Code schreibt ihr selbst.

```python
import torch
import torch.nn as nn
from torch.optim import SGD
import matplotlib.pyplot as plt
```

---

## Umgebung

| Schritt | wie |
|---|---|
| Terminal öffnen | VS Code, *Terminal → Neues Terminal* |
| Umgebung aktivieren | `conda activate realsense` (vorne steht dann `(realsense)`) |
| PyTorch installieren | `python -m pip install torch ipykernel` (unter Windows die Fassung ohne Grafikkarte, etwa 200 MB) |
| neues Notebook | VS Code, *Datei → Ordner öffnen* (euer Arbeitsordner), dann *Datei → Neue Datei → Jupyter Notebook* |
| Kernel wählen | oben rechts *Select Kernel* → *Python Environments* → `realsense` |
| Zelle ausführen | `Umschalt + Enter` |
| prüfen, ob PyTorch da ist | `print(torch.__version__)` (Buch S. 42) |

## Tensoren

| Befehl | bedeutet |
|---|---|
| `torch.tensor(liste)` | macht aus einer Liste einen Tensor. Ganze Zahlen werden `int64`. |
| `t.float()` | macht daraus Kommazahlen (`float32`). Damit rechnet ein Netz. |
| `t.shape`, `t.dtype` | Anzahl der Zahlen je Achse, Art der Zahlen |
| `t - u`, `t ** 2`, `t.mean()` | rechnet mit jeder Zahl; Mittelwert aller Zahlen |
| `t.item()` | macht aus einem Tensor mit genau einer Zahl eine gewöhnliche Python-Zahl |

## Gerät

| Befehl | bedeutet |
|---|---|
| `device = 'cuda' if torch.cuda.is_available() else 'cpu'` | Grafikkarte, wenn vorhanden, sonst Prozessor. Auf den Schulrechnern: `'cpu'`. |
| `X = X.to(device)` | legt den Tensor auf dieses Gerät. Ohne Grafikkarte ändert sich nichts. |

## Das Netz

| Befehl | bedeutet |
|---|---|
| `class MyNeuralNet(nn.Module):` | ein eigenes Netz, gebaut auf dem Grundbaustein `nn.Module` von PyTorch |
| `super().__init__()` | erste Zeile in `__init__`: holt alles, was `nn.Module` mitbringt |
| `nn.Linear(2, 8)` | Schicht mit 2 Eingängen und 8 Ausgängen: jede Ausgabe ist eine gewichtete Summe der Eingänge plus Bias |
| `nn.ReLU()` | Aktivierung: negative Zahlen werden 0, positive bleiben |
| `def forward(self, x):` | der Rechenweg: in welcher Reihenfolge die Eingabe durch die Schichten läuft |
| `mynet = MyNeuralNet()` | legt das Netz an, mit zufälligen Gewichten |
| `mynet(X)` | Vorhersage für alle Zeilen von `X` (ruft `forward` auf) |
| `mynet.input_to_hidden_layer.weight` | die Gewichte einer Schicht |
| `torch.manual_seed(0)` | vor dem Anlegen: immer dieselben Zufallsgewichte |

## Lernen

| Befehl | bedeutet |
|---|---|
| `loss_func = nn.MSELoss()` | Verlust: mittlerer quadratischer Fehler. Erst Vorhersage, dann Ziel: `loss_func(vorhersage, Y)` |
| `opt = SGD(mynet.parameters(), lr=0.001)` | Optimierer: Gradientenabstieg über alle Gewichte, Lernrate 0,001 |
| `opt.zero_grad()` | löscht die Gradienten vom letzten Schritt |
| `loss_value.backward()` | rechnet für jedes Gewicht den Gradienten aus |
| `opt.step()` | schiebt jedes Gewicht ein Stück in Richtung kleinerer Verlust |
| `for _ in range(50):` | 50-mal wiederholen; `_` heißt: die Nummer der Runde brauchen wir nicht |
| `liste.append(wert)` | hängt einen Wert hinten an eine Liste an |

## Kurve zeichnen

| Befehl | bedeutet |
|---|---|
| `plt.plot(liste)` | zeichnet die Werte der Liste als Linie |
| `plt.xlabel(...)`, `plt.ylabel(...)`, `plt.title(...)` | Achsen und Titel beschriften |
| `plt.show()` | zeigt die Grafik |

---

## Fehler und was sie heißen

| Meldung oder Beobachtung | Ursache |
|---|---|
| `No module named 'torch'` | falscher Kernel gewählt oder PyTorch nicht installiert |
| `mat1 and mat2 must have the same dtype, but got Long and Float` | Eingabe ohne `.float()` |
| `cannot assign module before Module.__init__() call` | `super().__init__()` fehlt oder steht nicht oben |
| `mat1 and mat2 shapes cannot be multiplied` | Eingabe passt nicht zur ersten Schicht: `nn.Linear(2, …)` will 2 Zahlen je Zeile |
| Verlust wird nicht kleiner, sondern springt | Lernrate zu groß oder `zero_grad` vergessen |
| Netz sagt für alles fast dasselbe | Training nicht gelaufen oder Netz nach dem Training neu angelegt |
