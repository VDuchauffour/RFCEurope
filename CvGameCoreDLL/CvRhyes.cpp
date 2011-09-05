//Rhye

#include "CvGameCoreDLL.h"
#include "CvRhyes.h"

// rhyes.cpp


int* startingTurn = NULL;
int *turnPlayed = NULL;
int *civSpreadFactor = NULL;

// (dynamic civ names - not jdog's)
/*wchar civDynamicNames[22][22][19]  = {
//				//people		monarchy				monarchy ext		monarchy mod		monarchy ext mod		republic			communism			fascism				islam monarchy		islam republic			vas. Byzantium			vas. Frankia		  vas. Arabia/Cordoba		vas. Spain			vas. Norse/Sweden		vas. Venice			vas. Moscow/Kiev		vas. Germany			vas. England		vas. Austria		vas. Turkey				Vassal generic					
//Burgundy
	{	 L"TXT_KEY_DN_BUR00", L"TXT_KEY_DN_BUR01", L"TXT_KEY_DN_BUR02", L"TXT_KEY_DN_BUR03",  L"TXT_KEY_DN_BUR04",  L"TXT_KEY_DN_BUR05",  L"TXT_KEY_DN_BUR06",  L"TXT_KEY_DN_BUR07",  L"TXT_KEY_DN_BUR08",  L"TXT_KEY_DN_BUR09",  L"TXT_KEY_DN_BUR10",  L"TXT_KEY_DN_BUR11",  L"TXT_KEY_DN_BUR12",  L"TXT_KEY_DN_BUR13",  L"TXT_KEY_DN_BUR14",  L"TXT_KEY_DN_BUR15",  L"TXT_KEY_DN_BUR16",  L"TXT_KEY_DN_BUR17",  L"TXT_KEY_DN_BUR18",  L"TXT_KEY_DN_BUR19",  L"TXT_KEY_DN_BUR20",  L"TXT_KEY_DN_BUR21" },
//Byzantium
	{	 L"TXT_KEY_DN_BYZ00", L"TXT_KEY_DN_BYZ01", L"TXT_KEY_DN_BYZ02", L"TXT_KEY_DN_BYZ03",  L"TXT_KEY_DN_BYZ04",  L"TXT_KEY_DN_BYZ05",  L"TXT_KEY_DN_BYZ06",  L"TXT_KEY_DN_BYZ07",  L"TXT_KEY_DN_BYZ08",  L"TXT_KEY_DN_BYZ09",  L"TXT_KEY_DN_BYZ10",  L"TXT_KEY_DN_BYZ11",  L"TXT_KEY_DN_BYZ12",  L"TXT_KEY_DN_BYZ13",  L"TXT_KEY_DN_BYZ14",  L"TXT_KEY_DN_BYZ15",  L"TXT_KEY_DN_BYZ16",  L"TXT_KEY_DN_BYZ17",  L"TXT_KEY_DN_BYZ18",  L"TXT_KEY_DN_BYZ19",  L"TXT_KEY_DN_BYZ20",  L"TXT_KEY_DN_BYZ21" },
//Frankia
	{	 L"TXT_KEY_DN_FRA00", L"TXT_KEY_DN_FRA01", L"TXT_KEY_DN_FRA02", L"TXT_KEY_DN_FRA03",  L"TXT_KEY_DN_FRA04",  L"TXT_KEY_DN_FRA05",  L"TXT_KEY_DN_FRA06",  L"TXT_KEY_DN_FRA07",  L"TXT_KEY_DN_FRA08",  L"TXT_KEY_DN_FRA09",  L"TXT_KEY_DN_FRA10",  L"TXT_KEY_DN_FRA11",  L"TXT_KEY_DN_FRA12",  L"TXT_KEY_DN_FRA13",  L"TXT_KEY_DN_FRA14",  L"TXT_KEY_DN_FRA15",  L"TXT_KEY_DN_FRA16",  L"TXT_KEY_DN_FRA17",  L"TXT_KEY_DN_FRA18",  L"TXT_KEY_DN_FRA19",  L"TXT_KEY_DN_FRA20",  L"TXT_KEY_DN_FRA21" },
//Arabia
	{	 L"TXT_KEY_DN_ARA00", L"TXT_KEY_DN_ARA01", L"TXT_KEY_DN_ARA02", L"TXT_KEY_DN_ARA03",  L"TXT_KEY_DN_ARA04",  L"TXT_KEY_DN_ARA05",  L"TXT_KEY_DN_ARA06",  L"TXT_KEY_DN_ARA07",  L"TXT_KEY_DN_ARA08",  L"TXT_KEY_DN_ARA09",  L"TXT_KEY_DN_ARA10",  L"TXT_KEY_DN_ARA11",  L"TXT_KEY_DN_ARA12",  L"TXT_KEY_DN_ARA13",  L"TXT_KEY_DN_ARA14",  L"TXT_KEY_DN_ARA15",  L"TXT_KEY_DN_ARA16",  L"TXT_KEY_DN_ARA17",  L"TXT_KEY_DN_ARA18",  L"TXT_KEY_DN_ARA19",  L"TXT_KEY_DN_ARA20",  L"TXT_KEY_DN_ARA21" },
//Bulgaria
	{	 L"TXT_KEY_DN_BUL00", L"TXT_KEY_DN_BUL01", L"TXT_KEY_DN_BUL02", L"TXT_KEY_DN_BUL03",  L"TXT_KEY_DN_BUL04",  L"TXT_KEY_DN_BUL05",  L"TXT_KEY_DN_BUL06",  L"TXT_KEY_DN_BUL07",  L"TXT_KEY_DN_BUL08",  L"TXT_KEY_DN_BUL09",  L"TXT_KEY_DN_BUL10",  L"TXT_KEY_DN_BUL11",  L"TXT_KEY_DN_BUL12",  L"TXT_KEY_DN_BUL13",  L"TXT_KEY_DN_BUL14",  L"TXT_KEY_DN_BUL15",  L"TXT_KEY_DN_BUL16",  L"TXT_KEY_DN_BUL17",  L"TXT_KEY_DN_BUL18",  L"TXT_KEY_DN_BUL19",  L"TXT_KEY_DN_BUL20",  L"TXT_KEY_DN_BUL21" },
//Cordoba
	{	 L"TXT_KEY_DN_COR00", L"TXT_KEY_DN_COR01", L"TXT_KEY_DN_COR02", L"TXT_KEY_DN_COR03",  L"TXT_KEY_DN_COR04",  L"TXT_KEY_DN_COR05",  L"TXT_KEY_DN_COR06",  L"TXT_KEY_DN_COR07",  L"TXT_KEY_DN_COR08",  L"TXT_KEY_DN_COR09",  L"TXT_KEY_DN_COR10",  L"TXT_KEY_DN_COR11",  L"TXT_KEY_DN_COR12",  L"TXT_KEY_DN_COR13",  L"TXT_KEY_DN_COR14",  L"TXT_KEY_DN_COR15",  L"TXT_KEY_DN_COR16",  L"TXT_KEY_DN_COR17",  L"TXT_KEY_DN_COR18",  L"TXT_KEY_DN_COR19",  L"TXT_KEY_DN_COR20",  L"TXT_KEY_DN_COR21" },
//Spain
	{	 L"TXT_KEY_DN_SPN00", L"TXT_KEY_DN_SPN01", L"TXT_KEY_DN_SPN02", L"TXT_KEY_DN_SPN03",  L"TXT_KEY_DN_SPN04",  L"TXT_KEY_DN_SPN05",  L"TXT_KEY_DN_SPN06",  L"TXT_KEY_DN_SPN07",  L"TXT_KEY_DN_SPN08",  L"TXT_KEY_DN_SPN09",  L"TXT_KEY_DN_SPN10",  L"TXT_KEY_DN_SPN11",  L"TXT_KEY_DN_SPN12",  L"TXT_KEY_DN_SPN13",  L"TXT_KEY_DN_SPN14",  L"TXT_KEY_DN_SPN15",  L"TXT_KEY_DN_SPN16",  L"TXT_KEY_DN_SPN17",  L"TXT_KEY_DN_SPN18",  L"TXT_KEY_DN_SPN19",  L"TXT_KEY_DN_SPN20",  L"TXT_KEY_DN_SPN21" },
//Norse
	{	 L"TXT_KEY_DN_NOR00", L"TXT_KEY_DN_NOR01", L"TXT_KEY_DN_NOR02", L"TXT_KEY_DN_NOR03",  L"TXT_KEY_DN_NOR04",  L"TXT_KEY_DN_NOR05",  L"TXT_KEY_DN_NOR06",  L"TXT_KEY_DN_NOR07",  L"TXT_KEY_DN_NOR08",  L"TXT_KEY_DN_NOR09",  L"TXT_KEY_DN_NOR10",  L"TXT_KEY_DN_NOR11",  L"TXT_KEY_DN_NOR12",  L"TXT_KEY_DN_NOR13",  L"TXT_KEY_DN_NOR14",  L"TXT_KEY_DN_NOR15",  L"TXT_KEY_DN_NOR16",  L"TXT_KEY_DN_NOR17",  L"TXT_KEY_DN_NOR18",  L"TXT_KEY_DN_NOR19",  L"TXT_KEY_DN_NOR20",  L"TXT_KEY_DN_NOR21" },
//Venecia
	{	 L"TXT_KEY_DN_VEN00", L"TXT_KEY_DN_VEN01", L"TXT_KEY_DN_VEN02", L"TXT_KEY_DN_VEN03",  L"TXT_KEY_DN_VEN04",  L"TXT_KEY_DN_VEN05",  L"TXT_KEY_DN_VEN06",  L"TXT_KEY_DN_VEN07",  L"TXT_KEY_DN_VEN08",  L"TXT_KEY_DN_VEN09",  L"TXT_KEY_DN_VEN10",  L"TXT_KEY_DN_VEN11",  L"TXT_KEY_DN_VEN12",  L"TXT_KEY_DN_VEN13",  L"TXT_KEY_DN_VEN14",  L"TXT_KEY_DN_VEN15",  L"TXT_KEY_DN_VEN16",  L"TXT_KEY_DN_VEN17",  L"TXT_KEY_DN_VEN18",  L"TXT_KEY_DN_VEN19",  L"TXT_KEY_DN_VEN20",  L"TXT_KEY_DN_VEN21" },
//Kiev
	{	 L"TXT_KEY_DN_KIE00", L"TXT_KEY_DN_KIE01", L"TXT_KEY_DN_KIE02", L"TXT_KEY_DN_KIE03",  L"TXT_KEY_DN_KIE04",  L"TXT_KEY_DN_KIE05",  L"TXT_KEY_DN_KIE06",  L"TXT_KEY_DN_KIE07",  L"TXT_KEY_DN_KIE08",  L"TXT_KEY_DN_KIE09",  L"TXT_KEY_DN_KIE10",  L"TXT_KEY_DN_KIE11",  L"TXT_KEY_DN_KIE12",  L"TXT_KEY_DN_KIE13",  L"TXT_KEY_DN_KIE14",  L"TXT_KEY_DN_KIE15",  L"TXT_KEY_DN_KIE16",  L"TXT_KEY_DN_KIE17",  L"TXT_KEY_DN_KIE18",  L"TXT_KEY_DN_KIE19",  L"TXT_KEY_DN_KIE20",  L"TXT_KEY_DN_KIE21" },
//Hungary
	{	 L"TXT_KEY_DN_HUN00", L"TXT_KEY_DN_HUN01", L"TXT_KEY_DN_HUN02", L"TXT_KEY_DN_HUN03",  L"TXT_KEY_DN_HUN04",  L"TXT_KEY_DN_HUN05",  L"TXT_KEY_DN_HUN06",  L"TXT_KEY_DN_HUN07",  L"TXT_KEY_DN_HUN08",  L"TXT_KEY_DN_HUN09",  L"TXT_KEY_DN_HUN10",  L"TXT_KEY_DN_HUN11",  L"TXT_KEY_DN_HUN12",  L"TXT_KEY_DN_HUN13",  L"TXT_KEY_DN_HUN14",  L"TXT_KEY_DN_HUN15",  L"TXT_KEY_DN_HUN16",  L"TXT_KEY_DN_HUN17",  L"TXT_KEY_DN_HUN18",  L"TXT_KEY_DN_HUN19",  L"TXT_KEY_DN_HUN20",  L"TXT_KEY_DN_HUN21" },
//Germany
	{	 L"TXT_KEY_DN_GER00", L"TXT_KEY_DN_GER01", L"TXT_KEY_DN_GER02", L"TXT_KEY_DN_GER03",  L"TXT_KEY_DN_GER04",  L"TXT_KEY_DN_GER05",  L"TXT_KEY_DN_GER06",  L"TXT_KEY_DN_GER07",  L"TXT_KEY_DN_GER08",  L"TXT_KEY_DN_GER09",  L"TXT_KEY_DN_GER10",  L"TXT_KEY_DN_GER11",  L"TXT_KEY_DN_GER12",  L"TXT_KEY_DN_GER13",  L"TXT_KEY_DN_GER14",  L"TXT_KEY_DN_GER15",  L"TXT_KEY_DN_GER16",  L"TXT_KEY_DN_GER17",  L"TXT_KEY_DN_GER18",  L"TXT_KEY_DN_GER19",  L"TXT_KEY_DN_GER20",  L"TXT_KEY_DN_GER21" },
//Poland
	{	 L"TXT_KEY_DN_POL00", L"TXT_KEY_DN_POL01", L"TXT_KEY_DN_POL02", L"TXT_KEY_DN_POL03",  L"TXT_KEY_DN_POL04",  L"TXT_KEY_DN_POL05",  L"TXT_KEY_DN_POL06",  L"TXT_KEY_DN_POL07",  L"TXT_KEY_DN_POL08",  L"TXT_KEY_DN_POL09",  L"TXT_KEY_DN_POL10",  L"TXT_KEY_DN_POL11",  L"TXT_KEY_DN_POL12",  L"TXT_KEY_DN_POL13",  L"TXT_KEY_DN_POL14",  L"TXT_KEY_DN_POL15",  L"TXT_KEY_DN_POL16",  L"TXT_KEY_DN_POL17",  L"TXT_KEY_DN_POL18",  L"TXT_KEY_DN_POL19",  L"TXT_KEY_DN_POL20",  L"TXT_KEY_DN_POL21" },
//Moscow
	{	 L"TXT_KEY_DN_MOS00", L"TXT_KEY_DN_MOS01", L"TXT_KEY_DN_MOS02", L"TXT_KEY_DN_MOS03",  L"TXT_KEY_DN_MOS04",  L"TXT_KEY_DN_MOS05",  L"TXT_KEY_DN_MOS06",  L"TXT_KEY_DN_MOS07",  L"TXT_KEY_DN_MOS08",  L"TXT_KEY_DN_MOS09",  L"TXT_KEY_DN_MOS10",  L"TXT_KEY_DN_MOS11",  L"TXT_KEY_DN_MOS12",  L"TXT_KEY_DN_MOS13",  L"TXT_KEY_DN_MOS14",  L"TXT_KEY_DN_MOS15",  L"TXT_KEY_DN_MOS16",  L"TXT_KEY_DN_MOS17",  L"TXT_KEY_DN_MOS18",  L"TXT_KEY_DN_MOS19",  L"TXT_KEY_DN_MOS20",  L"TXT_KEY_DN_MOS21" },
//Genoa
	{	 L"TXT_KEY_DN_GEN00", L"TXT_KEY_DN_GEN01", L"TXT_KEY_DN_GEN02", L"TXT_KEY_DN_GEN03",  L"TXT_KEY_DN_GEN04",  L"TXT_KEY_DN_GEN05",  L"TXT_KEY_DN_GEN06",  L"TXT_KEY_DN_GEN07",  L"TXT_KEY_DN_GEN08",  L"TXT_KEY_DN_GEN09",  L"TXT_KEY_DN_GEN10",  L"TXT_KEY_DN_GEN11",  L"TXT_KEY_DN_GEN12",  L"TXT_KEY_DN_GEN13",  L"TXT_KEY_DN_GEN14",  L"TXT_KEY_DN_GEN15",  L"TXT_KEY_DN_GEN16",  L"TXT_KEY_DN_GEN17",  L"TXT_KEY_DN_GEN18",  L"TXT_KEY_DN_GEN19",  L"TXT_KEY_DN_GEN20",  L"TXT_KEY_DN_GEN21" },
//England
	{	 L"TXT_KEY_DN_ENG00", L"TXT_KEY_DN_ENG01", L"TXT_KEY_DN_ENG02", L"TXT_KEY_DN_ENG03",  L"TXT_KEY_DN_ENG04",  L"TXT_KEY_DN_ENG05",  L"TXT_KEY_DN_ENG06",  L"TXT_KEY_DN_ENG07",  L"TXT_KEY_DN_ENG08",  L"TXT_KEY_DN_ENG09",  L"TXT_KEY_DN_ENG10",  L"TXT_KEY_DN_ENG11",  L"TXT_KEY_DN_ENG12",  L"TXT_KEY_DN_ENG13",  L"TXT_KEY_DN_ENG14",  L"TXT_KEY_DN_ENG15",  L"TXT_KEY_DN_ENG16",  L"TXT_KEY_DN_ENG17",  L"TXT_KEY_DN_ENG18",  L"TXT_KEY_DN_ENG19",  L"TXT_KEY_DN_ENG20",  L"TXT_KEY_DN_ENG21" },
//Prtugal
	{	 L"TXT_KEY_DN_POR00", L"TXT_KEY_DN_POR01", L"TXT_KEY_DN_POR02", L"TXT_KEY_DN_POR03",  L"TXT_KEY_DN_POR04",  L"TXT_KEY_DN_POR05",  L"TXT_KEY_DN_POR06",  L"TXT_KEY_DN_POR07",  L"TXT_KEY_DN_POR08",  L"TXT_KEY_DN_POR09",  L"TXT_KEY_DN_POR10",  L"TXT_KEY_DN_POR11",  L"TXT_KEY_DN_POR12",  L"TXT_KEY_DN_POR13",  L"TXT_KEY_DN_POR14",  L"TXT_KEY_DN_POR15",  L"TXT_KEY_DN_POR16",  L"TXT_KEY_DN_POR17",  L"TXT_KEY_DN_POR18",  L"TXT_KEY_DN_POR19",  L"TXT_KEY_DN_POR20",  L"TXT_KEY_DN_POR21" },
//Austria
	{	 L"TXT_KEY_DN_AUS00", L"TXT_KEY_DN_AUS01", L"TXT_KEY_DN_AUS02", L"TXT_KEY_DN_AUS03",  L"TXT_KEY_DN_AUS04",  L"TXT_KEY_DN_AUS05",  L"TXT_KEY_DN_AUS06",  L"TXT_KEY_DN_AUS07",  L"TXT_KEY_DN_AUS08",  L"TXT_KEY_DN_AUS09",  L"TXT_KEY_DN_AUS10",  L"TXT_KEY_DN_AUS11",  L"TXT_KEY_DN_AUS12",  L"TXT_KEY_DN_AUS13",  L"TXT_KEY_DN_AUS14",  L"TXT_KEY_DN_AUS15",  L"TXT_KEY_DN_AUS16",  L"TXT_KEY_DN_AUS17",  L"TXT_KEY_DN_AUS18",  L"TXT_KEY_DN_AUS19",  L"TXT_KEY_DN_AUS20",  L"TXT_KEY_DN_AUS21" },
//Turkey
	{	 L"TXT_KEY_DN_TUR00", L"TXT_KEY_DN_TUR01", L"TXT_KEY_DN_TUR02", L"TXT_KEY_DN_TUR03",  L"TXT_KEY_DN_TUR04",  L"TXT_KEY_DN_TUR05",  L"TXT_KEY_DN_TUR06",  L"TXT_KEY_DN_TUR07",  L"TXT_KEY_DN_TUR08",  L"TXT_KEY_DN_TUR09",  L"TXT_KEY_DN_TUR10",  L"TXT_KEY_DN_TUR11",  L"TXT_KEY_DN_TUR12",  L"TXT_KEY_DN_TUR13",  L"TXT_KEY_DN_TUR14",  L"TXT_KEY_DN_TUR15",  L"TXT_KEY_DN_TUR16",  L"TXT_KEY_DN_TUR17",  L"TXT_KEY_DN_TUR18",  L"TXT_KEY_DN_TUR19",  L"TXT_KEY_DN_TUR20",  L"TXT_KEY_DN_TUR21" },
//Sweden
	{	 L"TXT_KEY_DN_SWE00", L"TXT_KEY_DN_SWE01", L"TXT_KEY_DN_SWE02", L"TXT_KEY_DN_SWE03",  L"TXT_KEY_DN_SWE04",  L"TXT_KEY_DN_SWE05",  L"TXT_KEY_DN_SWE06",  L"TXT_KEY_DN_SWE07",  L"TXT_KEY_DN_SWE08",  L"TXT_KEY_DN_SWE09",  L"TXT_KEY_DN_SWE10",  L"TXT_KEY_DN_SWE11",  L"TXT_KEY_DN_SWE12",  L"TXT_KEY_DN_SWE13",  L"TXT_KEY_DN_SWE14",  L"TXT_KEY_DN_SWE15",  L"TXT_KEY_DN_SWE16",  L"TXT_KEY_DN_SWE17",  L"TXT_KEY_DN_SWE18",  L"TXT_KEY_DN_SWE19",  L"TXT_KEY_DN_SWE20",  L"TXT_KEY_DN_SWE21" },
//Dutc
	{	 L"TXT_KEY_DN_DUT00", L"TXT_KEY_DN_DUT01", L"TXT_KEY_DN_DUT02", L"TXT_KEY_DN_DUT03",  L"TXT_KEY_DN_DUT04",  L"TXT_KEY_DN_DUT05",  L"TXT_KEY_DN_DUT06",  L"TXT_KEY_DN_DUT07",  L"TXT_KEY_DN_DUT08",  L"TXT_KEY_DN_DUT09",  L"TXT_KEY_DN_DUT10",  L"TXT_KEY_DN_DUT11",  L"TXT_KEY_DN_DUT12",  L"TXT_KEY_DN_DUT13",  L"TXT_KEY_DN_DUT14",  L"TXT_KEY_DN_DUT15",  L"TXT_KEY_DN_DUT16",  L"TXT_KEY_DN_DUT17",  L"TXT_KEY_DN_DUT18",  L"TXT_KEY_DN_DUT19",  L"TXT_KEY_DN_DUT20",  L"TXT_KEY_DN_DUT21" },
//Pope
	{	 L"TXT_KEY_DN_POP00", L"TXT_KEY_DN_POP01", L"TXT_KEY_DN_POP02", L"TXT_KEY_DN_POP03",  L"TXT_KEY_DN_POP04",  L"TXT_KEY_DN_POP05",  L"TXT_KEY_DN_POP06",  L"TXT_KEY_DN_POP07",  L"TXT_KEY_DN_POP08",  L"TXT_KEY_DN_POP09",  L"TXT_KEY_DN_POP10",  L"TXT_KEY_DN_POP11",  L"TXT_KEY_DN_POP12",  L"TXT_KEY_DN_POP13",  L"TXT_KEY_DN_POP14",  L"TXT_KEY_DN_POP15",  L"TXT_KEY_DN_POP16",  L"TXT_KEY_DN_POP17",  L"TXT_KEY_DN_POP18",  L"TXT_KEY_DN_POP19",  L"TXT_KEY_DN_POP20",  L"TXT_KEY_DN_POP21" }
};
int civDynamicNamesFlag[22] = 	{	 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 };
//									BUR BYZ	FRA ARA BUL COR SPN NOR VEN KIE HUN GER POL MOS GEN ENG POR AUS TUR SWE DUT POP
// 1 = REL, 0 = GOV

int civDynamicNamesEraThreshold[22] = { 2,  3,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 2 };*/

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


int* lOwnedCities = NULL;
int* lOwnedPlots = NULL;


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

int psychoAI_x = -2; 
int psychoAI_y = -2;
int psychoAI_player = -2;

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
int provinceToColor = -1;
int numRegions = 1; // for map areas, give the number of regions
int *provinceRegionMap = NULL; // give the region for each province (province -1 is default reigion 0)

int iNumProvinceTypes; // how many type of provinces are there
int *iSettlerValuesPerProvinceType = NULL; // how do settlers value tiles from the specific province (AI purposes)
int *iWarValuesPerProvinceType = NULL; // how do you consider attacking a specific province (AI purposes)
int *iModCultureTop = NULL; // how do you modify culture for the specific province
int *iModCultureBottom = NULL; // Culture * Top / Bottom
int *iCultureImmune = NULL; // locks a province so that only the player in exception can put culture in it
int *iCultureImmuneException = NULL; // the only player that can put culture on the tiles of this province

int *conditionalVassalage = NULL;
int provinceFlagToVassalize;

int iParentReligion;
int iSchismReligion;

int iMercPromotion = -1;

bool MiroBelongToCore( int iCiv, int x, int y ){
	/*if ( ( x>= CoreAreasRect[iCiv][0] ) && ( y >= CoreAreasRect[iCiv][1] ) && ( x<= CoreAreasRect[iCiv][2] ) && ( y<= CoreAreasRect[iCiv][3] ) ){
		for ( int i=0; i<CoreAreasMinusCount[iCiv]; i++ ){
			if ( (CoreAreasMinus[iCiv][2*i] == x)&&(CoreAreasMinus[iCiv][2*i+1] == y) ) return false;
		};
		return true;
	};
	return false;*/
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

//int getSettlersMaps( int iCiv, int y, int x ){
int getSettlersMaps( int iCiv, int y, int x, char * w ){
	if ( settlersMaps == NULL || iCiv >= NUM_MAJOR_PLAYERS ){
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

bool isIndep( int iCiv ){
	if ( ( iCiv >= INDEP_START) && ( iCiv <= INDEP_END ) ) return true;
	return false;
};
