## Piraterie (Ep 3) - 512 points

### Problème

```
Sachant ce qui a été dérobé, il faut maintenant retrouver le malfrat.
Retracez son parcours et retrouvez l'IP ainsi que le port de connexion qu'il a utilisé pendant son attaque.

Le flag est de la forme PHACK{...} avec le résultat de IP:PORT encodé en base 64. 
```

### Résolution

Cette partie du challenge est selon moi plus facile que la précédente. Étant donné qu'un "malware" a infecté le PC, on peut penser que le processus malicieux est encore allumé sur l'ordinateur de la victime. On peut lister tout les processus utilisant la connexion sur la machine avec la commande `netscan`: (résultat tronqué)

```idl
0x7f191890      TCPv4      0.0.0.0:49153       0.0.0.0:0              LISTENING       820       svchost.exe
0x7f191890      TCPv6      :::49153            :::0                   LISTENING       820       svchost.exe
0x7fc2fcd0      TCPv4      -:49478             172.217.22.142:443     CLOSED          3040      firefox.exe
0x7fc64008      TCPv4      10.0.2.15:49461     185.13.37.99:1337      ESTABLISHED     4440      powershell.exe
0x7fc9a008      TCPv4      -:49480             172.217.22.142:443     CLOSED          3040      firefox.exe
0x7fc9a798      TCPv4      127.0.0.1:49415     127.0.0.1:49416        ESTABLISHED     2072      firefox.exe
0x7fcc4890      TCPv4      10.0.2.15:49489     216.58.213.78:443      ESTABLISHED     3040      firefox.exe
```

On y voit tout les processus, y compris un qui semble suspect: "powershell.exe". On nous donne l'ip et le port sous la forme demandé, il ne nous resque plus qu'à l'encoder et à tester le flag.

```shell
$ echo "185.13.37.99:1337" | base64
MTg1LjEzLjM3Ljk5OjEzMzcK
```

On reçoit les points en ajoutant l'enrobage, bingo!

**Flag: `PHACK{MTg1LjEzLjM3Ljk5OjEzMzcK}`**
