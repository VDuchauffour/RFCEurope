#include "CvGameCoreDLL.h"
#include "CyPlayer.h"
#include "CyUnit.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CySelectionGroup.h"
#include "CyArea.h"
//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>
//# include <boost/python/scope.hpp>

//
// published python interface for CyPlayer
//

void CyPlayerPythonInterface2(python::class_<CyPlayer>& x)
{
	OutputDebugString("Python Extension Module - CyPlayerPythonInterface2\n");

	// set the docstring of the current module scope
	python::scope().attr("__doc__") = "Civilization IV Player Class";
	x
		// 3Miro: added functions
		.def("getFinancialPower", &CyPlayer::getFinancialPower, "int getFinancialPower()")
		.def("getVotingPower", &CyPlayer::getVotingPower, "int getVotingPower( eReligionTypes )")

		.def("setIsCrusader", &CyPlayer::setIsCrusader, "void setIsCrusader( bool bVal )")
		.def("getIsCrusader", &CyPlayer::getIsCrusader, "bool getIsCrusader()")

		.def("getFaith", &CyPlayer::getFaith, "int getFaith()")
		.def("setFaith", &CyPlayer::setFaith, "void setFaith( int iNewFaith )")
		.def("changeFaith", &CyPlayer::changeFaith, "void changeFaith( int iChange )")

		.def("getProsecutionCount", &CyPlayer::getProsecutionCount, "int getProsecutionCount()")
		.def("setProsecutionCount", &CyPlayer::setProsecutionCount, "void setProsecutionCount( int iNewCount )")
		.def("changeProsecutionCount", &CyPlayer::changeProsecutionCount, "void changeProsecutionCount( int iChange )")

		//.def("getFaithStability", &CyPlayer::getFaithStability, "int getFaithStability()")
		.def("getFaithBenefit", &CyPlayer::getFaithBenefit, "int getFaithBenefit( int iFaithPower )")
		.def("isFaithBenefit", &CyPlayer::isFaithBenefit, "bool isFaithBenefit( int iFaithPower )")

		.def("countCultureProduced", &CyPlayer::countCultureProduced, "int countCultureProduced()")

		.def("setUHV", &CyPlayer::setUHV, "void ( int iUHV, int iValue )")
		.def("getUHV", &CyPlayer::getUHV, "int ( int iUHV )")
		.def("setUHVCounter", &CyPlayer::setUHVCounter, "void ( int iUHV, int iValue )")
		.def("getUHVCounter", &CyPlayer::getUHVCounter, "int ( int iUHV )")
		.def("setUHV2of3", &CyPlayer::setUHV2of3, "void ( bool bNewValue )")
		.def("getUHV2of3", &CyPlayer::getUHV2of3, "bool getUHV2of3()")
		.def("getUHVDescription", &CyPlayer::getUHVDescription, "str ( int )")

		.def("setProvinceType", &CyPlayer::setProvinceType, "void ( int, int )")
		.def("getProvinceType", &CyPlayer::getProvinceType, "int ( int )")
		.def("getProvinceCurrentState", &CyPlayer::getProvinceCurrentState, "int ( int )")
		.def("getProvinceCityCount", &CyPlayer::getProvinceCityCount, "int ( int )")
		.def("getForeignCitiesInMyProvinceType", &CyPlayer::getForeignCitiesInMyProvinceType, "int ( int )")

		// 3MiroStability
		.def("getStabilityBase", &CyPlayer::getStabilityBase, "int ( int )")
		.def("changeStabilityBase", &CyPlayer::changeStabilityBase, "void ( int, int )")
		.def("getStabilityVary", &CyPlayer::getStabilityVary, "int ( int )")
		.def("setStabilityVary", &CyPlayer::setStabilityVary, "void ( int, int )")
		.def("getStabilitySwing", &CyPlayer::getStabilitySwing, "int ( )")
		.def("setStabilitySwing", &CyPlayer::setStabilitySwing, "void ( int )")
		// Absinthe: swing instability in anarchy
		.def("getStabSwingAnarchy", &CyPlayer::getStabSwingAnarchy, "int ( )")
		.def("setStabSwingAnarchy", &CyPlayer::setStabSwingAnarchy, "void ( int )")
		.def("getStability", &CyPlayer::getStability, "int ( )")
		.def("getWarPeaceChange", &CyPlayer::getWarPeaceChange, "int ( )")

		// 3MiroColonies
		.def("getNumColonies", &CyPlayer::getNumColonies, "int ( )")
		.def("setNumColonies", &CyPlayer::setNumColonies, "void ( int )")

		.def("getPicklefreeParameter", &CyPlayer::getPicklefreeParameter, "int ( int )")
		.def("setPicklefreeParameter", &CyPlayer::setPicklefreeParameter, "void ( int, int )")

		.def("getMaster", &CyPlayer::getMaster, "int ( )")
		.def("countVassals", &CyPlayer::countVassals, "int ( )")

		// Absinthe: DCN update
		.def("processCivNames", &CyPlayer::processCivNames, "void ( )")

		// 3MiroProvinces: extra province functions
		.def("provinceIsSpreadReligion", &CyPlayer::provinceIsSpreadReligion, "bool (int, int)")
		.def("provinceIsConvertReligion", &CyPlayer::provinceIsConvertReligion, "bool (int, int)")

		// Absinthe: respawn status
		.def("getRespawnedAlive", &CyPlayer::getRespawnedAlive, "bool ()")
		.def("setRespawnedAlive", &CyPlayer::setRespawnedAlive, "void ( bool )")

		.def("getEverRespawned", &CyPlayer::getEverRespawned, "bool ()")
		.def("setEverRespawned", &CyPlayer::setEverRespawned, "void ( bool )")

		.def("getForcedHistoricityUnitProduction", &CyPlayer::getForcedHistoricityUnitProduction, "int ()")
		.def("setForcedHistoricityUnitProduction", &CyPlayer::setForcedHistoricityUnitProduction, "void ( int )")

		.def("getForcedHistoricityUnitSupport", &CyPlayer::getForcedHistoricityUnitSupport, "int ()")
		.def("setForcedHistoricityUnitSupport", &CyPlayer::setForcedHistoricityUnitSupport, "void ( int )")

		.def("getForcedHistoricityCivicSupport", &CyPlayer::getForcedHistoricityCivicSupport, "int ()")
		.def("setForcedHistoricityCivicSupport", &CyPlayer::setForcedHistoricityCivicSupport, "void ( int )")

		// Absinthe: original CyPlayerInterface2.cpp file started here
		.def("AI_updateFoundValues", &CyPlayer::AI_updateFoundValues, "void (bool bStartingLoc)")
		.def("AI_foundValue", &CyPlayer::AI_foundValue, "int (int, int, int, bool)")
		.def("AI_isFinancialTrouble", &CyPlayer::AI_isFinancialTrouble, "bool ()")
		.def("AI_demandRebukedWar", &CyPlayer::AI_demandRebukedWar, "bool (int /*PlayerTypes*/)")
		.def("AI_getAttitude", &CyPlayer::AI_getAttitude, "AttitudeTypes (int /*PlayerTypes*/) - Gets the attitude of the player towards the player passed in")
		.def("AI_unitValue", &CyPlayer::AI_unitValue, "int (int /*UnitTypes*/ eUnit, int /*UnitAITypes*/ eUnitAI, CyArea* pArea)")
		.def("AI_civicValue", &CyPlayer::AI_civicValue, "int (int /*CivicTypes*/ eCivic)")
		.def("AI_totalUnitAIs", &CyPlayer::AI_totalUnitAIs, "int (int /*UnitAITypes*/ eUnitAI)")
		.def("AI_totalAreaUnitAIs", &CyPlayer::AI_totalAreaUnitAIs, "int (CyArea* pArea, int /*UnitAITypes*/ eUnitAI)")
		.def("AI_totalWaterAreaUnitAIs", &CyPlayer::AI_totalWaterAreaUnitAIs, "int (CyArea* pArea, int /*UnitAITypes*/ eUnitAI)")
		.def("AI_getNumAIUnits", &CyPlayer::AI_getNumAIUnits, "int (UnitAIType) - Returns # of UnitAITypes the player current has of UnitAIType")
		.def("AI_getAttitudeExtra", &CyPlayer::AI_getAttitudeExtra, "int (int /*PlayerTypes*/ eIndex) - Returns the extra attitude for this player - usually scenario specific")
		.def("AI_setAttitudeExtra", &CyPlayer::AI_setAttitudeExtra, "void (int /*PlayerTypes*/ eIndex, int iNewValue) - Sets the extra attitude for this player - usually scenario specific")
		.def("AI_changeAttitudeExtra", &CyPlayer::AI_changeAttitudeExtra, "void (int /*PlayerTypes*/ eIndex, int iChange) - Changes the extra attitude for this player - usually scenario specific")
		.def("AI_getMemoryCount", &CyPlayer::AI_getMemoryCount, "int (/*PlayerTypes*/ eIndex1, /*MemoryTypes*/ eIndex2)")
		.def("AI_changeMemoryCount", &CyPlayer::AI_changeMemoryCount, "void (/*PlayerTypes*/ eIndex1, /*MemoryTypes*/ eIndex2, int iChange)")
		.def("AI_getExtraGoldTarget", &CyPlayer::AI_getExtraGoldTarget, "int ()")
		.def("AI_setExtraGoldTarget", &CyPlayer::AI_setExtraGoldTarget, "void (int)")

		.def("getScoreHistory", &CyPlayer::getScoreHistory, "int (int iTurn)")
		.def("getEconomyHistory", &CyPlayer::getEconomyHistory, "int (int iTurn)")
		.def("getIndustryHistory", &CyPlayer::getIndustryHistory, "int (int iTurn)")
		.def("getAgricultureHistory", &CyPlayer::getAgricultureHistory, "int (int iTurn)")
		.def("getPowerHistory", &CyPlayer::getPowerHistory, "int (int iTurn)")
		.def("getCultureHistory", &CyPlayer::getCultureHistory, "int (int iTurn)")
		.def("getEspionageHistory", &CyPlayer::getEspionageHistory, "int (int iTurn)")

		.def("getScriptData", &CyPlayer::getScriptData, "str () - Get stored custom data (via pickle)")
		.def("setScriptData", &CyPlayer::setScriptData, "void (str) - Set stored custom data (via pickle)")

		.def("chooseTech", &CyPlayer::chooseTech, "void (int iDiscover, wstring szText, bool bFront)")

		.def("AI_maxGoldTrade", &CyPlayer::AI_maxGoldTrade, "int (int)")
		.def("AI_maxGoldPerTurnTrade", &CyPlayer::AI_maxGoldPerTurnTrade, "int (int)")

		.def("splitEmpire", &CyPlayer::splitEmpire, "bool (int iAreaId)")
		.def("canSplitEmpire", &CyPlayer::canSplitEmpire, "bool ()")
		.def("canSplitArea", &CyPlayer::canSplitArea, "bool (int)")
		.def("canHaveTradeRoutesWith", &CyPlayer::canHaveTradeRoutesWith, "bool (int)")
		.def("forcePeace", &CyPlayer::forcePeace, "void (int)")

		.def("getSettlersMaps", &CyPlayer::getSettlersMaps, "int (int i, int j)") //Rhye
		.def("getWarsMaps", &CyPlayer::getWarsMaps, "int (int i, int j)") //Absinthe
		.def("setLeader", &CyPlayer::setLeader, "void (int i)") //Rhye
		.def("getLeader", &CyPlayer::getLeader, "int /*LeaderHeadTypes*/ ()") //Rhye
		;
}