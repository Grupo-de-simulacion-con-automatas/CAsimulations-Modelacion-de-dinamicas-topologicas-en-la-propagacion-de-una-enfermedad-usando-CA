import EpidemiologicalModels.AgeManagement as AgeManagement
import EpidemiologicalModels.StateSpaceConfiguration as StateSpaceConfiguration

def createSystemFromDim(nRows, nColumns):
    """
    Genera la configuración básica de un sistema de células a partir de una dimensión establecida.
    Parámetros:
        nRows(int)     Cantidad de filas del sistema
        nColumns(int)  Cantidad de columnas del sistema
    Salidas:
        EpidemiologicalModels.StateSpaceConfiguration.createSpace  Herramientas para configurar la forma básica del sistema.
        
    Ejemplo:
    system = createSystemFromDim(10,10)
    system.initialCondition(0.5)
    
    --> array([[1., 0., 0., 0., 0., 1., 0., 0., 1., 0.],
               [1., 1., 0., 1., 0., 1., 1., 0., 0., 1.],
               [1., 0., 0., 1., 0., 0., 1., 1., 0., 0.],
               [1., 0., 0., 1., 0., 0., 1., 0., 0., 0.],
               [0., 1., 0., 0., 1., 0., 0., 1., 0., 0.],
               [0., 0., 1., 0., 1., 1., 1., 0., 0., 0.],
               [0., 0., 0., 0., 0., 1., 0., 0., 1., 0.],
               [0., 0., 0., 1., 0., 1., 0., 0., 0., 1.],
               [1., 1., 1., 1., 0., 0., 0., 0., 1., 1.],
               [1., 1., 1., 0., 0., 0., 0., 0., 1., 0.]])
    """
    if nRows == 0:
        print("Defina una cantidad de filas distinta de cero.")
        return
    if nColumns == 0:
        print("Defina una cantidad de columnas distinta de cero.")
        return
    return StateSpaceConfiguration.cellManagement(None, nRows, nColumns)

def createSystemFromEmptyArray(emptyArray):
    """
    Genera la configuración básica de un sistema de células a partir de un sistema base.
    Parámetros:
        emptyArray(numpy.ndarray) Sistema base.
    Salidas:
        EpidemiologicalModels.StateSpaceConfiguration.createSpace  Herramientas para configurar la forma básica del sistema.
        
    Ejemplo:
    system = createSystemFromEmptyArray(np.ones((10,10)))
    system.system
    
    --> array([[1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.],
               [1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]])
    """
    if emptyArray.any == None:
        nRows, nColumns = emptyArray.shape
        return createSystemFromDim(nRows, nColumns)
    else:
        return StateSpaceConfiguration.cellManagement(emptyArray)

def createAgeMatrix(ranges, system):
    """
    Crea una matriz con las edades de las células de acuerdon con las probabilidades definidas en ranges.
    Parámetros: 
        ranges(list(list))     Debe contener los rangos de edad y la proporción de individuos del sistema que tendran una edad en el rango.
        system(numpy.ndarray)  Systema de células a las que se les asignará una edad.
    Salidas:
        numpy.ndarray          Arreglo con las edades del sistema de células.
    
    Ejemplo:
    ranges = [[0,10,0.2],[11,100,0.8]]  # 20% tienen entre 0 y 10 años, y 80% tienen entre 11 y 100.
    system = np.zeros((10,10)) 
    createAgeMatrix(ranges, system)
    
    --> array([[ 68.,   2.,  53.,  63.,  51.,  59.,  36.,  38.,  58.,  92.],
               [ 73.,  77.,  73.,  42.,  93.,  58.,  98.,   6.,  72.,  27.],
               [ 70.,  53.,  55.,  14.,  45.,  17.,  38.,  36.,  36.,  27.],
               [ 56.,  35.,  16.,  23.,  12.,  53.,  64.,  36.,  92.,  73.],
               [ 93.,  96.,  45.,  16.,  68.,  22.,  45.,  51., 100.,  88.],
               [ 10.,  71.,  76.,  71.,  55.,  50.,  45.,   3.,   4.,   8.],
               [ 64.,   1.,  94.,  10.,  27.,  13.,  96.,  71.,  67.,  27.],
               [ 96.,   5.,  71.,  51.,  90., 100.,  84.,  35.,  95.,  97.],
               [ 22.,   3.,  19.,  65.,  88.,  23.,  51.,  34.,  97.,   8.],
               [  1.,  35.,  98.,  96.,  76.,  58.,   2.,  19.,   2.,  55.]])
    """
    if len(ranges) == 0:
        print("Debe definir los rangos de edades en el sistema.")
        return
    else:
        for r in ranges:
            if len(ranges != 3):
                print("Asegurese de que todos los rangos de edad posean límite inferior, límite superior y la proporción en el sistema.")
                return
            elif r[2] > 1:
                print("Asegurese de que todas las proporciones sean menores o iguales a 1.")
    return AgeManagement.AgesMatrix(ranges, system).create()

def defineBoundaryConditions(basicArray, rectangleRows, rectangleColumns, rowPosition, columnPosition):
    """
    Permite definir una condición inicial sobre la ubicación de las células a partir de regiones rectangulares.
    Parámetros:
        basicArray(numpy.ndarray)  Arreglo sobre el cual se va a definir la región rectangular.
        rectangleRows(int)         Cantidad de filas del rectangulo.
        rectangleColumns(int)      Cantidad de columnas del rectangulo.
        rowPosition(int)           Fila desde donde iniciará la región rectangular.
        columnPosition(int)        Columna desde donde iniciará la región rectangular.
    Salidas:
        numpy.ndarray  Arreglo con la nueva región.
        
    Ejemplo:
    basicArray = -np.ones((5,5))
    system = defineBoundaryConditions(basicArray,3,3,0,0)
    system
    
    --> array([[-1., -1., -1., -1., -1.],
               [-1.,  0.,  0.,  0.,  0.],
               [-1.,  0.,  0.,  0.,  0.],
               [-1.,  0.,  0.,  0.,  0.],
               [-1., -1., -1., -1., -1.]])
    """
    if rectangleRows == None or rectangleRows == 0:
        print("Debe definir una cantidad de filas para el rectángulo.")
        return
    if rectangleColumns == None or rectangleColumns == 0:
        print("Debe definir una cantidad de columnas para el rectángulo.")
        return
    if rowPosition == None:
        print("Debe establecer la fila desde donde se generará la región rectángular.")
        return
    if columnPosition == None:
        print("Debe establecer la columna desde donde se generará la región rectángular.")
        return
    return StateSpaceConfiguration.boundaryConditions(basicArray).rectangularBoundary(rectangleRows, rectangleColumns, rowPosition, columnPosition)