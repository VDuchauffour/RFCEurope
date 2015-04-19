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
		# 3Miro: UHV conditions on the Victory Conditions Screen
		self.UHV1_ID = "UHVCondition1"
		self.UHV2_ID = "UHVCondition2"
		self.UHV3_ID = "UHVCondition3"

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

		self.X_AREA = 10
		self.Y_AREA = 60
		self.W_AREA = 1010
		self.H_AREA = 270

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

                self.X_UHV1 = 10
                self.Y_UHV1 = 350
                self.W_UHV1 = 1010
                self.H_UHV1 = 120

                self.X_UHV2 = 10
                self.Y_UHV2 = 470
                self.W_UHV2 = 1010
                self.H_UHV2 = 120

                self.X_UHV3 = 10
                self.Y_UHV3 = 590
                self.W_UHV3 = 1010
                self.H_UHV3 = 120

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
					bUnknown = true
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

		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)
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

		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)
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
		screen.appendListBoxStringNoUpdate(szSettingsTable, u"     (" + CyGameTextMgr().parseLeaderTraits(activePlayer.getLeaderType(), activePlayer.getCivilizationType(), True, False) + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
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
				screen.appendListBoxStringNoUpdate(szCivsTable, u"     (" + CyGameTextMgr().parseLeaderTraits(player.getLeaderType(), player.getCivilizationType(), True, False) + ")", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.appendListBoxStringNoUpdate(szCivsTable, " ", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

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
					bUnknown = true
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
		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)
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

	def drawCleanerVictoryConditions(self):
		screen = self.getScreen()
		pPlayer = gc.getPlayer(self.iActivePlayer)

                # 3Miro: I don't undestand how strings in C++ and Python work. For some reason, I managed to get C++ to return a unicode string
                #        just as it would on another alphabet. I had to "Typecast" the string to ASCII to get it to register in the text manager

                # UHV 1
                iGoal = pPlayer.getUHV( 0 )
                if ( iGoal == -1 ):
                        sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))) + localText.getText(pPlayer.getUHVDescription(0).encode('ascii', 'replace'),())
                elif ( iGoal == 0 ):
                        sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))) + u"<color=208,0,0>%s</color>" %(localText.getText(pPlayer.getUHVDescription(0).encode('ascii', 'replace'),()))
                else:
                        #sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR)))
                        sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))) + u"<color=0,255,0>%s</color>" %(localText.getText(pPlayer.getUHVDescription(0).encode('ascii', 'replace'),()))

                szUHV1Area = self.UHV1_ID
                screen.addPanel(self.UHV1_ID, "", "", True, True, self.X_UHV1, self.Y_UHV1, self.W_UHV1, self.H_UHV1, PanelStyles.PANEL_STYLE_MAIN)

                # 3Miro: Add verbose information about the UHV Conditions:
                bDisplayCounter = False
                bCustomString = False

                if ( self.iActivePlayer == con.iFrankia ):
                        sString += self.getProvinceString(vic.tFrankControl)
                elif ( self.iActivePlayer == con.iArabia ):
                        sString += self.getProvinceString(vic.tArabiaControlI)
                elif ( self.iActivePlayer == con.iBulgaria ):
                        sString += self.getProvinceString(vic.tBulgariaControl)
                elif ( self.iActivePlayer == con.iVenecia ):
                        sString += self.getProvinceString(vic.tVenetianControl)
                elif ( self.iActivePlayer == con.iGermany ):
                        sString += self.getProvinceString(vic.tGermanyControl)
                elif ( self.iActivePlayer == con.iEngland ):
                        sString += self.getProvinceString(vic.tEnglandControl)
                elif ( self.iActivePlayer == con.iGenoa ):
                        sString += self.getProvinceString(vic.tGenoaControl)
                elif ( self.iActivePlayer == con.iAustria ):
                        sString += self.getProvinceString(vic.tAustriaControl)
                elif ( self.iActivePlayer == con.iTurkey ):
                        sString += self.getProvinceString(vic.tOttomanControlI)
                elif ( self.iActivePlayer == con.iMorocco ):
                        sString += self.getProvinceString(vic.tMoroccoControl)
                elif ( self.iActivePlayer == con.iNovgorod ):
                        sString += self.getProvinceString(vic.tNovgorodControl)
                elif ( self.iActivePlayer == con.iPrussia ):
                        sString += self.getProvinceString(vic.tPrussiaControlI)
                elif ( self.iActivePlayer == con.iAragon ):
                        sString += self.getProvinceString(vic.tAragonControlI)
                elif ( self.iActivePlayer == con.iDenmark ):
                        sString += self.getProvinceString(vic.tDenmarkControlI)
                elif ( self.iActivePlayer == con.iSweden ):
                        bDisplayCounter = True
                        iCounter = 0
                        for iProv in vic.tSwedenControl:
                                iCounter += gc.getPlayer(con.iSweden).getProvinceCityCount(iProv)
								
                if ( bDisplayCounter ):
                        sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_CURRENTLY",()) + ": %d" %(iCounter)
                if ( bCustomString ):
                        sString = sString + szCustom

		# not on the victory screen yet
		## Scotland UHV 1: count the forts and castles
		#if ( self.iActivePlayer == con.iScotland ):
		#	iCounter = pPlayer.getUHVCounter( 0 )
		#	iScotlandFort = ( iCounter / 1000 ) % 10
		#	iScotlandCastle = iCounter % 100
		#	sScotlandFort = localText.getText("TXT_KEY_IMPROVEMENT_FORT",()) + ": "
		#	sScotlandCastle = localText.getText("TXT_KEY_BUILDING_CASTLE",()) + ": "
		#	if ( iScotlandFort >= 12 ):
		#		sScotlandFort = sScotlandFort + u" <color=0,255,0>%i</color>" %(iScotlandFort)
		#	elif ( iScotlandFort > 0 ):
		#		sScotlandFort = sScotlandFort + u" <color=255,250,0>%i</color>" %(iScotlandFort)
		#	else:
		#		sScotlandFort = sScotlandFort + u" <color=208,0,0>%i</color>" %(iScotlandFort)
		#	if ( iScotlandCastle >= 3 ):
		#		sScotlandCastle = sScotlandCastle + u" <color=0,255,0>%i</color>" %(iScotlandCastle)
		#	elif ( iScotlandCastle > 0 ):
		#		sScotlandCastle = sScotlandCastle + u" <color=255,250,0>%i</color>" %(iScotlandCastle)
		#	else:
		#		sScotlandCastle = sScotlandCastle + u" <color=208,0,0>%i</color>" %(iScotlandCastle)
		#	sString = sString + "\n\n" + sScotlandFort + "   " + sScotlandCastle

		# Scotland UHV 1: count the forts and castles
		if ( self.iActivePlayer == con.iScotland ):
			iScotlandFort = gc.getPlayer(con.iScotland).getImprovementCount( xml.iImprovementFort )
			iScotlandCastle = gc.getPlayer(con.iScotland).countNumBuildings(xml.iCastle)
			sScotlandFort = localText.getText("TXT_KEY_IMPROVEMENT_FORT",()) + ": "
			sScotlandCastle = localText.getText("TXT_KEY_BUILDING_CASTLE",()) + ": "
			if ( iScotlandFort >= 10 ):
				sScotlandFort = sScotlandFort + u" <color=0,255,0>%i</color>" %(iScotlandFort)
			elif ( iScotlandFort > 0 ):
				sScotlandFort = sScotlandFort + u" <color=255,250,0>%i</color>" %(iScotlandFort)
			else:
				sScotlandFort = sScotlandFort + u" <color=208,0,0>%i</color>" %(iScotlandFort)
			if ( iScotlandCastle >= 4 ):
				sScotlandCastle = sScotlandCastle + u" <color=0,255,0>%i</color>" %(iScotlandCastle)
			elif ( iScotlandCastle > 0 ):
				sScotlandCastle = sScotlandCastle + u" <color=255,250,0>%i</color>" %(iScotlandCastle)
			else:
				sScotlandCastle = sScotlandCastle + u" <color=208,0,0>%i</color>" %(iScotlandCastle)
			sString = sString + "\n\n" + sScotlandFort + "   " + sScotlandCastle
			
		if self.iActivePlayer == con.iByzantium:
			tConstantinople = con.tCapitals[con.iByzantium]
			pConstantinople = gc.getMap().plot( tConstantinople[0], tConstantinople[1] ).getPlotCity()
			bOwn = pConstantinople.getOwner() == con.iByzantium
			if (gc.isLargestCity( tConstantinople[0], tConstantinople[1])):
				sString += "\n\n" + u" <color=0,255,0>%s%s</color>" %(pConstantinople.getName(), localText.getText("TEXT_KEY_UHV_IS_LARGEST",()) )
			else:
				sString += "\n\n" + u" <color=208,0,0>%s%s</color>" %(pConstantinople.getName(), localText.getText("TEXT_KEY_UHV_ISNT_LARGEST",())	)	
			if gc.isTopCultureCity( tConstantinople[0], tConstantinople[1] ):
				sString += "\n" + u" <color=0,255,0>%s%s</color>" %(pConstantinople.getName(), localText.getText("TEXT_KEY_UHV_IS_CULTURAL",()))
			else:
				sString += "\n" + u" <color=208,0,0>%s%s</color>" %(pConstantinople.getName(), localText.getText("TEXT_KEY_UHV_ISNT_CULTURAL",()))
			if not bOwn:
				sString += "\n" + u" <color=208,0,0>%s%s</color>" %(localText.getText("TXT_KEY_UHV_CITY_NOT_OWNED",()), pConstantinople.getName())

                screen.addMultilineText("Child" + self.UHV1_ID, sString, self.X_UHV1+6, self.Y_UHV1+14, self.W_UHV1-12, self.H_UHV1-26, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

                # UHV 2
                iGoal = pPlayer.getUHV( 1 )
                if ( iGoal == -1 ):
                        sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))) + localText.getText(pPlayer.getUHVDescription(1).encode('ascii', 'replace'),())
                elif ( iGoal == 0 ):
                        sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))) + u"<color=208,0,0>%s</color>" %(localText.getText(pPlayer.getUHVDescription(1).encode('ascii', 'replace'),()))
                else:
                        #sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR)))
                        sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))) + u"<color=0,255,0>%s</color>" %(localText.getText(pPlayer.getUHVDescription(1).encode('ascii', 'replace'),()))

                szUHV2Area = self.UHV2_ID
                screen.addPanel(self.UHV2_ID, "", "", True, True, self.X_UHV2, self.Y_UHV2, self.W_UHV2, self.H_UHV2, PanelStyles.PANEL_STYLE_MAIN)

                bDisplayCounter = False
                bCustomString = False

                if ( self.iActivePlayer == con.iByzantium ):
                        sString += self.getProvinceString(vic.tByzantumControl)
                elif ( self.iActivePlayer == con.iArabia ):
                        sString += self.getProvinceString(vic.tArabiaControlII)
                elif ( self.iActivePlayer == con.iKiev ):
                        sString += self.getProvinceString(vic.tKievControl)
                elif ( self.iActivePlayer == con.iNorway ):
                        sString += self.getProvinceString(vic.tNorwayControl)
                        bCustomString = True
                        szCustom = "\n"
                        if (gc.getPlayer(con.iNorway).getNumColonies() >= 1):
                                szCustom = szCustom + localText.getText("TXT_KEY_PROJECT_VINLAND",()) + ":  " + u"<color=0,255,0>%s</color>" %localText.getText("TXT_KEY_UHV_EXPLORED",())
                        else:
                                szCustom = szCustom + localText.getText("TXT_KEY_PROJECT_VINLAND",()) + ":  " + u"<color=208,0,0>%s</color>" %localText.getText("TXT_KEY_UHV_NOT_EXPLORED",())
                elif ( self.iActivePlayer == con.iBurgundy ):
                        sString += self.getProvinceString(vic.tBurgundyControl)
                #elif ( self.iActivePlayer == con.iNorway ):
               #         sString += self.getProvinceString(vic.tNorwayControl)
                elif ( self.iActivePlayer == con.iTurkey ):
                        sString += self.getProvinceString(vic.tOttomanControlII)
                elif ( self.iActivePlayer == con.iNovgorod ):
                        bDisplayCounter = True
                        iCounter = gc.getPlayer(con.iNovgorod).countOwnedBonuses(xml.iFur)
                elif ( self.iActivePlayer == con.iSweden ):
                        bDisplayCounter = True
                        iCounter = gc.getPlayer(con.iSweden).getUHVCounter(1)
                elif ( self.iActivePlayer == con.iDenmark ):
                        sString += self.getProvinceString(vic.tDenmarkControlIII)
		elif ( self.iActivePlayer == con.iPrussia ):
			bCustomString = True
			szCustom = "\n\n"
			iConqRaw = gc.getPlayer(con.iPrussia).getUHVCounter(1)
			for iI in range(len(vic.tPrussiaDefeat)):
				iNumConq = (iConqRaw / pow(10,iI)) % 10
				pVictim = gc.getPlayer(vic.tPrussiaDefeat[iI])
				if(iNumConq < 9):
					szNumConq = " %d" % iNumConq
				else:
					szNumConq = ">8"
				if(iNumConq < 2 and pVictim.isAlive()):
					szCustom = szCustom + "  " + u"<color=208,0,0>%s:%s</color>" %(pVictim.getCivilizationShortDescription(0), szNumConq)
				else:
					szCustom = szCustom + "  " + u"<color=0,255,0>%s:%s</color>" %(pVictim.getCivilizationShortDescription(0), szNumConq)

                if ( bDisplayCounter ):
                        sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_CURRENTLY",()) + ": %d" %(iCounter)
                if ( bCustomString ):
                        sString = sString + szCustom

                if self.iActivePlayer == con.iEngland:
                        sString += self.getNumColoniesString(self.iActivePlayer, 8)
                elif self.iActivePlayer == con.iDutch:
                        sString += self.getNumColoniesString(self.iActivePlayer, 5)

		## Aragon UHV 2: count the seaports
		#if ( self.iActivePlayer == con.iAragon ):
		#	iSeaports = gc.getPlayer(con.iAragon).getUHVCounter(1)
		#	sSeaport = localText.getText("TXT_KEY_BUILDING_ARAGON_SEAPORT",()) + ": "
		#	if ( iSeaports >= 12 ):
		#		sSeaport = sSeaport + u" <color=0,255,0>%i</color>" %(iSeaports)
		#	elif ( iSeaports > 5 ):
		#		sSeaport = sSeaport + u" <color=255,250,0>%i</color>" %(iSeaports)
		#	else:
		#		sSeaport = sSeaport + u" <color=208,0,0>%i</color>" %(iSeaports)
		#	sString = sString + "\n\n" + sSeaport

		# Aragon UHV 2: count the seaports
		if ( self.iActivePlayer == con.iAragon ):
			iSeaport = PyPlayer(iAragon).countNumBuildings(xml.iAragonSeaport)
			sSeaport = localText.getText("TXT_KEY_BUILDING_ARAGON_SEAPORT",()) + ": "
			if ( iSeaport >= 12 ):
				sSeaport = sSeaport + u" <color=0,255,0>%i</color>" %(iSeaport)
			elif ( iSeaport > 5 ):
				sSeaport = sSeaport + u" <color=255,250,0>%i</color>" %(iSeaport)
			else:
				sSeaport = sSeaport + u" <color=208,0,0>%i</color>" %(iSeaport)
			sString = sString + "\n\n" + sSeaport

                if (self.iActivePlayer == con.iFrankia):
                        pJPlot = gc.getMap().plot( con.iJerusalem[0], con.iJerusalem[1] )
                        if ( pJPlot.isCity()):
                                iOwner = pJPlot.getPlotCity().getOwner()
                                pOwner = gc.getPlayer(iOwner)
                                if iOwner == con.iFrankia:
                                        sString += "\n\n" + localText.getText("TXT_KEY_UHV_FRA2_HELP",()) + u" <color=0,255,0>%s</color>" % ( pOwner.getName() )
                                else:
                                        sString += "\n\n" + localText.getText("TXT_KEY_UHV_FRA2_HELP",()) + u" <color=208,0,0>%s</color>" % ( pOwner.getName() )
                        else:
                                sString += "\n\n" + u" <color=208,0,0>%s</color>" % ( localText.getText("TXT_KEY_UHV_CITY_NOT_EXIT",(localText.getText("TXT_KEY_UHV_JERUSALEM"),()) ))

                # The Polish UHV 2: count the cities
                if ( self.iActivePlayer == con.iPoland ):
                        pPoland = gc.getPlayer( con.iPoland )
                        tProvsToCheck = vic.tPolishControl
                        iNumCities = 0
                        for iProv in tProvsToCheck:
                                iNumCities += pPoland.getProvinceCityCount( iProv )

                        if ( iNumCities < 10 ):
                                sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_CITIES_CONTROLLED",()) + u" <color=208,0,0>%i</color>" %(iNumCities)
                        elif ( iNumCities < 12 ):
                                sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_CITIES_CONTROLLED",()) + u" <color=255,250,0>%i</color>" %(iNumCities)
                        else:
                                sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_CITIES_CONTROLLED",()) + u" <color=0,255,0>%i</color>" %(iNumCities)

                screen.addMultilineText("Child" + self.UHV2_ID, sString, self.X_UHV2+6, self.Y_UHV2+14, self.W_UHV2-12, self.H_UHV2-26, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				
		if ( self.iActivePlayer == con.iMorocco ):
			victory = gc.getVictoryInfo(4) #Cultural victory
			ourBestCities = self.getListCultureCities(self.iActivePlayer)[0:victory.getNumCultureCities()]
			sString = sString + "\n\n" + localText.getText("TXT_KEY_MOR_HELP", ())
			for i in range(3):
				if (len(ourBestCities) > i):
					if ourBestCities[i][0] < 5000:
						sString += "\n" + ourBestCities[i][1].getName() + ": " + u"<color=208,0,0>%i</color>" %(ourBestCities[i][0])
					else:
						sString += "\n" + ourBestCities[i][1].getName() + ": " + u"<color=0,255,0>%i</color>" %(ourBestCities[i][0])
			screen.addMultilineText("Child" + self.UHV2_ID, sString, self.X_UHV2+6, self.Y_UHV2+14, self.W_UHV2-12, self.H_UHV2-26, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			

                # UHV 3
                iGoal = pPlayer.getUHV( 2 )
                if ( iGoal == -1 ):
                        sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))) + localText.getText(pPlayer.getUHVDescription(2).encode('ascii', 'replace'),())
                elif ( iGoal == 0 ):
                        sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))) + u"<color=208,0,0>%s</color>" %(localText.getText(pPlayer.getUHVDescription(2).encode('ascii', 'replace'),()))
                else:
                        #sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR)))
                        sString = (u"<font=5>%c</font>" %(CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))) + u"<color=0,255,0>%s</color>" %(localText.getText(pPlayer.getUHVDescription(2).encode('ascii', 'replace'),()))

                szUHV3Area = self.UHV3_ID
                screen.addPanel(self.UHV3_ID, "", "", True, True, self.X_UHV3, self.Y_UHV3, self.W_UHV3, self.H_UHV3, PanelStyles.PANEL_STYLE_MAIN)

                bDisplayCounter = False
                bCustomString = False

                if ( self.iActivePlayer == con.iGermany ):
                        sString += self.getProvinceString(vic.tGermanyControlII)
                elif ( self.iActivePlayer == con.iTurkey ):
                        sString += self.getProvinceString(vic.tOttomanControlIII)
                elif ( self.iActivePlayer == con.iScotland ):
                        sString += self.getProvinceString(vic.tScotlandControl)
                elif ( self.iActivePlayer == con.iAragon ):
                        sString += self.getProvinceString(vic.tAragonControlII)
                elif (self.iActivePlayer == con.iPrussia):
                        bDisplayCounter = True
                        pCapital = gc.getPlayer(con.iPrussia).getCapitalCity()
                        iGPStart = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_PRIEST")
                        iGPEnd = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), "SPECIALIST_GREAT_SPY")
                        iCounter = 0
                        for iType in range(iGPStart, iGPEnd+1):
                                iCounter += pCapital.getFreeSpecialistCount(iType)
                elif (self.iActivePlayer == con.iSweden):
                        bDisplayCounter = True
                        iCounter = up.getNumForeignCitiesOnBaltic(con.iSweden, True)
                        bCustomString = True
                        szCustom = " " + localText.getText("TXT_KEY_UHV_BALTIC_CITIES",())

                if ( bDisplayCounter ):
                        sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_CURRENTLY",()) + ": %d" %(iCounter)
                if ( bCustomString ):
                        sString = sString + szCustom
						
                if self.iActivePlayer == con.iFrankia:
                        sString += self.getNumColoniesString(self.iActivePlayer, 6)
                elif self.iActivePlayer == con.iDenmark:
                        sString += self.getNumColoniesString(self.iActivePlayer, 5)
                elif self.iActivePlayer == con.iPortugal:
                        sString += self.getNumColoniesString(self.iActivePlayer, 6)

                # Polish UHV 3: count cathedrals and quarters
                if ( self.iActivePlayer == con.iPoland ):
                        iCounter = pPlayer.getUHVCounter( 2 )
                        iCathCath = ( iCounter / 10000 ) % 10
                        iOrthCath = ( iCounter / 1000 ) % 10
                        iProtCath = ( iCounter / 100 ) % 10
                        iJewishQu = iCounter % 100
                        sCathCath = localText.getText("TXT_KEY_BUILDING_CATHOLIC_CATHEDRAL",()) + ": "
                        sOrthCath = localText.getText("TXT_KEY_BUILDING_ORTHODOX_CATHEDRAL",()) + ": "
                        sProtCath = localText.getText("TXT_KEY_BUILDING_PROTESTANT_CATHEDRAL",()) + ": "
                        sJewishQu = localText.getText("TXT_KEY_BUILDING_JEWISH_QUARTER",()) + ": "
                        if ( iCathCath >= 3 ):
                                sCathCath = sCathCath + u" <color=0,255,0>%i</color>" %(iCathCath)
                        elif ( iCathCath > 0 ):
                                sCathCath = sCathCath + u" <color=255,250,0>%i</color>" %(iCathCath)
                        else:
                                sCathCath = sCathCath + u" <color=208,0,0>%i</color>" %(iCathCath)
                        if ( iOrthCath >= 3 ):
                                sOrthCath = sOrthCath + u" <color=0,255,0>%i</color>" %(iOrthCath)
                        elif ( iOrthCath > 0 ):
                                sOrthCath = sOrthCath + u" <color=255,250,0>%i</color>" %(iOrthCath)
                        else:
                                sOrthCath = sOrthCath + u" <color=208,0,0>%i</color>" %(iOrthCath)
                        if ( iProtCath >= 2 ):
                                sProtCath = sProtCath + u" <color=0,255,0>%i</color>" %(iProtCath)
                        elif ( iProtCath > 0 ):
                                sProtCath = sProtCath + u" <color=255,250,0>%i</color>" %(iProtCath)
                        else:
                                sProtCath = sProtCath + u" <color=208,0,0>%i</color>" %(iProtCath)
                        if ( iJewishQu == 99 ):
                                sKazimierzWonder = localText.getText("TXT_KEY_BUILDING_KAZIMIERZ",())
                                sJewishQu = sJewishQu + u" <color=0,255,0>%s</color>" %(sKazimierzWonder)
                        elif ( iJewishQu >= 2 ):
                                sJewishQu = sJewishQu + u" <color=0,255,0>%i</color>" %(iJewishQu)
                        elif ( iJewishQu > 0 ):
                                sJewishQu = sJewishQu + u" <color=255,250,0>%i</color>" %(iJewishQu)
                        else:
                                sJewishQu = sJewishQu + u" <color=208,0,0>%i</color>" %(iJewishQu)
                        sString = sString + "\n\n" + sCathCath + "   " + sOrthCath + "   " + sProtCath + "   " + sJewishQu

                ### Add New Spanish UHV
                if ( self.iActivePlayer == con.iSpain ):
                        lLand = [ 0, 0, 0, 0, 0, 0 ] # Prot, Islam, Cath, Orth, Jew, Pagan
                        lPop  = [ 0, 0, 0, 0, 0, 0 ]
                        for iPlayer in range( con.iNumPlayers ):
                                pPlayer = gc.getPlayer( iPlayer )
                                iStateReligion = pPlayer.getStateReligion()
                                if ( iStateReligion > -1 ):
                                        lLand[ iStateReligion ] += pPlayer.getTotalLand()
                                        lPop[ iStateReligion ] += pPlayer.getTotalPopulation()
                                else:
                                        lLand[ 5 ] += pPlayer.getTotalLand()
                                        lPop[ 5 ] += pPlayer.getTotalPopulation()

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
                        if ( iBestLand == xml.iCatholicism ):
                                sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_MOST_LAND",()) + u" <color=0,255,0>%s</color>" %(sBestR)
                        else:
                                sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_MOST_LAND",()) + u" <color=208,0,0>%s</color>" %(sBestR)

                        if ( iBestPop == 5 ):
                                sBestR = localText.getText("TXT_KEY_UHV_PAGAN",())
                        else:
                                sBestR = localText.getText( gc.getReligionInfo(iBestPop).getAdjectiveKey().encode('ascii', 'replace'), () )
                        if ( iBestPop == xml.iCatholicism ):
                                sString = sString + "\n" + localText.getText("TXT_KEY_UHV_MOST_POPULATION",()) + u" <color=0,255,0>%s</color>" %(sBestR)
                        else:
                                sString = sString + "\n" + localText.getText("TXT_KEY_UHV_MOST_POPULATION",()) + u" <color=208,0,0>%s</color>" %(sBestR)

                ### Add New Genoa UHV
                if ( self.iActivePlayer == con.iGenoa ):
                        iMostTrade = 0
                        iBiggestTrader = -1
                        for iPlayer in range( con.iNumPlayers ):
                                pPlayer = gc.getPlayer( iPlayer )
                                iTrade = pPlayer.calculateTotalImports(YieldTypes.YIELD_COMMERCE) + pPlayer.calculateTotalExports(YieldTypes.YIELD_COMMERCE)
                                if ( iTrade > iMostTrade ):
                                       iMostTrade = iTrade
                                       iBiggestTrader = iPlayer

                        pBestTrader = gc.getPlayer( iBiggestTrader )
                        if ( iBiggestTrader == con.iGenoa ):
                                sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_BIGGEST_TRADER",()) + u" <color=0,255,0>%s</color>" %(pBestTrader.getName())
                        else:
                                sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_BIGGEST_TRADER",()) + u" <color=208,0,0>%s</color>" %(pBestTrader.getName())

                ### Add Dutch and Byzantium UHV
                if ( self.iActivePlayer == con.iDutch or self.iActivePlayer == con.iByzantium ):
                        iGold = 0
                        iPlayer = -1
                        for iCiv in range( con.iNumPlayers ):
                                if ( gc.getPlayer( iCiv ).isAlive() ):
                                        if (gc.getPlayer(iCiv).getGold() > iGold):
                                                iGold = gc.getPlayer(iCiv).getGold()
                                                iPlayer = iCiv
                        pPlayer = gc.getPlayer( iPlayer )
                        if ( iPlayer == self.iActivePlayer ):
                                sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_RICHEST_NATION",()) + u" <color=0,255,0>%s</color>" %(pPlayer.getName())
                        else:
                                sString = sString + "\n\n" + localText.getText("TXT_KEY_UHV_RICHEST_NATION",()) + u" <color=208,0,0>%s</color>" %(pPlayer.getName()) + " (%d)" %pPlayer.getGold()
								
                if (self.iActivePlayer == con.iArabia):
                        iPerc = gc.getGame().calculateReligionPercent( xml.iIslam )
                        sString += "\n\n" + localText.getText("TXT_KEY_UHV_ISLAM",()) + ": " + self.determineColor(iPerc > 35, str(iPerc)) + " %"
                        #if iPerc >= 35:
                        #        sString += "\n\n" + localText.getText("TXT_KEY_UHV_ISLAM",()) + ": " + u" <color=0,255,0>%i</color>" %(iPerc) + " %"
                        #else:
                        #        sString += "\n\n" + localText.getText("TXT_KEY_UHV_ISLAM",()) + ": " + u" <color=208,0,0>%i</color>" %(iPerc) + " %"
			
			
                screen.addMultilineText("Child" + self.UHV3_ID, sString, self.X_UHV3+6, self.Y_UHV3+14, self.W_UHV3-12, self.H_UHV3-26, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
 
					
				
	def getProvinceString(self, tProvsToCheck):
		sStringConq = localText.getText("TXT_KEY_UHV_CONQUERED",()) + ":"
		sStringMiss = localText.getText("TXT_KEY_UHV_NOT_YET",()) + ":"
		for iProv in tProvsToCheck:
			sProvName = "TXT_KEY_PROVINCE_NAME_%i" %iProv
			sProvName = localText.getText(sProvName,())
			#localText.getText(pPlayer.getUHVDescription(0).encode('ascii', 'replace'),())
			pPlayer = gc.getPlayer(self.iActivePlayer)
			iHave = pPlayer.getProvinceCurrentState( iProv )
			if ( iHave < con.iProvinceConquer ):
				sStringMiss = sStringMiss + "  " + u"<color=208,0,0>%s</color>" %(sProvName)
			else:
				sStringConq = sStringConq + "  " + u"<color=0,255,0>%s</color>" %(sProvName)
		sString = "\n\n" + sStringConq + "\n" + sStringMiss
		return sString
		
	def getNumColoniesString(self, iPlayer, iRequired):
		iCount = vic.getNumRealColonies(iPlayer)
		if iCount < iRequired:
			sString = "\n\n" + localText.getText("TXT_KEY_UHV_COLONIES",()) + ": " + u"<color=208,0,0>%i</color>" %(iCount)
		else:
			sString = "\n\n" + localText.getText("TXT_KEY_UHV_COLONIES",()) + ": " + u"<color=0,255,0>%i</color>" %(iCount)
		return sString

	def determineColor(self, bVal, sText):
		if bVal:
			sString = u"<color=0,255,0>%s</color>" %(sText)
		else:
			sString = u"<color=208,0,0>%s</color>" %(sText)
		return sString
