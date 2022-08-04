from BattleSystem.Effect import Effect
from BattleSystem.Ability import Ability
from BattleSystem.Dice import Dice
import pickle


class Ability_manager:
    abilities = []

    def __init__(self, list_abil=None):
        """

        :type list_abil: List
        """
        if list_abil is None:
            list_abil = []
        Ability_manager.abilities = list_abil

    @classmethod
    def basic(cls):
        ldice = [Dice.dice12]
        effect = Effect(scale_type=None, resist_type=None, damage=ldice, name="attack",
                        description="basic attack, one 12 dice",
                        is_fixed_targeting=True, turn_left=0, max_target=1)
        ability = [Ability([effect], name="just smash", description="one dice attack")]

        return cls(ability)

    def save_abilities(self, path="./save/abilities"):
        with open(path + ".pickle", 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_ability(self, path="./save/ability/default.pickle"):
        with open(path, 'rb') as handle:
            b = pickle.load(handle)
        if isinstance(b, Ability):
            self.abilities.append(b)