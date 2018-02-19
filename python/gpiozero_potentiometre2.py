from gpiozero import MCP3008
import time

pot = MCP3008(channel=0)

pot_list = []

pot_average = 0

while True:
	for i in range( 0, 10 ):
		pot_list.append(pot.value)
		time.sleep(0.1)
	for i in range( 0, 10 ):
		pot_average += pot_list[i]
	pot_average = pot_average / 10
	print(pot_average)
