# Teaching Factory - Regression Results

## Regression von ausgelesenen Daten

Mit den folgenden Daten wurde ein Regressionsmodell mit folgender Genauigkeit erstellt:

| Genutzte Spalten | Modell-Typ  | MSE-Wert (Training) | MSE-Wert (Test) |
|------------------|-------------|---------------------|---------------|
| Alle             | Linear      | 0.12                | 0.119         |
| fill-lvls excl.  | Linear      | 0.13                | 0.116         |
| vibrations excl. | Linear      | 53.36               | 55.19         |
| Alle             | Ridge       | 0.12                | 0.1186        |
| fill-lvls excl.  | Ridge       | 0.133               | 0.116         |
| Alle             | Lasso       | 0.12                | 0.1199        |
| fill-lvls excl.  | Lasso       | 0.133               | 0.116         |
| Alle             | Polynom (2) | 0.219               | 4.03          |

Bestes Regressionsmodell: Lineare Regression ohne Füllstände

## Regression an Datensatz 'X.csv'

Die Ergebnisse der durchgeführten Regression, nämlich das vorhergesehene Gewicht der Flaschen basierend auf den bereitgestellten Daten in 'X.csv', wurden im Verzeichnis './database/52216067-62200066-61901292.csv' abgespeichert