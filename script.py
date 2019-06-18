import sys, os
import smtplib

def menu():
	os.system('clear')
	print("Bienvenue à travers mon script d'automatisation des clients VPN \n ")
	print("\033[31m/_\ Attention ce dernier est à exécuter sur une machine GNU/Linux \n\033[0m") 
	print("Voici les differentes options:")
	print(" 1.Créer un fichier de configuration pour un client \n 2 Créer le fichier client sur la machine local \n 3.Quitter")
	print(" \n Votre choix:")
	choice = input(" >>")
	if choice=="1":
		client()
	elif choice=="2":
		installation()
	elif choice=="3":
		return
	else:
		menu()

	return


def client():
	print("Merci de completer les informations suivantes afin de démarrer le script ")
	print(" \n Entrer le nom du client:")
	nom = input(" >>")
	print(" \n Entrer l'IP du serveur:")
	ip = input(" >>")	
	print(" \n Quel est le port utiliser sur le serveur VPN:")
	port = input(" >>")
	print(" \n Le protocol utilisé est UDP ou TCP:")
	protocol = input(" >>")
	print("\nLes informations sont les suivantes:\nnom:",nom, "\nIP:",ip,"\nPort:",port,"\nProtocol:",protocol)
	print(" \n Etes vous sur?(y/n)")
	choice = input(" >>")

	if choice=="y" or "Y":
		print("nom:",nom,ip,port,protocol)

	elif choice=="n" or "N":
		print("Renseignez à nouveau les informations du client")
		client()
	else:
		client()

	print("Envoyer le fichier par mail à l'utilisateur?(y/n)")
	reponse = input(" >>")
	if reponse=="y" or "Y" :
		print("nom:",nom)
	elif reponse=="n" or "N" :
		print("Renseignez à nouveau les informations du client")
	else:
		client()


	return


def installation():
	os.system('ls')
	print ("ok sa marche")
	return


def mail_linux():
	fromaddr = 'lasassin974@gmail.com'
	toaddrs  = 'lasassin974@gmail.com'
	sujet = "Un mail de test"
	msg = "Un test de mail"

# Gmail Login
 
	username = 'username' # A modifier
	password = 'password' # A modifier
 
# Sending the mail  
 
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
	return  

menu()
