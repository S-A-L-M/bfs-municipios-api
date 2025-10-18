from collections import deque

class GraphService:
    def __init__(self):
        self.graph = {
            'Barranquilla': ['Soledad', 'Puerto Colombia', 'Galapa'],
            'Soledad': ['Barranquilla', 'Malambo', 'Sabanagrande'],
            'Santo Tomas': ['Sabanagrande', 'Palmar'],
            'Palmar': ['Santo Tomas', 'Sabanagrande'],
            'Baranoa': ['Sabanagrande', 'Galapa'],
            'Puerto Colombia': ['Barranquilla'],
            'Sabanagrande': ['Soledad', 'Santo Tomas', 'Palmar', 'Baranoa'],
            'Malambo': ['Soledad', 'Galapa'],
            'Galapa': ['Barranquilla', 'Malambo', 'Baranoa']
        }
    
    def obtener_municipios(self):
        return sorted(self.graph.keys())
    
    def obtener_grafo(self):
        return self.graph
    
    def buscar_ruta_bfs(self, origen, destino):
        if origen not in self.graph or destino not in self.graph:
            return {'success': False, 'error': 'Municipio no encontrado'}
        
        if origen == destino:
            return {
                'success': True,
                'ruta': [origen],
                'distancia': 0,
                'visitados': [origen]
            }
        
        cola = deque([(origen, [origen])])
        visitados = {origen}
        orden = [origen]
        
        while cola:
            actual, camino = cola.popleft()
            
            for vecino in self.graph[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    orden.append(vecino)
                    nuevo_camino = camino + [vecino]
                    
                    if vecino == destino:
                        return {
                            'success': True,
                            'ruta': nuevo_camino,
                            'distancia': len(nuevo_camino) - 1,
                            'visitados': orden,
                            'mensaje': ' → '.join(nuevo_camino)
                        }
                    
                    cola.append((vecino, nuevo_camino))
        
        return {
            'success': False,
            'error': 'No existe ruta',
            'visitados': orden
        }

graph_service = GraphService()