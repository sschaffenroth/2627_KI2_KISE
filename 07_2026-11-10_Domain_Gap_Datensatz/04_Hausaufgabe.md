# DS 07 · Hausaufgabe: Euer Datensatz

**Bis Dienstag, 17.11.** Nächste Woche trainiert ihr damit euer erstes Modell.

Fotografiert euer Bauteil nach eurem Aufnahmeplan aus der Stunde.

## Was in den Datensatz gehört

- **Zwei Klassen:** in Ordnung und fehlerhaft. Ab wann ein Teil fehlerhaft ist, steht in eurer Richtlinie.
- **Training:** je Klasse mindestens 40 Bilder, verteilt auf alle vier Lichter (hell, dunkel, seitlich, misch). Dreht und verschiebt das Teil zwischen den Aufnahmen.
- **Test:** je Klasse 10 Bilder von einem Teil, das im Training nicht vorkommt. Habt ihr nur ein Teil je Klasse: an einem anderen Tag und an einem anderen Ort fotografieren.
- **Gleiche Bedingungen in beiden Klassen:** derselbe Untergrund, dieselben Lichter, dieselbe Kamera. Sonst lernt das Modell den Unterschied der Bedingungen statt des Fehlers.

## Ordner und Dateinamen

```
datensatz/
  training/
    in_ordnung/    io_hell_01.jpg, io_dunkel_01.jpg, ...
    fehlerhaft/    nio_hell_01.jpg, ...
  test/
    in_ordnung/
    fehlerhaft/
  richtlinie.txt   eure drei Sätze aus dem Aufnahmeplan
```

Das Licht steht im Dateinamen, damit ihr nächste Woche die Trefferquote je Licht ausrechnen könnt.

## Prüft vor der Abgabe

- [ ] Kommt jedes Licht in beiden Klassen vor?
- [ ] Liegen beide Klassen auf demselben Untergrund?
- [ ] Ist kein Teil gleichzeitig im Training und im Test?
- [ ] Sieht man den Fehler auf dem Foto?
