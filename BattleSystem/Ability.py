import pickle


class Ability:
    def __init__(self, effects=None, name="Unknown", description="Unknown", is_principal=False):
        if effects is None:
            effects = []
        self.effects = effects
        self.name = name
        self.description = description
        self.is_principal = is_principal

    def cast(self, from_entity, to_entity):
        damage_done, resistance_target, accuracy_score = [], [], []
        for effect in self.effects:
            print("first effect : ")
            d, r, c = effect.cast(from_entity, to_entity)
            damage_done.append(d)
            resistance_target.append(r)
            accuracy_score.append(c)
        return damage_done, resistance_target, accuracy_score

    def save_ability(self, path="./save/abilities"):
        with open(path + ".pickle", 'wb') as handle:
            pickle.dump(self, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def __str__(self):
        description_effect = "\ncasting the effects :"
        for effect in self.effects:
            description_effect += "\n" + str(effect)
        return self.name + " : \n" + self.description + "\n" + description_effect
