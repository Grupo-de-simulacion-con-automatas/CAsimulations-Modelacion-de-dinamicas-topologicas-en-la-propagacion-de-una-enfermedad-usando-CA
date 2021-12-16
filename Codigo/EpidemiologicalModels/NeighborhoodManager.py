import numpy as np
import random

class NeigborhoodManager:
    def __init__(self, cellSpace, impactMatrix):
        self.cellSpace = cellSpace
        self.impactMatrix = impactMatrix
        
    def __Validator(self):
        return self.cellSpace.system.shape == self.impactMatrix.shape
        
    def __ListWithMatrixValues(self):
        '''Lista con los valores de la matriz'''
        values = []
        for r in range(self.cellSpace.nRows):
            for c in range(self.cellSpace.nColumns):
                if self.impactMatrix[r][c] not in values: 
                    values.append(self.impactMatrix[r][c])
        values.sort()
        return values

    def __Impacts(self):
        '''Crea el diccionario que va almacernará los estados de los vecinos por grado de impacto'''
        impactValues = self.__ListWithMatrixValues()
        keys = []; values = []
        for impact in impactValues:
            keys.append(impact); values.append([])
        return dict(zip(keys,values))

    def ImpactNeighborClassifier(self):
        '''Clasifica a los vecinos y sus estados por grado de impacto en un diccionario'''
        if self.__Validator():
            impacts = self.__Impacts()
            for r in range(self.cellSpace.nRows):
                for c in range(self.cellSpace.nColumns):
                    impact = self.impactMatrix[r][c]
                    neighborsByImpact = impacts.get(impact)
                    neighborsByImpact.append([self.cellSpace.system[r,c],[r,c]])
                    impacts.update({impact : neighborsByImpact})
            return impacts
        else:
            print("Las dimensiones del sistema y la matriz de impactos son diferentes.")

# Sistemas de vecindades básicos    

def randomNeighborhoods(cellSpace):        
    '''Sistema de vecindades generado aleatoriamente'''
    neighborhoodSystems = []
    for r in range(cellSpace.nRows):
        for c in range(cellSpace.nColumns):
            base = np.ones(cellSpace.system.shape)
            p = random.random()
            if p <= 0.5:
                base[r][c] = 0
            neighborhoodSystems.append([[r,c],base])
    return neighborhoodSystems

def Von_Neumann(cellSpace):
    '''Sistema de vecindades generado por la vecindad de Von Neumann'''
    neighborhoodSystems = []
    for r in range(cellSpace.nRows):
        for c in range(cellSpace.nColumns):
            base = np.ones(cellSpace.system.shape)
            for i in range(cellSpace.nRows):
                for j in range(cellSpace.nColumns):
                    if abs(r - i) + abs(c - j) <= 1:
                        base[i][j] = 0
            neighborhoodSystems.append([[r,c],base])
    return neighborhoodSystems

def Moore(cellSpace):
    '''Sistema de vecindades generado por la vecindad de Moore'''
    neighborhoodSystems = []
    for r in range(cellSpace.nRows):
        for c in range(cellSpace.nColumns):
            base = np.ones(cellSpace.system.shape)
            for i in range(cellSpace.nRows):
                for j in range(cellSpace.nColumns):
                    if abs(r - i) <= 1 and abs(c - j) <= 1:
                        base[i][j] = 0
            neighborhoodSystems.append([[r,c],base])
    return neighborhoodSystems