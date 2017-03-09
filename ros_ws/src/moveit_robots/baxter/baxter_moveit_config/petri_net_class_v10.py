#!/usr/bin/env python

import rospy
import math
import numpy
#from client_doma import BaxterArmClient
from BaxterArmClient_v10 import BaxterArmClient
#from calibration import Startup
from Utils import Utils
#ova funkcija je implementacija petrijeve mreze, odreduje se koji se kolut pomice sa kojeg na koji stup, dok se svi koluti ne pomaknu na treci stup. Pretpostavlja se da su u pocetnom stanju svi koluti na prvom stupu, odnosno stupu A. Pri inicijalizaciji je potrebno upisati broj koluta. 
class Petri_net:
	
	def __init__(self,s=[],konacno=[],U=[],slijedeci=None,trenutni=None,parno=None,n=None, sekvenca = None,pocetni_stup=None, krajnji_stup = None):
		self.s = s
		self.konacno = konacno
		self.U = U
		self.slijedeci = slijedeci
		self.parno = parno
		self.n = n #raw_input('Unesite broj kolutova: ')
		self.pocetni_stup = pocetni_stup
		self.krajnji_stup = krajnji_stup 
		self.trenutni = trenutni
		self.sekvenca = sekvenca
		self.client=BaxterArmClient()
		#self.startup = Startup()
	
	def parity(self):
		if (int(self.n) % 2) == 0:
			self.parno=1
		else:
			self.parno=0

	def sequence(self):
		#postoje dva moguce scenarija premjestanja kolutova, ovisno o kombinaciji pocetnih i odredisnih stupova
		if self.pocetni_stup == 'A' and self.krajnji_stup == 'B': self.sekvenca = 0
		elif self.pocetni_stup=='B' and self.krajnji_stup == 'C': self.sekvenca = 0
		elif self.pocetni_stup =='C' and self.krajnji_stup == 'A': self.sekvenca = 0
		else: self.sekvenca = 1 

 	def initialization(self):
		#ovisno o broju koluta odreduje se broj poteza. u vektor stanja s sprema se trenutno stanje, svi su koluti na 			stupu A. zeljeno krajnje stanje je da su svi koluti na C stupu i odigrani broj poteza je br_poteza= pow(2,int(n))-1
		self.s = []
		self.konacno = []		
		br_poteza= pow(2,int(self.n))-1 
		for i in range (0,3*int(self.n)):
			if self.pocetni_stup == 'A':			
				if i % 3 == 0:
					self.s.append(1)	
				else: self.s.append(0)
			if self.pocetni_stup == 'B':
				if (i+2) % 3 == 0: 
					self.s.append(1)
				else: self.s.append(0)
			if self.pocetni_stup == 'C':
				if (i+1) % 3 == 0:
					self.s.append(1)
				else: self.s.append(0)	
		
		for i in range (0,3*int(self.n)):
			if self.krajnji_stup== 'C':
				if (i+1) % 3 == 0:
					self.konacno.append(1)
				else: self.konacno.append(0)
			if self.krajnji_stup == 'B':
				if (i+2) % 3 == 0:
					self.konacno.append(1)
				else: self.konacno.append(0)
			if self.krajnji_stup == 'A':
				if i % 3 == 0:
					self.konacno.append(1)
				else: self.konacno.append(0)
		
		#na zadnjem mjestu niza cuva se broj odigranih poteza, na pocetku je 0 (vektor s), na kraju br_poteza(konacno)
		self.s.append(0)
		self.konacno.append(br_poteza)
		
		for i in range (0,int(self.n)):
			self.U.append(0)
	
	def get_height(self, position):
		#funkcija vraca broj koluta na zadanom stupu
		height = 0
		for i in range(0, int(self.n)): #za sve kolute provjetri jesu li na trenutnom
				if self.s[position+i*3]==1:
					height=height+1		
		return height
		
		
	def next(self): #ukoliko se premjestaju sa A na C, ili sa C na B, ili sa B - A
		#funkcija odreduje koji je kolut slijedeci na redu
		#ovisi o tome koliko je koluta ukupno u igri i o kojem se kolutu radi  
		
		if self.parno:
			if (self.kolut_br+1)%2==0:
				if self.trenutni==0: self.slijedeci=1   #sa A na B
				if self.trenutni==1: self.slijedeci=2   #sa B na c
				if self.trenutni==2: self.slijedeci=0   # sa C na A
			else:
				if self.trenutni==0: self.slijedeci=2	# sa A na c
				if self.trenutni==2: self.slijedeci=1	# sa C na B
				if self.trenutni==1: self.slijedeci=0	# sa B na A
				
		else:
			if (self.kolut_br+1)%2==0:
				if self.trenutni==0: self.slijedeci=2
				if self.trenutni==2: self.slijedeci=1
				if self.trenutni==1: self.slijedeci=0
				
			else:
				if self.trenutni==0: self.slijedeci=1
				if self.trenutni==1: self.slijedeci=2
				if self.trenutni==2: self.slijedeci=0
	
	def next_2(self): #ostala tri premjestanja 
		
		if self.parno:
			if (self.kolut_br+1)%2==0:
				if self.trenutni==0: self.slijedeci=2
				if self.trenutni==2: self.slijedeci=1
				if self.trenutni==1: self.slijedeci=0
				
			else:
				if self.trenutni==0: self.slijedeci=1
				if self.trenutni==1: self.slijedeci=2
				if self.trenutni==2: self.slijedeci=0
							
		else:
			if(self.kolut_br+1)%2==0:
				if self.trenutni==0: self.slijedeci=1   #sa A na B
				if self.trenutni==1: self.slijedeci=2   #sa B na c
				if self.trenutni==2: self.slijedeci=0   # sa C na A
			else:
				if self.trenutni==0: self.slijedeci=2	# sa A na c
				if self.trenutni==2: self.slijedeci=1	# sa C na B
				if self.trenutni==1: self.slijedeci=0	# sa B na A

	
	def logic(self, n, pocetni_stup, krajnji_stup, visina_A, visina_B, visina_C):
		self.pocetni_stup = pocetni_stup
		self.krajnji_stup = krajnji_stup
		self.n = n		
		self.initialization()
		self.parity()
		self.sequence()
		
		#print 's: ', self.s
		#print 'konacno: ',self.konacno
		print "potez br | kolut br | pocetni | konacni  | pick_height  | place_height"
	
		if self.pocetni_stup==self.krajnji_stup: zastavica=0
		else: zastavica=1
		
		if zastavica:		
			while (self.s!=self.konacno):
			#ovisno o tome koliko je do sada pokreta bilo, odreduje se koji je kolut na redu 
				for i in range(1,int(self.n)+1):
					if (self.s[3*int(self.n)]+1-pow(2,i-1)) % pow(2,i) == 0:		
						self.U[i-1]=1
						self.kolut_br=i
				#na redu je i-ti kolut, jos treba odrediti na kojem je trenutno stupu i na koji ga treba pomaknuti
				for i in range((self.kolut_br-1)*3,(self.kolut_br-1)*3+3):
					if self.s[i]==1: self.trenutni=i%3 #oznacava je li na prvom, drugom ili trecem stupu svoje sekvence
		
				if self.sekvenca:			
		
					self.next()
				else:
					self.next_2()
							
				pick_height = self.get_height(self.trenutni)
				place_height = self.get_height(self.slijedeci)

					
				if self.trenutni == 0: pick_height+=visina_A
				if self.trenutni == 1: 
					pick_height+=visina_B
					
				if self.trenutni == 2: pick_height+=visina_C

				if self.slijedeci == 0: place_height+=visina_A
				if self.slijedeci == 1: place_height+=visina_B
				if self.slijedeci == 2: place_height+=visina_C
	
				#broj do sada odigranih poteza 
				self.s[3*int(self.n)]=self.s[3*int(self.n)]+1
			# novo stanje, kolut_br je pomaknut s trenutnog na slijedeci 
				self.s[3*(self.kolut_br-1)+self.trenutni]=0
				self.s[(self.kolut_br-1)*3+self.slijedeci]=1
			
				print "   ", self.s[3*int(self.n)],"  |  ", self.kolut_br, "  |   ", self.trenutni, "   |  ",self.slijedeci,"  |  ", pick_height,"   |  ", place_height
			# 0-->A, 1-->B, 2-->C
				width= Utils().get_width(1) #kad budu prav koluti: Utils.get_width(self.kolut_br)
			
			#def start(self, pick_destination, pick_height, place_destination,place_height, width):
				self.client.start(self.trenutni,pick_height,self.slijedeci,place_height,width)

	
	def kalibracija_kolut(self):
		width= Utils().get_width(1)
		self.client.kalibracija_kolutovi(width)

	def kalibracija_stup(self):
		width= Utils().get_width(1)
		self.client.kalibracija_stupovi(width)	

	def run(self):
		
		print "potez br | kolut br | pocetni | konacni  | pick_height  | place_height"
		
		self.logic(n,pocetni_stup,krajnji_stup,visina_A,visina_B,visina_C)
		
if __name__=='__main__':
	rospy.init_node('petri_net_class',anonymous=True)
	try:
	        mreza = Petri_net()
		mreza.run()
	except rospy.ROSInterruptException:   
	        pass
	
