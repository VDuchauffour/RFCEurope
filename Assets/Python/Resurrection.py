from CvPythonExtensions import CyGlobalContext

from Consts import MessageData
from Core import (
    civilization,
    civilizations,
    event_popup,
    human,
    is_minor_civ,
    location,
    make_unit,
    make_units,
    player,
    team,
    text,
    message,
    turn,
    plots,
    cities,
)
from CoreTypes import (
    Area,
    AreaType,
    Building,
    Civ,
    LeaderType,
    StabilityCategory,
    Technology,
    Unit,
)
from PyUtils import percentage, percentage_chance, rand
from RFCUtils import (
    calculateDistance,
    clearPlague,
    createGarrisons,
    cultureManager,
    flipCity,
    flipUnitsInArea,
    flipUnitsInCityAfter,
    flipUnitsInCityBefore,
    pushOutGarrisons,
    relocateSeaGarrisons,
    setPlagueCountdown,
    setTempFlippingCity,
)
from StoredData import data
from Provinces import onRespawn

gc = CyGlobalContext()


def resurrection(iGameTurn, iDeadCiv):
    if iDeadCiv == -1:
        iDeadCiv = findCivToResurect(iGameTurn, 0, -1)
    else:
        iDeadCiv = findCivToResurect(iGameTurn, 1, iDeadCiv)  # For special re-spawn
    if iDeadCiv > -1:
        suppressResurection(iDeadCiv)


def findCivToResurect(iGameTurn, bSpecialRespawn, iDeadCiv):
    if bSpecialRespawn:
        iMinNumCities = 1
    else:
        iMinNumCities = 2

    iRndnum = rand(civilizations().majors().len())
    for j in civilizations().majors().ids():
        if not bSpecialRespawn:
            iDeadCiv = (j + iRndnum) % civilizations().majors().len()
        else:
            iDeadCiv = iDeadCiv  # We want a specific civ for special re-spawn
        cityList = []
        if (
            not gc.getPlayer(iDeadCiv).isAlive()
            and iGameTurn > civilization(iDeadCiv).date.birth + 25
            and iGameTurn > data.players[iDeadCiv].last_turn_alive + 10
        ):  # Sedna17: Allow re-spawns only 10 turns after death and 25 turns after birth
            tile_min = civilization(iDeadCiv).location.area[AreaType.NORMAL][Area.TILE_MIN]
            tile_max = civilization(iDeadCiv).location.area[AreaType.NORMAL][Area.TILE_MAX]

            for city in (
                plots.rectangle(tile_min, tile_max)
                .filter(
                    lambda p: p
                    not in civilization(iDeadCiv).location.area[AreaType.NORMAL][
                        Area.EXCEPTION_TILES
                    ]
                )
                .cities()
                .entities()
            ):
                if is_minor_civ(city.getOwner()):
                    cityList.append(location(city))
                else:
                    iMinNumCitiesOwner = 3
                    iOwnerStability = player(city).getStability()
                    if not player(city).isHuman():
                        iMinNumCitiesOwner = 2
                        iOwnerStability -= 5
                    if player(city).getNumCities() >= iMinNumCitiesOwner:
                        if iOwnerStability < -5:
                            if not city.isWeLoveTheKingDay() and not city.isCapital():
                                cityList.append(location(city))
                        elif iOwnerStability < 0:
                            if (
                                not city.isWeLoveTheKingDay()
                                and not city.isCapital()
                                and location(city) != civilization(city).location.capital
                            ):
                                if (
                                    player(city).getNumCities() > 0
                                ):  # this check is needed, otherwise game crashes
                                    capital = player(city).getCapitalCity()
                                    x, y = location(city)
                                    iDistance = calculateDistance(
                                        x, y, capital.getX(), capital.getY()
                                    )
                                    if (
                                        (iDistance >= 6 and player(city).getNumCities() >= 4)
                                        or city.angryPopulation(0) > 0
                                        or city.goodHealth() - city.badHealth(False) < -1
                                        or city.getReligionBadHappiness() < 0
                                        or city.getLargestCityHappiness() < 0
                                        or city.getHurryAngerModifier() > 0
                                        or city.getNoMilitaryPercentAnger() > 0
                                    ):
                                        cityList.append(location(city))
                        if (
                            not bSpecialRespawn
                            and iOwnerStability < 10
                            and (location(city) == civilization(iDeadCiv).location.capital)
                            and location(city) not in cityList
                        ):
                            cityList.append(location(city))
            if len(cityList) >= iMinNumCities:
                if bSpecialRespawn or percentage_chance(
                    civilization(iDeadCiv).location.respawning_threshold, strict=True
                ):
                    data.rebel_cities = cityList
                    data.rebel_civ = iDeadCiv  # for popup and CollapseCapitals()
                    return iDeadCiv
    return -1


def suppressResurection(iDeadCiv):
    lSuppressList = data.lRebelSuppress
    lCityList = data.rebel_cities
    lCityCount = [0] * civilizations().majors().len()

    for (x, y) in lCityList:
        iOwner = gc.getMap().plot(x, y).getPlotCity().getOwner()
        if iOwner < civilizations().majors().len():
            lCityCount[iOwner] += 1

    iHuman = human()
    for iCiv in civilizations().majors().ids():
        # Absinthe: have to reset the suppress values
        lSuppressList[iCiv] = 0
        if iCiv != iHuman:
            if lCityCount[iCiv] > 0:
                # Absinthe: for the AI there is 30% chance that the actual respawn does not happen (under these suppress situations), only some revolt in the corresponding cities
                if percentage_chance(30, strict=True):
                    lSuppressList[iCiv] = 1
                    for (x, y) in lCityList:
                        pCity = gc.getMap().plot(x, y).getPlotCity()
                        if pCity.getOwner() == iCiv:
                            pCity.changeOccupationTimer(1)
                            pCity.changeHurryAngerTimer(10)

    data.lRebelSuppress = lSuppressList

    if lCityCount[iHuman] > 0:
        rebellionPopup(iDeadCiv, lCityCount[iHuman])
    else:
        resurectCiv(iDeadCiv)


def resurectCiv(iDeadCiv):
    lCityList = data.rebel_cities
    lSuppressList = data.lRebelSuppress
    bSuppressed = True
    iHuman = human()
    lCityCount = [0] * civilizations().majors().len()
    for (x, y) in lCityList:
        iOwner = gc.getMap().plot(x, y).getPlotCity().getOwner()
        if iOwner < civilizations().majors().len():
            lCityCount[iOwner] += 1

    # Absinthe: if any of the AI civs didn't manage to suppress it, there is resurrection
    for iCiv in civilizations().majors().ids():
        if iCiv != iHuman and lCityCount[iCiv] > 0 and lSuppressList[iCiv] == 0:
            bSuppressed = False
    if lCityCount[iHuman] > 0:
        # Absinthe: if the human player didn't choose any suppress options or didn't succeed in it (so it has 0, 2 or 4 in the lSuppressList), there is resurrection
        if lSuppressList[iHuman] in [0, 2, 4]:
            bSuppressed = False
        # Absinthe: if the human player managed to suppress it, message about it
        else:
            message(
                iHuman,
                text("TXT_KEY_SUPPRESSED_RESURRECTION"),
                force=True,
                color=MessageData.GREEN,
            )
    # Absinthe: if neither of the above happened, so everyone managed to suppress it, no resurrection
    if bSuppressed:
        return

    pDeadCiv = gc.getPlayer(iDeadCiv)
    teamDeadCiv = gc.getTeam(pDeadCiv.getTeam())

    # Absinthe: respawn status
    pDeadCiv.setRespawnedAlive(True)
    pDeadCiv.setEverRespawned(True)  # needed for first turn vassalization and peace status fixes

    # Absinthe: store the turn of the latest respawn for each civ
    iGameTurn = turn()
    data.players[iDeadCiv].last_respawn_turn = iGameTurn

    # Absinthe: update province status before the cities are flipped, so potential provinces will update if there are cities in them
    # Absinthe: resetting the original potential provinces, and adding special province changes on respawn (Cordoba)
    onRespawn(iDeadCiv)

    # Absinthe: we shouldn't get a previous leader on respawn - would be changed to a newer one in a couple turns anyway
    # 			instead we have a random chance to remain with the leader before the collapse, or to switch to the next one
    leaders = civilization(iDeadCiv).leaders[LeaderType.LATE]
    if leaders:
        # no change if we are already at the last leader
        for leader in leaders[:-1]:
            if pDeadCiv.getLeader() == leader[0]:
                if percentage_chance(60, strict=True):
                    pDeadCiv.setLeader(leader[0])
                break

    for iCiv in civilizations().majors().ids():
        if iCiv != iDeadCiv:
            if teamDeadCiv.isAtWar(iCiv):
                teamDeadCiv.makePeace(iCiv)
    data.players[iDeadCiv].num_cities = 0  # reset collapse condition

    # Absinthe: reset vassalage and update dynamic civ names
    for iOtherCiv in civilizations().majors().ids():
        if iOtherCiv != iDeadCiv:
            if teamDeadCiv.isVassal(iOtherCiv) or gc.getTeam(
                gc.getPlayer(iOtherCiv).getTeam()
            ).isVassal(iDeadCiv):
                teamDeadCiv.freeVassal(iOtherCiv)
                gc.getTeam(gc.getPlayer(iOtherCiv).getTeam()).freeVassal(iDeadCiv)
                gc.getPlayer(iOtherCiv).processCivNames()
                gc.getPlayer(iDeadCiv).processCivNames()

    # Absinthe: no vassalization in the first 10 turns after resurrection?

    iNewUnits = 2
    if data.players[iDeadCiv].latest_rebellion_turn > 0:
        iNewUnits = 4
    data.players[iDeadCiv].latest_rebellion_turn = turn()
    bHuman = False
    for (x, y) in lCityList:
        if gc.getMap().plot(x, y).getPlotCity().getOwner() == iHuman:
            bHuman = True
            break

    ownersList = []
    bAlreadyVassal = False
    for tCity in lCityList:
        pCity = gc.getMap().plot(tCity[0], tCity[1]).getPlotCity()
        iOwner = pCity.getOwner()
        teamOwner = gc.getTeam(gc.getPlayer(iOwner).getTeam())
        bOwnerVassal = teamOwner.isAVassal()
        bOwnerHumanVassal = teamOwner.isVassal(iHuman)

        if iOwner >= civilizations().majors().len():
            cultureManager(tCity, 100, iDeadCiv, iOwner, False, True, True)
            flipUnitsInCityBefore(tCity, iDeadCiv, iOwner)
            setTempFlippingCity(tCity)
            flipCity(tCity, 0, 0, iDeadCiv, [iOwner])
            flipUnitsInCityAfter(tCity, iOwner)
            flipUnitsInArea(
                (tCity[0] - 2, tCity[1] - 2),
                (tCity[0] + 2, tCity[1] + 2),
                iDeadCiv,
                iOwner,
                True,
                False,
            )
        else:
            if lSuppressList[iOwner] in [0, 2, 4]:
                cultureManager(tCity, 50, iDeadCiv, iOwner, False, True, True)
                pushOutGarrisons(tCity, iOwner)
                relocateSeaGarrisons(tCity, iOwner)
                setTempFlippingCity(tCity)
                flipCity(
                    tCity, 0, 0, iDeadCiv, [iOwner]
                )  # by trade because by conquest may raze the city
                createGarrisons(tCity, iDeadCiv, iNewUnits)

            # 3Miro: indent to make part of the else on the if statement, otherwise one can make peace with the Barbs
            bAtWar = False  # AI won't vassalise if another owner has declared war; on the other hand, it won't declare war if another one has vassalised
            if (
                iOwner != iHuman
                and iOwner not in ownersList
                and iOwner != iDeadCiv
                and lSuppressList[iOwner] == 0
            ):  # declare war or peace only once - the 3rd condition is obvious but "vassal of themselves" was happening
                rndNum = percentage()
                if (
                    rndNum >= civilization(iOwner).ai.stop_birth_threshold
                    and not bOwnerHumanVassal
                    and not bAlreadyVassal
                ):  # if bOwnerHumanVassal is True, it will skip to the 3rd condition, as bOwnerVassal is True as well
                    if not teamOwner.isAtWar(iDeadCiv):
                        teamOwner.declareWar(iDeadCiv, False, -1)
                    bAtWar = True
                # Absinthe: do we really want to auto-vassal them on respawn? why?
                # 			set it to 0 from 60 temporarily (so it's never True), as a quick fix until the mechanics are revised
                elif rndNum <= 0 - (civilization(iOwner).ai.stop_birth_threshold / 2):
                    if teamOwner.isAtWar(iDeadCiv):
                        teamOwner.makePeace(iDeadCiv)
                    if (
                        not bAlreadyVassal and not bHuman and not bOwnerVassal and not bAtWar
                    ):  # bHuman == False cos otherwise human player can be deceived to declare war without knowing the new master
                        gc.getTeam(gc.getPlayer(iDeadCiv).getTeam()).setVassal(iOwner, True, False)
                        gc.getPlayer(
                            iOwner
                        ).processCivNames()  # setVassal already updates DCN for iDeadCiv
                        bAlreadyVassal = True
                else:
                    if teamOwner.isAtWar(iDeadCiv):
                        teamOwner.makePeace(iDeadCiv)
                ownersList.append(iOwner)
                for iTech in range(len(Technology)):
                    if teamOwner.isHasTech(iTech):
                        teamDeadCiv.setHasTech(iTech, True, iDeadCiv, False, False)

    # all techs added from minor civs
    for iTech in range(len(Technology)):
        if (
            team(Civ.BARBARIAN).isHasTech(iTech)
            or team(Civ.INDEPENDENT).isHasTech(iTech)
            or team(Civ.INDEPENDENT_2).isHasTech(iTech)
            or team(Civ.INDEPENDENT_3).isHasTech(iTech)
            or team(Civ.INDEPENDENT_4).isHasTech(iTech)
        ):
            teamDeadCiv.setHasTech(iTech, True, iDeadCiv, False, False)

    moveBackCapital(iDeadCiv)

    if player().isExisting():
        message(
            iHuman,
            text("TXT_KEY_INDEPENDENCE_TEXT", pDeadCiv.getCivilizationAdjectiveKey()),
            force=True,
            color=MessageData.DARK_PINK,
        )
    if lSuppressList[iHuman] in [2, 3, 4]:
        if not gc.getTeam(gc.getPlayer(iHuman).getTeam()).isAtWar(iDeadCiv):
            gc.getTeam(gc.getPlayer(iHuman).getTeam()).declareWar(iDeadCiv, False, -1)
    else:
        if gc.getTeam(gc.getPlayer(iHuman).getTeam()).isAtWar(iDeadCiv):
            gc.getTeam(gc.getPlayer(iHuman).getTeam()).makePeace(iDeadCiv)

    # Absinthe: the new civs start as slightly stable
    pDeadCiv.changeStabilityBase(
        StabilityCategory.CITIES,
        -pDeadCiv.getStabilityBase(StabilityCategory.CITIES),
    )
    pDeadCiv.changeStabilityBase(
        StabilityCategory.CIVICS,
        -pDeadCiv.getStabilityBase(StabilityCategory.CIVICS),
    )
    pDeadCiv.changeStabilityBase(
        StabilityCategory.ECONOMY,
        -pDeadCiv.getStabilityBase(StabilityCategory.ECONOMY),
    )
    pDeadCiv.changeStabilityBase(
        StabilityCategory.EXPANSION,
        -pDeadCiv.getStabilityBase(StabilityCategory.EXPANSION),
    )
    pDeadCiv.changeStabilityBase(StabilityCategory.EXPANSION, 5)

    # Absinthe: refresh dynamic civ name for the new civ
    pDeadCiv.processCivNames()

    setPlagueCountdown(iDeadCiv, -10)
    clearPlague(iDeadCiv)
    convertBackCulture(iDeadCiv)

    # Absinthe: alive status is now updated right on respawn, otherwise it would only update on the beginning of the next turn
    pDeadCiv.setAlive(True)


def moveBackCapital(iCiv):
    cityList = cities.owner(iCiv).entities()
    tiles = civilization(iCiv).location.get(
        lambda c: c.new_capital, [civilization(iCiv).location.capital]
    )

    # TODO: remove for/else implementation
    for tile in tiles:
        plot = gc.getMap().plot(*tile)
        if plot.isCity():
            newCapital = plot.getPlotCity()
            if newCapital.getOwner() == iCiv:
                if not newCapital.hasBuilding(Building.PALACE):
                    for city in cityList:
                        city.setHasRealBuilding((Building.PALACE), False)
                    newCapital.setHasRealBuilding((Building.PALACE), True)
                    makeResurectionUnits(iCiv, newCapital.getX(), newCapital.getY())
    else:
        iMaxValue = 0
        bestCity = None
        for loopCity in cityList:
            # loopCity.AI_cityValue() doesn't work as area AI types aren't updated yet
            loopValue = max(0, 500 - loopCity.getGameTurnFounded()) + loopCity.getPopulation() * 10
            if loopValue > iMaxValue:
                iMaxValue = loopValue
                bestCity = loopCity
        if bestCity is not None:
            for loopCity in cityList:
                if loopCity != bestCity:
                    loopCity.setHasRealBuilding((Building.PALACE), False)
            bestCity.setHasRealBuilding((Building.PALACE), True)
            makeResurectionUnits(iCiv, bestCity.getX(), bestCity.getY())


def makeResurectionUnits(iPlayer, iX, iY):
    if iPlayer == Civ.CORDOBA:
        make_units(Civ.CORDOBA, Unit.SETTLER, (iX, iY), 2)
        make_units(Civ.CORDOBA, Unit.CROSSBOWMAN, (iX, iY), 2)
        make_unit(Civ.CORDOBA, Unit.ISLAMIC_MISSIONARY, (iX, iY))


def convertBackCulture(iCiv):
    # 3Miro: same as Normal Areas in Resurrection
    # Sedna17: restored to be normal areas, not core
    # collect all the cities in the region
    for city in (
        plots.rectangle(
            civilization(iCiv).location.area[AreaType.NORMAL][Area.TILE_MIN],
            civilization(iCiv).location.area[AreaType.NORMAL][Area.TILE_MAX],
        )
        .cities()
        .entities()
    ):
        for plot in plots.surrounding(location(city)).entities():
            iCivCulture = plot.getCulture(iCiv)
            iLoopCivCulture = 0
            for civ in civilizations().minors().ids():
                iLoopCivCulture += plot.getCulture(civ)
                plot.setCulture(civ, 0, True)
            plot.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)

        iCivCulture = city.getCulture(iCiv)
        iLoopCivCulture = 0
        for civ in civilizations().minors().ids():
            iLoopCivCulture += plot.getCulture(civ)
            plot.setCulture(civ, 0, True)
        city.setCulture(iCiv, iCivCulture + iLoopCivCulture, True)


# resurrection when some human controlled cities are also included
def rebellionPopup(iRebelCiv, iNumCities):
    iLoyalPrice = min((10 * gc.getPlayer(human()).getGold()) / 100, 50 * iNumCities)
    event_popup(
        7622,
        text("TXT_KEY_REBELLION_TITLE"),
        text("TXT_KEY_REBELLION_HUMAN", player(iRebelCiv).getCivilizationAdjectiveKey()),
        [
            text("TXT_KEY_REBELLION_LETGO"),
            text("TXT_KEY_REBELLION_DONOTHING"),
            text("TXT_KEY_REBELLION_CRACK"),
            text("TXT_KEY_REBELLION_BRIBE") + " " + str(iLoyalPrice),
            text("TXT_KEY_REBELLION_BOTH"),
        ],
    )
