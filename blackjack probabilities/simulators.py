import pandas as pd
from numpy import random
import math

from constants import *
from functions import *
from classes import *


# deprecated
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


# deprecated
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


# deprecated
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
    

def simulateHandsPlayedVsTrueCount(games = 10000, decks = 6):
    """Creates a table with two columns: Hands played, and the current true count at the current number of hands played."""
    print(f'--- Beginning generation: {games:,} games ---')
    handsPlayed = []
    trueCounts = []
    for i in range(games):
        if i%(games/100) == 0:
            print(f'{i*100/games}% | {i}  games | {now()}')
        blackjack = Blackjack()
        while not blackjack.isFinished():
            blackjack.result()
            trueCounts.append(blackjack.trueCount())
            handsPlayed.append(blackjack.handsPlayed)
            blackjack.reset()
            
    data = {'Hands Played': handsPlayed,'True Count': trueCounts}
    df = pd.DataFrame(data = data)
    df.to_csv('hands played to true count.csv')
    
    print(f'Finished at: {now()}')
         
    
def simulateManyGames(games = 1000, decks = 6):
    """Creates a table with two columns: Hands played, and the current true count at the current number of hands played."""
    print(f'--- Beginning generation: {games:,} games ---')
    trueCounts = []
    initialPlayerHands = []
    upcards = []
    finalPlayerHands = []
    finalDealerHands = []
    results = []
    for i in range(games):
        if i%(games/100) == 0:
            print(f'{i*100/games}% | {i}  games | {now()}')
        blackjack = Blackjack()
        while not blackjack.isFinished():
            
            for playerHand in blackjack.playerHands:
                trueCounts.append(blackjack.trueCount())
                initialPlayerHands.append(playerHand.hand[:])
                upcards.append(blackjack.dealerUpcard)
            
            result = blackjack.result()
            
            for index, playerHand in enumerate(blackjack.playerHands):
                finalPlayerHands.append(playerHand.hand)
                finalDealerHands.append(blackjack.dealerHand)
                results.append(result[index])

                blackjack.reset()
    
    data = {'True Count': trueCounts, 'Player Hand': initialPlayerHands, 'Upcard': upcards, 'Final Player Hand': finalPlayerHands, 'Final Dealer Hand': finalDealerHands, 'Result': results}
    df = pd.DataFrame(data = data)
    df.to_csv('small game data.csv')
    
    print(f'Finished at: {now()}')