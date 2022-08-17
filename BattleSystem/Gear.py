from BattleSystem.Ability import Ability


class Gear:
    def __init__(self, abilities=None, name="", description="", is_consumable=False, nb_use=None, charact_bonus=None):
        if abilities is None:
            abilities = []

        if charact_bonus is None:
            charact_bonus = []

        self.charact_bonus = charact_bonus  # bonus that can be added on an entity holding it
        self.abilities = abilities  # a gear can have specific action when you use them
        self.name = name
        self.description = description
        self.is_consumable = is_consumable  # if the gear can be consumed
        self.nb_use = nb_use  # the number of time you can consume it before removing it

    def on_hold(self, entity):
        entity.gear.append(self)
        for key, value in self.charact_bonus.items():
            if key == "stre":
                entity.strength += value
            if key == "const":
                entity.constitution += value
            if key == "dext":
                entity.dexterity += value
            if key == "char":
                entity.charisma += value
            if key == "int":
                entity.intelligence += value
            if key == "wisd":
                entity.wisdom += value
            if key == "armor_class":
                entity.armor_class += value

        for ability in self.abilities:
            entity.ability.append(ability)

    def on_drop(self, entity):
        entity.gear.remove(self)
        for key, value in self.charact_bonus:
            if key == "stre":
                entity.strength -= value
            if key == "const":
                entity.constitution -= value
            if key == "dext":
                entity.dexterity -= value
            if key == "char":
                entity.charisma -= value
            if key == "int":
                entity.intelligence -= value
            if key == "wisd":
                entity.wisdom -= value
            if key == "armor_class":
                entity.armor_class -= value

        for ability in self.abilities:
            entity.ability.remove(ability)

    @staticmethod
    def to_simple_dict(obj):
        my_dict = {"abilities": [], "name": obj.name, "description": obj.description,
                   "is_consumable": obj.is_consumable, "nb_use": obj.nb_use, "charact_bonus": obj.charact_bonus}
        for ability in obj.abilities:
            my_dict["abilities"].append(Ability.to_simple_dict(ability))

        return my_dict

    @staticmethod
    def from_simple_json(dictionary):
        abilities = []
        for ability in dictionary["abilities"]:
            abilities.append(Ability.from_simple_dict(ability))

        this_gear = Gear(abilities=abilities, name=dictionary["name"],
                         description=dictionary["description"], is_consumable=dictionary["is_consumable"],
                         nb_use=dictionary["nb_use"], charact_bonus=dictionary["charact_bonus"])

        return this_gear
