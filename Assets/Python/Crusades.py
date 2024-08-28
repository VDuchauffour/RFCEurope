from CvPythonExtensions import *
from Consts import MessageData
from Core import (
    civilization,
    civilizations,
    event_popup,
    human,
    location,
    make_crusade_unit,
    make_crusade_units,
    message_if_human,
    player,
    team,
    teamtype,
    message,
    text,
    turn,
    year,
    cities,
    plots,
    units,
)
from Events import handler
from PyUtils import percentage, percentage_chance, rand, choice
from ProvinceMapData import PROVINCES_MAP
from CityNameManager import lookupName
from RFCUtils import convertPlotCulture, getMaster, getUniqueUnit, isAVassal
from StoredData import data
import random

from CoreTypes import City, Civ, Religion, Promotion, Technology, Unit, Province
from MiscData import NUM_CRUSADES
from LocationsData import CITIES

gc = CyGlobalContext()


# Can call defensive crusade to aid Catholics, if at war with Non-Catholic and Non-Orthodox player, who isn't vassal of Catholic or Orthodox player and has at least one city in the provinces listed here
tDefensiveCrusadeMap = [
    [],  # Byzantium
    [
        Province.ILE_DE_FRANCE,
        Province.AQUITAINE,
        Province.ORLEANS,
        Province.CHAMPAGNE,
        Province.BRETAGNE,
        Province.NORMANDY,
        Province.PROVENCE,
        Province.FLANDERS,
        Province.BURGUNDY,
        Province.PICARDY,
    ],  # France
    [],  # Arabia
    [],  # Bulgaria
    [
        Province.LEON,
        Province.GALICIA,
        Province.LUSITANIA,
        Province.ARAGON,
        Province.CATALONIA,
        Province.NAVARRE,
        Province.CASTILE,
        Province.ANDALUSIA,
        Province.LA_MANCHA,
        Province.VALENCIA,
    ],  # Cordoba (for consistency)
    [
        Province.VERONA,
        Province.TUSCANY,
        Province.ARBERIA,
        Province.DALMATIA,
    ],  # Venecia
    [
        Province.FLANDERS,
        Province.PROVENCE,
        Province.BURGUNDY,
        Province.CHAMPAGNE,
        Province.LORRAINE,
        Province.PICARDY,
    ],  # Burgundy
    [
        Province.LORRAINE,
        Province.SWABIA,
        Province.BAVARIA,
        Province.SAXONY,
        Province.FRANCONIA,
        Province.FLANDERS,
        Province.BRANDENBURG,
        Province.HOLSTEIN,
        Province.BOHEMIA,
    ],  # Germany
    [],  # Novgorod
    [],  # Norway
    [],  # Kiev
    [
        Province.HUNGARY,
        Province.TRANSYLVANIA,
        Province.UPPER_HUNGARY,
        Province.WALLACHIA,
        Province.SLAVONIA,
        Province.PANNONIA,
        Province.AUSTRIA,
        Province.CARINTHIA,
        Province.SERBIA,
        Province.MOESIA,
        Province.BANAT,
        Province.BOSNIA,
        Province.DALMATIA,
    ],  # Hungary
    [
        Province.LEON,
        Province.GALICIA,
        Province.LUSITANIA,
        Province.ARAGON,
        Province.CATALONIA,
        Province.NAVARRE,
        Province.CASTILE,
        Province.ANDALUSIA,
        Province.LA_MANCHA,
        Province.VALENCIA,
    ],  # Spain
    [Province.ESTONIA],  # Denmark
    [],  # Scotland
    [
        Province.GREATER_POLAND,
        Province.LESSER_POLAND,
        Province.SILESIA,
        Province.POMERANIA,
        Province.MASOVIA,
        Province.GALICJA,
        Province.BREST,
    ],  # Poland
    [
        Province.LIGURIA,
        Province.LOMBARDY,
        Province.CORSICA,
        Province.SARDINIA,
        Province.TUSCANY,
    ],  # Genoa
    [],  # Morocco
    [],  # England
    [
        Province.LEON,
        Province.GALICIA,
        Province.LUSITANIA,
        Province.ARAGON,
        Province.CATALONIA,
        Province.NAVARRE,
        Province.CASTILE,
        Province.ANDALUSIA,
        Province.LA_MANCHA,
        Province.VALENCIA,
    ],  # Portugal
    [
        Province.VALENCIA,
        Province.BALEARS,
        Province.SICILY,
        Province.APULIA,
        Province.CALABRIA,
    ],  # Aragon
    [Province.OSTERLAND],  # Sweden
    [
        Province.LIVONIA,
        Province.ESTONIA,
        Province.LITHUANIA,
        Province.PRUSSIA,
    ],  # Prussia
    [],  # Lithuania
    [
        Province.AUSTRIA,
        Province.CARINTHIA,
        Province.BAVARIA,
        Province.BOHEMIA,
        Province.MORAVIA,
        Province.SILESIA,
    ],  # Austria
    [],  # Turkey
    [],  # Moscow
    [],  # Dutch
    [],  # Papal States
]


def getCrusadeInit(iCrusade):
    return data.lCrusadeInit[iCrusade]


def setCrusadeInit(iCrusade, iNewCode):
    # codes are:	-2, no crusade yet
    # 				-1 crusade is active but waiting to start (Holy City is Christian and/or another Crusade in progress)
    # 				0 or more, the turn when it was initialized
    data.lCrusadeInit[iCrusade] = iNewCode


def addSelectedUnit(iUnitPlace):
    data.lSelectedUnits[iUnitPlace] += 1


def setSelectedUnit(iUnitPlace, iNewNumber):
    data.lSelectedUnits[iUnitPlace] = iNewNumber


def getSelectedUnit(iUnitPlace):
    return data.lSelectedUnits[iUnitPlace]


def changeNumUnitsSent(iPlayer, iChange):
    data.lNumUnitsSent[iPlayer] += iChange


def setNumUnitsSent(iPlayer, iNewNumber):
    data.lNumUnitsSent[iPlayer] = iNewNumber


def getNumUnitsSent(iPlayer):
    return data.lNumUnitsSent[iPlayer]


def getActiveCrusade(iGameTurn):
    for i in range(NUM_CRUSADES):
        iInit = data.lCrusadeInit[i]
        if iInit > -1 and iInit + 9 > iGameTurn:
            return i
    return -1


def getParticipate():
    return data.bParticipate


def setParticipate(bVal):
    data.bParticipate = bVal


def getVotingPower(iCiv):
    return data.lVotingPower[iCiv]


def setVotingPower(iCiv, iVotes):
    data.lVotingPower[iCiv] = iVotes


def getCrusadePower():
    return data.iCrusadePower


def setCrusadePower(iPower):
    data.iCrusadePower = iPower


def getFavorite():
    return data.iFavorite


def setFavorite(iFavorite):
    data.iFavorite = iFavorite


def getPowerful():
    return data.iPowerful


def setPowerful(iPowerful):
    data.iPowerful = iPowerful


def getLeader():
    return data.iLeader


def setLeader(iLeader):
    data.iLeader = iLeader


def getVotesGatheredFavorite():
    return data.lVotesGathered[0]


def setVotesGatheredFavorite(iVotes):
    data.lVotesGathered[0] = iVotes


def getVotesGatheredPowerful():
    return data.lVotesGathered[1]


def setVotesGatheredPowerful(iVotes):
    data.lVotesGathered[1] = iVotes


def getRichestCatholic():
    return data.iRichestCatholic


def setRichestCatholic(iPlayer):
    data.iRichestCatholic = iPlayer


def getIsTarget(iCiv):
    return data.lDeviateTargets[iCiv]


def setIsTarget(iCiv, bTarget):
    data.lDeviateTargets[iCiv] = bTarget


def getTargetPlot():
    return data.tTarget


def setTarget(iX, iY):
    data.tTarget = (iX, iY)


def hasSucceeded():
    iSucc = data.iCrusadeSucceeded
    iTest = iSucc == 1
    return iTest


def setSucceeded():
    data.iCrusadeSucceeded = 1


def getCrusadeToReturn():
    return data.iCrusadeToReturn


def setCrusadeToReturn(iNewValue):
    data.iCrusadeToReturn = iNewValue


def isDefensiveCrusadeEnabled():
    return data.bDCEnabled


def setDefensiveCrusadeEnabled(bNewValue):
    data.bDCEnabled = bNewValue


def getDefensiveCrusadeLast():
    return data.iDCLast


def setDefensiveCrusadeLast(iLast):
    data.iDCLast = iLast


def initVotePopup():
    iHuman = human()
    pHuman = gc.getPlayer(iHuman)
    iActiveCrusade = getActiveCrusade(turn())
    iBribe = 200 + 50 * iActiveCrusade
    if pHuman.getGold() >= iBribe:
        event_popup(
            7616,
            text("TXT_KEY_CRUSADE_INIT_POPUP"),
            text("TXT_KEY_CRUSADE_INIT"),
            [
                text("TXT_KEY_CRUSADE_ACCEPT"),
                text("TXT_KEY_CRUSADE_DENY"),
                text("TXT_KEY_CRUSADE_DENY_RUDE"),
                text("TXT_KEY_CRUSADE_BRIBE_OUT", iBribe),
            ],
        )
    else:
        event_popup(
            7616,
            text("TXT_KEY_CRUSADE_INIT_POPUP"),
            text("TXT_KEY_CRUSADE_INIT"),
            [
                text("TXT_KEY_CRUSADE_ACCEPT"),
                text("TXT_KEY_CRUSADE_DENY"),
                text("TXT_KEY_CRUSADE_DENY_RUDE"),
            ],
        )


def informLeaderPopup():
    event_popup(
        7617,
        text("TXT_KEY_CRUSADE_LEADER_POPUP"),
        player(getLeader()).getName() + text("TXT_KEY_CRUSADE_LEAD"),
        [text("TXT_KEY_CRUSADE_OK")],
    )


def voteHumanPopup():
    favorite_txt = (
        gc.getPlayer(getFavorite()).getName()
        + " ("
        + gc.getPlayer(getFavorite()).getCivilizationShortDescription(0)
        + ")"
    )
    powerful_txt = (
        gc.getPlayer(getPowerful()).getName()
        + " ("
        + gc.getPlayer(getPowerful()).getCivilizationShortDescription(0)
        + ")"
    )
    event_popup(
        7618,
        text("TXT_KEY_CRUSADE_VOTE_POPUP"),
        text("TXT_KEY_CRUSADE_VOTE"),
        [favorite_txt, powerful_txt],
    )


def deviateHumanPopup():
    iCost = gc.getPlayer(human()).getGold() / 3
    sString = (
        text("TXT_KEY_CRUSADE_RICHEST")
        + text("TXT_KEY_CRUSADE_COST")
        + " "
        + str(iCost)
        + " "
        + text("TXT_KEY_CRUSADE_GOLD")
        + gc.getPlayer(getLeader()).getName()
        + " "
        + text("TXT_KEY_CRUSADE_CURRENT_LEADER")
    )
    event_popup(
        7619,
        text("TXT_KEY_CRUSADE_DEVIATE"),
        sString,
        [text("TXT_KEY_CRUSADE_DECIDE_WEALTH"), text("TXT_KEY_CRUSADE_DECIDE_FAITH")],
    )


def deviateNewTargetPopup():
    lTargetList = []
    lTargetList.append(
        gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity().getName()
        + " ("
        + gc.getPlayer(
            gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity().getOwner()
        ).getCivilizationAdjective(0)
        + ")"
    )
    for iPlayer in civilizations().majors().ids():
        pPlayer = gc.getPlayer(iPlayer)
        if (
            iPlayer == Civ.POPE
            or pPlayer.getStateReligion() == Religion.CATHOLICISM
            or not pPlayer.isAlive()
        ):
            setIsTarget(iPlayer, False)
        else:
            setIsTarget(iPlayer, True)
            lTargetList.append(
                pPlayer.getCapitalCity().getName()
                + " ("
                + pPlayer.getCivilizationAdjective(0)
                + ")"
            )
    event_popup(7620, text("TXT_KEY_CRUSADE_CORRUPT"), text("TXT_KEY_CRUSADE_TARGET"), lTargetList)


def underCrusadeAttackPopup(sCityName, iLeader):
    sText = text(
        "TXT_KEY_CRUSADE_UNDER_ATTACK1",
        gc.getPlayer(iLeader).getCivilizationAdjective(0),
        gc.getPlayer(iLeader).getName(),
        sCityName,
    )
    event_popup(
        7621, text("TXT_KEY_CRUSADE_UNDER_ATTACK"), sText, [text("TXT_KEY_CRUSADE_PREPARE")]
    )


@handler("religionFounded")
def endCrusades(iReligion, iFounder):
    # 3Miro: end Crusades for the Holy Land after the Reformation
    if iReligion == Religion.PROTESTANTISM:
        for i in range(NUM_CRUSADES):
            if getCrusadeInit(i) < 0:
                setCrusadeInit(i, 0)
        # Absinthe: reset sent unit counter after the Crusades are over (so it won't give Company benefits forever based on the last one)
        for iPlayer in civilizations().majors().ids():
            setNumUnitsSent(iPlayer, 0)


def checkTurn(iGameTurn):
    # informPopup()

    if getCrusadeToReturn() > -1:
        freeCrusaders(getCrusadeToReturn())
        setCrusadeToReturn(-1)

    # Absinthe: crusade date - 5 means the exact time for the arrival
    if iGameTurn == year(1096) - 5:  # First Crusade arrives in 1096AD
        setCrusadeInit(0, -1)
    elif (
        iGameTurn >= year(1147) - 7 and getCrusadeInit(0) > 0 and getCrusadeInit(1) == -2
    ):  # Crusade of 1147AD, little earlier (need to be more than 9 turns between crusades)
        setCrusadeInit(1, -1)  # turn 176
    elif (
        iGameTurn >= year(1187) - 8 and getCrusadeInit(1) > 0 and getCrusadeInit(2) == -2
    ):  # Crusade of 1187AD, little earlier (need to be more than 9 turns between crusades)
        setCrusadeInit(2, -1)  # turn 187
    elif (
        iGameTurn >= year(1202) - 4 and getCrusadeInit(2) > 0 and getCrusadeInit(3) == -2
    ):  # Crusade of 1202AD, little later (need to be more than 9 turns between crusades)
        setCrusadeInit(3, -1)  # turn 197
    elif (
        iGameTurn >= year(1229) - 3 and getCrusadeInit(3) > 0 and getCrusadeInit(4) == -2
    ):  # Crusade of 1229AD, little later (need to be more than 9 turns between crusades)
        setCrusadeInit(4, -1)  # turn 207
    elif (
        iGameTurn >= year(1271) - 5 and getCrusadeInit(4) > 0 and getCrusadeInit(5) == -2
    ):  # Crusade of 1270AD
        setCrusadeInit(5, -1)  # turn 219

    # Start of Defensive Crusades: indulgences for the Reconquista given by the Catholic Church in 1000AD
    if iGameTurn == year(1000):
        setDefensiveCrusadeEnabled(True)

    # End of Defensive Crusades: no more defensive crusades after Protestantism is founded
    if isDefensiveCrusadeEnabled():
        if gc.getGame().isReligionFounded(Religion.PROTESTANTISM):
            setDefensiveCrusadeEnabled(False)

    if isDefensiveCrusadeEnabled():
        doDefensiveCrusade(iGameTurn)

    checkToStart(iGameTurn)

    iActiveCrusade = getActiveCrusade(iGameTurn)
    if iActiveCrusade > -1:
        iStartDate = getCrusadeInit(iActiveCrusade)
        if iStartDate == iGameTurn:
            doParticipation(iGameTurn)

        elif iStartDate + 1 == iGameTurn:
            computeVotingPower(iGameTurn)
            setCrusaders()
            for i in range(8):
                setSelectedUnit(i, 0)
            for iPlayer in civilizations().majors().ids():
                # Absinthe: first we set all civs' unit counter to 0, then send the new round of units
                setNumUnitsSent(iPlayer, 0)
                if getVotingPower(iPlayer) > 0:
                    sendUnits(iPlayer)
            if not anyParticipate():
                return
            chooseCandidates(iGameTurn)
            voteForCandidatesAI()
            voteForCandidatesHuman()

        elif iStartDate + 2 == iGameTurn:
            if not anyParticipate():
                return
            selectVoteWinner()
            decideTheRichestCatholic(iActiveCrusade)
            if getRichestCatholic() == human():
                decideDeviateHuman()
            else:
                decideDeviateAI()

        elif iStartDate + 5 == iGameTurn:
            if not anyParticipate():
                return
            crusadeArrival(iActiveCrusade)

        elif iStartDate + 8 == iGameTurn:
            iLeader = getLeader()
            setCrusadeToReturn(iLeader)
            returnCrusaders()


def checkToStart(iGameTurn):
    # if Jerusalem is Islamic or Pagan, Crusade has been initialized and it has been at least 5 turns since the last crusade and there are any Catholics, begin crusade
    pJPlot = gc.getMap().plot(*CITIES[City.JERUSALEM])
    for i in range(NUM_CRUSADES):  # check the Crusades
        if getCrusadeInit(i) == -1:  # if this one is to start
            if (
                pJPlot.isCity() and anyCatholic()
            ):  # if there is Jerusalem and there are any Catholics
                # Sedna17 -- allowing crusades against independent Jerusalem
                iVictim = pJPlot.getPlotCity().getOwner()
                if isOrMasterChristian(iVictim):
                    break
                if i == 0 or (
                    getCrusadeInit(i - 1) > -1 and getCrusadeInit(i - 1) + 9 < iGameTurn
                ):
                    setCrusadeInit(i, iGameTurn)


def anyCatholic():
    return civilizations().main().any(lambda c: c.has_state_religion(Religion.CATHOLICISM))


def anyParticipate():
    for i in civilizations().main().ids():
        if getVotingPower(i) > 0:
            return True
    return False


def eventApply7616(popupReturn):
    iHuman = human()
    if popupReturn.getButtonClicked() == 0:
        setParticipate(True)
        gc.getPlayer(iHuman).setIsCrusader(True)
    elif popupReturn.getButtonClicked() == 1 or popupReturn.getButtonClicked() == 2:
        setParticipate(False)
        pPlayer = gc.getPlayer(iHuman)
        pPlayer.setIsCrusader(False)
        pPlayer.changeFaith(-min(5, pPlayer.getFaith()))
        message(
            iHuman, text("TXT_KEY_CRUSADE_DENY_FAITH"), force=True, color=MessageData.LIGHT_RED
        )
        gc.getPlayer(Civ.POPE).AI_changeMemoryCount(iHuman, MemoryTypes.MEMORY_REJECTED_DEMAND, 2)
        # Absinthe: some units from Chivalric Orders might leave you nevertheless
        for pUnit in units().owner(iHuman).entities():
            iUnitType = pUnit.getUnitType()
            if iUnitType in [
                Unit.KNIGHT_OF_ST_JOHNS,
                Unit.TEMPLAR,
                Unit.TEUTONIC,
            ]:
                pPlot = gc.getMap().plot(pUnit.getX(), pUnit.getY())
                random_value = percentage()
                # Absinthe: less chance for units currently on ships
                if pUnit.isCargo():
                    random_value -= 10
                if pPlot.isCity():
                    if getNumDefendersAtPlot(pPlot) > 3:
                        if random_value < 50:
                            addSelectedUnit(unitCrusadeCategory(iUnitType))
                            message(
                                iHuman,
                                text("TXT_KEY_CRUSADE_DENY_LEAVE_ANYWAY"),
                                button=gc.getUnitInfo(iUnitType).getButton(),
                                color=MessageData.LIGHT_RED,
                                location=pUnit,
                            )
                            pUnit.kill(0, -1)
                    elif getNumDefendersAtPlot(pPlot) > 1:
                        if random_value < 10:
                            addSelectedUnit(unitCrusadeCategory(iUnitType))
                            message(
                                iHuman,
                                text("TXT_KEY_CRUSADE_DENY_LEAVE_ANYWAY"),
                                button=gc.getUnitInfo(iUnitType).getButton(),
                                color=MessageData.LIGHT_RED,
                                location=pUnit,
                            )
                            pUnit.kill(0, -1)
                elif random_value < 30:
                    addSelectedUnit(unitCrusadeCategory(iUnitType))
                    message(
                        iHuman,
                        text("TXT_KEY_CRUSADE_DENY_LEAVE_ANYWAY"),
                        button=gc.getUnitInfo(iUnitType).getButton(),
                        color=MessageData.LIGHT_RED,
                        location=pUnit,
                    )
                    pUnit.kill(0, -1)
    # Absinthe: 3rd option, only if you have enough money to make a contribution to the Crusade instead of sending units
    else:
        setParticipate(False)
        pPlayer = gc.getPlayer(iHuman)
        pPlayer.setIsCrusader(False)
        pPope = gc.getPlayer(Civ.POPE)
        iActiveCrusade = getActiveCrusade(turn())
        iBribe = 200 + 50 * iActiveCrusade
        pPope.changeGold(iBribe)
        pPlayer.changeGold(-iBribe)
        gc.getPlayer(Civ.POPE).AI_changeMemoryCount(iHuman, MemoryTypes.MEMORY_REJECTED_DEMAND, 1)


def eventApply7618(popupReturn):
    if popupReturn.getButtonClicked() == 0:
        setVotesGatheredFavorite(getVotesGatheredFavorite() + getVotingPower(human()))
    else:
        setVotesGatheredPowerful(getVotesGatheredPowerful() + getVotingPower(human()))


def eventApply7619(popupReturn):
    if popupReturn.getButtonClicked() == 0:
        player().changeGold(-player().getGold() / 3)
        setLeader(human())
        setCrusadePower(getCrusadePower() / 2)
        deviateNewTargetPopup()
    else:
        setTarget(*CITIES[City.JERUSALEM])
        startCrusade()


def eventApply7620(popupReturn):
    iDecision = popupReturn.getButtonClicked()
    if iDecision == 0:
        setTarget(*CITIES[City.JERUSALEM])
        startCrusade()
        return
    iTargets = 0
    for i in civilizations().majors().ids():
        if getIsTarget(i):
            iTargets += 1
        if iTargets == iDecision:
            pTargetCity = gc.getPlayer(i).getCapitalCity()
            setTarget(pTargetCity.getX(), pTargetCity.getY())
            iDecision = -2

    startCrusade()


def doParticipation(iGameTurn):
    iHuman = human()
    if civilization(iHuman).date.birth < iGameTurn:
        pHuman = gc.getPlayer(iHuman)
        if pHuman.getStateReligion() != Religion.CATHOLICISM:
            setParticipate(False)
            message(
                iHuman, text("TXT_KEY_CRUSADE_CALLED"), force=True, color=MessageData.LIGHT_RED
            )
        else:
            initVotePopup()
    else:
        setParticipate(False)


def chooseCandidates(iGameTurn):
    bFound = False
    iFavorite = 0
    iFavor = 0
    for i in civilizations().main().ids():
        if getVotingPower(i) > 0:
            if bFound:
                iNFavor = gc.getRelationTowards(Civ.POPE, i)
                if iNFavor > iFavor:
                    iNFavor = iFavor
                    iFavorite = i
            else:
                iFavor = gc.getRelationTowards(Civ.POPE, i)
                iFavorite = i
                bFound = True
    setFavorite(iFavorite)

    iPowerful = iFavorite
    iPower = getVotingPower(iPowerful)

    for i in civilizations().main().ids():
        if getVotingPower(i) > iPower or (iPowerful == iFavorite and getVotingPower(i) > 0):
            iPowerful = i
            iPower = getVotingPower(iPowerful)

    if iPowerful == iFavorite:
        setPowerful(-1)
    else:
        setPowerful(iPowerful)


def computeVotingPower(iGameTurn):
    iTmJerusalem = gc.getPlayer(
        gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity().getOwner()
    ).getTeam()
    for iPlayer in civilizations().majors().ids():
        pPlayer = gc.getPlayer(iPlayer)
        if (
            civilization(iPlayer).date.birth > iGameTurn
            or not pPlayer.isAlive()
            or pPlayer.getStateReligion() != Religion.CATHOLICISM
            or gc.getTeam(pPlayer.getTeam()).isVassal(iTmJerusalem)
        ):
            setVotingPower(iPlayer, 0)
        else:
            # We use the (similarly named) getVotingPower from CvPlayer.cpp to determine a vote value for a given State Religion, but it's kinda strange
            # Will leave it this way for now, but might be a good idea to improve it at some point
            setVotingPower(iPlayer, pPlayer.getVotingPower(Religion.CATHOLICISM))

    # No votes from the human player if he/she won't participate (AI civs will always participate)
    if not getParticipate():
        setVotingPower(human(), 0)

    # The Pope has more votes (Rome is small anyway)
    setVotingPower(Civ.POPE, getVotingPower(Civ.POPE) * (5 / 4))

    iPower = 0
    for iPlayer in civilizations().majors().ids():
        iPower += getVotingPower(iPlayer)

    setCrusadePower(iPower)
    # Note that voting power is increased after this (but before the actual vote) for each sent unit by 2


def setCrusaders():
    for iPlayer in civilizations().majors().ids():
        if not iPlayer == human() and getVotingPower(iPlayer) > 0:
            gc.getPlayer(iPlayer).setIsCrusader(True)


def sendUnits(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    iNumUnits = pPlayer.getNumUnits()
    if civilization(iPlayer).date.birth + 10 > turn():  # in the first 10 turns
        if iNumUnits < 10:
            iMaxToSend = 0
        else:
            iMaxToSend = 1
    elif civilization(iPlayer).date.birth + 25 > turn():  # between turn 11-25
        iMaxToSend = min(10, max(1, (5 * iNumUnits) / 50))
    else:
        iMaxToSend = min(10, max(1, (5 * iNumUnits) / 35))  # after turn 25
    iCrusadersSend = 0
    if iMaxToSend > 0:
        # Absinthe: a randomized list of all units of the civ
        lUnits = [pPlayer.getUnit(i) for i in range(iNumUnits)]
        random.shuffle(lUnits)
        for pUnit in lUnits:
            # Absinthe: check only for combat units and ignore naval units
            if pUnit.baseCombatStr() > 0 and pUnit.getDomainType() != DomainTypes.DOMAIN_SEA:
                # Absinthe: mercenaries and leaders (units with attached Great Generals) won't go
                if not pUnit.isHasPromotion(Promotion.MERC) and not pUnit.isHasPromotion(
                    Promotion.LEADER
                ):
                    iCrusadeCategory = unitCrusadeCategory(pUnit.getUnitType())
                    pPlot = gc.getMap().plot(pUnit.getX(), pUnit.getY())
                    iRandNum = percentage()
                    # Absinthe: much bigger chance for special Crusader units and Knights
                    if iCrusadeCategory < 4:
                        if pPlot.isCity():
                            if getNumDefendersAtPlot(pPlot) > 3:
                                if iRandNum < 80:
                                    iCrusadersSend += 1
                                    sendUnit(pUnit)
                            elif getNumDefendersAtPlot(pPlot) > 1:
                                if iRandNum < 40:
                                    iCrusadersSend += 1
                                    sendUnit(pUnit)
                        else:
                            # Absinthe: much less chance for units currently on ships
                            if pUnit.isCargo():
                                if iRandNum < 40:
                                    iCrusadersSend += 1
                                    sendUnit(pUnit)
                            else:
                                if iRandNum < 80:
                                    iCrusadersSend += 1
                                    sendUnit(pUnit)
                    else:
                        if pPlot.isCity():
                            if getNumDefendersAtPlot(pPlot) > 2:
                                if iRandNum < (unitProbability(pUnit.getUnitType()) - 10):
                                    iCrusadersSend += 1
                                    sendUnit(pUnit)
                        else:
                            # Absinthe: much less chance for units currently on ships
                            if pUnit.isCargo():
                                if iRandNum < (unitProbability(pUnit.getUnitType()) - 10) / 2:
                                    iCrusadersSend += 1
                                    sendUnit(pUnit)
                            else:
                                if iRandNum < (unitProbability(pUnit.getUnitType()) - 10):
                                    iCrusadersSend += 1
                                    sendUnit(pUnit)
                    if iCrusadersSend == iMaxToSend:
                        return
        # Absinthe: extra chance for some random units, if we didn't fill the quota
        for i in range(15):
            iNumUnits = (
                pPlayer.getNumUnits()
            )  # we have to recalculate each time, as some units might have gone on the Crusade already
            iRandUnit = rand(iNumUnits)
            pUnit = pPlayer.getUnit(iRandUnit)
            # Absinthe: check only for combat units and ignore naval units
            if pUnit.baseCombatStr() > 0 and pUnit.getDomainType() != 0:
                # Absinthe: mercenaries and leaders (units with attached Great Generals) won't go
                if not pUnit.isHasPromotion(Promotion.MERC) and not pUnit.isHasPromotion(
                    Promotion.LEADER
                ):
                    pPlot = gc.getMap().plot(pUnit.getX(), pUnit.getY())
                    if pPlot.isCity():
                        if getNumDefendersAtPlot(pPlot) > 2:
                            if percentage_chance(
                                unitProbability(pUnit.getUnitType()), strict=True
                            ):
                                iCrusadersSend += 1
                                sendUnit(pUnit)
                    else:
                        # Absinthe: much less chance for units currently on ships
                        if pUnit.isCargo() and percentage_chance(
                            unitProbability(pUnit.getUnitType() / 2), strict=True
                        ):
                            iCrusadersSend += 1
                            sendUnit(pUnit)
                        elif percentage_chance(unitProbability(pUnit.getUnitType()), strict=True):
                            iCrusadersSend += 1
                            sendUnit(pUnit)
                    if iCrusadersSend == iMaxToSend:
                        return


def getNumDefendersAtPlot(pPlot):
    iOwner = pPlot.getOwner()
    if iOwner < 0:
        return 0
    iNumUnits = pPlot.getNumUnits()
    iDefenders = 0
    for i in range(iNumUnits):
        pUnit = pPlot.getUnit(i)
        if pUnit.getOwner() == iOwner:
            if pUnit.baseCombatStr() > 0 and pUnit.getDomainType() != DomainTypes.DOMAIN_SEA:
                iDefenders += 1
    return iDefenders


def sendUnit(pUnit):
    iOwner = pUnit.getOwner()
    addSelectedUnit(unitCrusadeCategory(pUnit.getUnitType()))
    setVotingPower(iOwner, getVotingPower(iOwner) + 2)
    changeNumUnitsSent(iOwner, 1)  # Absinthe: counter for sent units per civ
    # Absinthe: faith point boost for each sent unit (might get some more on successful Crusade):
    player(iOwner).changeFaith(1)
    message_if_human(
        human(),
        text("TXT_KEY_CRUSADE_LEAVE") + " " + pUnit.getName(),
        sound="AS2D_BUILD_CATHOLIC",
        color=MessageData.ORANGE,
    )
    pUnit.kill(0, -1)


def unitProbability(iUnitType):
    if iUnitType in [
        Unit.ARCHER,
        Unit.CROSSBOWMAN,
        Unit.ARBALEST,
        Unit.GENOA_BALESTRIERI,
        Unit.LONGBOWMAN,
        Unit.ENGLISH_LONGBOWMAN,
        Unit.PORTUGAL_FOOT_KNIGHT,
    ]:
        return 10
    if iUnitType in [
        Unit.LANCER,
        Unit.BULGARIAN_KONNIK,
        Unit.CORDOBAN_BERBER,
        Unit.HEAVY_LANCER,
        Unit.HUNGARIAN_HUSZAR,
        Unit.ARABIA_GHAZI,
        Unit.BYZANTINE_CATAPHRACT,
        Unit.KIEV_DRUZHINA,
        Unit.KNIGHT,
        Unit.MOSCOW_BOYAR,
        Unit.BURGUNDIAN_PALADIN,
    ]:
        return 70
    if iUnitType in [
        Unit.TEMPLAR,
        Unit.TEUTONIC,
        Unit.KNIGHT_OF_ST_JOHNS,
        Unit.CALATRAVA_KNIGHT,
        Unit.DRAGON_KNIGHT,
    ]:
        return 90
    if (
        iUnitType <= Unit.ISLAMIC_MISSIONARY or iUnitType >= Unit.WORKBOAT
    ):  # Workers, Executives, Missionaries, Sea Units and Mercenaries do not go
        return -1
    return 50


def unitCrusadeCategory(iUnitType):
    if iUnitType == Unit.TEMPLAR:
        return 0
    if iUnitType == Unit.TEUTONIC:
        return 1
    if iUnitType in [
        Unit.KNIGHT_OF_ST_JOHNS,
        Unit.CALATRAVA_KNIGHT,
        Unit.DRAGON_KNIGHT,
    ]:
        return 2
    if iUnitType in [
        Unit.KNIGHT,
        Unit.MOSCOW_BOYAR,
        Unit.BURGUNDIAN_PALADIN,
    ]:
        return 3
    if iUnitType in [
        Unit.HEAVY_LANCER,
        Unit.HUNGARIAN_HUSZAR,
        Unit.ARABIA_GHAZI,
        Unit.BYZANTINE_CATAPHRACT,
        Unit.KIEV_DRUZHINA,
    ]:
        return 4
    if iUnitType in [
        Unit.LANCER,
        Unit.BULGARIAN_KONNIK,
        Unit.CORDOBAN_BERBER,
    ]:
        return 5
    if iUnitType in [Unit.CATAPULT, Unit.TREBUCHET]:
        return 6
    return 7


def voteForCandidatesAI():
    if getPowerful() == -1:
        setLeader(getFavorite())
        if getParticipate():
            informLeaderPopup()
        elif player().isExisting():
            message(
                human(),
                gc.getPlayer(getLeader()).getName() + text("TXT_KEY_CRUSADE_LEAD"),
                force=True,
                color=MessageData.LIGHT_RED,
            )
        return

    iFavorite = getFavorite()
    iPowerful = getPowerful()
    if iFavorite == human():
        iFavorVotes = 0
    else:
        iFavorVotes = getVotingPower(iFavorite)
    if iPowerful == human():
        iPowerVotes = 0
    else:
        iPowerVotes = getVotingPower(iPowerful)

    for civ in civilizations().majors().ai().drop(iFavorite, iPowerful).ids():
        iVotes = getVotingPower(civ)
        if iVotes > 0:
            if gc.getRelationTowards(civ, iFavorite) > gc.getRelationTowards(civ, iPowerful):
                iFavorVotes += iVotes
            else:
                iPowerVotes += iVotes

    setVotesGatheredFavorite(iFavorVotes)
    setVotesGatheredPowerful(iPowerVotes)


def voteForCandidatesHuman():
    if getParticipate() and not getPowerful() == -1:
        voteHumanPopup()


def selectVoteWinner():
    if getVotesGatheredPowerful() > getVotesGatheredFavorite():
        setLeader(getPowerful())
    else:
        setLeader(getFavorite())

    if getParticipate():
        informLeaderPopup()
    elif player().isExisting():
        message(
            human(),
            gc.getPlayer(getLeader()).getName() + text("TXT_KEY_CRUSADE_LEAD"),
            force=True,
            color=MessageData.LIGHT_RED,
        )

    # not yet, check to see for deviations
    # pJPlot = gc.getMap().plot(*CITIES[City.JERUSALEM])
    # gc.getTeam( gc.getPlayer( getLeader() ) ).declareWar( pJPlot.getPlotCity().getOwner(), True, -1 )


def decideTheRichestCatholic(iActiveCrusade):
    # The First Crusade cannot be deviated
    if iActiveCrusade == 0:
        setRichestCatholic(-1)
        return

    iRichest = -1
    iMoney = 0
    # iPopeMoney = gc.getPlayer( Civ.POPE ).getGold()
    for i in civilizations().main().ids():
        if getVotingPower(i) > 0:
            pPlayer = gc.getPlayer(i)
            iPlayerMoney = pPlayer.getGold()
            # if ( iPlayerMoney > iMoney and iPlayerMoney > iPopeMoney ):
            if iPlayerMoney > iMoney:
                iRichest = i
                iMoney = iPlayerMoney

    if iRichest != Civ.POPE:
        setRichestCatholic(iRichest)
    else:
        setRichestCatholic(-1)


def decideDeviateHuman():
    deviateHumanPopup()


def decideDeviateAI():
    iRichest = getRichestCatholic()
    bStolen = False
    if iRichest in [Civ.VENECIA, Civ.GENOA]:
        pByzantium = gc.getPlayer(Civ.BYZANTIUM)
        if pByzantium.isAlive():
            # Only if the potential attacker is not vassal of the target
            iTeamByzantium = pByzantium.getTeam()
            pRichest = gc.getPlayer(iRichest)
            pTeamRichest = gc.getTeam(pRichest.getTeam())
            if not pTeamRichest.isVassal(iTeamByzantium):
                # Only if Byzantium holds Constantinople and not a vassal
                pConstantinoplePlot = gc.getMap().plot(
                    *civilization(Civ.BYZANTIUM).location.capital
                )
                pConstantinopleCity = pConstantinoplePlot.getPlotCity()
                iConstantinopleOwner = pConstantinopleCity.getOwner()
                # should check if Constantinople is their capital city to be fully correct, but we can assume that's the case
                bIsNotAVassal = not isAVassal(Civ.BYZANTIUM)
                if iConstantinopleOwner == Civ.BYZANTIUM and bIsNotAVassal:
                    crusadeStolenAI(iRichest, Civ.BYZANTIUM)
                    bStolen = True
    elif iRichest in [Civ.CASTILE, Civ.PORTUGAL, Civ.ARAGON]:
        pCordoba = gc.getPlayer(Civ.CORDOBA)
        if pCordoba.isAlive():
            # Only if the potential attacker is not vassal of the target
            iTeamCordoba = pCordoba.getTeam()
            pRichest = gc.getPlayer(iRichest)
            pTeamRichest = gc.getTeam(pRichest.getTeam())
            if not pTeamRichest.isVassal(iTeamCordoba):
                # Only if Cordoba is Muslim and not a vassal
                bIsNotAVassal = not isAVassal(Civ.CORDOBA)
                if pCordoba.getStateReligion() == Religion.ISLAM and bIsNotAVassal:
                    crusadeStolenAI(iRichest, Civ.CORDOBA)
                    bStolen = True
    elif iRichest in [Civ.HUNGARY, Civ.POLAND, Civ.AUSTRIA]:
        pTurkey = gc.getPlayer(Civ.OTTOMAN)
        if pTurkey.isAlive():
            # Only if the potential attacker is not vassal of the target
            iTeamTurkey = pTurkey.getTeam()
            pRichest = gc.getPlayer(iRichest)
            pTeamRichest = gc.getTeam(pRichest.getTeam())
            if not pTeamRichest.isVassal(iTeamTurkey):
                # Only if the Ottomans are Muslim and not a vassal
                bIsNotAVassal = not isAVassal(Civ.OTTOMAN)
                if pTurkey.getStateReligion() == Religion.ISLAM and bIsNotAVassal:
                    crusadeStolenAI(iRichest, Civ.OTTOMAN)
                    bStolen = True

    if not bStolen:
        setTarget(*CITIES[City.JERUSALEM])

    startCrusade()


def crusadeStolenAI(iNewLeader, iNewTarget):
    setLeader(iNewLeader)
    pLeader = gc.getPlayer(iNewLeader)
    if player().isExisting():
        message(
            human(),
            pLeader.getName() + text("TXT_KEY_CRUSADE_DEVIATED"),
            color=MessageData.LIGHT_RED,
        )
    # pLeader.setGold( pLeader.getGold() - gc.getPlayer( Civ.POPE ).getGold() / 3 )
    # pLeader.setGold( gc.getPlayer( Civ.POPE ).getGold() / 4 )
    pLeader.setGold(2 * pLeader.getGold() / 3)
    pTarget = gc.getPlayer(iNewTarget).getCapitalCity()
    setTarget(pTarget.getX(), pTarget.getY())
    setCrusadePower(getCrusadePower() / 2)


def startCrusade():
    iHuman = human()
    iLeader = getLeader()
    iX, iY = getTargetPlot()
    pTargetCity = gc.getMap().plot(iX, iY).getPlotCity()
    iTargetPlayer = pTargetCity.getOwner()
    # Absinthe: in case the Crusader civ has been destroyed
    if not gc.getPlayer(iLeader).isAlive():
        returnCrusaders()
        return
    # Target city can change ownership during the voting
    if gc.getPlayer(iTargetPlayer).getStateReligion() == Religion.CATHOLICISM:
        returnCrusaders()
        return
    # Absinthe: do not Crusade against themselves
    if iTargetPlayer == iLeader:
        returnCrusaders()
        return
    if iTargetPlayer == iHuman:
        underCrusadeAttackPopup(pTargetCity.getName(), iLeader)
    elif player().isExisting():
        sCityName = lookupName(pTargetCity, Civ.POPE)
        if sCityName == "Unknown":
            sCityName = lookupName(pTargetCity, iLeader)
        sText = text(
            "TXT_KEY_CRUSADE_START",
            gc.getPlayer(iLeader).getCivilizationAdjectiveKey(),
            gc.getPlayer(iLeader).getName(),
            gc.getPlayer(iTargetPlayer).getCivilizationAdjectiveKey(),
            sCityName,
        )
        message(iHuman, sText, color=MessageData.LIGHT_RED)

    # Absinthe: proper war declaration checks
    teamLeader = gc.getTeam(gc.getPlayer(iLeader).getTeam())
    iTeamTarget = gc.getPlayer(iTargetPlayer).getTeam()
    if not teamLeader.isAtWar(iTeamTarget):
        # Absinthe: add contact if they did not meet before
        if not teamLeader.isHasMet(iTeamTarget):
            teamLeader.meet(iTeamTarget, False)
        if teamLeader.canDeclareWar(iTeamTarget):
            teamLeader.declareWar(iTeamTarget, True, -1)
        else:
            # we cannot declare war to the current owner of the target city
            returnCrusaders()
            return


def returnCrusaders():
    setLeader(-1)
    for i in civilizations().majors().ids():
        gc.getPlayer(i).setIsCrusader(False)


def crusadeArrival(iActiveCrusade):
    iTX, iTY = getTargetPlot()
    iChosenX = -1
    iChosenY = -1

    # if the leader has been destroyed, cancel the Crusade
    iLeader = getLeader()
    if iLeader == -1 or not gc.getPlayer(iLeader).isAlive():
        returnCrusaders()
        return

    # if the target is Jerusalem, and in the mean time it has been captured by an Orthodox or Catholic player (or the owner of Jerusalem converted to a Christian religion), cancel the Crusade
    if (iTX, iTY) == CITIES[City.JERUSALEM]:
        pPlot = gc.getMap().plot(*CITIES[City.JERUSALEM])
        if pPlot.isCity():
            iVictim = pPlot.getPlotCity().getOwner()
            if iVictim < civilizations().majors().len():
                iReligion = gc.getPlayer(iVictim).getStateReligion()
                if iReligion in [Religion.CATHOLICISM, Religion.ORTHODOXY]:
                    return

    # if not at war with the owner of the city, declare war
    pPlot = gc.getMap().plot(iTX, iTY)
    if pPlot.isCity():
        iVictim = pPlot.getPlotCity().getOwner()
        if iVictim != iLeader and gc.getPlayer(iVictim).getStateReligion() != Religion.CATHOLICISM:
            teamLeader = gc.getTeam(gc.getPlayer(iLeader).getTeam())
            iTeamVictim = gc.getPlayer(iVictim).getTeam()
            if not teamLeader.isAtWar(iTeamVictim):
                # Absinthe: add contact if they did not meet before
                if not teamLeader.isHasMet(iTeamVictim):
                    teamLeader.meet(iTeamVictim, False)
                if teamLeader.canDeclareWar(iTeamVictim):
                    teamLeader.declareWar(iTeamVictim, False, -1)
                else:
                    # we cannot declare war to the current owner of the target city
                    returnCrusaders()
                    return

    lFreeLandPlots = []
    lLandPlots = []
    for plot in (
        plots()
        .surrounding((iTX, iTY))
        .filter(lambda p: (p.isHills() or p.isFlatlands()) and not p.isCity())
        .entities()
    ):
        lLandPlots.append(location(plot))
        if plot.getNumUnits() == 0:
            lFreeLandPlots.append(location(plot))
    # Absinthe: we try to spawn the army west from the target city (preferably northwest), or at least on as low x coordinates as possible
    # 			works great both for Jerusalem (try not to spawn across the Jordan river) and for Constantinople (European side, where the actual city is located)
    # 			also better for most cities in the Levant and in Egypt, and doesn't really matter for the rest
    if lFreeLandPlots:
        iChosenX = 200
        iChosenY = 200
        for tFreeLandPlot in lFreeLandPlots:
            if tFreeLandPlot[0] < iChosenX:
                iChosenX = tFreeLandPlot[0]
                iChosenY = tFreeLandPlot[1]
            elif tFreeLandPlot[0] == iChosenX:
                if tFreeLandPlot[0] > iChosenY:
                    iChosenY = tFreeLandPlot[1]
    elif lLandPlots:
        iChosenX = 200
        iChosenY = 200
        for tLandPlot in lLandPlots:
            if tLandPlot[0] < iChosenX:
                iChosenX = tLandPlot[0]
                iChosenY = tLandPlot[1]
            elif tLandPlot[0] == iChosenX:
                if tLandPlot[0] > iChosenY:
                    iChosenY = tLandPlot[1]
        pPlot = gc.getMap().plot(iChosenX, iChosenY)
        for i in range(pPlot.getNumUnits()):
            pPlot.getUnit(0).kill(False, Civ.BARBARIAN)

    # Absinthe: if a valid plot is found, make the units and send a message about the arrival to the human player
    if (iChosenX, iChosenY) != (-1, -1):
        crusadeMakeUnits((iChosenX, iChosenY), iActiveCrusade)
        if human() == iLeader:
            pTargetCity = gc.getMap().plot(iTX, iTY).getPlotCity()
            sCityName = lookupName(pTargetCity, Civ.POPE)
            if sCityName == "Unknown":
                sCityName = lookupName(pTargetCity, iLeader)
            message(
                human(),
                text("TXT_KEY_CRUSADE_ARRIVAL", sCityName) + "!",
                color=MessageData.GREEN,
                location=(iChosenX, iChosenY),
            )
    else:
        returnCrusaders()


def crusadeMakeUnits(tPlot, iActiveCrusade):
    iLeader = getLeader()
    teamLeader = gc.getTeam(gc.getPlayer(iLeader).getTeam())
    iTX, iTY = getTargetPlot()
    # if the target is Jerusalem
    if (iTX, iTY) == CITIES[City.JERUSALEM]:
        iRougeModifier = 100
        # human player should always face powerful units when defending Jerusalem
        iHuman = human()
        pPlot = gc.getMap().plot(*CITIES[City.JERUSALEM])
        iVictim = pPlot.getPlotCity().getOwner()
        if teamLeader.isHasTech(Technology.CHIVALRY) or iVictim == iHuman:
            make_crusade_unit(iLeader, Unit.BURGUNDIAN_PALADIN, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.TEMPLAR, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.TEUTONIC, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.KNIGHT_OF_ST_JOHNS, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.GUISARME, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.CATAPULT, tPlot, iActiveCrusade)
        else:
            make_crusade_units(iLeader, Unit.HEAVY_LANCER, tPlot, iActiveCrusade, 2)
            make_crusade_unit(iLeader, Unit.LANCER, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.LONG_SWORDSMAN, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.SPEARMAN, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.TREBUCHET, tPlot, iActiveCrusade)
        # there are way too many generic units in most Crusades:
        if getSelectedUnit(7) > 1:
            iReducedNumber = (
                getSelectedUnit(7) * 6 / 10
            )  # note that this is before the specific Crusade reduction
            setSelectedUnit(7, iReducedNumber)
    # if the Crusade was derailed
    else:
        iRougeModifier = 200
        if teamLeader.isHasTech(Technology.CHIVALRY):
            make_crusade_unit(iLeader, Unit.KNIGHT, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.TEUTONIC, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.LONG_SWORDSMAN, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.GUISARME, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.CATAPULT, tPlot, iActiveCrusade)
        else:
            make_crusade_unit(iLeader, Unit.HEAVY_LANCER, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.LANCER, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.LONG_SWORDSMAN, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.SPEARMAN, tPlot, iActiveCrusade)
            make_crusade_unit(iLeader, Unit.TREBUCHET, tPlot, iActiveCrusade)
        # there are way too many generic units in most Crusades:
        if getSelectedUnit(7) > 1:
            iReducedNumber = (
                getSelectedUnit(7) * 8 / 10
            )  # note that this is before the specific Crusade reduction
            setSelectedUnit(7, iReducedNumber)

    # Absinthe: not all units should arrive near Jerusalem
    # 			later Crusades have more units in the pool, so they should have bigger reduction
    iHuman = human()
    pPlot = gc.getMap().plot(*CITIES[City.JERUSALEM])
    iVictim = pPlot.getPlotCity().getOwner()
    # Absinthe: this reduction is very significant for an AI-controlled Jerusalem, but Crusades should remain an increasing threat to the human player
    if iVictim != iHuman:
        if iActiveCrusade == 0:
            iRougeModifier *= 7 / 5
        elif iActiveCrusade == 1:
            iRougeModifier *= 8 / 5
        elif iActiveCrusade == 2:
            iRougeModifier *= 9 / 5
        elif iActiveCrusade == 3:
            iRougeModifier *= 10 / 5
        elif iActiveCrusade == 4:
            iRougeModifier *= 12 / 5
        else:
            iRougeModifier *= 14 / 5
    else:
        if iActiveCrusade == 0:
            iRougeModifier *= 11 / 10
        elif iActiveCrusade == 1:
            iRougeModifier *= 5 / 5
        elif iActiveCrusade == 2:
            iRougeModifier *= 6 / 5
        elif iActiveCrusade == 3:
            iRougeModifier *= 7 / 5
        elif iActiveCrusade == 4:
            iRougeModifier *= 8 / 5
        else:
            iRougeModifier *= 8 / 5

    if getSelectedUnit(0) > 0:
        make_crusade_units(
            iLeader,
            Unit.TEMPLAR,
            tPlot,
            iActiveCrusade,
            getSelectedUnit(0) * 100 / iRougeModifier,
        )
    if getSelectedUnit(1) > 0:
        make_crusade_units(
            iLeader,
            Unit.TEUTONIC,
            tPlot,
            iActiveCrusade,
            getSelectedUnit(1) * 100 / iRougeModifier,
        )
    if getSelectedUnit(2) > 0:
        make_crusade_units(
            iLeader,
            Unit.KNIGHT_OF_ST_JOHNS,
            tPlot,
            iActiveCrusade,
            getSelectedUnit(2) * 100 / iRougeModifier,
        )
    if getSelectedUnit(3) > 0:
        iKnightNumber = getSelectedUnit(3) * 100 / iRougeModifier
        if iLeader == Civ.BURGUNDY:
            for i in range(0, iKnightNumber):
                if percentage_chance(50, strict=True):
                    make_crusade_unit(iLeader, Unit.BURGUNDIAN_PALADIN, tPlot, iActiveCrusade)
                else:
                    make_crusade_unit(iLeader, Unit.KNIGHT, tPlot, iActiveCrusade)
        else:
            for i in range(0, iKnightNumber):
                if percentage_chance(20, strict=True):
                    make_crusade_unit(iLeader, Unit.BURGUNDIAN_PALADIN, tPlot, iActiveCrusade)
                else:
                    make_crusade_unit(iLeader, Unit.KNIGHT, tPlot, iActiveCrusade)
    if getSelectedUnit(4) > 0:
        iLightCavNumber = getSelectedUnit(4) * 100 / iRougeModifier
        if iLeader == Civ.HUNGARY:
            for i in range(0, iLightCavNumber):
                if percentage_chance(50, strict=True):
                    make_crusade_unit(iLeader, Unit.HUNGARIAN_HUSZAR, tPlot, iActiveCrusade)
                else:
                    make_crusade_unit(iLeader, Unit.HEAVY_LANCER, tPlot, iActiveCrusade)
        else:
            make_crusade_units(iLeader, Unit.HEAVY_LANCER, tPlot, iActiveCrusade, iLightCavNumber)
    if getSelectedUnit(5) > 0:
        make_crusade_units(
            iLeader,
            Unit.LANCER,
            tPlot,
            iActiveCrusade,
            getSelectedUnit(5) * 100 / iRougeModifier,
        )
    if getSelectedUnit(6) > 0:
        iSiegeNumber = getSelectedUnit(6) * 100 / iRougeModifier
        if iSiegeNumber > 2:
            make_crusade_units(iLeader, Unit.CATAPULT, tPlot, iActiveCrusade, 2)
            make_crusade_units(iLeader, Unit.TREBUCHET, tPlot, iActiveCrusade, iSiegeNumber - 2)
        else:
            make_crusade_units(iLeader, Unit.CATAPULT, tPlot, iActiveCrusade, iSiegeNumber)
    if getSelectedUnit(7) > 0:
        iFootNumber = getSelectedUnit(7) * 100 / iRougeModifier
        for i in range(0, iFootNumber):
            if percentage_chance(50, strict=True):
                make_crusade_unit(iLeader, Unit.LONG_SWORDSMAN, tPlot, iActiveCrusade)
            else:
                make_crusade_unit(iLeader, Unit.GUISARME, tPlot, iActiveCrusade)


def freeCrusaders(iPlayer):
    # the majority of Crusader units will return from the Crusade, so the Crusading civ will have harder time keeping Jerusalem and the Levant
    iPrevGameTurn = (
        turn() - 1
    )  # process for freeCrusaders was actually started in the previous turn, iActiveCrusade might have changed for the current turn
    iActiveCrusade = getActiveCrusade(
        iPrevGameTurn
    )  # Absinthe: the Crusader units are called back before the next Crusade is initialized
    iHuman = human()
    for pUnit in units().owner(iPlayer).entities():
        if pUnit.getMercID() == (
            -5 - iActiveCrusade
        ):  # Absinthe: so this is a Crusader Unit of the active Crusade
            pPlot = gc.getMap().plot(pUnit.getX(), pUnit.getY())
            iOdds = 80
            iCrusadeCategory = unitCrusadeCategory(pUnit.getUnitType())
            if iCrusadeCategory < 3:
                continue  # Knightly Orders don't return
            elif iCrusadeCategory == 7:
                iOdds = 50  # leave some defenders
            if pPlot.isCity():
                if pPlot.getPlotCity().getOwner() == iPlayer:
                    iDefenders = getNumDefendersAtPlot(pPlot)
                    if iDefenders < 4:
                        iOdds = 20
                        if iDefenders == 0:
                            continue

            if percentage_chance(iOdds, strict=True):
                pUnit.kill(0, -1)
                if iHuman == iPlayer:
                    message(
                        iHuman,
                        text("TXT_KEY_CRUSADE_CRUSADERS_RETURNING_HOME") + " " + pUnit.getName(),
                        color=MessageData.LIME,
                    )

    # benefits for the other participants on Crusade return - Faith points, GG points, Relics
    for iCiv in civilizations().main().ids():
        pCiv = gc.getPlayer(iCiv)
        if pCiv.getStateReligion() == Religion.CATHOLICISM and pCiv.isAlive():
            iUnitNumber = getNumUnitsSent(iCiv)
            if iUnitNumber > 0:
                # the leader already got exp points through the Crusade it
                if iCiv == iPlayer:
                    # if Jerusalem is held by a Christian civ (maybe some cities in the Levant should be enough) (maybe there should be a unit in the Levant from this Crusade)
                    pCity = gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity()
                    pPlayer = gc.getPlayer(pCity.getOwner())
                    if pPlayer.getStateReligion() == Religion.CATHOLICISM:
                        pCiv.changeFaith(1 * iUnitNumber)
                        # add relics in the capital
                        capital = pCiv.getCapitalCity()
                        iCapitalX = capital.getX()
                        iCapitalY = capital.getY()
                        pCiv.initUnit(
                            Unit.HOLY_RELIC,
                            iCapitalX,
                            iCapitalY,
                            UnitAITypes.NO_UNITAI,
                            DirectionTypes.DIRECTION_SOUTH,
                        )
                        if iCiv == iHuman:
                            message(
                                iHuman,
                                text("TXT_KEY_CRUSADE_NEW_RELIC"),
                                sound="AS2D_UNIT_BUILD_UNIQUE_UNIT",
                                button=gc.getUnitInfo(Unit.HOLY_RELIC).getButton(),
                                color=MessageData.GREEN,
                                location=(iCapitalX, iCapitalY),
                            )
                        if iUnitNumber > 3 and percentage_chance(80, strict=True):
                            pCiv.initUnit(
                                Unit.HOLY_RELIC,
                                iCapitalX,
                                iCapitalY,
                                UnitAITypes.NO_UNITAI,
                                DirectionTypes.DIRECTION_SOUTH,
                            )
                        if iUnitNumber > 9 and percentage_chance(80, strict=True):
                            pCiv.initUnit(
                                Unit.HOLY_RELIC,
                                iCapitalX,
                                iCapitalY,
                                UnitAITypes.NO_UNITAI,
                                DirectionTypes.DIRECTION_SOUTH,
                            )
                # all other civs get experience points as well
                else:
                    if iCiv == iHuman:
                        message(
                            iHuman,
                            text("TXT_KEY_CRUSADE_CRUSADERS_ARRIVED_HOME"),
                            color=MessageData.GREEN,
                        )
                    pCiv.changeCombatExperience(12 * iUnitNumber)
                    # if Jerusalem is held by a Christian civ (maybe some cities in the Levant should be enough) (maybe there should be a unit in the Levant from this Crusade)
                    pCity = gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity()
                    pPlayer = gc.getPlayer(pCity.getOwner())
                    if pPlayer.getStateReligion() == Religion.CATHOLICISM:
                        pCiv.changeFaith(1 * iUnitNumber)
                        # add relics in the capital
                        capital = pCiv.getCapitalCity()
                        iCapitalX = capital.getX()
                        iCapitalY = capital.getY()
                        # safety check, game crashes if it wants to create a unit in a non-existing city
                        if capital.getName():
                            if percentage_chance(80, strict=True):
                                pCiv.initUnit(
                                    Unit.HOLY_RELIC,
                                    iCapitalX,
                                    iCapitalY,
                                    UnitAITypes.NO_UNITAI,
                                    DirectionTypes.DIRECTION_SOUTH,
                                )
                                if iCiv == iHuman:
                                    message(
                                        iHuman,
                                        text("TXT_KEY_CRUSADE_NEW_RELIC"),
                                        sound="AS2D_UNIT_BUILD_UNIQUE_UNIT",
                                        button=gc.getUnitInfo(Unit.HOLY_RELIC).getButton(),
                                        color=MessageData.GREEN,
                                        location=(iCapitalX, iCapitalY),
                                    )
                            if iUnitNumber > 3 and percentage_chance(60, strict=True):
                                pCiv.initUnit(
                                    Unit.HOLY_RELIC,
                                    iCapitalX,
                                    iCapitalY,
                                    UnitAITypes.NO_UNITAI,
                                    DirectionTypes.DIRECTION_SOUTH,
                                )
                            if iUnitNumber > 9 and percentage_chance(60, strict=True):
                                pCiv.initUnit(
                                    Unit.HOLY_RELIC,
                                    iCapitalX,
                                    iCapitalY,
                                    UnitAITypes.NO_UNITAI,
                                    DirectionTypes.DIRECTION_SOUTH,
                                )


# Absinthe: called from CvRFCEventHandler.onCityAcquired
def success(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    if not hasSucceeded():
        pPlayer.changeGoldenAgeTurns(gc.getPlayer(iPlayer).getGoldenAgeLength())
        setSucceeded()
        for plot in plots().surrounding(CITIES[City.JERUSALEM]).entities():
            convertPlotCulture(plot, iPlayer, 100, False)


# Absinthe: pilgrims in Jerusalem if it's held by a Catholic civ
def checkPlayerTurn(iGameTurn, iPlayer):
    if iGameTurn % 3 == 1:  # checked every 3rd turn
        pCity = gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity()
        if pCity.getOwner() == iPlayer:
            pPlayer = gc.getPlayer(iPlayer)
            if pPlayer.getStateReligion() == Religion.CATHOLICISM:
                # possible population gain, chance based on the current size
                iRandom = rand(10)
                if (
                    1 + pCity.getPopulation()
                ) <= iRandom:  # 1 -> 80%, 2 -> 70%, 3 -> 60% ...  7 -> 20%, 8 -> 10%, 9+ -> 0%
                    pCity.changePopulation(1)
                    message_if_human(
                        iPlayer,
                        text("TXT_KEY_CRUSADE_JERUSALEM_PILGRIMS"),
                        color=MessageData.GREEN,
                        location=pCity,
                    )
                    # spread Catholicism if not present
                    if not pCity.isHasReligion(Religion.CATHOLICISM):
                        pCity.setHasReligion(Religion.CATHOLICISM, True, True, False)


def doDefensiveCrusade(iGameTurn):
    if iGameTurn < getDefensiveCrusadeLast() + 15:  # wait 15 turns between defensive crusades
        return
    if iGameTurn % 5 != rand(5):
        return
    if percentage_chance(33, strict=True):
        return
    lPotentials = [
        iPlayer
        for iPlayer in civilizations().main().ids()
        if canDefensiveCrusade(iPlayer, iGameTurn)
    ]
    if lPotentials:
        pPope = gc.getPlayer(Civ.POPE)
        weights = []
        for iPlayer in lPotentials:
            iCatholicFaith = 0
            pPlayer = gc.getPlayer(iPlayer)
            # while faith points matter more, diplomatic relations are also very important
            iCatholicFaith += pPlayer.getFaith()
            iCatholicFaith += 3 * max(0, pPope.AI_getAttitude(iPlayer))
            if iCatholicFaith > 0:
                weights.append(iCatholicFaith)
            else:
                weights.append(0)

        iChosenPlayer = choice(lPotentials, weights)
        if iChosenPlayer == human():
            callDefensiveCrusadeHuman()
        else:
            callDefensiveCrusadeAI(iChosenPlayer)
        setDefensiveCrusadeLast(iGameTurn)


def canDefensiveCrusade(iPlayer, iGameTurn):
    pPlayer = gc.getPlayer(iPlayer)
    teamPlayer = gc.getTeam(pPlayer.getTeam())
    # only born, flipped and living Catholics can defensive crusade
    if (
        (iGameTurn < civilization(iPlayer).date.birth + 5)
        or not pPlayer.isAlive()
        or pPlayer.getStateReligion() != Religion.CATHOLICISM
    ):
        return False
    # need to have open borders with the Pope
    if not teamPlayer.isOpenBorders(gc.getPlayer(Civ.POPE).getTeam()):
        return False

    tPlayerDCMap = tDefensiveCrusadeMap[iPlayer]
    # Can defensive crusade if at war with a non-catholic/orthodox enemy, enemy is not a vassal of a catholic/orthodox civ and has a city in the defensive crusade map
    for iEnemy in civilizations().main().ids():
        pEnemy = gc.getPlayer(iEnemy)
        if (
            teamPlayer.isAtWar(pEnemy.getTeam())
            and civilization(iEnemy).date.birth + 10 < iGameTurn
        ):
            if isOrMasterChristian(iEnemy):
                continue
            for pCity in cities().owner(iEnemy).entities():
                if PROVINCES_MAP[pCity.getY()][pCity.getX()] in tPlayerDCMap:
                    return True
    return False


def callDefensiveCrusadeHuman():
    event_popup(
        7625,
        text("TXT_KEY_CRUSADE_DEFENSIVE_PROPOSAL_POPUP"),
        text("TXT_KEY_CRUSADE_DEFENSIVE_PROPOSAL"),
        [
            text("TXT_KEY_CRUSADE_DEFENSIVE_PROPOSAL_YES"),
            text("TXT_KEY_CRUSADE_DEFENSIVE_PROPOSAL_NO"),
        ],
    )


def callDefensiveCrusadeAI(iPlayer):
    if player().isExisting():
        if (
            team().canContact(teamtype(iPlayer))
            or player().getStateReligion() == Religion.CATHOLICISM
        ):  # as you have contact with the Pope by default
            sText = text("TXT_KEY_CRUSADE_DEFENSIVE_AI_MESSAGE") + " " + player(iPlayer).getName()
            message(human(), sText, force=True, color=MessageData.LIGHT_RED)
    makeDefensiveCrusadeUnits(iPlayer)
    player(iPlayer).changeFaith(-min(2, player(iPlayer).getFaith()))


def eventApply7625(popupReturn):
    iDecision = popupReturn.getButtonClicked()
    if iDecision == 0:
        makeDefensiveCrusadeUnits(human())
        player().changeFaith(-min(2, player().getFaith()))
    # else:
    # #pHuman.changeFaith( - min( 1, pHuman.getFaith() ) )
    # pass


def makeDefensiveCrusadeUnits(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    iFaith = pPlayer.getFaith()
    iBestInfantry = getDefensiveCrusadeBestInfantry(iPlayer)
    iBestCavalry = getDefensiveCrusadeBestCavalry(iPlayer)
    pCapital = pPlayer.getCapitalCity()
    if pCapital:
        iX = pCapital.getX()
        iY = pCapital.getY()
    else:
        city = cities().owner(iPlayer).random_entry()
        if city is not None:
            iX = city.getX()
            iY = city.getY()
        else:
            return

    # Absinthe: interface message for the player
    if gc.getPlayer(iPlayer).isHuman():
        message(
            iPlayer,
            text("TXT_KEY_CRUSADE_DEFENSIVE_HUMAN_MESSAGE"),
            color=MessageData.GREEN,
            location=(iX, iY),
        )

    pPlayer.initUnit(
        iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH
    )
    pPlayer.initUnit(
        iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH
    )

    # smaller Empires need a bit more help
    if pPlayer.getNumCities() < 6:
        if iBestCavalry == Unit.KNIGHT:
            if percentage_chance(30, strict=True):
                pPlayer.initUnit(
                    Unit.BURGUNDIAN_PALADIN,
                    iX,
                    iY,
                    UnitAITypes.UNITAI_ATTACK,
                    DirectionTypes.DIRECTION_SOUTH,
                )
            else:
                pPlayer.initUnit(
                    iBestCavalry,
                    iX,
                    iY,
                    UnitAITypes.UNITAI_ATTACK,
                    DirectionTypes.DIRECTION_SOUTH,
                )
        else:
            pPlayer.initUnit(
                iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH
            )

    if iFaith > 4:
        pPlayer.initUnit(
            iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH
        )
    if iFaith > 11:
        if iBestCavalry == Unit.KNIGHT:
            if percentage_chance(30, strict=True):
                pPlayer.initUnit(
                    Unit.BURGUNDIAN_PALADIN,
                    iX,
                    iY,
                    UnitAITypes.UNITAI_ATTACK,
                    DirectionTypes.DIRECTION_SOUTH,
                )
            else:
                pPlayer.initUnit(
                    iBestCavalry,
                    iX,
                    iY,
                    UnitAITypes.UNITAI_ATTACK,
                    DirectionTypes.DIRECTION_SOUTH,
                )
        else:
            pPlayer.initUnit(
                iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH
            )
    if iFaith > 20:
        pPlayer.initUnit(
            iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH
        )
    if iFaith > 33:
        pPlayer.initUnit(
            iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH
        )

    # extra units for the AI, it is dumb anyway
    if not iPlayer == human():
        pPlayer.initUnit(
            iBestInfantry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH
        )
        pPlayer.initUnit(
            iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH
        )
        if iBestCavalry == Unit.KNIGHT:
            if percentage_chance(30, strict=True):
                pPlayer.initUnit(
                    Unit.BURGUNDIAN_PALADIN,
                    iX,
                    iY,
                    UnitAITypes.UNITAI_ATTACK,
                    DirectionTypes.DIRECTION_SOUTH,
                )
            else:
                pPlayer.initUnit(
                    iBestCavalry,
                    iX,
                    iY,
                    UnitAITypes.UNITAI_ATTACK,
                    DirectionTypes.DIRECTION_SOUTH,
                )
        else:
            pPlayer.initUnit(
                iBestCavalry, iX, iY, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH
            )


def getDefensiveCrusadeBestInfantry(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    lUnits = [
        Unit.GRENADIER,
        Unit.MACEMAN,
        Unit.LONG_SWORDSMAN,
        Unit.SWORDSMAN,
    ]
    for iUnit in lUnits:
        if pPlayer.canTrain(getUniqueUnit(iPlayer, iUnit), False, False):
            return getUniqueUnit(iPlayer, iUnit)
    return getUniqueUnit(iPlayer, Unit.AXEMAN)


def getDefensiveCrusadeBestCavalry(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    lUnits = [
        Unit.CUIRASSIER,
        Unit.KNIGHT,
        Unit.HEAVY_LANCER,
        Unit.LANCER,
    ]
    for iUnit in lUnits:
        if pPlayer.canTrain(getUniqueUnit(iPlayer, iUnit), False, False):
            return getUniqueUnit(iPlayer, iUnit)
    return getUniqueUnit(iPlayer, Unit.SCOUT)


def do1200ADCrusades():
    setCrusadeInit(0, year(1096))
    setCrusadeInit(1, year(1147))
    setCrusadeInit(2, year(1187))


def isOrMasterChristian(iPlayer):
    pPlayer = gc.getPlayer(iPlayer)
    iReligion = pPlayer.getStateReligion()
    if iReligion in [Religion.CATHOLICISM, Religion.ORTHODOXY]:
        return True
    iMaster = getMaster(iPlayer)
    if iMaster != -1:
        iMasterReligion = gc.getPlayer(iMaster).getStateReligion()
        if iMasterReligion in [Religion.CATHOLICISM, Religion.ORTHODOXY]:
            return True
    return False
