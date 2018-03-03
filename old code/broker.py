import time
import zmq
import random
import threading
from multiprocessing import Process


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
		
		#Requesting the publisher middleware for available publisher ports 
		print("Querying if there are any topics under which pulishers are publishing")
		context = zmq.Context()
		socket_req= context.socket(zmq.REP)
		socket_req.bind("tcp://*:5621")
		print("Bound to port 5621 and waiting for any publisher to contact\n")
		msg12=socket_req.recv()
		print(msg12)
		print("connecting to publisher.................................\n")
		socket_req.send("Please send me the publisher info..........\n")
		msg=socket_req.recv()
		#msg1=None
		m1=circ_buffer1(msg)
		#msg1=msg
		print("The available publishers are: %s" %m1)
		socket_req.send('Done...thank you!!!')

		random.shuffle(ports)
		print(ports)
		print(ports[0])

		#Sending the subscriber the information about publisher ports
		socket_rep= context.socket(zmq.REP)
		socket_rep.bind("tcp://127.0.0.1:5618") 
		print("waiting for subscriber to query\n")
		msg1=socket_rep.recv()
		print(msg1)
		time.sleep(5)
		print("answering the subscriber with the information")
		m=circ_buffer1(msg)
		socket_rep.send_string("%s" %m)
		socket_rep.recv()
		socket_rep.send_string("%s %s %s" %(ports[0],ports[1],ports[2]))
					

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
				#n=circ_buffer1(msg)
				socket_rep.send_string("%s" %m2)
				socket_rep.recv()
				socket_rep.send_string("%s %s %s" %(ports[0],ports[1],ports[2]))

				

			
		

if __name__=="__main__":
	main()


