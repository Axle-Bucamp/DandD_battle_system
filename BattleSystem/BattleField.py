from BattleSystem.Entity import Entity
import numpy as np


class battle_field:

    entities = []
    dead_list = []
    current_player = None

    def __init__(self, battle_list=None, current_player=None, dead_list=None):
        """
        the battlefield is the Game master using its functions to rule the game
        and the interaction between players

        :type battle_list: List
        """
        if battle_list is None:
            battle_list = []
        if dead_list is None:
            dead_list = []
        current_player = current_player

        battle_field.entities = battle_list
        battle_field.current_player = current_player
        battle_field.dead_list = dead_list

    @staticmethod
    def generate_group(nb_mob=1, mob_type=0, ilevel_to_fight=1, difficulty=1, party_id=0, name="Unknown"):
        # way to generate an entity group based on basic description
        level = int(ilevel_to_fight / nb_mob * difficulty)
        probability_of_epic = 0.1 * difficulty
        stats_order = None
        armor_cat = 0
        if mob_type == 0:
            stats_order = ["stre", "const", "dext", "char", "int", "wisd"]
            armor_cat = 3
        if mob_type == 1:
            stats_order = ["dext", "const", "int", "char", "stre", "wisd"]
            armor_cat = 2
        if mob_type == 2:
            stats_order = ["int", "wisd", "const", "char", "dext", "stre"]
            armor_cat = 1
        if mob_type == 3:
            stats_order = ["int", "const", "wisd", "char", "dext", "stre"]
            armor_cat = 1
        if mob_type == 4:
            stats_order = ["dext", "const", "char", "int", "wisd", "stre"]
            armor_cat = 2
        if mob_type == 5:
            stats_order = ["const", "stre", "dext", "char", "int", "wisd"]
            armor_cat = 3
        if stats_order is None:
            stats_order = ["stre", "const", "dext", "char", "int", "wisd"]
            armor_cat = 3

        for i in range(nb_mob):
            pname = name + "_" + str(i + 1)
            battle_field.entities.append(
                Entity.generate_human(probability_of_epic, level, stats_order, armor_cat, party_id, pname))

    @staticmethod
    def sort_init():
        # way to sort all entities with a battle in FIFO to play their turn one by one
        battle_field.entities.sort(reverse=True)
        battle_field.current_player = battle_field.entities[0]

    @staticmethod
    def end_turn():
        # everything that need to happen after a player turn
        ind = battle_field.entities.index(battle_field.current_player)
        battle_field.entities[ind].end_turn()

        for entity in battle_field.entities:
            if entity.hit_point < 1:
                print("dead")
                battle_field.dead_list.append(entity)
                battle_field.entities.remove(entity)

        battle_state, party = battle_field.check_battle_state()
        if battle_state:
            print("next turn")
            battle_field.next_turn(ind)
        else:
            print("party :" + str(np.unique(party)) + "has win the battle")

        return battle_state, np.unique(party)

    @staticmethod
    def next_turn(ind):
        # the way to choose the next player after the current one has played
        if ind < len(battle_field.entities) - 1:
            ind = ind + 1
        else:
            ind = 0
            battle_field.sort_init()

        battle_field.current_player = battle_field.entities[ind]

    @staticmethod
    def check_battle_state():
        # if the battle is not over and how many groups battling are still alive
        party_list = []
        for entity in battle_field.entities:
            party_list.append(entity.party_id)
        party_nb = np.unique(np.array(party_list)).shape[0]

        if party_nb > 1:
            return True, np.unique(np.array(party_list))
        else:
            return False, np.unique(np.array(party_list))

    @staticmethod
    def to_simple_dict(obj):
        # way to store the data into a json save file
        my_dict = {"entities": [], "dead_list": [], "current_player": None}
        for entity in obj.entities:
            my_dict["entities"].append(Entity.to_simple_dict(entity))
        for entity in obj.dead_list:
            my_dict["dead_list"].append(Entity.to_simple_dict(entity))
        if obj.current_player is not None:
            my_dict["current_player"] = str(obj.entities.index(obj.current_player))
        return my_dict

    @staticmethod
    def from_simple_json(dictionary):
        # way to load the data from a json
        if "entities" in dictionary.keys() and "dead_list" in dictionary.keys() and "current_player" in dictionary.keys():
            for entity in dictionary["entities"]:
                battle_field.entities.append(Entity.from_simple_json(entity))

            for entity in dictionary["dead_list"]:
                battle_field.entities.append(Entity.from_simple_json(entity))

            if dictionary["current_player"] and battle_field.current_player is None:
                battle_field.current_player = battle_field.entities[int(dictionary["current_player"])]
