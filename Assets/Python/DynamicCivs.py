from Core import civilizations, player
from Events import handler


@handler("BeginPlayerTurn")
def on_begin_player_turn(gameturn, player_id):
    refresh_civ_name(player_id)


@handler("GameStart")
def on_game_start():
    for player_id in civilizations().majors():
        refresh_civ_name(player_id)


def refresh_civ_name(player_id):
    player(player_id).processCivNames()
