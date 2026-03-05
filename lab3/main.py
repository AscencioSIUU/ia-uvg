import pandas as pd
from queues import FIFOQueue, LIFOQueue, PriorityQueue
from search_algorithms import graph_search
from excel_to_csv import excel_to_csv

def convert_data():
    # Convertir los archivos Excel a CSV (si es necesario)
    if(not pd.io.common.file_exists("funcion_de_costo.csv")):
        excel_to_csv("funcion_de_costo.xlsx", "funcion_de_costo.csv", "funcion_de_costo.csv")
        excel_to_csv("heuristica.xlsx", "heuristica.csv", "heuristica.csv")

def load_data():
    convert_data() 
    
    # Cargar los archivos (Asegúrate de cambiar .csv por .xlsx y usar pd.read_excel si son excel)
    costos_df = pd.read_csv("funcion_de_costo.csv")
    heuristica_df = pd.read_csv("heuristica.csv")
    
    # 1. Crear el diccionario de grafo para los costos
    graph = {}
    for index, row in costos_df.iterrows():
        origen = row['Origen']
        destino = row['Destino']
        costo = row['Cost']
        
        if origen not in graph:
            graph[origen] = {}
        graph[origen][destino] = costo

    # 2. Crear el diccionario de heurística
    heuristics = {}
    for index, row in heuristica_df.iterrows():
        actividad = row['Activity']
        tiempo = row['Recovery time after burning 300cal (minutes)']
        heuristics[actividad] = tiempo
        
    return graph, heuristics

def main():
    graph, heuristics = load_data()
    
    start = "Warm-up activities"
    goal = "Stretching"
    
    # Algoritmos sin Heuristica
    
    print("--- 1. Breadth-First Search  ---")
    ucs_path, ucs_cost = graph_search(start, goal, graph, heuristics, FIFOQueue(), use_heuristic=False)
    print(f"Ruta: {ucs_path}")
    print(f"Costo de tiempo: {ucs_cost} minutos\n")
    
    print("--- 2. Depth-First Search ---")
    ucs_path, ucs_cost = graph_search(start, goal, graph, heuristics, LIFOQueue(), use_heuristic=False)
    print(f"Ruta: {ucs_path}")
    print(f"Costo de tiempo: {ucs_cost} minutos\n")
    
    print("--- 3. Uniform-Cost Search ---")
    ucs_path, ucs_cost = graph_search(start, goal, graph, heuristics, PriorityQueue(), use_heuristic=False)
    print(f"Ruta: {ucs_path}")
    print(f"Costo de tiempo: {ucs_cost} minutos\n")
    
    # Algoritmos con Heuristica
    
    print("--- 3. Greedy Best-First Search ---")
    ucs_path, ucs_cost = graph_search(start, goal, graph, heuristics, PriorityQueue(), use_heuristic=True)
    print(f"Ruta: {ucs_path}")
    print(f"Costo de tiempo: {ucs_cost} minutos\n")
    
    print("--- 5. A* ---")
    astar_path, astar_cost = graph_search(start, goal, graph, heuristics, PriorityQueue(), use_heuristic=True)
    print(f"Ruta: {astar_path}")
    print(f"Costo de tiempo: {astar_cost} minutos\n")
    

if __name__ == "__main__":
    main()