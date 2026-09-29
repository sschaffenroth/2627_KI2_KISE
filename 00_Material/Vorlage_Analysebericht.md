# Vorlage Analysebericht LS 1 — „Wie weit kommen wir klassisch?"

**Fach** KI-Systementwicklung — Computer Vision · KI 2. Jahr
**Handlungsprodukt** Lernsituation 1 (DS 01–06)
**Abgabe** Di, **10.11.2026**, zu Stundenbeginn
**Bearbeitung** im Zweierteam, ein Bericht je Team

Name 1: ______________________________  Name 2: ______________________________

Bauteil: ______________________________

---

## Worum es geht

Ihr habt zwischen dem 22.09. und dem 27.10. eine vollständige klassische Bildverarbeitung
an eurem eigenen Bauteil aufgebaut: aufgenommen, das Histogramm gelesen, die Belichtung
korrigiert, gefiltert, binarisiert, Konturen gefunden und vermessen. Am 27.10. habt ihr
diese Pipeline über eure vier Beleuchtungen laufen lassen und **gemessen**, wie oft sie
das Bauteil findet.

Der Bericht beantwortet eine einzige Frage: **Reicht das für einen Betriebseinsatz?**

Er ist kein Protokoll und keine Zusammenfassung des Unterrichts. Er ist eine
**Beurteilung auf Grundlage eurer eigenen Messwerte**.

---

## Umfang und Form

| | |
|---|---|
| Umfang | **3 bis 5 Seiten** Text, Bilder und Tabellen zusätzlich |
| Format | PDF, ein Team eine Datei |
| Dateiname | `Analysebericht_Nachname1_Nachname2.pdf` |
| Abgabe | 10.11. zu Stundenbeginn, Namensliste liegt aus |
| Bilder | Screenshots und Aufnahmen gehören hinein, mit **Bildunterschrift** |
| Sprache | Deutsch; Fachbegriffe englisch, wo sie so heißen |

Ein Bericht ohne Zahlen wird nicht angenommen. Die Zahlen habt ihr — sie stehen in eurem
Aufnahmeprotokoll aus DS 03 und in eurer Trefferbilanz aus DS 06.

---

## Gliederung

### 1. Das Bauteil und die Prüfaufgabe (etwa 1/2 Seite)

- Welches Bauteil, woher, wie groß, welches Material, wie oberflächenbeschaffen?
- Was genau soll geprüft werden — gut/schlecht, vorhanden/fehlend, richtig/falsch herum?
- Ein Foto des Bauteils, gut und schlecht nebeneinander.

### 2. Die Aufnahmeserie (etwa 1/2 Seite)

- Die vier Beleuchtungen aus DS 03: hell/direkt, dunkel, seitlich streifend, Mischlicht.
- Die vier Aufnahmen abbilden, **alle vier**, mit Bildunterschrift.
- Die Aufnahmekonvention nennen: Abstand, Höhe, Untergrund, Kameraeinstellungen.
  Was war bei allen vier gleich, was hat sich unterschieden?
- Die Histogrammkennwerte je Aufnahme in einer Tabelle:

| Beleuchtung | Mittelwert | Streuung | Pixel bei 0 | Pixel bei 255 |
|---|---|---|---|---|
| hell/direkt | | | | |
| dunkel | | | | |
| seitlich streifend | | | | |
| Mischlicht | | | | |

- Ein bis zwei Sätze: Bei welcher Aufnahme ist bereits hier Information verloren?

### 3. Der Otsu-Test über vier Beleuchtungen (etwa 1 Seite)

Das ist die Messung aus DS 04.

- Otsu-Schwelle je Beleuchtung, in einer Tabelle.
- Die vier Masken abbilden.
- Bei welchen Aufnahmen ist die Maske brauchbar, bei welchen nicht?
- **Woran** genau scheitert es — zu viel Hintergrund, zerrissenes Objekt, Schatten als
  Objekt erkannt, Objekt komplett verschwunden?
- Ein Satz dazu, warum ein Verfahren, das die Schwelle je Bild neu bestimmt, hier
  trotzdem an seine Grenze kommt.

### 4. Der Härtetest der vollständigen Pipeline (etwa 1 bis 1 1/2 Seiten)

Das ist die Messung aus DS 06 — der Kern des Berichts.

- Eure Pipeline in **einer** nummerierten Aufzählung: welche Schritte in welcher
  Reihenfolge, mit welchen Parametern.
- Die drei Parameter, die für alle vier Aufnahmen unverändert galten:
  Schwellwert · Kerngröße Öffnen · Mindestfläche.
- Die Trefferbilanz:

| Beleuchtung | Bauteil gefunden | Fläche der größten Kontur | Formfaktor | gescheitert an |
|---|---|---|---|---|
| hell/direkt | ☐ ja ☐ nein | | | — |
| dunkel | ☐ ja ☐ nein | | | |
| seitlich streifend | ☐ ja ☐ nein | | | |
| Mischlicht | ☐ ja ☐ nein | | | |

**Treffer: ______ von 4**

- Je gescheiterter Aufnahme zwei Sätze: **was** war falsch, und **an welchem Schritt**
  ist es gescheitert (Schwellwert, Morphologie oder Konturauswahl)?
  „Hat nicht funktioniert" ist keine Aussage.
- Die Masken der gescheiterten Fälle abbilden.

### 5. Fazit — reicht das für den Betrieb? (etwa 1/2 bis 1 Seite)

- Beantwortet die Leitfrage **mit Bezug auf eure Trefferzahl**, nicht allgemein.
- Unter welchen Bedingungen würde euer System heute zuverlässig laufen? Nennt die
  Bedingungen konkret.
- Was müsste am **Prüfplatz** geändert werden, damit es läuft — und was kostet das?
- Was müsste am **Verfahren** geändert werden?
- Ein Absatz zur Verlässlichkeit: Was sagt euch eure Zahl darüber, ob ihr dem System
  eine Prüfentscheidung überlassen würdet? Geht dabei über „man braucht besseres Licht"
  hinaus.

---

## Bewertungskriterien

| Kriterium | Gewicht | Was zählt |
|---|---|---|
| **Messwerte vollständig und nachvollziehbar** | 30 % | Alle vier Beleuchtungen, alle Kennwerte, alle Parameter genannt. Fehlende Zahlen sind der häufigste Punktverlust. |
| **Fehleranalyse** | 30 % | Je gescheiterter Fall benannt, an welchem Schritt es kippt — nicht nur, dass es kippt. |
| **Fazit mit Bezug auf die eigene Messung** | 25 % | Die Beurteilung hängt an der eigenen Trefferzahl, nicht an einer allgemeinen Aussage über Bildverarbeitung. |
| **Form und Sprache** | 15 % | Gliederung eingehalten, Bilder beschriftet, Fachbegriffe richtig verwendet, Umfang eingehalten. |

**Ausdrücklich nicht bewertet:** wie viele Treffer ihr habt. Eine Pipeline, die 1 von 4
schafft und den Bruch sauber analysiert, ist ein besserer Bericht als eine mit 4 von 4
ohne Analyse.

> Wer 4 von 4 Treffern hat, ersetzt die Fehleranalyse in Abschnitt 4 durch: **drei
> konkrete Aufnahmesituationen, unter denen eure Pipeline scheitern würde**, jede in
> einem Satz begründet.

---

## Zeitplan

| Wann | Was |
|---|---|
| DS 03, 06.10. | Aufnahmeserie und Protokoll — Grundlage für Abschnitt 2 |
| DS 04, 13.10. | Otsu-Test — Grundlage für Abschnitt 3 |
| DS 06, 27.10. | Härtetest und Trefferbilanz — Grundlage für Abschnitt 4 |
| Hausaufgabe DS 06 | Rohbau: Tabelle, Fehleranalyse, These. **Das ist bereits der Kern.** |
| Herbstferien 02.–06.11. | Ausformulieren, Bilder einsetzen |
| **Di 10.11.** | **Abgabe zu Stundenbeginn** |

Der Bericht ist keine zusätzliche Arbeit, sondern vorgezogene: Wer die Hausaufgabe vom
27.10. sauber gemacht hat, hat Abschnitt 4 und 5 im Rohbau fertig.

---

## Checkliste vor der Abgabe

- ☐ Alle vier Beleuchtungen behandelt, keine weggelassen
- ☐ Trefferzahl aus DS 06 steht im Bericht
- ☐ Die drei Pipeline-Parameter sind genannt
- ☐ Je gescheiterter Fall: was war falsch **und** an welchem Schritt
- ☐ Alle Bilder haben eine Bildunterschrift
- ☐ Das Fazit nennt die eigene Trefferzahl
- ☐ 3 bis 5 Seiten Text, PDF, richtig benannt
- ☐ Beide Namen stehen drauf
