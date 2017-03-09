#!/usr/bin/env python

import rospy
import math
import numpy

from petri_net_class_v10 import Petri_net

class Petri_net_napredno:
	
	def __init__(self, s=[],n=None,pocetno=None, konacno = [], stanje = []):
		self.s = s
		self.n = n
		self.pocetno = pocetno
		self.konacno = konacno
		self.mreza = Petri_net()
		self.stanje = stanje
	
	def odredi_s(self, pocetno):
		#s je niz koji predstavlja inicijalno stanje
		if pocetno == 'A': 
			self.s.append(1)
			self.s.append(0)
			self.s.append(0)
		if pocetno == 'B':
			self.s.append(0)
			self.s.append(1)
			self.s.append(0)
		if pocetno == 'C':
			self.s.append(0)	
			self.s.append(0)
			self.s.append(1)

	def odredi_konacno(self, krajnji_stup):
		#petlja za odredivanje konacnog stanja, svi kolutovi morju biti na zadanom stupu 
		#STUP A : konacno = [1,0,0, 1,0,0, 1,0,0....]
		#STUP B : konacno = [0,1,0, 0,1,0, 0,1,0....]
		#STUP C : konacno = [0,0,1, 0,0,1, 0,0,1....]
		for i in range (0,3*int(self.n)):
			if krajnji_stup== 'C':
				if (i+1) % 3 == 0:
					self.konacno.append(1)
				else: self.konacno.append(0)
			if krajnji_stup == 'B':
				if (i+2) % 3 == 0:
					self.konacno.append(1)
				else: self.konacno.append(0)
			if krajnji_stup == 'A':
				if i % 3 == 0:
					self.konacno.append(1)
				else: self.konacno.append(0)
		
			
	def initialization(self):
		
		self.n = raw_input('unesite broj kolutova: ')
		for i in range(0,int(self.n)):
			print 'Pozicija koluta ', i+1, ': A/B/C --->' 
			temp = raw_input()
			self.stanje.append(temp)
			#stanje --> niz charova koji predstavlja stanja sustava
			self.odredi_s(temp)

		self.krajnji_stup= raw_input('unesite odredisni stup: ')
		
		#funkcija za odredivanje konacnog stanja
		self.odredi_konacno(self.krajnji_stup)

	def calibration(self):
		x = raw_input('Zelite li provesti kalibraciju stupova ? d/n ---> ')
		if x == 'd': 
			self.mreza.kalibracija_stup()
		
		x = raw_input('Zelite li provesti kalibraciju kolutova? d/n ---> ')
		if x == 'd':
			self.mreza.kalibracija_kolut()
		
		
	def logic(self):
		
		while (self.s!=self.konacno):
			for i in range(0,int(self.n)):
				visina_A = 0
				visina_B = 0
				visina_C = 0
				
				#izracunaj visinu na stupovima, onih kolutova koji se ne koriste u ovoj iteraciji 
				for j in range(i+1,int(self.n)):
					if self.stanje[j] == 'A': visina_A+=1 
					if self.stanje[j] == 'B': visina_B+=1
					if self.stanje[j] == 'C': visina_C+=1
				
				#ako se radi o zadnjem kolutu, destinacija je on koju je upisao korisnik
				#ako se radi o nekom od koluta prije, destinacija je stanje prvog veceg koluta	
				if i == int(self.n)-1: 
					destination = self.krajnji_stup
				else: 
					destination = self.stanje[i+1]
				
				#ako kolut nije na destinaciji, premjesti ga na zadanu destinaciju 
				if self.stanje[i]!=destination:
					self.mreza.logic(i+1, self.stanje[i], destination, visina_A, visina_B, visina_C) 
				
				#osvjezi vektor stanja, ako se radi o zadnjem kolutu onda je tamo gdje bi trebao biti
				#ako se radi o bilo kojem kolutu prije onda je tamo gdje je bio prvi veci 				
				if i == int(self.n)-1: 
					self.s[3*i]=self.konacno[3*i]
					self.s[3*i+1]=self.konacno[3*i+1]
					self.s[3*i+2]=self.konacno[3*i+2]
					#i ti i svi prije njega su gdje je i i+prvi kolut 
				for k in reversed(xrange(i)):
					self.s[3*k]=self.s[3*(k+1)]
					self.s[3*k+1]=self.s[3*(k+1)+1]
					self.s[3*k+2]=self.s[3*(k+1)+2]

				self.stanje[i]=destination
			
	def start(self):
		self.initialization()
		self.calibration()
		self.logic()	


if __name__=='__main__':
	rospy.init_node('petri_net_pocetno_stanje',anonymous=True)
	try:
	        mreza_nova = Petri_net_napredno()
		mreza_nova.start()
	except rospy.ROSInterruptException:   
	        pass	
			
			
		
			
