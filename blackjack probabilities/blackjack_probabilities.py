import pandas as pd
from numpy import random
import math

# number of decks in the dealer's pile (the standard is 6)
DECKS = 6

hardTotals = pd.read_csv('hard totals.csv')
softTotals = pd.read_csv('soft totals.csv')
pairSplitting = pd.read_csv('pair splitting.csv')

hardTotals.set_index('Total', inplace = True)
softTotals.set_index('Soft Total', inplace = True)
pairSplitting.set_index('Pair', inplace = True)

possibleUpcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '10', '10', '10', 'A']

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

### IGNORE THESE FOR NOW ###

def pnGivenC(c):
    """Given a true count c, returns a function n(p) that returns the number of 10+ cards needed to have been drawn if p 6- cards were drawn so that the true count is c."""
    def n(p, decks = 6):
        return(
            ((156 + 4*c) / (156 - 4*c)) * p -
            156 * c * decks / (156 - 4*c)
            )
    return(n)

def cGivenPN(p, n):
    return()

def generateDeck(trueCount = 0):
    ...

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

### END OF IGNORE THESE FOR NOW LAND ###

class Blackjack():
    def __init__(self, hand: list[str], upcard: str, decks:int = DECKS, trueCount:float = 0, double:bool = True):
        """Creates a blackjack game."""
        # this is gonna need to factor count in at some point

        # defines the current deck of the blackjack game
        self.deck = possibleUpcards * 4 * decks
        
        # defines whether or not the game allows doubling
        self.double = True
        
        # defines the player and dealer hands
        self.playerHand = hand
        self.dealerUpcard = upcard
        self.dealerHiddenCard = random.choice(self.deck)
        self.dealerHand = [self.dealerUpcard] + [self.dealerHiddenCard]
        
        # removes every card in the player and dealer hands from the deck
        self.deck.remove(self.dealerUpcard); self.deck.remove(self.dealerHiddenCard)
        for card in self.playerHand:
            self.deck.remove(card)
        
        # sets playerState to playing
        self.playerState = 'Playing'

    def deal(self, hand):
        """Deals a card from the deck to the specified hand (self.playerHand or self.dealerHand)."""
        drawnCard = random.choice(self.deck)
        hand += [drawnCard]
        self.deck.remove(drawnCard)

    def playerTurn(self, action):
        """Takes an action as an input (H, S, D, Ds) and modifies self.playerHand accordingly."""
        if action == 'H':
            self.deal(self.playerHand)
            self.playerState = 'No more double'
            if total(self.playerHand) > 21:
                self.playerState = 'Done'
        elif action == 'S':
            self.playerState = 'Done'
        elif 'D' in action and self.double == True and self.playerState == 'Playing':
            self.deal(self.playerHand)
            self.playerState = 'Done'
        elif action == 'D':
            self.deal(self.playerHand)
            if total(self.playerHand) > 21:
                self.playerState = 'Done'
        elif action == 'Ds':
            self.playerState = 'Done'
        else:
            raise Exception('YOU BROKE IT WTF DID YOU DO')
                  
    def playerPlay(self):
        """Modifies self.playerHand as if the player is playing optimally."""
        while self.playerState != 'Done' and total(self.playerHand) <= 21:
            playerTotal = total(self.playerHand)
            
            # case where an Ace is in the hand (ie the soft total table must be used)
            if 'A' in self.playerHand and noAceTotal(self.playerHand) < 11:
                softValue = playerTotal - 11
                softTotalEntry = f'A,{softValue}'

                action = softTotals[self.dealerUpcard][softTotalEntry]
                self.playerTurn(action)
                
            # case where an Ace is not in the hand (ie the hard total table must be used)
            else:
                action = hardTotals[self.dealerUpcard][playerTotal]
                self.playerTurn(action)
            
    def dealerPlay(self):
        if total(self.dealerHand) < 17:
            self.deal(self.dealerHand)
    
    def result(self):
        # the player plays, then the dealer plays
        self.playerPlay()
        self.dealerPlay()
        
        # determines whether the player wins or loses
        playerTotal = total(self.playerHand)
        dealerTotal = total(self.dealerHand)
        if playerTotal > 21:
            return 'Lose'
        elif dealerTotal > 21:
            return 'Win'
            return 'Blackjack'
        elif playerTotal < dealerTotal:
            return 'Lose'
        elif playerTotal == 21:
            return 'Blackjack'
        elif dealerTotal < playerTotal:
            return 'Win'
        else:
            return 'Push'
        
    def __str__(self):
        return f'Upcard: {self.dealerUpcard}, Hand: {self.playerHand}\nPlayer hand: {self.playerHand}\nDealer hand: {self.dealerHand}'
             
#game = Blackjack(['2', '3'], '5')

def simulate(handInput, upcard: str, iterations: int = 1000):
    # initialize counters
    wins = 0
    pushes = 0
    losses = 0
    blackjacks = 0
    
    # if handInput is an integer, treat it as a hard total
    if type(handInput) is int:
        # find the range of possible cards
        card1UpperBound = min(handInput - 2, 10)
        card1LowerBound = max(2, handInput - 10)

    for i in range(iterations):
        if i%(iterations/1000) == 0:
            ...#print(f'{i*100/iterations}%')
            
        if type(handInput) is int:
            # randomly generate the hand based on the possible card range
            card1 = random.choice([i for i in range(card1LowerBound, card1UpperBound + 1)])
            card2 = handInput - card1
            card1, card2 = str(card1), str(card2)
            hand = [card1, card2]
        else:
            hand = [handInput[0], handInput[2:]]
        
        # run the game
        game = Blackjack(hand, upcard)
        result = game.result()
        
        # check later if game.result is actually randomizing correctly
        
        # add to counters depending on the result of the blackjack game
        if result == 'Win':
            wins += 1
        if result == 'Lose':
            losses += 1
        if result == 'Push':
            pushes += 1
        if result == 'Blackjack':
            blackjacks += 1
    
    # divide the counters by the number of iterations and then output as a dictionary
    winrate, lossrate, pushrate, blackjackrate = wins/iterations, losses/iterations, pushes/iterations, blackjacks/iterations
    return(
        {'Win prop': winrate + blackjackrate, 'Loss prop': lossrate, 'Push prop': pushrate, 'Blackjack rate': blackjackrate, 'Ex': (winrate) + (lossrate * -1) + (blackjackrate * 3/2)}
        )



def createHardTotalTable(iterations = 10000, statistic = 'Ex'):
    """Creates a csv that contains the simulated statistic for each hand and upcard in the given table. Ex means expected value."""
    
    if statistic not in ['Ex', 'Win prop', 'Loss prop', 'Push prop']:
        raise Exception(f"Inputted statistic {statistic} is invalid. Valid stat strings are: 'Ex', 'Win prop', 'Loss prop', 'Push prop'")
    
    hardTotalEx = pd.DataFrame(
        index = [str(i) for i in range(20, 3, -1)], 
        columns = [str(i) for i in range(2, 11)] + ['A']
    )
    
    for handTotal, row in hardTotalEx.iterrows():
        for upcard in hardTotals.columns:
            print(f'Upcard: {upcard}, Hand total: {handTotal}')
            hardTotalEx[upcard][handTotal] = simulate(int(handTotal), upcard, iterations = iterations)[statistic]
    hardTotalEx.to_csv('hard total output.csv')


def createSoftTotalTable(iterations = 10000, statistic = 'Ex'):
    """Creates a csv that contains the simulated statistic for each hand and upcard in the given table. Ex means expected value."""
    
    if statistic not in ['Ex', 'Win prop', 'Loss prop', 'Push prop']:
        raise Exception(f"Inputted statistic {statistic} is invalid. Valid stat strings are: 'Ex', 'Win prop', 'Loss prop', 'Push prop'")
    
    softTotalEx = pd.DataFrame(
        index = [f'A,{i}' for i in range(10, 1, -1)], 
        columns = [str(i) for i in range(2, 11)] + ['A']
    )
    
    for hand, row in softTotals.iterrows():
        for upcard in hardTotals.columns:
            print(f'Upcard: {upcard}, Hand: {hand}')
            softTotalEx[upcard][hand] = simulate(hand, upcard, iterations = iterations)[statistic]
    softTotalEx.to_csv('soft total output.csv')

# doubling means you hit once then stop
# when you split aces, you only get one card for each hand

# when generating the cards that satisfy the given true count, make sure to remove those cards from the full shoe rather than making them the shoe