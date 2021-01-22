#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Originally written by Philip Sterne <psterne@minervaproject.com>
#
# Jan 16, 2018 Qifan Yang <qifan@minerva.kgi.edu>
# Added implementation for class Card and Carddeck;
# Added multilingual support to reduce workload

import itertools
import gettext

class Card(object):

    # Ref: Applied PRETTY_SUITS and STR_RANKS structure
    # from https://github.com/worldveil/deuces/

    # Constant for suits and ranks
    PRETTY_SUITS = {
        'h' : u'\u2660', # spades
        'd' : u'\u2764', # hearts
        'c' : u'\u2666', # diamonds
        's' : u'\u2663'  # clubs
    }
    STR_RANKS = ['A'] + [str(__) for __ in range(2, 11)] + ['J', 'Q', 'K']

    def __init__(self, suit, rank):
        if not suit in ['h', 'd', 'c', 's']:
            raise Exception('Unknown Card Suit')
        if not rank in range(1, 13):
            raise Exception('Unknown Card rank')
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return self.PRETTY_SUITS[self.suit] + ' ' + self.STR_RANKS[self.rank - 1]

    def value_blackjack(self):
        '''Return the value of a card when in the game of Blackjack.

        Input:
            card: A string which identifies the playing card.

        Returns:
            int, indicating the value of the card in blackjack rule.

        Strictly speaking, Aces can be valued at either 1 or 10, this
        implementation assumes that the value is always 1, and then determines
        later how many aces can be valued at 10.  (This occurs in
        blackjack_value.)
        '''
        return (self.rank < 10) * self.rank + (self.rank >= 10) * 10

    def is_ace(self):
        '''Identify whether or not a card is an ace.

        Input:
            card: A string which identifies the playing card.

        Returns:
            true or false, depending on whether the card is an ace or not.
        '''
        return self.rank == 1

class CardDeck(object):

    def __init__(self, status = 'empty'):
        if status == 'empty':
            self.cards = []
        elif status == 'full':
            self.cards = [Card(suit, rank) for suit, rank in itertools.product(Card.PRETTY_SUITS, range(1, 13))]
        else:
            raise Exception('Unknown deck status')

    def __repr__(self):
        # For output
        return str([Card.PRETTY_SUITS[__.suit] + ' ' + Card.STR_RANKS[__.rank - 1] for __ in self.cards])

    def __getitem__(self, key):
        # For indexing
        return self.cards[key]

    def append(self, card):
        if type(card) != Card:
            raise Exception('Invalid Card')
        self.cards.append(card)

    def pop(self, position = None):
        if position == None:
            return cards.pop()
        else:
            return cards.pop(position)

    # Modify the code here for abstraction.
    # ------------------------------------------------------
    def pop_rand(self, rand_method, x, c, m):
        ''' This element returns a random card from a given list of cards.

        Input:
          deck: list of available cards to return.
          x1: variable for use in the generation of random numbers.
          x2: variable for use in the generation of random numbers.
        '''
        if rand_method == "randU":
            rand_num = randU().generate_numbers()
        elif rand_method == "Mersenne":
            rand_num = mersenne().initialize_generator()
        else:
            raise Exception('Only choose from randU and Mersenne randomized methods')

        return self.cards.pop(rand_num % len(self.cards))
    # ------------------------------------------------------

    def blackjack_value(self):
        '''Calculate the maximal value of a given hand in Blackjack.

        Input:
            cards: A list of strings, with each string identifying a playing card.

        Returns:
            The highest possible value of this hand if it is a legal blackjack
            hand, or -1 if it is an illegal hand.
        '''

        sum_cards = sum([card.value_blackjack() for card in self.cards])
        num_aces = sum([card.is_ace() for card in self.cards])
        aces_to_use = max(int((21 - sum_cards) / 10.0), num_aces)
        final_value = sum_cards + 10 * aces_to_use

        if final_value > 21:
            return -1
        else:
            return final_value

# Modify the code here for abstraction.
# ------------------------------------------------------
def random_number(x, c, m):
    ''' Produce a random number using the Park-Miller method.
    See http://www.firstpr.com.au/dsp/rand31/ for further details of this
    method. It is recommended to use the returned value as the value for x1,
    when next calling the method.'''

    return abs((c * x) % m)
# ------------------------------------------------------

def display(player, dealer, args):
    '''Display the current information available to the player.'''
    print(_('The dealer is showing: '), dealer[0])
    print(_('Your hand is: '), player)

def hit_me(args):
    '''Query the user as to whether they want another car or not.

    Returns:
        A boolean value of True or False.  True means that the user does want
        another card.
    '''
    ans = ""
    while ans.lower() not in ('y', 'n'):
        ans = input(_('Would you like another card? (y/n):'))
    return ans.lower() == 'y'

def game(args):


    # Modify the code here for abstraction.
    # ------------------------------------------------------
    from datetime import datetime
    # randU initiation
    x = int((datetime.utcnow() - datetime.min).total_seconds())
    # Constants given by the RANDU algorithm:
    # https://en.wikipedia.org/wiki/RANDU
    c = 65539
    m = 2147483648
    # ------------------------------------------------------


    # Initialize everything

    deck = CardDeck(status = 'full')

    my_hand = CardDeck(status = 'empty')
    dealer_hand = CardDeck(status = 'empty')

    # Deal the initial cards
    for a in range(2):
        card = deck.pop_rand(rand_method = args.rand_method, x = x, c = c, m = m)
        my_hand.append(card)
        card = deck.pop_rand(rand_method = args.rand_method, x = x, c = c, m = m)
        dealer_hand.append(card)

    # Give the user as many cards as they want (without going bust).
    display(my_hand, dealer_hand, args)
    while hit_me(args):
        card = deck.pop_rand(rand_method = args.rand_method, x = x, c = c, m = m)
        my_hand.append(card)
        display(my_hand, dealer_hand, args)
        if my_hand.blackjack_value() < 0:
            print(_('You have gone bust!'))
            break

    # Now deal cards to the dealer:
    print(_("The dealer has: "), repr(dealer_hand))
    while 0 < dealer_hand.blackjack_value() < 17:
        card = deck.pop_rand(rand_method = args.rand_method, x = x, c = c, m = m)
        dealer_hand.append(card)
        print(_('The dealer hits'))
        print(_('The dealer has: '), repr(dealer_hand))

    if dealer_hand.blackjack_value() < 0:
        print(_("The dealer has gone bust!"))
    else:
        print(_('The dealer sticks with: '), repr(dealer_hand))

    # Determine who has won the game:
    my_total = my_hand.blackjack_value()
    dealer_total = dealer_hand.blackjack_value()
    if dealer_total == my_total:
        print(_("It's a draw!"))
    if dealer_total > my_total:
        print(_("The dealer won!"))
    if dealer_total < my_total:
        print(_("You won!"))


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description="BlackJack Game")
    # Note that the rand_method argument is nor enabled in code!
    parser.add_argument('--rand_method', default='randU',
                        help='The random number generator method. Choose between \'Mersenne\' and \'randU\'.')
    args = parser.parse_args()

    gettext.bindtextdomain('blackjack', 'locale/')
    gettext.textdomain('blackjack')
    _ = gettext.gettext

    print()
    print('BlackJack')
    print('-' * 30)
    print(vars(args))
    print('-' * 30)
    print()

    game(args)

    print()

class randU(object):
    # Constants were from the RANDU formula from:
    # https://en.wikipedia.org/wiki/RANDU
    c = 65539
    m = 2147483648

    def __init__(self, initial=1):
        self.initial = initial

    def generate_numbers(self):
        number = (c*self.initial) % m
        return number

class mersenne(object):

    #!/usr/bin/env python2
    # -*- coding: utf-8 -*-
    """
    Based on the pseudocode in https://en.wikipedia.org/wiki/Mersenne_Twister.

    Generates uniformly distributed 32-bit integers in the range [0, 2^32 − 1] with
    the MT19937 algorithm

    Yaşar Arabacı <yasar11732 et gmail nokta com>
    Modified by Philip Sterne <psterne at minervaproject dot com>
    """
    # Global constants that will never change:
    bitmask_1 = (2**32) - 1  # To get last 32 bits
    bitmask_2 = 2**31  # To get 32nd bit
    bitmask_3 = (2**31) - 1  # To get last 31 bits

    def __init__(self, seed):
        self.seed = seed

    def initialize_generator(self):
        "Initialize the generator from a seed"
        # Create a length 624 list to store the state of the generator
        MT = [0 for i in range(624)]
        index = 0
        MT[0] = seed
        for i in range(1, 624):
            MT[i] = ((1812433253 * MT[i - 1]) ^ (
                (MT[i - 1] >> 30) + i)) & bitmask_1
        return (MT, index)


    def generate_numbers(MT):
        "Generate an array of 624 untempered numbers"
        for i in range(624):
            y = (MT[i] & bitmask_2) + (MT[(i + 1) % 624] & bitmask_3)
            MT[i] = MT[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                MT[i] ^= 2567483615
        return MT


    def extract_number(MT, index):
        """
        Extract a tempered pseudorandom number based on the index-th value,
        calling generate_numbers() every 624 numbers
        """
        if index == 0:
            MT = generate_numbers(MT)
        y = MT[index]
        y ^= y >> 11
        y ^= (y << 7) & 2636928640
        y ^= (y << 15) & 4022730752
        y ^= y >> 18

        index = (index + 1) % 624
        return (MT, index, y)
