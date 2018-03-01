# Ce programme vous est gracieusement offert par le Dindoleon
# Merci de ne pas abîmer la musique

# Import des librairies

import os
from gpiozero import Button
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from time import sleep
import argparse
import sys
import pygame
from pygame import *
pygame.init()

# Declaration des variables et autres fantaisies
LISTE_SYNTHES = ['Beep', 'Blade', 'Bnoise', 'Chipbass', 'Chiplead', 'Chipnoise', 'Cnoise', 'Dark Ambience', 'Dpulse', 'Dsaw', 'Dtri', 'Dull Bell',
'Fm', 'Gnoise', 'Growl', 'Hollow', 'Hoover', 'Mod Beep', 'Mod Dsaw', 'Mod Fm', 'Mod Pulse', 'Mod Saw', 'Mod Sine', 'Mod Tri', 'Noise', 'Piano', 'Pluck',
'Pnoise', 'Pretty Bell', 'Prophet', 'Pulse', 'Saw', 'Sine', 'Sound In', 'Sound In Stereo', 'Square', 'Subpulse', 'Supersaw', 'Tb303', 'Tech Saws', 'Tri', 'Zawa']
liste_boutons = []

LARGEUR_FENETRE = 900
HAUTEUR_FENETRE = 600

attack = 0.1
sustain = 1
decay = 0
release = 0.5

# Initialisation de Pygame
DISPLAYSURF = pygame.display.set_mode( ( LARGEUR_FENETRE, HAUTEUR_FENETRE ) )
pygame.display.set_caption('Interface Clavier')

font = pygame.font.Font(None, 25)

# Fonctions
def initialiser_boutons():
	x = 0
	y = 0
	for i in range ( len(LISTE_SYNTHES) ):
		nouveau_bouton = Bouton(LISTE_SYNTHES[i], [ 5 + x * 120, 5 + y * 30 ])
		liste_boutons.append(nouveau_bouton)
		x += 1
		if x > 5:
			x = 0
			y += 1

def dessiner_boutons():

	for i in range ( len(liste_boutons) ):
		if liste_boutons[i].statut:
			pygame.draw.rect(DISPLAYSURF, [0, 255, 0], (liste_boutons[i].position, ( 100, 25 )), 0 )
		else:
			if liste_boutons[i].souris:
				pygame.draw.rect(DISPLAYSURF, [255, 255, 0], (liste_boutons[i].position, ( 115, 25 )), 0 )
			else:
				pygame.draw.rect(DISPLAYSURF, [255, 0, 0], (liste_boutons[i].position, ( 115, 25 )), 0 )
			
		text = font.render( liste_boutons[i].texte, True, (0,0,0) )
		DISPLAYSURF.blit(text, liste_boutons[i].position )
		
def update():
	dessiner_boutons()
	pygame.display.update()

# Classes
class Bouton:
	def __init__(self, texte, position):
		self.texte = texte
		self.position = position
		self.souris = False
		self.statut = False

initialiser_boutons()	
dessiner_boutons()

pygame.display.update()

# Mise en place du serveur OSC
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
  help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=4559,
  help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

# GPIO
button_list = [6, 13, 19, 26, 12, 16, 20, 21]

#These are representative buttons and leds used in initial tests
#You can specify your own pin numbers if differnt
button0 = Button(6)
button1 = Button(13)
button2 = Button(19)
button3 = Button(26)
button4 = Button(12)
button5 = Button(16)
button6 = Button(20)
button7 = Button(21)

#This function is called when the button connected to the GPIO is pushed
def msg0():
    #sender client set up in __main__ below
    client.send_message('/note',0)
    sleep(0.1)
def msg1():
    #sender client set up in __main__ below
    client.send_message('/note',1)
    sleep(0.01)
def msg2():
    #sender client set up in __main__ below
    client.send_message('/note',2)
    sleep(0.01)
def msg3():
    #sender client set up in __main__ below
    client.send_message('/note',3)
    sleep(0.01)
def msg4():
    #sender client set up in __main__ below
    client.send_message('/note',4)
    sleep(0.01)
def msg5():
    #sender client set up in __main__ below
    client.send_message('/note',5)
    sleep(0.01)
def msg6():
    #sender client set up in __main__ below
    client.send_message('/note',6)
    sleep(0.01)
def msg7():
    #sender client set up in __main__ below
    client.send_message('/note',7)
    sleep(0.01)

#this is where the msg routing is activated
button0.when_pressed = msg0
button1.when_pressed = msg1
button2.when_pressed = msg2
button3.when_pressed = msg3
button4.when_pressed = msg4
button5.when_pressed = msg5
button6.when_pressed = msg6
button7.when_pressed = msg7

client.send_message("/setup", [attack, sustain, decay, release])

# Boucle principale
while True:
	
	# Gestion des Inputs
	mouse = pygame.mouse.get_pos()
	KEY = pygame.key.get_pressed()

	for event in pygame.event.get():

		if event.type == QUIT or KEY[pygame.K_ESCAPE]:
			pygame.quit()
			sys.exit()
		
		if event.type == MOUSEMOTION:
			for i in range ( len(liste_boutons) ):
				liste_boutons[i].souris = False
				if mouse[0] > liste_boutons[i].position[0] and mouse[0] < liste_boutons[i].position[0] + 100:
					if mouse[1] > liste_boutons[i].position[1] and mouse[1] < liste_boutons[i].position[1] + 25:
						liste_boutons[i].souris = True
			update()
						
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				for i in range ( len(liste_boutons) ):
					if liste_boutons[i].souris == True:
						if liste_boutons[i].statut:
							liste_boutons[i].statut = False
						else:
							for j in range ( len(liste_boutons) ):
								liste_boutons[j].statut = False
							liste_boutons[i].statut = True
							client.send_message("/change_synth", i)
				update()
	
	# Fin de boucle
	pygame.time.wait(30)
