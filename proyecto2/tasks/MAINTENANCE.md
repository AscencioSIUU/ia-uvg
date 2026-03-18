# 🛠️ GUÍA DE MANTENIMIENTO - MAZE SOLVER

Esta guía documenta la arquitectura actual y el funcionamiento del motor de simulación para facilitar futuras modificaciones.

## 🏗️ Arquitectura del Sistema

### 1. Backend (`web/api.py` & `/algorithms`)
- **Motores de Búsqueda:** Ubicados en `algorithms/`. Todos son generadores que emiten nodos de exploración y, al final, un diccionario de métricas.
- **WebSocket (`/solve`):** Recibe el laberinto y la heurística. Ejecuta los 4 algoritmos en paralelo usando `asyncio.gather`.
- **Control de Flujo:** Tiene un `asyncio.sleep(0.01)` para no saturar el canal de comunicación, pero la velocidad visual real la controla el Frontend.

### 2. Frontend (`web/client/src/`)
- **`App.jsx`:** Componente principal. Gestiona la conexión WebSocket y distribuye los mensajes a los cuadrantes mediante `Refs`.
- **`Navbar.jsx`:** Componente independiente para controles. Mantiene la integridad horizontal.
- **`Quadrant.jsx` (DENTRO DE `App.jsx`):** Es el corazón visual.
    - **Canvas Directo:** Usa `useImperativeHandle` para permitir que el padre (`App.jsx`) ordene dibujar un paso sin provocar un re-render de React (crítico para el rendimiento).
    - **Cola de Animación:** Implementa un `stepQueue`. Los mensajes del servidor se encolan y se procesan a una tasa constante usando `requestAnimationFrame` y la constante `ANIMATION_SPEED`.

## 🎨 Lógica Visual (Canvas)
- **Fondo:** Negro (`#000`).
- **Paredes:** Negro (`#000`) sobre fondo gris muy oscuro (`#111`) para contraste.
- **Exploración:** Blanco semi-transparente (`rgba(255,255,255,0.2)`).
- **Cabezal de Decisión:** Blanco puro (`#fff`). Es el nodo que se está procesando en el frame actual.
- **Camino Final:** Amarillo neón (`#ffeb3b`) con `shadowBlur`.

## 🚀 Cómo continuar / Extender

### Ajustar Velocidad
Si la simulación es muy lenta o rápida, cambia `ANIMATION_SPEED` en `App.jsx`:
- `1`: Paso a paso muy lento (ideal para debug).
- `5-10`: Simulación rápida tipo "race".

### Añadir un nuevo Algoritmo
1. Crea el archivo en `algorithms/`.
2. Agrégalo al diccionario `generators` en `web/api.py`.
3. Actualiza la constante `ALGOS` en `App.jsx`.
4. El grid de CSS se ajustará automáticamente si es par, o puedes cambiar `grid-template-columns` en `App.css`.

### Cambiar Estética (Modo Oscuro)
- Los colores principales están definidos en `:root` dentro de `App.css`.
- La lógica de colores del laberinto está en la función `draw()` dentro de `Quadrant` en `App.jsx`.

## ⚠️ Notas de Seguridad
- No subas `maze_sample.txt` al repo (está en `.gitignore`).
- Mantén el `PYTHONPATH=.` al ejecutar el backend para que las importaciones de `core/` y `algorithms/` funcionen.
