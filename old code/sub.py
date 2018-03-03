import zmq
import time
from connections import notify
from connections import publisher_connect


#main function
def main():
	owner=notify()
	pub_num=raw_input("please choose the publisher:")
	topic=raw_input("please enter the topic:")
	if(pub_num=='5600' or pub_num== '5601' or pub_num== '5602'):
		if(topic=='1' or topic=='2' or topic=='3' or topic=='4'):
			publisher_connect(pub_num, topic,owner)

		else:
			print("please enter a topic from the available topics in the next try\n")
	else:
		print("please enter an available port from the list in the next try\n")




if __name__=="__main__":
	main()


