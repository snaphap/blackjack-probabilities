from constants import *
from functions import *
from classes import *
from simulators import *
    
from datascience import *
from tableReformatFuncs import *
from graphGeneration import *

if __name__ == '__main__':
    generateAll(Table().read_table('simulation testing.csv'), boundary = 2)


# actual todo list:
    # optimization:
        # use pd.groupby for gdtcht so that it's not necessary because that shit is not optimized
            # honestly reworking all of the table functions for pandas might be necessary
        # ax.imshow() can use dataframes as input thats useful and efficient maybe use that (it might even use tables !!!)
    # implement surrendering including deviations
    # the main simulate function should really keep track of hand count instead of needing a separate function
    # expected earning given upcard and true count (heatmap) (literally only to make the total number of graphs not a prime number lol)
    # implement betting spreads for Ev calculations
    # precision for rounding true counts is hard coded in some places fix that probably
    # make all the variables actually do things;
        # make a double only on 9,10,11 bool
        # make a resplit aces bool
        # make a 6:5 bool
        # changing DAS needs to work (the player never doubles after splitting), changing DECKS needs to work
        # add an option for H17 or S17
    # simulate imperfect play; determine which move is the best for each hand
        # idk if im actually gonna do this
        # if the output from the first functions line up with the output from the simulateManyGames function then you can use those
    # better exception handling
        # check when given hand or upcard is invalid and throw an exception when that happens

# in progress
    # change the generateAll function to account for the new table
    # ok im getting so confused with the DAS shit but im pretty sure its wrong just resimulate with DAS = False and then fix the rest later
 

# note: i think the code assumes double after split is true somewhere even though there's an option to turn it off
