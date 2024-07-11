import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(layout='wide', page_title='TeachingFactory Dashboard', page_icon=':factory:')

# Function to load CSV with error handling and preview the data
def load_and_preview_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except ValueError as e:
        st.error(f"Error loading {file_path}: {e}")
        st.error(f"Columns available in the file: {pd.read_csv(file_path).columns.tolist()}")
        return pd.DataFrame()  # return empty DataFrame
    except FileNotFoundError as e:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()  # return empty DataFrame

# Load the data from CSV files
fill_levels_df = load_and_preview_csv('../database/fill_levels_time.csv')
final_weight_df = load_and_preview_csv('../database/final_weight.csv')
temperatures_df = load_and_preview_csv('../database/temperatures.csv')

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
    # Convert pandas Timestamps to datetime for the slider
    min_time = fill_levels_df['time'].min().to_pydatetime()
    max_time = fill_levels_df['time'].max().to_pydatetime()

    if min_time == max_time:
        st.error("The time range is not valid as min_time and max_time are the same.")
        st.stop()

    # Streamlit app
    st.write("# TeachingFactory Dashboard")
    
    start_datetime = min_time
    end_datetime = max_time

    # Create the datetime range slider
    selected_datetimes = st.slider(
        "Select a date and time range",
        min_value=start_datetime,
        max_value=end_datetime,
        value=(start_datetime, end_datetime),
        format="YYYY-MM-DD HH:mm:ss"
    )

    # Display the selected start and end datetimes
    st.write("Selected start date and time:", selected_datetimes[0])
    st.write("Selected end date and time:", selected_datetimes[1])

    # Filter dataframes based on selected time range
    start_time = selected_datetimes[0]
    end_time = selected_datetimes[1]

    fill_levels_filtered = fill_levels_df[(fill_levels_df['time'] >= start_time) & (fill_levels_df['time'] <= end_time)]
    final_weight_filtered = final_weight_df[(final_weight_df['time'] >= start_time) & (final_weight_df['time'] <= end_time)]
    temperatures_filtered = temperatures_df[(temperatures_df['time'] >= start_time) & (temperatures_df['time'] <= end_time)]

    print(temperatures_filtered)

    tab1, tab2 = st.tabs(["Dashboard", "Rohdaten"])

    with tab1:
        col1, col2, col3 = st.columns(3)

        with col1:
            # Check if the necessary columns are present
            if all(col in fill_levels_filtered.columns for col in ['fill_level_grams_red', 'fill_level_grams_blue', 'fill_level_grams_green']):
                fig1 = px.line(fill_levels_filtered, x='time', y=['fill_level_grams_red', 'fill_level_grams_blue', 'fill_level_grams_green'], title='Fill Levels Over Time')
                st.plotly_chart(fig1)
            else:
                st.warning("One or more of the columns 'fill_level_grams_red', 'fill_level_grams_blue', 'fill_level_grams_green' are missing in the filtered data.")

        with col2:
            if 'final_weight' in final_weight_filtered.columns:
                fig2 = px.line(final_weight_filtered, x='time', y='final_weight', title='Final Weight Over Time')
                st.plotly_chart(fig2)
            else:
                st.warning("The column 'final_weight' is missing in the filtered data.")

        with col3:
            if 'temperature_C' in temperatures_filtered.columns:
                fig3 = px.line(temperatures_filtered, x='time', y='temperature_C', title='Temperatures Over Time')
                st.plotly_chart(fig3)
            else:
                st.warning("The column temperature_C is missing in the filtered data.")

    with tab2:

        col2_1, col2_2, col2_3 = st.columns([2,1,1])

        # Display the filtered data
        st.write(f"Displaying data from {start_time.date()} to {end_time.date()}:")
        with col2_1:
            st.write("### Fill Levels Data")
            st.dataframe(fill_levels_filtered)
        with col2_2:
            st.write("### Final Weight Data")
            st.dataframe(final_weight_filtered)
        with col2_3:    
            st.write("### Temperatures Data")
            st.dataframe(temperatures_filtered)
