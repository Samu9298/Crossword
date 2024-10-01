import constants
import crosswordProblem
import test
import gridDataset

# prova totale
"""
wordsList = []
for path in constants.WORDS_PATH:
    wordsList.append(test.buildWordsListFromFile(path))

gridDataset = gridDataset.GridDataset()

cspList = []
for key in gridDataset.gridDataSet.keys():
    for crossword in gridDataset.gridDataSet[key]:
        for wl in wordsList:
            cspList.append(crosswordProblem.CrosswordProblem(crossword.grid, wl))

for csp in cspList:
    result, timeToResult = test.solveCrossword(csp)
    test.print_solution(csp, result, timeToResult)
"""

# prova parziale
wordList = test.buildWordsListFromFile('Files/60000_parole_italiane.txt')

gridDataset = gridDataset.GridDataset()

csp = crosswordProblem.CrosswordProblem(gridDataset.gridDataSet['little'][2].grid, wordList)

result, timeToResult = test.solveCrossword(csp)

test.print_solution(csp, result, timeToResult)
