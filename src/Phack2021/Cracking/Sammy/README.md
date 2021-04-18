# Sammy - 256 points
On se retrouve avec un fichier `system` et un fichier `sam`. Ce sont des fichiers similaires à shadow sous linux, qui contiennent des informations sur les mots de passe des utilisateurs. On utilisera l'outil `hivexsh` pour ce challenge.
```bash
> hivexsh sam
> cd SAM
> sam\SAM> cd Domains
> sam\SAM\Domains> cd Account
> sam\SAM\Domains\Account
```
Avec `ls`, on trouve `Users`, on explore les clefs et on trouve dans `00003E9` et grâce à `lsval`,  on trouve une clef très interessante: `UserPasswordHint`.
Finalement, en utilisant `lsval UserPasswordHint`, on obtient le flag :).