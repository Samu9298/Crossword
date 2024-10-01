import os.path
import backtrack
import constants
import time


def buildWordsListFromFile(wordsPath):
    # build a list of words from a file (in this case a .txt file containing some italian words)

    words = []
    with open(wordsPath, "r", encoding="utf-8") as wordsFile:
        for word in wordsFile:
            words.append(word.rstrip())
    return words


def solveCrossword(csp):
    result, timeToResult = backtrack.backtrackingSearch(csp)
    if result:
        return result, timeToResult
    else:
        return False, constants.TIME_FOR_FAILURE


def print_solution(csp, solution, timeToResult):
    if solution is not False:
        gridIntoList = [list(gridList) for gridList in csp.crosswordGrid]
        for var, word in solution.items():
            for i in range(var.length):
                if var.direction == constants.HORIZONTAL_DIRECTION:
                    gridIntoList[var.cellsList[0][0]][var.cellsList[0][1] + i] = word[i]
                elif var.direction == constants.VERTICAL_DIRECTION:
                    gridIntoList[var.cellsList[0][0] + i][var.cellsList[0][1]] = word[i]
        csp.crosswordGrid = [''.join(row) for row in gridIntoList]

        with open(constants.SOLUTIONS_PATH, 'a') as file:
            for row in csp.crosswordGrid:
                file.write(''.join(row) + '\n')
            file.write('\n')

        with open(constants.TIMES_PATH, 'a') as file:
            file.write(str(timeToResult))
            file.write('\n\n')

    else:
        with open(constants.SOLUTIONS_PATH, 'a') as file:
            file.write('No solution found with the words set given')
            file.write('\n\n')

        with open(constants.TIMES_PATH, 'a') as file:
            file.write(str(timeToResult))
            file.write('\n\n')
