import CAsimulation.CellManagement as CellManagement
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class SystemVisualization:

    def __init__(self, evolutionsOfCellSpace):
        self.evolutionsOfCellSpace = evolutionsOfCellSpace

    def __color(self,cellSpace):                 
        """Transformación que permite visualizar el sistema a color"""
        cellSpaceCopy = CellManagement.CellManagement(cellSpace).InsideCopy()
        for i in range(cellSpace.nRows):
            for j in range(cellSpace.nColumns):
                if cellSpaceCopy.system[i][j] == 0:    
                    cellSpaceCopy.system[i][j] = 190  # Susceptibles => Amarillo
                if cellSpaceCopy.system[i][j] == 1:    
                    cellSpaceCopy.system[i][j] = 240  # Infectados => Rojo
                if cellSpaceCopy.system[i][j] == 2:    
                    cellSpaceCopy.system[i][j] = 115  # Recuperados => Verde
                if cellSpaceCopy.system[i][j] == -1:   
                    cellSpaceCopy.system[i][j] = 0    # Vacíos => Negro
                if cellSpaceCopy.system[i][j] == 3:
                    cellSpaceCopy.system[i][j] = 256  # Muertos => Gris
        increasedSystem = CellManagement.CellManagement(cellSpaceCopy).InsideCopy(1,1)
        increasedSystem.system[0][0] = 0
        increasedSystem.system[cellSpace.nRows + 1][cellSpace.nColumns + 1] = 256  
        return increasedSystem.system

    def evolutionsPlot(self,specificIteration):
        """Gráfica una evolución especifica del conjunto de evoluciones generadas tras aplicar el modelo"""
        plt.imshow(self.__color(self.evolutionsOfCellSpace[specificIteration]), cmap="nipy_spectral", interpolation='nearest')

    def heatmap(self, state):
        """Mapa de calor dado un estado"""
        stateHeatMap = []
        for iteration in range(len(self.evolutionsOfCellSpace)):
            stateMatrix = np.zeros((self.evolutionsOfCellSpace[0].nRows,self.evolutionsOfCellSpace[0].nColumns))
            for row in range(self.evolutionsOfCellSpace[0].nRows):
                for column in range(self.evolutionsOfCellSpace[0].nColumns):
                    if self.evolutionsOfCellSpace[iteration].system[row][column] == state:
                        stateMatrix[row][column] = 1
            stateHeatMap.append(stateMatrix)
        average = 1/len(stateHeatMap)*np.sum(stateHeatMap,axis=0)
        sns.heatmap(average, center=0, cmap='viridis',  fmt='.3f')