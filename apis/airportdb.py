import requests
import json
from dotenv import load_dotenv
import os

dotenv_path = 'config/.env'  # Substitua pelo caminho correto
load_dotenv(dotenv_path)
class AirportDB:
    #Get the API key from the environment .env file in config
    ApiToken = os.getenv('AIRPORT_KEY')

    @classmethod
    def get_airport_data(cls, codes):
        airport_data = {}
        for code in codes:
            url = f"https://airportdb.io/api/v1/airport/K{code}?apiToken={cls.ApiToken}"
            response = requests.get(url)

            #print(f"Requisição para {code}: Status Code - {response.status_code}")
            #print("Resposta da API:", response.text)

            #If the response is successful, get the latitude and longitude
            if response.status_code == 200:
                latitude = response.json()["latitude_deg"]
                longitude = response.json()["longitude_deg"]
                airport_data[code] = (latitude, longitude)
        return airport_data