import numpy as np
import random
import EpidemiologicalModels.DefineSpaceInCA as defSpace
import math
import EpidemiologicalModels.SystemMetrics as metrics
import EpidemiologicalModels.SImodel as SI
import EpidemiologicalModels.StateSpaceConfiguration as StateSpaceConfiguration

class CreateAgesMatrix:
    
    def __init__(self, ranges, system):
        self.ranges = ranges
        self.system = system
        self.nRows, self.nColumns = system.shape

    def __agesDivisions(self, amoungIndividuals):
        agesDivisions = []
        for r in self.ranges:
            agesDivisions.append([0] * math.ceil(r[2] * amoungIndividuals))
        return agesDivisions

    def create(self):
        '''Arreglo de edades aleatorias'''
        amoungIndividuals = metrics.SystemMetrics(self.system, [SI.State.S.value, SI.State.I.value, SI.State.R.value, SI.State.H.value]).numberOfIndividuals() 
        agesDivisions = self.__agesDivisions(amoungIndividuals)
        for divition in range(len(agesDivisions)):
            for individualPerGroup in range(len(agesDivisions[divition])):
                agesDivisions[divition][individualPerGroup] = random.randint(self.ranges[divition][0], self.ranges[divition][1]) 
        concatenatedAgeList = agesDivisions[0]
        for i in range(1, len(agesDivisions)): 
            concatenatedAgeList = concatenatedAgeList + agesDivisions[i]
        matrixOfAges = -np.ones((self.nRows, self.nColumns))
        for r in range(self.nRows):
            for c in range(self.nColumns):
                if self.system[r,c] != SI.State.H.value and self.system[r,c] != SI.State.D.value:
                    randomAge = random.choice(concatenatedAgeList)
                    matrixOfAges[r,c] = randomAge
                elif self.system[r,c] == SI.State.D.value: matrixOfAges[r,c] = 0
        return matrixOfAges
    
class AgeMatrixEvolution:

    def __init__(self, systemAges, birthRate, annualUnit = 365, probabilityOfDyingByAgeGroup = [[0, 100, 1]]):
        self.annualUnit = annualUnit
        self.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
        self.systemAges = systemAges
        self.nRows, self.nColumns = systemAges.shape
        self.birthRate = birthRate # Valor en [0,1)

    def ageGroupPositions(self):
        '''Genera las posiciones de los individuos que tienen entre minAge y maxAge años en el sistema'''
        groupPositions = []
        for r in range(self.nRows):
            for c in range(self.nColumns):
                if self.probabilityOfDyingByAgeGroup[0] < self.systemAges[r][c] and self.systemAges[r][c] < self.probabilityOfDyingByAgeGroup[1]:
                    groupPositions.append([r,c])
        return groupPositions

    def __birthCell(self):
        rate = random.random()
        if rate < self.birthRate: return 1
        else: return 0

    def __birthdaysAndBirths(self, timeUnit):
        newYearMatrix = StateSpaceConfiguration.createSpace(self.systemAges).insideCopy()
        if timeUnit % self.annualUnit == 0:
            for r in range(self.nRows):
                for c in range(self.nColumns):
                    if self.systemAges[r][c] != 0 and self.systemAges[r][c] != -1:
                        newYearMatrix[r][c] = self.systemAges[r][c] + 1
                    elif self.systemAges[r][c] == 0:
                        newYearMatrix[r][c] = self.__birthCell()
        return newYearMatrix

    def evolutionRuleForAges(self, timeUnit):
        agePositions = []
        mortalityApplicationGroups = []
        for probabilityOfDying in self.probabilityOfDyingByAgeGroup:
            ageGroupPosition = self.ageGroupPositions(probabilityOfDying[0], probabilityOfDying[1])
            agePositions.append(ageGroupPosition)
            mortalityApplicationGroups.append(math.ceil(len(ageGroupPosition) * probabilityOfDying[2]) - 1)
        deadPositions = []
        for g in range(len(mortalityApplicationGroups)):
            for age in range(mortalityApplicationGroups[g]):
                numberOfDead = random.randint(0, len(agePositions[g]) - 1)
                deadPositions.append(agePositions[g][numberOfDead])
        newYearMatrix = self.__birthdaysAndBirths(timeUnit)
        for p in range(len(deadPositions)):
            newYearMatrix[deadPositions[p][0]][deadPositions[p][1]] = 0
        return newYearMatrix