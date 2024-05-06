//
// published python interface for CyGlobalContext
// Author - Mustafa Thamer
//

#include "CvGameCoreDLL.h"
#include "CyMap.h"
#include "CyPlayer.h"
#include "CyGame.h"
#include "CyGlobalContext.h"
#include "CvRandom.h"
//#include "CvStructs.h"
#include "CvInfos.h"
#include "CyTeam.h"

void CyGlobalContextPythonInterface5(python::class_<CyGlobalContext> &x)
{
  OutputDebugString("Python Extension Module - CyGlobalContextPythonInterface5\n");

  x
      // 3Miro balancing stuff, expose to Python
      .def("setStartingTurn", &CyGlobalContext::setStartingTurn, "void (int iCiv, int iVal)") // 3Miro
      .def("getStartingTurn", &CyGlobalContext::getStartingTurn, "int (int iCiv )")           // 3Miro

      .def("setGrowthModifiersAI", &CyGlobalContext::setGrowthModifiersAI,
           "void ( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop )") // 3Miro
      .def("setProductionModifiersAI", &CyGlobalContext::setProductionModifiersAI,
           "void ( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch )") // 3Miro
      .def("setSupportModifiersAI", &CyGlobalContext::setSupportModifiersAI,
           "void ( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic )") // 3Miro

      .def("setGrowthModifiersHu", &CyGlobalContext::setGrowthModifiersHu,
           "void ( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop )") // 3Miro
      .def("setProductionModifiersHu", &CyGlobalContext::setProductionModifiersHu,
           "void ( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch )") // 3Miro
      .def("setSupportModifiersHu", &CyGlobalContext::setSupportModifiersHu,
           "void ( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic )") // 3Miro

      .def("setInitialPopulation", &CyGlobalContext::setInitialPopulation, "void ( int iCiv, int iInitPop )") // 3Miro
      .def("setInitialBuilding", &CyGlobalContext::setInitialBuilding,
           "void ( int iCiv, int iBuilding, bool w )") // 3Miro

      .def("setStartingTurn", &CyGlobalContext::setStartingTurn, "void (int iCiv, int iVal)") // 3Miro
      .def("setCityClusterAI", &CyGlobalContext::setCityClusterAI,
           "void (int iCiv, int iTop, int iBottom, int iMinus )")                                       // 3Miro
      .def("setCityWarDistanceAI", &CyGlobalContext::setCityWarDistanceAI, "void (int iCiv, int iVal)") // 3Miro
      .def("setTechPreferenceAI", &CyGlobalContext::setTechPreferenceAI,
           "void (int iCiv, int iTech, int iVal)") // 3Miro

      .def("setDiplomacyModifiers", &CyGlobalContext::setDiplomacyModifiers,
           "void (int iCiv1, int iCiv2, int iVal)")                                         // 3Miro
      .def("setUP", &CyGlobalContext::setUP, "void (int iCiv, int iPower, int iParameter)") // 3Miro
      .def("hasUP", &CyGlobalContext::hasUP, "bool (int iCiv, int iPower)")                 // 3Miro

      .def("setSizeNPlayers", &CyGlobalContext::setSizeNPlayers,
           "void ( int iMaxX, int iMaxY, int iNumPlayers, int iAllPlayers, int iNumTechs, int iNumReligions )") // 3Miro
      .def("setSettlersMap", &CyGlobalContext::setSettlersMap, "void (int iCiv, int y, int x, int iVal)")       // 3Miro
      .def("setWarsMap", &CyGlobalContext::setWarsMap, "void (int iCiv, int y, int x, int iVal)")               // 3Miro

      .def("setIndependnets", &CyGlobalContext::setIndependnets,
           "void ( int iIndyStart, int iIndyEnd, int iBarb )")                                     // 3Miro
      .def("setPapalPlayer", &CyGlobalContext::setPapalPlayer, "void ( int iCiv, int iReligion )") // 3Miro

      // UHV optimizations
      .def("getLargestOtherCity", &CyGlobalContext::getLargestOtherCity, "int (int x, int y)")       // Absinthe
      .def("isLargestCity", &CyGlobalContext::isLargestCity, "bool (int x, int y)")                  // 3Miro
      .def("getTopCultureOtherCity", &CyGlobalContext::getTopCultureOtherCity, "int (int x, int y)") // Absinthe
      .def("isTopCultureCity", &CyGlobalContext::isTopCultureCity, "bool (int x, int y)")            // 3Miro
      .def("doesOwnCities", &CyGlobalContext::doesOwnCities,
           "int (int iCiv, int BLx, int BLy, int TRx, int TRy )") // 3Miro
      .def("doesOwnOrVassalCities", &CyGlobalContext::doesOwnOrVassalCities,
           "int (int iCiv, int BLx, int BLy, int TRx, int TRy )") // 3Miro
      .def("doesHaveOtherReligion", &CyGlobalContext::doesHaveOtherReligion,
           "int (int BLx, int BLy, int TRx, int TRy, int AllowR )") // 3Miro
      .def("countOwnedCities", &CyGlobalContext::countOwnedCities,
           "int (int iCiv, int BLx, int BLy, int TRx, int TRy )")                                      // 3Miro
      .def("countCitiesLostTo", &CyGlobalContext::countCitiesLostTo, "int (int iCiv, int iNewOwner )") // 3Miro
      .def("safeMotherland", &CyGlobalContext::safeMotherland, "bool (int iCiv)")                      // 3Miro
      .def("canSeeAllTerrain", &CyGlobalContext::canSeeAllTerrain, "bool (int iCiv, int iTerrain)")    // 3Miro
      .def("controlMostTeritory", &CyGlobalContext::controlMostTeritory,
           "bool ( int iCiv, int BLx, int BLy, int TRx, int TRy );") // 3Miro

      // Core and Normal Areas
      .def("setCoreNormal", &CyGlobalContext::setCoreNormal,
           "void ( int iCiv, int iCBLx, int iCBLy, int iCTRx, int iCTRy, int iNBLx, int iNBLy, int iNTRx, int iNTRy, "
           "int iCCE, int iCNE )")                                                                      // 3Miro
      .def("addCoreException", &CyGlobalContext::addCoreException, "void (int iCiv, int x, int y)")     // 3Miro
      .def("addNormalException", &CyGlobalContext::addNormalException, "void (int iCiv, int x, int y)") // 3Miro

      // Absinthe: unused in RFCE
      /*
		// stability sweep
		.def("calcLastOwned", &CyGlobalContext::calcLastOwned, "void ()") // 3Miro
		.def("getlOwnedPlots", &CyGlobalContext::getlOwnedPlots, "int (int iCiv )") // 3Miro
		.def("getlOwnedCities", &CyGlobalContext::getlOwnedCities, "int (int iCiv )") // 3Miro
		// stability city sweep
		.def("cityStabilityExpansion", &CyGlobalContext::cityStabilityExpansion, "int (int iPlayer, int iFCity)") // 3Miro
		.def("cityStabilityPenalty", &CyGlobalContext::cityStabilityPenalty, "int ( int iPlayer, int iAnger, int iHealth, int iReligion, int iLarge, int iHurry, int iNoMilitary, int iWarW, int iFReligion, int iFCulture, int iPerCityCap )") // 3Miro
		.def("damageFromBuilding", &CyGlobalContext::damageFromBuilding, "void (int iPlayer, int iBuilding, int iFoeDamage, int iBarbDamage ))") // 3Miro
		*/

      // prosecution consts
      //.def("getProsecutionCount", &CyGlobalContext::getProsecutionCount, "int (int iCiv )") // 3Miro
      //.def("setProsecutionCount", &CyGlobalContext::setProsecutionCount, "void (int iCiv, int iCount )") // 3Miro
      .def("setProsecutorReligions", &CyGlobalContext::setProsecutorReligions,
           "void (int iProsecutor, int iProsecutorClass )") // 3Miro

      // saintly AI
      .def("setSaintParameters", &CyGlobalContext::setSaintParameters,
           "void ( int iUnitID, int iBenefit, int iTreshhold1, int iTreshhold3 )") // 3Miro

      // AI diplomacy
      .def("getRelationTowards", &CyGlobalContext::getRelationTowards, "int (int iWho, int iTowards )") // 3Miro

      // GlobalWarming
      .def("setGlobalWarming", &CyGlobalContext::setGlobalWarming, "void (bool bWhat )") // 3Miro

      // Religious Spread
      .def("setReligionSpread", &CyGlobalContext::setReligionSpread,
           "void ( int iCiv, int iReligion, int iSpread )") // 3Miro

      // Colony AI modifier
      .def("setColonyAIModifier", &CyGlobalContext::setColonyAIModifier, "void ( int iCiv, int iModifier )") // 3Miro

      // Schism Parameters
      .def("setSchism", &CyGlobalContext::setSchism, "void ( int iReligionA, int iReligionB, int iTurn )") // 3Miro

      // Faith Powers Parameters
      .def("setReligionBenefit", &CyGlobalContext::setReligionBenefit,
           "void ( int iReligion, int iBenefit, int iParameter, iCap )") // 3Miro

      // set Holiest City
      .def("setHoliestCity", &CyGlobalContext::setHoliestCity, "void ( int iCityX, int iCityY )") // 3Miro

      // set Starting Workers
      .def("setStartingWorkers", &CyGlobalContext::setStartingWorkers, "void ( int iCiv, int iWorkers )") // 3Miro

      // count cities outside the core
      .def("countCitiesOutside", &CyGlobalContext::countCitiesOutside, "int ( int iCiv )") // 3Miro

      // set strategic tiles
      .def("setStrategicTile", &CyGlobalContext::setStrategicTile, "void ( int iCiv, int iX, int iY )") // 3Miro

      // set fast Terrain
      .def("setFastTerrain", &CyGlobalContext::setFastTerrain, "void ( int iFastTerrain )") // 3Miro

      // set AI building prefs
      .def("setBuildingPref", &CyGlobalContext::setBuildingPref, "void ( int iCiv, int iBuilding, int iPref )") // 3Miro

      // 3Miro: set Autorun Hack
      .def("setAutorunHack", &CyGlobalContext::setAutorunHack, "void ( int iUnit, int iX, int iY )") // 3Miro

      // 3Miro: set Building + Civic combo
      .def("setBuildingCivicCommerseCombo1", &CyGlobalContext::setBuildingCivicCommerseCombo1,
           "void ( int iCode )") // 3Miro
      .def("setBuildingCivicCommerseCombo2", &CyGlobalContext::setBuildingCivicCommerseCombo2,
           "void ( int iCode )") // 3Miro
      .def("setBuildingCivicCommerseCombo3", &CyGlobalContext::setBuildingCivicCommerseCombo3,
           "void ( int iCode )") // 3Miro

      // 3Miro: Psycho AI cheat, this misleads the AI about it's odds in succeeding an attack against a given city, also actually improves the odds of success
      .def("setPsychoAICheat", &CyGlobalContext::setPsychoAICheat, "void ( int iPlayer, int iX, int iY )") // 3Miro

      // 3Miro: on AI to AI battles, this gives a iChange chnage to the attack.defense odds
      .def("setHistoricalEnemyAICheat", &CyGlobalContext::setHistoricalEnemyAICheat,
           "void ( int iAttacker, int iDefender, int iChange )") // 3Miro

      // tech Timeline modifiers
      .def("setTimelineTechModifiers", &CyGlobalContext::setTimelineTechModifiers,
           "void ( int iTPTop, int iTPBottom, int iTPCap, int iTBTop, int iTBBottom, int iTBCap )") // 3Miro
      .def("setTimelineTechDateForTech", &CyGlobalContext::setTimelineTechDateForTech,
           "void ( int iTech, int iTurn )") // 3Miro

      // 3MiroProvinces
      .def("setProvince", &CyGlobalContext::setProvince, "void ( int iX, int iY, int iProvince )")
      .def("createProvinceCrossreferenceList", &CyGlobalContext::createProvinceCrossreferenceList, "void ()")
      .def("setNumRegions", &CyGlobalContext::setNumRegions, "void ( int )")
      .def("setProvinceToRegion", &CyGlobalContext::setProvinceToRegion, "void ( int, int )")

      .def("setCultureImmume", &CyGlobalContext::setCultureImmume, "void (int, int, int)")
      .def("setProvinceTypeNumber", &CyGlobalContext::setProvinceTypeNumber, "void ( iNum )")
      .def("setProvinceTypeParams", &CyGlobalContext::setProvinceTypeParams, "void (int, int, int, int, int)")

      .def("setVassalagaeCondition", &CyGlobalContext::setVassalagaeCondition, "void (int, int, int, int)")

      .def("getNumProvinceTiles", &CyGlobalContext::getNumProvinceTiles, "int ( int )")
      .def("getProvinceX", &CyGlobalContext::getProvinceX, "int (int, int )")
      .def("getProvinceY", &CyGlobalContext::getProvinceY, "int (int, int )")

      .def("setParentSchismReligions", &CyGlobalContext::setParentSchismReligions, "void (int, int )")

      .def("setMercPromotion", &CyGlobalContext::setMercPromotion, "void ( int )")

      .def("setPaceTurnsAfterSpawn", &CyGlobalContext::setPaceTurnsAfterSpawn, "void ( int )")

      .def("setMinorReligion", &CyGlobalContext::setMinorReligion, "void ( int )")
      .def("setMinorReligionRefugies", &CyGlobalContext::setMinorReligionRefugies, "void ( int )")
      .def("getMinorReligionRefugies", &CyGlobalContext::getMinorReligionRefugies, "int( )")

      // Absinthe: set the plotting parameters
      .def("setCoreToPlot", &CyGlobalContext::setCoreToPlot, "void ( int )")
      .def("setNormalToPlot", &CyGlobalContext::setNormalToPlot, "void ( int )")
      // Absinthe: unused plot parameters
      //.def("setWhatToPlot", &CyGlobalContext::setNormalToPlot, "void ( int )")
      //.def("setCivForCore", &CyGlobalContext::setCivForCore, "void ( int )")
      //.def("setCivForNormal", &CyGlobalContext::setCivForNormal, "void ( int )")
      //.def("setCivForWars", &CyGlobalContext::setCivForWars, "void ( int )")
      //.def("setCivForSettler", &CyGlobalContext::setCivForSettler, "void ( int )")
      ;
}
