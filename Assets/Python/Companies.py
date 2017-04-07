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
lCompanyBuilding = [xml.iCorporation1, xml.iCorporation2, xml.iCorporation3, xml.iCorporation4, xml.iCorporation5, xml.iCorporation6, xml.iCorporation7, xml.iCorporation8, xml.iCorporation9]

class Companies:

	def setup(self):

		# update companies at the beginning of the 1200AD scenario:
		if utils.getScenario() == con.i1200ADScenario:
			iGameTurn = xml.i1200AD
			for iCompany in range(xml.iNumCompanies):
				if iGameTurn > tCompaniesBirth[iCompany] and iGameTurn < tCompaniesDeath[iCompany]:
					self.addCompany (iCompany, 2)


	def checkTurn(self, iGameTurn):

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
		if iGameTurn > tCompaniesDeath[iTemplars]:
			if iCompany == iHospitallers and iGameTurn < tCompaniesDeath[iCompany]:
				iMaxCompanies -= 1
			elif iCompany == iTeutons and iGameTurn < tCompaniesDeath[iCompany]:
				iMaxCompanies += 2
		# increased limit for Hansa after their first general Diet in 1356
		if iCompany == iHansa:
			if xml.i1356AD < iGameTurn < tCompaniesDeath[iCompany]:
				iMaxCompanies += 3

		# loop through all cities, check the company value for each and add the good ones to a list of tuples (city, value)
		cityValueList = []
		for iPlayer in range(iNumPlayers):
			for city in utils.getCityList(iPlayer):
				iValue = self.getCityValue(city, iCompany)
				if iValue > 0:
					sCityName = city.getName()
					bPresent = False
					if city.isHasCorporation(iCompany):
						bPresent = True
					print ("Company value:", sCityName, iCompany, iValue, bPresent)
					cityValueList.append((city, iValue * 10 + gc.getGame().getSorenRandNum(10, 'random bonus')))
				elif city.isHasCorporation(iCompany): # remove company from cities with a negative value
					city.setHasCorporation(iCompany, False, True, True)
					city.setHasRealBuilding(lCompanyBuilding[iCompany], False)
					sCityName = city.getName()
					print ("Company removed: ", sCityName, iCompany, iValue)
					# interface message for the human player
					self.announceHuman(iCompany, city, True)

		# sort cities from highest to lowest value
		cityValueList.sort(key=itemgetter(1), reverse=True)

		# count the number of companies
		iCompanyCount = 0
		for iLoopPlayer in range(iNumPlayers):
			if gc.getPlayer(iLoopPlayer).isAlive: # should we check for indy/barb cities? isMinorCiv() isBarbarian()
				iCompanyCount += gc.getPlayer(iLoopPlayer).countCorporations(iCompany)

		# spread the company
		for i in range(len(cityValueList)):
			city, iValue = cityValueList[i]
			if city.isHasCorporation(iCompany):
				continue
			if i >= iMaxCompanies: # the goal is to spread the company to the first iMaxCompanies number of cities
				break
			city.setHasCorporation(iCompany, True, True, True)
			city.setHasRealBuilding(lCompanyBuilding[iCompany], True)
			iCompanyCount += 1
			sCityName = city.getName()
			print ("Company spread: ", sCityName, iCompany, iValue)
			# interface message for the human player
			self.announceHuman(iCompany, city)
			# spread the religion if it wasn't present before
			if iCompany in [iHospitallers, iTemplars, iTeutons, iCalatrava]:
				if not city.isHasReligion(iCatholicism):
					city.setHasReligion(iCatholicism, True, True, False)
			# one change at a time, only add the highest ranked city (which didn't have the company before)
			break

		# if the limit was exceeded, remove company from it's worst city
		if iCompanyCount > iMaxCompanies:
			for (city, iValue) in reversed(cityValueList): # loop backwards in the ordered list
				if city.isHasCorporation(iCompany):
					city.setHasCorporation(iCompany, False, True, True)
					city.setHasRealBuilding(lCompanyBuilding[iCompany], False)
					sCityName = city.getName()
					print ("Company removed: ", sCityName, iCompany, iValue)
					# interface message for the human player
					self.announceHuman(iCompany, city, True)
					# one change at a time, only add the lowest ranked city
					break


	def onPlayerChangeStateReligion(self, argsList):
		iPlayer, iNewReligion, iOldReligion = argsList

		for city in utils.getCityList(iPlayer):
			for iCompany in range(iNumCompanies):
				if city.isHasCorporation(iCompany):
					if self.getCityValue(city, iCompany) < 0:
						city.setHasCorporation(iCompany, False, True, True)
						city.setHasRealBuilding(lCompanyBuilding[iCompany], False)
						sCityName = city.getName()
						print ("Company removed on religion change: ", sCityName, iCompany)
						# interface message for the human player
						self.announceHuman(iCompany, city, True)


	def onCityAcquired(self, city):

		for iCompany in range(iNumCompanies):
			if city.isHasCorporation(iCompany):
				if self.getCityValue(city, iCompany) < 0:
					city.setHasCorporation(iCompany, False, True, True)
					city.setHasRealBuilding(lCompanyBuilding[iCompany], False)
					sCityName = city.getName()
					print ("Company removed on conquest: ", sCityName, iCompany)
					# interface message for the human player
					self.announceHuman(iCompany, city, True)


	def announceHuman(self, iCompany, city, bRemove = False):
		iHuman = utils.getHumanID()
		if not utils.isActive(iHuman) or not city.isRevealed(iHuman, False):
			return

		sCityName = city.getName()
		sCompanyName = gc.getCorporationInfo(iCompany).getDescription()
		iX = city.getX()
		iY = city.getY()

		if bRemove:
			sText = CyTranslator().getText("TXT_KEY_MISC_CORPORATION_REMOVED", (sCompanyName, sCityName))
		else:
			sText = CyTranslator().getText("TXT_KEY_MISC_CORPORATION_SPREAD", (sCompanyName, sCityName))
		CyInterface().addMessage(iHuman, False, con.iDuration, sText, gc.getCorporationInfo(iCompany).getSound(), InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getCorporationInfo(iCompany).getButton(), ColorTypes(con.iWhite), iX, iY, True, True)


	def getCityValue(self, city, iCompany):

		if city is None: return -1
		elif city.isNone(): return -1

		iValue = 0

		owner = gc.getPlayer(city.getOwner())
		iOwner = owner.getID()
		ownerTeam = gc.getTeam(owner.getTeam())

		# spread the Teutons to Teutonic Order cities and don't spread if the owner civ is at war with the Teutons
		if iCompany == iTeutons:
			if iOwner == con.iPrussia:
				iValue += 5
			elif ownerTeam.isAtWar(con.iPrussia):
				return -1

		# state religion requirements
		iStateReligion = owner.getStateReligion()
		if iCompany in [iHospitallers, iTemplars, iTeutons]:
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
		elif iCompany == iAugsburg:
			if iProvince == xml.iP_Bavaria:
				iValue += 3
			elif iProvince == xml.iP_Swabia:
				iValue += 2
		elif iCompany == iStGeorge:
			if iProvince == xml.iP_Liguria:
				iValue += 3
		elif iCompany == iHansa:
			if iProvince == xml.iP_Holstein:
				iValue += 5
			if iProvince in [xml.iP_Brandenburg, xml.iP_Saxony]:
				iValue += 2

		# geographical requirement changes after the crusades
		iGameTurn = gc.getGame().getGameTurn()
		if iGameTurn < tCompaniesDeath[iTemplars]:
			if iCompany in [iHospitallers, iTemplars, iTeutons]:
				if iStateReligion == iCatholicism:
					if iProvince in [xml.iP_Antiochia, xml.iP_Lebanon, xml.iP_Jerusalem]:
						iValue += 5
					elif iProvince in [xml.iP_Cyprus, xml.iP_Egypt]:
						iValue += 3
		else:
			if iCompany == iHospitallers:
				if iProvince in [xml.iP_Rhodes, xml.iP_Malta]:
					iValue += 4
			elif iCompany == iTeutons:
				if iProvince == xml.iP_Transylvania:
					iValue += 2

		# additional bonus for the city of Jerusalem
		if (city.getX(), city.getY()) == con.tJerusalem:
			if iCompany in [iHospitallers, iTemplars, iTeutons]:
				iValue += 3

		# coastal and riverside check
		if iCompany == iHansa:
			if not city.isCoastal(20): # water body with at least 20 tiles
				if not city.plot().isRiverSide():
					return -1
		elif iCompany == iHospitallers:
			if city.isCoastal(20):
				iValue += 2

		# bonus for religions in the city
		if iCompany in [iHansa, iMedici, iAugsburg, iStGeorge]:
			if city.isHasReligion(iJudaism): # not necessarily historic, but has great gameplay synergies
				iValue += 1
		elif iCompany in [iHospitallers, iTemplars, iTeutons, iCalatrava]:
			# they have a harder time to choose a city without Catholicism, but they spread the religion there
			if not city.isHasReligion(iCatholicism):
				iValue -= 1
			if city.isHasReligion(iIslam):
				iValue -= 1
		elif iCompany == iDragon:
			if city.isHasReligion(iCatholicism) or city.isHasReligion(iOrthodoxy):
				iValue += 1
			if city.isHasReligion(iIslam):
				iValue -= 1

		# faith points of the population
		if iCompany in [iHospitallers, iTemplars, iTeutons, iCalatrava]:
			#print ("faith points:", city.getOwner(), owner.getFaith())
			if owner.getFaith() >= 50:
				iValue += 3
			elif owner.getFaith() >= 30:
				iValue += 2
			elif owner.getFaith() >= 15:
				iValue += 1

		# city size
		if iCompany in [iHansa, iDragon, iMedici, iAugsburg, iStGeorge]:
			if city.getPopulation() > 9:
				iValue += 3
			elif city.getPopulation() > 6:
				iValue += 2
			elif city.getPopulation() > 3:
				iValue += 1

		# various building bonuses, trade route bonus
		iBuildCounter = 0 # building bonus counter: we don't want buildings to be the deciding factor in company spread
		if iCompany in [iHospitallers, iTemplars, iTeutons]:
			iMaxPossible = 11 # building bonus counter: we don't want buildings to be the deciding factor in company spread
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWalls)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCastle)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iBarracks)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iStable)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iArcheryRange)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iForge)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCatholicTemple)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCatholicMonastery)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iGuildHall)) > 0: iBuildCounter += 1
			iValue += (4 * iBuildCounter) / iMaxPossible # maximum is 4, with all buildings built
			# wonders should be handled separately
			if city.getNumRealBuilding(xml.iKrakDesChevaliers) > 0:
				if iCompany == iHospitallers: iValue += 5
				else: iValue += 2
			if city.getNumRealBuilding(xml.iDomeRock) > 0:
				if iCompany == iTemplars: iValue += 5
				else: iValue += 2
		elif iCompany == iCalatrava:
			iMaxPossible = 11 # building bonus counter: we don't want buildings to be the deciding factor in company spread
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWalls)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCastle)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iBarracks)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iStable)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iArcheryRange)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iForge)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCatholicTemple)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCatholicMonastery)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iStarFort)) > 0: iBuildCounter += 1
			iValue += (5 * iBuildCounter) / iMaxPossible # maximum is 5, with all buildings built
		elif iCompany == iDragon:
			iMaxPossible = 9 # building bonus counter: we don't want buildings to be the deciding factor in company spread
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWalls)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCastle)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iBarracks)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iStable)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iArcheryRange)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iForge)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iStarFort)) > 0: iBuildCounter += 2
			iValue += (5 * iBuildCounter) / iMaxPossible # maximum is 5, with all buildings built
		elif iCompany in [iMedici, iAugsburg, iStGeorge]:
			iMaxPossible = 11 # building bonus counter: we don't want buildings to be the deciding factor in company spread
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iMarket)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iBank)) > 0: iBuildCounter += 3
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iJeweler)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iGuildHall)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iLuxuryStore)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCourthouse)) > 0: iBuildCounter += 2
			iValue += (5 * iBuildCounter) / iMaxPossible # maximum is 5, with all buildings built
			# wonders should be handled separately
			if city.getNumRealBuilding(xml.iPalace) > 0: iValue += 1
			if city.getNumRealBuilding(xml.iSummerPalace) > 0: iValue += 1
			# bonus from trade routes
			iValue += max(0, city.getTradeRoutes() - 1)
		elif iCompany == iHansa:
			iMaxPossible = 16 # building bonus counter: we don't want buildings to be the deciding factor in company spread
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iHarbor)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iLighthouse)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWharf)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iCustomHouse)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iMarket)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iBrewery)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWeaver)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iGuildHall)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iWarehouse)) > 0: iBuildCounter += 2
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iTannery)) > 0: iBuildCounter += 1
			if city.getNumRealBuilding(utils.getUniqueBuilding(iOwner, xml.iTextileMill)) > 0: iBuildCounter += 1
			iValue += (6 * iBuildCounter) / iMaxPossible # maximum is 6, with all buildings built
			# bonus from trade routes
			iValue += city.getTradeRoutes()

		# civic bonuses
		if owner.getCivics(0) == xml.iCivicMerchantRepublic:
			if iCompany in [iMedici, iStGeorge, iHospitallers]:
				iValue += 1
			elif iCompany == iHansa:
				iValue += 2
		if owner.getCivics(1) == xml.iCivicFeudalLaw:
			if iCompany in [iHospitallers, iTemplars, iTeutons, iDragon, iCalatrava]:
				iValue += 2
		elif owner.getCivics(1) == xml.iCivicReligiousLaw:
			if iCompany in [iHospitallers, iTemplars, iTeutons, iCalatrava]:
				iValue += 1
		if owner.getCivics(2) == xml.iCivicApprenticeship:
			if iCompany == iHansa:
				iValue += 1
		if owner.getCivics(3) == xml.iCivicTradeEconomy:
			if iCompany in [iMedici, iAugsburg, iStGeorge]:
				iValue += 1
			elif iCompany == iHansa:
				iValue += 2
		elif owner.getCivics(3) == xml.iCivicGuilds:
			if iCompany in [iHospitallers, iTemplars, iTeutons, iHansa, iDragon, iCalatrava]:
				iValue += 1
		elif owner.getCivics(3) == xml.iCivicMercantilism:
			if iCompany == iHansa:
				return -1
			elif iCompany in [iMedici, iAugsburg, iStGeorge]:
				iValue -= 2
		if owner.getCivics(4) == xml.iCivicTheocracy:
			if iCompany in [iHospitallers, iTemplars]:
				iValue += 1
			elif iCompany == iTeutons:
				iValue += 2
		elif owner.getCivics(4) == xml.iCivicFreeReligion:
			if iCompany in [iHospitallers, iTemplars, iTeutons, iDragon]:
				iValue -= 1
			elif iCompany == iCalatrava:
				iValue -= 2
		if owner.getCivics(5) == xml.iCivicOccupation:
			if iCompany in [iHospitallers, iTemplars, iCompany, iCompany == iCalatrava]:
				iValue += 1

		# bonus for techs
		if iCompany in [iHospitallers, iTemplars, iTeutons, iDragon, iCalatrava]:
			for iTech in [xml.iChivalry, xml.iPlateArmor, xml.iGuilds, xml.iMilitaryTradition]:
				if ownerTeam.isHasTech(iTech):
					iValue += 1
		elif iCompany == iHansa:
			for iTech in [xml.iGuilds, xml.iClockmaking, xml.iOptics, xml.iShipbuilding]:
				if ownerTeam.isHasTech(iTech):
					iValue += 1
		elif iCompany in [iMedici, iStGeorge]:
			for iTech in [xml.iBanking, xml.iPaper, xml.iClockmaking, xml.iOptics, xml.iShipbuilding]:
				if ownerTeam.isHasTech(iTech):
					iValue += 1
		elif iCompany == iAugsburg:
			for iTech in [xml.iBanking, xml.iPaper, xml.iChemistry]:
				if ownerTeam.isHasTech(iTech):
					iValue += 1

		# resources
		iTempValue = 0
		bFound = False
		for i in range(4):
			iBonus = gc.getCorporationInfo(iCompany).getPrereqBonus(i)
			if iBonus > -1:
				if city.getNumBonuses(iBonus) > 0:
					bFound = True
					if iCompany in [iHospitallers, iTemplars, iTeutons, iDragon, iCalatrava]:
						iTempValue += city.getNumBonuses(iBonus) + 2 # 3 for the first bonus, 1 for the rest of the same type
					else:
						iTempValue += (city.getNumBonuses(iBonus) + 1) * 2 # 4 for the first bonus, 2 for the rest
		if iCompany in [iHansa, iMedici, iAugsburg, iStGeorge] and not bFound: return -1
		# we don't want the bonus to get too big, and dominate the selection values
		iValue += iTempValue / 4

		# bonus for resources in the fat cross of a city?

		# competition
		if iCompany == iHospitallers:
			if city.isHasCorporation(iTemplars):
				iValue *= 2
				iValue /= 3
			if city.isHasCorporation(iTeutons):
				iValue *= 2
				iValue /= 3
		elif iCompany == iTemplars:
			if city.isHasCorporation(iHospitallers):
				iValue *= 2
				iValue /= 3
			if city.isHasCorporation(iTeutons):
				iValue *= 2
				iValue /= 3
		elif iCompany == iTeutons:
			if city.isHasCorporation(iTemplars):
				iValue *= 2
				iValue /= 3
			if city.isHasCorporation(iHospitallers):
				iValue *= 2
				iValue /= 3
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
		iCompOwned = owner.countCorporations(iCompany)
		if city.isHasCorporation(iCompany):
			iValue -= iCompOwned # -1 per city if the company is already present
		else:
			iValue -= 2 * iCompOwned # -2 if it's a possible new city
		if iCompOwned > 0:
			print ("Number of companies already present in civ:", city.getName(), iCompOwned)

		return iValue


	def addCompany(self, iCompany, iNumber):

		# adds the company to the best iNumber cities
		cityValueList = []
		iCompaniesAdded = 0
		for iPlayer in range(iNumPlayers):
			for city in utils.getCityList(iPlayer):
				iValue = self.getCityValue(city, iCompany)
				if iValue > 0:
					cityValueList.append((city, iValue * 10 + gc.getGame().getSorenRandNum(10, 'random bonus')))
		# sort cities from highest to lowest value
		cityValueList.sort(key=itemgetter(1), reverse=True)
		# spread the company
		for (city, _) in cityValueList:
			if not city.isHasCorporation(iCompany):
				city.setHasCorporation(iCompany, True, True, True)
				city.setHasRealBuilding(lCompanyBuilding[iCompany], True)
				print ("Company added under special circumstance:", city.getName(), iCompany)
				iCompaniesAdded += 1
				if iCompaniesAdded == iNumber:
					break

