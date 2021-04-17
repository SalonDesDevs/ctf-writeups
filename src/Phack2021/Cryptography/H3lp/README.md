# H3lp - 256 points

## Problème

 Un message de votre ami intergalactique vient d'arriver ! 
 Saurez-vous le décoder à temps ?

```
3()()¯¯V)--, '-- v^|--[]_|\|/ <(Z/\>-'v^ []_|¯¯U L!LL|_]_]^-]=[[]ZLL| |--() 3<[^<Z >-[]] .. '-- LLVVUU_] _|'--_V_\|/ -^() ^-WUU/\ 3<(v^ _V_'--¯¯VZ<{A_^-LL|¯¯V. E>- '--Z>LL|[/][--'--LD<||--'--()Zv^ <[A<W _]LL|<|/\'--ZLD EW [--[] |--]=[\|/ '--ZLL<{E()](/) N]A<LD. E^< A_()|--<([--() <(Z/\ A<LL|>< <{^<W ]=[\|/_]A_'--ZLD ELL| ()Z |--]=['--v^. E\|/LL|[-- EVV |--[]Z'--LD]=[[--, |¯¯A_.E, <[[-- ^-'--NN<|^-_]<{ZUU[--. '-- ]=[\|/<{A<¯¯U |--]=[<||-- []Z\|/ []L|_ |--]=[\|/ _|'--[--|--_]VV LD^<LL|WZ EUUZ E'--LD]=[|-- ]=[<|>UU (/)UUWZ V\[]E\|/[--]=['--ZLD. ¯¯U()Z'|-- 3()^<A<>- U()3-^())-- .. 3VV ]=[<(>\|/ <( L|_A<'--UUZ¯¯U '--Z ZUUVV¯¯U, <{Z¯¯V 3W 3'--_|_| Z()[-- ^<LL|(/)|-- ]Z|--'--_| ]=[W'v^ [/]<|LLUU '--Z <|Z¯¯U)--'V\ ^<()[]E. [--<{_V_W L|<[^<\|/.
AA]NN
```

Le flag est le lieu de rendez-vous en majuscules au format `PHACK{LIEU}`.

## Résolution

Ce challenge nous a pris beaucoup trop de temps pour sa difficulté. Au début, nous avons essayé de faire correspondre chaque signe du message avec des lettres, comme par exemple `() = O`, `3 = B` etc... Mais cela ne donnait rien et était trop lent. Au final, il suffisait d'identifier la méthode utilisée pour crypter le message. Le site [dcode.fr](https://www.dcode.fr/cipher-identifier) nous indique avec une grande confiance que ça serait du LSPK90 Clockwise, qui est une encryption qui consiste à tourner de 90 degrés chaque lettre d'un message. Effectivement, cela semble fonctionner sur notre texte sur le premier mot par exemple:

+ 3 = W
+ () = O
+ () = O
+ ¯¯V = D
+ )-- = Y

On peut s'aider d'un outil pour trouver le message original complet, comme celui de [dcode.fr](https://www.dcode.fr/lspk90-cw-leet-speak-90-degrees-clockwise):

```
WOODY, I STOLE ANDY'S OLD CELLPHONE TO WARN YOU : I FEEL LIKE BO PEED WAS KIDNAPPED. MY INVESTIGATIONS ARE LEADING ME TO THE INFAMOUS ZURG.
MR POTATO AND REX ARE HELPING ME ON THIS. MEET ME TONIGHT, 7P.M, AT PIZZAPLANET. I HEARD THAT ONE OF THE LITTLE GREEN MEN MIGHT HAVE SEEN SOMETHING.
DON'T WORRY COWBOY : WE HAVE A FRIEND IN NEED, AND WE WILL NOT REST UNTIL HE'S SAFE IN ANDY'S ROOM.
TAKE CARE.
BUZZ
```

On y lit que Buzz donne rendez-vous à Woody, au "PIZZAPLANET".

**Flag: `PHACK{PIZZAPLANET}`**