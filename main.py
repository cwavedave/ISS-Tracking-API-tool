import requests
import pandas as pd
import datetime as dt

now = dt.datetime.now()

print(now)

countries_csv = pd.read_csv("countries.csv")
countries_df = pd.DataFrame(countries_csv)

#Strips white Space from all columns: https://stackoverflow.com/questions/33788913/pythonic-efficient-way-to-strip-whitespace-from-every-pandas-data-frame-cell-tha
df = countries_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
print(df)

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

latitude = float(data["iss_position"]["latitude"])
longitude = float(data["iss_position"]["longitude"])

# #TODO Figure this out later - Why are other columns throwing up key errors?
# index = abs(df['latitude'] - (latitude).idxmin())
# print(index)
#
iss_position = (longitude,latitude)

print(iss_position)

vic_lo = 2.25486
vic_la = 41.93012

sun_response = requests.get(url=f'https://api.sunrise-sunset.org/json?lat={vic_la}&lng={vic_lo}&formatted=0')
data = sun_response.json()

print(data)

current_time = int(str(now).split(' ')[1].split('.')[0][:-3].replace(":",""))
print(current_time)

sunrise = int(data["results"]["sunrise"].split("T")[1].split("+")[0][:-3].replace(":",""))
sunset = int(data["results"]["sunset"].split("T")[1].split("+")[0][:-3].replace(":",""))

if sunset < current_time:
    print(f"Current time is {sunrise}")
    print(f" Calculate {sunset - current_time}")
    print(f"Sunset time is {sunset}")

if len(str(sunrise)) == 3:
    print(f"Sunrise time is {str(sunrise)[:-2] + ':' + list(str(sunrise))[1] + list(str(sunrise))[2]}")

else:
    print(f"Sunrise time is {str(sunrise)[:-2] + ':' + list(str(sunrise))[2] + list(str(sunrise))[3]}")

print(f"Sunset time is {str(sunset)[:-2] + ':' + list(str(sunset))[2] + list(str(sunset))[3]}")

print(sunset)