from CvPythonExtensions import *
from CoreData import civilization, civilizations
from CoreStructures import player
import RFCEMaps
import RFCUtils  # Absinthe
import PyHelpers  # Absinthe

from TimelineData import DateTurn
from CoreTypes import Civ, Province, Scenario, ProvinceTypes

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
        # Norse provinces switch back to unstable after the fall of the Norman Kingdom of Sicily
        if iGameTurn == DateTurn.i1194AD + 1:
            player(Civ.NORWAY).setProvinceType(Province.APULIA.value, ProvinceTypes.NONE.value)
            player(Civ.NORWAY).setProvinceType(Province.CALABRIA.value, ProvinceTypes.NONE.value)
            player(Civ.NORWAY).setProvinceType(Province.SICILY.value, ProvinceTypes.NONE.value)
            player(Civ.NORWAY).setProvinceType(Province.MALTA.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.APULIA.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.CALABRIA.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.SICILY.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.MALTA.value, ProvinceTypes.NONE.value)
        # Prussia direction change
        elif iGameTurn == DateTurn.i1618AD:
            player(Civ.PRUSSIA).setProvinceType(Province.ESTONIA.value, ProvinceTypes.NONE.value)
            player(Civ.PRUSSIA).setProvinceType(Province.LITHUANIA.value, ProvinceTypes.NONE.value)
            player(Civ.PRUSSIA).setProvinceType(Province.SUVALKIJA.value, ProvinceTypes.NONE.value)
            player(Civ.PRUSSIA).setProvinceType(Province.LIVONIA.value, ProvinceTypes.OUTER.value)
            player(Civ.PRUSSIA).setProvinceType(
                Province.POMERANIA.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.PRUSSIA).setProvinceType(
                Province.BRANDENBURG.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.PRUSSIA).setProvinceType(
                Province.SILESIA.value, ProvinceTypes.POTENTIAL.value
            )
            player(Civ.PRUSSIA).setProvinceType(
                Province.GREATER_POLAND.value, ProvinceTypes.OUTER.value
            )

    def onCityBuilt(self, iPlayer, x, y):
        if iPlayer not in civilizations().main().ids():
            return
        pPlayer = gc.getPlayer(iPlayer)
        iProv = RFCEMaps.tProvinceMap[y][x]
        if pPlayer.getProvinceType(iProv) == ProvinceTypes.POTENTIAL.value:
            pPlayer.setProvinceType(iProv, ProvinceTypes.NATURAL.value)
            utils.refreshStabilityOverlay()

    def onCityAcquired(self, owner, iPlayer, city, bConquest, bTrade):
        if iPlayer not in civilizations().main().ids():
            return
        pPlayer = gc.getPlayer(iPlayer)
        iProv = city.getProvince()
        if pPlayer.getProvinceType(iProv) == ProvinceTypes.POTENTIAL.value:
            pPlayer.setProvinceType(iProv, ProvinceTypes.NATURAL.value)
            utils.refreshStabilityOverlay()

    def onCityRazed(self, iOwner, iPlayer, city):
        pass

    def updatePotential(self, iPlayer):
        pPlayer = gc.getPlayer(iPlayer)
        for city in utils.getCityList(iPlayer):
            province = city.getProvince()
            if pPlayer.getProvinceType(province) == ProvinceTypes.POTENTIAL:
                pPlayer.setProvinceType(province, ProvinceTypes.NATURAL.value)
        utils.refreshStabilityOverlay()

    def onRespawn(self, iPlayer):
        # Absinthe: reset the original potential provinces, but only if they wasn't changed to something entirely different later on
        pPlayer = gc.getPlayer(iPlayer)
        for iProv in self.tPot2CoreProvinces[iPlayer]:
            if pPlayer.getProvinceType(iProv) == ProvinceTypes.CORE.value:
                pPlayer.setProvinceType(iProv, ProvinceTypes.POTENTIAL.value)
        for iProv in self.tPot2NormProvinces[iPlayer]:
            if pPlayer.getProvinceType(iProv) == ProvinceTypes.NATURAL.value:
                pPlayer.setProvinceType(iProv, ProvinceTypes.POTENTIAL.value)

        # Absinthe: special respawn conditions
        if iPlayer == Civ.CORDOBA.value:
            for iProv in range(len(Province)):
                player(Civ.CORDOBA).setProvinceType(iProv, ProvinceTypes.NONE.value)
            player(Civ.CORDOBA).setProvinceType(Province.IFRIQIYA.value, ProvinceTypes.CORE.value)
            player(Civ.CORDOBA).setProvinceType(
                Province.ALGIERS.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.CORDOBA).setProvinceType(Province.ORAN.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(
                Province.TRIPOLITANIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.CORDOBA).setProvinceType(Province.TETOUAN.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(Province.MOROCCO.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(Province.FEZ.value, ProvinceTypes.OUTER.value)

    def resetProvinces(self, iPlayer):
        # Absinthe: keep in mind that this will reset all to the initial status, so won't take later province changes into account
        civ = civilization(iPlayer)
        for province in Province:
            civ.player.setProvinceType(province.value, ProvinceTypes.NONE.value)

        for type, provinces in civ.location.provinces.items():
            for province in provinces:
                civ.player.setProvinceType(province.value, type.value)

    def onSpawn(self, iPlayer):
        # when a new nations spawns, old nations in the region should lose some of their provinces
        if iPlayer == Civ.ARABIA.value:
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CYRENAICA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.TRIPOLITANIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.IFRIQIYA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.EGYPT.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.ARABIA.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.SYRIA.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.LEBANON.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.JERUSALEM.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ANTIOCHIA.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CILICIA.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CHARSIANON.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.COLONEA.value, ProvinceTypes.NATURAL.value
            )
        elif iPlayer == Civ.BULGARIA.value:
            player(Civ.BYZANTIUM).setProvinceType(Province.SERBIA.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.MOESIA.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.THRACE.value, ProvinceTypes.NATURAL.value
            )
        elif iPlayer == Civ.VENECIA.value:
            player(Civ.BYZANTIUM).setProvinceType(
                Province.DALMATIA.value, ProvinceTypes.NONE.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.BOSNIA.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.SLAVONIA.value, ProvinceTypes.NONE.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.VERONA.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.TUSCANY.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.LOMBARDY.value, ProvinceTypes.NONE.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.LIGURIA.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.CORSICA.value, ProvinceTypes.NONE.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.SARDINIA.value, ProvinceTypes.NONE.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.LATIUM.value, ProvinceTypes.NONE.value)
        elif iPlayer == Civ.BURGUNDY.value:
            # these areas flip to Burgundy, so resetting them to Potential won't cause any issues
            player(Civ.FRANCE).setProvinceType(
                Province.PROVENCE.value, ProvinceTypes.POTENTIAL.value
            )
            player(Civ.FRANCE).setProvinceType(
                Province.BURGUNDY.value, ProvinceTypes.POTENTIAL.value
            )
        elif iPlayer == Civ.GERMANY.value:
            player(Civ.FRANCE).setProvinceType(Province.LORRAINE.value, ProvinceTypes.OUTER.value)
            player(Civ.FRANCE).setProvinceType(Province.BAVARIA.value, ProvinceTypes.NONE.value)
            player(Civ.FRANCE).setProvinceType(Province.FRANCONIA.value, ProvinceTypes.NONE.value)
            player(Civ.FRANCE).setProvinceType(Province.SAXONY.value, ProvinceTypes.NONE.value)
            player(Civ.FRANCE).setProvinceType(
                Province.NETHERLANDS.value, ProvinceTypes.NONE.value
            )
        elif iPlayer == Civ.HUNGARY.value:
            player(Civ.BULGARIA).setProvinceType(Province.BANAT.value, ProvinceTypes.NONE.value)
            player(Civ.BULGARIA).setProvinceType(
                Province.WALLACHIA.value, ProvinceTypes.OUTER.value
            )
        elif iPlayer == Civ.CASTILE.value:
            player(Civ.CORDOBA).setProvinceType(
                Province.LA_MANCHA.value, ProvinceTypes.NATURAL.value
            )
        elif iPlayer == Civ.MOROCCO.value:
            player(Civ.CORDOBA).setProvinceType(Province.MOROCCO.value, ProvinceTypes.NONE.value)
            player(Civ.CORDOBA).setProvinceType(Province.MARRAKESH.value, ProvinceTypes.NONE.value)
            player(Civ.CORDOBA).setProvinceType(Province.FEZ.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(Province.TETOUAN.value, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.ENGLAND.value:
            player(Civ.FRANCE).setProvinceType(
                Province.NORMANDY.value, ProvinceTypes.POTENTIAL.value
            )  # it flips to England, so resetting them to Potential won't cause any issues
            player(Civ.SCOTLAND).setProvinceType(
                Province.NORTHUMBRIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.SCOTLAND).setProvinceType(Province.MERCIA.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(
                Province.NORTHUMBRIA.value, ProvinceTypes.NONE.value
            )
            player(Civ.DENMARK).setProvinceType(Province.MERCIA.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(
                Province.EAST_ANGLIA.value, ProvinceTypes.NONE.value
            )
            player(Civ.DENMARK).setProvinceType(Province.LONDON.value, ProvinceTypes.NONE.value)
        elif iPlayer == Civ.ARAGON.value:
            player(Civ.BYZANTIUM).setProvinceType(Province.APULIA.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CALABRIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.SICILY.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(Province.MALTA.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(Province.ARAGON.value, ProvinceTypes.OUTER.value)
            player(Civ.CORDOBA).setProvinceType(
                Province.CATALONIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.CORDOBA).setProvinceType(
                Province.VALENCIA.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.CORDOBA).setProvinceType(Province.BALEARS.value, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.SWEDEN.value:
            player(Civ.NORWAY).setProvinceType(Province.SVEALAND.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.GOTALAND.value, ProvinceTypes.NONE.value)
            player(Civ.DENMARK).setProvinceType(Province.SVEALAND.value, ProvinceTypes.NONE.value)
            player(Civ.NOVGOROD).setProvinceType(
                Province.OSTERLAND.value, ProvinceTypes.OUTER.value
            )
        elif iPlayer == Civ.AUSTRIA.value:
            player(Civ.HUNGARY).setProvinceType(
                Province.CARINTHIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.HUNGARY).setProvinceType(Province.AUSTRIA.value, ProvinceTypes.OUTER.value)
            player(Civ.HUNGARY).setProvinceType(Province.MORAVIA.value, ProvinceTypes.OUTER.value)
            player(Civ.HUNGARY).setProvinceType(Province.BAVARIA.value, ProvinceTypes.NONE.value)
            player(Civ.GERMANY).setProvinceType(Province.BAVARIA.value, ProvinceTypes.OUTER.value)
            player(Civ.GERMANY).setProvinceType(Province.BOHEMIA.value, ProvinceTypes.OUTER.value)
            player(Civ.CASTILE).setProvinceType(
                Province.NETHERLANDS.value, ProvinceTypes.OUTER.value
            )
            player(Civ.CASTILE).setProvinceType(Province.FLANDERS.value, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.OTTOMAN.value:
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ANTIOCHIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CILICIA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.CHARSIANON.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.COLONEA.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ARMENIAKON.value, ProvinceTypes.OUTER.value
            )
            player(Civ.BYZANTIUM).setProvinceType(Province.CYPRUS.value, ProvinceTypes.OUTER.value)
            player(Civ.BYZANTIUM).setProvinceType(
                Province.ANATOLIKON.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.OPSIKION.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.THRAKESION.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.BYZANTIUM).setProvinceType(
                Province.PAPHLAGONIA.value, ProvinceTypes.NATURAL.value
            )
            player(Civ.HUNGARY).setProvinceType(Province.DALMATIA.value, ProvinceTypes.OUTER.value)
            player(Civ.HUNGARY).setProvinceType(Province.BOSNIA.value, ProvinceTypes.OUTER.value)
            player(Civ.HUNGARY).setProvinceType(Province.BANAT.value, ProvinceTypes.OUTER.value)
        elif iPlayer == Civ.MOSCOW.value:
            player(Civ.NOVGOROD).setProvinceType(Province.ROSTOV.value, ProvinceTypes.OUTER.value)
            player(Civ.NOVGOROD).setProvinceType(Province.SMOLENSK.value, ProvinceTypes.NONE.value)
        elif iPlayer == Civ.DUTCH.value:
            player(Civ.CASTILE).setProvinceType(
                Province.NETHERLANDS.value, ProvinceTypes.NONE.value
            )
            player(Civ.CASTILE).setProvinceType(Province.FLANDERS.value, ProvinceTypes.NONE.value)
            player(Civ.AUSTRIA).setProvinceType(
                Province.NETHERLANDS.value, ProvinceTypes.NONE.value
            )
            player(Civ.AUSTRIA).setProvinceType(Province.FLANDERS.value, ProvinceTypes.NONE.value)

        utils.refreshStabilityOverlay()
