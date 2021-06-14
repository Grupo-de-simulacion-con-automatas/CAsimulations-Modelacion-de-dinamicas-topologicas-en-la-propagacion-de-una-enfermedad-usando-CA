# Proyecto de Grado

## Actualización

Versión final del anteproyecto
Actualización del código hasta antes de la implementación del movimiento

## Próximas tareas

Respuesta por parte del comite
Implementar clases

# Informe de actualización de funciones

Lista con las actualizaciones realizadas y verificadas:

| Commit 0       |Actualización                  |Descripción                  |
|----------------|-------------------------------|-----------------------------|
|sumaS|susceptibleInTheNeighborhood|Cantidad de individuos susceptibles en la vecindad|
|sumaI|infectedInTheNeighborhood|Cantidad de individuos infectados en la vecindad|
|sumaR|recoveredInTheNeighborhood|Cantidad de individuos infectados en la vecindad|
|sumaV|holesInTheNeighborhood|Cantidad de espacios vacios en la vecindad|
|count_S|susceptibleInTheSystem|Cantidad de individuos susceptibles en el sistema|
|count_I|infectedInTheSystem|Cantidad de individuos infectados en el sistema|
|count_R|recoveredInTheSystem|Cantidad de individuos recuperados en el sistema|
|count_D|deadInTheSystem|Cantidad de individuos fallecidos en el sistema|
|num_individuals|numberOfIndividuals|Cantidad de individuos que interactuan en el sistema|
|count_s|susceptiblePercentage|Porcentaje de susceptibles en el sistema|
|count_i|infectedPercentage|Porcentaje de infectados en el sistema|
|count_r|recoveredPercentage|Porcentaje de recuperados en el sistema|
|count_d|deadPercentage|Porcentaje de fallecidos en el sistema|
|base_rule|baseRuleEvolution|Regla totalística que describe el cambio entre los estados S e I de manera local|
|evolution_sis|SIS_Rule|Regla base de evolucion aplicada en el sistema|
|evolution_SIS|SIS_Applied|Aplica el modelo SIS una cantidad n de veces|
|SIS_model|SIS_Model|Reporta los datos luego de aplicar el modelo SIS n veces|
|state_coor|stateCoordinates|Enlista los agentes que tengan un estado especifico|
|num_I|infectedPercentageInSpace|Porcentaje de infectados en el espacio (a de cada b están infectados)|
|initial_condition|initialCondition|Condición inicial aplicada al sistema|
|northwest|initialLocation(position = "northwest")|ubicación inicial de infectados|
|north|initialLocation(position = "north")|ubicación inicial de infectados|
|northeast|initialLocation(position = "northeast")|ubicación inicial de infectados|
|west|initialLocation(position = "west")|ubicación inicial de infectados|
|center|initialLocation(position = "center")|ubicación inicial de infectados|
|east|initialLocation(position = "east")|ubicación inicial de infectados|
|southwest|initialLocation(position = "southwest")|ubicación inicial de infectados|
|south|initialLocation(position = "south")|ubicación inicial de infectados|
|southeast|initialLocation(position = "southeast")|ubicación inicial de infectados|
|aleatorio|initialLocation(position = "random")|ubicación inicial de infectados|
|heatmap_sis|SIS_Heatmap|Mapa de calor de la enfermedad dados los datos luego de aplicar el modelo SIS n veces sobre un sistema|
|interaction_SI|SI_rule|Regla de interacción del estado S|
|num_R|recoveredPercentageInSpace|Porcentaje de recuperados en el espacio (a de cada b están curados)|
|interaction_IR|IR_rule|Regla de interacción del estado I|
|evolution_sir|SIR_Rule|Regla de comportamiento SIR|
|evolution_SIR|SIR_Applied|Lista de evoluciones al aplicar SIR n veces|
|SIR_model|SIR_Model|Modelo SIR|
|heatmap_sir_I|SIR_Heatmap_I|Mapa de calor para la población infectada (SIR_Model[6])|
|heatmap_sir_R|SIR_Heatmap_R|Mapa de calor para la población recuperada (SIR_Model[6])|
|medium_curves_sis|SIS_MediumCurves|Promedio de n simulaciones para el modelo SIS|
|medium_curves_sir|SIR_MediumCurves|Promedio de n simulaciones para el modelo SIR|
|boundary|boundaryDefinition|Definición de la estructura del sistema dadas las condiciones de frontera|
|domain_definition|rectangularBoundary|Ubica una matriz nula de tamaño rectangleRows*rectangleColumns en la posición a,b del sistema|
|scale_differences|variationsBetweenScales|Genera una lista con las diferencias entre escalas|
|ages|agesMatrix|Arreglo de edades aleatorias|
|age_group|ageGroupPositions|Genera las posiciones de los individuos que tienen entre minAge y maxAge años en el sistema|
|evolution_ages|newYear|Nuevo año para los agentes|
|evolution_sis_bm|SIS_Rule_birthAndMortavility|Regla de evolución del modelo SIS con natalidad y mortalidad|
|evolution_SIS_bm|SIS_Applied_birthAndMortavility|Aplica el modelo SIS con natalidad y mortalidad n_iterations veces sobre el sistema|
|SIS_bm_model|SIS_Model_birthAndMortavility|Reporta los datos luego de aplicar el modelo SIS con natalidad y mortalidad n veces|
|evolution_sir_bm|SIR_Rule_birthAndMortavility|Regla de evolución del modelo SIR con natalidad y mortalidad|
|evolution_SIR_bm|SIR_Applied_birthAndMortavility|Aplica el modelo SIR con natalidad y mortalidad n_iterations veces sobre el sistema|
|SIR_bm_model|SIR_Model_birthAndMortavility|Reporta los datos luego de aplicar el modelo SIR con natalidad y mortalidad n veces|
|dead_by_disease|deadByDisease|Aplica probabilidades de muerte por enfermedad a grupos de edad sobre el sistema|
|evolution_sis_dd|SIS_Rule_deathByDisease|Regla de evolución para el modelo SIS con muerte por enfermedad|
|evolution_SIS_dd|SIS_Applied_deathByDisease|Aplica el modelo SIS con muerte por enfermedad n_iterations veces sobre el sistema|
|SIS_dd_model|SIS_Model_deathByDisease|Modelo SIS con muerte por enfermedad|
|medium_curves_sis_dd|SIS_MediumCurves_deathByDisease|Promedio de csim simulaciones para el modelo SIS con muerte por enfermedad|
|evolution_sir_dd|SIR_Rule_deathByDisease|Regla de evolución para el modelo SIR con muerte por enfermedad|
|evolution_SIR_dd|SIR_Applied_deathByDisease|Aplica el modelo SIR con muerte por enfermedad n_iterations veces sobre el sistema|
|SIR_dd_model|SIR_Model_deathByDisease|Modelo SIR con muerte por enfermedad|
|medium_curves_sir_dd|SIR_MediumCurves_deathByDisease|Promedio de n_simulations simulaciones para el modelo SIR con muerte por enfermedad|
