import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL of the website to scrape
url = "https://www.laalmanac.com/employment/em12c.php"

# Send an HTTP GET request to the website
response = requests.get(url)

# Parse the HTML code using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize a list to store the data
data = []

# Find all 'tr' tags
for tr in soup.find_all('tr'):
    # For each 'tr', find all 'td' tags
    td_elements = tr.find_all('td')
    
    # Extract text or data from each 'td'
    zip_code = td_elements[0].text.strip()
    place_with_link = td_elements[1]
    place_name = place_with_link.text.strip()
    median_income = td_elements[2].text.strip()

    # Append a tuple or list of the data to our data list
    data.append((zip_code, place_name, median_income))

# At this point, 'data' list contains tuples of the extracted data
print(data)

#clean median_income
#df = pd.DataFrame(data, columns=['ZIP Code', 'Place Name', 'Median Income'])
df = pd.DataFrame(data, columns=['zip_code', 'place_name', 'median_income'])
df = df.drop(columns=['place_name']) # drop the Place name column
df = df[~df['median_income'].str.contains("No 2022 estimate")] # delete the rows with No 2022 estimate
# remove the $ sign in the median_income column
df['median_income'] = df['median_income'].str.replace('$', '')
df['median_income'] = df['median_income'].str.replace(',', '')
df['median_income'] = df['median_income'].astype(int)
df
df.to_csv('la_median_income.csv', index=False)


# URL of the website to scrape
url = "https://www.laalmanac.com/population/po03z.php"

# Send an HTTP GET request to the website
response = requests.get(url)

# Parse the HTML code using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize a list to store the data
data = []

# Find all 'tr' tags
for tr in soup.find_all('tr'):
    # Find all 'td' tags within the row
    td_elements = tr.find_all('td')
    if len(td_elements) >= 3:
        # Extract text or data from each 'td'
        zip_code = td_elements[0].text.strip()
        place_name = td_elements[1].text.strip()
        population = td_elements[2].text.strip()
        
        # Append the data as a tuple to the list
        data.append((zip_code, place_name, population))

# Convert the list to a DataFrame
df = pd.DataFrame(data, columns=['zip_code', 'place_name', 'population'])
df = df.drop([0])
#change the type of zip_code, population to int
df['zip_code'] = df['zip_code'].astype(int)
df['population'] = df['population'].str.replace(',', '').astype(int)
print(df)

df.to_csv('la_population.csv', index=False)
