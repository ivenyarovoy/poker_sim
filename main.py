import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def show(self):
        print("{} of {}".format(self.value, self.suit))

    def val(self):
        val = "{} of {}".format(self.value, self.suit)
        return str(val)


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

    def reset(self):
        self.cards=[]
        self.build()
        self.shuffle()
        print("Deck reset!")


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.draw())
        return self

    def show(self):
        for card in self.hand:
            card.show()

    def sayName(self):
        print("My name is " + self.name)

class Discard_Pile:
    def __init__(self):
        cards = []
    def add(self, card):
        self.cards.append(card)

class Community_Cards:
    def __init__(self):
        self.cards = []

    def turn(self, deck):
        card = deck.draw()
        print("Turn: "+card.val())
        self.cards.append(card)

    def burn(deck, discard_pile):
        card = deck.draw()
        discard_pile.add(card)
        print("Burn: {}".format(card.show()))

    def show(self):
        if not self.cards: print("There are no community cards")
        for card in self.cards:
            card.show()

    def clear(self):
        self.cards=[]
        print("Community cards cleared!")


if __name__=="__main__":
    nathan=Player("Nathan")
    deck=Deck()
    deck.shuffle()
    comm=Community_Cards()
    comm.show()
    comm.turn(deck)
    comm.show()
    deck.reset()
    comm.clear()
