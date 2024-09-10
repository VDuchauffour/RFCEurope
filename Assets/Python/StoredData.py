from Core import civilizations
from CoreTypes import Civ, RandomEvent
from MiscData import NUM_CRUSADES
from PyUtils import rand


class BaseData(object):
    def update(self, data):
        self.__dict__.update(data)


class CivData(BaseData):
    def __init__(self, player_id):
        self.id = player_id
        self.setup()

    def setup(self):
        self.plague_countdown = 0


class PlayerData(BaseData):
    def __init__(self, player_id):
        self.id = player_id
        self.setup()

    def init_ai_wars(self):
        data_mapper = {
            0: [
                Civ.BYZANTIUM,
                Civ.FRANCE,
                Civ.CORDOBA,
                Civ.VENECIA,
                Civ.BURGUNDY,
                Civ.NOVGOROD,
                Civ.SCOTLAND,
                Civ.POLAND,
                Civ.GENOA,
                Civ.PORTUGAL,
                Civ.ARAGON,
                Civ.PRUSSIA,
                Civ.LITHUANIA,
                Civ.DUTCH,
                Civ.POPE,
            ],
            -1: [
                Civ.ARABIA,
                Civ.BULGARIA,
                Civ.GERMANY,
                Civ.NORWAY,
                Civ.KIEV,
                Civ.HUNGARY,
                Civ.CASTILE,
                Civ.DENMARK,
                Civ.MOROCCO,
                Civ.ENGLAND,
                Civ.SWEDEN,
                Civ.AUSTRIA,
                Civ.OTTOMAN,
                Civ.MOSCOW,
            ],
        }
        for threshold, civs in data_mapper.items():
            if self.id in civs:
                self.attacking_threshold = threshold
                break

    def setup(self):
        self.init_ai_wars()

        # RiseAndFall
        self.num_cities = 0
        self.flips_Delay = 0
        self.latest_rebellion_turn = 0
        self.resurrect_suppress = 0
        self.last_turn_alive = 0
        self.last_respawn_turn = 0

        # Reformation
        self.reformation_hit = 0

        # Crusades
        self.voting_power = 0
        self.deviate_targets = False
        self.num_crusader_units_sent = 0


class GameData(BaseData):
    def __init__(self):
        self.setup()

    def update(self, data):
        self.__dict__.update(data)

        for player in self.players.values():
            data = player.__dict__.copy()
            player.setup()
            player.update(data)

        for civ in self.civs.values():
            data = civ.__dict__.copy()
            civ.setup()
            civ.update(data)

    def init_temp_values(self):
        self.temp_top_left = -1
        self.temp_bottom_right = -1
        self.temp_flipping_city = -1

    def init_random_values(self):
        self.random_events = {}
        self.random_events[RandomEvent.LIGHTHOUSE_EARTHQUAKE] = rand(40)
        self.random_events[RandomEvent.BYZANTIUM_VIKING_ATTACK] = rand(10)

    def init_crusade(self):
        # status are:
        # -2, no crusade yet
        # -1 crusade is active but waiting to start (Holy City is Christian and/or another Crusade in progress)
        # 0 or more, the turn when it was initialized
        self.crusade_status = [-2] * NUM_CRUSADES
        self.is_participate_to_crusade = False
        self.favorite_crusader = 0
        self.powerful_crusader = 0
        self.leader_of_crusade = 0
        self.votes_for_favorite = 0
        self.votes_for_powerful = 0
        self.richest_catholic = 0
        self.target = (0, 0)
        self.crusade_power = 0
        self.is_succesful_crusade = False
        self.crusade_to_return = -1
        self.crusade_selected_units = [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]  # Templar Knights, Teutonic Knights, Hospitaller Knights, Knights, Heavy Lancers, Lancers, Siege Weapons, Generic
        self.is_defending_crusade_active = False
        self.last_defensive_crusade = 0

    def init_plagues(self):
        # Sedna17: Set number of GenericPlagues in StoredData
        # 3Miro: Plague 0 strikes France too hard, make it less random and force it to pick Byzantium as starting land
        self.plagues = [
            28
            + rand(5)
            - 10,  # Plagues of Constantinople 612  TODO must start at alexandria, add start city arg
            247 + rand(40) - 20,  # 1341 Black Death
            300 + rand(40) - 20,  # Generic recurrence of plague 1500
            375 + rand(40) - 30,  # 1650 Great Plague
            440 + rand(40) - 30,  # 1740 Small Pox
        ]
        self.is_a_bad_plague = False
        self.is_first_plague = False

    def init_rise_and_fall(self):
        self.new_civ = -1
        self.new_civ_flip = -1
        self.old_civ_flip = -1
        self.spawn_war = 0  # if 1, add units and declare war. If >=2, do nothing
        self.already_switched = False
        self.betrayal_turns = 0
        self.civ_to_resurrect = 0
        self.cities_to_resurrect = []
        self.cheaters_check = [0, -1]
        self.delete_civ = -1

    def init_reformation(self):
        self.is_reformation_active = False
        self.is_counter_reformation_active = False

    def init_persecution(self):
        self.persecution_data = [-1, -1, -1]
        self.persecution_religions = []

    def init_minor_nations(self):
        self.minor_revolt_dates = [-1, -1, -1, -1, -1, -1, -1]
        self.revolut_nation_index = [-1, -1, -1, -1, -1, -1, -1]

    def init_mercenaries(self):
        self.lMercGlobalPool = []
        self.lMercsHiredBy = [
            -1
        ] * 500  # must be at least as long as lMercList (currently allow for 500)

    def init_civics_values(self):
        self.free_religion_choices = []

    def setup(self):
        """Initialise the global script data for usage."""
        self.players = dict((civ.key, PlayerData(civ.id)) for civ in civilizations().majors())
        self.civs = dict((civ.key, CivData(civ.id)) for civ in civilizations())
        self.init_temp_values()
        self.init_random_values()
        self.init_crusade()
        self.init_plagues()
        self.init_rise_and_fall()
        self.init_reformation()
        self.init_persecution()
        self.init_minor_nations()
        self.init_mercenaries()
        self.init_civics_values()

        self.ignore_ai_uhv = True
        self.next_turn_ai_war = -1


data = GameData()
