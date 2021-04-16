# Mr Weak - 256 points

On recherche un "Johnny Weak". [sherlock](https://github.com/sherlock-project/sherlock) peut donner des idées de réseaux / sites à regarder (l'output est toujours rempli de faux positifs néanmoins).

On trouve alors un https://github.com/johnnyweak dont l'avatar est analogue au logo du CTF. Celui-ci possède un repository "secret-project", dans lequel on trouve notamment un historique `.bash_profile` et une clé privée `id_rsa`.

À la fin de l'historique Johnny nous donne gentiment comment accéder à son serveur à l'aide de la clé privée adjointe : `ssh -p6969 -i id_rsa johnnyweak@secr3t-pr0j3cts.phack.fr`. Sur celui-ci il ne reste plus qu'à `cat` le fichier contenant le flag.

