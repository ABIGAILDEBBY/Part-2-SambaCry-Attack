# CMU 18731 HW3
# Code referenced from: git@bitbucket.org:huangty/cs144_bufferbloat.git
# Edited by: Soo-Jin Moon, Deepti Sunder Prakash

#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os

# Parse arguments

parser = ArgumentParser(description="Shrew tests")
parser.add_argument('--bw-host', '-B',
                    dest="bw_host",
                    type=float,
                    action="store",
                    help="Bandwidth of host links",
                    required=True)
parser.add_argument('--bw-net', '-b',
                    dest="bw_net",
                    type=float,
                    action="store",
                    help="Bandwidth of network link",
                    required=True)
parser.add_argument('--delay',
                    dest="delay",
                    type=float,
                    help="Delay in milliseconds of host links",
                    default='10ms')
parser.add_argument('--n',
                    dest="n",
                    type=int,
                    action="store",
                    help="Number of nodes in one side of the dumbbell.",
                    required=True)

parser.add_argument('--maxq',
                    dest="maxq",
                    action="store",
                    help="Max buffer size of network interface in packets",
                    default=1000)

# Expt parameters
args = parser.parse_args()

class DumbbellTopo(Topo):
    "Dumbbell topology for Shrew experiment"
    def build(self, n=3, bw_net=100, delay=20, bw_host=10, maxq=1000):
    #TODO: Add your code to create topology


        # Add hosts and switches
        hl1 = self.addHost( 'hl1' )
        hl2 = self.addHost( 'hl2' )
        a1 = self.addHost( 'a1' )
        hr1 = self.addHost( 'hr1' )
	hr2 = self.addHost( 'hr2' )
        a2 = self.addHost( 'a2' )
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add links
        self.addLink( hl1, s1, bw=bw_host, delay=delay, max_queue_size=maxq )
        self.addLink( hl2, s1, bw=bw_host, delay=delay, max_queue_size=maxq )
	self.addLink( a1, s1, bw=bw_host, delay=delay, max_queue_size=maxq )
	self.addLink( hr1, s2, bw=bw_host, delay=delay, max_queue_size=maxq )
	self.addLink( hr2, s2, bw=bw_host, delay=delay, max_queue_size=maxq )
	self.addLink( a2, s2, bw=bw_host, delay=delay, max_queue_size=maxq )
	self.addLink( s1, s2, bw=bw_host, delay=delay, max_queue_size=maxq )
topos = { 'mytopo': ( lambda: DumbbellTopo() ) }
	
def bbnet():
    "Create network and run shrew  experiment"
    print "starting mininet ...."
    topo = DumbbellTopo(n=args.n, bw_net=args.bw_net,
                    delay='%sms' % (args.delay),
                    bw_host=args.bw_host, maxq=int(args.maxq))

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink,
                  autoPinCpus=True)
    net.start()
    dumpNodeConnections(net.hosts)
    
    #TODO: Add your code to test reachability of hosts
    
    print "Testing network connectivity"
    net.pingAll()

    hl1,hl2,hr1,hr2 = net.get('hl1','hl2','hr1','hr2');
    #TODO: Add your code to start long lived TCP flows 

    # The code below creates the servers
    hl1.cmd('iperf -s -p 5001 &')
    hl2.cmd('iperf -s -p 5002 &')

    #This code creates the clients:
    hr1.cmd('iperf -c ' +hl1.IP() + ' -p 5001 -t 100 &')
    hr2.cmd('iperf -c ' +hl2.IP() + ' -p 5002 -t 100 &')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    bbnet()
