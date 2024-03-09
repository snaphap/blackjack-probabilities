from constants import *
from functions import *
from classes import *
from simulators import *
    
if __name__ == '__main__':
    simulateManyGames(games = 100000)
    
    

# deprecated todo list:    
    # the Blackjack class needs an option for the passed hand and upcard to not draw from the shoe (so that the true count is preserved)    
    # need the same thing for splitting
    # given a true count, simulate the probability of every possible combination of player hand and upcard and store that data in a table
        # uh the size of the shoe impacts this a bit so i guess randomize between whatever shoes are possible with the true count
    # use this to find the Ev for a shoe with a certain true count
    # find Ev for every type of move, just not the perfect one, to cross check with the given move table
    # ok maybe given a true count, find the Ev for every possible deck size instead of randomizing between them
        # alternatively just make it be the largest possible shoe size that fits the true count

# actual todo list:      
    # test to make sure the optimal split function works correctly
    # simulate a ton of games and record the outcome of a game and the true count among other things
    # simulate imperfect play; determine which move is the best for each hand
    # robust exception handling :D
        # check when given hand or upcard is invalid and throw an exception when that happens

# in progress
    # simulate a ton of games and record the outcome of a game and the true count among other things    

# todo finished
    # make it so that if a player has the same card in their hand and they should split against the current upcard, their hand becomes just one instance of the two cards. This simulates the chance of each hand winning individually
    # need a getTrueCount function that takes a shoe and returns its true count. Needed for the next function in this list
    # need a Blackjack.truecount()
    # need a Blackjack.reset() method that puts the cards in the player and dealer hands in a discard pile and deals them a new hand. Every other attribute should stay the same
    # simulate multiple games and keep track of the number of hands played and the true count. Graph this as a scatter plot or something later
    # create a dict of deviations 
    # implement the functions that find the best move considering count 
 