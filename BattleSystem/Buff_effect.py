from BattleSystem.Effect import Effect
from BattleSystem.Dice import Dice


class Buff_effect(Effect):
    def __init__(self, scale_type=None, resist_type=None, damage=None, name="Unknown", description="Unknown",
                 is_fixed_targeting=False, turn_left=0, max_target=1):
        super().__init__(scale_type, resist_type, damage, name, description,
                         is_fixed_targeting, turn_left, max_target)
        self.scale_type = None

    def cast(self, from_entity, to_entities):
        nb_targ = 0
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

            if accuracy_stat > resist:
                entity.buff_list.append(self)

        return 0, resist, accuracy_stat
