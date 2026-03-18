# 🧠 Maze Solver Engineer (Proyecto #2)

Este proyecto es un sistema avanzado de resolución de laberintos de 128x128 píxeles utilizando algoritmos de búsqueda informada y no informada. Incluye una interfaz gráfica interactiva (GUI) y un motor de simulación para comparación de métricas.

## 🚀 Versión Web (Nueva)

La versión web permite comparar los 4 algoritmos en tiempo real en una cuadrícula de 2x2.

### Cómo Correr la Versión Web

1. **Iniciar Backend (FastAPI):**
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   python3 web/api.py
   ```

2. **Iniciar Frontend (React):**
   ```bash
   cd web/client
   npm install
   npm run dev
   ```
   Abre [http://localhost:5173](http://localhost:5173) en tu navegador.

---

## 🛠️ Instalación (Versión Original Desktop)

### 1. Requisitos Previos
Asegúrate de tener Python 3.8 o superior instalado.

### 2. Instalación de Dependencias

#### 🍎 macOS / 🐧 Linux
Abre una terminal y ejecuta:
```bash
pip install pygame fastapi uvicorn websockets
```

#### 🪟 Windows
Abre el Command Prompt (CMD) o PowerShell y ejecuta:
```bash
pip install pygame fastapi uvicorn websockets
```

---

## 🏃 Cómo Correr el Proyecto (Desktop)

Es fundamental estar en la raíz de la carpeta `proyecto2` para ejecutar los comandos.

### 🎨 Interfaz Gráfica (GUI Pygame)
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

### 📊 Simulación de Métricas (Consola)
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

- `/web`: Backend API y Cliente React.
- `/core`: Clases base (`Node`, `Maze`).
- `/algorithms`: Implementaciones de búsqueda (BFS, DFS, Greedy, A*).
- `/heuristics`: Funciones de distancia.
- `/ui`: Interfaz gráfica con Pygame.
- `/utils`: Cargador de mapas, generador de pruebas y simulador.

---

## 🎨 Código de Colores (Visualización)
- **Negro:** Pared (1)
- **Blanco:** Camino libre (0)
- **Verde:** Inicio (2)
- **Rojo:** Salida (3)
- **Celeste/Azul:** Nodos en proceso de exploración
- **Amarillo:** Camino óptimo encontrado
