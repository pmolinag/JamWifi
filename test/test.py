import unittest, sys, os
from scapy.all import *

class TestApp(unittest.TestCase):

	#Test if calcule_time function from Controller class works
	def test_calcule_packets(self):
		time = 1
		packets = (60*time)/0.0001
		self.assertEqual(packets, 600000)

	#Test if calcule_time function from Controller class works
	def test2_calcule_packets(self):
		time = 1
		packets = (60*time)/0.03
		self.assertEqual(packets, 2000)

	#Test if the deauthentication jammer build the packet correctly
	def test_create_deauthentication(self):
		packet = RadioTap()/Dot11(addr1='ff:ff:ff:ff:ff:ff',addr2='ff:ff:ff:ff:ff:ff',addr3='ff:ff:ff:ff:ff:ff')/Dot11Deauth()
		self.assertEqual(packet.summary(), "RadioTap / 802.11 Management 12 ff:ff:ff:ff:ff:ff > ff:ff:ff:ff:ff:ff / Dot11Deauth")

	#Test if the deauthentication jammer build the packet correctly
	def test_create_rts(self):
		packet = RadioTap()/Dot11(type=1, subtype=11, addr1='ff:ff:ff:ff:ff:ff',addr2='ff:ff:ff:ff:ff:ff', ID=0xFF7F)
		self.assertEqual(packet.summary(), "RadioTap / 802.11 Control 11 ff:ff:ff:ff:ff:ff > ff:ff:ff:ff:ff:ff")

	#Test if the deauthentication jammer build the packet correctly
	def test_create_cts(self):
		packet = RadioTap()/Dot11(type=1, subtype=12, addr1='ff:ff:ff:ff:ff:ff', ID=0xFF7F)
		self.assertEqual(packet.summary(), "RadioTap / 802.11 Control 12 00:00:00:00:00:00 > ff:ff:ff:ff:ff:ff")
if __name__ == '__main__':
	unittest.main()
