#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import matplotlib.pyplot as plt

class CompartmentalModelsInEDOS:
    __h = 0.1; __n_iterations = 1
    __solutions = []; titlePlot = "Modelo compartimental"  
    
    def __init__(self, listOfDifferentialEquations, initialConditions):
        self.listOfDifferentialEquations = listOfDifferentialEquations
        self.__initialConditions = initialConditions
        self.__wasTheModelApplied = False
        self.__validParameters = False
        
    def __AreTheParametersValid(self):
        if not self.__IsThereAnInitialConditionForEachDifferentialEquation():
            print(f"Los parámetros no son validos, tienes {len(self.listOfDifferentialEquations)} ecuaciones diferenciales y {len(self.__initialConditions)} condiciones iniciales.")
        elif self.__n_iterations == 1:
            print(f"Solo esta considerando una iteración. Intente cambiando la cantidad de iteraciones con 'n_iterations()'.")
        else:
            self.__validParameters = True
    
    def __IsThereAnInitialConditionForEachDifferentialEquation(self):
        return len(self.listOfDifferentialEquations) == len(self.__initialConditions)    
    
    def __InitialValuesOfTheSolution(self):
        self.__discreteSolutions = []
        for value in self.__initialConditions:
            self.__discreteSolutions.append([value])
        return self.__discreteSolutions
    
    def __IsTheFirstIteration(self):
        return self.__discreteSolutions == []
    
    def __UpdateSolution(self):
        lastCalculatedValues = []
        if self.__IsTheFirstIteration():
            self.__InitialValuesOfTheSolution()
        for discreteSolution in self.__discreteSolutions:
            lastCalculatedValues.append(discreteSolution[-1])
        return lastCalculatedValues
    
    def __CalculateNewValue(self, diferentialEquationPosition, lastCalculatedValues):
        return self.__discreteSolutions[diferentialEquationPosition][-1]+self.__h*self.listOfDifferentialEquations[diferentialEquationPosition](lastCalculatedValues)
    
    def __TheModelWasApplied(self):
        self.__wasTheModelApplied = True
        self.__solutions = [self.__discreteSolutions, self.__domainValues]
    
    def __ApplyEulerMethod(self):
        self.__AreTheParametersValid()
        if self.__validParameters:
            self.__InitialValuesOfTheSolution()
            for iteration in range(1, self.__n_iterations):
                lastCalculatedValues = self.__UpdateSolution()
                for differentialEquation in self.listOfDifferentialEquations:
                    df = self.listOfDifferentialEquations.index(differentialEquation)
                    updatedValue = self.__CalculateNewValue(df, lastCalculatedValues)
                    self.__discreteSolutions[df].append(updatedValue)
            self.__TheModelWasApplied()
        return self.__solutions
    
    def n_iterations(self, valueForn_iterations):
        self.__n_iterations = valueForn_iterations
        self.__domainValues = range(valueForn_iterations)
    
    def ModelSolutions(self):
        if self.__wasTheModelApplied:
            return self.__solutions
        else:
            return self.__ApplyEulerMethod()
        
    def h(self, valueForh):
        self.__h = valueForh
        
    def plotSolutions(self,nameValues,colors,limit = False,legends = True):
        self.ModelSolutions()
        if len(nameValues) != len(self.__solutions[0]):
            print("Debe asignar la misma cantidad de nombres de variables")
        elif len(colors) != len(self.__solutions[0]):
            print("Debe asignar la misma cantidad de colores")
        else:
            for solution in self.__solutions[0]:
                index = self.__solutions[0].index(solution)
                plt.plot(self.__solutions[1], solution, c = colors[index], label = nameValues[index])
            plt.title(self.titlePlot)
            if legends:
                plt.legend()
            if limit:
                plt.plot(self.__solutions[1], [1 for s in range(len(self.__solutions[1]))], "k--")
    
    def PrintParameters(self):
        print(f"""h: {self.__h} \nn_iterations: {self.__n_iterations} \ndifferentialEquations: {self.listOfDifferentialEquations}
        """)
                
                
                
                