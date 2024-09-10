from CvPythonExtensions import CyGlobalContext, WarPlanTypes

from Consts import MessageData
from Core import civilization, civilizations, cities, message, text
from CoreTypes import ProvinceType, StabilityCategory, UniquePower
from PyUtils import chance, rand, choice
from RFCUtils import (
    calculateDistance,
    collapseImmune,
    cultureManager,
    flipCity,
    flipUnitsInCityAfter,
    flipUnitsInCitySecession,
    setTempFlippingCity,
)
from StoredData import data

gc = CyGlobalContext()


def secession(iGameTurn):
    # Absinthe: if stability is negative there is a chance for a random city to declare it's independence, checked every 3 turns
    iRndnum = rand(civilizations().majors().len())
    iSecessionNumber = 0
    for j in civilizations().majors().ids():
        iPlayer = (j + iRndnum) % civilizations().majors().len()
        pPlayer = gc.getPlayer(iPlayer)
        # Absinthe: no city secession for 15 turns after spawn, for 10 turns after respawn
        if (
            pPlayer.isAlive()
            and iGameTurn >= civilization(iPlayer).date.birth + 15
            and iGameTurn >= data.players[iPlayer].last_respawn_turn + 10
        ):
            if chance(10, -2 - pPlayer.getStability(), strict=True):
                # 10% at -3, increasing by 10% with each point (100% with -12 or less)
                revoltCity(iPlayer, False)
                iSecessionNumber += 1
                if iSecessionNumber > 2:
                    return  # max 3 secession per turn
                continue  # max 1 secession for each civ


def secessionCloseCollapse(iGameTurn):
    # Absinthe: another instance of secession, now with possibility for multiple cities revolting for the same civ
    # Absinthe: this can only happen with very bad stability, in case of fairly big empires
    iRndnum = rand(civilizations().majors().len())
    for j in civilizations().majors().ids():
        iPlayer = (j + iRndnum) % civilizations().majors().len()
        pPlayer = gc.getPlayer(iPlayer)
        if (
            pPlayer.isAlive()
            and iGameTurn >= civilization(iPlayer).date.birth + 20
            and iGameTurn >= data.players[iPlayer].last_respawn_turn + 10
        ):
            iStability = pPlayer.getStability()
            if (
                iStability < -15 and pPlayer.getNumCities() > 10
            ):  # so the civ is close to a civil war
                revoltCity(iPlayer, False)
                revoltCity(iPlayer, False)
                revoltCity(iPlayer, True)
                revoltCity(iPlayer, True)
                return  # max for 1 civ at a turn


def revoltCity(iPlayer, bForce):
    pPlayer = gc.getPlayer(iPlayer)
    iStability = pPlayer.getStability()

    cityListInCore = []
    cityListInNotCore = []
    for city in cities.owner(iPlayer).entities():
        tCity = (city.getX(), city.getY())
        x, y = tCity
        pCurrent = gc.getMap().plot(city.getX(), city.getY())

        # Absinthe: cities with We Love The King Day, your current and original capitals, and cities very close to your current capital won't revolt
        if (
            not city.isWeLoveTheKingDay()
            and not city.isCapital()
            and tCity != civilization(iPlayer).location.capital
        ):
            if pPlayer.getNumCities() > 0:  # this check is needed, otherwise game crashes
                capital = gc.getPlayer(iPlayer).getCapitalCity()
                iDistance = calculateDistance(x, y, capital.getX(), capital.getY())
                if iDistance > 3:
                    # Absinthe: Byzantine UP: cities in normal and core provinces won't go to the list
                    bCollapseImmune = collapseImmune(iPlayer)
                    iProvType = pPlayer.getProvinceType(city.getProvince())
                    # Absinthe: if forced revolt, all cities go into the list by default (apart from the Byzantine UP and the special ones above)
                    if bForce:
                        if iProvType >= ProvinceType.POTENTIAL:
                            if not bCollapseImmune:
                                cityListInCore.append(city)
                        else:
                            cityListInNotCore.append(city)
                    # Absinthe: angry population, bad health, untolerated religion, no military garrison can add the city to the list a couple more times (per type)
                    # 			if the city is in a contested province, the city is added a couple more times by default, if in a foreign province, a lot more times
                    # Absinthe: bigger chance to choose the city if unhappy
                    if city.angryPopulation(0) > 0:
                        if iProvType >= ProvinceType.POTENTIAL:
                            if not bCollapseImmune:
                                for i in range(2):
                                    cityListInCore.append(city)
                        else:
                            for i in range(4):
                                cityListInNotCore.append(city)
                    # Absinthe: health issues do not cause city secession in core provinces for anyone
                    # 			also less chance from unhealth for cities in contested and foreign provinces
                    if city.goodHealth() - city.badHealth(False) < -1:
                        if iProvType < ProvinceType.POTENTIAL:
                            cityListInNotCore.append(city)
                    # Absinthe: also not a cause for secession in core provinces, no need to punish the player this much (and especially the AI) for using the civic
                    if city.getReligionBadHappiness() < 0:
                        if iProvType < ProvinceType.POTENTIAL:
                            for i in range(2):
                                cityListInNotCore.append(city)
                    # Absinthe: no defensive units in the city increase chance
                    if city.getNoMilitaryPercentAnger() > 0:
                        if iProvType >= ProvinceType.POTENTIAL:
                            if not bCollapseImmune:
                                cityListInCore.append(city)
                        else:
                            for i in range(2):
                                cityListInNotCore.append(city)
                    # Absinthe: also add core cities if they have less than 40% own culture (and the civ doesn't have the Cultural Tolerance UP)
                    if iProvType >= ProvinceType.POTENTIAL:
                        if not bCollapseImmune and not gc.hasUP(
                            iPlayer, UniquePower.NO_UNHAPPINESS_WITH_FOREIGN_CULTURE
                        ):
                            if (
                                city.countTotalCultureTimes100() > 0
                                and (
                                    city.getCulture(iPlayer)
                                    * 10000
                                    / city.countTotalCultureTimes100()
                                )
                                < 40
                            ):
                                cityListInCore.append(city)
                            elif (
                                city.countTotalCultureTimes100() > 0
                                and (
                                    city.getCulture(iPlayer)
                                    * 10000
                                    / city.countTotalCultureTimes100()
                                )
                                < 20
                            ):
                                for i in range(2):
                                    cityListInCore.append(city)
                    # Absinthe: cities in outer and unstable provinces have chance by default, the number of times they are added is modified by the civ's own culture in the city
                    elif iProvType == ProvinceType.CONTESTED:
                        if (
                            city.countTotalCultureTimes100() > 0
                            and (
                                city.getCulture(iPlayer) * 10000 / city.countTotalCultureTimes100()
                            )
                            > 80
                        ):
                            cityListInNotCore.append(city)
                        elif (
                            city.countTotalCultureTimes100() > 0
                            and (
                                city.getCulture(iPlayer) * 10000 / city.countTotalCultureTimes100()
                            )
                            > 60
                        ):
                            for i in range(2):
                                cityListInNotCore.append(city)
                        elif (
                            city.countTotalCultureTimes100() > 0
                            and (
                                city.getCulture(iPlayer) * 10000 / city.countTotalCultureTimes100()
                            )
                            > 40
                        ):
                            for i in range(3):
                                cityListInNotCore.append(city)
                        else:
                            for i in range(4):
                                cityListInNotCore.append(city)
                    elif iProvType == ProvinceType.NONE:
                        if (
                            city.countTotalCultureTimes100() > 0
                            and (
                                city.getCulture(iPlayer) * 10000 / city.countTotalCultureTimes100()
                            )
                            > 80
                        ):
                            for i in range(3):
                                cityListInNotCore.append(city)
                        elif (
                            city.countTotalCultureTimes100() > 0
                            and (
                                city.getCulture(iPlayer) * 10000 / city.countTotalCultureTimes100()
                            )
                            > 60
                        ):
                            for i in range(5):
                                cityListInNotCore.append(city)
                        elif (
                            city.countTotalCultureTimes100() > 0
                            and (
                                city.getCulture(iPlayer) * 10000 / city.countTotalCultureTimes100()
                            )
                            > 40
                        ):
                            for i in range(7):
                                cityListInNotCore.append(city)
                        else:
                            for i in range(9):
                                cityListInNotCore.append(city)

    if cityListInNotCore or cityListInCore:
        # Absinthe: we only choose among the core cities if there are no non-core ones
        # Absinthe: each city can appear multiple times in both lists
        if cityListInNotCore:
            splittingCity = choice(cityListInNotCore)
        else:
            splittingCity = choice(cityListInCore)

        # Absinthe: city goes to random independent
        iRndNum = rand(
            max(civilizations().independents().ids())
            - min(civilizations().independents().ids())
            + 1
        )
        iIndy = min(civilizations().independents().ids()) + iRndNum

        tCity = (splittingCity.getX(), splittingCity.getY())
        sCityName = splittingCity.getName()
        message(
            iPlayer,
            sCityName + " " + text("TXT_KEY_STABILITY_SECESSION"),
            force=True,
            color=MessageData.ORANGE,
        )
        cultureManager(tCity, 50, iIndy, iPlayer, False, True, True)
        flipUnitsInCitySecession(tCity, iIndy, iPlayer)
        setTempFlippingCity(tCity)
        flipCity(tCity, 0, 0, iIndy, [iPlayer])  # by trade because by conquest may raze the city
        flipUnitsInCityAfter(tCity, iIndy)

        # Absinthe: loosing a city to secession/revolt gives a small boost to stability, to avoid a city-revolting chain reaction
        pPlayer.changeStabilityBase(StabilityCategory.EXPANSION, 1)
        # Absinthe: AI declares war on the indy city right away
        teamPlayer = gc.getTeam(pPlayer.getTeam())
        iTeamIndy = gc.getPlayer(iIndy).getTeam()
        if not teamPlayer.isAtWar(iTeamIndy):
            teamPlayer.declareWar(iTeamIndy, False, WarPlanTypes.WARPLAN_LIMITED)
