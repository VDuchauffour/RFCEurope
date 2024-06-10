# Rhye's and Fall of Civilization: Europe - Plague

from CvPythonExtensions import *
from Consts import MessageData
from CoreData import civilizations, civilization
from Core import (
    message,
    location,
    owner,
    text,
    human,
    player,
    turn,
    year,
    city as _city,
    plot as _plot,
    cities,
    plots,
)
from CoreTypes import PlagueType, Improvement, Civ
from PyUtils import percentage, percentage_chance, rand

from RFCUtils import calculateDistance, getPlagueCountdown, isMortalUnit, setPlagueCountdown
from StoredData import data
import random

from MiscData import PLAGUE_IMMUNITY

gc = CyGlobalContext()


# Absinthe: Black Death is more severe, while the Plague of Justinian is less severe than the others plagues
iBaseHumanDuration = 10
iBaseAIDuration = 6
iNumPlagues = 5
iConstantinople = 0
iBlackDeath = 1


class Plague:
    def getGenericPlagueDates(self, i):
        return data.lGenericPlagueDates[i]

    def setGenericPlagueDates(self, i, iNewValue):
        data.lGenericPlagueDates[i] = iNewValue

    def getBadPlague(self):
        return data.bBadPlague

    def setBadPlague(self, bBad):
        data.bBadPlague = bBad

    def getFirstPlague(self):
        return data.bFirstPlague

    def setFirstPlague(self, bFirst):
        data.bFirstPlague = bFirst

    #######################################
    ### Main methods (Event-Triggered) ###
    #####################################

    def setup(self):

        for i in civilizations().majors().ids():
            setPlagueCountdown(i, -PLAGUE_IMMUNITY)

        # Sedna17: Set number of GenericPlagues in StoredData
        # 3Miro: Plague 0 strikes France too hard, make it less random and force it to pick Byzantium as starting land
        self.setGenericPlagueDates(0, 28 + rand(5) - 10)  # Plagues of Constantinople
        self.setGenericPlagueDates(1, 247 + rand(40) - 20)  # 1341 Black Death
        self.setGenericPlagueDates(2, 300 + rand(40) - 20)  # Generic recurrence of plague
        self.setGenericPlagueDates(3, 375 + rand(40) - 30)  # 1650 Great Plague
        self.setGenericPlagueDates(4, 440 + rand(40) - 30)  # 1740 Small Pox

    def checkTurn(self, iGameTurn):

        for iPlayer in civilizations().ids():
            if gc.getPlayer(iPlayer).isAlive():
                if getPlagueCountdown(iPlayer) > 0:
                    setPlagueCountdown(iPlayer, getPlagueCountdown(iPlayer) - 1)
                    iPlagueCountDown = getPlagueCountdown(iPlayer)
                    if iPlagueCountDown == 2:
                        self.preStopPlague(iPlayer, iPlagueCountDown)
                    elif iPlagueCountDown == 1:
                        self.preStopPlague(iPlayer, iPlagueCountDown)
                    elif iPlagueCountDown == 0:
                        self.stopPlague(iPlayer)
                elif getPlagueCountdown(iPlayer) < 0:
                    setPlagueCountdown(iPlayer, getPlagueCountdown(iPlayer) + 1)

        for iPlague in range(iNumPlagues):
            if iGameTurn == self.getGenericPlagueDates(iPlague):
                self.startPlague(iPlague)

            # if the plague has stopped too quickly, restart
            if iGameTurn == self.getGenericPlagueDates(iPlague) + 4:
                # not on the first one, that's mostly for one civ anyway
                bFirstPlague = self.getFirstPlague()
                if not bFirstPlague:
                    iInfectedCounter = 0
                    for iPlayer in civilizations().ids():
                        if gc.getPlayer(iPlayer).isAlive() and getPlagueCountdown(iPlayer) > 0:
                            iInfectedCounter += 1
                    if iInfectedCounter <= 1:
                        self.startPlague(iPlague)

    def checkPlayerTurn(self, iGameTurn, iPlayer):
        if iPlayer < civilizations().len():
            if getPlagueCountdown(iPlayer) > 0:
                self.processPlague(iPlayer)

    def startPlague(self, iPlagueCount):
        iWorstCiv = -1
        iWorstHealth = 100

        # Absinthe: specific plagues
        # Plague of Constantinople (that started at Alexandria)
        if iPlagueCount == iConstantinople:
            iWorstCiv = Civ.BYZANTIUM
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
            for iPlayer in civilizations().majors().ids():
                pPlayer = gc.getPlayer(iPlayer)
                if pPlayer.isAlive():
                    if self.isVulnerable(iPlayer):
                        iHealth = self.calcHealth(iPlayer) - rand(10)
                        if iHealth < iWorstHealth:
                            iWorstCiv = iPlayer
                            iWorstHealth = iHealth

        # choose a random civ if we didn't find it
        if iWorstCiv == -1:
            iWorstCiv = civilizations().majors().alive().random().unwrap().id

        city = cities().owner(iWorstCiv).random_entry()
        if city is not None:
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
        return iAverageCityHealth

    def isVulnerable(self, iPlayer):
        # Absinthe: based on recent infections and the average city healthiness (also tech immunity should go here if it's ever added to the mod)
        if iPlayer >= civilizations().majors().len():
            if getPlagueCountdown(iPlayer) == 0:
                return True
        else:
            if getPlagueCountdown(iPlayer) == 0:
                # Absinthe: health doesn't matter for the Black Death, everyone is vulnerable
                if self.getBadPlague():
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
        if iPlayer in [Civ.FRANCE, Civ.POPE] and turn() <= year(632):
            return

        # Absinthe: message about the spread
        iHuman = human()
        iHumanTeam = gc.getPlayer(iHuman).getTeam()
        if gc.getPlayer(iHuman).canContact(iPlayer) and iHuman != iPlayer:
            if city != -1 and city.isRevealed(iHumanTeam, False):
                message(
                    iHuman,
                    text("TXT_KEY_PLAGUE_SPREAD_CITY")
                    + " "
                    + city.getName()
                    + " ("
                    + gc.getPlayer(city.getOwner()).getCivilizationAdjective(0)
                    + ")!",
                    force=True,
                    sound="AS2D_PLAGUE",
                    button=gc.getBuildingInfo(PlagueType.PLAGUE).getButton(),
                    color=MessageData.LIME,
                    location=city,
                )
            elif city != -1:
                pCiv = gc.getPlayer(city.getOwner())
                message(
                    iHuman,
                    text("TXT_KEY_PLAGUE_SPREAD_CIV")
                    + " "
                    + pCiv.getCivilizationDescription(0)
                    + "!",
                    force=True,
                    sound="AS2D_PLAGUE",
                    color=MessageData.LIME,
                )

        # Absinthe: this is where the duration is handled for each civ
        # 			number of cities should be a significant factor, so plague isn't way more deadly for smaller civs
        iHealth = self.calcHealth(iPlayer)
        iHealthDuration = max(min((iHealth / 14), 3), -4)  # between -4 and +3
        iCityDuration = min(
            (gc.getPlayer(iPlayer).getNumCities() + 2) / 3, 10
        )  # between 1 and 10 from cities
        if iPlayer == iHuman:
            # Overall duration for the plague is between 4 and 12 (usually between 6-8)
            iValue = (iBaseHumanDuration + iCityDuration - iHealthDuration) / 2
        else:
            # Overall duration for the plague is between 2 and 10 (usually around 5-6)
            iValue = max(
                ((iBaseAIDuration + iCityDuration - iHealthDuration) / 2), 4
            )  # at least 4
        setPlagueCountdown(iPlayer, iValue)

    def infectCity(self, city):
        # Absinthe: the Plague of Justinian shouldn't spread to Italy and France, even if it was as deadly as the Black Death
        if city.getOwner() in [Civ.FRANCE, Civ.POPE] and turn() <= year(632):
            return

        city.setHasRealBuilding(PlagueType.PLAGUE, True)
        if player(city).isHuman():
            message(
                city.getOwner(),
                text("TXT_KEY_PLAGUE_SPREAD_CITY") + " " + city.getName() + "!",
                force=True,
                sound="AS2D_PLAGUE",
                button=gc.getBuildingInfo(PlagueType.PLAGUE).getButton(),
                color=MessageData.LIME,
                location=location(city),
            )

        for plot in plots().surrounding(city, radius=2).entities():
            iImprovement = plot.getImprovementType()
            # Absinthe: chance for reducing the improvement vs. only resetting the process towards the next level to 0
            if iImprovement == Improvement.TOWN:  # 100% chance to reduce towns
                plot.setImprovementType(Improvement.VILLAGE)
            elif iImprovement == Improvement.VILLAGE:
                if percentage_chance(75, strict=True):
                    plot.setImprovementType(Improvement.HAMLET)
                else:
                    plot.setUpgradeProgress(0)
            elif iImprovement == Improvement.HAMLET:
                if percentage_chance(50, strict=True):
                    plot.setImprovementType(Improvement.COTTAGE)
                else:
                    plot.setUpgradeProgress(0)
            elif iImprovement == Improvement.COTTAGE:
                if percentage_chance(25, strict=True):
                    plot.setImprovementType(-1)
                else:
                    plot.setUpgradeProgress(0)

        # Absinthe: one population is killed by default
        if city.getPopulation() > 1:
            city.changePopulation(-1)

        # Absinthe: plagues won't kill units instantly on spread anymore
        # 			Plague of Justinian deals even less initial damage
        bFirstPlague = self.getFirstPlague()
        if bFirstPlague:
            self.killUnitsByPlague(city, _plot(city), 0, 80, 0)
        else:
            self.killUnitsByPlague(city, _plot(city), 0, 90, 0)

    def killUnitsByPlague(self, city, plot, iThreshold, iDamage, iPreserveDefenders):
        iCityOwner = city.getOwner()
        pCityOwner = gc.getPlayer(iCityOwner)
        teamCityOwner = gc.getTeam(pCityOwner.getTeam())

        iNumUnitsInAPlot = plot.getNumUnits()
        iHuman = human()
        iCityHealthRate = city.healthRate(False, 0)

        if iNumUnitsInAPlot > 0:
            # Absinthe: if we mix up the order of the units, health will be much less static for the chosen defender units
            bOrderChange = percentage_chance(25)
            for j in range(iNumUnitsInAPlot):
                if bOrderChange:
                    i = j  # we are counting from the strongest unit
                else:
                    i = iNumUnitsInAPlot - j - 1  # count back from the weakest unit
                unit = plot.getUnit(i)
                if isMortalUnit(unit) and percentage_chance(
                    iThreshold + 5 * iCityHealthRate, strict=True, reverse=True
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
                            Civ.BARBARIAN,
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
                            unit.kill(False, Civ.BARBARIAN)
                            if unit.getOwner() == iHuman:
                                message(
                                    iHuman,
                                    text("TXT_KEY_PLAGUE_PROCESS_UNIT", unit.getName())
                                    + " "
                                    + city.getName()
                                    + "!",
                                    force=False,
                                    sound="AS2D_PLAGUE",
                                    button=gc.getBuildingInfo(PlagueType.PLAGUE).getButton(),
                                    color=MessageData.LIME,
                                    location=plot,
                                )
                        else:
                            unit.setDamage(iUnitDamage, Civ.BARBARIAN)
                        # if we have many units in the same plot, decrease the damage for every other unit
                        iDamage *= 7
                        iDamage /= 8

    def processPlague(self, iPlayer):
        bBadPlague = self.getBadPlague()
        bFirstPlague = self.getFirstPlague()
        pPlayer = gc.getPlayer(iPlayer)
        iHuman = human()

        lInfectedCities = cities().owner(iPlayer).building(PlagueType.PLAGUE).entities()
        lNotInfectedCities = cities().owner(iPlayer).not_building(PlagueType.PLAGUE).entities()

        # first spread to close locations
        for city in lInfectedCities:
            # kill citizens
            if city.getPopulation() > 1:
                # the plague itself also greatly contributes to unhealth, so the health rate will almost always be negative
                iHealthRate = city.goodHealth() - city.badHealth(False)
                # always between -5 and +5
                iHealthRate = max(-5, min(5, iHealthRate))

                iRandom = percentage()
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
                        message(
                            iHuman,
                            text("TXT_KEY_PLAGUE_PROCESS_CITY", city.getName())
                            + " "
                            + city.getName()
                            + "!",
                            force=False,
                            sound="AS2D_PLAGUE",
                            button=gc.getBuildingInfo(PlagueType.PLAGUE).getButton(),
                            color=MessageData.LIME,
                            location=city,
                        )

            # infect vassals
            if getPlagueCountdown(iPlayer) > 2:  # don't spread in the last turns
                if city.isCapital():
                    for iLoopCiv in civilizations().majors().ids():
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
            if getPlagueCountdown(iPlayer) > 2:  # don't spread in the last turns
                for plot in (
                    plots()
                    .surrounding(city, radius=2)
                    .filter(lambda p: p.isOwned())
                    .without(city)
                    .entities()
                ):
                    if (
                        owner(plot, iPlayer)
                        and plot.isCity()
                        and not _city(plot).isHasRealBuilding(PlagueType.PLAGUE)
                    ):
                        self.infectCity(_city(plot))
                    else:
                        if self.isVulnerable(plot.getOwner()):
                            self.spreadPlague(plot.getOwner(), -1)
                            self.infectCitiesNear(plot.getOwner(), *location(plot))
            # kill units around the city
            for plot in plots().surrounding(city, radius=3).entities():
                iDistance = calculateDistance(city.getX(), city.getY(), *location(plot))
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
            if getPlagueCountdown(iPlayer) > 2:  # don't spread in the last turns
                for iTradeRoute in range(city.getTradeRoutes()):
                    loopCity = city.getTradeCity(iTradeRoute)
                    if not loopCity.isNone():
                        if not loopCity.isHasRealBuilding(PlagueType.PLAGUE):
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
            getPlagueCountdown(iPlayer) > 2
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

                # plagues are rather short, always spread at least once
                iNumSpreads = min(1, len(lNotInfectedCities), rand(iMaxNumInfections))

                iInfections = 0
                random.shuffle(lNotInfectedCities)
                for targetCity in lNotInfectedCities:
                    if [
                        city
                        for city in lInfectedCities
                        if targetCity.isConnectedTo(city)
                        and calculateDistance(
                            targetCity.getX(), targetCity.getY(), city.getX(), city.getY()
                        )
                        <= 10
                    ]:
                        if not targetCity.isHasRealBuilding(PlagueType.PLAGUE):
                            # might have changed since the beginning of the function
                            self.infectCity(targetCity)
                            iInfections += 1
                            if iInfections >= iNumSpreads:
                                break

        # if there are no cities with plague (gifted away, razed on conquest), but the civ itself has plague
        # there is a chance that it will spread to some of your cities
        # the civ would be immune otherwise, basically
        if len(lInfectedCities) == 0:
            if (
                getPlagueCountdown(iPlayer) > 2
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
                _cities = cities().owner(iPlayer).not_building(PlagueType.PLAGUE).entities()
                # TODO fix shuffle
                random.shuffle(_cities)
                for city in _cities:
                    if percentage_chance(20, strict=True):
                        self.infectCity(city)
                        iInfections += 1
                        if iInfections >= iMaxNumInfections:
                            break

    def infectCitiesNear(self, iPlayer, startingX, startingY):
        for city in cities().owner(iPlayer).not_building(PlagueType.PLAGUE).entities():
            if calculateDistance(city.getX(), city.getY(), startingX, startingY) <= 3:
                self.infectCity(city)

    def preStopPlague(self, iPlayer, iPlagueCountDown):
        cityList = cities().owner(iPlayer).building(PlagueType.PLAGUE).entities()
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
                if percentage_chance(
                    100 - iTimeModifier - iPopModifier + iHealthModifier - iRemoveModifier,
                    strict=True,
                ):
                    city.setHasRealBuilding(PlagueType.PLAGUE, False)
                    iRemoveModifier += 5  # less chance for each city which already quit

    def stopPlague(self, iPlayer):
        setPlagueCountdown(iPlayer, -PLAGUE_IMMUNITY)
        for city in cities().owner(iPlayer).entities():
            city.setHasRealBuilding(PlagueType.PLAGUE, False)

    def onCityAcquired(self, iOldOwner, iNewOwner, city):
        if city.isHasRealBuilding(PlagueType.PLAGUE):
            # TODO when plague will not kill units anymore, remove this
            # Absinthe: the Plague of Justinian shouldn't spread to Italy and France, even if it was as deadly as the Black Death
            if city.getOwner() in [Civ.FRANCE, Civ.POPE] and turn() <= year(632):
                city.setHasRealBuilding(PlagueType.PLAGUE, False)
                return

            # only if it's not a recently born civ
            if turn() > civilization(iNewOwner).date.birth + PLAGUE_IMMUNITY:
                # reinfect the human player if conquering plagued cities
                if iNewOwner == human():
                    # if > 0 do nothing, if < 0 skip immunity and restart the plague, if == 0 start the plague
                    if getPlagueCountdown(iNewOwner) <= 0:
                        self.spreadPlague(iNewOwner, -1)
                        for cityNear in cities().owner(iNewOwner).entities():
                            if not cityNear.isHasRealBuilding(PlagueType.PLAGUE):
                                if (
                                    calculateDistance(
                                        city.getX(), city.getY(), cityNear.getX(), cityNear.getY()
                                    )
                                    <= 3
                                ):
                                    if percentage_chance(50, strict=True):
                                        self.infectCity(cityNear)
                # no reinfect for the AI, only infect
                else:
                    # if > 0 do nothing, if < 0 keep immunity and remove plague from the city, if == 0 start the plague
                    if getPlagueCountdown(iNewOwner) == 0:
                        self.spreadPlague(iNewOwner, -1)
                        for cityNear in cities().owner(iNewOwner).entities():
                            if not cityNear.isHasRealBuilding(PlagueType.PLAGUE):
                                if (
                                    calculateDistance(
                                        city.getX(), city.getY(), cityNear.getX(), cityNear.getY()
                                    )
                                    <= 3
                                ):
                                    if percentage_chance(50, strict=True):
                                        self.infectCity(cityNear)
                    elif getPlagueCountdown(iNewOwner) < 0:
                        city.setHasRealBuilding(PlagueType.PLAGUE, False)
            else:
                city.setHasRealBuilding(PlagueType.PLAGUE, False)

    def onCityRazed(self, city, iNewOwner):
        pass
