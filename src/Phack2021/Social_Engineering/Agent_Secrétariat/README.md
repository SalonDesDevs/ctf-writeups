# Agent Secrétariat - 256 points

En cherchant un petit peu on trouve le profil Linkedin de [la cible](https://fr.linkedin.com/in/jessica-niche-a812b420a). On peut remarquer son adresse email, ainsi que diverses choses potentiellement intéressantes pour la duper (un potentiel amour pour les chiens, sa recherche d'un emploi combiné à ses compétences et sa localisation...).

Mais nous voulons lui soustraire des informations relatives à P'Hack, où elle est d'ailleurs "Directrice-fondatrice".

J'ai alors pris le parti d'imiter l'interface de login https://ctf.phack.fr/login. Pour ce faire j'ai utilisé le [Social Engineer Toolkit](https://github.com/trustedsec/social-engineer-toolkit) que j'ai découvert au passage, et plus précisément sa fonctionnalité "Clone website", que j'ai utilisée en suivant un gentil [article Medium](https://medium.com/@nancyjohn_95536/using-set-tool-kit-to-perform-website-cloning-in-kali-linux-67fa01c92af9) après l'avoir installé.

En guise d'IP où faire tourner notre clone, si l'on ne dispose pas d'un VPS ou d'un NAT on peut gratuitement utiliser [ngrok](https://ngrok.com) qui en faisant simplement `./ngrok 80` après avoir lié un compte nous offre une adresse.

Après avoir vérifié que le clone marche correctement (on arrive bien directement sur la bonne page (pour ce faire il faut rajouter le `/index2.html` ou sinon Jessica arrivera sur une redirection douteuse) et les noms d'utilisateur et mdp qu'on y rentre nous sont bien envoyés), il ne nous reste plus qu'à envoyer un mail à Jessica avec le lien de notre faux login en justifiant son utilisation et la connexion qui suit.
J'ai personnellement pris le parti du travail sur le site dont un stagiaire demande des retours, et ai envoyé le mail suivant, avec une nouvelle adresse pour l'occasion :

![screenshot gmail](https://codimd.s3.shivering-isles.com/demo/uploads/upload_98d440a016759134e82bd9b48574f210.png)

Une fois les admins éveillés et cléments, Jessica nous envoya bien son nom d'utilisateur, et son mot de passe qui était le flag.