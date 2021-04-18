# Une douce petite musique - 256 points

## Problème

```
Avec vos talents de hacker vous interceptez un échange plutôt louche. 
```

+  [message1.eml](..\AppData\Local\Temp\message1.eml) 

+  [message2.eml](..\AppData\Local\Temp\message2.eml) 

## Résolution

Ce challenge était très simple, mais nous a demandé beaucoup de temps... La première étape est plutôt évidente, puisqu'en ouvrant les deux fichiers mails, on remarque directement des grosses parties de base64 avec des noms de fichiers adjacents: "musique.mid" et "audio.ods". On peut récupérer les deux fichiers soit en ouvrant les fichiers dans une boîte mail comme Thunderbird, soit en transformant les base64 en fichier avec n'importe quel outil en ligne (ma solution, car plus rapide).
Voici à quoi ressemble le tableur:

![image-20210406202632094](C:\Users\cleme\AppData\Roaming\Typora\typora-user-images\image-20210406202632094.png)

Nous avons ensuite ouvert le fichier midi dans le premier site qui prétendait pouvoir le faire, et voici un extrait de ce que nous pouvons voir:

![image-20210406202817520](C:\Users\cleme\AppData\Roaming\Typora\typora-user-images\image-20210406202817520.png)

Bien que je ne l'ai pas vu tout de suite, les notes indiques des positions dans le tableur, qui est lui-même une table de correspondances avec les lettres qu'il contient. La seule fourberie était de remarque que les numéros après les notes devait être décrémentés de 3 unités. Par exemple pour la première note G4, on obtient G1 en faisant notre petite opération et on remarque la case G1 dans le tableur est "P". Si on répète cette technique sur les six premières lettres, on obtient "PHACK{". Il aurait été possible d'automatiser la conversion pour toutes les notes, mais j'ai préféré le faire à la main et vu que les notes se répétaient souvent, c'est allé assez vite.

**Flag: PHACK{\_ALLUMER\_LE\_FEU\_ALLUMER\_LE\_FEU\_ET\_FAIRE\_DANSER\_LES\_DIABLES\_ET\_LES\_DIEUX\_ALLUMER\_LE\_FEU\_ALLUMER\_LE\_FEU\_ET\_VOIR\_GRANDIR\_LA\_FLAMME\_DANS\_VOS\_YEUX\_ALLUMER\_LE\_FEU\_}**