import sys, os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#Fonction Menu
def menu():
	os.system('clear')
#On affiche ici les options possible à l'éxecution du programme
	print("Bienvenue à travers mon script d'automatisation des clients OPENVPN \n ")
	print("\033[31m/_\ Attention ce dernier est à exécuter sur une machine GNU/Linux \n\033[0m") 
	print("Voici les differentes options:")
	print(" 1.Créer un fichier de configuration pour un client \n 2 Créer le fichier client sur la machine local \n 3.Quitter")
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
	print("\nLes informations sont les suivantes:\nnom:",nom, "\nIP:",ip,"\nPort:",port,"\nProtocol:",protocol)
	print(" \n Etes vous sur?(y/n)")
	choice = input(" >>")
#Si le choix est yes on commence la création de la clé ovpn
	if choice=="y":
		print("nom:",nom,ip,port,protocol)


#Si le choix est no  l'utilisateur est invité a entrer à nouveau les informations		
	elif choice=="n":
		print("Renseignez à nouveau les informations du client")
		client()
#Sinon on fait à nouveau appel a la fonction client
	else:
		client()
#Maintenant que le fichier est créer on propose à l'utilisateur de l'envoyer par mail à l'utilisateur
	print("Envoyer le fichier par mail à l'utilisateur?(y/n)")
	reponse = input(" >>")
#Si oui on fait appel à la fonction mail correspondant à l'OS Client
	if reponse=="y" :
		envoimail()

#Sinon on indique uniquement le chemin d'accès vers le fichier ovpn
	elif reponse=="n":
		print("Le fichier est disponible à l'emplacement suivant:")
	else:
		print("Le fichier est disponible à l'emplacement suivant:")
	return
#Fin de la fonction client


def installation():
	os.system('ls')
	print ("ok sa marche")
	return


def envoimail():
	print("Quel est le mail utilisateur?")
	mail= input(" >>")
	print("Etes vous sur qu'il s'agit de cette adresse:",mail," ? (y/n)")
	choice = input(" >>")
	if choice=="y":
		msg = MIMEMultipart()
		msg['From'] = 'loic.esparon.ocr@gmail.com'
		msg['To'] = mail
		msg['Subject'] = 'Procédure installation OPENVPN Client Linux' 
		message = u"""\
		Bonjour voici la prrocédure
		SUffit d'installer le bidule dans le machin
		Et ensuite magie sisi"""
		msg.attach(MIMEText(message))
		mailserver = smtplib.SMTP('smtp.gmail.com', 587)
		mailserver.ehlo()
		mailserver.starttls()
		mailserver.ehlo()
		mailserver.login('loic.esparon.ocr@gmail.com', 'loicus7!')
		mailserver.sendmail('loic.esparon.ocr@gmail.com', mail, msg.as_string())
		mailserver.quit()
	elif choice=="n":
		print("Renseignez à nouveau les informations du client")
		envoimail()

	else :
		envoimail()
	return

menu()
