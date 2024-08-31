from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import json

app = Flask(__name__)

'''
/model/predict/
    Endpoint onde deverá receber um payload com as informações do voo e retornar a previsão do atraso no destino
/model/load/
    Endpoint onde deverá receber o arquivo .pkl do modelo e deixar a API pronta para realizar predições
/model/history/
    Endpoint onde deverá exibir o histórico de predições realizadas (o payload de entrada + as saídas preditas)
/health/
    Endpoint que irá retornar a saúde da API'''

PATH_TO_PREDICTIONS = "logs/predictions.json"
PATH_TO_MODEL = "model.pkl"

#config routes
@app.route('/model/predict', methods=['POST'])
def predict():
    return jsonify({'prediction': 'prediction'})

@app.route('/model/load', methods=['POST'])
def load():
    return jsonify({'model': 'model'})

@app.route('/model/history', methods=['GET'])
def history():
    #get data from json file using PATH_TO_PREDICTIONS 

    if not os.path.exists(PATH_TO_PREDICTIONS):
        return jsonify({"error": "No predictions found"}), 404
    else:
        with open(PATH_TO_PREDICTIONS, 'r') as file:
            try:
                data = json.load(file)
                return jsonify(data), 200
            except json.JSONDecodeError:
                return jsonify({"error": "Error reading predictions file"}), 500
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'health': 'health'})
