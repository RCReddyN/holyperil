from dotenv import load_dotenv
load_dotenv()

import os
from datetime import date
import requests
import json

class Holyperil:
    def __init__(self, token, today):
        self.token = token
        self.today = today
        self.days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
        self.url_str = 'https://api.nasa.gov/neo/rest/v1/feed?'
        self.no_of_pot_hazards = 0
        self.data_str = ''

    def is_leap_year(self, year):
        return (year % 400 == 0) or (year % 400 !=0 and (year % 100 == 0 or year % 4 == 0))

    def week_later(self, date):
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:10])
    
        if self.is_leap_year(year):
            days[2] = 29

        day = day + 6

        if self.days[month] < day:
            day = day % days[month]
            month += 1
    
        if month > 12:
            month = month % 12
            year += 1
         
        return str(year) + "-" + str(month) + "-" + str(day)

    def get_params(self):
        return { 'start_date' : self.week_later(self.today),
                        'end_date' : self.week_later(self.today),
                        'api_key' : self.token}

    def get_data(self):
        r = requests.get(url=self.url_str, params=self.get_params())
        data = r.json()
        asteroids = data['near_earth_objects']
        for asteroid in asteroids:
            for field in asteroids[asteroid]:
                try:
                    if field['is_potentially_hazardous_asteroid']:
                        self.no_of_pot_hazards += 1
                        self.data_str += ('Asteroid name: ' + field['name']) +'\n'
                        self.data_str += ('Estimated Diameter: ' + str((field['estimated_diameter']['meters']['estimated_diameter_min'] + field['estimated_diameter']['meters']['estimated_diameter_max'])/2)) +'\n'
                        self.data_str += ('Close Approach Date and Time: ' + field['close_approach_data'][0]['close_approach_date_full']) +'\n'
                        self.data_str += ('Velocity: ' + str(field["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]) + " km/h") +'\n'
                        self.data_str += ('Distance to Earth: ' + str(field["close_approach_data"][0]["miss_distance"]["kilometers"]) + " km") +'\n'
                        self.data_str += '\n'
                except:
                    self.data_str += ('Unable to access all data.') +'\n'

def main():
    token = os.environ.get("api-token")
    today = str(date.today())
    instance = Holyperil(token, today)
    instance.get_data()
    if instance.no_of_pot_hazards > 0:
        print('The date is '+ today+ '.')
        print(instance.no_of_pot_hazards, 'potentially hazardous asteroid(s) are approaching Earth.')
        print('You have six days to do something about it if something goes wrong.')
        print('The seventh day is Doomsday.')
        print()
        print(instance.data_str)
    elif self.no_of_pot_hazards == 0:
        print('You can rest, no observable threat.')

if __name__=='__main__':
    main()    
