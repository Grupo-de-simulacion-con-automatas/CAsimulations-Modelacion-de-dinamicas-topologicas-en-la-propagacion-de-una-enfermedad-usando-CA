# Proyecto de Grado

### ¿Qué se hizó?:
 - Validaciones hasta el mapa de calor para el modelo SIS
 - Orden en la función para el modelo SIR == S - I - R, en todos los datos generados por la función
### Próximas tareas:
 - Validar el comportamiento de los cambios realizados 
 - Construir una versión con clases

# Mapa de Funciones

sumaS => susceptibleInTheNeighborhood; sumaI => infectedInTheNeighborhood; sumaR => recoveredInTheNeighborhood; sumaV => holesInTheNeighborhood; 
count_S => susceptibleInTheSystem; count_I => infectedInTheSystem; count_R => recoveredInTheSystem; count_D => deadInTheSystem; num_individuals => numberOfIndividuals; 
count_s => susceptiblePercentage; count_i => infectedPercentage; count_r => recoveredPercentage; count_d => deadPercentage; base_rule => baseRuleEvolution; 
evolution_sis => SIS_Rule; evolution_SIS => SIS_Applied; SIS_model => SIS_Model; state_coor => stateCoordinates; num_I => infectedPercentageInSpace; 
initial_condition => initialCondition; northwest => initialLocation(position = "northwest"); north => initialLocation(position = "north"); 
northeast => initialLocation(position = "northeast"); west => initialLocation(position = "west"); center => initialLocation(position = "center"); 
east => initialLocation(position = "east"); southwest => initialLocation(position = "southwest"); south => initialLocation(position = "south"); 
southeast => initialLocation(position = "southeast"); aleatorio => initialLocation(position = "random"); heatmap_sis => SIS_Heatmap; interaction_SI => SI_rule; 
num_R => recoveredPercentageInSpace; interaction_IR => IR_rule; evolution_sir => SIR_Rule; evolution_SIR => SIR_Applied; SIR_model => SIR_Model; 