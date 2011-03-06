# Rhye's and Fall of Civilization - Religions management

from CvPythonExtensions import *
import CvUtil
import PyHelpers       
import Popup
import cPickle as pickle        	
import Consts as con
import XMLConsts as xml
import RFCUtils
import RFCEMaps as rfcemaps

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()

### Constants ###

iNumPlayers = con.iNumPlayers
iNumTotalPlayers = con.iNumTotalPlayers
iBarbarian = con.iBarbarian
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2

# initialise religion variables to religion indices from XML

# initialise coordinates

tToledo = (28,32)
tAugsburg = (56,41)
tSpainTL = (20,24)
tSpainBR = (35,40)
tMainzTL = (47,38)
tMainzBR = (56,55)
tPolandTL = (64,43)
tPolandBR = (78,57)

### Religious Buildings that give Faith Points ###
tCatholicBuildings = [ xml.iCatholicTemple, xml.iCatholicMonastery, xml.iCatholicCathedral ]
tOrthodoxBuildings = [ xml.iOrthodoxTemple, xml.iOrthodoxMonastery, xml.iOrthodoxCathedral ]
tProtestantBuildings = [ xml.iProtestantTemple, xml.iProtestantSchool, xml.iProtestantCathedral ]
tIslamicBuildings = [ xml.iIslamicTemple, xml.iIslamicCathedral, xml.iIslamicMadrassa ]
tReligiousWonders = [ xml.iMonasteryOfCluny, xml.iImperialDiet, xml.iKrakDesChevaliers, xml.iNotreDame, xml.iPalaisPapes, xml.iStBasil, xml.iSophiaKiev, xml.iDomeRock, xml.iRoundChurch, xml.iWestminster ]


### Reformation Begin ###       
#Matrix determines how likely the AI is to switch to Protestantism                                                               
lReformationMatrix = [
10, #Byzantium
40, #France
10, #Arabia
30, #Bulgaria
10, #Cordoba
80, #Norse
30, #Venecia
50, #Burgundy
90, #Germany
20, #Kiev
50, #Hungary
10, #Spain
30, #Poland
30, #Genoa
80, #England
30, #Portugal
30, #Lithuania
50, #Austria
10, #Turkey
10, #Moscow
90, #Sweden
90, #Dutch
0,  #Rome
0,  #Indies and Barbs
0,
0,
0,
0
] 

#Reformation neighbours spread reformation choice to each other
lReformationNeighbours = [
[con.iArabia,con.iBulgaria,con.iTurkey], #Byzantium
[con.iBurgundy,con.iSpain,con.iGermany,con.iGenoa,con.iEngland,con.iDutch], #Frankia
[con.iByzantium,con.iCordoba,con.iTurkey], 		#Arabia
[con.iByzantium,con.iKiev,con.iHungary,con.iTurkey], #Bulgaria
[con.iArabia,con.iSpain,con.iPortugal], 	#Cordoba
[con.iGermany,con.iSweden],  		#Norse
[con.iGenoa,con.iGermany,con.iAustria,con.iHungary,con.iPope],  #Venecia
[con.iFrankia,con.iGermany,con.iGenoa,con.iDutch], #Burgundy
[con.iBurgundy,con.iFrankia,con.iNorse,con.iVenecia,con.iHungary,con.iPoland,con.iGenoa,con.iAustria,con.iDutch],  #Germany
[con.iBulgaria,con.iHungary,con.iPoland,con.iMoscow,con.iLithuania],  		#Kiev
[con.iBulgaria,con.iVenecia,con.iKiev,con.iGermany,con.iPoland,con.iAustria,con.iTurkey],  #Hungary
[con.iFrankia,con.iCordoba,con.iPortugal], 	#Spain
[con.iKiev,con.iHungary,con.iGermany,con.iMoscow,con.iAustria,con.iLithuania],  			#Poland
[con.iBurgundy,con.iFrankia,con.iVenecia,con.iGermany,con.iPope],  #Genoa
[con.iFrankia,con.iDutch],  		#England
[con.iSpain,con.iCordoba],  		#Portugal
[con.iKiev,con.iMoscow,con.iAustria,con.iPoland],  	#Lithuania
[con.iVenecia,con.iHungary,con.iGermany,con.iPoland],  	#Austria
[con.iByzantium,con.iArabia,con.iBulgaria,con.iHungary],  	#Turkey
[con.iKiev,con.iPoland,con.iSweden,con.iLithuania],  		#Moscow
[con.iNorse,con.iMoscow],  				#Sweden
[con.iBurgundy,con.iFrankia,con.iGermany,con.iEngland],   	#Dutch
[con.iVenecia,con.iGenoa]			#Pope
]
### Reformation End ###    


### Regions to spread religion ###
tProvinceMap = rfcemaps.tProinceMap
tSpain = [xml.iP_Leon,xml.iP_GaliciaSpain,xml.iP_Aragon,xml.iP_Catalonia,xml.iP_Castile,xml.iP_Andalusia,xml.iP_Valencia]
tPoland = [xml.iP_GreaterPoland,xml.iP_LesserPoland,xml.iP_Masovia,xml.iP_Silesia,xml.iP_Suvalkija,xml.iP_Brest,xml.iP_Pomerania]
tGermany = [xml.iP_Lorraine,xml.iP_Franconia,xml.iP_Bavaria,xml.iP_Swabia]
tWestAfrica = [xml.iP_Tetouan,xml.iP_Morocco,xml.iP_Marrakesh,xml.iP_Oran]
tNorthAfrica = [xml.iP_Algiers,xml.iP_Ifriqiya,xml.iP_Tripolitania,xml.iP_Cyrenaica]
tBalkansAndAnatolia = [xml.iP_Constantinople,xml.iP_Thrace,xml.iP_Opsikion,xml.iP_Paphlagonia,xml.iP_Thrakesion,xml.iP_Cilicia,xml.iP_Anatolikon,xml.iP_Armeniakon,xml.iP_Charsiadon]

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

        def getReformationActive( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['bReformationActive']

        def setReformationActive( self, bNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['bReformationActive'] = bNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )  

        def getReformationHitMatrix( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lReformationHitMatrix'][iCiv]

        def setReformationHitMatrix( self, iCiv, bNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lReformationHitMatrix'][iCiv] = bNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )                

        def getReformationHitMatrixAll( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lReformationHitMatrix']

        def getCounterReformationActive( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['bCounterReformationActive']

        def setCounterReformationActive( self, bNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['bCounterReformationActive'] = bNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )  


#######################################
### Main methods (Event-Triggered) ###
#####################################  

        def setup(self):
                gc.getPlayer(con.iTurkey).changeFaith( 20 )
                self.setSeed()
       	
        def checkTurn(self, iGameTurn):
		# Sedna17: Spreading Judaism in a somewhat deterministic way
		if (iGameTurn == xml.i700AD-2):
			#Spread Judaism to Toledo
			#utils.spreadJews(tToledo,xml.iJudaism)
                        self.spreadReligion(tToledo,xml.iJudaism)
                        tCity = self.selectRandomCityArea(tNorthAfrica)
                        self.spreadReligion(tCity,xml.iIslam)
			#utils.spreadJews(tCity,xml.iIslam)
                        tCity = self.selectRandomCityArea(tNorthAfrica)
			self.spreadReligion(tCity,xml.iIslam)
                        #utils.spreadJews(tCity,xml.iIslam)
                if (iGameTurn == xml.i700AD+2):
			#Spread Judaism to Toledo
			tCity = self.selectRandomCityArea(tWestAfrica)
			self.spreadReligion(tCity,xml.iIslam)
                        #utils.spreadJews(tCity,xml.iIslam)
                        tCity = self.selectRandomCityArea(tWestAfrica)
                        self.spreadReligion(tCity,xml.iJudaism)
			#utils.spreadJews(tCity,xml.iJudaism)

		if (iGameTurn == xml.i900AD):
			#Spread Judaism to another town or two in Spain
			tCity = self.selectRandomCityArea(tSpain)
                        self.spreadReligion(tCity,xml.iJudaism)
			#utils.spreadJews(tCity,xml.iJudaism)
		if (iGameTurn == xml.i1000AD):
			#Spread Judaism to a city in France/Germany
			tCity = self.selectRandomCityArea(tGermany)
                        self.spreadReligion(tCity,xml.iJudaism)
			#utils.spreadJews(tCity,xml.iJudaism)
                        tCity = self.selectRandomCityArea(tNorthAfrica)
                        self.spreadReligion(tCity,xml.iIslam)
			#utils.spreadJews(tCity,xml.iIslam)
		if (iGameTurn == xml.i1101AD):
			#Spread Judaism to a couple towns in Poland
			tCity = self.selectRandomCityArea(tPoland)
                        self.spreadReligion(tToledo,xml.iJudaism)
			#self.spreadReligion(tToledo,xml.iJudaism)utils.spreadJews(tCity,xml.iJudaism)
		if (iGameTurn == xml.i1200AD):
			tCity = self.selectRandomCityArea(tPoland)
                        self.spreadReligion(tCity,xml.iJudaism)
			#utils.spreadJews(tCity,xml.iJudaism)
                if (iGameTurn > xml.i1299AD and iGameTurn < xml.i1359AD and iGameTurn % 3 == 0):
                        tCity = self.selectRandomCityArea(tBalkansAndAnatolia)
                        self.spreadReligion(tCity,xml.iIslam)
                        
		if (iGameTurn == xml.i1401AD):
			tCity = self.selectRandomCityArea(tPoland)
                        self.spreadReligion(tCity,xml.iJudaism)
			#utils.spreadJews(tCity,xml.iJudaism)
                        
                if (iGameTurn == xml.i1580AD and (not gc.getGame().isReligionFounded(xml.iProtestantism) ) ):
                        # if Protestantism has not been founded by the time the Dutch spawn, then the Dutch should found it
                        gc.getPlayer(con.iDutch).foundReligion(xml.iProtestantism,xml.iProtestantism,false)
                        gc.getGame().getHolyCity(xml.iProtestantism).setNumRealBuilding(xml.iProtestantShrine,1)
                        self.setReformationActive(True)
                        self.reformationchoice(con.iDutch)
                        self.reformationOther(con.iIndependent)
                        self.reformationOther(con.iIndependent2)
                        self.reformationOther(con.iIndependent3)
                        self.reformationOther(con.iIndependent4)
                        self.reformationOther(con.iBarbarian)
                        self.setReformationHitMatrix(con.iDutch,2)
                        for iCiv in range(iNumPlayers):
                                if ((iCiv in lReformationNeighbours[con.iDutch]) and self.getReformationHitMatrix(iCiv) == 0):
                                        self.setReformationHitMatrix(iCiv,1)
		
               	
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
               	if ( iGameTurn > xml.i1053AD ):
               		iDivBy = 7
               	else:
               		iDivBy = 17
               	if ( iGameTurn >= xml.i752AD and iGameTurn % iDivBy == 3 ):
               		pPope = gc.getPlayer( con.iPope )
               		teamPope = gc.getTeam( pPope.getTeam() )
               		if ( pPope.getGold() > 100 ):
	               		iCatholicFaith = 0
        	       		for i in range( iNumPlayers - 1 ): # the Pope cannot gift to himself
        	       			pPlayer = gc.getPlayer( i )
        	       			if ( pPlayer.getStateReligion() == xml.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
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
        		       			if ( pPlayer.getStateReligion() == xml.iCatholicism  and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
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
		if ( iGameTurn > xml.i800AD ): # 66 = 800AD, the crouning of Charlemagne
			if ( iGameTurn % 11 == 3 ):
				#print(" 3Miro Pope Builds " )
				pPope = gc.getPlayer( con.iPope )
				teamPope = gc.getTeam( pPope.getTeam() )
				iCatholicFaith = 0
        		        for i in range( iNumPlayers - 1 ): # the Pope cannot gift to himself
        		       		pPlayer = gc.getPlayer( i )
        		       		if ( pPlayer.getStateReligion() == xml.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
        		       			#iCatholicFaith += pPlayer.getFaith() + pPope.AI_getAttitude( i )
        		       			iCatholicFaith += max( 0, pPope.AI_getAttitude( i ) )
        		       	#print(" Catholic Faith: ",iCatholicFaith)
        		       	if ( iCatholicFaith > 0 ):
        		       		iCatholicFaith += iCatholicFaith / 5 + 1
        		       		if ( gc.getGame().getSorenRandNum(2, 'random Catholic BuildingType') % 2 == 0 ):
        		       			iCatholicBuilding = xml.iCatholicTemple
        		       		else:
        		       			iCatholicBuilding = xml.iCatholicMonastery
        			       	iRandomNum = gc.getGame().getSorenRandNum(iCatholicFaith, 'random Pope Building Build')
        		       		#print(" 3Miro Pope Builds " )
        		       		for i in range( iNumPlayers - 1 ):
        			       		pPlayer = gc.getPlayer( i )
        			       		if ( pPlayer.getStateReligion() == xml.iCatholicism and teamPope.isOpenBorders( pPlayer.getTeam() ) ):
				        		#iRandomNum -= pPlayer.getFaith() + pPope.AI_getAttitude( i )
				        		iRandomNum -= max( 0, pPope.AI_getAttitude( i ) )
				               		if ( iRandomNum <= 0 ):
				               			#print(" The Pope Builds ",iCatholicBuilding," for ",i )
				               			self.buildInRandomCity( i, iCatholicBuilding, xml.iCatholicism )
			               				break
        ##Reformation code
                if ( self.getCounterReformationActive() ):
                        self.doCounterReformation()
		if (self.getReformationActive() ):
			#print( " Reformation #1 " )
			self.reformationArrayChoice()
			if (self.getReformationActive() ):
				#print( " Reformation #2 " )
				self.reformationArrayChoice()
				if (self.getReformationActive() ):
					#print( " Reformation #3 " )
					self.reformationArrayChoice()
                

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
		if ( iStateReligion == xml.iCatholicism and ( iBuilding in tCatholicBuildings ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iCatholicCathedral ):
				pPlayer.changeFaith( 3 )
		if ( iStateReligion == xml.iOrthodoxy and ( iBuilding in tOrthodoxBuildings ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iOrthodoxCathedral ):
				pPlayer.changeFaith( 3 )
		if ( iStateReligion == xml.iIslam and ( iBuilding in tIslamicBuildings  ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iIslamicCathedral ):
				pPlayer.changeFaith( 3 )
		if ( iStateReligion == xml.iProtestantism and ( iBuilding in tProtestantBuildings ) ):
			pPlayer.changeFaith( 1 )
			if ( iBuilding == xml.iProtestantCathedral ):
				pPlayer.changeFaith( 3 )
		if ( iBuilding in tReligiousWonders ):
			pPlayer.changeFaith( 6 )
		if ( iStateReligion != xml.iJudaism and iBuilding == xml.iTempleMount ):
			pPlayer.changeFaith( - min( 1, pPlayer.getFaith() ) )

        def selectRandomCityCiv(self, iCiv):
                if (gc.getPlayer(iCiv).isAlive()):
                        cityList = []
                        for pyCity in PyPlayer(iCiv).getCityList():
                                cityList.append(pyCity.GetCy())
                        iCity = gc.getGame().getSorenRandNum(len(cityList), 'random city')
                        city = cityList[iCity]
                        return (city.getX(), city.getY())
                return False
            

        def selectRandomCityArea(self, tProvinces):
                cityList = []
                for x in range( con.iMapMaxX ):
                        for y in range( con.iMapMaxY ):
                                if ( tProvinceMap[y][x] in tProvinces ):
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


        #def spreadReligion(self, tCoords, iNum, iMissionary):
        #        city = gc.getMap().plot( tCoords[0], tCoords[1] ).getPlotCity()
        #        utils.makeUnit(iMissionary, city.getOwner(), tCoords, iNum)
        
        def spreadReligion(self, tPlot, iReligion ):
                pPlot = gc.getMap().plot( tPlot[0], tPlot[1] )                
                if ( pPlot.isCity() ):
                        pPlot.getPlotCity().setHasReligion(iReligion,1,0,0) #Puts Judaism or another religion into this city


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

##REFORMATION

        def showPopup(self, popupID, title, message, labels):
                popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
                popup.setHeaderString(title)
                popup.setBodyString(message)
                for i in labels:
                    popup.addButton( i )
                popup.launch(False)

        def reformationPopup(self):
                self.showPopup(7624, CyTranslator().getText("TXT_KEY_REFORMATION_TITLE", ()), CyTranslator().getText("TXT_KEY_REFORMATION_MESSAGE",()), (CyTranslator().getText("TXT_KEY_POPUP_YES", ()), CyTranslator().getText("TXT_KEY_POPUP_NO", ())))

        def eventApply7624(self, popupReturn):
                iHuman = utils.getHumanID()
                if(popupReturn.getButtonClicked() == 0):
                        self.reformationyes(iHuman)
                elif(popupReturn.getButtonClicked() == 1):
                        self.reformationno(iHuman)

        def onTechAcquired(self, iTech, iPlayer):
                if (iTech == xml.iPrintingPress):
                        if (gc.getPlayer(iPlayer).getStateReligion() == xml.iCatholicism):
                                if (not gc.getGame().isReligionFounded(xml.iProtestantism)):
                                        gc.getPlayer(iPlayer).foundReligion(xml.iProtestantism,xml.iProtestantism,false)
                                        gc.getGame().getHolyCity(xml.iProtestantism).setNumRealBuilding(xml.iProtestantShrine,1)
                                        self.setReformationActive(True)
                                        self.reformationchoice(iPlayer)
                                        self.reformationOther(con.iIndependent)
                                        self.reformationOther(con.iIndependent2)
                                        self.reformationOther(con.iIndependent3)
                                        self.reformationOther(con.iIndependent4)
                                        self.reformationOther(con.iBarbarian)
                                        self.setReformationHitMatrix(iPlayer,2)
                                        for iCiv in range(iNumPlayers):
                                                if ((iCiv in lReformationNeighbours[iPlayer]) and self.getReformationHitMatrix(iCiv) == 0):
                                                        self.setReformationHitMatrix(iCiv,1)

        def reformationArrayChoice(self):
                # 3Miro: this should be fixed, recusrion and Python don't go well together
                iCiv = gc.getGame().getSorenRandNum(iNumPlayers, 'Civ chosen for reformation')
                while ( self.getReformationHitMatrix(iCiv) != 1 ):
                        iCiv = gc.getGame().getSorenRandNum(iNumPlayers, 'Civ chosen for reformation')
                #print( " Chosen civ:", iCiv )
                if(self.getReformationHitMatrix(iCiv) == 1):
                        #print( " Chosen civ eligible for Reformation")
                        pPlayer = gc.getPlayer( iCiv )
                        if ( pPlayer.isAlive() and pPlayer.getStateReligion() == xml.iCatholicism ):
                                self.reformationchoice(iCiv)
                        #        print( "Catholic choice:", iCiv )
                        else:
                                self.reformationOther( iCiv )
                        #        print( "Not catholic and alive choice", iCiv )
                        self.setReformationHitMatrix(iCiv,2)
                        for iNextCiv in range(iNumPlayers):
                                if ((iNextCiv in lReformationNeighbours[iCiv]) and self.getReformationHitMatrix(iNextCiv) == 0):
                                        self.setReformationHitMatrix(iNextCiv,1)
                        print( self.getReformationHitMatrixAll(), 2*iNumPlayers )
                        if (sum(self.getReformationHitMatrixAll()) == 2*iNumPlayers):
                                self.setReformationActive(False)
                                self.setCounterReformationActive(True) # after all players have been hit by the Reformation
                else:
                        self.reformationArrayChoice()
                                
        def reformationOther( self, iCiv ):
                cityList = PyPlayer(iCiv).getCityList()
                iChanged = False
                for city in cityList:
                        if(city.city.isHasReligion(xml.iCatholicism)):
                                iDummy = self.reformationReformCity( city.city, 11, False )
                                
                

        def reformationchoice(self, iCiv):
                if ( gc.getPlayer(iCiv).getStateReligion() == xml.iProtestantism ):
                        self.reformationyes(iCiv)
                elif ((gc.getPlayer(iCiv)).isHuman()):
                        self.reformationPopup()
                else:
                        rndnum = gc.getGame().getSorenRandNum(100, 'Reformation')
                        #print( "Reformation calculus:", rndnum, lReformationMatrix[iCiv] )
                        if(rndnum <= lReformationMatrix[iCiv]):
                                self.reformationyes(iCiv)
                                #print( " Yes to Reformation" )
                        else:
                                self.reformationno(iCiv)
                                #print( " No to Reformation" )
                                
        def reformationReformCity( self, pCity, iKeepCatholicismBound, bForceConvertSmall ):
                iFaith = 0
                if(pCity.isHasReligion(xml.iCatholicism)):
                        #iRandNum = gc.getSorenRandNum(100, 'Reformation of a City')
                        if (pCity.getPopulation() > iKeepCatholicismBound ):
                                pCity.setHasReligion(xml.iProtestantism,True,True,False)
                                if(pCity.hasBuilding(xml.iCatholicChapel) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
                                        pCity.setHasRealBuilding(xml.iCatholicChapel, False)
                                        pCity.setHasRealBuilding(xml.iProtestantChapel, True)
                                if(pCity.hasBuilding(xml.iCatholicTemple) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
                                        pCity.setHasRealBuilding(xml.iCatholicTemple, False)
                                        pCity.setHasRealBuilding(xml.iProtestantTemple, True)
                                        iFaith += 1
                                if(pCity.hasBuilding(xml.iCatholicMonastery) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
                                        pCity.setHasRealBuilding(xml.iCatholicMonastery, False)
                                        pCity.setHasRealBuilding(xml.iProtestantSeminary, True)
                                        iFaith += 1
                                if(pCity.hasBuilding(xml.iCatholicCathedral) and gc.getGame().getSorenRandNum(100, 'Reformation of a City') > 50 ):
                                        pCity.setHasRealBuilding(xml.iCatholicCathedral, False)
					if ( pCity.hasBuilding(xml.iCatholicReliquary) ):
						pCity.setHasRealBuilding(xml.iCatholicReliquary, False) # remove Reliquary since it is connected to the Cathedral
                                        pCity.setHasRealBuilding(xml.iProtestantCathedral, True)
                                        iFaith += 1
                        elif ( bForceConvertSmall or gc.getGame().getSorenRandNum(100, 'Reformation of a City') < lReformationMatrix[pCity.getOwner()] ):
                                pCity.setHasReligion(xml.iProtestantism,True,True,False)
                                iFaith += 1
                                if(pCity.hasBuilding(xml.iCatholicReliquary)):
                                        pCity.setHasRealBuilding(xml.iCatholicReliquary, False)
                                if(pCity.hasBuilding(xml.iCatholicChapel)):
                                        pCity.setHasRealBuilding(xml.iCatholicChapel, False)
                                        pCity.setHasRealBuilding(xml.iProtestantChapel, True)
                                if(pCity.hasBuilding(xml.iCatholicTemple)):
                                        pCity.setHasRealBuilding(xml.iCatholicTemple, False)
                                        pCity.setHasRealBuilding(xml.iProtestantTemple, True)
                                        iFaith += 1
                                if(pCity.hasBuilding(xml.iCatholicMonastery)):
                                        pCity.setHasRealBuilding(xml.iCatholicMonastery, False)
                                        pCity.setHasRealBuilding(xml.iProtestantSeminary, True)
                                        iFaith += 1
                                if(pCity.hasBuilding(xml.iCatholicCathedral)):
                                        pCity.setHasRealBuilding(xml.iCatholicCathedral, False)
                                        pCity.setHasRealBuilding(xml.iProtestantCathedral, True)
                                        iFaith += 1
                                pCity.setHasReligion(xml.iCatholicism,False,False,False)
                return iFaith

        def reformationyes(self, iCiv):
                cityList = PyPlayer(iCiv).getCityList()
                iFaith = 0
                for city in cityList:
                        if(city.city.isHasReligion(xml.iCatholicism)):
                                iFaith += self.reformationReformCity( city.city, 7, True )

                pPlayer = gc.getPlayer(iCiv)
                #iStateReligion = pPlayer.getStateReligion()
                #if (pPlayer.getStateReligion() == xml.iCatholicism):
                pPlayer.setLastStateReligion(xml.iProtestantism)
                pPlayer.setFaith( iFaith )

        def reformationno(self, iCiv):
                cityList = PyPlayer(iCiv).getCityList()
                iLostFaith = 0
                for city in cityList:
                        if(city.city.isHasReligion(xml.iCatholicism)):
                                rndnum = gc.getGame().getSorenRandNum(100, 'ReformationAnyway')
                                if(rndnum <= lReformationMatrix[iCiv]):
                                        city.city.setHasReligion(xml.iProtestantism, True, False, False)
                                        iLostFaith += 1
                                        #iLostFaith += self.reformationReformCity( city.city, 9, False )
                gc.getPlayer(iCiv).changeFaith( - min( gc.getPlayer(iCiv).getFaith(), iLostFaith ) )
                
        def doCounterReformation(self):
                print(" Counter Reformation ")
                for iPlayer in range( con.iPope - 1 ):
                        pPlayer = gc.getPlayer( iPlayer )
                        if ( pPlayer.isAlive() and pPlayer.getStateReligion() == xml.iCatholicism ):
                                if ( pPlayer.isHuman() ):
                                        self.doCounterReformationHuman( iPlayer )
                                elif ( lReformationMatrix[iPlayer] < gc.getGame().getSorenRandNum(100, 'Counter Reformation AI') ):
                                        self.doCounterReformationYes( iPlayer )
                                else:
                                        self.doCounterReformationNo( iPlayer )
                self.setCounterReformationActive(False)
        
        def doCounterReformationHuman( self, iPlayer ):
                pPlayer = gc.getPlayer( iPlayer )
                szMessageYes = CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_YES_1", ()) + "+%d " %(max( 1, pPlayer.getNumCities() / 3 )) + CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_YES_2", ())
                szMessageNo = CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_NO_1", ()) + "+%d " %(max( 1, pPlayer.getNumCities() / 3 )) + CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE_NO_2", ())
                self.showCounterPopup(7626, CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_TITLE", ()), CyTranslator().getText("TXT_KEY_COUNTER_REFORMATION_MESSAGE",()), (szMessageYes, szMessageNo))
                
        def showCounterPopup(self, popupID, title, message, labels):
                popup = Popup.PyPopup(popupID, EventContextTypes.EVENTCONTEXT_ALL)
                popup.setHeaderString(title)
                popup.setBodyString(message)
                for i in labels:
                    popup.addButton( i )
                popup.launch(False)

        def eventApply7626(self, popupReturn):
                iHuman = utils.getHumanID()
                if(popupReturn.getButtonClicked() == 0):
                        self.doCounterReformationYes(iHuman)
                elif(popupReturn.getButtonClicked() == 1):
                        self.doCounterReformationNo(iHuman)
                        
        def doCounterReformationYes( self, iPlayer ):
                print(" Counter Reformation Yes",iPlayer)
                pPlayer = gc.getPlayer( iPlayer )
                pCapital = pPlayer.getCapitalCity()
		iX = pCapital.getX()
		iY = pCapital.getY()
                iNumProsecutors = max( 1, pPlayer.getNumCities() / 3 )
                for i in range( iNumProsecutors ):
                        pPlayer.initUnit(xml.iProsecutor, iX, iY, UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
                for iNbr in range( len( lReformationNeighbours[iPlayer] ) ):
                        pNbr = gc.getPlayer( lReformationNeighbours[iPlayer][iNbr] )
                        if ( pNbr.isAlive() and pNbr.getStateReligion() == xml.iProtestantism ):
                                pNCapital = pNbr.getCapitalCity()
                                iX = pNCapital.getX()
                                iY = pNCapital.getY()
                                pNbr.initUnit(xml.iProsecutor, iX, iY, UnitAITypes.UNITAI_MISSIONARY, DirectionTypes.DIRECTION_SOUTH)
        
        def doCounterReformationNo( self, iPlayer ):
                pPlayer = gc.getPlayer( iPlayer )
                pPlayer.changeStabilityBase( con.iCathegoryCities, max( 1, pPlayer.getNumCities() / 3 ) )      
        ### End Reformation ###
