import math
import numpy

class RSLCheck:

	def calcAngleOff(self,a,b,dist,pos):
		#This function is used to calculate the angle between two vectors
		#x1,y1 refers to the position of the respective user(dist is the distance between the road and the station)
		#(pos is the position of the user on the road)
		#x2,y2 refers to a unit vector
		x1,y1=dist,pos
		x2,y2=a,b
		dotProd = x1*x2 + y1*y2
		mod1 = math.hypot(x1, y1)
		mod2 = math.hypot(x2, y2)
		return math.acos(dotProd/(mod1*mod2))

	def calcRSL(self,freq,hMob,hBase,pos,dist,totLength,powTx,gainTx,connLoss,x1,y1):
		numbers_float=[]
		with open('antenna_pattern.txt') as f:
			for line in f:
				numbers_float.append(map(float, line.split()))
		for x in numbers_float:
			if x[0]==round(self.calcAngleOff(x1,y1,dist,pos)):
				factor=x[1]
		RSL=powTx+gainTx-connLoss-factor-self.propagationLoss(freq,hMob,hBase,dist,pos)-self.rayFading()-self.shadowing(6000);
		return RSL
		#freq = frequency, hMob=height of Mobile, hBase=height of Base Station,
		#pos=position on road,dist=distance of road from station, totLength=Length of road.
		#Creating a dictionary of shadowing values based on position on the road

	def propagationLoss(self,freq,hMob,hBase,dist,pos):
		#Calculating HeightCorrectionFactor according Okumura Model
		heightCorr=0.8+((1.1*math.log10(freq)-0.7)*hMob)-1.56*math.log10(freq)
		d=((pos**2)+(dist**2))**0.5
		#Calculating the PathLoss according to the Okumura Model
		pathLoss=69.55+26.6*math.log10(freq)-13.82*math.log10(hBase)-heightCorr+(44.9-(6.55*math.log10(hBase)))*math.log10(d/1000)
		return pathLoss
	
	def rayFading(self):
		tempFade=numpy.random.rayleigh(1,10)
		return sorted(tempFade)[1];

	def shadowing(self,totLength):
		dictFading=[]
		for x in range(0,totLength,10):
			temp=numpy.random.normal(0, 2)
			dictFading.append(temp)
		return 0




