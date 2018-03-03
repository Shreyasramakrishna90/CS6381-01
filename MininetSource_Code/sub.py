import zmq
import time
from connections import notify
from connections import publisher_connect
import argparse

#This is our subscriber program, all the functions can be found in the connections.py program.
#The available publishers along with previous ones are displayed to the subscribers for selection.
#The users can select any of the publisher ports and topics for communication.
#If the publisher number and topics match, then the subscriber will start receiving the information from the subscribed publisher.
#One publisher can have multiple subscribers.
#Team members: Shreyas Ramakrishna, Veena Nalluri, Sanchita Basak, Anabil Munshi
# main function


def main():
	args = parseCmdLineArgs()
	pub_ip = args.pub_ip
	print(pub_ip)
	broker_ip = args.broker_ip
	owner = notify(broker_ip)
	#time.sleep(10)
	pub_num = raw_input("please choose the publisher:")
	topic = raw_input("please enter the topic:")
	number = int(raw_input("Subscription count within 1-100?? else default is 0:"))
	if (pub_num == '5600' or pub_num == '5601' or pub_num == '5602'):
		if (topic == 'ind' or topic == 'usa' or topic == 'chn' or topic == 'ger'):
			publisher_connect(pub_num, topic, owner,number,pub_ip)

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


if __name__ == "__main__":
    main()

