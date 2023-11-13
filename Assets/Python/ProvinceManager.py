from CvPythonExtensions import *
from CoreData import civilization, civilizations
from CoreStructures import player
from MapsData import PROVINCES_MAP
import RFCUtils  # Absinthe
import PyHelpers  # Absinthe

from TimelineData import DateTurn
from CoreTypes import Civ, Province, ProvinceEvent, Scenario, ProvinceType

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer  # Absinthe
utils = RFCUtils.RFCUtils()  # Absinthe


class ProvinceManager:
    def setup(self):
        # set the initial situation for all players
        for civ in civilizations().main():
            for type, provinces in civ.location.provinces.items():
                for province in provinces:
                    civ.player.setProvinceType(province.value, type.value)
        # update provinces for the 1200 AD Scenario
        if utils.getScenario() == Scenario.i1200AD:
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
            for provinces in events.values():
                for province, province_type in provinces:
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
        if iPlayer == Civ.ARABIA.value:
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CYRENAICA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.TRIPOLITANIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.IFRIQIYA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.EGYPT.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.ARABIA.value, ProvinceType.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.SYRIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.LEBANON.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.JERUSALEM.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ANTIOCHIA.value, ProvinceType.HISTORICAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CILICIA.value, ProvinceType.HISTORICAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CHARSIANON.value, ProvinceType.HISTORICAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.COLONEA.value, ProvinceType.HISTORICAL.value
            )
        elif iPlayer == Civ.BULGARIA.value:
            player(Civ.BYZANTIUM).setProvinceType(
                Province.SERBIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.MOESIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.THRACE.value, ProvinceType.HISTORICAL.value
            )
        elif iPlayer == Civ.VENECIA.value:
            player(Civ.BYZANTIUM).setProvinceType(Province.DALMATIA.value, ProvinceType.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.BOSNIA.value, ProvinceType.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.SLAVONIA.value, ProvinceType.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.VERONA.value, ProvinceType.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.TUSCANY.value, ProvinceType.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.LOMBARDY.value, ProvinceType.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.LIGURIA.value, ProvinceType.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.CORSICA.value, ProvinceType.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.SARDINIA.value, ProvinceType.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.LATIUM.value, ProvinceType.NONE.value)
        elif iPlayer == Civ.BURGUNDY.value:
            # these areas flip to Burgundy, so resetting them to Potential won't cause any issues
            player(Civ.FRANCE).setProvinceType(
                Province.PROVENCE.value, ProvinceType.POTENTIAL.value
            )
            player(Civ.FRANCE).setProvinceType(
                Province.BURGUNDY.value, ProvinceType.POTENTIAL.value
            )
        elif iPlayer == Civ.GERMANY.value:
            player(Civ.FRANCE).setProvinceType(
                Province.LORRAINE.value, ProvinceType.CONTESTED.value
            )
            player(Civ.FRANCE).setProvinceType(Province.BAVARIA.value, ProvinceType.NONE.value)
            player(Civ.FRANCE).setProvinceType(Province.FRANCONIA.value, ProvinceType.NONE.value)
            player(Civ.FRANCE).setProvinceType(Province.SAXONY.value, ProvinceType.NONE.value)
            player(Civ.FRANCE).setProvinceType(Province.NETHERLANDS.value, ProvinceType.NONE.value)
        elif iPlayer == Civ.HUNGARY.value:
            player(Civ.BULGARIA).setProvinceType(Province.BANAT.value, ProvinceType.NONE.value)
            player(Civ.BULGARIA).setProvinceType(
                Province.WALLACHIA.value, ProvinceType.CONTESTED.value
            )
        elif iPlayer == Civ.CASTILE.value:
            player(Civ.CORDOBA).setProvinceType(
                Province.LA_MANCHA.value, ProvinceType.HISTORICAL.value
            )
        elif iPlayer == Civ.MOROCCO.value:
            player(Civ.CORDOBA).setProvinceType(Province.MOROCCO.value, ProvinceType.NONE.value)
            player(Civ.CORDOBA).setProvinceType(Province.MARRAKESH.value, ProvinceType.NONE.value)
            player(Civ.CORDOBA).setProvinceType(Province.FEZ.value, ProvinceType.CONTESTED.value)
            player(Civ.CORDOBA).setProvinceType(
                Province.TETOUAN.value, ProvinceType.CONTESTED.value
            )
        elif iPlayer == Civ.ENGLAND.value:
            player(Civ.FRANCE).setProvinceType(
                Province.NORMANDY.value, ProvinceType.POTENTIAL.value
            )  # it flips to England, so resetting them to Potential won't cause any issues
            player(Civ.SCOTLAND).setProvinceType(
                Province.NORTHUMBRIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.SCOTLAND).setProvinceType(Province.MERCIA.value, ProvinceType.NONE.value)
            player(Civ.DENMARK).setProvinceType(
                Province.NORTHUMBRIA.value, ProvinceType.NONE.value
            )
            player(Civ.DENMARK).setProvinceType(Province.MERCIA.value, ProvinceType.NONE.value)
            player(Civ.DENMARK).setProvinceType(
                Province.EAST_ANGLIA.value, ProvinceType.NONE.value
            )
            player(Civ.DENMARK).setProvinceType(Province.LONDON.value, ProvinceType.NONE.value)
        elif iPlayer == Civ.ARAGON.value:
            player(Civ.BYZANTIUM).setProvinceType(
                Province.APULIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CALABRIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.SICILY.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.MALTA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.CORDOBA).setProvinceType(
                Province.ARAGON.value, ProvinceType.CONTESTED.value
            )
            player(Civ.CORDOBA).setProvinceType(
                Province.CATALONIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.CORDOBA).setProvinceType(
                Province.VALENCIA.value, ProvinceType.HISTORICAL.value
            )
            player(Civ.CORDOBA).setProvinceType(
                Province.BALEARS.value, ProvinceType.CONTESTED.value
            )
        elif iPlayer == Civ.SWEDEN.value:
            player(Civ.NORWAY).setProvinceType(Province.SVEALAND.value, ProvinceType.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.GOTALAND.value, ProvinceType.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.SVEALAND.value, ProvinceType.NONE.value)
            player(Civ.NOVGOROD).setProvinceType(
                Province.OSTERLAND.value, ProvinceType.CONTESTED.value
            )
        elif iPlayer == Civ.AUSTRIA.value:
            player(Civ.HUNGARY).setProvinceType(
                Province.CARINTHIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.HUNGARY).setProvinceType(
                Province.AUSTRIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.HUNGARY).setProvinceType(
                Province.MORAVIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.HUNGARY).setProvinceType(Province.BAVARIA.value, ProvinceType.NONE.value)
            player(Civ.GERMANY).setProvinceType(
                Province.BAVARIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.GERMANY).setProvinceType(
                Province.BOHEMIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.CASTILE).setProvinceType(
                Province.NETHERLANDS.value, ProvinceType.CONTESTED.value
            )
            player(Civ.CASTILE).setProvinceType(
                Province.FLANDERS.value, ProvinceType.CONTESTED.value
            )
        elif iPlayer == Civ.OTTOMAN.value:
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ANTIOCHIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CILICIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CHARSIANON.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.COLONEA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ARMENIAKON.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CYPRUS.value, ProvinceType.CONTESTED.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ANATOLIKON.value, ProvinceType.HISTORICAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.OPSIKION.value, ProvinceType.HISTORICAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.THRAKESION.value, ProvinceType.HISTORICAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.PAPHLAGONIA.value, ProvinceType.HISTORICAL.value
            )
            player(Civ.HUNGARY).setProvinceType(
                Province.DALMATIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.HUNGARY).setProvinceType(
                Province.BOSNIA.value, ProvinceType.CONTESTED.value
            )
            player(Civ.HUNGARY).setProvinceType(Province.BANAT.value, ProvinceType.CONTESTED.value)
        elif iPlayer == Civ.MOSCOW.value:
            player(Civ.NOVGOROD).setProvinceType(
                Province.ROSTOV.value, ProvinceType.CONTESTED.value
            )
            player(Civ.NOVGOROD).setProvinceType(Province.SMOLENSK.value, ProvinceType.NONE.value)
        elif iPlayer == Civ.DUTCH.value:
            player(Civ.CASTILE).setProvinceType(
                Province.NETHERLANDS.value, ProvinceType.NONE.value
            )
            player(Civ.CASTILE).setProvinceType(Province.FLANDERS.value, ProvinceType.NONE.value)
            player(Civ.AUSTRIA).setProvinceType(
                Province.NETHERLANDS.value, ProvinceType.NONE.value
            )
            player(Civ.AUSTRIA).setProvinceType(Province.FLANDERS.value, ProvinceType.NONE.value)

        utils.refreshStabilityOverlay()
