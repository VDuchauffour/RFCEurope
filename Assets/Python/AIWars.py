from CvPythonExtensions import *
from Consts import INDEPENDENT_CIVS
from Core import (
    civilization,
    civilizations,
    get_data_from_upside_down_map,
    get_scenario_start_turn,
    is_independent_civ,
    is_major_civ,
    turn,
    year,
    plots,
)
from CoreTypes import Civ
from PyUtils import rand
from RFCUtils import (
    getMaster,
    getPlagueCountdown,
    isAVassal,
    minorCoreWars,
    minorWars,
    restorePeaceAI,
    restorePeaceHuman,
)
from StoredData import data
from WarMapData import WARS_MAP
from Events import handler

gc = CyGlobalContext()

iMinIntervalEarly = 15
iMaxIntervalEarly = 30
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30


@handler("GameStart")
def setup():
    iTurn = get_scenario_start_turn()  # only check from the start turn of the scenario
    data.iNextTurnAIWar = iTurn + rand(iMaxIntervalEarly - iMinIntervalEarly)


def getAttackingCivsArray(iCiv):
    return data.lAttackingCivsArray[iCiv]


def setAttackingCivsArray(iCiv, iNewValue):
    data.lAttackingCivsArray[iCiv] = iNewValue


def checkTurn(iGameTurn):
    if iGameTurn > 20:
        # Absinthe: automatically turn peace on between independent cities and all the major civs
        turn_peace_human_mapper = {
            Civ.INDEPENDENT: 9,
            Civ.INDEPENDENT_2: 4,
            Civ.INDEPENDENT_3: 14,
            Civ.INDEPENDENT_4: 19,
        }
        for civ, value in turn_peace_human_mapper.items():
            if iGameTurn % 20 == value:
                restorePeaceHuman(civ)

        turn_peace_ai_mapper = {
            Civ.INDEPENDENT: 0,
            Civ.INDEPENDENT_2: 9,
            Civ.INDEPENDENT_3: 18,
            Civ.INDEPENDENT_4: 27,
        }
        for civ, value in turn_peace_ai_mapper.items():
            if iGameTurn % 36 == value:
                restorePeaceAI(civ, False)

        # Absinthe: automatically turn war on between independent cities and some AI major civs
        # runned on the 2nd turn after restorePeaceAI()
        turn_minor_wars_mapper = {
            Civ.INDEPENDENT: 2,
            Civ.INDEPENDENT_2: 11,
            Civ.INDEPENDENT_3: 20,
            Civ.INDEPENDENT_4: 29,
        }
        for civ, value in turn_minor_wars_mapper.items():
            if iGameTurn % 36 == value:
                minorWars(civ, iGameTurn)

        # Absinthe: declare war sooner / more frequently if there is an Indy city inside the core area
        # so the AI will declare war much sooner after an indy city appeared in it's core
        turn_minor_core_wars_mapper = {
            Civ.INDEPENDENT: 10,
            Civ.INDEPENDENT_2: 7,
            Civ.INDEPENDENT_3: 4,
            Civ.INDEPENDENT_4: 1,
        }
        for civ, value in turn_minor_core_wars_mapper.items():
            if iGameTurn % 12 == value:
                minorCoreWars(civ, iGameTurn)

    # Absinthe: Venice always seeks war with an Independent Ragusa - should help AI Venice significantly
    if iGameTurn % 9 == 2:
        pVenice = gc.getPlayer(Civ.VENECIA)
        if pVenice.isAlive() and not pVenice.isHuman():
            pRagusaPlot = gc.getMap().plot(64, 28)
            if pRagusaPlot.isCity():
                pRagusaCity = pRagusaPlot.getPlotCity()
                iOwner = pRagusaCity.getOwner()
                if is_independent_civ(iOwner):
                    # Absinthe: probably better to use declareWar instead of setAtWar
                    teamVenice = gc.getTeam(pVenice.getTeam())
                    teamVenice.declareWar(iOwner, False, WarPlanTypes.WARPLAN_LIMITED)

    # Absinthe: Kingdom of Hungary should try to dominate Sisak/Zagreb if it's independent
    if iGameTurn > year(1000) and iGameTurn % 7 == 3:
        pHungary = gc.getPlayer(Civ.HUNGARY)
        if pHungary.isAlive() and not pHungary.isHuman():
            pZagrebPlot = gc.getMap().plot(62, 34)
            if pZagrebPlot.isCity():
                pZagrebCity = pZagrebPlot.getPlotCity()
                iOwner = pZagrebCity.getOwner()
                if is_independent_civ(iOwner):
                    # Absinthe: probably better to use declareWar instead of setAtWar
                    teamHungary = gc.getTeam(pHungary.getTeam())
                    teamHungary.declareWar(iOwner, False, WarPlanTypes.WARPLAN_LIMITED)

    if iGameTurn == data.iNextTurnAIWar:
        iMinInterval = iMinIntervalEarly
        iMaxInterval = iMaxIntervalEarly

        # skip if already in a world war
        iCiv, iTargetCiv = pickCivs()
        if 0 <= iTargetCiv <= civilizations().drop(Civ.BARBARIAN).len():
            if iTargetCiv != Civ.POPE and iCiv != Civ.POPE and iCiv != iTargetCiv:
                initWar(iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval)
                return
        data.iNextTurnAIWar = iGameTurn + iMinInterval + rand(iMaxInterval - iMinInterval)


def pickCivs():
    iCiv = chooseAttackingPlayer()
    if iCiv != -1:
        if is_major_civ(iCiv):
            iTargetCiv = checkGrid(iCiv)
            return (iCiv, iTargetCiv)
    else:
        return (-1, -1)


def initWar(iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval):
    # Absinthe: don't declare if couldn't do it otherwise
    teamAgressor = gc.getTeam(gc.getPlayer(iCiv).getTeam())
    if teamAgressor.canDeclareWar(iTargetCiv):
        gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iTargetCiv, True, -1)
        data.iNextTurnAIWar = iGameTurn + iMinInterval + rand(iMaxInterval - iMinInterval)
    # Absinthe: if not, next try will come the 1/2 of this time later
    else:
        data.iNextTurnAIWar = iGameTurn + (iMinInterval + rand(iMaxInterval - iMinInterval) / 2)


def chooseAttackingPlayer():
    # finding max teams ever alive (countCivTeamsEverAlive() doesn't work as late human starting civ gets killed every turn)
    iMaxCivs = civilizations().majors().len()
    for i in civilizations().majors().ids():
        j = civilizations().main().len() - i
        if gc.getPlayer(j).isAlive():
            iMaxCivs = j
            break

    if gc.getGame().countCivPlayersAlive() <= 2:
        return -1
    else:
        iRndnum = rand(iMaxCivs)
        iAlreadyAttacked = -100
        iMin = 100
        iCiv = -1
        for i in range(iRndnum, iRndnum + iMaxCivs):
            iLoopCiv = i % iMaxCivs
            if gc.getPlayer(iLoopCiv).isAlive() and not gc.getPlayer(iLoopCiv).isHuman():
                if (
                    getPlagueCountdown(iLoopCiv) >= -10 and getPlagueCountdown(iLoopCiv) <= 0
                ):  # civ is not under plague or quit recently from it
                    iAlreadyAttacked = getAttackingCivsArray(iLoopCiv)
                    if isAVassal(iLoopCiv):
                        iAlreadyAttacked += 1  # less likely to attack
                    # check if a world war is already in place:
                    iNumAlreadyWar = 0
                    tLoopCiv = gc.getTeam(gc.getPlayer(iLoopCiv).getTeam())
                    for kLoopCiv in civilizations().majors().ids():
                        if tLoopCiv.isAtWar(kLoopCiv):
                            iNumAlreadyWar += 1
                    if iNumAlreadyWar >= 4:
                        iAlreadyAttacked += 2  # much less likely to attack
                    elif iNumAlreadyWar >= 2:
                        iAlreadyAttacked += 1  # less likely to attack

                    if iAlreadyAttacked < iMin:
                        iMin = iAlreadyAttacked
                        iCiv = iLoopCiv
        if iAlreadyAttacked != -100:
            setAttackingCivsArray(iCiv, iAlreadyAttacked + 1)
            return iCiv
        else:
            return -1


def checkGrid(iCiv):
    pCiv = gc.getPlayer(iCiv)
    pTeam = gc.getTeam(pCiv.getTeam())
    lTargetCivs = [0] * civilizations().drop(Civ.BARBARIAN).len()

    # set alive civs to 1 to differentiate them from dead civs
    for iLoopPlayer in civilizations().drop(Civ.BARBARIAN).ids():
        if iLoopPlayer == iCiv:
            continue
        if pTeam.isAtWar(iLoopPlayer):  # if already at war with iCiv then it remains 0
            continue
        pLoopPlayer = gc.getPlayer(iLoopPlayer)
        iLoopTeam = pLoopPlayer.getTeam()
        pLoopTeam = gc.getTeam(iLoopTeam)
        if (
            iLoopPlayer < civilizations().majors().len()
        ):  # if master or vassal of iCiv then it remains 0
            if pLoopTeam.isVassal(iCiv) or pTeam.isVassal(iLoopPlayer):
                continue
        if pLoopPlayer.isAlive() and pTeam.isHasMet(iLoopTeam):
            lTargetCivs[iLoopPlayer] = 1

    for plot in plots().all().not_owner(iCiv).not_owner(Civ.BARBARIAN).entities():
        if lTargetCivs[plot.getOwner()] > 0:
            iValue = get_data_from_upside_down_map(WARS_MAP, iCiv, plot)
            if plot.getOwner() in INDEPENDENT_CIVS:
                iValue /= 3
            lTargetCivs[plot.getOwner()] += iValue

    # normalization
    iMaxTempValue = max(lTargetCivs)
    if iMaxTempValue > 0:
        for civ in civilizations().drop(Civ.BARBARIAN).ids():
            if lTargetCivs[civ] > 0:
                lTargetCivs[civ] = lTargetCivs[civ] * 500 / iMaxTempValue

    for iLoopCiv in civilizations().drop(Civ.BARBARIAN).ids():
        if iLoopCiv == iCiv:
            continue

        if lTargetCivs[iLoopCiv] <= 0:
            continue

        # add a random value
        if lTargetCivs[iLoopCiv] <= iThreshold:
            lTargetCivs[iLoopCiv] += rand(100)
        else:
            lTargetCivs[iLoopCiv] += rand(300)
        # balanced with attitude
        attitude = 2 * (pCiv.AI_getAttitude(iLoopCiv) - 2)
        if attitude > 0:
            lTargetCivs[iLoopCiv] /= attitude
        # exploit plague
        if (
            getPlagueCountdown(iLoopCiv) > 0
            or getPlagueCountdown(iLoopCiv) < -10
            and not turn() <= civilization(iLoopCiv).date.birth + 20
        ):
            lTargetCivs[iLoopCiv] *= 3
            lTargetCivs[iLoopCiv] /= 2

        # balanced with master's attitude
        iMaster = getMaster(iCiv)
        if iMaster != -1:
            attitude = 2 * (gc.getPlayer(iMaster).AI_getAttitude(iLoopCiv) - 2)
            if attitude > 0:
                lTargetCivs[iLoopCiv] /= attitude

        # if already at war
        if not pTeam.isAtWar(iLoopCiv):
            # consider peace counter
            iCounter = min(7, max(1, pTeam.AI_getAtPeaceCounter(iLoopCiv)))
            if iCounter <= 7:
                lTargetCivs[iLoopCiv] *= 20 + 10 * iCounter
                lTargetCivs[iLoopCiv] /= 100

        # if under pact
        if pTeam.isDefensivePact(iLoopCiv):
            lTargetCivs[iLoopCiv] /= 4

    # find max
    iMaxValue = max(lTargetCivs)
    iTargetCiv = lTargetCivs.index(iMaxValue)

    if iMaxValue >= iMinValue:
        return iTargetCiv
    return -1
