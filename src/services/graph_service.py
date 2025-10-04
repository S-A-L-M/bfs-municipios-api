class GraphService:
    def __init__(self):
        self.grafo = {}
    
    def crear_grafo(self, conexiones):
        """Crea el grafo con las conexiones proporcionadas"""
        self.grafo = {}
        for origen, destino in conexiones:
            if origen not in self.grafo:
                self.grafo[origen] = []
            if destino not in self.grafo:
                self.grafo[destino] = []
            
            self.grafo[origen].append(destino)
            self.grafo[destino].append(origen)  # Si es bidireccional
        
        return {
            'success': True,
            'message': 'Grafo creado exitosamente',
            'municipios': len(self.grafo)
        }
    
    def obtener_municipios(self):
        """Retorna la lista de municipios"""
        return list(self.grafo.keys())
    
    def obtener_grafo(self):
        """Retorna el grafo completo"""
        return self.grafo
    
    def buscar_ruta_bfs(self, origen, destino):
        """Busca la ruta más corta usando BFS"""
        if origen not in self.grafo or destino not in self.grafo:
            return {
                'success': False,
                'error': 'Municipio no encontrado en el grafo'
            }
        
        if origen == destino:
            return {
                'success': True,
                'ruta': [origen],
                'distancia': 0
            }
        
        # BFS
        visitados = {origen}
        cola = [(origen, [origen])]
        
        while cola:
            actual, ruta = cola.pop(0)
            
            for vecino in self.grafo[actual]:
                if vecino not in visitados:
                    nueva_ruta = ruta + [vecino]
                    
                    if vecino == destino:
                        return {
                            'success': True,
                            'ruta': nueva_ruta,
                            'distancia': len(nueva_ruta) - 1
                        }
                    
                    visitados.add(vecino)
                    cola.append((vecino, nueva_ruta))
        
        return {
            'success': False,
            'error': 'No hay ruta entre los municipios'
        }

# Instancia única
graph_service = GraphService()