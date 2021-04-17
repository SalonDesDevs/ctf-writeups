# Ben & Harry - 128 points

## Problème

```idl
Ben vient de découvrir un drôle de serveur qui semble envoyer des suites de chiffres aléatoires.

Harry est sûr que ça doit vouloir dire quelque chose.
Prouve que Harry a raison.

=== Connexion ===
Serveur : ben-and-harry.phack.fr
Port : 1664 
```

## Résolution

En se connectant pour la première fois au serveur, voici ce qu'on obtient:

```json
$ nc ben-and-harry.phack.fr 1664
{"b": 11, "code": "78 a0 2a 90 95 44 90 44 99 48 a6 2a 90 44 a0 a6 a4 47 2a 99 47 2a 93 99 48 94 40 2a 91 47 5a 99 58", "msg": "Answer me!"}
>>> 
```

Au début, je pensais que nous avions la main sur un interpréteur Python, mais taper n'importe quoi m'a fait mentir (et perdre la main):

```idl
>>> print(1)
✞ Nope, wrong answer...
```

En regardant le message donné, il n'est pas très compliqué de comprendre qu'il faut décoder la valeur de "code" avec la base "b", et un "msg" inutile.
Voici un script possible en Python:

```python
from pwn import *
import json

conn = remote("ben-and-harry.phack.fr", 1664)

while r := conn.recvline():
        print("[RECEIVED] ", r)

        try:
                r = r.decode("utf-8")

                if r.startswith(">>>"): # Si ce n'est pas le premier, on doit découper le début
                        r = json.loads(r[3:])
                else:
                        r = json.loads(r)


                res = ""
                for char in r["code"].split(): # Pour chaque caractère
                        res += chr(int(char, r["b"]))

                print(res)
                print();print() # Saute des lignes

                conn.send(bytes(res, "utf-8"))
        except Exception as e:
                if "PHACK{" in r: print("BINGO!!! FLAG:", r)
                exit(0)
```

+ [exploit.py](exploit.py) 

**Flag: `PHACK{Av3z-v0us-L3s-b4s3s?}`**