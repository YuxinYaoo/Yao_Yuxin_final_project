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


# Define the header function to display the first few rows of the dataset
def header(df, dataset_name):
    st.header(f'Data Header for {dataset_name}:')
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
st.write('This Streamlit app provides insights into Los Angeles County population, median income, coffee shops, stadiums, Trader Joe’s, and house prices.')

# Add a sidebar for navigation and dataset selection
st.sidebar.title('Navigation')
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
selected_dataset_name = st.sidebar.selectbox('Select a dataset to explore:', list(datasets.keys()))
selected_dataset_path = datasets[selected_dataset_name]
df = pd.read_csv(selected_dataset_path)
finaldf = pd.read_csv('final_data.csv')

# Navigation using radio buttons in sidebar
navigation = st.sidebar.radio('Go to:', ['Home', 'Final Data Statistics', 'Data Header', 'Top 10 in LA', 'Correlation Analysis', 'Map'])

# Display based on sidebar navigation
if navigation == 'Final Data Statistics':
    st.write('Los Angeles County Final Data Statistics:')
    st.write(finaldf[["population", "median_income", "median_unit_price", "num_traderjoes", "num_stadiums", "num_coffee"]].describe())
elif navigation == 'Data Header':
    header(df, selected_dataset_name)
elif navigation == 'Top 10 in LA':
    st.write(f'Top 10 in Los Angeles County for {selected_dataset_name}:')
    st.write(df.head(10))
elif navigation == 'Correlation Analysis':
    interactive_plot(finaldf)
elif navigation == 'Map':
    display_map(finaldf)
