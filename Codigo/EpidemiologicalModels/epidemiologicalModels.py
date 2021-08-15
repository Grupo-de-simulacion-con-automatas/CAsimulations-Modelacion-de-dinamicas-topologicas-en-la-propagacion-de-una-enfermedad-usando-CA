#!/usr/bin/env python
# coding: utf-8

# In[ ]:

get_ipython().system('pip install opencv-python')
get_ipython().system('pip install opencv-contrib-python')

import seaborn as sns
from EpidemiologicalModels.models import *

class models:
    # En las variables data y evolutions se almacenaran los datos luego de aplicar los modelos
    data = None  # Reporte numperico de los cambios en cada estado
    evolutions = None  # Reporte visual de los cambios del sistema   
    # Datos tomados por defecto
    extraRows = 1; extraColumns = 1  # Cantidad de filas y columnas extra para aplicar el tipo de vecindad elegido
    modelHasAges = False
    systemAges = None  # Edades de los individuos en el sistema
    annualUnit = None  # Unidad de ciclo temporal (año)
    birthRate = None  # Tasa de natalidad 
    probabilityOfDyingByAgeGroup = None  # Tasa de mortalidad por grupo de edad
    modelHasDeathByDisease = False  
    deathFromDiseaseByAgeRange = None  # Tasa de mortalidad causada por la enfermedad por grupo de edad
    
    def __init__(self,model,alpha,beta,system,neighborhoodType):
        """Modelos soportados: sis, sir, sis_birthAndMortavility, sir_birthAndMortavility, sis_deathByDisease, sir_deathByDisease"""
        self.model = model  # Modelo epidemiológico que se va a aplicar
        self.alpha = alpha; self.beta = beta  # Datos básicos de la enfermedad
        self.system = system  # Sistema sobre el que se va a aplicar el modelo
        self.neighborhoodType = neighborhoodType  # Tipo de vecindad que va a considerar para el análisis
        
    def __evalConditions(self):
        # Definición de las herramientas para aplicar los modelos
        if self.model == "sis":
            self.epidemiologicalModel = sis(self.alpha,self.beta,self.system,self.extraRows,self.extraColumns,self.neighborhoodType)
        elif self.model == "sir":
            self.epidemiologicalModel = sir(self.alpha,self.beta,self.system,self.extraRows,self.extraColumns,self.neighborhoodType)
        else:
            if self.birthRate == None:
                print("Defina birthRate, probabilityOfDyingByAgeGroup, systemAges, annualUnit") 
            self.modelHasAges = True
            if self.model == "sis_birthAndMortavility":
                self.epidemiologicalModel = birthAndMortavility("sis",self.alpha,self.beta,self.birthRate,
                                                                self.probabilityOfDyingByAgeGroup,self.system,self.systemAges,
                                                                self.annualUnit,self.extraRows,self.extraColumns,self.neighborhoodType)
            if self.model == "sir_birthAndMortavility":
                self.epidemiologicalModel = birthAndMortavility("sir",self.alpha,self.beta,self.birthRate,
                                                                self.probabilityOfDyingByAgeGroup,self.system,self.systemAges,
                                                                self.annualUnit,self.extraRows,self.extraColumns,self.neighborhoodType)
            if self.model == "sis_deathByDisease":
                self.epidemiologicalModel = deathByDisease("sis",self.alpha,self.beta,self.birthRate,
                                                           self.probabilityOfDyingByAgeGroup,self.deathFromDiseaseByAgeRange,
                                                           self.system,self.systemAges,self.annualUnit,self.extraRows,
                                                           self.extraColumns,self.neighborhoodType)
            if self.model == "sir_deathByDisease":
                self.epidemiologicalModel = deathByDisease("sir",self.alpha,self.beta,self.birthRate,
                                                           self.probabilityOfDyingByAgeGroup,self.deathFromDiseaseByAgeRange,
                                                           self.system,self.systemAges,self.annualUnit,self.extraRows,
                                                           self.extraColumns,self.neighborhoodType)
    
    def basicModel(self,n_iterations,modifiedSystem=False,system=None):
        self.__evalConditions()
        """Aplica el modelo n_iterations veces"""
        if modifiedSystem == False:
            evolutions = appliedModel(self.epidemiologicalModel.basicRule,self.system,n_iterations,self.modelHasAges,self.systemAges)
        else:
            evolutions = appliedModel(self.epidemiologicalModel.basicRule,system,n_iterations,self.modelHasAges,self.systemAges)
        visualization = dataVisualization(evolutions,self.epidemiologicalModel.states)
        self.data = visualization[0]; self.evolutions = visualization[2]
        return visualization
    
    def metricsPlot(self,n_iterations,title):
        """Gráfica la evolución de los estados en n_iterations"""
        if self.data == None:
            visualization = self.basicModel(n_iterations)
            self.data = visualization[0]; self.evolutions = visualization[2]
        graficas(self.data, self.epidemiologicalModel.eti, self.epidemiologicalModel.col, title)  
        
    def evolutionsPlot(self,n_iterations,specificIteration):
        """Gráfica una evolución especifica del conjunto de evoluciones generadas tras aplicar el modelo"""
        if self.evolutions == None:
            visualization = self.basicModel(n_iterations)
            self.data = visualization[0]; self.evolutions = visualization[2]
        plt.imshow(color(self.evolutions[specificIteration]),cmap="nipy_spectral",interpolation='nearest')
        
    def mediumCurves(self,initialPercentageInfected,n_iterations,n_simulations):
        self.__evalConditions()
        """Curvas promedio del modelo"""
        return appliedMediumData(self.basicModel,self.system,initialPercentageInfected,
                                 self.epidemiologicalModel.states,n_iterations,n_simulations)     
                 
def heatmap(evolutionsOfSystem,state):
    """Mapa de calor para la población infectada (SIR_Model[6])"""
    stateHeatMap = []
    n,m = evolutionsOfSystem[0].shape
    for iteration in range(len(evolutionsOfSystem)):
        stateMatrix = np.zeros((n,m))
        for row in range(n):
            for column in range(m):
                if evolutionsOfSystem[iteration][row][column] == state:
                    stateMatrix[row][column] = 1
        stateHeatMap.append(stateMatrix)
    average = 1/len(stateHeatMap)*np.sum(stateHeatMap,axis=0)
    sns.heatmap(average, center=0, cmap='viridis',  fmt='.3f')