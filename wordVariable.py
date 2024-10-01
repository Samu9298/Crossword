class WordVariable:
    def __init__(self, direction, cellsList, variableID):
        # it represents a variable of the crossword problem
        # cellsList is a list of the grid cells of the variable

        self.ID = variableID
        self.direction = direction
        self.cellsList = cellsList
        self.length = len(self.cellsList)

    def __str__(self):
        return str(self.cellsList[0]) + str(self.direction)
