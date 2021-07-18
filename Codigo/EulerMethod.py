#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import matplotlib.pyplot as plt

def listInitialization(listOfList):
    listsWithInitialValues = []
    for value in listOfList:
        listsWithInitialValues.append([value])
    return listsWithInitialValues

def specificIterationValues(iteration,listOfList):
    iterationValues = []
    for List in listOfList:
        iterationValues.append(List[iteration])
    return iterationValues

def isDifferent(newValue, previousValue):
    return newValue != previousValue

class CompartimentalModels:
    
    modelApplied = None
    titlePlot = "Modelo compartimental"
    h = 0.1
    n_iterations = 1
    
    def __init__(self, functionsModel, initialConditions):
        self.functionsModel = functionsModel
        self.initialConditions = initialConditions

    def __EulerMethod(self):
        if len(self.functionsModel) != len(self.initialConditions):
            print("Debe definir un valor inicial para cada ecuación diferencial")
        else:
            domainValues = range(self.n_iterations)
            discreteSolutions = listInitialization(self.initialConditions)
            for iteration in range(1, self.n_iterations):
                lastIterationValues = specificIterationValues(iteration - 1, discreteSolutions)
                for df in range(len(self.functionsModel)):
                    updatedValue = discreteSolutions[df][iteration - 1] + self.h * self.functionsModel[df](lastIterationValues)
                    discreteSolutions[df].append(updatedValue)
            self.modelApplied = [discreteSolutions, domainValues]
            return self.modelApplied
    
    def solutions(self):
        if self.modelApplied == None:
            return self.__EulerMethod()
        else:
            return self.modelApplied
        
    def plotSolutions(self,nameValues,colors,limit = False,legends = True):
        if self.modelApplied == None:
            self.__EulerMethod()
        if len(nameValues) != len(self.modelApplied[0]):
            print("Debe asignar la misma cantidad de nombres de variables")
        elif len(colors) != len(self.modelApplied[0]):
            print("Debe asignar la misma cantidad de colores")
        else:
            for solution in self.modelApplied[0]:
                index = self.modelApplied[0].index(solution)
                plt.plot(self.modelApplied[1], solution, c = colors[index], label = nameValues[index])
            plt.title(self.titlePlot)
            if legends:
                plt.legend()
            if limit:
                plt.plot(self.modelApplied[1], [1 for s in range(len(self.modelApplied[1]))], "k--")