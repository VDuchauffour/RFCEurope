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


void CyGlobalContextPythonInterface4(python::class_<CyGlobalContext>& x)
{
	OutputDebugString("Python Extension Module - CyGlobalContextPythonInterface1\n");

	x
		.def("getNumMissionInfos", &CyGlobalContext::getNumMissionInfos, "() - Total Mission Infos XML\\Units\\CIV4MissionInfos.xml")
		.def("getMissionInfo", &CyGlobalContext::getMissionInfo, python::return_value_policy<python::reference_existing_object>(), "(MissionID) - CvInfo for MissionID")

		.def("getNumAutomateInfos", &CyGlobalContext::getNumAutomateInfos, "() - Total Automate Infos XML\\Units\\CIV4AutomateInfos.xml")
		.def("getAutomateInfo", &CyGlobalContext::getAutomateInfo, python::return_value_policy<python::reference_existing_object>(), "(AutomateID) - CvInfo for AutomateID")

		.def("getNumCommandInfos", &CyGlobalContext::getNumCommandInfos, "() - Total Command Infos XML\\Units\\CIV4CommandInfos.xml")
		.def("getCommandInfo", &CyGlobalContext::getCommandInfo, python::return_value_policy<python::reference_existing_object>(), "(CommandID) - CvInfo for CommandID")

		.def("getNumControlInfos", &CyGlobalContext::getNumControlInfos, "() - Total Control Infos XML\\Units\\CIV4ControlInfos.xml")
		.def("getControlInfo", &CyGlobalContext::getControlInfo, python::return_value_policy<python::reference_existing_object>(), "(ControlID) - CvInfo for ControlID")

		.def("getNumPromotionInfos", &CyGlobalContext::getNumPromotionInfos, "() - Total Promotion Infos XML\\Units\\CIV4PromotionInfos.xml")
		.def("getPromotionInfo", &CyGlobalContext::getPromotionInfo, python::return_value_policy<python::reference_existing_object>(), "(PromotionID) - CvInfo for PromotionID")

		.def("getNumTechInfos", &CyGlobalContext::getNumTechInfos, "() - Total Technology Infos XML\\Technologies\\CIV4TechInfos.xml")
		.def("getTechInfo", &CyGlobalContext::getTechInfo, python::return_value_policy<python::reference_existing_object>(), "(TechID) - CvInfo for TechID")

		.def("getNumSpecialBuildingInfos", &CyGlobalContext::getNumSpecialBuildingInfos, "() - Total Special Building Infos")
		.def("getSpecialBuildingInfo", &CyGlobalContext::getSpecialBuildingInfo, python::return_value_policy<python::reference_existing_object>(), "(SpecialBuildingID) - CvInfo for SpecialBuildingID")

		.def("getNumReligionInfos", &CyGlobalContext::getNumReligionInfos, "() - Total Religion Infos XML\\GameInfo\\CIV4ReligionInfos.xml")
		.def("getReligionInfo", &CyGlobalContext::getReligionInfo, python::return_value_policy<python::reference_existing_object>(), "(ReligionID) - CvInfo for ReligionID")

		.def("getNumCorporationInfos", &CyGlobalContext::getNumCorporationInfos, "() - Total Religion Infos XML\\GameInfo\\CIV4CorporationInfos.xml")
		.def("getCorporationInfo", &CyGlobalContext::getCorporationInfo, python::return_value_policy<python::reference_existing_object>(), "(CorporationID) - CvInfo for CorporationID")

		.def("getNumVictoryInfos", &CyGlobalContext::getNumVictoryInfos, "() - Total Victory Infos XML\\GameInfo\\CIV4VictoryInfos.xml")
		.def("getVictoryInfo", &CyGlobalContext::getVictoryInfo, python::return_value_policy<python::reference_existing_object>(), "(VictoryID) - CvInfo for VictoryID")

		.def("getNumSpecialistInfos", &CyGlobalContext::getNumSpecialistInfos, "() - Total Specialist Infos XML\\Units\\CIV4SpecialistInfos.xml")
		.def("getSpecialistInfo", &CyGlobalContext::getSpecialistInfo, python::return_value_policy<python::reference_existing_object>(), "(SpecialistID) - CvInfo for SpecialistID")

		.def("getNumCivicOptionInfos", &CyGlobalContext::getNumCivicOptionInfos, "() - Total Civic Infos XML\\Misc\\CIV4CivicOptionInfos.xml")
		.def("getCivicOptionInfo", &CyGlobalContext::getCivicOptionInfo, python::return_value_policy<python::reference_existing_object>(), "(CivicID) - CvInfo for CivicID")

		.def("getNumCivicInfos", &CyGlobalContext::getNumCivicInfos, "() - Total Civic Infos XML\\Misc\\CIV4CivicInfos.xml")
		.def("getCivicInfo", &CyGlobalContext::getCivicInfo, python::return_value_policy<python::reference_existing_object>(), "(CivicID) - CvInfo for CivicID")

		.def("getNumDiplomacyInfos", &CyGlobalContext::getNumDiplomacyInfos, "() - Total diplomacy Infos XML\\GameInfo\\CIV4DiplomacyInfos.xml")
		.def("getDiplomacyInfo", &CyGlobalContext::getDiplomacyInfo, python::return_value_policy<python::reference_existing_object>(), "(DiplomacyID) - CvInfo for DiplomacyID")

		.def("getNumProjectInfos", &CyGlobalContext::getNumProjectInfos, "() - Total Project Infos XML\\GameInfo\\CIV4ProjectInfos.xml")
		.def("getProjectInfo", &CyGlobalContext::getProjectInfo, python::return_value_policy<python::reference_existing_object>(), "(ProjectID) - CvInfo for ProjectID")

		.def("getNumVoteInfos", &CyGlobalContext::getNumVoteInfos, "() - Total VoteInfos")
		.def("getVoteInfo", &CyGlobalContext::getVoteInfo, python::return_value_policy<python::reference_existing_object>(), "(VoteID) - CvInfo for VoteID")

		.def("getNumProcessInfos", &CyGlobalContext::getNumProcessInfos, "() - Total ProcessInfos")
		.def("getProcessInfo", &CyGlobalContext::getProcessInfo, python::return_value_policy<python::reference_existing_object>(), "(ProcessID) - CvInfo for ProcessID")

		.def("getNumEmphasizeInfos", &CyGlobalContext::getNumEmphasizeInfos, "() - Total EmphasizeInfos")
		.def("getEmphasizeInfo", &CyGlobalContext::getEmphasizeInfo, python::return_value_policy<python::reference_existing_object>(), "(EmphasizeID) - CvInfo for EmphasizeID")

		.def("getHurryInfo", &CyGlobalContext::getHurryInfo, python::return_value_policy<python::reference_existing_object>(), "(HurryID) - CvInfo for HurryID")

		.def("getUnitAIInfo", &CyGlobalContext::getUnitAIInfo, python::return_value_policy<python::reference_existing_object>(), "UnitAIInfo (int id)")

		.def("getColorInfo", &CyGlobalContext::getColorInfo, python::return_value_policy<python::reference_existing_object>(), "ColorInfo (int id)")

		.def("getInfoTypeForString", &CyGlobalContext::getInfoTypeForString, "int (string) - returns the info index with the matching type string")
		.def("getTypesEnum", &CyGlobalContext::getTypesEnum, "int (string) - returns the type enum from a type string")

		.def("getNumPlayerColorInfos", &CyGlobalContext::getNumPlayerColorInfos, "int () - Returns number of PlayerColorInfos")
		.def("getPlayerColorInfo", &CyGlobalContext::getPlayerColorInfo, python::return_value_policy<python::reference_existing_object>(), "PlayerColorInfo (int id)")

		.def("getNumQuestInfos", &CyGlobalContext::getNumQuestInfos, "int () - Returns number of QuestInfos")
		.def("getQuestInfo", &CyGlobalContext::getQuestInfo, python::return_value_policy<python::reference_existing_object>(), "QuestInfo () - Returns info object")

		.def("getNumTutorialInfos", &CyGlobalContext::getNumTutorialInfos, "int () - Returns number of TutorialInfos")
		.def("getTutorialInfo", &CyGlobalContext::getTutorialInfo, python::return_value_policy<python::reference_existing_object>(), "TutorialInfo () - Returns info object")

		.def("getNumEventTriggerInfos", &CyGlobalContext::getNumEventTriggerInfos, "int () - Returns number of EventTriggerInfos")
		.def("getEventTriggerInfo", &CyGlobalContext::getEventTriggerInfo, python::return_value_policy<python::reference_existing_object>(), "EventTriggerInfo () - Returns info object")

		.def("getNumEventInfos", &CyGlobalContext::getNumEventInfos, "int () - Returns number of EventInfos")
		.def("getEventInfo", &CyGlobalContext::getEventInfo, python::return_value_policy<python::reference_existing_object>(), "EventInfo () - Returns info object")

		.def("getNumEspionageMissionInfos", &CyGlobalContext::getNumEspionageMissionInfos, "int () - Returns number of EspionageMissionInfos")
		.def("getEspionageMissionInfo", &CyGlobalContext::getEspionageMissionInfo, python::return_value_policy<python::reference_existing_object>(), "EspionageMissionInfo () - Returns info object")

		.def("getNumHints", &CyGlobalContext::getNumHints, "int () - Returns number of Hints")
		.def("getHints", &CyGlobalContext::getHints, python::return_value_policy<python::reference_existing_object>(), "Hints () - Returns info object")

		.def("getNumMainMenus", &CyGlobalContext::getNumMainMenus, "int () - Returns number")
		.def("getMainMenus", &CyGlobalContext::getMainMenus, python::return_value_policy<python::reference_existing_object>(), "MainMenus () - Returns info object")

		.def("getNumVoteSourceInfos", &CyGlobalContext::getNumVoteSourceInfos, "int ()")
		.def("getVoteSourceInfo", &CyGlobalContext::getVoteSourceInfo, python::return_value_policy<python::reference_existing_object>(), "Returns info object")

		.def("getNumVoteSourceInfos", &CyGlobalContext::getNumVoteSourceInfos, "int ()")
		.def("getVoteSourceInfo", &CyGlobalContext::getVoteSourceInfo, python::return_value_policy<python::reference_existing_object>(), "Returns info object")

		// ArtInfos
		.def("getNumInterfaceArtInfos", &CyGlobalContext::getNumInterfaceArtInfos, "() - Total InterfaceArtnology Infos XML\\InterfaceArtnologies\\CIV4InterfaceArtInfos.xml")
		.def("getInterfaceArtInfo", &CyGlobalContext::getInterfaceArtInfo, python::return_value_policy<python::reference_existing_object>(), "(InterfaceArtID) - CvArtInfo for InterfaceArtID")

		.def("getNumMovieArtInfos", &CyGlobalContext::getNumMovieArtInfos, "() - Total MovieArt Infos XML\\MovieArtInfos\\CIV4ArtDefines.xml")
		.def("getMovieArtInfo", &CyGlobalContext::getMovieArtInfo, python::return_value_policy<python::reference_existing_object>(), "(MovieArtID) - CvArtInfo for MovieArtID")

		.def("getNumMiscArtInfos", &CyGlobalContext::getNumMiscArtInfos, "() - Total MiscArtnology Infos XML\\MiscArt\\CIV4MiscArtInfos.xml")
		.def("getMiscArtInfo", &CyGlobalContext::getMiscArtInfo, python::return_value_policy<python::reference_existing_object>(), "(MiscArtID) - CvArtInfo for MiscArtID")

		.def("getNumUnitArtInfos", &CyGlobalContext::getNumUnitArtInfos, "() - Total UnitArtnology Infos XML\\UnitArt\\CIV4UnitArtInfos.xml")
		.def("getUnitArtInfo", &CyGlobalContext::getUnitArtInfo, python::return_value_policy<python::reference_existing_object>(), "(UnitID) - CvArtInfo for UnitID")

		.def("getNumBuildingArtInfos", &CyGlobalContext::getNumBuildingArtInfos, "int () - Returns number of BuildingArtInfos")
		.def("getBuildingArtInfo", &CyGlobalContext::getBuildingArtInfo, python::return_value_policy<python::reference_existing_object>(), "(BuildingID) - CvArtInfo for BuildingID")

		.def("getNumCivilizationArtInfos", &CyGlobalContext::getNumCivilizationArtInfos, "int () - Returns number of CivilizationArtInfos")
		.def("getCivilizationArtInfo", &CyGlobalContext::getCivilizationArtInfo, python::return_value_policy<python::reference_existing_object>(), "(CivilizationID) - CvArtInfo for CivilizationID")

		.def("getNumLeaderheadArtInfos", &CyGlobalContext::getNumLeaderheadArtInfos, "int () - Returns number of LeaderHeadArtInfos")
		.def("getLeaderheadArtInfo", &CyGlobalContext::getLeaderheadArtInfo, python::return_value_policy<python::reference_existing_object>(), "(LeaderheadID) - CvArtInfo for LeaderheadID")

		.def("getNumBonusArtInfos", &CyGlobalContext::getNumBonusArtInfos, "int () - Returns number of BonusArtInfos")
		.def("getBonusArtInfo", &CyGlobalContext::getBonusArtInfo, python::return_value_policy<python::reference_existing_object>(), "BonusArtInfo () - Returns info object")

		.def("getNumImprovementArtInfos", &CyGlobalContext::getNumImprovementArtInfos, "int () - Returns number of ImprovementArtInfos")
		.def("getImprovementArtInfo", &CyGlobalContext::getImprovementArtInfo, python::return_value_policy<python::reference_existing_object>(), "ImprovementArtInfo () - Returns info object")

		.def("getNumTerrainArtInfos", &CyGlobalContext::getNumTerrainArtInfos, "int () - Returns number of TerrainArtInfos")
		.def("getTerrainArtInfo", &CyGlobalContext::getTerrainArtInfo, python::return_value_policy<python::reference_existing_object>(), "TerrainArtInfo () - Returns info object")

		.def("getNumFeatureArtInfos", &CyGlobalContext::getNumFeatureArtInfos, "int () - Returns number of FeatureArtInfos")
		.def("getFeatureArtInfo", &CyGlobalContext::getFeatureArtInfo, python::return_value_policy<python::reference_existing_object>(), "FeatureArtInfo () - Returns info object")

		// Types
		.def("getNumEntityEventTypes", &CyGlobalContext::getNumEntityEventTypes, "int () - Returns number of EntityEventTypes")
		.def("getEntityEventType", &CyGlobalContext::getEntityEventTypes, "string () - Returns enum string")

		.def("getNumAnimationOperatorTypes", &CyGlobalContext::getNumAnimationOperatorTypes, "int () - Returns number of AnimationOperatorTypes")
		.def("getAnimationOperatorTypes", &CyGlobalContext::getAnimationOperatorTypes, "string () - Returns enum string")

		.def("getFunctionTypes", &CyGlobalContext::getFunctionTypes, "string () - Returns enum string")

		.def("getNumArtStyleTypes", &CyGlobalContext::getNumArtStyleTypes, "int () - Returns number of ArtStyleTypes")
		.def("getArtStyleTypes", &CyGlobalContext::getArtStyleTypes, "string () - Returns enum string")

		.def("getNumFlavorTypes", &CyGlobalContext::getNumFlavorTypes, "int () - Returns number of FlavorTypes")
		.def("getFlavorTypes", &CyGlobalContext::getFlavorTypes, "string () - Returns enum string")

		.def("getNumUnitArtStyleTypeInfos", &CyGlobalContext::getNumUnitArtStyleTypeInfos, "int () - Returns number of UnitArtStyleTypes")
		.def("getUnitArtStyleTypeInfo", &CyGlobalContext::getUnitArtStyleTypeInfo, python::return_value_policy<python::reference_existing_object>(), "(UnitArtStyleTypeID) - CvInfo for UnitArtStyleTypeID")

		.def("getNumCitySizeTypes", &CyGlobalContext::getNumCitySizeTypes, "int () - Returns number of CitySizeTypes")
		.def("getCitySizeTypes", &CyGlobalContext::getCitySizeTypes, "string () - Returns enum string")

		.def("getContactTypes", &CyGlobalContext::getContactTypes, "string () - Returns enum string")

		.def("getDiplomacyPowerTypes", &CyGlobalContext::getDiplomacyPowerTypes, "string () - Returns enum string")

		// 3Miro balancing stuff, expose to Python
		.def("setStartingTurn", &CyGlobalContext::setStartingTurn, "void (int iCiv, int iVal)") // 3Miro
		.def("getStartingTurn", &CyGlobalContext::getStartingTurn, "int (int iCiv )") // 3Miro
		.def("setGrowthModifiers", &CyGlobalContext::setGrowthModifiers, "void ( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop )") // 3Miro
		.def("setProductionModifiers", &CyGlobalContext::setProductionModifiers, "void ( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch )") // 3Miro
		.def("setSupportModifiers", &CyGlobalContext::setSupportModifiers, "void ( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic )") // 3Miro
		.def("setInitialPopulation", &CyGlobalContext::setInitialPopulation, "void ( int iCiv, int iInitPop )") // 3Miro
		.def("setInitialBuilding", &CyGlobalContext::setInitialBuilding, "void ( int iCiv, int iBuilding, bool w )") // 3Miro
		
		.def("setStartingTurn", &CyGlobalContext::setStartingTurn, "void (int iCiv, int iVal)") // 3Miro
		.def("setCityClusterAI", &CyGlobalContext::setCityClusterAI, "void (int iCiv, int iTop, int iBottom, int iMinus )") // 3Miro
		.def("setCityWarDistanceAI", &CyGlobalContext::setCityWarDistanceAI, "void (int iCiv, int iVal)") // 3Miro
		.def("setTechPreferenceAI", &CyGlobalContext::setTechPreferenceAI, "void (int iCiv, int iTech, int iVal)") // 3Miro
		.def("setDiplomacyModifiers", &CyGlobalContext::setDiplomacyModifiers, "void (int iCiv1, int iCiv2, int iVal)") // 3Miro
		.def("setUP", &CyGlobalContext::setUP, "void (int iCiv, int iPower, int iParameter)") // 3Miro
		.def("hasUP", &CyGlobalContext::hasUP, "bool (int iCiv, int iPower)") // 3Miro
		
		.def("setSizeNPlayers", &CyGlobalContext::setSizeNPlayers, "void ( int iMaxX, int iMaxY, int iNumPlayers, int iAllPlayers, int iNumTechs, int iNumReligions )") // 3Miro
		.def("setSettlersMap", &CyGlobalContext::setSettlersMap, "void (int iCiv, int y, int x, int iVal)") // 3Miro
		.def("setWarsMap", &CyGlobalContext::setWarsMap, "void (int iCiv, int y, int x, int iVal)") // 3Miro

		.def("setIndependnets", &CyGlobalContext::setIndependnets, "void ( int iIndyStart, int iIndyEnd, int iBarb )") // 3Miro
		.def("setPapalPlayer", &CyGlobalContext::setPapalPlayer, "void ( int iCiv, int iReligion )") // 3Miro

		
		// UHV optimizations
		.def("isLargestCity", &CyGlobalContext::isLargestCity, "bool (int x, int y)") // 3Miro
		.def("isTopCultureCity", &CyGlobalContext::isTopCultureCity, "bool (int x, int y)") // 3Miro
		.def("doesOwnCities", &CyGlobalContext::doesOwnCities, "int (int iCiv, int BLx, int BLy, int TRx, int TRy )") // 3Miro
		.def("doesOwnOrVassalCities", &CyGlobalContext::doesOwnOrVassalCities, "int (int iCiv, int BLx, int BLy, int TRx, int TRy )") // 3Miro
		.def("doesHaveOtherReligion", &CyGlobalContext::doesHaveOtherReligion, "int (int BLx, int BLy, int TRx, int TRy, int AllowR )") // 3Miro
		.def("countOwnedCities", &CyGlobalContext::countOwnedCities, "int (int iCiv, int BLx, int BLy, int TRx, int TRy )") // 3Miro
		.def("countCitiesLostTo", &CyGlobalContext::countCitiesLostTo, "int (int iCiv, int iNewOwner )") // 3Miro
		.def("safeMotherland", &CyGlobalContext::safeMotherland, "bool (int iCiv)") // 3Miro
		.def("canSeeAllTerrain", &CyGlobalContext::canSeeAllTerrain, "bool (int iCiv, int iTerrain)") // 3Miro
		.def("controlMostTeritory", &CyGlobalContext::controlMostTeritory, "bool ( int iCiv, int BLx, int BLy, int TRx, int TRy );") // 3Miro
		.def("damageFromBuilding", &CyGlobalContext::damageFromBuilding, "void (int iPlayer, int iBuilding, int iFoeDamage, int iBarbDamage ))") // 3Miro

		// Core and Normal Areas
		.def("setCoreNormal", &CyGlobalContext::setCoreNormal, "void ( int iCiv, int iCBLx, int iCBLy, int iCTRx, int iCTRy, int iNBLx, int iNBLy, int iNTRx, int iNTRy, int iCCE, int iCNE )") // 3Miro
		.def("addCoreException", &CyGlobalContext::addCoreException, "void (int iCiv, int x, int y)") // 3Miro
		.def("addNormalException", &CyGlobalContext::addNormalException, "void (int iCiv, int x, int y)") // 3Miro

		// stability sweep
		.def("calcLastOwned", &CyGlobalContext::calcLastOwned, "void ()") // 3Miro
		.def("getlOwnedPlots", &CyGlobalContext::getlOwnedPlots, "int (int iCiv )") // 3Miro
		.def("getlOwnedCities", &CyGlobalContext::getlOwnedCities, "int (int iCiv )") // 3Miro
		// stability city sweep
		.def("cityStabilityExpansion", &CyGlobalContext::cityStabilityExpansion, "int (int iPlayer, int iFCity)") // 3Miro
		.def("cityStabilityPenalty", &CyGlobalContext::cityStabilityPenalty, "int ( int iPlayer, int iAnger, int iHealth, int iReligion, int iLarge, int iHurry, int iNoMilitary, int iWarW, int iFReligion, int iFCulture, int iPerCityCap )") // 3Miro

		// prosecution consts
		//.def("getProsecutionCount", &CyGlobalContext::getProsecutionCount, "int (int iCiv )") // 3Miro
		//.def("setProsecutionCount", &CyGlobalContext::setProsecutionCount, "void (int iCiv, int iCount )") // 3Miro
		.def("setProsecutorReligions", &CyGlobalContext::setProsecutorReligions, "void (int iProsecutor, int iProsecutorClass )") // 3Miro

		// saintly AI
		.def("setSaintParameters", &CyGlobalContext::setSaintParameters, "void ( int iUnitID, int iBenefit, int iTreshhold1, int iTreshhold3 )") // 3Miro

		// AI diplomacy
		.def("getRelationTowards", &CyGlobalContext::getRelationTowards, "int (int iWho, int iTowards )") // 3Miro

		// GlobalWarming
		.def("setGlobalWarming", &CyGlobalContext::setGlobalWarming, "void (bool bWhat )") // 3Miro

		// Religious Spread
		.def("setReligionSpread", &CyGlobalContext::setReligionSpread, "void ( int iCiv, int iReligion, int iSpread )") // 3Miro

		// Colony AI modifier
		.def("setColonyAIModifier", &CyGlobalContext::setColonyAIModifier, "void ( int iCiv, int iModifier )") // 3Miro

		// Schism Parameters
		.def("setSchism", &CyGlobalContext::setSchism, "void ( int iReligionA, int iReligionB, int iTurn )") // 3Miro

		// Faith Powers Parameters
		.def("setReligionBenefit", &CyGlobalContext::setReligionBenefit, "void ( int iReligion, int iBenefit, int iParameter )") // 3Miro

		// set Holiest City
		.def("setHoliestCity", &CyGlobalContext::setHoliestCity, "void ( int iCityX, int iCityY )") // 3Miro

		// set Starting Workers
		.def("setStartingWorkers", &CyGlobalContext::setStartingWorkers, "void ( int iCiv, int iWorkers )") // 3Miro

		// count cities outside the core
		.def("countCitiesOutside", &CyGlobalContext::countCitiesOutside, "int ( int iCiv )") // 3Miro

		// set strategic tiles
		.def("setStrategicTile", &CyGlobalContext::setStrategicTile, "void ( int iCiv, int iX, int iY )") // 3Miro
		;
}