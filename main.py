from flask import Flask
from flask_cors import CORS

from api.routes import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')

##configurar cors
# cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}) ##acceso limitado a url especificas
cors = CORS(app) # acceso a todas las urls

if __name__ == '__main__':
    app.run(debug=True, port=4000)
