# RFC Europe - Companies
# Implemented by AbsintheRed, based on the wonderful idea of embryodead

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Consts as con
import XMLConsts as xml
import RFCUtils
from StoredData import sd
from operator import itemgetter

# globals
utils = RFCUtils.RFCUtils()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer

iNumPlayers = con.iNumPlayers
iNumTotalPlayers = con.iNumTotalPlayers
iNumCompanies = xml.iNumCompanies
iHospitallers = xml.iHospitallers
iTemplars = xml.iTemplars
iTeutons = xml.iTeutons
iHansa = xml.iHansa
iMedici = xml.iMedici
iAugsburg = xml.iAugsburg
iStGeorge = xml.iStGeorge
iDragon = xml.iDragon
iCalatrava = xml.iCalatrava
tCompaniesBirth = xml.tCompaniesBirth
tCompaniesDeath = xml.tCompaniesDeath
tCompaniesLimit = xml.tCompaniesLimit
lCompanyRegions = xml.lCompanyRegions
iCatholicism = xml.iCatholicism
iOrthodoxy = xml.iOrthodoxy
iProtestantism = xml.iProtestantism
iIslam = xml.iIslam
iJudaism = xml.iJudaism

class Companies:


	def checkTurn(self, iGameTurn):

	#	if (iGameTurn == 3):
	#		for iPlayer in range(iNumPlayers):
	#			if (iPlayer == 1):
	#				apCityList = PyPlayer(iPlayer).getCityList()
	#				for pCity in apCityList:
	#					city = pCity.GetCy()
	#					city.setHasCorporation(0, True, True, True)
	#
	#	if (iGameTurn == 8):
	#		for iPlayer in range(iNumPlayers):
	#			if (iPlayer == 1):
	#				apCityList = PyPlayer(iPlayer).getCityList()
	#				for pCity in apCityList:
	#					city = pCity.GetCy()
	#					city.setHasCorporation(0, False, True, True)

		# check if it's not too early
		iCompany = iGameTurn % iNumCompanies
		if iGameTurn < tCompaniesBirth[iCompany]:
			return

		# check if it's not too late
		elif iGameTurn > tCompaniesDeath[iCompany] + gc.getGame().getSorenRandNum(iNumCompanies, 'small randomness with a couple extra turns'):
			iMaxCompanies = 0
			# do not dissolve the Templars while Jerusalem is under Catholic control
			if iCompany == iTemplars:
				plot = gc.getMap().plot(con.tJerusalem[0], con.tJerusalem[1])
				if plot.isCity():
					if gc.getPlayer(plot.getPlotCity().getOwner()).getStateReligion() == iCatholicism:
						iMaxCompanies = tCompaniesLimit[iCompany]

		# set the company limit
		else:
			iMaxCompanies = tCompaniesLimit[iCompany]

		# modified limit for Hospitallers and Teutons after the Crusades
		if (iGameTurn > tCompaniesDeath[iTemplars]):
			if iCompany == iHospitallers:
				iMaxCompanies -= 1
			elif iCompany == iTeutons:
				iMaxCompanies += 2

		# loop through all cities, check the company value for each and add the good ones to a list of tuples (city, value)
		cityValueList = []
		for iPlayer in range(iNumPlayers):
			apCityList = PyPlayer(iPlayer).getCityList()
			for pCity in apCityList:
				city = pCity.GetCy()
				iValue = self.getCityValue(city, iCompany)
				if iValue > 0:
					cityValueList.append((city, iValue * 10 + gc.getGame().getSorenRandNum(10, 'random bonus')))
				elif city.isHasCorporation(iCompany): # remove company from cities with a negative value
					city.setHasCorporation(iCompany, False, True, True)
					sCityName = city.getName()
					print ("Company removed: ", sCityName, iCompany, iValue)
					# interface message for the human player
					iHuman = utils.getHumanID()
					sCompanyName = gc.getCorporationInfo(iCompany).getDescription()
					iX = city.getX()
					iY = city.getY()
					if (utils.isActive(iHuman) and city.isRevealed(iHuman, False)):
						CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_MISC_CORPORATION_REMOVED", (sCompanyName,sCityName)), gc.getCorporationInfo(iCompany).getSound(), InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getCorporationInfo(iCompany).getButton(), ColorTypes(con.iWhite), iX, iY, True, True)

		# sort cities from highest to lowest value
		cityValueList.sort(key=itemgetter(1), reverse=True)

		# count the number of companies
		iCompanyCount = 0
		for iLoopPlayer in range(iNumPlayers):
			if gc.getPlayer(iLoopPlayer).isAlive:
				iCompanyCount += gc.getPlayer(iLoopPlayer).countCorporations(iCompany)

		# spread the company
		for i in range(len(cityValueList)):
			city = cityValueList[i][0]
			iValue = cityValueList[i][1]
			if city.isHasCorporation(iCompany):
				continue
			if iCompanyCount >= iMaxCompanies and i >= iMaxCompanies: # don't spread to weak cities if the limit was reached
				break
			city.setHasCorporation(iCompany, True, True, True)
			sCityName = city.getName()
			print ("Company spread: ", sCityName, iCompany, iValue)
			# interface message for the human player
			iHuman = utils.getHumanID()
			sCompanyName = gc.getCorporationInfo(iCompany).getDescription()
			iX = city.getX()
			iY = city.getY()
			if (utils.isActive(iHuman) and city.isRevealed(iHuman, False)):
				CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_MISC_CORPORATION_SPREAD", (sCompanyName,sCityName)), gc.getCorporationInfo(iCompany).getSound(), InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getCorporationInfo(iCompany).getButton(), ColorTypes(con.iWhite), iX, iY, True, True)
			# spread the religion if it wasn't present before
			if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons or iCompany == iCalatrava):
				if not city.isHasReligion(iCatholicism):
					city.setHasReligion(iCatholicism, True, True, False)
			# one change at a time, only add the highest ranked city (which didn't have the company before)
			break

		# if the limit was exceeded, remove company from it's worst city
		if iCompanyCount > iMaxCompanies:
			for i in range(len(cityValueList)-1, 0, -1):
				city = cityValueList[i][0]
				iValue = cityValueList[i][1]
				if city.isHasCorporation(iCompany):
					city.setHasCorporation(iCompany, False, True, True)
					sCityName = city.getName()
					print ("Company removed: ", sCityName, iCompany, iValue)
					# interface message for the human player
					iHuman = utils.getHumanID()
					sCompanyName = gc.getCorporationInfo(iCompany).getDescription()
					iX = city.getX()
					iY = city.getY()
					if (utils.isActive(iHuman) and city.isRevealed(iHuman, False)):
						CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_MISC_CORPORATION_REMOVED", (sCompanyName,sCityName)), gc.getCorporationInfo(iCompany).getSound(), InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getCorporationInfo(iCompany).getButton(), ColorTypes(con.iWhite), iX, iY, True, True)
					break


	def onPlayerChangeStateReligion(self, argsList):
		iPlayer, iNewReligion, iOldReligion = argsList

		apCityList = PyPlayer(iPlayer).getCityList()
		for pCity in apCityList:
			city = pCity.GetCy()
			for iCompany in range(iNumCompanies):
				if city.isHasCorporation(iCompany):
					if self.getCityValue(city, iCompany) < 0:
						city.setHasCorporation(iCompany, False, True, True)
						sCityName = city.getName()
						print ("Company removed on religion change: ", sCityName, iCompany)
						# interface message for the human player
						iHuman = utils.getHumanID()
						sCompanyName = gc.getCorporationInfo(iCompany).getDescription()
						iX = city.getX()
						iY = city.getY()
						if (utils.isActive(iHuman) and city.isRevealed(iHuman, False)):
							CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_MISC_CORPORATION_REMOVED", (sCompanyName,sCityName)), gc.getCorporationInfo(iCompany).getSound(), InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getCorporationInfo(iCompany).getButton(), ColorTypes(con.iWhite), iX, iY, True, True)


	def onCityAcquired(self, city):

		for iCompany in range(iNumCompanies):
			if city.isHasCorporation(iCompany):
				if self.getCityValue(city, iCompany) < 0:
					city.setHasCorporation(iCompany, False, True, True)
					sCityName = city.getName()
					print ("Company removed on conquest: ", sCityName, iCompany)
					# interface message for the human player
					iHuman = utils.getHumanID()
					sCompanyName = gc.getCorporationInfo(iCompany).getDescription()
					iX = city.getX()
					iY = city.getY()
					if (utils.isActive(iHuman) and city.isRevealed(iHuman, False)):
						CyInterface().addMessage(iHuman, False, con.iDuration, CyTranslator().getText("TXT_KEY_MISC_CORPORATION_REMOVED", (sCompanyName,sCityName)), gc.getCorporationInfo(iCompany).getSound(), InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getCorporationInfo(iCompany).getButton(), ColorTypes(con.iWhite), iX, iY, True, True)


	def getCityValue(self, city, iCompany):

		if city is None: return -1
		elif city.isNone(): return -1

		iValue = 0

		owner = gc.getPlayer(city.getOwner())
		ownerTeam = gc.getTeam(owner.getTeam())

		# spread the Teutons to Teutonic Order cities and don't spread if the owner civ is at war with the Teutons
		if iCompany == iTeutons:
			if owner.getID() == con.iPrussia:
				iValue += 4
			elif ownerTeam.isAtWar(con.iPrussia):
				return -1

		# state religion requirements
		iStateReligion = owner.getStateReligion()
		if iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons:
			if iStateReligion == iCatholicism:
				iValue += 3
			elif iStateReligion == iOrthodoxy:
				iValue += 1
			elif iStateReligion == iProtestantism:
				iValue -= -2
			else:
				return -1
		elif iCompany == iDragon:
			if iStateReligion == iCatholicism:
				iValue += 2
			elif iStateReligion == iOrthodoxy:
				iValue += 1
			elif iStateReligion == iIslam:
				return -1
		elif iCompany == iCalatrava:
			if iStateReligion == iCatholicism:
				iValue += 2
			else:
				return -1
		else:
			if iStateReligion == iIslam:
				return -1

		# geographical requirements
		iProvince = city.getProvince()
		if len(lCompanyRegions[iCompany]) > 0 and iProvince not in lCompanyRegions[iCompany]:
			return -1
		if iCompany == iMedici:
			if iProvince == xml.iP_Tuscany:
				iValue += 4
		if iCompany == iAugsburg:
			if iProvince == xml.iP_Bavaria:
				iValue += 3
			if iProvince == xml.iP_Swabia:
				iValue += 2
		if iCompany == iStGeorge:
			if iProvince == xml.iP_Liguria:
				iValue += 3
		if iCompany == iHansa:
			if iProvince == xml.iP_Holstein:
				iValue += 2
			if iProvince == xml.iP_Brandenburg or iProvince == xml.iP_Saxony:
				iValue += 1

		# geographical requirement changes after the crusades
		iGameTurn = gc.getGame().getGameTurn()
		if (iGameTurn < tCompaniesDeath[iTemplars]):
			if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons):
				if iStateReligion == iCatholicism:
					if (iProvince == xml.iP_Antiochia or iProvince == xml.iP_Lebanon or iProvince == xml.iP_Jerusalem):
						iValue += 5
					if (iProvince == xml.iP_Cyprus or iProvince == xml.iP_Egypt):
						iValue += 3
		else:
			if iCompany == iHospitallers:
				if (iProvince == xml.iP_Rhodes or iProvince == xml.iP_Malta):
					iValue += 4
			if iCompany == iTeutons:
				if iProvince == xml.iP_Transylvania:
					iValue += 2

		# additional bonus for the city of Jerusalem
		if (city.getX() == con.tJerusalem[0] and city.getY() == con.tJerusalem[1]):
			if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons):
				iValue += 3

		# coastal city check
		if iCompany == iHansa:
			if not city.isCoastal(20):
				return -1
		elif iCompany == iHospitallers:
			if city.isCoastal(20):
				iValue += 2

		# bonus for religions in the city
		if (iCompany == iHansa or iCompany == iMedici or iCompany == iAugsburg or iCompany == iStGeorge):
			if city.isHasReligion(iJudaism): # not necessarily historic, but has great gameplay synergies
				iValue += 1
		if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons or iCompany == iCalatrava):
			# they have a harder time to choose a city without Catholicism, but they spread the religion there
			if not city.isHasReligion(iCatholicism):
				iValue -= 1
			if city.isHasReligion(iIslam):
				iValue -= 1
		if iCompany == iDragon:
			if city.isHasReligion(iCatholicism) or city.isHasReligion(iOrthodoxy):
				iValue += 1
			if city.isHasReligion(iIslam):
				iValue -= 1

		# various building bonuses, trade route bonus
		if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons):
			if city.getNumRealBuilding(xml.iWalls) > 0 or city.getNumRealBuilding(xml.iMoroccoKasbah) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iCastle) > 0 or city.getNumRealBuilding(xml.iHungarianStronghold) > 0 or city.getNumRealBuilding(xml.iSpanishCitadel) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iBarracks) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iStable) > 0 or city.getNumRealBuilding(xml.iBulgarianStan) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iArcheryRange) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iCatholicTemple) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iCatholicMonastery) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iGuildHall) > 0 or city.getNumRealBuilding(xml.iNovgorodKonets) > 0: iValue += 1
			if iCompany == iHospitallers and city.getNumRealBuilding(xml.iKrakDesChevaliers) > 0: iValue += 5
			elif city.getNumRealBuilding(xml.iKrakDesChevaliers) > 0: iValue += 2
			if iCompany == iTemplars and city.getNumRealBuilding(xml.iDomeRock) > 0: iValue += 5
			elif city.getNumRealBuilding(xml.iDomeRock) > 0: iValue += 2
		if (iCompany == iDragon or iCompany == iCalatrava):
			if city.getNumRealBuilding(xml.iWalls) > 0 or city.getNumRealBuilding(xml.iMoroccoKasbah) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iCastle) > 0 or city.getNumRealBuilding(xml.iHungarianStronghold) > 0 or city.getNumRealBuilding(xml.iSpanishCitadel) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iBarracks) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iStable) > 0 or city.getNumRealBuilding(xml.iBulgarianStan) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iArcheryRange) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iStarFort) > 0: iValue += 1
		if (iCompany == iMedici or iCompany == iAugsburg or iCompany == iStGeorge):
			if city.getNumRealBuilding(xml.iMarket) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iBank) > 0 or city.getNumRealBuilding(xml.iGenoaBank) > 0 or city.getNumRealBuilding(xml.iEnglishRoyalExchange) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iJeweler) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iPalace) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iSummerPalace) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iGuildHall) > 0 or city.getNumRealBuilding(xml.iNovgorodKonets) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iLuxuryStore) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iCourthouse) > 0 or city.getNumRealBuilding(xml.iHolyRomanRathaus) > 0 or city.getNumRealBuilding(xml.iKievVeche) > 0 or city.getNumRealBuilding(xml.iLithuanianVoivodeship) > 0: iValue += 1
			iValue += city.getTradeRoutes() - 1
		if iCompany == iHansa:
			if city.getNumRealBuilding(xml.iHarbor) > 0 or city.getNumRealBuilding(xml.iVikingTradingPost) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iLighthouse) > 0 or city.getNumRealBuilding(xml.iPortugalFeitoria) > 0 or city.getNumRealBuilding(xml.iAragonSeaport) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iWharf) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iCustomHouse) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iMarket) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iBrewery) > 0 or city.getNumRealBuilding(xml.iBurgundianWinery) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iWeaver) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iGuildHall) > 0 or city.getNumRealBuilding(xml.iNovgorodKonets) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iWarehouse) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iTannery) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iTextileMill) > 0: iValue += 1
			iValue += city.getTradeRoutes()

		# civic bonuses
		if owner.getCivics(0) == xml.iCivicMerchantRepublic:
			if (iCompany == iMedici or iCompany == iStGeorge or iCompany == iHospitallers):
				iValue += 1
			if iCompany == iHansa:
				iValue += 2
		if owner.getCivics(1) == xml.iCivicFeudalLaw:
			if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons or iCompany == iDragon or iCompany == iCalatrava):
				iValue += 2
		if owner.getCivics(1) == xml.iCivicReligiousLaw:
			if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons or iCompany == iCalatrava):
				iValue += 1
		if owner.getCivics(2) == xml.iCivicApprenticeship:
			if iCompany == iHansa:
				iValue += 1
		if owner.getCivics(3) == xml.iCivicTradeEconomy:
			if (iCompany == iMedici or iCompany == iAugsburg or iCompany == iStGeorge):
				iValue += 1
			if iCompany == iHansa:
				iValue += 2
		if owner.getCivics(3) == xml.iCivicGuilds:
			if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons or iCompany == iHansa or iCompany == iDragon or iCompany == iCalatrava):
				iValue += 1
		if owner.getCivics(3) == xml.iCivicMercantilism:
			if iCompany == iHansa:
				return -1
			elif (iCompany == iMedici or iCompany == iAugsburg or iCompany == iStGeorge):
				iValue -= 2
		if owner.getCivics(4) == xml.iCivicTheocracy:
			if (iCompany == iHospitallers or iCompany == iTemplars):
				iValue += 1
			if iCompany == iTeutons:
				iValue += 2
		if owner.getCivics(4) == xml.iCivicFreeReligion:
			if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons or iCompany == iDragon):
				iValue -= 1
			if iCompany == iCalatrava:
				iValue -= 2
		if owner.getCivics(5) == xml.iCivicOccupation:
			if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons or iCompany == iDragon or iCompany == iCalatrava):
				iValue += 1

		# bonus for techs
		if (iCompany == iHospitallers or iCompany == iTemplars or iCompany == iTeutons or iCompany == iDragon or iCompany == iCalatrava):
			for iTech in (xml.iChivalry, xml.iPlateArmor, xml.iGuilds, xml.iMilitaryTradition):
				if (ownerTeam.isHasTech(iTech)):
					iValue += 1
		if iCompany == iHansa:
			for iTech in (xml.iGuilds, xml.iClockmaking, xml.iOptics, xml.iShipbuilding):
				if (ownerTeam.isHasTech(iTech)):
					iValue += 1
		if (iCompany == iMedici or iCompany == iStGeorge):
			for iTech in (xml.iBanking, xml.iPaper, xml.iClockmaking, xml.iOptics, xml.iShipbuilding):
				if (ownerTeam.isHasTech(iTech)):
					iValue += 1
		if iCompany == iAugsburg:
			for iTech in (xml.iBanking, xml.iPaper, xml.iChemistry):
				if (ownerTeam.isHasTech(iTech)):
					iValue += 1

		# resources
		iTempValue = 0
		bFound = False
		for i in range(4):
			iBonus = gc.getCorporationInfo(iCompany).getPrereqBonus(i)
			if iBonus > -1:
				if city.getNumBonuses(iBonus) > 0: bFound = True
				if iCompany in [iHospitallers, iTemplars, iTeutons, iDragon, iCalatrava]:
					iTempValue += city.getNumBonuses(iBonus)
				else:
					iTempValue += city.getNumBonuses(iBonus) * 2
		if iCompany in [iHansa, iMedici, iAugsburg, iStGeorge] and not bFound: return -1
		iValue += iTempValue

		# bonus for resources in the fat cross of a city?

		# competition
		if iCompany == iHospitallers:
			if city.isHasCorporation(iTemplars):
				iValue *= 0.66
			if city.isHasCorporation(iTeutons):
				iValue *= 0.66
		elif iCompany == iTemplars:
			if city.isHasCorporation(iHospitallers):
				iValue *= 0.66
			if city.isHasCorporation(iTeutons):
				iValue *= 0.66
		elif iCompany == iTeutons:
			if city.isHasCorporation(iTemplars):
				iValue *= 0.66
			if city.isHasCorporation(iHospitallers):
				iValue *= 0.66
		elif iCompany == iMedici:
			if city.isHasCorporation(iStGeorge) or city.isHasCorporation(iAugsburg):
				iValue /= 2
		elif iCompany == iStGeorge:
			if city.isHasCorporation(iMedici) or city.isHasCorporation(iAugsburg):
				iValue /= 2
		elif iCompany == iAugsburg:
			if city.isHasCorporation(iMedici) or city.isHasCorporation(iStGeorge):
				iValue /= 2

		# threshold
		if iValue < 3: return -1

		# spread it out
		iValue -= owner.countCorporations(iCompany)

		return iValue
