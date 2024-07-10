import os
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(layout='wide', page_title='TeachingFactory Dashboard', page_icon=':factory:')

# Print the current working directory
st.write(f"Current working directory: {os.getcwd()}")

# Print the contents of the database directory to verify the path
base_dir = '../database/'
st.write(f"Contents of the base directory ({base_dir}):")
st.write(os.listdir(base_dir))

# Function to load CSV with error handling and preview the data
def load_and_preview_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        st.write(f"Preview of {file_path}:")
        st.write(df.head())  # Display the first few rows of the dataframe
        return df
    except ValueError as e:
        st.error(f"Error loading {file_path}: {e}")
        st.error(f"Columns available in the file: {pd.read_csv(file_path).columns.tolist()}")
        return pd.DataFrame()  # return empty DataFrame
    except FileNotFoundError as e:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()  # return empty DataFrame

# Load the data from CSV files
fill_levels_df = load_and_preview_csv(f'{base_dir}fill_levels_time.csv')
final_weight_df = load_and_preview_csv(f'{base_dir}final_weight.csv')
temperatures_df = load_and_preview_csv(f'{base_dir}temperatures.csv')

# Function to parse time column if it exists in the dataframes
def parse_time_column(df, time_col_name):
    if time_col_name in df.columns:
        if df[time_col_name].dtype == 'int64' or df[time_col_name].dtype == 'float64':
            df[time_col_name] = pd.to_datetime(df[time_col_name], unit='s')  # Unix timestamp to datetime
        else:
            df[time_col_name] = pd.to_datetime(df[time_col_name])  # General case
    return df

# Parse the 'time' column if it exists
fill_levels_df = parse_time_column(fill_levels_df, 'time')
final_weight_df = parse_time_column(final_weight_df, 'time')
temperatures_df = parse_time_column(temperatures_df, 'time')

# Ensure that all dataframes have the 'time' column
if 'time' not in fill_levels_df.columns or 'time' not in final_weight_df.columns or 'time' not in temperatures_df.columns:
    st.error("One or more dataframes are missing the 'time' column after loading.")
else:
    # Convert pandas Timestamps to datetime.date for the slider
    min_time = fill_levels_df['time'].min()
    max_time = fill_levels_df['time'].max()

    if min_time == max_time :
        st.error("The time range is not valid as min_time and max_time are the same.")
        st.stop()

    min_date = min_time.date()
    max_date = max_time.date()

    # Streamlit app
    st.write("# TeachingFactory Dashboard")

    # Time range slider
    start_time, end_time = st.slider(
        "Select a time range:",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="DD-MM-YYYY"
    )

    # Convert the selected times back to pandas Timestamps
    start_time = pd.Timestamp(start_time)
    end_time = pd.Timestamp(end_time)

    # Filter dataframes based on selected time range
    fill_levels_filtered = fill_levels_df[(fill_levels_df['time'] >= start_time) & (fill_levels_df['time'] <= end_time)]
    final_weight_filtered = final_weight_df[(final_weight_df['time'] >= start_time) & (final_weight_df['time'] <= end_time)]
    temperatures_filtered = temperatures_df[(temperatures_df['time'] >= start_time) & (temperatures_df['time'] <= end_time)]

    tab1, tab2 = st.tabs(["Dashboard", "Rohdaten"])

    with tab1:
        col1, col2, col3 = st.columns(3)

        with col1:
            # Plot fill levels data
            fig1 = px.line(fill_levels_filtered, x='time', y=['level1', 'level2', 'level3'], title='Fill Levels Over Time')
            st.plotly_chart(fig1)

        with col2:
            # Plot final weight data
            fig2 = px.line(final_weight_filtered, x='time', y='final_weight', title='Final Weight Over Time')
            st.plotly_chart(fig2)

        with col3:
            # Plot temperatures data
            fig3 = px.line(temperatures_filtered, x='time', y='temperature', title='Temperatures Over Time')
            st.plotly_chart(fig3)

    with tab2:
        # Display the filtered data
        st.write(f"Displaying data from {start_time.date()} to {end_time.date()}:")
        st.write("### Fill Levels Data")
        st.dataframe(fill_levels_filtered)
        st.write("### Final Weight Data")
        st.dataframe(final_weight_filtered)
        st.write("### Temperatures Data")
        st.dataframe(temperatures_filtered)
