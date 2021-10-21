import numpy as np

class NeigborhoodManager:
    def __init__(self, system, impactMatrix):
        self.system = system
        self.impactMatrix = impactMatrix
        
    def __Validator(self):
        return self.system.shape == self.impactMatrix.shape
        
    def __ListWithMatrixValues(self):
        '''Lista con los valores de la matriz'''
        values = []
        nrow, ncolumn = self.system.shape
        for r in range(nrow):
            for c in range(ncolumn):
                if self.impactMatrix[r][c] not in values: 
                    values.append(self.impactMatrix[r][c])
        values.sort()
        return values

    def __Impacts(self):
        '''Crea el diccionario que va almacernará los estados de los vecinos por grado de impacto'''
        nrows, ncolumns = self.impactMatrix.shape
        impactValues = self.__ListWithMatrixValues()
        keys = []; values = []
        for impact in impactValues:
            keys.append(impact); values.append([])
        return dict(zip(keys,values))

    def ImpactNeighborClassifier(self):
        '''Clasifica a los vecinos y sus estados por grado de impacto en un diccionario'''
        if self.__Validator():
            impacts = self.__Impacts()
            nrows, ncolumns = self.system.shape
            for r in range(nrows):
                for c in range(ncolumns):
                    impact = self.impactMatrix[r][c]
                    neighborsByImpact = impacts.get(impact)
                    neighborsByImpact.append([self.system[r,c],[r,c]])
                    impacts.update({impact : neighborsByImpact})
            return impacts
        else:
            print("Las dimensiones del sistema y la matriz de impactos son diferentes.")

# Sistemas de vecindades usuales            
            
def Von_Neumann(system):
    '''Sistema de vecindades generado por la vecindad de Von Neumann'''
    neighborhoodSystems = []
    nrows, ncolumns = system.shape
    for r in range(nrows):
        for c in range(ncolumns):
            base = np.ones(system.shape)
            for i in range(nrows):
                for j in range(ncolumns):
                    if abs(r - i) + abs(c - j) <= 1:
                        base[i][j] = 0
            neighborhoodSystems.append([[r,c],base])
    return neighborhoodSystems

def Moore(system):
    '''Sistema de vecindades generado por la vecindad de Moore'''
    neighborhoodSystems = []
    nrows, ncolumns = system.shape
    for r in range(nrows):
        for c in range(ncolumns):
            base = np.ones(system.shape)
            for i in range(nrows):
                for j in range(ncolumns):
                    if abs(r - i) <= 1 and abs(c - j) <= 1:
                        base[i][j] = 0
            neighborhoodSystems.append([[r,c],base])
    return neighborhoodSystems