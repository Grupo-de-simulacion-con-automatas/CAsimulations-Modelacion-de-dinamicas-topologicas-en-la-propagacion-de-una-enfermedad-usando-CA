import EpidemiologicalModels.StateSpaceConfiguration as StateSpaceConfiguration
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class SystemVisualization:

    def __init__(self, evolutionsOfSystem):
        self.evolutionsOfSystem = evolutionsOfSystem

    def __color(system):                 
        """Transformación que permite visualizar el sistema a color"""
        nRows, mColumns = system.shape
        systemCopy = StateSpaceConfiguration.createSpace(system).insideCopy()
        for i in range(nRows):
            for j in range(mColumns):
                if systemCopy[i][j] == 0:    
                    systemCopy[i][j] = 190  # Susceptibles => Amarillo
                if systemCopy[i][j] == 1:    
                    systemCopy[i][j] = 240  # Infectados => Rojo
                if systemCopy[i][j] == 2:    
                    systemCopy[i][j] = 115  # Recuperados => Verde
                if systemCopy[i][j] == -1:   
                    systemCopy[i][j] = 0    # Vacíos => Negro
                if systemCopy[i][j] == 3:
                    systemCopy[i][j] = 256  # Muertos => Gris
        increasedSystem = StateSpaceConfiguration.createSpace(system).insideCopy(1,1)
        increasedSystem[0][0] = 0; increasedSystem[nRows+1][mColumns+1] = 256  
        return increasedSystem

    def evolutionsPlot(self,specificIteration):
        """Gráfica una evolución especifica del conjunto de evoluciones generadas tras aplicar el modelo"""
        plt.imshow(self.__color(self.evolutionsOfSystem[specificIteration]), cmap="nipy_spectral", interpolation='nearest')

    def __orderDefinition(numberOfElements, numberOfCategories):
        categories = [(i % numberOfElements) * numberOfCategories for i in range(numberOfElements)]
        groups = [[j,i] for i in range(numberOfElements) for j in categories]
        return groups

    def showEvolutions(self, categorizer = 5):
        numberOfEvolutions = len(self.evolutionsOfSystem)
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
        n,m = self.evolutionsOfSystem[0].shape
        for iteration in range(len(self.evolutionsOfSystem)):
            stateMatrix = np.zeros((n,m))
            for row in range(n):
                for column in range(m):
                    if self.evolutionsOfSystem[iteration][row][column] == state:
                        stateMatrix[row][column] = 1
            stateHeatMap.append(stateMatrix)
        average = 1/len(stateHeatMap)*np.sum(stateHeatMap,axis=0)
        sns.heatmap(average, center=0, cmap='viridis',  fmt='.3f')