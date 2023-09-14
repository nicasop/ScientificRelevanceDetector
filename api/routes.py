from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message='¡Hola, mundo desde Flask!')

@api.route('/echo/<string:message>', methods=['GET'])
def echo_message(message):
    return jsonify(message=message)