from BattleSystem.Gear import Gear


class Item_manager:
    gears = []

    def __init__(self, gears=None):
        if gears is None:
            gears = []
        self.gears = gears

    def to_simple_dict(self):
        my_dict = {"gears": []}
        for gear in self.gears:
            my_dict["gears"].append(Gear.to_simple_dict(gear))
        return my_dict

    @staticmethod
    def from_simple_dict(dictionary):
        for gear in dictionary["gears"]:
            Item_manager.gears.append(Gear.from_simple_json(gear))
