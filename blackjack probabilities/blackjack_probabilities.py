from constants import *
from functions import *
from classes import *
from simulators import *
    
from datascience import *
from tableReformatFuncs import *
from graphGeneration import *

if __name__ == '__main__':
    #simulateManyGames(games = 10000).to_csv('simulation testing.csv')
    gameData = Table().read_table('simulation testing.csv')
    generateAll(gameData, boundary = 3)
    
    
    
    
    
    


# actual todo list:
    # test trueCountEVBar
    # add a gamenumber column to the simulation so you can select random games later, maybe also a money lost/gained column
    # make all the variables actually do things;
        # make a double only on 9,10,11 bool
        # make a resplit aces bool
        # make a 6:5 bool
        # changing DAS needs to work (the player never doubles after splitting), changing DECKS needs to work
            # ok im getting so confused with the DAS shit but im pretty sure its wrong just resimulate with DAS = False and then fix the rest later
        # add an option for H17 or S17
        # add an option for insurance
    

    
    # implement betting spreads for Ev calculations
    # precision for rounding true counts is hard coded in some places fix that probably
    # add more comments and docstrings
    # simulate imperfect play; determine which move is the best for each hand
        # idk if im actually gonna do this
        # if the output from the first functions line up with the output from the simulateManyGames function then you can use those
    # better exception handling
        # check when given hand or upcard is invalid and throw an exception when that happens

# in progress   
 

# MAYBE: expected earning given upcard and true count (heatmap) (literally only to make the total number of graphs not a prime number lol)
# optimization:
    # maybe convert everything to pandas idk
    # ax.imshow() can use dataframes as input thats useful and efficient maybe use that (it might even use tables !!!)    
