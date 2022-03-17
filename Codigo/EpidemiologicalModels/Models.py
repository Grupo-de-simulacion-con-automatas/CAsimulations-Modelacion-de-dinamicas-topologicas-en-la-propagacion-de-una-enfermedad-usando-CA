import enum
import random
import math
from typing_extensions import Annotated
import EpidemiologicalModels.NeighborhoodManager as NeighborhoodManager
import EpidemiologicalModels.CellManagement as CellManagement
import numpy as np
import EpidemiologicalModels.AgeManagement as AgeManagement
import EpidemiologicalModels.DataManager as DataManager
import EpidemiologicalModels.PlotsManager as PlotsManager
import EpidemiologicalModels.SystemVisualization as SystemVisualization

class State(enum.Enum):
    H = -1  # Huecos
    S = 0   # Susceptibles
    I = 1   # Infectados
    R = 2   # Recuperados
    D = 3   # Espacio vacío que se puede ocupar por una nueva célula

class SImodel:
    
    def __init__(self, alpha, beta, cellSpace, neighborhoodSystems = [], impactRates = []):
        """Modelo SI
        alpha => Tasa de recuperación
        beta  => Tasa de infección
        system => Espacio de celulas
        neighborhoodSystems => Lista con las matrices que describen los sistemas de vecindades en el sistema
        """
        self.alpha = alpha
        self.beta = beta 
        self.cellSpace = cellSpace
        self.neighborhoodSystems = neighborhoodSystems
        self.impactRates = impactRates

    def __validate(self):
        if self.alpha <= 0:
            print("Debe definir una tasa de recuperación alpha > 0.")
            return False
        if self.beta <= 0:
            print("Debe definir una tasa de infección beta > 0.")
            return False
        if self.cellSpace is CellManagement.CellSpaceConfiguration.CellSpaceConfiguration:
            print("Asegurese de pasar un sistema con el tipo <class 'EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration'>")
            return False
        if len(self.neighborhoodSystems) == 0:
            print("Debe definir un sistema de vecindades.")
            return False
        if len(self.impactRates) == 0:
            print("Debe definir las tasas de impacto.")
            return False
        else:
            return True
    
    def __CountNeighborsByState(self, neighbors):
        """Cantidad de individuos por estado"""
        numberOfSByImpact = 0; numberOfIByImpact = 0; numberOfRByImpact = 0; numberOfDByImpact = 0; numberOfH = 0
        for n in neighbors:
            if n[0] == State.S.value: numberOfSByImpact += 1
            elif n[0] == State.I.value: numberOfIByImpact += 1
            elif n[0] == State.R.value: numberOfRByImpact += 1
            elif n[0] == State.D.value: numberOfDByImpact += 1
            elif n[0] == State.H.value: numberOfH += 1
        amountOfCells = numberOfSByImpact + numberOfIByImpact + numberOfRByImpact + numberOfDByImpact + numberOfH
        return (numberOfSByImpact, numberOfIByImpact, amountOfCells, numberOfH)

    def __SI_rule(self, cellState, neighborsByImpact): # Grados de impacto 0 y 1
        """Regla totalística que describe el cambio entre los estados S e I de manera local"""
        impactRanges = list(neighborsByImpact.keys())
        numberOfS = 0; numberOfI = 0; numberOfH = 0
        numberOfCells = 0
        for ir in impactRanges:
            neighbors = neighborsByImpact.get(ir)
            numberOfSByImpact, numberOfIByImpact, amountOfCells, amountOfHoles = self.__CountNeighborsByState(neighbors)
            numberOfS += numberOfSByImpact * self.impactRates[impactRanges.index(ir)]
            numberOfI += numberOfIByImpact * self.impactRates[impactRanges.index(ir)]
            numberOfH += amountOfHoles * self.impactRates[impactRanges.index(ir)]
            numberOfCells += amountOfCells * self.impactRates[impactRanges.index(ir)]
        rho = random.random()
        if numberOfI > 0:
            localInfectionRate = (self.beta / self.alpha) * (numberOfI / ((numberOfCells - 1) - numberOfH))
            if cellState == State.S.value:
                if numberOfI <= numberOfS and rho >= localInfectionRate: return State.S.value
                else: return State.I.value
            else: return cellState
        else: return cellState
        
    def Apply(self): 
        """Regla S -> I"""
        if self.__validate():
            systemUpdate = CellManagement.CellManagement(self.cellSpace).InsideCopy()
            for ns in self.neighborhoodSystems:
                neighborsByImpact = NeighborhoodManager.NeigborhoodManager(self.cellSpace, ns[1]).ImpactNeighborClassifier()
                if systemUpdate.system[ns[0][0]][ns[0][1]] not in [State.H.value, State.R.value, State.D.value]:
                    systemUpdate.system[ns[0][0]][ns[0][1]] = self.__SI_rule(self.cellSpace.system[ns[0][0]][ns[0][1]], neighborsByImpact)   
            return systemUpdate  

class SISmodel(SImodel):

    states = [State.S.value, State.I.value]
    colors = ["y", "r"]
    labels = ["Susceptibles", "Infectados"]
    
    def __siRule(self, updatedCellSpace, impactRates): 
        """Regla S -> I"""
        return SImodel(self.alpha, self.beta, updatedCellSpace, self.neighborhoodSystems, impactRates).Apply()  
    
    def __isRule(self, previousCellSpace):
        """Regla I -> S"""
        PreviousCellSpace = CellManagement.CellManagement(previousCellSpace)
        infectedCoordinates = PreviousCellSpace.StateCoordinates(State.I.value)
        initialRecoveredNumber = math.ceil(len(infectedCoordinates) * self.alpha)
        percentageInSpace = PreviousCellSpace.StatePercentageInSpace(initialRecoveredNumber, len(infectedCoordinates) + 1, State.S.value, State.I.value)
        cellSpaceCopy = PreviousCellSpace.InsideCopy()
        for i in range(len(percentageInSpace)):
            cellSpaceCopy.system[infectedCoordinates[i][0]][infectedCoordinates[i][1]] = percentageInSpace[i]
        return cellSpaceCopy
    
    def basicRule(self, previousCellSpace):   
        """Aplica la regla de evolución al sistema previousSystem"""
        updatedStates_IS = self.__isRule(previousCellSpace)
        updatedStates_SI = self.__siRule(updatedStates_IS, self.impactRates)        
        return updatedStates_SI

class SIRmodel(SImodel):

    states = [State.S.value, State.I.value, State.R.value]
    colors = ["y", "r", "g"]
    labels = ["Susceptibles", "Infectados", "Recuperados"]
        
    def __siRule(self, updatedCellSpace, impactRates): 
        """Regla S -> I"""
        return SImodel(self.alpha, self.beta, updatedCellSpace, self.neighborhoodSystems, impactRates).Apply()
    
    def __irRule(self,previousCellSpace):      
        """Regla I -> R"""
        PreviousSystem = CellManagement.CellManagement(previousCellSpace)
        infectedCoordinates = PreviousSystem.StateCoordinates(State.I.value)
        initialRecoveredNumber = math.ceil(len(infectedCoordinates) * self.alpha)
        percentageInSpace = PreviousSystem.StatePercentageInSpace(initialRecoveredNumber, len(infectedCoordinates) + 1, State.R.value, State.I.value)
        cellSpaceCopy = PreviousSystem.InsideCopy()

        for i in range(len(percentageInSpace)):
            cellSpaceCopy.system[infectedCoordinates[i][0]][infectedCoordinates[i][1]] = percentageInSpace[i]
        return cellSpaceCopy
    
    def basicRule(self,previousSystem):   
        """Aplica la regla de evolución al sistema previousSystem"""
        updatedStates_IR = self.__irRule(previousSystem) 
        updatedStates_SI = self.__siRule(updatedStates_IR, self.impactRates)   
        return updatedStates_SI

class birthAndMortavility:

    probabilityOfDyingByAgeGroup = []
    neighborhoodSystems = []
    impactRates = []
    systemAges = np.array(())

    def __init__(self, model, alpha, beta, birthRate, probabilityOfDyingByAgeGroup, annualUnit, cellSpace, neighborhoodSystems, impactRates, systemAges):
        self.model = model.lower()
        self.alpha = alpha
        self.beta = beta
        self.birthRate = birthRate
        self.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
        self.annualUnit = annualUnit
        self.cellSpace = cellSpace
        self.neighborhoodSystems = neighborhoodSystems
        self.impactRates = impactRates
        self.systemAges = systemAges
        self.__modelVariables()

    def __validate(self):
        if self.model != "sis" and self.model != "sir":
            print("Introduzca un modelo valido. (SIS o SIR)")
            return False
        elif self.birthRate <= 0:
            print("Defina una tasa de natalidad mayor a cero.")
            return False
        elif len(self.probabilityOfDyingByAgeGroup) == 0:
            print("Establezca las probabilidades de muerte por rango.")
            return False
        elif self.annualUnit <= 0:
            print("Defina una unidad anual mayor a cero.")
            return False
        elif str(type(self.cellSpace)) != "<class 'EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration'>":
            print("Asegurese de pasar un sistema con el tipo <class 'EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration'>")
            return False
        elif len(self.neighborhoodSystems) == 0:
            print("Defina un sistema de vecindades.")
            return False
        elif len(self.impactRates) == 0:
            print("Defina las tasas de impacto.")
            return False
        elif self.systemAges.shape[0] == 0:
            print("Defina una matriz de edades.")
            return False
        else:
            return True

    def __modelVariables(self):
        if self.model == "sis":
            self.states = [State.S.value, State.I.value, State.D.value]
            self.colors = ["y", "r", "b"]
            self.labels = ["Susceptibles", "Infectados", "Espacios disponibles"]
        elif self.model == "sir":
            self.states = [State.S.value, State.I.value, State.R.value, State.D.value]
            self.colors = ["y", "r", "g", "b"]
            self.labels = ["Susceptibles", "Infectados", "Recuperados", "Espacios disponibles"]
    
    def basicRule(self,previousCellSpace,previousAgesSystem,timeUnit):
        '''Regla de evolución del modelo con natalidad y mortalidad'''
        if self.__validate():
            modelWithBirthAndMortavilityCellSpace = CellManagement.CellManagement(self.cellSpace).InsideCopy()
            newYearMatrix = AgeManagement.AgeMatrixEvolution(previousAgesSystem, self.birthRate, self.annualUnit, self.probabilityOfDyingByAgeGroup).evolutionRuleForAges(timeUnit)
            if self.model == "sis":
                modelCellSpace = SISmodel(self.alpha, self.beta, previousCellSpace, self.neighborhoodSystems, self.impactRates).basicRule(previousCellSpace)
            elif self.model == "sir":
                modelCellSpace = SIRmodel(self.alpha, self.beta, previousCellSpace, self.neighborhoodSystems, self.impactRates).basicRule(previousCellSpace)
            for row in range(self.cellSpace.nRows):
                for column in range(self.cellSpace.nColumns):
                    if newYearMatrix[row,column] == 0: modelWithBirthAndMortavilityCellSpace.system[row,column] = State.D.value
                    elif newYearMatrix[row,column] == 1: modelWithBirthAndMortavilityCellSpace.system[row,column] = State.S.value
                    else: modelWithBirthAndMortavilityCellSpace.system[row][column] = modelCellSpace.system[row][column]
            return [modelWithBirthAndMortavilityCellSpace, newYearMatrix]

class deathByDisease:

    deathFromDiseaseByAgeRange = []

    def __init__(self, model, alpha, beta, birthRate, probabilityOfDyingByAgeGroup, deathFromDiseaseByAgeRange, annualUnit, cellSpace, neighborhoodSystems, impactRates, systemAges):
        self.model = model.lower()
        self.alpha = alpha
        self.beta = beta
        self.birthRate = birthRate
        self.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
        self.deathFromDiseaseByAgeRange = deathFromDiseaseByAgeRange
        self.annualUnit = annualUnit
        self.cellSpace = cellSpace
        self.neighborhoodSystems = neighborhoodSystems
        self.impactRates = impactRates
        self.systemAges = systemAges
        self.__modelVariables()

    def __modelVariables(self):
        if self.model == "sis":
            self.states = [State.S.value, State.I.value, State.D.value]
            self.colors = ["y", "r", "b"]
            self.labels = ["Susceptibles", "Infectados", "Espacios disponibles"]
        elif self.model == "sir":
            self.states = [State.S.value, State.I.value, State.R.value, State.D.value]
            self.colors = ["y", "r", "g", "b"]
            self.labels = ["Susceptibles", "Infectados", "Recuperados", "Espacios disponibles"]

    def __validate(self):
        if len(self.deathFromDiseaseByAgeRange) == 0:
            print("Defina las probabilidades de muerte por enfermedad.")
            return False
        else:
            return True
        
    def basicRule(self,cellSpace,systemAges,timeUnit):
        if self.__validate():
            evolution = birthAndMortavility(self.model, self.alpha, self.beta, self.birthRate, self.probabilityOfDyingByAgeGroup, self.annualUnit,
                                            cellSpace, self.neighborhoodSystems, self.impactRates, systemAges).basicRule(cellSpace,systemAges,timeUnit)
            cellSpaceCopy = CellManagement.CellManagement(evolution[0]).InsideCopy()
            evolutionsAfterDeaths = AgeManagement.AgeMatrixEvolution(evolution[1],0).deathByDiseaseRule(cellSpaceCopy, self.deathFromDiseaseByAgeRange)
            return evolutionsAfterDeaths

class applyEpidemiologicalModel:
    # En las variables data y evolutions se almacenaran los datos luego de aplicar los modelos
    data = None  # Reporte numperico de los cambios en cada estado
    mediumData = None  # Reporte numperico promedio de los cambios en cada estado
    evolutions = None  # Reporte visual de los cambios del sistema   
    # Datos tomados por defecto
    modelHasAges = False
    systemAges = None  # Edades de los individuos en el sistema
    annualUnit = None  # Unidad de ciclo temporal (año)
    birthRate = None  # Tasa de natalidad 
    probabilityOfDyingByAgeGroup = None  # Tasa de mortalidad por grupo de edad
    modelHasDeathByDisease = False  
    deathFromDiseaseByAgeRange = None  # Tasa de mortalidad causada por la enfermedad por grupo de edad
    
    def __init__(self, model, alpha, beta, cellSpace, neighborhoodSystems, impactRates = [1,0]):
        """Modelos soportados: sis, sir, sis_bm, sir_bm, sis_dd, sir_dd"""
        self.model = model.lower()  # Modelo epidemiológico que se va a aplicar
        self.alpha = alpha; self.beta = beta  # Datos básicos de la enfermedad
        self.cellSpace = cellSpace  # Sistema sobre el que se va a aplicar el modelo
        self.neighborhoodSystems = neighborhoodSystems  # Tipo de vecindad que va a considerar para el análisis
        self.impactRates = impactRates
        self.title = f"Modelo {self.model.upper()}"
        
    def __validate(self):
        if self.model not in ("sis", "sir", "sis_bm", "sir_bm", "sis_dd", "sir_dd"):
            print("Asegurese de ingresar un modelo valido. (sis, sir, sis_bm, sir_bm, sis_dd, sir_dd)")
            return False
        else:
            return True

    def __evalConditions(self):
        # Definición de las herramientas para aplicar los modelos
        if self.model == "sis":
            self.epidemiologicalModel = SISmodel(self.alpha,self.beta,self.cellSpace,self.neighborhoodSystems, self.impactRates)
        elif self.model == "sir":
            self.epidemiologicalModel = SIRmodel(self.alpha,self.beta,self.cellSpace,self.neighborhoodSystems, self.impactRates)
        else:
            self.modelHasAges = True
            if self.model == "sis_bm":
                self.epidemiologicalModel = birthAndMortavility("sis", self.alpha, self.beta, self.birthRate, self.probabilityOfDyingByAgeGroup, self.annualUnit,
                                                                        self.cellSpace, self.neighborhoodSystems, self.impactRates, self.systemAges)
            if self.model == "sir_bm":
                self.epidemiologicalModel = birthAndMortavility("sir", self.alpha, self.beta, self.birthRate, self.probabilityOfDyingByAgeGroup, self.annualUnit,
                                                                        self.cellSpace, self.neighborhoodSystems, self.impactRates, self.systemAges)
            if self.model == "sis_dd":
                self.epidemiologicalModel = deathByDisease("sis", self.alpha, self.beta, self.birthRate, self.probabilityOfDyingByAgeGroup, 
                                                                    self.deathFromDiseaseByAgeRange, self.annualUnit, self.cellSpace, 
                                                                    self.neighborhoodSystems, self.impactRates, self.systemAges)
            if self.model == "sir_dd":
                self.epidemiologicalModel = deathByDisease("sir", self.alpha, self.beta, self.birthRate, self.probabilityOfDyingByAgeGroup, 
                                                                    self.deathFromDiseaseByAgeRange, self.annualUnit, self.cellSpace, 
                                                                    self.neighborhoodSystems, self.impactRates, self.systemAges)

    def basicModel(self, n_iterations, modifiedSystem = False, system = None):
        """Aplica el modelo n_iterations veces"""
        if self.__validate():
            self.__evalConditions()
            if modifiedSystem == False:
                evolutions = DataManager._appliedModel(self.epidemiologicalModel.basicRule, self.cellSpace, n_iterations, self.modelHasAges, self.systemAges)
            else:
                evolutions = DataManager._appliedModel(self.epidemiologicalModel.basicRule, system, n_iterations, self.modelHasAges, self.systemAges)
            visualization = DataManager.OrderData(evolutions, self.epidemiologicalModel.states)
            self.data = visualization[0]
            self.evolutions = visualization[2]

    def plotCurvesModel(self, title = "", limit = False):
        if title == "":
            PlotsManager.plotSolutions(self.data, self.epidemiologicalModel.labels, self.epidemiologicalModel.colors, self.title, limit)
        else:
            PlotsManager.plotSolutions(self.data, self.epidemiologicalModel.labels, self.epidemiologicalModel.colors, title, limit)

    def plotSpecificIteration(self, iteration):
        if iteration <= len(self.evolutions) - 1:
            SystemVisualization.SystemVisualization(self.evolutions).evolutionsPlot(iteration)
        else:
            print(f"La iteración no es valida. Debe ser menor o igual a {len(self.evolutions)-1}")

class applyEpidemiologicalModel_nIterations:
    # En las variables data y evolutions se almacenaran los datos luego de aplicar los modelos
    data = None  # Reporte numperico de los cambios en cada estado
    mediumData = None  # Reporte numperico promedio de los cambios en cada estado
    evolutions = None  # Reporte visual de los cambios del sistema   
    # Datos tomados por defecto
    modelHasAges = False
    systemAges = None  # Edades de los individuos en el sistema
    annualUnit = None  # Unidad de ciclo temporal (año)
    birthRate = None  # Tasa de natalidad 
    probabilityOfDyingByAgeGroup = None  # Tasa de mortalidad por grupo de edad
    modelHasDeathByDisease = False  
    deathFromDiseaseByAgeRange = None  # Tasa de mortalidad causada por la enfermedad por grupo de edad

    def __init__(self, model, alpha, beta, cellSpace, neighborhoodSystems, impactRates = [1,0], nSimulations = 1, initialPercentageInfected = 0):
        """Modelos soportados: sis, sir, sis_bm, sir_bm, sis_dd, sir_dd"""
        self.model = model.lower()  # Modelo epidemiológico que se va a aplicar
        self.alpha = alpha; self.beta = beta  # Datos básicos de la enfermedad
        self.cellSpace = cellSpace  # Sistema sobre el que se va a aplicar el modelo
        self.neighborhoodSystems = neighborhoodSystems  # Tipo de vecindad que va a considerar para el análisis
        self.impactRates = impactRates
        self.title = f"Modelo {self.model.upper()}"
        self.nSimulations = nSimulations
        self.initialPercentageInfected = initialPercentageInfected

    def __validate(self):
        if self.model not in ("sis", "sir", "sis_bm", "sir_bm", "sis_dd", "sir_dd"):
            print("Asegurese de ingresar un modelo valido. (sis, sir, sis_bm, sir_bm, sis_dd, sir_dd)")
            return False
        elif self.nSimulations == 1:
            print("Debe generar más de una simulación.")
            return False
        elif self.initialPercentageInfected < 0:
            print("Debe establecer un porcentage de infectados inicial para cada simulación.")
            return False
        else:
            return True

    def __evalConditions(self):
        # Definición de las herramientas para aplicar los modelos
        if self.model == "sis":
            self.epidemiologicalModel = SISmodel(self.alpha,self.beta,self.cellSpace,self.neighborhoodSystems, self.impactRates)
        elif self.model == "sir":
            self.epidemiologicalModel = SIRmodel(self.alpha,self.beta,self.cellSpace,self.neighborhoodSystems, self.impactRates)
        else:
            self.modelHasAges = True
            if self.model == "sis_bm":
                self.epidemiologicalModel = birthAndMortavility("sis", self.alpha, self.beta, self.birthRate, self.probabilityOfDyingByAgeGroup, self.annualUnit,
                                                                        self.cellSpace, self.neighborhoodSystems, self.impactRates, self.systemAges)
            if self.model == "sir_bm":
                self.epidemiologicalModel = birthAndMortavility("sir", self.alpha, self.beta, self.birthRate, self.probabilityOfDyingByAgeGroup, self.annualUnit,
                                                                        self.cellSpace, self.neighborhoodSystems, self.impactRates, self.systemAges)
            if self.model == "sis_dd":
                self.epidemiologicalModel = deathByDisease("sis", self.alpha, self.beta, self.birthRate, self.probabilityOfDyingByAgeGroup, 
                                                                    self.deathFromDiseaseByAgeRange, self.annualUnit, self.cellSpace, 
                                                                    self.neighborhoodSystems, self.impactRates, self.systemAges)
            if self.model == "sir_dd":
                self.epidemiologicalModel = deathByDisease("sir", self.alpha, self.beta, self.birthRate, self.probabilityOfDyingByAgeGroup, 
                                                                    self.deathFromDiseaseByAgeRange, self.annualUnit, self.cellSpace, 
                                                                    self.neighborhoodSystems, self.impactRates, self.systemAges)

    def basicModel(self, n_iterations):
        """Aplica el modelo n_iterations veces"""
        if self.__validate():
            self.__evalConditions()
            if self.model == "sis" or self.model == "sir":
                evolutions = DataManager._appliedMediumData(self.epidemiologicalModel.basicRule, self.cellSpace, self.initialPercentageInfected, 
                                                           self.epidemiologicalModel.states, n_iterations, self.nSimulations)
            else:
                evolutions = DataManager._appliedMediumData(self.epidemiologicalModel.basicRule, self.cellSpace, self.initialPercentageInfected, 
                                                           self.epidemiologicalModel.states, n_iterations, self.nSimulations, True, self.systemAges)
            self.data = evolutions[0]

    def plotCurvesModel(self, title = "", limit = False):
        if title == "":
            PlotsManager.plotSolutions(self.data, self.epidemiologicalModel.labels, self.epidemiologicalModel.colors, self.title, limit)
        else:
            PlotsManager.plotSolutions(self.data, self.epidemiologicalModel.labels, self.epidemiologicalModel.colors, title, limit)