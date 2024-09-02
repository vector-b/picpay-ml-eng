test_list = ['LGA', 'EWR', 'JFK', 'PSE', 'MSY']

from apis.airportdb import AirportDB

AirportDB.get_airport_data(test_list)