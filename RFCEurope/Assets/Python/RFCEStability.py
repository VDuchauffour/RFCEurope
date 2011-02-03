# Rhye's and Fall of Civilization - Stability

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

iCathegoryCities = 0
iCathegoryCivics = 1
iCathegoryEconomy = 2
iCathegoryExpansion = 3

class RFCEStability:


     
##################################################
### Secure storage & retrieval of script data ###
################################################   

        
#######################################
### Main methods (Event-Triggered) ###
#####################################  

        def setup(self): # Sets human starting stability
                for iPlayer in range( iNumMajorPlayers ):
                        pPlayer = gc.getPlayer( iPlayer )
                        for iCath in range( 4 ):
                                pPlayer.changeStabilityBase( iCath, - pPlayer.getStabilityBase( iCath ) )
                                pPlayer.setStabilityVary( iCath, 0 )
                                pPlayer.setStabilitySwing( 0 )


        def checkTurn(self, iGameTurn):
                print "3Miro NewStability Check Turn"
                # 3Miro: hidden modifier based upon the group/continent
        	#if (iGameTurn % 21 == 0):
	       	#	self.continentsNormalization(iGameTurn)
                #if (iGameTurn % 6 == 0): #3 is too short to detect any change; must be a multiple of 3 anyway
			#gc.calcLastOwned() # Compute the RFC arrays (getlOwnedPlots,getlOwnedCities) in C instead
                        #for iLoopCiv in range(iNumPlayers):
                        	#if ( gc.hasUP(iLoopCiv, con.iUP_LandStability) ): #French UP
                        		#self.setOwnedPlotsLastTurn(iLoopCiv, 0)
                        	#else:
                                	#self.setOwnedPlotsLastTurn(iLoopCiv, gc.getlOwnedPlots(iLoopCiv))
                                #self.setOwnedCitiesLastTurn(iLoopCiv, gc.getlOwnedCities(iLoopCiv))

                        ##Display up/down arrows
                        #if (iGameTurn % 3 == 0 and gc.getActivePlayer().getNumCities() > 0):  #numcities required to test autoplay with minor civs
                                #iHuman = utils.getHumanID()
                                #self.setLastRecordedStabilityStuff(0, self.getStability(iHuman))
                                #self.setLastRecordedStabilityStuff(1, utils.getParCities(iHuman))
                                #self.setLastRecordedStabilityStuff(2, utils.getParCivics(iHuman))
                                #self.setLastRecordedStabilityStuff(3, utils.getParEconomy(iHuman))
                                #self.setLastRecordedStabilityStuff(4, utils.getParExpansion(iHuman))
                                #self.setLastRecordedStabilityStuff(5, utils.getParDiplomacy(iHuman))
                pass


        def updateBaseStability(self, iGameTurn, iPlayer): #Base stability is temporary (i.e. turn-based) stability
                # 3Miro: this is called for every player
                #print "3Miro NewStability Update Base"

                cyPlayer = PyHelpers.PyPlayer(iPlayer)
                pPlayer = gc.getPlayer(iPlayer)
                teamPlayer = gc.getTeam(pPlayer.getTeam())
                
                if ( pPlayer.getWarPeaceChange() == -1 ): # we have been involved in a war since last turn
                        gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryCities, -1 )
                
                iImports = pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
                iExports = pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
                
                iFinances = pPlayer.getFinancialPower()
                iInflation = pPlayer.calculateInflatedCosts()
                iProduction = pPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
                iAgriculture = pPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD)
                
                iPopNum = pPlayer.getTotalPopulation()
                iNumCities = pPlayer.getNumCities()
                if ( iGameTurn % 6 == 0 ):
                        iProductionPenalty = 0
                        apCityList = PyPlayer(iPlayer).getCityList()
                        for pLoopCity in apCityList:
                                pCity = pLoopCity.GetCy()
                                if ( pCity.isProductionUnit() ):
                                        iUnit = pCity.getProductionUnit()
                                        if ( iUnit < xml.iWorker or iUnit > xml.iIslamicMissionary ):
                                                iProductionPenalty -= 1
                                elif ( pCity.isProductionBuilding() ):
                                        iBuilding = pCity.getProductionBuilding()
                                        if (iBuilding >= xml.iSistineChapel and iBuilding <= xml.iPressburg): #+2 per wonder
                                                iProductionPenalty -= 2
                                else:
                                        iProductionPenalty -= 2
                        iProductionPenalty = min( iProductionPenalty + iNumCities / 3, 0 )
                        print(" Turn: ",iGameTurn)
                        print " ---------------- New Stability For " + cyPlayer.getCivilizationShortDescription()
                        szShortName = cyPlayer.getCivilizationShortDescription()
                        #print(" Turn: ",iGameTurn,"  Imports: ",iImports,"  Exports: ",iExports,"  Finances: ",iFinances,"  Inflation: ",iInflation)
                        #print(" Production: ",iProduction,"  Agriculture: ",iAgriculture,"  Population: ",iPopNum,"  NumberOfCities: ",iNumCities)
                        iIndustrialStability = min( max( 2 * ( 2 * iAgriculture + iProduction ) / iPopNum - 13, -3 ), 3 )
                        iFinancialPowerPerCity = ( iFinances - iInflation + iImports + iExports ) / iNumCities
                        iFFF = ( iFinances + iImports + iExports ) / iNumCities
                        iFFF3 =  iPopNum / iNumCities
                        #iFinancialStability = min( max( ( iFinances - iInflation + iImports + iExports - 2*iPopNum ) / iNumCities, -3, 3 )
                        iFinancialStability = min( max( ( iFinances - iInflation + iImports + iExports )/iPopNum + iProductionPenalty,  -4 ), 4 )
                        print(" IndustryStability: ",iIndustrialStability,"  Financial 1: ",iFinancialPowerPerCity,"  Financial 2: ", iFFF )
                        print("  ifff3: ",iFFF3,"  Production Penalty: ",iProductionPenalty)
                        iEconomicStability = pPlayer.getStabilityBase( iCathegoryEconomy ) + iFinancialStability + iIndustrialStability
                        print("  ",szShortName," ES: ",iEconomicStability)
                        
                        

                
        
        def continentsNormalization(self, iGameTurn): #Sedna17
                #lContinentModifier = [-1, -1, 0, -2, 0, 0] #Eastern, Central, Atlantic, Islamic, Italian, Norse, see Consts.py
                #for iPlayer in range(iNumPlayers):
                #       if (gc.getPlayer(iPlayer).isAlive()):
                #                for j in range(len(con.lCivStabilityGroups)):
                #                        if (iPlayer in con.lCivStabilityGroups[j]):
		#				self.setParameter(iPlayer, iParExpansionE, True, lContinentModifier[j])
                #                                self.setStability(iPlayer, (self.getStability(iPlayer) + lContinentModifier[j]))
                pass
	

        def onCityBuilt(self, iPlayer, x, y):
                pass
                

        def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
                pass

        def onCityRazed(self, iOwner, playerType, city):
            	#Sedna17: Not sure what difference between iOwner and playerType is here
		#3Miro: iOwner owns the city (victim) and playerType conquers the city (pillager)
                pass

                                                
        def onImprovementDestroyed(self, owner):
                pass


        def onTechAcquired(self, iTech, iPlayer):
                if ( iTech == xml.iFeudalism or
                iTech == xml.iGuilds or
                iTech == xml.iGunpowder or
                iTech == xml.iProfessionalArmy or
                iTech == xml.iNationalism or
                iTech == xml.iCivilService or
                iTech == xml.iEconomics or
                iTech == xml.iMachinery or
                iTech == xml.iAristocracy ):
                        gc.getPlayer(iPlayer).changeStabilityBase( iCathegoryEconomy, -1 )
        	pass


        def onBuildingBuilt(self, iPlayer, iBuilding, city):
		# 3Miro: some buildings give and others take stability
                if ( iBuilding == xml.iManorHouse or iBuilding == xml.iFrenchChateau):
                        gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryEconomy, 1 )
                elif ( iBuilding == xml.iCastle or iBuilding == xml.iMoscowKremlin or iBuilding == xml.iHungarianStronghold or iBuilding == xml.iSpanishCitadel):
                	gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryExpansion, 1 )
                elif ( iBuilding == xml.iNightWatch):
                	gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryCities, 1 )
                elif ( iBuilding == xml.iCourthouse or iBuilding == xml.iHolyRomanRathaus or iBuilding == xml.iKievVeche ):
                        gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryCivics, 1 )

        def onProjectBuilt(self, iPlayer, iProject):
                pPlayer = gc.getPlayer(iPlayer)
                iCivic5 = pPlayer.getCivics(5)


        def onCombatResult(self, argsList):
                pass


        def onReligionFounded(self, iPlayer):
                pass


        def onCorporationFounded(self, iPlayer):
		pass
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
                pass
                #3Miro: Turkey hack, upon their spawn, hit Byzantium and Bulgaria really hard


	def printStability(self, iPlayer, tBaseStability1, tBaseStability3, tPermStability ):
		pass

	def zeroStability(self,iPlayer): #Called by RiseAndFall Resurrection
		pass

			


