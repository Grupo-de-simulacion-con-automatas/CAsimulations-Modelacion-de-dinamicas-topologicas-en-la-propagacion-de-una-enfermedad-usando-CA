import CAsimulation.CellSpaceConfiguration as CellSpaceConfiguration
import CAsimulation.AgeManagement as AgeManagement
import CAsimulation.NeighborhoodManager as NeighborhoodManager
import CAsimulation.Models as Models
import CAsimulation.CompartmentalModelsInEDOS as CompartmentalModelsInEDOS

def CellSpace(nRows, nColumns, xnRows = -1, xnColumns = -1, unRows = 0, unColumns = 0):
    """
    Genera la configuración básica de un sistema de células
    Parámetros:
        nRows(int)     Filas de la región interna inicial del sistema / filas del sistema
        nColumns(int)  Columnas de la región interna inicial del sistema / Columnas del sistema
        xnRows(int)    Fila donde se ubica la región interna inicial
        xnColumns(int) Columna donde se ubica la región interna inicial
        unRows(int)    Filas del área externa
        unColumns(int) Columnas del área externa
    Salida:
        EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration  Sistema de células

    Ejemplo 1:
    space = CellSpace(10,10)
    space.system
    --> array([[0., 0., 0., 0., 0.],
               [0., 0., 0., 0., 0.],
               [0., 0., 0., 0., 0.],
               [0., 0., 0., 0., 0.],
               [0., 0., 0., 0., 0.]])

    space.initialLocationOfInfected(0.1)
    --> array([[0., 0., 0., 0., 0.],
               [0., 0., 1., 0., 0.],
               [1., 0., 0., 0., 0.],
               [0., 1., 0., 0., 0.],
               [0., 0., 0., 0., 0.]])

    Ejemplo 2:
    space = CellSpace(3,1,5,5)
    space.system
    --> array([[ 0., -1., -1., -1., -1.],
               [ 0., -1., -1., -1., -1.],
               [ 0., -1., -1., -1., -1.],
               [-1., -1., -1., -1., -1.],
               [-1., -1., -1., -1., -1.]])

    space.rectangularBoundary(2,2,3,1)
    --> array([[ 0., -1., -1., -1., -1.],
               [ 0., -1., -1., -1., -1.],
               [ 0., -1., -1., -1., -1.],
               [-1.,  0.,  0., -1., -1.],
               [-1.,  0.,  0., -1., -1.]])

    Ejemplo 3:
    space = CellSpace(3,1,5,5,1,2)
    space.system
    --> array([[-1., -1., -1., -1., -1.],
               [-1., -1.,  0., -1., -1.],
               [-1., -1.,  0., -1., -1.],
               [-1., -1.,  0., -1., -1.],
               [-1., -1., -1., -1., -1.]])
    """
    return CellSpaceConfiguration.CellSpaceConfiguration(nRows, nColumns, xnRows, xnColumns, unRows, unColumns)

def CreateAgeMatrix(ranges, cellSpace):
    """
    Crea una matriz con las edades de las células de acuerdon con las probabilidades definidas en ranges.
    Parámetros: 
        ranges(list(list))  Debe contener los rangos de edad y la proporción de individuos del sistema que tendran una edad en el rango.
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Systema de células a las que se les asignará una edad.
    Salidas:
        numpy.ndarray  Arreglo con las edades del sistema de células.
    
    Ejemplo:
    ranges = [[0,10,0.2],[11,100,0.8]]  # 20% tienen entre 0 y 10 años, y 80% tienen entre 11 y 100.
    space = CellSpace(5,5)
    createAgeMatrix(ranges, space)
    
    --> array([[ 1., 81., 33.,  5., 18.],
               [90., 19., 18., 36., 50.],
               [ 5., 67.,  4., 18., 74.],
               [45., 36.,  4., 36.,  4.],
               [ 5., 67., 74.,  1.,  1.]])
    """
    return AgeManagement.AgesMatrix(ranges, cellSpace).agesMatrix

def GenerateNeighborhoodSystem(cellSpace, neighborhoodType = "random"):
    """
    Genera un conjunto de vecindades básico para aplicar los modelos epidemiológicos
    Parámetros:
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Sistema de células para el cuál se definirá el sistema de vecindades
        neighborhoodType(string)  Configuración del sistema - Valores permitidos (Moore - Von Neumann), por defecto se genera un sistema con valores aleatorios
    Salidas:
        list  Lista con los arreglos que describen el conjunto de vecindades y las coordenadas de cada célula

    Ejemplo 1:
    GenerateNeighborhoodSystem(CellSpace(3,3))
    --> [[[0, 0],array([[0., 1., 1.],
                        [1., 1., 1.],
                        [1., 1., 1.]])],
         [[0, 1],array([[1., 0., 1.],
                        [1., 1., 1.],
                        [1., 1., 1.]])],
         [[0, 2],array([[1., 1., 1.],
                        [1., 1., 1.],
                        [1., 1., 1.]])],
         [[1, 0],array([[1., 1., 1.],
                        [1., 1., 1.],
                        [1., 1., 1.]])],
         [[1, 1],array([[1., 1., 1.],
                        [1., 1., 1.],
                        [1., 1., 1.]])],
         [[1, 2],array([[1., 1., 1.],
                        [1., 1., 0.],
                        [1., 1., 1.]])],
         [[2, 0],array([[1., 1., 1.],
                        [1., 1., 1.],
                        [0., 1., 1.]])],
         [[2, 1],array([[1., 1., 1.],
                        [1., 1., 1.],
                        [1., 1., 1.]])],
         [[2, 2],array([[1., 1., 1.],
                        [1., 1., 1.],
                        [1., 1., 0.]])]]

    Ejemplo 2:
    GenerateNeighborhoodSystem(CellSpace(3,3),"Moore")
    --> [[[0, 0],array([[0., 0., 1.],
                        [0., 0., 1.],
                        [1., 1., 1.]])],
         [[0, 1],array([[0., 0., 0.],
                        [0., 0., 0.],
                        [1., 1., 1.]])],
         [[0, 2],array([[1., 0., 0.],
                        [1., 0., 0.],
                        [1., 1., 1.]])],
         [[1, 0],array([[0., 0., 1.],
                        [0., 0., 1.],
                        [0., 0., 1.]])],
         [[1, 1],array([[0., 0., 0.],
                        [0., 0., 0.],
                        [0., 0., 0.]])],
         [[1, 2],array([[1., 0., 0.],
                        [1., 0., 0.],
                        [1., 0., 0.]])],
         [[2, 0],array([[1., 1., 1.],
                        [0., 0., 1.],
                        [0., 0., 1.]])],
         [[2, 1],array([[1., 1., 1.],
                        [0., 0., 0.],
                        [0., 0., 0.]])],
         [[2, 2],array([[1., 1., 1.],
                        [1., 0., 0.],
                        [1., 0., 0.]])]]
    """
    if neighborhoodType.lower() == 'moore':
        return NeighborhoodManager.Moore(cellSpace)
    elif neighborhoodType.lower() == 'von neumann':
        return NeighborhoodManager.Von_Neumann(cellSpace)
    else:
        return NeighborhoodManager.randomNeighborhoods(cellSpace)

def SIS(alpha, beta, n_iterations, cellSpace, neighborhoodSystem, impactRates):
    """
    Modelo SIS aplicado sobre el espacio de células
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9,9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace,"moore")
    sis = SIS(0.2,0.5,10,cellSpace,neighborhoodSystem,[1,0])
    sis.data
    --> [array([[ 0.        ,  0.88888889],
                [ 1.        ,  0.67901235],
                [ 2.        ,  0.38271605],
                [ 3.        ,  0.19753086],
                [ 4.        ,  0.09876543],
                [ 5.        ,  0.03703704],
                [ 6.        ,  0.        ],
                [ 7.        ,  0.        ],
                [ 8.        ,  0.        ],
                [ 9.        ,  0.        ],
                [10.        ,  0.        ],
                [11.        ,  0.        ]]),
         array([[ 0.        ,  0.11111111],
                [ 1.        ,  0.32098765],
                [ 2.        ,  0.61728395],
                [ 3.        ,  0.80246914],
                [ 4.        ,  0.90123457],
                [ 5.        ,  0.96296296],
                [ 6.        ,  1.        ],
                [ 7.        ,  1.        ],
                [ 8.        ,  1.        ],
                [ 9.        ,  1.        ],
                [10.        ,  1.        ],
                [11.        ,  1.        ]])]

    sis.evolutions[1].system
    --> array([[1., 1., 0., 0., 0., 0., 0., 0., 0.],
               [1., 1., 0., 0., 0., 1., 0., 0., 0.],
               [1., 1., 0., 0., 0., 1., 1., 0., 0.],
               [1., 1., 0., 0., 0., 1., 0., 0., 0.],
               [1., 0., 0., 0., 0., 0., 0., 0., 0.],
               [0., 1., 1., 1., 0., 0., 0., 0., 0.],
               [1., 0., 1., 1., 1., 0., 0., 0., 0.],
               [0., 0., 1., 1., 1., 0., 0., 0., 1.],
               [0., 0., 1., 0., 0., 0., 0., 0., 1.]])
    """
    modelApply = Models.applyEpidemiologicalModel("sis", alpha, beta, cellSpace, neighborhoodSystem, impactRates)
    modelApply.basicModel(n_iterations)
    return modelApply

def SIR(alpha, beta, n_iterations, cellSpace, neighborhoodSystem, impactRates):
    """
    Modelo SIR aplicado sobre el espacio de células
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9,9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace,"moore")
    sir = SIR(0.2,0.5,10,cellSpace,neighborhoodSystem,[1,0])
    sir.data
    [array([[ 0.        ,  0.90123457],
            [ 1.        ,  0.75308642],
            [ 2.        ,  0.50617284],
            [ 3.        ,  0.2345679 ],
            [ 4.        ,  0.12345679],
            [ 5.        ,  0.08641975],
            [ 6.        ,  0.04938272],
            [ 7.        ,  0.02469136],
            [ 8.        ,  0.        ],
            [ 9.        ,  0.        ],
            [10.        ,  0.        ],
            [11.        ,  0.        ]]),
     array([[ 0.        ,  0.09876543],
            [ 1.        ,  0.22222222],
            [ 2.        ,  0.43209877],
            [ 3.        ,  0.61728395],
            [ 4.        ,  0.62962963],
            [ 5.        ,  0.54320988],
            [ 6.        ,  0.4691358 ],
            [ 7.        ,  0.39506173],
            [ 8.        ,  0.35802469],
            [ 9.        ,  0.28395062],
            [10.        ,  0.2345679 ],
            [11.        ,  0.18518519]]),
     array([[ 0.        ,  0.        ],
            [ 1.        ,  0.02469136],
            [ 2.        ,  0.0617284 ],
            [ 3.        ,  0.14814815],
            [ 4.        ,  0.24691358],
            [ 5.        ,  0.37037037],
            [ 6.        ,  0.48148148],
            [ 7.        ,  0.58024691],
            [ 8.        ,  0.64197531],
            [ 9.        ,  0.71604938],
            [10.        ,  0.7654321 ],
            [11.        ,  0.81481481]])]

    sir.evolutions[4].system
    --> array([[0., 0., 2., 1., 2., 1., 2., 1., 2.],
               [0., 0., 0., 1., 1., 1., 1., 1., 1.],
               [0., 0., 0., 1., 2., 2., 1., 1., 1.],
               [0., 0., 2., 2., 1., 1., 1., 1., 1.],
               [1., 1., 1., 2., 2., 1., 1., 1., 1.],
               [2., 1., 1., 2., 2., 2., 1., 1., 1.],
               [2., 1., 2., 1., 1., 1., 1., 2., 2.],
               [1., 1., 1., 1., 1., 2., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 2., 1.]])
    """
    modelApply = Models.applyEpidemiologicalModel("sir", alpha, beta, cellSpace, neighborhoodSystem, impactRates)
    modelApply.basicModel(n_iterations)
    return modelApply

def SIS_BM(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, annualUnit, n_iterations, cellSpace, neighborhoodSystem, impactRates, systemAges):
    """
    Modelo SIS con natalidad y mortalidad aplicado sobre el espacio de células
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        birthRate(float)  Tasa de natalidad
        probabilityOfDyingByAgeGroup(list)  Lista con las probabilidades de muerte de una célula por rangos de edad
        annualUnit(int)  Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
        systemAges(numpy.ndarray)  Matriz con las edades de cada célula
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
    ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

    sis_bm = SIS_BM(0.2,0.5,0.2,[[0,100,0.0005]],365,20,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
    """
    modelApply = Models.applyEpidemiologicalModel("sis_bm", alpha, beta, cellSpace, neighborhoodSystem, impactRates)
    modelApply.birthRate = birthRate
    modelApply.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
    modelApply.annualUnit = annualUnit
    modelApply.systemAges = systemAges
    modelApply.basicModel(n_iterations)
    return modelApply

def SIR_BM(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, annualUnit, n_iterations, cellSpace, neighborhoodSystem, impactRates, systemAges):
    """
    Modelo SIR con natalidad y mortalidad aplicado sobre el espacio de células
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        birthRate(float)  Tasa de natalidad
        probabilityOfDyingByAgeGroup(list)  Lista con las probabilidades de muerte de una célula por rangos de edad
        annualUnit(int)  Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
        systemAges(numpy.ndarray)  Matriz con las edades de cada célula
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
    ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

    sir_bm = SIR_BM(0.2,0.5,0.2,[[0,100,0.0005]],365,20,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
    """
    modelApply = Models.applyEpidemiologicalModel("sir_bm", alpha, beta, cellSpace, neighborhoodSystem, impactRates)
    modelApply.birthRate = birthRate
    modelApply.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
    modelApply.annualUnit = annualUnit
    modelApply.systemAges = systemAges
    modelApply.basicModel(n_iterations)
    return modelApply

def SIS_DD(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, deathFromDiseaseByAgeRange, annualUnit, n_iterations, cellSpace, neighborhoodSystem, impactRates, systemAges):
    """
    Modelo SIS con muerte por enfermedad aplicado sobre el espacio de células
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        birthRate(float)  Tasa de natalidad
        probabilityOfDyingByAgeGroup(list)  Lista con las probabilidades de muerte de una célula por rangos de edad
        deathFromDiseaseByAgeRange(list)  Lista con las probabilidades de muerte ocasionada por la enfermedad por rango de edad
        annualUnit(int)  Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
        systemAges(numpy.ndarray)  Matriz con las edades de cada célula
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
    ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

    sis_dd = SIS_DD(0.2,0.5,0.2,[[0,100,0.0005]],[[0,100,0.0005]],365,20,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
    """
    modelApply = Models.applyEpidemiologicalModel("sis_dd", alpha, beta, cellSpace, neighborhoodSystem, impactRates)
    modelApply.birthRate = birthRate
    modelApply.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
    modelApply.deathFromDiseaseByAgeRange = deathFromDiseaseByAgeRange
    modelApply.annualUnit = annualUnit
    modelApply.systemAges = systemAges
    modelApply.basicModel(n_iterations)
    return modelApply

def SIR_DD(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, deathFromDiseaseByAgeRange, annualUnit, n_iterations, cellSpace, neighborhoodSystem, impactRates, systemAges):
    """
    Modelo SIR con muerte por enfermedad aplicado sobre el espacio de células
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        birthRate(float)  Tasa de natalidad
        probabilityOfDyingByAgeGroup(list)  Lista con las probabilidades de muerte de una célula por rangos de edad
        deathFromDiseaseByAgeRange(list)  Lista con las probabilidades de muerte ocasionada por la enfermedad por rango de edad
        annualUnit(int)  Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
        systemAges(numpy.ndarray)  Matriz con las edades de cada célula
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
    ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

    sir_dd = SIR_DD(0.2,0.5,0.2,[[0,100,0.0005]],[[0,100,0.0005]],365,20,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
    """
    modelApply = Models.applyEpidemiologicalModel("sir_dd", alpha, beta, cellSpace, neighborhoodSystem, impactRates)
    modelApply.birthRate = birthRate
    modelApply.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
    modelApply.deathFromDiseaseByAgeRange = deathFromDiseaseByAgeRange
    modelApply.annualUnit = annualUnit
    modelApply.systemAges = systemAges
    modelApply.basicModel(n_iterations)
    return modelApply

def medium_SIS(alpha, beta, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates):
    """
    Aplica el modelo SIS una cantidad determinada de veces y calcula sus datos promedio
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        initialPercentageInfected(float)  Porcentage inicial de individuos infectados
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        nSimulations(int)  Cantidad de simulaciones que va a considerar
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
    ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

    medium_sis = medium_SIS(0.2,0.5,0.1,10,3,cellSpace,neighborhoodSystem,[1,0])
    """
    modelApply = Models.applyEpidemiologicalModel_nIterations("sis", alpha, beta, cellSpace, neighborhoodSystem, impactRates, nSimulations, initialPercentageInfected)
    modelApply.basicModel(n_iterations)
    return modelApply

def medium_SIR(alpha, beta, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates):
    """
    Aplica el modelo SIR una cantidad determinada de veces y calcula sus datos promedio
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        initialPercentageInfected(float)  Porcentage inicial de individuos infectados
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        nSimulations(int)  Cantidad de simulaciones que va a considerar
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
    ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

    medium_sir = medium_SIR(0.2,0.5,0.1,10,3,cellSpace,neighborhoodSystem,[1,0])
    """
    modelApply = Models.applyEpidemiologicalModel_nIterations("sir", alpha, beta, cellSpace, neighborhoodSystem, impactRates, nSimulations, initialPercentageInfected)
    modelApply.basicModel(n_iterations)
    return modelApply

def medium_SIS_BM(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, annualUnit, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates, systemAges):
    """
    Aplica el modelo SIS con natalidad y mortalidad una cantidad determinada de veces y calcula sus datos promedio
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        birthRate(float)  Tasa de natalidad
        probabilityOfDyingByAgeGroup(list)  Lista con las probabilidades de muerte de una célula por rangos de edad
        annualUnit(int)  Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
        initialPercentageInfected(float)  Porcentage inicial de individuos infectados
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        nSimulations(int)  Cantidad de simulaciones que va a considerar
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
        systemAges(numpy.ndarray)  Matriz con las edades de cada célula
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
    ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

    medium_sis_bm = medium_SIS_BM(0.2,0.5, 0.2, [[0,100,0.0000005]], 365, 0.1,10,3,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
    """
    modelApply = Models.applyEpidemiologicalModel_nIterations("sis_bm", alpha, beta, cellSpace, neighborhoodSystem, impactRates, nSimulations, initialPercentageInfected)
    modelApply.birthRate = birthRate
    modelApply.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
    modelApply.annualUnit = annualUnit
    modelApply.systemAges = systemAges
    modelApply.basicModel(n_iterations)
    return modelApply

def medium_SIR_BM(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, annualUnit, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates, systemAges):
    """
    Aplica el modelo SIR con natalidad y mortalidad una cantidad determinada de veces y calcula sus datos promedio
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        birthRate(float)  Tasa de natalidad
        probabilityOfDyingByAgeGroup(list)  Lista con las probabilidades de muerte de una célula por rangos de edad
        annualUnit(int)  Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
        initialPercentageInfected(float)  Porcentage inicial de individuos infectados
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        nSimulations(int)  Cantidad de simulaciones que va a considerar
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
        systemAges(numpy.ndarray)  Matriz con las edades de cada célula
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
    ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

    medium_sir_bm = medium_SIR_BM(0.2,0.5, 0.2, [[0,100,0.0000005]], 365, 0.1,10,3,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
    """
    modelApply = Models.applyEpidemiologicalModel_nIterations("sir_bm", alpha, beta, cellSpace, neighborhoodSystem, impactRates, nSimulations, initialPercentageInfected)
    modelApply.birthRate = birthRate
    modelApply.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
    modelApply.annualUnit = annualUnit
    modelApply.systemAges = systemAges
    modelApply.basicModel(n_iterations)
    return modelApply

def medium_SIS_DD(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, deathFromDiseaseByAgeRange, annualUnit, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates, systemAges):
    """
    Aplica el modelo SIS con muerte por enfermead una cantidad determinada de veces y calcula sus datos promedio
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        birthRate(float)  Tasa de natalidad
        probabilityOfDyingByAgeGroup(list)  Lista con las probabilidades de muerte de una célula por rangos de edad
        deathFromDiseaseByAgeRange(list)  Lista con las probabilidades de muerte ocasionada por la enfermedad por rango de edad
        annualUnit(int)  Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
        initialPercentageInfected(float)  Porcentage inicial de individuos infectados
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        nSimulations(int)  Cantidad de simulaciones que va a considerar
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
        systemAges(numpy.ndarray)  Matriz con las edades de cada célula
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
    ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

    medium_sis_dd = medium_SIS_DD(0.2,0.5, 0.2, [[0,100,0.0000005]], [[0,100,0.0000005]],365, 0.1,10,3,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
    """
    modelApply = Models.applyEpidemiologicalModel_nIterations("sis_dd", alpha, beta, cellSpace, neighborhoodSystem, impactRates, nSimulations, initialPercentageInfected)
    modelApply.birthRate = birthRate
    modelApply.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
    modelApply.deathFromDiseaseByAgeRange = deathFromDiseaseByAgeRange
    modelApply.annualUnit = annualUnit
    modelApply.systemAges = systemAges
    modelApply.basicModel(n_iterations)
    return modelApply

def medium_SIR_DD(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, deathFromDiseaseByAgeRange, annualUnit, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates, systemAges):
    """
    Aplica el modelo SIR con muerte por enfermead una cantidad determinada de veces y calcula sus datos promedio
    Parámetros:
        alpha(float)  Tasa de recuperación
        beta(float)  Tasa de infección
        birthRate(float)  Tasa de natalidad
        probabilityOfDyingByAgeGroup(list)  Lista con las probabilidades de muerte de una célula por rangos de edad
        deathFromDiseaseByAgeRange(list)  Lista con las probabilidades de muerte ocasionada por la enfermedad por rango de edad
        annualUnit(int)  Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
        initialPercentageInfected(float)  Porcentage inicial de individuos infectados
        n_iterations(int)  Cantidad de iteraciones en las que se aplica en modelo
        nSimulations(int)  Cantidad de simulaciones que va a considerar
        cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)  Espacio de células
        neighborhoodSystem(list)  Lista con los grados de impacto para cada célula
        impactRates(list)  Tasas de impacto consideradas
        systemAges(numpy.ndarray)  Matriz con las edades de cada célula
    Salidas:
        EpidemiologicalModels.Models.applyEpidemiologicalModel  Contiene toda la información generada al aplicar el modelo

    Ejemplo:
    cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
    neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
    ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

    medium_sir_dd = medium_SIR_DD(0.2,0.5, 0.2, [[0,100,0.0000005]], [[0,100,0.0000005]],365, 0.1,10,3,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
    """
    modelApply = Models.applyEpidemiologicalModel_nIterations("sir_dd", alpha, beta, cellSpace, neighborhoodSystem, impactRates, nSimulations, initialPercentageInfected)
    modelApply.birthRate = birthRate
    modelApply.probabilityOfDyingByAgeGroup = probabilityOfDyingByAgeGroup
    modelApply.deathFromDiseaseByAgeRange = deathFromDiseaseByAgeRange
    modelApply.annualUnit = annualUnit
    modelApply.systemAges = systemAges
    modelApply.basicModel(n_iterations)
    return modelApply