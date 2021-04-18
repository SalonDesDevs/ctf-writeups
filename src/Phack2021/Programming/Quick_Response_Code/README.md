# Quick Response Code - 128 points

## Problème

```
Philippe XXXIV, roi de Macédoine et descendant de Philippe II, souhaiterais cacher son mot de passe sur son ordinateur pour éviter qu'on puisse facilement lui dérober. Mais pas question pour Philippe d'utiliser un gestionnaire de mot de passe (qui serait digne de garder le précieux mot de passe d'un roi après tout ?). Il décide donc d'appliquer le célèbre principe de son arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-arrière-grand-père : diviser pour mieux... enfin vous avez compris. 
```

+  [data.zip](..\AppData\Local\Temp\data.zip) 

## Résolution

En décompressant l'archive, on obtient un dossier avec près de 2000 codes QR... Vu la quantité d'images, on ne peut pas tout scanner à la main. Ma première approche a été de penser qu'un seul code contenait le flag, et donc voici ma première tentative:

```python
from glob import iglob
from PIL import Image
from pyzbar.pyzbar import decode

for filepath in iglob("./out/*.png"):
        decoded = decode(Image.open(filepath))[0][0]
        if "PHACK{" in str(decoded):
                print(f"Données: {decoded} \nChemin: {filepath}")
```

Or, rien ne sort... Donc le flag n'est pas dans une seule image, mais peut-être dans plusieurs. J'ai donc ensuite décidé d'imprimmer chaque "decoded" à chaque itération, et dans les premières images, on trouve:

```idl
...
b'Nothing here (id = 0xbbe6e6d923ca40da91eef6aebfaa6331)'
b'Nothing here (id = 0x23dfffe762be47098abe11d250fcf409)'
b'Nothing here (id = 0xff8e269ec7a749ce9dbeae198d4aef15)'
b'Flag char 1 is "H" (id = 0x52e5067410b140aaba159ab3f589d9dc)'
b'Nothing here (id = 0xaeb605c2eab14e5380f5fb72b3d449b7)'
b'Nothing here (id = 0x364bab3371654dd1aacbdcce64da55b5)'
b'Nothing here (id = 0x62c9411324f34f7d874de30ab8126d78)'
...
```

Le flag semble être donné par caractère. J'ai décidé de le faire rapidement, à défaut d'être propre:

```python
from glob import iglob
from PIL import Image
from pyzbar.pyzbar import decode

FLAG = [0]*100

for filepath in iglob("./out/*.png"):
	decoded = decode(Image.open(filepath))[0][0]

	if "Flag" in str(decoded):
		idx = int(decoded.split()[2])
		char = chr(decoded.split()[4][1])
		# print(idx, char)
		FLAG[idx] = char

print("".join(str(e)for e in FLAG))
```

```idl
$ python3 solve.py 
PHACK{MaaaYb3_Th1s_Waas_Overk1lL?!}00000000000000000000000000000000000000000000000000000000000000000
```

**Flag: `PHACK{MaaaYb3_Th1s_Waas_Overk1lL?!}`**