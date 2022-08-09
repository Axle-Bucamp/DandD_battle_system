from BattleSystem.Dice import Dice


class Effect:

    def __init__(self, scale_type=None, resist_type=None, damage=None, name="Unknown", description="Unknown",
                 is_fixed_targeting=False, turn_left=0, max_target=1, is_positive=False):
        if damage is None:
            damage = []

        self.scale_type = scale_type
        self.resist_type = resist_type
        self.damage = damage
        self.name = name
        self.description = description
        self.is_fixed_targeting = is_fixed_targeting
        self.turn_left = turn_left

        self.caster_stat = 0
        self.max_target = max_target
        self.is_positive = is_positive

    def compute(self):
        dam = 0
        for di in self.damage:
            if self.is_positive:
                dam = di()
            else:
                dam = -di()
        return dam

    def cast(self, from_entity, to_entities):
        print(str(self))
        accuracy_stat = from_entity.get_stat(self.scale_type)
        self.caster_stat = accuracy_stat

        if self.scale_type is not None:
            accuracy_stat = (accuracy_stat - 10) / 2
        else:
            accuracy_stat = 0
        accuracy_stat += Dice.dice20()
        damage = 0

        nb_target = 0
        for entity in to_entities:
            if nb_target > self.max_target:
                break
            if self.resist_type is not None:
                resist_stat = (entity.get_stat(self.resist_type) - 10) / 2
            else:
                resist_stat = 0
            resist_stat += entity.armor_class
            print("accuracy test :" + str(accuracy_stat) + "/" + str(resist_stat))
            if accuracy_stat > resist_stat:
                damage = self.compute()
                print("damage :" + str(damage))
                entity.hit_point += damage
        return damage, resist_stat, accuracy_stat

    def __str__(self):
        return self.name + "[" + " max target: " + str(self.max_target) + "]\n" + self.description

    @staticmethod
    def to_simple_dict(obj):
        my_dict = {"scale_type": obj.scale_type, "resist_type": obj.resist_type,
                   "damage": [], "name": obj.name, "description": obj.description,
                   "is_fixed_targeting": str(obj.is_fixed_targeting), "turn_left": str(obj.turn_left),
                   "caster_stat": str(obj.caster_stat), "max_target": str(obj.max_target)}
        for dice in obj.damage:
            my_dict["damage"].append(Dice.to_simple_dict(dice))
        return my_dict

    @staticmethod
    def from_simple_dict(dict):
        damage_list = []
        for damage in dict["damage"]:
            damage_list.append(Dice.from_simple_dict(damage))

        eff = Effect(scale_type=dict["scale_type"], resist_type=dict["resist_type"],
                     damage=damage_list, name=dict["name"], description=dict["description"],
                     is_fixed_targeting=bool(dict["is_fixed_targeting"]), turn_left=int(dict["turn_left"]),
                     max_target=int(dict["max_target"]))

        if dict["caster_stat"]:
            eff.caster_stat = dict["caster_stat"]

        return eff
