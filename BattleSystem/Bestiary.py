from BattleSystem.Entity import Entity


class Bestiary:
    bestiary = []

    def __init__(self, bestiar=None):
        if bestiar is None:
            bestiar = []
        Bestiary.bestiary = bestiar

    @staticmethod
    def to_simple_dict(obj):
        my_dict = {"bestiary": []}
        for entity in obj.entities:
            my_dict["bestiary"].append(Entity.to_simple_dict(entity))
        return my_dict

    @staticmethod
    def from_simple_json(dict):
        if "bestiary" in dict.keys() :
            for entity in dict["bestiary"]:
                Bestiary.bestiary.append(Entity.from_simple_json(entity))
