# Rhye's and Fall of Civilization: Europe - Unique Powers (only a couple of them is here, most are handled in the .dll)

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
#import cPickle as pickle
import Consts as con
import XMLConsts as xml
import Religions
import RFCUtils

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()
religion = Religions.Religions()

iJanissaryPoints = con.iJanissaryPoints

class UniquePowers:

	def checkTurn(self, iGameTurn):
		pass


	# Absinthe: Arabian UP
	def faithUP(self, iPlayer, city):
		pFaithful = gc.getPlayer(iPlayer)
		iStateReligion = pFaithful.getStateReligion()
		iTemple = 0
		# Absinthe: shouldn't work on minor religions, to avoid exploit with spreading Judaism this way
		if 0 <= iStateReligion <= 3:
			if not city.isHasReligion(iStateReligion):
				city.setHasReligion(iStateReligion, True, True, False)
				pFaithful.changeFaith( 1 )

			if iStateReligion == 0:
				iTemple = xml.iProtestantTemple
			elif iStateReligion == 1:
				iTemple = xml.iIslamicTemple
			elif iStateReligion == 2:
				iTemple = xml.iCatholicTemple
			elif iStateReligion == 3:
				iTemple = xml.iOrthodoxTemple
			if not city.hasBuilding(iTemple):
				city.setHasRealBuilding(iTemple, True)
				pFaithful.changeFaith( 1 )


	# Absinthe: Ottoman UP
	def janissaryUP(self, iPlayer ):
		pPlayer = gc.getPlayer( iPlayer )
		iStateReligion = pPlayer.getStateReligion()

		iNewPoints = 0
		for city in utils.getCityList(iPlayer):
			for iReligion in range( xml.iNumReligions ):
				if iReligion != iStateReligion and city.isHasReligion( iReligion ):
					iNewPoints += city.getPopulation()
					break

		iOldPoints = pPlayer.getPicklefreeParameter( iJanissaryPoints )

		iNextJanissary = 200
		if pPlayer.isHuman():
			iNextJanissary = 300

		if ( iOldPoints + iNewPoints > iNextJanissary ):
			#tCity = religion.selectRandomCityCiv(iPlayer)
			#utils.makeUnit( xml.iJanissary, iPlayer, tCity, 1 )
			pCity = utils.getRandomCity(iPlayer) # The Janissary unit appears in a random city - should it be the capital instead?
			if pCity != -1:
				iX = pCity.getX()
				iY = pCity.getY()
				utils.makeUnit( xml.iJanissary, iPlayer, (iX, iY), 1 )
				# interface message for the human player
				if iPlayer == utils.getHumanID():
					CyInterface().addMessage(iPlayer, False, con.iDuration, CyTranslator().getText("TXT_KEY_UNIT_NEW_JANISSARY", ()) + " " + pCity.getName() + "!", "AS2D_UNIT_BUILD_UNIQUE_UNIT", 0, gc.getUnitInfo(xml.iJanissary).getButton(), ColorTypes(con.iGreen), iX, iY, True, True)
				pPlayer.setPicklefreeParameter( iJanissaryPoints, 0 )
				print(" New Janissary in ",pCity.getName() )
		else:
			pPlayer.setPicklefreeParameter( iJanissaryPoints, iOldPoints + iNewPoints )


	# Absinthe: Danish UP
	def soundUP(self, iPlayer):
		print("Sound dues")
		lSoundCoords = [(60,57),(60,58)]

		# Check if we control the Sound
		bControlsSound = False
		for tCoord in lSoundCoords:
			pPlot = gc.getMap().plot(tCoord[0], tCoord[1])
			if pPlot.calculateCulturalOwner() == iPlayer:
				bControlsSound = True
				break
		if not bControlsSound:
			print("No sound dues, sound not controlled")
			return

		iCities = self.getNumForeignCitiesOnBaltic(iPlayer)

		iGold = iCities * 2
		print("We got %d gold." % iGold)
		gc.getPlayer(iPlayer).changeGold(iGold)

		CyInterface().addMessage(iPlayer, False, con.iDuration/2, CyTranslator().getText("TXT_KEY_UP_SOUND_TOLL", ( iGold, )), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)

	def getNumForeignCitiesOnBaltic(self, iPlayer, bVassal = False):
		lBalticRects = [((56, 52), (70, 57)), ((62, 58), (74, 62)), ((64, 63), (79, 66)), ((64, 67), (71, 72))]

		# Count foreign coastal cities
		iCities = 0
		for tRect in lBalticRects:
			for (iX, iY) in utils.getPlotList(tRect[0], tRect[1]):
				#print(iX,iY)
				pPlot = gc.getMap().plot(iX, iY)
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					#print(pCity.getName() + " is a city.")
					if pCity.isCoastal(5):
						if not bVassal:
							if pCity.getOwner() != iPlayer:
								#print(pCity.getName() + " is a foreign coastal city on the Baltic.")
								iCities += 1
						else:
							iOwner = pCity.getOwner()
							if iOwner != iPlayer and iOwner != utils.getMaster(iOwner) != iPlayer:
								iCities += 1
		return iCities


	# Absinthe: Aragonese UP
	def confederationUP(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		# Only recalculate if we have a different number of cities from last turn.
		if pPlayer.getNumCities() == pPlayer.getUHVCounter(1):
			return
		pPlayer.setUHVCounter(1, pPlayer.getNumCities())

		#print("Recalc Province Commerce UP")
		cityProvinces = []
		capital = pPlayer.getCapitalCity()
		iCapitalX = capital.getX()
		iCapitalY = capital.getY()
		for city in utils.getCityList(iPlayer):
			pProvince = city.getProvince()
			cityProvinces.append(pProvince)
		# How many unique provinces?
		uniqueProvinces = set(cityProvinces)
		iProvinces = len(uniqueProvinces)
		#print("Unique provinces", iProvinces)
		#print("Capital at",iCapitalX,iCapitalY)
		# Kludge: the UHV counter is a storage of sorts
		iProvinceCommerceLastBonus = pPlayer.getUHVCounter(0)
		iProvinceCommerceNextBonus = iProvinces * 2 # <- This number is the amount of extra commerce per province
		gc.getGame().setPlotExtraYield( iCapitalX, iCapitalY, 2, -iProvinceCommerceLastBonus)
		#print("Capital commerce reduced by", iProvinceCommerceLastBonus)
		gc.getGame().setPlotExtraYield( iCapitalX, iCapitalY, 2, iProvinceCommerceNextBonus)
		#print("Capital commerce increased by", iProvinceCommerceNextBonus)
		pPlayer.setUHVCounter(0, iProvinceCommerceNextBonus )


	# Absinthe: Scottish UP
	def defianceUP(self, iPlayer):
		print("Defiance called")
		pPlayer = gc.getPlayer(iPlayer)

		# One ranged/gun class
		RangedClass = utils.getUniqueUnit(iPlayer, xml.iArcher)
		lRangedList = [xml.iLineInfantry, xml.iMusketman, xml.iLongbowman, xml.iArbalest, xml.iCrossbowman, xml.iArcher]
		for iUnit in lRangedList:
			if pPlayer.canTrain(utils.getUniqueUnit(iPlayer, iUnit), False, False):
				RangedClass = utils.getUniqueUnit(iPlayer, iUnit)
				break

		# One polearm class
		PolearmClass = utils.getUniqueUnit(iPlayer, xml.iSpearman)
		lPolearmList = [xml.iLineInfantry, xml.iPikeman, xml.iGuisarme]
		for iUnit in lPolearmList:
			if pPlayer.canTrain(utils.getUniqueUnit(iPlayer, iUnit), False, False):
				PolearmClass = utils.getUniqueUnit(iPlayer, iUnit)
				break

		print("Making ", RangedClass, " and ", PolearmClass)
		for city in utils.getCityList(iPlayer):
			tPlot = (city.getX(), city.getY())
			if gc.getGame().getSorenRandNum(2,'DefiancyType') == 1:
				utils.makeUnit(RangedClass, iPlayer, tPlot, 1)
			else:
				utils.makeUnit(PolearmClass, iPlayer, tPlot, 1)
			print("In city: ", tPlot)

