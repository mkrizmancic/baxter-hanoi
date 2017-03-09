import math
import rospy

class Utils:
	def get_right_joints(self):
		return [0.0859029240234, -0.859029240234, 0.623179694366, 1.46073320359, 0.230480613116, 1.58421865688, -0.500844726672]

	def get_left_joints(self):
		return [0.018791264651596317, -0.6657476619422695,-1.1125195664138963, 1.4162477624152083, 0.7781117546548761, 1.3023496889147164, -0.33402431656204884] #kad je rotiran za 90
	
	def get_width(self, kolut_br):
		if kolut_br == 1:
			return -0.27
		elif kolut_br == 2:
			return -0.3
		else:
			return -0.31

	def get_pick_height(self, height):
		#return height*0.04 #kad radi sebi bocno
		#return height*0.04 - 0.03 #kad radi ispred sebe, odozgo
		#return height*0.05 -0.04 -0.02
		return height*0.06 - 0.05 - 0.02 - 0.005
	
	def get_place_height(self, height):
		#return height*0.04 + 0.04
		#return height*0.04 + 0.04 + 0.01 - 0.03 ispred sebe, odozgo
		#return height*0.055 + 0.05 -0.04 -0.025 +0.005
		return height*0.06 + 0.05 -0.04 -0.025 + 0.007 
		

	
