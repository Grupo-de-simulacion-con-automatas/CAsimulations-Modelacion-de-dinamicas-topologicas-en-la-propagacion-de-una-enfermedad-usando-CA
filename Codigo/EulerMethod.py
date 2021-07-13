#!/usr/bin/env python
# coding: utf-8

# In[ ]:

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

def EulerMethod(differentialEquations,initialValues,h,n_iterations):
    if len(differentialEquations) != len(initialValues):
        print("Debe definir un valor inicial para cada ecuación diferencial")
    else:
        domainValues = range(n_iterations)
        discreteSolutions = listInitialization(initialValues)
        for iteration in range(1,n_iterations):
            lastIterationValues = specificIterationValues(iteration-1,discreteSolutions)
            for df in range(len(differentialEquations)):
                updatedValue = discreteSolutions[df][iteration-1]+h*differentialEquations[df](lastIterationValues)
                discreteSolutions[df].append(updatedValue)
        return [discreteSolutions, domainValues]

