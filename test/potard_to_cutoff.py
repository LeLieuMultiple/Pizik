from gpiozero import MCP3008
import time
import os
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from time import sleep
import argparse
import sys

pot = MCP3008(channel=0)
pot2 = MCP3008(channel=1)

prev_pot_value = 0
prev_pot_value2 = 1

# Mise en place du serveur OSC
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
  help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=4559,
  help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)


while True:
	
	pot_value = int(128*pot.value)
	if pot_value != prev_pot_value:	
		print(pot_value)
		client.send_message("/basse_cutoff", pot_value)
		prev_pot_value = pot_value
		
	pot_value2 = int(128*pot2.value)
	if pot_value2 != prev_pot_value2:	
		print(pot_value2)
		client.send_message("/basse_note", pot_value2)
		prev_pot_value2 = pot_value2
		
	time.sleep(0.05)
