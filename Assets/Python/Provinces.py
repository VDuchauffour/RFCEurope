from Core import get_scenario, civilization, civilizations, player, year, cities
from RFCUtils import refreshStabilityOverlay
from ProvinceMapData import PROVINCES_MAP
from CoreTypes import Province, Event, Scenario, ProvinceType
from Events import handler


@handler("GameStart")
def setup():
    # set the initial situation for all players
    for civ in civilizations().main():
        for type, provinces in civ.location.provinces.items():
            for province in provinces:
                civ.player.setProvinceType(province, type)
    # update provinces for the 1200 AD Scenario
    if get_scenario() == Scenario.i1200AD:
        for civ in civilizations().main():
            if year(civ.date.birth) < year(1200):
                onSpawn(civ.id)


def onSpawn(iPlayer):
    # when a new nations spawns, old nations in the region should lose some of their provinces
    events = civilization(iPlayer).event.provinces.get(Event.ON_SPAWN)
    if events is not None:
        for civ, province, province_type in events:
            player(civ).setProvinceType(province, province_type)

    refreshStabilityOverlay()


@handler("BeginGameTurn")
def checkTurn(iGameTurn):
    for civ in civilizations():
        events = civ.event.provinces.get(Event.ON_DATETURN)
        if events is not None:
            for dateturn, provinces in events.items():
                if iGameTurn == year(dateturn):
                    for province, province_type in provinces:
                        civ.player.setProvinceType(province, province_type)


def onCityBuilt(iPlayer, x, y):
    if iPlayer not in civilizations().main().ids():
        return
    civ = civilization(iPlayer)
    province = PROVINCES_MAP[y][x]
    if civ.player.getProvinceType(province) == ProvinceType.POTENTIAL:
        civ.player.setProvinceType(province, ProvinceType.HISTORICAL)
        refreshStabilityOverlay()


@handler("cityAcquired")
def onCityAcquired(owner, iPlayer, city, bConquest, bTrade):
    if iPlayer not in civilizations().main().ids():
        return
    civ = civilization(iPlayer)
    province = city.getProvince()
    if civ.player.getProvinceType(province) == ProvinceType.POTENTIAL:
        civ.player.setProvinceType(province, ProvinceType.HISTORICAL)
        refreshStabilityOverlay()


def updatePotential(iPlayer):
    civ = civilization(iPlayer)
    for city in cities.owner(iPlayer).entities():
        province = city.getProvince()
        if civ.player.getProvinceType(province) == ProvinceType.POTENTIAL:
            civ.player.setProvinceType(province, ProvinceType.HISTORICAL)
    refreshStabilityOverlay()


def onRespawn(iPlayer):
    # Absinthe: reset the original potential provinces, but only if they wasn't changed to something entirely different later on
    civ = civilization(iPlayer)
    for province in civ.location.provinces[ProvinceType.HISTORICAL]:
        if civ.player.getProvinceType(province) == ProvinceType.HISTORICAL:
            civ.player.setProvinceType(province, ProvinceType.POTENTIAL)

    # Absinthe: special respawn conditions
    events = civ.event.provinces.get(Event.ON_RESPAWN)
    if events is not None:
        for province, province_type in events:
            civ.player.setProvinceType(province, province_type)


def resetProvinces(iPlayer):
    # Absinthe: keep in mind that this will reset all to the initial status, so won't take later province changes into account
    civ = civilization(iPlayer)
    for province in Province:
        civ.player.setProvinceType(province, ProvinceType.NONE)

    for type, provinces in civ.location.provinces.items():
        for province in provinces:
            civ.player.setProvinceType(province, type)
