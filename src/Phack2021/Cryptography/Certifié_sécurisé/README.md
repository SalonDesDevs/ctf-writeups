# Certifié sécurisé - 256 points

On trouve l'image Docker sur [hub.docker.com](https://hub.docker.com/layers/phackctf/challenge/latest/images/sha256-3bcce5574805a24195a3a48b160605a07a62a9e33e0f1c0969de51fe8c3cdbe4?context=explore)

On peut alors la mettre en place afin de naviguer en tant que `root` dans ses dossiers : 

```bash
docker pull phackctf/challenge
sudo dockerd &
sudo docker run -i -t bd2940a6f086 /bin/bash
```

on retrouve la clé privée associée au certificat `phack.key` dans le dossier `/cert`

On peut ensuite l'utiliser dans un logiciel comme Wireshark pour déchiffrer les échanges HTTPS avec
le site, dans lesquels on accède au mot de passe qui constitue (une fois qu'on l'enveloppe de `PHACK{}`) le flag.

Procédure (graphique) pour Wireshark : Editer - Préférences - Protocols - TLS - Edit (RSA keys list) - ajouter son key file ; et au besoin IP serveur | port HTTPS (443) | tls ; ainsi qu'éventuellement la passphrase de la clé privée.