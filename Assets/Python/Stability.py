# Rhye's and Fall of Civilization - Stability

from CvPythonExtensions import *
import CvUtil
import PyHelpers   
import Popup
import cPickle as pickle
import Consts as con
import RFCUtils
utils = RFCUtils.RFCUtils()

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

iNumPlayers = con.iNumPlayers
iNumMajorPlayers = con.iNumMajorPlayers
iIndependent = con.iIndependent
iIndependent2 = con.iIndependent2
iNumTotalPlayers = con.iNumTotalPlayers
iBarbarian = con.iBarbarian
tCapitals = con.tCapitals

iParCities3 = con.iParCities3
iParCitiesE = con.iParCitiesE
iParCivics3 = con.iParCivics3
iParCivics1 = con.iParCivics1
iParCivicsE = con.iParCivicsE
iParDiplomacy3 = con.iParDiplomacy3
iParDiplomacyE = con.iParDiplomacyE
iParEconomy3 = con.iParEconomy3
iParEconomy1 = con.iParEconomy1
iParEconomyE = con.iParEconomyE
iParExpansion3 = con.iParExpansion3
iParExpansion1 = con.iParExpansion1
iParExpansionE = con.iParExpansionE


class Stability:


     
##################################################
### Secure storage & retrieval of script data ###
################################################   


        def getBaseStabilityLastTurn( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lBaseStabilityLastTurn'][iCiv]

        def setBaseStabilityLastTurn( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lBaseStabilityLastTurn'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
            
        def getStability( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lStability'][iCiv]

        def setStability( self, iCiv, iNewValue ):
        	#print("  Stability Changed iCiv:  iValue: ",iCiv,iNewValue)
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lStability'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getCombatResultTempModifier( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lCombatResultTempModifier'][iCiv]

        def setCombatResultTempModifier( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lCombatResultTempModifier'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getGNPold( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lGNPold'][iCiv]

        def setGNPold( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lGNPold'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getGNPnew( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lGNPnew'][iCiv]

        def setGNPnew( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lGNPnew'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getRebelCiv( self ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['iRebelCiv']

        def getLatestRebellionTurn( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lLatestRebellionTurn'][iCiv]

        def getPartialBaseStability( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lPartialBaseStability'][iCiv]

        def setPartialBaseStability( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lPartialBaseStability'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getOwnedPlotsLastTurn( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lOwnedPlotsLastTurn'][iCiv]

        def setOwnedPlotsLastTurn( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lOwnedPlotsLastTurn'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

        def getOwnedCitiesLastTurn( self, iCiv ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lOwnedCitiesLastTurn'][iCiv]

        def setOwnedCitiesLastTurn( self, iCiv, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lOwnedCitiesLastTurn'][iCiv] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getStabilityParameters( self, iCiv, iParameter ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lStabilityParameters'][iCiv][iParameter]

        def setStabilityParameters( self, iCiv, iParameter, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lStabilityParameters'][iCiv][iParameter] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )
                
        def getLastRecordedStabilityStuff( self, iParameter ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                return scriptDict['lLastRecordedStabilityStuff'][iParameter]

        def setLastRecordedStabilityStuff( self, iParameter, iNewValue ):
                scriptDict = pickle.loads( gc.getGame().getScriptData() )
                scriptDict['lLastRecordedStabilityStuff'][iParameter] = iNewValue
                gc.getGame().setScriptData( pickle.dumps(scriptDict) )

	def getHasEscorial( self, iCiv ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		return scriptDict['lHasEscorial'][iCiv]

	def setHasEscorial( self, iCiv, iNewValue ):
		scriptDict = pickle.loads( gc.getGame().getScriptData() )
		scriptDict['lHasEscorial'][iCiv] = iNewValue
		gc.getGame().setScriptData( pickle.dumps(scriptDict) )
	

        
#######################################
### Main methods (Event-Triggered) ###
#####################################  

        def setParameter(self, iPlayer, iParameter, bPreviousAmount, iAmount):
                    if (bPreviousAmount):
                            self.setStabilityParameters(iPlayer, iParameter, self.getStabilityParameters(iPlayer,iParameter) + iAmount)
                    else:
                            self.setStabilityParameters(iPlayer,iParameter, 0 + iAmount)

        def setup(self): # Sets human starting stability
                iHandicap = gc.getGame().getHandicapType()
                if (iHandicap == 0):
                        self.setStability(utils.getHumanID(), 20)
			self.setParameter(utils.getHumanID(), iParExpansionE, False, 20) 
                elif (iHandicap == 1):
                        self.setStability(utils.getHumanID(), 5)
			self.setParameter(utils.getHumanID(), iParExpansionE, False, 5) 
                elif (iHandicap == 2):
                        self.setStability(utils.getHumanID(), -10)
			self.setParameter(utils.getHumanID(), iParExpansionE, False, -10) 



        def checkTurn(self, iGameTurn):
        	if (iGameTurn % 21 == 0):
	       		self.continentsNormalization(iGameTurn)
                if (iGameTurn % 6 == 0): #3 is too short to detect any change; must be a multiple of 3 anyway
			gc.calcLastOwned() # Compute the RFC arrays (getlOwnedPlots,getlOwnedCities) in C instead
                        for iLoopCiv in range(iNumPlayers):
                        	if ( gc.hasUP(iLoopCiv, con.iUP_LandStability) ): #French UP
                        		self.setOwnedPlotsLastTurn(iLoopCiv, 0)
                        	else:
                                	self.setOwnedPlotsLastTurn(iLoopCiv, gc.getlOwnedPlots(iLoopCiv))
                                self.setOwnedCitiesLastTurn(iLoopCiv, gc.getlOwnedCities(iLoopCiv))

                        #Display up/down arrows
                        if (iGameTurn % 3 == 0 and gc.getActivePlayer().getNumCities() > 0):  #numcities required to test autoplay with minor civs
                                iHuman = utils.getHumanID()
                                self.setLastRecordedStabilityStuff(0, self.getStability(iHuman))
                                self.setLastRecordedStabilityStuff(1, utils.getParCities(iHuman))
                                self.setLastRecordedStabilityStuff(2, utils.getParCivics(iHuman))
                                self.setLastRecordedStabilityStuff(3, utils.getParEconomy(iHuman))
                                self.setLastRecordedStabilityStuff(4, utils.getParExpansion(iHuman))
                                self.setLastRecordedStabilityStuff(5, utils.getParDiplomacy(iHuman))


        def updateBaseStability(self, iGameTurn, iPlayer): #Base stability is temporary (i.e. turn-based) stability

                pPlayer = gc.getPlayer(iPlayer)
                teamPlayer = gc.getTeam(pPlayer.getTeam())

                iCivic0 = pPlayer.getCivics(0)
                iCivic1 = pPlayer.getCivics(1)
                iCivic2 = pPlayer.getCivics(2)
                iCivic3 = pPlayer.getCivics(3)
                iCivic4 = pPlayer.getCivics(4)
                iCivic5 = pPlayer.getCivics(5)
                
                if (iGameTurn % 3 != 0): 
                        iNewBaseStability3 = self.getPartialBaseStability(iPlayer) #Skip the lengthy calculation every 2 out of 3 turns

                else:   #Every 1/3 turns

			#Calculate Diplomacy Stability
			iNewDiplomacyBaseStability = 0 #Start fresh
                        iNewDiplomacyBaseStability += min( 10, 4*teamPlayer.getDefensivePactTradingCount() ) # +4 per DP, cap at 10
			# If stable while a single neighbour (as defined in consts.py) is unstable loose 5 points.
                        for iLoopCiv in range (iNumPlayers):
                                if (iLoopCiv in con.lNeighbours[iPlayer]):
                                        if (gc.getPlayer(iLoopCiv).isAlive()):
                                                if (self.getStability(iLoopCiv) < -20):
                                                        if (self.getStability(iPlayer) >= 0):
                                                                iNewDiplomacyBaseStability -= 5
								print("Player",iPlayer,"is loosing stability due to player",iLoopCiv)
                                                                break
			# Vassals get +10 and another (-6,5) based on Master's stability / 4
                        for iLoopCiv in range( iNumPlayers ):                                
                                if (teamPlayer.isVassal(iLoopCiv)):
                                        iNewDiplomacyBaseStability += 10                                
                                        iNewDiplomacyBaseStability += min(5,max(-6,self.getStability(iLoopCiv)/4))
                                        break
			# (-3,3) from Vassals' stability / 4. +4 from each vassal if in Viceroy
                        for iLoopCiv2 in range( iNumPlayers ):                                
                                if (gc.getTeam(gc.getPlayer(iLoopCiv2).getTeam()).isVassal(iPlayer)):
                                        iNewDiplomacyBaseStability += min(3,max(-3,self.getStability(iLoopCiv2)/4))                             
                                        if (iCivic5 == 26):
                                                iNewDiplomacyBaseStability += 4
                                                
                        # 3Miro: new action for Imperialism
                        if ( iCivic5 == 27 ):
                        	iNewDiplomacyBaseStability += gc.countCitiesOutside( iPlayer )
                        	
                        iNumContacts = 0
                        iNumOpenBorders = 0
                        iNumWars = 0
                        for iLoopCiv3 in range( iNumPlayers ):     
                                if (pPlayer.canContact(iLoopCiv3) and iLoopCiv3 != iPlayer and gc.getPlayer(iLoopCiv3).isAlive()):
                                        iNumContacts += 1
					#print("Player",iPlayer,"has contact with",iLoopCiv3)
                                if (teamPlayer.isOpenBorders(iLoopCiv3) and iLoopCiv3 != iPlayer and gc.getPlayer(iLoopCiv3).isAlive()):
                                	iNumOpenBorders += 1
					#print("Player",iPlayer,"has open borders with",iLoopCiv3)
                                if (teamPlayer.isAtWar(iLoopCiv3) and iLoopCiv3 != iPlayer and gc.getPlayer(iLoopCiv3).isAlive()):
                                	iNumWars += 1
					#print("Player",iPlayer,"is at war with",iLoopCiv3)

			# (-6,5) from ratio of OpenBorders - 2 * Wars / Contacts
			if ( iNumContacts > 0 ):
				iNewDiplomacyBaseStability += max( -6, ( (5 * ( iNumOpenBorders - 2*iNumWars )) / iNumContacts ) )
                        
                        self.setParameter(iPlayer, iParDiplomacy3, False, iNewDiplomacyBaseStability) #Store current Foreign Stability

			#Calculate Expansion Stability
                        iNewExpansionBaseStability = 0
                        iNumPlotsAbroad = max(0,self.getOwnedPlotsLastTurn(iPlayer)-32) #These are plots outside of your settler map                       
                        iNewExpansionBaseStability -= iNumPlotsAbroad/21 # Effectively -6 per BFC 3Miro value = iNumPlots/21
                        iNewExpansionBaseStability -= self.getOwnedCitiesLastTurn(iPlayer)*4 #-4 per City in Foreign land 3Miro value = 4
                        # penalize (by iCityPenalty), cities in foreign normal teritory and bad settlersMap
			iCityPenalty = -1
                        iCityExp = gc.cityStabilityExpansion(iPlayer, iCityPenalty)
                        iNewExpansionBaseStability += iCityExp
                        self.setParameter(iPlayer, iParExpansion3, False, iNewExpansionBaseStability)

                        #Calculate Civic Stability
                        iNewBaseCivicStability = 0
 			if (iCivic3 == 19): #Merchant Republic should be under a republic
				if (iCivic0 != 4):
					iNewBaseCivicStability -= 5
					#print("iNewBaseCivicStability civic combination1",iNewBaseCivicStability, iPlayer)
				if (iCivic1 == 6): #Incompatible with Feudal Law
					iNewBaseCivicStability -= 10
			if (iCivic0 == 2): #Divine Monarchy should have an appropriate religious civic
				if (iCivic4 == 20): #Paganism
					iNewBaseCivicStability -=3
				if (iCivic4 == 22): #Theocracy
					iNewBaseCivicStability +=2
				if (iCivic4 == 23): #State Religion
					iNewBaseCivicStability +=2
				if (iCivic4 == 24): #Free Religion
					iNewBaseCivicStability -=5
				if (iCivic1 == 8): #Religious Law
					iNewBaseCivicStability +=5
			if (iCivic0 == 3 or iCivic0 == 4): #Limited Monarchy and Republics both like enlightened civics
				if (iCivic1 == 9): #Common Law
					iNewBaseCivicStability +=2
				if (iCivic2 == 12 or iCivic2 == 14): #Free Peasantry or free labor
					iNewBaseCivicStability +=2
			if (iCivic1 == 6): #Feudal law works well with...
				if (iCivic2 == 11): # Serfdom
					iNewBaseCivicStability +=2
				if (iCivic3 == 16): #Manorialism
					iNewBaseCivicStability +=2
				if (iCivic2 == 12): #but poorly with uppity free peasants
					iNewBaseCivicStability -=7
			if (iCivic2 == 11): #Serfdom and Manorialism go together
				if (iCivic3 == 16):
					iNewBaseCivicStability +=2
			if (iCivic1 == 8): #Religious Law 
				if (iCivic0 == 1):#incompatible with Electorate
					iNewBaseCivicStability -=2
				if (iCivic4 == 20 or iCivic4 == 24): #Dislikes Paganism or Free Religion
					iNewBaseCivicStability -=5
				if (iCivic4 == 22): #Favors theocracy
					iNewBaseCivicStability +=5
			if (iCivic1 == 9): #Common Law 
				if (iCivic2 == 14): #likes Free labor
					iNewBaseCivicStability +=5
				if (iCivic4 == 22): #dislikes theocracy
					iNewBaseCivicStability -=7
			if (iCivic2 == 12): #Free Peasants don't like theocracy
				if (iCivic4 == 22):
					iNewBaseCivicStability -=7
			if (iCivic2 == 13): #Apprenticeship
				if (iCivic3 == 17): #and Guilds
					iNewBaseCivicStability +=3
                        if (iCivic1 == 7): #Bureaucracy 
				if (iCivic3 == 18): #Bonus with Mercantalism
					iNewBaseCivicStability +=2
                                if (pPlayer.getNumCities() <= 5):
                                        iNewBaseCivicStability += 5
                                else:
                                        iNewBaseCivicStability += max(-7,(5 - pPlayer.getNumCities()))
			if (iCivic0 == 1): #Electorate. -1 per city beyond capitol. Too harsh? 3Miro: Yep, move to .5 per city
				iNewBaseCivicStability += (1 - pPlayer.getNumCities() / 2)
                        if (iCivic0 == 4): #Merchant Republic city cap (like Republic from RFC)
                                iNewBaseCivicStability += max(-7,2*(3 - pPlayer.getNumCities()))
                        if (iCivic0 == 3): #Limited Monarchy
                                iNewBaseCivicStability += min(10, pPlayer.getNumCities()/5) #slightly counterbalances the effect of number of cities (below)
			if (iCivic0 == 0): #despotism from RFC
                                if (self.getStability(iPlayer) < -60):
                                        iNewBaseCivicStability += 10
                        if (iCivic0 == 2): #Divine Monarchy
                                if (self.getStability(iPlayer) > 30):
                                        iNewBaseCivicStability += 5
                        if (iCivic0 == 3): #Limited Monarchy
                                if (self.getStability(iPlayer) < -60):
                                        iNewBaseCivicStability += 5
                        if (iCivic0 == 4): #Republic
                                if (self.getStability(iPlayer) > 50):
                                        iNewBaseCivicStability += 10
                        self.setParameter(iPlayer, iParCivics3, False, iNewBaseCivicStability)

			#Calculate City Stability
			iNewBaseCityStability = 0
			# 3Miro: stability sweep in C++, for iPlayer penalize by the following amounts:
			#int cityStabilityPenalty( int iPlayer, int iAnger, int iHealth, int iReligion, int iLarge, int iHurry, int iNoMilitary, int iWarW, int iFReligion, int iFCulture, int iPerCityCap );
			iCityPenalty = gc.cityStabilityPenalty(iPlayer, -2, 0, 0, -2, -1, -1, -1, -1, -2, -5 );
                        if (iCityPenalty < 0):
                                iNewBaseCityStability += max(-12, iCityPenalty)

			# 3MiroFaith
			#iNewBaseCityStability += pPlayer.getFaithStability();
			iNewBaseCityStability += pPlayer.getFaithBenefit( con.iFP_Stability )
						
			iHappiness = -10
                        if (pPlayer.calculateTotalCityHappiness() > 0):
                                iHappiness = int((1.0 * pPlayer.calculateTotalCityHappiness()) / (pPlayer.calculateTotalCityHappiness() + \
                                                pPlayer.calculateTotalCityUnhappiness()) * 100) - 60			
                        iNewBaseCityStability += iHappiness/10

			# 3Miro: this is done every 3 turns, so update prosecution stability into city stability
			#iProsecutionCount = utils.getProsecutionCount( iPlayer )
			iProsecutionCount = pPlayer.getProsecutionCount()
			if ( iProsecutionCount > 0 ):
				iStabilityModifier = 2* ( (iProsecutionCount+9) / 10 )
                		iNewBaseCityStability -= iStabilityModifier
                        
                        self.setParameter(iPlayer, iParCities3, False, iNewBaseCityStability)
                        
			#Calculate Economy Stability
			# 3Miro: Import/Export trade routes
                        iNewBaseEconomyStability = 0

                        iImports = pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
                        iExports = pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
                        iImportExportOffset = 3        
                        iTrade = (iImports+iExports)/5 -iImportExportOffset
			
			# Non-trade part of economy
                        iFinances = pPlayer.getFinancialPower() - pPlayer.calculateInflatedCosts()
                        iProduction = pPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
                        iAgriculture = pPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD)
                        iIndustry = iProduction + iAgriculture
                        iPopulation = pPlayer.getRealPopulation() / 1000
                        iPopNum = pPlayer.getTotalPopulation()
                        iNumCities = pPlayer.getNumCities()
                        iExpProd16 = 68
                        iExpFin16 = 74
                        
                        # 3Miro: Economy categories
                        iAgricultureStability = 3*iAgriculture / iPopNum - 7
                        iIndustryStability = 10* (iProduction + iAgriculture) * iNumCities / (iPopNum * ( 4 * iPopNum / 100 + 4 * iNumCities ) ) - 8
                        iFinancialStability = 10* (iFinances) * iNumCities / (iPopNum * ( 24 * iPopNum / 100 + 4 * iNumCities ) ) - 8
                        iNewBaseEconomyStability += min( 10, iTrade ) + min( 4, iAgricultureStability ) + min( 6, iIndustryStability ) + min( 8, iFinancialStability )
			#print("EconomyStability",iNewBaseEconomyStability,iPlayer)
			if (iGameTurn >= con.tBirth[iPlayer]+15): 
				iEconomy = 0
				#print("Economy: Production ",iProduction," Agriculture ", iAgriculture, " Imports ", iImports, " Exports ", iExports, " iFinances ", iFinances)
				iEconomy = iProduction + iAgriculture + iImports + iExports + iFinances
	                        self.setGNPnew(iPlayer, self.getGNPnew(iPlayer) + (iEconomy))                
			
				iMaxShrink = 7
                                iMaxGrowth = 3
                                if self.getGNPold(iPlayer) == 0:
                                	self.setGNPold(iPlayer,1)
                                iGrowth = 100*self.getGNPnew(iPlayer)/self.getGNPold(iPlayer) #Require significant (5%?) growth
                                #print("iGrowth",iGrowth, iPlayer)
                               # print("iGNPnew",self.getGNPnew(iPlayer), iPlayer)
                               # print(iProduction,iAgriculture,iImports,iExports,iFinances)
				#print("iGNPold",self.getGNPold(iPlayer), iPlayer)
				if (iGrowth <= 105):
					iNewBaseEconomyStability += max(-7,(iGrowth-105))
				elif (iGrowth > 105):
					iNewBaseEconomyStability += min(3,(iGrowth-105))
				else:
					pass
				self.setGNPold(iPlayer, self.getGNPnew(iPlayer))
	                        self.setGNPnew(iPlayer, 0)
				#Getting into this loops appears to be killing stability printing (and maybe stability overall?)

                        self.setParameter(iPlayer, iParEconomy3, False, iNewBaseEconomyStability)

			#Save these values for other 2/3 turns
			if (iNewBaseEconomyStability < 0 and self.getHasEscorial(iPlayer) == 1):
				iNewBaseStability3 = iNewBaseCityStability+iNewBaseCivicStability+iNewExpansionBaseStability+iNewDiplomacyBaseStability
			else:
				iNewBaseStability3 = iNewBaseEconomyStability+iNewBaseCityStability+iNewBaseCivicStability+iNewExpansionBaseStability+iNewDiplomacyBaseStability
                        self.setPartialBaseStability(iPlayer, iNewBaseStability3)
			tBaseStability3 = (iNewBaseCityStability,iNewBaseCivicStability,iNewDiplomacyBaseStability,iNewBaseEconomyStability,iNewExpansionBaseStability)

                #every turn
                
                iNewBaseCivicStability1 = 0
		iAnarchyHit = 0
                if (pPlayer.getAnarchyTurns() != 0):
                        CurrentStability = self.getStability(iPlayer)
                        if (CurrentStability > 24):
				iAnarchyHit = -1*CurrentStability/8
                        else:
                                iAnarchyHit = -3
                        self.setParameter(iPlayer, iParCivicsE, True, iAnarchyHit)

                        if (CurrentStability >= 0):
                                iNewBaseCivicStability1 -= 25
                        else:
                                iNewBaseCivicStability1 -= 17
                self.setParameter(iPlayer, iParCivics1, False, iNewBaseCivicStability1) 


                iNewBaseExpansionStability1 = 0
                iNumPlayerCities = pPlayer.getNumCities()
                # 3Miro: Number of Cities Stability Penalty
                if (iNumPlayerCities < 12):
                        pass
                else:
                        iNewBaseExpansionStability1 -= (iNumPlayerCities-8)*(iNumPlayerCities-8)/9
                iEraModifier = 0 # for combat purposes only
		iCombatResult = self.getCombatResultTempModifier(iPlayer)
                if (iCombatResult != 0):
                        iNewBaseExpansionStability1 += max(-20, min(20,iCombatResult))
                        if (iCombatResult <= -4 -(iEraModifier/2)): #great loss results in permanent stability hit
                                self.setParameter(iPlayer, iParDiplomacyE, True, -1)
                        if (abs(iCombatResult) >= 4):
                                self.setCombatResultTempModifier(iPlayer, iCombatResult/2)
                        else:
                                self.setCombatResultTempModifier(iPlayer, 0)
		self.setParameter(iPlayer, iParExpansion1, False, iNewBaseExpansionStability1)
		
		                                        
		iNewBaseEconomyStability1 = 0
                if (pPlayer.isGoldenAge()):
                        iNewBaseEconomyStability1 += 15
	                self.setParameter(iPlayer, iParEconomy1, False, iNewBaseEconomyStability1)

		iNewBaseStability1 = iNewBaseEconomyStability1+iNewBaseExpansionStability1+iNewBaseCivicStability1
		tBaseStability1 = (iNewBaseCivicStability1,iNewBaseEconomyStability1,iNewBaseExpansionStability1)
		iNewBaseStability = iNewBaseStability3 + iNewBaseStability1
                tPermStability = (self.getStabilityParameters(iPlayer,iParCitiesE),self.getStabilityParameters(iPlayer,iParCivicsE),self.getStabilityParameters(iPlayer,iParDiplomacyE),self.getStabilityParameters(iPlayer,iParEconomyE),self.getStabilityParameters(iPlayer,iParExpansionE))
                                
                iPermStability = self.getStabilityParameters(iPlayer,iParCitiesE)+self.getStabilityParameters(iPlayer,iParCivicsE)+self.getStabilityParameters(iPlayer,iParDiplomacyE)+self.getStabilityParameters(iPlayer,iParEconomyE)+self.getStabilityParameters(iPlayer,iParExpansionE)
 		

                self.setStability(iPlayer, iPermStability+iNewBaseStability)
		
		iCurrStability = self.getStability(iPlayer)
                if (iCurrStability < -80):
			self.setParameter(iPlayer, iParExpansionE,True,-80-iCurrStability)
                        self.setStability(iPlayer, -80)
                if (iCurrStability > 80):
			self.setParameter(iPlayer, iParExpansionE,True,80-iCurrStability)
                        self.setStability(iPlayer, 80)
                        
                self.setBaseStabilityLastTurn(iPlayer, iNewBaseStability) 
                #if (iGameTurn % 3 == 0): #On time we have tBaseStability3 defined.
                #	#if (gc.getPlayer(iPlayer).isHuman()): #anti-exploit
		#	self.printStability(iPlayer,tBaseStability1,tBaseStability3,tPermStability)
        
        def continentsNormalization(self, iGameTurn): #Sedna17
                lContinentModifier = [-1, -1, 0, -2, 0, 0] #Eastern, Central, Atlantic, Islamic, Italian, Norse, see Consts.py
                for iPlayer in range(iNumPlayers):
                        if (gc.getPlayer(iPlayer).isAlive()):
                                for j in range(len(con.lCivStabilityGroups)):
                                        if (iPlayer in con.lCivStabilityGroups[j]):
						self.setParameter(iPlayer, iParExpansionE, True, lContinentModifier[j])
                                                self.setStability(iPlayer, (self.getStability(iPlayer) + lContinentModifier[j]))
	

        def onCityBuilt(self, iPlayer, x, y):

                iTempExpansion = 0
                iGameTurn = gc.getGame().getGameTurn()
                if (iGameTurn <= con.tBirth[iPlayer] + 20):
			iTempExpansion += 3
                else:
			iTempExpansion += 1
                if (gc.getPlayer(iPlayer).getNumCities() == 1):
			iTempExpansion += 1
		# 3Miro: Imperialism has changed
                #if (gc.getPlayer(iPlayer).getCivics(5) == 27):
                #        capital = gc.getPlayer(iPlayer).getCapitalCity()
                #        iDistance = utils.calculateDistance(x, y, capital.getX(), capital.getY())
                #        if (iDistance >= 15):
		#		iTempExpansion += 2
                self.setParameter(iPlayer, iParExpansionE, True, iTempExpansion) 
                self.setStability(iPlayer, self.getStability(iPlayer) + iTempExpansion )
                             


        def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
                iGameTurn = gc.getGame().getGameTurn()
                #playerType is the new owner and gains stability, while old owner (owner) loses 

		if (city.hasBuilding(con.iEscorial)):
			self.setHasEscorial(playerType,1)
			self.setHasEscorial(owner,0)
			
                if (owner < con.iNumPlayers):
                        iTotalCityLostModifier = 0       
                 	iDiplomacyHit = 0
                        if (bTrade and (iGameTurn == con.tBirth[playerType] or iGameTurn == con.tBirth[playerType]+1 or iGameTurn == con.tBirth[playerType]+2)):
                                iTotalCityLostModifier = 3 #during a civ birth
                                if (not gc.getPlayer(owner).isHuman()):
                                        iTotalCityLostModifier += 1
                        elif (bTrade and playerType == self.getRebelCiv() and iGameTurn == self.getLatestRebellionTurn(playerType)):
                                iTotalCityLostModifier = 2 #during a civ resurrection
                        else:
                                iTotalCityLostModifier = (16 - gc.getPlayer(owner).getNumCities())/2
                                if (bTrade):                                        
                                        iTotalCityLostModifier += 2
					iDiplomacyHit += 1
                                        if (gc.getPlayer(owner).isHuman()): #anti-exploit
                                                if (city.isOccupation()):
							iTotalCityLostModifier += 3
							iDiplomacyHit += 3
                                if (city.getX() == tCapitals[owner][0] and city.getY() == tCapitals[owner][1]):
                                        iTotalCityLostModifier += 20
	                self.setParameter(owner, iParDiplomacyE, True, -iDiplomacyHit)
                        self.setParameter(owner, iParExpansionE, True, -iTotalCityLostModifier) 
                        self.setStability(owner, self.getStability(owner) - iTotalCityLostModifier - iDiplomacyHit)
                        
                if (playerType < con.iNumPlayers):
                        iTempExpansionThreshold = 0
                        if (iGameTurn == con.tBirth[playerType] or iGameTurn == con.tBirth[playerType]+1 or iGameTurn == con.tBirth[playerType]+2):
                                iTempExpansionThreshold += 3
                        elif (owner >= con.iNumPlayers):
                                iTempExpansionThreshold += max(0,min(5,(12 - gc.getPlayer(playerType).getNumCities())/2))
                        else:
                                iTempExpansionThreshold += max(0,min(5,(12 - gc.getPlayer(playerType).getNumCities())/2))
                        if (gc.getPlayer(playerType).getCivics(5) == 28):
                                if (bConquest):
                                        iTempExpansionThreshold += 2 
                        if (owner < con.iNumPlayers):
                                if (city.getX() == tCapitals[owner][0] and city.getY() == tCapitals[owner][1]):
                                        iTempExpansionThreshold += 3
                        self.setParameter(playerType, iParExpansionE, True, iTempExpansionThreshold) 
                        self.setStability(playerType, self.getStability(playerType) + iTempExpansionThreshold)
                        #print("Sedna17: Stability - city acquired by", playerType)
                        #print("Sedna17: Stability - city acquired iTempExpansionThreshold", iTempExpansionThreshold)

                        

                
     


        def onCityRazed(self, iOwner, playerType, city):
            	#Sedna17: Not sure what difference between iOwner and playerType is here
                if (iOwner < con.iNumPlayers):      
                        self.setParameter(iOwner, iParExpansionE, True, - 3)
                        self.setStability(iOwner, self.getStability(iOwner) - 3 )


                if (playerType < con.iNumPlayers):
                        iTempExpansionThreshold = 0                
                        if (gc.getPlayer(playerType).getCivics(5) == 28):
                                iTempExpansionThreshold -= 2  #balance the +2 and makes 0 for city razed
                        self.setParameter(playerType, iParExpansionE, True, iTempExpansionThreshold) 
                        self.setStability(playerType, self.getStability(playerType) + iTempExpansionThreshold) 


                                                
        def onImprovementDestroyed(self, owner):

                if (owner < con.iNumPlayers and owner >= 0):
	                iTempExpansionThreshold = -1                
	                self.setParameter(owner, iParExpansionE, True, iTempExpansionThreshold) 
                        self.setStability(owner, self.getStability(playerType) + iTempExpansionThreshold) 
                        ##print("Stability - improvement destroyed", owner)


        def onTechAcquired(self, iTech, iPlayer):
        	if (iTech == con.iBronzeCasting or
        	iTech == con.iStirrup or
        	iTech == con.iChainMail or
        	iTech == con.iMachinery or
        	iTech == con.iFarriers):
			self.setParameter(iPlayer, iParEconomyE, True, -2)
			self.setStability(iPlayer, self.getStability(iPlayer)-2)
        	elif (iTech == con.iMonasticism or
        	iTech == con.iAstrolabe or
        	iTech == con.iHerbalMedicine or
        	iTech == con.iArt or
        	iTech == con.iVaultedArches or 
        	iTech == con.iMusic):
			self.setParameter(iPlayer, iParEconomyE, True, 1)
			self.setStability(iPlayer, self.getStability(iPlayer)+1)
        	pass


        def onBuildingBuilt(self, iPlayer, iBuilding, city):
		# 3Miro: some buildings give and others take stability
                iTempCitiesThreshold = 0
                if (iBuilding == con.iPalace): #palace
                	iTempCitiesThreshold -= 15 
                elif ( iBuilding == con.iCourthouse or iBuilding == con.iHolyRomanRathaus or iBuilding == con.iKievVeche):
                	iTempCitiesThreshold += 1
                elif ( iBuilding == con.iManorHouse or iBuilding == con.iBurgundianChateau):
                	iTempCitiesThreshold += 1
                elif ( iBuilding == con.iDungeon):
                	iTempCitiesThreshold += 1
                elif ( iBuilding == con.iNightWatch):
                	iTempCitiesThreshold += 1
		elif (iBuilding == con.iEscorial):
			self.setHasEscorial(iPlayer,1)
		if (iBuilding >= con.iSistineChapel and iBuilding <= con.iTombKhal): #+2 per wonder
			iTempCitiesThreshold +=2
                self.setParameter(iPlayer, iParCitiesE, True, iTempCitiesThreshold)
                self.setStability(iPlayer, self.getStability(iPlayer)+iTempCitiesThreshold)

                    


                            
        def onProjectBuilt(self, iPlayer, iProject):
            
                #if (iProject <= con.iApolloProgram ): #no SS parts
                #        self.setStability(iPlayer, self.getStability(iPlayer) + 1 )
                #        self.setParameter(iPlayer, iParCitiesE, True, 2)
                #        #print("Stability - project built", iPlayer)
                pass




        def onCombatResult(self, argsList):

                pWinningUnit,pLosingUnit = argsList
                iWinningPlayer = pWinningUnit.getOwner()
                iLosingPlayer = pLosingUnit.getOwner()

                if (iWinningPlayer < con.iNumPlayers):  
                        self.setCombatResultTempModifier(iWinningPlayer, self.getCombatResultTempModifier(iWinningPlayer) + 1 )
                        #print("Stability - iWinningPlayer", self.getCombatResultTempModifier(iWinningPlayer), iWinningPlayer)
                if (iLosingPlayer < con.iNumPlayers):  
                        self.setCombatResultTempModifier(iLosingPlayer, self.getCombatResultTempModifier(iLosingPlayer) - 2 )
                        #print("Stability - iLosingPlayer", self.getCombatResultTempModifier(iLosingPlayer), iLosingPlayer)


        def onReligionFounded(self, iPlayer):

                #self.setStability(iPlayer, self.getStability(iPlayer) - 2 )
                #self.setParameter(iPlayer, iParCitiesE, True, -2)
                #print("Stability - onReligionFounded", iPlayer)
                pass


        def onCorporationFounded(self, iPlayer):
		self.setParameter(iPlayer, iParCitiesE, True, -2)
                self.setStability(iPlayer, self.getStability(iPlayer) - 2 )
                #print("Stability - onCorporationFounded", iPlayer)


        def onReligionSpread(self, iReligion, iPlayer):
        	pass
		#Sedna17: Religions seemed to be subtracted and re-inserted into cities, which makes this a bad idea.
                #if (iPlayer < iNumPlayers):  
                #        pPlayer = gc.getPlayer(iPlayer)
                #        if (pPlayer.getStateReligion() != iReligion):
                #                for iLoopCiv in range(iNumPlayers):
                #                        if (gc.getTeam(pPlayer.getTeam()).isAtWar(iLoopCiv)):
                #                                if (gc.getPlayer(iLoopCiv).getStateReligion() == iReligion):
                #                                        self.setStability(iPlayer, self.getStability(iPlayer) - 1 )
                #                                        self.setParameter(iPlayer, iParCitiesE, True, -1)
                #                                        print("Stability - onReligionSpread - Target = ", iPlayer, "Cause = ", iLoopCiv, "Religion = ",iReligion)
                #					 break

       	
        def checkImplosion(self, iGameTurn):
    
                if (iGameTurn > 10 and iGameTurn % 8 == 5):
                        for iPlayer in range(iNumPlayers):
                                if (gc.getPlayer(iPlayer).isAlive() and iGameTurn >= con.tBirth[iPlayer] + 25):
                                	# 3MiroUP: Emperor
                                        if (self.getStability(iPlayer) < -40 and not utils.collapseImmune(iPlayer) ): #civil war
                                                print ("COLLAPSE: CIVIL WAR", gc.getPlayer(iPlayer).getCivilizationAdjective(0))
                                                if (iPlayer != utils.getHumanID()):
                                                        if (gc.getPlayer(utils.getHumanID()).canContact(iPlayer)):
                                                                CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, gc.getPlayer(iPlayer).getCivilizationDescription(0) + " " + \
                                                                                                    CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
                                                        #if (iGameTurn < con.i1000AD):
                                                        # 3Miro: fragments to indeps and barbs, after some year just indeps
                                                        #utils.killAndFragmentCiv(iPlayer, iIndependent, iIndependent2, -1, False)
                                                        utils.killAndFragmentCiv(iPlayer, False, False)
                                                       
                                                else:
                                                        if (gc.getPlayer(iPlayer).getNumCities() > 1):
                                                                CyInterface().addMessage(iPlayer, True, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
                                                                #utils.killAndFragmentCiv(iPlayer, iIndependent, iIndependent2, -1, True)
                                                                utils.killAndFragmentCiv(iPlayer, False, True)
                                                                self.setStability(iPlayer, -15)
                                                return



	def printStability(self, iPlayer, tBaseStability1, tBaseStability3, tPermStability ):
		print( " 3Miro: STABILITY FOR PLAYER: ",iPlayer )
		print( "          iParCities3: ",tBaseStability3[0])
		print( "          iParCitiesE: ",tPermStability[0] )
		print( "          iParCivics3: ",tBaseStability3[1])
		print( "          iParCivicsE: ",tPermStability[1] )
		print( "          iParCivics1: ",tBaseStability1[0])
		print( "       iParDiplomacy3: ",tBaseStability3[2])
		print( "       iParDiplomacyE: ",tPermStability[2] )
		print( "         iParEconomy3: ",tBaseStability3[3])
		print( "         iParEconomyE: ",tPermStability[3] )
		print( "         iParEconomy1: ",tBaseStability1[1])
		print( "       iParExpansion3: ",tBaseStability3[4])
		print( "       iParExpansionE: ",tPermStability[4] )
		print( "       iParExpansion1: ",tBaseStability1[2])
		print( "            Stability: ",self.getStability( iPlayer ) )

	def zeroStability(self,iPlayer): #Called by RiseAndFall Resurrection
		for iCount in range(con.iNumStabilityParameters):
			self.setParameter(iPlayer, iCount, False, 0)

			


