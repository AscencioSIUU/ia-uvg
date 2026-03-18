# 🧠 Maze Solver Engineer (Proyecto #2)

Este proyecto es un sistema avanzado de resolución de laberintos de 128x128 píxeles utilizando algoritmos de búsqueda informada y no informada. Incluye una interfaz gráfica interactiva (GUI) y un motor de simulación para comparación de métricas.

## 🚀 Características

- **Algoritmos implementados:** BFS, DFS, Greedy Best-First Search y A*.
- **Heurísticas:** Distancia Manhattan y Euclidiana.
- **Visualización:** Interfaz en tiempo real usando Pygame (128x128 grid).
- **Métricas:** Longitud del camino, nodos explorados, tiempo de ejecución y factor de ramificación.
- **Simulación:** Ejecución automatizada con múltiples puntos de inicio aleatorios.

---

## 🛠️ Instalación

### 1. Requisitos Previos
Asegúrate de tener Python 3.8 o superior instalado.

### 2. Instalación de Dependencias

#### 🍎 macOS / 🐧 Linux
Abre una terminal y ejecuta:
```bash
pip install pygame
```

#### 🪟 Windows
Abre el Command Prompt (CMD) o PowerShell y ejecuta:
```bash
pip install pygame
```

---

## 🏃 Cómo Correr el Proyecto

Es fundamental estar en la raíz de la carpeta `proyecto2` para ejecutar los comandos.

### 🎨 Interfaz Gráfica (GUI)
La GUI permite seleccionar algoritmos y ver la exploración en tiempo real.

**macOS / Linux:**
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 ui/app.py
```

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH += ";."
python ui/app.py
```

**Controles de la GUI:**
- `1`: Seleccionar BFS
- `2`: Seleccionar DFS
- `3`: Seleccionar Greedy
- `4`: Seleccionar A*
- `M`: Usar Heurística Manhattan
- `E`: Usar Heurística Euclidiana
- `SPACE`: Iniciar resolución
- `R`: Reiniciar laberinto

---

### 📊 Simulación de Métricas
Ejecuta todos los algoritmos 10 veces con puntos de inicio aleatorios y genera un reporte comparativo.

**macOS / Linux:**
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 utils/simulator.py
```

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH += ";."
python utils/simulator.py
```

---

## 🏗️ Arquitectura del Proyecto

- `/core`: Clases base (`Node`, `Maze`).
- `/algorithms`: Implementaciones de búsqueda (BFS, DFS, Greedy, A*).
- `/heuristics`: Funciones de distancia.
- `/ui`: Interfaz gráfica con Pygame.
- `/utils`: Cargador de mapas, generador de pruebas y simulador.
- `/tasks`: Seguimiento del desarrollo.

---

## 🎨 Código de Colores (Visualización)
- **Negro:** Pared (1)
- **Blanco:** Camino libre (0)
- **Verde:** Inicio (2)
- **Rojo:** Salida (3)
- **Celeste/Azul:** Nodos en proceso de exploración
- **Amarillo:** Camino óptimo encontrado
