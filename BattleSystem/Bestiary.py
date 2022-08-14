from BattleSystem.Entity import Entity


class Bestiary:
    bestiary = []

    def __init__(self, bestiary=None):
        # storing some entity in the bestiary and way to interact with them
        if bestiary is None:
            bestiary = []
        Bestiary.bestiary = bestiary

    @staticmethod
    def to_simple_dict():
        # way to save a bestiary
        my_dict = {"bestiary": []}
        for entity in Bestiary.bestiary:
            my_dict["bestiary"].append(Entity.to_simple_dict(entity))
        return my_dict

    @staticmethod
    def from_simple_json(dictionary):
        # way to load a bestiary from json
        if "bestiary" in dictionary.keys():
            for entity in dictionary["bestiary"]:
                Bestiary.bestiary.append(Entity.from_simple_json(entity))
