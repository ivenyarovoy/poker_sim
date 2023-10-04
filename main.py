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
    def __init__(self, name, position_text, chips=1000):
        self.name = name
        self.hand = []
        self.position_text = position_text
        self.chips = chips

    def draw(self, deck):
        self.hand.append(deck.draw())
        return self

    def show(self):
        for card in self.hand:
            card.show()

    def sayName(self):
        print("My name is " + self.name)

    def bet(self, amount):
        self.chips -= amount
        return amount


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


def set_position_options(num_players):
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


def startGame(num_players=6, pick_position=False):
    print("Welcome to Poker!")
    if not num_players:
        while True:
            try:
                num_players = int(input("Enter number of players (2-9):\n"))
                if num_players < 2 or num_players > 9:
                    raise ValueError
                break

            except ValueError:
                print("Invalid input. Enter a number between 2-9.")

    position_options = set_position_options(num_players)

    # Allows text-based position selecting
    if pick_position:
        try:
            _ = input("Enter the desired 2- or 3- letter position code:\n")
            player_position = position_options.index(_)
        except:
            player_position = random.randint(0, num_players)
    else:
        player_position = random.randint(0, num_players)

    # Creates a bank of names
    names = []
    for i in range(num_players):
        names.append(faker.Faker().name())

    players = []
    # Create NPCs
    for idx, pos in enumerate(position_options):
        # Skip making NPC if player position
        if idx == player_position:
            players.append(Player("You", pos))
            continue

        players.append(Player(names.pop(), pos))

    print("You are now in position: {}".format(players[player_position].position_text))

    current_player = 0

    # Deal cards
    deck = Deck()
    print("Shuffling deck...")
    deck.shuffle()
    for i in range(2):
        for player in players:
            player.draw(deck)

    # Show cards to player
    print("Your cards:")
    players[player_position].show()

    # Betting round
    print("Betting round begins!")
    highest_bet, pot, current_player = 0, 0, 0
    # TODO: Make this variable
    small_blind, big_blind = 5, 10
    call_bet = big_blind
    players_in_betting_round = players.copy()
    # Enter an infinite loop until betting round is over
    while True:
        for player in players_in_betting_round:
            # Check if player has chips
            if player.chips == 0:
                players_in_betting_round.remove(player)
                continue

            # TODO: make user input
            if player.name is "You":
                print ("Your turn!")
                print ("Your cards:")
                player.show()
                print ("Your stack: {}".format(player.chips))
                bet_or_fold = input("Enter 'b' to bet or 'f' to fold:\n")
                if bet_or_fold != "b":
                    print("You fold!")
                    players_in_betting_round.remove(player)
                # Gets a valid bet
                while True:
                    try:
                        player_bet = int(input("Enter bet amount: "))
                        if player_bet < highest_bet:
                            raise ValueError
                        if player_bet > player.chips:
                            raise IndexError
                    except ValueError as ve:
                        print("You must enter at least as much as the previous bet.")
                    except IndexError as ie:
                        print("You do not have enough chips to bet that much.")
                    break
                print("You bet {}".format(player_bet))
                player.bet(player_bet)
                pot += player_bet

            # If player has less chips than call, they are all-in
            if player.chips <= call_bet:
                pot += player.chips
                print("{} is all-in!".format(player.position_text))
                player.bet(player.chips)
                players_in_betting_round.remove(player)
                continue

            # TODO: Make this more AI like, for now it is random
            player_bet = random.randint(big_blind, player.chips)
            if player_bet > highest_bet:
                highest_bet = player_bet
            pot += player_bet
            player.bet(player_bet)
            print("{} bets {}".format(player.position_text, player_bet))
        break


if __name__ == "__main__":
    startGame()
