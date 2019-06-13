import sys, os
import smtplib

def menu():
	os.system('clear')
	print("Bienvenue à travers mon script d'automatisation de VPN \n Voici les differentes options:")
	print(" 1.Créer un fichier de configuration pour un client Linux \n 2.Créer un fichier de configuration pour un client Windows \n 3.Appliquer le script sur la machine local \n 4.Quitter")
	print(" \n Votre choix:")
	choice = input(" >>")
	if choice=="1":
		print("Hello",choice)
		envoimail()
	elif choice=="2":
		client()
	elif choice=="3":
		client()
	elif choice=="4":
		return
	else:
		menu()

	return

def installation():
	os.system('ls')
	print ("ok")
	return

def client():
	print(" \n Entrer le nom du client:")
	nom = input(" >>")
	print(" \n Entrer le prenom du client:")
	prenom = input(" >>")	
	print(" \n Etes vous sur?(y/n)")
	choice = input(" >>")

	if choice=="y":
		print("nom:",nom)

	elif choice=="n":
		print("Renseignez à nouveau les informations du client")
		client()
	else:
		print("nul")
	return

def envoimail():
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
