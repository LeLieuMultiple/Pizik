from gpiozero import Button

import time

from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
import argparse

from time import sleep

# Mise en place du serveur OSC
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
  help="The ip of the OSC server")
parser.add_argument("--port", type=int, default = 4559,
  help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

# GPIO
liste_pins = [6, 13, 19, 26, 12, 16, 20, 21]
liste_boutons = []
liste_etat = []

for index, item in enumerate( liste_pins ):
	b = Button( liste_pins[index] )
	liste_boutons.append( b )
	liste_etat.append(False)
	
while True:
	for index, item in enumerate( liste_boutons ):
		if liste_boutons[index].is_pressed:
			if liste_etat[index] == False:
				liste_etat[index] = True
				client.send_message("/clavier", index)
				print(index)
		else:
			if liste_etat[index] == True:
				liste_etat[index] = False
	
	time.sleep(0.005)
