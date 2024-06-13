import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sensor Data Display", page_icon="📊"
                   , layout="wide", initial_sidebar_state="expanded")

st.title("Sensor Data Display")

# Load the CSV file
@st.cache
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Streamlit app layout
def main():
    st.title("Sensor Data Display")

    # File upload
    file = st.file_uploader("Upload CSV", type=["csv"])

    if file is not None:
        data = load_data(file)
        
        # Display the raw data
        st.subheader("Raw Sensor Data")
        st.write(data)

        # Show a summary of the data
        st.subheader("Data Summary")
        st.write(data.describe())
        
        # Select sensor to visualize
        sensor_options = data.columns[1:]  # Exclude the time column
        selected_sensor = st.selectbox("Select Sensor to Display", sensor_options)
        
        # Plot the selected sensor data
        st.subheader(f"{selected_sensor} Data")
        st.line_chart(data.set_index('time')[selected_sensor])

if __name__ == "__main__":
    main()
