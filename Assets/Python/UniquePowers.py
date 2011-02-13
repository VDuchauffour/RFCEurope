# Rhye's and Fall of Civilization - (a part of) Unique Powers


#Emperor is in RiseAndFall in the collapse and scession functions, RFCUtils.collapseImmune and stability
#Khan is in c++ CvPlayer.cpp::acquireCity()


from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
import cPickle as pickle
import Consts as con
import XMLConsts as xml
import RFCUtils
utils = RFCUtils.RFCUtils()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer


### Constants ###

iByzantium = con.iByzantium
iBulgaria = con.iBulgaria
iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iNumActivePlayers = con.iNumActivePlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iBarbarian = con.iBarbarian
iNumTotalPlayers = con.iNumTotalPlayers

# initialise player variables
# 3Miro: set dummy values
#iEgypt = 100
#iIndia = 100
#iChina = 100
#iBabylonia = 100
#iGreece = 100
#iPersia = 100
#iCarthage = 100
#iRome = 100
#iJapan = 100
#iVikings = 100
#iArabia = 100
#iSpain = 100
#iFrance = 100
#iEngland = 100
#iGermany = 100
#iRussia = 100
#iMali = 100
#iTurkey = 100
#iInca = 100
#iMongolia = 100
#iAztecs = 100
#iAmerica = 100

#iHolland = con.iHolland
#iPortugal = con.iPortugal

iNative = 100
iCeltia = 100


# 3Miro set more dummy values, and never reference them
#pMongolia = gc.getPlayer(iMongolia)
#teamMongolia = gc.getTeam(pMongolia.getTeam())
pMongolia = 100
teamMongolia = 100

tRussianTopLeft = (10, 20)
tRussianBottomRight = (20, 10)


iNumReligions = 0


#Buildings



iMongolianRadius = 4
iMongolianTimer = 1


# 3Miro: I will put this somewhere else, it makes no sense to have a separate module for only one UP

class UniquePowers:
       	
        def checkTurn(self, iGameTurn):
                pass
                
#------------------U.P. FAITH-------------------
        def faithUP(self, iPlayer, city):
                pFaithful = gc.getPlayer(iPlayer)
                iStateReligion = pFaithful.getStateReligion()
                iTemple = 0
                if (iStateReligion >= 0):
                	if (not city.isHasReligion(iStateReligion)):
	                        city.setHasReligion(iStateReligion, True, True, False)
	                        pFaithful.changeFaith( 1 )
			if (iStateReligion == 0):
			        iTemple = xml.iProtestantTemple
			if (iStateReligion == 1):
			        iTemple = xml.iIslamicTemple
			if (iStateReligion == 2):
		                iTemple = xml.iCatholicTemple
			if (iStateReligion == 3):
			        iTemple = xml.iOrthodoxTemple
                        if (not city.hasBuilding(iTemple)):
                                city.setHasRealBuilding(iTemple, True)
                                pFaithful.changeFaith( 1 )
                        
