from models.deauthentication import Deauthentication
from models.rts_cts_NAV import RTS_CTS_NAV
from libraries.utils import *
import os

class Controller():

    def nav_jamming(self, address, card_mac, monitor_card, selective, subtype, packets, inter):
        nav = RTS_CTS_NAV(address, card_mac, monitor_card, subtype, packets, inter)
        nav.create_packet()
        if selective == False:
            nav.jam()
        else:
            nav.sniff()
        quit_monitor_mode(monitor_card)


    def deauthentication_jamming(self, client, address, packets, monitor_card):
        dea = Deauthentication(client, address, packets, monitor_card)
        dea.create_packet()
        dea.jam()
        quit_monitor_mode(monitor_card)
