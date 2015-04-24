"""
Author: Benjamin Elan

Card:
    Creates a Card with a suit and rank from a standard deck of cards, given an id (0-51) 
    for either bridge or blackjack
        - Raises Exception if the id is not 0-51
Deck:
    Creates a list of type BlackjackCards as implemented in Card.py
        - Overwrites methods that can add non-Card type objects to deck
        - restore function verifies its argument is a list of Card objects
"""
from random import shuffle


class Card:
    """
    Creates a card with a value, suit and points based off of bridge rules
    """
    def __init__(self, id):
        if 0 <= id <= 51:
            self._id = id
        else:
            raise Exception('id needs to be an integer from 0 to 51 inclusive')

    def __lt__(self, other):
        """
        sorts by id
        """
        if self.id() < other.id():
            return True
        return False

    def __repr__(self):
        """
        Makes sure string of Card looks like a card
        """
        suits = {3: '\u2660', 2: '\u2665', 1: '\u2666', 0: '\u2663'}
        cards = {0: "2", 1: "3", 2: "4", 3: "5", 4: "6", 5: "7", 6: "8", 7: "9", 8: "10", 9: "J", 10: "Q", 11: "K",
                 12: "A"}
        return cards[self.rank()] + suits[self.suit()]

    def rank(self):
        """
        :return: rank (a number between 0 and 12, where 2s have rank 0 and aces have rank 12)
        """
        return self._id % 13

    def id(self):
        """
        :return: id (a number between 0 and 51, representing cards in a deck)
        """
        return self._id

    def suit(self):
        """
        :return: suit (clubs = 0, diamonds = 1, hearts = 2, and spades = 3)
        """
        return self._id // 13

    def points(self):
        """
        :return: points (4 if the card is an ace, 3 if it’s a king, 2 if it’s a queen, 1 if it’s a jack, and 0 otherwise)
        """
        point = {12: 4, 11: 3, 10: 2, 9: 1, 8: 0, 7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 0: 0}
        return point[self.rank()]


class BlackjackCard(Card):
    """
    Inherits Card, but sorts by rank and has different point values
    """

    def __lt__(self, other):
        """
        sorts according to rank
        """
        if self.rank() < other.rank():
            return True
        return False

    def points(self):
        """
        points according to the rules of blackjack
        """
        point = {12: 11, 11: 10, 10: 10, 9: 10, 8: 10, 7: 9, 6: 8, 5: 7, 4: 6, 3: 5, 2: 4, 1: 3, 0: 2}
        return point[self.rank()]


def new_deck(cls=Card):
    """
    Creates a deck of cards with a specified type
    :param: the class of the deck to create (default = Card)
    :return: a deck of cards of the specified type
    """
    return [cls(i) for i in range(52)]


class Deck(list):
    """
    Creates a deck of cards (a list of 52 Card objects in order from 2 of clubs up through A of spades)
    """
    def __init__(self):
        list.__init__(self, new_deck(BlackjackCard))

    def shuffle(self):
        """
        rearranges the cards into a new random permutation
        :return: shuffled deck
        """
        return shuffle(self)

    def deal(self, n):
        """
        removes the first n cards from the deck and returns them in a list
        :return: the list of cards dealt
        """
        cards = []
        for count in range(n):
            cards.append(self.pop(0))  # removes first card from deck and adds it to hand
        return cards

    def restore(self, l):
        """
        adds the cards in list 'l' to the end of the deck. If any object in 'l' isn't type Card an Exception is raised
        """
        for card in l:
            if isinstance(card, Card):
                self.append(card)
            else:
                raise Exception("List must only contain Card objects")

    # Overwrites methods that can add non-Card-type objects to deck
    def extend(self, iterable):
        for item in iterable:
            if not isinstance(item, Card):
                raise Exception("All objects must be of type Card")
        list.extend(self, iterable)

    def append(self, p_object):
        if isinstance(p_object, Card):
            list.append(self, p_object)
        else:
            raise Exception("All objects must be of type Card")

    def insert(self, index, p_object):
        if isinstance(p_object, Card):
            list.insert(self, index, p_object)
        else:
            raise Exception("All objects must be of type Card")