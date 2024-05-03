import pandas as pd

# import whole dataset
whole_df = pd.read_csv('realtor-data.zip.csv')
print(whole_df.head())

# get california df
df = whole_df[whole_df['state'] == 'California']
print(df.head())

# count missing values
na_counts = df.isna().sum()
na_counts
(na_counts / len(df)) * 100

# handle missing values
df['bed'].fillna(df['bed'].median(), inplace=True)
df['bath'].fillna(df['bath'].median(),inplace=True)
df['house_size'].fillna(df['house_size'].mean(),inplace=True)
df['acre_lot'].fillna(df['house_size'].mean(),inplace=True)
df.dropna(inplace=True)
df.isna().sum()
df.shape

# correct data types
df['bath'] = df['bath'].astype(int)
df['bed'] = df['bed'].astype(int)
df['house_size'] = df['house_size'].astype(int)
df['acre_lot'] = df['acre_lot'].astype(int)
df['zip_code'] = df['zip_code'].astype(int)
df['price'] = df['price'].astype(int)
df['street'] = df['street'].astype(int)
df.dtypes

# add id column
df['id'] = range(1, len(df) + 1)
headers = ['id', 'street', 'city', 'zip_code', 'price', 'bed', 'bath', 'house_size', 'acre_lot']
df = df[headers]
df = df.drop(columns=['city'])
df = df.rename(columns={'id': 'house_id', 'street': 'house_street'})
print(df.head())

# save cleaned data to csv
df.to_csv('ca_house_price.csv', index=False)


