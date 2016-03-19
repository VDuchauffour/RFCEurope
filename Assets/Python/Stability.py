# Rhye's and Fall of Civilization - Stability

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
#import cPickle as pickle
import Consts as con
import XMLConsts as xml
import RFCUtils
import RFCEMaps as rfcemaps
import RiseAndFall

utils = RFCUtils.RFCUtils()
rnf = RiseAndFall.RiseAndFall()

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

tStabilityPenalty = ( -5, -2, 0, 0, 0 )

class Stability:

	def setup(self): # Sets human starting stability
		for iPlayer in range( iNumMajorPlayers ):
			pPlayer = gc.getPlayer( iPlayer )
			for iCath in range( 4 ):
				pPlayer.changeStabilityBase( iCath, - pPlayer.getStabilityBase( iCath ) )
				pPlayer.setStabilityVary( iCath, 0 )
			pPlayer.setStabilitySwing( 0 )
		#if ( not gc.getPlayer( con.iFrankia ).isHuman() ):
		#	gc.getPlayer( con.iFrankia ).changeStabilityBase( iCathegoryExpansion, 5 ) # so that they don't collapse from the cities they lose to everyone
		#if ( not gc.getPlayer( con.iVenecia ).isHuman() ):
		#	gc.getPlayer( con.iVenecia ).changeStabilityBase( iCathegoryExpansion, 4 ) # they collapse too often
		#if ( gc.getPlayer( con.iDenmark ).isHuman() ):
		#	gc.getPlayer( con.iDenmark ).changeStabilityBase( iCathegoryExpansion, 2 ) # too many border provinces to conquer in short time
		iHandicap = gc.getGame().getHandicapType()
		if (iHandicap == 0):
			gc.getPlayer( utils.getHumanID() ).changeStabilityBase( iCathegoryExpansion, 6 )
		elif (iHandicap == 1):
			gc.getPlayer( utils.getHumanID() ).changeStabilityBase( iCathegoryExpansion, 2 )

		# Absinthe: Stability is accounted properly for stuff preplaced in the scenario file - from RFCE++
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
				if ( iCounter < 5 ): # early boost to small civs
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
			if ( iPlayer != con.iPrussia ): # Absinthe: Prussian UP
				if ( pPlayer.isHuman() ):
					pPlayer.changeStabilityBase( iCathegoryCivics, min( 0, max( -2, (-iNumCities+3) / 6 ) ) ) # 0 with 1-3 cities, -1 with 4-9 cities, -2 with at least 10 cities
				else:
					pPlayer.changeStabilityBase( iCathegoryCivics, min( 0, max( -1, (-iNumCities+3) / 6 ) ) ) # the AI is largely unaware of Stability issues

			if ( iPlayer != con.iPrussia ): # Absinthe: Prussian UP
				pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() - 8  )

		if ( pPlayer.getWarPeaceChange() == -1 ): # Whenever your nation switches from peace to the state of war (with a major nation)
			gc.getPlayer( iPlayer ).changeStabilityBase( iCathegoryCities, -1 ) # 1 permanent stability loss, since your people won't appreciate leaving the state of peace
			pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() - 3  )

		if ( (iGameTurn + iPlayer) % 3 == 0 ): # Economy Check every 3 turns
			self.recalcEconomy( pPlayer )

		self.recalcCity( iPlayer ) # update city stability

		# # Absinthe: Collapse dates for AI nations
		if(iGameTurn > con.tCollapse[iPlayer] and iPlayer != utils.getHumanID() and pPlayer.isAlive()):
			# Absinthe: -1 stability every 4 turns up to a total of -15 stability
			if(iGameTurn % 4 == 0 and iGameTurn <= con.tCollapse[iPlayer] + 60):
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
		elif ( pPlayer.getProvinceType( iProv ) == con.iProvincePotential ):
			pPlayer.changeStabilityBase( iCathegoryExpansion, 0 )
		elif ( not gc.hasUP( iPlayer, con.iUP_StabilitySettler ) ):
			pPlayer.changeStabilityBase( iCathegoryExpansion, -2 )
		if ( pPlayer.getNumCities() < 5 ): # early boost to small Empires
			pPlayer.changeStabilityBase( iCathegoryExpansion, 1 )
		self.recalcEpansion( pPlayer )
		self.recalcCivicCombos( iPlayer )


	def onCityAcquired(self, owner, playerType, city, bConquest, bTrade):
		pOwner = gc.getPlayer( owner )
		pConq = gc.getPlayer( playerType )
		if (city.hasBuilding(xml.iEscorial)):
			pConq.setPicklefreeParameter( con.iIsHasEscorial, 1 )
			pOwner.setPicklefreeParameter( con.iIsHasEscorial, 0 )
		if (city.hasBuilding(xml.iStephansdom)):
			pConq.setPicklefreeParameter( con.iIsHasStephansdom, 1 )
			pOwner.setPicklefreeParameter( con.iIsHasStephansdom, 0 )
		self.recalcCivicCombos(playerType)
		self.recalcCivicCombos(owner)
		iProv = city.getProvince()
		iProvOwnerType = pOwner.getProvinceType( iProv )
		iProvConqType = pConq.getProvinceType( iProv )
		if ( iProvOwnerType >= con.iProvinceNatural ):
			if( owner == con.iScotland ): #Scotland UP part 2
				pOwner.changeStabilityBase( iCathegoryExpansion, -2 )
				pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 2 )
			else:
				pOwner.changeStabilityBase( iCathegoryExpansion, -3 )
				pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 4 )
		elif ( iProvOwnerType < con.iProvinceNatural ):
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
			elif ( gc.hasUP(owner,con.iUP_Emperor) ): # If Byzantium loses Constantinople, they should lose all non-core cities
				pOwner.changeStabilityBase( iCathegoryExpansion, -20 )
				pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 20 )
			else:
				pOwner.changeStabilityBase( iCathegoryExpansion, -10 )
				pOwner.setStabilitySwing( pOwner.getStabilitySwing() - 10 )
		self.recalcEpansion( pOwner )
		self.recalcEpansion( pConq )


	def onCityRazed(self, iOwner, playerType, city):
		#Sedna17: Not sure what difference between iOwner and playerType is here
		#3Miro: iOwner owns the city (victim) and I think playerType is the one razing the city
		#		On second thought, if iOwner (the previous owner) doesn't have enough culture, then iOwner == playerType
		#AbsintheRed: playerType is the one razing city, iOwner is the previous owner of the city (apart from playerType)
		pPlayer = gc.getPlayer( playerType )
		pOwner = gc.getPlayer( iOwner )
		if (city.hasBuilding(xml.iEscorial)):
			pPlayer.setPicklefreeParameter( con.iIsHasEscorial, 1 )
			pOwner.setPicklefreeParameter( con.iIsHasEscorial, 0 )
		if (city.hasBuilding(xml.iStephansdom)):
			pPlayer.setPicklefreeParameter( con.iIsHasStephansdom, 1 )
			pOwner.setPicklefreeParameter( con.iIsHasStephansdom, 0 )
		self.recalcCivicCombos(playerType)
		self.recalcCivicCombos(iOwner)

		# Absinthe: new city razing penalties
		# permanent, based on city population
		iRazeStab = 0
		if (city.getPopulation() > 9):
			iRazeStab = 3
		elif (city.getPopulation() > 5):
			iRazeStab = 2
		elif (city.getPopulation() > 2):
			iRazeStab = 1
		# Absinthe: Norwegian UP - one less stability penalty
		if ( playerType == con.iNorway ):
			iRazeStab -= 1
		if (iRazeStab > 0):
			pPlayer.changeStabilityBase( iCathegoryExpansion, -iRazeStab )
		# temporary, 3 for everyone but Norway
		if ( playerType != con.iNorway ):
			pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() - 3 )
		self.recalcEpansion( pPlayer )


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
		pPlayer = gc.getPlayer( iPlayer )
		if ( iBuilding == xml.iManorHouse or iBuilding == xml.iFrenchChateau):
			pPlayer.changeStabilityBase( iCathegoryEconomy, 1 )
			self.recalcEconomy( pPlayer )
		elif ( iBuilding == xml.iCastle or iBuilding == xml.iMoscowKremlin or iBuilding == xml.iHungarianStronghold or iBuilding == xml.iSpanishCitadel):
			pPlayer.changeStabilityBase( iCathegoryExpansion, 1 )
			self.recalcEpansion( pPlayer )
		elif ( iBuilding == xml.iNightWatch or iBuilding == xml.iSwedishTennant):
			pPlayer.changeStabilityBase( iCathegoryCivics, 1 )
			self.recalcCivicCombos( iPlayer )
		elif ( iBuilding == xml.iCourthouse or iBuilding == xml.iHolyRomanRathaus or iBuilding == xml.iKievVeche or iBuilding == xml.iLithuanianVoivodeship ):
			pPlayer.changeStabilityBase( iCathegoryCities, 1 )
			self.recalcCity( iPlayer )
		elif (iBuilding == xml.iEscorial):
			pPlayer.setPicklefreeParameter( con.iIsHasEscorial, 1 )
		elif (iBuilding == xml.iStephansdom):
			pPlayer.setPicklefreeParameter( con.iIsHasStephansdom, 1 )
		elif (iBuilding == xml.iPalace):
			pPlayer.changeStabilityBase( iCathegoryExpansion, -2 )
			pPlayer.setStabilitySwing( pPlayer.getStabilitySwing() -5  )
			self.recalcEpansion( pPlayer )


	def onProjectBuilt(self, iPlayer, iProject):
		pPlayer = gc.getPlayer(iPlayer)
		iCivic5 = pPlayer.getCivics(5)
		if (iProject >= xml.iNumNotColonies):
			pPlayer.changeStabilityBase( iCathegoryExpansion, -2 ) # -2 stability for each colony
			if (iCivic5 == xml.iCivicColonialism):
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
		if (iGameTurn > 10 and iGameTurn % 6 == 3):
			for iPlayer in range(iNumPlayers - 1):
				pPlayer = gc.getPlayer(iPlayer)
				if (pPlayer.isAlive() and iGameTurn >= con.tBirth[iPlayer] + 10):
					# Absinthe: if stability is less than -3, there is a chance that the secession/revolt or collapse mechanics start
					#			if more than 8 cities: high chance for secession mechanics, low chance for collapse
					#			elif more than 4 cities: medium chance for collapse mechanics, medium chance for secession
					#			otherwise big chance for collapse mechanics
					#			the actual chance for both secession/revolt and total collapse is increasing with lower stability
					iStability = pPlayer.getStability()
					if (iStability < -3):
						if (pPlayer.getNumCities() > 8):
							if (gc.getGame().getSorenRandNum(10, 'city secession') < 8): #80 chance for secession start
								if (gc.getGame().getSorenRandNum(10, 'city secession') < -3 - iStability): #10% at -4, increasing by 10% with each point (100% with -13 or less)
									rnf.revoltCity( iPlayer, False )
							elif (gc.getGame().getSorenRandNum(10, 'civ collapse') < 1 and iGameTurn >= con.tBirth[iPlayer] + 20): #10 chance for collapse start
								if (gc.getGame().getSorenRandNum(10, 'civ collapse') < -1.5 - (iStability/2)): #10% at -4, increasing by 10% with 2 points (100% with -22 or less)
									print ("COLLAPSE: CIVIL WAR", gc.getPlayer(iPlayer).getCivilizationAdjective(0))
									if (iPlayer != utils.getHumanID()):
										if (gc.getPlayer(utils.getHumanID()).canContact(iPlayer)):
											CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, gc.getPlayer(iPlayer).getCivilizationDescription(0) + " " + CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
										utils.killAndFragmentCiv(iPlayer, False, False)
									elif (pPlayer.getNumCities() > 1):
										CyInterface().addMessage(iPlayer, True, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
										utils.killAndFragmentCiv(iPlayer, False, True)
										self.zeroStability( iPlayer )
						elif (pPlayer.getNumCities() > 4):
							if (gc.getGame().getSorenRandNum(10, 'city secession') < 4): #40 chance for secession start
								if (gc.getGame().getSorenRandNum(10, 'city secession') < -3 - iStability): #10% at -4, increasing by 10% with each point (100% with -13 or less)
									rnf.revoltCity( iPlayer, False )
							elif (gc.getGame().getSorenRandNum(10, 'civ collapse') < 4 and iGameTurn >= con.tBirth[iPlayer] + 20): #40 chance for collapse start
								if (gc.getGame().getSorenRandNum(10, 'civ collapse') < -1.5 - (iStability/2)): #10% at -4, increasing by 10% with 2 points (100% with -22 or less)
									print ("COLLAPSE: CIVIL WAR", gc.getPlayer(iPlayer).getCivilizationAdjective(0))
									if (iPlayer != utils.getHumanID()):
										if (gc.getPlayer(utils.getHumanID()).canContact(iPlayer)):
											CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, gc.getPlayer(iPlayer).getCivilizationDescription(0) + " " + CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
										utils.killAndFragmentCiv(iPlayer, False, False)
									elif (pPlayer.getNumCities() > 1):
										CyInterface().addMessage(iPlayer, True, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
										utils.killAndFragmentCiv(iPlayer, False, True)
										self.zeroStability( iPlayer )
						elif (gc.getGame().getSorenRandNum(10, 'civ collapse') < 7  and iGameTurn >= con.tBirth[iPlayer] + 20): #70 chance for collapse start
							if (gc.getGame().getSorenRandNum(10, 'civ collapse') < -1.5 - (iStability/2)): #10% at -4, increasing by 10% with 2 points (100% with -22 or less)
								print ("COLLAPSE: CIVIL WAR", gc.getPlayer(iPlayer).getCivilizationAdjective(0))
								if (iPlayer != utils.getHumanID()):
									if (gc.getPlayer(utils.getHumanID()).canContact(iPlayer)):
										CyInterface().addMessage(utils.getHumanID(), False, con.iDuration, gc.getPlayer(iPlayer).getCivilizationDescription(0) + " " + CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
									utils.killAndFragmentCiv(iPlayer, False, False)
								elif (pPlayer.getNumCities() > 1):
									CyInterface().addMessage(iPlayer, True, con.iDuration, CyTranslator().getText("TXT_KEY_STABILITY_CIVILWAR_HUMAN", ()), "", 0, "", ColorTypes(con.iRed), -1, -1, True, True)
									utils.killAndFragmentCiv(iPlayer, False, True)
									self.zeroStability( iPlayer )


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


	def zeroStability(self,iPlayer): #Called by Stability.CheckImplosion
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
		if ( pPlayer.getNumCities() == 0 ):
			iHappyStability = 0
		else:
			iHappyStability = max( (iTotalHappy / pPlayer.getNumCities() - 1)/2, 0 ) # +k stability for an average city happiness of at least 2k+1
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
			# Absinthe: getWarWearinessPercentAnger is not a local variable for your cities, but a global one for your entire civ
			#			thus it results in 1 instability for each city, if there is an ongoing war
			if ( pCity.getWarWearinessPercentAnger() > 10 ):
				iWarWStability -= 1
			#print(" getWarWearinessPercentAnger_city: ",pCity.getWarWearinessPercentAnger())
			#print(" getWarWearinessPercentAnger_player: ",pPlayer.getWarWearinessPercentAnger())
			if ( iCivic4 != 24 ): # if not a Free religion
				if ( ( not gc.hasUP( iPlayer, con.iUP_ReligiousTolerance )) and pCity.getNumForeignReligions() > 0 ):
					if ( iCivic4 == 20 ): # pagans are a bit more tolerant
						iReligionStability -= 1
					else:
						iReligionStability -= 2
			#print(" iReligionStability: ",iReligionStability)
			# Absinthe: -1 stability if own culture is less than 40% of total culture in a city, -2 stability if less than 20%
			iTotalCulture = pCity.countTotalCultureTimes100()
			if ( (iTotalCulture > 0) and ( (pCity.getCulture(iPlayer) * 10000) / iTotalCulture < 40 ) and ( not gc.hasUP( iPlayer, con.iUP_CulturalTolerance )) ):
				iCultureStability -= 1
				if ( (iTotalCulture > 0) and ( (pCity.getCulture(iPlayer) * 10000) / iTotalCulture < 20 ) and ( not gc.hasUP( iPlayer, con.iUP_CulturalTolerance )) ):
					iCultureStability -= 1
			#print(" iCultureStability: ",iCultureStability)
		# Absinthe: persecution counter - cooldown is handled in Religions.checkTurn
		#			1-3 means 1 instability, 4-6 means 2 instability, 7-9 means 3 instability, etc...
		iProsecutionCount = pPlayer.getProsecutionCount()
		if ( iProsecutionCount > 0 ):
			iReligionStability -= (iProsecutionCount + 2) / 3
		# Humans are far more competent then the AI, so the AI won't get all the penalties
		if ( pPlayer.isHuman() ):
			iCityStability += iHappyStability + iHealthStability + iReligionStability + iHurryStability + iCultureStability + iMilitaryStability
			iCityStability += max( iWarWStability/3 - 1, -10 ) # max 10 instability from war weariness
			iCityStability = min( iCityStability, 8 ) # max 8 extra stability from cities - don't want to add too many bonuses for runaway civs
		else:
			iCityStability += max( iHappyStability, -3 ) + iHealthStability # AI keeps very unhappy cities
			iCityStability += max( iReligionStability + iHurryStability, -7 ) + max( iCultureStability, -3 )
			iCityStability += max( iMilitaryStability + iWarWStability/3, -3 ) # AI is also bad at handling war weariness
			iCityStability = min( max( iCityStability, -10 ), 8 )
		iCityStability += pPlayer.getFaithBenefit( con.iFP_Stability )
		#print(" City Stability for: ",iPlayer," Categories: ",iHappyStability,iHealthStability,iHurryStability,iMilitaryStability,iWarWStability,iReligionStability,iCultureStability)
		if ( pPlayer.getGoldenAgeTurns() > 0 ):
			iCityStability += 8

		pPlayer.setStabilityVary( iCathegoryCities, iCityStability)


	def recalcCivicCombos(self, iPlayer):
		# Note from 3Miro: this is the only place Civics are referenced, yet referring them by number makes this hard to read
		pPlayer = gc.getPlayer(iPlayer)
		iCivicGovernment = pPlayer.getCivics(0)
		iCivicLegal = pPlayer.getCivics(1)
		iCivicLabor = pPlayer.getCivics(2)
		iCivicEconomy = pPlayer.getCivics(3)
		iCivicReligion = pPlayer.getCivics(4)
		iCivicExpansion = pPlayer.getCivics(5)

		lCivics = [iCivicGovernment, iCivicLegal, iCivicLabor, iCivicEconomy, iCivicReligion, iCivicExpansion]
		lCombinations = [(iCivic1, iCivic2) for iCivic1 in lCivics for iCivic2 in lCivics if iCivic1 < iCivic2]

		iCivicCombo = 0
		# Calculate the combinations
		for lCombination in lCombinations:
			iCivicCombo += self.getCivicCombinationStability(lCombination[0], lCombination[1])

		if ( pPlayer.getPicklefreeParameter( con.iIsHasStephansdom ) == 1 ):
			#if (self.getHasStephansdom(iPlayer) == 1):
			if (iCivicGovernment in ( xml.iCivicFeudalMonarchy, xml.iCivicDivineMonarchy, xml.iCivicLimitedMonarchy) ):
				iCivicCombo +=2

		if (iCivicLegal == xml.iCivicBureaucracy): #Bureaucracy city cap
			if ( pPlayer.isHuman() ):
				if ( iPlayer == con.iNovgorod and pPlayer.getNumCities() > 6): #the penalties are halved for Novgorod
					iCivicCombo += (( 6 - pPlayer.getNumCities() ) / 2 )
				else:
					iCivicCombo += ( 6 - pPlayer.getNumCities() )
			else:
				if ( iPlayer == con.iNovgorod and pPlayer.getNumCities() > 6): #the penalties are halved for Novgorod
					iCivicCombo += max( -5, (( 6 - pPlayer.getNumCities() ) / 2 ) )
				else:
					iCivicCombo += max( -5, 6 - pPlayer.getNumCities() ) #max -5 penalty for the AI
		if (iCivicGovernment == xml.iCivicMerchantRepublic): #Merchant Republic city cap
			if ( pPlayer.isHuman() ):
				if ( iPlayer == con.iVenecia and pPlayer.getNumCities() > 5): #the penalties are halved for Venice
					iCivicCombo += (( 5 - pPlayer.getNumCities() ) / 2 )
				else:
					iCivicCombo += ( 5 - pPlayer.getNumCities() )
			else:
				if ( iPlayer == con.iVenecia and pPlayer.getNumCities() > 5): #the penalties are halved for Venice
					iCivicCombo += max( -5, (( 5 - pPlayer.getNumCities() ) / 2 ) )
				else:
					iCivicCombo += max( -5, 5 - pPlayer.getNumCities() ) #max -5 penalty for the AI

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
			
	def getCivicCombinationStability(self, iCivic0, iCivic1):
		lCivics = set([iCivic0, iCivic1])

		if xml.iCivicMerchantRepublic in lCivics:
			if xml.iCivicFeudalLaw in lCivics: return -3
			if xml.iCivicTradeEconomy in lCivics: return 4
			if xml.iCivicImperialism in lCivics: return -2

		if xml.iCivicDivineMonarchy in lCivics: #Divine Monarchy should have an appropriate religious civic
			if xml.iCivicPaganism in lCivics: return -4
			if xml.iCivicTheocracy in lCivics: return 3
			if xml.iCivicStateReligion in lCivics: return 2
			if xml.iCivicOrganizedReligion in lCivics: return 4
			if xml.iCivicFreeReligion in lCivics: return -3
			if xml.iCivicReligiousLaw in lCivics: return 2

		if set([xml.iCivicLimitedMonarchy, xml.iCivicMerchantRepublic]) & lCivics: #Constitutional Monarchy and Republic both like enlightened civics
			if xml.iCivicCommonLaw in lCivics: return 3
			if set([xml.iCivicFreePeasantry, xml.iCivicFreeLabor]) & lCivics: return 2

		if xml.iCivicFeudalLaw in lCivics:
			if xml.iCivicSerfdom in lCivics: return 3
			if xml.iCivicFreePeasantry in lCivics: return -4
			if xml.iCivicManorialism in lCivics: return 2
			if xml.iCivicFeudalMonarchy in lCivics: return 3
			if xml.iCivicVassalage in lCivics: return 2

		if xml.iCivicSerfdom in lCivics:
			if xml.iCivicManorialism in lCivics: return 2
			if xml.iCivicCommonLaw in lCivics: return -3

		if xml.iCivicReligiousLaw in lCivics:
			if xml.iCivicPaganism in lCivics: return -5
			if xml.iCivicFreeReligion in lCivics: return -3
			if xml.iCivicTheocracy in lCivics:  return 4

		if xml.iCivicCommonLaw in lCivics:
			if xml.iCivicFreeLabor in lCivics: return 3
			if xml.iCivicTheocracy in lCivics: return -4

		if xml.iCivicApprenticeship in lCivics:
			if xml.iCivicGuilds in lCivics: return 3

		return 0

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
				if (iBuilding >= xml.iSistineChapel and iBuilding <= xml.iLanterna): #+2 per wonder
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
		iExpStability += iCivicBonus # Imperialism
		iExpStability += iUPBonus # French UP
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
	#	if ( pPlayer.getID() == con.iTurkey and pPlayer.getStability() < 1 and gc.getGame().getGameTurn() < xml.i1570AD ): # boost Turkey before the battle of Lepanto
	#		if ( not pPlayer.isHuman() ):
	#			iExpStability += min( 3 - pPlayer.getStability(), 6 )
	#	if ( pPlayer.getID() == con.iVenecia and pPlayer.getStability() < 1 and gc.getGame().getGameTurn() < xml.i1204AD ): # Venice has trouble early on due to its civics
	#		if ( not pPlayer.isHuman() ):
	#			iExpStability += 4
		pPlayer.setStabilityVary( iCathegoryExpansion, iExpStability )

