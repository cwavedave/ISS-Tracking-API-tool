import requests
import pandas as pd

countries_csv = pd.read_csv("countries.csv")
countries_df = pd.DataFrame(countries_csv)

#Strips white Space from all columns: https://stackoverflow.com/questions/33788913/pythonic-efficient-way-to-strip-whitespace-from-every-pandas-data-frame-cell-tha
df = countries_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
print(df)

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

latitude = data ["iss_position"]["latitude"]
longitude = data["iss_position"]["longitude"]

#TODO Figure this out later - Why are other columns throwing up key errors?
index = abs(df['latitude'] - (latitude).idxmin())
print(index)

iss_position = (longitude,latitude)

print(iss_position)