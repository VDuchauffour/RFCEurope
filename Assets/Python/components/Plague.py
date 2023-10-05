# Rhye's and Fall of Civilization: Europe - Plague

from CvPythonExtensions import *
from CivilizationsData import CIVILIZATIONS
from CoreTypes import Civ
import PyHelpers
import XMLConsts as xml
import RFCUtils

from StoredData import sd
import random

from MiscData import PLAGUE_IMMUNITY, MessageData
from TimelineData import CIV_BIRTHDATE
from CoreStructures import get_civ_by_id

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
utils = RFCUtils.RFCUtils()


iPlague = xml.iPlague

# Absinthe: Black Death is more severe, while the Plague of Justinian is less severe than the others plagues
iBaseHumanDuration = 10
iBaseAIDuration = 6
iNumPlagues = 5
iConstantinople = 0
iBlackDeath = 1


class Plague:

    ##################################################
    ### Secure storage & retrieval of script data ###
    ################################################

    def getPlagueCountdown(self, iCiv):
        return sd.scriptDict["lPlagueCountdown"][iCiv]

    def setPlagueCountdown(self, iCiv, iNewValue):
        sd.scriptDict["lPlagueCountdown"][iCiv] = iNewValue

    def getGenericPlagueDates(self, i):
        return sd.scriptDict["lGenericPlagueDates"][i]

    def setGenericPlagueDates(self, i, iNewValue):
        sd.scriptDict["lGenericPlagueDates"][i] = iNewValue

    def getBadPlague(self):
        return sd.scriptDict["bBadPlague"]

    def setBadPlague(self, bBad):
        sd.scriptDict["bBadPlague"] = bBad

    def getFirstPlague(self):
        return sd.scriptDict["bFirstPlague"]

    def setFirstPlague(self, bFirst):
        sd.scriptDict["bFirstPlague"] = bFirst

    #######################################
    ### Main methods (Event-Triggered) ###
    #####################################

    def setup(self):

        for i in CIVILIZATIONS.majors().ids():
            self.setPlagueCountdown(i, -PLAGUE_IMMUNITY)

        # Sedna17: Set number of GenericPlagues in StoredData
        # 3Miro: Plague 0 strikes France too hard, make it less random and force it to pick Byzantium as starting land
        self.setGenericPlagueDates(
            0, 28 + gc.getGame().getSorenRandNum(5, "Variation") - 10
        )  # Plagues of Constantinople
        self.setGenericPlagueDates(
            1, 247 + gc.getGame().getSorenRandNum(40, "Variation") - 20
        )  # 1341 Black Death
        self.setGenericPlagueDates(
            2, 300 + gc.getGame().getSorenRandNum(40, "Variation") - 20
        )  # Generic recurrence of plague
        self.setGenericPlagueDates(
            3, 375 + gc.getGame().getSorenRandNum(40, "Variation") - 30
        )  # 1650 Great Plague
        self.setGenericPlagueDates(
            4, 440 + gc.getGame().getSorenRandNum(40, "Variation") - 30
        )  # 1740 Small Pox
        for i in range(iNumPlagues):
            print("plagues", self.getGenericPlagueDates(i))

    def checkTurn(self, iGameTurn):

        for iPlayer in CIVILIZATIONS.ids():
            if gc.getPlayer(iPlayer).isAlive():
                if self.getPlagueCountdown(iPlayer) > 0:
                    self.setPlagueCountdown(iPlayer, self.getPlagueCountdown(iPlayer) - 1)
                    iPlagueCountDown = self.getPlagueCountdown(iPlayer)
                    if iPlagueCountDown == 2:
                        self.preStopPlague(iPlayer, iPlagueCountDown)
                    elif iPlagueCountDown == 1:
                        self.preStopPlague(iPlayer, iPlagueCountDown)
                    elif iPlagueCountDown == 0:
                        self.stopPlague(iPlayer)
                elif self.getPlagueCountdown(iPlayer) < 0:
                    self.setPlagueCountdown(iPlayer, self.getPlagueCountdown(iPlayer) + 1)

        for iPlague in range(iNumPlagues):
            if iGameTurn == self.getGenericPlagueDates(iPlague):
                self.startPlague(iPlague)

            # if the plague has stopped too quickly, restart
            if iGameTurn == self.getGenericPlagueDates(iPlague) + 4:
                # not on the first one, that's mostly for one civ anyway
                bFirstPlague = self.getFirstPlague()
                if not bFirstPlague:
                    iInfectedCounter = 0
                    for iPlayer in CIVILIZATIONS.ids():
                        if (
                            gc.getPlayer(iPlayer).isAlive()
                            and self.getPlagueCountdown(iPlayer) > 0
                        ):
                            iInfectedCounter += 1
                    if iInfectedCounter <= 1:
                        self.startPlague(iPlague)

    def checkPlayerTurn(self, iGameTurn, iPlayer):
        if iPlayer < CIVILIZATIONS.len():
            if self.getPlagueCountdown(iPlayer) > 0:
                self.processPlague(iPlayer)

    def startPlague(self, iPlagueCount):
        iWorstCiv = -1
        iWorstHealth = 100

        # Absinthe: specific plagues
        # Plague of Constantinople (that started at Alexandria)
        if iPlagueCount == iConstantinople:
            iWorstCiv = Civ.BYZANTIUM.value
            self.setFirstPlague(True)
            self.setBadPlague(False)
        # Black Death in the 14th century
        elif iPlagueCount == iBlackDeath:
            self.setFirstPlague(False)
            self.setBadPlague(True)
        # all the others
        else:
            self.setFirstPlague(False)
            self.setBadPlague(False)

        # try to find the most unhealthy civ
        if iWorstCiv == -1:
            for iPlayer in CIVILIZATIONS.majors().ids():
                pPlayer = gc.getPlayer(iPlayer)
                if pPlayer.isAlive():
                    if self.isVulnerable(iPlayer):
                        iHealth = self.calcHealth(iPlayer) - gc.getGame().getSorenRandNum(
                            10, "random modifier"
                        )
                        if iHealth < iWorstHealth:
                            iWorstCiv = iPlayer
                            iWorstHealth = iHealth

        # choose a random civ if we didn't find it
        if iWorstCiv == -1:
            iWorstCiv = utils.getRandomCiv()

        pWorstCiv = gc.getPlayer(iWorstCiv)
        city = utils.getRandomCity(iWorstCiv)
        if city != -1:
            self.spreadPlague(iWorstCiv, city)
            self.infectCity(city)

    def calcHealth(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        iTCH = pPlayer.calculateTotalCityHealthiness()
        iTCU = pPlayer.calculateTotalCityUnhealthiness()
        # Absinthe: use average city health instead
        iNumCities = pPlayer.getNumCities()
        if iNumCities == 0:
            return 0  # Avoid zero division error
        iAverageCityHealth = int(
            (10 * (iTCH - iTCU)) / iNumCities
        )  # 10x the average health actually
        print("iAverageCityHealth", iAverageCityHealth)
        return iAverageCityHealth
        # if ( iTCH > 0 ):
        # 	return int((10.0 * iTCH) / (iTCH + iTCU)) - 5 # theoretically between 5 and -5, but almost always between -2 and +2
        # else:
        # 	return -4

    def isVulnerable(self, iPlayer):
        # Absinthe: based on recent infections and the average city healthiness (also tech immunity should go here if it's ever added to the mod)
        if iPlayer >= CIVILIZATIONS.majors().len():
            if self.getPlagueCountdown(iPlayer) == 0:
                return True
        else:
            pPlayer = gc.getPlayer(iPlayer)
            if self.getPlagueCountdown(iPlayer) == 0:
                # Absinthe: health doesn't matter for the Black Death, everyone is vulnerable
                bBadPlague = self.getBadPlague()
                if bBadPlague:
                    return True
                else:
                    iHealth = self.calcHealth(iPlayer)
                    if (
                        iHealth < 42
                    ):  # won't spread at all if the average surplus health in the cities is at least 4.2
                        return True
        return False

    def spreadPlague(self, iPlayer, city):
        # Absinthe: the Plague of Justinian shouldn't spread to Italy and France, even if it was as deadly as the Black Death
        if (
            iPlayer in [Civ.FRANCE.value, Civ.POPE.value]
            and gc.getGame().getGameTurn() <= xml.i632AD
        ):
            return

        # Absinthe: message about the spread
        iHuman = utils.getHumanID()
        iHumanTeam = gc.getPlayer(iHuman).getTeam()
        if gc.getPlayer(iHuman).canContact(iPlayer) and iHuman != iPlayer:
            if city != -1 and city.isRevealed(iHumanTeam, False):
                CyInterface().addMessage(
                    iHuman,
                    True,
                    MessageData.DURATION / 2,
                    CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ())
                    + " "
                    + city.getName()
                    + " ("
                    + gc.getPlayer(city.getOwner()).getCivilizationAdjective(0)
                    + ")!",
                    "AS2D_PLAGUE",
                    0,
                    gc.getBuildingInfo(iPlague).getButton(),
                    ColorTypes(MessageData.LIME),
                    city.getX(),
                    city.getY(),
                    True,
                    True,
                )
            elif city != -1:
                pCiv = gc.getPlayer(city.getOwner())
                # print ("pCiv.getCivilizationDescriptionKey()", pCiv.getCivilizationDescriptionKey())
                # print ("pCiv.getCivilizationDescription(0)", pCiv.getCivilizationDescription(0))
                CyInterface().addMessage(
                    iHuman,
                    True,
                    MessageData.DURATION / 2,
                    CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CIV", ())
                    + " "
                    + pCiv.getCivilizationDescription(0)
                    + "!",
                    "AS2D_PLAGUE",
                    0,
                    "",
                    ColorTypes(MessageData.LIME),
                    -1,
                    -1,
                    True,
                    True,
                )

        # Absinthe: this is where the duration is handled for each civ
        # 			number of cities should be a significant factor, so plague isn't way more deadly for smaller civs
        iHealth = self.calcHealth(iPlayer)
        iHealthDuration = max(min((iHealth / 14), 3), -4)  # between -4 and +3
        iCityDuration = min(
            (gc.getPlayer(iPlayer).getNumCities() + 2) / 3, 10
        )  # between 1 and 10 from cities
        print("plague duration iCities", iCityDuration)
        if iPlayer == iHuman:
            # Overall duration for the plague is between 4 and 12 (usually between 6-8)
            iValue = (iBaseHumanDuration + iCityDuration - iHealthDuration) / 2
        else:
            # Overall duration for the plague is between 2 and 10 (usually around 5-6)
            iValue = max(
                ((iBaseAIDuration + iCityDuration - iHealthDuration) / 2), 4
            )  # at least 4
        print("plague duration overall, iPlayer, iValue", iPlayer, iValue)
        self.setPlagueCountdown(iPlayer, iValue)

    def infectCity(self, city):
        # Absinthe: the Plague of Justinian shouldn't spread to Italy and France, even if it was as deadly as the Black Death
        if (
            city.getOwner() in [Civ.FRANCE.value, Civ.POPE.value]
            and gc.getGame().getGameTurn() <= xml.i632AD
        ):
            return

        x = city.getX()
        y = city.getY()

        city.setHasRealBuilding(iPlague, True)
        if gc.getPlayer(city.getOwner()).isHuman():
            CyInterface().addMessage(
                city.getOwner(),
                True,
                MessageData.DURATION / 2,
                CyTranslator().getText("TXT_KEY_PLAGUE_SPREAD_CITY", ())
                + " "
                + city.getName()
                + "!",
                "AS2D_PLAGUE",
                0,
                gc.getBuildingInfo(iPlague).getButton(),
                ColorTypes(MessageData.LIME),
                x,
                y,
                True,
                True,
            )
        for (i, j) in utils.surroundingPlots((x, y), 2):
            pPlot = gc.getMap().plot(i, j)
            iImprovement = pPlot.getImprovementType()
            # Absinthe: chance for reducing the improvement vs. only resetting the process towards the next level to 0
            if iImprovement == xml.iImprovementTown:  # 100% chance to reduce towns
                pPlot.setImprovementType(xml.iImprovementVillage)
            elif iImprovement == xml.iImprovementVillage:
                iRand = gc.getGame().getSorenRandNum(100, "roll")
                if iRand < 75:  # 75% for reducing, 25% for resetting
                    pPlot.setImprovementType(xml.iImprovementHamlet)
                else:
                    pPlot.setUpgradeProgress(0)
            elif iImprovement == xml.iImprovementHamlet:
                iRand = gc.getGame().getSorenRandNum(100, "roll")
                if iRand < 50:  # 50% for reducing, 50% for resetting
                    pPlot.setImprovementType(xml.iImprovementCottage)
                else:
                    pPlot.setUpgradeProgress(0)
            elif iImprovement == xml.iImprovementCottage:
                iRand = gc.getGame().getSorenRandNum(100, "roll")
                if iRand < 25:  # 25% for reducing, 75% for resetting
                    pPlot.setImprovementType(-1)
                else:
                    pPlot.setUpgradeProgress(0)

        # Absinthe: one population is killed by default
        if city.getPopulation() > 1:
            city.changePopulation(-1)

        # Absinthe: plagues won't kill units instantly on spread anymore
        # 			Plague of Justinian deals even less initial damage
        bFirstPlague = self.getFirstPlague()
        if bFirstPlague:
            self.killUnitsByPlague(city, gc.getMap().plot(x, y), 0, 80, 0)
        else:
            self.killUnitsByPlague(city, gc.getMap().plot(x, y), 0, 90, 0)

    def killUnitsByPlague(self, city, plot, iThreshold, iDamage, iPreserveDefenders):
        iCityOwner = city.getOwner()
        pCityOwner = gc.getPlayer(iCityOwner)
        teamCityOwner = gc.getTeam(pCityOwner.getTeam())

        iNumUnitsInAPlot = plot.getNumUnits()
        iHuman = utils.getHumanID()
        iCityHealthRate = city.healthRate(False, 0)

        if iNumUnitsInAPlot > 0:
            # Absinthe: if we mix up the order of the units, health will be much less static for the chosen defender units
            bOrderChange = gc.getGame().getSorenRandNum(4, "roll") == 1
            for j in range(iNumUnitsInAPlot):
                if bOrderChange:
                    i = j  # we are counting from the strongest unit
                else:
                    i = iNumUnitsInAPlot - j - 1  # count back from the weakest unit
                unit = plot.getUnit(i)
                if (
                    utils.isMortalUnit(unit)
                    and gc.getGame().getSorenRandNum(100, "roll")
                    > iThreshold + 5 * iCityHealthRate
                ):
                    iUnitDamage = unit.getDamage()
                    # if some defenders are set to be preserved for some reason, they won't get more damage if they are already under 50%
                    if (
                        unit.getOwner() == iCityOwner
                        and iPreserveDefenders > 0
                        and unit.getDomainType() != 0
                        and unit.baseCombatStr() > 0
                    ):  # only units which can really defend
                        iPreserveDefenders -= 1
                        unit.setDamage(
                            max(
                                iUnitDamage,
                                min(
                                    50,
                                    iUnitDamage
                                    + iDamage
                                    - unit.getExperience() / 10
                                    - 3 * unit.baseCombatStr() / 7,
                                ),
                            ),
                            Civ.BARBARIAN.value,
                        )
                    else:
                        if unit.baseCombatStr() > 0:
                            if (
                                unit.getDomainType() == DomainTypes.DOMAIN_SEA
                            ):  # naval units get less damage, won't be killed unless they were very badly damaged originally
                                iShipDamage = iDamage * 93 / 100
                                iUnitDamage = max(
                                    iUnitDamage,
                                    unit.getDamage()
                                    + iShipDamage
                                    - unit.getExperience() / 10
                                    - 3 * unit.baseCombatStr() / 7,
                                )
                            else:
                                iUnitDamage = max(
                                    iUnitDamage,
                                    unit.getDamage()
                                    + iDamage
                                    - unit.getExperience() / 10
                                    - 3 * unit.baseCombatStr() / 7,
                                )
                        else:  # less damage for civilian units - workers, settlers, missionaries, etc.
                            iCivilDamage = (
                                iDamage * 96 / 100
                            )  # workers will be killed with any value here if they are automated (thus moving instead of healing)
                            iUnitDamage = max(iUnitDamage, unit.getDamage() + iCivilDamage)
                        # kill the unit if necessary
                        if iUnitDamage >= 100:
                            unit.kill(False, Civ.BARBARIAN.value)
                            if unit.getOwner() == iHuman:
                                CyInterface().addMessage(
                                    iHuman,
                                    False,
                                    MessageData.DURATION / 2,
                                    CyTranslator().getText(
                                        "TXT_KEY_PLAGUE_PROCESS_UNIT", (unit.getName(),)
                                    )
                                    + " "
                                    + city.getName()
                                    + "!",
                                    "AS2D_PLAGUE",
                                    0,
                                    gc.getBuildingInfo(iPlague).getButton(),
                                    ColorTypes(MessageData.LIME),
                                    plot.getX(),
                                    plot.getY(),
                                    True,
                                    True,
                                )
                        else:
                            unit.setDamage(iUnitDamage, Civ.BARBARIAN.value)
                        # if we have many units in the same plot, decrease the damage for every other unit
                        iDamage *= 7
                        iDamage /= 8

    def processPlague(self, iPlayer):
        bBadPlague = self.getBadPlague()
        bFirstPlague = self.getFirstPlague()
        pPlayer = gc.getPlayer(iPlayer)
        iHuman = utils.getHumanID()

        lInfectedCities = [
            city for city in utils.getCityList(iPlayer) if city.hasBuilding(iPlague)
        ]
        lNotInfectedCities = [
            city for city in utils.getCityList(iPlayer) if not city.hasBuilding(iPlague)
        ]

        # first spread to close locations
        for city in lInfectedCities:
            # kill citizens
            if city.getPopulation() > 1:
                # the plague itself also greatly contributes to unhealth, so the health rate will almost always be negative
                iHealthRate = city.goodHealth() - city.badHealth(False)
                # always between -5 and +5
                iHealthRate = max(-5, min(5, iHealthRate))

                iRandom = gc.getGame().getSorenRandNum(100, "roll")
                iPopSize = city.getPopulation()
                if bBadPlague:  # if it's the Black Death, bigger chance for population loss
                    bKill = iRandom < 10 + 10 * (iPopSize - 4) - 5 * iHealthRate
                elif (
                    bFirstPlague
                ):  # if it's the Plague of Justinian, smaller chance for population loss
                    bKill = iRandom < 10 * (iPopSize - 4) - 5 * iHealthRate
                else:
                    # in "normal" plagues the range for a given pop size is from 10*(size-6) to 10*(size-1)
                    # so with size 2: from -40 to 10, size 5: -10 to 40, size 8: 20 to 70, size 12: 60 to 110, size 15: 90 to 140
                    bKill = iRandom < 5 + 10 * (iPopSize - 4) - 5 * iHealthRate
                if bKill:
                    city.changePopulation(-1)
                    if iPlayer == iHuman:
                        CyInterface().addMessage(
                            iHuman,
                            False,
                            MessageData.DURATION / 2,
                            CyTranslator().getText(
                                "TXT_KEY_PLAGUE_PROCESS_CITY", (city.getName(),)
                            )
                            + " "
                            + city.getName()
                            + "!",
                            "AS2D_PLAGUE",
                            0,
                            gc.getBuildingInfo(iPlague).getButton(),
                            ColorTypes(MessageData.LIME),
                            city.getX(),
                            city.getY(),
                            True,
                            True,
                        )

            # infect vassals
            if self.getPlagueCountdown(iPlayer) > 2:  # don't spread in the last turns
                if city.isCapital():
                    for iLoopCiv in CIVILIZATIONS.majors().ids():
                        if gc.getTeam(pPlayer.getTeam()).isVassal(iLoopCiv) or gc.getTeam(
                            gc.getPlayer(iLoopCiv).getTeam()
                        ).isVassal(iPlayer):
                            if (
                                gc.getPlayer(iLoopCiv).getNumCities() > 0
                            ):  # this check is needed, otherwise game crashes
                                if self.isVulnerable(iLoopCiv):
                                    capital = gc.getPlayer(iLoopCiv).getCapitalCity()
                                    self.spreadPlague(iLoopCiv, capital)
                                    self.infectCity(capital)

            # spread plague in 2 distance around the city
            if self.getPlagueCountdown(iPlayer) > 2:  # don't spread in the last turns
                for (x, y) in utils.surroundingPlots((city.getX(), city.getY()), 2):
                    plot = gc.getMap().plot(x, y)

                    if not plot.isOwned():
                        continue
                    if (city.getX(), city.getY()) == (x, y):
                        continue

                    if plot.getOwner() == iPlayer:
                        if plot.isCity():
                            cityNear = plot.getPlotCity()
                            if not cityNear.isHasRealBuilding(iPlague):
                                self.infectCity(cityNear)
                    else:
                        if self.isVulnerable(plot.getOwner()):
                            self.spreadPlague(plot.getOwner(), -1)
                            self.infectCitiesNear(plot.getOwner(), x, y)

            # kill units around the city
            for (x, y) in utils.surroundingPlots((city.getX(), city.getY()), 3):
                plot = gc.getMap().plot(x, y)
                iDistance = utils.calculateDistance(city.getX(), city.getY(), x, y)

                if iDistance == 0:  # City
                    self.killUnitsByPlague(city, plot, 20, 40, 2)
                elif not plot.isCity():
                    if iDistance == 1:
                        if plot.isRoute():
                            self.killUnitsByPlague(city, plot, 20, 30, 0)
                        else:
                            self.killUnitsByPlague(city, plot, 30, 30, 0)
                    elif iDistance == 2:
                        if plot.isRoute():
                            self.killUnitsByPlague(city, plot, 30, 30, 0)
                        else:
                            self.killUnitsByPlague(city, plot, 40, 30, 0)
                    else:
                        if plot.getOwner() == iPlayer or not plot.isOwned():
                            if plot.isRoute() or plot.isWater():
                                self.killUnitsByPlague(city, plot, 40, 30, 0)

            # spread by the trade routes
            if self.getPlagueCountdown(iPlayer) > 2:  # don't spread in the last turns
                for iTradeRoute in range(city.getTradeRoutes()):
                    loopCity = city.getTradeCity(iTradeRoute)
                    if not loopCity.isNone():
                        if not loopCity.hasBuilding(iPlague):
                            iOwner = loopCity.getOwner()
                            if iOwner == iPlayer:
                                self.infectCity(loopCity)
                            if self.isVulnerable(iOwner):
                                self.spreadPlague(iOwner, loopCity)
                                self.infectCity(loopCity)

        # Absinthe: spread to a couple cities which are not too far from already infected ones
        # 			cities are chosen randomly from the possible targets
        # 			the maximum number of infections is based on the size of the empire
        if (
            self.getPlagueCountdown(iPlayer) > 2
        ):  # don't spread in the last turns, when preStopPlague is active
            if lNotInfectedCities:
                iTotalCities = pPlayer.getNumCities()
                if iTotalCities > 21:
                    iMaxNumInfections = 4
                elif iTotalCities > 14:
                    iMaxNumInfections = 3
                elif iTotalCities > 7:
                    iMaxNumInfections = 2
                else:
                    iMaxNumInfections = 1

                iNumSpreads = (
                    gc.getGame().getSorenRandNum(iMaxNumInfections, "max number of new infections")
                    + 1
                )  # plagues are rather short, always spread at least once
                iNumSpreads = min(
                    len(lNotInfectedCities), iNumSpreads
                )  # in case there are not enough uninfected cities

                if iNumSpreads > 0:
                    iInfections = 0
                    random.shuffle(lNotInfectedCities)
                    for targetCity in lNotInfectedCities:
                        if [
                            city
                            for city in lInfectedCities
                            if targetCity.isConnectedTo(city)
                            and utils.calculateDistance(
                                targetCity.getX(), targetCity.getY(), city.getX(), city.getY()
                            )
                            <= 10
                        ]:
                            if not targetCity.hasBuilding(
                                iPlague
                            ):  # might have changed since the beginning of the function
                                self.infectCity(targetCity)
                                iInfections += 1
                                if iInfections >= iNumSpreads:
                                    break

        # if there are no cities with plague (gifted away, razed on conquest), but the civ itself has plague
        # there is a chance that it will spread to some of your cities
        # the civ would be immune otherwise, basically
        if len(lInfectedCities) == 0:
            if (
                self.getPlagueCountdown(iPlayer) > 2
            ):  # don't spread in the last turns, when preStopPlague is active
                iTotalCities = pPlayer.getNumCities()
                if iTotalCities > 21:
                    iMaxNumInfections = 4
                elif iTotalCities > 14:
                    iMaxNumInfections = 3
                elif iTotalCities > 7:
                    iMaxNumInfections = 2
                else:
                    iMaxNumInfections = 1
                iInfections = 0
                lAllCities = [city for city in utils.getCityList(iPlayer)]
                random.shuffle(lAllCities)
                for city in lAllCities:
                    if not city.hasBuilding(iPlague):
                        if gc.getGame().getSorenRandNum(10, "roll") < 2:
                            self.infectCity(city)
                            iInfections += 1
                            if iInfections >= iMaxNumInfections:
                                break

    def infectCitiesNear(self, iPlayer, startingX, startingY):
        cityList = [city for city in utils.getCityList(iPlayer) if not city.hasBuilding(iPlague)]
        for city in cityList:
            if utils.calculateDistance(city.getX(), city.getY(), startingX, startingY) <= 3:
                self.infectCity(city)

    def preStopPlague(self, iPlayer, iPlagueCountDown):
        cityList = [city for city in utils.getCityList(iPlayer) if city.hasBuilding(iPlague)]
        if cityList:
            iRemoveModifier = 0
            iTimeModifier = iPlagueCountDown * 15
            iPopModifier = 0
            iHealthModifier = 0
            # small cities should have a good chance to be chosen
            for city in cityList:
                # iPopModifier: -28, -21, -14, -7, 0, 7, 14, 21, 28, 35, etc.
                iPopModifier = 7 * city.getPopulation() - 35
                iHealthModifier = 5 * city.healthRate(False, 0)
                if gc.getGame().getSorenRandNum(100, "roll") < (
                    100 - iTimeModifier - iPopModifier + iHealthModifier - iRemoveModifier
                ):
                    city.setHasRealBuilding(iPlague, False)
                    iRemoveModifier += 5  # less chance for each city which already quit

    def stopPlague(self, iPlayer):
        self.setPlagueCountdown(iPlayer, -PLAGUE_IMMUNITY)
        for city in utils.getCityList(iPlayer):
            city.setHasRealBuilding(iPlague, False)

    def onCityAcquired(self, iOldOwner, iNewOwner, city):
        if city.hasBuilding(iPlague):
            # Absinthe: the Plague of Justinian shouldn't spread to Italy and France, even if it was as deadly as the Black Death
            if (
                city.getOwner() in [Civ.FRANCE.value, Civ.POPE.value]
                and gc.getGame().getGameTurn() <= xml.i632AD
            ):
                city.setHasRealBuilding(iPlague, False)
                return

            # only if it's not a recently born civ
            if (
                gc.getGame().getGameTurn()
                > CIV_BIRTHDATE[get_civ_by_id(iNewOwner)] + PLAGUE_IMMUNITY
            ):
                # reinfect the human player if conquering plagued cities
                if iNewOwner == utils.getHumanID():
                    # if > 0 do nothing, if < 0 skip immunity and restart the plague, if == 0 start the plague
                    if self.getPlagueCountdown(iNewOwner) <= 0:
                        self.spreadPlague(iNewOwner, -1)
                        for cityNear in utils.getCityList(iNewOwner):
                            if not cityNear.isHasRealBuilding(iPlague):
                                if (
                                    utils.calculateDistance(
                                        city.getX(), city.getY(), cityNear.getX(), cityNear.getY()
                                    )
                                    <= 3
                                ):
                                    if gc.getGame().getSorenRandNum(10, "roll") < 5:
                                        self.infectCity(cityNear)
                # no reinfect for the AI, only infect
                else:
                    # if > 0 do nothing, if < 0 keep immunity and remove plague from the city, if == 0 start the plague
                    if self.getPlagueCountdown(iNewOwner) == 0:
                        self.spreadPlague(iNewOwner, -1)
                        for cityNear in utils.getCityList(iNewOwner):
                            if not cityNear.isHasRealBuilding(iPlague):
                                if (
                                    utils.calculateDistance(
                                        city.getX(), city.getY(), cityNear.getX(), cityNear.getY()
                                    )
                                    <= 3
                                ):
                                    if gc.getGame().getSorenRandNum(10, "roll") < 5:
                                        self.infectCity(cityNear)
                    elif self.getPlagueCountdown(iNewOwner) < 0:
                        city.setHasRealBuilding(iPlague, False)
            else:
                city.setHasRealBuilding(iPlague, False)

    def onCityRazed(self, city, iNewOwner):
        pass
