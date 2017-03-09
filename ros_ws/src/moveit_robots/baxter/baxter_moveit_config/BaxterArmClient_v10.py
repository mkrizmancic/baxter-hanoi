#!/usr/bin/env python

import rospy
import actionlib
import time
import sys
import math
import tf
from geometry_msgs.msg import Pose, PoseStamped
from baxter_moveit_config.msg import baxterAction, baxterGoal, baxterResult, baxterFeedback, IntList
from threading import Thread
from std_msgs.msg import Int16
from functools import partial
from Utils import Utils
from tf.transformations import quaternion_from_euler
from std_msgs.msg import Int16

class BaxterArmClient():

	def __init__(self):
		self.left_client = actionlib.SimpleActionClient("baxter_action_server_left", baxterAction)
		self.left_client.wait_for_server()
		self.listener = tf.TransformListener()

	def transformations(self, stup):
		#transformacija markera sa stupova u bazu baxtera
		if stup == 0: 	#stup A
			self.listener.waitForTransform("/base", "/stup", rospy.Time(0), rospy.Duration(8.0))
			(trans, rot) = self.listener.lookupTransform('/base', '/stup', rospy.Time(0))
		elif stup == 1: #stup B
			self.listener.waitForTransform("/base", "/stup", rospy.Time(0), rospy.Duration(8.0))
			(trans, rot) = self.listener.lookupTransform('/base', '/stup', rospy.Time(0))		
		elif stup == 2: #stup C
			self.listener.waitForTransform("/base", "/stup", rospy.Time(0), rospy.Duration(8.0))
			(trans, rot) = self.listener.lookupTransform('/base', '/stup', rospy.Time(0))			
		return trans

	def position(self, target_position, trans, height, width):
		#pozicija robota, height-visina, ovisi o tome koliko je koluta na stupu
		#widht - ovisi o tome koji je kolut na redu 
		roll=-math.pi/2
		pitch=0
		yaw=-math.pi/2
		quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
		target_position.orientation.x = quaternion[0]
  		target_position.orientation.y = quaternion[1]
		target_position.orientation.z = quaternion[2]
		target_position.orientation.w = quaternion[3]
		target_position.position.x = trans[0] + 0.08 + width -0.18 - 0.05 #0.05 dodano 8.2.	
		target_position.position.y = trans[1] -0.05
		target_position.position.z = trans[2] + height -0.015#+0.02 #0.02 za markere na papiru, malo iznad onog sto je bilo prije
		return target_position

	def go_to_position(self, task, destination, height, width, offset_x, offset_y, offset_z):
		goal = Pose()
		trans = self.transformations(destination)
		if task == 'pick':
			height = Utils().get_pick_height(height)
		else: 
			height = Utils().get_place_height(height)
		goal = self.position(goal, trans, height, width)
		#if destination==0 : offset_y-=0.18
		#if destination==2 : offset_y+=0.18
		#if destination==2 : offset_z+=0.005
		#if destination==0 : offset_y-=0.00
		#if destination==1 : offset_y+=0.18
		#if destination==2 : offset_y+=0.40
		#16.2.2017.
		if destination==0: offset_y-=0.2
		if destination==1: offset_y+=0
		if destination==2: offset_y+=0.2
		offset_z+=0.05
		offset_z-=0.02
		offset_y-=0.05
		if destination==0: offset_z-=0.005
		if destination==1: offset_z-=0.005		

		goal.position.x = goal.position.x + offset_x
		goal.position.y = goal.position.y + offset_y 
		goal.position.z = goal.position.z + offset_z
		goal_final = baxterGoal(id = 1, pose = goal)
		
		self.left_client.send_goal_and_wait(goal_final)
		result = self.left_client.get_result()
		#print result.status
		if result.status:
			#print 'succeeded'
			return 1 
		else:
			#print 'aborted'
			return 0
		

	def close_gripper(self):
		goal = Pose()
		goal_final = baxterGoal(id=3, pose = goal)
		#self.left_client.send_goal(goal_final)
		#result = self.left_client.wait_for_result()
		status = self.left_client.send_goal_and_wait(goal_final)
		result = self.left_client.wait_for_result()
		
		#if result == GoalStatus.SUCCEEDED:
			#return 1
		#else: return 0
	
	def open_gripper(self):
		goal = Pose()
		goal_final = baxterGoal(id=2, pose = goal)
		self.left_client.send_goal(goal_final)
		self.left_client.wait_for_result()	
		

	def pick(self, pick_destination, pick_height, width):
		offset = Utils().get_pick_height(pick_height) 
		pick1 = self.go_to_position('pick', pick_destination, pick_height, width, 0, 0, 0 ) #odi na poziciju
		if pick1: 
			pick2 = self.go_to_position('pick', pick_destination, pick_height, width, 0.1, 0, 0) #odi na ofset poziciju
			print 'PICK 1 ok'
			if pick2: 
				print 'PICK 2 ok'
				pick3 = self.close_gripper() #zatvori gripper 
				if pick2:
					print 'PICK 3 ok' 
					pick4 = self.go_to_position('pick', pick_destination, pick_height, width, 0.1, 0, 0.28-offset)#digni se ravno iznad stupa
					if pick4:
						print 'PICK 4 ok' 
						return 1
					else: return 0
				else: return 0 
			else: return 0
		else: return 0	
		
		
	def place(self, place_destination, place_height, width):
		offset= Utils().get_place_height(place_height)
		place1 = self.go_to_position('place', place_destination, place_height, width, 0.1, 0, 0.28-offset)#postavi se okomito iznad odredisnog stupa
		if place1:
			place2 = self.go_to_position('place', place_destination, place_height, width, 0.1, 0, 0)#spusti se dolje
			if place2: 
				place3 = self.open_gripper()
				if place2: 
					place4 = self.go_to_position('place', place_destination, place_height, width, 0.1, 0, -0.015) #izmakni se van
					if place4: 
						place5=self.go_to_position('place', place_destination, place_height, width, 0, 0, -0.015)
						if place5: return 1
						else: return 0
					else: return 0 
				else:return 0
			else: return 0 
		else: return 0 
	
	
	def calibration(self, width, nesto):
		#kalibracija stupova, odi na poziciju koluta na prvom drugom i trecem stupu
		self.go_to_position('pick', 0, 1, width, 0.1+0.15, 0, 0)
		rospy.sleep(2)
		self.go_to_position('pick', 1, 1, width, 0.1+0.15, 0, 0)
		rospy.sleep(2)
		self.go_to_position('pick', 2, 1, width, 0.1+0.15, 0, 0)
		rospy.sleep(2)

	def calibration2(self, width, nesto):
		#def go_to_position(self, task, destination, height, width, offset_x, offset_y, offset_z)
		#kalibracija visine, odi na prvi, drugi i treci kolut na prvom stupu. 
		self.go_to_position('pick', 0, 1, width, 0, 0, 0)
		self.go_to_position('pick', 0, 1, width, 0.1, 0, 0)
		rospy.sleep(10)
		self.go_to_position('pick', 0, 1, width, 0.1, 0, 0.01)
		self.go_to_position('pick', 0, 1, width, 0, 0, 0)

		self.go_to_position('pick',0, 2, width, 0, 0, 0)
		self.go_to_position('pick', 0, 2, width, 0.1, 0, 0)
		rospy.sleep(10)
		self.go_to_position('pick', 0, 2, width, 0.1, 0, 0.01)
		self.go_to_position('pick', 0, 2, width, 0, 0, 0)

		self.go_to_position('pick',0, 3, width, 0, 0, 0)
		self.go_to_position('pick', 0, 3, width, 0.1, 0, 0)
		rospy.sleep(10)
		self.go_to_position('pick', 0, 3, width, 0.1, 0, 0.01)
		self.go_to_position('pick', 0, 3, width, 0, 0, 0)

		

		
		

	def pick_and_place(self, pick_destination, pick_height, place_destination, place_height, width):
		
		print '------PICK---------------', pick_destination, pick_height
		pick = self.pick(pick_destination, pick_height, width)
		if pick == 0: 
			print 'Pick locations not reachable'
			return 0
		else:
			print '------PLACE--------------',place_destination, place_height
			place = self.place(place_destination, place_height, width)
			if place == 0: 
				print 'place locations not reachable'
				return 0
			else: 
				return 1
		

	def start(self, pick_destination, pick_height, place_destination,place_height, width):
		
		thread = Thread(target = self.pick_and_place, args=(pick_destination, pick_height, place_destination,place_height, width))
		thread.start()
		thread.join()

	def kalibracija_kolutovi(self,width):
		thread = Thread(target = self.calibration2, args=(width,1))
		thread.start()
		thread.join()

	def kalibracija_stupovi(self,width):
		thread = Thread(target = self.calibration, args=(width,1))
		thread.start()
		thread.join()

if __name__ == '__main__':
	rospy.init_node('baxter_client',anonymous=True, disable_signals = True)
	try:
		client = BaxterArmClient()
		client.start()	
	except rospy.ROSInterruptException:
		rospy.loginfo('Terminating baxter_client.')

				

















	
