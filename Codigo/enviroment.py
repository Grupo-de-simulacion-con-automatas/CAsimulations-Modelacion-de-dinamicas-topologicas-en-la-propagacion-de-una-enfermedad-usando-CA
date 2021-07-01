#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import numpy as np
import random
import math
from IPython.core.pylabtools import figsize

def Moore(system,i,j):
    """Definición de la vecindad de Moore"""
    vicinityOf_ij = np.zeros((3,3))      
    vicinityOf_ij[0][0] = system[i-1][j-1]; vicinityOf_ij[0][1] = system[i-1][j]; vicinityOf_ij[0][2] = system[i-1][j+1]    
    vicinityOf_ij[1][0] = system[i][j-1]; vicinityOf_ij[1][1] = system[i][j]; vicinityOf_ij[1][2] = system[i][j+1]      
    vicinityOf_ij[2][0] = system[i+1][j-1]; vicinityOf_ij[2][1] = system[i+1][j]; vicinityOf_ij[2][2] = system[i+1][j+1]    
    return [vicinityOf_ij,[1,1]]  # Los valores en su vecindad, junto con la coordenada de la célula principal

def Von_Neumann(system,i,j):
    """Definición de la vecindad de Von Neumann"""
    vicinityOf_ij = -np.ones((3,3))              
    vicinityOf_ij[0][1] = system[i-1][j]
    vicinityOf_ij[1][0] = system[i][j-1]; vicinityOf_ij[1][1] = system[i][j]; vicinityOf_ij[1][2] = system[i][j+1]      
    vicinityOf_ij[2][1] = system[i+1][j]      
    return [vicinityOf_ij,[1,1]]  # Los valores en su vecindad, junto con la coordenada de la célula principal

def identificador(neighborhoodType,system,i,j):
    """Reconoce a function como la vecindad del agente en la posición ij en el sistema"""
    vicinityOf_ij = neighborhoodType(system,i,j)[0]
    masterCell = [neighborhoodType(system,i,j)[1]]
    return (vicinityOf_ij, masterCell)  # Los valores en su vecindad, junto con la coordenada de la célula principal

def insideCopy(system,extraRows=0,extraColumns=0):
    """Copia del sistema en un entorno extendido
    extraRows    => Cantidad de filas extra del entorno
    extraColumns => Cantidad de columnas extra del entorno"""
    nRows,nColumns = system.shape
    copy = -np.ones((nRows+(extraRows*2),nColumns+(extraColumns*2)))
    for row in range(nRows):
        for column in range(nColumns):
            copy[row+extraRows][column+extraColumns] = system[row][column]
    return copy

def stateCoordinates(system, stateIndicator):
    """Enlista los agentes que tengan un estado especifico
    stateIndicator : 0 -> Susceptibles; 1 -> Infectados; 2 -> Recuperados; -1 -> Espacios vacios; 3 -> Fallecidos"""
    nRows,nColumns = system.shape 
    coordinates = []
    for i in range(nRows):
        for j in range(nColumns):
            if system[i,j] == stateIndicator:  
                coordinates.append([i,j])
    return coordinates

def statePercentageInSpace(a,b,state,spatialState=0):
    """Porcentaje de individuos con el estado en el espacio (a de cada b tienen el estado)
    a,b => Porcentage visto como fracción
    state => Estado que van a adquirir los individuos
    spatialState => Estado que se considera como base para el cambio al estado state"""
    space = spatialState*np.ones((1,b))
    percentageInSpace = [] 
    for j in range(a):
        i = random.randint(1,b-1) 
        space[0][i] = state
    for m in range(1,b):
        percentageInSpace.append(int(space[0][m]))  
    return percentageInSpace

def initialCondition(initialPercentageInfected,system):
    """Condición inicial aplicada al sistema
    initialPercentageInfected => Porcentage inicial de infectados en el sistema"""
    susceptibleCoordinates = stateCoordinates(system,0)
    # Se toma la función techo para redondear a un entero la cantidad inicial de infectados 
    initialInfectedNumber = math.ceil(len(susceptibleCoordinates)*initialPercentageInfected)
    # Lista de posiciones de los idividuos que se infectaron y de los que se mantuvieron sanos al aplicar la condicion inicial
    percentageInSpace = statePercentageInSpace(initialInfectedNumber,len(susceptibleCoordinates)+1,1)
    systemCopy = insideCopy(system)
    for i in range(len(percentageInSpace)):
        # Los vectores en las posiciones descritas en la lista percentageInSpace adquieren el estado de infección
        systemCopy[susceptibleCoordinates[i][0]][susceptibleCoordinates[i][1]] = percentageInSpace[i]
    return systemCopy

def initialLocation(n,m,initialPercentageInfected,position="random",percentageOfInfectedMisplaced=0):
    """ubicación inicial de infectados    
    position : random
               northwest  north   northeast
               west       center  east
               southwest  south   southeast"""
    if position == "random":
        return initialCondition(initialPercentageInfected,np.zeros((n,m)))
    else: 
        # Se divide la zona rectángular en 9 bloques
        a = int(n/3); b = int(m/3)
        system = initialCondition(initialPercentageInfected*percentageOfInfectedMisplaced,np.zeros((n,m)))
        infectedBlock = initialCondition(initialPercentageInfected-percentageOfInfectedMisplaced,np.zeros((a,b)))
        if position == "northwest":
            for i in range(a):
                for j in range(b):
                    system[i][j] = infectedBlock[i][j]
        elif position == "north":
            for i in range(a):
                for j in range(b,2*b):
                    system[i][j] = infectedBlock[i][j-b]
        elif position == "northeast":
            for i in range(a):
                for j in range(2*b,3*b):
                    system[i][j] = infectedBlock[i][j-2*b]
        elif position == "west":
            for i in range(a,a*2):
                for j in range(b):
                    system[i][j] = infectedBlock[i-a][j]
        elif position == "center":
            for i in range(a,a*2):
                for j in range(b,2*b):
                    system[i][j] = infectedBlock[i-a][j-b]
        elif position == "east":
            for i in range(a,a*2):
                for j in range(2*b,3*b):
                    system[i][j]=infectedBlock[i-a][j-2*b]
        elif position == "southwest":
            for i in range(2*a,3*a):
                for j in range(b):
                    system[i][j] = infectedBlock[i-2*a][j]
        elif position == "south":
            for i in range(2*a,3*a):
                for j in range(b,2*b):
                    system[i][j] = infectedBlock[i-2*a][j-b]
        elif position == "southeast":
            for i in range(2*a,3*a):
                for j in range(2*b,3*b):
                    system[i][j] = infectedBlock[i-2*a][j-2*b]
        return system
    
def boundaryDefinition(boundaryConditions,system):
    """Definición de la estructura del sistema dadas las condiciones de frontera    
    boundaryConditions : Lista con las posiciones con individuos dentro del sistema"""
    nRows, mColumns = system.shape
    for condition in range(len(boundaryConditions)):
        system[boundaryConditions[condition][0],boundaryConditions[condition][1]] = 0  
    return system

def rectangularBoundary(rectangleRows,rectangleColumns,rowPosition,columnPosition,system):
    """Ubica una matriz nula de tamaño rectangleRows*rectangleColumns en la posición a,b del sistema"""
    boundaryConditions = []
    for row in range(rectangleRows):      
        for column in range(rectangleColumns):
            boundaryConditions.append((rowPosition+row,columnPosition+column)) 
    return boundaryDefinition(boundaryConditions,system)

def color(system):                 
    """Transformación que permite visualizar el sistema a color"""
    nRows, mColumns = system.shape
    systemCopy = insideCopy(system)
    for i in range(nRows):
        for j in range(mColumns):
            if systemCopy[i][j] == 0:    
                systemCopy[i][j] = 190  # Susceptibles => Amarillo
            if systemCopy[i][j] == 1:    
                systemCopy[i][j] = 240  # Infectados => Rojo
            if systemCopy[i][j] == 2:    
                systemCopy[i][j] = 115  # Recuperados => Verde
            if systemCopy[i][j] == -1:   
                systemCopy[i][j] = 0    # Vacíos => Negro
            if systemCopy[i][j] == 3:
                systemCopy[i][j] = 256  # Muertos => Gris
    increasedSystem = insideCopy(systemCopy,1,1)
    increasedSystem[0][0] = 0; increasedSystem[nRows+1][mColumns+1] = 256  
    return increasedSystem