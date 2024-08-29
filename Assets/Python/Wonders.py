from CvPythonExtensions import *
from Core import city, civilizations, human, message, text, year, cities
from CoreTypes import Building, Civ, Specialist, StabilityCategory, Wonder
from PyUtils import rand
from RFCUtils import getUniqueBuilding
from Events import handler
from StoredData import data
from Consts import MessageData, iLighthouseEarthQuake

gc = CyGlobalContext()


@handler("cityAcquired")
def krak_des_chevaliers_acquired(owner, player, city, bConquest, bTrade):
    # Sedna17: code for Krak des Chevaliers
    if bConquest:
        iNewOwner = city.getOwner()
        pNewOwner = gc.getPlayer(iNewOwner)
        if pNewOwner.countNumBuildings(Wonder.KRAK_DES_CHEVALIERS) > 0:
            city.setHasRealBuilding(getUniqueBuilding(iNewOwner, Building.WALLS), True)
            # Absinthe: if the Castle building were built with the Krak, then it should add stability
            #             the safety checks are probably unnecessary, as Castle buildings are destroyed on conquest (theoretically)
            if not (
                city.isHasBuilding(Building.SPANISH_CITADEL)
                or city.isHasBuilding(Building.MOSCOW_KREMLIN)
                or city.isHasBuilding(Building.HUNGARIAN_STRONGHOLD)
                or city.isHasBuilding(Building.CASTLE)
            ):
                city.setHasRealBuilding(getUniqueBuilding(iNewOwner, Building.CASTLE), True)
                pNewOwner.changeStabilityBase(StabilityCategory.EXPANSION, 1)


@handler("BeginGameTurn")
def remove_lighthouse(iGameTurn):
    # Absinthe: Remove the Great Lighthouse, message for the human player if the city is visible
    if iGameTurn == year(1323) - 40 + data.lEventRandomness[iLighthouseEarthQuake]:
        for iPlayer in civilizations().drop(Civ.BARBARIAN).ids():
            bFound = 0
            for city in cities().owner(iPlayer).entities():
                if city.isHasBuilding(Wonder.GREAT_LIGHTHOUSE):
                    city.setHasRealBuilding(Wonder.GREAT_LIGHTHOUSE, False)
                    GLcity = city
                    bFound = 1
            if bFound and human() == iPlayer:
                pPlayer = gc.getPlayer(iPlayer)
                iTeam = pPlayer.getTeam()
                if GLcity.isRevealed(iTeam, False):
                    message(
                        iPlayer,
                        text("TXT_KEY_BUILDING_GREAT_LIGHTHOUSE_REMOVED"),
                        color=MessageData.RED,
                    )


def leaning_tower_effect():
    iGP = rand(7)
    pFlorentia = city(54, 32)
    iSpecialist = Specialist.GREAT_PROPHET + iGP
    pFlorentia.setFreeSpecialistCount(iSpecialist, 1)
