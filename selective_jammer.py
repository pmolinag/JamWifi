#!/usr/bin/python3

from scapy.all import *
from wifi import Cell
import time
from wireless import Wireless
import os
import sys
from subprocess import Popen, PIPE

DN = open(os.devnull, 'w')

if __name__ == "__main__":
