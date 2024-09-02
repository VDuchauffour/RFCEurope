import random
from CvPythonExtensions import *
from Core import (
    city,
    civilization,
    civilizations,
    human,
    message,
    message_if_human,
    player,
    text,
    year,
    cities,
)
from CoreTypes import (
    Building,
    Civ,
    Improvement,
    Project,
    Promotion,
    Specialist,
    StabilityCategory,
    Unit,
    Wonder,
)
from PyUtils import choice, percentage_chance, rand
from RFCUtils import getBaseUnit, getUniqueBuilding, getUniqueUnit
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
            for city in cities.owner(iPlayer).entities():
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


@handler("combatResult")
def gediminas_tower_effect(pWinner, pLoser):
    # Absinthe: Gediminas Tower wonder effect: extra city defence on unit win in the city
    pPlayer = gc.getPlayer(pWinner.getOwner())
    if pPlayer.countNumBuildings(Wonder.GEDIMINAS_TOWER) > 0:
        pPlot = pWinner.plot()
        if pPlot.isCity():
            pCity = pPlot.getPlotCity()
            if pCity.getNumActiveBuilding(Wonder.GEDIMINAS_TOWER):
                pCity.changeDefenseDamage(-10)


@handler("improvementBuilt")
def stephansdom_effect(iImprovement, iX, iY):
    if iImprovement == Improvement.COTTAGE:
        pPlot = CyMap().plot(iX, iY)
        iOwner = pPlot.getOwner()
        # if there is an owner
        if iOwner >= 0:
            pOwner = gc.getPlayer(iOwner)
            if pOwner.countNumBuildings(Wonder.STEPHANSDOM) > 0:
                pPlot.setImprovementType(Improvement.HAMLET)


@handler("buildingBuilt")
def leaning_tower_effect(city, building_type):
    if building_type == Wonder.LEANING_TOWER:
        iX = city.getX()
        iY = city.getY()
        iUnit = Unit.GREAT_PROPHET + rand(7)
        player(city).initUnit(
            iUnit,
            iX,
            iY,
            UnitAITypes(gc.getUnitInfo(iUnit).getDefaultUnitAIType()),
            DirectionTypes.NO_DIRECTION,
        )
        if player().isExisting():
            szText = (
                text("TXT_KEY_BUILDING_LEANING_TOWER_EFFECT")
                + " "
                + gc.getUnitInfo(iUnit).getDescription()
            )
            message(
                human(),
                szText,
                event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                color=MessageData.LIGHT_BLUE,
            )


def leaning_tower_effect_1200AD():
    iGP = rand(7)
    pFlorentia = city(54, 32)
    iSpecialist = Specialist.GREAT_PROPHET + iGP
    pFlorentia.setFreeSpecialistCount(iSpecialist, 1)


@handler("buildingBuilt")
def bibliothecas_corviniana_effect(city, building_type):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if building_type == Wonder.BIBLIOTHECA_CORVINIANA:
        # techs known by the owner civ
        iTeam = pPlayer.getTeam()
        pTeam = gc.getTeam(iTeam)
        lBuilderKnownTechs = []
        for iTech in xrange(gc.getNumTechInfos()):  # type: ignore
            if pTeam.isHasTech(iTech):
                lBuilderKnownTechs.append(iTech)

        # techs known by the other civs
        lOthersKnownTechs = []
        for iLoopPlayer in civilizations().majors().ids():
            pLoopPlayer = gc.getPlayer(iLoopPlayer)
            iLoopTeam = pLoopPlayer.getTeam()
            pLoopTeam = gc.getTeam(iLoopTeam)
            # only for known civs
            if iLoopPlayer != iPlayer and pTeam.isHasMet(iLoopTeam):
                for iTech in xrange(gc.getNumTechInfos()):  # type: ignore
                    if pLoopTeam.isHasTech(iTech):
                        lOthersKnownTechs.append(iTech)

        # collecting the not known techs which are available for at least one other civ
        # note that we can have the same tech multiple times
        lPotentialTechs = []
        for iTech in lOthersKnownTechs:
            if iTech not in lBuilderKnownTechs:
                lPotentialTechs.append(iTech)

        if len(lPotentialTechs) > 0:
            # converting to a set (and then back to a list), as sets only keep unique elements
            lUniquePotentialTechs = list(set(lPotentialTechs))

            # randomizing the order of the techs
            random.shuffle(lPotentialTechs)

            # adding the techs, with message for the human player
            if len(lUniquePotentialTechs) == 1:
                # add the first instance of the single tech, with message for the human player
                iChosenTech = lPotentialTechs[0]
                pTeam.setHasTech(iChosenTech, True, iPlayer, False, True)
                if iPlayer == human():
                    sText = text(
                        "TXT_KEY_BUILDING_BIBLIOTHECA_CORVINIANA_EFFECT",
                        gc.getTechInfo(iChosenTech).getDescription(),
                    )
                    message(iPlayer, sText, force=True, color=MessageData.LIGHT_BLUE)
            elif len(lUniquePotentialTechs) > 1:
                # add two different random techs, with message for the human player
                for tech in random.sample(lPotentialTechs, 2):
                    pTeam.setHasTech(tech, True, iPlayer, False, True)
                    if iPlayer == human():
                        sText = text(
                            "TXT_KEY_BUILDING_BIBLIOTHECA_CORVINIANA_EFFECT",
                            gc.getTechInfo(tech).getDescription(),
                        )
                        message(iPlayer, sText, force=True, color=MessageData.LIGHT_BLUE)


@handler("buildingBuilt")
def kalmar_castle_effect(city, building_type):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if building_type == Wonder.KALMAR_CASTLE:
        for neighbour in civilization(iPlayer).location.neighbours:
            iNeighbour = neighbour
            pNeighbour = gc.getPlayer(iNeighbour)
            if pNeighbour.isAlive() and iPlayer != iNeighbour:
                pPlayer.AI_changeAttitudeExtra(iNeighbour, 3)
                pNeighbour.AI_changeAttitudeExtra(iPlayer, 3)


@handler("buildingBuilt")
def grand_arsenal_effect(city, building_type):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if building_type == Wonder.GRAND_ARSENAL:
        iX = city.getX()
        iY = city.getY()
        for _ in range(3):
            # should we have Galleass for all civs, or use the getUniqueUnit function in RFCUtils?
            pNewUnit = pPlayer.initUnit(
                Unit.VENICE_GALLEAS,
                iX,
                iY,
                UnitAITypes(gc.getUnitInfo(Unit.VENICE_GALLEAS).getDefaultUnitAIType()),
                DirectionTypes.DIRECTION_SOUTH,
            )
            pNewUnit.setExperience(6, -1)
            for iPromo in [
                Promotion.COMBAT,
                Promotion.LEADERSHIP,
                Promotion.NAVIGATION,
            ]:
                pNewUnit.setHasPromotion(iPromo, True)


@handler("buildingBuilt")
def magellan_voyage_effect(city, building_type):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if building_type == Wonder.MAGELLANS_VOYAGE:
        iTeam = pPlayer.getTeam()
        pTeam = gc.getTeam(iTeam)
        pTeam.changeExtraMoves(gc.getInfoTypeForString("DOMAIN_SEA"), 2)


@handler("buildingBuilt")
def st_catherine_monastery_effect(city, building_type):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if building_type == Wonder.ST_CATHERINE_MONASTERY:
        iX = city.getX()
        iY = city.getY()
        for i in range(2):
            pPlayer.initUnit(
                Unit.HOLY_RELIC,
                iX,
                iY,
                UnitAITypes.NO_UNITAI,
                DirectionTypes.DIRECTION_SOUTH,
            )
        message_if_human(
            iPlayer,
            text("TXT_KEY_BUILDING_SAINT_CATHERINE_MONASTERY_EFFECT"),
            color=MessageData.LIGHT_BLUE,
        )


@handler("buildingBuilt")
def al_azhar_university_effect_on_building_built(city, building_type):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if building_type == Wonder.ALAZHAR:
        iTeam = pPlayer.getTeam()
        pTeam = gc.getTeam(iTeam)
        for iTech in xrange(gc.getNumTechInfos()):
            if gc.getTechInfo(iTech).getAdvisorType() == gc.getInfoTypeForString(
                "ADVISOR_RELIGION"
            ) and not pTeam.isHasTech(iTech):
                research_cost = pTeam.getResearchCost(iTech)
                pTeam.changeResearchProgress(
                    iTech,
                    min(research_cost - pTeam.getResearchProgress(iTech), research_cost / 2),
                    iPlayer,
                )


@handler("cityAcquired")
def al_azhar_university_effect_on_city_acquired(
    iPreviousOwner, iNewOwner, pCity, bConquest, bTrade
):
    pPreviousOwner = gc.getPlayer(iPreviousOwner)
    pNewOwner = gc.getPlayer(iNewOwner)
    if pCity.getNumActiveBuilding(Wonder.ALAZHAR):
        iPreviousTeam = pPreviousOwner.getTeam()
        pPreviousTeam = gc.getTeam(iPreviousTeam)
        iNewTeam = pNewOwner.getTeam()
        pNewTeam = gc.getTeam(iNewTeam)
        for iTech in xrange(gc.getNumTechInfos()):
            if gc.getTechInfo(iTech).getAdvisorType() == gc.getInfoTypeForString(
                "ADVISOR_RELIGION"
            ):
                if not pPreviousTeam.isHasTech(iTech):
                    research_cost = pPreviousTeam.getResearchCost(iTech)
                    pPreviousTeam.changeResearchProgress(
                        iTech,
                        max(-pPreviousTeam.getResearchProgress(iTech), -research_cost / 5),
                        iPreviousOwner,
                    )
                if not pNewTeam.isHasTech(iTech):
                    research_cost = pNewTeam.getResearchCost(iTech)
                    pNewTeam.changeResearchProgress(
                        iTech,
                        min(
                            research_cost - pNewTeam.getResearchProgress(iTech),
                            research_cost / 5,
                        ),
                        iNewOwner,
                    )


@handler("cityRazed")
def remove_al_azhar_university_effect_on_city_razed(city, iPlayer):
    if city.getNumActiveBuilding(Wonder.ALAZHAR):
        pPlayer = gc.getPlayer(iPlayer)
        iTeam = pPlayer.getTeam()
        pTeam = gc.getTeam(iTeam)
        for iTech in xrange(gc.getNumTechInfos()):
            if not pTeam.isHasTech(iTech):
                if gc.getTechInfo(iTech).getAdvisorType() == gc.getInfoTypeForString(
                    "ADVISOR_RELIGION"
                ):
                    pTeam.changeResearchProgress(
                        iTech,
                        max(
                            -pPreviousTeam.getResearchProgress(iTech),  # type: ignore
                            -pTeam.getResearchCost(iTech) / 5,
                        ),
                        iPlayer,
                    )


@handler("buildingBuilt")
def sistine_chapel_effect(city, building_type):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if building_type == Wonder.SISTINE_CHAPEL:
        for city in cities.owner(iPlayer).entities():
            if city.getNumWorldWonders() > 0:
                city.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_ARTIST"), 1)
    elif isWorldWonderClass(gc.getBuildingInfo(building_type).getBuildingClassType()):
        # if the given civ already had the Sistine Chapel, and built another wonder in a new city
        if pPlayer.countNumBuildings(Wonder.SISTINE_CHAPEL) > 0:
            if city.getNumWorldWonders() == 1:
                city.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_ARTIST"), 1)


@handler("cityAcquired")
def sistine_chapel_effect_on_city_acquired(iPreviousOwner, iNewOwner, pCity, bConquest, bTrade):
    pPreviousOwner = gc.getPlayer(iPreviousOwner)
    pNewOwner = gc.getPlayer(iNewOwner)
    if pCity.getNumActiveBuilding(Wonder.SISTINE_CHAPEL):
        for loopCity in cities.owner(iPreviousOwner).entities():
            if loopCity.getNumWorldWonders() > 0:
                loopCity.changeFreeSpecialistCount(
                    gc.getInfoTypeForString("SPECIALIST_ARTIST"), -1
                )
        for loopCity in cities.owner(iNewOwner).entities():
            if loopCity.getNumWorldWonders() > 0 and not loopCity.getNumActiveBuilding(
                Wonder.SISTINE_CHAPEL
            ):
                loopCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_ARTIST"), 1)
    elif pCity.getNumWorldWonders() > 0:
        if pPreviousOwner.countNumBuildings(Wonder.SISTINE_CHAPEL) > 0:
            pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_ARTIST"), -1)
        elif pNewOwner.countNumBuildings(Wonder.SISTINE_CHAPEL) > 0:
            pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_ARTIST"), 1)


@handler("cityRazed")
def remove_sistine_chapel_effect_on_city_razed(city, iPlayer):
    if city.getNumActiveBuilding(Wonder.SISTINE_CHAPEL):
        for loopCity in cities.owner(iPlayer).entities():
            if loopCity.getNumWorldWonders() > 0:
                loopCity.changeFreeSpecialistCount(
                    gc.getInfoTypeForString("SPECIALIST_ARTIST"), -1
                )


@handler("buildingBuilt")
def jasna_gora_effect_on_building_built(city, building_type):
    iPlayer = city.getOwner()
    if building_type == Wonder.JASNA_GORA:
        for city in cities.owner(iPlayer).entities():
            jasna_gora_effect(city)


@handler("cityBuilt")
def jasna_gora_effect_on_city_built(city):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if pPlayer.countNumBuildings(Wonder.JASNA_GORA) > 0:
        jasna_gora_effect(city)


@handler("cityAcquired")
def jasna_gora_effect_on_city_acquired(iPreviousOwner, iNewOwner, pCity, bConquest, bTrade):
    pPreviousOwner = gc.getPlayer(iPreviousOwner)
    pNewOwner = gc.getPlayer(iNewOwner)

    if pCity.getNumActiveBuilding(Wonder.JASNA_GORA):
        for city in cities.owner(iPreviousOwner).entities():
            remove_jasna_gora_effect(city)
        for city in cities.owner(iNewOwner).entities():
            jasna_gora_effect(city)
    elif pPreviousOwner.countNumBuildings(Wonder.JASNA_GORA) > 0:
        remove_jasna_gora_effect(pCity)
    elif pNewOwner.countNumBuildings(Wonder.JASNA_GORA) > 0:
        jasna_gora_effect(pCity)


@handler("cityRazed")
def remove_jasna_gora_effect_on_city_razed(city, iPlayer):
    if city.getNumActiveBuilding(Wonder.JASNA_GORA):
        for city in cities.owner(iPlayer).entities():
            remove_jasna_gora_effect(city)


def jasna_gora_effect(city):
    _jasna_gora_effect(city, True)


def remove_jasna_gora_effect(city):
    _jasna_gora_effect(city, False)


def _jasna_gora_effect(city, apply):
    if apply:
        value = 1
    else:
        value = 0
    for building_class in [
        "BUILDINGCLASS_CATHOLIC_TEMPLE",
        "BUILDINGCLASS_ORTHODOX_TEMPLE",
        "BUILDINGCLASS_PROTESTANT_TEMPLE",
        "BUILDINGCLASS_ISLAMIC_TEMPLE",
    ]:
        city.setBuildingCommerceChange(
            gc.getInfoTypeForString(building_class),
            CommerceTypes.COMMERCE_CULTURE,
            value,
        )


@handler("buildingBuilt")
def kizil_kule_effect_on_building_built(city, building_type):
    iPlayer = city.getOwner()
    if building_type == Wonder.KIZIL_KULE:
        for city in cities.owner(iPlayer).entities():
            kizil_kule_effect(city)


@handler("cityBuilt")
def kizil_kule_effect_on_city_built(city):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if pPlayer.countNumBuildings(Wonder.KIZIL_KULE) > 0:
        kizil_kule_effect(city)


@handler("cityAcquired")
def kizil_kule_effect_on_city_acquired(iPreviousOwner, iNewOwner, pCity, bConquest, bTrade):
    pPreviousOwner = gc.getPlayer(iPreviousOwner)
    pNewOwner = gc.getPlayer(iNewOwner)
    if pCity.getNumActiveBuilding(Wonder.KIZIL_KULE):
        for _city in cities.owner(iPreviousOwner).entities():
            remove_kizil_kule_effect(_city)
        for _city in cities.owner(iNewOwner).entities():
            kizil_kule_effect(_city)
    elif pPreviousOwner.countNumBuildings(Wonder.KIZIL_KULE) > 0:
        remove_kizil_kule_effect(pCity)
    elif pNewOwner.countNumBuildings(Wonder.KIZIL_KULE) > 0:
        kizil_kule_effect(pCity)


@handler("cityRazed")
def remove_kizil_kule_effect_on_city_razed(city, iPlayer):
    if city.getNumActiveBuilding(Wonder.KIZIL_KULE):
        for _city in cities.owner(iPlayer).entities():
            remove_kizil_kule_effect(_city)


def kizil_kule_effect(city):
    _kizil_kule_effect(city, 2)


def remove_kizil_kule_effect(city):
    _kizil_kule_effect(city, 0)


def _kizil_kule_effect(city, value):
    city.setBuildingYieldChange(
        gc.getInfoTypeForString("BUILDINGCLASS_HARBOR"), YieldTypes.YIELD_COMMERCE, value
    )


@handler("buildingBuilt")
def samogitian_alkas_effect_on_building_built(city, building_type):
    iPlayer = city.getOwner()
    if building_type == Wonder.SAMOGITIAN_ALKAS:
        for city in cities.owner(iPlayer).entities():
            samogitian_alkas_effect(city)


@handler("cityBuilt")
def samogitian_alkas_effect_on_city_built(city):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if pPlayer.countNumBuildings(Wonder.SAMOGITIAN_ALKAS) > 0:
        samogitian_alkas_effect(city)


@handler("cityAcquired")
def samogitian_alkas_effect_on_city_acquired(iPreviousOwner, iNewOwner, pCity, bConquest, bTrade):
    pPreviousOwner = gc.getPlayer(iPreviousOwner)
    pNewOwner = gc.getPlayer(iNewOwner)
    if pCity.getNumActiveBuilding(Wonder.SAMOGITIAN_ALKAS):
        for _city in cities.owner(iPreviousOwner).entities():
            remove_samogitian_alkas_effect(_city)
        for _city in cities.owner(iNewOwner).entities():
            samogitian_alkas_effect(_city)
    elif pPreviousOwner.countNumBuildings(Wonder.SAMOGITIAN_ALKAS) > 0:
        remove_samogitian_alkas_effect(pCity)
    elif pNewOwner.countNumBuildings(Wonder.SAMOGITIAN_ALKAS) > 0:
        samogitian_alkas_effect(pCity)


@handler("cityRazed")
def remove_samogitian_alkas_effect_on_city_razed(city, iPlayer):
    if city.getNumActiveBuilding(Wonder.SAMOGITIAN_ALKAS):
        for _city in cities.owner(iPlayer).entities():
            remove_samogitian_alkas_effect(_city)


def samogitian_alkas_effect(city):
    _samogitian_alkas_effect(city, 2)


def remove_samogitian_alkas_effect(city):
    _samogitian_alkas_effect(city, 0)


def _samogitian_alkas_effect(city, value):
    city.setBuildingCommerceChange(
        gc.getInfoTypeForString("BUILDINGCLASS_PAGAN_SHRINE"),
        CommerceTypes.COMMERCE_RESEARCH,
        value,
    )


@handler("buildingBuilt")
def magna_carta_effect_on_building_built(city, building_type):
    iPlayer = city.getOwner()
    if building_type == Wonder.MAGNA_CARTA:
        for city in cities.owner(iPlayer).entities():
            magna_carta_effect(city)


@handler("cityBuilt")
def magna_carta_effect_on_city_built(city):
    iPlayer = city.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if pPlayer.countNumBuildings(Wonder.MAGNA_CARTA) > 0:
        magna_carta_effect(city)


@handler("cityAcquired")
def magna_carta_effect_on_city_acquired(iPreviousOwner, iNewOwner, pCity, bConquest, bTrade):
    pPreviousOwner = gc.getPlayer(iPreviousOwner)
    pNewOwner = gc.getPlayer(iNewOwner)
    if pCity.getNumActiveBuilding(Wonder.MAGNA_CARTA):
        for _city in cities.owner(iPreviousOwner).entities():
            remove_magna_carta_effect(_city)
        for _city in cities.owner(iNewOwner).entities():
            magna_carta_effect(_city)
    elif pPreviousOwner.countNumBuildings(Wonder.MAGNA_CARTA) > 0:
        remove_magna_carta_effect(pCity)
    elif pNewOwner.countNumBuildings(Wonder.MAGNA_CARTA) > 0:
        magna_carta_effect(pCity)


@handler("cityRazed")
def remove_magna_carta_effect_on_city_razed(city, iPlayer):
    if city.getNumActiveBuilding(Wonder.MAGNA_CARTA):
        for _city in cities.owner(iPlayer).entities():
            remove_magna_carta_effect(_city)


def magna_carta_effect(city):
    _magna_carta_effect(city, 2)


def remove_magna_carta_effect(city):
    _magna_carta_effect(city, 0)


def _magna_carta_effect(city, value):
    city.setBuildingCommerceChange(
        gc.getInfoTypeForString("BUILDINGCLASS_COURTHOUSE"),
        CommerceTypes.COMMERCE_CULTURE,
        value,
    )


@handler("projectBuilt")
def onProjectBuilt(pCity, iProjectType):
    iPlayer = pCity.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if iProjectType >= len(Project):
        if pPlayer.countNumBuildings(Wonder.TORRE_DEL_ORO) > 0:
            # 70% chance for a 3 turn Golden Age
            if percentage_chance(70, strict=True):
                pPlayer.changeGoldenAgeTurns(3)
                message_if_human(
                    iPlayer,
                    text("TXT_KEY_PROJECT_COLONY_GOLDEN_AGE"),
                    color=MessageData.GREEN,
                )


@handler("unitBuilt")
def topkapi_palace_effect(city, unit):
    iPlayer = unit.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    iUnitType = unit.getUnitType()
    iTeam = pPlayer.getTeam()
    pTeam = gc.getTeam(iTeam)

    if pTeam.isTrainVassalUU():
        l_vassalUU = []
        iDefaultUnit = getBaseUnit(iUnitType)
        for iLoopPlayer in civilizations().majors().ids():
            pLoopPlayer = gc.getPlayer(iLoopPlayer)
            if pLoopPlayer.isAlive():
                if gc.getTeam(pLoopPlayer.getTeam()).isVassal(iTeam):
                    iUniqueUnit = getUniqueUnit(iLoopPlayer, iUnitType)
                    if iUniqueUnit != iDefaultUnit:
                        l_vassalUU.append(iUniqueUnit)
        if l_vassalUU:  # Only convert if vassal UU is possible
            iPlayerUU = getUniqueUnit(iPlayer, iUnitType)
            if iPlayerUU != iDefaultUnit:
                # double chance for the original UU
                l_vassalUU.append(iPlayerUU)
                l_vassalUU.append(iPlayerUU)
            iUnit = choice(l_vassalUU)
            pNewUnit = pPlayer.initUnit(
                iUnit,
                unit.getX(),
                unit.getY(),
                UnitAITypes.NO_UNITAI,
                DirectionTypes.NO_DIRECTION,
            )
            pNewUnit.convert(unit)
            # message if it was changed to a vassal UU
            if iUnit != iPlayerUU and iUnit != iDefaultUnit:
                if human() == iPlayer:
                    szText = text(
                        "TXT_KEY_BUILDING_TOPKAPI_PALACE_EFFECT",
                        gc.getUnitInfo(iUnit).getDescription(),
                        gc.getUnitInfo(iPlayerUU).getDescription(),
                    )
                    message(
                        human(),
                        szText,
                        event=InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                        button=gc.getUnitInfo(iUnit).getButton(),
                        color=MessageData.LIGHT_BLUE,
                        location=city,
                    )


@handler("unitBuilt")
def brandenburg_gate_effect(city, unit):
    iPlayer = unit.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if unit.getUnitCombatType() != -1:
        if pPlayer.countNumBuildings(Wonder.BRANDENBURG_GATE) > 0:
            unit.changeExperience(
                (
                    2
                    * city.getAddedFreeSpecialistCount(
                        gc.getInfoTypeForString("SPECIALIST_GREAT_GENERAL")
                    )
                ),
                999,
                False,
                False,
                False,
            )


@handler("unitBuilt")
def selimiye_mosque_effect(city, unit):
    iPlayer = unit.getOwner()
    pPlayer = gc.getPlayer(iPlayer)
    if pPlayer.countNumBuildings(Wonder.SELIMIYE_MOSQUE) > 0:
        if pPlayer.isGoldenAge():
            unit.changeExperience(unit.getExperience(), 999, False, False, False)


@handler("greatPersonBorn")
def louvre_effect(pUnit, iPlayer, pCity):
    pPlayer = gc.getPlayer(iPlayer)
    if pPlayer.countNumBuildings(Wonder.LOUVRE) > 0:
        for loopCity in cities.owner(iPlayer).entities():
            # bigger boost for the GP city and the Louvre city
            if loopCity.getNumActiveBuilding(Wonder.LOUVRE) or pCity == loopCity:
                loopCity.changeCulture(iPlayer, min(300, loopCity.getCultureThreshold() / 5), True)
            else:
                loopCity.changeCulture(
                    iPlayer, min(100, loopCity.getCultureThreshold() / 10), True
                )


@handler("greatPersonBorn")
def peterhof_palace_effect(pUnit, iPlayer, pCity):
    pPlayer = gc.getPlayer(iPlayer)
    if pPlayer.countNumBuildings(Wonder.PETERHOF_PALACE) > 0:
        if percentage_chance(70, strict=True):
            if pUnit.getUnitType() == Unit.GREAT_SCIENTIST:
                pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SCIENTIST"), 1)
            elif pUnit.getUnitType() == Unit.GREAT_PROPHET:
                pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_PRIEST"), 1)
            elif pUnit.getUnitType() == Unit.GREAT_ARTIST:
                pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_ARTIST"), 1)
            elif pUnit.getUnitType() == Unit.GREAT_MERCHANT:
                pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_MERCHANT"), 1)
            elif pUnit.getUnitType() == Unit.GREAT_ENGINEER:
                pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_ENGINEER"), 1)
            elif pUnit.getUnitType() == Unit.GREAT_SPY:
                pCity.changeFreeSpecialistCount(gc.getInfoTypeForString("SPECIALIST_SPY"), 1)


@handler("vassalState")
def onVassalState(iMaster, iVassal, bVassal):
    if bVassal:
        MasterTeam = gc.getTeam(iMaster)
        for iPlayer in civilizations().majors().ids():
            pPlayer = gc.getPlayer(iPlayer)
            if (
                pPlayer.getTeam() == iMaster
                and pPlayer.countNumBuildings(Wonder.IMPERIAL_DIET) > 0
            ):
                pPlayer.changeGoldenAgeTurns(3)
                message_if_human(
                    iPlayer,
                    text("TXT_KEY_BUILDING_IMPERIAL_DIET_EFFECT"),
                    color=MessageData.LIGHT_BLUE,
                )
