import pandas as pd
import numpy as np
from pprint import pprint
from queue import Queue
from typing import List
from heapq import heappop, heappush
import folium

#La clas grafo funciona perfecto---------------------------------------------------------------
class Grafo:
    def __init__(self, n):
        self.n = n
        self.nodos = [] 
        self.matriz_adyacencia = [[0] * n for _ in range(n)]

    def agregar_arista(self, org, dest, peso):
        if org not in self.nodos:
            self.nodos.append(org)
        if dest not in self.nodos:
            self.nodos.append(dest)
        org_i = self.nodos.index(org)
        dest_i = self.nodos.index(dest)
        self.matriz_adyacencia[org_i][dest_i] = peso
        self.matriz_adyacencia[dest_i][org_i] = peso

    def encontrar_arista(self,origen,destino):
        org=self.nodos.index(origen)
        dest=self.nodos.index(destino)
        print(self.matriz_adyacencia[org][dest])

    def show(self):
        print("Matriz de adyacencia final:")
        for fila in self.matriz_adyacencia:
            print(fila)
            
    def dijkstra(self,v0):
        inf= (1 << 31) - 1 #creacion del infinito
        def all_visit(visit: List[bool]) -> bool:
            for v in visit:
                if not v:
                    return False
            return True
         #Para las distancia minima entre dos verices
        def min_dist_not_visit(D: List[int], visit: List[bool]) -> int:
            min_dist, index =inf + 1, -1
            for i in range(self.n):
                if D[i] < min_dist and not visit[i]:
                    min_dist = D[i]
                    index = i
            return index
        
        D=[inf]*self.n
        P=[None]*self.n
        visit=[False]*self.n
        D[v0]=0
        #En este ciclo la idea es ir calculando los caminos minimos
        while not all_visit(visit):
            v=min_dist_not_visit(D,visit)#lo hice de forma que v es un indice
            visit[v]=True
            for i,peso in enumerate(self.matriz_adyacencia[v]):
                if peso != 0 and D[v] + peso < D[i] and not visit[i]:   
                    D[i] = D[v] + peso
                    P[i] = self.nodos[v] # y el indice v representa el nodo en el que estamos
                                         # pero se guarda es el codigo del aeropuerto
        return(D,P) #D es la lista de las distancias, y P es la lista de los vertices de donde proviene

    def shortest_path_between_vertices(self,D, P, v0, target):
        path = []
        while target != v0:
            path.append(self.nodos[target]) 
            target = self.nodos.index(P[target])
            
        path.append(self.nodos[v0])
        path.reverse()
        return D[self.nodos.index(path[-1])], path

    def top_k_longest_paths(self,D, P, v0, k=10):
        n = len(D)
        paths = []
        for target in range(n):
            if target != v0 and D[target]!= (1 << 31) - 1 :
                distance, path = self.shortest_path_between_vertices(D, P, v0, target)
                paths.append((distance, path))
        paths.sort(reverse=True)
        return paths[:k]
    
    def crear_mapa_folium(self):
        m = folium.Map(location=[0, 0], zoom_start=2)
        for i, nodo in enumerate(self.nodos):
            folium.Marker(location=[nodo[0], nodo[1]], popup=nodo[2], icon=folium.Icon(color='blue')).add_to(m)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.matriz_adyacencia[i][j] != 0:
                    puntos = [self.nodos[i][:2], self.nodos[j][:2]]
                    folium.PolyLine(locations=puntos, color='red').add_to(m)
        return m
#-------------Aqui acaba la clase-----------------------------


def rad_deg(radians):
    degrees = radians * 180 / np.pi
    return degrees

def deg_rad(degrees):
    radians = degrees * np.pi / 180
    return radians

def Calc_Dist(lat1, long1, lat2, long2, unit = 'kilometros'):
    angulo = long1 - long2
    distance = 60 * 1.1515 * rad_deg(
        np.arccos(
        (np.sin(deg_rad(lat1)) * np.sin(deg_rad(lat2))) + 
        (np.cos(deg_rad(lat1)) * np.cos(deg_rad(lat2)) * np.cos(deg_rad(angulo)))
        )
        )
    if unit == 'millas':
        return round(distance, 2)
    if unit == 'kilometros':
        return round(distance * 1.609344, 2)

def Mostrar_info(code):
    fila=Aeropuertos.loc[Aeropuertos["Source Airport Code"]==code]
    return fila

#Empiza el main----------------------------------------------------------------

Vuelos = pd.read_csv("C:\\Users\\Ivan_JR_PC\\VSC\\U\\Lab3_EDD\\flights_final.csv")


#Aqui creo el dataframe con aeropuertos
Aeropuertos=Vuelos.iloc[:,:6]
Aeropuertos.columns=["Airport Code", "Airport Name", "Airport City", "Airport Country", "Airport Latitude", "Airport Longitude"]
aeropuertos_llegada = Vuelos.iloc[:, 6:12]
aeropuertos_llegada.columns = Aeropuertos.columns
Aeropuertos = pd.concat([Aeropuertos, aeropuertos_llegada])
Aeropuertos =Aeropuertos.drop_duplicates(subset=["Airport Code"])
#Creación del dataframe con todos los aeropuertos, este ya esta perfecto
#Para imprimir el dataframe con los aeropuertos
#print(Aeropuertos)

#Aqui calculo las distancias entre aeropuertos
Vuelos["Distancia"]=Vuelos.apply(lambda fila: Calc_Dist(fila["Source Airport Latitude"], fila["Source Airport Longitude"], fila["Destination Airport Latitude"], fila["Destination Airport Longitude"]), axis=1)
#se imprime el dataframe con los vuelso ya con las distancias
#print(Vuelos)


#Aqui se crea el grafo--------------------------------------------------------------------------
vuelosM=Grafo(Aeropuertos.shape[0])

for indice, fila in Vuelos.iterrows():
 vuelosM.agregar_arista(fila["Source Airport Code"], fila["Destination Airport Code"], int(fila["Distancia"]))

#creación del mapa 
mapa1 = folium.Map(location=[0, 0], zoom_start=2)

# Crear marcadores de aeropuertos
aeropuertos_fg = folium.FeatureGroup(name='Aeropuertos')

# Agregar marcadores de aeropuertos al mapa
for indice, aeropuerto in Aeropuertos.iterrows():
    folium.Marker(
        location=[aeropuerto['Airport Latitude'], aeropuerto['Airport Longitude']],
        popup=f"{aeropuerto['Airport Code']} - {aeropuerto['Airport Name']} ({aeropuerto['Airport City']}, {aeropuerto['Airport Country']}), {aeropuerto['Airport Latitude']}, {aeropuerto['Airport Longitude']}",
        icon=folium.Icon(color='blue', icon='plane')
    ).add_to(aeropuertos_fg)

# Agregar la capa de marcadores de aeropuertos al mapa
aeropuertos_fg.add_to(mapa1)

# Guardar el mapa como un archivo HTML
mapa1.save('aeropuertos_mapa.html')

def buscar_codigo(codigo):
    aeropuerto_encontrado = Aeropuertos[Aeropuertos['Airport Code'] == codigo]
    return aeropuerto_encontrado

def buscar_aeropuerto_distantes():
    codigo_aeropuerto = input("Ingrese el código del aeropuerto que desea buscar: ")
    aeropuerto_seleccionado = buscar_codigo(codigo_aeropuerto)
    if not aeropuerto_seleccionado.empty: #Se verifica si está el aeropuerto
        vuelosM=Grafo(Aeropuertos.shape[0])
        for indice, fila in Vuelos.iterrows():
            vuelosM.agregar_arista(fila["Source Airport Code"], fila["Destination Airport Code"], int(fila["Distancia"]))
        v0=vuelosM.nodos.index(codigo_aeropuerto)
        D,P=vuelosM.dijkstra(v0)
        print("los 10 mas grandes de ", vuelosM.nodos[v0])
        X=vuelosM.top_k_longest_paths(D,P,v0) #este calcula los 10 mas grandes
        for i in X:
            print(i)
        
        #Desde aquí se crea un data frame con la información de los 10 aeropuertos
        k = 10 
        longest_paths = vuelosM.top_k_longest_paths(D, P, v0, k)
        aeropuertos_longest_paths = []

        for distance, path in longest_paths:
            for airport_code in path:
                aeropuerto_info = Aeropuertos[Aeropuertos['Airport Code'] == airport_code].iloc[0]
                aeropuertos_longest_paths.append({
                    'Airport Code': aeropuerto_info['Airport Code'],
                    'Airport Name': aeropuerto_info['Airport Name'],
                    'Airport City': aeropuerto_info['Airport City'],
                    'Airport Country': aeropuerto_info['Airport Country'],
                    'Latitude': aeropuerto_info['Airport Latitude'],
                    'Longitude': aeropuerto_info['Airport Longitude'],
                    'Distance': distance  # Distancia total de la ruta
                })
        
        df_longest_paths = pd.DataFrame(aeropuertos_longest_paths)
        
        
        #Se crea el mapa        
        mapa = folium.Map(location=[0, 0], zoom_start=2)
        longest_paths_fg = folium.FeatureGroup(name='Aeropuertos en las rutas más largas') 
        
        #Este ciclo genera los marcadores de los aeropuertos
        for indice, aeropuerto in df_longest_paths.iterrows():
            folium.Marker(
                location=[aeropuerto['Latitude'], aeropuerto['Longitude']], #la ubicación basándose en latitud y longitud
                popup=f"{aeropuerto['Airport Code']} - {aeropuerto['Airport Name']} ({aeropuerto['Airport City']}, {aeropuerto['Airport Country']}) - Distancia: {aeropuerto['Distance']} km", #La info a agregar 
                icon=folium.Icon(color='red', icon='plane') 
            ).add_to(longest_paths_fg)
    
        longest_paths_fg.add_to(mapa) #Se agrega al mapa
        
        #Esto es para crear las líneas que los conectan 
        for i in range(len(df_longest_paths) - 1):
            current_airport = df_longest_paths.iloc[i]
            next_airport = df_longest_paths.iloc[i + 1]
            puntos = [[current_airport['Latitude'], current_airport['Longitude']],
                    [next_airport['Latitude'], next_airport['Longitude']]]
            folium.PolyLine(locations=puntos, color='blue').add_to(mapa)

        mapa.save('aeropuertos_caminos_distantes.html') #Se agrega al mapa 
    else:
        print("¡El aeropuerto no se encontró!")


def buscar_camino_min():
    codigo_aeropuerto_salida = input("Ingrese el código del aeropuerto de salida que desea buscar: ")
    codigo_aeropuerto_llegada = input("Ingrese el código del aeropuerto de llegada que desea buscar: ")
    
    aeropuerto_seleccionado_salida = buscar_codigo(codigo_aeropuerto_salida)
    aeropuerto_seleccionado_llegada = buscar_codigo(codigo_aeropuerto_llegada)
    
    if not aeropuerto_seleccionado_salida.empty and not aeropuerto_seleccionado_llegada.empty:
        vuelosM=Grafo(Aeropuertos.shape[0])
        
        for indice, fila in Vuelos.iterrows():
            vuelosM.agregar_arista(fila["Source Airport Code"], fila["Destination Airport Code"], int(fila["Distancia"]))
            
        v0=vuelosM.nodos.index(codigo_aeropuerto_salida) 
        target=vuelosM.nodos.index(codigo_aeropuerto_llegada)
        D,P=vuelosM.dijkstra(v0)
        distancia_minima, camino_minimo = vuelosM.shortest_path_between_vertices(D, P, v0, target)
        
        #creación del dataframe con la información de los aeropuertos
        df_camino_minimo = pd.DataFrame(columns=['Airport Code', 'Airport Name', 'Airport City', 'Airport Country', 'Latitude', 'Longitude', 'Distance'])
        
        for aeropuerto_codigo in camino_minimo:
            aeropuerto_info = Aeropuertos[Aeropuertos['Airport Code'] == aeropuerto_codigo].iloc[0]
            df_camino_minimo.loc[len(df_camino_minimo)] = {
                'Airport Code': aeropuerto_info['Airport Code'],
                'Airport Name': aeropuerto_info['Airport Name'],
                'Airport City': aeropuerto_info['Airport City'],
                'Airport Country': aeropuerto_info['Airport Country'],
                'Latitude': aeropuerto_info['Airport Latitude'],
                'Longitude': aeropuerto_info['Airport Longitude'],
                'Distance': distancia_minima  # Distancia total de la ruta mínima
            }          
            
        print("Camino mínimo entre:", codigo_aeropuerto_salida, "y", codigo_aeropuerto_llegada)
        print(df_camino_minimo)
        
        df_shortest_paths = pd.DataFrame(camino_minimo)
        #creación del mapa       
        mapa2 = folium.Map(location=[0, 0], zoom_start=2)
        shortest_path_fg = folium.FeatureGroup(name='Aeropuertos en el camino mínimo')  
        
        #lo de los marcadores      
        for indice, aeropuerto in df_camino_minimo.iterrows():
            folium.Marker(
                location=[aeropuerto['Latitude'], aeropuerto['Longitude']],  
                popup=f"{aeropuerto['Airport Code']} - {aeropuerto['Airport Name']} ({aeropuerto['Airport City']}, {aeropuerto['Airport Country']}) - Distancia: {aeropuerto['Distance']} km",
                icon=folium.Icon(color='red', icon='plane')
            ).add_to(shortest_path_fg)
            
        shortest_path_fg.add_to(mapa2)
        
        #Lo de las lineas 
        for i in range(len(df_camino_minimo) - 1):
            current_airport = df_camino_minimo.iloc[i]
            next_airport = df_camino_minimo.iloc[i + 1]
            puntos = [[current_airport['Latitude'], current_airport['Longitude']],
                    [next_airport['Latitude'], next_airport['Longitude']]]
            folium.PolyLine(locations=puntos, color='blue').add_to(mapa2)
            
        mapa2.save('aeropuertos_camino_minimo.html')
        
    else:
        print("¡El aeropuerto de salida o el aeropuerto de llegada no se encontraron!")
        
    
        
        
#--------------
buscar_aeropuerto_distantes()
buscar_camino_min()









