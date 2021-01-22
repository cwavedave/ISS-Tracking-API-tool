import requests
import pandas as pd
import datetime as dt

now = dt.datetime.now()
countries_csv = pd.read_csv("countries.csv", sep='\s*,\s*', engine='python')
df = pd.DataFrame(countries_csv)
df['latitude'] = df['latitude'].astype(float)


# print(df['latitude'])

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

latitude = float(data["iss_position"]["latitude"])
longitude = float(data["iss_position"]["longitude"])

print(f"ISS locations is {(latitude,longitude)}")

print(df.iloc[1]['latitude'])

latitudes = df['latitude'].to_list()

longitudes = df['longitude'].to_list()

for l in latitudes:
    if isinstance(l,str):
        print("String Located")

latitude_match = df[df['latitude'].between(latitude -5, latitude + 5)]
print("Matching Latitudes")
print(latitude_match)

# Attempt 1 - To find closest
# index = abs(countries_df['latitude'] - (latitude).idxmin())
# print(index)

iss_position = (longitude,latitude)

# print(iss_position)

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
    print(f" Calculate {sunset - current_time}")
    print(f"Sunset time is {sunset}")

if len(str(sunrise)) == 3:
    print(f"Sunrise time is {str(sunrise)[:-2] + ':' + list(str(sunrise))[1] + list(str(sunrise))[2]}")

else:
    print(f"Sunrise time is {str(sunrise)[:-2] + ':' + list(str(sunrise))[2] + list(str(sunrise))[3]}")

print(f"Sunset time is {str(sunset)[:-2] + ':' + list(str(sunset))[2] + list(str(sunset))[3]}")

# print(sunset)