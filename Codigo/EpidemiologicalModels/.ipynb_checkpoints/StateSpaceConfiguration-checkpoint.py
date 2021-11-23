import numpy as np
import math
import random
import EpidemiologicalModels.SImodel as SImodel

class createSpace:

    def __init__(self, system = None, nRows = 0, nColumns = 0):
        self.nRows = nRows
        self.nColumns = nColumns
        if nRows != 0 and nColumns != 0:
            self.system = np.zeros((nRows, nColumns))
        else:
            self.system = system

    def insideCopy(self, extraRows = 0, extraColumns = 0):
        """Copia del sistema en un entorno extendido
        extraRows    => Cantidad de filas extra del entorno
        extraColumns => Cantidad de columnas extra del entorno"""
        copy = -np.ones((self.nRows + (extraRows * 2), self.nColumns + (extraColumns * 2)))
        for row in range(self.nRows):
            for column in range(self.nColumns):
                copy[row + extraRows][column+extraColumns] = self.system[row][column]
        return copy

    def stateCoordinates(self, stateIndicator):
        """Enlista los agentes que tengan un estado especifico
        stateIndicator : 0 -> Susceptibles; 1 -> Infectados; 2 -> Recuperados; -1 -> Espacios vacios; 3 -> Fallecidos"""
        coordinates = []
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.system[i,j] == stateIndicator:  
                    coordinates.append([i,j])
        return coordinates

    def statePercentageInSpace(self,a,b,state,spatialState=0):
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

    def initialCondition(self, initialPercentageInfected):
        """Condición inicial aplicada al sistema
        initialPercentageInfected => Porcentage inicial de infectados en el sistema"""
        susceptibleCoordinates = self.stateCoordinates(SImodel.State.S.value)
        initialInfectedNumber = math.ceil(len(susceptibleCoordinates)*initialPercentageInfected)
        # Lista de posiciones de los idividuos que se infectaron y de los que se mantuvieron sanos al aplicar la condicion inicial
        percentageInSpace = self.statePercentageInSpace(initialInfectedNumber,len(susceptibleCoordinates)+1,SImodel.State.I.value)
        systemCopy = self.insideCopy()
        for i in range(len(percentageInSpace)):
            # Los vectores en las posiciones descritas en la lista percentageInSpace adquieren el estado de infección
            systemCopy[susceptibleCoordinates[i][0]][susceptibleCoordinates[i][1]] = percentageInSpace[i]
        return systemCopy

    def initialLocation(self,initialPercentageInfected,position="random",percentageOfInfectedMisplaced=0):
        """ubicación inicial de infectados    
        position : random
                   northwest  north   northeast
                   west       center  east
                   southwest  south   southeast"""
        if position == "random":
            return self.initialCondition(initialPercentageInfected)
        else: 
            # Se divide la zona rectángular en 9 bloques
            a = int(self.nRows/3); b = int(self.nColumns/3)
            system = self.initialCondition(initialPercentageInfected*percentageOfInfectedMisplaced)
            infectedBlock = self.initialCondition(initialPercentageInfected-percentageOfInfectedMisplaced)
            if position == "northwest":
                for i in range(a):
                    for j in range(b):
                        system[i][j] = infectedBlock[i][j]
            elif position == "north":
                for i in range(a):
                    for j in range(b,2*b):
                        system[i][j] = infectedBlock[i][j-b]
            elif position == "northeast":
                for i in range(a):
                    for j in range(2*b,3*b):
                        system[i][j] = infectedBlock[i][j-2*b]
            elif position == "west":
                for i in range(a,a*2):
                    for j in range(b):
                        system[i][j] = infectedBlock[i-a][j]
            elif position == "center":
                for i in range(a,a*2):
                    for j in range(b,2*b):
                        system[i][j] = infectedBlock[i-a][j-b]
            elif position == "east":
                for i in range(a,a*2):
                    for j in range(2*b,3*b):
                        system[i][j]=infectedBlock[i-a][j-2*b]
            elif position == "southwest":
                for i in range(2*a,3*a):
                    for j in range(b):
                        system[i][j] = infectedBlock[i-2*a][j]
            elif position == "south":
                for i in range(2*a,3*a):
                    for j in range(b,2*b):
                        system[i][j] = infectedBlock[i-2*a][j-b]
            elif position == "southeast":
                for i in range(2*a,3*a):
                    for j in range(2*b,3*b):
                        system[i][j] = infectedBlock[i-2*a][j-2*b]
            return system

class boundaryConditions(createSpace):

    def boundaryDefinition(self,boundaryConditions):
        """Definición de la estructura del sistema dadas las condiciones de frontera    
        boundaryConditions : Lista con las posiciones con individuos dentro del sistema"""
        for condition in range(len(boundaryConditions)):
            self.system[boundaryConditions[condition][0],boundaryConditions[condition][1]] = 0  
        return self.system

    def rectangularBoundary(self, rectangleRows, rectangleColumns, rowPosition, columnPosition):
        """Ubica una matriz nula de tamaño rectangleRows*rectangleColumns en la posición a,b del sistema"""
        boundaryConditions = []
        for row in range(rectangleRows):      
            for column in range(rectangleColumns):
                boundaryConditions.append((rowPosition + row,columnPosition + column)) 
        return self.boundaryDefinition(boundaryConditions)