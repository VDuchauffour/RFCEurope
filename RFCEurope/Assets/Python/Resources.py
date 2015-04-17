# Rhye's and Fall of Civilization: Europe - Dynamic resources
# Based on SoI version, added by Absinthe

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import Popup
import Consts as con
import XMLConsts as xml

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
localText = CyTranslator()


class Resources:

	def createResource(self, iX, iY, iBonus, textKey="TXT_KEY_RESOURCE_DISCOVERED"):
		"""Creates a bonus resource and alerts the plot owner"""

		if gc.getMap().plot(iX,iY).getBonusType(-1) == -1 or iBonus == -1: # only proceed if the bonus isn't already there or if we're removing the bonus
			if iBonus == -1:
				iBonus = gc.getMap().plot(iX,iY).getBonusType(-1) # for alert
				gc.getMap().plot(iX,iY).setBonusType(-1)
			else:
				gc.getMap().plot(iX,iY).setBonusType(iBonus)

			iOwner = gc.getMap().plot(iX,iY).getOwner()
			if iOwner >= 0 and textKey != -1: # only show alert to the tile owner
				city = gc.getMap().findCity(iX, iY, iOwner, TeamTypes.NO_TEAM, True, False, TeamTypes.NO_TEAM, DirectionTypes.NO_DIRECTION, CyCity())
				if not city.isNone():
					szText = localText.getText(textKey, (gc.getBonusInfo(iBonus).getTextKey(), city.getName(), gc.getPlayer(iOwner).getCivilizationAdjective(0)))
					CyInterface().addMessage(iOwner, False, con.iDuration, szText, "AS2D_DISCOVERBONUS", InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT, gc.getBonusInfo(iBonus).getButton(), ColorTypes(con.iLightBlue), iX, iY, True, True)


	def removeResource(self, iX, iY, textKey="TXT_KEY_RESOURCE_EXHAUSTED"):
		"""Removes a bonus resource and alerts the plot owner"""

		self.createResource(iX, iY, -1, textKey)


	def checkTurn(self, iGameTurn):
		# Note that all actions are taken place in the end of the turn, so actually the resources will appear/disappear for the next turn
		if (iGameTurn == xml.i1000AD):
			self.createResource(36, 24, xml.iRice) #Rice in Iberia
			self.createResource(86,  2, xml.iRice) #Rice in the Middle East
		if (iGameTurn == xml.i1500AD):
			self.createResource(55, 35, xml.iRice) #Rice in Italy
		if (iGameTurn == xml.i1250AD):
			self.removeResource( 2, 69)  #Remove the NAA from Iceland
		if (iGameTurn == xml.i1452AD):   #Coffee spawns instead of being preplaced
			self.createResource(93, 0, xml.iCoffee)  #near Sinai
			self.createResource(99, 13, xml.iCoffee) #between Damascus and Edessa
		if (iGameTurn == xml.i1580AD):
			self.createResource(32, 59, xml.iPotato) #Potatoes in Ireland
			self.createResource(29, 57, xml.iPotato)
			self.createResource(69, 49, xml.iPotato) #Poland
			self.createResource(66, 46, xml.iPotato)
			self.createResource(60, 48, xml.iPotato) #Northern Germany
			self.createResource(55, 52, xml.iPotato)
			self.createResource(59, 61, xml.iAccess) #Atlantic Access in Scandinavia


	def onTechAcquired( self, iTech, iPlayer ):
		pass
		#if ( iTech == xml.iAstronomy ):
			#if ( gc.getMap().plot(23, 23).getBonusType() != -1 ): # if the AA has already been added to the tile
				#gc.getMap().plot(23, 23).setBonusType(xml.iAccess)
			#if ( iPlayer == con.iSpain ):
				#gc.getMap().plot(23, 41).setBonusType(xml.iAccess)
				#gc.getMap().plot(24, 27).setBonusType(xml.iAccess)
			#if ( iPlayer == con.iPortugal ):
				#gc.getMap().plot(20, 31).setBonusType(xml.iAccess)
			#if ( iPlayer == con.iEngland ):
				#gc.getMap().plot(36, 54).setBonusType(xml.iAccess)
				#gc.getMap().plot(34, 50).setBonusType(xml.iAccess)
			#if ( iPlayer == con.iFrankia ):
				#gc.getMap().plot(37, 42).setBonusType(xml.iAccess)
			#if ( iPlayer == con.iNorway and ( not gc.getPlayer(con.iEngland).isAlive() ) ):
				#if ( gc.getMap().plot(36, 54).getBonusType(-1) != -1 ):
					#gc.getMap().plot(36, 54).setBonusType(xml.iAccess)

