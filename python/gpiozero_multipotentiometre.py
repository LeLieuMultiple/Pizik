from gpiozero import MCP3008
import time

pot0 = MCP3008(channel=0)
#pot1 = MCP3008(channel=1)

pot0_list = []
#pot1_list = []

pot0_average = 0
#pot1_average = 0

while True:
	for i in range( 0, 10 ):
		pot0_list.append(pot0.value)
		#pot1_list.append(pot1.value)
		time.sleep(0.1)
	for i in range( 0, 10 ):
		pot0_average += pot0_list[i]
		#pot1_average += pot1_list[i]
	pot0_average = pot0_average / 10
	#pot1_average = pot1_average / 10
	print(pot0_average)
	#print(pot1_average)
