## Piraterie (Ep 1) - 512 points

### Problème

```
Vous venez d'être embauché en tant qu'analyse sécurité dans votre nouvelle entreprise. Encore ému par cette nouvelle, on vous affecte à votre première mission.

Votre client du jour s'est fait piraté. Heureusement, il a eut la présence d'esprit de ne pas éteindre la machine compromise et vous fournit un dump mémoire.

Essayez de trouver ce qu'a pu faire le pirate.
```

+ dump.raw

### Résolution

On nous donne un fichier `dump.raw` de 2Go, qui semble être un dump mémoire. On va donc l'analyser avec volatility:

```bash
$ ./volatility_2.6_lin64_standalone -f dump.raw imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/clem/Desktop/phack/forensics/piraterie/volatility_2.6_lin64_standalone/dump.raw)
                      PAE type : PAE
                           DTB : 0x185000L
                          KDBG : 0x82b40c28L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0x82b41c00L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2021-02-20 23:46:58 UTC+0000
     Image local date and time : 2021-02-21 00:46:58 +0100
```

Selon l'analyse, c'est un profil Win7SP1x86_23418. On va donc pouvoir utiliser ce profil pour récupérer des infos sur le dump. Les premières choses à regarder peuvent varier, c'est un peu du pif mais on peut deviner qu'il faut regarder le contenu de la console. Pour ça il faut utiliser la commande `consoles` (en précisant bien le profil trouvé). J'ai coupé la sortie car elle était vraiment longue, mais elle contenait surtout ça:

```shell
...
C:\Users\Mes-vms.fr\Desktop>echo "Got U fucker !!!!" > .Pwned                   
                                                                                
C:\Users\Mes-vms.fr\Desktop>echo "PHACK{STEP_1-IC4nD0Wh4TuD0}" >> .Pwned        
                                                                                
C:\Users\Mes-vms.fr\Desktop>rm .Pwned
...
```

**Flag: `PHACK{STEP_1-IC4nD0Wh4TuD0}`**
