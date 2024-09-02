from pyspark.sql import SparkSession
from preprocess_data import PreprocessData
from model_trainer import ModelTrainer
import datetime
import os


if __name__ == "__main__":
    spark = SparkSession.builder.appName("FlightModel").getOrCreate()
    
    preprocessor = PreprocessData(spark)
    path = "data/airports-database.csv"

    data = preprocessor.read_data(path)
    
    processed_data = preprocessor.preprocess(data)

    train_data, test_data = preprocessor.split_data(processed_data)

    trainer = ModelTrainer(X_columns=["distance", "dep_delay", "air_time"], y_column="arr_delay")

    pipeline = trainer.create_pipeline()

    model = trainer.train(pipeline, train_data)

    model_path = "models/trained_models/model-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    trainer.save_model(model, model_path)

    rmse, predictions = trainer.evaluate(model, test_data)

    print(f"RMSE: {rmse}")
    predictions.show()