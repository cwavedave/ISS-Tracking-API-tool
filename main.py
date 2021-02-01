import requests
import pandas as pd
import datetime as dt
import time
import smtplib
import json

CLIENT_EMAIL = ""
CLIENT_PASSWORD = ""

program = True
email = "david@creativewavelength.co.uk"

now = dt.datetime.now()
countries_csv = pd.read_csv("countries.csv", sep='\s*,\s*', engine='python')
df = pd.DataFrame(countries_csv)
df['latitude'] = df['latitude'].astype(float)

# Calling Sun Times API
def get_sun(lat,long):
    response = requests.get(url=f'https://api.sunrise-sunset.org/json?lat={lat}&lng={long}&formatted=0')
    sun_times = response.json()
    return sun_times

#COLLECTS USER LAT / LONG & ASKS IF THEY WANT TO SUBMIT EMAIL FOR ALERTS. SAVES DATA TO JSON IF YES.
def user_input():
    user = {}
    search = False
    while search == False:
        search_area = input("Type in your country name / ISO code. \nOr type 'manual', if you want to use your own coordinates\n")

        if len(df.loc[(df['name'] == search_area.title())]) > 0:
            matched_result = df.loc[(df['name'] == search_area.title())]
            user_latitude = matched_result['latitude'].item()
            user_longitude = matched_result['longitude'].item()
            print(f"Database entry for {matched_result['name'].item()} used for latitude ({user_latitude}) & longitude({user_longitude})")
            search = True

        elif len(df.loc[(df['country'] == search_area.upper())]) > 0:
            matched_result = df.loc[(df['country'] == search_area.upper())]
            user_latitude = matched_result['latitude'].item()
            user_longitude = matched_result['longitude'].item()
            print("=====================================================================================")
            print(f"Database entry for {matched_result['name'].item()} used for latitude ({user_latitude}) & longitude({user_longitude})")
            print("=====================================================================================")

            search = True

        elif search_area.lower() == 'manual':
            user_latitude = input("Enter Latitude\n")
            user_longitude = input("Enter longitude\n")
            search = True
        else:
            print("Country not found in Database, check spelling or type 'manual' to enter location manually\n")

    question = input("Do you want email alerts when the ISS is visible from your location?\n")

    if question.lower() == "y" or question.lower() ==  "yes":
        print("Email Alert / Future use case / Testing")

        user_email = input("\nWhat is your email address?\nThis Application is not currently secured, please do not use a work / primary email address\n")
        new_entry = {'email': user_email, 'latitude': user_latitude, 'longitude':user_longitude}

        try:
            with open("users.json", "r") as user_file:
                # Reading old data
                data = pd.read_json("users.json")

        except FileNotFoundError:
            with open("users.json", "w") as user_file:
                default = {'email': ['david@creative-wavelength.com', 'porfirio.cd52000a@mailerq.net', 'rashad.0c3e9859@inboxeen.com', 'darrick.0694ea0c@creative-wavelength.com'],
                        'latitude': [40.463667, 53.41291, 37.09024, 35.86166],
                        'longitude': [-3.74922, -8.24389, -95.712891, 104.195397]}
                default_df = pd.DataFrame(default, columns=['email', 'latitude', 'longitude'])
                updated_df = default_df.append(new_entry, ignore_index=True)
                updated_df.to_json(r'users.json', indent=4)
        else:
            df_stored = pd.DataFrame(data)
            updated_df = df_stored.append(new_entry, ignore_index=True)
            updated_df.to_json(r'users.json',indent=4)

        finally:
            print("\nUser Lat, Long & Email Returned")
            return (user_latitude,user_longitude,user_email)

    else:
        print("user lat & user long returned only")
        return (user_latitude,user_longitude)

user = user_input()
user_la = user[0]
user_lo = user[1]

def get_iss_location():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    latitude = float(data["iss_position"]["latitude"])
    longitude = float(data["iss_position"]["longitude"])
    return (latitude,longitude)

iss_location = get_iss_location()

def find_user():
    ISS = get_iss_location()
    try:
        json_stored = pd.read_json('users.json')
        df_stored = pd.DataFrame(json_stored)
        print(f" ISS location = {ISS}")

    except FileNotFoundError:
        print("File not Found")
        return False
    else:
        print("df_stored")
        print(df_stored)
        condition = df_stored['latitude'].between(-45,45)
        print(condition)

find_user()


latitudes = df['latitude'].to_list()
longitudes = df['longitude'].to_list()

nearby_countries = df[df['longitude'].between(iss_location[1] -45, iss_location[1] + 45) & df['latitude'].between(iss_location[0] -45, iss_location[0] + 45)]

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
    print("\n=====================================================================================")
    print(f"COUNTRIES THE ISS IS CURRENTLY PASSING OVER - {len(countries_nearby_list)}")
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
print("Times are in UTC")
print("=====================================================================================")

#Suntimes API
# All this code does, is return True if it's night time where the user currently is.
# Most of this code is for printing local information accessed from API / learning / testing features / keeping it there for potential future expansion.
# Essentially though, all it does is return True at night.

def local_is_night(user_la, user_lo):
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
            print(f"{time_until_sunset} Minutes left until sunset in Submitted Location")
        else:
            print(f"Calculate time until sunset in Submitted location - {str(time_until_sunset)[:-2] + ':' + list(str(time_until_sunset))[1] + list(str(time_until_sunset))[2]}")
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

    #IS DARK?
    if sunset < current_time:
        return True
    else:
        return False

if len(user) == 3:
    # Can pass email here if needed
    user_email = user[2]
    local_is_night(user_la,user_lo)
else:
    local_is_night(user_la,user_lo)

def is_iss_overhead():
    print("Checking")

while program == True:
    if is_iss_overhead() and local_is_night():
        while True:
            if is_iss_overhead() and local_is_night():
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=CLIENT_EMAIL, password=CLIENT_PASSWORD)
                    connection.sendmail(
                    from_addr=CLIENT_EMAIL,
                    to_addrs=f"{email}",
                    msg=f"Subject:Look Up 👆, The ISS is above your head! \n\nNo message tag yet")
    else:
        time.sleep(60)

# Bug Catcher used earlier for finding formatting issue in data
# for l in latitudes:
# if isinstance(l,str):
# print("String Located")