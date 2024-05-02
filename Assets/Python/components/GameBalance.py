from CvPythonExtensions import *
from CoreData import civilizations, civilization
from Consts import WORLD_WIDTH, WORLD_HEIGHT
from CoreStructures import year
from CoreTypes import (
    Modifier,
    Building,
    City,
    Civ,
    Civic,
    Colony,
    Feature,
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
)
from ProvinceMapData import PROVINCES_MAP
from MiscData import (
    DIPLOMACY_MODIFIERS,
    HISTORICAL_ENEMIES,
    GREAT_PROPHET_FAITH_POINT_BONUS,
    PROSECUTOR_UNITCLASS,
)
from TimelineData import TIMELINE_TECH_MODIFIER, DateTurn
from SettlerMapData import SETTLERS_MAP
from LocationsData import CITIES
from WarMapData import WARS_MAP

gc = CyGlobalContext()  # LOQ


class GameBalance:
    def setBalanceParameters(self):
        self.setModifiers()
        self.setDiplomacyModifier()
        self.setTechTimeline()
        self.setInitialBuilding()
        self.setBuildingPreferences()
        self.setUniquePowers()
        self.setReligionSpreadFactor()
        self.setReligionBenefit()
        self.setHistoricalEnemies()
        self.setProvinceTypeParameters()
        self.setOtherParameters()
        self.set_starting_workers()

    def setModifiers(self):
        for civ in civilizations():
            self.setGrowthModifier(civ)
            self.setProductionModifier(civ)
            self.setSupportModifier(civ)
            self.setCityClusterModifier(civ)
            self.setCityWarDistanceModifier(civ)
            self.setTechPreferenceModifier(civ)

    def _setModifier(self, civ, modifier, function):
        """Modifiers and functions are tuple."""
        if modifier is not None:
            function(civ.id, *modifier)

    def setGrowthModifier(self, civ):
        # void setGrowthModifiers( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop );
        # iInitPop is the initial population in a city, also can use gc.setInitialPopulation( iCiv, iInitPop ) to change a single civ
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100, 1 )
        # 3Miro: ABOUT CULTURE notice the culture modifier is different from the others, it modifies the culture output as opposed to the culture threshold
        # 	50 means less culture, 200 means more culture. This is applied to Culture output of 10 or more.
        human_modifier = civ.human.modifiers.get(Modifier.GROWTH)
        ai_modifier = civ.ai.modifiers.get(Modifier.GROWTH)
        self._setModifier(civ, human_modifier, gc.setGrowthModifiersHu)
        self._setModifier(civ, ai_modifier, gc.setGrowthModifiersAI)

    def setProductionModifier(self, civ):
        # void setProductionModifiers( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch );
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100 )
        # 3Miro: at 100 research cost, the cost is exactly as in the XML files, the cost in general is however increased for all civs
        human_modifier = civ.human.modifiers.get(Modifier.PRODUCTION)
        ai_modifier = civ.ai.modifiers.get(Modifier.PRODUCTION)
        self._setModifier(civ, human_modifier, gc.setProductionModifiersHu)
        self._setModifier(civ, ai_modifier, gc.setProductionModifiersAI)

    def setSupportModifier(self, civ):
        # void setSupportModifiers( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic );
        # defaults (i.e. no effect) ( iCiv, 100, 100, 100, 100, 100 )
        # note that iCityNum also gets an additional modifier based on population in the city
        # note that the base for inflation is modified by turn number (among many other things)
        human_modifier = civ.human.modifiers.get(Modifier.SUPPORT)
        ai_modifier = civ.ai.modifiers.get(Modifier.SUPPORT)
        self._setModifier(civ, human_modifier, gc.setSupportModifiersHu)
        self._setModifier(civ, ai_modifier, gc.setSupportModifiersAI)

    def setCityClusterModifier(self, civ):
        # 3Miro: setCityClusterAI(iCiv,iTop,iBottom,iMinus) for each AI civilization (set them for all, but only the AI make difference)
        # this determines how clustered the cities would be
        # AI_foundValue in PlayerAI would compute for a candidate city location the number of plots that are taken (i.e. by another city)
        # in CivIV, if more than a third of the tiles are "taken", do not found city there. In RFC, cities are clustered closer
        # if ( iTaken > 21 * iTop / iBottom - iMinus ) do not build city there.
        # RFC default values are 2/3 -1 for Europe, 1/3 - 0 for Russia and 1/2 for Mongolia
        # for example gc.setCityClusterAI( iByzantium, 1, 3, 0 ) wouldn't allow Byzantium to settle cities if more than 7 tiles are taken
        ai_modifier = civ.ai.modifiers.get(Modifier.CITY_CLUSTER)
        if ai_modifier is not None:
            self._setModifier(civ, ai_modifier, gc.setCityClusterAI)

    def setCityWarDistanceModifier(self, civ):
        # 3Miro: setCityWarDistanceAI(iCiv,iVal), depending on the type of the empire, modify how likely the AI is to attack a city
        # values are 1 - small empires, 2 - large continuous empires, 3 - not necessarily continuous empires
        ai_modifier = civ.ai.modifiers.get(Modifier.CITY_WAR_DISTANCE)
        if ai_modifier is not None:
            gc.setCityWarDistanceAI(civ.id, ai_modifier)

    def setTechPreferenceModifier(self, civ):
        # 3Miro: setTechPreferenceAI(iCiv,iTech,iVal), for each civ, for each tech, specify how likable it is. iVal is same as in growth.
        # low percent makes the tech less desirable
        ai_modifier = civ.ai.modifiers.get(Modifier.TECH_PREFERENCE)
        if ai_modifier is not None:
            for tech, value in ai_modifier:
                gc.setTechPreferenceAI(civ.id, tech.value, value)

    def setDiplomacyModifier(self):
        # 3Miro: setDiplomacyModifiers(iCiv1,iCiv2,iVal) hidden modifier for the two civ's AI relations. More likely to have OB and so on.
        # + means they will like each other - they will hate each other.
        # from Civ1 towards Civ2 (make them symmetric)
        for civ1, civ2, value in DIPLOMACY_MODIFIERS:
            gc.setDiplomacyModifiers(civ1.value, civ2.value, value)

    def setTechTimeline(self):
        gc.setTimelineTechModifiers(
            9, 25, -50, 1, 100, 50
        )  # go between 10 times slower and 4 times faster
        # formula is: iAhistoric = iCurrentTurn - iHistoricTurn, capped at ( iTPCap, iTBCap )
        # iCost *= 100 + topPenalty * iHistoric * iAhistoric / BotPenalty, iCost /= 100
        # iCost *= 100 - topBuff * iHistoric * iAhistoric / BotBuff, iCost /= 100
        for tech, turn in TIMELINE_TECH_MODIFIER:
            gc.setTimelineTechDateForTech(tech.value, year(turn))

    def setInitialBuilding(self):
        # gc.setInitialBuilding( iCiv, iBuilding, True\False ), if ( True) give iCiv, building iBuildings else don't Default is False
        # we can change True <-> False with the onTechAquire event
        for civ in civilizations():
            buildings = civ.initial.get("buildings")
            if buildings is not None:
                for building in buildings:
                    gc.setInitialBuilding(civ.id, building.value, True)

    def setBuildingPreferences(self):
        # use values -10 for very unlikely, 0 for default neutral and positive for desirable
        # values less than -10 might not work, above 10 should be fine
        # the getUniqueBuilding function does not work, probably the util functions are not yet usable when these initial values are set
        # but in the .dll these values are only used for the civ-specific building of the given buildingclass, so we can these add redundantly
        for civ in civilizations().majors():
            gc.setBuildingPref(civ.id, Building.WALLS.value, 5)
            gc.setBuildingPref(civ.id, Building.CASTLE.value, 7)
            gc.setBuildingPref(civ.id, Building.MANOR_HOUSE.value, 5)
            gc.setBuildingPref(civ.id, Building.COURTHOUSE.value, 5)
            gc.setBuildingPref(civ.id, Building.NIGHT_WATCH.value, 3)
            gc.setBuildingPref(civ.id, Building.MOROCCO_KASBAH.value, 5)
            gc.setBuildingPref(civ.id, Building.MOSCOW_KREMLIN.value, 7)
            gc.setBuildingPref(civ.id, Building.HUNGARIAN_STRONGHOLD.value, 7)
            gc.setBuildingPref(civ.id, Building.SPANISH_CITADEL.value, 7)
            gc.setBuildingPref(civ.id, Building.FRENCH_CHATEAU.value, 5)
            gc.setBuildingPref(civ.id, Building.VENICE_NAVAL_BASE.value, 5)
            gc.setBuildingPref(civ.id, Building.KIEV_VECHE.value, 5)
            gc.setBuildingPref(civ.id, Building.HOLY_ROMAN_RATHAUS.value, 5)
            gc.setBuildingPref(civ.id, Building.LITHUANIAN_VOIVODESHIP.value, 5)
            gc.setBuildingPref(civ.id, Building.SWEDISH_TENNANT.value, 3)

        for civ in civilizations():
            ai_modifier = civ.ai.modifiers.get(Modifier.BUILDING_PREFERENCE)
            if ai_modifier is not None:
                for building, value in ai_modifier:
                    gc.setBuildingPref(civ.id, building.value, value)

    def setUniquePowers(self):
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

    def setReligionSpreadFactor(self):
        for civ in civilizations():
            for religion, threshold in civ.religion.spreading_threshold.items():
                gc.setReligionSpread(civ.id, religion.value, threshold)

    def setReligionBenefit(self):
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

    def setHistoricalEnemies(self):
        # 3Miro: be very careful here, this can really mess the AI
        # 	setHistoricalEnemyAICheat( iAttacker, iDefender, 10 ) gives the attacker +10% bonus, when attacked units belong to the defender
        # 	this modifier only works in AI vs AI battles, it's ignored if either player is Human
        # 	none of the AI players is "aware" of the modification, if you make it too big, it could lead to a couple strange situations
        # 	(where the AI has clear advantage in a battle, yet it still won't attack)
        # 	so this should be a "last resort" solution, other methods are always preferable
        for civ1, civ2, value in HISTORICAL_ENEMIES:
            gc.setHistoricalEnemyAICheat(civ1.value, civ2.value, value)

    def setProvinceTypeParameters(self):
        # How much culture should we get into a province of this type, ignore the war and settler values (0,0)
        gc.setProvinceTypeParams(ProvinceType.NONE.value, 0, 0, 1, 3)  # 1/3 culture
        gc.setProvinceTypeParams(ProvinceType.CONTESTED.value, 0, 0, 1, 1)  # no change to culture
        gc.setProvinceTypeParams(ProvinceType.POTENTIAL.value, 0, 0, 1, 1)  # same as outer culture
        gc.setProvinceTypeParams(ProvinceType.HISTORICAL.value, 0, 0, 2, 1)  # double-culture
        gc.setProvinceTypeParams(ProvinceType.CORE.value, 0, 0, 3, 1)  # triple-culture

    def setOtherParameters(self):
        gc.setGlobalWarming(False)

        # Set FastTerrain (i.e. double movement over ocean)
        gc.setFastTerrain(Terrain.OCEAN.value)

        # set the religions and year of the great schism
        gc.setSchism(Religion.CATHOLICISM.value, Religion.ORTHODOXY.value, DateTurn.i1053AD)
        gc.setHoliestCity(*CITIES[City.JERUSALEM])

        # 3Miro: set the Jews as the minor Religion
        gc.setMinorReligion(Religion.JUDAISM.value)
        gc.setMinorReligionRefugies(0)

        # 3Miro: Psycho AI cheat, this will make Ottoman AI think it can win battles vs Constantinople at 90/100 rate
        # 	it will also actually boost the Ottoman's odds (actually lower the defenders chance by 20 percent), but only when attacking Constantinople
        gc.setPsychoAICheat(Civ.OTTOMAN.value, *civilization(Civ.BYZANTIUM).location.capital)

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

        # block foundation of Protestantism except by a Catholic player
        gc.setParentSchismReligions(Religion.CATHOLICISM.value, Religion.PROTESTANTISM.value)

        # block declaration of war against newly spawning nations for this many turns (pre-set wars are not affected)
        gc.setPaceTurnsAfterSpawn(5)

    def setProvinceTypes(self):
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
        for civ in civilizations().majors():
            for y in range(WORLD_HEIGHT):
                for x in range(WORLD_WIDTH):
                    gc.setSettlersMap(civ.id, y, x, SETTLERS_MAP[civ.key][y][x])
                    gc.setWarsMap(civ.id, y, x, WARS_MAP[civ.key][y][x])

        for y in range(WORLD_HEIGHT):
            for x in range(WORLD_WIDTH):
                if PROVINCES_MAP[y][x] > -1:
                    # "no province" of ocean is settled different than -1, set only non-negative values,
                    # the C++ map is initialized to "no-province" by setSizeNPlayers(...)
                    # "no-province" is returned as -1 via the Cy interface
                    gc.setProvince(x, y, PROVINCES_MAP[y][x])
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
                core_tile_min[0],
                core_tile_min[1],
                core_tile_max[0],
                core_tile_max[1],
                normal_tile_min[0],
                normal_tile_min[1],
                normal_tile_max[0],
                normal_tile_max[1],
                len(core_additional_tiles),
                len(normal_exception_tiles),
            )
            for tile in core_additional_tiles:
                gc.addCoreException(civ.id, *tile)
            for tile in normal_exception_tiles:
                gc.addNormalException(civ.id, *tile)

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

    def set_starting_workers(self):
        for civ in civilizations().majors():
            gc.setStartingWorkers(civ.id, civ.initial.workers)
