# Testprotokoll

Name: Sayed Ali Sina Mosavi
Datum: 05.11.2026

Ich habe die Tests im Terminal gemacht. Die Dateigröße habe ich mit `ls -l` geprüft, die Bildgröße mit `sips` und das Aussehen in der Vorschau. Der Hintergrund einer neuen Bitmap ist grau, damit man die weiße untere Hälfte vom Ball sieht.

| Nr. | Was ich eingebe | Das erwarte ich | Das ist passiert |
|---|---|---|---|
| 1 | `python3 main.py neu.bmp -w 200 -h 100 -x 100 -y 50 -r 40` | Es steht "Fertig: neu.bmp". Das Bild ist 200 x 100 groß, die Datei 60054 Byte. Oben roter Halbkreis, unten weißer Halbkreis, schwarzes Band, Ring mit weißer Mitte. | Ausgabe "Fertig: neu.bmp". Dateigröße 60054 Byte, 200 x 100 Pixel. Pokeball mit grauem Hintergrund wie erwartet. Der Pokeball ist klein und hat sehr viel leeren Hintergrund. Hat geklappt. |
| 2 | `python3 main.py std.bmp -w 100 -h 100` (ohne x, y, r) | Der Ball ist in der Mitte und füllt das Bild in der Breite. Oben rot, unten weiß, Ecken grau. | Ausgabe "Fertig: std.bmp". Diesmal wurde eine Bitmap mit 100 x 100 Pixeln erstellt. Weniger Hintergrund und ein größerer Pokeball. Hat geklappt. |
| 3 | `python3 main.py klein.bmp -w 3 -h 2` | Das Bild ist 3 x 2 groß, die Datei genau 78 Byte. | Ausgabe "Fertig: klein.bmp". Das Bild ist 3 x 2 Pixel groß und 78 Byte. Es ist grau, ein weißer Punkt ist nur an der unteren Mitte zu sehen. Hat geklappt. |
| 4 | `python3 main.py mitte.bmp -w 100 -h 100 -x 30 -y 30 -r 20` | Kleiner Ball oben links, der Rest ist grau. | Ausgabe "Fertig: mitte.bmp". Eine 100 x 100 Bitmap mit 30054 Byte (30,05 KB) wurde erstellt. Der kleine Ball ist in der oberen linken Ecke. Hat geklappt. |
| 5 | `python3 main.py r10.bmp -w 100 -h 100 -x 50 -y 50 -r 10` und dann `python3 main.py r30.bmp -w 100 -h 100 -x 50 -y 50 -r 30` | r10 hat einen kleinen Ball, r30 einen deutlich größeren. | Ausgabe "Fertig: r10.bmp" und "Fertig: r30.bmp". Wie erwartet wurde ein kleiner und ein größerer Ball erstellt. Hat geklappt. |
| 6 | Erst `open neu.bmp` (links oben ist kein Ball), dann `python3 main.py neu.bmp -x 30 -y 30 -r 20` | Das Bild bleibt 200 x 100 groß (60054 Byte). Links oben ist ein neuer Ball, der große in der Mitte ist noch da. | Ausgabe "Fertig: neu.bmp". Wie erwartet wurde ein kleiner Pokeball neben dem alten Ball in neu.bmp erstellt. Die Datei hat weiterhin 60054 Byte. Hat geklappt. |
| 7 | `python3 main.py rush.bmp pokerush -w 400 -h 300` | Das Bild ist 400 x 300 groß (360054 Byte). Man sieht viele Bälle in verschiedenen Größen. | Ausgabe "Fertig: rush.bmp". Das Bild ist 400 x 300 Pixel groß und 360054 Byte. Wie erwartet wurden sehr viele große und kleine Pokebälle übereinander gezeichnet. Hat geklappt. |
| 8 | `python3 main.py zu_klein.bmp pokerush -w 19 -h 100` | Fehlermeldung, dass das Bild zu klein ist. Die Datei wird nicht erstellt. | Ausgabe "Fehler: Die Bitmap ist für 'pokerush' zu klein: Die kleinere Kante muss mindestens 20 Pixel lang sein." Mit `ls zu_klein.bmp` sieht man, dass die Datei nicht erstellt wurde. Hat geklappt. |
| 9 | `python3 main.py` | Fehlermeldung, dass der Pfad fehlt. | Ausgabe "Fehler: the following arguments are required: path". Wie erwartet. |
| 10 | `python3 main.py nix.bmp` | Fehlermeldung, dass es die Datei nicht gibt und -w und -h gebraucht werden. | Ausgabe "Fehler: Die Datei 'nix.bmp' existiert nicht. Zum Erzeugen einer neuen Bitmap müssen -w und -h angegeben werden." Wie erwartet. |
| 11 | `python3 main.py nix.bmp -w 100` | Fehlermeldung, dass -w und -h zusammen kommen müssen. | Ausgabe "Fehler: Breite (-w) und Höhe (-h) müssen zusammen angegeben werden." Wie erwartet. |
| 12 | `python3 main.py nix.bmp -w 0 -h 100` | Fehlermeldung, dass -w größer als 0 sein muss. | Ausgabe "Fehler: Der Parameter -w muss größer als 0 sein (angegeben: 0)." Wie erwartet. |
| 13 | `python3 main.py nix.bmp -w abc -h 100` | Fehlermeldung, dass "abc" keine Zahl ist. | Ausgabe "Fehler: argument -w: invalid int value: 'abc'". Wie erwartet. |
| 14 | `echo "kein bild" > text.txt` und dann `python3 main.py text.txt -x 1 -y 1 -r 5` | Fehlermeldung, dass es keine Bitmap ist. Die Datei text.txt bleibt gleich. | Ausgabe "Fehler: Keine gültige Bitmap-Datei (Signatur 'BM' fehlt oder Datei ist zu kurz)." Mit `cat text.txt` steht dort weiterhin "kein bild". Wie erwartet. |

Von 14 Tests geklappt: Alle 14 haben geklappt. 

Zusätzlich habe ich test.py gestartet: 11 Tests, Ergebnis ist OK.

Was nicht geklappt hat: Nichts.