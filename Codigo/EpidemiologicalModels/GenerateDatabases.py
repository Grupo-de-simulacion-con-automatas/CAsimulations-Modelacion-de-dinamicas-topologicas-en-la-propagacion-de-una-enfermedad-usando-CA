#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
from EpidemiologicalModels.epidemiologicalModels import *

def Coordinates(system):
    nrows, ncolumns = system.shape
    coordinatesSystem = []
    for i in range(nrows):
        coordinatesSystem.append([[i,j] for j in range(ncolumns)])
    return np.array(coordinatesSystem)

def ListOfNeighbors(system,isInsideCopy=True):
    neighbors = []
    nrows, ncolumns = system.shape
    for i in range(nrows):
        for j in range(ncolumns):
            if system[i][j] != -1:
                if isInsideCopy:
                    neighbors.append([i-1,j-1])
                else:
                    neighbors.append([i,j])
    return neighbors

def NeighborsOfijInSystemCoordinates(system,i,j,neighborCoordinates):
    systemCoordinates = Coordinates(system)
    listOfNeighborsOfij = []
    for coordinate in neighborCoordinates:
        listOfNeighborsOfij.append(systemCoordinates[i+coordinate[0]][j+coordinate[1]])
    return [list(n) for n in listOfNeighborsOfij]

def Neighbors(system,functionOfNeighbors,extraRows,extraColumns):
    nrows, ncolumns = system.shape
    systemExtended = insideCopy(system,extraRows,extraColumns)
    coordinatesSystem = Coordinates(system)
    listOfNeighborsByCell = []
    for i in range(nrows):
        for j in range(ncolumns):
            neighborsOfCellij = ListOfNeighbors(functionOfNeighbors(systemExtended,i+extraRows,j+extraColumns)[0])
            listOfNeighborsByCell.append([[i,j],NeighborsOfijInSystemCoordinates(system,i,j,neighborsOfCellij)])
    return listOfNeighborsByCell

def StateOfNeighbors(system,coordinatesOfneighborsOfij):
    statesByCell = []
    for cellNeighbors in coordinatesOfneighborsOfij:
        states = [system[cellNeighbors[0][0]][cellNeighbors[0][1]]]
        statesOfNeighbors = []
        for neighborCordinate in coordinatesOfneighborsOfij[coordinatesOfneighborsOfij.index(cellNeighbors)][1]:
            statesOfNeighbors.append(system[neighborCordinate[0]][neighborCordinate[1]])
        states.append(statesOfNeighbors)
        statesByCell.append(states)
    return statesByCell

def IndexOfListInList(item, listOfList):
    for List in listOfList:
        if item in List:
            return listOfList.index(List) 

def ListOfEvolutionsByCell(cell,listOfCoordinatesNeighbors,listOfNeighborsStatesByEvolution):
    index = IndexOfListInList(cell,listOfCoordinatesNeighbors)
    statesOFCell = []
    for evolution in listOfNeighborsStatesByEvolution:
        statesOFCell.append(evolution[index][0])
    return statesOFCell

def GetStatesByIteration(modelEvolutions,listOfCoordinatesNeighbors):
    cellStateByIteration = pd.DataFrame()
    cellStateByIteration["Iteración"] = range(len(modelEvolutions))
    listOfNeighborsStatesByEvolution = [StateOfNeighbors(evo,listOfCoordinatesNeighbors) for evo in modelEvolutions]
    for coordinate in listOfCoordinatesNeighbors:
        cellStateByIteration[f"{coordinate[0]}"] = ListOfEvolutionsByCell(coordinate[0],listOfCoordinatesNeighbors,
                                                    listOfNeighborsStatesByEvolution)
    return cellStateByIteration

def NeighborsStatesInDataFrame(cell,listOfCoordinatesNeighbors,dataFrame):
    neighborsStates = pd.DataFrame()
    neighborsStates["Iteración"] = dataFrame["Iteración"]
    index = IndexOfListInList(cell,listOfCoordinatesNeighbors)
    for item in listOfCoordinatesNeighbors[index][1]:
        neighborsStates[f"{item}"] = dataFrame[f"{item}"]
    return neighborsStates


