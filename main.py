from rsl import RSLCheck
import numpy
import random
import math
RSLMain=RSLCheck()

def determineCall(lamb,dt):
	if lamb*dt>random.random():
		return 1
	else:
		return 0

def returnDirection():
	#1 corresponds to North, 0 corresponds to South
	if random.random()>0.5:
		return 1
	else:
		return 0

def updateLocation(currLocation,direction,velocity):
	if direction==1:
		currLocation=currLocation+velocity*1
	else:
		currLocation=currLocation-velocity*1
	return currLocation

def checkLocation(loc):
	if loc>6000 or loc<0:
		return 1
	else:
		return 0


roadLength = 6000
dT=1
totTime=1
T=totTime*3600
hAntenna=150
loc=20
pTrans=43
loss=2
antennaGain=15
noChannelAlpha=15
noChannelBeta=15
fAlpha=860
fBeta=865
heightMob=1.5
handoffMargin=3
RSLThresh=-102
noUsers=160
callRate=(2.0/3600)
callDur=180
speed=15
callArchive=[0]*noUsers #Creating a dictionary of whether call is active for user X
callTime=[0]*noUsers #Creating a dictionary of time elapsed since call
carsDir=[]
callServiceSector=[0]*noUsers #1 if Alpha is Service Sector, 2 if Beta is Service Sector
#Creating a dictionary of whether call is active for user X

unitAlphaX=(3**0.5)/2
unitAlphaY=-0.5
unitBetaX=0
unitBetaY=1
noAvailableChannelAlpha=15
noAvailableChannelBeta=15
carsRoad=numpy.random.uniform(0,roadLength,160)
#Variables to keep count of no of blocked and dropped calls
noBlockedCallsAlpha=0
noDroppedCallsAlpha=0
noBlockedCallsBeta=0
noDroppedCallsBeta=0
#Variables to keep count of successfull Calls
successfulAlpha=0
successfulBeta=0
handoffAlpha=0
handoffBeta=0
#Variables to keep count of handoff Failures
handoffAttemptAlpha=0
handoffAttemptBeta=0
handoffFailAlphaInto=0
handoffFailBetaInto=0
handoffFailAlphaOutof=0
handoffFailBetaOutof=0

#Loop to generate 160 random values to decide which direction the car is going in. If val>0.5->North, val<0.5->South
for i in range(1,161):
	carsDir.append(returnDirection())

for time in range(0,1000):
	#Determining if the user makes a call request
	for cust in range(0,160):
		#Calculating RSL Value for both the sectors
		RSLAlpha=RSLMain.calcRSL(fAlpha,heightMob,hAntenna,carsRoad[cust],loc,roadLength,pTrans,antennaGain,loss,unitAlphaX,unitAlphaY)
		RSLBeta=RSLMain.calcRSL(fBeta,heightMob,hAntenna,carsRoad[cust],loc,roadLength,pTrans,antennaGain,loss,unitBetaX,unitBetaY)
		if callArchive[cust]==0:
			if determineCall(callRate,time):
				if RSLAlpha>RSLBeta:
					#Comparing RSL Values
					if RSLAlpha>=RSLThresh:
						if noAvailableChannelAlpha>0:
							noAvailableChannelAlpha=noAvailableChannelAlpha-1
							callArchive[cust]=1
							callServiceSector[cust]=1
							callTime[cust]=numpy.random.exponential(180)
							#SETUPCALL
						else:
							noBlockedCallsAlpha=noBlockedCallsAlpha+1
							if RSLBeta>RSLThresh:
								if noAvailableChannelBeta>0:
									noAvailableChannelBeta=noAvailableChannelBeta-1
									callArchive[cust]=1
									callServiceSector[cust]=2
									callTime[cust]=numpy.random.exponential(180)
									#SETUPCALL
					else:
						noDroppedCallsAlpha=noDroppedCallsAlpha+1
				else:
					if RSLBeta>=RSLThresh:
						if noAvailableChannelBeta>0:
							noAvailableChannelBeta=noAvailableChannelBeta-1
							callArchive[cust]=1
							callServiceSector[cust]=2
							callTime[cust]=numpy.random.exponential(180)
							#SETUPCALL
						else:
							noBlockedCallsBeta=noBlockedCallsBeta+1
							if RSLAlpha>RSLThresh:
								if noAvailableChannelAlpha>0:
									noAvailableChannelAlpha=noAvailableChannelAlpha-1
									callArchive[cust]=1
									callServiceSector[cust]=1
									callTime[cust]=numpy.random.exponential(180)
									#SETUPCALL
					else:
						noDroppedCallsBeta=noDroppedCallsBeta+1
						#RECORD CALL DROP
				#else:
					#print "hi"
					#
		elif callArchive[cust]==1:
			carsRoad[cust]=updateLocation(carsRoad[cust],carsDir[cust],speed)
			callTime[cust]=callTime[cust]-1
			if callTime[cust]<=0:
				if callServiceSector[cust]==1:
					successfulAlpha=successfulAlpha+1
					callArchive[cust]=0
					noAvailableChannelAlpha=noAvailableChannelAlpha+1
				else:
					successfulBeta=successfulBeta+1
					callArchive[cust]=0
					noAvailableChannelBeta=noAvailableChannelBeta+1
			elif checkLocation(carsRoad[cust]):
				if callServiceSector[cust]==1:
					handoffAlpha=handoffAlpha+1
					noAvailableChannelAlpha=noAvailableChannelAlpha+1
					carsRoad[cust]=numpy.random.uniform(0,roadLength)
					callArchive[cust]=0
					callServiceSector[cust]=0
					callTime[cust]=numpy.random.exponential(180)
					carsDir[cust]=returnDirection()
				else:
					handoffBeta=handoffBeta+1
					noAvailableChannelBeta=noAvailableChannelBeta+1
					carsRoad[cust]=numpy.random.uniform(0,roadLength)
					callArchive[cust]=0
					callServiceSector[cust]=0
					callTime[cust]=numpy.random.exponential(180)
					carsDir[cust]=returnDirection()
			else:
				if callServiceSector[cust]==1:
					RSLAlpha=RSLMain.calcRSL(fAlpha,heightMob,hAntenna,carsRoad[cust],loc,roadLength,pTrans,antennaGain,loss,unitAlphaX,unitAlphaY)
					print RSLAlpha
					if RSLAlpha<RSLThresh:
						noDroppedCallsAlpha=noDroppedCallsAlpha+1
						callArchive[cust]=0
						noAvailableChannelAlpha=noAvailableChannelAlpha+1
					elif RSLAlpha>RSLThresh:
						RSLBeta=RSLMain.calcRSL(fBeta,heightMob,hAntenna,carsRoad[cust],loc,roadLength,pTrans,antennaGain,loss,unitBetaX,unitBetaY)
						if RSLBeta>RSLAlpha+handoffMargin:
							handoffAttemptAlpha=handoffAttemptAlpha+1
							if noAvailableChannelBeta>0:
								callServiceSector[cust]=2
								successfulAlpha=successfulAlpha+1
								noAvailableChannelBeta=noAvailableChannelBeta-1
								noAvailableChannelAlpha=noAvailableChannelAlpha+1
							else:
								handoffFailAlphaOutof=handoffFailAlphaOutof+1
				else:
					RSLBeta=RSLMain.calcRSL(fBeta,heightMob,hAntenna,carsRoad[cust],loc,roadLength,pTrans,antennaGain,loss,unitBetaX,unitBetaY)
					if RSLBeta<RSLThresh:
						noDroppedCallsBeta=noDroppedCallsBeta+1
						callArchive[cust]=0
						noAvailableChannelBeta=noAvailableChannelBeta+1
					elif RSLBeta>RSLThresh:
						RSLAlpha=RSLMain.calcRSL(fAlpha,heightMob,hAntenna,carsRoad[cust],loc,roadLength,pTrans,antennaGain,loss,unitAlphaX,unitAlphaY)
						if RSLAlpha>RSLBeta+handoffMargin:
							handoffAttemptBeta=handoffAttemptBeta+1
							if noAvailableChannelAlpha>0:
								callServiceSector[cust]=2
								successfulBeta=successfulBeta+1
								noAvailableChannelAlpha=noAvailableChannelAlpha-1
								noAvailableChannelBeta=noAvailableChannelBeta+1
							else:
								handoffFailBetaOutof=handoffFailBetaOutof+1


print noBlockedCallsAlpha,noDroppedCallsAlpha,noBlockedCallsBeta, noDroppedCallsBeta, successfulAlpha, successfulBeta, handoffAlpha, handoffBeta, handoffAttemptAlpha, handoffAttemptBeta, handoffFailAlphaInto, handoffFailBetaInto, handoffFailAlphaOutof, handoffFailBetaOutof



			#UPDATE TIMER ADD TO PREVIOUS SECTIONstepB
			#STEP3





			#Chudap




