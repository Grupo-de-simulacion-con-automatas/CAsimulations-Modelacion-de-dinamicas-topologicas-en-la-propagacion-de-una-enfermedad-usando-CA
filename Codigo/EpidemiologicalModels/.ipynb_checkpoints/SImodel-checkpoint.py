import enum
import random
import EpidemiologicalModels.DefineSpaceInCA as defSpace
import EpidemiologicalModels.NeighborhoodManager as N_Manager

class State(enum.Enum):
    H = -1  # Huecos
    S = 0   # Susceptibles
    I = 1   # Infectados
    R = 2   # Recuperados
    D = 3   # Espacio vacío que se puede ocupar por una nueva célula

class SImodel:

    data = None
    evolutions = None

    def __init__(self, alpha, beta, system, neighborhoodSystems):
        """Modelo SI
        alpha => Tasa de recuperación
        beta  => Tasa de infección
        system => Espacio de celulas
        neighborhoodSystems => Lista con las matrices que describen los sistemas de vecindades en el sistema
        """
        self.alpha = alpha
        self.beta = beta 
        self.system = system
        self.nRows, self.nColumns = system.shape
        self.neighborhoodSystems = neighborhoodSystems
        self.nRows, self.nColumns = system.shape
    
    def __CountNeighborsByState(self,neighbors):
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

    def __SI_rule(self,cellState,neighborsByImpact,impacts = [1,0]): # Grados de impacto 0 y 1
        """Regla totalística que describe el cambio entre los estados S e I de manera local"""
        impactRanges = list(neighborsByImpact.keys())
        numberOfS = 0; numberOfI = 0; numberOfH = 0
        numberOfCells = 0
        for ir in impactRanges:
            amountOfIndividuals = 0
            neighbors = neighborsByImpact.get(ir)
            numberOfSByImpact, numberOfIByImpact, amountOfCells, amountOfHoles = self.__CountNeighborsByState(neighbors)
            numberOfS += numberOfSByImpact * impacts[impactRanges.index(ir)]
            numberOfI += numberOfIByImpact * impacts[impactRanges.index(ir)]
            numberOfH += amountOfHoles * impacts[impactRanges.index(ir)]
            numberOfCells += amountOfCells * impacts[impactRanges.index(ir)]
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
        systemUpdate = defSpace.insideCopy(self.system)
        for ns in self.neighborhoodSystems:
            neighborsByImpact = N_Manager.NeigborhoodManager(self.system,ns[1]).ImpactNeighborClassifier()
            if systemUpdate[ns[0][0]][ns[0][1]] not in [State.H.value, State.R.value, State.D.value]:
                systemUpdate[ns[0][0]][ns[0][1]] = self.__SI_rule(self.system[ns[0][0]][ns[0][1]], neighborsByImpact)   
        return systemUpdate  