import pandas as pd
from numpy import random
import math

from constants import *
from functions import *
from classes import *
from graphGenerationUtilFuncs import handListToType, roundCount, TCHT
    

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
    handsPlayed = []
    initialTrueCounts = []
    roundedInitialTrueCounts = []
    trueCounts = []
    roundedTrueCounts = []
    initialPlayerHands = []
    handTypes = []
    TCHTs = []
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
                handsPlayed.append(blackjack.handsPlayed)
                initialTrueCounts.append(currentInitialTrueCount := blackjack.initialTrueCount)
                roundedInitialTrueCounts.append(roundCount(currentInitialTrueCount))
                trueCounts.append(currentTrueCount := blackjack.trueCount())
                roundedTrueCounts.append(currentRoundedTrueCount := roundCount(currentTrueCount))
                initialPlayerHands.append(playerHand.hand[:])
                handTypes.append(currentHandType := handListToType(playerHand.hand))
                TCHTs.append(TCHT(currentRoundedTrueCount, currentHandType))
                upcards.append(blackjack.dealerUpcard)
            
            result = blackjack.result()
            
            for index, playerHand in enumerate(blackjack.playerHands):
                finalPlayerHands.append(playerHand.hand)
                finalDealerHands.append(blackjack.dealerHand)
                results.append(result[index])

                blackjack.reset()
    
    data = {'Hands Played': handsPlayed,
            'Initial True Count': initialTrueCounts, 'Rounded Initial True Count': roundedInitialTrueCounts, 'True Count': trueCounts, 'Rounded True Count': roundedTrueCounts,
            'Player Hand': initialPlayerHands, 'Hand Type': handTypes, 'Hand Type|True Count': TCHTs,
            'Upcard': upcards, 'Final Player Hand': finalPlayerHands, 'Final Dealer Hand': finalDealerHands, 
            'Result': results}
    
    return pd.DataFrame(data = data)
    
    print(f'Finished at: {now()}')