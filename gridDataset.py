import os
import constants
import crosswordGrid


class GridDataset:
    # the class contains a dictionary of crosswords
    # the crosswords are divided into three categories: little, medium, big
    # the category describes the size of the crossword

    def __init__(self):
        self.gridDataSet = dict()
        if os.path.getsize(constants.DATASET_PATH) != 0:
            self.gridDataSet = self.loadGridsFromFile(constants.DATASET_PATH)
        else:
            for label, dim in constants.CROSSWORD_GRID_DIMENSION.items():
                gridSet = []
                for counter in range(constants.GRID_COUNTER):
                    grid = crosswordGrid.CrosswordGrid(dim[0], dim[1], False, constants.SHADED_SQUARE_PROBABILITY)
                    gridSet.append(grid)
                self.gridDataSet[label] = gridSet
            self.saveGridDataSetToFile(constants.DATASET_PATH)

    def saveGridDataSetToFile(self, filename):
        if os.path.getsize(filename) == 0:
            with open(filename, 'w') as file:
                for label, grids in self.gridDataSet.items():
                    for grid in grids:
                        for row in grid.grid:
                            file.write(''.join(row) + '\n')
                        file.write('\n')

    def loadGridsFromFile(self, filename):
        with open(filename, 'r') as file:
            content = file.read().strip()

        grids = content.split('\n\n')

        listKeys = []
        for k in constants.CROSSWORD_GRID_DIMENSION.keys():
            for i in range(constants.GRID_COUNTER):
                listKeys.append(k)

        gridsDict = dict()
        for i, grid in enumerate(grids):
            key = listKeys[i]
            if key in gridsDict.keys():
                gridsDict[key].append(crosswordGrid.CrosswordGrid(constants.CROSSWORD_GRID_DIMENSION[key][0],
                                                                  constants.CROSSWORD_GRID_DIMENSION[key][1],
                                                                  grid.strip().split('\n'),
                                                                  constants.SHADED_SQUARE_PROBABILITY))
            else:
                gridsDict[key] = [crosswordGrid.CrosswordGrid(constants.CROSSWORD_GRID_DIMENSION[key][0],
                                                              constants.CROSSWORD_GRID_DIMENSION[key][1],
                                                              grid.strip().split('\n'),
                                                              constants.SHADED_SQUARE_PROBABILITY)]
        return gridsDict
