#!/usr/bin/env python3
#SPoschandler.py written by Robin Newman, July 2017 
#Provides the "glue" to enable the GPIO on Raspberry Pi
#to communicate with Sonic Pi. Sonic Pi can control LEDs etc,and receive
#input from devices like push buttons connected to GPIO pins
#Sonic Pi can be running either on the Raspberry Pi,
#or on an external networked computer

#The program requires gpiod daemon to be running. Yu can install this with
#sudo apt-get update followed by sudo apt-get install pigpio if you don't have it
#best to set it up to auto start on boot using
#sudo systemctl enable pigpiod.service          (followed by a reboot)
#The program also requires gpiozero to be installed and python-osc

import os
from gpiozero import Button
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from time import sleep
import argparse
import sys

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
    sender.send_message('/test',0)
    print('test')
    sleep(0.1)
def msg1():
    #sender client set up in __main__ below
    sender.send_message('/test',1)
    sleep(0.01)
def msg2():
    #sender client set up in __main__ below
    sender.send_message('/test',2)
    sleep(0.01)
def msg3():
    #sender client set up in __main__ below
    sender.send_message('/test',3)
    sleep(0.01)
def msg4():
    #sender client set up in __main__ below
    sender.send_message('/test',4)
    sleep(0.01)
def msg5():
    #sender client set up in __main__ below
    sender.send_message('/test',5)
    sleep(0.01)
def msg6():
    #sender client set up in __main__ below
    sender.send_message('/test',6)
    sleep(0.01)
def msg7():
    #sender client set up in __main__ below
    sender.send_message('/test',7)
    sleep(0.01)

def send_message(message):
	#sender client set up in __main__ below
    sender.send_message(message)

#this is where the msg routing is activated
button0.when_pressed = msg0
button1.when_pressed = msg1
button2.when_pressed = msg2
button3.when_pressed = msg3
button4.when_pressed = msg4
button5.when_pressed = msg5
button6.when_pressed = msg6
button7.when_pressed = msg7

while True:
    try:
		#use try...except to handle possible errors
        #first set up and deal with input args when program starts
        parser = argparse.ArgumentParser()
        #This arg gets the server IP address to use. 127.0.0.1 or
        #The local IP address of the PI, required when using external Sonic Pi
        parser.add_argument("--ip",
        default="127.0.0.1", help="The ip to listen on")
        #This is the port on which the server listens. Usually 8000 is OK
        #but you can specify a different one
        parser.add_argument("--port",
              type=int, default=8000, help="The port to listen on")
        #This is the IP address of the machine running Sonic Pi if remote
        #or you can omit if using Sonic Pi on the local Pi.
        parser.add_argument("--sp",
              default="127.0.0.1", help="The ip Sonic Pi is on")
        args = parser.parse_args()
        if args.ip=="127.0.0.1" and args.sp !="127.0.0.1":
            #You must specify the local IP address of the Pi if trying to use
            #the program with a remote Sonic Pi aon an external computer
            raise AttributeError("--ip arg must specify actual local machine ip if using remote SP, not 127.0.0.1")
        #Provide feed back to the user on the setup being used    
        if args.sp == "127.0.0.1":
            spip=args.ip
            print("local machine used for SP",spip)  
        else:
            spip=args.sp
            print("remote_host for SP is",args.sp)
        #setup a sender udp-client to send out OSC messages to Sonic Pi
        #Sonic Pi listens on port 4559 for incoming OSC messages
        sender=udp_client.SimpleUDPClient(spip,4559) #sender set up for specified IP
        #dispatcher reacts to incoming OSC messages and then allocates
        #different handler routines to deal with them
        dispatcher = dispatcher.Dispatcher()
        #The following handler responds to the OSC message /testprint
        #and prints it plus any arguments (data) sent with the message
        dispatcher.map("/testprint",print)
        #Now set up and run the OSC server
        server = osc_server.ThreadingOSCUDPServer(
              (args.ip, args.port), dispatcher)
        print("Serving on {}".format(server.server_address))
        #run the server "forever" (till stopped by pressing ctrl-C)
        server.serve_forever()
    #deal with some error events
    except KeyboardInterrupt:
        print("\nServer stopped") #stop program with ctrl+C
    #Used the AttributeError to specify problems with the local ip address
    except AttributeError as err:
        print(err.args[0])
    #handle errors generated by the server
    except OSError as err:
       print("OSC server error",err.args)
    #anything else falls through
