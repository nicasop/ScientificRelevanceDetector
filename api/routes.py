from flask import Blueprint, jsonify, request

import json
import pandas as pd

# import sys
# sys.path.append("..")

api = Blueprint('api', __name__)

from machine_learning import functions as fun

@api.route('/papers', methods=['POST'])
def papers():
    if request.method == 'POST':
        collections = json.loads(request.data)
        collections_matrix = pd.DataFrame(collections['data'])
        mT,mK,mA,M = fun.matricesDistancia(collections_matrix)

        return {
            'weighted_matrix': json.dumps(M.tolist()),
            'titles_matrix': json.dumps(mT.tolist()),
            'keywords_matrix': json.dumps(mK.tolist()),
            'abstracts_matrix': json.dumps(mA.tolist())
        }


@api.route('/heatmap', methods=['POST'])
def heatmap():
    if request.method == 'POST':
        send_data = json.loads(request.data)
        weighted_matrix = json.loads(send_data['data'])

        xaxis, yaxis, heat_map = fun.get_heat_map_data(weighted_matrix)
        
        return {'xaxis': xaxis, 
                'yaxis': yaxis, 
                'data': heat_map}

@api.route('/cluster', methods=['POST'])
def cluster():
    if request.method == 'POST':
        send_data = json.loads(request.data)
        weighted_matrix = json.loads(send_data['data'])

        cluster_data = fun.get_cluster_data(weighted_matrix,4)

        return cluster_data


@api.route('/mds', methods=['POST'])
def mds():
    if request.method == 'POST':
        send_data = json.loads(request.data)
        weighted_matrix = json.loads(send_data['data'])

        mds_data = fun.get_scatter_data(weighted_matrix)

        return mds_data