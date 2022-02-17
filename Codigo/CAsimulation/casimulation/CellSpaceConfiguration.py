import numpy as np
import CAsimulation.CellManagement as CellManagement

class CellSpaceConfiguration:

    def __init__(self, nRows, nColumns, xnRows = -1, xnColumns = -1, unRows = 0, unColumns = 0):
        self.__nRows = nRows; self.__nColumns = nColumns  # Dimensiones de la región interna inicial
        self.__xnRows = xnRows; self.__xnColumns = xnColumns  # Ubicación de la región interna inicial
        self.__unRows = unRows; self.__unColumns = unColumns  # Dimensiones del área externa
        self.nRows = max(self.__nRows, self.__xnRows)
        self.nColumns = max(self.__nColumns, self.__xnColumns)
        self.__createInternalSpace()

    def __validate(self):
        if self.__nRows < 0:
            print("Debe definir un número de filas mayor a cero.")
            return False
        elif self.__nColumns < 0:
            print("Debe definir un número de columnas mayor a cero.")
            return False
        else:
            return True

    def basicParameters(self):
        """Parámetros con los que se definió el sistema inicialmente."""
        return (self.__nRows, self.__nColumns, self.__xnRows, self.__xnColumns, self.__unRows, self.__unColumns)

    # Forma del espacio de células

    def __createInternalSpace(self):
        if self.__validate():
            if self.__xnRows == -1 or self.__nColumns == -1:
                self.system = np.zeros((self.__nRows, self.__nColumns))
            else:
                self.system = -np.ones((self.__xnRows, self.__xnColumns))
                self.system = self.rectangularBoundary(self.__nRows, self.__nColumns, self.__unRows, self.__unColumns)

    def __boundaryDefinition(self, boundaryConditions):
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
        return self.__boundaryDefinition(boundaryConditions)

    # Condición inicial para aplicar el modelo epidemiológico

    def initialLocationOfInfected(self, initialPercentageInfected, position = "random", percentageOfInfectedMisplaced = 0): 
        """ubicación inicial de infectados
        position : random
                   northwest  north   northeast
                   west       center  east
                   southwest  south   southeast"""
        if position == "random":
            return CellManagement.CellManagement(self).InitialCondition(initialPercentageInfected)
        else: 
            # Se divide la zona rectángular en 9 bloques
            a = int(self.nRows/3); b = int(self.nColumns/3)
            system = CellManagement.CellManagement(self).InitialCondition(initialPercentageInfected*percentageOfInfectedMisplaced).system
            infectedBlock = CellManagement.CellManagement(CellSpaceConfiguration(a,b)).InitialCondition(initialPercentageInfected-percentageOfInfectedMisplaced,).system
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