#include "CvGameCoreDLL.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CyArea.h"
#include "CvInfos.h"

//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>

//
// published python interface for CyCity
//

void CyCityPythonInterface1(python::class_<CyCity> &x)
{
  OutputDebugString("Python Extension Module - CyCityPythonInterface1\n");

  x.def("isNone", &CyCity::isNone, "void () - is the instance valid?")
      .def("kill", &CyCity::kill, "void () - kill the city")
      .def("doTask", &CyCity::doTask,
           "void (int eTaskTypes, int iData1, int iData2, bool bOption) - Enacts the TaskType passed")
      .def("chooseProduction", &CyCity::chooseProduction,
           "void (int /*UnitTypes*/ eTrainUnit, int /*BuildingTypes*/ eConstructBuilding, int /*ProjectTypes*/ "
           "eCreateProject, bool bFinish, bool bFront) - Chooses production for a city")

      .def("createGreatPeople", &CyCity::createGreatPeople,
           "void (int /*UnitTypes*/ eGreatPersonUnit, bool bIncrementThreshold) - Creates a great person in this city "
           "and whether it should increment the threshold to the next level")

      .def("getCityPlotIndex", &CyCity::getCityPlotIndex, "int (CyPlot* pPlot)")
      .def("getCityIndexPlot", &CyCity::getCityIndexPlot, python::return_value_policy<python::manage_new_object>(),
           "CyPlot* (int iIndex)")
      .def("canWork", &CyCity::canWork, "bool (CyPlot*) - can the city work the plot?")
      .def("clearWorkingOverride", &CyCity::clearWorkingOverride, "void (int iIndex)")
      .def("countNumImprovedPlots", &CyCity::countNumImprovedPlots, "int ()")
      .def("countNumWaterPlots", &CyCity::countNumWaterPlots, "int ()")
      .def("countNumRiverPlots", &CyCity::countNumRiverPlots, "int ()")

      .def("findPopulationRank", &CyCity::findPopulationRank, "int ()")
      .def("findBaseYieldRateRank", &CyCity::findBaseYieldRateRank, "int (int /*YieldTypes*/ eYield)")
      .def("findYieldRateRank", &CyCity::findYieldRateRank, "int (int /*YieldTypes*/ eYield)")
      .def("findCommerceRateRank", &CyCity::findCommerceRateRank, "int (int /*CommerceTypes*/ eCommerce)")

      .def("allUpgradesAvailable", &CyCity::allUpgradesAvailable, "int UnitTypes (int eUnit, int iUpgradeCount)")
      .def("isWorldWondersMaxed", &CyCity::isWorldWondersMaxed, "bool ()")
      .def("isTeamWondersMaxed", &CyCity::isTeamWondersMaxed, "bool ()")
      .def("isNationalWondersMaxed", &CyCity::isNationalWondersMaxed, "bool ()")
      .def("isBuildingsMaxed", &CyCity::isBuildingsMaxed, "bool ()")
      .def("canTrain", &CyCity::canTrain, "bool (int eUnit, bool bContinue, bool bTestVisible)")
      .def("canConstruct", &CyCity::canConstruct,
           "bool (int eBuilding, bool bContinue, bool bTestVisible, bool bIgnoreCost)")
      .def("canCreate", &CyCity::canCreate, "bool (int eProject, bool bContinue, bool bTestVisible)")
      .def("canMaintain", &CyCity::canMaintain, "bool (int eProcess, bool bContinue)")
      .def("canJoin", &CyCity::canJoin, "bool () - can a Great Person join the city")
      .def("getFoodTurnsLeft", &CyCity::getFoodTurnsLeft, "int () - how many food turns remain?")
      .def("isProduction", &CyCity::isProduction, "bool () - is city producing?")
      .def("isProductionLimited", &CyCity::isProductionLimited, "bool ()")
      .def("isProductionUnit", &CyCity::isProductionUnit, "bool () - is city training a unit?")
      .def("isProductionBuilding", &CyCity::isProductionBuilding, "bool () - is city constructing a building?")
      .def("isProductionProject", &CyCity::isProductionProject, "bool ()")
      .def("isProductionProcess", &CyCity::isProductionProcess, "bool () - is city maintaining a process?")

      .def("canContinueProduction", &CyCity::canContinueProduction, "bool (OrderData order)")
      .def("getProductionExperience", &CyCity::getProductionExperience, "int (int /*UnitTypes*/ eUnit)")
      .def("addProductionExperience", &CyCity::addProductionExperience, "void (CyUnit* pUnit, bool bConscript)")

      .def("getProductionUnit", &CyCity::getProductionUnit, "UnitID () - ID for unit that is being trained")
      .def("getProductionUnitAI", &CyCity::getProductionUnitAI, "int eUnitAIType ()")
      .def("getProductionBuilding", &CyCity::getProductionBuilding,
           "BuildingID () - ID for building that is under construction")
      .def("getProductionProject", &CyCity::getProductionProject, "int /*ProjectTypes*/ ()")
      .def("getProductionProcess", &CyCity::getProductionProcess, "int /*ProcessTypes*/ ()")
      .def("getProductionName", &CyCity::getProductionName, "str () - description of item that the city is working on")
      .def("getGeneralProductionTurnsLeft", &CyCity::getGeneralProductionTurnsLeft,
           "int - # of production turns left for the top order node item in a city...")
      .def("getProductionNameKey", &CyCity::getProductionNameKey,
           "str () - description of item that the city is working on")
      .def("isFoodProduction", &CyCity::isFoodProduction,
           "bool () - is item under construction being created with food instead of production?")
      .def("getFirstUnitOrder", &CyCity::getFirstUnitOrder, "int (int /*UnitTypes*/ eUnit)")
      .def("getFirstBuildingOrder", &CyCity::getFirstBuildingOrder, "int (int /*BuildingTypes*/ eBuilding)")
      .def("getFirstProjectOrder", &CyCity::getFirstProjectOrder, "int (int /*ProjectTypes*/ eProject)")
      .def("isUnitFoodProduction", &CyCity::isUnitFoodProduction,
           "bool (UnitID) - does UnitID require food to be trained?")
      .def("getProduction", &CyCity::getProduction,
           "int () - returns the current production towards whatever is top of this city's OrderQueue")
      .def("getProductionNeeded", &CyCity::getProductionNeeded,
           "int () - # of production needed to complete construction")
      .def("getProductionTurnsLeft", &CyCity::getProductionTurnsLeft,
           "int () - # of turns remaining until item is completed")
      .def("getUnitProductionTurnsLeft", &CyCity::getUnitProductionTurnsLeft,
           "int (UnitID, int iNum) - # of turns remaining to complete UnitID")
      .def("getBuildingProductionTurnsLeft", &CyCity::getBuildingProductionTurnsLeft,
           "int (BuildingID, int iNum) - # of turns remaining to complete UnitID")
      .def("getProjectProductionTurnsLeft", &CyCity::getProjectProductionTurnsLeft,
           "int (int /*ProjectTypes*/ eProject, int iNum)")
      .def("setProduction", &CyCity::setProduction, "void (int iNewValue)")
      .def("changeProduction", &CyCity::changeProduction, "void (int iChange)")
      .def("getProductionModifier", &CyCity::getProductionModifier,
           "int () - multiplier (if any) for item being produced")
      .def("getCurrentProductionDifference", &CyCity::getCurrentProductionDifference,
           "int (bool bIgnoreFood, bool bOverflow)")
      .def("getUnitProductionModifier", &CyCity::getUnitProductionModifier,
           "int (UnitID) - production multiplier for UnitID")
      .def("getBuildingProductionModifier", &CyCity::getBuildingProductionModifier,
           "int (BuildingID) - production multiplier for BuildingID")
      .def("getProjectProductionModifier", &CyCity::getProductionModifier, "int (int /*ProjectTypes*/ eProject)")

      .def("getExtraProductionDifference", &CyCity::getExtraProductionDifference, "int (int iExtra)")

      .def("canHurry", &CyCity::canHurry,
           "bool (HurryTypes eHurry, bool bTestVisible = 0) - can player eHurry in this city?")
      .def("hurry", &CyCity::hurry, "void (HurryTypes eHurry) - forces the city to rush production using eHurry")
      .def("getConscriptUnit", &CyCity::getConscriptUnit, "UnitID () - UnitID for the best unit the city can conscript")
      .def("getConscriptPopulation", &CyCity::getConscriptPopulation, "int ()")
      .def("conscriptMinCityPopulation", &CyCity::conscriptMinCityPopulation, "int ()")
      .def("flatConscriptAngerLength", &CyCity::flatConscriptAngerLength, "int ()")
      .def("canConscript", &CyCity::canConscript, "bool () - can the city conscript units?")
      .def("conscript", &CyCity::conscript, "void () - conscripts a unit")
      .def("getBonusHealth", &CyCity::getBonusHealth, "int (BonusID) - total health bonus from BonusID")
      .def("getBonusHappiness", &CyCity::getBonusHappiness, "int (BonusID) - total happiness bonus from BonusID")
      .def("getBonusPower", &CyCity::getBonusPower, "int (int /*BonusTypes*/ eBonus, bool bDirty)")
      .def("getBonusYieldRateModifier", &CyCity::getBonusYieldRateModifier,
           "int (int /*YieldTypes*/ eIndex, int /*BonusTypes*/ eBonus)")
      .def("getHandicapType", &CyCity::getHandicapType, "HandicapType () - owners difficulty level")
      .def("getCivilizationType", &CyCity::getCivilizationType, "CivilizationID () - owners CivilizationID")
      .def("getPersonalityType", &CyCity::getPersonalityType, "int /*LeaderHeadTypes*/ ()")
      .def("getArtStyleType", &CyCity::getArtStyleType, "int /*ArtStyleTypes*/ ()")
      .def("getCitySizeType", &CyCity::getCitySizeType, "int /*CitySizeTypes*/ ()")

      .def("hasTrait", &CyCity::hasTrait, "bool (TraitID) - does owner have TraitID?")
      .def("isBarbarian", &CyCity::isBarbarian, "bool () - is owner a barbarian?")
      .def("isHuman", &CyCity::isHuman, "bool () - is owner human?")
      .def("isVisible", &CyCity::isVisible, "bool (int /*TeamTypes*/ eTeam, bool bDebug)")

      .def("isCapital", &CyCity::isCapital, "bool () - is city the owners capital?")
      .def("isCoastal", &CyCity::isCoastal, "bool (int) - is the city on the coast?")
      .def("isCoastalOld", &CyCity::isCoastalOld, "bool () - is the city on the coast?") //Rhye
      .def("isDisorder", &CyCity::isDisorder, "bool () - is the city in disorder?")
      .def("isHolyCityByType", &CyCity::isHolyCityByType, "bool (ReligionID) - is the city ReligionID's holy city?")
      .def("isHolyCity", &CyCity::isHolyCity, "bool () - is the city ReligionID's holy city?")
      .def("isHeadquartersByType", &CyCity::isHeadquartersByType,
           "bool (CorporationID) - is the city CorporationID's headquarters?")
      .def("isHeadquarters", &CyCity::isHeadquarters, "bool () - is the city CorporationID's headquarters?")
      .def("getOvercrowdingPercentAnger", &CyCity::getOvercrowdingPercentAnger, "int (iExtra)")
      .def("getNoMilitaryPercentAnger", &CyCity::getNoMilitaryPercentAnger, "int ()")
      .def("getCulturePercentAnger", &CyCity::getCulturePercentAnger, "int ()")
      .def("getReligionPercentAnger", &CyCity::getReligionPercentAnger, "int ()")
      .def("getWarWearinessPercentAnger", &CyCity::getWarWearinessPercentAnger, "int ()")
      .def("getLargestCityHappiness", &CyCity::getLargestCityHappiness, "int ()")
      .def("unhappyLevel", &CyCity::unhappyLevel, "int (int iExtra)")
      .def("happyLevel", &CyCity::happyLevel, "int ()")
      .def("angryPopulation", &CyCity::angryPopulation, "int (iExtra) - # of unhappy citizens")
      .def("totalFreeSpecialists", &CyCity::totalFreeSpecialists)
      .def("extraFreeSpecialists", &CyCity::extraFreeSpecialists, "int () - # of specialist that are allowed for free")
      .def("extraPopulation", &CyCity::extraPopulation, "int () - # of extra/available citizens")
      .def("extraSpecialists", &CyCity::extraSpecialists, "int () - # of extra/available specialists")
      .def("unhealthyPopulation", &CyCity::unhealthyPopulation, "int (bool bNoAngry), int (iExtra)")
      .def("totalGoodBuildingHealth", &CyCity::totalGoodBuildingHealth, "int ()")
      .def("totalBadBuildingHealth", &CyCity::totalBadBuildingHealth, "int ()")
      .def("goodHealth", &CyCity::goodHealth, "int () - total health")
      .def("badHealth", &CyCity::badHealth, "int (bool bNoAngry) - total unhealthiness")
      .def("healthRate", &CyCity::healthRate, "int (bool bNoAngry, int iExtra)")
      .def("foodConsumption", &CyCity::foodConsumption, "int (bool bNoAngry, int iExtra)")
      .def("foodDifference", &CyCity::foodDifference,
           "int (bool bBottom) - result of getYieldRate(Food) - foodConsumption()")
      .def("growthThreshold", &CyCity::growthThreshold, "int () - value needed for growth")
      .def("productionLeft", &CyCity::productionLeft, "int () - result of (getProductionNeeded() - getProduction()")
      .def("hurryCost", &CyCity::hurryCost, "int (bool bExtra)")
      .def("hurryGold", &CyCity::hurryGold, "int (HurryID) - total value of gold when hurrying")
      .def("hurryPopulation", &CyCity::hurryPopulation, "int (HurryID) - value of each pop when hurrying")
      .def("hurryProduction", &CyCity::hurryProduction, "int (HurryID)")
      .def("flatHurryAngerLength", &CyCity::flatHurryAngerLength, "int ()")
      .def("hurryAngerLength", &CyCity::hurryAngerLength, "int (HurryID)")
      .def("maxHurryPopulation", &CyCity::maxHurryPopulation, "int ()")

      .def("cultureDistance", &CyCity::cultureDistance, "int (iDX, iDY) - culture distance")
      .def("cultureStrength", &CyCity::cultureStrength, "int (ePlayer)")
      .def("cultureGarrison", &CyCity::cultureGarrison, "int (ePlayer)")
      .def("hasBuilding", &CyCity::hasBuilding,
           "bool - (BuildingID) - does city have BuildingID (real or free)?") //Rhye
      .def("hasActiveBuilding", &CyCity::hasActiveBuilding,
           "bool (BuildingID) - is BuildingID active in the city (present & not obsolete)?") //Rhye
      .def("getNumBuilding", &CyCity::getNumBuilding,
           "int - (BuildingID) - How many BuildingID does this city have (real or free)?")
      .def("isHasBuilding", &CyCity::isHasBuilding,
           "bool (int iBuildingID) - This function actually no longer exists in C++, this is a helper function which "
           "hooks up to getNumBuilding() to help mod backwards compatibility")
      .def("getNumActiveBuilding", &CyCity::getNumActiveBuilding,
           "bool (BuildingID) - is BuildingID active in the city (present & not obsolete)?")
      .def("getID", &CyCity::getID,
           "int () - index ID # for the city - use with pPlayer.getCity(ID) to obtain city instance")
      .def("getX", &CyCity::getX, "int () - X coordinate for the cities plot")
      .def("getY", &CyCity::getY, "int () - Y coordinate for the cities plot")
      .def("at", &CyCity::at, "bool (iX, iY) - is the city at (iX, iY) ?")
      .def("atPlot", &CyCity::atPlot, "bool (CyPlot) - is pPlot the cities plot?")
      .def("plot", &CyCity::plot, python::return_value_policy<python::manage_new_object>(),
           "CyPlot () - returns cities plot instance")
      .def("isConnectedTo", &CyCity::isConnectedTo,
           "bool (CyCity*) - is city connected to CyCity* via the Trade Network?")
      .def("isConnectedToCapital", &CyCity::isConnectedToCapital, "bool (iOwner) - connected to the capital?")
      .def("area", &CyCity::area, python::return_value_policy<python::manage_new_object>(),
           "CyArea() () - returns CyArea instance for location of city")
      .def("waterArea", &CyCity::waterArea, python::return_value_policy<python::manage_new_object>(), "CyArea* ()")
      .def("getRallyPlot", &CyCity::getRallyPlot, python::return_value_policy<python::manage_new_object>(),
           "CyPlot () - returns city's rally plot instance")
      .def("getGameTurnFounded", &CyCity::getGameTurnFounded, "int () - GameTurn the city was founded")

      .def("getGameTurnAcquired", &CyCity::getGameTurnAcquired, "int ()")
      .def("getPopulation", &CyCity::getPopulation, "int () - total city population")
      .def("setPopulation", &CyCity::setPopulation, "void (int iNewValue) - sets the city population to iNewValue")
      .def("changePopulation", &CyCity::changePopulation, "void (int iChange) - adjusts the city population by iChange")
      .def("getRealPopulation", &CyCity::getRealPopulation, "int () - total city population in \"real\" numbers")
      .def("getHighestPopulation", &CyCity::getHighestPopulation, "int () ")
      .def("setHighestPopulation", &CyCity::setHighestPopulation, "void (iNewValue)")
      .def("getWorkingPopulation", &CyCity::getWorkingPopulation, "int () - # of citizens who are working")
      .def("getSpecialistPopulation", &CyCity::getSpecialistPopulation, "int () - # of specialists")
      .def("getNumGreatPeople", &CyCity::getNumGreatPeople, "int () - # of great people who are joined to the city")
      .def("getBaseGreatPeopleRate", &CyCity::getBaseGreatPeopleRate, "int () - base great person rate")
      .def("getGreatPeopleRate", &CyCity::getGreatPeopleRate, "int () - total Great Person rate")
      .def("getTotalGreatPeopleRateModifier", &CyCity::getTotalGreatPeopleRateModifier, "int ()")
      .def("changeBaseGreatPeopleRate", &CyCity::changeBaseGreatPeopleRate)
      .def("getGreatPeopleProgress", &CyCity::getGreatPeopleProgress, "int () - current great person progress")
      .def("getGreatPeopleRateModifier", &CyCity::getGreatPeopleRateModifier, "int ()")
      // BUG - Building Additional Great People - start
      .def("getAdditionalGreatPeopleRateByBuilding", &CyCity::getAdditionalGreatPeopleRateByBuilding,
           "int (int /*BuildingTypes*/)")
      .def("getAdditionalBaseGreatPeopleRateByBuilding", &CyCity::getAdditionalBaseGreatPeopleRateByBuilding,
           "int (int /*BuildingTypes*/)")
      .def("getAdditionalGreatPeopleRateModifierByBuilding", &CyCity::getAdditionalGreatPeopleRateModifierByBuilding,
           "int (int /*BuildingTypes*/)")
      // BUG - Building Additional Great People - end
      .def("getNumWorldWonders", &CyCity::getNumWorldWonders, "int ()")
      .def("getNumTeamWonders", &CyCity::getNumTeamWonders, "int ()")
      .def("getNumNationalWonders", &CyCity::getNumNationalWonders, "int ()")
      .def("getNumBuildings", &CyCity::getNumBuildings, "int ()")
      .def("changeGreatPeopleProgress", &CyCity::changeGreatPeopleProgress,
           "void (int iChange) - adjusts great person progress by iChange")
      .def("isGovernmentCenter", &CyCity::isGovernmentCenter, "bool () - is city the government center?")
      // BUG - Building Saved Maintenance - start
      .def("getSavedMaintenanceByBuilding", &CyCity::getSavedMaintenanceByBuilding, "int (int /*BuildingTypes*/)")
      .def("getSavedMaintenanceTimes100ByBuilding", &CyCity::getSavedMaintenanceTimes100ByBuilding,
           "int (int /*BuildingTypes*/)")
      // BUG - Building Saved Maintenance - end
      .def("getMaintenance", &CyCity::getMaintenance, "int () - cities current maintenance cost")
      .def("getMaintenanceTimes100", &CyCity::getMaintenanceTimes100, "int () - cities current maintenance cost")
      .def("calculateDistanceMaintenance", &CyCity::calculateDistanceMaintenance, "int ()")
      .def("calculateDistanceMaintenanceTimes100", &CyCity::calculateDistanceMaintenanceTimes100, "int ()")
      .def("calculateNumCitiesMaintenance", &CyCity::calculateNumCitiesMaintenance, "int ()")
      .def("calculateNumCitiesMaintenanceTimes100", &CyCity::calculateNumCitiesMaintenanceTimes100, "int ()")
      .def("calculateColonyMaintenance", &CyCity::calculateColonyMaintenance, "int ()")
      .def("calculateColonyMaintenanceTimes100", &CyCity::calculateColonyMaintenanceTimes100, "int ()")
      .def("calculateCorporationMaintenance", &CyCity::calculateCorporationMaintenance, "int ()")
      .def("calculateCorporationMaintenanceTimes100", &CyCity::calculateCorporationMaintenanceTimes100, "int ()")
      .def("getMaintenanceModifier", &CyCity::getMaintenanceModifier,
           "int () - total value of the city maintenance modifier")
      .def("getWarWearinessModifier", &CyCity::getWarWearinessModifier)
      .def("getHurryAngerModifier", &CyCity::getHurryAngerModifier)
      .def("changeHealRate", &CyCity::changeHealRate,
           "void (int iChange) - changes the heal rate of this city to iChange")

      .def("getEspionageHealthCounter", &CyCity::getEspionageHealthCounter, "int ()")
      .def("changeEspionageHealthCounter", &CyCity::changeEspionageHealthCounter, "void (int iChange)")
      .def("getEspionageHappinessCounter", &CyCity::getEspionageHappinessCounter, "int ()")
      .def("changeEspionageHappinessCounter", &CyCity::changeEspionageHappinessCounter, "void (int iChange)")

      .def("getFreshWaterGoodHealth", &CyCity::getFreshWaterGoodHealth, "int ()")
      .def("getFreshWaterBadHealth", &CyCity::getFreshWaterBadHealth, "int ()")
      .def("getBuildingGoodHealth", &CyCity::getBuildingGoodHealth, "int ()")
      .def("getBuildingBadHealth", &CyCity::getBuildingBadHealth, "int ()")
      .def("getFeatureGoodHealth", &CyCity::getFeatureGoodHealth,
           "int () - returns the good health provided by the feature this city is built on")
      .def("getFeatureBadHealth", &CyCity::getFeatureBadHealth,
           "int () - returns the bad health provided by the feature this city is built on")
      .def("getBuildingHealth", &CyCity::getBuildingHealth, "int (int eBuilding)")
      // BUG - Building Additional Health - start
      .def("getAdditionalHealthByBuilding", &CyCity::getAdditionalHealthByBuilding,
           "int (int /*BuildingTypes*/ eBuilding) - additional healthiness minus additional unhealthiness")
      .def("getAdditionalGoodHealthByBuilding", &CyCity::getAdditionalGoodHealthByBuilding,
           "int (int /*BuildingTypes*/ eBuilding) - additional healthiness")
      .def("getAdditionalBadHealthByBuilding", &CyCity::getAdditionalBadHealthByBuilding,
           "int (int /*BuildingTypes*/ eBuilding) - additional unhealthiness")
      .def("getAdditionalSpiledFoodByBuilding", &CyCity::getAdditionalSpoiledFoodByBuilding,
           "int (int /*BuildingTypes*/ eBuilding) - additional spoiled food")
      // BUG - Building Additional Health - end
      .def("getPowerGoodHealth", &CyCity::getPowerGoodHealth, "int ()")
      .def("getPowerBadHealth", &CyCity::getPowerBadHealth, "int ()")
      .def("getBonusGoodHealth", &CyCity::getBonusGoodHealth, "int ()")
      .def("getBonusBadHealth", &CyCity::getBonusBadHealth, "int ()")
      .def("getMilitaryHappiness", &CyCity::getMilitaryHappiness,
           "int () - happiness created by military units stationed in the city")
      .def("getMilitaryHappinessUnits", &CyCity::getMilitaryHappinessUnits,
           "number of military units creating happiness")
      .def("getBuildingGoodHappiness", &CyCity::getBuildingGoodHappiness, "int ()")
      .def("getBuildingBadHappiness", &CyCity::getBuildingBadHappiness, "int ()")
      .def("getBuildingHappiness", &CyCity::getBuildingHappiness, "int (int eBuilding)")
      // BUG - Building Additional Happiness - start
      .def("getAdditionalHappinessByBuilding", &CyCity::getAdditionalHappinessByBuilding,
           "int (int /*BuildingTypes*/ eBuilding) - additional happiness minus additional unhappiness")
      .def("getAdditionalGoodHappinessByBuilding", &CyCity::getAdditionalGoodHappinessByBuilding,
           "int (int /*BuildingTypes*/ eBuilding) - additional happiness")
      .def("getAdditionalBadHappinessByBuilding", &CyCity::getAdditionalBadHappinessByBuilding,
           "int (int /*BuildingTypes*/ eBuilding) - additional unhappiness")
      .def("getAdditionalAngryPopulationByBuilding", &CyCity::getAdditionalAngryPopulationByBuilding,
           "int (int /*BuildingTypes*/ eBuilding) - additional angry population")
      // BUG - Building Additional Happiness - end
      .def("getExtraBuildingGoodHappiness", &CyCity::getExtraBuildingGoodHappiness, "int ()")
      .def("getExtraBuildingBadHappiness", &CyCity::getExtraBuildingBadHappiness, "int ()")
      .def("getFeatureGoodHappiness", &CyCity::getFeatureGoodHappiness, "int ()")
      .def("getFeatureBadHappiness", &CyCity::getFeatureBadHappiness, "int ()")
      .def("getBonusGoodHappiness", &CyCity::getBonusGoodHappiness, "int ()")
      .def("getReligionGoodHappiness", &CyCity::getReligionGoodHappiness, "int ()")
      .def("getReligionBadHappiness", &CyCity::getReligionBadHappiness, "int ()")
      .def("getReligionHappiness", &CyCity::getReligionHappiness, "int (int eReligion)")
      .def("getExtraHappiness", &CyCity::getExtraHappiness, "int ()")
      .def("getExtraHealth", &CyCity::getExtraHealth, "int ()")
      .def("changeExtraHealth", &CyCity::changeExtraHealth, "void (int iChange)")
      .def("changeExtraHappiness", &CyCity::changeExtraHappiness, "void (int iChange)")
      .def("getHurryAngerTimer", &CyCity::getHurryAngerTimer, "int () - Anger caused by Hurrying timer")
      .def("changeHurryAngerTimer", &CyCity::changeHurryAngerTimer,
           "void (iChange) - adjust Hurry Angry timer by iChange")
      .def("getConscriptAngerTimer", &CyCity::getConscriptAngerTimer,
           "int () - returns the amount of time left on the conscript anger timer")
      .def("changeConscriptAngerTimer", &CyCity::changeConscriptAngerTimer,
           "void (int iChange) -changes the amount of time left on the conscript anger timer")
      .def("getDefyResolutionAngerTimer", &CyCity::getDefyResolutionAngerTimer,
           "int () - returns the amount of time left on the anger timer")
      .def("changeDefyResolutionAngerTimer", &CyCity::changeDefyResolutionAngerTimer,
           "void (int iChange) -changes the amount of time left on the anger timer")
      .def("flatDefyResolutionAngerLength", &CyCity::flatDefyResolutionAngerLength, "int ()")
      .def("getHappinessTimer", &CyCity::getHappinessTimer, "int () - Temporary Happiness timer")
      .def("changeHappinessTimer", &CyCity::changeHappinessTimer, "void (iChange) - adjust Happiness timer by iChange")
      .def("isNoUnhappiness", &CyCity::isNoUnhappiness, "bool () - is the city unaffected by unhappiness?")
      .def("isNoUnhealthyPopulation", &CyCity::isNoUnhealthyPopulation,
           "bool () - is the city unaffected by unhealthiness?")
      .def("isBuildingOnlyHealthy", &CyCity::isBuildingOnlyHealthy, "bool () - is the city ?")

      .def("getFood", &CyCity::getFood, "int () - stored food")
      .def("setFood", &CyCity::setFood, "void (iNewValue) - set stored food to iNewValue")
      .def("changeFood", &CyCity::changeFood, "void (iChange) - adjust stored food by iChange")
      .def("getFoodKept", &CyCity::getFoodKept, "int ()")
      .def("getMaxFoodKeptPercent", &CyCity::getMaxFoodKeptPercent, "int ()")
      .def("getOverflowProduction", &CyCity::getOverflowProduction, "int () - value of overflow production")
      .def("setOverflowProduction", &CyCity::setOverflowProduction,
           "void (iNewValue) - set overflow production to iNewValue")
      .def("getFeatureProduction", &CyCity::getFeatureProduction, "int () - value of feature production")
      .def("setFeatureProduction", &CyCity::setFeatureProduction,
           "void (iNewValue) - set feature production to iNewValue")
      .def("getMilitaryProductionModifier", &CyCity::getMilitaryProductionModifier,
           "int () - value of adjustments to military production")
      .def("getSpaceProductionModifier", &CyCity::getSpaceProductionModifier, "int ()")
      .def("getExtraTradeRoutes", &CyCity::getExtraTradeRoutes,
           "int () - returns the number of extra trade routes this city has")
      .def("changeExtraTradeRoutes", &CyCity::changeExtraTradeRoutes,
           "void (iChange) - Change the number of trade routes this city has")
      .def("getTradeRouteModifier", &CyCity::getTradeRouteModifier, "int ()")
      .def("getForeignTradeRouteModifier", &CyCity::getForeignTradeRouteModifier, "int ()")
      .def("getBuildingDefense", &CyCity::getBuildingDefense, "int () - building defense")
      // BUG - Building Additional Defense - start
      .def("getAdditionalDefenseByBuilding", &CyCity::getAdditionalDefenseByBuilding,
           "int (int /*BuildingTypes*/) - additional building defense")
      // BUG - Building Additional Defense - end
      .def("getBuildingBombardDefense", &CyCity::getBuildingBombardDefense, "int () - building defense")
      // BUG - Building Additional Bombard Defense - start
      .def("getAdditionalBombardDefenseByBuilding", &CyCity::getAdditionalBombardDefenseByBuilding,
           "int (int /*BuildingTypes*/) - additional building bombard defense")
      // BUG - Building Additional Bombard Defense - end
      .def("getFreeExperience", &CyCity::getFreeExperience, "int () - # of free experience newly trained units receive")
      .def("getCurrAirlift", &CyCity::getCurrAirlift, "int ()")
      .def("getMaxAirlift", &CyCity::getMaxAirlift, "int ()")
      .def("getAirModifier", &CyCity::getAirModifier, "int () - returns the air defense modifier")
      .def("getAirUnitCapacity", &CyCity::getAirUnitCapacity,
           "int (int /*TeamTypes*/ eTeam) - returns the number of air units allowed here")
      .def("getNukeModifier", &CyCity::getNukeModifier, "int ()")
      .def("getFreeSpecialist", &CyCity::getFreeSpecialist, "int ()")
      .def("isPower", &CyCity::isPower, "bool ()")
      .def("isAreaCleanPower", &CyCity::isAreaCleanPower, "bool ()")
      .def("isDirtyPower", &CyCity::isDirtyPower, "bool ()")
      .def("getDefenseDamage", &CyCity::getDefenseDamage, "int () - value of damage city defenses can receive")
      .def("changeDefenseDamage", &CyCity::changeDefenseDamage, "void (iChange) - adjust damage value by iChange")
      .def("isBombardable", &CyCity::isBombardable, "bool (CyUnit* pUnit)")
      .def("getNaturalDefense", &CyCity::getNaturalDefense, "int ()")
      .def("getTotalDefense", &CyCity::getTotalDefense, "int (bool bIgnoreBuilding)")
      .def("getDefenseModifier", &CyCity::getDefenseModifier, "int (bool bIgnoreBuilding)")

      .def("getOccupationTimer", &CyCity::getOccupationTimer, "int () - total # of turns remaining on occupation timer")
      .def("isOccupation", &CyCity::isOccupation, "bool () - is the city under occupation?")
      .def("setOccupationTimer", &CyCity::setOccupationTimer,
           "void (iNewValue) - set the Occupation Timer to iNewValue")
      .def("changeOccupationTimer", &CyCity::changeOccupationTimer,
           "void (iChange) - adjusts the Occupation Timer by iChange")
      .def("getCultureUpdateTimer", &CyCity::getCultureUpdateTimer, "int () - Culture Update Timer")
      .def("changeCultureUpdateTimer", &CyCity::changeCultureUpdateTimer,
           "void (iChange) - adjusts the Culture Update Timer by iChange")
      .def("isNeverLost", &CyCity::isNeverLost, "bool ()")
      .def("setNeverLost", &CyCity::setNeverLost, "void (iNewValue)")
      .def("isBombarded", &CyCity::isBombarded, "bool ()")
      .def("setBombarded", &CyCity::setBombarded, "void (iNewValue)")
      .def("isDrafted", &CyCity::isDrafted, "bool ()")
      .def("setDrafted", &CyCity::setDrafted, "void (iNewValue)")
      .def("isAirliftTargeted", &CyCity::isAirliftTargeted, "bool ()")
      .def("setAirliftTargeted", &CyCity::setAirliftTargeted, "void (iNewValue)")
      .def("isWeLoveTheKingDay", &CyCity::isWeLoveTheKingDay, "bool ()") //Rhye
      .def("isCitizensAutomated", &CyCity::isCitizensAutomated, "bool () - are citizens under automation?")
      .def("setCitizensAutomated", &CyCity::setCitizensAutomated,
           "void (bool bNewValue) - set city animation bNewValue")
      .def("isProductionAutomated", &CyCity::isProductionAutomated, "bool () - is production under automation?")
      .def("setProductionAutomated", &CyCity::setProductionAutomated,
           "void (bool bNewValue) - set city production automation to bNewValue")
      .def("isWallOverride", &CyCity::isWallOverride, "bool isWallOverride()")
      .def("setWallOverride", &CyCity::setWallOverride, "setWallOverride(bool bOverride)")
      .def("setCitySizeBoost", &CyCity::setCitySizeBoost, "setCitySizeBoost(int iBoost)")
      .def("isPlundered", &CyCity::isPlundered, "bool ()")
      .def("setPlundered", &CyCity::setPlundered, "void (iNewValue)")
      .def("getOwner", &CyCity::getOwner, "int /*PlayerTypes*/ ()")
      .def("getTeam", &CyCity::getTeam, "int /*TeamTypes*/ ()")
      .def("getPreviousOwner", &CyCity::getPreviousOwner, "int /*PlayerTypes*/ ()")
      .def("getOriginalOwner", &CyCity::getOriginalOwner, "int /*PlayerTypes*/ ()")
      .def("getCultureLevel", &CyCity::getCultureLevel, "int /*CultureLevelTypes*/ ()")
      .def("getCultureThreshold", &CyCity::getCultureThreshold)
      .def("getSeaPlotYield", &CyCity::getSeaPlotYield, "int (int /*YieldTypes*/) - total YieldType for water plots")
      .def("getCoastalPlotYield", &CyCity::getCoastalPlotYield,
           "int (int /*YieldTypes*/) - total YieldType for coastal plots")
      .def("getRiverPlotYield", &CyCity::getRiverPlotYield,
           "int (int /*YieldTypes*/) - total YieldType for river plots")

      // BUG - Building Additional Yield - start
      .def("getAdditionalYieldByBuilding", &CyCity::getAdditionalYieldByBuilding,
           "int (int /*YieldTypes*/, int /*BuildingTypes*/) - total change of YieldType from adding one BuildingType")
      .def("getAdditionalBaseYieldRateByBuilding", &CyCity::getAdditionalBaseYieldRateByBuilding,
           "int (int /*YieldTypes*/, int /*BuildingTypes*/) - base rate change of YieldType from adding one "
           "BuildingType")
      .def("getAdditionalYieldRateModifierByBuilding", &CyCity::getAdditionalYieldRateModifierByBuilding,
           "int (int /*YieldTypes*/, int /*BuildingTypes*/) - rate modifier change of YieldType from adding one "
           "BuildingType")
      // BUG - Building Additional Yield - end

      .def("getBaseYieldRate", &CyCity::getBaseYieldRate, "int (int /*YieldTypes*/) - base rate for YieldType")
      .def("setBaseYieldRate", &CyCity::setBaseYieldRate,
           "int (int /*YieldTypes*/, int iNewValue) - sets the base rate for YieldType")
      .def("changeBaseYieldRate", &CyCity::changeBaseYieldRate,
           "int (int /*YieldTypes*/, int iChange) - changes the base rate for YieldType")

      // Absinthe: exposed to python
      .def("changeBonusYieldRateModifier", &CyCity::changeBonusYieldRateModifier,
           "int (int /*YieldTypes*/, int iChange) - changes the bonus (resource) yield rate for YieldType")
      .def("changeBonusCommerceRateModifier", &CyCity::changeBonusCommerceRateModifier,
           "int (int /*CommerceTypes*/, int iChange) - changes the bonus (resource) commerce rate for CommerceType")
      .def("changeCommerceRateModifier", &CyCity::changeCommerceRateModifier,
           "int (int /*CommerceTypes*/, int iChange) - changes the general (building) commerce rate for CommerceType")

      .def("getBaseYieldRateModifier", &CyCity::getBaseYieldRateModifier)
      .def("getYieldRate", &CyCity::getYieldRate, "int (int /*YieldTypes*/) - total value of YieldType")
      .def("getYieldRateModifier", &CyCity::getYieldRateModifier,
           "int (int /*YieldTypes*/) - yield rate modifier for YieldType")
      .def("getTradeYield", &CyCity::getTradeYield, "int (int /*YieldTypes*/) - trade adjustment to YieldType")
      .def("totalTradeModifier", &CyCity::totalTradeModifier, "int () - total trade adjustment")

// BUG - Fractional Trade Routes - start
#ifdef _MOD_FRACTRADE
      .def("calculateTradeProfitTimes100", &CyCity::calculateTradeProfitTimes100,
           "int (CyCity) - returns the unrounded trade profit created by CyCity")
#endif
      // BUG - Fractional Trade Routes - end
      .def("calculateTradeProfit", &CyCity::calculateTradeProfit,
           "int (CyCity) - returns the trade profit created by CyCity")
      .def("calculateTradeYield", &CyCity::calculateTradeYield,
           "int (YieldType, int iTradeProfit) - calculates Trade Yield")

      .def("getExtraSpecialistYield", &CyCity::getExtraSpecialistYield, "int (int /*YieldTypes*/ eIndex)")
      .def("getExtraSpecialistYieldOfType", &CyCity::getExtraSpecialistYieldOfType,
           "int (int /*YieldTypes*/ eIndex, int /*SpecialistTypes*/ eSpecialist)")

      .def("getCommerceRate", &CyCity::getCommerceRate, "int (int /*CommerceTypes*/) - total Commerce rate")
      .def("getCommerceRateTimes100", &CyCity::getCommerceRateTimes100,
           "int (int /*CommerceTypes*/) - total Commerce rate")
      .def("getCommerceFromPercent", &CyCity::getCommerceFromPercent, "int (int /*CommerceTypes*/, int iYieldRate)")
      .def("getBaseCommerceRate", &CyCity::getBaseCommerceRate, "int (int /*CommerceTypes*/)")
      .def("getBaseCommerceRateTimes100", &CyCity::getBaseCommerceRateTimes100, "int (int /*CommerceTypes*/)")
      .def("getTotalCommerceRateModifier", &CyCity::getTotalCommerceRateModifier, "int (int /*CommerceTypes*/)")
      .def("getProductionToCommerceModifier", &CyCity::getProductionToCommerceModifier,
           "int (int /*CommerceTypes*/) - value of production to commerce modifier")
      .def("getBuildingCommerce", &CyCity::getBuildingCommerce,
           "int (int /*CommerceTypes*/) - total effect of cities buildings on CommerceTypes")
      .def("getBuildingCommerceByBuilding", &CyCity::getBuildingCommerceByBuilding,
           "int (int /*CommerceTypes*/, BuildingTypes) - total value of CommerceType from BuildingTypes")
      // BUG - Building Additional Commerce - start
      .def("getAdditionalCommerceByBuilding", &CyCity::getAdditionalCommerceByBuilding,
           "int (int /*CommerceTypes*/, int /*BuildingTypes*/) - rounded change of CommerceType from adding one "
           "BuildingType")
      .def("getAdditionalCommerceTimes100ByBuilding", &CyCity::getAdditionalCommerceTimes100ByBuilding,
           "int (int /*CommerceTypes*/, int /*BuildingTypes*/) - total change of CommerceType from adding one "
           "BuildingType")
      .def("getAdditionalBaseCommerceRateByBuilding", &CyCity::getAdditionalBaseCommerceRateByBuilding,
           "int (int /*CommerceTypes*/, int /*BuildingTypes*/) - base rate change of CommerceType from adding one "
           "BuildingType")
      .def("getAdditionalCommerceRateModifierByBuilding", &CyCity::getAdditionalCommerceRateModifierByBuilding,
           "int (int /*CommerceTypes*/, int /*BuildingTypes*/) - rate modifier change of CommerceType from adding one "
           "BuildingType")
      // BUG - Building Additional Commerce - end
      .def("getSpecialistCommerce", &CyCity::getSpecialistCommerce,
           "int (int /*CommerceTypes*/) - value of CommerceType adjustment from Specialists")
      .def("changeSpecialistCommerce", &CyCity::changeSpecialistCommerce,
           "void (int /*CommerceTypes*/, iChange) - adjusts Specialist contribution to CommerceType by iChange")
      .def("getReligionCommerce", &CyCity::getReligionCommerce,
           "int (int /*CommerceTypes*/) - effect on CommerceType by Religions")
      .def("getReligionCommerceByReligion", &CyCity::getReligionCommerceByReligion,
           "int (int /*CommerceTypes*/, ReligionType) - CommerceType effect from ReligionType")
      .def("getCorporationCommerce", &CyCity::getCorporationCommerce,
           "int (int /*CommerceTypes*/) - effect on CommerceType by Corporation")
      .def("getCorporationCommerceByCorporation", &CyCity::getCorporationCommerceByCorporation,
           "int (int /*CommerceTypes*/, CorporationType) - CommerceType effect from CorporationType")
      .def("getCorporationYield", &CyCity::getCorporationYield,
           "int (int /*CommerceTypes*/) - effect on YieldTypes by Corporation")
      .def("getCorporationYieldByCorporation", &CyCity::getCorporationYieldByCorporation,
           "int (int /*YieldTypes*/, CorporationType) - YieldTypes effect from CorporationType")
      .def("getCommerceRateModifier", &CyCity::getCommerceRateModifier,
           "int (int /*CommerceTypes*/) - indicates the total rate modifier on CommerceType")
      .def("getCommerceHappinessPer", &CyCity::getCommerceHappinessPer,
           "int (int /*CommerceTypes*/) - happiness from each level of entertainment")
      .def("getCommerceHappinessByType", &CyCity::getCommerceHappinessByType,
           "int (int /*CommerceTypes*/) - happiness from CommerceType")
      .def("getCommerceHappiness", &CyCity::getCommerceHappiness, "int () - happiness from all CommerceTypes")
      .def("getDomainFreeExperience", &CyCity::getDomainFreeExperience, "int (int /*DomainTypes*/)")
      .def("getDomainProductionModifier", &CyCity::getDomainProductionModifier, "int (int /*DomainTypes*/)")
      .def("getCulture", &CyCity::getCulture, "int /*PlayerTypes*/ ()")
      .def("getCultureTimes100", &CyCity::getCultureTimes100, "int /*PlayerTypes*/ ()")
      .def("countTotalCultureTimes100", &CyCity::countTotalCultureTimes100, "int ()")
      .def("findHighestCulture", &CyCity::findHighestCulture, "PlayerTypes ()")
      .def("calculateCulturePercent", &CyCity::calculateCulturePercent, "int (int eIndex)")
      .def("calculateTeamCulturePercent", &CyCity::calculateTeamCulturePercent, "int /*TeamTypes*/ ()")
      .def("setCulture", &CyCity::setCulture, "void (int PlayerTypes eIndex`, bool bPlots)")
      .def("setCultureTimes100", &CyCity::setCultureTimes100,
           "void (int PlayerTypes eIndex, int iNewValue, bool bPlots)")
      .def("changeCulture", &CyCity::changeCulture, "void (int PlayerTypes eIndex, int iChange, bool bPlots)")
      .def("changeCultureTimes100", &CyCity::changeCultureTimes100,
           "void (int PlayerTypes eIndex, int iChange, bool bPlots)")

      .def("isTradeRoute", &CyCity::isTradeRoute, "bool ()")
      .def("isEverOwned", &CyCity::isEverOwned, "bool ()")

      .def("isRevealed", &CyCity::isRevealed, "bool (int /*TeamTypes*/ eIndex, bool bDebug)")
      .def("setRevealed", &CyCity::setRevealed, "void (int /*TeamTypes*/ eIndex, bool bNewValue)")
      .def("getEspionageVisibility", &CyCity::getEspionageVisibility, "bool (int /*TeamTypes*/ eIndex)")
      .def("getName", &CyCity::getName, "string () - city name")
      .def("getNameForm", &CyCity::getNameForm, "string () - city name")
      .def("getNameKey", &CyCity::getNameKey, "string () - city name")
      .def("setName", &CyCity::setName, "void (TCHAR szNewValue, bool bFound) - sets the name to szNewValue")
      .def("isNoBonus", &CyCity::isNoBonus, "bool (int eIndex)")
      .def("changeNoBonusCount", &CyCity::changeNoBonusCount, "void (int eIndex, int iChange)")
      .def("getFreeBonus", &CyCity::getFreeBonus, "int (int eIndex)")
      .def("changeFreeBonus", &CyCity::changeFreeBonus, "void (int eIndex, int iChange)")
      .def("getNumBonuses", &CyCity::getNumBonuses, "int (PlayerID)")
      .def("hasBonus", &CyCity::hasBonus, "bool - (BonusID) - is BonusID connected to the city?")
      .def("getBuildingProduction", &CyCity::getBuildingProduction,
           "int (BuildingID) - current production towards BuildingID")
      .def("setBuildingProduction", &CyCity::setBuildingProduction,
           "void (BuildingID, iNewValue) - set progress towards BuildingID as iNewValue")
      .def("changeBuildingProduction", &CyCity::changeBuildingProduction,
           "void (BuildingID, iChange) - adjusts progress towards BuildingID by iChange")
      .def("getBuildingProductionTime", &CyCity::getBuildingProductionTime, "int (int eIndex)")
      .def("setBuildingProductionTime", &CyCity::setBuildingProductionTime, "int (int eIndex, int iNewValue)")
      .def("changeBuildingProductionTime", &CyCity::changeBuildingProductionTime, "int (int eIndex, int iChange)")
      // BUG - Production Decay - start
      .def("isBuildingProductionDecay", &CyCity::isBuildingProductionDecay, "bool (int /*BuildingTypes*/ eIndex)")
      .def("getBuildingProductionDecay", &CyCity::getBuildingProductionDecay, "int (int /*BuildingTypes*/ eIndex)")
      .def("getBuildingProductionDecayTurns", &CyCity::getBuildingProductionDecayTurns,
           "int (int /*BuildingTypes*/ eIndex)")
      // BUG - Production Decay - end
      .def("getBuildingOriginalOwner", &CyCity::getBuildingOriginalOwner,
           "int (BuildingType) - index of original building owner")
      .def("getBuildingOriginalTime", &CyCity::getBuildingOriginalTime, "int (BuildingType) - original build date")
      .def("getUnitProduction", &CyCity::getUnitProduction, "int (UnitID) - gets current production towards UnitID")
      .def("setUnitProduction", &CyCity::setUnitProduction,
           "void (UnitID, iNewValue) - sets production towards UnitID as iNewValue")
      .def("changeUnitProduction", &CyCity::changeUnitProduction,
           "void (UnitID, iChange) - adjusts production towards UnitID by iChange")
      // BUG - Production Decay - start
      .def("getUnitProductionTime", &CyCity::getUnitProductionTime, "int (int /*UnitTypes*/ eIndex)")
      .def("setUnitProductionTime", &CyCity::setUnitProductionTime, "int (int /*UnitTypes*/ eIndex, int iNewValue)")
      .def("changeUnitProductionTime", &CyCity::changeUnitProductionTime, "int (int /*UnitTypes*/ eIndex, int iChange)")
      .def("isUnitProductionDecay", &CyCity::isUnitProductionDecay, "bool (int /*UnitTypes*/ eIndex)")
      .def("getUnitProductionDecay", &CyCity::getUnitProductionDecay, "int (int /*UnitTypes*/ eIndex)")
      .def("getUnitProductionDecayTurns", &CyCity::getUnitProductionDecayTurns, "int (int /*UnitTypes*/ eIndex)")
      // BUG - Production Decay - end
      // BUG - Project Production - start
      .def("getProjectProduction", &CyCity::getProjectProduction, "int (int /*ProjectTypes*/ eIndex)")
      .def("setProjectProduction", &CyCity::setProjectProduction, "void (int /*ProjectTypes*/ eIndex, int iNewValue)")
      .def("changeProjectProduction", &CyCity::changeProjectProduction,
           "void (int /*ProjectTypes*/ eIndex, int iChange)")
      // BUG - Project Production - end
      .def("getGreatPeopleUnitRate", &CyCity::getGreatPeopleUnitRate, "int (int /*UnitTypes*/ iIndex)")
      .def("getGreatPeopleUnitProgress", &CyCity::getGreatPeopleUnitProgress, "int (int /*UnitTypes*/ iIndex)")
      .def("setGreatPeopleUnitProgress", &CyCity::setGreatPeopleUnitProgress,
           "int (int /*UnitTypes*/ iIndex, int iNewValue)")
      .def("changeGreatPeopleUnitProgress", &CyCity::changeGreatPeopleUnitProgress,
           "int (int /*UnitTypes*/ iIndex, int iChange)")
      .def("getSpecialistCount", &CyCity::getSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
      .def("alterSpecialistCount", &CyCity::alterSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, int iChange)")
      .def("getMaxSpecialistCount", &CyCity::getMaxSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
      .def("isSpecialistValid", &CyCity::isSpecialistValid, "bool (int /*SpecialistTypes*/ eIndex, int iExtra)")
      .def("getForceSpecialistCount", &CyCity::getForceSpecialistCount, "int (int /*SpecialistTypes*/ eIndex)")
      .def("isSpecialistForced", &CyCity::isSpecialistForced, "bool ()")
      .def("setForceSpecialistCount", &CyCity::setForceSpecialistCount,
           "int (int /*SpecialistTypes*/ eIndex, int iNewValue")
      .def("changeForceSpecialistCount", &CyCity::changeForceSpecialistCount,
           "int (int /*SpecialistTypes*/ eIndex, int iChange")
      .def("getFreeSpecialistCount", &CyCity::getFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex")
      .def("setFreeSpecialistCount", &CyCity::setFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex, iNewValue")
      .def("changeFreeSpecialistCount", &CyCity::changeFreeSpecialistCount,
           "int (int /*SpecialistTypes*/ eIndex, iChange")
      .def("getAddedFreeSpecialistCount", &CyCity::getAddedFreeSpecialistCount, "int (int /*SpecialistTypes*/ eIndex")
      .def("getImprovementFreeSpecialists", &CyCity::getImprovementFreeSpecialists, "int (ImprovementID)")
      .def("changeImprovementFreeSpecialists", &CyCity::changeImprovementFreeSpecialists,
           "void (ImprovementID, iChange) - adjust ImprovementID free specialists by iChange")
      .def("getReligionInfluence", &CyCity::getReligionInfluence,
           "int (ReligionID) - value of influence from ReligionID")
      .def("changeReligionInfluence", &CyCity::changeReligionInfluence,
           "void (ReligionID, iChange) - adjust ReligionID influence by iChange")

      .def("getCurrentStateReligionHappiness", &CyCity::getCurrentStateReligionHappiness, "int ()")
      .def("getStateReligionHappiness", &CyCity::getStateReligionHappiness, "int (int /*ReligionTypes*/ ReligionID)")
      .def("changeStateReligionHappiness", &CyCity::changeStateReligionHappiness,
           "void (int /*ReligionTypes*/ ReligionID, iChange)")

      .def("getUnitCombatFreeExperience", &CyCity::getUnitCombatFreeExperience, "int (int /*UnitCombatTypes*/ eIndex)")
      .def("getFreePromotionCount", &CyCity::getFreePromotionCount, "int (int /*PromotionTypes*/ eIndex)")
      .def("isFreePromotion", &CyCity::isFreePromotion, "bool (int /*PromotionTypes*/ eIndex)")
      .def("getSpecialistFreeExperience", &CyCity::getSpecialistFreeExperience, "int ()")
      .def("getEspionageDefenseModifier", &CyCity::getEspionageDefenseModifier, "int ()")

      .def("isWorkingPlotByIndex", &CyCity::isWorkingPlotByIndex,
           "bool (iIndex) - true if a worker is working this city's plot iIndex")
      .def("isWorkingPlot", &CyCity::isWorkingPlot, "bool (iIndex) - true if a worker is working this city's pPlot")
      .def("alterWorkingPlot", &CyCity::alterWorkingPlot, "void (iIndex)")
      .def("isHasRealBuilding", &CyCity::isHasRealBuilding, "bool (BuildingID) - real building or a free one?") //Rhye
      .def("setHasRealBuilding", &CyCity::setHasRealBuilding,
           "(BuildingID, bAdd) - if bAdd = 1 the building is Added, 0 it is removed") //Rhye
      .def("getNumRealBuilding", &CyCity::getNumRealBuilding, "int (BuildingID) - get # real building of this type")
      .def("setNumRealBuilding", &CyCity::setNumRealBuilding,
           "(BuildingID, iNum) - Sets number of buildings in this city of BuildingID type")
      .def("getNumFreeBuilding", &CyCity::getNumFreeBuilding,
           "int (BuildingID) - # of free Building ID (ie: from a Wonder)")
      .def("isHasReligion", &CyCity::isHasReligion, "bool (ReligionID) - does city have ReligionID?")
      .def("setHasReligion", &CyCity::setHasReligion,
           "void (ReligionID, bool bNewValue, bool bAnnounce, bool bArrows) - religion begins to spread")
      .def("isHasCorporation", &CyCity::isHasCorporation, "bool (CorporationID) - does city have CorporationID?")
      .def("setHasCorporation", &CyCity::setHasCorporation,
           "void (CorporationID, bool bNewValue, bool bAnnounce, bool bArrows) - corporation begins to spread")
      .def("isActiveCorporation", &CyCity::isActiveCorporation,
           "bool (CorporationID) - does city have active CorporationID?")
      .def("getTradeCity", &CyCity::getTradeCity, python::return_value_policy<python::manage_new_object>(),
           "CyCity (int iIndex) - remove SpecialistType[iIndex]")
      .def("getTradeRoutes", &CyCity::getTradeRoutes, "int ()")
      .def("getReligionCount", &CyCity::getReligionCount,
           "int ()") // Absinthe: edead's code from SoI, needed for the persecution python function

      .def("clearOrderQueue", &CyCity::clearOrderQueue, "void ()")
      .def("pushOrder", &CyCity::pushOrder,
           "void (OrderTypes eOrder, int iData1, int iData2, bool bSave, bool bPop, bool bAppend, bool bForce)")
      .def("popOrder", &CyCity::popOrder, "int (int iNum, bool bFinish, bool bChoose)")
      .def("getOrderQueueLength", &CyCity::getOrderQueueLength, "void ()")
      .def("getOrderFromQueue", &CyCity::getOrderFromQueue, python::return_value_policy<python::manage_new_object>(),
           "OrderData* (int iIndex)")

      .def("setWallOverridePoints", &CyCity::setWallOverridePoints,
           "setWallOverridePoints(const python::tuple& kPoints)")
      .def("getWallOverridePoints", &CyCity::getWallOverridePoints, "python::tuple getWallOverridePoints()")

      .def("AI_avoidGrowth", &CyCity::AI_avoidGrowth, "bool ()")
      .def("AI_isEmphasize", &CyCity::AI_isEmphasize, "bool (int iEmphasizeType)")
      .def("AI_countBestBuilds", &CyCity::AI_countBestBuilds, "int (CyArea* pArea)")
      .def("AI_cityValue", &CyCity::AI_cityValue, "int ()")

      .def("getScriptData", &CyCity::getScriptData, "str () - Get stored custom data (via pickle)")
      .def("setScriptData", &CyCity::setScriptData, "void (str) - Set stored custom data (via pickle)")

      .def("visiblePopulation", &CyCity::visiblePopulation, "int ()")

      .def("getBuildingYieldChange", &CyCity::getBuildingYieldChange,
           "int (int /*BuildingClassTypes*/ eBuildingClass, int /*YieldTypes*/ eYield)")
      .def("setBuildingYieldChange", &CyCity::setBuildingYieldChange,
           "void (int /*BuildingClassTypes*/ eBuildingClass, int /*YieldTypes*/ eYield, int iChange)")
      .def("getBuildingCommerceChange", &CyCity::getBuildingCommerceChange,
           "int (int /*BuildingClassTypes*/ eBuildingClass, int /*CommerceTypes*/ eCommerce)")
      .def("setBuildingCommerceChange", &CyCity::setBuildingCommerceChange,
           "void (int /*BuildingClassTypes*/ eBuildingClass, int /*CommerceTypes*/ eCommerce, int iChange)")
      .def("getBuildingHappyChange", &CyCity::getBuildingHappyChange, "int (int /*BuildingClassTypes*/ eBuildingClass)")
      .def("setBuildingHappyChange", &CyCity::setBuildingHappyChange,
           "void (int /*BuildingClassTypes*/ eBuildingClass, int iChange)")
      .def("getBuildingHealthChange", &CyCity::getBuildingHealthChange,
           "int (int /*BuildingClassTypes*/ eBuildingClass)")
      .def("setBuildingHealthChange", &CyCity::setBuildingHealthChange,
           "void (int /*BuildingClassTypes*/ eBuildingClass, int iChange)")

      .def("getLiberationPlayer", &CyCity::getLiberationPlayer, "int ()")
      .def("liberate", &CyCity::liberate, "void ()")

      // 3Miro: New functions
      // Absinthe: with the new persecution code added from SoI, these functions are currently unused
      /*.def("canPurgeReligion", &CyCity::canPurgeReligion, "bool ()")
      .def("doPurgeReligions", &CyCity::doPurgeReligions, "void ()")*/
      // Absinthe: end
      .def("getProvince", &CyCity::getProvince, "int ()")
      .def("getProvinceID", &CyCity::getProvinceID, "int ()")

      .def("getNumForeignReligions", &CyCity::getNumForeignReligions, "int ()");
}
