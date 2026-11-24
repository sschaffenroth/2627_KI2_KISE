# DS 09 · Hausaufgabe

**Eure Fotos als Datensatz · bis Dienstag, 01.12.2026**

Zeitbedarf: etwa 20 Minuten, ohne Rechner. Nächste Woche bekommt euer Netz Faltungsschichten, wie die Filterkerne aus DS 05. Die Hausaufgabe zeigt, warum.

**H1** In DS 03 bis DS 06 habt ihr Merkmale von Hand aus Bildern berechnet. Nennt drei davon.

______________________________________________________________________

**H2** Ein Netz sucht sich seine Merkmale beim Lernen selbst. Nennt einen Vorteil und einen Nachteil gegenüber Merkmalen von Hand.

______________________________________________________________________

______________________________________________________________________

**H3** Ein Netz für Graubilder 28 × 28 hat die Schichten `nn.Linear(28 * 28, 1000)`, `nn.ReLU()` und `nn.Linear(1000, 10)`. Rechnet aus, wie viele Gewichte und Bias-Werte es hat. Rechenweg wie in DS 08 (33 Gewichte).

______________________________________________________________________

**H4** Euer Netz aus Teil 3 hatte über 12 Millionen Gewichte, fast alle in der ersten Schicht `nn.Linear(3 * 64 * 64, 1000)`. Wie viele Gewichte und Bias-Werte hätte diese erste Schicht, wenn ihr die Fotos nicht auf 64 × 64, sondern auf 128 × 128 verkleinert? Vergleicht mit der Zahl eurer Trainingsfotos.

______________________________________________________________________

**H5** Schreibt die Trefferquote eures Netzes im Test nach 10 Epochen auf. Dasselbe Netz schafft bei FashionMNIST etwa 85 %. Nennt zwei Gründe, warum es bei euren Fotos schlechter ist.

______________________________________________________________________

______________________________________________________________________
