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
zipcodes = pd.read_csv('/Users/yaoyuxin/Desktop/DSCI510/Yao_Yuxin_proj3/csv/lazip.csv')
population = pd.read_csv('/Users/yaoyuxin/Desktop/DSCI510/Yao_Yuxin_proj3/csv/la_population.csv')
median_income = pd.read_csv('/Users/yaoyuxin/Desktop/DSCI510/Yao_Yuxin_proj3/csv/la_median_income.csv')
houseprices = pd.read_csv('/Users/yaoyuxin/Desktop/DSCI510/Yao_Yuxin_proj3/csv/ca_house_price.csv')
traderjoes = pd.read_csv('/Users/yaoyuxin/Desktop/DSCI510/Yao_Yuxin_proj3/csv/trader_joes_locations.csv')
stadiums = pd.read_csv('/Users/yaoyuxin/Desktop/DSCI510/Yao_Yuxin_proj3/csv/yelp_stadium_los_angeles.csv')
coffee = pd.read_csv('/Users/yaoyuxin/Desktop/DSCI510/Yao_Yuxin_proj3/csv/yelp_coffee_los_angeles.csv')

# head
print(zipcodes.head())
print(population.head())
print(median_income.head())
print(houseprices.head())
print(traderjoes.head())
print(stadiums.head())
print(coffee.head())


# Add a new column for unit price
houseprices['unit_price'] = houseprices['price'] / houseprices['house_size']
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
num_coffee['zip_code'] = num_coffee['zip_code'].str.split('-').str[0]
num_coffee['zip_code'] = num_coffee['zip_code'].astype(int)
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
df
print(df.isnull().sum()) # show if there is any missing value



# Top 10 Zip Codes with the Most Coffee Shops in Los Angeles
top10_coffee = df.nlargest(10, 'num_coffee')
# only show the zip_code, place name and num_coffee columns
top10_coffee = top10_coffee[['zip_code', 'place_name', 'num_coffee']]
top10_coffee

fig, ax = plt.subplots()
ax.bar(top10_coffee['zip_code'].astype(str), top10_coffee['num_coffee'])
ax.set_xlabel('Zip Code')
ax.set_ylabel('Number of Coffee Shops')
ax.set_title('Top 10 Zip Codes with the Most Coffee Shops in Los Angeles')
ax.set_xticklabels(top10_coffee['zip_code'].astype(str), rotation=45)  
plt.show()

# Top 10 Zip Codes with the Most stadium in Los Angeles
top10_stadium = df.nlargest(10, 'num_stadiums')
# only show the zip_code, place name and num_stadiums columns
top10_stadium = top10_stadium[['zip_code', 'place_name', 'num_stadiums']]
top10_stadium

fig, ax = plt.subplots()
ax.bar(top10_stadium['zip_code'].astype(str), top10_stadium['num_stadiums'])
ax.set_xlabel('Zip Code')
ax.set_ylabel('Number of Stadiums')
ax.set_title('Top 10 Zip Codes with the Most Stadiums in Los Angeles')
ax.set_xticklabels(top10_stadium['zip_code'].astype(str), rotation=45)
plt.show()

# Top 10 Zip Codes with the Most Trader Joe's in Los Angeles
top10_traderjoes = df.nlargest(10, 'num_traderjoes')
# only show the zip_code, place name and num_traderjoes columns
top10_traderjoes = top10_traderjoes[['zip_code', 'place_name', 'num_traderjoes']]
top10_traderjoes

fig, ax = plt.subplots()
ax.bar(top10_traderjoes['zip_code'].astype(str), top10_traderjoes['num_traderjoes'])
ax.set_xlabel('Zip Code')
ax.set_ylabel('Number of Trader Joe\'s')
ax.set_title('Top 10 Zip Codes with the Most Trader Joe\'s in Los Angeles')
ax.set_xticklabels(top10_traderjoes['zip_code'].astype(str), rotation=45)
plt.show()

# Top 10 Zip Codes with the Most Population in Los Angeles
top10_population = df.nlargest(10, 'population')
# only show the zip_code, place name and population columns
top10_population = top10_population[['zip_code', 'place_name', 'population']]
top10_population

fig, ax = plt.subplots()
ax.bar(top10_population['zip_code'].astype(str), top10_population['population'])
ax.set_xlabel('Zip Code')
ax.set_ylabel('Population')
ax.set_title('Top 10 Zip Codes with the Most Population in Los Angeles')
ax.set_xticklabels(top10_population['zip_code'].astype(str), rotation=45)
plt.show()

# Top 10 Zip Codes with the Highest Median Income in Los Angeles
top10_median_income = df.nlargest(10, 'median_income')
# only show the zip_code, place name and median_income columns
top10_median_income = top10_median_income[['zip_code', 'place_name', 'median_income']]
top10_median_income

fig, ax = plt.subplots()
ax.bar(top10_median_income['zip_code'].astype(str), top10_median_income['median_income'])
ax.set_xlabel('Zip Code')
ax.set_ylabel('Median Income')
ax.set_title('Top 10 Zip Codes with the Highest Median Income in Los Angeles')
ax.set_xticklabels(top10_median_income['zip_code'].astype(str), rotation=45)
plt.show()

# Top 10 Zip Codes with the Highest Median Unit Price in Los Angeles
top10_median_unit_price = df.nlargest(10, 'median_unit_price')
# only show the zip_code, place name and median_unit_price columns
top10_median_unit_price = top10_median_unit_price[['zip_code', 'place_name', 'median_unit_price']]
top10_median_unit_price

fig, ax = plt.subplots()
ax.bar(top10_median_unit_price['zip_code'].astype(str), top10_median_unit_price['median_unit_price'])
ax.set_xlabel('Zip Code')
ax.set_ylabel('Median Unit Price')
ax.set_title('Top 10 Zip Codes with the Highest Median Unit Price in Los Angeles')
ax.set_xticklabels(top10_median_unit_price['zip_code'].astype(str), rotation=45)
plt.show()

# figure out the relationship between median income and median unit price
fig, ax = plt.subplots()

ax.scatter(df['median_income'], df['median_unit_price'], s=10, color='blue', alpha=0.5)
ax.set_xlabel('Median Income')
ax.set_ylabel('Unit House Price')
ax.set_title('Median Income vs. Unit House Price by Zip Code')

m, b = np.polyfit(df['median_income'], df['median_unit_price'], 1)
ax.plot(df['median_income'], m * df['median_income'] + b, color='red')

fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax.xaxis.set_major_formatter(tick)

ax.grid(True)
plt.show()

# Get the R squared value
cor1 = df['median_income'].corr(df['median_unit_price'])
r_squared1 = cor1 ** 2
r_squared1

# figure out the relationship between median unit price and number of coffee shops
fig, ax = plt.subplots()

ax.scatter(df['median_unit_price'], df['num_coffee'], s=10, color='blue', alpha=0.5)
ax.set_xlabel('Unit House Price')
ax.set_ylabel('Number of coffee shops')
ax.set_title('Unit House Price vs. number of coffee shops by Zip Code')

m, b = np.polyfit(df['median_unit_price'], df['num_coffee'], 1)
ax.plot(df['median_unit_price'], m * df['median_unit_price'] + b, color='red')

fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax.xaxis.set_major_formatter(tick)

ax.grid(True)
plt.show()

# Get the R squared value
cor2 = df['median_unit_price'].corr(df['num_coffee'])
r_squared2 = cor2 ** 2
r_squared2

# figure out the relationship between median unit price and number of stadiums
fig, ax = plt.subplots()

ax.scatter(df['median_unit_price'], df['num_stadiums'], s=10, color='blue', alpha=0.5)
ax.set_xlabel('Unit House Price')
ax.set_ylabel('Number of Stadiums')
ax.set_title('Unit House Price vs. number of stadiums by Zip Code')

m, b = np.polyfit(df['median_unit_price'], df['num_stadiums'], 1)
ax.plot(df['median_unit_price'], m * df['median_unit_price'] + b, color='red')

fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax.xaxis.set_major_formatter(tick)

ax.grid(True)
plt.show()

# Get the R squared value
cor3 = df['median_unit_price'].corr(df['num_stadiums'])
r_squared3 = cor3 ** 2
r_squared3

# figure out the relationship between median unit price and number of trader joes
fig, ax = plt.subplots()

ax.scatter(df['median_unit_price'], df['num_traderjoes'], s=10, color='blue', alpha=0.5)
ax.set_xlabel('Unit House Price')
ax.set_ylabel('Number of traderjoes')
ax.set_title('Unit House Price vs. number of traderjoes by Zip Code')

m, b = np.polyfit(df['median_unit_price'], df['num_traderjoes'], 1)
ax.plot(df['median_unit_price'], m * df['median_unit_price'] + b, color='red')

fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax.xaxis.set_major_formatter(tick)

ax.grid(True)
plt.show()

# Get the R squared value
cor4 = df['median_unit_price'].corr(df['num_traderjoes'])
r_squared4 = cor4 ** 2
r_squared4

fig, ax = plt.subplots()

# Use population density to determine the size of the points and economic level to determine the color
scatter = ax.scatter(df['median_unit_price'], df['num_coffee'], 
                     c=df['median_income'],   # Color based on economic level
                     s=df['population'],  # Size based on population density
                     cmap='viridis', alpha=0.6)  # Color map and transparency

# Add a color bar
plt.colorbar(scatter, ax=ax, label='Median Income')

# Set axis labels and chart title
ax.set_xlabel('Median House Price')
ax.set_ylabel('Number of Coffee Shops')
ax.set_title('House Price vs. Number of Coffee Shops: Effects of Population Density and Economic Level')

plt.show() # Display the plot

# Plot the geographical distribution
df = df[df['population'] != 0] # delete the data with 0 population
df = df.sort_values(by='population', ascending=False) # order by population
df = df[df['longitude'] < -117] # remove the outlier of longitude and latitude
df = df[df['latitude'] < 34.5]

transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True) # Create a transformer
lon_min, lon_max = df['longitude'].min(), df['longitude'].max()
lat_min, lat_max = df['latitude'].min(), df['latitude'].max()
xmin, ymin = transformer.transform(lon_min, lat_min) # Transform the boundaries to Web Mercator
xmax, ymax = transformer.transform(lon_max, lat_max)


gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df.longitude, df.latitude)
)
gdf = gdf.set_crs("epsg:4326")  # Confirm it's in WGS84
gdf = gdf.to_crs(epsg=3857)     # Convert to Web Mercator

# figure number of coffee shops in each zipcode
fig, ax = plt.subplots(figsize=(10, 10)) # Plotting
gdf.plot(ax=ax, column='num_coffee', cmap='coolwarm', legend=True,
         legend_kwds={'label': "Number of Coffee Shops by Zip Code",
                      'orientation': "horizontal"})

ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron) # Add basemap
ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
ax.set_axis_off()
plt.show()

# figure out the median unit price in each zipcode
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, column='median_unit_price', cmap='coolwarm', legend=True,
         legend_kwds={'label': "Number of median unit price by Zip Code",
                      'orientation': "horizontal"})


ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron) # Add basemap
ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
ax.set_axis_off()
plt.show()

