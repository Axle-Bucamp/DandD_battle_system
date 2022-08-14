from random import randrange


class Dice:
    # storing some dice to use them when need and allow user to choose them, you can custom some here
    dice12 = lambda x=12: Dice.do_dice(x)
    dice20 = lambda x=20: Dice.do_dice(x)
    dice100 = lambda x=100: Dice.do_dice(x)
    dice8 = lambda x=8: Dice.do_dice(x)
    dice6 = lambda x=6: Dice.do_dice(x)
    dice4 = lambda x=4: Dice.do_dice(x)

    @staticmethod
    def do_dice(x):
        # compute one dice
        return randrange(1, x, 1)

    @staticmethod
    def to_simple_dict(obj):
        # way to store them in json for the custom effect to keep their computation
        dice_max_int = "0"
        if obj == Dice.dice12:
            dice_max_int = "12"
        if obj == Dice.dice20:
            dice_max_int = "20"
        if obj == Dice.dice100:
            dice_max_int = "100"
        if obj == Dice.dice8:
            dice_max_int = "8"
        if obj == Dice.dice6:
            dice_max_int = "6"
        if obj == Dice.dice4:
            dice_max_int = "4"
        my_dict = {"dice": dice_max_int}
        return my_dict

    @staticmethod
    def from_simple_dict(dictionary):
        # load from a json a dice
        damage = Dice.dice4
        if dictionary["dice"] == "6":
            damage = Dice.dice6
        if dictionary["dice"] == "8":
            damage = Dice.dice8
        if dictionary["dice"] == "12":
            damage = Dice.dice12
        if dictionary["dice"] == "20":
            damage = Dice.dice20
        if dictionary["dice"] == "100":
            damage = Dice.dice100
        return damage

    @staticmethod
    def get_description_dice(obj):
        # way to describe a dice
        desc = "0"
        if obj == Dice.dice12:
            desc = "12"
        if obj == Dice.dice20:
            desc = "20"
        if obj == Dice.dice100:
            desc = "100"
        if obj == Dice.dice8:
            desc = "8"
        if obj == Dice.dice6:
            desc = "6"
        if obj == Dice.dice4:
            desc = "4"

        return desc

