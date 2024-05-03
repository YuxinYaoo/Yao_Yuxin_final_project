import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import seaborn as sns
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Point
import contextily as ctx
from pyproj import Transformer

# Load data as global variables
finaldf = pd.read_csv('final_data.csv')
datasets = {
    'medium income': 'la_median_income.csv',
    'population': 'la_population.csv',
    'coffee shops': 'yelp_coffee_los_angeles.csv',
    'stadiums': 'yelp_stadium_los_angeles.csv',
    'trader joes': 'trader_joes_locations.csv',
    'house price': 'ca_house_price.csv',
    'zip code': 'lazip.csv',
    'final data': 'final_data.csv'
}

def header():
    st.header('Data Header by ZIP code:')
    # Select a dataset to explore
    selected_dataset_name = st.selectbox('Select a dataset to explore:', list(datasets.keys()), key='header_select_dataset')
    selected_dataset_path = datasets[selected_dataset_name]
    df = pd.read_csv(selected_dataset_path)

    zip_code = st.text_input("Enter ZIP code to filter:", key='header_zip_code')
    if zip_code:
        try:
            zip_code = int(zip_code)
            df_filtered = df[df['zip_code'] == zip_code]
            if not df_filtered.empty:
                st.write(df_filtered)
            else:
                st.write("No data found for this ZIP code.")
        except ValueError:
            st.error("Please enter a valid ZIP code.")
    else:
        st.write(df.head())


def interactive_plot(finaldf):
    # List of specific columns that are necessary for the scatter plot 
    allowed_columns = ['population', 'median_income', 'median_unit_price', 'num_traderjoes', 'num_stadiums', 'num_coffee']


    # Filter dataframe to include only the allowed columns for safety
    plot_columns = [col for col in allowed_columns if col in finaldf.columns]

    # Check if there are enough columns to plot
    if len(plot_columns) < 2:
        st.error("Not enough data available to create a plot.")
        return

    # Selectboxes for choosing columns for the x and y axes
    x_axis_val = st.selectbox('Select X-axis variable:', plot_columns)
    y_axis_val = st.selectbox('Select Y-axis variable:', plot_columns)


    # Handling potential NaN values or infinite values which can disrupt correlation computation
    if finaldf[x_axis_val].isnull().any() or finaldf[y_axis_val].isnull().any():
        st.warning('Warning: Data contains NaN values. Filling NaN with the median value.')
        finaldf[x_axis_val].fillna(finaldf[x_axis_val].median(), inplace=True)
        finaldf[y_axis_val].fillna(finaldf[y_axis_val].median(), inplace=True)

    # Create a scatter plot using Plotly Express
    plot = px.scatter(finaldf, x=x_axis_val, y=y_axis_val,
                      title=f"{y_axis_val} vs {x_axis_val}",
                      labels={x_axis_val: x_axis_val, y_axis_val: y_axis_val})  # Labels ensure axis titles match selected columns

    # Display the plot in Streamlit
    st.plotly_chart(plot)

    # Calculate the correlation coefficient and R squared value
    correlation_coef = np.corrcoef(finaldf[x_axis_val], finaldf[y_axis_val])[0, 1]
    r_squared = correlation_coef ** 2
    st.write(f'Correlation coefficient: {correlation_coef:.2f}')
    st.write(f'R squared value: {r_squared:.2f}')

    # Provide interpretation based on R squared value
    if r_squared < 0.3:
        st.write("There is a weak relationship.")
    elif r_squared < 0.7:
        st.write("There is a moderate relationship.")
    else:
        st.write("There is a strong relationship.")

def display_map(finaldf):
    # Required columns check
    required_columns = ['longitude', 'latitude', 'population', 'median_income', 'median_unit_price', 'num_traderjoes', 'num_stadiums', 'num_coffee']
    if not all(col in finaldf.columns for col in required_columns):
        st.error("Dataframe is missing one or more required columns.")
        return

    # Filtering out the outliers
    mapdf = finaldf[(finaldf['longitude'] < -117) & (finaldf['latitude'] < 34.5)]

    

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(mapdf, geometry=gpd.points_from_xy(mapdf.longitude, mapdf.latitude))
    gdf.set_crs("epsg:4326", inplace=True)  # Set to WGS84
    gdf = gdf.to_crs(epsg=3857)  # Convert to Web Mercator for mapping

    # Create a plot
    fig, ax = plt.subplots(figsize=(10, 10))
    attribute = st.selectbox('Select an attribute to display:', ['population', 'median_income', 'median_unit_price', 'num_traderjoes', 'num_stadiums', 'num_coffee'])
    gdf.plot(ax=ax, column=attribute, cmap='coolwarm', legend=True,
             legend_kwds={'label': f"{attribute} by Zip Code",
                          'orientation': "horizontal"})

    # Adding a basemap
    ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.CartoDB.Positron)
    ax.set_axis_off()

    # Show the plot in Streamlit
    st.pyplot(fig)



# Main title and introduction
st.title('Los Angeles County Information')   
st.write('Yuxin Yao usc id: 9109746606')
st.write('This Streamlit app provides insights into Los Angeles County population, median income, coffee shops, stadiums, Trader Joe’s, and house prices.')

# Add a sidebar for navigation and dataset selection
st.sidebar.title('Navigation')


# Navigation using radio buttons in sidebar
navigation = st.sidebar.radio('Go to:', ['Home', 'Final Data Statistics', 'Data Header', 'Correlation Analysis', 'Map'])

# Display based on sidebar navigation
if navigation == 'Home':
    st.markdown("""
    ## An explanation of how to use your webapp:
    This web application allows users to explore datasets related to Los Angeles County. Users can select from the sidebar to navigate to different pages, including the homepage, statistical analysis of the final data, data header, correlation analysis, and maps. On the data header page, I have set interactive options for selecting datasets and entering zip codes. By default, the first five rows of the dataset are displayed when no zip code is entered. If a zip code is entered, the data corresponding to that zip code in the dataset will be shown. On the correlation analysis page, users can display scatter plots, as well as correlation coefficients and R-squared values by choosing variables for the x and y axes. The map visualization page also has interactive options for selecting datasets, which can be used to display the distribution of quantity or size of the selected dataset on a map of Los Angeles County.

    ## Any major “gotchas”:
    There is not something that cannot work or work slowly. However, the Trader Joe's dataset obtained through web scraping is small and insufficient for in-depth data analysis.

    ## What did you set out to study?
    I have gathered data on the population of Los Angeles County, median household income, and the current median price per square inch of houses on sale, as well as information on coffee shops, stadiums, and Trader Joe's stores. I aim to study their interrelations, particularly their impact on housing prices. Initially, for Milestone 1, I only planned to collect data on Trader Joe's, stadiums, and the current median prices per square meter of houses, but I found this to be insufficient for comprehensive analysis. I realized that median household income is likely more influential on housing prices, while population more likely affects the distribution of shops and stadiums. Therefore, I have also scraped data on population and household income for each ZIP code from the Los Angeles Almanac website. Additionally, as a coffee enthusiast, I used the Yelp API to gather data on coffee shops in Los Angeles County.

    ## What did you discover?
    After researching, I discovered a relatively strong correlation between median household income and median price per square inch of houses on sale, with a correlation coefficient of 0.61, which aligns with my hypothesis. Besides, the median price per square inch of houses on sale did not show significant relationships with other variables. Additionally, the relationship between population and amenities such as coffee shops, supermarkets, and stadiums was not as evident as expected. Typically, in more economically developed areas with larger populations, these conveniences and entertainment facilities should be more prevalent. I suspect that the lack of significant relationships may be due to the small number of supermarkets, stadiums, and coffee shops per ZIP code.

    ## What difficulties did you have in completing the project?
    My biggest technical challenge was collecting data from the Yelp API because searching directly for Los Angeles County in the Yelp API parameters did not yield complete data. Therefore, I chose to search by ZIP code. I wrote a for loop to iterate through all the ZIP codes in Los Angeles County, which ultimately provided the results I wanted. As mentioned, the greatest difficulty in my research was that the datasets I found were too sparse when broken down by individual ZIP codes, which might lead to less accurate research results.

    ## What skills did you wish you had while you were doing the project?
    I want to do further text analysis, so I hope I can strengthen my natural language processing skills and apply them to my project next.

    ## What would you do “next” to expand or augment the project?
    I can further analyze the coffee shop and stadium dataset, for example, I can scrape the reviews of coffee shops and stadiums on Yelp and further do text analysis to get the high-frequency word cloud to present to Streamlit. Also, we can do sentiment analysis, we can get the information that the merchant may not provide by doing the text analysis of the reviews, such as whether it is convenient to park or not, and the service attitude. This can help us make better decisions. To summarize, I hope I can strengthen my natural language processing skills and apply them to my projects in the next step.
    """)
    
elif navigation == 'Final Data Statistics':
    st.write('Los Angeles County Final Data Statistics:')
    st.write(finaldf[["population", "median_income", "median_unit_price", "num_traderjoes", "num_stadiums", "num_coffee"]].describe())
elif navigation == 'Data Header':
    header()
elif navigation == 'Correlation Analysis':
    interactive_plot(finaldf)
elif navigation == 'Map':
    display_map(finaldf)
