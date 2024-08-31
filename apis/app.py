from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

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


#config routes
@app.route('/model/predict', methods=['POST'])
def predict():
    return jsonify({'prediction': 'prediction'})

@app.route('/model/load', methods=['POST'])
def load():
    return jsonify({'model': 'model'})

@app.route('/model/history', methods=['GET'])
def history():
    return jsonify({'history': 'history'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'health': 'health'})
