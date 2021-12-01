import numpy as np
import random
import math
import EpidemiologicalModels.Models as Models
import EpidemiologicalModels.CellSpaceConfiguration as CellSpaceConfiguration

class CellManagement:
    
    def __init__(self, cellSpace):
        self.cellSpace = cellSpace

    def InsideCopy(self, extraRows = 0, extraColumns = 0):
        """Copia del sistema en un entorno extendido
        extraRows    => Cantidad de filas extra del entorno
        extraColumns => Cantidad de columnas extra del entorno"""
        copy = -np.ones((self.cellSpace.nRows + (extraRows * 2), self.cellSpace.nColumns + (extraColumns * 2)))
        for row in range(self.cellSpace.nRows):
            for column in range(self.cellSpace.nColumns):
                copy[row + extraRows][column+extraColumns] = self.cellSpace.system[row][column]
        nRows, nColumns, unRows, unColumns, xnRows, xnColumns = self.cellSpace.basicParameters()
        cellSpaceCopy = CellSpaceConfiguration.CellSpaceConfiguration(nRows, nColumns, unRows, unColumns, xnRows, xnColumns)
        cellSpaceCopy.system = copy
        return cellSpaceCopy

    def StateCoordinates(self, stateIndicator):
        """Enlista los agentes que tengan un estado especifico
        stateIndicator : 0 -> Susceptibles; 1 -> Infectados; 2 -> Recuperados; -1 -> Espacios vacios; 3 -> Fallecidos"""
        coordinates = []
        for i in range(self.cellSpace.nRows):
            for j in range(self.cellSpace.nColumns):
                if self.cellSpace.system[i,j] == stateIndicator:  
                    coordinates.append([i,j])
        return coordinates

    def StatePercentageInSpace(self,a,b,state,spatialState=0):
        """Porcentaje de individuos con el estado en el espacio (a de cada b tienen el estado)
        a,b => Porcentage visto como fracción
        state => Estado que van a adquirir los individuos
        spatialState => Estado que se considera como base para el cambio al estado state"""
        percentageInSpace = []
        space = spatialState*np.ones((1,b)) 
        for j in range(a):
            i = random.randint(1,b-1) 
            space[0][i] = state
        for m in range(1,b):
            percentageInSpace.append(int(space[0][m]))  
        return percentageInSpace

    def InitialCondition(self, initialPercentageInfected):
        """Condición inicial aplicada al sistema
        initialPercentageInfected => Porcentage inicial de infectados en el sistema"""
        susceptibleCoordinates = self.StateCoordinates(Models.State.S.value)
        initialInfectedNumber = math.ceil(len(susceptibleCoordinates)*initialPercentageInfected)
        # Lista de posiciones de los idividuos que se infectaron y de los que se mantuvieron sanos al aplicar la condicion inicial
        percentageInSpace = self.StatePercentageInSpace(initialInfectedNumber,len(susceptibleCoordinates)+1,Models.State.I.value)
        cellSpaceCopy = self.InsideCopy()
        for i in range(len(percentageInSpace)):
            # Los vectores en las posiciones descritas en la lista percentageInSpace adquieren el estado de infección
            cellSpaceCopy.system[susceptibleCoordinates[i][0]][susceptibleCoordinates[i][1]] = percentageInSpace[i]
        return cellSpaceCopy