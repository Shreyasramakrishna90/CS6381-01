import time
import zmq


def main():
	#Requesting the broker for publishers information
	print("Asking the broker for publishers and topics available")
	context = zmq.Context()
	socket= context.socket(zmq.REQ)
	socket.connect("tcp://localhost:5614")
	print("trying to get topics and publisher info from the broker\n")
	socket.send("Please send me the topic and publisher info\n")
	msg2=socket.recv()
	print("The available publishers and topics are: %s" %msg2)
	time.sleep(10)
	socket.close()
	

if __name__=="__main__":
	main()
