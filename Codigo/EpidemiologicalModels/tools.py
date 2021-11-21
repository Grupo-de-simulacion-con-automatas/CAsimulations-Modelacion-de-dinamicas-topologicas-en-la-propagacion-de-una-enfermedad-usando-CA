#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from EpidemiologicalModels.DefineSpaceInCA import *
import matplotlib.pyplot as plt
import EpidemiologicalModels.StateSpaceConfiguration as StateSpaceConfiguration

def spline3(A):     #spline cubico para la lista de coordenadas A
    n = len(A); l = [1]; B = [0] ; g = [0]; gn = 0; C = [0]*n
    alpha = []; spline = []; a = []; h = []; x = []; y = []*(n-1)
    for i in range(n):
        a.append(A[i][1])
    for i in range(n-1):
        xh = A[i+1][0]-A[i][0]; h.append(xh)
    for i in range(1, n-1):
        xa = (3/h[i])*(a[i+1]-a[i])-(3/h[i-1])*(a[i]-a[i-1]); alpha.append(xa)
    for i in range(1, n-1):
        xl = 2*(A[i+1][0]-A[i-1][0])-h[i-1]*B[i-1]; l.append(xl)
        xb = h[i]/l[i]; B.append(xb)
        xg = (alpha[i-1]-h[i-1]*g[i-1])/l[i]; g.append(xg)
    l.append(1); g.append(0)
    for i in range(n-1):
        j = (n-1)-(i+1)
        xC = g[j]-B[j]*C[j+1]; C[j] = xC
        xy = ((a[j+1]-a[j])/h[j])-(h[j]/3)*(C[j+1]+2*C[j]); y.append(xy)
        xx = (C[j+1]-C[j])/(3*h[j]); x.append(xx)
    for i in range(n-1):
        j=(n-1)-(i+1)
        S3 = [a[i],y[j],C[i],x[j]]; spline.append(S3)
    return np.array(spline)

def graficas(variables, etiquetas, colores, title, limit=True):
    if len(etiquetas) != len(variables):
        print("La cantidad de etiquetas debe ser igual a la cantidad de variables")
    elif len(colores) != len(variables):
        print("La cantidad de colores debe ser igual a la cantidad de variables")
    else:
        for j in range(len(variables)):
            funcion = []; cond = []; x = []; y = []
            A = variables[j]
            SP = spline3(A)
            for i in range(len(spline3(A))):
                xa = np.linspace(A[i,0],A[i+1,0] - 0.0001,11); x = np.concatenate((x,xa))
                ya = SP[i,0] + SP[i,1]*(xa-A[i,0]) + SP[i,2]*(xa-A[i,0])**2 + SP[i,3]*(xa-A[i,0])**3
                y = np.concatenate((y,ya))
            plt.plot(x,y,c = colores[j],label = etiquetas[j])
    if limit == True:
        plt.plot(x, x**0, 'k--')
        plt.ylim(0,1.05)
    plt.title(title)
    plt.xlabel("Time")
    plt.legend(loc=0)
    plt.show()

# Identificación de los estados
# 0 --> Susceptible; 1 --> Infectado; 2 --> Recuperados; -1 --> Espacios vacios

class systemMetrics:
    """Metricas que se monitorean por cada modelo:
    statusInTheSystem      => Cantidad de individuos por estado
    numberOfIndividuals    => Cantidad de individuos en el sistema 
    percentagesInTheSystem => Cantidad normalizada de individuos por estado"""
    def __init__(self,system,states,i=None, j=None):
        self.system = system; self.states = states
        self.nRows,self.nColums = system.shape
        self.i, self.j = i, j # Si el sistema es una vecindad
    
    def statusInTheSystem(self, percentages=True):
        """Lista con las cantidades de individuos por cada estado
        percentages == True  => Valores normalizados
        percentages == False => Valores enteros"""
        globalMetrics = [0]*len(self.states)
        for row in range(self.nRows):
            for column in range(self.nColums):
                if self.system[row][column] in self.states:
                    state = self.states.index(self.system[row][column])
                    globalMetrics[state] += 1
        if self.i != None and self.j != None:
            if self.system[self.i][self.j] in self.states:
                state = self.states.index(self.system[self.i][self.j])
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
            if self.system[self.i][self.j] in self.states:
                self.totalIndividuals += 1     
        return self.totalIndividuals

def dataVisualization(data,states):
    """Separa los tipos de datos en 3 grupos: duplas, valores y estados del sistema
    data   => Lista de evoluciones tras aplicar el modelo epidemiológico
    states => Estados que considera el modelo"""
    percentages = []; amountsIndividuals = []
    for state in range(len(states)):
        percentages.append([])
    for iteration in range(len(data)):
        systemUpdate = data[iteration]
        metrics = systemMetrics(systemUpdate,states)
        percentageData = metrics.statusInTheSystem()
        for percentageList in percentages:
            percentageList.append(percentageData[percentages.index(percentageList)])
    for state in range(len(states)):
        amountsIndividuals.append(np.array((range(len(data)),percentages[state])).transpose())
    return [amountsIndividuals,percentages,data]

def appliedModel(modelFunction,system,n_iterations,theSystemHasAges=False,systemAges=None):
    """Aplica el modelo 'modelFunction' una cantidad nIterations de veces
    modelFunction => Regla de evolución del modelo
    n_iterations  => Cantidad de veces que va a iterar el modelo
    theSystemHasAges => Se usa para los modelos que tienen en cuenta la edad de los individuos
    systemAges => Edades que se consideran en el sistema (por defecto no existe)"""
    systemChanges = [system] 
    if theSystemHasAges == False:
        iteration = 0
        while iteration <= n_iterations:
            iteration += 1
            systemChanges.append(modelFunction(systemChanges[iteration-1]))
        return systemChanges  
    else:
        systemAgesEvolutions = [systemAges]
        iteration = 0       
        while iteration <= n_iterations:                        
            iteration = iteration + 1   
            updateSystem = modelFunction(systemChanges[iteration-1],systemAgesEvolutions[iteration-1],iteration)
            systemChanges.append(updateSystem[0])
            systemAgesEvolutions.append(updateSystem[1])
        return systemChanges    
    
def mediumData(dataPerSimulation,states,n_iterations,n_simulations):
    """Organiza la información de cada simulación
    dataPerSimulation => Lista con los datos por estado
    states => Estados que se consideran"""
    percentages = []; amountsIndividuals = []
    for state in range(len(states)):
        percentages.append([])
    for iteration in range(n_iterations):
        for state in states:
            rate = 0
            for simulation in range(n_simulations):
                rate += dataPerSimulation[states.index(state)][simulation][iteration]/n_simulations
            percentages[states.index(state)].append(rate)
    for state in range(len(states)):
        amountsIndividuals.append(np.array((range(n_iterations),percentages[state])).transpose())
    return [amountsIndividuals,percentages]

def appliedMediumData(modelFunction,system,initialPercentageInfected,states,n_iterations,n_simulations):
    """Aplica el modelo epidemiológico en n_simulations
    modelFunction => Función basica del modelo epidemiológico
    initialPercentageInfected => Porcentaje de infectados en el momento inicial
    states => Estados que se consideran"""
    mediumStates = []
    stationarySystem = system
    for state in states:
        mediumStates.append([])
    for simulation in range(n_simulations):
        # infectedSystem = initialCondition(initialPercentageInfected,stationarySystem)
        infectedSystem = StateSpaceConfiguration.createSpace(stationarySystem).initialCondition(initialPercentageInfected)
        evolution = modelFunction(n_iterations,True,infectedSystem)[1]
        for state in range(len(states)):
            mediumStates[state].append(evolution[state])
    return mediumData(mediumStates,states,n_iterations,n_simulations)
    
def variationsBetweenScales(scale1,scale2):
    '''Genera una lista con las diferencias entre escalas'''
    variationsArray = np.zeros((len(scale1),2))
    for data in range(len(scale1)):
        variationsArray[data][0] = data
        variationsArray[data][1] = abs(scale1[data]-scale2[data])
    return variationsArray

def scale_differences(L1,L2):
    '''variationsBetweenScales'''
    L=np.zeros((len(L1),2))
    for i in range(len(L1)):
        L[i][0]=i; L[i][1]=abs(L1[i]-L2[i])
    return L