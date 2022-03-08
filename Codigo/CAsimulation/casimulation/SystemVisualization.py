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
        print(len(specificIteration))
        plt.imshow(self.__color(self.evolutionsOfCellSpace[specificIteration]), cmap="nipy_spectral", interpolation='nearest')

    def __orderDefinition(self,numberOfElements, numberOfCategories):
        categories = [(i % numberOfElements) * numberOfCategories for i in range(numberOfElements)]
        groups = [[j,i] for i in range(numberOfElements) for j in categories]
        return groups

    def showEvolutions(self, categorizer = 5):
        numberOfEvolutions = len(self.evolutionsOfCellSpace)
        order = self.__orderDefinition(numberOfEvolutions, categorizer)
        for i in range(numberOfEvolutions**2):
            plt.subplot(numberOfEvolutions,numberOfEvolutions,i+1)
            if i in range(numberOfEvolutions):
                plt.title(f"t = {i*5}")
            self.evolutionsPlot(order[i][0])
        plt.show()

    def heatmap(self, state):
        """Mapa de calor para la población infectada (SIR_Model[6])"""
        stateHeatMap = []
        n,m = self.evolutionsOfCellSpace[0].shape
        for iteration in range(len(self.evolutionsOfCellSpace)):
            stateMatrix = np.zeros((n,m))
            for row in range(n):
                for column in range(m):
                    if self.evolutionsOfCellSpace[iteration][row][column] == state:
                        stateMatrix[row][column] = 1
            stateHeatMap.append(stateMatrix)
        average = 1/len(stateHeatMap)*np.sum(stateHeatMap,axis=0)
        sns.heatmap(average, center=0, cmap='viridis',  fmt='.3f')