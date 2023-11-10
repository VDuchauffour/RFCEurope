from CvPythonExtensions import *
from CoreData import civilizations, civilization
from CoreTypes import (
    Building,
    City,
    Civ,
    Civic,
    Colony,
    Feature,
    ModifierCategory,
    PlagueType,
    Promotion,
    Terrain,
    ProvinceType,
    Religion,
    Improvement,
    Project,
    UniquePower,
    Technology,
    Unit,
    FaithPointBonusCategory,
    Wonder,
)
import RFCEMaps
import RFCUtils
from MiscData import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    GREAT_PROPHET_FAITH_POINT_BONUS,
    PROSECUTOR_UNITCLASS,
)
from LocationsData import CITIES
from TimelineData import TIMELINE_TECH_MODIFIER, DateTurn

gc = CyGlobalContext()  # LOQ
utils = RFCUtils.RFCUtils()


class RFCEBalance:
    def setBalanceParameters(self):

        self.preMapsNSizes()
        self.setTechTimeline()  # Timeline for correct tech three
        self.setModifiers()

        ##### Set Initial buildings for the civs
        # gc.setInitialBuilding( iCiv, iBuilding, True\False ), if ( True) give iCiv, building iBuildings else don't Default is False
        # we can change True <-> False with the onTechAquire event

        gc.setInitialBuilding(Civ.VENECIA.value, Building.HARBOR.value, True)
        gc.setInitialBuilding(Civ.VENECIA.value, Building.GRANARY.value, True)

        gc.setInitialBuilding(Civ.CASTILE.value, Building.BARRACKS.value, True)

        gc.setInitialBuilding(Civ.DENMARK.value, Building.BARRACKS.value, True)

        gc.setInitialBuilding(Civ.SCOTLAND.value, Building.BARRACKS.value, True)

        gc.setInitialBuilding(Civ.MOSCOW.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.MOSCOW.value, Building.BARRACKS.value, True)
        gc.setInitialBuilding(Civ.MOSCOW.value, Building.FORGE.value, True)
        gc.setInitialBuilding(Civ.MOSCOW.value, Building.MARKET.value, True)

        gc.setInitialBuilding(Civ.GENOA.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.GENOA.value, Building.BARRACKS.value, True)
        gc.setInitialBuilding(Civ.GENOA.value, Building.HARBOR.value, True)

        gc.setInitialBuilding(Civ.MOROCCO.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.MOROCCO.value, Building.BARRACKS.value, True)

        gc.setInitialBuilding(Civ.ENGLAND.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.ENGLAND.value, Building.BARRACKS.value, True)

        gc.setInitialBuilding(Civ.PORTUGAL.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.PORTUGAL.value, Building.BARRACKS.value, True)

        gc.setInitialBuilding(Civ.ARAGON.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.ARAGON.value, Building.BARRACKS.value, True)
        gc.setInitialBuilding(Civ.ARAGON.value, Building.HARBOR.value, True)

        gc.setInitialBuilding(Civ.PRUSSIA.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.PRUSSIA.value, Building.BARRACKS.value, True)

        gc.setInitialBuilding(Civ.LITHUANIA.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.LITHUANIA.value, Building.BARRACKS.value, True)

        gc.setInitialBuilding(Civ.AUSTRIA.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.AUSTRIA.value, Building.BARRACKS.value, True)
        gc.setInitialBuilding(Civ.AUSTRIA.value, Building.FORGE.value, True)

        gc.setInitialBuilding(Civ.OTTOMAN.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.OTTOMAN.value, Building.BARRACKS.value, True)
        gc.setInitialBuilding(Civ.OTTOMAN.value, Building.FORGE.value, True)
        gc.setInitialBuilding(Civ.OTTOMAN.value, Building.HARBOR.value, True)

        gc.setInitialBuilding(Civ.SWEDEN.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.SWEDEN.value, Building.BARRACKS.value, True)
        gc.setInitialBuilding(Civ.SWEDEN.value, Building.HARBOR.value, True)

        gc.setInitialBuilding(Civ.DUTCH.value, Building.GRANARY.value, True)
        gc.setInitialBuilding(Civ.DUTCH.value, Building.BARRACKS.value, True)
        gc.setInitialBuilding(Civ.DUTCH.value, Building.FORGE.value, True)
        gc.setInitialBuilding(Civ.DUTCH.value, Building.HARBOR.value, True)
        gc.setInitialBuilding(Civ.DUTCH.value, Building.AQUEDUCT.value, True)
        gc.setInitialBuilding(Civ.DUTCH.value, Building.MARKET.value, True)
        gc.setInitialBuilding(Civ.DUTCH.value, Building.LIGHTHOUSE.value, True)
        gc.setInitialBuilding(Civ.DUTCH.value, Building.THEATRE.value, True)
        gc.setInitialBuilding(Civ.DUTCH.value, Building.SMOKEHOUSE.value, True)

        ####### AI Modifiers
        # 3Miro: setCityClusterAI(iCiv,iTop,iBottom,iMinus) for each AI civilization (set them for all, but only the AI make difference)
        # this determines how clustered the cities would be
        # AI_foundValue in PlayerAI would compute for a candidate city location the number of plots that are taken (i.e. by another city)
        # in CivIV, if more than a third of the tiles are "taken", do not found city there. In RFC, cities are clustered closer
        # if ( iTaken > 21 * iTop / iBottom - iMinus ) do not build city there.
        # RFC default values are 2/3 -1 for Europe, 1/3 - 0 for Russia and 1/2 for Mongolia
        # for example gc.setCityClusterAI( iByzantium, 1, 3, 0 ) wouldn't allow Byzantium to settle cities if more than 7 tiles are taken
        gc.setCityClusterAI(Civ.BYZANTIUM.value, 1, 3, 0)  # won't settle if 8+ tiles are taken
        gc.setCityClusterAI(Civ.FRANCE.value, 1, 3, 0)  # 8
        gc.setCityClusterAI(Civ.ARABIA.value, 1, 3, 1)  # 7
        gc.setCityClusterAI(Civ.BULGARIA.value, 2, 3, 4)  # 11
        gc.setCityClusterAI(Civ.CORDOBA.value, 1, 2, 1)  # 10
        gc.setCityClusterAI(Civ.VENECIA.value, 2, 3, 1)  # 14
        gc.setCityClusterAI(Civ.BURGUNDY.value, 2, 3, 3)  # 12
        gc.setCityClusterAI(Civ.GERMANY.value, 2, 3, 4)  # 11
        gc.setCityClusterAI(Civ.NOVGOROD.value, 1, 3, 2)  # 6
        gc.setCityClusterAI(Civ.NORWAY.value, 1, 2, 1)  # 10
        gc.setCityClusterAI(Civ.KIEV.value, 1, 3, 2)  # 6
        gc.setCityClusterAI(Civ.HUNGARY.value, 2, 3, 3)  # 12
        gc.setCityClusterAI(Civ.CASTILE.value, 1, 2, 1)  # 10
        gc.setCityClusterAI(Civ.DENMARK.value, 2, 3, 3)  # 12
        gc.setCityClusterAI(Civ.SCOTLAND.value, 2, 3, 2)  # 13
        gc.setCityClusterAI(Civ.POLAND.value, 1, 3, 0)  # 8
        gc.setCityClusterAI(Civ.GENOA.value, 2, 3, 1)  # 14
        gc.setCityClusterAI(Civ.MOROCCO.value, 1, 3, 2)  # 6
        gc.setCityClusterAI(Civ.ENGLAND.value, 1, 2, 1)  # 10
        gc.setCityClusterAI(Civ.PORTUGAL.value, 2, 3, 1)  # 14
        gc.setCityClusterAI(Civ.ARAGON.value, 2, 3, 1)  # 14
        gc.setCityClusterAI(Civ.SWEDEN.value, 1, 2, 2)  # 9
        gc.setCityClusterAI(Civ.PRUSSIA.value, 2, 3, 1)  # 14
        gc.setCityClusterAI(Civ.LITHUANIA.value, 1, 3, 0)  # 8
        gc.setCityClusterAI(Civ.AUSTRIA.value, 2, 3, 3)  # 12
        gc.setCityClusterAI(Civ.OTTOMAN.value, 1, 3, 1)  # 7
        gc.setCityClusterAI(Civ.MOSCOW.value, 1, 4, 1)  # 5
        gc.setCityClusterAI(Civ.DUTCH.value, 2, 3, 1)  # 14

        # 3Miro: setCityWarDistanceAI(iCiv,iVal), depending on the type of the empire, modify how likely the AI is to attack a city
        # values are 1 - small empires, 2 - large continuous empires, 3 - not necessarily continuous empires
        gc.setCityWarDistanceAI(Civ.BYZANTIUM.value, 2)
        gc.setCityWarDistanceAI(Civ.FRANCE.value, 2)
        gc.setCityWarDistanceAI(Civ.ARABIA.value, 2)
        gc.setCityWarDistanceAI(Civ.BULGARIA.value, 1)
        gc.setCityWarDistanceAI(Civ.CORDOBA.value, 2)
        gc.setCityWarDistanceAI(Civ.VENECIA.value, 3)
        gc.setCityWarDistanceAI(Civ.BURGUNDY.value, 1)
        gc.setCityWarDistanceAI(Civ.GERMANY.value, 2)
        gc.setCityWarDistanceAI(Civ.NOVGOROD.value, 2)
        gc.setCityWarDistanceAI(Civ.NORWAY.value, 3)
        gc.setCityWarDistanceAI(Civ.KIEV.value, 2)
        gc.setCityWarDistanceAI(Civ.HUNGARY.value, 2)
        gc.setCityWarDistanceAI(Civ.CASTILE.value, 3)
        gc.setCityWarDistanceAI(Civ.DENMARK.value, 2)
        gc.setCityWarDistanceAI(Civ.SCOTLAND.value, 1)
        gc.setCityWarDistanceAI(Civ.POLAND.value, 2)
        gc.setCityWarDistanceAI(Civ.GENOA.value, 3)
        gc.setCityWarDistanceAI(Civ.MOROCCO.value, 2)
        gc.setCityWarDistanceAI(Civ.ENGLAND.value, 3)
        gc.setCityWarDistanceAI(Civ.PORTUGAL.value, 3)
        gc.setCityWarDistanceAI(Civ.ARAGON.value, 3)
        gc.setCityWarDistanceAI(Civ.SWEDEN.value, 3)
        gc.setCityWarDistanceAI(Civ.PRUSSIA.value, 2)
        gc.setCityWarDistanceAI(Civ.LITHUANIA.value, 2)
        gc.setCityWarDistanceAI(Civ.AUSTRIA.value, 2)
        gc.setCityWarDistanceAI(Civ.OTTOMAN.value, 2)
        gc.setCityWarDistanceAI(Civ.MOSCOW.value, 2)
        gc.setCityWarDistanceAI(Civ.DUTCH.value, 1)

        # 3Miro: setTechPreferenceAI(iCiv,iTech,iVal), for each civ, for each tech, specify how likable it is. iVal is same as in growth.
        # low percent makes the tech less desirable
        gc.setTechPreferenceAI(Civ.BULGARIA.value, Technology.BRONZE_CASTING.value, 200)
        gc.setTechPreferenceAI(Civ.GERMANY.value, Technology.PRINTING_PRESS.value, 200)
        gc.setTechPreferenceAI(Civ.ENGLAND.value, Technology.PRINTING_PRESS.value, 150)
        gc.setTechPreferenceAI(
            Civ.POPE.value, Technology.PRINTING_PRESS.value, 10
        )  # Pope shouldn't want this
        gc.setTechPreferenceAI(Civ.CASTILE.value, Technology.ASTRONOMY.value, 200)
        gc.setTechPreferenceAI(Civ.PORTUGAL.value, Technology.ASTRONOMY.value, 200)

        # 3Miro: setDiplomacyModifiers(iCiv1,iCiv2,iVal) hidden modifier for the two civ's AI relations. More likely to have OB and so on.
        # + means they will like each other - they will hate each other.
        # from Civ1 towards Civ2 (make them symmetric)
        gc.setDiplomacyModifiers(Civ.CORDOBA.value, Civ.ARABIA.value, +5)
        gc.setDiplomacyModifiers(Civ.ARABIA.value, Civ.CORDOBA.value, +5)
        gc.setDiplomacyModifiers(Civ.ARABIA.value, Civ.BYZANTIUM.value, -8)
        gc.setDiplomacyModifiers(Civ.BYZANTIUM.value, Civ.ARABIA.value, -8)
        gc.setDiplomacyModifiers(Civ.BULGARIA.value, Civ.BYZANTIUM.value, +3)
        gc.setDiplomacyModifiers(Civ.BYZANTIUM.value, Civ.BULGARIA.value, +3)
        gc.setDiplomacyModifiers(Civ.CORDOBA.value, Civ.CASTILE.value, -14)
        gc.setDiplomacyModifiers(Civ.CASTILE.value, Civ.CORDOBA.value, -14)
        gc.setDiplomacyModifiers(Civ.MOROCCO.value, Civ.CASTILE.value, -10)
        gc.setDiplomacyModifiers(Civ.CASTILE.value, Civ.MOROCCO.value, -10)
        gc.setDiplomacyModifiers(Civ.ARAGON.value, Civ.CASTILE.value, +4)
        gc.setDiplomacyModifiers(Civ.CASTILE.value, Civ.ARAGON.value, +4)
        gc.setDiplomacyModifiers(Civ.PORTUGAL.value, Civ.CASTILE.value, +6)
        gc.setDiplomacyModifiers(Civ.CASTILE.value, Civ.PORTUGAL.value, +6)
        gc.setDiplomacyModifiers(Civ.CORDOBA.value, Civ.PORTUGAL.value, -8)
        gc.setDiplomacyModifiers(Civ.PORTUGAL.value, Civ.CORDOBA.value, -8)
        gc.setDiplomacyModifiers(Civ.KIEV.value, Civ.NOVGOROD.value, +5)
        gc.setDiplomacyModifiers(Civ.NOVGOROD.value, Civ.KIEV.value, +5)
        gc.setDiplomacyModifiers(Civ.MOSCOW.value, Civ.NOVGOROD.value, -8)
        gc.setDiplomacyModifiers(Civ.NOVGOROD.value, Civ.MOSCOW.value, -8)
        gc.setDiplomacyModifiers(Civ.FRANCE.value, Civ.BURGUNDY.value, -2)
        gc.setDiplomacyModifiers(Civ.BURGUNDY.value, Civ.FRANCE.value, -2)
        gc.setDiplomacyModifiers(Civ.OTTOMAN.value, Civ.BYZANTIUM.value, -14)
        gc.setDiplomacyModifiers(Civ.BYZANTIUM.value, Civ.OTTOMAN.value, -14)
        gc.setDiplomacyModifiers(Civ.GERMANY.value, Civ.POLAND.value, -5)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.GERMANY.value, -5)
        gc.setDiplomacyModifiers(Civ.MOSCOW.value, Civ.POLAND.value, -4)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.MOSCOW.value, -4)
        gc.setDiplomacyModifiers(Civ.MOSCOW.value, Civ.LITHUANIA.value, -2)
        gc.setDiplomacyModifiers(Civ.LITHUANIA.value, Civ.MOSCOW.value, -2)
        gc.setDiplomacyModifiers(Civ.AUSTRIA.value, Civ.POLAND.value, -2)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.AUSTRIA.value, -2)
        gc.setDiplomacyModifiers(Civ.LITHUANIA.value, Civ.POLAND.value, +4)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.LITHUANIA.value, +4)
        gc.setDiplomacyModifiers(Civ.HUNGARY.value, Civ.POLAND.value, +3)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.HUNGARY.value, +3)
        gc.setDiplomacyModifiers(Civ.AUSTRIA.value, Civ.HUNGARY.value, -6)
        gc.setDiplomacyModifiers(Civ.HUNGARY.value, Civ.AUSTRIA.value, -6)
        gc.setDiplomacyModifiers(Civ.SWEDEN.value, Civ.POLAND.value, -2)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.SWEDEN.value, -2)
        gc.setDiplomacyModifiers(Civ.SWEDEN.value, Civ.MOSCOW.value, -8)
        gc.setDiplomacyModifiers(Civ.MOSCOW.value, Civ.SWEDEN.value, -8)
        gc.setDiplomacyModifiers(Civ.PRUSSIA.value, Civ.POLAND.value, -6)
        gc.setDiplomacyModifiers(Civ.POLAND.value, Civ.PRUSSIA.value, -6)
        gc.setDiplomacyModifiers(Civ.PRUSSIA.value, Civ.LITHUANIA.value, -8)
        gc.setDiplomacyModifiers(Civ.LITHUANIA.value, Civ.PRUSSIA.value, -8)
        gc.setDiplomacyModifiers(Civ.ENGLAND.value, Civ.SCOTLAND.value, -8)
        gc.setDiplomacyModifiers(Civ.SCOTLAND.value, Civ.ENGLAND.value, -8)
        gc.setDiplomacyModifiers(Civ.FRANCE.value, Civ.SCOTLAND.value, +4)
        gc.setDiplomacyModifiers(Civ.SCOTLAND.value, Civ.FRANCE.value, +4)
        gc.setDiplomacyModifiers(Civ.NORWAY.value, Civ.DENMARK.value, +4)
        gc.setDiplomacyModifiers(Civ.DENMARK.value, Civ.NORWAY.value, +4)
        gc.setDiplomacyModifiers(Civ.SWEDEN.value, Civ.DENMARK.value, -4)
        gc.setDiplomacyModifiers(Civ.DENMARK.value, Civ.SWEDEN.value, -4)

        ####### 3Miro: UNIQUE POWERS
        # 3Miro: setUP(iCiv,iPower) sets the Unique Powers for C++

        # 3Miro: setUP(iCiv,iPower,iParameter)
        # iUP_Happiness, iParameter = the amount of additional happiness
        # iUP_PerCityCommerce, iParameter = 1000000 * bonus_in_gold + 10000*bonus_in_research + 100*bonus_in_culture + bonus_in_espionage (bonuses are limited to 0 - 99)
        # iUP_CommercePercent, iParameter = 1000000 * bonus_in_gold + 10000*bonus_in_research + 100*bonus_in_culture + bonus_in_espionage (bonuses are limited to 0 - 99 percent)
        # iUP_CulturalTolerance, iParameter = 0 for no unhappiness or iParameter = k for unhappiness = unhappiness / k
        # iUP_ReligiousTolerance, iParameter = 0 for no instability
        # iUP_Conscription, iParameter = percent of foreign culture needed to draft + 100 * max number of units to draft per turn
        # iUP_NoResistance, iParameter = 0 for no resistance or iParameter = k for resistance turns = resistance turns / k
        # iUP_UnitProduction, iParameter = iRequiredTech * 100 + Percent ( 75% for 25% faster unit building)
        # iUP_EnableCivics, iParameter = Civic5 * 100000000 + Civic4 * 1000000 + Civic3 * 10000 + Civic2 * 100 + Civic1, NOTE: also need to enable this in the WB, civic indexed by 0 is always available, civic5 cannot be bigger than 20
        # iUP_TradeRoutes, iParameter = number of extra trade routes, NOTE: this must be synchronized with GlobalDefines.xml: max trade routes
        # iUP_PromotionI, iParameter = the bonus promotion
        # iUP_PromotionII, iParameter = the bonus promotion
        # iUP_Inquisition, iParameter is not used
        # iUP_CanEnterTerrain, iParameter is the terrain to enter, NOTE: also enables trade through the given terrain type
        # iUP_Discovery, iParameter = ColonyStart * 1000000 + ColonyEnd * 1000 + iModifier modifies the cost associated with all projects (iCost *= iModifier; iCost /= 100 )
        # iUP_EndlessLand, iParameter = percent change (i.e. upkeep *= iParameter, upkeep /= 100 )
        # iUP_ForeignSea, use iParameter = 1 to activate
        # iUP_Pious, whenever changeFaith( x ) is called, x is multiplied by iParameter
        # iUP_HealthFood, iParameter = percentage, what ratio of the city's excess health should be converted into food
        # iUP_TerrainBonus, iParameter = iActivate * 100000 (1 to be active) + iTerrain * 1000 + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus (bonuses are limited to 0-9)
        # iUP_FeatureBonus, iParameter = iActivate * 100000 (1 to be active) + iFeature * 1000 + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus (bonuses are limited to 0-9)
        # iUP_ImprovementBonus, iParameter = iActivate * 100000 (1 to be active) + iImprovement * 1000 + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus (bonuses are limited to 0-9)
        # iUP_CityTileYield, iParameter = iActivate * 1000 (1 to be active) + iFoodBonus * 100 + iProductionBonus * 10 + iCommerceBonus, (bonuses are limited to 0-9)

        gc.setUP(Civ.BURGUNDY.value, UniquePower.HAPPINESS_BONUS.value, 1)
        gc.setUP(Civ.BURGUNDY.value, UniquePower.PER_CITY_COMMERCE_BONUS.value, 200)

        gc.setUP(Civ.BYZANTIUM.value, UniquePower.NO_COLLAPSE_IN_CORE_AND_NORMAL_AREAS.value, 1)
        gc.setUP(Civ.BYZANTIUM.value, UniquePower.PRE_ACCESS_CIVICS.value, Civic.IMPERIALISM.value)

        gc.setUP(Civ.FRANCE.value, UniquePower.LESS_INSTABILITY_WITH_FOREIGN_LAND.value, 1)

        gc.setUP(Civ.ARABIA.value, UniquePower.SPREAD_STATE_RELIGION_TO_NEW_CITIES.value, 1)

        gc.setUP(Civ.BULGARIA.value, UniquePower.NO_RESISTANCE.value, 0)

        gc.setUP(
            Civ.CORDOBA.value,
            UniquePower.PROMOTION_FOR_ALL_VALID_UNITS.value,
            Promotion.MEDIC.value,
        )
        gc.setUP(Civ.CORDOBA.value, UniquePower.GROWTH_CITY_WITH_HEALTH_EXCESS.value, 50)

        gc.setUP(
            Civ.MOROCCO.value,
            UniquePower.TERRAIN_BONUS.value,
            1 * 100000 + Terrain.DESERT.value * 1000 + 10 + 1,
        )
        gc.setUP(
            Civ.MOROCCO.value,
            UniquePower.FEATURE_BONUS.value,
            1 * 100000 + Feature.OASIS.value * 1000 + 100 + 1,
        )

        gc.setUP(
            Civ.CASTILE.value, UniquePower.LESS_INSTABILITY_WITH_RELIGIOUS_PROSECUTION.value, 1
        )
        gc.setUP(Civ.CASTILE.value, UniquePower.PER_CITY_COMMERCE_BONUS.value, 2)

        gc.setUP(Civ.NORWAY.value, UniquePower.CAN_ENTER_TERRAIN.value, Terrain.OCEAN.value)
        gc.setUP(
            Civ.NORWAY.value, UniquePower.STABILITY_BONUS_FOUNDING.value, 1
        )  # "hidden" part of the UP

        gc.setUP(
            Civ.VENECIA.value, UniquePower.PRE_ACCESS_CIVICS.value, Civic.MERCHANT_REPUBLIC.value
        )
        # gc.setUP( iVenecia, UniquePower.ALLOW_SHIPS_IN_FOREIGN_SEA.value, 1 )

        gc.setUP(Civ.KIEV.value, UniquePower.CITY_TILE_YIELD_BONUS.value, 1 * 1000 + 100 * 2)

        gc.setUP(Civ.HUNGARY.value, UniquePower.HAPPINESS_BONUS.value, 1)
        gc.setUP(Civ.HUNGARY.value, UniquePower.NO_UNHAPPINESS_WITH_FOREIGN_CULTURE.value, 0)

        gc.setUP(
            Civ.GERMANY.value,
            UniquePower.FASTER_UNIT_PRODUCTION.value,
            Technology.GUNPOWDER.value * 100 + 75,
        )

        gc.setUP(Civ.POLAND.value, UniquePower.NO_INSTABILITY_WITH_FOREIGN_RELIGION.value, 0)

        gc.setUP(Civ.LITHUANIA.value, UniquePower.CULTURE_BONUS_WITH_NO_STATE_RELIGION.value, 200)
        gc.setUP(Civ.LITHUANIA.value, UniquePower.HAPPINESS_BONUS_WITH_NO_STATE_RELIGION.value, 1)

        gc.setSupportModifiersAI(Civ.MOSCOW.value, 10, 100, 20, 10, 100)  # sync with preset values
        gc.setSupportModifiersHu(Civ.MOSCOW.value, 10, 100, 20, 10, 100)  # sync with preset values
        gc.setUP(Civ.MOSCOW.value, UniquePower.LOWER_CITY_MAINTENANCE_COST.value, 50)

        gc.setUP(
            Civ.GENOA.value, UniquePower.HALVE_COST_OF_MERCENARIES.value, 1
        )  # Absinthe: this actually has no effect, it is implemented in Mercenaries.py entirely

        gc.setUP(
            Civ.SCOTLAND.value,
            UniquePower.IMPROVEMENT_BONUS.value,
            1 * 100000 + Improvement.FORT.value * 1000 + 2,
        )

        gc.setUP(
            Civ.ENGLAND.value,
            UniquePower.IMPROVEMENT_BONUS.value,
            1 * 100000 + Improvement.WORKSHOP.value * 1000 + 1,
        )
        gc.setUP(
            Civ.ENGLAND.value,
            UniquePower.IMPROVEMENT_BONUS_2.value,
            1 * 100000 + Improvement.COTTAGE.value * 1000 + 10,
        )
        gc.setUP(
            Civ.ENGLAND.value,
            UniquePower.IMPROVEMENT_BONUS_3.value,
            1 * 100000 + Improvement.HAMLET.value * 1000 + 10,
        )
        gc.setUP(
            Civ.ENGLAND.value,
            UniquePower.IMPROVEMENT_BONUS_4.value,
            1 * 100000 + Improvement.VILLAGE.value * 1000 + 10,
        )
        gc.setUP(
            Civ.ENGLAND.value,
            UniquePower.IMPROVEMENT_BONUS_5.value,
            1 * 100000 + Improvement.TOWN.value * 1000 + 10,
        )

        # Speed up East/West India Trading Companies and all Colonies
        gc.setUP(
            Civ.PORTUGAL.value,
            UniquePower.LOWER_COST_FOR_PROJECTS.value,
            (len(Project) - 2) * 1000000 + max(Colony) * 1000 + 30,
        )
        gc.setUP(
            Civ.PORTUGAL.value, UniquePower.STABILITY_BONUS_FOUNDING.value, 1
        )  # "hidden" part of the UP

        for i in civilizations().drop(Civ.BARBARIAN).ids():
            if not i == Civ.AUSTRIA.value:
                gc.setDiplomacyModifiers(i, Civ.AUSTRIA.value, +4)
        gc.setUP(Civ.AUSTRIA.value, UniquePower.PER_CITY_COMMERCE_BONUS.value, 200)

        # gc.setUP( iTurkey, UniquePower.CONSCRIPTION.value, 330 )
        # gc.setUP( iTurkey, UniquePower.CONSCRIPTION.value, 1 )
        gc.setUP(Civ.OTTOMAN.value, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS.value, 1)

        gc.setUP(
            Civ.SWEDEN.value,
            UniquePower.PROMOTION_FOR_ALL_VALID_UNITS.value,
            Promotion.FORMATION.value,
        )

        gc.setUP(Civ.NOVGOROD.value, UniquePower.PRE_ACCESS_CIVICS.value, Civic.BUREAUCRACY.value)

        gc.setUP(Civ.PRUSSIA.value, UniquePower.PRE_ACCESS_CIVICS.value, Civic.THEOCRACY.value)
        # Absinthe: handled in python currently
        # gc.setUP( iPrussia, UniquePower.NO_INSTABILITY_WITH_CIVIC_AND_STATE_RELIGION_CHANGE.value, 1 )

        # Absinthe: handled in python currently
        # gc.setUP( iAragon, UniquePower.EXTRA_COMMERCE_BONUS.value, 0 )

        # Absinthe: handled in python currently
        # gc.setUP( iScotland, UniquePower.EXTRA_UNITS_WHEN_LOSING_CITY.value, 1 )

        gc.setUP(Civ.DUTCH.value, UniquePower.EXTRA_TRADE_ROUTES.value, 2)
        gc.setUP(
            Civ.DUTCH.value, UniquePower.IMPROVE_GAIN_FAITH_POINTS.value, 2
        )  # 3Miro: "hidden" buff to the Dutch FP, otherwise they have too little piety (not enough cities)
        gc.setUP(
            Civ.DUTCH.value,
            UniquePower.LOWER_COST_FOR_PROJECTS.value,
            (len(Project) - 2) * 1000000 + max(Colony) * 1000 + 30,
        )  # "hidden" part of the UP

        gc.setUP(Civ.POPE.value, UniquePower.NO_COLLAPSE_IN_CORE_AND_NORMAL_AREAS.value, 1)

        # GlobalWarming
        gc.setGlobalWarming(False)

        # Set FastTerrain (i.e. double movement over ocean)
        gc.setFastTerrain(Terrain.OCEAN.value)

        # set religious spread factors
        for civ in civilizations():
            for religion, threshold in civ.religion.spreading_threshold.items():
                gc.setReligionSpread(
                    civ.id,
                    religion.value,
                    threshold,
                )

        # set the religions and year of the great schism
        gc.setSchism(Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, DateTurn.i1053AD)

        gc.setHoliestCity(*CITIES[City.JERUSALEM].to_tuple())

        # 3Miro: Faith Points benefits
        # gc.setReligionBenefit( iReligion, iFP_(whatever it is), iParameter, iCap )
        # 	note that for powers iParameter = -1 means that this religion doesn't have this power (-1 is the default)
        # 	iCap sets a cap for the maximum number of FP a religion can have (per player) Can be adjusted per Player
        #
        # iFP_Stability: stability += iParameter * num_FaithPoints / 100
        # 		 i.e. 1 Faith Point = iParameter percent of a stability point
        # iFP_Civic: civic_upkeep *= 100 - (num_FaithPoints * iParameter) / 100
        # 		civic_upkeep /= 100
        # 		iParameter = 200, means 2% lower cost per Faith Point, iParameter = 50 means .5% lower cost per FP
        # iFP_Growth: iTreshhold *= 100 - (num_FaithPoints * iParameter) / 100
        # 		iTreshhold /= 100
        # 		iParameter = 200, means 2% faster growth per Faith Point, iParameter = 50 means .5% faster growth per FP
        # iFP_Units: iProductionNeeded *= 100 - (num_FaithPoints * iParameter) / 100
        # 		iProductionNeeded /= 100
        # 		iParameter = 200, means 2% faster production per Faith Point, iParameter = 50 means .5% faster production per FP
        # iFP_Science: same as units, iParameter = 200, means 2% lower tech cost per Faith Point, iParameter = 50 means .5% lower tech cost per FP
        # iFP_Production: iProductionNeeded *= 100 - (num_FaithPoints * iParameter) / 100
        # 		iProductionNeeded /= 100
        # 		iParameter = 200, means 2% faster production per Faith Point, iParameter = 50 means .5% faster production per FP
        # 		Counts for Wonders and Projects
        # iFP_Diplomacy: iAttitude += iParameter * num_FaithPoints / 100
        # 		i.e. 1 Faith Point = iParameter percent of an attitude point

        gc.setReligionBenefit(
            Religion.ORTHODOXY.value, FaithPointBonusCategory.BOOST_STABILITY.value, 10, 100
        )
        gc.setReligionBenefit(
            Religion.ORTHODOXY.value, FaithPointBonusCategory.REDUCE_CIVIC_UPKEEP.value, 50, 100
        )

        gc.setReligionBenefit(
            Religion.ISLAM.value, FaithPointBonusCategory.FASTER_POPULATION_GROWTH.value, 50, 100
        )
        gc.setReligionBenefit(
            Religion.ISLAM.value, FaithPointBonusCategory.REDUCING_COST_UNITS.value, 50, 100
        )

        gc.setReligionBenefit(
            Religion.PROTESTANTISM.value, FaithPointBonusCategory.REDUCING_TECH_COST.value, 30, 100
        )
        gc.setReligionBenefit(
            Religion.PROTESTANTISM.value,
            FaithPointBonusCategory.REDUCING_WONDER_COST.value,
            30,
            100,
        )

        gc.setReligionBenefit(
            Religion.CATHOLICISM.value, FaithPointBonusCategory.BOOST_DIPLOMACY.value, 6, 100
        )
        gc.setReligionBenefit(
            Religion.ISLAM.value, FaithPointBonusCategory.BOOST_DIPLOMACY.value, 5, 100
        )
        gc.setReligionBenefit(
            Religion.PROTESTANTISM.value, FaithPointBonusCategory.BOOST_DIPLOMACY.value, 4, 100
        )
        gc.setReligionBenefit(
            Religion.ORTHODOXY.value, FaithPointBonusCategory.BOOST_DIPLOMACY.value, 3, 100
        )

        # a land tile that is normally impassable but the desired player can pass through it
        # gc.setStrategicTile( iVenecia, 56, 35 )

        # set AI modifiers for preferred buildings
        # use values -10 for very unlikely, 0 for default neutral and positive for desirable
        # values less than -10 might not work, above 10 should be fine

        # the utils.getUniqueBuilding function does not work, probably the util functions are not yet usable when these initial values are set
        # but in the .dll these values are only used for the civ-specific building of the given buildingclass, so we can these add redundantly
        for iPlayer in civilizations().majors().ids():
            # walls, kasbah
            gc.setBuildingPref(iPlayer, Building.WALLS.value, 5)
            gc.setBuildingPref(iPlayer, Building.MOROCCO_KASBAH.value, 5)
            # castle, stronghold, citadel, kremlin
            gc.setBuildingPref(iPlayer, Building.CASTLE.value, 7)
            gc.setBuildingPref(iPlayer, Building.MOSCOW_KREMLIN.value, 7)
            gc.setBuildingPref(iPlayer, Building.HUNGARIAN_STRONGHOLD.value, 7)
            gc.setBuildingPref(iPlayer, Building.SPANISH_CITADEL.value, 7)
            # manor house, chateau, naval base
            gc.setBuildingPref(iPlayer, Building.MANOR_HOUSE.value, 5)
            gc.setBuildingPref(iPlayer, Building.FRENCH_CHATEAU.value, 5)
            gc.setBuildingPref(iPlayer, Building.VENICE_NAVAL_BASE.value, 5)
            # courthouse, rathaus, veche, voivodeship
            gc.setBuildingPref(iPlayer, Building.COURTHOUSE.value, 5)
            gc.setBuildingPref(iPlayer, Building.KIEV_VECHE.value, 5)
            gc.setBuildingPref(iPlayer, Building.HOLY_ROMAN_RATHAUS.value, 5)
            gc.setBuildingPref(iPlayer, Building.LITHUANIAN_VOIVODESHIP.value, 5)
            # nightwatch, soldattorp
            gc.setBuildingPref(iPlayer, Building.NIGHT_WATCH.value, 3)
            gc.setBuildingPref(iPlayer, Building.SWEDISH_TENNANT.value, 3)

        gc.setBuildingPref(Civ.BYZANTIUM.value, Wonder.ST_CATHERINE_MONASTERY.value, 15)
        gc.setBuildingPref(Civ.BYZANTIUM.value, Wonder.BOYANA_CHURCH.value, 2)
        gc.setBuildingPref(Civ.BYZANTIUM.value, Wonder.ROUND_CHURCH.value, 2)
        gc.setBuildingPref(Civ.BYZANTIUM.value, Wonder.SOPHIA_KIEV.value, 5)

        gc.setBuildingPref(Civ.FRANCE.value, Wonder.NOTRE_DAME.value, 20)
        gc.setBuildingPref(Civ.FRANCE.value, Wonder.VERSAILLES.value, 20)
        gc.setBuildingPref(Civ.FRANCE.value, Wonder.FONTAINEBLEAU.value, 10)
        gc.setBuildingPref(Civ.FRANCE.value, Wonder.MONASTERY_OF_CLUNY.value, 10)
        gc.setBuildingPref(Civ.FRANCE.value, Wonder.MONT_SAINT_MICHEL.value, 10)
        gc.setBuildingPref(Civ.FRANCE.value, Wonder.PALAIS_DES_PAPES.value, 5)
        gc.setBuildingPref(Civ.FRANCE.value, Wonder.LOUVRE.value, 20)

        gc.setBuildingPref(Civ.ARABIA.value, Wonder.DOME_ROCK.value, 15)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.TOMB_AL_WALID.value, 20)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.ALAZHAR.value, 20)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.MOSQUE_OF_KAIROUAN.value, 10)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.KOUTOUBIA_MOSQUE.value, 5)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.GARDENS_AL_ANDALUS.value, 5)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.LA_MEZQUITA.value, 5)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.ALHAMBRA.value, 5)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.NOTRE_DAME.value, -5)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.STEPHANSDOM.value, -5)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.SISTINE_CHAPEL.value, -5)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.KRAK_DES_CHEVALIERS.value, -5)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.LEANING_TOWER.value, -3)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.GOLDEN_BULL.value, -3)
        gc.setBuildingPref(Civ.ARABIA.value, Wonder.COPERNICUS.value, -3)

        gc.setBuildingPref(Civ.BULGARIA.value, Wonder.ROUND_CHURCH.value, 20)
        gc.setBuildingPref(Civ.BULGARIA.value, Wonder.BOYANA_CHURCH.value, 20)
        gc.setBuildingPref(Civ.BULGARIA.value, Wonder.ST_CATHERINE_MONASTERY.value, 5)
        gc.setBuildingPref(Civ.BULGARIA.value, Wonder.SOPHIA_KIEV.value, 5)

        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.GARDENS_AL_ANDALUS.value, 20)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.LA_MEZQUITA.value, 20)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.ALHAMBRA.value, 20)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.DOME_ROCK.value, 10)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.ALAZHAR.value, 5)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.MOSQUE_OF_KAIROUAN.value, 10)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.KOUTOUBIA_MOSQUE.value, 5)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.NOTRE_DAME.value, -5)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.STEPHANSDOM.value, -5)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.SISTINE_CHAPEL.value, -5)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.KRAK_DES_CHEVALIERS.value, -5)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.LEANING_TOWER.value, -3)
        gc.setBuildingPref(Civ.CORDOBA.value, Wonder.GOLDEN_BULL.value, -3)

        gc.setBuildingPref(Civ.VENECIA.value, Wonder.MARCO_POLO.value, 15)
        gc.setBuildingPref(Civ.VENECIA.value, Wonder.SAN_MARCO.value, 20)
        gc.setBuildingPref(Civ.VENECIA.value, Wonder.LANTERNA.value, 10)
        gc.setBuildingPref(Civ.VENECIA.value, Wonder.LEONARDOS_WORKSHOP.value, 5)
        gc.setBuildingPref(Civ.VENECIA.value, Wonder.LEANING_TOWER.value, 5)
        gc.setBuildingPref(Civ.VENECIA.value, Wonder.GRAND_ARSENAL.value, 20)
        gc.setBuildingPref(Civ.VENECIA.value, Wonder.GALATA_TOWER.value, 10)
        gc.setBuildingPref(Civ.VENECIA.value, Wonder.FLORENCE_DUOMO.value, 10)
        gc.setBuildingPref(Civ.VENECIA.value, Wonder.SAN_GIORGIO.value, 5)

        gc.setBuildingPref(Civ.BURGUNDY.value, Wonder.MONASTERY_OF_CLUNY.value, 20)
        gc.setBuildingPref(Civ.BURGUNDY.value, Wonder.NOTRE_DAME.value, 10)
        gc.setBuildingPref(Civ.BURGUNDY.value, Wonder.VERSAILLES.value, 10)
        gc.setBuildingPref(Civ.BURGUNDY.value, Wonder.MONT_SAINT_MICHEL.value, 10)
        gc.setBuildingPref(Civ.BURGUNDY.value, Wonder.FONTAINEBLEAU.value, 5)
        gc.setBuildingPref(Civ.BURGUNDY.value, Wonder.PALAIS_DES_PAPES.value, 5)
        gc.setBuildingPref(Civ.BURGUNDY.value, Wonder.LOUVRE.value, 10)

        gc.setBuildingPref(Civ.GERMANY.value, Wonder.BRANDENBURG_GATE.value, 10)
        gc.setBuildingPref(Civ.GERMANY.value, Wonder.IMPERIAL_DIET.value, 20)
        gc.setBuildingPref(Civ.GERMANY.value, Wonder.COPERNICUS.value, 5)
        gc.setBuildingPref(Civ.GERMANY.value, Wonder.GOLDEN_BULL.value, 10)
        gc.setBuildingPref(Civ.GERMANY.value, Wonder.MONASTERY_OF_CLUNY.value, 5)
        gc.setBuildingPref(Civ.GERMANY.value, Wonder.URANIBORG.value, 5)
        gc.setBuildingPref(Civ.GERMANY.value, Wonder.THOMASKIRCHE.value, 20)

        gc.setBuildingPref(Civ.NOVGOROD.value, Wonder.ST_BASIL.value, 10)
        gc.setBuildingPref(Civ.NOVGOROD.value, Wonder.SOPHIA_KIEV.value, 10)
        gc.setBuildingPref(Civ.NOVGOROD.value, Wonder.ROUND_CHURCH.value, 5)
        gc.setBuildingPref(Civ.NOVGOROD.value, Wonder.BOYANA_CHURCH.value, 5)
        gc.setBuildingPref(Civ.NOVGOROD.value, Wonder.BORGUND_STAVE_CHURCH.value, 5)
        gc.setBuildingPref(Civ.NOVGOROD.value, Wonder.PETERHOF_PALACE.value, 15)

        gc.setBuildingPref(Civ.NORWAY.value, Wonder.SHRINE_OF_UPPSALA.value, 20)
        gc.setBuildingPref(Civ.NORWAY.value, Wonder.SAMOGITIAN_ALKAS.value, 5)
        gc.setBuildingPref(Civ.NORWAY.value, Wonder.BORGUND_STAVE_CHURCH.value, 15)
        gc.setBuildingPref(Civ.NORWAY.value, Wonder.URANIBORG.value, 10)
        gc.setBuildingPref(Civ.NORWAY.value, Wonder.KALMAR_CASTLE.value, 5)

        gc.setBuildingPref(Civ.KIEV.value, Wonder.SOPHIA_KIEV.value, 20)
        gc.setBuildingPref(Civ.KIEV.value, Wonder.ST_BASIL.value, 5)
        gc.setBuildingPref(Civ.KIEV.value, Wonder.ROUND_CHURCH.value, 5)
        gc.setBuildingPref(Civ.KIEV.value, Wonder.BOYANA_CHURCH.value, 5)
        gc.setBuildingPref(Civ.KIEV.value, Wonder.PETERHOF_PALACE.value, 10)

        gc.setBuildingPref(Civ.HUNGARY.value, Wonder.PRESSBURG.value, 20)
        gc.setBuildingPref(Civ.HUNGARY.value, Wonder.GOLDEN_BULL.value, 20)
        gc.setBuildingPref(Civ.HUNGARY.value, Wonder.BIBLIOTHECA_CORVINIANA.value, 20)
        gc.setBuildingPref(Civ.HUNGARY.value, Wonder.KAZIMIERZ.value, 10)
        gc.setBuildingPref(Civ.HUNGARY.value, Wonder.COPERNICUS.value, 5)
        gc.setBuildingPref(Civ.HUNGARY.value, Wonder.STEPHANSDOM.value, 5)

        gc.setBuildingPref(Civ.CASTILE.value, Wonder.ESCORIAL.value, 20)
        gc.setBuildingPref(Civ.CASTILE.value, Wonder.MAGELLANS_VOYAGE.value, 10)
        gc.setBuildingPref(Civ.CASTILE.value, Wonder.TORRE_DEL_ORO.value, 20)
        gc.setBuildingPref(Civ.CASTILE.value, Wonder.BELEM_TOWER.value, 10)

        gc.setBuildingPref(Civ.DENMARK.value, Wonder.KALMAR_CASTLE.value, 10)
        gc.setBuildingPref(Civ.DENMARK.value, Wonder.SHRINE_OF_UPPSALA.value, 20)
        gc.setBuildingPref(Civ.DENMARK.value, Wonder.SAMOGITIAN_ALKAS.value, 5)
        gc.setBuildingPref(Civ.DENMARK.value, Wonder.BORGUND_STAVE_CHURCH.value, 15)
        gc.setBuildingPref(Civ.DENMARK.value, Wonder.URANIBORG.value, 20)

        gc.setBuildingPref(Civ.SCOTLAND.value, Wonder.MAGNA_CARTA.value, 10)
        gc.setBuildingPref(Civ.SCOTLAND.value, Wonder.WESTMINSTER.value, 10)
        gc.setBuildingPref(Civ.SCOTLAND.value, Wonder.MONASTERY_OF_CLUNY.value, 5)
        gc.setBuildingPref(Civ.SCOTLAND.value, Wonder.BORGUND_STAVE_CHURCH.value, 5)
        gc.setBuildingPref(Civ.SCOTLAND.value, Wonder.MONT_SAINT_MICHEL.value, 5)

        gc.setBuildingPref(Civ.POLAND.value, Wonder.PRESSBURG.value, 10)
        gc.setBuildingPref(Civ.POLAND.value, Wonder.COPERNICUS.value, 10)
        gc.setBuildingPref(Civ.POLAND.value, Wonder.GOLDEN_BULL.value, 5)
        gc.setBuildingPref(Civ.POLAND.value, Wonder.KAZIMIERZ.value, 15)
        gc.setBuildingPref(Civ.POLAND.value, Wonder.JASNA_GORA.value, 20)
        gc.setBuildingPref(Civ.POLAND.value, Wonder.BRANDENBURG_GATE.value, 5)

        gc.setBuildingPref(Civ.GENOA.value, Wonder.SAN_GIORGIO.value, 20)
        gc.setBuildingPref(Civ.GENOA.value, Wonder.LANTERNA.value, 20)
        gc.setBuildingPref(Civ.GENOA.value, Wonder.LEONARDOS_WORKSHOP.value, 5)
        gc.setBuildingPref(Civ.GENOA.value, Wonder.LEANING_TOWER.value, 5)
        gc.setBuildingPref(Civ.GENOA.value, Wonder.SAN_MARCO.value, 5)
        gc.setBuildingPref(Civ.GENOA.value, Wonder.MARCO_POLO.value, 5)
        gc.setBuildingPref(Civ.GENOA.value, Wonder.GRAND_ARSENAL.value, 10)
        gc.setBuildingPref(Civ.GENOA.value, Wonder.GALATA_TOWER.value, 20)
        gc.setBuildingPref(Civ.GENOA.value, Wonder.FLORENCE_DUOMO.value, 10)

        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.GARDENS_AL_ANDALUS.value, 10)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.LA_MEZQUITA.value, 10)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.ALHAMBRA.value, 10)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.DOME_ROCK.value, 10)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.ALAZHAR.value, 5)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.MOSQUE_OF_KAIROUAN.value, 10)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.KOUTOUBIA_MOSQUE.value, 20)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.NOTRE_DAME.value, -5)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.STEPHANSDOM.value, -5)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.SISTINE_CHAPEL.value, -5)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.KRAK_DES_CHEVALIERS.value, -5)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.LEANING_TOWER.value, -3)
        gc.setBuildingPref(Civ.MOROCCO.value, Wonder.GOLDEN_BULL.value, -3)

        gc.setBuildingPref(Civ.ENGLAND.value, Wonder.MAGNA_CARTA.value, 20)
        gc.setBuildingPref(Civ.ENGLAND.value, Wonder.WESTMINSTER.value, 20)
        gc.setBuildingPref(Civ.ENGLAND.value, Wonder.MONASTERY_OF_CLUNY.value, 5)
        gc.setBuildingPref(Civ.ENGLAND.value, Wonder.URANIBORG.value, 5)
        gc.setBuildingPref(Civ.ENGLAND.value, Wonder.TORRE_DEL_ORO.value, 5)
        gc.setBuildingPref(Civ.ENGLAND.value, Wonder.BELEM_TOWER.value, 5)

        gc.setBuildingPref(Civ.PORTUGAL.value, Wonder.BELEM_TOWER.value, 20)
        gc.setBuildingPref(Civ.PORTUGAL.value, Wonder.PALACIO_DA_PENA.value, 20)
        gc.setBuildingPref(Civ.PORTUGAL.value, Wonder.MAGELLANS_VOYAGE.value, 20)
        gc.setBuildingPref(Civ.PORTUGAL.value, Wonder.TORRE_DEL_ORO.value, 10)

        gc.setBuildingPref(Civ.ARAGON.value, Wonder.MAGELLANS_VOYAGE.value, 10)
        gc.setBuildingPref(Civ.ARAGON.value, Wonder.TORRE_DEL_ORO.value, 10)
        gc.setBuildingPref(Civ.ARAGON.value, Wonder.ESCORIAL.value, 5)
        gc.setBuildingPref(Civ.ARAGON.value, Wonder.BELEM_TOWER.value, 10)

        gc.setBuildingPref(Civ.SWEDEN.value, Wonder.KALMAR_CASTLE.value, 20)
        gc.setBuildingPref(Civ.SWEDEN.value, Wonder.SHRINE_OF_UPPSALA.value, 5)
        gc.setBuildingPref(Civ.SWEDEN.value, Wonder.BORGUND_STAVE_CHURCH.value, 15)
        gc.setBuildingPref(Civ.SWEDEN.value, Wonder.URANIBORG.value, 10)

        gc.setBuildingPref(Civ.PRUSSIA.value, Wonder.BRANDENBURG_GATE.value, 20)
        gc.setBuildingPref(Civ.PRUSSIA.value, Wonder.THOMASKIRCHE.value, 10)
        gc.setBuildingPref(Civ.PRUSSIA.value, Wonder.COPERNICUS.value, 5)
        gc.setBuildingPref(Civ.PRUSSIA.value, Wonder.PRESSBURG.value, 5)

        gc.setBuildingPref(Civ.LITHUANIA.value, Wonder.SAMOGITIAN_ALKAS.value, 20)
        gc.setBuildingPref(Civ.LITHUANIA.value, Wonder.GEDIMINAS_TOWER.value, 20)
        gc.setBuildingPref(Civ.LITHUANIA.value, Wonder.BORGUND_STAVE_CHURCH.value, 5)

        gc.setBuildingPref(Civ.AUSTRIA.value, Wonder.STEPHANSDOM.value, 20)
        gc.setBuildingPref(Civ.AUSTRIA.value, Wonder.THOMASKIRCHE.value, 15)
        gc.setBuildingPref(Civ.AUSTRIA.value, Wonder.COPERNICUS.value, 5)
        gc.setBuildingPref(Civ.AUSTRIA.value, Wonder.GOLDEN_BULL.value, 5)
        gc.setBuildingPref(Civ.AUSTRIA.value, Wonder.PRESSBURG.value, 5)
        gc.setBuildingPref(Civ.AUSTRIA.value, Building.AUSTRIAN_OPERA_HOUSE.value, 10)

        gc.setBuildingPref(Civ.OTTOMAN.value, Wonder.TOPKAPI_PALACE.value, 20)
        gc.setBuildingPref(Civ.OTTOMAN.value, Wonder.BLUE_MOSQUE.value, 20)
        gc.setBuildingPref(Civ.OTTOMAN.value, Wonder.SELIMIYE_MOSQUE.value, 20)
        gc.setBuildingPref(Civ.OTTOMAN.value, Wonder.TOMB_AL_WALID.value, 10)
        gc.setBuildingPref(Civ.OTTOMAN.value, Wonder.KIZIL_KULE.value, 10)
        gc.setBuildingPref(Civ.OTTOMAN.value, Wonder.ALAZHAR.value, 5)

        gc.setBuildingPref(Civ.MOSCOW.value, Wonder.ST_BASIL.value, 20)
        gc.setBuildingPref(Civ.MOSCOW.value, Wonder.PETERHOF_PALACE.value, 20)
        gc.setBuildingPref(Civ.MOSCOW.value, Wonder.SOPHIA_KIEV.value, 5)

        gc.setBuildingPref(Civ.DUTCH.value, Wonder.BEURS.value, 20)
        gc.setBuildingPref(Civ.DUTCH.value, Wonder.URANIBORG.value, 5)
        gc.setBuildingPref(Civ.DUTCH.value, Wonder.THOMASKIRCHE.value, 5)

        gc.setBuildingPref(Civ.POPE.value, Wonder.SISTINE_CHAPEL.value, 20)
        gc.setBuildingPref(Civ.POPE.value, Wonder.PALAIS_DES_PAPES.value, 10)
        gc.setBuildingPref(Civ.POPE.value, Wonder.LEANING_TOWER.value, 5)
        gc.setBuildingPref(Civ.POPE.value, Wonder.FLORENCE_DUOMO.value, 5)
        gc.setBuildingPref(Civ.POPE.value, Wonder.LEONARDOS_WORKSHOP.value, 5)

        # 3Miro: set the Jews as the minor Religion
        gc.setMinorReligion(Religion.JUDAISM.value)
        gc.setMinorReligionRefugies(0)

        # Manor House + Manorialism: iBuilding + 1000 * iCivic + 100,000 * iGold + 1,000,000 * iResearch + 10,000,000 * iCulture + 100,000,000 * iEspionage
        # 3Miro: moved to XML, no need to put it here
        # gc.setBuildingCivicCommerseCombo1( Building.MANOR_HOUSE.value + 1000 * Technology.MANORIALISM.value + 100000 * 2 + 1000000 * 0 + 10000000 * 0 + 100000000 * 0 );
        # gc.setBuildingCivicCommerseCombo2( Building.FRENCH_CHATEAU.value + 1000 * Technology.MANORIALISM.value + 100000 * 2 + 1000000 * 0 + 10000000 * 0 + 100000000 * 0 );
        # gc.setBuildingCivicCommerseCombo3(-1)

        # 3Miro: Psycho AI cheat, this will make Ottoman AI think it can win battles vs Constantinople at 90/100 rate
        # 	it will also actually boost the Ottoman's odds (actually lower the defenders chance by 20 percent), but only when attacking Constantinople
        gc.setPsychoAICheat(
            Civ.OTTOMAN.value, *civilization(Civ.BYZANTIUM).location.capital.to_tuple()
        )

        # 3Miro: be very careful here, this can really mess the AI
        # 	setHistoricalEnemyAICheat( iAttacker, iDefender, 10 ) gives the attacker +10% bonus, when attacked units belong to the defender
        # 	this modifier only works in AI vs AI battles, it's ignored if either player is Human
        # 	none of the AI players is "aware" of the modification, if you make it too big, it could lead to a couple strange situations
        # 	(where the AI has clear advantage in a battle, yet it still won't attack)
        # 	so this should be a "last resort" solution, other methods are always preferable
        gc.setHistoricalEnemyAICheat(Civ.OTTOMAN.value, Civ.BULGARIA.value, 10)
        gc.setHistoricalEnemyAICheat(Civ.BULGARIA.value, Civ.OTTOMAN.value, -10)

        gc.setHistoricalEnemyAICheat(Civ.CASTILE.value, Civ.CORDOBA.value, 10)
        gc.setHistoricalEnemyAICheat(Civ.CORDOBA.value, Civ.CASTILE.value, -10)

        gc.setHistoricalEnemyAICheat(Civ.PORTUGAL.value, Civ.CASTILE.value, 10)
        gc.setHistoricalEnemyAICheat(Civ.CASTILE.value, Civ.PORTUGAL.value, -10)

        gc.setHistoricalEnemyAICheat(Civ.AUSTRIA.value, Civ.HUNGARY.value, 10)
        gc.setHistoricalEnemyAICheat(Civ.HUNGARY.value, Civ.AUSTRIA.value, -10)

        gc.setHistoricalEnemyAICheat(Civ.AUSTRIA.value, Civ.GERMANY.value, 10)
        gc.setHistoricalEnemyAICheat(Civ.GERMANY.value, Civ.AUSTRIA.value, -10)

        # 3Miro: this sets rules on how players can Vassalize, first two parameters are the players (we should probably keep this symmetric)
        # 	if the third parameter is -1: cannot Vassalize, 0: has to satisfy a condition (default), 1 can Vassalize without conditions
        # 	the condition is that either one of the players needs to have a city in a province that the other players considers >= the last parameter
        # 	the default for the last parameter is 0, we should call this at least once to set the parameter (it is the same for all players)
        gc.setVassalagaeCondition(
            Civ.CORDOBA.value, Civ.ARABIA.value, 1, ProvinceType.CONTESTED.value
        )
        gc.setVassalagaeCondition(
            Civ.ARABIA.value, Civ.CORDOBA.value, 1, ProvinceType.CONTESTED.value
        )

        # How much culture should we get into a province of this type, ignore the war and settler values (0,0)
        gc.setProvinceTypeParams(ProvinceType.NONE.value, 0, 0, 1, 3)  # 1/3 culture
        gc.setProvinceTypeParams(ProvinceType.CONTESTED.value, 0, 0, 1, 1)  # no change to culture
        gc.setProvinceTypeParams(ProvinceType.POTENTIAL.value, 0, 0, 1, 1)  # same as outer culture
        gc.setProvinceTypeParams(ProvinceType.HISTORICAL.value, 0, 0, 2, 1)  # double-culture
        gc.setProvinceTypeParams(ProvinceType.CORE.value, 0, 0, 3, 1)  # triple-culture

        # block foundation of Protestantism except by a Catholic player
        gc.setParentSchismReligions(Religion.CATHOLICISM.value, Religion.PROTESTANTISM.value)

        # block declaration of war against newly spawning nations for this many turns (pre-set wars are not affected)
        gc.setPaceTurnsAfterSpawn(5)

        # Absinthe: Visualization parameters are outdated
        # 			display for Core and Normal areas were added in CvEventManager/onGameStart, can be enabled/disabled in the GlobalDefines_Alt.xml
        # 			those are the only 2 you might want to use on the main map, for everything else we have better tools in the WB
        ## set the Visualization parameters, note that those functions can be accessed at any time, not just here
        ## note that if you set Civs for mode 0 and 1 in WB mode, they will stay set until you exit
        # gc.setWhatToPlot( 0 ) # 0 - Core (default), 1 - Normal, 2 - Settler, 3 - Wars
        ##gc.setCivForCore( iByzantium ) # plot the Core of Byzantium (only if setWhatToPlot is set to 0)
        ##gc.setCivForNormal( iByzantium ) # plot the Normal area of Byzantium (only if setWhatToPlot is set to 1)
        ##gc.setCivForSettler( iFrankia ) # plot the Settlers Map of Byzantium (only if setWhatToPlot is set to 2)
        ##gc.setCivForWars( iByzantium ) # plot the Wars Map of of Byzantium (only if setWhatToPlot is set to 3)

        self.postAreas()

    def setModifiers(self):
        for civ in civilizations():
            self.setGrowthModifier(civ)
            self.setProductionModifier(civ)
            self.setSupportModifier(civ)

    def setGrowthModifier(self, civ):
        # void setGrowthModifiers( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop );
        # iInitPop is the initial population in a city, also can use gc.setInitialPopulation( iCiv, iInitPop ) to change a single civ
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100, 1 )
        # 3Miro: ABOUT CULTURE notice the culture modifier is different from the others, it modifies the culture output as opposed to the culture threshold
        # 	50 means less culture, 200 means more culture. This is applied to Culture output of 10 or more.
        fct_mapper = {
            ModifierCategory.AI: gc.setGrowthModifiersAI,
            ModifierCategory.HUMAN: gc.setGrowthModifiersHu,
        }
        for category, modifiers in civ.modifiers.growth.items():
            if modifiers is not None:
                fct_mapper[category](civ.id, *modifiers)

    def setProductionModifier(self, civ):
        # void setProductionModifiers( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch );
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100 )
        # 3Miro: at 100 research cost, the cost is exactly as in the XML files, the cost in general is however increased for all civs
        fct_mapper = {
            ModifierCategory.AI: gc.setProductionModifiersAI,
            ModifierCategory.HUMAN: gc.setProductionModifiersHu,
        }
        for category, modifiers in civ.modifiers.production.items():
            if modifiers is not None:
                fct_mapper[category](civ.id, *modifiers)

    def setSupportModifier(self, civ):
        # void setSupportModifiers( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic );
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100 )
        # note that iCityNum also gets an additional modifier based on population in the city
        # note that the base for inflation is modified by turn number (among many other things)
        fct_mapper = {
            ModifierCategory.AI: gc.setSupportModifiersAI,
            ModifierCategory.HUMAN: gc.setSupportModifiersHu,
        }
        for category, modifiers in civ.modifiers.support.items():
            if modifiers is not None:
                fct_mapper[category](civ.id, *modifiers)

    def setTechTimeline(self):
        gc.setTimelineTechModifiers(
            9, 25, -50, 1, 100, 50
        )  # go between 10 times slower and 4 times faster
        # formula is: iAhistoric = iCurrentTurn - iHistoricTurn, capped at ( iTPCap, iTBCap )
        # iCost *= 100 + topPenalty * iHistoric * iAhistoric / BotPenalty, iCost /= 100
        # iCost *= 100 - topBuff * iHistoric * iAhistoric / BotBuff, iCost /= 100
        for tech, turn in TIMELINE_TECH_MODIFIER:
            gc.setTimelineTechDateForTech(tech.value, turn)

    def preMapsNSizes(self):
        # settlersMaps, DO NOT CHANGE THIS CODE
        gc.setSizeNPlayers(
            WORLD_WIDTH,
            WORLD_HEIGHT,
            civilizations().majors().len(),
            civilizations().drop(Civ.BARBARIAN).len(),
            len(Technology),
            PlagueType.BUILDING_PLAGUE.value,
            len(Religion),
        )
        for i in civilizations().majors().ids():
            for y in range(WORLD_HEIGHT):
                for x in range(WORLD_WIDTH):
                    gc.setSettlersMap(i, y, x, RFCEMaps.SETTLERS_MAP[i][y][x])
                    gc.setWarsMap(i, y, x, RFCEMaps.WARS_MAP[i][y][x])

        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                if RFCEMaps.PROVINCES_MAP[y][x] > -1:
                    # "no province" of ocean is settled different than -1, set only non-negative values,
                    # the C++ map is initialized to "no-province" by setSizeNPlayers(...)
                    # "no-province" is returned as -1 via the Cy interface
                    gc.setProvince(x, y, RFCEMaps.PROVINCES_MAP[y][x])
        gc.createProvinceCrossreferenceList()  # make sure to call this AFTER setting all the Province entries

        gc.setProvinceTypeNumber(
            len(ProvinceType)
        )  # set the Number of Provinces, call this before you set any AI or culture modifiers

        # birth turns for the players, do not change this loop
        for civ in civilizations().drop(Civ.BARBARIAN):
            gc.setStartingTurn(civ.id, civ.date.birth)

    def postAreas(self):
        # 3Miro: DO NOT CHANGE THIS CODE
        # this adds the Core and Normal Areas into C++. There is Dynamical Memory involved, so don't change this
        for civ in civilizations().majors():
            core_tile_min = civ.location.area.core.tile_min
            core_tile_max = civ.location.area.core.tile_max
            core_additional_tiles = civ.location.area.core.additional_tiles
            normal_tile_min = civ.location.area.normal.tile_min
            normal_tile_max = civ.location.area.normal.tile_max
            normal_exception_tiles = civ.location.area.normal.exception_tiles
            gc.setCoreNormal(
                civ.id,
                core_tile_min.x,
                core_tile_min.y,
                core_tile_max.x,
                core_tile_max.y,
                normal_tile_min.x,
                normal_tile_min.y,
                normal_tile_max.x,
                normal_tile_max.y,
                len(core_additional_tiles),
                len(normal_exception_tiles),
            )
            for tile in core_additional_tiles:
                gc.addCoreException(civ.id, *tile.to_tuple())
            for tile in normal_exception_tiles:
                gc.addNormalException(civ.id, *tile.to_tuple())

        gc.setProsecutorReligions(Unit.PROSECUTOR.value, PROSECUTOR_UNITCLASS)
        gc.setSaintParameters(
            Unit.GREAT_PROPHET.value, GREAT_PROPHET_FAITH_POINT_BONUS, 20, 40
        )  # try to amass at least 20 and don't bother above 40 points
        gc.setIndependnets(
            min(civilizations().independents().ids()),
            max(civilizations().independents().ids()),
            Civ.BARBARIAN.value,
        )
        gc.setPapalPlayer(Civ.POPE.value, Religion.CATHOLICISM.value)

        gc.setAutorunHack(Unit.CATAPULT.value, 32, 0)  # Autorun hack, sync with RNF module

        # 3MiroMercs: set the merc promotion
        gc.setMercPromotion(Promotion.MERC.value)

        for civ in civilizations().majors():
            if civ.initial.condition:
                gc.setStartingWorkers(civ.id, civ.initial.condition.workers)
