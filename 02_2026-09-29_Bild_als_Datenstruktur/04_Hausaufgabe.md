# DS 02 — Hausaufgabe

---

## Eure Werkzeugkiste

Baut euch jetzt vier Funktionen. Alles, was ihr dafür
braucht, kennt ihr aus dieser Stunde; die Befehle stehen im Spickzettel unter „Hausaufgabe".

Schreibt jeweils eure Zeilen statt `pass` hinein und testet mit den Zeilen darunter.

---

## 1 — `info(b)`

Gibt für ein Bild `shape`, `size`, `dtype` sowie den kleinsten, größten und mittleren Wert aus.

Test: `info(bild)` und `info(MATRIX)`. Bei `MATRIX` muss herauskommen: `shape (8, 8)`,
`size 64`, kleinster Wert 30, größter 214.

## 2 — `quadrat_mitte(b, seite)`

Schneidet ein Quadrat mit der Kantenlänge `seite` genau aus der Bildmitte aus und gibt es
zurück.

> **Tipp:** Die linke obere Ecke liegt eine halbe Restbreite vom Rand entfernt:
> `(Höhe − seite) // 2` Zeilen und `(Breite − seite) // 2` Spalten.

Test: `zeigen(quadrat_mitte(bild, 500))` — ist das Bauteil in der Mitte? `shape` muss
`(500, 500, 3)` sein.

## 3 — `netz_eingang(b, grau=False)`

Macht aus einem beliebigen Foto einen Netz-Eingang: das größtmögliche Quadrat aus der Mitte
(`seite` ist die kleinere der beiden Bildseiten), dann auf 224 × 224 skaliert, und wenn
`grau=True`, in Graustufen umgerechnet. Benutzt dafür eure Funktion aus Aufgabe 2.

Test: `netz_eingang(bild).shape` muss `(224, 224, 3)` ergeben,
`netz_eingang(bild, grau=True).shape` muss `(224, 224)` ergeben.


---
