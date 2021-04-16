# WE-1 (FlagClub) - variable

Il s'agit de rassembler 5 shares afin de pouvoir reconstituer le flag dans le cadre d'un [Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing). Chaque équipe est munie d'un share différent (donc il y en a une cinquantaine) et doit donc en obtenir 4 autres. De plus, le challenge vaudra de moins en moins de points au fur et à mesure que plus d'équipes le réussiront.

Toute la difficulté du challenge repose sur l'obtention des "shares" de la part des autres participants, qui n'ont pas d'intérêt à partager leur véritable clé car cela entraînerait potentiellement une perte d'avantage contre cette équipe que l'on aiderait à flag, ainsi que de l'avantage général sur les équipes n'ayant pas flag de par la valeur diminuant. Et ceci est sans même imaginer que l'équipe à qui l'on donne sa clé la partage encore plus.

Il est de plus très difficile d'attester de l'authenticité d'une clé (et probablement impossible avec assez de moyens, mais on supposera que personne n'en viendra à ces extrêmes). Le message Discord initial, posté par un bot dans le channel de chaque équipe, est supposé non altérable en tant que tel. Dès lors il s'agit de la preuve évidente que souhaiteront ceux récupérant des clés.

Néanmoins un message Discord est vite falsifié côté client, (notamment car il s'agit d'une application Electron) il suffit d'accéder à ses outils de développeur et d'éditer à foison. Nous avons néanmoins remarqué que changer de channel puis revenir au même rafraîchissait ces changements.
Nous avons donc conclu qu'un live Discord montrant le message original après un changement de channel était preuve de validité suffisante pour une clé.

Reste à forcer quelqu'un à donner sa vraie clé. Et pour cela aucune réelle solution. Une fois que le premier parti d'un supposé échange a rempli sa part et donné sa clé, strictement rien n'empêche l'autre de lâchement fuir sans remplir sa part du contrat, si ce n'est son honneur / amour propre s'il en a.

Une fois (si cela arrive) que l'on a récupéré 5 shares, diverses applications permettent de reconstituer le secret, par exemple [ssss](http://point-at-infinity.org/ssss/demo.html).

