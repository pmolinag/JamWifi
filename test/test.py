import unittest
import sys
import os
sys.path.append("..")
from jammer import MainWidget

class TestApp(unittest.TestCase):

	#Test if Type function from MainWidget class works
	def testType(self):
		false = MainWidget.type(self, "other")
		self.assertEqual(false, False)

if __name__ == '__main__':
	unittest.main()
