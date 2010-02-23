# Rhye's and Fall of Civilization - Dynamic resources

from CvPythonExtensions import *
import CvUtil
import PyHelpers  
import Popup
import Consts as con

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

### Constants ###

class Resources:
       	
        def checkTurn(self, iGameTurn):
		if (iGameTurn == con.i1000AD):
			gc.getMap().plot(35, 29).setBonusType(con.iRice) #Rice in Iberia
			gc.getMap().plot(86, 2).setBonusType(con.iRice)  #Rice in Middle East
		if (iGameTurn == con.i1500AD):
			gc.getMap().plot(54, 35).setBonusType(con.iRice) #Rice in Italy?
		if (iGameTurn == con.i1580AD): #1580
			gc.getMap().plot(35, 58).setBonusType(con.iPotato) #Potatoes in Ireland
			gc.getMap().plot(37, 60).setBonusType(con.iPotato)
			gc.getMap().plot(68, 49).setBonusType(con.iPotato) #Poland
			gc.getMap().plot(59, 53).setBonusType(con.iPotato) #Northern Germany

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

                        


            




                        
