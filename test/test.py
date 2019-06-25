import unittest
import sys
import os
sys.path.append("..")
from main import MainWidget
from src.jammer import Jammer

class TestApp(unittest.TestCase):

	#Test if Type function from MainWidget class works
	def testType(self):
		false = MainWidget.select(self, "other")
		self.assertEqual(false, False)

	#Test if calcule_time function from Jammer class works
	def testTime(self):
		time = Jammer.calcule_time(1)
		self.assertEqual(time, 1831)

if __name__ == '__main__':
	unittest.main()
