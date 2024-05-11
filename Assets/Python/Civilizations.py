from CvPythonExtensions import CyGlobalContext
from CivilizationsData import TECH_STARTERS_1200AD
from CoreData import civilization, civilizations
from CoreFunctions import get_civ_by_id
from CoreStructures import human, make_unit, make_units, year
from CoreTypes import Civ, Technology, Unit
from LocationsData import CIV_CAPITAL_LOCATIONS
from RFCUtils import change_attitude_extra_between_civ

gc = CyGlobalContext()


def setup():
    init_player_births()


def init_player_births():
    for civ in civilizations().drop(Civ.BARBARIAN):
        gc.setStartingTurn(civ.id, civ.date.birth)


def set_starting_gold():
    for civ in civilizations():
        condition = civ.scenario.get("condition")
        if condition is not None:
            civ.player.changeGold(condition.gold)


def set_starting_faith():
    for civ in civilizations():
        condition = civ.scenario.get("condition")
        if condition is not None:
            civ.player.setFaith(condition.faith)


def create_starting_workers(iCiv, tPlot):
    make_units(iCiv, Unit.WORKER, tPlot, civilization(iCiv).initial.workers)


def create_starting_units_500AD():
    make_units(Civ.FRANCE, Unit.SETTLER, CIV_CAPITAL_LOCATIONS[Civ.FRANCE], 3)
    make_units(Civ.FRANCE, Unit.ARCHER, CIV_CAPITAL_LOCATIONS[Civ.FRANCE], 4)
    make_units(Civ.FRANCE, Unit.AXEMAN, CIV_CAPITAL_LOCATIONS[Civ.FRANCE], 5)
    make_unit(Civ.FRANCE, Unit.SCOUT, CIV_CAPITAL_LOCATIONS[Civ.FRANCE])
    make_units(Civ.FRANCE, Unit.WORKER, CIV_CAPITAL_LOCATIONS[Civ.FRANCE], 2)
    make_units(Civ.FRANCE, Unit.CATHOLIC_MISSIONARY, CIV_CAPITAL_LOCATIONS[Civ.FRANCE], 2)

    iHuman = human()
    if civilization(iHuman).date.birth > year(500):
        # so everyone apart from Byzantium and France
        tStart = CIV_CAPITAL_LOCATIONS[get_civ_by_id(iHuman)]

        # Absinthe: changes in the unit positions, in order to prohibit these contacts in 500AD
        if iHuman == Civ.ARABIA:  # contact with Byzantium
            tStart = (
                CIV_CAPITAL_LOCATIONS[Civ.ARABIA][0],
                CIV_CAPITAL_LOCATIONS[Civ.ARABIA][1] - 10,
            )
        elif iHuman == Civ.BULGARIA:  # contact with Byzantium
            tStart = (
                CIV_CAPITAL_LOCATIONS[Civ.BULGARIA][0],
                CIV_CAPITAL_LOCATIONS[Civ.BULGARIA][1] + 1,
            )
        elif iHuman == Civ.OTTOMAN:  # contact with Byzantium
            tStart = (97, 23)

        make_unit(iHuman, Unit.SETTLER, tStart)
        make_unit(iHuman, Unit.SPEARMAN, tStart)


def create_starting_units_1200AD():
    iHuman = human()
    if civilization(iHuman).date.birth > year(1200):
        # so iSweden, iPrussia, iLithuania, iAustria, iTurkey, iMoscow, iDutch
        tStart = civilization(iHuman).location.capital

        # Absinthe: changes in the unit positions, in order to prohibit these contacts in 1200AD
        if iHuman == Civ.SWEDEN:  # contact with Denmark
            tStart = (
                CIV_CAPITAL_LOCATIONS[Civ.SWEDEN][0] - 2,
                CIV_CAPITAL_LOCATIONS[Civ.SWEDEN][1] + 2,
            )
        elif iHuman == Civ.PRUSSIA:  # contact with Poland
            tStart = (
                CIV_CAPITAL_LOCATIONS[Civ.PRUSSIA][0] + 1,
                CIV_CAPITAL_LOCATIONS[Civ.PRUSSIA][1] + 1,
            )
        elif iHuman == Civ.LITHUANIA:  # contact with Kiev
            tStart = (
                CIV_CAPITAL_LOCATIONS[Civ.LITHUANIA][0] - 2,
                CIV_CAPITAL_LOCATIONS[Civ.LITHUANIA][1],
            )
        elif iHuman == Civ.AUSTRIA:  # contact with Germany and Hungary
            tStart = (
                CIV_CAPITAL_LOCATIONS[Civ.AUSTRIA][0] - 3,
                CIV_CAPITAL_LOCATIONS[Civ.AUSTRIA][1] - 1,
            )
        elif iHuman == Civ.OTTOMAN:  # contact with Byzantium
            tStart = (98, 18)

        make_unit(iHuman, Unit.SETTLER, tStart)
        make_unit(iHuman, Unit.MACEMAN, tStart)


def set_starting_techs(iCiv):
    civ = civilization(iCiv)
    techs = civ.initial.get("tech")
    if techs is not None:
        for tech in techs:
            civ.add_tech(tech)


def set_starting_techs_1200AD(iCiv):
    # As a temporary solution, everyone gets Aragon's starting techs
    civ = civilization(iCiv)
    for tech in TECH_STARTERS_1200AD:
        civ.add_tech(tech)

    if iCiv in [Civ.ARABIA, Civ.MOROCCO]:
        civ.add_tech(Technology.ARABIC_KNOWLEDGE)


def set_starting_diplomacy_1200AD():
    change_attitude_extra_between_civ(Civ.BYZANTIUM.value, Civ.ARABIA.value, -2)
    change_attitude_extra_between_civ(Civ.SCOTLAND.value, Civ.FRANCE.value, 4)
