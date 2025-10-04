from flask import Blueprint, jsonify, request
from services.graph_service import graph_service

routes_graph = Blueprint("routes_graph",__name__, url_prefix='/api')

@routes_graph.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'success': True,
        'status': 'ok'
    })

@routes_graph.route('/crear-grafo', methods=['POST'])
def crear_grafo():
    """
    Crea el grafo con las conexiones enviadas
    
    Body JSON:
    {
        "conexiones": [
            ["Barranquilla", "Soledad"],
            ["Barranquilla", "Malambo"],
            ["Soledad", "Sabanagrande"]
        ]
    }
    """
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        data = request.get_json()
        conexiones = data.get('conexiones')
        
        if not conexiones:
            return jsonify({
                'success': False,
                'error': 'Se requiere el campo "conexiones"'
            }), 400
        
        if not isinstance(conexiones, list):
            return jsonify({
                'success': False,
                'error': 'Las conexiones deben ser una lista'
            }), 400
        
        # Convertir a tuplas
        conexiones_tuplas = [tuple(c) for c in conexiones]
        
        resultado = graph_service.crear_grafo(conexiones_tuplas)
        return jsonify(resultado), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@routes_graph.route('/municipios', methods=['GET'])
def get_municipios():
    """Obtiene todos los municipios"""
    try:
        municipios = graph_service.obtener_municipios()
        return jsonify({
            'success': True,
            'data': municipios,
            'total': len(municipios)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@routes_graph.route('/grafo', methods=['GET'])
def get_grafo():
    """Obtiene el grafo completo"""
    try:
        grafo = graph_service.obtener_grafo()
        return jsonify({
            'success': True,
            'data': grafo
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@routes_graph.route('/buscar-ruta', methods=['POST'])
def buscar_ruta():
    """
    Busca ruta entre dos municipios
    
    Body JSON:
    {
        "origen": "Barranquilla",
        "destino": "Santo Tomas"
    }
    """
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        data = request.get_json()
        origen = data.get('origen')
        destino = data.get('destino')
        
        if not origen or not destino:
            return jsonify({
                'success': False,
                'error': 'Se requieren "origen" y "destino"'
            }), 400
        
        resultado = graph_service.buscar_ruta_bfs(origen, destino)
        
        if resultado['success']:
            return jsonify(resultado), 200
        else:
            return jsonify(resultado), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500