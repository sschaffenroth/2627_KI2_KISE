# DS 02 — Arbeitsblatt

**Das Bild als Datenstruktur · 29.09.2026**

*Lesefassung. Die Vorlage zum Ausfüllen bekommen Sie im Unterricht auf Papier — hier sind die Schreiblinien entfernt.*

> **Die Frage der Stunde:** Das Netz nimmt 224 × 224 × 3 = 150 528 Zahlen. Euer Foto hat Millionen. **Was werft ihr weg — und was kostet es euch?**

---

## 1 — Was haben wir da eigentlich in der Hand? (Teil 0, etwa 10 min)

Tragt oben im Skript den Pfad zu eurem Bild ein.

a) Ladet euer Bild.

b) Stellt die Farben richtig: OpenCV liefert Blau-Grün-Rot, wir brauchen Rot-Grün-Blau. Vergleicht die beiden Bilder.

c) Sucht euch an den Achsen grob die Lage eines hellen und eines dunklen Pixels und lest die Werte aus.

Heller Pixel: `bild[…, …]` = [ …, …, … ]

Dunkler Pixel: `bild[…, …]` = [ …, …, … ]

d) Setzt im Bereich x = 400 bis 600 und y = 400 bis 600 alle Pixel auf Rot. Welche drei Zahlen sind Rot? [ …, …, … ]

e) Wie groß ist euer Bild? `shape` … · `size` … Werte

---

## 2 — Welche Hebel haben wir, und was kostet jeder? (Teile 1 bis 5, etwa 20 min)

Je Hebel ein Teil im Skript. Notiert die Werte (`size`) und — das Wichtige — was der Hebel bei **eurem** Bild gekostet hat.

**Teil 1 · Ausschneiden.** Verschiebt das 224 × 224-Fenster, bis euer Merkmal gut drin liegt.
Werte … · kostet:

**Teil 2 · Skalieren.** Gleich viele Zahlen, zwei Bilder — was ist der Unterschied?
Werte … · kostet:

**Teil 3 · Kanäle.** In welchem Kanal sieht man euer Merkmal am besten? ☐ Rot ☐ Grün ☐ Blau
In Grau: Werte … · Merkmal noch zu erkennen? ☐ ja ☐ nein · kostet:

**Teil 4 · Bittiefe.** Ab wie vielen Stufen ist euer Merkmal weg? ☐ 16 ☐ 4 ☐ 2 ☐ nie
Werte … · kostet:

**Teil 5 · JPEG.** Datei von … auf … Byte · Werte vorher … nachher
Was bringt JPEG dem Netz?

---

## 3 — Eure Vorverarbeitung (Teil 6, etwa 10 min)

Das Netz bekommt immer 224 × 224. Ihr entscheidet, **was** darauf zu sehen ist — so wenig Zahlen wie möglich, aber euer Merkmal muss noch klar zu sehen sein. Im Skript stellt ihr dafür drei Dinge ein und probiert mindestens drei Einstellungen aus, auch eine, bei der das Merkmal verschwindet:

- `SEITE` — wie groß ihr ausschneidet: 224 = nur das Merkmal, scharf; größer = mehr Umgebung, dafür unschärfer
- `GRAU` — Farbe behalten oder Grau
- `STUFEN` — 256, 16, 4 oder 2

Unsere Entscheidung: `SEITE` … · ☐ Farbe ☐ Grau · `STUFEN` … → … Werte

Warum nicht noch weniger? Ein Satz:

---

## 4 — Prüfungsformat, ohne Rechner (wer fertig ist, sonst zu Hause)

> Ein Ziegelwerk will Risse erkennen. Ein Ziegel ist **240 mm** breit, ein feiner Riss **0,5 mm**. Das Netz nimmt 224 × 224.
>
> `mm je Netz-Pixel = Breite des Ausschnitts in mm ÷ 224`
> `Merkmal in Netz-Pixeln = Merkmal in mm ÷ mm je Netz-Pixel`

a) Der ganze Ziegel kommt ins Netz. Wie viele Netz-Pixel bleiben vom Riss?

b) Wie breit darf der Ausschnitt höchstens sein, damit der Riss **3 Netz-Pixel** behält? … mm

c) Nennt eine Konsequenz für den Aufbau der Prüfanlage und begründet sie in einem Satz.

> **Ansatz, falls ihr hängt:** Bei a) verteilen sich 240 mm auf 224 Pixel — ein Pixel ist also etwa 1 mm breit. Wie viel von einem Pixel ist dann 0,5 mm? Bei b) rückwärts: Wenn 0,5 mm auf 3 Pixel kommen sollen, wie breit ist dann ein Pixel? Und 224 solche Pixel?

---

## Probiert gerne auch aus

Für alle, die fertig sind oder Lust auf mehr haben. Vorschläge stehen am Ende des Skripts, die Befehle im Spickzettel.

- Invertiert euer Bild, spiegelt es, stellt es auf den Kopf.
- Macht es mit `+ 60` heller. Schaut genau auf die hellsten Stellen: Was passiert da, und warum?
- Schaltet einen Kanal ab oder vertauscht die Kanäle.
- Verpixelt euer Bild auf 32 × 32 — ab welcher Größe erkennt ihr das Bauteil nicht mehr?
- Um welchen Faktor habt ihr euer Bild in Teil 6 verkleinert? Rechnet ihn aus den beiden `size`-Werten aus: Faktor

---

**Zum 06.10.:** Bauteil mitbringen — handgroß, nicht spiegelnd, eines davon erkennbar fehlerhaft.
