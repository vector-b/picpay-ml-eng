from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, FloatType
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import col, date_format, date_add
from pyspark.sql.types import StructType, StructField, DoubleType, StringType
from pyspark.sql import functions as F
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from apis.airportdb import AirportDB
from apis.weatherbit import WeatherBitDB

class WindImporter:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    @staticmethod
    def create_location_udf(location_dict):
        def get_location(airport_code):
            return location_dict.get(airport_code, None)
        
        return udf(get_location, ArrayType(FloatType()))


    def import_wind(self, data):
        origins = data.select('origin').distinct()
        dests = data.select('dest').distinct()
        dests = dests.withColumnRenamed('dest', 'origin')
        unique_locations = origins.union(dests).distinct()
        location_list = [row['origin'] for row in unique_locations.collect()]

        location_dict = AirportDB.get_airport_data(location_list)

        get_location_udf = self.create_location_udf(location_dict)

        df_with_coordinates = data.withColumn("origin_coordinates", get_location_udf(data["origin"]))

        df_unique_weather_requests = df_with_coordinates.select([
            col("origin_coordinates"),
            date_format(col("time_hour"), "yyyy-MM-dd").alias("start_date"),
            date_format(date_add(col("time_hour"), 1), "yyyy-MM-dd").alias("end_date")
        ]).dropDuplicates()

        lat_lon_dates = df_unique_weather_requests.rdd.map(lambda row: (
            row['origin_coordinates'][0],  
            row['origin_coordinates'][1],  
            row['start_date'],             
            row['end_date']                
        )).collect()

        weather_data = WeatherBitDB.get_weather_list(lat_lon_dates)

        weather_list = [(lat, lon, date, float(wind_speed)) for (lat, lon, date, _), wind_speed in weather_data.items()]

        schema = StructType([
            StructField("lat", DoubleType(), False),
            StructField("lon", DoubleType(), False),
            StructField("date", StringType(), False),
            StructField("wind_speed", DoubleType(), False)
        ])

        weather_df = self.spark.createDataFrame(weather_list, schema)

        df_with_coordinates = df_with_coordinates.withColumn("date", F.date_format(F.col("time_hour"), "yyyy-MM-dd"))

        df_with_lat_lon = df_with_coordinates.withColumn("lat", F.col("origin_coordinates")[0]) \
                                     .withColumn("lon", F.col("origin_coordinates")[1])
        
        df_final = df_with_lat_lon.join(weather_df, on=["lat", "lon", "date"], how="left")
        return data
    
    