# Status der Implementierung das Pokeball-Renderer 

| Nr. | Anforderung                                | Stand    | Anmerkung |
|---|--------------------------------------------|----------|---|
| 1 | Pokeball in eine vorhandene Bitmap rendern | umgesetzt | Die Bitmap wird mit `Bitmap.read` gelesen, der Ball gezeichnet und die Datei wieder gespeichert (Test 6). |
| 2 | Neue Bitmap mit Pokeball erzeugen          | umgesetzt | Gibt es die Datei nicht, wird sie mit `-w` und `-h` neu erstellt, der Hintergrund ist grau (Tests 1 bis 5). |
| 3 | Breite und Höhe mit -w und -h angeben      | umgesetzt | `-w` und `-h` müssen zusammen angegeben werden und größer als 0 sein (Tests 3, 11, 12). |
| 4 | Mittelpunkt mit -x und -y angeben          | umgesetzt | Ohne Angabe liegt der Ball in der Mitte. Teile außerhalb des Bildes werden nicht gezeichnet (Tests 2, 4). |
| 5 | Radius mit -r angeben                      | umgesetzt | Ohne Angabe ist der Radius die Hälfte der kleineren Bildkante (Test 5). |
| 6 | pokerush: 10 bis 100 zufällige Pokebälle   | umgesetzt | Zufällige Anzahl, Position und Radius (10 bis halbe kleinere Kante). Das Bild muss mindestens 20 Pixel Kantenlänge haben (Tests 7, 8). |
| 7 | Fehlermeldungen bei falschen Eingaben      | umgesetzt | Eigene Fehlerklassen, Ausgabe mit "Fehler: ..." und Rückgabewert 1 (Tests 8 bis 14). |