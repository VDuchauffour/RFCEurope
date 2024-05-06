# Rhye's and Fall of Civilization: Europe - Stability

from CvPythonExtensions import *
from CoreData import civilizations, civilization
from CoreFunctions import message, text
from CoreStructures import human, cities

from Consts import MessageData
from CoreTypes import (
    Building,
    Civ,
    Civic,
    Project,
    Scenario,
    Religion,
    FaithPointBonusCategory,
    ProvinceType,
    SpecialParameter,
    UniquePower,
    StabilityCategory,
    Technology,
    Wonder,
)
from PyUtils import percentage_chance, rand

from ProvinceMapData import PROVINCES_MAP
from RFCUtils import collapseImmune, getLastRespawnTurn, getUniqueBuilding, killAndFragmentCiv
import RiseAndFall
import Province
from Scenario import get_scenario

rnf = RiseAndFall.RiseAndFall()
pm = Province.ProvinceManager()

gc = CyGlobalContext()

tStabilityPenalty = (-5, -2, 0, 0, 0)  # province type: unstable, border, potential, historic, core


class Stability:
    def setup(self):  # Sets starting stability
        for iPlayer in civilizations().majors().ids():
            pPlayer = gc.getPlayer(iPlayer)
            for iCath in range(4):
                pPlayer.changeStabilityBase(iCath, -pPlayer.getStabilityBase(iCath))
                pPlayer.setStabilityVary(iCath, 0)
            pPlayer.setStabilitySwing(0)
        # Absinthe: bonus stability for the human player based on difficulty level
        iHandicap = gc.getGame().getHandicapType()
        if iHandicap == 0:
            gc.getPlayer(human()).changeStabilityBase(StabilityCategory.EXPANSION.value, 6)
        elif iHandicap == 1:
            gc.getPlayer(human()).changeStabilityBase(StabilityCategory.EXPANSION.value, 2)

        # Absinthe: Stability is accounted properly for stuff preplaced in the scenario file - from RFCE++
        for iPlayer in civilizations().majors().ids():
            pPlayer = gc.getPlayer(iPlayer)
            teamPlayer = gc.getTeam(pPlayer.getTeam())
            iCounter = 0
            for pCity in cities().owner(iPlayer).entities():
                iCounter += 1
                iOldStab = pPlayer.getStability()

                # Province stability
                iProv = PROVINCES_MAP[pCity.getY()][pCity.getX()]
                iProvinceType = pPlayer.getProvinceType(iProv)
                if iProvinceType == ProvinceType.CORE.value:
                    pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, 1)
                elif not gc.hasUP(
                    iPlayer, UniquePower.STABILITY_BONUS_FOUNDING.value
                ):  # no instability with the Settler UP
                    if iProvinceType == ProvinceType.CONTESTED.value:
                        pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, -1)
                    elif iProvinceType == ProvinceType.NONE.value:
                        pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, -2)

                # Building stability: only a chance for these, as all the permanent negative stability modifiers are missing up to the start
                if pCity.hasBuilding(
                    getUniqueBuilding(iPlayer, Building.MANOR_HOUSE.value)
                ) and percentage_chance(70, strict=True):
                    pPlayer.changeStabilityBase(StabilityCategory.ECONOMY.value, 1)
                if pCity.hasBuilding(
                    getUniqueBuilding(iPlayer, Building.CASTLE.value)
                ) and percentage_chance(70, strict=True):
                    pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, 1)
                if pCity.hasBuilding(
                    getUniqueBuilding(iPlayer, Building.NIGHT_WATCH.value)
                ) and percentage_chance(70, strict=True):
                    pPlayer.changeStabilityBase(StabilityCategory.CIVICS.value, 1)
                if pCity.hasBuilding(
                    getUniqueBuilding(iPlayer, Building.COURTHOUSE.value)
                ) and percentage_chance(70, strict=True):
                    pPlayer.changeStabilityBase(StabilityCategory.CITIES.value, 1)

            # Small boost for small civs
            if iCounter < 6:  # instead of the additional boost for the first few cities
                pPlayer.changeStabilityBase(
                    StabilityCategory.EXPANSION.value, (6 - iCounter) / 2 + 1
                )

            # Known techs which otherwise give instability should also give the penalty here
            for iTech in [
                Technology.FEUDALISM.value,
                Technology.GUILDS.value,
                Technology.GUNPOWDER.value,
                Technology.PROFESSIONAL_ARMY.value,
                Technology.NATIONALISM.value,
                Technology.CIVIL_SERVICE.value,
                Technology.ECONOMICS.value,
                Technology.MACHINERY.value,
                Technology.ARISTOCRACY.value,
            ]:
                if teamPlayer.isHasTech(iTech):
                    gc.getPlayer(iPlayer).changeStabilityBase(StabilityCategory.ECONOMY.value, -1)

            # Absinthe: update all potential provinces at the start for all living players (needed for the scenario)
            if pPlayer.isAlive():
                pm.updatePotential(iPlayer)

        # Absinthe: AI stability bonus - for civs that have a hard time at the beginning
        # 			for example France, Arabia, Bulgaria, Cordoba, Ottomans
        for iPlayer in civilizations().main().ids():
            pPlayer = gc.getPlayer(iPlayer)
            if iPlayer != human():
                pPlayer.changeStabilityBase(
                    StabilityCategory.EXPANSION.value, civilization(iPlayer).ai.stability_bonus
                )

        # Absinthe: update Byzantine stability on the start of the game
        if get_scenario() == Scenario.i500AD:
            # small stability boost for the human player for the first UHV
            if Civ.BYZANTIUM.value == human():
                pByzantium = gc.getPlayer(Civ.BYZANTIUM.value)
                pByzantium.changeStabilityBase(StabilityCategory.EXPANSION.value, 4)
            self.recalcEpansion(Civ.BYZANTIUM.value)

    def checkTurn(self, iGameTurn):
        # Absinthe: logging AI stability levels
        if iGameTurn % 9 == 2:
            for iPlayer in civilizations().main().ids():
                pPlayer = gc.getPlayer(iPlayer)
                if pPlayer.getStability() != 0:
                    print(
                        "AI stability check:",
                        pPlayer.getCivilizationDescription(0),
                        pPlayer.getStability(),
                    )

    def updateBaseStability(
        self, iGameTurn, iPlayer
    ):  # Base stability is temporary (i.e. turn-based) stability
        # 3Miro: this is called for every player

        pPlayer = gc.getPlayer(iPlayer)
        teamPlayer = gc.getTeam(pPlayer.getTeam())

        # Swing stability converges to zero very fast
        iStabilitySwing = pPlayer.getStabilitySwing()
        if iStabilitySwing < -3 or iStabilitySwing > 3:
            pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() / 2)
        elif iStabilitySwing < 0:
            pPlayer.setStabilitySwing(min(0, pPlayer.getStabilitySwing() + 2))
        elif iStabilitySwing > 0:
            pPlayer.setStabilitySwing(max(0, pPlayer.getStabilitySwing() - 2))

        # Absinthe: Anarchy swing stability gets halved every turn
        iStabSwingAnarchy = pPlayer.getStabSwingAnarchy()
        if iStabSwingAnarchy > 1:
            pPlayer.setStabSwingAnarchy(pPlayer.getStabSwingAnarchy() / 2)
        elif iStabSwingAnarchy == 1:
            pPlayer.setStabSwingAnarchy(0)

        # Absinthe: anarchy timer refreshes later in the turn, so it should be reduced by 1 if we want to have it on the correct turns (if nothing else then for the human player)
        # 			but this also means that all 1st turn instability has to be added directly on the revolution / converting - CvPlayer::revolution and CvPlayer::convert
        if pPlayer.getAnarchyTurns() - 1 > 0:
            self.recalcCivicCombos(iPlayer)
            self.recalcEpansion(iPlayer)
            iNumCities = pPlayer.getNumCities()

            if iPlayer != Civ.PRUSSIA.value:  # Absinthe: Prussian UP
                if pPlayer.isHuman():
                    # Absinthe: anarchy base instability
                    pPlayer.changeStabilityBase(
                        StabilityCategory.CIVICS.value, min(0, max(-2, (-iNumCities + 4) / 7))
                    )  # 0 with 1-4 cities, -1 with 5-11 cities, -2 with at least 12 cities

                    # Absinthe: more constant swing instability during anarchy, instead of ever-increasing instability from it
                    iStabSwingAnarchy = pPlayer.getStabSwingAnarchy()
                    if (
                        iStabSwingAnarchy > 0
                    ):  # half of it is already included in the swing, we only add the other half
                        pPlayer.setStabSwingAnarchy(4)
                    else:  # safety net (should be positive, as we add it before the first check)
                        pPlayer.setStabSwingAnarchy(8)
                    pPlayer.setStabilitySwing(
                        pPlayer.getStabilitySwing() - pPlayer.getStabSwingAnarchy()
                    )

                else:
                    # Absinthe: anarchy base instability
                    pPlayer.changeStabilityBase(
                        StabilityCategory.CIVICS.value, min(0, max(-1, (-iNumCities + 6) / 7))
                    )  # Absinthe: reduced for the AI: 0 with 1-6 cities, -1 with at least 7

                    # Absinthe: more constant swing instability during anarchy, instead of ever-increasing instability from it
                    iStabSwingAnarchy = pPlayer.getStabSwingAnarchy()
                    if (
                        iStabSwingAnarchy > 0
                    ):  # half of it is already included in the swing, we only add the other half
                        pPlayer.setStabSwingAnarchy(2)
                    else:  # safety net (should be positive, as we add it before the first check)
                        pPlayer.setStabSwingAnarchy(4)
                    pPlayer.setStabilitySwing(
                        pPlayer.getStabilitySwing() - pPlayer.getStabSwingAnarchy()
                    )

        if (
            pPlayer.getWarPeaceChange() == -1
        ):  # Whenever your nation switches from peace to the state of war (with a major nation)
            gc.getPlayer(iPlayer).changeStabilityBase(
                StabilityCategory.CITIES.value, -1
            )  # 1 permanent stability loss, since your people won't appreciate leaving the state of peace
            pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 3)

        if (iGameTurn + iPlayer) % 3 == 0:  # Economy Check every 3 turns
            self.recalcEconomy(iPlayer)

        self.recalcCity(iPlayer)  # update city stability

        # Absinthe: Collapse dates for AI nations
        if (
            iGameTurn > civilization(iPlayer).date.collapse
            and iPlayer != human()
            and pPlayer.isAlive()
        ):
            # Absinthe: -1 stability every 4 turns up to a total of -15 stability
            if iGameTurn % 4 == 0 and iGameTurn <= civilization(iPlayer).date.collapse + 60:
                pPlayer.changeStabilityBase(StabilityCategory.CITIES.value, -1)

    def refreshBaseStability(
        self, iPlayer
    ):  # Base stability is temporary (i.e. turn-based) stability
        # Absinthe: this is called upon entering the stability/finance screen (F2)

        pPlayer = gc.getPlayer(iPlayer)

        self.recalcCivicCombos(iPlayer)
        self.recalcEpansion(iPlayer)
        self.recalcEconomy(iPlayer)
        self.recalcCity(iPlayer)

    def continentsNormalization(self, iGameTurn):  # Sedna17
        pass

    def onCityBuilt(self, iPlayer, x, y):
        iProv = PROVINCES_MAP[y][x]
        pPlayer = gc.getPlayer(iPlayer)
        # Absinthe: +1 for core, -1 for contested, -2 for foreign provinces
        iProvinceType = pPlayer.getProvinceType(iProv)
        if iProvinceType == ProvinceType.CORE.value:
            pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, 1)
        elif not gc.hasUP(
            iPlayer, UniquePower.STABILITY_BONUS_FOUNDING.value
        ):  # no instability with the Settler UP
            if iProvinceType == ProvinceType.CONTESTED.value:
                pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, -1)
            elif iProvinceType == ProvinceType.NONE.value:
                pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, -2)
        if pPlayer.getNumCities() < 5:  # early boost to small civs
            pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, 1)
        self.recalcEpansion(iPlayer)
        self.recalcCivicCombos(iPlayer)

    def onCityAcquired(self, iOwner, playerType, city, bConquest, bTrade):
        pOwner = gc.getPlayer(iOwner)
        pConq = gc.getPlayer(playerType)

        if city.hasBuilding(Wonder.ESCORIAL.value):
            pConq.setPicklefreeParameter(SpecialParameter.HAS_ESCORIAL.value, 1)
            pOwner.setPicklefreeParameter(SpecialParameter.HAS_ESCORIAL.value, 0)
        if city.hasBuilding(Wonder.STEPHANSDOM.value):
            pConq.setPicklefreeParameter(SpecialParameter.HAS_STEPHANSDOM.value, 1)
            pOwner.setPicklefreeParameter(SpecialParameter.HAS_STEPHANSDOM.value, 0)
        if city.hasBuilding(Wonder.SHRINE_OF_UPPSALA.value):
            pConq.setPicklefreeParameter(SpecialParameter.HAS_UPPSALA_SHRINE.value, 1)
            pOwner.setPicklefreeParameter(SpecialParameter.HAS_UPPSALA_SHRINE.value, 0)
        if city.hasBuilding(Wonder.KOUTOUBIA_MOSQUE.value):
            pConq.setPicklefreeParameter(SpecialParameter.HAS_KOUTOUBIA_MOSQUE.value, 1)
            pOwner.setPicklefreeParameter(SpecialParameter.HAS_KOUTOUBIA_MOSQUE.value, 0)
        if city.hasBuilding(Wonder.MAGNA_CARTA.value):
            pConq.setPicklefreeParameter(SpecialParameter.HAS_MAGNACARTA.value, 1)
            pOwner.setPicklefreeParameter(SpecialParameter.HAS_MAGNACARTA.value, 0)

        self.recalcCivicCombos(playerType)
        self.recalcCivicCombos(iOwner)
        iProv = city.getProvince()
        iProvOwnerType = pOwner.getProvinceType(iProv)
        iProvConqType = pConq.getProvinceType(iProv)

        if iProvOwnerType >= ProvinceType.HISTORICAL.value:
            if iOwner == Civ.SCOTLAND.value:  # Scotland UP part 2
                pOwner.changeStabilityBase(StabilityCategory.EXPANSION.value, -2)
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 2)
            else:
                pOwner.changeStabilityBase(StabilityCategory.EXPANSION.value, -3)
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 4)
        elif iProvOwnerType < ProvinceType.HISTORICAL.value:
            if iOwner == Civ.SCOTLAND.value:  # Scotland UP part 2
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 1)
            else:
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 2)

        if iProvConqType >= ProvinceType.HISTORICAL.value:
            pConq.changeStabilityBase(StabilityCategory.EXPANSION.value, 1)
            pConq.setStabilitySwing(pConq.getStabilitySwing() + 3)

        if pConq.getCivics(5) == Civic.OCCUPATION.value:
            pConq.changeStabilityBase(StabilityCategory.EXPANSION.value, 1)

        if (
            iOwner < civilizations().majors().len()
            and (city.getX(), city.getY()) == civilization(iOwner).location.capital
        ):
            if iOwner == Civ.SCOTLAND.value:  # Scotland UP part 2
                pOwner.changeStabilityBase(StabilityCategory.EXPANSION.value, -5)
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 5)
            elif gc.hasUP(
                iOwner, UniquePower.NO_COLLAPSE_IN_CORE_AND_NORMAL_AREAS.value
            ):  # If Byzantium loses Constantinople, they should lose all non-core cities
                pOwner.changeStabilityBase(StabilityCategory.EXPANSION.value, -20)
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 20)
            else:
                pOwner.changeStabilityBase(StabilityCategory.EXPANSION.value, -10)
                pOwner.setStabilitySwing(pOwner.getStabilitySwing() - 10)
        self.recalcEpansion(iOwner)
        self.recalcEpansion(playerType)

    def onCityRazed(self, iOwner, iPlayer, city):
        # Sedna17: Not sure what difference between iOwner and iPlayer is here
        # 3Miro: iOwner owns the city (victim) and I think iPlayer is the one razing the city
        # 		On second thought, if iOwner (the previous owner) doesn't have enough culture, then iOwner == playerType
        # AbsintheRed: iPlayer is the one razing city, iOwner is the previous owner of the city (right before iPlayer)
        pPlayer = gc.getPlayer(iPlayer)
        pOwner = gc.getPlayer(iOwner)
        if city.hasBuilding(Wonder.ESCORIAL.value):
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_ESCORIAL.value, 0)
            pOwner.setPicklefreeParameter(SpecialParameter.HAS_ESCORIAL.value, 0)
        if city.hasBuilding(Wonder.STEPHANSDOM.value):
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_STEPHANSDOM.value, 0)
            pOwner.setPicklefreeParameter(SpecialParameter.HAS_STEPHANSDOM.value, 0)
        if city.hasBuilding(Wonder.SHRINE_OF_UPPSALA.value):
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_UPPSALA_SHRINE.value, 0)
            pOwner.setPicklefreeParameter(SpecialParameter.HAS_UPPSALA_SHRINE.value, 0)
        if city.hasBuilding(Wonder.KOUTOUBIA_MOSQUE.value):
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_KOUTOUBIA_MOSQUE.value, 0)
            pOwner.setPicklefreeParameter(SpecialParameter.HAS_KOUTOUBIA_MOSQUE.value, 0)
        if city.hasBuilding(Wonder.MAGNA_CARTA.value):
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_MAGNACARTA.value, 0)
            pOwner.setPicklefreeParameter(SpecialParameter.HAS_MAGNACARTA.value, 0)
        self.recalcCivicCombos(iPlayer)
        self.recalcCivicCombos(iOwner)

        # Absinthe: city razing penalty - permanent, based on city population
        # note that the city is already reduced by 1 on city conquest, so city.getPopulation() is one less than the original size
        # so currently: 0 with 1-2 population, -1 with 3-5 population, -2 with 6-9 population, -3 with 10+ population
        iRazeStab = 0
        if city.getPopulation() >= 9:
            iRazeStab = 3
        elif city.getPopulation() >= 5:
            iRazeStab = 2
        elif city.getPopulation() >= 2:
            iRazeStab = 1
        # Absinthe: Norwegian UP - one less stability penalty
        if iPlayer == Civ.NORWAY.value:
            iRazeStab -= 1
        if iRazeStab > 0:
            pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, -iRazeStab)
        # temporary, 3 for everyone but Norway
        if iPlayer != Civ.NORWAY.value:
            pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 3)
        self.recalcEpansion(iPlayer)

    def onImprovementDestroyed(self, owner):
        pPlayer = gc.getPlayer(owner)
        pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 2)

    def onTechAcquired(self, iTech, iPlayer):
        if iTech in [
            Technology.FEUDALISM.value,
            Technology.GUILDS.value,
            Technology.GUNPOWDER.value,
            Technology.PROFESSIONAL_ARMY.value,
            Technology.NATIONALISM.value,
            Technology.CIVIL_SERVICE.value,
            Technology.ECONOMICS.value,
            Technology.MACHINERY.value,
            Technology.ARISTOCRACY.value,
        ]:
            gc.getPlayer(iPlayer).changeStabilityBase(StabilityCategory.ECONOMY.value, -1)
        pass

    def onBuildingBuilt(self, iPlayer, iBuilding):
        pPlayer = gc.getPlayer(iPlayer)
        if iBuilding == getUniqueBuilding(iPlayer, Building.MANOR_HOUSE.value):
            pPlayer.changeStabilityBase(StabilityCategory.ECONOMY.value, 1)
            self.recalcEconomy(iPlayer)
        elif iBuilding == getUniqueBuilding(iPlayer, Building.CASTLE.value):
            pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, 1)
            self.recalcEpansion(iPlayer)
        elif iBuilding == getUniqueBuilding(iPlayer, Building.NIGHT_WATCH.value):
            pPlayer.changeStabilityBase(StabilityCategory.CIVICS.value, 1)
            self.recalcCivicCombos(iPlayer)
        elif iBuilding == getUniqueBuilding(iPlayer, Building.COURTHOUSE.value):
            pPlayer.changeStabilityBase(StabilityCategory.CITIES.value, 1)
            self.recalcCity(iPlayer)
        elif iBuilding == Wonder.ESCORIAL.value:
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_ESCORIAL.value, 1)
        elif iBuilding == Wonder.STEPHANSDOM.value:
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_STEPHANSDOM.value, 1)
        elif iBuilding == Wonder.SHRINE_OF_UPPSALA.value:
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_UPPSALA_SHRINE.value, 1)
        elif iBuilding == Wonder.KOUTOUBIA_MOSQUE.value:
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_KOUTOUBIA_MOSQUE.value, 1)
        elif iBuilding == Wonder.MAGNA_CARTA.value:
            pPlayer.setPicklefreeParameter(SpecialParameter.HAS_MAGNACARTA.value, 1)
        elif iBuilding == Building.PALACE.value:
            pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, -2)
            pPlayer.setStabilitySwing(pPlayer.getStabilitySwing() - 5)
            self.recalcEpansion(iPlayer)
        elif iBuilding == Building.RELIQUARY.value:
            pPlayer.changeStabilityBase(StabilityCategory.EXPANSION.value, 1)
            self.recalcEpansion(iPlayer)

    def onProjectBuilt(self, iPlayer, iProject):
        pPlayer = gc.getPlayer(iPlayer)
        iCivic5 = pPlayer.getCivics(5)
        if iProject >= len(Project):
            pPlayer.changeStabilityBase(
                StabilityCategory.EXPANSION.value, -2
            )  # -2 stability for each colony
            if iCivic5 == Civic.COLONIALISM.value:
                pPlayer.changeStabilityBase(
                    StabilityCategory.EXPANSION.value, 1
                )  # one less stability penalty if civ is in Colonialism
        self.recalcEpansion(iPlayer)

    def onCombatResult(self, argsList):
        pass

    def onReligionFounded(self, iPlayer):
        pass

    def onReligionSpread(self, iReligion, iPlayer):
        pass

    def checkImplosion(self, iGameTurn):
        if iGameTurn > 14 and iGameTurn % 6 == 3:
            for iPlayer in civilizations().main().ids():
                pPlayer = gc.getPlayer(iPlayer)
                # Absinthe: no city secession for 15 turns after spawn, for 10 turns after respawn
                iRespawnTurn = getLastRespawnTurn(iPlayer)
                if (
                    pPlayer.isAlive()
                    and iGameTurn >= civilization(iPlayer).date.birth + 15
                    and iGameTurn >= iRespawnTurn + 10
                ):
                    iStability = pPlayer.getStability()
                    # Absinthe: human player with very bad stability should have a much bigger chance for collapse
                    if iStability < -14 and iPlayer == human():
                        if percentage_chance(-2 * iStability, strict=True):
                            # 30 chance with -15, 50% with -25, 70% with -35, 100% with -50 or less
                            if not collapseImmune(iPlayer):
                                self.collapseCivilWar(iPlayer, iStability)
                        else:  # when won't collapse, secession should always happen
                            rnf.revoltCity(iPlayer, False)
                    # Absinthe: if stability is less than -3, there is a chance that the secession/revolt or collapse mechanics start
                    # 			if more than 8 cities: high chance for secession mechanics, low chance for collapse
                    # 			elif more than 4 cities: medium chance for collapse mechanics, medium chance for secession
                    # 			otherwise big chance for collapse mechanics
                    # 			the actual chance for both secession/revolt and total collapse is increasing with lower stability
                    elif iStability < -3:
                        iRand1 = rand(10)
                        iRand2 = rand(10)
                        iRand3 = rand(10)
                        if pPlayer.getNumCities() > 8:
                            if iRand1 < 8:  # 80 chance for secession start
                                if iRand2 < (
                                    -3 - iStability
                                ):  # 10% at -4, increasing by 10% with each point (100% with -13 or less)
                                    rnf.revoltCity(iPlayer, False)
                            elif (
                                iRand3 < 1
                                and iGameTurn >= civilization(iPlayer).date.birth + 20
                                and not collapseImmune(iPlayer)
                            ):  # 10 chance for collapse start
                                if iRand2 < (
                                    -1.5 - (iStability / 2)
                                ):  # 10% at -4, increasing by 10% with 2 points (100% with -22 or less)
                                    self.collapseCivilWar(iPlayer, iStability)
                        elif pPlayer.getNumCities() > 4:
                            if iRand1 < 4:  # 40 chance for secession start
                                if iRand2 < (
                                    -3 - iStability
                                ):  # 10% at -4, increasing by 10% with each point (100% with -13 or less)
                                    rnf.revoltCity(iPlayer, False)
                            elif (
                                iRand3 < 4
                                and iGameTurn >= civilization(iPlayer).date.birth + 20
                                and not collapseImmune(iPlayer)
                            ):  # 40 chance for collapse start
                                if iRand2 < (
                                    -1.5 - (iStability / 2)
                                ):  # 10% at -4, increasing by 10% with 2 points (100% with -22 or less)
                                    self.collapseCivilWar(iPlayer, iStability)
                        elif (
                            iRand1 < 7
                            and iGameTurn >= civilization(iPlayer).date.birth + 20
                            and not collapseImmune(iPlayer)
                        ):  # 70 chance for collapse start
                            if iRand2 < (
                                -1.5 - (iStability / 2)
                            ):  # 10% at -4, increasing by 10% with 2 points (100% with -22 or less)
                                self.collapseCivilWar(iPlayer, iStability)

    def collapseCivilWar(self, iPlayer, iStability):
        pPlayer = gc.getPlayer(iPlayer)
        iHuman = human()
        if iPlayer != iHuman:
            if gc.getPlayer(iHuman).canContact(iPlayer):
                message(
                    iHuman,
                    pPlayer.getCivilizationDescription(0)
                    + " "
                    + text("TXT_KEY_STABILITY_CIVILWAR_STABILITY"),
                    color=MessageData.RED,
                )
            killAndFragmentCiv(iPlayer, False, False)
        elif pPlayer.getNumCities() > 1:
            message(
                iPlayer,
                text("TXT_KEY_STABILITY_CIVILWAR_STABILITY_HUMAN"),
                force=True,
                color=MessageData.RED,
            )
            killAndFragmentCiv(iPlayer, False, True)
            self.zeroStability(iPlayer)

    def printStability(self, iGameTurn, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        print(" Turn: ", iGameTurn)
        print(" ---------------- New Stability For " + pPlayer.getCivilizationShortDescription())
        print("                  Stability : ", pPlayer.getStability())
        print(
            "                  Cities    : ",
            pPlayer.getStabilityBase(StabilityCategory.CITIES.value)
            + pPlayer.getStabilityVary(StabilityCategory.CITIES.value),
        )
        print(
            "                  Civics    : ",
            pPlayer.getStabilityBase(StabilityCategory.CIVICS.value)
            + pPlayer.getStabilityVary(StabilityCategory.CIVICS.value),
        )
        print(
            "                  Economy   : ",
            pPlayer.getStabilityBase(StabilityCategory.ECONOMY.value)
            + pPlayer.getStabilityVary(StabilityCategory.ECONOMY.value),
        )
        print(
            "                  Expansion : ",
            pPlayer.getStabilityBase(StabilityCategory.EXPANSION.value)
            + pPlayer.getStabilityVary(StabilityCategory.EXPANSION.value),
        )

    def zeroStability(self, iPlayer):  # Called by Stability.CheckImplosion
        pPlayer = gc.getPlayer(iPlayer)
        pPlayer.changeStabilityBase(
            StabilityCategory.CITIES.value,
            -pPlayer.getStabilityBase(StabilityCategory.CITIES.value),
        )
        pPlayer.changeStabilityBase(
            StabilityCategory.CIVICS.value,
            -pPlayer.getStabilityBase(StabilityCategory.CIVICS.value),
        )
        pPlayer.changeStabilityBase(
            StabilityCategory.ECONOMY.value,
            -pPlayer.getStabilityBase(StabilityCategory.ECONOMY.value),
        )
        pPlayer.changeStabilityBase(
            StabilityCategory.EXPANSION.value,
            -pPlayer.getStabilityBase(StabilityCategory.EXPANSION.value),
        )
        pPlayer.setStabilityVary(StabilityCategory.CITIES.value, 0)
        pPlayer.setStabilityVary(StabilityCategory.CIVICS.value, 0)
        pPlayer.setStabilityVary(StabilityCategory.ECONOMY.value, 0)
        pPlayer.setStabilityVary(StabilityCategory.EXPANSION.value, 0)
        pPlayer.setStabilitySwing(0)

    def recalcCity(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        iCivic4 = pPlayer.getCivics(4)
        iCivic5 = pPlayer.getCivics(5)
        iTotalHappy = (
            pPlayer.calculateTotalCityHappiness() - pPlayer.calculateTotalCityUnhappiness()
        )
        iCityStability = 0
        if pPlayer.getNumCities() == 0:
            iHappyStability = 0
        else:
            iHappyStability = (
                iTotalHappy / pPlayer.getNumCities()
            )  # +k stability for an average city happiness of at least k
        iCivHealthStability = 0
        iHealthStability = 0
        iHurryStability = 0
        iMilitaryStability = 0
        iWarWStability = 0
        iReligionStability = 0
        iCivicReligionInstability = 0
        iCultureStability = 0

        for pCity in cities().owner(iPlayer).entities():
            # Absinthe: if your civ is healthy, bonus stability
            # 			if one of your is cities is unhealthy, -1 stability
            iCivHealthStability += pCity.goodHealth()
            iCivHealthStability -= pCity.badHealth(False)
            if pCity.goodHealth() - pCity.badHealth(False) < 0:
                iHealthStability -= 1
            if pCity.angryPopulation(0) > 0:
                iHappyStability -= 2

            # Absinthe: This is the "We desire religious freedom!" unhappiness, from civics - currently from the Religious Law civic
            # 			also it is a negative counter with the current civic setup, so getReligionBadHappiness() == -1 with one non-state religion in the city
            if pCity.getReligionBadHappiness() < 0:
                if not gc.hasUP(
                    iPlayer, UniquePower.NO_INSTABILITY_WITH_FOREIGN_RELIGION.value
                ):  # Polish UP
                    iCivicReligionInstability += 1
            if pCity.getHurryAngerModifier() > 0:
                iHurryStability -= 1
            if pCity.getNoMilitaryPercentAnger() > 0:
                iMilitaryStability -= 1
            # Absinthe: getWarWearinessPercentAnger is not a local variable for your cities, but a global one for your entire civ
            # 			it would results in 1 instability for each city if there is an ongoing war, thus I added some modifications below
            if pCity.getWarWearinessPercentAnger() > 10:
                iWarWStability -= 1

            bJewInstability = False
            if (
                iCivic4 != Civic.FREE_RELIGION.value
            ):  # Religious Tolerance negates stability penalties from non-state religions
                if not gc.hasUP(
                    iPlayer, UniquePower.NO_INSTABILITY_WITH_FOREIGN_RELIGION.value
                ):  # Polish UP
                    if pCity.getNumForeignReligions() > 0:
                        # only calculate if Judaism is not the State Religion
                        if pPlayer.getStateReligion() != Religion.JUDAISM.value:
                            bJewInstability = True
                        if iCivic4 == Civic.PAGANISM.value:  # Pagans are a bit more tolerant
                            iReligionStability -= 1
                        elif (
                            iPlayer == Civ.OTTOMAN.value
                        ):  # Janissary UP - not necessarily a historical aspect of it, but important for gameplay
                            # elif ( gc.hasUP( iPlayer, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS.value )):
                            iReligionStability -= 1
                        else:
                            iReligionStability -= 2
                    if (
                        pCity.getNumForeignReligions() > 1
                    ):  # additional -1 stability for every further foreign religion
                        iReligionStability -= min(pCity.getNumForeignReligions() - 1, 3)

            # Absinthe: Jewish Quarter reduces religion instability if Judaism is present in the city
            if (
                bJewInstability
                and pCity.hasBuilding(Building.JEWISH_QUARTER.value)
                and pCity.isHasReligion(Religion.JUDAISM.value)
            ):  # only if there are some religious penalties present in the city
                iReligionStability += 1

            # Absinthe: -1 stability if own culture is less than 40% of total culture in a city, -2 stability if less than 20%
            iTotalCulture = pCity.countTotalCultureTimes100()
            if (
                (iTotalCulture > 0)
                and ((pCity.getCulture(iPlayer) * 10000) / iTotalCulture < 40)
                and not gc.hasUP(iPlayer, UniquePower.NO_UNHAPPINESS_WITH_FOREIGN_CULTURE.value)
            ):
                # Absinthe: 1 less instability with the Vassalage Civic, so only -1 with less than 20%, 0 otherwise
                if iCivic5 != Civic.SUBJUGATION.value:
                    iCultureStability -= 1
                if (pCity.getCulture(iPlayer) * 10000) / iTotalCulture < 20:
                    iCultureStability -= 1

        # Absinthe: if your civ is healthy, bonus stability
        if iCivHealthStability > 0:
            iCivHealthStability = (
                iCivHealthStability / pPlayer.getNumCities()
            )  # +k stability for an average city health of at least k
            iHealthStability += iCivHealthStability

        # Absinthe: reduced value for getReligionBadHappiness, shouldn't add -1 for each city if almost all of them has multiple religions
        # 			switching in and out of the civic won't result in that much fluctuation
        iCivicReligionInstability = min(pPlayer.getNumCities() / 2, iCivicReligionInstability)

        # Absinthe: persecution counter - cooldown is handled in Religions.checkTurn
        # 			1-3 means 1 instability, 4-6 means 2 instability, 7-9 means 3 instability, etc...
        iProsecutionCount = pPlayer.getProsecutionCount()
        if iProsecutionCount > 0:
            iReligionStability -= (iProsecutionCount + 2) / 3

        # Humans are far more competent then the AI, so the AI won't get all the penalties
        if pPlayer.isHuman():
            iCityStability += (
                iHappyStability
                + iHealthStability
                + iReligionStability
                - iCivicReligionInstability
                + iHurryStability
                + iCultureStability
                + iMilitaryStability
            )
            iCityStability += max(
                iWarWStability / 3 - 1, -10
            )  # max 10 instability from war weariness
            iCityStability = min(
                iCityStability, 8
            )  # max 8 extra stability from cities - don't want to add too many bonuses for runaway civs
        else:
            iCityStability += max(iHappyStability, -5) + max(
                iHealthStability, -5
            )  # AI keeps very unhappy cities
            iCityStability += max(
                iReligionStability - iCivicReligionInstability + iHurryStability, -7
            ) + max(iCultureStability, -5)
            iCityStability += max(
                iMilitaryStability + iWarWStability / 3, -3
            )  # AI is also bad at handling war weariness
            iCityStability = min(max(iCityStability, -10), 8)
        iCityStability += pPlayer.getFaithBenefit(FaithPointBonusCategory.BOOST_STABILITY.value)
        if pPlayer.getGoldenAgeTurns() > 0:
            iCityStability += 8
        # Absinthe: Westminster Abbey faith-stability effect
        if pPlayer.countNumBuildings(Wonder.WESTMINSTER.value) > 0:
            # would be better, if the stability bonus was also only applied for Divine Monarchy?
            # if pPlayer.getCivics(0) == Civic.DIVINE_MONARCHY.value:
            iFaith = pPlayer.getFaith()
            iCityStability += iFaith / 20

        pPlayer.setStabilityVary(StabilityCategory.CITIES.value, iCityStability)

    def recalcCivicCombos(self, iPlayer):
        # Note: this is more or less the only place where Civics are referenced, yet referring them by number makes this hard to read
        pPlayer = gc.getPlayer(iPlayer)
        iCivicGovernment = pPlayer.getCivics(0)
        iCivicLegal = pPlayer.getCivics(1)
        iCivicLabor = pPlayer.getCivics(2)
        iCivicEconomy = pPlayer.getCivics(3)
        iCivicReligion = pPlayer.getCivics(4)
        iCivicExpansion = pPlayer.getCivics(5)

        lCivics = [
            iCivicGovernment,
            iCivicLegal,
            iCivicLabor,
            iCivicEconomy,
            iCivicReligion,
            iCivicExpansion,
        ]
        lCombinations = [
            (iCivic1, iCivic2) for iCivic1 in lCivics for iCivic2 in lCivics if iCivic1 < iCivic2
        ]

        iCivicCombo = 0
        # Calculate the combinations
        for lCombination in lCombinations:
            iComboValue = self.getCivicCombinationStability(lCombination[0], lCombination[1])
            if (
                iComboValue < 0
                and pPlayer.getPicklefreeParameter(SpecialParameter.HAS_MAGNACARTA.value) == 1
            ):
                iComboValue = 0
            iCivicCombo += iComboValue

        if pPlayer.getPicklefreeParameter(SpecialParameter.HAS_STEPHANSDOM.value) == 1:
            if iCivicGovernment in [
                Civic.FEUDAL_MONARCHY.value,
                Civic.DIVINE_MONARCHY.value,
                Civic.LIMITE_DMONARCHY.value,
            ]:
                iCivicCombo += 2

        if pPlayer.getPicklefreeParameter(SpecialParameter.HAS_UPPSALA_SHRINE.value) == 1:
            if iCivicReligion == Civic.PAGANISM.value:
                iCivicCombo += 3

        if pPlayer.getPicklefreeParameter(SpecialParameter.HAS_KOUTOUBIA_MOSQUE.value) == 1:
            if iCivicLegal == Civic.RELIGIOUS_LAW.value:
                iCivicCombo += 4

        if iCivicLegal == Civic.BUREAUCRACY.value:  # Bureaucracy city cap
            if (
                iPlayer == Civ.NOVGOROD.value and pPlayer.getNumCities() > 6
            ):  # the penalties are halved for Novgorod
                iBureaucracyCap = (6 - pPlayer.getNumCities()) / 2
            else:
                iBureaucracyCap = 6 - pPlayer.getNumCities()
            if not pPlayer.isHuman():  # max -5 penalty for the AI
                iBureaucracyCap = max(-5, iBureaucracyCap)
            iCivicCombo += iBureaucracyCap

        if iCivicGovernment == Civic.MERCHANT_REPUBLIC.value:  # Merchant Republic city cap
            if (
                iPlayer == Civ.VENECIA.value and pPlayer.getNumCities() > 5
            ):  # the penalties are halved for Venice
                iMerchantRepublicCap = (5 - pPlayer.getNumCities()) / 2
            else:
                iMerchantRepublicCap = 5 - pPlayer.getNumCities()
            if not pPlayer.isHuman():  # max -5 penalty for the AI
                iMerchantRepublicCap = max(-5, iMerchantRepublicCap)
            iCivicCombo += iMerchantRepublicCap

        pPlayer.setStabilityVary(StabilityCategory.CIVICS.value, iCivicCombo)

    def getCivicCombinationStability(self, iCivic0, iCivic1):
        lCivics = set([iCivic0, iCivic1])

        if Civic.FEUDAL_MONARCHY.value in lCivics:
            if Civic.FEUDAL_LAW.value in lCivics:
                return 3

        if (
            Civic.DIVINE_MONARCHY.value in lCivics
        ):  # Divine Monarchy should have an appropriate religious civic
            if Civic.RELIGIOUS_LAW.value in lCivics:
                return 2
            if Civic.PAGANISM.value in lCivics:
                return -4
            if Civic.STATE_RELIGION.value in lCivics:
                return 2
            if Civic.THEOCRACY.value in lCivics:
                return 3
            if Civic.ORGANIZED_RELIGION.value in lCivics:
                return 4
            if Civic.FREE_RELIGION.value in lCivics:
                return -3

        if (
            Civic.LIMITE_DMONARCHY.value in lCivics
        ):  # Constitutional Monarchy and Republic both like enlightened civics
            if Civic.COMMON_LAW.value in lCivics:
                return 3
            if Civic.FREE_PEASANTRY.value in lCivics:
                return 2
            if Civic.FREE_LABOR.value in lCivics:
                return 2

        if (
            Civic.MERCHANT_REPUBLIC.value in lCivics
        ):  # Constitutional Monarchy and Republic both like enlightened civics
            if Civic.FEUDAL_LAW.value in lCivics:
                return -3
            if Civic.COMMON_LAW.value in lCivics:
                return 3
            if Civic.FREE_PEASANTRY.value in lCivics:
                return 2
            if Civic.FREE_LABOR.value in lCivics:
                return 2
            if Civic.TRADE_ECONOMY.value in lCivics:
                return 4
            if Civic.MERCANTILISM.value in lCivics:
                return -4
            if Civic.IMPERIALISM.value in lCivics:
                return -2

        if Civic.FEUDAL_LAW.value in lCivics:
            if Civic.SERFDOM.value in lCivics:
                return 3
            if Civic.FREE_PEASANTRY.value in lCivics:
                return -4
            if Civic.MANORIALISM.value in lCivics:
                return 2
            if Civic.VASSALAGE.value in lCivics:
                return 2

        if Civic.RELIGIOUS_LAW.value in lCivics:
            if Civic.PAGANISM.value in lCivics:
                return -5
            if Civic.THEOCRACY.value in lCivics:
                return 5
            if Civic.FREE_RELIGION.value in lCivics:
                return -3

        if Civic.COMMON_LAW.value in lCivics:
            if Civic.SERFDOM.value in lCivics:
                return -3
            if Civic.FREE_LABOR.value in lCivics:
                return 3
            if Civic.THEOCRACY.value in lCivics:
                return -4

        if Civic.SERFDOM.value in lCivics:
            if Civic.MANORIALISM.value in lCivics:
                return 2
            if Civic.TRADE_ECONOMY.value in lCivics:
                return -3

        if Civic.APPRENTICESHIP.value in lCivics:
            if Civic.GUILDS.value in lCivics:
                return 3

        return 0

    def recalcEconomy(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        iPopNum = pPlayer.getTotalPopulation()
        iImports = pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE)
        iExports = pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
        # Absinthe: removed - why was Cordoba penalized in the first place?
        # if iPlayer == Civ.CORDOBA.value:
        # 	iImports /= 2
        # 	iExports /= 2

        iFinances = pPlayer.getFinancialPower()
        iInflation = pPlayer.calculateInflatedCosts()
        iProduction = pPlayer.calculateTotalYield(YieldTypes.YIELD_PRODUCTION)
        # Absinthe: removed - Venice no longer has that weak production
        # if iPlayer == Civ.VENECIA.value:
        # 	iProduction += iPopNum # offset their weak production
        iAgriculture = pPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD)

        iLargeCities = 0
        for pCity in cities().owner(iPlayer).entities():
            # Absinthe: production penalty removed - was a mistake to add a city-based modifier to the financial stability which is based on average per population
            # if pCity.isProductionUnit():
            # 	iUnit = pCity.getProductionUnit()
            # 	if iUnit < Unit.WORKER.value or iUnit > Unit.ISLAMIC_MISSIONARY.value:
            # 		iProductionPenalty -= 1
            # elif pCity.isProductionBuilding():
            # 	iBuilding = pCity.getProductionBuilding()
            # 	if isWonder(iBuilding):
            # 		iProductionPenalty -= 2
            # else:
            # 	iProductionPenalty -= 2
            iCityPop = pCity.getPopulation()
            if (
                iCityPop > 10
            ):  # large cities should have production bonus buildings, drop by 10 percent
                iProduction -= pCity.getYieldRate(YieldTypes.YIELD_PRODUCTION) / 10
                iLargeCities += 1

        iNumCities = pPlayer.getNumCities()
        if iNumCities > 0:
            iIndustrialStability = min(
                max(2 * (2 * iAgriculture + iProduction) / iPopNum - 14, -3), 3
            )  # this is 0 if the average yield per population is a little more than 2 food and 2 production (with bonuses)
            if (
                pPlayer.getPicklefreeParameter(SpecialParameter.HAS_ESCORIAL.value) == 1
            ):  # El Escorial no economic instability effect
                iIndustrialStability = max(iIndustrialStability, 0)
            iFinances = (
                iFinances * (100 - 20 * iLargeCities / iNumCities) / 100
            )  # between 80% and 100%, based on the number of large cities
            iFinancialStability = min(
                max((iFinances - iInflation + iImports + iExports) / iPopNum - 6, -4), 4
            )  # this is 0 if the average financial power per population is around 6
            # iFinancialPowerPerCity = ( iFinances - iInflation + iImports + iExports ) / iNumCities
            if (
                pPlayer.getPicklefreeParameter(SpecialParameter.HAS_ESCORIAL.value) == 1
            ):  # El Escorial no economic instability effect
                iFinancialStability = max(iFinancialStability, 0)
            pPlayer.setStabilityVary(
                StabilityCategory.ECONOMY.value, iFinancialStability + iIndustrialStability
            )
        else:
            pPlayer.setStabilityVary(StabilityCategory.ECONOMY.value, 0)

    def recalcEpansion(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        iExpStability = 0
        iCivic5 = pPlayer.getCivics(5)
        bIsUPLandStability = gc.hasUP(
            iPlayer, UniquePower.LESS_INSTABILITY_WITH_FOREIGN_LAND.value
        )
        iCivicBonus = 0
        iUPBonus = 0
        for pCity in cities().owner(iPlayer).entities():
            iProvType = pPlayer.getProvinceType(pCity.getProvince())
            iProvNum = pCity.getProvince()
            CityName = pCity.getNameKey()
            assert 0 <= iProvType < len(tStabilityPenalty), (
                "Bad ProvinceType value for CityName (%s)" % CityName
            )

            iExpStability += tStabilityPenalty[iProvType]
            if iProvType <= ProvinceType.CONTESTED.value:
                if iCivic5 == Civic.IMPERIALISM.value:  # Imperialism
                    iCivicBonus += 1
                if bIsUPLandStability:  # French UP
                    iUPBonus += 1
        iExpStability += iCivicBonus  # Imperialism
        iExpStability += iUPBonus  # French UP
        if pPlayer.getCivics(5) != Civic.OCCUPATION.value:
            iExpStability -= 3 * pPlayer.getForeignCitiesInMyProvinceType(
                ProvinceType.CORE.value
            )  # -3 stability for each foreign/enemy city in your core provinces, without the Militarism civic
            iExpStability -= 1 * pPlayer.getForeignCitiesInMyProvinceType(
                ProvinceType.HISTORICAL.value
            )  # -1 stability for each foreign/enemy city in your natural provinces, without the Militarism civic
        if pPlayer.getMaster() > -1:
            iExpStability += 8
        if iCivic5 == Civic.VASSALAGE.value:
            iExpStability += 3 * pPlayer.countVassals()
        else:
            iExpStability += pPlayer.countVassals()
        iNumCities = pPlayer.getNumCities()
        if iPlayer in [Civ.OTTOMAN.value, Civ.MOSCOW.value]:  # five free cities for those two
            iNumCities = max(0, iNumCities - 5)
        iExpStability -= iNumCities * iNumCities / 40
        pPlayer.setStabilityVary(StabilityCategory.EXPANSION.value, iExpStability)
