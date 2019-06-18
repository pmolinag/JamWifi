import os
import sys
from subprocess import Popen, PIPE
import subprocess
import kivy
from kivy.app import App
from kivy.uix.widget import Widget

class MainWidget(Widget):
    def type(self, type):
        subprocess.call('python3 {}'.format(type), shell=True)

class JammerApp(App):
    def build(self):
        return MainWidget()

if __name__=="__main__":
    JammerApp().run()
