from random import randrange


class Dice:
    dice12 = lambda x=0: randrange(1, 12, 1)
    dice20 = lambda x=0: randrange(1, 20, 1)
    dice100 = lambda x=0: randrange(1, 100, 1)
    dice8 = lambda x=0: randrange(1, 8, 1)
    dice6 = lambda x=0: randrange(1, 6, 1)
    dice4 = lambda x=0: randrange(1, 4, 1)

    @staticmethod
    def to_simple_dict(obj):
        dice_max_int = 0
        if obj == Dice.dice12:
            dice_max_int = 12
        if obj == Dice.dice20:
            dice_max_int = 20
        if obj == Dice.dice100:
            dice_max_int = 100
        if obj == Dice.dice8:
            dice_max_int = 8
        if obj == Dice.dice6:
            dice_max_int = 6
        if obj == Dice.dice4:
            dice_max_int = 4
        my_dict = {"dice": dice_max_int}
        return my_dict

    @staticmethod
    def from_simple_dict(dict):
        damage = Dice.dice4
        if dict["damage"] == 6:
            damage = Dice.dice6
        if dict["damage"] == 8:
            damage = Dice.dice8
        if dict["damage"] == 12:
            damage = Dice.dice12
        if dict["damage"] == 20:
            damage = Dice.dice20
        if dict["damage"] == 100:
            damage = Dice.dice100
        return damage
