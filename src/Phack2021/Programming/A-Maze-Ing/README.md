# A-Maze-Ing - 256 points

## Problème

```
Un étrange serveur souhaite vous mettre à l'épreuve.
Soyez à la hauteur.

=== Connexion ===
Serveur : a-maze-ing.phack.fr
Port : 4242
```

## Résolution

En se connectant sur l'URL, voici les informations qu'on a:

![image-20210406193226899](C:\Users\cleme\AppData\Roaming\Typora\typora-user-images\image-20210406193226899.png)

On peut essayer de faire une requête GET sur la route http://a-maze-ing.phack.fr:4242/chall pour voir ce qu'on nous donne:

```
$ curl -X GET "http://a-maze-ing.phack.fr:4242/chall"
{"token": "c612355bbaed4a5ab9d2b3c593d90903", "solveMe": "######################x  #         #   # #### # ##### # # # # ##   #   #   #   #   ## ### ### ######### ## # # #   #     # # ## # # # ##### # # # ## #   #     # #   # ## # ####### # ##### ## #       # #     # ## ##### ### # ### # ##   #   #   #   #   #### ### # ##### ###### #   # #   # #   # ## ### ##### # ### # ##   #   #   # #   # ## ##### # ### # ### ##     #   # #   #   ## ### ##### # ### # ##   #             #$######################"}
```

Vu le nom du challenge et ce qu'on nous recevons, on peut se douter qu'on va devoir résoudre le labyrinthe donné dans la réponse. Mais d'abord, essayons de reformer le labyrinthe:

![image-20210406193610511](C:\Users\cleme\AppData\Roaming\Typora\typora-user-images\image-20210406193610511.png)

On comprend assez bien qu'on doit partir du "x" et se rendre jusqu'au "$", mais comment soumettre la solution ? On peut donc essayer de soumettre une solution au hasard sur la route /chall en POST, et voir la réponse du serveur:

```sh
$ curl -X POST "http://a-maze-ing.phack.fr:4242/chall"
Expected json format : { "token" : "", "solution" : "" }
```

Adaptons la requête:

```sh
$ curl -X POST http://a-maze-ing.phack.fr:4242/chall -H "Content-Type: application/json" -d "{\"token\":\"c612355bbaed4a5ab9d2b3c593d90903\",\"solution\":\"ma_super_solution\"}"
Wrong token or time is over
```

Le token semble avoir expiré, ce qui est normal vu qu'on a mis plus de 5 secondes à répondre. En automatisant, voilà la réponse qu'on obtient:

```python
$ cat test.py 
import requests
import json

# On récupère le labyrinthe et le token
url = "http://a-maze-ing.phack.fr:4242/"
to_solve = json.loads(requests.get(url+"chall").text)

print("Maze token:", to_solve["token"])

# On prépare notre réponse avec le token et n'importe quelle solution
params = {
	"token": to_solve["token"],
	"solution": "ma_super_solution"
}


print("Sending solution:", params)

# On l'envoit et on affiche la réponse
s = requests.post(url+"chall", json=params)

print(s, s.text)

clem@ubuntu:~/Desktop/phack/prog/laby$ python3 test.py 
Maze token: b7cfe7a37b0b4557a128eb4487e86b76
Sending solution: {'token': 'b7cfe7a37b0b4557a128eb4487e86b76', 'solution': 'ma_super_solution'}
<Response [200]> "Solution" field must match "^[↑↓←→]*$"
```

Super, on a notre réponse; on doit envoyer la solution sous la forme de flèches. Il ne reste plus qu'a trouver une façon de résoudre le labyrinthe et de l'envoyer! Pour ça, j'ai trouvé un [script sur internet](https://gist.github.com/a613/49d65dc30e98c165d567). La plupart du temps de résolution du challenge a en fait été prise par l'adaptation de ce script pour les besoins sur challenge, car ce script était fait pour Python 2.x et surtout ne renvoyait pas la solution sous la forme que nous voulons (les flèches), il a donc fallut l'adapter pour qu'au lieu de juste renvoyer la solution sous forme de labyrinthe dans le fichier "out.txt", le solveur renvoie également la solution sous forme de flèches. J'ai donc opté pour une technique de gros porc, c'est-à-dire ne changer que le strict minimum. Le script se fait donc toujours exécuter avec la commande `python3 solver.py in.txt out.txt`, et donc ma technique a été d'appeler ce script avec la méthode "system" du module "os". Voici le solveur adapté:

+ [solver.py](solver.py) 

Et voici l'utilisation que j'en fais avec le fichier "exploit.py": (non modifiée depuis le CTF, toujours pas propre)

```python
import requests
import json
from os import system

dirs = {
	"up": "↑",
	"down": "↓",
	"left": "←",
	"right": "→"
}

url = "http://a-maze-ing.phack.fr:4242/"
to_solve = json.loads(requests.get(url+"chall").text)

print("Maze token:", to_solve["token"])

to_solve["solveMe"] = to_solve["solveMe"].replace("x","S").replace("$","E")

with open("in.txt", "w") as fin:
	lines = int(len(to_solve["solveMe"])/22)
	fin.write("\n".join(to_solve["solveMe"][line*21:line*21+21] for line in range(lines+1)))

system("python3 solver.py in.txt out.txt")

with open("path.txt", "r") as fin:
	path = fin.read()
	print("Path to send:", path)


	params = {
		"token": to_solve["token"],
		"solution": "↓" + path
	}


	print("Sending solution:", params)


	s = requests.post(url+"chall", json=params)

	print(s)
	print(s.text)
```

+  [exploit.py](exploit.py) 

Voici la sortie:

```shell
$ python3 exploit.py 
Maze token: 96cc6ed6b5eb45d795dc79eaaaa00930
Path to send: ↓↓↓→→↑↑↑↑→→↓↓→→→→↑↑→→↓↓→→↓↓↓↓↓↓↓↓↓↓←←↓↓←←↑↑←←↑↑→→↑↑→→↑↑←←←←↓↓←←↑↑←←↓↓←←↓↓↓↓↓↓↓↓↓↓→→→→↑↑→→↓↓→→→→→→→→↑↑→→→→↓↓
Sending solution: {'token': '96cc6ed6b5eb45d795dc79eaaaa00930', 'solution': '↓↓↓↓→→↑↑↑↑→→↓↓→→→→↑↑→→↓↓→→↓↓↓↓↓↓↓↓↓↓←←↓↓←←↑↑←←↑↑→→↑↑→→↑↑←←←←↓↓←←↑↑←←↓↓←←↓↓↓↓↓↓↓↓↓↓→→→→↑↑→→↓↓→→→→→→→→↑↑→→→→↓↓'}
<Response [200]>
Congrats ! The flag is PHACK{M4zEs_4Re_7rUly_4m@zIng}
```

**Flag: `PHACK{M4zEs_4Re_7rUly_4m@zIng}`**