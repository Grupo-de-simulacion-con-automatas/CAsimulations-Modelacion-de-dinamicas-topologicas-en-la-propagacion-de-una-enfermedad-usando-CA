# CAsimulations

Para importar la librería, ejecute el siguiente script
~~~
 from EpidemiologicalModels.epidemiologicalModelsInCA import * 
 ~~~
## El espacio de células

### CellSpace(nRows, nColumns, xnRows, xnColumns, unRows, unColumns)

Genera la configuración básica de un sistema de células
**Parámetros:**
* **nRows(int)**     Filas de la región interna inicial del sistema / filas del sistema
* **nColumns(int)**  Columnas de la región interna inicial del sistema / Columnas del sistema
* **xnRows(int)**    Fila donde se ubica la región interna inicial
* **xnColumns(int)**  Columna donde se ubica la región interna inicial
* **unRows(int)**    Filas del área externa
* **unColumns(int)** Columnas del área externa

**Salida:**
* **EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration**  Sistema de células

**Ejemplo 1:**
~~~
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
~~~
**Ejemplo 2:**
~~~
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
~~~
**Ejemplo 3:**
~~~
space = CellSpace(3,1,5,5,1,2)
space.system
--> array([[-1., -1., -1., -1., -1.],
           [-1., -1.,  0., -1., -1.],
           [-1., -1.,  0., -1., -1.],
           [-1., -1.,  0., -1., -1.],
           [-1., -1., -1., -1., -1.]])
~~~
### CreateAgeMatrix(ranges, cellSpace)
Crea una matriz con las edades de las células de acuerdon con las probabilidades definidas en ranges.
**Parámetros:**
* **ranges(list(list))**  Debe contener los rangos de edad y la proporción de individuos del sistema que tendran una edad en el rango.
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)**  Systema de células a las que se les asignará una edad.

**Salidas:**
* **numpy.ndarray ** Arreglo con las edades del sistema de células.
    
**Ejemplo:**
~~~
ranges = [[0,10,0.2],[11,100,0.8]]  # 20% tienen entre 0 y 10 años, y 80% tienen entre 11 y 100.
space = CellSpace(5,5)
createAgeMatrix(ranges, space)
    
--> array([[ 1., 81., 33.,  5., 18.],
           [90., 19., 18., 36., 50.],
           [ 5., 67.,  4., 18., 74.],
           [45., 36.,  4., 36.,  4.],
           [ 5., 67., 74.,  1.,  1.]])
~~~
### GenerateNeighborhoodSystem(cellSpace, neighborhoodType)
Genera un conjunto de vecindades básico para aplicar los modelos epidemiológicos
**Parámetros:**
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)**  Sistema de células para el cuál se definirá el sistema de vecindades
* **neighborhoodType(string)**  Configuración del sistema - Valores permitidos (Moore - Von Neumann), por defecto se genera un sistema con valores aleatorios

**Salidas:**
* **list**  Lista con los arreglos que describen el conjunto de vecindades y las coordenadas de cada célula

**Ejemplo 1:**
~~~
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
~~~
**Ejemplo 2:**
~~~
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
~~~
## Modelos epidemiológicos
### SIS(alpha, beta, n_iterations, cellSpace, neighborhoodSystem, impactRates)
Modelo SIS aplicado sobre el espacio de células
**Parámetros:**
* **alpha(float)**  Tasa de recuperación
* **beta(float)** Tasa de infección
* **n_iterations(int)**  Cantidad de iteraciones en las que se aplica en modelo
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)**  Espacio de células
* **neighborhoodSystem(list)**  Lista con los grados de impacto para cada célula
* **impactRates(list)**  Tasas de impacto consideradas
    
**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9,9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace,"moore")

sis = SIS(0.2,0.5,10,cellSpace,neighborhoodSystem,[1,0])
~~~

### SIR(alpha, beta, n_iterations, cellSpace, neighborhoodSystem, impactRates):
Modelo SIR aplicado sobre el espacio de células
**Parámetros:**
* **alpha(float)**  Tasa de recuperación
* **beta(float)**  Tasa de infección
* **n_iterations(int)**  Cantidad de iteraciones en las que se aplica en modelo
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)**  Espacio de células
* **neighborhoodSystem(list)**  Lista con los grados de impacto para cada célula
* **impactRates(list)**  Tasas de impacto consideradas
    
**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel**  Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9,9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace,"moore")

sir = SIR(0.2,0.5,10,cellSpace,neighborhoodSystem,[1,0])
~~~
### SIS_BM(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, annualUnit, n_iterations, cellSpace, neighborhoodSystem, impactRates, systemAges)
Modelo SIS con natalidad y mortalidad aplicado sobre el espacio de células
**Parámetros:**
* **alpha(float)** Tasa de recuperación
* **beta(float)** Tasa de infección
* **birthRate(float)** Tasa de natalidad
* **probabilityOfDyingByAgeGroup(list)** Lista con las probabilidades de muerte de una célula por rangos de edad
* **annualUnit(int)** Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
* **n_iterations(int)** Cantidad de iteraciones en las que se aplica en modelo
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)** Espacio de células
* **neighborhoodSystem(list)** Lista con los grados de impacto para cada célula
* **impactRates(list)** Tasas de impacto consideradas
* **systemAges(numpy.ndarray)** Matriz con las edades de cada célula

**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

sis_bm = SIS_BM(0.2,0.5,0.2,[[0,100,0.0005]],365,20,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
~~~
### SIR_BM(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, annualUnit, n_iterations, cellSpace, neighborhoodSystem, impactRates, systemAges)
Modelo SIR con natalidad y mortalidad aplicado sobre el espacio de células
**Parámetros:**
* **alpha(float)** Tasa de recuperación
* **beta(float)** Tasa de infección
* **birthRate(float)** Tasa de natalidad
* **probabilityOfDyingByAgeGroup(list)** Lista con las probabilidades de muerte de una célula por rangos de edad
* **annualUnit(int)** Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
* **n_iterations(int)** Cantidad de iteraciones en las que se aplica en modelo
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)** Espacio de células
* **neighborhoodSystem(list)** Lista con los grados de impacto para cada célula
* **impactRates(list)** Tasas de impacto consideradas
* **systemAges(numpy.ndarray)** Matriz con las edades de cada célula

**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

sir_bm = SIR_BM(0.2,0.5,0.2,[[0,100,0.0005]],365,20,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
~~~
### SIS_DD(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, deathFromDiseaseByAgeRange, annualUnit, n_iterations, cellSpace, neighborhoodSystem, impactRates, systemAges)
Modelo SIS con muerte por enfermedad aplicado sobre el espacio de células
**Parámetros:**
* **alpha(float)** Tasa de recuperación
* **beta(float)** Tasa de infección
* **birthRate(float)** Tasa de natalidad
* **probabilityOfDyingByAgeGroup(list)** Lista con las probabilidades de muerte de una célula por rangos de edad
* **deathFromDiseaseByAgeRange(list)** Lista con las probabilidades de muerte ocasionada por la enfermedad por rango de edad
* **annualUnit(int)** Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
* **n_iterations(int)** Cantidad de iteraciones en las que se aplica en modelo
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)** Espacio de células
* **neighborhoodSystem(list)** Lista con los grados de impacto para cada célula
* **impactRates(list)** Tasas de impacto consideradas
* **systemAges(numpy.ndarray)** Matriz con las edades de cada célula

**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

sis_dd = SIS_DD(0.2,0.5,0.2,[[0,100,0.0005]],[[0,100,0.0005]],365,20,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
~~~
### SIR_DD(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, deathFromDiseaseByAgeRange, annualUnit, n_iterations, cellSpace, neighborhoodSystem, impactRates, systemAges)
Modelo SIR con muerte por enfermedad aplicado sobre el espacio de células
**Parámetros:**
* **alpha(float)** Tasa de recuperación
* **beta(float)** Tasa de infección
* **birthRate(float)** Tasa de natalidad
* **probabilityOfDyingByAgeGroup(list)** Lista con las probabilidades de muerte de una célula por rangos de edad
* **deathFromDiseaseByAgeRange(list)** Lista con las probabilidades de muerte ocasionada por la enfermedad por rango de edad
* **annualUnit(int)** Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
* **n_iterations(int)** Cantidad de iteraciones en las que se aplica en modelo
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)** Espacio de células
* **neighborhoodSystem(list)** Lista con los grados de impacto para cada célula
* **impactRates(list)** Tasas de impacto consideradas
* **systemAges(numpy.ndarray)** Matriz con las edades de cada célula

**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

sir_dd = SIR_DD(0.2,0.5,0.2,[[0,100,0.0005]],[[0,100,0.0005]],365,20,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
~~~

### medium_SIS(alpha, beta, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates)
Aplica el modelo SIS una cantidad determinada de veces y calcula sus datos promedio
**Parámetros:**
* **alpha(float)** Tasa de recuperación
* **beta(float)** Tasa de infección
* **initialPercentageInfected(float)** Porcentage inicial de individuos infectados
* **n_iterations(int)** Cantidad de iteraciones en las que se aplica en modelo
* **nSimulations(int)** Cantidad de simulaciones que va a considerar
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)** Espacio de células
* **neighborhoodSystem(list)** Lista con los grados de impacto para cada célula
* **impactRates(list)** Tasas de impacto consideradas

**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

medium_sis = medium_SIS(0.2,0.5,0.1,10,3,cellSpace,neighborhoodSystem,[1,0])
~~~
### medium_SIR(alpha, beta, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates)
Aplica el modelo SIR una cantidad determinada de veces y calcula sus datos promedio
**Parámetros:**
* **alpha(float)** Tasa de recuperación
* **beta(float)** Tasa de infección
* **initialPercentageInfected(float)** Porcentage inicial de individuos infectados
* **n_iterations(int)** Cantidad de iteraciones en las que se aplica en modelo
* **nSimulations(int)** Cantidad de simulaciones que va a considerar
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)** Espacio de células
* **neighborhoodSystem(list)** Lista con los grados de impacto para cada célula
* **impactRates(list)** Tasas de impacto consideradas

**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

medium_sir = medium_SIR(0.2,0.5,0.1,10,3,cellSpace,neighborhoodSystem,[1,0])
~~~
### medium_SIS_BM(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, annualUnit, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates, systemAges) 
Aplica el modelo SIS con natalidad y mortalidad una cantidad determinada de veces y calcula sus datos promedio
**Parámetros:**
* **alpha(float)** Tasa de recuperación
* **beta(float)** Tasa de infección
* **birthRate(float)** Tasa de natalidad
* **probabilityOfDyingByAgeGroup(list)** Lista con las probabilidades de muerte de una célula por rangos de edad
* **annualUnit(int)** Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
* **initialPercentageInfected(float)** Porcentage inicial de individuos infectados
* **n_iterations(int)** Cantidad de iteraciones en las que se aplica en modelo
* **nSimulations(int)** Cantidad de simulaciones que va a considerar
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)** Espacio de células
* **neighborhoodSystem(list)** Lista con los grados de impacto para cada célula
* **impactRates(list)** Tasas de impacto consideradas
* **systemAges(numpy.ndarray)** Matriz con las edades de cada célula

**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

medium_sis_bm = medium_SIS_BM(0.2,0.5, 0.2, [[0,100,0.0000005]], 365, 0.1,10,3,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
~~~
### medium_SIR_BM(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, annualUnit, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates, systemAges) 
Aplica el modelo SIR con natalidad y mortalidad una cantidad determinada de veces y calcula sus datos promedio
**Parámetros:**
* **alpha(float)** Tasa de recuperación
* **beta(float)** Tasa de infección
* **birthRate(float)** Tasa de natalidad
* **probabilityOfDyingByAgeGroup(list)** Lista con las probabilidades de muerte de una célula por rangos de edad
* **annualUnit(int)** Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
* **initialPercentageInfected(float)** Porcentage inicial de individuos infectados
* **n_iterations(int)** Cantidad de iteraciones en las que se aplica en modelo
* **nSimulations(int)** Cantidad de simulaciones que va a considerar
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)** Espacio de células
* **neighborhoodSystem(list)** Lista con los grados de impacto para cada célula
* **impactRates(list)** Tasas de impacto consideradas
* **systemAges(numpy.ndarray)** Matriz con las edades de cada célula

**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

medium_sir_bm = medium_SIR_BM(0.2,0.5, 0.2, [[0,100,0.0000005]], 365, 0.1,10,3,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
~~~
### medium_SIS_DD(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, deathFromDiseaseByAgeRange, annualUnit, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates, systemAges)
Aplica el modelo SIS con muerte por enfermead una cantidad determinada de veces y calcula sus datos promedio
**Parámetros:**
* **alpha(float)** Tasa de recuperación
* **beta(float)** Tasa de infección
* **birthRate(float)** Tasa de natalidad
* **probabilityOfDyingByAgeGroup(list)** Lista con las probabilidades de muerte de una célula por rangos de edad
* **deathFromDiseaseByAgeRange(list)** Lista con las probabilidades de muerte ocasionada por la enfermedad por rango de edad
* **annualUnit(int)** Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
* **initialPercentageInfected(float)** Porcentage inicial de individuos infectados
* **n_iterations(int)** Cantidad de iteraciones en las que se aplica en modelo
* **nSimulations(int)** Cantidad de simulaciones que va a considerar
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)** Espacio de células
* **neighborhoodSystem(list)** Lista con los grados de impacto para cada célula
* **impactRates(list)** Tasas de impacto consideradas
* **systemAges(numpy.ndarray)** Matriz con las edades de cada célula

**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

medium_sis_dd = medium_SIS_DD(0.2,0.5, 0.2, [[0,100,0.0000005]], [[0,100,0.0000005]],365, 0.1,10,3,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
~~~
### medium_SIR_DD(alpha, beta, birthRate, probabilityOfDyingByAgeGroup, deathFromDiseaseByAgeRange, annualUnit, initialPercentageInfected, n_iterations, nSimulations, cellSpace, neighborhoodSystem, impactRates, systemAges)
Aplica el modelo SIR con muerte por enfermead una cantidad determinada de veces y calcula sus datos promedio
**Parámetros:**
* **alpha(float)** Tasa de recuperación
* **beta(float)** Tasa de infección
* **birthRate(float)** Tasa de natalidad
* **probabilityOfDyingByAgeGroup(list)** Lista con las probabilidades de muerte de una célula por rangos de edad
* **deathFromDiseaseByAgeRange(list)** Lista con las probabilidades de muerte ocasionada por la enfermedad por rango de edad
* **annualUnit(int)** Unidad que se toma como base para un ciclo (se puede entender como un año de 365 días)
* **initialPercentageInfected(float)** Porcentage inicial de individuos infectados
* **n_iterations(int)** Cantidad de iteraciones en las que se aplica en modelo
* **nSimulations(int)** Cantidad de simulaciones que va a considerar
* **cellSpace(EpidemiologicalModels.CellSpaceConfiguration.CellSpaceConfiguration)** Espacio de células
* **neighborhoodSystem(list)** Lista con los grados de impacto para cada célula
* **impactRates(list)** Tasas de impacto consideradas
* **systemAges(numpy.ndarray)** Matriz con las edades de cada célula

**Salidas:**
* **EpidemiologicalModels.Models.applyEpidemiologicalModel** Contiene toda la información generada al aplicar el modelo

**Ejemplo:**
~~~
cellSpace = CellSpace(9, 9).initialLocationOfInfected(0.1)
neighborhoodSystem = GenerateNeighborhoodSystem(cellSpace, "moore")
ageMatrix = CreateAgeMatrix([[0,100,1]], cellSpace)

medium_sir_dd = medium_SIR_DD(0.2,0.5, 0.2, [[0,100,0.0000005]], [[0,100,0.0000005]],365, 0.1,10,3,cellSpace,neighborhoodSystem,[1,0],ageMatrix)
~~~