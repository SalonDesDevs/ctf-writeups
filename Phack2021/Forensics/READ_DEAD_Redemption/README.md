## RAID Dead Redemption - 512 points

### Problème

```
Vous travaillez à la brigade spéciale du service cyberdéfense de la gendarmerie de Montargis.

Les disques dur d'une femme ont été saisis et viennent de vous être transmis. Elle est suspectée d'avoir téléchargé de nombreux fichiers PNG et JPG dont elle n'avait pas la propriété intellectuelle. Mais il semblerait qu'elle ait eu le temps de supprimer une partie des preuves avant l'intervention. Faites de votre mieux pour en extraire le maximum !

Le manuel d'un logiciel suspect tournant sur l'ordinateur a également été retrouvé et vous a été transmis pour vous guider dans votre enquête.
```

+  [Notice_Mastok_3000.pdf](https://filebin.net/oi3yn5ptwwkxrj5p/Notice_Mastok_3000.pdf?t=dn2zkydq) 

+  [files.zip](https://filebin.net/ph6v9sz252y45lj0/files.zip?t=e2ds5pxp) 

  ### Résolution

  On nous donne une documentation technique faite maison qui parle de disque montés en RAID5, et aussi 3 fichiers, respectivement DISK1.bin, DISK2.bin et DISK3.bin. Ces trois partitions semblent donc faire partie d'un système RAID5, sauf qu'en analysant les fichiers avec la commande `file`, on remarque que le disque 2 est vide:

  ```idl
  $ file ./DISK*
  DISK1.bin: data
  DISK2.bin: empty
  DISK3.bin: data
  ```

  Or, comme les partitions viennent d'un système monté en RAID5, une partition est simplement le XOR de deux autres. On peut donc XORer les partitions 1 et 3 pour récupérer la deuxième:

  ```python
  with open("DISK1.bin", "rb") as fin:
      disk1 = fin.read()
  
  with open("DISK3.bin", "rb") as fin:
      disk3 = fin.read()
  
  disk2 = "".join([chr(int(d1) ^ int(d3)) for d1, d3 in zip(disk1, disk3)])
  
  with open("DISK2_RECOVERED.bin", "wb") as fout:
  	fout.write(bytes(disk2, "utf-8"))
  ```

  Ainsi, on obtient notre deuxième disque. Maintenant, on va pouvoir ré-écrire les données contenues dans les disques en se servant des 3 partitions qu'on a, et des informations données dans la notice (comme la taille des blocs à écrire ou la parité):

  <sup>(je lie une version commentée du code ci-dessous, pour éviter de trop remplir le document)</sup>

  ```python
  with open("DISK1.bin", "rb") as fin:
      disk1 = fin.read()
  
  with open("DISK2_RECOVERED.bin", "rb") as fin:
      disk2 = fin.read()
  
  with open("DISK3.bin", "rb") as fin:
      disk3 = fin.read()
  
  raidArray = [disk1, disk2, disk3]
  
  BLOCKSIZE = 1
  
  with open("data", "wb") as fout:
          for blockIndex in range(int(len(disk1) / BLOCKSIZE)):
                  parityIndex = (2 - blockIndex) % 3
  
                  for driveIndex in range(3):
                          if driveIndex != parityIndex:
  
                                  blockStart = blockIndex * BLOCKSIZE
  
                                  fout.write(raidArray[driveIndex][blockStart:blockStart + BLOCKSIZE])
  ```

  + [rebuilder_commente.py](https://filebin.net/ph6v9sz252y45lj0/rebuilder_commente.py?t=0p9q07jd) 

  

  Avec ce script on obtient donc les données des disques:

  ```idl
  $ file data
  data: PNG image data, 706 x 242, 8-bit non-interlaced
  ```

  C'est une image! C'est bon signe car c'est ce qui était demandé dans la consigne: de retrouver les images volées. Voici l'image en question:

  ![image-20210406190421642](https://i.imgur.com/vJDEFGY.png)

  Rien de très concluant... Mais foremost arrive à extraire des données de cette image, donc voici un screen du dossier "output/" qu'il produit:

  ![image-20210406190758800](https://i.imgur.com/bDCaoV8.png)

En fouillant dans le dossier jpg/, on trouve ces images:

![image-20210406190837299](https://i.imgur.com/xt0W09j.png)

Dont celle-ci: ([00000752.jpg](https://i.imgur.com/4ZNCXjB.png))

![image-20210406190923749](https://i.imgur.com/4ZNCXjB.png)

Malgré la qualité déplorable, on a le flag! Le reste des images n'étaient que des [memes que voici](https://filebin.net/qvmv7tnwuiw3vce8/memes_RAID.zip?t=qu9zv7zu).

**Flag: `PHACK{R41d_1s_N1cE_7hANk_U2_m4s7ok_3000!!}`**
