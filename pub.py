import zmq
import sys
import time
#import pub_mw
import threading
from multiprocessing import Process
import collections
from connections import register_pub
from connections import create_publisher 

#Main function to display the available publishers to the users
def main():
	

	print("The 3 available ports for publishers are:\n 5600\n 5601\n 5602\n")
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

