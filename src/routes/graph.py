from flask import Blueprint, jsonify, request
from services.graph_service import graph_service

routes_graph = Blueprint("routes_graph", __name__, url_prefix='/api')

@routes_graph.route('/municipios', methods=['GET'])
def get_municipios():
    try:
        municipios = graph_service.obtener_municipios()
        return jsonify({
            'success': True,
            'data': municipios,
            'total': len(municipios)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@routes_graph.route('/grafo', methods=['GET'])
def get_grafo():
    try:
        grafo = graph_service.obtener_grafo()
        return jsonify({'success': True, 'data': grafo})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@routes_graph.route('/buscar-ruta', methods=['POST'])
def buscar_ruta():
    try:
        data = request.get_json()
        origen = data.get('origen')
        destino = data.get('destino')
        
        if not origen or not destino:
            return jsonify({
                'success': False,
                'error': 'Se requieren origen y destino'
            }), 400
        
        resultado = graph_service.buscar_ruta_bfs(origen, destino)
        status_code = 200 if resultado['success'] else 404
        
        return jsonify(resultado), status_code
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500