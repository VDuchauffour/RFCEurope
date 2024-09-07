# Rhye's and Fall of Civilization: Europe - Unique Powers (only a couple of them is here, most are handled in the .dll)
from CvPythonExtensions import *
from Core import (
    civilization,
    message_if_human,
    player,
    human,
    turn,
    year,
    message,
    text,
    make_unit,
    cities,
    plots,
    infos,
)
from CoreTypes import Building, Civ, SpecialParameter, Religion, Technology, UniquePower, Unit
from RFCUtils import getMaster, getUniqueUnit
from Consts import MessageData
from PyUtils import choice
from Events import handler

gc = CyGlobalContext()


@handler("cityAcquired")
def ottoman_up_1(owner, player_id, city, bConquest, bTrade):
    if gc.hasUP(player_id, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS):
        janissaryNewCityUP(player_id, city, bConquest)


@handler("BeginPlayerTurn")
def ottoman_up_2(iGameTurn, iPlayer):
    # janissaryDraftUP
    if gc.hasUP(iPlayer, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS):
        pPlayer = gc.getPlayer(iPlayer)
        iStateReligion = pPlayer.getStateReligion()

        iNewPoints = 0
        for city in cities.owner(iPlayer).entities():
            for iReligion in range(len(Religion)):
                if iReligion != iStateReligion and city.isHasReligion(iReligion):
                    iNewPoints += city.getPopulation()
                    break

        iOldPoints = pPlayer.getPicklefreeParameter(SpecialParameter.JANISSARY_POINTS)

        iNextJanissary = 200
        if pPlayer.isHuman():
            iNextJanissary = 300

        iTotalPoints = iOldPoints + iNewPoints
        while iTotalPoints >= iNextJanissary:
            pCity = cities.owner(iPlayer).random_entry()
            if pCity is not None:
                iTotalPoints -= iNextJanissary
                make_unit(iPlayer, Unit.JANISSARY, pCity)
                message_if_human(
                    iPlayer,
                    text("TXT_KEY_UNIT_NEW_JANISSARY") + " " + pCity.getName() + "!",
                    sound="AS2D_UNIT_BUILD_UNIQUE_UNIT",
                    button=gc.getUnitInfo(Unit.JANISSARY).getButton(),
                    color=MessageData.GREEN,
                    location=pCity,
                )
        pPlayer.setPicklefreeParameter(SpecialParameter.JANISSARY_POINTS, iTotalPoints)


@handler("BeginPlayerTurn")
def danish_up(iGameTurn, iPlayer):
    if iPlayer == Civ.DENMARK:
        lSoundCoords = [(60, 57), (60, 58)]

        # Check if we control the Sound
        bControlsSound = False
        for tCoord in lSoundCoords:
            pPlot = gc.getMap().plot(tCoord[0], tCoord[1])
            if pPlot.calculateCulturalOwner() == iPlayer:
                bControlsSound = True
                break
        if not bControlsSound:
            return

        iCities = getNumForeignCitiesOnBaltic(iPlayer)
        iGold = iCities * 2
        gc.getPlayer(iPlayer).changeGold(iGold)
        message(iPlayer, text("TXT_KEY_UP_SOUND_TOLL", iGold), color=MessageData.GREEN)


@handler("cityAcquired")
def scottish_up(owner, player_id, city, bConquest, bTrade):
    # against all players (including indies and barbs), but only on conquest
    # only in cities with at least 20% Scottish culture
    if owner == Civ.SCOTLAND and bConquest:
        iTotalCulture = city.countTotalCultureTimes100()
        if iTotalCulture == 0 or (city.getCulture(owner) * 10000) / iTotalCulture > 20:
            defianceUP(owner)


@handler("cityAcquired")
def aragon_up_on_city_acquired(owner, player_id, city, bConquest, bTrade):
    # Absinthe: Aragonese UP
    # UP tile yields should be recalculated right away, in case the capital was conquered, or province number changed
    if owner == Civ.ARAGON:
        confederationUP(owner)
    if player_id == Civ.ARAGON:
        confederationUP(player_id)


@handler("cityRazed")
def aragon_up_on_city_razed(city, iPlayer):
    # UP tile yields should be recalculated if your new city is razed
    if iPlayer == Civ.ARAGON:
        confederationUP(iPlayer)


@handler("cityBuilt")
def aragon_up_on_city_built(city):
    # UP tile yields should be recalculated on city foundation
    iPlayer = city.getOwner()
    if iPlayer == Civ.ARAGON:
        confederationUP(iPlayer)


@handler("BeginPlayerTurn")
def aragon_up_on_begin_player_turn(iGameTurn, iPlayer):
    # safety check: probably redundant, calls from onBuildingBuilt, onCityBuilt, onCityAcquired and onCityRazed should be enough
    if iPlayer == Civ.ARAGON:
        confederationUP(iPlayer)


@handler("buildingBuilt")
def aragon_up_on_building_built(city, building_type):
    # UP tile yields should be recalculated right away if a new Palace was built
    iPlayer = city.getOwner()
    if iPlayer == Civ.ARAGON and building_type == Building.PALACE:
        confederationUP(iPlayer)


@handler("cityBuilt")
def portugal_up_on_city_built(city):
    iPlayer = city.getOwner()
    if iPlayer == Civ.PORTUGAL and civilization(Civ.PORTUGAL).has_tech(Technology.ASTRONOMY):
        city.setHasRealBuilding(Building.PORTUGAL_FEITORIA, True)


@handler("combatResult")
def norway_up(winning_unit, losing_unit):
    if winning_unit.getOwner() == Civ.NORWAY and turn() < year(1066) + 2:
        if infos.unit(losing_unit).getDomainType() == DomainTypes.DOMAIN_SEA:
            if losing_unit.getUnitType() != Unit.WORKBOAT:
                player(Civ.NORWAY).setUHVCounter(0, player(Civ.NORWAY).getUHVCounter(0) + 2)
            else:
                player(Civ.NORWAY).setUHVCounter(0, player(Civ.NORWAY).getUHVCounter(0) + 1)


# Absinthe: Arabian UP
def faithUP(iPlayer, city):
    pFaithful = gc.getPlayer(iPlayer)
    iStateReligion = pFaithful.getStateReligion()
    iTemple = 0
    # Absinthe: shouldn't work on minor religions, to avoid exploit with spreading Judaism this way
    if 0 <= iStateReligion <= 3:
        if not city.isHasReligion(iStateReligion):
            city.setHasReligion(iStateReligion, True, True, False)
            pFaithful.changeFaith(1)

        if iStateReligion == 0:
            iTemple = Building.PROTESTANT_TEMPLE
        elif iStateReligion == 1:
            iTemple = Building.ISLAMIC_TEMPLE
        elif iStateReligion == 2:
            iTemple = Building.CATHOLIC_TEMPLE
        elif iStateReligion == 3:
            iTemple = Building.ORTHODOX_TEMPLE
        if not city.hasBuilding(iTemple):
            city.setHasRealBuilding(iTemple, True)
            pFaithful.changeFaith(1)


def janissaryNewCityUP(iPlayer, city, bConquest):
    pPlayer = gc.getPlayer(iPlayer)
    iStateReligion = pPlayer.getStateReligion()
    for iReligion in range(len(Religion)):
        if iReligion != iStateReligion and city.isHasReligion(iReligion):
            iCityPopulation = city.getPopulation()
            # more janissary points on conquest, less on flip and trade
            if bConquest:
                iJanissaryPoint = iCityPopulation * 9
            else:
                iJanissaryPoint = iCityPopulation * 4
            iOldPoints = pPlayer.getPicklefreeParameter(SpecialParameter.JANISSARY_POINTS)
            pPlayer.setPicklefreeParameter(
                SpecialParameter.JANISSARY_POINTS, iOldPoints + iJanissaryPoint
            )
            break

    # removed free janissary, probably too powerful to add a new janissary unit right on conquest
    iIsHasForeignReligion = 0
    if iIsHasForeignReligion:
        make_unit(iPlayer, Unit.JANISSARY, city)
        message_if_human(
            iPlayer,
            text("TXT_KEY_UNIT_NEW_JANISSARY") + " " + city.getName() + "!",
            sound="AS2D_UNIT_BUILD_UNIQUE_UNIT",
            button=gc.getUnitInfo(Unit.JANISSARY).getButton(),
            color=MessageData.GREEN,
            location=city,
        )


def getNumForeignCitiesOnBaltic(iPlayer, bVassal=False):
    lBalticRects = [
        ((56, 52), (70, 57)),
        ((62, 58), (74, 62)),
        ((64, 63), (79, 66)),
        ((64, 67), (71, 72)),
    ]

    # Count foreign coastal cities
    iCities = 0
    for start, end in lBalticRects:
        for city in plots.rectangle(start, end).cities().coastal(5).not_owner(iPlayer).entities():
            if not bVassal or city.getOwner() != getMaster(city.getOwner()) != iPlayer:
                iCities += 1
    return iCities


# Absinthe: Aragonese UP
def confederationUP(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    capital = pPlayer.getCapitalCity()
    iCapitalX = capital.getX()
    iCapitalY = capital.getY()

    # Collect all provinces
    cityProvinces = []
    for city in cities.owner(iPlayer).entities():
        pProvince = city.getProvince()
        cityProvinces.append(pProvince)
    # Calculate unique provinces
    uniqueProvinces = set(cityProvinces)
    iProvinces = len(uniqueProvinces)

    # Note that Aragon do not use any of its UHV counters, so we can safely use them here
    # Do not recalculate if we have the same number of provinces as in the last check, and the capital has not changed
    if (
        iProvinces == pPlayer.getUHVCounter(1)
        and pPlayer.getUHVCounter(2) == 100 * iCapitalX + iCapitalY
    ):
        return

    # Store the province number for the next check
    pPlayer.setUHVCounter(1, iProvinces)

    # On capital change, reset yield for the previous capital's tile, also reset the commerce counter
    if pPlayer.getUHVCounter(2) != 100 * iCapitalX + iCapitalY:
        iOldCapitalX = pPlayer.getUHVCounter(2) / 100
        iOldCapitalY = pPlayer.getUHVCounter(2) % 100
        iProvinceCommerceLastBonus = pPlayer.getUHVCounter(0)
        gc.getGame().setPlotExtraYield(iOldCapitalX, iOldCapitalY, 2, -iProvinceCommerceLastBonus)
        # If there was a capital change, the discount should be 0 for the new capital's tile
        pPlayer.setUHVCounter(0, 0)
        # New capital's coordinates are stored for the next check
        pPlayer.setUHVCounter(2, 100 * iCapitalX + iCapitalY)

    # Update tile yield for the capital's plot
    iProvinceCommerceLastBonus = pPlayer.getUHVCounter(0)
    gc.getGame().setPlotExtraYield(iCapitalX, iCapitalY, 2, -iProvinceCommerceLastBonus)
    iProvinceCommerceNextBonus = (
        iProvinces * 2
    )  # <- This number is the amount of extra commerce per province
    gc.getGame().setPlotExtraYield(iCapitalX, iCapitalY, 2, iProvinceCommerceNextBonus)
    # Tile yield is stored for the next check
    pPlayer.setUHVCounter(0, iProvinceCommerceNextBonus)


# Absinthe: Scottish UP
def defianceUP(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    # One ranged/gun class
    RangedClass = getUniqueUnit(iPlayer, Unit.ARCHER)
    lRangedList = [
        Unit.LINE_INFANTRY,
        Unit.MUSKETMAN,
        Unit.LONGBOWMAN,
        Unit.ARBALEST,
        Unit.CROSSBOWMAN,
        Unit.ARCHER,
    ]
    for iUnit in lRangedList:
        if pPlayer.canTrain(getUniqueUnit(iPlayer, iUnit), False, False):
            RangedClass = getUniqueUnit(iPlayer, iUnit)
            break

    # One polearm class
    PolearmClass = getUniqueUnit(iPlayer, Unit.SPEARMAN)
    lPolearmList = [Unit.LINE_INFANTRY, Unit.PIKEMAN, Unit.GUISARME]
    for iUnit in lPolearmList:
        if pPlayer.canTrain(getUniqueUnit(iPlayer, iUnit), False, False):
            PolearmClass = getUniqueUnit(iPlayer, iUnit)
            break

    for city in cities.owner(iPlayer).entities():
        # only in cities with at least 20% Scottish culture
        iTotalCulture = city.countTotalCultureTimes100()
        if iTotalCulture == 0 or (city.getCulture(iPlayer) * 10000) / iTotalCulture > 20:
            make_unit(iPlayer, choice([RangedClass, PolearmClass]), city)
            # interface message for the human player
            if iPlayer == human():
                text_string = text("TXT_KEY_UNIT_NEW_DEFENDER") + " " + city.getName() + "!"
                message(
                    iPlayer,
                    text_string,
                    sound="AS2D_UNIT_BUILD_UNIQUE_UNIT",
                    color=MessageData.GREEN,
                    location=city,
                )
