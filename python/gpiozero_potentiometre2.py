from gpiozero import MCP3008
import time

pot = MCP3008(channel=0)

pot2 = MCP3008(channel=1)

while True:
	print(int(128*pot.value))
	print(int(128*pot2.value))
	time.sleep(1)
