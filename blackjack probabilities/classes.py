from numpy import random

from constants import *
from functions import *

class PlayerHand():
    def __init__(self, handList):
        self.hand = handList
        self.state = 'Playing'
        self.doubled = False
        self.actions = []
        

    def __str__(self):
        return f'Hand: {self.hand} | State: {self.state} | Doubled: {self.doubled}'
        

class Blackjack():
    def __init__(self, hand = None, upcard = None, decks:int = DECKS, trueCount:float = 0, double:bool = True, DAS:bool = True, shoeSizeLowerBound: float = 2, maxsplit: int = 3):
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
                
        # creates the list of playerHands
        self.playerHands = [PlayerHand(self.playerHand)]     
        
        # splits the hands in self.playerHands if they ought to be split
        for i in range(maxsplit):
            for playerHand in self.playerHands:
                if (splitCard := playerHand.hand[0]) == playerHand.hand[1]:
                    action = getOptimalSplit(splitCard, self.dealerUpcard, shoe = self.deck)
                    if action == 'Y/N':
                        action = 'Y' if DAS is True else 'N'
                    
                    if action == 'Y' and len(self.playerHands) < maxsplit:
                        playerHand.hand.pop(1)
                        playerHand.hand += [drawnCard1 := random.choice(self.deck)]
                        self.deck.remove(drawnCard1)
                    
                        self.playerHands.append(
                            PlayerHand([splitCard, drawnCard2 := random.choice(self.deck)])
                            )
                        self.deck.remove(drawnCard2)
                    
        if 'A' in self.playerHands[0].hand:
            for playerHand in self.playerHands:
                playerHand.state = 'Done'
 
        # number of hands played. Increases every time Blackjack().result() is run
        self.handsPlayed = 0
        self.shoeSizeLowerBound = shoeSizeLowerBound # at what shoe size the blackjack game ends
        self.maxsplit = maxsplit
        

    def trueCount(self):
        """Returns the true count of the game's shoe."""
        return getTrueCount(self.deck)
    

    def shoeSize(self):
        """Returns the size of the shoe in decks."""
        return len(self.deck)/52


    def deal(self, hand):
        """Deals a card from the deck to the specified hand (self.playerHand or self.dealerHand)."""
        drawnCard = random.choice(self.deck)
        hand += [drawnCard]
        self.deck.remove(drawnCard)


    def playerTurn(self, playerHand, action):
        """Takes an action as an input (H, S, D, Ds) and modifies self.playerHand accordingly."""

        # action = Hit
        if action == 'H':
            # if player's hand is a split Ace
            if playerHand.hand == ['A']:
                # when you split with aces, you only get one card, so playerState is set to Done
                self.deal(playerHand.hand)
                playerHand.state = 'Done'
            # otherwise
            else:
                self.deal(playerHand.hand)
                playerHand.state = 'No more double' # disallow doubling after the first hit
                # if player busts
                if total(playerHand.hand) > 21:
                    playerHand.state = 'Done'
                    
        # action = Stand
        elif action == 'S':
            playerHand.state = 'Done'
            
        # action = Double and double is allowed and player hasn't already hit
        elif 'D' in action and self.double is True and playerHand.state == 'Playing':
            self.deal(playerHand.hand)
            playerHand.doubled = True
            playerHand.state = 'Done'
            
        # action = Double if not hit and double isn't possible
        elif action == 'D':
            self.deal(playerHand.hand)
            playerHand.state = 'No more double' # disallow doubling after the first hit (this probably isn't necessary but i'm keeping it here anyway)
            # if player busts
            if total(playerHand.hand) > 21:
                playerHand.state = 'Done'
                
        # action = Double if not stand and double isn't possible
        elif action == 'Ds':
            playerHand.state = 'Done'
        
        # action that doesn't exist
        else:
            raise Exception('invalid action idk how that happened')
                  

    def playerPlay(self, playerHand):
        """Modifies self.playerHand as if the player is playing optimally."""
        while playerHand.state != 'Done' and total(playerHand.hand) <= 21:
            playerTotal = total(playerHand.hand)
            
            # case where an Ace is in the hand (ie the soft total table must be used)
            if 'A' in playerHand.hand and noAceTotal(playerHand.hand) < 11:
                softValue = playerTotal - 11
                softTotalEntry = f'A,{softValue}'

                action = getOptimalMove(softTotalEntry, self.dealerUpcard, self.deck)
                self.playerTurn(playerHand, action)
                
            # case where an Ace is not in the hand (ie the hard total table must be used)
            else:
                action = getOptimalMove(str(playerTotal), self.dealerUpcard, self.deck)
                self.playerTurn(playerHand, action)
            

    def dealerPlay(self):
        """Makes the dealer play out their hand."""
        while total(self.dealerHand) < 17:
            self.deal(self.dealerHand)
            
    def isPlayerBlackjack(self, playerHand):
        """Returns True if the given playerHand is a blackjack."""
        return True if 'A' in playerHand.hand and '10' in playerHand.hand else False
    
    def isDealerBlackjack(self):
        """Returns True if the dealer's hand is a blackjack."""
        return True if 'A' in self.dealerHand and '10' in self.dealerHand else False
            
    def playAll(self):
        """Plays every hand in the list self.playerHands using optimal moves, then the dealer plays if the player doesn't bust."""
        if not self.isDealerBlackjack():
            for playerHand in self.playerHands:
                self.playerPlay(playerHand)
        if any([not self.isPlayerBlackjack(playerHand) for playerHand in self.playerHands]):
            self.dealerPlay()
        
        # increases number of hands played by 1
        self.handsPlayed += 1
        

    def oneResult(self, playerHand):
        """Given one playerHand, returns the result of that hand vs the dealer's hand."""
        playerTotal = total(playerHand.hand)
        dealerTotal = total(self.dealerHand)
        if self.isPlayerBlackjack(playerHand) and not self.isDealerBlackjack():
            output = 'Blackjack'
        elif playerTotal > 21:
            output = 'Lose'
        elif dealerTotal > 21:
            output = 'Win'
        elif playerTotal < dealerTotal:
            output = 'Lose'
        elif playerTotal == dealerTotal:
            output = 'Push'
        elif dealerTotal < playerTotal:
            output = 'Win'
        
        # if the player doubled, add 'Doubled' to the front of the string
        if playerHand.doubled:
            output = f'Doubled {output}'
            
        return output


    def result(self):
        """Runs self.playAll(), then returns a list of results for every hand in self.playerHands."""
        self.playAll()
        return [self.oneResult(playerHand) for playerHand in self.playerHands]

    
    def reset(self):
        """Starts a new game with the same shoe. The player and dealer hands are randomized."""
        cards = random.choice(self.deck, size = 4, replace = False)
        self.playerHand = [cards[0]] + [cards[2]]
        self.dealerHiddenCard = cards[1]
        self.dealerUpcard = cards[3]
        self.dealerHand = [self.dealerUpcard, self.dealerHiddenCard]
            
        self.deck.remove(self.dealerHiddenCard); self.deck.remove(self.dealerUpcard)
        for card in self.playerHand:
            self.deck.remove(card)
            
        self.playerHands = [PlayerHand(self.playerHand)]
        
        # splits the hands in self.playerHands if they ought to be split
        for i in range(self.maxsplit):
            for playerHand in self.playerHands:
                if (splitCard := playerHand.hand[0]) == playerHand.hand[1]:
                    action = getOptimalSplit(splitCard, self.dealerUpcard, shoe = self.deck)
                    if action == 'Y/N':
                        action = 'Y' if self.DAS is True else 'N'
                    
                    if action == 'Y' and len(self.playerHands) < self.maxsplit:
                        playerHand.hand.pop(1)
                        playerHand.hand += [drawnCard1 := random.choice(self.deck)]
                        self.deck.remove(drawnCard1)
                    
                        self.playerHands.append(
                            PlayerHand([splitCard, drawnCard2 := random.choice(self.deck)])
                            )
                        self.deck.remove(drawnCard2)
                    
        if 'A' in self.playerHands[0].hand:
            for playerHand in self.playerHands:
                playerHand.state = 'Done'
            

    def isFinished(self):
        return True if self.shoeSize() < self.shoeSizeLowerBound else False
        

    def __str__(self):
        return f'Upcard: {self.dealerUpcard}\nHand: {self.playerHand}\nDealer hand: {self.dealerHand}'