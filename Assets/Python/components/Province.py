from CvPythonExtensions import *
from CoreData import civilization, civilizations
from CoreStructures import player
from ProvinceMapData import PROVINCES_MAP
import RFCUtils  # Absinthe
from Scenario import get_scenario  # Absinthe

from TimelineData import DateTurn
from CoreTypes import Province, ProvinceEvent, Scenario, ProvinceType

gc = CyGlobalContext()
utils = RFCUtils.RFCUtils()  # Absinthe


class ProvinceManager:
    def setup(self):
        # set the initial situation for all players
        for civ in civilizations().main():
            for type, provinces in civ.location.provinces.items():
                for province in provinces:
                    civ.player.setProvinceType(province.value, type.value)
        # update provinces for the 1200 AD Scenario
        if get_scenario() == Scenario.i1200AD:
            for civ in civilizations().main():
                if civ.date.birth < DateTurn.i1200AD:
                    self.onSpawn(civ.id)

    def checkTurn(self, iGameTurn):
        for civ in civilizations():
            events = civ.event.provinces.get(ProvinceEvent.ON_DATETURN)
            if events is not None:
                for dateturn, provinces in events.items():
                    if iGameTurn == dateturn:
                        for province, province_type in provinces:
                            civ.player.setProvinceType(province.value, province_type.value)

    def onCityBuilt(self, iPlayer, x, y):
        if iPlayer not in civilizations().main().ids():
            return
        pPlayer = gc.getPlayer(iPlayer)
        iProv = PROVINCES_MAP[y][x]
        if pPlayer.getProvinceType(iProv) == ProvinceType.POTENTIAL.value:
            pPlayer.setProvinceType(iProv, ProvinceType.HISTORICAL.value)
            utils.refreshStabilityOverlay()

    def onCityAcquired(self, owner, iPlayer, city, bConquest, bTrade):
        if iPlayer not in civilizations().main().ids():
            return
        pPlayer = gc.getPlayer(iPlayer)
        iProv = city.getProvince()
        if pPlayer.getProvinceType(iProv) == ProvinceType.POTENTIAL.value:
            pPlayer.setProvinceType(iProv, ProvinceType.HISTORICAL.value)
            utils.refreshStabilityOverlay()

    def onCityRazed(self, iOwner, iPlayer, city):
        pass

    def updatePotential(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        for city in utils.getCityList(iPlayer):
            province = city.getProvince()
            if pPlayer.getProvinceType(province) == ProvinceType.POTENTIAL:
                pPlayer.setProvinceType(province, ProvinceType.HISTORICAL.value)
        utils.refreshStabilityOverlay()

    def onRespawn(self, iPlayer):
        # Absinthe: reset the original potential provinces, but only if they wasn't changed to something entirely different later on
        civ = civilization(iPlayer)
        for province in civ.location.provinces[ProvinceType.HISTORICAL]:
            if civ.player.getProvinceType(province) == ProvinceType.HISTORICAL:
                civ.player.setProvinceType(province.value, ProvinceType.POTENTIAL.value)

        # Absinthe: special respawn conditions
        events = civ.event.provinces.get(ProvinceEvent.ON_RESPAWN)
        if events is not None:
            for province, province_type in events:
                civ.player.setProvinceType(province.value, province_type.value)

    def resetProvinces(self, iPlayer):
        # Absinthe: keep in mind that this will reset all to the initial status, so won't take later province changes into account
        civ = civilization(iPlayer)
        for province in Province:
            civ.player.setProvinceType(province.value, ProvinceType.NONE.value)

        for type, provinces in civ.location.provinces.items():
            for province in provinces:
                civ.player.setProvinceType(province.value, type.value)

    def onSpawn(self, iPlayer):
        # when a new nations spawns, old nations in the region should lose some of their provinces
        events = civilization(iPlayer).event.provinces.get(ProvinceEvent.ON_SPAWN)
        if events is not None:
            for civ, province, province_type in events:
                player(civ).setProvinceType(province.value, province_type.value)

        utils.refreshStabilityOverlay()
