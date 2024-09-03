from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, udf

class PreprocessData:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def read_data(self, path: str) -> DataFrame:
        return self.spark.read.csv(path, header=True, inferSchema=True)
    
    def preprocess(self, data: DataFrame) -> DataFrame:
        data = data.filter(data["dep_time"].isNotNull() | data["arr_time"].isNotNull())
        data = data.dropna()
        #data = WindImporter().import_wind(data)
        return data

    def split_data(self, data: DataFrame):
        return data.randomSplit([0.8, 0.2])
    
    def split_X_y(self, data: DataFrame, X_columns:str, y_column: str):
        return data.select(X_columns), data.select(y_column)

