# class SystemMetrics:
#     """Metricas que se monitorean por cada modelo:
#     statusInTheSystem      => Cantidad de individuos por estado
#     numberOfIndividuals    => Cantidad de individuos en el sistema 
#     percentagesInTheSystem => Cantidad normalizada de individuos por estado"""
#     def __init__(self, system, states, i=None, j=None):
#         self.system = system; self.states = states
#         self.nRows,self.nColums = system.shape
#         self.i, self.j = i, j # Si el sistema es una vecindad
    
#     def statusInTheSystem(self, percentages=True):
#         """Lista con las cantidades de individuos por cada estado
#         percentages == True  => Valores normalizados
#         percentages == False => Valores enteros"""
#         globalMetrics = [0]*len(self.states)
#         for row in range(self.nRows):
#             for column in range(self.nColums):
#                 if self.system[row][column] in self.states:
#                     state = self.states.index(self.system[row][column])
#                     globalMetrics[state] += 1
#         if self.i != None and self.j != None:
#             if self.system[self.i][self.j] in self.states:
#                 state = self.states.index(self.system[self.i][self.j])
#                 globalMetrics[state] -= 1
#         if percentages == False:
#             return globalMetrics
#         else:
#             percentage = []
#             for state in globalMetrics:
#                 percentage.append(state/self.numberOfIndividuals())    
#             return percentage
    
#     def numberOfIndividuals(self):
#         """Cantidad de individuos en el sistema"""
#         self.totalIndividuals = sum(self.statusInTheSystem(percentages=False))
#         if self.i != None and self.j != None:
#             if self.system[self.i][self.j] in self.states:
#                 self.totalIndividuals += 1     
#         return self.totalIndividuals

# def statusInTheSystem(self, percentages=True):
#         """Lista con las cantidades de individuos por cada estado
#         percentages == True  => Valores normalizados
#         percentages == False => Valores enteros"""
#         globalMetrics = [0]*len(self.states)
#         for row in range(self.nRows):
#             for column in range(self.nColums):
#                 if self.system[row][column] in self.states:
#                     state = self.states.index(self.system[row][column])
#                     globalMetrics[state] += 1
#         if self.i != None and self.j != None:
#             if self.system[self.i][self.j] in self.states:
#                 state = self.states.index(self.system[self.i][self.j])
#                 globalMetrics[state] -= 1
#         if percentages == False:
#             return globalMetrics
#         else:
#             percentage = []
#             for state in globalMetrics:
#                 percentage.append(state/self.numberOfIndividuals())    
#             return percentage