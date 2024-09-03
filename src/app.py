import pandas as pd
from flask import Flask, jsonify, request
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
import os
import json

def load_pipeline(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Pipeline not found at {path}")
    try:
        return PipelineModel.load(path)
    except Exception as e:
        raise Exception(f"Error loading pipeline: {str(e)}")


app = Flask(__name__)
spark = SparkSession.builder.appName("ModelService").getOrCreate()

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
PIPELINE_PATH = "models/pipeline"


@app.route('/health', methods=['GET'])
def health():
    try:
        return jsonify({
            'status': 'ok',
            'message': 'API is working fine :)'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/model/predict', methods=['POST'])
def predict():
    pipeline = load_pipeline(PIPELINE_PATH)

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    df = spark.createDataFrame(pd.DataFrame([data]))

    predictions = pipeline.transform(df)
    
    predictions_json = predictions.select("prediction").toPandas().to_dict(orient="records")
    
    return jsonify(predictions_json)

@app.route('/model/load', methods=['POST'])
def load():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    try:
        model_path = data.get('model_path')
        if not model_path:
            return jsonify({'error': 'Model path not provided'}), 400
        model = load_pipeline(model_path)
        model.write().overwrite().save(PIPELINE_PATH)
        return jsonify({"message": "Model successfully loaded"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/model/history', methods=['GET'])
def history():
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


