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

## 4 — `helligkeitsklassen(g)`

Teilt die Grauwerte eines Bildes in acht Klassen ein — 0 bis 31, 32 bis 63, … 224 bis 255 —
und zählt, wie viele Pixel in jede Klasse fallen. Gibt eine Liste mit acht Anzahlen zurück.

> **Tipp:** `g // 32` macht aus jedem Grauwert seine Klassennummer 0 bis 7 — derselbe Trick
> wie bei der Bittiefe. `(klasse == 3).sum()` zählt, wie viele Pixel in Klasse 3 liegen.
> Eine `for`-Schleife über `range(8)` erledigt den Rest.

Test: `helligkeitsklassen(MATRIX)` — die acht Zahlen müssen zusammen **64** ergeben.

Tragt das Ergebnis ein und zeichnet es mit `plt.bar(range(8), anzahlen)` als Balkendiagramm:

| Klasse | 0–31 | 32–63 | 64–95 | 96–127 | 128–159 | 160–191 | 192–223 | 224–255 |
|---|---|---|---|---|---|---|---|---|
| Anzahl | | | | | | | | |

Wo im Diagramm liegt der Hintergrund, wo das Objekt? Ein Satz:

---

**Abgabeform:** das Skript mit den vier Funktionen gespeichert mitbringen (Colab oder
USB-Stick), dieses Blatt mit der Tabelle ausgefüllt.

**Wozu das gebraucht wird:** Die vier Funktionen benutzt ihr ab DS 03 in jeder Stunde. Und
das Balkendiagramm aus Aufgabe 4 hat einen Namen, den ihr noch nicht kennt — DS 03 beginnt
damit.

> **Und nicht vergessen: Bauteil mitbringen.** Am 06.10. nimmt jedes Team sein Bauteil
> unter vier Beleuchtungen auf. Ohne Bauteil keine Serie — und die Serie wird bis zum
> 22. Dezember viermal gebraucht.
