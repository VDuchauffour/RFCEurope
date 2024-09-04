from CvPythonExtensions import *
from Consts import MessageData
from Core import (
    city,
    civilization,
    civilizations,
    event_popup,
    human,
    location,
    make_crusade_unit,
    make_crusade_units,
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
from Events import handler, popup_handler
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


def addSelectedUnit(iUnitPlace):
    data.crusade_selected_units[iUnitPlace] += 1


def setSelectedUnit(iUnitPlace, iNewNumber):
    data.crusade_selected_units[iUnitPlace] = iNewNumber


def getSelectedUnit(iUnitPlace):
    return data.crusade_selected_units[iUnitPlace]


def getActiveCrusade(iGameTurn):
    for i in range(NUM_CRUSADES):
        iInit = data.crusade_status[i]
        if iInit > -1 and iInit + 9 > iGameTurn:
            return i
    return -1


def getVotingPower(iCiv):
    return data.players[iCiv].voting_power


def initVotePopup():
    iHuman = human()
    pHuman = player(iHuman)
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


@popup_handler(7617)
def event7617(playerID, netUserData, popupReturn):
    pass


def informLeaderPopup():
    event_popup(
        7617,
        text("TXT_KEY_CRUSADE_LEADER_POPUP"),
        player(data.leader_of_crusade).getName() + text("TXT_KEY_CRUSADE_LEAD"),
        [text("TXT_KEY_CRUSADE_OK")],
    )


@popup_handler(7618)
def HumanVotePopup(playerID, netUserData, popupReturn):
    if popupReturn.getButtonClicked() == 0:
        data.votes_for_favorite += getVotingPower(human())
    else:
        data.votes_for_powerful += getVotingPower(human())


def voteHumanPopup():
    favorite_txt = (
        player(data.favorite_crusader).getName()
        + " ("
        + player(data.favorite_crusader).getCivilizationShortDescription(0)
        + ")"
    )
    powerful_txt = (
        player(data.powerful_crusader).getName()
        + " ("
        + player(data.powerful_crusader).getCivilizationShortDescription(0)
        + ")"
    )
    event_popup(
        7618,
        text("TXT_KEY_CRUSADE_VOTE_POPUP"),
        text("TXT_KEY_CRUSADE_VOTE"),
        [favorite_txt, powerful_txt],
    )


@popup_handler(7619)
def HumanDeviate(playerID, netUserData, popupReturn):
    if popupReturn.getButtonClicked() == 0:
        player().changeGold(-player().getGold() / 3)
        data.leader_of_crusade = human()
        data.crusade_power /= 2
        deviateNewTargetPopup()
    else:
        data.target = CITIES[City.JERUSALEM]
        startCrusade()


def deviateHumanPopup():
    iCost = player(human()).getGold() / 3
    sString = (
        text("TXT_KEY_CRUSADE_RICHEST")
        + text("TXT_KEY_CRUSADE_COST")
        + " "
        + str(iCost)
        + " "
        + text("TXT_KEY_CRUSADE_GOLD")
        + player(data.leader_of_crusade).getName()
        + " "
        + text("TXT_KEY_CRUSADE_CURRENT_LEADER")
    )
    event_popup(
        7619,
        text("TXT_KEY_CRUSADE_DEVIATE"),
        sString,
        [text("TXT_KEY_CRUSADE_DECIDE_WEALTH"), text("TXT_KEY_CRUSADE_DECIDE_FAITH")],
    )


@popup_handler(7620)
def ChoseNewCrusadeTarget(playerID, netUserData, popupReturn):
    iDecision = popupReturn.getButtonClicked()
    if iDecision == 0:
        data.target = CITIES[City.JERUSALEM]
        startCrusade()
        return
    iTargets = 0
    for iCiv in civilizations().majors().ids():
        if data.players[iCiv].deviate_targets:
            iTargets += 1
        if iTargets == iDecision:
            data.target = location(player(iCiv).getCapitalCity())
            iDecision = -2

    startCrusade()


def deviateNewTargetPopup():
    lTargetList = []
    lTargetList.append(
        gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity().getName()
        + " ("
        + player(
            gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity().getOwner()
        ).getCivilizationAdjective(0)
        + ")"
    )
    for iPlayer in civilizations().majors().ids():
        pPlayer = player(iPlayer)
        if (
            iPlayer == Civ.POPE
            or pPlayer.getStateReligion() == Religion.CATHOLICISM
            or not pPlayer.isAlive()
        ):
            data.players[iPlayer].deviate_targets = False
        else:
            data.players[iPlayer].deviate_targets = True
            lTargetList.append(
                pPlayer.getCapitalCity().getName()
                + " ("
                + pPlayer.getCivilizationAdjective(0)
                + ")"
            )
    event_popup(7620, text("TXT_KEY_CRUSADE_CORRUPT"), text("TXT_KEY_CRUSADE_TARGET"), lTargetList)


@popup_handler(7621)
def event7621(playerID, netUserData, popupReturn):
    pass


def underCrusadeAttackPopup(sCityName, iLeader):
    sText = text(
        "TXT_KEY_CRUSADE_UNDER_ATTACK1",
        player(iLeader).getCivilizationAdjective(0),
        player(iLeader).getName(),
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
            if data.crusade_status[i] < 0:
                data.crusade_status[i] = 0
        # Absinthe: reset sent unit counter after the Crusades are over (so it won't give Company benefits forever based on the last one)
        for iPlayer in civilizations().majors().ids():
            data.players[iPlayer].num_units_sent = 0


@handler("BeginGameTurn")
def checkTurn(iGameTurn):
    if data.crusade_to_return > -1:
        freeCrusaders(data.crusade_to_return)
        data.crusade_to_return = -1

    # Absinthe: crusade date - 5 means the exact time for the arrival
    if iGameTurn == year(1096) - 5:  # First Crusade arrives in 1096AD
        data.crusade_status[0] = -1
    elif (
        iGameTurn >= year(1147) - 7 and data.crusade_status[0] > 0 and data.crusade_status[1] == -2
    ):  # Crusade of 1147AD, little earlier (need to be more than 9 turns between crusades)
        data.crusade_status[1] = -1  # turn 176
    elif (
        iGameTurn >= year(1187) - 8 and data.crusade_status[1] > 0 and data.crusade_status[2] == -2
    ):  # Crusade of 1187AD, little earlier (need to be more than 9 turns between crusades)
        data.crusade_status[2] = -1  # turn 187
    elif (
        iGameTurn >= year(1202) - 4 and data.crusade_status[2] > 0 and data.crusade_status[3] == -2
    ):  # Crusade of 1202AD, little later (need to be more than 9 turns between crusades)
        data.crusade_status[3] = -1  # turn 197
    elif (
        iGameTurn >= year(1229) - 3 and data.crusade_status[3] > 0 and data.crusade_status[4] == -2
    ):  # Crusade of 1229AD, little later (need to be more than 9 turns between crusades)
        data.crusade_status[4] = -1  # turn 207
    elif (
        iGameTurn >= year(1271) - 5 and data.crusade_status[4] > 0 and data.crusade_status[5] == -2
    ):  # Crusade of 1270AD
        data.crusade_status[5] = -1  # turn 219

    # Start of Defensive Crusades: indulgences for the Reconquista given by the Catholic Church in 1000AD
    if iGameTurn == year(1000):
        data.is_defending_crusade_active = True

    # End of Defensive Crusades: no more defensive crusades after Protestantism is founded
    if data.is_defending_crusade_active:
        if gc.getGame().isReligionFounded(Religion.PROTESTANTISM):
            data.is_defending_crusade_active = False

    if data.is_defending_crusade_active:
        doDefensiveCrusade(iGameTurn)

    checkToStart(iGameTurn)

    iActiveCrusade = getActiveCrusade(iGameTurn)
    if iActiveCrusade > -1:
        iStartDate = data.crusade_status[iActiveCrusade]
        if iStartDate == iGameTurn:
            doParticipation(iGameTurn)

        elif iStartDate + 1 == iGameTurn:
            computeVotingPower(iGameTurn)
            setCrusaders()
            for i in range(8):
                setSelectedUnit(i, 0)
            for iPlayer in civilizations().majors().ids():
                # Absinthe: first we set all civs' unit counter to 0, then send the new round of units
                data.players[iPlayer].num_units_sent = 0
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
            if data.richest_catholic == human():
                decideDeviateHuman()
            else:
                decideDeviateAI()

        elif iStartDate + 5 == iGameTurn:
            if not anyParticipate():
                return
            crusadeArrival(iActiveCrusade)

        elif iStartDate + 8 == iGameTurn:
            data.crusade_to_return = data.leader_of_crusade
            returnCrusaders()


def checkToStart(iGameTurn):
    # if Jerusalem is Islamic or Pagan, Crusade has been initialized and it has been at least 5 turns since the last crusade and there are any Catholics, begin crusade
    pJPlot = gc.getMap().plot(*CITIES[City.JERUSALEM])
    for i in range(NUM_CRUSADES):  # check the Crusades
        if data.crusade_status[i] == -1:  # if this one is to start
            if (
                pJPlot.isCity() and anyCatholic()
            ):  # if there is Jerusalem and there are any Catholics
                # Sedna17 -- allowing crusades against independent Jerusalem
                iVictim = pJPlot.getPlotCity().getOwner()
                if isOrMasterChristian(iVictim):
                    break
                if i == 0 or (
                    data.crusade_status[i - 1] > -1 and data.crusade_status[i - 1] + 9 < iGameTurn
                ):
                    data.crusade_status[i] = iGameTurn


def anyCatholic():
    return civilizations().main().any(lambda c: c.has_state_religion(Religion.CATHOLICISM))


def anyParticipate():
    for i in civilizations().main().ids():
        if getVotingPower(i) > 0:
            return True
    return False


@popup_handler(7616)
def CrusadeInitVoteEvent(playerID, netUserData, popupReturn):
    iHuman = human()
    if popupReturn.getButtonClicked() == 0:
        data.is_participate_to_crusade = True
        player(iHuman).setIsCrusader(True)
    elif popupReturn.getButtonClicked() == 1 or popupReturn.getButtonClicked() == 2:
        data.is_participate_to_crusade = False
        pPlayer = player(iHuman)
        pPlayer.setIsCrusader(False)
        pPlayer.changeFaith(-min(5, pPlayer.getFaith()))
        message(
            iHuman, text("TXT_KEY_CRUSADE_DENY_FAITH"), force=True, color=MessageData.LIGHT_RED
        )
        player(Civ.POPE).AI_changeMemoryCount(iHuman, MemoryTypes.MEMORY_REJECTED_DEMAND, 2)
        # Absinthe: some units from Chivalric Orders might leave you nevertheless
        for pUnit in units.owner(iHuman).entities():
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
        data.is_participate_to_crusade = False
        pPlayer = player(iHuman)
        pPlayer.setIsCrusader(False)
        pPope = player(Civ.POPE)
        iActiveCrusade = getActiveCrusade(turn())
        iBribe = 200 + 50 * iActiveCrusade
        pPope.changeGold(iBribe)
        pPlayer.changeGold(-iBribe)
        player(Civ.POPE).AI_changeMemoryCount(iHuman, MemoryTypes.MEMORY_REJECTED_DEMAND, 1)


def doParticipation(iGameTurn):
    iHuman = human()
    if civilization(iHuman).date.birth < iGameTurn:
        pHuman = player(iHuman)
        if pHuman.getStateReligion() != Religion.CATHOLICISM:
            data.is_participate_to_crusade = False
            message(
                iHuman, text("TXT_KEY_CRUSADE_CALLED"), force=True, color=MessageData.LIGHT_RED
            )
        else:
            initVotePopup()
    else:
        data.is_participate_to_crusade = False


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
    data.favorite_crusader = iFavorite

    iPowerful = iFavorite
    iPower = getVotingPower(iPowerful)

    for i in civilizations().main().ids():
        if getVotingPower(i) > iPower or (iPowerful == iFavorite and getVotingPower(i) > 0):
            iPowerful = i
            iPower = getVotingPower(iPowerful)

    if iPowerful == iFavorite:
        data.powerful_crusader = -1
    else:
        data.powerful_crusader = iPowerful


def computeVotingPower(iGameTurn):
    iTmJerusalem = player(
        gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity().getOwner()
    ).getTeam()
    for iPlayer in civilizations().majors().ids():
        pPlayer = player(iPlayer)
        if (
            civilization(iPlayer).date.birth > iGameTurn
            or not pPlayer.isAlive()
            or pPlayer.getStateReligion() != Religion.CATHOLICISM
            or gc.getTeam(pPlayer.getTeam()).isVassal(iTmJerusalem)
        ):
            data.players[iPlayer].voting_power = 0
        else:
            # We use the (similarly named) getVotingPower from CvPlayer.cpp to determine a vote value for a given State Religion, but it's kinda strange
            # Will leave it this way for now, but might be a good idea to improve it at some point
            data.players[iPlayer].voting_power = pPlayer.getVotingPower(Religion.CATHOLICISM)

    # No votes from the human player if he/she won't participate (AI civs will always participate)
    if not data.is_participate_to_crusade:
        data.players[human()].voting_power = 0

    # The Pope has more votes (Rome is small anyway)
    data.players[Civ.POPE].voting_power *= 5 / 4

    iPower = 0
    for iPlayer in civilizations().majors().ids():
        iPower += getVotingPower(iPlayer)

    data.crusade_power = iPower
    # Note that voting power is increased after this (but before the actual vote) for each sent unit by 2


def setCrusaders():
    for iPlayer in civilizations().majors().ids():
        if not iPlayer == human() and getVotingPower(iPlayer) > 0:
            player(iPlayer).setIsCrusader(True)


def sendUnits(iPlayer):
    pPlayer = player(iPlayer)
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
    data.players[iOwner].voting_power += 2
    data.players[iOwner].num_units_sent += 1  # Absinthe: counter for sent units per civ
    # Absinthe: faith point boost for each sent unit (might get some more on successful Crusade):
    player(iOwner).changeFaith(1)
    message(
        pUnit,
        text("TXT_KEY_CRUSADE_LEAVE") + " " + pUnit.getName(),
        sound="AS2D_BUILD_CATHOLIC",
        color=MessageData.ORANGE,
        location=location(pUnit),
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
    if data.powerful_crusader == -1:
        data.leader_of_crusade = data.favorite_crusader
        if data.is_participate_to_crusade:
            informLeaderPopup()
        elif player().isExisting():
            message(
                human(),
                player(data.leader_of_crusade).getName() + text("TXT_KEY_CRUSADE_LEAD"),
                force=True,
                color=MessageData.LIGHT_RED,
            )
        return

    iFavorite = data.favorite_crusader
    iPowerful = data.powerful_crusader
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

    data.votes_for_favorite = iFavorVotes
    data.votes_for_powerful = iPowerVotes


def voteForCandidatesHuman():
    if data.is_participate_to_crusade and not data.powerful_crusader == -1:
        voteHumanPopup()


def selectVoteWinner():
    if data.votes_for_powerful > data.votes_for_favorite:
        data.leader_of_crusade = data.powerful_crusader
    else:
        data.leader_of_crusade = data.favorite_crusader

    if data.is_participate_to_crusade:
        informLeaderPopup()
    elif player().isExisting():
        message(
            human(),
            player(data.leader_of_crusade).getName() + text("TXT_KEY_CRUSADE_LEAD"),
            force=True,
            color=MessageData.LIGHT_RED,
        )


def decideTheRichestCatholic(iActiveCrusade):
    # The First Crusade cannot be deviated
    if iActiveCrusade == 0:
        data.richest_catholic = -1
        return

    iRichest = -1
    iMoney = 0
    for i in civilizations().main().ids():
        if getVotingPower(i) > 0:
            pPlayer = player(i)
            iPlayerMoney = pPlayer.getGold()
            if iPlayerMoney > iMoney:
                iRichest = i
                iMoney = iPlayerMoney

    if iRichest != Civ.POPE:
        data.richest_catholic = iRichest
    else:
        data.richest_catholic = -1


def decideDeviateHuman():
    deviateHumanPopup()


def decideDeviateAI():
    iRichest = data.richest_catholic
    bStolen = False
    if iRichest in [Civ.VENECIA, Civ.GENOA]:
        pByzantium = player(Civ.BYZANTIUM)
        if pByzantium.isAlive():
            # Only if the potential attacker is not vassal of the target
            iTeamByzantium = pByzantium.getTeam()
            pRichest = player(iRichest)
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
        pCordoba = player(Civ.CORDOBA)
        if pCordoba.isAlive():
            # Only if the potential attacker is not vassal of the target
            iTeamCordoba = pCordoba.getTeam()
            pRichest = player(iRichest)
            pTeamRichest = gc.getTeam(pRichest.getTeam())
            if not pTeamRichest.isVassal(iTeamCordoba):
                # Only if Cordoba is Muslim and not a vassal
                bIsNotAVassal = not isAVassal(Civ.CORDOBA)
                if pCordoba.getStateReligion() == Religion.ISLAM and bIsNotAVassal:
                    crusadeStolenAI(iRichest, Civ.CORDOBA)
                    bStolen = True
    elif iRichest in [Civ.HUNGARY, Civ.POLAND, Civ.AUSTRIA]:
        pTurkey = player(Civ.OTTOMAN)
        if pTurkey.isAlive():
            # Only if the potential attacker is not vassal of the target
            iTeamTurkey = pTurkey.getTeam()
            pRichest = player(iRichest)
            pTeamRichest = gc.getTeam(pRichest.getTeam())
            if not pTeamRichest.isVassal(iTeamTurkey):
                # Only if the Ottomans are Muslim and not a vassal
                bIsNotAVassal = not isAVassal(Civ.OTTOMAN)
                if pTurkey.getStateReligion() == Religion.ISLAM and bIsNotAVassal:
                    crusadeStolenAI(iRichest, Civ.OTTOMAN)
                    bStolen = True

    if not bStolen:
        data.target = CITIES[City.JERUSALEM]

    startCrusade()


def crusadeStolenAI(iNewLeader, iNewTarget):
    data.leader_of_crusade = iNewLeader
    pLeader = player(iNewLeader)
    if player().isExisting():
        message(
            human(),
            pLeader.getName() + text("TXT_KEY_CRUSADE_DEVIATED"),
            color=MessageData.LIGHT_RED,
        )
    pLeader.setGold(2 * pLeader.getGold() / 3)
    data.target = location(player(iNewTarget).getCapitalCity())
    data.crusade_power /= 2


def startCrusade():
    iHuman = human()
    iLeader = data.leader_of_crusade
    pTargetCity = city(data.target)
    iTargetPlayer = pTargetCity.getOwner()
    # Absinthe: in case the Crusader civ has been destroyed
    if not player(iLeader).isAlive():
        returnCrusaders()
        return
    # Target city can change ownership during the voting
    if player(iTargetPlayer).getStateReligion() == Religion.CATHOLICISM:
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
            player(iLeader).getCivilizationAdjectiveKey(),
            player(iLeader).getName(),
            player(iTargetPlayer).getCivilizationAdjectiveKey(),
            sCityName,
        )
        message(iHuman, sText, color=MessageData.LIGHT_RED)

    # Absinthe: proper war declaration checks
    teamLeader = gc.getTeam(player(iLeader).getTeam())
    iTeamTarget = player(iTargetPlayer).getTeam()
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
    data.leader_of_crusade = -1
    for i in civilizations().majors().ids():
        player(i).setIsCrusader(False)


def crusadeArrival(iActiveCrusade):
    iTX, iTY = data.target
    iChosenX = -1
    iChosenY = -1

    # if the leader has been destroyed, cancel the Crusade
    iLeader = data.leader_of_crusade
    if iLeader == -1 or not player(iLeader).isAlive():
        returnCrusaders()
        return

    # if the target is Jerusalem, and in the mean time it has been captured by an Orthodox or Catholic player (or the owner of Jerusalem converted to a Christian religion), cancel the Crusade
    if (iTX, iTY) == CITIES[City.JERUSALEM]:
        pPlot = gc.getMap().plot(*CITIES[City.JERUSALEM])
        if pPlot.isCity():
            iVictim = pPlot.getPlotCity().getOwner()
            if iVictim < civilizations().majors().len():
                iReligion = player(iVictim).getStateReligion()
                if iReligion in [Religion.CATHOLICISM, Religion.ORTHODOXY]:
                    return

    # if not at war with the owner of the city, declare war
    pPlot = gc.getMap().plot(iTX, iTY)
    if pPlot.isCity():
        iVictim = pPlot.getPlotCity().getOwner()
        if iVictim != iLeader and player(iVictim).getStateReligion() != Religion.CATHOLICISM:
            teamLeader = gc.getTeam(player(iLeader).getTeam())
            iTeamVictim = player(iVictim).getTeam()
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
        plots.surrounding((iTX, iTY))
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
                iLeader,
                text("TXT_KEY_CRUSADE_ARRIVAL", sCityName) + "!",
                color=MessageData.GREEN,
                location=(iChosenX, iChosenY),
            )
    else:
        returnCrusaders()


def crusadeMakeUnits(tPlot, iActiveCrusade):
    iLeader = data.leader_of_crusade
    teamLeader = gc.getTeam(player(iLeader).getTeam())
    iTX, iTY = data.target
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
    for pUnit in units.owner(iPlayer).entities():
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
                message(
                    iPlayer,
                    text("TXT_KEY_CRUSADE_CRUSADERS_RETURNING_HOME") + " " + pUnit.getName(),
                    color=MessageData.LIME,
                )

    # benefits for the other participants on Crusade return - Faith points, GG points, Relics
    for iCiv in civilizations().main().ids():
        pCiv = player(iCiv)
        if pCiv.getStateReligion() == Religion.CATHOLICISM and pCiv.isAlive():
            iUnitNumber = data.players[iCiv].num_units_sent
            if iUnitNumber > 0:
                # the leader already got exp points through the Crusade it
                if iCiv == iPlayer:
                    # if Jerusalem is held by a Christian civ (maybe some cities in the Levant should be enough) (maybe there should be a unit in the Levant from this Crusade)
                    pCity = gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity()
                    pPlayer = player(pCity.getOwner())
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
                        message(
                            iCiv,
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
                    message(
                        iCiv,
                        text("TXT_KEY_CRUSADE_CRUSADERS_ARRIVED_HOME"),
                        color=MessageData.GREEN,
                    )
                    pCiv.changeCombatExperience(12 * iUnitNumber)
                    # if Jerusalem is held by a Christian civ (maybe some cities in the Levant should be enough) (maybe there should be a unit in the Levant from this Crusade)
                    pCity = gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity()
                    pPlayer = player(pCity.getOwner())
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
                                message(
                                    iCiv,
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
    pPlayer = player(iPlayer)
    if not data.is_succesful_crusade:
        pPlayer.changeGoldenAgeTurns(player(iPlayer).getGoldenAgeLength())
        data.is_succesful_crusade = True
        for plot in plots.surrounding(CITIES[City.JERUSALEM]).entities():
            convertPlotCulture(plot, iPlayer, 100, False)


@handler("BeginPlayerTurn")
def checkPlayerTurn(iGameTurn, iPlayer):
    # Absinthe: pilgrims in Jerusalem if it's held by a Catholic civ
    if iGameTurn % 3 == 1:  # checked every 3rd turn
        pCity = gc.getMap().plot(*CITIES[City.JERUSALEM]).getPlotCity()
        if pCity.getOwner() == iPlayer:
            pPlayer = player(iPlayer)
            if pPlayer.getStateReligion() == Religion.CATHOLICISM:
                # possible population gain, chance based on the current size
                iRandom = rand(10)
                if (
                    1 + pCity.getPopulation()
                ) <= iRandom:  # 1 -> 80%, 2 -> 70%, 3 -> 60% ...  7 -> 20%, 8 -> 10%, 9+ -> 0%
                    pCity.changePopulation(1)
                    message(
                        iPlayer,
                        text("TXT_KEY_CRUSADE_JERUSALEM_PILGRIMS"),
                        color=MessageData.GREEN,
                        location=pCity,
                    )
                    # spread Catholicism if not present
                    if not pCity.isHasReligion(Religion.CATHOLICISM):
                        pCity.setHasReligion(Religion.CATHOLICISM, True, True, False)


def doDefensiveCrusade(iGameTurn):
    if iGameTurn < data.last_defensive_crusade + 15:  # wait 15 turns between defensive crusades
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
        pPope = player(Civ.POPE)
        weights = []
        for iPlayer in lPotentials:
            iCatholicFaith = 0
            pPlayer = player(iPlayer)
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
        data.last_defensive_crusade = iGameTurn


def canDefensiveCrusade(iPlayer, iGameTurn):
    pPlayer = player(iPlayer)
    teamPlayer = gc.getTeam(pPlayer.getTeam())
    # only born, flipped and living Catholics can defensive crusade
    if (
        (iGameTurn < civilization(iPlayer).date.birth + 5)
        or not pPlayer.isAlive()
        or pPlayer.getStateReligion() != Religion.CATHOLICISM
    ):
        return False
    # need to have open borders with the Pope
    if not teamPlayer.isOpenBorders(player(Civ.POPE).getTeam()):
        return False

    tPlayerDCMap = tDefensiveCrusadeMap[iPlayer]
    # Can defensive crusade if at war with a non-catholic/orthodox enemy, enemy is not a vassal of a catholic/orthodox civ and has a city in the defensive crusade map
    for iEnemy in civilizations().main().ids():
        pEnemy = player(iEnemy)
        if (
            teamPlayer.isAtWar(pEnemy.getTeam())
            and civilization(iEnemy).date.birth + 10 < iGameTurn
        ):
            if isOrMasterChristian(iEnemy):
                continue
            for pCity in cities.owner(iEnemy).entities():
                if PROVINCES_MAP[pCity.getY()][pCity.getX()] in tPlayerDCMap:
                    return True
    return False


@popup_handler(7625)
def DefensiveCrusadeEvent(playerID, netUserData, popupReturn):
    iDecision = popupReturn.getButtonClicked()
    if iDecision == 0:
        makeDefensiveCrusadeUnits(human())
        player().changeFaith(-min(2, player().getFaith()))


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


def makeDefensiveCrusadeUnits(iPlayer):
    pPlayer = player(iPlayer)
    iFaith = pPlayer.getFaith()
    iBestInfantry = getDefensiveCrusadeBestInfantry(iPlayer)
    iBestCavalry = getDefensiveCrusadeBestCavalry(iPlayer)
    pCapital = pPlayer.getCapitalCity()
    if pCapital:
        iX = pCapital.getX()
        iY = pCapital.getY()
    else:
        city = cities.owner(iPlayer).random_entry()
        if city is not None:
            iX = city.getX()
            iY = city.getY()
        else:
            return

    # Absinthe: interface message for the player
    if player(iPlayer).isHuman():
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
    pPlayer = player(iPlayer)
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
    pPlayer = player(iPlayer)
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
    data.crusade_status[0] = year(1096)
    data.crusade_status[1] = year(1147)
    data.crusade_status[2] = year(1187)


def isOrMasterChristian(iPlayer):
    pPlayer = player(iPlayer)
    iReligion = pPlayer.getStateReligion()
    if iReligion in [Religion.CATHOLICISM, Religion.ORTHODOXY]:
        return True
    iMaster = getMaster(iPlayer)
    if iMaster != -1:
        iMasterReligion = player(iMaster).getStateReligion()
        if iMasterReligion in [Religion.CATHOLICISM, Religion.ORTHODOXY]:
            return True
    return False
