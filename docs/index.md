# CAsimulations: Modelación de dinámicas topológicas en la propagación de una enfermedad usando autómatas celulares

```CAsimulations``` proporciona una manera de simular fenómenos asociados con la propagación de enfermedades, basándose en modelos SIS, SIR y algunas de sus variaciones implementadas en autómatas celulares en Python. ```CAsimulations``` incluye una gran variedad de utilidades para análisis epidemiológicos tales como la capacidad de definir la condición inicial de frontera del sistema, la condición inicial de dispersión de los individuos infectados, variaciones y comparaciones con respecto al cambio de escala y al cambio de frontera del sistema, variaciones promedio para un número arbitrario de simulaciones, entre otros.

Si desea profundizar sobre los fundamentos detrás de la lógica implementada en la librería, puede dirigirse al [documento principal](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/blob/master/Documentos/Proyecto_de_grado.pdf).

Para importar la librería, ejecute el siguiente comando pip en su entorno de Python:

```pip install -i https://test.pypi.org/simple/ CAsimulation```

Una vez instalada, podemos proceder a cargar la librería, para lo cual tendrá que ejecutar el siguiente script

```from CAsimulation import epidemiologicalModelsInCA as ca```

Con la línea anterior podrá acceder a los módulos que le brindarán la posibilidad de implementar las herramientas descritas en el documento de una manera fácil y rápida. Si desea analizar detalladamente las funciones de la librería, puede dirigirse al [enlace](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/tree/master/Codigo/CAsimulation/casimulation) o implementar los módulos de manera individual.

A continuación presentaremos la documentación de cada uno de los módulos de la librería, si desea consultar ejemplos particulares puede consultar directamente el [documento principal](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/blob/master/Documentos/Proyecto_de_grado.pdf) o los [ejemplos particulares](https://github.com/Grupo-de-simulacion-con-automatas/Prediccion-del-comportamiento-de-una-enfermedad-simulada-en-AC-con-un-algoritmo-en-RN/tree/master/Codigo).

## CompartmentalModelsInEDOS
Este módulo permite visualizar las soluciones para un sistema de ecuaciones cualquiera, en nuestro caso lo usaremos para observar los comportamientos descritos por los modelos compartimentales clásicos, sin embargo, el lector puede usar este módulo en el contexto sobre el que esté trabajando.

Puede importar esté módulo de dos maneras: la primera es haciéndolo directamente con siguiente comando:

```from CAsimulation import CompartmentalModelsInEDOS as ca ```

La segunda forma de hacerlo es a través del módulo ```epidemiologicalModelsInCA``` con el comando

```from CAsimulation.epidemiologicalModelsInCA import CompartmentalModelsInEDOS as ca```

