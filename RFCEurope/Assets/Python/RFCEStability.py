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
                
                # Swing stability converges to zero very fast
                iStabilitySwing = pPlayer.getStabilitySwing()
                if ( iStabilitySwing < -7 or iStabilitySwing > 7 ):
                        pPlayer.setStabilitySwing( pPlayer.getStabilitySwing()/2 )
                elif ( iStabilitySwing < 0 ):
                        pPlayer.setStabilitySwing( min( 0, pPlayer.getStabilitySwing() + 3) )
                elif ( iStabilitySwing > 0 ):
                        pPlayer.setStabilitySwing( max( 0, pPlayer.getStabilitySwing() - 3) )
                
                if ( pPlayer.getAnarchyTurns() != 0 ):
                        self.recalcCivicCombos(iPlayer)
                        if ( pPlayer.isHuman() ):
                                pPlayer.changeStabilityBase( iCathegoryCivics, -4 )
                        else:
                                pPlayer.changeStabilityBase( iCathegoryCivics, -2 ) # the AI is largely unaware of Stability issues
                        pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() - 15  )
                
                if ( pPlayer.getWarPeaceChange() == -1 ): # we have been involved in a war since last turn
                        gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryCities, -1 )
                        pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() - 3  )
                
                if ( (iGameTurn + iPlayer) % 3 == 0 ): # Economy Check every 3 turns
                        self.recalcEconomy( pPlayer )
                        
                self.recalcCity( iPlayer ) # update city stability
                
                
                        
                        
                if ( iGameTurn % 6 == 1 ):
                        szShortName = cyPlayer.getCivilizationShortDescription()
                        print(" Turn: ",iGameTurn)
                        print " ---------------- New Stability For " + cyPlayer.getCivilizationShortDescription()
                        print("  ",szShortName," Stability : ",pPlayer.getStability() )
                        print("                  Cities    : ",pPlayer.getStabilityBase( iCathegoryCities ) + pPlayer.getStabilityVary( iCathegoryCities ))
                        print("                  Civics    : ",pPlayer.getStabilityBase( iCathegoryCivics ) + pPlayer.getStabilityVary( iCathegoryCivics ))
                        print("                  Economy   : ",pPlayer.getStabilityBase( iCathegoryEconomy ) + pPlayer.getStabilityVary( iCathegoryEconomy ) )
                        print("                  Swing     : ",pPlayer.getStabilitySwing() )

                
        
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
                self.recalcCivicCombos(iPlayer)
                pass
                

        def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
                if (city.hasBuilding(xml.iEscorial)):
                        gc.getPlayer( playerType ).setPicklefreeParameter( con.iIsHasEscorial, 1 )
                        gc.getPlayer( owner ).setPicklefreeParameter( con.iIsHasEscorial, 0 )
		if (city.hasBuilding(xml.iStephansdom)):
			gc.getPlayer( playerType ).setPicklefreeParameter( con.iIsHasStephansdom, 1 )
                        gc.getPlayer( owner ).setPicklefreeParameter( con.iIsHasStephansdom, 0 )
                self.recalcCivicCombos(playerType)
                
                pass

        def onCityRazed(self, iOwner, playerType, city):
            	#Sedna17: Not sure what difference between iOwner and playerType is here
		#3Miro: iOwner owns the city (victim) and playerType conquers the city (pillager)
                if (city.hasBuilding(xml.iEscorial)):
                        gc.getPlayer( playerType ).setPicklefreeParameter( con.iIsHasEscorial, 0 )
                        gc.getPlayer( owner ).setPicklefreeParameter( con.iIsHasEscorial, 0 )
		if (city.hasBuilding(xml.iStephansdom)):
			gc.getPlayer( playerType ).setPicklefreeParameter( con.iIsHasStephansdom, 0 )
                        gc.getPlayer( owner ).setPicklefreeParameter( con.iIsHasStephansdom, 0 )
                self.recalcCivicCombos(playerType)
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
                	gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryCivics, 1 )
                elif ( iBuilding == xml.iCourthouse or iBuilding == xml.iHolyRomanRathaus or iBuilding == xml.iKievVeche ):
                        gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryCities, 1 )
                elif (iBuilding == xml.iEscorial):
			gc.getPlayer( iPlayer ).setPicklefreeParameter( con.iIsHasEscorial, 1 )
		elif (iBuilding == xml.iStephansdom):
			gc.getPlayer( iPlayer ).setPicklefreeParameter( con.iIsHasStephansdom, 1 )

        def onProjectBuilt(self, iPlayer, iProject):
                pPlayer = gc.getPlayer(iPlayer)
                iCivic5 = pPlayer.getCivics(5)
                
                if (iCivic5 == 29): #If civ is in Colonialism
                        if (iProject >= xml.iNumNotColonies):
                                pPlayer.changeStabilityBase( iCathegoryExpansion, 1 )


        def onCombatResult(self, argsList):
                pass


        def onReligionFounded(self, iPlayer):
                pass


        def onCorporationFounded(self, iPlayer):
                gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryEconomy, -2 ) # a small offset to the large boost of income
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
                pPlayer = gc.getPlayer(iPlayer)
                pPlayer.changeStabilityBase( iCathegoryCities, -pPlayer.getStabilityBase( iCathegoryCities ) )
                pPlayer.changeStabilityBase( iCathegoryCivics, -pPlayer.getStabilityBase( iCathegoryCivics ) )
                pPlayer.changeStabilityBase( iCathegoryEconomy, -pPlayer.getStabilityBase( iCathegoryEconomy ) )
                pPlayer.changeStabilityBase( iCathegoryExpansion, -pPlayer.getStabilityBase( iCathegoryExpansion ) )
                pPlayer.setStabilityVary( iCathegoryCities, 0 )
                pPlayer.setStabilityVary( iCathegoryCivics, 0 )
                pPlayer.setStabilityVary( iCathegoryEconomy, 0 )
                pPlayer.setStabilityVary( iCathegoryExpansion, 0 )
                pPlayer.setStabilitySwing( 0 )
                
        def recalcCity( self, iPlayer ):
                pPlayer = gc.getPlayer( iPlayer )
                iCivic4 = pPlayer.getCivics(4)
                iTotalHappy = pPlayer.calculateTotalCityHappiness() - pPlayer.calculateTotalCityUnhappiness()
                iCityStability = 0
                ### For Debug Purposes, count individual contributions
                iHappyStability = max( (iTotalHappy / pPlayer.getNumCities() - 1)/2, 0 ) # more than +2 happy per city, negative effects are handled below
                iHealthStability = 0
                iHurryStability = 0
                iMilitaryStability = 0
                iWarWStability  = 0
                iReligionStability = 0
                iCultureStability = 0
                ### end
                apCityList = PyPlayer(iPlayer).getCityList()
                for pLoopCity in apCityList:
                        pCity = pLoopCity.GetCy()
                        if ( pCity.healthRate(False,0) > 0 ):
                                iHealthStability += 1
                        if ( pCity.angryPopulation(0) > 0 ):
                                iHappyStability -= 2
                        if ( pCity.getReligionBadHappiness() > 0 ):
                                iReligionStability -= 1
                        if ( pCity.getHurryAngerModifier() > 0 ):
                                iHurryStability -= 1
                        if ( pCity.getNoMilitaryPercentAnger() > 0 ):
                                iMilitaryStability -= 1
                        if ( pCity.getWarWearinessPercentAnger() > 0 ):
                                iWarWStability -= 1
                        if ( iCivic4 != 24 ): # if not a Free religion
                                if ( ( not gc.hasUP( iPlayer, con.iUP_ReligiousTolerance )) and pCity.getNumForeignReligions() > 0 ):
                                        if ( iCivic4 == 20 ): # pagans are a bit more tolerant
                                                iReligionStability -= 1
                                        else:
                                                iReligionStability -= 2
                        iTotalCulture = pCity.countTotalCultureTimes100()
                        if ( (iTotalCulture > 0) and ( (pCity.getCulture(iPlayer) * 10000) / iTotalCulture < 40 ) and ( not gc.hasUP( iPlayer, con.iUP_CulturalTolerance )) ):
                                iCultureStability -= 1
                # 3Miro: prosecution count is decremented in Religions.py
		iProsecutionCount = pPlayer.getProsecutionCount()
		if ( iProsecutionCount > 0 ):
                        iReligionStability -= 2* ( (iProsecutionCount+9) / 10 )
                # Humans are far more competent then the AI, so give the AI a small boost
                if ( pPlayer.isHuman() ):
                        iCityStability += iHappyStability + iHealthStability + iReligionStability + iHurryStability + iCultureStability
                        iCityStability += max( iMilitaryStability + iWarWStability, -4 )
                        iCityStability = min( max( iCityStability, -10 ), 8 )
                else:
                        iCityStability += max( iHappyStability, -2 ) + iHealthStability # AI keeps very unhappy cities
                        iCityStability += max( iReligionStability + iHurryStability, -3 )+ max( iCultureStability, -3 )
                        iCityStability = min( max( iCityStability, -8 ), 8 )
                print(" City Stability for: ",iPlayer," Caths: ",iHappyStability,iHealthStability,iHurryStability,iMilitaryStability,iWarWStability,iReligionStability,iCultureStability)
                pPlayer.setStabilityVary( iCathegoryCities, iCityStability)

	def recalcCivicCombos(self, iPlayer):
                # Note from 3Miro: this is the only place Civics are referenced, yet refering them by number makes this hard to read
                pPlayer = gc.getPlayer(iPlayer)
                iCivic0 = pPlayer.getCivics(0)
                iCivic1 = pPlayer.getCivics(1)
                iCivic2 = pPlayer.getCivics(2)
                iCivic3 = pPlayer.getCivics(3)
                iCivic4 = pPlayer.getCivics(4)
                iCivic5 = pPlayer.getCivics(5)
                
                iCivicCombo = 0
                if (iCivic3 == 19): #Merchant Republic doesn't require Republic since they are different tiers
                        if (iCivic1 == 6): #Incompatible with Feudal Law (Venice likes this one)
				iCivicCombo -= 5
                if (iCivic0 == 2): #Divine Monarchy should have an appropriate religious civic
			if (iCivic4 == 20): #Paganism
				iCivicCombo -=4
			if (iCivic4 == 22): #Theocracy
				iCivicCombo +=2
			if (iCivic4 == 23): #State Religion
				iCivicCombo +=2
			if (iCivic4 == 24): #Free Religion
				iCivicCombo -=6
			if (iCivic1 == 8): #Religious Law
				iCivicCombo +=4
                if ( pPlayer.getPicklefreeParameter( con.iIsHasStephansdom ) == 1 ):
                        #if (self.getHasStephansdom(iPlayer) == 1):
                        if(iCivic0 == 2 or iCivic0 == 3):
					iCivicCombo +=2
                if (iCivic0 == 3 or iCivic0 == 4): #Limited Monarchy and Republics both like enlightened civics
                        if (iCivic1 == 9): #Common Law
                                iCivicCombo +=2
                        if (iCivic2 == 12 or iCivic2 == 14): #Free Peasantry or free labor
                                iCivicCombo +=3
                if (iCivic1 == 6): #Feudal law works well with...
                        if (iCivic2 == 11): # Serfdom
                                iCivicCombo +=1
                        if (iCivic3 == 16): #Manorialism
                                iCivicCombo +=1
                        if (iCivic2 == 12): #but poorly with uppity free peasants
                                iCivicCombo -=5
                if (iCivic2 == 11 and iCivic3 == 16): #Serfdom and Manorialism go together
                        iCivicCombo +=2
                if (iCivic1 == 8): #Religious Law 
                        if (iCivic4 == 20 or iCivic4 == 24): #Dislikes Paganism or Free Religion
                                iCivicCombo -=6
                        if (iCivic4 == 22): #Favors theocracy
                                iCivicCombo +=4
                if (iCivic1 == 9): #Common Law 
                        if (iCivic2 == 14): #likes Free labor
                                iCivicCombo +=4
                        if (iCivic4 == 22): #dislikes theocracy
                                iCivicCombo -=7
                if (iCivic2 == 13 and iCivic3 == 18): #Apprenticeship
                        iCivicCombo +=3
                if (iCivic1 == 7): #Bureaucracy 
                        if (pPlayer.getNumCities() <= 5):
                                iCivicCombo += 4
                        elif ( pPlayer.isHuman() ):
                                iCivicCombo += max(-6,(5 - pPlayer.getNumCities()))
                        else:
                                iCivicCombo += max(-2,(5 - pPlayer.getNumCities())) # Turkish and Moscow AI think this is a good civic???
                if (iCivic0 == 4): #Merchant Republic city cap (like Republic from RFC)
                        iCivicCombo += max(-4,(3 - pPlayer.getNumCities()))
                # TODO: boost for stability depending on the current stability
                #if (iCivic0 == 2): #Divine Monarchy
                #        if (self.getStability(iPlayer) > 30):
                #                iCivicCombo += 5
                #if (iCivic0 == 3): #Limited Monarchy
                #        if (self.getStability(iPlayer) < -60):
                #                iCivicCombo += 5
                #if (iCivic0 == 4): #Republic
                #        if (self.getStability(iPlayer) > 50):
                #                iCivicCombo += 10
                #szShortName = pPlayer.getCivilizationShortDescription()
                print(" Civic Combo for ",iPlayer,"   is ",iCivicCombo)
                print("       Civics  ",iCivic0,"  ",iCivic1,"  ",iCivic2,"  ",iCivic3,"  ",iCivic4)
                pPlayer.setStabilityVary( iCathegoryCivics, iCivicCombo)

        def recalcEconomy(self, pPlayer):
                iPopNum = pPlayer.getTotalPopulation()
                iNumCities = pPlayer.getNumCities()
                
                iImports = pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
                iExports = pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
                iFinances = pPlayer.getFinancialPower()
                iInflation = pPlayer.calculateInflatedCosts()
                iProduction = pPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
                iAgriculture = pPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD)
        
                iLargeCities = 0
                iProductionPenalty = 0
                apCityList = PyPlayer(pPlayer.getID()).getCityList()
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
                        iCityPop = pCity.getPopulation()
                        if ( iCityPop > 10 ): # large cities should have production bonus buildings, drop by 10 percent
                                iProduction -= pCity.getYieldRate(YieldTypes.YIELD_PRODUCTION) / 10
                                iLargeCities += 1
                                
                iFinances = (iFinances * ( 100 - 20 * iLargeCities / iNumCities ) ) / 100
                                
                iProductionPenalty = min( iProductionPenalty + iNumCities / 3, 0 )
                if ( pPlayer.getPicklefreeParameter( con.iIsHasEscorial ) == 1 ): # remove the production penalty, otherwise it will be OP
                        iProductionPenalty = max( iProductionPenalty, 0 )
                iIndustrialStability = min( max( 2 * ( 2 * iAgriculture + iProduction ) / iPopNum - 13, -3 ), 3 )
                iFinancialPowerPerCity = ( iFinances - iInflation + iImports + iExports ) / iNumCities
                iFinancialStability = min( max( ( iFinances - iInflation + iImports + iExports )/iPopNum + iProductionPenalty,  -4 ), 4 )
                pPlayer.setStabilityVary( iCathegoryEconomy, iFinancialStability + iIndustrialStability )
                
