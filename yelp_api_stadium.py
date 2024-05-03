import requests
import json
import pandas as pd


# import the zip code data(los angeles county)
df_la = pd.read_csv('la_population.csv')
la_zip = df_la['zip_code']

# Define API Key and header
MY_API_KEY = 's2a3B2jNXBYxFIUcbrieypxLUau7UptHZfAUP8CDNbq9dWleFZdmgzmeIadYTrvTcsKen4Rp4UrjiybLjYJVlzNjSCNQBBtAD731yq7-RzjSW5flTSMmAxE2V04cZnYx'
BUSINESS_PATH = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % MY_API_KEY}

# Function to make a request to the Yelp API for the given zip code
def get_businesses(zip_code):
    PARAMETERS = {
        'term': 'Stadiums',
        'location': zip_code,
        'categories': 'Stadiums & Arenas'
    }
    response = requests.get(url=BUSINESS_PATH, params=PARAMETERS, headers=HEADERS)
    return response.json()

# Iterate over the first Los Angeles zip codes and collect the results
all_businesses = []
for zip_code in la_zip:
    business_data = get_businesses(zip_code)
    all_businesses.extend(business_data.get('businesses', []))

# Convert the collected results to a DataFrame
df_businesses_la = pd.json_normalize(all_businesses)
df_businesses_la = df_businesses_la.drop_duplicates(subset=['id']) # REMOVE THE DUPLICATES
df_businesses_la = df_businesses_la.drop(['attributes.business_temp_closed', 'location.address1', 'location.city', 'location.address2','location.address3', 'location.country', 'location.state', 'alias','attributes.open24_hours','attributes.waitlist_reservation','price','categories','rating','phone','is_closed','url','display_phone','attributes.menu_url','coordinates.latitude','distance','coordinates.longitude','review_count','image_url','transactions'], axis=1)
df_businesses_la = df_businesses_la.rename(columns={'id': 'stadium_id', 'name': 'stadium_name', 'location.zip_code': 'zip_code', 'location.display_address': 'stadium_address'})
print(df_businesses_la.head())

df_businesses_la.to_csv('yelp_stadium_los_angeles.csv', index=False)
