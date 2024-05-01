import requests
import json
import pandas as pd


# import the zip code data(los angeles county)
df_la = pd.read_csv('/Users/yaoyuxin/Desktop/DSCI510/Yao_Yuxin_proj3/la_population.csv')
la_zip = df_la['zip_code']

# Define API Key and header
MY_API_KEY = 'ovaXJ_ozZ-jL6hJdtmTr4ekwtoMKEuR-NWLqj-hyfjrEpq3iEgzbK2fS0f9bQWFI4T_2mER7ub6wUvRR5YAigBJt0ihmOwvn_E4BaS1k1XO1X019gNvZQxUJ7M0uZnYx'
BUSINESS_PATH = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % MY_API_KEY}

# Function to make a request to the Yelp API for the given zip code
def get_businesses(zip_code):
    PARAMETERS = {
        'term': 'coffee',
        'location': zip_code,
        'categories': 'Coffee & Tea'
    }
    response = requests.get(url=BUSINESS_PATH, params=PARAMETERS, headers=HEADERS)
    return response.json()

# Iterate over the first los angeles zip codes and collect the results
all_businesses = []
for zip_code in la_zip:
    business_data = get_businesses(zip_code)
    all_businesses.extend(business_data.get('businesses', []))

# Convert the collected results to a DataFrame
df_businesses_la = pd.json_normalize(all_businesses)
df_businesses_la = df_businesses_la.drop_duplicates(subset=['id']) # REMOVE THE DUPLICATES
#clean coffee
df_businesses_la = df_businesses_la.drop(['location.address1', 'location.city', 'location.address2','location.address3', 'location.country',
                       'location.state', 'alias','attributes.open24_hours','attributes.waitlist_reservation','price','categories',
                       'rating','phone','is_closed','url','display_phone','attributes.menu_url', 'coordinates.latitude','distance',
                       'coordinates.longitude','review_count','image_url','transactions'], axis=1) # rename the columns
df_businesses_la = df_businesses_la.rename(columns={'id': 'coffee_id', 'name': 'coffee_name', 'location.zip_code': 'zip_code', 'location.display_address': 'coffee_address'})
print(df_businesses_la.head())

df_businesses_la.to_csv('/Users/yaoyuxin/Desktop/DSCI510/Yao_Yuxin_proj3/yelp_coffee_los_angeles.csv', index=False)
