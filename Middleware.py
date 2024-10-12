from flask import Flask, request, jsonify
from functools import wraps
import jwt

app = Flask(__name__)

# Clave secreta para firmar los tokens JWT
SECRET_KEY = 'super_secret_key'

# Middleware de autenticación
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user']
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(current_user, *args, **kwargs)
    return decorated

# Ruta para iniciar sesión y generar el token JWT
@app.route('/login', methods=['POST'])
def login():
    auth_data = request.json

    if auth_data['username'] == 'admin' and auth_data['password'] == 'admin':
        token = jwt.encode({'user': 'admin', 'role': 'admin'}, SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})
    
    return jsonify({'message': 'Invalid credentials!'}), 401

# Ruta protegida solo accesible por usuarios autenticados
@app.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    if current_user['role'] == 'admin':
        return jsonify({'tasks': 'All tasks for admin'})
    else:
        return jsonify({'tasks': 'Tasks for regular user'})

if __name__ == '__main__':
    app.run(debug=True)
