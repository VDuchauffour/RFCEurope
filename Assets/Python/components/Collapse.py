from CvPythonExtensions import CyGlobalContext

from Consts import MessageData
from CoreData import civilization, civilizations
from CoreFunctions import message, text
from CoreStructures import human
from CoreTypes import Civ
from RFCUtils import collapseImmune, getLastRespawnTurn, killAndFragmentCiv
from StoredData import data

gc = CyGlobalContext()


def collapseByBarbs(iGameTurn):
    # Absinthe: collapses if more than 1/3 of the empire is conquered and/or held by barbs
    for iCiv in civilizations().majors().ids():
        pCiv = gc.getPlayer(iCiv)
        if pCiv.isAlive():
            # Absinthe: no barb collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
            iRespawnTurn = getLastRespawnTurn(iCiv)
            if (
                iGameTurn >= civilization(iCiv).date.birth + 20
                and iGameTurn >= iRespawnTurn + 10
                and not collapseImmune(iCiv)
            ):
                iNumCities = pCiv.getNumCities()
                iLostCities = gc.countCitiesLostTo(iCiv, Civ.BARBARIAN)
                # Absinthe: if the civ is respawned, it's harder to collapse them by barbs
                if pCiv.getRespawnedAlive():
                    iLostCities = max(iLostCities - (iNumCities / 4), 0)
                # Absinthe: if more than one third is captured, the civ collapses
                if iLostCities * 2 > iNumCities + 1 and iNumCities > 0:
                    iHuman = human()
                    if not pCiv.isHuman():
                        if gc.getPlayer(iHuman).canContact(iCiv):
                            message(
                                iHuman,
                                pCiv.getCivilizationDescription(0)
                                + " "
                                + text("TXT_KEY_STABILITY_CIVILWAR_BARBS"),
                                color=MessageData.RED,
                            )
                        killAndFragmentCiv(iCiv, True, False)
                    elif pCiv.getNumCities() > 1:
                        message(
                            iCiv,
                            text("TXT_KEY_STABILITY_CIVILWAR_BARBS_HUMAN"),
                            force=True,
                            color=MessageData.RED,
                        )
                        killAndFragmentCiv(iCiv, True, True)


def collapseGeneric(iGameTurn):
    # Absinthe: collapses if number of cities is less than half than some turns ago
    lNumCitiesLastTime = [0] * civilizations().majors().len()
    for iCiv in civilizations().majors().ids():
        pCiv = gc.getPlayer(iCiv)
        teamCiv = gc.getTeam(pCiv.getTeam())
        if pCiv.isAlive():
            lNumCitiesLastTime[iCiv] = data.lNumCities[iCiv]
            iNumCitiesCurrently = pCiv.getNumCities()
            data.lNumCities[iCiv] = iNumCitiesCurrently
            # Absinthe: no generic collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
            iRespawnTurn = getLastRespawnTurn(iCiv)
            if (
                iGameTurn >= civilization(iCiv).date.birth + 20
                and iGameTurn >= iRespawnTurn + 10
                and not collapseImmune(iCiv)
            ):
                # Absinthe: pass for small civs, we have bad stability collapses and collapseMotherland anyway, which is better suited for the collapse of those
                if (
                    lNumCitiesLastTime[iCiv] > 2
                    and iNumCitiesCurrently * 2 <= lNumCitiesLastTime[iCiv]
                ):
                    iHuman = human()
                    if not pCiv.isHuman():
                        if gc.getPlayer(iHuman).canContact(iCiv):
                            message(
                                iHuman,
                                pCiv.getCivilizationDescription(0)
                                + " "
                                + text("TXT_KEY_STABILITY_CIVILWAR_DECLINE"),
                                color=MessageData.RED,
                            )
                        killAndFragmentCiv(iCiv, False, False)
                    elif pCiv.getNumCities() > 1:
                        message(
                            iCiv,
                            text("TXT_KEY_STABILITY_CIVILWAR_DECLINE_HUMAN"),
                            force=True,
                            color=MessageData.RED,
                        )
                        killAndFragmentCiv(iCiv, False, True)


def collapseMotherland(iGameTurn):
    # Absinthe: collapses if completely pushed out of the core area and also doesn't have enough presence in the normal area
    for iCiv in civilizations().majors().ids():
        pCiv = gc.getPlayer(iCiv)
        teamCiv = gc.getTeam(pCiv.getTeam())
        if pCiv.isAlive():
            # Absinthe: no motherland collapse for 20 turns after spawn, for 10 turns after respawn, or with the Emperor UP
            iRespawnTurn = getLastRespawnTurn(iCiv)
            if (
                iGameTurn >= civilization(iCiv).date.birth + 20
                and iGameTurn >= iRespawnTurn + 10
                and not collapseImmune(iCiv)
            ):
                # Absinthe: respawned Cordoba or Aragon shouldn't collapse because not holding the original core area
                if iCiv in [Civ.CORDOBA, Civ.ARAGON] and pCiv.getRespawnedAlive():
                    continue
                if not gc.safeMotherland(iCiv):
                    iHuman = human()
                    if not pCiv.isHuman():
                        if gc.getPlayer(iHuman).canContact(iCiv):
                            message(
                                iHuman,
                                pCiv.getCivilizationDescription(0)
                                + " "
                                + text("TXT_KEY_STABILITY_CIVILWAR_MOTHERLAND"),
                                color=MessageData.RED,
                            )
                        killAndFragmentCiv(iCiv, False, False)
                    elif pCiv.getNumCities() > 1:
                        message(
                            iCiv,
                            text("TXT_KEY_STABILITY_CIVILWAR_MOTHERLAND_HUMAN"),
                            color=MessageData.RED,
                        )
                        killAndFragmentCiv(iCiv, False, True)
