import numpy as np
import ast

def roundCount(count, precision = 1):
    """Rounds a true count to a given level of precision. """
    return (1 / precision) * round(precision * count)


def resultToEV(result):
    """Returns the earnings of a result"""
    if 'Lose' in result:
        output = -1
    elif 'Push' in result:
        output = 0
    elif 'Win' in result:
        output = 1
    elif 'Blackjack' in result:
        output = 3/2
    else:
        raise Exception(f'that shit {result} is not a result')
    if 'Doubled' in result:
        output *= 2
    return output


def averageEV(results):
    """Returns the average earnings given an array of results."""
    return np.mean(np.array([resultToEV(result) for result in results]))


def handListToType(handList):
    """Takes an initial hand list and reformats it as either a hard total (ie 20) or a soft total (ie A,9)."""
    handList = ast.literal_eval(handList)
    if handList == ['A', 'A']:
        return 'A,1'
    elif 'A' in handList:
        notAce = [card for card in handList if card != 'A'][0]
        return (f'A,{notAce}')
    else:
        return sum([int(card) for card in handList])
    

def TCHT(trueCount, handType):
    """Returns a string that contains both the true count and hand type for a row."""
    return f'{handType}|{trueCount}'


def TCHTtoHT(TCHT):
    "Given the HT|TC format, returns hand type."
    pipeIndex = TCHT.index('|')
    return TCHT[:pipeIndex]


def TCHTtoTC(TCHT):
    "Given the HT|TC format, returns true count."
    pipeIndex = TCHT.index('|')
    return float(TCHT[(pipeIndex + 1):])


def hardOrSoft(handType):
    try:
        int(handType)
        return 'Hard'
    except:
        return 'Soft'