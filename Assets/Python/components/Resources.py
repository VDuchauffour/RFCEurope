# Rhye's and Fall of Civilization: Europe - Dynamic resources
# Based on SoI version, added by Absinthe

from CvPythonExtensions import *
import PyHelpers
import XMLConsts as xml

from MiscData import MessageData
from TimelineData import DateTurn

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()


class Resources:
    def createResource(self, iX, iY, iBonus, textKey="TXT_KEY_RESOURCE_DISCOVERED"):
        """Creates a bonus resource and alerts the plot owner"""

        if (
            gc.getMap().plot(iX, iY).getBonusType(-1) == -1 or iBonus == -1
        ):  # Absinthe: only proceed if there isn't any bonus resources on the plot, or if we're removing the bonus
            if iBonus == -1:
                iBonus = gc.getMap().plot(iX, iY).getBonusType(-1)  # for alert
                gc.getMap().plot(iX, iY).setBonusType(-1)
            else:
                gc.getMap().plot(iX, iY).setBonusType(iBonus)

            iOwner = gc.getMap().plot(iX, iY).getOwner()
            if iOwner >= 0 and textKey != -1:  # Absinthe: only show alert to the tile owner
                city = gc.getMap().findCity(
                    iX,
                    iY,
                    iOwner,
                    TeamTypes.NO_TEAM,
                    True,
                    False,
                    TeamTypes.NO_TEAM,
                    DirectionTypes.NO_DIRECTION,
                    CyCity(),
                )
                if not city.isNone():
                    szText = localText.getText(
                        textKey,
                        (
                            gc.getBonusInfo(iBonus).getTextKey(),
                            city.getName(),
                            gc.getPlayer(iOwner).getCivilizationAdjective(0),
                        ),
                    )
                    CyInterface().addMessage(
                        iOwner,
                        False,
                        MessageData.DURATION,
                        szText,
                        "AS2D_DISCOVERBONUS",
                        InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT,
                        gc.getBonusInfo(iBonus).getButton(),
                        ColorTypes(MessageData.LIME),
                        iX,
                        iY,
                        True,
                        True,
                    )

    def removeResource(self, iX, iY, textKey="TXT_KEY_RESOURCE_EXHAUSTED"):
        """Removes a bonus resource and alerts the plot owner"""

        if (
            gc.getMap().plot(iX, iY).getBonusType(-1) != -1
        ):  # only proceed if there is a bonus resource on the plot
            iBonusType = gc.getMap().plot(iX, iY).getBonusType(-1)
            iImprovementType = gc.getMap().plot(iX, iY).getImprovementType()
            self.createResource(iX, iY, -1, textKey)
            # Absinthe: remove the improvement too, but only if it improves the given resource
            # 			for now only adding the ones we actually use
            # 			Pasture, Camp and Colonial Trade Route cannot be built on base terrain (only with resource), so it is always safe to remove those
            # 			the question is whether we should also remove Farms and Lumbermills for example
            if iBonusType == xml.iHorse and iImprovementType == xml.iImprovementPasture:
                gc.getMap().plot(iX, iY).setImprovementType(-1)
            elif (
                iBonusType == xml.iNorthAccess
                and iImprovementType == xml.iImprovementColonialTrade
            ):
                gc.getMap().plot(iX, iY).setImprovementType(-1)

    def checkTurn(self, iGameTurn):
        # Absinthe: note that all actions are taken place in the end of the turn, so actually the resources will appear/disappear for the next turn
        if iGameTurn == DateTurn.i552AD:
            self.createResource(80, 24, xml.iSilk)  # Silk near Constantinople
        elif iGameTurn == DateTurn.i1000AD:
            self.createResource(36, 24, xml.iRice)  # Rice in Iberia
            self.createResource(86, 2, xml.iRice)  # Rice in the Middle East
        elif iGameTurn == (DateTurn.i1066AD + 1):
            self.removeResource(2, 69)  # Remove the NAA from Iceland
        elif iGameTurn == DateTurn.i1452AD:  # Coffee spawns instead of being preplaced
            self.createResource(93, 0, xml.iCoffee)  # near Sinai
            self.createResource(99, 13, xml.iCoffee)  # between Damascus and Edessa
        elif iGameTurn == DateTurn.i1500AD:
            self.createResource(
                55, 35, xml.iRice
            )  # Rice in Italy - represents trade of the merchant republics
        elif iGameTurn == DateTurn.i1580AD:
            self.createResource(32, 59, xml.iPotato)  # Potatoes in Ireland
            self.createResource(29, 57, xml.iPotato)
            self.createResource(69, 49, xml.iPotato)  # Poland
            self.createResource(66, 46, xml.iPotato)
            self.createResource(60, 48, xml.iPotato)  # Northern Germany
            self.createResource(55, 52, xml.iPotato)
            self.createResource(59, 61, xml.iAccess)  # Atlantic Access in Scandinavia

    def onTechAcquired(self, iTech, iPlayer):
        pass
