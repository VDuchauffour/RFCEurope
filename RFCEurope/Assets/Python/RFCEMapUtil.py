## RFCEMaptUtils
## contains classes for reading, editing, visualizing and saving SettlerMaps, WarMaps, CityNameMaps, Provinces, CoreAreas and NormalAreas from RFCE
##
## Author: Caliom

from CvPythonExtensions import *
import RFCEMaps
import RFCUtils
import Consts


gc = CyGlobalContext()
utils = RFCUtils.RFCUtils()
Map = CyMap()
localText = CyTranslator()

#Somehow sometimes Map.getGridHeight() doesn't work. I think it has something to do when python scripts are reloaded. For the time beeing i hardcode the map size
#iMapMaxY = Map.getGridHeight()
#iMapMaxX = Map.getGridWidth()
#iNumPlots = Map.numPlots()
iMapMaxX = Consts.iMapMaxX
iMapMaxY = Consts.iMapMaxY
iNumPlots = iMapMaxX * iMapMaxY

# Reserved AreaBorderLayers: 100 - 260(100 to iAreaBorderLayerProvinceOffset+iNumProvinces)
iNumProvinces = 150
iAreaBorderLayerProvinceOffset = 110
iAreaBorderLayerCoreArea = 108
iAreaBorderLayerNormalArea = 109

#The	default filename that the maps are exported to.
tDefaultExportFileName = "./Mods/RFCEurope/Reference/ModdingTools/RFCEMaps.py"

# The values in the shades array are:
# - The value as in the corresponding map. it is important that the values are orderd, highest value first.
# - The color that this value is rendered in
# - a key that is used for the AreaBorderPlots, (like AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS). This key must be unique within one array and should not conflict with other AreaBorderLayer Constants. -1 means that it is not rendered
settlerMapShades = ((700, "COLOR_YELLOW", 100,"highest [700]"),(500, "COLOR_PLAYER_RED", 101, "high [500]"),(400, "COLOR_PLAYER_DARK_RED", 102, "medium [400]"),(300, "COLOR_PLAYER_ORANGE", 103,"low [300]"),(200, "COLOR_PLAYER_PEACH", 104,"lowest [200]"),(20, "COLOR_BLACK", -1, "doesn't settle [20]"),(-1, "COLOR_WHITE", 105, "never [-1]"))
warMapShades = ((8, "COLOR_PLAYER_RED", 100 , "8"),(6, "COLOR_PLAYER_DARK_RED", 101 , "6"),(4, "COLOR_PLAYER_ORANGE", 102 , "4"),(2, "COLOR_PLAYER_LIGHT_ORANGE", 103 , "2"),(0, "COLOR_BLACK", -1 , "0"))

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
			self.provinceMap = self.convertProvinceMap(RFCEMaps.tProinceMap)
			self.settlerMap = self.convertMap(RFCEMaps.tSettlersMaps)
			self.warMap = self.convertMap(RFCEMaps.tWarsMaps)
			self.cityNameMap = self.convertMap(RFCEMaps.tCityMap)
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
	
	
	def getSettlerMapShades(self):
		return settlerMapShades
	
	def getWarMapShades(self):
		return warMapShades
	
	
	def getSettlerValue( self, iPlayer, pPlot):
		return self.getValue(iPlayer, pPlot, self.settlerMap)
	
	def setSettlerValue( self, iPlayer, pPlot, iValue ):
		self.setValue(iPlayer, pPlot, self.settlerMap, iValue)
	
	def increaseSettlerValue(self, iPlayer, pPlot):
		self.changeValue(iPlayer, pPlot, self.settlerMap, settlerMapShades, 1)
	
	def decreaseSettlerValue(self, iPlayer, pPlot):
		self.changeValue(iPlayer, pPlot, self.settlerMap, settlerMapShades, -1)
	
	
	def getWarValue( self, iPlayer, pPlot):
		return self.getValue(iPlayer, pPlot, self.warMap)
		
	def setWarValue( self, iPlayer, pPlot, iValue ):
		self.setValue(iPlayer, pPlot, self.warMap, iValue)
	
	def increaseWarValue(self, iPlayer, pPlot):
		self.changeValue(iPlayer, pPlot, self.warMap, warMapShades, 1)
	
	def decreaseWarValue(self, iPlayer, pPlot):
		self.changeValue(iPlayer, pPlot, self.warMap, warMapShades, -1)
	
	
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
	
	
	def getProvinceName( self, iProvinceIdOrPlot):
		if(isinstance(iProvinceIdOrPlot, CyPlot)):
			iProvince = self.getProvinceId(iProvinceIdOrPlot)
		else:
			iProvince = iProvinceIdOrPlot
		if(iProvince != provinceMapDefault):
			return str(localText.getText( ("TXT_KEY_PROVINCE_NAME_%i" %iProvince),()))
		return ""
	
	def getProvinceId( self, pPlot):
		return self.provinceMap[pPlot.getY()][pPlot.getX()]
	
	def setProvinceId( self, pPlot, iProvince ):
		self.provinceMap[pPlot.getY()][pPlot.getX()] = int(iProvince)
	
	def removeProvince( self, pPlot):
		self.setProvinceId(pPlot, provinceMapDefault)
	
	def isValidProvinceId(self, iProvince):
		return (iProvince >= 0 and iProvince < iNumProvinces)
	
	
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
		for i in range (iMapMaxX):
			for j in range (iMapMaxY):
				pPlot = Map.plot(i,j)
				if (not pPlot.isNone()):
					iValue = self.mapManager.getSettlerValue(self.iPlayer, pPlot)
					for shade in settlerMapShades:
						if(iValue >= shade[0]):
							if(shade[2] > 0):
								CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), shade[2], shade[1], 1.0)
							break
	
	def hideSettlerMap(self):
		for shade in settlerMapShades:
			if(shade[2] > 0):
				CyEngine().clearAreaBorderPlots(shade[2])
	
	
	def showWarMap(self):
		for i in range (iMapMaxX):
			for j in range (iMapMaxY):
				pPlot = Map.plot(i,j)
				if (not pPlot.isNone()):
					iValue = self.mapManager.getWarValue(self.iPlayer, pPlot)
					for shade in warMapShades:
						if(iValue >= shade[0]):
							if(shade[2] > 0):
								CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), shade[2], shade[1], 1.0)
							break
	
	def hideWarMap(self):
		for shade in warMapShades:
			if(shade[2] > 0):
				CyEngine().clearAreaBorderPlots(shade[2])
	
	
	def showCityNames(self):
		for i in range (iMapMaxX):
			for j in range (iMapMaxY):
				pPlot = Map.plot(i,j)
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
		BL = Consts.tCoreAreasTL[self.iPlayer]
		TR = Consts.tCoreAreasBR[self.iPlayer]
		plotX = BL[0]
		plotY = TR[1]
		for iX in range(TR[0]-BL[0]+1):
			for iY in range(TR[1]-BL[1]+1):
				pPlot = Map.plot(plotX+iX, plotY-iY)
				if (not pPlot.isNone()):
					CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), iAreaBorderLayerCoreArea, "COLOR_WHITE", 1.0)
		
		for xy in Consts.tExceptions[self.iPlayer] :
			pPlot = Map.plot(xy[0], xy[1])
			if (not pPlot.isNone()):
				CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), iAreaBorderLayerCoreArea, "COLOR_WHITE", 1.0)
		
	def hideCoreArea(self):
		CyEngine().clearAreaBorderPlots(iAreaBorderLayerCoreArea)
	
	
	def showNormalArea(self):
		exceptions = Consts.tNormalAreasSubtract[self.iPlayer]
		BL = Consts.tNormalAreasTL[self.iPlayer]
		TR = Consts.tNormalAreasBR[self.iPlayer]
		plotX = BL[0]
		plotY = TR[1]
		for iX in range(TR[0]-BL[0]+1):
			for iY in range(TR[1]-BL[1]+1):
				if not (plotX+iX, plotY-iY) in exceptions:
					pPlot = Map.plot(plotX+iX, plotY-iY)
					if (not pPlot.isNone()):
						CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), iAreaBorderLayerCoreArea, "COLOR_WHITE", 1.0)
	
	def hideNormalArea(self):
		CyEngine().clearAreaBorderPlots(iAreaBorderLayerNormalArea)
	
	
	def showProvinces(self):
		iNumColors = len(provinceColors)
		for i in range(iNumPlots):
			pPlot = Map.plotByIndex(i)
			if (not pPlot.isNone()):
				iProvince = self.mapManager.getProvinceId(pPlot)
				if (iProvince != provinceMapDefault):
					sColor = provinceColors[iProvince%iNumColors]
					CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), iAreaBorderLayerProvinceOffset + iProvince, sColor, 1.0)
		self.iHighlightedProvince = -1
	
	def hideProvinces(self):
		for i in range(iNumProvinces):
			self.hideProvince(i)
	
	
	#experimental functions
	def updateProvince(self, iProvince):
		self.colorProvince(iProvince, self.getProvinceColor(iProvince), 1.0)
		
	def highlightProvince(self, iProvince):
		showMessage( "%d - %d" %(self.iHighlightedProvince, iProvince))
		if(not self.mapManager.isValidProvinceId(iProvince) or self.iHighlightedProvince == iProvince):
			return
		self.colorProvince(self.iHighlightedProvince, self.getProvinceColor(self.iHighlightedProvince), 1.0)
		self.iHighlightedProvince = iProvince
		self.colorProvince(iProvince, self.getProvinceColor(iProvince), 2.0)
	
	def colorProvince(self, iProvince, sColor, fAlpha):
		if(not self.mapManager.isValidProvinceId(iProvince)):
			return
		self.hideProvince(iProvince)
		for i in range(iNumPlots):
			pPlot = Map.plotByIndex(i)
			if (not pPlot.isNone()):
				iLoopProvince = self.mapManager.getProvinceId(pPlot)
				if (iLoopProvince == iProvince):
					CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), iAreaBorderLayerProvinceOffset + iProvince, sColor, fAlpha)
	
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
				pPlot = Map.plot(i,j)
				if (not pPlot.isNone()):
					CyEngine().removeLandmark(pPlot)
					#CyEngine().removeSign(pPlot, utils.getHumanID())


class RFCEMapExporter:

	def __init__(self, mapManager):
		self.mapManager = mapManager
	
	def save(self):
		self.saveTo(tDefaultExportFileName)
	
	def saveTo(self, sFilename):
		if(not self.mapManager.mapsInitiated):
			return
		file = open(sFilename, "w")
		self.writePlayerMap(self.mapManager.settlerMap, "tSettlersMaps", file, "%3d", "# settlersMaps")
		self.writePlayerMap(self.mapManager.warMap, "tWarsMaps", file, "%2d", "# warMaps")
		self.writePlayerMap(self.mapManager.cityNameMap, "tCityMap", file, "\"%s\"", "# cityMaps")
		self.writeMap(self.mapManager.provinceMap, "tProinceMap" , file, "%3d", "# 3Miro: Provinces - This is right now the only map that doesn't require the [iMaxY - iY - 1] inversion [i.e. visually the map is upside down]")
		file.close()
		showMessage("Saved RFCEMaps to file: %s" %sFilename)
	
	def writeMap(self, aMap, sName, file, sFormat="%d", sComment=""):
		file.write("\n\n%s\n%s = (" %(sComment,sName))
		self.writeArray(aMap, file, sFormat)
		file.write(")")
		return
		
	def writePlayerMap(self, aMap, sName, file, sFormat="%d", sComment=""):
		file.write("\n\n%s\n%s = (" %(sComment,sName))
		length = len(aMap)
		for iPlayer in range(length):
			file.write("\n#" + gc.getPlayer(iPlayer).getCivilizationShortDescription(0) + "\n(")
			self.writeArray(aMap[iPlayer], file, sFormat)
			file.write("\n)")
			if(iPlayer < length-1):
				file.write(",")
		file.write("\n)")
		return
	
	def writeArray(self, array, file, sFormat):
		for iY in range( len(array) ):
			file.write("\n(")
			for iX in range( len(array[iY]) ):
				sstr = ( sFormat % array[iY][iX] )
				if ( iX < iMapMaxX -1 ):
					sstr += ","
				file.write(sstr)
			file.write(")")
			if (iY < iMapMaxY -1):
				file.write(",")
		return



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
