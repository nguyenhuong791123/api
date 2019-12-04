from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import ( JWTManager )

from auth import auth
from urls import fileapi

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

app.register_blueprint(auth.app)
app.register_blueprint(fileapi.app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8085)