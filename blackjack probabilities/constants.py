import pandas as pd
from config import *

# DO NOT CHANGE THIS NUMBER OR THINGS WILL NOT WORK CORRECTLY
DECKS = decks # number of decks in the dealer's pile (the standard is 6)

# dictionaries that store deviation data
splitDeviations = {'10,4': {'sign':'>', 'count':6, 'action':'Y'}, '10,5':{'sign':'>', 'count':5, 'action':'Y'}, '10,6':{'sign':'>', 'count':4, 'action':'Y'}}
handDeviations = {
    'A,8,4': {'sign':'>', 'count':3, 'action':'Ds'}, 'A,8,5': {'sign':'>', 'count':1, 'action':'Ds'}, 'A,8,5': {'sign':'<', 'count':0, 'action':'S'}, 'A,6,2':{'sign':'>', 'count':1, 'action':'D'},
    '16,9': {'sign':'>', 'count':4, 'action':'S'}, '16,10': {'sign':'>', 'count':0, 'action':'S'}, '16,A': {'sign':'>', 'count':3, 'action':'S'},
    '15,10': {'sign':'>', 'count':4, 'action':'S'}, '15,A': {'sign':'>', 'count':5, 'action':'S'},
    '13,2': {'sign':'<', 'count':-1, 'action':'H'},
    '12,2': {'sign':'>', 'count':3, 'action':'S'}, '12,3': {'sign':'>', 'count':2, 'action':'S'}, '12,4': {'sign':'<', 'count':0, 'action':'H'},
    '10,10': {'sign':'>', 'count':4, 'action':'D'}, '10,A': {'sign':'>', 'count':3, 'action':'D'},
    '9,2': {'sign':'>', 'count':1, 'action':'D'}, '9,7': {'sign':'>', 'count':3, 'action':'D'},
    '8,6': {'sign':'>', 'count':2, 'action':'D'}
     }
surrenderDeviations = {
    '16,8': {'sign':'>', 'count':4, 'action':'Y'}, '16,9': {'sign':'<', 'count':-1, 'action':'N'},
    '15,9': {'sign':'>', 'count':2, 'action':'Y'}, '15,10': {'sign':'<', 'count':0, 'action':'N'},
    '15,A': {'sign':'>', 'count':-1, 'action':'Y'}
    }


possibleUpcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '10', '10', '10', 'A']
DECK = possibleUpcards * 4 # full deck of 52 cards

# optimal move tables
hardTotals = pd.read_csv('hard totals.csv')
softTotals = pd.read_csv('soft totals.csv')
pairSplitting = pd.read_csv('pair splitting.csv')
surrender = pd.read_csv('surrender.csv')

# minor reformatting
hardTotals.set_index('Total', inplace = True)
softTotals.set_index('Soft Total', inplace = True)
pairSplitting.set_index('Pair', inplace = True)
surrender.set_index('Total', inplace = True)