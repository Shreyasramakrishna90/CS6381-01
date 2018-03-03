#!/usr/bin/python                                                                            

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, pubnum,subnum):
        switch = self.addSwitch('s1')
        brokerHost = self.addHost('Broker')
        self.addLink(brokerHost,switch)
        # Python's range(N) generates 0..N-1
        for PUB in range(pubnum):
            pubHosts = self.addHost('PUB%s' % (PUB + 1))
            self.addLink(pubHosts, switch)
        for SUB in range(subnum):
            subHosts = self.addHost('SUB%s' % (SUB + 1))
            self.addLink(subHosts, switch)



def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo()
    net = Mininet(topo)
    net.start()
    print ("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print ("Testing network connectivity")
    net.pingAll()
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()
