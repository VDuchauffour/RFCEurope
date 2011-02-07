//
// Python wrapper class for global vars and fxns
// Author - Mustafa Thamer
//

#include "CvGameCoreDLL.h"
#include "CyGlobalContext.h"
#include "CyGame.h"
#include "CyPlayer.h"
#include "CyMap.h"
#include "CvGlobals.h"
#include "CvPlayerAI.h"
#include "CvGameAI.h"
//#include "CvStructs.h"
#include "CvInfos.h"
#include "CyTeam.h"
#include "CvTeamAI.h"
#include "CyArtFileMgr.h"

// 3Miro: add the header with the balance information
#include "CvRhyes.h"

CyGlobalContext::CyGlobalContext()
{
}

CyGlobalContext::~CyGlobalContext()
{
}

CyGlobalContext& CyGlobalContext::getInstance()
{
	static CyGlobalContext globalContext;
	return globalContext;
}

bool CyGlobalContext::isDebugBuild() const
{
#ifdef _DEBUG
	return true;
#else
	return false;
#endif
}

CyGame* CyGlobalContext::getCyGame() const
{
	static CyGame cyGame(&GC.getGameINLINE());
	return &cyGame;
}


CyMap* CyGlobalContext::getCyMap() const
{
	static CyMap cyMap(&GC.getMapINLINE());
	return &cyMap;
}


CyPlayer* CyGlobalContext::getCyPlayer(int idx)
{
	static CyPlayer cyPlayers[MAX_PLAYERS];
	static bool bInit=false;

	if (!bInit)
	{
		int i;
		for(i=0;i<MAX_PLAYERS;i++)
			cyPlayers[i]=CyPlayer(&GET_PLAYER((PlayerTypes)i));
		bInit=true;
	}

	FAssert(idx>=0);
	FAssert(idx<MAX_PLAYERS);

	return idx < MAX_PLAYERS && idx != NO_PLAYER ? &cyPlayers[idx] : NULL;
}


CyPlayer* CyGlobalContext::getCyActivePlayer()
{
	PlayerTypes pt = GC.getGameINLINE().getActivePlayer();
	return pt != NO_PLAYER ? getCyPlayer(pt) : NULL;
}


CvRandom& CyGlobalContext::getCyASyncRand() const
{
	return GC.getASyncRand();
}

CyTeam* CyGlobalContext::getCyTeam(int i)
{
	static CyTeam cyTeams[MAX_TEAMS];
	static bool bInit=false;

	if (!bInit)
	{
		int j;
		for(j=0;j<MAX_TEAMS;j++)
		{
			cyTeams[j]=CyTeam(&GET_TEAM((TeamTypes)j));
		}
		bInit = true;
	}

	return i<MAX_TEAMS ? &cyTeams[i] : NULL;
}


CvEffectInfo* CyGlobalContext::getEffectInfo(int /*EffectTypes*/ i) const
{
	return (i>=0 && i<GC.getNumEffectInfos()) ? &GC.getEffectInfo((EffectTypes) i) : NULL;
}

CvTerrainInfo* CyGlobalContext::getTerrainInfo(int /*TerrainTypes*/ i) const
{
	return (i>=0 && i<GC.getNumTerrainInfos()) ? &GC.getTerrainInfo((TerrainTypes) i) : NULL;
}

CvBonusClassInfo* CyGlobalContext::getBonusClassInfo(int /*BonusClassTypes*/ i) const
{
	return (i > 0 && i < GC.getNumBonusClassInfos() ? &GC.getBonusClassInfo((BonusClassTypes) i) : NULL);
}


CvBonusInfo* CyGlobalContext::getBonusInfo(int /*(BonusTypes)*/ i) const
{
	return (i>=0 && i<GC.getNumBonusInfos()) ? &GC.getBonusInfo((BonusTypes) i) : NULL;
}

CvFeatureInfo* CyGlobalContext::getFeatureInfo(int i) const
{
	return (i>=0 && i<GC.getNumFeatureInfos()) ? &GC.getFeatureInfo((FeatureTypes) i) : NULL;
}

CvCivilizationInfo* CyGlobalContext::getCivilizationInfo(int i) const
{
	return (i>=0 && i<GC.getNumCivilizationInfos()) ? &GC.getCivilizationInfo((CivilizationTypes) i) : NULL;
}


CvLeaderHeadInfo* CyGlobalContext::getLeaderHeadInfo(int i) const
{
	return (i>=0 && i<GC.getNumLeaderHeadInfos()) ? &GC.getLeaderHeadInfo((LeaderHeadTypes) i) : NULL;
}


CvTraitInfo* CyGlobalContext::getTraitInfo(int i) const
{
	return (i>=0 && i<GC.getNumTraitInfos()) ? &GC.getTraitInfo((TraitTypes) i) : NULL;
}


CvUnitInfo* CyGlobalContext::getUnitInfo(int i) const
{
	return (i>=0 && i<GC.getNumUnitInfos()) ? &GC.getUnitInfo((UnitTypes) i) : NULL;
}

CvSpecialUnitInfo* CyGlobalContext::getSpecialUnitInfo(int i) const
{
	return (i>=0 && i<GC.getNumSpecialUnitInfos()) ? &GC.getSpecialUnitInfo((SpecialUnitTypes) i) : NULL;
}

CvYieldInfo* CyGlobalContext::getYieldInfo(int i) const
{
	return (i>=0 && i<NUM_YIELD_TYPES) ? &GC.getYieldInfo((YieldTypes) i) : NULL;
}


CvCommerceInfo* CyGlobalContext::getCommerceInfo(int i) const
{
	return (i>=0 && i<NUM_COMMERCE_TYPES) ? &GC.getCommerceInfo((CommerceTypes) i) : NULL;
}


CvRouteInfo* CyGlobalContext::getRouteInfo(int i) const
{
	return (i>=0 && i<GC.getNumRouteInfos()) ? &GC.getRouteInfo((RouteTypes) i) : NULL;
}


CvImprovementInfo* CyGlobalContext::getImprovementInfo(int i) const
{
	return (i>=0 && i<GC.getNumImprovementInfos()) ? &GC.getImprovementInfo((ImprovementTypes) i) : NULL;
}


CvGoodyInfo* CyGlobalContext::getGoodyInfo(int i) const
{
	return (i>=0 && i<GC.getNumGoodyInfos()) ? &GC.getGoodyInfo((GoodyTypes) i) : NULL;
}


CvBuildInfo* CyGlobalContext::getBuildInfo(int i) const
{
	return (i>=0 && i<GC.getNumBuildInfos()) ? &GC.getBuildInfo((BuildTypes) i) : NULL;
}


CvHandicapInfo* CyGlobalContext::getHandicapInfo(int i) const
{
	return (i>=0 && i<GC.getNumHandicapInfos()) ? &GC.getHandicapInfo((HandicapTypes) i) : NULL;
}


CvBuildingClassInfo* CyGlobalContext::getBuildingClassInfo(int i) const
{
	return (i>=0 && i<GC.getNumBuildingClassInfos()) ? &GC.getBuildingClassInfo((BuildingClassTypes) i) : NULL;
}


CvBuildingInfo* CyGlobalContext::getBuildingInfo(int i) const
{
	return (i>=0 && i<GC.getNumBuildingInfos()) ? &GC.getBuildingInfo((BuildingTypes) i) : NULL;
}

CvUnitClassInfo* CyGlobalContext::getUnitClassInfo(int i) const
{
	return (i>=0 && i<GC.getNumUnitClassInfos()) ? &GC.getUnitClassInfo((UnitClassTypes) i) : NULL;
}


CvInfoBase* CyGlobalContext::getUnitCombatInfo(int i) const
{
	return (i>=0 && i<GC.getNumUnitCombatInfos()) ? &GC.getUnitCombatInfo((UnitCombatTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getDomainInfo(int i) const
{
	return (i>=0 && i<NUM_DOMAIN_TYPES) ? &GC.getDomainInfo((DomainTypes)i) : NULL;
}


CvActionInfo* CyGlobalContext::getActionInfo(int i) const
{
	return (i>=0 && i<GC.getNumActionInfos()) ? &GC.getActionInfo(i) : NULL;
}

CvAutomateInfo* CyGlobalContext::getAutomateInfo(int i) const
{
	return (i>=0 && i<GC.getNumAutomateInfos()) ? &GC.getAutomateInfo(i) : NULL;
}

CvCommandInfo* CyGlobalContext::getCommandInfo(int i) const
{
	return (i>=0 && i<NUM_COMMAND_TYPES) ? &GC.getCommandInfo((CommandTypes)i) : NULL;
}

CvControlInfo* CyGlobalContext::getControlInfo(int i) const
{
	return (i>=0 && i<NUM_CONTROL_TYPES) ? &GC.getControlInfo((ControlTypes)i) : NULL;
}

CvMissionInfo* CyGlobalContext::getMissionInfo(int i) const
{
	return (i>=0 && i<NUM_MISSION_TYPES) ? &GC.getMissionInfo((MissionTypes) i) : NULL;
}

CvPromotionInfo* CyGlobalContext::getPromotionInfo(int i) const
{
	return (i>=0 && i<GC.getNumPromotionInfos()) ? &GC.getPromotionInfo((PromotionTypes) i) : NULL;
}


CvTechInfo* CyGlobalContext::getTechInfo(int i) const
{
	return (i>=0 && i<GC.getNumTechInfos()) ? &GC.getTechInfo((TechTypes) i) : NULL;
}


CvSpecialBuildingInfo* CyGlobalContext::getSpecialBuildingInfo(int i) const
{
	return (i>=0 && i<GC.getNumSpecialBuildingInfos()) ? &GC.getSpecialBuildingInfo((SpecialBuildingTypes) i) : NULL;
}


CvReligionInfo* CyGlobalContext::getReligionInfo(int i) const
{
	return (i>=0 && i<GC.getNumReligionInfos()) ? &GC.getReligionInfo((ReligionTypes) i) : NULL;
}


CvCorporationInfo* CyGlobalContext::getCorporationInfo(int i) const
{
	return (i>=0 && i<GC.getNumCorporationInfos()) ? &GC.getCorporationInfo((CorporationTypes) i) : NULL;
}


CvSpecialistInfo* CyGlobalContext::getSpecialistInfo(int i) const
{
	return (i>=0 && i<GC.getNumSpecialistInfos()) ? &GC.getSpecialistInfo((SpecialistTypes) i) : NULL;
}


CvCivicOptionInfo* CyGlobalContext::getCivicOptionInfo(int i) const
{
	return &GC.getCivicOptionInfo((CivicOptionTypes) i);
}


CvCivicInfo* CyGlobalContext::getCivicInfo(int i) const
{
	return &GC.getCivicInfo((CivicTypes) i);
}

CvDiplomacyInfo* CyGlobalContext::getDiplomacyInfo(int i) const
{
	return &GC.getDiplomacyInfo(i);
}

CvHurryInfo* CyGlobalContext::getHurryInfo(int i) const
{
	return (i>=0 && i<GC.getNumHurryInfos()) ? &GC.getHurryInfo((HurryTypes) i) : NULL;
}


CvProjectInfo* CyGlobalContext::getProjectInfo(int i) const
{
	return (i>=0 && i<GC.getNumProjectInfos()) ? &GC.getProjectInfo((ProjectTypes) i) : NULL;
}


CvVoteInfo* CyGlobalContext::getVoteInfo(int i) const
{
	return (i>=0 && i<GC.getNumVoteInfos()) ? &GC.getVoteInfo((VoteTypes) i) : NULL;
}


CvProcessInfo* CyGlobalContext::getProcessInfo(int i) const
{
	return (i>=0 && i<GC.getNumProcessInfos()) ? &GC.getProcessInfo((ProcessTypes) i) : NULL;
}

CvAnimationPathInfo* CyGlobalContext::getAnimationPathInfo(int i) const
{
	return (i>=0 && i<GC.getNumAnimationPathInfos()) ? &GC.getAnimationPathInfo((AnimationPathTypes)i) : NULL;
}


CvEmphasizeInfo* CyGlobalContext::getEmphasizeInfo(int i) const
{
	return (i>=0 && i<GC.getNumEmphasizeInfos()) ? &GC.getEmphasizeInfo((EmphasizeTypes) i) : NULL;
}


CvCultureLevelInfo* CyGlobalContext::getCultureLevelInfo(int i) const
{
	return (i>=0 && i<GC.getNumCultureLevelInfos()) ? &GC.getCultureLevelInfo((CultureLevelTypes) i) : NULL;
}


CvUpkeepInfo* CyGlobalContext::getUpkeepInfo(int i) const
{
	return (i>=0 && i<GC.getNumUpkeepInfos()) ? &GC.getUpkeepInfo((UpkeepTypes) i) : NULL;
}


CvVictoryInfo* CyGlobalContext::getVictoryInfo(int i) const
{
	return (i>=0 && i<GC.getNumVictoryInfos()) ? &GC.getVictoryInfo((VictoryTypes) i) : NULL;
}


CvEraInfo* CyGlobalContext::getEraInfo(int i) const
{
	return (i>=0 && i<GC.getNumEraInfos()) ? &GC.getEraInfo((EraTypes) i) : NULL;
}


CvWorldInfo* CyGlobalContext::getWorldInfo(int i) const
{
	return (i>=0 && i<GC.getNumWorldInfos()) ? &GC.getWorldInfo((WorldSizeTypes) i) : NULL;
}


CvClimateInfo* CyGlobalContext::getClimateInfo(int i) const
{
	return (i>=0 && i<GC.getNumClimateInfos()) ? &GC.getClimateInfo((ClimateTypes) i) : NULL;
}


CvSeaLevelInfo* CyGlobalContext::getSeaLevelInfo(int i) const
{
	return (i>=0 && i<GC.getNumSeaLevelInfos()) ? &GC.getSeaLevelInfo((SeaLevelTypes) i) : NULL;
}


CvInfoBase* CyGlobalContext::getUnitAIInfo(int i) const
{
	return (i>=0 && i<NUM_UNITAI_TYPES) ? &GC.getUnitAIInfo((UnitAITypes)i) : NULL;
}


CvColorInfo* CyGlobalContext::getColorInfo(int i) const
{
	return (i>=0 && i<GC.getNumColorInfos()) ? &GC.getColorInfo((ColorTypes)i) : NULL;
}


int CyGlobalContext::getInfoTypeForString(const char* szInfoType) const
{
	return GC.getInfoTypeForString(szInfoType);
}


int CyGlobalContext::getTypesEnum(const char* szType) const
{
	return GC.getTypesEnum(szType);
}


CvPlayerColorInfo* CyGlobalContext::getPlayerColorInfo(int i) const
{
	return (i>=0 && i<GC.getNumPlayerColorInfos()) ? &GC.getPlayerColorInfo((PlayerColorTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getHints(int i) const
{
	return ((i >= 0 && i < GC.getNumHints()) ? &GC.getHints(i) : NULL);
}


CvMainMenuInfo* CyGlobalContext::getMainMenus(int i) const
{
	return ((i >= 0 && i < GC.getNumMainMenus()) ? &GC.getMainMenus(i) : NULL);
}


CvVoteSourceInfo* CyGlobalContext::getVoteSourceInfo(int i) const
{
	return ((i >= 0 && i < GC.getNumVoteSourceInfos()) ? &GC.getVoteSourceInfo((VoteSourceTypes)i) : NULL);
}


CvInfoBase* CyGlobalContext::getInvisibleInfo(int i) const
{
	return ((i >= 0 && i < GC.getNumInvisibleInfos()) ? &GC.getInvisibleInfo((InvisibleTypes)i) : NULL);
}


CvInfoBase* CyGlobalContext::getAttitudeInfo(int i) const
{
	return (i>=0 && i<NUM_ATTITUDE_TYPES) ? &GC.getAttitudeInfo((AttitudeTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getMemoryInfo(int i) const
{
	return (i>=0 && i<NUM_MEMORY_TYPES) ? &GC.getMemoryInfo((MemoryTypes)i) : NULL;
}


CvPlayerOptionInfo* CyGlobalContext::getPlayerOptionsInfoByIndex(int i) const
{
	return &GC.getPlayerOptionInfo((PlayerOptionTypes) i);
}


CvGraphicOptionInfo* CyGlobalContext::getGraphicOptionsInfoByIndex(int i) const
{
	return &GC.getGraphicOptionInfo((GraphicOptionTypes) i);
}


CvInfoBase* CyGlobalContext::getConceptInfo(int i) const
{
	return (i>=0 && i<GC.getNumConceptInfos()) ? &GC.getConceptInfo((ConceptTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getNewConceptInfo(int i) const
{
	return (i>=0 && i<GC.getNumNewConceptInfos()) ? &GC.getNewConceptInfo((NewConceptTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getCityTabInfo(int i) const
{
	return (i>=0 && i<GC.getNumCityTabInfos()) ? &GC.getCityTabInfo((CityTabTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getCalendarInfo(int i) const
{
	return (i>=0 && i<GC.getNumCalendarInfos()) ? &GC.getCalendarInfo((CalendarTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getGameOptionInfo(int i) const
{
	return (i>=0 && i<GC.getNumGameOptionInfos()) ? &GC.getGameOptionInfo((GameOptionTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getMPOptionInfo(int i) const
{
	return (i>=0 && i<GC.getNumMPOptionInfos()) ? &GC.getMPOptionInfo((MultiplayerOptionTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getForceControlInfo(int i) const
{
	return (i>=0 && i<GC.getNumForceControlInfos()) ? &GC.getForceControlInfo((ForceControlTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getSeasonInfo(int i) const
{
	return (i>=0 && i<GC.getNumSeasonInfos()) ? &GC.getSeasonInfo((SeasonTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getMonthInfo(int i) const
{
	return (i>=0 && i<GC.getNumMonthInfos()) ? &GC.getMonthInfo((MonthTypes)i) : NULL;
}


CvInfoBase* CyGlobalContext::getDenialInfo(int i) const
{
	return (i>=0 && i<GC.getNumDenialInfos()) ? &GC.getDenialInfo((DenialTypes)i) : NULL;
}


CvQuestInfo* CyGlobalContext::getQuestInfo(int i) const
{
	return (i>=0 && i<GC.getNumQuestInfos()) ? &GC.getQuestInfo(i) : NULL;
}


CvTutorialInfo* CyGlobalContext::getTutorialInfo(int i) const
{
	return (i>=0 && i<GC.getNumTutorialInfos()) ? &GC.getTutorialInfo(i) : NULL;
}


CvEventTriggerInfo* CyGlobalContext::getEventTriggerInfo(int i) const
{
	return (i>=0 && i<GC.getNumEventTriggerInfos()) ? &GC.getEventTriggerInfo((EventTriggerTypes)i) : NULL;
}


CvEventInfo* CyGlobalContext::getEventInfo(int i) const
{
	return (i>=0 && i<GC.getNumEventInfos()) ? &GC.getEventInfo((EventTypes)i) : NULL;
}


CvEspionageMissionInfo* CyGlobalContext::getEspionageMissionInfo(int i) const
{
	return (i>=0 && i<GC.getNumEspionageMissionInfos()) ? &GC.getEspionageMissionInfo((EspionageMissionTypes)i) : NULL;
}


CvUnitArtStyleTypeInfo* CyGlobalContext::getUnitArtStyleTypeInfo(int i) const
{
	return (i>=0 && i<GC.getNumUnitArtStyleTypeInfos()) ? &GC.getUnitArtStyleTypeInfo((UnitArtStyleTypes)i) : NULL;
}


CvArtInfoInterface* CyGlobalContext::getInterfaceArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumInterfaceArtInfos()) ? &ARTFILEMGR.getInterfaceArtInfo(i) : NULL;
}


CvArtInfoMovie* CyGlobalContext::getMovieArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumMovieArtInfos()) ? &ARTFILEMGR.getMovieArtInfo(i) : NULL;
}


CvArtInfoMisc* CyGlobalContext::getMiscArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumMiscArtInfos()) ? &ARTFILEMGR.getMiscArtInfo(i) : NULL;
}


CvArtInfoUnit* CyGlobalContext::getUnitArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumUnitArtInfos()) ? &ARTFILEMGR.getUnitArtInfo(i) : NULL;
}


CvArtInfoBuilding* CyGlobalContext::getBuildingArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumBuildingArtInfos()) ? &ARTFILEMGR.getBuildingArtInfo(i) : NULL;
}


CvArtInfoCivilization* CyGlobalContext::getCivilizationArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumCivilizationArtInfos()) ? &ARTFILEMGR.getCivilizationArtInfo(i) : NULL;
}


CvArtInfoLeaderhead* CyGlobalContext::getLeaderheadArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumLeaderheadArtInfos()) ? &ARTFILEMGR.getLeaderheadArtInfo(i) : NULL;
}


CvArtInfoBonus* CyGlobalContext::getBonusArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumBonusArtInfos()) ? &ARTFILEMGR.getBonusArtInfo(i) : NULL;
}


CvArtInfoImprovement* CyGlobalContext::getImprovementArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumImprovementArtInfos()) ? &ARTFILEMGR.getImprovementArtInfo(i) : NULL;
}


CvArtInfoTerrain* CyGlobalContext::getTerrainArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumTerrainArtInfos()) ? &ARTFILEMGR.getTerrainArtInfo(i) : NULL;
}


CvArtInfoFeature* CyGlobalContext::getFeatureArtInfo(int i) const
{
	return (i>=0 && i<ARTFILEMGR.getNumFeatureArtInfos()) ? &ARTFILEMGR.getFeatureArtInfo(i) : NULL;
}


CvGameSpeedInfo* CyGlobalContext::getGameSpeedInfo(int i) const
{
	return &(GC.getGameSpeedInfo((GameSpeedTypes) i));
}

CvTurnTimerInfo* CyGlobalContext::getTurnTimerInfo(int i) const
{
	return &(GC.getTurnTimerInfo((TurnTimerTypes) i));
}

// 3Miro: Balancing functions
void CyGlobalContext::setStartingTurn( int iCiv, int iVal ){
	/*if ( startingTurn == NULL ){
		startingTurn = new int[NUM_ALL_PLAYERS_B];
		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) startingTurn[i] = 0;
	};*/
	//GC.getGameINLINE().logMsg(" Set starting turn: %d  %d ",iCiv,iVal);
	startingTurn[iCiv] = iVal;
};

void CyGlobalContext::setCityClusterAI( int iCiv, int iTop, int iBottom, int iMinus ){
	/*if ( cityClusterTop == NULL || cityClusterBottom == NULL || cityClusterMinus == NULL ){
		cityClusterTop = new int[NUM_ALL_PLAYERS_B];
		cityClusterBottom = new int[NUM_ALL_PLAYERS_B];
		cityClusterMinus = new int[NUM_ALL_PLAYERS_B];
		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ){
			cityClusterTop[i] = 2;
			cityClusterBottom[i] = 3;
			cityClusterMinus[i] = 1;
		};
	};*/
	cityClusterTop[iCiv] = iTop;
	cityClusterBottom[iCiv] = iBottom;
	cityClusterMinus[iCiv] = iMinus;
};

void CyGlobalContext::setCityWarDistanceAI( int iCiv, int iVal ){
	/*if ( cityWarDistance == NULL ){
		cityWarDistance = new int[NUM_ALL_PLAYERS_B];
		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) cityWarDistance[i] = 1;
	};*/
	cityWarDistance[iCiv] = iVal;
};

void CyGlobalContext::setTechPreferenceAI( int iCiv, int iTech, int iVal ){
	/*if ( techPreferences == NULL ){
		techPreferences = new int* [NUM_ALL_PLAYERS_B];
		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) techPreferences[i] = new int[MAX_NUM_TECHS];
		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ )
			for ( int j=0; j<MAX_NUM_TECHS; j++ )
				techPreferences[i][j] = 100;
	};*/
	techPreferences[iCiv][iTech] = iVal;
};

void CyGlobalContext::setDiplomacyModifiers( int iCiv1, int iCiv2, int iVal ){
	/*if ( diplomacyModifiers == NULL ){
		diplomacyModifiers = new int* [NUM_ALL_PLAYERS_B];
		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) diplomacyModifiers[i] = new int[NUM_ALL_PLAYERS_B];
		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ )
			for ( int j=0; j<NUM_ALL_PLAYERS_B; j++ )
				diplomacyModifiers[i][j] = 0;
	};*/
	diplomacyModifiers[iCiv1][iCiv2] = iVal;
	//diplomacyModifiers[iCiv2][iCiv1] = iVal;
};

void CyGlobalContext::setUP( int iCiv, int iPower, int iParameter ){
	//UniquePowers[iCiv][iPower] = 1;
	/*if ( UniquePowers == NULL ){
		UniquePowers = new int* [NUM_ALL_PLAYERS_B];
		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) UniquePowers[i] = new int[UP_TOTAL_NUM];
		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ )
			for ( int j=0; j<UP_TOTAL_NUM; j++ )
				UniquePowers[i][j] = 0;
	};*/
	//UniquePowers[iCiv][iPower] = 1;
	UniquePowers[iCiv *UP_TOTAL_NUM + iPower ] = iParameter;
};

bool CyGlobalContext::hasUP( int iCiv, int iPower ){
	if ( UniquePowers[iCiv *UP_TOTAL_NUM + iPower ] >-1 )
		return true;
	return false;
};

void CyGlobalContext::setSizeNPlayers( int iMaxX, int iMaxY, int iNumPlayers, int iAllPlayers, int iNumTechs, int iNumBuildings, int iNumReligions ){
	EARTH_X = iMaxX;
	EARTH_Y = iMaxY;
	NUM_MAJOR_PLAYERS = iNumPlayers;
	NUM_ALL_PLAYERS = iAllPlayers;
	NUM_ALL_PLAYERS_B = iAllPlayers + 1;
	SETTLER_OFFSET = EARTH_X * EARTH_Y;
	MAX_NUM_TECHS = iNumTechs;
	NUM_BUILDINGS = iNumBuildings;
	//settlersMaps = new int**[NUM_MAJOR_PLAYERS];
	int i;
	/*for ( i=0; i<NUM_MAJOR_PLAYERS; i++ ){
		settlersMaps[i] = new int*[iMaxY];
		for ( j=0; j<iMaxY; j++ ){
			settlersMaps[i][j] = new int[iMaxX];
			for ( k=0; k<iMaxX; k++ ) settlersMaps[i][j][k] = 20;
		};
	};*/
	settlersMaps = new int[NUM_MAJOR_PLAYERS *EARTH_X* EARTH_Y ];
	for( i=0; i<NUM_MAJOR_PLAYERS *EARTH_X* EARTH_Y; i++ ) settlersMaps[i] = 20;
	warsMaps = new int[NUM_MAJOR_PLAYERS *EARTH_X* EARTH_Y ];
	for( i=0; i<NUM_MAJOR_PLAYERS *EARTH_X* EARTH_Y; i++ ) warsMaps[i] = 0;
	/*warsMaps = new int**[NUM_MAJOR_PLAYERS];
	for ( i=0; i<NUM_MAJOR_PLAYERS; i++ ){
		warsMaps[i] = new int*[iMaxY];
		for ( j=0; j<iMaxY; j++ ){
			warsMaps[i][j] = new int[iMaxX];
			for ( k=0; k<iMaxX; k++ ) warsMaps[i][j][k] = 0;
		};
	};*/
	CoreAreasRect = new int*[NUM_ALL_PLAYERS_B];
	CoreAreasMinusCount = new int[NUM_ALL_PLAYERS_B];
	CoreAreasMinus = new int*[NUM_ALL_PLAYERS_B];
	NormalAreasRect = new int*[NUM_ALL_PLAYERS_B];
	NormalAreasMinusCount = new int[NUM_ALL_PLAYERS_B];
	NormalAreasMinus = new int*[NUM_ALL_PLAYERS_B];
	//ProsecutionCount = new int[NUM_ALL_PLAYERS_B];
	for ( i=0; i<NUM_ALL_PLAYERS_B; i++ ){
		CoreAreasRect[i] = new int[4];
		NormalAreasRect[i] = new int[4];
		CoreAreasMinusCount[i] = 0;
		NormalAreasMinusCount[i] = 0;
		CoreAreasMinus[i] = NULL;
		NormalAreasMinus[i] = NULL;
		//ProsecutionCount[i] = 0;
	};
	startingTurn = new int[NUM_ALL_PLAYERS_B];					for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) startingTurn[i] = 0;
	growthThreshold = new int[NUM_ALL_PLAYERS_B];				for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) growthThreshold[i] = 100;
	productionModifierUnits = new int[NUM_ALL_PLAYERS_B];		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) productionModifierUnits[i] = 100;
	productionModifierBuildings = new int[NUM_ALL_PLAYERS_B];	for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) productionModifierBuildings[i] = 100;
	productionModifierWonders = new int[NUM_ALL_PLAYERS_B];		for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) productionModifierWonders[i] = 100;
	inflationModifier = new int[NUM_ALL_PLAYERS_B];				for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) inflationModifier[i] = 100;
	gpModifier = new int[NUM_ALL_PLAYERS_B];					for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) gpModifier[i] = 100;
	unitSupportModifier = new int[NUM_ALL_PLAYERS_B];			for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) unitSupportModifier[i] = 100;
	cityDistanceSupport = new int[NUM_ALL_PLAYERS_B];			for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) cityDistanceSupport[i] = 100;
	cityNumberSupport = new int[NUM_ALL_PLAYERS_B];				for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) cityNumberSupport[i] = 100;
	civicSupportModifier = new int[NUM_ALL_PLAYERS_B];			for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) civicSupportModifier[i] = 100;
	researchModifier = new int[NUM_ALL_PLAYERS_B];				for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) researchModifier[i] = 100;
	healthModifier = new int[NUM_ALL_PLAYERS_B];				for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) healthModifier[i] = 100;
	workerModifier = new int[NUM_ALL_PLAYERS_B];				for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) workerModifier[i] = 100;
	cultureModifier = new int[NUM_ALL_PLAYERS_B];				for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) cultureModifier[i] = 100;
	cityInitPop = new int[NUM_ALL_PLAYERS_B];					for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) cityInitPop[i] = 1;

	cityClusterTop = new int[NUM_ALL_PLAYERS_B];
	cityClusterBottom = new int[NUM_ALL_PLAYERS_B];
	cityClusterMinus = new int[NUM_ALL_PLAYERS_B];
	for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ){
		cityClusterTop[i] = 2;
		cityClusterBottom[i] = 3;
		cityClusterMinus[i] = 1;
	};

	cityWarDistance = new int[NUM_ALL_PLAYERS_B];				for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) cityWarDistance[i] = 1;
	techPreferences = new int* [NUM_ALL_PLAYERS_B];
	for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) techPreferences[i] = new int[MAX_NUM_TECHS];
	for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ )
		for ( int j=0; j<MAX_NUM_TECHS; j++ )
			techPreferences[i][j] = 100;

	diplomacyModifiers = new int* [NUM_ALL_PLAYERS_B];
	for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) diplomacyModifiers[i] = new int[NUM_ALL_PLAYERS_B];
	for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ )
		for ( int j=0; j<NUM_ALL_PLAYERS_B; j++ )
			diplomacyModifiers[i][j] = 0;

	/*UniquePowers = new int* [NUM_ALL_PLAYERS_B];
	for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) UniquePowers[i] = new int[UP_TOTAL_NUM];
	for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ )
		for ( int j=0; j<UP_TOTAL_NUM; j++ )
			UniquePowers[i][j] = -1;*/
	UniquePowers = new int[NUM_ALL_PLAYERS_B * UP_TOTAL_NUM];
	for ( int i=0; i<NUM_ALL_PLAYERS_B* UP_TOTAL_NUM; i++ ) UniquePowers[i] = -1;

	cityInitBuildings = new int* [NUM_ALL_PLAYERS_B];
	for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ ) cityInitBuildings[i] = new int[NUM_BUILDINGS];
	for ( int i=0; i<NUM_ALL_PLAYERS_B; i++ )
		for ( int j=0; j<NUM_BUILDINGS; j++ )
			cityInitBuildings[i][j] = 0;

	//GC.getGameINLINE().logMsg(" Num Religions is %d ",GC.getNumReligionInfos() );

	NUM_RELIGIONS = iNumReligions;

	civSpreadFactor = new int[ NUM_ALL_PLAYERS_B * NUM_RELIGIONS ];
	for ( int i=0; i< NUM_ALL_PLAYERS_B * NUM_RELIGIONS; i++ ) civSpreadFactor[i] = 100;

	colonyAIModifier = new int[ NUM_ALL_PLAYERS_B ];
	for ( int i=0; i< NUM_ALL_PLAYERS_B; i++ ) colonyAIModifier[i] = 100;

	FaithPowers = new int[ NUM_RELIGIONS * FP_TOTAL_NUM ];
	for ( int i=0; i< NUM_RELIGIONS * FP_TOTAL_NUM; i++ ) FaithPowers[i] = -1;

	startingWorkers = new int[ NUM_ALL_PLAYERS_B ];
	for ( int i=0; i< NUM_ALL_PLAYERS_B; i++ ) startingWorkers[i] = 0;

	turnPlayed = new int[NUM_ALL_PLAYERS_B];
	for ( int i=0; i< NUM_ALL_PLAYERS_B; i++ ) turnPlayed[i] = 0;

	StrategicTileX = new int[NUM_ALL_PLAYERS_B];
	StrategicTileY = new int[NUM_ALL_PLAYERS_B];
	for ( int i=0; i< NUM_ALL_PLAYERS_B; i++ ){ StrategicTileX[i] = -1; StrategicTileY[i] = -1; }

	buildingPrefs = new int[ NUM_ALL_PLAYERS_B * NUM_BUILDINGS ];
	for ( int i=0; i < NUM_ALL_PLAYERS_B * NUM_BUILDINGS; i++ ){ buildingPrefs[i] = 0; }
};

void CyGlobalContext::setGrowthModifiers( int iCiv, int iPop, int iCult, int iGP, int iWorker, int iHealth, int iInitPop ){
	growthThreshold[iCiv] = iPop;
	cultureModifier[iCiv] = iCult;
	gpModifier[iCiv] = iGP;
	workerModifier[iCiv] = iWorker;
	healthModifier[iCiv] = iHealth;
	cityInitPop[iCiv] = iInitPop;
};

void CyGlobalContext::setProductionModifiers( int iCiv, int iUnits, int iBuildings, int iWonders, int iResearch ){
	//if ( iCiv == 21 ){
	//	GC.getGameINLINE().logMsg(" input: %d %d %d %d %d",iCiv,iUnits,iBuildings,iWonders,iResearch );
	//	GC.getGameINLINE().logMsg(" iUnits %d %d %d",startingTurn[4],productionModifierUnits[4],productionModifierUnits[iCiv]);
	//	GC.getGameINLINE().logMsg(" iWonders %d %d %d",startingTurn[4],productionModifierUnits[4],productionModifierWonders[iCiv]);
	//};
	productionModifierUnits[iCiv] = iUnits;
	productionModifierBuildings[iCiv] = iBuildings;
	productionModifierWonders[iCiv] = iWonders;
	researchModifier[iCiv] = iResearch;
	//if ( iCiv == 21 ){
	//	GC.getGameINLINE().logMsg(" iUnits %d %d %d",startingTurn[4],productionModifierUnits[4],productionModifierUnits[iCiv]);
	//	GC.getGameINLINE().logMsg(" iWonders %d %d %d",startingTurn[4],productionModifierUnits[4],productionModifierWonders[iCiv]);
	//};
};

void CyGlobalContext::setSupportModifiers( int iCiv, int iInflation, int iUnits, int iCityDist, int iCityNum, int iCivic ){
	inflationModifier[iCiv] = iInflation;
	unitSupportModifier[iCiv] = iUnits;
	cityDistanceSupport[iCiv] = iCityDist;
	cityNumberSupport[iCiv] = iCityNum;
	civicSupportModifier[iCiv] = iCivic;
};

void CyGlobalContext::setInitialPopulation( int iCiv, int iInitPop ){
	cityInitPop[iCiv] = iInitPop;
};

void CyGlobalContext::setInitialBuilding( int iCiv, int iBuilding, bool w ){
	if ( w ){
		cityInitBuildings[iCiv][iBuilding] = 1;
	}else{
		cityInitBuildings[iCiv][iBuilding] = 0;
	};
};

void CyGlobalContext::setWarsMap( int iCiv, int y, int x, int iVal ){
	//warsMaps[iCiv][y][x] = iVal;
	warsMaps[ iCiv * SETTLER_OFFSET + EARTH_X *y + x ] = iVal;
};

void CyGlobalContext::setSettlersMap( int iCiv, int y, int x, int iVal ){
	//settlersMaps[iCiv][y][x] = iVal;
	settlersMaps[ iCiv * SETTLER_OFFSET + EARTH_X *y + x ] = iVal;
};

bool CyGlobalContext::isLargestCity( int x, int y ){
	return getCyGame() ->isLargestCity( x, y );
};

bool CyGlobalContext::isTopCultureCity( int x, int y ){
	return getCyGame() ->isTopCultureCity( x, y );
};

int CyGlobalContext::doesOwnCities( int iCiv, int BLx, int BLy, int TRx, int TRy ){
	return getCyGame() ->doesOwnCities( iCiv, BLx, BLy, TRx, TRy );
};

int CyGlobalContext::doesOwnOrVassalCities( int iCiv, int BLx, int BLy, int TRx, int TRy ){
	return getCyGame() ->doesOwnOrVassalCities( iCiv, BLx, BLy, TRx, TRy );
};

bool CyGlobalContext::doesHaveOtherReligion( int BLx, int BLy, int TRx, int TRy, int AllowR ){
	return getCyGame() ->doesHaveOtherReligion( BLx, BLy, TRx, TRy, AllowR );
};

int CyGlobalContext::countOwnedCities( int iCiv, int BLx, int BLy, int TRx, int TRy ){
	return getCyGame() ->countOwnedCities( iCiv, BLx, BLy, TRx, TRy );
};

int CyGlobalContext::countCitiesLostTo( int iCiv, int iNewOwner ){
	return getCyGame() ->countCitiesLostTo( iCiv, iNewOwner );
};

bool CyGlobalContext::safeMotherland( int iCiv ){
	return getCyGame() ->safeMotherland( iCiv );
};

bool CyGlobalContext::canSeeAllTerrain( int iCiv, int iTerrain ){
	return getCyGame() ->canSeeAllTerrain( iCiv, iTerrain );
};

bool CyGlobalContext::controlMostTeritory( int iCiv, int BLx, int BLy, int TRx, int TRy ){
	return getCyGame() ->controlMostTeritory( iCiv, BLx, BLy, TRx, TRy );
};

void CyGlobalContext::setCoreNormal( int iCiv, int iCBLx, int iCBLy, int iCTRx, int iCTRy, int iNBLx, int iNBLy, int iNTRx, int iNTRy, int iCCE, int iCNE ){
	CoreAreasRect[iCiv][0] = iCBLx; CoreAreasRect[iCiv][1] = iCBLy; CoreAreasRect[iCiv][2] = iCTRx; CoreAreasRect[iCiv][3] = iCTRy;
	NormalAreasRect[iCiv][0] = iNBLx; NormalAreasRect[iCiv][1] = iNBLy; NormalAreasRect[iCiv][2] = iNTRx; NormalAreasRect[iCiv][3] = iNTRy;
	CoreAreasMinusCount[iCiv] = 0;
	if ( iCCE > 0 ) CoreAreasMinus[iCiv] = new int[2*iCCE];
	NormalAreasMinusCount[iCiv] = 0;
	if ( iCNE > 0 ) NormalAreasMinus[iCiv] = new int[2*iCNE];
};

void CyGlobalContext::addCoreException( int iCiv, int x, int y ){
	CoreAreasMinus[iCiv][2*CoreAreasMinusCount[iCiv]] = x;
	CoreAreasMinus[iCiv][2*CoreAreasMinusCount[iCiv]+1] = y;
	CoreAreasMinusCount[iCiv]++;
};
	
void CyGlobalContext::addNormalException( int iCiv, int x, int y ){
	NormalAreasMinus[iCiv][2*NormalAreasMinusCount[iCiv]] = x;
	NormalAreasMinus[iCiv][2*NormalAreasMinusCount[iCiv]+1] = y;
	NormalAreasMinusCount[iCiv]++;
};

void CyGlobalContext::calcLastOwned(){
	getCyGame() ->calcLastOwned();
};

int CyGlobalContext::getlOwnedPlots( int iCiv ){
	return lOwnedPlots[iCiv];
};

int CyGlobalContext::getlOwnedCities( int iCiv ){
	return lOwnedCities[iCiv];
};

/*int CyGlobalContext::getProsecutionCount( int iCiv ){
	return ProsecutionCount[iCiv];
};*/

/*void CyGlobalContext::setProsecutionCount( int iCiv, int iCount ){
	ProsecutionCount[iCiv] = iCount;
};*/

void CyGlobalContext::setProsecutorReligions( int iProsecutor, int iProsecutorClass ){
	UNIT_PROSECUTOR = iProsecutor;
	UNIT_PROSECUTOR_CLASS = iProsecutorClass;
	//NUM_RELIGIONS = GC.getNumReligionInfos();
};

void CyGlobalContext::setSaintParameters( int iUnitID, int iBenefit, int iTreshhold1, int iTreshhold3 ){
	UNIT_SAINT = iUnitID;
	UNIT_SAINT_BENEFIT = iBenefit;
	UNIT_SAINT_1_TRESHHOLD = iTreshhold1;
	UNIT_SAINT_3_TRESHHOLD = iTreshhold3;
};

int CyGlobalContext::cityStabilityExpansion( int iPlayer, int iFCity ){
	return getCyGame() ->cityStabilityExpansion( iPlayer, iFCity );
};

int CyGlobalContext::cityStabilityPenalty( int iPlayer, int iAnger, int iHealth, int iReligion, int iLarge, int iHurry, int iNoMilitary, int iWarW, int iFReligion, int iFCulture, int iPerCityCap ){
	return getCyGame() ->cityStabilityPenalty( iPlayer, iAnger, iHealth, iReligion, iLarge, iHurry, iNoMilitary, iWarW, iFReligion, iFCulture, iPerCityCap );
};

void CyGlobalContext::damageFromBuilding( int iPlayer, int iBuilding, int iFoeDamage, int iBarbDamage ){
	return getCyGame() ->damageFromBuilding( iPlayer, iBuilding, iFoeDamage, iBarbDamage );
};

void CyGlobalContext::setIndependnets( int iIndyStart, int iIndyEnd, int iBarb ){
	INDEP_START = iIndyStart;
	INDEP_END = iIndyEnd;
	BARBARIAN = iBarb;
	AI_INDEP_HUNT = new bool[INDEP_END - INDEP_START + 1];
};

int CyGlobalContext::getStartingTurn( int iCiv ){
	return startingTurn[iCiv];
};

void CyGlobalContext::setPapalPlayer( int iCiv, int iReligion ){
	PAPAL_PLAYER = iCiv;
	PAPAL_RELIGION = iReligion;
};

int CyGlobalContext::getRelationTowards( int iWho, int iTowards ){
	return GET_PLAYER((PlayerTypes) iWho).AI_getAttitudeVal( (PlayerTypes) iTowards, true );
};

void CyGlobalContext::setGlobalWarming( bool bWhat ){
	USE_GLOBAL_WARMING = bWhat;
};

void CyGlobalContext::setReligionSpread( int iCiv, int iReligion, int iSpread ){
	civSpreadFactor[ iReligion * NUM_ALL_PLAYERS_B + iCiv ] = iSpread;
};

void CyGlobalContext::setColonyAIModifier( int iCiv, int iModifier ){
	colonyAIModifier[iCiv] = iModifier;
};

void CyGlobalContext::setReligionBenefit( int iReligion, int iBenefit, int iParameter ){
	FaithPowers[ iReligion * FP_TOTAL_NUM + iBenefit ] = iParameter;
};

void CyGlobalContext::setSchism( int iReligionA, int iReligionB, int iTurn ){
	SCHISM_A = iReligionA;
	SCHISM_B = iReligionB;
	SCHISM_YEAR = iTurn;
};

void CyGlobalContext::setHoliestCity( int iCityX, int iCityY ){
	HOLIEST_CITY_X = iCityX;
	HOLIEST_CITY_Y = iCityY;
};

void CyGlobalContext::setStartingWorkers( int iCiv, int iWorkers ){
	startingWorkers[iCiv] = iWorkers;
};

int CyGlobalContext::countCitiesOutside( int iCiv ){
	return GET_PLAYER( (PlayerTypes) iCiv ).countExternalCities();
};

void CyGlobalContext::setStrategicTile( int iCiv, int iX, int iY ){
	StrategicTileX[iCiv] = iX;
	StrategicTileY[iCiv] = iY;
};

void CyGlobalContext::setFastTerrain( int iFastTerrain ){
	FAST_TERRAIN = iFastTerrain;
};

void CyGlobalContext::setBuildingPref( int iCiv, int iBuilding, int iPref ){
	buildingPrefs[ iCiv * NUM_BUILDINGS + iBuilding ] = iPref;
};