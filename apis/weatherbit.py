"1f22b701b6904b66a169a5f52eddbed4"

import requests
import json

class WeatherBitDB:
    ApiToken = '1f22b701b6904b66a169a5f52eddbed4'

    @classmethod
    def get_weather(cls, lat, lon, start_date, end_date):
        url = 'https://api.weatherbit.io/v2.0/history/daily'
        params = {
        'lat': lat,
        'lon': lon,
        'start_date': start_date,
        'end_date': end_date,
        'key': cls.ApiToken,
        }
        headers = {
        'Accept': 'application/json',
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @classmethod
    def get_weather_list(cls, lat_lon_list, start_date, end_date):
        weather_data = {}
        for lat, lon in lat_lon_list:
            data = cls.get_weather(lat, lon, start_date, end_date)
            if data:
                weather_data[(lat, lon)] = data
        return weather_data