# coding: utf-8


# Techs: initialize tech variables to unit indices from XML

iNumTechs = 75
# Early
(
    iCalendar,
    iArchitecture,
    iBronzeCasting,
    iTheology,
    iManorialism,
    iStirrup,  # teir 1
    iEngineering,
    iChainMail,
    iArt,
    iMonasticism,
    iVassalage,  # teir 2
    iAstrolabe,
    iMachinery,
    iVaultedArches,
    iMusic,
    iHerbalMedicine,
    iFeudalism,
    iFarriers,  # tier 3
    # High
    iMapMaking,
    iBlastFurnace,
    iSiegeEngines,
    iGothicArchitecture,
    iLiterature,
    iCodeOfLaws,
    iAristocracy,  # teir 4
    iLateenSails,
    iPlateArmor,
    iMonumentBuilding,
    iClassicalKnowledge,
    iAlchemy,
    iCivilService,  # teir 5
    iClockmaking,
    iPhilosophy,
    iEducation,
    iGuilds,
    iChivalry,  # tier 6
    # Late
    iOptics,
    iReplaceableParts,
    iPatronage,
    iGunpowder,
    iBanking,
    iMilitaryTradition,  # teir 7
    iShipbuilding,
    iDrama,
    iDivineRight,
    iChemistry,
    iPaper,
    iProfessionalArmy,  # teir 8
    iPrintingPress,
    iPublicWorks,
    iMatchlock,
    iArabicKnowledge,  # teir 9, around turn 304
    # Renaissance
    iAstronomy,
    iSteamEngines,
    iConstitution,
    iPolygonalFort,
    iArabicMedicine,  # teir 10
    iRenaissanceArt,
    iNationalism,
    iLiberalism,
    iScientificMethod,
    iMilitaryTactics,  # teir 11
    iNavalArchitecture,
    iCivilEngineering,
    iRightOfMan,
    iEconomics,
    iPhysics,
    iBiology,
    iCombinedArms,  # teir 12
    iTradingCompanies,
    iMachineTools,
    iFreeMarket,
    iExplosives,
    iMedicine,  # teir 13, TradingCompanies around turn 325
    iIndustrialTech,  # last tech, turn 500
) = range(iNumTechs)
iFutureTech = iIndustrialTech
iNumTechsFuture = 1


# Units: initialize unit variables to unit indices from XML

iNumUnits = 129
(
    iSettler,
    iWorker,
    iCatholicMissionary,
    iOrthodoxMissionary,
    iProtestantMissionary,
    iIslamicMissionary,
    iArcher,
    iCrossbowman,
    iArbalest,
    iGenoaBalestrieri,
    iLongbowman,
    iEnglishLongbowman,
    iSpearman,
    iGuisarme,
    iAragonAlmogavar,
    iScotlandSheltron,
    iPikeman,
    iHolyRomanLandsknecht,
    iAxeman,
    iVikingBerserker,
    iSwordsman,
    iDenmarkHuskarl,
    iLongSwordsman,
    iMaceman,
    iPortugalFootKnight,
    iLithuanianBajoras,
    iNovgorodUshkuinik,
    iGrenadier,
    iNetherlandsGrenadier,
    iArquebusier,
    iMusketman,
    iSwedishKarolin,
    iSpanishTercio,
    iFrenchMusketeer,
    iMoroccoBlackGuard,
    iLineInfantry,
    iDragoon,
    iScout,
    iMountedInfantry,
    iHorseArcher,
    iPistolier,
    iHussar,
    iPrussiaDeathsHeadHussar,
    iLancer,
    iBulgarianKonnik,
    iCordobanBerber,
    iHeavyLancer,
    iHungarianHuszar,
    iArabiaGhazi,
    iByzantineCataphract,
    iKievDruzhina,
    iKnight,
    iMoscowBoyar,
    iBurgundianPaladin,
    iCuirassier,
    iAustrianKurassier,
    iPolishWingedHussar,
    iTemplar,
    iTeutonic,
    iKnightofStJohns,
    iDragonKnight,
    iCalatravaKnight,
    iCatapult,
    iTrebuchet,
    iBombard,
    iTurkeyGreatBombard,
    iCannon,
    iFieldArtillery,
    iWorkboat,
    iGalley,
    iCogge,
    iHolk,
    iGalleon,
    iWarGalley,
    iGunGalley,
    iVeniceGalleas,
    iCarrack,
    iFrigate,
    iCaravel,
    iPrivateer,
    iSpy,
    iProsecutor,
    iHolyRelic,
    iGreatProphet,
    iGreatArtist,
    iGreatScientist,
    iGreatMerchant,
    iGreatEngineer,
    iGreatGeneral,
    iGreatSpy,
    iMongolKeshik,
    iSeljukLancer,
    iJanissary,
    iTagmata,
    iCorsair,
    iHighlander,
    iWelshLongbowman,
    iCondottieri,
    iSwissPikeman,
    iVarangianGuard,
    iHackapell,
    iReiter,
    iZaporozhianCossack,
    iDonCossack,
    iDoppelsoldner,
    iIrishBrigade,
    iStradiot,
    iWaardgelder,
    iNaffatun,
    iTurkopoles,
    iWalloonGuard,
    iSwissGun,
    iLipkaTatar,
    iHighlanderGun,
    iZanji,
    iTouareg,
    iNubianLongbowman,
    iBedouin,
    iTurcomanHorseArcher,
    iMamlukHeavyCavalry,
    iSouthSlavVlastela,
    iBohemianWarWagon,
    iLombardHeavyFootman,
    iSteppeHorseArcher,
    iCrimeanTatarRider,
    iSeljukCrossbow,
    iSeljukSwordsman,
    iSeljukFootman,
    iSeljukGuisarme,
) = range(iNumUnits)

# Bonuses: initialize bonus variables to bonus IDs from WBSinulAi

iNumBonus = 53
(
    iHemp,
    iCoal,
    iCopper,
    iHorse,
    iIron,
    iMarble,
    iStone,
    iBanana,
    iClam,
    iCorn,
    iCow,
    iCrab,
    iDeer,
    iFish,
    iPig,
    iRice,
    iSheep,
    iWheat,
    iDye,
    iFur,
    iGems,
    iGold,
    iIncense,
    iIvory,
    iSilk,
    iSilver,
    iSpices,
    iSugar,
    iWine,
    iWhale,
    iCotton,
    iApple,
    iBarley,
    iHoney,
    iPotato,
    iSalt,
    iSulphur,
    iTimber,
    iCoffee,
    iSlaves,
    iTea,
    iTobacco,
    iOlives,
    iAccess,
    iNorthAccess,
    iSouthAccess,
    iAsiaAccess,
    iAmber,
    iCitrus,
    iDates,
    iCamels,
    iCocoa,
    iOpium,
) = range(iNumBonus)


# Buildings

iNumBuildings = 176
(
    iPalace,
    iSummerPalace,
    iHeroicEpic,
    iNationalEpic,
    iNationalTheatre,
    iNationalGallery,
    iNationalUniversity,
    iRoyalDungeon,
    iRoyalAcademy,
    iStarFort,
    iWalls,
    iMoroccoKasbah,
    iCastle,
    iMoscowKremlin,
    iHungarianStronghold,
    iSpanishCitadel,
    iBarracks,
    iArcheryRange,
    iStable,
    iBulgarianStan,
    iGranary,
    iCordobanNoria,
    iPolishFolwark,
    iSmokehouse,
    iScotlandShieling,
    iAqueduct,
    iOttomanHammam,
    iHarbor,
    iVikingTradingPost,
    iLighthouse,
    iPortugalFeitoria,
    iAragonSeaport,
    iWharf,
    iCustomHouse,
    iDrydock,
    iForge,
    iGuildHall,
    iNovgorodKonets,
    iTextileMill,
    iUniversity,
    iObservatory,
    iPrussiaPublicSchool,
    iDenmarkResearchInstitute,
    iApothecary,
    iHospital,
    iTheatre,
    iByzantineHippodrome,
    iAustrianOperaHouse,
    iMarket,
    iArabicCaravan,
    iBrewery,
    iBurgundianWinery,
    iJeweler,
    iWeaver,
    iTannery,
    iInn,
    iCoffeeHouse,
    iLuxuryStore,
    iWarehouse,
    iBank,
    iGenoaBank,
    iEnglishRoyalExchange,
    iManorHouse,
    iFrenchChateau,
    iVeniceNavalBase,
    iCourthouse,
    iKievVeche,
    iHolyRomanRathaus,
    iLithuanianVoivodeship,
    iDungeon,
    iNightWatch,
    iSwedishTennant,
    iLevee,
    iNetherlandsDike,
    iPaganShrine,
    iJewishQuarter,
    iJewishShrine,
    iProtestantTemple,
    iProtestantSchool,
    iProtestantCathedral,
    iProtestantChapel,
    iProtestantSeminary,
    iProtestantShrine,
    iIslamicTemple,
    iIslamicChapel,
    iIslamicCathedral,
    iIslamicSchool,
    iIslamicMadrassa,
    iIslamicShrine,
    iCatholicTemple,
    iCatholicCathedral,
    iCatholicChapel,
    iCatholicMonastery,
    iCatholicSeminary,
    iCatholicShrine,
    iOrthodoxTemple,
    iOrthodoxCathedral,
    iOrthodoxChapel,
    iOrthodoxMonastery,
    iOrthodoxSeminary,
    iOrthodoxShrine,
    iReliquary,
    iInfirmary,
    iKontor,
    iCorporation1,
    iCorporation2,
    iCorporation3,
    iCorporation4,
    iCorporation5,
    iCorporation6,
    iCorporation7,
    iCorporation8,
    iCorporation9,
    iVersailles,
    iNotreDame,
    iLeaningTower,
    iSistineChapel,
    iTheodosianWalls,
    iTopkapiPalace,
    iJasnaGora,
    iShrineOfUppsala,
    iSamogitianAlkas,
    iGediminasTower,
    iGrandArsenal,
    iGalataTower,
    iKizilKule,
    iMontSaintMichel,
    iBoyanaChurch,
    iTorreDelOro,
    iFlorenceDuomo,
    iBorgundStaveChurch,
    iBlueMosque,
    iSelimiyeMosque,
    iAlAzhar,
    iMosqueOfKairouan,
    iKoutoubiaMosque,
    iStCatherineMonastery,
    iGreatLighthouse,
    iAlhambra,
    iKrakDesChevaliers,
    iSanMarco,
    iLaMezquita,
    iStBasil,
    iMagnaCarta,
    iSophiaKiev,
    iDomeRock,
    iBrandenburgGate,
    iPalacioDaPena,
    iMonasteryOfCluny,
    iRoundChurch,
    iLeonardosWorkshop,
    iGardensAlAndalus,
    iMagellansVoyage,
    iMarcoPolo,
    iEscorial,
    iKazimierz,
    iBelemTower,
    iGoldenBull,
    iKalmarCastle,
    iPalaisPapes,
    iTombAlWalid,
    iStephansdom,
    iBibliothecaCorviniana,
    iLouvre,
    iPeterhofPalace,
    iUraniborg,
    iThomaskirche,
    iFontainebleau,
    iImperialDiet,
    iBeurs,
    iCopernicus,
    iSanGiorgio,
    iWestminster,
    iPressburg,
    iLanterna,
    iTriumphalArch,
) = range(iNumBuildings)


# Projects, Colonies
iNumProjects = 25
(
    iEncyclopedie,
    iEastIndiaCompany,
    iWestIndiaCompany,
    iColVinland,
    iColGoldCoast,
    iColIvoryCoast,
    iColCuba,
    iColHispaniola,
    iColBrazil,
    iColHudson,
    iColVirginia,
    iColEastAfrica,
    iColFarEast,
    iColIndia,
    iColEastIndies,
    iColMalaysia,
    iColCapeTown,
    iColAztec,
    iColInca,
    iColQuebec,
    iColNewEngland,
    iColJamaica,
    iColPanama,
    iColLouisiana,
    iColPhillippines,
) = range(iNumProjects)
iNumNotColonies = 3
iNumTotalColonies = iNumProjects

# Specialists
iNumSpecialists = 14
(
    iCitizen,
    iSpecialistPriest,
    iSpecialistArtist,
    iSpecialistScientist,
    iSpecialistMerchant,
    iSpecialistEngineer,
    iSpecialistSpy,
    iSpecialistGreatProphet,
    iSpecialistGreatArtist,
    iSpecialistGreatScientist,
    iSpecialistGreatMerchant,
    iSpecialistGreatEngineer,
    iSpecialistGreatGeneral,
    iSpecialistGreatSpy,
) = range(iNumSpecialists)


# Improvements
iNumImprovements = 25
(
    iImprovementLandWorked,
    iImprovementWaterWorked,
    iImprovementCityRuins,
    iImprovementGoodyHut,
    iImprovementFarm,
    iImprovementFishingBoats,
    iImprovementWhalingBoats,
    iImprovementMine,
    iImprovementWorkshop,
    iImprovementLumbermill,
    iImprovementWindmill,
    iImprovementWatermill,
    iImprovementPlantation,
    iImprovementQuarry,
    iImprovementPasture,
    iImprovementCamp,
    iImprovementColonialTrade,
    iImprovementWinery,
    iImprovementCottage,
    iImprovementHamlet,
    iImprovementVillage,
    iImprovementTown,
    iImprovementFort,
    iImprovementForestPreserve,
    iImprovementApiary,
) = range(iNumImprovements)


# Civics
iNumCivics = 30
(
    iCivicDespotism,
    iCivicFeudalMonarchy,
    iCivicDivineMonarchy,
    iCivicLimitedMonarchy,
    iCivicMerchantRepublic,
    iCivicTibalLaw,
    iCivicFeudalLaw,
    iCivicBureaucracy,
    iCivicReligiousLaw,
    iCivicCommonLaw,
    iCivicTribalism,
    iCivicSerfdom,
    iCivicFreePeasantry,
    iCivicApprenticeship,
    iCivicFreeLabor,
    iCivicDecentralization,
    iCivicManorialism,
    iCivicTradeEconomy,
    iCivicGuilds,
    iCivicMercantilism,
    iCivicPaganism,
    iCivicStateReligion,
    iCivicTheocracy,
    iCivicOrganizedReligion,
    iCivicFreeReligion,
    iCivicSubjugation,
    iCivicVassalage,
    iCivicImperialism,
    iCivicOccupation,
    iCivicColonialism,
) = range(iNumCivics)


# Feature & terrain
iNumFeatures = 11
(
    iIce,
    iJungle,
    iDenseForest,
    iOasis,
    iFloodPlains,
    iWoodland,
    iMarsh,
    iPalmForest,
    iIslands,
    iReef,
    iPyramid,
) = range(iNumFeatures)

iNumTerrain = 14
(
    iTerrainGrass,
    iTerrainPlains,
    iTerrainSemiDesert,
    iTerrainDesert,
    iTerrainWetland,
    iTerrainMoorland,
    iTerrainTundra,
    iTerrainSnow,
    iTerrainFreshLake,
    iTerrainSaltLake,
    iTerrainCoast,
    iTerrainOcean,
    iTerrainPeak,
    iTerrainHill,
) = range(iNumTerrain)


# Promotions
iNumPromotions = 51
(
    iPromotionCombat1,
    iPromotionCombat2,
    iPromotionCombat3,
    iPromotionCombat4,
    iPromotionCombat5,
    iPromotionCover,
    iPromotionShock,
    iPromotionPinch,
    iPromotionFormation,
    iPromotionCharge,
    iPromotionAmbush,
    iPromotionFeint,
    iPromotionAmphibious,
    iPromotionMarch,
    iPromotionMedic1,
    iPromotionMedic2,
    iPromotionGuerilla1,
    iPromotionGuerilla2,
    iPromotionGuerilla3,
    iPromotionWoodsman1,
    iPromotionWoodsman2,
    iPromotionWoodsman3,
    iPromotionCityRaider1,
    iPromotionCityRaider2,
    iPromotionCityRaider3,
    iPromotionCityGarrison1,
    iPromotionCityGarrison2,
    iPromotionCityGarrison3,
    iPromotionDrill1,
    iPromotionDrill2,
    iPromotionDrill3,
    iPromotionDrill4,
    iPromotionBarrage1,
    iPromotionBarrage2,
    iPromotionBarrage3,
    iPromotionAccuracy,
    iPromotionFlanking1,
    iPromotionFlanking2,
    iPromotionSentry,
    iPromotionMobility,
    iPromotionNavigation,
    iPromotionNavigation2,
    iPromotionCargo,
    iPromotionLeader,
    iPromotionLeadership,
    iPromotionTactics,
    iPromotionCommando,
    iPromotionCombat6,
    iPromotionMorale,
    iPromotionMedic3,
    iPromotionMerc,
) = range(iNumPromotions)


# Leaders
iNumLeaders = 74
(
    iLeaderBarbarian,  # Do NOT name this iBarbarian.	#AbsintheRed: Renamed to iLeaderBarbarian - this is the way vanilla RFC uses it
    iYaqub_al_Mansur,
    iMaria_Theresa,
    iAbu_Bakr,
    iJoan,
    iMatthias,
    iBarbarossa,
    iCatherine,
    iCharlemagne,
    iPhilip_Ii,
    iSobieski,
    iChristian_Iv,
    iWilliam,
    iAfonso,
    iMehmed,
    iSaladin,
    iMaximilian,
    iSimeon,
    iPhilip_the_Bold,
    iJustinian,
    iAbd_ar_Rahman,
    iWillem_Van_Oranje,
    iElizabeth,
    iLouis_Xiv,
    iBoccanegra,
    iFrederick,
    iStephen,
    iYaroslav,
    iPeter,
    iCasimir,
    iJoao,
    iIsabella,
    iGustav_Vasa,
    iSuleiman,
    iEnrico_Dandolo,
    iThe_Pope,
    iHarald_Hardrada,
    iIvan_Iv,
    iGeorge_Iii,
    iMaria_I,
    iAndrea_Gritti,
    iHaakon_Iv,
    iMindaugas,
    iVytautas,
    iKarl_Xii,
    iIvan_Asen,
    iHarun_al_Rashid,
    iBela_III,
    iGustav_Adolf,
    iBasil_II,
    iPalaiologos,
    iMargaret_I,
    iMieszko,
    iPhilip_Augustus,
    iMstislav,
    iFerdinand_III,
    iBohdan_Khmelnytsky,
    iMohammed_ibn_Nasr,
    iOtto_I,
    iOtto_William,
    iBeatrice,
    iEmbriaco,
    iRobert_the_Bruce,
    iRurik,
    iAlexander_Nevsky,
    iMarfa,
    iIsmail_ibn_Sharif,
    iHermann_von_Salza,
    iJames_I,
    iHarald_Bluetooth,
    iMagnus_Ladulas,
    iJames_IV,
    iJohan_de_Witt,
    iJohn_II,
) = range(iNumLeaders)


################################ PROVINCES ################################
iP_MaxNumberOfProvinces = 150
(  # Iberia 0+
    iP_GaliciaSpain,
    iP_Castile,
    iP_Navarre,
    iP_Leon,
    iP_Lusitania,  # Portugal
    iP_LaMancha,
    iP_Catalonia,
    iP_Aragon,
    iP_Valencia,
    iP_Andalusia,
    # France 10+ # + 1 in the end
    iP_Bretagne,
    iP_Normandy,
    iP_Aquitania,
    iP_IleDeFrance,  # Paris
    iP_Provence,
    iP_Burgundy,
    iP_Orleans,
    iP_Champagne,
    iP_Flanders,
    iP_Netherlands,
    # Britania 20+ inc Ireland
    iP_London,
    iP_Wessex,
    iP_Wales,
    iP_Scotland,
    iP_Ireland,
    iP_Mercia,
    iP_EastAnglia,
    iP_Northumbria,
    iP_TheIsles,
    iP_Iceland,
    # Scandinavia 30+ inc Denmark
    iP_Denmark,
    iP_Osterland,
    iP_Norway,
    iP_Vestfold,
    iP_Gotaland,
    iP_Svealand,
    iP_Norrland,
    iP_Jamtland,
    iP_Skaneland,
    iP_Gotland,
    # Germany 40+, +1 dummy
    iP_Swabia,
    iP_Bavaria,
    iP_Bohemia,
    iP_Saxony,
    iP_Lorraine,
    iP_Franconia,
    iP_Brandenburg,
    iP_Holstein,
    iP_Prussia,
    iP_Dummy1,
    # Poland 50+, +1 dummy
    iP_Pomerania,
    iP_GaliciaPoland,
    iP_GreaterPoland,
    iP_Masovia,
    iP_LesserPoland,
    iP_Suvalkija,
    iP_Lithuania,
    iP_Livonia,
    iP_Estonia,
    iP_Dummy2,
    # Austria and Hungary 60+, +1 dummy
    iP_Carinthia,
    iP_Austria,
    iP_Slavonia,
    # iP_Tyrol = 63 # merged with Bavaria
    # iP_Salzburg = 63 # merged with Bavaria
    iP_Dummy3,
    iP_Transylvania,
    iP_Hungary,
    iP_Moravia,
    iP_Silesia,
    iP_Pannonia,
    iP_UpperHungary,
    # Italy 70+
    iP_Lombardy,
    iP_Verona,
    iP_Tuscany,
    iP_Latium,
    iP_Calabria,
    iP_Apulia,
    iP_Liguria,
    # Balkans 77+
    iP_Arberia,
    iP_Dalmatia,
    iP_Banat,
    iP_Moesia,
    iP_Constantinople,
    iP_Thrace,
    iP_Thessaly,
    iP_Macedonia,
    iP_Serbia,
    iP_Bosnia,
    # iP_Croatia = 86 # merged with Slavonia
    iP_Epirus,
    iP_Morea,
    iP_Wallachia,
    # Middle East 90+ inc Asia Minor
    iP_Jerusalem,
    iP_Paphlagonia,
    iP_Opsikion,
    iP_Thrakesion,
    iP_Cilicia,
    iP_Anatolikon,
    iP_Armeniakon,
    iP_Charsianon,
    iP_Colonea,
    iP_Antiochia,
    # North Africa 100+
    iP_Syria,
    iP_Lebanon,
    iP_Arabia,
    iP_Egypt,
    iP_Cyrenaica,
    iP_Tripolitania,
    iP_Ifriqiya,
    iP_Algiers,
    iP_Tetouan,
    iP_Oran,
    # Islands 110+ inc Sicily
    iP_Sicily,
    iP_Crete,
    iP_Cyprus,
    iP_Rhodes,
    iP_Corsica,
    iP_Sardinia,
    iP_Balears,
    iP_Canaries,
    iP_Azores,
    iP_Morocco,
    # Russia 120+
    iP_Moldova,
    iP_Crimea,
    iP_Novgorod,
    iP_Kuban,
    iP_Zaporizhia,
    iP_Rostov,
    iP_Moscow,
    iP_Vologda,
    iP_Smolensk,
    iP_Polotsk,
    iP_Murom,
    iP_Chernigov,
    iP_Pereyaslavl,
    iP_Sloboda,
    iP_Donets,
    iP_Kiev,
    iP_Podolia,
    iP_Minsk,
    iP_Brest,
    iP_Simbirsk,
    iP_NizhnyNovgorod,
    iP_Karelia,
    iP_Volhynia,
    # Rest
    iP_Sahara,
    iP_Thessaloniki,
    iP_Marrakesh,
    iP_Madeira,
    iP_Malta,
    iP_Fez,
    iP_Picardy,
) = range(iP_MaxNumberOfProvinces)


# these regions are for easier access for UHVs and Mercenaries
lRegionIberia = [
    iP_GaliciaSpain,
    iP_Castile,
    iP_Leon,
    iP_Lusitania,
    iP_Catalonia,
    iP_Aragon,
    iP_Valencia,
    iP_Andalusia,
    iP_Navarre,
    iP_LaMancha,
]
lRegionFrance = [iP_Normandy, iP_Bretagne, iP_IleDeFrance, iP_Orleans, iP_Picardy]
lRegionBurgundy = [iP_Provence, iP_Burgundy, iP_Champagne, iP_Flanders]
lRegionBritain = [
    iP_London,
    iP_Wales,
    iP_Wessex,
    iP_Scotland,
    iP_EastAnglia,
    iP_Mercia,
    iP_Northumbria,
    iP_Ireland,
]
lRegionScandinavia = [
    iP_Denmark,
    iP_Osterland,
    iP_Norway,
    iP_Vestfold,
    iP_Gotaland,
    iP_Svealand,
    iP_Norrland,
    iP_Jamtland,
    iP_Skaneland,
    iP_Gotland,
]
lRegionGermany = [
    iP_Lorraine,
    iP_Swabia,
    iP_Saxony,
    iP_Bavaria,
    iP_Franconia,
    iP_Brandenburg,
    iP_Holstein,
]
lRegionPoland = [
    iP_Pomerania,
    iP_GaliciaPoland,
    iP_GreaterPoland,
    iP_LesserPoland,
    iP_Silesia,
    iP_Masovia,
]
lRegionLithuania = [iP_Lithuania, iP_Livonia, iP_Estonia]
lRegionAustria = [iP_Carinthia, iP_Austria, iP_Moravia, iP_Bohemia, iP_Silesia]
lRegionHungary = [iP_Transylvania, iP_Hungary, iP_Slavonia, iP_Pannonia, iP_UpperHungary]
lRegionBalkans = [
    iP_Serbia,
    iP_Thrace,
    iP_Macedonia,
    iP_Moesia,
    iP_Arberia,
    iP_Dalmatia,
    iP_Bosnia,
    iP_Banat,
]
lRegionGreece = [iP_Constantinople, iP_Thessaly, iP_Epirus, iP_Morea, iP_Thessaloniki]
lRegionAsiaMinor = [
    iP_Colonea,
    iP_Charsianon,
    iP_Cilicia,
    iP_Armeniakon,
    iP_Anatolikon,
    iP_Paphlagonia,
    iP_Thrakesion,
    iP_Opsikion,
]
lRegionMiddleEast = [iP_Antiochia, iP_Syria, iP_Lebanon, iP_Arabia, iP_Jerusalem]
lRegionAfrica = [
    iP_Oran,
    iP_Algiers,
    iP_Ifriqiya,
    iP_Cyrenaica,
    iP_Tripolitania,
    iP_Tetouan,
    iP_Morocco,
    iP_Marrakesh,
    iP_Fez,
]
lRegionKiev = [
    iP_Moldova,
    iP_Kiev,
    iP_Crimea,
    iP_Zaporizhia,
    iP_Sloboda,
    iP_Pereyaslavl,
    iP_Chernigov,
    iP_Podolia,
    iP_Minsk,
]
lRegionItaly = [
    iP_Lombardy,
    iP_Liguria,
    iP_Verona,
    iP_Tuscany,
    iP_Latium,
    iP_Calabria,
    iP_Apulia,
    iP_Arberia,
    iP_Malta,
    iP_Dalmatia,
]
lRegionSwiss = [
    iP_Bavaria,
    iP_Austria,
    iP_Swabia,
    iP_Burgundy,
    iP_Lorraine,
    iP_Champagne,
    iP_Provence,
    iP_Lombardy,
    iP_Liguria,
    iP_Verona,
    iP_Franconia,
    iP_Bohemia,
]
# Hungarian UHV most territory in Europe:
lNotEurope = [
    iP_Oran,
    iP_Algiers,
    iP_Ifriqiya,
    iP_Cyrenaica,
    iP_Tripolitania,
    iP_Tetouan,
    iP_Morocco,
    iP_Marrakesh,
    iP_Fez,
    iP_Sahara,
    iP_Egypt,
    iP_Antiochia,
    iP_Syria,
    iP_Lebanon,
    iP_Arabia,
    iP_Jerusalem,
    iP_Colonea,
    iP_Charsianon,
    iP_Cilicia,
    iP_Armeniakon,
    iP_Anatolikon,
    iP_Paphlagonia,
    iP_Thrakesion,
    iP_Opsikion,
]


# Companies

iNumCompanies = 9
(
    iHospitallers,
    iTemplars,
    iTeutons,
    iHansa,
    iMedici,
    iAugsburg,
    iStGeorge,
    iDragon,
    iCalatrava,
) = range(iNumCompanies)
# Dates:		1096	1096	1096	1157	1397	1487	1407	1408	1164
# 			n/a		1312	n/a		1669	1499	n/a		1805	n/a		1838
tCompaniesBirth = (165, 165, 165, 186, 266, 295, 269, 269, 188)
tCompaniesDeath = (
    999,
    237,
    999,
    385,
    300,
    999,
    999,
    999,
    999,
)  # maybe add a couple extra turns for Templars and Medici?
tCompaniesLimit = (
    3,
    4,
    3,
    3,
    4,
    4,
    3,
    5,
    5,
)  # note that we have a modified limit for Hospitallers and Teutons after the Crusades

# Companies will only settle in their preferred regions
lCompanyRegions = [
    [
        iP_Antiochia,
        iP_Lebanon,
        iP_Jerusalem,
        iP_Cyprus,
        iP_Egypt,
        iP_Rhodes,
        iP_Crete,
        iP_Malta,
        iP_Sicily,
        iP_Corsica,
        iP_Sardinia,
        iP_Latium,
        iP_Calabria,
        iP_Apulia,
    ],
    [
        iP_Antiochia,
        iP_Lebanon,
        iP_Jerusalem,
        iP_Cyprus,
        iP_Egypt,
        iP_IleDeFrance,
        iP_Orleans,
        iP_Burgundy,
        iP_Champagne,
        iP_Picardy,
        iP_Provence,
        iP_Aquitania,
        iP_Normandy,
        iP_London,
        iP_Wales,
        iP_Wessex,
        iP_EastAnglia,
        iP_Mercia,
        iP_Northumbria,
    ],
    [
        iP_Antiochia,
        iP_Lebanon,
        iP_Jerusalem,
        iP_Cyprus,
        iP_Egypt,
        iP_Transylvania,
        iP_Prussia,
        iP_Livonia,
        iP_Estonia,
        iP_Pomerania,
        iP_Brandenburg,
        iP_Holstein,
        iP_Saxony,
        iP_Netherlands,
        iP_Flanders,
        iP_Lorraine,
        iP_Franconia,
        iP_Swabia,
        iP_Bavaria,
        iP_Bohemia,
        iP_Moravia,
        iP_Silesia,
    ],
    [
        iP_Saxony,
        iP_Brandenburg,
        iP_Holstein,
        iP_London,
        iP_EastAnglia,
        iP_Norway,
        iP_Vestfold,
        iP_Denmark,
        iP_Skaneland,
        iP_Gotaland,
        iP_Gotland,
        iP_Svealand,
        iP_Prussia,
        iP_Livonia,
        iP_Estonia,
        iP_Pomerania,
        iP_Netherlands,
        iP_Flanders,
        iP_Novgorod,
        iP_Karelia,
        iP_Osterland,
    ],
    [
        iP_Tuscany,
        iP_Lombardy,
        iP_Verona,
        iP_Latium,
        iP_Calabria,
        iP_Apulia,
        iP_Dalmatia,
        iP_Arberia,
        iP_Epirus,
        iP_Morea,
    ],
    [
        iP_Bavaria,
        iP_Swabia,
        iP_Franconia,
        iP_Austria,
        iP_Carinthia,
        iP_Bohemia,
        iP_Moravia,
        iP_Silesia,
        iP_UpperHungary,
        iP_Hungary,
        iP_Pannonia,
        iP_Slavonia,
    ],
    [
        iP_Liguria,
        iP_Lombardy,
        iP_Tuscany,
        iP_Latium,
        iP_Corsica,
        iP_Sardinia,
        iP_Sicily,
        iP_Calabria,
        iP_Apulia,
        iP_Provence,
        iP_Catalonia,
        iP_Balears,
    ],
    [
        iP_Hungary,
        iP_Pannonia,
        iP_UpperHungary,
        iP_Transylvania,
        iP_Slavonia,
        iP_Dalmatia,
        iP_Banat,
        iP_Bosnia,
        iP_Serbia,
        iP_Arberia,
        iP_Wallachia,
        iP_Moesia,
    ],
    [
        iP_GaliciaSpain,
        iP_Castile,
        iP_Leon,
        iP_Lusitania,
        iP_Catalonia,
        iP_Aragon,
        iP_Valencia,
        iP_Andalusia,
        iP_Navarre,
        iP_LaMancha,
        iP_Balears,
    ],
]


## Absinthe: was only needed for the AI regions, disabled them
## 3Miro: these regions are for the map and AI
# tRegionMap = [ [], # default region is empty
# [ iP_GaliciaSpain, iP_Castile, iP_Leon, iP_Lusitania, iP_Catalonia, iP_Aragon, iP_Navarre, iP_LaMancha, iP_Valencia, iP_Andalusia, iP_Bretagne, iP_Normandy, iP_Aquitania, iP_IleDeFrance, iP_Provence, iP_Burgundy, iP_Orleans, iP_Champagne, iP_Flanders, iP_Picardy, iP_London, iP_Wessex, iP_Wales, iP_Scotland, iP_Ireland, iP_Mercia, iP_EastAnglia, iP_Northumbria, iP_Iceland, iP_TheIsles ], # Western Europe
# [ iP_Norway, iP_Vestfold, iP_Gotaland, iP_Svealand, iP_Norrland, iP_Jamtland, iP_Skaneland, iP_Gotland ], # Northern Europe
# [ iP_Netherlands, iP_Denmark, iP_Swabia, iP_Bavaria, iP_Bohemia, iP_Saxony, iP_Lorraine, iP_Franconia, iP_Brandenburg, iP_Holstein, iP_Pomerania, iP_GaliciaPoland, iP_LesserPoland, iP_GreaterPoland, iP_Masovia, iP_Carinthia, iP_Austria, iP_Slavonia, iP_Transylvania, iP_Hungary, iP_Moravia, iP_Silesia, iP_Pannonia, iP_UpperHungary, iP_Lombardy, iP_Liguria, iP_Verona, iP_Tuscany, iP_Latium, iP_Calabria, iP_Apulia, iP_Arberia, iP_Dalmatia, iP_Bosnia, iP_Banat ], # Central Europe
# [ iP_Prussia, iP_Suvalkija, iP_Lithuania, iP_Livonia, iP_Moesia, iP_Constantinople, iP_Thrace, iP_Thessaly, iP_Macedonia, iP_Serbia, iP_Epirus, iP_Morea, iP_Wallachia, iP_Moldova, iP_Crimea, iP_Novgorod, iP_Kuban, iP_Zaporizhia, iP_Rostov, iP_Moscow, iP_Vologda, iP_Smolensk, iP_Polotsk, iP_Murom, iP_Chernigov, iP_Pereyaslavl, iP_Sloboda, iP_Donets, iP_Kiev, iP_Podolia, iP_Minsk, iP_Brest, iP_Simbirsk, iP_NizhnyNovgorod, iP_Karelia, iP_Volhynia, iP_Thessaloniki, iP_Estonia, iP_Osterland ], # Eastern Europe
# [ iP_Jerusalem, iP_Paphlagonia, iP_Opsikion, iP_Thrakesion, iP_Cilicia, iP_Anatolikon, iP_Armeniakon, iP_Charsianon, iP_Colonea, iP_Antiochia, iP_Syria, iP_Lebanon, iP_Arabia, iP_Egypt ], # Asia
# [ iP_Sicily, iP_Crete, iP_Cyprus, iP_Rhodes, iP_Corsica, iP_Sardinia, iP_Balears, iP_Canaries, iP_Azores, iP_Malta, iP_Madeira ], # Islands
# [ iP_Cyrenaica, iP_Tripolitania, iP_Ifriqiya, iP_Algiers, iP_Tetouan, iP_Oran, iP_Marrakesh, iP_Morocco, iP_Fez, iP_Sahara ], # North Africa
# ]
# iNumMapRegions = 8
