import rospy
import math
import numpy
#from client_doma import BaxterArmClient
from BaxterArmClient_v08 import BaxterArmClient
from Utils import Utils

class Startup:

	#def __init__(self):
	#	self.client = BaxterArmClient()

	#def check_positions(self, arm):
	#	if arm == 'left'
			

	def calibrate_all(self, client):

		while True:
			key = raw_input('Upisite oznaku stupa na koji se zelite pozicionirati, A, B ili C. Za kraj pritisnite Q. ')
			if key == 'A':
				print 'pozicioniranje na stup A'
				self.client.calibrate(0)
			elif key == 'B':
				print 'pozicioniranje na stup B'
				self.client.calibrate(1)
			elif key == 'C':
				print 'pozicioniranje na stup C'
				self.client.calibrate(2)
			#elif key == 'Q':
			#	return

if __name__ == '__main__':
	try:
		Startup()
	except rospy.ROSInterruptException:
		pass		
