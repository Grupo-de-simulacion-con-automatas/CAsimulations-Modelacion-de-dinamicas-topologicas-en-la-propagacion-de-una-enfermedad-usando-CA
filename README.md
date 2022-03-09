# CAsimulations: Modelación de las dinámicas de la propagación de una enfermedad usando AC

```CAsimulations``` proporciona una manera de simular fenómenos asociados con la propagación de enfermedades, basándose en modelos SIS, SIR y algunas de sus variaciones implementadas en autómatas celulares en Python. ```CAsimulations``` incluye una gran variedad de utilidades para análisis epidemiológicos tales como la capacidad de definir la condición inicial de frontera del sistema, la condición inicial de dispersión de los individuos infectados, variaciones y comparaciones con respecto al cambio de escala y al cambio de frontera del sistema, variaciones promedio para un número arbitrario de simulaciones, entre otros.

Si desea profundizar sobre los fundamentos detrás de la lógica implementada en la librería, puede dirigirse al [documento principal](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/blob/master/Documentos/Proyecto_de_grado.pdf).

Para importar la librería, ejecute el siguiente comando pip en su entorno de Python:

```pip install -i https://test.pypi.org/simple/ CAsimulation```

Una vez instalada, podemos proceder a cargar la librería, para lo cual tendrá que ejecutar el siguiente script

```from CAsimulation import epidemiologicalModelsInCA as ca```

Con la línea anterior podrá acceder a los módulos que le brindarán la posibilidad de implementar las herramientas descritas en el documento de una manera fácil y rápida. Si desea analizar detalladamente las funciones de la librería, puede dirigirse al [enlace](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/tree/master/Codigo/CAsimulation/casimulation) o implementar los módulos de manera individual.

A continuación presentaremos la documentación de cada uno de los módulos de la librería, si desea consultar ejemplos particulares puede consultar directamente el [documento principal](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/blob/master/Documentos/Proyecto_de_grado.pdf) o los [ejemplos particulares](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/tree/master/Codigo).

## AgeManagement

## CellManagement

## CellSpaceConfiguration

## CompartmentalModelsInEDOS
Con este módulo podremos aplicar el método de Euler para ecuaciones diferenciales y visualizar sus soluciones, en nuestro caso lo usaremos para observar los comportamientos descritos por los modelos compartimentales clásicos, sin embargo, el lector puede implementarlo en el contexto sobre el que esté trabajando.

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

El módulo ```CompartmentalModelsInEDOS``` permite establecer la cantidad de iteraciones y el valor $h$ usado en el método de Euler.

```
# Se instancia el módulo
discreteSolutions = ca.CompartmentalModelsInEDOS(listOfFunctions, initialValues)
discreteSolutions.n_iterations(1100)
discreteSolutions.h(0.1)
```

Si desea visualizar los parámetros que está usando en su modelo, puede ejecutar la siguiente linea:

```
discreteSolutions.PrintParameters()
>>> h: 0.1 
    n_iterations: 1100 
    differentialEquations: [<function S_function at 0x7f5462cb14d0>, <function I_function at 0x7f5462cb1200>]
```

Puede obtener las soluciones discretas del sistema que esté trabajando de dos formas: la primera le presenta el conjunto de coordenadas por iteración para estado del modelo; y la segunda le muestra los datos en forma de gráfica brindandole la posibilidad de acceder a los datos.

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

## DataManager

## Models

## NeighborhoodManager

## PlotsManager

## SystemVisualization

## epidemiologicalModelsInCA
