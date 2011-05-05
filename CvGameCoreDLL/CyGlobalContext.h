#pragma once

#ifndef CyGlobalContext_h
#define CyGlobalContext_h

//
// Python wrapper class for global vars and fxns
// Passed to Python
//

#include "CvGlobals.h"
#include "CvArtFileMgr.h"

class CyGame;
class CyMap;
class CyPlayer;
class CvRandom;
class CyEngine;
class CyTeam;
class CyArtFileMgr;
class CyUserProfile;
class CyVariableSystem;

class CyGlobalContext
{
public:
	CyGlobalContext();
	virtual ~CyGlobalContext();

	static CyGlobalContext& getInstance();		// singleton accessor

	bool isDebugBuild() const;
	CyGame* getCyGame() const;
	CyMap* getCyMap() const;
	CyPlayer* getCyPlayer(int idx);
	CyPlayer* getCyActivePlayer();
	CvRandom& getCyASyncRand() const;
	CyTeam* getCyTeam(int i);
	CyArtFileMgr* getCyArtFileMgr() const;

	CvEffectInfo* getEffectInfo(int i) const;
	CvTerrainInfo* getTerrainInfo(int i) const;
	CvBonusClassInfo* getBonusClassInfo(int i) const;
	CvBonusInfo* getBonusInfo(int i) const;
	CvFeatureInfo* getFeatureInfo(int i) const;
	CvCivilizationInfo* getCivilizationInfo(int idx) const;
	CvLeaderHeadInfo* getLeaderHeadInfo(int i) const;
	CvTraitInfo* getTraitInfo(int i) const;
	CvUnitInfo* getUnitInfo(int i) const;
	CvSpecialUnitInfo* getSpecialUnitInfo(int i) const;
	CvYieldInfo* getYieldInfo(int i) const;
	CvCommerceInfo* getCommerceInfo(int i) const;
	CvRouteInfo* getRouteInfo(int i) const;
	CvImprovementInfo* getImprovementInfo(int i) const;
	CvGoodyInfo* getGoodyInfo(int i) const;
	CvBuildInfo* getBuildInfo(int i) const;
	CvHandicapInfo* getHandicapInfo(int i) const;
	CvGameSpeedInfo* getGameSpeedInfo(int i) const;
	CvTurnTimerInfo* getTurnTimerInfo(int i) const;
	CvBuildingClassInfo* getBuildingClassInfo(int i) const;
	CvMissionInfo* getMissionInfo(int i) const;
	CvCommandInfo* getCommandInfo(int i) const;
	CvAutomateInfo* getAutomateInfo(int i) const;
	CvActionInfo* getActionInfo(int i) const;
	CvUnitClassInfo* getUnitClassInfo(int i) const;
	CvInfoBase* getUnitCombatInfo(int i) const;
	CvInfoBase* getDomainInfo(int i) const;
	CvBuildingInfo* getBuildingInfo(int i) const;
	CvCivicOptionInfo* getCivicOptionInfo(int i) const;
	CvCivicInfo* getCivicInfo(int i) const;
	CvDiplomacyInfo* getDiplomacyInfo(int i) const;
	CvProjectInfo* getProjectInfo(int i) const;
	CvVoteInfo* getVoteInfo(int i) const;
	CvProcessInfo* getProcessInfo(int i) const;
	CvSpecialistInfo* getSpecialistInfo(int i) const;
	CvReligionInfo* getReligionInfo(int i) const;
	CvCorporationInfo* getCorporationInfo(int i) const;
	CvControlInfo* getControlInfo(int i) const;
	CvTechInfo* getTechInfo(int i) const;
	CvSpecialBuildingInfo* getSpecialBuildingInfo(int i) const;
	CvPromotionInfo* getPromotionInfo(int i) const;
	CvAnimationPathInfo * getAnimationPathInfo(int i) const;
	CvEmphasizeInfo * getEmphasizeInfo(int i) const;
	CvUpkeepInfo * getUpkeepInfo(int i) const;
	CvCultureLevelInfo * getCultureLevelInfo(int i) const;
	CvEraInfo * getEraInfo(int i) const;
	CvVictoryInfo * getVictoryInfo(int i) const;
	CvWorldInfo * getWorldInfo(int i) const;
	CvClimateInfo * getClimateInfo(int i) const;
	CvSeaLevelInfo * getSeaLevelInfo(int i) const;
	CvInfoBase * getUnitAIInfo(int i) const;
	CvColorInfo* getColorInfo(int i) const;
    CvUnitArtStyleTypeInfo* getUnitArtStyleTypeInfo(int i) const;

	int getInfoTypeForString(const char* szInfoType) const;
	int getTypesEnum(const char* szType) const;

	int getNumPlayerColorInfos() const { return GC.getNumPlayerColorInfos(); }
	CvPlayerColorInfo* getPlayerColorInfo(int i) const;

	CvInfoBase* getHints(int i) const;
	CvMainMenuInfo* getMainMenus(int i) const;
	CvInfoBase* getInvisibleInfo(int i) const;
	CvVoteSourceInfo* getVoteSourceInfo(int i) const;
	CvInfoBase* getAttitudeInfo(int i) const;
	CvInfoBase* getMemoryInfo(int i) const;
	CvInfoBase* getConceptInfo(int i) const;
	CvInfoBase* getNewConceptInfo(int i) const;
	CvInfoBase* getCityTabInfo(int i) const;
	CvInfoBase* getCalendarInfo(int i) const;
	CvInfoBase* getGameOptionInfo(int i) const;
	CvInfoBase* getMPOptionInfo(int i) const;
	CvInfoBase* getForceControlInfo(int i) const;
	CvInfoBase* getSeasonInfo(int i) const;
	CvInfoBase* getMonthInfo(int i) const;
	CvInfoBase* getDenialInfo(int i) const;
	CvQuestInfo* getQuestInfo(int i) const;
	CvTutorialInfo* getTutorialInfo(int i) const;
	CvEventTriggerInfo* getEventTriggerInfo(int i) const;
	CvEventInfo* getEventInfo(int i) const;
	CvEspionageMissionInfo* getEspionageMissionInfo(int i) const;
	CvHurryInfo* getHurryInfo(int i) const;
	CvPlayerOptionInfo* getPlayerOptionInfo(int i) const;
	CvPlayerOptionInfo* getPlayerOptionsInfoByIndex(int i) const;

	CvGraphicOptionInfo* getGraphicOptionInfo(int i) const;
	CvGraphicOptionInfo* getGraphicOptionsInfoByIndex(int i) const;

	// ArtInfos
	CvArtInfoInterface* getInterfaceArtInfo(int i) const;
	CvArtInfoMovie* getMovieArtInfo(int i) const;
	CvArtInfoMisc* getMiscArtInfo(int i) const;
	CvArtInfoUnit* getUnitArtInfo(int i) const;
	CvArtInfoBuilding* getBuildingArtInfo(int i) const;
	CvArtInfoCivilization* getCivilizationArtInfo(int i) const;
	CvArtInfoLeaderhead* getLeaderheadArtInfo(int i) const;
	CvArtInfoBonus* getBonusArtInfo(int i) const;
	CvArtInfoImprovement* getImprovementArtInfo(int i) const;
	CvArtInfoTerrain* getTerrainArtInfo(int i) const;
	CvArtInfoFeature* getFeatureArtInfo(int i) const;


	// Structs

	const char* getEntityEventTypes(int i) const { return GC.getEntityEventTypes((EntityEventTypes) i); }
	const char* getAnimationOperatorTypes(int i) const { return GC.getAnimationOperatorTypes((AnimationOperatorTypes) i); }
	const char* getFunctionTypes(int i) const { return GC.getFunctionTypes((FunctionTypes) i); }
	const char* getFlavorTypes(int i) const { return GC.getFlavorTypes((FlavorTypes) i); }
	const char* getArtStyleTypes(int i) const { return GC.getArtStyleTypes((ArtStyleTypes) i); }
	const char* getCitySizeTypes(int i) const { return GC.getCitySizeTypes(i); }
	const char* getContactTypes(int i) const { return GC.getContactTypes((ContactTypes) i); }
	const char* getDiplomacyPowerTypes(int i) const { return GC.getDiplomacyPowerTypes((DiplomacyPowerTypes) i); }
	const char *getFootstepAudioTypes(int i) { return GC.getFootstepAudioTypes(i); }
	const char *getFootstepAudioTags(int i) { return GC.getFootstepAudioTags(i); }

	int getNumEffectInfos() const { return GC.getNumEffectInfos(); }
	int getNumTerrainInfos() const { return GC.getNumTerrainInfos(); }
	int getNumSpecialBuildingInfos() const { return GC.getNumSpecialBuildingInfos(); }
	int getNumBonusInfos() const { return GC.getNumBonusInfos(); };
	int getNumPlayableCivilizationInfos() const { return GC.getNumPlayableCivilizationInfos(); }
	int getNumCivilizatonInfos() const { return GC.getNumCivilizationInfos(); }
	int getNumLeaderHeadInfos() const { return GC.getNumLeaderHeadInfos(); }
	int getNumTraitInfos() const { return GC.getNumTraitInfos(); }
	int getNumUnitInfos() const { return GC.getNumUnitInfos(); }
	int getNumSpecialUnitInfos() const { return GC.getNumSpecialUnitInfos(); }
	int getNumRouteInfos() const { return GC.getNumRouteInfos(); }
	int getNumFeatureInfos() const { return GC.getNumFeatureInfos(); }
	int getNumImprovementInfos() const { return GC.getNumImprovementInfos(); }
	int getNumGoodyInfos() const { return GC.getNumGoodyInfos(); }
	int getNumBuildInfos() const { return GC.getNumBuildInfos(); }
	int getNumHandicapInfos() const { return GC.getNumHandicapInfos(); }
	int getNumGameSpeedInfos() const { return GC.getNumGameSpeedInfos(); }
	int getNumTurnTimerInfos() const { return GC.getNumTurnTimerInfos(); }
	int getNumBuildingClassInfos() const { return GC.getNumBuildingClassInfos(); }
	int getNumBuildingInfos() const { return GC.getNumBuildingInfos(); }
	int getNumUnitClassInfos() const { return GC.getNumUnitClassInfos(); }
	int getNumUnitCombatInfos() const { return GC.getNumUnitCombatInfos(); }
	int getNumAutomateInfos() const { return GC.getNumAutomateInfos(); }
	int getNumCommandInfos() const { return GC.getNumCommandInfos(); }
	int getNumControlInfos() const { return GC.getNumControlInfos(); }
	int getNumMissionInfos() const { return GC.getNumMissionInfos(); }
	int getNumActionInfos() const { return GC.getNumActionInfos(); }
	int getNumPromotionInfos() const { return GC.getNumPromotionInfos(); }
	int getNumTechInfos() const { return GC.getNumTechInfos(); }
	int getNumReligionInfos() const { return GC.getNumReligionInfos(); }
	int getNumCorporationInfos() const { return GC.getNumCorporationInfos(); }
	int getNumSpecialistInfos() const { return GC.getNumSpecialistInfos(); }
	int getNumCivicInfos() const { return GC.getNumCivicInfos(); }
	int getNumDiplomacyInfos() const { return GC.getNumDiplomacyInfos(); }
	int getNumCivicOptionInfos() const { return GC.getNumCivicOptionInfos(); }
	int getNumProjectInfos() const { return GC.getNumProjectInfos(); }
	int getNumVoteInfos() const { return GC.getNumVoteInfos(); }
	int getNumProcessInfos() const { return GC.getNumProcessInfos(); }
	int getNumEmphasizeInfos() const { return GC.getNumEmphasizeInfos(); }
	int getNumHurryInfos() const { return GC.getNumHurryInfos(); }
	int getNumUpkeepInfos() const { return GC.getNumUpkeepInfos(); }
	int getNumCultureLevelInfos() const { return GC.getNumCultureLevelInfos(); }
	int getNumEraInfos() const { return GC.getNumEraInfos(); }
	int getNumVictoryInfos() const { return GC.getNumVictoryInfos(); }
	int getNumWorldInfos() const { return GC.getNumWorldInfos(); }
	int getNumSeaLevelInfos() const { return GC.getNumSeaLevelInfos(); }
	int getNumClimateInfos() const { return GC.getNumClimateInfos(); }
	int getNumConceptInfos() const { return GC.getNumConceptInfos(); }
	int getNumNewConceptInfos() const { return GC.getNumNewConceptInfos(); }
	int getNumCityTabInfos() const { return GC.getNumCityTabInfos(); }
	int getNumCalendarInfos() const { return GC.getNumCalendarInfos(); }
	int getNumPlayerOptionInfos() const { return GC.getNumPlayerOptionInfos(); }
	int getNumGameOptionInfos() const { return GC.getNumGameOptionInfos(); }
	int getNumMPOptionInfos() const { return GC.getNumMPOptionInfos(); }
	int getNumForceControlInfos() const { return GC.getNumForceControlInfos(); }
	int getNumSeasonInfos() const { return GC.getNumSeasonInfos(); }
	int getNumMonthInfos() const { return GC.getNumMonthInfos(); }
	int getNumDenialInfos() const { return GC.getNumDenialInfos(); }
	int getNumQuestInfos() const { return GC.getNumQuestInfos(); }
	int getNumTutorialInfos() const { return GC.getNumTutorialInfos(); }
	int getNumEventTriggerInfos() const { return GC.getNumEventTriggerInfos(); }
	int getNumEventInfos() const { return GC.getNumEventInfos(); }
	int getNumEspionageMissionInfos() const { return GC.getNumEspionageMissionInfos(); }
	int getNumHints() const { return GC.getNumHints(); }
	int getNumMainMenus() const { return GC.getNumMainMenus(); }
	int getNumInvisibleInfos() const { return GC.getNumInvisibleInfos(); }
	int getNumVoteSourceInfos() const { return GC.getNumVoteSourceInfos(); }

	// ArtInfos
	int getNumInterfaceArtInfos() const { return ARTFILEMGR.getNumInterfaceArtInfos(); }
	int getNumMovieArtInfos() const { return ARTFILEMGR.getNumMovieArtInfos(); }
	int getNumMiscArtInfos() const { return ARTFILEMGR.getNumMiscArtInfos(); }
	int getNumUnitArtInfos() const { return ARTFILEMGR.getNumUnitArtInfos(); }
	int getNumBuildingArtInfos() const { return ARTFILEMGR.getNumBuildingArtInfos(); }
	int getNumCivilizationArtInfos() const { return ARTFILEMGR.getNumCivilizationArtInfos(); }
	int getNumLeaderheadArtInfos() const { return ARTFILEMGR.getNumLeaderheadArtInfos(); }
	int getNumImprovementArtInfos() const { return ARTFILEMGR.getNumImprovementArtInfos(); }
	int getNumBonusArtInfos() const { return ARTFILEMGR.getNumBonusArtInfos(); }
	int getNumTerrainArtInfos() const { return ARTFILEMGR.getNumTerrainArtInfos(); }
	int getNumFeatureArtInfos() const { return ARTFILEMGR.getNumFeatureArtInfos(); }
	int getNumAnimationPathInfos() const { return GC.getNumAnimationPathInfos(); }
	int getNumAnimationCategoryInfos() const { return GC.getNumAnimationCategoryInfos(); }
    int getNumUnitArtStyleTypeInfos() const { return GC.getNumUnitArtStyleTypeInfos(); }


	int getNumEntityEventTypes() const { return GC.getNumEntityEventTypes(); }
	int getNumAnimationOperatorTypes() const { return GC.getNumAnimationOperatorTypes(); }
	int getNumArtStyleTypes() const { return GC.getNumArtStyleTypes(); }
	int getNumFlavorTypes() const { return GC.getNumFlavorTypes(); }
	int getNumCitySizeTypes() const { return GC.getNumCitySizeTypes(); }
	int getNumFootstepAudioTypes() const { return GC.getNumFootstepAudioTypes(); }

	//////////////////////
	// Globals Defines
	//////////////////////

	CyVariableSystem* getCyDefinesVarSystem();
	int getDefineINT( const char * szName ) const { return GC.getDefineINT( szName ); }
	float getDefineFLOAT( const char * szName ) const { return GC.getDefineFLOAT( szName ); }
	const char * getDefineSTRING( const char * szName ) const { return GC.getDefineSTRING( szName ); }
	void setDefineINT( const char * szName, int iValue ) { return GC.setDefineINT( szName, iValue ); }
	void setDefineFLOAT( const char * szName, float fValue ) { return GC.setDefineFLOAT( szName, fValue ); }
	void setDefineSTRING( const char * szName, const char * szValue ) { return GC.setDefineSTRING( szName, szValue ); }

	int getMOVE_DENOMINATOR() const { return GC.getMOVE_DENOMINATOR(); }
	int getNUM_UNIT_PREREQ_OR_BONUSES() const { return GC.getNUM_UNIT_PREREQ_OR_BONUSES(); }
	int getNUM_BUILDING_PREREQ_OR_BONUSES() const { return GC.getNUM_BUILDING_PREREQ_OR_BONUSES(); }
	int getFOOD_CONSUMPTION_PER_POPULATION() const { return GC.getFOOD_CONSUMPTION_PER_POPULATION(); }
	int getMAX_HIT_POINTS() const { return GC.getMAX_HIT_POINTS(); }
	int getHILLS_EXTRA_DEFENSE() const { return GC.getHILLS_EXTRA_DEFENSE(); }
	int getRIVER_ATTACK_MODIFIER() const { return GC.getRIVER_ATTACK_MODIFIER(); }
	int getAMPHIB_ATTACK_MODIFIER() const { return GC.getAMPHIB_ATTACK_MODIFIER(); }
	int getHILLS_EXTRA_MOVEMENT() const { return GC.getHILLS_EXTRA_MOVEMENT(); }
	int getMAX_PLOT_LIST_ROWS() const { return GC.getMAX_PLOT_LIST_ROWS(); }
	int getUNIT_MULTISELECT_MAX() const { return GC.getUNIT_MULTISELECT_MAX(); }
	int getPERCENT_ANGER_DIVISOR() const { return GC.getPERCENT_ANGER_DIVISOR(); }
	int getEVENT_MESSAGE_TIME() const { return GC.getEVENT_MESSAGE_TIME(); }
	int getROUTE_FEATURE_GROWTH_MODIFIER() const { return GC.getROUTE_FEATURE_GROWTH_MODIFIER(); }
	int getFEATURE_GROWTH_MODIFIER() const { return GC.getFEATURE_GROWTH_MODIFIER(); }
	int getMIN_CITY_RANGE() const { return GC.getMIN_CITY_RANGE(); }
	int getCITY_MAX_NUM_BUILDINGS() const { return GC.getCITY_MAX_NUM_BUILDINGS(); }
	int getNUM_UNIT_AND_TECH_PREREQS() const { return GC.getNUM_UNIT_AND_TECH_PREREQS(); }
	int getNUM_AND_TECH_PREREQS() const { return GC.getNUM_AND_TECH_PREREQS(); }
	int getNUM_OR_TECH_PREREQS() const { return GC.getNUM_OR_TECH_PREREQS(); }
	int getLAKE_MAX_AREA_SIZE() const { return GC.getLAKE_MAX_AREA_SIZE(); }
	int getNUM_ROUTE_PREREQ_OR_BONUSES() const { return GC.getNUM_ROUTE_PREREQ_OR_BONUSES(); }
	int getNUM_BUILDING_AND_TECH_PREREQS() const { return GC.getNUM_BUILDING_AND_TECH_PREREQS(); }
	int getMIN_WATER_SIZE_FOR_OCEAN() const { return GC.getMIN_WATER_SIZE_FOR_OCEAN(); }
	int getFORTIFY_MODIFIER_PER_TURN() const { return GC.getFORTIFY_MODIFIER_PER_TURN(); }
	int getMAX_CITY_DEFENSE_DAMAGE() const { return GC.getMAX_CITY_DEFENSE_DAMAGE(); }
	int getNUM_CORPORATION_PREREQ_BONUSES() const { return GC.getNUM_CORPORATION_PREREQ_BONUSES(); }
	int getPEAK_SEE_THROUGH_CHANGE() const { return GC.getPEAK_SEE_THROUGH_CHANGE(); }
	int getHILLS_SEE_THROUGH_CHANGE() const { return GC.getHILLS_SEE_THROUGH_CHANGE(); }
	int getSEAWATER_SEE_FROM_CHANGE() const { return GC.getSEAWATER_SEE_FROM_CHANGE(); }
	int getPEAK_SEE_FROM_CHANGE() const { return GC.getPEAK_SEE_FROM_CHANGE(); }
	int getHILLS_SEE_FROM_CHANGE() const { return GC.getHILLS_SEE_FROM_CHANGE(); }
	int getUSE_SPIES_NO_ENTER_BORDERS() const { return GC.getUSE_SPIES_NO_ENTER_BORDERS(); }

	float getCAMERA_MIN_YAW() const { return GC.getCAMERA_MIN_YAW(); }
	float getCAMERA_MAX_YAW() const { return GC.getCAMERA_MAX_YAW(); }
	float getCAMERA_FAR_CLIP_Z_HEIGHT() const { return GC.getCAMERA_FAR_CLIP_Z_HEIGHT(); }
	float getCAMERA_MAX_TRAVEL_DISTANCE() const { return GC.getCAMERA_MAX_TRAVEL_DISTANCE(); }
	float getCAMERA_START_DISTANCE() const { return GC.getCAMERA_START_DISTANCE(); }
	float getAIR_BOMB_HEIGHT() const { return GC.getAIR_BOMB_HEIGHT(); }
	float getPLOT_SIZE() const { return GC.getPLOT_SIZE(); }
	float getCAMERA_SPECIAL_PITCH() const { return GC.getCAMERA_SPECIAL_PITCH(); }
	float getCAMERA_MAX_TURN_OFFSET() const { return GC.getCAMERA_MAX_TURN_OFFSET(); }
	float getCAMERA_MIN_DISTANCE() const { return GC.getCAMERA_MIN_DISTANCE(); }
	float getCAMERA_UPPER_PITCH() const { return GC.getCAMERA_UPPER_PITCH(); }
	float getCAMERA_LOWER_PITCH() const { return GC.getCAMERA_LOWER_PITCH(); }
	float getFIELD_OF_VIEW() const { return GC.getFIELD_OF_VIEW(); }
	float getSHADOW_SCALE() const { return GC.getSHADOW_SCALE(); }
	float getUNIT_MULTISELECT_DISTANCE() const { return GC.getUNIT_MULTISELECT_DISTANCE(); }

	int getMAX_CIV_PLAYERS() const { return GC.getMAX_CIV_PLAYERS(); }
	int getMAX_PLAYERS() const { return GC.getMAX_PLAYERS(); }
	int getMAX_CIV_TEAMS() const { return GC.getMAX_CIV_TEAMS(); }
	int getMAX_TEAMS() const { return GC.getMAX_TEAMS(); }
	int getBARBARIAN_PLAYER() const { return GC.getBARBARIAN_PLAYER(); }
	int getBARBARIAN_TEAM() const { return GC.getBARBARIAN_TEAM(); }
	int getINVALID_PLOT_COORD() const { return GC.getINVALID_PLOT_COORD(); }
	int getNUM_CITY_PLOTS() const { return GC.getNUM_CITY_PLOTS(); }
	int getCITY_HOME_PLOT() const { return GC.getCITY_HOME_PLOT(); }

	// 3Miro: set balance parameters
	void setStartingTurn( int iCiv, int iVal );
	int getStartingTurn( int iCiv ); // for debug purposes

	void setGrowthModifiersAI( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop );
	void setProductionModifiersAI( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch );
	void setSupportModifiersAI( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic );
	
	void setGrowthModifiersHu( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop );
	void setProductionModifiersHu( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch );
	void setSupportModifiersHu( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic );
	
	void setInitialPopulation( int iCiv, int iInitPop );
	void setInitialBuilding( int iCiv, int iBuilding, bool w );

	void setCityClusterAI( int iCiv, int iTop, int iBottom, int iMinus );
	void setCityWarDistanceAI( int iCiv, int iVal );
	void setTechPreferenceAI( int iCiv, int iTech, int iVal );
	void setDiplomacyModifiers( int iCiv1, int iCiv2, int iVal );

	void setUP( int iCiv, int iPower, int iParameter );
	bool hasUP( int iCiv, int iPower );

	void setSettlersMap( int iCiv, int y, int x, int iVal );
	void setWarsMap( int iCiv, int y, int x, int iVal );
	void setSizeNPlayers( int iMaxX, int iMaxY, int iNumPlayers, int iAllPlayers, int iNumTechs, int iNumBuildings, int iNumReligions );
	// note that the direction of y reversed and the notation is different from the standard (x,y)

	void setIndependnets( int iIndyStart, int iIndyEnd, int iBarb );
	// sets the indy and barb players. The Indy players are in a block from start to end

	void setPapalPlayer( int iCiv, int iReligion );

	// 3Miro: UHV optimizations exposed to Python
	bool isLargestCity( int x, int y );
	bool isTopCultureCity( int x, int y );
	int doesOwnCities( int iCiv, int BLx, int BLy, int TRx, int TRy );
	int doesOwnOrVassalCities( int iCiv, int BLx, int BLy, int TRx, int TRy );
	bool doesHaveOtherReligion( int BLx, int BLy, int TRx, int TRy, int AllowR );
	int countOwnedCities( int iCiv, int BLx, int BLy, int TRx, int TRy );
	int countCitiesLostTo( int iCiv, int iNewOwner ); 
	bool safeMotherland( int iCiv );
	bool canSeeAllTerrain( int iCiv, int iTerrain );
	bool controlMostTeritory( int iCiv, int BLx, int BLy, int TRx, int TRy );
	void damageFromBuilding( int iPlayer, int iBuilding, int iFoeDamage, int iBarbDamage );

	// 3Miro: set Core and Normal Areas
	void setCoreNormal( int iCiv, int iCBLx, int iCBLy, int iCTRx, int iCTRy, int iNBLx, int iNBLy, int iNTRx, int iNTRy, int iCCE, int iCNE );
	// for iCiv, int Core Bottol Left x, ... int Normal Top Right y, int Count Core Exceptions, int Count Normal Exceptions
	void addCoreException( int iCiv, int x, int y );
	void addNormalException( int iCiv, int x, int y );

	//int getProsecutionCount( int iCiv );
	//void setProsecutionCount( int iCiv, int iCount );
	void setProsecutorReligions( int iProsecutor, int iProsecutorClass );

	// 3Miro: set Saint AI
	void setSaintParameters( int iUnitID, int iBenefit, int iTreshhold1, int iTreshhold3 );

	// city stability loop
	int cityStabilityExpansion( int iPlayer, int iFCity );
	int cityStabilityPenalty( int iPlayer, int iAnger, int iHealth, int iReligion, int iLarge, int iHurry, int iNoMilitary, int iWarW, int iFReligion, int iFCulture, int iPerCityCap );


	// 3Miro: do Stability map sweep
	void calcLastOwned();
	int getlOwnedPlots( int iCiv );
	int getlOwnedCities( int iCiv );

	// 3Miro: AI atitude stuff
	int getRelationTowards( int iWho, int iTowards );

	// 3Miro: GlobalWarming
	void setGlobalWarming( bool bWhat );

	// 3Miro: religion spread factors
	void setReligionSpread( int iCiv, int iReligion, int iSpread );

	// 3Miro: set colonyAI modifier (doesn't work)
	void setColonyAIModifier( int iCiv, int iModifier );

	// 3Miro: set the parameters for the schism
	void setSchism( int iReligionA, int iReligionB, int iTurn );

	// 3Miro: set Holiest city (Jerusalem)
	void setHoliestCity( int iCityX, int iCityY );

	// 3MiroFaith: set religious benefits from Faith
	void setReligionBenefit( int iReligion, int iBenefit, int iParameter, int iCap );

	// 3Miro: set starting workers
	void setStartingWorkers( int iCiv, int iWorkers );

	// 3Miro: count the cities outside the core
	int countCitiesOutside( int iCiv );

	// 3Miro: set strategic tile
	void setStrategicTile( int iCiv, int iX, int iY );

	// 3Miro: set fast terrain (i.e. ships move fast over ocean)
	void setFastTerrain( int iFastTerrain );

	// 3Miro: set building preference
	void setBuildingPref( int iCiv, int iBuilding, int iPref );

	// 3Miro: set Autorun Hack
	void setAutorunHack( int iUnit, int iX, int iY );

	// 3Miro: set Building + Civic combo
	void setBuildingCivicCommerseCombo1( int iCode );
	void setBuildingCivicCommerseCombo2( int iCode );
	void setBuildingCivicCommerseCombo3( int iCode );

	// 3Miro: Psycho AI cheat, this gives a AI player gratiinsentive to attack a city at X, Y and it greatly improves the odds of success
	void setPsychoAICheat( int iPlayer, int iX, int iY );

	// 3Miro: set historical enemy AI cheat
	void setHistoricalEnemyAICheat( int iAttacker, int iDefender, int iChange );

	// 3Miro: set timeline Tech modifiers, strong gain and penalty for teching out of historical order
	void setTimelineTechModifiers( int iTPTop, int iTPBottom, int iTPCap, int iTBTop, int iTBBottom, int iTBCap );
	void setTimelineTechDateForTech( int iTech, int iTurn );

	void setProvince( int iX, int iY, int iProvince ); // set the province at tile (iX,iY)
	void createProvinceCrossreferenceList(); // call this after setting all provinces

	void setCultureImmume( int iProvince, int iPlayerException, int iNumTurns ); // make a province immune to culture not comming from iPlayerException
	void setProvinceTypeNumber( int iNum ); // set the number of province types
	void setProvinceTypeParams( int iType, int iSettlerValue, int iWarValue, int iCultureTop, int iCultureBottom ); // set the number of province types

	void setVassalagaeCondition( int iPlayer, int iWhoTo, int iCondition, int iProvinceType );
	// there is only one iProvinceType, even though it is being set every time (only the last one counts). 
	// If iCondition is 1, iProvinceType still needs to be set

};

#endif	// CyGlobalContext_h
