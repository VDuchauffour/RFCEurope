from CoreTypes import (
    Civ,
    CivilizationProperty,
    Leader,
    LeaderType,
    Religion,
    Scenario,
    StartingSituation,
)
from CoreStructures import (
    CivDataMapper,
    ScenarioDataMapper,
)
from TimelineData import DateTurn

CIV_PROPERTIES = CivDataMapper(
    {
        Civ.POPE: {
            CivilizationProperty.IS_PLAYABLE: False,
            CivilizationProperty.IS_MINOR: False,
        },
        Civ.INDEPENDENT: {
            CivilizationProperty.IS_PLAYABLE: False,
            CivilizationProperty.IS_MINOR: True,
        },
        Civ.INDEPENDENT_2: {
            CivilizationProperty.IS_PLAYABLE: False,
            CivilizationProperty.IS_MINOR: True,
        },
        Civ.INDEPENDENT_3: {
            CivilizationProperty.IS_PLAYABLE: True,
            CivilizationProperty.IS_MINOR: True,
        },
        Civ.INDEPENDENT_4: {
            CivilizationProperty.IS_PLAYABLE: True,
            CivilizationProperty.IS_MINOR: True,
        },
        Civ.BARBARIAN: {
            CivilizationProperty.IS_PLAYABLE: True,
            CivilizationProperty.IS_MINOR: True,
        },
    }
).fill_missing_members(
    {
        CivilizationProperty.IS_PLAYABLE: True,
        CivilizationProperty.IS_MINOR: False,
    }
)

CIV_STARTING_SITUATION_500AD = CivDataMapper(
    {
        Civ.BYZANTIUM: {
            StartingSituation.WORKERS: 0,
            StartingSituation.GOLD: 1200,
            StartingSituation.FAITH: 0,
        },
        Civ.FRANCE: {
            StartingSituation.WORKERS: 0,
            StartingSituation.GOLD: 100,
            StartingSituation.FAITH: 0,
        },
        Civ.ARABIA: {
            StartingSituation.WORKERS: 1,
            StartingSituation.GOLD: 200,
            StartingSituation.FAITH: 0,
        },
        Civ.BULGARIA: {
            StartingSituation.WORKERS: 1,
            StartingSituation.GOLD: 100,
            StartingSituation.FAITH: 0,
        },
        Civ.CORDOBA: {
            StartingSituation.WORKERS: 2,
            StartingSituation.GOLD: 200,
            StartingSituation.FAITH: 0,
        },
        Civ.VENECIA: {
            StartingSituation.WORKERS: 2,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 0,
        },
        Civ.BURGUNDY: {
            StartingSituation.WORKERS: 2,
            StartingSituation.GOLD: 250,
            StartingSituation.FAITH: 0,
        },
        Civ.GERMANY: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 0,
        },
        Civ.NOVGOROD: {
            StartingSituation.WORKERS: 2,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 0,
        },
        Civ.NORWAY: {
            StartingSituation.WORKERS: 2,
            StartingSituation.GOLD: 250,
            StartingSituation.FAITH: 0,
        },
        Civ.KIEV: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 250,
            StartingSituation.FAITH: 0,
        },
        Civ.HUNGARY: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 0,
        },
        Civ.CASTILLE: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 500,
            StartingSituation.FAITH: 0,
        },
        Civ.DENMARK: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 0,
        },
        Civ.SCOTLAND: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 0,
        },
        Civ.POLAND: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 0,
        },
        Civ.GENOA: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 0,
        },
        Civ.MOROCCO: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 0,
        },
        Civ.ENGLAND: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 0,
        },
        Civ.PORTUGAL: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 450,
            StartingSituation.FAITH: 0,
        },
        Civ.ARAGON: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 450,
            StartingSituation.FAITH: 0,
        },
        Civ.SWEDEN: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 0,
        },
        Civ.PRUSSIA: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 0,
        },
        Civ.LITHUANIA: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 0,
        },
        Civ.AUSTRIA: {
            StartingSituation.WORKERS: 4,
            StartingSituation.GOLD: 1000,
            StartingSituation.FAITH: 0,
        },
        Civ.OTTOMAN: {
            StartingSituation.WORKERS: 4,
            StartingSituation.GOLD: 1000,
            StartingSituation.FAITH: 0,
        },
        Civ.MOSCOW: {
            StartingSituation.WORKERS: 4,
            StartingSituation.GOLD: 500,
            StartingSituation.FAITH: 0,
        },
        Civ.DUTCH: {
            StartingSituation.WORKERS: 4,
            StartingSituation.GOLD: 1500,
            StartingSituation.FAITH: 0,
        },
        Civ.POPE: {
            StartingSituation.WORKERS: 0,
            StartingSituation.GOLD: 50,
            StartingSituation.FAITH: 0,
        },
    }
).fill_missing_members(None)

CIV_STARTING_SITUATION_1200AD = CivDataMapper(
    {
        Civ.BYZANTIUM: {
            StartingSituation.WORKERS: 0,
            StartingSituation.GOLD: 750,
            StartingSituation.FAITH: 40,
        },
        Civ.FRANCE: {
            StartingSituation.WORKERS: 0,
            StartingSituation.GOLD: 250,
            StartingSituation.FAITH: 30,
        },
        Civ.ARABIA: {
            StartingSituation.WORKERS: 1,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 50,
        },
        Civ.BULGARIA: {
            StartingSituation.WORKERS: 1,
            StartingSituation.GOLD: 150,
            StartingSituation.FAITH: 50,
        },
        Civ.CORDOBA: {
            StartingSituation.WORKERS: 2,
            StartingSituation.GOLD: 0,
            StartingSituation.FAITH: 0,
        },
        Civ.VENECIA: {
            StartingSituation.WORKERS: 2,
            StartingSituation.GOLD: 500,
            StartingSituation.FAITH: 25,
        },
        Civ.BURGUNDY: {
            StartingSituation.WORKERS: 2,
            StartingSituation.GOLD: 0,
            StartingSituation.FAITH: 0,
        },
        Civ.GERMANY: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 30,
        },
        Civ.NOVGOROD: {
            StartingSituation.WORKERS: 2,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 25,
        },
        Civ.NORWAY: {
            StartingSituation.WORKERS: 2,
            StartingSituation.GOLD: 250,
            StartingSituation.FAITH: 0,
        },
        Civ.KIEV: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 250,
            StartingSituation.FAITH: 20,
        },
        Civ.HUNGARY: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 25,
        },
        Civ.CASTILLE: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 500,
            StartingSituation.FAITH: 35,
        },
        Civ.DENMARK: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 20,
        },
        Civ.SCOTLAND: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 20,
        },
        Civ.POLAND: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 30,
        },
        Civ.GENOA: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 500,
            StartingSituation.FAITH: 25,
        },
        Civ.MOROCCO: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 35,
        },
        Civ.ENGLAND: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 20,
        },
        Civ.PORTUGAL: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 450,
            StartingSituation.FAITH: 20,
        },
        Civ.ARAGON: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 450,
            StartingSituation.FAITH: 10,
        },
        Civ.SWEDEN: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 0,
        },
        Civ.PRUSSIA: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 300,
            StartingSituation.FAITH: 0,
        },
        Civ.LITHUANIA: {
            StartingSituation.WORKERS: 3,
            StartingSituation.GOLD: 400,
            StartingSituation.FAITH: 0,
        },
        Civ.AUSTRIA: {
            StartingSituation.WORKERS: 4,
            StartingSituation.GOLD: 1000,
            StartingSituation.FAITH: 0,
        },
        Civ.OTTOMAN: {
            StartingSituation.WORKERS: 4,
            StartingSituation.GOLD: 1000,
            StartingSituation.FAITH: 0,
        },
        Civ.MOSCOW: {
            StartingSituation.WORKERS: 4,
            StartingSituation.GOLD: 500,
            StartingSituation.FAITH: 0,
        },
        Civ.DUTCH: {
            StartingSituation.WORKERS: 4,
            StartingSituation.GOLD: 1500,
            StartingSituation.FAITH: 0,
        },
        Civ.POPE: {
            StartingSituation.WORKERS: 0,
            StartingSituation.GOLD: 200,
            StartingSituation.FAITH: 0,
        },
    }
).fill_missing_members(None)

CIV_STARTING_SITUATION = ScenarioDataMapper(
    {
        Scenario.i500AD: CIV_STARTING_SITUATION_500AD,
        Scenario.i1200AD: CIV_STARTING_SITUATION_1200AD,
    }
)

CIV_STABILITY_AI_BONUS = CivDataMapper(
    {
        Civ.BYZANTIUM: 0,
        Civ.FRANCE: 4,
        Civ.ARABIA: 4,
        Civ.BULGARIA: 3,
        Civ.CORDOBA: 2,
        Civ.VENECIA: 3,
        Civ.BURGUNDY: 0,
        Civ.GERMANY: 0,
        Civ.NOVGOROD: 3,
        Civ.NORWAY: 0,
        Civ.KIEV: 6,
        Civ.HUNGARY: 2,
        Civ.CASTILLE: 0,
        Civ.DENMARK: 0,
        Civ.SCOTLAND: 0,
        Civ.POLAND: 0,
        Civ.GENOA: 2,
        Civ.MOROCCO: 0,
        Civ.ENGLAND: 0,
        Civ.PORTUGAL: 0,
        Civ.ARAGON: 4,
        Civ.SWEDEN: 0,
        Civ.PRUSSIA: 3,
        Civ.LITHUANIA: 0,
        Civ.AUSTRIA: 4,
        Civ.OTTOMAN: 8,
        Civ.MOSCOW: 0,
        Civ.DUTCH: 0,
    }
).fill_missing_members(None)

CIV_INITIAL_CONTACTS_500AD = CivDataMapper(
    {
        Civ.BYZANTIUM: [
            Civ.POPE,
        ],
        Civ.ARABIA: [
            Civ.BYZANTIUM,
        ],
        Civ.BULGARIA: [
            Civ.BYZANTIUM,
        ],
        Civ.CORDOBA: [
            Civ.ARABIA,
        ],
        Civ.VENECIA: [
            Civ.BYZANTIUM,
            Civ.POPE,
        ],
        Civ.BURGUNDY: [
            Civ.FRANCE,
        ],
        Civ.GERMANY: [
            Civ.BURGUNDY,
            Civ.FRANCE,
        ],
        Civ.NOVGOROD: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
        ],
        Civ.KIEV: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
            Civ.NOVGOROD,
        ],
        Civ.HUNGARY: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
            Civ.KIEV,
        ],
        Civ.CASTILLE: [
            Civ.FRANCE,
            Civ.BURGUNDY,
            Civ.CORDOBA,
        ],
        Civ.DENMARK: [
            Civ.NORWAY,
            Civ.GERMANY,
        ],
        Civ.SCOTLAND: [
            Civ.FRANCE,
            Civ.NORWAY,
        ],
        Civ.POLAND: [
            Civ.GERMANY,
            Civ.HUNGARY,
        ],
        Civ.GENOA: [
            Civ.BURGUNDY,
            Civ.BYZANTIUM,
            Civ.VENECIA,
            Civ.POPE,
        ],
        Civ.MOROCCO: [
            Civ.ARABIA,
            Civ.CASTILLE,
            Civ.CORDOBA,
        ],
        Civ.ENGLAND: [
            Civ.FRANCE,
            Civ.DENMARK,
            Civ.SCOTLAND,
            Civ.NORWAY,
        ],
        Civ.PORTUGAL: [
            Civ.CASTILLE,
            Civ.CORDOBA,
        ],
        Civ.ARAGON: [
            Civ.BURGUNDY,
            Civ.CASTILLE,
            Civ.CORDOBA,
            Civ.FRANCE,
        ],
        Civ.SWEDEN: [
            Civ.DENMARK,
            Civ.NORWAY,
            Civ.NOVGOROD,
        ],
        Civ.PRUSSIA: [
            Civ.GERMANY,
            Civ.POLAND,
            Civ.NOVGOROD,
        ],
        Civ.LITHUANIA: [
            Civ.POLAND,
            Civ.KIEV,
            Civ.NOVGOROD,
            Civ.PRUSSIA,
        ],
        Civ.AUSTRIA: [
            Civ.GERMANY,
            Civ.VENECIA,
            Civ.POLAND,
            Civ.HUNGARY,
        ],
        Civ.OTTOMAN: [
            Civ.BYZANTIUM,
            Civ.ARABIA,
        ],
        Civ.MOSCOW: [
            Civ.KIEV,
            Civ.NOVGOROD,
            Civ.LITHUANIA,
        ],
        Civ.DUTCH: [
            Civ.ENGLAND,
            Civ.CASTILLE,
            Civ.FRANCE,
            Civ.GERMANY,
            Civ.DENMARK,
            Civ.NORWAY,
        ],
    }
).fill_missing_members(None)

CIV_INITIAL_CONTACTS_1200AD = CivDataMapper(
    {
        Civ.BYZANTIUM: [
            Civ.POPE,
            Civ.VENECIA,
            Civ.GENOA,
            Civ.HUNGARY,
            Civ.BULGARIA,
            Civ.ARABIA,
            Civ.KIEV,
            Civ.NOVGOROD,
        ],
        Civ.FRANCE: [
            Civ.SCOTLAND,
            Civ.ENGLAND,
            Civ.NORWAY,
            Civ.ARAGON,
            Civ.CASTILLE,
            Civ.GERMANY,
        ],
        Civ.ARABIA: [
            Civ.BYZANTIUM,
            Civ.MOROCCO,
        ],
        Civ.BULGARIA: [
            Civ.BYZANTIUM,
            Civ.KIEV,
            Civ.NOVGOROD,
            Civ.VENECIA,
            Civ.HUNGARY,
        ],
        Civ.VENECIA: [
            Civ.BYZANTIUM,
            Civ.GENOA,
            Civ.HUNGARY,
            Civ.POPE,
        ],
        Civ.GERMANY: [
            Civ.NORWAY,
            Civ.FRANCE,
            Civ.DENMARK,
            Civ.ENGLAND,
            Civ.POLAND,
            Civ.HUNGARY,
            Civ.VENECIA,
            Civ.GENOA,
            Civ.POPE,
        ],
        Civ.NOVGOROD: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
            Civ.KIEV,
            Civ.POLAND,
        ],
        Civ.NORWAY: [
            Civ.DENMARK,
            Civ.ENGLAND,
            Civ.SCOTLAND,
            Civ.FRANCE,
        ],
        Civ.KIEV: [
            Civ.BYZANTIUM,
            Civ.HUNGARY,
            Civ.BULGARIA,
            Civ.NOVGOROD,
        ],
        Civ.HUNGARY: [
            Civ.BYZANTIUM,
            Civ.BULGARIA,
            Civ.KIEV,
            Civ.VENECIA,
            Civ.GERMANY,
            Civ.POLAND,
            Civ.POPE,
        ],
        Civ.CASTILLE: [
            Civ.MOROCCO,
            Civ.ARAGON,
            Civ.PORTUGAL,
            Civ.FRANCE,
            Civ.CORDOBA,
        ],
        Civ.DENMARK: [
            Civ.NORWAY,
            Civ.GERMANY,
            Civ.FRANCE,
            Civ.ENGLAND,
            Civ.POLAND,
        ],
        Civ.SCOTLAND: [
            Civ.NORWAY,
            Civ.GERMANY,
            Civ.FRANCE,
            Civ.ENGLAND,
        ],
        Civ.POLAND: [
            Civ.GERMANY,
            Civ.HUNGARY,
            Civ.DENMARK,
            Civ.KIEV,
            Civ.NOVGOROD,
        ],
        Civ.GENOA: [
            Civ.BYZANTIUM,
            Civ.FRANCE,
            Civ.VENECIA,
            Civ.GERMANY,
            Civ.POPE,
        ],
        Civ.MOROCCO: [
            Civ.ARABIA,
            Civ.CASTILLE,
            Civ.ARAGON,
            Civ.PORTUGAL,
        ],
        Civ.ENGLAND: [
            Civ.FRANCE,
            Civ.DENMARK,
            Civ.SCOTLAND,
            Civ.NORWAY,
            Civ.POPE,
        ],
        Civ.PORTUGAL: [
            Civ.CASTILLE,
            Civ.MOROCCO,
            Civ.ARAGON,
            Civ.POPE,
        ],
        Civ.ARAGON: [
            Civ.CASTILLE,
            Civ.PORTUGAL,
            Civ.MOROCCO,
            Civ.GENOA,
            Civ.POPE,
        ],
        Civ.SWEDEN: [
            Civ.POLAND,
            Civ.GERMANY,
            Civ.DENMARK,
            Civ.NORWAY,
            Civ.NOVGOROD,
        ],
        Civ.PRUSSIA: [
            Civ.GERMANY,
            Civ.POLAND,
            Civ.NOVGOROD,
        ],
        Civ.LITHUANIA: [
            Civ.POLAND,
            Civ.KIEV,
            Civ.PRUSSIA,
        ],
        Civ.AUSTRIA: [
            Civ.GERMANY,
            Civ.VENECIA,
            Civ.POLAND,
            Civ.HUNGARY,
        ],
        Civ.OTTOMAN: [
            Civ.BYZANTIUM,
            Civ.HUNGARY,
            Civ.ARABIA,
        ],
        Civ.MOSCOW: [
            Civ.KIEV,
            Civ.NOVGOROD,
            Civ.SWEDEN,
            Civ.LITHUANIA,
        ],
        Civ.DUTCH: [
            Civ.ENGLAND,
            Civ.CASTILLE,
            Civ.FRANCE,
            Civ.GERMANY,
            Civ.DENMARK,
            Civ.NORWAY,
            Civ.SWEDEN,
        ],
    }
).fill_missing_members(None)

CIV_INITIAL_CONTACTS = ScenarioDataMapper(
    {
        Scenario.i500AD: CIV_INITIAL_CONTACTS_500AD,
        Scenario.i1200AD: CIV_INITIAL_CONTACTS_1200AD,
    }
)

CIV_INITIAL_WARS_500AD = CivDataMapper(
    {
        Civ.BYZANTIUM: CivDataMapper(
            {
                Civ.ARABIA: 90,
                Civ.BULGARIA: 90,
                Civ.OTTOMAN: 90,
            }
        ).fill_missing_members(0),
        Civ.FRANCE: CivDataMapper(
            {
                Civ.ENGLAND: 60,
            }
        ).fill_missing_members(0),
        Civ.ARABIA: CivDataMapper(
            {
                Civ.OTTOMAN: 60,
            }
        ).fill_missing_members(0),
        Civ.BULGARIA: CivDataMapper(
            {
                Civ.OTTOMAN: 70,
            }
        ).fill_missing_members(0),
        Civ.CORDOBA: CivDataMapper(
            {
                Civ.CASTILLE: 90,
                Civ.PORTUGAL: 90,
                Civ.ARAGON: 80,
            }
        ).fill_missing_members(0),
        Civ.NOVGOROD: CivDataMapper(
            {
                Civ.PRUSSIA: 80,
            }
        ).fill_missing_members(0),
        Civ.DENMARK: CivDataMapper(
            {
                Civ.SWEDEN: 60,
            }
        ).fill_missing_members(0),
        Civ.SCOTLAND: CivDataMapper(
            {
                Civ.ENGLAND: 60,
            }
        ).fill_missing_members(0),
        Civ.POLAND: CivDataMapper(
            {
                Civ.PRUSSIA: 20,
            }
        ).fill_missing_members(0),
        Civ.PRUSSIA: CivDataMapper(
            {
                Civ.LITHUANIA: 80,
            }
        ).fill_missing_members(0),
        Civ.OTTOMAN: CivDataMapper(
            {
                Civ.INDEPENDENT: 50,
                Civ.INDEPENDENT_2: 50,
                Civ.INDEPENDENT_3: 50,
                Civ.INDEPENDENT_4: 50,
            }
        ).fill_missing_members(0),
    }
).fill_missing_members(CivDataMapper({}).fill_missing_members(0))

CIV_INITIAL_WARS_1200AD = CivDataMapper(
    {
        Civ.BYZANTIUM: CivDataMapper(
            {
                Civ.ARABIA: 20,
                Civ.BULGARIA: 70,
                Civ.VENECIA: 90,
                Civ.OTTOMAN: 90,
            }
        ).fill_missing_members(0),
        Civ.FRANCE: CivDataMapper(
            {
                Civ.ARABIA: 30,
                Civ.ENGLAND: 90,
            }
        ).fill_missing_members(0),
        Civ.ARABIA: CivDataMapper(
            {
                Civ.GERMANY: 20,
                Civ.HUNGARY: 20,
                Civ.CASTILLE: 30,
                Civ.GENOA: 20,
                Civ.ENGLAND: 20,
                Civ.PORTUGAL: 20,
                Civ.ARAGON: 10,
                Civ.OTTOMAN: 60,
            }
        ).fill_missing_members(0),
        Civ.BULGARIA: CivDataMapper(
            {
                Civ.OTTOMAN: 70,
            }
        ).fill_missing_members(0),
        Civ.CORDOBA: CivDataMapper(
            {
                Civ.PORTUGAL: 90,
            }
        ).fill_missing_members(0),
        Civ.NOVGOROD: CivDataMapper(
            {
                Civ.PRUSSIA: 80,
            }
        ).fill_missing_members(0),
        Civ.DENMARK: CivDataMapper(
            {
                Civ.SWEDEN: 60,
            }
        ).fill_missing_members(0),
        Civ.SCOTLAND: CivDataMapper(
            {
                Civ.ENGLAND: 60,
            }
        ).fill_missing_members(0),
        Civ.POLAND: CivDataMapper(
            {
                Civ.PRUSSIA: 20,
            }
        ).fill_missing_members(0),
        Civ.MOROCCO: CivDataMapper(
            {
                Civ.CASTILLE: 90,
                Civ.PORTUGAL: 80,
                Civ.ARAGON: 80,
            }
        ).fill_missing_members(0),
        Civ.PRUSSIA: CivDataMapper(
            {
                Civ.LITHUANIA: 80,
            }
        ).fill_missing_members(0),
        Civ.OTTOMAN: CivDataMapper(
            {
                Civ.INDEPENDENT: 50,
                Civ.INDEPENDENT_2: 50,
                Civ.INDEPENDENT_3: 50,
                Civ.INDEPENDENT_4: 50,
            }
        ).fill_missing_members(0),
    }
).fill_missing_members(CivDataMapper({}).fill_missing_members(0))

CIV_INITIAL_WARS = ScenarioDataMapper(
    {
        Scenario.i500AD: CIV_INITIAL_WARS_500AD,
        Scenario.i1200AD: CIV_INITIAL_WARS_1200AD,
    }
)

# Used for mercenaries (Higher number = less likely to hire)
CIV_HIRE_MERCENARY_THRESHOLD = CivDataMapper(
    {
        Civ.BYZANTIUM: 10,
        Civ.FRANCE: 30,
        Civ.ARABIA: 50,
        Civ.BULGARIA: 10,
        Civ.CORDOBA: 50,
        Civ.VENECIA: 30,
        Civ.BURGUNDY: 10,
        Civ.GERMANY: 70,
        Civ.NOVGOROD: 30,
        Civ.NORWAY: 60,
        Civ.KIEV: 40,
        Civ.HUNGARY: 10,
        Civ.CASTILLE: 40,
        Civ.DENMARK: 30,
        Civ.SCOTLAND: 50,
        Civ.POLAND: 60,
        Civ.GENOA: 30,
        Civ.MOROCCO: 40,
        Civ.ENGLAND: 70,
        Civ.PORTUGAL: 40,
        Civ.ARAGON: 30,
        Civ.SWEDEN: 30,
        Civ.PRUSSIA: 50,
        Civ.LITHUANIA: 20,
        Civ.AUSTRIA: 20,
        Civ.OTTOMAN: 80,
        Civ.MOSCOW: 60,
        Civ.DUTCH: 30,
        Civ.POPE: 80,
        Civ.INDEPENDENT: 50,
        Civ.INDEPENDENT_2: 50,
        Civ.INDEPENDENT_3: 50,
        Civ.INDEPENDENT_4: 50,
        Civ.BARBARIAN: 50,
    }
)

# Not used
CIV_AI_AGGRRESSION_LEVEL = CivDataMapper(
    {
        Civ.BYZANTIUM: 1,
        Civ.FRANCE: 1,
        Civ.ARABIA: 2,
        Civ.BULGARIA: 2,
        Civ.CORDOBA: 1,
        Civ.VENECIA: 0,
        Civ.BURGUNDY: 0,
        Civ.GERMANY: 1,
        Civ.NOVGOROD: 0,
        Civ.NORWAY: 2,
        Civ.KIEV: 1,
        Civ.HUNGARY: 2,
        Civ.CASTILLE: 2,
        Civ.DENMARK: 2,
        Civ.SCOTLAND: 0,
        Civ.POLAND: 0,
        Civ.GENOA: 0,
        Civ.MOROCCO: 2,
        Civ.ENGLAND: 1,
        Civ.PORTUGAL: 2,
        Civ.ARAGON: 1,
        Civ.SWEDEN: 2,
        Civ.PRUSSIA: 2,
        Civ.LITHUANIA: 1,
        Civ.AUSTRIA: 1,
        Civ.OTTOMAN: 2,
        Civ.MOSCOW: 1,
        Civ.DUTCH: 0,
    }
).fill_missing_members(None)

# Used for war during rise and respawn of new civs (Higher number means less chance for war)
CIV_AI_STOP_BIRTH_THRESHOLD = CivDataMapper(
    {
        Civ.BYZANTIUM: 30,
        Civ.FRANCE: 60,
        Civ.ARABIA: 50,
        Civ.BULGARIA: 70,
        Civ.CORDOBA: 20,
        Civ.VENECIA: 50,
        Civ.BURGUNDY: 70,
        Civ.GERMANY: 80,
        Civ.NOVGOROD: 80,
        Civ.NORWAY: 70,
        Civ.KIEV: 80,
        Civ.HUNGARY: 60,
        Civ.CASTILLE: 70,
        Civ.DENMARK: 40,
        Civ.SCOTLAND: 40,
        Civ.POLAND: 80,
        Civ.GENOA: 80,
        Civ.MOROCCO: 50,
        Civ.ENGLAND: 30,
        Civ.PORTUGAL: 60,
        Civ.ARAGON: 60,
        Civ.SWEDEN: 70,
        Civ.PRUSSIA: 30,
        Civ.LITHUANIA: 50,
        Civ.AUSTRIA: 50,
        Civ.OTTOMAN: 70,
        Civ.MOSCOW: 70,
        Civ.DUTCH: 80,
        Civ.POPE: 90,
    }
).fill_missing_members(0)

# Used to tune frequency of resurrections.
CIV_RESPAWNING_THRESHOLD = CivDataMapper(
    {
        Civ.BYZANTIUM: 30,
        Civ.FRANCE: 80,
        Civ.ARABIA: 60,
        Civ.BULGARIA: 30,
        Civ.CORDOBA: 20,
        Civ.VENECIA: 40,
        Civ.BURGUNDY: 20,
        Civ.GERMANY: 70,
        Civ.NOVGOROD: 20,
        Civ.NORWAY: 50,
        Civ.KIEV: 30,
        Civ.HUNGARY: 60,
        Civ.CASTILLE: 80,
        Civ.DENMARK: 70,
        Civ.SCOTLAND: 40,
        Civ.POLAND: 60,
        Civ.GENOA: 30,
        Civ.MOROCCO: 60,
        Civ.ENGLAND: 70,
        Civ.PORTUGAL: 60,
        Civ.ARAGON: 20,
        Civ.SWEDEN: 70,
        Civ.PRUSSIA: 50,
        Civ.LITHUANIA: 50,
        Civ.AUSTRIA: 70,
        Civ.OTTOMAN: 70,
        Civ.MOSCOW: 80,
        Civ.DUTCH: 60,
        Civ.POPE: 90,
    }
).fill_missing_members(None)

CIV_RELIGION_SPEADING_THRESHOLD = CivDataMapper(
    {
        Civ.BYZANTIUM: {
            Religion.PROTESTANTISM: 100,
            Religion.ISLAM: 50,
            Religion.CATHOLICISM: 70,
            Religion.ORTHODOXY: 150,
            Religion.JUDAISM: 10,
        },
        Civ.FRANCE: {
            Religion.PROTESTANTISM: 150,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 250,
            Religion.ORTHODOXY: 70,
            Religion.JUDAISM: 10,
        },
        Civ.ARABIA: {
            Religion.PROTESTANTISM: 20,
            Religion.ISLAM: 350,
            Religion.CATHOLICISM: 50,
            Religion.ORTHODOXY: 10,
            Religion.JUDAISM: 10,
        },
        Civ.BULGARIA: {
            Religion.PROTESTANTISM: 80,
            Religion.ISLAM: 50,
            Religion.CATHOLICISM: 80,
            Religion.ORTHODOXY: 400,
            Religion.JUDAISM: 10,
        },
        Civ.CORDOBA: {
            Religion.PROTESTANTISM: 50,
            Religion.ISLAM: 250,
            Religion.CATHOLICISM: 80,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.VENECIA: {
            Religion.PROTESTANTISM: 90,
            Religion.ISLAM: 50,
            Religion.CATHOLICISM: 200,
            Religion.ORTHODOXY: 30,
            Religion.JUDAISM: 10,
        },
        Civ.BURGUNDY: {
            Religion.PROTESTANTISM: 150,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 150,
            Religion.ORTHODOXY: 70,
            Religion.JUDAISM: 10,
        },
        Civ.GERMANY: {
            Religion.PROTESTANTISM: 450,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 250,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.NOVGOROD: {
            Religion.PROTESTANTISM: 60,
            Religion.ISLAM: 40,
            Religion.CATHOLICISM: 60,
            Religion.ORTHODOXY: 500,
            Religion.JUDAISM: 10,
        },
        Civ.NORWAY: {
            Religion.PROTESTANTISM: 250,
            Religion.ISLAM: 50,
            Religion.CATHOLICISM: 150,
            Religion.ORTHODOXY: 80,
            Religion.JUDAISM: 10,
        },
        Civ.KIEV: {
            Religion.PROTESTANTISM: 90,
            Religion.ISLAM: 60,
            Religion.CATHOLICISM: 90,
            Religion.ORTHODOXY: 400,
            Religion.JUDAISM: 10,
        },
        Civ.HUNGARY: {
            Religion.PROTESTANTISM: 250,
            Religion.ISLAM: 60,
            Religion.CATHOLICISM: 200,
            Religion.ORTHODOXY: 80,
            Religion.JUDAISM: 10,
        },
        Civ.CASTILLE: {
            Religion.PROTESTANTISM: 100,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 200,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.DENMARK: {
            Religion.PROTESTANTISM: 250,
            Religion.ISLAM: 50,
            Religion.CATHOLICISM: 180,
            Religion.ORTHODOXY: 80,
            Religion.JUDAISM: 10,
        },
        Civ.SCOTLAND: {
            Religion.PROTESTANTISM: 450,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 100,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.POLAND: {
            Religion.PROTESTANTISM: 200,
            Religion.ISLAM: 60,
            Religion.CATHOLICISM: 450,
            Religion.ORTHODOXY: 200,
            Religion.JUDAISM: 10,
        },
        Civ.GENOA: {
            Religion.PROTESTANTISM: 190,
            Religion.ISLAM: 50,
            Religion.CATHOLICISM: 250,
            Religion.ORTHODOXY: 30,
            Religion.JUDAISM: 10,
        },
        Civ.MOROCCO: {
            Religion.PROTESTANTISM: 50,
            Religion.ISLAM: 250,
            Religion.CATHOLICISM: 70,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.ENGLAND: {
            Religion.PROTESTANTISM: 450,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 100,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.PORTUGAL: {
            Religion.PROTESTANTISM: 200,
            Religion.ISLAM: 80,
            Religion.CATHOLICISM: 250,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.ARAGON: {
            Religion.PROTESTANTISM: 150,
            Religion.ISLAM: 80,
            Religion.CATHOLICISM: 250,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.SWEDEN: {
            Religion.PROTESTANTISM: 450,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 200,
            Religion.ORTHODOXY: 50,
            Religion.JUDAISM: 10,
        },
        Civ.PRUSSIA: {
            Religion.PROTESTANTISM: 450,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 250,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.LITHUANIA: {
            Religion.PROTESTANTISM: 80,
            Religion.ISLAM: 80,
            Religion.CATHOLICISM: 80,
            Religion.ORTHODOXY: 80,
            Religion.JUDAISM: 10,
        },
        Civ.AUSTRIA: {
            Religion.PROTESTANTISM: 200,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 250,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.OTTOMAN: {
            Religion.PROTESTANTISM: 20,
            Religion.ISLAM: 350,
            Religion.CATHOLICISM: 80,
            Religion.ORTHODOXY: 80,
            Religion.JUDAISM: 10,
        },
        Civ.MOSCOW: {
            Religion.PROTESTANTISM: 100,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 100,
            Religion.ORTHODOXY: 250,
            Religion.JUDAISM: 10,
        },
        Civ.DUTCH: {
            Religion.PROTESTANTISM: 550,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 90,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
        Civ.POPE: {
            Religion.PROTESTANTISM: 10,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 500,
            Religion.ORTHODOXY: 10,
            Religion.JUDAISM: 10,
        },
        Civ.INDEPENDENT: {
            Religion.PROTESTANTISM: 250,
            Religion.ISLAM: 100,
            Religion.CATHOLICISM: 100,
            Religion.ORTHODOXY: 100,
            Religion.JUDAISM: 10,
        },
        Civ.INDEPENDENT_2: {
            Religion.PROTESTANTISM: 250,
            Religion.ISLAM: 100,
            Religion.CATHOLICISM: 100,
            Religion.ORTHODOXY: 100,
            Religion.JUDAISM: 10,
        },
        Civ.INDEPENDENT_3: {
            Religion.PROTESTANTISM: 250,
            Religion.ISLAM: 100,
            Religion.CATHOLICISM: 100,
            Religion.ORTHODOXY: 100,
            Religion.JUDAISM: 10,
        },
        Civ.INDEPENDENT_4: {
            Religion.PROTESTANTISM: 250,
            Religion.ISLAM: 100,
            Religion.CATHOLICISM: 100,
            Religion.ORTHODOXY: 100,
            Religion.JUDAISM: 10,
        },
        Civ.BARBARIAN: {
            Religion.PROTESTANTISM: 20,
            Religion.ISLAM: 20,
            Religion.CATHOLICISM: 20,
            Religion.ORTHODOXY: 20,
            Religion.JUDAISM: 10,
        },
    }
)

# 100 and 80: don't purge any religions; 60: purge islam if christian, and all christian religions if muslim; 40: also judaism; 20: all but state religion
CIV_RELIGIOUS_TOLERANCE = CivDataMapper(
    {
        Civ.BYZANTIUM: 60,
        Civ.FRANCE: 40,
        Civ.ARABIA: 60,
        Civ.BULGARIA: 40,
        Civ.CORDOBA: 80,
        Civ.VENECIA: 40,
        Civ.BURGUNDY: 20,
        Civ.GERMANY: 20,
        Civ.NOVGOROD: 60,
        Civ.NORWAY: 60,
        Civ.KIEV: 40,
        Civ.HUNGARY: 60,
        Civ.CASTILLE: 20,
        Civ.DENMARK: 60,
        Civ.SCOTLAND: 40,
        Civ.POLAND: 80,
        Civ.GENOA: 20,
        Civ.MOROCCO: 60,
        Civ.ENGLAND: 40,
        Civ.PORTUGAL: 40,
        Civ.ARAGON: 60,
        Civ.SWEDEN: 60,
        Civ.PRUSSIA: 20,
        Civ.LITHUANIA: 80,
        Civ.AUSTRIA: 20,
        Civ.OTTOMAN: 80,
        Civ.MOSCOW: 40,
        Civ.DUTCH: 40,
        Civ.POPE: 20,
        Civ.INDEPENDENT: 100,
        Civ.INDEPENDENT_2: 100,
        Civ.INDEPENDENT_3: 100,
        Civ.INDEPENDENT_4: 100,
        Civ.BARBARIAN: 100,
    }
)

CIV_LEADERS = CivDataMapper(
    {
        Civ.BYZANTIUM: {
            LeaderType.PRIMARY: Leader.JUSTINIAN,
            LeaderType.EARLY: Leader.JUSTINIAN,
            LeaderType.LATE: [
                (Leader.BASIL_II, DateTurn.i910AD),
                (Leader.PALAIOLOGOS, DateTurn.i1230AD),
            ],
        },
        Civ.FRANCE: {
            LeaderType.PRIMARY: Leader.CHARLEMAGNE,
            LeaderType.EARLY: Leader.CHARLEMAGNE,
            LeaderType.LATE: [
                (Leader.PHILIP_AUGUSTUS, DateTurn.i1101AD),
                (Leader.JOAN, DateTurn.i1376AD),
                (Leader.LOUIS_XIV, DateTurn.i1523AD),
            ],
        },
        Civ.ARABIA: {
            LeaderType.PRIMARY: Leader.ABU_BAKR,
            LeaderType.EARLY: Leader.ABU_BAKR,
            LeaderType.LATE: [
                (Leader.HARUN_AL_RASHID, DateTurn.i752AD),
                (Leader.SALADIN, DateTurn.i1160AD),
            ],
        },
        Civ.BULGARIA: {
            LeaderType.PRIMARY: Leader.SIMEON,
            LeaderType.EARLY: Leader.SIMEON,
            LeaderType.LATE: [
                (Leader.IVAN_ASEN, DateTurn.i1101AD),
            ],
        },
        Civ.CORDOBA: {
            LeaderType.PRIMARY: Leader.ABD_AR_RAHMAN,
            LeaderType.EARLY: Leader.ABD_AR_RAHMAN,
            LeaderType.LATE: [
                (Leader.MOHAMMED_IBN_NASR, DateTurn.i1202AD),
            ],
        },
        Civ.VENECIA: {
            LeaderType.PRIMARY: Leader.ENRICO_DANDOLO,
            LeaderType.EARLY: Leader.ENRICO_DANDOLO,
            LeaderType.LATE: [
                (Leader.ANDREA_GRITTI, DateTurn.i1259AD),
            ],
        },
        Civ.BURGUNDY: {
            LeaderType.PRIMARY: Leader.OTTO_WILLIAM,
            LeaderType.EARLY: Leader.OTTO_WILLIAM,
            LeaderType.LATE: [
                (Leader.BEATRICE, DateTurn.i1200AD),
                (Leader.PHILIP_THE_BOLD, DateTurn.i1356AD),
            ],
        },
        Civ.GERMANY: {
            LeaderType.PRIMARY: Leader.OTTO_I,
            LeaderType.EARLY: Leader.OTTO_I,
            LeaderType.LATE: [
                (Leader.BARBAROSSA, DateTurn.i1139AD),
            ],
        },
        Civ.NOVGOROD: {
            LeaderType.PRIMARY: Leader.RURIK,
            LeaderType.EARLY: Leader.RURIK,
            LeaderType.LATE: [
                (Leader.ALEXANDER_NEVSKY, DateTurn.i1150AD),
                (Leader.MARFA, DateTurn.i1380AD),
            ],
        },
        Civ.NORWAY: {
            LeaderType.PRIMARY: Leader.HARALD_HARDRADA,
            LeaderType.EARLY: Leader.HARALD_HARDRADA,
            LeaderType.LATE: [
                (Leader.HAAKON_IV, DateTurn.i1160AD),
            ],
        },
        Civ.KIEV: {
            LeaderType.PRIMARY: Leader.YAROSLAV,
            LeaderType.EARLY: Leader.YAROSLAV,
            LeaderType.LATE: [
                (Leader.MSTISLAV, DateTurn.i1101AD),
                (Leader.BOHDAN_KHMELNYTSKY, DateTurn.i1520AD),
            ],
        },
        Civ.HUNGARY: {
            LeaderType.PRIMARY: Leader.STEPHEN,
            LeaderType.EARLY: Leader.STEPHEN,
            LeaderType.LATE: [
                (Leader.BELA_III, DateTurn.i1167AD),
                (Leader.MATTHIAS, DateTurn.i1444AD),
            ],
        },
        Civ.CASTILLE: {
            LeaderType.PRIMARY: Leader.FERDINAND_III,
            LeaderType.EARLY: Leader.FERDINAND_III,
            LeaderType.LATE: [
                (Leader.ISABELLA, DateTurn.i1250AD),
                (Leader.PHILIP_II, DateTurn.i1520AD),
            ],
        },
        Civ.DENMARK: {
            LeaderType.PRIMARY: Leader.HARALD_BLUETOOTH,
            LeaderType.EARLY: Leader.HARALD_BLUETOOTH,
            LeaderType.LATE: [
                (Leader.MARGARET_I, DateTurn.i1320AD),
                (Leader.CHRISTIAN_IV, DateTurn.i1520AD),
            ],
        },
        Civ.SCOTLAND: {
            LeaderType.PRIMARY: Leader.ROBERT_THE_BRUCE,
            LeaderType.EARLY: Leader.ROBERT_THE_BRUCE,
            LeaderType.LATE: [
                (Leader.JAMES_IV, DateTurn.i1296AD),
            ],
        },
        Civ.POLAND: {
            LeaderType.PRIMARY: Leader.MIESZKO,
            LeaderType.EARLY: Leader.MIESZKO,
            LeaderType.LATE: [
                (Leader.CASIMIR, DateTurn.i1320AD),
                (Leader.SOBIESKI, DateTurn.i1570AD),
            ],
        },
        Civ.GENOA: {
            LeaderType.PRIMARY: Leader.EMBRIACO,
            LeaderType.EARLY: Leader.EMBRIACO,
            LeaderType.LATE: [
                (Leader.BOCCANEGRA, DateTurn.i1101AD),
            ],
        },
        Civ.MOROCCO: {
            LeaderType.PRIMARY: Leader.YAQUB_AL_MANSUR,
            LeaderType.EARLY: Leader.YAQUB_AL_MANSUR,
            LeaderType.LATE: [
                (Leader.ISMAIL_IBN_SHARIF, DateTurn.i1419AD),
            ],
        },
        Civ.ENGLAND: {
            LeaderType.PRIMARY: Leader.WILLIAM,
            LeaderType.EARLY: Leader.WILLIAM,
            LeaderType.LATE: [
                (Leader.ELIZABETH, DateTurn.i1452AD),
                (Leader.GEORGE_III, DateTurn.i1700AD),
            ],
        },
        Civ.PORTUGAL: {
            LeaderType.PRIMARY: Leader.AFONSO,
            LeaderType.EARLY: Leader.AFONSO,
            LeaderType.LATE: [
                (Leader.JOAO, DateTurn.i1419AD),
                (Leader.MARIA_I, DateTurn.i1700AD),
            ],
        },
        Civ.ARAGON: {
            LeaderType.PRIMARY: Leader.JAMES_I,
            LeaderType.EARLY: Leader.JAMES_I,
            LeaderType.LATE: [
                (Leader.JOHN_II, DateTurn.i1397AD),
            ],
        },
        Civ.SWEDEN: {
            LeaderType.PRIMARY: Leader.MAGNUS_LADULAS,
            LeaderType.EARLY: Leader.MAGNUS_LADULAS,
            LeaderType.LATE: [
                (Leader.GUSTAV_VASA, DateTurn.i1470AD),
                (Leader.GUSTAV_ADOLF, DateTurn.i1540AD),
                (Leader.KARL_XII, DateTurn.i1680AD),
            ],
        },
        Civ.PRUSSIA: {
            LeaderType.PRIMARY: Leader.HERMANN_VON_SALZA,
            LeaderType.EARLY: Leader.HERMANN_VON_SALZA,
            LeaderType.LATE: [
                (Leader.FREDERICK, DateTurn.i1580AD),
            ],
        },
        Civ.LITHUANIA: {
            LeaderType.PRIMARY: Leader.MINDAUGAS,
            LeaderType.EARLY: Leader.MINDAUGAS,
            LeaderType.LATE: [
                (Leader.VYTAUTAS, DateTurn.i1377AD),
            ],
        },
        Civ.AUSTRIA: {
            LeaderType.PRIMARY: Leader.MAXIMILIAN,
            LeaderType.EARLY: Leader.MAXIMILIAN,
            LeaderType.LATE: [
                (Leader.MARIA_THERESA, DateTurn.i1700AD),
            ],
        },
        Civ.OTTOMAN: {
            LeaderType.PRIMARY: Leader.MEHMED,
            LeaderType.EARLY: Leader.MEHMED,
            LeaderType.LATE: [
                (Leader.SULEIMAN, DateTurn.i1520AD),
            ],
        },
        Civ.MOSCOW: {
            LeaderType.PRIMARY: Leader.IVAN_IV,
            LeaderType.EARLY: Leader.IVAN_IV,
            LeaderType.LATE: [
                (Leader.PETER, DateTurn.i1570AD),
                (Leader.CATHERINE, DateTurn.i1700AD),
            ],
        },
        Civ.DUTCH: {
            LeaderType.PRIMARY: Leader.WILLEM_VAN_ORANJE,
            LeaderType.EARLY: Leader.WILLEM_VAN_ORANJE,
            LeaderType.LATE: [
                (Leader.JOHAN_DE_WITT, DateTurn.i1650AD),
            ],
        },
        Civ.POPE: {
            LeaderType.PRIMARY: Leader.THE_POPE,
            LeaderType.EARLY: Leader.THE_POPE,
            LeaderType.LATE: None,
        },
    }
).fill_missing_members(None)
