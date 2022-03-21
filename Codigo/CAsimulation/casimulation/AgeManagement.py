from typing import Type
import numpy as np
import random
import math
import CAsimulation.Models as Models
import CAsimulation.CellManagement as CellManagement
import CAsimulation.DataManager as DataManager
import CAsimulation.CellSpaceConfiguration as CellSpaceConfiguration

class AgesMatrix:
    
    ranges = []

    def __init__(self, ranges, cellSpace):
        self.ranges = ranges
        self.cellSpace = cellSpace
        self.agesMatrix = self.__create()

    def __validate(self):
        if len(self.ranges) == 0:
            print("Debe definir los rangos de edades en el sistema.")
            return False
        if str(type(self.cellSpace)) != "<class 'CAsimulation.CellSpaceConfiguration.CellSpaceConfiguration'>":
            print("Asegurese de pasar un sistema con el tipo CellSpaceConfiguration.CellSpaceConfiguration.")
            return False
        else:
            for r in self.ranges:
                if len(r) != 3:
                    print("Asegurese de que todos los rangos de edad posean límite inferior, límite superior y la proporción en el sistema.")
                    return False
                elif r[2] > 1:
                    print("Asegurese de que todas las proporciones sean menores o iguales a 1.")
                    return False
                else:
                    return True

    def __agesDivisions(self, amoungIndividuals):
        agesDivisions = []
        for r in self.ranges:
            agesDivisions.append([0] * math.ceil(r[2] * amoungIndividuals))
        return agesDivisions

    def __create(self):
        '''Arreglo de edades aleatorias'''
        if self.__validate():
            amoungIndividuals = DataManager.SystemMetrics(self.cellSpace, [Models.State.S.value, Models.State.I.value, Models.State.R.value, Models.State.H.value]).numberOfIndividuals() 
            agesDivisions = self.__agesDivisions(amoungIndividuals)
            for divition in range(len(agesDivisions)):
                for individualPerGroup in range(len(agesDivisions[divition])):
                    agesDivisions[divition][individualPerGroup] = random.randint(self.ranges[divition][0], self.ranges[divition][1]) 
            concatenatedAgeList = agesDivisions[0]
            for i in range(1, len(agesDivisions)): 
                concatenatedAgeList = concatenatedAgeList + agesDivisions[i]
            matrixOfAges = -np.ones((self.cellSpace.nRows, self.cellSpace.nColumns))
            for r in range(self.cellSpace.nRows):
                for c in range(self.cellSpace.nColumns):
                    if self.cellSpace.system[r,c] != Models.State.H.value and self.cellSpace.system[r,c] != Models.State.D.value:
                        randomAge = random.choice(concatenatedAgeList)
                        matrixOfAges[r,c] = randomAge
                    elif self.cellSpace.system[r,c] == Models.State.D.value: matrixOfAges[r,c] = 0
            return matrixOfAges
    
class AgeMatrixEvolution:

    def __init__(self, systemAges, birthRate, annualUnit = 365, probabilityOfDyingByAgeGroup = [[0, 100, 1]]):
        self.birthRate = birthRate # Valor en [0,1)
        self.systemAges = systemAges
        self.nRows, self.nColumns = systemAges.shape
        self.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
        self.annualUnit = annualUnit

    def ageGroupPositions(self, inferiorLimit, superiorLimit):
        '''Genera las posiciones de los individuos que tienen entre minAge y maxAge años en el sistema'''
        groupPositions = []
        for r in range(self.nRows):
            for c in range(self.nColumns):
                if inferiorLimit < self.systemAges[r][c] and self.systemAges[r][c] < superiorLimit:
                    groupPositions.append([r,c])
        return groupPositions

    def __birthCell(self):
        rate = random.random()
        if rate < self.birthRate: return 1
        else: return 0

    def __birthdaysAndBirths(self, timeUnit):
        agesMatrix = CellSpaceConfiguration.CellSpaceConfiguration(self.nRows, self.nColumns)
        newYearMatrix = CellManagement.CellManagement(agesMatrix).InsideCopy().system
        if timeUnit % self.annualUnit == 0:
            for r in range(self.nRows):
                for c in range(self.nColumns):
                    if self.systemAges[r][c] != 0 and self.systemAges[r][c] != -1:
                        newYearMatrix[r][c] = self.systemAges[r][c] + 1
                    elif self.systemAges[r][c] == 0:
                        newYearMatrix[r][c] = self.__birthCell()
        else:
            for r in range(self.nRows):
                for c in range(self.nColumns):
                    newYearMatrix[r][c] = self.systemAges[r][c]
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

    def deathByDiseaseRule(self,cellSpace,deathFromDiseaseByAgeRange):   
        '''Aplica probabilidades de muerte por enfermedad a grupos de edad sobre el sistema'''
        deathPositions = []
        infectedIndividualsPerGroup = []
        numberOfInfectedIndividualsDeathPerGroup = []
        systemCopy = CellManagement.CellManagement(cellSpace).InsideCopy()
        for group in range(len(deathFromDiseaseByAgeRange)):
            groupPositions = self.ageGroupPositions(deathFromDiseaseByAgeRange[group][0], deathFromDiseaseByAgeRange[group][1])
            infectedIndividuals = []
            for individual in range(len(groupPositions)):     
                if cellSpace.system[groupPositions[individual][0],groupPositions[individual][1]] == Models.State.I.value:
                    infectedIndividuals.append(groupPositions[individual])
            numberOfInfectedIndividualsDeath = math.ceil(len(infectedIndividuals) * deathFromDiseaseByAgeRange[group][2]) - 1
            infectedIndividualsPerGroup.append(infectedIndividuals)
            numberOfInfectedIndividualsDeathPerGroup.append(numberOfInfectedIndividualsDeath)
        for group in range(len(numberOfInfectedIndividualsDeathPerGroup)):
            for infectedIndividual in range(numberOfInfectedIndividualsDeathPerGroup[group]):
                randomIndividual = random.randint(0,len(infectedIndividualsPerGroup[group]) - 1)
                deathPositions.append(infectedIndividualsPerGroup[group][randomIndividual])
        for position in range(len(deathPositions)):
            self.systemAges[deathPositions[position][0]][deathPositions[position][1]] = 0
            systemCopy.system[deathPositions[position][0]][deathPositions[position][1]] = 3
        return [systemCopy, self.systemAges]