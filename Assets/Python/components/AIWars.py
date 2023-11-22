# Rhye's and Fall of Civilization: Europe - AI Wars

from CvPythonExtensions import *
from CoreData import civilizations, civilization
from CoreFunctions import get_civ_by_id
from CoreTypes import Civ
from PyUtils import rand
import RFCUtils
from Scenario import get_scenario_start_turn
from StoredData import data
from WarMapData import WARS_MAP
from CoreStructures import WORLD_HEIGHT
from TimelineData import DateTurn

# globals
gc = CyGlobalContext()
utils = RFCUtils.RFCUtils()

### Constants ###

iMinIntervalEarly = 15
iMaxIntervalEarly = 30
iMinIntervalLate = 40
iMaxIntervalLate = 60
iThreshold = 100
iMinValue = 30


class AIWars:
    def getAttackingCivsArray(self, iCiv):
        return data.lAttackingCivsArray[iCiv]

    def setAttackingCivsArray(self, iCiv, iNewValue):
        data.lAttackingCivsArray[iCiv] = iNewValue

    def getNextTurnAIWar(self):
        return data.iNextTurnAIWar

    def setNextTurnAIWar(self, iNewValue):
        data.iNextTurnAIWar = iNewValue

    def setup(self):
        iTurn = get_scenario_start_turn()  # only check from the start turn of the scenario
        self.setNextTurnAIWar(iTurn + rand(iMaxIntervalEarly - iMinIntervalEarly))

    def checkTurn(self, iGameTurn):

        if iGameTurn > 20:
            # Absinthe: automatically turn peace on between independent cities and all the major civs
            if iGameTurn % 20 == 4:
                utils.restorePeaceHuman(Civ.INDEPENDENT_2.value)
            elif iGameTurn % 20 == 9:
                utils.restorePeaceHuman(Civ.INDEPENDENT.value)
            elif iGameTurn % 20 == 14:
                utils.restorePeaceHuman(Civ.INDEPENDENT_3.value)
            elif iGameTurn % 20 == 19:
                utils.restorePeaceHuman(Civ.INDEPENDENT_4.value)

            if iGameTurn % 36 == 0:
                utils.restorePeaceAI(Civ.INDEPENDENT.value, False)
            elif iGameTurn % 36 == 9:
                utils.restorePeaceAI(Civ.INDEPENDENT_2.value, False)
            elif iGameTurn % 36 == 18:
                utils.restorePeaceAI(Civ.INDEPENDENT_3.value, False)
            elif iGameTurn % 36 == 27:
                utils.restorePeaceAI(Civ.INDEPENDENT_4.value, False)

            # Absinthe: automatically turn war on between independent cities and some AI major civs
            elif iGameTurn % 36 == 2:  # on the 2nd turn after restorePeaceAI()
                utils.minorWars(Civ.INDEPENDENT.value, iGameTurn)
            elif iGameTurn % 36 == 11:  # on the 2nd turn after restorePeaceAI()
                utils.minorWars(Civ.INDEPENDENT_2.value, iGameTurn)
            elif iGameTurn % 36 == 20:  # on the 2nd turn after restorePeaceAI()
                utils.minorWars(Civ.INDEPENDENT_3.value, iGameTurn)
            elif iGameTurn % 36 == 29:  # on the 2nd turn after restorePeaceAI()
                utils.minorWars(Civ.INDEPENDENT_4.value, iGameTurn)

            # Absinthe: declare war sooner / more frequently if there is an Indy city inside the core area
            # 			so the AI will declare war much sooner after an indy city appeared in it's core
            if iGameTurn % 12 == 1:
                utils.minorCoreWars(Civ.INDEPENDENT_4.value, iGameTurn)
            elif iGameTurn % 12 == 4:
                utils.minorCoreWars(Civ.INDEPENDENT_3.value, iGameTurn)
            elif iGameTurn % 12 == 7:
                utils.minorCoreWars(Civ.INDEPENDENT_2.value, iGameTurn)
            elif iGameTurn % 12 == 10:
                utils.minorCoreWars(Civ.INDEPENDENT.value, iGameTurn)

        # Absinthe: Venice always seeks war with an Independent Ragusa - should help AI Venice significantly
        if iGameTurn % 9 == 2:
            pVenice = gc.getPlayer(Civ.VENECIA.value)
            if pVenice.isAlive() and not pVenice.isHuman():
                pRagusaPlot = gc.getMap().plot(64, 28)
                if pRagusaPlot.isCity():
                    pRagusaCity = pRagusaPlot.getPlotCity()
                    iOwner = pRagusaCity.getOwner()
                    if utils.isIndep(iOwner):
                        # Absinthe: probably better to use declareWar instead of setAtWar
                        teamVenice = gc.getTeam(pVenice.getTeam())
                        teamVenice.declareWar(iOwner, False, WarPlanTypes.WARPLAN_LIMITED)

        # Absinthe: Kingdom of Hungary should try to dominate Sisak/Zagreb if it's independent
        if iGameTurn > DateTurn.i1000AD and iGameTurn % 7 == 3:
            pHungary = gc.getPlayer(Civ.HUNGARY.value)
            if pHungary.isAlive() and not pHungary.isHuman():
                pZagrebPlot = gc.getMap().plot(62, 34)
                if pZagrebPlot.isCity():
                    pZagrebCity = pZagrebPlot.getPlotCity()
                    iOwner = pZagrebCity.getOwner()
                    if utils.isIndep(iOwner):
                        # Absinthe: probably better to use declareWar instead of setAtWar
                        teamHungary = gc.getTeam(pHungary.getTeam())
                        teamHungary.declareWar(iOwner, False, WarPlanTypes.WARPLAN_LIMITED)

        if iGameTurn == self.getNextTurnAIWar():
            iMinInterval = iMinIntervalEarly
            iMaxInterval = iMaxIntervalEarly

            # skip if already in a world war
            iCiv, iTargetCiv = self.pickCivs()
            if 0 <= iTargetCiv <= civilizations().drop(Civ.BARBARIAN).len():
                if iTargetCiv != Civ.POPE.value and iCiv != Civ.POPE.value and iCiv != iTargetCiv:
                    self.initWar(iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval)
                    return
            self.setNextTurnAIWar(iGameTurn + iMinInterval + rand(iMaxInterval - iMinInterval))

    def pickCivs(self):
        iCiv = -1
        iTargetCiv = -1
        iCiv = self.chooseAttackingPlayer()
        if 0 <= iCiv <= civilizations().majors().len():
            iTargetCiv = self.checkGrid(iCiv)
            return (iCiv, iTargetCiv)
        else:
            return (-1, -1)

    def initWar(self, iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval):
        # Absinthe: don't declare if couldn't do it otherwise
        teamAgressor = gc.getTeam(gc.getPlayer(iCiv).getTeam())
        if teamAgressor.canDeclareWar(iTargetCiv):
            gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iTargetCiv, True, -1)
            self.setNextTurnAIWar(iGameTurn + iMinInterval + rand(iMaxInterval - iMinInterval))
        # Absinthe: if not, next try will come the 1/2 of this time later
        else:
            self.setNextTurnAIWar(
                iGameTurn + (iMinInterval + rand(iMaxInterval - iMinInterval) / 2)
            )

    def chooseAttackingPlayer(self):
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
                        utils.getPlagueCountdown(iLoopCiv) >= -10
                        and utils.getPlagueCountdown(iLoopCiv) <= 0
                    ):  # civ is not under plague or quit recently from it
                        iAlreadyAttacked = self.getAttackingCivsArray(iLoopCiv)
                        if utils.isAVassal(iLoopCiv):
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
                self.setAttackingCivsArray(iCiv, iAlreadyAttacked + 1)
                return iCiv
            else:
                return -1
        return -1

    def checkGrid(self, iCiv):
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

        for (i, j) in utils.getWorldPlotsList():
            iOwner = gc.getMap().plot(i, j).getOwner()
            if 0 <= iOwner < civilizations().drop(Civ.BARBARIAN).len() and iOwner != iCiv:
                if lTargetCivs[iOwner] > 0:
                    iValue = WARS_MAP[get_civ_by_id(iCiv)][WORLD_HEIGHT - 1 - j][i]
                    if iOwner in [
                        Civ.INDEPENDENT.value,
                        Civ.INDEPENDENT_2.value,
                        Civ.INDEPENDENT_3.value,
                        Civ.INDEPENDENT_4.value,
                    ]:
                        iValue /= 3
                    lTargetCivs[iOwner] += iValue

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
                utils.getPlagueCountdown(iLoopCiv) > 0
                or utils.getPlagueCountdown(iLoopCiv) < -10
                and not gc.getGame().getGameTurn() <= civilization(iLoopCiv).date.birth + 20
            ):
                lTargetCivs[iLoopCiv] *= 3
                lTargetCivs[iLoopCiv] /= 2

            # balanced with master's attitude
            iMaster = utils.getMaster(iCiv)
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

    def forgetMemory(self, iTech, iPlayer):
        pass
