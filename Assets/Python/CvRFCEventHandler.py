# Rhye's and Fall of Civilization: Europe - Event handler

from CvPythonExtensions import *
from StoredData import data
import Locations
import Modifiers
import Civilizations

gc = CyGlobalContext()


class CvRFCEventHandler:
    def __init__(self, eventManager):

        # initialize base class
        eventManager.addEventHandler("GameStart", self.onGameStart)  # Stability
        eventManager.addEventHandler("BeginGameTurn", self.onBeginGameTurn)  # Stability
        eventManager.addEventHandler("cityAcquired", self.onCityAcquired)  # Stability
        eventManager.addEventHandler(
            "cityAcquiredAndKept", self.onCityAcquiredAndKept
        )  # Stability
        eventManager.addEventHandler("cityRazed", self.onCityRazed)  # Stability
        eventManager.addEventHandler("cityBuilt", self.onCityBuilt)  # Stability
        eventManager.addEventHandler("combatResult", self.onCombatResult)  # Stability
        # eventManager.addEventHandler("changeWar", self.onChangeWar)
        eventManager.addEventHandler("religionFounded", self.onReligionFounded)  # Victory
        eventManager.addEventHandler("buildingBuilt", self.onBuildingBuilt)  # Victory
        eventManager.addEventHandler("projectBuilt", self.onProjectBuilt)  # Victory
        eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)  # Mercenaries
        # eventManager.addEventHandler("EndPlayerTurn", self.onEndPlayerTurn)
        eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)  # Stability
        eventManager.addEventHandler(
            "kbdEvent", self.onKbdEvent
        )  # Mercenaries and Stability overlay
        eventManager.addEventHandler("unitLost", self.onUnitLost)  # Mercenaries
        eventManager.addEventHandler("unitKilled", self.onUnitKilled)  # Mercenaries
        eventManager.addEventHandler("OnPreSave", self.onPreSave)  # edead: StoredData
        eventManager.addEventHandler("OnLoad", self.onLoadGame)  # Mercenaries, StoredData
        eventManager.addEventHandler("unitPromoted", self.onUnitPromoted)  # Mercenaries
        eventManager.addEventHandler("techAcquired", self.onTechAcquired)  # Mercenaries #Stability
        # eventManager.addEventHandler("improvementDestroyed",self.onImprovementDestroyed) #Stability
        eventManager.addEventHandler("unitPillage", self.onUnitPillage)  # Stability
        eventManager.addEventHandler("religionSpread", self.onReligionSpread)  # Stability
        eventManager.addEventHandler("firstContact", self.onFirstContact)
        eventManager.addEventHandler(
            "playerChangeAllCivics", self.onPlayerChangeAllCivics
        )  # Absinthe: Python Event for civic changes
        eventManager.addEventHandler(
            "playerChangeSingleCivic", self.onPlayerChangeSingleCivic
        )  # Absinthe: Python Event for civic changes
        eventManager.addEventHandler("playerChangeStateReligion", self.onPlayerChangeStateReligion)

    def onGameStart(self, argsList):
        "Called at the start of the game"
        return 0

    def onPreSave(self, argsList):
        "called before a game is actually saved"
        return 0

    # This method creates a new instance of the MercenaryUtils class to be used later
    def onLoadGame(self, argsList):
        data.load()  # edead: load & unpickle script data
        Locations.setup()
        Modifiers.setup()
        Civilizations.setup()

    def onCityAcquired(self, argsList):
        "City Acquired"
        return 0

    def onCityAcquiredAndKept(self, argsList):
        "City Acquired and Kept"
        return 0

    def onCityRazed(self, argsList):
        "City Razed"
        return 0

    def onCityBuilt(self, argsList):
        "City Built"
        return 0

    def onCombatResult(self, argsList):
        return 0

    def onReligionFounded(self, argsList):
        "Religion Founded"
        return 0

    def onBuildingBuilt(self, argsList):
        return 0

    def onProjectBuilt(self, argsList):
        return 0

    def onUnitPillage(self, argsList):
        return 0

    def onBeginGameTurn(self, argsList):
        iGameTurn = argsList[0]
        return 0

    def onBeginPlayerTurn(self, argsList):
        return 0

    def onEndPlayerTurn(self, argsList):
        """Called at the end of a players turn"""
        # 3Miro does not get called
        iGameTurn, iPlayer = argsList

    def onEndGameTurn(self, argsList):
        iGameTurn = argsList[0]
        return 0

    def onReligionSpread(self, argsList):
        iReligion, iOwner, pSpreadCity = argsList
        return 0

    def onFirstContact(self, argsList):
        iTeamX, iHasMetTeamY = argsList
        return 0

    def onPlayerChangeAllCivics(self, argsList):
        return 0

    def onPlayerChangeSingleCivic(self, argsList):
        # note that this reports all civic changes in single instances (so also reports force converts by diplomacy or with spies)
        "Civics are changed for a player"
        iPlayer, iNewCivic, iOldCivic = argsList

    def onPlayerChangeStateReligion(self, argsList):
        "Player changes his state religion"
        return 0

    def onTechAcquired(self, argsList):
        return 0

    def onUnitPromoted(self, argsList):
        "Unit Promoted"
        return 0

    def onUnitKilled(self, argsList):
        "Unit Killed"
        return 0

    def onUnitLost(self, argsList):
        "Unit Lost"
        return 0

    # This method handles the key input and will bring up the mercenary manager screen if the
    # player has at least one city and presses 'ctrl' and the 'M' key.
    def onKbdEvent(self, argsList):
        "keypress handler - return 1 if the event was consumed"
        return 0

    def printPlotsDebug(self):
        pass
