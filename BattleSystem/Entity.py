import numpy as np
from random import random
import math
from BattleSystem.Dice import Dice


class Entity:

    def __init__(self, hit_point=10, armor_class=10, intelligence=10, charisma=10, dexterity=10, strength=10,
                 constitution=10, ilevel=1, gear=None, ability=None, party_id=0, name="Unknown", description=""):
        if ability is None:
            ability = []
        if gear is None:
            gear = []
        self.hit_point = hit_point
        self.max_life = hit_point
        self.armor_class = armor_class
        self.level = ilevel
        self.party_id = party_id

        self.intelligence = intelligence
        self.charisma = charisma
        self.dexterity = dexterity
        self.strength = strength
        self.constitution = constitution

        self.gear = gear
        self.dot_list = []
        self.buff_list = []
        self.ability = ability

        self.main_action = None
        self.second_action = None

        self.name = name
        self.description = description
        self.initiative = 0
        self.compute_initiative()

    @classmethod
    def generate_human(cls, probability_of_epic=0.1, ilevel=1, stats_order=None, armor_cat=3, party_id=0,
                       name="Unknown"):
        if stats_order is None:
            stats_order = ["stre", "const", "dext", "char", "int"]
        stre, const, dext, char, inte = cls.generate_stat(stats_order, probability_of_epic)
        hit_point = cls.compute_health(ilevel, const)
        armor = cls.compute_armor(armor_cat, probability_of_epic, ilevel)

        return cls(hit_point=hit_point, armor_class=armor, intelligence=inte, charisma=char, dexterity=dext,
                   strength=stre, constitution=const, ilevel=ilevel, gear=[], party_id=party_id, name=name,
                   description="")

    @classmethod
    def import_from_file(cls, path):
        return cls()

    @staticmethod
    def compute_health(ilevel, const):
        hit_point = 0
        for i in range(ilevel):
            hit_point += int(Dice.dice12() + (const - 10) / 2)
        return hit_point

    @staticmethod
    def compute_armor(armor_cat, probability_of_epic, ilevel):
        random_part = np.min([abs(np.random.normal(0, math.sqrt(ilevel + probability_of_epic * armor_cat))), 5])
        for i in range(armor_cat):
            random_part += abs(np.random.normal(0, 2.5)) + 2.5

        return np.min([int(random_part), 20])

    @staticmethod
    def generate_stat(stats_order, probability_of_epic):
        stats_point = []
        for i in range(5):
            if random() > probability_of_epic:
                stat_x = Dice.dice8()
                stat_x += Dice.dice12()
            else:
                stat_x = np.min([20, 12 + int(np.random.normal(3, 2))])
            stats_point.append(stat_x)
        stats_point.sort(reverse=True)

        return stats_point[stats_order.index("stre")], stats_point[stats_order.index("const")], \
               stats_point[stats_order.index("dext")], stats_point[stats_order.index("char")], \
               stats_point[stats_order.index("int")]

    def get_stat(self, name):
        # ["stre", "const", "dext", "char", "int"]
        buff = self.compute_buff(name)
        if name is None:
            return 0
        if name == "stre":
            return self.strength + buff
        if name == "const":
            return self.constitution + buff
        if name == "dext":
            return self.dexterity + buff
        if name == "char":
            return self.charisma + buff
        if name == "int":
            return self.intelligence + buff
        else:
            return 0

    def compute_initiative(self):
        self.initiative = Dice.dice20() + (self.dexterity - 10)

    def save(self):
        return True

    def end_turn(self):
        self.compute_dot()

    def cast_to_target(self, entities, is_main: bool):
        damage_done, resistance_target, accuracy_score = [], [], []
        print("cast :" + str(self) + " to " + str(entities))
        if not is_main:
            if self.second_action is not None:
                damage_done, resistance_target, accuracy_score = self.second_action.cast(self, entities)
                self.second_action = None
        else:
            if self.main_action is not None:
                damage_done, resistance_target, accuracy_score = self.main_action.cast(self, entities)
                self.main_action = None
        return damage_done, resistance_target, accuracy_score

    def compute_buff(self, name: str) -> int:
        boost = 0
        for buff in self.buff_list:
            if buff.buff_stat == name:
                boost += buff.compute()
        return boost

    def compute_dot(self):
        dam = 0
        for dot in self.dot_list:
            if dot.resist_type is None:
                if Dice.dice20() < dot.caster_stat:
                    dam += dot.compute()
            else:
                if Dice.dice20() + (self.get_stat(dot.resist_type) + 10) / 2 < dot.caster_stat:
                    dam += dot.compute()

            dot.turn_left -= 1
            if dot.turn_left < 0:
                self.dot_list.remove(dot)

        self.hit_point -= dam

    def rest(self):
        self.hit_point = self.max_life

    def learn_ability(self, ability):
        self.ability.append(ability)

    def equip_gear(self, gear):
        self.gear.append(gear)

    def set_stat(self, value, name):
        if name == "inteligence":
            self.intelligence = value
        if name == "constitution":
            self.constitution = value
        if name == "dexterity":
            self.dexterity = value
        if name == "strength":
            self.strength = value
        if name == "charisma":
            self.charisma = value

    def __gt__(self, entity):
        if self.initiative == entity.initiative:
            return self.dexterity > self.dexterity
        else:
            return self.initiative > entity.initiative

    def __lt__(self, entity):
        if self.initiative == entity.initiative:
            return self.dexterity < self.dexterity
        else:
            return self.initiative < entity.initiative

    def __str__(self):
        return self.name + " : " + self.description