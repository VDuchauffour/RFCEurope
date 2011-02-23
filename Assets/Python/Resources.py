# Rhye's and Fall of Civilization - Dynamic resources

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
import Popup
import Consts as con
import XMLConsts as xml

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

### Constants ###

class Resources:
       	
        def checkTurn(self, iGameTurn):
		if (iGameTurn == xml.i1000AD):
			gc.getMap().plot(35, 29).setBonusType(xml.iRice) #Rice in Iberia
			gc.getMap().plot(86, 2).setBonusType(xml.iRice)  #Rice in Middle East
		if (iGameTurn == xml.i1500AD):
			gc.getMap().plot(54, 35).setBonusType(xml.iRice) #Rice in Italy?
		if (iGameTurn == xml.i1580AD): #1580
			gc.getMap().plot(35, 58).setBonusType(xml.iPotato) #Potatoes in Ireland
			gc.getMap().plot(37, 60).setBonusType(xml.iPotato)
			gc.getMap().plot(68, 49).setBonusType(xml.iPotato) #Poland
			gc.getMap().plot(59, 53).setBonusType(xml.iPotato) #Northern Germany
                        gc.getMap().plot(49, 54).setBonusType(xml.iAccess) #Dutch AA
		if (iGameTurn == xml.i1680AD):
			gc.getMap().plot(59, 61).setBonusType(xml.iAccess) #Atlantic Access in Scandinavia

		# 3Miro: resources appear
                #if (iGameTurn == 5): #otherwise it's picked by Portugal at the beginning
                #        gc.getMap().plot(49, 43).setImprovementType(con.iHut)


                #if (iGameTurn == con.i450AD): #(dye added later to prevent Carthaginian UHV exploit)
                #        gc.getMap().plot(53, 51).setBonusType(iDye) #France
                #        gc.getMap().plot(53, 55).setBonusType(iDye) #England
                #if (not gc.getPlayer(0).isPlayable()): #late start condition
                #        if (iGameTurn == con.i600AD): 
                #                gc.getMap().plot(53, 51).setBonusType(iDye) #France
                #                gc.getMap().plot(53, 55).setBonusType(iDye) #England
                    
                 
                #setImprovementType(ImprovementType eNewValue)
                #setPlotType(PlotType eNewValue, BOOL bRecalculate, BOOL bRebuildGraphics)
                #setTerrainType(TerrainType eNewValue, BOOL bRecalculate, BOOL bRebuildGraphics)
		#pass

                        


            




                        
