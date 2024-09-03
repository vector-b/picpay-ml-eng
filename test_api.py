test_list = ['LGA', 'EWR', 'JFK', 'PSE', 'MSY']

from apis.airportdb import AirportDB

#AirportDB.get_airport_data(test_list)

from apis.weatherbit import WeatherBitDB

test_list_2 = [(40.692501068115234, -74.168701171875, '2013-01-01', '2013-01-02'),
 (40.777198791503906, -73.87259674072266, '2013-01-01', '2013-01-02')]

list  = WeatherBitDB.get_weather_list(test_list_2)
print(list)