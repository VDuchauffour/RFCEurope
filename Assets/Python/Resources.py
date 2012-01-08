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
			gc.getMap().plot(36, 24).setBonusType(xml.iRice) #Rice in Iberia
			gc.getMap().plot(86, 2).setBonusType(xml.iRice)  #Rice in Middle East
		if (iGameTurn == xml.i1500AD):
			gc.getMap().plot(55, 35).setBonusType(xml.iRice) #Rice in Italy
		if (iGameTurn == xml.i1250AD):
			gc.getMap().plot( 2, 69).setBonusType(-1) #Remove the NAA from Iceland
		if (iGameTurn == xml.i1452AD):
			gc.getMap().plot(94, 0).setBonusType(xml.iCoffee) #Coffee spawns instead of being preplaced
			gc.getMap().plot(99, 14).setBonusType(xml.iCoffee)
		if (iGameTurn == xml.i1580AD):
			gc.getMap().plot(32, 59).setBonusType(xml.iPotato) #Potatoes in Ireland
			gc.getMap().plot(29, 57).setBonusType(xml.iPotato)
			gc.getMap().plot(69, 49).setBonusType(xml.iPotato) #Poland
			gc.getMap().plot(66, 46).setBonusType(xml.iPotato)
			gc.getMap().plot(60, 48).setBonusType(xml.iPotato) #Northern Germany
			gc.getMap().plot(55, 52).setBonusType(xml.iPotato)
		if (iGameTurn == xml.i1680AD):
			gc.getMap().plot(59, 61).setBonusType(xml.iAccess) #Atlantic Access in Scandinavia

                
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
                        #if ( iPlayer == con.iNorse and ( not gc.getPlayer(con.iEngland).isAlive() ) ):
                                #if ( gc.getMap().plot(36, 54).getBonusType(-1) != -1 ):
                                        #gc.getMap().plot(36, 54).setBonusType(xml.iAccess)

                        


            




                        

