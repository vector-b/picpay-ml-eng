from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession, DataFrame
from pyspark.ml.evaluation import RegressionEvaluator


class ModelTrainer:
    def __init__(self, X_columns, y_column):
        self.X_columns = X_columns
        self.y_column = y_column

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
        
        # return rmse and predictions
        return rmse, predictions.select(self.y_column, "prediction")