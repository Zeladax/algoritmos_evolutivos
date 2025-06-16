import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import random

# Cargar datos de notas (puedes reemplazar este CSV con el archivo que tengas)
df = pd.read_csv('notas_1u.csv')
alumnos = df['Alumno'].tolist()
notas = df['Nota'].tolist()

def crear_cromosoma_real():
    cromosoma = []
    for i in range(39):  # Hay 39 alumnos
        # Generamos 3 valores reales entre 0 y 1
        pesos = [random.random() for _ in range(3)]
        suma = sum(pesos)
        # Normalizamos los pesos para que sumen 1
        pesos_norm = [p / suma for p in pesos]
        cromosoma.extend(pesos_norm)
    return cromosoma

def crear_cromosoma_permutacional():
    # Creamos una lista de índices para los 39 alumnos
    cromosoma = list(range(39))
    random.shuffle(cromosoma)  # Desordenamos aleatoriamente
    return cromosoma

def crear_cromosoma_binario():
    cromosoma = []
    for i in range(39):  # Hay 39 alumnos
        # Generamos un vector de 3 bits aleatorios, donde cada bit corresponde a un examen
        examen = random.randint(0, 2)
        genes = [0, 0, 0]
        genes[examen] = 1  # Asignamos el alumno a un examen
        cromosoma.extend(genes)
    return cromosoma

# Función para graficar la evolución del fitness por generación
def graficar_evolucion_fitness(historial_fitness, nombre_representacion):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(historial_fitness)), historial_fitness, label=f"Fitness {nombre_representacion}")
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title(f'Evolución del Fitness por Generación ({nombre_representacion})')
    plt.grid(True)
    plt.legend()
    plt.show()

# Función para graficar el histograma de notas por examen
def graficar_histograma_notas(examenes, nombre_representacion):
    plt.figure(figsize=(10, 6))
    
    # Extraemos las notas de los exámenes
    notas_examen_A = [notas[i] for i in examenes['A']]
    notas_examen_B = [notas[i] for i in examenes['B']]
    notas_examen_C = [notas[i] for i in examenes['C']]
    
    # Histograma por cada examen
    sns.histplot(notas_examen_A, kde=True, color='blue', label='Examen A', bins=10)
    sns.histplot(notas_examen_B, kde=True, color='green', label='Examen B', bins=10)
    sns.histplot(notas_examen_C, kde=True, color='red', label='Examen C', bins=10)
    
    plt.xlabel('Nota')
    plt.ylabel('Frecuencia')
    plt.title(f'Histograma de Notas por Examen ({nombre_representacion})')
    plt.legend()
    plt.grid(True)
    plt.show()


# Función para comparar las distribuciones de las 3 representaciones
def graficar_comparacion_distribuciones(rep_binaria, rep_permutacional, rep_real):
    plt.figure(figsize=(10, 6))

    # Gráfico de notas por representación
    sns.kdeplot(rep_binaria, label="Representación Binaria", color='blue', fill=True, alpha=0.3)
    sns.kdeplot(rep_permutacional, label="Representación Permutacional", color='green', fill=True, alpha=0.3)
    sns.kdeplot(rep_real, label="Representación Real", color='red', fill=True, alpha=0.3)

    plt.xlabel('Nota')
    plt.ylabel('Densidad')
    plt.title('Comparación de Distribuciones de Notas por Representación')
    plt.legend()
    plt.grid(True)
    plt.show()

# Función de decodificación de cromosomas (como en los programas anteriores)
def decodificar_cromosoma(cromosoma):
    asignaciones = {'A': [], 'B': [], 'C': []}
    
    # Para asegurar que los índices sean enteros, transformamos los índices de acuerdo a la probabilidad
    # Asumimos que los cromosomas ya están normalizados (sumando 1 en cada 3 elementos para cada examen)
    
    examenes = ['A', 'B', 'C']
    num_alumnos = len(cromosoma) // 3
    
    # Decodificar el cromosoma, asignando alumnos a exámenes basados en la probabilidad
    for i in range(num_alumnos):
        # Extracción de los 3 valores para cada alumno
        start_idx = i * 3
        alumno_probabilidades = cromosoma[start_idx:start_idx + 3]
        
        # Encontramos el examen con la mayor probabilidad
        examen_asignado = max(range(3), key=lambda x: alumno_probabilidades[x])
        
        # Asignamos el alumno al examen correspondiente
        asignaciones[examenes[examen_asignado]].append(i)
    
    return asignaciones

# Función principal de visualización
def visualizacion(historial_binario, historial_permutacional, historial_real, mejor_binario, mejor_permutacional, mejor_real):
    # Graficar la evolución del fitness para cada representación
    graficar_evolucion_fitness(historial_binario, 'Binaria')
    graficar_evolucion_fitness(historial_permutacional, 'Permutacional')
    graficar_evolucion_fitness(historial_real, 'Real')

    # Obtener asignaciones finales para cada representación
    asignaciones_binaria = decodificar_cromosoma(mejor_binario)
    asignaciones_permutacional = decodificar_cromosoma(mejor_permutacional)
    asignaciones_real = decodificar_cromosoma(mejor_real)

    # Graficar histograma de notas por examen
    graficar_histograma_notas(asignaciones_binaria, 'Binaria')
    graficar_histograma_notas(asignaciones_permutacional, 'Permutacional')
    graficar_histograma_notas(asignaciones_real, 'Real')

    # Comparar las distribuciones de notas entre las 3 representaciones
    notas_binaria = [notas[i] for i in asignaciones_binaria['A'] + asignaciones_binaria['B'] + asignaciones_binaria['C']]
    notas_permutacional = [notas[i] for i in asignaciones_permutacional['A'] + asignaciones_permutacional['B'] + asignaciones_permutacional['C']]
    notas_real = [notas[i] for i in asignaciones_real['A'] + asignaciones_real['B'] + asignaciones_real['C']]
    
    graficar_comparacion_distribuciones(notas_binaria, notas_permutacional, notas_real)

# Ejemplo de cómo usar el script
# Estos valores se obtienen al ejecutar el algoritmo en cada representación (representación_binaria, representacion_permutacional, representacion_real)
historial_binario = [0.5, 0.6, 0.7, 0.75, 0.8]  # Ejemplo de evolución de fitness para la representación binaria
historial_permutacional = [0.4, 0.55, 0.6, 0.65, 0.75]  # Ejemplo para permutacional
historial_real = [0.45, 0.55, 0.6, 0.7, 0.85]  # Ejemplo para real

# Mejores soluciones finales para cada representación
mejor_binario = crear_cromosoma_binario()  # Estos deben ser el mejor cromosoma encontrado para cada representación
mejor_permutacional = crear_cromosoma_permutacional()
mejor_real = crear_cromosoma_real()

# Llamar a la función de visualización
visualizacion(historial_binario, historial_permutacional, historial_real, mejor_binario, mejor_permutacional, mejor_real)

