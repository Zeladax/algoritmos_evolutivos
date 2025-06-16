import random
import numpy as np
import pandas as pd

df = pd.read_csv('notas_1u.csv')
alumnos = df['Alumno'].tolist()
notas = df['Nota'].tolist()

def crear_cromosoma():
    cromosoma = []
    for i in range(39):
        examen = random.randint(0, 2)
        genes = [0, 0, 0]
        genes[examen] = 1
        cromosoma.extend(genes)
    return cromosoma

def decodificar_cromosoma(cromosoma):
    asignaciones = {'A': [], 'B': [], 'C': []}
    examenes = ['A', 'B', 'C']
    
    for i in range(39):
        idx = i * 3
        for j in range(3):
            if cromosoma[idx + j] == 1:
                asignaciones[examenes[j]].append(i)
                break
    
    return asignaciones

def calcular_fitness(cromosoma):
    asignaciones = decodificar_cromosoma(cromosoma)
    
    # Penalización si no están equilibrados
    if any(len(asignaciones[ex]) != 13 for ex in ['A', 'B', 'C']):
        return -1000
    
    promedios = []
    varianzas = []
    diversidades = []

    for examen in ['A', 'B', 'C']:
        indices = asignaciones[examen]
        notas_examen = [notas[i] for i in indices]

        # Promedio del grupo (para comparar entre grupos) 
        promedio = np.mean(notas_examen)
        
        # Varianza del grupo (penalización si es alta)
        varianza = np.var(notas_examen)
        
        # Evaluar diversidad: contar cuántos alumnos hay de alto, medio y bajo rendimiento
        altos = sum(1 for n in notas_examen if n >=17)
        bajos = sum(1 for n in notas_examen if n <=13)
        medios = 13 - altos - bajos # Ya que el total de estudiantes por grupo debe ser 13

        # Mientras más equilibrado entre alto, medio, bajo significa que hay mayor diversidad
        # Lo ideal para este caso seria que hayan entre 4-5 por categoria
        diversidad = -((altos - 4.3)**2 + (bajos-4.3)**2 + (medios - 4.3)**2)
        
        promedios.append(promedio)
        varianzas.append(varianza)
        diversidades.append(diversidad)

    # Calculamos la desviacion estándar de los promedios entre grupos (queremos minimizar)
    desviacion_promedios = np.std(promedios)    
    
    # Penalización por varianza interna alta
    penalizacion_varianza = np.mean(varianzas)

    # Premio por diversidad de grupos
    premio_diversidad = np.mean(diversidades)

    # Calculo del fitness final (buscando maximizarlo)
    fitness = -desviacion_promedios - (0.1 * penalizacion_varianza) + (0.05 * premio_diversidad)
    return fitness

def mutacion(cromosoma):
    cromosoma_mutado = cromosoma.copy()
    
    alumno1 = random.randint(0, 38)
    alumno2 = random.randint(0, 38)
    
    idx1 = alumno1 * 3
    idx2 = alumno2 * 3
    
    examen1 = [i for i in range(3) if cromosoma_mutado[idx1 + i] == 1][0]
    examen2 = [i for i in range(3) if cromosoma_mutado[idx2 + i] == 1][0]
    
    if examen1 != examen2:
        cromosoma_mutado[idx1:idx1+3] = [0, 0, 0]
        cromosoma_mutado[idx1 + examen2] = 1
        
        cromosoma_mutado[idx2:idx2+3] = [0, 0, 0]
        cromosoma_mutado[idx2 + examen1] = 1
    
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

print("REPRESENTACIÓN BINARIA")
print("Problema: Distribuir 39 alumnos en 3 exámenes (A, B, C) de forma equitativa")
print("Cromosoma: 117 bits (39 alumnos × 3 bits cada uno)")
print("Gen: [0,1,0] significa alumno asignado a examen B\n")

mejor_solucion = algoritmo_genetico()
asignaciones_finales = decodificar_cromosoma(mejor_solucion)

print("\nDistribución final:")
promedios = []
varianzas = []
diversidades = []

for examen in ['A', 'B', 'C']:
    indices = asignaciones_finales[examen]
    notas_examen = [notas[i] for i in indices]

    promedio = np.mean(notas_examen)
    varianza = np.var(notas_examen)

    altos = sum(1 for n in notas_examen if n >= 17)
    bajos = sum(1 for n in notas_examen if n <= 13)
    medios = 13 - altos - bajos
    diversidad = -((altos - 4.3)**2 + (bajos - 4.3)**2 + (medios - 4.3)**2)

    promedios.append(promedio)
    varianzas.append(varianza)
    diversidades.append(diversidad)

    print(f"Examen {examen}: {len(indices)} alumnos, promedio = {promedio:.2f}, varianza = {varianza:.2f}")
    print(f"  Rango de notas: [{min(notas_examen)} - {max(notas_examen)}]")
    print(f"  Composición (Altos: {altos}, Medios: {medios}, Bajos: {bajos})")
    print(f"  Diversidad: {diversidad:.4f}")
    print(f"  Alumnos: {[alumnos[i] for i in indices[:5]]}... (mostrando primeros 5)")

print("\nVerificación de equilibrio:")
print(f"Desviación estándar entre promedios: {np.std(promedios):.4f}")
print(f"Promedio de varianzas internas: {np.mean(varianzas):.4f}")
print(f"Promedio de diversidad entre grupos: {np.mean(diversidades):.4f}")
