import random
import numpy as np
import pandas as pd

df = pd.read_csv('notas_1u.csv')
alumnos = df['Alumno'].tolist()
notas = df['Nota'].tolist()

def crear_cromosoma():
    cromosoma = []
    for i in range(39):  # Hay 39 alumnos
        examen = random.randint(0, 3)  # Ahora generamos un número entre 0 y 3
        genes = [0, 0, 0, 0]  # 4 exámenes
        genes[examen] = 1  # Asignamos el alumno al examen correspondiente
        cromosoma.extend(genes)
    return cromosoma

def decodificar_cromosoma(cromosoma):
    asignaciones = {'A': [], 'B': [], 'C': [], 'D': []}  # Añadimos el examen D
    examenes = ['A', 'B', 'C', 'D']  # Ahora tenemos 4 exámenes
    contadores = {'A': 0, 'B': 0, 'C': 0, 'D': 0}  # Inicializamos los contadores de alumnos por examen
    
    alumnos_disponibles = list(range(39))  # Lista de alumnos disponibles
    
    # Asignamos los alumnos a los exámenes, respetando la probabilidad
    for i in range(39):
        idx = i * 4  # Cada alumno tiene 4 probabilidades en el cromosoma
        mejor_examen = max(range(4), key=lambda x: cromosoma[idx + x])  # Asignar al examen con mayor probabilidad
        asignaciones[examenes[mejor_examen]].append(i)
        contadores[examenes[mejor_examen]] += 1
    
    # Si algún examen tiene 0 alumnos, lo corregimos distribuyendo entre los exámenes
    for examen in examenes:
        if len(asignaciones[examen]) == 0:
            # Asignamos aleatoriamente un alumno a este examen
            asignaciones[examen].append(alumnos_disponibles.pop())
            contadores[examen] += 1
    
    return asignaciones

def calcular_fitness(cromosoma):
    asignaciones = decodificar_cromosoma(cromosoma)
    
    promedios = {}
    varianzas = {}
    
    # Verificar si hay exámenes vacíos y evitar errores
    for examen in ['A', 'B', 'C', 'D']:  # Ahora tenemos 4 exámenes
        indices = asignaciones[examen]
        if len(indices) == 0:
            promedios[examen] = 0  # Si no hay alumnos, le damos promedio 0
            varianzas[examen] = 0  # Y varianza 0
        else:
            notas_examen = [notas[i] for i in indices]
            promedios[examen] = np.mean(notas_examen)
            varianzas[examen] = np.var(notas_examen)
    
    desv_promedios = np.std(list(promedios.values()))
    promedio_varianzas = np.mean(list(varianzas.values()))
    
    # Calcular el número de alumnos por examen
    num_alumnos_por_examen = [len(asignaciones[examen]) for examen in ['A', 'B', 'C', 'D']]
    
    # El número ideal de alumnos por examen sería aproximadamente 39 / 4 = 9.75
    objetivo = 39 / 4  # Aproximadamente 9.75 alumnos por examen
    # Penalizar desviación del número ideal de alumnos
    desbalance = np.std(num_alumnos_por_examen)  # La desviación estándar del número de alumnos por examen
    
    # Penalizar las soluciones más desbalanceadas
    penalizacion_desbalance = desbalance * 0.1  # Puedes ajustar el factor de penalización
    
    # Añadir la penalización de desbalance al fitness
    fitness = -desv_promedios - 0.1 * promedio_varianzas - penalizacion_desbalance
    return fitness


def mutacion(cromosoma):
    cromosoma_mutado = cromosoma.copy()
    
    for i in range(39):
        if random.random() < 0.1:
            idx = i * 4  # Ahora cada alumno tiene 4 valores
            nuevos_pesos = [random.random() for _ in range(4)]
            suma = sum(nuevos_pesos)
            cromosoma_mutado[idx:idx+4] = [p/suma for p in nuevos_pesos]
    
    return cromosoma_mutado

def algoritmo_genetico(generaciones=100, tam_poblacion=50):
    poblacion = [crear_cromosoma() for _ in range(tam_poblacion)]
    
    for gen in range(generaciones):
        fitness_scores = [(crom, calcular_fitness(crom)) for crom in poblacion]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        nueva_poblacion = []
        
        elite = int(tam_poblacion * 0.2)
        for i in range(elite):
            nueva_poblacion.append(fitness_scores[i][0])
        
        while len(nueva_poblacion) < tam_poblacion:
            padre = random.choice(poblacion[:tam_poblacion//2])
            hijo = mutacion(padre)
            nueva_poblacion.append(hijo)
        
        poblacion = nueva_poblacion
        
        if gen % 20 == 0:
            mejor_fitness = fitness_scores[0][1]
            print(f"Generación {gen}: Mejor fitness = {mejor_fitness:.4f}")
    
    mejor_cromosoma = fitness_scores[0][0]
    return mejor_cromosoma

print("REPRESENTACIÓN BINARIA CON 4 EXAMENES")
print("Problema: Distribuir 39 alumnos en 4 exámenes (A, B, C, D)")
print("Cromosoma: 156 bits (39 alumnos × 4 bits cada uno)")
print("Gen: [0,0,1,0] significa alumno asignado a examen C\n")

# Llamar a la función de visualización
mejor_solucion = algoritmo_genetico()
asignaciones_finales = decodificar_cromosoma(mejor_solucion)

print("\nDistribución final:")
for examen in ['A', 'B', 'C', 'D']:
    indices = asignaciones_finales[examen]
    notas_examen = [notas[i] for i in indices]
    promedio = np.mean(notas_examen)
    print(f"Examen {examen}: {len(indices)} alumnos, promedio = {promedio:.2f}")
    print(f"  Alumnos: {[alumnos[i] for i in indices[:5]]}... (mostrando primeros 5)")

print("\nVerificación de equilibrio:")
promedios = []
for examen in ['A', 'B', 'C', 'D']:
    indices = asignaciones_finales[examen]
    notas_examen = [notas[i] for i in indices]
    promedios.append(np.mean(notas_examen))
print(f"  Desviación estándar entre promedios: {np.std(promedios):.4f}")
