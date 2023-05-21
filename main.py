import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def show(self):
        print("{} of {}".format(self.value, self.suit))


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))

    def show(self):
        for card in self.cards:
            card.show()

    def count(self):
        print(len(self.cards))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()


class Player:
    def __init__(self, name, isCpu=True):
        self.name = name
        self.hand = []
        self.cpu = isCpu

    def draw(self, deck):
        self.hand.append(deck.draw())
        return self

    def show(self):
        for card in self.hand:
            card.show()

    def sayName(self):
        print("My name is " + self.name)
