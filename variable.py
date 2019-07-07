#On definit ici les variables utilisé pour la fonction mail.
#Dans un premier temps l'adresse mail expediteur
expediteur= "loic"
#Suivi du mot de passe
mdp ="test"

#Si l'environement est frequement utilisé on peut definir les variable avec ce fichier:

#Ici la localisation des fichiers necessaires à la création de la clé (ca.crt ca.key build-key)
#Attention le repertoire doit avoir la syntaxte suivante: build-key présent dans le repertoire indiquer et ca.crt +ca.key présent dans un sous-repertoire 'keys'
localisation="/home/administrateur/easy-rsa"

#Et enfin les informations du serveur
ip="192.168.1.1"
port="1194"
protocol="udp"

