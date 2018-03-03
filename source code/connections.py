#This program implements all the zmq socket operations. We have different functions to perform the publisher_register, subscriber_connect.
#We also have implemented the dieing subscriber requirement in the publisher_connect part of the implementation.
#We import all the functions written in this code to our main programs of pub, sub and broker_mw1
#Team members: Shreyas Ramakrishna, Veena Nalluri, Sanchita Basak, Anabil Munshi


import zmq
import time

owner=[0,0,0]
list1=[]

def circ_buffer(msg):
	list1.append(msg)
	return list1	

#function to create a publisher and bind it to required port before sending messages
def create_publisher(x, y):
	context = zmq.Context()
	socket= context.socket(zmq.PUB)
	socket.bind("tcp://127.0.0.1:%s" %x)
	time.sleep(40)
	t=0
	for x1 in range (0,20):
		t=circ_buffer(x1)
		socket.send_string("%s %s %s" %(y, str(x1),t))
		time.sleep(5)
			
	socket.send_string('dieing')
	print('Will die in 100 seconds')
	time.sleep(100)	
	socket.close()

#function to register the publisher information to the broker
def register_pub(x, y):
	print('Registering the publisher information to broker\n')
	context = zmq.Context()
	socket= context.socket(zmq.REQ)
	socket.connect("tcp://127.0.0.1:5621")
	socket.send('hi....are you there....................') 
	msg1=socket.recv()
	#time.sleep(5)
	print("answering the broker with the information about publisher and topic")
	socket.send_string("%s %s" %(x, y))
	msg123=socket.recv()
	print(msg123)
	socket.close()



#function to notify the subscriber info about available publishers and ownership strength
def notify():
	print("Asking the broker for publishers and topics available")
	context = zmq.Context()
	socket= context.socket(zmq.REQ)
	socket.connect("tcp://localhost:5618")
	print("trying to get topics and publisher info from the broker\n")
	socket.send("Please send me the topic and publisher info\n")
	msg2=socket.recv()
	print("The available publishers and topics are: %s" %msg2)
	socket.send('send me the ownership strength')
	msg13=socket.recv_string()
	print(msg13)
	owner[0],owner[1],owner[2]=msg13.split()
	time.sleep(10)
	return(owner)
	msg13=None
	socket.close()

#function to bind the subscriber to the available publisher	
def publisher_connect(pub_num, topic,owner, number):
	poller=zmq.Poller()
	x=0
	context = zmq.Context()
	socket_sub= context.socket(zmq.SUB)
	socket_sub.connect("tcp://localhost:%s" %pub_num)
	poller.register(socket_sub, zmq.POLLIN)
	socket_sub.setsockopt(zmq.SUBSCRIBE, '')
	print("connected to publisher with port number %s and topic %s" %(pub_num,topic))
	while True:
		event=dict(poller.poll(10))
		if socket_sub in event:
			if(x<number) or (number==0):
				x=x+1
				message=socket_sub.recv_string()
				print(message)
				if(message=='dieing'):
					if(pub_num==owner[0]):
						print("hi")
						socket_sub1= context.socket(zmq.SUB)
						socket_sub1.connect("tcp://localhost:%s" %owner[1])
						poller.register(socket_sub1, zmq.POLLIN)
						socket_sub1.setsockopt(zmq.SUBSCRIBE, '')
						print("Trying to connect to publisher with port number %s" %(owner[1]))		
						while True:
							event=dict(poller.poll(10))
							if socket_sub1 in event:
								message2=socket_sub1.recv_string()
								print(message2)
								if(message2=='dieing'):
									print('connect to the next in the order.....')
									socket_sub2= context.socket(zmq.SUB)
									socket_sub2.connect("tcp://localhost:%s" %owner[2])
									poller.register(socket_sub2, zmq.POLLIN)
									socket_sub2.setsockopt(zmq.SUBSCRIBE, '')
									print("Trying to connect to publisher with port number %s" %(owner[2]))		
									while True:
										event=dict(poller.poll(10))
										print('waiting..............................')
										if socket_sub2 in event:
											message3=socket_sub2.recv_string()
											print(message3)
											if(message3=='dieing'):
												print('nobody is avaialble........I will listen until anybody comes')
												time.sleep(5)
												

										'''
										else:
											print('no service.............................')
											time.sleep(5)
											#socket_sub2.close()
										'''				

								
					elif(pub_num==owner[1]):
						print("looking for next available ")
						socket_sub3= context.socket(zmq.SUB)
						socket_sub3.connect("tcp://localhost:%s" %owner[0])
						poller.register(socket_sub3, zmq.POLLIN)
						socket_sub3.setsockopt(zmq.SUBSCRIBE, '')
						print(" Trying to connect to the publisher with port number %s and topic %s" %(owner[0],topic))
						while True:
							event=dict(poller.poll(10))
							print('waiting..............................')
							if socket_sub3 in event:
								message4=socket_sub3.recv_string()
								print(message4)
								if(message4=='dieing'):
									print('connect to the next in the order.....')
									socket_sub4= context.socket(zmq.SUB)
									socket_sub4.connect("tcp://localhost:%s" %owner[2])
									poller.register(socket_sub4, zmq.POLLIN)
									socket_sub4.setsockopt(zmq.SUBSCRIBE, '')
									print("Trying to connect to publisher with port number %s and topic %s" %(owner[2]))		
									while True:
										event=dict(poller.poll(10))
										print('waiting..............................')
										if socket_sub4 in event:
											message5=socket_sub4.recv_string()
											print(message5)
											if(message5=='dieing'):
												print('nobody is avaialble........I will listen until anybody comes')
												time.sleep(5)
												
												
										else:
											print('no service.............................')
											time.sleep(5)
										
							'''			
							
							else:
								print('no service.............................')
								time.sleep(5)
								#socket_sub3.close()

							'''
							
						
					elif(pub_num==owner[2]):
						print("hi")
						socket_sub5= context.socket(zmq.SUB)
						socket_sub.connect("tcp://localhost:%s" %owner[0])
						poller.register(socket_sub5, zmq.POLLIN)
						socket_sub.setsockopt(zmq.SUBSCRIBE, '')
						print("Trying to connect to publisher with port number %s and topic %s" %(owner[0],topic))
						while True:
							event=dict(poller.poll(10))
							if socket_sub in event:
								message6=socket_sub5.recv_string()
								print(message6)
								if(message6=='dieing'):
									print('connect to the next in the order.....')
									socket_sub6= context.socket(zmq.SUB)
									socket_sub6.connect("tcp://localhost:%s" %owner[2])
									poller.register(socket_sub6, zmq.POLLIN)
									socket_sub6.setsockopt(zmq.SUBSCRIBE, '')
									print("Trying to connect to publisher with port number %s and topic %s" %(owner[2]))		
									while True:
										event=dict(poller.poll(10))
							
										if socket_sub6 in event:
											message7=socket_sub6.recv_string()
											print(message7)
											if(message7=='dieing'):
												print('nobody is avaialble........I will listen until anybody comes')
												time.sleep(5)
											
										
										else:
											print('no service.............................')
											time.sleep(5)										

									
							'''
							else:
								print('no service.............................')
								time.sleep(5)
								#socket_sub5.close()
							'''
		
			else:
				print('I dont want the subscription of this publisher %s under topic %s' %(pub_num, topic))
				socket_sub.close()
				break
			
	socket_sub.close()


#Main function
def main():

	print('Hi from publisher middleware')



if __name__=="__main__":
	main()

