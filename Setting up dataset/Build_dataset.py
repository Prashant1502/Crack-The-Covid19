
###### Version 1 #####
###### Importing File and making dataset#####

import pandas as pd
df_icmrlab = pd.read_csv("/kaggle/input/covid19-in-india/ICMRTestingLabs.csv")
from geopy.geocoders import get_geocoder_for_service
get_geocoder_for_service("nominatim")
import geopy.geocoders
from geopy.geocoders import Nominatim
geopy.geocoders.options.default_user_agent = 'my_app/1'
geopy.geocoders.options.default_timeout = 7 
geolocator = Nominatim()
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_app/1")
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
temp = df_icmrlab['city'].apply(geocode)
point = temp.apply(lambda loc: tuple(loc.point) if loc else None)
df_icmrlab['location'] = point
df_icmrlab.to_csv('ICMRLabDetails.csv',index=False)

##### Version 2 #####
##### Inserting Location Column and inserting data in location column #####
temp = df_icmrlab['pincode'].apply(geocode)
point = temp.apply(lambda loc: tuple(loc.point) if loc else None)
df_icmrlab['location'] = point
df_icmrlab.to_csv('ICMRLabDetails.csv',index=False)
df_icmrlab.head(10)
df_icmrlab[df_icmrlab.isna().any(axis=1)]

##### Version 3 #####
##### Removing NaN values from Location column #####
err_point = ["(30.8986, 76.9659,0.0)" , "(23.2131, 81.2026, 0.0)", "(15.8266, 76.2752, 0.0)" , "(22.304, 84.4204, 0.0)","(26.741, 78.7252, 0.0)" , "(30.0669, 78.2631, 0.0)"]
df_icmrlab['location'][df_icmrlab.isna().any(axis=1)] = err_point
df_icmrlab.to_csv("ICMRLabDetails.csv")

##### Version 4 #####
##### Taking Input and Testing #####

query = input("Enter your pincode of your city: ")
import pgeocode
nomi = pgeocode.Nominatim('in')
df_query = nomi.query_postal_code(query)
lat = df_query.latitude
lon = df_query.longitude
query_point = (lat,lon,0.0)
import geopy.distance
index = 0
count = 0
min_dis = float("inf")
for itr in df_icmrlab['location']:
    res = itr[1:-1]
    res = tuple(map(float, res.split(',')))
    dis = geopy.distance.geodesic(query_point, res).km
    if dis<min_dis:
        min_dis = dis
        index = count
    count+=1
min_dis
near_lab = df_icmrlab.loc[index,'address']
print(near_lab)
