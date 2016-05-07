# Rhye's and Fall of Civilization - (a part of) Unique Powers

#Emperor UP is in RiseAndFall in the collapse and secession functions, RFCUtils.collapseImmune and stability
#Khan UP is in c++ CvPlayer.cpp::acquireCity()

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
#import cPickle as pickle
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
		if (iStateReligion >= 0 and iStateReligion <= 3):
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

		iOldPoints = pPlayer.getPicklefreeParameter( iJanissaryPoints )

		iNextJanissary = 200
		if ( pPlayer.isHuman() ):
			iNextJanissary = 300


		if ( iOldPoints + iNewPoints > iNextJanissary ):
			#iNewPoints = 0
			apCityList = PyPlayer(iPlayer).getCityList()
			iRandCity = gc.getGame().getSorenRandNum(len( apCityList ), 'Janissary city')
			pCity = apCityList[iRandCity].GetCy()
			utils.makeUnit( xml.iJanissary, iPlayer, [pCity.getX(), pCity.getY()], 1 )
			pPlayer.setPicklefreeParameter( iJanissaryPoints, 0 )
			#print(" 3Miro making a Janissary in ",pCity.getName() )
		else:
		     pPlayer.setPicklefreeParameter( iJanissaryPoints, iOldPoints + iNewPoints )

		#print(" 3Miro Janissaries for player: ",iPlayer,pPlayer.getPicklefreeParameter( iJanissaryPoints ) )
		#print(" 3Miro Janissaries this turn addes: ", iNewPoints)


# Absinthe: Danish UP
	def soundUP(self, iPlayer):
		print("Sound dues")
		lSoundCoords = [(60,57),(60,58)]

		#Check if we control the Sound
		bControlsSound = False
		for tCoord in lSoundCoords:
			pPlot = gc.getMap().plot(tCoord[0],tCoord[1])
			if(pPlot.calculateCulturalOwner() == iPlayer):
				bControlsSound = True
				break
		if(not bControlsSound):
			print("No sound dues, sound not controlled")
			return

		iCities = self.getNumForeignCitiesOnBaltic(iPlayer)

		iGold = iCities * 2
		print("We got %d gold." % iGold)
		gc.getPlayer(iPlayer).changeGold(iGold)

		CyInterface().addMessage(iPlayer, True, con.iDuration/2, CyTranslator().getText("TXT_KEY_UP_SOUND_TOLL", ( iGold, )), "", 0, "", ColorTypes(con.iGreen), -1, -1, True, True)

	def getNumForeignCitiesOnBaltic(self, iPlayer, bVassal = False):
		lBalticRects = [((56, 52), (70, 57)), ((62, 58), (74, 62)), ((64, 63), (79, 66)), ((64, 67), (71, 72))]

		#Count foreign coastal cities
		iCities = 0
		for tRect in lBalticRects:
			for iX in range(tRect[0][0], tRect[1][0]+1):
				for iY in range(tRect[0][1], tRect[1][1]+1):
					#print(iX,iY)
					pPlot = gc.getMap().plot(iX,iY)
					if(pPlot.isCity()):
						pCity = pPlot.getPlotCity()
						#print(pCity.getName() + " is a city.")
						if pCity.isCoastal(5):
							if not bVassal:
								if (pCity.getOwner() != iPlayer):
									#print(pCity.getName() + " is a foreign coastal city on the Baltic.")
									iCities += 1
							else:
								bCount = False
								iOwner = pCity.getOwner()
								if (iOwner != iPlayer and iOwner != utils.getMaster(iOwner) != iPlayer):
									iCities += 1
		return iCities


# Absinthe: Aragon UP
	def confederationUP(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		#Only recalc if we have a different number of cities from last turn.
		if pPlayer.getNumCities() == pPlayer.getUHVCounter(1):
			return
		pPlayer.setUHVCounter(1, pPlayer.getNumCities())

		#print("Recalc Province Commerce UP")
		cityProvinces = []
		iCapitalX = -1
		iCapitalY = -1
		apCityList = PyPlayer(iPlayer).getCityList()
		for pLoopCity in apCityList:
			pCity = pLoopCity.GetCy()
			# The capital, note the position
			if(pCity.hasBuilding(xml.iPalace)):
				iCapitalX = pCity.getX()
				iCapitalY = pCity.getY()
			pProvince = pCity.getProvince()
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
		teamPlayer = gc.getTeam(pPlayer.getTeam())

		# One ranged/gun class
		RangedClass = xml.iArcher
		if(teamPlayer.isHasTech(xml.iCombinedArms) and teamPlayer.isHasTech(xml.iNationalism)):
			RangedClass = xml.iLineInfantry
		elif(teamPlayer.isHasTech(xml.iMatchlock)):
			RangedClass = xml.iMusketman
		elif(teamPlayer.isHasTech(xml.iChivalry) and teamPlayer.isHasTech(xml.iReplaceableParts)):
			RangedClass = xml.iLongbowman
		elif(teamPlayer.isHasTech(xml.iPlateArmor)):
			RangedClass = xml.iArbalest
		elif(teamPlayer.isHasTech(xml.iMachinery)):
			RangedClass = xml.iCrossbowman

		# One polearm class
		PolearmClass = xml.iSpearman
		if(teamPlayer.isHasTech(xml.iCombinedArms) and teamPlayer.isHasTech(xml.iNationalism)):
			PolearmClass = xml.iLineInfantry
		elif(teamPlayer.isHasTech(xml.iProfessionalArmy)):
			PolearmClass = xml.iPikeman
		elif(teamPlayer.isHasTech(xml.iAristocracy)):
			PolearmClass = xml.iGuisarme

		print("Making ", RangedClass, " and ", PolearmClass)
		apCityList = PyPlayer(iPlayer).getCityList()
		for pLoopCity in apCityList:
			pCity = pLoopCity.GetCy()
			tPlot = (pCity.getX(), pCity.getY())
			if(gc.getGame().getSorenRandNum(2,'DefiancyType') == 1):
				utils.makeUnit(RangedClass, iPlayer, tPlot, 1)
			else:
				utils.makeUnit(PolearmClass, iPlayer, tPlot, 1)
			print("In city: ", tPlot)

