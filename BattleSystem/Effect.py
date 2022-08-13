from BattleSystem.Dice import Dice
import numpy as np

class Effect:

    def __init__(self, scale_type=None, resist_type=None, damage=None, name="Unknown", description="Unknown",
                 is_fixed_targeting=False, turn_left=0, max_target=1, is_positive=False):
        if damage is None:
            damage = []
        # an effect is a way to describe what compose an Ability and what it does,
        # so then ability can be a composition of effects describing their actions on a targets
        self.scale_type = scale_type  # caster stat used on save dice or scaling on targeted armor
        self.resist_type = resist_type  # target resistance on save Dice else it hit armor class
        self.damage = damage  # list of dice that will do damage or heal on hit
        self.name = name
        self.description = description
        self.is_fixed_targeting = is_fixed_targeting  # if the ability need to hit at least the max target entities
        self.turn_left = turn_left  # turn before an effect is ended (not use for instant cast)

        self.caster_stat = 0  # stat used to store the saving score of the caster
        self.max_target = max_target  # number of target you can hit with an aoe
        self.is_positive = is_positive

    def compute(self):
        dam = 0
        for di in self.damage:
            if self.is_positive:
                dam += di()
            else:
                dam += -di()
        return dam

    def cast(self, from_entity, to_entities):
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
        for entity in to_entities:
            if not self.is_positive:
                if self.resist_type is not None:
                    target_resistance = Dice.dice20() + (entity.get_stat(self.resist_type)-10)/2
                else:
                    target_resistance = entity.armor_class
                targets_resistances.append(target_resistance)
                print("target: " + str(entity))
                print("score target vs caster: " + str(target_resistance) + " / " + str(self.caster_stat))

                if target_resistance < self.caster_stat:
                    dam = self.compute()
                    entity.hit_point -= dam
                    print('target hit, damage done: ' + str(dam))
            else:
                dam = self.compute()
                damages.append(dam)
                entity.hit_point += dam
                print('heal done: ' + str(dam) + "/" + str(entity.hit_point))

        return damages, targets_resistances, self.caster_stat

    def __str__(self):
        desc_damage = "["
        for dice in self.damage:
            desc_damage += "(" + Dice.get_description_dice(dice) + " dice) "
        desc_damage += "]"

        if self.is_positive:
            desc_damage += " heal"
        else:
            desc_damage += " damage"

        return str(self.name) + "[max target: " + str(self.max_target) + "]\n"\
               + str(self.description) + "\n [caster scaling: " + str(self.scale_type) \
               + ", target resistance :" + str(self.resist_type) + "]" + "\n it does " \
               + str(desc_damage)

    @staticmethod
    def to_simple_dict(obj):
        my_dict = {"scale_type": obj.scale_type, "resist_type": obj.resist_type,
                   "damage": [], "name": obj.name, "description": obj.description,
                   "is_fixed_targeting": str(obj.is_fixed_targeting), "turn_left": str(obj.turn_left),
                   "caster_stat": str(obj.caster_stat), "max_target": str(obj.max_target),
                   "is_positive": str(obj.is_positive)}
        for dice in obj.damage:
            my_dict["damage"].append(Dice.to_simple_dict(dice))
        return my_dict

    @staticmethod
    def from_simple_dict(dictionary):
        damage_list = []
        for damage in dictionary["damage"]:
            damage_list.append(Dice.from_simple_dict(damage))

        eff = Effect(scale_type=dictionary["scale_type"], resist_type=dictionary["resist_type"],
                     damage=damage_list, name=dictionary["name"], description=dictionary["description"],
                     is_fixed_targeting=bool(dictionary["is_fixed_targeting"]), turn_left=int(dictionary["turn_left"]),
                     max_target=int(dictionary["max_target"]), is_positive=bool(dictionary["is_positive"]))

        if dictionary["caster_stat"]:
            eff.caster_stat = dictionary["caster_stat"]

        return eff
