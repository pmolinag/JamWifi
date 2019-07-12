import unittest
import sys
import os
from package.src import functions

class TestApp(unittest.TestCase):

	#Test if Type function from MainWidget class works
	def test_type(self):
		false = MainWidget.select(self, "other")
		self.assertEqual(false, False)

	#Test if calcule_time function from Jammer class works
	def test_paquets(self):
		time = Jammer.calcule_paquets(1)
		self.assertEqual(time, 1831)

	#Test if calcule_time function from Jammer class works
	def test_paquets_dea(self):
		time = Jammer.calcule_time(1)
		self.assertEqual(time, 600000)


if __name__ == '__main__':
	unittest.main()
