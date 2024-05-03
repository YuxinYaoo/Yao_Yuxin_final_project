import requests
import pandas as pd
import random

def select_user():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Mobile Safari/537.36"
    ]
    return random.choice(user_agents)

# Get a list of California zip codes
def get_zipcode(api_key="NWTEGROTEO1TMFKX6DDY"):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'User-Agent': select_user()
    }

    service_url = 'https://api.zip-codes.com/ZipCodesAPI.svc/1.0/GetAllZipCodes?state=CA&country=US&key=' + api_key
    response = requests.get(service_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['ZipCode'])  
        df['id'] = range(1, len(df) + 1)  
        df.rename(columns={'ZipCode': 'zipcode'}, inplace=True)  
        df.to_csv('zipcodes.csv', index=False)
        return df
    else:
        return f"Failed to retrieve data: {response.status_code}"  

data_zip = get_zipcode()
print(data_zip)


# get more information of california zip codes
def fetch_zip_code_data(zip_code):
    url = f"http://api.zippopotam.us/us/{zip_code}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Collect data for each zip code
california_zip_data = []
for zip_code in data_zip['zipcode']:
    data = fetch_zip_code_data(zip_code)
    if data:
        california_zip_data.append(data)

# Display the collected data
for data in california_zip_data:
    print(data)


# Save the data to a dataframe and a CSV file
df = pd.DataFrame(california_zip_data)
df_places = pd.json_normalize(df['places'].explode()).reset_index(drop=True)
df = df.drop('places', axis=1).join(df_places)
# clean zipcodes
df = df.rename(columns={'post code': 'zip_code', 'place name': 'city'})
df = df.drop(columns=['country', 'country abbreviation', 'city', 'state', 'state abbreviation']) 
print(df.head())

df.to_csv('cazip.csv', index=False)



