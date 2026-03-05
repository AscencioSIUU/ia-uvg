# Lab 3 - Algoritmos de Búsqueda en Grafos

## Descripción

Este proyecto implementa y compara diferentes algoritmos de búsqueda en grafos para encontrar la ruta óptima entre actividades de ejercicio. El objetivo es encontrar el camino desde "Warm-up activities" hasta "Stretching" utilizando diversos algoritmos de búsqueda.

## Algoritmos Implementados

### Algoritmos sin Heurística
1. **Breadth-First Search (BFS)** - Búsqueda en anchura
2. **Depth-First Search (DFS)** - Búsqueda en profundidad  
3. **Uniform-Cost Search (UCS)** - Búsqueda de costo uniforme

### Algoritmos con Heurística
4. **Greedy Best-First Search** - Búsqueda codiciosa
5. **A*** - Algoritmo A estrella

## Instalación y Configuración

### Prerequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar el repositorio** (si aplica):
```bash
git clone <url-del-repositorio>
cd lab3
```

2. **Crear un entorno virtual** (recomendado):
```bash
python -m venv env
source env/bin/activate  # En macOS/Linux
# o
env\Scripts\activate     # En Windows
```

3. **Instalar las dependencias**:
```bash
pip install pandas openpyxl numpy
```

## Uso

### Ejecución Principal

Para ejecutar todos los algoritmos y comparar resultados:

```bash
python main.py
```

# Salida

El programa mostrará la ruta encontrada y el costo total para cada algoritmo:

```
--- 1. Breadth-First Search  ---
Ruta: ['Warm-up activities', 'Skipping Rope', 'Dumbbell', 'Leg Press Machine', 'Stretching']
Costo de tiempo: 48 minutos

--- 2. Depth-First Search ---
Ruta: ['Warm-up activities', 'Step Mill', 'Incline Bench', 'Hammer Strength', 'Stretching']
Costo de tiempo: 54 minutos

--- 3. Uniform-Cost Search ---
Ruta: ['Warm-up activities', 'Tread Mill', 'Pulling Bars', 'Climbing Rope', 'Stretching']
Costo de tiempo: 46 minutos

--- 3. Greedy Best-First Search ---
Ruta: ['Warm-up activities', 'Tread Mill', 'Pulling Bars', 'Climbing Rope', 'Stretching']
Costo de tiempo: 46 minutos

--- 5. A* ---
Ruta: ['Warm-up activities', 'Tread Mill', 'Pulling Bars', 'Climbing Rope', 'Stretching']
Costo de tiempo: 46 minutos
```
