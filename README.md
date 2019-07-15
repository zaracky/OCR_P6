 -------------------------------------------------------------------------
|									  |
|			MANUEL D'INSTRUCTION				  |
|									  |
 --------------------------------------------------------------------------

1. PRE-REQUIS

/!\ Ce Script est à exécuter en tant que ROOT sur un serveur OPENVPN sous GNU LINUX!

Pour le bien de son exécution, les fichiers nécessaires à la création des clés client (ca.key ,ca.crt et build.key) doivent être présents dans un dossier sous la forme suivante:
Le dossier (qui contient build.key) et un sous dossier qui se nom keys (contenant ca.key et ca.crt du serveur VPN)

Cette configuration est celle par défaut lors de l'installation de OPENVPN sur un serveur. Il ne devrait donc avoir aucune modification à réaliser.

Un fichier variable.py est mis à disposition. Ce dernier est à utiliser dans le cadre d'une utilisation au sein d'un même environnement. Il permet de configurer les variables les plus utilisées et les identifiants gmail
Il est important que ce dernier se trouve dans le même répertoire que le script !

Les informations présentes dans le fichier vars doivent être paramétrées au préalable. Afin d'optimiser la création, les informations mentionnées seront validées automatiquement. 
Il faut impérativement le valider avec la commande "source ./vars" avant de débuter le script!!

Une connexion internet est requise pour l'envoi par mail.


--------------------------------------------------------------------------------------------------------------------------------------------------------------

2. SON FONCTIONNEMENT

Le script a pour fonction de créer automatiquement les fichiers de configurations nécessaires à la connexion des utilisateurs. 
Pour ce faire, des informations seront demandées à l'utilisateur du script telles que : le nom du client, l'adresse IP du serveur, le port utilisé, et le protocole.

Une fois le fichier créer, il est possible de les envoyer par mail à un utilisateur avec en corps du mail une procédure détailler de l'utilisation des fichiers. Le mail est adapté en fonction de s’il s'agit d'un client Linux ou Windows

Ce manuel d'instruction est également disponible au sein du script avec le choix "3" dans le menu.

/!\ Attention à bien respecter les réponses attendues aux afin de ne pas avoir à répondre aux mêmes questions plusieurs fois d'affilées. 

----------------------------------------------------------------------------------------------------------------------------------------------------------------

3. OPTIMISATION

Une seconde fonction existe et permet d'importer les variables mentionnées précédemment depuis le fichier variable.py. Cela permet un gain de temps dans le cadre d'une exécution répétée au sein du même environnement (choix "2").

Ce fichier est disponible à l'url suivante : https://github.com/zaracky/OCR_P6

La configuration est faite de sorte que le script puisse communiquer optimalement avec ce dernier. Il est conseillé de ne pas changer le nom des variables et respecter la mise en page.

Pour plus de sécurité, l'accès à ce fichier devra être restreint, car il contient notamment les identifiants gmail nécessaires à l'expédition.

Rien n'empêche néanmoins à l'utilisateur du script d'opter pour des sécurités supplémentaires telles que l'import du mot de passe depuis un fichier extérieur...

----------------------------------------------------------------------------------------------------------------------------------------------------------------

4. MAIL

La fonction mail est configurée pour accueillir une adresse gmail. Rien n'empêche par la suite d'opter pour une autre adresse à condition de modifier le serveur et port smpt de l'hébergeur mail.
Des commentaires contenant un "§§§§§§" précèdent les lignes concernées.


L'adresse mail expéditrice est à entrer lors de l'application de la fonction ou importer via le fichier variable.py

Idem pour le mot de passe.

Un corps de mail avec une procédure générique a été mis en place. Ce dernier sera à adapter en fonction du contexte et des utilisateurs.

Les fichiers seront envoyés en pièce jointe sous la forme d'une archive .zip

