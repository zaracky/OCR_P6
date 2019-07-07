#On commence par importer les librairies necessaires au fonctionnement
import sys, os, os.path
import smtplib
import subprocess 
from os import chdir, mkdir

#Pour l'envoie des mail avec corps de texte+pj
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#On importe les variables prédefinis du fichier variable
from variable import expediteur,mdp,localisation,ip,port,protocol

#Fonction Menu
def menu():
#On definit ici les variable globales qui seront utilisé par la suite
	global localisation
	global nom

	os.system('clear')
#On affiche ici les options possible à l'éxecution du programme
	print("--------------------------------------------------------------------")
	print("Bienvenue à travers mon script d'automatisation des clients OPENVPN \n ")
	print("\033[31m/_\ Attention ce dernier est à exécuter sur le serveur OPENVPN en tant que ROOT\n\033[0m") 
	print("Voici les differentes options:")
	print(" 1.Créer un fichier de configuration pour un client \n 2 Configurer le VPN sur une machine cliente \n 3.Manuel d'instruction \n 4.Quitter")
	print("-------------------------------------------------------------------")
	print(" \n Votre choix:")
	choice = input(" >>")

#On definit une fonction à exécuter en fonction de chaque choix
	if choice=="1":
		client()
	elif choice=="2":
		installation()
	elif choice=="3":
		readme()
	elif choice=="4":
		return
	else:
		print("Merci de choisir parmi les choix proposés")
		menu()

	return
#Fin fonction menu


#Fonction permettant la création de la clé client
def client():
	os.system('clear')
#Des informations sont necessaires afin de personnaliser les clés
	print("Merci de completer les informations suivantes afin de démarrer le script ")
#Il nous faut dans un premier temps l'accès vers le repertoire contenant les scripts et le certificat serveur:
	print(" \nOu se trouve le repertoire easy-rsa contenant les script de création?")
	print("\033[31m/_\ Attention le repertoire doit avoir la syntaxte suivante: build-key présent dans le repertoire indiquer et ca.crt +ca.key présent dans un sous-repertoire 'keys'\n (cf README) \n\033[0m") 
	localisation= input("[exemple: /etc/openvpn/easy-rsa ] >>")
#On procéde la verification de la présence des fichiers necessaires pour la création de la clé client 
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
	print("Tout les fichiers sont présent. Merci d'entrer les informations utilisateurs :\n")
	
#Maintenant cette étape réaliser, nous pouvons personaliser l'accès via les informations ci dessous:
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
	print("\nLes informations sont les suivantes:\nnom:",nom, "\nIP:",ip,"\nPort:",port,"\nProtocol:",protocol)
	print(" \n Etes vous sur?(y/n)")
	choice = input(" >>")
#Si le choix est yes on commence la création de la clé vpn
	if (choice == "y") or (choice == "yes") or (choice == "o") or (choice == "oui"):
		print("Début de la procédure..")
		os.chdir(localisation)

#Création du fichier de configuration

		fichier = open(localisation+"/"+nom+".conf", "w")
		fichier.write("client\ndev tun\nproto "+protocol+"\nremote "+ip+" "+port+"\nresolv-retryinfinite \nnobind \npersist-key \npersist-turn \nca /etc/openvpn/ca.crt\ncert /etc/openvpn/"+nom+".crt \nkey /etc/openvpn/"+nom+".key\ncomp-lzo \nverb 3 \npull")
		fichier.close()
#On créer ensuite un repertoire ou l'on deplace tout les fichiers
		os.mkdir(nom)
		os.system('mv '+nom+'.conf '+nom)
		os.system('zip -r '+nom+'.zip '+nom)
#Si le choix est non  l'utilisateur est invité a entrer à nouveau les informations		
	else:
		client()

#Maintenant que le fichier est créer on propose de l'envoyer par mail à l'utilisateur
	print("Envoyer le fichier par mail à l'utilisateur?(y/n)")
	reponse = input(" >>")
#Si oui on fait appel à la fonction mail 
	if (reponse == "y") or (reponse == "yes") or (reponse == "o") or (reponse == "oui"):
		envoimail()

#Sinon on indique uniquement le chemin d'accès vers le fichier ovpn
	else:
		print("Les fichier sont disponible à l'emplacement suivant:",localisation,"/",nom)
	print("\nVoulez-vous configurer d'autre client?(y/n)")
	choix = input(" >>")
	if (choix == "y") or (choix == "yes") or (choix == "o") or (choix == "oui"):
		client()
	else:
		print("A bientôt")
		return
	return
#Fin de la fonction client


def installation():
	os.system('ls')
	print ("ok sa marche")
	return

def readme():
	os.system('ls')
	print ("ok sa marche")
	return


#Fonction permettant l'envoi des mail
def envoimail():
#on stock dans une variable le mdp et le compte mail utilisé
	expediteur = "loic.esparon.ocr@gmail.com"
	mdp = subprocess.check_output(['cat', '/home/administrateur/mdp.txt'])
#On demande le mail de l'utilisateur à qui est destiner les fichiers
	print("Quel est le mail utilisateur?")
#On l'integre ensuite à une variable
	mail= input(" >>")
#Demande de confirmation
	print("Etes vous sur qu'il s'agit de cette adresse:",mail," ? (y/n)")
	choice = input(" >>")
	if (choice == "y") or (choice == "yes") or (choice == "o") or (choice == "oui"):
#Si oui, on l'informe de la préparation du mail
		print("Préparation du mail pour l'envoie..")
	else:
#Sinon on l'invite a entrer à nouveau les informations
		print("Renseignez à nouveau les informations du client")
		envoimail()
#Nous avons un mail pour client linux et un autre pour client windows. On demande donc sous quel système est le client
	print("S'agit-il d'un client 'linux' ou 'windows'?")
	systemexploit= input("[linux/windows]>>")
	if (systemexploit=="linux") or (systemexploit=="Linux"):
#Si il s'agit d'un client linux on lui envoie la procédure approprié
		msg = MIMEMultipart()
#On definit ici le corps du mail. Ce dernier sera a adapté en fonction du type de destinataire (technique ou non)
		msg['From'] = expediteur
		msg['To'] = mail
		msg['Subject'] = 'Procédure installation OPENVPN Client Linux' 
		message = u"""\
		Bonjour,
		Vous trouverez ci-joint la procédure d'installation OPENVPN pour un client sous un système d'exploitation GNU/Linux:
		
		Installation en ligne de commande:
		On commence par installer openvpn avec la commande: apt-get install openvpn
		Il faudra ensuite copier le fichier .ovpn présent en pj à l'emplacement suivant: /etc/openvpn
		Enfin afin de démarrer la connexion, on exectuera la commande: openvpn /etc/openvpn/(votreprenom).conf

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
		mailserver.login(expediteur, mdp.decode())
		mailserver.sendmail(expediteur, mail, msg.as_string())
		mailserver.quit()
#On informe l'utilisateur que l'envoie est fait et qu'on le renvoie au menu principal
		print("Envoie du mail terminé! Retour au menu principal")
		input (" ")
		menu()
	elif (systemexploit=="windows") or (systemexploit=="Windows"):
#Si il s'agit d'un client Windows on lui envoie la procédure approprié
		msg = MIMEMultipart()
		msg['From'] = expediteur
		msg['To'] = mail
#On definit ici le corps du mail. Ce dernier sera a adapté en fonction du type de destinataire (technique ou non)
		msg['Subject'] = 'Procédure installation OPENVPN Client Windows' 
		message = u"""\
		Bonjour,
		Vous trouverez ci-joint la procédure d'installation OPENVPN pour un client sous un système d'exploitation Windows:
		
		Vous trouverez l'éxecutable openvpn à l'url suivant: https://www.vpnvision.com/installation-vpn/installation-vpn-openvpn-windows-10/

		Une fois l'installation terminée on executera les actions suivantes:
		Cliquer droit sur l’icône OpenVPN GUI puis aller dans Ouvrir l’emplacement du fichier.

		Dans la barre d’adresse : Programmes > OpenVPN > bin cliquer sur OpenVPN

		Cliquer sur le dossier config (vous y trouverez un ficher nommé README).

	Faîtes glissez tous les fichiers de configuration en pj de ce mail dans le dossier config
		La configuration est maintenant terminée. Maintenant afin de se connecter il suffit d'exécuter à nouveau OPENVPN en tant que administrateur et cliquer sur "Connect"

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
		mailserver.login(expediteur, mdp.decode())
		mailserver.sendmail(expediteur, mail, msg.as_string())
		mailserver.quit()
#On informe l'utilisateur que l'envoi est fait et qu'on le renvoie au menu principal
		print("Envoie du mail terminé! Retour au menu principal")
		input (" ")
		menu()
	else :
#Si aucune des réponses n'est entrer on invite à nouveau l'utilisateur a renseigner les informations
		print("Le champs renseigner n'est pas celui attendu. Merci de réesayer")
		envoimail()
	return
#Fin de la fonction mail
menu()
