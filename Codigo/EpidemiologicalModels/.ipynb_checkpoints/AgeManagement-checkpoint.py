class AgeManagement:
    def agesMatrix(ranges, system):
    '''Arreglo de edades aleatorias'''
    amoungIndividuals = metrics.SystemMetrics(system, [SI.State.S.value, SI.State.I.value, SI.State.R.value, SI.State.H.value]).numberOfIndividuals() 
    agesDivisions = AgesDivisions(ranges, amoungIndividuals)
    for divition in range(len(agesDivisions)):
        for individualPerGroup in range(len(agesDivisions[divition])):
            agesDivisions[divition][individualPerGroup] = random.randint(ranges[divition][0], ranges[divition][1]) 
    concatenatedAgeList = agesDivisions[0]
    for i in range(1, len(agesDivisions)): 
        concatenatedAgeList = concatenatedAgeList + agesDivisions[i]
    numberOfRows, numberOfColumns = system.shape    
    matrixOfAges = -np.ones((numberOfRows, numberOfColumns))
    for row in range(numberOfRows):
        for column in range(numberOfColumns):
            if system[row,column] != SI.State.H.value and system[row,column] != SI.State.D.value:
                randomAge = random.choice(concatenatedAgeList)
                matrixOfAges[row,column] = randomAge
            elif system[row,column] == SI.State.D.value: matrixOfAges[row,column] = 0
    return matrixOfAges

    def AgesDivisions(ranges, amoungIndividuals):
        agesDivisions = []
        for Range in ranges:
            agesDivisions.append([0] * math.ceil(Range[2] * amoungIndividuals))
        return agesDivisions

    def ageGroupPositions(minAge, maxAge, systemAges):   
        '''Genera las posiciones de los individuos que tienen entre minAge y maxAge años en el sistema'''
        groupPositions = []
        numberOfRows, numberOfColumns = systemAges.shape
        for row in range(numberOfRows):
            for column in range(numberOfColumns):
                if minAge < systemAges[row][column] and systemAges[row][column] < maxAge:
                    groupPositions.append([row,column])
        return groupPositions

    def newYear(birthRate, probabilityOfDyingByAgeGroup, systemAges, timeUnit, annualUnit):
        '''Nuevo año para los agentes'''
        agePositions = []
        mortalityApplicationGroups = []
        deadPositions = []
        numberOfRows, numberOfColumns = systemAges.shape
        newYearMatrix = np.zeros((numberOfRows, numberOfColumns))
        for row in range(numberOfRows):
            for column in range(numberOfColumns):
                if systemAges[row][column] != 0 and systemAges[row][column] != -1 and timeUnit%annualUnit == 0: newYearMatrix[row][column] = systemAges[row][column] + 1
                elif systemAges[row,column] == 0:
                    rate = random.randint(0,100)
                    if rate < birthRate: newYearMatrix[row][column] = 1
                elif systemAges[row,column] == -1: newYearMatrix[row,column] = -1
                else: newYearMatrix[row,column] = systemAges[row,column]
        for group in range(len(probabilityOfDyingByAgeGroup)):   
            agePositions.append(ageGroupPositions(probabilityOfDyingByAgeGroup[group][0], probabilityOfDyingByAgeGroup[group][1], systemAges))
            mortalityApplicationGroups.append(math.ceil(len(agePositions[group]) * probabilityOfDyingByAgeGroup[group][2]) - 1)
        for group in range(len(mortalityApplicationGroups)):
            for age in range(mortalityApplicationGroups[group]):
                numberOfDead = random.randint(0, len(agePositions[group]) - 1)
                deadPositions.append(agePositions[group][numberOfDead])
        for position in range(len(deadPositions)):
            newYearMatrix[deadPositions[position][0]][deadPositions[position][1]] = 0
        return newYearMatrix