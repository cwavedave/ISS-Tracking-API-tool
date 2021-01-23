import requests
import pandas as pd
import datetime as dt

now = dt.datetime.now()
countries_csv = pd.read_csv("countries.csv", sep='\s*,\s*', engine='python')
df = pd.DataFrame(countries_csv)
df['latitude'] = df['latitude'].astype(float)

def get_iss_location():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["longitude"])
    return (latitude,longitude)

iss_location = get_iss_location()
print(f"ISS locations is {(iss_location)}")

latitudes = df['latitude'].to_list()
longitudes = df['longitude'].to_list()

for l in latitudes:
    if isinstance(l,str):
        print("String Located")

nearby_countries = df[df['longitude'].between(iss_location[1] -15, iss_location[1] + 15) & df['latitude'].between(iss_location[0] -15, iss_location[0] + 15)]

# Current limited use is, must be near the center of the country.
countries_nearby_list = nearby_countries['name'].to_list()

if len(countries_nearby_list) != 0:
    print(countries_nearby_list)
    print(f"Number of nearby countries - {len(countries_nearby_list)}")

vic_lo = 2.25486
vic_la = 41.93012

#Suntimes API
response = requests.get(url=f'https://api.sunrise-sunset.org/json?lat={vic_la}&lng={vic_lo}&formatted=0')
sun_times = response.json()

# print(sun_times)

current_time = int(str(now).split(' ')[1].split('.')[0][:-3].replace(":",""))
# print(current_time)

sunrise = int(sun_times["results"]["sunrise"].split("T")[1].split("+")[0][:-3].replace(":",""))
sunset = int(sun_times["results"]["sunset"].split("T")[1].split("+")[0][:-3].replace(":",""))

if sunset > current_time:
    print(f"Current time is {sunrise}")
    time_until_sunset = sunset - current_time
    print(time_until_sunset)
    if len(str(time_until_sunset)) <= 2:
        print(f"{time_until_sunset} Minutes left until sunset in Vic")
    else:
        print(f"Calculate time until sunset in Vic - {str(time_until_sunset)[:-2] + ':' + list(str(time_until_sunset))[1] + list(str(time_until_sunset))[2]}")
    print(f"Sunset time is {sunset}")

if sunrise > current_time:
    print("Time until Sunrise ( Morning ) ")

if sunrise < current_time and sunset < current_time:
    sunrise_time_tomorrow = 2400 - current_time + sunrise
    print(f"Time until sunrise tomorrow {sunrise_time_tomorrow}")

if len(str(sunrise)) == 3:
    print(f"Sunrise time is {str(sunrise)[:-2] + ':' + list(str(sunrise))[1] + list(str(sunrise))[2]}")

else:
    print(f"Sunrise time is {str(sunrise)[:-2] + ':' + list(str(sunrise))[2] + list(str(sunrise))[3]}")

print(f"Sunset time is {str(sunset)[:-2] + ':' + list(str(sunset))[2] + list(str(sunset))[3]}")
