# DS 08 · Hausaufgabe

**Das erste Netz in PyTorch · bis Dienstag, 24.11.2026**

Zeitbedarf: etwa 25 Minuten, ohne Rechner. Nächste Woche bekommt euer Netz eure eigenen Fotos. Dafür braucht ihr Dataset und DataLoader.

**Buch:** Kapitel 2, *Dataset, DataLoader, and batch size*, S. 59–62 (bis vor *Predicting on new data points*)

**H1** `MyDataset` hat drei Methoden. Was macht oder liefert jede?

| Methode | macht oder liefert |
|---|---|
| `__init__` | |
| `__len__` | |
| `__getitem__` | |

**H2** `ds` hat vier Beispiele, der `DataLoader` hat `batch_size=2`. Wie viele Stapel liefert `dl`, und welche shape hat `x` in einem Stapel? Was bewirkt `shuffle=True`?

**H3** In unserer Stunde hat jeder Lernschritt alle vier Beispiele auf einmal benutzt. Was ändert sich mit `batch_size=2`? (S. 62)

**H4** Überlegt für euren eigenen Datensatz: Was wäre bei euch ein Beispiel, also `x` und `y`?

x:

y:
