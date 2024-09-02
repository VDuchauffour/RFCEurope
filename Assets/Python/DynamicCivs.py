from Core import civilizations, player
from Events import handler


@handler("BeginPlayerTurn")
def refresh_civ_name(iGameTurn, iPlayer):
    if iPlayer < civilizations().majors().len():
        player(iPlayer).processCivNames()
