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

@api.route('/heatmap', methods=['POST'])
def matrices():
    if request.method == 'POST':
        collections = json.loads(request.data)
        collections_matrix = pd.DataFrame(collections['data'])
        mT,mK,mA,M = fun.matricesDistancia(collections_matrix)

        #### diccionario heat map
        xaxis, yaxis, heat_map = fun.get_heat_map_data(M)

        # #### JSON
        matriz_general_str = json.dumps(M.tolist())
        dict_heat_map = json.dumps(heat_map)
        dict_xaxis = json.dumps(xaxis)
        dict_yaxis = json.dumps(yaxis)
        
        return {'matriz': matriz_general_str, 
                'xaxis_data': dict_xaxis, 
                'yaxis_data': dict_yaxis, 
                'heat_map_data': dict_heat_map}

@api.route('/cluster', methods=['POST'])
def cluster():
    if request.method == 'POST':
        collections = json.loads(request.data)
        collections_matrix = pd.DataFrame(collections['data'])
        mT,mK,mA,M = fun.matricesDistancia(collections_matrix)

        cluster_data = fun.get_cluster_data(M,4)

        return {'cluster': json.dumps(cluster_data)}


@api.route('/mds', methods=['POST'])
def mds():
    if request.method == 'POST':
        collections = json.loads(request.data)
        collections_matrix = pd.DataFrame(collections['data'])
        mT,mK,mA,M = fun.matricesDistancia(collections_matrix)

        mds_data = fun.get_scatter_data(M)

        return {'mds': json.dumps(mds_data)}