import random


class CrosswordGrid:
    # this class represent the grid of the crossword
    # there are blank cell where you can write (we use "_" for them) and blocked cell ("#")

    def __init__(self, rows, columns, grid, shadedSquareProbability):
        self.rows = rows
        self.columns = columns
        self.shadedSquareProbability = shadedSquareProbability
        if not grid:
            self.grid = self.createGrid()
        else:
            self.grid = grid

    def createGrid(self):
        # fill the grid with blank cells and # cells
        # #cells are like the black cells in crosswords where you can't write any letter
        # control the adjacent cells to make sure no isolated blank cells are in the grid

        self.grid = []
        for nRow in range(self.rows):
            row = []
            for column in range(self.columns):
                if random.random() < self.shadedSquareProbability:
                    row.append('#')
                else:
                    row.append('_')
            self.grid.append(row)

        for row in range(self.rows):
            for column in range(self.columns):
                if self.grid[row][column] == '_':
                    blockedCell, positions = self.verifyCell(row, column)
                    if blockedCell == 4:
                        direction = random.choice(positions)
                        self.grid[direction[0]][direction[1]] = '_'

        return self.grid

    def verifyCell(self, row, col):
        # verify if the adjacent cells up, down, left and right of a blank cell are blocked cell and return a list with
        # the indexes of blocked cells

        blockedCells = 0
        positions = []
        if row == 0:
            blockedCells += 1
        elif row > 0 and self.grid[row - 1][col] == '#':
            blockedCells += 1
            positions.append((row - 1, col))

        if row == self.rows - 1:
            blockedCells += 1
        elif row < self.rows - 1 and self.grid[row + 1][col] == '#':
            blockedCells += 1
            positions.append((row + 1, col))

        if col == 0:
            blockedCells += 1
        elif col > 0 and self.grid[row][col - 1] == '#':
            blockedCells += 1
            positions.append((row, col - 1))

        if col == self.columns - 1:
            blockedCells += 1
        elif col < self.columns - 1 and self.grid[row][col + 1] == '#':
            blockedCells += 1
            positions.append((row, col + 1))

        return blockedCells, positions

    def printGrid(self):
        for row in range(self.rows):
            line = []
            for column in range(self.columns):
                line.append(self.grid[row][column])
            print(''.join(line))
        print('')

