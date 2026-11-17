# DS 08 · Arbeitsblatt

**Das erste Netz in PyTorch · 17.11.2026**

Ihr baut ein Netz, das aus vier Beispielen addieren lernt. Grundlage ist das Buch *Modern Computer Vision with PyTorch*, Kapitel 2, Seiten 52 bis 63. Zu jeder Stufe lest ihr die Seiten und **schreibt den Code selbst** in ein neues Notebook, Zeile für Zeile. Nicht kopieren: Wer tippt, merkt, was er nicht versteht. Was die Befehle bedeuten, steht im Werkzeugkasten. Wer festhängt, klappt unter der Stufe den nächsten Tipp auf.

```
PyTorch   →  Daten  →  Netz  →  Verlust und Optimierer  →  Training  →  Vorhersage
Stufe 0      Stufe 1   Stufe 2   Stufe 3                    Stufe 4      Stufe 4
```

**Was ihr im Buch lest:**

| Stufe | Seiten | genau |
|---|---|---|
| 0 | 41–42 | *Installing PyTorch*. Den conda-Befehl mit CUDA aus Abb. 2.1 nehmt ihr **nicht**, sondern den aus Stufe 0. |
| 1 | 52–53 | *Building a neural network using PyTorch*, Schritte 1 und 2 |
| 2 | 53–56 | Schritt 3, i bis iv (die Klasse, die Gewichte ansehen). Schritt v auf S. 56 überspringen. |
| 3 | 57–58 | Schritte 5 und 6, Schritt 7 i bis iv |
| 4 | 58–59 und 62–63 | Schritt 7 v und vi mit Abb. 2.5; dann *Predicting on new data points*, Schritte 1 bis 3 (S. 62 Mitte bis S. 63 oben) |

S. 43–51 (Tensor-Befehle) und S. 63–71 braucht ihr heute nicht. S. 59–62 ist die Hausaufgabe.

**Frage der Stunde:** Was sagt euer Netz zu 10 und 11?

---

## Stufe 0 · PyTorch installieren (etwa 10 min)

**Buch:** S. 41–42, *Installing PyTorch*

**Ziel:** In eurer Umgebung `realsense` läuft PyTorch, und ihr habt ein neues Notebook mit dem richtigen Kernel.

*Installiert PyTorch in der Umgebung `realsense` und prüft die Version wie auf S. 42.*

Im Terminal von VS Code:

```
conda activate realsense
python -m pip install torch ipykernel
```

Der Download dauert ein paar Minuten. Lest währenddessen schon S. 52–53 für Stufe 1.

Eure PyTorch-Version: … Läuft auf: `cpu` oder `cuda`?

**0a** Das Buch installiert mit `pytorch-cuda=12.1` (S. 42). Warum passt das für die Schulrechner nicht, und warum ist das heute egal?

<details><summary>Tipp zu Stufe 0</summary>

Steht im Terminal vorne nicht `(realsense)`, ist die Umgebung nicht aktiv. Im Notebook oben rechts *Select Kernel* → *Python Environments* → `realsense`. Kommt `No module named 'torch'`, ist der falsche Kernel gewählt oder die Installation noch nicht fertig.

</details>

---

## Stufe 1 · Die Daten (etwa 7 min)

**Buch:** S. 52–53, Schritte 1 und 2

**Ziel:** Eingaben und Ziele liegen als Tensoren `X` und `Y` vor, mit Kommazahlen.

*Legt `x` und `y` als Listen an und macht daraus die Tensoren `X` und `Y`.*

Vermutet **vor** dem Ausführen und prüft dann:

| | Vermutung | Ausgabe |
|---|---|---|
| `X.shape` | | |
| `Y.shape` | | |
| `torch.tensor(x).dtype` (ohne `.float()`) | | |
| `X.dtype` | | |

**1a** Was bedeuten die zwei Zahlen in `X.shape`?

**1b** Warum macht das Buch aus den ganzen Zahlen Kommazahlen? (S. 53, erster Absatz)

<details><summary>Tipp zu Stufe 1</summary>

`x` ist eine Liste aus vier kleinen Listen mit je zwei Zahlen. Die erste Zahl der `shape` zählt die kleinen Listen, die zweite die Zahlen in jeder.

</details>

---

## Stufe 2 · Das Netz (etwa 13 min)

**Buch:** S. 53–56, Schritt 3, i bis iv (die Klasse `MyNeuralNet`, die Gewichte ansehen); Schritt v überspringen

**Ziel:** Euer Netz existiert als `mynet` und macht eine erste Vorhersage, auch wenn sie noch falsch ist.

*Schreibt die Klasse `MyNeuralNet` mit zwei Schichten und ReLU, legt `mynet` an und lasst es für `X` vorhersagen.*

**2a** Rechnet **vorher** aus: Wie viele Gewichte hat `nn.Linear(2, 8)`, wie viele Bias-Werte? Und `nn.Linear(8, 1)`?

| Schicht | Gewichte | Bias | zusammen |
|---|---|---|---|
| `nn.Linear(2, 8)` | | | |
| `nn.Linear(8, 1)` | | | |
| ganzes Netz | | | |

Prüft mit `mynet.input_to_hidden_layer.weight.shape` und S. 55–56.

**2b** Was steht in `__init__`, was in `forward`? Je ein Satz.

`__init__`:

`forward`:

**2c** `mynet(X)` ergibt bei euch:

Warum ist das noch weit weg von 3, 7, 11, 15?

<details><summary>Tipp 1 · Die Klasse</summary>

Die Klasse besteht aus zwei Teilen: In `__init__` werden die Schichten angelegt (S. 53, iii und iv). In `forward` steht, in welcher Reihenfolge die Eingabe durch die Schichten läuft. Achtet auf `super().__init__()` als erste Zeile in `__init__`.

</details>

<details><summary>Tipp 2 · Fehlermeldung beim Vorhersagen</summary>

`mat1 and mat2 must have the same dtype` heißt: Ihr gebt dem Netz ganze Zahlen. Das Netz rechnet mit Kommazahlen. Schaut in Stufe 1, welcher Tensor `.float()` hat.

</details>

---

## Stufe 3 · Verlust und ein Lernschritt (etwa 9 min)

**Buch:** S. 57–58, Schritte 5 und 6, Schritt 7 i bis iv

**Ziel:** Ihr könnt den Verlust ausrechnen lassen und seht, dass er nach einem Lernschritt kleiner ist.

*Legt `loss_func` und `opt` an, gebt den Verlust aus, macht genau einen Lernschritt und gebt den Verlust noch einmal aus.*

| | Verlust |
|---|---|
| vor dem Lernschritt | |
| nach einem Lernschritt | |

**3a** Prüft den ersten Wert selbst: Rechnet aus `mynet(X)` und `Y` den mittleren quadratischen Fehler mit eigenen Tensor-Rechnungen aus. Kommt dasselbe heraus?

**3b** Was tut jede der vier Zeilen eines Lernschritts? (S. 58, oben)

| Zeile | tut |
|---|---|
| `opt.zero_grad()` | |
| `loss_value = loss_func(mynet(X), Y)` | |
| `loss_value.backward()` | |
| `opt.step()` | |

<details><summary>Tipp zu 3a</summary>

Mittlerer quadratischer Fehler: Abstand von Vorhersage und Ziel, ins Quadrat, dann der Mittelwert. Mit Tensoren geht jeder dieser Schritte mit einem Rechenzeichen oder einem Befehl aus dem Werkzeugkasten.

</details>

<details><summary>Tipp zu 3b</summary>

`backward` rechnet für jedes Gewicht aus, in welche Richtung der Verlust sinkt. `step` schiebt die Gewichte. `zero_grad` löscht, was vom letzten Mal noch gespeichert ist.

</details>

---

## Stufe 4 · Training und Vorhersage (etwa 14 min)

**Buch:** S. 58–59 (Schritt 7 v und vi, Abb. 2.5), S. 62 Mitte bis S. 63 oben (*Predicting on new data points*, Schritte 1 bis 3)

**Ziel:** Euer Netz ist 50 Epochen trainiert, ihr seht die Verlaufskurve, und es sagt etwas zu 10 und 11.

*Wiederholt den Lernschritt in einer Schleife 50-mal, speichert den Verlust jeder Epoche, zeichnet die Kurve und lasst das Netz für 10 und 11 vorhersagen.*

Verlust nach 50 Epochen: … Vorhersage für 10 und 11:

**Abgabe am Handy:** eure Vorhersage für 10 und 11.

**4a** Warum speichert das Buch `loss_value.item()` und nicht `loss_value`? (S. 72, Frage 10)

**4b** Das Netz hat nie 10 und 11 gesehen. Woher weiß es die Antwort ungefähr?

**4c** Ein anderes Team hat eine etwas andere Vorhersage. Warum? (S. 55, Kasten)

<details><summary>Tipp 1 · Die Schleife</summary>

`for _ in range(50):` und darunter eingerückt die vier Zeilen aus Stufe 3. Die Liste für die Verluste legt ihr **vor** der Schleife an, angehängt wird **in** der Schleife.

</details>

<details><summary>Tipp 2 · Die Vorhersage</summary>

10 und 11 müssen genauso aussehen wie eine Zeile von `X`: eine Liste in einer Liste, als Tensor, mit `.float()`.

</details>

---

## Wer noch Zeit hat

**Ziel:** Ihr wisst, was passiert, wenn man am Training etwas ändert.

*Probiert es aus und notiert den Verlust nach 50 Epochen. Legt das Netz vor jedem Versuch neu an.*

| Änderung | Verlust nach 50 Epochen | was ihr seht |
|---|---|---|
| Lernrate 0.01 statt 0.001 | | |
| `opt.zero_grad()` weggelassen | | |
| eigene Regel, z. B. y = 2 · erste Zahl + zweite Zahl | | |

---

## Prüfungsformat

1. Nennt die fünf Schritte, mit denen man ein Netz in PyTorch baut und trainiert, und je einen Befehl dazu.
2. Wie viele Gewichte und Bias-Werte hat ein Netz aus `nn.Linear(3, 4)` und `nn.Linear(4, 2)`? Rechenweg.
3. Erklärt, warum vor jedem Lernschritt `opt.zero_grad()` steht.
4. Ein Netz gibt einen Fehler, weil `X` den dtype `torch.int64` hat. Was fehlt?
