from flask import Flask, jsonify, render_template
from flask_cors import CORS
from routes.graph import routes_graph 

app = Flask(__name__)
CORS(app)

# Registrar rutas
app.register_blueprint(routes_graph)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api_info():
    return jsonify({
        'message': 'API BFS Municipios',
        'status': 'ok',
        'endpoints': [
            '/api/municipios',
            '/api/grafo',
            '/api/buscar-ruta'
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)