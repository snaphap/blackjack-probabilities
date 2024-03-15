from datascience import *
from graphGenerationUtilFuncs import *

def addRoundedTC(gameData):
    """Returns gameData with an additional rounded true count column."""
    return gameData.with_column('Rounded True Count', gameData.apply(roundCount, 'True Count'))


def addHandTypes(gameData):
    """Returns gameData with an additional hand type column."""
    handTypes = gameData.apply(handListToType, 'Player Hand')
    return gameData.with_column('Hand Type', handTypes)


def gameDataTCHT(gameDataHandTypes):
    """Takes a table returned by addHandTypes and returns the same table with an additional Hand Type|True Count column."""
    return gameDataHandTypes.with_column('Hand Type|True Count', gameDataHandTypes.apply(TCHT, 'Rounded True Count', 'Hand Type'))


def groupedGDTCHT(gameDataTCHT):
    """Takes a table returned by gameDataTCHT and groups by true count and hand type, applying the averageEV function to the results for each group. Also adds a Hard or Soft Total column."""
    groupedGameDataTCHT = gameDataTCHT.select('Hand Type|True Count', 'Result').group('Hand Type|True Count', averageEV)
    TCHTHandTypes = groupedGameDataTCHT.apply(TCHTtoHT, 'Hand Type|True Count')
    TCHTTrueCounts = groupedGameDataTCHT.apply(TCHTtoTC, 'Hand Type|True Count')
    groupedGameDataTCHT = groupedGameDataTCHT.with_columns(
        'Hand Type', TCHTHandTypes,
        'True Count', TCHTTrueCounts
    )
    return groupedGameDataTCHT.with_column('Hard or Soft Total', groupedGameDataTCHT.apply(hardOrSoft, 'Hand Type'))


def filterGDTCHT(groupedGDTCHT, boundary = 6):
    """Takes a table returned by groupedGDTCHT and returns a table only with entries whose true count is in the interval [-boundary, boundary]."""
    return groupedGDTCHT.where('True Count', are.between(-1*boundary, boundary+1))


def GDTCHThardTotals(GDTCHT):
    """Takes a GDTCHT table and returns the same table with only entries whose hand type is a hard total."""
    return GDTCHT.where('Hard or Soft Total', are.equal_to('Hard'))


def hardTotalColumns(GDTCHThardTotals, boundary):
    """Takes a table returned from GDTCHThardTotals, returns a table to be inputted into hardTotalLineGraph and hardTotalHeatMap."""
    restrictedTrueCounts = [i for i in range(-1, -1*boundary-1, -1)] + [i for i in range(0, boundary+1)]
    table = Table().with_column('True Counts', restrictedTrueCounts)
    for i in range(4, 21):
        averageEVs = GDTCHThardTotals.where('Hand Type', are.equal_to(str(i))).column('Result averageEV')
        table = table.with_column(f'{i}', averageEVs)
    table = table.sort('True Counts')
    return table


def GDTCHTsoftTotals(GDTCHT):
    """Takes a GDTCHT table and returns the same table with only entries whose hand type is a soft total."""
    return GDTCHT.where('Hard or Soft Total', are.equal_to('Soft'))


def softTotalColumns(GDTCHTsoftTotals, boundary):
    """Takes a table returned from GDTCHThardTotals, returns a table to be inputted into hardTotalLineGraph and hardTotalHeatMap."""
    restrictedTrueCounts = [i for i in range(-1, -1*boundary-1, -1)] + [i for i in range(0, boundary+1)]
    table = Table().with_column('True Counts', restrictedTrueCounts)
    for i in range(2, 11):
        averageEVs = GDTCHTsoftTotals.where('Hand Type', are.equal_to(f'A,{i}')).column('Result averageEV')
        table = table.with_column(f'A,{i}', averageEVs)
    table = table.sort('True Counts')
    return table


def trueCountData(gameDataRoundedTC, boundary):
    """Returns a table with true count data; to be inputted into FUNCTION NOT NAMED YET PUT IT LATER."""
    counts = gameDataRoundedTC.group('Rounded True Count').column('count')
    gameDataEV = gameDataRoundedTC.select('Rounded True Count', 'Result').group('Rounded True Count', averageEV).with_column('Count', counts)
    filteredGameDataEV = gameDataEV.where('Rounded True Count', are.between(-1*boundary, boundary+1))
    return filteredGameDataEV


def upcardData(gameData):
    upcardEV = gameData.select('Upcard', 'Result').group('Upcard', averageEV)
    upcardEV.append(upcardEV.take(0))
    upcardEV.append(upcardEV.take(9))
    upcardEV.remove(0)
    upcardEV.remove(8)
    return upcardEV


def overalls(gameDataHandTypes):
    return gameDataHandTypes.select('Hand Type', 'Result').group('Hand Type', averageEV)


def createFiltered(gameDataHandTypes, boundary):
    """Returns a filtered table to be passed into createHardColumns or createSoftColumns."""
    gameDataHandTypes = gameDataTCHT(gameDataHandTypes)
    grouped = groupedGDTCHT(gameDataHandTypes)
    filtered = filterGDTCHT(grouped, boundary = boundary)
    return filtered


def createHardColumns(filtered, boundary):
    """Takes a table from createFiltered and returns a table that's passed into generateHardTotalGraphs."""
    hardTotals = GDTCHThardTotals(filtered)
    hardColumns = hardTotalColumns(hardTotals, boundary = boundary)
    return hardColumns


def createSoftColumns(filtered, boundary):
    """Takes a table from createFiltered and returns a table that's passed into generateSoftTotalGraphs."""
    softTotals = GDTCHTsoftTotals(filtered)
    softColumns = softTotalColumns(softTotals, boundary = boundary)
    return softColumns


