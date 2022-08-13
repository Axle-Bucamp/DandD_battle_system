class Gear:
    def __init__(self, abilities=None, name="", description="", is_consumable=False, nb_use=None, charact_bonus=None):
        if abilities is None:
            abilities = []

        if charact_bonus is None:
            charact_bonus = []

        self.charact_bonus = charact_bonus
        self.abilities = abilities
        self.name = name
        self.description = description
        self.is_consumable = is_consumable
        self.nb_use = nb_use

    def on_hold(self, entity):
        entity.gear.append(self)
        for key, value in self.charact_bonus:
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
            entity.append(ability)

    def on_drop(self, entity):
        entity.gear.remvoe(self)
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
            entity.remove(ability)
