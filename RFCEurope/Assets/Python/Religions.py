# Rhye's and Fall of Civilization - Religions management

from CvPythonExtensions import *
import CvUtil
import PyHelpers       
import Popup
import cPickle as pickle        	
import Consts as con
import RFCUtils

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()

### Constants ###

iNumPlayers = con.iNumPlayers
iBarbarian = con.iBarbarian
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2


# initialise religion variables to religion indices from XML

# initialise coordinates

tToledo = (27,31)
tAugsburg = (56,41)
tSpainTL = (20,24)
tSpainBR = (35,40)
tMainzTL = (47,38)
tMainzBR = (56,55)
tPolandTL = (64,43)
tPolandBR = (78,57)


class Religions:

##################################################
### Secure storage & retrieval of script data ###
################################################
		
        def getSeed( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iSeed']

        def setSeed( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['iSeed'] = gc.getGame().getSorenRandNum(100, 'Seed for random delay')
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )        


#######################################
### Main methods (Event-Triggered) ###
#####################################  

        def setup(self):
                self.setSeed()
                
       	
        def checkTurn(self, iGameTurn):
		# Sedna17: Spreading Judaism in a somewhat deterministic way
		if (iGameTurn == con.i700AD-2):
			#Spread Judaism to Toledo
			utils.spreadJews(tToledo,con.iJudaism)
		if (iGameTurn == con.i900AD):
			#Spread Judaism to another town or two in Spain
			tCity = self.selectRandomCityArea(tSpainTL,tSpainBR)
			utils.spreadJews(tCity,con.iJudaism)
		if (iGameTurn == con.i1000AD):
			#Spread Judaism to a city in France/Germany
			tCity = self.selectRandomCityArea(tMainzTL,tMainzBR)
			utils.spreadJews(tCity,con.iJudaism)
		if (iGameTurn == con.i1500AD):
			#Spread Judaism to a couple towns in Poland
			tCity = self.selectRandomCityArea(tPolandTL,tPolandBR)
			utils.spreadJews(tCity,con.iJudaism)
			tCity = self.selectRandomCityArea(tPolandTL,tPolandBR)
			utils.spreadJews(tCity,con.iJudaism)
               	
               	#for i in range( iNumPlayers - 1 ): # the Pope cannot gift to himself
        		#pPlayer = gc.getPlayer( i )
        		#print( " Player ",i,"  Faith: ",pPlayer.getFaith() )
               	
               	# Prosecution
               	for i in range( con.iNumPlayers ):
               		pPlayer = gc.getPlayer( i )
               		if ( pPlayer.getProsecutionCount() > 0 ):
               			pPlayer.changeProsecutionCount( -1 )
               	
               	# 3Miro: Catholic Benefits from the Pope
               	# the Pope gifts gold every 3 turns
               	if ( iGameTurn > con.i1053AD ):
               		iDivBy = 7
               	else:
               		iDivBy = 17
               	if ( iGameTurn % iDivBy == 3 ):
               		pPope = gc.getPlayer( con.iPope )
               		teamPope = gc.getTeam( pPope.getTeam() )
               		if ( pPope.getGold() > 100 ):
	               		iCatholicFaith = 0
        	       		for i in range( iNumPlayers - 1 ): # the Pope cannot gift to himself
        	       			pPlayer = gc.getPlayer( i )
        	       			if ( pPlayer.getStateReligion() == con.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
        	       				iCatholicFaith += pPlayer.getFaith()
        	       		if ( iCatholicFaith > 0 ):
        	       			iCatholicFaith += iCatholicFaith / 10 + 1
        	       			if ( iGameTurn < 100 ):
        	       				iGift = 20
        	       			else:
        	       				iGift = 50
	        	       		iRandomNum = gc.getGame().getSorenRandNum(iCatholicFaith, 'random Pope gold gift')
        		       		for i in range( iNumPlayers - 1 ):
        		       			pPlayer = gc.getPlayer( i )
        		       			if ( pPlayer.getStateReligion() == con.iCatholicism  and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
			               			iRandomNum -= pPlayer.getFaith()
			               			if ( iRandomNum <= 0 ):
			               				#print(" The Pope gifts 50 gold to ",i )
			               				pPope.changeGold( -iGift )
			               				pPlayer.changeGold( iGift )
			               				if ( utils.getHumanID() == i ):
			               					sText = CyTranslator().getText("TXT_KEY_FAITH_GIFT", ())
			               					CyInterface().addMessage(i, True, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)
		               					break

		# free religious building every 6 turns
		if ( iGameTurn > 66 ): # 66 = 800AD, the crouning of Charlemagne
			if ( iGameTurn % 11 == 3 ):
				#print(" 3Miro Pope Builds " )
				pPope = gc.getPlayer( con.iPope )
				teamPope = gc.getTeam( pPope.getTeam() )
				iCatholicFaith = 0
        		        for i in range( iNumPlayers - 1 ): # the Pope cannot gift to himself
        		       		pPlayer = gc.getPlayer( i )
        		       		if ( pPlayer.getStateReligion() == con.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
        		       			#iCatholicFaith += pPlayer.getFaith() + pPope.AI_getAttitude( i )
        		       			iCatholicFaith += max( 0, pPope.AI_getAttitude( i ) )
        		       	#print(" Catholic Faith: ",iCatholicFaith)
        		       	if ( iCatholicFaith > 0 ):
        		       		iCatholicFaith += iCatholicFaith / 5 + 1
        		       		if ( gc.getGame().getSorenRandNum(2, 'random Catholic BuildingType') % 2 == 0 ):
        		       			iCatholicBuilding = con.iCatholicTemple
        		       		else:
        		       			iCatholicBuilding = con.iCatholicMonastery
        			       	iRandomNum = gc.getGame().getSorenRandNum(iCatholicFaith, 'random Pope Building Build')
        		       		#print(" 3Miro Pope Builds " )
        		       		for i in range( iNumPlayers - 1 ):
        			       		pPlayer = gc.getPlayer( i )
        			       		if ( pPlayer.getStateReligion() == con.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
				        		#iRandomNum -= pPlayer.getFaith() + pPope.AI_getAttitude( i )
				        		iRandomNum -= max( 0, pPope.AI_getAttitude( i ) )
				               		if ( iRandomNum <= 0 ):
				               			#print(" The Pope Builds ",iCatholicBuilding," for ",i )
				               			self.buildInRandomCity( i, iCatholicBuilding, con.iCatholicism )
			               				break		       	

        def foundReligion(self, tPlot, iReligion):
                if (tPlot != False):
                        plot = gc.getMap().plot( tPlot[0], tPlot[1] )                
                        if (not plot.getPlotCity().isNone()):
                                #if (gc.getPlayer(city.getOwner()).isHuman() == 0):
                                #if (not gc.getGame().isReligionFounded(iReligion)):
                                gc.getGame().setHolyCity(iReligion, plot.getPlotCity(), True)
                                return True
                        else:
                                return False
                            
                return False

	def onReligionSpread(self, iReligion, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		if ( pPlayer.getStateReligion() == iReligion ):
			pPlayer.changeFaith( 1 )
		else:
			pPlayer.changeFaith( -1 )
		
	def onBuildingBuild(seld, iPlayer, iBuilding ):
		pPlayer = gc.getPlayer( iPlayer )
		iStateReligion = pPlayer.getStateReligion()
		if ( iStateReligion == con.iCatholicism and ( iBuilding == con.iCatholicTemple or iBuilding == con.iCatholicMonastery or iBuilding == con.iCatholicCathedral ) ):
			pPlayer.changeFaith( 1 )
		if ( iStateReligion == con.iOrthodoxy and ( iBuilding == con.iOrthodoxTemple or iBuilding == con.iOrthodoxMonastery or iBuilding == con.iOrthodoxCathedral ) ):
			pPlayer.changeFaith( 1 )
		if ( iStateReligion == con.iIslam and ( iBuilding == con.iIslamicTemple or iBuilding == con.iIslamicCathedral or iBuilding == con.iIslamicMadrassa ) ):
			pPlayer.changeFaith( 1 )
		if ( iStateReligion == con.iProtestantism and ( iBuilding == con.iProtestantTemple or iBuilding == con.iProtestantCathedral or iBuilding == con.iProtestantSchool ) ):
			pPlayer.changeFaith( 1 )

        def selectRandomCityCiv(self, iCiv):
                if (gc.getPlayer(iCiv).isAlive()):
                        cityList = []
                        for pyCity in PyPlayer(iCiv).getCityList():
                                cityList.append(pyCity.GetCy())
                        iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                        city = cityList[iCity]
                        return (city.getX(), city.getY())
                return False
            

        def selectRandomCityArea(self, tTopLeft, tBottomRight):
                cityList = []
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
                                pCurrent = gc.getMap().plot( x, y )
                                if ( pCurrent.isCity()):
                                        cityList.append(pCurrent.getPlotCity())
                if (cityList):
                        iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                        city = cityList[iCity]
                        return (city.getX(), city.getY())
                else:
                        return False


        def selectRandomCityAreaCiv(self, tTopLeft, tBottomRight, iCiv):
                cityList = []
                for x in range(tTopLeft[0], tBottomRight[0]+1):
                        for y in range(tTopLeft[1], tBottomRight[1]+1):
                                pCurrent = gc.getMap().plot( x, y )
                                if ( pCurrent.isCity()):
                                        if (pCurrent.getPlotCity().getOwner() == iCiv):
                                                cityList.append(pCurrent.getPlotCity())
                if (cityList):
                        iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                        city = cityList[iCity]
                        return (city.getX(), city.getY())
                else:
                        return False



        def selectRandomCityReligion(self, iReligion):
                if (gc.getGame().isReligionFounded(iReligion)):
                        cityList = []
                        for iPlayer in range(iNumPlayers):
                                for pyCity in PyPlayer(iPlayer).getCityList():
                                        if pyCity.GetCy().isHasReligion(iReligion):
                                                cityList.append(pyCity.GetCy())                                        
                        iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                        city = cityList[iCity]
                        return (city.getX(), city.getY())
                return False


        def selectRandomCityReligionCiv(self, iReligion, iCiv):
                if (gc.getGame().isReligionFounded(iReligion)):
                        cityList = []
                        for iPlayer in range(iNumPlayers):
                                for pyCity in PyPlayer(iPlayer).getCityList():
                                        if pyCity.GetCy().isHasReligion(iReligion):
                                                if (pyCity.GetCy().getOwner() == iCiv):                            
                                                        cityList.append(pyCity.GetCy())
                        if (cityList):
                                iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                                city = cityList[iCity]
                                return (city.getX(), city.getY())
                return False


        def spreadReligion(self, tCoords, iNum, iMissionary):
                city = gc.getMap().plot( tCoords[0], tCoords[1] ).getPlotCity()
                #print city
                #print city.getOwner()
                utils.makeUnit(iMissionary, city.getOwner(), tCoords, iNum)

	def buildInRandomCity( self, iPlayer, iBuilding, iReligion ):
		#print(" Building ",iBuilding," for ",iPlayer )
		cityList = []
		for pyCity in PyPlayer(iPlayer).getCityList():
			if ( (not pyCity.GetCy().hasBuilding(iBuilding)) and pyCity.GetCy().isHasReligion( iReligion )  ):
				cityList.append(pyCity.GetCy())
		if ( len(cityList) > 0 ):
			iRandCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
			city = cityList[iRandCity]
			city.setHasRealBuilding(iBuilding, True)
			gc.getPlayer( iPlayer ).changeFaith( 1 )
			if ( utils.getHumanID() == iPlayer ):
				#sText = CyTranslator().getText("TXT_KEY_FAITH_GIFT", ())
				sText = CyTranslator().getText("TXT_KEY_FAITH_BUILDING1", ()) +" " + gc.getBuildingInfo( iBuilding ).getDescription() + " " + CyTranslator().getText("TXT_KEY_FAITH_BUILDING2", ()) + " " + city.getName()
				CyInterface().addMessage(iPlayer, True, con.iDuration/2, sText, "", 0, "", ColorTypes(con.iOrange), -1, -1, True, True)

