"""
DS 02 — Bildwerkstatt
KI-Systementwicklung, 29.09.2026

Die Frage der Stunde: Das Netz nimmt 224 x 224 x 3 = 150 528 Zahlen.
Euer Foto hat Millionen. Was werft ihr weg — und was kostet es euch?

Die Befehle stehen alle hier drin. Eure Arbeit ist ausprobieren, hinschauen,
entscheiden. Ändern dürft ihr alles; wo ihr etwas ändern MÜSST, steht  >>> EINTRAGEN.
Jeder Teil beginnt mit AUFGABE — das steht auch auf dem Arbeitsblatt.
Was ein Befehl tut, steht im Spickzettel — in derselben Reihenfolge wie hier.

Teil für Teil ausführen (in Colab: eine Zelle je Teil), nicht alles auf einmal.
"""

# =================================================================
# Teil 0 — Die Werkstatt: was haben wir da eigentlich in der Hand?
# =================================================================
#
# Drei Bibliotheken, jede mit einer Aufgabe:
#
#   cv2         OpenCV, die Werkstatt: Bild laden und speichern,
#               skalieren, Farben umrechnen.
#   numpy       das Zahlenfeld: Ein geladenes Bild IST ein NumPy-Array.
#               Auswählen, ausschneiden, rechnen, zählen geht mit NumPy.
#   matplotlib  der Bildschirm. Davon brauchen wir nur den Teil pyplot,
#               der macht aus dem Zahlenfeld wieder ein Bild.
#
#   Datei  --cv2.imread-->  Zahlenfeld  --plt.imshow-->  Bild auf dem Schirm

import os

import cv2
import numpy as np
import matplotlib.pyplot as plt

# >>> EINTRAGEN — der Pfad zu eurem Bild
#   Colab:  links Ordnersymbol, Bild hochladen   ->  "/content/bauteil.jpg"
#   lokal:  mit r vor dem Pfad                   ->  r"C:\Users\...\bauteil.jpg"
#   Kein eigenes Foto? Das Testbild sys02_bauteil.jpg liegt im Repository neben
#   diesem Skript. In Colab holt es diese Zeile (in eine eigene Zelle):
#   !wget -q https://raw.githubusercontent.com/sschaffenroth/2627_KI2_KISE/main/02_2026-09-29_Bild_als_Datenstruktur/sys02_bauteil.jpg
BILDPFAD = "/content/sys02_bauteil.jpg"

KANTE = 224              # Eingang des Netzes: 224 x 224. Fest vorgegeben.


# --- Zwei Helfer fürs Anzeigen. Lesen lohnt sich, ändern ist nicht nötig.

def zeigen(b, titel="", achsen=False):
    """Ein Bild anzeigen. Mit achsen=True seht ihr Zeilen- und Spaltennummern."""
    plt.figure(figsize=(8, 6))
    if b.ndim == 2:                                  # Graustufen brauchen eine Farbskala
        plt.imshow(b, cmap="gray", vmin=0, vmax=255)
    else:
        plt.imshow(b)
    plt.title(titel)
    if not achsen:
        plt.xticks([])
        plt.yticks([])
    plt.show()


def vergleich(*paare):
    """Bilder nebeneinander:  vergleich((bild_a, "vorher"), (bild_b, "nachher"))"""
    plt.figure(figsize=(5 * len(paare), 5))
    for i, (b, titel) in enumerate(paare, start=1):
        plt.subplot(1, len(paare), i)
        if b.ndim == 2:
            plt.imshow(b, cmap="gray", vmin=0, vmax=255)
        else:
            plt.imshow(b)
        plt.title(titel)
        plt.xticks([])
        plt.yticks([])
    plt.show()


# --- a) Bild laden

roh = cv2.imread(BILDPFAD)
if roh is None:
    raise SystemExit("Kein Bild geladen. Pfad prüfen — steht der Dateiname genau so da?")


# --- b) Farben richtig stellen
# cv2 liest die drei Kanäle in der Reihenfolge Blau, Grün, Rot (BGR).
# plt und fast alle anderen erwarten Rot, Grün, Blau (RGB). Also einmal
# umdrehen — ab hier arbeiten wir nur noch mit RGB.

bild = cv2.cvtColor(roh, cv2.COLOR_BGR2RGB)
vergleich((roh, "so wie cv2 es liefert (BGR)"), (bild, "nach COLOR_BGR2RGB"))
zeigen(bild, "euer Bild — die Achsen sagen euch, wo ihr seid", achsen=True)


# --- c) Ein heller und ein dunkler Pixel
# >>> EINTRAGEN — Lage an den Achsen oben ablesen: erst Zeile y, dann Spalte x.

hell = bild[100, 200]
dunkel = bild[400, 600]
print("heller Pixel :", hell, "  (Rot, Grün, Blau)")
print("dunkler Pixel:", dunkel)


# --- d) Ein rotes Quadrat: Zeilen 400 bis 600, Spalten 400 bis 600

rot = bild.copy()
rot[400:600, 400:600] = [255, 0, 0]
zeigen(rot, "rotes Quadrat", achsen=True)


# --- e) Wie groß ist euer Bild?

print("shape:", bild.shape, "  (Höhe, Breite, Kanäle)")
print("size :", bild.size, "  Werte — so viele Zahlen stecken in eurem Bild")
print("Netz :", KANTE * KANTE * 3, "  Werte")


# =================================================================
# Teil 1 — Hebel Ausschneiden: alles weg, was nicht zum Merkmal gehört
# =================================================================
#
# AUFGABE: Verschiebt das 224 x 224-Fenster, bis euer Merkmal gut drin liegt.
#
# >>> EINTRAGEN — die linke obere Ecke des Ausschnitts.

Y, X = 190, 500

ausschnitt = bild[Y:Y + KANTE, X:X + KANTE]

print("ganzes Bild:", bild.shape, "  size", bild.size)
print("Ausschnitt :", ausschnitt.shape, "  size", ausschnitt.size)
vergleich((bild, "ganzes Bild"), (ausschnitt, "Ausschnitt 224 x 224"))
# Steht bei shape nicht (224, 224, 3)? Dann ragt der Ausschnitt über den Bildrand.


# =================================================================
# Teil 2 — Hebel Skalieren: das ganze Bild auf 224 x 224
# =================================================================
#
# AUFGABE: Gleich viele Zahlen, zwei Bilder — was ist der Unterschied?
#
# Achtung: resize will (Breite, Höhe) — andersherum als shape.

ganz = cv2.resize(bild, (KANTE, KANTE))

print("A ganzes Bild skaliert:", ganz.shape, "  size", ganz.size)
print("B Ausschnitt          :", ausschnitt.shape, "  size", ausschnitt.size)
vergleich((ganz, "A: ganzes Bild auf 224 skaliert"),
          (ausschnitt, "B: Ausschnitt 224, nicht skaliert"))


# =================================================================
# Teil 3 — Hebel Kanäle: braucht ihr die Farbe?
# =================================================================
#
# AUFGABE: Schaut euch die drei Kanäle einzeln an — in welchem sieht man
# euer Merkmal am besten? Dann Grau: Ist das Merkmal noch zu erkennen?
# Daraus eure Entscheidung: Farbe behalten oder Grau?
#
# Ein Farbbild sind drei Zahlenfelder übereinander, eins je Grundfarbe.
# bild[:, :, 0] ist das Rot-Feld, [:, :, 1] Grün, [:, :, 2] Blau.
# Hell heißt: viel von dieser Farbe.

vergleich((ausschnitt[:, :, 0], "Kanal 0: Rot"),
          (ausschnitt[:, :, 1], "Kanal 1: Grün"),
          (ausschnitt[:, :, 2], "Kanal 2: Blau"))

# Grau: aus drei Werten je Pixel wird einer.
#   Grauwert = 0,299 · Rot + 0,587 · Grün + 0,114 · Blau
grau = cv2.cvtColor(ausschnitt, cv2.COLOR_RGB2GRAY)

py, px = 62, 109            # eine farbige Stelle im Testbild — sucht euch eure eigene
print("dieser Pixel in Farbe:", ausschnitt[py, px], "  (Rot, Grün, Blau)")
print("derselbe Pixel in Grau:", grau[py, px])

print("Farbe:", ausschnitt.shape, "  size", ausschnitt.size)
print("Grau :", grau.shape, "  size", grau.size)
vergleich((ausschnitt, "Farbe"), (grau, "Grau"))

# Ausblick DS 03: Es gibt Farbräume, in denen "welche Farbe" und "wie hell"
# getrennt stehen, zum Beispiel HSV:  cv2.cvtColor(ausschnitt, cv2.COLOR_RGB2HSV)


# =================================================================
# Teil 4 — Hebel Bittiefe: wie viele Helligkeitsstufen braucht ihr?
# =================================================================
#
# AUFGABE: Ab wie vielen Stufen ist euer Merkmal nicht mehr zu erkennen?
#
# Jeder Grauwert kann 256 verschiedene Stufen haben, 0 bis 255. Dafür
# braucht man 8 bit (2^8 = 256). Weniger Stufen = weniger bit je Wert:
#
#   16 Stufen = 4 bit      4 Stufen = 2 bit      2 Stufen = 1 bit
#
# So rundet man auf 4 Stufen: Die 256 Werte werden in 4 Schubladen zu je
# 64 aufgeteilt, und jeder Wert bekommt den Anfang seiner Schublade.
#
#   Schublade 0:   0 ...  63  ->   0        Beispiel: 200
#   Schublade 1:  64 ... 127  ->  64          200 // 64 = 3   (// teilt ohne Rest)
#   Schublade 2: 128 ... 191  -> 128          3 * 64 = 192
#   Schublade 3: 192 ... 255  -> 192          aus 200 wird 192
#
# Die Zahl der Werte (size) bleibt dabei gleich — jeder Wert kann nur
# weniger Verschiedenes sagen.

schritt = 256 // 4                      # 64 — so breit ist eine Schublade
vier_stufen = (grau // schritt) * schritt

print("vorher kommen", len(np.unique(grau)), "verschiedene Werte vor")
print("nachher nur noch:", np.unique(vier_stufen))


def stufen(b, n):
    """Dasselbe für beliebig viele Stufen n (2, 4, 8, 16, ... 256)."""
    schritt = 256 // n
    return (b // schritt) * schritt


vergleich((grau, "256 Stufen · 8 bit"),
          (stufen(grau, 16), "16 Stufen · 4 bit"),
          (vier_stufen, "4 Stufen · 2 bit"),
          (stufen(grau, 2), "2 Stufen · 1 bit"))


# =================================================================
# Teil 5 — JPEG: ist das auch ein Hebel?
# =================================================================
#
# AUFGABE: Wie viel kleiner wird die Datei — und wie viel kleiner das
# Zahlenfeld, das beim Laden wieder herauskommt?
#
# imwrite erwartet wieder BGR, deshalb beim Speichern zurück umdrehen.

zum_speichern = cv2.cvtColor(ausschnitt, cv2.COLOR_RGB2BGR)
cv2.imwrite("gross.png", zum_speichern)
cv2.imwrite("klein.jpg", zum_speichern, [cv2.IMWRITE_JPEG_QUALITY, 10])

jpeg = cv2.cvtColor(cv2.imread("klein.jpg"), cv2.COLOR_BGR2RGB)

print("PNG  Datei", os.path.getsize("gross.png"), "Byte   size", ausschnitt.size)
print("JPEG Datei", os.path.getsize("klein.jpg"), "Byte   size", jpeg.size)

unterschied = cv2.absdiff(ausschnitt, jpeg)
verstaerkt = np.clip(unterschied.astype(np.int16) * 4, 0, 255).astype(np.uint8)
vergleich((ausschnitt, "PNG"), (jpeg, "JPEG, Qualität 10"),
          (verstaerkt, "Unterschied, 4-fach verstärkt"))


# =================================================================
# Teil 6 — Eure Vorverarbeitung: was bekommt das Netz von eurem Bauteil?
# =================================================================
#
# AUFGABE: Stellt die Vorverarbeitung für euer Bauteil ein — so wenig
# Zahlen wie möglich, aber euer Merkmal muss noch klar zu sehen sein.
#
# Das Netz bekommt immer 224 x 224. Ihr entscheidet drei Dinge:
#
#   1. SEITE: Wie groß schneidet ihr aus?  224 = nur das Merkmal, in voller
#      Schärfe. Größer (z. B. 448 oder 896) = mehr vom Bauteil, wird dann auf
#      224 verkleinert und dabei unschärfer.
#   2. GRAU:  Farbe behalten (False) oder Grau (True)?
#   3. STUFEN: 256, 16, 4 oder 2?
#
# Ausführen, hinschauen, Werte ändern, nochmal. Probiert mindestens drei
# Einstellungen — auch eine, bei der das Merkmal verschwindet.
#
# >>> EINTRAGEN — eure Entscheidung

SEITE = 448              # Kantenlänge des Ausschnitts in Pixeln, mindestens 224
Y6, X6 = 100, 420        # linke obere Ecke des Ausschnitts
GRAU = False
STUFEN = 256

stueck = bild[Y6:Y6 + SEITE, X6:X6 + SEITE]
netz = cv2.resize(stueck, (KANTE, KANTE))
if GRAU:
    netz = cv2.cvtColor(netz, cv2.COLOR_RGB2GRAY)
netz = stufen(netz, STUFEN)

print("euer Ausschnitt:", stueck.shape, "  size", stueck.size)
print("fürs Netz      :", netz.shape, "  size", netz.size)
vergleich((stueck, "euer Ausschnitt"), (netz, "das bekommt das Netz"))


# =================================================================
# Probiert gerne auch aus — für alle, die Lust auf mehr haben
# =================================================================
#
# Zeile anschalten (# weg), ausführen, hinschauen. Befehle im Spickzettel.
#
# spiel = 255 - bild                          # invertieren: aus hell wird dunkel
# spiel = bild[:, ::-1]                       # spiegeln — und wie steht es auf dem Kopf?
# spiel = bild + 60                           # heller machen ... wirklich? Schaut auf die hellen Stellen
# spiel = bild.copy(); spiel[:, :, 0] = 0     # den Rotkanal abschalten
# spiel = bild[:, :, [1, 2, 0]]               # Kanäle vertauschen — Pop-Art
# spiel = cv2.resize(cv2.resize(bild, (32, 32)), (bild.shape[1], bild.shape[0]),
#                    interpolation=cv2.INTER_NEAREST)       # verpixeln
# zeigen(spiel, "Spielwiese")
#
# print("verkleinert um Faktor", bild.size / netz.size)   # euer Reduktionsfaktor


# =================================================================
# Ausblick — derselbe Zahlenblock heißt später Tensor (ab DS 09)
# =================================================================
#
#   bild.shape    ->  (224, 224, 3)     NumPy-Array, Kanal zuletzt
#   tensor.shape  ->  (3, 224, 224)     PyTorch-Tensor, Kanal zuerst
#
# Gleiche Zahlen, gleiches Slicing. Nichts installieren.


# =================================================================
# Hausaufgabe bis 06.10. — eure Werkzeugkiste
# =================================================================
#
# Vier Funktionen, die ihr ab DS 03 immer wieder braucht. Alles, was ihr
# dafür braucht, kennt ihr aus dieser Stunde. Die Aufgabe steht in
# 04_Hausaufgabe.md, die Befehle im Spickzettel unter "Hausaufgabe".

def info(b):
    """Gibt shape, size, dtype, kleinsten, größten und mittleren Wert aus."""
    pass   # <- hier eure Zeilen statt pass


def quadrat_mitte(b, seite):
    """Schneidet ein Quadrat mit der Kantenlänge seite aus der Bildmitte."""
    pass


def netz_eingang(b, grau=False):
    """Größtmögliches Quadrat aus der Mitte, auf 224 x 224, auf Wunsch in Grau."""
    pass


def helligkeitsklassen(g):
    """Zählt, wie viele Pixel in jede der 8 Klassen 0-31, 32-63, ... 224-255 fallen.
    Gibt eine Liste mit 8 Anzahlen zurück."""
    pass


# Zum Testen — ein Graustufenbild mit 8 x 8 Pixeln
MATRIX = np.array([
    [34,  30,  41,  38,  35,  44,  31,  36],
    [33,  40,  96, 120, 118,  92,  37,  39],
    [36, 101, 198, 205, 201, 196,  99,  34],
    [42, 110, 207, 214, 211, 203, 104,  38],
    [30, 108, 204, 209, 206, 199, 102,  41],
    [37,  97, 190, 197, 193, 188,  95,  35],
    [40,  36, 103, 115, 112,  99,  33,  43],
    [31,  38,  32,  45,  39,  30,  42,  37],
], dtype=np.uint8)

# info(bild)
# zeigen(quadrat_mitte(bild, 500), "Quadrat aus der Mitte")
# print(netz_eingang(bild).shape, netz_eingang(bild, grau=True).shape)
# print(helligkeitsklassen(MATRIX))
