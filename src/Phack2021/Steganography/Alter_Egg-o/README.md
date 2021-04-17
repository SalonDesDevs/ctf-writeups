# Alter Egg-o - 256 points

Le fichier (un PNG) est apparemment corrompu, si on y jette un coup d'oeil dans un éditeur de texte les headers (IHDR, IEND...) ont l'air épargnés, le seul problème flagrant est le début du fichier qui n'arbore pas la signature de tous les fichiers PNG : 89 50 4E 47 0D 0A 1A 0A (dont les 2e à 4e octets sont notamment 'PNG').

En remplaçant correctement ces 4 premiers octets (89 50 4E 47), le fichier peut être lu correctement et il s'agit du flag par dessus une image.