# Rhye's and Fall of Civilization: Europe - AI Wars

from CvPythonExtensions import *
from CivilizationsData import CIVILIZATIONS
from CoreTypes import Civ
import PyHelpers  # LOQ
import XMLConsts as xml
import RFCUtils
import RFCEMaps
from StoredData import sd
from MiscData import WORLD_HEIGHT
from TimelineData import CIV_BIRTHDATE
from CoreStructures import get_civ_by_id

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer  # LOQ
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
        return sd.scriptDict["lAttackingCivsArray"][iCiv]

    def setAttackingCivsArray(self, iCiv, iNewValue):
        sd.scriptDict["lAttackingCivsArray"][iCiv] = iNewValue

    def getNextTurnAIWar(self):
        return sd.scriptDict["iNextTurnAIWar"]

    def setNextTurnAIWar(self, iNewValue):
        sd.scriptDict["iNextTurnAIWar"] = iNewValue

    def setup(self):
        iTurn = utils.getScenarioStartTurn()  # only check from the start turn of the scenario
        self.setNextTurnAIWar(
            iTurn
            + gc.getGame().getSorenRandNum(iMaxIntervalEarly - iMinIntervalEarly, "random turn")
        )

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
                        print("minorWars_Ragusa", "WARPLAN_LIMITED")
                        # teamVenice.setAtWar( gc.getPlayer( iOwner ).getTeam(), True )
                        # teamRagusa = gc.getTeam( gc.getPlayer( iOwner ).getTeam() )
                        # teamRagusa.setAtWar( pVenice.getTeam(), True )

        # Absinthe: Kingdom of Hungary should try to dominate Sisak/Zagreb if it's independent
        if iGameTurn > xml.i1000AD and iGameTurn % 7 == 3:
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
                        print("minorWars_Zagreb", "WARPLAN_LIMITED")

        if iGameTurn == self.getNextTurnAIWar():

            # 3Miro: how long it takes (the else from the statement goes all the way down)
            # if (iGameTurn > xml.i1600AD): #longer periods due to globalization of contacts
            # 	iMinInterval = iMinIntervalLate
            # 	iMaxInterval = iMaxIntervalLate
            # else:
            iMinInterval = iMinIntervalEarly
            iMaxInterval = iMaxIntervalEarly

            # skip if already in a world war
            # print ("AIWars iTargetCiv missing", iCiv)
            iCiv, iTargetCiv = self.pickCivs()
            print("AIWars chosen civs: iCiv, iTargetCiv", iCiv, iTargetCiv)
            if 0 <= iTargetCiv <= CIVILIZATIONS.drop(Civ.BARBARIAN).len():
                if iTargetCiv != Civ.POPE.value and iCiv != Civ.POPE.value and iCiv != iTargetCiv:
                    self.initWar(iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval)
                    return
            else:
                print("AIWars iTargetCiv missing again", iCiv)

            # make sure we don't miss this
            print("Skipping AIWar")
            self.setNextTurnAIWar(
                iGameTurn
                + iMinInterval
                + gc.getGame().getSorenRandNum(iMaxInterval - iMinInterval, "random turn")
            )

    def pickCivs(self):
        iCiv = -1
        iTargetCiv = -1
        iCiv = self.chooseAttackingPlayer()
        if 0 <= iCiv <= CIVILIZATIONS.majors().len():
            iTargetCiv = self.checkGrid(iCiv)
            return (iCiv, iTargetCiv)
        else:
            print("AIWars iCiv missing", iCiv)
            return (-1, -1)

    def initWar(self, iCiv, iTargetCiv, iGameTurn, iMaxInterval, iMinInterval):
        # Absinthe: don't declare if couldn't do it otherwise
        teamAgressor = gc.getTeam(gc.getPlayer(iCiv).getTeam())
        if teamAgressor.canDeclareWar(iTargetCiv):
            gc.getTeam(gc.getPlayer(iCiv).getTeam()).declareWar(iTargetCiv, True, -1)
            self.setNextTurnAIWar(
                iGameTurn
                + iMinInterval
                + gc.getGame().getSorenRandNum(iMaxInterval - iMinInterval, "random turn")
            )
            print("Setting AIWar", iCiv, "attacking", iTargetCiv)
        # Absinthe: if not, next try will come the 1/2 of this time later
        else:
            self.setNextTurnAIWar(
                iGameTurn
                + (
                    iMinInterval
                    + gc.getGame().getSorenRandNum(iMaxInterval - iMinInterval, "random turn") / 2
                )
            )
            print("No AIWar this time, but the next try will come sooner")

    ##	def initArray(self):
    ##		for k in CIVILIZATIONS.majors().ids():
    ##			grid = []
    ##			for j in range( WORLD_HEIGHT ):
    ##				line = []
    ##				for i in range( WORLD_WIDTH ):
    ##					line.append( gc.getPlayer(iCiv).getSettlersMaps( WORLD_HEIGHT-j-1, i ) )
    ##				grid.append( line )
    ##			self.lSettlersMap.append( grid )
    ##		print self.lSettlersMap

    def chooseAttackingPlayer(self):
        # finding max teams ever alive (countCivTeamsEverAlive() doesn't work as late human starting civ gets killed every turn)
        iMaxCivs = CIVILIZATIONS.majors().len()
        for i in CIVILIZATIONS.majors().ids():
            j = CIVILIZATIONS.main().len() - i
            if gc.getPlayer(j).isAlive():
                iMaxCivs = j
                break
        # print ("iMaxCivs", iMaxCivs)

        if gc.getGame().countCivPlayersAlive() <= 2:
            return -1
        else:
            iRndnum = gc.getGame().getSorenRandNum(iMaxCivs, "attacking civ index")
            # print ("iRndnum", iRndnum)
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
                        for kLoopCiv in CIVILIZATIONS.majors().ids():
                            if tLoopCiv.isAtWar(kLoopCiv):
                                iNumAlreadyWar += 1
                        if iNumAlreadyWar >= 4:
                            iAlreadyAttacked += 2  # much less likely to attack
                        elif iNumAlreadyWar >= 2:
                            iAlreadyAttacked += 1  # less likely to attack

                        if iAlreadyAttacked < iMin:
                            iMin = iAlreadyAttacked
                            iCiv = iLoopCiv
            # print ("attacking civ", iCiv)
            if iAlreadyAttacked != -100:
                self.setAttackingCivsArray(iCiv, iAlreadyAttacked + 1)
                return iCiv
            else:
                return -1
        return -1

    def checkGrid(self, iCiv):
        pCiv = gc.getPlayer(iCiv)
        pTeam = gc.getTeam(pCiv.getTeam())
        lTargetCivs = [0] * CIVILIZATIONS.drop(Civ.BARBARIAN).len()

        # set alive civs to 1 to differentiate them from dead civs
        for iLoopPlayer in CIVILIZATIONS.drop(Civ.BARBARIAN).ids():
            if iLoopPlayer == iCiv:
                continue
            if pTeam.isAtWar(iLoopPlayer):  # if already at war with iCiv then it remains 0
                continue
            pLoopPlayer = gc.getPlayer(iLoopPlayer)
            iLoopTeam = pLoopPlayer.getTeam()
            pLoopTeam = gc.getTeam(iLoopTeam)
            if (
                iLoopPlayer < CIVILIZATIONS.majors().len()
            ):  # if master or vassal of iCiv then it remains 0
                if pLoopTeam.isVassal(iCiv) or pTeam.isVassal(iLoopPlayer):
                    continue
            if pLoopPlayer.isAlive() and pTeam.isHasMet(iLoopTeam):
                lTargetCivs[iLoopPlayer] = 1

        for (i, j) in utils.getWorldPlotsList():
            iOwner = gc.getMap().plot(i, j).getOwner()
            if 0 <= iOwner < CIVILIZATIONS.drop(Civ.BARBARIAN).len() and iOwner != iCiv:
                if lTargetCivs[iOwner] > 0:
                    iValue = RFCEMaps.tWarsMaps[iCiv][WORLD_HEIGHT - 1 - j][i]
                    if iOwner in [
                        Civ.INDEPENDENT.value,
                        Civ.INDEPENDENT_2.value,
                        Civ.INDEPENDENT_3.value,
                        Civ.INDEPENDENT_4.value,
                    ]:
                        iValue /= 3
                    lTargetCivs[iOwner] += iValue

        # contacts do not disappear in RFCE, so if isHasMet was True they do have a contact
        # for k in CIVILIZATIONS.majors().ids():
        # 	if not pCiv.canContact(k):
        # 		lTargetCivs[k] /= 8

        # print(lTargetCivs)

        # normalization
        iMaxTempValue = max(lTargetCivs)
        # print(iMaxTempValue)
        if iMaxTempValue > 0:
            for civ in CIVILIZATIONS.drop(Civ.BARBARIAN).ids():
                if lTargetCivs[civ] > 0:
                    lTargetCivs[civ] = lTargetCivs[civ] * 500 / iMaxTempValue

        # print(lTargetCivs)

        for iLoopCiv in CIVILIZATIONS.drop(Civ.BARBARIAN).ids():
            if iLoopCiv == iCiv:
                continue

            if lTargetCivs[iLoopCiv] <= 0:
                continue

            # add a random value
            if lTargetCivs[iLoopCiv] <= iThreshold:
                lTargetCivs[iLoopCiv] += gc.getGame().getSorenRandNum(100, "random modifier")
            if lTargetCivs[iLoopCiv] > iThreshold:
                lTargetCivs[iLoopCiv] += gc.getGame().getSorenRandNum(300, "random modifier")
            # balanced with attitude
            attitude = 2 * (pCiv.AI_getAttitude(iLoopCiv) - 2)
            if attitude > 0:
                lTargetCivs[iLoopCiv] /= attitude
            # exploit plague
            if (
                utils.getPlagueCountdown(iLoopCiv) > 0
                or utils.getPlagueCountdown(iLoopCiv) < -10
                and not gc.getGame().getGameTurn() <= CIV_BIRTHDATE[get_civ_by_id(iLoopCiv)] + 20
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
            # if friend of a friend
        ##			for jLoopCiv in CIVILIZATIONS.drop(Civ.BARBARIAN).ids():
        ##				if (pTeam.isDefensivePact(jLoopCiv) and gc.getTeam(gc.getPlayer(iLoopCiv).getTeam()).isDefensivePact(jLoopCiv)):
        ##					lTargetCivs[iLoopCiv] /= 2

        # print(lTargetCivs)

        # find max
        iMaxValue = max(lTargetCivs)
        iTargetCiv = lTargetCivs.index(iMaxValue)

        # print ("maxvalue", iMaxValue)
        # print("target civ", iTargetCiv)

        if iMaxValue >= iMinValue:
            return iTargetCiv
        return -1

    def forgetMemory(self, iTech, iPlayer):
        pass
