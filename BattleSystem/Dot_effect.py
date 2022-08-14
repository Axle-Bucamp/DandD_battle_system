from BattleSystem.Effect import Effect
from BattleSystem.Dice import Dice
import numpy as np


class Dot_effect(Effect):
    def __init__(self, scale_type=None, resist_type=None, damage=None, name="Unknown", description="Unknown",
                 is_fixed_targeting=False, turn_left=0, max_target=1, is_positive=False):
        # way to use effect that will be cast once and each turn before the turn limit
        super().__init__(scale_type, resist_type, damage, name, description,
                         is_fixed_targeting, turn_left, max_target, is_positive)

    def cast(self, from_entity, to_entities):
        # way to cast it
        print(str(self))
        accuracy_stat = from_entity.get_stat(self.scale_type)
        bonus_stats_caster = (accuracy_stat-10)/2

        if accuracy_stat is not None and self.resist_type is not None:
            maitrise = np.min([2, int(from_entity.level / 4)])
            self.caster_stat = 8 + bonus_stats_caster + maitrise
        else:
            self.caster_stat = Dice.dice20() + bonus_stats_caster

        damages = []
        targets_resistances = []
        i = 0
        for entity in to_entities:
            if i > self.max_target:
                break
            if not self.is_positive:
                if self.resist_type is not None:
                    target_resistance = Dice.dice20() + (entity.get_stat(self.resist_type)-10)/2
                else:
                    target_resistance = entity.armor_class
                targets_resistances.append(target_resistance)
                print("target: " + str(entity))
                print("score target vs caster: " + str(target_resistance) + " / " + str(self.caster_stat))

                if target_resistance < self.caster_stat:
                    entity.dot_list.append(self)
                    print('target will suffer the dot')
            else:
                print('target will be healed over time')
                entity.dot_list.append(self)

        return damages, targets_resistances, self.caster_stat

    def __str__(self):
        # description of those effect
        desc_damage = "["
        for dice in self.damage:
            desc_damage += "(" + Dice.get_description_dice(dice) + " dice) "
        desc_damage += "]"

        if self.is_positive:
            desc_damage += " heal"
        else:
            desc_damage += " damage"

        return str(self.name) + "[max target: " + str(self.max_target) + "]\n" \
               + str(self.description) + "\n [caster scaling: " + str(self.scale_type) \
               + ", target resistance :" + str(self.resist_type) + "]" + "\n it does " \
               + str(desc_damage) + " over " + str(self.turn_left) + " turn"
