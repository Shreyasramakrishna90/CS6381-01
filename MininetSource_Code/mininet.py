#!/usr/bin/env /usr/local/bin/python /usr/bin/python
# encoding: utf-8

import os  # OS level utilities
import sys
import argparse  # for command line parsing

from signal import SIGINT
import time
import threading
# import zmq

import subprocess

# These are all Mininet-specific
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import CLI
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.util import pmonitor
from SingleSwitchTopology import SingleSwitchTopo


##################################
# Command line parsing
##################################
def parseCmdLineArgs():
    # parse the command line
    parser = argparse.ArgumentParser()

    # add optional arguments
    parser.add_argument("-p", "--publisher", type=int, default=3, help="Number of publishers, default 3")
    parser.add_argument("-s", "--subscriber", type=int, default=5, help="Number of subscriber, default 5")
    parser.add_argument("-T", "--topo", type=int, choices=[1, 2], default=1,help='Topology choice 1.Single Switch Topology 2. Tree Topology')


    # parse the args
    args = parser.parse_args()

    return args


def broker_helper(brokerHost):
    def broker_op():
        # Invoke broker
        broker_ip = brokerHost.IP()
        command = 'xterm -e python broker.py'
        brokerHost.cmd(command)

    threading.Thread(target=broker_op, args=()).start()
    time.sleep(1)


def pub_helper(pubHosts, broker_ip):
    for pub in pubHosts:
        def pub_op():
            # print(broker_ip)
            # print(pubHosts[0].IP())
            command = 'xterm -e python pub.py -pub ' + pub.IP() + ' -a ' + broker_ip
            pub.cmd(command)


        # print('hi')
        threading.Thread(target=pub_op, args=()).start()
        time.sleep(len(pubHosts))


def sub_helper(pubHosts, subHosts, broker_ip):
    # Invoke subscribers

    if(len(subHosts)==1):
        def sub_op():
            command = 'xterm -e python sub.py -pub ' +pubHosts[0].IP() + ' -a ' + broker_ip
            subHosts[0].cmd(command)

        threading.Thread(target=sub_op, args=()).start()

    if(len(subHosts)==2):
        def sub_op():
            command = 'xterm -e python sub.py -pub ' + pubHosts[0].IP() + ' -a ' + broker_ip
            subHosts[0].cmd(command)

        threading.Thread(target=sub_op, args=()).start()
        time.sleep(50)

        def sub_op1():
            command = 'xterm -e python sub.py -pub ' + pubHosts[1].IP() + ' -a ' + broker_ip
            subHosts[1].cmd(command)

        threading.Thread(target=sub_op1, args=()).start()




def runTestCase(pubHosts, subHosts, brokerHost):
    broker_ip = brokerHost.IP()
    pub_helper(pubHosts, broker_ip)
    broker_helper(brokerHost)
    sub_helper(pubHosts, subHosts, broker_ip)

    while True:
        pass


def mainHelper(topo):
    # create the network
    print('Instantiate network')
    net = Mininet(topo=topo, link=TCLink)

    # activate the network
    print('Activate network')
    net.start()

    # debugging purposes
    print('Dumping host connections')
    dumpNodeConnections(net.hosts)

    # debugging purposes
    print('Testing network connectivity')
    net.pingAll()

    pubhosts = []
    subhosts = []
    brokerhost = None
    for host in net.hosts:

        if 'PUB' in host.name:
            pubhosts.append(host)
        elif 'SUB' in host.name:
            subhosts.append(host)
        elif 'Broker' in host.name:
            brokerhost = host
    print('Available hosts are %s' % net.hosts)
    print('SUB %s\nPUB %s\n Broker %s\n' % (pubhosts, subhosts, brokerhost))
    runTestCase(pubhosts, subhosts, brokerhost)

    net.stop()


#####################
# main program
######################
def main():

    print('---------------------------------------------------')

    args = parseCmdLineArgs()

    pub_num = args.publisher
    sub_num = args.subscriber
    topo_choice = args.topo

    # SingleSwitchTopology
    if topo_choice == 1:
        # instantiate our topology
        print('Instantiate topology')
        topo = SingleSwitchTopo(pubnum=pub_num, subnum=sub_num)
        print(topo)
        mainHelper(topo)


if __name__ == '__main__':
    main()

