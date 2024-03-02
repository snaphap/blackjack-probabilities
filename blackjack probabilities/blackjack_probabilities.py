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
DECK = possibleUpcards * 4

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

class Blackjack():
    def __init__(self, hand = None, upcard = None, decks:int = DECKS, trueCount:float = 0, double:bool = True, DAS:bool = True):
        """Creates a blackjack game."""

        # defines the current shoe of the blackjack game
        self.deck = generateShoe(trueCount = trueCount)
        
        # defines whether or not the game allows doubling and doubling after splitting
        self.double = double
        self.DAS = DAS
        
        # if no hand or upcard is passed when defining the class, randomize them
        if hand is None and upcard is None:
            cards = random.choice(self.deck, size = 4, replace = False)
            self.playerHand = [cards[0]] + [cards[2]]
            self.dealerHiddenCard = cards[1]
            self.dealerUpcard = cards[3]
            self.dealerHand = [self.dealerUpcard, self.dealerHiddenCard]
            
            self.deck.remove(self.dealerHiddenCard); self.deck.remove(self.dealerUpcard)
            for card in self.playerHand:
                self.deck.remove(card)
        
        # if no hand is passed but an upcard is, randomize the hand
        elif hand is None and not upcard is None:
            self.dealerUpcard = upcard
            self.deck.remove(upcard)
            
            cards = random.choice(self.deck, size = 3, replace = False)
            self.playerHand = [cards[0]] + [cards[2]]
            self.dealerHiddenCard = cards[1]
            self.dealerHand = [self.dealerUpcard, self.dealerHiddenCard]
            
            self.deck.remove(self.dealerHiddenCard)
            for card in self.playerHand:
                self.deck.remove(card)
                
        # if no upcard is passed but a hand is, randomize the upcard
        elif not hand is None and upcard is None:
            self.playerHand = hand
            for card in self.playerHand:
                self.deck.remove(card)
            
            cards = random.choice(self.deck, size = 2, replace = False)
            self.dealerHiddenCard = cards[0]
            self.dealerUpcard = cards[1]
            self.dealerHand = [self.dealerUpcard, self.dealerHiddenCard]
            
            self.deck.remove(self.dealerHiddenCard); self.deck.remove(self.dealerUpcard)
        
        # if both are passed, randomize only the hidden card
        else:
            self.playerHand = hand
            self.dealerUpcard = upcard
            self.dealerHiddenCard = random.choice(self.deck)
            self.dealerHand = [self.dealerUpcard] + [self.dealerHiddenCard]
            
            self.deck.remove(self.dealerUpcard); self.deck.remove(self.dealerHiddenCard)
            for card in self.playerHand:
                self.deck.remove(card)
                
        #splits hand if hand ought to be split
        if self.playerHand[0] == self.playerHand[1]:
            action = pairSplitting[self.dealerUpcard][self.playerHand[0]] # WHERE THE CSV IS CALLED AND MOVE IS CALCULATED
            if action == 'Y/N':
                action = 'Y' if self.DAS == True else 'N'
            if action == 'Y':
                self.playerHand.pop(1)
        
        # sets playerState to playing
        self.playerState = 'Playing'
        
        # if the player doubled. Needed for E(x) calculations later
        self.doubled = False

    def deal(self, hand):
        """Deals a card from the deck to the specified hand (self.playerHand or self.dealerHand)."""
        drawnCard = random.choice(self.deck)
        hand += [drawnCard]
        self.deck.remove(drawnCard)

    def playerTurn(self, action):
        """Takes an action as an input (H, S, D, Ds) and modifies self.playerHand accordingly."""
        
        # action = Hit
        if action == 'H':
            # if player's hand is a split Ace
            if self.playerHand == ['A']:
                # when you split with aces, you only get one card, so playerState is set to Done
                self.deal(self.playerHand)
                self.playerState = 'Done'
            # otherwise
            else:
                self.deal(self.playerHand)
                self.playerState = 'No more double' # disallow doubling after the first hit
                # if player busts
                if total(self.playerHand) > 21:
                    self.playerState = 'Done'
                    
        # action = Stand
        elif action == 'S':
            self.playerState = 'Done'
            
        # action = Double and double is allowed and player hasn't already hit
        elif 'D' in action and self.double == True and self.playerState == 'Playing':
            self.deal(self.playerHand)
            self.doubled = True
            self.playerState = 'Done'
            
        # action = Double if not hit and double isn't possible
        elif action == 'D':
            self.deal(self.playerHand)
            self.playerState = 'No more double' # disallow doubling after the first hit (this probably isn't necessary but i'm keeping it here anyway)
            # if player busts
            if total(self.playerHand) > 21:
                self.playerState = 'Done'
                
        # action = Double if not stand and double isn't possible
        elif action == 'Ds':
            self.playerState = 'Done'
        
        # action that doesn't exist
        else:
            raise Exception('invalid action idk how that happened')
                  
    def playerPlay(self):
        """Modifies self.playerHand as if the player is playing optimally."""
        while self.playerState != 'Done' and total(self.playerHand) <= 21:
            playerTotal = total(self.playerHand)
            
            # case where an Ace is in the hand (ie the soft total table must be used)
            if 'A' in self.playerHand and noAceTotal(self.playerHand) < 11:
                softValue = playerTotal - 11
                softTotalEntry = f'A,{softValue}'

                action = softTotals[self.dealerUpcard][softTotalEntry] # WHERE THE CSV IS CALLED AND MOVE IS CALCULATED
                self.playerTurn(action)
                
            # case where an Ace is not in the hand (ie the hard total table must be used)
            else:
                action = hardTotals[self.dealerUpcard][playerTotal]
                self.playerTurn(action)
            
    def dealerPlay(self):
        """Makes the dealer play out their hand."""
        while total(self.dealerHand) < 17:
            self.deal(self.dealerHand)
    
    # unused for now but will be useful later
    def playOnce(self):
        """Makes the player play with perfect moves, followed by the dealer."""
        self.playerPlay()
        if total(self.playerHand) < 21:
            self.dealerPlay()

    def result(self):
        """Makes the player play with perfect moves, followed by the dealer, then calculates the result."""
        # the player plays, then the dealer plays
        self.playerPlay()
        if total(self.playerHand) < 21:
            self.dealerPlay()
        
        # determines whether the player wins or loses
        playerTotal = total(self.playerHand)
        dealerTotal = total(self.dealerHand)
        if playerTotal > 21:
            output = 'Lose'
        elif dealerTotal > 21:
            output = 'Win'
        elif playerTotal < dealerTotal:
            output = 'Lose'
        elif playerTotal == dealerTotal:
            output = 'Push'
        elif dealerTotal < playerTotal:
            if playerTotal == 21:
                output = 'Blackjack'
            else:
                output = 'Win'
        
        # if the player doubled, add 'Doubled' to the front of the string
        if self.doubled == True:
            output = f'Doubled {output}'
            
        return output
        
    def __str__(self):
        return f'Upcard: {self.dealerUpcard}\nHand: {self.playerHand}\nDealer hand: {self.dealerHand}'

game = Blackjack(['A', '10'], '2')

def simulate(handInput, upcard: str, iterations: int = 1000, trueCount = 0):
    """Simulates one single combination of hand and upcard many times. The shoe used will have a true count of trueCount. handInput is either an integer (hard total) or a string (soft total, such as 'A,2')."""
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
            print(f'{i*100/iterations}%')
            
        if type(handInput) is int:
            if handInput == 2 or handInput == 3:
                hand = [str(handInput)]
            else:
                # randomly generate the hand based on the possible card range
                card1 = random.choice([i for i in range(card1LowerBound, card1UpperBound + 1)])
                card2 = handInput - card1
                card1, card2 = str(card1), str(card2)
                hand = [card1, card2]
        else:
            hand = [handInput[0], handInput[2:]]
        
        # create and run the game
        game = Blackjack(hand, upcard, trueCount = trueCount)
        result = game.result()
        
        # check later if game.result is actually randomizing correctly
        
        # add to counters depending on the result of the blackjack game
        if 'Win' in result:
            wins += 1
        if 'Lose' in result:
            losses += 1
        if 'Push' in result:
            pushes += 1
        if 'Blackjack' in result:
            blackjacks += 1
    
    # divide the counters by the number of iterations and then output as a dictionary
    winrate, lossrate, pushrate, blackjackrate = wins/iterations, losses/iterations, pushes/iterations, blackjacks/iterations
    return(
        {'Win prop': winrate + blackjackrate, 'Loss prop': lossrate, 'Push prop': pushrate, 'Blackjack rate': blackjackrate, 'Ex': (winrate) + (lossrate * -1) + (blackjackrate * 3/2)}
        )



def createHardTotalTable(trueCount = 0, iterations = 10000, statistic = 'Win prop'):
    """Creates a table where the rows are hard totals, the columns are upcards, and each cell is the probability of winning given that situation and true count."""
    
    # check if the passed statistic variable is in the defined dicitonary that simulate() returns
    if statistic not in ['Ex', 'Win prop', 'Loss prop', 'Push prop']:
        raise Exception(f"Inputted statistic {statistic} is invalid. Valid stat strings are: 'Ex', 'Win prop', 'Loss prop', 'Push prop'")
    
    # defines an empty table of hard totals/upcards to write to
    hardTotalEx = pd.DataFrame(
        index = [str(i) for i in range(20, 1, -1)], 
        columns = [str(i) for i in range(2, 11)] + ['A']
    )
    
    # simulates many blackjack games for each combination of hard total and upcard and writes the given statistic to the table
    for handTotal, row in hardTotalEx.iterrows():
        for upcard in hardTotals.columns:
            print(f'Upcard: {upcard}, Hand total: {handTotal}')
            hardTotalEx[upcard][handTotal] = simulate(int(handTotal), upcard, iterations = iterations, trueCount = trueCount)[statistic]
            
    # saves the table to a csv
    hardTotalEx.to_csv(f'hard total output count{trueCount}.csv')


def createSoftTotalTable(trueCount = 0, iterations = 10000, statistic = 'Win prop'):
    """Creates a table where the rows are soft totals, the columns are upcards, and each cell is the probability of winning given that situation and true count."""
    
    # check if the passed statistic variable is in the defined dicitonary that simulate() returns
    if statistic not in ['Ex', 'Win prop', 'Loss prop', 'Push prop']:
        raise Exception(f"Inputted statistic {statistic} is invalid. Valid stat strings are: 'Ex', 'Win prop', 'Loss prop', 'Push prop'")
    
    # defines an empty table of soft totals/upcards to write to
    softTotalEx = pd.DataFrame(
        index = [f'A,{i}' for i in range(10, 1, -1)], 
        columns = [str(i) for i in range(2, 11)] + ['A']
    )
    
    # simulates many blackjack games for each combination of soft total and upcard and writes the given statistic to the table
    for hand, row in softTotals.iterrows():
        for upcard in hardTotals.columns:
            print(f'Upcard: {upcard}, Hand: {hand}')
            softTotalEx[upcard][hand] = simulate(hand, upcard, iterations = iterations)[statistic]
            
    # saves the table to a csv
    softTotalEx.to_csv('soft total output.csv')


if __name__ == '__main__':
    game = Blackjack(hand = ['A', 'A'], upcard = '10')
    game.result()
    print(game)
    

# when splitting you can split until you have 4 hands, often max of 3

# todo list:
    # need a findOptimalMove function that takes a hand, upcard, and shoe (mostly for the true count) and returns the best move that also considers deviations
    # need the same thing for splitting
    # the Blackjack class needs a discardPile attrtibute
    # need a Blackjack.reset() method that puts the cards in the player and dealer hands in a discard pile and deals them a new hand. Every other attribute should stay the same
    # given a true count, simulate the probability of every possible combination of player hand and upcard and store that data in a table
    # use this to find the Ev for a shoe with a certain true count
    # simulate multiple games and keep track of the number of hands played and the true count. Graph this as a scatter plot or something later

# todo finished
    # make it so that if a player has the same card in their hand and they should split against the current upcard, their hand becomes just one instance of the two cards. This simulates the chance of each hand winning individually
    # need a getTrueCount function that takes a shoe and returns its true count. Needed for the next function in this list