## Android Cloud - 128 points

### Problème

```
Un service américain propose de se débarasser définitivement de son smartphone grâce à sa nouvelle  plateforme de AaaS (Android as a Service).

Mais méfiant de nature, vous décidez d'aller vérifier par vous même que la sécurité correspond à vos standards.

Lien du challenge : http://android-cloud.phack.fr 
```

### Résolution

En arrivant sur le site, on a un téléphone Android qui est verrouillé par un pattern. On peut essayer d'en faire au hasard, mais cela n'affiche juste "Wrong code". Il faut trouver une manière de le deviner.

![image-20210403193523500](https://i.imgur.com/Z03CnWH.png)

En bas à gauche du site, on a une rubrique "Last <u>backup</u> on Sat Mar 10 2020, 17:16:18 (UTC+1)". En cliquant sur le mot souligné "backup", on arrive sur le code d'un fichier .php dont voici le début:

```php
# For debug, must remove later !!!
highlight_file ( __FILE__, false ); die();

$filename = "backup@" . date("m-d-Y") . ".zip";
$archive  = new ZipArchive();

if (!$archive->open("./dev-backups/" . $filename, (ZipArchive::CREATE | ZipArchive::OVERWRITE))) {
    die("Archive init failed");
}
```

On remarque que le nom de fichier d'une backup commence toujours pas "backup@", puis contient la date sous la forme "mois-jour-année" et enfin l'extension ".zip".

Ayant la date de la dernière backup, on peut former le string suivant: `backup@03-10-2020.zip`.

Grâce à la suite du code, on sait que les backups sont stockées dans le dossier `dev-backups/`.

On a donc le chemin complet de la dernière backup: `url/dev-backups/backup@03-10-2020.zip`, ce qui nous fait télécharger l'archive quand on s'y rend. Une fois l'archive téléchargée, on la décompresse et on obtient ce qui semble être un système Android:

![image-20210403194727409](https://i.imgur.com/NsrIx08.png)

On va donc essayer de cracker le code avec le fichier ou il est stocké, ``gesture.key`` dans ``data/system/gesture.key``.

Il existe plein d'outils pour obtenir le code, j'ai utilisé celui-ci: https://github.com/sch3m4/androidpatternlock

```sh
clem@ubuntu:~/Desktop/phack/forensics/android$ python2 aplc.py ./data/system/gesture.key 

################################
# Android Pattern Lock Cracker #
#             v0.2             #
# ---------------------------- #
#  Written by Chema Garcia     #
#     http://safetybits.net    #
#     chema@safetybits.net     #
#          @sch3m4             #
################################

[i] Taken from: http://forensics.spreitzenbarth.de/2012/02/28/cracking-the-pattern-lock-on-android/

[:D] The pattern has been FOUND!!! => 04137658

[+] Gesture:

  -----  -----  -----
  | 1 |  | 3 |  |   |  
  -----  -----  -----
  -----  -----  -----
  | 4 |  | 2 |  | 7 |  
  -----  -----  -----
  -----  -----  -----
  | 6 |  | 5 |  | 8 |  
  -----  -----  -----

It took: 0.6148 seconds
```

On obtient le code ainsi que le chemin à dessiner, qu'on peut directement faire sur le site:

![image-20210403195755304](https://i.imgur.com/mnl3UcM.png)

**Flag: ``PHACK{T4kec4rE_oF_Ur_B4cKupS!}``**
