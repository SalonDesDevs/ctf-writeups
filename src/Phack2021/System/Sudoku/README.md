# Sudoku - 128 points

Le nom du challenge, et ses tags, laissent savoir que celui-ci porte sur `sudo`. Une fois connecté par ssh, `sudo -l` nous informe que nous pouvons utiliser `zip` en tant que `master` auquel le fichier cible est lisible.

On peut donc zip le fichier en question en tant que master : `sudo -u master zip archive ../master/flag.txt`.

On peut ensuite lire le flag directement dans le zip.