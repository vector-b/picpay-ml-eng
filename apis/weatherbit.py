import requests
from dotenv import load_dotenv
import os

dotenv_path = 'config/.env'  # Substitua pelo caminho correto
load_dotenv(dotenv_path)
class WeatherBitDB:
    #Get the API key from the environment .env file in config/.env
    ApiToken = os.getenv('WEATHER_KEY')
    

    # Get weather for a specific lat, lon, date tuple!
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

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # levanta exceção para status codes de erro
            data = response.json()

            if 'data' in data and len(data['data']) > 0:
                return data['data'][0]['wind_spd']
            else:
                print(f"Not found {lat}, {lon} between {start_date} and {end_date}.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")
            return None

    # Get weather for a list of lat, lon, date tuples!
    @classmethod
    def get_weather_list(cls, lat_lon_dates):
        weather_data = {}
        for lat_lon_date in lat_lon_dates:
            lat, lon, start_date, end_date = lat_lon_date
            wind_speed = cls.get_weather(lat, lon, start_date, end_date)
            weather_data[(lat, lon, start_date, end_date)] = wind_speed
        return weather_data
