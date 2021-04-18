# Caumunikassion - 128 points

Le site de l'épreuve est le site du CTF, en supposant qu'on ne regarde que la page d'accueil notre intérêt se porte sur le glitch de la date et le logo. Un rapide coup d'oeil au code-source (dans les sources JavaScript de la page) du glitch nous fait comprendre que celui-ci est aléatoire. Reste l'image.

En commentaire dans ses données Exif (vues avec `exiftool`) est un url pastebin, sur lequel on trouve le flag.