from flask import Blueprint, jsonify, request

# import sys
# sys.path.append("..")

api = Blueprint('api', __name__)

from machine_learning import nlp
from machine_learning import distancias as dis

datos = nlp.importarCSV("https://raw.githubusercontent.com/sebas979/archicosCSV/main/DataSet.csv");
mT,mK,mA,M=dis.matricesDistancia(datos)

@api.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message='¡Hola, mundo desde Flask!')

@api.route('/echo/<string:message>', methods=['GET'])
def echo_message(message):
    return jsonify(message=message)

@api.route('/matrices', methods=['POST'])
def matrices():
    if request.method == 'POST':
        # data = request.data
        # data = request.form['data']
        # print(request.data)


        
        print(request.form)
        print('=========================')
        return True
    # print(data)
    # print(type(data))
    # print('matriz completa')
    # print(M)