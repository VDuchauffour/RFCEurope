from CvPythonExtensions import *
import Barbs
from Consts import MessageData
from Core import (
    civilization,
    civilizations,
    human,
    make_units,
    cities,
    message,
    message_if_human,
    player,
    show,
    show_if_human,
    text,
    year,
)
from CoreTypes import Building, City, Civ, Religion, StabilityCategory, Unit
import Crusades
from Events import handler
from LocationsData import CITIES, CIV_CAPITAL_LOCATIONS
from PyUtils import percentage_chance
from RFCUtils import forcedInvasion
from StoredData import data
import Religions
from Consts import iByzantiumVikingAttack

gc = CyGlobalContext()


@handler("cityAcquired")
def move_ottoman_capital(owner, iPlayer, city, bConquest, bTrade):
    # Constantinople -> Istanbul
    if iPlayer == Civ.OTTOMAN:
        cityList = cities.owner(iPlayer).entities()
        if (city.getX(), city.getY()) == CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM]:
            for loopCity in cityList:
                if loopCity != city:
                    loopCity.setHasRealBuilding((Building.PALACE), False)
            city.setHasRealBuilding(Building.PALACE, True)
            if civilization(Civ.OTTOMAN).has_state_religion(Religion.ISLAM):
                city.setHasReligion(Religion.ISLAM, True, True, False)
            # some stability boost and flavour message
            player(Civ.OTTOMAN).changeStabilityBase(StabilityCategory.EXPANSION, 6)
            message_if_human(
                iPlayer,
                text("TXT_KEY_GLORY_ON_CONQUEST"),
                force=True,
                color=MessageData.GREEN,
            )
        # Absinthe: Edirne becomes capital if conquered before Constantinople
        else:
            if (city.getX(), city.getY()) == (76, 25):
                bHasIstanbul = False
                IstanbulPlot = gc.getMap().plot(*CIV_CAPITAL_LOCATIONS[Civ.BYZANTIUM])
                if IstanbulPlot.isCity():
                    if IstanbulPlot.getPlotCity().getOwner() == iPlayer:
                        bHasIstanbul = True
                if not bHasIstanbul:
                    gc.getPlayer(iPlayer).getCapitalCity().setHasRealBuilding(
                        Building.PALACE, False
                    )
                    city.setHasRealBuilding(Building.PALACE, True)
                if civilization(Civ.OTTOMAN).has_state_religion(Religion.ISLAM):
                    city.setHasReligion(Religion.ISLAM, True, True, False)


@handler("cityAcquired")
def jerusalem_incentive(owner, player, city, bConquest, bTrade):
    # 3Miro: Jerusalem's Golden Age Incentive

    tCity = (city.getX(), city.getY())
    if tCity == CITIES[City.JERUSALEM]:
        pPlayer = gc.getPlayer(player)
        if pPlayer.getStateReligion() == Religion.CATHOLICISM:
            # Absinthe: spread Catholicism if not present already
            if not city.isHasReligion(Religion.CATHOLICISM):
                Religions.spreadReligion(tCity, Religion.CATHOLICISM)
            Crusades.success(player)
            message_if_human(
                human(),
                text("TXT_KEY_CRUSADE_JERUSALEM_SAFE", city.getNameKey()),
                force=True,
                color=MessageData.GREEN,
            )

        # Absinthe: acquiring Jerusalem, with any faith (but not Paganism) -> chance to find a relic
        #             maybe only after a specific date? maybe only if there isn't any ongoing Crusades?
        if (
            percentage_chance(15, strict=True)
            and player in civilizations().majors().ids()
            and pPlayer.getStateReligion() != -1
        ):
            pPlayer.initUnit(
                Unit.HOLY_RELIC,
                CITIES[City.JERUSALEM][0],
                CITIES[City.JERUSALEM][1],
                UnitAITypes.NO_UNITAI,
                DirectionTypes.DIRECTION_SOUTH,
            )


@handler("BeginGameTurn")
def viking_attack_on_constantinople(iGameTurn):
    # Absinthe: 868AD Viking attack on Constantinople
    if iGameTurn == year(860) + data.lEventRandomness[iByzantiumVikingAttack] - 2:
        if human() == Civ.BYZANTIUM:
            show(text("TXT_KEY_EVENT_VIKING_CONQUERERS_RUMOURS"))

    if iGameTurn == year(860) + data.lEventRandomness[iByzantiumVikingAttack]:
        if human() == Civ.BYZANTIUM:
            for unit, number in zip((Unit.DENMARK_HUSKARL, Unit.VIKING_BERSERKER), (3, 4)):
                Barbs.spawnUnits(
                    Civ.BARBARIAN,
                    (80, 24),
                    (80, 25),
                    unit,
                    number,
                    iGameTurn,
                    1,
                    0,
                    forcedInvasion,
                    UnitAITypes.UNITAI_ATTACK,
                    text("TXT_KEY_BARBARIAN_NAMES_VIKINGS"),
                )
            message(
                Civ.BYZANTIUM,
                text("TXT_KEY_EVENT_VIKING_CONQUERERS_ARRIVE"),
                color=MessageData.RED,
            )


@handler("BeginPlayerTurn")
def byzantine_conqueror_army(iGameTurn, iPlayer):
    if iGameTurn == year(520) and iPlayer == Civ.BYZANTIUM:
        pByzantium = gc.getPlayer(Civ.BYZANTIUM)
        tStartingPlot = (59, 16)
        for _ in range(5):
            pByzantium.initUnit(
                Unit.GALLEY,
                tStartingPlot[0],
                tStartingPlot[1],
                UnitAITypes.UNITAI_ASSAULT_SEA,
                DirectionTypes.DIRECTION_SOUTH,
            )
        great_general = pByzantium.initUnit(
            Unit.GREAT_GENERAL,
            tStartingPlot[0],
            tStartingPlot[1],
            UnitAITypes.UNITAI_GENERAL,
            DirectionTypes.DIRECTION_SOUTH,
        )
        great_general.setName(text("TXT_KEY_GREAT_PERSON_BELISARIUS"))
        make_units(Civ.BYZANTIUM, Unit.SWORDSMAN, tStartingPlot, 4)
        make_units(Civ.BYZANTIUM, Unit.AXEMAN, tStartingPlot, 3)
        make_units(Civ.BYZANTIUM, Unit.ARCHER, tStartingPlot, 2)
        show_if_human(iPlayer, text("TXT_KEY_EVENT_CONQUEROR_BELISARIUS"))


def ottoman_invasion(iCiv, tPlot):
    # Absinthe: second Ottoman spawn stack may stay, although they now spawn in Gallipoli in the first place (one plot SE)
    make_units(iCiv, Unit.LONGBOWMAN, tPlot, 2)
    make_units(iCiv, Unit.MACEMAN, tPlot, 2)
    make_units(iCiv, Unit.KNIGHT, tPlot, 3)
    make_units(iCiv, Unit.TURKEY_GREAT_BOMBARD, tPlot, 2)
    make_units(iCiv, Unit.ISLAMIC_MISSIONARY, tPlot, 2)
