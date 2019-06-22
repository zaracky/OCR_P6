import sys, os
import smtplib
import subprocess #Pour le stockage dans des variables des commandes systemes

#Pour l'envoie des mail avec corps de texte+pj
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


#Fonction Menu
def menu():
	os.system('clear')
#On affiche ici les options possible à l'éxecution du programme
	print("--------------------------------------------------------------------")
	print("Bienvenue à travers mon script d'automatisation des clients OPENVPN \n ")
	print("\033[31m/_\ Attention ce dernier est à exécuter sur une machine GNU/Linux \n\033[0m") 
	print("Voici les differentes options:")
	print(" 1.Créer un fichier de configuration pour un client \n 2 Créer le fichier client sur la machine local \n 3.Quitter")
	print("-------------------------------------------------------------------")
	print(" \n Votre choix:")
	choice = input(" >>")

#Une fonction à exécuter en fonction de chaque choix
	if choice=="1":
		client()
	elif choice=="2":
		installation()
	elif choice=="3":
		return
	else:
		menu()

	return
#Fin fonction menu


#FOnction permettant la création de la clé client
def client():
#Des informations sont necessaires afin de personnaliser les clés
	print("Merci de completer les informations suivantes afin de démarrer le script ")
	print(" \n Entrer le nom du client:")
	nom = input(" >>")
	print(" \n Entrer l'IP du serveur:")
	ip = input(" >>")	
	print(" \n Quel est le port utiliser sur le serveur VPN:")
	port = input(" >>")
	print(" \n Le protocol utilisé est UDP ou TCP:")
	protocol = input(" >>")
#On affiche le résumé des données entrées afin que l'utilisateur valide en toute conscience
	print("--------------------------------------------------------------")
	print("\nLes informations sont les suivantes:\nnom:",nom, "\nIP:",ip,"\nPort:",port,"\nProtocol:",protocol)
	print(" \n Etes vous sur?(y/n)")
	choice = input(" >>")
#Si le choix est yes on commence la création de la clé ovpn
	if choice=="y":
		print("nom:",nom,ip,port,protocol)


#Si le choix est no  l'utilisateur est invité a entrer à nouveau les informations		
	elif choice=="n":
		os.system('clear')
		client()
#Sinon on fait à nouveau appel a la fonction client
	else:
		client()
#Maintenant que le fichier est créer on propose à l'utilisateur de l'envoyer par mail à l'utilisateur
	print("Envoyer le fichier par mail à l'utilisateur?(y/n)")
	reponse = input(" >>")
#Si oui on fait appel à la fonction mail 
	if reponse=="y" :
		envoimail()

#Sinon on indique uniquement le chemin d'accès vers le fichier ovpn
	elif reponse=="n":
		print("Le fichier est disponible à l'emplacement suivant:")
		return
	else:
		print("Le fichier est disponible à l'emplacement suivant:")
	return
#Fin de la fonction client


def installation():
	os.system('ls')
	print ("ok sa marche")
	return



#Fonction permettant l'envoi des mail
def envoimail():
#on stock dans une variable le mdp du compte mail
	mdp = subprocess.check_output(['cat', '/home/administrateur/mdp.txt'])
#On demande le mail de l'utilisateur
	print("Quel est le mail utilisateur?")
#On l'integre ensuite à une variable
	mail= input(" >>")
#Demande de confirmation
	print("Etes vous sur qu'il s'agit de cette adresse:",mail," ? (y/n)")
	choice = input(" >>")
	if choice=="y":
#Si oui, on l'informe de la préparation du mail
		print("Préparation du mail pour l'envoie..")
	else:
#Sinon on l'invite a entrer à nouveau les informations
		print("Renseignez à nouveau les informations du client")
		envoimail()
#Nous avons un mail pour client linux et un autre pour client windows. On demande donc sous quel système est le client
	print("S'agit-il d'un client 'linux' ou 'windows'?")
	systemexploit= input(" [linux/windows]>>")
	if systemexploit=="linux":
#Si il s'agit d'un client linux on lui envoie la procédure approprié
		msg = MIMEMultipart()
#On definit ici le corps du mail
		msg['From'] = 'loic.esparon.ocr@gmail.com'
		msg['To'] = mail
		msg['Subject'] = 'Procédure installation OPENVPN Client Linux' 
		message = u"""\
		Bonjour,
		Vous trouverez ci-joint la procédure d'installation OPENVPN pour un client sous un système d'exploitation GNU/Linux:
		
		Installation en ligne de commande:
		On commence par installer openvpn avec la commande: apt-get install openvpn
		Il faudra ensuite copier le fichier .ovpn présent en pj à l'emplacement suivant: /etc/openvpn
		Enfin afin de démarrer la connexion, on exectuera la commande: openvpn /etc/openvpn/(votreprenom)ovpn

		Installation par interface graphique:
		La procédure est disponible en image au lieu suivant: https://doc.ubuntu-fr.org/openvpn

		Cordialement,
		L'équipe informatique"""
		msg.attach(MIMEText(message))
# Ces lignes permettent de definir la piece jointe:
#Son nom dans le mail
		filename = "test.txt"
#Son emplacement
		attachment = open("/home/administrateur/mdp.txt", "rb")
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
		mailserver.login('loic.esparon.ocr@gmail.com', mdp.decode())
		mailserver.sendmail('loic.esparon.ocr@gmail.com', mail, msg.as_string())
		mailserver.quit()
#On informe l'utilisateur que l'envoie est fait et qu'on le renvoie au menu principal
		print("Envoie du mail terminé! Retour au menu principal")
		input (" ")
		menu()
	elif systemexploit=="windows":
#Si il s'agit d'un client Windows on lui envoie la procédure approprié
		msg = MIMEMultipart()
		msg['From'] = 'loic.esparon.ocr@gmail.com'
		msg['To'] = mail
		msg['Subject'] = 'Procédure installation OPENVPN Client Windows' 
		message = u"""\
		Bonjour,
		Vous trouverez ci-joint la procédure d'installation OPENVPN pour un client sous un système d'exploitation Windows:
		
		Vous trouverez l'éxecutable openvpn à l'url suivant: https://www.vpnvision.com/installation-vpn/installation-vpn-openvpn-windows-10/

		Une fois l'installation terminée on executera les actions suivantes:
		Cliquer droit sur l’icône OpenVPN GUI puis aller dans Ouvrir l’emplacement du fichier.

		Dans la barre d’adresse : Programmes > OpenVPN > bin cliquer sur OpenVPN

		Cliquer sur le dossier config (vous y trouverez un ficher nommé README).

	Faîtes glissez tous les fichiers de configuration en pj de ce mail dans ce dossier config
		La configuration est maintenant terminée. Maintenant afin de se connecter il suffit d'exécuter à nouveau OPENVPN en tant que administrateur et cliquer sur "Connect"

		Cordialement,
		L'équipe informatique"""
		msg.attach(MIMEText(message))
# Ces lignes permettent de definir la piece jointe:
#Son nom dans le mail
		filename = "test.txt"
#Son emplacement
		attachment = open("/home/administrateur/mdp.txt", "rb")
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
		mailserver.login('loic.esparon.ocr@gmail.com', mdp.decode())
		mailserver.sendmail('loic.esparon.ocr@gmail.com', mail, msg.as_string())
		mailserver.quit()
#On informe l'utilisateur que l'envoie est fait et qu'on le renvoie au menu principal
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
