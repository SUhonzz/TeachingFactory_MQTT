import streamlit as st
import pandas as pd
from tinydb import TinyDB, Query
import json

st.set_page_config(layout="wide", page_title="TeachingFactory", page_icon=":gear:")
st.header("Teaching Factory Data Visualisation")

db = TinyDB('../database/db.json')

def get_entries_for_topic(db, topic):
    try:
        # Load the entire JSON data
        with open(db.storage._handle.name) as f:
            data = json.load(f)

        # Retrieve the entries for the given topic
        entries = data.get(topic, {})
        return entries
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def create_disp_df(db, topic):
    df = pd.DataFrame(columns=["index", "bottle", "time", "fill_level_grams"])
    entries = get_entries_for_topic(db, topic)
    for key in entries:
        df.loc[len(df)] = [key, entries[key]['bottle'], entries[key]['time'], entries[key]['fill_level_grams']]
    return df

fill_disp_red = create_disp_df(db, "iot1/teaching_factory_fast/dispenser_red")
fill_disp_blue = create_disp_df(db, "iot1/teaching_factory_fast/dispenser_blue")
fill_disp_green = create_disp_df(db, "iot1/teaching_factory_fast/dispenser_green")


disp_r, disp_b, disp_g = st.tabs(["Dispenser Red", "Dispenser Blue", "Dispenser Green"])

with disp_r:
    st.dataframe(fill_disp_red)

with disp_b:
    st.dataframe(fill_disp_blue)

with disp_g:
    st.dataframe(fill_disp_green)




print(fill_disp_red)
print(fill_disp_blue)
print(fill_disp_green)

#taught_df.loc[len(taught_df)] = [result[i]['title'], result[i]['artist'], result[i]['album']]