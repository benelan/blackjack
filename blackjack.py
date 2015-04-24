#!/usr/local/bin/python
"""
Author: Benjamin Elan

A GUI in which you can play a game of Blackjack

-- 5 card rule implemented
-- Checks for blackjack immediately
-- Made Aces soft if total points is over 21
-- Added a balance and ability to bet
    -- cannot bet once you press deal
    -- cannot press hit/stand once the game is over. prevents spamming a win to cheat for higher balance
-- Added score keeping
-- Made it so the deck is not re-shuffled every deal so that you can count cards
-- Made a double down button only available when dealt 10 or 11
"""

from Deck import *
from CardLabel import *
import tkinter as tk
from tkinter.messagebox import showinfo

dealers = []
players = []
count = 2
wins = 0
loses = 0
ties = 0
balance = 100
deck = Deck()
deck.shuffle()
d = False


def result(res):
    """
    Configures scoreboard, balance, and pop up message depending on the result of the game
    :param res: string 'win', 'lose', or 'tie'
    """
    global wins, loses, ties, balance, d
    dealer1.display('front', dealers[0].id())
    if res == 'win':
        if len(b.get()) > 0:
            if d:
                balance += float(b.get())*2
                d = False
            else:
                balance += float(b.get())
            bal.config(text="Balance:  $" + str(balance))
        wins += 1
        showinfo(title="Game Over", message="You win!")
    elif res == 'lose':
        if len(b.get()) > 0:
            if d:
                balance -= float(b.get())*2
                d = False
            else:
                balance -= float(b.get())
            bal.config(text="Balance:  $" + str(balance))
        loses += 1
        showinfo(title="Game over", message="You lose!")
    elif res == 'tie':
        showinfo(title="Tie", message="It's a tie!")
        ties += 1
    score.config(text=" Wins:   " + str(wins) + "\n Loses:  " + str(loses) + "\n Ties:    " + str(ties))
    b.config(state=NORMAL)
    hit_button.config(state=DISABLED)
    stand_button.config(state=DISABLED)
    deal_button.config(state=NORMAL)


def deal():
    """
    Creates a new game of blackjack
    """
    global dealers, players, count, deck
    hit_button.config(state=NORMAL)
    stand_button.configure(state=NORMAL)
    deal_button.config(state=DISABLED)
    b.config(state=DISABLED)
    count = 2
    dealers = []
    players = []
    if (len(deck)) <= 10:
        deck = Deck()
        deck.shuffle()
    dealers = deck.deal(2)
    players = deck.deal(2)
    dealer1.display('back', dealers[0].id())
    player1.display('front', players[0].id())
    dealer2.display('front', dealers[1].id())
    player2.display('front', players[1].id())
    dealer3.display('blank')
    player3.display('blank')
    dealer4.display('blank')
    player4.display('blank')
    dealer5.display('blank')
    player5.display('blank')
    # if dealer or player gets blackjack on deal result is displayed immediately
    if total(dealers) == 21:
        result('lose')
    if total(players) == 21:
        result('win')
    if 12 > total(players) > 9 and len(b.get()) > 0:  # Player must have 10 or 11 at deal to be able to double down
        double_button.config(state=NORMAL)


def total(hand):
    """
    :return: the sum of points from a list of cards according to blackjack rules
    """
    tot = 0
    aces = 0
    for card in hand:
        tot += card.points()
        if card.points() == 11:
            aces += 1
    while tot > 21 and aces > 0:
        aces -= 1
        tot -= 10
    return tot


def hit():
    """
    Gives the player another card and determines if player busts or wins by getting 5 cards
    """
    global players, count, deck
    double_button.config(state=DISABLED)
    players += deck.deal(1)
    player_labels[count].display('front', players[-1:][0].id())
    if total(players) > 21:
        result('lose')
    if len(players) == 5 and total(players) <= 21:  # Extra Credit
        result(' win')
    count += 1


def stand():
    """
    Player chooses to stay and dealer must hit until they receive 17 or above. Determines winner afterwards
    """
    global dealers, players, count, deck
    double_button.config(state=DISABLED)
    dc = 2
    dealer1.display('front', dealers[0].id())
    while total(dealers) < 17 and len(dealers) <= 5:
        dealers += deck.deal(1)
        dealer_labels[dc].display('front', dealers[-1:][0].id())
        dc += 1
    if total(dealers) > 21 or (total(players) > total(dealers)):
        result('win')
    elif len(dealers) == 5 or (total(players) < total(dealers) <= 21):
        result('lose')
    elif total(players) == total(dealers):
        result('tie')


def double():
    """
    If the player has a total of 11 or 10 points as their first two cards they have an option of doubling their bet
    but they can only hit once
    """
    global d
    d = True
    hit()
    stand()


root = tk.Tk()
CardLabel.load_images()

dealer1 = CardLabel(root)
dealer1.grid(row=0, column=0)
root.rowconfigure(0, minsize=115)
root.columnconfigure(0, minsize=85)

dealer2 = CardLabel(root)
dealer2.grid(row=0, column=1)
root.columnconfigure(1, minsize=85)

dealer3 = CardLabel(root)
dealer3.grid(row=0, column=2)
root.columnconfigure(2, minsize=85)

dealer4 = CardLabel(root)
dealer4.grid(row=0, column=3)
root.columnconfigure(3, minsize=85)

dealer5 = CardLabel(root)
dealer5.grid(row=0, column=4)
root.columnconfigure(4, minsize=85)

player1 = CardLabel(root)
player1.grid(row=1, column=0)
root.rowconfigure(1, minsize=115)

player2 = CardLabel(root)
player2.grid(row=1, column=1)

player3 = CardLabel(root)
player3.grid(row=1, column=2)

player4 = CardLabel(root)
player4.grid(row=1, column=3)

player5 = CardLabel(root)
player5.grid(row=1, column=4)
root.columnconfigure(5, minsize=150)

b = Entry(root, width=10)
b.grid(row=2, column=4)
Label(root, text="Place Bet:").grid(row=2, column=3)

score = Label(root, text=" Wins:   " + str(wins) + "\n Loses:  " + str(loses) + "\n Ties:    " + str(ties))
score.grid(row=0, column=5)
bal = Label(root, text="Balance:  $" + str(balance))
bal.grid(row=1, column=5)

deal_button = Button(root, text="Deal", command=deal)
deal_button.grid(row=2, column=0, pady=10, padx=10)

hit_button = Button(root, text="Hit", command=hit)
hit_button.grid(row=2, column=1, pady=10, padx=10)

stand_button = Button(root, text="Stand", command=stand)
stand_button.grid(row=2, column=2, pady=10, padx=10)

double_button = Button(root, text="Double Down", command=double, state=DISABLED)
double_button.grid(row=2, column=5, pady=10, padx=10)

# Made the root window expandable
top = root.winfo_toplevel()
top.rowconfigure(0, weight=1)
top.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

top.rowconfigure(1, weight=1)
top.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(1, weight=1)

top.columnconfigure(2, weight=1)
top.rowconfigure(2, weight=1)
root.rowconfigure(2, weight=1)
root.columnconfigure(2, weight=1)

top.columnconfigure(3, weight=1)
root.columnconfigure(3, weight=1)

top.columnconfigure(4, weight=1)
root.columnconfigure(4, weight=1)

top.columnconfigure(5, weight=1)
root.columnconfigure(5, weight=1)

dealer_labels = [dealer1, dealer2, dealer3, dealer4, dealer5]
player_labels = [player1, player2, player3, player4, player5]

root.title("Blackjack")

if __name__ == '__main__':
    root.mainloop()