# Teaching Factory - Classification Results

## Bestimmung von beschädigten Flaschen durch Vibrationsmessungen

Es wurden folgende Klassifizierungsmodelle mit folgenden Daten verwendet:

| Genutzte Daten      | Modell-Typ     | F1-Wert (Training)  | F1-Wert (Test)| Konfusionsmatrix |
|---------------------|----------------|---------------------|---------------|------------------|
| Mittelwert          | Decision-Tree  | 1.00                | 0.00          |<table><tr><td>81</td><td>0</td></tr><tr><td>3</td><td>0</td></tr></table>|
| Dominante Frequenz  | Decision-Tree  | 1.00                | 0.80          |<table><tr><td>81</td><td>0</td></tr><tr><td>1</td><td>2</td></tr></table>|
| MW + dom. Freq.     | Decision-Tree  | 1.00                | 0.80          |<table><tr><td>81</td><td>0</td></tr><tr><td>1</td><td>2</td></tr></table>|
| Mittelwert          | KNNeighbors    | 0.00                | 0.00          |<table><tr><td>81</td><td>0</td></tr><tr><td>3</td><td>0</td></tr></table>|
| Dominante Frequenz  | KNNeighbors    | 1.00                | 0.80          |<table><tr><td>81</td><td>0</td></tr><tr><td>1</td><td>2</td></tr></table>|
| MW + dom. Freq.     | KNNeighbors    | 1.00                | 0.80          |<table><tr><td>81</td><td>0</td></tr><tr><td>1</td><td>2</td></tr></table>|
| Mittelwert          | Logistic Regr. | 0.00                | 0.00          |<table><tr><td>81</td><td>0</td></tr><tr><td>3</td><td>0</td></tr></table>|
| Dominante Frequenz  | Logistic Regr. | 1.00                | 0.80          |<table><tr><td>81</td><td>0</td></tr><tr><td>1</td><td>2</td></tr></table>|
| MW + dom. Freq.     | Logistic Regr. | 1.00                | 0.80          |<table><tr><td>81</td><td>0</td></tr><tr><td>1</td><td>2</td></tr></table>|

Für die dominanten Frequenzen wurde eine Fourier-Transformation mit den folgenden Sampling-Raten durchgeführt: [50, 100, 150]  
Es wurden alle drei Ergebnisse in den Modellen eingebunden.

Alle drei Modelle liefern halbwegs verlässliche Klassifikationen, solange die dominante Frequenz als Parameter zum Trainieren des Modells mit-verwendet wird. Die reine Verwendung des Mittelwertes liefert keine verlässliche Vorraussage.

(Strg + Shift + V für Markdown-Preview in VS-Code)