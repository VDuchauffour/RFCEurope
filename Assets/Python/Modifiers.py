from CvPythonExtensions import *
from Core import civilizations, log
from CoreTypes import (
    Modifier,
    City,
    Civ,
    Civic,
    Colony,
    Feature,
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
)
from MiscData import (
    BUILDING_PREFERENCES,
    DIPLOMACY_MODIFIERS,
    HISTORICAL_ENEMIES,
    GREAT_PROPHET_FAITH_POINT_BONUS,
    PROSECUTOR_UNITCLASS,
)
from TimelineData import DateTurn
from LocationsData import CITIES
from Events import handler

gc = CyGlobalContext()


@handler("GameStart")
def setup_gamestart():
    log("RFCE: GameStart")
    setup()


@handler("OnLoad")
def setup_on_load():
    log("RFCE: OnLoad")
    setup()


def setup():
    set_modifiers()
    set_diplomacy_modifier()
    set_tech_timeline_modifier()
    set_starting_workers()
    set_initial_building()
    set_building_preferences()
    set_unique_powers()
    set_religion_spread_factor()
    set_religion_benefit()
    set_historical_enemies()
    set_other_parameters()
    log("RFCE: Modifiers.setup()")


def set_modifiers():
    for civ in civilizations():
        set_growth_modifier(civ)
        set_production_modifier(civ)
        set_support_modifier(civ)
        set_city_cluster_modifier(civ)
        set_city_war_distance_modifier(civ)
        set_tech_preference_modifier(civ)


def set_modifier(civ, modifier, function):
    """Modifiers and functions are tuple."""
    if modifier is not None:
        function(civ.id, *modifier)


def set_growth_modifier(civ):
    # void setGrowthModifiers( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop );
    # iInitPop is the initial population in a city, also can use gc.setInitialPopulation( iCiv, iInitPop ) to change a single civ
    # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100, 1 )
    # 3Miro: ABOUT CULTURE notice the culture modifier is different from the others, it modifies the culture output as opposed to the culture threshold
    # 	50 means less culture, 200 means more culture. This is applied to Culture output of 10 or more.
    human_modifier = civ.human.modifiers.get(Modifier.GROWTH)
    ai_modifier = civ.ai.modifiers.get(Modifier.GROWTH)
    set_modifier(civ, human_modifier, gc.setGrowthModifiersHu)
    set_modifier(civ, ai_modifier, gc.setGrowthModifiersAI)


def set_production_modifier(civ):
    # void setProductionModifiers( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch );
    # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100 )
    # 3Miro: at 100 research cost, the cost is exactly as in the XML files, the cost in general is however increased for all civs
    human_modifier = civ.human.modifiers.get(Modifier.PRODUCTION)
    ai_modifier = civ.ai.modifiers.get(Modifier.PRODUCTION)
    set_modifier(civ, human_modifier, gc.setProductionModifiersHu)
    set_modifier(civ, ai_modifier, gc.setProductionModifiersAI)


def set_support_modifier(civ):
    # void setSupportModifiers( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic );
    # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100 )
    # note that iCityNum also gets an additional modifier based on population in the city
    # note that the base for inflation is modified by turn number (among many other things)
    human_modifier = civ.human.modifiers.get(Modifier.SUPPORT)
    ai_modifier = civ.ai.modifiers.get(Modifier.SUPPORT)
    set_modifier(civ, human_modifier, gc.setSupportModifiersHu)
    set_modifier(civ, ai_modifier, gc.setSupportModifiersAI)


def set_city_cluster_modifier(civ):
    # 3Miro: setCityClusterAI(iCiv,iTop,iBottom,iMinus) for each AI civilization (set them for all, but only the AI make difference)
    # this determines how clustered the cities would be
    # AI_foundValue in PlayerAI would compute for a candidate city location the number of plots that are taken (i.e. by another city)
    # in CivIV, if more than a third of the tiles are "taken", do not found city there. In RFC, cities are clustered closer
    # if ( iTaken > 21 * iTop / iBottom - iMinus ) do not build city there.
    # RFC default values are 2/3 -1 for Europe, 1/3 - 0 for Russia and 1/2 for Mongolia
    # for example gc.setCityClusterAI( iByzantium, 1, 3, 0 ) wouldn't allow Byzantium to settle cities if more than 7 tiles are taken
    ai_modifier = civ.ai.modifiers.get(Modifier.CITY_CLUSTER)
    if ai_modifier is not None:
        set_modifier(civ, ai_modifier, gc.setCityClusterAI)


def set_city_war_distance_modifier(civ):
    # 3Miro: setCityWarDistanceAI(iCiv,iVal), depending on the type of the empire, modify how likely the AI is to attack a city
    # values are 1 - small empires, 2 - large continuous empires, 3 - not necessarily continuous empires
    ai_modifier = civ.ai.modifiers.get(Modifier.CITY_WAR_DISTANCE)
    if ai_modifier is not None:
        gc.setCityWarDistanceAI(civ.id, ai_modifier)


def set_tech_preference_modifier(civ):
    # 3Miro: setTechPreferenceAI(iCiv,iTech,iVal), for each civ, for each tech, specify how likable it is. iVal is same as in growth.
    # low percent makes the tech less desirable
    ai_modifier = civ.ai.modifiers.get(Modifier.TECH_PREFERENCE)
    if ai_modifier is not None:
        for tech, value in ai_modifier:
            gc.setTechPreferenceAI(civ.id, tech, value)


def set_diplomacy_modifier():
    # 3Miro: setDiplomacyModifiers(iCiv1,iCiv2,iVal) hidden modifier for the two civ's AI relations. More likely to have OB and so on.
    # + means they will like each other - they will hate each other.
    # from Civ1 towards Civ2 (make them symmetric)
    for civ1, civ2, value in DIPLOMACY_MODIFIERS:
        gc.setDiplomacyModifiers(civ1, civ2, value)


def set_starting_workers():
    for civ in civilizations().majors():
        gc.setStartingWorkers(civ.id, civ.initial.workers)


def set_tech_timeline_modifier():
    gc.setTimelineTechModifiers(
        9, 25, -50, 1, 100, 50
    )  # go between 10 times slower and 4 times faster
    # formula is: iAhistoric = iCurrentTurn - iHistoricTurn, capped at ( iTPCap, iTBCap )
    # iCost *= 100 + topPenalty * iHistoric * iAhistoric / BotPenalty, iCost /= 100
    # iCost *= 100 - topBuff * iHistoric * iAhistoric / BotBuff, iCost /= 100


def set_initial_building():
    # gc.setInitialBuilding( iCiv, iBuilding, True\False ), if ( True) give iCiv, building iBuildings else don't Default is False
    # we can change True <-> False with the onTechAquire event
    for civ in civilizations():
        buildings = civ.initial.get("buildings")
        if buildings is not None:
            for building in buildings:
                gc.setInitialBuilding(civ.id, building, True)


def set_building_preferences():
    # use values -10 for very unlikely, 0 for default neutral and positive for desirable
    # values less than -10 might not work, above 10 should be fine
    # the getUniqueBuilding function does not work, probably the util functions are not yet usable when these initial values are set
    # but in the .dll these values are only used for the civ-specific building of the given buildingclass, so we can these add redundantly
    for civ in civilizations().majors():
        for building, preference in BUILDING_PREFERENCES:
            gc.setBuildingPref(civ.id, building, preference)

    for civ in civilizations():
        ai_modifier = civ.ai.modifiers.get(Modifier.BUILDING_PREFERENCE)
        if ai_modifier is not None:
            for building, value in ai_modifier:
                gc.setBuildingPref(civ.id, building, value)


def set_unique_powers():
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

    gc.setUP(Civ.BURGUNDY, UniquePower.HAPPINESS_BONUS, 1)
    gc.setUP(Civ.BURGUNDY, UniquePower.PER_CITY_COMMERCE_BONUS, 200)

    gc.setUP(Civ.BYZANTIUM, UniquePower.NO_COLLAPSE_IN_CORE_AND_NORMAL_AREAS, 1)
    gc.setUP(Civ.BYZANTIUM, UniquePower.PRE_ACCESS_CIVICS, Civic.IMPERIALISM)

    gc.setUP(Civ.FRANCE, UniquePower.LESS_INSTABILITY_WITH_FOREIGN_LAND, 1)

    gc.setUP(Civ.ARABIA, UniquePower.SPREAD_STATE_RELIGION_TO_NEW_CITIES, 1)

    gc.setUP(Civ.BULGARIA, UniquePower.NO_RESISTANCE, 0)

    gc.setUP(Civ.CORDOBA, UniquePower.PROMOTION_FOR_ALL_VALID_UNITS, Promotion.MEDIC)
    gc.setUP(Civ.CORDOBA, UniquePower.GROWTH_CITY_WITH_HEALTH_EXCESS, 50)

    gc.setUP(
        Civ.MOROCCO,
        UniquePower.TERRAIN_BONUS,
        1 * 100000 + Terrain.DESERT * 1000 + 10 + 1,
    )
    gc.setUP(
        Civ.MOROCCO,
        UniquePower.FEATURE_BONUS,
        1 * 100000 + Feature.OASIS * 1000 + 100 + 1,
    )

    gc.setUP(Civ.CASTILE, UniquePower.LESS_INSTABILITY_WITH_RELIGIOUS_PROSECUTION, 1)
    gc.setUP(Civ.CASTILE, UniquePower.PER_CITY_COMMERCE_BONUS, 2)

    gc.setUP(Civ.NORWAY, UniquePower.CAN_ENTER_TERRAIN, Terrain.OCEAN)
    gc.setUP(Civ.NORWAY, UniquePower.STABILITY_BONUS_FOUNDING, 1)  # "hidden" part of the UP

    gc.setUP(Civ.VENECIA, UniquePower.PRE_ACCESS_CIVICS, Civic.MERCHANT_REPUBLIC)

    gc.setUP(Civ.KIEV, UniquePower.CITY_TILE_YIELD_BONUS, 1 * 1000 + 100 * 2)

    gc.setUP(Civ.HUNGARY, UniquePower.HAPPINESS_BONUS, 1)
    gc.setUP(Civ.HUNGARY, UniquePower.NO_UNHAPPINESS_WITH_FOREIGN_CULTURE, 0)

    gc.setUP(
        Civ.GERMANY,
        UniquePower.FASTER_UNIT_PRODUCTION,
        Technology.GUNPOWDER * 100 + 75,
    )

    gc.setUP(Civ.POLAND, UniquePower.NO_INSTABILITY_WITH_FOREIGN_RELIGION, 0)

    gc.setUP(Civ.LITHUANIA, UniquePower.CULTURE_BONUS_WITH_NO_STATE_RELIGION, 200)
    gc.setUP(Civ.LITHUANIA, UniquePower.HAPPINESS_BONUS_WITH_NO_STATE_RELIGION, 1)

    gc.setSupportModifiersAI(Civ.MOSCOW, 10, 100, 20, 10, 100)  # sync with preset values
    gc.setSupportModifiersHu(Civ.MOSCOW, 10, 100, 20, 10, 100)  # sync with preset values
    gc.setUP(Civ.MOSCOW, UniquePower.LOWER_CITY_MAINTENANCE_COST, 50)

    gc.setUP(
        Civ.GENOA, UniquePower.HALVE_COST_OF_MERCENARIES, 1
    )  # Absinthe: this actually has no effect, it is implemented in Mercenaries.py entirely

    gc.setUP(
        Civ.SCOTLAND,
        UniquePower.IMPROVEMENT_BONUS,
        1 * 100000 + Improvement.FORT * 1000 + 2,
    )

    gc.setUP(
        Civ.ENGLAND,
        UniquePower.IMPROVEMENT_BONUS,
        1 * 100000 + Improvement.WORKSHOP * 1000 + 1,
    )
    gc.setUP(
        Civ.ENGLAND,
        UniquePower.IMPROVEMENT_BONUS_2,
        1 * 100000 + Improvement.COTTAGE * 1000 + 10,
    )
    gc.setUP(
        Civ.ENGLAND,
        UniquePower.IMPROVEMENT_BONUS_3,
        1 * 100000 + Improvement.HAMLET * 1000 + 10,
    )
    gc.setUP(
        Civ.ENGLAND,
        UniquePower.IMPROVEMENT_BONUS_4,
        1 * 100000 + Improvement.VILLAGE * 1000 + 10,
    )
    gc.setUP(
        Civ.ENGLAND,
        UniquePower.IMPROVEMENT_BONUS_5,
        1 * 100000 + Improvement.TOWN * 1000 + 10,
    )

    # Speed up East/West India Trading Companies and all Colonies
    gc.setUP(
        Civ.PORTUGAL,
        UniquePower.LOWER_COST_FOR_PROJECTS,
        (len(Project) - 2) * 1000000 + max(Colony) * 1000 + 30,
    )
    gc.setUP(Civ.PORTUGAL, UniquePower.STABILITY_BONUS_FOUNDING, 1)  # "hidden" part of the UP

    for i in civilizations().drop(Civ.BARBARIAN).ids():
        if not i == Civ.AUSTRIA:
            gc.setDiplomacyModifiers(i, Civ.AUSTRIA, +4)
    gc.setUP(Civ.AUSTRIA, UniquePower.PER_CITY_COMMERCE_BONUS, 200)

    gc.setUP(Civ.OTTOMAN, UniquePower.FREE_UNITS_WITH_FOREIGN_RELIGIONS, 1)

    gc.setUP(
        Civ.SWEDEN,
        UniquePower.PROMOTION_FOR_ALL_VALID_UNITS,
        Promotion.FORMATION,
    )

    gc.setUP(Civ.NOVGOROD, UniquePower.PRE_ACCESS_CIVICS, Civic.BUREAUCRACY)

    gc.setUP(Civ.PRUSSIA, UniquePower.PRE_ACCESS_CIVICS, Civic.THEOCRACY)
    # Absinthe: handled in python currently
    # gc.setUP( iPrussia, UniquePower.NO_INSTABILITY_WITH_CIVIC_AND_STATE_RELIGION_CHANGE, 1 )

    # Absinthe: handled in python currently
    # gc.setUP( iAragon, UniquePower.EXTRA_COMMERCE_BONUS, 0 )

    # Absinthe: handled in python currently
    # gc.setUP( iScotland, UniquePower.EXTRA_UNITS_WHEN_LOSING_CITY, 1 )

    gc.setUP(Civ.DUTCH, UniquePower.EXTRA_TRADE_ROUTES, 2)
    gc.setUP(
        Civ.DUTCH, UniquePower.IMPROVE_GAIN_FAITH_POINTS, 2
    )  # 3Miro: "hidden" buff to the Dutch FP, otherwise they have too little piety (not enough cities)
    gc.setUP(
        Civ.DUTCH,
        UniquePower.LOWER_COST_FOR_PROJECTS,
        (len(Project) - 2) * 1000000 + max(Colony) * 1000 + 30,
    )  # "hidden" part of the UP

    gc.setUP(Civ.POPE, UniquePower.NO_COLLAPSE_IN_CORE_AND_NORMAL_AREAS, 1)


def set_religion_spread_factor():
    for civ in civilizations():
        for religion, threshold in civ.religion.spreading_threshold.items():
            gc.setReligionSpread(civ.id, religion, threshold)


def set_religion_benefit():
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

    gc.setReligionBenefit(Religion.ORTHODOXY, FaithPointBonusCategory.BOOST_STABILITY, 10, 100)
    gc.setReligionBenefit(Religion.ORTHODOXY, FaithPointBonusCategory.REDUCE_CIVIC_UPKEEP, 50, 100)

    gc.setReligionBenefit(
        Religion.ISLAM, FaithPointBonusCategory.FASTER_POPULATION_GROWTH, 50, 100
    )
    gc.setReligionBenefit(Religion.ISLAM, FaithPointBonusCategory.REDUCING_COST_UNITS, 50, 100)

    gc.setReligionBenefit(
        Religion.PROTESTANTISM, FaithPointBonusCategory.REDUCING_TECH_COST, 30, 100
    )
    gc.setReligionBenefit(
        Religion.PROTESTANTISM, FaithPointBonusCategory.REDUCING_WONDER_COST, 30, 100
    )

    gc.setReligionBenefit(Religion.CATHOLICISM, FaithPointBonusCategory.BOOST_DIPLOMACY, 6, 100)
    gc.setReligionBenefit(Religion.ISLAM, FaithPointBonusCategory.BOOST_DIPLOMACY, 5, 100)
    gc.setReligionBenefit(Religion.PROTESTANTISM, FaithPointBonusCategory.BOOST_DIPLOMACY, 4, 100)
    gc.setReligionBenefit(Religion.ORTHODOXY, FaithPointBonusCategory.BOOST_DIPLOMACY, 3, 100)


def set_historical_enemies():
    # 3Miro: be very careful here, this can really mess the AI
    # 	setHistoricalEnemyAICheat( iAttacker, iDefender, 10 ) gives the attacker +10% bonus, when attacked units belong to the defender
    # 	this modifier only works in AI vs AI battles, it's ignored if either player is Human
    # 	none of the AI players is "aware" of the modification, if you make it too big, it could lead to a couple strange situations
    # 	(where the AI has clear advantage in a battle, yet it still won't attack)
    # 	so this should be a "last resort" solution, other methods are always preferable
    for civ1, civ2, value in HISTORICAL_ENEMIES:
        gc.setHistoricalEnemyAICheat(civ1, civ2, value)
        gc.setHistoricalEnemyAICheat(civ2, civ1, -value)


def set_other_parameters():
    gc.setGlobalWarming(False)

    # Set FastTerrain (i.e. double movement over ocean)
    gc.setFastTerrain(Terrain.OCEAN)

    # set the religions and year of the great schism
    gc.setSchism(Religion.CATHOLICISM, Religion.ORTHODOXY, DateTurn.i1053AD)
    gc.setHoliestCity(*CITIES[City.JERUSALEM])

    # 3Miro: set the Jews as the minor Religion
    gc.setMinorReligion(Religion.JUDAISM)
    gc.setMinorReligionRefugies(0)

    # 3Miro: Psycho AI cheat, this will make Ottoman AI think it can win battles vs Constantinople at 90/100 rate
    # 	it will also actually boost the Ottoman's odds (actually lower the defenders chance by 20 percent), but only when attacking Constantinople
    gc.setPsychoAICheat(Civ.OTTOMAN, *CITIES[City.CONSTANTINOPLE])

    # 3Miro: this sets rules on how players can Vassalize, first two parameters are the players (we should probably keep this symmetric)
    # 	if the third parameter is -1: cannot Vassalize, 0: has to satisfy a condition (default), 1 can Vassalize without conditions
    # 	the condition is that either one of the players needs to have a city in a province that the other players considers >= the last parameter
    # 	the default for the last parameter is 0, we should call this at least once to set the parameter (it is the same for all players)
    gc.setVassalagaeCondition(Civ.CORDOBA, Civ.ARABIA, 1, ProvinceType.CONTESTED)
    gc.setVassalagaeCondition(Civ.ARABIA, Civ.CORDOBA, 1, ProvinceType.CONTESTED)

    # block foundation of Protestantism except by a Catholic player
    gc.setParentSchismReligions(Religion.CATHOLICISM, Religion.PROTESTANTISM)

    # block declaration of war against newly spawning nations for this many turns (pre-set wars are not affected)
    gc.setPaceTurnsAfterSpawn(5)

    gc.setProsecutorReligions(Unit.PROSECUTOR, PROSECUTOR_UNITCLASS)
    gc.setSaintParameters(
        Unit.GREAT_PROPHET, GREAT_PROPHET_FAITH_POINT_BONUS, 20, 40
    )  # try to amass at least 20 and don't bother above 40 points
    gc.setIndependnets(
        min(civilizations().independents().ids()),
        max(civilizations().independents().ids()),
        Civ.BARBARIAN,
    )
    gc.setPapalPlayer(Civ.POPE, Religion.CATHOLICISM)

    # 3MiroMercs: set the merc promotion
    gc.setMercPromotion(Promotion.MERC)
