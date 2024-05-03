import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Point
import contextily as ctx
from pyproj import Transformer

# Read data sets
zipcodes = pd.read_csv('lazip.csv')
population = pd.read_csv('la_population.csv')
median_income = pd.read_csv('la_median_income.csv')
houseprices = pd.read_csv('ca_house_price.csv')
traderjoes = pd.read_csv('trader_joes_locations.csv')
stadiums = pd.read_csv('yelp_stadium_los_angeles.csv')
coffee = pd.read_csv('yelp_coffee_los_angeles.csv')

# head
print(zipcodes.head())
print(population.head())
print(median_income.head())
print(houseprices.head())
print(traderjoes.head())
print(stadiums.head())
print(coffee.head())

# clean the data
coffee['zip_code'] = coffee['zip_code'].str.split('-').str[0]
coffee['zip_code'] = coffee['zip_code'].astype(int)
# save the cleaned data
coffee.to_csv('yelp_coffee_los_angeles.csv', index=False)
traderjoes['zip_code'] = traderjoes['zip_code'].astype(int)
traderjoes.to_csv('trader_joes_locations.csv', index=False)

# get the median unit price of each zipcode
median_unit_price = houseprices.groupby('zip_code')['unit_price'].median().reset_index()
median_unit_price = median_unit_price.rename(columns={'unit_price': 'median_unit_price'})
print(median_unit_price.head())

# number of trader joes in each zipcode
num_traderjoes = traderjoes.groupby('zip_code').size().reset_index()
num_traderjoes = num_traderjoes.rename(columns={0: 'num_traderjoes'})
num_traderjoes

# number of stadiums in each zipcode
num_stadiums = stadiums.groupby('zip_code').size().reset_index()
num_stadiums = num_stadiums.rename(columns={0: 'num_stadiums'})
num_stadiums

# count the number of coffee shops in each zipcode
num_coffee = coffee.groupby('zip_code').size().reset_index()
num_coffee = num_coffee.rename(columns={0: 'num_coffee'})
num_coffee

# merge the data
merged1 = pd.merge(population, median_income, on='zip_code', how='left')
merged1 = merged1.fillna(0)
merged1
merge2 = pd.merge(merged1, median_unit_price, on='zip_code', how='left')
merge2
merge3 = pd.merge(merge2, num_traderjoes, on='zip_code', how='left')
merge3 = merge3.fillna(0)
merge3
merge4 = pd.merge(merge3, num_stadiums, on='zip_code', how='left')
merge4 = merge4.fillna(0)
merge4
merge5 = pd.merge(merge4, num_coffee, on='zip_code', how='left')
merge5 = merge5.fillna(0)
merge5
df = pd.merge(merge5, zipcodes, on='zip_code', how='left')
df = df.drop(columns=['country', 'country abbreviation', 'city', 'state', 'state abbreviation'])
df = df[df['population'] != 0] # delete the data with 0 population
df
# save the data
df.to_csv('final_data.csv', index=False)
print(df.isnull().sum()) # show if there is any missing value


