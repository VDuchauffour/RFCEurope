//Rhye

#include "CvGameCoreDLL.h"
#include "CvRhyes.h"

// rhyes.cpp


int* startingTurn = NULL;
int *turnPlayed = NULL;
int *civSpreadFactor = NULL;

int techFoundedDate[120];

int *settlersMaps = NULL;
int *warsMaps = NULL;

int EARTH_X = 0;
int EARTH_Y = 0;
int NUM_MAJOR_PLAYERS = 0;
int NUM_ALL_PLAYERS = 0;
int NUM_ALL_PLAYERS_B = 0;
int SETTLER_OFFSET = 0;

int MAX_NUM_TECHS = 0;
int NUM_BUILDINGS = 0;

int PAPAL_PLAYER = -2;
int PAPAL_RELIGION = -2;


int SCHISM_A = -2; int SCHISM_B = -2;
int SCHISM_YEAR = -2;

int HOLIEST_CITY_X = -1;
int HOLIEST_CITY_Y = -1;

int *UniquePowers = NULL;
int *FaithPowers = NULL;

int *FaithPointsCap = NULL;

// 3Miro: export balance factors
// actual values are set in via Python
int* growthThresholdAI = NULL;
int* productionModifierUnitsAI = NULL;
int* productionModifierBuildingsAI = NULL;
int* productionModifierWondersAI = NULL;
int* inflationModifierAI = NULL;
int* gpModifierAI = NULL;
int* unitSupportModifierAI = NULL;
int* cityDistanceSupportAI = NULL;
int* cityNumberSupportAI = NULL;
int* civicSupportModifierAI = NULL;
int* researchModifierAI = NULL;
int* healthModifierAI = NULL;
int* workerModifierAI = NULL;
int* cultureModifierAI = NULL;
// 3Miro: Start the export of the balance factors (for Human)
int* growthThresholdHu = NULL;
int* productionModifierUnitsHu = NULL;
int* productionModifierBuildingsHu = NULL;
int* productionModifierWondersHu = NULL;
int* inflationModifierHu = NULL;
int* gpModifierHu = NULL;
int* unitSupportModifierHu = NULL;
int* cityDistanceSupportHu = NULL;
int* cityNumberSupportHu = NULL;
int* civicSupportModifierHu = NULL;
int* researchModifierHu = NULL;
int* healthModifierHu = NULL;
int* workerModifierHu = NULL;
int* cultureModifierHu = NULL;

int *cityInitPop = NULL;
int **cityInitBuildings = NULL;
int *startingWorkers = NULL;


int* cityClusterTop = NULL;
int* cityClusterBottom = NULL;
int* cityClusterMinus = NULL;
int** diplomacyModifiers = NULL;
int *buildingPrefs = NULL;

int* cityWarDistance = NULL;
int** techPreferences = NULL;

// Absinthe: unused in RFCE
//int* lOwnedCities = NULL;
//int* lOwnedPlots = NULL;

// Absinthe: in python now
int* ProsecutionCount = NULL;


int** CoreAreasRect = NULL;
int* CoreAreasMinusCount = NULL;
int** CoreAreasMinus = NULL;
int** NormalAreasRect = NULL;
int* NormalAreasMinusCount = NULL;
int** NormalAreasMinus = NULL;

int UNIT_PROSECUTOR = -2;
int UNIT_PROSECUTOR_CLASS = -1;
int NUM_RELIGIONS = 5;

int UNIT_SAINT = -2;
int UNIT_SAINT_BENEFIT = -2;
int UNIT_SAINT_1_TRESHHOLD = 0;
int UNIT_SAINT_3_TRESHHOLD = 0;

int INDEP_START = -1;
int INDEP_END = -1;
int BARBARIAN = -1;
bool *AI_INDEP_HUNT = NULL;

bool USE_GLOBAL_WARMING = true;
int FAST_TERRAIN = -1;

int *StrategicTileX = NULL;
int *StrategicTileY = NULL;

int * colonyAIModifier = NULL;

// 3Miro: Psycho AI cheat
int psychoAI_x = -2;
int psychoAI_y = -2;
int psychoAI_player = -2;

// 3Miro: historical enemy AI cheat
int *historicalEnemyAIcheat = NULL;

// this is a more elegant solution to the bug in the culture of CvPlot (although it is still a hack)
// once a turn we will check if we are within 3 turns of someone's spawn, if so, then set withinSpawnDate = true
// and then only check that in CvPlot. We will set withinSpawnDate in CvGame.cpp
bool withinSpawnDate = false;

// 3Miro: Autorun hack
int iAutorunUnit;
int iAutorunX;
int iAutorunY;

// 3Miro: Commerse from Building + Civic
int iCivicBuildingCommerse1 = -1;
int iCivicBuildingCommerse2 = -1;
int iCivicBuildingCommerse3 = -1;

// 3MiroTimeline: set the timeline for technologies
int *timelineTechDates;
int timelineTechPenaltyTop = 0;
int timelineTechPenaltyBottom = 1;
int timelineTechPenaltyCap = 0;
int timelineTechBuffTop = 0;
int timelineTechBuffBottom = 1;
int timelineTechBuffCap = 0;

int *provinceMap = NULL;
int *provinceSizeList = NULL;
int **provinceTileList = NULL;
//int provinceToColor = -1; // Absinthe: moved to python
int numRegions = 1; // for map areas, give the number of regions
int *provinceRegionMap = NULL; // give the region for each province (province -1 is default reigion 0)

int iNumProvinceTypes; // how many type of provinces are there
int *iSettlerValuesPerProvinceType = NULL; // how do settlers value tiles from the specific province (AI purposes)
int *iWarValuesPerProvinceType = NULL; // how do you consider attacking a specific province (AI purposes)
int *iModCultureTop = NULL; // how do you modify culture for the specific province
int *iModCultureBottom = NULL; // Culture * Top / Bottom
int *iCultureImmune = NULL; // locks a province so that only the player in exception can put culture in it
int *iCultureImmuneException = NULL; // the only player that can put culture on the tiles of this province

// Additional Plotting Tools:
int iPlotCore = -1; // plot the core area of this player
int iPlotNormal = -1; // plot the normal area of this player
// Absinthe: plotting updates:
//int iPlotSettlers = -1; // which player to plot for the settlers map
//int iPlotWars = -1; // which player to plot for the wars map
int iCoreToPlot = 0; // set in RFCEBalance.py if you want to use
int iNormalToPlot = 0; // set in RFCEBalance.py if you want to use
//int iWhatToPlot = 0; // 0 plots Core, 1 plots Normal, 2 plots Settlers and 3 plots Wars

int *conditionalVassalage = NULL;
int provinceFlagToVassalize;

int iParentReligion;
int iSchismReligion;

int iMercPromotion = -1;

int iPeaceTurnsAfterSpawn = 0;

int minorReligion = -1;
int minorReligionRefugies = 0;

bool MiroBelongToCore( int iCiv, int x, int y ){
	// Wrong name, Minus is actually added to the core area
	if ( ( x>= CoreAreasRect[iCiv][0] ) && ( y >= CoreAreasRect[iCiv][1] ) && ( x<= CoreAreasRect[iCiv][2] ) && ( y<= CoreAreasRect[iCiv][3] ) ){
		return true;
	}else{
		for ( int i=0; i<CoreAreasMinusCount[iCiv]; i++ ){
			if ( (CoreAreasMinus[iCiv][2*i] == x)&&(CoreAreasMinus[iCiv][2*i+1] == y) ) return true;
		};
	};
	return false;
};
bool MiroBelongToNormal( int iCiv, int x, int y ){
	if ( ( x>= NormalAreasRect[iCiv][0] ) && ( y >= NormalAreasRect[iCiv][1] ) && ( x<= NormalAreasRect[iCiv][2] ) && ( y<= NormalAreasRect[iCiv][3] ) ){
		for ( int i=0; i<NormalAreasMinusCount[iCiv]; i++ ){
			if ( (NormalAreasMinus[iCiv][2*i] == x)&&(NormalAreasMinus[iCiv][2*i+1] == y) ) return false;
		};
		return true;
	};
	return false;
};

int getSettlersMaps( int iCiv, int y, int x, char * w ){
	if ( settlersMaps == NULL || iCiv >= NUM_MAJOR_PLAYERS ){ //fixed value for the Pope and the Independents
		return 20;
	}else{
		if ( (x>=0)&&(x<EARTH_X)&&(y>=0)&&(y<EARTH_Y) ){
			//return settlersMaps[iCiv][y][x];
			return settlersMaps[ iCiv * SETTLER_OFFSET + y * EARTH_X + x ];
		}else{
			if ( w != NULL ){
				GC.getGameINLINE().logMsg(w);
			};
			return 20;
		};
	};
};

// Absinthe: moved to CvPlayer, exported to python
int getWarsMaps( int iCiv, int y, int x, char *w ){
	if ( warsMaps == NULL || iCiv >= NUM_MAJOR_PLAYERS ){ //fixed value for the Pope and the Independents
		return 0;
	}else{
		if ( (x>=0)&&(x<EARTH_X)&&(y>=0)&&(y<EARTH_Y) ){
			//return warsMaps[iCiv][y][x];
			return warsMaps[ iCiv * SETTLER_OFFSET + y * EARTH_X + x ];
		}else{
			if ( w != NULL ){
				GC.getGameINLINE().logMsg(w);
			};
			return 0;
		};
	};
};

bool isIndep( int iCiv ){
	if ( ( iCiv >= INDEP_START) && ( iCiv <= INDEP_END ) ) return true;
	return false;
};

int getModifiedTechCostForTurn( int iTech, int iTurn ){
	int iCost = GC.getTechInfo((TechTypes)iTech).getResearchCost();
	// 3MiroTimeline: adjust the tech cost according to the turn it should get discovered
	int iAhistoric = iTurn - timelineTechDates[iTech];
	if ( iAhistoric < 0 ){ // too fast
		iAhistoric = std::max( iAhistoric, timelineTechPenaltyCap );
		iCost *= 100 + timelineTechPenaltyTop * iAhistoric * iAhistoric / timelineTechPenaltyBottom;
	}else{ // too slow
		iAhistoric = std::min( iAhistoric, timelineTechBuffCap );
		iCost *= 100 - timelineTechBuffTop * iAhistoric * iAhistoric / timelineTechBuffBottom;
	};
	return iCost / 100;
};