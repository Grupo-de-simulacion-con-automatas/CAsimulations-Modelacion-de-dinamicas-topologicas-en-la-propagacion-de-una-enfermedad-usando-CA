
# CAsimulations: Modelación de las dinámicas de la propagación de una enfermedad usando AC

```CAsimulations``` proporciona una manera de simular fenómenos asociados con la propagación de enfermedades, basándose en modelos SIS, SIR y algunas de sus variaciones implementadas en autómatas celulares en Python. ```CAsimulations``` incluye una gran variedad de utilidades para análisis epidemiológicos tales como la capacidad de definir la condición inicial de frontera del sistema, la condición inicial de dispersión de los individuos infectados, variaciones y comparaciones con respecto al cambio de escala y al cambio de frontera del sistema, variaciones promedio para un número arbitrario de simulaciones, entre otros.

Si desea profundizar sobre los fundamentos detrás de la lógica implementada en la librería, puede dirigirse al [documento principal](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/blob/master/Documentos/Proyecto_de_grado.pdf).

Para importar la librería, ejecute el siguiente comando pip en su entorno de Python:

```pip install -i https://test.pypi.org/simple/ CAsimulation```

Una vez instalada, podemos proceder a cargar la librería, para lo cual tendrá que ejecutar el siguiente script

```from CAsimulation import epidemiologicalModelsInCA as ca```

Con la línea anterior podrá acceder a los módulos que le brindarán la posibilidad de implementar las herramientas descritas en el documento de una manera fácil y rápida. Si desea analizar detalladamente las funciones de la librería, puede dirigirse al [enlace](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/tree/master/Codigo/CAsimulation/casimulation) o implementar los módulos de manera individual.

A continuación presentaremos la documentación de cada uno de los módulos de la librería, si desea consultar ejemplos particulares puede consultar directamente el [documento principal](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/blob/master/Documentos/Proyecto_de_grado.pdf) o los [ejemplos particulares](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/tree/master/Codigo).

Los módulos de la siguiente manera:
1. [AgeManagement](#AgeManagement)
2. [CellManagement](#id2)
3. [CellSpaceConfiguration](#id3)
4. [CompartmentalModelsInEDOS](#id4)
5. [DataManager](#id5)
6. [Models](#id6)
7. [NeighborhoodManager](#id7)
8. [PlotsManager](#id8)
9. [SystemVisualization](#id9)
10. [epidemiologicalModelsInCA](#id10) 

## AgeManagement<a name="AgeManagement"></a>
El módulo```AgeManagement``` se encarga de controlar todos los procesos que tengan que ver con el manejo de las edades de algún conjunto de células, esto en particular para los modelos con natalidad y mortalidad; y los que tienen en cuenta la muerte por enfermedad, ambos descritos en el  [documento principal](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/blob/master/Documentos/Proyecto_de_grado.pdf).

Con este módulo podremos crear a la matriz de edades, dados los rangos y las proporciones de edades en el sistema, y, por otro lado, tenemos a las evoluciones para la matriz de edades descritas en los modelos que implementan esta característica. Para importar este módulo puede usar la siguiente línea:

```from EpidemiologicalModels import AgeManagement as am```

Para usar la clase ```AgesMatrix``` debe establecer inicialmente los rangos de edades y sus proporciones en el sistema, es decir, que porcentaje de los individuos tiene cierto rango de edad; y, por otro lado, será necesario que ya tenga definido un espacio de células. 

```
from EpidemiologicalModels import epidemiologicalModelsInCA as em

# Espacio de células
cellSpace = em.CellSpace(5,5)  # Sistema con 25 células (dim(cellSpace) = 5x5)

# Rangos de edades
ranges = [[0,20,0.5], [21,60,0.25], [61,100,0.25]]  # El 50% tienen entre 0 y 20, el 25% entre 
                                                    # 21 y 60 , y el 25% restante tiene entre 61 y 100

# Matriz de edades
agesMatrix = am.AgesMatrix(ranges, cellSpace)
```
No es necesario utilizar un script adicional, ya que al instanciar la clase ```AgesMatrix``` se genera automáticamente la matriz de edades. Para ver dicha matriz, ejecute el siguiente comando:

```
agesMatrix.agesMatrix
>>> array([[52.,  0., 52., 52., 52.],
           [15., 75., 12.,  8., 41.],
           [ 5.,  7., 10.,  7.,  7.],
           [12., 71.,  5., 52., 74.],
           [16., 24.,  7., 53., 15.]])
```

Una vez tenemos definida la matriz de edades, podremos aplicar las reglas de evolución que tienen en cuenta las edades de las células. En particular nos encontramos con el manejo de edades descrito en la regla para modelos con natalidad y mortalidad, y los modelos con muerte por enfermedad.

Debido a que una de las características de nuestra propuesta es considerar diferentes rangos de edades para aplicar las reglas de evolución que definimos en el documento, debemos ser capaces de identificar a los individuos que poseen cierta edad. Esto lo podremos hacer con la siguiente línea de código:
```
# Parámetros para instanciar la clase AgeMatrixEvolution
birthRate = 0.02
annualUnit = 365
mortabilityRatesByAgeRange = [[1,20,0.05],[21,100,0.025]]
ages = agesMatrix.agesMatrix

ageMatrixManagement = am.AgeMatrixEvolution(ages, birthRate, annualUnit, mortabilityRatesByAgeRange)
ageMatrixManagement.ageGroupPositions(42, 65)  # Coordenadas de células con edades entre 42 y 65 "años"
>>> [[0, 0], [0, 2], [0, 3], [0, 4], [3, 3], [4, 3]]
```
Para aplicar la regla que describe la evolución para la matriz de edades considerando la natalidad y la mortalidad, debemos establecer la iteración sobre la que estamos aplicando el modelo. Si esta iteración es múltiplo de ```annualUnit``` diremos que las células cumplen un ciclo temporal (años, meses, décadas, minutos, etc).  El siguiente script nos muestra la manera adecuada de implementar esta característica:

```
ageMatrixManagement.evolutionRuleForAges(10)
>>> array([[52.,  0., 52., 52., 52.],
           [15., 75., 12.,  8., 41.],
           [ 5.,  7., 10.,  7.,  7.],
           [12., 71.,  5., 52., 74.],
           [16., 24.,  7., 53., 15.]])

ageMatrixManagement.evolutionRuleForAges(365*2)
>>> array([[53.,  1., 53., 53., 53.],
           [16., 76., 13.,  9., 42.],
           [ 6.,  8., 11.,  8.,  8.],
           [13., 72.,  6., 53., 75.],
           [17., 25.,  8., 54., 16.]])
```
Para aplicar la regla que describe la evolución para las edades del sistema de células considerando la muerte por enfermedad podemos ejecutar el siguiente script:
```
cellSpace = cellSpace.initialLocationOfInfected(0.5)  # Suponemos que el 50% de la población posee la enfermedad
cellSpace.system
>>> array([[1., 0., 1., 1., 0.],
           [1., 1., 1., 1., 1.],
           [1., 1., 1., 1., 0.],
           [0., 1., 1., 1., 1.],
           [1., 1., 1., 1., 1.]])
	       
deathByDiseaseRatesByAgeRanges = [[1,50,0.2], [51,100,0.4]]
systemAfterEvolution, agesMatrixAfterEvolution = ageMatrixManagement.deathByDiseaseRule(cellSpace, deadByDiseaseRatesByAgeRanges)
systemAfterEvolution.system
>>> array([[1., 3., 3., 3., 0.],
           [1., 1., 3., 3., 1.],
           [1., 1., 3., 1., 0.],
           [0., 1., 3., 3., 3.],
           [1., 1., 1., 3., 3.]])

agesMatrixAfterEvolution
>>> array([[52.,  0.,  0.,  0., 52.],
           [15., 75.,  0.,  0., 41.],
           [ 5.,  7.,  0.,  7.,  7.],
           [12., 71.,  0.,  0.,  0.],
           [ 0., 24.,  7.,  0.,  0.]])
```

## CellManagement<a name="id2"></a>
Con el módulo ```CellManagement``` podrá darle manejo a propiedades espaciales que le permitan manipular o redefinir la lógica para el comportamiento mismo de las células. Adicionalmente, tendremos la capacidad de acceder a un conjunto de células, vía sus coordenadas, dado un estado específico del modelo. Para importar el módulo ```CellManagement``` puede usar la siguiente línea:

```from CAsimulation.CellManagement import CellManagement as cm```


## CellSpaceConfiguration<a name="id3"></a>
Como su nombre lo indica, el módulo ```CellSpaceConfiguration``` será el encargado de las configuraciones sobre el espacio de células, como por ejemplo, las condiciones iniciales o las condiciones de frontera. Para importar el módulo ```CellSpaceConfiguration``` puede usar la siguiente línea:

```
from CAsimulation.CellSpaceConfiguration import CellSpaceConfiguration as cc
```

## CompartmentalModelsInEDOS<a name="id4"></a>
Con el módulo ```CompartmentalModelsInEDOS```podremos aplicar el método de Euler para ecuaciones diferenciales y visualizar sus soluciones, en nuestro caso lo usaremos para observar los comportamientos descritos por los modelos compartimentales clásicos, sin embargo, el lector puede implementarlo en el contexto sobre el que esté trabajando.

Puede importar esté módulo de la siguiente manera:

```from CAsimulation import CompartmentalModelsInEDOS as ca ```

Antes de empezar a usar este módulo debemos definir el sistema de ecuaciones adecuadamente, como se muestra  a continuación

```
# Parámetros del modelo:
alpha =  0.2
mu = 1/(75*365)
theta = 0.4
beta = 0.5

# Funciones del modelo:
def S_function(values, beta = beta, mu = mu, theta = theta):
    S = values[0]; I = values[1]
    return mu*(1 - S) + (1 - theta)*alpha*I - beta*S*I

def I_function(values, alpha = alpha, beta = beta, mu = mu, theta = theta):
    S = values[0]; I = values[1]
    return beta*S*I - (1 - theta)*alpha*I - mu*I

listOfFunctions = [S_function, I_function]

# Condiciones iniciales:
initialValues = [0.9, 0.1]  # S_0 = 0.9; I_0 = 0.1
```

El módulo ```CompartmentalModelsInEDOS``` permite establecer la cantidad de iteraciones y el valor h empleado en el método de Euler.

```
# Se instancia el módulo
discreteSolutions = ca.CompartmentalModelsInEDOS(listOfFunctions, initialValues)
discreteSolutions.n_iterations(1100)
discreteSolutions.h(0.1)
```

Si desea visualizar los parámetros que está usando en su modelo, puede ejecutar la siguiente línea:

```
discreteSolutions.PrintParameters()
>>> h: 0.1 
    n_iterations: 1100 
    differentialEquations: [<function S_function at 0x7f5462cb14d0>, <function I_function at 0x7f5462cb1200>]
```

Puede obtener las soluciones discretas del sistema que esté trabajando de dos formas: la primera le presenta el conjunto de coordenadas por iteración para estado del modelo; y la segunda le muestra los datos en forma de gráfica, brindándole la posibilidad de acceder a los datos.

```
# Conjunto de datos correspondiente a las soluciones del modelo
discreteSolutions.ModelSolutions()
>>> [[[0.9,
       0.8967003652968036,
       0.8933088972548366,
       0.8898241746599574,
       0.8862448313902722,
       ...],
      [0.1,
       0.10329963470319635,
       0.10669110274516336,
       0.1101758253400425,
       0.11375516860972777,
       ...]],
      range(0, 1100)]

# Gráfica de las soluciones del modelo
nameVariables = ["Susceptibles", "Infectados"]
colorOfVariables = ["yellow", "red"]
discreteSolutions.titlePlot = "Modelo SIS"
discreteSolutions.plotSolutions(nameVariables, colorOfVariables)
```
![Modelo SIS](Codigo/Imagenes/ex1SIS.PNG)

Si desea consultar más ejemplos, puede dirigirse al cuadernillo [Modelos compartimentales clásicos](https://github.com/Grupo-de-simulacion-con-automatas/CAsimulations-Modelacion-de-dinamicas-topologicas-en-la-propagacion-de-una-enfermedad-usando-CA/blob/master/Codigo/1.%20Modelos%20compartimentales%20en%20ecuaciones%20diferenciales.ipynb).

## DataManager<a name="id5"></a>
Este módulo será el encargado de darle manejo a todos los datos que puedan extraerse de las aplicaciones por iteración de cada uno de los modelos descritos en el [documento principal](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/blob/master/Documentos/Proyecto_de_grado.pdf). Para importar el módulo ```DataManager``` puede usar la siguiente línea:

```
from CAsimulation import DataManager as dm
```

## Models<a name="id6"></a>
En el módulo ```Models``` podrá encontrar las reglas definidas en el [documento principal](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/blob/master/Documentos/Proyecto_de_grado.pdf). Para importarlo puede usar el siguiente comando:
```
from CAsimulation import Models as mo
```

## NeighborhoodManager<a name="id7"></a>



## PlotsManager<a name="id8"></a>

## SystemVisualization<a name="id9"></a>

## epidemiologicalModelsInCA<a name="id10"></a>
