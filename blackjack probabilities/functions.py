from constants import *
from numpy import random
from datetime import datetime

def value(card):
    """Takes a card as a string and returns its value as an integer."""
    if card not in possibleUpcards:
        raise Exception(f"Value for card '{card}' does not exist")
    elif card == 'A':
        raise Exception('Ace does not have a hard value')
    else:
        return int(card) if card != 'T' else 10
    

def total(hand):
    """Takes a hand as a list and returns its total."""
    noAceHand = [card for card in hand if card != 'A']
    
    handTotal = sum([value(card) for card in noAceHand])
    
    for i in range(hand.count('A')):
        handTotal += 11 if handTotal < 11 else 1
    
    return handTotal


def noAceTotal(hand):
    return sum([value(card1) for card1 in [card for card in hand if card != 'A']])


def pnGivenC(c):
    """Given a true count c, returns a function n(p) that returns the number of 10+ cards needed to have been drawn if p 6- cards were drawn so that the true count is c."""
    def n(p, decks = 6):
        return(
            ((156 + 4*c) / (156 - 4*c)) * p -
            156 * c * decks / (156 - 4*c)
            )
    return(n)


def cGivenPN(p, n, decks = 6):
    """Returns the true count of a deck given there are p 6- cards and n 10+ cards. Assumes that the number of 7-9 cards is 1/3(p+n)"""
    return(
        (156*p - 156*n) / 
        (156*decks - 4*p - 4*n)
        )


def generateShoe(trueCount = 0, decks = 6):
    # if trueCount = 0, return a full shoe
    if trueCount == 0:
        return(DECK * decks)
    
    # otherwise, find p and n
    else:
        nGivenPC = pnGivenC(trueCount)
        p = 0
        z = .5 # arbitrary float value
        n = .5 # arbitrary float value
        while not n.is_integer() or not z.is_integer():
            p += 1
            if p == 117: # the 117 is hardcoded to 6 decks for now
                raise Exception('Given true count is impossible')
            n = round(nGivenPC(p), 5)
            z = round((1/3) * (p + n), 5)
            if p < 0 or n < 0: # this is super hacky
                n = 1.5 # if p or n is negative, set n to an arbitrary float so that the while loop keeps going
        n, z = int(n), int(z)
        

        lessThan7 = ['2', '3', '4', '5', '6'] * 4 * decks
        zero = ['7', '8', '9'] * 4 * decks
        moreThan9 = ['10', '10', '10', '10', 'A'] * 4 * decks
        
        lessThan7Drawn = random.choice(lessThan7, size = p, replace = False).tolist()
        zeroDrawn = random.choice(zero, size = z, replace = False).tolist()
        moreThan9Drawn = random.choice(moreThan9, size = n, replace = False).tolist()
        
        shoe = DECK * decks
        for card in lessThan7Drawn + zeroDrawn + moreThan9Drawn:
            if not card in shoe:
                print(shoe, '\n', card)
            shoe.remove(card)
            
        return(shoe)


def getTrueCount(shoe, decks = 6):
    """Finds the true count of a shoe given the initial shoe size (number of decks)"""
    # creates a full shoe then removes every card from the given shoe from the full shoe to get the complement
    fullShoe = DECK * decks
    for card in shoe:
        fullShoe.remove(card)
    fullShoeComplement = fullShoe
    
    # number of -1s, +1s, and 0s
    negative = fullShoeComplement.count('10') + fullShoeComplement.count('A')
    positive = sum([fullShoeComplement.count(str(i)) for i in range(2, 7)])
    zero = sum([fullShoeComplement.count(str(i)) for i in range(7, 10)])
    
    # find the true count and return it
    trueCount = (positive - negative) / (len(shoe) / 52)
    return trueCount
    

def getOptimalMove(hand: str, upcard: str, shoe: list[str]):
    """Takes a hand, upcard, and shoe, and then returns the best move. Hand should be formatted as 'A,5' or an integer hard total."""
    
    key = f'{hand},{upcard}'
    
    # if given hand has a potential deviation
    if key in handDeviations:
        deviation = handDeviations[key]
        trueCount = getTrueCount(shoe, decks = DECKS)
        if deviation['sign'] == '>' and deviation['count'] <= trueCount:
            return deviation['action']
        elif deviation['sign'] == '<' and deviation['count'] >= trueCount:
            return deviation['action']
        else:
            if 'A' in hand:
                return softTotals[upcard][hand]
            else:
                return hardTotals[upcard][int(hand)]
    # otherwise
    else:
        if 'A' in hand:
            return softTotals[upcard][hand]
        else:
            return hardTotals[upcard][int(hand)]


def getOptimalSplit(card:str, upcard: str, shoe: list[str]):
    key = f'{card},{upcard}'
    
    # if given hand has a potential deviation
    if key in splitDeviations:
        deviation = splitDeviations[key]
        trueCount = getTrueCount(shoe, decks = DECKS)
        if deviation['sign'] == '>' and deviation['count'] <= trueCount:
            return deviation['action']
        elif deviation['sign'] == '<' and deviation['count'] >= trueCount:
            return deviation['action']
        else:
            return pairSplitting[upcard][card]
    # otherwise
    else:
        return pairSplitting[upcard][card]
    

def getOptimalSurrender(hand:str, upcard:str, shoe: list[str]):
    key = f'{hand},{upcard}'
    
    # if given hand has a potential deviation
    if key in surrenderDeviations:
        deviation = surrenderDeviations[key]
        trueCount = getTrueCount(shoe, decks = DECKS)
        if deviation['sign'] == '>' and deviation['count'] <= trueCount:
            return deviation['action']
        elif deviation['sign'] == '<' and deviation['count'] >= trueCount:
            return deviation['action']
        else:
            print('nope')
            return surrender[upcard][int(hand)]
    else:
        if 'A' in hand:
            return 'N'
        else:
            return surrender[upcard][hand]


# this one isn't used anywhere for now
def superTotal(hand):
    """Same as total, except treats every ace as an 11."""
    handTotal = 0
    for card in hand:
        if card == 'A':
            addValue = 11
        else:
            addValue = value(card)
        handTotal += addValue
    return handTotal

def now():
    return f'{datetime.now():%I:%M:%S %p}'