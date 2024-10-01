import constants
import wordVariable
import uuid


class CrosswordProblem:
    # this class represents the constraint problem
    # it contains the list of words to use to solve the problem, the grid, the variables,
    # a dictionary with a list of neighbors for every variable and the domains of the variable

    def __init__(self, grid, words):
        self.crosswordGrid = grid
        self.words = words
        self.overlaps = dict()
        self.variables = self.findVariables()
        self.variablesNeighbors = self.getNeighbors()
        self.domains = self.defineVariableDomain()

    def findVariables(self):
        # it finds all the variable in the grid, both horizontal and vertical variable
        # it uses createVariable to create the variable and puts all of them in self.variable

        variables = []
        for r, row in enumerate(self.crosswordGrid):
            for c, col in enumerate(row):
                if (c == 0 or self.crosswordGrid[r][c - 1] == '#') and (c < len(row) - 1 and
                                                                        self.crosswordGrid[r][c + 1] == '_'):
                    variables.append(self.createVariable(r, c, constants.HORIZONTAL_DIRECTION))
                if ((r == 0 or self.crosswordGrid[r - 1][c] == '#') and
                        (r < len(self.crosswordGrid) - 1 and self.crosswordGrid[r + 1][c] == '_')):
                    variables.append(self.createVariable(r, c, constants.VERTICAL_DIRECTION))

        noBlankVariables = []
        for var in variables:
            if len(var.cellsList) > 1:
                noBlankVariables.append(var)

        return noBlankVariables

    def createVariable(self, row, col, direction):
        # it creates a variable from the starting cell (row, col) in the grid

        variableID = uuid.uuid4()
        cellsList = []
        if direction == constants.HORIZONTAL_DIRECTION:
            while col < len(self.crosswordGrid[row]) and self.crosswordGrid[row][col] == '_':
                cellsList.append((row, col))
                col += 1
            var = wordVariable.WordVariable(constants.HORIZONTAL_DIRECTION, cellsList, variableID)
        elif direction == constants.VERTICAL_DIRECTION:
            while row < len(self.crosswordGrid) and self.crosswordGrid[row][col] == '_':
                cellsList.append((row, col))
                row += 1
            var = wordVariable.WordVariable(constants.VERTICAL_DIRECTION, cellsList, variableID)

        return var

    def defineVariableDomain(self):
        # search in the list of words the words with the same length as the variable and save them
        # the chosen words are saved in a dictionary with key=variable and values=list of words (with same length)

        domains = dict()
        for variable in self.variables:
            domains[variable] = []
            for word in self.words:
                if len(word) == variable.length:
                    if variable in domains.keys():
                        domains[variable].append(word)

        return domains

    def variablesOverlap(self, firstVar, secondVar):
        if (firstVar, secondVar) in self.overlaps.keys():
            return self.overlaps[(firstVar, secondVar)]
        else:
            for i, firstCell in enumerate(firstVar.cellsList):
                for j, secondCell in enumerate(secondVar.cellsList):
                    if firstCell == secondCell:
                        self.overlaps[(firstVar, secondVar)] = (i, j)
                        return self.overlaps[(firstVar, secondVar)]

        self.overlaps[(firstVar, secondVar)] = None
        return self.overlaps[(firstVar, secondVar)]

    def getNeighbors(self):
        # for every variable it finds all its neighbors i.e. all the variables that overlap that variable in a cell
        # it creates a dictionary with key=variable and values=list of the neighbors (of the variable)

        neighbors = dict()
        for var1 in self.variables:
            for var2 in self.variables:
                if var1 != var2 and self.variablesOverlap(var1, var2):
                    if var1 not in neighbors.keys():
                        neighbors[var1] = [var2]
                    else:
                        neighbors[var1].append(var2)

        return neighbors
