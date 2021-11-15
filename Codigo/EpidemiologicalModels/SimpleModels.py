import math
import EpidemiologicalModels.SImodel as SI
import EpidemiologicalModels.DefineSpaceInCA as defSpace

class SISmodel(SI.SImodel):

    states = [SI.State.S.value, SI.State.I.value]
    colors = ["y", "r"]
    labels = ["Susceptibles", "Infectados"]
    
    def __siRule(self, updatedSystem, impactRates): 
        """Regla S -> I"""
        return SI.SImodel(self.alpha, self.beta, updatedSystem, self.neighborhoodSystems, impactRates).Apply()  
    
    def __isRule(self, previousSystem):      
        """Regla I -> S"""
        infectedCoordinates = defSpace.stateCoordinates(previousSystem, SI.State.I.value)
        initialRecoveredNumber = math.ceil(len(infectedCoordinates) * self.alpha)
        percentageInSpace = defSpace.statePercentageInSpace(initialRecoveredNumber, len(infectedCoordinates) + 1, 
                                                            self.states[0], self.states[1])
        systemCopy = defSpace.insideCopy(previousSystem)
        for i in range(len(percentageInSpace)):
            systemCopy[infectedCoordinates[i][0]][infectedCoordinates[i][1]] = percentageInSpace[i]
        return systemCopy
    
    def basicRule(self,previousSystem):   
        """Aplica la regla de evolución al sistema previousSystem"""
        updatedStates_IS = self.__isRule(previousSystem)
        updatedStates_SI = self.__siRule(updatedStates_IS, self.impactRates)        
        return updatedStates_SI

class SIRmodel(SI.SImodel):

    states = [SI.State.S.value, SI.State.I.value, SI.State.R.value]
    colors = ["y", "r", "g"]
    labels = ["Susceptibles", "Infectados", "Recuperados"]
        
    def __siRule(self, updatedSystem, impactRates): 
        """Regla S -> I"""
        return SI.SImodel(self.alpha, self.beta, updatedSystem, self.neighborhoodSystems, impactRates).Apply()
    
    def __irRule(self,previousSystem):      
        """Regla I -> R"""
        infectedCoordinates = defSpace.stateCoordinates(previousSystem, SI.State.I.value)
        initialRecoveredNumber = math.ceil(len(infectedCoordinates) * self.alpha)
        percentageInSpace = defSpace.statePercentageInSpace(initialRecoveredNumber, len(infectedCoordinates) + 1, 
                                                            self.states[2], self.states[1])
        systemCopy = defSpace.insideCopy(previousSystem)
        for i in range(len(percentageInSpace)):
            systemCopy[infectedCoordinates[i][0]][infectedCoordinates[i][1]] = percentageInSpace[i]
        return systemCopy
    
    def basicRule(self,previousSystem):   
        """Aplica la regla de evolución al sistema previousSystem"""
        updatedStates_IR = self.__irRule(previousSystem) 
        updatedStates_SI = self.__siRule(updatedStates_IR, self.impactRates)   
        return updatedStates_SI