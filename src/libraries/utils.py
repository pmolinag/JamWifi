from wifi import Cell
from wireless import Wireless
import time, subprocess, os
from subprocess import PIPE
FNULL = open(os.devnull, 'w')

def network_scan():
    wifi_card = Wireless()
    interface = wifi_card.interface()
    wifi_collect = Cell.all(interface)
    print ("Available networks scan in progress ...")
    print ("#" * 40)
    time.sleep(0.5)
    for wi in wifi_collect:
        print("SSID: " + wi.ssid)
        print("BSSID: " + wi.address)
        print("Channel: " + str(wi.channel))
        #print("Quality: " + str(wi.quality))
        print("+-" * 10)
        time.sleep(0.5)
    print ("#" * 40)

def clear():
    subprocess.call('clear', shell=True)

def show(name):
    subprocess.call('figlet {}'.format(name), shell=True)

    #def quit_monitor_mode(self, card):
    #    subprocess.call('sudo ip link set {} down'.format(card), shell=True)
    #    subprocess.call('sudo iw dev {} set type managed'.format(card), shell=True)
    #    subprocess.call('sudo ip link set {} up'.format(card), shell=True)
    #    subprocess.call('service network-manager start', shell=True)

    #def injection_test(self, card):
    #    try:
    #        i = 0
    #        while i < 2:
    #            subprocess.call('aireplay-ng --test {}'.format(card), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
    #        i = i + 1
    #    except KeyboardInterrupt:
    #        pass

def injection_test(bssid, card):
    subprocess.call('aireplay-ng --test -a {} {}'.format(bssid, card), shell=True)

# Calculate the time to Jam
def calcule_paquets(attack, time):

    if attack == "Deauthentication":

        time = int(time)

        packets = (60*time)/0.0001

        packets = int(packets)

    elif attack == "RTS/CTS NAV" or attack == "selective RTS/CTS NAV":

        time = int(time)

        packets = (60*time)/0.032767

        packets = int(packets)

    return packets

def kill_processes():

    subprocess.call('airmon-ng check kill', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

# Get the mac of the card
def get_mac(card):
    card_mac = subprocess.Popen('ifdata -ph {}'.format(card), stdout=PIPE, shell=True).stdout
    card_mac = card_mac.read()
    card_mac = card_mac.decode()
    return card_mac

#def monitor_mode(self, card, channel):
#    #Start monitor mode on the selected device
#    subprocess.call('sudo ip link set {} down'.format(card), shell=True)
#    subprocess.call('sudo iw dev {} set type monitor'.format(card), shell=True)
#    subprocess.call('sudo ip link set {} up'.format(card), shell=True)
#    subprocess.call('sudo iw dev {} set channel {}'.format(card, channel), shell=True)

def monitor_mode(card, channel):
    subprocess.call('airmon-ng start {} {}'.format(card, channel), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

def quit_monitor_mode(card):
    subprocess.call('airmon-ng stop {}'.format(card), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
