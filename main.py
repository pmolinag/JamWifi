import os
import sys
from subprocess import Popen, PIPE
import subprocess
import kivy
from kivy.app import App
from kivy.uix.widget import Widget

class MainWidget(Widget):
	def select(self, type):
		if type == 'deauthentication.py' or type == 'rts_cts_NAV.py' or type == 'selective_rts_cts_NAV.py':
			subprocess.Popen('sudo gnome-terminal -- python3 ./types/{}'.format(type), shell=True)
			return True
		else:
			return False

class MainApp(App):
    def build(self):
        return MainWidget()

if __name__=="__main__":
    MainApp().run()
