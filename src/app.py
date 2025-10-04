from flask import Flask, jsonify
from flask_cors import CORS
from routes import api_bp

app = Flask(__name__)
CORS(app)

# Registrar rutas
app.register_blueprint(api_bp)

@app.route('/')
def index():
    return jsonify({
        'message': '¡Hola Mundo!',
        'status': 'ok',
        'api': 'BFS Municipios'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)