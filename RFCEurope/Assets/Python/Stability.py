# Rhye's and Fall of Civilization - Stability

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
#import cPickle as pickle
import Consts as con
import XMLConsts as xml
#import RFCEStability
import RFCUtils
import RFCEMaps as rfcemaps

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
iCathegoryCities = con.iCathegoryCities
iCathegoryCivics = con.iCathegoryCivics
iCathegoryEconomy = con.iCathegoryEconomy
iCathegoryExpansion = con.iCathegoryExpansion
tCapitals = con.tCapitals

tStabilityPenalty = ( -4, -1, 0, 0, 0 )

class Stability:

	def setup(self): # Sets human starting stability
		for iPlayer in range( iNumMajorPlayers ):
			pPlayer = gc.getPlayer( iPlayer )
			for iCath in range( 4 ):
				pPlayer.changeStabilityBase( iCath, - pPlayer.getStabilityBase( iCath ) )
				pPlayer.setStabilityVary( iCath, 0 )
			pPlayer.setStabilitySwing( 0 )
		if ( not gc.getPlayer( con.iFrankia ).isHuman() ):
			gc.getPlayer( con.iFrankia ).changeStabilityBase( iCathegoryExpansion, 5 ) # so that they don't collapse from the cities they lose to everyone
		#if ( not gc.getPlayer( con.iVenecia ).isHuman() ):
			#gc.getPlayer( con.iVenecia ).changeStabilityBase( iCathegoryExpansion, 4 ) # they collapse too often
		#if ( gc.getPlayer( con.iDenmark ).isHuman() ):
			#gc.getPlayer( con.iDenmark ).changeStabilityBase( iCathegoryExpansion, 2 ) # too many border provinces to conquer in short time
		iHandicap = gc.getGame().getHandicapType()
		if (iHandicap == 0):
			gc.getPlayer( utils.getHumanID() ).changeStabilityBase( iCathegoryExpansion, 6 )
		elif (iHandicap == 0):
			gc.getPlayer( utils.getHumanID() ).changeStabilityBase( iCathegoryExpansion, 2 )

		# Absinthe: Stability is accounted properly for stuff placed in WB - from RFCE++
		for iPlayer in range(iNumMajorPlayers):
			pPlayer = gc.getPlayer(iPlayer)
			apCityList = PyPlayer(iPlayer).getCityList()
			iCounter = 0
			for pLoopCity in apCityList:
				pCity = pLoopCity.GetCy()
				iCounter += 1
				iOldStab = pPlayer.getStability()

				# Province stability
				iProv = rfcemaps.tProinceMap[pCity.getY()][pCity.getX()]
				if ( pPlayer.getProvinceType( iProv ) >= con.iProvincePotential ):
					pPlayer.changeStabilityBase( iCathegoryExpansion, 1 )
				elif ( not gc.hasUP( iPlayer, con.iUP_StabilitySettler ) ):
					pPlayer.changeStabilityBase( iCathegoryExpansion, -2 )
				if ( iCounter < 5 ): # early boost to small Empires
					pPlayer.changeStabilityBase( iCathegoryExpansion, 1 )

				# Building stability
				for econBuilding in (xml.iManorHouse, xml.iFrenchChateau):
					if (pCity.hasBuilding(econBuilding)):
						pPlayer.changeStabilityBase( iCathegoryEconomy, 1 )
				for expBuilding in (xml.iCastle, xml.iMoscowKremlin, xml.iHungarianStronghold, xml.iSpanishCitadel):
					if (pCity.hasBuilding(expBuilding)):
						pPlayer.changeStabilityBase( iCathegoryExpansion, 1 )
				for civicBuilding in (xml.iNightWatch, xml.iSwedishTennant):
					if (pCity.hasBuilding(civicBuilding)):
						pPlayer.changeStabilityBase( iCathegoryCivics, 1 )
				for cityBuilding in (xml.iCourthouse, xml.iHolyRomanRathaus, xml.iKievVeche, xml.iLithuanianVoivodeship ):
					if (pCity.hasBuilding(cityBuilding)):
						pPlayer.changeStabilityBase( iCathegoryCities, 1 )
				print(pCity.getName() + " contributes " + str(pPlayer.getStability() - iOldStab) + " stability.")

			print("Player "+str(iPlayer)+" initial stability: "+str(pPlayer.getStability()))


	def zeroStability(self,iPlayer): #Called by RiseAndFall Resurrection
		pPlayer = gc.getPlayer( iPlayer )
		for iCath in range( 4 ):
			pPlayer.changeStabilityBase( iCath, - pPlayer.getStabilityBase( iCath ) )
			pPlayer.setStabilityVary( iCath, 0 )
		pPlayer.setStabilitySwing( 0 )


	def checkTurn(self, iGameTurn):
		#print "3Miro NewStability Check Turn"
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

		if (iGameTurn == 0):
			self.recalcEpansion( gc.getPlayer(con.iByzantium) )


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
			self.recalcEpansion(pPlayer)
			iNumCities = pPlayer.getNumCities()
			if ( iPlayer != con.iPrussia ):
				if ( pPlayer.isHuman() ):
					pPlayer.changeStabilityBase( iCathegoryCivics, max( -2, -iNumCities / 4 ) ) # 0 with 1-2 cities, -1 with 3-6 cities, -2 with at least 7 cities
				else:
					pPlayer.changeStabilityBase( iCathegoryCivics, max( -1, -iNumCities / 4 ) ) # the AI is largely unaware of Stability issues

			if ( iPlayer != con.iPrussia ):
				pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() - 8  )

		if ( pPlayer.getWarPeaceChange() == -1 ): # Whenever your nation switches from peace to the state of war (with a major nation)
			gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryCities, -1 ) # 1 permanent stability loss, since your people won't appreciate leaving the state of peace
			pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() - 3  )

		if ( (iGameTurn + iPlayer) % 3 == 0 ): # Economy Check every 3 turns
			self.recalcEconomy( pPlayer )

		self.recalcCity( iPlayer ) # update city stability

		# Collapse dates for AI nations - from RFCE++
		if(iGameTurn > con.tCollapse[iPlayer] and iPlayer != utils.getHumanID() and pPlayer.isAlive()):
			# -1 stability every 4 turns up to a total of -15 stability
			if(iGameTurn % 4 == 0 and iGameTurn <= con.tCollapse[iPlayer]+4*15):
				pPlayer.changeStabilityBase(iCathegoryCities, -1)

		#if ( iGameTurn % 6 == 1 ):
		#	self.printStability( iGameTurn, iPlayer )


	def continentsNormalization(self, iGameTurn): #Sedna17
		#lContinentModifier = [-1, -1, 0, -2, 0, 0] #Eastern, Central, Atlantic, Islamic, Italian, Norse, see Consts.py
		#for iPlayer in range(iNumPlayers):
		#       if (gc.getPlayer(iPlayer).isAlive()):
		#		for j in range(len(con.lCivStabilityGroups)):
		#			if (iPlayer in con.lCivStabilityGroups[j]):
		#				self.setParameter(iPlayer, iParExpansionE, True, lContinentModifier[j])
		#				self.setStability(iPlayer, (self.getStability(iPlayer) + lContinentModifier[j]))
		pass


	def onCityBuilt(self, iPlayer, x, y):
		iProv = rfcemaps.tProinceMap[y][x]
		pPlayer = gc.getPlayer( iPlayer )
		if ( pPlayer.getProvinceType( iProv ) >= con.iProvinceNatural ):
			pPlayer.changeStabilityBase( iCathegoryExpansion, 1 )
		elif ( not gc.hasUP( iPlayer, con.iUP_StabilitySettler ) ):
			pPlayer.changeStabilityBase( iCathegoryExpansion, -2 )
		if ( pPlayer.getNumCities() < 5 ): # early boost to small Empires
			pPlayer.changeStabilityBase( iCathegoryExpansion, 1 )
		self.recalcEpansion( pPlayer )
		self.recalcCivicCombos( iPlayer )


	def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
		if (city.hasBuilding(xml.iEscorial)):
			gc.getPlayer( playerType ).setPicklefreeParameter( con.iIsHasEscorial, 1 )
			gc.getPlayer( owner ).setPicklefreeParameter( con.iIsHasEscorial, 0 )
		if (city.hasBuilding(xml.iStephansdom)):
			gc.getPlayer( playerType ).setPicklefreeParameter( con.iIsHasStephansdom, 1 )
			gc.getPlayer( owner ).setPicklefreeParameter( con.iIsHasStephansdom, 0 )
		self.recalcCivicCombos(playerType)
		self.recalcCivicCombos(owner)
		iProv = city.getProvince()
		pOwner = gc.getPlayer( owner )
		pConq = gc.getPlayer( playerType )
		iProvOwnerType = pOwner.getProvinceType( iProv )
		iProvConqType = pConq.getProvinceType( iProv )
		if ( iProvOwnerType >= con.iProvinceNatural ):
			if( owner == con.iScotland ): #Scotland UP part 2
				pOwner.changeStabilityBase( iCathegoryExpansion, -2 )
				pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 2 )
			else:
				pOwner.changeStabilityBase( iCathegoryExpansion, -3 )
				pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 4 )
		if ( iProvOwnerType < con.iProvinceNatural ):
			if( owner == con.iScotland ): #Scotland UP part 2
				pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 1 )
			else:
				pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 2 )
		if ( iProvConqType >= con.iProvinceNatural ):
			pConq.changeStabilityBase( iCathegoryExpansion, 1 )
			pConq.setStabilitySwing( pConq.getStabilitySwing() + 3 )
		if ( pConq.getCivics(5) == 28 ):
			pConq.changeStabilityBase( iCathegoryExpansion, 1 )
		if (owner < iNumPlayers and city.getX() == tCapitals[owner][0] and city.getY() == tCapitals[owner][1]):
			if( owner == con.iScotland ): #Scotland UP part 2
				pOwner.changeStabilityBase( iCathegoryExpansion, -5 )
				pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 5 )
			else:
				pOwner.changeStabilityBase( iCathegoryExpansion, -10 )
				pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 10 )
				if ( gc.hasUP(owner,con.iUP_Emperor) ): # If Byzantium loses Constantinople, they should collapse
					pOwner.changeStabilityBase( iCathegoryExpansion, -10 )
					pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 10 )
		self.recalcEpansion( pOwner )
		self.recalcEpansion( pConq )


	def onCityRazed(self, iOwner, playerType, city):
		#Sedna17: Not sure what difference between iOwner and playerType is here
		#3Miro: iOwner owns the city (victim) and I think playerType is the one razing the city
		#		On second thought, if iOwner (the previous owner) doesn't have enough culture, then iOwner == playerType
		#AbsintheRed: The question of razing is after the conquest of the city. This means iOwner is the conqueror.
		#			Thus, if 3Miro is right, and playerType is the one razing the city, then: iOwner == playerType in all cases
		if (city.hasBuilding(xml.iEscorial)):
			gc.getPlayer( playerType ).setPicklefreeParameter( con.iIsHasEscorial, 0 )
			gc.getPlayer( iOwner ).setPicklefreeParameter( con.iIsHasEscorial, 0 )
		if (city.hasBuilding(xml.iStephansdom)):
			gc.getPlayer( playerType ).setPicklefreeParameter( con.iIsHasStephansdom, 0 )
			gc.getPlayer( iOwner ).setPicklefreeParameter( con.iIsHasStephansdom, 0 )
		self.recalcCivicCombos(playerType)

		#AbsintheRed: -1 for everyone, additional -1 if not Norway:
		if ( playerType != con.iNorway ):
			gc.getPlayer( playerType ).changeStabilityBase( iCathegoryExpansion, -1 )
		if ( iOwner == playerType ):
			gc.getPlayer( iOwner ).changeStabilityBase( iCathegoryExpansion, -1 )
		self.recalcEpansion( gc.getPlayer( playerType ) )

				#if city.getPopulation()


	def onImprovementDestroyed(self, owner):
		pPlayer = gc.getPlayer( owner )
		pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() - 2 )


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
		elif ( iBuilding == xml.iNightWatch or iBuilding == xml.iSwedishTennant):
			gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryCivics, 1 )
		elif ( iBuilding == xml.iCourthouse or iBuilding == xml.iHolyRomanRathaus or iBuilding == xml.iKievVeche or iBuilding == xml.iLithuanianVoivodeship ):
			gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryCities, 1 )
		elif (iBuilding == xml.iEscorial):
			gc.getPlayer( iPlayer ).setPicklefreeParameter( con.iIsHasEscorial, 1 )
		elif (iBuilding == xml.iStephansdom):
			gc.getPlayer( iPlayer ).setPicklefreeParameter( con.iIsHasStephansdom, 1 )
		elif (iBuilding == xml.iPalace):
			#print(" Capital Changed",iPlayer)
			pPlayer= gc.getPlayer( iPlayer )
			pPlayer.changeStabilityBase( iCathegoryExpansion, -3 )
			pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() -5  )


	def onProjectBuilt(self, iPlayer, iProject):
		pPlayer = gc.getPlayer(iPlayer)
		iCivic5 = pPlayer.getCivics(5)
		if (iProject >= xml.iNumNotColonies):
			pPlayer.changeStabilityBase( iCathegoryExpansion, -2 ) # -2 stability for each colony
			if (iCivic5 == 29):
				pPlayer.changeStabilityBase( iCathegoryExpansion, 1 ) # one less stability penalty if civ is in Colonialism
		self.recalcEpansion( pPlayer )


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
		#	pPlayer = gc.getPlayer(iPlayer)
		#	if (pPlayer.getStateReligion() != iReligion):
		#		for iLoopCiv in range(iNumPlayers):
		#			if (gc.getTeam(pPlayer.getTeam()).isAtWar(iLoopCiv)):
		#				if (gc.getPlayer(iLoopCiv).getStateReligion() == iReligion):
		#					self.setStability(iPlayer, self.getStability(iPlayer) - 1 )
		#					self.setParameter(iPlayer, iParCitiesE, True, -1)
		#					print("Stability - onReligionSpread - Target = ", iPlayer, "Cause = ", iLoopCiv, "Religion = ",iReligion)
		#					break


	def checkImplosion(self, iGameTurn):
		if (iGameTurn > 10 and iGameTurn % 8 == 5):
			for iPlayer in range(iNumPlayers):
				pPlayer = gc.getPlayer(iPlayer)
				if (pPlayer.isAlive() and iGameTurn >= con.tBirth[iPlayer] + 25):
					# 3MiroUP: Emperor
					if (pPlayer.getStability() < -15 and pPlayer.getNumCities() > 9 and (not utils.collapseImmune(iPlayer))): #civil war
						print ("COLLAPSE: CIVIL WAR", gc.getPlayer(iPlayer).getCivilizationAdjective(0))
						if (iPlayer != utils.getHumanID()):
							if (gc.getPlayer(utils.getHumanID()).canContact(iPlayer)):
								CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, gc.getPlayer(iPlayer).getCivilizationDescription(0) + " " + CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
							#if (iGameTurn < xml.i1000AD):
							# 3Miro: fragments to indeps and barbs, after some year just indeps
							#utils.killAndFragmentCiv(iPlayer, iIndependent, iIndependent2, -1, False)
							utils.killAndFragmentCiv(iPlayer, False, False)
						else:
							if (pPlayer.getNumCities() > 1):
								CyInterface().addMessage(iPlayer, True, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
								#utils.killAndFragmentCiv(iPlayer, iIndependent, iIndependent2, -1, True)
								utils.killAndFragmentCiv(iPlayer, False, True)
								#self.setStability(iPlayer, -15)
								self.zeroStability( iPlayer )
								pPlayer.changeStabilityBase( iCathegoryExpansion, -3 )


	def printStability(self, iGameTurn, iPlayer ):
		cyPlayer = PyHelpers.PyPlayer(iPlayer)
		pPlayer = gc.getPlayer( iPlayer )
		print(" Turn: ",iGameTurn)
		print " ---------------- New Stability For " + cyPlayer.getCivilizationShortDescription()
		print("                  Stability : ",pPlayer.getStability() )
		print("                  Cities    : ",pPlayer.getStabilityBase( iCathegoryCities ) + pPlayer.getStabilityVary( iCathegoryCities ))
		print("                  Civics    : ",pPlayer.getStabilityBase( iCathegoryCivics ) + pPlayer.getStabilityVary( iCathegoryCivics ))
		print("                  Economy   : ",pPlayer.getStabilityBase( iCathegoryEconomy ) + pPlayer.getStabilityVary( iCathegoryEconomy ) )
		print("                  Expansion : ",pPlayer.getStabilityBase( iCathegoryExpansion ) + pPlayer.getStabilityVary( iCathegoryExpansion ) )
		print("                  Swing     : ",pPlayer.getStabilitySwing() )


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
			iCityStability += max( iMilitaryStability + iWarWStability, -2 )
			iCityStability = min( max( iCityStability, -6 ), 8 )
		else:
			iCityStability += max( iHappyStability, -2 ) + iHealthStability # AI keeps very unhappy cities
			iCityStability += max( iReligionStability + iHurryStability, -3 ) + max( iCultureStability, -3 )
			iCityStability = min( max( iCityStability, -5 ), 5 )
		iCityStability += pPlayer.getFaithBenefit( con.iFP_Stability )
		#print(" City Stability for: ",iPlayer," Caths: ",iHappyStability,iHealthStability,iHurryStability,iMilitaryStability,iWarWStability,iReligionStability,iCultureStability)
		if ( pPlayer.getGoldenAgeTurns() > 0 ):
			iCityStability += 8

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
		if (iCivic0 == xml.iCivicMerchantRepublic):
			if (iCivic1 == xml.iCivicFeudalLaw): #Incompatible with Feudal Law (Venice likes this one)
				iCivicCombo -= 4
			if (iCivic3 == xml.iCivicTradeEconomy):
				iCivicCombo += 3
		if (iCivic0 == xml.iCivicDivineMonarchy): #Divine Monarchy should have an appropriate religious civic
			if (iCivic4 == xml.iCivicPaganism): #Paganism
				iCivicCombo -=4
			elif (iCivic4 == xml.iCivicTheocracy): #Theocracy
				iCivicCombo +=3
			elif (iCivic4 == xml.iCivicStateReligion): #State Religion
				iCivicCombo +=2
			elif (iCivic4 == xml.iCivicOrganizedReligion): #State Religion
				iCivicCombo +=2
			elif (iCivic4 == xml.iCivicFreeReligion): #Free Religion
				iCivicCombo -=5
			if (iCivic1 == xml.iCivicReligiousLaw): #Religious Law
				iCivicCombo +=2
		if ( pPlayer.getPicklefreeParameter( con.iIsHasStephansdom ) == 1 ):
			#if (self.getHasStephansdom(iPlayer) == 1):
			if (iCivic0 in ( xml.iCivicFeudalMonarchy, xml.iCivicDivineMonarchy, xml.iCivicLimitedMonarchy) ):
					iCivicCombo +=2
		if (iCivic0 == xml.iCivicLimitedMonarchy or iCivic0 == xml.iCivicMerchantRepublic): #Limited Monarchy and Republics both like enlightened civics
			if (iCivic1 == xml.iCivicCommonLaw): #Common Law
				iCivicCombo +=3
			if (iCivic2 == xml.iCivicFreePeasantry or iCivic2 == xml.iCivicFreeLabor): #Free Peasantry or free labor
				iCivicCombo +=3
		if (iCivic1 == xml.iCivicFeudalLaw): #Feudal law works well with...
			if (iCivic2 == xml.iCivicSerfdom): # Serfdom
				iCivicCombo +=1
			elif (iCivic2 == xml.iCivicFreePeasantry): #but poorly with uppity free peasants
				iCivicCombo -=4
			if (iCivic3 == xml.iCivicManorialism): #Manorialism
				iCivicCombo +=1
			if (iCivic0 == xml.iCivicFeudalMonarchy ):
				iCivicCombo +=1
		if (iCivic2 == xml.iCivicSerfdom and iCivic3 == xml.iCivicManorialism): #Serfdom and Manorialism go together
			iCivicCombo +=2
		if (iCivic1 == xml.iCivicReligiousLaw): #Religious Law
			if (iCivic4 == xml.iCivicPaganism or iCivic4 == xml.iCivicFreeReligion): #Dislikes Paganism or Free Religion
				iCivicCombo -=5
			elif (iCivic4 == xml.iCivicTheocracy): #Favors theocracy
				iCivicCombo +=3
		if (iCivic1 == xml.iCivicCommonLaw): #Common Law
			if (iCivic2 == xml.iCivicFreeLabor): #likes Free labor
				iCivicCombo +=3
			if (iCivic4 == xml.iCivicTheocracy): #dislikes theocracy
				iCivicCombo -=4
		if (iCivic2 == xml.iCivicApprenticeship and iCivic3 == xml.iCivicGuilds): #Apprenticeship and Guilds
			iCivicCombo +=3
		if (iCivic1 == xml.iCivicBureaucracy): #Bureaucracy
			if ( pPlayer.isHuman() ):
				iCivicCombo += max( -4, 5 - pPlayer.getNumCities() )
			else:
				iCivicCombo += max( -2, 5 - pPlayer.getNumCities() )
		if (iCivic0 == xml.iCivicMerchantRepublic): #Merchant Republic city cap (like Republic from RFC)
			if ( pPlayer.isHuman() ):
				iCivicCombo += max( -3, 4 - pPlayer.getNumCities() )
			else:
				iCivicCombo += max( -1, 4 - pPlayer.getNumCities() )
		# TODO: boost for stability depending on the current stability
		#if (iCivic0 == 2): #Divine Monarchy
		#	if (self.getStability(iPlayer) > 30):
		#		iCivicCombo += 5
		#if (iCivic0 == 3): #Limited Monarchy
		#	if (self.getStability(iPlayer) < -60):
		#		iCivicCombo += 5
		#if (iCivic0 == 4): #Republic
		#	if (self.getStability(iPlayer) > 50):
		#		iCivicCombo += 10
		#szShortName = pPlayer.getCivilizationShortDescription()
		#print(" Civic Combo for ",iPlayer,"   is ",iCivicCombo)
		#print("       Civics  ",iCivic0,"  ",iCivic1,"  ",iCivic2,"  ",iCivic3,"  ",iCivic4)
		pPlayer.setStabilityVary( iCathegoryCivics, iCivicCombo)


	def recalcEconomy(self, pPlayer):
		iPopNum = pPlayer.getTotalPopulation()
		iNumCities = pPlayer.getNumCities()
		iImports = pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
		iExports = pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
		if ( pPlayer.getID() == con.iCordoba ):
			iImports /= 2
			iExports /= 2
		iFinances = pPlayer.getFinancialPower()
		iInflation = pPlayer.calculateInflatedCosts()
		iProduction = pPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
		if ( pPlayer.getID() == con.iVenecia ):
			iProduction += iPopNum # offset their weak production
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
		#print(" Civilization: ",pPlayer.getID(),"  ",iFinancialStability,iIndustrialStability )
		pPlayer.setStabilityVary( iCathegoryEconomy, iFinancialStability + iIndustrialStability )


	def recalcEpansion( self, pPlayer ):
		apCityList = PyPlayer(pPlayer.getID()).getCityList()
		iExpStability = 0
		iCivic5 = pPlayer.getCivics(5)
		bIsUPLandStability = gc.hasUP( pPlayer.getID(), con.iUP_LandStability )
		iCivicBonus = 0
		iUPBonus = 0
		for pLoopCity in apCityList:
			pCity = pLoopCity.GetCy()
			iProvType = pPlayer.getProvinceType( pCity.getProvince() )
			iExpStability += tStabilityPenalty[ iProvType ]
			if ( iProvType <= con.iProvinceOuter ):
				if ( iCivic5 == xml.iCivicImperialism ): # Imperialism
					iCivicBonus += 1
				if ( bIsUPLandStability ): # French UP
					iUPBonus += 1
		iExpStability += min( 12, iCivicBonus ) # Imperialism
		iExpStability += min( 6, iUPBonus ) # French UP
		if ( not (pPlayer.getCivics(5) == xml.iCivicOccupation) ):
			iExpStability -= 3 * pPlayer.getForeignCitiesInMyProvinceType( con.iProvinceCore ) # -3 stability for each foreign/enemy city in your core provinces, without the Militarism civic
			iExpStability -= 1 * pPlayer.getForeignCitiesInMyProvinceType( con.iProvinceNatural ) # -1 stability for each foreign/enemy city in your natural provinces, without the Militarism civic
		if ( pPlayer.getMaster() > -1 ):
			iExpStability += 8
		if ( iCivic5 == xml.iCivicVassalage ):
			iExpStability += 3*pPlayer.countVassals()
		else:
			iExpStability += pPlayer.countVassals()
		iNumCities = pPlayer.getNumCities()
		iPlayer = pPlayer.getID()
		if ( iPlayer == con.iTurkey or iPlayer == con.iMoscow ): # five free cities for those two
			iNumCities = max( 0, iNumCities - 5 )
		iExpStability -= iNumCities*iNumCities / 40
		if ( pPlayer.getID() == con.iTurkey and pPlayer.getStability() < 1 and gc.getGame().getGameTurn() < xml.i1570AD ): # boost Turkey before the battle of Lepanto
			if ( not pPlayer.isHuman() ):
				iExpStability += min( 3 - pPlayer.getStability(), 6 )
		if ( pPlayer.getID() == con.iVenecia and pPlayer.getStability() < 1 and gc.getGame().getGameTurn() < xml.i1204AD ): # Venice has trouble early on due to its civics
			if ( not pPlayer.isHuman() ):
				iExpStability += 4
		pPlayer.setStabilityVary( iCathegoryExpansion, iExpStability )

