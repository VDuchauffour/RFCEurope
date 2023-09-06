## RFCEMapUtils
## contains classes for reading, editing, visualizing and saving SettlerMaps, WarMaps, CityNameMaps, Provinces, CoreAreas and NormalAreas from RFCE
##
## Author: Caliom

from CvPythonExtensions import *
import CvMainInterface
import CvScreenEnums
import RFCEMaps
import RFCUtils
import Consts as con


gc = CyGlobalContext()
utils = RFCUtils.RFCUtils()
map = CyMap()
localText = CyTranslator()
engine = CyEngine()

# Somehow sometimes map.getGridHeight() doesn't work. I think it has something to do when python scripts are reloaded. For the time being I hardcode the map size
#iMapMaxY = map.getGridHeight()
#iMapMaxX = map.getGridWidth()
#iNumPlots = map.numPlots()
iMapMaxX = con.iMapMaxX
iMapMaxY = con.iMapMaxY
iNumPlots = iMapMaxX * iMapMaxY

# Reserved AreaBorderLayers: 100 - 260(100 to iAreaBorderLayerProvinceOffset+iNumProvinces)
iNumProvinces = 150
iAreaBorderLayerProvinceOffset = 110
iAreaBorderLayerCoreArea = 108
iAreaBorderLayerNormalArea = 109

# The default filename that the maps are exported to.
tDefaultExportFileName = "./Mods/RFCEurope/Reference/ModdingTools/RFCEMaps.py"

# The values in the shades array are:
# - The value as in the corresponding map. it is important that the values are orderd, highest value first.
# - The color that this value is rendered in
# - a key that is used for the AreaBorderPlots, (like AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS). This key must be unique within one array and should not conflict with other AreaBorderLayer Constants. -1 means that it is not rendered
settlerMapShades = ((700, "COLOR_YELLOW", 100,"highest [700]"),(500, "COLOR_PLAYER_RED", 101, "high [500]"),(400, "COLOR_PLAYER_DARK_RED", 102, "medium [400]"),(300, "COLOR_PLAYER_ORANGE", 103,"low [300]"),(200, "COLOR_PLAYER_PEACH", 104,"lowest [200]"),(20, "COLOR_BLACK", -1, "doesn't settle [20]"),(-1, "COLOR_WHITE", 105, "never [-1]"))
warMapShades = ((16, "COLOR_PLAYER_DARK_RED", 100 , "16"),(10, "COLOR_PLAYER_RED", 101 , "10"),(6, "COLOR_PLAYER_ORANGE", 102 , "6"),(2, "COLOR_PLAYER_LIGHT_ORANGE", 103 , "2"),(0, "COLOR_BLACK", -1 , "0"))

#provinceColors = ("COLOR_YELLOW","COLOR_RED","COLOR_BLUE","COLOR_BLACK","COLOR_GREEN","COLOR_PLAYER_ORANGE","COLOR_PLAYER_BROWN", "COLOR_MAGENTA")
provinceColors = ("COLOR_YELLOW","COLOR_RED","COLOR_BLUE","COLOR_GREEN","COLOR_PLAYER_ORANGE","COLOR_MAGENTA","COLOR_CYAN")
sHighlightColor = "COLOR_CYAN"
defaultProvinceColor = "COLOR_BLACK"

#Default Values
settlerMapDefault = 20
warMapDefault = 0
cityNameMapDefault = "-1"
provinceMapDefault = -1

def showMessage(tMessage):
	CyInterface().addImmediateMessage(tMessage, "")

class RFCEMapManager:

	def __init__(self):
		self.mapsInitiated = False

	def initMaps(self):
		if(not self.mapsInitiated):
			showMessage("initializing RFCEMaps")
			self.provinceMap = self.convertProvinceMap(RFCEMaps.tProvinceMap)
			self.settlerMap = self.convertMap(RFCEMaps.tSettlersMaps)
			self.warMap = self.convertMap(RFCEMaps.tWarsMaps)
			self.cityNameMap = self.convertMap(RFCEMaps.tCityMap)
			self.coreAreasBL = self.convertArray(con.tCoreAreasTL)
			self.coreAreasTR = self.convertArray(con.tCoreAreasBR)
			self.coreAreasAdditionalPlots = con.lExtraPlots
			self.normalAreasBL = self.convertArray(con.tNormalAreasTL)
			self.normalAreasTR = self.convertArray(con.tNormalAreasBR)
			self.normalAreasSubtractedPlots = self.convertNestedArray(con.tNormalAreasSubtract)

			self.mapsInitiated = True

	def convertMap(self, aMap):
		length = len(aMap)
		aList = [None]*length
		for i in range(length):
			aList[i] = [None]*iMapMaxY
			for j in range(iMapMaxY):
				aList[i][j] = list(aMap[i][j])
		return aList

	def convertProvinceMap(self, aMap):
		aList = [None]*iMapMaxY
		for i in range(iMapMaxY):
			aList[i] = list(aMap[i])
		return aList

	def convertArray(self, aTuple):
		length = len(aTuple)
		aList = [None] * length
		for i in range(length):
			aList[i] = aTuple[i]
		return aList

	def convertNestedArray(self, aTuple):
		length = len(aTuple)
		aList = [None] * length
		for i in range(length):
			nestedLength = len(aTuple[i])
			aList[i] = [None] * nestedLength
			for j in range(nestedLength):
				aList[i][j] = aTuple[i][j]
		return aList

	def getSettlerMapShades(self):
		return settlerMapShades

	def getWarMapShades(self):
		return warMapShades

	# settler map
	def getSettlerValue( self, iPlayer, pPlot):
		return self.getValue(iPlayer, pPlot, self.settlerMap)

	def setSettlerValue( self, iPlayer, pPlot, iValue ):
		self.setValue(iPlayer, pPlot, self.settlerMap, iValue)

	def increaseSettlerValue(self, iPlayer, pPlot):
		self.changeValue(iPlayer, pPlot, self.settlerMap, settlerMapShades, 1)

	def decreaseSettlerValue(self, iPlayer, pPlot):
		self.changeValue(iPlayer, pPlot, self.settlerMap, settlerMapShades, -1)

	# war map
	def getWarValue( self, iPlayer, pPlot):
		return self.getValue(iPlayer, pPlot, self.warMap)

	def setWarValue( self, iPlayer, pPlot, iValue ):
		self.setValue(iPlayer, pPlot, self.warMap, iValue)

	def increaseWarValue(self, iPlayer, pPlot):
		self.changeValue(iPlayer, pPlot, self.warMap, warMapShades, 1)

	def decreaseWarValue(self, iPlayer, pPlot):
		self.changeValue(iPlayer, pPlot, self.warMap, warMapShades, -1)

	# city names
	def getCityName( self, iPlayer, pPlot):
		name = self.getValue(iPlayer, pPlot, self.cityNameMap)
		if(name != cityNameMapDefault):
			return name
		return None

	def setCityName( self, iPlayer, pPlot, sName ):
		if(sName == None or sName == ""):
			sName = cityNameMapDefault
		self.setStringValue(iPlayer, pPlot, self.cityNameMap, sName)

	def removeCityName( self, iPlayer, pPlot):
		self.setCityName(iPlayer, pPlot, cityNameMapDefault)

	# provinces
	def getProvinceName( self, iProvinceIdOrPlot):
		if(isinstance(iProvinceIdOrPlot, CyPlot)):
			iProvince = self.getProvinceId(iProvinceIdOrPlot)
		else:
			iProvince = iProvinceIdOrPlot
		if(iProvince != provinceMapDefault):
			return unicode(localText.getText( ("TXT_KEY_PROVINCE_NAME_%i" %iProvince),()))
		return ""

	def getProvinceId( self, pPlot):
		return self.provinceMap[pPlot.getY()][pPlot.getX()]

	def setProvinceId( self, pPlot, iProvince ):
		self.provinceMap[pPlot.getY()][pPlot.getX()] = int(iProvince)

	def removeProvince( self, pPlot):
		self.setProvinceId(pPlot, provinceMapDefault)

	def isValidProvinceId(self, iProvince):
		return (iProvince >= 0 and iProvince < iNumProvinces)

	# core area
	def setCoreAreaBLTR(self, iPlayer, BL, TR):
		self.coreAreasBL[iPlayer] = BL
		self.coreAreasTR[iPlayer] = TR

		overlappingPlots = []
		for xy in self.coreAreasAdditionalPlots[iPlayer]:
			if(self.isInRectangle(xy, self.coreAreasBL[iPlayer],self.coreAreasTR[iPlayer])):
				overlappingPlots.append(xy)

		for xy in overlappingPlots:
			self.removeCoreAreaAdditionalPlot(iPlayer,xy)

	def getCoreAreaBL(self, iPlayer):
		return self.coreAreasBL[iPlayer]

	def getCoreAreaTR(self, iPlayer):
		return self.coreAreasTR[iPlayer]

	def addCoreAreaAdditionalPlot(self, iPlayer, xy):
		if(self.isInRectangle(xy, self.coreAreasBL[iPlayer],self.coreAreasTR[iPlayer])):
			return
		self.coreAreasAdditionalPlots[iPlayer].append(xy)

	def removeCoreAreaAdditionalPlot(self, iPlayer, xy):
		try:
			self.coreAreasAdditionalPlots[iPlayer].remove(xy)
		except ValueError:
			pass

	def getCoreAreaAdditionalPlots(self, iPlayer):
		return self.coreAreasAdditionalPlots[iPlayer]

	#normal area
	def setNormalAreaBLTR(self, iPlayer, BL, TR):
		self.normalAreasBL[iPlayer] = BL
		self.normalAreasTR[iPlayer] = TR

		outsidePlots = []
		for xy in self.normalAreasSubtractedPlots[iPlayer]:
			if(not self.isInRectangle(xy, self.normalAreasBL[iPlayer],self.normalAreasTR[iPlayer])):
				outsidePlots.append(xy)

		for xy in outsidePlots:
			self.removeNormalAreaSubtractedPlot(iPlayer,xy)

	def getNormalAreaBL(self, iPlayer):
		return self.normalAreasBL[iPlayer]

	def getNormalAreaTR(self, iPlayer):
		return self.normalAreasTR[iPlayer]

	def addNormalAreaSubtractedPlot(self, iPlayer, xy):
		if(not self.isInRectangle(xy, self.normalAreasBL[iPlayer],self.normalAreasTR[iPlayer])):
			return
		self.normalAreasSubtractedPlots[iPlayer].append(xy)

	def removeNormalAreaSubtractedPlot(self, iPlayer, xy):
		try:
			self.normalAreasSubtractedPlots[iPlayer].remove(xy)
		except ValueError:
			pass

	def getNormalAreaSubtractedPlots(self, iPlayer):
		return self.normalAreasSubtractedPlots[iPlayer]


	def isInRectangle(self, xy, BL, TR):
		if(xy[0] < BL[0] or xy[0] > TR[0] or xy[1] < BL[1] or xy[1] > TR[1]):
			return False
		return True

	def getValue( self, iPlayer, pPlot, aMap):
		return aMap[iPlayer][self.swapY(pPlot.getY())][pPlot.getX()]

	def setValue( self, iPlayer, pPlot, aMap, iValue):
		aMap[iPlayer][self.swapY(pPlot.getY())][pPlot.getX()] = iValue

	def setStringValue( self, iPlayer, pPlot, aMap, sValue):
		aMap[iPlayer][self.swapY(pPlot.getY())][pPlot.getX()] = ("%s" %sValue)

	def changeValue(self, iPlayer, pPlot, aMap, aShades, iChange):
		iValue =	self.getValue(iPlayer, pPlot, aMap)
		iNewValue = self.findNewValue(aShades, iValue, iChange)
		self.setValue(iPlayer, pPlot, aMap, iNewValue)

	def findNewValue(self, aShades, iValue, iChange):
		length = len(aShades)
		for i in range(length):
			if (iValue >= aShades[i][0]):
				j = i-iChange
				if(j>=length):
					j=length-1
				elif(j<0):
					j=0
				return aShades[j][0]
		return 0

	def swapY( self, iY):
		return iMapMaxY - iY - 1


class RFCEMapVisualizer:

	def __init__(self, mapManager):
		self.iPlayer = 0
		self.iHighlightedProvince = -1
		self.mapManager = mapManager

	def setPlayer(self, iPlayer):
		self.iPlayer = iPlayer


	def getProvinceColor(self, iProvince):
		if(iProvince == provinceMapDefault):
			return defaultProvinceColor
		else:
			return provinceColors[iProvince % len(provinceColors)]

	def getSettlerMapColor(self, iValue):
		shade = self.getSettlerMapShade(iValue)
		return shade[1]

	def getWarMapColor(self, iValue):
		shade = self.getWarMapShade(iValue)
		return shade[1]


	def getSettlerMapShade(self, iValue):
		for shade in settlerMapShades:
			if(iValue >= shade[0]):
				return shade
		return settlerMapShades[len(settlerMapShades)-1] #fallback

	def getWarMapShade(self, iValue):
		for shade in warMapShades:
			if(iValue >= shade[0]):
				return shade
		return warMapShades[len(warMapShades)-1] #fallback


	def showSettlerMap(self):
		self.resetMinimap(True)
		for i in range (iMapMaxX):
			for j in range (iMapMaxY):
				pPlot = map.plot(i,j)
				if (not pPlot.isNone()):
					iValue = self.mapManager.getSettlerValue(self.iPlayer, pPlot)
					for shade in settlerMapShades:
						if(iValue >= shade[0]):
							if(shade[2] > 0):
								self.showOnMinimap(pPlot, shade[1])
								CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), shade[2], shade[1], 1.0)
							break

	def hideSettlerMap(self):
		self.resetMinimap()
		for shade in settlerMapShades:
			if(shade[2] > 0):
				CyEngine().clearAreaBorderPlots(shade[2])


	def showWarMap(self):
		self.resetMinimap(True)
		for i in range (iMapMaxX):
			for j in range (iMapMaxY):
				pPlot = map.plot(i,j)
				if (not pPlot.isNone()):
					iValue = self.mapManager.getWarValue(self.iPlayer, pPlot)
					for shade in warMapShades:
						if(iValue >= shade[0]):
							if(shade[2] > 0):
								CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), shade[2], shade[1], 1.0)
								self.showOnMinimap(pPlot, shade[1])
							break

	def hideWarMap(self):
		self.resetMinimap()
		for shade in warMapShades:
			if(shade[2] > 0):
				CyEngine().clearAreaBorderPlots(shade[2])


	def showCityNames(self):
		for i in range (iMapMaxX):
			for j in range (iMapMaxY):
				pPlot = map.plot(i,j)
				self.showCityName(pPlot)

	def showCityName(self, pPlot):
		if (not pPlot.isNone()):
			name = self.mapManager.getCityName(self.iPlayer, pPlot)
			if (name != None):
				CyEngine().addLandmark(pPlot, name)
				#CyEngine().addSign(pPlot, utils.getHumanID(), name)

	def hideCityNames(self):
		self.removeLandMarks()

	def hideCityName(self, pPlot):
		if (not pPlot.isNone()):
			CyEngine().removeLandmark(pPlot)
			#CyEngine().removeSign(pPlot, utils.getHumanID())


	def showCoreArea(self):
		self.resetMinimap(True)
		BL = self.mapManager.getCoreAreaBL(self.iPlayer)
		TR = self.mapManager.getCoreAreaTR(self.iPlayer)
		plotX = BL[0]
		plotY = TR[1]
		for iX in range(TR[0]-BL[0]+1):
			for iY in range(TR[1]-BL[1]+1):
				pPlot = map.plot(plotX+iX, plotY-iY)
				if (not pPlot.isNone()):
					CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), iAreaBorderLayerCoreArea, "COLOR_WHITE", 1.0)
					self.showOnMinimap(pPlot, "COLOR_WHITE")

		for xy in self.mapManager.getCoreAreaAdditionalPlots(self.iPlayer):
			pPlot = map.plot(xy[0], xy[1])
			if (not pPlot.isNone()):
				CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), iAreaBorderLayerCoreArea, "COLOR_GREY", 1.0)
				self.showOnMinimap(pPlot, "COLOR_WHITE")

	def hideCoreArea(self):
		CyEngine().clearAreaBorderPlots(iAreaBorderLayerCoreArea)
		self.resetMinimap()


	def showNormalArea(self):
		self.resetMinimap(True)
		exceptions = self.mapManager.getNormalAreaSubtractedPlots(self.iPlayer)
		BL = self.mapManager.getNormalAreaBL(self.iPlayer)
		TR = self.mapManager.getNormalAreaTR(self.iPlayer)
		plotX = BL[0]
		plotY = TR[1]
		for iX in range(TR[0]-BL[0]+1):
			for iY in range(TR[1]-BL[1]+1):
				if not (plotX+iX, plotY-iY) in exceptions:
					pPlot = map.plot(plotX+iX, plotY-iY)
					if (not pPlot.isNone()):
						CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), iAreaBorderLayerCoreArea, "COLOR_WHITE", 1.0)
						self.showOnMinimap(pPlot, "COLOR_WHITE")

	def hideNormalArea(self):
		CyEngine().clearAreaBorderPlots(iAreaBorderLayerNormalArea)
		self.resetMinimap()


	def showProvinces(self):
		self.resetMinimap(True)
		iNumColors = len(provinceColors)
		for i in range(iNumPlots):
			pPlot = map.plotByIndex(i)
			if (not pPlot.isNone()):
				iProvince = self.mapManager.getProvinceId(pPlot)
				if (iProvince != provinceMapDefault):
					sColor = provinceColors[iProvince%iNumColors]
					CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), iAreaBorderLayerProvinceOffset + iProvince, sColor, 1.0)
					self.showOnMinimap(pPlot, sColor)
		self.iHighlightedProvince = -1

	def hideProvinces(self):
		self.resetMinimap()
		for i in range(iNumProvinces):
			self.hideProvince(i)

	def highlightProvince(self, iProvince):
		self.resetMinimap(True)
		if(not self.mapManager.isValidProvinceId(iProvince)):
			return
		sColor = self.getProvinceColor(iProvince)
		for i in range(iNumPlots):
			pPlot = map.plotByIndex(i)
			if (not pPlot.isNone()):
				if (self.mapManager.getProvinceId(pPlot) == iProvince):
					self.showOnMinimap(pPlot, sColor)


	#experimental functions
	# def updateProvince(self, iProvince):
		# self.colorProvince(iProvince, self.getProvinceColor(iProvince), 1.0)

	# def highlightProvince(self, iProvince):
		# showMessage( "%d - %d" %(self.iHighlightedProvince, iProvince))
		# if(not self.mapManager.isValidProvinceId(iProvince) or self.iHighlightedProvince == iProvince):
			# return
		# self.colorProvince(self.iHighlightedProvince, self.getProvinceColor(self.iHighlightedProvince), 1.0)
		# self.iHighlightedProvince = iProvince
		# self.colorProvince(iProvince, self.getProvinceColor(iProvince), 2.0)

	# def colorProvince(self, iProvince, sColor, fAlpha):
		# if(not self.mapManager.isValidProvinceId(iProvince)):
			# return
		# self.hideProvince(iProvince)
		# for i in range(iNumPlots):
			# pPlot = map.plotByIndex(i)
			# if (not pPlot.isNone()):
				# iLoopProvince = self.mapManager.getProvinceId(pPlot)
				# if (iLoopProvince == iProvince):
					# CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), iAreaBorderLayerProvinceOffset + iProvince, sColor, fAlpha)


	def hideProvince(self, iProvince):
		if(not self.mapManager.isValidProvinceId(iProvince)):
			return
		CyEngine().clearAreaBorderPlots(iAreaBorderLayerProvinceOffset + iProvince)

	def hideAll(self):
		self.hideCityNames()
		self.hideSettlerMap()
		self.hideWarMap()
		self.hideProvinces()
		self.hideCoreArea()
		self.hideNormalArea()

	def removeLandMarks(self):
		for i in range (iMapMaxX):
			for j in range (iMapMaxY):
				pPlot = map.plot(i,j)
				if (not pPlot.isNone()):
					CyEngine().removeLandmark(pPlot)
					#CyEngine().removeSign(pPlot, utils.getHumanID())

	def showOnMinimap(self, pPlot, sColor):
		mainScreen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		mainScreen.minimapFlashPlot (pPlot.getX(), pPlot.getY(), gc.getInfoTypeForString(sColor), 0.3) #time
		mainScreen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_TERRITORY, pPlot.getX(), pPlot.getY(), gc.getInfoTypeForString(sColor), 0.7) #alpha

	def resetMinimap(self, clearAll=False):
		mainScreen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		mainScreen.minimapClearAllFlashingTiles()
		if(clearAll):
			for i in range (iMapMaxX):
				for j in range (iMapMaxY):
					pPlot = map.plot(i,j)
					if (not pPlot.isNone()):
						mainScreen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_TERRITORY, pPlot.getX(), pPlot.getY(), 1, 0.2) #alpha
			# mainScreen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)
		else:
			# mainScreen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_TERRITORY)
			map.updateMinimapColor()
		# mainScreen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_TERRITORY)
		# -1 = NO_MINIMAPMODE
		# 0 = MINIMAPMODE_TERRITORY
		# 1 = MINIMAPMODE_TERRAIN
		# 2 = MINIMAPMODE_REPLAY
		# 3 = MINIMAPMODE_MILITARY


class RFCEMapExporter:

	def __init__(self, mapManager):
		self.mapManager = mapManager

	def save(self):
		self.saveTo(tDefaultExportFileName)

	def saveTo(self, sFilename):
		if(not self.mapManager.mapsInitiated):
			return
		file = open(sFilename, "w")
		self.writePlayerMap(self.mapManager.settlerMap, "tSettlersMaps", file, "%3d", "# Settler Maps")
		self.writePlayerMap(self.mapManager.warMap, "tWarsMaps", file, "%2d", "# War Maps")
		self.writePlayerMap(self.mapManager.cityNameMap, "tCityMap", file, "\"%s\"", "# City Name Maps")
		self.writeArray(self.mapManager.provinceMap, "tProvinceMap" , file, self.writeTupel, self.write3Digit,  None, "# 3Miro: Provinces - This is right now the only map that doesn't require the [iMaxY - iY - 1] inversion (i.e. visually the map is upside down)")

		self.writeArray(self.mapManager.coreAreasBL, "tCoreAreasTL", file, self.writeCoords, None, self.getCommentCivName, "#Core Area is initial spawn location, no longer relevant for stability")
		self.writeArray(self.mapManager.coreAreasTR, "tCoreAreasBR", file, self.writeCoords, None, self.getCommentCivName)
		self.writeArray(self.mapManager.coreAreasAdditionalPlots, "lExtraPlots", file, self.writeTupel, self.writeCoords, self.getCommentCivName, "#for RiseAndFall. These are (badly named) extra squares used in spawn.")
		self.writeArray(self.mapManager.normalAreasBL, "tNormalAreasTL", file, self.writeCoords, None, self.getCommentCivName, "#These areas are typically used for resurrection.")
		self.writeArray(self.mapManager.normalAreasTR, "tNormalAreasBR", file, self.writeCoords, None, self.getCommentCivName)
		self.writeArray(self.mapManager.normalAreasSubtractedPlots, "tNormalAreasSubtract", file, self.writeTupel, self.writeCoords, self.getCommentCivName, "#These are squares subtracted from normal areas")

		file.close()
		showMessage("Saved RFCEMaps to file: %s" %sFilename)

	def writeMap(self, aMap, sName, file, sFormat="%d", sComment=""):
		file.write("\n\n%s\n%s = (" %(sComment,sName))
		self.writeNestedMap(aMap, file, sFormat)
		file.write(")")
		return

	def writePlayerMap(self, aMap, sName, file, sFormat="%d", sComment=""):
		file.write("\n\n%s\n%s = (" %(sComment,sName))
		length = len(aMap)
		for iPlayer in range(length):
			file.write("\n#" + gc.getPlayer(iPlayer).getCivilizationShortDescription(0) + "\n(")
			self.writeNestedMap(aMap[iPlayer], file, sFormat)
			file.write("\n)")
			if(iPlayer < length-1):
				file.write(",")
		file.write("\n)")
		return

	def writeNestedMap(self, aMap, file, sFormat):
		for iY in range( len(aMap) ):
			file.write("\n(")
			for iX in range( len(aMap[iY]) ):
				sstr = ( sFormat % aMap[iY][iX] )
				if ( iX < iMapMaxX -1 ):
					sstr += ","
				file.write(sstr)
			file.write(")")
			if (iY < iMapMaxY -1):
				file.write(",")
		return

	def writePlayerArray(self, aArray, sName, file, lineFunc, elementFunc=None, lineCommentFunc=None, sComment=""):
		file.write("\n\n%s\n%s = (" %(sComment,sName))

		iLength = len(aArray)
		for i in range(iLength):
			file.write("\n#" + gc.getPlayer(i).getCivilizationShortDescription(0) + "\n(")

			self.writeArrayElements(aArray[i], file, lineFunc, elementFunc, lineCommentFunc)

			file.write("\n)")
			if(i < iLength-1):
				file.write(",")

		file.write("\n)")
		return


	def writeArray(self, aArray, sName, file, lineFunc, elementFunc=None, lineCommentFunc=None, sComment=""):
		file.write("\n\n%s\n%s = (" %(sComment,sName))
		self.writeArrayElements(aArray, file, lineFunc, elementFunc, lineCommentFunc)
		file.write("\n)")
		return

	def writeArrayElements(self, aArray, file, lineFunc, elementFunc, lineCommentFunc):
		iLength = len(aArray)
		for i in range(iLength):
			file.write("\n")

			lineFunc(aArray[i], file, elementFunc)

			if(i < iLength-1):
				file.write(",")

			if(not lineCommentFunc is None):
				file.write(lineCommentFunc(i))
		return

	def writeTupel(self, aTupel, file, elementFunc):
		file.write("(")
		iLength = len(aTupel)
		for i in range(iLength):
			elementFunc(aTupel[i], file)
			if(i < iLength-1):
				file.write(",")
		file.write(")")
		return

	def writeFormat(self, element, file, format):
		file.write( (format % (element)) )

	def write3Digit(self, element, file):
		self.writeFormat(element, file, "%3d")

	def writeCoords(self, coords, file, func=None):
		file.write( ("(%2d,%2d)" % coords) )


	def getCommentCivName(self, iIndex):
		return " #" + gc.getPlayer(iIndex).getCivilizationShortDescription(0)


#Global MapManager
MapManager = RFCEMapManager()
MapVisualizer = RFCEMapVisualizer(MapManager)
MapExporter = RFCEMapExporter(MapManager)


g_nextEventID = 5050

def getNewEventID():
	"""
	Defines a new event and returns its unique ID to be passed to EventManager.beginEvent(id).
	"""
	global g_nextEventID
	id = g_nextEventID
	g_nextEventID += 1

	return id

