import requests
import pandas as pd
import datetime as dt

now = dt.datetime.now()
countries_csv = pd.read_csv("countries.csv", sep='\s*,\s*', engine='python')
df = pd.DataFrame(countries_csv)
df['latitude'] = df['latitude'].astype(float)

# Calling Sun Times API
def get_sun(lat,long):
    response = requests.get(url=f'https://api.sunrise-sunset.org/json?lat={lat}&lng={long}&formatted=0')
    sun_times = response.json()
    return sun_times

def user_input():
    user_latitude = input("Enter Latitude\n")
    user_longitude = input("Enter longitude\n")
    question = input("Do you want email alerts when the ISS is visible from your location?")
    if question.lower() == "y":
        user_email = input("What is your email address?")
        return (user_latitude,user_longitude,user_email)
    else:
        return (user_latitude,user_longitude)

user = user_input()
user_la = user[0]
user_lo = user[1]
print(len(user_input()))


def get_iss_location():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["longitude"])
    return (latitude,longitude)

iss_location = get_iss_location()
print(f"ISS locations is {(iss_location)}\n")

latitudes = df['latitude'].to_list()
longitudes = df['longitude'].to_list()

# Bug Catcher used earlier for finding formatting issue in data
# for l in latitudes:
#     if isinstance(l,str):
#         print("String Located")

nearby_countries = df[df['longitude'].between(iss_location[1] -5, iss_location[1] + 5) & df['latitude'].between(iss_location[0] -5, iss_location[0] + 5)]

# Current limited use is, must be near the center of the country.
countries_nearby_list = nearby_countries['name'].to_list()

country_list = []

def nearby_countries():
    for country in countries_nearby_list:
        country_add = df.loc[(df['name'] == country)]
        country_name = country_add['name'].item()
        country_latitude = country_add['latitude'].item()
        country_longitude = country_add['longitude'].item()
        direction = []
        if iss_lat < country_latitude:
            direction.append("North")
        else:
            direction.append("South")
        if iss_long < country_longitude:
            direction.append("East")
        else:
            direction.append("West")

        country = {country_name: country_add['name'].item(), 'Latitude': country_add['latitude'].item(), 'Longitude':country_add['longitude'].item(),
                   "Direction": f"{' '.join(direction)} of ISS"}
        country_list.append(country)

iss_lat = get_iss_location()[0]
iss_long = get_iss_location()[1]

def direction_NS(iss_lat, country_location):
    if iss_lat > country_location['latitude']:
        print(f"ISS is North of {country_location['name']}")
        return "North"
    else:
        print("South")
        return "South"

def direction_WE(iss_long, country_location):
    if iss_lat > country_location['latitude']:
        print(f"ISS is North of {country_location['name']}")
        return "North"
    else:
        print("South")
        return "South"

#Check if there are countries nearby
if len(countries_nearby_list) != 0:
    # print(countries_nearby_list)
    print("=====================================================================================")
    print(f"Number of nearby countries nearby the ISS - {len(countries_nearby_list)}")
    nearby_countries()
    print("=====================================================================================")
    print(country_list)
else:
    print("=====================================================================================")
    print(f"ISS NOT CURRENTLY LOCATED CLOSE ENOUGH TO CENTER OF ANY COUNTRY FOR REFERENCE")
    nearby_countries()
    print("=====================================================================================")


print("\n=====================================================================================")
print("Current Location Data")
print("=====================================================================================")

#Suntimes API

def local(user_la, user_lo):
    #GET CURRENT TIME
    current_time = int(str(now).split(' ')[1].split('.')[0][:-3].replace(":",""))
    sun_times = get_sun(user_la,user_lo)
    # print(current_time)

    #SUNRISE FORMATTING INTO DIGITS
    sunrise = int(sun_times["results"]["sunrise"].split("T")[1].split("+")[0][:-3].replace(":",""))
    sunset = int(sun_times["results"]["sunset"].split("T")[1].split("+")[0][:-3].replace(":",""))

    #SUNSET IN LOCATION
    if sunset > current_time:
        print(f"Current time is {sunrise}")
        time_until_sunset = sunset - current_time
        print(time_until_sunset)
        if len(str(time_until_sunset)) <= 2:
            print(f"{time_until_sunset} Minutes left until sunset in Vic")
        else:
            print(f"Calculate time until sunset in Vic - {str(time_until_sunset)[:-2] + ':' + list(str(time_until_sunset))[1] + list(str(time_until_sunset))[2]}")
        print(f"Sunset time is {sunset}")

    #SUNRISE IN LOCATION
    if sunrise > current_time:
        print("Time until Sunrise ( Morning ) ")

    #TIME UNTIL SUNRISE TOMORROW
    if sunrise < current_time and sunset < current_time:
        sunrise_time_tomorrow = 2400 - current_time + sunrise
        print(f"Time until sunrise tomorrow {sunrise_time_tomorrow}")

    #FORMATTING FOR TIME OUTPUT
    if len(str(sunrise)) == 3:
        print(f"Sunrise time is {str(sunrise)[:-2] + ':' + list(str(sunrise))[1] + list(str(sunrise))[2]}")
    else:
        print(f"Sunrise time is {str(sunrise)[:-2] + ':' + list(str(sunrise))[2] + list(str(sunrise))[3]}")

    #SUNSET TIME - ALWAYS 4 DIGITS LONG
    print(f"Sunset time is {str(sunset)[:-2] + ':' + list(str(sunset))[2] + list(str(sunset))[3]}")

local(user_la,user_lo)