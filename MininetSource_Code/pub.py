#This is our publisher program, all the functions can be found in the connections.py program.
#There are three assigned ports for our implementation along with a set of topics.
#The users can select any of the publisher ports and topics for communication.
#For the simplicity of implementation, we could just assign one topic for each publisher.
#The register_pub function, sends all the information about the publisher being created to the broker.
#After the user entry, the create_publisher function starts a publisher running in a thread.
#Team members: Shreyas Ramakrishna, Veena Nalluri, Sanchita Basak, Anabil Munshi




import zmq
import sys
import time
import threading
from multiprocessing import Process
import argparse
import collections
from connections import register_pub
from connections import create_publisher 

#Main function to display the available publishers to the users
def main():
	args = parseCmdLineArgs()
	pub_ip = args.pub_ip
	print(pub_ip)
	broker_ip = args.broker_ip
	print("The 3 available ports for publishers are:\n 5600\n 5601\n 5602\n")
	print("The available topics are:\n ind\n usa\n chn\n ger\n")
	print("Kindly excuse my service, I can only handle one topic for a publisher request at once so please bare with my services")
	pub_num=raw_input('Please select a publisher from the available ones:')
	topic=raw_input('Please enter a topic associated with the chosen publisher:')
	if(pub_num=='5600' or pub_num== '5601' or pub_num== '5602'):
		if(topic=='ind' or topic=='usa' or topic=='chn' or topic=='ger'):
			print('The publisher: %s is available with topic: %s'% (pub_num,topic))
			#time.sleep(20)
			register_pub(pub_num, topic,broker_ip)
			Process(target=create_publisher(pub_num, topic,pub_ip)).start()

		else:
			print("please enter a topic from the available topics in the next try\n") 
	else:
		print("please enter an available port from the list in the next try\n")


def parseCmdLineArgs():
	# parse the command line
	parser = argparse.ArgumentParser()

	# add optional arguments
	parser.add_argument("-pub", "--pub_ip", default="10.0.0.2", type=str, help="Please enter Ip address of Publisher")
	parser.add_argument("-a", "--broker_ip", type=str, default="10.0.0.1", help="Please enter Ip address of Broker")

	args = parser.parse_args()

	return args



if __name__=="__main__":
	main()

