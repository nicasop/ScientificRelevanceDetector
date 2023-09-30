from flask import Blueprint, jsonify, request

import json
import pandas as pd

# import sys
# sys.path.append("..")

api = Blueprint('api', __name__)

from machine_learning import nlp
from machine_learning import distancias as dis
from machine_learning import functions as fun

# datos = nlp.importarCSV("https://raw.githubusercontent.com/sebas979/archicosCSV/main/DataSet.csv");
# mT,mK,mA,M=dis.matricesDistancia(datos)

@api.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message='¡Hola, mundo desde Flask!')

@api.route('/echo/<string:message>', methods=['GET'])
def echo_message(message):
    return jsonify(message=message)

@api.route('/matrices', methods=['POST'])
def matrices():
    if request.method == 'POST':
        collections = json.loads(request.data)

        # datos_test = nlp.importarCSV("https://raw.githubusercontent.com/Freddy8-C/Proyecto_MachineLearning/master/csv/Proyecto.csv")
        # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # print(datos_test)

        collections_matrix = pd.DataFrame(collections['data'])

        # mT1,mK1,mA1,M1=dis.matricesDistancia(collections_matrix)

        mT,mK,mA,M = fun.matricesDistancia(collections_matrix)

        # print('========================= matriz de titulos')
        # print(mT1)
        # print('========================= matriz general')
        # print(M1)


        # mT,mK,mA,M = fun.matricesDistancia(datos_test)

        # print('========================= matriz de titulos')
        # print(mT)
        print('========================= matriz general')
        # print(M)
        # print(type(M))

        #### transformar matriz numpy a array y a json
        json_str = json.dumps(M.tolist())
        
        print(json_str)



        return {'matriz': json_str}
