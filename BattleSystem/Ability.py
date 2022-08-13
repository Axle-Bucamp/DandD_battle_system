from BattleSystem.Effect import Effect


class Ability:
    def __init__(self, effects=None, name="Unknown", description="Unknown", is_principal=False, level=1):
        if effects is None:
            effects = []
        self.effects = effects
        self.name = name
        self.description = description
        self.is_principal = is_principal
        self.level = level

    def cast(self, from_entity, to_entity):
        damage_done, resistance_target, accuracy_score = [], [], []
        for effect in self.effects:
            print("first effect : ")
            d, r, c = effect.cast(from_entity, to_entity)
            damage_done.append(d)
            resistance_target.append(r)
            accuracy_score.append(c)
        return damage_done, resistance_target, accuracy_score

    def __str__(self):
        description_effect = "\ncasting the effects :"
        for effect in self.effects:
            description_effect += "\n" + str(effect)
        return self.name + " : \n" + self.description + "\n" + description_effect

    @staticmethod
    def to_simple_dict(obj):
        my_dict = {"effects": [], "name": obj.name, "description": obj.description,
                   "is_principal": str(obj.is_principal), "level": str(obj.level)}
        for effect in obj.effects:
            my_dict["effects"].append(Effect.to_simple_dict(effect))
        return my_dict

    @staticmethod
    def from_simple_dict(dictionary):
        effect_list = []
        for effect in dictionary["effects"]:
            effect_list.append(Effect.from_simple_dict(effect))

        return Ability(effects=effect_list, name=dictionary["name"],
                       description=dictionary["description"], is_principal=bool(dictionary["is_principal"]),
                       level=int(dictionary["level"]))

    def __eq__(self, other):
        return self.name == other.name and self.description == other.description and\
               isinstance(other, Ability) and self.is_principal == other.is_principal\
               and self.level == other.level