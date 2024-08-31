from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession, DataFrame
from pyspark.ml.evaluation import RegressionEvaluator
from datetime import datetime
import json 
import os 


class ModelTrainer:
    def __init__(self, X_columns, y_column):
        self.X_columns = X_columns
        self.y_column = y_column

    def _save_predictions_json(self, predictions: DataFrame, path: str):
        # Converter DataFrame para pandas DataFrame
        pd_predictions = predictions.toPandas()
        
        # Convert pandas DataFrame para lista de dicionários
        predictions_list = pd_predictions.to_dict(orient="records")
        
        # Obter o timestamp da predição
        prediction_time = datetime.now().isoformat()
        
        # Estruturar os dados finais
        final_output = {
            "prediction_time": prediction_time,
            "predictions": predictions_list
        }
        
        # Verificar se o arquivo já existe
        if os.path.exists(path):
            with open(path, "r") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {"predictions": []}
        else:
            existing_data = {"predictions": []}
        
        # Adicionar as novas previsões ao arquivo existente
        existing_data["predictions"].append(final_output)
        
        # Salvar os dados atualizados no arquivo
        with open(path, "w") as f:
            json.dump(existing_data, f, indent=4)

    def create_pipeline(self):
        assembler = VectorAssembler(inputCols=self.X_columns, outputCol="features")
        
        rf = RandomForestRegressor(featuresCol="features", labelCol=self.y_column)
        
        pipeline = Pipeline(stages=[assembler, rf])
        
        return pipeline

    def train(self, pipeline, train_data: DataFrame):
        return pipeline.fit(train_data)

    def evaluate(self, model, test_data: DataFrame):
        predictions = model.transform(test_data) 
    
        evaluator = RegressionEvaluator(labelCol=self.y_column, predictionCol="prediction", metricName="rmse")
        rmse = evaluator.evaluate(predictions)
        
        # Selecionar as colunas relevantes
        predicted = predictions.select(self.y_column, "prediction")

        # Salvar as previsões no arquivo JSON
        self._save_predictions_json(predicted, "logs/predictions.json")
        
        # Retornar RMSE e previsões
        return rmse, predicted