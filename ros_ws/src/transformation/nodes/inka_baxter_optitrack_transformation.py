#!/usr/bin/env python 
#kod preuzet iz diplomskog rada Inke Brijacak 
import rospy
import tf
import math
from PyKDL import Vector, Frame, Rotation

if __name__ == '__main__':
    rospy.init_node('baxter_optitrack_transformer')

    listener = tf.TransformListener()
    br = tf.TransformBroadcaster()

    rate = rospy.Rate(50.0)
    while not rospy.is_shutdown(): 

        # Transformation -------------------------------------------------------------
        #T_GB_p=Vector(0.0707,0.0187,-0.8593)  # project
        #T_GB_Q=Rotation.Quaternion(-0.004002,-0.004752,0.999994,-0.000251)
        #T_GB=Frame(T_GB_Q,T_GB_p) [0.101118 <-0.573142, 0.049050, 0.811713>]  (0.421538700623461, 0.5060896478392994, 0.5964256398717394, -0.45875358127230415)

        T_GB_p=Vector(-0.0157712999511,-0.835218066682,-0.0674771192051) #INKA
        T_GB_Q=Rotation.Quaternion(-0.484148,-0.486831,-0.522866, 0.505181)  # qz,qx,qy,qw    INKA    


	#T_GB_p=Vector(0.0366584397092, -0.839661563598, -0.202769519381)    #JA
	#T_GB_Q=Rotation.Quaternion(0.421538700623461, 0.5060896478392994, 0.5964256398717394, -0.45875358127230415)  # qz,qx,qy,qw   JA
        T_GB=Frame(T_GB_Q,T_GB_p)

        T_empty_p=Vector(0,0,0)
        T_empty_Q=Rotation.Quaternion(0,0,0,1)
        T_empty=Frame(T_empty_Q,T_empty_p)

        Rotx_p = Vector(0, 0, 0)
	Rotx_Q = Rotation.Quaternion(0.70682518,0,0,0.70682518) # x za 90
	Rotx = Frame(Rotx_Q, Rotx_p)

	Roty_p = Vector(0, 0, 0)
        Roty_Q = Rotation.Quaternion(0,0.70682518,0,0.70738827)  # y za 90
        Roty = Frame(Roty_Q, Roty_p)

        Rotz_p = Vector(0, 0, 0)
        Rotz_Q = Rotation.Quaternion(0,0,0.70682518,0.70738827)  # z za 90
        Rotz = Frame(Rotz_Q, Rotz_p)

        #T_GB = Rotz*Roty*T_GB  # prvi Roty je kad je baxter okrenut prema ploci!!
	#T_GB = Roty*T_GB #OVO JE ZADNJI PUT RADILO!!!ovo je moje !!!!

	T_GB = Roty*T_GB #ili #bez ovog Roty....jednom radi jedno, drugi put drugo ?!?!?

        # sending new Transformations -----------------------------------------------
        br.sendTransform(T_GB.p,T_GB.M.GetQuaternion(),rospy.Time.now(),'base','/kruna')
        br.sendTransform(T_GB.p,T_GB.M.GetQuaternion(),rospy.Time.now(),'reference/base','/kruna') 
        br.sendTransform(T_empty.p,T_empty.M.GetQuaternion(),rospy.Time.now(),'world','base')
        rate.sleep()
