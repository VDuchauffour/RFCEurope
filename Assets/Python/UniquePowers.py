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

iJanissaryPoints = con.iJanissaryPoints

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
                        
                        
#------------------U.P. Janissary-------------------
        def janissary(self, iPlayer ):
                pPlayer = gc.getPlayer( iPlayer )
                iStateReligion = pPlayer.getStateReligion()
                
                apCityList = PyPlayer(iPlayer).getCityList()
                iNewPoints = 0
                for apCity in apCityList:
                        pCity = apCity.GetCy()
                        for iReligion in range( xml.iNumReligions ):
                                if ( iReligion != iStateReligion and pCity.isHasReligion( iReligion ) ):
                                        iNewPoints += pCity.getPopulation()
                                        break
                                        
                pPlayer.setPicklefreeParameter( iJanissaryPoints, pPlayer.getPicklefreeParameter( iJanissaryPoints ) + iNewPoints )
                print(" 3Miro Janissaries: ",pPlayer.getPicklefreeParameter( iJanissaryPoints ) )
                

