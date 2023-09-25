import random
import faker


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
        self.cards = []
        self.build()
        self.shuffle()
        print("Deck reset!")


class Player:
    def __init__(self, name, position):
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
        print("Turn: " + card.val())
        self.cards.append(card)

    def burn(deck, discard_pile):
        card = deck.draw()
        discard_pile.add(card)
        print("Burn: {}".format(card.show()))

    def show(self):
        if not self.cards:
            print("There are no community cards")
        print(", ".join([card.val() for card in self.cards]))

    def clear(self):
        self.cards = []
        print("Community cards cleared!")


def setposition_options(num_players):
    if num_players == 2:
        return ["SB", "BB"]
    elif num_players == 3:
        return ["BTN", "SB", "BB"]
    elif num_players == 4:
        return ["CO", "BTN", "SB", "BB"]
    elif num_players == 5:
        return ["MP1", "CO", "BTN", "SB", "BB"]
    elif num_players == 6:
        return ["UTG", "MP1", "CO", "BTN", "SB", "BB"]
    elif num_players == 7:
        return ["UTG", "UTG+1", "MP1", "CO", "BTN", "SB", "BB"]
    elif num_players == 8:
        return ["UTG", "UTG+1", "MP1", "MP2", "CO", "BTN", "SB", "BB"]
    else:
        return ["UTG", "UTG+1", "MP1", "MP2", "MP3", "CO", "BTN", "SB", "BB"]


def startGame(num_players=None, pick_position=False):
    if not num_players:
        while True:
            try:
                num_players = int(input("Enter number of players (2-9):\n"))
                if num_players < 2 or num_players > 9:
                    raise ValueError
                break

            except ValueError:
                print("Invalid input. Enter a number between 2-9.")

    position_options = setposition_options(num_players)

    # Allows text-based position selecting
    if pick_position:
        try:
            position_text = input("Enter the desired 2- or 3- letter position code:\n")
            position = position_options.index(position_text)
        except:
            position = random.randint(0,num_players)
            position_text = position_options[position]
    else:
        position = random.randint(0,num_players)
        position_text = position_options[position]

    # Creates a bank of names
    names = []
    for i in range(num_players):
        names.append(faker.Faker().name())

    players = []
    # Create NPCs
    for idx, pos in enumerate(position_options):
        # Skip making NPC if player position
        if idx == position:
            players.append(Player("You", position))
            continue

        players.append(Player(names.pop(), pos))


    print("You are now in position: {}".format(position_text))


if __name__ == "__main__":
    startGame()
