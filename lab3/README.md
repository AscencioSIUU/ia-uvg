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

## Estructura del Proyecto

```
├── main.py                 # Archivo principal con la ejecución de los algoritmos
├── search_algorithms.py    # Implementación de los algoritmos de búsqueda
├── node.py                # Clase Node para representar nodos del grafo
├── queues.py              # Implementación de diferentes tipos de colas
├── excel_to_csv.py        # Utilidad para convertir archivos Excel a CSV
├── funcion_de_costo.csv   # Datos de costos entre actividades
├── heuristica.csv         # Datos de heurística para cada actividad
└── README.md              # Este archivo
```

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

### Salida Esperada

El programa mostrará la ruta encontrada y el costo total para cada algoritmo:

```
--- 1. Breadth-First Search  ---
Ruta: ['Warm-up activities', ..., 'Stretching']
Costo de tiempo: X minutos

--- 2. Depth-First Search ---
Ruta: ['Warm-up activities', ..., 'Stretching']
Costo de tiempo: Y minutos

...
```

## Componentes Principales

### 1. Clase Node (`node.py`)
Representa un nodo en el grafo con:
- `state`: Estado actual (actividad)
- `parent`: Nodo padre
- `path_cost`: Costo del camino desde el inicio
- `heuristic`: Valor heurístico
- `mode`: Modo de comparación ("ucs", "greedy", "astar")

### 2. Colas (`queues.py`)
- **FIFOQueue**: Cola FIFO para BFS
- **LIFOQueue**: Pila LIFO para DFS
- **PriorityQueue**: Cola de prioridad para UCS, Greedy y A*

### 3. Algoritmos de Búsqueda (`search_algorithms.py`)
- `graph_search()`: Función genérica de búsqueda en grafo
- `reconstruct_path()`: Reconstruye el camino desde el nodo objetivo

### 4. Gestión de Datos
- **Conversión automática**: Excel a CSV si es necesario
- **Carga de datos**: Función de costos y heurística desde CSV
- **Construcción del grafo**: Diccionario de adyacencias

## Datos de Entrada

### Función de Costo (`funcion_de_costo.csv`)
Contiene las conexiones entre actividades y sus costos:
```csv
Origen,Destino,Cost
Warm-up activities,Cardio,10
...
```

### Heurística (`heuristica.csv`)
Contiene valores heurísticos para cada actividad:
```csv
Activity,Recovery time after burning 300cal (minutes)
Warm-up activities,45
...
```

## Personalización

### Cambiar Puntos de Inicio y Meta
En `main.py`, modifica las variables:
```python
start = "Tu-actividad-inicio"
goal = "Tu-actividad-meta"
```

### Agregar Nuevos Algoritmos
1. Implementa la función en `search_algorithms.py`
2. Crea una nueva cola si es necesario en `queues.py`
3. Agrega la llamada en `main.py`

## Análisis y Comparación

Cada algoritmo puede producir diferentes resultados:
- **BFS**: Encuentra la ruta con menos pasos
- **DFS**: Puede encontrar rutas más largas pero explora menos nodos
- **UCS**: Encuentra la ruta de menor costo sin considerar heurística
- **Greedy**: Usa solo heurística, puede no ser óptima
- **A***: Combina costo y heurística para encontrar la ruta óptima

## Problemas Comunes

1. **Error de archivo no encontrado**: Asegúrate de que los archivos CSV estén en el directorio correcto
2. **Error de dependencias**: Instala las librerías requeridas con `pip install`
3. **Error de entorno virtual**: Activa el entorno virtual antes de ejecutar

## Contribuir

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto es parte del curso de Inteligencia Artificial - UVG 2026.

## Autores

- [Tu Nombre] - Desarrollo inicial

## Reconocimientos

- Curso de Inteligencia Artificial - Universidad del Valle de Guatemala
- Algoritmos basados en el libro "Artificial Intelligence: A Modern Approach"
