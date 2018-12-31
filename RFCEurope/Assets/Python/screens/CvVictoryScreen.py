## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import PyHelpers
import time
import Consts as con
import XMLConsts as xml
import RFCUtils
import Victory as vic
import UniquePowers

PyPlayer = PyHelpers.PyPlayer

# globals

up = UniquePowers.UniquePowers()
utils = RFCUtils.RFCUtils()
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

VICTORY_CONDITION_SCREEN = 0
GAME_SETTINGS_SCREEN = 1
UN_RESOLUTION_SCREEN = 2
UN_MEMBERS_SCREEN = 3

class CvVictoryScreen:
	"Keeps track of victory conditions"

	def __init__(self, screenId):
		self.screenId = screenId
		self.SCREEN_NAME = "VictoryScreen"
		self.DEBUG_DROPDOWN_ID =  "VictoryScreenDropdownWidget"
		self.INTERFACE_ART_INFO = "TECH_BG"
		self.EXIT_AREA = "EXIT"
		self.EXIT_ID = "VictoryScreenExit"
		self.BACKGROUND_ID = "VictoryScreenBackground"
		self.HEADER_ID = "VictoryScreenHeader"
		self.WIDGET_ID = "VictoryScreenWidget"
		self.VC_TAB_ID = "VictoryTabWidget"
		self.SETTINGS_TAB_ID = "SettingsTabWidget"
		self.UN_RESOLUTION_TAB_ID = "VotingTabWidget"
		self.UN_MEMBERS_TAB_ID = "MembersTabWidget"
		self.SPACESHIP_SCREEN_BUTTON = 1234

		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 12

		self.X_EXIT = 994
		self.Y_EXIT = 726

		self.X_AREA = 8
		self.Y_AREA = 58
		self.W_AREA = 1010
		self.H_AREA = 267

		# 3Miro: resize the table to fit the long strings of UHVs (same idea as RFC 1.186)
		#self.TABLE_WIDTH_0 = 350
		#self.TABLE_WIDTH_1 = 80
		#self.TABLE_WIDTH_2 = 180
		#self.TABLE_WIDTH_3 = 100
		#self.TABLE_WIDTH_4 = 180
		#self.TABLE_WIDTH_5 = 100
		self.TABLE_WIDTH_0 = 575
		self.TABLE_WIDTH_1 = 5
		self.TABLE_WIDTH_2 = 135
		self.TABLE_WIDTH_3 = 105
		self.TABLE_WIDTH_4 = 120
		self.TABLE_WIDTH_5 = 100

		self.TABLE2_WIDTH_0 = 740
		self.TABLE2_WIDTH_1 = 265

		self.X_LINK = 100
		self.DX_LINK = 220
		self.Y_LINK = 726
		self.MARGIN = 20

		self.SETTINGS_PANEL_X1 = 50
		self.SETTINGS_PANEL_X2 = 355
		self.SETTINGS_PANEL_X3 = 660
		self.SETTINGS_PANEL_Y = 150
		self.SETTINGS_PANEL_WIDTH = 300
		self.SETTINGS_PANEL_HEIGHT = 500

		self.nWidgetCount = 0
		self.iActivePlayer = -1
		self.bVoteTab = False

		self.iScreen = VICTORY_CONDITION_SCREEN

		self.X_UHV1 = 8
		self.Y_UHV1 = 334
		self.W_UHV1 = 1010
		self.H_UHV1 = 129

		self.X_UHV2 = self.X_UHV1
		self.Y_UHV2 = self.Y_UHV1 + 127
		self.W_UHV2 = self.W_UHV1
		self.H_UHV2 = self.H_UHV1

		self.X_UHV3 = self.X_UHV1
		self.Y_UHV3 = self.Y_UHV2 + 127
		self.W_UHV3 = self.W_UHV1
		self.H_UHV3 = self.H_UHV1

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, self.screenId)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()

	def interfaceScreen(self):

		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.iActivePlayer = CyGame().getActivePlayer()
		if self.iScreen == -1:
			self.iScreen = VICTORY_CONDITION_SCREEN

		# Set the background widget and exit button
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground( False )
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setText(self.EXIT_ID, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		# Header...
		screen.setLabel(self.HEADER_ID, "Background", u"<font=4b>" + localText.getText("TXT_KEY_VICTORY_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if self.iScreen == VICTORY_CONDITION_SCREEN:
			self.showVictoryConditionScreen()
		elif self.iScreen == GAME_SETTINGS_SCREEN:
			self.showGameSettingsScreen()
		elif self.iScreen == UN_RESOLUTION_SCREEN:
			self.showVotingScreen()
		elif self.iScreen == UN_MEMBERS_SCREEN:
			self.showMembersScreen()

	def drawTabs(self):

		screen = self.getScreen()

		xLink = self.X_LINK
		if (self.iScreen != VICTORY_CONDITION_SCREEN):
			screen.setText(self.VC_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_MAIN_MENU_VICTORIES", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setText(self.VC_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_MAIN_MENU_VICTORIES", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += self.DX_LINK

		if (self.iScreen != GAME_SETTINGS_SCREEN):
			screen.setText(self.SETTINGS_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_MAIN_MENU_SETTINGS", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setText(self.SETTINGS_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_MAIN_MENU_SETTINGS", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += self.DX_LINK

		if self.bVoteTab:
			if (self.iScreen != UN_RESOLUTION_SCREEN):
				screen.setText(self.UN_RESOLUTION_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_VOTING_TITLE", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				screen.setText(self.UN_RESOLUTION_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_VOTING_TITLE", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLink += self.DX_LINK

			if (self.iScreen != UN_MEMBERS_SCREEN):
				screen.setText(self.UN_MEMBERS_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_MEMBERS_TITLE", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				screen.setText(self.UN_MEMBERS_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_MEMBERS_TITLE", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLink += self.DX_LINK

	def showVotingScreen(self):

		self.deleteAllWidgets()

		activePlayer = gc.getPlayer(self.iActivePlayer)
		iActiveTeam = activePlayer.getTeam()

		aiVoteBuildingClass = []
		for i in range(gc.getNumBuildingInfos()):
			for j in range(gc.getNumVoteSourceInfos()):
				if (gc.getBuildingInfo(i).getVoteSourceType() == j):
					iUNTeam = -1
					bUnknown = True
					for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
						if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
							if (gc.getTeam(iLoopTeam).getBuildingClassCount(gc.getBuildingInfo(i).getBuildingClassType()) > 0):
								iUNTeam = iLoopTeam
								if (iLoopTeam == iActiveTeam or gc.getGame().isDebugMode() or gc.getTeam(activePlayer.getTeam()).isHasMet(iLoopTeam)):
									bUnknown = false
								break

					aiVoteBuildingClass.append((gc.getBuildingInfo(i).getBuildingClassType(), iUNTeam, bUnknown))

		if (len(aiVoteBuildingClass) == 0):
			return

		screen = self.getScreen()

		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-8, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+22, PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 2, self.X_AREA, self.Y_AREA, self.W_AREA, self.H_AREA, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(szTable, False)
		screen.setTableColumnHeader(szTable, 0, "", self.TABLE2_WIDTH_0)
		screen.setTableColumnHeader(szTable, 1, "", self.TABLE2_WIDTH_1)

		for (iVoteBuildingClass, iUNTeam, bUnknown) in aiVoteBuildingClass:
			iRow = screen.appendTableRow(szTable)
			screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_ELECTION", (gc.getBuildingClassInfo(iVoteBuildingClass).getTextKey(), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if (iUNTeam != -1):
				if bUnknown:
					szName = localText.getText("TXT_KEY_TOPCIVS_UNKNOWN", ())
				else:
					#Rhye - start
					#szName = gc.getTeam(iUNTeam).getName()
					szName = gc.getPlayer(iUNTeam).getCivilizationShortDescription(0)
					#Rhye - end
				screen.setTableText(szTable, 1, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_BUILT", (szName, )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			else:
				screen.setTableText(szTable, 1, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_NOT_BUILT", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		for i in range(gc.getNumVoteSourceInfos()):
			if (gc.getGame().canHaveSecretaryGeneral(i) and -1 != gc.getGame().getSecretaryGeneral(i)):
				iRow = screen.appendTableRow(szTable)
				screen.setTableText(szTable, 0, iRow, gc.getVoteSourceInfo(i).getSecretaryGeneralText(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(szTable, 1, iRow, gc.getTeam(gc.getGame().getSecretaryGeneral(i)).getName(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

			for iLoop in range(gc.getNumVoteInfos()):
				if gc.getGame().countPossibleVote(iLoop, i) > 0:
					info = gc.getVoteInfo(iLoop)
					if gc.getGame().isChooseElection(iLoop):
						iRow = screen.appendTableRow(szTable)
						screen.setTableText(szTable, 0, iRow, info.getDescription(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						if gc.getGame().isVotePassed(iLoop):
							screen.setTableText(szTable, 1, iRow, localText.getText("TXT_KEY_POPUP_PASSED", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						else:
							screen.setTableText(szTable, 1, iRow, localText.getText("TXT_KEY_POPUP_ELECTION_OPTION", (u"", gc.getGame().getVoteRequired(iLoop, i), gc.getGame().countPossibleVote(iLoop, i))), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		self.drawTabs()


	def showMembersScreen(self):

		self.deleteAllWidgets()

		activePlayer = gc.getPlayer(self.iActivePlayer)
		iActiveTeam = activePlayer.getTeam()

		screen = self.getScreen()

		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-8, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+22, PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 2, self.X_AREA, self.Y_AREA, self.W_AREA, self.H_AREA, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(szTable, False)
		screen.setTableColumnHeader(szTable, 0, "", self.TABLE2_WIDTH_0)
		screen.setTableColumnHeader(szTable, 1, "", self.TABLE2_WIDTH_1)

		for i in range(gc.getNumVoteSourceInfos()):
			if gc.getGame().isDiploVote(i):
				kVoteSource = gc.getVoteSourceInfo(i)
				iRow = screen.appendTableRow(szTable)
				screen.setTableText(szTable, 0, iRow, u"<font=4b>" + kVoteSource.getDescription().upper() + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				if (gc.getGame().getVoteSourceReligion(i) != -1):
					screen.setTableText(szTable, 1, iRow, gc.getReligionInfo(gc.getGame().getVoteSourceReligion(i)).getDescription(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				iSecretaryGeneralVote = -1
				if (gc.getGame().canHaveSecretaryGeneral(i) and -1 != gc.getGame().getSecretaryGeneral(i)):
					for j in range(gc.getNumVoteInfos()):
						print j
						if gc.getVoteInfo(j).isVoteSourceType(i):
							print "votesource"
							if gc.getVoteInfo(j).isSecretaryGeneral():
								print "secgen"
								iSecretaryGeneralVote = j
								break
				print iSecretaryGeneralVote

				for j in range(gc.getMAX_PLAYERS()):
					if gc.getPlayer(j).isAlive() and gc.getTeam(iActiveTeam).isHasMet(gc.getPlayer(j).getTeam()):
						#szPlayerText = gc.getPlayer(j).getName() #Rhye
						szPlayerText = gc.getPlayer(j).getCivilizationShortDescription(0) #Rhye
						if (-1 != iSecretaryGeneralVote):
							szPlayerText += localText.getText("TXT_KEY_VICTORY_SCREEN_PLAYER_VOTES", (gc.getPlayer(j).getVotes(iSecretaryGeneralVote, i), ))
						if (gc.getGame().canHaveSecretaryGeneral(i) and gc.getGame().getSecretaryGeneral(i) == gc.getPlayer(j).getTeam()):
							iRow = screen.appendTableRow(szTable)
							screen.setTableText(szTable, 0, iRow, szPlayerText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 1, iRow, gc.getVoteSourceInfo(i).getSecretaryGeneralText(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						elif (gc.getPlayer(j).isFullMember(i)):
							iRow = screen.appendTableRow(szTable)
							screen.setTableText(szTable, 0, iRow, szPlayerText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 1, iRow, localText.getText("TXT_KEY_VOTESOURCE_FULL_MEMBER", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						elif (gc.getPlayer(j).isVotingMember(i)):
							iRow = screen.appendTableRow(szTable)
							screen.setTableText(szTable, 0, iRow, szPlayerText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 1, iRow, localText.getText("TXT_KEY_VOTESOURCE_VOTING_MEMBER", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				iRow = screen.appendTableRow(szTable)

		self.drawTabs()


	def showGameSettingsScreen(self):

		self.deleteAllWidgets()
		screen = self.getScreen()


		activePlayer = gc.getPlayer(self.iActivePlayer)

		szSettingsPanel = self.getNextWidgetName()
		screen.addPanel(szSettingsPanel, localText.getText("TXT_KEY_MAIN_MENU_SETTINGS", ()).upper(), "", True, True, self.SETTINGS_PANEL_X1, self.SETTINGS_PANEL_Y - 10, self.SETTINGS_PANEL_WIDTH, self.SETTINGS_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)
		szSettingsTable = self.getNextWidgetName()
		screen.addListBoxGFC(szSettingsTable, "", self.SETTINGS_PANEL_X1 + self.MARGIN, self.SETTINGS_PANEL_Y + self.MARGIN, self.SETTINGS_PANEL_WIDTH - 2*self.MARGIN, self.SETTINGS_PANEL_HEIGHT - 2*self.MARGIN, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(szSettingsTable, False)

		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_LEADER_CIV_DESCRIPTION", (activePlayer.getNameKey(), activePlayer.getCivilizationShortDescriptionKey())), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		# Absinthe: no leader traits
		#screen.appendListBoxStringNoUpdate(szSettingsTable, u"     (" + CyGameTextMgr().parseLeaderTraits(activePlayer.getLeaderType(), activePlayer.getCivilizationType(), True, False) + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, " ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_DIFFICULTY", (gc.getHandicapInfo(activePlayer.getHandicapType()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, " ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, gc.getMap().getMapScriptName(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_MAP_SIZE", (gc.getWorldInfo(gc.getMap().getWorldSize()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_CLIMATE", (gc.getClimateInfo(gc.getMap().getClimate()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_SEA_LEVEL", (gc.getSeaLevelInfo(gc.getMap().getSeaLevel()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, " ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_STARTING_ERA", (gc.getEraInfo(gc.getGame().getStartEra()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		screen.appendListBoxStringNoUpdate(szSettingsTable, localText.getText("TXT_KEY_SETTINGS_GAME_SPEED", (gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getTextKey(), )), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		screen.updateListBox(szSettingsTable)

		szOptionsPanel = self.getNextWidgetName()
		screen.addPanel(szOptionsPanel, localText.getText("TXT_KEY_MAIN_MENU_CUSTOM_SETUP_OPTIONS", ()).upper(), "", True, True, self.SETTINGS_PANEL_X2, self.SETTINGS_PANEL_Y - 10, self.SETTINGS_PANEL_WIDTH, self.SETTINGS_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)
		szOptionsTable = self.getNextWidgetName()
		screen.addListBoxGFC(szOptionsTable, "", self.SETTINGS_PANEL_X2 + self.MARGIN, self.SETTINGS_PANEL_Y + self.MARGIN, self.SETTINGS_PANEL_WIDTH - 2*self.MARGIN, self.SETTINGS_PANEL_HEIGHT - 2*self.MARGIN, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(szOptionsTable, False)

		for i in range(GameOptionTypes.NUM_GAMEOPTION_TYPES):
			if gc.getGame().isOption(i):
				screen.appendListBoxStringNoUpdate(szOptionsTable, gc.getGameOptionInfo(i).getDescription(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		if (gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START)):
			szNumPoints = u"%s %d" % (localText.getText("TXT_KEY_ADVANCED_START_POINTS", ()), gc.getGame().getNumAdvancedStartPoints())
			screen.appendListBoxStringNoUpdate(szOptionsTable, szNumPoints, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		if (gc.getGame().isGameMultiPlayer()):
			for i in range(gc.getNumMPOptionInfos()):
				if (gc.getGame().isMPOption(i)):
					screen.appendListBoxStringNoUpdate(szOptionsTable, gc.getMPOptionInfo(i).getDescription(), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

			if (gc.getGame().getMaxTurns() > 0):
				szMaxTurns = u"%s %d" % (localText.getText("TXT_KEY_TURN_LIMIT_TAG", ()), gc.getGame().getMaxTurns())
				screen.appendListBoxStringNoUpdate(szOptionsTable, szMaxTurns, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

			if (gc.getGame().getMaxCityElimination() > 0):
				szMaxCityElimination = u"%s %d" % (localText.getText("TXT_KEY_CITY_ELIM_TAG", ()), gc.getGame().getMaxCityElimination())
				screen.appendListBoxStringNoUpdate(szOptionsTable, szMaxCityElimination, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		if (gc.getGame().hasSkippedSaveChecksum()):
			screen.appendListBoxStringNoUpdate(szOptionsTable, "Skipped Checksum", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		screen.updateListBox(szOptionsTable)

		szCivsPanel = self.getNextWidgetName()
		screen.addPanel(szCivsPanel, localText.getText("TXT_KEY_RIVALS_MET", ()).upper(), "", True, True, self.SETTINGS_PANEL_X3, self.SETTINGS_PANEL_Y - 10, self.SETTINGS_PANEL_WIDTH, self.SETTINGS_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)

		szCivsTable = self.getNextWidgetName()
		screen.addListBoxGFC(szCivsTable, "", self.SETTINGS_PANEL_X3 + self.MARGIN, self.SETTINGS_PANEL_Y + self.MARGIN, self.SETTINGS_PANEL_WIDTH - 2*self.MARGIN, self.SETTINGS_PANEL_HEIGHT - 2*self.MARGIN, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(szCivsTable, False)

		for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
			player = gc.getPlayer(iLoopPlayer)
			if (player.isEverAlive() and iLoopPlayer != self.iActivePlayer and (gc.getTeam(player.getTeam()).isHasMet(activePlayer.getTeam()) or gc.getGame().isDebugMode()) and not player.isBarbarian() and not player.isMinorCiv()):
				screen.appendListBoxStringNoUpdate(szCivsTable, localText.getText("TXT_KEY_LEADER_CIV_DESCRIPTION", (player.getNameKey(), player.getCivilizationShortDescriptionKey())), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
				# Absinthe: no leader traits
				#screen.appendListBoxStringNoUpdate(szCivsTable, u"     (" + CyGameTextMgr().parseLeaderTraits(player.getLeaderType(), player.getCivilizationType(), True, False) + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
				#screen.appendListBoxStringNoUpdate(szCivsTable, " ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		screen.updateListBox(szCivsTable)

		self.drawTabs()


	def showVictoryConditionScreen(self):

		activePlayer = PyHelpers.PyPlayer(self.iActivePlayer)
		iActiveTeam = gc.getPlayer(self.iActivePlayer).getTeam()

		# Conquest
		nRivals = -1
		for i in range(gc.getMAX_CIV_TEAMS()):
			if (gc.getTeam(i).isAlive() and not gc.getTeam(i).isMinorCiv() and not gc.getTeam(i).isBarbarian()):
				nRivals += 1

		# Population
		totalPop = gc.getGame().getTotalPopulation()
		ourPop = activePlayer.getTeam().getTotalPopulation()
		if (totalPop > 0):
			popPercent = (ourPop * 100.0) / totalPop
		else:
			popPercent = 0.0

		iBestPopTeam = -1
		bestPop = 0
		for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
			if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
				if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
					teamPop = gc.getTeam(iLoopTeam).getTotalPopulation()
					if (teamPop > bestPop):
						bestPop = teamPop
						iBestPopTeam = iLoopTeam

		# Score
		ourScore = gc.getGame().getTeamScore(iActiveTeam)

		iBestScoreTeam = -1
		bestScore = 0
		for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
			if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
				if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
					teamScore = gc.getGame().getTeamScore(iLoopTeam)
					if (teamScore > bestScore):
						bestScore = teamScore
						iBestScoreTeam = iLoopTeam

		# Land Area
		totalLand = gc.getMap().getLandPlots()
		ourLand = activePlayer.getTeam().getTotalLand()
		if (totalLand > 0):
			landPercent = (ourLand * 100.0) / totalLand
		else:
			landPercent = 0.0

		iBestLandTeam = -1
		bestLand = 0
		for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
			if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
				if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
					teamLand = gc.getTeam(iLoopTeam).getTotalLand()
					if (teamLand > bestLand):
						bestLand = teamLand
						iBestLandTeam = iLoopTeam

		# Religion
		iOurReligion = -1
		ourReligionPercent = 0
		for iLoopReligion in range(gc.getNumReligionInfos()):
			if (activePlayer.getTeam().hasHolyCity(iLoopReligion)):
				religionPercent = gc.getGame().calculateReligionPercent(iLoopReligion)
				if (religionPercent > ourReligionPercent):
					ourReligionPercent = religionPercent
					iOurReligion = iLoopReligion

		iBestReligion = -1
		bestReligionPercent = 0
		for iLoopReligion in range(gc.getNumReligionInfos()):
			if (iLoopReligion != iOurReligion):
				religionPercent = gc.getGame().calculateReligionPercent(iLoopReligion)
				if (religionPercent > bestReligionPercent):
					bestReligionPercent = religionPercent
					iBestReligion = iLoopReligion

		# Total Culture
		ourCulture = activePlayer.getTeam().countTotalCulture()

		iBestCultureTeam = -1
		bestCulture = 0
		for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
			if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
				if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
					teamCulture = gc.getTeam(iLoopTeam).countTotalCulture()
					if (teamCulture > bestCulture):
						bestCulture = teamCulture
						iBestCultureTeam = iLoopTeam

		# Vote
		aiVoteBuildingClass = []
		for i in range(gc.getNumBuildingInfos()):
			for j in range(gc.getNumVoteSourceInfos()):
				if (gc.getBuildingInfo(i).getVoteSourceType() == j):
					iUNTeam = -1
					bUnknown = True
					for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
						if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
							if (gc.getTeam(iLoopTeam).getBuildingClassCount(gc.getBuildingInfo(i).getBuildingClassType()) > 0):
								iUNTeam = iLoopTeam
								if (iLoopTeam == iActiveTeam or gc.getGame().isDebugMode() or activePlayer.getTeam().isHasMet(iLoopTeam)):
									bUnknown = false
								break

					aiVoteBuildingClass.append((gc.getBuildingInfo(i).getBuildingClassType(), iUNTeam, bUnknown))

		self.bVoteTab = (len(aiVoteBuildingClass) > 0)

		self.deleteAllWidgets()
		screen = self.getScreen()

		# Start filling in the table below
		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-8, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+22, PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 6, self.X_AREA, self.Y_AREA, self.W_AREA, self.H_AREA, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(szTable, 0, "", self.TABLE_WIDTH_0)
		screen.setTableColumnHeader(szTable, 1, "", self.TABLE_WIDTH_1)
		screen.setTableColumnHeader(szTable, 2, "", self.TABLE_WIDTH_2)
		screen.setTableColumnHeader(szTable, 3, "", self.TABLE_WIDTH_3)
		screen.setTableColumnHeader(szTable, 4, "", self.TABLE_WIDTH_4)
		screen.setTableColumnHeader(szTable, 5, "", self.TABLE_WIDTH_5)
		screen.appendTableRow(szTable)

		for iLoopVC in range(gc.getNumVictoryInfos()):
			victory = gc.getVictoryInfo(iLoopVC)
			if (gc.getGame().isVictoryValid(iLoopVC) and (iLoopVC != 7) and (iLoopVC != 6)): # 3Miro: Changes to the Victory screen

				iNumRows = screen.getTableNumRows(szTable)

				szVictoryType = u"<font=4b>" + victory.getDescription().upper() + u"</font>"
				if (victory.isEndScore() and (gc.getGame().getMaxTurns() > gc.getGame().getElapsedGameTurns())):
					szVictoryType += "    (" + localText.getText("TXT_KEY_MISC_TURNS_LEFT", (gc.getGame().getMaxTurns() - gc.getGame().getElapsedGameTurns(), )) + ")"

				iVictoryTitleRow = iNumRows - 1
				screen.setTableText(szTable, 0, iVictoryTitleRow, szVictoryType, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				bSpaceshipFound = False
				bEntriesFound = False

				if (victory.isTargetScore() and gc.getGame().getTargetScore() != 0):

					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_TARGET_SCORE", (gc.getGame().getTargetScore(), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#Rhye - start
					#screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, activePlayer.getCivilizationShortDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#Rhye - end
					screen.setTableText(szTable, 3, iRow, (u"%d" % ourScore), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

					if (iBestScoreTeam != -1):
						#Rhye - start
						#screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestScoreTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 4, iRow, gc.getPlayer(iBestScoreTeam).getCivilizationShortDescription(0) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#Rhye - end
						screen.setTableText(szTable, 5, iRow, (u"%d" % bestScore), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

					bEntriesFound = True

				if (victory.isEndScore()):

					szText1 = localText.getText("TXT_KEY_VICTORY_SCREEN_HIGHEST_SCORE", (CyGameTextMgr().getTimeStr(gc.getGame().getStartTurn() + gc.getGame().getMaxTurns(), false), ))

					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, szText1, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#Rhye - start
					#screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, activePlayer.getCivilizationShortDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#Rhye - end
					screen.setTableText(szTable, 3, iRow, (u"%d" % ourScore), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

					if (iBestScoreTeam != -1):
						#Rhye - start
						#screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestScoreTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 4, iRow, gc.getPlayer(iBestScoreTeam).getCivilizationShortDescription(0) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#Rhye - end
						screen.setTableText(szTable, 5, iRow, (u"%d" % bestScore), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

					bEntriesFound = True

				if (victory.isConquest() and iLoopVC != 7): #Rhye
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_ELIMINATE_ALL", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_RIVALS_LEFT", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 3, iRow, unicode(nRivals), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					bEntriesFound = True

				if (gc.getGame().getAdjustedPopulationPercent(iLoopVC) > 0):
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_POP", (gc.getGame().getAdjustedPopulationPercent(iLoopVC), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#Rhye - start
					#screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, activePlayer.getCivilizationShortDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#Rhye - end
					screen.setTableText(szTable, 3, iRow, (u"%.2f%%" % popPercent), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if (iBestPopTeam != -1):
						#Rhye - start
						#screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestPopTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 4, iRow, gc.getPlayer(iBestPopTeam).getCivilizationShortDescription(0) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#Rhye - end
						screen.setTableText(szTable, 5, iRow, (u"%.2f%%" % (bestPop * 100 / totalPop)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					bEntriesFound = True

				if (gc.getGame().getAdjustedLandPercent(iLoopVC) > 0):
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_LAND", (gc.getGame().getAdjustedLandPercent(iLoopVC), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#Rhye - start
					#screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, activePlayer.getCivilizationShortDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#Rhye - end
					screen.setTableText(szTable, 3, iRow, (u"%.2f%%" % landPercent), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if (iBestLandTeam != -1):
						#Rhye - start
						#screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestLandTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 4, iRow, gc.getPlayer(iBestLandTeam).getCivilizationShortDescription(0) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#Rhye - end
						screen.setTableText(szTable, 5, iRow, (u"%.2f%%" % (bestLand * 100 / totalLand)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					bEntriesFound = True

				if (victory.getReligionPercent() > 0):
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_RELIGION", (victory.getReligionPercent(), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if (iOurReligion != -1):
						screen.setTableText(szTable, 2, iRow, gc.getReligionInfo(iOurReligion).getDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 3, iRow, (u"%d%%" % ourReligionPercent), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					else:
						#Rhye - start
						#screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 2, iRow, activePlayer.getCivilizationShortDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#Rhye - end
						screen.setTableText(szTable, 3, iRow, u"No Holy City", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if (iBestReligion != -1):
						screen.setTableText(szTable, 4, iRow, gc.getReligionInfo(iBestReligion).getDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 5, iRow, (u"%d%%" % religionPercent), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					bEntriesFound = True

				if (victory.getTotalCultureRatio() > 0):
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_CULTURE", (int((100.0 * bestCulture) / victory.getTotalCultureRatio()), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#Rhye - start
					#screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					screen.setTableText(szTable, 2, iRow, activePlayer.getCivilizationShortDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#Rhye - end
					screen.setTableText(szTable, 3, iRow, unicode(ourCulture), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					if (iBestLandTeam != -1):
						#Rhye - start
						#screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestCultureTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 4, iRow, gc.getPlayer(iBestCultureTeam).getCivilizationShortDescription(0) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#Rhye - end
						screen.setTableText(szTable, 5, iRow, unicode(bestCulture), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					bEntriesFound = True

				iBestBuildingTeam = -1
				bestBuilding = 0
				for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
					if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
						if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
							teamBuilding = 0
							for i in range(gc.getNumBuildingClassInfos()):
								if (gc.getBuildingClassInfo(i).getVictoryThreshold(iLoopVC) > 0):
									teamBuilding += gc.getTeam(iLoopTeam).getBuildingClassCount(i)
							if (teamBuilding > bestBuilding):
								bestBuilding = teamBuilding
								iBestBuildingTeam = iLoopTeam

				for i in range(gc.getNumBuildingClassInfos()):
					if (gc.getBuildingClassInfo(i).getVictoryThreshold(iLoopVC) > 0):
						iRow = screen.appendTableRow(szTable)
						szNumber = unicode(gc.getBuildingClassInfo(i).getVictoryThreshold(iLoopVC))
						screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_BUILDING", (szNumber, gc.getBuildingClassInfo(i).getTextKey())), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#Rhye - start
						#screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 2, iRow, activePlayer.getCivilizationShortDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#Rhye - end
						screen.setTableText(szTable, 3, iRow, activePlayer.getTeam().getBuildingClassCount(i), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						if (iBestBuildingTeam != -1):
							#Rhye - start
							#screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestBuildingTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 4, iRow, gc.getPlayer(iBestBuildingTeam).getCivilizationShortDescription(0) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							#Rhye - end
							screen.setTableText(szTable, 5, iRow, gc.getTeam(iBestBuildingTeam).getBuildingClassCount(i), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						bEntriesFound = True

				iBestProjectTeam = -1
				bestProject = 0
				for iLoopTeam in range(gc.getMAX_CIV_TEAMS()):
					if (gc.getTeam(iLoopTeam).isAlive() and not gc.getTeam(iLoopTeam).isMinorCiv() and not gc.getTeam(iLoopTeam).isBarbarian()):
						if (iLoopTeam != iActiveTeam and (activePlayer.getTeam().isHasMet(iLoopTeam) or gc.getGame().isDebugMode())):
							teamProject = 0
							for i in range(gc.getNumProjectInfos()):
								if (gc.getProjectInfo(i).getVictoryThreshold(iLoopVC) > 0):
									teamProject += gc.getTeam(iLoopTeam).getProjectCount(i)
							if (teamProject > bestProject):
								bestProject = teamProject
								iBestProjectTeam = iLoopTeam

				for i in range(gc.getNumProjectInfos()):
					if (gc.getProjectInfo(i).getVictoryThreshold(iLoopVC) > 0):
						iRow = screen.appendTableRow(szTable)
						if (gc.getProjectInfo(i).getVictoryMinThreshold(iLoopVC) == gc.getProjectInfo(i).getVictoryThreshold(iLoopVC)):
							szNumber = unicode(gc.getProjectInfo(i).getVictoryThreshold(iLoopVC))
						else:
							szNumber = unicode(gc.getProjectInfo(i).getVictoryMinThreshold(iLoopVC)) + u"-" + unicode(gc.getProjectInfo(i).getVictoryThreshold(iLoopVC))
						screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_BUILDING", (szNumber, gc.getProjectInfo(i).getTextKey())), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#Rhye - start
						#screen.setTableText(szTable, 2, iRow, activePlayer.getTeam().getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 2, iRow, activePlayer.getCivilizationShortDescription() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#Rhye - end
						screen.setTableText(szTable, 3, iRow, str(activePlayer.getTeam().getProjectCount(i)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

						#check if spaceship
						#if (gc.getProjectInfo(i).isSpaceship() and (activePlayer.getTeam().getProjectCount(i) > 0)):
						if (gc.getProjectInfo(i).isSpaceship()):
							bSpaceshipFound = True

						if (iBestProjectTeam != -1):
							#Rhye - start
							#screen.setTableText(szTable, 4, iRow, gc.getTeam(iBestProjectTeam).getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 4, iRow, gc.getPlayer(iBestProjectTeam).getCivilizationShortDescription(0) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							#Rhye - end
							screen.setTableText(szTable, 5, iRow, unicode(gc.getTeam(iBestProjectTeam).getProjectCount(i)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						bEntriesFound = True

				#add spaceship button
				if (bSpaceshipFound):
					screen.setButtonGFC("SpaceShipButton" + str(iLoopVC), localText.getText("TXT_KEY_GLOBELAYER_STRATEGY_VIEW", ()), "", 0, 0, 15, 10, WidgetTypes.WIDGET_GENERAL, self.SPACESHIP_SCREEN_BUTTON, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
					screen.attachControlToTableCell("SpaceShipButton" + str(iLoopVC), szTable, iVictoryTitleRow, 1)

					victoryDelay = gc.getTeam(iActiveTeam).getVictoryCountdown(iLoopVC)
					if((victoryDelay > 0) and (gc.getGame().getGameState() != GameStateTypes.GAMESTATE_EXTENDED)):
						victoryDate = CyGameTextMgr().getTimeStr(gc.getGame().getGameTurn() + victoryDelay, false)
						screen.setTableText(szTable, 2, iVictoryTitleRow, localText.getText("TXT_KEY_SPACE_SHIP_SCREEN_ARRIVAL", ()) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 3, iVictoryTitleRow, victoryDate, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 4, iVictoryTitleRow, localText.getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()) + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						screen.setTableText(szTable, 5, iVictoryTitleRow, str(victoryDelay), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

				if (victory.isDiploVote()):
					for (iVoteBuildingClass, iUNTeam, bUnknown) in aiVoteBuildingClass:
						iRow = screen.appendTableRow(szTable)
						screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_ELECTION", (gc.getBuildingClassInfo(iVoteBuildingClass).getTextKey(), )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						if (iUNTeam != -1):
							if bUnknown:
								szName = localText.getText("TXT_KEY_TOPCIVS_UNKNOWN", ())
							else:
								#Rhye - start
								#szName = gc.getTeam(iUNTeam).getName()
								szName = gc.getPlayer(iUNTeam).getCivilizationShortDescription(0)
								#Rhye - end
							screen.setTableText(szTable, 2, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_BUILT", (szName, )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						else:
							screen.setTableText(szTable, 2, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_NOT_BUILT", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						bEntriesFound = True

				if (victory.getCityCulture() != CultureLevelTypes.NO_CULTURELEVEL and victory.getNumCultureCities() > 0):
					ourBestCities = self.getListCultureCities(self.iActivePlayer)[0:victory.getNumCultureCities()]

					iBestCulturePlayer = -1
					bestCityCulture = 0
					maxCityCulture = gc.getCultureLevelInfo(victory.getCityCulture()).getSpeedThreshold(gc.getGame().getGameSpeedType())
					for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						if (gc.getPlayer(iLoopPlayer).isAlive() and not gc.getPlayer(iLoopPlayer).isMinorCiv() and not gc.getPlayer(iLoopPlayer).isBarbarian()):
							if (iLoopPlayer != self.iActivePlayer and (activePlayer.getTeam().isHasMet(gc.getPlayer(iLoopPlayer).getTeam()) or gc.getGame().isDebugMode())):
								theirBestCities = self.getListCultureCities(iLoopPlayer)[0:victory.getNumCultureCities()]

								iTotalCulture = 0
								for loopCity in theirBestCities:
									if loopCity[0] >= maxCityCulture:
										iTotalCulture += maxCityCulture
									else:
										iTotalCulture += loopCity[0]

								if (iTotalCulture >= bestCityCulture):
									bestCityCulture = iTotalCulture
									iBestCulturePlayer = iLoopPlayer

					if (iBestCulturePlayer != -1):
						theirBestCities = self.getListCultureCities(iBestCulturePlayer)[0:(victory.getNumCultureCities())]
					else:
						theirBestCities = []

					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_CITY_CULTURE", (victory.getNumCultureCities(), gc.getCultureLevelInfo(victory.getCityCulture()).getTextKey())), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

					for i in range(victory.getNumCultureCities()):
						if (len(ourBestCities) > i):
							screen.setTableText(szTable, 2, iRow, ourBestCities[i][1].getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 3, iRow, str(ourBestCities[i][0]), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						if (len(theirBestCities) > i):
							screen.setTableText(szTable, 4, iRow, theirBestCities[i][1].getName() + ":", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
							screen.setTableText(szTable, 5, iRow, unicode(theirBestCities[i][0]), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						if (i < victory.getNumCultureCities()-1):
							iRow = screen.appendTableRow(szTable)
					bEntriesFound = True

				#Rhye - start # 3Miro: this should never get called
				#if (iLoopVC == 7):
					#for i in range(3):
						#iRow = screen.appendTableRow(szTable)
						#screen.setTableText(szTable, 0, iRow, localText.getText(con.tGoals[self.iActivePlayer][i], ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#screen.setTableText(szTable, 2, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_ACCOMPLISHED", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#if (utils.getGoal(self.iActivePlayer, i) == 1):
							#screen.setTableText(szTable, 3, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_YES", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#elif (utils.getGoal(self.iActivePlayer, i) == 0):
							#screen.setTableText(szTable, 3, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_NO", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
						#else:
							#screen.setTableText(szTable, 3, iRow, localText.getText("TXT_KEY_VICTORY_SCREEN_NOTYET", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
					#bEntriesFound = True
				#Rhye - end

				if (bEntriesFound and (iLoopVC < 4)): # 3Miro: last one appends 2 rows
					screen.appendTableRow(szTable)
					screen.appendTableRow(szTable)

		self.drawCleanerVictoryConditions()

		# civ picker dropdown
		if (CyGame().isDebugMode()):
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		self.drawTabs()

	def getListCultureCities(self, iPlayer):
		if iPlayer >= 0:
			player = PyPlayer(iPlayer)
			if player.isAlive():
				cityList = player.getCityList()
				listCultureCities = len(cityList) * [(0, 0)]
				i = 0
				for city in cityList:
					listCultureCities[i] = (city.getCulture(), city)
					i += 1
				listCultureCities.sort()
				listCultureCities.reverse()
				return listCultureCities
		return []


	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0


	# handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getFunctionName() == self.DEBUG_DROPDOWN_ID):
				szName = self.DEBUG_DROPDOWN_ID
				iIndex = self.getScreen().getSelectedPullDownID(szName)
				self.iActivePlayer = self.getScreen().getPullDownData(szName, iIndex)
				self.iScreen = VICTORY_CONDITION_SCREEN
				self.showVictoryConditionScreen()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.VC_TAB_ID):
				self.iScreen = VICTORY_CONDITION_SCREEN
				self.showVictoryConditionScreen()
			elif (inputClass.getFunctionName() == self.SETTINGS_TAB_ID):
				self.iScreen = GAME_SETTINGS_SCREEN
				self.showGameSettingsScreen()
			elif (inputClass.getFunctionName() == self.UN_RESOLUTION_TAB_ID):
				self.iScreen = UN_RESOLUTION_SCREEN
				self.showVotingScreen()
			elif (inputClass.getFunctionName() == self.UN_MEMBERS_TAB_ID):
				self.iScreen = UN_MEMBERS_SCREEN
				self.showMembersScreen()
			elif (inputClass.getData1() == self.SPACESHIP_SCREEN_BUTTON):
				#close screen
				screen = self.getScreen()
				screen.setDying(True)
				CyInterface().clearSelectedCities()

				#popup spaceship screen
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(-1)
				popupInfo.setText(u"showSpaceShip")
				popupInfo.addPopup(self.iActivePlayer)

	def update(self, fDelta):
		return

	def getCivHelpsTexts(self):
		dCivs = { con.iByzantium : self.getByzantiumText(),
		con.iFrankia : self.getFrankiaText(),
		con.iArabia : self.getArabiaText(),
		con.iBulgaria : self.getBulgariaText(),
		con.iCordoba : self.getCordobaText(),
		con.iVenecia : self.getVeneciaText(),
		con.iBurgundy : self.getBurgundyText(),
		con.iGermany : self.getGermanyText(),
		con.iNovgorod : self.getNovgorodText(),
		con.iNorway : self.getNorwayText(),
		con.iKiev : self.getKievText(),
		con.iHungary : self.getHungaryText(),
		con.iSpain : self.getSpainText(),
		con.iDenmark : self.getDenmarkText(),
		con.iScotland : self.getScotlandText(),
		con.iPoland : self.getPolandText(),
		con.iGenoa : self.getGenoaText(),
		con.iMorocco : self.getMoroccoText(),
		con.iEngland : self.getEnglandText(),
		con.iPortugal : self.getPortugalText(),
		con.iAragon : self.getAragonText(),
		con.iSweden : self.getSwedenText(),
		con.iPrussia : self.getPrussiaText(),
		con.iLithuania : self.getLithuaniaText(),
		con.iAustria : self.getAustriaText(),
		con.iTurkey : self.getTurkeyText(),
		con.iMoscow : self.getMoscowText(),
		con.iDutch : self.getDutchText(),
		}
		lHelpTexts = dCivs[self.iActivePlayer]
		return lHelpTexts

	def getByzantiumText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		tProvsToCheck = vic.tByzantiumControl
		iNumCities = 0
		for iProv in tProvsToCheck:
			iNumCities += pPlayer.getProvinceCityCount( iProv )
		sText1 += localText.getText("TXT_KEY_UHV_CITIES_CONTROLLED",()) + " " + self.determineColor(iNumCities >= 6, str(iNumCities))
		#UHV2
		sText2 += self.getProvinceString(vic.tByzantiumControlII)
		#UHV3
		tConstantinople = con.tCapitals[iPlayer]
		pConstantinople = gc.getMap().plot( tConstantinople[0], tConstantinople[1] ).getPlotCity()
		sConstantinopleName = localText.getText("TXT_KEY_CITY_NAME_CONSTANTINOPLE",())
		if self.checkCity(tConstantinople, iPlayer, sConstantinopleName) == -1:
			sLargest = sConstantinopleName +" "+ localText.getText("TXT_KEY_UHV_IS_LARGEST",())
			sNotLargest = sConstantinopleName +" "+ localText.getText("TXT_KEY_UHV_IS_NOT_LARGEST",())
			sCultural = sConstantinopleName +" "+ localText.getText("TXT_KEY_UHV_IS_CULTURAL",())
			sNotCultural = sConstantinopleName +" "+ localText.getText("TXT_KEY_UHV_IS_NOT_CULTURAL",())
			sText3 += self.determineColor(gc.isLargestCity(tConstantinople[0], tConstantinople[1]), sLargest, sNotLargest)
			sText3 += "\n" + self.determineColor(gc.isTopCultureCity(tConstantinople[0], tConstantinople[1]), sCultural, sNotCultural)
		else:
			sText3 += self.checkCity(tConstantinople, iPlayer, sConstantinopleName)
		sText3 += "\n" + self.RichestString()
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getFrankiaText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tFrankControl)
		#UHV2
		tPlot = con.tJerusalem
		sText2 += self.checkCity(tPlot, iPlayer, localText.getText("TXT_KEY_UHV_JERUSALEM",()), True)
		#UHV3
		sText3 += self.getNumColoniesString(5)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getArabiaText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tArabiaControlI)
		#sText1 += self.getMultiProvinceString([(vic.tArabiaControlI, xml.i955AD), (vic.tArabiaControlII, xml.i1291AD)])
		#UHV2
		iMostAdvancedCiv = utils.getMostAdvancedCiv()
		if iMostAdvancedCiv != -1:
			pMostAdvancedCiv = gc.getPlayer(iMostAdvancedCiv)
			sCivShortName = str(pMostAdvancedCiv.getCivilizationShortDescriptionKey())
			sText2 += localText.getText("TXT_KEY_UHV_MOST_ADVANCED_CIV", ()) + ": " + self.determineColor(iMostAdvancedCiv == iPlayer, localText.getText(sCivShortName, ()))
		else:
			sText2 += localText.getText("TXT_KEY_UHV_MOST_ADVANCED_CIV", ()) + ": " + u"<color=208,0,0>%s</color>" %(localText.getText("TXT_KEY_UHV_NO_MOST_ADVANCED_CIV",()))
		sText2 += "\n" + self.getProvinceString(vic.tArabiaControlII)
		#UHV3
		iPerc = gc.getGame().calculateReligionPercent( xml.iIslam )
		sText3 += localText.getText("TXT_KEY_UHV_ISLAM",()) + ": " + self.determineColor(iPerc > 35, str(iPerc)) + " %"
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getBulgariaText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tBulgariaControl)
		#UHV2
		iFaith = pPlayer.getFaith()
		sText2 += localText.getText("TXT_KEY_UHV_FAITH_POINTS",()) + ": "  + self.determineColor(iFaith >= 100, str(iFaith))
		#UHV3
		iGoal = pPlayer.getUHV( 2 )
		sText3 += self.determineColor(iGoal != 0, localText.getText("TXT_KEY_UHV_NO_CITIES_LOST", ()))
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getCordobaText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		tCordoba = con.tCapitals[iPlayer]
		pCordoba = gc.getMap().plot( tCordoba[0], tCordoba[1] ).getPlotCity()
		sCordobaName = localText.getText("TXT_KEY_CITY_NAME_CORDOBA",())
		if self.checkCity(tCordoba, iPlayer, sCordobaName) == -1:
			sLargest = sCordobaName +" "+ localText.getText("TXT_KEY_UHV_IS_LARGEST",())
			sNotLargest = sCordobaName +" "+ localText.getText("TXT_KEY_UHV_IS_NOT_LARGEST",())
			sText1 += self.determineColor(gc.isLargestCity(tCordoba[0], tCordoba[1]), sLargest, sNotLargest)
		else:
			sText1 += self.checkCity(tCordoba, iPlayer, sCordobaName)
		#UHV2
		sText2 += self.getWonderString(vic.tCordobaWonders)
		#UHV3
		sText3 += self.getReligionProvinceString(vic.tCordobaIslamize, xml.iIslam, 1)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getVeneciaText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tVenetianControl)
		#UHV2
		tConstantinople = con.tCapitals[con.iByzantium]
		sText2 += self.checkCity(tConstantinople, iPlayer, localText.getText("TXT_KEY_CITY_NAME_CONSTANTINOPLE",()), True)
		sText2 += "\n" + self.getProvinceString(vic.tVenetianControlII)
		#UHV3
		iGoal = pPlayer.getUHV( 2 )
		sText3 += self.determineColor(iGoal == -1, localText.getText("TXT_KEY_UHV_NO_COLONIES_YET", ()))
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getBurgundyText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		iCulture = pPlayer.getUHVCounter( 0 )
		sText1 += localText.getText("TXT_KEY_UHV_CULTURE",()) + ": " + self.determineColor(iCulture >= 12000, str(iCulture))
		#UHV2
		sText2 += self.getProvinceString(vic.tBurgundyControl)
		#UHV3
		sText3 += self.checkScores(vic.tBurgundyOutrank)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getGermanyText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tGermanyControl)
		#UHV2
		iGoal = pPlayer.getUHV( 1 )
		sTextGood = localText.getText("TXT_KEY_UHV_NOT_FOUND_YET", ())
		sText2 += self.determineColor(iGoal != 0, gc.getReligionInfo(xml.iProtestantism).getDescription() + " " + sTextGood)
		#UHV3
		sText3 += self.getProvinceString(vic.tGermanyControlII)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getNovgorodText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tNovgorodControl)
		#UHV2
		iNumFurs = pPlayer.countCultBorderBonuses(xml.iFur)
		sText2 += self.getCounterString(iNumFurs, 11)
		#UHV3
		sText3 += self.ConquerOrVassal([[con.iMoscow, xml.iP_Moscow]])
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getNorwayText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += localText.getText("TXT_KEY_UHV_NOR1_HELP",()) + "\n"
		iCount = pPlayer.getUHVCounter( 2 )
		sText1 += self.getCounterString(iCount, 100)
		sText1 += "\n" + localText.getText("TXT_KEY_PROJECT_VINLAND",()) + ": " + self.determineColor(gc.getTeam(iPlayer).getProjectCount(xml.iColVinland) >= 1, localText.getText("TXT_KEY_UHV_EXPLORED",()), localText.getText("TXT_KEY_UHV_NOT_EXPLORED",()))
		#UHV2
		sText2 += self.getProvinceString(vic.tNorwayControl)
		#UHV3
		sText3 += self.checkScores(vic.tNorwayOutrank)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getKievText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		iKievCath = pPlayer.countNumBuildings(xml.iOrthodoxCathedral)
		iKievMona = pPlayer.countNumBuildings(xml.iOrthodoxMonastery)
		sKievCath = localText.getText("TXT_KEY_BUILDING_ORTHODOX_CATHEDRAL",()) + ": "
		sKievMona = localText.getText("TXT_KEY_BUILDING_ORTHODOX_MONASTERY",()) + ": "
		sText1 += sKievCath + self.determineColor(iKievCath >= 2, str(iKievCath))
		sText1 += "\n" + sKievMona + self.determineColor(iKievMona >= 8, str(iKievMona))
		#UHV2
		sText2 += self.getProvinceString(vic.tKievControl, (True, 10))
		#UHV3
		iFood = pPlayer.getUHVCounter( 2 )
		sText3 += self.getCounterString(iFood, 25000)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getHungaryText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tHungaryControl)
		#UHV2
		sText2 += self.getNotCivProvinceString(con.iTurkey, vic.tHungaryControlII)
		#UHV3
		iGoal = pPlayer.getUHV( 2 )
		sText3 += self.determineColor(iGoal != 0, localText.getText("TXT_KEY_UHV_NO_ADOPTION_YET", ()))
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getSpainText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getReligionProvinceString(vic.tSpainConvert, xml.iCatholicism, 2)
		#UHV2
		iSpainColonies = vic.Victory().getNumRealColonies(iPlayer)
		iOtherColonies = 0
		iColonyPlayer = -1
		for iCiv in range( con.iNumPlayers ):
			if iCiv == iPlayer: continue
			if ( gc.getPlayer( iCiv ).isAlive() ):
				iTempNumColonies = vic.Victory().getNumRealColonies(iCiv)
				if (iTempNumColonies > iOtherColonies):
					iOtherColonies = iTempNumColonies
					iColonyPlayer = iCiv
		sText = localText.getText("TXT_KEY_UHV_COLONIES",())
		sUnit = ""
		sText2 += self.getCompetition(iSpainColonies, iOtherColonies, iColonyPlayer, sText, sUnit, 3)
		#UHV3
		lLand = [ 0, 0, 0, 0, 0, 0 ] # Prot, Islam, Cath, Orth, Jew, Pagan
		lPop  = [ 0, 0, 0, 0, 0, 0 ]
		for iLoopPlayer in range( con.iNumPlayers ):
			pLoopPlayer = gc.getPlayer( iLoopPlayer )
			iStateReligion = pLoopPlayer.getStateReligion()
			if ( iStateReligion > -1 ):
				lLand[ iStateReligion ] += pLoopPlayer.getTotalLand()
				lPop[ iStateReligion ] += pLoopPlayer.getTotalPopulation()
			else:
				lLand[ 5 ] += pLoopPlayer.getTotalLand()
				lPop[ 5 ] += pLoopPlayer.getTotalPopulation()
		iBestLand = xml.iCatholicism
		iBestPop = xml.iCatholicism
		for iReligion in range( xml.iNumReligions + 1 ):
			if ( iReligion != xml.iCatholicism ):
				if ( lLand[ iReligion ] > lLand[ iBestLand ] ):
					iBestLand = iReligion
				if ( lPop[ iReligion ] > lPop[ iBestPop ] ):
					iBestPop = iReligion
		if ( iBestLand == 5 ):
			sBestR = localText.getText("TXT_KEY_UHV_PAGAN",())
		else:
			sBestR = localText.getText( gc.getReligionInfo(iBestLand).getAdjectiveKey().encode('ascii', 'replace'), () )
		sText3 += localText.getText("TXT_KEY_UHV_MOST_LAND",()) + " " + self.determineColor(iBestLand == xml.iCatholicism, sBestR)
		if ( iBestPop == 5 ):
			sBestR = localText.getText("TXT_KEY_UHV_PAGAN",())
		else:
			sBestR = localText.getText( gc.getReligionInfo(iBestPop).getAdjectiveKey().encode('ascii', 'replace'), () )
		sText3 += "\n" + localText.getText("TXT_KEY_UHV_MOST_POPULATION",()) + " " + self.determineColor(iBestLand == xml.iCatholicism, sBestR)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getDenmarkText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tDenmarkControlI)
		#UHV2
		sText2 += self.getProvinceString(vic.tDenmarkControlIII)
		#UHV3
		sText3 += self.getNumColoniesString(3, True)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getScotlandText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		iScotlandFort = gc.getPlayer(con.iScotland).getImprovementCount( xml.iImprovementFort )
		iScotlandCastle = gc.getPlayer(con.iScotland).countNumBuildings(xml.iCastle)
		sScotlandFort = localText.getText("TXT_KEY_IMPROVEMENT_FORT",()) + ": "
		sScotlandCastle = localText.getText("TXT_KEY_BUILDING_CASTLE",()) + ": "
		sText1 += sScotlandFort + self.determineColor(iScotlandFort >= 10, str(iScotlandFort))
		sText1 += "\n" + sScotlandCastle + self.determineColor(iScotlandCastle >= 4, str(iScotlandCastle))
		#UHV2
		sText2 += localText.getText("TXT_KEY_UHV_SCO2_HELP",()) + "\n"
		iScore = pPlayer.getUHVCounter(1)
		sText2 += self.getCounterString(iScore, 1500)
		#UHV3
		sText3 += self.getProvinceString(vic.tScotlandControl)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getPolandText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		if gc.getGame().getGameTurn() < xml.i1500AD:
			sText1 += localText.getText("TXT_KEY_UHV_TOO_EARLY",()) + "\n"
		iPolandFood = pPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD)
		iOtherFood = 0
		iFoodPlayer = -1
		for iLoopPlayer in range( con.iNumMajorPlayers ):
			if iLoopPlayer == iPlayer: continue
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if pLoopPlayer.isAlive():
				iTempFood = pLoopPlayer.calculateTotalYield(YieldTypes.YIELD_FOOD)
				if iTempFood > iOtherFood:
					iOtherFood = iTempFood
					iFoodPlayer = iLoopPlayer
		sText = localText.getText("TXT_KEY_UHV_FOOD_PRODUCTION",())
		sUnit = "%s" %( u"<font=5>%c</font>" %( gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar()) )
		sText1 += self.getCompetition(iPolandFood, iOtherFood, iFoodPlayer, sText, sUnit)
		#UHV2
		tProvsToCheck = vic.tPolishControl
		iNumCities = 0
		for iProv in tProvsToCheck:
			iNumCities += pPlayer.getProvinceCityCount( iProv )
		sText2 += localText.getText("TXT_KEY_UHV_CITIES_CONTROLLED",()) + " " + self.determineColor(iNumCities >= 12, str(iNumCities))
		#UHV3
		iCounter = pPlayer.getUHVCounter( 2 )
		iCathCath = ( iCounter / 10000 ) % 10
		iOrthCath = ( iCounter / 1000 ) % 10
		iProtCath = ( iCounter / 100 ) % 10
		iJewishQu = iCounter % 100
		sCathCath = localText.getText("TXT_KEY_BUILDING_CATHOLIC_CATHEDRAL",()) + ": "
		sOrthCath = localText.getText("TXT_KEY_BUILDING_ORTHODOX_CATHEDRAL",()) + ": "
		sProtCath = localText.getText("TXT_KEY_BUILDING_PROTESTANT_CATHEDRAL",()) + ": "
		sJewishQu = localText.getText("TXT_KEY_BUILDING_JEWISH_QUARTER",()) + ": "
		sCathCath += self.determineColor(iCathCath >= 3, str(iCathCath))
		sOrthCath += self.determineColor(iOrthCath >= 3, str(iOrthCath))
		sProtCath += self.determineColor(iProtCath >= 2, str(iProtCath))
		if ( iJewishQu == 99 ):
			sKazimierzWonder = localText.getText("TXT_KEY_BUILDING_KAZIMIERZ",())
			sJewishQu += u" <color=0,255,0>%s</color>" %(sKazimierzWonder)
		else:
			sJewishQu += self.determineColor(iJewishQu >= 2, str(iJewishQu))
		sText3 += sCathCath + "   " + sOrthCath + "   " + sProtCath + "   " + sJewishQu
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getGenoaText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tGenoaControl)
		#UHV2
		iGenoaTrade = pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE) + pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
		iOtherTrade = 0
		iBiggestTrader = -1
		for iLoopPlayer in range( con.iNumPlayers ):
			if iLoopPlayer == iPlayer: continue
			pLoopPlayer = gc.getPlayer( iLoopPlayer )
			if not pLoopPlayer.isAlive(): continue
			iTrade = pLoopPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE) + pLoopPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
			if ( iTrade > iOtherTrade ):
				iOtherTrade = iTrade
				iBiggestTrader = iLoopPlayer
		sTextTmp = localText.getText("TXT_KEY_UHV_IMPORT_EXPORT",())
		sUnit = "%s" %( u"<font=5>%c</font>" %( gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar()) )
		sText2 += self.getCompetition(iGenoaTrade, iOtherTrade, iBiggestTrader, sTextTmp, sUnit)
		#UHV3
		iBankCount = 0
		for city in utils.getCityList(iPlayer):
			if city.getNumRealBuilding(xml.iBank) > 0 or city.getNumRealBuilding(xml.iGenoaBank) > 0 or city.getNumRealBuilding(xml.iEnglishRoyalExchange) > 0:
				iBankCount += 1
		iCompanyCities = pPlayer.countCorporations(xml.iStGeorge)
		sText3 += localText.getText("TXT_KEY_UHV_BANKS",()) + ": " + self.determineColor(iBankCount >= 8, str(iBankCount))
		sText3 += "\n" + localText.getText("TXT_KEY_UHV_COMPANIES",()) + ": " + self.determineColor(iCompanyCities == xml.tCompaniesLimit[xml.iStGeorge], str(iCompanyCities))
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getMoroccoText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tMoroccoControl)
		#UHV2
		victory = gc.getVictoryInfo(4) #Cultural victory
		ourBestCities = self.getListCultureCities(self.iActivePlayer)[0:victory.getNumCultureCities()]
		sText2 += localText.getText("TXT_KEY_UHV_MOR2_HELP", ()) + "\n"
		for i in range(3):
			if (len(ourBestCities) > i):
				sText2 += "  " + ourBestCities[i][1].getName() + ": " + self.determineColor(ourBestCities[i][0] >= 5000, ourBestCities[i][0])
		#UHV3
		sText3 += self.CollapseOrVassal([con.iSpain, con.iPortugal, con.iAragon])
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getEnglandText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tEnglandControl)
		#UHV2
		sText2 += self.getNumColoniesString(7)
		#UHV3
		iGoal = pPlayer.getUHV( 2 )
		sText3 += self.determineColor(iGoal != 0, localText.getText("TXT_KEY_UHV_NO_INDUSTRIAL", ()))
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getPortugalText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		iCounter = pPlayer.getUHVCounter( 0 )
		iIslands = iCounter % 100
		iAfrica = iCounter / 100
		sText1 += localText.getText("TXT_KEY_UHV_CITIES_IN_ISLANDS",()) + ": " + self.determineColor(iIslands >= 3, str(iIslands))
		sText1 += "\n" + localText.getText("TXT_KEY_UHV_CITIES_IN_AFRICA",()) + ": " + self.determineColor(iAfrica >= 2, str(iAfrica))
		#UHV2
		iGoal = pPlayer.getUHV( 1 )
		sText2 += self.determineColor(iGoal != 0, localText.getText("TXT_KEY_UHV_NO_CITIES_LOST", ()))
		#UHV3
		sText3 += self.getNumColoniesString(5)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getAragonText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tAragonControlI)
		#UHV2
		iSeaports = pPlayer.countNumBuildings(xml.iAragonSeaport)
		iCargoShips = utils.getCargoShips(con.iAragon)
		sText2 += localText.getText("TXT_KEY_UHV_CURRENTLY",()) + ": " + self.determineColor(iSeaports >= 12, str(iSeaports)) + " " + localText.getText("TXT_KEY_UHV_SEAPORTS",()) + ", "
		sText2 += self.determineColor(iCargoShips >= 30, str(iCargoShips)) + " " + localText.getText("TXT_KEY_UHV_TRADE_SHIPS",())
		#UHV3
		sText3 += self.getProvinceString(vic.tAragonControlII)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getSwedenText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		iCounter = 0
		for iProv in vic.tSwedenControl:
			iCounter += pPlayer.getProvinceCityCount(iProv)
		sText1 += self.getCounterString(iCounter, 6)
		#UHV2
		iCounter = pPlayer.getUHVCounter(1)
		sText2 += self.getCounterString(iCounter, 5)
		#UHV3
		iCounter = up.getNumForeignCitiesOnBaltic(iPlayer, True)
		sText3 += self.getCounterString(iCounter, 0, True)
		sText3 += " " + localText.getText("TXT_KEY_UHV_BALTIC_CITIES",())
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getPrussiaText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tPrussiaControlI)
		#UHV2
		if gc.getGame().getGameTurn()  >= xml.i1650AD:
			iConqRaw = gc.getPlayer(con.iPrussia).getUHVCounter(1)
			for iI in range(len(vic.tPrussiaDefeat)):
				iNumConq = (iConqRaw / pow(10,iI)) % 10
				pVictim = gc.getPlayer(vic.tPrussiaDefeat[iI])
				if(iNumConq < 9):
					szNumConq = " %d" % iNumConq
				else:
					szNumConq = ">8"
				sText2 +=  "  " + self.determineColor(not (iNumConq < 2 and pVictim.isAlive()), localText.getText(str(pVictim.getCivilizationShortDescriptionKey()), ()) + ":" + szNumConq)
		else:
			sText2 += localText.getText("TXT_KEY_UHV_TOO_EARLY",())
		#UHV3
		pCapital = gc.getPlayer(iPlayer).getCapitalCity()
		iGPStart = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_PRIEST")
		iGPEnd = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_SPY")
		iCounter = 0
		for iType in range(iGPStart, iGPEnd+1):
			iCounter += pCapital.getFreeSpecialistCount(iType)
		if iCounter < 0:
			iCounter = 0
		sText3 += self.getCounterString(iCounter, 15)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getLithuaniaText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		iCulture = pPlayer.getUHVCounter( 0 )
		sText1 += self.getCounterString(iCulture, 2500)
		#UHV2
		iCount, iTotal = vic.Victory().getTerritoryPercentEurope(iPlayer, True)
		iOtherCount = 0
		iMostPlayer = -1
		for iLoopPlayer in range( con.iNumMajorPlayers ):
			if iLoopPlayer == iPlayer: continue
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if pLoopPlayer.isAlive():
				iTempCount = vic.Victory().getTerritoryPercentEurope(iLoopPlayer)
				if iTempCount > iOtherCount:
					iOtherCount = iTempCount
					iMostPlayer = iLoopPlayer
		if (iCount > 0):
			landPercent = (iCount * 100.0) / iTotal
		else:
			landPercent = 0.0
		if (iOtherCount > 0):
			otherlandPercent = (iOtherCount * 100.0) / iTotal
		else:
			otherlandPercent = 0.0
		sText = localText.getText("TXT_KEY_UHV_CONTROL_TERRITORY",())
		sText2 += self.getLandCompetition(landPercent, otherlandPercent, iMostPlayer, sText)
		#UHV3
		sText3 += self.CollapseOrVassal([con.iMoscow, con.iNovgorod, con.iPrussia])
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getAustriaText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tAustriaControl)
		#UHV2
		iCount = 0
		for iLoopPlayer in range( con.iNumMajorPlayers ):
			pLoopPlayer = gc.getPlayer( iLoopPlayer )
			if ( iLoopPlayer != iPlayer and pLoopPlayer.isAlive() ):
				if ( gc.getTeam( pLoopPlayer.getTeam() ).isVassal( iPlayer ) ):
					iCount += 1
		sText2 += self.getCounterString(iCount, 3)
		#UHV3
		iBestCiv = gc.getGame().getRankPlayer(0)
		pBestCiv = gc.getPlayer(iBestCiv)
		sCivShortName = str(pBestCiv.getCivilizationShortDescriptionKey())
		sText3 += localText.getText("TXT_KEY_UHV_HIGHEST_SCORE", ()) + ": " + self.determineColor(iBestCiv == iPlayer, localText.getText(sCivShortName, ()))
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getTurkeyText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getProvinceString(vic.tOttomanControlI)
		#UHV2
		sText2 += self.getWonderString(vic.tOttomanWonders)
		#UHV3
		sText3 += self.getProvinceString(vic.tOttomanControlII)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getMoscowText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		sText1 += self.getNotCivProvinceString(con.iBarbarian, vic.tMoscowControl)
		#UHV2
		totalLand = gc.getMap().getLandPlots()
		RussianLand = pPlayer.getTotalLand()
		if (totalLand > 0):
			landPercent = (RussianLand * 100.0) / totalLand
		else:
			landPercent = 0.0
		sText2 += self.getCounterString(landPercent, 25, False, True) + " %"
		#UHV3
		bColor = False
		iNumAccess = pPlayer.countCultBorderBonuses(xml.iAccess)
		tConstantinople = con.tCapitals[con.iByzantium]
		iConstantinopleOwner = gc.getMap().plot( tConstantinople[0], tConstantinople[1] ).getPlotCity().getOwner()
		if iNumAccess > 0 or iConstantinopleOwner == iPlayer:
			bColor = True
		sText3 += localText.getText("TXT_KEY_BONUS_ACCESS",()) + ": " + self.determineColor(bColor, str(iNumAccess))
		if self.checkCity(tConstantinople, con.iMoscow, localText.getText("TXT_KEY_CITY_NAME_CONSTANTINOPLE",()), True, True) == -1:
			sText3 += "\n" + localText.getText("TXT_KEY_UHV_CONTROLLER_OF",()) + " " + localText.getText("TXT_KEY_CITY_NAME_CONSTANTINOPLE",()) + ": " + self.determineColor(bColor, gc.getPlayer(iConstantinopleOwner).getName())
		else:
			sText3 += self.checkCity(tConstantinople, con.iMoscow, localText.getText("TXT_KEY_CITY_NAME_CONSTANTINOPLE",()), True, True)
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getDutchText(self):
		iPlayer = self.iActivePlayer
		pPlayer = gc.getPlayer(iPlayer)
		sText1, sText2, sText3 = self.getEmptyTexts()
		#UHV1
		tAmsterdam = con.tCapitals[iPlayer]
		pPlot = gc.getMap().plot( tAmsterdam[0], tAmsterdam[1])
		if self.checkCity(tAmsterdam, iPlayer, localText.getText("TXT_KEY_CITY_NAME_AMSTERDAM",())) == -1:
			iNumMerchants = pPlot.getPlotCity().getFreeSpecialistCount(xml.iSpecialistGreatMerchant)
			sText1 += self.getCounterString(iNumMerchants, 5)
		else:
			sText1 += self.checkCity(tAmsterdam, iPlayer, localText.getText("TXT_KEY_CITY_NAME_AMSTERDAM",()))
		#UHV2
		sText2 += self.getNumColoniesString(3, True)
		#UHV3
		sText3 += self.RichestString()
		lHelpTexts = [sText1, sText2, sText3]
		return lHelpTexts

	def getBaseString(self, iUHV):
		pPlayer = gc.getPlayer(self.iActivePlayer)
		iGoal = pPlayer.getUHV( iUHV )
		# 3Miro: I don't understand how strings in C++ and Python work. For some reason, I managed to get C++ to return a unicode string
		#	just as it would on another alphabet. I had to "Typecast" the string to ASCII to get it to register in the text manager
		if iGoal == 1:
			sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))) + localText.getText(pPlayer.getUHVDescription(iUHV).encode('ascii', 'replace'),())
			sString += u"<font=1>" + "\n\n" + u"</font>" + u"<color=0,255,0>%s</color>" %(localText.getText("TXT_KEY_VICTORY_SCREEN_ACCOMPLISHED",()))
		elif iGoal == 0:
			sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))) + localText.getText(pPlayer.getUHVDescription(iUHV).encode('ascii', 'replace'),())
			sString += u"<font=1>" + "\n\n" + u"</font>" + u"<color=208,0,0>%s</color>" %(localText.getText("TXT_KEY_VICTORY_SCREEN_FAILED",()))
		else:
			sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))) + localText.getText(pPlayer.getUHVDescription(iUHV).encode('ascii', 'replace'),())
			sString += u"<font=1>" + "\n\n" + u"</font>" + self.getCivHelpsTexts()[iUHV]
		return sString

	def drawCleanerVictoryConditions(self):
		screen = self.getScreen()

		#Panels
		szUHV1Area = self.getNextWidgetName()
		screen.addPanel(szUHV1Area, "", "", True, True, self.X_UHV1, self.Y_UHV1, self.W_UHV1, self.H_UHV1, PanelStyles.PANEL_STYLE_MAIN)
		szUHV2Area = self.getNextWidgetName()
		screen.addPanel(szUHV2Area, "", "", True, True, self.X_UHV2, self.Y_UHV2, self.W_UHV2, self.H_UHV2, PanelStyles.PANEL_STYLE_MAIN)
		szUHV3Area = self.getNextWidgetName()
		screen.addPanel(szUHV3Area, "", "", True, True, self.X_UHV3, self.Y_UHV3, self.W_UHV3, self.H_UHV3, PanelStyles.PANEL_STYLE_MAIN)

		#Texts
		szUHV1Table = self.getNextWidgetName()
		sString = self.getBaseString(0)
		screen.addMultilineText(szUHV1Table, sString, self.X_UHV1+8, self.Y_UHV1+12, self.W_UHV1-16, self.H_UHV1-22, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		szUHV2Table = self.getNextWidgetName()
		sString = self.getBaseString(1)
		screen.addMultilineText(szUHV2Table, sString, self.X_UHV2+8, self.Y_UHV2+12, self.W_UHV2-16, self.H_UHV2-22, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		szUHV3Table = self.getNextWidgetName()
		sString = self.getBaseString(2)
		screen.addMultilineText(szUHV3Table, sString, self.X_UHV3+8, self.Y_UHV3+12, self.W_UHV3-16, self.H_UHV3-22, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def getMultiProvinceString(self, lVictories):
		iGameTurn = gc.getGame().getGameTurn()
		sString = "" 
		for iGoal in range(len(lVictories)):
			if iGoal > 0:
				sString += "\n\n"
			sString += localText.getText("TXT_KEY_UHV_PART",()) + " " + str(iGoal+1) + "\n"
			if iGameTurn > lVictories[iGoal][1]:
				sString += localText.getText("TXT_KEY_VICTORY_SCREEN_ACCOMPLISHED",())
			else:
				sString += self.getProvinceString(lVictories[iGoal][0])
		return sString

	def getProvinceString(self, tProvsToCheck, tCount = (False, 0)):
		sStringConq = localText.getText("TXT_KEY_UHV_CONQUERED",()) + ":"
		sStringMiss = localText.getText("TXT_KEY_UHV_NOT_YET",()) + ":"
		sStringConqTemp = ""
		iCount = 0
		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		for iProv in tProvsToCheck:
			sProvName = "TXT_KEY_PROVINCE_NAME_%i" %iProv
			sProvName = localText.getText(sProvName,())
			#localText.getText(pPlayer.getUHVDescription(0).encode('ascii', 'replace'),())
			iHave = pActivePlayer.getProvinceCurrentState( iProv )
			if ( iHave < con.iProvinceConquer ):
				sStringMiss += "  " + u"<color=208,0,0>%s</color>" %(sProvName)
			else:
				sStringConqTemp += "  " + u"<color=0,255,0>%s</color>" %(sProvName)
				iCount += 1
		if tCount[0]:
			sStringConq += " " + self.determineColor(iCount >= tCount[1], "("+str(iCount)+")" ) + sStringConqTemp
		else:
			sStringConq += sStringConqTemp
		sString = sStringConq + "\n" + sStringMiss
		return sString

	def getNotCivProvinceString(self, iEnemy, tProvsToCheck):
		pEnemy = gc.getPlayer(iEnemy)
		sCivShortName = str(pEnemy.getCivilizationShortDescriptionKey())
		sStringConq = localText.getText(sCivShortName,()) + " " + localText.getText("TXT_KEY_UHV_NOT_PRESENT",()) + ":"
		sStringMiss = localText.getText(sCivShortName,()) + " " + localText.getText("TXT_KEY_UHV_PRESENT",()) + ":"
		for iProv in tProvsToCheck:
			sProvName = "TXT_KEY_PROVINCE_NAME_%i" %iProv
			sProvName = localText.getText(sProvName,())
			if ( pEnemy.isAlive() and pEnemy.getProvinceCityCount( iProv ) > 0 ):
				sStringMiss += "  " + u"<color=208,0,0>%s</color>" %(sProvName)
			else:
				sStringConq += "  " + u"<color=0,255,0>%s</color>" %(sProvName)
		sString = sStringConq + "\n" + sStringMiss
		return sString

	def getWonderString(self, tWondersToCheck):
		sStringBuild = localText.getText("TXT_KEY_UHV_BUILD",()) + ":"
		sStringMiss = localText.getText("TXT_KEY_UHV_NOT_YET",()) + ":"
		for iWonder in tWondersToCheck:
			sWonderName = gc.getBuildingInfo(iWonder).getDescription()
			if gc.getPlayer(self.iActivePlayer).countNumBuildings(iWonder) > 0:
				sStringBuild += "  " + u"<color=0,255,0>%s</color>" %(sWonderName)
			else:
				sStringMiss += "  " + u"<color=208,0,0>%s</color>" %(sWonderName)
		sString = sStringBuild + "\n" + sStringMiss
		return sString

	def getProjectsString(self, tProjectsToCheck):
		sStringBuild = localText.getText("TXT_KEY_UHV_BUILD",()) + ":"
		sStringMiss = localText.getText("TXT_KEY_UHV_NOT_YET",()) + ":"
		for iProject in tProjectsToCheck:
			sProjectName = gc.getProjectInfo(iProject).getDescription()
			if gc.getTeam(self.iActivePlayer).getProjectCount(iProject) > 0:
				sStringBuild += "  " + u"<color=0,255,0>%s</color>" %(sProjectName)
			else:
				sStringMiss += "  " + u"<color=208,0,0>%s</color>" %(sProjectName)
		sString = sStringBuild + "\n" + sStringMiss
		return sString

	def getReligionProvinceString(self, tProvsToCheck, iReligion, iFunction):
		#iFuction == 1 = provinceIsSpreadReligion (Cordoba 3rd UHV)
		#iFuction == 2 = provinceIsConvertReligion (Spain 1st UHV)
		sAdjective = str(gc.getReligionInfo(iReligion).getAdjectiveKey())
		sStringSpread = localText.getText(sAdjective,()) + ":"
		sStringMiss = localText.getText("TXT_KEY_UHV_NOT_YET",()) + ":"
		pActivePlayer = gc.getPlayer(self.iActivePlayer)
		for iProv in tProvsToCheck:
			sProvName = "TXT_KEY_PROVINCE_NAME_%i" %iProv
			sProvName = localText.getText(sProvName,())
			if iFunction == 1 and pActivePlayer.provinceIsSpreadReligion( iProv, iReligion ):
				sStringSpread = sStringSpread + "  " + u"<color=0,255,0>%s</color>" %(sProvName)
			elif iFunction == 2 and pActivePlayer.provinceIsConvertReligion( iProv, iReligion ):
				sStringSpread = sStringSpread + "  " + u"<color=0,255,0>%s</color>" %(sProvName)
			else:
				sStringMiss = sStringMiss + "  " + u"<color=208,0,0>%s</color>" %(sProvName)
		sString = sStringSpread + "\n" + sStringMiss
		return sString

	def getCounterString(self, iCounter, iRequired, bInverse = False, bRound = False):
		if bRound:
			iNewCounter = "%.2f" % iCounter
		else:
			iNewCounter = iCounter
		if not bInverse:
			sString = localText.getText("TXT_KEY_UHV_CURRENTLY",()) + ": " + self.determineColor(iCounter >= iRequired, str(iNewCounter))
		else:
			sString = localText.getText("TXT_KEY_UHV_CURRENTLY",()) + ": " + self.determineColor(iCounter <= iRequired, str(iNewCounter))
		return sString

	def getNumColoniesString(self, iRequired, bTradingCompanies = False):
		iCount = vic.Victory().getNumRealColonies(self.iActivePlayer)
		sString = localText.getText("TXT_KEY_UHV_COLONIES",()) + ": " + self.determineColor(iCount >= iRequired, iCount)
		if bTradingCompanies:
			sString += "\n" + self.getProjectsString((xml.iWestIndiaCompany, xml.iEastIndiaCompany))
		return sString

	def determineColor(self, bVal, sTextGood, sTextBad = ""):
		if sTextBad == "":
			sTextBad = sTextGood
		if bVal:
			sString = u"<color=0,255,0>%s</color>" %(sTextGood)
		else:
			sString = u"<color=208,0,0>%s</color>" %(sTextBad)
		return sString

	def checkCity(self, tPlot, iCiv, cityName, bCityUHV = False, bCustomColor = False):
		x, y = tPlot
		if not gc.getMap().plot(x, y).isCity():
			return u"<color=208,0,0>%s</color>" % (cityName + " " + localText.getText("TXT_KEY_UHV_CITY_NOT_EXIST",()))
		iOwner = gc.getMap().plot(x, y).getPlotCity().getOwner()
		if not bCityUHV:
			if iOwner != iCiv:
				return u"<color=208,0,0>%s</color>" % (localText.getText("TXT_KEY_UHV_CITY_NOT_OWNED",()) + " " + cityName)
		elif not bCustomColor:
			return localText.getText("TXT_KEY_UHV_CONTROLLER_OF",()) + " " + cityName + ": " + self.determineColor(iOwner == iCiv, gc.getPlayer(iOwner).getName())
		return -1

	def checkScores(self, tCompetitors):
		iOwnRank = gc.getGame().getTeamRank(self.iActivePlayer)
		sStringLower = localText.getText("TXT_KEY_UHV_LOWER_SCORE",()) + ":"
		sStringHigher = localText.getText("TXT_KEY_UHV_HIGHER_SCORE",()) + ":"
		sStringUnkown = localText.getText("TXT_KEY_UHV_UNKNOWN_SCORE",()) + ":"
		iGameTurn = gc.getGame().getGameTurn()
		for iLoopPlayer in tCompetitors:
			pTestPlayer = gc.getPlayer(iLoopPlayer)
			sCivShortName = str(pTestPlayer.getCivilizationShortDescriptionKey())
			# unknown: if not yet born, or alive but no contact
			if iGameTurn <= con.tBirth[iLoopPlayer] or (not gc.getPlayer(self.iActivePlayer).canContact(iLoopPlayer) and pTestPlayer.isAlive()):
				sStringUnkown += "  " + u"<color=208,0,0>%s</color>" %( localText.getText(sCivShortName,()) )
			elif ( gc.getGame().getTeamRank(iLoopPlayer) < iOwnRank ):
				sStringHigher += "  " + u"<color=208,0,0>%s</color>" %( localText.getText(sCivShortName,()) )
			else:
				sStringLower += "  " + u"<color=0,255,0>%s</color>" %( localText.getText(sCivShortName,()) )
		sString = sStringLower + "\n" + sStringHigher + "\n" + sStringUnkown
		return sString

	def CollapseOrVassal(self, lEnemies):
		sStringConq = localText.getText("TXT_KEY_UHV_COLLAPSE_OR_VASSALIZE",()) + ":"
		sStringMiss = localText.getText("TXT_KEY_UHV_NOT_YET",()) + ":"
		iGameTurn = gc.getGame().getGameTurn()
		for iEnemy in lEnemies:
			teamOwn = gc.getTeam(self.iActivePlayer)
			pEnemy = gc.getPlayer(iEnemy)
			teamEnemy = gc.getTeam(iEnemy)
			sCivShortName = str(pEnemy.getCivilizationShortDescriptionKey())
			if ( pEnemy.isAlive() and not teamEnemy.isVassal( teamOwn.getID() ) ) or iGameTurn <= con.tBirth[iEnemy]:
				sStringMiss += "  " + u"<color=208,0,0>%s</color>" %( localText.getText(sCivShortName,()) )
			else:
				sStringConq += "  " + u"<color=0,255,0>%s</color>" %( localText.getText(sCivShortName,()) )
		sString = sStringConq + "\n" + sStringMiss
		return sString

	def ConquerOrVassal(self, lEnemies):
		sStringConq = localText.getText("TXT_KEY_UHV_CONQUER_OR_VASSALIZE",()) + ":"
		sStringMiss = localText.getText("TXT_KEY_UHV_NOT_YET",()) + ":"
		iGameTurn = gc.getGame().getGameTurn()
		for lEnemy in lEnemies:
			iEnemyCiv = lEnemy[0]
			iEnemyProvince = lEnemy[1]
			pActivePlayer = gc.getPlayer(self.iActivePlayer)
			teamOwn = gc.getTeam(self.iActivePlayer)
			pEnemy = gc.getPlayer(iEnemyCiv)
			teamEnemy = gc.getTeam(iEnemyCiv)
			sCivShortName = str(pEnemy.getCivilizationShortDescriptionKey())
			if iGameTurn <= con.tBirth[iEnemyCiv]:
				sStringMiss += "  " + u"<color=208,0,0>%s</color>" %( localText.getText(sCivShortName,()) )
			elif not pEnemy.isAlive() and pActivePlayer.getProvinceCurrentState(iEnemyProvince) < con.iProvinceConquer:
				sStringMiss += "  " + u"<color=208,0,0>%s</color>" %( localText.getText(sCivShortName,()) )
			elif pEnemy.isAlive() and not teamEnemy.isVassal(teamOwn.getID()) and pActivePlayer.getProvinceCurrentState(iEnemyProvince) < con.iProvinceConquer:
				sStringMiss += "  " + u"<color=208,0,0>%s</color>" %( localText.getText(sCivShortName,()) )
			else:
				sStringConq += "  " + u"<color=0,255,0>%s</color>" %( localText.getText(sCivShortName,()) )
		sString = sStringConq + "\n" + sStringMiss
		return sString

	def RichestString(self):
		pPlayer = gc.getPlayer(self.iActivePlayer)
		iPlayerGold = pPlayer.getGold()
		iGold = 0
		iRichestPlayer = -1
		for iCiv in range( con.iNumPlayers ):
			if iCiv == self.iActivePlayer: continue
			if ( gc.getPlayer( iCiv ).isAlive() ):
				if (gc.getPlayer(iCiv).getGold() > iGold):
					iGold = gc.getPlayer(iCiv).getGold()
					iRichestPlayer = iCiv
		sText = localText.getText("TXT_KEY_UHV_GOLD",())
		sUnit = "%s" %( u"<font=5>%c</font>" %(gc.getCommerceInfo( CommerceTypes.COMMERCE_GOLD).getChar()) )
		sString = self.getCompetition(iPlayerGold, iGold, iRichestPlayer, sText, sUnit)
		return sString

	def getCompetition(self, iNum, iNumEnemy, iEnemy, sText, sUnit, iNumMin = 0):
		sString = ""
		sString += sText + ": " + self.determineColor(iNum > iNumEnemy, str(iNum)) + " " + sUnit
		sString += "   " + localText.getText("TXT_KEY_UHV_BEST",()) + ": " + self.determineColor(iNum > iNumEnemy and iNum >= iNumMin, localText.getText("TXT_KEY_POPUP_YES",()), localText.getText("TXT_KEY_POPUP_NO",()))
		sString += "\n" + localText.getText("TXT_KEY_UHV_BEST_COMPETITOR",()) + ": " + self.determineColor(iNum > iNumEnemy, str(iNumEnemy))
		if iEnemy != -1:
			pEnemyPlayer = gc.getPlayer(iEnemy)
			sString += " " + sUnit + ", " + pEnemyPlayer.getName()
		return sString
		
	def getLandCompetition(self, fLand, fLandEnemy, iEnemy, sText):
		bVal = fLand > fLandEnemy
		sLand = "%.2f" % fLand
		sOtherLand = "%.2f" % fLandEnemy
		sString = ""
		sString += sText + ": " + self.determineColor(bVal, sLand) + " %"
		sString += "   " + localText.getText("TXT_KEY_UHV_BEST",()) + ": " + self.determineColor(bVal, localText.getText("TXT_KEY_POPUP_YES",()), localText.getText("TXT_KEY_POPUP_NO",()))
		sString += "\n" + localText.getText("TXT_KEY_UHV_BEST_COMPETITOR",()) + ": " + self.determineColor(bVal, sOtherLand)
		if iEnemy != -1:
			pEnemyPlayer = gc.getPlayer(iEnemy)
			sString += " %, " + pEnemyPlayer.getName()
		return sString

	def getEmptyTexts(self):
		return ("", "", "")