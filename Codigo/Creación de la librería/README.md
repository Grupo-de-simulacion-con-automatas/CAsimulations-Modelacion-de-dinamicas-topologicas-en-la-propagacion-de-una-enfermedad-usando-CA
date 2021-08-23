# Actualizaciones sobre la última versión de CAsimulations

## CompartimentalModelsInEDOS

|Función|Parámetros|Descripción|
|---|---|---|
|n_iterations|valueForn_iterations|Define la cantidad de iteraciones. Por defecto es igual a 1|
|ModelSolutions||Devuelve una lista con las soluciones discretas luego de aplicar el método de Euler|
|plotSolutions|Nombres, colores de las variables, límite explícito (false), legenda (true)|Gráfica de las soluciones|
|PrintParameters||Imprime los parámetros que se  están usando|

## DefineSpaceInCA
|Versión actual|Actualización|Descripción|
|---|---|---|
||Moore|Definición de la vecindad de Moore|
||Von_Neumann|Definición de la vecindad de Von Neumann|
||Identificador|Reconoce la función de vecindad como la vecindad del agente en la posición $ij$ en el sistema|
||insideCopy|Copia del sistema en un entorno extendido|
|state_coor|stateCoordinates|Enlista los agentes que tengan un estado específico|
|num_I, num_R|statePercentageInSpace|Porcentaje de individuos con el estado en el espacio (a de cada b tienen el estado)|
|initial_condition|initialCondition|Condición inicial aplicada al sistema|
|northwest, north, northeast, west, center, east, southwest, south, southeast, aleatorio|initialLocation|Ubicación inicial de infectados|
|boundary|boundaryDefinition|Definición de la estructura del sistema dadas las condiciones de frontera|
|domain_definition|rectangularBoundary|Ubica una matriz nula de tamaño rectangleRows*rectangleColumns en la posición a,b del sistema|
|color|color|Transformación que permite visualizar el sistema a color|
## epidemiologicalModels
|Versión actual|Actualización|Descripción|
|---|---|---|
|SIS_model, SIR_model, SIS_bm_model, SIR_bm_model, SIS_dd_model, SIR_dd_model|basicModel|Aplica el modelo n_iterations veces|
||metricsPlot|Gráfica la evolución de los estados en n_iterations|
||evolutionsPlot|Gráfica una evolución especifica del conjunto de evoluciones generadas tras aplicar el modelo|
|medium_curves_sis, medium_curves_sir, medium_curves_sir_dd|mediumCurves|Curvas promedio del modelo|
|heatmap_sis, heatmap_sir_I, heatmap_sir_R|heatmap|Mapa de calor para la población infectada (SIR_Model[6])|
## models
|Versión actual|Actualización|Descripción|
|---|---|---|
|base_rule|baseRuleEvolution|Regla totalística que describe el cambio entre los estados S e I de manera local|
|evolution_sis|sis.basicRule|Aplica la regla base de evolución al sistema updateSystem|
|evolution_sir|sir.basicRule|Aplica la regla de evolución al sistema previousSystem|
|ages|agesMatrix|Arreglo de edades aleatorias|
|age_group|ageGroupPositions|Genera las posiciones de los individuos que tienen entre minAge y maxAge años en el sistema|
|evolution_ages|newYear|Nuevo año para los agentes|
|evolution_sis_bm, evolution_sir_bm|birthAndMortavility.basicRule|Aplica la regla base de evolución al sistema updateSystem|
|dead_by_disease|deathByDiseaseRule|Aplica probabilidades de muerte por enfermedad a grupos de edad sobre el sistema|
|evolution_sis_dd, evolution_sir_dd|deathByDisease.basicRule|Aplica la regla base de evolución al sistema updateSystem|

## tools
|Versión actual|Actualización|Descripción|
|---|---|---|
|spline3|spline3|spline cubico para la lista de coordenadas|
||graficas|Gráfica del spline cúbico|
|sumaS, sumaI, sumaR, sumaV, count_S, count_I, count_R, count_D, count_s, count_i, count_r, count_d|statusInTheSystem|Lista con las cantidades de individuos por cada estado|
|num_individuals|numberOfIndividuals|Cantidad de individuos en el sistema|
||dataVisualization|Separa los tipos de datos en 3 grupos: duplas, valores y estados del sistema|
|evolution_SIS, evolution_SIR, evolution_SIS_bm, evolution_SIR_bm, evolution_SIS_dd, evolution_SIR_dd|appliedModel|Aplica el modelo 'modelFunction' una cantidad nIterations de veces|
||mediumData|Organiza la información de cada simulación|
|medium_curves_sis_dd|appliedMediumData|Aplica el modelo epidemiológico en n_simulations|
|scale_differences|variationsBetweenScales|Genera una lista con las diferencias entre escalas|
## Paso de funciones públicas a funciones privadas

|Versión actual|Actualización|Descripción|
|---|---|---|
|interaction_SI|__siRule|Regla de interacción del estado S|
|interaction_IR|__irRule|Regla de interacción del estado I|