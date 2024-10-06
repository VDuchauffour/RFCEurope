from Core import get_scenario_start_turn, game
import CvScreensInterface


# @handler("BeginGameTurn")
def showDawnOfMan(iGameTurn):
    if iGameTurn == get_scenario_start_turn() and game.getAIAutoPlay() > 0:
        CvScreensInterface.dawnOfMan.interfaceScreen()
