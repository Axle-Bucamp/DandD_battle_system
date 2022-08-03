from random import randrange


class Dice:
    dice12 = lambda x=0: randrange(1, 12, 1)
    dice20 = lambda x=0: randrange(1, 20, 1)
    dice100 = lambda x=0: randrange(1, 100, 1)
    dice8 = lambda x=0: randrange(1, 8, 1)
    dice6 = lambda x=0: randrange(1, 6, 1)
    dice4 = lambda x=0: randrange(1, 4, 1)


if __name__ == '__main__':
    print(Dice.dice12())
