# Lab 4: Búsqueda Local - 8 Reinas

Este proyecto implementa y compara algoritmos de búsqueda local para resolver el problema de las 8 reinas.

## Requisitos

Para ejecutar el notebook, asegúrate de tener instaladas las siguientes librerías:
- `numpy`
- `matplotlib`
- `jupyter` / `notebook`

Puedes instalarlas con:
```bash
pip install numpy matplotlib notebook
```

## Estructura del Proyecto

- `local_search_lab.ipynb`: Notebook principal con la implementación y experimentos.
- `README.md`: Instrucciones de uso.

## Workflow de Trabajo

1.  **Preparación:** Abre el notebook `local_search_lab.ipynb`.
2.  **Implementación:** Revisa las funciones `es_solucion` y `heuristica` proporcionadas.
3.  **Algoritmos:** El notebook ya contiene la implementación de:
    *   Hill Climbing (Ascenso de colina).
    *   Random Restart Hill Climbing.
    *   Local Beam Search (con k variable).
4.  **Ejecución de Experimentos:** Ejecuta la celda de experimentos que corre cada algoritmo 1000 veces para recolectar métricas de éxito y eficiencia.
5.  **Análisis:** Responde las preguntas de discusión basadas en los datos obtenidos (tiempos, porcentaje de éxito, etc.).
6.  **Visualización:** Usa la función `dibujar_tablero` al final del notebook para ver gráficamente las soluciones encontradas.

## Algoritmos Implementados

- **Hill Climbing:** Busca el mejor vecino inmediato. Es rápido pero propenso a estancarse en máximos locales.
- **Random Restart:** Supera los máximos locales reiniciando la búsqueda desde un estado aleatorio.
- **Beam Search:** Mantiene múltiples estados en paralelo, permitiendo una exploración más amplia del espacio de búsqueda.
