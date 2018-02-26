import zmq
import sys
import time
import pub_mw
import threading
from multiprocessing import Process
import collections

port1=5600
port2=5601
port3=5602

list=[]
#function to send the history along with previous messages
def circ_buffer(x):
	if not (x in list):
		list.append(x)
	return list	


def create_publisher(port_num, topic):
	context = zmq.Context()
	socket= context.socket(zmq.PUB)
	socket.bind("tcp://127.0.0.1:%s" %port_num)
	time.sleep(20)
	t=0
	for x in range (0,20):
		t=circ_buffer(x)
		socket.send_string("%s %s %s" %(topic, str(x),t))
		time.sleep(5)
			
	socket.send_string('dieing')
	print('Will die in 100 seconds')
	time.sleep(100)	
	socket.close()

def register_pub(pub_num, topic):
		print('Registering the publisher information to broker\n')
		context = zmq.Context()
		socket= context.socket(zmq.REQ)
		socket.connect("tcp://127.0.0.1:5621")
		socket.send('hi....are you there....................') 
		msg1=socket.recv()
		#time.sleep(5)
		print("answering the broker with the information about publisher and topic")
		socket.send_string("%s %s" %(pub_num, topic))
		msg123=socket.recv()
		print(msg123)
		socket.close()


#Main function to display the available publishers to the users
def main():
	

	print("The 4 available ports for publishers are:\n 5600\n 5601\n 5602\n")
	print("The available topics are:\n 1\n 2\n 3\n 4\n")
	print("Kindly excuse my service, I can only handle one topic for a publisher request at once so please bare with my services")
	pub_num=raw_input('Please select a publisher from the available ones:')
	topic=raw_input('Please enter a topic associated with the chosen publisher:')
	if(pub_num=='5600' or pub_num== '5601' or pub_num== '5602'):
		if(topic=='1' or topic=='2' or topic=='3' or topic=='4'):
			print('The publisher: %s is available with topic: %s'% (pub_num,topic))
			time.sleep(20)
			register_pub(pub_num, topic)
			Process(target=create_publisher(pub_num, topic)).start()

		else:
			print("please enter a topic from the available topics in the next try\n") 
	else:
		print("please enter an available port from the list in the next try\n")



if __name__=="__main__":
	main()

