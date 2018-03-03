#This is the broker middleware we have created.
#This program is responsible for communicating with the publisher and subscriber.
#One part of the code looks after the communication between the publisher and the broker. All the initial communication about topic and port info is sent to broker.
#The Broker assigns ownership order through a random generator.
#The Broker then sends all the inofrmation to the subscriber.
#We have implemented two reply-request patterns to accomplish this implementation.
#Team members: Shreyas Ramakrishna, Veena Nalluri, Sanchita Basak, Anabil Munshi


import time
import zmq
import random

import argparse


a=[0,0,0]
g=[0,0,0]
ports=['5600','5601','5602']
ports1=[0,0,0]
list1=[]
def circ_buffer1(msg):
	if not (msg in list1):
		list1.append(msg)
	return list1	

def circ_buffer(msg):
	list1.append(msg)
	return list1	

def main():
		args = parseCmdLineArgs()
		broker_ip = args.broker_ip
		#Requesting the publisher middleware for available publisher ports 
		print("Querying if there are any topics under which pulishers are publishing")
		context = zmq.Context()
		socket_req= context.socket(zmq.REP)
		socket_req.bind("tcp://"+broker_ip+":5621")
		print("Bound to port 5621 and waiting for any publisher to contact\n")
		msg12=socket_req.recv()
		print(msg12)
		print("connecting to publisher.................................\n")
		socket_req.send("Please send me the publisher info..........\n")
		msg=socket_req.recv()
		m1=circ_buffer1(msg)
		print("The available publishers are: %s" %m1)
		socket_req.send('Done...thank you!!!')

		#Ownership order has been implemented using random shuffle concept
		random.shuffle(ports)
		print('The ownership_strength order is %s' %ports)

		#Sending the subscriber the information about publisher ports
		socket_rep= context.socket(zmq.REP)
		socket_rep.bind("tcp://"+broker_ip+":5618")
		print("waiting for subscriber to query\n")
		msg1=socket_rep.recv()
		print(msg1)
		time.sleep(5)
		print("answering the subscriber with the information")
		m=circ_buffer1(msg)
		socket_rep.send_string("%s" %m)
		socket_rep.recv()
		socket_rep.send_string("%s %s %s" %(ports[0],ports[1],ports[2]))
		m2=m			

		#Pollers to monitor the ports for receiving connectivity information of different publishers and subscribers
		poller=zmq.Poller()
		poller.register(socket_req, zmq.POLLIN)
		poller.register(socket_rep, zmq.POLLIN)
	
		while True:
			events=dict(poller.poll())
			if socket_req in events:
				msg12=socket_req.recv()
				print(msg12)
				print("connecting to publisher.................................\n")
				socket_req.send("Please send me the publisher info..........\n")
				msg=socket_req.recv()
				m2=circ_buffer1(msg)
				print("The available publishers are: %s" %m2)
				socket_req.send('Done...thank you!!!')
				
			
			
			if socket_rep in events:
				print("waiting for subscriber to query............\n")
				msg1=socket_rep.recv(zmq.DONTWAIT)
				print(msg1)
				time.sleep(20)
				print("answering the subscriber with the information")
				socket_rep.send_string("%s" %m2)
				socket_rep.recv()
				socket_rep.send_string("%s %s %s" %(ports[0],ports[1],ports[2]))

				
def parseCmdLineArgs():
	# parse the command line
	parser = argparse.ArgumentParser()

	# add optional arguments
	parser.add_argument("-a", "--broker_ip", type=str, default="10.0.0.1", help="Please enter Ip address of Broker")

	args = parser.parse_args()

	return args
		

if __name__=="__main__":
	main()


