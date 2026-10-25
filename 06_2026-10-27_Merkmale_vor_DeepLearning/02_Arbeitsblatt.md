# DS 06 — Arbeitsblatt

**Den Halter finden: Wie weit kommen wir klassisch? · 27.10.2026**

Ein neues Skript im Ordner eurer vier Aufnahmen aus DS 03. Alles, was ihr braucht, kennt ihr schon — bis auf einen Schritt: die Umrisse. Die Befehle stehen im Werkzeugkasten. Wer festhängt, klappt unter dem Auftrag den nächsten Tipp auf.

```
Aufnahme  →  Glätten  →  Schwelle  →  Umriss  →  einzeichnen
DS 02/03     DS 05       DS 04        neu        neu
```

---

## P1 — Findet den Halter in `misch` (etwa 19 min)

**Ziel:** Das Farbfoto `misch`, in dem euer Programm den Umriss eures Halters orange eingezeichnet hat — und daneben seine Fläche in Pixeln.

### Auftrag 1 — Die Maske (etwa 6 min)

Ladet `misch`, schneidet den Ausschnitt aus, glättet mit einem 9 × 9-Mittelwertkern und lasst Otsu die Schwelle suchen. Zeigt die Maske an.

**Tipps** — erst selbst probieren, dann immer nur den nächsten aufklappen.

<details><summary>Tipp 1 — In welcher Reihenfolge?</summary>

Genau in der Reihenfolge der Zeile oben: laden, Ausschnitt, Graustufen, glätten, Otsu. Ladet das Foto **einmal in Farbe** und schneidet es aus — das Graubild macht ihr aus diesem Ausschnitt. So passen Farbfoto und Maske später Pixel für Pixel aufeinander.

</details>

<details><summary>Tipp 2 — Otsu meldet einen Fehler</summary>

Otsu nimmt nur ein Bild mit ganzen Zahlen von 0 bis 255. Mit `cv2.CV_64F` kommt beim Glätten ein Bild aus Kommazahlen heraus. Schreibt beim Glätten `-1` statt `cv2.CV_64F`: Dann ist das Ergebnis wieder ein Bild wie das Original. Beim Glätten geht dabei nichts verloren — ein Mittelwert von Grauwerten liegt immer zwischen 0 und 255.

</details>

Otsu-Schwelle: … Anteil weiß: … %

### Auftrag 2 — Der Umriss (etwa 13 min)

Lasst das Programm alle Umrisse in der Maske suchen. Nehmt den **größten**, gebt seine Fläche aus und zeichnet ihn orange ins Farbfoto.

**Tipps zu Auftrag 2**

<details><summary>Tipp 3 — Wie viele Umrisse?</summary>

`cv2.findContours` liefert eine Liste — einen Umriss für jede weiße Fläche in der Maske, auch für jeden Fleck. Wie lang die Liste ist, sagt `len`.

</details>

<details><summary>Tipp 4 — Der größte</summary>

`max(konturen, key=cv2.contourArea)` geht die Liste durch, misst bei jedem Umriss die Fläche und gibt den Umriss mit der größten zurück. Seine Fläche bekommt ihr danach mit `cv2.contourArea`.

</details>

<details><summary>Tipp 5 — Einzeichnen</summary>

Gezeichnet wird ins **ausgeschnittene Farbfoto**, nicht ins Graubild und nicht in die Maske. `cv2.drawContours` will eine Liste von Umrissen — auch wenn es nur einer ist, steht er in eckigen Klammern: `[groesster]`. OpenCV speichert Farben als Blau, Grün, Rot: `(0, 128, 255)` ist Orange. Zum Anzeigen dreht `cv2.cvtColor(…, cv2.COLOR_BGR2RGB)` die Reihenfolge um.

</details>

| | Otsu-Schwelle | Anzahl Umrisse | Fläche des größten |
|---|---|---|---|
| mit Glätten 9 × 9 | | | |
| ohne Glätten (wer fertig ist) | | | |

**Wer fertig ist:** Lasst das Glätten einmal weg (Otsu direkt auf dem Graubild) und tragt die zweite Zeile ein. Was hat das Glätten aus DS 05 hier getan? Schaut euch dazu auch den Rand des eingezeichneten Umrisses vergrößert an.

---

## P2 — Der Härtetest: Findet euer Programm den Halter bei jedem Licht? (etwa 15 min)

**Ziel:** Ein Fenster mit allen vier Aufnahmen, in jeder der gefundene Umriss — und eure Trefferzahl an der Tafel.

**Erst tippen:** In wie vielen der vier Aufnahmen findet euer Programm den Halter?

**Auftrag:** Lasst **dasselbe** Programm über alle vier Aufnahmen laufen. Ihr ändert nichts: derselbe Ausschnitt, derselbe Kern. Otsu sucht die Schwelle für jede Aufnahme selbst — das ist so gewollt.

**Gefunden** heißt: Der Umriss liegt auf dem Halter, und seine Fläche weicht höchstens 10 % von der Fläche in `misch` ab.

**Tipps zu P2**

<details><summary>Tipp 6 — Vier Aufnahmen in einem Fenster</summary>

Wie bei den vier Kantenbildern in DS 05: Die Dateinamen in eine Liste, `for i in range(1, 5):`, und alles aus P1 eingerückt in die Schleife — mit `bildpfad[i - 1]` statt des festen Namens. `plt.subplot(2, 2, i)` vor `plt.imshow` setzt jedes Bild an seinen Platz, `plt.show()` steht erst nach der Schleife, nicht eingerückt.

</details>

<details><summary>Tipp 7 — Die Abweichung</summary>

Abweichung in Prozent = (Fläche − Fläche in `misch`) / Fläche in `misch` · 100. Die Fläche in `misch` habt ihr aus P1 — schreibt sie als feste Zahl ins Programm. Ist die Abweichung größer als 10 oder kleiner als −10, gilt der Halter als nicht gefunden.

</details>

| Aufnahme | Otsu-Schwelle | Anzahl Umrisse | Fläche des größten | Abweichung von `misch` | gefunden? |
|---|---|---|---|---|---|
| `misch` | | | | 0 % | |
| `hell` | | | | | |
| `seitlich` | | | | | |
| `dunkel` | | | | | |

**Treffer: … von 4** — tragt sie in die Tabelle an der Tafel ein.

Wo der Halter nicht gefunden wurde: Was hat euer Programm stattdessen umrandet? Schaut in die Maske.

---

## Kür — Braucht es Otsu überhaupt?

Ersetzt Otsu durch eine **feste** Schwelle: die Otsu-Schwelle, die ihr in P1 für `misch` bekommen habt. Lasst den Härtetest noch einmal laufen. Wie viele Treffer jetzt — und bei welcher Aufnahme hat Otsu euch gerettet?

<details><summary>Tipp 8 — Kür</summary>

Die feste Schwelle steht im Werkzeugkasten unter „Für die Kür". Meldet `max` einen Fehler mit `empty`, gibt es in der Maske keinen einzigen weißen Pixel — dann ist die Liste der Umrisse leer. Zeigt euch die Maske dieser Aufnahme an.

</details>

Feste Schwelle: … Treffer: … von 4
