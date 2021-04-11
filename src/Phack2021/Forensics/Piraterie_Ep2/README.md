## Piraterie (Ep 2) - 512 points

### Problème

```
Il semble que le pirate ait réussi à récupérer des informations confidentielles qui étaient visibles sur le bureau.
Validez cette hypothèse et retrouvez cette information.
```

### Résolution

La première chose logique à faire en lisant l'énnoncé est de regarder le contenu du bureau. Pour ça, on a la commande `filescan` à laquelle on va piper `grep "\Desktop"`:

```shell
$ ./volatility_2.6_lin64_standalone -f dump.raw --profile=Win7SP1x86_23418 filescan | grep "\Desktop"
Volatility Foundation Volatility Framework 2.6
0x000000007ce4ae68      1      1 R--rw- \Device\HarddiskVolume1\Users\Mes-vms.fr\Desktop
0x000000007d10ca70      1      1 R--rw- \Device\HarddiskVolume1\Users\Mes-vms.fr\Desktop
0x000000007d1b71a8      1      1 R--rw- \Device\HarddiskVolume1\Users\Mes-vms.fr\Desktop
0x000000007d258778      7      0 R--rwd \Device\HarddiskVolume1\Users\Mes-vms.fr\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Maintenance\Desktop.ini
0x000000007d258b68      7      0 R--rwd \Device\HarddiskVolume1\Users\Mes-vms.fr\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Accessories\Accessibility\Desktop.ini
0x000000007d30a1c0      1      1 R--rw- \Device\HarddiskVolume1\Users\Mes-vms.fr\Desktop
0x000000007d33e9b0      7      0 R--rwd \Device\HarddiskVolume1\Users\Mes-vms.fr\Desktop\desktop.ini
0x000000007d34f4f8      8      0 R--rwd \Device\HarddiskVolume1\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\System Tools\Desktop.ini
0x000000007d34fd08      7      0 R--rwd \Device\HarddiskVolume1\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Desktop.ini
0x000000007d35ace8      7      0 R--rwd \Device\HarddiskVolume1\Users\Mes-vms.fr\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Accessories\System Tools\Desktop.ini
0x000000007d38b378      8      0 R--rwd \Device\HarddiskVolume1\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Tablet PC\Desktop.ini
0x000000007d38ba58      8      0 R--rwd \Device\HarddiskVolume1\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Accessibility\Desktop.ini
0x000000007d38ce50      8      0 R--rwd \Device\HarddiskVolume1\ProgramData\Microsoft\Windows\Start Menu\Programs\Maintenance\Desktop.ini
0x000000007d3c0f80      1      1 R--rw- \Device\HarddiskVolume1\Users\Mes-vms.fr\Desktop
0x000000007d3fc518      2      1 R--rwd \Device\HarddiskVolume1\Users\Public\Desktop
0x000000007d3fc7f0      2      1 R--rwd \Device\HarddiskVolume1\Users\Public\Desktop
0x000000007d3fcac8      2      1 R--rwd \Device\HarddiskVolume1\Users\Mes-vms.fr\Desktop
0x000000007d3fcda0      2      1 R--rwd \Device\HarddiskVolume1\Users\Mes-vms.fr\Desktop
0x000000007ee66570      7      0 R--rwd \Device\HarddiskVolume1\Users\Mes-vms.fr\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Accessories\Desktop.ini
0x000000007ee668a8      7      0 R--rwd \Device\HarddiskVolume1\Users\Public\Desktop\desktop.ini
0x000000007fc9af80      8      0 R--rwd \Device\HarddiskVolume1\Windows\Web\Wallpaper\Characters\Desktop.ini
0x000000007fca7260      8      0 R--rwd \Device\HarddiskVolume1\Windows\Web\Wallpaper\Landscapes\Desktop.ini
0x000000007fca79d8      8      0 R--rwd \Device\HarddiskVolume1\Windows\Web\Wallpaper\Architecture\Desktop.ini
0x000000007fd21900      8      0 R--rwd \Device\HarddiskVolume1\Windows\Web\Wallpaper\Nature\Desktop.ini
0x000000007fd3c908      1      1 R--rw- \Device\HarddiskVolume1\Users\Mes-vms.fr\Desktop
0x000000007fd44e00      8      0 R--rwd \Device\HarddiskVolume1\Users\Mes-vms.fr\AppData\Roaming\Microsoft\Windows\SendTo\Desktop.ini
0x000000007fe2f5f0      8      0 R--rwd \Device\HarddiskVolume1\Windows\Web\Wallpaper\Scenes\Desktop.ini

```

On obtient plein de chemins, mais rien de concluant... J'ai quand même durant le CTF essayé d'extraire le fichier "desktop.ini", qui ne donnait rien. Et c'est la qu'il faut comprendre le sens de la consigne; ce qui "est visible depuis le bureau" n'est pas un fichier, mais le fond d'écran! On peut donc (quand on est comme moi et qu'on ne sait pas ou est stoqué le fond d'écran) grep "wallpaper":

```shell
$ ./volatility_2.6_lin64_standalone -f dump.raw --profile=Win7SP1x86_23418 filescan | grep "Wallpaper"
Volatility Foundation Volatility Framework 2.6
0x000000007d10b440      7      0 RWD--- \Device\HarddiskVolume1\Users\Mes-vms.fr\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper.jpg
0x000000007fc9af80      8      0 R--rwd \Device\HarddiskVolume1\Windows\Web\Wallpaper\Characters\Desktop.ini
0x000000007fca7260      8      0 R--rwd \Device\HarddiskVolume1\Windows\Web\Wallpaper\Landscapes\Desktop.ini
0x000000007fca79d8      8      0 R--rwd \Device\HarddiskVolume1\Windows\Web\Wallpaper\Architecture\Desktop.ini
0x000000007fd21900      8      0 R--rwd \Device\HarddiskVolume1\Windows\Web\Wallpaper\Nature\Desktop.ini
0x000000007fe2f5f0      8      0 R--rwd \Device\HarddiskVolume1\Windows\Web\Wallpaper\Scenes\Desktop.ini
```

On trouve le fond d'écran à la première ligne, on peut essayer de récupérer le fichier avec l'adresse physique du fichier:

```shell
$ mkdir output
$ ./volatility_2.6_lin64_standalone -f dump.raw --profile=Win7SP1x86_23418 dumpfiles -Q 0x000000007d10b440 -D output/
Volatility Foundation Volatility Framework 2.6
DataSectionObject 0x7d10b440   None   \Device\HarddiskVolume1\Users\Mes-vms.fr\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper.jpg
```

On obtient cette image:

![image-20210403224259688](https://i.imgur.com/YeLIGO7.png)

**Flag: `PHACK{STEP_2-IC4nCwH4TUC}`**