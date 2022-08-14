from BattleSystem.Effect import Effect


class Ability:
    def __init__(self, effects=None, name="Unknown", description="Unknown", is_principal=False, level=1):
        # an ability is a list of independent effect that can be cast on target
        if effects is None:
            effects = []
        self.effects = effects
        self.name = name
        self.description = description
        self.is_principal = is_principal  # if the ability can only be used as main move
        self.level = level  # minimum level you need to learn an ability

    def cast(self, from_entity, to_entity):
        # casting all effect
        damage_done, resistance_target, accuracy_score = [], [], []
        for effect in self.effects:
            print("first effect : ")
            d, r, c = effect.cast(from_entity, to_entity)
            damage_done.append(d)
            resistance_target.append(r)
            accuracy_score.append(c)
        return damage_done, resistance_target, accuracy_score

    def __str__(self):
        # way to describe it and it s effects
        description_effect = "\ncasting the effects :"
        for effect in self.effects:
            description_effect += "\n" + str(effect)
        return self.name + " : \n" + self.description + "\n" + description_effect

    @staticmethod
    def to_simple_dict(obj):
        # save it to json
        my_dict = {"effects": [], "name": obj.name, "description": obj.description,
                   "is_principal": str(obj.is_principal), "level": str(obj.level)}
        for effect in obj.effects:
            my_dict["effects"].append(Effect.to_simple_dict(effect))
        return my_dict

    @staticmethod
    def from_simple_dict(dictionary):
        # load it from json
        effect_list = []
        for effect in dictionary["effects"]:
            effect_list.append(Effect.from_simple_dict(effect))

        return Ability(effects=effect_list, name=dictionary["name"],
                       description=dictionary["description"], is_principal=bool(dictionary["is_principal"]),
                       level=int(dictionary["level"]))

    def __eq__(self, other):
        # better way to compare ability for some usage
        return self.name == other.name and self.description == other.description and \
               isinstance(other, Ability) and self.is_principal == other.is_principal \
               and self.level == other.level
