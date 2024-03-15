from constants import *
from functions import *
from classes import *
from simulators import *
    
from datascience import *
from tableReformatFuncs import *
from graphGeneration import *

if __name__ == '__main__':
    print('Reading game data...')
    gameData = Table().read_table('small game data.csv')
    generateAll(gameData, boundary = 7)


# actual todo list:
    # test to make sure the optimal split function works correctly    
    # implement surrendering including deviations
    # the main simulate function should really keep track of hand count instead of needing a separate function
    # implement betting spreads for Ev calculations
    # precision for rounding true counts is hard coded in some places fix that probably
    # make all the variables actually do things;
        # changing DAS needs to work (i think the EV calculations might be wrong when DAS == False), changing DECKS needs to work
        # add an option for H17 or S17
    # simulate imperfect play; determine which move is the best for each hand
        # idk if im actually gonna do this
        # if the output from the first functions line up with the output from the simulateManyGames function then you can use those
    # robust exception handling
        # check when given hand or upcard is invalid and throw an exception when that happens

# in progress
  

# todo finished
    # make it so that if a player has the same card in their hand and they should split against the current upcard, their hand becomes just one instance of the two cards. This simulates the chance of each hand winning individually
    # need a getTrueCount function that takes a shoe and returns its true count. Needed for the next function in this list
    # need a Blackjack.truecount()
    # need a Blackjack.reset() method that puts the cards in the player and dealer hands in a discard pile and deals them a new hand. Every other attribute should stay the same
    # simulate multiple games and keep track of the number of hands played and the true count. Graph this as a scatter plot or something later
    # create a dict of deviations 
    # implement the functions that find the best move considering count
    # move everything to visual studio
 

# note: i think the code assumes double after split is true somewhere even though there's an option to turn it off
