#!/usr/bin/python
 
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf
 
def aggNet():
 
    CONTROLLER_IP='127.0.0.1'
 
    net = Mininet( topo=None,
                build=False)
 
    net.addController( 'c0',
                    controller=RemoteController,
                    ip=CONTROLLER_IP,
                    port=6633)
 
    h1 = net.addHost( 'h1', ip='0.0.0.0' )
    h2 = net.addHost( 'h2', ip='0.0.0.0' )
    h3 = net.addHost( 'h3', ip='0.0.0.0' )
    s1 = net.addSwitch( 's1' )
 
 
    net.addLink( h1, s1 )
    net.addLink( h2, s1 )
    net.addLink( h3, s1 )
 
    net.start()
    CLI( net )
    net.stop()
 
if __name__ == '__main__':
    setLogLevel( 'info' )
    aggNet()
