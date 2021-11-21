# import random
# import math
import numpy as np
import EpidemiologicalModels.SImodel as SI
# import EpidemiologicalModels.SystemMetrics as metrics
import EpidemiologicalModels.SimpleModels as SModels
import EpidemiologicalModels.AgeManagement as AgeManagement

# def agesMatrix(ranges, system):
#     '''Arreglo de edades aleatorias'''
#     amoungIndividuals = metrics.SystemMetrics(system, [SI.State.S.value, SI.State.I.value, SI.State.R.value, SI.State.H.value]).numberOfIndividuals() 
#     agesDivisions = AgesDivisions(ranges, amoungIndividuals)
#     for divition in range(len(agesDivisions)):
#         for individualPerGroup in range(len(agesDivisions[divition])):
#             agesDivisions[divition][individualPerGroup] = random.randint(ranges[divition][0], ranges[divition][1]) 
#     concatenatedAgeList = agesDivisions[0]
#     for i in range(1, len(agesDivisions)): 
#         concatenatedAgeList = concatenatedAgeList + agesDivisions[i]
#     numberOfRows, numberOfColumns = system.shape    
#     matrixOfAges = -np.ones((numberOfRows, numberOfColumns))
#     for row in range(numberOfRows):
#         for column in range(numberOfColumns):
#             if system[row,column] != SI.State.H.value and system[row,column] != SI.State.D.value:
#                 randomAge = random.choice(concatenatedAgeList)
#                 matrixOfAges[row,column] = randomAge
#             elif system[row,column] == SI.State.D.value: matrixOfAges[row,column] = 0
#     return matrixOfAges

# def AgesDivisions(ranges, amoungIndividuals):
#     agesDivisions = []
#     for Range in ranges:
#         agesDivisions.append([0] * math.ceil(Range[2] * amoungIndividuals))
#     return agesDivisions

# def ageGroupPositions(minAge, maxAge, systemAges):   
#     '''Genera las posiciones de los individuos que tienen entre minAge y maxAge años en el sistema'''
#     groupPositions = []
#     numberOfRows, numberOfColumns = systemAges.shape
#     for row in range(numberOfRows):
#         for column in range(numberOfColumns):
#             if minAge < systemAges[row][column] and systemAges[row][column] < maxAge:
#                 groupPositions.append([row,column])
#     return groupPositions

# def newYear(birthRate, probabilityOfDyingByAgeGroup, systemAges, timeUnit, annualUnit):
#     '''Nuevo año para los agentes'''
#     agePositions = []
#     mortalityApplicationGroups = []
#     deadPositions = []
#     numberOfRows, numberOfColumns = systemAges.shape
#     newYearMatrix = np.zeros((numberOfRows, numberOfColumns))
#     for row in range(numberOfRows):
#         for column in range(numberOfColumns):
#             if systemAges[row][column] != 0 and systemAges[row][column] != -1 and timeUnit%annualUnit == 0: newYearMatrix[row][column] = systemAges[row][column] + 1
#             elif systemAges[row,column] == 0:
#                 rate = random.randint(0,100)
#                 if rate < birthRate: newYearMatrix[row][column] = 1
#             elif systemAges[row,column] == -1: newYearMatrix[row,column] = -1
#             else: newYearMatrix[row,column] = systemAges[row,column]
#     for group in range(len(probabilityOfDyingByAgeGroup)):   
#         agePositions.append(ageGroupPositions(probabilityOfDyingByAgeGroup[group][0], probabilityOfDyingByAgeGroup[group][1], systemAges))
#         mortalityApplicationGroups.append(math.ceil(len(agePositions[group]) * probabilityOfDyingByAgeGroup[group][2]) - 1)
#     for group in range(len(mortalityApplicationGroups)):
#         for age in range(mortalityApplicationGroups[group]):
#             numberOfDead = random.randint(0, len(agePositions[group]) - 1)
#             deadPositions.append(agePositions[group][numberOfDead])
#     for position in range(len(deadPositions)):
#         newYearMatrix[deadPositions[position][0]][deadPositions[position][1]] = 0
#     return newYearMatrix

class birthAndMortavility:
    
    data = None
    evolutions = None

    def __init__(self, model, alpha, beta, birthRate, probabilityOfDyingByAgeGroup, system, systemAges, annualUnit, neighborhoodSystems, impactRates):
        self.model = model
        self.alpha = alpha; self.beta = beta
        self.birthRate = birthRate
        self.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
        self.system = system; self.systemAges = systemAges
        self.nRows, self.nColumns = system.shape
        self.annualUnit = annualUnit
        self.neighborhoodSystems = neighborhoodSystems
        if self.model == "sis" or self.model == "SIS":
            self.states = [SI.State.S.value, SI.State.I.value, SI.State.D.value]
            self.colors = ["y", "r", "b"]
            self.labels = ["Susceptibles", "Infectados", "Espacios disponibles"]
        elif self.model == "sir" or self.model == "SIR":
            self.states = [SI.State.S.value, SI.State.I.value, SI.State.R.value, SI.State.D.value]
            self.colors = ["y", "r", "g", "b"]
            self.labels = ["Susceptibles", "Infectados", "Recuperados","Espacios disponibles"]
        self.impactRates = impactRates
    
    def basicRule(self,previousSystem,previousAgesSystem,timeUnit):
        '''Regla de evolución del modelo con natalidad y mortalidad'''
        modelWithBirthAndMortavilityMatrix = np.zeros((self.nRows,self.nColumns))
        # newYearMatrix = newYear(self.birthRate,self.probabilityOfDyingByAgeGroup,
        #                         previousAgesSystem,timeUnit,self.annualUnit)
        newYearMatrix = AgeManagement.AgeMatrixEvolution(previousAgesSystem, self.birthRate, self.annualUnit, self.probabilityOfDyingByAgeGroup).evolutionRuleForAges(timeUnit)
        if self.model == "sis":
            modelMatrix = SModels.SISmodel(self.alpha, self.beta, previousSystem, self.neighborhoodSystems, self.impactRates).basicRule(previousSystem)
        elif self.model == "sir":
            modelMatrix = SModels.SIRmodel(self.alpha, self.beta, previousSystem, self.neighborhoodSystems, self.impactRates).basicRule(previousSystem)
        for row in range(self.nRows):
            for column in range(self.nColumns):
                if newYearMatrix[row,column] == 0: modelWithBirthAndMortavilityMatrix[row,column] = SI.State.D.value
                elif newYearMatrix[row,column] == 1: modelWithBirthAndMortavilityMatrix[row,column] = SI.State.S.value
                else: modelWithBirthAndMortavilityMatrix[row,column] = modelMatrix[row,column]
        return [modelWithBirthAndMortavilityMatrix, newYearMatrix]