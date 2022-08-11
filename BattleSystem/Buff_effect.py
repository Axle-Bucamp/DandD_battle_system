from BattleSystem.Effect import Effect
from BattleSystem.Dice import Dice


class Buff_effect(Effect):
    def __init__(self, scale_type=None, resist_type=None, damage=None, name="Unknown", description="Unknown",
                 is_fixed_targeting=False, turn_left=0, max_target=1, is_positive=False):
        super().__init__(scale_type, resist_type, damage, name, description,
                         is_fixed_targeting, turn_left, max_target, is_positive)

    def cast(self, from_entity, to_entities):
        nb_targ = 0
        resist = 0
        accuracy_stat = 0
        for entity in to_entities:
            if nb_targ > self.max_target:
                break
            if self.scale_type is None:
                accuracy_stat = Dice.dice20()
            else:
                accuracy_stat = from_entity.get_stat(self.scale_type)
            self.caster_stat = accuracy_stat

            if self.resist_type is None:
                resist = 10
            else:
                resist = from_entity.get_stat(self.resist_type)
            resist = Dice.dice20() + (resist-10)/2

            if accuracy_stat > resist or self.is_positive:
                entity.buff_list.append(self)

        return 0, resist, accuracy_stat

    def __str__(self):
        desc_damage = "["
        for dice in self.damage:
            desc_damage += "(" + Dice.get_description_dice(dice) + " dice) "
        desc_damage += "]"

        if self.is_positive:
            desc_damage += " boost on " + str(self.scale_type)
        else:
            desc_damage += " curse on " + str(self.resist_type)

        return str(self.name) + "[max target: " + str(self.max_target) + "]\n" \
               + str(self.description) + "\n [caster scaling: "\
               + str(self.scale_type) + "]" + "\n it does " \
               + str(desc_damage) + " over " + str(self.turn_left) + " turn"
