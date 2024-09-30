from CvPythonExtensions import CyGlobalContext
from CivilizationsData import TECH_STARTERS_1200AD
from Core import (
    civilization,
    civilizations,
    human,
    make_unit,
    make_units,
    team,
    teamtype,
    year,
    plots,
)
from CoreTypes import Area, Civ, InitialCondition, Technology, Unit
from LocationsData import CIV_CAPITAL_LOCATIONS
from MiscData import REVEAL_DATE_TECHNOLOGY
from RFCUtils import change_attitude_extra_between_civ
from Events import handler
from TimelineData import TIMELINE_TECH_MODIFIER

gc = CyGlobalContext()


@handler("GameStart")
def setup():
    set_starting_turns()
    set_tech_timeline_date()


def set_starting_turns():
    for civ in civilizations().drop(Civ.BARBARIAN):
        civ.player.setInitialBirthTurn(civ.date.birth)


def set_tech_timeline_date():
    for tech, turn in TIMELINE_TECH_MODIFIER:
        gc.setTimelineTechDateForTech(tech, year(turn))


def set_starting_gold():
    for civ in civilizations():
        condition = civ.scenario.get("condition")
        if condition is not None:
            civ.player.changeGold(condition[InitialCondition.GOLD])


def set_starting_faith():
    for civ in civilizations():
        condition = civ.scenario.get("condition")
        if condition is not None:
            civ.player.setFaith(condition[InitialCondition.FAITH])


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
        tStart = CIV_CAPITAL_LOCATIONS[iHuman]

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
    change_attitude_extra_between_civ(Civ.BYZANTIUM, Civ.ARABIA, -2)
    change_attitude_extra_between_civ(Civ.SCOTLAND, Civ.FRANCE, 4)


def set_initial_contacts(iCiv, bMeet=True):
    civ = team(iCiv)
    contacts = civilization(iCiv).scenario.get("contact")
    if contacts is not None:
        for contact in contacts:
            other = civilization(contact)
            if other.is_alive() and not civ.isHasMet(other.teamtype):
                civ.meet(other.teamtype, bMeet)


def reveal_rectangle(iCiv, area):
    for plot in plots.rectangle(area[Area.TILE_MIN], area[Area.TILE_MAX]).entities():
        plot.setRevealed(teamtype(iCiv), True, False, -1)


def reveal_areas(iCiv):
    for area in civilization(iCiv).location.visible_area:
        reveal_rectangle(iCiv, area)


def has_date_revealed(identifier=None):
    if team(identifier).isHasTech(REVEAL_DATE_TECHNOLOGY):
        return True
    return False
