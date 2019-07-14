#Ce fichier est utiliser pour definir automatiquement les variables au sein du script principal.
#/!\ Ce fichier doit être sécuriser! Il est déconseiller de changer le nom des variables


#On definit ici l'adresse qui sera utilisé pour expedier les mail
expediteur= "mail expediteur"
#Suivi du mot de passe
mdp ="test"


#On definit ensuite les variables necessaires à la création des fichiers client:

#Ici la localisation des fichiers necessaires à la création de la clé (ca.crt ca.key build-key)
#Attention le repertoire doit avoir la syntaxte suivante: build-key présent dans le repertoire indiquer et ca.crt +ca.key présent dans un sous-repertoire 'keys'
localisation="/home/administrateur/easy-rsa"

#Et enfin les informations de connexion du serveur
ip="192.168.1.1"
port="1194"
protocol="udp"


