import requests
import json

class AirportDB:
    ApiToken = '757e363e492fbb6df56bd03e4f6c123a93f24e3742f98843bd8cb0324ee63fcdf68f360c2744edc250109ad53dae7417'

    @classmethod
    def get_airport_data(cls, codes):
        airport_data = {}
        for code in codes:
            url = f"https://airportdb.io/api/v1/airport/K{code}?apiToken={cls.ApiToken}"
            response = requests.get(url)

            #print(f"Requisição para {code}: Status Code - {response.status_code}")
            #print("Resposta da API:", response.text)

            if response.status_code == 200:
                latitude = response.json()["latitude_deg"]
                longitude = response.json()["longitude_deg"]
                airport_data[code] = (latitude, longitude)
        return airport_data