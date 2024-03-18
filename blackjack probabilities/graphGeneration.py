import matplotlib.pyplot as plt
import matplotlib.colors as colors
from datascience import *
import numpy as np
from functions import now

# maybe find a way to evaluate handtype automatically
def handLineGraph(columns, handType, boundary = 6):
    if not handType in ['Soft Total', 'Hard Total']:
        raise Exception(f'Invalid hand type {handType}. Valid hand types are: Soft Total, Hard Total')
    
    plt.style.use('bmh')

    fig, ax = plt.subplots()
    plt.ylim(-.8, .9)
    colors = ['lightcoral', 'maroon', 'red', 'darkorange', 
                    'darkgoldenrod', 'gold', 'gray', 'olivedrab', 'chartreuse',
                    'darkgreen', 'turquoise', 'lightseagreen', 'steelblue',
                    'midnightblue', 'mediumpurple', 'violet', 'fuchsia']
    np.random.shuffle(colors)
    ax.set_prop_cycle(color=colors)

    for column in columns.drop('True Counts'):
        line = ax.plot(range(-1*boundary, boundary+1), columns[column], label = column)
    ax.legend(loc='upper center', bbox_to_anchor=(.5, 1.125), fancybox=True, shadow=True, title = handType, ncol = 7 if handType == 'Hard Total' else 5)
    ax.set(xlabel = 'True Count', ylabel = 'Expected Value')

    plt.savefig(f'Graphs\{handType} Line Graph.png')
    

def handHeatmap(columns, handType):
    if not handType in ['Soft Total', 'Hard Total']:
        raise Exception(f'Invalid hand type {handType}. Valid hand types are: Soft Total, Hard Total')
    
    plt.style.use('default')

    data = []
    for row in columns.drop('True Counts').rows:
        data += [list(row)]
    data = np.array(data).transpose()
    
    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(columns.num_rows), labels=[f'{count}' for count in columns.column('True Counts')])
    ax.set_yticks(np.arange(columns.num_columns - 1), labels=columns.drop('True Counts').labels)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    im = ax.imshow(data, cmap = 'viridis', vmin = -.6, vmax = .6)

    for i in range(columns.num_columns - 1):
        for j in range(columns.num_rows):
            text = ax.text(j, i, round(data[i, j], 2),
                           ha="center", va="center", color="w", size = 6)

    fig.colorbar(im, ax=ax, label='Expected Earning')

    plt.xlabel('True Count')
    plt.ylabel(handType)
    plt.title('Expected earnings (bet size of 1)')
    fig.tight_layout()
    plt.savefig(f'Graphs\{handType} Heatmap.png')
    

def generateHardTotalGraphs(hardColumns, boundary):
    handLineGraph(hardColumns, 'Hard Total', boundary = boundary)
    handHeatmap(hardColumns, handType = 'Hard Total')
    

def generateSoftTotalGraphs(softColumns, boundary):
    handLineGraph(softColumns, 'Soft Total', boundary = boundary)
    handHeatmap(softColumns, handType = 'Soft Total')


def handsPlayedTCHeatmap(handsPlayed, boundary = 10):
    """Takes a table generated by simulateHandsPlayedVsTrueCount() and makes of the data."""
    handsPlayed = Table().read_table('hands played to true count.csv')
    handsPlayedRoundedCount = handsPlayed.with_column('Rounded Count', handsPlayed.apply(round, 'True Count'))
    handsPlayedRoundedCount = handsPlayedRoundedCount.where('Rounded Count', are.between(-1*boundary, boundary + 1))
    
    plt.style.use('default')

    data = [[0 for i in range(2 * boundary + 1)] for i in range(50)]
    for row in handsPlayedRoundedCount.rows:
        try:
            data[row[1]-1][row[3]+boundary] += 1
        except:
            print(row[1]-1, row[3]+boundary)
        
    data = np.array(data).transpose()
    
    fig, ax = plt.subplots()
    ax.set_yticks(np.arange(2 * boundary + 1), labels=[f'{count-boundary if count%2==0 else ""}' for count in np.arange(2 * boundary + 1)])
    ax.set_xticks(np.arange(50), labels=[f'{handsPlayed if handsPlayed%5==0 else ""}' for handsPlayed in np.arange(50)])
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")
    im = ax.imshow(data, cmap = 'viridis', norm = colors.LogNorm())
    ax.set(xlabel = 'Hands Played', ylabel = 'True Count')
        
    fig.colorbar(im, ax=ax, label='Count')
    fig.tight_layout()
    plt.savefig(r'Graphs\true count frequency heatmap.png')
    

def trueCountEVBar(trueCountData):
    fig, ax = plt.subplots()

    trueCounts = [str(int(i)) for i in trueCountData.column('Rounded True Count')]
    EVs = trueCountData.column('Result averageEV')

    ax.bar(trueCounts, EVs)

    ax.set_ylabel('Expected earning')
    ax.set_xlabel('True count')
    
    plt.savefig(r'Graphs\true count EV bar.png')
    

def trueCountFreqBar(trueCountData):
    fig, ax = plt.subplots()

    trueCounts = [str(int(i)) for i in trueCountData.column('Rounded True Count')]
    counts = trueCountData.column('Count')

    ax.bar(trueCounts, counts)

    ax.set_ylabel('Frequency')
    ax.set_xlabel('True count')

    plt.savefig(r'Graphs\true count frequency bar.png')
    

def upcardEVBar(upcardData):
    fig, ax = plt.subplots()

    upcards = upcardData.column('Upcard')
    upcardEVs = upcardData.column('Result averageEV')

    ax.bar(upcards, upcardEVs)

    ax.set_ylabel('Expected earning')
    ax.set_xlabel('Upcard')
    
    plt.savefig(r'Graphs\Upcard EV Bar.png')
    

def hardTotalEV(overalls):
    hardOveralls = overalls.take(range(17))
    hardOveralls = hardOveralls.with_column('Integer Totals', [int(i) for i in hardOveralls.column('Hand Type')])
    hardOveralls = hardOveralls.sort('Integer Totals')

    hardHandTypes = hardOveralls.column('Hand Type')
    hardHandTypeEVs = hardOveralls.column('Result averageEV')

    fig, ax = plt.subplots()

    ax.bar(hardHandTypes, hardHandTypeEVs)

    ax.set_ylabel('Expected Earning')
    ax.set_xlabel('Hard Total')
    
    plt.savefig(r'Graphs\Hard Total EV.png')
    

def softTotalEV(overalls):
    softOveralls = overalls.take(range(17, 27))
    softOveralls.append(softOveralls.take(1)).remove(1)

    softHandTypes = softOveralls.column('Hand Type')
    softHandTypeEVs = softOveralls.column('Result averageEV')

    fig, ax = plt.subplots()

    ax.bar(softHandTypes, softHandTypeEVs)

    ax.set_ylabel('Expected Earning')
    ax.set_xlabel('Soft Total')
    
    plt.savefig(r'Graphs\Soft Total EV.png')


from tableReformatFuncs import *

def generateAll(gameData, boundary):
    """Takes game data as an input and runs every graph generation function"""
    print(f'--- Beginning Graph Generation ---')
    print(f'Upcard bar chart | {(beginning := now())}')
    upcardEVBar(upcardData(gameData))
    
    print(f'Rounded TC table | {now()}')
    gameDataRoundedTC = addRoundedTC(gameData)
    gameData = None
    
    print(f'True count table generation | {now()}')
    trueCountTable = trueCountData(gameDataRoundedTC, boundary = boundary)
    print(f'True count EV bar | {now()}')
    trueCountEVBar(trueCountTable)
    print(f'True count frequency bar | {now()}')
    trueCountFreqBar(trueCountTable)
    trueCountTable = None
    
    print(f'Hand type table generation | {now()}')
    gameDataHandTypes = addHandTypes(gameDataRoundedTC)
    gameDataRoundedTC = None
    
    print(f'Bar graph table generation | {now()}')
    overallHandTypeData = overalls(gameDataHandTypes)
    print(f'Hard total EV bar graph | {now()}')
    hardTotalEV(overallHandTypeData)
    print(f'Soft total EV bar graph | {now()}')
    softTotalEV(overallHandTypeData)
    overallHandTypeData = None
    
    print(f'Line graphs/heatmap table generation | {now()}')
    filtered = createFiltered(gameDataHandTypes, boundary = boundary)
    print(f'Hard total table generation | {now()}')
    hardColumns = createHardColumns(filtered, boundary = boundary)
    print(f'Soft total table generation | {now()}')
    softColumns = createSoftColumns(filtered, boundary = boundary)
    print(f'Hard total graph generation | {now()}')
    generateHardTotalGraphs(hardColumns, boundary = boundary)
    print(f'Soft total graph generation | {now()}')
    generateSoftTotalGraphs(softColumns, boundary = boundary)
    
    print('Finished!')
    print(f'Begun at {beginning}, finished at {now()}')