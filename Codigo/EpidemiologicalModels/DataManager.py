import numpy as np
import EpidemiologicalModels.CellManagement as CellManagement

class SystemMetrics:
    """Metricas que se monitorean por cada modelo:
    statusInTheSystem      => Cantidad de individuos por estado
    numberOfIndividuals    => Cantidad de individuos en el sistema 
    percentagesInTheSystem => Cantidad normalizada de individuos por estado"""
    def __init__(self, cellSpace, states, i = None, j = None):
        self.cellSpace = cellSpace
        self.states = states
        self.i, self.j = i, j # Si el sistema es una vecindad
    
    def statusInTheSystem(self, percentages=True, differentSystem=False, difSystem = None):
        """Lista con las cantidades de individuos por cada estado
        percentages == True  => Valores normalizados
        percentages == False => Valores enteros"""
        if differentSystem == False:
            difSystem = self.cellSpace.system
        globalMetrics = [0]*len(self.states)
        for row in range(self.cellSpace.nRows):
            for column in range(self.cellSpace.nColumns):
                if difSystem[row][column] in self.states:
                    state = self.states.index(difSystem[row][column])
                    globalMetrics[state] += 1
        if self.i != None and self.j != None:
            if difSystem[self.i][self.j] in self.states:
                state = self.states.index(difSystem[self.i][self.j])
                globalMetrics[state] -= 1
        if percentages == False:
            return globalMetrics
        else:
            percentage = []
            for state in globalMetrics:
                percentage.append(state/self.numberOfIndividuals())    
            return percentage
    
    def numberOfIndividuals(self):
        """Cantidad de individuos en el sistema"""
        self.totalIndividuals = sum(self.statusInTheSystem(percentages=False))
        if self.i != None and self.j != None:
            if self.cellSpace[self.i][self.j] in self.states:
                self.totalIndividuals += 1     
        return self.totalIndividuals

def OrderData(data,states):
    """Separa los tipos de datos en 3 grupos: duplas, valores y estados del sistema
    data   => Lista de evoluciones tras aplicar el modelo epidemiológico
    states => Estados que considera el modelo"""
    percentages = []; amountsIndividuals = []
    for state in range(len(states)):
        percentages.append([])
    for iteration in range(len(data)):
        cellSpaceUpdate = data[iteration]
        metrics = SystemMetrics(cellSpaceUpdate,states)
        percentageData = metrics.statusInTheSystem()
        for percentageList in percentages:
            percentageList.append(percentageData[percentages.index(percentageList)])
    for state in range(len(states)):
        amountsIndividuals.append(np.array((range(len(data)),percentages[state])).transpose())
    return [amountsIndividuals,percentages,data]

def _appliedModel(modelFunction, cellSpace, n_iterations, theSystemHasAges = False, systemAges = None):
    """Aplica el modelo 'modelFunction' una cantidad nIterations de veces
    modelFunction => Regla de evolución del modelo
    n_iterations  => Cantidad de veces que va a iterar el modelo
    theSystemHasAges => Se usa para los modelos que tienen en cuenta la edad de los individuos
    systemAges => Edades que se consideran en el sistema (por defecto no existe)"""
    cellSpaceChanges = [cellSpace] 
    if theSystemHasAges == False:
        iteration = 0
        while iteration <= n_iterations:
            iteration += 1
            cellSpaceChanges.append(modelFunction(cellSpaceChanges[iteration-1]))
        return cellSpaceChanges  
    else:
        systemAgesEvolutions = [systemAges]
        iteration = 0       
        while iteration <= n_iterations:                        
            iteration = iteration + 1   
            updateCellSpace = modelFunction(cellSpaceChanges[iteration-1],systemAgesEvolutions[iteration-1],iteration)
            cellSpaceChanges.append(updateCellSpace[0])
            systemAgesEvolutions.append(updateCellSpace[1])
        return cellSpaceChanges    

def _mediumData(dataPerSimulation,states,n_iterations,n_simulations):
    """Organiza la información de cada simulación
    dataPerSimulation => Lista con los datos por estado
    states => Estados que se consideran"""
    percentages = []; amountsIndividuals = []; percentageAmounts = []
    for state in range(len(states)):
        percentages.append([])
    for iteration in range(n_iterations):
        for state in states:
            rate = 0
            for simulation in range(n_simulations):
                rate += dataPerSimulation[states.index(state)][simulation][iteration]/n_simulations
            percentages[states.index(state)].append(rate)
    for percentage in percentages:
        percentageAmounts.append(percentage[1])
    for state in range(len(states)):
        amountsIndividuals.append(np.array((range(n_iterations),percentages[state])).transpose())
    return [amountsIndividuals,percentages]

def _appliedMediumData(modelFunction,cellSpace,initialPercentageInfected,states,n_iterations,n_simulations,theSystemHasAges = False, systemAges = None):
    """Aplica el modelo epidemiológico en n_simulations
    modelFunction => Función basica del modelo epidemiológico
    initialPercentageInfected => Porcentaje de infectados en el momento inicial
    states => Estados que se consideran"""
    mediumStates = []
    for state in states:
            mediumStates.append([])
    if theSystemHasAges:
        for simulation in range(n_simulations):
            infectedCellSpace = CellManagement.CellManagement(cellSpace).InitialCondition(initialPercentageInfected)
            systemEvolution = _appliedModel(modelFunction, infectedCellSpace, n_iterations, True, systemAges)
            evolution = OrderData(systemEvolution, states)[1]
            for state in range(len(states)):
                mediumStates[state].append(evolution[state])
    else:
        for simulation in range(n_simulations):
            infectedCellSpace = CellManagement.CellManagement(cellSpace).InitialCondition(initialPercentageInfected)
            systemEvolution = _appliedModel(modelFunction, infectedCellSpace, n_iterations, False)
            evolution = OrderData(systemEvolution, states)[1]
            for state in range(len(states)):
                mediumStates[state].append(evolution[state])
    return _mediumData(mediumStates,states,n_iterations,n_simulations)

def variationsBetweenScales(scale1,scale2):
    '''Genera una lista con las diferencias entre escalas'''
    variationsArray = np.zeros((len(scale1),2))
    for data in range(len(scale1)):
        variationsArray[data][0] = data
        variationsArray[data][1] = abs(scale1[data]-scale2[data])
    return variationsArray