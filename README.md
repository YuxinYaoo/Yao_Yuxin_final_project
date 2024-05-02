# Yao_Yuxin_final_project
# Analysis of Housing Prices, Median Income, Population and Local Amenities in Los Angeles County

## Project Overview
This project aims to explore the interrelations between local amenities such as Trader Joe's stores, coffee shops, stadiums, and housing prices across various zip codes in California. By analyzing data from multiple sources, we hope to determine how factors like median household income and population density impact housing markets.

## Data Sources
1. **Trader Joe's Locations**  
   - **Source**: [Trader Joe's Store Locations](https://locations.traderjoes.com/ca/)  
   - **Description**: List of all Trader Joe's store locations in California, including addresses and contact information.

2. **Yelp Fusion API**  
   - **Documentation**: [Yelp Developer Docs](https://docs.developer.yelp.com/docs/fusion-intro)  
   - **Description**: Data on local businesses, including stadiums and coffee shops in California, with details such as user ratings and reviews.

3. **USA Real Estate Dataset**  
   - **Source**: [Kaggle Dataset by Ahmed Shahriar Sakib](https://www.kaggle.com/datasets/ahmedshahriarsakib/usa-real-estate-dataset/data)  
   - **Description**: Real estate listings in the US with detailed information on property prices, types, sizes, and more.

4. **Los Angeles County Income Data**  
   - **Source**: [LA Almanac - Income by Zip Code](https://www.laalmanac.com/employment/em12c.php)  
   - **Description**: 2022 median household income data by zip code for Los Angeles County.

5. **Los Angeles County Population Data**  
   - **Source**: [LA Almanac - Population by Zip Code](https://www.laalmanac.com/population/po03z.php)  
   - **Description**: 2022 general population figures by zip code for Los Angeles County.

6. **Zippopotam.us API**  
   - **Source**: [Zippopotam.us](http://api.zippopotam.us/)  
   - **Description**: API provides details on zip codes, including place names, longitude, latitude, and more.

## Methodology:
- **Data Collection**: Utilize APIs, web scrape, and datasets to gather comprehensive data by zip code.
- **Data Integration**: Merge datasets based on zip code to form a unified database for analysis.
- **Data Analysis**: Employ statistical search by zip code, see each data set's information by searching the zip code, and provide a map visualization, which shows the selected attributes by ZIP code on an interactive map of Los Angeles County.

## How to Use this Repository
- final.py is the streamlit code.
- main.py is data cleaning and merging data code.

## Expected Findings
We anticipate that zip codes with higher incomes and larger populations might show a higher density of amenities and correspondingly higher housing prices. These insights could be valuable for potential home buyers, real estate agents, and urban planners.

## Authors
- **Yuxin Yao**


