#On commence par importer les librairies necessaires au commandes systeme
import sys, os, os.path
import smtplib
import subprocess 
from os import chdir, mkdir
from getpass import getpass

#Ces librairies permettent l'envoie par mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



#Fonction Menu
def menu():
	os.system('clear')
#On affiche ici les options possible à l'éxécution du programme
	print("--------------------------------------------------------------------")
	print("Bienvenue à travers mon script d'automatisation des clients OPENVPN \n ")
	print("\033[31m/_\ Attention ce dernier est à exécuter sur le serveur OPENVPN en tant que ROOT\n\033[0m") 
	print("Voici les différentes options:")
	print(" 1.Créer un fichier de configuration pour un client \n 2 Créer un fichier de configuration à l'aide du fichier variable.py \n 3.Manuel d'instruction \n 4.Quitter")
	print("-------------------------------------------------------------------")
	print(" \n Votre choix:")
	choice = input(" >>")
#On definit une fonction à exécuter en fonction de chaque choix
	if choice=="1":
		client()
	elif choice=="2":
		client_auto()
	elif choice=="3":
		readme()
	elif choice=="4":
		exit();
	else:
		print("Merci de choisir parmi les choix proposés")
		menu()

	return
#Fin fonction menu



#Fonction permettant la création de la clé client
def client():
	os.system('clear')
#On définit ici les variables globales qui seront utilisées par la suite
	global localisation
	global nom,expediteur,mdp
#Des informations sont nécessaires afin de personnaliser les clés
	print("Merci de compléter les informations suivantes afin de démarrer le script ")
#Il nous faut dans un premier temps l'accès vers le répertoire contenant les scripts et le certificat serveur:
	print(" \nOu se trouve le repertoire easy-rsa contenant les scripts de création?")
	print("\033[31m/_\ Attention le répertoire doit avoir la syntaxe suivante: build-key présent dans le répertoire indiqué et ca.crt +ca.key présent dans un sous-répertoire 'keys'\n (cf README) \n\033[0m") 
	localisation= input("[exemple: /etc/openvpn/easy-rsa ] >>")
#On procède à la verification de la présence des fichiers necessaires pour la création de la clé client 
	print("Verification de la présence des fichiers en cours.. \n")
	if os.path.isfile(localisation+'/keys/ca.crt'):
		print("Le fichier ca.crt est présent")
	else:
		print("\033[31m \n /_\ Erreur le fichier ca.crt n'est pas présent à l'emplacement suivant:",localisation,"/keys/\n\033[0m")
		print("Merci d'indiquer à nouveau le chemin d'accès")
		input (" ")
		client()
	if os.path.isfile(localisation+'/keys/ca.key'):
		print("Le fichier ca.key est présent")
	else:
		print("\033[31m \n /_\ Erreur le fichier ca.key n'est pas présent à l'emplacement suivant:",localisation,"/keys/\n\033[0m")
		print("Merci d'indiquer à nouveau le chemin d'accès")
		input (" ")
		client()
	if os.path.isfile(localisation+'/build-key'):
		print("Le fichier build-key est présent")
	else:
		print("\033[31m \n /_\ Erreur le fichier build-key n'est pas présent à l'emplacement suivant:",localisation,"\n\033[0m")
		print("Merci d'indiquer à nouveau le chemin d'accès")
		input (" ")
		client()
	print("Tous les fichiers sont présents. Merci d'entrer les informations utilisateurs :\n")
	
#Maintenant cette étape réaliser, nous pouvons personnaliser l'accès via les informations ci dessous:
	print(" \n Entrer le nom du client:")
	nom = input(" Nom:")
	print(" \n Entrer l'IP du serveur:")
	ip = input(" IP du serveur:")	
	print(" \n Quel est le port utiliser sur le serveur VPN:")
	port = input(" Port utilisé:")
	print(" \n Le protocol utilisé est UDP ou TCP:")
	protocol = input(" Protocol utilisé:")


#On affiche le résumé des données entrées afin que l'utilisateur valide en toute conscience
	print("--------------------------------------------------------------")
	print("\nLes informations sont les suivantes:\nNom:",nom, "\nIP:",ip,"\nPort:",port,"\nProtocol:",protocol)
	print(" \n Etes vous sur?(y/n)")
	choice = input(" >>")
#Si le choix est yes on commence la création de la clé vpn
	if (choice == "y") or (choice == "yes") or (choice == "o") or (choice == "oui"):
		print("Début de la procédure...")
		os.chdir(localisation)

#Création de la clé de chiffrement client
		fichier = open("buildkey.txt", "w")
		fichier.write("\n\n\n\n\n\n\n\n\n\ny\ny")
		fichier.close()
		os.system('bash build-key '+nom+ '< buildkey.txt')
		os.system('rm -fr buildkey.txt')
#Création du fichier de configuration client
		fichier = open(localisation+"/"+nom+".conf", "w")
		fichier.write("client\ndev tun\nproto "+protocol+"\nremote "+ip+" "+port+"\nresolv-retryinfinite \nnobind \npersist-key \npersist-turn \nca /etc/openvpn/ca.crt\ncert /etc/openvpn/"+nom+".crt \nkey /etc/openvpn/"+nom+".key\ncomp-lzo \nverb 3 \npull")
		fichier.close()
#On créer ensuite un repertoire ou l'on deplace tous les fichiers créer précédemment
		os.mkdir(nom)
		os.system('mv '+nom+'.conf '+nom)
		os.system('cp keys/ca.crt '+nom)
		os.system('mv keys/'+nom+'.crt '+nom)
		os.system('mv keys/'+nom+'.key '+nom)
		os.system('zip -r '+nom+'.zip '+nom)
#Si le choix est non  l'utilisateur est invité a entrer à nouveau les informations		
	else:
		client()

#Maintenant que le fichier est crée, on propose de l'envoyer par mail à l'utilisateur
	print("\n\n\n Fichiers de configuration créer! \n\n")
	print("Voulez-vous les envoyer par mail à l'utilisateur?(y/n)")
	reponse = input(" >>")
#Si oui on fait appel à la fonction mail 
	if (reponse == "y") or (reponse == "yes") or (reponse == "o") or (reponse == "oui"):
		print(" \nEntrer les informations de l'adresse mail expediteur:")
		expediteur = input("Mail expediteur:")
		mdp = getpass("Mot de passe de la boite mail: ")
		envoimail()

#Sinon on indique uniquement le chemin d'accès vers le fichier ovpn
	else:
		print("Les fichier sont disponible à l'emplacement suivant:",localisation,"/",nom)
#On propose à l'utilisateur de configurer d'autres clients
	print("\nVoulez-vous configurer d'autres clients?(y/n)")
	choix = input(" >>")
	if (choix == "y") or (choix == "yes") or (choix == "o") or (choix == "oui"):
#SI oui on relance la fonction client
		client()
	else:
#Sinon, on quitte le programme
		print("A bientôt")
	return
#Fin de la fonction client






#Cette fonction est une optimisation de la premiere dans le cas d'une execution repeté dans le même environnement
def client_auto():
	os.system('clear')
#On définit ici les variables globales qui seront utilisées par la suite
	global localisation
	global nom
#On verifie la précense du fichier variable.py
	print("Verification de la présence du fichier variable.py en cours.. \n")
	if os.path.isfile('variable.py'):
		print("Le fichier variable.py est présent :) Début de la procédure...")
#Si le fichier est présent on importe les variable
		from variable import expediteur,mdp,localisation,ip,port,protocol
	else:
#Sinon on indique un message d'erreur avec la possibilité de basculer sur la version non automatiser
		print("\033[31m \n /_\ Erreur le fichier variable n'est pas présent!\n\033[0m")
		print("Voulez-vous continuer?")
		choix = input(
" >>")
		if (choix == "y") or (choix == "yes") or (choix == "o") or (choix == "oui"):
			client()
		else:
			print("Retour au menu principal..")
			input (" ")
			menu()
#On verifie ici la présence des fichiers necessaires à la création des fichiers clients
	print("Verification de la présence des certificats en cours.. \n")
	if os.path.isfile(localisation+'/keys/ca.crt'):
		print("Le fichier ca.crt est présent")
	else:
		print("\033[31m \n /_\ Erreur le fichier ca.crt n'est pas présent à l'emplacement suivant:",localisation,"/keys/\n\033[0m")
		print("Merci d'indiquer à nouveau le chemin d'accès")
		input (" ")
		client()
	if os.path.isfile(localisation+'/keys/ca.key'):
		print("Le fichier ca.key est présent")
	else:
		print("\033[31m \n /_\ Erreur le fichier ca.key n'est pas présent à l'emplacement suivant:",localisation,"/keys/\n\033[0m")
		print("Merci d'indiquer à nouveau le chemin d'accès")
		input (" ")
		client()
	if os.path.isfile(localisation+'/build-key'):
		print("Le fichier build-key est présent")
	else:
		print("\033[31m \n /_\ Erreur le fichier build-key n'est pas présent à l'emplacement suivant:",localisation,"\n\033[0m")
		print("Merci d'indiquer à nouveau le chemin d'accès")
		input (" ")
		client()
	print("Tous les fichiers sont présents. \n Merci de completer le nom du client afin de démarrer la fonction:\n")
#Dans cette fonction nous ne demanderons pas d'entrer toutes les informations utilisateurs car ces derniers seront importés du fichier variable.pŷ
	nom = input(" Nom:")
	print("\nCréation des fichiers en cours...\n")
#Création de la clé de chiffrement client
	os.chdir(localisation)
	fichier = open("buildkey.txt", "w")
	fichier.write("\n\n\n\n\n\n\n\n\n\ny\ny")
	fichier.close()
	os.system('bash build-key '+nom+ '< buildkey.txt')
	os.system('rm -fr buildkey.txt')
#Création du fichier de configuration client
	fichier = open(localisation+"/"+nom+".conf", "w")
	fichier.write("client\ndev tun\nproto "+protocol+"\nremote "+ip+" "+port+"\nresolv-retryinfinite \nnobind \npersist-key \npersist-turn \nca /etc/openvpn/ca.crt\ncert /etc/openvpn/"+nom+".crt \nkey /etc/openvpn/"+nom+".key\ncomp-lzo \nverb 3 \npull")
	fichier.close()
#On créer ensuite un repertoire ou l'on deplace tous les fichiers créer précédemment
	os.mkdir(nom)
	os.system('mv '+nom+'.conf '+nom)
	os.system('cp keys/ca.crt '+nom)
	os.system('mv keys/'+nom+'.crt '+nom)
	os.system('mv keys/'+nom+'.key '+nom)
	os.system('zip -r '+nom+'.zip '+nom)
#Maintenant que le fichier est crée, on propose de l'envoyer par mail à l'utilisateur
	print("\n\n\n Fichiers de configuration créer! \n\n")
	print("Voulez-vous les envoyer par mail à l'utilisateur?(y/n)")
	reponse = input(" >>")
#Si oui on fait appel à la fonction mail 
	if (reponse == "y") or (reponse == "yes") or (reponse == "o") or (reponse == "oui"):
		envoimail()

#Sinon on indique uniquement le chemin d'accès vers le fichier ovpn
	else:
		print("Les fichier sont disponible à l'emplacement suivant:",localisation,"/",nom)
#On propose également la possibilité de configurer d'autre client
	print("\nVoulez-vous configurer d'autre client?(y/n)")
	choix = input(" >>")
	if (choix == "y") or (choix == "yes") or (choix == "o") or (choix == "oui"):
		client()
	else:
#Sinon on quitte le programme
		print("A bientôt")
		return;
	return
#Fin de la fonction client_auto






#Cette fonction vas contenir le manuel d'instruction
def readme():
	print("""  -------------------------------------------------------------------------
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

Une connexion internet est requise pour l'envoi par mail.
""")
	input("Appuyez Entrer pour continuer ")
	print(""" ----------------------------------------------------------------------------

2. SON FONCTIONNEMENT

Le script a pour fonction de créer automatiquement les fichiers de configurations nécessaires à la connexion des utilisateurs. 
Pour ce faire, des informations seront demandées à l'utilisateur du script telles que : le nom du client, l'adresse IP du serveur, le port utilisé, et le protocole.

Une fois le fichier créer, il est possible de les envoyer par mail à un utilisateur avec en corps du mail une procédure détailler de l'utilisation des fichiers. Le mail est adapté en fonction de s’il s'agit d'un client Linux ou Windows

Ce manuel d'instruction est également disponible au sein du script avec le choix "3" dans le menu.

/!\ Attention à bien respecter les réponses attendues aux afin de ne pas avoir à répondre aux mêmes questions plusieurs fois d'affilées. 
""")
	input(" ")
	print(""" ----------------------------------------------------------------------------

3. OPTIMISATION

Une seconde fonction existe et permet d'importer les variables mentionnées précédemment depuis le fichier variable.py. Cela permet un gain de temps dans le cadre d'une exécution répétée au sein du même environnement (choix "2").

Ce fichier est disponible à l'url suivante : https://github.com/zaracky/OCR_P6

La configuration est faite de sorte que le script puisse communiquer optimalement avec ce dernier. Il est conseillé de ne pas changer le nom des variables et respecter la mise en page.

Pour plus de sécurité, l'accès à ce fichier devra être restreint, car il contient notamment les identifiants gmail nécessaires à l'expédition.

Rien n'empêche néanmoins à l'utilisateur du script d'opter pour des sécurités supplémentaires telles que l'import du mot de passe depuis un fichier extérieur...
""")
	input(" ")
	print(""" ----------------------------------------------------------------------------

4. MAIL

L'adresse mail expéditrice est à entrer lors de l'application de la fonction ou importer via le fichier variable.py

Idem pour le mot de passe.

Un corps de mail avec une procédure générique a été mis en place. Ce dernier sera à adapter en fonction du contexte et des utilisateurs.

Les fichiers seront envoyés en pièce jointe sous la forme d'une archive .zip
""")
	input("Retour au menu principal ")
	menu()
	return
#Fin de la fonction README




#Fonction permettant l'envoi des mail
def envoimail():
#On demande le mail de l'utilisateur à qui sont destinés les fichiers
	print("\nQuel est le mail de l'utilisateur?")
#On l'integre ensuite à une variable
	mail= input(" >>")
#Demande de confirmation
	print("\nEtes vous sur qu'il s'agit de cette adresse:",mail," ? (y/n)")
	choice = input(" >>")
	if (choice == "y") or (choice == "yes") or (choice == "o") or (choice == "oui"):
#Si oui, on l'informe de la préparation du mail
		print("\nPréparation du mail pour l'envoie..")
	else:
#Sinon on l'invite a entrer à nouveau les informations
		print("Renseignez à nouveau les informations du client")
		envoimail()
#Nous avons un mail pour client linux et un autre pour client windows. On demande donc sous quel système est le client
	print("S'agit-il d'un client 'linux' ou 'windows'?")
	systemexploit= input("[linux/windows]>>")
	if (systemexploit=="linux") or (systemexploit=="Linux"):
#Si il s'agit d'un client linux on lui envoie la procédure appropriée
		msg = MIMEMultipart()
#On definit ici le corps du mail. Ce dernier sera a adapter en fonction du type de destinataire (technique ou non)
		msg['From'] = expediteur
		msg['To'] = mail
		msg['Subject'] = 'Procédure installation OPENVPN Client Linux' 
		message = u"""\
		Bonjour,
		Vous trouverez ci-joint la procédure d'installation OPENVPN pour un client sous un système d'exploitation GNU/Linux:
		
		Installation en ligne de commande:
		On commence par installer openvpn avec la commande: apt-get install openvpn
		Il faudra ensuite copier le fichier .ovpn présent en pj à l'emplacement suivant: /etc/openvpn
		Enfin afin de démarrer la connexion, on éxecutera la commande: openvpn /etc/openvpn/(votreprenom).conf

		Installation par interface graphique:
		La procédure est disponible en image au lieu suivant: https://doc.ubuntu-fr.org/openvpn

		Cordialement,
		L'équipe informatique"""
		msg.attach(MIMEText(message))
# Ces lignes permettent de definir la piece jointe:
#Son nom dans le mail
		filename = "Fichier_configuration.zip"
#Son emplacement
		attachment = open(localisation+"/"+nom+".zip", "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(attachment.read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment", filename=filename)
		msg.attach(part)
		mailserver = smtplib.SMTP('smtp.gmail.com', 587)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
#On indique les identifiants de connexion
		mailserver.login(expediteur, mdp)
		mailserver.sendmail(expediteur, mail, msg.as_string())
		mailserver.quit()
#On informe l'utilisateur que l'envoie est fait et qu'on le renvoie au menu principal
		print("\nEnvoie du mail terminé! Retour au menu principal")
		input (" ")
		menu()
	elif (systemexploit=="windows") or (systemexploit=="Windows"):
#Si il s'agit d'un client Windows on lui envoie la procédure appropriée
		msg = MIMEMultipart()
		msg['From'] = expediteur
		msg['To'] = mail
#On definit ici le corps du mail. Ce dernier sera à adapter en fonction du type de destinataire (technique ou non)
		msg['Subject'] = 'Procédure installation OPENVPN Client Windows' 
		message = u"""\
		Bonjour,
		Vous trouverez ci-joint la procédure d'installation OPENVPN pour un client sous un système d'exploitation Windows:
		
		Vous trouverez l'éxécutable openvpn à l'url suivant: https://www.vpnvision.com/installation-vpn/installation-vpn-openvpn-windows-10/

		Une fois l'installation terminée on exécutera les actions suivantes:
		Cliquer droit sur l’icône OpenVPN GUI puis aller dans Ouvrir l’emplacement du fichier.

		Dans la barre d’adresse : Programmes > OpenVPN > bin cliquer sur OpenVPN

		Cliquer sur le dossier config (vous y trouverez un ficher nommé README).

	Faîtes glissez tous les fichiers de configuration en pj de ce mail dans le dossier config
		La configuration est maintenant terminée. Maintenant afin de se connecter il suffit d'exécuter à nouveau OPENVPN en tant qu'administrateur et cliquer sur "Connect"

		Cordialement,
		L'équipe informatique"""
		msg.attach(MIMEText(message))
# Ces lignes permettent de definir la piece jointe:
#Son nom dans le mail
		filename = "Fichier_configuration.zip"
#Son emplacement
		attachment = open(localisation+"/"+nom+".zip", "rb")
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(attachment.read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment", filename=filename)
		msg.attach(part)
		mailserver = smtplib.SMTP('smtp.gmail.com', 587)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
#On indique les identifiants de connexion
		mailserver.login(expediteur, mdp)
		mailserver.sendmail(expediteur, mail, msg.as_string())
		mailserver.quit()
#On informe l'utilisateur que l'envoi est fait et qu'on le renvoie au menu principal
		print("\nEnvoie du mail terminé! Retour au menu principal")
		input (" ")
		menu()
	else :
#Si aucune des réponses n'est entrée, on invite à nouveau l'utilisateur à renseigner les informations
		print("Le champs renseigner n'est pas celui attendu. Merci de réessayer")
		envoimail()
	return
#Fin de la fonction mail
menu()
