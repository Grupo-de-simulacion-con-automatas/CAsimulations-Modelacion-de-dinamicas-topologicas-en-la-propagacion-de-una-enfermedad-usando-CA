#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import random
from tools import *

def baseRuleEvolution(alpha,beta,neighborhood,i,j):
    """Regla totalística que describe el cambio entre los estados S e I de manera local"""
    nRows,nColumns = neighborhood.shape  # Conteo de infectados, susceptibles y espacios vacios en la vecindad de ij
    numberOfSusceptible,numberOfInfected,numberOfHoles = systemMetrics(neighborhood,[0,1,-1],i,j).statusInTheSystem(False)
    rho = random.random()
    neighborhoodCopy = insideCopy(neighborhood)
    # La tranformación de un espacio vacio es vacio
    if neighborhood[1][1] != -1 and neighborhood[1][1] != 2 and neighborhood[1][1] != 3:
        if numberOfInfected > 0:
            # Condición para transición al estado S 
            localInfectionRate = (beta/alpha)*(numberOfInfected/((nRows*nColumns-1)-numberOfHoles))
            if numberOfInfected <= numberOfSusceptible and rho >= localInfectionRate: 
                neighborhoodCopy[i][j] = 0  # Pasa al estado S
            else:
                neighborhoodCopy[i][j] = 1  # Pasa al estado I
        else:
            neighborhoodCopy[i][j] = neighborhood[i][j]
    return neighborhoodCopy[i][j]

class sis:
    data = None; evolutions = None
    states = [0,1]
    col = ["y","r"]; eti = ["susceptibles", "infectados"]
    def __init__(self,alpha,beta,system,extraRows,extraColumns,neighborhoodType):
        """Modelo SIS
        alpha => Tasa de recuperación        
        beta  => Tasa de infección
        extraRows    => Cantidad de filas extra del entorno
        extraColumns => Cantidad de columnas extra del entorno
        neighborhoodType => Tipo de vecindad que va a considerar para el análisis"""
        self.alpha = alpha; self.beta = beta 
        self.system = system; self.nRows, self.nColumns = system.shape
        self.neighborhoodType = neighborhoodType; self.extraRows = extraRows; self.extraColumns = extraColumns
    
    def basicRule(self,updateSystem):
        """Aplica la regla base de evolución al sistema updateSystem"""
        extendedSystem = insideCopy(updateSystem,self.extraRows,self.extraColumns)
        numberOfInfected = systemMetrics(updateSystem,[1]).statusInTheSystem(False)[0]
        if numberOfInfected > 0:
            systemUpdate = np.zeros((self.nRows,self.nColumns))
            for i in range(self.nRows):
                for j in range(self.nColumns):
                    vecinityOf_ij, masterCell = identificador(self.neighborhoodType,extendedSystem,i+self.extraRows,j+self.extraColumns)
                    # Aplica la regla base de evolución local y guarda los valores en systemUpdate
                    systemUpdate[i][j] = baseRuleEvolution(self.alpha,self.beta,vecinityOf_ij,masterCell[0][0],masterCell[0][1])
            return systemUpdate
        else: 
            return updateSystem
        
class sir:
    data = None; evolutions = None
    states = [0,1,2]
    col = ["y","r","g"]; eti = ["susceptibles", "infectados", "recuperados"]
    def __init__(self,alpha,beta,system,extraRows,extraColumns,neighborhoodType):
        """Modelo SIR
        alpha => Tasa de recuperación        
        beta  => Tasa de infección
        extraRows    => Cantidad de filas extra del entorno
        extraColumns => Cantidad de columnas extra del entorno
        neighborhoodType => Tipo de vecindad que va a considerar para el análisis"""
        self.alpha = alpha; self.beta = beta
        self.system = system; self.nRows, self.nColumns = system.shape
        self.neighborhoodType = neighborhoodType; self.extraRows = extraRows; self.extraColumns = extraColumns
        
    def __siRule(self,updatedSystem): 
        """Regla S -> I"""
        extendedSystem = insideCopy(updatedSystem,self.extraRows,self.extraColumns)
        systemUpdate = np.zeros((self.nRows,self.nColumns))
        for row in range(self.nRows):
            for column in range(self.nColumns): 
                vecinityOf_ij, masterCell = identificador(self.neighborhoodType,extendedSystem,row+self.extraRows,column+self.extraColumns)
                if updatedSystem[row][column] == 0:
                    # Si el estado de la célula es susceptible aplique la regla base de interaccion local
                    systemUpdate[row][column] = baseRuleEvolution(self.alpha,self.beta,vecinityOf_ij,masterCell[0][0],masterCell[0][1])
                else:
                    systemUpdate[row][column] = updatedSystem[row][column]
        return systemUpdate  
    
    def __irRule(self,previousSystem):      
        """Regla I -> R"""
        infectedCoordinates = stateCoordinates(previousSystem,1)
        # alpha de los infectados se curará
        initialRecoveredNumber = math.ceil(len(infectedCoordinates)*self.alpha)
        percentageInSpace = statePercentageInSpace(initialRecoveredNumber,len(infectedCoordinates)+1,2,1)
        systemCopy = insideCopy(previousSystem)
        for i in range(len(percentageInSpace)):
            # Los individuos que se recuperarón se envian a la posición que tenian en el estado I  
            systemCopy[infectedCoordinates[i][0]][infectedCoordinates[i][1]]=percentageInSpace[i]
        return systemCopy
    
    def basicRule(self,previousSystem):   
        """Aplica la regla de evolución al sistema previousSystem"""
        # Primero se evalua cuales individuos se curarán
        updatedStates_IR = self.__irRule(previousSystem)      
        # Los que no se curarón siguen infectando la población susceptible
        updatedStates_SI = self.__siRule(updatedStates_IR)  
        return updatedStates_SI
    
def agesMatrix(ranges, system):
    '''Arreglo de edades aleatorias'''
    numberOfRows, numberOfColumns = system.shape
    metricas = systemMetrics(system,[0,1,2,3])
    amoungIndividuals = metricas.numberOfIndividuals() # numberOfIndividuals(system)   
    agesDivisions = []
    for Range in ranges:
        agesDivisions.append([0]*math.ceil(Range[2]*amoungIndividuals))
    for divition in range(len(agesDivisions)):
        for individualPerGroup in range(len(agesDivisions[divition])):
            agesDivisions[divition][individualPerGroup] = random.randint(ranges[divition][0],ranges[divition][1]) 
    concatenatedAgeList = agesDivisions[0]
    for i in range(1,len(agesDivisions)):
        concatenatedAgeList = concatenatedAgeList + agesDivisions[i]
    matrixOfAges = -np.ones((numberOfRows,numberOfColumns))
    for row in range(numberOfRows):
        for column in range(numberOfColumns):
            #Si el píxel no es un espacio vacío o un agente muerto se le asigna una edad
            if system[row,column] != -1 and system[row,column] != 3:
                randomAge = random.choice(concatenatedAgeList)
                matrixOfAges[row,column] = randomAge
            elif system[row,column] == 3:
                matrixOfAges[row,column] = 0
    return matrixOfAges

def ageGroupPositions(minAge, maxAge, systemAges):   
    '''Genera las posiciones de los individuos que tienen entre minAge y maxAge años en el sistema'''
    numberOfRows, numberOfColumns = systemAges.shape
    groupPositions = []
    for row in range(numberOfRows):
        for column in range(numberOfColumns):
            if minAge < systemAges[row][column] and systemAges[row][column] < maxAge:
                groupPositions.append([row,column])
    return groupPositions

def newYear(birthRate,probabilityOfDyingByAgeGroup, systemAges, timeUnit, annualUnit):
    '''Nuevo año para los agentes'''
    numberOfRows, numberOfColumns = systemAges.shape
    newYearMatrix = np.zeros((numberOfRows, numberOfColumns))
    for row in range(numberOfRows):
        for column in range(numberOfColumns):
            # Si se cumple la condición, los individuos "cumplirán un año"
            if systemAges[row][column] != 0 and systemAges[row][column] != -1 and timeUnit%annualUnit == 0:   
                newYearMatrix[row][column] = systemAges[row][column] + 1
            # Los individuos muertos tienen una probabilidad birthRate de reaparecer
            elif systemAges[row,column] == 0:
                rate = random.randint(0,100)
                if rate < birthRate:       
                    newYearMatrix[row][column] = 1
            elif systemAges[row,column] == -1:
                newYearMatrix[row,column] = -1
            else:
                newYearMatrix[row,column] = systemAges[row,column]
    agePositions = []
    mortalityApplicationGroups=[]
    for group in range(len(probabilityOfDyingByAgeGroup)):   
        # Se separan los grupos de edades para aplicar las tasas de mortalidad de probabilityOfDyingByAgeGroup
        agePositions.append(ageGroupPositions(probabilityOfDyingByAgeGroup[group][0],probabilityOfDyingByAgeGroup[group][1],systemAges))
        mortalityApplicationGroups.append(math.ceil(len(agePositions[group])*probabilityOfDyingByAgeGroup[group][2])-1)
    deadPositions = []
    for group in range(len(mortalityApplicationGroups)):
        for age in range(mortalityApplicationGroups[group]):
            numberOfDead = random.randint(0, len(agePositions[group]) - 1)
            deadPositions.append(agePositions[group][numberOfDead])
    for position in range(len(deadPositions)):
        newYearMatrix[deadPositions[position][0]][deadPositions[position][1]] = 0
    return newYearMatrix

class birthAndMortavility:
    data = None; evolutions = None
    def __init__(self,model,alpha,beta,birthRate,probabilityOfDyingByAgeGroup,system,systemAges,annualUnit,extraRows,extraColumns,neighborhoodType):
        self.model = model
        self.alpha = alpha; self.beta = beta
        self.birthRate = birthRate; self.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
        self.system = system; self.systemAges = systemAges; self.nRows, self.nColumns = system.shape
        self.annualUnit = annualUnit
        self.neighborhoodType = neighborhoodType; self.extraRows = extraRows; self.extraColumns = extraColumns
        if self.model == "sis":
            self.states = [0,1,3]; self.col = ["y","r","b"]; self.eti = ["susceptibles", "infectados","muertos"]
        elif self.model == "sir":
            self.states = [0,1,2,3]; self.col = ["y","r","g","b"]; self.eti = ["susceptibles","infectados","recuperados","muertos"]
    
    def basicRule(self,previousSystem,previousAgesSystem,timeUnit):
        '''Regla de evolución del modelo SIS con natalidad y mortalidad'''
        newYearMatrix = newYear(self.birthRate,self.probabilityOfDyingByAgeGroup,previousAgesSystem,timeUnit,self.annualUnit)
        if self.model == "sis":
            modelMatrix = sis(self.alpha,self.beta,previousSystem,self.extraRows,self.extraColumns,
                              self.neighborhoodType).basicRule(previousSystem)
        elif self.model == "sir":
            modelMatrix = sir(self.alpha,self.beta,previousSystem,self.extraRows,self.extraColumns,
                              self.neighborhoodType).basicRule(previousSystem)
        modelWithBirthAndMortavilityMatrix = np.zeros((self.nRows,self.nColumns))
        for row in range(self.nRows):
            for column in range(self.nColumns):
                if newYearMatrix[row,column] == 0:   
                    # Si en la evolución de edades, la edad de un agente es 0 el agente se representará como muerto
                    modelWithBirthAndMortavilityMatrix[row,column] = 3
                elif newYearMatrix[row,column] == 1:   
                    # Si en la evolución de edades, la edad de un agente es 1 el agente es susceptible
                    modelWithBirthAndMortavilityMatrix[row,column] = 0
                else:
                    modelWithBirthAndMortavilityMatrix[row,column] = modelMatrix[row,column]
        return [modelWithBirthAndMortavilityMatrix, newYearMatrix]
    
    def basicModel(self,n_iterations,modifiedSystem=False,system=None):
        """Aplica el modelo n_iterations veces"""
        if modifiedSystem == False:
            evolutions = appliedModel(self.basicRule,self.system,n_iterations,True,self.systemAges)
        else:
            evolutions = appliedModel(self.basicRule,system,n_iterations,True,self.systemAges)
        visualization = dataVisualization(evolutions,self.states)
        self.data = visualization[0]; self.evolutions = visualization[2]
        return visualization

    def metricsPlot(self,n_iterations,title="Modelo con natalidad y mortalidad"):
        """Gráfica la evolución de los estados en n_iterations"""
        if self.data == None:
            visualization = self.basicModel(n_iterations)
            self.data = visualization[0]; self.evolutions = visualization[2]    
        graficas(self.data, eti, col, title)

    def evolutionsPlot(self,n_iterations,specificIteration):
        """Gráfica una evolución especifica del conjunto de evoluciones generadas tras aplicar el modelo"""
        if self.evolutions == None:
            visualization = self.basicModel(n_iterations)
            self.data = visualization[0]; self.evolutions = visualization[2]
        plt.imshow(color(self.evolutions[specificIteration]),cmap="nipy_spectral",interpolation='nearest')
    
    def mediumCurves(self,initialPercentageInfected,n_iterations,n_simulations):
        return appliedMediumData(self.basicModel,self.system,initialPercentageInfected,self.states,n_iterations,n_simulations)
    
def deathByDiseaseRule(deathFromDiseaseByAgeRange,system,systemAges):   
    '''Aplica probabilidades de muerte por enfermedad a grupos de edad sobre el sistema'''
    numberOfRows, numberOfColumns = system.shape
    systemAgesCopy = insideCopy(systemAges)
    systemCopy = insideCopy(system)
    infectedIndividualsPerGroup = []
    numberOfInfectedIndividualsDeathPerGroup = []
    deathPositions = []
    for group in range(len(deathFromDiseaseByAgeRange)):
        groupPositions = ageGroupPositions(deathFromDiseaseByAgeRange[group][0],deathFromDiseaseByAgeRange[group][1], systemAgesCopy)
        infectedIndividuals = []
        for individual in range(len(groupPositions)):          
            # Aplica la probabilidad de muerte únicamente a los individuos infectados
            if system[groupPositions[individual][0],groupPositions[individual][1]] == 1:
                infectedIndividuals.append(groupPositions[individual])
        numberOfInfectedIndividualsDeath = math.ceil(len(infectedIndividuals)*deathFromDiseaseByAgeRange[group][2]) - 1
        infectedIndividualsPerGroup.append(infectedIndividuals)
        numberOfInfectedIndividualsDeathPerGroup.append(numberOfInfectedIndividualsDeath)
    for group in range(len(numberOfInfectedIndividualsDeathPerGroup)):
        for infectedIndividual in range(numberOfInfectedIndividualsDeathPerGroup[group]):
            randomIndividual = random.randint(0,len(infectedIndividualsPerGroup[group]) - 1)
            deathPositions.append(infectedIndividualsPerGroup[group][randomIndividual])
    for position in range(len(deathPositions)):
        systemAgesCopy[deathPositions[position][0]][deathPositions[position][1]] = 0
        systemCopy[deathPositions[position][0]][deathPositions[position][1]] = 3
    return [systemCopy, systemAgesCopy]

class deathByDisease(birthAndMortavility):
    data = None; evolutions = None
    def __init__(self,model,alpha,beta,birthRate,probabilityOfDyingByAgeGroup,deathFromDiseaseByAgeRange,system,systemAges,annualUnit,extraRows,extraColumns,neighborhoodType):
        self.model = model
        self.alpha = alpha; self.beta = beta
        self.birthRate = birthRate; self.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
        self.deathFromDiseaseByAgeRange = deathFromDiseaseByAgeRange
        self.system = system; self.nRows, self.nColumns = system.shape
        self.systemAges = systemAges; self.annualUnit = annualUnit
        self.neighborhoodType = neighborhoodType; self.extraRows = extraRows; self.extraColumns = extraColumns 
        if self.model == "sis":
            self.states = [0,1,3]
        elif self.model == "sir":
            self.states = [0,1,2,3]
        
    def basicRule(self,system,systemAges,timeUnit):
        evolution = birthAndMortavility(self.model,self.alpha,self.beta,self.birthRate,self.probabilityOfDyingByAgeGroup,
                                        system,systemAges,self.annualUnit,self.extraRows,self.extraColumns,
                                        self.neighborhoodType).basicRule(system,systemAges,timeUnit)
        systemCopy = insideCopy(evolution[0])
        evolutionsAfterDeaths = deathByDiseaseRule(self.deathFromDiseaseByAgeRange,systemCopy,evolution[1])
        return evolutionsAfterDeaths
    
    def basicModel(self,n_iterations,modifiedSystem=False,system=None):
        """Aplica el modelo n_iterations veces"""
        if modifiedSystem == False:
            evolutions = appliedModel(self.basicRule,self.system,n_iterations,True,self.systemAges)
        else:
            evolutions = appliedModel(self.basicRule,system,n_iterations,True,self.systemAges)
        visualization = dataVisualization(evolutions,self.states)
        self.data = visualization[0]; self.evolutions = visualization[2]
        return visualization

    def metricsPlot(self,n_iterations,title="Modelo con natalidad y mortalidad"):
        """Gráfica la evolución de los estados en n_iterations"""
        if self.data == None:
            visualization = self.basicModel(n_iterations)
            self.data = visualization[0]; self.evolutions = visualization[2]
        if self.model == "sis":
            col = ["y","r","b"]; eti = ["susceptibles", "infectados","muertos"]
        elif self.model == "sir":
            col = ["y","r","g","b"]; eti = ["susceptibles","infectados","recuperados","muertos"]
        graficas(self.data, eti, col, title)

    def evolutionsPlot(self,n_iterations,specificIteration):
        """Gráfica una evolución especifica del conjunto de evoluciones generadas tras aplicar el modelo"""
        if self.evolutions == None:
            visualization = self.basicModel(n_iterations)
            self.data = visualization[0]; self.evolutions = visualization[2]
        plt.imshow(color(self.evolutions[specificIteration]),cmap="nipy_spectral",interpolation='nearest')
    
    def mediumCurves(self,initialPercentageInfected,n_iterations,n_simulations):
        return appliedMediumData(self.basicModel,self.system,initialPercentageInfected,self.states,n_iterations,n_simulations)