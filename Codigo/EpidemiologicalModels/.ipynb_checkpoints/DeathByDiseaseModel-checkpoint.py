import math
import random
import EpidemiologicalModels.SImodel as SI
import EpidemiologicalModels.DefineSpaceInCA as defSpace
import EpidemiologicalModels.BirthAndMortavilityModel as BMModel

def deathByDiseaseRule(deathFromDiseaseByAgeRange,system,systemAges):   
    '''Aplica probabilidades de muerte por enfermedad a grupos de edad sobre el sistema'''
    deathPositions = []
    infectedIndividualsPerGroup = []
    numberOfInfectedIndividualsDeathPerGroup = []
    systemCopy = defSpace.insideCopy(system)
    systemAgesCopy = defSpace.insideCopy(systemAges)
    for group in range(len(deathFromDiseaseByAgeRange)):
        groupPositions = BMModel.ageGroupPositions(deathFromDiseaseByAgeRange[group][0], deathFromDiseaseByAgeRange[group][1], systemAgesCopy)
        infectedIndividuals = []
        for individual in range(len(groupPositions)):          
            if system[groupPositions[individual][0],groupPositions[individual][1]] == SI.State.I.value:
                infectedIndividuals.append(groupPositions[individual])
        numberOfInfectedIndividualsDeath = math.ceil(len(infectedIndividuals) * deathFromDiseaseByAgeRange[group][2]) - 1
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

class deathByDisease:
    
    data = None
    evolutions = None

    def __init__(self, model, alpha, beta, birthRate, probabilityOfDyingByAgeGroup, deathFromDiseaseByAgeRange, system, systemAges, annualUnit, neighborhoodSystems, impactRates):
        self.model = model
        self.alpha = alpha; self.beta = beta
        self.birthRate = birthRate
        self.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
        self.deathFromDiseaseByAgeRange = deathFromDiseaseByAgeRange
        self.system = system; self.systemAges = systemAges
        self.nRows, self.nColumns = system.shape
        self.annualUnit = annualUnit
        self.neighborhoodSystems = neighborhoodSystems
        if self.model == "sis" or self.model == "SIS":
            self.states = [SI.State.S.value, SI.State.I.value, SI.State.D.value]
            self.colors = ["y", "r", "b"]
            self.labels = ["Susceptibles", "Infectados", "Espacios disponibles"]
        elif self.model == "sir" or self.model == "SIR":
            self.states = [SI.State.S.value, SI.State.I.value, SI.State.R.value, SI.State.D.value]
            self.colors = ["y", "r", "g", "b"]
            self.labels = ["Susceptibles", "Infectados", "Recuperados","Espacios disponibles"]
        self.impactRates = impactRates
        
    def basicRule(self,system,systemAges,timeUnit):
        evolution = BMModel.birthAndMortavility(self.model, self.alpha, self.beta, self.birthRate, self.probabilityOfDyingByAgeGroup, 
                                                system, systemAges, self.annualUnit, self.neighborhoodSystems, self.impactRates).basicRule(system,systemAges,timeUnit)
        systemCopy = defSpace.insideCopy(evolution[0])
        evolutionsAfterDeaths = deathByDiseaseRule(self.deathFromDiseaseByAgeRange, systemCopy,evolution[1])
        return evolutionsAfterDeaths