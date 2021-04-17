# Harduino - 256 points

On est face à une jolie interface qui fait afficher du texte sur une Arduino imaginaire.

En regardant les requêtes on constate que l'affichage est réalisé par une page PHP, dont l'url exact nous est d'ailleurs donné, ainsi que le code à l'accueil.

On constate de plus que l'argument url `message`, qui constitue ce qui sera affiché, est passé, après se voir ajouter à l'avant et à l'arrière des guillemets à une regex finissant par `/e` dans `preg_replace`. La documentation PHP nous informe qu'il s'agit d'un modifier déprécié permettant d'utiliser du code PHP dans la regex.

On va donc ajouter des guillemets afin d'écrire du code qui sera évalué en tant que tel, lisant le flag, qu'on concaténe aux deux chaînes vides qu'on créé autour : `".file_get_contents('../../../../flag.txt')."`

```
http://harduino.phack.fr/workspace/apps/arduino/arduino.php?message=%22.file_get_contents(%27../../../../flag.txt%27).%22
```

affiche lentement le flag sur l'écran LCD.