#create a class called WindImporter
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, FloatType

from apis.airportdb import AirportDB
from apis.weatherbit import WeatherBitDB
from pyspark.sql import Row
from pyspark.sql.functions import col, date_format, date_add



class WindImporter:
    #create a function called import_wind that takes in self and data as input

    @staticmethod
    def create_location_udf(location_dict):
        def get_location(airport_code):
            return location_dict.get(airport_code, None)
        
        return udf(get_location, ArrayType(FloatType()))


    @classmethod
    def import_wind(cls, data):
        origins = data.select('origin').distinct()
        dests = data.select('dest').distinct()
        dests = dests.withColumnRenamed('dest', 'origin')
        unique_locations = origins.union(dests).distinct()
        location_list = [row['origin'] for row in unique_locations.collect()]

        location_dict = AirportDB.get_airport_data(location_list)

        get_location_udf = cls.create_location_udf(location_dict)

        df_with_coordinates = data.withColumn("origin_coordinates", get_location_udf(data["origin"]))


        df_weather = df_with_coordinates.withColumn(
                "start_date", date_format(col("time_hour"), "yyyy-MM-dd")
            ).withColumn(
                "end_date", date_format(date_add(col("time_hour"),1), "yyyy-MM-dd")  #1 day after start_date
            ).select(
                col("origin_coordinates").alias("coordinates"),
                col("start_date"),
                col("end_date")
            )

        data_to_send = df_weather.rdd.map(lambda row: (
            row["coordinates"][0],  # latitude
            row["coordinates"][1],  # longitude
            row["start_date"],
            row["end_date"]
        )).collect()


        weather_rows = [
            Row(
                lat=lat,
                lon=lon,
                start_date=start_date,
                end_date=end_date,
                wind_spd=wind_spd
            )
            for (lat, lon, start_date, end_date), wind_spd in weather_data.items()
        ]

        # Criar um DataFrame a partir da lista de Rows
        df_weather = spark.createDataFrame(weather_rows)
        

        df_with_coords_alias = df_with_coordinates.alias("df_coords")
        df_weather_alias = df_weather.alias("df_weather")

        # Realizando a junção com os alias
        df_final = df_with_coords_alias.join(
            df_weather_alias,
            (col("df_coords.origin_coordinates")[0] == col("df_weather.lat")) &
            (col("df_coords.origin_coordinates")[1] == col("df_weather.lon")) &
            (col("df_coords.start_date") == col("df_weather.start_date")) &
            (col("df_coords.end_date") == col("df_weather.end_date")),
            "left"
)
        
        return data
    
    