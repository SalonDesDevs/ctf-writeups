# Journées portes ouvertes - 128 points

On se voit fourni un nom de domaine ainsi que la mention de "port(e)s ouvert(e)s.". On va donc regarder les ports ouverts avec `nmap` et voir si ceux-ci acceptent de nous donner un flag.

`sudo nmap -vv -p- journees-portes-ouvertes.phack.fr`

Et effectivement, sur certains des ports accessibles, on obtient avec `nc journees-portes-ouvertes.phack.fr <port>` un fragment du flag, ou sinon un message disant qu'il n'y a rien.

La liste des ports ouverts sur la machine a grandement fluctué pendant que nous essayions de flag ce challenge, et à plusieurs reprises finissait par uniquement 1 ou deux ports disponibles et invariables. Nous ne savons pas dans quelle mesure cela faisait partie du challenge.
Dans l'optique de ports ouverts que brièvement nous avons aussi fait usage de [rustscan](https://github.com/RustScan/RustScan) pour détecter ceux-ci le plus vite possible avec le compromis des faux positifs et ratés.
